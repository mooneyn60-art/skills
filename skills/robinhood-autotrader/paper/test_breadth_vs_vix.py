#!/usr/bin/env python3
"""
Agenda item 11: does breadth add anything VIX doesn't? Prints data only.
Design and prediction: research/2026-09-30_BREADTH_VS_VIX.md (committed first).

Breadth = share of the 14 backtest names above their 200-day SMA.
Monthly samples (first trading day), forward 21 trading days of SPY.
VIX: vix_weekly.json, value dated >= 7 calendar days before the day.
Usage: python3 paper/test_breadth_vs_vix.py
"""
import bisect, json, math, os
from datetime import date, timedelta

from engine import load, C

HERE = os.path.dirname(os.path.abspath(__file__))
VIX = json.load(open(os.path.join(HERE, "history", "vix_weekly.json")))
VK = sorted(VIX)


def vix_on(d):
    cut = (date.fromisoformat(d) - timedelta(days=7)).isoformat()
    i = bisect.bisect_right(VK, cut) - 1
    return VIX[VK[i]] if i >= 0 else None


def inv(m):
    n = len(m)
    a = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(m)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(a[r][c]))
        a[c], a[p] = a[p], a[c]
        piv = a[c][c]
        a[c] = [x / piv for x in a[c]]
        for r in range(n):
            if r != c:
                f = a[r][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [row[n:] for row in a]


def ols(y, cols):
    """Coefficients and classical t-stats; cols excludes the intercept."""
    n = len(y)
    X = [[1.0] + [c[i] for c in cols] for i in range(n)]
    k = len(X[0])
    xtx = [[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(k)] for a in range(k)]
    xty = [sum(X[i][a] * y[i] for i in range(n)) for a in range(k)]
    ixtx = inv(xtx)
    beta = [sum(ixtx[a][b] * xty[b] for b in range(k)) for a in range(k)]
    res = [y[i] - sum(beta[a] * X[i][a] for a in range(k)) for i in range(n)]
    s2 = sum(r * r for r in res) / (n - k)
    se = [math.sqrt(s2 * ixtx[a][a]) for a in range(k)]
    return beta, [b / s for b, s in zip(beta, se)]


def main():
    dates, bars, syms = load()
    spy = bars["SPY"]
    rows, seen = [], set()
    for i, d in enumerate(dates):
        if d[:7] in seen:
            continue
        seen.add(d[:7])
        if i < 200 or i + 21 >= len(dates):
            continue
        v = vix_on(d)
        if v is None:
            continue
        above = sum(1 for s in syms if bars[s][i][C] > sum(b[C] for b in bars[s][i - 199:i + 1]) / 200)
        r = [math.log(spy[j + 1][C] / spy[j][C]) for j in range(i, i + 21)]
        m = sum(r) / 21
        vol = math.sqrt(sum((x - m) ** 2 for x in r) / 20 * 252)
        rows.append((d, above / len(syms), v, spy[i + 21][C] / spy[i][C] - 1, vol))
    print(f"source: daily_stocks.json ({len(syms)} names + SPY), vix_weekly.json; "
          f"{len(rows)} months {rows[0][0]} to {rows[-1][0]}")
    b = [x[1] for x in rows]
    print(f"breadth: mean {sum(b) / len(b):.2f}, months below 0.30: {sum(1 for x in b if x < 0.3)}, "
          f"above 0.70: {sum(1 for x in b if x > 0.7)}")

    def run(label, sub):
        br = [x[1] for x in sub]
        vx = [x[2] for x in sub]
        for oname, idx in (("fwd return", 3), ("fwd volatility", 4)):
            y = [x[idx] for x in sub]
            b1, t1 = ols(y, [br])
            b2, t2 = ols(y, [br, vx])
            print(f"  {label:<26} {oname:<15} breadth alone: coef {b1[1]:+.4f} t={t1[1]:+.2f} | "
                  f"with VIX: breadth coef {b2[1]:+.4f} t={t2[1]:+.2f}, VIX t={t2[2]:+.2f}  (n={len(sub)})")

    run("full", rows)
    h = len(rows) // 2
    run("first half", rows[:h])
    run("second half", rows[h:])
    run("without 2008 and 2020", [x for x in rows if x[0][:4] not in ("2008", "2020")])
    print("  9-window sign of the breadth coefficient (with VIX in the regression):")
    for oname, idx in (("fwd return", 3), ("fwd volatility", 4)):
        signs = []
        k = len(rows)
        for w in range(9):
            sub = rows[w * k // 9:(w + 1) * k // 9]
            try:
                bb, _ = ols([x[idx] for x in sub], [[x[1] for x in sub], [x[2] for x in sub]])
                signs.append("+" if bb[1] > 0 else "-")
            except ZeroDivisionError:
                signs.append("n/a")
        print(f"    {oname:<15} {' '.join(signs)}")


if __name__ == "__main__":
    main()
