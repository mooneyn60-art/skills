# Momentum Screen Variants: First Queen-Led Swarm Run

One-line: RESEARCH_SWARM queue item 1. Three changes to the live momentum
screen (pullback entry, 6-1 lookback, top-3 sector rotation), each tested by
its own worker against one shared baseline.

Last Updated: 2026-10-18
Status: DESIGN + PREDICTIONS (committed before any variant ran). Results below once run.
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
