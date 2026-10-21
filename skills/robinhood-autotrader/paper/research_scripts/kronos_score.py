"""Score kronos_test.py output. Direction hit rate vs 50% and vs naive baselines, the 'trade its side' gross return,
top-third-confidence subset, range forecast correlation vs a trailing-range baseline, halves."""
import json, statistics as st
from pathlib import Path
def corr(a, b):
    ma, mb = st.mean(a), st.mean(b); sa = sum((x - ma) ** 2 for x in a) ** .5; sb = sum((y - mb) ** 2 for y in b) ** .5
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb) if sa and sb else 0
def block(rs, pk, ak, label):
    if len(rs) < 20: return None
    sig = [(r[pk] - r["c0"]) / r["c0"] for r in rs]; act = [(r[ak] - r["c0"]) / r["c0"] for r in rs]
    hit = sum((s > 0) == (a > 0) for s, a in zip(sig, act) if a != 0) / sum(a != 0 for a in act)
    side = st.mean((1 if s > 0 else -1) * a for s, a in zip(sig, act)) * 1e4
    up = sum(a > 0 for a in act) / len(act)
    order = sorted(range(len(rs)), key=lambda j: -abs(sig[j]))[: len(rs) // 3]
    hit3 = sum((sig[j] > 0) == (act[j] > 0) for j in order) / len(order)
    o = dict(n=len(rs), hit=round(100 * hit, 1), always_up=round(100 * up, 1), side_bp=round(side, 1), top_third_hit=round(100 * hit3, 1),
             ic=round(corr(sig, act), 3), range_corr=round(corr([r["prng"] for r in rs], [r["arng"] for r in rs]), 3),
             baseline_range_corr=round(corr([r["trng"] for r in rs], [r["arng"] for r in rs]), 3))
    print(f"{label:28s} {o}"); return o
OUT = {}; here = Path(__file__).parent
if (here / "kronos_intraday.json").exists():
    R = json.load(open(here / "kronos_intraday.json")); days = sorted({r["day"] for r in R}); mid = days[len(days) // 2]
    for hz in ("30", "60"):
        OUT[f"SPY +{hz}m all"] = block(R, "p" + hz, "a" + hz, f"SPY +{hz}m all")
        OUT[f"SPY +{hz}m H1"] = block([r for r in R if r["day"] < mid], "p" + hz, "a" + hz, f"SPY +{hz}m H1")
        OUT[f"SPY +{hz}m H2"] = block([r for r in R if r["day"] >= mid], "p" + hz, "a" + hz, f"SPY +{hz}m H2")
        for t in ("10:30", "12:00", "13:30"): OUT[f"SPY +{hz}m {t}"] = block([r for r in R if r["t"] == t], "p" + hz, "a" + hz, f"SPY +{hz}m from {t}")
if (here / "kronos_daily.json").exists():
    R = json.load(open(here / "kronos_daily.json"))
    for sym in sorted({r["sym"] for r in R}):
        rs = [r for r in R if r["sym"] == sym]; m = len(rs) // 2
        OUT[f"{sym} 1d all"] = block(rs, "p1", "a1", f"{sym} next day")
        OUT[f"{sym} 1d H1"] = block(rs[:m], "p1", "a1", f"{sym} next day H1"); OUT[f"{sym} 1d H2"] = block(rs[m:], "p1", "a1", f"{sym} next day H2")
    hold = [r for r in R if r["sym"] != "SPY"]; OUT["holdings pooled 1d"] = block(hold, "p1", "a1", "7 holdings pooled next day")
json.dump(OUT, open(here / "kronos_scores.json", "w"), indent=1)
