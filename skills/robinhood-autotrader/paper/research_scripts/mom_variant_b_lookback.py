#!/usr/bin/env python3
"""Variant (b): 6-1 momentum = close[i-21]/close[i-126]-1. Data only (R14.1).
The harness 252-bar history requirement (i - first_valid >= 252) is UNCHANGED for
like-for-like comparison; only the score changes."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mom_screen_base as mb
from mom_screen_base import C, hurdles


def mom_6_1(seq, i):
    if i - 126 < 0 or seq[i - 126] is None:
        return None
    return seq[i - 21][C] / seq[i - 126][C] - 1


def ranked(bars, syms, i, score_fn):
    """Same candidate construction as harness run() step 4 (no sector cap, no portfolio state)."""
    out = []
    for s in syms:
        seq = bars[s]
        if seq[i] is None or i - mb.first_valid(seq) < 252:
            continue
        sc = score_fn(seq, i)
        s200, v = mb.sma(seq, i, 200), mb.vol63(seq, i)
        if sc is None or sc <= 0 or s200 is None or v is None:
            continue
        if seq[i][C] <= s200 or v > 0.80:
            continue
        out.append((s, sc))
    out.sort(key=lambda x: -x[1])
    return [s for s, _ in out]


def overlap(universe="WIDE", k=8):
    dates, bars, spyb = mb.load(universe)
    lo = "2006-01-01" if universe == "LONG" else "2021-12-01"
    i0 = max(next(i for i, d in enumerate(dates) if d >= lo), 253)
    syms = sorted(bars)
    month, rows = None, []
    for i in range(i0, len(dates)):
        d = dates[i]
        if d[:7] == month:
            continue
        month = d[:7]
        a = ranked(bars, syms, i, mb.mom_12_1)[:k]
        b = ranked(bars, syms, i, mom_6_1)[:k]
        if not a:
            rows.append((d, 0, len(b), None))
            continue
        n = len(set(a) & set(b))
        rows.append((d, len(a), len(b), n / len(a)))
    print(f"\n=== top-{k} overlap, baseline 12-1 vs variant 6-1 | universe {universe} ===")
    print("  (share of baseline top-k also in variant top-k; raw ranks after base eligibility, no sector cap)")
    print("  date        nBase nVar  shared  overlap")
    for d, na, nb, o in rows:
        print(f"  {d}  {na:>4} {nb:>4}  " + ("   n/a    n/a" if o is None else f"{round(o*na):>5}  {o*100:6.1f}%"))
    vals = [r[3] for r in rows if r[3] is not None]
    print(f"  months with baseline picks {len(vals)} of {len(rows)}; average overlap {sum(vals)/len(vals)*100:.1f}%"
          f"; min {min(vals)*100:.1f}%; max {max(vals)*100:.1f}%")


if __name__ == "__main__":
    print("NOTE: 252-bar history requirement kept unchanged (like-for-like).")
    hurdles("variant b 6-1", "LONG", score_fn=mom_6_1)
    hurdles("variant b 6-1", "WIDE", score_fn=mom_6_1)
    overlap("WIDE")
