"""Nolan: "Even meme coins we can make a quick buck and get out before they dump it."
Test: catch a pump in progress and ride it. Meme coins DOGE SHIB PEPE BONK WIF, 2y hourly, halves.
Trigger: the last hour closed up >= X% (X = 3, 5, 8) on volume >= 3x its 24h average. Buy at the next open.
Exit: after 1h / 2h, or a trailing exit that sells the first hour that closes red (no peeking).
Also measured: after the trigger, how far it ran at best within 3h, and how far it fell at worst."""
import json, statistics as st
from pathlib import Path
C = Path(__file__).resolve().parent.parent / "history" / "crypto"
COST = 0.020; OUT = {}
pool = {}
for coin in ("doge", "shib", "pepe", "bonk", "wif"):
    h = json.load(open(C / f"{coin}_hourly.json")); k = sorted(h)
    o, hi, lo, c, v = ([h[x][j] for x in k] for j in (0, 1, 2, 3, 4)); mid = len(k) // 2
    for X in (0.03, 0.05, 0.08):
        for lab, a, b in (("H1", 30, mid), ("H2", mid, len(k) - 6)):
            last = -99
            for i in range(a, b):
                if i - last < 3: continue
                if c[i] / o[i] - 1 < X or v[i] < 3 * st.mean(v[i - 24:i]): continue
                last = i; e = o[i + 1]
                trail = next((c[j] / e - 1 for j in range(i + 1, i + 6) if c[j] < o[j]), c[i + 5] / e - 1)
                r = dict(h1=c[i + 1] / e - 1, h2=c[i + 2] / e - 1, trail=trail,
                         best=max(hi[i + 1:i + 4]) / e - 1, worst=min(lo[i + 1:i + 4]) / e - 1)
                pool.setdefault((X, lab), []).append(r)
for (X, lab), rs in sorted(pool.items()):
    s = {m: round(1e4 * st.mean(r[m] for r in rs), 1) for m in ("h1", "h2", "trail")}
    beat = {m: round(100 * sum(r[m] > COST for r in rs) / len(rs)) for m in ("h1", "h2", "trail")}
    OUT[f"pump>={int(X*100)}% {lab}"] = dict(n=len(rs), gross_bp=s, pct_trades_beat_cost=beat,
        median_best_3h=round(100 * st.median(r["best"] for r in rs), 2), median_worst_3h=round(100 * st.median(r["worst"] for r in rs), 2))
    print(f"pump >= {int(X*100)}% {lab}: n {len(rs):4d} | gross bp h1 {s['h1']:+6.1f} h2 {s['h2']:+6.1f} trail {s['trail']:+6.1f} | "
          f"net(trail) {s['trail']-200:+6.1f} | trades beating the 2% cost: {beat['trail']}% | median next-3h best +{OUT[f'pump>={int(X*100)}% {lab}']['median_best_3h']}% worst {OUT[f'pump>={int(X*100)}% {lab}']['median_worst_3h']}%")
json.dump(OUT, open(Path(__file__).with_name("meme_pump_ride.json"), "w"), indent=1)
