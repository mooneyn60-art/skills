#!/usr/bin/env python3
"""
Wednesday probe 2026-10-14: does cross-sectional return dispersion predict
SPY return, SPY volatility, or the 200-day above-minus-below spread?
Prints data only (R14.1). Design: research/2026-10-14_DISPERSION.md.

Monthly samples (first trading day). D = mean over the prior 21 days of the
cross-sectional std of daily log returns. Outcomes over the next 21 days.
Usage: python3 paper/test_dispersion.py
"""
import math

from engine import load, C
from test_breadth_vs_vix import ols, vix_on

MEGA = {"AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"}


def build(dates, bars, names):
    spy = bars["SPY"]
    rows, seen = [], set()
    for i, d in enumerate(dates):
        if d[:7] in seen:
            continue
        seen.add(d[:7])
        if i < 221 or i + 21 >= len(dates):
            continue
        v = vix_on(d)
        if v is None:
            continue
        cs = []
        for j in range(i - 21, i):
            r = [math.log(bars[s][j + 1][C] / bars[s][j][C]) for s in names]
            m = sum(r) / len(r)
            cs.append(math.sqrt(sum((x - m) ** 2 for x in r) / (len(r) - 1)))
        disp = sum(cs) / len(cs)
        lr = [math.log(spy[j + 1][C] / spy[j][C]) for j in range(i, i + 21)]
        mu = sum(lr) / 21
        vol = math.sqrt(sum((x - mu) ** 2 for x in lr) / 20 * 252)
        up, dn = [], []
        for s in names:
            sma = sum(b[C] for b in bars[s][i - 199:i + 1]) / 200
            f = bars[s][i + 21][C] / bars[s][i][C] - 1
            (up if bars[s][i][C] > sma else dn).append(f)
        spread = (sum(up) / len(up) - sum(dn) / len(dn)) if up and dn else None
        rows.append(dict(d=d, D=disp * 100, vix=v, ret=spy[i + 21][C] / spy[i][C] - 1, vol=vol, spread=spread))
    return rows


OUT = (("SPY fwd return", "ret"), ("SPY fwd vol", "vol"), ("200d spread", "spread"))


def report(label, rows):
    for oname, k in OUT:
        sub = [r for r in rows if r[k] is not None]
        y = [r[k] for r in sub]
        b1, t1 = ols(y, [[r["D"] for r in sub]])
        b2, t2 = ols(y, [[r["D"] for r in sub], [r["vix"] for r in sub]])
        print(f"  {label:<22} {oname:<15} D alone: coef {b1[1]:+.4f} t={t1[1]:+.2f} | with VIX: D coef {b2[1]:+.4f} "
              f"t={t2[1]:+.2f}, VIX t={t2[2]:+.2f}  (n={len(sub)})")


def main():
    dates, bars, syms = load()
    rows = build(dates, bars, syms)
    Ds = [r["D"] for r in rows]
    vx = [r["vix"] for r in rows]
    md, mv = sum(Ds) / len(Ds), sum(vx) / len(vx)
    corr = sum((a - md) * (b - mv) for a, b in zip(Ds, vx)) / math.sqrt(
        sum((a - md) ** 2 for a in Ds) * sum((b - mv) ** 2 for b in vx))
    print(f"source: daily_stocks.json ({len(syms)} names + SPY), vix_weekly.json; {len(rows)} months "
          f"{rows[0]['d']} to {rows[-1]['d']}")
    print(f"D (daily cross-sectional std, %, 21d mean): mean {md:.2f}, min {min(Ds):.2f}, max {max(Ds):.2f}; "
          f"corr(D, VIX) {corr:+.2f}")
    report("full", rows)
    h = len(rows) // 2
    report(f"first half to {rows[h - 1]['d'][:7]}", rows[:h])
    report("second half", rows[h:])
    report("megacaps dropped (9)", build(dates, bars, [s for s in syms if s not in MEGA]))
    print("  9-window sign of D coefficient (with VIX):")
    k = len(rows)
    for oname, key in OUT:
        signs = []
        for w in range(9):
            sub = [r for r in rows[w * k // 9:(w + 1) * k // 9] if r[key] is not None]
            bb, _ = ols([r[key] for r in sub], [[r["D"] for r in sub], [r["vix"] for r in sub]])
            signs.append("+" if bb[1] > 0 else "-")
        print(f"    {oname:<15} {' '.join(signs)}  (+ count {signs.count('+')} of 9)")

    print("\nADDED AFTER THE FIRST RUN (post hoc subgroup checks, not part of the committed design):")
    report("excl 2008-2009", [r for r in rows if r["d"][:4] not in ("2008", "2009")])
    report("excl 2020", [r for r in rows if r["d"][:4] != "2020"])
    sub = sorted((r for r in rows if r["spread"] is not None), key=lambda r: r["D"])
    q = len(sub) // 3
    for lab, g in (("low D third", sub[:q]), ("middle third", sub[q:2 * q]), ("high D third", sub[2 * q:])):
        s = [r["spread"] for r in g]
        m = sum(s) / len(s)
        sd = math.sqrt(sum((x - m) ** 2 for x in s) / (len(s) - 1))
        print(f"  {lab:<13} n={len(g)} D {g[0]['D']:.2f}-{g[-1]['D']:.2f}  mean 200d spread {m * 100:+.2f}pp "
              f"t={m / (sd / math.sqrt(len(s))):+.2f}")


if __name__ == "__main__":
    main()
