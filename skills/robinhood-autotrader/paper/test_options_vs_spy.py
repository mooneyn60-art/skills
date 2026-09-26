#!/usr/bin/env python3
"""
Agenda item 15: do options beat the S&P 500? Prints data only (R14.1).
Design and predictions: research/2026-09-24_OPTIONS_VS_SPY.md, committed
before this file existed.

O1/O2  CBOE PUT, BXM, BXMD vs S&P 500 total return (SPTR), month-end.
O3     Simulated BUYING of 1-month SPX options, Black-Scholes at VIX
       (and 0.9 x VIX), r = DTB3, q = SPTR-vs-SPX trailing yield,
       +1% of premium as cost, rolled every 21 trading days.
O4     This account's own closed option trades, in R.

Data: paper/history/options_indices.json (paper/fetch_options_indices.py),
paper/trades.jsonl.
Usage: python3 paper/test_options_vs_spy.py
"""
import json, math, os
from statistics import NormalDist

HERE = os.path.dirname(os.path.abspath(__file__))
SER = json.load(open(os.path.join(HERE, "history", "options_indices.json")))["series"]
N = NormalDist().cdf


def tstat(xs):
    n = len(xs)
    m = sum(xs) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
    return m, m / (sd / math.sqrt(n))


def month_ends(names, start="0000"):
    """Last date in each month on which every named series has a value.
    `start` drops early sparse points (PUT has 6 scattered values before 2007,
    which would otherwise be read as monthly returns spanning years)."""
    common = sorted(d for d in set.intersection(*(set(SER[n]) for n in names)) if d >= start)
    out = {}
    for d in common:
        out[d[:7]] = d
    return [out[k] for k in sorted(out)]


def rf_on(d):
    ks = SER["DTB3"]
    while d not in ks:  # step back to the latest published rate
        y, m, dd = map(int, d.split("-"))
        dd -= 1
        if dd == 0:
            m, dd = m - 1, 28
            if m == 0:
                y, m = y - 1, 12
        d = f"{y:04d}-{m:02d}-{dd:02d}"
    return ks[d] / 100


def summarize(label, rets, rfs):
    n = len(rets)
    g = 1.0
    peak, mdd = 1.0, 0.0
    for r in rets:
        g *= 1 + r
        peak = max(peak, g)
        mdd = min(mdd, g / peak - 1)
    cagr = g ** (12 / n) - 1
    m = sum(rets) / n
    sd = math.sqrt(sum((r - m) ** 2 for r in rets) / (n - 1))
    ex = [r - f for r, f in zip(rets, rfs)]
    sharpe = (sum(ex) / n) / sd * math.sqrt(12)
    print(f"  {label:<10} CAGR {cagr * 100:6.2f}%  vol {sd * math.sqrt(12) * 100:5.1f}%  "
          f"Sharpe {sharpe:5.2f}  maxDD {mdd * 100:6.1f}%")


def annual(dates, rets):
    by = {}
    for d, r in zip(dates, rets):
        by[d[:4]] = by.get(d[:4], 1.0) * (1 + r)
    return {y: v - 1 for y, v in by.items()}


