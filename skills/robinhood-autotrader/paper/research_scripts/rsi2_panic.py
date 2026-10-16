"""
RSI(2) "buy the dip in an uptrend" (Connors & Alvarez) + a pooled test of
"oversold only works in a panic" -- mechanical, pre-registered signal + system
test.

RESEARCH_AGENDA item. Predictions were written and committed BEFORE this
script was run (research/2026-09-24_RSI2_AND_PANIC_DIPS.md, commit 52bed82).
This script implements the tests described there. It prints raw numbers
only -- no conclusions are hardcoded here; the verdict is written into the
note by hand after reading this output.

Universe: 14 large caps (AAPL AMZN BAC C CSCO F GE GOOGL IBM MSFT NVDA PFE T
XOM) + SPY, daily OHLCV, 2006-01-03 to 2026-09-23
(paper/history/daily_ohlcv.json). Weekly VIX closes (paper/history/
vix_weekly.json) for Part B's VIX-regime split.

Loading, Wilder RSI, SMA, Welch t-test and dedup follow
paper/research_scripts/indicators_price.py and indicators_volume_vwap.py for
consistency, duplicated here (no cross-script imports, matching existing
convention).

-----------------------------------------------------------------------------
PART A -- RSI(2) SYSTEM (Connors & Alvarez, "Short Term Trading Strategies
That Work", 2008)
-----------------------------------------------------------------------------
RSI(2), Wilder: identical formula to RSI(14) elsewhere in this repo, period=2
(first value at day index 2 uses a simple 2-day average gain/loss; every
subsequent value uses Wilder smoothing avg = (avg*(period-1)+new)/period).

Base rule: entry when close[i] > SMA(200)[i] AND RSI(2)[i] < 10 -> buy at the
NEXT day's open (day i+1). Exit when close[j] > SMA(5)[j] (while long) -> sell
at the NEXT day's open (day j+1). Long only, flat otherwise (cash earns 0).
Only one transition evaluated per day (if flat, only the entry condition is
checked; if long, only the exit condition is checked), so entry and exit
cannot both fire the same day. Cost = 0.10% per side, charged on the day of
the executing trade (entry day and exit day each pay it once; a full round
trip costs 0.20% total).

Execution mechanics (uses REAL open prices, unlike the close-to-close
approximation in indicators_price.py's Test 2 engine): on the transition-in
day i, the day's return is C[i]/O[i]-1 (bought at today's open, held to
today's close) minus the entry cost. On every day the position is already
long and not transitioning, the return is C[i]/C[i-1]-1 (ordinary
close-to-close). On the transition-out day j, the return is O[j]/C[j-1]-1
(held from yesterday's close to this morning's open, then sold) minus the
exit cost. On flat days the return is 0 (cash earns 0). These telescope
exactly to a completed trade's gross return = O[exit]/O[entry]-1, cost
included at each end -- so the daily return series used for CAGR/vol/Sharpe/
drawdown is fully consistent with the per-trade return used for win rate /
average trade / per-trade t-stat.

Warmup: 200 bars (needed for SMA200; also covers SMA5/SMA10 and RSI(2)).
Buy-and-hold is computed over the identical post-warmup window for a fair
comparison.

Metrics per symbol, full sample and both halves (2006-01 to 2015-12-31,
2016-01-01 to 2026-09-23; each half's CAGR/vol/Sharpe/maxDD computed on that
half's own return slice, capital restarting at 1.0 -- same convention as
indicators_price.py's period_stats): number of (completed) trades, win rate,
average trade % (compounded, cost-inclusive), average holding days (trading
days actually held long), % of days invested, CAGR, annualized vol, Sharpe
(rf=0), max drawdown; the same set (minus trade-level fields, which do not
apply) for buy-and-hold. A trade still open at the end of the sample is
excluded from trade-level stats (win rate / avg trade / holding days / t-
stat) but IS included in the daily return series (mark-to-market), so system
CAGR/Sharpe/etc. reflect it.

Per-trade t-stat: one-sample t-test of the trade-return sample against 0
(mean / (stdev/sqrt(n)), df=n-1), computed per symbol and pooled across all
14 stocks (concatenating every stock's trades into one sample -- more power
than any single stock, reported as the headline pooled figure) and for SPY
alone.

Sensitivity variants (extra tests, reported compactly -- full sample only,
SPY + 14-stock equal-weight average, not the full per-symbol/per-half
breakdown): (a) RSI(2) < 5 instead of < 10, (b) RSI(2) < 15 instead of < 10,
(c) exit on close > SMA(10) instead of SMA(5) (entry unchanged, RSI(2)<10).

-----------------------------------------------------------------------------
PART B -- POOLED PANIC DIPS
-----------------------------------------------------------------------------
Universe: ALL 15 symbols (14 large caps + SPY) pooled together -- unlike Part
A and unlike the other indicator scripts in this repo, SPY is NOT reported
separately here, because the point of this test is a market-wide/cross-
sectional "panic day" pattern, and excluding the index from the pool would
throw away exactly the kind of broad-based selloff day the test is looking
for.

Four oversold signals (mechanical, written before looking at any results):
  1. rsi14_cross_below_30:   RSI(14) Wilder crosses below 30
                              (rsi[i-1]>=30 and rsi[i]<30)
  2. bb_below_lower:         close[i] < lower Bollinger(20,2) band[i]
  3. new_60d_low:            close[i] < min(close[i-60:i])  (prior 60 trading
                              days, excluding today; requires i>=60)
  4. down2pct_heavyvol:      (close[i]/close[i-1]-1) <= -0.02 AND
                              volume[i] >= 2 * mean(volume[i-20:i])  (prior 20
                              days, excluding today; requires i>=20)

Union: for each symbol, a day counts as a signal day if ANY of the four fire
(a symbol-day counts once no matter how many of the four fire on it). Dedup:
5-trading-day window applied to this UNION list per symbol (once a
symbol-day qualifies, the next 4 trading days for that symbol are skipped
even if another of the four conditions fires), matching the dedup convention
used elsewhere in this repo.

Baseline (unconditional): mean forward return over ALL symbol-days (all 15
symbols) with a computable forward return at that horizon, matching the
convention in candlesticks.py / indicators_price.py / indicators_volume_vwap.py.

Forward returns measured at 5, 10, 21 trading days from the signal day's
close.

VIX regime: most recent WEEKLY VIX close on/before the signal day; <20,
20-25, >=25 (same buckets as the other indicator scripts).

TWO t-stats are reported, per the note's design (signals cluster on the same
calendar dates -- a market panic day fires the signal in many symbols at
once, so naive per-signal-day observations are not independent draws):
  (1) NAIVE t: Welch's two-sample t-test, treating every qualifying
      (symbol, day) instance as one independent observation, sample vs the
      unconditional baseline. This is the number that looks most impressive
      and is explicitly flagged as NOT the headline.
  (2) DATE-CLUSTERED t: for each calendar date on which at least one
      qualifying instance fired (pooling across all symbols that fired that
      date), compute the mean excess return (instance forward return minus
      the unconditional baseline MEAN for that horizon) across all instances
      sharing that date. This gives exactly one number per distinct date.
      The t-stat is then a one-sample t-test of that per-date series against
      0 (mean / (stdev/sqrt(n_dates)), df=n_dates-1). This is the headline.

Episodes: distinct signal dates are further collapsed into "episodes" -- a
run of dates where consecutive distinct dates are separated by fewer than 10
trading days (using SPY's date list, which is identical to every other
symbol's, as the master trading calendar to measure the gap). A gap of 10+
trading days starts a new episode.

Robustness cut: the entire analysis (naive t, clustered t, distinct dates,
episodes, VIX-regime split) is repeated with the 2008-09-01..2009-03-31 and
2020-02-01..2020-04-30 calendar windows removed from BOTH the signal
instances and the baseline pool, to check whether the two big historical
crashes are doing all the work.
"""

