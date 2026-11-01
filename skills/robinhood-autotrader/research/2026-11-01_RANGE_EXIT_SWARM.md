# Range-Regime Exits: Can Any Exit Keep the Entry's Edge? (Swarm Run 2)

One-line: RESEARCH_SWARM queue item 3, the standing open question. The
range-bottom entry (ADX<20, bottom 25% of the 60-day range) has the best
signal evidence in the repo (t=5.20). Every exit tried so far threw the edge
away. Three new exits, one per worker, against SPY and an entry-at-the-top control.

Last Updated: 2026-11-01
Status: DESIGN + PREDICTIONS (committed before any variant ran). Results below once run.
Audience: Nolan, TARS sessions

## Why not queue item 2 (Options Apprentice Stage 2)

It needs Nolan's option round trips with ENTRY times. The ledger has entry
times for only 15-17 of 191 owner option trades. The full set came from the
broker's order history, which was dumped once to a scratch folder
(owner_trips_build.py -> trips.json) and never committed. Rebuilding it
needs the account number, which TARS must not pick by itself. Fix for the
desk: commit trips.json (per-trade prices and times, no balances, so R13 is
fine) to paper/history/owner_trips.json. Item 2 stays next in the queue.

## Shared harness (queen-built)

paper/research_scripts/range_exit_base.py. Entry as in
research/2026-09-23_RANGE_REGIME.md, 14 names 2006-2026, max 4 positions,
85%/4 of equity each, fractional, 5bp per side, 8% hard stop always on.
Control: identical but entering in the TOP 25% of the range. If an exit
preserves the entry signal, bottom beats top under that exit.
Reproduction check of the old rule (range-top exit): 4.98% CAGR vs SPY
9.02% (old note: 6.81%, with whole shares and different sizing).
Same verdict: far below SPY.

## Variants

a. TIME exit: sell after 21 trading days, the horizon the signal was
   measured on.
b. R4-style exit: stop to breakeven once a close is >= 1.08 x entry, then
   sell on a close below max(breakeven, 0.80 x highest close); 63-day cap.
c. MIDPOINT exit: sell when the close reaches 50% of the 60-day range
   (take the mean-reversion and leave).

Survives only if: bottom beats SPY on CAGR, in both halves, with megacaps
dropped, and in >= 5 of 9 windows; AND bottom beats the top control (the
edge is the entry's, not the market's); daily t >= 2 vs SPY. Then the skeptic.

## PREDICTIONS (before any variant ran)

- a. Time exit: CAGR 5-9%, below SPY. Bottom beats top by +1 to +3pp (the
  entry edge shows up at its own horizon). Walk-forward vs SPY at most 4/9. Dies.
- b. R4 exit: CAGR 7-11%, the best of the three; vs SPY roughly level,
  walk-forward at most 5/9, fails the halves or megacap drop. Dies.
- c. Midpoint: worst, CAGR 3-6%, caps winners even harder. Dies.
- No survivor. The entry signal is real but too small per trade (+1pp a
  month) to beat simply holding the index in a rising 20 years.
