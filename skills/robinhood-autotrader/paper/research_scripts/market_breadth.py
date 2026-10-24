"""
Market breadth (share of the 14 large caps above their 200-day) as a regime
signal for next-month SPY return and volatility, alone and alongside VIX.

RESEARCH_AGENDA item 11 / research/2026-10-01_MARKET_BREADTH.md.
Predictions committed BEFORE this ran (commit 5613181). Prints raw numbers
only, no hardcoded conclusions (R14).

One observation per month-end; forward window = next 21 trading days, so
samples don't overlap. Each month is one observation (clustered by design).
"""
import json
import math
import sys
from pathlib import Path
from statistics import mean, pstdev

sys.path.insert(0, str(Path(__file__).resolve().parent))
from momentum_reversal import load_universe, sma, month_end_dates, LARGE_CAP_FILE  # noqa: E402

BASE = Path(__file__).resolve().parents[2]
VIX_FILE = BASE / "paper" / "history" / "vix_weekly.json"
SPLIT = "2016-06"
H = 21


def t_of_mean(xs):
    n = len(xs)
    if n < 3:
        return float("nan")
    sd = pstdev(xs) * math.sqrt(n / (n - 1))
    return mean(xs) / (sd / math.sqrt(n)) if sd > 0 else float("nan")


def welch(a, b):
    na, nb = len(a), len(b)
    if na < 3 or nb < 3:
        return float("nan"), float("nan")
    va = pstdev(a) ** 2 * na / (na - 1)
    vb = pstdev(b) ** 2 * nb / (nb - 1)
    d = mean(a) - mean(b)
    return d, d / math.sqrt(va / na + vb / nb)


def corr_t(x, y):
    n = len(x)
    mx, my = mean(x), mean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    r = sxy / math.sqrt(sxx * syy)
    t = r * math.sqrt((n - 2) / (1 - r * r))
    return r, t


def ols2(y, x1, x2):
    """y = a + b1*x1 + b2*x2; return (b1, t1, b2, t2) with classical SEs."""
    n = len(y)
    X = [[1.0, a, b] for a, b in zip(x1, x2)]
    # normal equations 3x3
    XtX = [[sum(X[k][i] * X[k][j] for k in range(n)) for j in range(3)] for i in range(3)]
    Xty = [sum(X[k][i] * y[k] for k in range(n)) for i in range(3)]
    inv = invert3(XtX)
    beta = [sum(inv[i][j] * Xty[j] for j in range(3)) for i in range(3)]
    resid = [y[k] - sum(beta[i] * X[k][i] for i in range(3)) for k in range(n)]
    s2 = sum(r * r for r in resid) / (n - 3)
    se = [math.sqrt(s2 * inv[i][i]) for i in range(3)]
    return beta[1], beta[1] / se[1], beta[2], beta[2] / se[2]


def invert3(m):
    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    return [
        [(e * i - f * h) / det, (c * h - b * i) / det, (b * f - c * e) / det],
        [(f * g - d * i) / det, (a * i - c * g) / det, (c * d - a * f) / det],
        [(d * h - e * g) / det, (b * g - a * h) / det, (a * e - b * d) / det],
    ]


def main():
    raw = json.load(open(LARGE_CAP_FILE))
    spy_dates = sorted(raw["SPY"])
    spy_c = [raw["SPY"][d][3] for d in spy_dates]
    spy_idx = {d: i for i, d in enumerate(spy_dates)}
    names = load_universe(LARGE_CAP_FILE, exclude={"SPY"})
    vix = json.load(open(VIX_FILE))
    vix_dates = sorted(vix)

    rows = []
    for d in month_end_dates(names):
        if d not in spy_idx:
            continue
        i = spy_idx[d]
        if i + H >= len(spy_c):
            continue
        above = valid = 0
        for s in names.values():
            j = s["idx"].get(d)
            if j is None:
                continue
            m = sma(s["C"], j, 200)
            if m is None:
                continue
            valid += 1
            above += s["C"][j] > m
        if valid < 10:
            continue
        breadth = above / valid
        fwd = spy_c[i + H] / spy_c[i] - 1
        lr = [math.log(spy_c[k + 1] / spy_c[k]) for k in range(i, i + H)]
        vol = pstdev(lr) * math.sqrt(252)
        vprev = [v for v in vix_dates if v <= d]
        if not vprev:
            continue
        rows.append({"m": d[:7], "b": breadth, "ret": fwd, "vol": vol, "vix": vix[vprev[-1]]})

    print(f"months: {len(rows)}  ({rows[0]['m']} .. {rows[-1]['m']})")
    print(f"breadth mean {mean(r['b'] for r in rows):.3f}, "
          f"min {min(r['b'] for r in rows):.3f}, max {max(r['b'] for r in rows):.3f}")

    def block(label, rs):
        b = [r["b"] for r in rs]
        ret = [r["ret"] for r in rs]
        vol = [r["vol"] for r in rs]
        vx = [r["vix"] for r in rs]
        srt = sorted(b)
        lo_cut = srt[len(srt) // 3]
        hi_cut = srt[2 * len(srt) // 3]
        lo = [r for r in rs if r["b"] <= lo_cut]
        hi = [r for r in rs if r["b"] >= hi_cut]
        print(f"\n[{label}] n={len(rs)}  low-third breadth<= {lo_cut:.2f} (n={len(lo)}), "
              f"high-third >= {hi_cut:.2f} (n={len(hi)})")
        r1, t1 = corr_t(b, ret)
        d1, tw1 = welch([r["ret"] for r in lo], [r["ret"] for r in hi])
        print(f"  RETURN  corr(breadth,fwd)={r1:+.3f} t={t1:+.2f} | "
              f"low-high mean diff={d1*100:+.2f}pp t={tw1:+.2f}")
        r2, t2 = corr_t(b, vol)
        d2, tw2 = welch([r["vol"] for r in lo], [r["vol"] for r in hi])
        print(f"  VOL     corr(breadth,vol)={r2:+.3f} t={t2:+.2f} | "
              f"low-high vol diff={d2*100:+.2f}pp t={tw2:+.2f}")
        r3, t3 = corr_t(vx, vol)
        print(f"  VIX alone corr(vix,vol)={r3:+.3f} t={t3:+.2f}")
        bv, tv, bb, tb = ols2(vol, vx, b)
        print(f"  VOL ~ VIX + breadth: VIX coef={bv:+.4f} t={tv:+.2f} | "
              f"breadth coef={bb:+.4f} t={tb:+.2f}")
        rr, tr_ = corr_t(vx, b)
        print(f"  corr(vix, breadth)={rr:+.3f}")

    block("ALL", rows)
    block(f"pre-{SPLIT}", [r for r in rows if r["m"] < SPLIT])
    block(f"post-{SPLIT}", [r for r in rows if r["m"] >= SPLIT])


if __name__ == "__main__":
    main()
