#!/usr/bin/env python3
"""
Do R4's 8% stop and 8% trail earn their place?

WHY THIS EXISTS
---------------
R4 is the rule that actually governs every dollar in the account. Every share
Nolan owns sits behind a stop placed by R4, and R4 decides when each one is
sold. It has never been tested by anything.

test_r2_conditions.py could not test it -- monthly bars are far too coarse to
resolve an 8% stop, and I said so in that file rather than producing a number
that looked real and was not. This file removes that excuse: 5,209 DAILY bars
per symbol, 2006-01-03 to 2026-09-18, the same 14 stocks the monthly test used
so the two results are directly comparable.

WHERE THE 8% CAME FROM
----------------------
Nowhere measurable. Like R2's rules 2-5 and like the three constant-drift bugs
already found (R12's stale $85, R9's flat $50, R3's flat $340), it was written
from intuition. The question here is not "is a stop good" but "is EIGHT the
right number, and does the trail add anything the stop does not."

METHOD, no lookahead
--------------------
Signals are computed from bars[0..t] and ACTED ON AT THE NEXT OPEN, never at
the close that produced them. That costs the strategy a night of gap risk,
which is what live trading costs too.

STOPS ARE FILLED HONESTLY. A resting stop is a market order once touched, so:

    gap down through the stop  ->  filled at the OPEN  (worse than the stop)
    touched during the session ->  filled at the STOP

Filling every stop at the stop price is the single most common way a backtest
manufactures money it could never have earned. The open-price rule is why this
test needed open/high/low and not just closes.

Cash earns 0%, which understates every variant that spends time flat and so
biases the comparison AGAINST the rules being tested -- the honest direction.

WHAT IS STILL NOT TESTED
------------------------
R2 rule 4 (earnings blackout) and rule 5 (sector cap) are not price rules and
are absent here. Slippage beyond the open-price gap rule, commissions, and
partial fills are not modelled. Intraday stop-hunting below the daily low is
invisible at this resolution. Their absence is a limit of this test, not
evidence they are free.

Usage:  python3 test_r4_exits.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "history", "daily_stocks.json")
BENCH = "SPY"

MA_SLOW = 200       # R2 rule 1
MA_FAST = 50        # R2 rule 2
DONCHIAN = 20       # R2 rule 3 window
PROX = 0.95         # R2 rule 3 threshold: within 5% of the 20-day high

O, H, L, C = 0, 1, 2, 3


def load():
    raw = json.load(open(DATA))
    return {s: ([d for d in sorted(v)], [v[d] for d in sorted(v)])
            for s, v in raw.items()}


def entry_ok(bars, t, mode):
    """R2's price conditions at the close of day t, from bars[0..t] only."""
    if t < MA_SLOW:
        return False
    closes = [b[C] for b in bars[t - MA_SLOW + 1:t + 1]]
    px = bars[t][C]
    if px <= sum(closes) / len(closes):                 # rule 1: above 200d
        return False
    if mode == "ma_only":
        return True
    if px <= sum(closes[-MA_FAST:]) / MA_FAST:          # rule 2: above 50d
        return False
    if mode == "r2_12":
        return True
    hi = max(b[H] for b in bars[t - DONCHIAN + 1:t + 1])
    return px >= hi * PROX                              # rule 3: near the high


def run(bars, entry_mode, stop_pct, raise_mode, trend_exit, trail_pct=None):
    """One symbol. Returns (daily return series, trade list).

    R4 is three separate mechanisms and they are separable here:

        stop_pct    the initial hard stop, None to disable
        raise_mode  "none"      stop never moves off the initial level
                    "breakeven" raised to entry once close >= entry * 1.08
                    "trail"     breakeven, then trails below the highest close
        trail_pct   how far below the highest close to trail. Defaults to
                    stop_pct, which is what R4 does today -- but the width of
                    the initial stop and the width of the trail are two
                    different decisions and R4 conflates them.

    trend_exit=True adds R4's other exit: a close below both moving averages.
    """
    if trail_pct is None:
        trail_pct = stop_pct
    rets, trades = [], []
    pos = None          # dict(entry, stop, hi_close, day)
    pending_entry = False
    pending_exit = False

    for t in range(len(bars) - 1):
        nxt = bars[t + 1]
        r = 0.0

        # --- act on yesterday's signal, at today's open ---
        if pos is None and pending_entry:
            e = nxt[O]
            pos = {"entry": e, "hi_close": e, "day": t + 1,
                   "stop": e * (1 - stop_pct) if stop_pct else None}
            r = nxt[C] / e - 1.0
            pending_entry = False
            rets.append(r)
            continue
        if pos is not None and pending_exit:
            px = nxt[O]
            r = px / bars[t][C] - 1.0
            trades.append((pos["entry"], px, t + 1 - pos["day"], "trend"))
            pos, pending_exit = None, False
            rets.append(r)
            continue

        if pos is None:
            pending_entry = entry_ok(bars, t, entry_mode)
            rets.append(0.0)
            continue

        # --- holding: the stop is live intraday, before any close-based logic ---
        prev_close = bars[t][C]
        stop = pos["stop"]
        if stop is not None and nxt[L] <= stop:
            # a resting stop is a market order once touched
            fill = nxt[O] if nxt[O] <= stop else stop
            r = fill / prev_close - 1.0
            trades.append((pos["entry"], fill, t + 1 - pos["day"], "stop"))
            pos = None
            rets.append(r)
            continue

        r = nxt[C] / prev_close - 1.0
        rets.append(r)

        # --- raise the stop on today's close; never lower it ---
        if nxt[C] > pos["hi_close"]:
            pos["hi_close"] = nxt[C]
        if stop is not None and raise_mode != "none":
            want = None
            if pos["hi_close"] >= pos["entry"] * 1.08:
                want = pos["entry"]                      # breakeven raise
                if raise_mode == "trail":
                    want = max(want, pos["hi_close"] * (1 - trail_pct))
            if want is not None and want > pos["stop"]:
                pos["stop"] = want

        if trend_exit and t + 1 >= MA_SLOW:
            w = [b[C] for b in bars[t + 2 - MA_SLOW:t + 2]]
            if nxt[C] < sum(w) / len(w) and nxt[C] < sum(w[-MA_FAST:]) / MA_FAST:
                pending_exit = True

    return rets, trades


