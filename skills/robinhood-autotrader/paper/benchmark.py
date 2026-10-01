#!/usr/bin/env python3
"""
Score closed paper trades against a benchmark held over the identical window.

Why this exists, separately from expectancy.py:

  expectancy.py answers "did the trades make money relative to what was risked."
  It cannot answer "did picking these names beat just owning the index," and
  those come apart badly. The NANC congressional-trading ETF returned 31.4%
  since Feb 2023 and beat the S&P -- entirely because it was concentrated in
  tech during a tech bull market, not because congressional disclosures carried
  information. Raw return scored it a winner. Excess return over a matched
  window scores it flat.

  Any strategy run here is exposed to the same illusion. A basket of oversold
  large-caps bought in a rising market will show profits that have nothing to
  do with the selection rule. This script isolates the part attributable to the
  choice by subtracting what the benchmark did over the same days.

The benchmark series is read from disk, never fetched at scoring time, so a
score is reproducible and cannot change because a quote moved. If a date is
missing from the series the trade is reported unscoreable -- it is NEVER
interpolated or carried forward. A wrong benchmark is worse than no benchmark,
because it produces an alpha number that looks computed.

Usage:  python3 benchmark.py [trades.jsonl] [--bench spy_closes.json] [--strategy NAME]

The benchmark file is {"YYYY-MM-DD": close, ...}, populated from daily closes
(e.g. the Robinhood get_equity_historicals endpoint). Dates are trading days;
weekends and holidays are simply absent.
"""
import json, math, sys, os, datetime
from collections import defaultdict

try:
    from expectancy import stats
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from expectancy import stats


def load_benchmark(path, symbol=None):
    """Load {date: close}.

    Accepts either a flat series or the multi-symbol closes.json that
    fetch_closes.py maintains, so the benchmark needs no separately fetched
    file that could drift out of sync with the prices the signal actually saw.
    """
    if not os.path.exists(path):
        return {}
    with open(path) as fh:
        raw = json.load(fh)
    if raw and all(isinstance(v, dict) for v in raw.values()):
        if symbol is None:
            raise SystemExit(f"{path} holds several symbols {sorted(raw)}; "
                             "name one with --bench-symbol.")
        if symbol not in raw:
            raise SystemExit(f"{path} has no series for {symbol}.")
        raw = raw[symbol]
    return {d: float(p) for d, p in raw.items()}


def trade_return(t):
    """Fractional return on the position, sign-corrected for direction.

    Returns None when entry or exit is missing, or entry is zero -- an absent
    price is not a zero price.
    """
    entry, exit_ = t.get("entry"), t.get("exit")
    if entry in (None, 0) or exit_ is None:
        return None
    r = (exit_ - entry) / entry
    return -r if str(t.get("direction", "long")).startswith("short") else r


def score(path, bench, strategy=None):
    """Return (scored, unscoreable). Declines never enter the statistics.

    A `not_taken` record is the process working, not a trade that returned
    zero -- folding it in would make the strategy look worse the more
    disciplined it was. Same rule as expectancy.py.
    """
    scored, unscoreable = [], []
    if not os.path.exists(path):
        return scored, unscoreable
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        t = json.loads(line)
        if t.get("exit_reason") in ("not_taken", "scored_not_taken"):
            continue
        if not t.get("closed"):
            continue
        if strategy and t.get("strategy") != strategy:
            continue

        ret = trade_return(t)
        if ret is None:
            unscoreable.append((t, "no entry/exit price recorded"))
            continue

        d_open, d_close = t["opened"][:10], t["closed"][:10]
        if d_open not in bench or d_close not in bench:
            missing = d_open if d_open not in bench else d_close
            unscoreable.append((t, f"benchmark has no close for {missing}"))
            continue

        b_ret = (bench[d_close] - bench[d_open]) / bench[d_open]
        t["_ret"], t["_bench"], t["_excess"] = ret, b_ret, ret - b_ret
        scored.append(t)
    return scored, unscoreable


