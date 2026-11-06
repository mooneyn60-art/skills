#!/usr/bin/env python3
"""
R17 Slot Design simulation.

Simulated (Black-Scholes) long-call backtest on real daily stock paths, comparing
Nolan's bracket exit vs a fixed 21-DTE time exit (HOLD), and a no-initial-stop
ladder-only variant, across a DTE x target-delta grid.

Data: paper/history/daily_stocks.json  (14 symbols + SPY benchmark, 2006-2026,
daily OHLC; only the close is used).

IMPORTANT LIMITATIONS (see also research/2026-09-24_R17_SLOT_DESIGN.md):
  - IV is set ONCE at entry (20-day trailing realized close-to-close log-return
    stdev * sqrt(252) * 1.15, floored at 0.15) and held CONSTANT for the life
    of the trade. Real IV moves (term structure, skew, earnings crush, vol
    regime changes) are not modeled.
  - No dividends. r = 0.04 flat.
  - Costs are a flat 3% on entry and 3% on exit (model price * 1.03 to buy,
    model price * 0.97 to sell/mark bid), i.e. a 6% round-trip spread. No
    commissions, no assignment/early-exercise modeling (European BS used
    throughout as an approximation for American calls on non-dividend stock,
    which is a reasonable approximation since early exercise of a non-dividend
    call is never optimal).
  - Universe is 14 large caps that exist through 2026 (survivorship).

This script prints raw numbers only. It draws no conclusions.
"""

import json
import math
import statistics
from datetime import datetime, timedelta
from bisect import bisect_right

# ---------------------------------------------------------------------------
# Paths / constants
# ---------------------------------------------------------------------------

DATA_PATH = "/home/user/skills/skills/robinhood-autotrader/paper/history/daily_stocks.json"

SYMBOLS = ["AAPL", "AMZN", "BAC", "C", "CSCO", "F", "GE", "GOOGL", "IBM",
           "MSFT", "NVDA", "PFE", "T", "XOM"]
BENCH = "SPY"

R = 0.04                      # risk-free rate
VOL_LOOKBACK = 20              # trading days for realized vol
VOL_MULT = 1.15                # vol premium over realized
VOL_FLOOR = 0.15
ENTRY_STEP = 10                 # every 10th trading day
TIME_EXIT_DAYS = 21             # calendar days before expiry -> time exit
BUY_MULT = 1.03
SELL_MULT = 0.97
DTE_GRID = [60, 90, 120, 180]   # calendar days to expiry at entry
DELTA_GRID = [0.30, 0.45, 0.60]
DEFAULT_DTE = 90
DEFAULT_DELTA = 0.45
SPLIT_DATE = datetime(2016, 6, 1)
SMA_WINDOW = 200

CAL_PER_YEAR = 365.0


# ---------------------------------------------------------------------------
# Math helpers (no scipy available in this environment)
# ---------------------------------------------------------------------------

def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def norm_ppf(p):
    """Acklam's rational approximation to the standard normal inverse CDF."""
    if not (0.0 < p < 1.0):
        raise ValueError("p must be in (0,1)")
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    p_low = 0.02425
    p_high = 1 - p_low
    if p < p_low:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p <= p_high:
        q = p - 0.5
        rr = q * q
        return (((((a[0]*rr+a[1])*rr+a[2])*rr+a[3])*rr+a[4])*rr+a[5])*q / \
               (((((b[0]*rr+b[1])*rr+b[2])*rr+b[3])*rr+b[4])*rr+1)
    q = math.sqrt(-2 * math.log(1 - p))
    return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
           ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)


def bs_call_price(S, K, T, sigma, r):
    if T <= 0:
        return max(S - K, 0.0)
    if sigma <= 0:
        return max(S - K * math.exp(-r * T), 0.0)
    sqrtT = math.sqrt(T)
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * sqrtT)
    d2 = d1 - sigma * sqrtT
    return S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)


def strike_for_delta(S, T, sigma, r, delta):
    """Continuous (unrounded) strike giving BS call delta == target delta."""
    d1 = norm_ppf(delta)
    K = S * math.exp((r + 0.5 * sigma * sigma) * T - d1 * sigma * math.sqrt(T))
    return K


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

