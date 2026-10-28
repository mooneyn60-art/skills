# The Day Before a Market Holiday: Still Special?

One-line: Wednesday contrarian probe. Calendar structure never tested here:
is the last trading day before an NYSE holiday better than an ordinary day,
in SPY and in our 14 names, 2006-2026?

Last Updated: 2026-10-28
Status: DESIGN + PREDICTION (committed before the first run). Results below once run.
Audience: Nolan, TARS sessions

## Overview

Turn-of-month was tested and failed; day of week flips between decades;
monthly-expiry Fridays hold up (KNOWLEDGE). The pre-holiday effect is the
classic calendar anomaly (Lakonishok & Smidt 1988 RFS; Ariel 1990 J. Finance:
pre-holiday returns many times an ordinary day's), and also a classic case
of decay after publication. Neither has been tested here. Not a moving
average, a momentum rank, a volatility measure or a channel.

## Mechanism (written before the test)

Before a long weekend, short sellers close positions to avoid holding risk
over the break, and retail mood is better before holidays. Both push prices
up on the last session. Against: once published, it should be arbitraged
away. Prior: mostly gone since 2006.

## Test (fixed before running)

- Data: paper/history/daily_ohlcv.json (SPY + 14 names, 2006-01 to 2026-10).
- Pre-holiday day: a trading day whose next trading day is more than one
  weekday away (a weekday with no session in between; weekends don't count).
  That captures every NYSE full-day closure with no hand-made list. Half
  days are included as normal sessions.
- Return: close-to-close of the pre-holiday day. Also open-to-close (the
  session itself) for SPY.
- Compare with all other days: difference in means, Welch t.
- Hurdles: split halves (2006-2015 / 2016-2026); 9 consecutive windows
  (pre-holiday minus other mean, >= 5 of 9 positive); drop the megacaps
  (equal-weight average of the 9 non-megacap names instead of SPY);
  |t| >= 2 to be interesting, >= 3.9 to be anything.

## PREDICTION

- SPY pre-holiday mean about +0.05 to +0.15%/day vs about +0.04% otherwise;
  difference t between 0.5 and 2.0 (n about 180 days).
- Weaker in 2016-2026 than 2006-2015 (post-publication decay).
- Walk-forward: 5-7 of 9 positive (direction persists but is noisy).
- Non-megacap basket: similar, t < 2.
- Nothing usable as a rule. At best a "lean" for the desk.
