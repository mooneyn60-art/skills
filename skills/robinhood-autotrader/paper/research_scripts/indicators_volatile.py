"""
Chart indicators on volatile growth stocks -- mechanical, pre-registered
signal + system test, same method as indicators_price.py applied to a
higher-volatility universe.

RESEARCH_AGENDA item ("Nolan trades SOFI-type names -- do the indicators
behave the same way on volatile growth stocks as on blue chips?").
Predictions were written and committed BEFORE this script was run
(research/2026-09-24_INDICATORS_VOLATILE_NAMES.md, commit 52bed82). This
script implements the test described there. It prints raw numbers only --
no conclusions are hardcoded here; the verdict is written into the note by
hand after reading this output.

Universe (volatile growth names, pulled fresh via Robinhood
get_equity_historicals, daily bars, split-adjusted, regular hours,
interpolated=true bars dropped): SOFI PLTR HOOD COIN RIVN AFRM UPST SNAP
ROKU SHOP TSLA AMD NVDA MU ENPH NFLX UBER DKNG CRWD NET MARA RIOT.
Data file: paper/history/daily_ohlcv_volatile.json, schema
{SYMBOL: {"YYYY-MM-DD": [open, high, low, close, volume]}}.
Comparison universe (large caps, for the volatility check only):
paper/history/daily_stocks.json, the same 14 symbols used in
indicators_price.py (AAPL AMZN BAC C CSCO F GE GOOGL IBM MSFT NVDA PFE T
XOM), plus SPY.

Indicator definitions, event-signal definitions, system definitions,
dedup rule, cost model, and Bonferroni method are IDENTICAL to
paper/research_scripts/indicators_price.py -- see that file's docstring
for the exact formulas. The two differences, both required by the short
and uneven histories of this universe (spelled out in the note before any
test ran):

1. TEST 2 (trading systems) splits each name's own history at ITS OWN
   midpoint date (dates[len(dates)//2]) rather than a universe-wide date,
   since these names IPO'd at very different times and a single fixed
   split date would leave some names with almost no "first half".
2. TEST 1 (event study) pools across all 22 names and splits both halves
   at a single fixed calendar date, 2021-01-01 (matching indicators_price.py's
   use of one split date for the pooled event study), since most of these
   names' full histories only start after 2019-2021 anyway.

No VIX-regime cut is run here (indicators_price.py's secondary VIX-regime
family). It was not requested for this universe and the short per-name
histories would make most regime buckets too thin to read.
"""

import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev, median

REPO = Path(__file__).resolve().parents[2]
VOLATILE_PATH = REPO / "paper" / "history" / "daily_ohlcv_volatile.json"
LARGECAP_PATH = REPO / "paper" / "history" / "daily_stocks.json"

EVENT_SPLIT_DATE = "2021-01-01"
HORIZONS = [5, 10, 21]
DEDUP_WINDOW = 5
COST_PER_SIDE = 0.001
TRADING_DAYS_YEAR = 252
MIN_BARS = 750  # ~3 years; names below this are excluded (none were, see report)

VOLATILE_SYMS = ["SOFI", "PLTR", "HOOD", "COIN", "RIVN", "AFRM", "UPST", "SNAP",
                  "ROKU", "SHOP", "TSLA", "AMD", "NVDA", "MU", "ENPH", "NFLX",
                  "UBER", "DKNG", "CRWD", "NET", "MARA", "RIOT"]
LARGECAP_SYMS = ["AAPL", "AMZN", "BAC", "C", "CSCO", "F", "GE", "GOOGL", "IBM",
                  "MSFT", "NVDA", "PFE", "T", "XOM"]
SPY = "SPY"

SIGNAL_ORDER = [
    "macd_bull_cross", "macd_bear_cross", "macd_cross_above_zero", "macd_cross_below_zero",
    "rsi_cross_below_30", "rsi_cross_above_70", "rsi_cross_back_above_30", "rsi_cross_above_50",
    "bb_close_below_lower", "bb_close_above_upper", "bb_squeeze_break_up", "bb_squeeze_break_down",
    "sma50_cross_above", "sma50_cross_below", "golden_cross", "death_cross",
    "ema9_cross_above", "ema9_cross_below",
]
DIRECTION = {
    "macd_bull_cross": "BULL", "macd_bear_cross": "BEAR",
    "macd_cross_above_zero": "BULL", "macd_cross_below_zero": "BEAR",
    "rsi_cross_below_30": "BULL", "rsi_cross_above_70": "BEAR",
    "rsi_cross_back_above_30": "BULL", "rsi_cross_above_50": "BULL",
    "bb_close_below_lower": "BULL", "bb_close_above_upper": "BEAR",
    "bb_squeeze_break_up": "BULL", "bb_squeeze_break_down": "BEAR",
    "sma50_cross_above": "BULL", "sma50_cross_below": "BEAR",
    "golden_cross": "BULL", "death_cross": "BEAR",
    "ema9_cross_above": "BULL", "ema9_cross_below": "BEAR",
}


