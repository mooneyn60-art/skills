#!/usr/bin/env python3
"""Log a trade to the ledger, or score a closed trade against SPY.

Subcommands:
  log    append a trade entry (JSONL) to the robinhood-autotrader ledger
  score  compare a closed trade's return to SPY over the same window

Appends only; never edits or deletes rows. Places nothing. No fabricated
numbers: if SPY prices are missing, score refuses rather than guessing.
See SKILL.md. Dollar account balances stay out of commits (R13).
"""
import argparse
import json
import sys
import uuid
from datetime import datetime, timezone


def cmd_log(args):
    entry = {
        "id": args.id or ("tj-" + uuid.uuid4().hex[:8]),
        "opened": args.opened or datetime.now(timezone.utc).isoformat(),
        "ts": datetime.now(timezone.utc).isoformat(),
        "closed": False,
        "account": args.account,          # placeholder/env, not hardcoded here
        "symbol": args.symbol,
        "instrument": args.instrument,
        "contract": args.contract,
        "direction": args.direction,
        "qty": args.qty,
        "entry": args.entry,
        "stop": args.stop,
        "target": args.target,
        "strategy": args.strategy,
        "thesis": args.thesis,
        "source": args.source,
    }
    if args.entry is not None and args.stop is not None:
        entry["planned_risk"] = round(abs(args.entry - args.stop), 4)
    entry = {k: v for k, v in entry.items() if v is not None}
    if args.dry_run:
        print(json.dumps(entry, indent=2))
        print("\n(dry run — not written)")
        return 0
    with open(args.ledger, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"appended id={entry['id']} to {args.ledger}")
    return 0


def cmd_score(args):
    missing = [n for n, v in (("spy-entry", args.spy_entry), ("spy-exit", args.spy_exit))
               if v is None]
    if missing:
        print(f"CANNOT SCORE: missing {', '.join(missing)}. "
              "Not fabricating a SPY comparison.")
        return 2
    trade_ret = args.exit / args.entry - 1
    spy_ret = args.spy_exit / args.spy_entry - 1
    excess = trade_ret - spy_ret
    print("TRADE vs SPY (same window)")
    print(f"  trade return : {trade_ret*100:+.2f}%")
    print(f"  SPY  return  : {spy_ret*100:+.2f}%")
    print(f"  excess vs SPY: {excess*100:+.2f}%")
    if args.planned_risk_pct:
        r_mult = trade_ret / (args.planned_risk_pct / 100)
        print(f"  R-multiple   : {r_mult:+.2f}R  (return / {args.planned_risk_pct:.0f}% planned risk)")
    if trade_ret > 0 and excess < 0:
        print("  FLAG: green but LAGGED SPY — no value added over just holding the index.")
    elif trade_ret < 0 and excess > 0:
        print("  NOTE: down, but LESS than SPY over these days (relative outperformance).")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Trade journal")
    sub = p.add_subparsers(dest="cmd", required=True)

    lg = sub.add_parser("log", help="append a trade entry")
    lg.add_argument("--ledger", required=True)
    lg.add_argument("--symbol", required=True)
    lg.add_argument("--instrument", default="equity")
    lg.add_argument("--contract", default=None)
    lg.add_argument("--direction", default="long")
    lg.add_argument("--qty", type=float, default=None)
    lg.add_argument("--entry", type=float, default=None)
    lg.add_argument("--stop", type=float, default=None)
    lg.add_argument("--target", type=float, default=None)
    lg.add_argument("--strategy", default=None)
    lg.add_argument("--thesis", default=None)
    lg.add_argument("--source", default="TARS")
    lg.add_argument("--account", default=None, help="account id/placeholder; do not hardcode")
    lg.add_argument("--id", default=None)
    lg.add_argument("--opened", default=None)
    lg.add_argument("--dry-run", action="store_true")
    lg.set_defaults(func=cmd_log)

    sc = sub.add_parser("score", help="score a closed trade vs SPY")
    sc.add_argument("--entry", type=float, required=True)
    sc.add_argument("--exit", type=float, required=True)
    sc.add_argument("--spy-entry", type=float, default=None)
    sc.add_argument("--spy-exit", type=float, default=None)
    sc.add_argument("--planned-risk-pct", type=float, default=None)
    sc.set_defaults(func=cmd_score)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
