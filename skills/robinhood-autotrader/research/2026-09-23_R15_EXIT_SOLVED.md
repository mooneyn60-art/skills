# The R15 Exit — Hypothesis Wrong, Adopted Exit Validated, Rule Weaker Than It Looked

One-line: self-directed work; the regime-exit hypothesis was stated in
advance and refuted, the inherited R4 exit turns out to be the best of six
tested, and R15 as a standalone strategy fails the walk-forward at 4/8.

Last Updated: 2026-09-23
Status: EXIT QUESTION CLOSED / R15 CAVEAT ADDED
Audience: TARS sessions, Nolan

## Why this was run

Nolan asked what stops TARS from learning on its own, and said he wanted to
see what TARS does rather than what he can watch. NOBODY REQUESTED THIS
TEST. R15 had been adopted an hour earlier with an exit explicitly labelled
"inherited from R4 and never tested in this regime." That was the known
hole in a rule now governing real money, so it was the obvious thing to
work on unprompted.

## A capability unlock, found first

FRED IS REACHABLE from this environment via plain HTTPS, no key required:
  https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIES>&cosd=<DATE>
Confirmed working: T10Y2Y and T10Y3M (yield curve, 5,407 daily rows each,
2006-2026), DFF (fed funds, 7,570 rows), UNRATE (monthly, 249 rows).
BAMLH0A0HYM2 (high-yield credit spread) returned only 795 rows from
2023-09 -- the cosd parameter did not take and the short history makes it
unusable for now; worth retrying with a different endpoint.

This removes the constraint recorded in 2026-09-23_VIX_REGIME.md that VIX
was the only reachable macro variable. Rates, the curve and employment are
all now available and UNTESTED.

## The hypothesis, stated before the run, and refuted

PREDICTION AS WRITTEN: "a position taken because the REGIME is stressed
should be exited when the REGIME normalises, not when the price hits a
level. Price exits cap winners; a regime exit should not, because VIX
normalisation takes months."

WRONG. Results, R15 entry held constant, exit varied, 2006-2026:

    R4 inherited (as adopted)   10.00% CAGR  -63.2% DD  270 trades
    hold until VIX<20            4.61%       -54.1%     302
    hold until VIX<18            4.66%       -57.5%     276
    VIX<20 OR the 8% stop        4.61%       -54.1%     302
    hold 63 days or stop         4.50%       -58.7%     334
    hold 126 days or stop        5.91%       -63.6%     278
    SPY buy & hold, same window  8.89%       -56.5%

WHY THE PREDICTION FAILED: VIX normalising does not mean the STOCK has
finished recovering. Exiting on VIX<20 sells in the middle of the
recovery. This is the THIRD time this week the same lesson has appeared --
capping winners is what breaks every otherwise-good entry -- and the third
time it was not anticipated.

The exit in R15 is therefore no longer an assumption. It is the best of six
tested, by a wide margin.

## The uncomfortable half — R15 is thinner than it looked

Tested as a STANDALONE strategy against SPY over the same window:

  WALK-FORWARD: 4 of 8 windows that produced any trades. That is BELOW the
  5/9 threshold used to kill other findings in this repository.
    2007-2008 WIN, 2008-2010 WIN, 2010-2012 lose, 2012-2015 no trades,
    2015-2017 lose, 2017-2019 lose, 2019-2022 lose, 2022-2024 WIN,
    2024-2026 WIN.

  CONCENTRATION: 58% of all qualifying entry signals come from three years
  -- 2008 (240 signal-days), 2020 (224) and 2022 (165) out of 1,081 total.

  DROP THE BIG WINNERS: holds through removing NVDA, AAPL and AMZN
  (10.11%), then falls to 6.12% with all five megacaps removed -- BELOW
  SPY's 8.89%.

  Return 10.00% against SPY's 8.89%, but drawdown -63.2% against -56.5%.

## What this does and does not change

IT DOES NOT INVALIDATE THE ENTRY SIGNAL. The +4.95pp per month at t=8.46
was measured on forward returns across 1,081 observations and survives
every hurdle including the megacap strip. That stands.

IT DOES MEAN R15 AS AN IMPLEMENTED STRATEGY IS WEAKER THAN THE ENTRY
STATISTIC IMPLIES, and Nolan was told so the same hour the rule was
adopted rather than after it lost money.

THE TEST NOT YET RUN, and it is the correct one: R15 was never intended as
a standalone system. It is a conditional modifier inside TARS-1 that fires
only during stress. The right question is "does adding R15 improve TARS-1
overall," not "does R15 beat SPY alone." That test is the next piece of
work and should be done before R15 ever fires live.

## Note on process

The hypothesis was written into the script's header BEFORE the run and the
script printed only data, per R14.1. That is why the refutation was visible
instead of being quietly absorbed. The rule worked the first time it was
tested on a prediction TARS actually cared about.
