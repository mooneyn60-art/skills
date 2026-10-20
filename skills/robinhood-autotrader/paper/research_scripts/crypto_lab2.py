"""Crypto lab round 2: slower ideas that pay the 1.9% spread rarely. BTC/ETH daily (Coinbase), SPY daily, FOMC dates.
Halves: BTC/ETH 2016-2020 vs 2021-2026. Cost 0.95% per side on every switch."""
import json, math, statistics as st, datetime as dt, collections
from pathlib import Path
H = Path(__file__).resolve().parent.parent / "history"; C = H / "crypto"; SIDE = 0.0095
def load(n): d = json.load(open(C / f"{n}_daily.json")); k = sorted(d); return k, [d[x][3] for x in k]
def stats(r, ppy):
    if len(r) < 6: return None
    eq = peak = 1; dd = 0
    for x in r: eq *= 1 + x; peak = max(peak, eq); dd = min(dd, eq / peak - 1)
    yrs = len(r) / ppy; sd = st.pstdev(r) * math.sqrt(ppy)
    return dict(cagr=round(100 * ((eq ** (1 / yrs) - 1) if eq > 0 else -1), 1), sharpe=round(st.mean(r) * ppy / sd, 2) if sd else 0, maxdd=round(100 * dd))
OUT = {}; HALF = lambda d: "2016-20" if d < "2021" else "2021-26"
kb, cb = load("btc"); ke, ce = load("eth"); emap = dict(zip(ke, ce))
# month-end series
def month_ends(k, c):
    out = {}
    for d, v in zip(k, c): out[d[:7]] = (d, v)
    return [out[m] for m in sorted(out)]
mb = month_ends(kb, cb); me = {m[0][:7]: m for m in month_ends(ke, ce)}
print("1. Monthly time-series momentum (hold next month if the last L months were up), vs holding every month")
for L in (1, 3, 6, 12):
    for coin, M in (("BTC", mb), ("ETH", month_ends(ke, ce))):
        rs = collections.defaultdict(list); hold = collections.defaultdict(list); pos = 0
        for i in range(L, len(M) - 1):
            d = M[i][0]
            if d < "2016-06": continue
            sig = int(M[i][1] > M[i - L][1]); r = M[i + 1][1] / M[i][1] - 1
            cost = SIDE if sig != pos else 0; pos = sig
            rs[HALF(d)].append(sig * r - cost); hold[HALF(d)].append(r)
        for h in ("2016-20", "2021-26"):
            a, b = stats(rs[h], 12), stats(hold[h], 12)
            if a: OUT[f"tsmom {coin} L{L} {h}"] = dict(strategy=a, hold=b); print(f"  {coin} L={L:2d} {h}: strategy {a['cagr']:6.1f}%/yr Sharpe {a['sharpe']:5.2f} maxDD {a['maxdd']:4d}% | hold {b['cagr']:6.1f}% Sharpe {b['sharpe']:5.2f} maxDD {b['maxdd']:4d}%")
print("\n2. BTC vs ETH monthly rotation (hold the one with the stronger last-3-month return)")
rs = collections.defaultdict(list); pos = None
for i in range(3, len(mb) - 1):
    m, m3, m1 = mb[i][0][:7], mb[i - 3][0][:7], mb[i + 1][0][:7]
    if m not in me or m3 not in me or m1 not in me or mb[i][0] < "2016-09": continue
    rb = mb[i][1] / mb[i - 3][1]; re_ = me[m][1] / me[m3][1]; pick = "BTC" if rb >= re_ else "ETH"
    r = (mb[i + 1][1] / mb[i][1] - 1) if pick == "BTC" else (me[m1][1] / me[m][1] - 1)
    cost = 2 * SIDE if pos and pick != pos else 0; pos = pick
    rs[HALF(mb[i][0])].append(r - cost)
for h in rs: s = stats(rs[h], 12); OUT[f"rotation {h}"] = s; print(f"  {h}: {s}")
print("\n3. Weekend: BTC Friday 20:00 UTC -> Monday 13:30 UTC (what an IBIT holder carries over the weekend), %")
hb = json.load(open(C / "btc_hourly.json"))
wk = collections.defaultdict(list)
for k in sorted(hb):
    if not k.endswith("T20:00Z") or dt.date.fromisoformat(k[:10]).weekday() != 4: continue
    mon = (dt.date.fromisoformat(k[:10]) + dt.timedelta(days=3)).isoformat() + "T13:00Z"
    if mon in hb: wk["2023-24" if k < "2025-04" else "2025-26"].append(100 * (hb[mon][0] / hb[k][0] - 1))