import json
import math
from pathlib import Path
from statistics import mean, stdev

REPO = Path(__file__).resolve().parents[2]
DAILY_PATH = REPO / "paper" / "history" / "daily_ohlcv.json"
VIX_PATH = REPO / "paper" / "history" / "vix_weekly.json"

TRADING_DAYS_YEAR = 252
COST_PER_SIDE = 0.001
DEDUP_WINDOW = 5

ALL_STOCKS_14 = ["AAPL", "AMZN", "BAC", "C", "CSCO", "F", "GE", "GOOGL", "IBM", "MSFT", "NVDA", "PFE", "T", "XOM"]
SPY = "SPY"
ALL_15 = ALL_STOCKS_14 + [SPY]

# Part A split (as specified in the task / research note)
SPLIT_DATE_A = "2016-01-01"

# Part B
HORIZONS_B = [5, 10, 21]
EXCLUDED_WINDOWS = [("2008-09-01", "2009-03-31"), ("2020-02-01", "2020-04-30")]


# -----------------------------------------------------------------------
# data loading (shared)
# -----------------------------------------------------------------------

def load_data():
    raw = json.loads(DAILY_PATH.read_text())
    vix_raw = json.loads(VIX_PATH.read_text())
    series = {}
    for sym, bars in raw.items():
        dates = sorted(bars.keys())
        O = [bars[d][0] for d in dates]
        H = [bars[d][1] for d in dates]
        L = [bars[d][2] for d in dates]
        C = [bars[d][3] for d in dates]
        V = [bars[d][4] for d in dates]
        series[sym] = {"dates": dates, "O": O, "H": H, "L": L, "C": C, "V": V}
    vix_dates = sorted(vix_raw.keys())
    vix_vals = [vix_raw[d] for d in vix_dates]
    return series, (vix_dates, vix_vals)


