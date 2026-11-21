"""
Momentum vs reversal by horizon -- mechanical, pre-registered signal test.

RESEARCH_AGENDA item 12. Predictions were written and committed BEFORE this
script was run (research/2026-09-24_MOMENTUM_VS_REVERSAL.md, commit b82b430).
This script implements the test described there. It prints raw numbers only
-- no conclusions are hardcoded here; the verdict is written into the note by
hand after reading this output.

Universes: 14 large caps (AAPL AMZN BAC C CSCO F GE GOOGL IBM MSFT NVDA PFE T
XOM), SPY EXCLUDED from rankings (paper/history/daily_ohlcv.json); 22 volatile
names with uneven start dates (paper/history/daily_ohlcv_volatile.json).
Schema {SYM: {date: [o,h,l,c,v]}}.

-----------------------------------------------------------------------------
DESIGN (written before looking at any results)
-----------------------------------------------------------------------------

Monthly rebalance at month-end (the last trading day present in the pooled
calendar for each calendar month). Look-backs, in trading days ending at the
rebalance date t (inclusive of t as the "now" price):

  1w    =   5 days:  C[t] / C[t-5]   - 1
  1m    =  21 days:  C[t] / C[t-21]  - 1
  3m    =  63 days:  C[t] / C[t-63]  - 1
  6m    = 126 days:  C[t] / C[t-126] - 1
  12-1m = 252 days, skipping the latest 21: C[t-21] / C[t-252] - 1

Forward return: the next 21 trading days, C[t+21] / C[t] - 1.

Per universe, per month, per look-back: cross-sectional Spearman rank
correlation (rank IC) between the look-back return and the forward return,
across every name that HAS DATA at date t (handles the volatile universe's
uneven start dates -- a name simply isn't in a given month's cross-section
until its history covers the full look-back). Reported across months: mean
IC, a t-stat (mean / (stdev/sqrt(n))) against zero, and % of months with
IC > 0. Also a top-third minus bottom-third spread of forward returns (sort
that month's cross-section by look-back return, split into thirds by count,
compare mean forward return of top vs bottom third), with its mean and t
across months.

Sample split: large caps at 2016-06-01 (roughly the middle of the pooled
history); volatile names at 2021-01-01 (most names IPO'd/data-started
2020-2021, so this splits "early, thin cross-section" from "mature, full
cross-section").

Time-series version (per name, then averaged): for each name, regress its
forward 21-day return on the SIGN of its own past return over each look-back
(OLS, forward = alpha + beta*sign(lookback)), across that name's own
rebalance months. Average alpha and beta across names; a one-sample t-test
of the cross-name beta distribution against zero.

The 200-day gate: at each rebalance date with a valid 200-day SMA, split
name-months into close > SMA200 vs close < SMA200. Compare mean forward 21-
and 63-day returns between the two groups, per universe, with a Welch t-stat
on the difference.

TARS's holding horizon: (a) from paper/trades.jsonl, the median/mean holding
days (calendar) of TARS's own closed live trades -- strategy starting "TARS",
non-null opened AND closed, a real fill (realized_pnl not null), deduplicated
on (symbol, opened, closed, realized_pnl) since the ledger's append-only
correction convention re-writes some records verbatim. (b) A simulation of
R4's exit ladder (8% hard stop, breakeven raise at +8%, 20% trail below the
highest close since entry, plus a 200-day trend exit on a closing basis) on
entries taken at every month-end when close > SMA200, per universe, reporting
the distribution of simulated holding days in TRADING days (not calendar --
this is the number comparable to "252 days" style horizons above, whereas the
live ledger figure in (a) is calendar days because the account is only ~2
weeks old and every trade there closed within days).
-----------------------------------------------------------------------------
"""

import json
import math
from pathlib import Path
from statistics import mean, stdev, median

BASE = Path(__file__).resolve().parents[2]
LARGE_CAP_FILE = BASE / "paper" / "history" / "daily_ohlcv.json"
VOLATILE_FILE = BASE / "paper" / "history" / "daily_ohlcv_volatile.json"
TRADES_FILE = BASE / "paper" / "trades.jsonl"

LOOKBACKS = [("1w", 5), ("1m", 21), ("3m", 63), ("6m", 126)]
MOM_121_NAME = "12-1m"
MOM_121_LONG = 252
MOM_121_SKIP = 21
FORWARD = 21
SMA_GATE = 200

LARGE_CAP_SPLIT = "2016-06-01"
VOLATILE_SPLIT = "2021-01-01"


