# My Own Calibration: How Good Were Today's Written Predictions?

One-line: RESEARCH_AGENDA item 7, applied to TARS itself. Every test today
had its predictions committed before it ran. Scoring them shows where TARS's
judgment can be trusted and where it can't.

Last Updated: 2026-09-24
Status: DONE. Scored from the Verdict sections of 7 notes written today in
the main session (27 predictions). Batch-1 notes (runner session) are
excluded because their predictions were structured differently.
Audience: Nolan, TARS sessions

## Overview

A prediction was scored CONFIRMED, PARTLY or REFUTED as its own note judged
it. Then each prediction was sorted into one of two kinds:
- NULL: "this has no edge / doesn't beat holding / doesn't predict"
- EFFECT: "this has an edge / a direction / beats something"

## The score

  All 27:          11 confirmed, 12 partly, 4 refuted

  NULL (10):       10 confirmed, 0 partly, 0 refuted
  EFFECT (17):      1 confirmed, 12 partly, 4 refuted

  NULL predictions: RSI>70 no reversal, puts don't clear cost, candlesticks,
  support bounces, MACD, SMA50, EMA9, volume-confirmed breakouts, VWAP,
  volatile-name events.
  EFFECT predictions, with the one confirmed: longer expiries lose less
  (R17 P2). The four refuted: RSI 80 better than 70; the 52-week-high
  breakout premium; the high-volume return premium; delta 0.5-0.6 beating
  0.30 (likely a model artifact).

## What it means

1. WHEN TARS SAYS "THIS DOESN'T WORK", IT HAS BEEN RIGHT 10 OUT OF 10 TODAY.
   Skepticism is well calibrated.
2. WHEN TARS SAYS "THIS HAS AN EDGE", IT HAS BEEN RIGHT 1 TIME OUT OF 17.
   Positive calls are badly overconfident.
3. Two of the four outright misses were published academic anomalies (the
   52-week-high effect, the high-volume premium). TARS trusted the
   literature, and our data didn't show it. That matches the decay research
   (research/2026-09-24_DOES_THE_PAST_STILL_APPLY.md): published effects
   lose ~58% after publication.
4. THE UNCOMFORTABLE ONE: TARS predicted the VIX-regime pattern (R15's
   idea) five times today, in RSI<30, lower Bollinger band, 60-day lows,
   heavy-volume selloffs and pooled panic dips. It came back "directionally
   right, not significant" all five times, and those five were mostly the
   same crash days. R15 was adopted on a t=8.46 result from a different
   test. Today's evidence doesn't refute it, but it doesn't strengthen it
   either, and TARS's own positive predictions are the ones that keep
   failing. Recommendation for the weekend re-read: treat R15 as an
   experiment on probation, and keep its 8% hard stop exactly as is.

## Rule of thumb going forward

Discount TARS's "this works" by a lot. Trust TARS's "this doesn't" more.
The same standard applies to Nolan's gut calls, which is why they're
scored, not argued.

## Limits

One day, 27 predictions, one scorer (TARS scoring TARS, from its own
agents' verdicts). "Partly" is a judgment call. The NULL/EFFECT sorting was
done after the fact.
