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
    """Return (taken, skipped, unstopped).

    A `not_taken` record is a candidate the process generated and declined. It
    belongs in the ledger -- without it the record silently keeps only the ideas
    that felt good -- but it must NOT enter the expectancy statistics. Counting a
    decline as a 0R trade would drag the mean toward zero and make the strategy
    look worse the more disciplined it was. Declining is the process working, not
    a trade with no profit.

    An `unstopped` record is a closed position with no planned_risk -- chiefly
    options structures (a covered call has no stop; the shares must be held to
    cover the call, so there is no price that defines 1R). R-multiples are
    undefined without a stop, so these must NEVER be folded into the R stats.
    The bug this replaced did the opposite silently: `if planned_risk` treats
    None/0 as falsy and drops the trade from every report with no message,
    which is worse than a wrong number -- it is a number that quietly never
    existed. Found during the 2026-09-10 post-close review, before any options
    trade had actually closed, precisely because nothing had broken yet.
    """
    if not os.path.exists(path):
        return [], [], []
    records = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        records.append(json.loads(line))

    # PROTOCOL.md is append-only: a wrong record gets a correction appended
    # with id "<original-id>-CORRECTION", never edited in place. Without this
    # step both versions land in stats and the original (often missing or
    # wrong planned_risk/realized_pnl) double-counts or double-classifies the
    # same trade. Drop any base record whose corrected version also exists.
    corrected_base_ids = {
        r["id"][: -len("-CORRECTION")] for r in records if r["id"].endswith("-CORRECTION")
    }
    records = [r for r in records if r["id"] not in corrected_base_ids]

    taken, skipped, unstopped = [], [], []
    for t in records:
        if t.get("exit_reason") == "not_taken":
            skipped.append(t)
            continue
        if not t.get("closed"):
            continue
        if t.get("realized_pnl") is None:
            # A closed-timestamp research/protocol record (e.g. exit_reason
            # "R9_locked" or "protocol_review") that was priced but never
            # actually opened as a position. Not "not_taken" literally, but
            # the same category for stats purposes: no real P&L exists.
            # Treating it as `unstopped` used to crash sum() on None; treating
            # it as a real trade would be worse -- it would count a snapshot
            # that was never risked. Bucket with skipped/declined instead.
            skipped.append(t)
            continue
        if t.get("planned_risk"):
            t["R"] = t["realized_pnl"] / t["planned_risk"]
            taken.append(t)
        else:
            unstopped.append(t)
    return taken, skipped, unstopped

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
    ts, skipped, unstopped = load(path)
    if unstopped:
        total = sum(t["realized_pnl"] for t in unstopped)
        print(f"UNSTOPPED (options/no-stop) -- {len(unstopped)} closed, "
              f"excluded from R stats, tracked in dollars:")
        for t in unstopped:
            print(f"    {t['symbol']:<6} {t.get('instrument','?'):<14} "
                  f"{t['realized_pnl']:+.2f}  {t.get('closed','')[:10]}")
        print(f"    total {total:+.2f}\n")
    if not ts:
        print("No closed R-based trades logged yet.")
        print(f"  ledger: {path}")
        if skipped:
            print(f"  {len(skipped)} candidate(s) logged and declined:")
            for t in skipped[-8:]:
                print(f"    {t['symbol']:<6} {t.get('opened','')[:10]}")
        return

    rs = [t["R"] for t in ts]
    n, mean, sd, se = stats(rs)
    wins = [r for r in rs if r > 0]
    losses = [r for r in rs if r <= 0]

    print(f"PAPER TRADING -- {n} closed trades"
          f"{f' ({len(skipped)} candidates declined, excluded from stats)' if skipped else ''}\n")
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
        if mean == 0:
            detail = "The mean is exactly zero."
        else:
            detail = (f"The mean is {'positive' if mean > 0 else 'negative'}, "
                      f"but the interval spans zero.")
        print(f"\n  VERDICT: indistinguishable from random. {detail}")
        if need and need > n:
            print(f"           At this mean and spread, ~{need} trades would be needed "
                  f"to prove it ({need - n} more).")
        print("           Do NOT fund this on the strength of the number above.")

    # PROTOCOL.md: "Tag every record with strategy... untagged records score
    # as one undifferentiated blob, so a good rule and a bad one average into
    # 'indistinguishable.'" The verdict above IS that blob when the ledger
    # mixes strategies (e.g. TARS-1's mechanical equity stops next to
    # user_discretionary options trades) -- break it out so each strategy is
    # judged on its own sample, not smeared by the other's variance.
    by_strategy = defaultdict(list)
    for t in ts:
        by_strategy[t.get("strategy", "untagged")].append(t["R"])
    if len(by_strategy) > 1:
        print("\n  by strategy (same trades, not a separate sample):")
        for strat, v in sorted(by_strategy.items(), key=lambda kv: -len(kv[1])):
            sn, smean, ssd, sse = stats(v)
            if sn < 2:
                print(f"    {strat:<20} n={sn:<3} mean {smean:+.2f}R  (n=1, no CI yet)")
                continue
            slo, shi = smean - 1.96 * sse, smean + 1.96 * sse
            print(f"    {strat:<20} n={sn:<3} mean {smean:+.2f}R  95% CI [{slo:+.2f}R, {shi:+.2f}R]")

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
