"""Chart Analyst's engine: turns SPY bars into a structured, honest chart read.
Usage: python3 chart_read.py bars_today.json [prev_day.json] [daily.json]
Each file is the payload of Robinhood get_equity_historicals (data.results[0].bars), 1-min or 5-min bars today;
prev_day = yesterday's bars (any interval); daily = daily bars (for the 20-day average).
Prints JSON: trend (3 timeframes), structure, VWAP/sigma, momentum, volume, day type, key levels, the nearest
liquidity pools with first-touch odds (tested), and which TARS setups are live. Every read says if it is tested."""
import json, math, sys
from zoneinfo import ZoneInfo
from datetime import datetime
NY = ZoneInfo("America/New_York")
def load(p):
    d = json.load(open(p)); d = d.get("data", d); r = d["results"][0] if "results" in d else d
    out = []
    for b in r["bars"]:
        if b.get("interpolated"): continue
        t = datetime.fromisoformat(b["begins_at"].replace("Z", "+00:00")).astimezone(NY)
        out.append(dict(hm=t.strftime("%H:%M"), o=float(b["open_price"]), h=float(b["high_price"]), l=float(b["low_price"]), c=float(b["close_price"]), v=float(b.get("volume") or 1)))
    return [b for b in out if "09:30" <= b["hm"] < "16:00"] if out and ":" in out[0]["hm"] else out
def five(b1):
    out = []
    for b in b1:
        m = int(b["hm"][:2]) * 60 + int(b["hm"][3:]); k = (m - 570) // 5
        if out and out[-1]["k"] == k: x = out[-1]; x["h"] = max(x["h"], b["h"]); x["l"] = min(x["l"], b["l"]); x["c"] = b["c"]; x["v"] += b["v"]
        else: out.append(dict(b, k=k))
    return out
bars = load(sys.argv[1]); prev = load(sys.argv[2]) if len(sys.argv) > 2 else None
daily = load(sys.argv[3]) if len(sys.argv) > 3 else None
b5 = five(bars) if len(bars) > 1 and bars[1]["hm"][3:] != bars[0]["hm"][3:] and int(bars[1]["hm"][3:]) - int(bars[0]["hm"][3:]) == 1 else bars
pv = vv = pv2 = 0; e9 = e21 = g = l = None
for i, b in enumerate(b5):
    tp = (b["h"] + b["l"] + b["c"]) / 3; pv += tp * b["v"]; vv += b["v"]; pv2 += tp * tp * b["v"]
    b["vwap"] = pv / vv; b["sd"] = math.sqrt(max(0, pv2 / vv - b["vwap"] ** 2))
    e9 = b["c"] if e9 is None else e9 + 0.2 * (b["c"] - e9); e21 = b["c"] if e21 is None else e21 + 2 / 22 * (b["c"] - e21); b["e9"], b["e21"] = e9, e21
    if i:
        ch = b["c"] - b5[i - 1]["c"]; g = max(ch, 0) if g is None else (g * 13 + max(ch, 0)) / 14; l = max(-ch, 0) if l is None else (l * 13 + max(-ch, 0)) / 14
    b["rsi"] = 50 if not l else 100 - 100 / (1 + (g or 0) / l)
last = b5[-1]; px = last["c"]; open_ = b5[0]["o"]; hi = max(b["h"] for b in b5); lo = min(b["l"] for b in b5); rng = hi - lo or 1e-9
swH = [i for i in range(2, len(b5) - 2) if b5[i]["h"] == max(x["h"] for x in b5[i - 2:i + 3])]
swL = [i for i in range(2, len(b5) - 2) if b5[i]["l"] == min(x["l"] for x in b5[i - 2:i + 3])]
struct = "up (higher highs and higher lows)" if len(swH) > 1 and len(swL) > 1 and b5[swH[-1]]["h"] > b5[swH[-2]]["h"] and b5[swL[-1]]["l"] > b5[swL[-2]]["l"] else \
         "down (lower highs and lower lows)" if len(swH) > 1 and len(swL) > 1 and b5[swH[-1]]["h"] < b5[swH[-2]]["h"] and b5[swL[-1]]["l"] < b5[swL[-2]]["l"] else "mixed / range"
