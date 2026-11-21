#!/usr/bin/env python3
"""
R6 circuit breaker cost through the four hurdles. Prints data only (R14.1).
Design and prediction: research/2026-10-11_R6_BREAKER_COST.md (committed first).

A = live loss-only breaker, B = no breaker; drawdown halt on in both.
Usage: python3 paper/test_r6_breaker.py
"""
import math

from engine import load, simulate, Config

BASE = dict(use_ma_fast=False, prox=None, exit_on="slow", stop_pct=0.08,
            raise_mode="trail", trail_pct=0.20, cap_pct=0.20, cap_abs=1e12,
            cash_floor=0.15, whole_shares=True, slip=0.0005)
A = dict(breaker_loss_only=True)
B = dict(breaker_stops=99)


def stats(res):
    eq = res["equity"]
    yrs = len(eq) / 252.0
    peak, mdd = eq[0], 0.0
    for v in eq:
        peak = max(peak, v)
        mdd = min(mdd, v / peak - 1)
    return (eq[-1] / eq[0]) ** (1 / yrs) - 1, mdd


def run(dates, bars, syms, extra, **kw):
    return simulate(Config(name="x", **BASE, **extra, **kw), dates, bars, syms)


def pair(label, dates, bars, syms, **kw):
    ra, rb = run(dates, bars, syms, A, **kw), run(dates, bars, syms, B, **kw)
    (ca, da), (cb, db) = stats(ra), stats(rb)
    print(f"  {label:<34} breaker CAGR {ca * 100:6.2f}% DD {da * 100:6.1f}% | none CAGR {cb * 100:6.2f}% "
          f"DD {db * 100:6.1f}% | diff {(cb - ca) * 100:+6.2f}pp CAGR, {(db - da) * 100:+5.1f}pp DD | "
          f"blocked days {ra['blocked_breaker']}")
    return ra, rb, cb - ca


def main():
    dates, bars, syms = load()
    print(f"source: paper/history/daily_stocks.json, {len(syms)} names, {dates[0]} to {dates[-1]}; paper/engine.py")
    print("\nFULL PERIOD")
    ra, rb, _ = pair("full", dates, bars, syms)
    old = run(dates, bars, syms, {})
    c, d = stats(old)
    print(f"  {'reference: old any-stop breaker':<34} CAGR {c * 100:6.2f}% DD {d * 100:6.1f}% blocked days {old['blocked_breaker']}")

    ea, eb = ra["equity"], rb["equity"]
    diff = [eb[i] / eb[i - 1] - ea[i] / ea[i - 1] for i in range(1, len(ea))]
    n = len(diff)
    m = sum(diff) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in diff) / (n - 1))
    nz = sum(1 for x in diff if abs(x) > 1e-12)
    print(f"  daily return difference (none minus breaker): n={n} mean {m * 1e4:+.3f}bp t={m / (sd / math.sqrt(n)):+.2f}; "
          f"days that differ at all {nz}")

    off = len(dates) - len(ea)
    yr = {}
    for i in range(len(ea)):
        yr.setdefault(dates[off + i][:4], []).append(i)
    wins, tot = 0, 0
    parts = []
    for y, idx in sorted(yr.items()):
        i0, i1 = max(idx[0] - 1, 0), idx[-1]
        g = (eb[i1] / eb[i0]) - (ea[i1] / ea[i0])
        tot += 1
        wins += g > 1e-9
        parts.append(f"{y}:{g * 100:+.1f}")
    print(f"  calendar years, none minus breaker (pp of that year's return): {' '.join(parts)}")
    print(f"  years none ahead: {wins} of {tot}")

    print("\nSPLIT")
    pair("2006-2015", dates, bars, syms, end_date="2015-12-31")
    pair("2016-2026", dates, bars, syms, start_date="2016-01-01")

    print("\nDROP THE BIG WINNERS (cumulative), full period")
    drop = []
    for s in (["NVDA"], ["AAPL"], ["AMZN"], ["MSFT", "GOOGL"]):
        drop += s
        pair("without " + "+".join(drop), dates, bars, [x for x in syms if x not in drop])

    print("\nWALK-FORWARD, 9 equal windows (each run fresh)")
    first = 201
    edges = [first + (len(dates) - first) * k // 9 for k in range(10)]
    w = 0
    for k in range(9):
        a0, a1 = dates[edges[k]], dates[edges[k + 1] - 1]
        _, _, g = pair(f"{a0} to {a1}", dates, bars, syms, start_date=a0, end_date=a1)
        w += g > 1e-9
    print(f"  windows where no-breaker had the higher CAGR: {w} of 9")


if __name__ == "__main__":
    main()
