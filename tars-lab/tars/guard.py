"""Pre-trade guard.

Two uses:
  1. Claude Code PreToolUse hook: reads the hook JSON on stdin; for option buys it
     checks the adopted limits against state/today.json and returns a deny decision.
  2. `unprotected`: given a broker positions JSON, lists positions with shares not
     held by a sell order (i.e. no stop), excluding names in the allow list.

The desk refreshes state/today.json each hourly check. If the file is stale or
missing, option buys are DENIED with a reason to refresh it (fail closed): a guard
that silently allows on missing data is how the 10/15 losses compounded.
"""
import json
import os
import sys
from datetime import datetime, timezone

from . import registry

HERE = os.path.dirname(__file__)
STATE = os.environ.get("TARS_STATE", os.path.join(HERE, "..", "state", "today.json"))
OPTION_TOOLS = ("place_option_order",)


def load_state(path=None):
    try:
        with open(path or STATE) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def is_option_open(tool_name, tool_input):
    if not any(tool_name.endswith(t) for t in OPTION_TOOLS):
        return False
    legs = tool_input.get("legs") or []
    effects = {str(l.get("position_effect", "")).lower() for l in legs if isinstance(l, dict)}
    if effects:
        return "open" in effects
    # No legs info: treat a debit/buy as an opening order.
    return str(tool_input.get("direction", tool_input.get("side", ""))).lower() in ("debit", "buy")


def check_option_open(state, limits, today=None, qty=None):
    """Return a list of human-readable violations (empty = allowed)."""
    today = today or datetime.now(timezone.utc).astimezone(registry.ET).date().isoformat()
    if not state or state.get("date") != today:
        return [f"state/today.json is missing or not for {today}; refresh options P/L before buying"]
    v = []
    pnl = float(state.get("options_pnl", 0))
    if "daily_stop" in limits and pnl <= -limits["daily_stop"]:
        v.append(f"daily options stop hit: day P/L {pnl:+.0f} <= -{limits['daily_stop']:g}")
    streak = int(state.get("losses_in_row", 0))
    if "max_losses_in_row" in limits and streak >= limits["max_losses_in_row"]:
        v.append(f"{streak} losses in a row (limit {limits['max_losses_in_row']})")
    n = int(state.get("round_trips", 0))
    if "max_trades" in limits and n >= limits["max_trades"]:
        v.append(f"{n} round trips today (limit {limits['max_trades']})")
    if qty is not None and "max_qty" in limits and qty > limits["max_qty"]:
        v.append(f"size {qty:g} > max {limits['max_qty']:g} contracts")
    return v


def unprotected(positions, allow=("VLO",)):
    out = []
    for p in positions:
        avail = float(p.get("shares_available_for_sells", 0) or 0)
        if avail > 0 and p.get("symbol") not in allow:
            out.append({"symbol": p.get("symbol"), "unprotected_shares": avail,
                        "quantity": float(p.get("quantity", 0))})
    return out


def hook_main(stdin=sys.stdin, stdout=sys.stdout):
    try:
        event = json.load(stdin)
    except ValueError:
        return 0
    name = event.get("tool_name", "")
    tin = event.get("tool_input") or {}
    if not is_option_open(name, tin):
        return 0
    limits = registry.adopted_limits()
    if not limits:
        return 0  # nothing adopted yet: guard is inert by design
    qty = tin.get("quantity")
    qty = float(qty) if qty not in (None, "") else None
    v = check_option_open(load_state(), limits, qty=qty)
    if v:
        json.dump({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "TARS guard (adopted rules): " + "; ".join(v)}}, stdout)
    return 0
