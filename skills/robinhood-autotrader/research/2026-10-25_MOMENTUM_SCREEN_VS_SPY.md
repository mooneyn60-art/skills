# Live Momentum Screen vs SPY: Does It Beat Just Holding the Index?

One-line: RESEARCH_SWARM queue item 1b. The live 12-1 momentum screen has
only been measured in-sample. Here it goes through the four hurdles against
SPY buy-and-hold, and its live trades are scored in R.

Last Updated: 2026-10-25
Status: DESIGN + PREDICTION (committed before the run). Results below once run.
Audience: Nolan, TARS sessions

## Overview

Last week's swarm (research/2026-10-18_MOMENTUM_SCREEN_SWARM.md) found no
variant better than the live screen. It didn't test whether the screen
itself beats SPY. Since 10/01 the whole equity book is this screen, with no
index core ("drop the spy, I want to beat it not ride it", Nolan 10/01).
So the question that matters is whether it does.

## Test (fixed before running)

- Harness: paper/research_scripts/mom_screen_base.py, baseline as is (12-1,
  above the 200-day, vol <= 80%, 2 per sector, 8 slots, 15% cash, stops by R4,
  5bp per side, next-open fills).
- Benchmarks: (1) SPY buy-and-hold, price only; (2) 85% SPY + 15% cash,
  rebalanced daily, which matches the screen's cash floor.
- Universes LONG (14 names, 2007-2026) and WIDE (41 names, 2021-12 on).
- Hurdles: split halves; 9 walk-forward windows (screen ahead of SPY in >= 5);
  drop the megacaps; t on the daily return difference (screen minus SPY) >= 2.
  Bonferroni bar for calling it an edge: |t| >= 3.9.
- Live: every closed momentum_satellite / rebalance_momentum trade in
  paper/trades.jsonl with a planned_risk, scored in R.

## PREDICTION

- LONG: screen minus SPY within +/-2pp CAGR. Daily t between -1 and +1.
  Walk-forward ahead of SPY in 4-5 of 9. Megacaps dropped: the screen trails
  SPY by more than 4pp (2.99% vs 8.94% CAGR is already in last week's run).
- WIDE: screen ahead of SPY by 0-4pp; daily t < 1.5.
- Against 85% SPY: the screen looks slightly better than against SPY, but
  still t < 2.
- Live trades: mean below -0.3R, n under 15, so it means nothing either way.
- Verdict: the screen is NOT shown to beat SPY. If so, that goes to Nolan as
  information (his call), not as a rule change.
