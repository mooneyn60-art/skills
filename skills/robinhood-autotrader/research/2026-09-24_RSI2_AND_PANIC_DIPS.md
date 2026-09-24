# RSI(2) "Buy the Dip in an Uptrend", and a Pooled Test of Panic Dips

One-line: the best-documented indicator strategy (Connors RSI(2)), tested for
decay since publication, plus one pooled test of the "oversold only works in
a panic" pattern that four separate studies hinted at.

Last Updated: 2026-09-24
Status: IN PROGRESS. Predictions committed before any test runs (R14.1, R16.2).
Audience: Nolan, TARS sessions

## Overview

RSI(2) rule (Connors & Alvarez, "Short Term Trading Strategies That Work",
2008): price above its 200-day SMA, RSI(2) closes below 10 -> buy next open;
sell when the close is above the 5-day SMA. Published 2008, so 2009-2026 is
out of sample for the original authors.
Pooled panic test: the RSI < 30, lower-Bollinger-Band, new-60-day-low and
heavy-volume-selloff results each leaned positive at VIX >= 25 without being
significant. Signals on the same dates aren't independent, so the pooled
test must cluster by date.
Data: paper/history/daily_ohlcv.json (15 symbols, 2006-2026) and
vix_weekly.json. R16 trigger (c) is ON in the writing session. Nothing
adopted before the weekend re-read. Survivorship: 2026's winners.

## Predictions (written before the test)

P1 RSI(2) on SPY: a high win rate (60-75%) and a positive average trade. As a
   system it trails buy-and-hold on CAGR (invested only ~15-30% of the time),
   with a Sharpe near or above buy-and-hold's. The edge is smaller in
   2016-2026 than 2006-2015 (published patterns decay).
P2 RSI(2) on single large caps: weaker than on SPY. Index-level mean
   reversion is the documented version; single stocks carry news risk.
P3 POOLED PANIC DIPS: directionally positive at VIX >= 25. Once signals are
   clustered by date, the t-stat stays below 3. Four weak results pointing
   the same way are less than they look, because they are mostly the same
   days.

What would prove P1 wrong: RSI(2) on SPY beating buy-and-hold on BOTH CAGR
and Sharpe in the 2016-2026 half, after costs.
