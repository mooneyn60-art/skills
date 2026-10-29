"""
Volume and VWAP: mechanical, pre-registered signal test.

RESEARCH_AGENDA item (chart indicators, part 2). Predictions were written and
committed BEFORE this script was run
(research/2026-09-24_INDICATORS_VOLUME_VWAP.md, commit 9f0f731). This script
implements the test described there. It prints raw numbers only -- no
conclusions are hardcoded here; the verdict is written into the note by hand
after reading this output.

Universe (P1/P2/P4, daily): 14 large caps (AAPL AMZN BAC C CSCO F GE GOOGL
IBM MSFT NVDA PFE T XOM), pooled, plus SPY reported separately (descriptive
only, small n, not part of the primary Bonferroni family) -- same convention
as paper/research_scripts/candlesticks.py. Daily OHLCV, 2006-01-03 to
2026-09-23 (paper/history/daily_ohlcv.json, pulled fresh via Robinhood
get_equity_historicals). Weekly VIX closes (paper/history/vix_weekly.json)
used for the P4 VIX-regime split.

Universe (P3, intraday): SPY AAPL NVDA INTC SOFI, 5-minute bars, regular
session, 2026-02-23 to 2026-09-24 (paper/history/intraday_vwap_sample.json).
Robinhood's intraday history for 5-minute (and 30-minute, checked directly)
bars only returns real data back to ~2026-02-23; everything requested before
that came back with interpolated=true on every bar and was dropped. So the
intraday window actually used is ~7 months, not the ~12 months targeted.

-----------------------------------------------------------------------------
SIGNAL DEFINITIONS (mechanical, written before looking at any results)
-----------------------------------------------------------------------------

Per-day: avgvol20[i] = mean(V[i-20:i]) (prior 20 trading days, EXCLUDING day
i). Requires i >= 20.

P1 VOLUME SPIKE: V[i] >= 2 * avgvol20[i]. Split by day direction:
  - volspike_up:   spike AND C[i] > O[i]
  - volspike_down: spike AND C[i] < O[i]

P2 VOLUME-CONFIRMED BREAKOUT: 60-day breakout, same definition as the
candlestick script: C[i] > max(H[i-60:i]) (prior 60 trading days, excluding
day i; requires i >= 60, which also covers the i >= 20 needed for avgvol20).
Split by volume:
  - breakout_highvol: breakout AND V[i] >= 1.5 * avgvol20[i]
  - breakout_lowvol:  breakout AND V[i] <  1.0 * avgvol20[i]
Also: a direct two-sample test of breakout_highvol's forward returns vs
breakout_lowvol's forward returns (the "difference" the prediction asks for).

P4 HEAVY-VOLUME SELLOFF: (C[i]/C[i-1] - 1) <= -0.02 AND V[i] >= 2*avgvol20[i]
(requires i >= 20). Split by VIX regime at the signal day (most recent
weekly VIX close on/before the signal date): <20, 20-25, >=25.

OBV DIVERGENCE (exploratory, not in the primary Bonferroni family): OBV[i] =
OBV[i-1] + V[i] if C[i]>C[i-1], OBV[i-1]-V[i] if C[i]<C[i-1], else
OBV[i-1] (OBV[0]=0). Using prior 60 days, excluding day i:
  - obv_bullish_divergence: OBV[i] > max(OBV[i-60:i]) (OBV new 60d high) AND
    NOT C[i] > max(C[i-60:i]) (price did NOT make a new 60d closing high)
  - obv_bearish_divergence: OBV[i] < min(OBV[i-60:i]) (OBV new 60d low) AND
    NOT C[i] < min(C[i-60:i]) (price did NOT make a new 60d closing low)

P3 VWAP (intraday sample): for each symbol-day, typical price tp = (H+L+C)/3
per 5-minute bar; day_vwap = sum(tp*V) / sum(V) over that day's bars.
day_close = last bar's close. day_high/day_low = max/min over the day's
bars. Signals:
  - vwap_above: day_close > day_vwap
  - vwap_below: day_close < day_vwap
  - distance_pct = (day_close - day_vwap) / day_vwap * 100 (continuous)
Forward: next trading day's close-to-close return (h=1) and the return 5
trading days later (h=5), using the intraday-derived daily closes (kept
self-consistent within this sub-analysis rather than joined to the separate
daily_ohlcv.json).
Reversion check: for vwap_above days, did the NEXT trading day's low dip
back down to (or below) today's VWAP level? For vwap_below days, did the
next day's high rise back up to (or above) today's VWAP level? Reported as a
touch rate compared against a flat 50% null (an uninformed "yes/no" split)
via a normal-approximation proportion test.

Dedup (P1, P2, P4, OBV only -- NOT P3, which is a daily state, not a rare
event): for each (symbol, subtype) only the FIRST day of a run counts; once
a signal fires, the next 4 trading days are skipped even if the condition
still holds (5-trading-day window), matching the candlestick script.

-----------------------------------------------------------------------------
MEASUREMENT
-----------------------------------------------------------------------------
Forward return at horizon h (5, 10, 21 trading days for P1/P2/P4/OBV; 1, 5
trading days for P3) from a signal day's close: C[i+h]/C[i] - 1.

Baseline (P1/P2/P4/OBV; per symbol group, per horizon) = mean forward return
over ALL days in that group with a computable forward return (i.e. every
day, not just signal days), same convention as the candlestick script.
Baseline (P3) = mean forward return over all symbol-days in the intraday
sample with a computable forward return.

t-stat = Welch's two-sample t-test comparing the signal-day forward-return
sample against the baseline sample (or, for the P2 difference test and the
P3 above-vs-below test, against each other directly).

Split-sample: pre/post 2016-06-01 for P1/P2/P4/OBV (daily history spans
2006-2026, matching the candlestick script); first half vs second half of
the intraday window (chronological midpoint date) for P3.
"""

