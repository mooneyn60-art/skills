"""
Earnings reaction moves for our 8 holdings, SOFI's implied-vs-realized earnings
move, and a Black-Scholes scenario table for the SOFI Dec 18 $19 call.

RESEARCH_AGENDA item. Predictions were written and committed BEFORE this
script was run (research/2026-09-24_EARNINGS_MOVES.md, commit b82b430). This
script implements the tests described there. It prints raw numbers only -- no
conclusions are hardcoded here; the verdict is written into the note by hand
after reading this output.

Universe: NVDA SOFI INTC TGT ABBV EXEL NWG CVE.
  - Daily OHLCV: paper/history/daily_ohlcv.json (NVDA, back to 2006) and
    paper/history/daily_ohlcv_holdings.json (SOFI INTC TGT ABBV EXEL NWG CVE,
    2022-09-01 to 2026-09-23, split-adjusted, via Robinhood get_equity_historicals).
  - Earnings report dates/timing/EPS: paper/history/earnings_reports.json
    (trailing up to 8 quarters per symbol, via Robinhood get_earnings_results).
  - SOFI live option quotes: paper/history/sofi_options_2026-09-24.json (via
    Robinhood get_equity_quotes / get_option_chains / get_option_instruments /
    get_option_quotes on 2026-09-24, read-only -- no orders placed).

-----------------------------------------------------------------------------
PART 1 -- EARNINGS REACTION MOVES
-----------------------------------------------------------------------------
For each report in earnings_reports.json (as many of the trailing-8 as fall
inside the symbol's price history):

  - "pm" (after close) timing: reaction = close[report_day] -> close[next
    trading day]. The report_day close already reflects the day's regular
    session (pre-announcement); the reaction shows up the next session.
  - "am" (before open) timing: reaction = close[prior trading day] ->
    close[report_day]. The report_day close already reflects the reaction.

Move % = (end_close / start_close) - 1. We report the *signed* move and its
absolute value.

"Normal daily move" for a symbol = median absolute daily close-to-close
return over the SAME price history window, EXCLUDING the specific dates used
above as either the start or end leg of any reaction window (so the earnings
days themselves don't contaminate their own baseline). Ratio = median
|earnings move| / median |normal day move|.

EPS surprise = eps_actual - eps_estimate (both from earnings_reports.json).
"Direction match" = sign(surprise) == sign(reaction move), reported only for
quarters where both an estimate and an actual exist.

-----------------------------------------------------------------------------
PART 2 -- SOFI IMPLIED VS REALIZED EARNINGS MOVE
-----------------------------------------------------------------------------
Method (isolating the earnings-specific component of an ATM straddle):

  1. straddle_pct(expiry) = (ATM call mid + ATM put mid) / stock price, at the
     17-strike (nearest to SOFI's $16.79 spot on 2026-09-24).
  2. expiry_before = 2026-10-23 (nearest expiry that does NOT span the
     2026-10-27 am report) -- this is the "normal vol" reference.
     expiry_after  = 2026-10-30 (nearest expiry AFTER the report) -- this
     straddle's variance = normal diffusion over 36 days + the one-day
     earnings jump.
  3. Scale the before-expiry straddle out to the after-expiry's calendar-day
     count by sqrt(time), on the assumption that all of expiry_before's
     implied move comes from ordinary (non-earnings) daily vol:
         baseline_scaled = straddle_pct(before) * sqrt(days(after)/days(before))
  4. Variances add for independent sources of variance, so the earnings-only
     component is recovered by quadrature subtraction:
         implied_earnings_move = sqrt(straddle_pct(after)^2 - baseline_scaled^2)
     A plain linear subtraction (straddle_after - baseline_scaled) is also
     printed as a conservative lower bound / sanity check -- it is NOT the
     primary estimate because it double-subtracts the shared normal-vol
     component instead of treating variances as additive.

Compared against SOFI's median |realized earnings move| from Part 1.

-----------------------------------------------------------------------------
PART 3 -- SOFI DEC 18 2026 $19 CALL, BLACK-SCHOLES SCENARIOS
-----------------------------------------------------------------------------
Standard Black-Scholes call, no dividend yield (SOFI pays none), r = 4%
(approx short-term T-bill rate, used only for the tiny discounting term --
immaterial to the conclusion at this vega/theta scale). All valuations use
the actual current mark IV as the starting point and either (a) the Jan 2027
$19 call's current IV as an ex-earnings term-structure proxy, or (b) a flat
IV shock of -8 or -15 points, or (c) the scenario table's per-move IV.

Time decay: valuation date = the day after the assumed 2026-10-27 am report
(2026-10-28), so time-to-expiry shrinks by the number of calendar days from
2026-09-24 to 2026-10-28 (34 days) in every scenario -- this box isolates the
"unchanged stock, only IV/theta move" question asked in the note; it is not
a claim that the stock could not also move.

Scenario table: SOFI spot at -15%, -8%, 0%, +8%, +15% from today's spot the
day after earnings (2026-10-28), each repriced at today's IV MINUS 8 points
(the mid-size, non-symbol-specific IV-crush assumption used throughout this
section -- NOT a claim about what IV will actually do to any particular
strike/skew). The stop (0.66 trigger / 0.60 limit) and first ratchet rung
(bid 1.03) are located on that table for reference ONLY -- this script makes
no recommendation to change them; that is Nolan's call.
-----------------------------------------------------------------------------
"""
import json
import math
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
HIST = os.path.join(HERE, "..", "history")

