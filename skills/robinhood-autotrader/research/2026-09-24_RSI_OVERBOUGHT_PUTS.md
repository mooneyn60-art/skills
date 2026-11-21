# RSI Overbought Puts: Buy Puts When RSI Hits the Top?

One-line: Nolan's idea. Buy puts on stocks (or SPY) when RSI(14) reaches the
top of its range (70+), betting on a pullback.

Last Updated: 2026-09-24
Status: DONE. Not supported. Predictions committed first (1a6ce1f).
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

## Results (script run after the predictions above were committed)

Signal = first day RSI(14) crosses the threshold. Baseline = every day's
forward return for the same names. Put model: ATM 30-day put, IV = 20-day
realized vol x 1.1. That is CHEAPER than real puts (skew makes real puts
pricier), so every put number below is optimistic for the put buyer.

A. 14 large caps, stock RSI >= 70 (n=1478)
   fwd 5d  -0.01pp vs baseline, t=-0.08
   fwd 21d +0.23pp vs baseline, t=+1.01  (stocks went UP slightly MORE)
   both halves positive (+1.64% / +1.37% per 21d)
   put held to expiry: mean -12% of premium, median -100%, 27% win rate
A. RSI >= 80 (n=219): fwd 21d -0.06pp, t=-0.09. Nothing. Put mean -6%.

B. SPY RSI >= 70 (n=119): fwd 21d +0.15pp, t=+0.66. Put mean -61%, 16% win.
B. SPY RSI >= 75 (n=40): a real short dip, fwd 5d -0.51pp t=-2.37,
   10d -0.56pp t=-2.10, gone by 21d (t=-1.52). A put held 5 days then sold,
   less a 3% spread: +2.1% mean, t=+0.27, 42% win rate. Breakeven at best,
   on 40 events, the best of four variants tried (multiple testing).

## Verdict

P1 CONFIRMED: overbought large caps don't reverse. In a bull market RSI 70
    is what strength looks like, and strength keeps going.
P2 CONFIRMED at 70. PARTLY WRONG at 75: SPY does dip for about a week, but it
    is small (half a percent).
P3 CONFIRMED: no variant clears the cost of the put.
P4 NOT CONFIRMED: RSI 80 is no better than 70 on single stocks.

The one live thread: SPY RSI >= 75 -> a short-dated SPY put for a few days.
It breaks even in a model that flatters puts. Not tradeable. Worth
re-testing only with real historical option prices, not a model.

Why it fails (the mechanism): RSI measures how one-sided recent moves were,
not whether the price is wrong. A put has to be right on direction, size AND
timing, and pays time decay the whole while. A tiny statistical dip can't
cover that.
