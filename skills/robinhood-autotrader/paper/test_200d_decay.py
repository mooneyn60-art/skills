#!/usr/bin/env python3
"""
Agenda item 20: has the 200-day gate's evidence decayed? Prints data only.
Design and prediction: research/2026-09-24_DOES_THE_PAST_STILL_APPLY.md.

Monthly samples (first trading day), forward 21 trading days,
paper/history/daily_stocks.json. Per era:
  D1  14 stocks: mean fwd return ABOVE 200-day minus BELOW, per month, t
  D2  SPY: mean fwd return above / below, and fwd realized vol above / below
Usage: python3 paper/test_200d_decay.py
"""
import math

from engine import load, C

ERAS = [("2007-2011", "2007", "2012"), ("2012-2016", "2012", "2017"),
        ("2017-2021", "2017", "2022"), ("2022-2026", "2022", "2027")]


def mt(xs):
    n = len(xs)
    if n < 3:
        return n, float("nan"), float("nan")
    m = sum(xs) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
    return n, m, m / (sd / math.sqrt(n))


def main():
    dates, bars, syms = load()
    months, seen = [], set()
    for i, d in enumerate(dates):
        if d[:7] not in seen:
            seen.add(d[:7])
            if 200 <= i < len(dates) - 21:
                months.append(i)
    sma = lambda s, i: sum(b[C] for b in bars[s][i - 199:i + 1]) / 200
    fwd = lambda s, i: bars[s][i + 21][C] / bars[s][i][C] - 1

    def fvol(s, i):
        r = [math.log(bars[s][j + 1][C] / bars[s][j][C]) for j in range(i, i + 21)]
        m = sum(r) / 21
        return math.sqrt(sum((x - m) ** 2 for x in r) / 20) * math.sqrt(252)

    print("source: paper/history/daily_stocks.json; monthly samples; forward 21 trading days")
    print("D1  14 stocks, above-minus-below 200-day forward return, per month")
    for lab, a, b in ERAS:
        spreads = []
        for i in months:
            if not (a <= dates[i] < b):
                continue
            up = [fwd(s, i) for s in syms if bars[s][i][C] > sma(s, i)]
            dn = [fwd(s, i) for s in syms if bars[s][i][C] <= sma(s, i)]
            if up and dn:
                spreads.append(sum(up) / len(up) - sum(dn) / len(dn))
        n, m, t = mt(spreads)
        print(f"  {lab}  months={n:>3}  spread {m * 100:+6.2f}pp  t={t:+5.2f}")

    print("D2  SPY alone")
    for lab, a, b in ERAS:
        up_r, dn_r, up_v, dn_v = [], [], [], []
        for i in months:
            if not (a <= dates[i] < b):
                continue
            if bars["SPY"][i][C] > sma("SPY", i):
                up_r.append(fwd("SPY", i)); up_v.append(fvol("SPY", i))
            else:
                dn_r.append(fwd("SPY", i)); dn_v.append(fvol("SPY", i))
        avg = lambda x: sum(x) / len(x) if x else float("nan")
        ratio = avg(dn_v) / avg(up_v) if up_v and dn_v else float("nan")
        print(f"  {lab}  above n={len(up_r):>2} fwd {avg(up_r) * 100:+5.2f}% vol {avg(up_v) * 100:4.1f}%   "
              f"below n={len(dn_r):>2} fwd {avg(dn_r) * 100:+5.2f}% vol {avg(dn_v) * 100:4.1f}%   "
              f"vol ratio below/above {ratio:.2f}")


if __name__ == "__main__":
    main()
