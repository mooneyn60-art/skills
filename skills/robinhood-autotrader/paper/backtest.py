#!/usr/bin/env python3
"""
Walk-forward test of the absolute-momentum filter on real monthly history.

This exists because the experiment does not have to wait years for an answer.
The rule is fully mechanical, so it can be run over two decades of real prices
now and produce a result today. That does not replace live paper trading -- a
backtest is in-sample in a way a forward test is not -- but it answers the one
question STRATEGY.md stakes the whole design on:

    does the absolute filter actually reduce drawdown in a real decline?

That is the strategy's only claim. It does not promise to beat the index on raw
return; it promises comparable return at materially lower drawdown. If it fails
to protect in 2008, 2020 and 2022, it has no reason to exist and the falsifi-
cation condition in STRATEGY.md fires.

Method, with no lookahead: at each month-end t the signal uses closes through t
only, and is applied to the return of month t+1. Cash earns 0%, which
understates the strategy (real T-bills paid something, especially 2006-2007 and
2023-2026) and so biases the comparison AGAINST it -- the honest direction to be
wrong in.

Usage:  python3 backtest.py history/spy_monthly.json [--symbol SPY]
"""
import json, sys, os

LOOKBACK = 12   # months
SKIP = 1        # months, per the 12-1 construction in STRATEGY.md
MA_WINDOW = 10  # months; the canonical monthly equivalent of the 200-day SMA


def signal(closes, t):
    """True = hold the asset next month. Uses closes[:t+1] only.

    Returns None when there is not enough history yet, rather than defaulting to
    invested or to cash -- an unknown signal is not a decision.
    """
    if t < max(LOOKBACK, MA_WINDOW):
        return None
    mom = closes[t - SKIP] / closes[t - LOOKBACK] - 1.0
    ma = sum(closes[t - MA_WINDOW + 1:t + 1]) / MA_WINDOW
    return mom > 0 and closes[t] > ma


def run(dates, closes):
    """Return per-month records with both equity curves, starting at 1.0."""
    rows, strat, bh, invested = [], 1.0, 1.0, False
    for t in range(len(closes) - 1):
        sig = signal(closes, t)
        r = closes[t + 1] / closes[t] - 1.0
        if sig is None:
            continue
        bh *= (1 + r)
        strat *= (1 + r) if sig else 1.0
        rows.append({"date": dates[t + 1], "ret": r, "invested": sig,
                     "strat": strat, "bh": bh})
        invested = sig
    return rows


def max_drawdown(curve):
    peak, worst = curve[0], 0.0
    for v in curve:
        peak = max(peak, v)
        worst = min(worst, v / peak - 1.0)
    return worst


def cagr(curve, months):
    return curve[-1] ** (12.0 / months) - 1.0


def window(rows, lo, hi):
    return [r for r in rows if lo <= r["date"][:7] <= hi]


def drawdown_in(rows, lo, hi, key):
    seg = window(rows, lo, hi)
    return max_drawdown([r[key] for r in seg]) if seg else 0.0


def run_dual(hist, bench="SPY", top=3):
    """Full dual momentum: rank eligible assets, hold top N equal-weighted.

    The single-asset filter parks 30% of its life in 0% cash. This tests whether
    rotating into whatever is actually trending -- bonds and gold in 2008, say --
    recovers the return that parking gives up, which is the whole reason the plan
    holds eight assets rather than one.
    """
    syms = sorted(hist)
    if bench not in hist:
        raise SystemExit(f"benchmark {bench} is not in the universe {syms}; "
                         "pass one that is, or the comparison column is meaningless.")
    dates = sorted(set.intersection(*(set(hist[s]) for s in syms)))
    px = {s: [hist[s][d] for d in dates] for s in syms}
    rows, strat, bh = [], 1.0, 1.0
    for t in range(len(dates) - 1):
        if t < max(LOOKBACK, MA_WINDOW):
            continue
        elig = []
        for s in syms:
            mom = px[s][t - SKIP] / px[s][t - LOOKBACK] - 1.0
            ma = sum(px[s][t - MA_WINDOW + 1:t + 1]) / MA_WINDOW
            if mom > 0 and px[s][t] > ma:
                elig.append((mom, s))
        elig.sort(reverse=True)
        held = [s for _, s in elig[:top]]
        # Unfilled slots sit in cash at 0%, same conservative assumption as above.
        ret = sum(px[s][t + 1] / px[s][t] - 1.0 for s in held) / top if held else 0.0
        strat *= (1 + ret)
        bh *= (1 + px[bench][t + 1] / px[bench][t] - 1.0)
        rows.append({"date": dates[t + 1], "ret": ret, "invested": bool(held),
                     "held": held, "strat": strat, "bh": bh})
    return rows


