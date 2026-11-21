#!/usr/bin/env python3
"""
Agenda item 1: among names above their 200-day (R2 rule 1), does the latest
reported YoY growth (net income, revenue) separate forward returns?

Design is fixed in research/2026-09-23_FUNDAMENTALS_EARNINGS_TREND.md and was
committed before this file existed. Prints data only (R14.1).

Sampling: first trading day of each month. Forward return: 21 trading days.
Signal: latest 10-Q/10-K filed STRICTLY BEFORE the sample day, ignored if
filed more than 200 calendar days earlier. Spread per month = mean forward
return of GROWING names minus NOT GROWING names, among names above the
200-day; months need at least one name on each side. t = mean / (sd/sqrt(n))
across months.

Usage: python3 paper/test_fundamentals.py
"""
import json, math, os
from datetime import date

from engine import load, C

HERE = os.path.dirname(os.path.abspath(__file__))
FUND = os.path.join(HERE, "history", "fundamentals_yoy.json")
MEGACAPS = {"AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"}
FWD = 21
MA = 200
STALE_DAYS = 200


def stats(xs):
    n = len(xs)
    if n < 3:
        return n, float("nan"), float("nan")
    m = sum(xs) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))
    return n, m, m / (sd / math.sqrt(n)) if sd > 0 else float("nan")


def fmt(label, xs):
    n, m, t = stats(xs)
    return f"  {label:<26} months={n:>4}  spread={m * 100:+6.2f}pp  t={t:+5.2f}"


def signal_at(rows, day, metric):
    """Latest filing strictly before `day`, not stale. Returns growth sign or None."""
    best = None
    for r in rows:
        if r["filed"] >= day:
            break
        if r.get(metric):
            best = r
    if best is None:
        return None
    if (date.fromisoformat(day) - date.fromisoformat(best["filed"])).days > STALE_DAYS:
        return None
    g = best[metric]
    return g["cur"] > g["prior"]


def month_starts(dates):
    out, seen = [], set()
    for i, d in enumerate(dates):
        if d[:7] not in seen:
            seen.add(d[:7])
            out.append(i)
    return out


def run(dates, bars, syms, fund, metric, exclude=()):
    """Returns [(date, spread)] and coverage counts."""
    out, n_grow, n_not, n_missing = [], 0, 0, 0
    for t in month_starts(dates):
        if t < MA or t + FWD >= len(dates):
            continue
        day = dates[t]
        grow, not_grow = [], []
        for s in syms:
            if s in exclude or s not in fund:
                continue
            b = bars[s]
            closes = [x[C] for x in b[t - MA + 1:t + 1]]
            if any(c is None for c in closes) or b[t + FWD][C] is None:
                continue
            if b[t][C] <= sum(closes) / MA:
                continue
            sig = signal_at(fund[s], day, metric)
            if sig is None:
                n_missing += 1
                continue
            fwd = b[t + FWD][C] / b[t][C] - 1
            (grow if sig else not_grow).append(fwd)
        n_grow += len(grow)
        n_not += len(not_grow)
        if grow and not_grow:
            out.append((day, sum(grow) / len(grow) - sum(not_grow) / len(not_grow)))
    return out, (n_grow, n_not, n_missing)


def main():
    dates, bars, syms = load()
    fund = json.load(open(FUND))["data"]
    print(f"prices: paper/history/daily_stocks.json, {len(syms)} symbols, {dates[0]} to {dates[-1]}")
    print(f"fundamentals: paper/history/fundamentals_yoy.json (SEC EDGAR XBRL), stale after {STALE_DAYS}d")
    print(f"sample: first trading day of each month; forward {FWD} trading days; eligible = close > {MA}-day SMA")

    for tid, metric in (("T1", "net_income"), ("T2", "revenue")):
        res, (ng, nn, nm) = run(dates, bars, syms, fund, metric)
        xs = [x for _, x in res]
        print()
        print(f"{tid} {metric}: eligible name-months growing={ng}  not growing={nn}  no signal={nm}")
        print(fmt("full sample", xs))
        print(f"    first month {res[0][0] if res else '-'}, last {res[-1][0] if res else '-'}")
        print(fmt("2009-2017", [x for d, x in res if d < "2018"]))
        print(fmt("2018-2026", [x for d, x in res if d >= "2018"]))
        k = len(res)
        pos = 0
        for w in range(9):
            chunk = res[w * k // 9:(w + 1) * k // 9]
            cx = [x for _, x in chunk]
            n, m, tt = stats(cx)
            pos += (m > 0) if n >= 3 else 0
            print(f"    window {w + 1}: {chunk[0][0]} to {chunk[-1][0]}  n={n:>3}  "
                  f"spread={m * 100:+6.2f}pp  t={tt:+5.2f}")
        print(f"  walk-forward windows with positive spread: {pos} of 9")
        res2, (ng2, nn2, _) = run(dates, bars, syms, fund, metric, exclude=MEGACAPS)
        print(fmt("drop megacaps (9 names)", [x for _, x in res2]))
        print(f"    growing={ng2}  not growing={nn2}")


if __name__ == "__main__":
    main()
