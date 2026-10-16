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
def report(title, ev):  # ev: list of (day, fwd30 signed)
    for lab, sub in (("OUT-OF-SAMPLE Feb23-Sep1", [e for e in ev if e[0] < OOS_END]), ("in-sample Sep2-Oct15", [e for e in ev if e[0] >= OOS_END])):
        by = collections.defaultdict(list); [by[d].append(x) for d, x in sub]
        v = [x for _, x in sub]
        if not v: print(f"  {title:52s} {lab:26s} n=0"); continue
        print(f"  {title:52s} {lab:26s} n={len(v):3d} days={len(by):3d} mean {st.mean(v):+.3f} pts  hit {100*sum(x>0 for x in v)/len(v):3.0f}%  t {tstat(by):+.1f}")

print(f"Intraday days: {len(DAYS)} ({sum(d < OOS_END for d in DAYS)} out-of-sample)\n")
print("A. CANDIDATES FROM THE DESK STUDY, RE-TESTED (5-min bars, 30-min forward, 09:45-15:30)")
EV = collections.defaultdict(list)
prev = None
for d in DAYS:
    b = days[d]; ind(b)
    f30 = lambda i, s: s * (b[min(len(b) - 1, i + 6)]["c"] - b[i]["c"]) if i + 6 < len(b) else None
    def add(name, i, s):
        x = f30(i, s)
        if x is not None and 585 <= b[i]["t"] <= 930: EV[name].append((d, x))
    for i in range(15, len(b)):
        if b[i]["rsi"] <= 30 < b[i - 1]["rsi"]: add("5m RSI14 crosses below 30 -> long", i, 1)
        if b[i]["rsi"] >= 70 > b[i - 1]["rsi"]: add("5m RSI14 crosses above 70 -> short", i, -1)
        z, za = (b[i]["c"] - b[i]["vwap"]) / (b[i]["sd"] or 1), (b[i - 1]["c"] - b[i - 1]["vwap"]) / (b[i - 1]["sd"] or 1)
        if z <= -2 < za: add("5m close below -2 sigma VWAP -> long", i, 1)
        if z >= 2 > za: add("5m close above +2 sigma VWAP -> short", i, -1)
    if prev:
        PDH, PDL = max(x["h"] for x in prev), min(x["l"] for x in prev)
        tol = 0.0003 * b[0]["c"]
        for name, p, hi in (("PDL", PDL, False), ("PDH", PDH, True)):
            for i in range(3, len(b)):
                x = b[i]
                if hi and x["h"] > p + tol: add(f"{name} " + ("swept+reclaimed -> short" if x["c"] < p else "broken -> long"), i, -1 if x["c"] < p else 1); break
                if not hi and x["l"] < p - tol: add(f"{name} " + ("swept+reclaimed -> long" if x["c"] > p else "broken -> short"), i, 1 if x["c"] > p else -1); break
    ORH, ORL = max(x["h"] for x in b[:3]), min(x["l"] for x in b[:3])
    for name, p, hi in (("ORH", ORH, True), ("ORL", ORL, False)):
        for i in range(3, len(b)):
            x = b[i]
            if hi and x["c"] > p: add("15-min OR high broken -> long", i, 1); break
            if not hi and x["c"] < p: add("15-min OR low broken -> short", i, -1); break
    # equal lows / highs (5-bar swings) swept and reclaimed
    sw = [j for j in range(2, len(b) - 2) if b[j]["l"] == min(y["l"] for y in b[j - 2:j + 3])]
    swh = [j for j in range(2, len(b) - 2) if b[j]["h"] == max(y["h"] for y in b[j - 2:j + 3])]
    for idx, key, hi in ((sw, "l", False), (swh, "h", True)):
        done = set()
        for a in idx:
            grp = [j for j in idx if j < a and j not in done and abs(b[j][key] - b[a][key]) <= 0.0005 * b[a]["c"]]
            if not grp: continue
            done.update(grp + [a]); p = (sum(b[j][key] for j in grp) + b[a][key]) / (len(grp) + 1)
            for i in range(a + 3, len(b)):
                x = b[i]
                if not hi and x["l"] < p - 0.0002 * p:
                    add("equal lows swept+reclaimed -> long" if x["c"] > p else "equal lows broken -> short", i, 1 if x["c"] > p else -1); break
                if hi and x["h"] > p + 0.0002 * p:
                    add("equal highs swept+reclaimed -> short" if x["c"] < p else "equal highs broken -> long", i, -1 if x["c"] < p else 1); break
    prev = b
