#!/usr/bin/env python3
"""
A portfolio simulator for TARS. One engine, many rulesets.

WHY THIS EXISTS
---------------
test_r2_conditions.py and test_r4_exits.py both test ONE RULE AT A TIME on ONE
SYMBOL AT A TIME, always fully invested. That was enough to show that R2's
rules 2-3 and R4's trail cost return. It is not enough to test TARS, because
TARS is not a rule -- it is a portfolio with a fixed amount of money in it, and
most of what governs this account only exists at the portfolio level:

    R3   position sizing, the per-position cap, the 15% cash floor
    R5   at most 2 positions per sector
    R6   the circuit breaker: 2 stop-outs in 5 days pauses entries
    R12  WHOLE SHARES ONLY -- the rule that quantizes every position weight

R12 is the one that cannot be tested any other way, and it is the one I
suspect costs the most. On 2026-09-21 ABBV sat at 25.2% of the book and INTC
at 11.4%, not because anyone decided that, but because ABBV's share price is
$265 and INTC's is $101. At $1,320 of capital, share price IS position sizing.
A per-symbol test is blind to that by construction.

WHAT THIS ENGINE DOES NOT MODEL
-------------------------------
Commissions (Robinhood charges none), dividends (so every return here is a
PRICE return and understates buy-and-hold most of all), borrow, taxes, and
intraday stop-running below the daily low. Bid-ask is charged as a flat
one-way `slip` on entries and exits, default 5bp, which is a guess and is
labelled as one. Survivorship is REAL AND UNFIXED: these 14 names all survived
to 2026, so every number here flatters every strategy that holds stocks.
Comparisons between rulesets on the same universe remain valid; the absolute
CAGRs do not transfer to a live account.

Usage:  python3 engine.py        (runs the built-in comparison)
        from engine import simulate, Config
"""
import json, math, os
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "history", "daily_stocks.json")
O, H, L, C = 0, 1, 2, 3

# Sector map for R5. Hand-assigned to match how Robinhood labels these names,
# which is what the live rule actually reads.
SECTORS = {
    "AAPL": "tech", "MSFT": "tech", "NVDA": "tech", "CSCO": "tech",
    "IBM": "tech", "GOOGL": "comm", "T": "comm", "AMZN": "retail",
    "BAC": "finance", "C": "finance", "F": "auto", "GE": "industrial",
    "PFE": "health", "XOM": "energy",
}


@dataclass
class Config:
    # --- R2, entry ---
    ma_slow: int = 200          # rule 1
    use_ma_fast: bool = True    # rule 2
    ma_fast: int = 50
    prox_window: int = 20       # rule 3
    prox: float = 0.95          # within 5% of the 20-day high
    # --- R4, exit ---
    stop_pct: float = 0.08      # initial hard stop; None disables
    raise_mode: str = "trail"   # "none" | "breakeven" | "trail"
    trail_pct: float = None     # defaults to stop_pct, as R4 does today
    trend_exit: bool = True     # close below both MAs
    atr_stop: float = None      # if set, stop = N * ATR(14) instead of a %
    time_stop: int = None       # exit after N days regardless
    # --- R3, sizing and capacity ---
    sizing: str = "cap"         # "cap" | "equal" | "risk"
    cap_abs: float = 340.0
    cap_pct: float = 0.20
    cash_floor: float = 0.15
    risk_per_trade: float = 0.02   # for sizing="risk": fraction of equity at risk
    max_positions: int = 6
    whole_shares: bool = True   # R12
    # --- R5, R6 ---
    sector_cap: int = 2
    breaker_stops: int = 2      # N stop-outs...
    breaker_window: int = 5     # ...in M days...
    breaker_pause: int = 3      # ...pauses entries for P days
    halt_drawdown: float = 0.15
    halt_mode: str = "rebase"   # "latch" = R6 as literally written, never resumes
    halt_pause: int = 10        # cooling-off days before "rebase" resumes
    # --- costs and capital ---
    start_cash: float = 1320.0
    start_date: str = None      # restrict the window, for out-of-sample tests
    end_date: str = None
    slip: float = 0.0005        # one-way, each side
    name: str = "unnamed"


