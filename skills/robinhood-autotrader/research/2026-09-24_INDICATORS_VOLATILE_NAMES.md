# Chart Indicators on Volatile Growth Stocks

One-line: every indicator test so far used blue chips. Nolan trades SOFI-type
names. Do the same indicators behave differently on volatile growth stocks?

Last Updated: 2026-09-24
Status: IN PROGRESS. Predictions committed before any test runs (R14.1, R16.2).
Audience: Nolan, TARS sessions

## Overview

Same indicators and settings as 2026-09-24_INDICATORS_PRICE.md (MACD 12/26/9,
RSI 14, Bollinger 20/2, SMA 50, SMA 200, EMA 9), on higher-volatility growth
names pulled read-only from Robinhood. Many of these listed recently, so
histories are short and uneven. Survivorship is WORSE here than in the
large-cap set: names that crashed and delisted aren't in the data. That
flatters buy-and-hold, and it flatters "buy the dip" signals most of all.
R16 trigger (c) is ON in the writing session. Nothing adopted before the
weekend re-read.

## Predictions (written before the test)

P4 TREND SYSTEMS (SMA 50/200 long/flat): on volatile names they cut the max
   drawdown by much more than on blue chips (those names fall 70-90%), and
   come CLOSER to buy-and-hold on Sharpe than on blue chips. Some names beat
   buy-and-hold on Sharpe. Still not most of them.
P5 OSCILLATOR SYSTEMS (RSI 30/70, Bollinger lower-band buy): still lose to
   buy-and-hold, and fail worse than on blue chips, because "oversold" keeps
   getting more oversold on names in a real downtrend.
P6 EVENTS: no event signal survives multiple testing in both halves.

What would prove me wrong: any indicator system beating buy-and-hold on
Sharpe in a MAJORITY of the volatile names, in both halves of each name's
own history.
