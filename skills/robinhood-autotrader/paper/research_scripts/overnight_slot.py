"""Can the options slot capture SPY's overnight edge? Reprice options with Black-Scholes across every real
SPY overnight move (close -> next open) 2016-2026, holding IV fixed, and compare with holding shares.
Also: the same, only on nights the overnight model scores p >= 0.60 (walk-forward, from predict_lab)."""
import json, math, statistics as st
from pathlib import Path
from math import log, sqrt, exp, erf
here = Path(__file__).resolve().parent
g = {"__file__": str(here / "predict_lab.py")}
exec(compile(open(here / "predict_lab.py").read().split("R = {}")[0], "pl", "exec"), g)
rows = [r for r in g["rows"] if r["d"] >= "2016"]
o = g["walk"]("on", "fc"); P = {r["d"]: p for r, p in zip(g["rows"], o["P"]["logit"]) if p == p}
N = lambda x: 0.5 * (1 + erf(x / sqrt(2)))
def call(S, K, T, v, r=0.04):
    if T <= 0: return max(0.0, S - K)
    d1 = (log(S / K) + (r + v * v / 2) * T) / (v * sqrt(T)); return S * N(d1) - K * exp(-r * T) * N(d1 - v * sqrt(T))
S0 = 763.0; out = {}; W = g["W"]
for label, sel in (("every night", lambda r: True), ("model p>=0.60 nights", lambda r: P.get(r["d"], 0) >= 0.60)):
    ons = [r["on"] for r in rows if sel(r)]
    res = {"n": len(ons), "shares_bp": round(1e4 * st.mean(ons), 2), "shares_up%": round(100 * sum(x > 0 for x in ons) / len(ons), 1)}
    import datetime as dt
    sub = [r for r in rows if sel(r)]
    for dte in (1, 7, 30):
        pnl = []
        for r in sub:
            iv = (W["vix"].get(r["d"]) or [0, 20])[1] / 100  # that day's VIX close as the option's IV (honest regime)
            i = g["D"].index(r["d"]); gap = (dt.date.fromisoformat(g["D"][i + 1]) - dt.date.fromisoformat(r["d"])).days
            hold = (gap - 1 + 17.5 / 24) / 365  # real calendar time to the next open (weekends included)
            T0 = max(dte, gap + 0.3) / 365       # contract must outlive the hold
            c0 = call(S0, S0, T0, iv) + 0.02
            pnl.append((call(S0 * math.exp(r["on"]), S0, T0 - hold, iv) - 0.02 - c0) / c0)
        res[f"{dte}DTE ATM call (IV = VIX)"] = f"{100*st.mean(pnl):+.2f}%/night, median {100*st.median(pnl):+.1f}%, win {100*sum(p > 0 for p in pnl)/len(pnl):.0f}%"
    out[label] = res
    print(label, json.dumps(res, indent=1))
json.dump(out, open(here / "overnight_slot.json", "w"), indent=1)
