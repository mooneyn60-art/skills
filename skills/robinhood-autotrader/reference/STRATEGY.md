# Strategy: Dual Momentum with a Trend Filter

A rules-based plan for the live account, derived from replicated literature rather than
assembled from plausible-sounding ideas.
Last updated: 2026-09-11 · Status: measured on history; paper-only, not funded · Audience: TARS, account owner

## Overview

This document exists because "a plan, not guessing" has a specific technical meaning: every
entry and exit is determined by a rule computable in advance, the expected return is stated
*before* the first trade, and a falsification condition is written down that would end the
strategy. Anything that fails those three tests is discretion wearing a plan's clothes.

The plan below is deliberately low-turnover and unglamorous. That is the finding, not a
compromise — see "What the research actually says."

## What the research actually says

Four results, each replicated, that jointly constrain what a small account can sensibly do.

**1. Turnover destroys retail returns.** Barber & Odean's Journal of Finance work found the
most active 20% of investors earned **11.4%/yr net of costs against 18.5% for the least
active** — a 7-point annual penalty. High-turnover households underperform low-turnover ones
by 5.5–9.6%/yr depending on adjustment. In Taiwan, with a complete national trading record,
individual investors lost **3.8 percentage points a year** in aggregate. They also documented
the disposition effect: selling winners and holding losers, which is precisely backwards.

*Implication:* every additional trade has a negative expected contribution before its thesis
is even considered. Trade frequency is a cost, not an opportunity.

**2. Published edges decay roughly by half.** McLean & Pontiff tracked 97 documented
predictors: returns were **26% lower out-of-sample and 58% lower post-publication**, with the
decay largest for the predictors that looked best in-sample, and concentrated in illiquid,
high-idiosyncratic-risk stocks.

*Implication:* any backtested figure quoted below is haircut by ~50% before use. A strategy
whose edge survives only at full published strength is not viable.

**3. Post-earnings announcement drift is dead at this size.** PEAD is one of the most durable
anomalies in the literature, and it is still unusable here: transaction costs consume
**70–100% of the paper profits**. The long-short spread is 0.04%/month in the most liquid
stocks and 2.43%/month in the most illiquid — and the illiquid leg is where costs and market
impact are prohibitive.

*Implication:* **PEAD is excluded.** This is the clearest example of a real anomaly that a
$950 account cannot harvest. Earnings dates remain useful only as a risk filter — avoid
holding through a print.

**4. Trend-following is the one that survives costs.** Moskowitz, Ooi & Pedersen documented
time-series momentum across **58 liquid instruments** in every asset class, with return
continuation over 1–12 month horizons, little exposure to standard factors, and — the key
property — it **performs best during extreme markets**. Cross-sectional momentum
(Jegadeesh & Titman) remains significant 30 years on, though there is live debate over whether
single-stock momentum is anything more than factor momentum.

*Implication:* trend is used for the highest-value decision available — *whether to hold
equities at all* — rather than for stock selection.

## The plan

**Universe.** Liquid ETFs only, fractional shares: `SPY`, `QQQ`, `IWM`, `EFA`, `VNQ`,
`GLD`, `TLT`. Cash leg: `BIL`. (`EEM` was in this list until 2026-09-11 and is now
quarantined for inconsistent split adjustment — see the EEM note below.) ETFs rather than single names because at this account size one
idiosyncratic blowup is unrecoverable, and because spreads are pennies.

**Signal, computed on the last trading day of each month:**

0. All signals run on a **monthly** basis — 12-month lookback, 1-month skip,
   10-month MA. This is the parameterisation `paper/backtest.py` measured over
   235 months. A daily variant (252/21/200) existed briefly and was removed
   unmeasured: what runs live must be what was actually tested.
1. For each asset, compute the 12-month total return skipping the most recent month (12-1).
2. **Absolute filter:** an asset is eligible only if its 12-1 return is positive *and* price is
   above its 10-month moving average (the canonical monthly equivalent of the 200-day).
   Both, not either.
