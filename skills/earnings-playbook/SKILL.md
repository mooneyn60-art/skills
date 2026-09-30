---
name: earnings-playbook
description: Prep a stock for its earnings report. Use before an earnings date to compare how the stock has actually moved on past earnings against the move options are pricing in now, and to scenario a held option's P/L across up/flat/down outcomes. Built for the robinhood-autotrader SOFI Oct-27 situation and reusable for any name.
---

# Earnings Playbook

Prep for an earnings report on a name you hold or are watching. It answers three
questions, honestly:

1. **How much does this stock usually move on earnings?** (historical |move|)
2. **How much move are options pricing in now?** (implied move from the ATM
   straddle) — so you can see if options are cheap or expensive vs history.
3. **What happens to my option across outcomes?** (P/L if the stock goes up X%,
   flat, down X%, including that an ATM straddle's implied move is roughly the
   breakeven).

It does not predict direction. Earnings direction is not predictable (see
robinhood-autotrader research/2026-09-24_EARNINGS_MOVES.md and _WHY_PRICES_MOVE).
The point is to size and stop correctly, and to know the odds before the print,
not to guess the number.

## When to use

In the days before any earnings date for a held or watched name. For the
robinhood-autotrader account, the desk's one-shot pre-earnings brief calls this.

## Step 1 — historical moves

Reuse `paper/research_scripts/earnings_moves.py` in the robinhood-autotrader
skill if the name is in its data, or pull the last ~8 earnings dates and the
next-day % move from get_earnings_results / get_equity_historicals. Report the
median and the range of |move|, and how many were up vs down (usually ~50/50).

## Step 2 — implied move

From the option chain nearest the earnings date, take the ATM call + ATM put
mid prices (the straddle). Implied move ≈ straddle_price / stock_price. Compare
to the historical median: if implied >> historical, options are expensive (the
market expects a big move); if implied << historical, they're cheap. Pull
quotes with get_option_quotes.

## Step 3 — scenario the position

Run `scripts/scenario.py` with the held option and a set of post-earnings stock
prices. It prints intrinsic value at each outcome and the P/L vs what you paid,
and flags that a long option through earnings usually loses to IV crush if the
stock doesn't move more than the implied move.

```
python3 scripts/scenario.py \
  --type call --strike 16 --paid 2.05 --stock-now 16.05 \
  --implied-move-pct 6.5 --moves -10 -6.5 0 6.5 10
```

## What to tell Nolan

- historical median move vs implied move (cheap/expensive)
- his option's breakeven move and P/L in each scenario
- the honest caveat: direction is a coin flip; through-earnings long options need
  a move BIGGER than implied just to break even (IV crush). Holding through
  earnings is a volatility bet, not a direction edge.
- whether to hold through, trim, or close before the print — his call.

## Hard rules

- No direction predictions dressed up as forecasts.
- Advice only; places nothing.
- Never hardcode the account number; no dollar balances in commits (R13).
- The scenario model is a simple intrinsic + implied-move breakeven; it is NOT a
  full option pricer (no skew, crude IV crush). Say so when reporting.
