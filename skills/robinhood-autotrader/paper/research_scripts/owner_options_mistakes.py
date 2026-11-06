"""
Owner (Nolan) options trades: where the money is won and lost.
Prints DATA only (R14). Reads paper/trades.jsonl rows whose id contains -USER
and instrument starts with option_ and that have a realized_pnl.

Breakdowns: overall, by days-to-expiry, by size (premium at risk),
by hour of exit (ET), by the day's running P/L before the trade
(tilt/chasing), by underlying (SPY vs single names), by size relative to
the previous trade (sizing up after a loss).
"""
import json, re, collections
from datetime import datetime, timedelta
from pathlib import Path
from statistics import mean

LEDGER = Path(__file__).resolve().parents[1] / "trades.jsonl"

def load():
    out = []
    for line in open(LEDGER):
        if not line.strip():
            continue
        r = json.loads(line)
        if "USER" not in str(r.get("id", "")) or not str(r.get("instrument", "")).startswith("option"):
            continue
        if r.get("realized_pnl") is None or not r.get("closed"):
            continue
        note = r.get("r_note", "") or ""
        m = re.search(r"\((\d+)DTE\)", note)
        r["dte"] = int(m.group(1)) if m else None
        r["risk"] = float(r["entry"]) * float(r["qty"]) * 100
        t = datetime.fromisoformat(r["closed"].replace("Z", "+00:00")) - timedelta(hours=4)  # ET (EDT)
        r["et"] = t
        out.append(r)
    out.sort(key=lambda r: r["et"])
    return out

def stats(label, rs):
    if not rs:
        return
    p = [r["realized_pnl"] for r in rs]
    w = [x for x in p if x > 0]; l = [x for x in p if x < 0]
    print(f"  {label:<28} n={len(rs):>3}  net={sum(p):>+8.0f}  per_trade={mean(p):>+7.1f}  "
          f"win%={100*len(w)/len(p):>4.0f}  avgW={mean(w) if w else 0:>+6.0f}  avgL={mean(l) if l else 0:>+6.0f}")

def main():
    rs = load()
    print(f"owner option round trips: {len(rs)}  ({rs[0]['et']:%Y-%m-%d} .. {rs[-1]['et']:%Y-%m-%d})")
    stats("ALL", rs)

    print("\nBy days to expiry")
    for k in ["0", "1-3", "4+", "unknown"]:
        f = {"0": lambda d: d == 0, "1-3": lambda d: d is not None and 1 <= d <= 3,
             "4+": lambda d: d is not None and d >= 4, "unknown": lambda d: d is None}[k]
        stats(f"DTE {k}", [r for r in rs if f(r["dte"])])

    print("\nBy premium at risk (entry x qty x 100)")
    for lo, hi in [(0, 150), (150, 400), (400, 800), (800, 1e9)]:
        stats(f"${lo:.0f}-{'max' if hi > 1e8 else f'{hi:.0f}'}", [r for r in rs if lo <= r["risk"] < hi])

    print("\nBy exit hour (ET)")
    for h in range(9, 16):
        stats(f"{h}:00-{h}:59", [r for r in rs if r["et"].hour == h])

    print("\nBy the day's running P/L BEFORE the trade (tilt)")
    day_pnl = collections.defaultdict(float)
    tagged = []
    for r in rs:
        d = r["et"].date()
        before = day_pnl[d]
        tagged.append((before, r))
        day_pnl[d] += r["realized_pnl"]
    for lab, f in [("down > $200 on the day", lambda b: b < -200), ("down $1-200", lambda b: -200 <= b < 0),
                   ("flat (first trade)", lambda b: b == 0), ("up on the day", lambda b: b > 0)]:
        stats(lab, [r for b, r in tagged if f(b)])

    print("\nSizing up after a loss (risk > 1.5x previous trade's risk, previous trade lost)")
    up, other = [], []
    for prev, cur in zip(rs, rs[1:]):
        (up if prev["realized_pnl"] < 0 and cur["risk"] > 1.5 * prev["risk"] else other).append(cur)
    stats("sized up after loss", up)
    stats("everything else", other)

    print("\nBy underlying")
    stats("SPY", [r for r in rs if r["symbol"] == "SPY"])
    stats("single names", [r for r in rs if r["symbol"] != "SPY"])

    print("\nBy exit reason")
    for k in sorted({r.get("exit_reason") for r in rs}, key=str):
        stats(str(k), [r for r in rs if r.get("exit_reason") == k])

    print("\nPer day")
    for d in sorted(day_pnl):
        stats(str(d), [r for r in rs if r["et"].date() == d])

if __name__ == "__main__":
    main()
