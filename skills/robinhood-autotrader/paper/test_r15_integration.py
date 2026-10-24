#!/usr/bin/env python3
"""
One-shot: does TARS-1 WITH R15 beat TARS-1 WITHOUT R15?
Routine: routines/ONESHOT_R15_INTEGRATION.md. Prints data only (R14.1).

TARS-1 as it stands (paper/engine.py): symmetric 200-day entry and exit
(exit_on="slow", no 50-day, no near-the-high rule), 8% stop, breakeven at
+8%, 20% trail, 20% position cap (no flat cap), 15% cash floor, whole
shares, 5bp slippage; R5 sector cap and R6 breaker at engine defaults.
R15: engine Config(r15=True): weekly VIX (vix_weekly.json, value dated >= 7
calendar days earlier) >= 25 -> ranging (ADX14 < 20) names in the bottom
quartile of their 60-day range are eligible with the 200-day gate
suspended, tagged, and exempt from the trend exit. VIX 20-25 changes nothing.

PREDICTION (written before the first run, committed with this file):
  R15 fires rarely (VIX >= 25 on roughly 15% of weeks, mostly 2008, 2020,
  2022) and the book is usually full of trend positions when it does, so:
  - full-period CAGR difference within +/-1pp; max drawdown within +/-3pp;
  - R15 version ahead in 3-6 of 9 walk-forward windows (no consistent edge);
  - with the megacaps dropped, the difference stays within +/-1pp;
  - R15 entries: a few dozen over 20 years.
  Expected verdict: NO MEANINGFUL DIFFERENCE. Not worse, not better.

Usage: python3 paper/test_r15_integration.py
"""
import math

from engine import load, simulate, Config

MEGA = {"AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"}
BASE = dict(use_ma_fast=False, prox=None, exit_on="slow", stop_pct=0.08,
            raise_mode="trail", trail_pct=0.20, cap_pct=0.20, cap_abs=1e12,
            cash_floor=0.15, whole_shares=True, slip=0.0005)


def stats(res):
    eq = res["equity"]
    yrs = len(eq) / 252.0
    cagr = (eq[-1] / eq[0]) ** (1 / yrs) - 1
    peak, mdd = eq[0], 0.0
    for v in eq:
        peak = max(peak, v)
        mdd = min(mdd, v / peak - 1)
    r = [eq[i] / eq[i - 1] - 1 for i in range(1, len(eq))]
    m = sum(r) / len(r)
    sd = math.sqrt(sum((x - m) ** 2 for x in r) / (len(r) - 1))
    return cagr, mdd, (m / sd * math.sqrt(252) if sd else float("nan")), len(res["trades"]), res["r15_entries"]


def row(label, res):
    c, d, s, n, k = stats(res)
    print(f"  {label:<22} CAGR {c * 100:6.2f}%  maxDD {d * 100:6.1f}%  Sharpe {s:5.2f}  "
          f"trades {n:>4}  R15 entries {k:>3}")
    return c


def pair(title, dates, bars, syms, **kw):
    print(title)
    a = row("TARS-1", simulate(Config(name="TARS-1", **BASE, **kw), dates, bars, syms))
    b = row("TARS-1 + R15", simulate(Config(name="TARS-1+R15", r15=True, **BASE, **kw), dates, bars, syms))
    print(f"  difference (with R15 minus without): {(b - a) * 100:+.2f}pp CAGR")
    return a, b


def main():
    dates, bars, syms = load()
    print(f"source: paper/history/daily_stocks.json, {len(syms)} names, {dates[0]} to {dates[-1]}; "
          f"vix_weekly.json; paper/engine.py")
    pair("\nFULL PERIOD", dates, bars, syms)
    pair("\nSPLIT: 2006-2015", dates, bars, syms, end_date="2015-12-31")
    pair("\nSPLIT: 2016-2026", dates, bars, syms, start_date="2016-01-01")
    pair("\nMEGACAPS DROPPED (AAPL MSFT NVDA GOOGL AMZN), full period",
         dates, bars, [s for s in syms if s not in MEGA])

    print("\nWALK-FORWARD, 9 equal windows (each run fresh from its start date)")
    first = 201
    edges = [first + (len(dates) - first) * k // 9 for k in range(10)]
    wins = 0
    for k in range(9):
        a0, a1 = dates[edges[k]], dates[edges[k + 1] - 1]
        ra = simulate(Config(name="w", start_date=a0, end_date=a1, **BASE), dates, bars, syms)
        rb = simulate(Config(name="w", start_date=a0, end_date=a1, r15=True, **BASE), dates, bars, syms)
        ca, cb = stats(ra)[0], stats(rb)[0]
        wins += cb > ca
        print(f"  {a0} to {a1}: without {ca * 100:6.2f}%  with {cb * 100:6.2f}%  "
              f"diff {(cb - ca) * 100:+6.2f}pp  R15 entries {rb['r15_entries']}")
    print(f"  windows where the R15 version had the higher CAGR: {wins} of 9")


if __name__ == "__main__":
    main()
