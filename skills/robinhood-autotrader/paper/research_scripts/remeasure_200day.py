"""
Re-measure the 200-day gate's RETURN and RISK claims with non-overlapping,
first-trading-day-of-month sampling and month-clustered errors.

RESEARCH_AGENDA / research/2026-09-25_200DAY_REMEASURED.md. Predictions (P1-P4)
were written and committed BEFORE this script was run (commit 60ae4b0). This
script prints raw numbers only -- no conclusions are hardcoded here.

Reuses loading/SMA/forward-return/spearman/t-stat helpers from
momentum_reversal.py (same directory) rather than reimplementing them.

-----------------------------------------------------------------------------
DESIGN
-----------------------------------------------------------------------------
Sampling: ONLY the first trading day of each calendar month, taken from the
pooled calendar of each universe (large caps excl. SPY; volatile names).
Consecutive samples are ~21 trading days apart, so the 21-day forward window
used for the RETURN/RISK claims does not overlap the next sample's window.
The 12-1m momentum IC uses the same monthly dates. The 63-day/quarterly
version samples only the first trading day of Jan/Apr/Jul/Oct (quarter
starts), so its 63-day forward window likewise does not overlap the next
sample.

For each sampled date, for each name with a valid 200-day SMA (i >= 199 bars
of history at that date) and the needed forward window, we record:
  above      : close > SMA200 (bool)
  fwd21      : close[t+21]/close[t] - 1
  fwd63      : close[t+63]/close[t] - 1  (only used by the quarterly test)
  vol21      : stdev(daily log returns over t..t+21) * sqrt(252)
  dd21_mag   : magnitude (>=0) of the worst peak-to-trough decline over
               t..t+21, peak reset to close[t] (i.e. 0.15 means a 15% max
               drawdown in the 21 days after the sample date)
  mom121     : close[t-21]/close[t-252] - 1  (12-1 month momentum), when
               t >= 252 bars of history

RETURN claim -- three variants, all on fwd21 (plus a quarterly fwd63 variant):
  (a) NAIVE t: pool every name-month observation into above/below groups
      (ignoring which month they came from) and run a Welch two-sample t.
      This over-weights months with more names above (or below).
  (b) MONTH-CLUSTERED t: for each month with at least one name in EACH group,
      compute diff_month = mean(above) - mean(below) that month. Then a
      one-sample t-test of the diff_month series across months (each month
      is one observation/cluster, regardless of how many names it holds).
  (c) EXCESS-RETURN version: each name's fwd21 minus that month's own
      equal-weight average fwd21 (across all SMA-valid names that month),
      i.e. a name/month fixed-effect removed. NOTE: subtracting a constant
      that is identical for the above- and below-group within a given month
      cannot change mean(above)-mean(below) for that month algebraically, so
      re-running method (b) on excess returns is guaranteed to reproduce (b)
      exactly. To make this a genuinely distinct check, (c) instead pools
      the individual excess observations (not first averaged per month) and
      computes a cluster-robust t (clustered by month) on the pooled excess
      values -- the same "month-clustered standard errors" construction used
      in test_multiple_testing_r15.py / MULTIPLE_TESTING.md's method (b),
      applied here to market/month-adjusted returns instead of raw daily
      overlapping ones. This is sensitive to how above/below group sizes
      vary month to month in a way (b)'s per-month-average approach is not.
  Quarterly/63d: same construction as (b) but sampled quarterly (Jan/Apr/
      Jul/Oct first trading day) on fwd63, clustered by quarter.

RISK claim: forward 21-day realized vol and forward 21-day max-drawdown
magnitude, above vs below, using the SAME per-month-average-then-t-across-
months construction as (b), but reported as "mean(below) - mean(above)"
(so a positive number means "below the 200-day is riskier", matching the
claim's direction for both metrics).

MOMENTUM IC: per month, Spearman rank IC of (12-1m lookback, fwd21) across
every name with both defined that month (no SMA-validity filter). One-sample
t of the per-month IC series across months -- already non-overlapping by
construction here (unlike a IC computed on daily samples), so this t is the
honest one. Compared against momentum_reversal.py's month-END-sampled 12-1m
IC (large caps t=2.60 n=234; volatile t=3.45 n=234) as a sampling-anchor
robustness check (first-trading-day-of-month vs last-trading-day-of-month).

Splits: large caps at 2016-06-01, volatile at 2021-01-01. Every clustered
statistic above ((b), (c), quarterly/63d, RISK vol, RISK dd, momentum IC) is
also reported for the two halves (dates strictly before / on-or-after the
split).

Usage: python3 paper/research_scripts/remeasure_200day.py
"""

