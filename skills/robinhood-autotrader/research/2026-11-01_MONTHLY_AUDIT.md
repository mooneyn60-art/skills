# Monthly Expectancy Audit, November 2026

One-line: The live account LOST 22.4% in October against SPY's -1.1%
(deposits stripped), with a -49.8% peak-to-trough swing, driven by owner
0DTE options. Closed-trade expectancy is -0.10R (n=29). TARS-1's rules beat
SPY over the last 12 months in backtest, but the 200-day selection spread
is negative for the second month running.

Last Updated: 2026-11-01
Status: DONE. Script and predictions committed before the run (paper/audit_2026_11.py).
Audience: Nolan, TARS sessions

## Headline: the account is losing to the index

- **Live NAV index, 2026-10-01 to 2026-10-30, deposits stripped
  (paper/nav_index.csv): -22.36% vs SPY -1.09%, gap -21.27pp.** Max drawdown
  in the month -49.8% (peak 1.5467 on 10/13 after a +43.9% options day,
  trough 0.7764 on 10/30). The swings are owner 0DTE options days
  (10/13 +44%, 10/15 -37.5%), per the close reports in NOLAN_LOG.
- Shadow TARS-1 book (rules only, no discretion), 2026-09-25 to 10-23:
  -7.80% vs SPY -1.49% (-6.3pp). The shadow log stops at 10/23 (no rows
  10/26-10/30). **Desk: the shadow book has not been updated for a week.**
- R6 drawdown halt fired 10/15 (-44% from the high-water mark), 10 trading
  days through 10/29, then a rebase. **No rebase row is in trades.jsonl**;
  without it the -15% condition is still literally true. Desk: log the
  rebase (R6 "Deposits rebase the high-water mark" format).

## Q1 Expectancy (paper/trades.jsonl, closed live trades with a numeric planned_risk)

- All, ex-SOFI shares (1 excluded), ex-option-slot: **n=29, mean -0.10R,
  total -2.96R, t=-1.01.**
- By exit: user_closed n=24 -0.06R; stop n=3 -0.78R; trail n=2 +0.38R.
- By source: user_discretionary n=15 +0.03R; **TARS-1 n=11 -0.29R (t=-1.70)**.
- By holding: < 1 day n=12 +0.08R; **1-5 days n=11 -0.37R (t=-2.70)**;
  >= 5 days n=2 +0.38R.
- Option book (options closed 9/24 on, with a planned_risk): n=8, -0.26R,
  t=-2.34, all SOFI/NVDA Sept trades; R17 tag coverage is poor.
- Coverage problem: most October trades have no numeric planned_risk (the
  momentum sleeve: 9 of 12 closes; owner 0DTE scalps: none), so they're
  invisible here. The desk's own R figures for the sleeve (12 closes,
  -0.43R) are in research/2026-10-25_MOMENTUM_SCREEN_VS_SPY.md. Until
  planned_risk is logged on every row, this audit measures a minority of
  the trades.

## Q3 Rule cost: R2's exit after 1 vs 2 vs 3 closes below the 200-day (never measured before)

engine.py TARS-1 (live loss-only breaker), 14 names. In-sample, mechanical.

| Cut | 1 close (live) | 2 closes | 3 closes |
|---|---|---|---|
| Full 2006-2026 | 12.24% / -31.0% | 12.35% / -35.9% | 13.91% / -30.5% |
| 2006-2015 | 9.03% | 8.55% | 11.90% |
| 2016-2026 | 18.42% | 17.36% | **14.91%** |
| No megacaps | 4.33% | 4.28% | 3.91% |

Walk-forward vs live: 2 closes ahead 5 of 9, 3 closes ahead 3 of 9. The
3-close full-period +1.67pp is all 2006-2015; in 2016-2026 it costs 3.5pp,
and it loses without megacaps. **No change: the one-close exit stays.**

## Q4 Decay: the last 12 months (2025-10-28 to 2026-10-29)

- TARS-1 backtest +17.08% vs SPY +11.98% vs equal-weight hold of the 14
  +11.24% (15 trades). TARS-1 BEAT both.
- **200-day above-minus-below forward 21-day spread, monthly: n=12,
  mean -3.74pp, t=-2.23.** Last month: t=-2.11. For two months running,
  names above their 200-day have done WORSE over the next month than names
  below it, over the trailing year. TARS-1 still beat SPY because the stops
  and the names held carried it, not because the 200-day gate picked well.
  n=12 monthly samples, so one year can do this by chance (the 20-year
  evidence is positive), but it's now a repeat, and it's flagged. If it
  shows up a third month, it goes to a full re-test.

## Q5 Positions held over 6 months

None. The account's oldest equity positions date from 2026-10-01 (the
momentum rebuild). Nothing is anywhere near 6 months.

## Prediction scorecard (committed in the script header)

- Q1 mean between -0.5R and 0: RIGHT (-0.10R). No split clears |t| 2:
  **WRONG** (holding 1-5 days t=-2.70; option book t=-2.34).
- Q2 live behind SPY by more than 10pp: RIGHT (-21.27pp). Shadow behind by 2-8pp: RIGHT (-6.3pp).
- Q3 within +/-1pp, sign flips (3-6 of 9): mostly RIGHT (2 closes +0.11pp,
  5/9); 3 closes +1.67pp is outside the band. **Half wrong.**
- Q4 TARS-1 trails SPY by 0-8pp: **WRONG** (beat by +5.1pp). Spread |t| < 2:
  **WRONG** (t=-2.23).

## A correction to last week (R15 repeal), found during this audit

On 2026-10-25 the weekend block repealed R15 after checking that R16 was
OFF. It checked the R6 CIRCUIT BREAKER (expired) and the consecutive-loss
count (0), but not the R6 DRAWDOWN HALT, which was active from 10/15
through 10/29. R16 trigger (b) is "either R6 breaker is active", so R16 was
ON, and the routine said to skip the task in that case. The repeal is in
substance a tightening (R15 allowed entries below the 200-day; with it gone
they're never allowed), and the result reproduced. But the precondition
was wrong. Today's audit also refuted three of its own predictions, which
turns R16 on again (trigger c) for this session. So this session can't
redo the re-read cleanly either.

Action taken: R15 returned to SUSPENDED (behaviour identical: VIX 25+ is an
alert only, the 200-day gate always applies), the one-time task restored to
the weekend routine with a stricter R16 check (circuit breaker AND
drawdown halt AND this session's refuted predictions), and the mistake
logged in skills/tars/SELF_REVIEW.md.
