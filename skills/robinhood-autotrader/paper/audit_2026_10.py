#!/usr/bin/env python3
"""
Monthly expectancy audit, 2026-10-01 (routines/MONTHLY_EXPECTANCY_AUDIT.md).
Prints data only (R14.1). No dollar balances printed (R13): R, %, ratios.

Q1  expectancy of closed live trades in R, SOFI SHARES EXCLUDED (carve-out);
    split by exit category, source and holding period. Option trades from
    2026-09-24 on are the R17 slot book, reported separately.
Q2a shadow book vs SPY (paper/shadow/nav.csv).
Q3  rule cost, R6 circuit breaker (2 stop-outs in 5 days -> 3-day pause) and
    R6 drawdown halt, under TODAY's TARS-1 config, vs not having them.
Q4  decay: the most recent 12 months of data, TARS-1 vs SPY vs equal-weight
    buy-and-hold of the 14 names, and the 200-day above/below spread.

PREDICTIONS (written before the first run, committed with this file):
  Q3: removing the breaker changes full-period CAGR by less than +/-0.5pp;
      removing the halt changes it by less than +/-1pp. Both near-free.
  Q4: in the last 12 months (a mostly calm, rising market) TARS-1 trails
      SPY by 2-8pp, and trails equal-weight buy-and-hold too; the 200-day
      above-minus-below spread over 12 monthly samples is |t| < 2.
Usage: python3 paper/audit_2026_10.py
"""
import csv, json, math, os
from datetime import datetime

from engine import load, simulate, Config, C

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = dict(use_ma_fast=False, prox=None, exit_on="slow", stop_pct=0.08,
            raise_mode="trail", trail_pct=0.20, cap_pct=0.20, cap_abs=1e12,
            cash_floor=0.15, whole_shares=True, slip=0.0005)


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def mt(xs):
    n = len(xs)
    if n == 0:
        return "n= 0"
    m = sum(xs) / n
    if n < 3:
        return f"n={n:>2} mean {m:+.2f}R  total {sum(xs):+.2f}R"
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
    return f"n={n:>2} mean {m:+.2f}R  total {sum(xs):+.2f}R  t={m / (sd / math.sqrt(n)):+.2f}" if sd else f"n={n} mean {m:+.2f}R"


def exit_cat(r):
    r = str(r)
    if "trail" in r:
        return "trail"
    if "stop" in r:
        return "stop"
    if "R2_fail" in r or "trend" in r:
        return "trend/R2 exit"
    if "expired" in r:
        return "expired"
    return "user_closed / discretionary"


def q1():
    rows = {}
    for line in open(os.path.join(HERE, "trades.jsonl")):
        if line.strip():
            d = json.loads(line)
            rows[d["id"].replace("-CORRECTION", "")] = d
    trades, slot, sofi = [], [], 0
    for d in rows.values():
        if (d.get("account") != "live" or d.get("realized_pnl") is None or not d.get("planned_risk")
                or d.get("exit_reason") in (None, "not_taken") or not d.get("closed")):
            continue
        opt = str(d.get("instrument", "")).startswith("option") or "contract" in d
        if d.get("symbol") == "SOFI" and not opt:
            sofi += 1
            continue
        t = dict(id=d["id"], r=d["realized_pnl"] / d["planned_risk"], src=str(d.get("strategy")),
                 ex=exit_cat(d.get("exit_reason")),
                 hold=(ts(d["closed"]) - ts(d["opened"])).total_seconds() / 86400 if d.get("opened") else None)
        if opt and d["closed"] >= "2026-09-24":
            slot.append(t)
        else:
            trades.append(t)
    print(f"=== Q1 expectancy, paper/trades.jsonl, closed live trades with planned_risk ===")
    print(f"  SOFI share trades excluded (carve-out): {sofi}")
    print(f"  ALL (ex-SOFI shares, ex-slot): {mt([t['r'] for t in trades])}")
    for key, lab in (("ex", "exit category"), ("src", "source")):
        groups = {}
        for t in trades:
            groups.setdefault(t[key], []).append(t["r"])
        for g, xs in sorted(groups.items(), key=lambda kv: -len(kv[1])):
            print(f"    {lab:<14} {g:<28} {mt(xs)}")
    for lab, f in (("< 1 day", lambda h: h is not None and h < 1), ("1-5 days", lambda h: h is not None and 1 <= h < 5),
                   (">= 5 days", lambda h: h is not None and h >= 5)):
        print(f"    holding        {lab:<28} {mt([t['r'] for t in trades if f(t['hold'])])}")
    print(f"  R17 / option slot book (options closed 2026-09-24 on): {mt([t['r'] for t in slot])}")
    for t in slot:
        print(f"    {t['r']:+.2f}R  {t['id']}")


