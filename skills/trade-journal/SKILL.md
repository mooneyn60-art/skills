---
name: trade-journal
description: Log trades to the robinhood-autotrader ledger and score them against SPY. Use to append a trade entry in the ledger's JSONL schema, and to compute a closed position's return vs buy-and-hold SPY over the same days (was TARS actually adding value, or just riding the market?). Keeps R13 (no dollar balances in commits) and treats missing data honestly.
---

# Trade Journal

Two jobs: **record** each trade in the ledger, and **score** it against SPY over
the same holding window. The second is the honest test — a green trade that
lagged SPY over those days did not add value (robinhood-autotrader research
item 18, _IS_TARS_ADDING_VALUE.md).

## Ledger location and schema

`skills/robinhood-autotrader/paper/trades.jsonl`, one JSON object per line.
A trade entry uses these keys (match existing rows):

```
id, ts/opened/closed, account, symbol, instrument, contract, direction, qty,
entry, exit, stop, target, planned_risk, realized_pnl, exit_reason, strategy,
source, thesis
```

Report ratios/percentages (R-multiples, % of account), never raw account
balances, in anything that gets committed (R13 — dollar balances in a commit
message have blocked pushes before). Per-trade dollar P/L in the ledger file is
fine; account totals are not.

## Log a trade

Append with `scripts/journal.py log`:

```
python3 scripts/journal.py log --ledger <path-to>/trades.jsonl \
  --symbol SOFI --instrument option --contract "SOFI 2026-12-18 C16" \
  --direction long --qty 1 --entry 2.05 --stop 1.23 \
  --strategy R17_option_slot --thesis "Oct 27 earnings" --source TARS
```

It fills `id`, `opened`/`ts`, `closed:false`, and computes `planned_risk` from
entry and stop. Never invents fields it wasn't given.

## Score a closed trade vs SPY

`scripts/journal.py score` takes the trade's return and SPY's return over the
SAME dates and prints the difference and an R-multiple:

```
python3 scripts/journal.py score \
  --entry 17.35 --exit 15.75 --spy-entry 771.35 --spy-exit 765.61 \
  --planned-risk-pct 8
```

Output: trade %, SPY % over the same days, excess vs SPY, and R-multiple
(trade return / planned risk). A positive P/L with NEGATIVE excess-vs-SPY is
flagged: "green but lagged SPY — no value added."

## Weekly roll-up

For the Friday desk run, score every position closed that week, sum the excess
vs SPY, and write a `type:"weekly"` summary row (the schema the ledger already
uses: account_week_pct, spy_week_pct, r_multiples, expectancy_*). Report the
week in R-multiples and vs-SPY, not dollars.

## Hard rules

- Reads and appends to the ledger; never edits or deletes past rows.
- Places no trades.
- Missing data (no SPY price, unknown dates) → say so and skip the score; never
  fabricate a comparison (RULE #1 spirit: no fake numbers).
- No account balances in commit messages (R13). Never hardcode the account
  number.
