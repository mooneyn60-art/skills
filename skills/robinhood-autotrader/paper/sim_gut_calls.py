#!/usr/bin/env python3
"""
Agenda item 21: how many binary gut calls before an edge over the market's
own probability is distinguishable from zero at t = 2? Prints data only.
Per call: market probability p ~ Uniform(0.30, 0.60) (the range of calls so
far); the caller's true hit probability is p + edge; score = hit - p.
For each n, the share of 20,000 simulated records reaching t >= 2 (power).
Usage: python3 paper/sim_gut_calls.py
"""
import math, random

random.seed(7)
TRIALS = 20000


def power(edge, n):
    hits = 0
    for _ in range(TRIALS):
        xs = []
        for _ in range(n):
            p = random.uniform(0.30, 0.60)
            xs.append((1.0 if random.random() < p + edge else 0.0) - p)
        m = sum(xs) / n
        sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
        hits += sd > 0 and m / (sd / math.sqrt(n)) >= 2
    return hits / TRIALS


print("share of simulated records reaching t >= 2 (power), by true edge and number of calls")
for edge in (0.05, 0.10, 0.20):
    row = []
    for n in (10, 25, 50, 100, 200, 400):
        row.append(f"n={n}: {power(edge, n) * 100:4.0f}%")
    print(f"  edge +{edge * 100:.0f} pts  " + "  ".join(row))
print(f"  edge 0 (no skill), n=100: {power(0.0, 100) * 100:.1f}% false positives")
print("formula n = (2 x 0.5 / edge)^2 gives the n where the EXPECTED t is 2 (about 50% power):",
      {f'+{e * 100:.0f}': round((2 * 0.5 / e) ** 2) for e in (0.05, 0.10, 0.20)})
