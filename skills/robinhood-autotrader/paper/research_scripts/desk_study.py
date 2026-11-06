"""TARS self-study: does each SPY Live Desk indicator / pattern predict the next 15-30 minutes?
Same definitions as live_desk.html. Real SPY 1-min bars only (paper/history/spy_1min.json).
Each event -> forward move in the hypothesised direction (points, close to close).
Stats are clustered by day (mean of day-means, t over days) and split into first/second half of days."""
import json, math, statistics as stt, collections, sys
from pathlib import Path
here = Path(__file__).resolve().parent.parent
raw = json.load(open(here / "history/spy_1min.json"))

def et_hm(k):  # keys are UTC 'YYYY-MM-DDTHH:MM'; Sep-Oct 2026 is EDT (UTC-4) until Nov 1
    h, m = int(k[11:13]) - 4, int(k[14:16]); return h * 60 + m
days = collections.defaultdict(list)
for k, v in sorted(raw.items()):
    t = et_hm(k)
    if 570 <= t < 960: days[k[:10]].append(dict(t=t, o=v[0], h=v[1], l=v[2], c=v[3], v=v[4] or 1))
DAYS = sorted(days)

def agg(bars, m):
    if m == 1: return [dict(b) for b in bars]
    out = []
    for b in bars:
        key = (b["t"] - 570) // m
        if out and out[-1]["key"] == key:
            o = out[-1]; o["h"] = max(o["h"], b["h"]); o["l"] = min(o["l"], b["l"]); o["c"] = b["c"]; o["v"] += b["v"]; o["t_end"] = b["t"]
        else: out.append(dict(b, key=key, t=570 + key * m, t_end=b["t"]))
    return out

def indicators(bars):
    pv = vv = pv2 = 0; e9 = e21 = g = l = atr = None
    for i, b in enumerate(bars):
        tp = (b["h"] + b["l"] + b["c"]) / 3; pv += tp * b["v"]; vv += b["v"]; pv2 += tp * tp * b["v"]
        b["vwap"] = pv / vv; b["sd"] = math.sqrt(max(0, pv2 / vv - b["vwap"] ** 2))
        e9 = b["c"] if e9 is None else e9 + 0.2 * (b["c"] - e9); e21 = b["c"] if e21 is None else e21 + 2 / 22 * (b["c"] - e21)
        b["e9"], b["e21"] = e9, e21
        tr = b["h"] - b["l"]
        if i:
            p = bars[i - 1]; ch = b["c"] - p["c"]
            g = max(ch, 0) if g is None else (g * 13 + max(ch, 0)) / 14
            l = max(-ch, 0) if l is None else (l * 13 + max(-ch, 0)) / 14
            tr = max(tr, abs(b["h"] - p["c"]), abs(b["l"] - p["c"]))
        atr = tr if atr is None else (atr * 13 + tr) / 14
        b["atr"] = atr; b["rsi"] = 50 if not l else 100 - 100 / (1 + (g or 0) / l)
        b["trend"] = 1 if b["c"] > b["vwap"] and e9 > e21 else -1 if b["c"] < b["vwap"] and e9 < e21 else 0

EV = collections.defaultdict(list)  # name -> [(day, signed fwd15, signed fwd30)]
def fwd(bars, i, side, H):  # bars are 1-min; side +1/-1
    j = min(len(bars) - 1, i + H)
    return None if j <= i else side * (bars[j]["c"] - bars[i]["c"])
def add(name, day, b1, i1, side):
    f15, f30 = fwd(b1, i1, side, 15), fwd(b1, i1, side, 30)
    if f15 is not None and i1 + 15 < len(b1): EV[name].append((day, f15, f30 if i1 + 30 < len(b1) else None))

def idx1(b1, t):  # 1-min index of the last minute in a bar ending at minute t
    for i in range(len(b1) - 1, -1, -1):
        if b1[i]["t"] <= t: return i
    return 0

