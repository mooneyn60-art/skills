# Range-Regime Mean Reversion — Real Signal, No Tradeable Strategy

One-line: Nolan was right that TARS applied a trend filter to a ranging
stock; inside ranging regimes buying the bottom of the range genuinely beats
buying the top (t=5.20), but no exit rule converts that edge into a strategy
that beats buy-and-hold.

Last Updated: 2026-09-23
Status: SIGNAL CONFIRMED / STRATEGY REJECTED
Audience: TARS sessions, Nolan

## Why this was run

TARS told Nolan "buy low loses to buy high," citing an aggregate test across
all stocks and all days. Nolan pushed back that SOFI has been range-bound
and that the 200-day was the wrong tool for it. HE WAS RIGHT ABOUT THE
MIS-SPECIFICATION. The aggregate test pooled trending and ranging regimes,
and the regime is exactly what determines which rule applies.

## The signal — confirmed, and it survives everything

Regime split by Wilder ADX(14), position measured as location within the
trailing 60-day high/low range. Forward 1-month returns, 14 symbols,
2006-2026:

    RANGING  (ADX<20)  bottom quartile  +1.95%   n=4323
    RANGING  (ADX<20)  top quartile     +0.95%   n=8448
    TRENDING (ADX>25)  bottom quartile  +1.35%   n=7722
    TRENDING (ADX>25)  top quartile     +1.31%   n=12769

In ranges, buy-low earns DOUBLE buy-high. In trends it is a coin flip.

Edge +1.01pp per month, WELCH t = 5.20. Split sample: wins both halves.
Rolling walk-forward: 7 of 9 windows. Drop the big winners: the edge HOLDS
in all five universes and STRENGTHENS without NVDA (+1.18pp, t=6.06) --
the opposite of the momentum result, and the single strongest evidence in
this repository.

ADX threshold behaves like a real effect rather than a fitted cell:
ADX<15 +1.11pp, <18 +1.24pp, <20 +1.01pp, <22 +0.65pp, <25 +0.39pp,
<30 +0.17pp, NO FILTER +0.21pp (t=1.76). That last figure is why the
original aggregate test saw nothing -- without the regime filter the
effect is invisible.

## The strategy — rejected

Mechanical rule, no hand-picked levels: buy when ADX<20 and price sits in
the bottom 25% of its 60-day range; sell at the top 25% or an 8% stop.
Max 4 positions, whole shares, 5bp slippage per side.

    RANGE strategy      6.81% CAGR, -59.9% DD, Sharpe 0.46, 962 trades
    buy & hold same 14 22.94% CAGR, -59.7% DD, Sharpe 0.89
    SPY buy & hold      9.11% CAGR, -56.5% DD
    walk-forward: 2 of 8 windows

Costs are NOT the cause: at zero slippage it returns 7.13%. The structure
is the problem.

The exit is what breaks it, the same defect found in the 2026-09-23 mean
reversion test: selling at the top of the range caps every winner. Removing
the range exit entirely (stop only) returns 30.09% -- but that variant fails
its own hurdles: walk-forward 4/9, LOSES the second half of the split
sample (18.31% vs 34.82% for holding), falls below buy-and-hold once three
megacaps are removed, and rests on only 32 ROUND TRIPS IN 20 YEARS.

## Two errors TARS made and caught only because Nolan demanded a fact-check

1. WRONG EXPLANATION, ASSERTED AS CONFIRMED. TARS hypothesised that the
   edge fails to convert because ranging stocks are a low-return regime,
   and hardcoded the word "CONFIRMED" into the diagnostic script BEFORE
   seeing the output. The data refutes it: ranging regimes return 16.9%
   annualised against 15.4% for trending. Ranging is the BETTER
   neighbourhood. The real cause is the exit rule, not the regime.

2. AN ANECDOTE PRESENTED AS A BACKTEST. TARS quoted Nolan a "+67.5% vs
   -10.3%" result for a range rule on SOFI. That came from 29 weekly bars
   typed in by hand, with buy/sell levels (16.50/18.50) chosen AFTER
   looking at the chart, never run through the engine, never walk-forwarded,
   n=3 round trips. It should have been labelled an anecdote and was not.
   RETRACTED.

## What stands

The ENTRY signal is real and is the best-evidenced finding in this
repository. What is not established is any exit that monetises it. A future
session may test combining the range-bottom entry with R4's full exit stack
(stop, breakeven raise, 20% trail, 200-day trend exit) -- note that the
closest tested approximation, entry plus stop only, already failed its
hurdles, so expectations should be low.

## Where this leaves the running tally

Six strategy families tested: momentum rotation, concentration, volatility
targeting, trend-gated volatility targeting, channel mean reversion, and
range-regime mean reversion. NONE produces a tradeable strategy that beats
buy-and-hold under the four hurdles. This one is different in kind, though:
it is the first whose underlying SIGNAL is statistically solid. The failure
is in conversion, not in the hypothesis.
