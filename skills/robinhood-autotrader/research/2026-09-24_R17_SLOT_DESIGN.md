# R17 Slot Design: Bracket vs Hold, and Which Contracts Lose Least

One-line: R17 is live. Does Nolan's bracket (-20% stop, +25% ratchet) help or
hurt 60+ DTE calls, and which expiry and delta lose the least?

Last Updated: 2026-09-24
Status: IN PROGRESS. Predictions committed before any test runs (R14.1, R16.2).
Audience: Nolan, TARS sessions

## Overview

R16 trigger (c) is ON in the session that wrote this (the RSI test refuted
one of TARS's stated predictions). Under R16.3, nothing here is adopted
before the weekend re-read, whatever it finds.

Method: simulated option prices (Black-Scholes) on real daily stock paths,
paper/history/daily_stocks.json, 14 large caps, 2006-2026. IV = trailing
20-day realized vol x 1.15 (a volatility premium; real options are richer
than realized on average), plus a round-trip spread cost. The model has no
skew and no earnings IV crush, so absolute returns are only a rough guide.
The COMPARISONS between exits on the SAME paths are the point.
Survivorship: the universe is 2026's winners. That flatters calls.

## Predictions (written before the test)

P1 BRACKET vs HOLD: on the same paths, Nolan's bracket has a LOWER mean
   return per trade than holding to the 21-DTE time exit. A 60+ DTE option
   moves about 3x the stock in percent, so a -20% stop gets hit by ordinary
   noise, about a 6-7% stock dip. The bracket cuts the worst losses (stopped
   trades average near -25%, not -100%) but costs more in mean than it
   saves. Expect the bracket's win rate to be HIGHER, with smaller wins.
P2 EXPIRY: per trade, 120-180 DTE loses less to decay than 60 DTE and has a
   better mean return.
P3 DELTA: delta 0.50-0.60 has a better mean return per dollar than 0.30
   (less paid for lottery odds), once the volatility premium is priced in.
P4 TREND FILTER: buying calls only when the stock is above its 200-day
   changes the mean by less than the bracket-vs-hold difference.

What would prove P1 wrong: the bracket beats hold-to-time-exit on mean
return by 2pp+ per trade with t > 2, in both halves of the sample.
