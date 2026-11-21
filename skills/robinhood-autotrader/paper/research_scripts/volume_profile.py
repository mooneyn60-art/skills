"""TikTok (@tradingelder, 10/20): "Volume profile + orderflow = payouts". Location = prior session's value area
(VAH/VAL, 70% of volume) and POC; trigger = order-flow absorption (needs tick/delta data we don't have).
We test the LOCATION half, the part our bars can see:
 A) Fade at the edge: today's first touch of prior VAL from above -> long, target POC, stop the same distance below (1:1).
    Mirror for VAH -> short. Control: the same 1:1 test at a random level the same distance from the open.
 B) The "80% rule": open outside the prior value area, then 2 bars close back inside -> target the far edge, stop = the open.
Data: SPY 1-min (~34 sessions), BTC/ETH hourly (3y, UTC days), SOL/DOGE/PEPE/BONK/WIF hourly (2y)."""
import json, random, statistics as st
from pathlib import Path
from collections import defaultdict
H = Path(__file__).resolve().parent.parent / "history"
random.seed(7)
def profile(bars, nb=60):
    lo = min(b[2] for b in bars); hi = max(b[1] for b in bars); w = (hi - lo) / nb or 1e-9
    vol = [0.0] * nb
    for o, h, l, c, v in bars:
        a, b = int((l - lo) / w), min(nb - 1, int((h - lo) / w)); a = min(a, nb - 1)
        for j in range(a, b + 1): vol[j] += v / (b - a + 1)
    p = max(range(nb), key=vol.__getitem__); i = j = p; tot = sum(vol); s = vol[p]
    while s < 0.7 * tot:
        up = vol[j + 1] if j + 1 < nb else -1; dn = vol[i - 1] if i > 0 else -1
        if up >= dn: j += 1; s += up
        else: i -= 1; s += dn
    f = lambda k: lo + (k + 0.5) * w
    return f(i) - w / 2, f(p), f(j) + w / 2
def race(bars, entry, tgt, stop):
    up = tgt > entry
    for o, h, l, c, v in bars:
        if (l <= stop) if up else (h >= stop): return 0
        if (h >= tgt) if up else (l <= tgt): return 1
    return None
def run(sessions, label):
    days = sorted(sessions); res = defaultdict(list)
    for d0, d1 in zip(days, days[1:]):
        prev, today = sessions[d0], sessions[d1]
        if len(prev) < 10 or len(today) < 10: continue
        val, poc, vah = profile(prev); op = today[0][0]
        # A) first touch of an edge from inside/outside-in
        for side, lvl in (("VAL long", val), ("VAH short", vah)):
            long = side.startswith("VAL")
            if (long and op <= val) or (not long and op >= vah) or abs(poc - lvl) <= 0: continue
            k = next((n for n, b in enumerate(today) if (b[2] <= lvl if long else b[1] >= lvl)), None)
            if k is None: continue
            dist = abs(poc - lvl); stop = lvl - dist if long else lvl + dist
            r = race(today[k + 1:], lvl, poc, stop)
            if r is not None: res[side].append(r)
            # control: random level same distance from the open as the edge was, same 1:1 test
            g = abs(op - lvl) * random.uniform(0.5, 1.5); cl = op - g if long else op + g
            kc = next((n for n, b in enumerate(today) if (b[2] <= cl if long else b[1] >= cl)), None)
            if kc is not None:
                rc = race(today[kc + 1:], cl, cl + dist if long else cl - dist, cl - dist if long else cl + dist)
                if rc is not None: res["control " + side].append(rc)
        # B) 80% rule
        if op < val or op > vah:
            long = op < val; ins = 0
            for n, b in enumerate(today):
                ins = ins + 1 if val < b[3] < vah else 0
                if ins == 2:
                    e = b[3]; tgt = vah if long else val; stop = min(x[2] for x in today[:n + 1]) if long else max(x[1] for x in today[:n + 1])
                    r = race(today[n + 1:], e, tgt, stop)
                    if r is not None: res["80% rule"].append(r); res["80% rule R"].append(abs(tgt - e) / abs(e - stop) if e != stop else 0)
                    break
    out = {}
    for k, v in res.items():
        if k == "80% rule R": continue
        out[k] = dict(n=len(v), hit=round(100 * st.mean(v), 1))
    if res["80% rule R"]: out["80% rule"]["median_reward_to_risk"] = round(st.median(res["80% rule R"]), 2)
    print(label, json.dumps(out)); return out
if __name__ == "__main__":
    OUT = {}
    spy = json.load(open(H / "spy_1min.json")); s = defaultdict(list)
    for t in sorted(spy):
        if "13:30" <= t[11:] < "20:00": s[t[:10]].append(spy[t])
    OUT["SPY 1min"] = run(s, "SPY 1min")
    for coin in ("btc", "eth", "sol", "doge", "pepe", "bonk", "wif"):
        h = json.load(open(H / "crypto" / f"{coin}_hourly.json")); s = defaultdict(list)
        for t in sorted(h): s[t[:10]].append(h[t])
        keys = sorted(s); mid = len(keys) // 2
        for lab, ks in (("H1", keys[:mid]), ("H2", keys[mid:])):
            OUT[f"{coin} {lab}"] = run({k: s[k] for k in ks}, f"{coin.upper()} {lab}")
    json.dump(OUT, open(Path(__file__).with_name("volume_profile.json"), "w"), indent=1)
