#!/usr/bin/env python3
"""
Monthly signal generator for the dual-momentum plan in reference/STRATEGY.md.

The rule, in full:

  1. For each asset compute 12-1 momentum -- the return from ~12 months ago to
     ~1 month ago, skipping the most recent month. The skip is not decoration:
     the last month carries short-term reversal that runs against momentum, and
     Jegadeesh & Titman's construction omits it for that reason.
  2. An asset is ELIGIBLE only if 12-1 momentum is positive AND the current
     close is above its 10-month moving average. Both conditions, not either --
     the absolute filter is the entire drawdown-control claim of the strategy.
  3. Rank eligible assets by 12-1 momentum, hold the top N equal-weighted.
  4. Any unfilled slot goes to the cash proxy. A month that allocates entirely
     to cash is a signal, not a non-event, and is logged like any other.

No prices are fetched here. The close series is read from disk so a signal is
reproducible: re-running this for a past date must produce what it produced
then, which is impossible if it reaches for a live quote. An asset without
enough history is reported INELIGIBLE with the reason stated -- never assumed
flat, never back-filled, never estimated from a shorter window. A momentum
number computed from fabricated history is worse than no signal, because it
ranks.

Usage:
    python3 signal_dual_momentum.py closes.json [--asof YYYY-MM-DD]
                                    [--top 3] [--emit-ledger]

closes.json is {"SPY": {"YYYY-MM-DD": close, ...}, ...} of MONTHLY closes.
"""
import json, sys, os
from datetime import datetime

# MONTHLY basis, matching backtest.py and the measured result in
# reference/STRATEGY.md. These were daily (252/21/200) until 2026-09-11. The
# daily variant was never backtested; the monthly one was, over 235 months. What
# runs live must be what was actually measured, so the untested parameterisation
# is the one that had to go -- not the other way round.
LOOKBACK = 12    # months
SKIP = 1         # months, omitted to avoid short-term reversal
MA_WINDOW = 10   # months; the canonical monthly equivalent of the 200-day SMA
CASH = "BIL"
STRATEGY = "dual-momentum"


def check_params(top, universe, lock_path=None):
    """Compare effective parameters against the lock. Returns a list of drifts.

    Guards the failure mode that kills this experiment silently: a future session
    re-fits after a losing stretch, and the ledger goes on looking rigorous. The
    lock cannot stop a determined change -- editing it is a one-line diff -- but
    it stops an accidental or quiet one, which is the realistic threat. A
    re-fitted run has to announce itself in version control with a name attached.

    `top` is checked because it is a CLI flag: the easiest parameter to change
    without touching a tracked file.
    """
    lock_path = lock_path or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          "params.lock.json")
    if not os.path.exists(lock_path):
        return [f"no lock file at {lock_path} -- parameters are unverified"]
    with open(lock_path) as fh:
        locked = json.load(fh)["params"]
    effective = {"lookback": LOOKBACK, "skip": SKIP, "ma_window": MA_WINDOW,
                 "top": top, "cash": CASH, "universe": sorted(universe)}
    drift = []
    for key, want in locked.items():
        got = effective.get(key)
        if key == "universe":
            want = sorted(want)
        if got != want:
            drift.append(f"{key}: locked {want!r}, running {got!r}")
    return drift


def closes_asof(series, asof):
    """Monthly closes up to and including asof, oldest first."""
    return [px for d, px in sorted(series.items()) if d <= asof]


def momentum_12_1(series, asof):
    """Return (momentum, reason). momentum is None when history is insufficient."""
    px = closes_asof(series, asof)
    if len(px) < LOOKBACK:
        return None, f"insufficient history ({len(px)} monthly closes, need {LOOKBACK})"
    start, end = px[-LOOKBACK], px[-(SKIP + 1)]
    if start == 0:
        return None, "zero price in lookback window"
    return (end - start) / start, None


def moving_average(series, asof, window=MA_WINDOW):
    px = closes_asof(series, asof)
    if len(px) < window:
        return None
    return sum(px[-window:]) / window


def evaluate(universe, asof):
    """Return (eligible, rejected). Eligible is sorted by momentum, best first."""
    eligible, rejected = [], []
    for symbol, series in universe.items():
        if symbol == CASH:
            continue
        mom, reason = momentum_12_1(series, asof)
        if mom is None:
            rejected.append({"symbol": symbol, "reason": reason})
            continue
        ma = moving_average(series, asof)
        if ma is None:
            rejected.append({"symbol": symbol, "reason": "insufficient history for the 10-month MA"})
            continue
        px = closes_asof(series, asof)[-1]
        if mom <= 0:
            rejected.append({"symbol": symbol, "momentum": mom,
                             "reason": f"12-1 momentum not positive ({mom:+.2%})"})
        elif px <= ma:
            rejected.append({"symbol": symbol, "momentum": mom,
                             "reason": f"below 10-month MA ({px:.2f} <= {ma:.2f})"})
        else:
            eligible.append({"symbol": symbol, "momentum": mom, "price": px, "ma": ma})
    eligible.sort(key=lambda a: -a["momentum"])
    return eligible, rejected


