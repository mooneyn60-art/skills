#!/usr/bin/env python3
"""
Agenda item 13: does the CBOE equity put/call ratio add anything VIX doesn't?
Prints data only (R14.1). Design: research/2026-10-04_SENTIMENT_PUTCALL.md.

Monthly samples (first trading day), signal = 10-day average equity P/C
ending the prior trading day, outcome = SPY forward 21 trading days.
Usage: python3 paper/test_sentiment_putcall.py
"""
import csv, math, os
from datetime import datetime

from engine import load, C
from test_breadth_vs_vix import ols, vix_on

HERE = os.path.dirname(os.path.abspath(__file__))


def load_pc():
    out = {}
    for row in csv.reader(open(os.path.join(HERE, "history", "cboe_equity_putcall.csv"))):
        if len(row) < 5:
            continue
        try:
            d = datetime.strptime(row[0].strip(), "%m/%d/%Y").strftime("%Y-%m-%d")
            out[d] = float(row[4])
        except ValueError:
            continue
    return out


def main():
    pc = load_pc()
    pk = sorted(pc)
    dates, bars, _ = load()
    spy = bars["SPY"]
    rows, seen = [], set()
    for i, d in enumerate(dates):
        if d[:7] in seen:
            continue
        seen.add(d[:7])
        if i + 21 >= len(dates) or d <= pk[10] or d > pk[-1]:
            continue
        prior = [x for x in pk if x < d][-10:]
        if len(prior) < 10:
            continue
        sig = sum(pc[x] for x in prior) / 10
        v = vix_on(d)
        if v is None:
            continue
        r = [math.log(spy[j + 1][C] / spy[j][C]) for j in range(i, i + 21)]
        m = sum(r) / 21
        vol = math.sqrt(sum((x - m) ** 2 for x in r) / 20 * 252)
        rows.append((d, sig, v, spy[i + 21][C] / spy[i][C] - 1, vol))
    sigs = [x[1] for x in rows]
    print(f"source: cboe_equity_putcall.csv (CBOE), daily_stocks.json SPY, vix_weekly.json; "
          f"{len(rows)} months {rows[0][0]} to {rows[-1][0]}")
    print(f"10-day equity P/C: mean {sum(sigs) / len(sigs):.3f}, min {min(sigs):.3f}, max {max(sigs):.3f}")

    def run(label, sub):
        p = [x[1] for x in sub]
        vx = [x[2] for x in sub]
        for oname, idx in (("fwd return", 3), ("fwd volatility", 4)):
            y = [x[idx] for x in sub]
            b1, t1 = ols(y, [p])
            b2, t2 = ols(y, [p, vx])
            print(f"  {label:<16} {oname:<15} P/C alone: coef {b1[1]:+.4f} t={t1[1]:+.2f} | "
                  f"with VIX: P/C coef {b2[1]:+.4f} t={t2[1]:+.2f}, VIX t={t2[2]:+.2f}  (n={len(sub)})")

    run("full", rows)
    h = len(rows) // 2
    run("first half", rows[:h])
    run("second half", rows[h:])
    run("without 2008", [x for x in rows if x[0][:4] != "2008"])
    print("  9-window sign of the P/C coefficient (with VIX):")
    for oname, idx in (("fwd return", 3), ("fwd volatility", 4)):
        k, signs = len(rows), []
        for w in range(9):
            sub = rows[w * k // 9:(w + 1) * k // 9]
            bb, _ = ols([x[idx] for x in sub], [[x[1] for x in sub], [x[2] for x in sub]])
            signs.append("+" if bb[1] > 0 else "-")
        print(f"    {oname:<15} {' '.join(signs)}")


if __name__ == "__main__":
    main()
