"""
Options practice account: a fake SPY 0DTE market TARS can trade without money.

Simulates intraday SPY paths (5-minute steps, 9:30-16:00), prices 0DTE calls
and puts with Black-Scholes, charges a bid/ask spread on every fill, and runs
rule sets through a paper account with cash, positions, stops and a daily
loss limit. Prints DATA only (R14). See routines/OPTIONS_APPRENTICE.md.

Honest limits, read before using a number from this:
- The simulated market has NO edge for anyone by construction (random paths,
  options priced at slightly MORE vol than the path realizes, as in real
  markets). It teaches mechanics: time decay, how stops fill in fast moves,
  spread drag, how fast a size or loss rule ruins or saves an account.
  It cannot prove a strategy makes money. Only the live paper book can.
- VIX levels are drawn from the real 2006-2026 weekly VIX history.

Usage:
  python3 paper/options_sim.py                     # all scenarios, all rule sets
  python3 paper/options_sim.py --days 500 --seed 7
  python3 paper/options_sim.py --scenario trend
"""
import argparse
import json
import math
import random
from pathlib import Path
from statistics import mean, median

BASE = Path(__file__).resolve().parent
VIX_FILE = BASE / "history" / "vix_weekly.json"
STEPS = 78                 # 5-minute bars, 9:30 -> 16:00
MIN_PER_STEP = 5
YEAR_MIN = 252 * 390       # trading minutes per year
REALIZED_OVER_IMPLIED = 0.85   # paths realize less vol than options price in (set by --fair)
IV_PREMIUM = 1.05              # 0DTE options carry a small vol premium (set by --fair)
SPY0 = 775.0


def ncdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs(kind, s, k, t_years, vol):
    if t_years <= 1e-9 or vol <= 0:
        return max(0.0, s - k) if kind == "C" else max(0.0, k - s)
    sd = vol * math.sqrt(t_years)
    d1 = (math.log(s / k) + 0.5 * sd * sd) / sd
    d2 = d1 - sd
    if kind == "C":
        return s * ncdf(d1) - k * ncdf(d2)
    return k * ncdf(-d2) - s * ncdf(-d1)


def half_spread(mid):
    return max(0.01, 0.01 * mid)


def clock(step):
    m = 9 * 60 + 30 + step * MIN_PER_STEP
    return f"{m // 60}:{m % 60:02d}"


# ---------------------------------------------------------------- market paths
def make_day(rng, vix, scenario):
    """Return a list of STEPS+1 SPY prices for one day."""
    iv = vix / 100.0
    sig = iv * REALIZED_OVER_IMPLIED * math.sqrt(MIN_PER_STEP / YEAR_MIN)
    day_sd = sig * math.sqrt(STEPS)
    kind = scenario
    if scenario == "mixed":
        kind = rng.choices(["random", "trend", "chop", "gapfade"], [0.4, 0.25, 0.25, 0.1])[0]
    drift = 0.0
    if kind == "trend":
        drift = rng.choice([-1, 1]) * 0.8 * day_sd / STEPS
    s = SPY0 * (1 + (rng.gauss(0, 1.2 * day_sd) if kind == "gapfade" else 0.0))
    open_px = s
    path = [s]
    for i in range(STEPS):
        pull = 0.0
        if kind == "chop":
            pull = -0.08 * (s / open_px - 1)
        if kind == "gapfade" and i < 24:
            pull = -0.04 * (s / SPY0 - 1)
        s *= math.exp(drift + pull + rng.gauss(0, sig))
        path.append(s)
    return path, kind


# ---------------------------------------------------------------- rule sets
class Rules:
    def __init__(self, name, budget, stop, target, first_entry, last_entry, time_exit,
                 max_trades, day_stop, signal, hold_steps=None):
        self.__dict__.update(locals())


RULESETS = [
    # A model of the recent scalping style: lots of trades, either direction,
    # quick holds, bigger size, no daily stop.
    Rules("scalper (Nolan-style)", budget=400, stop=None, target=None, first_entry=3,
          last_entry=74, time_exit=77, max_trades=20, day_stop=None, signal="random",
          hold_steps=(1, 6)),
    # Candidate v0: wait for the opening range, trade breakouts only, fixed
    # small size, stop and target, out by 15:25, max 6 trades, daily stop.
    Rules("rules v0 (stop -25%)", budget=150, stop=0.25, target=0.50, first_entry=12,
          last_entry=60, time_exit=71, max_trades=6, day_stop=300, signal="breakout"),
    Rules("rules v0, stop -20%", budget=150, stop=0.20, target=0.50, first_entry=12,
          last_entry=60, time_exit=71, max_trades=6, day_stop=300, signal="breakout"),
    Rules("rules v0, stop -40%", budget=150, stop=0.40, target=0.50, first_entry=12,
          last_entry=60, time_exit=71, max_trades=6, day_stop=300, signal="breakout"),
    Rules("rules v0, no time exit", budget=150, stop=0.25, target=0.50, first_entry=12,
          last_entry=60, time_exit=78, max_trades=6, day_stop=300, signal="breakout"),
]


