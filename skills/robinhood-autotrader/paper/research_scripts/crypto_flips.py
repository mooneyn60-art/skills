"""Crypto flips (hold <= 2 hours), the way Nolan wants to trade. 3y hourly BTC/ETH (Coinbase), halves.
1) How often does price even move 1.9% (Robinhood's round-trip spread) in your favor within 2 hours?
2) Classic flip setups, held 2 hours: gross, after Robinhood spot cost (1.9%), after IBIT-share cost (~0.04%)."""
import json, statistics as st
from pathlib import Path
C = Path(__file__).resolve().parent.parent / "history" / "crypto"
OUT = {}
for coin in ("btc", "eth"):
    h = json.load(open(C / f"{coin}_hourly.json")); k = sorted(h); o = [h[x][0] for x in k]; hi = [h[x][1] for x in k]; lo = [h[x][2] for x in k]; c = [h[x][3] for x in k]
    mid = len(k) // 2
    # 1) best-case: max high within the next 2 hours vs entry at the open
    for lab, a, b in (("first 1.5y", 24, mid), ("last 1.5y", mid, len(k) - 2)):
        mfe = [max(hi[i], hi[i + 1]) / o[i] - 1 for i in range(a, b)]
        hit = sum(x >= 0.019 for x in mfe) / len(mfe)
        OUT[f"{coin} reach+1.9% {lab}"] = round(100 * hit, 1)
        print(f"{coin.upper()} {lab}: the price touched +1.9% within 2 hours on {100*hit:.1f}% of hours (median best move {100*st.median(mfe):.2f}%)")
    # 2) setups, entry at the next hour's open, exit 2 hours later at the open
    def rsi(i, n=14):
        g = [max(c[j] - c[j - 1], 0) for j in range(i - n + 1, i + 1)]; l = [max(c[j - 1] - c[j], 0) for j in range(i - n + 1, i + 1)]
        return 100 - 100 / (1 + (sum(g) / n) / ((sum(l) / n) or 1e-9))
    setups = {
        "dip: down 2%+ in 4h": lambda i: c[i] / c[i - 4] - 1 <= -0.02,
        "breakout: new 24h high": lambda i: c[i] > max(hi[i - 24:i]),
        "oversold: RSI(14h) < 25": lambda i: rsi(i) < 25,
        "momentum: up 2%+ in 4h": lambda i: c[i] / c[i - 4] - 1 >= 0.02,
    }
    for name, f in setups.items():
        for lab, a, b in (("first 1.5y", 30, mid), ("last 1.5y", mid, len(k) - 3)):
            r, last = [], -99
            for i in range(a, b):
                if i - last < 3 or not f(i): continue
                last = i; r.append(o[i + 3] / o[i + 1] - 1)
            if len(r) < 10: continue
            g = 100 * st.mean(r); win = 100 * sum(x > 0 for x in r) / len(r)
            OUT[f"{coin} {name} {lab}"] = dict(n=len(r), gross=round(g, 3), win=round(win), rh_spot_bp=round(g * 100 - 190, 1), ibit_bp=round(g * 100 - 4, 1))
            print(f"  {coin.upper()} {name:26s} {lab}: n {len(r):4d} gross {g*100:+6.1f}bp win {win:3.0f}% | after RH spot {g*100-190:+7.1f}bp | after IBIT shares {g*100-4:+6.1f}bp")
json.dump(OUT, open(Path(__file__).with_name("crypto_flips.json"), "w"), indent=1)
