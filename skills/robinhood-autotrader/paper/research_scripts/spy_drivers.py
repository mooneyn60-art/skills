"""What moves SPY the most, and how. Contemporaneous influence (R², beta) of each driver on SPY's daily move,
on the opening gap, and how that changed 2006-15 vs 2016-26. Data: daily_ohlcv.json (SPY + 14 stocks),
world_daily.json ([open, close]: DAX, FTSE, Nikkei, HSI, KOSPI, ASX, VIX, ES), fred_macro.json (10y-2y), fomc_dates.json."""
import json, math, bisect, statistics as st
from pathlib import Path
H = Path(__file__).resolve().parent.parent / "history"
px = json.load(open(H / "daily_ohlcv.json")); W = json.load(open(H / "world_daily.json"))
fred = json.load(open(H / "fred_macro.json"))["series"]["T10Y2Y"]; fomc = set(json.load(open(H / "fomc_dates.json"))["scheduled"])
D = sorted(px["SPY"])
def r(s, i): a, b = px[s].get(D[i - 1]), px[s].get(D[i]); return math.log(b[3] / a[3]) if a and b else None
def w(n, d, k=1): v = W[n].get(d); return v[k] if v else None
def corr(x, y):
    mx, my = st.mean(x), st.mean(y); sx = math.sqrt(sum((a - mx) ** 2 for a in x)); sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy) if sx and sy else float("nan")
def beta(x, y): mx, my = st.mean(x), st.mean(y); return sum((a - mx) * (b - my) for a, b in zip(x, y)) / sum((a - mx) ** 2 for a in x)
OUT = {}
def stat(name, pairs, per):
    pairs = [(a, b) for a, b in pairs if a is not None and b is not None]
    if len(pairs) < 50: return
    x, y = [p[0] for p in pairs], [p[1] for p in pairs]; c = corr(x, y)
    OUT.setdefault(name, {})[per] = dict(n=len(pairs), corr=round(c, 3), r2=round(c * c, 3), beta=round(beta(x, y), 3))
for lo, hi, per in ((1, None, "2006-15"), (None, None, "2016-26")):
    idx = [i for i in range(1, len(D)) if (D[i] < "2016") == (per == "2006-15")]
    spy = {i: r("SPY", i) for i in idx}
    for s in [k for k in px if k != "SPY"]: stat(f"{s} same day", [(r(s, i), spy[i]) for i in idx], per)
    def wret(n, i): a, b = w(n, D[i - 1]), w(n, D[i]); return math.log(b / a) if a and b else None
    stat("VIX change same day", [(wret("vix", i), spy[i]) for i in idx], per)
    for n in ("dax", "ftse", "nikkei", "hsi", "kospi", "asx"): stat(f"{n.upper()} same day", [(wret(n, i), spy[i]) for i in idx], per)
    def dcurve(i): a, b = fred.get(D[i - 1]), fred.get(D[i]); return (b - a) if a is not None and b is not None else None
    stat("10y-2y curve change", [(dcurve(i), spy[i]) for i in idx], per)
    # what moves the OPEN (gap): Asia's day and Europe's morning, known before 9:30
    gap = {i: math.log(px["SPY"][D[i]][0] / px["SPY"][D[i - 1]][3]) for i in idx}
    for n in ("nikkei", "hsi", "kospi", "asx"):
        stat(f"{n.upper()} day -> SPY gap", [((math.log(w(n, D[i]) / w(n, D[i], 0)) if w(n, D[i]) and w(n, D[i], 0) else None), gap[i]) for i in idx], per)
    stat("DAX open gap -> SPY gap", [((math.log(w("dax", D[i], 0) / w("dax", D[i - 1])) if w("dax", D[i], 0) and w("dax", D[i - 1]) else None), gap[i]) for i in idx], per)
    stat("SPY yesterday -> SPY gap", [(spy.get(i - 1), gap[i]) for i in idx], per)
    # mega-cap concentration: share of SPY's daily variance explained by the 5 megas' average move
    mega = ("AAPL", "MSFT", "NVDA", "GOOGL", "AMZN")
    stat("5 mega-caps (avg) same day", [((st.mean([r(s, i) for s in mega]) if all(r(s, i) is not None for s in mega) else None), spy[i]) for i in idx], per)
    rest = [k for k in px if k not in mega + ("SPY",)]
    stat("9 other stocks (avg) same day", [((st.mean([r(s, i) for s in rest]) if all(r(s, i) is not None for s in rest) else None), spy[i]) for i in idx], per)
    # events: size of the move on Fed days vs other days
    ab = lambda sel: st.mean(abs(spy[i]) for i in idx if sel(D[i]) and spy[i] is not None) * 100
    OUT.setdefault("FOMC day |move| vs other days (%)", {})[per] = dict(fomc=round(ab(lambda d: d in fomc), 3), other=round(ab(lambda d: d not in fomc), 3))
by = sorted(((k, v) for k, v in OUT.items() if "2016-26" in v and "r2" in v["2016-26"]), key=lambda kv: -kv[1]["2016-26"]["r2"])
print(f"{'driver':32s} {'R² 06-15':>9s} {'R² 16-26':>9s} {'beta 16-26':>10s}  (R² = share of SPY's move it explains)")
for k, v in by:
    a = v.get("2006-15", {}); print(f"{k:32s} {a.get('r2', float('nan')):9.3f} {v['2016-26']['r2']:9.3f} {v['2016-26']['beta']:10.3f}")
print("FOMC:", OUT["FOMC day |move| vs other days (%)"])
json.dump(OUT, open(Path(__file__).with_name("spy_drivers.json"), "w"), indent=1)