import json
import math
from pathlib import Path
from statistics import mean, stdev

REPO = Path(__file__).resolve().parents[2]
DAILY_PATH = REPO / "paper" / "history" / "daily_ohlcv.json"
VIX_PATH = REPO / "paper" / "history" / "vix_weekly.json"
INTRADAY_PATH = REPO / "paper" / "history" / "intraday_vwap_sample.json"

SPLIT_DATE = "2016-06-01"
HORIZONS = [5, 10, 21]
P3_HORIZONS = [1, 5]
DEDUP_WINDOW = 5

ALL_STOCKS_14 = ["AAPL", "AMZN", "BAC", "C", "CSCO", "F", "GE", "GOOGL", "IBM", "MSFT", "NVDA", "PFE", "T", "XOM"]
SPY = "SPY"
INTRADAY_SYMBOLS = ["SPY", "AAPL", "NVDA", "INTC", "SOFI"]


# -----------------------------------------------------------------------------
# Loading
# -----------------------------------------------------------------------------

def load_daily():
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


# -----------------------------------------------------------------------------
# Shared stats helpers
# -----------------------------------------------------------------------------

def welch_t(sample, baseline):
    n1, n2 = len(sample), len(baseline)
    if n1 < 2 or n2 < 2:
        return float("nan"), float("nan")
    m1, m2 = mean(sample), mean(baseline)
    v1, v2 = stdev(sample) ** 2, stdev(baseline) ** 2
    se = math.sqrt(v1 / n1 + v2 / n2)
    if se == 0:
        return float("nan"), m1 - m2
    t = (m1 - m2) / se
    return t, m1 - m2


