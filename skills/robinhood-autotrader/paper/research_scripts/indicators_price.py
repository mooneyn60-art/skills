"""
Chart indicators (price-based), part 1: MACD, RSI, Bollinger Bands, SMA(50),
EMA(9) -- mechanical, pre-registered signal + system test.

RESEARCH_AGENDA item (Nolan's "test every indicator on my Robinhood chart").
Predictions were written and committed BEFORE this script was run
(research/2026-09-24_INDICATORS_PRICE.md, commit 9f0f731). This script
implements the test described there. It prints raw numbers only -- no
conclusions are hardcoded here; the verdict is written into the note by hand
after reading this output.

Universe: 14 large caps (AAPL AMZN BAC C CSCO F GE GOOGL IBM MSFT NVDA PFE T
XOM), pooled, plus SPY reported separately. Daily OHLC, 2006-01-03 to
2026-09-18 (paper/history/daily_stocks.json). Weekly VIX closes
(paper/history/vix_weekly.json) used for the VIX-regime splits.

Loading, dedup, Welch t-test, split-sample and VIX-regime plumbing follow
paper/research_scripts/candlesticks.py for consistency.

-----------------------------------------------------------------------------
INDICATOR DEFINITIONS (exact settings, written before looking at any results)
-----------------------------------------------------------------------------

EMA(span): seeded EMA[0] = C[0], EMA[i] = a*C[i] + (1-a)*EMA[i-1],
a = 2/(span+1). Standard recursive EMA; early values carry seed bias, which
is why every system below has a warmup period before it starts trading (see
SYSTEM WARMUPS).

MACD(12,26,9): macd_line = EMA(C,12) - EMA(C,26); signal_line =
EMA(macd_line, 9) (same seeded-EMA formula applied to the MACD line itself).
Histogram = macd_line - signal_line (not separately tested; the sign of the
histogram is exactly the sign-cross condition below).

RSI(14), Wilder: day-over-day gain/loss; first RSI value (day index 14) uses
a simple 14-day average gain/loss; every subsequent value uses Wilder
smoothing avg = (avg*(13) + new)/14. RSI = 100 - 100/(1+avg_gain/avg_loss);
100 if avg_loss == 0.

Bollinger(20, 2): mid = 20-day SMA of close; sd = 20-day POPULATION std
(ddof=0) of close; upper = mid + 2*sd; lower = mid - 2*sd.

SMA(50), SMA(200), EMA(9): as named, on close.

-----------------------------------------------------------------------------
TEST 1 -- EVENT STUDY: SIGNAL DEFINITIONS (18 signal types x 3 horizons = 54
primary tests; VIX-regime cuts on RSI<30 and BB-below-lower add 2*3*3=18 more,
reported but not part of the primary Bonferroni family)
-----------------------------------------------------------------------------
  MACD bullish signal cross:  macd[i-1] <= signal[i-1] and macd[i] > signal[i]   [BULL]
  MACD bearish signal cross:  macd[i-1] >= signal[i-1] and macd[i] < signal[i]   [BEAR]
  MACD crosses above zero:    macd[i-1] <= 0 and macd[i] > 0                     [BULL]
  MACD crosses below zero:    macd[i-1] >= 0 and macd[i] < 0                     [BEAR]
  RSI crosses below 30:       rsi[i-1] >= 30 and rsi[i] < 30                     [BULL] (oversold, textbook reversal-up reading)
  RSI crosses above 70:       rsi[i-1] <= 70 and rsi[i] > 70                     [BEAR] (overbought, textbook reversal-down reading)
  RSI crosses back above 30:  rsi[i-1] < 30 and rsi[i] >= 30                     [BULL]
  RSI crosses above 50:       rsi[i-1] < 50 and rsi[i] >= 50                     [BULL]
  BB close below lower band:  C[i] < lower[i]                                    [BULL] (textbook mean-reversion reading)
  BB close above upper band:  C[i] > upper[i]                                    [BEAR] (textbook mean-reversion reading)
  BB squeeze -> break up:     see below                                          [BULL]
  BB squeeze -> break down:   see below                                          [BEAR]
  SMA50 crosses above:        C[i-1] <= sma50[i-1] and C[i] > sma50[i]           [BULL]
  SMA50 crosses below:        C[i-1] >= sma50[i-1] and C[i] < sma50[i]           [BEAR]
  Golden cross (50>200):      sma50[i-1] <= sma200[i-1] and sma50[i] > sma200[i] [BULL]
  Death cross (50<200):       sma50[i-1] >= sma200[i-1] and sma50[i] < sma200[i] [BEAR]
  EMA9 crosses above:         C[i-1] <= ema9[i-1] and C[i] > ema9[i]             [BULL]
  EMA9 crosses below:         C[i-1] >= ema9[i-1] and C[i] < ema9[i]             [BEAR]

  Squeeze definition: bandwidth[i] = (upper[i]-lower[i])/mid[i]. A "squeeze
  start" day is the first day of a run where bandwidth[i] is at or below the
  10th percentile of the trailing 120 trading days of bandwidth (inclusive of
  day i). From each squeeze-start day, scan forward up to 5 trading days for
  the first close outside either band; that breakout day (not the squeeze
  day) is the signal day, recorded as squeeze_break_up or squeeze_break_down.
  If no breakout occurs within 5 days, the squeeze episode produces no signal.

  Dedup: for each (symbol, signal) only the FIRST day of a run counts; once a
  signal fires, the next 5 trading days for that symbol+signal are skipped
  even if the condition still holds (identical rule/code to candlesticks.py).

Baseline / diff / t-stat / sign-adjustment: identical method to
candlesticks.py -- baseline is the mean forward return over ALL days (not
just signal days) in the same symbol group and horizon; diff = signal mean
minus baseline mean, in percentage points; t = Welch's two-sample t-test;
sign_adj = diff for BULL-tagged signals, -diff for BEAR-tagged signals (so a
positive sign_adj always means "behaved the way the textbook label predicts").

-----------------------------------------------------------------------------
TEST 2 -- TRADING SYSTEMS
-----------------------------------------------------------------------------
Long/flat, no leverage, no shorting. A system's target position for day i is
decided using data available at close of day i; the position is ACTED ON at
day i+1 (approximated here with day i+1's close-to-close return, i.e. the
position used for return r[i+1] = C[i+1]/C[i]-1 is the target computed at
close of day i -- this avoids lookahead while keeping the simulation to
close-to-close returns, a standard simplification; it does not use open
prices even though the position is described as "acting at the next day's
open"). Cost = 0.10% applied on every day the position changes (each side
priced once, so a full round trip costs 0.20% total, 0.10% in and 0.10% out).
Cash earns 0.

  MACD system:      long when macd[i] > signal[i], else cash. Flips freely.
  SMA(50) system:    long when C[i] > sma50[i], else cash. Flips freely.
  SMA(200) system:   long when C[i] > sma200[i], else cash (comparison only).
  EMA(9) system:     long when C[i] > ema9[i], else cash. Flips freely.
  RSI system:        stateful. Buy (state -> 1) on "RSI crosses back above
                      30 from below". Sell (state -> 0) on "RSI crosses
                      above 70". Otherwise holds current state. Starts flat.
  Bollinger system:  stateful. Buy (state -> 1) on close < lower band. Sell
                      (state -> 0) on close > mid band. Otherwise holds.
                      Starts flat.

SYSTEM WARMUPS (bars skipped before a system is allowed to trade, and before
which its matched buy-and-hold comparison also does not start -- this keeps
the system vs buy-and-hold comparison over the identical date window):
  MACD: 35 bars (26+9). SMA50/Bollinger-buy-hold-for-SMA: 50 bars.
  SMA200: 200 bars. EMA9: 30 bars. RSI system: 20 bars. Bollinger system:
  20 bars.

Metrics (per symbol, then equal-weight averaged across the 14; SPY reported
separately): CAGR, annualized vol, Sharpe (rf=0), max drawdown, trades per
year (count of position-change days / years in window), % of days invested.
Reported for the system and for buy-and-hold over the identical window, full
sample and both halves (split 2016-06-01, same as Test 1; each half's
metrics are computed on that half's own return slice, i.e. as if capital
restarted at 1.0 at the start of the half -- position STATE for stateful
systems still carries over continuously from before the split, only the P&L
accounting resets).
"""

