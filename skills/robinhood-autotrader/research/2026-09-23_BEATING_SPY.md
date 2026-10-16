# Four Attempts to Beat SPY — All Four Failed

One-line: four independent strategy families were tested against the same
four hurdles and none of them beats the index on return; every one of them
reduces drawdown.

Last Updated: 2026-09-23
Status: CLOSED — negative result, and the most useful thing found so far
Audience: TARS sessions, Nolan

## Overview

Nolan asked for a strategy that beats SPY. Four were built and tested. None
survived. This file records the failures at full strength because a negative
result that took four attempts is worth more than a positive one that took
none — and because a future session WILL rediscover at least one of these
and should not have to spend the compute twice.

Test bed: 5,209 daily bars per symbol, 2006-01 to 2026-09, whole shares,
5bp slippage per side, 5%/yr borrowing cost where leverage is used.
SPY buy and hold over the same window: 9.11% CAGR, max drawdown -56.5%,
Sharpe 0.55.

## Attempt 1 — Cross-sectional momentum rotation

Hold the two strongest names above their own 200-day, rebalanced monthly.
Printed 25.79% CAGR against SPY's 9.11%, beat SPY in 7 of 9 walk-forward
windows, and held up in both halves of the split sample.

KILLED BY THE DROP-THE-WINNERS TEST. Removing NVDA takes it to 16.62%,
also removing AAPL to 14.88%, also removing AMZN to 9.38%, and removing the
five megacaps to 8.03% -- below the index. The entire edge is three stocks
in a 14-name universe that TARS selected in 2026 with full knowledge of
which names had won. It is not a strategy, it is hindsight.

## Attempt 2 — Concentrating the book

Fewer, larger positions, on the argument that whole-share quantization lets
share price rather than conviction set position weight. Documented
separately in 2026-09-23_POSITION_COUNT.md.

REJECTED, AND BACKWARDS. Below four positions is destructive; n=1 and n=2
never win a single walk-forward window and n=1 goes negative in two. Four
through eight are statistically indistinguishable. Trend following pays
through a few large winners that cannot be identified at entry, so fewer
slots buys fewer tickets rather than a sharper bet.

## Attempt 3 — Volatility targeting (Moreira & Muir shape)

Scale exposure inversely to 20-day realised volatility. At a 20% target
capped at 2x it returned 10.08% against SPY's 9.11%, with a -48.0%
drawdown against -56.5%. Better on both axes.

IT SURVIVED THE NULL, WHICH IS WORTH RECORDING. The obvious objection is
that it is just leverage in disguise. It is not: the rule ran at 1.49x
average leverage, and constant 1.4x leverage with no timing at all returns
9.59% with a -71.4% drawdown. Same exposure, 23 POINTS LESS DRAWDOWN and
more return. The risk control is real.

KILLED ON RETURN BY THE WALK-FORWARD AND THE PARAMETER GRID. It beat SPY in
only 4 of 9 windows. And across a 6x5 grid of lookback window against
target volatility, CAGR rises MONOTONICALLY with the target in every single
row -- at a 16% target it mostly loses to SPY, at 24% it wins. A parameter
whose result is a monotonic function of how much leverage it dials in is a
leverage dial, not an edge.

Capped at 1.0x, which is what a cash account can actually do, it returns
9.28% against 9.11% -- noise on return, but a -40.9% drawdown against
-56.5%, which is not noise.

## Attempt 4 — Trend-gated volatility targeting

The synthesis: vol-targeted position size, but only while above the
200-day. Worse than either component alone. 6.80% CAGR, -40.9% drawdown,
Sharpe 0.41, and 3 OF 9 WALK-FORWARD WINDOWS -- the same score that killed
the exit-confirmation band on 2026-09-21. Dead.

## The pattern, which is the actual finding

FOUR INDEPENDENT FAMILIES -- cross-sectional selection, concentration,
volatility timing, and trend timing -- ALL FAIL IN THE SAME DIRECTION.
Every one of them reduces drawdown reliably and across both halves of the
sample. NOT ONE of them raises return reliably. Where return appears to
improve, it traces to either survivorship in the universe or leverage in
the parameter.

That is not four unlucky results. It is what an efficient market looks like
from the position TARS actually occupies: no informational edge, public
price data, retail execution. The risk premium is available. Alpha is not.

## What this implies, stated plainly

1. Timing and selection buy RISK CONTROL, not return. Every rule in
   TARS_RULES.md that survived testing -- the 200-day gate, the hard stop,
   the widened trail -- is a drawdown tool. They should be justified that
   way and never sold to Nolan as return enhancers.
2. Broad exposure plus drawdown control plus deposits is the honest
   strategy at this account size. A deposit of roughly 7.5% of account
   value per week is worth more than any edge measured above, by more than
   an order of magnitude.
3. ANY future candidate must clear the drop-the-winners test and a
   walk-forward before it is shown to Nolan as a live proposal. Attempts 1
   and 3 both looked excellent until exactly those two tests.

## What was NOT tested and would be the honest next step

Every test here runs on 15 symbols TARS chose in 2026. THAT IS THE BINDING
DEFECT and no amount of further testing on this universe fixes it. The next
real step is a universe selected as of the START of the test window --
point-in-time index membership, including the names that later failed --
which is not available from the current data source. Until that exists,
every cross-sectional result in this repository should be treated as an
upper bound rather than an estimate.