for k in sorted(EV): report(k, EV[k])

print("\nB. DAILY TREND FILTER on the dip-buy (5m RSI<30 long), SPY vs its 20-day average at the prior close")
sma = {}
for i in range(20, len(DD)): sma[DD[i]] = sum(daily[DD[j]][3] for j in range(i - 20, i)) / 20  # 20d avg of closes before day
up = [(d, x) for d, x in EV["5m RSI14 crosses below 30 -> long"] if d in sma and daily[DD[DD.index(d) - 1]][3] > sma[d]]
dn = [(d, x) for d, x in EV["5m RSI14 crosses below 30 -> long"] if d in sma and daily[DD[DD.index(d) - 1]][3] <= sma[d]]
report("dip-buy, SPY ABOVE 20-day", up); report("dip-buy, SPY BELOW 20-day", dn)

print("\nC. OPENING GAPS (intraday, 165 days): fill = trades back to prior close the same day")
rows = []
for k, d in enumerate(DAYS[1:], 1):
    pc = days[DAYS[k - 1]][-1]["c"]; b = days[d]; o = b[0]["o"]; g = 100 * (o - pc) / pc
    fill_t = next((x["t"] for x in b if (x["l"] <= pc if g > 0 else x["h"] >= pc)), None)
    rows.append((d, g, fill_t, b[-1]["c"] - o))
for lo, hi in ((0, .1), (.1, .3), (.3, .6), (.6, 9)):
    r = [x for x in rows if lo <= abs(x[1]) < hi]
    if not r: continue
    fills = [x for x in r if x[2] is not None]; by30 = [x for x in fills if x[2] < 600]
    gogo = sum(1 for x in r if (x[3] > 0) == (x[1] > 0))
    print(f"  gap {lo:.1f}-{hi:.1f}%: n={len(r):3d}  filled same day {100*len(fills)/len(r):3.0f}%  filled by 10:00 {100*len(by30)/len(r):3.0f}%  "
          f"median fill time {('%02d:%02d' % divmod(int(st.median(x[2] for x in fills)), 60)) if fills else '-'}  day kept going gap's way (close>open for gap up) {100*gogo/len(r):3.0f}%")
print("  20-year daily check (SPY 2006-2026):")
drows = []
for i in range(1, len(DD)):
    o, h, l, c = daily[DD[i]][:4]; pc = daily[DD[i - 1]][3]; g = 100 * (o - pc) / pc
    drows.append((DD[i], g, (l <= pc) if g > 0 else (h >= pc), (c > o) == (g > 0)))
for lo, hi in ((0.1, .3), (.3, .6), (.6, 1.2), (1.2, 99)):
    for side in (1, -1):
        r = [x for x in drows if lo <= side * x[1] < hi]
        if r: print(f"    gap {'up' if side > 0 else 'down'} {lo:.1f}-{hi:.1f}%: n={len(r):4d} filled {100*sum(x[2] for x in r)/len(r):3.0f}%  kept going {100*sum(x[3] for x in r)/len(r):3.0f}%   (2006-15: filled {100*sum(x[2] for x in r if x[0]<'2016')/max(1,sum(1 for x in r if x[0]<'2016')):.0f}% / 2016-26: {100*sum(x[2] for x in r if x[0]>='2016')/max(1,sum(1 for x in r if x[0]>='2016')):.0f}%)")

print("\nD. VIX EXPECTED MOVE (daily, 2006-2026): 1 sigma = prior close x VIX/100/sqrt(252)")
inside = tag_hi = closes_beyond = n = 0; byv = collections.defaultdict(lambda: [0, 0])
for i in range(1, len(DD)):
    v = vix_on(DD[i - 1])
    if not v: continue
    o, h, l, c = daily[DD[i]][:4]; pc = daily[DD[i - 1]][3]; em = pc * v / 100 / math.sqrt(252)
    n += 1; inside += (h <= pc + em and l >= pc - em)
    for s, touched in ((1, h >= pc + em), (-1, l <= pc - em)):
        if touched: tag_hi += 1; closes_beyond += (s * (c - pc) >= em)
    bucket = "<15" if v < 15 else "15-20" if v < 20 else "20-30" if v < 30 else "30+"
    byv[bucket][0] += 1; byv[bucket][1] += abs(c - pc) / em
