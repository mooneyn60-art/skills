---
name: robinhood-autotrader
description: Runs an automated Robinhood equities trading loop that uses Claude to analyze a watchlist and decide buy/sell/hold, sized by a configurable risk manager. Use when the user wants to set up, configure, or run autonomous or semi-autonomous stock trading against a Robinhood account via robin_stocks. Defaults to paper trading (no real orders) until the user explicitly enables live mode on their own machine.
license: Complete terms in LICENSE.txt
---

# Robinhood Autotrader

## Overview

An autonomous trading loop for a Robinhood equities account:

1. Logs into Robinhood with `robin_stocks` + `pyotp` (TOTP, no manual 2FA codes).
2. Pulls quotes/history for a configurable watchlist.
3. Sends a market snapshot to Claude (`anthropic` SDK), which returns a structured
   buy/sell/hold decision per symbol with a confidence score and reasoning.
4. Runs every decision through a risk manager that enforces a max position size and a
   daily-loss circuit breaker before anything is sized or sent.
5. Executes the trade — or, in paper mode (the default), just logs what it *would* have
   done — and writes a full audit trail to `trade_log.csv`.

**This is not run inside a Claude Code session.** It needs the user's own Robinhood
credentials and Anthropic API key, so it's meant to run unattended on the user's own
machine/server (cron, systemd, Docker), not here. Claude's job when this skill is
invoked is to help the user set it up, configure risk limits, review `trade_log.csv`
output, and debug issues — not to hold or transmit the user's credentials.

## Critical safety notes (read before enabling live trading)

- **`robin_stocks` is an unofficial, reverse-engineered client for Robinhood's private
  API.** Robinhood's terms generally prohibit automated/bot trading through unofficial
  channels. Using this can lead to account restriction or closure — that risk exists
  independent of whether the strategy is profitable. Make sure the user understands
  this before helping them go live.
- **Live trading is opt-in, not the default.** `scripts/executor.py` only places real
  orders when the user sets `LIVE_TRADING=true` in their own environment. Never set
  that flag on the user's behalf, and never ask the user for their Robinhood password
  or TOTP secret inside this chat — those belong in the user's own `.env` on their own
  machine, from `.env.example`.
- **The daily-loss circuit breaker halts the whole loop**, not just new trades, by
  writing a `HALT_TRADING` file next to `trade_log.csv`. It only clears when the user
  deletes that file, so a bad day can't compound unattended. Don't build a
  "self-healing" workaround for this — it's the whole point.
- **LLM output is not guaranteed correct or profitable.** Claude's decisions are
  probabilistic and can be wrong, hallucinate reasoning, or misjudge risk in ways that
  differ from a human trader. Treat this as automation of a strategy the user is
  responsible for, not a source of guaranteed returns. Nothing here is financial
  advice.
- **Always get real paper-trading history before discussing enabling live mode** —
  several days/weeks of `trade_log.csv` output the user has actually reviewed.

## When to use this skill

Use it when the user wants to:
- Set up automated Robinhood trading with Claude-driven decisions.
- Change risk limits (position size cap, daily loss cap, watchlist).
- Understand or debug what the bot did (read `trade_log.csv`).
- Move from paper mode to live mode — walk through the safety notes above first and
  confirm the user has reviewed paper-trading output before helping them set
  `LIVE_TRADING=true` in their own environment.

## Setup

See `reference/setup.md` for full instructions (env vars, install, running the loop).
Quick path:

```bash
cd scripts
pip install -r requirements.txt
cp .env.example .env   # fill in the user's own credentials, never Claude's
python trader.py --once          # single decision pass, paper mode by default
python trader.py --interval 900  # loop every 15 minutes during market hours
```

## File map

| File | Purpose |
|---|---|
| `scripts/config.py` | Watchlist, risk caps, model name — all overridable via env vars |
| `scripts/auth.py` | Robinhood login via `robin_stocks` + TOTP from `pyotp` |
| `scripts/market_data.py` | Fetches quotes/history and account state from Robinhood |
| `scripts/signals.py` | Calls the `anthropic` SDK for structured trade decisions |
| `scripts/risk.py` | Position sizing caps + daily-loss circuit breaker (`HALT_TRADING`) |
| `scripts/executor.py` | Places live orders or logs paper trades, per `LIVE_TRADING` |
| `scripts/trader.py` | Orchestrates one pass or a continuous loop, writes `trade_log.csv` |
| `reference/setup.md` | Env vars, ToS caveats, how to move from paper to live safely |
