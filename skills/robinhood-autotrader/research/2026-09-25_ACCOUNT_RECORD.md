# The Account's Own Record: When Does This Account Lose Money?

One-line: RESEARCH_AGENDA item 6. Slice the live account's closed trades
by owner, instrument, holding time, entry time, exit type, market backdrop
and R16 streak state, and see whether any slice stands out.

Last Updated: 2026-09-25
Status: PREDICTION COMMITTED, TESTS NOT YET RUN
Audience: Nolan, TARS sessions

## Data

paper/trades.jsonl, closed live trades with a recorded planned_risk (so R
can be computed): 23 trades, 2026-09-11 to 2026-09-21 (corrections replace
the rows they correct). SPY daily closes from book_daily.json.

## Slices (only these; fixed before running)

A1 owner (TARS vs Nolan) and instrument (option vs equity)
A2 holding time: under 1 hour vs 1 day or more
A3 entry in the first hour of trading (13:30-14:30 UTC) vs later
A4 exit type: rule-driven (R4 stop/trail, stop_fired) vs discretionary
A5 R16: opened while TARS's losing streak was >= 3 vs not
A6 entered the day after an SPY down day vs up day
Each: n, mean R, Welch t where both sides have n >= 3.

## PREDICTION

Every slice |t| < 2: 23 trades over 8 trading days can't separate
anything. Point estimates I expect: options worse than equity; sub-hour
round trips worse than longer holds; discretionary exits near zero,
rule exits mixed. A5 has too few trades on one side to test. Item 18
already says ~124 trades are needed before trade-level results mean
anything; this note is the baseline for that count.

## Result

(not yet run)
