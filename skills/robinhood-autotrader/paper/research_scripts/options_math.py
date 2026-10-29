"""Options math for the slot (py_vollib, Black-Scholes). Robinhood's quote already carries IV and the Greeks;
this adds what it doesn't: a what-if grid (option value for SPY moves over the next hours) and the SPY move needed
to cover the spread + decay. Usage: python3 options_math.py SPY_PRICE STRIKE call|put MID CALENDAR_HOURS_TO_EXPIRY [IV]"""
import sys
from py_vollib.black_scholes import black_scholes as bs
from py_vollib.black_scholes.implied_volatility import implied_volatility as iv_of
from py_vollib.black_scholes.greeks.analytical import delta, theta
S, K, kind, mid, hrs = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3][0], float(sys.argv[4]), float(sys.argv[5])
r = 0.04; T = hrs / (24 * 365)  # calendar clock (matches Robinhood IV)
# Prefer passing Robinhood's implied_volatility as arg 6: our solved IV differs from RH's (10/21: 9.8% vs 15.4% on the 1DTE 770C)
iv = float(sys.argv[6]) if len(sys.argv) > 6 else iv_of(mid, S, K, T, r, kind)
print(f"IV {iv:.1%}  delta {delta(kind, S, K, T, r, iv):.2f}  theta/day {theta(kind, S, K, T, r, iv):.2f} per share")
print("value after N hours if SPY moves by X (per contract, vs cost", round(mid * 100), "):")
moves = (-3, -2, -1, -0.5, 0, 0.5, 1, 2, 3)
print("  hrs  " + "".join(f"{m:+6.1f}" for m in moves))
for h in (0.5, 1, 2, 4):
    t2 = max(T - h / (24 * 365), 1e-6)
    print(f"  {h:>3}  " + "".join(f"{(bs(kind, S + m, K, t2, r, iv) - mid) * 100:+6.0f}" for m in moves))
for h in (1, 2):
    t2 = T - h / (24 * 365); m = 0.0
    while bs(kind, S + m * (1 if kind == "c" else -1), K, t2, r, iv) < mid and m < 20: m += 0.05
    print(f"SPY must move {m:.2f} pts ({m / S:.2%}) your way within {h}h just to break even")