import json
import math
from pathlib import Path
from statistics import mean, stdev

REPO = Path(__file__).resolve().parents[2]
STOCKS_PATH = REPO / "paper" / "history" / "daily_stocks.json"
VIX_PATH = REPO / "paper" / "history" / "vix_weekly.json"

SPLIT_DATE = "2016-06-01"
HORIZONS = [5, 10, 21]
DEDUP_WINDOW = 5
COST_PER_SIDE = 0.001
TRADING_DAYS_YEAR = 252

ALL_STOCKS_14 = ["AAPL", "AMZN", "BAC", "C", "CSCO", "F", "GE", "GOOGL", "IBM", "MSFT", "NVDA", "PFE", "T", "XOM"]
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

def load_data():
    raw = json.loads(STOCKS_PATH.read_text())
    vix_raw = json.loads(VIX_PATH.read_text())
    series = {}
    for sym, bars in raw.items():
        dates = sorted(bars.keys())
        O = [bars[d][0] for d in dates]
        H = [bars[d][1] for d in dates]
        L = [bars[d][2] for d in dates]
        C = [bars[d][3] for d in dates]
        series[sym] = {"dates": dates, "O": O, "H": H, "L": L, "C": C}
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


# -----------------------------------------------------------------------
# indicators
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
# dedup (identical logic to candlesticks.py)
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
# signal detection
# -----------------------------------------------------------------------

