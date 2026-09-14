# TARS-1 — Trading Rules

One-line description: The complete, mechanical ruleset TARS trades. No discretion.
Last Updated: 2026-09-14
Status: ACTIVE — pending single-writer confirmation
Audience: Nolan; any agent or session operating account #731951265

## Overview

These rules exist so that no trade is ever the product of a hunch. Every entry,
exit and size below is computable from price data alone. If a decision cannot be
derived from these rules, it does not get made.

The design assumption is honest: this system has no forecasting edge. It is
built on the one thing with decades of out-of-sample evidence behind it —
trend persistence — and on the one advantage a machine actually has over a
person, which is following its own rule after a loss. Everything here optimises
for surviving long enough for that to matter.

## R1 — Universe

Tradeable: US equities and ETFs, last price > $5.00, 30-day average volume
> 1,000,000 shares. Nothing else. No OTC, no crypto (execution is blocked, 403,
not retryable), no options until R9 opens them.

## R2 — Entry (all four must be true)

  1. Price > 200-day moving average.
  2. Price > 50-day moving average.
  3. Price within 3% of its 20-day high.
  4. No scheduled earnings within the next 3 trading days.

Rule 1 is the load-bearing one. Buying below the 200-day MA — "it's cheap now" —
is the rule that tested WORST in this repo's own backtest: -87.7% max drawdown
on the single-stock basket. It is prohibited, permanently, including when the
name looks obviously oversold. Especially then.

## R3 — Sizing

Max $50 notional per position at entry. Max 8 concurrent positions. Minimum 40%
of account value held in cash at the close of any session.

No averaging down, ever. A position is entered once. If it falls, it hits its
stop; it does not get reinforced.

## R4 — Exits

  Hard stop: -8% from fill. Placed as a GTC stop order within 60 seconds of the
             fill being confirmed. A position without a live stop is a bug.
  Breakeven: at +8% unrealised, raise stop to the fill price.
  Trail:     thereafter, stop trails 8% below the highest close since entry,
             raised only, never lowered.
  No fixed profit target. Winners are trailed out, not trimmed early.

## R5 — Order types

Entries: limit orders only, priced at or inside the ask, good-for-day. If it
does not fill, it does not get chased.
Stops: stop-market. Slippage on the exit is accepted as the price of certainty
that the exit happens.

## R6 — Circuit breakers

  Two positions stopped out within any rolling 5 trading days
      -> no new entries for the next 3 trading days.
  Account value -15% below its high-water mark
      -> halt all new entries, flatten nothing, report and wait for Nolan.
  Any rule in this file cannot be evaluated (data missing, tool erroring)
      -> no trade. A missing input is never treated as a passing test.

## R7 — Single writer

Only one agent places orders into this account at a time. Two agents managing
one book will cancel each other's stops. Before trading, confirm the other is
stood down.

## R8 — Logging

Every order is appended to paper/trades.jsonl with the rule number that
triggered it. Every closed trade is scored in R-multiples and against SPY held
over the identical window, so that a rising market does not get recorded as
skill.

## R9 — Options

Locked until: account value > $2,000 AND 20 closed equity trades logged. Then
long calls/puts only, 30-45+ DTE, max $50 per position. Never 0DTE, never naked
calls, never uncovered puts.

## R10 — Kill switch

Nolan says stop -> all new entries cease immediately, that message, no
argument, no clarifying questions. Existing positions are held with their stops
live unless he says flatten.

## What would falsify this

If after 30 closed trades the expectancy is not distinguishable from zero at 95%
confidence, and the benchmark-relative excess is negative, the ruleset is not
working and gets replaced rather than tuned. Tuning a losing rule until it
backtests well is how you turn a small loss into a large one.