3. **Relative rank:** among eligible assets, rank by 12-1 return.
4. **Hold the top 3, equally weighted.** Any slot with fewer than 3 eligible assets goes to
   `BIL`.

**Execution.**

- Rebalance monthly, at the open of the first trading day. Nothing intramonth.
- A position is exited only by the monthly rule, or by a catastrophic stop at **−25% from
  entry**, which exists for gap risk, not for trade management.
- **No options.** No leverage. No shorts.
- Expected turnover: roughly 12–20 trades per year.

**Why this shape.** Monthly rebalancing respects finding 1. The trend filter is finding 4
applied where it is strongest. ETF liquidity sidesteps finding 3. And the rules are fully
mechanical, so running them requires no forecasting skill from whoever executes — which is the
point, because nobody involved has any.

## Pre-registered expectations

Stated before the first trade, and not to be revised afterwards:

| | |
|---|---|
| Published dual-momentum backtests | ~15%/yr, max drawdown ~20% |
| After the McLean–Pontiff ~50% haircut | **6–9%/yr** |
| SPY long-run | ~10%/yr, max drawdown ~50% |

**This strategy is not expected to beat SPY on raw return.** Its claim is better
*risk-adjusted* return — comparable return at roughly half the drawdown, because the absolute
filter moves to cash in sustained declines. Anyone running it expecting to outperform an index
fund on total return has misread it.

The honest summary: the research supports *lower turnover and systematic exposure control*,
not superior stock picking. That is a real edge, and it is a small one.

## Measured result, 2007-2026 (added 2026-09-11)

`paper/backtest.py` runs the absolute filter over 235 months of real SPY closes.
Parameters were the published ones (12-1 momentum, 10-month SMA — the canonical
monthly equivalent of the 200-day), not fitted to this data. Cash earns 0%,
which understates the strategy and so errs against it.

| | filtered | buy & hold |
|---|---|---|
| CAGR | **5.99%** | 8.92% |
| max drawdown | **−17.9%** | −52.2% |
| time in market | 70% | 100% |

Drawdown through each real decline: 2008 **−5.5%** vs −52.2%; 2020 **−7.9%** vs
−19.9%; 2022 **−11.5%** vs −20.9%; 2011 −9.4% vs −16.1%; 2015 −8.3% vs −9.0%.
**2018 Q4 it made things worse: −15.6% vs −14.0%** — it sold and the market
snapped back. 34 signal switches (1.7/yr), 9 costly whipsaws.

**Scored against the pre-registration above, honestly:**

- ✅ "Not expected to beat SPY on raw return." Correct — it lost by 2.93pp/yr.
- ✅ Drawdown control works, and **better than predicted**: a third of buy-and-hold's
  worst loss, not the half I claimed.
- ❌ **"Comparable return at roughly half the drawdown" was wrong.** 5.99% against
  8.92% is not comparable; it is a third less. Over 20 years that compounds to
  212% versus 433% — buy-and-hold finished with more than twice the money.
- ❌ 5.99% lands **below** the pre-registered 6–9% range, not inside it.

The honest reading: this is a **risk-reduction** instrument, not a growth one.
Return per unit of drawdown is roughly twice buy-and-hold's (0.33 vs 0.17), and
that is a real edge — but it is paid for in return, and for an account trying to
grow rather than preserve, that trade may be the wrong way round. Its strongest
practical argument is behavioural: an investor who would abandon the plan during
a −52% drawdown but sit through −18% is better off with the filter, and that is
a fact about the investor, not the market.

## The full plan, measured (added 2026-09-11, same session)

The above tests only the filter on SPY — a crippled version that parks 30% of
its life in 0% cash. The real plan rotates. Running the whole rule over seven
assets (EEM quarantined, see below), same 235 months:

| | dual momentum | SPY b&h | same 7 held passively |
|---|---|---|---|
| CAGR | **8.14%** | 8.92% | 6.94% |
| max drawdown | **−16.1%** | −52.2% | −40.9% |

