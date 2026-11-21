"""Pre-trade check for a same-day option the owner asks the desk to place.

Encodes the 10/15 lessons as questions with thresholds; returns warnings, not blocks
(blocks live in guard.py and only for adopted rules).
"""

def check(side, qty, spy_move_pct, day_pnl=0.0, last_side=None, minutes_since_last=None,
          usual_qty=3, has_stop=False):
    w = []
    if abs(spy_move_pct) < 0.4:
        w.append(f"flat tape: SPY {spy_move_pct:+.2f}% (< 0.4%); your wins come from trend days")
    if qty > usual_qty:
        w.append(f"size {qty} is above your usual {usual_qty}")
    if day_pnl < 0 and qty > usual_qty:
        w.append("sizing up while red on the day")
    if last_side and last_side != side and minutes_since_last is not None and minutes_since_last < 15:
        w.append(f"direction flip {last_side}->{side} after {minutes_since_last} min")
    if not has_stop:
        w.append("no stop named for this trade")
    return w