# -----------------------------------------------------------------------
# data loading
# -----------------------------------------------------------------------

def load_volatile():
    raw = json.loads(VOLATILE_PATH.read_text())
    series = {}
    excluded = []
    for sym in VOLATILE_SYMS:
        bars = raw.get(sym, {})
        dates = sorted(bars.keys())
        if len(dates) < MIN_BARS:
            excluded.append((sym, len(dates)))
            continue
        O = [bars[d][0] for d in dates]
        H = [bars[d][1] for d in dates]
        L = [bars[d][2] for d in dates]
        C = [bars[d][3] for d in dates]
        V = [bars[d][4] for d in dates]
        series[sym] = {"dates": dates, "O": O, "H": H, "L": L, "C": C, "V": V}
    return series, excluded


def load_largecap():
    raw = json.loads(LARGECAP_PATH.read_text())
    series = {}
    for sym, bars in raw.items():
        dates = sorted(bars.keys())
        O = [bars[d][0] for d in dates]
        H = [bars[d][1] for d in dates]
        L = [bars[d][2] for d in dates]
        C = [bars[d][3] for d in dates]
        series[sym] = {"dates": dates, "O": O, "H": H, "L": L, "C": C}
    return series


# -----------------------------------------------------------------------
# indicators (identical formulas to indicators_price.py)
# -----------------------------------------------------------------------

def ema(values, span):
    a = 2.0 / (span + 1)
    out = [values[0]]
    for v in values[1:]:
        out.append(a * v + (1 - a) * out[-1])
    return out


def macd_calc(C):
    e12 = ema(C, 12)
    e26 = ema(C, 26)
    macd_line = [x - y for x, y in zip(e12, e26)]
    signal_line = ema(macd_line, 9)
    return macd_line, signal_line


def rsi_wilder(C, period=14):
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


def percentile(sorted_vals, pct):
    if not sorted_vals:
        return None
    k = (len(sorted_vals) - 1) * pct
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_vals[int(k)]
    return sorted_vals[f] * (c - k) + sorted_vals[c] * (k - f)


class Indicators:
    __slots__ = ("macd", "signal", "rsi", "sma50", "sma200", "ema9", "bb_up", "bb_mid", "bb_lo", "bandwidth")

    def __init__(self, bars):
        C = bars["C"]
        self.macd, self.signal = macd_calc(C)
        self.rsi = rsi_wilder(C, 14)
        self.sma50 = sma(C, 50)
        self.sma200 = sma(C, 200)
        self.ema9 = ema(C, 9)
        self.bb_up, self.bb_mid, self.bb_lo = bollinger(C, 20, 2.0)
        self.bandwidth = [
            (self.bb_up[i] - self.bb_lo[i]) / self.bb_mid[i] if self.bb_mid[i] not in (None, 0) else None
            for i in range(len(C))
        ]


# -----------------------------------------------------------------------
# dedup
# -----------------------------------------------------------------------

def dedup(days, window=DEDUP_WINDOW):
    kept = []
    last = -10 ** 9
    for d in days:
        if d - last >= window:
            kept.append(d)
        last = d
    return kept


# -----------------------------------------------------------------------
# signal detection (identical to indicators_price.py)
# -----------------------------------------------------------------------

