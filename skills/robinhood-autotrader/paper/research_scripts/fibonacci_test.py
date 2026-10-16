"""
Do Fibonacci retracement levels (38.2%, 50%, 61.8%) act as support on SPY
more than nearby non-Fibonacci control levels? Prints data only (R14).

Method (daily, 2006-2026): an up-swing = the 20-day low followed by the
20-day high (low comes first). When price first trades down into a level
L = H - f*(H-L) (bar low <= level <= prior close), record the next 5-day
return from the level and whether the bar closed back above the level
(a "hold"). Compare f in {0.382, 0.5, 0.618} with controls {0.30, 0.44, 0.70}.
Non-overlapping: one touch per level per swing.
"""
import json, math
from pathlib import Path
from statistics import mean, pstdev

D = json.load(open(Path(__file__).resolve().parents[1] / "history" / "daily_ohlcv.json"))["SPY"]
days = sorted(D)
O = [D[d][0] for d in days]; H = [D[d][1] for d in days]; L = [D[d][2] for d in days]; C = [D[d][3] for d in days]
LEVELS = {"fib 38.2": .382, "fib 50.0": .5, "fib 61.8": .618, "ctrl 30.0": .30, "ctrl 44.0": .44, "ctrl 70.0": .70}
res = {k: [] for k in LEVELS}
seen = set()
for i in range(25, len(days) - 6):
    w = range(i - 20, i)
    hi_i = max(w, key=lambda j: H[j]); lo_i = min(w, key=lambda j: L[j])
    if lo_i >= hi_i:
        continue
    hi, lo = H[hi_i], L[lo_i]
    if (hi - lo) / lo < 0.03:
        continue
    for name, f in LEVELS.items():
        lvl = hi - f * (hi - lo)
        key = (name, lo_i, hi_i)
        if key in seen:
            continue
        if L[i] <= lvl <= C[i - 1]:
            seen.add(key)
            res[name].append((C[i + 5] / lvl - 1, C[i] > lvl))
print(f"SPY daily {days[0]}..{days[-1]}, swings >= 3%")
print(f"  {'level':<10} {'n':>4} {'next 5d avg':>11} {'t':>6} {'close back above (hold%)':>25}")
for name, r in res.items():
    if len(r) < 3:
        continue
    x = [a for a, _ in r]
    t = mean(x) / (pstdev(x) / math.sqrt(len(x))) if pstdev(x) > 0 else float('nan')
    print(f"  {name:<10} {len(r):>4} {100*mean(x):>+10.2f}% {t:>6.2f} {100*mean(h for _, h in r):>24.0f}%")
