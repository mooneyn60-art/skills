#!/usr/bin/env python3
"""
Agenda item 4: correlation inside the book. Prints data only (R14.1).
Design: research/2026-09-25_BOOK_CORRELATION.md (committed first).
Usage: python3 paper/test_book_correlation.py
"""
import json, math, os
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
HOLD = json.load(open(os.path.join(HERE, "history", "daily_ohlcv_holdings.json")))
BOOK = json.load(open(os.path.join(HERE, "history", "book_daily.json")))["prices"]
NAMES = ["NVDA", "SOFI", "INTC", "TGT", "ABBV", "EXEL", "NWG", "CVE"]
SAME = {("INTC", "NVDA"), ("NWG", "SOFI")}


def closes(s):
    if s in ("NVDA", "SPY"):
        return BOOK[s]
    return {d: v[3] for d, v in HOLD[s].items()}


def corr(a, b):
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    va = sum((x - ma) ** 2 for x in a)
    vb = sum((y - mb) ** 2 for y in b)
    return cov / math.sqrt(va * vb)


def main():
    px = {s: closes(s) for s in NAMES + ["SPY"]}
    days = sorted(set.intersection(*(set(v) for v in px.values())))
    days = [d for d in days if d >= "2023-09-25"]
    ret = {s: [px[s][b] / px[s][a] - 1 for a, b in zip(days, days[1:])] for s in px}
    stress = [i for i, r in enumerate(ret["SPY"]) if r < -0.015]
    print(f"sources: daily_ohlcv_holdings.json, book_daily.json (NVDA, SPY); {days[0]} to {days[-1]}, "
          f"{len(days) - 1} daily returns; stress days (SPY < -1.5%): {len(stress)}")

    def table(idx, label):
        pairs = {}
        for a, b in combinations(NAMES, 2):
            pairs[(a, b)] = corr([ret[a][i] for i in idx], [ret[b][i] for i in idx])
        allv = list(pairs.values())
        same = [v for k, v in pairs.items() if tuple(sorted(k)) in SAME]
        cross = [v for k, v in pairs.items() if tuple(sorted(k)) not in SAME]
        avg = sum(allv) / len(allv)
        n = len(NAMES)
        neff = n / (1 + (n - 1) * avg)
        print(f"\n{label}: average pairwise {avg:+.3f}  same-sector {sum(same) / len(same):+.3f} "
              f"(NVDA-INTC {pairs[('NVDA', 'INTC')]:+.3f}, SOFI-NWG {pairs[('SOFI', 'NWG')]:+.3f})  "
              f"cross-sector {sum(cross) / len(cross):+.3f}  N_eff {neff:.2f} of {n}")
        top = sorted(pairs.items(), key=lambda kv: -kv[1])
        print("  highest: " + ", ".join(f"{a}-{b} {v:+.2f}" for (a, b), v in top[:6]))
        print("  lowest:  " + ", ".join(f"{a}-{b} {v:+.2f}" for (a, b), v in top[-4:]))
        return pairs

    allp = table(range(len(ret["SPY"])), "C1/C3 all days")
    strp = table(stress, "C2/C3 stress days")
    diffs = [strp[k] - allp[k] for k in allp]
    print(f"\nC2 change on stress days: average {sum(diffs) / len(diffs):+.3f}, "
          f"{sum(1 for x in diffs if x > 0)} of {len(diffs)} pairs higher")
    print("\ncorrelation with SPY, all days: " +
          ", ".join(f"{s} {corr(ret[s], ret['SPY']):+.2f}" for s in NAMES))


if __name__ == "__main__":
    main()