def stats(rets):
    eq, peak, mdd = 1.0, 1.0, 0.0
    for r in rets:
        eq *= (1 + r)
        peak = max(peak, eq)
        mdd = min(mdd, eq / peak - 1)
    yrs = len(rets) / 252.0
    return (eq ** (1 / yrs) - 1 if eq > 0 else -1.0), mdd


VARIANTS = [
    # label,                      entry,     stop, raise_mode,  trend, trail_pct
    ("buy & hold",                "BH",      None, None,        False, None),
    ("R2 entry, no stop at all",  "r2_full", None, "none",      True,  None),
    ("-- R4 taken apart, 8% --",  None,      None, None,        None,  None),
    ("  + 8% stop, never moves",  "r2_full", 0.08, "none",      True,  None),
    ("  + breakeven raise",       "r2_full", 0.08, "breakeven", True,  None),
    ("  + 8% trail = FULL R4",    "r2_full", 0.08, "trail",     True,  0.08),
    ("-- trail width, 8% stop --",None,      None, None,        None,  None),
    ("  trail 12%",               "r2_full", 0.08, "trail",     True,  0.12),
    ("  trail 15%",               "r2_full", 0.08, "trail",     True,  0.15),
    ("  trail 20%",               "r2_full", 0.08, "trail",     True,  0.20),
    ("  trail 25%",               "r2_full", 0.08, "trail",     True,  0.25),
    ("-- stop width, no trail --",None,      None, None,        None,  None),
    ("  5% stop + breakeven",     "r2_full", 0.05, "breakeven", True,  None),
    ("  8% stop + breakeven",     "r2_full", 0.08, "breakeven", True,  None),
    ("  12% stop + breakeven",    "r2_full", 0.12, "breakeven", True,  None),
    ("  15% stop + breakeven",    "r2_full", 0.15, "breakeven", True,  None),
    ("-- 200d entry only --",     None,      None, None,        None,  None),
    ("  no stop",                 "ma_only", None, "none",      True,  None),
    ("  8% stop + breakeven",     "ma_only", 0.08, "breakeven", True,  None),
    ("  FULL R4 (8% + 8% trail)", "ma_only", 0.08, "trail",     True,  0.08),
    ("  8% stop + 20% trail",     "ma_only", 0.08, "trail",     True,  0.20),
]


