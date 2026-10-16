"""TARS market lab: how SPY actually moves. Tests a batch of indicators and market effects on real data,
in-sample (since 2026-09-02) vs out-of-sample (2026-02-23..09-01) for intraday, and 2006-2016 vs 2016-2026 for daily."""
import json, math, statistics as st, collections, bisect
from pathlib import Path
from zoneinfo import ZoneInfo
from datetime import datetime
H = Path(__file__).resolve().parent.parent / "history"
NY = ZoneInfo("America/New_York")
OOS_END = "2026-09-02"

def et(ts):
    d = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(NY); return d.strftime("%Y-%m-%d"), d.hour * 60 + d.minute
days = collections.defaultdict(list)
for day, bars in json.load(open(H / "intraday_vwap_sample.json"))["SPY"].items():
    for ts, o, h, l, c, v in bars:
        d, t = et(ts)
        if d < OOS_END and 570 <= t < 960: days[d].append(dict(t=t, o=o, h=h, l=l, c=c, v=v or 1))
m1 = json.load(open(H / "spy_1min.json"))
tmp = collections.defaultdict(list)
for k, (o, h, l, c, v) in sorted(m1.items()):
    d, t = et(k + ":00Z")
    if d >= OOS_END and 570 <= t < 960: tmp[d].append(dict(t=t, o=o, h=h, l=l, c=c, v=v or 1))
for d, bs in tmp.items():
    out = []
    for b in bs:
        key = (b["t"] - 570) // 5
        if out and out[-1]["k"] == key: x = out[-1]; x["h"] = max(x["h"], b["h"]); x["l"] = min(x["l"], b["l"]); x["c"] = b["c"]; x["v"] += b["v"]
        else: out.append(dict(b, k=key, t=570 + key * 5))
    days[d] = out
DAYS = sorted(d for d in days if len(days[d]) >= 60)
for d in DAYS: days[d].sort(key=lambda b: b["t"])


daily = json.load(open(H / "daily_ohlcv.json"))["SPY"]; DD = sorted(daily)

def prev_close(d):
    i = bisect.bisect_left(DD, d); return daily[DD[i - 1]][3] if 0 < i <= len(DD) and DD[i - 1] < d else None

def tstat(xs):
    xs = [x for x in xs if x == x]
    if len(xs) < 3 or st.stdev(xs) == 0: return float("nan")
    return st.mean(xs) / (st.stdev(xs) / math.sqrt(len(xs)))
OUT = {}
def report(name, samples, unit="pts"):
    """samples: {label: [one value per day/trade]} printed as mean, hit%, n, t"""
    print(f"\n{name}"); OUT[name] = {}
    for lab, xs in samples.items():
        if len(xs) < 5: print(f"  {lab:34s} n={len(xs)} (too few)"); continue
        r = dict(n=len(xs), mean=round(st.mean(xs), 4), hit=round(100 * sum(x > 0 for x in xs) / len(xs)), t=round(tstat(xs), 2))
        OUT[name][lab] = r; print(f"  {lab:34s} n={r['n']:5d} mean {r['mean']:+.4f} {unit}  >0 {r['hit']:3d}%  t {r['t']:+.2f}")

# ---------- DAILY, 20 years ----------
P = {}
for i, d in enumerate(DD[1:], 1):
    o, h, l, c, v = daily[d]; pc = daily[DD[i - 1]][3]
    P[d] = dict(on=math.log(o / pc) * 100, intra=math.log(c / o) * 100, gap=(o / pc - 1) * 100, o=o, h=h, l=l, c=c, pc=pc)
half = lambda d: "2006-15" if d < "2016" else "2016-26"
report("1. Where the return comes from: overnight vs day session (% per day)",
       {f"overnight {s}": [P[d]["on"] for d in P if half(d) == s] for s in ("2006-15", "2016-26")} |
       {f"day session {s}": [P[d]["intra"] for d in P if half(d) == s] for s in ("2006-15", "2016-26")}, "%")
def gapfill(lo, hi):
    out = {}
    for s in ("2006-15", "2016-26"):
        xs = [1.0 if (P[d]["l"] <= P[d]["pc"] if P[d]["gap"] > 0 else P[d]["h"] >= P[d]["pc"]) else 0.0
              for d in P if half(d) == s and lo <= abs(P[d]["gap"]) < hi]
        out[f"{lo}-{hi}% gaps {s} (fill=1)"] = [x - 0.5 for x in xs]
    return out
report("2. Gap fill: chance the gap closes the same day (shown as fill rate − 50%)", gapfill(0.1, 0.3) | gapfill(0.3, 0.6) | gapfill(0.6, 1.0) | gapfill(1.0, 9), "")
import datetime as dt
def tom(d):  # turn of month: last trading day + first 3 of next month
    i = DD.index(d); m = d[:7]
    nxt = DD[i + 1][:7] if i + 1 < len(DD) else m
    first = [x for x in DD if x[:7] == m][:3]
    return nxt != m or d in first
def third_fri(d):
    y, m, dd = map(int, d.split("-")); x = dt.date(y, m, dd)
    return x.weekday() == 4 and 15 <= dd <= 21
cc = {d: (P[d]["c"] / P[d]["pc"] - 1) * 100 for d in P}
report("3. Calendar effects (close-to-close %)",
       {f"turn of month {s}": [cc[d] for d in P if half(d) == s and tom(d)] for s in ("2006-15", "2016-26")} |
       {f"other days {s}": [cc[d] for d in P if half(d) == s and not tom(d)] for s in ("2006-15", "2016-26")} |
       {f"monthly opex Friday {s}": [cc[d] for d in P if half(d) == s and third_fri(d)] for s in ("2006-15", "2016-26")}, "%")
