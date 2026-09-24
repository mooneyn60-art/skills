# Is TARS Adding Value at All?

One-line: RESEARCH_AGENDA item 18. Compare the live record against SPY,
and work out how much data it would take before the answer means anything.

Last Updated: 2026-09-24
Status: PREDICTION COMMITTED, TEST NOT YET RUN
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

## Result

(not yet run)
