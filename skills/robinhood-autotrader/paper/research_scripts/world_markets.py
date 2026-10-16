"""Do Asian and European markets move with / lead the US? (daily 2006-2026 + 2 years hourly)
Input: Yahoo chart JSON files (d_*.json daily, h_*.json hourly) in the folder passed as argv[1];
writes paper/history/world_daily.json (compact closes/opens) for reuse. SPY daily from daily_ohlcv.json."""
import json, sys, math, statistics as st, collections
from pathlib import Path
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
RAW = Path(sys.argv[1]); H = Path(__file__).resolve().parent.parent / "history"
TZ = {"dax": "Europe/Berlin", "ftse": "Europe/London", "stoxx": "Europe/Berlin", "nikkei": "Asia/Tokyo", "hsi": "Asia/Hong_Kong",
      "kospi": "Asia/Seoul", "asx": "Australia/Sydney", "shanghai": "Asia/Shanghai", "spx": "America/New_York", "vix": "America/New_York", "es": "America/New_York"}
def load(fn, tz):
    r = json.load(open(fn))["chart"]["result"][0]; q = r["indicators"]["quote"][0]; out = {}
    for i, ts in enumerate(r.get("timestamp") or []):
        o, c = q["open"][i], q["close"][i]
        if c is None or o is None: continue
        out[datetime.fromtimestamp(ts, ZoneInfo(tz)).strftime("%Y-%m-%d")] = (o, c)
    return out
D = {n: load(RAW / f"d_{n}.json", tz) for n, tz in TZ.items() if (RAW / f"d_{n}.json").exists()}
json.dump({n: {d: [round(o, 4), round(c, 4)] for d, (o, c) in v.items()} for n, v in D.items()}, open(H / "world_daily.json", "w"))
spy = json.load(open(H / "daily_ohlcv.json"))["SPY"]; SD = sorted(spy)
def ret(series, d, prev):  # close-to-close from prev date
    return series[d][1] / series[prev][1] - 1
def pdate(series, d):  # previous trading date in series before d
    ks = series["_k"]; import bisect; i = bisect.bisect_left(ks, d) - 1; return ks[i] if i >= 0 else None
for v in D.values(): v["_k"] = sorted(k for k in v if not k.startswith("_"))
def corr(x, y):
    mx, my = st.mean(x), st.mean(y); sx, sy = st.pstdev(x), st.pstdev(y)
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / len(x) / (sx * sy) if sx and sy else float("nan")
def tc(c, n): return c * math.sqrt((n - 2) / max(1e-12, 1 - c * c))
rows = []
for k in range(1, len(SD)):
    d, p = SD[k], SD[k - 1]
    o, h, l, c = spy[d][:4]; pc = spy[p][3]
    r = dict(d=d, gap=o / pc - 1, oc=c / o - 1, cc=c / pc - 1, prev_cc=(spy[p][3] / spy[SD[k - 2]][3] - 1) if k >= 2 else None)
    for n in ("nikkei", "hsi", "kospi", "asx", "shanghai", "dax", "ftse", "stoxx"):
        s = D.get(n)
        if s and d in s:
            pp = pdate(s, d)
            if pp: r[n] = ret(s, d, pp)
    rows.append(r)
ASIA = ["nikkei", "hsi", "kospi", "asx", "shanghai"]; EU = ["dax", "ftse", "stoxx"]
print(f"SPY days {len(rows)} ({rows[0]['d']}..{rows[-1]['d']})\n")
print("1) SAME-DAY CO-MOVEMENT (close-to-close, same calendar date). Europe closes 11:30 ET; Asia closes before the US opens.")
for n in ASIA + EU:
    sub = [r for r in rows if n in r]
    for lab, s2 in (("2006-15", [r for r in sub if r["d"] < "2016"]), ("2016-26", [r for r in sub if r["d"] >= "2016"])):
        pass
    c_all = corr([r[n] for r in sub], [r["cc"] for r in sub])
    c_old = corr([r[n] for r in sub if r["d"] < "2016"], [r["cc"] for r in sub if r["d"] < "2016"])
    c_new = corr([r[n] for r in sub if r["d"] >= "2016"], [r["cc"] for r in sub if r["d"] >= "2016"])
    print(f"   {n:9s} corr with SPY same day {c_all:+.2f}  (2006-15 {c_old:+.2f} | 2016-26 {c_new:+.2f})  n={len(sub)}")
print("\n2) WHO LEADS? US yesterday -> Asia today, vs Asia today -> US today")
for n in ASIA:
    sub = [r for r in rows if n in r and r["prev_cc"] is not None]
    a = corr([r["prev_cc"] for r in sub], [r[n] for r in sub])
    g = corr([r[n] for r in sub], [r["gap"] for r in sub]); oc = corr([r[n] for r in sub], [r["oc"] for r in sub])
    # Asia's own news: the part of Asia not explained by the US close before it
    x = [r["prev_cc"] for r in sub]; y = [r[n] for r in sub]; b = sum((xi - st.mean(x)) * (yi - st.mean(y)) for xi, yi in zip(x, y)) / sum((xi - st.mean(x)) ** 2 for xi in x)
    res = [yi - b * xi for xi, yi in zip(x, y)]
    gr = corr(res, [r["gap"] for r in sub]); ocr = corr(res, [r["oc"] for r in sub])
    print(f"   {n:9s} US yesterday->{n} {a:+.2f} | {n}->SPY gap {g:+.2f} | {n}->SPY open-to-close {oc:+.2f} (t {tc(oc, len(sub)):+.1f}) | {n}'s OWN news->gap {gr:+.2f}, ->open-to-close {ocr:+.2f} (t {tc(ocr, len(sub)):+.1f})")
