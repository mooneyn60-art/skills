"""
Kelly / fractional-Kelly position sizing for the 200-day + R4 strategy.

RESEARCH_AGENDA item 10 / research/2026-09-30_KELLY_SIZING.md.
Predictions (P1-P3) were committed BEFORE this script was run (commit 331b301).
This script PRINTS RAW NUMBERS ONLY -- no conclusion is hardcoded here (R14).

Reuses load_universe / sma / month_end_dates from momentum_reversal.py so the
universe, gate and month sampling match every other study in this repo.

A "trade": enter at a month-end where close > SMA200; hold with R4 exits
(hard -8%, breakeven raise at +8%, 20% trail below highest close, 200-day
trend exit). Record each RESOLVED trade's net return (exit/entry - 1) minus a
round-trip cost. Censored trades (open at data end) are excluded and counted.

Kelly on the per-trade return distribution R:
  binary Kelly    f = p - (1-p)/b,  b = avg_win / |avg_loss|
  continuous Kelly argmax_f mean(log(1 + f*R))   (growth-optimal single bet)
Bootstrap CI clusters by entry month (item 8's clustering). Four hurdles:
both halves + drop megacaps. Concurrency read against item 4's N_eff ~= 3.9.
"""

import math
import sys
import random
from pathlib import Path
from statistics import mean, median, pstdev

sys.path.insert(0, str(Path(__file__).resolve().parent))
from momentum_reversal import (  # noqa: E402
    load_universe, sma, month_end_dates, SMA_GATE,
    LARGE_CAP_FILE, VOLATILE_FILE, LARGE_CAP_SPLIT,
)

COST = 0.001          # round-trip, matches shadow book; conservative vs item 9
MEGACAPS = {"NVDA", "AAPL", "MSFT", "GOOGL", "AMZN"}
random.seed(20260930)


def trades_for(series):
    """Return list of dicts: {sym, entry_date, ret, days, reason} for every
    RESOLVED 200d+R4 trade. ret is net of COST. Also count censored."""
    out = []
    censored = 0
    mset = set(month_end_dates(series))  # pooled calendar for the universe
    for sym, s in series.items():
        C, dates = s["C"], s["dates"]
        n = len(C)
        for i, d in enumerate(dates):
            if d not in mset:
                continue
            sma200 = sma(C, i, SMA_GATE)
            if sma200 is None or not (C[i] > sma200):
                continue
            entry = C[i]
            stop = entry * 0.92
            hi = entry
            be = False
            exited = False
            for j in range(i + 1, n):
                c = C[j]
                if c > hi:
                    hi = c
                if not be and c >= entry * 1.08:
                    be = True
                    stop = max(stop, entry)
                if be:
                    stop = max(stop, hi * 0.80)
                s200 = sma(C, j, SMA_GATE)
                trend_exit = s200 is not None and c < s200
                if c <= stop:
                    out.append({"sym": sym, "m": d[:7], "ret": c / entry - 1 - COST,
                                "days": j - i, "reason": "hard_stop"})
                    exited = True
                    break
                if trend_exit:
                    out.append({"sym": sym, "m": d[:7], "ret": c / entry - 1 - COST,
                                "days": j - i, "reason": "trend_exit"})
                    exited = True
                    break
            if not exited:
                censored += 1
    return out, censored


def continuous_kelly(rets, lo=0.0, hi=5.0):
    """argmax_f mean(log(1+f*R)); guard against 1+f*R<=0 (bankruptcy)."""
    def g(f):
        tot = 0.0
        for r in rets:
            x = 1 + f * r
            if x <= 1e-9:
                return -1e18  # this f can bankrupt on some trade -> reject
            tot += math.log(x)
        return tot / len(rets)
    # golden-section search on [lo,hi]
    gr = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    c = b - gr * (b - a)
    d = a + gr * (b - a)
    for _ in range(45):
        if g(c) < g(d):
            a = c
        else:
            b = d
        c = b - gr * (b - a)
        d = a + gr * (b - a)
    f = (a + b) / 2
    return f


