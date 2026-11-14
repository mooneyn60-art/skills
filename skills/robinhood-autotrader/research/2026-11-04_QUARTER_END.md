# Quarter-End Window Dressing: Do Winners Get a Push Before the Quarter Closes?

One-line: No window dressing in our names. Quarter winners don't pull ahead
of losers in the final 5 days (+0.19pp, t=0.57) and don't reverse after.
Ordinary month-ends look the same. Large caps are too big to be dressed.

Last Updated: 2026-11-04
Status: DONE. Dead: winners minus losers in the last 5 days +0.19pp, t=+0.57 (n=82 quarters); no reversal (t=+0.48); placebo month-ends no different. Prediction committed first (6a25512); all lines right.
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

## Results (python3 paper/research_scripts/quarter_end.py)

One observation per quarter (no overlap), winners/losers = top/bottom third
by quarter-to-date return at the close 5 sessions before quarter-end.
In-sample, mechanical, price returns.

| Cut | A: last 5 days, winners - losers | t | B: first 5 days after | t |
|---|---|---|---|---|
| LONG 14 names, 82 quarters | +0.186pp | +0.57 | +0.184pp | +0.48 |
| 1st half (41) | +0.462pp | +0.96 | +0.074pp | +0.12 |
| 2nd half (41) | -0.091pp | -0.20 | +0.293pp | +0.61 |
| No megacaps | +0.340pp | +1.35 | -0.371pp | -1.00 |
| PLACEBO: non-quarter month-ends (164) | -0.223pp | -0.61 | +0.360pp | +1.26 |
| WIDE 41 names (82 quarters*) | +0.320pp | +0.75 | -0.342pp | -0.53 |
| WIDE no megacaps | +0.337pp | +0.66 | -0.507pp | -0.70 |

\*WIDE spans 2006-2026 too: before 2021 it's the same 14 names; the
volatile and holdings names join as their data starts.

9 windows (LONG): A positive in 4 of 9, B positive in 5 of 9.

## Reading it

- Nothing at quarter-end. The largest number, no-megacaps A at t=+1.35, has
  the shape the theory predicts (a push before, a giveback after, -0.37pp, t=-1.00),
  but neither clears t 2 and the first-half value isn't repeated in the second.
- The placebo month-ends do no better or worse, so whatever wobble exists
  is ordinary short-horizon noise, not reporting dates.
- Fits the literature: window dressing is a small-cap phenomenon (Ng & Wang
  2004), and the names here are among the largest companies in the world.
- For Nolan: no reason to time anything around quarter-ends. Next one: 12/31.

## Prediction scorecard

- A = 0 +/- 0.4pp, |t| < 1.5 on LONG: RIGHT (+0.186pp, t=+0.57).
- B no reliable reversal, |t| < 1.5: RIGHT (t=+0.48).
- Placebo similar in size: RIGHT (-0.22 / +0.36pp).
- Nothing usable: RIGHT.
