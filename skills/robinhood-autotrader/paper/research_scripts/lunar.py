#!/usr/bin/env python3
"""
Wednesday probe 2026-11-11: new-moon vs full-moon returns. Prints data only (R14.1).
Design and prediction: research/2026-11-11_LUNAR.md (committed first).
Usage: python3 paper/research_scripts/lunar.py
"""
import json, math, os
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(HERE, "..", "history", "daily_ohlcv.json")))
MEGA = {"AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"}
SYN = 29.530588853
REF = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)


def age(d):
    """Moon age in days at 16:00 ET (~21:00 UTC) on date d."""
    t = datetime.fromisoformat(d + "T21:00:00+00:00")
    return ((t - REF).total_seconds() / 86400) % SYN


def is_new(d):
    a = age(d)
    return a < SYN / 4 or a >= 3 * SYN / 4


spy = raw["SPY"]
dates = sorted(spy)
others = [s for s in raw if s != "SPY" and s not in MEGA]
series = {"SPY": {}, "basket": {}}
for i in range(1, len(dates)):
    d, p = dates[i], dates[i - 1]
    series["SPY"][d] = spy[d][3] / spy[p][3] - 1
    r = [raw[s][d][3] / raw[s][p][3] - 1 for s in others if d in raw[s] and p in raw[s]]
    if r:
        series["basket"][d] = sum(r) / len(r)


def welch(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    va = sum((x - ma) ** 2 for x in a) / (len(a) - 1)
    vb = sum((x - mb) ** 2 for x in b) / (len(b) - 1)
    return ma, mb, (ma - mb) / math.sqrt(va / len(a) + vb / len(b))


def report(label, ser, ds):
    a = [ser[d] for d in ds if is_new(d)]
    b = [ser[d] for d in ds if not is_new(d)]
    ma, mb, t = welch(a, b)
    print(f"  {label:<22} new-moon n={len(a):>4} {ma * 100:+.4f}%/d | full-moon n={len(b):>4} {mb * 100:+.4f}%/d | "
          f"gap {(ma - mb) * 100:+.4f}pp/d (~{(ma - mb) * 252 * 100:+.1f}pp/yr) t={t:+.2f}")
    return ma - mb


# sanity: known new moons should give age near 0 / 29.5
for d in ("2024-01-11", "2025-01-29", "2026-01-18"):
    print(f"phase check {d}: moon age {age(d):.2f} days (a known new-moon date should be near 0 or 29.5)")
for name, ser in series.items():
    ds = sorted(ser)
    print(f"\n=== {name} ({ds[0]} .. {ds[-1]}) ===")
    report("full", ser, ds)
    h = len(ds) // 2
    report("1st half", ser, ds[:h])
    report("2nd half", ser, ds[h:])
    k = len(ds)
    g = [report(f"window {w + 1}", ser, ds[w * k // 9:(w + 1) * k // 9]) for w in range(9)]
    print(f"  windows with new > full: {sum(x > 0 for x in g)} of 9")
