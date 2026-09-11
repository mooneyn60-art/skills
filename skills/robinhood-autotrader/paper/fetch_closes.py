#!/usr/bin/env python3
"""
Build and maintain the monthly-close series that signal_dual_momentum.py reads.

Separated from the signal itself on purpose. The signal must be reproducible --
regenerating it for a past date has to return what it returned then -- which is
only true if it reads a stored series rather than reaching for a live quote.
This script is the only thing that talks to the network, and it is append-only
in spirit: it merges new closes into the existing file rather than replacing it,
so history accumulates instead of being rebuilt (and silently revised) each run.

Two data-integrity rules, both load-bearing:

  1. **Interpolated bars are dropped, never stored.** Robinhood synthesises bars
     to fill gaps; they carry no new information. Storing one would put a price
     in the series that no trade ever happened at, and the momentum figure
     computed from it would look exactly as real as any other. Missing days stay
     missing -- regular-hours series simply omit non-session days, which is
     correct and needs no filling.

  2. **A bar without a usable close is skipped, not defaulted.** No zeros, no
     carry-forward of yesterday's price. See the same rule in market_data.py.

Note: the most recent bar's close is not the official settled close until the
session has settled. Generate month-end signals after settlement, or verify the
final bar against get_equity_quotes.

Usage:
    python3 fetch_closes.py                    # universe -> history/monthly.json
    python3 fetch_closes.py --daily            # keep daily granularity instead
    python3 fetch_closes.py --symbols SPY,QQQ,TLT
"""
import json, os, sys

# Liquid ETFs per reference/STRATEGY.md, plus the cash proxy.
# EEM is deliberately absent: its series is quarantined for inconsistent split
# adjustment (see history/QUARANTINE_eem.json). Re-add only once re-verified.
UNIVERSE = ["SPY", "QQQ", "IWM", "EFA", "VNQ", "GLD", "TLT", "BIL"]


def parse_bars(bars):
    """Fold raw bars into {symbol: {date: close}}.

    Pure -- no network -- so the integrity rules above are directly testable.
    """
    out = {}
    for bar in bars or []:
        if not bar:
            continue
        if bar.get("interpolated") in (True, "true", "True"):
            continue
        symbol, raw = bar.get("symbol"), bar.get("close_price")
        begins = bar.get("begins_at")
        if not symbol or not begins or raw in (None, ""):
            continue
        try:
            close = float(raw)
        except (TypeError, ValueError):
            continue
        if close <= 0:
            continue
        out.setdefault(symbol, {})[begins[:10]] = close
    return out


def to_monthly(daily):
    """Collapse daily closes to one close per month: the month's LAST observation.

    Keyed "YYYY-MM-01" to match history/monthly.json, whose bars are month-start
    labelled. The key is a label, not a claim about which day the price is from --
    the value is always the last real close observed in that month. Nothing is
    synthesised: a month with no trading days simply does not appear.
    """
    out = {}
    for symbol, series in daily.items():
        by_month = {}
        for date, close in sorted(series.items()):
            by_month[date[:7] + "-01"] = close
        out[symbol] = by_month
    return out


def merge(existing, fresh):
    """Fold fresh closes into the stored series. Later data wins per date."""
    merged = {s: dict(d) for s, d in existing.items()}
    for symbol, series in fresh.items():
        merged.setdefault(symbol, {}).update(series)
    return merged


def fetch(rh, symbols, span="5year"):
    """Pull daily regular-hours bars. Returns {symbol: {date: close}}."""
    bars = rh.stocks.get_stock_historicals(
        symbols, interval="day", span=span, bounds="regular"
    )
    return parse_bars(bars)


def load(path):
    if not os.path.exists(path):
        return {}
    with open(path) as fh:
        return json.load(fh)


def main():
    args = sys.argv[1:]
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(here, "history", "monthly.json")
    symbols = UNIVERSE
    monthly = True
    i = 0
    while i < len(args):
        if args[i] == "--out" and i + 1 < len(args):
            out_path, i = args[i + 1], i + 2
        elif args[i] == "--daily":
            monthly, i = False, i + 1
        elif args[i] == "--symbols" and i + 1 < len(args):
            symbols, i = [s.strip().upper() for s in args[i + 1].split(",")], i + 2
        else:
            i += 1

    sys.path.insert(0, os.path.join(os.path.dirname(here), "scripts"))
    from auth import login, logout

    rh = login()
    try:
        fresh = fetch(rh, symbols)
    finally:
        logout()
    if monthly:
        fresh = to_monthly(fresh)

    if not fresh:
        print("No usable bars returned -- nothing written.")
        return 1

    merged = merge(load(out_path), fresh)
    with open(out_path, "w") as fh:
        json.dump(merged, fh, indent=1, sort_keys=True)

    print(f"wrote {out_path}")
    for symbol in sorted(merged):
        dates = sorted(merged[symbol])
        print(f"  {symbol:<5} {len(dates):>5} closes  {dates[0]} -> {dates[-1]}")
    need = 12 if monthly else 273
    short = [s for s in symbols if len(merged.get(s, {})) < need]
    if short:
        print(f"\n  ⚠ under the {need} closes the 12-1 signal needs: {', '.join(short)}")
        print("    Those symbols will be reported ineligible rather than estimated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