print("\n3) BIG OVERNIGHT SHOCKS: Nikkei or DAX-overnight-proxy days")
for n in ("nikkei", "hsi"):
    for lab, cond in ((f"{n} down >2%", lambda v: v < -0.02), (f"{n} up >2%", lambda v: v > 0.02)):
        sub = [r for r in rows if n in r and cond(r[n])]
        if not sub: continue
        print(f"   {lab:16s} n={len(sub):4d}  SPY gap avg {100*st.mean(r['gap'] for r in sub):+.2f}%  then open-to-close avg {100*st.mean(r['oc'] for r in sub):+.2f}% ({100*sum(r['oc']>0 for r in sub)/len(sub):.0f}% up days)  vs all days {100*st.mean(r['oc'] for r in rows):+.3f}% / {100*sum(r['oc']>0 for r in rows)/len(rows):.0f}%")
print("\n4) CRISIS COUPLING: correlation of DAX and Nikkei with SPY when VIX >= 25 vs < 20")
vix = D["vix"]
for n in ("dax", "nikkei"):
    hi = [r for r in rows if n in r and r["d"] in vix and vix[r["d"]][1] >= 25]; lo = [r for r in rows if n in r and r["d"] in vix and vix[r["d"]][1] < 20]
    print(f"   {n:7s} calm (VIX<20) {corr([r[n] for r in lo], [r['cc'] for r in lo]):+.2f} (n={len(lo)}) | stressed (VIX>=25) {corr([r[n] for r in hi], [r['cc'] for r in hi]):+.2f} (n={len(hi)})")

print("\n5) INTRADAY (2 years hourly): Europe's morning before the US open, and after Europe closes")
def hourly(fn):
    r = json.load(open(RAW / fn))["chart"]["result"][0]; q = r["indicators"]["quote"][0]; out = []
    for i, ts in enumerate(r.get("timestamp") or []):
        if q["close"][i] is None: continue
        t = datetime.fromtimestamp(ts, ZoneInfo("America/New_York")); out.append((t, q["open"][i], q["close"][i]))
    return out
dax = hourly("h_dax.json"); es = hourly("h_es.json"); spyh = hourly("h_spy.json")
def by_day(bars): g = collections.defaultdict(list); [g[t.strftime("%Y-%m-%d")].append((t.hour * 60 + t.minute, o, c)) for t, o, c in bars]; return g
DX, ESD, SP = by_day(dax), by_day(es), by_day(spyh)
recs = []
for d in sorted(SP):
    if d not in DX or d not in spy: continue
    dx = sorted(DX[d]); pre = [b for b in dx if b[0] < 570]; post = [b for b in dx if 570 <= b[0] < 690]
    if not pre or not post: continue
    k = SD.index(d) if d in SD else None
    if not k: continue
    o, h, l, c = spy[d][:4]; pc = spy[SD[k - 1]][3]
    eu_am = pre[-1][2] / pre[0][1] - 1               # DAX from its open (~3:00 ET) to 9:30 ET
    eu_overlap = post[-1][2] / post[0][1] - 1        # DAX 9:30-11:30 ET
    sp = sorted(SP[d]); s_am = [b for b in sp if 570 <= b[0] < 690]; s_pm = [b for b in sp if b[0] >= 690]
    if not s_am or not s_pm: continue
    recs.append(dict(d=d, eu_am=eu_am, eu_ov=eu_overlap, gap=o / pc - 1, oc=c / o - 1, spy_am=s_am[-1][2] / s_am[0][1] - 1, spy_pm=s_pm[-1][2] / s_pm[0][1] - 1))
n = len(recs)
for lab, a, b in (("DAX morning (3:00-9:30 ET) -> SPY gap", "eu_am", "gap"), ("DAX morning -> SPY open-to-close", "eu_am", "oc"),
                  ("DAX 9:30-11:30 vs SPY 9:30-11:30 (same time)", "eu_ov", "spy_am"), ("SPY 9:30-11:30 -> SPY 11:30-close", "spy_am", "spy_pm"),
                  ("DAX 9:30-11:30 -> SPY 11:30-close (after Europe shuts)", "eu_ov", "spy_pm")):
    c = corr([r[a] for r in recs], [r[b] for r in recs]); print(f"   {lab:55s} corr {c:+.2f} (t {tc(c, n):+.1f}, n={n})")
sa = [abs(r["spy_am"]) for r in recs]; sp_ = [abs(r["spy_pm"]) for r in recs]
print(f"   SPY median |move| 9:30-11:30 {100*st.median(sa):.2f}% vs 11:30-16:00 {100*st.median(sp_):.2f}% (afternoon is 4.5 h long)")
