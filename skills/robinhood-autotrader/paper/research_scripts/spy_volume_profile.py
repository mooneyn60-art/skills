"""Volume profile on SPY, 5-min Robinhood bars (Feb 23 - Oct 20 2026, 167 sessions; spy_5min.json).
Same tests as volume_profile.py (prior-day VAL/VAH 1:1 fade to POC vs a random-level control; the 80% rule),
plus, for options: from the first touch of each level, the SPY move over the next 30/60 min, and the touch split
before/after 10:30 ET (our no-entry window). Halves = first/second 83 sessions."""
import json, random, statistics as st
from pathlib import Path
from collections import defaultdict
from volume_profile import profile, race
H = Path(__file__).resolve().parent.parent / "history"
random.seed(11)
bars = json.load(open(H / "spy_5min.json")); S = defaultdict(list)
for t in sorted(bars): S[t[:10]].append((t, *bars[t]))
days = sorted(S); OUT = {}
def et_min(t, d):  # minutes after 9:30 ET (first bar of the day = 0)
    f = S[d][0][0]; return (int(t[11:13]) * 60 + int(t[14:16])) - (int(f[11:13]) * 60 + int(f[14:16]))
res = defaultdict(list)
for n, (d0, d1) in enumerate(zip(days, days[1:])):
    half = "H1" if n < len(days) // 2 else "H2"
    prev = [b[1:] for b in S[d0]]; today = S[d1]; tb = [b[1:] for b in today]
    val, poc, vah = profile(prev); op = tb[0][0]
    for name, lvl, long in (("VAL long", val, True), ("VAH short", vah, False), ("POC from above, long", poc, True), ("POC from below, short", poc, False)):
        if (long and op <= lvl) or (not long and op >= lvl): continue
        k = next((i for i, b in enumerate(tb) if (b[2] <= lvl if long else b[1] >= lvl)), None)
        if k is None: continue
        tgt = poc if "PO" not in name else (vah if long else val)
        dist = abs(tgt - lvl)
        if dist <= 0: continue
        late = et_min(today[k][0], d1) >= 60
        r = race(tb[k + 1:], lvl, lvl + dist if long else lvl - dist, lvl - dist if long else lvl + dist)
        sgn = 1 if long else -1
        m30 = sgn * (tb[min(k + 6, len(tb) - 1)][3] / lvl - 1) * 1e4; m60 = sgn * (tb[min(k + 12, len(tb) - 1)][3] / lvl - 1) * 1e4
        for tag in (name, f"{name} {half}", f"{name} {'after' if late else 'before'} 10:30"):
            res[tag].append((r, m30, m60))
        g = abs(op - lvl) * random.uniform(0.5, 1.5); cl = op - g if long else op + g
        kc = next((i for i, b in enumerate(tb) if (b[2] <= cl if long else b[1] >= cl)), None)
        if kc is not None:
            rc = race(tb[kc + 1:], cl, cl + dist if long else cl - dist, cl - dist if long else cl + dist)
            m30c = sgn * (tb[min(kc + 6, len(tb) - 1)][3] / cl - 1) * 1e4
            res["control " + name].append((rc, m30c, 0))
    if op < val or op > vah:
        long = op < val; ins = 0
        for i, b in enumerate(tb):
            ins = ins + 1 if val < b[3] < vah else 0
            if ins == 2:
                e = b[3]; tgt = vah if long else val
                stop = min(x[2] for x in tb[:i + 1]) if long else max(x[1] for x in tb[:i + 1])
                r = race(tb[i + 1:], e, tgt, stop); rr = abs(tgt - e) / abs(e - stop) if e != stop else 0
                res["80% rule"].append((r, rr, 0)); res[f"80% rule {half}"].append((r, rr, 0)); break
for k, v in sorted(res.items()):
    hits = [x[0] for x in v if x[0] is not None]
    o = dict(n=len(v), hit=round(100 * st.mean(hits), 1) if hits else None)
    if k.startswith("80%"): o["median_reward_to_risk"] = round(st.median(x[1] for x in v), 2)
    else: o["mean_30m_bp"] = round(st.mean(x[1] for x in v), 1); o["mean_60m_bp"] = round(st.mean(x[2] for x in v), 1)
    OUT[k] = o; print(f"{k:38s} {o}")
json.dump(OUT, open(Path(__file__).with_name("spy_volume_profile.json"), "w"), indent=1)
