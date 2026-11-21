"""Ledger loading and normalisation."""
import json
import os
from collections import OrderedDict
from datetime import datetime, timedelta, timezone

DEFAULT_LEDGER = os.path.join(
    os.path.dirname(__file__), "..", "..", "skills", "robinhood-autotrader", "paper", "trades.jsonl")

ET = timezone(timedelta(hours=-4))  # EDT; good enough for hour-of-day buckets Mar-Nov


def ledger_path():
    return os.environ.get("TARS_LEDGER", os.path.normpath(DEFAULT_LEDGER))


def load(path=None):
    rows = []
    with open(path or ledger_path()) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def parse_ts(s):
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def is_owner_option(r):
    return (str(r.get("id", "")).endswith("-USER")
            and str(r.get("instrument", "")).startswith("option")
            and r.get("realized_pnl") is not None
            and r.get("closed"))


def owner_option_trades(rows):
    """Closed owner option round trips, sorted by close time, with derived fields."""
    out = []
    for r in rows:
        if not is_owner_option(r):
            continue
        closed = parse_ts(r["closed"])
        out.append({
            "id": r["id"],
            "symbol": r.get("symbol"),
            "kind": "call" if "call" in r["instrument"] else "put",
            "qty": float(r.get("qty") or 0),
            "entry": r.get("entry"),
            "exit": r.get("exit"),
            "pnl": float(r["realized_pnl"]),
            "closed": closed,
            "day": closed.astimezone(ET).date().isoformat(),
            "hour_et": closed.astimezone(ET).hour,
        })
    out.sort(key=lambda t: t["closed"])
    return out


def by_day(trades):
    days = OrderedDict()
    for t in trades:
        days.setdefault(t["day"], []).append(t)
    return days


def closed_equity(rows):
    out = []
    for r in rows:
        if r.get("instrument") == "equity" and r.get("realized_pnl") is not None \
                and isinstance(r.get("closed"), str) and r.get("exit") is not None:
            out.append(r)
    return out
