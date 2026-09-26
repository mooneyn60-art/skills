# Is TARS Adding Value at All?

One-line: RESEARCH_AGENDA item 18. Compare the live record against SPY,
and work out how much data it would take before the answer means anything.

Last Updated: 2026-09-24
Status: DONE. Answer: unknown, and it will stay unknown for years. Predictions (bb6733e) held.
Audience: Nolan, TARS sessions

## What can and can't be measured

The live account has traded since 2026-09-10, about ten trading days. The
ledger holds one close report with an account value (2026-09-18); there is
no daily account-value series to compare against SPY day by day. So the
live comparison is necessarily trade-level (R-multiples), and the
"how long until we know" question has to come from the backtest's
statistical properties.

## Method (fixed before the run)

A. Live: closed live trades from paper/trades.jsonl by owner (TARS vs
   Nolan), n, mean R, t.
B. Backtest of the CURRENT ruleset, approximated in paper/engine.py as:
   200-day as the only entry/exit line (R2', exit_on="slow", no 50-day, no
   near-the-high rule), 8% hard stop, 20% trail, percentage cap only.
   Daily active return vs SPY (both price returns, same 14 names).
   Report annualised alpha, tracking error, information ratio (IR), and
   the years of live data needed for t = 2: years = (2 / IR)^2.
C. Trades needed: n = (2 x sd(R) / mean(R))^2 from the backtest's trade
   R-multiples (R = return / 8%).

## PREDICTION

A. Live TARS trades: n around 10, mean R negative or near zero, |t| < 1:
   too few to say anything.
B. Backtest IR between -0.1 and +0.3; if positive, more than 40 years of
   live data to prove it at t = 2.
C. More than 100 trades needed.
Overall: "Is TARS adding value?" cannot be answered for years. The honest
answer today is "unknown", and the default assumption should be "no", since
most active strategies don't beat the index.

## Answer first

WE CAN'T KNOW YET, AND WON'T FOR A LONG TIME. That is a real finding, not
a dodge:
- Live, TARS's own closed trades with a recorded risk: n=6, mean -0.41R,
  t=-1.35. Nolan's: n=17, mean +0.01R. Neither says anything yet.
- Even taking the 20-year backtest at face value, the current rules beat
  SPY by +1.9%/yr with 16.6%/yr tracking error. That is an information
  ratio of 0.11, and at that ratio it takes about 312 years of live
  results to reach t = 2. The backtest itself (20 years) only reaches
  t = +0.50 against SPY.
- A trap worth knowing: the backtest's TRADES look strong (+0.51R per
  trade, t=3.77 over 442 trades), yet the PORTFOLIO barely beats SPY.
  Positive trades are not the same as beating the index. A trend system
  that is long stocks most of the time earns mostly the market's return,
  and its good-looking trades are largely the market going up.

## Result

Script: paper/test_tars_value.py.

    A  live closed trades with planned_risk (paper/trades.jsonl)
       Nolan  n=17  mean +0.01R  sd 0.53R  t=+0.08
       TARS   n= 6  mean -0.41R  sd 0.74R  t=-1.35
       all    n=23  mean -0.10R  sd 0.61R  t=-0.78
       (paper/pressure_state.py counts 10 TARS closes; 4 lack planned_risk,
       so R can't be computed for them.)

    B  backtest, current rules approximated, 14 names, 2006-10 to 2026-09
       strategy CAGR 11.81%  vs SPY 9.03% (both price returns)
       active return +1.88%/yr, tracking error 16.6%/yr, IR +0.11, t=+0.50
       first half IR +0.10, second half +0.13: stable, and small
       live years needed for t=2 at IR 0.11: ~312

    C  backtest trades: n=442, mean +0.51R, sd 2.87R, t=+3.77
       trades needed for t=2 at that edge: 124
       if the true edge were +0.25R: 526 trades; +0.10R: 3,287

Survivorship flatters B and C: the 14 names all survived to 2026 (agenda
item 5). The true numbers are likely worse.

## Scored against the prediction

    A  n~10, mean <= 0, |t|<1: RIGHT in substance (n=6, -0.41R, |t|=1.35 slightly above 1)
    B  IR -0.1 to +0.3, >40 years: RIGHT (0.11, ~312 years)
    C  >100 trades: RIGHT (124 at the backtest edge; far more at a realistic one)

## What this means (interpretation)

- The right question isn't "is TARS beating SPY?". It can't be answered.
  Better questions: (1) is TARS FOLLOWING its rules (measurable now)?
  (2) are its costs and mistakes small (measurable now: items 6, 9)?
  (3) does its risk profile differ from SPY in a way Nolan wants, e.g.
  smaller drawdowns (measurable from the backtest)?
- 124 trades at the backtest edge is roughly 2-3 years at this account's
  pace. That is the earliest point the TRADE-level question could be
  answered. The PORTFOLIO-vs-SPY question effectively never can be.
- The default should be humility. Most active strategies don't beat the
  index after costs, and nothing here shows TARS is an exception. Nor does
  anything show it's worse: after 10 trading days, there is no evidence
  either way.