def load_data():
    raw = json.load(open(DATA_PATH))
    dates = sorted(raw[SYMBOLS[0]].keys())
    date_objs = [datetime.strptime(d, "%Y-%m-%d") for d in dates]
    n = len(dates)
    closes = {sym: [raw[sym][d][3] for d in dates] for sym in SYMBOLS + [BENCH]}
    return dates, date_objs, n, closes


def build_log_returns(closes, n):
    log_ret = {}
    for sym in SYMBOLS:
        c = closes[sym]
        log_ret[sym] = [math.log(c[i] / c[i - 1]) for i in range(1, n)]
    return log_ret


def realized_sigma(log_ret, sym, idx):
    """20-day realized vol ending just before idx (returns for days idx-20..idx)."""
    rets = log_ret[sym][idx - VOL_LOOKBACK:idx]
    stdev = statistics.stdev(rets)  # sample stdev, ddof=1
    sigma = stdev * math.sqrt(252) * VOL_MULT
    return max(sigma, VOL_FLOOR)


def sma200(closes, sym, idx):
    if idx < SMA_WINDOW - 1:
        return None
    window = closes[sym][idx - SMA_WINDOW + 1: idx + 1]
    return sum(window) / len(window)


# ---------------------------------------------------------------------------
# Build entries: valid (idx, idx_time_exit) pairs per DTE (symbol-independent,
# since all symbols share the same trading calendar in this dataset).
# ---------------------------------------------------------------------------

def valid_entries_for_dte(date_objs, n, dte):
    out = []
    idx_candidates = range(VOL_LOOKBACK, n, ENTRY_STEP)
    for idx in idx_candidates:
        entry_date = date_objs[idx]
        expiry_date = entry_date + timedelta(days=dte)
        time_exit_target = expiry_date - timedelta(days=TIME_EXIT_DAYS)
        # last trading day <= time_exit_target
        j = bisect_right(date_objs, time_exit_target) - 1
        if j <= idx:
            continue  # not enough future data / degenerate window
        if date_objs[j] > date_objs[-1]:
            continue
        out.append((idx, j, entry_date, expiry_date))
    return out


# ---------------------------------------------------------------------------
# Main driver
# ---------------------------------------------------------------------------

