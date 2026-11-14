#!/usr/bin/env python3
"""
Does R2's proximity-to-high condition earn its place?

WHY THIS EXISTS
---------------
TARS-1's R2 entry has five conditions. Exactly ONE of them -- "price above the
200-day moving average" -- corresponds to something this repo ever measured
(STRATEGY.md's 10-month MA filter, validated over 235 months). The other four
were written from intuition and have never been tested against anything.

The tightest of those untested conditions is rule 3: price must sit within 5%
of the 20-day high. It is the condition that does the most work in practice --
on 2026-09-21 alone it rejected NEM (8.5% off), rejected SHEL, and forced the
NEM exit discussion. If it is not adding return or cutting drawdown, it is
just a filter that says no a lot, and "says no a lot" is not the same as
"protects capital."

WHAT IS AND IS NOT TESTED HERE
------------------------------
Monthly bars cannot test an 8% stop or an 8% trail -- the bar is far too
coarse, and pretending otherwise would produce a number that looks real and
is not. So this tests the ENTRY TREND CONDITIONS only, on their honest
monthly analogues:

    R2 rule 1  "above the 200-day MA"        -> above the 10-month MA
    R2 rule 3  "within 5% of the 20-day high" -> within X% of the 12-month high
    (dual momentum, for reference)            -> 12-1 month momentum > 0

Rules 2 (50-day MA), 4 (earnings) and 5 (sector cap) are NOT tested. The
50-day has no clean monthly analogue, and the other two are not price rules.
Their absence is a limit of this test, not evidence they work.

METHOD, no lookahead
--------------------
At each month-end t the signal uses closes[0..t] ONLY and is applied to the
return of month t+1. Cash earns 0%, which understates every filtered variant
and so biases the comparison AGAINST the rules being tested -- the honest
direction to be wrong in. Equal weight across symbols, rebalanced monthly.

Usage:  python3 test_r2_conditions.py
"""
import json, os, sys

MA_WINDOW = 10      # months; monthly equivalent of the 200-day SMA
LOOKBACK = 12       # months, for 12-1 momentum and for the "recent high" window
SKIP = 1

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "history", "monthly_stocks.json")
BENCH = "SPY"


def load():
    raw = json.load(open(DATA))
    series = {}
    for sym, d in raw.items():
        dates = sorted(d.keys())
        series[sym] = (dates, [float(d[k]) for k in dates])
    return series


def features(closes, t):
    """All signal inputs at month-end t, from closes[0..t] only.

    Returns None when history is insufficient -- an unknown signal is not a
    decision, and defaulting to 'invested' would silently manufacture return.
    """
    if t < max(LOOKBACK, MA_WINDOW):
        return None
    ma = sum(closes[t - MA_WINDOW + 1:t + 1]) / MA_WINDOW
    # R2 rule 2 is the 50-day MA. 50 trading days is ~2.4 months; test 2 and 3.
    ma_fast2 = sum(closes[t - 1:t + 1]) / 2.0
    ma_fast3 = sum(closes[t - 2:t + 1]) / 3.0
    mom = closes[t - SKIP] / closes[t - LOOKBACK] - 1.0
    hi = max(closes[t - LOOKBACK + 1:t + 1])
    return {"above_ma": closes[t] > ma,
            "above_fast2": closes[t] > ma_fast2,
            "above_fast3": closes[t] > ma_fast3,
            "mom_pos": mom > 0,
            "prox": closes[t] / hi}


def equity_curve(closes, rule):
    """Monthly equity curve for one symbol under `rule`. Starts at 1.0.

    Months without a signal are held in cash at 0%, matching backtest.py.
    """
    eq, curve = 1.0, []
    for t in range(len(closes) - 1):
        f = features(closes, t)
        r = closes[t + 1] / closes[t] - 1.0
        invested = rule(f) if f is not None else False
        if invested:
            eq *= (1.0 + r)
        curve.append(eq)
    return curve


