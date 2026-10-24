# Setup and safety walkthrough

This covers **Section B** of `SKILL.md` — the offline `scripts/` loop that runs
outside any Claude Code session via `robin_stocks`. For live in-session trading via
Robinhood's official Trading MCP server, see `reference/live-mcp-architecture.md`
instead — this file's steps (its own `.env`, `LIVE_TRADING` flag, `trade_log.csv`)
don't apply there.

## 1. Install

```bash
cd scripts
pip install -r requirements.txt
```

## 2. Credentials

```bash
cp .env.example .env
```

Fill in `.env` with your own Robinhood username/password and TOTP secret (the base32
string Robinhood shows you when you turn on authenticator-app 2FA — not a rotating
6-digit code), plus your own Anthropic API key. This file should never be committed;
it's already covered by a reasonable `.gitignore` pattern (`.env`), but double check
before pushing anywhere.

## 3. Run in paper mode first

```bash
python trader.py --once
```

This logs in, pulls the watchlist, gets a decision from Claude, and writes to
`trade_log.csv` — no real orders, because `LIVE_TRADING` defaults to false. Do this
repeatedly (or with `--interval`) over several days and actually read the log before
even considering live mode.

## 4. Where this should run

This is meant to run unattended on infrastructure you control — your own machine, a
small server, a container on a schedule — not inside a Claude Code session, which
doesn't hold your Robinhood credentials and shouldn't. Use cron, systemd, or Docker's
own restart policy to keep it running; `trader.py --interval N` handles the loop
itself, so you don't need this process supervised beyond "restart if it dies."

## 5. Moving to live trading

Before you ever set `LIVE_TRADING=true`:

- **Read the ToS risk.** `robin_stocks` is an unofficial client. Robinhood's terms
  generally prohibit bot/automated trading through unofficial channels — this is a
  real risk of account restriction or closure, separate from whether the strategy
  makes money.
- **Review real paper-trading history.** Don't flip the switch after one good run.
- **Confirm your risk caps in `.env` actually match your risk tolerance** —
  `AUTOTRADER_MAX_POSITION_USD`, `AUTOTRADER_MAX_DAILY_LOSS_FRACTION`, and
  `AUTOTRADER_MAX_POSITION_FRACTION` are the knobs; the shipped defaults are a
  reasonable moderate starting point, not a recommendation for your account size.
- **Understand the circuit breaker.** If daily loss hits the cap, `risk.py` writes a
  `HALT_TRADING` file next to `trade_log.csv` and the loop stops. It does not clear
  itself — you have to look at what happened and delete the file yourself to resume.
  Don't automate that deletion.
- Only then set `LIVE_TRADING=true` in your own `.env`, on your own machine.

## 6. Debugging

`trade_log.csv` has one row per decision Claude made, whether or not it turned into an
order — `order_id` is empty for decisions that didn't clear a risk check (below
`AUTOTRADER_MIN_CONFIDENCE`, no existing position to sell, etc.), so it's a full audit
trail of "what did the bot see and think," not just "what did it trade."