import math
import sys
from pathlib import Path
from statistics import mean, stdev

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from momentum_reversal import (  # noqa: E402
    LARGE_CAP_FILE, VOLATILE_FILE, LARGE_CAP_SPLIT, VOLATILE_SPLIT,
    load_universe, sma, forward_return, spearman, one_sample_t, welch_t, fmt,
)

SMA_GATE = 200
MOM_LONG = 252
MOM_SKIP = 21


# -----------------------------------------------------------------------------
# Sampling calendars
# -----------------------------------------------------------------------------

def first_trading_day_dates(series):
    """First trading date present in the pooled calendar for each YYYY-MM."""
    all_dates = set()
    for s in series.values():
        all_dates.update(s["dates"])
    all_dates = sorted(all_dates)
    by_month = {}
    for d in all_dates:
        ym = d[:7]
        if ym not in by_month:
            by_month[ym] = d  # first date seen for that month (sorted order)
    return sorted(by_month.values())


def quarter_start_dates(monthly_dates):
    return [d for d in monthly_dates if d[5:7] in ("01", "04", "07", "10")]


# -----------------------------------------------------------------------------
# Per-name-month record building
# -----------------------------------------------------------------------------

def vol_and_drawdown(C, i, horizon):
    """Forward realized vol (annualized, log returns) and max-drawdown
    magnitude (>=0) over the window [i, i+horizon], peak reset at i."""
    window = C[i:i + horizon + 1]
    if len(window) < horizon + 1:
        return None, None
    log_rets = [math.log(window[k] / window[k - 1]) for k in range(1, len(window))]
    if len(log_rets) < 2:
        return None, None
    vol = stdev(log_rets) * math.sqrt(252)
    peak = window[0]
    min_dd = 0.0
    for px in window[1:]:
        peak = max(peak, px)
        dd = px / peak - 1.0
        if dd < min_dd:
            min_dd = dd
    return vol, -min_dd


def build_records(series, dates):
    """dates -> list of per-name records at that date."""
    records = {}
    for d in dates:
        recs = []
        for sym, s in series.items():
            i = s["idx"].get(d)
            if i is None:
                continue
            C = s["C"]
            sma200 = sma(C, i, SMA_GATE)
            above = None if sma200 is None else (C[i] > sma200)
            fwd21 = forward_return(series, sym, i, 21)
            fwd63 = forward_return(series, sym, i, 63)
            vol21 = dd21 = None
            if fwd21 is not None:
                vol21, dd21 = vol_and_drawdown(C, i, 21)
            mom121 = None
            if i >= MOM_LONG:
                mom121 = C[i - MOM_SKIP] / C[i - MOM_LONG] - 1.0
            recs.append({
                "sym": sym, "above": above, "fwd21": fwd21, "fwd63": fwd63,
                "vol21": vol21, "dd21": dd21, "mom121": mom121,
            })
        records[d] = recs
    return records


# -----------------------------------------------------------------------------
# Stat constructions
# -----------------------------------------------------------------------------

def clustered_t(a, b, ca, cb):
    """Cluster-robust t for mean(a) - mean(b), clustered by ca/cb labels.
    Same construction as paper/test_multiple_testing_r15.py's clustered_t."""
    if len(a) < 2 or len(b) < 2:
        return float("nan"), float("nan"), 0, 0
    ma, mb = mean(a), mean(b)

    def var_of_mean(xs, cs, m):
        g = {}
        for x, c in zip(xs, cs):
            g[c] = g.get(c, 0.0) + (x - m)
        G = len(g)
        if G < 2:
            return float("nan"), G
        return sum(v * v for v in g.values()) / (len(xs) ** 2) * G / (G - 1), G

    va, ga = var_of_mean(a, ca, ma)
    vb, gb = var_of_mean(b, cb, mb)
    if math.isnan(va) or math.isnan(vb) or (va + vb) <= 0:
        return float("nan"), ma - mb, ga, gb
    return (ma - mb) / math.sqrt(va + vb), ma - mb, ga, gb


