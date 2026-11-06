#!/usr/bin/env python3
"""
Wednesday probe 2026-10-28: pre-holiday effect in SPY and the 14 names.
Prints data only (R14.1). Design and prediction: research/2026-10-28_PRE_HOLIDAY.md.
Data: paper/history/daily_ohlcv.json ([open, high, low, close, volume] per date).
Usage: python3 paper/research_scripts/pre_holiday.py
"""
import json, math, os
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(HERE, "..", "history", "daily_ohlcv.json")))
MEGA = {"AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"}
spy = raw["SPY"]
dates = sorted(spy)


def weekday_gap(d0, d1):
    """Number of weekdays strictly between two trading dates."""
    a, b = date.fromisoformat(d0), date.fromisoformat(d1)
    n, x = 0, a + timedelta(days=1)
    while x < b:
        n += x.weekday() < 5
        x += timedelta(days=1)
    return n


pre = set()
for i in range(len(dates) - 1):
    if weekday_gap(dates[i], dates[i + 1]) >= 1:
        pre.add(dates[i])

others = [s for s in raw if s != "SPY" and s not in MEGA]


def series(kind):
    out = {}
    for i in range(1, len(dates)):
        d, p = dates[i], dates[i - 1]
        if kind == "spy_cc":
            out[d] = spy[d][3] / spy[p][3] - 1
        elif kind == "spy_oc":
            out[d] = spy[d][3] / spy[d][0] - 1
        else:
            rs = [raw[s][d][3] / raw[s][p][3] - 1 for s in others if d in raw[s] and p in raw[s]]
            if rs:
                out[d] = sum(rs) / len(rs)
    return out


def welch(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    va = sum((x - ma) ** 2 for x in a) / (len(a) - 1)
    vb = sum((x - mb) ** 2 for x in b) / (len(b) - 1)
    return ma, mb, (ma - mb) / math.sqrt(va / len(a) + vb / len(b))


def report(label, ser, lo="0000", hi="9999"):
    ds = [d for d in ser if lo <= d <= hi]
    a = [ser[d] for d in ds if d in pre]
    b = [ser[d] for d in ds if d not in pre]
    ma, mb, t = welch(a, b)
    up = sum(x > 0 for x in a) / len(a)
    print(f"  {label:<34} pre-holiday n={len(a):>3} mean {ma * 100:+.3f}% up {up * 100:4.0f}% | other n={len(b):>4} "
          f"mean {mb * 100:+.3f}% | diff {(ma - mb) * 100:+.3f}pp t={t:+.2f}")


print(f"source: daily_ohlcv.json, {dates[0]} to {dates[-1]}; pre-holiday days found: {len(pre)}")
print("  first 12 detected:", " ".join(sorted(pre)[:12]))
for kind, name in (("spy_cc", "SPY close-to-close"), ("spy_oc", "SPY open-to-close"),
                   ("basket", "9 non-megacap names, eq-weight")):
    ser = series(kind)
    print(f"\n=== {name} ===")
    report("full", ser)
    report("2006-2015", ser, hi="2015-12-31")
    report("2016-2026", ser, lo="2016-01-01")
    ds = sorted(ser)
    k = len(ds)
    cells, pos = [], 0
    for w in range(9):
        sub = ds[w * k // 9:(w + 1) * k // 9]
        a = [ser[d] for d in sub if d in pre]
        b = [ser[d] for d in sub if d not in pre]
        g = sum(a) / len(a) - sum(b) / len(b) if a else float("nan")
        cells.append(f"{g * 100:+.2f}(n{len(a)})")
        pos += g > 0
    print(f"  9 windows, pre minus other (pp): {' '.join(cells)}  -> positive {pos} of 9")
