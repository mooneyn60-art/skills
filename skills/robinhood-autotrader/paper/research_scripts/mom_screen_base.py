#!/usr/bin/env python3
"""
Shared harness for the 2026-10-18 swarm: the live momentum screen as a
backtest, with hooks so each worker changes exactly ONE thing.
Prints data only (R14.1). Design: research/2026-10-18_MOMENTUM_SCREEN_SWARM.md.

BASELINE (the live screen, routines/HOURLY_TRADING_CHECK.md "MOMENTUM REBUILD"):
  - monthly ranking on the first trading day: 12-1 momentum
    = close[t-21] / close[t-252] - 1, must be > 0;
  - eligible: close > 200-day SMA and 63-day annualised vol <= 80%;
  - max 2 names per sector, 8 slots, each slot = 85% of equity / 8 at entry
    (15% cash floor), fractional shares;
  - entry at the NEXT day's open; 5bp per side;
  - exits: stop = max(0.92 x entry, entry once a close >= 1.08 x entry,
    0.80 x highest close), checked on the day's low, filled at
    min(open, stop) so gaps fill through; trend exit when close < 200-day
    (filled next open);
  - slots refill only at the monthly rebalance. No earnings filter (no
    complete point-in-time earnings dates; noted as a deviation).

Universes:
  LONG : paper/history/daily_ohlcv.json, 14 names (SPY excluded), 2006-2026.
  WIDE : LONG + daily_ohlcv_volatile.json + daily_ohlcv_holdings.json
         (41 names); a name joins once it has 252 bars. 2021-12 on.
Both are survivorship-biased (names chosen in 2026).

Hooks a worker may pass to run():
  score_fn(bars, i)            -> momentum score or None (default 12-1)
  eligible_fn(sym, bars, i)    -> bool, extra eligibility on top of the base
  pick_filter(cands, ctx)      -> filtered list of (sym, score) at rebalance
  entry_mode="monthly" | "pullback" (pullback: daily, see pullback_ok)
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
HIST = os.path.join(HERE, "..", "history")
O, H, L, C = 0, 1, 2, 3
MEGA = {"AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"}

SECTORS = {
    # LONG (engine.py map)
    "AAPL": "tech", "MSFT": "tech", "NVDA": "tech", "CSCO": "tech", "IBM": "tech",
    "GOOGL": "comm", "T": "comm", "AMZN": "retail", "BAC": "finance", "C": "finance",
    "F": "auto", "GE": "industrial", "PFE": "health", "XOM": "energy",
    # volatile (hand-assigned, Robinhood-style labels)
    "AFRM": "finance", "AMD": "tech", "COIN": "finance", "CRWD": "tech", "DKNG": "consumer",
    "ENPH": "energy", "HOOD": "finance", "MARA": "crypto", "MU": "tech", "NET": "tech",
    "NFLX": "comm", "PLTR": "tech", "RIOT": "crypto", "RIVN": "auto", "ROKU": "comm",
    "SHOP": "tech", "SNAP": "comm", "SOFI": "finance", "TSLA": "auto", "UBER": "industrial",
    "UPST": "finance",
    # holdings
    "ABBV": "health", "CVE": "energy", "EXEL": "health", "INTC": "tech", "NWG": "finance",
    "TGT": "retail",
}


def load(universe="LONG"):
    files = ["daily_ohlcv.json"] + (["daily_ohlcv_volatile.json", "daily_ohlcv_holdings.json"]
                                   if universe == "WIDE" else [])
    raw = {}
    for f in files:
        for s, rows in json.load(open(os.path.join(HIST, f))).items():
            raw.setdefault(s, rows)
    spy = raw.pop("SPY")
    dates = sorted(spy)
    bars = {}
    for s, rows in raw.items():
        seq, last = [], None
        for d in dates:
            r = rows.get(d)
            if r is not None:
                last = [float(x) for x in r[:4]]
                seq.append(last)
            else:
                seq.append(None if last is None else last)  # carry forward; None before listing
        bars[s] = seq
    spyb = [[float(x) for x in spy[d][:4]] for d in dates]
    return dates, bars, spyb


def first_valid(seq):
    return next((i for i, b in enumerate(seq) if b is not None), len(seq))


def sma(seq, i, n):
    if i - n + 1 < 0 or seq[i - n + 1] is None:
        return None
    return sum(seq[j][C] for j in range(i - n + 1, i + 1)) / n


def vol63(seq, i):
    if i - 63 < 0 or seq[i - 63] is None:
        return None
    r = [math.log(seq[j][C] / seq[j - 1][C]) for j in range(i - 62, i + 1)]
    m = sum(r) / len(r)
    return math.sqrt(sum((x - m) ** 2 for x in r) / (len(r) - 1) * 252)


def mom_12_1(seq, i):
    if i - 252 < 0 or seq[i - 252] is None:
        return None
    return seq[i - 21][C] / seq[i - 252][C] - 1


def pullback_ok(seq, i):
    """Variant (a): 3-8% below the 20-day high close, still above the 50-day."""
    if i - 20 < 0 or seq[i - 19] is None:
        return False
    hi = max(seq[j][C] for j in range(i - 19, i + 1))
    dd = 1 - seq[i][C] / hi
    s50 = sma(seq, i, 50)
    return 0.03 <= dd <= 0.08 and s50 is not None and seq[i][C] > s50


def run(dates, bars, spyb, start=None, end=None, syms=None, score_fn=mom_12_1,
        eligible_fn=None, pick_filter=None, entry_mode="monthly", slots=8, cost=0.0005):
    syms = sorted(syms or bars)
    i0 = next(i for i, d in enumerate(dates) if d >= (start or "0000"))
    i1 = max(i for i, d in enumerate(dates) if d <= (end or "9999"))
    i0 = max(i0, 253)
    cash, pos, trades, eq = 1.0, {}, [], []
    pending, watch = [], []
    month = None
    bought_this_month = set()   # pullback mode: no same-month re-buys (fix 2026-10-18, worker a)
    for i in range(i0, i1 + 1):
        d = dates[i]
        # 1. fill pending entries at today's open
        for s in pending:
            if s in pos or bars[s][i] is None or len(pos) >= slots:
                continue
            equity = cash + sum(p["q"] * bars[x][i][O] for x, p in pos.items())
            px = bars[s][i][O] * (1 + cost)
            amt = min(equity * 0.85 / slots, cash - equity * 0.15)
            if amt <= 0:
                continue
            q = amt / px
            cash -= q * px
            pos[s] = dict(q=q, e=px, hi=bars[s][i][O], stop=0.92 * px, d0=i, exit_next=False)
        pending = []
        # 2. exits
        for s in list(pos):
            p, b = pos[s], bars[s][i]
            if p["exit_next"]:
                fill = b[O] * (1 - cost)
                why = "trend"
            elif b[L] <= p["stop"]:
                fill = min(b[O], p["stop"]) * (1 - cost)
                why = "stop"
            else:
                continue
            cash += p["q"] * fill
            trades.append(dict(sym=s, entry=p["e"], exit=fill, ret=fill / p["e"] - 1, why=why,
                               hold=i - p["d0"], d=d))
            del pos[s]
        # 3. end-of-day updates
        for s, p in pos.items():
            b = bars[s][i]
            p["hi"] = max(p["hi"], b[C])
            p["stop"] = max(p["stop"], 0.80 * p["hi"], p["e"] if b[C] >= 1.08 * p["e"] else 0)
            s200 = sma(bars[s], i, 200)
            p["exit_next"] = s200 is not None and b[C] < s200
        equity = cash + sum(p["q"] * bars[s][i][C] for s, p in pos.items())
        eq.append(equity)
        # 4. ranking (monthly) and entry signals
        new_month = d[:7] != month
        month = d[:7]
        if new_month or entry_mode == "pullback":
            if new_month:
                bought_this_month = set()
                cands = []
                for s in syms:
                    seq = bars[s]
                    if seq[i] is None or i - first_valid(seq) < 252:
                        continue
                    sc = score_fn(seq, i)
                    s200, v = sma(seq, i, 200), vol63(seq, i)
                    if sc is None or sc <= 0 or s200 is None or v is None:
                        continue
                    if seq[i][C] <= s200 or v > 0.80:
                        continue
                    if eligible_fn and not eligible_fn(s, bars, i):
                        continue
                    cands.append((s, sc))
                cands.sort(key=lambda x: -x[1])
                if pick_filter:
                    cands = pick_filter(cands, dict(bars=bars, i=i, syms=syms))
                watch = cands
            free = slots - len(pos) - len(pending)
            sec = {}
            for s in pos:
                sec[SECTORS[s]] = sec.get(SECTORS[s], 0) + 1
            for s, _ in watch:
                if free <= 0:
                    break
                if s in pos or s in pending or sec.get(SECTORS[s], 0) >= 2:
                    continue
                if entry_mode == "pullback":
                    s200 = sma(bars[s], i, 200)
                    if (s in bought_this_month or not pullback_ok(bars[s], i)
                            or s200 is None or bars[s][i][C] <= s200):
                        continue
                    bought_this_month.add(s)
                pending.append(s)
                sec[SECTORS[s]] = sec.get(SECTORS[s], 0) + 1
                free -= 1
    spy_seg = [spyb[i][C] for i in range(i0, i1 + 1)]
    return dict(eq=eq, trades=trades, spy=spy_seg, start=dates[i0], end=dates[i1])


def stats(res):
    eq = res["eq"]
    yrs = len(eq) / 252
    peak, dd = eq[0], 0.0
    for v in eq:
        peak = max(peak, v)
        dd = min(dd, v / peak - 1)
    cagr = (eq[-1] / eq[0]) ** (1 / yrs) - 1
    spy = res["spy"]
    scagr = (spy[-1] / spy[0]) ** (1 / yrs) - 1
    tr = res["trades"]
    wins = sum(1 for t in tr if t["ret"] > 0)
    return dict(cagr=cagr, dd=dd, spy=scagr, n=len(tr), win=wins / len(tr) if tr else float("nan"),
                avg=sum(t["ret"] for t in tr) / len(tr) if tr else float("nan"))


def daily_t(a, b):
    """t-stat of the mean daily return difference b - a (same dates)."""
    n = min(len(a), len(b))
    diff = [b[i] / b[i - 1] - a[i] / a[i - 1] for i in range(1, n)]
    m = sum(diff) / len(diff)
    sd = math.sqrt(sum((x - m) ** 2 for x in diff) / (len(diff) - 1))
    return m / (sd / math.sqrt(len(diff))) if sd else float("nan")


def line(label, res):
    s = stats(res)
    return (f"  {label:<34} {res['start']}..{res['end']}  CAGR {s['cagr'] * 100:6.2f}%  maxDD {s['dd'] * 100:6.1f}%  "
            f"SPY {s['spy'] * 100:6.2f}%  trades {s['n']:>4}  win {s['win'] * 100:4.0f}%  avg/trade {s['avg'] * 100:+.2f}%")


def hurdles(label, universe, **variant):
    """Baseline vs one variant through split, 9-window walk-forward, megacap drop. Data only."""
    dates, bars, spyb = load(universe)
    lo = "2006-01-01" if universe == "LONG" else "2021-12-01"
    print(f"\n=== {label} | universe {universe} ({len(bars)} names) ===")
    a = run(dates, bars, spyb, start=lo)
    b = run(dates, bars, spyb, start=lo, **variant)
    print(line("baseline", a))
    print(line("variant", b))
    print(f"  diff CAGR {(stats(b)['cagr'] - stats(a)['cagr']) * 100:+.2f}pp  daily-return t (variant - baseline) "
          f"{daily_t(a['eq'], b['eq']):+.2f}")
    mid = a["start"][:4]
    idx = [i for i, d in enumerate(dates) if d >= a["start"]]
    half = dates[idx[len(idx) // 2]]
    for lab, s0, s1 in (("1st half", lo, half), ("2nd half", half, None)):
        aa = run(dates, bars, spyb, start=s0, end=s1)
        bb = run(dates, bars, spyb, start=s0, end=s1, **variant)
        print(f"  {lab}: baseline {stats(aa)['cagr'] * 100:6.2f}%  variant {stats(bb)['cagr'] * 100:6.2f}%  "
              f"diff {(stats(bb)['cagr'] - stats(aa)['cagr']) * 100:+.2f}pp")
    no_mega = [s for s in bars if s not in MEGA]
    aa = run(dates, bars, spyb, start=lo, syms=no_mega)
    bb = run(dates, bars, spyb, start=lo, syms=no_mega, **variant)
    print(f"  megacaps dropped: baseline {stats(aa)['cagr'] * 100:6.2f}%  variant {stats(bb)['cagr'] * 100:6.2f}%  "
          f"diff {(stats(bb)['cagr'] - stats(aa)['cagr']) * 100:+.2f}pp")
    edges = [idx[len(idx) * k // 9] for k in range(9)] + [idx[-1]]
    w = 0
    cells = []
    for k in range(9):
        s0, s1 = dates[edges[k]], dates[edges[k + 1]]
        aa = run(dates, bars, spyb, start=s0, end=s1)
        bb = run(dates, bars, spyb, start=s0, end=s1, **variant)
        g = stats(bb)["cagr"] - stats(aa)["cagr"]
        w += g > 1e-9
        cells.append(f"{g * 100:+.1f}")
    print(f"  walk-forward 9 windows (variant - baseline, pp CAGR): {' '.join(cells)}  -> variant ahead {w} of 9")
    _ = mid


if __name__ == "__main__":
    for u in ("LONG", "WIDE"):
        dates, bars, spyb = load(u)
        lo = "2006-01-01" if u == "LONG" else "2021-12-01"
        print(line(f"BASELINE {u} ({len(bars)} names)", run(dates, bars, spyb, start=lo)))
