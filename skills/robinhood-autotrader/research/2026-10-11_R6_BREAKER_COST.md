# R6 Breaker Cost: Does Pausing After Two Stop-Losses Pay?

One-line: The 10/01 monthly audit found removing the R6 circuit breaker added
2-3pp CAGR in the backtest. This runs that result through the four hurdles
before anyone acts on it.

Last Updated: 2026-10-11
Status: DESIGN + PREDICTION (committed before the first run). Results below once run.
Audience: Nolan, TARS sessions

## Overview

R6's circuit breaker: 2 losing stop-outs within 5 trading days pause new
entries for 3 days (loss-only version live since 2026-09-23). The 10/01 audit
(research/2026-10-01_MONTHLY_AUDIT.md, paper/audit_2026_10.py Q3) showed the
old any-stop breaker costing +2.93pp CAGR and the loss-only one costing less,
but that was a single full-period number: one test, in-sample, no split,
no walk-forward, megacaps included. It is not evidence yet.

The research agenda (items 1-24) is complete, so this is the weekend block's
own pick: the one open question that bears on a live rule.

## Mechanism (written before the test)

Stop-outs cluster in sharp selloffs. Short-term losers tend to bounce
(1-month reversal, agenda item 12; momentum crashes happen on rebounds).
A pause that starts right after a cluster of stops skips the re-entries that
would catch that bounce, so it should COST return. Against that: if
selloffs keep going (volatility clustering), the pause avoids a third and
fourth stop, which should REDUCE drawdown.

## Test (fixed before running)

- paper/engine.py, TARS-1 config (same BASE as test_r15_integration.py),
  14 names, 2006-2026, price returns, whole shares, 5bp slippage.
- A = live loss-only breaker (breaker_loss_only=True).
  B = no breaker (breaker_stops=99). The drawdown halt stays on in both.
  Reference line: the old any-stop breaker.
- Hurdle 2: split 2006-2015 / 2016-2026.
- Hurdle 3: 9 equal walk-forward windows, each run fresh.
- Hurdle 4: drop NVDA, then AAPL, then AMZN, then MSFT and GOOGL (cumulative),
  then all five.
- t-statistic on the daily return difference B minus A over the full period.
- Subgroup: calendar years, count of years B beats A.

Decision rule (fixed now): recommend repealing the breaker only if B beats A
in both halves, in at least 5 of 9 windows, in every megacap-drop run, with
t >= 2 on the daily difference. This is removing a rule, not adding one,
so the multiple-testing bar for new rules (|t| >= 3.9) does not apply.
Anything less: the breaker stays and the 2-3pp is recorded as noise.

## PREDICTION

- Full period: removing the loss-only breaker adds +0.5 to +2.5pp CAGR.
- Positive in both halves; B ahead in 6 or more of 9 windows.
- Survives dropping the megacaps (still positive in every drop run).
- Max drawdown changes by less than 3pp either way.
- t on the daily difference between 1 and 2.5. Honest guess: it fails the
  t >= 2 bar, because the breaker only fires on a few dozen days in 20 years.
