# Chart Indicators, Part 1: MACD, RSI, Bollinger Bands, SMA(50), EMA(9)

One-line: Nolan asked to test every indicator on his Robinhood chart. Do the
price-based ones predict anything, and do they beat buy-and-hold when you
trade them?

Last Updated: 2026-09-24
Status: IN PROGRESS. Predictions committed before any test runs (R14.1, R16.2).
Audience: Nolan, TARS sessions

## Overview

Settings exactly as on Nolan's chart: MACD (12, 26, 9), RSI (14), Bollinger
Bands (20, 2), SMA (50), EMA (9). Data: paper/history/daily_stocks.json,
14 large caps + SPY, 2006-2026. Two tests per indicator: (1) event study,
forward 5/10/21-day returns after each signal vs baseline; (2) where traders
use it as a system, long/flat vs buy-and-hold with costs.
R16 trigger (c) is ON in the writing session. Nothing adopted before the
weekend re-read. Survivorship: 2026's winners.

## Predictions (written before the test)

P1 MACD: signal-line and zero-line crosses have no forward edge that survives
   multiple testing. As a long/flat system it trails buy-and-hold after costs
   (whipsaw), with a smaller max drawdown.
P2 RSI: RSI < 30 depends on the regime. Calm (VIX < 20): no edge or negative.
   Stressed (VIX >= 25): positive. That's R15 again. RSI > 70 reversal is
   already refuted (2026-09-24_RSI_OVERBOUGHT_PUTS.md) and should replicate.
P3 BOLLINGER: close below the lower band behaves like RSI < 30 (depends on
   the regime). Close above the upper band is followed by continuation, not
   reversal. Squeeze-then-breakout: no edge.
P4 SMA(50): as a long/flat filter it cuts drawdown but trails buy-and-hold
   in return, and whipsaws more than the 200-day. The 50/200 golden and
   death crosses have no forward edge at the cross.
P5 EMA(9): too fast. A price/EMA9 crossover system loses to buy-and-hold
   after costs by a wide margin, because it trades constantly.

What would prove me wrong: any indicator system beating buy-and-hold on
risk-adjusted return (Sharpe) in BOTH halves after costs, or any event
signal with |t| > 3 in both halves.
