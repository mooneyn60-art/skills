#!/usr/bin/env python3
"""Max dollar size for a new position under robinhood-autotrader money rules.

Enforces: 20% per-name hard cap (15% non-core), 15% cash floor, 8% risk budget,
and shares+option premium counted as one position. Sizes nothing, places
nothing. See SKILL.md and research/2026-09-30_KELLY_SIZING.md.
"""
import argparse
import sys

PER_NAME_CORE = 0.20
PER_NAME_NONCORE = 0.15
CASH_FLOOR = 0.15
RISK_BUDGET = 0.08


def yn(v):
    return str(v).strip().lower() in ("y", "yes", "true", "1")


def main(argv=None):
    p = argparse.ArgumentParser(description="Position sizer")
    p.add_argument("--account", type=float, required=True)
    p.add_argument("--cash", type=float, required=True)
    p.add_argument("--name-exposure", type=float, default=0.0,
                   help="$ already in this underlying (shares + option premium)")
    p.add_argument("--core", default="no")
    p.add_argument("--stop-distance-pct", type=float, default=100.0,
                   help="planned stop distance below entry, %% (option: %% of premium at risk)")
    p.add_argument("--open-risk", type=float, default=0.0,
                   help="$ already at risk across all open positions")
    args = p.parse_args(argv)

    acct = args.account
    core = yn(args.core)
    name_cap_pct = PER_NAME_CORE if core else PER_NAME_NONCORE

    # 1) per-name cap headroom
    name_cap_dollars = name_cap_pct * acct
    headroom_name = name_cap_dollars - args.name_exposure

    # 2) cash above the floor
    floor_dollars = CASH_FLOOR * acct
    cash_available = args.cash - floor_dollars

    # 3) risk budget: remaining risk / stop distance = max notional this position
    budget_dollars = RISK_BUDGET * acct
    remaining_risk = budget_dollars - args.open_risk
    sd = max(args.stop_distance_pct, 1e-9) / 100.0
    risk_capped_notional = remaining_risk / sd if remaining_risk > 0 else 0.0

    limits = {
        f"per-name cap ({name_cap_pct*100:.0f}%)": headroom_name,
        "cash above 15% floor": cash_available,
        f"8% risk budget @ {args.stop_distance_pct:.0f}% stop": risk_capped_notional,
    }
    binding = min(limits, key=limits.get)
    max_add = limits[binding]

    print("POSITION SIZER")
    print(f"  account={acct:.0f}  cash={args.cash:.0f}  "
          f"name_exposure={args.name_exposure:.0f}  core={core}")
    print("-" * 56)
    for k, v in limits.items():
        mark = "<== binds" if k == binding else ""
        print(f"  {k:40} ${v:8.0f} {mark}")
    print("-" * 56)
    if max_add <= 0:
        why = {
            f"per-name cap ({name_cap_pct*100:.0f}%)": "already at/over the per-name cap",
            "cash above 15% floor": "at/below the 15% cash floor — NO new buys",
            f"8% risk budget @ {args.stop_distance_pct:.0f}% stop": "risk budget spent",
        }[binding]
        print(f"MAX ADD: $0 — {why}.")
    else:
        print(f"MAX ADD: ${max_add:.0f}  (bound by {binding}).")
        print("This is a CEILING, not a recommendation to fill it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
