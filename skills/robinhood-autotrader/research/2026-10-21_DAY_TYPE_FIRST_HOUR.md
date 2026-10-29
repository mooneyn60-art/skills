# Day Type: Does the First Hour Tell You Trend or Chop?

One-line: A clean one-way first hour is followed by a slightly more trending
rest of day (E2 0.47 vs 0.41), with the right sign in 8 of 9 windows, but
t=+1.66 and fading in the recent half. It says nothing about direction.

Last Updated: 2026-10-21
Status: DONE. Weak and not usable: ER1 -> E2 corr +0.13, t=+1.66 (n=167), sign positive in 8 of 9 windows, but only t=+0.58 in the second half. No continuation signal. Re-test when the 5-min history doubles. Prediction committed first (9b5a755).
Audience: Nolan, TARS sessions

## Overview

research/2026-10-15_OWNER_OPTIONS_REPLAY.md found that Nolan's money
depends on day type: wide stops and hold-to-close pay only on trend days.
It asked whether the first 60-90 minutes can tell which kind of day it is.
Not a moving average, momentum ranking or price channel. It's about path
shape, which the probe rules allow.

## Mechanism (written before the test)

When real information arrives before or at the open (news, a big order to
work), it gets traded in one direction for hours. The early path is then
one-way (high efficiency), and the rest of the day keeps moving rather than
mean-reverting. On days with no information, the open is noise and the day
chops. Against: by 10:30 most of the day's range is already in (42% by 10:00,
KNOWLEDGE.md), so the early move may use up the trend rather than signal it.

## Test (fixed before running)

- Data: paper/history/spy_5min.json, Robinhood regular-session 5-min bars,
  2026-02-23 onward (about 167 sessions; real bars only from Feb 23). Times
  are UTC in the file; the 9:30 ET bar is 13:30 or 14:30 UTC depending on DST,
  so each day is cut by bar order (first 12 bars = first hour).
- Predictor ER1 = |close at 10:30 - open| / sum of |5-min close changes| in
  the first hour (1 = straight line, near 0 = round trip).
- Outcome 1 (day type) E2 = |close(16:00) - close(10:30)| / (high - low of
  10:30-16:00). Trend days are high, chop days low.
- Outcome 2 (secondary) continuation: does 10:30-16:00 move in the same
  direction as the first hour? Hit rate and t on the signed rest-of-day
  move times the first-hour sign, split by ER1 tercile.
- Stats: OLS of E2 on ER1 (t), Spearman corr, tercile means of E2.
- Hurdles: split halves by date; 9 consecutive windows (sign of the slope,
  >= 5 of 9 positive); the megacap drop doesn't apply (one symbol), so
  instead: drop the 5 largest-range days, and drop FOMC days
  (fomc_dates.json). Multiple-testing bar for anything used live: |t| >= 3.9.

## PREDICTION

- ER1 -> E2: positive but weak. Correlation 0.05 to 0.15, OLS t between
  0.5 and 2.0. Fails walk-forward (under 5/9 positive).
- Continuation: 50-55% overall; no tercile clears |t| 2.
- Nothing usable as a rule. Answer to question #1: "not from the first hour's
  path."

## Results (python3 paper/research_scripts/day_type_first_hour.py, run 2026-10-21)

167 full sessions, 2026-02-23 to 2026-10-20 (no short days; 5 FOMC days).
Mean ER1 0.30, mean E2 0.45. In-sample, mechanical, nothing fitted.

| Cut | n | slope | t | Pearson | low / mid / high ER1 -> mean E2 |
|---|---|---|---|---|---|
| Full | 167 | +0.145 | **+1.66** | +0.128 | 0.410 / 0.457 / 0.474 |
| 1st half (to 06-22) | 83 | +0.320 | +2.14 | +0.231 | 0.391 / 0.501 / 0.507 |
| 2nd half | 84 | +0.060 | +0.58 | +0.064 | 0.425 / 0.431 / 0.428 |
| Drop 5 widest days | 162 | +0.161 | +1.85 | +0.144 | 0.407 / 0.438 / 0.490 |
| Drop FOMC days | 162 | +0.154 | +1.74 | +0.136 | 0.402 / 0.452 / 0.486 |

- Walk-forward, sign of the slope in 9 windows of about 18 days:
  **+ + + + - + + + + (8 of 9).**
- Continuation (does 10:30-16:00 go the first hour's way?): 55% / 49% / 58%
  by tercile, all |t| < 0.9. High-minus-low ER1 continuation is positive in
  6 of 9 windows but tiny (+0.04 to +0.84pp, mostly about 0.1). In the second
  half the high-ER1 tercile continued only 43% of the time.

## Reading it

- The day-type effect has a consistent SIGN (8 of 9 windows, both halves
  positive, survives dropping the widest days and FOMC), but it's small
  (high-ER1 days end about 15% more "trendy" than low-ER1 days) and it fails
  the |t| >= 2 bar on the full sample (+1.66). The second half is flat
  (t=+0.58), so the first-half t=+2.14 may be the whole story.
- It says nothing about DIRECTION. A clean first hour doesn't mean the
  rest of the day goes the same way. That's consistent with the earlier
  finding that first-30-minutes -> last-30-minutes momentum flips (KNOWLEDGE).
- Practical: for Nolan, "the first hour was a straight line" is a very weak
  reason to hold for a trend. It's not a filter, and it doesn't change the 10:30
  rule.
- Sample size is the limit: 167 days, and Robinhood's real 5-min history only
  starts in February. This is the one probe worth re-running: by spring 2027
  there will be about 330 days. Flagged in QUESTIONS.md.

## Prediction scorecard

- Correlation 0.05-0.15, t 0.5-2.0: RIGHT (+0.128, t=+1.66).
- Fails walk-forward (< 5/9 positive): **WRONG**. 8 of 9 positive, more
  consistent than I expected for something this weak.
- Continuation 50-55%, no tercile |t| 2: RIGHT (overall about 54%, max |t| 0.84).
- Nothing usable: RIGHT.