def detect_signals(bars, ind):
    C = bars["C"]
    n = len(C)
    raw = {name: [] for name in SIGNAL_ORDER}

    for i in range(1, n):
        # MACD
        if ind.macd[i - 1] <= ind.signal[i - 1] and ind.macd[i] > ind.signal[i]:
            raw["macd_bull_cross"].append(i)
        if ind.macd[i - 1] >= ind.signal[i - 1] and ind.macd[i] < ind.signal[i]:
            raw["macd_bear_cross"].append(i)
        if ind.macd[i - 1] <= 0 and ind.macd[i] > 0:
            raw["macd_cross_above_zero"].append(i)
        if ind.macd[i - 1] >= 0 and ind.macd[i] < 0:
            raw["macd_cross_below_zero"].append(i)

        # RSI
        if ind.rsi[i - 1] is not None and ind.rsi[i] is not None:
            if ind.rsi[i - 1] >= 30 and ind.rsi[i] < 30:
                raw["rsi_cross_below_30"].append(i)
            if ind.rsi[i - 1] <= 70 and ind.rsi[i] > 70:
                raw["rsi_cross_above_70"].append(i)
            if ind.rsi[i - 1] < 30 and ind.rsi[i] >= 30:
                raw["rsi_cross_back_above_30"].append(i)
            if ind.rsi[i - 1] < 50 and ind.rsi[i] >= 50:
                raw["rsi_cross_above_50"].append(i)

        # Bollinger band touches
        if ind.bb_lo[i] is not None:
            if C[i] < ind.bb_lo[i]:
                raw["bb_close_below_lower"].append(i)
            if C[i] > ind.bb_up[i]:
                raw["bb_close_above_upper"].append(i)

        # SMA50
        if ind.sma50[i - 1] is not None and ind.sma50[i] is not None:
            if C[i - 1] <= ind.sma50[i - 1] and C[i] > ind.sma50[i]:
                raw["sma50_cross_above"].append(i)
            if C[i - 1] >= ind.sma50[i - 1] and C[i] < ind.sma50[i]:
                raw["sma50_cross_below"].append(i)

        # golden/death cross
        if ind.sma50[i - 1] is not None and ind.sma200[i - 1] is not None and ind.sma200[i] is not None:
            if ind.sma50[i - 1] <= ind.sma200[i - 1] and ind.sma50[i] > ind.sma200[i]:
                raw["golden_cross"].append(i)
            if ind.sma50[i - 1] >= ind.sma200[i - 1] and ind.sma50[i] < ind.sma200[i]:
                raw["death_cross"].append(i)

        # EMA9
        if C[i - 1] <= ind.ema9[i - 1] and C[i] > ind.ema9[i]:
            raw["ema9_cross_above"].append(i)
        if C[i - 1] >= ind.ema9[i - 1] and C[i] < ind.ema9[i]:
            raw["ema9_cross_below"].append(i)

    # squeeze -> breakout
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
# event-study stats (mirrors candlesticks.py analyze_group)
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
                half = "pre" if dates[i] < SPLIT_DATE else "post"
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
                    if bars["dates"][d] < SPLIT_DATE:
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