def combine(curves):
    """Equal-weight portfolio across symbols, rebalanced monthly."""
    n = min(len(c) for c in curves)
    out, eq = [], 1.0
    for i in range(n):
        if i == 0:
            step = sum(c[0] for c in curves) / len(curves)
        else:
            step = sum(c[i] / c[i - 1] for c in curves) / len(curves)
        eq *= step
        out.append(eq)
    return out


def stats(curve, months):
    if not curve:
        return 0.0, 0.0
    years = months / 12.0
    cagr = curve[-1] ** (1.0 / years) - 1.0 if years > 0 and curve[-1] > 0 else -1.0
    peak, mdd = curve[0], 0.0
    for v in curve:
        peak = max(peak, v)
        mdd = min(mdd, v / peak - 1.0)
    return cagr, mdd


RULES = [
    ("buy & hold",                 lambda f: True),
    ("R2-1 only: above 10m MA",    lambda f: f["above_ma"]),
    ("MA + 12-1 momentum",         lambda f: f["above_ma"] and f["mom_pos"]),
    ("MA + within 5% of 12m high", lambda f: f["above_ma"] and f["prox"] >= 0.95),
    ("MA + within 10% of high",    lambda f: f["above_ma"] and f["prox"] >= 0.90),
    ("MA + within 20% of high",    lambda f: f["above_ma"] and f["prox"] >= 0.80),
    ("MA + mom + within 5%",       lambda f: f["above_ma"] and f["mom_pos"] and f["prox"] >= 0.95),
    # --- R2 rule 2: the 50-day MA, never previously tested ---
    ("R2-2 only: above 3m MA",     lambda f: f["above_fast3"]),
    ("MA + above 3m MA (r1+r2)",   lambda f: f["above_ma"] and f["above_fast3"]),
    ("MA + above 2m MA",           lambda f: f["above_ma"] and f["above_fast2"]),
    ("FULL R2 (r1+r2+r3 @5%)",     lambda f: f["above_ma"] and f["above_fast3"] and f["prox"] >= 0.95),
    ("r1+r2, prox loosened to 15%",lambda f: f["above_ma"] and f["above_fast3"] and f["prox"] >= 0.85),
]


def main():
    series = load()
    syms = [s for s in sorted(series) if s != BENCH]
    months = min(len(series[s][1]) for s in syms) - 1

    print(f"R2 ENTRY CONDITIONS, TESTED -- {len(syms)} stocks, {months} months\n")
    print(f"  symbols: {', '.join(syms)}\n")
    print(f"  {'rule':<30} {'CAGR':>8} {'max DD':>9} {'invested':>10}")
    print("  " + "-" * 60)

    for name, rule in RULES:
        curves, exposure = [], []
        for s in syms:
            closes = series[s][1]
            curves.append(equity_curve(closes, rule))
            inv = [1 if (features(closes, t) is not None and rule(features(closes, t)))
                   else 0 for t in range(len(closes) - 1)]
            exposure.append(sum(inv) / len(inv))
        port = combine(curves)
        cagr, mdd = stats(port, len(port))
        pct_inv = sum(exposure) / len(exposure)
        print(f"  {name:<30} {cagr*100:7.2f}% {mdd*100:8.1f}% {pct_inv*100:9.1f}%")

    bdates, bcloses = series[BENCH]
    bench = [1.0]
    for t in range(len(bcloses) - 1):
        bench.append(bench[-1] * (bcloses[t + 1] / bcloses[t]))
    bench = bench[1:]
    bc, bd = stats(bench, len(bench))
    print("  " + "-" * 60)
    print(f"  {'SPY buy & hold (benchmark)':<30} {bc*100:7.2f}% {bd*100:8.1f}% {100.0:9.1f}%")
    print("\n  Cash earns 0%, which biases every filtered row DOWNWARD.")
    print("  Stops and trails are NOT modelled -- monthly bars are too coarse.")


if __name__ == "__main__":
    main()