for h, v in wk.items(): print(f"  {h}: n {len(v)} mean {st.mean(v):+.2f}% median {st.median(v):+.2f}% up {100*sum(x>0 for x in v)/len(v):.0f}%  avg size {st.mean(abs(x) for x in v):.2f}%"); OUT[f"weekend {h}"] = dict(n=len(v), mean=round(st.mean(v), 2), up=round(100 * sum(x > 0 for x in v) / len(v)), size=round(st.mean(abs(x) for x in v), 2))
print("\n4. Fed days: BTC close-to-close on FOMC statement days vs other days, % (and size)")
fomc = set(json.load(open(H / "fomc_dates.json"))["scheduled"]); prev = dict(zip(kb[1:], kb[:-1])); bm = dict(zip(kb, cb))
for h in ("2016-20", "2021-26"):
    f = [100 * (bm[d] / bm[prev[d]] - 1) for d in kb[1:] if HALF(d) == h and d >= "2016" and d in fomc]
    o = [100 * (bm[d] / bm[prev[d]] - 1) for d in kb[1:] if HALF(d) == h and d >= "2016" and d not in fomc]
    print(f"  {h}: FOMC n {len(f)} mean {st.mean(f):+.2f}% size {st.mean(abs(x) for x in f):.2f}% | other days mean {st.mean(o):+.2f}% size {st.mean(abs(x) for x in o):.2f}%")
    OUT[f"fomc {h}"] = dict(n=len(f), mean=round(st.mean(f), 2), size=round(st.mean(abs(x) for x in f), 2), other_mean=round(st.mean(o), 3), other_size=round(st.mean(abs(x) for x in o), 2))
print("\n5. Does the stock market's trend help BTC? BTC next-day return when SPY is above/below its 200-day average, %/day")
spy = json.load(open(H / "daily_ohlcv.json"))["SPY"]; sk = sorted(spy)
s200 = {sk[i]: st.mean(spy[sk[j]][3] for j in range(i - 200, i)) for i in range(200, len(sk))}
for h in ("2016-20", "2021-26"):
    up, dn = [], []
    for i in range(len(sk) - 1):
        d, n = sk[i], sk[i + 1]
        if d not in s200 or d not in bm or n not in bm or HALF(d) != h or d < "2016": continue
        (up if spy[d][3] > s200[d] else dn).append(100 * (bm[n] / bm[d] - 1))
    print(f"  {h}: SPY above 200d n {len(up)} BTC {st.mean(up):+.3f}%/day | below n {len(dn)} BTC {st.mean(dn):+.3f}%/day")
    OUT[f"spy-trend {h}"] = dict(above=round(st.mean(up), 3), below=round(st.mean(dn), 3), n_above=len(up), n_below=len(dn))
print("\n6. BTC above its 200-day AND SPY above its 200-day (both trends up) vs everything else, BTC %/day")
b200 = {kb[i]: st.mean(cb[i - 200:i]) for i in range(200, len(kb))}
for h in ("2016-20", "2021-26"):
    both, rest = [], []
    for i in range(len(sk) - 1):
        d, n = sk[i], sk[i + 1]
        if d not in s200 or d not in b200 or n not in bm or HALF(d) != h or d < "2016": continue
        (both if (spy[d][3] > s200[d] and bm[d] > b200[d]) else rest).append(100 * (bm[n] / bm[d] - 1))
    print(f"  {h}: both up n {len(both)} BTC {st.mean(both):+.3f}%/day (up {100*sum(x>0 for x in both)/len(both):.0f}%) | rest n {len(rest)} BTC {st.mean(rest):+.3f}%/day")
    OUT[f"both-trends {h}"] = dict(both=round(st.mean(both), 3), rest=round(st.mean(rest), 3), n_both=len(both), n_rest=len(rest))
json.dump(OUT, open(Path(__file__).with_name("crypto_lab2.json"), "w"), indent=1)
