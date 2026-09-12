#!/usr/bin/env python3
"""
Run several documented strategies over the same history, same rules, same costs.

The point is to have alternatives measured BEFORE one is needed, because the
moment to choose a replacement is the worst possible moment to research one.
Switching after a drawdown, without a rule fixed in advance, is performance
chasing at the strategy level -- you reliably abandon whatever just had its bad
run, which is the disposition effect with extra steps.

Every strategy here is scored identically: monthly rebalance, equal weight unless
stated, cash earns 0%, signals use closes through month t applied to month t+1,
no lookahead. Differences in the table are differences in the RULE, not in how
generously it was measured.

The strategies, and what each one claims:

  momentum       Hold the strongest 12-1 performers that are also above their
                 10-month MA. Jegadeesh & Titman; the baseline in STRATEGY.md.
  reversion      Hold the WEAKEST 12-1 performers. De Bondt & Thaler found
                 long-horizon losers outperform. It is the direct contradiction
                 of momentum, which makes it the cleanest alternative to measure:
                 both cannot be right in the same universe over the same window.
  lowvol         Hold the lowest realised-volatility names, ignoring return
                 entirely. The low-volatility anomaly (Baker, Haugen): low-beta
                 assets have historically delivered better risk-adjusted returns
                 than theory says they should.
  volweight      Momentum selection, but weighted inversely to volatility rather
                 than equally. Risk parity's core idea -- equalise each position's
                 contribution to risk instead of its dollar size.
  equalweight    Hold everything, always. The null hypothesis. Any strategy that
                 cannot beat this is not earning its complexity.
  mom3 / mom6    Momentum at 3- and 6-month lookbacks instead of 12. Jegadeesh &
                 Titman tested 3/6/9/12 and found all of them significant. Real
                 trend-following funds run an ENSEMBLE of speeds for exactly this
                 reason: fast and slow momentum disagree often enough to
                 diversify each other while both earning a positive return, which
                 is the combination blending actually needs.
  breakout       Hold whatever sits closest to its own 12-month high. George &
                 Hwang showed nearness-to-52-week-high predicts returns and is
                 NOT the same signal as trailing return -- a stock can have
                 strong 12-1 momentum while sitting well off its high, and vice
                 versa.
  seasonal       Momentum, but only invested November-April; cash May-October.
                 The Halloween effect is the one candidate whose signal source is
                 not price at all, so its correlation to everything else is low
                 by construction rather than by luck.

Usage:  python3 compare_strategies.py history/monthly.json [--top 3]
"""
import json, sys, statistics as st

LOOKBACK, SKIP, MA_WINDOW = 12, 1, 10
dates_ref = []   # set by prep(); seasonal needs the calendar month


def prep(hist):
    global dates_ref
    syms = sorted(hist)
    dates = sorted(set.intersection(*(set(hist[s]) for s in syms)))
    dates_ref = dates
    return syms, dates, {s: [hist[s][d] for d in dates] for s in syms}


def momentum(px, s, t):
    return px[s][t - SKIP] / px[s][t - LOOKBACK] - 1.0


def above_ma(px, s, t):
    return px[s][t] > sum(px[s][t - MA_WINDOW + 1:t + 1]) / MA_WINDOW


def realised_vol(px, s, t, n=12):
    rets = [px[s][i] / px[s][i - 1] - 1.0 for i in range(t - n + 1, t + 1)]
    return st.pstdev(rets) or 1e-9