def run():
    dates, date_objs, n, closes = load_data()
    log_ret = build_log_returns(closes, n)

    entries_by_dte = {dte: valid_entries_for_dte(date_objs, n, dte) for dte in DTE_GRID}

    for dte in DTE_GRID:
        print(f"DTE={dte}: {len(entries_by_dte[dte])} valid entry dates (per symbol)")
    print()

    # records[(dte, delta)] = list of dict per (symbol, entry)
    records = {}
    # spy window returns per dte (symbol independent)
    spy_window = {}

    for dte in DTE_GRID:
        entries = entries_by_dte[dte]
        spy_rets = []
        for (idx, j_te, entry_date, expiry_date) in entries:
            spy0 = closes[BENCH][idx]
            spy1 = closes[BENCH][j_te]
            spy_rets.append(spy1 / spy0 - 1.0)
        spy_window[dte] = spy_rets

        for delta in DELTA_GRID:
            recs = []
            for sym in SYMBOLS:
                for (idx, j_te, entry_date, expiry_date) in entries:
                    S0 = closes[sym][idx]
                    sigma = realized_sigma(log_ret, sym, idx)
                    T0 = dte / CAL_PER_YEAR
                    K = strike_for_delta(S0, T0, sigma, R, delta)
                    entry_model_price = bs_call_price(S0, K, T0, sigma, R)
                    E = entry_model_price * BUY_MULT
                    if E <= 1e-8:
                        continue

                    path_idx = list(range(idx + 1, j_te + 1))
                    if not path_idx:
                        continue

                    model_prices = []
                    for jj in path_idx:
                        Sj = closes[sym][jj]
                        Tj = (expiry_date - date_objs[jj]).days / CAL_PER_YEAR
                        Tj = max(Tj, 0.0)
                        pj = bs_call_price(Sj, K, Tj, sigma, R)
                        model_prices.append(pj)

                    # ---- HOLD (time exit at last index) ----
                    hold_exit_price = model_prices[-1] * SELL_MULT
                    hold_return = hold_exit_price / E - 1.0

                    # ---- BRACKET ----
                    stop = 0.80 * E
                    bracket_stopped = False
                    bracket_exit_price = None
                    for k_i, pj in enumerate(model_prices):
                        bid = pj * SELL_MULT
                        if bid >= 1.25 * E:
                            k = math.floor((bid / E - 1.0) / 0.25)
                            candidate = (1 + 0.25 * (k - 1)) * E
                            if candidate > stop:
                                stop = candidate
                        if bid <= stop:
                            bracket_exit_price = bid
                            bracket_stopped = True
                            break
                    if not bracket_stopped:
                        bracket_exit_price = model_prices[-1] * SELL_MULT
                    bracket_return = bracket_exit_price / E - 1.0

                    # ---- NO-STOP ladder-only ----
                    stop2 = float("-inf")
                    nostop_stopped = False
                    nostop_exit_price = None
                    for pj in model_prices:
                        bid = pj * SELL_MULT
                        if bid >= 1.25 * E:
                            k = math.floor((bid / E - 1.0) / 0.25)
                            candidate = (1 + 0.25 * (k - 1)) * E
                            if candidate > stop2:
                                stop2 = candidate
                        if stop2 > float("-inf") and bid <= stop2:
                            nostop_exit_price = bid
                            nostop_stopped = True
                            break
                    if not nostop_stopped:
                        nostop_exit_price = model_prices[-1] * SELL_MULT
                    nostop_return = nostop_exit_price / E - 1.0

                    sma = sma200(closes, sym, idx)
                    above_sma = None
                    if sma is not None:
                        above_sma = S0 > sma

                    recs.append({
                        "sym": sym, "idx": idx, "entry_date": entry_date,
                        "hold_return": hold_return,
                        "bracket_return": bracket_return,
                        "bracket_stopped": bracket_stopped,
                        "nostop_return": nostop_return,
                        "nostop_stopped": nostop_stopped,
                        "above_sma": above_sma,
                    })
            records[(dte, delta)] = recs

    return records, spy_window, entries_by_dte


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def summarize(recs, key_return, key_stopped=None):
    returns = [rc[key_return] for rc in recs]
    n = len(returns)
    mean = statistics.mean(returns) if n else float("nan")
    median = statistics.median(returns) if n else float("nan")
    win_rate = sum(1 for x in returns if x > 0) / n if n else float("nan")
    out = {"n": n, "mean": mean, "median": median, "win_rate": win_rate}
    if key_stopped is not None:
        stopped = [rc for rc in recs if rc[key_stopped]]
        n_stopped = len(stopped)
        stop_share = n_stopped / n if n else float("nan")
        stopped_mean = (statistics.mean([rc[key_return] for rc in stopped])
                         if n_stopped else float("nan"))
        stopped_hold_mean = (statistics.mean([rc["hold_return"] for rc in stopped])
                              if n_stopped else float("nan"))
        recovered = [rc for rc in stopped if rc["hold_return"] > 0]
        n_recovered = len(recovered)
        recovered_share = n_recovered / n_stopped if n_stopped else float("nan")
        # "stopped" mixes two mechanisms: the -20% initial floor stop (a real
        # loss lock) and the +25%/ratchet profit-lock stop (a gain lock).
        # Break these out separately for honest reporting.
        loss_stops = [rc for rc in stopped if rc[key_return] < 0]
        gain_stops = [rc for rc in stopped if rc[key_return] >= 0]
        n_loss_stops = len(loss_stops)
        n_gain_stops = len(gain_stops)
        loss_stop_mean = (statistics.mean([rc[key_return] for rc in loss_stops])
                           if n_loss_stops else float("nan"))
        gain_stop_mean = (statistics.mean([rc[key_return] for rc in gain_stops])
                           if n_gain_stops else float("nan"))
        out.update({
            "n_stopped": n_stopped, "stop_share": stop_share,
            "stopped_mean_return": stopped_mean,
            "stopped_would_be_hold_mean": stopped_hold_mean,
            "n_stopped_then_recovered": n_recovered,
            "stopped_then_recovered_share": recovered_share,
            "n_loss_stops": n_loss_stops,
            "loss_stop_share_of_stopped": n_loss_stops / n_stopped if n_stopped else float("nan"),
            "loss_stop_mean_return": loss_stop_mean,
            "n_gain_stops": n_gain_stops,
            "gain_stop_share_of_stopped": n_gain_stops / n_stopped if n_stopped else float("nan"),
            "gain_stop_mean_return": gain_stop_mean,
        })
    return out


