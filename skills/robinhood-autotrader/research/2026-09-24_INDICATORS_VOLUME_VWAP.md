# Chart Indicators, Part 2: Volume and VWAP

One-line: the two indicators on Nolan's chart that need volume data, which
this repo didn't have until now.

Last Updated: 2026-09-24
Status: IN PROGRESS. Predictions committed before any test runs (R14.1, R16.2).
Audience: Nolan, TARS sessions

## Overview

New data pulled read-only from Robinhood historicals: daily OHLCV for the
same 14 large caps + SPY, 2006-2026, plus intraday bars for VWAP on a small
set of names over a recent window. VWAP is a within-day measure (the average
price paid today, weighted by volume). Day traders and execution desks use
it. This account holds for weeks, so VWAP is tested for what it could tell
a swing trader.
R16 trigger (c) is ON in the writing session. Nothing adopted before the
weekend re-read. Survivorship: 2026's winners.

## Predictions (written before the test)

P1 VOLUME SPIKES: days with volume at least 2x the 20-day average are
   followed by slightly ABOVE-baseline returns over the next 21 days,
   whichever way the price moved that day (the high-volume return premium,
   Gervais, Kaniel & Mingelgrin 2001). Small: under 1pp.
P2 VOLUME-CONFIRMED BREAKOUTS: a 60-day-high breakout on 1.5x+ volume does
   NOT do meaningfully better than one on normal volume. The candlestick
   study found 60-day breakouts had no edge; volume won't rescue them.
P3 VWAP: closing above vs below the day's VWAP does not predict the next
   day's or next week's return on large caps. It's an execution benchmark,
   not a forecast.
P4 VOLUME ON DOWN DAYS: heavy-volume selloffs in calm markets are followed
   by below-baseline returns; in stressed markets (VIX >= 25), above.

What would prove me wrong: any volume or VWAP signal with |t| > 3 in both
halves of the sample (or both halves of the intraday window for VWAP).
