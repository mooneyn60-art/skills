---
name: position-sizer
description: Compute the max dollar size for a new trade from the robinhood-autotrader money rules (R3 20% per-name cap, 15% cash floor, 8% risk budget) and the 2026-09-30 Kelly study. Use before any buy to answer "how much can I put in this?" It counts shares and option premium in the same underlying as one position, and it never sizes past the cash floor.
---

# Position Sizer

Answers one question before a buy: **how many dollars may go into this position?**
It turns the robinhood-autotrader money rules and the 2026-09-30 Kelly study
(research/2026-09-30_KELLY_SIZING.md) into a single number, so sizing stops
being a vibe.

Computes nothing about whether the trade is good — that's options-risk-check
and Nolan's judgement. This only bounds the size.

## Why these numbers

The Kelly study measured the strategy's per-trade payoff and found:
- robust (binary) Kelly ~0.20-0.25 for a single name, ~0.08-0.20 for non-core
  names → R3's 20% cap is about right, maybe generous.
- full continuous Kelly is huge but fat-tail/survivorship-flattered → treat as
  an upper bound, not a target; use fractional Kelly.
- the book runs ~3.9 independent bets at once → concentration is the real risk.

So the caps are: 20% per name (hard), 15% soft for non-core names, and the same
name's shares + option premium count together (the SOFI 2026-09-28 lesson).

## The rules it enforces

| Rule | Value | Source |
|---|---|---|
| Per-name hard cap | 20% of account | R3 + Kelly |
| Non-core soft cap | 15% of account | Kelly ex-megacap ~0.08-0.20 |
| Cash floor | 15% of account must stay in cash | R3 |
| Risk budget | 8% of account at risk across open positions | R3 |
| Same-name aggregation | shares + option premium = one position | Kelly / SOFI lesson |

## How to run

```
python3 scripts/size.py \
  --account 1700 --cash 250 \
  --name-exposure 95 --core no \
  --stop-distance-pct 40 \
  --open-risk 60
```

- `--name-exposure`: $ already in this underlying (shares + option premium).
- `--core`: yes for a conviction/core name (20% cap), no for others (15%).
- `--stop-distance-pct`: how far the planned stop is below entry, in % (used
  for the 8% risk-budget check; for an option, the premium at risk to its stop).
- `--open-risk`: $ already at risk across all open positions (sum of each
  position's distance to its stop).

Pull the inputs from get_portfolio (account, cash), get_option_positions /
get_equity_positions (name exposure, open risk). Report the binding limit to
Nolan.

## Output

The max additional $ for this position = the smallest of: (per-name cap minus
current name exposure), (cash above the floor), and (remaining risk budget /
stop-distance). It names WHICH limit binds, so Nolan knows what's stopping him.
If the answer is <= 0, it says so plainly (e.g. "already at the cap" or "below
the cash floor — no new buys").

## Hard rules

- Advice only; sizes nothing, places nothing.
- Never hardcode the account number (`$ROBINHOOD_ACCOUNT` or passed in).
- No dollar balances in any commit message (R13).
- A size > 0 is a ceiling, not a recommendation to fill it.