def paired_ttest(recs, key_a, key_b):
    diffs = [rc[key_a] - rc[key_b] for rc in recs]
    n = len(diffs)
    if n < 2:
        return {"n": n, "mean_diff": float("nan"), "t_stat": float("nan")}
    mean_diff = statistics.mean(diffs)
    sd = statistics.stdev(diffs)
    if sd == 0:
        t_stat = float("inf") if mean_diff != 0 else 0.0
    else:
        t_stat = mean_diff / (sd / math.sqrt(n))
    return {"n": n, "mean_diff": mean_diff, "t_stat": t_stat}


def main():
    records, spy_window, entries_by_dte = run()

    print("=" * 100)
    print("PER-CELL SUMMARY: DTE x delta x policy")
    print("=" * 100)
    header = (f"{'DTE':>4} {'delta':>6} {'policy':>8} {'n':>5} {'mean':>8} "
              f"{'median':>8} {'win%':>6} {'stop%':>6} {'stopmean':>9} "
              f"{'stop_hold_mean':>14} {'recov%':>7}")
    print(header)
    for dte in DTE_GRID:
        for delta in DELTA_GRID:
            recs = records[(dte, delta)]
            hold_s = summarize(recs, "hold_return")
            bracket_s = summarize(recs, "bracket_return", "bracket_stopped")
            nostop_s = summarize(recs, "nostop_return", "nostop_stopped")

            def row(name, s, has_stop):
                stop_pct = f"{s['stop_share']*100:6.1f}" if has_stop else "   n/a"
                stop_mean = f"{s['stopped_mean_return']*100:9.2f}" if has_stop else "      n/a"
                stop_hold = f"{s['stopped_would_be_hold_mean']*100:14.2f}" if has_stop else "           n/a"
                recov = f"{s['stopped_then_recovered_share']*100:7.1f}" if has_stop else "    n/a"
                print(f"{dte:>4} {delta:>6.2f} {name:>8} {s['n']:>5} "
                      f"{s['mean']*100:8.2f} {s['median']*100:8.2f} "
                      f"{s['win_rate']*100:6.1f} {stop_pct} {stop_mean} "
                      f"{stop_hold} {recov}")

            row("hold", hold_s, False)
            row("bracket", bracket_s, True)
            row("nostop", nostop_s, True)
        print("-" * 100)

    print()
    print("=" * 100)
    print("STOP BREAKDOWN: of trades stopped out, share exited at a LOSS (hit the")
    print("-20% floor or a ratchet level still below entry cost) vs at a GAIN")
    print("(ratchet had already locked in a profit level)")
    print("=" * 100)
    for dte in DTE_GRID:
        for delta in DELTA_GRID:
            recs = records[(dte, delta)]
            for name, key, stopkey in [("bracket", "bracket_return", "bracket_stopped"),
                                        ("nostop", "nostop_return", "nostop_stopped")]:
                s = summarize(recs, key, stopkey)
                print(f"DTE={dte:>3} delta={delta:.2f} {name:>7}: n_stopped={s['n_stopped']:>5} "
                      f"loss_stop%={s['loss_stop_share_of_stopped']*100:5.1f} "
                      f"loss_stop_mean={s['loss_stop_mean_return']*100:7.2f} "
                      f"gain_stop%={s['gain_stop_share_of_stopped']*100:5.1f} "
                      f"gain_stop_mean={s['gain_stop_mean_return']*100:7.2f}")

    print()
    print("=" * 100)
    print("PAIRED COMPARISON: bracket - hold, same entries")
    print("=" * 100)
    for dte in DTE_GRID:
        for delta in DELTA_GRID:
            recs = records[(dte, delta)]
            full = paired_ttest(recs, "bracket_return", "hold_return")
            pre = [rc for rc in recs if rc["entry_date"] < SPLIT_DATE]
            post = [rc for rc in recs if rc["entry_date"] >= SPLIT_DATE]
            pre_t = paired_ttest(pre, "bracket_return", "hold_return")
            post_t = paired_ttest(post, "bracket_return", "hold_return")
            print(f"DTE={dte} delta={delta:.2f} | FULL n={full['n']} "
                  f"mean_diff={full['mean_diff']*100:.3f}% t={full['t_stat']:.3f} "
                  f"| PRE-2016-06 n={pre_t['n']} mean_diff={pre_t['mean_diff']*100:.3f}% "
                  f"t={pre_t['t_stat']:.3f} "
                  f"| POST-2016-06 n={post_t['n']} mean_diff={post_t['mean_diff']*100:.3f}% "
                  f"t={post_t['t_stat']:.3f}")

    print()
    print("=" * 100)
    print(f"PAIRED COMPARISON: nostop - hold, same entries")
    print("=" * 100)
    for dte in DTE_GRID:
        for delta in DELTA_GRID:
            recs = records[(dte, delta)]
            full = paired_ttest(recs, "nostop_return", "hold_return")
            print(f"DTE={dte} delta={delta:.2f} | FULL n={full['n']} "
                  f"mean_diff={full['mean_diff']*100:.3f}% t={full['t_stat']:.3f}")

    print()
    print("=" * 100)
    print(f"TREND FILTER (P4) at default DTE={DEFAULT_DTE} delta={DEFAULT_DELTA}")
    print("=" * 100)
    recs = records[(DEFAULT_DTE, DEFAULT_DELTA)]
    recs_sma = [rc for rc in recs if rc["above_sma"] is not None]
    above = [rc for rc in recs_sma if rc["above_sma"]]
    below = [rc for rc in recs_sma if not rc["above_sma"]]
    for label, subset in [("ABOVE 200SMA", above), ("BELOW 200SMA", below)]:
        h = summarize(subset, "hold_return")
        b = summarize(subset, "bracket_return", "bracket_stopped")
        print(f"{label}: n={h['n']} hold_mean={h['mean']*100:.3f}% "
              f"bracket_mean={b['mean']*100:.3f}% "
              f"bracket_minus_hold={(b['mean']-h['mean'])*100:.3f}%")
    full_diff = paired_ttest(recs_sma, "bracket_return", "hold_return")
    print(f"(for reference) overall bracket-hold mean diff at this cell "
          f"(all entries with SMA available): {full_diff['mean_diff']*100:.3f}% "
          f"t={full_diff['t_stat']:.3f} n={full_diff['n']}")

    print()
    print("=" * 100)
    print("BENCHMARK: SPY return over the same trade window, by DTE")
    print("=" * 100)
    for dte in DTE_GRID:
        rets = spy_window[dte]
        n = len(rets)
        mean = statistics.mean(rets) if n else float("nan")
        median = statistics.median(rets) if n else float("nan")
        print(f"DTE={dte}: n={n} mean_SPY_window_return={mean*100:.3f}% "
              f"median={median*100:.3f}%")

    print()
    print("=" * 100)
    print(f"DEFAULT CELL DETAIL: DTE={DEFAULT_DTE} delta={DEFAULT_DELTA}")
    print("=" * 100)
    recs = records[(DEFAULT_DTE, DEFAULT_DELTA)]
    for name, key, stopkey in [("hold", "hold_return", None),
                                ("bracket", "bracket_return", "bracket_stopped"),
                                ("nostop", "nostop_return", "nostop_stopped")]:
        s = summarize(recs, key, stopkey)
        print(name, s)


if __name__ == "__main__":
    main()
