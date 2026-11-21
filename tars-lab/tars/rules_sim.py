"""Counterfactual replay of discipline rules over the owner's option round trips.

A rule set is applied day by day, in close-time order. Trades the rules would have
blocked are dropped; oversize trades are scaled down. Caveat (printed in every
report): this assumes the skipped trades were independent of the ones kept, which
ignores tilt; real effect of a daily stop is probably better than shown.
"""
from itertools import product


def apply(day_trades, daily_stop=None, max_losses_in_row=None, max_qty=None, max_trades=None):
    kept, pnl, streak, n = [], 0.0, 0, 0
    for t in day_trades:
        if daily_stop is not None and pnl <= -daily_stop:
            break
        if max_losses_in_row is not None and streak >= max_losses_in_row:
            break
        if max_trades is not None and n >= max_trades:
            break
        p = t["pnl"]
        if max_qty is not None and t["qty"] > max_qty:
            p = p * max_qty / t["qty"]
        kept.append(p)
        pnl += p
        n += 1
        streak = streak + 1 if p < 0 else 0
    return pnl, len(kept)


def run(days, **rule):
    """days: OrderedDict day -> trades. Returns dict of total, worst_day, days, trades."""
    daily = []
    trades = 0
    for d, ts in days.items():
        p, k = apply(ts, **rule)
        daily.append(p)
        trades += k
    return {
        "total": round(sum(daily), 2),
        "worst_day": round(min(daily), 2) if daily else 0.0,
        "trades": trades,
        "days": len(daily),
    }


GRID = {
    "daily_stop": [None, 150, 200, 300, 400, 600],
    "max_losses_in_row": [None, 2, 3, 4, 5],
    "max_qty": [None, 3, 5, 10],
    "max_trades": [None, 6, 10, 15],
}


def candidates(grid=GRID):
    keys = list(grid)
    for vals in product(*(grid[k] for k in keys)):
        rule = {k: v for k, v in zip(keys, vals) if v is not None}
        yield rule


def describe(rule):
    if not rule:
        return "baseline (no rule)"
    parts = []
    if "daily_stop" in rule:
        parts.append(f"stop for the day at -{rule['daily_stop']:g}")
    if "max_losses_in_row" in rule:
        parts.append(f"stop after {rule['max_losses_in_row']} losses in a row")
    if "max_qty" in rule:
        parts.append(f"max {rule['max_qty']:g} contracts")
    if "max_trades" in rule:
        parts.append(f"max {rule['max_trades']} round trips a day")
    return "; ".join(parts)
