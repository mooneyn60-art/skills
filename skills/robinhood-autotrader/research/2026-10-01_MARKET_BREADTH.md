# Market Breadth as a Regime Signal

One-line: Does breadth (the share of our universe above its 200-day) tell us
anything about next month that VIX doesn't already?

Last Updated: 2026-10-01
Status: DONE 2026-10-01. P1, P2 confirmed; P3 refuted narrowly (R16 on, nothing adopted).
Audience: Nolan, TARS sessions
Research agenda item #11. INDEPENDENT REPLICATION of research/2026-09-30_BREADTH_VS_VIX.md (written by the research runner a day earlier; this session hadn't seen it). Different code, monthly non-overlapping sampling, same universe.

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

Script: `paper/research_scripts/market_breadth.py`, run after predictions were
committed (5613181). 238 month-ends, 2006-10 to 2026-07. Breadth averaged 0.62
(range 0.00 to 1.00). Low third = breadth <= 0.57; high third = >= 0.79.

| Test | ALL (n=238) | pre-2016-06 (n=116) | post-2016-06 (n=122) |
|---|---|---|---|
| corr(breadth, next-month SPY return) | +0.09, t=+1.45 | +0.20, t=+2.17 | -0.05, t=-0.57 |
| low-minus-high breadth, next-month return | -0.65pp, t=-0.91 | -1.67pp, t=-1.52 | +0.33pp, t=+0.36 |
| corr(breadth, next-month realized vol) | -0.52, t=-9.34 | -0.61, t=-8.12 | -0.39, t=-4.58 |
| low-minus-high breadth, next-month vol | +9.6pp, t=+5.84 | +12.0pp, t=+4.83 | +7.2pp, t=+3.42 |
| corr(VIX, next-month vol) | +0.75, t=+17.5 | +0.78, t=+13.3 | +0.70, t=+10.8 |
| vol ~ VIX + breadth: breadth coef | -0.057, **t=-2.41** | -0.069, t=-1.95 | -0.043, t=-1.32 |
| corr(VIX, breadth) | -0.58 | -0.67 | -0.44 |

Prediction scorecard:
- P1 RETURN: CONFIRMED. Full sample |t| < 2 on both tests. The pre-2016 half
  shows corr t=+2.17, but the post-2016 half flips sign (t=-0.57), so it
  doesn't replicate. Breadth doesn't time next-month returns.
- P2 VOLATILITY: CONFIRMED, strongly and in both halves. When few large caps
  are above their 200-day, next month is about 10 vol points rougher (t=5.8;
  halves t=4.8 and 3.4).
- P3 BEYOND VIX: **REFUTED as stated, narrowly.** I predicted breadth's
  coefficient would drop below |t| = 2 with VIX in the model. On the full
  sample it's t=-2.41. It is below 2 in BOTH halves (-1.95, -1.32), and far
  below item 8's adoption hurdle of |t| >= 3.9.

R16: P3 was refuted by this session's own test, so the pressure state is on
for the rest of this session. Nothing here is adopted.

Caveats: 14-name universe chosen in 2026 (survivorship; breadth is biased up
in early years). Monthly vol is persistent from month to month, which makes
classical t-stats on the vol tests somewhat generous. VIX here is a weekly
print on or before month-end, not the exact close.

## Agreement with the 2026-09-30 study

Both runs reach the same answer by different code: breadth doesn't predict returns, does predict volatility, and keeps only a little information once VIX is in the model (theirs t=-2.80, mine t=-2.41), which fades after 2016 (theirs t=-1.48, mine t=-1.32). Neither comes close to |t| >= 3.9. Two independent runs agreeing makes this item settled.

## Verdict

**Breadth is a good warning light for rough markets, but VIX already does that
job better. Don't add breadth to R15.**

1. **No return signal.** Like every macro and regime measure tested so far
   (items 2, 8), breadth doesn't say which way the market goes next month.
2. **Real volatility signal, but mostly a copy of VIX.** Low breadth predicts
   a rougher next month, robustly. But breadth and VIX move together
   (corr -0.58), and VIX alone predicts next-month vol far better (t=17.5 vs
   9.3).
3. **What breadth adds on top of VIX is small and fragile.** With VIX in the
   model, breadth keeps a sliver of information on the full sample (t=-2.4,
   about 1.3 vol points between the low and high thirds), but not in either
   half on its own, and nowhere near the |t| >= 3.9 bar.

Practical use: a free cross-check. If VIX ever looks off or is unavailable,
"under ~55% of the universe above its 200-day" means expect a rough month.
That's context for Nolan, not a rule.

Feeds: R15 (VIX regime; unchanged), item 8 (hurdle), the 200-day risk finding
(breadth is that finding measured across the whole universe).

