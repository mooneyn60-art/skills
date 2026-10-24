# Momentum Screen Variants: First Queen-Led Swarm Run

One-line: RESEARCH_SWARM queue item 1. None of pullback entry, 6-1 lookback or
top-3 sector rotation beats the live 12-1 screen. Pullback and sector rotation
are significantly WORSE on the 20-year universe (t=-3.02, t=-2.96).

Last Updated: 2026-10-18
Status: DONE. All three variants DEAD; the live 12-1 screen stays as is. Predictions committed first (aadb496). No skeptic run (no survivor).
Audience: Nolan, TARS sessions

## Overview

The live equity book since 10/01 is a momentum sleeve: rank by 12-1 month
momentum, require above the 200-day and 63-day vol <= 80%, max 2 per sector,
8% stops raised by R4. It was adopted on Nolan's order while R16 was on, and
TARS_RULES/HOURLY_TRADING_CHECK flag it "NOT an adopted rule: review it at the
weekend re-read". Its live record so far: RVMD -1.03R, GH -1.01R,
MU -1.12R, HPE -1.0R, ASX -1.72R, HALO +1.29R (half). That's six live
results, far too few to judge anything, but worth stating.

This run: R16 is ON (R6 breaker fired 10/15 on the HPE and ASX losing stops),
so the one-time R15 task is skipped again, and per R16 nothing found today
may loosen a rule.

## Shared baseline (queen-built, so every worker measures the same thing)

paper/research_scripts/mom_screen_base.py. The live screen as a backtest:
monthly 12-1 ranking (>0), above the 200-day, 63-day vol <= 80%, max 2 per
sector, 8 slots of 85%/8 of equity, entry next open, 5bp per side, stop
max(0.92E, E after +8%, 0.80 x high close) filled through gaps, trend exit
below the 200-day. No earnings filter (no point-in-time dates).

Baseline, measured before any variant (price returns, survivorship-biased):
- LONG, 14 names, 2007-01 to 2026-10: CAGR 9.29%, maxDD -17.3%, SPY 8.94%,
  341 trades, 31% winners, +5.03% average.
- WIDE, 41 names, 2021-12 to 2026-10: CAGR 13.79%, maxDD -23.6%, SPY 11.47%,
  163 trades, 20% winners, +3.62% average.

## Variants (one worker each)

a. Pullback entry: same ranking, but buy a ranked name only on a day it is
   3-8% below its 20-day high close and above its 50-day.
b. Lookback 6-1: close[t-21] / close[t-126] - 1 instead of 12-1.
c. Sector rotation: rank sectors by the mean 6-1 momentum of their names;
   only names from the top 3 sectors are eligible.

Hurdles for each, on both universes: split halves, 9-window walk-forward
(>= 5/9), drop the megacaps, daily-return t >= 2 against the baseline.
Survives only if it beats the baseline on CAGR and passes everything.
Then the skeptic rebuilds it from scratch.

## PREDICTIONS (before any variant ran)

- a. Pullback: fewer trades, higher win rate; CAGR within +/-2pp of baseline
  on both universes; walk-forward under 5/9. Dies.
- b. 6-1: within +/-1.5pp of baseline; the change flips sign across
  windows (about 4-5/9). Dies.
- c. Sector top-3: on LONG (7 sectors, 14 names), it barely changes anything,
  within +/-1pp. On WIDE, within +/-3pp. Dies.
- No variant clears daily-return t >= 2. Nothing goes to Nolan as a
  proposal.

## Results (workers' raw tables; queen re-ran variant a after a harness fix)

Diff = variant minus baseline, CAGR percentage points. Daily t = mean daily
return difference. All in-sample backtests, mechanical, price returns,
survivorship-biased universes.