def vix_asof(vix_dates, vix_vals, date_str):
    lo, hi = 0, len(vix_dates)
    while lo < hi:
        mid = (lo + hi) // 2
        if vix_dates[mid] <= date_str:
            lo = mid + 1
        else:
            hi = mid
    if lo == 0:
        return None
    return vix_vals[lo - 1]


def in_excluded(date_str, windows):
    return any(lo <= date_str <= hi for lo, hi in windows)


# -----------------------------------------------------------------------
# indicators (shared)
# -----------------------------------------------------------------------

def rsi_wilder(C, period):
    n = len(C)
    rsi = [None] * n
    if n <= period:
        return rsi
    gains = [0.0] * n
    losses = [0.0] * n
    for i in range(1, n):
        chg = C[i] - C[i - 1]
        gains[i] = chg if chg > 0 else 0.0
        losses[i] = -chg if chg < 0 else 0.0

    def rsi_from(ag, al):
        if al == 0:
            return 100.0
        rs = ag / al
        return 100.0 - 100.0 / (1.0 + rs)

    avg_gain = sum(gains[1:period + 1]) / period
    avg_loss = sum(losses[1:period + 1]) / period
    rsi[period] = rsi_from(avg_gain, avg_loss)
    for i in range(period + 1, n):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        rsi[i] = rsi_from(avg_gain, avg_loss)
    return rsi


def sma(C, period):
    n = len(C)
    out = [None] * n
    s = 0.0
    for i in range(n):
        s += C[i]
        if i >= period:
            s -= C[i - period]
        if i >= period - 1:
            out[i] = s / period
    return out


def bollinger(C, period=20, k=2.0):
    n = len(C)
    mid = [None] * n
    upper = [None] * n
    lower = [None] * n
    for i in range(period - 1, n):
        window = C[i - period + 1:i + 1]
        m = sum(window) / period
        var = sum((x - m) ** 2 for x in window) / period
        sd = math.sqrt(var)
        mid[i] = m
        upper[i] = m + k * sd
        lower[i] = m - k * sd
    return upper, mid, lower


def dedup(days, window=DEDUP_WINDOW):
    kept = []
    last = -10 ** 9
    for d in days:
        if d - last >= window:
            kept.append(d)
        last = d
    return kept


# -----------------------------------------------------------------------
# stats helpers (shared)
# -----------------------------------------------------------------------

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


def one_sample_t(sample):
    n = len(sample)
    if n < 2:
        return float("nan")
    m = mean(sample)
    sd = stdev(sample)
    if sd == 0:
        return float("nan")
    return m / (sd / math.sqrt(n))


def fmt(x, nd=3):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "NA"
    return f"{x:.{nd}f}"


def bonferroni_t(n_tests, alpha=0.05):
    try:
        from scipy.stats import norm
        return norm.ppf(1 - (alpha / n_tests) / 2)
    except ImportError:
        adj_alpha = alpha / n_tests
        p = 1 - adj_alpha / 2
        lo, hi = -10.0, 10.0
        for _ in range(200):
            mid = (lo + hi) / 2
            cdf = 0.5 * (1 + math.erf(mid / math.sqrt(2)))
            if cdf < p:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2


def perf_metrics(rets):
    n = len(rets)
    if n < 2:
        return {"cagr": float("nan"), "vol": float("nan"), "sharpe": float("nan"), "maxdd": float("nan")}
    equity = [1.0]
    for r in rets:
        equity.append(equity[-1] * (1 + r))
    total_ret = equity[-1] / equity[0]
    years = n / TRADING_DAYS_YEAR
    cagr = total_ret ** (1 / years) - 1 if years > 0 and total_ret > 0 else float("nan")
    sd = stdev(rets)
    vol = sd * math.sqrt(TRADING_DAYS_YEAR)
    sharpe = (mean(rets) / sd) * math.sqrt(TRADING_DAYS_YEAR) if sd > 0 else float("nan")
    peak = equity[0]
    maxdd = 0.0
    for e in equity:
        if e > peak:
            peak = e
        dd = e / peak - 1
        if dd < maxdd:
            maxdd = dd
    return {"cagr": cagr, "vol": vol, "sharpe": sharpe, "maxdd": maxdd}


def period_stats(dates, rets, poss, date_lo=None, date_hi=None):
    idx = [k for k, d in enumerate(dates) if (date_lo is None or d >= date_lo) and (date_hi is None or d < date_hi)]
    if not idx:
        return None
    sub_rets = [rets[k] for k in idx]
    sub_poss = [poss[k] for k in idx]
    m = perf_metrics(sub_rets)
    m["pct_invested"] = mean(sub_poss) * 100
    m["n_days"] = len(idx)
    return m


