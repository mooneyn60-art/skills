#!/usr/bin/env python3
"""
2026-11-15: live momentum screen with and without earnings handling, 20 years.
Prints data only (R14.1). Design and prediction: research/2026-11-15_EARNINGS_EXIT_BACKTEST.md.
A: harness baseline. B: no entry if a reaction is within the next 3 sessions.
C: B + sell at the close before each reaction, rebuy at the next open after the
   reaction day if still eligible and a slot is free.
D (ADDED AFTER THE FIRST RUN, post hoc decomposition): B, but each reaction day is
   neutralised (value frozen, 2x cost), stops/trail state kept. C - D = the cost of
   resetting stops on rebuy; D - B = the cost of missing the reactions themselves.
Data: earnings_8k.json (SEC 8-K item 2.02), daily_ohlcv.json via mom_screen_base.
Usage: python3 paper/research_scripts/earnings_exit_test.py
"""
import json, math, os

from mom_screen_base import load, sma, vol63, mom_12_1, first_valid, stats, daily_t, SECTORS, MEGA, O, C

HERE = os.path.dirname(os.path.abspath(__file__))
E8K = json.load(open(os.path.join(HERE, "..", "history", "earnings_8k.json")))


def reaction_index(dates):
    """sym -> set of bar indexes i such that the earnings reaction is close(i-1) -> close(i)."""
    pos = {d: i for i, d in enumerate(dates)}
    out = {}
    for s, evs in E8K.items():
        if s.startswith("_"):
            continue
        idx = set()
        for e in evs:
            i = next((pos[d] for d in dates[max(0, 0):] if d >= e["date"]), None) if e["date"] not in pos else pos[e["date"]]
            if i is None:
                continue
            idx.add(i + 1 if e["timing"] == "pm" else i)
        out[s] = idx
    return out


def run(dates, bars, spyb, react, mode, start=None, end=None, syms=None, slots=8, cost=0.0005):
    syms = sorted(syms or bars)
    i0 = max(next(i for i, d in enumerate(dates) if d >= (start or "0000")), 253)
    i1 = max(i for i, d in enumerate(dates) if d <= (end or "9999"))
    cash, pos, pend, watch, eq, month = 1.0, {}, [], [], [], None
    rebuy = {}   # sym -> index of the open at which to try re-entering
    n_exits = 0

    def eligible(s, i):
        seq = bars[s]
        if seq[i] is None or i - first_valid(seq) < 252:
            return False
        sc, s200, v = mom_12_1(seq, i), sma(seq, i, 200), vol63(seq, i)
        return sc is not None and sc > 0 and s200 is not None and v is not None and seq[i][C] > s200 and v <= 0.80

    def near(s, i, k):
        return any(i < j <= i + k for j in react.get(s, ()))

    for i in range(i0, i1 + 1):
        # fills at the open
        todo = pend + [s for s, j in rebuy.items() if j == i]
        rebuy = {s: j for s, j in rebuy.items() if j != i}
        for s in todo:
            if s in pos or len(pos) >= slots or bars[s][i] is None:
                continue
            equity = cash + sum(p["q"] * bars[x][i][O] for x, p in pos.items())
            px = bars[s][i][O] * (1 + cost)
            amt = min(equity * 0.85 / slots, cash - 0.15 * equity)
            if amt <= 0:
                continue
            pos[s] = dict(q=amt / px, e=px, hi=bars[s][i][O], stop=0.92 * px, out=False)
            cash -= amt
        pend = []
        for s in list(pos):
            p, b = pos[s], bars[s][i]
            if p["out"]:
                fill = b[O] * (1 - cost)
            elif mode == "D" and i in react.get(s, ()):
                continue                      # D: reaction bar neutralised, no stop check on it
            elif b[2] <= p["stop"]:
                fill = min(b[O], p["stop"]) * (1 - cost)
            else:
                continue
            cash += p["q"] * fill
            del pos[s]
        # close: stops, trend flag, earnings exit at THIS close
        for s in list(pos):
            p, b = pos[s], bars[s][i]
            if mode == "D" and i in react.get(s, ()) and bars[s][i - 1]:
                p["q"] *= bars[s][i - 1][C] / b[C] * (1 - 2 * cost)   # value frozen over the reaction, 2 trades of cost
                continue
            p["hi"] = max(p["hi"], b[C])
            p["stop"] = max(p["stop"], 0.80 * p["hi"], p["e"] if b[C] >= 1.08 * p["e"] else 0)
            s200 = sma(bars[s], i, 200)
            p["out"] = s200 is not None and b[C] < s200
            if mode == "C" and (i + 1) in react.get(s, ()) and not p["out"]:
                cash += p["q"] * b[C] * (1 - cost)
                del pos[s]
                n_exits += 1
                if i + 2 <= i1:
                    rebuy[s] = i + 2
        # drop rebuys that are no longer eligible at the reaction-day close
        for s, j in list(rebuy.items()):
            if j == i + 1 and not eligible(s, i):
                del rebuy[s]
        eq.append(cash + sum(p["q"] * bars[s][i][C] for s, p in pos.items()))
        if dates[i][:7] != month:
            month = dates[i][:7]
            cands = [(s, mom_12_1(bars[s], i)) for s in syms if eligible(s, i)]
            watch = sorted(cands, key=lambda x: -x[1])
        free = slots - len(pos) - len(rebuy)
        if dates[i][:7] == month and free > 0 and (i == 0 or dates[i - 1][:7] != month):
            sec = {}
            for s in pos:
                sec[SECTORS[s]] = sec.get(SECTORS[s], 0) + 1
            for s, _ in watch:
                if free <= 0:
                    break
                if s in pos or s in rebuy or sec.get(SECTORS[s], 0) >= 2:
                    continue
                if mode in ("B", "C", "D") and near(s, i, 3):
                    continue
                pend.append(s)
                sec[SECTORS[s]] = sec.get(SECTORS[s], 0) + 1
                free -= 1
    return dict(eq=eq, spy=[spyb[i][C] for i in range(i0, i1 + 1)], trades=[], start=dates[i0], end=dates[i1],
                exits=n_exits)


