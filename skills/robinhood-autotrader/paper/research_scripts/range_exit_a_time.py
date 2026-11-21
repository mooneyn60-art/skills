#!/usr/bin/env python3
"""Variant (a): 21-trading-day time exit on the range-regime entry. Data only (R14)."""
from range_exit_base import run, hurdles


def time21(p, seq, i, rng):
    return i - p["d0"] >= 21


if __name__ == "__main__":
    hurdles("variant a: 21-day time exit", time21)
    for ent in ("bottom", "top"):
        tr = run(time21, ent)["trades"]
        print(f"\n  exit-reason split, {ent} entry (n={len(tr)}):")
        for why in ("stop", "exit_rule"):
            g = [t for t in tr if t["why"] == why]
            if g:
                print(f"    {why:<10} n={len(g):>4}  share {len(g)/len(tr)*100:5.1f}%  avg ret {sum(t['ret'] for t in g)/len(g)*100:+.2f}%  "
                      f"win {sum(t['ret']>0 for t in g)/len(g)*100:4.0f}%  avg hold {sum(t['hold'] for t in g)/len(g):5.1f}d")
