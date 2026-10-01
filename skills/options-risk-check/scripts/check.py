#!/usr/bin/env python3
"""Pre-trade gate for a single-leg option buy. Prints PASS/WARN/FAIL per rule.

Places nothing. Encodes robinhood-autotrader R3/R4/R5/R17. Numbers in, verdict
out; the human decides. Run with --help for args.
"""
import argparse
import sys


def yn(v):
    return str(v).strip().lower() in ("y", "yes", "true", "1")


def main(argv=None):
    p = argparse.ArgumentParser(description="Option pre-trade risk check")
    p.add_argument("--account", type=float, required=True, help="account value $")
    p.add_argument("--premium", type=float, required=True, help="this position's premium $ (per contract x100 x qty)")
    p.add_argument("--bid", type=float, required=True)
    p.add_argument("--ask", type=float, required=True)
    p.add_argument("--dte", type=int, required=True, help="days to expiry")
    p.add_argument("--oi", type=int, required=True, help="open interest")
    p.add_argument("--delta", type=float, default=None)
    p.add_argument("--name-exposure", type=float, default=0.0,
                   help="existing $ in this underlying (shares + option premium)")
    p.add_argument("--earnings-before-expiry", default="no")
    p.add_argument("--stop-planned", default="no")
    p.add_argument("--slot", default="yes", help="is this the R17 60+DTE slot? yes/no")
    args = p.parse_args(argv)

    mid = (args.bid + args.ask) / 2.0
    spread_pct = (args.ask - args.bid) / mid if mid > 0 else 1.0
    prem_pct = args.premium / args.account if args.account > 0 else 1.0
    name_pct = (args.name_exposure + args.premium) / args.account if args.account > 0 else 1.0
    slot = yn(args.slot)

    results = []  # (level, label, detail)

    # DTE
    if args.dte < 30:
        results.append(("FAIL", "DTE", f"{args.dte}d < 30d: lottery / decay trap"))
    elif args.dte < 60:
        lvl = "FAIL" if slot else "WARN"
        results.append((lvl, "DTE", f"{args.dte}d: below the R17 60+ DTE slot rule"))
    else:
        results.append(("PASS", "DTE", f"{args.dte}d"))

    # Spread
    if spread_pct > 0.10:
        results.append(("FAIL", "Spread", f"{spread_pct*100:.1f}% of mid > 10%"))
    else:
        results.append(("PASS", "Spread", f"{spread_pct*100:.1f}% of mid"))

    # Open interest
    if args.oi < 500:
        results.append(("FAIL", "Open interest", f"{args.oi} < 500 (illiquid)"))
    else:
        results.append(("PASS", "Open interest", f"{args.oi}"))

    # Premium size (R17 6%)
    if prem_pct > 0.06:
        results.append(("FAIL", "Premium size", f"{prem_pct*100:.1f}% of account > 6% (R17)"))
    else:
        results.append(("PASS", "Premium size", f"{prem_pct*100:.1f}% of account"))

    # Name concentration (R3 20%, counting shares+premium)
    if name_pct > 0.20:
        results.append(("FAIL", "Name concentration", f"{name_pct*100:.1f}% in this name > 20% (R3)"))
    elif name_pct > 0.15:
        results.append(("WARN", "Name concentration", f"{name_pct*100:.1f}% in this name (nearing 20% cap)"))
    else:
        results.append(("PASS", "Name concentration", f"{name_pct*100:.1f}% in this name"))

    # Delta
    if args.delta is not None:
        if 0.30 <= abs(args.delta) <= 0.60:
            results.append(("PASS", "Delta", f"{args.delta:+.2f}"))
        else:
            results.append(("WARN", "Delta", f"{args.delta:+.2f} outside 0.30-0.60 swing range"))

    # Earnings
    if yn(args.earnings_before_expiry):
        results.append(("WARN", "Earnings", "earnings before expiry: IV crush / gap risk"))
    else:
        results.append(("PASS", "Earnings", "none before expiry"))

    # Stop planned
    if yn(args.stop_planned):
        results.append(("PASS", "Stop planned", "yes"))
    else:
        results.append(("FAIL", "Stop planned", "NO stop planned (R4/R5)"))

    order = {"FAIL": 0, "WARN": 1, "PASS": 2}
    n_fail = sum(1 for r in results if r[0] == "FAIL")
    n_warn = sum(1 for r in results if r[0] == "WARN")

    print("OPTION PRE-TRADE CHECK")
    print(f"  mid={mid:.2f}  premium={args.premium:.0f}  account={args.account:.0f}")
    print("-" * 52)
    for lvl, label, detail in sorted(results, key=lambda r: order[r[0]]):
        print(f"  [{lvl:4}] {label:20} {detail}")
    print("-" * 52)
    if n_fail:
        print(f"VERDICT: FAIL ({n_fail} blocking, {n_warn} warn). Don't buy as-is.")
    elif n_warn:
        print(f"VERDICT: PASS WITH {n_warn} WARN. Structurally OK; judgement call. Not a buy signal.")
    else:
        print("VERDICT: PASS. Structurally OK. Not a buy signal — Nolan decides.")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
