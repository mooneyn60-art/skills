#!/usr/bin/env python3
"""
Wednesday probe 2026-11-04: quarter-end window dressing. Prints data only (R14.1).
Design and prediction: research/2026-11-04_QUARTER_END.md (committed first).
Usage: python3 paper/research_scripts/quarter_end.py
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
H = os.path.join(HERE, "..", "history")
MEGA = {"AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"}


def load(files):
    raw = {}
    for f in files:
        for s, rows in json.load(open(os.path.join(H, f))).items():
            raw.setdefault(s, rows)
    spy = raw.pop("SPY")
    return sorted(spy), raw


def month_ends(dates, months):
    """Last trading day of each month whose month number is in `months`."""
    out = []
    for i, d in enumerate(dates[:-1]):
        if dates[i + 1][:7] != d[:7] and int(d[5:7]) in months:
            out.append(i)
    return out


def spreads(dates, raw, ends, syms):
    rows = []
    for e in ends:
        r = e - 5          # rank at this close; A covers the 5 sessions r+1..e (the last 5 of the period)
        if r - 70 < 0 or e + 5 >= len(dates):
            continue
        # period start: last close of the previous calendar quarter/month block (~63 or ~21 days back)
        start = next((j for j in range(r - 1, 0, -1) if dates[j][:7] != dates[j + 1][:7]
                      and (int(dates[j][5:7]) - int(dates[e][5:7])) % 3 == 0), None)
        if start is None:
            continue
        d0, dr, de, d5 = dates[start], dates[r], dates[e], dates[e + 5]
        live = [s for s in syms if all(x in raw[s] for x in (d0, dr, de, d5))]
        if len(live) < 6:
            continue
        qtd = sorted(live, key=lambda s: raw[s][dr][3] / raw[s][d0][3])
        k = len(live) // 3
        lo, hi = qtd[:k], qtd[-k:]
        f = lambda g, a, b: sum(raw[s][b][3] / raw[s][a][3] - 1 for s in g) / len(g)
        rows.append(dict(d=de, A=f(hi, dr, de) - f(lo, dr, de), B=f(hi, de, d5) - f(lo, de, d5)))
    return rows


def mt(v):
    n = len(v); m = sum(v) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in v) / (n - 1))
    return m, m / (sd / math.sqrt(n)), n


def show(label, rows):
    for key, name in (("A", "last 5d of period (winners-losers)"), ("B", "first 5d after (winners-losers)")):
        m, t, n = mt([r[key] for r in rows])
        print(f"  {label:<30} {name:<36} n={n:>3} mean {m * 100:+.3f}pp t={t:+.2f}")


for U, files in (("LONG", ["daily_ohlcv.json"]),
                 ("WIDE", ["daily_ohlcv.json", "daily_ohlcv_volatile.json", "daily_ohlcv_holdings.json"])):
    dates, raw = load(files)
    syms = sorted(raw)
    qe = month_ends(dates, {3, 6, 9, 12})
    rows = spreads(dates, raw, qe, syms)
    print(f"\n=== {U} ({len(syms)} names), quarter-ends {rows[0]['d']} .. {rows[-1]['d']} ===")
    show("quarter-ends, all", rows)
    h = len(rows) // 2
    show("quarter-ends, 1st half", rows[:h])
    show("quarter-ends, 2nd half", rows[h:])
    show("quarter-ends, no megacaps", spreads(dates, raw, qe, [s for s in syms if s not in MEGA]))
    pl = spreads(dates, raw, month_ends(dates, {1, 2, 4, 5, 7, 8, 10, 11}), syms)
    show("PLACEBO non-quarter month-ends", pl)
    if U == "LONG":
        k = len(rows)
        for key in ("A", "B"):
            cells = [sum(r[key] for r in rows[w * k // 9:(w + 1) * k // 9]) / len(rows[w * k // 9:(w + 1) * k // 9])
                     for w in range(9)]
            print(f"  9 windows {key} (pp): {' '.join(f'{c * 100:+.2f}' for c in cells)}  -> positive {sum(c > 0 for c in cells)} of 9")