prev = None
for day in DAYS:
    b1 = days[day]; indicators(b1)
    if len(b1) < 60: prev = b1; continue
    # baseline: every bar, long
    for i in range(0, len(b1), 5): add("baseline: any minute, long", day, b1, i, 1)
    for m in (1, 5, 15):
        bm = agg(b1, m); indicators(bm)
        for k in range(22, len(bm)):
            b, a = bm[k], bm[k - 1]; i1 = idx1(b1, b.get("t_end", b["t"]))
            if b1[i1]["t"] > 930: continue
            # VWAP sigma stretch -> fade
            z = (b["c"] - b["vwap"]) / (b["sd"] or 1); za = (a["c"] - a["vwap"]) / (a["sd"] or 1)
            if z >= 2 and za < 2: add(f"{m}m price crosses +2σ VWAP band → fade (short)", day, b1, i1, -1)
            if z <= -2 and za > -2: add(f"{m}m price crosses −2σ VWAP band → fade (long)", day, b1, i1, 1)
            # RSI extremes -> fade
            if b["rsi"] >= 70 and a["rsi"] < 70: add(f"{m}m RSI crosses above 70 → fade (short)", day, b1, i1, -1)
            if b["rsi"] <= 30 and a["rsi"] > 30: add(f"{m}m RSI crosses below 30 → fade (long)", day, b1, i1, 1)
            # EMA 9/21 cross -> follow
            if (b["e9"] > b["e21"]) != (a["e9"] > a["e21"]):
                add(f"{m}m EMA 9/21 cross → follow", day, b1, i1, 1 if b["e9"] > b["e21"] else -1)
            # VWAP cross -> follow
            if (b["c"] > b["vwap"]) != (a["c"] > a["vwap"]):
                add(f"{m}m close crosses VWAP → follow", day, b1, i1, 1 if b["c"] > b["vwap"] else -1)
            # trend state start
            if b["trend"] != 0 and a["trend"] != b["trend"]: add(f"{m}m trend state turns on (VWAP+EMA agree) → follow", day, b1, i1, b["trend"])
            # FVG formed -> follow gap direction ; retest of gap -> bounce
            if k >= 2:
                c0 = bm[k - 2]
                if b["l"] - c0["h"] >= b["c"] * 0.0004: add(f"{m}m bullish FVG forms → follow", day, b1, i1, 1)
                if c0["l"] - b["h"] >= b["c"] * 0.0004: add(f"{m}m bearish FVG forms → follow", day, b1, i1, -1)
        # FVG retest bounce (first touch of unfilled gap edge)
        gaps = []
        for k in range(2, len(bm)):
            b, c0 = bm[k], bm[k - 2]; i1 = idx1(b1, b.get("t_end", b["t"]))
            for gp in gaps:
                if gp["done"]: continue
                if gp["side"] == 1 and b["l"] <= gp["top"]:
                    gp["done"] = True
                    if b1[i1]["t"] <= 930: add(f"{m}m first retest of bullish FVG → bounce (long)", day, b1, i1, 1)
                    EV[f"{m}m bull FVG: wick fully through gap on the retest bar"].append((day, 1.0 if b["l"] < gp["bot"] else 0.0, None))
                if gp["side"] == -1 and b["h"] >= gp["bot"]:
                    gp["done"] = True
                    if b1[i1]["t"] <= 930: add(f"{m}m first retest of bearish FVG → bounce (short)", day, b1, i1, -1)
                    EV[f"{m}m bear FVG: wick fully through gap on the retest bar"].append((day, 1.0 if b["h"] > gp["top"] else 0.0, None))
            if b["l"] - c0["h"] >= b["c"] * 0.0004: gaps.append(dict(side=1, top=b["l"], bot=c0["h"], done=False))
            if c0["l"] - b["h"] >= b["c"] * 0.0004: gaps.append(dict(side=-1, top=c0["l"], bot=b["h"], done=False))
    # key levels on 1-min
    lv = {}
    if prev: lv["PDH"] = max(b["h"] for b in prev); lv["PDL"] = min(b["l"] for b in prev)
    lv["ORH"] = max(b["h"] for b in b1[:15]); lv["ORL"] = min(b["l"] for b in b1[:15])
    tol = 0.0003 * b1[0]["c"]
    for name, p in lv.items():
        hi = name.endswith("H"); start = 15 if name.startswith("OR") else 0
        for i in range(start, len(b1)):
            b = b1[i]
            if b["t"] > 930: break
            if hi and b["h"] > p + tol:
                if b["c"] < p: add(f"{name} swept & closed back inside → reverse (short)", day, b1, i, -1)
                else: add(f"{name} broken (close above) → follow (long)", day, b1, i, 1)
                break
            if not hi and b["l"] < p - tol:
                if b["c"] > p: add(f"{name} swept & closed back inside → reverse (long)", day, b1, i, 1)
                else: add(f"{name} broken (close below) → follow (short)", day, b1, i, -1)
                break
    # equal highs/lows pools (swing clusters) -> sweep vs break
    sh = [j for j in range(2, len(b1) - 2) if b1[j]["h"] == max(x["h"] for x in b1[j - 2:j + 3])]
    sl = [j for j in range(2, len(b1) - 2) if b1[j]["l"] == min(x["l"] for x in b1[j - 2:j + 3])]
    for idx, key, hi in ((sh, "h", True), (sl, "l", False)):
        used = set()
        for a in idx:
            if a in used: continue
            # only swings known by now: cluster with earlier swings within tolerance
            grp = [j for j in idx if j <= a and j not in used and abs(b1[j][key] - b1[a][key]) <= max(tol, 0.25 * b1[a]["atr"])]
            if len(grp) < 2: continue
            used.update(grp); p = sum(b1[j][key] for j in grp) / len(grp)
            for i in range(a + 3, len(b1)):  # swing confirmed 2 bars after a
                b = b1[i]
                if b["t"] > 930: break
                if hi and b["h"] > p + tol:
                    add("Equal highs swept & closed back inside → reverse (short)" if b["c"] < p else "Equal highs broken (close above) → follow (long)", day, b1, i, -1 if b["c"] < p else 1); break
                if not hi and b["l"] < p - tol:
                    add("Equal lows swept & closed back inside → reverse (long)" if b["c"] > p else "Equal lows broken (close below) → follow (short)", day, b1, i, 1 if b["c"] > p else -1); break
    # Fibonacci of the swing so far (from 10:30): first touch of 50/61.8 vs a control level 40% -> bounce?
    for i in range(60, len(b1)):
        if b1[i]["t"] > 930: break
    def fib_touch(level_f, label):
        hiI = loI = 0
        for i in range(60, len(b1)):
            b = b1[i]
            if b["t"] > 930: break
            seg = b1[:i]
            hiI = max(range(i), key=lambda j: b1[j]["h"]); loI = min(range(i), key=lambda j: b1[j]["l"])
            H, L = b1[hiI]["h"], b1[loI]["l"]
            if H - L < 0.002 * b["c"]: continue
            up = loI < hiI; p = H - level_f * (H - L) if up else L + level_f * (H - L)
            if (up and b["l"] <= p < b1[i - 1]["l"]) or (not up and b["h"] >= p > b1[i - 1]["h"]):
                add(label, day, b1, i, 1 if up else -1); return
    fib_touch(0.618, "Fib 61.8% first touch → bounce with the swing")
    fib_touch(0.5, "Fib 50% first touch → bounce with the swing")
    fib_touch(0.45, "CONTROL: random 45% level first touch → bounce")
    fib_touch(0.7, "CONTROL: random 70% level first touch → bounce")
    prev = b1

