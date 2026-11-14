"""Rebuild of a "Godmode"-style SMC indicator (structure, liquidity sweeps, BOS/CHoCH, non-repainting)
and an honest test of it on real SPY 5-min bars. Same data as s2_context.py. Signals use only bars
already closed (pivots confirmed K bars late) so nothing repaints."""
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


def tstat(by):  # day-clustered t-stat
    dm = [st.mean(v) for v in by.values() if v]
    if len(dm) < 3 or st.stdev(dm) == 0: return float("nan")
    return st.mean(dm) / (st.stdev(dm) / math.sqrt(len(dm)))

def vwap(bars):
    pv = vv = 0
    for b in bars:
        tp = (b["h"] + b["l"] + b["c"]) / 3; pv += tp * b["v"]; vv += b["v"]; b["vw"] = pv / vv

K = 3  # pivot needs K bars each side; known only K bars later (non-repainting)
def signals(bars):
    """Yield (i, side, kind, stop) at the close of bar i, using only bars <= i."""
    sh = sl = None; prev_sh = prev_sl = None; trend = 0; sweep = None
    for i in range(len(bars)):
        j = i - K  # pivot candidate whose right side just completed
        if j >= K:
            w = bars[j - K:j + K + 1]
            if bars[j]["h"] == max(b["h"] for b in w): prev_sh, sh = sh, (j, bars[j]["h"])
            if bars[j]["l"] == min(b["l"] for b in w): prev_sl, sl = sl, (j, bars[j]["l"])
        b = bars[i]
        if i < 6 or b["t"] < 630 or b["t"] > 870: continue  # 10:30-14:30 like the slot
        # liquidity sweep: wick through the last swing, close back inside
        if sl and b["l"] < sl[1] and b["c"] > sl[1]:
            yield i, 1, "sweep", b["l"]; sweep = (1, i, b["l"])
        if sh and b["h"] > sh[1] and b["c"] < sh[1]:
            yield i, -1, "sweep", b["h"]; sweep = (-1, i, b["h"])
        # break of structure / change of character on a close
        if sh and b["c"] > sh[1] and bars[i - 1]["c"] <= sh[1]:
            kind = "choch" if trend <= 0 else "bos"; trend = 1
            yield i, 1, kind, sl[1] if sl else b["l"]
            if sweep and sweep[0] == 1 and i - sweep[1] <= 12: yield i, 1, "sweep+choch", sweep[2]
        if sl and b["c"] < sl[1] and bars[i - 1]["c"] >= sl[1]:
            kind = "choch" if trend >= 0 else "bos"; trend = -1
            yield i, -1, kind, sh[1] if sh else b["h"]
            if sweep and sweep[0] == -1 and i - sweep[1] <= 12: yield i, -1, "sweep+choch", sweep[2]

def outcome(bars, i, side, stop, rr=2.0, hold=12):
    e = bars[i]["c"]; risk = abs(e - stop)
    if risk < 0.05: risk = 0.05
    tgt = e + side * rr * risk; stp = e - side * risk
    for b in bars[i + 1:i + 1 + hold]:
        if (side == 1 and b["l"] <= stp) or (side == -1 and b["h"] >= stp): return -risk, "stop", risk
        if (side == 1 and b["h"] >= tgt) or (side == -1 and b["l"] <= tgt): return rr * risk, "target", risk
    last = bars[min(i + hold, len(bars) - 1)]["c"]
    return side * (last - e), "time", risk

COST = 0.03  # SPY pts round trip (spread + slippage on an ATM option, approx.)
res = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))
for d in DAYS:
    bars = days[d]; vwap(bars)
    for i, side, kind, stop in signals(bars):
        pts, how, risk = outcome(bars, i, side, stop)
        samp = "OOS" if d < OOS_END else "IS"
        tags = [kind, kind + (" long" if side == 1 else " short"),
                kind + (" with-vwap" if (bars[i]["c"] - bars[i]["vw"]) * side > 0 else " vs-vwap")]
        for tg in tags: res[tg][samp][d].append((pts - COST, how, pts / risk if risk else 0))

print(f"days IS={sum(d >= OOS_END for d in DAYS)} OOS={sum(d < OOS_END for d in DAYS)}  exits: stop at structure, 2R target, 60 min")
print(f"{'signal':28s} {'samp':4s} {'n':>4s} {'pts/tr':>7s} {'win%':>5s} {'tgt%':>5s} {'avgR':>6s} {'t':>5s}")
out = {}
for tg in sorted(res):
    for samp in ("IS", "OOS"):
        by = res[tg][samp]; xs = [x for v in by.values() for x in v]
        if len(xs) < 15: continue
        p = [x[0] for x in xs]
        row = dict(n=len(xs), pts=round(st.mean(p), 3), win=round(100 * sum(v > 0 for v in p) / len(p)),
                   tgt=round(100 * sum(x[1] == "target" for x in xs) / len(xs)), R=round(st.mean(x[2] for x in xs), 2),
                   t=round(tstat({d: [x[0] for x in v] for d, v in by.items()}), 1))
        out.setdefault(tg, {})[samp] = row
        print(f"{tg:28s} {samp:4s} {row['n']:4d} {row['pts']:7.3f} {row['win']:5d} {row['tgt']:5d} {row['R']:6.2f} {row['t']:5.1f}")
json.dump(out, open(Path(__file__).with_name("godmode_test.json"), "w"), indent=1)