def analyze_vix_regime(series, symbols, per_symbol_signals, signal_name, vix_dates, vix_vals):
    regimes = {"lt20": [], "20to25": [], "gte25": []}
    for sym in symbols:
        bars = series[sym]
        dates = bars["dates"]
        for d in per_symbol_signals[sym][signal_name]:
            v = vix_asof(vix_dates, vix_vals, dates[d])
            if v is None:
                continue
            key = "lt20" if v < 20 else ("20to25" if v < 25 else "gte25")
            regimes[key].append((sym, d))

    baseline_fwd = {h: [] for h in HORIZONS}
    for sym in symbols:
        bars = series[sym]
        C = bars["C"]
        n = len(C)
        for h in HORIZONS:
            for i in range(n - h):
                baseline_fwd[h].append(C[i + h] / C[i] - 1.0)

    out = {}
    for regime, sig_list in regimes.items():
        out[regime] = {"n": len(sig_list)}
        for h in HORIZONS:
            sample = []
            for sym, d in sig_list:
                bars = series[sym]
                C = bars["C"]
                if d + h < len(C):
                    sample.append(C[d + h] / C[d] - 1.0)
            baseline = baseline_fwd[h]
            if len(sample) >= 2:
                t, diff = welch_t(sample, baseline)
            else:
                t, diff = float("nan"), float("nan")
            out[regime][h] = {"n": len(sample), "diff_pp": diff * 100 if not math.isnan(diff) else float("nan"), "t": t}
    return out


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
# TEST 2: trading systems
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
    """pos_target[i-1] decides the position used for return r[i]=C[i]/C[i-1]-1.
    Returns lists aligned from index start_idx+1..n-1."""
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
    pos_target = build_pos_target(bars, ind, system)
    dates, rets, poss, trades = simulate(bars["dates"], bars["C"], pos_target, warmup)
    bh_target = [1] * n
    bh_dates, bh_rets, bh_poss, bh_trades = simulate(bars["dates"], bars["C"], bh_target, warmup)

    out = {}
    for label, lo, hi in [("full", None, None), ("pre", None, SPLIT_DATE), ("post", SPLIT_DATE, None)]:
        sys_stats = period_stats(dates, rets, poss, trades, lo, hi)
        bh_stats = period_stats(bh_dates, bh_rets, bh_poss, bh_trades, lo, hi)
        out[label] = {"sys": sys_stats, "bh": bh_stats}
    return out


def fmt_row(m):
    if m is None:
        return "NA".rjust(8) * 6
    return (f"{fmt(m['cagr']*100,2):>8s}{fmt(m['vol']*100,2):>8s}{fmt(m['sharpe'],2):>8s}"
            f"{fmt(m['maxdd']*100,2):>8s}{fmt(m['trades_per_yr'],2):>8s}{fmt(m['pct_invested'],1):>8s}")


def print_system_table(system, per_symbol_runs, spy_run):
    print(f"--- SYSTEM: {system} ---")
    colhdr = f"{'sym':6s}{'period':6s}| {'sys_cagr%':>8s}{'sys_vol%':>8s}{'sys_shrp':>8s}{'sys_mdd%':>8s}{'sys_tpy':>8s}{'sys_pin%':>8s} | {'bh_cagr%':>8s}{'bh_vol%':>8s}{'bh_shrp':>8s}{'bh_mdd%':>8s}{'bh_tpy':>8s}{'bh_pin%':>8s}"
    print(colhdr)
    print("-" * len(colhdr))

    avg_rows = {"full": {}, "pre": {}, "post": {}}
    for label in ["full", "pre", "post"]:
        for key in ["sys", "bh"]:
            for metric in ["cagr", "vol", "sharpe", "maxdd", "trades_per_yr", "pct_invested"]:
                avg_rows[label][(key, metric)] = []

    n_beats = {"full": 0, "pre": 0, "post": 0}
    n_valid = {"full": 0, "pre": 0, "post": 0}
    for sym in ALL_STOCKS_14:
        run = per_symbol_runs[sym]
        if run is None:
            print(f"{sym:6s}{'--':6s}| insufficient history")
            continue
        for label in ["full", "pre", "post"]:
            sys_m, bh_m = run[label]["sys"], run[label]["bh"]
            print(f"{sym:6s}{label:6s}| {fmt_row(sys_m)} | {fmt_row(bh_m)}")
            if sys_m is not None:
                for metric in ["cagr", "vol", "sharpe", "maxdd", "trades_per_yr", "pct_invested"]:
                    avg_rows[label][("sys", metric)].append(sys_m[metric])
            if bh_m is not None:
                for metric in ["cagr", "vol", "sharpe", "maxdd", "trades_per_yr", "pct_invested"]:
                    avg_rows[label][("bh", metric)].append(bh_m[metric])
            if sys_m is not None and bh_m is not None and not math.isnan(sys_m["sharpe"]) and not math.isnan(bh_m["sharpe"]):
                n_valid[label] += 1
                if sys_m["sharpe"] > bh_m["sharpe"]:
                    n_beats[label] += 1
    print("-" * len(colhdr))
    for label in ["full", "pre", "post"]:
        def avgm(key):
            d = {}
            for metric in ["cagr", "vol", "sharpe", "maxdd", "trades_per_yr", "pct_invested"]:
                vals = [v for v in avg_rows[label][(key, metric)] if not (isinstance(v, float) and math.isnan(v))]
                d[metric] = mean(vals) if vals else float("nan")
            return d
        sys_avg, bh_avg = avgm("sys"), avgm("bh")
        print(f"{'AVG14':6s}{label:6s}| {fmt_row(sys_avg)} | {fmt_row(bh_avg)}")
    print()
    print(f"SPY (separate):")
    for label in ["full", "pre", "post"]:
        run = spy_run
        sys_m, bh_m = run[label]["sys"], run[label]["bh"]
        print(f"{'SPY':6s}{label:6s}| {fmt_row(sys_m)} | {fmt_row(bh_m)}")
    print()
    print(f"Symbols (of 14) where system Sharpe > buy-and-hold Sharpe: "
          f"full={n_beats['full']}/{n_valid['full']}  pre={n_beats['pre']}/{n_valid['pre']}  post={n_beats['post']}/{n_valid['post']}")
    print()
    return n_beats, n_valid


