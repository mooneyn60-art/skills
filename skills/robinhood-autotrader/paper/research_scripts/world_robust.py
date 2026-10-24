"""Robustness for world_markets.py findings: split halves for (a) Asia own-news -> SPY open-to-close,
(b) big Asia down days -> SPY open-to-close, (c) DAX morning -> SPY open-to-close by year."""
import json, math, sys
from pathlib import Path
H = Path(__file__).resolve().parent.parent / "history"
W = json.load(open(H / "world_daily.json")); spy = json.load(open(H / "daily_ohlcv.json"))["SPY"]; SD = sorted(spy)
import bisect
def prev(ks, d): i = bisect.bisect_left(ks, d) - 1; return ks[i] if i >= 0 else None
KS = {n: sorted(v) for n, v in W.items()}
def corr(x, y):
    n = len(x); mx, my = sum(x) / n, sum(y) / n; sx = math.sqrt(sum((a - mx) ** 2 for a in x) / n); sy = math.sqrt(sum((b - my) ** 2 for b in y) / n)
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / n / (sx * sy)
tc = lambda c, n: c * math.sqrt((n - 2) / (1 - c * c))
rows = []
for k in range(2, len(SD)):
    d = SD[k]; o, h, l, c = spy[d][:4]; pc = spy[SD[k - 1]][3]
    r = dict(d=d, oc=c / o - 1, gap=o / pc - 1, prev=pc / spy[SD[k - 2]][3] - 1)
    for n in ("hsi", "asx", "nikkei", "kospi"):
        if d in W[n]:
            p = prev(KS[n], d)
            if p: r[n] = W[n][d][1] / W[n][p][1] - 1
    rows.append(r)
for n in ("hsi", "asx", "kospi"):
    sub = [r for r in rows if n in r]
    x = [r["prev"] for r in sub]; y = [r[n] for r in sub]; mx, my = sum(x) / len(x), sum(y) / len(y)
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sum((a - mx) ** 2 for a in x)
    for r in sub: r[n + "_own"] = r[n] - b * r["prev"]
    for lab, s2 in (("2006-15", [r for r in sub if r["d"] < "2016"]), ("2016-26", [r for r in sub if r["d"] >= "2016"])):
        c = corr([r[n + "_own"] for r in s2], [r["oc"] for r in s2])
        print(f"{n} own news -> SPY open-to-close {lab}: corr {c:+.3f} (t {tc(c, len(s2)):+.1f}, n={len(s2)})")
    # tradeable form: top/bottom 20% of own-news days -> SPY open-to-close
    srt = sorted(sub, key=lambda r: r[n + "_own"]); q = len(srt) // 5
    lo, hi = srt[:q], srt[-q:]
    print(f"   bottom 20% own-news days: SPY open-to-close {100*sum(r['oc'] for r in lo)/q:+.3f}%  | top 20%: {100*sum(r['oc'] for r in hi)/q:+.3f}%  | spread {100*(sum(r['oc'] for r in hi)-sum(r['oc'] for r in lo))/q:+.3f}% per day")
for lab, s2 in (("2006-15", [r for r in rows if r["d"] < "2016"]), ("2016-26", [r for r in rows if r["d"] >= "2016"])):
    big = [r for r in s2 if "nikkei" in r and r["nikkei"] < -0.02]
    print(f"Nikkei down >2% {lab}: n={len(big)} SPY open-to-close avg {100*sum(r['oc'] for r in big)/len(big):+.3f}% ({100*sum(r['oc']>0 for r in big)/len(big):.0f}% up) vs base {100*sum(r['oc'] for r in s2)/len(s2):+.3f}% ({100*sum(r['oc']>0 for r in s2)/len(s2):.0f}%)")
    gd = [r for r in s2 if r["gap"] < -0.006]
    print(f"   any SPY gap down >0.6% {lab}: n={len(gd)} open-to-close {100*sum(r['oc'] for r in gd)/len(gd):+.3f}% ({100*sum(r['oc']>0 for r in gd)/len(gd):.0f}% up)  | gap down >0.6% WITH Nikkei down >2%: ", end="")
    both = [r for r in gd if "nikkei" in r and r["nikkei"] < -0.02]
    print(f"n={len(both)} {100*sum(r['oc'] for r in both)/max(1,len(both)):+.3f}% ({100*sum(r['oc']>0 for r in both)/max(1,len(both)):.0f}% up)")