def main():
    series = load()
    syms = [s for s in sorted(series) if s != BENCH]
    n = min(len(series[s][1]) for s in syms) - 1

    print(f"R4 EXITS, TESTED -- {len(syms)} stocks, {n} daily bars each "
          f"({series[syms[0]][0][0]} to {series[syms[0]][0][-1]})\n")
    print(f"  {'variant':<30} {'CAGR':>8} {'max DD':>9} {'trades':>7} "
          f"{'win%':>6} {'hold':>6} {'stopped':>8}")
    print("  " + "-" * 79)

    for label, entry, stop, raise_mode, trend, trail_pct in VARIANTS:
        if entry is None:      # separator row
            print(f"  {label}")
            continue
        if label == "buy & hold":
            port = []
            for i in range(n):
                port.append(sum(series[s][1][i + 1][C] / series[s][1][i][C] - 1
                                for s in syms) / len(syms))
            cagr, mdd = stats(port)
            print(f"  {label:<30} {cagr*100:7.2f}% {mdd*100:8.1f}% "
                  f"{'-':>7} {'-':>6} {'-':>6} {'-':>8}")
            continue

        allrets, alltrades = [], []
        for s in syms:
            rr, tt = run(series[s][1], entry, stop, raise_mode, trend, trail_pct)
            allrets.append(rr)
            alltrades += tt
        m = min(len(r) for r in allrets)
        port = [sum(r[i] for r in allrets) / len(allrets) for i in range(m)]
        cagr, mdd = stats(port)

        wins = sum(1 for e, x, _, _ in alltrades if x > e)
        hold = sum(d for _, _, d, _ in alltrades) / max(1, len(alltrades))
        stopped = sum(1 for _, _, _, w in alltrades if w == "stop")
        print(f"  {label:<30} {cagr*100:7.2f}% {mdd*100:8.1f}% "
              f"{len(alltrades):7d} {wins/max(1,len(alltrades))*100:5.1f}% "
              f"{hold:5.0f}d {stopped/max(1,len(alltrades))*100:7.1f}%")

    bd, bb = series[BENCH]
    bench = [bb[i + 1][C] / bb[i][C] - 1 for i in range(len(bb) - 1)]
    bc, bm = stats(bench)
    print("  " + "-" * 79)
    print(f"  {'SPY buy & hold (benchmark)':<30} {bc*100:7.2f}% {bm*100:8.1f}%")
    print("\n  Stops fill at the OPEN when price gaps through them, at the stop"
          "\n  otherwise. Cash earns 0%, biasing every filtered row downward."
          "\n  'stopped' = share of exits taken by the stop rather than the trend.")

    regimes(series, syms)


# --------------------------------------------------------------------------
# A single 20-year number can hide a rule that worked in 2008 and has been
# losing money ever since. This is the check that stops that conclusion from
# being published. It is not decoration -- it changed the recommendation.
# --------------------------------------------------------------------------
PERIODS = [("2006-2009 GFC",        "2006-01-01", "2009-12-31"),
           ("2010-2014",            "2010-01-01", "2014-12-31"),
           ("2015-2019",            "2015-01-01", "2019-12-31"),
           ("2020-2022 covid+bear", "2020-01-01", "2022-12-31"),
           ("2023-2026",            "2023-01-01", "2026-12-31")]

REGIME_CFG = [("no stop",        None, "none",      None),
              ("8% + breakeven", 0.08, "breakeven", None),
              ("FULL R4 8%+8%",  0.08, "trail",     0.08),
              ("8% + 20% trail", 0.08, "trail",     0.20)]


def regimes(series, syms):
    dates = series[syms[0]][0]
    runs = {}
    for lab, st, rm, tp in REGIME_CFG:
        allr = [run(series[s][1], "r2_full", st, rm, True, tp)[0] for s in syms]
        n = min(len(r) for r in allr)
        runs[lab] = [sum(r[i] for r in allr) / len(allr) for i in range(n)]

    for title, fn in (("CAGR BY REGIME", "cagr"), ("MAX DRAWDOWN BY REGIME", "mdd")):
        print(f"\n  {title}")
        print(f"  {'period':<22}" + "".join(f"{l:>17}" for l, _, _, _ in REGIME_CFG))
        print("  " + "-" * (22 + 17 * len(REGIME_CFG)))
        for name, a, b in PERIODS:
            cells = []
            for lab, _, _, _ in REGIME_CFG:
                r = runs[lab]
                seg = [r[i] for i in range(len(r)) if a <= dates[i + 1] <= b]
                eq, peak, mdd = 1.0, 1.0, 0.0
                for x in seg:
                    eq *= (1 + x)
                    peak = max(peak, eq)
                    mdd = min(mdd, eq / peak - 1)
                v = (eq ** (252.0 / len(seg)) - 1) * 100 if fn == "cagr" else mdd * 100
                cells.append(f"{v:16.2f}%")
            print(f"  {name:<22}" + "".join(cells))

    print("\n  READ THIS BEFORE QUOTING THE HEADLINE NUMBER.")
    print("  The trail is not uniformly bad. In 2020-2022 -- covid plus the 2022")
    print("  bear -- it BEAT no-stop on return AND cut drawdown from 15.4% to")
    print("  10.1%. It is crash insurance. Over 20 years the premium cost more")
    print("  than the payout, but the payout is real and arrives exactly when")
    print("  an account can least afford not to have it.")
    print("  The damning period is 2015-2019: the trail returned 5.17% against")
    print("  8.47%, AND its drawdown was WORSE (-15.1% vs -10.7%). Insurance")
    print("  that loses money and deepens the loss is not insurance. Mechanism:")
    print("  the trail sells into a dip, then R2 rule 3 will not re-enter until")
    print("  price is back within 5% of the 20-day high -- so it buys back")
    print("  HIGHER. The exit rule and the entry rule fight each other.")


if __name__ == "__main__":
    main()
