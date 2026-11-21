"""Nolan's own option round trips: when and how he makes / loses money (entry time, hold time, size, day).
Input: trips.json from owner_trips_build.py. Prints premium-point and % results; dollar totals stay in chat (R13)."""
import json, sys, collections, statistics as st
from datetime import datetime
from zoneinfo import ZoneInfo
NY = ZoneInfo("America/New_York")
T = json.load(open(sys.argv[1]))
for t in T:
    a = datetime.fromisoformat(t["t_in"].replace("Z", "+00:00")).astimezone(NY); b = datetime.fromisoformat(t["t_out"].replace("Z", "+00:00")).astimezone(NY)
    t["day"] = a.strftime("%Y-%m-%d"); t["hm"] = a.hour * 60 + a.minute; t["hold"] = (b - a).total_seconds() / 60
    t["usd"] = (t["p_out"] - t["p_in"]) * t["q"] * 100; t["pct"] = 100 * (t["p_out"] / t["p_in"] - 1) if t["p_in"] else 0
    t["dte0"] = t["exp"] == t["day"]
tot = sum(t["usd"] for t in T); gross_win = sum(t["usd"] for t in T if t["usd"] > 0)
def show(lab, g):
    if not g: return
    u = sum(x["usd"] for x in g); w = sum(x["usd"] > 0 for x in g)
    print(f"  {lab:28s} trips {len(g):3d}  win {100*w/len(g):3.0f}%  avg {st.mean(x['pct'] for x in g):+6.1f}% per trip  share of net {u:+9.0f}")
print(f"{len(T)} trips, {len(set(t['day'] for t in T))} days, net {tot:+.0f}\nBY ENTRY TIME (ET)")
for lo, hi, lab in ((570, 600, "09:30-10:00"), (600, 630, "10:00-10:30"), (630, 690, "10:30-11:30"), (690, 840, "11:30-14:00"), (840, 930, "14:00-15:30"), (930, 960, "15:30-16:00")):
    show(lab, [t for t in T if lo <= t["hm"] < hi])
print("BY HOLD TIME")
for lo, hi, lab in ((0, 2, "< 2 min"), (2, 5, "2-5 min"), (5, 15, "5-15 min"), (15, 60, "15-60 min"), (60, 999, "> 1 hour")):
    show(lab, [t for t in T if lo <= t["hold"] < hi])
print("BY SIZE (contracts in the lot)")
for lo, hi, lab in ((0, 1.5, "1"), (1.5, 3.5, "2-3"), (3.5, 6.5, "4-6"), (6.5, 99, "7+")):
    show(lab, [t for t in T if lo <= t["q"] < hi])
print("BY TYPE / EXPIRY")
show("calls", [t for t in T if t["typ"] == "call"]); show("puts", [t for t in T if t["typ"] == "put"])
show("0DTE", [t for t in T if t["dte0"]]); show("1+ DTE", [t for t in T if not t["dte0"]])
print("BY DAY")
for d in sorted(set(t["day"] for t in T)):
    g = [t for t in T if t["day"] == d]; show(d, g)
print("TRADE NUMBER WITHIN THE DAY")
byd = collections.defaultdict(list)
for t in sorted(T, key=lambda x: x["t_in"]): byd[t["day"]].append(t)
for lo, hi, lab in ((0, 3, "trips 1-3"), (3, 6, "trips 4-6"), (6, 10, "trips 7-10"), (10, 99, "trips 11+")):
    show(lab, [t for g in byd.values() for i, t in enumerate(g) if lo <= i < hi])
best = sorted(byd, key=lambda d: -sum(t["usd"] for t in byd[d]))
print(f"net without the best day ({best[0]}): {tot - sum(t['usd'] for t in byd[best[0]]):+.0f}")
w = [t["pct"] for t in T if t["usd"] > 0]; l = [t["pct"] for t in T if t["usd"] <= 0]
print(f"avg winner {st.mean(w):+.1f}%  avg loser {st.mean(l):+.1f}%  (median {st.median(w):+.1f}% / {st.median(l):+.1f}%)")
