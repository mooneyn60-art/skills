#!/usr/bin/env python3
"""
Agenda item 8, test M2: rebuild the evidence behind R15 and measure it with
(a) the original daily name-day observations, (b) month-clustered standard
errors, (c) monthly non-overlapping samples. Prints data only (R14.1).
Design and prediction: research/2026-09-25_MULTIPLE_TESTING.md.

Definitions follow research/2026-09-23_VIX_CONDITIONAL_REVERSAL.md:
ranging = Wilder ADX(14) < 20; range position = (close - 60d low) /
(60d high - 60d low) using daily highs/lows; bottom quartile <= 0.25, top
>= 0.75; forward return = close 21 trading days later / close - 1.
VIX: paper/history/vix_weekly.json, the latest weekly value dated at least
7 calendar days before the day (so a week's close is never used before the
week has ended). The original note's exact VIX alignment is not recorded;
this is the conservative choice.
Usage: python3 paper/test_multiple_testing_r15.py
"""
import bisect, json, math, os
from datetime import date, timedelta

from engine import load, O, H, L, C

HERE = os.path.dirname(os.path.abspath(__file__))
VIX = json.load(open(os.path.join(HERE, "history", "vix_weekly.json")))
VK = sorted(VIX)


def vix_on(d):
    cutoff = (date.fromisoformat(d) - timedelta(days=7)).isoformat()
    i = bisect.bisect_right(VK, cutoff) - 1
    return VIX[VK[i]] if i >= 0 else None


def adx_series(b, n=14):
    """Wilder ADX. Returns list aligned with bars (None until defined)."""
    out = [None] * len(b)
    tr_s = pdm_s = ndm_s = None
    dx = []
    adx = None
    for t in range(1, len(b)):
        h, l, pc = b[t][H], b[t][L], b[t - 1][C]
        up, dn = h - b[t - 1][H], b[t - 1][L] - l
        tr = max(h - l, abs(h - pc), abs(l - pc))
        pdm = up if up > dn and up > 0 else 0.0
        ndm = dn if dn > up and dn > 0 else 0.0
        if t <= n:
            tr_s = (tr_s or 0) + tr
            pdm_s = (pdm_s or 0) + pdm
            ndm_s = (ndm_s or 0) + ndm
            if t < n:
                continue
        else:
            tr_s = tr_s - tr_s / n + tr
            pdm_s = pdm_s - pdm_s / n + pdm
            ndm_s = ndm_s - ndm_s / n + ndm
        if tr_s == 0:
            continue
        pdi, ndi = 100 * pdm_s / tr_s, 100 * ndm_s / tr_s
        dx.append(0.0 if pdi + ndi == 0 else 100 * abs(pdi - ndi) / (pdi + ndi))
        if len(dx) == n:
            adx = sum(dx) / n
        elif len(dx) > n:
            adx = (adx * (n - 1) + dx[-1]) / n
        out[t] = adx
    return out


def welch_t(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    va = sum((x - ma) ** 2 for x in a) / (len(a) - 1)
    vb = sum((x - mb) ** 2 for x in b) / (len(b) - 1)
    return ma - mb, (ma - mb) / math.sqrt(va / len(a) + vb / len(b))


def clustered_t(a, b, ca, cb):
    """Difference in means with standard errors clustered by month."""
    ma, mb = sum(a) / len(a), sum(b) / len(b)

    def var_of_mean(xs, cs, m):
        g = {}
        for x, c in zip(xs, cs):
            g[c] = g.get(c, 0.0) + (x - m)
        G = len(g)
        return sum(v * v for v in g.values()) / (len(xs) ** 2) * G / (G - 1), G
    va, ga = var_of_mean(a, ca, ma)
    vb, gb = var_of_mean(b, cb, mb)
    return ma - mb, (ma - mb) / math.sqrt(va + vb), ga, gb


def main():
    dates, bars, syms = load()
    adx = {s: adx_series(bars[s]) for s in syms}
    buckets = {"<15": (0, 15), "15-20": (15, 20), "20-25": (20, 25), "25+": (25, 1e9)}
    obs = {k: ([], [], [], []) for k in buckets}  # bottom, top, bottom-month, top-month
    first_of_month = set()
    seen = set()
    for i, d in enumerate(dates):
        if d[:7] not in seen:
            seen.add(d[:7])
            first_of_month.add(i)
    monthly = {k: [] for k in buckets}
    for i in range(60, len(dates) - 21):
        d = dates[i]
        v = vix_on(d)
        if v is None:
            continue
        k = next(k for k, (lo, hi) in buckets.items() if lo <= v < hi)
        bot_m, top_m = [], []
        for s in syms:
            b = bars[s]
            a = adx[s][i]
            if a is None or a >= 20:
                continue
            hi = max(x[H] for x in b[i - 59:i + 1])
            lo = min(x[L] for x in b[i - 59:i + 1])
            if hi <= lo:
                continue
            pos = (b[i][C] - lo) / (hi - lo)
            fwd = b[i + 21][C] / b[i][C] - 1
            if pos <= 0.25:
                obs[k][0].append(fwd); obs[k][2].append(d[:7]); bot_m.append(fwd)
            elif pos >= 0.75:
                obs[k][1].append(fwd); obs[k][3].append(d[:7]); top_m.append(fwd)
        if i in first_of_month and bot_m and top_m:
            monthly[k].append(sum(bot_m) / len(bot_m) - sum(top_m) / len(top_m))

    print("source: paper/history/daily_stocks.json (14 symbols), vix_weekly.json; ranging = ADX(14)<20")
    print("(a) daily name-day observations, bottom-quartile minus top-quartile fwd 21d return, Welch t")
    print("(b) same observations, standard errors clustered by calendar month")
    print("(c) first trading day of each month only; per-month spread; t across months")
    for k in buckets:
        bot, top, cb, ct = obs[k]
        if len(bot) < 3 or len(top) < 3:
            continue
        sa, ta = welch_t(bot, top)
        sb, tb, gb, gt = clustered_t(bot, top, cb, ct)
        m = monthly[k]
        if len(m) >= 3:
            mm = sum(m) / len(m)
            sd = math.sqrt(sum((x - mm) ** 2 for x in m) / (len(m) - 1))
            tc = f"{mm * 100:+6.2f}pp t={mm / (sd / math.sqrt(len(m))):+5.2f} months={len(m)}"
        else:
            tc = f"months={len(m)} (too few)"
        print(f"  VIX {k:<6} (a) {sa * 100:+6.2f}pp t={ta:+5.2f} n={len(bot)}+{len(top)}   "
              f"(b) t={tb:+5.2f} clusters={gb}/{gt}   (c) {tc}")


if __name__ == "__main__":
    main()