def report(scored, unscoreable, label, account=None):
    if unscoreable:
        print(f"UNSCOREABLE -- {len(unscoreable)} closed trade(s) skipped, not estimated:")
        for t, why in unscoreable:
            print(f"    {t.get('symbol','?'):<6} {t.get('id','?'):<28} {why}")
        print()

    if not scored:
        print(f"No scoreable closed trades{label}.")
        return

    ex = [t["_excess"] for t in scored]
    n, mean, sd, se = stats(ex)
    gross = sum(t["_ret"] for t in scored) / n
    bench = sum(t["_bench"] for t in scored) / n
    beat = sum(1 for e in ex if e > 0)

    print(f"BENCHMARK-RELATIVE{label} -- {n} closed trade(s)\n")
    print(f"  avg trade return   {gross:>+8.2%}")
    print(f"  avg benchmark      {bench:>+8.2%}   (same days held)")
    print(f"  avg EXCESS         {mean:>+8.2%}")
    print(f"  beat benchmark     {beat}/{n}  ({beat/n:.0%})")

    lo, hi = mean - 1.96 * se, mean + 1.96 * se
    print(f"  95% CI            [{lo:+.2%}, {hi:+.2%}]")

    if account:
        # A percentage edge on a small account is easy to admire and easy to
        # misjudge. +2% reads like a result; $19/yr reads like what it is.
        # The span is measured from the trades themselves, not assumed.
        dates = sorted([t["opened"][:10] for t in scored] +
                       [t["closed"][:10] for t in scored])
        days = (datetime.date.fromisoformat(dates[-1])
                - datetime.date.fromisoformat(dates[0])).days
        total = sum(t["_excess"] for t in scored) * account / len(scored)
        print(f"\n  at a ${account:,.0f} account, this sample's excess is "
              f"${total:+,.2f} over {days} day(s)")
        if days >= 30:
            print(f"  annualised, that is roughly ${total * 365 / days:+,.2f}/yr")
        else:
            print("  too short a span to annualise honestly")

    if n < 2 or sd == 0:
        print("\n  VERDICT: not enough data to say anything.")
    elif lo > 0:
        print("\n  VERDICT: positive excess return at 95% confidence, on this sample.")
    elif hi < 0:
        print("\n  VERDICT: NEGATIVE excess return at 95% confidence. The selection "
              "rule is destroying value versus simply holding the benchmark.")
    else:
        print("\n  VERDICT: indistinguishable from holding the benchmark. Whatever "
              "the raw return, this sample\n           does not show that picking "
              "these names beat owning the index.")
        if mean > 0:
            need = int((1.96 * sd / mean) ** 2) + 1
            if need > n:
                print(f"           At this mean and spread, ~{need} trades would be "
                      f"needed to prove it ({need - n} more).")
                print(f"           Progress toward an answer: {n}/{need}. Stopping "
                      f"here yields no result, not a bad one.")

    by = defaultdict(list)
    for t in scored:
        by[t.get("strategy", "untagged")].append(t["_excess"])
    if len(by) > 1:
        print("\n  by strategy:")
        for name, v in sorted(by.items(), key=lambda kv: -len(kv[1])):
            print(f"    {name:<24} n={len(v):<4} mean excess {sum(v)/len(v):+.2%}")


def main():
    args = sys.argv[1:]
    here = os.path.dirname(os.path.abspath(__file__))
    strategy = None
    account = None
    bench_symbol = None
    bench_path = os.path.join(here, "benchmark_spy.json")
    if not os.path.exists(bench_path) and os.path.exists(os.path.join(here, "closes.json")):
        bench_path, bench_symbol = os.path.join(here, "closes.json"), "SPY"
    positional = []
    i = 0
    while i < len(args):
        if args[i] == "--strategy" and i + 1 < len(args):
            strategy, i = args[i + 1], i + 2
        elif args[i] == "--bench" and i + 1 < len(args):
            bench_path, i = args[i + 1], i + 2
        elif args[i] == "--account" and i + 1 < len(args):
            account, i = float(args[i + 1]), i + 2
        elif args[i] == "--bench-symbol" and i + 1 < len(args):
            bench_symbol, i = args[i + 1], i + 2
        else:
            positional.append(args[i]); i += 1

    trades_path = positional[0] if positional else os.path.join(here, "trades.jsonl")
    bench = load_benchmark(bench_path, bench_symbol)
    if not bench:
        print(f"No benchmark series at {bench_path} -- cannot score.")
        print("  Populate it as {\"YYYY-MM-DD\": close, ...} from daily closes.")
        return 1

    scored, unscoreable = score(trades_path, bench, strategy)
    report(scored, unscoreable, f" [{strategy}]" if strategy else "", account)
    return 0


if __name__ == "__main__":
    sys.exit(main())
