"""Dealer-hedging ideas the options crowd watches, tested on real SPY intraday bars (164 days, 2026).
1) Intraday momentum (Gao, Han, Li & Zhou 2018 JFE; Baltussen, Da, Lammers & Martens 2021 JFE):
   return from prior close to 10:00 predicts the last half hour (15:30-16:00) return.
2) Strike pinning (Ni, Pearson & Poteshman 2005): with daily SPY expiries, does price get pulled to the
   nearest $1 strike into the close more than chance?"""
import math, statistics as st, sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from intraday_deep import days, DAYS, OOS_END  # reuses the loader (prints its report first; ignore)
def at(b, t):  # close of the last bar starting before minute t
    s = [x for x in b if x["t"] < t]; return s[-1]["c"] if s else None
rows = []
for k in range(1, len(DAYS)):
    b, pb = days[DAYS[k]], days[DAYS[k - 1]]
    pc = pb[-1]["c"]; c1000 = at(b, 600); c1530 = at(b, 930); c1500 = at(b, 900); cl = b[-1]["c"]
    if None in (c1000, c1530, c1500): continue
    rows.append(dict(d=DAYS[k], r1=c1000 / pc - 1, r12=c1530 / c1000 - 1, rl=cl / c1530 - 1, c1500=c1500, c1530=c1530, cl=cl))
def corr(x, y):
    mx, my = st.mean(x), st.mean(y); sx, sy = st.pstdev(x), st.pstdev(y)
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / len(x) / (sx * sy)
print("\n==== 1) INTRADAY MOMENTUM: first move (prev close -> 10:00) vs last half hour (15:30 -> 16:00)")
for lab, rs in (("all", rows), ("out-of-sample Feb-Sep1", [r for r in rows if r["d"] < OOS_END]), ("Sep-Oct", [r for r in rows if r["d"] >= OOS_END])):
    x = [r["r1"] for r in rs]; y = [r["rl"] for r in rs]; c = corr(x, y); t = c * math.sqrt((len(rs) - 2) / (1 - c * c))
    same = sum((a > 0) == (b > 0) for a, b in zip(x, y)); big = [r for r in rs if abs(r["r1"]) > 0.003]
    sb = sum((r["r1"] > 0) == (r["rl"] > 0) for r in big)
    pnl = [math.copysign(1, r["r1"]) * r["rl"] * r["c1530"] for r in rs]
    print(f"  {lab:24s} n={len(rs):3d} corr {c:+.2f} (t {t:+.1f})  same sign {100*same/len(rs):.0f}%  | first move >0.3%: {sb}/{len(big)} same sign | trade last 30 min in first-move direction: avg {st.mean(pnl):+.3f} pts/day")
x = [r["r12"] for r in rows]; y = [r["rl"] for r in rows]; c = corr(x, y)
print(f"  midday (10:00->15:30) vs last half hour: corr {c:+.2f}")
print("\n==== 2) PINNING to the nearest $1 strike")
d15 = [abs(r["c1500"] - round(r["c1500"])) for r in rows]; d30 = [abs(r["c1530"] - round(r["c1530"])) for r in rows]; dc = [abs(r["cl"] - round(r["cl"])) for r in rows]
print(f"  mean distance to nearest whole dollar: 15:00 {st.mean(d15):.3f} | 15:30 {st.mean(d30):.3f} | close {st.mean(dc):.3f}  (pure chance = 0.250)")
near = [r for r in rows if abs(r["c1530"] - round(r["c1530"])) <= 0.15]
stay = sum(1 for r in near if round(r["cl"]) == round(r["c1530"]) and abs(r["cl"] - round(r["cl"])) <= 0.25)
print(f"  within 0.15 of a strike at 15:30: {len(near)} days; closed within 0.25 of that same strike {stay} ({100*stay/max(1,len(near)):.0f}%)")
far = [r for r in rows if abs(r["c1530"] - round(r["c1530"])) > 0.35]
moved = [abs(r["cl"] - round(r["cl"])) for r in far]
print(f"  between strikes at 15:30 (>0.35 away): {len(far)} days; close distance {st.mean(moved):.3f} vs 0.25 chance")
print(f"  last-30-min move size median {st.median(abs(r['cl']-r['c1530']) for r in rows):.2f} pts (so a 0.25 'pin' window is small vs the move)")