def select(kind, syms, px, t, top):
    """Return [(symbol, weight)]. An empty list means all cash."""
    if kind == "equalweight":
        return [(s, 1.0 / len(syms)) for s in syms]

    if kind == "momentum":
        elig = [s for s in syms if momentum(px, s, t) > 0 and above_ma(px, s, t)]
        held = sorted(elig, key=lambda s: -momentum(px, s, t))[:top]
        return [(s, 1.0 / top) for s in held]

    if kind == "reversion":
        # Deliberately no trend filter: requiring price above its MA while
        # selecting the weakest performers is self-contradictory, and stacking
        # it would test a strategy nobody proposed.
        held = sorted(syms, key=lambda s: momentum(px, s, t))[:top]
        return [(s, 1.0 / top) for s in held]

    if kind in ("mom3", "mom6"):
        n = 3 if kind == "mom3" else 6
        def m(sym):
            return px[sym][t - SKIP] / px[sym][t - n] - 1.0
        elig = [sym for sym in syms if m(sym) > 0 and above_ma(px, sym, t)]
        held = sorted(elig, key=lambda sym: -m(sym))[:top]
        return [(sym, 1.0 / top) for sym in held]

    if kind == "breakout":
        def near_high(sym):
            hi = max(px[sym][t - LOOKBACK + 1:t + 1])
            return px[sym][t] / hi
        # Must still be in an uptrend; nearness alone would buy a falling knife
        # that simply has not fallen far yet.
        elig = [sym for sym in syms if above_ma(px, sym, t)]
        held = sorted(elig, key=lambda sym: -near_high(sym))[:top]
        return [(sym, 1.0 / top) for sym in held]

    if kind == "seasonal":
        month = int(dates_ref[t][5:7])
        if month in (5, 6, 7, 8, 9, 10):
            return []
        elig = [sym for sym in syms if momentum(px, sym, t) > 0 and above_ma(px, sym, t)]
        held = sorted(elig, key=lambda sym: -momentum(px, sym, t))[:top]
        return [(sym, 1.0 / top) for sym in held]

    if kind == "lowvol":
        held = sorted(syms, key=lambda s: realised_vol(px, s, t))[:top]
        return [(s, 1.0 / top) for s in held]

    if kind == "volweight":
        elig = [s for s in syms if momentum(px, s, t) > 0 and above_ma(px, s, t)]
        held = sorted(elig, key=lambda s: -momentum(px, s, t))[:top]
        if not held:
            return []
        inv = {s: 1.0 / realised_vol(px, s, t) for s in held}
        tot = sum(inv.values())
        # Scaled so a full book is fully invested, matching the others.
        return [(s, inv[s] / tot) for s in held]

    raise ValueError(kind)


def monthly_returns(kind, syms, dates, px, top):
    """Per-month return series for one strategy, for correlation and blending."""
    out = []
    for t in range(max(LOOKBACK, MA_WINDOW), len(dates) - 1):
        book = select(kind, syms, px, t, top)
        out.append(sum(w * (px[s][t + 1] / px[s][t] - 1.0) for s, w in book))
    return out


def blend(series_a, series_b, wa):
    """Rebalanced blend: wa in A, (1-wa) in B, reset every month."""
    return [wa * a + (1 - wa) * b for a, b in zip(series_a, series_b)]


def curve_of(rets):
    eq, out = 1.0, []
    for r in rets:
        eq *= (1 + r); out.append(eq)
    return out


def run(kind, syms, dates, px, top):
    eq, curve, months_in = 1.0, [], 0
    for t in range(max(LOOKBACK, MA_WINDOW), len(dates) - 1):
        book = select(kind, syms, px, t, top)
        r = sum(w * (px[s][t + 1] / px[s][t] - 1.0) for s, w in book)
        eq *= (1 + r)
        curve.append(eq)
        if book:
            months_in += 1
    return curve, months_in


def mdd(curve):
    peak, worst = curve[0], 0.0
    for v in curve:
        peak = max(peak, v)
        worst = min(worst, v / peak - 1.0)
    return worst


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "history/monthly.json"
    top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 3
    syms, dates, px = prep(json.load(open(path)))

    print(f"{len(syms)} assets, {dates[0][:7]} to {dates[-1][:7]}, top {top}, "
          f"monthly rebalance\n")
    print(f"{'strategy':<14}{'CAGR':>9}{'max DD':>10}{'ret/DD':>9}{'best yr':>10}"
          f"{'worst yr':>10}{'invested':>10}")
    results = {}
    for kind in ("momentum", "mom3", "mom6", "breakout", "seasonal",
                 "reversion", "lowvol", "volweight", "equalweight"):
        curve, months_in = run(kind, syms, dates, px, top)
        n = len(curve)
        c = curve[-1] ** (12.0 / n) - 1.0
        d = mdd(curve)
        yrs = [curve[i + 12] / curve[i] - 1 for i in range(n - 12)]
        results[kind] = (c, d)
        print(f"  {kind:<12}{c:>8.2%}{d:>10.1%}{c/abs(d):>9.2f}"
              f"{max(yrs):>+10.1%}{min(yrs):>+10.1%}{months_in/n:>10.0%}")

    best = max(results, key=lambda k: results[k][0])
    safest = max(results, key=lambda k: results[k][0] / abs(results[k][1]))
    print(f"\n  highest return: {best}    best return-per-drawdown: {safest}")
    print("  A backtest ranking is not a forecast. Differences smaller than the")
    print("  spread between strategies here are well inside what luck produces.")


if __name__ == "__main__":
    main()