# -----------------------------------------------------------------------------
# Loading
# -----------------------------------------------------------------------------

def load_universe(path, exclude=()):
    with open(path) as f:
        raw = json.load(f)
    series = {}
    for sym, bars in raw.items():
        if sym in exclude:
            continue
        dates = sorted(bars.keys())
        closes = [bars[d][3] for d in dates]
        series[sym] = {"dates": dates, "C": closes, "idx": {d: i for i, d in enumerate(dates)}}
    return series


def month_end_dates(series):
    """Last trading date present in the pooled calendar for each YYYY-MM."""
    all_dates = set()
    for s in series.values():
        all_dates.update(s["dates"])
    all_dates = sorted(all_dates)
    by_month = {}
    for d in all_dates:
        ym = d[:7]
        by_month[ym] = d  # sorted iteration keeps overwriting to the latest date in the month
    return sorted(by_month.values())


# -----------------------------------------------------------------------------
# Stats primitives (no scipy available in this environment; numpy is)
# -----------------------------------------------------------------------------

def spearman(xs, ys):
    """Spearman rank correlation, average-rank ties, no scipy dependency."""
    n = len(xs)
    if n < 3:
        return float("nan")

    def ranks(vals):
        order = sorted(range(len(vals)), key=lambda i: vals[i])
        r = [0.0] * len(vals)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
                j += 1
            avg_rank = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                r[order[k]] = avg_rank
            i = j + 1
        return r

    rx, ry = ranks(xs), ranks(ys)
    mx, my = mean(rx), mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    denx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    deny = math.sqrt(sum((b - my) ** 2 for b in ry))
    if denx == 0 or deny == 0:
        return float("nan")
    return num / (denx * deny)


def one_sample_t(vals):
    n = len(vals)
    if n < 2:
        return float("nan"), float("nan"), n
    m = mean(vals)
    sd = stdev(vals)
    if sd == 0:
        return float("nan"), m, n
    t = m / (sd / math.sqrt(n))
    return t, m, n


def welch_t(sample, baseline):
    n1, n2 = len(sample), len(baseline)
    if n1 < 2 or n2 < 2:
        return float("nan"), float("nan")
    m1, m2 = mean(sample), mean(baseline)
    v1, v2 = stdev(sample) ** 2, stdev(baseline) ** 2
    se = math.sqrt(v1 / n1 + v2 / n2)
    if se == 0:
        return float("nan"), m1 - m2
    return (m1 - m2) / se, m1 - m2


def ols_beta_alpha(xs, ys):
    """Simple OLS y = alpha + beta*x."""
    n = len(xs)
    if n < 2:
        return float("nan"), float("nan")
    mx, my = mean(xs), mean(ys)
    varx = sum((x - mx) ** 2 for x in xs)
    if varx == 0:
        return float("nan"), float("nan")
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    beta = cov / varx
    alpha = my - beta * mx
    return alpha, beta


def sma(closes, i, period):
    if i - period + 1 < 0:
        return None
    window = closes[i - period + 1: i + 1]
    return sum(window) / period


def fmt(x, nd=4):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "NA"
    return f"{x:.{nd}f}"


# -----------------------------------------------------------------------------
# Cross-sectional rank-IC + spread test
# -----------------------------------------------------------------------------

def lookback_return(series, sym, i, window, skip=0):
    C = series[sym]["C"]
    end = i - skip
    start = end - window
    if start < 0 or end < 0:
        return None
    return C[end] / C[start] - 1.0


def forward_return(series, sym, i, horizon):
    C = series[sym]["C"]
    if i + horizon >= len(C):
        return None
    return C[i + horizon] / C[i] - 1.0


def cross_sectional_month(series, mdates, horizon_name, window, skip=0):
    """For each month-end date, compute (lookback_ret, fwd_ret) pairs across
    every name with sufficient history at that date. Returns list of
    (date, [(sym, lb, fwd), ...])."""
    out = []
    for d in mdates:
        pairs = []
        for sym, s in series.items():
            idx = s["idx"].get(d)
            if idx is None:
                continue
            lb = lookback_return(series, sym, idx, window, skip)
            fwd = forward_return(series, sym, idx, FORWARD)
            if lb is None or fwd is None:
                continue
            pairs.append((sym, lb, fwd))
        if len(pairs) >= 3:
            out.append((d, pairs))
    return out