Rotation recovers most of what parking in cash gave up: **5.99% → 8.14%**, with
drawdown unchanged. The mechanism is visible rather than inferred — through the
GFC it held **TLT**, not cash, from 2008-09 onward.

Drawdowns: 2008 **−13.1%** vs −52.2%; 2020 **−5.3%** vs −19.9%; 2022 **−7.6%**
vs −20.9%; 2011 −5.8% vs −16.1%; 2018 −11.7% vs −14.0%. One miss: 2015-16 at
−9.7% vs −9.0%.

**This partly reverses the verdict above.** 8.14% lands *inside* the
pre-registered 6–9% band, and "comparable return at much lower drawdown" is a
fair description of 8.14% vs 8.92% at a third of the loss. The earlier failing
grade was issued against half the strategy, and is left standing above rather
than edited away, because which half you test is exactly the sort of thing that
quietly flatters a result.

**Against the right benchmark it looks better still.** SPY is not the honest
comparison for a seven-asset rotation; the same seven held passively is. On that
basis the rule adds **+1.20pp/yr** *and* cuts drawdown from −40.9% to −16.1%.
That is the risk-matched comparison `benchmark.py` exists to enforce.

**The caveat that matters most — and it is the NANC trap again.** QQQ was held
**63% of all months**, across the largest tech bull run in market history.
Remove QQQ and CAGR falls **8.14% → 6.42%**. So a meaningful share of this is
tech beta wearing a momentum costume, and the result is fragile to dropping a
single asset. Before any of it is funded, this needs testing on a period where
tech did not lead.

## Out-of-sample: the dot-com bust (added 2026-09-12)

The QQQ caveat above is the one that mattered, so it was tested directly on a
period where tech was the *worst* place to be. `paper/history/monthly_early.json`,
86 months, 2000-10 to 2007-11 — data entirely outside the 2006-2026 window every
figure above was measured on.

**Absolute filter on QQQ alone:**

| | filtered | buy & hold |
|---|---|---|
| total return | **+31.4%** | −42.2% |
| CAGR | **3.88%** | −7.36% |
| max drawdown | **−15.1%** | −74.6% |
| time in market | 45% | 100% |

Drawdown through the bust itself: **0.0% versus −74.6%.** Not a rounding artifact
— verified month by month, the filter sat in cash for **33 consecutive months**
(2000-10 through 2003-06), through every leg of the collapse, and re-entered in
2003-07 once the recovery was established.

**SPY+QQQ, two-asset rotation, same window:** +37.0% against SPY's +3.5%, CAGR
4.49% vs 0.48%, max drawdown **−7.8% vs −42.8%**.

**This answers the QQQ-dependency question.** The rule does not need tech to rise;
it needs *trend*. When tech collapsed it went to cash and stayed there. An
eight-year stretch in which buy-and-hold QQQ lost 42% and the filter gained 31%
is the strongest evidence in this document, and it comes from the period most
hostile to the strategy's most-held asset.

**What it cost, stated plainly.** Sitting out 33 months meant missing the +18.5%
October 2002 and +12.9% November 2002 bounces and the entire early-2003 recovery.
Late re-entry is the price of the filter, and here it was roughly 35% of the
rebound. The test also begins 2000-10, twelve months after data starts, so it
misses the first leg down from the March 2000 peak — meaning it *understates* the
protection rather than flattering it.

Limits: two assets, not seven (EFA begins 2001-08 and TLT 2002-07, both mid-bust,
so an intersection across all four would have skipped the period entirely). IWM's
pre-2005 segment is quarantined — unadjusted for its June 2005 2:1 split, same
defect class as EEM. See `paper/history/QUARANTINE_iwm_early.json`.

Other limits, stated rather than buried: it is a backtest, in-sample in a way a
forward test is not; the universe was chosen by me; no transaction costs or
spreads are modelled; cash still earns 0%; and it is seven assets, not eight.

