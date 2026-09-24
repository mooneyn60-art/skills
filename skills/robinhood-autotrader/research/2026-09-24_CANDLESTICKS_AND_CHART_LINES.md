# Candlesticks and Chart Lines: Can They Call a Breakout or a Breakdown?

One-line: RESEARCH_AGENDA item 23, Nolan's request ("how to read candles and
lines to see how the stock is going to break or boom"). Do classic
candlestick patterns and support/resistance breaks predict the next move?

Last Updated: 2026-09-24
Status: IN PROGRESS. Predictions committed before any test runs (R14.1, R16.2).
Audience: Nolan, TARS sessions

## Overview

R16 trigger (c) is ON in the session that wrote this. Nothing here is
adopted before the weekend re-read.

Data: paper/history/daily_stocks.json, 14 large caps + SPY, daily OHLC,
2006-2026. Survivorship: 2026's winners. Forward returns measured against
the same names' unconditional baseline. Every pattern tested counts toward
multiple testing; the count is reported.

Patterns: hammer, shooting star, bullish/bearish engulfing, doji, morning
star, evening star, three white soldiers, three black crows. Lines:
breakout above the 60-day and 252-day high ("boom"), breakdown below the
60-day low ("break"), bounce off a prior 60-day swing low, and a
volume-free version of each (no volume data stored).

## Predictions (written before the test)

P1 CANDLESTICKS: no single or multi-bar candlestick pattern has a forward
   5 or 10-day edge that survives multiple testing AND holds in both halves
   of the sample. Most will show |t| < 2. At most one or two cross t = 2 by
   chance, and they won't replicate in the other half.
P2 BREAKOUTS ("boom"): new 252-day highs are followed by slightly
   ABOVE-baseline returns (the 52-week-high effect, George & Hwang 2004).
   Small: under 1pp over 21 days.
P3 BREAKDOWNS: new 60-day lows are followed by below-baseline returns when
   VIX is calm (< 20) and above-baseline when VIX >= 25. That's the R15
   finding again, from a different angle.
P4 SUPPORT BOUNCES: no edge.

What would prove P1 wrong: any candlestick pattern with a forward edge of
|t| > 3 in BOTH halves of the sample.
