#!/usr/bin/env python3
"""
Monthly expectancy audit, 2026-11-01 (routines/MONTHLY_EXPECTANCY_AUDIT.md).
Built from audit_2026_10.py; Q3 changed (R2 exit confirmation), Q2 added (live NAV index).
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
  Q1: expectancy of closed live trades (ex-SOFI shares, ex-slot) still
      negative, mean between -0.5R and 0R; no split clears |t| 2.
  Q2: live NAV index since 2026-10-01 (deposit-stripped) is BEHIND SPY by
      more than 10pp; the shadow TARS-1 book is behind SPY by 2-8pp.
  Q3: requiring 2 (or 3) consecutive closes below the 200-day before the
      R2 trend exit changes TARS-1 full-period CAGR by less than +/-1pp,
      with the sign flipping across the 9 walk-forward windows (3-6 of 9).
  Q4: last 12 months: TARS-1 trails SPY by 0-8pp; the 200-day spread
      |t| < 2.
Usage: python3 paper/audit_2026_11.py
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
        try:
            pr, rp = float(d["planned_risk"]), float(d["realized_pnl"])
        except (TypeError, ValueError):
            print(f"  skipped (non-numeric risk or pnl): {d['id']}")
            continue
        if pr <= 0:
            continue
        opt = str(d.get("instrument", "")).startswith("option") or "contract" in d
        if d.get("symbol") == "SOFI" and not opt:
            sofi += 1
            continue
        t = dict(id=d["id"], r=rp / pr, src=str(d.get("strategy")),
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


def q2_live():
    print("\n=== Q2 live NAV index vs SPY, paper/nav_index.csv (deposits stripped) ===")
    rows = list(csv.DictReader(open(os.path.join(HERE, "nav_index.csv"))))
    a, b = rows[0], rows[-1]
    nv = float(b["nav_index"]) / float(a["nav_index"]) - 1
    sp = float(b["spy_close"]) / float(a["spy_close"]) - 1
    print(f"  {a['date']} to {b['date']} ({len(rows)} rows): live {nv * 100:+.2f}%  SPY {sp * 100:+.2f}%  gap {(nv - sp) * 100:+.2f}pp")
    peak, dd = 0.0, 0.0
    for r in rows:
        v = float(r["nav_index"]); peak = max(peak, v); dd = min(dd, v / peak - 1)
    print(f"  live max drawdown in the window {dd * 100:.1f}%")


def cagr_dd(res):
    eq = res["equity"]
    y = len(eq) / 252
    peak, dd = eq[0], 0.0
    for v in eq:
        peak = max(peak, v); dd = min(dd, v / peak - 1)
    return (eq[-1] / eq[0]) ** (1 / y) - 1, dd


def q3(dates, bars, syms):
    print("\n=== Q3 rule cost: R2 trend exit after 1 (live) vs 2 vs 3 consecutive closes below the 200-day ===")
    mega = {"AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"}
    for lab, kw in (("full", {}), ("2006-2015", dict(end_date="2015-12-31")), ("2016-2026", dict(start_date="2016-01-01"))):
        out = []
        for k in (1, 2, 3):
            c, d = cagr_dd(simulate(Config(name=f"c{k}", exit_confirm=k, breaker_loss_only=True, **BASE, **kw), dates, bars, syms))
            out.append(f"confirm={k}: CAGR {c * 100:6.2f}% DD {d * 100:6.1f}%")
        print(f"  {lab:<10} " + " | ".join(out))
    nm = [s for s in syms if s not in mega]
    out = []
    for k in (1, 2, 3):
        c, d = cagr_dd(simulate(Config(name=f"c{k}", exit_confirm=k, breaker_loss_only=True, **BASE), dates, bars, nm))
        out.append(f"confirm={k}: CAGR {c * 100:6.2f}% DD {d * 100:6.1f}%")
    print(f"  {'no megacaps':<10} " + " | ".join(out))
    first = 201
    edges = [first + (len(dates) - first) * k // 9 for k in range(10)]
    for k in (2, 3):
        cells, w = [], 0
        for j in range(9):
            a0, a1 = dates[edges[j]], dates[edges[j + 1] - 1]
            ca = cagr_dd(simulate(Config(name="w", start_date=a0, end_date=a1, breaker_loss_only=True, **BASE), dates, bars, syms))[0]
            cb = cagr_dd(simulate(Config(name="w", start_date=a0, end_date=a1, exit_confirm=k, breaker_loss_only=True, **BASE), dates, bars, syms))[0]
            cells.append(f"{(cb - ca) * 100:+.1f}"); w += cb > ca
        print(f"  walk-forward confirm={k} minus confirm=1 (pp): {' '.join(cells)} -> ahead {w} of 9")


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
    q2_live()
    dates, bars, syms = load()
    q3(dates, bars, syms)
    q4(dates, bars, syms)


if __name__ == "__main__":
    main()