def load():
    raw = json.load(open(DATA))
    syms = sorted(k for k in raw if k != "SPY")
    dates = sorted(raw[syms[0]])
    bars = {s: [raw[s][d] for d in dates] for s in raw}
    return dates, bars, syms


def sma(bars, t, n):
    return sum(b[C] for b in bars[t - n + 1:t + 1]) / n


def atr(bars, t, n=14):
    """True range average. Needs bars[t-n..t]."""
    tot = 0.0
    for i in range(t - n + 1, t + 1):
        pc = bars[i - 1][C]
        tot += max(bars[i][H] - bars[i][L], abs(bars[i][H] - pc), abs(bars[i][L] - pc))
    return tot / n


def entry_signal(bars, t, cfg):
    """R2's price conditions at the close of t, from bars[0..t] only."""
    if t < max(cfg.ma_slow, cfg.prox_window, 15):
        return False
    px = bars[t][C]
    if px <= sma(bars, t, cfg.ma_slow):
        return False
    if cfg.use_ma_fast and px <= sma(bars, t, cfg.ma_fast):
        return False
    if cfg.prox is not None:
        hi = max(b[H] for b in bars[t - cfg.prox_window + 1:t + 1])
        if px < hi * cfg.prox:
            return False
    return True


def simulate(cfg, dates, bars, syms):
    cash = cfg.start_cash
    pos = {}                     # sym -> dict(qty, entry, stop, hi, day)
    pending_buy, pending_sell = [], []
    stop_days = []               # trading-day indices of recent stop-outs
    pause_until = -1
    high_water = cfg.start_cash
    halted = False
    halt_until = -1
    halts = []
    equity_curve, trades = [], []
    blocked_by_breaker = 0
    blocked_by_cash = 0
    blocked_by_granularity = 0

    start = max(cfg.ma_slow, cfg.prox_window, 15) + 1
    if cfg.start_date:
        start = max(start, next(i for i, d in enumerate(dates)
                                if d >= cfg.start_date))
    stop_at = len(dates)
    if cfg.end_date:
        stop_at = next((i for i, d in enumerate(dates) if d > cfg.end_date),
                       len(dates))
    for t in range(start, stop_at):
        # ---------- at the open: yesterday's decisions execute ----------
        for s in pending_sell:
            if s in pos:
                p = pos.pop(s)
                px = bars[s][t][O] * (1 - cfg.slip)
                cash += p["qty"] * px
                trades.append((s, p["entry"], px, p["qty"], t - p["day"], "trend"))
        pending_sell = []

        for s, qty in pending_buy:
            if s in pos or qty <= 0:
                continue
            px = bars[s][t][O] * (1 + cfg.slip)
            cost = qty * px
            if cost > cash:
                continue
            cash -= cost
            stop = None
            if cfg.atr_stop:
                stop = px - cfg.atr_stop * atr(bars[s], t - 1)
            elif cfg.stop_pct:
                stop = px * (1 - cfg.stop_pct)
            pos[s] = {"qty": qty, "entry": px, "stop": stop, "hi": px, "day": t}
        pending_buy = []

        # ---------- intraday: resting stops are live ----------
        for s in list(pos):
            p = pos[s]
            if p["stop"] is None:
                continue
            if bars[s][t][L] <= p["stop"]:
                raw = bars[s][t][O] if bars[s][t][O] <= p["stop"] else p["stop"]
                px = raw * (1 - cfg.slip)
                cash += p["qty"] * px
                trades.append((s, p["entry"], px, p["qty"], t - p["day"], "stop"))
                del pos[s]
                stop_days.append(t)

        # ---------- mark to market on the close ----------
        equity = cash + sum(p["qty"] * bars[s][t][C] for s, p in pos.items())
        equity_curve.append(equity)
        high_water = max(high_water, equity)
        if cfg.halt_drawdown and not halted and \
                equity < high_water * (1 - cfg.halt_drawdown):
            halted = True
            halts.append(t)
            # R6 AS WRITTEN HAS NO RESUME CONDITION -- it is a one-way latch.
            # "latch" reproduces that literally: the book never trades again.
            # "rebase" models what actually happens live, where Nolan reviews
            # and his next deposit resets the high-water mark.
            if cfg.halt_mode == "rebase":
                halt_until = t + cfg.halt_pause
        if halted and cfg.halt_mode == "rebase" and t >= halt_until:
            halted = False
            high_water = equity

        # ---------- raise stops on the close; never lower ----------
        for s, p in pos.items():
            px = bars[s][t][C]
            p["hi"] = max(p["hi"], px)
            if p["stop"] is None or cfg.raise_mode == "none":
                continue
            want = None
            if p["hi"] >= p["entry"] * 1.08:
                want = p["entry"]
                if cfg.raise_mode == "trail":
                    tp = cfg.trail_pct if cfg.trail_pct is not None else cfg.stop_pct
                    if cfg.atr_stop:
                        want = max(want, p["hi"] - cfg.atr_stop * atr(bars[s], t))
                    elif tp:
                        want = max(want, p["hi"] * (1 - tp))
            if want is not None and want > p["stop"]:
                p["stop"] = want

        # ---------- exit signals for tomorrow ----------
        for s, p in pos.items():
            px = bars[s][t][C]
            out = False
            if cfg.trend_exit:
                below_slow = px < sma(bars[s], t, cfg.ma_slow)
                below_fast = px < sma(bars[s], t, cfg.ma_fast)
                if below_slow and below_fast:
                    out = True
            if cfg.time_stop and t - p["day"] >= cfg.time_stop:
                out = True
            if out:
                pending_sell.append(s)

        # ---------- R6 breaker ----------
        stop_days = [d for d in stop_days if t - d < cfg.breaker_window]
        if len(stop_days) >= cfg.breaker_stops and t > pause_until:
            pause_until = t + cfg.breaker_pause
        if halted or t <= pause_until:
            if t <= pause_until and not halted:
                blocked_by_breaker += 1
            continue

        # ---------- entry signals for tomorrow ----------
        open_slots = cfg.max_positions - len(pos) - len(pending_buy)
        if open_slots <= 0:
            continue
        sector_n = {}
        for s in pos:
            sector_n[SECTORS[s]] = sector_n.get(SECTORS[s], 0) + 1

        cands = [s for s in syms
                 if s not in pos and s not in pending_sell
                 and entry_signal(bars[s], t, cfg)
                 and sector_n.get(SECTORS[s], 0) < cfg.sector_cap]
        # deterministic preference: strongest 20-day relative position first
        cands.sort(key=lambda s: -(bars[s][t][C] /
                                   max(b[H] for b in bars[s][t - 19:t + 1])))

        deployable = cash - equity * cfg.cash_floor
        for s in cands[:open_slots]:
            px = bars[s][t][C]
            if cfg.sizing == "cap":
                budget = min(cfg.cap_abs, equity * cfg.cap_pct)
            elif cfg.sizing == "equal":
                budget = equity / cfg.max_positions
            elif cfg.sizing == "risk":
                if cfg.atr_stop:
                    dist = cfg.atr_stop * atr(bars[s], t)
                else:
                    dist = px * cfg.stop_pct
                budget = (equity * cfg.risk_per_trade / dist) * px if dist > 0 else 0
                budget = min(budget, equity * cfg.cap_pct)
            budget = min(budget, deployable)
            if budget <= 0:
                blocked_by_cash += 1
                continue
            qty = math.floor(budget / px) if cfg.whole_shares else budget / px
            if qty < (1 if cfg.whole_shares else 1e-9):
                blocked_by_granularity += 1
                continue
            pending_buy.append((s, qty))
            deployable -= qty * px
            sector_n[SECTORS[s]] = sector_n.get(SECTORS[s], 0) + 1

    return {"equity": equity_curve, "trades": trades, "cfg": cfg,
            "halts": halts, "dates": dates,
            "blocked_breaker": blocked_by_breaker,
            "blocked_cash": blocked_by_cash,
            "blocked_gran": blocked_by_granularity}


