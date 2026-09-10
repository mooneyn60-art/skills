#!/usr/bin/env python3
"""
Compute expectancy and its confidence interval from the paper-trading ledger.

The point of this script is to make it hard to lie about performance -- to the
owner or to myself. Two design choices carry that weight:

  1. Everything is reported in R-multiples (realized / planned_risk), not
     dollars. Dollars scale with account size and hide whether the process
     works; R does not.

  2. Expectancy is reported with a 95% confidence interval and an explicit
     "trades still needed" figure. A positive mean on a small sample is not
     evidence, and the script says so rather than letting a good streak read
     as a good strategy.

Usage:  python3 expectancy.py [trades.jsonl]
"""
import json, math, sys, os
from collections import Counter, defaultdict

def load(path):
    if not os.path.exists(path):
        return []
    out = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        t = json.loads(line)
        if t.get("closed") and t.get("planned_risk"):
            t["R"] = t["realized_pnl"] / t["planned_risk"]
            out.append(t)
    return out

def stats(rs):
    n = len(rs)
    mean = sum(rs) / n
    sd = math.sqrt(sum((r - mean) ** 2 for r in rs) / (n - 1)) if n > 1 else 0.0
    se = sd / math.sqrt(n) if n else 0.0
    return n, mean, sd, se

def max_drawdown(rs):
    peak = cum = trough = 0.0
    for r in rs:
        cum += r
        peak = max(peak, cum)
        trough = min(trough, cum - peak)
    return trough

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "trades.jsonl")
    ts = load(path)
    if not ts:
        print("No closed trades logged yet.")
        print(f"  ledger: {path}")
        return

    rs = [t["R"] for t in ts]
    n, mean, sd, se = stats(rs)
    wins = [r for r in rs if r > 0]
    losses = [r for r in rs if r <= 0]

    print(f"PAPER TRADING -- {n} closed trades\n")
    print(f"  win rate        {len(wins)/n:>7.1%}  ({len(wins)}W / {len(losses)}L)")
    if wins:   print(f"  average win     {sum(wins)/len(wins):>+7.2f}R")
    if losses: print(f"  average loss    {sum(losses)/len(losses):>+7.2f}R")
    if wins and losses:
        print(f"  win/loss ratio  {abs((sum(wins)/len(wins))/(sum(losses)/len(losses))):>7.2f}")
    print(f"  total           {sum(rs):>+7.2f}R")
    print(f"  max drawdown    {max_drawdown(rs):>+7.2f}R")

    lo, hi = mean - 1.96 * se, mean + 1.96 * se
    print(f"\n  EXPECTANCY      {mean:>+7.2f}R per trade")
    print(f"  95% CI          [{lo:+.2f}R, {hi:+.2f}R]")

    # Is the edge distinguishable from zero yet?
    if n < 2 or sd == 0:
        print("\n  VERDICT: not enough data to say anything.")
    elif lo > 0:
        print(f"\n  VERDICT: edge is positive at 95% confidence. Real, on this sample.")
    elif hi < 0:
        print(f"\n  VERDICT: edge is NEGATIVE at 95% confidence. Stop and rebuild.")
    else:
        # trades needed for the CI to clear zero, if the mean holds
        need = int((1.96 * sd / mean) ** 2) + 1 if mean > 0 else None
        print(f"\n  VERDICT: indistinguishable from random. The mean is "
              f"{'positive' if mean > 0 else 'negative'}, but the interval spans zero.")
        if need and need > n:
            print(f"           At this mean and spread, ~{need} trades would be needed "
                  f"to prove it ({need - n} more).")
        print("           Do NOT fund this on the strength of the number above.")

    # Exit-reason breakdown. This is the diagnostic that catches the failure
    # mode the live account actually had: full-size losses, fractional wins.
    by = defaultdict(list)
    for t in ts:
        by[t.get("exit_reason", "unspecified")].append(t["R"])
    print("\n  by exit reason:")
    for reason, v in sorted(by.items(), key=lambda kv: -len(kv[1])):
        print(f"    {reason:<16} n={len(v):<4} mean {sum(v)/len(v):+.2f}R")

    small_wins = [r for r in wins if r < 1.0]
    if wins and len(small_wins) / len(wins) > 0.5:
        print(f"\n  ⚠ {len(small_wins)}/{len(wins)} winners closed under +1R. "
              f"That is the 'cutting winners early' leak -- losses run to 1R by\n"
              f"    construction, so wins must exceed it or expectancy cannot be positive.")

if __name__ == "__main__":
    main()
