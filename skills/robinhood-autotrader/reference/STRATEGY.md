# Strategy: Dual Momentum with a Trend Filter

A rules-based plan for the live account, derived from replicated literature rather than
assembled from plausible-sounding ideas.
Last updated: 2026-09-11 · Status: proposed, not yet running · Audience: TARS, account owner

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

**Universe.** Liquid ETFs only, fractional shares: `SPY`, `QQQ`, `IWM`, `EFA`, `EEM`, `VNQ`,
`GLD`, `TLT`. Cash leg: `BIL`. ETFs rather than single names because at this account size one
idiosyncratic blowup is unrecoverable, and because spreads are pennies.

**Signal, computed on the last trading day of each month:**

1. For each asset, compute the 12-month total return skipping the most recent month (12-1).
2. **Absolute filter:** an asset is eligible only if its 12-1 return is positive *and* price is
   above its 200-day moving average. Both, not either.
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
