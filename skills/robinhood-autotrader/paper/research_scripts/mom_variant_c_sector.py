#!/usr/bin/env python3
"""Variant (c) sector rotation: keep only candidates in the top-3 sectors by mean 6-1
momentum (close[i-21]/close[i-126]-1) over ALL names in ctx["syms"] with valid bars at i-126.
Ranking within them stays 12-1. Prints data only (R14)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mom_screen_base import *


def sector_means(ctx):
    bars, i = ctx["bars"], ctx["i"]
    acc = {}
    for s in ctx["syms"]:
        seq = bars[s]
        if i - 126 < 0 or seq[i - 126] is None or seq[i - 21] is None:
            continue
        acc.setdefault(SECTORS[s], []).append(seq[i - 21][C] / seq[i - 126][C] - 1)
    return {k: sum(v) / len(v) for k, v in acc.items()}


def f(cands, ctx):
    m = sector_means(ctx)
    top = set(sorted(m, key=lambda k: -m[k])[:3])
    return [(s, sc) for s, sc in cands if SECTORS[s] in top]


hurdles("variant c sector top3", "LONG", pick_filter=f)
hurdles("variant c sector top3", "WIDE", pick_filter=f)

# Extra data: recorder runs the BASELINE (filter returns cands unchanged) and logs per rebalance.
for u in ("LONG", "WIDE"):
    dates, bars, spyb = load(u)
    lo = "2006-01-01" if u == "LONG" else "2021-12-01"
    log = []

    def rec(cands, ctx):
        m = sector_means(ctx)
        top = set(sorted(m, key=lambda k: -m[k])[:3])
        base8 = [s for s, _ in cands[:8]]
        kept = [s for s in base8 if SECTORS[s] in top]
        log.append((len(m), len(base8), len(base8) - len(kept), len(cands),
                    sum(1 for s, _ in cands if SECTORS[s] in top)))
        return cands
    run(dates, bars, spyb, start=lo, pick_filter=rec)
    n = len(log)
    withc = [x for x in log if x[1] > 0]
    removed = sum(1 for x in withc if x[2] > 0)
    print(f"\n=== extra data | universe {u} ({len(bars)} names) ===")
    print(f"  rebalances {n}; rebalances with >=1 candidate {len(withc)}")
    print(f"  mean distinct sectors with >=1 valid name (bars at i-126): {sum(x[0] for x in log)/n:.2f}  "
          f"(min {min(x[0] for x in log)}, max {max(x[0] for x in log)})")
    print(f"  top-3 filter removes >=1 of baseline's top-8 (first 8 of ranked eligible list, pre sector cap): "
          f"{removed} of {len(withc)} rebalances with candidates = {removed/len(withc)*100:.1f}% "
          f"({removed/n*100:.1f}% of all rebalances)")
    print(f"  mean top-8 picks removed per rebalance (with candidates): {sum(x[2] for x in withc)/len(withc):.2f}; "
          f"mean eligible cands {sum(x[3] for x in log)/n:.2f} -> after filter {sum(x[4] for x in log)/n:.2f}")
print("\nCaveat (data): sector labels are hand-assigned in mom_screen_base.py SECTORS (lines 40-54); "
      "volatile/holdings labels are 'hand-assigned, Robinhood-style' per source comment.")
