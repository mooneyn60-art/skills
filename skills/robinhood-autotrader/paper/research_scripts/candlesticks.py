"""
Candlesticks and chart lines: mechanical, pre-registered signal test.

RESEARCH_AGENDA item 23. Predictions were written and committed BEFORE this
script was run (research/2026-09-24_CANDLESTICKS_AND_CHART_LINES.md, commit
060c26f). This script implements the test described there. It prints raw
numbers only -- no conclusions are hardcoded here; the verdict is written
into the note by hand after reading this output.

Universe: 14 large caps (AAPL AMZN BAC C CSCO F GE GOOGL IBM MSFT NVDA PFE T
XOM), pooled, plus SPY reported separately. Daily OHLC, 2006-01-03 to
2026-09-18 (paper/history/daily_stocks.json). Weekly VIX closes
(paper/history/vix_weekly.json) used for the P3 VIX-regime split.

-----------------------------------------------------------------------------
PATTERN DEFINITIONS (mechanical, written before looking at any results)
-----------------------------------------------------------------------------

Per-day quantities: body = |C-O|; rng = H-L (skipped if 0); upper shadow =
H - max(O,C); lower shadow = min(O,C) - L.

Trend context helper: trend_down(day) is true when C[day] < C[day-5]
(net decline over the 5 trading days ending at `day`); trend_up(day) is the
mirror. A pattern's "context day" is the close right before the pattern's
first candle -- i.e. the trend is measured *into* the pattern, not using the
pattern's own candles.

Single-candle (signal day = i):
  - HAMMER: body <= 0.35*rng; lower shadow >= 2*body; upper shadow <=
    0.25*rng; requires trend_down(i-1) (5-day decline into the candle).
  - SHOOTING STAR: body <= 0.35*rng; upper shadow >= 2*body; lower shadow <=
    0.25*rng; requires trend_up(i-1) (5-day rise into the candle).
  - DOJI: body <= 0.10*rng. No directional context required (classic doji is
    a neutral/indecision signal, not a directional one).

Two-candle (signal day = i, prior candle = i-1):
  - BULLISH ENGULFING: candle i-1 bearish (C<O), candle i bullish (C>O),
    and candle i's real body fully engulfs candle i-1's real body
    (O[i] <= C[i-1] and C[i] >= O[i-1]); requires trend_down(i-2) (decline
    into the two-candle formation).
  - BEARISH ENGULFING: mirror (candle i-1 bullish, candle i bearish, body
    engulfs), requires trend_up(i-2).

Three-candle (signal day = i, candles i-2, i-1, i):
  - MORNING STAR: candle i-2 bearish with body >= 0.6*rng[i-2] (a "long"
    black body); candle i-1 has a small body <= 0.3*body[i-2] (the "star");
    candle i is bullish and closes above the midpoint of candle i-2's real
    body. Requires trend_down(i-3) (decline into the formation).
  - EVENING STAR: mirror (long white i-2, small star i-1, bearish i closing
    below the midpoint of i-2's body), requires trend_up(i-3).
  - THREE WHITE SOLDIERS: candles i-2,i-1,i all bullish (C>O); each close
    higher than the prior close; each open within the prior candle's real
    body (O[k] >= O[k-1] and O[k] <= C[k-1]); each has a small upper shadow
    (<= 0.25*rng[k]). No prior-trend context required -- the classic
    (Nison) definition describes the three-candle shape only; this is a
    stated simplification/limitation, not an oversight.
  - THREE BLACK CROWS: mirror (bearish, descending closes, opens inside
    prior body, small lower shadows). No prior-trend context required, same
    caveat as above.

Chart lines (signal day = i, using the prior 60 or 252 trading days,
EXCLUDING day i itself):
  - 60-DAY BREAKOUT: C[i] > max(H[i-60:i]).
  - 252-DAY BREAKOUT: C[i] > max(H[i-252:i]).
  - 60-DAY BREAKDOWN: C[i] < min(L[i-60:i]).
  - SUPPORT BOUNCE: L[i] <= 1.01 * min(L[i-60:i]) (low within 1% of the
    prior 60-day swing low) AND C[i] > O[i] (closed up on the day).

Dedup: for each (symbol, signal) only the FIRST day of a run counts; once a
signal fires, the next 5 trading days for that symbol+signal are skipped
even if the condition still holds.

-----------------------------------------------------------------------------
MEASUREMENT
-----------------------------------------------------------------------------
Forward return at horizon h (5, 10, 21 trading days) from a signal day's
close: C[i+h]/C[i] - 1.

Baseline (per symbol group, per horizon) = mean forward return over ALL days
in that group with a computable forward return (i.e. every day, not just
signal days). Diff = mean(signal fwd ret) - mean(baseline fwd ret), reported
in percentage points (pp). t-stat = Welch's two-sample t-test comparing the
signal-day forward-return sample against the all-day baseline sample.

Sign-adjusted diff: for bearish patterns the predicted edge is a NEGATIVE
diff, so sign-adjusted = -diff for bearish patterns (and doji, which has no
predicted sign, is reported unadjusted and flagged neutral). This lets every
signal's sign-adjusted column read as "positive = pattern behaved as
predicted."
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

BULLISH_PATTERNS = {"hammer", "bullish_engulfing", "morning_star", "three_white_soldiers", "support_bounce",
                     "breakout_60d", "breakout_252d"}
BEARISH_PATTERNS = {"shooting_star", "bearish_engulfing", "evening_star", "three_black_crows", "breakdown_60d"}
NEUTRAL_PATTERNS = {"doji"}

ALL_STOCKS_14 = ["AAPL", "AMZN", "BAC", "C", "CSCO", "F", "GE", "GOOGL", "IBM", "MSFT", "NVDA", "PFE", "T", "XOM"]
SPY = "SPY"


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
    """Most recent weekly VIX close on or before date_str. None if none exists yet."""
    # vix_dates sorted ascending; binary search
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


def trend_down(C, day):
    if day - 5 < 0:
        return False
    return C[day] < C[day - 5]


def trend_up(C, day):
    if day - 5 < 0:
        return False
    return C[day] > C[day - 5]


def detect_patterns(bars):
    """Return dict pattern_name -> sorted list of signal day indices (raw, pre-dedup)."""
    O, H, L, C = bars["O"], bars["H"], bars["L"], bars["C"]
    n = len(C)
    out = {name: [] for name in [
        "hammer", "shooting_star", "doji", "bullish_engulfing", "bearish_engulfing",
        "morning_star", "evening_star", "three_white_soldiers", "three_black_crows",
        "breakout_60d", "breakout_252d", "breakdown_60d", "support_bounce",
    ]}

    for i in range(n):
        rng = H[i] - L[i]
        body = abs(C[i] - O[i])
        upper = H[i] - max(O[i], C[i])
        lower = min(O[i], C[i]) - L[i]

        # --- single-candle ---
        if rng > 0:
            if body <= 0.35 * rng and lower >= 2 * body and upper <= 0.25 * rng and trend_down(C, i - 1):
                out["hammer"].append(i)
            if body <= 0.35 * rng and upper >= 2 * body and lower <= 0.25 * rng and trend_up(C, i - 1):
                out["shooting_star"].append(i)
            if body <= 0.10 * rng:
                out["doji"].append(i)

        # --- two-candle ---
        if i - 1 >= 0:
            prev_bear = C[i - 1] < O[i - 1]
            prev_bull = C[i - 1] > O[i - 1]
            cur_bull = C[i] > O[i]
            cur_bear = C[i] < O[i]
            engulfs = O[i] <= C[i - 1] and C[i] >= O[i - 1]
            engulfs_bear = O[i] >= C[i - 1] and C[i] <= O[i - 1]
            if prev_bear and cur_bull and engulfs and trend_down(C, i - 2):
                out["bullish_engulfing"].append(i)
            if prev_bull and cur_bear and engulfs_bear and trend_up(C, i - 2):
                out["bearish_engulfing"].append(i)

        # --- three-candle ---
        if i - 2 >= 0:
            b0 = abs(C[i - 2] - O[i - 2])
            r0 = H[i - 2] - L[i - 2]
            b1 = abs(C[i - 1] - O[i - 1])
            mid0 = (O[i - 2] + C[i - 2]) / 2.0

            first_bear_long = (C[i - 2] < O[i - 2]) and r0 > 0 and b0 >= 0.6 * r0
            first_bull_long = (C[i - 2] > O[i - 2]) and r0 > 0 and b0 >= 0.6 * r0
            star_small = b1 <= 0.3 * b0 if b0 > 0 else False

            if first_bear_long and star_small and (C[i] > O[i]) and C[i] > mid0 and trend_down(C, i - 3):
                out["morning_star"].append(i)
            if first_bull_long and star_small and (C[i] < O[i]) and C[i] < mid0 and trend_up(C, i - 3):
                out["evening_star"].append(i)

            # three white soldiers / three black crows
            all_bull = C[i - 2] > O[i - 2] and C[i - 1] > O[i - 1] and C[i] > O[i]
            all_bear = C[i - 2] < O[i - 2] and C[i - 1] < O[i - 1] and C[i] < O[i]
            rising_closes = C[i - 1] > C[i - 2] and C[i] > C[i - 1]
            falling_closes = C[i - 1] < C[i - 2] and C[i] < C[i - 1]
            opens_inside_up = (O[i - 1] >= O[i - 2] and O[i - 1] <= C[i - 2] and
                                O[i] >= O[i - 1] and O[i] <= C[i - 1])
            opens_inside_down = (O[i - 1] <= O[i - 2] and O[i - 1] >= C[i - 2] and
                                  O[i] <= O[i - 1] and O[i] >= C[i - 1])
            small_upper_all = all(
                (H[k] - max(O[k], C[k])) <= 0.25 * (H[k] - L[k]) for k in (i - 2, i - 1, i) if H[k] > L[k]
            )
            small_lower_all = all(
                (min(O[k], C[k]) - L[k]) <= 0.25 * (H[k] - L[k]) for k in (i - 2, i - 1, i) if H[k] > L[k]
            )
            if all_bull and rising_closes and opens_inside_up and small_upper_all:
                out["three_white_soldiers"].append(i)
            if all_bear and falling_closes and opens_inside_down and small_lower_all:
                out["three_black_crows"].append(i)

        # --- lines ---
        if i - 60 >= 0:
            prior_high_60 = max(H[i - 60:i])
            prior_low_60 = min(L[i - 60:i])
            if C[i] > prior_high_60:
                out["breakout_60d"].append(i)
            if C[i] < prior_low_60:
                out["breakdown_60d"].append(i)
            if L[i] <= 1.01 * prior_low_60 and C[i] > O[i]:
                out["support_bounce"].append(i)
        if i - 252 >= 0:
            prior_high_252 = max(H[i - 252:i])
            if C[i] > prior_high_252:
                out["breakout_252d"].append(i)

    # dedup: keep only first day of a run; skip next DEDUP_WINDOW-1 days after a hit
    deduped = {}
    for name, days in out.items():
        kept = []
        last = -10 ** 9
        for d in days:
            if d - last >= DEDUP_WINDOW:
                kept.append(d)
            last = d
        deduped[name] = kept
    return deduped


def forward_returns_all_days(bars, horizon):
    C = bars["C"]
    n = len(C)
    return [C[i + horizon] / C[i] - 1.0 for i in range(n - horizon)]


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


def analyze_group(series, symbols, dates_by_symbol, vix_lookup=None):
    """Compute per-pattern, per-horizon signal stats for a pooled symbol group.
    Returns dict[pattern][horizon] -> dict with n, diff_pp, t, first_half_diff_pp,
    second_half_diff_pp, sign_adjusted_pp.
    Also returns raw signal (symbol, day_index, date) lists for the VIX-regime cut.
    """
    all_patterns_signals = {}  # pattern -> list of (sym, day_idx)
    all_days_fwd = {h: [] for h in HORIZONS}  # pooled baseline forward returns per horizon
    all_days_fwd_by_half = {h: {"pre": [], "post": []} for h in HORIZONS}
    sig_fwd_by_half = {}  # pattern -> horizon -> {"pre": [...], "post": [...]}

    per_symbol_patterns = {}
    for sym in symbols:
        bars = series[sym]
        pats = detect_patterns(bars)
        per_symbol_patterns[sym] = pats
        dates = bars["dates"]
        C = bars["C"]
        n = len(C)
        for h in HORIZONS:
            for i in range(n - h):
                fr = C[i + h] / C[i] - 1.0
                all_days_fwd[h].append(fr)
                half = "pre" if dates[i] < SPLIT_DATE else "post"
                all_days_fwd_by_half[h][half].append(fr)

    for pname in ["hammer", "shooting_star", "doji", "bullish_engulfing", "bearish_engulfing",
                  "morning_star", "evening_star", "three_white_soldiers", "three_black_crows",
                  "breakout_60d", "breakout_252d", "breakdown_60d", "support_bounce"]:
        sig_list = []
        for sym in symbols:
            for d in per_symbol_patterns[sym][pname]:
                sig_list.append((sym, d))
        all_patterns_signals[pname] = sig_list

    results = {}
    for pname, sig_list in all_patterns_signals.items():
        results[pname] = {}
        for h in HORIZONS:
            sample = []
            sample_pre = []
            sample_post = []
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
            if n_sig >= 2:
                t, diff = welch_t(sample, baseline)
            else:
                t, diff = float("nan"), float("nan")
            diff_pp = diff * 100 if not math.isnan(diff) else float("nan")

            base_pre = all_days_fwd_by_half[h]["pre"]
            base_post = all_days_fwd_by_half[h]["post"]
            diff_pre_pp = (mean(sample_pre) - mean(base_pre)) * 100 if len(sample_pre) >= 2 and base_pre else float("nan")
            diff_post_pp = (mean(sample_post) - mean(base_post)) * 100 if len(sample_post) >= 2 and base_post else float("nan")

            if pname in BEARISH_PATTERNS:
                sign_adj = -diff_pp if not math.isnan(diff_pp) else float("nan")
            elif pname in NEUTRAL_PATTERNS:
                sign_adj = float("nan")  # no predicted direction
            else:
                sign_adj = diff_pp

            results[pname][h] = {
                "n": n_sig,
                "n_pre": len(sample_pre),
                "n_post": len(sample_post),
                "diff_pp": diff_pp,
                "t": t,
                "diff_pre_pp": diff_pre_pp,
                "diff_post_pp": diff_post_pp,
                "sign_adj_pp": sign_adj,
            }

    return results, all_patterns_signals, per_symbol_patterns


def analyze_vix_regime_breakdown(series, symbols, vix_dates, vix_vals):
    """P3: 60-day breakdowns split by VIX regime at signal day."""
    regimes = {"lt20": [], "20to25": [], "gte25": []}
    for sym in symbols:
        bars = series[sym]
        pats = detect_patterns(bars)
        dates = bars["dates"]
        for d in pats["breakdown_60d"]:
            v = vix_asof(vix_dates, vix_vals, dates[d])
            if v is None:
                continue
            if v < 20:
                regimes["lt20"].append((sym, d))
            elif v < 25:
                regimes["20to25"].append((sym, d))
            else:
                regimes["gte25"].append((sym, d))

    # baseline forward returns per horizon, pooled across symbols (unconditional, not VIX-split,
    # matching the same baseline definition used elsewhere)
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
    # Normal approximation to the two-tailed critical t at alpha/n_tests (valid for the
    # sample sizes here, which are all well into the hundreds of degrees of freedom).
    try:
        from scipy.stats import norm
        adj_alpha = alpha / n_tests
        return norm.ppf(1 - adj_alpha / 2)
    except ImportError:
        # fallback: crude inverse-normal approximation (Acklam-free, coarse)
        adj_alpha = alpha / n_tests
        p = 1 - adj_alpha / 2
        # Beasley-Springer-Moro-ish crude approximation is overkill; use a lookup-free
        # bisection against the standard normal CDF via error function.
        import math as _m
        lo, hi = -10.0, 10.0
        for _ in range(200):
            mid = (lo + hi) / 2
            cdf = 0.5 * (1 + _m.erf(mid / _m.sqrt(2)))
            if cdf < p:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2


def main():
    series, (vix_dates, vix_vals) = load_data()

    pattern_order = [
        "hammer", "shooting_star", "doji", "bullish_engulfing", "bearish_engulfing",
        "morning_star", "evening_star", "three_white_soldiers", "three_black_crows",
        "breakout_60d", "breakout_252d", "breakdown_60d", "support_bounce",
    ]

    print("=" * 100)
    print("CANDLESTICKS AND CHART LINES -- RAW TEST OUTPUT")
    print("=" * 100)
    print(f"Universe: {len(ALL_STOCKS_14)} large caps (pooled) = {ALL_STOCKS_14}")
    print(f"SPY reported separately. Date range: {series['AAPL']['dates'][0]} to {series['AAPL']['dates'][-1]}")
    print(f"Split date for sub-samples: before {SPLIT_DATE} vs on/after {SPLIT_DATE}")
    print(f"Horizons (trading days): {HORIZONS}")
    print(f"Dedup window: {DEDUP_WINDOW} trading days (no repeat signal within window, per symbol+pattern)")
    print()

    print("-" * 100)
    print("MAIN RESULTS: 14-STOCK POOL")
    print("-" * 100)
    results_14, sig_signals_14, per_sym_pats_14 = analyze_group(series, ALL_STOCKS_14, None)

    n_tests_main = len(pattern_order) * len(HORIZONS)

    header = f"{'pattern':22s} {'h':>3s} {'n':>6s} {'diff_pp':>9s} {'t':>7s} {'pre_pp':>9s} {'post_pp':>9s} {'sign_adj_pp':>12s} {'dir':>4s}"
    print(header)
    print("-" * len(header))
    for pname in pattern_order:
        direction = "BULL" if pname in BULLISH_PATTERNS else ("BEAR" if pname in BEARISH_PATTERNS else "NEUT")
        for h in HORIZONS:
            r = results_14[pname][h]
            print(f"{pname:22s} {h:>3d} {r['n']:>6d} {fmt(r['diff_pp']):>9s} {fmt(r['t'],2):>7s} "
                  f"{fmt(r['diff_pre_pp']):>9s} {fmt(r['diff_post_pp']):>9s} {fmt(r['sign_adj_pp']):>12s} {direction:>4s}")
    print()

    print("-" * 100)
    print("SPY (reported separately, same definitions, n will be small)")
    print("-" * 100)
    results_spy, sig_signals_spy, per_sym_pats_spy = analyze_group(series, [SPY], None)
    print(header)
    print("-" * len(header))
    for pname in pattern_order:
        direction = "BULL" if pname in BULLISH_PATTERNS else ("BEAR" if pname in BEARISH_PATTERNS else "NEUT")
        for h in HORIZONS:
            r = results_spy[pname][h]
            print(f"{pname:22s} {h:>3d} {r['n']:>6d} {fmt(r['diff_pp']):>9s} {fmt(r['t'],2):>7s} "
                  f"{fmt(r['diff_pre_pp']):>9s} {fmt(r['diff_post_pp']):>9s} {fmt(r['sign_adj_pp']):>12s} {direction:>4s}")
    print()

    print("-" * 100)
    print("P3: 60-DAY BREAKDOWNS SPLIT BY VIX REGIME AT SIGNAL DAY (14-stock pool)")
    print("VIX regime = most recent WEEKLY VIX close on/before the signal day")
    print("-" * 100)
    vix_regime = analyze_vix_regime_breakdown(series, ALL_STOCKS_14, vix_dates, vix_vals)
    rheader = f"{'regime':10s} {'h':>3s} {'n':>6s} {'diff_pp':>9s} {'t':>7s}"
    print(rheader)
    print("-" * len(rheader))
    n_tests_vix = 0
    for regime in ["lt20", "20to25", "gte25"]:
        for h in HORIZONS:
            r = vix_regime[regime][h]
            print(f"{regime:10s} {h:>3d} {r['n']:>6d} {fmt(r['diff_pp']):>9s} {fmt(r['t'],2):>7s}")
            n_tests_vix += 1
    print(f"(total signal days by regime -- lt20: {vix_regime['lt20']['n']}, "
          f"20to25: {vix_regime['20to25']['n']}, gte25: {vix_regime['gte25']['n']})")
    print()

    total_primary_tests = n_tests_main
    total_all_tests = n_tests_main + n_tests_vix  # SPY table is descriptive/secondary, not counted in the
    # pre-registered primary family (n too small in most cells); split-half diffs are reported alongside
    # the main test, not as separate hypothesis tests.

    print("-" * 100)
    print("MULTIPLE TESTING")
    print("-" * 100)
    print(f"Primary pre-registered family: {len(pattern_order)} patterns x {len(HORIZONS)} horizons "
          f"= {n_tests_main} tests (14-stock pool, full sample).")
    print(f"P3 VIX-regime cut adds {n_tests_vix} more tests (3 regimes x {len(HORIZONS)} horizons) on the "
          f"breakdown-60d signal specifically.")
    print(f"Grand total tests run in this script (excluding the separately-reported SPY table and the "
          f"pre/post split columns, which are diagnostic, not independently thresholded): {total_all_tests}")
    for n_tests, label in [(n_tests_main, "primary (pattern x horizon)"), (total_all_tests, "primary + VIX-regime")]:
        crit = bonferroni_t(n_tests)
        print(f"  Bonferroni alpha=0.05/{n_tests} -> two-tailed critical |t| ~= {crit:.3f}")
    print()

    print("-" * 100)
    print("SURVIVORS: full-sample |t| exceeds the primary Bonferroni threshold "
          f"({bonferroni_t(n_tests_main):.3f}) AND both half-sample diffs share the predicted sign")
    print("-" * 100)
    crit_main = bonferroni_t(n_tests_main)
    any_survivor = False
    for pname in pattern_order:
        if pname in NEUTRAL_PATTERNS:
            continue
        expected_sign = 1 if pname in BULLISH_PATTERNS else -1
        for h in HORIZONS:
            r = results_14[pname][h]
            t = r["t"]
            if math.isnan(t):
                continue
            passes_bonferroni = abs(t) > crit_main
            pre_ok = (not math.isnan(r["diff_pre_pp"])) and (r["diff_pre_pp"] * expected_sign > 0)
            post_ok = (not math.isnan(r["diff_post_pp"])) and (r["diff_post_pp"] * expected_sign > 0)
            both_halves_ok = pre_ok and post_ok
            if passes_bonferroni and both_halves_ok:
                any_survivor = True
                print(f"  SURVIVOR: {pname} h={h} t={t:.2f} diff_pp={r['diff_pp']:.3f} "
                      f"pre_pp={r['diff_pre_pp']:.3f} post_pp={r['diff_post_pp']:.3f}")
    if not any_survivor:
        print("  none")
    print()

    print("-" * 100)
    print("SIGNAL COUNTS (raw, after dedup) -- 14-stock pool")
    print("-" * 100)
    for pname in pattern_order:
        total_n = sum(len(per_sym_pats_14[s][pname]) for s in ALL_STOCKS_14)
        print(f"  {pname:22s} n={total_n}")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
