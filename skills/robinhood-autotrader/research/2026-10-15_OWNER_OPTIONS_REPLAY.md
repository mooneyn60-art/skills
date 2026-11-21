# Owner Options Replay and Fibonacci Test

One-line: Replayed Nolan's 197 SPY 0DTE round trips (10/08-10/14) minute by minute to ask "how could these have made more?", and tested Fibonacci retracements on 20 years of SPY.

Last Updated: 2026-10-15
Status: DONE (data, in-sample, one week)
Audience: Nolan, TARS sessions (OPTIONS_APPRENTICE stage 1-2)

## Overview

Nolan: "learn from my trades, my fails, how I could've profited ... Fibonacci ... the whole thing."
Method: fills from get_option_orders -> FIFO round trips (paper/research_scripts/owner_trips_build.py).
Robinhood's option minute bars were ~79% interpolated (flat filler), so the
option's path was rebuilt from REAL SPY minute bars with Black-Scholes at the
implied vol backed out of each entry fill (owner_trips_replay.py). Model check:
modeled price at Nolan's actual exit time vs his real exit price, median error
+1.0%, middle half within -2.8%..+5.1% (n=197). Good enough for exit studies.
Constant-IV, no skew; 10/15 excluded (bars incomplete). ONE WEEK of data.

## Results

| Exit rule applied to his exact entries | Net | Per trade | Win% | Days better than actual |
|---|---|---|---|---|
| What he actually did | +1,719 | - | 32% | - |
| Stop -20% / take +50% | -312 | -3.3% | 25% | 2 of 5 |
| Stop -40% / take +100% | +5,130 | -5.3% | 27% | 2 of 5 (all from 10/14 + 10/09) |
| Stop -30%, trail 25% off peak | +948 | -3.6% | 24% | 2 of 5 |
| Hold to 15:55 | +1,189 | -28.5% | 25% | 2 of 5 (one +11,523 day, one -6,883 day) |

- Direction: SPY moved his way 45% (5 min), 49% (15 min), 52% (30 min),
  46% (60 min) after entries. A coin flip. His edge, if any, is NOT
  picking direction.
- What his result comes from: management. Losers cut fast (median loser
  -10%, held ~3 min), winners held a bit longer (~7 min), size raised on
  some winners. Only 5 of 197 trades were up 20%+ while held and closed red.
- No mechanical exit beat his own exits consistently (each won 2 of 5 days).
  The dollar wins of wide stops and hold-to-close come from ONE trend day
  (10/14, SPY -5.2 points, trend-ness 0.56); the same rules lost big on
  10/12. The money question is day TYPE (trend vs chop), same as the
  simulator (paper/options_sim.py).
- Day type: trend-ness |close-open| / range: 10/08 0.12, 10/09 0.55,
  10/12 0.57, 10/13 0.11, 10/14 0.56, 10/15 0.53.

## Fibonacci retracements (SPY daily 2006-2026)

paper/research_scripts/fibonacci_test.py. First touch of a retracement level
inside a >=3% 20-day up-swing; next 5-day return from the level:

| Level | n | Next 5d | t | Closed back above |
|---|---|---|---|---|
| fib 38.2 | 227 | +0.21% | 1.27 | 49% |
| fib 50.0 | 160 | +0.09% | 0.41 | 42% |
| fib 61.8 | 126 | +0.23% | 0.93 | 51% |
| control 30 | 296 | +0.16% | 1.14 | 49% |
| control 44 | 177 | +0.05% | 0.26 | 45% |
| control 70 | 96 | +0.38% | 1.32 | 53% |

Fibonacci levels behave like any other level: none |t| >= 2, and a
non-Fibonacci control (70%) did best. No support effect found. Not adopted.

## What to try next (research swarm queue, OPTIONS_APPRENTICE stage 2)

1. Day-type filter: can the first 60-90 minutes predict a trend day
   (opening range width vs VIX-implied range, gap size, first-hour
   trend-ness)? Test on SPY minute data (needs more than one week; pull
   more history).
2. Keep his management style (fast loser cuts) as the baseline the rules
   must beat; mechanical stops/targets alone did not.