def summarize(label, trades):
    rets = [t["ret"] for t in trades]
    if len(rets) < 5:
        print(f"\n[{label}] n={len(rets)} too few to summarise")
        return
    wins = [r for r in rets if r > 0]
    losses = [r for r in rets if r <= 0]
    p = len(wins) / len(rets)
    avg_w = mean(wins) if wins else 0.0
    avg_l = mean(losses) if losses else 0.0
    b = (avg_w / abs(avg_l)) if avg_l != 0 else float("inf")
    binary_k = p - (1 - p) / b if b not in (0, float("inf")) else float("nan")
    m = mean(rets)
    sd = pstdev(rets)
    mu_over_var = m / (sd * sd) if sd > 0 else float("nan")
    fk = continuous_kelly(rets)

    # bootstrap CI on continuous Kelly, clustered by entry month
    by_month = {}
    for t in trades:
        by_month.setdefault(t["m"], []).append(t["ret"])
    months = list(by_month.keys())
    boot = []
    for _ in range(300):
        samp = []
        for _ in range(len(months)):
            mm = random.choice(months)
            samp.extend(by_month[mm])
        boot.append(continuous_kelly(samp))
    boot.sort()
    lo5 = boot[int(0.05 * len(boot))]
    hi95 = boot[int(0.95 * len(boot))]

    print(f"\n[{label}]")
    print(f"  n_resolved={len(rets)}  win_rate={p:.3f}  mean={m:+.4f}  sd={sd:.4f}")
    print(f"  avg_win={avg_w:+.4f}  avg_loss={avg_l:+.4f}  payoff_b={b:.3f}")
    print(f"  binary_kelly = {binary_k:+.3f}   (fraction of bankroll)")
    print(f"  mu/var       = {mu_over_var:+.3f}")
    print(f"  CONTINUOUS full Kelly = {fk:+.3f}")
    print(f"  half Kelly            = {fk/2:+.3f}")
    print(f"  bootstrap 90% CI (month-clustered) = [{lo5:+.3f}, {hi95:+.3f}]")
    print(f"  Kelly / N_eff(3.9)   full={fk/3.9:+.3f}  half={fk/7.8:+.3f}")


def main():
    large = load_universe(LARGE_CAP_FILE, exclude={"SPY"})
    volatile = load_universe(VOLATILE_FILE)

    print("=" * 70)
    print("KELLY SIZING -- 200d gate + R4 exits, cost/round-trip =", COST)
    print("=" * 70)

    for uname, series in (("LARGE CAPS (excl SPY)", large), ("VOLATILE NAMES", volatile)):
        tr, cens = trades_for(series)
        print(f"\n##### {uname}: {len(tr)} resolved, {cens} censored at data end")
        # exit-reason mix
        hs = sum(1 for t in tr if t["reason"] == "hard_stop")
        te = len(tr) - hs
        print(f"      exits: hard_stop={hs}  trend_exit={te}  "
              f"mean_days={mean(t['days'] for t in tr):.0f}")
        summarize(f"{uname} ALL", tr)
        # both halves
        first = [t for t in tr if t["m"] < LARGE_CAP_SPLIT[:7]]
        second = [t for t in tr if t["m"] >= LARGE_CAP_SPLIT[:7]]
        summarize(f"{uname} pre-{LARGE_CAP_SPLIT[:7]}", first)
        summarize(f"{uname} post-{LARGE_CAP_SPLIT[:7]}", second)
        # drop megacaps (only meaningful for large caps)
        nomega = [t for t in tr if t["sym"] not in MEGACAPS]
        if len(nomega) != len(tr):
            summarize(f"{uname} ex-megacaps", nomega)

    print("\n" + "=" * 70)
    print("Read against R3's 20% single-name cap and item 4's N_eff~=3.9.")
    print("=" * 70)


if __name__ == "__main__":
    main()