def trade_stats(trades, date_lo=None, date_hi=None):
    filt = [t for t in trades
            if (date_lo is None or t["entry_date"] >= date_lo) and (date_hi is None or t["entry_date"] < date_hi)]
    n = len(filt)
    if n == 0:
        return {"n": 0, "win_rate": float("nan"), "avg_trade_pct": float("nan"),
                "avg_hold_days": float("nan"), "t_stat": float("nan"), "rets": []}
    rets = [t["ret"] for t in filt]
    wins = sum(1 for r in rets if r > 0)
    return {
        "n": n,
        "win_rate": wins / n * 100.0,
        "avg_trade_pct": mean(rets) * 100.0,
        "avg_hold_days": mean(t["holding_days"] for t in filt),
        "t_stat": one_sample_t(rets),
        "rets": rets,
    }


# =========================================================================
# PART A -- RSI(2) SYSTEM
# =========================================================================

WARMUP_A = 200


def run_rsi2_system(bars, entry_rsi_period=2, entry_thresh=10.0, exit_sma_period=5, entry_sma_period=200):
    """Long/flat RSI(2) system with real next-open execution. Returns None if
    insufficient history."""
    C, O, dates = bars["C"], bars["O"], bars["dates"]
    n = len(C)
    if n <= max(entry_sma_period, WARMUP_A) + 2:
        return None

    rsi = rsi_wilder(C, entry_rsi_period)
    sma_entry = sma(C, entry_sma_period)
    sma_exit = sma(C, exit_sma_period)
    warmup = max(entry_sma_period, WARMUP_A)

    # state machine: target_pos[i] = position to HOLD during day i, decided
    # using data available at close of day i-1.
    target_pos = [0] * n
    state = 0
    for i in range(warmup, n - 1):
        if state == 0:
            if (sma_entry[i] is not None and rsi[i] is not None
                    and C[i] > sma_entry[i] and rsi[i] < entry_thresh):
                state = 1
        else:
            if sma_exit[i] is not None and C[i] > sma_exit[i]:
                state = 0
        target_pos[i + 1] = state

    out_dates, rets, poss = [], [], []
    trades = []
    prev_pos = 0
    entry_idx = None
    trade_mult = None
    for i in range(warmup + 1, n):
        target = target_pos[i]
        if target != prev_pos:
            if target == 1:  # transition in: buy at today's open
                day_ret = C[i] / O[i] - 1.0 - COST_PER_SIDE
                entry_idx = i
                trade_mult = 1.0 + day_ret
            else:  # transition out: sell at today's open
                day_ret = O[i] / C[i - 1] - 1.0 - COST_PER_SIDE
                trade_mult *= (1.0 + day_ret)
                if entry_idx is not None:
                    trades.append({
                        "entry_idx": entry_idx, "exit_idx": i,
                        "entry_date": dates[entry_idx], "exit_date": dates[i],
                        "holding_days": i - entry_idx,
                        "ret": trade_mult - 1.0,
                    })
                entry_idx = None
                trade_mult = None
        else:
            if target == 1:
                day_ret = C[i] / C[i - 1] - 1.0
                trade_mult *= (1.0 + day_ret)
            else:
                day_ret = 0.0
        rets.append(day_ret)
        poss.append(target)
        out_dates.append(dates[i])
        prev_pos = target

    still_open = prev_pos == 1
    return {"dates": out_dates, "rets": rets, "poss": poss, "trades": trades, "still_open": still_open}


def run_buy_and_hold(bars, warmup):
    C, dates = bars["C"], bars["dates"]
    n = len(C)
    if n <= warmup + 2:
        return None
    out_dates = dates[warmup + 1:]
    rets = [C[i] / C[i - 1] - 1.0 for i in range(warmup + 1, n)]
    poss = [1] * len(rets)
    return {"dates": out_dates, "rets": rets, "poss": poss}


def fmt_perf_row(m):
    if m is None:
        return "NA".rjust(8) * 5
    return (f"{fmt(m['cagr']*100,2):>8s}{fmt(m['vol']*100,2):>8s}{fmt(m['sharpe'],2):>8s}"
            f"{fmt(m['maxdd']*100,2):>8s}{fmt(m['pct_invested'],1):>8s}")


def fmt_trade_row(t):
    return (f"{t['n']:>6d}{fmt(t['win_rate'],1):>8s}{fmt(t['avg_trade_pct'],3):>9s}"
            f"{fmt(t['avg_hold_days'],1):>8s}{fmt(t['t_stat'],2):>7s}")