print(f"  days fully inside the +-1 sigma band: {100*inside/n:.0f}%   band tagged (either side): {100*tag_hi/n:.0f}% of days")
print(f"  when SPY tags the 1-sigma edge, it CLOSES beyond it {100*closes_beyond/max(1,tag_hi):.0f}% of the time (the rest fall back inside)")
for k in ("<15", "15-20", "20-30", "30+"): print(f"  VIX {k:6s}: actual |close move| / expected = {byv[k][1]/byv[k][0]:.2f} (n={byv[k][0]})")
print("  intraday (165 days): share of the day's full range already printed by")
for t in (600, 630, 690, 780, 900):
    sh = [ (max(x['h'] for x in days[d] if x['t'] < t) - min(x['l'] for x in days[d] if x['t'] < t)) / (max(x['h'] for x in days[d]) - min(x['l'] for x in days[d])) for d in DAYS]
    print(f"    {t//60:02d}:{t%60:02d}  median {100*st.median(sh):.0f}%")
hi_t = collections.Counter(); lo_t = collections.Counter()
for d in DAYS:
    b = days[d]; hi_t[(max(b, key=lambda x: x['h'])['t'] - 570) // 30] += 1; lo_t[(min(b, key=lambda x: x['l'])['t'] - 570) // 30] += 1
print("  when the day's HIGH / LOW printed (% of days per half hour):")
print("    " + "  ".join(f"{(570+30*k)//60:02d}:{(570+30*k)%60:02d} {100*hi_t[k]/len(DAYS):.0f}/{100*lo_t[k]/len(DAYS):.0f}" for k in range(13)))

print("\nE. NEWS DAYS (2026, intraday)")
fomc = [d for d in json.load(open(H / "fomc_dates.json"))["scheduled"] if d in DAYS]
cpi = [d for d in ["2026-03-11", "2026-04-10", "2026-05-12", "2026-06-10", "2026-07-14", "2026-08-12", "2026-09-11", "2026-10-14"] if d in DAYS]
nfp = [d for d in ["2026-03-06", "2026-08-07", "2026-09-04", "2026-10-02", "2026-04-03", "2026-05-08", "2026-06-05", "2026-07-02"] if d in DAYS]
def rng(d, t0=570, t1=960):
    s = [x for x in days[d] if t0 <= x["t"] < t1]; return max(x["h"] for x in s) - min(x["l"] for x in s)
normal = [d for d in DAYS if d not in fomc + cpi + nfp]
print(f"  normal days median range {st.median(rng(d) for d in normal):.2f} pts | 14:00-16:00 range {st.median(rng(d,840) for d in normal):.2f}")
for nm, ds in (("FOMC (2:00pm)", fomc), ("CPI (8:30am)", cpi), ("Jobs report (8:30am; Apr-Jul dates estimated)", nfp)):
    if not ds: continue
    gaps = [abs(days[d][0]["o"] - days[DAYS[DAYS.index(d) - 1]][-1]["c"]) for d in ds if DAYS.index(d) > 0]
    print(f"  {nm}: n={len(ds)} median day range {st.median(rng(d) for d in ds):.2f} | median |gap| {st.median(gaps):.2f} | 14:00-16:00 range {st.median(rng(d,840) for d in ds):.2f}")
for d in fomc:
    b = days[d]; at = next(x for x in b if x["t"] >= 840); i = b.index(at)
    first = b[i + 3]["c"] - b[i - 1]["c"]; rest = b[-1]["c"] - b[i + 3]["c"]
    print(f"    FOMC {d}: first 20 min after 2:00 {first:+.2f}, then to close {rest:+.2f} -> {'REVERSED' if first * rest < 0 else 'continued'}")
normal_gap = [abs(days[d][0]["o"] - days[DAYS[DAYS.index(d) - 1]][-1]["c"]) for d in normal if DAYS.index(d) > 0]
print(f"  normal days median |gap| {st.median(normal_gap):.2f}")
print("  20-year FOMC statement days vs all days (daily high-low % range):")
fall = json.load(open(H / "fomc_dates.json"))["scheduled"]
r = lambda d: 100 * (daily[d][1] - daily[d][2]) / daily[d][3]
fd = [d for d in fall if d in daily]; nd = [d for d in DD if d not in set(fall)]
print(f"    FOMC days median range {st.median(r(d) for d in fd):.2f}% vs other days {st.median(r(d) for d in nd):.2f}%  (n={len(fd)})")
nxt = [DD[DD.index(d) + 1] for d in fd if DD.index(d) + 1 < len(DD)]
print(f"    day AFTER FOMC median range {st.median(r(d) for d in nxt):.2f}%")
