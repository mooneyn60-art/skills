#!/usr/bin/env python3
"""
Wednesday probe 2026-10-21: does the first hour's path efficiency (ER1)
predict the rest-of-day trend-ness (E2) or continuation? Prints data only.
Design and prediction: research/2026-10-21_DAY_TYPE_FIRST_HOUR.md (committed first).
Data: paper/history/spy_5min.json (Robinhood 5-min, regular session).
Usage: python3 paper/research_scripts/day_type_first_hour.py
"""
import json, math, os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
H = os.path.join(HERE, "..", "history")
raw = json.load(open(os.path.join(H, "spy_5min.json")))
fomc = set(json.load(open(os.path.join(H, "fomc_dates.json")))["scheduled"])

days = defaultdict(list)
for ts in sorted(raw):
    days[ts[:10]].append(raw[ts])

rows, skipped = [], 0
for d, b in sorted(days.items()):
    if len(b) < 78:          # half days / gaps
        skipped += 1
        continue
    b = b[:78]
    o = b[0][0]
    first = b[:12]
    p1030 = first[-1][3]
    path = abs(first[0][3] - o) + sum(abs(first[k][3] - first[k - 1][3]) for k in range(1, 12))
    er1 = abs(p1030 - o) / path if path else 0.0
    rest = b[12:]
    hi, lo = max(x[1] for x in rest), min(x[2] for x in rest)
    cl = rest[-1][3]
    e2 = abs(cl - p1030) / (hi - lo) if hi > lo else 0.0
    s1 = 1 if p1030 > o else -1
    cont = (cl - p1030) / p1030 * s1 * 100          # % move in the first hour's direction
    rng = (max(x[1] for x in b) - min(x[2] for x in b)) / o
    rows.append(dict(d=d, er1=er1, e2=e2, cont=cont, rng=rng, fomc=d in fomc,
                     fh_move=(p1030 - o) / o * 100))


def corr(x, y):
    n = len(x); mx, my = sum(x) / n, sum(y) / n
    sx = math.sqrt(sum((a - mx) ** 2 for a in x)); sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)


def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v)
    for k, i in enumerate(o):
        r[i] = k
    return r


def slope_t(x, y):
    n = len(x); mx, my = sum(x) / n, sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x)
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sxx
    res = [c - my - b * (a - mx) for a, c in zip(x, y)]
    se = math.sqrt(sum(r * r for r in res) / (n - 2) / sxx)
    return b, b / se


def mt(v):
    n = len(v); m = sum(v) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in v) / (n - 1)) if n > 1 else float("nan")
    return m, (m / (sd / math.sqrt(n)) if sd else float("nan"))


def report(label, R):
    x, y = [r["er1"] for r in R], [r["e2"] for r in R]
    b, t = slope_t(x, y)
    print(f"  {label:<26} n={len(R):>3}  E2~ER1 slope {b:+.3f} t={t:+.2f}  pearson {corr(x, y):+.3f}  "
          f"spearman {corr(rank(x), rank(y)):+.3f}")
    srt = sorted(R, key=lambda r: r["er1"]); q = len(srt) // 3
    for lab, g in (("low ER1", srt[:q]), ("mid ER1", srt[q:2 * q]), ("high ER1", srt[2 * q:])):
        e2m = sum(r["e2"] for r in g) / len(g)
        cm, ct = mt([r["cont"] for r in g])
        hit = sum(1 for r in g if r["cont"] > 0) / len(g)
        print(f"      {lab:<9} ER1 {g[0]['er1']:.2f}-{g[-1]['er1']:.2f}  mean E2 {e2m:.3f}  continuation "
              f"{hit * 100:4.0f}% mean {cm:+.3f}% t={ct:+.2f}")


print(f"source: spy_5min.json, {len(rows)} full sessions {rows[0]['d']} to {rows[-1]['d']} "
      f"(skipped {skipped} short days); FOMC days in sample {sum(r['fomc'] for r in rows)}")
print(f"ER1 mean {sum(r['er1'] for r in rows) / len(rows):.3f}; E2 mean {sum(r['e2'] for r in rows) / len(rows):.3f}")
report("full", rows)
h = len(rows) // 2
report(f"1st half to {rows[h - 1]['d']}", rows[:h])
report("2nd half", rows[h:])
big = sorted(rows, key=lambda r: -r["rng"])[:5]
report("drop 5 widest-range days", [r for r in rows if r not in big])
report("drop FOMC days", [r for r in rows if not r["fomc"]])
k = len(rows); signs, cs = [], []
for w in range(9):
    sub = rows[w * k // 9:(w + 1) * k // 9]
    b, _ = slope_t([r["er1"] for r in sub], [r["e2"] for r in sub])
    signs.append("+" if b > 0 else "-")
    srt = sorted(sub, key=lambda r: r["er1"]); q = len(srt) // 3
    cs.append(sum(r["cont"] for r in srt[2 * q:]) / len(srt[2 * q:]) - sum(r["cont"] for r in srt[:q]) / q)
print(f"  9 windows, sign of E2~ER1 slope: {' '.join(signs)}  (+ {signs.count('+')} of 9)")
print(f"  9 windows, high-minus-low ER1 continuation (pp): {' '.join(f'{c:+.2f}' for c in cs)}  "
      f"(+ {sum(c > 0 for c in cs)} of 9)")