def part_a_variant(series, entry_thresh, exit_sma_period, label, full_report=True):
    print("-" * 118)
    print(f"VARIANT: {label}  (RSI(2) < {entry_thresh}, exit close > SMA({exit_sma_period}))")
    print("-" * 118)

    per_symbol_sys = {}
    per_symbol_bh = {}
    for sym in ALL_15:
        sysrun = run_rsi2_system(series[sym], entry_thresh=entry_thresh, exit_sma_period=exit_sma_period)
        per_symbol_sys[sym] = sysrun
        per_symbol_bh[sym] = run_buy_and_hold(series[sym], WARMUP_A) if sysrun is not None else None

    periods = [("full", None, None), ("2006-2015", None, SPLIT_DATE_A), ("2016-2026", SPLIT_DATE_A, None)]
    if not full_report:
        periods = [("full", None, None)]

    hdr = (f"{'sym':6s}{'period':10s}| {'trades':>6s}{'win%':>8s}{'avgtrd%':>9s}{'holdd':>8s}{'t':>7s}"
           f" | {'cagr%':>8s}{'vol%':>8s}{'shrp':>8s}{'mdd%':>8s}{'pin%':>8s}"
           f" | {'bh_cagr%':>8s}{'bh_vol%':>8s}{'bh_shrp':>8s}{'bh_mdd%':>8s}{'bh_pin%':>8s}")
    print(hdr)
    print("-" * len(hdr))

    pooled_trade_rets = {p[0]: [] for p in periods}
    avg_rows = {p[0]: {"sys": {}, "bh": {}, "trade": {}} for p in periods}
    for p_label, lo, hi in periods:
        for key in ["cagr", "vol", "sharpe", "maxdd", "pct_invested"]:
            avg_rows[p_label]["sys"][key] = []
            avg_rows[p_label]["bh"][key] = []
        for key in ["n", "win_rate", "avg_trade_pct", "avg_hold_days"]:
            avg_rows[p_label]["trade"][key] = []

    still_open_syms = []
    for sym in ALL_15:
        sysrun = per_symbol_sys[sym]
        bhrun = per_symbol_bh[sym]
        if sysrun is None:
            if full_report:
                print(f"{sym:6s}{'--':10s}| insufficient history")
            continue
        if sysrun["still_open"]:
            still_open_syms.append(sym)
        for p_label, lo, hi in periods:
            sys_perf = period_stats(sysrun["dates"], sysrun["rets"], sysrun["poss"], lo, hi)
            bh_perf = period_stats(bhrun["dates"], bhrun["rets"], bhrun["poss"], lo, hi) if bhrun else None
            tstats = trade_stats(sysrun["trades"], lo, hi)
            if full_report:
                print(f"{sym:6s}{p_label:10s}| {fmt_trade_row(tstats)} | {fmt_perf_row(sys_perf)} | {fmt_perf_row(bh_perf)}")
            if sym in ALL_STOCKS_14:
                pooled_trade_rets[p_label].extend(tstats["rets"])
                if sys_perf is not None:
                    for key in ["cagr", "vol", "sharpe", "maxdd", "pct_invested"]:
                        v = sys_perf[key]
                        if not (isinstance(v, float) and math.isnan(v)):
                            avg_rows[p_label]["sys"][key].append(v)
                if bh_perf is not None:
                    for key in ["cagr", "vol", "sharpe", "maxdd", "pct_invested"]:
                        v = bh_perf[key]
                        if not (isinstance(v, float) and math.isnan(v)):
                            avg_rows[p_label]["bh"][key].append(v)
                for key in ["n", "win_rate", "avg_trade_pct", "avg_hold_days"]:
                    v = tstats[key]
                    if not (isinstance(v, float) and math.isnan(v)):
                        avg_rows[p_label]["trade"][key].append(v)

    if full_report:
        print("-" * len(hdr))
    # 14-stock equal-weight average + pooled trade t-stat
    for p_label, lo, hi in periods:
        def avgm(d):
            return {k: (mean(v) if v else float("nan")) for k, v in d.items()}
        sys_avg = avgm(avg_rows[p_label]["sys"])
        bh_avg = avgm(avg_rows[p_label]["bh"])
        trade_avg_n = sum(avg_rows[p_label]["trade"]["n"]) if avg_rows[p_label]["trade"]["n"] else 0
        trade_avg_win = mean(avg_rows[p_label]["trade"]["win_rate"]) if avg_rows[p_label]["trade"]["win_rate"] else float("nan")
        trade_avg_ret = mean(avg_rows[p_label]["trade"]["avg_trade_pct"]) if avg_rows[p_label]["trade"]["avg_trade_pct"] else float("nan")
        trade_avg_hold = mean(avg_rows[p_label]["trade"]["avg_hold_days"]) if avg_rows[p_label]["trade"]["avg_hold_days"] else float("nan")
        pooled_t = one_sample_t(pooled_trade_rets[p_label])
        fake_trade = {"n": trade_avg_n, "win_rate": trade_avg_win, "avg_trade_pct": trade_avg_ret,
                      "avg_hold_days": trade_avg_hold, "t_stat": pooled_t}
        print(f"{'AVG14':6s}{p_label:10s}| {fmt_trade_row(fake_trade)} | {fmt_perf_row(sys_avg)} | {fmt_perf_row(bh_avg)}"
              f"   (n=total trades across 14, t-stat=POOLED across all 14 stocks' trades)")

    print()
    print("SPY (separate):")
    for p_label, lo, hi in periods:
        sysrun = per_symbol_sys[SPY]
        bhrun = per_symbol_bh[SPY]
        sys_perf = period_stats(sysrun["dates"], sysrun["rets"], sysrun["poss"], lo, hi)
        bh_perf = period_stats(bhrun["dates"], bhrun["rets"], bhrun["poss"], lo, hi)
        tstats = trade_stats(sysrun["trades"], lo, hi)
        print(f"{'SPY':6s}{p_label:10s}| {fmt_trade_row(tstats)} | {fmt_perf_row(sys_perf)} | {fmt_perf_row(bh_perf)}")
    if still_open_syms:
        print(f"(still holding an open position at end of sample, excluded from trade-level stats: {still_open_syms})")
    print()


