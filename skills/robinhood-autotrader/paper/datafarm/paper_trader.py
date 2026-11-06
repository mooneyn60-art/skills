"""
Data Farm PAPER TRADER: runs the frozen datafarm.py setups forward on new
SPY minute bars and keeps a paper account. No real orders, ever.

Each run (called by the desk, see routines/DATA_FARM_PAPER.md):
  1. --bars FILE: merge a saved get_equity_historicals result (SPY, minute)
     into paper/history/spy_1min.json. Interpolated (filler) bars are dropped.
  2. Re-run every setup on the stored days (rules are frozen: the hash of
     datafarm.py is recorded, and a changed hash starts a new forward book).
  3. Every trade on a day >= FORWARD_START is a forward paper trade. Trades
     whose day is still in progress and that have not hit stop/target are
     OPEN, marked at the last bar. Writes paper/datafarm/paper_book.json and
     prints the account: closed R, open R, by setup, and the paper equity of
     a 2,000 account risking 1% per trade.

Usage:  python3 paper/datafarm/paper_trader.py [--bars saved_tool_result.json]
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datafarm as farm  # noqa: E402

HERE = Path(__file__).resolve().parent
BOOK = HERE / "paper_book.json"
FORWARD_START = "2026-10-15"     # first day after the rules were frozen
START_EQUITY = 2000.0
RISK_PCT = 0.01


def merge(path):
    raw = json.load(open(farm.DATA))
    res = json.load(open(path))
    res = res.get("data", res)
    added = 0
    for r in res["results"]:
        if r.get("symbol", "SPY") != "SPY":
            continue
        for b in r["bars"]:
            if b.get("interpolated"):
                continue
            k = b["begins_at"][:16]
            if k not in raw:
                added += 1
            raw[k] = [float(b["open_price"]), float(b["high_price"]), float(b["low_price"]),
                      float(b["close_price"]), int(b.get("volume") or 0)]
    json.dump({k: raw[k] for k in sorted(raw)}, open(farm.DATA, "w"), separators=(",", ":"))
    return added


def rules_hash():
    return hashlib.sha256(open(farm.__file__, "rb").read()).hexdigest()[:12]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bars")
    a = ap.parse_args()
    if a.bars:
        print(f"merged {merge(a.bars)} new SPY minute bars")
    names, trades, counts, per_day = farm.run()
    days = farm.load()
    h = rules_hash()
    prev = json.load(open(BOOK)) if BOOK.exists() else {}
    start = FORWARD_START
    if prev.get("rules_hash") and prev["rules_hash"] != h:
        # rules changed: the old forward record is kept, a new one starts tomorrow-onward
        start = max(prev.get("forward_start", FORWARD_START), names[-1])
        print(f"RULES CHANGED ({prev['rules_hash']} -> {h}); forward book restarts from {start}")
    fwd = [t for t in trades if t["day"] >= start]
    last_day = names[-1]
    last_t = days[last_day][-1]["t"]
    for t in fwd:
        live = t["day"] == last_day and last_t < farm.TIME_EXIT and t["reason"] in ("close",)
        t["status"] = "open" if live else "closed"
    eq = START_EQUITY
    for t in sorted([t for t in fwd if t["status"] == "closed"], key=lambda t: (t["day"], t["t_in"])):
        eq += eq * RISK_PCT * t["R"]
    book = {"rules_hash": h, "forward_start": start, "as_of": f"{last_day} {last_t} ET",
            "equity": round(eq, 2), "start_equity": START_EQUITY, "risk_pct": RISK_PCT, "trades": fwd}
    json.dump(book, open(BOOK, "w"), indent=0)
    closed = [t for t in fwd if t["status"] == "closed"]
    print(f"PAPER BOOK  rules {h}  forward since {start}  as of {book['as_of']}")
    print(f"  closed {len(closed)}  open {len(fwd) - len(closed)}  equity {eq:,.2f} (start {START_EQUITY:,.0f}, 1% risk/trade)")
    for s in farm.SETUPS:
        ts = [t for t in closed if t["setup"] == s]
        if ts:
            print(f"  {s:<16} n={len(ts):>3}  sum R {sum(t['R'] for t in ts):+.2f}  win% {100*sum(t['R']>0 for t in ts)/len(ts):.0f}")
    for t in fwd:
        if t["status"] == "open":
            print(f"  OPEN {t['setup']} {t['side']} @ {t['entry']} stop {t['stop']} target {t['target']} (since {t['t_in']})")


if __name__ == "__main__":
    main()