def report(res):
    eq = res["equity"]
    cfg = res["cfg"]
    yrs = len(eq) / 252.0
    cagr = (eq[-1] / eq[0]) ** (1 / yrs) - 1
    peak, mdd = eq[0], 0.0
    rets = [eq[i] / eq[i - 1] - 1 for i in range(1, len(eq))]
    for v in eq:
        peak = max(peak, v)
        mdd = min(mdd, v / peak - 1)
    mean = sum(rets) / len(rets)
    sd = (sum((r - mean) ** 2 for r in rets) / len(rets)) ** 0.5
    sharpe = mean / sd * math.sqrt(252) if sd > 0 else 0.0
    tr = res["trades"]
    wins = [x for x in tr if x[2] > x[1]]
    return {"name": cfg.name, "cagr": cagr, "mdd": mdd, "sharpe": sharpe,
            "final": eq[-1], "trades": len(tr),
            "win": len(wins) / max(1, len(tr)),
            "stopped": sum(1 for x in tr if x[5] == "stop") / max(1, len(tr)),
            "hold": sum(x[4] for x in tr) / max(1, len(tr))}


def bench(dates, bars, start_cash, n):
    """SPY buy and hold over the same window, whole shares, same capital."""
    b = bars["SPY"]
    i0 = len(dates) - n
    qty = math.floor(start_cash / b[i0][C])
    cash = start_cash - qty * b[i0][C]
    eq = [cash + qty * b[i][C] for i in range(i0, len(dates))]
    yrs = len(eq) / 252.0
    peak, mdd = eq[0], 0.0
    for v in eq:
        peak = max(peak, v)
        mdd = min(mdd, v / peak - 1)
    return (eq[-1] / eq[0]) ** (1 / yrs) - 1, mdd, eq[-1]