levels = {"day high": hi, "day low": lo, "open": open_, "VWAP": last["vwap"], "VWAP -2sd": last["vwap"] - 2 * last["sd"], "VWAP +2sd": last["vwap"] + 2 * last["sd"]}
if len(b5) >= 3: levels["opening-range high (15m)"] = max(x["h"] for x in b5[:3]); levels["opening-range low (15m)"] = min(x["l"] for x in b5[:3])
if prev: levels["yesterday high"] = max(x["h"] for x in prev); levels["yesterday low"] = min(x["l"] for x in prev); levels["yesterday close"] = prev[-1]["c"]
above = sorted((v, k) for k, v in levels.items() if v > px + 0.02); below = sorted(((v, k) for k, v in levels.items() if v < px - 0.02), reverse=True)
pool = None
if above and below:
    up, dn = above[0], below[0]; p_up = (px - dn[0]) / (up[0] - dn[0])
    pool = {"up": f"{up[1]} {up[0]:.2f}", "down": f"{dn[1]} {dn[0]:.2f}", "p_up_first": round(p_up, 2),
            "call": ("UP" if p_up >= 0.5 else "DOWN") + f" first, {round(100 * max(p_up, 1 - p_up))}%", "tested": "first-touch odds by distance; calibrated on the desk's pools (1,668 checks, called 70% -> 69%), these levels are a similar set"}
tn = abs(px - open_) / rng
day_type = ("trending " + ("down" if px < open_ else "up")) if tn >= 0.5 else "choppy" if tn <= 0.25 else "in between"
sma20 = sum(x["c"] for x in daily[-20:]) / 20 if daily and len(daily) >= 20 else None
pc = prev[-1]["c"] if prev else None
gap = 100 * (open_ / pc - 1) if pc else None
dip = any(x["c"] < x["vwap"] - 2 * x["sd"] or x["rsi"] < 30 for x in b5[-3:-1]); turn = len(b5) > 1 and last["c"] > b5[-2]["h"]
read = {
  "time": last["hm"], "price": round(px, 2),
  "trend": {"daily": None if sma20 is None or pc is None else ("up: prior close above 20-day average" if pc > sma20 else "down: prior close below 20-day average"),
            "intraday": f"{'below' if px < last['vwap'] else 'above'} VWAP {last['vwap']:.2f} ({(px - last['vwap']) / (last['sd'] or 1):+.1f} sd), EMA9 {'<' if last['e9'] < last['e21'] else '>='} EMA21",
            "structure_5m": struct},
  "momentum": {"rsi_5m": round(last["rsi"]), "note": "RSI alone: no tested edge"},
  "volume": f"last 5-min bar {last['v'] / (sum(x['v'] for x in b5[-21:-1]) / max(1, len(b5[-21:-1]))):.1f}x the recent average",
  "day_type": f"{day_type} (trend-ness {tn:.2f}); range {rng:.2f} pts",
  "gap": None if gap is None else f"{gap:+.2f}% (fill odds: <0.1% 88%, 0.1-0.3% 64-76%, 0.3-0.6% 31-58%, >0.6% 21-38%)",
  "levels_above": [f"{k} {v:.2f}" for v, k in above[:3]], "levels_below": [f"{k} {v:.2f}" for v, k in below[:3]],
  "next_pool": pool,
  "setups": {"S1 gap-and-go": "n/a" if gap is None else ("live" if gap >= 0.6 and px > open_ and px > last["vwap"] else "off"),
             "S2 dip + turn": "FIRED" if dip and turn else "armed (dip, waiting for a turn)" if dip else "off",
             "S2 warning (tested 2026-10-16)": "S2 with its real exits lost -0.11 pts/trade out of sample (95 trades, 39% wins); worst when EMA9 >= EMA21 at the signal (8% wins). Treat as paused unless Nolan says otherwise."},
  "honest_bottom_line": "Lines and patterns map the chart; tested direction edges are few. What holds: time of day, gap odds, expected move, pool first-touch odds.",
}
print(json.dumps(read, indent=1))