def rank_ic_and_spread(month_data):
    ics = []
    spreads = []
    for d, pairs in month_data:
        lbs = [p[1] for p in pairs]
        fwds = [p[2] for p in pairs]
        ic = spearman(lbs, fwds)
        if not math.isnan(ic):
            ics.append(ic)
        n = len(pairs)
        k = n // 3
        if k >= 1:
            ranked = sorted(pairs, key=lambda p: p[1])
            bottom = ranked[:k]
            top = ranked[-k:]
            spread = mean([p[2] for p in top]) - mean([p[2] for p in bottom])
            spreads.append(spread)
    ic_t, ic_mean, ic_n = one_sample_t(ics)
    pct_pos = 100.0 * sum(1 for x in ics if x > 0) / len(ics) if ics else float("nan")
    sp_t, sp_mean, sp_n = one_sample_t(spreads)
    return {
        "n_months": len(month_data),
        "ic_mean": ic_mean, "ic_t": ic_t, "ic_n": ic_n, "pct_pos": pct_pos,
        "spread_mean": sp_mean, "spread_t": sp_t, "spread_n": sp_n,
    }


def split_month_data(month_data, split_date):
    pre = [(d, p) for d, p in month_data if d < split_date]
    post = [(d, p) for d, p in month_data if d >= split_date]
    return pre, post


# -----------------------------------------------------------------------------
# Time-series version: per-name regression of fwd21 on sign(lookback)
# -----------------------------------------------------------------------------

def time_series_regression(series, mdates, window, skip=0):
    betas, alphas = [], []
    per_name_n = []
    for sym, s in series.items():
        xs, ys = [], []
        for d in mdates:
            idx = s["idx"].get(d)
            if idx is None:
                continue
            lb = lookback_return(series, sym, idx, window, skip)
            fwd = forward_return(series, sym, idx, FORWARD)
            if lb is None or fwd is None:
                continue
            xs.append(1.0 if lb > 0 else (-1.0 if lb < 0 else 0.0))
            ys.append(fwd)
        if len(xs) >= 12:  # need a minimally sane number of months per name
            a, b = ols_beta_alpha(xs, ys)
            if not math.isnan(b):
                alphas.append(a)
                betas.append(b)
                per_name_n.append(len(xs))
    beta_t, beta_mean, beta_n = one_sample_t(betas)
    alpha_mean = mean(alphas) if alphas else float("nan")
    return {
        "n_names": beta_n, "beta_mean": beta_mean, "beta_t": beta_t,
        "alpha_mean": alpha_mean,
        "avg_months_per_name": mean(per_name_n) if per_name_n else float("nan"),
    }


# -----------------------------------------------------------------------------
# 200-day gate comparison
# -----------------------------------------------------------------------------

def gate_200d(series, mdates):
    above21, below21 = [], []
    above63, below63 = [], []
    for d in mdates:
        for sym, s in series.items():
            idx = s["idx"].get(d)
            if idx is None:
                continue
            C = s["C"]
            sma200 = sma(C, idx, SMA_GATE)
            if sma200 is None:
                continue
            fwd21 = forward_return(series, sym, idx, 21)
            fwd63 = forward_return(series, sym, idx, 63)
            above = C[idx] > sma200
            if fwd21 is not None:
                (above21 if above else below21).append(fwd21)
            if fwd63 is not None:
                (above63 if above else below63).append(fwd63)
    t21, diff21 = welch_t(above21, below21)
    t63, diff63 = welch_t(above63, below63)
    return {
        "n_above": len(above21), "n_below": len(below21),
        "mean_above_21": mean(above21) if above21 else float("nan"),
        "mean_below_21": mean(below21) if below21 else float("nan"),
        "diff_21": diff21, "t_21": t21,
        "n_above_63": len(above63), "n_below_63": len(below63),
        "mean_above_63": mean(above63) if above63 else float("nan"),
        "mean_below_63": mean(below63) if below63 else float("nan"),
        "diff_63": diff63, "t_63": t63,
    }


# -----------------------------------------------------------------------------
# TARS live holding days from the ledger
# -----------------------------------------------------------------------------

def parse_iso(ts):
    ts = ts.replace("Z", "+00:00")
    # normalize fractional seconds length for fromisoformat portability
    from datetime import datetime
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        # trim/pad microseconds
        if "." in ts:
            head, rest = ts.split(".", 1)
            frac, tz = rest[:-6], rest[-6:]
            frac = (frac + "000000")[:6]
            ts = f"{head}.{frac}{tz}"
        return datetime.fromisoformat(ts)


