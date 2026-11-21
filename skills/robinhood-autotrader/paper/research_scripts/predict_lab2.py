"""TARS prediction engine v2: more connections. Adds cross-market inputs to v1 (predict_lab.py) and checks whether
the confident tails get better, then builds an intraday next-hour model for the slot's 10:30-14:30 window.
Walk-forward throughout. Run: python3 predict_lab2.py"""
import json, math, bisect, collections, statistics as st
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
here = Path(__file__).resolve().parent
g = {"__file__": str(here / "predict_lab.py")}
exec(compile(open(here / "predict_lab.py").read().split("R = {}")[0], "predict_lab", "exec"), g)
rows, walk, spy, D, H = g["rows"], g["walk"], g["spy"], g["D"], g["H"]
stk = json.load(open(H / "daily_ohlcv.json")); names = [k for k in stk if k != "SPY"]
fred = json.load(open(H / "fred_macro.json"))["series"]; FK = {k: sorted(v) for k, v in fred.items()}
def fred_before(k, d, back=0):
    i = bisect.bisect_left(FK[k], d) - 1 - back; return fred[k][FK[k][i]] if i >= 0 else None
pcs = g["pc"]; PCK = sorted(pcs)
def ret(s, d, lag=1):  # close-to-close return of stock s on the trading day `lag` sessions before d
    i = bisect.bisect_left(D, d) - lag
    if i < 1: return None
    a, b = stk[s].get(D[i - 1]), stk[s].get(D[i]); return b[3] / a[3] - 1 if a and b else None
for r in rows:
    d = r["d"]; sp = ret("SPY", d)
    rs = [x for x in (ret(s, d) for s in names) if x is not None]
    r["fo2"] = dict(r["fo"],
        breadth=sum(x > 0 for x in rs) / len(rs) if rs else 0.5,
        disp=st.pstdev(rs) if len(rs) > 2 else 0.0,
        tech_rel=st.mean([x for x in (ret(s, d) for s in ("NVDA", "AAPL", "MSFT", "GOOGL", "AMZN")) if x is not None] or [0]) - (sp or 0),
        bank_rel=st.mean([x for x in (ret(s, d) for s in ("BAC", "C")) if x is not None] or [0]) - (sp or 0),
        oil_rel=(ret("XOM", d) or 0) - (sp or 0),
        curve=fred_before("T10Y2Y", d) or 0.0, dcurve=(fred_before("T10Y2Y", d) or 0) - (fred_before("T10Y2Y", d, 5) or 0),
        pc5=st.mean([pcs[k] for k in PCK[max(0, bisect.bisect_left(PCK, d) - 5):bisect.bisect_left(PCK, d)]] or [float("nan")]) if PCK[0] < d <= "2019-10-31" else float("nan"))
yrs = np.array([r["y"] for r in rows]); Y = np.array([r["day"] for r in rows])
def tails(P, label):
    out = {}
    for lo, hi in ((0, .45), (.45, .55), (.55, .6), (.6, 1.01)):
        cells = []
        for lab, sel in (("2011-18", (yrs >= 2011) & (yrs <= 2018)), ("2019-26", yrs >= 2019)):
            m = sel & (P >= lo) & (P < hi); y = Y[m]
            cells.append(dict(n=int(m.sum()), up=round(100 * float(np.mean(y > 0)), 1) if len(y) else None, bp=round(1e4 * float(y.mean()), 1) if len(y) else None))
        out[f"{lo}-{hi}"] = cells
        print(f"  {label:6s} p[{lo:.2f},{hi:.2f}) " + " | ".join(f"n {c['n']:4d} up {c['up']}% {c['bp']:+}bp" for c in cells if c['n']))
    return out
OUT = {}
drop_lite = ("asia", "daxgap", "pc", "dvix", "vixrel")
print("DAY SESSION, logit, walk-forward. v1 lite vs v1 full vs v2 (+connections)")
for lab, fk, drop in (("v1lite", "fo", drop_lite), ("v1", "fo", ()), ("v2", "fo2", ()), ("v2lite", "fo2", drop_lite + ("pc5",))):
    o = walk("day", fk, drop=drop); OUT[lab] = dict(tails=tails(o["P"]["logit"], lab), weights=o["weights"])
