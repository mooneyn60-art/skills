#!/usr/bin/env python3
"""
Agenda item 17: anatomy of INTC's rally. Prints data only (R14.1).
Design and prediction: research/2026-09-24_INTC_CASE_STUDY.md.

Prices: paper/history/book_daily.json (Yahoo adjusted closes, 3 years),
written by paper/test_why_prices_move.py.
Earnings: SEC EDGAR companyfacts for INTC (filer 50863), net income as
reported in each 10-Q/10-K, via fetch_fundamentals.derive().
Usage: python3 paper/test_intc_case.py
"""
import json, math, os, urllib.request

from fetch_fundamentals import derive, UA

HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, "history", "book_daily.json")))["prices"]


def main():
    days = sorted(set(P["INTC"]) & set(P["SMH"]))
    px = [P["INTC"][d] for d in days]
    smh = [P["SMH"][d] for d in days]
    last_year = [i for i, d in enumerate(days) if d >= days[-1][:4] + "-00"][0] - 252
    start = max(0, len(days) - 300)
    lo = min(range(start, len(days)), key=lambda i: px[i])
    hi = max(range(lo, len(days)), key=lambda i: px[i])
    total = math.log(px[hi] / px[lo])
    print(f"source: book_daily.json, INTC adjusted closes {days[0]} to {days[-1]}")
    print(f"low  {days[lo]} {px[lo]:.2f}   high {days[hi]} {px[hi]:.2f}   last {days[-1]} {px[-1]:.2f}")
    print(f"log gain low->high {total:.3f} ({px[hi] / px[lo]:.2f}x) over {hi - lo} trading days")

    rets = [(days[i], math.log(px[i] / px[i - 1]), math.log(smh[i] / smh[i - 1]))
            for i in range(lo + 1, hi + 1)]
    ups = sorted(rets, key=lambda r: -r[1])
    for n in (5, 10, 20):
        share = sum(r[1] for r in ups[:n]) / total
        print(f"  top {n:>2} up-days: {share * 100:5.1f}% of the log gain")
    print("  the 10 biggest up-days (date, INTC, SMH same day):")
    for d, r, s in ups[:10]:
        print(f"    {d}  INTC {math.exp(r) * 100 - 100:+6.1f}%   SMH {math.exp(s) * 100 - 100:+5.1f}%")
    pos_days = sum(1 for r in rets if r[1] > 0)
    print(f"  up-days {pos_days} of {len(rets)}; sum of all SMH log moves over the window "
          f"{sum(r[2] for r in rets):.3f} vs INTC {total:.3f}")

    cross = None
    for i in range(max(lo, 200), len(days)):
        sma = sum(px[i - 199:i + 1]) / 200
        if px[i] > sma:
            cross = i
            break
    if cross is not None:
        cap_hi = math.log(px[hi] / px[cross]) / total
        print(f"first close above 200-day after the low: {days[cross]} at {px[cross]:.2f} "
              f"({cross - lo} trading days after the low)")
        print(f"  share of the low->high log move from that close to the high: {cap_hi * 100:.1f}%")
        print(f"  closes above the 200-day from then to the last day: "
              f"{sum(1 for j in range(cross, len(days)) if px[j] > sum(px[j - 199:j + 1]) / 200)} of {len(days) - cross}")

    req = urllib.request.Request("https://data.sec.gov/api/xbrl/companyfacts/CIK0000050863.json",
                                 headers={"User-Agent": UA})
    gaap = json.load(urllib.request.urlopen(req, timeout=60))["facts"]["us-gaap"]
    rows = sorted(derive(gaap), key=lambda r: r["filed"])
    print("INTC net income as filed (SEC EDGAR, same-filing comparative), filings since 2024:")
    for r in rows:
        if r["filed"] >= "2024" and r.get("net_income"):
            g = r["net_income"]
            print(f"  filed {r['filed']} {r['form']:<5} period end {g['end']}  "
                  f"net income {g['cur'] / 1e9:+6.2f}B  (year earlier {g['prior'] / 1e9:+6.2f}B)")


if __name__ == "__main__":
    main()
