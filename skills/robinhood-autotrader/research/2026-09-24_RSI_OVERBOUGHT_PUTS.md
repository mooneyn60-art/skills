# RSI Overbought Puts: Buy Puts When RSI Hits the Top?

One-line: Nolan's idea. Buy puts on stocks (or SPY) when RSI(14) reaches the
top of its range (70+), betting on a pullback.

Last Updated: 2026-09-24
Status: IN PROGRESS. Predictions committed before any test runs (R14.1).
Audience: Nolan, TARS sessions

## Overview

Two readings of "companies hitting the top of the RSI line on the SPY":
  A. Individual stocks with daily RSI(14) >= 70 -> buy a put on that stock.
  B. SPY's own RSI(14) >= 70 -> buy a SPY put.
Data: paper/history/daily_stocks.json, 14 large caps + SPY, 2006-2026.
Survivorship bias: that universe was picked in 2026 and is full of winners,
which biases AGAINST puts. That's a caveat, not an excuse; test it anyway.

## Predictions (written before the test)

P1 (A): forward 5, 10 and 21-day returns after RSI >= 70 are NOT meaningfully
    below the unconditional baseline. Overbought large caps in a bull market
    keep drifting up (momentum), so there is no reversal to sell.
P2 (B): same for SPY. RSI >= 70 on SPY precedes NORMAL-to-positive returns.
P3: even if a small reversal exists, it is smaller than a put's cost.
    A 30-day ATM put costs roughly 0.4 x vol x sqrt(T), about 3-4% of the stock
    for a 30% vol name. The stock has to fall more than that just to break even.
P4: RSI >= 80 (extreme) does better for puts than 70, but n is small.

What would prove me wrong: forward 21-day return after RSI >= 70 at least
2pp below baseline with t < -3, holding in both halves of the sample.