def report_dual(rows, top):
    n = len(rows)
    sc = [r["strat"] for r in rows]
    bc = [r["bh"] for r in rows]
    print(f"DUAL MOMENTUM (top {top} of 7) -- {n} months, "
          f"{rows[0]['date'][:7]} to {rows[-1]['date'][:7]}\n")
    print(f"{'':<22}{'strategy':>12}{'SPY b&h':>14}")
    print(f"  {'total return':<20}{sc[-1] - 1:>11.1%}{bc[-1] - 1:>14.1%}")
    print(f"  {'CAGR':<20}{cagr(sc, n):>11.2%}{cagr(bc, n):>14.2%}")
    print(f"  {'max drawdown':<20}{max_drawdown(sc):>11.1%}{max_drawdown(bc):>14.1%}")
    fully = sum(1 for r in rows if len(r["held"]) == top)
    print(f"  {'fully invested':<20}{fully / n:>11.0%}{1.0:>14.0%}")
    print("\n  drawdown through each real decline:")
    for label, lo, hi in [("2008 GFC", "2007-10", "2009-03"),
                          ("2011 debt ceiling", "2011-05", "2011-10"),
                          ("2015-16 China", "2015-06", "2016-02"),
                          ("2018 Q4", "2018-09", "2018-12"),
                          ("2020 COVID", "2020-01", "2020-04"),
                          ("2022 bear", "2022-01", "2022-10")]:
        f = drawdown_in(rows, lo, hi, "strat")
        b = drawdown_in(rows, lo, hi, "bh")
        print(f"  {label:<22}{f:>11.1%}{b:>14.1%}"
              f"{'  ✓' if f > b + 0.005 else '  ✗'}")
    from collections import Counter
    c = Counter(s for r in rows for s in r["held"])
    print("\n  months held, by asset:")
    for s, k in c.most_common():
        print(f"    {s:<5}{k:>5}  ({k / n:.0%})")
    print(f"\n  what it held through 2008-09 to 2009-03:")
    for r in rows:
        if "2008-09" <= r["date"][:7] <= "2009-03":
            print(f"    {r['date'][:7]}  {', '.join(r['held']) or 'all cash'}")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "history/spy_monthly.json"
    symbol = "SPY"
    if "--symbol" in sys.argv:
        symbol = sys.argv[sys.argv.index("--symbol") + 1]
    if "--dual" in sys.argv:
        top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 3
        hist = json.load(open(path))
        report_dual(run_dual(hist, top=top), top)
        return 0
    if not os.path.exists(path):
        print(f"No history at {path}.")
        return 1
    series = json.load(open(path))[symbol]
    dates = sorted(series)
    closes = [series[d] for d in dates]

    rows = run(dates, closes)
    n = len(rows)
    sc = [r["strat"] for r in rows]
    bc = [r["bh"] for r in rows]

    print(f"ABSOLUTE-MOMENTUM FILTER on {symbol} -- {n} months, "
          f"{rows[0]['date'][:7]} to {rows[-1]['date'][:7]}\n")
    print(f"{'':<22}{'filtered':>12}{'buy & hold':>14}")
    print(f"  {'total return':<20}{sc[-1] - 1:>11.1%}{bc[-1] - 1:>14.1%}")
    print(f"  {'CAGR':<20}{cagr(sc, n):>11.2%}{cagr(bc, n):>14.2%}")
    print(f"  {'max drawdown':<20}{max_drawdown(sc):>11.1%}{max_drawdown(bc):>14.1%}")
    invested = sum(1 for r in rows if r["invested"])
    print(f"  {'months invested':<20}{invested:>11}{n:>14}")
    print(f"  {'time in market':<20}{invested / n:>11.0%}{1.0:>14.0%}")

    print("\n  drawdown through each real decline (the only claim it makes):")
    print(f"{'':<24}{'filtered':>12}{'buy & hold':>14}")
    for label, lo, hi in [("2008 GFC", "2007-10", "2009-03"),
                          ("2011 debt ceiling", "2011-05", "2011-10"),
                          ("2015-16 China", "2015-06", "2016-02"),
                          ("2018 Q4", "2018-09", "2018-12"),
                          ("2020 COVID", "2020-01", "2020-04"),
                          ("2022 bear", "2022-01", "2022-10")]:
        f = drawdown_in(rows, lo, hi, "strat")
        b = drawdown_in(rows, lo, hi, "bh")
        flag = "  ✓" if f > b + 0.005 else ("  ✗ no protection" if f <= b + 0.005 else "")
        print(f"  {label:<22}{f:>11.1%}{b:>14.1%}{flag}")

    # Whipsaw: exits that were back in within three months, having lost money out.
    whip = 0
    for i in range(1, len(rows)):
        if rows[i - 1]["invested"] and not rows[i]["invested"]:
            for j in range(i + 1, min(i + 4, len(rows))):
                if rows[j]["invested"]:
                    if rows[j]["bh"] / rows[i]["bh"] - 1 > 0.02:
                        whip += 1
                    break
    switches = sum(1 for i in range(1, len(rows))
                   if rows[i]["invested"] != rows[i - 1]["invested"])
    print(f"\n  signal switches   {switches} in {n} months "
          f"({switches / (n / 12.0):.1f}/yr)")
    print(f"  costly whipsaws   {whip}  (exited, market rose >2%, back in within 3 months)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