def compare(name, bench="SPTR", start="0000"):
    me = month_ends([name, bench], start)
    d0 = me[0]
    dates, a, b, rfs = [], [], [], []
    for p, c in zip(me, me[1:]):
        dates.append(c)
        a.append(SER[name][c] / SER[name][p] - 1)
        b.append(SER[bench][c] / SER[bench][p] - 1)
        rfs.append(rf_on(p) / 12)
    print(f"\n{name} vs {bench}: {len(a)} months, {d0} to {me[-1]}")
    summarize(name, a, rfs)
    summarize(bench, b, rfs)
    diff = [x - y for x, y in zip(a, b)]
    m, t = tstat(diff)
    print(f"  monthly difference {name}-{bench}: mean {m * 100:+.3f}pp  t={t:+.2f}")
    h = len(diff) // 2
    for lab, sl in (("first half", slice(0, h)), ("second half", slice(h, None))):
        m2, t2 = tstat(diff[sl])
        print(f"    {lab:<11} {dates[sl][0]} to {dates[sl][-1]}: mean {m2 * 100:+.3f}pp  t={t2:+.2f}")
    pos = 0
    k = len(diff)
    for w in range(9):
        seg = diff[w * k // 9:(w + 1) * k // 9]
        mw = sum(seg) / len(seg)
        pos += mw > 0
        print(f"    window {w + 1}: {dates[w * k // 9]} to {dates[(w + 1) * k // 9 - 1]}  mean {mw * 100:+.3f}pp")
    print(f"  windows where {name} beat {bench}: {pos} of 9")
    for lab, s in ((name, a), (bench, b)):
        yr = annual(dates, s)
        full = [y for y in yr if y not in (dates[0][:4], dates[-1][:4])]
        best = max(full, key=yr.get)
        worst = min(full, key=yr.get)
        keep = [yr[y] for y in full if y not in (best, worst)]
        geo = math.prod(1 + x for x in keep) ** (1 / len(keep)) - 1
        print(f"    {lab:<5} full calendar years {len(full)}, drop best {best} ({yr[best] * 100:+.1f}%) "
              f"and worst {worst} ({yr[worst] * 100:+.1f}%): geometric mean {geo * 100:.2f}%/yr")


def point_to_point(name, bench="SPTR", end="2006-12-29"):
    pts = sorted(d for d in SER[name] if d <= end and d in SER[bench])
    d0, d1 = pts[0], pts[-1]
    yrs = (int(d1[:4]) - int(d0[:4])) + (int(d1[5:7]) - int(d0[5:7])) / 12
    for s in (name, bench):
        c = (SER[s][d1] / SER[s][d0]) ** (1 / yrs) - 1
        print(f"  {s:<5} {d0} -> {d1}: CAGR {c * 100:.2f}% ({yrs:.1f} yrs, 2 points only)")


def bs(S, K, T, r, q, sig, call):
    d1 = (math.log(S / K) + (r - q + sig * sig / 2) * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    if call:
        return S * math.exp(-q * T) * N(d1) - K * math.exp(-r * T) * N(d2)
    return K * math.exp(-r * T) * N(-d2) - S * math.exp(-q * T) * N(-d1)


def buying(scale):
    days = sorted(set(SER["SPX"]) & set(SER["SPTR"]) & set(SER["VIX"]))
    H, T = 21, 21 / 252
    cost = 0.01
    legs = {"ATM call": (1.00, True), "5% OTM call": (1.05, True), "ATM put": (1.00, False)}
    per = {k: [] for k in legs}
    eq1 = eq2 = bench = 1.0
    path = []
    for i in range(252, len(days) - H, H):
        d, e = days[i], days[i + H]
        S0, S1 = SER["SPX"][d], SER["SPX"][e]
        r = math.log(1 + rf_on(d))
        tr = math.log(SER["SPTR"][d] / SER["SPTR"][days[i - 252]])
        pr = math.log(S0 / SER["SPX"][days[i - 252]])
        q = max(tr - pr, 0.0)
        sig = SER["VIX"][d] / 100 * scale
        for k, (mny, call) in legs.items():
            K = S0 * mny
            prem = bs(S0, K, T, r, q, sig, call) * (1 + cost)
            pay = max(S1 - K, 0) if call else max(K - S1, 0)
            per[k].append(pay / prem - 1)
        prem = bs(S0, S0, T, r, q, sig, True) * (1 + cost)
        pay = max(S1 - S0, 0)
        for lev in (1, 2):
            eq = eq1 if lev == 1 else eq2
            units = lev * eq / S0
            cash = eq - units * prem
            new = cash * math.exp(r * T) + units * pay
            if lev == 1:
                eq1 = new
            else:
                eq2 = max(new, 0.0)
        bench *= SER["SPTR"][e] / SER["SPTR"][d]
        path.append((e, eq1, eq2, bench))
    return days, per, path


def curve_stats(vals, yrs):
    peak, mdd = vals[0], 0.0
    for v in vals:
        peak = max(peak, v)
        mdd = min(mdd, v / peak - 1)
    return (vals[-1]) ** (1 / yrs) - 1, mdd


def main():
    print("source: paper/history/options_indices.json (CBOE, Yahoo ^SP500TR, FRED DTB3)")
    print("\n=== O1 PUT (daily history from 2007) ===")
    compare("PUT", start="2007-01-01")
    print("  long run before 2007, sparse CBOE points only:")
    point_to_point("PUT")
    print("\n=== O2 BXM and BXMD ===")
    compare("BXM")
    compare("BXMD")

    for scale in (1.0, 0.9):
        days, per, path = buying(scale)
        print(f"\n=== O3 BUYING, sigma = {scale} x VIX, {len(path)} rolls, "
              f"{path[0][0]} to {path[-1][0]} ===")
        for k, xs in per.items():
            s = sorted(xs)
            m, t = tstat(xs)
            worthless = sum(1 for x in xs if x <= -0.999) / len(xs)
            lose = sum(1 for x in xs if x < 0) / len(xs)
            print(f"  {k:<12} mean {m * 100:+6.1f}% of premium  t={t:+5.2f}  median {s[len(s) // 2] * 100:+6.1f}%  "
                  f"lose money {lose * 100:4.1f}%  expire worthless {worthless * 100:4.1f}%")
        yrs = len(path) * 21 / 252
        for lab, idx in (("1x calls + T-bills", 1), ("2x calls + T-bills", 2), ("S&P 500 TR", 3)):
            c, mdd = curve_stats([1.0] + [p[idx] for p in path], yrs)
            print(f"  {lab:<20} CAGR {c * 100:6.2f}%  maxDD (at roll dates) {mdd * 100:6.1f}%")
        half = len(path) // 2
        for lab, sl in (("first half", (0, half)), ("second half", (half, len(path) - 1))):
            a, b = sl
            y = (b - a) * 21 / 252
            base = path[a - 1] if a > 0 else (None, 1.0, 1.0, 1.0)
            r1 = (path[b][1] / base[1]) ** (1 / y) - 1
            r2 = (path[b][2] / base[2]) ** (1 / y) - 1 if base[2] > 0 else float("nan")
            rb = (path[b][3] / base[3]) ** (1 / y) - 1
            print(f"    {lab:<11} to {path[b][0]}: 1x {r1 * 100:6.2f}%  2x {r2 * 100:6.2f}%  S&P TR {rb * 100:6.2f}%")

    print("\n=== O4 this account's closed option trades ===")
    rows = {}
    for line in open(os.path.join(HERE, "trades.jsonl")):
        if line.strip():
            d = json.loads(line)
            rows[d["id"].replace("-CORRECTION", "")] = d
    rs = []
    for d in rows.values():
        is_opt = d.get("instrument") == "option" or "contract" in d
        if (is_opt and d.get("realized_pnl") is not None and d.get("planned_risk")
                and d.get("exit_reason") not in (None, "not_taken")):
            rs.append((d["id"], d["realized_pnl"] / d["planned_risk"]))
    for i, r in sorted(rs):
        print(f"  {r:+6.2f}R  {i}")
    if len(rs) > 2:
        m, t = tstat([r for _, r in rs])
        print(f"  n={len(rs)}  mean {m:+.2f}R  t={t:+.2f}")


if __name__ == "__main__":
    main()
