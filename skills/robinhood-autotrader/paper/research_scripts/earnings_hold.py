#!/usr/bin/env python3
"""
Swarm queue item 4 (2026-11-08): hold through earnings or sell the close before?
Prints data only (R14.1). Design and prediction: research/2026-11-08_EARNINGS_HOLD_SWARM.md.
Data: paper/history/earnings_reports.json + earnings_reports_wide.json (dates, am/pm),
daily_ohlcv*.json (prices: [open, high, low, close, volume]).
Usage: python3 paper/research_scripts/earnings_hold.py
"""
import json, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
H = os.path.join(HERE, "..", "history")
MEGA = {"AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"}

px = {}
for f in ("daily_ohlcv.json", "daily_ohlcv_volatile.json", "daily_ohlcv_holdings.json"):
    for s, rows in json.load(open(os.path.join(H, f))).items():
        px.setdefault(s, rows)
er = {}
for f in ("earnings_reports.json", "earnings_reports_wide.json"):
    p = os.path.join(H, f)
    if os.path.exists(p):
        for s, v in json.load(open(p)).items():
            if not s.startswith("_") and isinstance(v, list):
                er.setdefault(s, v)

events, skipped = [], 0
for s, qs in er.items():
    if s not in px:
        skipped += len(qs)
        continue
    ds = sorted(px[s])
    pos = {d: i for i, d in enumerate(ds)}
    for q in qs:
        d, tm = q.get("date"), q.get("timing")
        if not d or tm not in ("am", "pm"):
            skipped += 1
            continue
        i = next((k for k, x in enumerate(ds) if x >= d), None)
        if i is None:
            skipped += 1
            continue
        a = i - 1 if tm == "am" else i          # last close before the reaction
        b = a + 1
        if a < 252 or b + 20 >= len(ds):
            skipped += 1
            continue
        c = lambda k: px[s][ds[k]][3]
        sma = sum(c(k) for k in range(a - 199, a + 1)) / 200
        mom = c(a - 21) / c(a - 252) - 1
        events.append(dict(s=s, d=ds[b], R=c(b) / c(a) - 1, drift=c(b + 20) / c(b) - 1,
                           gap_open=px[s][ds[b]][0] / c(a) - 1,
                           momentum=c(a) > sma and mom > 0))


def mt(v):
    n = len(v)
    if n < 2:
        return float("nan"), float("nan"), n
    m = sum(v) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in v) / (n - 1))
    return m, m / (sd / math.sqrt(n)), n


def boot(ev, key, reps=10000, seed=1):
    """Bootstrap the mean, resampling whole report DATES (events on the same day move together)."""
    by = {}
    for e in ev:
        by.setdefault(e["d"], []).append(e[key])
    days = list(by)
    rnd = random.Random(seed)
    ms = []
    for _ in range(reps):
        pick = [x for _ in days for x in by[rnd.choice(days)]]
        ms.append(sum(pick) / len(pick))
    ms.sort()
    return ms[int(0.05 * reps)], ms[int(0.95 * reps)]


def row(label, ev):
    if len(ev) < 2:
        print(f"  {label:<34} n={len(ev)}")
        return
    m, t, n = mt([e["R"] for e in ev])
    dm, dt, _ = mt([e["drift"] for e in ev])
    lo, hi = boot(ev, "R")
    thru = sum(e["R"] <= -0.08 for e in ev) / n
    gopen = sum(e["gap_open"] <= -0.08 for e in ev) / n
    print(f"  {label:<34} n={n:>3}  reaction mean {m * 100:+.2f}% t={t:+.2f} (90% boot {lo * 100:+.2f}..{hi * 100:+.2f})  "
          f"<=-8%: close {thru * 100:4.1f}% / open {gopen * 100:4.1f}%  20d drift after {dm * 100:+.2f}% t={dt:+.2f}")


print(f"events: {len(events)} usable, {skipped} skipped; symbols {len({e['s'] for e in events})}; "
      f"{min(e['d'] for e in events)} .. {max(e['d'] for e in events)}")
mom = [e for e in events if e["momentum"]]
oth = [e for e in events if not e["momentum"]]
row("ALL", events)
row("momentum names (screen-eligible)", mom)
row("other names", oth)
m1, _, _ = mt([e["R"] for e in mom]); m2, _, _ = mt([e["R"] for e in oth])
va = lambda v: sum((x - sum(v) / len(v)) ** 2 for x in v) / (len(v) - 1)
a, b = [e["R"] for e in mom], [e["R"] for e in oth]
print(f"  momentum minus other: {(m1 - m2) * 100:+.2f}pp  Welch t={(m1 - m2) / math.sqrt(va(a) / len(a) + va(b) / len(b)):+.2f}")
mid = sorted(e["d"] for e in mom)[len(mom) // 2] if mom else "9999"
row("momentum, 1st half", [e for e in mom if e["d"] < mid])
row("momentum, 2nd half", [e for e in mom if e["d"] >= mid])
row("momentum, megacaps", [e for e in mom if e["s"] in MEGA])
row("momentum, non-megacaps", [e for e in mom if e["s"] not in MEGA])
print("  per symbol, momentum events (n, mean reaction):")
cells = []
for s in sorted({e["s"] for e in mom}):
    v = [e["R"] for e in mom if e["s"] == s]
    cells.append(f"{s} {len(v)} {sum(v) / len(v) * 100:+.1f}%")
print("    " + "; ".join(cells))