# =========================================================================
# PART B -- POOLED PANIC DIPS
# =========================================================================

def detect_panic_raw(bars):
    C, V = bars["C"], bars["V"]
    n = len(C)
    rsi14 = rsi_wilder(C, 14)
    bb_up, bb_mid, bb_lo = bollinger(C, 20, 2.0)
    raw_counts = {"rsi14_cross_below_30": 0, "bb_below_lower": 0, "new_60d_low": 0, "down2pct_heavyvol": 0}
    union_days = set()
    for i in range(n):
        fired = False
        if i >= 1 and rsi14[i - 1] is not None and rsi14[i] is not None and rsi14[i - 1] >= 30 and rsi14[i] < 30:
            raw_counts["rsi14_cross_below_30"] += 1
            fired = True
        if bb_lo[i] is not None and C[i] < bb_lo[i]:
            raw_counts["bb_below_lower"] += 1
            fired = True
        if i >= 60:
            prior_low60 = min(C[i - 60:i])
            if C[i] < prior_low60:
                raw_counts["new_60d_low"] += 1
                fired = True
        if i >= 20 and i >= 1:
            avgvol20 = mean(V[i - 20:i])
            if avgvol20 > 0:
                day_ret = C[i] / C[i - 1] - 1.0
                if day_ret <= -0.02 and V[i] >= 2 * avgvol20:
                    raw_counts["down2pct_heavyvol"] += 1
                    fired = True
        if fired:
            union_days.add(i)
    deduped = dedup(sorted(union_days))
    return deduped, raw_counts


def build_baseline_b(series, symbols, exclude_windows=None):
    baseline = {h: [] for h in HORIZONS_B}
    for sym in symbols:
        bars = series[sym]
        C, dates = bars["C"], bars["dates"]
        n = len(C)
        for h in HORIZONS_B:
            for i in range(n - h):
                if exclude_windows and in_excluded(dates[i], exclude_windows):
                    continue
                baseline[h].append(C[i + h] / C[i] - 1.0)
    return baseline


def count_episodes(distinct_dates, master_dates, gap_trading_days=10):
    idx_map = {d: i for i, d in enumerate(master_dates)}
    idxs = sorted(idx_map[d] for d in distinct_dates if d in idx_map)
    if not idxs:
        return 0
    episodes = 1
    for a, b in zip(idxs, idxs[1:]):
        if b - a >= gap_trading_days:
            episodes += 1
    return episodes


def analyze_instances(series, instances, baseline, label_prefix=""):
    """instances: list of (sym, day_idx, date_str). Returns per-horizon stats
    plus distinct-date / episode counts (horizon-independent, from the full
    instance list)."""
    distinct_dates = sorted({d for _, _, d in instances})
    master_dates = series[SPY]["dates"]
    n_episodes = count_episodes(distinct_dates, master_dates)

    per_h = {}
    for h in HORIZONS_B:
        base_mean = mean(baseline[h]) if baseline[h] else float("nan")
        sample = []
        excess_by_date = {}
        for sym, d, date_str in instances:
            C = series[sym]["C"]
            n = len(C)
            if d + h < n:
                fr = C[d + h] / C[d] - 1.0
                sample.append(fr)
                excess_by_date.setdefault(date_str, []).append(fr - base_mean)
        t_naive, diff = welch_t(sample, baseline[h]) if len(sample) >= 2 and baseline[h] else (float("nan"), float("nan"))
        diff_pp = diff * 100 if not (isinstance(diff, float) and math.isnan(diff)) else float("nan")
        per_date_avg = [mean(v) for v in excess_by_date.values()]
        t_clustered = one_sample_t(per_date_avg)
        mean_excess_pp = mean(per_date_avg) * 100 if per_date_avg else float("nan")
        per_h[h] = {
            "n_instances": len(sample), "n_dates_h": len(excess_by_date),
            "diff_pp": diff_pp, "t_naive": t_naive,
            "mean_excess_clustered_pp": mean_excess_pp, "t_clustered": t_clustered,
        }
    return {
        "n_instances_total": len(instances), "n_distinct_dates": len(distinct_dates),
        "n_episodes": n_episodes, "per_h": per_h,
    }