def run_day(rng, path, vix, r):
    """Trade one simulated day; return list of (pnl, reason)."""
    iv = vix / 100.0 * IV_PREMIUM
    trades = []
    day_pnl = 0.0
    hi = max(path[:7]); lo = min(path[:7])   # 30-minute opening range
    pos = None
    step = r.first_entry
    while step <= 77:
        s = path[step]
        t_left = (STEPS - step) * MIN_PER_STEP / YEAR_MIN
        if pos:
            mid = bs(pos["kind"], s, pos["k"], t_left, iv)
            bid = max(0.0, mid - half_spread(mid))
            reason = None
            if r.stop is not None and bid <= pos["px"] * (1 - r.stop):
                reason = "stop"
            elif r.target is not None and bid >= pos["px"] * (1 + r.target):
                reason = "target"
            elif r.hold_steps and step >= pos["until"]:
                reason = "time-hold"
            elif step >= r.time_exit:
                reason = "time-exit"
            if step == STEPS - 1 and reason is None:
                reason = "expiry"
            if reason:
                pnl = (bid - pos["px"]) * 100 * pos["n"]
                trades.append((pnl, reason))
                day_pnl += pnl
                pos = None
        elif (len(trades) < r.max_trades and step <= r.last_entry
              and (r.day_stop is None or day_pnl > -r.day_stop)):
            kind = None
            if r.signal == "random" and rng.random() < 0.35:
                kind = rng.choice("CP")
            elif r.signal == "breakout":
                if s > hi * 1.0005:
                    kind = "C"
                elif s < lo * 0.9995:
                    kind = "P"
            if kind:
                k = round(s)
                mid = bs(kind, s, k, t_left, iv)
                ask = mid + half_spread(mid)
                if ask >= 0.05:
                    n = max(1, int(r.budget // (ask * 100)))
                    until = step + (rng.randint(*r.hold_steps) if r.hold_steps else 99)
                    pos = {"kind": kind, "k": k, "px": ask, "n": n, "until": until}
        step += 1
    return trades


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, max(0, int(q * len(xs))))]


def simulate(days, seed, scenario, start_cash=2000.0, horizon=60):
    rng = random.Random(seed)
    vix_hist = list(json.load(open(VIX_FILE)).values())
    print(f"SCENARIO {scenario}: {days} simulated days, seed {seed}, start cash {start_cash:.0f}, "
          f"ruin check over {horizon}-day runs")
    print(f"  {'rule set':<24} {'trades/day':>10} {'per trade':>10} {'win%':>5} "
          f"{'median day':>10} {'5% worst day':>12} {'worst day':>9} {'P(-50% in 60d)':>14}")
    day_set = []
    for _ in range(days):
        vix = rng.choice(vix_hist)
        path, kind = make_day(rng, vix, scenario)
        day_set.append((vix, path, rng.random()))
    for r in RULESETS:
        rr = random.Random(seed + 1)
        all_t, day_p = [], []
        for vix, path, _ in day_set:
            t = run_day(rr, path, vix, r)
            all_t += [p for p, _ in t]
            day_p.append(sum(p for p, _ in t))
        # ruin: chop daily P/L into 60-day runs from start_cash
        ruined = runs = 0
        for i in range(0, len(day_p) - horizon + 1, horizon):
            cash = start_cash
            for p in day_p[i:i + horizon]:
                cash += p
                if cash <= start_cash * 0.5:
                    ruined += 1
                    break
            runs += 1
        wins = sum(1 for p in all_t if p > 0)
        print(f"  {r.name:<24} {len(all_t) / days:>10.1f} {mean(all_t) if all_t else 0:>+10.2f} "
              f"{100 * wins / max(1, len(all_t)):>5.0f} {median(day_p):>+10.0f} "
              f"{pct(day_p, 0.05):>+12.0f} {min(day_p):>+9.0f} "
              f"{(f'{ruined}/{runs}') if runs else 'n/a':>14}")


def main():
    ap = argparse.ArgumentParser(description="SPY 0DTE practice simulator (no real orders)")
    ap.add_argument("--days", type=int, default=1200)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--fair", action="store_true",
                    help="no vol premium: options priced at exactly the vol the path realizes")
    ap.add_argument("--scenario", choices=["random", "trend", "chop", "gapfade", "mixed", "all"],
                    default="all")
    a = ap.parse_args()
    global REALIZED_OVER_IMPLIED, IV_PREMIUM
    if a.fair:
        REALIZED_OVER_IMPLIED, IV_PREMIUM = 1.0, 1.0
        print("FAIR MARKET: options priced at the realized vol; only the bid/ask spread costs you\n")
    scen = ["random", "trend", "chop", "gapfade", "mixed"] if a.scenario == "all" else [a.scenario]
    for sc in scen:
        simulate(a.days, a.seed, sc)
        print()


if __name__ == "__main__":
    main()
