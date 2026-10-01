# Market Breadth as a Regime Signal

One-line: Does breadth (the share of our universe above its 200-day) tell us
anything about next month that VIX doesn't already?

Last Updated: 2026-10-01
Status: PREDICTIONS COMMITTED (results pending)
Audience: Nolan, TARS sessions
Research agenda item #11.

## Overview

R15 reads the regime from VIX alone. Breadth is the other classic regime
gauge: when most stocks sit above their 200-day the market is broadly healthy;
when few do, the rally is narrow or the market is breaking down. The question
is whether breadth adds information VIX lacks, for next-month SPY return and
for next-month volatility.

## Method (stated before running)

- Universe: the 14 large caps in paper/history/daily_ohlcv.json (SPY
  excluded), 2006-2026. Fixed membership so the measure doesn't drift as names
  enter. Survivorship: these are 2026's survivors (item 5), which flatters
  breadth upward in the early years.
- Breadth at each month-end = share of names with close > SMA200 (names
  without 200 bars yet are skipped that month).
- Sampling: one observation per month-end. The forward window is the next
  21 trading days, so samples don't overlap (item 8's lesson). Each month is
  one observation, so a plain t-test across months is already "clustered".
- Outcomes: SPY next-21-day return, and SPY next-21-day realized volatility
  (annualized stdev of daily log returns).
- VIX: the last weekly VIX print on or before the month-end
  (paper/history/vix_weekly.json).
- Tests:
  1. Return: corr(breadth, next-month return), and low-breadth (bottom third)
     vs high-breadth (top third) mean return difference, with t.
  2. Volatility: the same for next-month realized volatility.
  3. Beyond VIX: regress next-month vol on VIX and breadth together; report
     breadth's coefficient and t with VIX in the model.
  4. Split halves (pre/post 2016-06) for anything that looks significant.
- Hurdle: item 8's |t| >= 3.9 for adopting anything. R14: the script prints
  numbers only. R16: a refuted prediction turns the pressure state on.

## Predictions (written BEFORE the script ran)

P1 RETURN: breadth does NOT predict next-month SPY return (|t| < 2 for both
   the correlation and the low-vs-high split). Consistent with items 2 and 8:
   nothing we've tested times next-month returns.
P2 VOLATILITY: low breadth precedes HIGHER next-month volatility, t > 2. Same
   mechanism as the 200-day risk finding: a market with few names above trend
   is one already in stress.
P3 BEYOND VIX: once VIX is in the model, breadth's volatility coefficient
   shrinks and is NOT significant (|t| < 2). VIX already prices what breadth
   sees, so breadth adds nothing usable to R15.

What would refute: breadth predicting return with |t| >= 2 (P1), low breadth
NOT preceding higher vol (P2), or breadth staying significant with VIX in the
model (P3).

## Results

(pending)

## Verdict

(pending)