def cagr(x):
    return (x[-1] / x[0]) ** (252 / len(x)) - 1


def mdd(x):
    pk, d = x[0], 0.0
    for v in x:
        pk = max(pk, v); d = min(d, v / pk - 1)
    return d


def main():
    dates, bars, spyb = load("LONG")
    react = reaction_index(dates)
    # validity check: is the assigned reaction day the big-move day?
    def absr(s, i):
        return abs(bars[s][i][C] / bars[s][i - 1][C] - 1) if bars[s][i] and bars[s][i - 1] else None
    cells = []
    for off in (-1, 0, 1):
        v = [absr(s, i + off) for s, ix in react.items() for i in ix if 1 <= i + off < len(dates)]
        v = [x for x in v if x is not None]
        cells.append(f"day {off:+d}: mean |ret| {sum(v) / len(v) * 100:.2f}% (n={len(v)})")
    allv = [abs(bars["AAPL"][i][C] / bars["AAPL"][i - 1][C] - 1) for i in range(1, len(dates))]
    print("validity: " + " | ".join(cells) + f" | AAPL all days {sum(allv) / len(allv) * 100:.2f}%")
    # event level, momentum-eligible at the pre-reaction close
    R, thru = [], 0
    for s, ix in react.items():
        for i in ix:
            a = i - 1
            if a < 253 or i >= len(dates):
                continue
            seq = bars[s]
            s200, m = sma(seq, a, 200), mom_12_1(seq, a)
            if s200 and m is not None and seq[a][C] > s200 and m > 0:
                r = seq[i][C] / seq[a][C] - 1
                R.append(r); thru += r <= -0.08
    m = sum(R) / len(R); sd = math.sqrt(sum((x - m) ** 2 for x in R) / (len(R) - 1))
    print(f"event level, momentum-eligible: n={len(R)} mean reaction {m * 100:+.2f}% t={m / (sd / math.sqrt(len(R))):+.2f} "
          f"share <= -8%: {thru / len(R) * 100:.1f}%")
    print("\nportfolio, LONG 14 names (in-sample, price returns, survivorship-biased):")
    res = {}
    for mode in ("A", "B", "C", "D"):
        r = run(dates, bars, spyb, react, mode)
        res[mode] = r
        print(f"  {mode}: CAGR {cagr(r['eq']) * 100:6.2f}%  maxDD {mdd(r['eq']) * 100:6.1f}%  earnings exits {r['exits']}  "
              f"SPY {cagr(r['spy']) * 100:.2f}%")
    for x, y in (("B", "A"), ("C", "B"), ("D", "B")):
        print(f"  {x} - {y}: {(cagr(res[x]['eq']) - cagr(res[y]['eq'])) * 100:+.2f}pp CAGR, daily t {daily_t(res[y]['eq'], res[x]['eq']):+.2f}")
    idx = list(range(len(dates)))
    st = next(i for i, d in enumerate(dates) if d >= res["A"]["start"])
    half = dates[st + (len(dates) - st) // 2]
    for lab, s0, s1 in (("1st half", None, half), ("2nd half", half, None)):
        b, c = run(dates, bars, spyb, react, "B", s0, s1), run(dates, bars, spyb, react, "C", s0, s1)
        print(f"  {lab}: B {cagr(b['eq']) * 100:6.2f}% DD {mdd(b['eq']) * 100:5.1f}%  C {cagr(c['eq']) * 100:6.2f}% DD {mdd(c['eq']) * 100:5.1f}%")
    nm = [s for s in bars if s not in MEGA]
    b, c = run(dates, bars, spyb, react, "B", syms=nm), run(dates, bars, spyb, react, "C", syms=nm)
    print(f"  megacaps dropped: B {cagr(b['eq']) * 100:6.2f}%  C {cagr(c['eq']) * 100:6.2f}%")
    edges = [st + (len(dates) - st) * k // 9 for k in range(9)] + [len(dates) - 1]
    cells, w = [], 0
    for k in range(9):
        b = run(dates, bars, spyb, react, "B", dates[edges[k]], dates[edges[k + 1]])
        c = run(dates, bars, spyb, react, "C", dates[edges[k]], dates[edges[k + 1]])
        g = cagr(c["eq"]) - cagr(b["eq"]); cells.append(f"{g * 100:+.1f}"); w += g > 0
    print(f"  walk-forward C - B (pp): {' '.join(cells)} -> C ahead {w} of 9")


if __name__ == "__main__":
    main()
