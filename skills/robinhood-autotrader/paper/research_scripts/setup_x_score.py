"""Connections: do the slot's setups work better when the day-score model agrees? (walk-forward scores only)
S1 proxy on 20y daily: gap up >= 0.6% -> open-to-close. S2: the exact traded rules from s2_context.py (164 days)."""
import json, collections, statistics as st, io, contextlib
from pathlib import Path
import numpy as np
here = Path(__file__).resolve().parent
g = {"__file__": str(here / "predict_lab.py")}
exec(compile(open(here / "predict_lab.py").read().split("R = {}")[0], "pl", "exec"), g)
o = g["walk"]("day", "fo", drop=("asia", "daxgap", "pc", "dvix", "vixrel"))
score = {r["d"]: p for r, p in zip(g["rows"], o["P"]["logit"]) if p == p}
out = {}
print("S1 proxy: gap up >= 0.6%, open->close (%), by day score")
for lab, f in (("score < 0.50", lambda p: p < 0.5), ("0.50-0.55", lambda p: 0.5 <= p < 0.55), ("score >= 0.55", lambda p: p >= 0.55)):
    for per, sel in (("2011-18", lambda d: d < "2019"), ("2019-26", lambda d: d >= "2019")):
        v = [100 * r["day"] for r in g["rows"] if r["d"] in score and sel(r["d"]) and r["fo"]["gap"] >= 0.006 and f(score[r["d"]])]
        if v: print(f"  {lab:14s} {per}: n {len(v):3d} up {100*sum(x>0 for x in v)/len(v):4.1f}% avg {st.mean(v):+.3f}%"); out[f"S1 {lab} {per}"] = dict(n=len(v), up=round(100*sum(x>0 for x in v)/len(v),1), avg=round(st.mean(v),3))
s = {"__file__": str(here / "s2_context.py")}
src = open(here / "s2_context.py").read().split("def show(")[0]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, "s2", "exec"), s)
base = [r for r in s["rows"] if r["up"]]
print("\nS2 as traded (SPY pts/trade), by day score")
for lab, f in (("score < 0.50", lambda p: p is not None and p < 0.5), ("score >= 0.50", lambda p: p is not None and p >= 0.5), ("no score", None)):
    v = [r["res"] for r in base if f(score.get(r["d"]))] if lab != "no score" else [r["res"] for r in base if r["d"] not in score]
    if v: print(f"  {lab:14s} n {len(v):3d} win {100*sum(x>0 for x in v)/len(v):4.1f}% avg {st.mean(v):+.3f}"); out[f"S2 {lab}"] = dict(n=len(v), win=round(100*sum(x>0 for x in v)/len(v),1), avg=round(st.mean(v),3))
json.dump(out, open(here / "setup_x_score.json", "w"), indent=1)
