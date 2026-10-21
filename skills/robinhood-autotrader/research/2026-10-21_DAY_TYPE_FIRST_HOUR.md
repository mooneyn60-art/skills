# Day Type: Does the First Hour Tell You Trend or Chop?

One-line: Wednesday contrarian probe. Not direction: the SHAPE of the rest
of the day. If the 9:30-10:30 path is clean and one-way, is the 10:30-16:00
session more likely to trend? (TARS open question #1; Nolan trades after 10:30.)

Last Updated: 2026-10-21
Status: DESIGN + PREDICTION (committed before the first run). Results below once run.
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
