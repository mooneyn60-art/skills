"""TARS crypto lab: what actually works in crypto after Robinhood's real cost? Coinbase daily candles
(BTC 2015-, ETH 2016-, SOL/DOGE 2021-) and 3y hourly BTC/ETH. Every strategy is checked in two halves.
Cost: Robinhood's quoted bid/ask spread on 2026-10-20 was ~1.9% for BTC/ETH/SOL/DOGE -> 0.95% per side."""
import json, math, statistics as st, datetime as dt, collections
from pathlib import Path
H = Path(__file__).resolve().parent.parent / "history"
C = H / "crypto"; SIDE = 0.0095
def load(n): d = json.load(open(C / f"{n}_daily.json")); k = sorted(d); return k, [d[x][3] for x in k], [d[x][0] for x in k]
OUT = {}
def stats(rets, days_per_year=365):
    if len(rets) < 30: return None
    eq = 1; peak = 1; dd = 0
    for r in rets: eq *= 1 + r; peak = max(peak, eq); dd = min(dd, eq / peak - 1)
    yrs = len(rets) / days_per_year; cagr = eq ** (1 / yrs) - 1 if eq > 0 else -1
    sd = st.pstdev(rets) * math.sqrt(days_per_year); m = st.mean(rets) * days_per_year
    return dict(cagr=round(100 * cagr, 1), vol=round(100 * sd, 0), sharpe=round(m / sd, 2) if sd else 0, maxdd=round(100 * dd, 0))
def run(close, signal, cost=SIDE):
    """signal[i] = hold during day i+1 (decided at close i). Returns daily strategy returns and trade count."""
    out, pos, trades = [], 0, 0
    for i in range(1, len(close)):
        s = signal[i - 1]; r = close[i] / close[i - 1] - 1
        c = cost if s != pos else 0; trades += s != pos; pos = s
        out.append(r * s - c)
    return out, trades
def sma(x, n): return [None if i < n - 1 else sum(x[i - n + 1:i + 1]) / n for i in range(len(x))]
def halves(keys, split):
    i = next(j for j, k in enumerate(keys) if k >= split); return [(f"{keys[0][:4]}-{keys[i-1][:4]}", 0, i), (f"{keys[i][:4]}-{keys[-1][:4]}", i, len(keys))]

print("1-2. Buy & hold vs trend filters (cost 0.95%/side). CAGR % | vol % | Sharpe | max drawdown %")
for coin, split in (("btc", "2021-01-01"), ("eth", "2021-06-01"), ("sol", "2023-12-01"), ("doge", "2023-12-01")):
    k, c, o = load(coin)
    s200, s50, s20 = sma(c, 200), sma(c, 50), sma(c, 20)
    mom30 = [None if i < 30 else c[i] / c[i - 30] - 1 for i in range(len(c))]
    hi20 = [None if i < 20 else max(c[i - 20:i]) for i in range(len(c))]; lo10 = [None if i < 10 else min(c[i - 10:i]) for i in range(len(c))]
    don, p = [], 0
    for i in range(len(c)):
        if hi20[i] and c[i] > hi20[i]: p = 1
        elif lo10[i] and c[i] < lo10[i]: p = 0
        don.append(p)
    sigs = {"buy & hold": [1] * len(c), "above 200d avg": [int(bool(s200[i]) and c[i] > s200[i]) for i in range(len(c))],
            "50d > 200d": [int(bool(s200[i]) and s50[i] > s200[i]) for i in range(len(c))],
            "above 20d avg": [int(bool(s20[i]) and c[i] > s20[i]) for i in range(len(c))],
            "30d momentum > 0": [int(bool(mom30[i]) and mom30[i] > 0) for i in range(len(c))], "20d breakout / 10d low exit": don}
    for lab, a, b in halves(k, split):
        for name, sg in sigs.items():
            start = max(a, 200 if coin in ("btc", "eth") else 50)
            r, n = run(c[start:b], sg[start:b], 0 if name == "buy & hold" else SIDE)
            s = stats(r)
            if s: OUT.setdefault(f"{coin.upper()} {lab}", {})[name] = dict(s, trades=n); print(f"  {coin.upper():4s} {lab} {name:28s} {s['cagr']:7.1f} {s['vol']:5.0f} {s['sharpe']:5.2f} {s['maxdd']:5.0f}  trades {n}")