def per_period_diff_series(records, dates, value_key, flip=False, min_each=1):
    """For each date, diff = mean(above) - mean(below) [or below-above if
    flip] among names with both groups present that date and a non-None
    value_key. Returns list of (date, diff)."""
    out = []
    for d in dates:
        above_vals = [r[value_key] for r in records.get(d, []) if r["above"] is True and r[value_key] is not None]
        below_vals = [r[value_key] for r in records.get(d, []) if r["above"] is False and r[value_key] is not None]
        if len(above_vals) >= min_each and len(below_vals) >= min_each:
            diff = mean(below_vals) - mean(above_vals) if flip else mean(above_vals) - mean(below_vals)
            out.append((d, diff))
    return out


def halves(series_list, split_date):
    """series_list: list of (date, value). Returns (full_vals, pre_vals, post_vals)."""
    full = [v for _, v in series_list]
    pre = [v for d, v in series_list if d < split_date]
    post = [v for d, v in series_list if d >= split_date]
    return full, pre, post


def report_t(vals):
    t, m, n = one_sample_t(vals)
    return f"n={n:3d} mean={fmt(m * 100, 3):>8s}pp t={fmt(t, 2):>6s}" if n else "n=  0 (none)"


def report_t_raw(vals):
    """Same as report_t but for values not already in percent-return units
    (vol, drawdown, IC) -- prints mean without the pp suffix."""
    t, m, n = one_sample_t(vals)
    return f"n={n:3d} mean={fmt(m, 4):>8s}  t={fmt(t, 2):>6s}" if n else "n=  0 (none)"


# -----------------------------------------------------------------------------
# Per-universe report
# -----------------------------------------------------------------------------

