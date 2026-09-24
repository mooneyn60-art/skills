# Momentum vs Reversal by Horizon

One-line: RESEARCH_AGENDA item 12. Past winners keep winning over some
horizons and reverse over others. Where does each horizon sit for our
universe, and is TARS's holding period in the right one?

Last Updated: 2026-09-24
Status: IN PROGRESS. Predictions committed before any test runs (R14.1, R16.2).
Audience: Nolan, TARS sessions

## Overview

Data: paper/history/daily_ohlcv.json (14 large caps) and
daily_ohlcv_volatile.json (22 volatile names). Cross-sectional ranking of
past returns over each look-back vs the next month's return. R16 trigger (c)
is ON in the writing session. Nothing adopted before the weekend re-read.

## Predictions (written before the test)

P1 1-week and 1-month look-backs show REVERSAL (past losers beat past winners
   next month) on large caps. Weak with only 14 names.
P2 12-1 month momentum (skip the latest month) is positive for the next
   month. Weak on 14 names, clearer on the 22 volatile names.
P3 TARS's average hold (~50 trading days) and the 200-day gate sit in the
   momentum horizon, not the reversal one. The design is in the right
   horizon.

What would prove P3 wrong: the 3-month horizon showing reversal (t < -2)
in both universes.
