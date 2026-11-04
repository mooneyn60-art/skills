# Quarter-End Window Dressing: Do Winners Get a Push Before the Quarter Closes?

One-line: Wednesday contrarian probe. Do the quarter's winners beat its
losers in the last 5 trading days of a quarter, and give it back in the first
5 days of the next? Calendar structure, never tested here.

Last Updated: 2026-11-04
Status: DESIGN + PREDICTION (committed before the first run). Results below once run.
Audience: Nolan, TARS sessions

## Mechanism (written before the test)

Fund managers report holdings at quarter-end. To look smart, some buy the
quarter's winners and dump its losers just before the snapshot ("window
dressing", Lakonishok, Shleifer, Thaler & Vishny 1991 AER P&P; Ng & Wang
2004 JF, mostly small caps). That buying lifts winners late in the quarter,
and the effect should reverse once the snapshot is taken. Against: our
names are mega and large caps, where window dressing is a rounding error,
and the effect is old and published.

## Test (fixed before running)

- Universes: LONG = paper/history/daily_ohlcv.json, 14 names 2006-2026
  (about 82 quarter-ends); WIDE = LONG + volatile + holdings (41 names,
  2021-2026, about 20 quarter-ends; names enter once they have data).
- At the close 6 trading days before the last trading day of each calendar
  quarter: rank names by quarter-to-date return (from the last close of the
  previous quarter). Winners = top third, losers = bottom third.
- Outcome A (dressing): winners minus losers, equal weight, over the last 5
  trading days of the quarter.
- Outcome B (reversal): the same groups over the first 5 trading days of the
  next quarter.
- Placebo: the same construction at the end of the 1st and 2nd months of
  each quarter (no reporting date), to see whether it's just short-term
  momentum or reversal.
- Hurdles: split halves; 9 consecutive windows of quarters; drop the
  megacaps; t on per-quarter spreads (one observation per quarter, no overlap).

## PREDICTION

- A: winners minus losers in the last 5 days = 0 +/- 0.4pp, |t| < 1.5 on LONG.
- B: no reliable reversal, |t| < 1.5.
- Placebo similar in size to A (whatever shows up isn't about the quarter-end).
- Nothing usable. These are large caps.