def q2a():
    print("\n=== Q2a shadow book vs SPY, paper/shadow/nav.csv ===")
    rows = list(csv.DictReader(open(os.path.join(HERE, "shadow", "nav.csv"))))
    seen, uniq = set(), []
    for r in rows:
        if r["date"] not in seen:
            seen.add(r["date"]); uniq.append(r)
    for r in uniq:
        print(f"  {r['date']}  tars1 {float(r['tars1']):.4f}  trend_only {float(r['trend_only']):.4f}  spy {float(r['spy']):.4f}")
    a, b = uniq[0], uniq[-1]
    print(f"  {a['date']} to {b['date']} ({len(uniq)} rows): tars1 {(float(b['tars1']) / float(a['tars1']) - 1) * 100:+.2f}%  "
          f"spy {(float(b['spy']) / float(a['spy']) - 1) * 100:+.2f}%")


def cagr_dd(res):
    eq = res["equity"]
    y = len(eq) / 252
    peak, dd = eq[0], 0.0
    for v in eq:
        peak = max(peak, v); dd = min(dd, v / peak - 1)
    return (eq[-1] / eq[0]) ** (1 / y) - 1, dd


def q3(dates, bars, syms):
    print("\n=== Q3 rule cost: R6 breaker and halt under today's TARS-1 config (engine, 14 names, 2006-2026) ===")
    for lab, kw in (("TARS-1 as is", {}), ("no circuit breaker", dict(breaker_stops=99)),
                    ("no drawdown halt", dict(halt_drawdown=None)),
                    ("neither", dict(breaker_stops=99, halt_drawdown=None))):
        res = simulate(Config(name=lab, **BASE, **kw), dates, bars, syms)
        c, d = cagr_dd(res)
        print(f"  {lab:<20} CAGR {c * 100:6.2f}%  maxDD {d * 100:6.1f}%  trades {len(res['trades'])}  "
              f"breaker-blocked days {res['blocked_breaker']}  halts {len(res['halts'])}")


def q4(dates, bars, syms):
    print("\n=== Q4 decay: most recent 12 months ===")
    start = dates[-253]
    res = simulate(Config(name="12m", start_date=start, **BASE), dates, bars, syms)
    eq = res["equity"]
    i0 = dates.index(start)
    spy = bars["SPY"][-1][C] / bars["SPY"][i0][C] - 1
    ew = sum(bars[s][-1][C] / bars[s][i0][C] - 1 for s in syms) / len(syms)
    print(f"  {start} to {dates[-1]}: TARS-1 {(eq[-1] / eq[0] - 1) * 100:+.2f}%  SPY {spy * 100:+.2f}%  "
          f"equal-weight hold of 14 {ew * 100:+.2f}%  (price returns; TARS-1 trades {len(res['trades'])})")
    spreads = []
    seen = set()
    for i in range(i0, len(dates) - 21):
        if dates[i][:7] in seen:
            continue
        seen.add(dates[i][:7])
        up, dn = [], []
        for s in syms:
            sma = sum(b[C] for b in bars[s][i - 199:i + 1]) / 200
            f = bars[s][i + 21][C] / bars[s][i][C] - 1
            (up if bars[s][i][C] > sma else dn).append(f)
        if up and dn:
            spreads.append(sum(up) / len(up) - sum(dn) / len(dn))
    n = len(spreads)
    m = sum(spreads) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in spreads) / (n - 1))
    print(f"  200-day above-minus-below fwd 21d spread, monthly: n={n} mean {m * 100:+.2f}pp t={m / (sd / math.sqrt(n)):+.2f}")


def main():
    q1()
    q2a()
    dates, bars, syms = load()
    q3(dates, bars, syms)
    q4(dates, bars, syms)


if __name__ == "__main__":
    main()
