# Sentiment: Does the Put/Call Ratio Add Anything VIX Doesn't?

One-line: RESEARCH_AGENDA item 13. When option traders buy unusually many
puts (fear), does the market do better next month, and is that information
VIX doesn't already carry?

Last Updated: 2026-10-04
Status: DONE. Prediction committed first (3c25e86) and held. Nothing beyond VIX that clears the bar.
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

## Answer first

- FOR VOLATILITY, THE PUT/CALL RATIO IS JUST VIX AGAIN. On its own it
  predicts a rougher next month (t = +5.29). With VIX in the regression its
  t drops to +0.51 (VIX t = +9.08). It adds nothing.
- FOR RETURNS, THERE'S A FAINT CONTRARIAN SIGN AND NO MORE. Heavy put
  buying comes before slightly better months: t = +1.28 with VIX, positive
  in 7 of 9 windows, t = +2.07 when 2008 is left out. That's the direction
  the mechanism predicts, but at 155 months it's far below the |t| >= 3.9
  hurdle (item 8), and both halves on their own are under t = 1.
- Gaps, stated so they aren't mistaken for "no effect": the AAII survey
  (download blocked) and short interest (no free history) were not tested.
  The P/C data stops in October 2019.

## Result

Script: paper/test_sentiment_putcall.py. 155 months, 2006-12 to 2019-10;
10-day average equity P/C 0.50 to 0.86 (mean 0.65).

                       forward return                    forward volatility
                       P/C alone    P/C (+VIX)           P/C alone    P/C (+VIX)   VIX t
    full               t=+1.14      t=+1.28              t=+5.29      t=+0.51      +9.08
    first half         t=+0.29      t=+0.41              t=+3.98      t=+0.85      +6.09
    second half        t=+2.25      t=+0.82              t=+1.93      t=+0.34      +1.97
    without 2008       t=+2.51      t=+2.07              t=+3.67      t=-0.02      +9.35
    9 windows (+VIX)   + - + + + + - + +                 - + - - + - + - +

## Scored against the prediction

    S1 P/C alone positive, |t| < 2: RIGHT (+1.14). With VIX |t| < 1.5: RIGHT (1.28).
    S2 P/C alone predicts vol |t| > 2: RIGHT (5.29). With VIX below 2: RIGHT (0.51).
    "Nothing beyond VIX": RIGHT for volatility; for returns a weak contrarian
    sign that doesn't reach any significance bar.

R16 trigger (c) not triggered by this test. (R16 is on anyway via trigger
(a): 4 consecutive TARS losing closes.)

## For TARS (interpretation)

Nothing to add to the rules. If sentiment is ever revisited, the cheapest
next step is the AAII survey through another source, tested the same way
and against the same VIX control. The put/call ratio is a VIX proxy for
risk, and at best a weak contrarian nudge for returns.
