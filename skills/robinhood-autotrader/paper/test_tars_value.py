#!/usr/bin/env python3
"""
Agenda item 18: is TARS adding value, and how much data before we'd know?
Prints data only (R14.1). Design: research/2026-09-24_IS_TARS_ADDING_VALUE.md.

A  live closed trades (paper/trades.jsonl) by owner, in R
B  backtest of the current ruleset (approximation, see the note) vs SPY:
   alpha, tracking error, information ratio, years needed for t = 2
C  trades needed for t = 2 from the backtest's R distribution
Usage: python3 paper/test_tars_value.py
"""
import json, math, os

from engine import load, simulate, Config, C

HERE = os.path.dirname(os.path.abspath(__file__))


def mt(xs):
    n = len(xs)
    m = sum(xs) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
    return n, m, sd, m / (sd / math.sqrt(n))


def main():
    print("=== A live closed trades, paper/trades.jsonl ===")
    rows = {}
    for line in open(os.path.join(HERE, "trades.jsonl")):
        if line.strip():
            d = json.loads(line)
            rows[d["id"].replace("-CORRECTION", "")] = d
    groups = {}
    for d in rows.values():
        if (d.get("account") == "live" and d.get("realized_pnl") is not None and d.get("planned_risk")
                and d.get("exit_reason") not in (None, "not_taken")):
            owner = "TARS" if str(d.get("strategy") or "").startswith("TARS") else "Nolan"
            groups.setdefault(owner, []).append(d["realized_pnl"] / d["planned_risk"])
    for k, xs in sorted(groups.items()):
        n, m, sd, t = mt(xs)
        print(f"  {k:<6} n={n:>2}  mean {m:+.2f}R  sd {sd:.2f}R  t={t:+.2f}")
    alls = [x for xs in groups.values() for x in xs]
    n, m, sd, t = mt(alls)
    print(f"  all    n={n:>2}  mean {m:+.2f}R  sd {sd:.2f}R  t={t:+.2f}")
    print("  (rows without planned_risk are excluded: R cannot be computed for them)")

    print("\n=== B backtest, current ruleset approximation vs SPY (price returns, 14 names) ===")
    dates, bars, syms = load()
    cfg = Config(name="current approx", use_ma_fast=False, prox=None, exit_on="slow",
                 trail_pct=0.20, cap_abs=1e12)
    res = simulate(cfg, dates, bars, syms)
    eq = res["equity"]
    off = len(dates) - len(eq)
    spy = [bars["SPY"][off + i][C] for i in range(len(eq))]
    act = [(eq[i] / eq[i - 1]) - (spy[i] / spy[i - 1]) for i in range(1, len(eq))]
    n, m, sd, t = mt(act)
    alpha, te = m * 252, sd * math.sqrt(252)
    ir = alpha / te
    yrs = len(eq) / 252
    cagr = (eq[-1] / eq[0]) ** (1 / yrs) - 1
    scagr = (spy[-1] / spy[0]) ** (1 / yrs) - 1
    print(f"  {dates[off]} to {dates[-1]}, {yrs:.1f} yrs: strategy CAGR {cagr * 100:.2f}%  SPY CAGR {scagr * 100:.2f}%")
    print(f"  mean active return {alpha * 100:+.2f}%/yr  tracking error {te * 100:.1f}%/yr  "
          f"IR {ir:+.2f}  t over the whole backtest {t:+.2f}")
    if ir > 0:
        print(f"  years of live data for t=2 at this IR: {(2 / ir) ** 2:.0f}")
    for lab, a, b in (("first half", 1, len(eq) // 2), ("second half", len(eq) // 2, len(eq) - 1)):
        seg = act[a - 1:b]
        _, ms, sds, ts = mt(seg)
        print(f"    {lab:<11} active {ms * 252 * 100:+.2f}%/yr  IR {ms / sds * math.sqrt(252):+.2f}  t={ts:+.2f}")

    print("\n=== C trades needed, backtest trades (R = trade return / 8%) ===")
    rs = [((tr[2] / tr[1]) - 1) / 0.08 for tr in res["trades"]]
    n, m, sd, t = mt(rs)
    print(f"  backtest trades n={n}  mean {m:+.2f}R  sd {sd:.2f}R  t={t:+.2f}")
    if m > 0:
        print(f"  trades needed for t=2 at this mean and sd: {(2 * sd / m) ** 2:.0f}")
    print(f"  trades needed for t=2 if the true edge were +0.10R: {(2 * sd / 0.10) ** 2:.0f}; "
          f"+0.25R: {(2 * sd / 0.25) ** 2:.0f}")


if __name__ == "__main__":
    main()