print("v2 weights:", OUT["v2"]["weights"])

# ---------- intraday: next hour from 10:30 (and each half hour to 13:30) ----------
ig = {"__file__": str(here / "s2_context.py")}
src = open(here / "s2_context.py").read().splitlines()
exec(compile("\n".join(src[:34]), "s2", "exec"), ig)
days, DAYS = ig["days"], ig["DAYS"]
dscore = {}  # v1 lite day score for each intraday day (walk-forward P is per row)
o = walk("day", "fo", drop=drop_lite); P = o["P"]["logit"]
for r, p in zip(rows, P): dscore[r["d"]] = p
X, Yh, dd = [], [], []
for d in DAYS:
    b = days[d]; pv = vv = 0; o0 = b[0]["o"]
    for i, x in enumerate(b):
        tp = (x["h"] + x["l"] + x["c"]) / 3; pv += tp * x["v"]; vv += x["v"]; x["vw"] = pv / vv
    i0 = bisect.bisect_left(D, d); pcl = spy[D[i0 - 1]][3] if 0 < i0 <= len(D) and D[i0 - 1] < d else None
    for t0 in (630, 660, 690, 720, 750, 780, 810):
        k = next((i for i, x in enumerate(b) if x["t"] + 5 >= t0), None)
        if k is None or k + 12 >= len(b) or k < 12: continue
        c = b[k]["c"]; hi = max(x["h"] for x in b[:k + 1]); lo = min(x["l"] for x in b[:k + 1])
        rr = [b[j]["c"] - b[j - 1]["c"] for j in range(k - 11, k + 1)]
        X.append([c / o0 - 1, (o0 / pcl - 1) if pcl else 0, (c - b[k]["vw"]) / c, (c - lo) / ((hi - lo) or 1), b[k]["c"] / b[k - 6]["c"] - 1,
                  sum(1 for q in rr if q > 0) / 12, (hi - lo) / c, t0, dscore.get(d, 0.5)])
        Yh.append(b[k + 12]["c"] - c); dd.append(d)
X, Yh, dd = np.array(X), np.array(Yh), np.array(dd)
feat = ["day_ret", "gap", "vwap_dist", "range_pos", "ret30", "upbars", "range", "time", "day_score"]
ud = sorted(set(dd)); P = np.full(len(Yh), np.nan)
for j in range(40, len(ud)):  # expanding window by day: train on all days before, predict this day
    tr, te = np.isin(dd, ud[:j]), dd == ud[j]
    mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-12
    m = LogisticRegression(C=0.1, max_iter=2000).fit((X[tr] - mu) / sd, (Yh[tr] > 0).astype(int)); P[te] = m.predict_proba((X[te] - mu) / sd)[:, 1]
ok = ~np.isnan(P); half = np.array([d < ud[(40 + len(ud)) // 2] for d in dd])
print("\nINTRADAY next hour (SPY pts), expanding walk-forward from day 41")
OUT["intraday"] = {}
for lab, sel in (("first half", ok & half), ("second half", ok & ~half)):
    for lo, hi in ((0, .4), (.4, .5), (.5, .6), (.6, 1.01)):
        m = sel & (P >= lo) & (P < hi); y = Yh[m]
        if m.sum(): print(f"  {lab:11s} p[{lo:.1f},{hi:.1f}) n {m.sum():4d} up {100*np.mean(y>0):4.1f}% avg {y.mean():+.3f} pts")
        OUT["intraday"][f"{lab} {lo}-{hi}"] = dict(n=int(m.sum()), up=round(100 * float(np.mean(y > 0)), 1) if m.sum() else None, pts=round(float(y.mean()), 3) if m.sum() else None)
mu, sd = X.mean(0), X.std(0) + 1e-12
m = LogisticRegression(C=0.1, max_iter=2000).fit((X - mu) / sd, (Yh > 0).astype(int))
print("  weights:", {f: round(float(w), 3) for f, w in sorted(zip(feat, m.coef_[0]), key=lambda z: -abs(z[1]))})
json.dump(OUT, open(here / "predict_lab2.json", "w"), indent=1)
