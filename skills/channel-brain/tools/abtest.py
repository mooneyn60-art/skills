#!/usr/bin/env python3
"""Score an A/B experiment honestly: is B really better than A, or is it luck?

Give it one number per video for each version (stayed-to-watch %, views at 48 h, subs per 1,000 views...):
    python3 abtest.py --a 40,38,45,41,36 --b 55,61,48,52 [--metric "stayed-to-watch %"] [--lower-is-better]
It prints the two averages, the difference with a 90% confidence range (bootstrap, 10,000 resamples),
how many videos per side a test this noisy needs, and a verdict:
  TOO FEW     - fewer than 5 videos on a side: keep running, decide nothing
  B WINS      - the whole 90% range is above zero (B better), and it held in both halves of B's videos
  A WINS      - the whole range is below zero
  NO DIFFERENCE YET - the range crosses zero: keep the cheaper version or run longer
Views are skewed by one lucky video, so it also reports medians and flags when one video drives the result.
"""
import argparse
import random
import statistics as st


def boot_diff(a, b, n=10000, seed=7):
    rnd = random.Random(seed)
    d = sorted(st.mean(rnd.choices(b, k=len(b))) - st.mean(rnd.choices(a, k=len(a))) for _ in range(n))
    return d[int(0.05 * n)], d[int(0.95 * n)]


def needed_n(a, b, lift):
    s = st.pstdev(a + b) or 1e-9
    return max(5, int(round(2 * ((1.645 + 0.84) * s / lift) ** 2))) if lift else None  # 90% one-sided, 80% power


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--a", required=True, help="comma-separated numbers for version A (the old way)")
    p.add_argument("--b", required=True, help="comma-separated numbers for version B (the change)")
    p.add_argument("--metric", default="metric")
    p.add_argument("--lower-is-better", action="store_true")
    x = p.parse_args()
    a = [float(v) for v in x.a.split(",") if v.strip()]
    b = [float(v) for v in x.b.split(",") if v.strip()]
    sign = -1 if x.lower_is_better else 1
    ma, mb = st.mean(a), st.mean(b)
    print(f"{x.metric}: A mean {ma:.2f} (median {st.median(a):.2f}, n {len(a)}) | B mean {mb:.2f} (median {st.median(b):.2f}, n {len(b)})")
    if min(len(a), len(b)) < 5:
        print("Verdict: TOO FEW. Need at least 5 videos per side before deciding anything.")
        return
    lo, hi = boot_diff(a, b)
    print(f"B - A = {mb - ma:+.2f}, 90% range {lo:+.2f} to {hi:+.2f}")
    target = abs(mb - ma) or 0.1 * abs(ma) or 1
    print(f"Videos per side needed to trust a difference this size: about {needed_n(a, b, target)}")
    top = max(b) if sign > 0 else min(b)
    without = [v for v in b if v != top] or b
    if len(b) >= 5 and (st.mean(without) - ma) * sign <= 0 < (mb - ma) * sign:
        print("Warning: B's lead disappears without its single best video. One lucky post is not a result.")
    h1, h2 = b[: len(b) // 2], b[len(b) // 2:]
    both = (st.mean(h1) - ma) * sign > 0 and (st.mean(h2) - ma) * sign > 0
    if lo * sign > 0 and hi * sign > 0 and both:
        print("Verdict: B WINS (whole range on B's side, and it held in both halves). Adopt B, log it, move to the next test.")
    elif lo * sign < 0 and hi * sign < 0:
        print("Verdict: A WINS. Revert to A and write down why B lost.")
    else:
        print("Verdict: NO DIFFERENCE YET. Keep the cheaper/simpler version, or run until the needed count above.")


if __name__ == "__main__":
    main()