def detect_signals(bars, ind):
    C = bars["C"]
    n = len(C)
    raw = {name: [] for name in SIGNAL_ORDER}

    for i in range(1, n):
        if ind.macd[i - 1] <= ind.signal[i - 1] and ind.macd[i] > ind.signal[i]:
            raw["macd_bull_cross"].append(i)
        if ind.macd[i - 1] >= ind.signal[i - 1] and ind.macd[i] < ind.signal[i]:
            raw["macd_bear_cross"].append(i)
        if ind.macd[i - 1] <= 0 and ind.macd[i] > 0:
            raw["macd_cross_above_zero"].append(i)
        if ind.macd[i - 1] >= 0 and ind.macd[i] < 0:
            raw["macd_cross_below_zero"].append(i)

        if ind.rsi[i - 1] is not None and ind.rsi[i] is not None:
            if ind.rsi[i - 1] >= 30 and ind.rsi[i] < 30:
                raw["rsi_cross_below_30"].append(i)
            if ind.rsi[i - 1] <= 70 and ind.rsi[i] > 70:
                raw["rsi_cross_above_70"].append(i)
            if ind.rsi[i - 1] < 30 and ind.rsi[i] >= 30:
                raw["rsi_cross_back_above_30"].append(i)
            if ind.rsi[i - 1] < 50 and ind.rsi[i] >= 50:
                raw["rsi_cross_above_50"].append(i)

        if ind.bb_lo[i] is not None:
            if C[i] < ind.bb_lo[i]:
                raw["bb_close_below_lower"].append(i)
            if C[i] > ind.bb_up[i]:
                raw["bb_close_above_upper"].append(i)

        if ind.sma50[i - 1] is not None and ind.sma50[i] is not None:
            if C[i - 1] <= ind.sma50[i - 1] and C[i] > ind.sma50[i]:
                raw["sma50_cross_above"].append(i)
            if C[i - 1] >= ind.sma50[i - 1] and C[i] < ind.sma50[i]:
                raw["sma50_cross_below"].append(i)

        if ind.sma50[i - 1] is not None and ind.sma200[i - 1] is not None and ind.sma200[i] is not None:
            if ind.sma50[i - 1] <= ind.sma200[i - 1] and ind.sma50[i] > ind.sma200[i]:
                raw["golden_cross"].append(i)
            if ind.sma50[i - 1] >= ind.sma200[i - 1] and ind.sma50[i] < ind.sma200[i]:
                raw["death_cross"].append(i)

        if C[i - 1] <= ind.ema9[i - 1] and C[i] > ind.ema9[i]:
            raw["ema9_cross_above"].append(i)
        if C[i - 1] >= ind.ema9[i - 1] and C[i] < ind.ema9[i]:
            raw["ema9_cross_below"].append(i)

    bw = ind.bandwidth
    sq_flag = [False] * n
    for i in range(n):
        if bw[i] is None:
            continue
        lo_needed = i - 119
        if lo_needed < 0 or bw[lo_needed] is None:
            continue
        window = [bw[j] for j in range(lo_needed, i + 1)]
        if any(w is None for w in window):
            continue
        p10 = percentile(sorted(window), 0.10)
        sq_flag[i] = bw[i] <= p10
    for i in range(n):
        if sq_flag[i] and not (i > 0 and sq_flag[i - 1]):
            for j in range(i + 1, min(i + 6, n)):
                if ind.bb_up[j] is None:
                    continue
                if C[j] > ind.bb_up[j]:
                    raw["bb_squeeze_break_up"].append(j)
                    break
                if C[j] < ind.bb_lo[j]:
                    raw["bb_squeeze_break_down"].append(j)
                    break

    return {name: dedup(sorted(set(days))) for name, days in raw.items()}


# -----------------------------------------------------------------------
# event-study stats (pooled across volatile names, split at EVENT_SPLIT_DATE)
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


def analyze_group(series, symbols, per_symbol_signals):
    all_days_fwd = {h: [] for h in HORIZONS}
    all_days_fwd_by_half = {h: {"pre": [], "post": []} for h in HORIZONS}
    for sym in symbols:
        bars = series[sym]
        C = bars["C"]
        dates = bars["dates"]
        n = len(C)
        for h in HORIZONS:
            for i in range(n - h):
                fr = C[i + h] / C[i] - 1.0
                all_days_fwd[h].append(fr)
                half = "pre" if dates[i] < EVENT_SPLIT_DATE else "post"
                all_days_fwd_by_half[h][half].append(fr)

    all_signals = {name: [] for name in SIGNAL_ORDER}
    for sym in symbols:
        for name in SIGNAL_ORDER:
            for d in per_symbol_signals[sym][name]:
                all_signals[name].append((sym, d))

    results = {}
    for name, sig_list in all_signals.items():
        results[name] = {}
        for h in HORIZONS:
            sample, sample_pre, sample_post = [], [], []
            for sym, d in sig_list:
                bars = series[sym]
                C = bars["C"]
                n = len(C)
                if d + h < n:
                    fr = C[d + h] / C[d] - 1.0
                    sample.append(fr)
                    if bars["dates"][d] < EVENT_SPLIT_DATE:
                        sample_pre.append(fr)
                    else:
                        sample_post.append(fr)
            baseline = all_days_fwd[h]
            n_sig = len(sample)
            t, diff = welch_t(sample, baseline) if n_sig >= 2 else (float("nan"), float("nan"))
            diff_pp = diff * 100 if not math.isnan(diff) else float("nan")

            base_pre = all_days_fwd_by_half[h]["pre"]
            base_post = all_days_fwd_by_half[h]["post"]
            diff_pre_pp = (mean(sample_pre) - mean(base_pre)) * 100 if len(sample_pre) >= 2 and base_pre else float("nan")
            diff_post_pp = (mean(sample_post) - mean(base_post)) * 100 if len(sample_post) >= 2 and base_post else float("nan")

            sign = 1 if DIRECTION[name] == "BULL" else -1
            sign_adj = sign * diff_pp if not math.isnan(diff_pp) else float("nan")

            results[name][h] = {
                "n": n_sig, "n_pre": len(sample_pre), "n_post": len(sample_post),
                "diff_pp": diff_pp, "t": t,
                "diff_pre_pp": diff_pre_pp, "diff_post_pp": diff_post_pp,
                "sign_adj_pp": sign_adj,
            }
    return results, all_signals


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