def stats(rows, col):
    by = collections.defaultdict(list)
    for r in rows:
        if r[col] is not None: by[r[0]].append(r[col])
    if not by: return None
    dm = [stt.mean(v) for v in by.values()]; allv = [x for v in by.values() for x in v]
    t = stt.mean(dm) / (stt.stdev(dm) / math.sqrt(len(dm))) if len(dm) > 2 and stt.stdev(dm) > 0 else float("nan")
    half = sorted(by); a, b = half[:len(half) // 2], half[len(half) // 2:]
    m1 = stt.mean([x for d in a for x in by[d]]) if a else float("nan"); m2 = stt.mean([x for d in b for x in by[d]]) if b else float("nan")
    return dict(n=len(allv), days=len(dm), mean=stt.mean(allv), hit=100 * sum(x > 0 for x in allv) / len(allv), t=t, h1=m1, h2=m2)

out = {}
for name in sorted(EV):
    s15, s30 = stats(EV[name], 1), stats(EV[name], 2)
    out[name] = {"15m": s15, "30m": s30}
json.dump(out, open(here / "datafarm/desk_study.json", "w"), indent=1)
print(f"{len(DAYS)} days {DAYS[0]}..{DAYS[-1]}\n")
print(f"{'event':72s} {'n':>4s} {'d':>3s} | {'15m pts':>7s} {'hit':>4s} {'t':>5s} | {'30m pts':>7s} {'hit':>4s} {'t':>5s} | {'H1':>6s} {'H2':>6s}")
for name, s in out.items():
    a, b = s["15m"], s["30m"]
    if "wick" in name: print(f"{name:72s} {a['n']:4d} {a['days']:3d} | rate {a['mean']*100:.0f}%"); continue
    f = lambda x: "   n/a" if x is None else f"{x['mean']:+7.3f} {x['hit']:4.0f} {x['t']:+5.1f}"
    print(f"{name:72s} {a['n']:4d} {a['days']:3d} | {f(a)} | {f(b)} | {b['h1'] if b else float('nan'):+6.3f} {b['h2'] if b else float('nan'):+6.3f}")