print("\n3. Day of week (BTC, mean daily %), halves")
k, c, o = load("btc")
for lab, a, b in halves(k, "2021-01-01"):
    by = collections.defaultdict(list)
    for i in range(max(a, 1), b): by[dt.date.fromisoformat(k[i]).weekday()].append(100 * (c[i] / c[i - 1] - 1))
    print(f"  {lab}: " + "  ".join(f"{d}:{st.mean(by[j]):+.2f}" for j, d in enumerate("MTWTFSS")))
    OUT[f"BTC dow {lab}"] = {d: round(st.mean(by[j]), 3) for j, d in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])}

print("\n4. After a big down day (BTC close-to-close <= -5%): next 1 / 5 days, %")
for lab, a, b in halves(k, "2021-01-01"):
    n1, n5 = [], []
    for i in range(max(a, 1), b - 5):
        if c[i] / c[i - 1] - 1 <= -0.05: n1.append(100 * (c[i + 1] / c[i] - 1)); n5.append(100 * (c[i + 5] / c[i] - 1))
    print(f"  {lab}: n {len(n1)}  next day {st.mean(n1):+.2f} (up {100*sum(x>0 for x in n1)/len(n1):.0f}%)  next 5 {st.mean(n5):+.2f} (up {100*sum(x>0 for x in n5)/len(n5):.0f}%)")
    OUT[f"BTC after -5% {lab}"] = dict(n=len(n1), next1=round(st.mean(n1), 2), next5=round(st.mean(n5), 2))

print("\n5. Hour of day (BTC hourly 3y, UTC): US stock-market hours vs closed hours, mean bp/hour")
hb = json.load(open(C / "btc_hourly.json")); hk = sorted(hb); mid = hk[len(hk) // 2]
for lab, sel in (("first 1.5y", lambda t: t < mid), ("last 1.5y", lambda t: t >= mid)):
    by = collections.defaultdict(list)
    for t in hk:
        if not sel(t): continue
        op, hi, lo, cl, v = hb[t]; by[int(t[11:13])].append(1e4 * (cl / op - 1))
    us = [x for h in range(14, 21) for x in by[h]]; off = [x for h in list(range(0, 14)) + list(range(21, 24)) for x in by[h]]
    best = sorted(by, key=lambda h: -st.mean(by[h]))[:3]; worst = sorted(by, key=lambda h: st.mean(by[h]))[:3]
    print(f"  {lab}: US hours {st.mean(us):+.2f} bp/h, closed hours {st.mean(off):+.2f} bp/h; best UTC hours {best}, worst {worst}")
    OUT[f"BTC hours {lab}"] = dict(us=round(st.mean(us), 2), closed=round(st.mean(off), 2), best=best, worst=worst)

print("\n6. BTC vs SPY: daily correlation by year (same calendar day)")
spy = json.load(open(H / "daily_ohlcv.json"))["SPY"]; sk = sorted(spy); bmap = dict(zip(k, c))
for y in range(2018, 2027):
    xs, ys = [], []
    for i in range(1, len(sk)):
        d, p = sk[i], sk[i - 1]
        if d[:4] == str(y) and d in bmap and p in bmap: xs.append(spy[d][3] / spy[p][3] - 1); ys.append(bmap[d] / bmap[p] - 1)
    if len(xs) > 30:
        mx, my = st.mean(xs), st.mean(ys); cv = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
        r = cv / math.sqrt(sum((a - mx) ** 2 for a in xs) * sum((b - my) ** 2 for b in ys)); OUT.setdefault("BTC-SPY corr", {})[y] = round(r, 2)
print("  ", OUT["BTC-SPY corr"])

print("\n7. Volatility targeting (BTC, 40% annual vol target, 30d realized; rebalance weekly, cost on the change)")
rets = [c[i] / c[i - 1] - 1 for i in range(1, len(c))]
for lab, a, b in halves(k, "2021-01-01"):
    out, w = [], 0.0
    for i in range(max(a, 31), b - 1):
        if i % 7 == 0:
            rv = st.pstdev(rets[i - 30:i]) * math.sqrt(365); nw = min(1.0, 0.40 / rv) if rv else 0
            cost = abs(nw - w) * SIDE; w = nw
        else: cost = 0
        out.append(w * rets[i] - cost)
    bh = stats(rets[max(a, 31):b - 1]); vt = stats(out)
    print(f"  {lab}: hold Sharpe {bh['sharpe']} maxDD {bh['maxdd']}% | vol-target Sharpe {vt['sharpe']} maxDD {vt['maxdd']}% CAGR {vt['cagr']}%")
    OUT[f"BTC voltarget {lab}"] = dict(hold=bh, voltarget=vt)
json.dump(OUT, open(Path(__file__).with_name("crypto_lab.json"), "w"), indent=1)