# -----------------------------------------------------------------------
# main
# -----------------------------------------------------------------------

def main():
    series, (vix_dates, vix_vals) = load_data()

    all_symbols = ALL_STOCKS_14 + [SPY]
    indicators = {}
    for sym in all_symbols:
        indicators[sym] = Indicators(series[sym])

    per_symbol_signals = {}
    for sym in all_symbols:
        per_symbol_signals[sym] = detect_signals(series[sym], indicators[sym])

    print("=" * 110)
    print("CHART INDICATORS (PRICE) -- RAW TEST OUTPUT")
    print("=" * 110)
    print(f"Universe: {len(ALL_STOCKS_14)} large caps (pooled) = {ALL_STOCKS_14}")
    print(f"SPY reported separately. Date range: {series['AAPL']['dates'][0]} to {series['AAPL']['dates'][-1]}")
    print(f"Split date for sub-samples: before {SPLIT_DATE} vs on/after {SPLIT_DATE}")
    print(f"Horizons (trading days): {HORIZONS}")
    print(f"Dedup window: {DEDUP_WINDOW} trading days")
    print()

    print("#" * 110)
    print("TEST 1: EVENT STUDY")
    print("#" * 110)

    print("-" * 110)
    print("MAIN RESULTS: 14-STOCK POOL")
    print("-" * 110)
    results_14, sig_signals_14 = analyze_group(series, ALL_STOCKS_14, per_symbol_signals)
    n_tests_main = len(SIGNAL_ORDER) * len(HORIZONS)

    header = f"{'signal':26s} {'h':>3s} {'n':>6s} {'diff_pp':>9s} {'t':>7s} {'pre_pp':>9s} {'post_pp':>9s} {'sign_adj_pp':>12s} {'dir':>4s}"
    print(header)
    print("-" * len(header))
    for name in SIGNAL_ORDER:
        for h in HORIZONS:
            r = results_14[name][h]
            print(f"{name:26s} {h:>3d} {r['n']:>6d} {fmt(r['diff_pp']):>9s} {fmt(r['t'],2):>7s} "
                  f"{fmt(r['diff_pre_pp']):>9s} {fmt(r['diff_post_pp']):>9s} {fmt(r['sign_adj_pp']):>12s} {DIRECTION[name]:>4s}")
    print()

    print("-" * 110)
    print("SPY (reported separately, same definitions, n will be small)")
    print("-" * 110)
    results_spy, sig_signals_spy = analyze_group(series, [SPY], per_symbol_signals)
    print(header)
    print("-" * len(header))
    for name in SIGNAL_ORDER:
        for h in HORIZONS:
            r = results_spy[name][h]
            print(f"{name:26s} {h:>3d} {r['n']:>6d} {fmt(r['diff_pp']):>9s} {fmt(r['t'],2):>7s} "
                  f"{fmt(r['diff_pre_pp']):>9s} {fmt(r['diff_post_pp']):>9s} {fmt(r['sign_adj_pp']):>12s} {DIRECTION[name]:>4s}")
    print()

    print("-" * 110)
    print("VIX-REGIME CUTS (14-stock pool; regime = most recent WEEKLY VIX close on/before the signal day)")
    print("-" * 110)
    n_tests_vix = 0
    for sig_name in ["rsi_cross_below_30", "bb_close_below_lower"]:
        print(f"  -- {sig_name} --")
        vix_regime = analyze_vix_regime(series, ALL_STOCKS_14, per_symbol_signals, sig_name, vix_dates, vix_vals)
        rheader = f"{'regime':10s} {'h':>3s} {'n':>6s} {'diff_pp':>9s} {'t':>7s}"
        print(rheader)
        print("-" * len(rheader))
        for regime in ["lt20", "20to25", "gte25"]:
            for h in HORIZONS:
                r = vix_regime[regime][h]
                print(f"{regime:10s} {h:>3d} {r['n']:>6d} {fmt(r['diff_pp']):>9s} {fmt(r['t'],2):>7s}")
                n_tests_vix += 1
        print(f"  (total signal days by regime -- lt20: {vix_regime['lt20']['n']}, "
              f"20to25: {vix_regime['20to25']['n']}, gte25: {vix_regime['gte25']['n']})")
        print()

    total_all_tests = n_tests_main + n_tests_vix
    print("-" * 110)
    print("MULTIPLE TESTING")
    print("-" * 110)
    print(f"Primary pre-registered family: {len(SIGNAL_ORDER)} signals x {len(HORIZONS)} horizons = {n_tests_main} tests "
          f"(14-stock pool, full sample).")
    print(f"VIX-regime cuts add {n_tests_vix} more tests (2 signals x 3 regimes x {len(HORIZONS)} horizons) -- secondary, not "
          f"in the primary Bonferroni family.")
    print(f"Grand total tests run in this script (excluding the separately-reported SPY table and the pre/post split "
          f"columns, which are diagnostic, not independently thresholded): {total_all_tests}")
    for n_tests, label in [(n_tests_main, "primary (signal x horizon)"), (total_all_tests, "primary + VIX-regime")]:
        crit = bonferroni_t(n_tests)
        print(f"  Bonferroni alpha=0.05/{n_tests} -> two-tailed critical |t| ~= {crit:.3f}")
    print()

    crit_main = bonferroni_t(n_tests_main)
    print("-" * 110)
    print(f"SURVIVORS: full-sample |t| exceeds the primary Bonferroni threshold ({crit_main:.3f}) "
          "AND both half-sample diffs share the predicted sign")
    print("-" * 110)
    any_survivor = False
    for name in SIGNAL_ORDER:
        expected_sign = 1 if DIRECTION[name] == "BULL" else -1
        for h in HORIZONS:
            r = results_14[name][h]
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

    print("-" * 110)
    print("SIGNAL COUNTS (raw, after dedup) -- 14-stock pool")
    print("-" * 110)
    for name in SIGNAL_ORDER:
        total_n = sum(len(per_symbol_signals[s][name]) for s in ALL_STOCKS_14)
        print(f"  {name:26s} n={total_n}")
    print()

    print("#" * 110)
    print("TEST 2: TRADING SYSTEMS")
    print("#" * 110)
    print(f"Cost: {COST_PER_SIDE*100:.2f}% per side, applied on every position-change day. Cash earns 0.")
    print()

    all_beats = {}
    for system in ["macd", "sma50", "sma200", "ema9", "rsi", "bollinger"]:
        per_symbol_runs = {}
        for sym in ALL_STOCKS_14:
            per_symbol_runs[sym] = run_system_for_symbol(series[sym], indicators[sym], system)
        spy_run = run_system_for_symbol(series[SPY], indicators[SPY], system)
        n_beats, n_valid = print_system_table(system, per_symbol_runs, spy_run)
        all_beats[system] = (n_beats, n_valid)

    print("-" * 110)
    print("SUMMARY: symbols (of 14) beating buy-and-hold on Sharpe, by system and period")
    print("-" * 110)
    for system, (n_beats, n_valid) in all_beats.items():
        print(f"  {system:10s} full={n_beats['full']}/{n_valid['full']}  pre={n_beats['pre']}/{n_valid['pre']}  post={n_beats['post']}/{n_valid['post']}")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
