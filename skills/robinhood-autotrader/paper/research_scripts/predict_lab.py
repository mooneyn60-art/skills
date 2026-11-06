"""TARS prediction engine v1: can anything known BEFORE a session predict SPY's direction?
Targets: day session (open->close) using what is known at 9:30 ET; overnight (close->next open) using what is known at 16:00.
Walk-forward: each year is predicted by models trained only on earlier years (no peeking). Data: SPY daily 2006-2026,
world indexes / daily VIX (world_daily.json: [open, close]), Cboe equity put/call (2006-2019)."""
import json, math, datetime as dt, statistics as st
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
H = Path(__file__).resolve().parent.parent / "history"
spy = json.load(open(H / "daily_ohlcv.json"))["SPY"]; D = sorted(spy)
W = json.load(open(H / "world_daily.json"))
pc = {}
for line in open(H / "cboe_equity_putcall.csv").read().splitlines()[3:]:
    p = line.split(",")
    try: m, d, y = p[0].split("/"); pc[f"{y}-{int(m):02d}-{int(d):02d}"] = float(p[4])
    except Exception: pass
def wl(name, d, k):  # last value of index `name` strictly before date d (k=0 open, 1 close), or on d if same=True
    s = W[name]; ks = WK[name]; import bisect; i = bisect.bisect_left(ks, d) - 1
    return s[ks[i]][k] if i >= 0 else None
WK = {k: sorted(v) for k, v in W.items()}
def same(name, d, k): v = W[name].get(d); return v[k] if v else None
def third_fri(x): return x.weekday() == 4 and 15 <= x.day <= 21

rows = []
for i in range(25, len(D) - 1):
    d, dp, dn = D[i], D[i - 1], D[i + 1]
    o, h, l, c, v = spy[d]; cp = spy[dp][3]
    x = dt.date(*map(int, d.split("-")))
    sma20 = st.mean(spy[D[j]][3] for j in range(i - 20, i))
    vix = [same("vix", D[j], 1) for j in range(i - 21, i)]
    if None in vix[-2:]: continue
    vixok = [q for q in vix if q]
    asia = [same(n, d, 1) / same(n, d, 0) - 1 if same(n, d, 0) else None for n in ("nikkei", "hsi", "kospi", "asx")]
    asia = [a for a in asia if a is not None]
    dax_o, dax_pc = same("dax", d, 0), wl("dax", d, 1)
    f_open = dict(  # known at 9:30 ET on day d
        gap=o / cp - 1, r1=cp / spy[D[i - 2]][3] - 1, r5=cp / spy[D[i - 6]][3] - 1, r20=cp / spy[D[i - 21]][3] - 1,
        dist20=cp / sma20 - 1, vix=vix[-1], dvix=vix[-1] / vix[-2] - 1, vixrel=vix[-1] / st.mean(vixok) - 1,
        rng1=(spy[dp][1] - spy[dp][2]) / cp, intra1=cp / spy[dp][0] - 1,
        asia=st.mean(asia) if asia else 0.0, daxgap=(dax_o / dax_pc - 1) if dax_o and dax_pc else 0.0,
        dow=x.weekday(), opex=float(third_fri(x)), pc=pc.get(dp, float("nan")))
    on_next = spy[dn][0] / c - 1
    f_close = dict(  # known at 16:00 ET on day d
        r1=c / cp - 1, intra=c / o - 1, gap=o / cp - 1, r5=c / spy[D[i - 5]][3] - 1, dist20=c / sma20 - 1,
        vix=same("vix", d, 1) or vix[-1], dvix=(same("vix", d, 1) or vix[-1]) / vix[-1] - 1, rng=(h - l) / c,
        clv=((c - l) - (h - c)) / ((h - l) or 1), dow=x.weekday(), opex=float(third_fri(x)),
        dax=(same("dax", d, 1) / same("dax", d, 0) - 1) if same("dax", d, 0) else 0.0)
    rows.append(dict(d=d, y=int(d[:4]), fo=f_open, fc=f_close, day=c / o - 1, on=on_next))

def walk(target, fkey, drop=(), cost=0.0002, thr=0.03, years=range(2011, 2027)):
    names = [k for k in rows[0][fkey] if k not in drop]
    X = np.array([[r[fkey][k] for k in names] for r in rows], float); Y = np.array([r[target] for r in rows])
    X = np.nan_to_num(X, nan=0.0); yrs = np.array([r["y"] for r in rows])
    out = {}
    for mname, mk in (("logit", lambda: LogisticRegression(C=0.1, max_iter=2000)),
                      ("boost", lambda: HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05, max_iter=150, l2_regularization=1.0))):
        P = np.full(len(rows), np.nan)
        for Yr in years:
            tr, te = yrs < Yr, yrs == Yr
            if te.sum() == 0: continue
            mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-12
            m = mk().fit((X[tr] - mu) / sd, (Y[tr] > 0).astype(int)); P[te] = m.predict_proba((X[te] - mu) / sd)[:, 1]
        res = {}
        for lab, sel in (("2011-18", (yrs >= 2011) & (yrs <= 2018)), ("2019-26", yrs >= 2019)):
            p, yv = P[sel], Y[sel]
            acc = float(np.mean((p > 0.5) == (yv > 0)))
            base = float(np.mean(yv > 0))
            pick = np.abs(p - 0.5) > thr
            tr_ret = np.sign(p[pick] - 0.5) * yv[pick] - cost
            longonly = (p > 0.5 + thr); lo = yv[longonly] - cost
            t = lambda a: float(a.mean() / (a.std() / math.sqrt(len(a)))) if len(a) > 2 and a.std() > 0 else float("nan")
            res[lab] = dict(acc=round(100 * acc, 1), base_up=round(100 * base, 1), n_trades=int(pick.sum()),
                            trade_bp=round(1e4 * float(tr_ret.mean()), 2) if len(tr_ret) else None, t=round(t(tr_ret), 2),
                            long_only_n=int(longonly.sum()), long_bp=round(1e4 * float(lo.mean()), 2) if len(lo) else None, long_t=round(t(lo), 2),
                            all_days_bp=round(1e4 * float(yv.mean()), 2))
        out[mname] = res
        if mname == "logit":
            m = LogisticRegression(C=0.1, max_iter=2000).fit((X - X.mean(0)) / (X.std(0) + 1e-12), (Y > 0).astype(int))
            out["weights"] = {n: round(float(w), 3) for n, w in sorted(zip(names, m.coef_[0]), key=lambda z: -abs(z[1]))}
        out.setdefault("P", {})[mname] = P
    return out

R = {}
for name, tgt, fk in (("DAY SESSION (open->close), known at 9:30", "day", "fo"), ("OVERNIGHT (close->next open), known at 16:00", "on", "fc")):
    o = walk(tgt, fk); P = o.pop("P"); R[name] = o
    print(f"\n=== {name} ===  (bp = basis points per trade, 1bp = 0.01%; cost 2bp)")
    for m in ("logit", "boost"):
        for lab, r in o[m].items(): print(f"  {m:5s} {lab}: acc {r['acc']}% (days up {r['base_up']}%) | trades {r['n_trades']} avg {r['trade_bp']}bp t {r['t']} | long-only {r['long_only_n']} avg {r['long_bp']}bp t {r['long_t']} | every day {r['all_days_bp']}bp")
    print("  logit weights:", o["weights"])
json.dump(R, open(Path(__file__).with_name("predict_lab.json"), "w"), indent=1)