def report_universe(name, series, split_date):
    print(f"\n{'=' * 90}\nUNIVERSE: {name}  ({len(series)} names)\n{'=' * 90}")
    mdates = first_trading_day_dates(series)
    qdates = quarter_start_dates(mdates)
    print(f"first-trading-day-of-month dates: {len(mdates)} ({mdates[0]} .. {mdates[-1]})")
    print(f"of which quarter-start (Jan/Apr/Jul/Oct) dates: {len(qdates)}")

    records = build_records(series, mdates)  # covers fwd21/fwd63/vol/dd/mom at monthly dates

    # ---- RETURN claim -------------------------------------------------
    print("\n--- RETURN claim: forward 21-day return, above vs below SMA200 ---")

    above21_all, below21_all = [], []
    for d in mdates:
        for r in records[d]:
            if r["above"] is True and r["fwd21"] is not None:
                above21_all.append(r["fwd21"])
            elif r["above"] is False and r["fwd21"] is not None:
                below21_all.append(r["fwd21"])
    t_a, diff_a = welch_t(above21_all, below21_all)
    print(f"(a) naive (pooled name-months, Welch t): n_above={len(above21_all)} n_below={len(below21_all)} "
          f"diff={fmt(diff_a * 100, 3)}pp t={fmt(t_a, 2)}")
    above21_pre = [r["fwd21"] for d in mdates if d < split_date for r in records[d] if r["above"] is True and r["fwd21"] is not None]
    below21_pre = [r["fwd21"] for d in mdates if d < split_date for r in records[d] if r["above"] is False and r["fwd21"] is not None]
    above21_post = [r["fwd21"] for d in mdates if d >= split_date for r in records[d] if r["above"] is True and r["fwd21"] is not None]
    below21_post = [r["fwd21"] for d in mdates if d >= split_date for r in records[d] if r["above"] is False and r["fwd21"] is not None]
    ta1, da1 = welch_t(above21_pre, below21_pre)
    ta2, da2 = welch_t(above21_post, below21_post)
    print(f"    (a) first half: diff={fmt(da1 * 100, 3)}pp t={fmt(ta1, 2)} n={len(above21_pre)}+{len(below21_pre)}   "
          f"second half: diff={fmt(da2 * 100, 3)}pp t={fmt(ta2, 2)} n={len(above21_post)}+{len(below21_post)}")

    diffs_b = per_period_diff_series(records, mdates, "fwd21")
    full_b, pre_b, post_b = halves(diffs_b, split_date)
    tb, mb, nb = one_sample_t(full_b)
    tb1, mb1, nb1 = one_sample_t(pre_b)
    tb2, mb2, nb2 = one_sample_t(post_b)
    print(f"(b) month-clustered (per-month avg diff, t across months): months={nb} diff={fmt(mb * 100, 3)}pp t={fmt(tb, 2)}")
    print(f"    first half: months={nb1} diff={fmt(mb1 * 100, 3) if nb1 else 'NA'}pp t={fmt(tb1, 2)}   "
          f"second half: months={nb2} diff={fmt(mb2 * 100, 3) if nb2 else 'NA'}pp t={fmt(tb2, 2)}")

    def excess_pools(dates_subset):
        exc_above, exc_below, c_above, c_below = [], [], [], []
        for d in dates_subset:
            valid = [r["fwd21"] for r in records[d] if r["above"] is not None and r["fwd21"] is not None]
            if not valid:
                continue
            bench = mean(valid)
            for r in records[d]:
                if r["fwd21"] is None or r["above"] is None:
                    continue
                exc = r["fwd21"] - bench
                if r["above"]:
                    exc_above.append(exc); c_above.append(d)
                else:
                    exc_below.append(exc); c_below.append(d)
        return exc_above, exc_below, c_above, c_below

    ea, eb, ca, cb = excess_pools(mdates)
    tc, dc, ga, gbb = clustered_t(ea, eb, ca, cb)
    print(f"(c) excess-return, pooled obs, cluster-robust t (clustered by month): "
          f"n={len(ea)}+{len(eb)} clusters={ga}/{gbb} diff={fmt(dc * 100, 3)}pp t={fmt(tc, 2)}")
    ea1, eb1, ca1, cb1 = excess_pools([d for d in mdates if d < split_date])
    ea2, eb2, ca2, cb2 = excess_pools([d for d in mdates if d >= split_date])
    tc1, dc1, _, _ = clustered_t(ea1, eb1, ca1, cb1)
    tc2, dc2, _, _ = clustered_t(ea2, eb2, ca2, cb2)
    print(f"    first half: diff={fmt(dc1 * 100, 3)}pp t={fmt(tc1, 2)}   second half: diff={fmt(dc2 * 100, 3)}pp t={fmt(tc2, 2)}")

    diffs_q = per_period_diff_series(records, qdates, "fwd63")
    full_q, pre_q, post_q = halves(diffs_q, split_date)
    tq, mq, nq = one_sample_t(full_q)
    tq1, mq1, nq1 = one_sample_t(pre_q)
    tq2, mq2, nq2 = one_sample_t(post_q)
    print(f"Quarterly 63d-fwd, clustered by quarter: quarters={nq} diff={fmt(mq * 100, 3)}pp t={fmt(tq, 2)}")
    print(f"    first half: quarters={nq1} diff={fmt(mq1 * 100, 3) if nq1 else 'NA'}pp t={fmt(tq1, 2)}   "
          f"second half: quarters={nq2} diff={fmt(mq2 * 100, 3) if nq2 else 'NA'}pp t={fmt(tq2, 2)}")

    # ---- RISK claim -----------------------------------------------------
    print("\n--- RISK claim: forward 21-day realized vol and max-drawdown, below vs above (positive = below is riskier) ---")

    diffs_vol = per_period_diff_series(records, mdates, "vol21", flip=True)
    fv, prev, postv = halves(diffs_vol, split_date)
    tv, mv, nv = one_sample_t(fv)
    tv1, mv1, nv1 = one_sample_t(prev)
    tv2, mv2, nv2 = one_sample_t(postv)
    print(f"vol21 (annualized): months={nv} mean(below-above)={fmt(mv, 4)} t={fmt(tv, 2)}")
    print(f"    first half: months={nv1} mean={fmt(mv1, 4) if nv1 else 'NA'} t={fmt(tv1, 2)}   "
          f"second half: months={nv2} mean={fmt(mv2, 4) if nv2 else 'NA'} t={fmt(tv2, 2)}")

    diffs_dd = per_period_diff_series(records, mdates, "dd21", flip=True)
    fd, pred, postd = halves(diffs_dd, split_date)
    td, md, nd = one_sample_t(fd)
    td1, md1, nd1 = one_sample_t(pred)
    td2, md2, nd2 = one_sample_t(postd)
    print(f"dd21 (max-drawdown magnitude): months={nd} mean(below-above)={fmt(md, 4)} t={fmt(td, 2)}")
    print(f"    first half: months={nd1} mean={fmt(md1, 4) if nd1 else 'NA'} t={fmt(td1, 2)}   "
          f"second half: months={nd2} mean={fmt(md2, 4) if nd2 else 'NA'} t={fmt(td2, 2)}")

    # ---- Momentum IC ------------------------------------------------------
    print("\n--- 12-1m momentum rank IC vs forward 21d return (first-trading-day sampling) ---")
    ics = []
    for d in mdates:
        pairs = [(r["mom121"], r["fwd21"]) for r in records[d] if r["mom121"] is not None and r["fwd21"] is not None]
        if len(pairs) >= 3:
            xs, ys = zip(*pairs)
            ic = spearman(list(xs), list(ys))
            if not math.isnan(ic):
                ics.append((d, ic))
    full_ic, pre_ic, post_ic = halves(ics, split_date)
    ti, mi, ni = one_sample_t(full_ic)
    ti1, mi1, ni1 = one_sample_t(pre_ic)
    ti2, mi2, ni2 = one_sample_t(post_ic)
    print(f"IC: months={ni} mean={fmt(mi, 4)} t={fmt(ti, 2)}")
    print(f"    first half: months={ni1} mean={fmt(mi1, 4) if ni1 else 'NA'} t={fmt(ti1, 2)}   "
          f"second half: months={ni2} mean={fmt(mi2, 4) if ni2 else 'NA'} t={fmt(ti2, 2)}")
    print("    for comparison, momentum_reversal.py (month-END sampling) 12-1m IC:")
    print("      large caps: full n=234 IC_mean=0.0614 t=2.60 | pre n=112 t=1.92 | post n=122 t=1.75")
    print("      volatile:   full n=234 IC_mean=0.0893 t=3.45 | pre n=167 t=3.51 | post n=67  t=0.59")

    return {
        "return_naive_t": t_a, "return_naive_diff": diff_a,
        "return_clustered_t": tb, "return_clustered_diff": mb, "return_clustered_t1": tb1, "return_clustered_t2": tb2,
        "return_excess_t": tc, "return_excess_diff": dc, "return_excess_t1": tc1, "return_excess_t2": tc2,
        "return_q63_t": tq, "return_q63_diff": mq, "return_q63_t1": tq1, "return_q63_t2": tq2,
        "risk_vol_t": tv, "risk_vol_diff": mv, "risk_vol_t1": tv1, "risk_vol_t2": tv2,
        "risk_dd_t": td, "risk_dd_diff": md, "risk_dd_t1": td1, "risk_dd_t2": td2,
        "ic_t": ti, "ic_mean": mi, "ic_t1": ti1, "ic_t2": ti2,
    }


