"""Tonight's overnight-model score (paper tracking). Trains the overnight logit on all history (predict_lab.py
features, known at 16:00) and scores the latest SPY session. VIX for the latest day can be passed if world_daily
doesn't have it yet; DAX's day return defaults to 0 when missing (its weight is small).
Usage: python3 overnight_score.py [vix_close]   -> prints the score and appends to paper/overnight/ledger.jsonl"""
import json, sys, math, statistics as st, datetime as dt
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
here = Path(__file__).resolve().parent
g = {"__file__": str(here / "predict_lab.py")}
exec(compile(open(here / "predict_lab.py").read().split("R = {}")[0], "pl", "exec"), g)
rows, spy, D, W = g["rows"], g["spy"], g["D"], g["W"]
names = list(rows[0]["fc"]); X = np.nan_to_num(np.array([[r["fc"][k] for k in names] for r in rows], float)); Y = np.array([r["on"] > 0 for r in rows], int)
mu, sd = X.mean(0), X.std(0) + 1e-12; m = LogisticRegression(C=0.1, max_iter=2000).fit((X - mu) / sd, Y)
i = len(D) - 1; d = D[i]; o, h, l, c, v = spy[d]; cp = spy[D[i - 1]][3]
sma20 = st.mean(spy[D[j]][3] for j in range(i - 20, i))
vix_prev = (W["vix"].get(D[i - 1]) or [None, None])[1]
vix = float(sys.argv[1]) if len(sys.argv) > 1 else (W["vix"].get(d) or [None, vix_prev])[1]
x = dt.date.fromisoformat(d)
f = dict(r1=c / cp - 1, intra=c / o - 1, gap=o / cp - 1, r5=c / spy[D[i - 5]][3] - 1, dist20=c / sma20 - 1, vix=vix, dvix=vix / vix_prev - 1,
         rng=(h - l) / c, clv=((c - l) - (h - c)) / ((h - l) or 1), dow=x.weekday(), opex=float(x.weekday() == 4 and 15 <= x.day <= 21),
         dax=(W["dax"][d][1] / W["dax"][d][0] - 1) if d in W["dax"] else 0.0)
p = float(m.predict_proba(((np.array([[f[k] for k in names]]) - mu) / sd))[0, 1])
rec = dict(session=d, close=c, score=round(p, 3), strong=p >= 0.60, features={k: round(v, 5) for k, v in f.items()},
           paper=("BUY SPY shares at the close, sell at the next open" if p >= 0.60 else "no position (score below 0.60)"), result=None)
print(json.dumps(rec, indent=1))
led = here.parent / "overnight" / "ledger.jsonl"
if not any(json.loads(l).get("session") == d for l in open(led)) if led.exists() else True:
    with open(led, "a") as fh: fh.write(json.dumps(rec) + "\n")
