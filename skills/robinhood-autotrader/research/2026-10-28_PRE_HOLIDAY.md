# The Day Before a Market Holiday: Still Special?

One-line: The day before a market holiday is a little better than an ordinary
day (SPY up 61% vs about 54%, +0.09pp a day), in both decades and both
universes, but at t=1.3 it's a lean, not an edge.

Last Updated: 2026-10-28
Status: DONE. A small, consistent lean, not an edge: SPY +0.125% on pre-holiday days vs +0.039% otherwise (diff t=+1.29, n=193), positive in both halves and 7 of 9 windows. No sign of decay. Fails |t| >= 2. Prediction committed first (baacc99).
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

## Results (python3 paper/research_scripts/pre_holiday.py, data 2006-01-03 to 2026-10-22)

193 pre-holiday days found automatically (about 9 a year, which matches the
NYSE calendar; includes Good Friday eves, the 2012 Sandy closures and
national days of mourning). In-sample, mechanical, nothing fitted.

| Series | Cut | Pre-holiday mean (n) | Up % | Other mean | Diff | t |
|---|---|---|---|---|---|---|
| SPY close-to-close | full | +0.125% (193) | 61% | +0.039% | +0.086pp | **+1.29** |
| | 2006-2015 | +0.117% (91) | 56% | +0.025% | +0.092pp | +0.84 |
| | 2016-2026 | +0.132% (102) | 65% | +0.052% | +0.081pp | +1.01 |
| SPY open-to-close | full | +0.080% | 56% | +0.014% | +0.066pp | +1.13 |
| | 2006-2015 | +0.105% | 56% | +0.006% | +0.099pp | +1.02 |
| | 2016-2026 | +0.057% | 56% | +0.022% | +0.035pp | +0.52 |
| 9 non-megacap names | full | +0.133% | 59% | +0.028% | +0.105pp | +1.13 |
| | 2006-2015 | +0.156% | 57% | +0.021% | +0.135pp | +0.81 |
| | 2016-2026 | +0.113% | 60% | +0.035% | +0.078pp | +0.81 |

Walk-forward (pre minus other, 9 windows of about 21 holidays each): SPY
close-to-close positive in **7 of 9**, SPY session 8 of 9, non-megacap
basket 5 of 9.

## Reading it

- Direction is consistent: positive in both halves, both universes and
  most windows, and the up-rate is higher (61% vs about 54% on an ordinary
  day). That's what the literature reports.
- But it's small: +0.09pp a day, about $0.65 on SPY at 770, and t=1.3 on
  20 years. It never clears |t| >= 2 in any cut.
- No post-publication decay shows up in this window: the 2016-26 SPY gap
  (+0.081pp) is about the same as 2006-15 (+0.092pp). The session-only part
  did shrink (+0.099 -> +0.035pp), so what's left of the effect sits more in
  the overnight gap into the day than in the session Nolan trades.
- For 0DTE options it's far smaller than the bid-ask spread. Useful only as
  a context line on the desk ("pre-holiday: mild up-lean"), the same tier as
  the Nikkei lean. Next ones: Wed 11/25 (before Thanksgiving) and Thu 12/24.

## Prediction scorecard

- SPY pre-holiday mean +0.05 to +0.15%: RIGHT (+0.125%).
- Diff t 0.5 to 2.0: RIGHT (+1.29).
- Weaker in 2016-2026: **WRONG** for close-to-close (about equal; the recent
  up-rate is actually higher), right for open-to-close only.
- 5-7 of 9 windows positive: RIGHT (7).
- Non-megacap basket t < 2: RIGHT (+1.13).
- Nothing usable as a rule, a lean at best: RIGHT.