def print_pooled_block(result, title):
    print(title)
    print(f"  distinct signal instances (symbol-days, after per-symbol 5-day dedup): {result['n_instances_total']}")
    print(f"  distinct calendar dates: {result['n_distinct_dates']}   "
          f"episodes (gap >= 10 trading days starts a new one): {result['n_episodes']}")
    hdr = f"  {'h':>3s} {'n_inst':>7s} {'n_dates':>7s} {'diff_pp':>9s} {'t_naive':>8s} {'clustexc_pp':>11s} {'t_clustered':>11s}"
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    for h in HORIZONS_B:
        r = result["per_h"][h]
        print(f"  {h:>3d} {r['n_instances']:>7d} {r['n_dates_h']:>7d} {fmt(r['diff_pp']):>9s} "
              f"{fmt(r['t_naive'],2):>8s} {fmt(r['mean_excess_clustered_pp']):>11s} {fmt(r['t_clustered'],2):>11s}")
    print()


def part_b():
    series, (vix_dates, vix_vals) = load_data()

    print("#" * 118)
    print("PART B: POOLED PANIC DIPS")
    print("#" * 118)
    print(f"Universe: all 15 symbols pooled = {ALL_15}")
    print(f"Date range: {series['SPY']['dates'][0]} to {series['SPY']['dates'][-1]}")
    print(f"Forward-return horizons (trading days): {HORIZONS_B}")
    print(f"Dedup: 5-trading-day window on the per-symbol UNION of the four signals")
    print()

    per_symbol_instances = {}
    per_symbol_raw_counts = {}
    for sym in ALL_15:
        deduped, counts = detect_panic_raw(series[sym])
        per_symbol_instances[sym] = deduped
        per_symbol_raw_counts[sym] = counts

    all_instances = []
    for sym in ALL_15:
        dates = series[sym]["dates"]
        for d in per_symbol_instances[sym]:
            all_instances.append((sym, d, dates[d]))
    all_instances.sort(key=lambda x: x[2])

    print("-" * 118)
    print("RAW SIGNAL COUNTS (pre-union, pre-dedup, per symbol summed) -- informational only")
    print("-" * 118)
    totals = {"rsi14_cross_below_30": 0, "bb_below_lower": 0, "new_60d_low": 0, "down2pct_heavyvol": 0}
    for sym in ALL_15:
        for k in totals:
            totals[k] += per_symbol_raw_counts[sym][k]
    for k, v in totals.items():
        print(f"  {k:24s} n={v}")
    print(f"  UNION signal-day instances after per-symbol 5-day dedup (all 15 symbols): {len(all_instances)}")
    print()

    baseline_full = build_baseline_b(series, ALL_15)

    print("=" * 118)
    print("MAIN RESULT -- ALL SIGNAL INSTANCES POOLED, FULL SAMPLE")
    print("=" * 118)
    result_all = analyze_instances(series, all_instances, baseline_full)
    print_pooled_block(result_all, "ALL INSTANCES (unconditional baseline):")

    print("-" * 118)
    print("VIX-REGIME SPLIT (regime = most recent WEEKLY VIX close on/before the signal day; baseline stays")
    print("the UNCONDITIONAL baseline computed above -- not a regime-specific baseline)")
    print("-" * 118)
    regime_instances = {"lt20": [], "20to25": [], "gte25": [], "novix": []}
    for sym, d, date_str in all_instances:
        v = vix_asof(vix_dates, vix_vals, date_str)
        if v is None:
            regime_instances["novix"].append((sym, d, date_str))
        elif v < 20:
            regime_instances["lt20"].append((sym, d, date_str))
        elif v < 25:
            regime_instances["20to25"].append((sym, d, date_str))
        else:
            regime_instances["gte25"].append((sym, d, date_str))
    for regime in ["lt20", "20to25", "gte25"]:
        result_r = analyze_instances(series, regime_instances[regime], baseline_full)
        print_pooled_block(result_r, f"VIX regime {regime}:")
    if regime_instances["novix"]:
        print(f"  ({len(regime_instances['novix'])} instances had no VIX data on/before their date and are excluded "
              f"from the regime split)")
    print()

    print("=" * 118)
    print("ROBUSTNESS CUT -- 2008-09-01..2009-03-31 and 2020-02-01..2020-04-30 REMOVED")
    print("(removed from BOTH the signal instances AND the baseline pool)")
    print("=" * 118)
    filtered_instances = [(s, d, dt) for s, d, dt in all_instances if not in_excluded(dt, EXCLUDED_WINDOWS)]
    baseline_filtered = build_baseline_b(series, ALL_15, exclude_windows=EXCLUDED_WINDOWS)
    n_removed = len(all_instances) - len(filtered_instances)
    print(f"Instances removed by the exclusion windows: {n_removed} (of {len(all_instances)})")
    result_filt = analyze_instances(series, filtered_instances, baseline_filtered)
    print_pooled_block(result_filt, "ALL INSTANCES, crisis windows excluded (unconditional baseline, also crisis-excluded):")

    print("-" * 118)
    print("VIX-REGIME SPLIT, crisis windows excluded")
    print("-" * 118)
    regime_instances_filt = {"lt20": [], "20to25": [], "gte25": [], "novix": []}
    for sym, d, date_str in filtered_instances:
        v = vix_asof(vix_dates, vix_vals, date_str)
        if v is None:
            regime_instances_filt["novix"].append((sym, d, date_str))
        elif v < 20:
            regime_instances_filt["lt20"].append((sym, d, date_str))
        elif v < 25:
            regime_instances_filt["20to25"].append((sym, d, date_str))
        else:
            regime_instances_filt["gte25"].append((sym, d, date_str))
    for regime in ["lt20", "20to25", "gte25"]:
        result_r = analyze_instances(series, regime_instances_filt[regime], baseline_filtered)
        print_pooled_block(result_r, f"VIX regime {regime} (crisis-excluded):")
    print()

    print("-" * 118)
    print("MULTIPLE TESTING (Part B)")
    print("-" * 118)
    n_tests_b = len(HORIZONS_B) * 2  # naive + clustered, per horizon, main result
    n_tests_b_regime = len(HORIZONS_B) * 2 * 3  # 3 regimes
    n_tests_b_robust = len(HORIZONS_B) * 2 * (1 + 3)  # robustness overall + 3 regimes
    total_b = n_tests_b + n_tests_b_regime + n_tests_b_robust
    print(f"Main pooled result: {n_tests_b} tests (3 horizons x {{naive, clustered}})")
    print(f"VIX-regime split: {n_tests_b_regime} more tests (3 horizons x {{naive, clustered}} x 3 regimes)")
    print(f"Robustness cut (crisis windows removed, overall + regime split): {n_tests_b_robust} more tests")
    print(f"Total Part B tests: {total_b}")
    crit = bonferroni_t(total_b)
    print(f"  Bonferroni alpha=0.05/{total_b} -> two-tailed critical |t| ~= {crit:.3f}")
    print("  (This threshold applies to the CLUSTERED t, which is the number that should be judged against it --")
    print("   see docstring for why the naive t is not the headline.)")
    print()