report("4. Opex-day range vs other Fridays (day range % minus Friday average)",
       (lambda fr: {f"opex Friday range {s}": [(P[d]["h"] - P[d]["l"]) / P[d]["o"] * 100 - st.mean((P[x]["h"] - P[x]["l"]) / P[x]["o"] * 100 for x in fr if half(x) == s) for d in fr if half(d) == s and third_fri(d)] for s in ("2006-15", "2016-26")})
       ([d for d in P if dt.date(*map(int, d.split("-"))).weekday() == 4]), "%")

# ---------- INTRADAY, 164 days of 5-min bars ----------
samp = lambda d: "IS" if d >= OOS_END else "OOS"
def at(bars, t):  # close of the bar ending at or before minute t
    xs = [b for b in bars if b["t"] + 5 <= t]; return xs[-1]["c"] if xs else None
im = collections.defaultdict(list); orb = collections.defaultdict(list); vr = collections.defaultdict(list)
clv = collections.defaultdict(list); sq = collections.defaultdict(list); pin = collections.defaultdict(list)
for d in DAYS:
    b = days[d]; s = samp(d); o = b[0]["o"]; c = b[-1]["c"]; pc = prev_close(d)
    p10, p1530 = at(b, 600), at(b, 930)
    # 5. intraday momentum (Gao-Han-Li-Zhou): first 30 min (incl. overnight) predicts the last 30 min
    if p10 and p1530 and pc:
        first = p10 - pc; last = c - p1530
        im[f"last30 signed by first30 {s}"].append(last * (1 if first > 0 else -1))
    # 6. opening range breakout (30 min): first close outside the OR after 10:00, hold to close
    orr = [x for x in b if x["t"] < 600]
    if orr:
        hi, lo = max(x["h"] for x in orr), min(x["l"] for x in orr)
        for x in b:
            if x["t"] >= 600 and x["t"] < 900 and (x["c"] > hi or x["c"] < lo):
                sd = 1 if x["c"] > hi else -1; orb[f"ORB30 hold to close {s}"].append(sd * (c - x["c"]) - 0.03); break
    # 7. regime: morning variance ratio predicts afternoon continuation?
    m = [x for x in b if x["t"] < 690]
    if len(m) >= 24:
        r5 = [math.log(m[i]["c"] / m[i - 1]["c"]) for i in range(1, len(m))]
        r30 = [math.log(m[i]["c"] / m[i - 6]["c"]) for i in range(6, len(m), 6)]
        if len(r30) >= 3 and st.pvariance(r5) > 0:
            v = st.pvariance(r30) / (6 * st.pvariance(r5)); mv = m[-1]["c"] - o; aft = c - m[-1]["c"]
            vr[f"afternoon in morning's direction, VR>1 (trendy) {s}" if v > 1 else f"afternoon in morning's direction, VR<=1 {s}"].append(aft * (1 if mv > 0 else -1))
    # 8. buying pressure (close location x volume, 6 bars) -> next 30 min
    for i in range(12, len(b) - 6):
        if not 630 <= b[i]["t"] <= 870: continue
        w = b[i - 5:i + 1]; vol = sum(x["v"] for x in w) or 1
        p = sum(((x["c"] - x["l"]) - (x["h"] - x["c"])) / ((x["h"] - x["l"]) or 1) * x["v"] for x in w) / vol
        if abs(p) > 0.5 and i % 6 == 0: clv[f"pressure |p|>0.5 next 30m {s}"].append((1 if p > 0 else -1) * (b[i + 6]["c"] - b[i]["c"]))
    # 9. squeeze (Bollinger inside Keltner) release -> direction of the release bar, next 30 min
    for i in range(21, len(b) - 6):
        def sqz(k):
            w = b[k - 19:k + 1]; mu = st.mean(x["c"] for x in w); sd = st.pstdev(x["c"] for x in w)
            atr = st.mean(x["h"] - x["l"] for x in w); return 2 * sd < 1.5 * atr, mu
        on_prev, _ = sqz(i - 1); on_now, mu = sqz(i)
        if on_prev and not on_now and 630 <= b[i]["t"] <= 870:
            sq[f"squeeze release next 30m {s}"].append((1 if b[i]["c"] > mu else -1) * (b[i + 6]["c"] - b[i]["c"]) - 0.03)
    # 10. opex pin: last-hour drift toward the nearest $5 strike (signed: + = toward)
    p15 = at(b, 900)
    if p15:
        k = round(p15 / 5) * 5; tw = (abs(p15 - k) - abs(c - k))
        y, mo, dd = map(int, d.split("-")); fri3 = dt.date(y, mo, dd).weekday() == 4 and 15 <= dd <= 21
        pin["opex Fridays: last hour toward $5 strike" if fri3 else "other days: last hour toward $5 strike"].append(tw)
report("5. Intraday momentum: last 30 min, signed by the first 30 min (incl. overnight gap)", im)
report("6. Opening-range breakout (30-min range), after costs", orb)
report("7. Regime: does the afternoon continue the morning? (split by morning variance ratio)", vr)
report("8. Buying/selling pressure (close location x volume) -> next 30 min", clv)
report("9. Bollinger-inside-Keltner squeeze release -> next 30 min, after costs", sq)
report("10. Pinning: last hour moves toward the nearest $5 strike? (pts closer)", pin)
json.dump(OUT, open(Path(__file__).with_name("market_lab.json"), "w"), indent=1)