SYMBOLS = ["NVDA", "SOFI", "INTC", "TGT", "ABBV", "EXEL", "NWG", "CVE"]


def load_prices():
    with open(os.path.join(HIST, "daily_ohlcv.json")) as f:
        main = json.load(f)
    with open(os.path.join(HIST, "daily_ohlcv_holdings.json")) as f:
        holdings = json.load(f)
    out = {}
    for sym in SYMBOLS:
        if sym in main:
            out[sym] = main[sym]
        elif sym in holdings:
            out[sym] = holdings[sym]
        else:
            raise KeyError(f"no price series for {sym}")
    return out


def load_earnings():
    with open(os.path.join(HIST, "earnings_reports.json")) as f:
        d = json.load(f)
    return {k: v for k, v in d.items() if k in SYMBOLS}


def load_sofi_options():
    with open(os.path.join(HIST, "sofi_options_2026-09-24.json")) as f:
        return json.load(f)


def load_sofi_live():
    """Refreshed 2026-09-25 live quotes for the now-two-leg SOFI call
    position (Dec 18 $19c and Dec 18 $18c) plus the 10-share stake. See
    PART 3B below -- this supersedes the single-leg PART 3 for the
    position math (PART 3 is left in place as the original single-leg
    scenario, dated to the 2026-09-24 snapshot)."""
    with open(os.path.join(HIST, "sofi_live_quotes_2026-09-25.json")) as f:
        return json.load(f)


def sorted_dates(bars):
    return sorted(bars.keys())


def trading_day_index(dates, date):
    """Index of `date` in the sorted trading-day list, or None if absent."""
    lo, hi = 0, len(dates) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if dates[mid] == date:
            return mid
        if dates[mid] < date:
            lo = mid + 1
        else:
            hi = mid - 1
    return None


def next_trading_day_on_or_after(dates, date):
    lo, hi = 0, len(dates) - 1
    ans = None
    while lo <= hi:
        mid = (lo + hi) // 2
        if dates[mid] >= date:
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return ans