# =========================================================================
# main
# =========================================================================

def main():
    series, (vix_dates, vix_vals) = load_data()

    print("=" * 118)
    print("RSI(2) AND POOLED PANIC DIPS -- RAW TEST OUTPUT")
    print("=" * 118)
    print(f"Universe: {len(ALL_STOCKS_14)} large caps + SPY = {ALL_15}")
    print(f"Date range: {series['SPY']['dates'][0]} to {series['SPY']['dates'][-1]}")
    print(f"Cost: {COST_PER_SIDE*100:.2f}% per side (0.20% round trip). Cash earns 0.")
    print(f"Part A split: 2006-01-01..2015-12-31 vs {SPLIT_DATE_A}..2026-09-23")
    print()

    print("#" * 118)
    print("PART A: RSI(2) SYSTEM")
    print("#" * 118)
    print()
    part_a_variant(series, entry_thresh=10.0, exit_sma_period=5, label="BASE RULE (RSI(2)<10, exit SMA5)", full_report=True)

    print("-" * 118)
    print("SENSITIVITY VARIANTS (extra tests, compact report: full sample only, SPY + 14-stock avg + pooled trade t)")
    print("-" * 118)
    part_a_variant(series, entry_thresh=5.0, exit_sma_period=5, label="SENSITIVITY: RSI(2)<5, exit SMA5", full_report=False)
    part_a_variant(series, entry_thresh=15.0, exit_sma_period=5, label="SENSITIVITY: RSI(2)<15, exit SMA5", full_report=False)
    part_a_variant(series, entry_thresh=10.0, exit_sma_period=10, label="SENSITIVITY: RSI(2)<10, exit SMA10", full_report=False)

    print("-" * 118)
    print("MULTIPLE TESTING (Part A)")
    print("-" * 118)
    n_base = 15 * 3  # 15 symbols x 3 periods (full/pre/post), each with a system-vs-BH Sharpe comparison
    n_variants = 3 * 15  # 3 sensitivity variants x 15 symbols, full sample only
    total_a = n_base + n_variants
    print(f"Base rule: {n_base} symbol-period system runs (15 symbols x 3 periods)")
    print(f"Sensitivity variants: {n_variants} additional symbol runs (3 variants x 15 symbols, full sample)")
    print(f"Total Part A runs: {total_a}")
    print()

    part_b()

    print("Done.")


if __name__ == "__main__":
    main()
