# Range-Regime Exits: Can Any Exit Keep the Entry's Edge? (Swarm Run 2)

One-line: RESEARCH_SWARM queue item 3, the standing open question. The
range-bottom entry (ADX<20, bottom 25% of the 60-day range) has the best
signal evidence in the repo (t=5.20). Every exit tried so far threw the edge
away. Three new exits, one per worker, against SPY and an entry-at-the-top control.

Last Updated: 2026-11-01
Status: DONE. All three exits DEAD vs SPY (-2.2 to -4.3pp CAGR). Only the 21-day time exit keeps the entry's edge over the control (+2.0pp, t=0.65), and it still loses to SPY. The standing question is answered: no exit tested monetises the signal. Predictions committed first (b18e1cc).
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

## Results (workers' raw tables, harness range_exit_base.py, 14 names 2006-2026)

All in-sample, mechanical, price returns, survivorship-biased. The strategy is
at most 85% invested, with cash at 0%, against SPY 100% invested (worker
note). That costs about 1pp a year against SPY at these returns. It doesn't
change any verdict below, and it doesn't touch bottom vs top.

| Exit | Bottom CAGR / DD | Top (control) | SPY | Bottom - SPY (t) | Bottom - top (t) | Halves (bottom / SPY) | Megacaps dropped (bottom / SPY) | WF vs SPY | WF vs top |
|---|---|---|---|---|---|---|---|---|---|
| a. 21-day time | 6.16% / -51.0% | 4.15% | 9.02% | -2.86pp (-1.01) | **+2.01pp (+0.65)** | 2.68 / 5.01, 9.75 / 13.18 | 2.73 / 9.02 | 5 of 9 | 5 of 9 |
| b. R4 trail + 63d | 6.87% / -61.1% | 8.16% | 9.02% | -2.15pp (-0.75) | -1.29pp (-0.26) | 4.40 / 5.01, 9.49 / 13.18 | 3.36 / 9.02 | 3 of 9 | 5 of 9 |
| c. midpoint | 4.71% / -45.7% | -0.77%* | 9.02% | -4.31pp (-1.42) | +5.47pp* (+2.07) | 3.19 / 5.01, 6.24 / 13.18 | 0.29 / 9.02 | 2 of 9 | 8 of 9* |

\*c's control is degenerate: a top entry (above 75% of the range) hits the
50% exit at once, so 3,894 of 3,920 top trades lasted 1 day and paid 10bp
each time. That "+5.47pp" is mostly turnover cost, not entry edge.

Exit mix, bottom entry:
- a: 31.5% stopped out (-8.28% average), 68.5% time exits (+5.51%, 70% winners).
- b: 45.6% stopped (-8.25%), 16.3% trail/breakeven (+3.54%), 38.1% at the 63-day cap (+13.55%).
- c: 37.2% stopped (-8.26%), 62.8% midpoint (+6.29%, median 12 days).

## Reading it

- The entry signal does show up at its own horizon: with a 21-day time exit,
  buying range bottoms beats buying range tops by +2.0pp a year (+1.16% vs
  +0.63% per trade). That's the same direction and rough size as the
  original +1pp-a-month signal, diluted by stops and empty slots.
- But nothing comes close to SPY. Every exit loses to simply holding the
  index, in both halves, and badly without the megacaps (2.7-3.4% vs 9.0%).
  A per-trade edge of about 0.5% on 4 slots, with an 8% stop hitting a third
  of trades, can't keep up with a 20-year bull market held at 100%.
- The 8% stop is the real tax: 31-46% of trades end at -8.3%. In a
  ranging, low-ADX name, an 8% stop is about the size of the range itself, so
  noise takes out a third of entries before the reversion arrives. (Not
  tested here. It's a candidate question, and on past form it will also fail,
  because a wider stop deepens the drawdown.)
- R4-style trailing turns the entry edge NEGATIVE (bottom loses to top). Letting
  winners run makes this a trend trade, and range-bottom names don't trend.

## Verdict

The standing open question since 9/23 ("an exit that preserves the entry's
edge") gets a clear answer: the edge survives only with a plain time exit,
and even then the strategy loses to SPY by about 3pp a year. The range-regime
signal stays where it was: real, but not something to trade on its own.
Closed. Recorded as the 9th strategy family tested, with the same pattern
as the first eight (no return gain over the index).

## Prediction scorecard

- a: CAGR 5-9%, below SPY: RIGHT (6.16%). Bottom beats top by +1 to +3pp:
  RIGHT (+2.01). Walk-forward vs SPY at most 4/9: WRONG (5/9). Dies: RIGHT.
- b: CAGR 7-11%, the best of three: half (6.87%, just under the band; it IS
  the best on CAGR). Roughly level with SPY: WRONG (-2.15pp). Fails halves
  or megacaps: RIGHT (both). Dies: RIGHT.
- c: worst, CAGR 3-6%: RIGHT (4.71%). Dies: RIGHT.
- No survivor: RIGHT.

## Workers' harness notes

Three independent reads found no look-ahead and no bottom-vs-top asymmetry.
Shared caveats, all symmetric and logged: open positions at window end are
missing from the trade stats (equity is right); halves and windows share one
boundary day; rule exits release their slot one day later than stops; the
naive daily t ignores autocorrelation. The only exposure asymmetry is c's
degenerate control (above).