**EEM is quarantined, not used.** Its series splices two differently-adjusted
segments — 2007-12 closes at 16.70, 2008-01 at 45.63, a factor of ~2.73 in a
month emerging markets fell hard. The true ratio and effective date are not known
with confidence, so no correction factor was guessed: a patched series would
produce prices that look real. See `paper/history/QUARANTINE_eem.json`.

## Single stocks instead of ETFs (added 2026-09-12)

Tested on request: does the same rule do better on individual names than on ETFs?
Basket of 14 large caps that were prominent in 2006, plus SPY, `paper/history/monthly_stocks.json`.

| | CAGR | max drawdown |
|---|---|---|
| momentum, top 3 of 15 | **22.67%** | −39.5% |
| same 14 stocks, equal weight passive | 13.64% | −61.3% |
| SPY passive | 8.92% | −52.2% |

Against the risk-matched benchmark — the same basket held passively, not SPY —
momentum added **+9pp/yr and cut drawdown from −61% to −39%**. On its face a far
better result than the ETF version's 8.14%.

**Then remove NVDA, AAPL and AMZN:**

| | CAGR | max drawdown |
|---|---|---|
| momentum, top 3 | **8.91%** | −27.1% |
| SPY passive | **8.92%** | −52.2% |

**8.91% against 8.92%.** The entire return advantage was three names. What
survives without them is the drawdown halving, which is real but is the same
finding the ETF version already gave.

**The survivorship admission.** This basket was assembled to avoid survivorship
bias and failed to. The names were chosen in 2026 with full knowledge of which
became moonshots — NVDA returned +58,827% over the window, AAPL +11,649%, AMZN
+11,492% — and the rule held NVDA 46% of months, AAPL 39%, AMZN 35%. Whether
momentum *found* those names or was *handed* them cannot be separated without
point-in-time universe data, which is not available here. A 2006 investor did not
know NVDA would become NVDA.

**What it does support.** Whatever edge exists lives in catching a handful of very
large winners, not in being right often. That has a practical consequence: the
approach needs enough positions and enough time for a moonshot to land, and it
cannot be judged over a year. The passive basket still returned 13.64% while
losing 61% at its worst — these names are violent, and the −39.5% drawdown on the
momentum version is the cost of admission.

**Integrity note, recorded because it nearly corrupted the test.** The
month-over-month jump heuristic flagged BAC, C and F. On inspection all three were
REAL: BAC ran 35 → 24 → 16 → 14 → 6.58 → 3.95 → 6.82 through 2008-09, smooth and
continuous, with no split factor. Quarantining them would have removed the
financial-crisis casualties and reintroduced exactly the survivorship bias the
basket was built to avoid — a safety check biasing a result toward survivors.
INTC *was* excluded, for 44.13 → 94.48 in 2026-04 and onward to 139.63, which
could be the turnaround or could be an artifact; it is excluded as unverifiable
rather than as proven wrong, since a +114% month is precisely what a momentum rule
chases.

## Falsification

The strategy is abandoned, not tuned, if any of these occur:

- `benchmark.py` shows a **negative 95% CI on excess return** versus SPY after 30+ closed
  rebalances.
- Realised max drawdown exceeds **30%**, i.e. materially worse than the backtest it is based on.
- The absolute filter fails to reduce drawdown during an actual equity decline of 15%+ — that
  is the strategy's single reason to exist, and if it does not deliver there it has none.

Parameters are **not** to be re-fit after a bad run. Re-fitting on the realised sample is how a
dead strategy becomes an overfitted one.

## Status

Proposed. Not running. Log every monthly signal to `paper/trades.jsonl` with
`"strategy": "dual-momentum"` — including the months it says hold cash, which are data points,
not non-events — and score with:

```bash
python3 paper/benchmark.py --strategy dual-momentum
```

Paper first. The live account funds it only when the interval clears zero, per the stopping
rules in `paper/PROTOCOL.md`.
