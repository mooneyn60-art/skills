"""TARS deep dig: out-of-sample check of the desk candidates, gaps, VIX expected move, news days.
Intraday: real SPY 5-min bars 2026-02-23..2026-09-01 (intraday_vwap_sample.json) = OUT-OF-SAMPLE for the
2026-10-15 desk study; plus 1-min bars from 2026-09-02 aggregated to 5-min (in-sample period).
Daily: SPY 2006-2026 (daily_ohlcv.json) + weekly VIX (vix_weekly.json)."""
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
vixw = json.load(open(H / "vix_weekly.json")); VW = sorted(vixw)
def vix_on(d):
    i = bisect.bisect_right(VW, d) - 1; return vixw[VW[i]] if i >= 0 else None

def ind(bars):
    pv = vv = pv2 = 0; g = l = None
    for i, b in enumerate(bars):
        tp = (b["h"] + b["l"] + b["c"]) / 3; pv += tp * b["v"]; vv += b["v"]; pv2 += tp * tp * b["v"]
        b["vwap"] = pv / vv; b["sd"] = math.sqrt(max(0, pv2 / vv - b["vwap"] ** 2))
        if i:
            ch = b["c"] - bars[i - 1]["c"]
            g = max(ch, 0) if g is None else (g * 13 + max(ch, 0)) / 14; l = max(-ch, 0) if l is None else (l * 13 + max(-ch, 0)) / 14
        b["rsi"] = 50 if not l else 100 - 100 / (1 + (g or 0) / l)


def tstat(by):  # by: day -> list of values; clustered by day
    dm = [st.mean(v) for v in by.values() if v]
    if len(dm) < 3 or st.stdev(dm) == 0: return float("nan")
    return st.mean(dm) / (st.stdev(dm) / math.sqrt(len(dm)))

# ---- S2 as traded, with its real exits, split by the intraday context at the signal ----
sma = {}
for i, d in enumerate(DD):
    if i >= 20: sma[d] = st.mean(daily[x][3] for x in DD[i - 20:i])  # 20-day average of closes before d
def prev_close(d):
    i = bisect.bisect_left(DD, d); return daily[DD[i - 1]][3] if i > 0 else None
rows = []
for d in DAYS:
    b = days[d]; ind(b)
    e9 = e21 = None
    for x in b:
        e9 = x["c"] if e9 is None else e9 + 0.2 * (x["c"] - e9); e21 = x["c"] if e21 is None else e21 + (2 / 22) * (x["c"] - e21); x["e9"], x["e21"] = e9, e21
    pc = prev_close(d); up = d in sma and pc is not None and pc > sma[d]
    i = 2; open_ = b[0]["o"]
    while i < len(b):
        t = b[i]["t"]
        if not (630 <= t + 5 <= 870): i += 1; continue  # signal bar closes inside 10:30-14:30
        dip = [k for k in (i - 1, i - 2) if k >= 0 and (b[k]["c"] < b[k]["vwap"] - 2 * b[k]["sd"] or b[k]["rsi"] < 30)]
        if dip and b[i]["c"] > b[i - 1]["h"]:
            low = min(x["l"] for x in b[max(0, i - 3):i + 1]); entry = b[i]["c"]; res = None
            for j in range(i + 1, min(len(b), i + 13)):
                if b[j]["l"] < low: res = low - entry; break
                if b[j]["h"] >= b[j]["vwap"]: res = b[j]["vwap"] - entry; break
            if res is None: j = min(len(b) - 1, i + 12); res = b[j]["c"] - entry
            rng = max(x["h"] for x in b[:i + 1]) - min(x["l"] for x in b[:i + 1])
            tn = abs(entry - open_) / rng if rng else 0
            h30 = b[min(len(b) - 1, i + 6)]['c'] - entry; stop_only = None
            for j2 in range(i + 1, min(len(b), i + 13)):
                if b[j2]['l'] < low: stop_only = low - entry; break
            if stop_only is None: stop_only = b[min(len(b) - 1, i + 12)]['c'] - entry
            rows.append(dict(d=d, t=t, up=up, res=res, h30=h30, stop_only=stop_only, below_open=entry < open_, ema_down=b[i]["e9"] < b[i]["e21"],
                             down_day=(entry < open_ and tn >= 0.5), lower_hi=max(x["h"] for x in b[i - 3:i]) < max(x["h"] for x in b[max(0, i - 9):i - 3] or [0]),
                             early=t < 690))
            i = j + 1; continue
        i += 1
def show(lab, sub):
    for per, s in (("OOS Feb-Aug", [r for r in sub if r["d"] < OOS_END]), ("in-sample Sep-Oct", [r for r in sub if r["d"] >= OOS_END])):
        if not s: print(f"  {lab:44s} {per:18s} n=0"); continue
        by = collections.defaultdict(list); [by[r['d']].append(r['res']) for r in s]
        v = [r["res"] for r in s]
        print(f"  {lab:44s} {per:18s} n={len(v):3d} mean {st.mean(v):+.3f} pts  win {100*sum(x>0 for x in v)/len(v):3.0f}%  t {tstat(by):+.1f}")
print("S2 (dip + turn, 10:30-14:30), exits: VWAP / new low / 60 min. SPY points per trade.")
base = [r for r in rows if r["up"]]
show("S2 as traded (daily uptrend)", base)
show("  ...on a DOWN day so far (below open, trend>=0.5)", [r for r in base if r["down_day"]])
show("  ...NOT a down day", [r for r in base if not r["down_day"]])
show("  ...5-min EMA9 < EMA21 at signal", [r for r in base if r["ema_down"]])
show("  ...5-min EMA9 >= EMA21", [r for r in base if not r["ema_down"]])
show("  ...lower highs into the dip", [r for r in base if r["lower_hi"]])
show("  ...no lower highs", [r for r in base if not r["lower_hi"]])
show("S2 without the daily uptrend filter", rows)

print("\nSame S2 signals (daily uptrend), other exits:")
for key, lab in (("h30", "hold 30 min, no stop"), ("stop_only", "new-low stop, else hold 60 min (no VWAP take)")):
    for per, sub in (("OOS Feb-Aug", [r for r in base if r["d"] < OOS_END]), ("in-sample Sep-Oct", [r for r in base if r["d"] >= OOS_END])):
        by = collections.defaultdict(list); [by[r['d']].append(r[key]) for r in sub]; v = [r[key] for r in sub]
        print(f"  {lab:44s} {per:18s} n={len(v):3d} mean {st.mean(v):+.3f} pts  win {100*sum(x>0 for x in v)/len(v):3.0f}%  t {tstat(by):+.1f}")
