#!/usr/bin/env python3
"""Reading Nolan over time (GROWTH backlog #1, 2026-10-24): patterns in his own option trades, not single moments.
Input: one or more get_option_orders JSON dumps (agent_initiated=false, state=filled). Builds FIFO round trips per
contract, then looks at sequences: what he does right after a loss, after two losses, before 10:30, how fast he
re-enters, and whether his first trade of the day sets the tone. Prints plain-language findings with counts.
No dollar balances are written anywhere (R13); per-trade P&L stays in memory and percentages are printed."""
import json, sys, datetime as dt, statistics as st
from collections import defaultdict

ET = dt.timezone(dt.timedelta(hours=-4))
fills = []
for path in sys.argv[1:]:
    for o in json.load(open(path))["data"]["orders"]:
        if o.get("agent_initiated") or o["state"] != "filled":
            continue
        for leg in o["legs"]:
            for ex in leg.get("executions", []):
                fills.append(dict(t=dt.datetime.fromisoformat(ex["timestamp"].replace("Z", "+00:00")).astimezone(ET),
                                  opt=leg["option_id"], side=leg["side"], eff=leg["position_effect"], kind=leg["option_type"],
                                  qty=float(ex["quantity"]), px=float(ex["price"]) * 100))
fills.sort(key=lambda f: f["t"])
lots, trips = defaultdict(list), []
for f in fills:
    if f["eff"] == "open":
        lots[f["opt"]].append([f["t"], f["qty"], f["px"], f["kind"]])
    else:
        q = f["qty"]
        while q > 1e-9 and lots[f["opt"]]:
            lot = lots[f["opt"]][0]; take = min(q, lot[1])
            trips.append(dict(entry=lot[0], exit=f["t"], kind=lot[3], cost=take * lot[2], pnl=take * (f["px"] - lot[2])))
            lot[1] -= take; q -= take
            if lot[1] <= 1e-9: lots[f["opt"]].pop(0)
# merge partial closes of the same entry into one trade
merged = {}
for t in trips:
    k = (t["entry"], t["kind"])
    m = merged.setdefault(k, dict(entry=t["entry"], exit=t["exit"], kind=t["kind"], cost=0, pnl=0))
    m["cost"] += t["cost"]; m["pnl"] += t["pnl"]; m["exit"] = max(m["exit"], t["exit"])
T = sorted(merged.values(), key=lambda t: t["entry"])
for t in T:
    t["ret"] = t["pnl"] / t["cost"] if t["cost"] else 0
    t["win"] = t["pnl"] > 0
    t["early"] = t["entry"].hour * 60 + t["entry"].minute < 10 * 60 + 30
    t["hold_m"] = (t["exit"] - t["entry"]).total_seconds() / 60
n = len(T)
if n < 10:
    sys.exit(f"only {n} round trips; need more history")
def rate(xs): return f"{100 * sum(x['win'] for x in xs) / len(xs):.0f}% wins, avg {100 * st.mean(x['ret'] for x in xs):+.1f}% per trade (n {len(xs)})" if xs else "n 0"
days = defaultdict(list)
for t in T: days[t["entry"].date()].append(t)
print(f"{n} round trips over {len(days)} days ({T[0]['entry']:%m/%d}-{T[-1]['entry']:%m/%d}); overall {rate(T)}")
print(f"- Before 10:30: {rate([t for t in T if t['early']])} | after: {rate([t for t in T if not t['early']])}")
after_loss = [b for a, b in zip(T, T[1:]) if not a["win"] and a["entry"].date() == b["entry"].date()]
after_win = [b for a, b in zip(T, T[1:]) if a["win"] and a["entry"].date() == b["entry"].date()]
print(f"- Next trade after a loss (same day): {rate(after_loss)} | after a win: {rate(after_win)}")
gaps_l = [(b["entry"] - a["exit"]).total_seconds() / 60 for a, b in zip(T, T[1:]) if not a["win"] and a["entry"].date() == b["entry"].date()]
gaps_w = [(b["entry"] - a["exit"]).total_seconds() / 60 for a, b in zip(T, T[1:]) if a["win"] and a["entry"].date() == b["entry"].date()]
if gaps_l and gaps_w:
    print(f"- Minutes to the next entry: after a loss median {st.median(gaps_l):.1f}, after a win {st.median(gaps_w):.1f}")
fast = [b for a, b in zip(T, T[1:]) if not a["win"] and a["entry"].date() == b["entry"].date() and (b["entry"] - a["exit"]).total_seconds() < 300]
print(f"- Re-entered within 5 min of a loss: {rate(fast)}")
flip = [b for a, b in zip(T, T[1:]) if not a["win"] and a["kind"] != b["kind"] and a["entry"].date() == b["entry"].date() and (b["entry"] - a["exit"]).total_seconds() < 600]
print(f"- Flipped call<->put within 10 min of a loss: {rate(flip)}")
two = [c for a, b, c in zip(T, T[1:], T[2:]) if not a["win"] and not b["win"] and a["entry"].date() == c["entry"].date()]
print(f"- After two losses in a row (same day): {rate(two)}")
first_win = [d for d, ts in days.items() if ts[0]["win"]]; first_loss = [d for d, ts in days.items() if not ts[0]["win"]]
rest = lambda ds: [t for d in ds for t in days[d][1:]]
print(f"- Rest of day when the first trade WON: {rate(rest(first_win))} | when it LOST: {rate(rest(first_loss))}")
by_count = sorted(days.items(), key=lambda kv: len(kv[1]))
busy = [t for d, ts in days.items() if len(ts) >= 8 for t in ts]; calm = [t for d, ts in days.items() if len(ts) < 8 for t in ts]
print(f"- Busy days (8+ trades): {rate(busy)} | calmer days: {rate(calm)}")
for lab, lo, hi in (("under 5 min", 0, 5), ("5-20 min", 5, 20), ("20+ min", 20, 1e9)):
    print(f"- Held {lab}: {rate([t for t in T if lo <= t['hold_m'] < hi])}")