# ---------------------------------------------------------------------------
# PART 1
# ---------------------------------------------------------------------------
def part1_reaction_moves(prices, earnings):
    results = {}
    for sym in SYMBOLS:
        bars = prices[sym]
        dates = sorted_dates(bars)
        reports = earnings[sym]
        moves = []
        used_dates = set()
        for rep in reports:
            rdate = rep["date"]
            idx = next_trading_day_on_or_after(dates, rdate)
            if idx is None:
                continue
            report_idx = idx if dates[idx] == rdate else idx  # nearest trading day >= report date
            if rep["timing"] == "pm":
                # prior close of report day -> next trading day's close
                start_idx = report_idx
                end_idx = report_idx + 1
            else:  # "am"
                # prior trading day's close -> report day's close
                start_idx = report_idx - 1
                end_idx = report_idx
            if start_idx < 0 or end_idx >= len(dates):
                continue
            start_close = bars[dates[start_idx]][3]
            end_close = bars[dates[end_idx]][3]
            move = end_close / start_close - 1.0
            surprise = None
            if rep.get("eps_actual") is not None and rep.get("eps_estimate") is not None:
                surprise = rep["eps_actual"] - rep["eps_estimate"]
            moves.append({
                "date": rdate,
                "timing": rep["timing"],
                "year": rep["year"],
                "quarter": rep["quarter"],
                "start_date": dates[start_idx],
                "end_date": dates[end_idx],
                "move_pct": move,
                "eps_surprise": surprise,
                "direction_match": (None if surprise is None or surprise == 0
                                    else (surprise > 0) == (move > 0)),
            })
            used_dates.add(dates[start_idx])
            used_dates.add(dates[end_idx])

        # normal-day baseline: median |daily return| excluding earnings-window dates
        daily_abs = []
        for i in range(1, len(dates)):
            if dates[i] in used_dates or dates[i - 1] in used_dates:
                continue
            c0, c1 = bars[dates[i - 1]][3], bars[dates[i]][3]
            daily_abs.append(abs(c1 / c0 - 1.0))
        normal_median = statistics.median(daily_abs) if daily_abs else float("nan")

        abs_moves = [abs(m["move_pct"]) for m in moves]
        median_abs = statistics.median(abs_moves) if abs_moves else float("nan")
        mean_abs = statistics.mean(abs_moves) if abs_moves else float("nan")
        ratio = median_abs / normal_median if normal_median else float("nan")

        results[sym] = {
            "n_reports": len(moves),
            "moves": moves,
            "median_abs_move": median_abs,
            "mean_abs_move": mean_abs,
            "normal_day_median_abs_move": normal_median,
            "ratio_to_normal_day": ratio,
        }
    return results


# ---------------------------------------------------------------------------
# PART 2
# ---------------------------------------------------------------------------
def part2_sofi_implied_vs_realized(opt, part1_sofi):
    spot = opt["stock_quote"]["last_trade_price"]
    before = opt["straddles"]["2026-10-23"]
    after = opt["straddles"]["2026-10-30"]

    straddle_before = before["call"]["mark"] + before["put"]["mark"]
    straddle_after = after["call"]["mark"] + after["put"]["mark"]
    pct_before = straddle_before / spot
    pct_after = straddle_after / spot

    n1 = before["days_to_expiry"]
    n2 = after["days_to_expiry"]
    baseline_scaled = pct_before * math.sqrt(n2 / n1)

    linear_diff = pct_after - baseline_scaled
    if pct_after ** 2 >= baseline_scaled ** 2:
        quad_diff = math.sqrt(pct_after ** 2 - baseline_scaled ** 2)
    else:
        quad_diff = float("nan")

    return {
        "spot": spot,
        "atm_strike": opt["atm_strike"],
        "straddle_before_dollars": straddle_before,
        "straddle_after_dollars": straddle_after,
        "straddle_before_pct": pct_before,
        "straddle_after_pct": pct_after,
        "days_before": n1,
        "days_after": n2,
        "baseline_scaled_pct": baseline_scaled,
        "implied_earnings_move_linear_pct": linear_diff,
        "implied_earnings_move_quadrature_pct": quad_diff,
        "realized_median_abs_move_pct": part1_sofi["median_abs_move"],
        "realized_mean_abs_move_pct": part1_sofi["mean_abs_move"],
    }


# ---------------------------------------------------------------------------
# PART 3 -- Black-Scholes
# ---------------------------------------------------------------------------
def _norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_call(S, K, T, r, sigma):
    """T in years. Returns (price, delta)."""
    if T <= 0:
        return max(S - K, 0.0), (1.0 if S > K else 0.0)
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    price = S * _norm_cdf(d1) - K * math.exp(-r * T) * _norm_cdf(d2)
    return price, _norm_cdf(d1)