# -----------------------------------------------------------------------
# TEST 0: annualized volatility comparison
# -----------------------------------------------------------------------

def annualized_vol_pct(C):
    rets = [C[i] / C[i - 1] - 1.0 for i in range(1, len(C))]
    if len(rets) < 2:
        return float("nan")
    return stdev(rets) * math.sqrt(TRADING_DAYS_YEAR) * 100


def print_vol_comparison(volatile_series, largecap_series):
    print("-" * 110)
    print("TEST 0: ANNUALIZED VOLATILITY -- volatile-name universe vs large-cap universe")
    print("-" * 110)
    print(f"{'sym':6s} {'first_date':12s} {'n_bars':8s} {'ann_vol%':>10s}")
    vol_vals = []
    for sym in VOLATILE_SYMS:
        if sym not in volatile_series:
            continue
        bars = volatile_series[sym]
        v = annualized_vol_pct(bars["C"])
        vol_vals.append(v)
        print(f"{sym:6s} {bars['dates'][0]:12s} {len(bars['dates']):<8d} {fmt(v,2):>10s}")
    print()
    lc_vals = []
    for sym in LARGECAP_SYMS + [SPY]:
        bars = largecap_series[sym]
        v = annualized_vol_pct(bars["C"])
        lc_vals.append(v)
        print(f"{sym:6s} {bars['dates'][0]:12s} {len(bars['dates']):<8d} {fmt(v,2):>10s}")
    print()
    print(f"Median annualized vol -- volatile-name universe ({len(vol_vals)} names): {fmt(median(vol_vals),2)}%")
    print(f"Median annualized vol -- large-cap universe (14 names, SPY excluded from median): "
          f"{fmt(median(lc_vals[:-1]),2)}%")
    print(f"SPY annualized vol (separate): {fmt(lc_vals[-1],2)}%")
    print()


# -----------------------------------------------------------------------
# TEST 2: trading systems, per-name own-history midpoint split
# -----------------------------------------------------------------------

SYSTEM_WARMUP = {
    "macd": 35, "sma50": 50, "sma200": 200, "ema9": 30, "rsi": 20, "bollinger": 20,
}


def stateful_positions(buy_trigger, sell_trigger, n):
    state = [0] * n
    cur = 0
    for i in range(n):
        if cur == 0 and buy_trigger[i]:
            cur = 1
        elif cur == 1 and sell_trigger[i]:
            cur = 0
        state[i] = cur
    return state


def build_pos_target(bars, ind, system):
    C = bars["C"]
    n = len(C)
    if system == "macd":
        return [1 if ind.macd[i] > ind.signal[i] else 0 for i in range(n)]
    if system == "sma50":
        return [1 if (ind.sma50[i] is not None and C[i] > ind.sma50[i]) else 0 for i in range(n)]
    if system == "sma200":
        return [1 if (ind.sma200[i] is not None and C[i] > ind.sma200[i]) else 0 for i in range(n)]
    if system == "ema9":
        return [1 if C[i] > ind.ema9[i] else 0 for i in range(n)]
    if system == "rsi":
        buy = [ind.rsi[i - 1] is not None and ind.rsi[i - 1] < 30 and ind.rsi[i] >= 30 if i > 0 else False for i in range(n)]
        sell = [ind.rsi[i - 1] is not None and ind.rsi[i - 1] <= 70 and ind.rsi[i] > 70 if i > 0 else False for i in range(n)]
        return stateful_positions(buy, sell, n)
    if system == "bollinger":
        buy = [ind.bb_lo[i] is not None and C[i] < ind.bb_lo[i] for i in range(n)]
        sell = [ind.bb_mid[i] is not None and C[i] > ind.bb_mid[i] for i in range(n)]
        return stateful_positions(buy, sell, n)
    raise ValueError(system)


def simulate(dates, C, pos_target, start_idx):
    n = len(C)
    out_dates, rets, poss, trade_dates = [], [], [], []
    prev_pos = 0
    for i in range(start_idx + 1, n):
        target = pos_target[i - 1]
        raw_ret = C[i] / C[i - 1] - 1.0
        ret = target * raw_ret
        changed = target != prev_pos
        if changed:
            ret -= COST_PER_SIDE
            if target == 1:
                trade_dates.append(dates[i])
        rets.append(ret)
        poss.append(target)
        out_dates.append(dates[i])
        prev_pos = target
    return out_dates, rets, poss, trade_dates


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


def period_stats(out_dates, rets, poss, trade_dates, date_lo=None, date_hi=None):
    idx = [k for k, d in enumerate(out_dates) if (date_lo is None or d >= date_lo) and (date_hi is None or d < date_hi)]
    if not idx:
        return None
    sub_rets = [rets[k] for k in idx]
    sub_poss = [poss[k] for k in idx]
    n_trades = sum(1 for d in trade_dates if (date_lo is None or d >= date_lo) and (date_hi is None or d < date_hi))
    years = len(idx) / TRADING_DAYS_YEAR
    m = perf_metrics(sub_rets)
    m["trades_per_yr"] = n_trades / years if years > 0 else float("nan")
    m["pct_invested"] = mean(sub_poss) * 100
    m["n_days"] = len(idx)
    return m


