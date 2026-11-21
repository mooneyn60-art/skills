# The Account's Own Record: When Does This Account Lose Money?

One-line: RESEARCH_AGENDA item 6. Slice the live account's closed trades
by owner, instrument, holding time, entry time, exit type, market backdrop
and R16 streak state, and see whether any slice stands out.

Last Updated: 2026-09-25
Status: DONE. Prediction committed first (5ddc2ee). Nothing separates yet.
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

## Answer first

NOTHING STANDS OUT YET, AND NOTHING COULD. The whole live record is 23
closed trades in 8 trading days, averaging -0.10R. Every slice has
|t| < 1.5. The one visible pattern is that each slice is dominated by one
or two trades: the best slice ("round trips under an hour", +0.14R) is
almost entirely the +2.00R F call held 19 minutes.

What the record does show, descriptively:
- The account's trades so far are mostly Nolan's (17 of 23), mostly short
  (9 closed within an hour), and discretionary (20 of 23 exits).
- R16's first real test: trades opened during the 2026-09-14 to 09-17
  losing streak averaged -0.12R against -0.08R otherwise (n=11 vs 12,
  t=-0.18). No sign that decisions got worse during the streak, but also
  nothing close to enough data to say they didn't. R16 stays until item
  6 can measure it properly (the rule says 20+ streak-period decisions).

## Result

Script: paper/test_account_record.py. 23 trades, 2026-09-10 to 2026-09-21.

    slice                                  side A              side B              t
    A1 owner              TARS  n=6  -0.41R       Nolan  n=17 +0.01R    -1.28
    A1 instrument         option n=12 -0.08R      equity n=11 -0.12R    +0.14
    A2 holding time       <1h   n=9  +0.14R       >=1h   n=14 -0.25R    +1.44
    A3 entry time         1st hour n=10 -0.13R    later  n=13 -0.07R    -0.21
    A4 exit type          rule  n=3  -0.54R       discr. n=20 -0.03R    -0.75
    A5 R16 streak         during n=11 -0.12R      not    n=12 -0.08R    -0.18
    A6 prior SPY day      down  n=15 -0.03R       up     n=8  -0.23R    +0.91

The streak window (2026-09-14 14:09 to 09-17 13:32 UTC) is taken from
paper/pressure_state.py's list: from the third consecutive TARS loss to the
TENB win.

## Scored against the prediction

    all slices |t| < 2: RIGHT.
    options worse than equity: WRONG (about equal).
    sub-hour round trips worse: WRONG (better, because of one trade).
    discretionary exits near zero: RIGHT (-0.03R).
    A5 untestable (too few on one side): WRONG, both sides had 11-12.

## What to do with this

Re-run paper/test_account_record.py at each monthly audit. The slices are
fixed now, so they can't be picked after the fact. Take nothing from them
before ~100 trades (item 18: ~124 at the backtest's edge). The most useful
thing this item did is lock the definitions in place before the data
arrives.