def part3_call_scenarios(opt):
    call = opt["dec18_19c"]
    jan_call = opt["jan15_19c"]
    S0 = opt["stock_quote"]["last_trade_price"]
    K = call["strike"]
    r = 0.04
    iv_today = call["iv"]

    from datetime import date
    today = date(2026, 9, 24)
    expiry = date(2026, 12, 18)
    T_today = (expiry - today).days / 365.0

    valuation_day = date(2026, 10, 28)  # day after the assumed 2026-10-27 am report
    T_post = (expiry - valuation_day).days / 365.0

    price_today, delta_today = bs_call(S0, K, T_today, r, iv_today)

    # (a)/(b) unchanged-stock IV scenarios
    iv_scenarios = {
        "current_iv (sanity check, S unchanged, only time passes)": iv_today,
        "jan2027_$19c_iv_proxy": jan_call["iv"],
        "current_iv_minus_8pts": iv_today - 0.08,
        "current_iv_minus_15pts": iv_today - 0.15,
    }
    unchanged_stock = {}
    for label, iv in iv_scenarios.items():
        iv = max(iv, 0.01)
        px, delta = bs_call(S0, K, T_post, r, iv)
        unchanged_stock[label] = {
            "iv": iv,
            "price": px,
            "pct_change_from_current_mark": px / call["mark"] - 1.0,
        }

    # scenario table: spot moves x IV drop of -8 points (mid assumption)
    moves = [-0.15, -0.08, 0.0, 0.08, 0.15]
    iv_drop_for_table = 0.08
    iv_for_table = max(iv_today - iv_drop_for_table, 0.01)
    scenario_table = []
    for m in moves:
        S = S0 * (1 + m)
        px, delta = bs_call(S, K, T_post, r, iv_for_table)
        scenario_table.append({
            "spot_move_pct": m,
            "spot_price": S,
            "iv_used": iv_for_table,
            "call_price": px,
            "delta": delta,
            "vs_current_mark_pct": px / call["mark"] - 1.0,
            "above_stop_trigger_0.66": px > 0.66,
            "above_stop_limit_0.60": px > 0.60,
            "above_ratchet_rung_bid_1.03": px > 1.03,
        })

    return {
        "current_mark": call["mark"],
        "current_iv": iv_today,
        "current_delta": call["delta"],
        "current_gamma": call["gamma"],
        "current_theta": call["theta"],
        "current_vega": call["vega"],
        "bs_price_today_check": price_today,
        "unchanged_stock_iv_scenarios": unchanged_stock,
        "scenario_table_iv_drop_8pts": scenario_table,
        "stop_trigger": 0.66,
        "stop_limit": 0.60,
        "ratchet_rung_bid": 1.03,
    }