def tars_ledger_holding_days():
    recs = []
    with open(TRADES_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            recs.append(r)

    seen = set()
    holds = []
    detail = []
    for r in recs:
        strat = r.get("strategy")
        if not isinstance(strat, str) or not strat.startswith("TARS"):
            continue
        opened, closed = r.get("opened"), r.get("closed")
        if not opened or not closed:
            continue
        if r.get("realized_pnl") is None:
            # research-only / not-taken records (e.g. R9_locked, not_taken) carry
            # opened==closed by construction and are not real filled trades
            continue
        key = (r.get("symbol"), opened, closed, r.get("realized_pnl"))
        if key in seen:
            continue
        seen.add(key)
        try:
            d_open = parse_iso(opened)
            d_close = parse_iso(closed)
        except Exception:
            continue
        days = (d_close - d_open).total_seconds() / 86400.0
        holds.append(days)
        detail.append((r.get("id"), r.get("symbol"), r.get("instrument"), round(days, 3), r.get("realized_pnl")))
    return holds, detail


# -----------------------------------------------------------------------------
# R4 exit-ladder simulation on 200-day-gated month-end entries
# -----------------------------------------------------------------------------

def simulate_r4_exits(series, mdates):
    """Enter at every month-end where close > SMA200. Simulate day-by-day:
    hard stop -8%, breakeven raise at +8%, 20% trail below highest close,
    and a 200-day trend exit (close < SMA200 on a completed daily bar).
    Returns list of holding days (trading days) for entries that reached a
    resolved exit before the data ended (censored trades at data-end are
    reported separately, per RULE #1's spirit: don't silently treat an
    unresolved trade as if it were closed)."""
    resolved_days = []
    censored = 0
    exit_reasons = {"hard_stop": 0, "trend_exit": 0}
    n_entries = 0
    mdate_set = set(mdates)
    for sym, s in series.items():
        C = s["C"]
        dates = s["dates"]
        n = len(C)
        for i, d in enumerate(dates):
            if d not in mdate_set:
                continue
            sma200 = sma(C, i, SMA_GATE)
            if sma200 is None or not (C[i] > sma200):
                continue
            n_entries += 1
            entry = C[i]
            stop = entry * 0.92
            highest_close = entry
            breakeven_hit = False
            exited = False
            for j in range(i + 1, n):
                c = C[j]
                if c > highest_close:
                    highest_close = c
                if not breakeven_hit and c >= entry * 1.08:
                    breakeven_hit = True
                    stop = max(stop, entry)
                if breakeven_hit:
                    stop = max(stop, highest_close * 0.80)
                sma200_j = sma(C, j, SMA_GATE)
                trend_exit = sma200_j is not None and c < sma200_j
                if c <= stop:
                    resolved_days.append(j - i)
                    exit_reasons["hard_stop"] += 1
                    exited = True
                    break
                if trend_exit:
                    resolved_days.append(j - i)
                    exit_reasons["trend_exit"] += 1
                    exited = True
                    break
            if not exited:
                censored += 1
    return {
        "n_entries": n_entries,
        "n_resolved": len(resolved_days),
        "n_censored_at_data_end": censored,
        "exit_reasons": exit_reasons,
        "mean_days": mean(resolved_days) if resolved_days else float("nan"),
        "median_days": median(resolved_days) if resolved_days else float("nan"),
        "p25_days": sorted(resolved_days)[len(resolved_days) // 4] if resolved_days else float("nan"),
        "p75_days": sorted(resolved_days)[3 * len(resolved_days) // 4] if resolved_days else float("nan"),
        "max_days": max(resolved_days) if resolved_days else float("nan"),
        "min_days": min(resolved_days) if resolved_days else float("nan"),
    }


# -----------------------------------------------------------------------------
# Report
# -----------------------------------------------------------------------------

def report_universe(name, series, split_date):
    print(f"\n{'=' * 78}\nUNIVERSE: {name}  ({len(series)} names)\n{'=' * 78}")
    mdates = month_end_dates(series)
    print(f"month-end dates in pooled calendar: {len(mdates)}  "
          f"({mdates[0]} .. {mdates[-1]})")

    horizon_specs = list(LOOKBACKS) + [(MOM_121_NAME, MOM_121_LONG)]

    print(f"\n--- Cross-sectional rank IC (lookback vs next-21d forward return) ---")
    header = f"{'horizon':8s} {'period':10s} {'months':>7s} {'IC_mean':>9s} {'IC_t':>8s} {'%pos':>6s} {'spread_mean':>12s} {'spread_t':>9s}"
    print(header)
    for hname, window in horizon_specs:
        skip = MOM_121_SKIP if hname == MOM_121_NAME else 0
        month_data = cross_sectional_month(series, mdates, hname, window, skip)
        pre, post = split_month_data(month_data, split_date)
        for label, md in (("full", month_data), ("pre-split", pre), ("post-split", post)):
            r = rank_ic_and_spread(md)
            print(f"{hname:8s} {label:10s} {r['n_months']:7d} {fmt(r['ic_mean'],4):>9s} "
                  f"{fmt(r['ic_t'],2):>8s} {fmt(r['pct_pos'],1):>6s} "
                  f"{fmt(r['spread_mean']*100,3):>11s}% {fmt(r['spread_t'],2):>9s}")

    print(f"\n--- Time-series version (per-name regression, forward21 ~ alpha + beta*sign(lookback)) ---")
    print(f"{'horizon':8s} {'n_names':>8s} {'avg_months/name':>16s} {'beta_mean':>10s} {'beta_t':>8s} {'alpha_mean':>11s}")
    for hname, window in horizon_specs:
        skip = MOM_121_SKIP if hname == MOM_121_NAME else 0
        r = time_series_regression(series, mdates, window, skip)
        print(f"{hname:8s} {r['n_names']:8d} {fmt(r['avg_months_per_name'],1):>16s} "
              f"{fmt(r['beta_mean']*100,3):>9s}% {fmt(r['beta_t'],2):>8s} {fmt(r['alpha_mean']*100,3):>10s}%")

    print(f"\n--- 200-day gate: forward returns, close>SMA200 vs close<SMA200 ---")
    g = gate_200d(series, mdates)
    print(f"  n above SMA200 (21d fwd sample): {g['n_above']}   n below: {g['n_below']}")
    print(f"  21d fwd: mean(above)={fmt(g['mean_above_21']*100,3)}%  mean(below)={fmt(g['mean_below_21']*100,3)}%  "
          f"diff={fmt(g['diff_21']*100,3)}pp  t={fmt(g['t_21'],2)}")
    print(f"  63d fwd: mean(above)={fmt(g['mean_above_63']*100,3)}%  mean(below)={fmt(g['mean_below_63']*100,3)}%  "
          f"diff={fmt(g['diff_63']*100,3)}pp  t={fmt(g['t_63'],2)}")

    print(f"\n--- R4 exit-ladder simulation, entries at month-end when close>SMA200 ---")
    sim = simulate_r4_exits(series, mdates)
    print(f"  entries: {sim['n_entries']}   resolved: {sim['n_resolved']}   "
          f"censored (still open at data end): {sim['n_censored_at_data_end']}")
    print(f"  exit reasons among resolved: {sim['exit_reasons']}")
    print(f"  holding days (trading days): mean={fmt(sim['mean_days'],1)}  median={fmt(sim['median_days'],1)}  "
          f"p25={fmt(sim['p25_days'],1)}  p75={fmt(sim['p75_days'],1)}  min={fmt(sim['min_days'],1)}  max={fmt(sim['max_days'],1)}")

    return {"gate": g, "sim": sim}


def main():
    large = load_universe(LARGE_CAP_FILE, exclude={"SPY"})
    volatile = load_universe(VOLATILE_FILE)

    print("MOMENTUM VS REVERSAL BY HORIZON -- raw output, no conclusions baked in")
    print(f"Large-cap universe: {sorted(large.keys())}")
    print(f"Volatile universe:  {sorted(volatile.keys())}")

    report_universe("large caps (SPY excluded)", large, LARGE_CAP_SPLIT)
    report_universe("volatile names", volatile, VOLATILE_SPLIT)

    print(f"\n{'=' * 78}\nTARS LIVE LEDGER HOLDING DAYS\n{'=' * 78}")
    holds, detail = tars_ledger_holding_days()
    print(f"n closed TARS-strategy trades (deduped, real fills only): {len(holds)}")
    for row in detail:
        print(f"  {row}")
    if holds:
        print(f"mean holding days (calendar): {fmt(mean(holds),2)}")
        print(f"median holding days (calendar): {fmt(median(holds),2)}")
        print(f"min={fmt(min(holds),2)}  max={fmt(max(holds),2)}")
    else:
        print("no qualifying records found")


if __name__ == "__main__":
    main()