def allocate(eligible, top):
    """Top N equal-weighted; unfilled slots go to cash."""
    held = eligible[:top]
    weight = 1.0 / top
    alloc = [{"symbol": a["symbol"], "weight": weight, "momentum": a["momentum"],
              "price": a["price"]} for a in held]
    if len(held) < top:
        alloc.append({"symbol": CASH, "weight": weight * (top - len(held)),
                      "momentum": None, "price": None})
    return alloc


def ledger_lines(alloc, asof):
    """Ledger records, pre-registered: written at signal time, before any outcome."""
    out = []
    for i, a in enumerate(alloc, 1):
        out.append({
            "id": f"{asof}-DM-{i:02d}",
            "symbol": a["symbol"],
            "instrument": "etf",
            "direction": "long",
            "strategy": STRATEGY,
            "opened": f"{asof}T20:00:00Z",
            "closed": None,
            "entry": a["price"],
            "stop": round(a["price"] * 0.75, 4) if a["price"] else None,
            "target": None,
            "exit": None,
            "weight": round(a["weight"], 4),
            "realized_pnl": None,
            "exit_reason": None,
            "thesis": (
                f"Dual momentum monthly signal. 12-1 momentum {a['momentum']:+.2%}, "
                f"above the 10-month MA. Held to next monthly rebalance; -25% catastrophic "
                f"stop for gap risk only, not trade management."
                if a["momentum"] is not None else
                "Dual momentum monthly signal: no eligible asset for this slot, "
                "allocated to cash. A cash month is a signal, not a skipped trade."
            ),
        })
    return out


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__.strip())
        return 1
    path, asof, top, emit = args[0], None, 3, False
    i = 1
    while i < len(args):
        if args[i] == "--asof" and i + 1 < len(args):
            asof, i = args[i + 1], i + 2
        elif args[i] == "--top" and i + 1 < len(args):
            top, i = int(args[i + 1]), i + 2
        elif args[i] == "--emit-ledger":
            emit, i = True, i + 1
        else:
            i += 1

    if not os.path.exists(path):
        print(f"No close series at {path} -- cannot generate a signal.")
        return 1
    with open(path) as fh:
        universe = json.load(fh)
    if asof is None:
        asof = max(d for s in universe.values() for d in s)

    traded = [s for s in universe if s != CASH]
    drift = check_params(top, traded)

    eligible, rejected = evaluate(universe, asof)
    alloc = allocate(eligible, top)

    if emit:
        if drift:
            # Refuse, don't warn. A warning on stdout gets piped into the ledger
            # alongside the records it was warning about, and nobody reads it.
            sys.stderr.write("REFUSING to emit: parameters differ from params.lock.json\n")
            for d in drift:
                sys.stderr.write(f"  {d}\n")
            sys.stderr.write(
                "\nIf this change is deliberate, edit params.lock.json and commit it\n"
                "so the re-fit is on the record. See reference/STRATEGY.md.\n")
            return 2
        for rec in ledger_lines(alloc, asof):
            print(json.dumps(rec))
        return 0

    if drift:
        print("⚠ PARAMETER DRIFT versus params.lock.json:")
        for d in drift:
            print(f"    {d}")
        print("  Ledger emission is blocked until the lock is updated and committed.\n")

    print(f"DUAL MOMENTUM signal -- as of {asof}\n")
    print(f"  ELIGIBLE ({len(eligible)}):")
    for a in eligible:
        print(f"    {a['symbol']:<6} mom {a['momentum']:+8.2%}   "
              f"px {a['price']:>8.2f}  ma10 {a['ma']:>8.2f}")
    if not eligible:
        print("    none")
    print(f"\n  REJECTED ({len(rejected)}):")
    for r in rejected:
        print(f"    {r['symbol']:<6} {r['reason']}")
    print(f"\n  ALLOCATION (top {top}, equal weight):")
    for a in alloc:
        m = f"mom {a['momentum']:+.2%}" if a["momentum"] is not None else "cash — no eligible asset"
        print(f"    {a['symbol']:<6} {a['weight']:>6.1%}   {m}")
    if any(a["symbol"] == CASH for a in alloc):
        print("\n  Note: a cash allocation is the absolute filter doing its job.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
