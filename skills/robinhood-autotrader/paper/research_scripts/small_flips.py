"""Small/meme-coin flips (hold <= 2h), Nolan's style. 2y hourly Coinbase, two halves.
RH spot spread measured live 10/20: DOGE/SHIB/SOL/XRP/AVAX 1.9%, WIF 2.0%, PEPE/BONK 2.1% round trip -> cost 2.0%.
1) How often does each coin touch +2% within 2h (the break-even)?
2) Setups held 2h (exit at open 2h later), and with an options-style bracket: target +T% / stop -S% within 2h
   (both hit in one bar -> count the stop; conservative). Gross and after 2.0% cost.
3) Cross-coin: each hour buy the basket's biggest 4h gainer / biggest 4h loser, hold 2h."""
import json, statistics as st
from pathlib import Path
C = Path(__file__).resolve().parent.parent / "history" / "crypto"
COINS = ("doge", "shib", "pepe", "bonk", "wif", "sol", "avax", "xrp")
COST = 0.020
OUT = {}
def load(c):
    h = json.load(open(C / f"{c}_hourly.json")); k = sorted(h)
    return k, [h[x][0] for x in k], [h[x][1] for x in k], [h[x][2] for x in k], [h[x][3] for x in k], [h[x][4] for x in k]
def bracket(o, hi, lo, i, T, S, hold=2):
    e = o[i]
    for j in range(i, i + hold):
        if lo[j] <= e * (1 - S): return -S
        if hi[j] >= e * (1 + T): return T
    return o[i + hold] / e - 1
def summ(r):
    if len(r) < 15: return None
    g = st.mean(r); return dict(n=len(r), gross_bp=round(g * 1e4, 1), net_bp=round((g - COST) * 1e4, 1), win_net=round(100 * sum(x > COST for x in r) / len(r)))
setups = {
    "dip -5% in 4h": lambda c, v, i: c[i] / c[i - 4] - 1 <= -0.05,
    "pump +5% in 4h": lambda c, v, i: c[i] / c[i - 4] - 1 >= 0.05,
    "volume spike 4x + green hour": lambda c, v, i: v[i] > 4 * st.mean(v[i - 24:i]) and c[i] > c[i - 1],
    "volume spike 4x + red hour": lambda c, v, i: v[i] > 4 * st.mean(v[i - 24:i]) and c[i] < c[i - 1],
    "new 24h high": lambda c, v, i: c[i] > max(c[i - 24:i]),
    "crash -10% in 24h": lambda c, v, i: c[i] / c[i - 24] - 1 <= -0.10,
}
exits = {"hold 2h": None, "bracket +4/-2": (0.04, 0.02), "bracket +6/-3": (0.06, 0.03), "bracket +10/-5": (0.10, 0.05)}
agg = {}
for coin in COINS:
    k, o, hi, lo, c, v = load(coin); mid = len(k) // 2
    halves = (("H1", 30, mid), ("H2", mid, len(k) - 3))
    for lab, a, b in halves:
        mfe = [max(hi[i], hi[i + 1]) / o[i] - 1 for i in range(a, b)]
        OUT[f"{coin} touch+2% {lab}"] = round(100 * sum(x >= COST for x in mfe) / len(mfe), 1)
    print(f"{coin.upper():5s} touches +2% within 2h: {OUT[f'{coin} touch+2% H1']}% / {OUT[f'{coin} touch+2% H2']}% of hours")
    for sn, f in setups.items():
        for en, ex in exits.items():
            for lab, a, b in halves:
                r, last = [], -99
                for i in range(a, b):
                    if i - last < 3 or not f(c, v, i): continue
                    last = i; r.append(o[i + 3] / o[i + 1] - 1 if ex is None else bracket(o, hi, lo, i + 1, *ex))
                agg.setdefault((sn, en, lab), []).extend(r)
for (sn, en, lab), r in sorted(agg.items()):
    s = summ(r)
    if s: OUT[f"pooled {sn} | {en} | {lab}"] = s
print("\nPooled across 8 coins (n, gross, after 2% RH cost, % trades that beat cost):")
for sn in setups:
    for en in exits:
        a, b = OUT.get(f"pooled {sn} | {en} | H1"), OUT.get(f"pooled {sn} | {en} | H2")
        if a and b: print(f"  {sn:30s} {en:15s} H1 n{a['n']:5d} gross {a['gross_bp']:+7.1f} net {a['net_bp']:+7.1f} | H2 n{b['n']:5d} gross {b['gross_bp']:+7.1f} net {b['net_bp']:+7.1f}")
# 3) cross-coin rank
data = {c: load(c) for c in COINS}
common = sorted(set.intersection(*(set(data[c][0]) for c in COINS)))
idx = {c: {t: i for i, t in enumerate(data[c][0])} for c in COINS}
for side in ("top gainer", "top loser"):
    for lab, a, b in (("H1", 30, len(common) // 2), ("H2", len(common) // 2, len(common) - 3)):
        r = []
        for n in range(a, b, 3):
            t = common[n]
            def ch(c):
                i = idx[c][t]; _, o, hi, lo, cl, v = data[c]
                return cl[i] / cl[i - 4] - 1 if i >= 4 else 0
            pick = (max if side == "top gainer" else min)(COINS, key=ch)
            i = idx[pick][t]; o = data[pick][1]
            if i + 3 < len(o): r.append(o[i + 3] / o[i + 1] - 1)
        s = summ(r); OUT[f"rank {side} {lab}"] = s
        print(f"  buy {side} of last 4h, hold 2h {lab}: n {s['n']} gross {s['gross_bp']:+.1f}bp net {s['net_bp']:+.1f}bp")
json.dump(OUT, open(Path(__file__).with_name("small_flips.json"), "w"), indent=1)
