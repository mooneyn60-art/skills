"""IBIT day score: can anything known at the US open (13:30 UTC) predict BTC's US-session move (13:30->20:00 UTC),
the window an IBIT option trades in? Features from 3y hourly BTC/ETH + BTC daily + SPY/VIX daily (previous day).
Walk-forward: expanding window, retrained monthly, first 250 sessions are training only. Also: does the overnight
range predict the session's range (sizing stops, like VIX for SPY)?"""
import json, math, bisect, statistics as st, datetime as dt
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
H = Path(__file__).resolve().parent.parent / "history"
hb = json.load(open(H / "crypto" / "btc_hourly.json")); he = json.load(open(H / "crypto" / "eth_hourly.json"))
bd = json.load(open(H / "crypto" / "btc_daily.json")); BD = sorted(bd)
spy = json.load(open(H / "daily_ohlcv.json"))["SPY"]; SK = sorted(spy)
vix = json.load(open(H / "world_daily.json"))["vix"]; VK = sorted(vix)
def o(h, d, hh): v = h.get(f"{d}T{hh:02d}:00Z"); return v[0] if v else None
def before(keys, d): i = bisect.bisect_left(keys, d) - 1; return keys[i] if i >= 0 else None
days = sorted({k[:10] for k in hb}); rows = []
for i in range(1, len(days)):
    d, p = days[i], days[i - 1]
    x = dt.date.fromisoformat(d)
    if x.weekday() > 4: continue
    b20, b1330, b20n = o(hb, p, 20), o(hb, d, 13), o(hb, d, 20)
    e20, e1330 = o(he, p, 20), o(he, d, 13)
    if not all((b20, b1330, b20n, e20, e1330)): continue
    hrs = [hb.get(f"{p}T{h:02d}:00Z") for h in range(20, 24)] + [hb.get(f"{d}T{h:02d}:00Z") for h in range(0, 13)]
    hrs = [v for v in hrs if v]
    if len(hrs) < 12: continue
    on_rng = (max(v[1] for v in hrs) - min(v[2] for v in hrs)) / b20
    db = before(BD, d); j = BD.index(db) if db else 0
    if j < 200: continue
    cl = [bd[BD[k]][3] for k in range(j - 200, j + 1)]
    sp = before(SK, d); sp2 = before(SK, sp) if sp else None; vv = before(VK, d)
    if not (sp and sp2 and vv): continue
    sess = [hb.get(f"{d}T{h:02d}:00Z") for h in range(13, 20)]; sess = [v for v in sess if v]
    s_rng = (max(v[1] for v in sess) - min(v[2] for v in sess)) / b1330 if sess else None
    rows.append(dict(d=d, y=100 * (b20n / b1330 - 1), s_rng=s_rng, f=dict(
        on=b1330 / b20 - 1, eth_rel=(e1330 / e20 - 1) - (b1330 / b20 - 1), on_rng=on_rng,
        r1=cl[-1] / cl[-2] - 1, r5=cl[-1] / cl[-6] - 1, r20=cl[-1] / cl[-21] - 1,
        d20=cl[-1] / st.mean(cl[-20:]) - 1, d200=cl[-1] / st.mean(cl[-200:]) - 1,
        vol7=st.pstdev([cl[k] / cl[k - 1] - 1 for k in range(-7, 0)]),
        spy1=spy[sp][3] / spy[sp2][3] - 1, vix=vix[vv][1], dow=x.weekday())))
names = list(rows[0]["f"]); X = np.array([[r["f"][k] for k in names] for r in rows]); Y = np.array([r["y"] for r in rows])
P = np.full(len(rows), np.nan); months = sorted({r["d"][:7] for r in rows})
for m in months:
    te = np.array([r["d"][:7] == m for r in rows]); tr = np.array([r["d"][:7] < m for r in rows])
    if tr.sum() < 250 or te.sum() == 0: continue
    mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-12
    P[te] = LogisticRegression(C=0.1, max_iter=2000).fit((X[tr] - mu) / sd, (Y[tr] > 0).astype(int)).predict_proba((X[te] - mu) / sd)[:, 1]
ok = ~np.isnan(P); idx = np.where(ok)[0]; half = idx[len(idx) // 2]
OUT = {"n_sessions": len(rows), "oos_sessions": int(ok.sum())}
print(f"sessions {len(rows)}, out-of-sample {ok.sum()} ({rows[idx[0]]['d']} .. {rows[idx[-1]]['d']})")
for lab, sel in (("OOS first half", ok & (np.arange(len(rows)) < half)), ("OOS second half", ok & (np.arange(len(rows)) >= half))):
    for lo, hi in ((0, .45), (.45, .55), (.55, 1.01)):
        m = sel & (P >= lo) & (P < hi); y = Y[m]
        if m.sum(): print(f"  {lab:16s} p[{lo:.2f},{hi:.2f}) n {m.sum():3d}  BTC session {y.mean():+.2f}%  up {100*np.mean(y>0):3.0f}%")
        OUT[f"{lab} {lo}-{hi}"] = dict(n=int(m.sum()), mean=round(float(y.mean()), 3) if m.sum() else None, up=round(100 * float(np.mean(y > 0)), 1) if m.sum() else None)
mu, sd = X.mean(0), X.std(0) + 1e-12
w = LogisticRegression(C=0.1, max_iter=2000).fit((X - mu) / sd, (Y > 0).astype(int)).coef_[0]
OUT["weights"] = {k: round(float(v), 3) for k, v in sorted(zip(names, w), key=lambda z: -abs(z[1]))}; print("  weights:", OUT["weights"])
# sizing: overnight range vs session range (like VIX for SPY)
pairs = [(r["f"]["on_rng"], r["s_rng"]) for r in rows if r["s_rng"]]
xs, ys = [p[0] for p in pairs], [p[1] for p in pairs]; mx, my = st.mean(xs), st.mean(ys)
corr = sum((a - mx) * (b - my) for a, b in pairs) / math.sqrt(sum((a - mx) ** 2 for a in xs) * sum((b - my) ** 2 for b in ys))
q = sorted(xs); t1, t2 = q[len(q) // 3], q[2 * len(q) // 3]
buck = {n: [b for a, b in pairs if f(a)] for n, f in (("quiet night", lambda a: a < t1), ("normal night", lambda a: t1 <= a < t2), ("wild night", lambda a: a >= t2))}
OUT["range"] = dict(corr=round(corr, 2), **{k: round(100 * st.mean(v), 2) for k, v in buck.items()}, cut1=round(100 * t1, 2), cut2=round(100 * t2, 2))
print(f"  overnight range -> session range: corr {corr:.2f}; session range after quiet/normal/wild nights: " + ", ".join(f"{k} {100*st.mean(v):.2f}%" for k, v in buck.items()) + f" (cuts {100*t1:.2f}% / {100*t2:.2f}%)")
json.dump(OUT, open(Path(__file__).with_name("ibit_dayscore.json"), "w"), indent=1)