HDR = (f"  {'ruleset':<34}{'CAGR':>8}{'maxDD':>9}{'Sharpe':>8}"
       f"{'final $':>10}{'trades':>8}{'win%':>7}{'stop%':>7}{'hold':>6}")


def line(r):
    return (f"  {r['name']:<34}{r['cagr']*100:7.2f}%{r['mdd']*100:8.1f}%"
            f"{r['sharpe']:8.2f}{r['final']:10,.0f}{r['trades']:8d}"
            f"{r['win']*100:6.1f}%{r['stopped']*100:6.1f}%{r['hold']:5.0f}d")


def main():
    dates, bars, syms = load()
    runs = [
        Config(name="TARS-1 as it stands today"),
        Config(name="TARS-1, trail widened to 20%", trail_pct=0.20),
        Config(name="TARS-1, no trail (breakeven only)", raise_mode="breakeven"),
        Config(name="drop R2 rule 2 (the 50d MA)", use_ma_fast=False),
        Config(name="drop R2 rule 3 (near-the-high)", prox=None),
        Config(name="drop rules 2 AND 3", use_ma_fast=False, prox=None),
        Config(name="ATR stop 3x, ATR trail", atr_stop=3.0, stop_pct=None),
        Config(name="risk-parity sizing (2%/trade)", sizing="risk"),
        Config(name="no circuit breaker", breaker_stops=99),
        Config(name="no cash floor", cash_floor=0.0),
        Config(name="FRACTIONAL shares allowed", whole_shares=False),
    ]
    print("TARS PORTFOLIO ENGINE -- 14 stocks, "
          f"{dates[0]} to {dates[-1]}, ${runs[0].start_cash:,.0f} start\n")
    print(HDR)
    print("  " + "-" * 97)
    n = None
    for cfg in runs:
        res = simulate(cfg, dates, bars, syms)
        n = len(res["equity"])
        print(line(report(res)))
    bc, bm, bf = bench(dates, bars, runs[0].start_cash, n)
    print("  " + "-" * 97)
    print(f"  {'SPY buy & hold, same capital':<34}{bc*100:7.2f}%{bm*100:8.1f}%"
          f"{'':>8}{bf:10,.0f}")
    print("\n  Price returns only -- no dividends, which understates buy & hold most."
          "\n  These 14 names all survived to 2026; survivorship flatters everything here.")


if __name__ == "__main__":
    main()
