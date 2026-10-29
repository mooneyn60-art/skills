#!/usr/bin/env python3
"""Calibration check (brain habit 5): are my 70% calls right about 70% of the time?
Reads PREDICTIONS.jsonl (settled rows have "hit" 0/1), prints hit rate per confidence band, my average Brier score,
and the Brier of always saying 50% (0.25). Lower Brier is better. Needs ~20+ settled calls before it means much.
Run monthly (GROWTH backlog item done 2026-10-24) and before trusting my own gut on a new kind of call."""
import json
from pathlib import Path
rows = [json.loads(l) for l in open(Path(__file__).with_name("PREDICTIONS.jsonl")) if l.strip()]
done = [r for r in rows if r.get("hit") in (0, 1)]
open_ = [r for r in rows if r.get("hit") not in (0, 1)]
print(f"{len(done)} settled, {len(open_)} open")
if not done:
    raise SystemExit
bands = [(0, .35, "<35%"), (.35, .5, "35-50%"), (.5, .65, "50-65%"), (.65, .8, "65-80%"), (.8, 1.01, "80%+")]
for lo, hi, lab in bands:
    b = [r for r in done if lo <= r["p"] < hi]
    if b:
        print(f"  said {lab:7s}: n {len(b):2d}, average said {sum(r['p'] for r in b) / len(b):.0%}, actually hit {sum(r['hit'] for r in b) / len(b):.0%}")
brier = sum((r["p"] - r["hit"]) ** 2 for r in done) / len(done)
print(f"My Brier {brier:.3f} vs coin-flip 0.250 ({'better' if brier < 0.25 else 'not better'} than saying 50% every time)")
if len(done) < 20:
    print(f"Only {len(done)} calls: too few to judge calibration. Keep logging every probability I give Nolan.")