def run_system_for_symbol(bars, ind, system):
    n = len(bars["C"])
    warmup = SYSTEM_WARMUP[system]
    if n <= warmup + 2:
        return None
    own_mid_date = bars["dates"][n // 2]
    pos_target = build_pos_target(bars, ind, system)
    dates, rets, poss, trades = simulate(bars["dates"], bars["C"], pos_target, warmup)
    bh_target = [1] * n
    bh_dates, bh_rets, bh_poss, bh_trades = simulate(bars["dates"], bars["C"], bh_target, warmup)

    out = {}
    for label, lo, hi in [("full", None, None), ("first", None, own_mid_date), ("second", own_mid_date, None)]:
        sys_stats = period_stats(dates, rets, poss, trades, lo, hi)
        bh_stats = period_stats(bh_dates, bh_rets, bh_poss, bh_trades, lo, hi)
        out[label] = {"sys": sys_stats, "bh": bh_stats}
    out["own_mid_date"] = own_mid_date
    return out


def fmt_row(m):
    if m is None:
        return "NA".rjust(8) * 6
    return (f"{fmt(m['cagr']*100,2):>8s}{fmt(m['vol']*100,2):>8s}{fmt(m['sharpe'],2):>8s}"
            f"{fmt(m['maxdd']*100,2):>8s}{fmt(m['trades_per_yr'],2):>8s}{fmt(m['pct_invested'],1):>8s}")


def print_system_table(system, per_symbol_runs):
    print(f"--- SYSTEM: {system} ---")
    colhdr = f"{'sym':6s}{'period':7s}| {'sys_cagr%':>8s}{'sys_vol%':>8s}{'sys_shrp':>8s}{'sys_mdd%':>8s}{'sys_tpy':>8s}{'sys_pin%':>8s} | {'bh_cagr%':>8s}{'bh_vol%':>8s}{'bh_shrp':>8s}{'bh_mdd%':>8s}{'bh_tpy':>8s}{'bh_pin%':>8s}"
    print(colhdr)
    print("-" * len(colhdr))

    n_beats = {"full": 0, "first": 0, "second": 0}
    n_valid = {"full": 0, "first": 0, "second": 0}
    dd_cut_pp = {"full": [], "first": [], "second": []}  # positive = system's |mdd| smaller than bh's |mdd|

    for sym in VOLATILE_SYMS:
        run = per_symbol_runs.get(sym)
        if run is None:
            print(f"{sym:6s}{'--':7s}| insufficient history")
            continue
        for label in ["full", "first", "second"]:
            sys_m, bh_m = run[label]["sys"], run[label]["bh"]
            print(f"{sym:6s}{label:7s}| {fmt_row(sys_m)} | {fmt_row(bh_m)}")
            if sys_m is not None and bh_m is not None and not math.isnan(sys_m["sharpe"]) and not math.isnan(bh_m["sharpe"]):
                n_valid[label] += 1
                if sys_m["sharpe"] > bh_m["sharpe"]:
                    n_beats[label] += 1
            if sys_m is not None and bh_m is not None and not math.isnan(sys_m["maxdd"]) and not math.isnan(bh_m["maxdd"]):
                cut = (abs(bh_m["maxdd"]) - abs(sys_m["maxdd"])) * 100
                dd_cut_pp[label].append(cut)
    print("-" * len(colhdr))
    for label in ["full", "first", "second"]:
        med_cut = median(dd_cut_pp[label]) if dd_cut_pp[label] else float("nan")
        print(f"  [{label}] beats B&H on Sharpe: {n_beats[label]}/{n_valid[label]}  "
              f"median max-drawdown cut vs B&H: {fmt(med_cut,2)}pp")
    print()
    return n_beats, n_valid, dd_cut_pp


# -----------------------------------------------------------------------
# ROBUSTNESS CHECK (added after coordinator follow-up on the macd_cross_below_zero
# survivor): pooling 22 names' signals treats each signal-day as an independent
# observation, but signals cluster on the same calendar dates (esp. the 2022
# growth-stock selloff), so the naive Welch t overstates how many independent
# pieces of evidence there really are. Four checks, run only on the flagged
# signal (macd_cross_below_zero) and its natural control (macd_cross_above_zero,
# same indicator, opposite sign, no reason to expect it survives) at all three
# horizons. All numbers here are diagnostic/supplementary -- not a new
# pre-registered family, not held to a fresh Bonferroni bar; they test whether
# the ALREADY-FLAGGED cell survives being de-clustered, market-neutralized, and
# stripped of the single worst year.
# -----------------------------------------------------------------------

ROBUSTNESS_SIGNALS = ["macd_cross_below_zero", "macd_cross_above_zero"]
CLUSTER_GAP_DAYS = 10  # trading days; consecutive signal dates closer than this = same episode
EXCLUDE_YEAR = "2022"


def build_global_calendar(series, symbols):
    cal = sorted(set().union(*(set(series[s]["dates"]) for s in symbols)))
    idx = {d: i for i, d in enumerate(cal)}
    return cal, idx


def build_equal_weight_benchmark(series, symbols, horizons):
    """bench[h][date] = equal-weight average forward-h-day return across `symbols`,
    starting from `date`, using each symbol's own price series. This is the
    sector-neutral benchmark: a name's excess return relative to THIS, on THIS
    date, nets out a move common to the whole pool (e.g. a market-wide selloff)."""
    sums = {h: defaultdict(lambda: [0.0, 0]) for h in horizons}
    for sym in symbols:
        bars = series[sym]
        C, dates, n = bars["C"], bars["dates"], len(bars["C"])
        for h in horizons:
            for i in range(n - h):
                acc = sums[h][dates[i]]
                acc[0] += C[i + h] / C[i] - 1.0
                acc[1] += 1
    return {h: {d: (s / c) for d, (s, c) in sums[h].items()} for h in horizons}


def baseline_returns(series, symbols, h, exclude_year=None):
    """All (symbol, day) forward-h-day returns, optionally dropping any day whose
    date falls in `exclude_year` (used for the 2022-removed check)."""
    vals = []
    for sym in symbols:
        bars = series[sym]
        C, dates, n = bars["C"], bars["dates"], len(bars["C"])
        for i in range(n - h):
            if exclude_year is not None and dates[i][:4] == exclude_year:
                continue
            vals.append(C[i + h] / C[i] - 1.0)
    return vals


def one_sample_t(values):
    n = len(values)
    if n < 2:
        return float("nan")
    sd = stdev(values)
    if sd == 0:
        return float("nan")
    return mean(values) / (sd / math.sqrt(n))


def cluster_by_date(recs_with_excess):
    """recs_with_excess: list of (date_str, excess_return). Average within date
    first (one number per date), THEN return that list of per-date averages --
    the clustered t is a one-sample t-test on this list, with n = distinct dates,
    not n = distinct signal instances."""
    by_date = defaultdict(list)
    for d, ex in recs_with_excess:
        by_date[d].append(ex)
    return [mean(v) for v in by_date.values()]


def count_episodes(distinct_dates, cal_index, gap_days=CLUSTER_GAP_DAYS):
    if not distinct_dates:
        return 0
    idxs = sorted(cal_index[d] for d in distinct_dates)
    n_episodes = 1
    prev = idxs[0]
    for ix in idxs[1:]:
        if ix - prev >= gap_days:
            n_episodes += 1
        prev = ix
    return n_episodes


def run_robustness_check(series, active_syms, sig_signals):
    cal, cal_index = build_global_calendar(series, active_syms)
    bench = build_equal_weight_benchmark(series, active_syms, HORIZONS)
    baseline_all = {h: baseline_returns(series, active_syms, h) for h in HORIZONS}
    baseline_ex2022 = {h: baseline_returns(series, active_syms, h, exclude_year=EXCLUDE_YEAR) for h in HORIZONS}

    print("#" * 110)
    print("ROBUSTNESS CHECK ON THE MACD-ZERO-CROSS SURVIVOR (coordinator follow-up)")
    print("#" * 110)
    print("Target signal (flagged survivor): macd_cross_below_zero. Control (same indicator, opposite")
    print("sign, no prior reason to expect it survives): macd_cross_above_zero. Diagnostic only -- not")
    print(f"a new Bonferroni family. Episode gap threshold: {CLUSTER_GAP_DAYS} trading days. Excluded year for")
    print(f"check (3): {EXCLUDE_YEAR}. Sector-neutral benchmark (check 4): equal-weight avg fwd return")
    print("across the 22-name pool, same start date, same horizon.")
    print()

    for name in ROBUSTNESS_SIGNALS:
        for h in HORIZONS:
            recs = []
            for sym, d in sig_signals[name]:
                bars = series[sym]
                C, dates, n = bars["C"], bars["dates"], len(bars["C"])
                if d + h >= n:
                    continue
                recs.append((sym, dates[d], C[d + h] / C[d] - 1.0))

            n_total = len(recs)
            distinct_dates = sorted(set(r[1] for r in recs))
            n_dates = len(distinct_dates)
            n_episodes = count_episodes(distinct_dates, cal_index)

            # (1) date-clustered t vs the unconditional pooled baseline
            base_mean = mean(baseline_all[h]) if baseline_all[h] else float("nan")
            excess_uncond = [(r[1], r[2] - base_mean) for r in recs]
            date_avgs = cluster_by_date(excess_uncond)
            t_clust = one_sample_t(date_avgs)
            diff_clust_pp = mean(date_avgs) * 100 if date_avgs else float("nan")

            # naive (uncorrected) pooled t, for reference -- same method as the primary test
            sample = [r[2] for r in recs]
            t_naive, diff_naive = welch_t(sample, baseline_all[h]) if n_total >= 2 else (float("nan"), float("nan"))
            diff_naive_pp = diff_naive * 100 if not math.isnan(diff_naive) else float("nan")

            # (3) with 2022 removed entirely (both signal instances AND baseline)
            recs_ex = [r for r in recs if r[1][:4] != EXCLUDE_YEAR]
            n_ex = len(recs_ex)
            sample_ex = [r[2] for r in recs_ex]
            t_naive_ex, diff_naive_ex = (welch_t(sample_ex, baseline_ex2022[h]) if n_ex >= 2 and baseline_ex2022[h]
                                          else (float("nan"), float("nan")))
            diff_naive_ex_pp = diff_naive_ex * 100 if not math.isnan(diff_naive_ex) else float("nan")
            base_mean_ex = mean(baseline_ex2022[h]) if baseline_ex2022[h] else float("nan")
            excess_ex = [(r[1], r[2] - base_mean_ex) for r in recs_ex]
            date_avgs_ex = cluster_by_date(excess_ex)
            t_clust_ex = one_sample_t(date_avgs_ex)
            n_dates_ex = len(date_avgs_ex)

            # (4) sector-neutral: excess vs contemporaneous equal-weight benchmark
            recs_sn = [(r[0], r[1], r[2] - bench[h][r[1]]) for r in recs if r[1] in bench[h]]
            n_sn = len(recs_sn)
            sn_values = [r[2] for r in recs_sn]
            t_sn_naive = one_sample_t(sn_values)
            diff_sn_pp = mean(sn_values) * 100 if sn_values else float("nan")
            sn_excess_for_cluster = [(r[1], r[2]) for r in recs_sn]
            date_avgs_sn = cluster_by_date(sn_excess_for_cluster)
            t_sn_clust = one_sample_t(date_avgs_sn)
            n_dates_sn = len(date_avgs_sn)

            print(f"  -- {name} h={h} --")
            print(f"    n_instances={n_total}  n_distinct_dates={n_dates}  n_episodes(gap<{CLUSTER_GAP_DAYS}d)={n_episodes}")
            print(f"    (1) naive pooled (uncorrected, matches primary table):      diff_pp={fmt(diff_naive_pp)}  t={fmt(t_naive,2)}")
            print(f"    (1) date-clustered (one obs/date, n={n_dates}):              diff_pp={fmt(diff_clust_pp)}  t={fmt(t_clust,2)}")
            print(f"    (3) 2022 removed, naive pooled (n={n_ex}, n_dates={n_dates_ex}): diff_pp={fmt(diff_naive_ex_pp)}  t={fmt(t_naive_ex,2)}")
            print(f"    (3) 2022 removed, date-clustered:                            diff_pp={fmt(mean(date_avgs_ex)*100 if date_avgs_ex else float('nan'))}  t={fmt(t_clust_ex,2)}")
            print(f"    (4) sector-neutral (vs 22-name equal-weight bench), naive (n={n_sn}): diff_pp={fmt(diff_sn_pp)}  t={fmt(t_sn_naive,2)}")
            print(f"    (4) sector-neutral, date-clustered (n_dates={n_dates_sn}):    diff_pp={fmt(mean(date_avgs_sn)*100 if date_avgs_sn else float('nan'))}  t={fmt(t_sn_clust,2)}")
            print()
    print("Done (robustness check).")
    print()


# -----------------------------------------------------------------------
# main
# -----------------------------------------------------------------------

def main():
    volatile_series, excluded = load_volatile()
    largecap_series = load_largecap()

    print("=" * 110)
    print("CHART INDICATORS ON VOLATILE GROWTH NAMES -- RAW TEST OUTPUT")
    print("=" * 110)
    print(f"Volatile-name universe ({len(volatile_series)} of {len(VOLATILE_SYMS)} requested): "
          f"{sorted(volatile_series.keys())}")
    if excluded:
        print(f"Excluded (< {MIN_BARS} bars, ~3 years): {excluded}")
    else:
        print(f"None excluded -- all {len(VOLATILE_SYMS)} names have >= {MIN_BARS} bars.")
    print(f"Large-cap comparison universe (14 + SPY, from indicators_price.py): {LARGECAP_SYMS + [SPY]}")
    print(f"Horizons (trading days): {HORIZONS}")
    print(f"Dedup window: {DEDUP_WINDOW} trading days")
    print(f"Event-study split date (fixed, pooled): {EVENT_SPLIT_DATE}")
    print(f"Trading-systems split: each name's OWN midpoint date (own history split in half)")
    print()

    print_vol_comparison(volatile_series, largecap_series)

    indicators = {sym: Indicators(volatile_series[sym]) for sym in volatile_series}
    per_symbol_signals = {sym: detect_signals(volatile_series[sym], indicators[sym]) for sym in volatile_series}

    print("#" * 110)
    print("TEST 1: EVENT STUDY (pooled across volatile names)")
    print("#" * 110)
    active_syms = [s for s in VOLATILE_SYMS if s in volatile_series]
    results, sig_signals = analyze_group(volatile_series, active_syms, per_symbol_signals)
    n_tests_main = len(SIGNAL_ORDER) * len(HORIZONS)

    header = f"{'signal':26s} {'h':>3s} {'n':>6s} {'diff_pp':>9s} {'t':>7s} {'pre_pp':>9s} {'post_pp':>9s} {'sign_adj_pp':>12s} {'dir':>4s}"
    print(header)
    print("-" * len(header))
    for name in SIGNAL_ORDER:
        for h in HORIZONS:
            r = results[name][h]
            print(f"{name:26s} {h:>3d} {r['n']:>6d} {fmt(r['diff_pp']):>9s} {fmt(r['t'],2):>7s} "
                  f"{fmt(r['diff_pre_pp']):>9s} {fmt(r['diff_post_pp']):>9s} {fmt(r['sign_adj_pp']):>12s} {DIRECTION[name]:>4s}")
    print()
    print("(pre_pp/post_pp above are the diff before/after the fixed pooled split date "
          f"{EVENT_SPLIT_DATE}, NOT per-name halves.)")
    print()

    print("-" * 110)
    print("SIGNAL COUNTS (raw, after dedup) -- volatile-name pool")
    print("-" * 110)
    for name in SIGNAL_ORDER:
        total_n = sum(len(per_symbol_signals[s][name]) for s in active_syms)
        print(f"  {name:26s} n={total_n}")
    print()

    print("-" * 110)
    print("MULTIPLE TESTING")
    print("-" * 110)
    print(f"Primary pre-registered family: {len(SIGNAL_ORDER)} signals x {len(HORIZONS)} horizons = {n_tests_main} tests "
          f"(volatile-name pool, full sample).")
    crit_main = bonferroni_t(n_tests_main)
    print(f"  Bonferroni alpha=0.05/{n_tests_main} -> two-tailed critical |t| ~= {crit_main:.3f}")
    print()

    print("-" * 110)
    print(f"SURVIVORS: full-sample |t| exceeds the Bonferroni threshold ({crit_main:.3f}) "
          "AND both half-sample diffs share the predicted sign")
    print("-" * 110)
    any_survivor = False
    for name in SIGNAL_ORDER:
        expected_sign = 1 if DIRECTION[name] == "BULL" else -1
        for h in HORIZONS:
            r = results[name][h]
            t = r["t"]
            if math.isnan(t):
                continue
            passes = abs(t) > crit_main
            pre_ok = (not math.isnan(r["diff_pre_pp"])) and (r["diff_pre_pp"] * expected_sign > 0)
            post_ok = (not math.isnan(r["diff_post_pp"])) and (r["diff_post_pp"] * expected_sign > 0)
            if passes and pre_ok and post_ok:
                any_survivor = True
                print(f"  SURVIVOR: {name} h={h} t={t:.2f} diff_pp={r['diff_pp']:.3f} "
                      f"pre_pp={r['diff_pre_pp']:.3f} post_pp={r['diff_post_pp']:.3f}")
    if not any_survivor:
        print("  none")
    print()

    run_robustness_check(volatile_series, active_syms, sig_signals)

    print("#" * 110)
    print("TEST 2: TRADING SYSTEMS (per name, own-history halves)")
    print("#" * 110)
    print(f"Cost: {COST_PER_SIDE*100:.2f}% per side, applied on every position-change day. Cash earns 0.")
    print()

    all_beats = {}
    for system in ["macd", "sma50", "sma200", "ema9", "rsi", "bollinger"]:
        per_symbol_runs = {}
        for sym in active_syms:
            per_symbol_runs[sym] = run_system_for_symbol(volatile_series[sym], indicators[sym], system)
        n_beats, n_valid, dd_cut_pp = print_system_table(system, per_symbol_runs)
        all_beats[system] = (n_beats, n_valid, dd_cut_pp)

    print("-" * 110)
    print("HEADLINE SUMMARY: names (of 22) beating buy-and-hold on Sharpe, by system and period; "
          "median max-drawdown cut vs B&H")
    print("-" * 110)
    for system, (n_beats, n_valid, dd_cut_pp) in all_beats.items():
        parts = []
        for label in ["full", "first", "second"]:
            med_cut = median(dd_cut_pp[label]) if dd_cut_pp[label] else float("nan")
            parts.append(f"{label}={n_beats[label]}/{n_valid[label]} (mdd_cut={fmt(med_cut,1)}pp)")
        print(f"  {system:10s} " + "  ".join(parts))
    print()
    print("Done.")


if __name__ == "__main__":
    main()
