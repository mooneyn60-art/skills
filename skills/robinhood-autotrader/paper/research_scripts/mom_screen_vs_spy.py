#!/usr/bin/env python3
"""
Swarm queue 1b (2026-10-25): the live 12-1 momentum screen vs SPY buy-and-hold
through the four hurdles, plus its live trades in R. Prints data only (R14.1).
Design and prediction: research/2026-10-25_MOMENTUM_SCREEN_VS_SPY.md (committed first).
Usage: python3 paper/research_scripts/mom_screen_vs_spy.py
"""
import json, math, os

from mom_screen_base import load, run, MEGA

HERE = os.path.dirname(os.path.abspath(__file__))


def cagr(eq):
    return (eq[-1] / eq[0]) ** (252 / len(eq)) - 1


def mdd(eq):
    peak, d = eq[0], 0.0
    for v in eq:
        peak = max(peak, v); d = min(d, v / peak - 1)
    return d


def mix85(spy):
    out = [1.0]
    for i in range(1, len(spy)):
        out.append(out[-1] * (1 + 0.85 * (spy[i] / spy[i - 1] - 1)))
    return out


def tdiff(a, b):
    d = [a[i] / a[i - 1] - b[i] / b[i - 1] for i in range(1, len(a))]
    m = sum(d) / len(d)
    sd = math.sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
    return m / (sd / math.sqrt(len(d)))


def row(label, res):
    eq, spy = res["eq"], res["spy"]
    m85 = mix85(spy)
    print(f"  {label:<28} {res['start']}..{res['end']}  screen {cagr(eq) * 100:6.2f}% (DD {mdd(eq) * 100:5.1f}%)  "
          f"SPY {cagr(spy) * 100:6.2f}% (DD {mdd(spy) * 100:5.1f}%)  85%SPY {cagr(m85) * 100:6.2f}%  "
          f"diff vs SPY {(cagr(eq) - cagr(spy)) * 100:+6.2f}pp t={tdiff(eq, spy):+.2f}  "
          f"vs 85% {(cagr(eq) - cagr(m85)) * 100:+6.2f}pp t={tdiff(eq, m85):+.2f}")
    return cagr(eq) - cagr(spy)


for U, lo in (("LONG", "2006-01-01"), ("WIDE", "2021-12-01")):
    dates, bars, spyb = load(U)
    print(f"\n=== {U} ({len(bars)} names; survivorship-biased, price returns) ===")
    full = run(dates, bars, spyb, start=lo)
    row("full", full)
    idx = [i for i, d in enumerate(dates) if d >= full["start"]]
    half = dates[idx[len(idx) // 2]]
    row("1st half", run(dates, bars, spyb, start=lo, end=half))
    row("2nd half", run(dates, bars, spyb, start=half))
    row("megacaps dropped", run(dates, bars, spyb, start=lo, syms=[s for s in bars if s not in MEGA]))
    edges = [idx[len(idx) * k // 9] for k in range(9)] + [idx[-1]]
    cells, w = [], 0
    for k in range(9):
        r = run(dates, bars, spyb, start=dates[edges[k]], end=dates[edges[k + 1]])
        g = cagr(r["eq"]) - cagr(r["spy"])
        cells.append(f"{g * 100:+.1f}"); w += g > 0
    print(f"  walk-forward 9 windows, screen minus SPY (pp CAGR): {' '.join(cells)}  -> screen ahead {w} of 9")

print("\n=== LIVE momentum-sleeve trades (paper/trades.jsonl, closed, planned_risk > 0) ===")
rs = []
for line in open(os.path.join(HERE, "..", "trades.jsonl")):
    if not line.strip():
        continue
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("strategy") != "momentum_satellite" or d.get("realized_pnl") is None:
        continue
    try:
        pr, pnl = float(d.get("planned_risk") or 0), float(d["realized_pnl"])
    except (TypeError, ValueError):
        continue
    if pr <= 0:
        continue
    rs.append((d.get("symbol"), pnl / pr, str(d.get("exit_reason"))[:30]))
for s, r, why in rs:
    print(f"  {s:<6} {r:+.2f}R  {why}")
if len(rs) > 1:
    m = sum(r for _, r, _ in rs) / len(rs)
    sd = math.sqrt(sum((r - m) ** 2 for _, r, _ in rs) / (len(rs) - 1))
    print(f"  n={len(rs)} mean {m:+.2f}R t={m / (sd / math.sqrt(len(rs))):+.2f}  winners {sum(r > 0 for _, r, _ in rs)}")
