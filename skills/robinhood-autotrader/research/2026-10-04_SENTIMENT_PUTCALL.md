# Sentiment: Does the Put/Call Ratio Add Anything VIX Doesn't?

One-line: RESEARCH_AGENDA item 13. When option traders buy unusually many
puts (fear), does the market do better next month, and is that information
VIX doesn't already carry?

Last Updated: 2026-10-04
Status: PREDICTION COMMITTED, TESTS NOT YET RUN
Audience: Nolan, TARS sessions

## Scope and data

- CBOE EQUITY put/call ratio, daily, 2006-11 to 2019-10 (CBOE's free
  history file; cdn.cboe.com volume_and_call_put_ratios/equitypc.csv,
  saved as paper/history/cboe_equity_putcall.csv). Equity-only P/C is the
  usual retail-sentiment gauge; index P/C is dominated by hedging.
- Not tested, and why: AAII sentiment survey (download blocked, 403);
  short interest (no free point-in-time history for our names). Recorded
  as gaps, not as "no effect".
- SPY from daily_stocks.json; VIX from vix_weekly.json (value dated >= 7
  days earlier).

## Mechanism (stated before the test)

Contrarian sentiment: crowds buy puts after falls, near bottoms, and calls
near tops, so high P/C should precede better returns. But VIX also spikes
when fear spikes, so P/C may simply repeat what VIX says.

## Test (fixed before running)

First trading day of each month; signal = 10-day average equity P/C ending
the PRIOR trading day; outcome = SPY forward 21 trading days.
S1  forward RETURN on P/C alone, then on P/C + VIX: P/C coefficient and t.
S2  forward realised VOLATILITY, same two regressions.
Hurdles for the P/C coefficient with VIX: split halves, 9-window signs,
drop 2008. Adoption would need |t| >= 3.9 (item 8); R16 is on, so nothing
is adopted this session regardless.

## PREDICTION

S1: P/C alone positive (contrarian) but |t| < 2; with VIX, |t| < 1.5.
S2: P/C alone predicts higher volatility (|t| > 2); with VIX, P/C's t
    falls below 2.
Verdict expected: nothing beyond VIX. A clean "no".

## Result

(not yet run)
