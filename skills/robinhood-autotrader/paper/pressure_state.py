"""R16 pressure-state inputs. Prints data only (R14.1): no verdicts.

Reads paper/trades.jsonl and lists TARS-owned closed trades on the live
account, oldest first, with each trade's sign and R-multiple, then prints
the two counts R16 is evaluated on:
  - consecutive losing closes, counting back from the most recent
  - losing closes inside the last 5 weekdays (same window as R6)

Rules for which rows count:
  - account == "live" and strategy starts with "TARS" (TARS's own
    decisions; user_discretionary / user_directed rows are excluded and
    counted separately so they stay visible)
  - a row whose id ends in "-CORRECTION" replaces the row it corrects
  - exit_reason "not_taken" and rows without a close time or realized
    result are skipped
Dollar amounts are never printed (R13): only sign and R.

Usage: python3 paper/pressure_state.py [--asof YYYY-MM-DD]
"""
import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path

LEDGER = Path(__file__).resolve().parent / "trades.jsonl"
STREAK_THRESHOLD = 3      # R16 trigger (a)
WINDOW_WEEKDAYS = 5       # R6's rolling window, reused


def load_rows():
    rows = {}
    for line in LEDGER.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        key = d["id"]
        if key.endswith("-CORRECTION"):
            key = key[: -len("-CORRECTION")]
        rows[key] = d  # later rows (corrections) overwrite earlier ones
    return list(rows.values())


def closed_trades(rows):
    out = []
    for d in rows:
        if d.get("account") != "live":
            continue
        if d.get("exit_reason") in (None, "not_taken"):
            continue
        if d.get("closed") is None or d.get("realized_pnl") is None:
            continue
        closed = datetime.fromisoformat(d["closed"].replace("Z", "+00:00"))
        risk = d.get("planned_risk")
        r = d.get("r_multiple")
        if r is None and risk:
            r = d["realized_pnl"] / risk
        out.append({
            "id": d["id"],
            "owner": "TARS" if str(d.get("strategy") or "").startswith("TARS") else "user",
            "closed": closed,
            "sign": "loss" if d["realized_pnl"] < 0 else "win/flat",
            "r": r,
            "exit_reason": d.get("exit_reason"),
        })
    return sorted(out, key=lambda t: t["closed"])


def weekdays_back(asof, n):
    d, seen = asof, 0
    while seen < n:
        if d.weekday() < 5:
            seen += 1
        if seen < n:
            d -= timedelta(days=1)
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--asof", default=date.today().isoformat())
    args = ap.parse_args()
    asof = date.fromisoformat(args.asof)

    trades = [t for t in closed_trades(load_rows()) if t["closed"].date() <= asof]
    tars = [t for t in trades if t["owner"] == "TARS"]
    user = [t for t in trades if t["owner"] == "user"]

    print(f"source: {LEDGER.name}, as of {asof}")
    print(f"TARS-owned closed live trades: {len(tars)}   user-owned: {len(user)}")
    print()
    print(f"{'closed (UTC)':<17} {'result':<9} {'R':>7}  {'exit_reason':<24} id")
    for t in tars:
        r = f"{t['r']:+.2f}" if t["r"] is not None else "n/a"
        print(f"{t['closed']:%Y-%m-%d %H:%M}  {t['sign']:<9} {r:>7}  "
              f"{str(t['exit_reason']):<24} {t['id']}")

    streak = 0
    for t in reversed(tars):
        if t["sign"] != "loss":
            break
        streak += 1

    start = weekdays_back(asof, WINDOW_WEEKDAYS)
    recent_losses = [t for t in tars if t["sign"] == "loss" and t["closed"].date() >= start]
    user_recent_losses = [t for t in user if t["sign"] == "loss" and t["closed"].date() >= start]

    print()
    print(f"consecutive TARS losing closes (latest first): {streak}   "
          f"R16 threshold: {STREAK_THRESHOLD}")
    print(f"TARS losing closes since {start} ({WINDOW_WEEKDAYS} weekdays): {len(recent_losses)}")
    print(f"user-owned losing closes in the same window (not an R16 input): {len(user_recent_losses)}")
    print("R6 breaker state and in-session refuted hypotheses are R16 inputs "
          "this script cannot see; check them by hand.")


if __name__ == "__main__":
    main()
