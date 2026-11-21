#!/usr/bin/env python3
"""Variant c: midpoint exit. Sell at next open when close is at/above 50% of trailing 60d range. 8% stop stays."""
from range_exit_base import hurdles, C


def exit_fn(p, seq, i, rng):
    lo, hi = rng
    return hi > lo and (seq[i][C] - lo) / (hi - lo) >= 0.50


if __name__ == "__main__":
    hurdles("variant c: midpoint exit", exit_fn)
