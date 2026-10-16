#!/usr/bin/env python3
"""
Agenda item 14: TARS-1 vs buy-and-hold SPY after federal tax. Prints data only.
Design and prediction: research/2026-10-07_AFTER_TAX.md (committed first).

TARS-1: engine trades (exit day = 7th field), realised gains taxed each
calendar year (short-term at the ordinary rate, > 252 trading days at the
long-term rate; net losses carried forward), tax paid at year-end, which
shrinks the compounding base. SPY: taxed once on sale at the end (long-term).
Price returns on both sides. Not tax advice.
Usage: python3 paper/test_after_tax.py
"""
from engine import load, simulate, Config, C

BASE = dict(use_ma_fast=False, prox=None, exit_on="slow", stop_pct=0.08,
            raise_mode="trail", trail_pct=0.20, cap_pct=0.20, cap_abs=1e12,
            cash_floor=0.15, whole_shares=True, slip=0.0005)
SCEN = [(0.12, 0.00), (0.22, 0.15), (0.24, 0.15), (0.32, 0.15)]


def main():
    dates, bars, syms = load()
    res = simulate(Config(name="TARS-1", **BASE), dates, bars, syms)
    eq = res["equity"]
    off = len(dates) - len(eq)
    yrs = len(eq) / 252
    years = sorted({dates[off + i][:4] for i in range(len(eq))})
    # equity at each year end (last bar of the year) and start
    ye = {}
    for i in range(len(eq)):
        ye[dates[off + i][:4]] = eq[i]
    first_year = years[0]

    st = {y: 0.0 for y in years}
    lt = {y: 0.0 for y in years}
    n_lt = 0
    for tr in res["trades"]:
        s, entry, px, qty, hold, why, t = tr
        y = dates[t][:4]
        g = (px - entry) * qty
        if hold > 252:
            lt[y] += g
            n_lt += 1
        else:
            st[y] += g
    tot_st, tot_lt = sum(st.values()), sum(lt.values())
    print(f"source: paper/engine.py TARS-1, 14 names, {dates[off]} to {dates[-1]} ({yrs:.1f} yrs), price returns")
    print(f"trades {len(res['trades'])}, long-term (held > 252 days) {n_lt}; "
          f"net realised short-term gains {tot_st / eq[0]:+.2f}x start equity, long-term {tot_lt / eq[0]:+.2f}x")
    spy0, spy1 = bars["SPY"][off][C], bars["SPY"][-1][C]
    pre_tars = (eq[-1] / eq[0]) ** (1 / yrs) - 1
    pre_spy = (spy1 / spy0) ** (1 / yrs) - 1
    print(f"PRE-TAX CAGR: TARS-1 {pre_tars * 100:.2f}%   SPY {pre_spy * 100:.2f}%   gap {(pre_tars - pre_spy) * 100:+.2f}pp")

    for ordr, ltr in SCEN:
        w = 1.0
        carry_st = carry_lt = 0.0
        prev = eq[0]
        taxes = 0.0
        for y in years:
            end = ye[y]
            r = end / prev - 1
            gs, gl = st[y] / prev + carry_st, lt[y] / prev + carry_lt   # gains as a fraction of start-of-year equity
            # losses offset gains across categories
            if gs < 0 and gl > 0:
                gl, gs = max(gl + gs, 0.0), min(gl + gs, 0.0)
            elif gl < 0 and gs > 0:
                gs, gl = max(gs + gl, 0.0), min(gs + gl, 0.0)
            tax = max(gs, 0) * ordr + max(gl, 0) * ltr
            carry_st, carry_lt = min(gs, 0.0) * prev / end, min(gl, 0.0) * prev / end
            w *= (1 + r - tax)
            taxes += tax
            prev = end
        aft_tars = w ** (1 / yrs) - 1
        spy_final = (spy1 / spy0)
        aft_spy = (spy_final - ltr * (spy_final - 1)) ** (1 / yrs) - 1
        print(f"  ordinary {ordr * 100:.0f}% / long-term {ltr * 100:.0f}%:  TARS-1 after tax {aft_tars * 100:.2f}%   "
              f"SPY sold at end {aft_spy * 100:.2f}%   SPY never sold {pre_spy * 100:.2f}%   "
              f"gap vs sold SPY {(aft_tars - aft_spy) * 100:+.2f}pp   tax drag on TARS {(pre_tars - aft_tars) * 100:.2f}pp/yr")


if __name__ == "__main__":
    main()