# ---------------------------------------------------------------------------
# PART 3B -- full position (two calls + shares), refreshed 2026-09-25 quotes
# ---------------------------------------------------------------------------
def part3b_position_scenarios(live):
    """As of 2026-09-25 the R17 slot plus Nolan's own add mean the SOFI
    options book is TWO Dec 18 2026 calls ($19 and $18 strikes), each with
    its own -20%-of-cost stop-limit bracket, plus 10 SOFI shares with a
    single stop (15.75, carried since 2026-09-22, no separate limit on
    record so it is treated as a stop-market). This reprices both legs and
    the shares together for the day after the assumed 2026-10-27 (am)
    report, using TODAY's (2026-09-25) live quotes as the pre-earnings
    baseline for the +/-15%/+/-8%/0% spot grid, an 8-point IV crush (same
    mid-case assumption as PART 3), and one extra day of theta beyond the
    grid's implied report-day gap (valuation date 2026-10-28, matching
    PART 3's convention). A stop is "gapped through" when the modeled
    price/value opens BELOW the stop's limit (for the calls) or its single
    trigger (for the shares) -- the order could not have filled there.
    Between the trigger and the limit, a call's stop-limit would have
    filled close to where it is modeled. No stop is proposed to move; this
    is Nolan's call per R16.3.
    """
    from datetime import date
    today = date(2026, 9, 25)
    expiry = date(2026, 12, 18)
    valuation_day = date(2026, 10, 28)
    r = 0.04
    T_now = (expiry - today).days / 365.0
    T_post = (expiry - valuation_day).days / 365.0

    S0 = live["stock_quote"]["last_trade_price"]
    shares = live["position"]["shares"]
    legs_raw = {"19C": live["position"]["dec18_19c"], "18C": live["position"]["dec18_18c"]}
    legs = {
        name: dict(K=v["strike"], iv_now=v["iv"], mark_now=v["mark"], cost=v["cost_basis"],
                   trig=v["stop_trigger"], lim=v["stop_limit"], qty=v["qty"])
        for name, v in legs_raw.items()
    }

    sanity = {}
    for name, leg in legs.items():
        px, delta = bs_call(S0, leg["K"], T_now, r, leg["iv_now"])
        sanity[name] = {"bs_price_now": px, "live_mark": leg["mark_now"], "delta": delta}

    iv_drop = 0.08
    moves = [-0.15, -0.08, 0.0, 0.08, 0.15]
    table = []
    for m in moves:
        S = S0 * (1 + m)
        row = {"move_pct": m, "spot": S, "legs": {}}
        for name, leg in legs.items():
            iv = max(leg["iv_now"] - iv_drop, 0.01)
            px, delta = bs_call(S, leg["K"], T_post, r, iv)
            if px < leg["lim"]:
                status = "GAP-THROUGH (unfilled, exposed)"
            elif px < leg["trig"]:
                status = "STOPPED (fills near limit)"
            else:
                status = "no stop hit"
            row["legs"][name] = {
                "price": px, "delta": delta, "vs_cost_pct": px / leg["cost"] - 1.0,
                "status": status,
            }
        row["shares_value"] = shares["qty"] * S
        row["shares_status"] = (
            f"STOP HIT, market fill ~{S:.2f} (gap below {shares['stop_price']})"
            if S < shares["stop_price"] else "no stop hit"
        )
        table.append(row)

    # decomposition: pure IV-crush vs pure time-decay, each in isolation, at S0 unchanged
    decomposition = {}
    for name, leg in legs.items():
        px_now, _ = bs_call(S0, leg["K"], T_now, r, leg["iv_now"])
        px_ivcrush_only, _ = bs_call(S0, leg["K"], T_now, r, leg["iv_now"] - iv_drop)
        px_decay_only, _ = bs_call(S0, leg["K"], T_post, r, leg["iv_now"])
        decomposition[name] = {
            "price_now": px_now,
            "ivcrush_only_price": px_ivcrush_only,
            "ivcrush_only_pct": px_ivcrush_only / px_now - 1.0,
            "decay_only_price": px_decay_only,
            "decay_only_pct": px_decay_only / px_now - 1.0,
        }

    # pure-decay stop-crossing check: holding S0 and IV fixed at today's live
    # values, what calendar date would theta decay ALONE push each leg's BS
    # price down through its stop trigger -- i.e. before 2026-10-27 even if
    # SOFI does not move and IV does not change.
    from datetime import timedelta
    decay_crossing = {}
    for name, leg in legs.items():
        d = today
        found = None
        while d < date(2026, 10, 27):
            T = (expiry - d).days / 365.0
            px = bs_call(S0, leg["K"], T, r, leg["iv_now"])[0]
            if px <= leg["trig"]:
                found = (d.isoformat(), px)
                break
            d += timedelta(days=1)
        decay_crossing[name] = found  # None means it does not cross before the report

    today_value = sum(l["mark_now"] * 100 * l["qty"] for l in legs.values()) + shares["qty"] * S0

    return {
        "spot_now": S0, "sanity": sanity, "table": table, "decomposition": decomposition,
        "decay_crossing_before_report": decay_crossing, "today_position_value": today_value,
    }


def fmt_pct(x):
    return "nan" if x != x else f"{x * 100:.2f}%"


