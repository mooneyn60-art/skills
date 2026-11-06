---
name: options-risk-check
description: Pre-trade gate for buying a single-leg option. Use before ANY option buy to check days-to-expiry, bid/ask spread, open interest, premium as a share of the account, and earnings timing, and to confirm a stop is planned. Turns the robinhood-autotrader R5/R17 option rules into a checklist that fails loudly instead of letting a bad contract through.
---

# Options Risk Check

A pre-trade gate. Run it before buying any single-leg option so a contract that
violates the account's own rules never gets placed. It encodes what the
robinhood-autotrader skill learned the hard way (see its research/ on options),
including the 2026-09-28 SOFI day where naked, over-sized, wide-spread contracts
churned real money.

This skill NEVER places an order. It returns PASS / WARN / FAIL and the numbers
behind each, so the human (Nolan) decides. It is advice, not execution.

## When to use

Before every option buy, and whenever asked "is this a good contract to buy?"
or "check this option". Also good as the first step inside the earnings-playbook
skill.

## The checks (from robinhood-autotrader R5 / R17)

Run `scripts/check.py` with the contract's numbers. It applies:

| Check | Rule | Result if broken |
|---|---|---|
| Days to expiry | >= 60 DTE for the R17 slot; < 30 DTE is a lottery | FAIL if <30 for a swing; WARN 30-59 |
| Spread | (ask-bid) <= 10% of mid | FAIL |
| Open interest | >= 500 | FAIL |
| Premium size | position premium <= 6% of account (R17), and shares+premium in the same name <= 20% (R3) | FAIL over 6%; WARN toward the R3 cap |
| Delta | 0.30-0.60 for a directional swing (not deep OTM lottery) | WARN outside |
| Earnings | flag if an earnings date falls before expiry (IV crush / gap risk) | WARN |
| Stop planned | a stop MUST be planned (R4/R5). No stop = FAIL | FAIL |

A single FAIL means don't buy it as-is. WARNs are judgement calls to surface to
Nolan, not blockers.

## How to run

```
python3 scripts/check.py \
  --account 1700 --premium 108 \
  --bid 0.93 --ask 1.01 --dte 24 --oi 271 --delta 0.63 \
  --name-exposure 388 --earnings-before-expiry yes --stop-planned no
```

Feed it live numbers from the Robinhood tools (get_option_quotes for bid/ask/
delta/oi, get_portfolio for account value, get_option_positions for existing
name exposure). Report the output to Nolan verbatim; do not soften a FAIL.

## Hard rules this skill must respect

- It only reads and computes. It places nothing.
- Never hardcode the account number; the account is `$ROBINHOOD_ACCOUNT` or is
  passed in. (Past mistake: account details in tracked files.)
- Dollars stay out of any commit message or ledger per robinhood-autotrader
  R13 — use ratios/percentages there.
- If a contract passes every check, that is NOT a buy signal. It only means the
  contract isn't structurally bad. The decision is still Nolan's.
