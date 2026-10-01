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
import math
import sys


def intrinsic(opt_type, strike, s):
    return max(0.0, s - strike) if opt_type == "call" else max(0.0, strike - s)


def _ncdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_price(opt_type, s, k, t_years, iv, r=0.04):
    """Black-Scholes value. Falls back to intrinsic at/after expiry or zero IV."""
    if t_years <= 0 or iv <= 0:
        return intrinsic(opt_type, k, s)
    d1 = (math.log(s / k) + (r + 0.5 * iv * iv) * t_years) / (iv * math.sqrt(t_years))
    d2 = d1 - iv * math.sqrt(t_years)
    if opt_type == "call":
        return s * _ncdf(d1) - k * math.exp(-r * t_years) * _ncdf(d2)
    return k * math.exp(-r * t_years) * _ncdf(-d2) - s * _ncdf(-d1)


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
    p.add_argument("--days-left-after", type=float, default=None,
                   help="calendar days to expiry remaining the day AFTER earnings; "
                        "enables Black-Scholes value with time value left")
    p.add_argument("--iv-after", type=float, default=None,
                   help="post-earnings (crushed) implied vol as a decimal, e.g. 0.45")
    p.add_argument("--rate", type=float, default=0.04)
    args = p.parse_args(argv)
    use_bs = args.days_left_after is not None and args.iv_after is not None

    print(f"EARNINGS SCENARIO — long {args.type} strike {args.strike}, paid {args.paid:.2f}")
    print(f"  stock now {args.stock_now:.2f}")
    if args.implied_move_pct is not None:
        up = args.stock_now * (1 + args.implied_move_pct / 100)
        dn = args.stock_now * (1 - args.implied_move_pct / 100)
        print(f"  implied move ±{args.implied_move_pct:.1f}%  ->  {dn:.2f} / {up:.2f}")
    if use_bs:
        print(f"  post-earnings model: {args.days_left_after:.0f} days left, "
              f"IV after crush {args.iv_after*100:.0f}%, r={args.rate*100:.1f}%")
    print("-" * 72)
    hdr = f"  {'move%':>7} {'stock':>8} {'intrinsic':>10}"
    if use_bs:
        hdr += f" {'BS value':>9}"
    hdr += f" {'P/L/sh':>9} {'P/L x100':>9}"
    print(hdr)
    for m in sorted(args.moves):
        s = args.stock_now * (1 + m / 100)
        iv = intrinsic(args.type, args.strike, s)
        val = iv
        line = f"  {m:>6.1f}% {s:>8.2f} {iv:>10.2f}"
        if use_bs:
            val = bs_price(args.type, s, args.strike, args.days_left_after / 365.0,
                           args.iv_after, args.rate)
            line += f" {val:>9.2f}"
        pl = val - args.paid
        line += f" {pl:>+9.2f} {pl*100:>+9.0f}"
        print(line)
    print("-" * 72)
    if use_bs:
        print("  P/L uses the Black-Scholes value (time value left after the crush).")
    else:
        print("  P/L uses intrinsic only. For an option that outlives earnings, pass "
              "--days-left-after and --iv-after, or this understates its value.")
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
    print("  NOTE: Black-Scholes here has no skew and one flat post-crush IV; it's a "
          "scenario tool, not a quote. Direction is a coin flip.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
