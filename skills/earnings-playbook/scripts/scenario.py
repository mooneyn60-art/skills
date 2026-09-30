#!/usr/bin/env python3
"""Scenario a long single-leg option across post-earnings stock prices.

Simple model: value at each outcome = intrinsic value (max(0, S-K) for a call,
max(0, K-S) for a put). This is a LOWER BOUND right after earnings once IV has
crushed and little time is left; it is NOT a full option pricer (no skew, no
remaining time value). It also prints the implied-move breakevens so you can see
whether the move needed to profit is bigger than what options priced in.

Places nothing. See SKILL.md.
"""
import argparse
import sys


def intrinsic(opt_type, strike, s):
    return max(0.0, s - strike) if opt_type == "call" else max(0.0, strike - s)


def main(argv=None):
    p = argparse.ArgumentParser(description="Earnings scenario for a long option")
    p.add_argument("--type", choices=["call", "put"], required=True)
    p.add_argument("--strike", type=float, required=True)
    p.add_argument("--paid", type=float, required=True, help="premium paid per share (e.g. 2.05)")
    p.add_argument("--stock-now", type=float, required=True)
    p.add_argument("--implied-move-pct", type=float, default=None,
                   help="implied move from the straddle, %%")
    p.add_argument("--moves", type=float, nargs="+", default=[-10, -5, 0, 5, 10],
                   help="post-earnings stock moves in %% to scenario")
    args = p.parse_args(argv)

    print(f"EARNINGS SCENARIO — long {args.type} strike {args.strike}, paid {args.paid:.2f}")
    print(f"  stock now {args.stock_now:.2f}")
    if args.implied_move_pct is not None:
        up = args.stock_now * (1 + args.implied_move_pct / 100)
        dn = args.stock_now * (1 - args.implied_move_pct / 100)
        print(f"  implied move ±{args.implied_move_pct:.1f}%  ->  {dn:.2f} / {up:.2f}")
    print("-" * 60)
    print(f"  {'move%':>7} {'stock':>8} {'intrinsic':>10} {'P/L/sh':>9} {'P/L x100':>9}")
    for m in sorted(args.moves):
        s = args.stock_now * (1 + m / 100)
        iv = intrinsic(args.type, args.strike, s)
        pl = iv - args.paid
        print(f"  {m:>6.1f}% {s:>8.2f} {iv:>10.2f} {pl:>+9.2f} {pl*100:>+9.0f}")
    print("-" * 60)
    # breakeven move
    if args.type == "call":
        be_stock = args.strike + args.paid
    else:
        be_stock = args.strike - args.paid
    be_move = (be_stock / args.stock_now - 1) * 100
    print(f"  Breakeven at expiry: stock {be_stock:.2f} ({be_move:+.1f}% move).")
    if args.implied_move_pct is not None:
        need = abs(be_move)
        print(f"  Needs a {need:.1f}% move to break even vs {args.implied_move_pct:.1f}% "
              f"priced in -> {'HARDER' if need > args.implied_move_pct else 'easier'} than the implied move.")
    print("  NOTE: intrinsic-only = lower bound post-crush; not a full pricer. "
          "Direction is a coin flip.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