def main():
    prices = load_prices()
    earnings = load_earnings()
    opt = load_sofi_options()
    live = load_sofi_live()

    print("=" * 78)
    print("PART 1 -- EARNINGS REACTION MOVES")
    print("=" * 78)
    p1 = part1_reaction_moves(prices, earnings)
    for sym in SYMBOLS:
        r = p1[sym]
        print(f"\n{sym}  n={r['n_reports']}  median|move|={fmt_pct(r['median_abs_move'])}  "
              f"mean|move|={fmt_pct(r['mean_abs_move'])}  "
              f"normal_day_median|move|={fmt_pct(r['normal_day_median_abs_move'])}  "
              f"ratio={r['ratio_to_normal_day']:.2f}x")
        for m in r["moves"]:
            surprise = "" if m["eps_surprise"] is None else f"surprise={m['eps_surprise']:+.3f}"
            dmatch = "" if m["direction_match"] is None else f"dir_match={m['direction_match']}"
            print(f"    {m['date']} ({m['timing']}) {m['start_date']}->{m['end_date']} "
                  f"move={m['move_pct']*100:+.2f}%  {surprise} {dmatch}")

    print("\n" + "=" * 78)
    print("PART 2 -- SOFI IMPLIED VS REALIZED EARNINGS MOVE")
    print("=" * 78)
    p2 = part2_sofi_implied_vs_realized(opt, p1["SOFI"])
    for k, v in p2.items():
        if isinstance(v, float):
            print(f"  {k}: {v:.4f}" + (f"  ({fmt_pct(v)})" if "pct" in k else ""))
        else:
            print(f"  {k}: {v}")

    print("\n" + "=" * 78)
    print("PART 3 -- SOFI DEC 18 2026 $19 CALL, BLACK-SCHOLES SCENARIOS")
    print("=" * 78)
    p3 = part3_call_scenarios(opt)
    print(f"  current mark: {p3['current_mark']}  IV: {p3['current_iv']:.4f}  "
          f"delta: {p3['current_delta']:.4f}  gamma: {p3['current_gamma']:.4f}  "
          f"theta: {p3['current_theta']:.4f}  vega: {p3['current_vega']:.4f}")
    print(f"  BS price today (sanity check vs mark): {p3['bs_price_today_check']:.4f}")
    print("\n  Unchanged-stock IV scenarios (valuation date 2026-10-28, day after report):")
    for label, v in p3["unchanged_stock_iv_scenarios"].items():
        print(f"    {label}: IV={v['iv']:.4f}  price={v['price']:.4f}  "
              f"chg_vs_current_mark={fmt_pct(v['pct_change_from_current_mark'])}")
    print(f"\n  Scenario table (IV drop of 8 points to {p3['scenario_table_iv_drop_8pts'][0]['iv_used']:.4f}, "
          f"valuation date 2026-10-28):")
    print(f"  {'move':>7} {'spot':>8} {'call_px':>8} {'delta':>6} {'vs_mark':>8}  "
          f"stop_trig(>0.66) stop_lim(>0.60) ratchet(>1.03)")
    for row in p3["scenario_table_iv_drop_8pts"]:
        print(f"  {row['spot_move_pct']*100:+6.0f}% {row['spot_price']:8.2f} "
              f"{row['call_price']:8.3f} {row['delta']:6.3f} "
              f"{fmt_pct(row['vs_current_mark_pct']):>8}  "
              f"{str(row['above_stop_trigger_0.66']):>16} {str(row['above_stop_limit_0.60']):>15} "
              f"{str(row['above_ratchet_rung_bid_1.03']):>14}")

    print("\n" + "=" * 78)
    print("PART 3B -- FULL POSITION (2 calls + 10 shares), LIVE 2026-09-25 QUOTES")
    print("=" * 78)
    p3b = part3b_position_scenarios(live)
    print(f"  SOFI live spot 2026-09-25 14:29 UTC: {p3b['spot_now']:.3f}")
    for name, v in p3b["sanity"].items():
        print(f"  {name} sanity: BS_now={v['bs_price_now']:.3f} vs live_mark={v['live_mark']:.3f} delta={v['delta']:.3f}")
    print(f"  Today's mark-to-market position value (2 calls x100 + 10 shares): {p3b['today_position_value']:.2f}")
    print("\n  Decomposition (spot unchanged): pure IV-crush-only vs pure time-decay-only vs combined:")
    for name, d in p3b["decomposition"].items():
        print(f"    {name}: now={d['price_now']:.3f}  IV-crush-only={d['ivcrush_only_price']:.3f} ({fmt_pct(d['ivcrush_only_pct'])})  "
              f"decay-only(34d)={d['decay_only_price']:.3f} ({fmt_pct(d['decay_only_pct'])})")
    print("\n  Pure time-decay stop-crossing check (S and IV held at today's live values -- does theta ALONE push the")
    print("  price through the stop trigger before the 2026-10-27 report?):")
    for name, hit in p3b["decay_crossing_before_report"].items():
        if hit:
            print(f"    {name}: YES -- crosses trigger around {hit[0]} (px={hit[1]:.3f}), i.e. before earnings even happens")
        else:
            print(f"    {name}: no, does not cross its trigger from decay alone before the report")
    print(f"\n  Scenario table (valuation 2026-10-28, IV drop 8pts, spot grid off live {p3b['spot_now']:.3f}):")
    for row in p3b["table"]:
        print(f"    move={row['move_pct']*100:+.0f}%  S={row['spot']:.2f}")
        for name, leg in row["legs"].items():
            print(f"        {name}: px={leg['price']:.3f} ({fmt_pct(leg['vs_cost_pct'])} vs cost)  "
                  f"delta={leg['delta']:.2f}  [{leg['status']}]")
        print(f"        10sh value={row['shares_value']:.2f}  [{row['shares_status']}]")

    return p1, p2, p3, p3b


if __name__ == "__main__":
    main()
