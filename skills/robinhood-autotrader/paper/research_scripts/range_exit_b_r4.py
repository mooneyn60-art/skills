#!/usr/bin/env python3
"""Variant (b): R4-style exit. Data only."""
from range_exit_base import hurdles, run


def fn(p, seq, i, rng):
    level = max(p["e"] if p["hi"] >= 1.08 * p["e"] else 0, 0.80 * p["hi"])
    return seq[i][3] <= level or (i - p["d0"] >= 63)


def breakdown(r, label):
    tr = r["trades"]
    groups = {
        "8% stop": [t for t in tr if t["why"] == "stop"],
        "trail/breakeven (exit_rule, hold<63)": [t for t in tr if t["why"] == "exit_rule" and t["hold"] < 63],
        "63d cap (exit_rule, hold>=63)": [t for t in tr if t["why"] == "exit_rule" and t["hold"] >= 63],
        "  of which hold>=64": [t for t in tr if t["why"] == "exit_rule" and t["hold"] >= 64],
        "  of which hold==63": [t for t in tr if t["why"] == "exit_rule" and t["hold"] == 63],
    }
    print(f"\n{label}: total trades {len(tr)}")
    for k, g in groups.items():
        n = len(g)
        avg = sum(t["ret"] for t in g) / n * 100 if n else float("nan")
        print(f"  {k:<40} n {n:>4}  share {n / len(tr) * 100:5.1f}%  avg ret {avg:+.2f}%")


if __name__ == "__main__":
    hurdles("variant b: R4-style trail + 63d cap", fn)
    breakdown(run(fn, "bottom"), "bottom entry, full period")
    breakdown(run(fn, "top"), "top entry (control), full period")
