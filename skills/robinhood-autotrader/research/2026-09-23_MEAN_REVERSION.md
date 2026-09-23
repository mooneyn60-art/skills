# Buy-Low-Sell-High Mean Reversion — Tested and Rejected

One-line: Nolan proposed buying a volatile stock near its low and selling
when it returns to its high, repeating; it loses to buy-and-hold in all
sixteen parameter cells and on four of five single stocks.

Last Updated: 2026-09-23
Status: CLOSED — rejected. DO NOT RE-DERIVE.
Audience: TARS sessions, Nolan

## The proposal, in his words

"Switch to a higher volatility stock that we buy low, let it get back to
its high, sell, wait for it to drop, buy again, rinse and repeat."

This is channel mean reversion. It is the single most intuitive strategy in
retail trading and it deserved a real test rather than an opinion.

## Method

14 symbols, 5,209 daily bars each, 2006-01 to 2026-09, whole shares, 5bp
slippage per side, signals on the close and execution at the next open.
Buy when the close sits within band% of the N-day low; sell when it reaches
within band% of the N-day high. Swept N over 20/60/120/250 and band over
2/5/10/15 percent. Tested with and without an 8% stop, on the five most
volatile names and on all fourteen, as a portfolio and single-symbol.

Volatility ranking (annualised, 20 years) to honour the "high volatility"
premise: C 48.9, NVDA 48.9, BAC 46.1, F 42.4, AMZN 37.8, GE 33.7, AAPL
31.6, GOOGL 30.8, CSCO 28.5, MSFT 27.9, XOM 26.8, IBM 25.4, PFE 23.6,
T 23.2.

## Results

SIXTEEN OF SIXTEEN PARAMETER CELLS LOSE TO BUY-AND-HOLD OF THE SAME 14
STOCKS (22.94% CAGR). Best cell, N=60 band=2%, returns 6.77%. Several
cells are outright negative. This is not a tuning problem.

Single-stock, exactly as proposed: NVDA rule 6.93% vs hold 37.27%; AMZN
12.87% vs 25.35%; BAC -2.48% vs 0.99%; F -5.03% vs 2.56%; C -5.23% vs
-6.18%. Four of five lose outright. The fifth "wins" only by losing less,
both legs negative.

Portfolio version with an 8% stop: 5.71% CAGR, -56.8% drawdown, 1,152
trades. Without a stop: 5.64%, -49.6%, 864 trades. The stop does not
rescue it.

The published short-horizon version (Connors RSI-2: buy RSI(2) below 10
while above the 200-day, sell above 70) returns 6.79% against the same
22.94% benchmark.

## Why it fails -- the mechanism, which is not obvious

THE SELL RULE FIRES THE WINNERS AND KEEPS THE LOSERS. "Sell when it gets
back to its high" means a stock that recovers is sold and then continues
without you, while a stock that never recovers is held indefinitely waiting
for a high it will not reach. NVDA printed new highs hundreds of times in
twenty years; the rule sells every one. Citigroup never recovered its high;
the rule holds it for two decades.

The position's upside is capped at the previous high. Its downside is open.
THIS IS THE SAME DEFECT AS THE INVERTED HYSTERESIS REMOVED FROM R2 ON
2026-09-22 -- an exit condition that is structurally easier to satisfy than
the entry -- wearing different clothes. A future session that rediscovers
this idea should recognise the shape before running the test.

## The pattern this makes five for five

Mean reversion joins momentum rotation, concentration, volatility targeting
and trend-gated volatility targeting. The RSI-2 variant cuts max drawdown
from -59.7% to -27.0% while earning a third as much. EVERY STRATEGY TESTED
IN THIS REPOSITORY REDUCES RISK AND NONE RAISES RETURN. See
2026-09-23_BEATING_SPY.md.

## Caveat

The buy-and-hold benchmarks here are inflated by the same survivorship
defect named in 2026-09-23_BEATING_SPY.md -- the 14 symbols were chosen in
2026. That inflates the BENCHMARK, which makes this rejection CONSERVATIVE
rather than generous: the strategy would have to beat a lower bar on an
honest universe, and it loses by 16 points on this one.
