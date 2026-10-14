# Dispersion: Does How Far Apart the Names Move Predict Anything?

One-line: Wednesday contrarian probe. Not the level of returns or volatility,
but their SPREAD across the 14 names. Does it predict the market, its
volatility, or whether TARS's 200-day selection pays?

Last Updated: 2026-10-14
Status: DESIGN + PREDICTION (committed before the first run). Results below once run.
Audience: Nolan, TARS sessions

## Overview

The research agenda (items 1-24) is complete, so the Wednesday probe is free
to choose. Dispersion has never been tested here (grep of research/: only an
incidental mention). It is not a moving average, a momentum ranking or a
price channel. It is close to a volatility measure, which is why every test
below controls for VIX.

## Mechanism (written before the test)

High dispersion means the names are moving on their own news rather than
together. Two published claims (from memory, being checked by a sub-agent,
UNVERIFIED until then):
1. Dispersion is a proxy for idiosyncratic risk and uncertainty, so it
   predicts higher future market volatility (Stivers 2003 and successors).
2. Lagged high dispersion is followed by a WEAKER momentum premium (Stivers &
   Sun 2010). TARS's 200-day gate is a trend/momentum filter, so if this
   holds, the gap between names above and below their 200-day should shrink
   after high-dispersion months. That would be a reason to size down.

## Test (fixed before running)

- Data: paper/history/daily_stocks.json (14 names + SPY, 2006-2026),
  vix_weekly.json (value dated at least 7 days before, as in item 11).
- Monthly samples, first trading day. Signal D = mean over the prior 21
  trading days of the cross-sectional standard deviation of the 14 daily
  log returns.
- Outcomes over the next 21 trading days:
  (a) SPY return;
  (b) SPY realised volatility (annualised);
  (c) the 200-day spread: mean forward return of names above their 200-day
      SMA minus names below (the same construction as audit Q4).
- OLS of each outcome on D alone, then on D + VIX. Classical t (monthly
  samples don't overlap).
- Hurdles: split halves; sign of the D coefficient (with VIX) across 9
  windows (>= 5/9 the same sign as the full-sample one); drop the megacaps
  (D and the spread recomputed on the 9 non-megacap names);
  multiple-testing bar |t| >= 3.9 for anything that would become a rule.

## PREDICTION

- (a) Market return: nothing. |t| < 2 with VIX, and probably alone too.
- (b) Volatility: D predicts forward vol alone (t > 3), but adding VIX
  absorbs most of it (D's t < 2 with VIX).
- (c) 200-day spread: negative coefficient (high dispersion, weaker trend
  payoff), t between -1 and -2.5. Does NOT clear |t| >= 3.9.
- Overall: nothing becomes a rule.
