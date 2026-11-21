#!/usr/bin/env python3
"""
Agenda item 3: gaps through stops, earnings share of big gaps, Fed days.
Prints data only (R14.1). Design: research/2026-09-25_EVENT_REACTIONS.md.

E1  daily_stocks.json (14 names, 2006-2026) and daily_ohlcv_holdings.json
    (holdings, 2022-2026): open vs a stop k% below the prior close.
E2  holdings, earnings_reports.json window only: share of <= -8% gaps on
    earnings reaction days (report day if 'am', next trading day if 'pm').
E3  S&P 500 TR (options_indices.json) on Fed statement days and the day
    before vs other days. Dates: paper/history/fomc_dates.json.
Usage: python3 paper/test_event_reactions.py
"""
import json, math, os

from engine import load, O, C

HERE = os.path.dirname(os.path.abspath(__file__))
HIST = os.path.join(HERE, "history")


def gaps_table(label, series):
    """series: {sym: [(date, open, prev_close)]}"""
    n = sum(len(v) for v in series.values())
    print(f"\nE1 {label}: {n} name-days")
    for k in (0.02, 0.04, 0.06, 0.08):
        hits, short = 0, []
        for rows in series.values():
            for _, o, pc in rows:
                stop = pc * (1 - k)
                if o < stop:
                    hits += 1
                    short.append(1 - o / stop)
        avg = sum(short) / len(short) * 100 if short else float("nan")
        worst = max(short) * 100 if short else float("nan")
        print(f"  stop {k * 100:.0f}% below prior close: open already below it on {hits} days "
              f"({hits / n * 100:.3f}%); avg shortfall {avg:.2f}%, worst {worst:.1f}%")


def welch(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    va = sum((x - ma) ** 2 for x in a) / (len(a) - 1)
    vb = sum((x - mb) ** 2 for x in b) / (len(b) - 1)
    return ma - mb, (ma - mb) / math.sqrt(va / len(a) + vb / len(b))


def main():
    dates, bars, syms = load()
    long_ = {s: [(dates[i], bars[s][i][O], bars[s][i - 1][C]) for i in range(1, len(dates))]
             for s in syms}
    gaps_table("14 names, daily_stocks.json 2006-2026", long_)

    hold = json.load(open(os.path.join(HIST, "daily_ohlcv_holdings.json")))
    hseries = {}
    for s, v in hold.items():
        if s.startswith("_"):
            continue
        ks = sorted(v)
        hseries[s] = [(ks[i], v[ks[i]][0], v[ks[i - 1]][3]) for i in range(1, len(ks))]
    gaps_table(f"holdings {sorted(hseries)}, daily_ohlcv_holdings.json", hseries)

    earn = json.load(open(os.path.join(HIST, "earnings_reports.json")))
    print("\nE2 holdings, <= -8% opening gaps, earnings_reports.json window only")
    tot = on_e = 0
    for s, rows in hseries.items():
        reps = earn.get(s, [])
        if not reps:
            continue
        ks = [d for d, _, _ in rows]
        react = set()
        for r in reps:
            d = r["date"]
            if r.get("timing") == "pm":
                later = [x for x in ks if x > d]
                if later:
                    react.add(later[0])
            else:
                react.add(d)
        start = min(r["date"] for r in reps)
        big = [(d, o / pc - 1) for d, o, pc in rows if d >= start and o / pc - 1 <= -0.08]
        e = [x for x in big if x[0] in react]
        tot += len(big)
        on_e += len(e)
        print(f"  {s:<5} from {start}: {len(big)} gaps <= -8%, {len(e)} on earnings reaction days  "
              + " ".join(f"{d}({g * 100:+.0f}%{'E' if d in react else ''})" for d, g in big))
    print(f"  total {tot}, on earnings days {on_e}")

    path = os.path.join(HIST, "fomc_dates.json")
    if not os.path.exists(path):
        print("\nE3 skipped: paper/history/fomc_dates.json not present")
        return
    fomc = set(json.load(open(path))["scheduled"])
    sp = json.load(open(os.path.join(HIST, "options_indices.json")))["series"]["SPTR"]
    sd = [d for d in sorted(sp) if d >= "2006-01-01"]
    r = {sd[i]: sp[sd[i]] / sp[sd[i - 1]] - 1 for i in range(1, len(sd))}
    days = sd[1:]
    before = {days[i - 1] for i in range(1, len(days)) if days[i] in fomc}
    print(f"\nE3 S&P 500 TR, {days[0]} to {days[-1]}; scheduled statement days found in data: "
          f"{sum(1 for d in days if d in fomc)} of {len(fomc)}")
    for lab, sel in (("statement day", lambda d: d in fomc), ("day before", lambda d: d in before)):
        for per, lo, hi in (("2006-2026", "2006", "2027"), ("2006-2015", "2006", "2016"),
                            ("2016-2026", "2016", "2027")):
            a = [r[d] for d in days if lo <= d < hi and sel(d)]
            b = [r[d] for d in days if lo <= d < hi and not sel(d) and d not in fomc and d not in before]
            diff, t = welch(a, b)
            print(f"  {lab:<13} {per}: n={len(a):>3} mean {sum(a) / len(a) * 100:+.3f}%  "
                  f"other days {sum(b) / len(b) * 100:+.3f}%  diff {diff * 100:+.3f}pp  t={t:+.2f}")


if __name__ == "__main__":
    main()
