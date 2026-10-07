#!/usr/bin/env python3
"""
Agenda item 2: do macro signals condition next-month returns? Prints data only.
Design and prediction: research/2026-09-25_MACRO_REGIME.md (committed first).

Data: paper/history/fred_macro.json (FRED), options_indices.json (SPTR),
daily_stocks.json (BAC, C). Monthly samples, forward 21 trading days.
Usage: python3 paper/test_macro_regime.py
"""
import bisect, json, math, os

from engine import load, C

HERE = os.path.dirname(os.path.abspath(__file__))
F = json.load(open(os.path.join(HERE, "history", "fred_macro.json")))["series"]
SPTR = json.load(open(os.path.join(HERE, "history", "options_indices.json")))["series"]["SPTR"]


def daily_before(series, d):
    ks = sorted(series)
    i = bisect.bisect_left(ks, d) - 1
    return series[ks[i]] if i >= 0 else None


def monthly_lag2(series, d):
    y, m = int(d[:4]), int(d[5:7]) - 2
    while m <= 0:
        y, m = y - 1, m + 12
    return series.get(f"{y:04d}-{m:02d}-01")


def monthly_back(series, d, months):
    y, m = int(d[:4]), int(d[5:7]) - 2 - months
    while m <= 0:
        y, m = y - 1, m + 12
    return series.get(f"{y:04d}-{m:02d}-01")


def welch(a, b):
    if len(a) < 3 or len(b) < 3:
        return float("nan"), float("nan")
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    va = sum((x - ma) ** 2 for x in a) / (len(a) - 1)
    vb = sum((x - mb) ** 2 for x in b) / (len(b) - 1)
    return ma - mb, (ma - mb) / math.sqrt(va / len(a) + vb / len(b))


def report(name, rows):
    """rows: list of (date, flag, value). Prints the four hurdles."""
    on = [v for _, f, v in rows if f]
    off = [v for _, f, v in rows if not f]
    d, t = welch(on, off)
    print(f"\n{name}: months ON={len(on)} OFF={len(off)}  {rows[0][0]} to {rows[-1][0]}")
    print(f"  ON mean {sum(on) / len(on) * 100:+.2f}%  OFF mean {sum(off) / len(off) * 100:+.2f}%  "
          f"diff {d * 100:+.2f}pp  t={t:+.2f}")
    h = len(rows) // 2
    for lab, part in (("first half", rows[:h]), ("second half", rows[h:])):
        dd, tt = welch([v for _, f, v in part if f], [v for _, f, v in part if not f])
        print(f"    {lab:<11} {part[0][0]}..{part[-1][0]}  diff {dd * 100:+.2f}pp  t={tt:+.2f}")
    k = len(rows)
    signs = []
    for w in range(9):
        part = rows[w * k // 9:(w + 1) * k // 9]
        a = [v for _, f, v in part if f]
        b = [v for _, f, v in part if not f]
        signs.append("n/a" if not a or not b else ("+" if sum(a) / len(a) > sum(b) / len(b) else "-"))
    print(f"  9 windows, sign of ON-minus-OFF: {' '.join(signs)}")
    ex = [(dt, f, v) for dt, f, v in rows if dt[:4] not in ("2008", "2020")]
    dd, tt = welch([v for _, f, v in ex if f], [v for _, f, v in ex if not f])
    print(f"  without 2008 and 2020: diff {dd * 100:+.2f}pp  t={tt:+.2f}")


def main():
    sp_days = sorted(SPTR)
    months, seen = [], set()
    for i, d in enumerate(sp_days):
        if d[:7] not in seen:
            seen.add(d[:7])
            if i + 21 < len(sp_days):
                months.append(i)

    def fwd(i):
        return SPTR[sp_days[i + 21]] / SPTR[sp_days[i]] - 1

    def fvol(i):
        r = [math.log(SPTR[sp_days[j + 1]] / SPTR[sp_days[j]]) for j in range(i, i + 21)]
        m = sum(r) / 21
        return math.sqrt(sum((x - m) ** 2 for x in r) / 20 * 252)

    print("sources: FRED (fred_macro.json), S&P 500 TR (options_indices.json), BAC/C (daily_stocks.json)")
    g1, g2, g3, g3v = [], [], [], []
    for i in months:
        d = sp_days[i]
        c = daily_before(F["T10Y3M"], d)
        if c is not None:
            g1.append((d, c < 0, fwd(i)))
        ff, ff6 = monthly_lag2(F["FEDFUNDS"], d), monthly_back(F["FEDFUNDS"], d, 6)
        if ff is not None and ff6 is not None:
            g2.append((d, ff < ff6, fwd(i)))
        u = monthly_lag2(F["UNRATE"], d)
        hist = [monthly_back(F["UNRATE"], d, k) for k in range(0, 12)]
        if u is not None and all(h is not None for h in hist):
            flag = u - min(hist) >= 0.5
            g3.append((d, flag, fwd(i)))
            g3v.append((d, flag, fvol(i)))
    report("G1 curve inverted (T10Y3M<0)", g1)
    report("G2 Fed cutting (FEDFUNDS below 6 months earlier)", g2)
    report("G3 unemployment rising (>=0.5pt above 12m low), forward RETURN", g3)
    report("G3 same trigger, forward realised VOLATILITY (annualised)", g3v)

    dates, bars, syms = load()
    idx = {d: i for i, d in enumerate(dates)}
    g4 = []
    seen = set()
    t2 = F["T10Y2Y"]
    for i, d in enumerate(dates):
        if d[:7] in seen or i < 64 or i + 21 >= len(dates):
            continue
        seen.add(d[:7])
        now, then = daily_before(t2, d), daily_before(t2, dates[i - 63])
        if now is None or then is None or d not in SPTR or dates[i + 21] not in SPTR:
            continue
        banks = sum(bars[s][i + 21][C] / bars[s][i][C] - 1 for s in ("BAC", "C")) / 2
        mkt = SPTR[dates[i + 21]] / SPTR[d] - 1
        g4.append((d, now > then, banks - mkt))
    report("G4 curve steepening (T10Y2Y up over 63 days): BAC+C minus S&P TR", g4)


if __name__ == "__main__":
    main()
