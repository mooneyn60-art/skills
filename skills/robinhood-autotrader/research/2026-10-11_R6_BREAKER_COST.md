# R6 Breaker Cost: Does Pausing After Two Stop-Losses Pay?

One-line: The backtest says dropping the R6 breaker adds +2.42pp CAGR, but it
fails walk-forward (4 of 9) and t=+1.44, and nearly all of the gain sits in
2006-2015. Path noise, not an edge. The breaker stays.

Last Updated: 2026-10-11
Status: DONE. FAILS the hurdles: walk-forward 4 of 9, t=+1.44. R6 breaker STAYS. Prediction committed first (afbf02b); half right.
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

## Results (python3 paper/test_r6_breaker.py, run 2026-10-11, data through 2026-10-08)

All numbers: engine backtest, 14 names, mechanical levels, nothing fitted.
"Diff" = no breaker minus live loss-only breaker.

| Test | Breaker CAGR / maxDD | None CAGR / maxDD | Diff CAGR | Diff DD |
|---|---|---|---|---|
| Full 2006-2026 (in-sample) | 12.23% / -31.0% | 14.66% / -35.3% | +2.42pp | 4.4pp deeper |
| Old any-stop breaker (ref) | 11.79% / -33.6% | | | |
| 2006-2015 | 9.03% / -31.0% | 10.14% / -35.3% | +1.11pp | 4.4pp deeper |
| 2016-2026 | 18.61% / -20.9% | 18.69% / -22.0% | +0.07pp | 1.1pp deeper |
| without NVDA | 10.08% | 12.25% | +2.17pp | 3.7pp deeper |
| without NVDA+AAPL | 8.30% | 9.25% | +0.95pp | 2.2pp shallower |
| without NVDA+AAPL+AMZN | 6.80% | 6.80% | +0.00pp | 0.3pp shallower |
| without all five megacaps | 4.38% | 6.20% | +1.82pp | 3.9pp deeper |

- Daily return difference: n=5,021, mean +0.88bp/day, **t=+1.44**.
- Walk-forward, 9 fresh windows: no-breaker ahead in **4 of 9** (+5.10, -1.01,
  -0.08, 0.00, -0.11, +2.06, +0.92, -4.48, +0.93pp). One window (2013-15) never
  triggered the breaker at all. The biggest single gain is 2006-2009 (+5.10pp,
  the financial crisis), the biggest loss is 2022-2024 (-4.48pp).
- Calendar years: no-breaker ahead in 12 of 21, but the yearly gaps swing
  from -18.9pp (2016) to +42.4pp (2023). 4,806 of 5,021 days differ, even though
  the breaker blocked entries on only 113. One skipped entry changes which
  names fill the slots for months afterwards, so the yearly gaps are mostly
  path divergence rather than the breaker's direct effect.

## Verdict against the decision rule (fixed before running)

| Hurdle | Needed | Got | Pass? |
|---|---|---|---|
| Both halves positive | yes | +1.11 / +0.07pp | technically, but the second half is zero |
| Walk-forward | >= 5 of 9 | 4 of 9 | **FAIL** |
| Every megacap-drop run positive | yes | one run exactly 0.00pp | **FAIL** |
| t on daily difference | >= 2 | +1.44 | **FAIL** |

**The breaker stays.** The +2-3pp from the 10/01 audit was a single
in-sample path. What does reproduce is the drawdown side: without the
breaker, max drawdown is deeper in 4 of the 6 full-period runs (by 3.7-4.4pp).
That is the trade it makes, which fits the mechanism's "avoids the third and
fourth stop" half. But the drawdown effect hasn't been tested to the same
standard either, so it isn't claimed as an edge.

## Prediction scorecard (honest)

- Full period +0.5 to +2.5pp: RIGHT (+2.42).
- Positive in both halves: RIGHT, but only on a technicality (+0.07pp).
- 6 or more of 9 windows: **WRONG** (4).
- Survives every megacap drop: **WRONG** (one run 0.00pp).
- Max drawdown changes by less than 3pp: **WRONG** (4.4pp deeper without it).
- t between 1 and 2.5 and fails the bar: RIGHT (+1.44).
Running tally for this session's predictions: 3 right, 3 wrong.

## Literature (haiku sub-agent, a lead only, nothing verified against full texts)

- Clare, Seaton, Smith & Thomas (2013, J. Asset Management): on the S&P 500,
  stop-loss rules add nothing on top of a 200-day MA rule. This is the closest
  published test to ours, and it agrees with today's result.
- Kaminski & Lo (2014, J. Financial Markets): stop-losses cut expected return
  under a random walk and help only when returns have momentum, so any benefit
  depends on the regime. Our crisis-window gain (+5.1pp in 2006-09) against a
  2022-24 loss (-4.5pp) fits that.
- Daniel & Moskowitz (2016, JFE): sharp rebounds follow market declines. That
  is the cost side of the mechanism.
- No published test of a "pause after N stop-outs" rule was found.

## Found along the way: the R16 counter is missing two TARS losses

paper/pressure_state.py counts a trade as TARS-owned only if strategy starts
with "TARS" and account == "live". The 10/01 rebalance rows
(rebal-1001-rvmd-close, rebal-1001-gh-close, strategy "momentum_satellite",
no account field) are TARS R4 hard stops that hit on 10/08 at about -1.0R each.
The script doesn't see them. Counting them, the run of consecutive TARS losses
is 6, not 4, and there were 2 losses in the last 5 weekdays, not 0. R16 is ON
either way, so nothing changes today. The weekday session should either tag
those rows (owner/account) or widen the classifier. Neither was changed here,
because who owns the "momentum_satellite" bucket is a ledger question.