def pearson_r_t(xs, ys):
    n = len(xs)
    if n < 3:
        return float("nan"), float("nan"), n
    mx, my = mean(xs), mean(ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return float("nan"), float("nan"), n
    r = sxy / math.sqrt(sxx * syy)
    denom = 1 - r * r
    if denom <= 0:
        return r, float("nan"), n
    t = r * math.sqrt(n - 2) / math.sqrt(denom)
    return r, t, n


def prop_z(successes, n, p0=0.5):
    if n == 0:
        return float("nan"), float("nan")
    p_hat = successes / n
    se = math.sqrt(p0 * (1 - p0) / n)
    if se == 0:
        return p_hat, float("nan")
    z = (p_hat - p0) / se
    return p_hat, z


def fmt(x, nd=3):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "NA"
    return f"{x:.{nd}f}"


def bonferroni_t(n_tests, alpha=0.05):
    try:
        from scipy.stats import norm
        adj_alpha = alpha / n_tests
        return norm.ppf(1 - adj_alpha / 2)
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


def dedup(days):
    kept = []
    last = -10 ** 9
    for d in days:
        if d - last >= DEDUP_WINDOW:
            kept.append(d)
        last = d
    return kept


# -----------------------------------------------------------------------------
# Detection: P1, P2, P4, OBV
# -----------------------------------------------------------------------------

def detect_signals(bars, vix_dates, vix_vals):
    O, H, L, C, V = bars["O"], bars["H"], bars["L"], bars["C"], bars["V"]
    dates = bars["dates"]
    n = len(C)

    raw = {
        "volspike_up": [], "volspike_down": [],
        "breakout_highvol": [], "breakout_lowvol": [],
        "down2pct_heavyvol": [],
        "obv_bull_div": [], "obv_bear_div": [],
    }

    # OBV
    obv = [0.0] * n
    for i in range(1, n):
        if C[i] > C[i - 1]:
            obv[i] = obv[i - 1] + V[i]
        elif C[i] < C[i - 1]:
            obv[i] = obv[i - 1] - V[i]
        else:
            obv[i] = obv[i - 1]

    for i in range(n):
        if i >= 20:
            avgvol20 = mean(V[i - 20:i])
        else:
            avgvol20 = None

        if avgvol20 is not None and avgvol20 > 0:
            spike = V[i] >= 2 * avgvol20
            if spike:
                if C[i] > O[i]:
                    raw["volspike_up"].append(i)
                elif C[i] < O[i]:
                    raw["volspike_down"].append(i)

            if i >= 60:
                prior_high_60 = max(H[i - 60:i])
                breakout = C[i] > prior_high_60
                if breakout:
                    if V[i] >= 1.5 * avgvol20:
                        raw["breakout_highvol"].append(i)
                    elif V[i] < 1.0 * avgvol20:
                        raw["breakout_lowvol"].append(i)

            if i >= 1:
                day_ret = C[i] / C[i - 1] - 1.0
                if day_ret <= -0.02 and V[i] >= 2 * avgvol20:
                    raw["down2pct_heavyvol"].append(i)

        if i >= 60:
            obv_prior = obv[i - 60:i]
            c_prior = C[i - 60:i]
            obv_new_high = obv[i] > max(obv_prior)
            obv_new_low = obv[i] < min(obv_prior)
            price_new_high = C[i] > max(c_prior)
            price_new_low = C[i] < min(c_prior)
            if obv_new_high and not price_new_high:
                raw["obv_bull_div"].append(i)
            if obv_new_low and not price_new_low:
                raw["obv_bear_div"].append(i)

    return {name: dedup(days) for name, days in raw.items()}


def forward_returns_all_days(bars, horizon):
    C = bars["C"]
    n = len(C)
    return [C[i + horizon] / C[i] - 1.0 for i in range(n - horizon)]


def build_baseline(series, symbols):
    baseline = {h: [] for h in HORIZONS}
    baseline_half = {h: {"pre": [], "post": []} for h in HORIZONS}
    for sym in symbols:
        bars = series[sym]
        dates = bars["dates"]
        C = bars["C"]
        n = len(C)
        for h in HORIZONS:
            for i in range(n - h):
                fr = C[i + h] / C[i] - 1.0
                baseline[h].append(fr)
                half = "pre" if dates[i] < SPLIT_DATE else "post"
                baseline_half[h][half].append(fr)
    return baseline, baseline_half


def signal_stats(series, symbols, signal_name, per_symbol_signals, baseline, baseline_half):
    out = {}
    for h in HORIZONS:
        sample, sample_pre, sample_post = [], [], []
        for sym in symbols:
            bars = series[sym]
            C = bars["C"]
            dates = bars["dates"]
            n = len(C)
            for d in per_symbol_signals[sym][signal_name]:
                if d + h < n:
                    fr = C[d + h] / C[d] - 1.0
                    sample.append(fr)
                    if dates[d] < SPLIT_DATE:
                        sample_pre.append(fr)
                    else:
                        sample_post.append(fr)
        t, diff = welch_t(sample, baseline[h]) if len(sample) >= 2 else (float("nan"), float("nan"))
        diff_pp = diff * 100 if not math.isnan(diff) else float("nan")
        base_pre, base_post = baseline_half[h]["pre"], baseline_half[h]["post"]
        diff_pre_pp = (mean(sample_pre) - mean(base_pre)) * 100 if len(sample_pre) >= 2 and base_pre else float("nan")
        diff_post_pp = (mean(sample_post) - mean(base_post)) * 100 if len(sample_post) >= 2 and base_post else float("nan")
        out[h] = {"n": len(sample), "n_pre": len(sample_pre), "n_post": len(sample_post),
                   "diff_pp": diff_pp, "t": t, "diff_pre_pp": diff_pre_pp, "diff_post_pp": diff_post_pp,
                   "sample": sample}
    return out


def two_sample_diff(series, symbols, sig_a_lists, sig_b_lists, h):
    a, b = [], []
    for sym in symbols:
        bars = series[sym]
        C = bars["C"]
        n = len(C)
        for d in sig_a_lists[sym]:
            if d + h < n:
                a.append(C[d + h] / C[d] - 1.0)
        for d in sig_b_lists[sym]:
            if d + h < n:
                b.append(C[d + h] / C[d] - 1.0)
    if len(a) >= 2 and len(b) >= 2:
        t, diff = welch_t(a, b)
    else:
        t, diff = float("nan"), float("nan")
    return {"n_a": len(a), "n_b": len(b), "diff_pp": diff * 100 if not math.isnan(diff) else float("nan"), "t": t}


# -----------------------------------------------------------------------------
# P3: VWAP (intraday)
# -----------------------------------------------------------------------------

def load_intraday():
    raw = json.loads(INTRADAY_PATH.read_text())
    days_by_symbol = {}
    for sym, dmap in raw.items():
        days = []
        for date in sorted(dmap.keys()):
            bars = dmap[date]  # list of [ts, o, h, l, c, v]
            if not bars:
                continue
            num = sum(((b[2] + b[3] + b[4]) / 3.0) * b[5] for b in bars)
            den = sum(b[5] for b in bars)
            if den <= 0:
                continue
            day_vwap = num / den
            day_close = bars[-1][4]
            day_high = max(b[2] for b in bars)
            day_low = min(b[3] for b in bars)
            days.append({"date": date, "vwap": day_vwap, "close": day_close,
                         "high": day_high, "low": day_low})
        days_by_symbol[sym] = days
    return days_by_symbol


def p3_vwap_analysis(days_by_symbol):
    all_dates = sorted({d["date"] for days in days_by_symbol.values() for d in days})
    mid = all_dates[len(all_dates) // 2]

    baseline = {h: [] for h in P3_HORIZONS}
    baseline_half = {h: {"first": [], "second": []} for h in P3_HORIZONS}
    per_symbol_group = {h: {"above": [], "below": []} for h in P3_HORIZONS}
    per_symbol_group_half = {h: {"above": {"first": [], "second": []}, "below": {"first": [], "second": []}}
                              for h in P3_HORIZONS}
    dist_pairs = {h: [] for h in P3_HORIZONS}
    touch_above = [0, 0]  # successes, n
    touch_below = [0, 0]

    for sym, days in days_by_symbol.items():
        n = len(days)
        closes = [d["close"] for d in days]
        for i in range(n):
            for h in P3_HORIZONS:
                if i + h < n:
                    fr = closes[i + h] / closes[i] - 1.0
                    baseline[h].append(fr)
                    half = "first" if days[i]["date"] < mid else "second"
                    baseline_half[h][half].append(fr)
                    above = days[i]["close"] > days[i]["vwap"]
                    below = days[i]["close"] < days[i]["vwap"]
                    if above:
                        per_symbol_group[h]["above"].append(fr)
                        per_symbol_group_half[h]["above"][half].append(fr)
                    elif below:
                        per_symbol_group[h]["below"].append(fr)
                        per_symbol_group_half[h]["below"][half].append(fr)
                    dist_pct = (days[i]["close"] - days[i]["vwap"]) / days[i]["vwap"] * 100.0
                    dist_pairs[h].append((dist_pct, fr))
            # reversion check (next trading day only)
            if i + 1 < n:
                vwap_today = days[i]["vwap"]
                nxt = days[i + 1]
                if days[i]["close"] > vwap_today:
                    touch_above[1] += 1
                    if nxt["low"] <= vwap_today:
                        touch_above[0] += 1
                elif days[i]["close"] < vwap_today:
                    touch_below[1] += 1
                    if nxt["high"] >= vwap_today:
                        touch_below[0] += 1

    group_stats = {}
    for h in P3_HORIZONS:
        group_stats[h] = {}
        for g in ("above", "below"):
            sample = per_symbol_group[h][g]
            t, diff = welch_t(sample, baseline[h]) if len(sample) >= 2 else (float("nan"), float("nan"))
            first = per_symbol_group_half[h][g]["first"]
            second = per_symbol_group_half[h][g]["second"]
            base_first, base_second = baseline_half[h]["first"], baseline_half[h]["second"]
            diff_first = (mean(first) - mean(base_first)) * 100 if len(first) >= 2 and base_first else float("nan")
            diff_second = (mean(second) - mean(base_second)) * 100 if len(second) >= 2 and base_second else float("nan")
            group_stats[h][g] = {"n": len(sample), "diff_pp": diff * 100 if not math.isnan(diff) else float("nan"),
                                  "t": t, "diff_first_pp": diff_first, "diff_second_pp": diff_second}
        # above vs below direct comparison
        a, b = per_symbol_group[h]["above"], per_symbol_group[h]["below"]
        if len(a) >= 2 and len(b) >= 2:
            t_ab, diff_ab = welch_t(a, b)
        else:
            t_ab, diff_ab = float("nan"), float("nan")
        group_stats[h]["above_vs_below"] = {"diff_pp": diff_ab * 100 if not math.isnan(diff_ab) else float("nan"),
                                             "t": t_ab}

    corr_stats = {}
    for h in P3_HORIZONS:
        xs = [p[0] for p in dist_pairs[h]]
        ys = [p[1] for p in dist_pairs[h]]
        r, t, n = pearson_r_t(xs, ys)
        corr_stats[h] = {"r": r, "t": t, "n": n}

    p_above, z_above = prop_z(touch_above[0], touch_above[1])
    p_below, z_below = prop_z(touch_below[0], touch_below[1])

    return {
        "mid_date": mid, "all_dates_n": len(all_dates),
        "group_stats": group_stats, "corr_stats": corr_stats,
        "reversion": {
            "above": {"touched": touch_above[0], "n": touch_above[1], "rate": p_above, "z": z_above},
            "below": {"touched": touch_below[0], "n": touch_below[1], "rate": p_below, "z": z_below},
        },
    }


# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------

def main():
    series, (vix_dates, vix_vals) = load_daily()

    print("=" * 100)
    print("VOLUME AND VWAP -- RAW TEST OUTPUT")
    print("=" * 100)
    print(f"Daily universe: {len(ALL_STOCKS_14)} large caps (pooled) = {ALL_STOCKS_14}")
    print(f"SPY reported separately (descriptive, small n). Date range: "
          f"{series['AAPL']['dates'][0]} to {series['AAPL']['dates'][-1]}")
    print(f"Split date for daily sub-samples: before {SPLIT_DATE} vs on/after {SPLIT_DATE}")
    print(f"Horizons (trading days), P1/P2/P4: {HORIZONS}")
    print(f"Dedup window (P1/P2/P4/OBV): {DEDUP_WINDOW} trading days per symbol+signal")
    print()

    per_symbol_signals_14 = {sym: detect_signals(series[sym], vix_dates, vix_vals) for sym in ALL_STOCKS_14}
    per_symbol_signals_spy = {SPY: detect_signals(series[SPY], vix_dates, vix_vals)}
    baseline_14, baseline_half_14 = build_baseline(series, ALL_STOCKS_14)
    baseline_spy, baseline_half_spy = build_baseline(series, [SPY])

    test_records = []  # (label, t, expected_sign(+1/-1/None), diff_pre_pp, diff_post_pp)

    print("-" * 100)
    print("P1: VOLUME SPIKE (V >= 2x 20-day avg vol), split by day direction -- 14-stock pool")
    print("-" * 100)
    header = f"{'signal':22s} {'h':>3s} {'n':>6s} {'diff_pp':>9s} {'t':>7s} {'pre_pp':>9s} {'post_pp':>9s}"
    print(header)
    print("-" * len(header))
    for sig_name, exp_sign in [("volspike_up", +1), ("volspike_down", +1)]:
        stats = signal_stats(series, ALL_STOCKS_14, sig_name, per_symbol_signals_14, baseline_14, baseline_half_14)
        for h in HORIZONS:
            r = stats[h]
            print(f"{sig_name:22s} {h:>3d} {r['n']:>6d} {fmt(r['diff_pp']):>9s} {fmt(r['t'],2):>7s} "
                  f"{fmt(r['diff_pre_pp']):>9s} {fmt(r['diff_post_pp']):>9s}")
            test_records.append((f"P1:{sig_name} h={h}", r["t"], exp_sign, r["diff_pre_pp"], r["diff_post_pp"]))
    print()

    print("-" * 100)
    print("P2: 60-DAY BREAKOUT split by volume confirmation -- 14-stock pool")
    print("-" * 100)
    print(header)
    print("-" * len(header))
    for sig_name, exp_sign in [("breakout_highvol", +1), ("breakout_lowvol", +1)]:
        stats = signal_stats(series, ALL_STOCKS_14, sig_name, per_symbol_signals_14, baseline_14, baseline_half_14)
        for h in HORIZONS:
            r = stats[h]
            print(f"{sig_name:22s} {h:>3d} {r['n']:>6d} {fmt(r['diff_pp']):>9s} {fmt(r['t'],2):>7s} "
                  f"{fmt(r['diff_pre_pp']):>9s} {fmt(r['diff_post_pp']):>9s}")
            test_records.append((f"P2:{sig_name} h={h}", r["t"], exp_sign, r["diff_pre_pp"], r["diff_post_pp"]))
    print()
    print("P2 DIFFERENCE: breakout_highvol forward returns vs breakout_lowvol forward returns (direct)")
    dheader = f"{'h':>3s} {'n_hi':>6s} {'n_lo':>6s} {'diff_pp(hi-lo)':>15s} {'t':>7s}"
    print(dheader)
    print("-" * len(dheader))
    sig_a_lists = {sym: per_symbol_signals_14[sym]["breakout_highvol"] for sym in ALL_STOCKS_14}
    sig_b_lists = {sym: per_symbol_signals_14[sym]["breakout_lowvol"] for sym in ALL_STOCKS_14}
    for h in HORIZONS:
        d = two_sample_diff(series, ALL_STOCKS_14, sig_a_lists, sig_b_lists, h)
        print(f"{h:>3d} {d['n_a']:>6d} {d['n_b']:>6d} {fmt(d['diff_pp']):>15s} {fmt(d['t'],2):>7s}")
        # no pre/post half check for this direct-difference test; still add to family with no sign expectation
        test_records.append((f"P2:diff_hi_lo h={h}", d["t"], None, float("nan"), float("nan")))
    print()

    print("-" * 100)
    print("P4: DOWN DAY >= -2% on volume >= 2x 20-day avg, split by VIX regime -- 14-stock pool")
    print("VIX regime = most recent WEEKLY VIX close on/before the signal day")
    print("-" * 100)
    regimes = {"lt20": {}, "20to25": {}, "gte25": {}}
    for sym in ALL_STOCKS_14:
        dates = series[sym]["dates"]
        for d in per_symbol_signals_14[sym]["down2pct_heavyvol"]:
            v = vix_asof(vix_dates, vix_vals, dates[d])
            if v is None:
                continue
            regime = "lt20" if v < 20 else ("20to25" if v < 25 else "gte25")
            regimes[regime].setdefault(sym, []).append(d)
    rheader = f"{'regime':10s} {'h':>3s} {'n':>6s} {'diff_pp':>9s} {'t':>7s} {'pre_pp':>9s} {'post_pp':>9s}"
    print(rheader)
    print("-" * len(rheader))
    for regime in ["lt20", "20to25", "gte25"]:
        per_sym = {sym: regimes[regime].get(sym, []) for sym in ALL_STOCKS_14}
        stats = signal_stats(series, ALL_STOCKS_14, "_tmp", {sym: {"_tmp": per_sym[sym]} for sym in ALL_STOCKS_14},
                              baseline_14, baseline_half_14)
        for h in HORIZONS:
            r = stats[h]
            print(f"{regime:10s} {h:>3d} {r['n']:>6d} {fmt(r['diff_pp']):>9s} {fmt(r['t'],2):>7s} "
                  f"{fmt(r['diff_pre_pp']):>9s} {fmt(r['diff_post_pp']):>9s}")
            # predicted sign: negative (below baseline) in calm markets, positive (above baseline) when stressed
            exp_sign = -1 if regime == "lt20" else (+1 if regime == "gte25" else None)
            test_records.append((f"P4:{regime} h={h}", r["t"], exp_sign, r["diff_pre_pp"], r["diff_post_pp"]))
    print(f"(total signal days by regime -- lt20: {sum(len(v) for v in regimes['lt20'].values())}, "
          f"20to25: {sum(len(v) for v in regimes['20to25'].values())}, "
          f"gte25: {sum(len(v) for v in regimes['gte25'].values())})")
    print()

    print("-" * 100)
    print("SPY (reported separately, same definitions, n will be small) -- descriptive only, not in Bonferroni family")
    print("-" * 100)
    print(header)
    print("-" * len(header))
    for sig_name in ["volspike_up", "volspike_down", "breakout_highvol", "breakout_lowvol"]:
        stats = signal_stats(series, [SPY], sig_name, per_symbol_signals_spy, baseline_spy, baseline_half_spy)
        for h in HORIZONS:
            r = stats[h]
            print(f"{sig_name:22s} {h:>3d} {r['n']:>6d} {fmt(r['diff_pp']):>9s} {fmt(r['t'],2):>7s} "
                  f"{fmt(r['diff_pre_pp']):>9s} {fmt(r['diff_post_pp']):>9s}")
    print()

    print("-" * 100)
    print("OBV DIVERGENCE (EXPLORATORY -- not in the primary Bonferroni family) -- 14-stock pool")
    print("-" * 100)
    print(header)
    print("-" * len(header))
    obv_records = []
    for sig_name, exp_sign in [("obv_bull_div", +1), ("obv_bear_div", -1)]:
        stats = signal_stats(series, ALL_STOCKS_14, sig_name, per_symbol_signals_14, baseline_14, baseline_half_14)
        for h in HORIZONS:
            r = stats[h]
            print(f"{sig_name:22s} {h:>3d} {r['n']:>6d} {fmt(r['diff_pp']):>9s} {fmt(r['t'],2):>7s} "
                  f"{fmt(r['diff_pre_pp']):>9s} {fmt(r['diff_post_pp']):>9s}")
            obv_records.append((f"OBV:{sig_name} h={h}", r["t"], exp_sign, r["diff_pre_pp"], r["diff_post_pp"]))
    print()

    # ---------------------- P3 VWAP ----------------------
    print("-" * 100)
    print("P3: VWAP (intraday sample) -- SPY AAPL NVDA INTC SOFI")
    print("-" * 100)
    days_by_symbol = load_intraday()
    for sym in INTRADAY_SYMBOLS:
        d0, d1 = days_by_symbol[sym][0]["date"], days_by_symbol[sym][-1]["date"]
        print(f"  {sym}: {len(days_by_symbol[sym])} trading days, {d0} to {d1}")
    p3 = p3_vwap_analysis(days_by_symbol)
    print(f"Chronological midpoint date for first/second half split: {p3['mid_date']} "
          f"(total distinct trading days: {p3['all_dates_n']})")
    print()
    print("Close above VWAP vs close below VWAP -- forward close-to-close return vs all-symbol-day baseline")
    p3header = f"{'group':14s} {'h':>3s} {'n':>6s} {'diff_pp':>9s} {'t':>7s} {'1sthalf_pp':>11s} {'2ndhalf_pp':>11s}"
    print(p3header)
    print("-" * len(p3header))
    for h in P3_HORIZONS:
        for g in ("above", "below"):
            r = p3["group_stats"][h][g]
            print(f"{g:14s} {h:>3d} {r['n']:>6d} {fmt(r['diff_pp']):>9s} {fmt(r['t'],2):>7s} "
                  f"{fmt(r['diff_first_pp']):>11s} {fmt(r['diff_second_pp']):>11s}")
            exp_sign = +1 if g == "above" else -1
            test_records.append((f"P3:{g} h={h}", r["t"], exp_sign, r["diff_first_pp"], r["diff_second_pp"]))
        ab = p3["group_stats"][h]["above_vs_below"]
        print(f"  -> above vs below direct: diff_pp={fmt(ab['diff_pp'])} t={fmt(ab['t'],2)}")
    print()
    print("Distance-from-VWAP (%) vs forward return: Pearson correlation, pooled symbol-days")
    cheader = f"{'h':>3s} {'n':>6s} {'r':>8s} {'t':>7s}"
    print(cheader)
    print("-" * len(cheader))
    for h in P3_HORIZONS:
        c = p3["corr_stats"][h]
        print(f"{h:>3d} {c['n']:>6d} {fmt(c['r'],4):>8s} {fmt(c['t'],2):>7s}")
        test_records.append((f"P3:distance_corr h={h}", c["t"], +1, float("nan"), float("nan")))
    print()
    print("Reversion: does the next day's range touch back to today's VWAP level?")
    print("  (above-VWAP close -> does next day's LOW dip to/below today's VWAP; "
          "below-VWAP close -> does next day's HIGH rise to/above today's VWAP)")
    rev = p3["reversion"]
    for g in ("above", "below"):
        r = rev[g]
        print(f"  {g}: touched {r['touched']}/{r['n']} = {fmt(r['rate'],4)} "
              f"(z vs 50% null = {fmt(r['z'],2)})")
        test_records.append((f"P3:reversion_{g}", r["z"], +1, float("nan"), float("nan")))
    print()

    # ---------------------- Multiple testing ----------------------
    print("-" * 100)
    print("MULTIPLE TESTING")
    print("-" * 100)
    n_primary = len(test_records)
    n_obv = len(obv_records)
    print(f"Primary pre-registered family (P1 + P2 + P2-diff + P4 + P3): {n_primary} tests")
    print(f"OBV divergence (exploratory, reported separately): {n_obv} tests, NOT counted in the primary family")
    crit_primary = bonferroni_t(n_primary)
    crit_obv = bonferroni_t(n_obv)
    print(f"  Bonferroni alpha=0.05/{n_primary} -> two-tailed critical |t| ~= {crit_primary:.3f} (primary family)")
    print(f"  Bonferroni alpha=0.05/{n_obv} -> two-tailed critical |t| ~= {crit_obv:.3f} (OBV, informational only)")
    print()

    print("-" * 100)
    print(f"SURVIVORS (primary family): |t| > {crit_primary:.3f} AND both half-sample diffs share the predicted sign")
    print("(tests with no directional half-split -- P2 diff, P3 correlation/reversion -- listed if |t| clears "
          "the threshold, with half-sign check marked N/A)")
    print("-" * 100)
    any_survivor = False
    for label, t, exp_sign, diff_pre, diff_post in test_records:
        if t is None or (isinstance(t, float) and math.isnan(t)):
            continue
        passes = abs(t) > crit_primary
        if not passes:
            continue
        if exp_sign is None or math.isnan(diff_pre) or math.isnan(diff_post):
            print(f"  SURVIVOR (half-check N/A): {label} t={t:.2f}")
            any_survivor = True
            continue
        pre_ok = diff_pre * exp_sign > 0
        post_ok = diff_post * exp_sign > 0
        if pre_ok and post_ok:
            print(f"  SURVIVOR: {label} t={t:.2f} pre_pp={diff_pre:.3f} post_pp={diff_post:.3f}")
            any_survivor = True
    if not any_survivor:
        print("  none")
    print()

    print("-" * 100)
    print("SIGNAL COUNTS (raw, after dedup where applicable) -- 14-stock pool")
    print("-" * 100)
    for name in ["volspike_up", "volspike_down", "breakout_highvol", "breakout_lowvol",
                 "down2pct_heavyvol", "obv_bull_div", "obv_bear_div"]:
        total_n = sum(len(per_symbol_signals_14[s][name]) for s in ALL_STOCKS_14)
        print(f"  {name:22s} n={total_n}")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