| Variant | Universe | Diff CAGR | Daily t | 1st / 2nd half | Megacaps dropped | Walk-forward ahead |
|---|---|---|---|---|---|---|
| a pullback (fixed) | LONG 14, 2007-2026 | **-2.95** | **-3.02** | -2.39 / -3.34 | -1.19 | 3 of 9 |
| a pullback (fixed) | WIDE 41, 2021-2026 | -0.88 | -0.24 | +7.24 / -6.79 | -3.71 | 6 of 9 |
| b 6-1 lookback | LONG | -0.09 | -0.08 | +0.02 / -0.27 | +0.17 | 3 of 9 |
| b 6-1 lookback | WIDE | -3.70 | -0.87 | +2.38 / -7.28 | -2.67 | 3 of 9 |
| c sector top-3 | LONG | **-2.61** | **-2.96** | -3.74 / -1.57 | -1.30 | 2 of 9 |
| c sector top-3 | WIDE | +1.65 | +0.29 | +6.54 / -3.70 | +0.03 | 6 of 9 |

Baselines: LONG 9.29% CAGR (SPY 8.94%), WIDE 13.79% (SPY 11.47%).

Supporting data from the workers:
- a: of 965 monthly picks on WIDE, only 140 ever got their 3-8% dip that
  month. The average wait was 8 trading days. Waiting for the dip mostly
  means missing the move.
- b: the 6-1 and 12-1 top-8 overlap by 69% on average (33-100%), so the
  lookback change swaps about 2-3 names a month, and those swaps don't help.
- c: on LONG the filter removes about 2.5 of the would-be top-8 in 85% of
  months. With 14 names in 8 sectors, "top 3 sectors" leaves about 4 candidates
  for 8 slots, so the book sits in cash. That's the main reason it costs
  return.

## Harness bug found by worker a, fixed before the verdict

The first pullback run let a stopped-out name be re-bought later the same
month (18-21 of 161 entries), and didn't recheck the 200-day on the signal
day (9 entries were bought below their 200-day). Both make the variant
something other than the spec. The queen patched pullback mode only
(bought_this_month set, 200-day recheck); baseline numbers are unchanged
(checked: same 9.29% / 13.79%). Before/after for variant a LONG: -3.14pp,
t=-3.18 -> -2.95pp, t=-3.02. Same verdict. Workers b and c independently
reported the same two harmless quirks (dead code, a shared boundary day
between halves, start clamped to bar 253).

## Verdict

- Nothing beats the baseline AND passes the hurdles. Per RESEARCH_SWARM
  step 4, no skeptic run.
- The WIDE "6 of 9 windows" for a and c are noise: window swings of
  +24 to -37pp on a 41-name, 5-year sample, daily t < 0.3, halves flip sign.
- The two significant results are NEGATIVE: on 20 years, waiting for a
  pullback and narrowing to top sectors both cost about 3pp a year (|t| near 3).
  Neither clears |t| >= 3.9, but they point the same way and are
  mechanistically sensible (missing moves, holding too much cash).
- What this does NOT say: that the live screen is good. It beats SPY
  by +0.35pp (LONG) and +2.3pp (WIDE) in-sample on hand-picked names, and its
  live record is 5 losing stops of 6. The baseline itself has never been
  through the hurdles against SPY. That's the obvious next item (added to the
  swarm queue).

## Prediction scorecard

- a: CAGR within +/-2pp on both: WRONG on LONG (-2.95, worse than
  predicted), right on WIDE (-0.88). Fewer trades RIGHT. Higher win rate
  WRONG (28% vs 31%). Dies: RIGHT.
- b: within +/-1.5pp: RIGHT on LONG (-0.09), WRONG on WIDE (-3.70). About 4-5/9:
  WRONG (3/9 both). Dies: RIGHT.
- c: LONG within +/-1pp: WRONG (-2.61; I didn't think through the cash
  drag). WIDE within +/-3pp: RIGHT (+1.65). Dies: RIGHT.
- No variant clears t >= 2 against baseline: RIGHT in the positive
  direction. Two variants clear it NEGATIVELY, which I didn't predict.

## Cost

Session cost went from $105.48 to $109.22 during this run, a delta of about
$3.74. That figure may not include the three sonnet workers if they're
billed separately, so it's a lower bound. Logged in SWARM_COSTS.csv.
