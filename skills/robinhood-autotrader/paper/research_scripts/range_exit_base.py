#!/usr/bin/env python3
"""
Shared harness for the 2026-11-01 swarm: range-regime entry with different
EXITS. Prints data only (R14.1). Design: research/2026-11-01_RANGE_EXIT_SWARM.md.

ENTRY (fixed, from research/2026-09-23_RANGE_REGIME.md): at the close, Wilder
ADX(14) < 20 and close in the bottom 25% of its trailing 60-day high-low range
-> buy at the next open. Max 4 positions, each 85%/4 of equity at entry,
fractional, 5bp per side. 8% hard stop from entry, checked on the low, filled
at min(open, stop).
CONTROL entry ("top"): same, but close in the TOP 25% of the range. If an
exit preserves the entry's edge, bottom must beat top under the same exit.

Exit hook: exit_fn(p, seq, i, rng) -> True to sell at the next open, where
p = position dict (e=entry px, d0=entry index, hi=highest close), seq = bars,
i = today, rng = (lo60, hi60). The stop always applies on top.
Data: paper/history/daily_stocks.json (14 names + SPY, 2006-2026).
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from engine import load, _adx, O, H, L, C  # noqa: E402

MEGA = {"AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"}
_CACHE = {}


def prep():
    if "d" not in _CACHE:
        dates, bars, syms = load()
        adx = {s: _adx(bars[s]) for s in syms}
        _CACHE["d"] = (dates, bars, syms, adx)
    return _CACHE["d"]


def rng60(seq, i):
    lo = min(seq[j][L] for j in range(i - 59, i + 1))
    hi = max(seq[j][H] for j in range(i - 59, i + 1))
    return lo, hi


def run(exit_fn, entry="bottom", start=None, end=None, syms=None, slots=4, cost=0.0005, stop=0.08):
    dates, bars, allsyms, adx = prep()
    syms = sorted(syms or allsyms)
    i0 = max(next(i for i, d in enumerate(dates) if d >= (start or "0000")), 80)
    i1 = max(i for i, d in enumerate(dates) if d <= (end or "9999"))
    cash, pos, pend, trades, eq = 1.0, {}, [], [], []
    for i in range(i0, i1 + 1):
        for s in pend:
            if s in pos or len(pos) >= slots:
                continue
            equity = cash + sum(p["q"] * bars[x][i][O] for x, p in pos.items())
            px = bars[s][i][O] * (1 + cost)
            amt = min(equity * 0.85 / slots, cash - 0.15 * equity)
            if amt <= 0:
                continue
            pos[s] = dict(q=amt / px, e=px, d0=i, hi=bars[s][i][O], out=False)
            cash -= amt
        pend = []
        for s in list(pos):
            p, b = pos[s], bars[s][i]
            st = p["e"] * (1 - stop)
            if p["out"]:
                fill, why = b[O] * (1 - cost), "exit_rule"
            elif b[L] <= st:
                fill, why = min(b[O], st) * (1 - cost), "stop"
            else:
                continue
            cash += p["q"] * fill
            trades.append(dict(sym=s, ret=fill / p["e"] - 1, why=why, hold=i - p["d0"]))
            del pos[s]
        for s, p in pos.items():
            seq = bars[s]
            p["hi"] = max(p["hi"], seq[i][C])
            p["out"] = bool(exit_fn(p, seq, i, rng60(seq, i)))
        eq.append(cash + sum(p["q"] * bars[s][i][C] for s, p in pos.items()))
        free = slots - len(pos)
        if free > 0:
            cands = []
            for s in syms:
                if s in pos or adx[s][i] is None or adx[s][i] >= 20:
                    continue
                lo, hi = rng60(bars[s], i)
                if hi <= lo:
                    continue
                loc = (bars[s][i][C] - lo) / (hi - lo)
                if (entry == "bottom" and loc <= 0.25) or (entry == "top" and loc >= 0.75):
                    cands.append((loc if entry == "bottom" else -loc, s))
            cands.sort()
            pend = [s for _, s in cands[:free]]
    spy = [bars["SPY"][i][C] for i in range(i0, i1 + 1)]
    return dict(eq=eq, spy=spy, trades=trades, start=dates[i0], end=dates[i1])


def cagr(x):
    return (x[-1] / x[0]) ** (252 / len(x)) - 1


def mdd(x):
    pk, d = x[0], 0.0
    for v in x:
        pk = max(pk, v); d = min(d, v / pk - 1)
    return d


def tdiff(a, b):
    d = [a[i] / a[i - 1] - b[i] / b[i - 1] for i in range(1, len(a))]
    m = sum(d) / len(d)
    sd = math.sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
    return m / (sd / math.sqrt(len(d))) if sd else float("nan")


def line(label, r):
    tr = r["trades"]
    n = len(tr)
    avg = sum(t["ret"] for t in tr) / n if n else float("nan")
    win = sum(t["ret"] > 0 for t in tr) / n if n else float("nan")
    hold = sum(t["hold"] for t in tr) / n if n else float("nan")
    return (f"  {label:<26} {r['start']}..{r['end']}  CAGR {cagr(r['eq']) * 100:6.2f}%  DD {mdd(r['eq']) * 100:6.1f}%  "
            f"SPY {cagr(r['spy']) * 100:6.2f}%  trades {n:>4}  win {win * 100:4.0f}%  avg {avg * 100:+.2f}%  hold {hold:5.1f}d")


def hurdles(label, exit_fn):
    """Bottom entry vs SPY and vs the TOP-entry control, same exit. Data only."""
    dates = prep()[0]
    print(f"\n=== {label} ===")
    b = run(exit_fn, "bottom")
    t = run(exit_fn, "top")
    print(line("bottom entry", b))
    print(line("top entry (control)", t))
    print(f"  bottom - SPY {(cagr(b['eq']) - cagr(b['spy'])) * 100:+.2f}pp (daily t {tdiff(b['eq'], b['spy']):+.2f}); "
          f"bottom - top {(cagr(b['eq']) - cagr(t['eq'])) * 100:+.2f}pp (daily t {tdiff(b['eq'], t['eq']):+.2f})")
    idx = [i for i, d in enumerate(dates) if d >= b["start"]]
    half = dates[idx[len(idx) // 2]]
    for lab, s0, s1 in (("1st half", None, half), ("2nd half", half, None)):
        bb, tt = run(exit_fn, "bottom", s0, s1), run(exit_fn, "top", s0, s1)
        print(f"  {lab}: bottom {cagr(bb['eq']) * 100:6.2f}%  top {cagr(tt['eq']) * 100:6.2f}%  SPY {cagr(bb['spy']) * 100:6.2f}%")
    nm = [s for s in prep()[2] if s not in MEGA]
    bb, tt = run(exit_fn, "bottom", syms=nm), run(exit_fn, "top", syms=nm)
    print(f"  megacaps dropped: bottom {cagr(bb['eq']) * 100:6.2f}%  top {cagr(tt['eq']) * 100:6.2f}%  SPY {cagr(bb['spy']) * 100:6.2f}%  "
          f"trades {len(bb['trades'])}")
    edges = [idx[len(idx) * k // 9] for k in range(9)] + [idx[-1]]
    vs_spy, vs_top = [], []
    for k in range(9):
        s0, s1 = dates[edges[k]], dates[edges[k + 1]]
        bb, tt = run(exit_fn, "bottom", s0, s1), run(exit_fn, "top", s0, s1)
        vs_spy.append(cagr(bb["eq"]) - cagr(bb["spy"]))
        vs_top.append(cagr(bb["eq"]) - cagr(tt["eq"]))
    print(f"  walk-forward vs SPY (pp): {' '.join(f'{x * 100:+.1f}' for x in vs_spy)} -> ahead {sum(x > 0 for x in vs_spy)} of 9")
    print(f"  walk-forward vs top (pp): {' '.join(f'{x * 100:+.1f}' for x in vs_top)} -> ahead {sum(x > 0 for x in vs_top)} of 9")


def range_top_exit(p, seq, i, rng):
    """The 2026-09-23 rule (reproduction check): sell in the top 25% of the range."""
    lo, hi = rng
    return hi > lo and (seq[i][C] - lo) / (hi - lo) >= 0.75


if __name__ == "__main__":
    print("reproduction of the 2026-09-23 rejected rule (range-top exit + 8% stop):")
    print(line("bottom entry", run(range_top_exit, "bottom")))