def main():
    large = load_universe(LARGE_CAP_FILE, exclude={"SPY"})
    volatile = load_universe(VOLATILE_FILE)

    print("200-DAY GATE, RE-MEASURED -- raw output, no conclusions baked in")
    print("Sampling: first trading day of each month (non-overlapping 21d fwd windows);")
    print("quarterly first-trading-day for the 63d variant. See docstring for exact")
    print("construction of each 'clustered' statistic.")
    print(f"Large-cap universe: {sorted(large.keys())}")
    print(f"Volatile universe:  {sorted(volatile.keys())}")

    res_large = report_universe("large caps (SPY excluded)", large, LARGE_CAP_SPLIT)
    res_vol = report_universe("volatile names", volatile, VOLATILE_SPLIT)

    print(f"\n{'=' * 90}\nSUMMARY (key clustered t-stats)\n{'=' * 90}")
    for label, res in (("large caps", res_large), ("volatile", res_vol)):
        print(f"{label}: RETURN (b) t={fmt(res['return_clustered_t'],2)}  RETURN (c) t={fmt(res['return_excess_t'],2)}  "
              f"RETURN 63d-quarterly t={fmt(res['return_q63_t'],2)}  "
              f"RISK vol t={fmt(res['risk_vol_t'],2)}  RISK dd t={fmt(res['risk_dd_t'],2)}  "
              f"12-1m IC t={fmt(res['ic_t'],2)}")


if __name__ == "__main__":
    main()
