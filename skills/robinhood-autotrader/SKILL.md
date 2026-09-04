---
name: robinhood-autotrader
description: Two ways to run autonomous Robinhood trading with Claude. (A) Live, in-session agentic trading via Robinhood's official Trading MCP server, orchestrated as parallel read-only research "desks" (regime, momentum, mean-reversion, crypto, crowd/popularity, options flow, earnings, social sentiment) with all execution authority centralized in the main session behind a Confirmation Gate and a Risk/PDT Checks-and-Balances Gate. (B) An offline unattended script loop (robin_stocks + pyotp + anthropic) that runs outside any Claude Code session, for a single Claude-scored watchlist decision per pass. Use when the user wants to set up, configure, extend, or debug either path — especially when they've connected Robinhood's official agentic Trading MCP connector and want Claude Code itself to research and trade.
license: Complete terms in LICENSE.txt
---

# Robinhood Autotrader

## Which path is this?

- **Section A — live in-session trading via Robinhood's official Trading MCP server**
  (`agent.robinhood.com/mcp/trading`). Claude Code itself researches and places orders,
  right here, in this session, against a Robinhood-connected account — normally a
  dedicated "agentic" sub-account the user sets up specifically for this, separate from
  their primary brokerage/IRA accounts. This is Robinhood's own sanctioned agentic-
  trading feature (OAuth-based), not an unofficial API client. **This is the path to
  use when the user has connected that MCP server and wants ongoing autonomous or
  semi-autonomous trading happening in Claude Code conversations.**
- **Section B — offline unattended script loop** (`scripts/`) using `robin_stocks` +
  `pyotp` + the `anthropic` SDK. Runs on the user's own machine/server (cron, systemd,
  Docker), independent of any Claude Code session, and needs the user's own Robinhood
  credentials and Anthropic API key directly. Use this when the user explicitly wants
  something running outside of a Claude Code conversation.

Don't mix the two: Section A never touches `robin_stocks` or the user's raw
credentials; Section B never assumes an MCP connection. Ask which the user means if
it's ambiguous — "set up Robinhood trading" defaults to asking, not guessing.

## Section A — Live in-session trading (Robinhood Trading MCP)

Full architecture, gates, cadence, and the live-dashboard pattern live in
`reference/live-mcp-architecture.md` — read it before setting this up or extending an
existing setup. Summary:

- **Research is parallel and read-only; execution is centralized.** Spin up independent
  "desks" as subagents (the `Agent` tool, `subagent_type: "general-purpose"`,
  `run_in_background: false`, all spawned in one message so they run concurrently).
  Every desk gets explicit instructions to never call an order-placing tool. The main
  session is the only place with execution authority — it receives every desk's report
  and is the sole Risk/Portfolio-Manager.
- **Desk roster** (research angles, expand thoughtfully rather than by rote): Regime,
  Momentum, Oversold/Mean-Reversion, Crypto, Popularity/Crowd (Robinhood's own
  popular-watchlist data — genuinely "what other users are buying"), Options Flow
  (unusual volume/OI as an institutional-positioning proxy, signal-only), Earnings/
  Catalyst, Social Sentiment (web-wide "what people are buying" chatter). See the
  reference doc for exact tool calls per desk.
- **Two gates every idea must clear before it can execute:**
  1. **Confirmation Gate** — cross-check against the Regime Desk's call and against
     other desks' findings; corroboration across desks raises conviction, a
     contradiction kills the idea here.
  2. **Risk & PDT Checks-and-Balances Gate** — new position size cap (~20% of equity),
     existing-position concentration cap (~30%), PDT budget (≤3 same-day round trips
     per rolling 5 business days), and a daily hard-stop floor (prior trading day's
     close equity minus the user's chosen dollar loss limit, recomputed every new
     trading day) that halts new buys once breached.
- **Cadence:** scheduled Routines (`create_trigger`) drive check-ins. The platform's
  Routine scheduler has a hard 1-hour minimum cron interval — anything tighter is
  rejected outright. Faster cadence during market hours is achieved by
  self-chaining (`send_later` N minutes out at the end of each check-in, repeated),
  with the hourly Routine kept as a fallback in case the chain breaks. Split fast
  ticks into a cheap **light tick** (refresh account/positions/risk, always) and a
  **full desk round** gated on elapsed time or a material change — running all desks
  every few minutes is almost pure redundancy and burns real budget for no new signal.
- **Optional live dashboard:** publish an HTML Artifact with the `db` capability and
  write account/risk/desk-status/decision-log/trade-log snapshots to it on every
  check-in; the page subscribes live via `onSnapshot`, so no republish is needed for
  routine updates. Add the `sample` capability for an in-page chat box, but be explicit
  in the UI that it's a separate, memory-less quick-answer assistant that **cannot
  place trades** — log the user's message to a shared doc too, so the actual trading
  session can give a real ("live") answer at its next check-in.
- **Hard constraints worth knowing before you hit them** — see
  `reference/live-mcp-architecture.md` for the full list (harness tool-approval gates
  that chat "yes" can't bypass, fractional/dollar order restrictions by session and
  order type, pre-market order queuing behavior, and that crypto agentic execution can
  be regulatorily blocked for some account residencies — check for that before
  promising the user crypto execution, and keep any crypto desk strictly research-only
  if it's blocked).
- **Standing autopilot (no per-trade confirmation) is opt-in, not a default** — only run
  fully autonomously once the user has explicitly and repeatedly granted that in chat.
  A fresh request for this setup should start with research-only or confirm-before-
  execute, the same posture Section B defaults to.

## Section B — Offline unattended script loop

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
machine/server (cron, systemd, Docker), not here. Claude's job when this path is used
is to help the user set it up, configure risk limits, review `trade_log.csv` output,
and debug issues — not to hold or transmit the user's credentials.

### Critical safety notes (read before enabling live trading)

- **`robin_stocks` is an unofficial, reverse-engineered client for Robinhood's private
  API.** Robinhood's terms generally prohibit automated/bot trading through unofficial
  channels. Using this can lead to account restriction or closure — that risk exists
  independent of whether the strategy is profitable. Make sure the user understands
  this before helping them go live. (Section A, via Robinhood's official Trading MCP
  server, does not carry this specific unofficial-API risk — a good reason to prefer
  Section A when the user has that connector available.)
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
  advice. (This caveat applies equally to Section A's desks and Risk/Portfolio-Manager
  session — none of it is guaranteed correct either.)
- **Always get real paper-trading history before discussing enabling live mode** —
  several days/weeks of `trade_log.csv` output the user has actually reviewed.

### Setup

See `reference/setup.md` for full instructions (env vars, install, running the loop).
Quick path:

```bash
cd scripts
pip install -r requirements.txt
cp .env.example .env   # fill in the user's own credentials, never Claude's
python trader.py --once          # single decision pass, paper mode by default
python trader.py --interval 900  # loop every 15 minutes during market hours
```

## When to use this skill

- **Section A**: the user has connected Robinhood's official Trading MCP server and
  wants Claude Code to research and trade autonomously or semi-autonomously across
  conversations — set up or extend the desk architecture, gates, cadence, and
  dashboard described in `reference/live-mcp-architecture.md`.
- **Section B**: the user wants something running independent of any Claude Code
  session — set up or debug the `scripts/` loop, change risk limits (position size cap,
  daily loss cap, watchlist), read `trade_log.csv`, or move from paper to live mode
  (walk through the safety notes above first, and confirm the user has reviewed
  paper-trading output before helping them set `LIVE_TRADING=true`).

## File map

| File | Purpose |
|---|---|
| `reference/live-mcp-architecture.md` | Section A: desks, gates, cadence self-chaining, live dashboard pattern, hard constraints |
| `reference/setup.md` | Section B: env vars, ToS caveats, how to move from paper to live safely |
| `scripts/config.py` | Section B: watchlist, risk caps, model name — all overridable via env vars |
| `scripts/auth.py` | Section B: Robinhood login via `robin_stocks` + TOTP from `pyotp` |
| `scripts/market_data.py` | Section B: fetches quotes/history and account state from Robinhood |
| `scripts/signals.py` | Section B: calls the `anthropic` SDK for structured trade decisions |
| `scripts/risk.py` | Section B: position sizing caps + daily-loss circuit breaker (`HALT_TRADING`) |
| `scripts/executor.py` | Section B: places live orders or logs paper trades, per `LIVE_TRADING` |
| `scripts/trader.py` | Section B: orchestrates one pass or a continuous loop, writes `trade_log.csv` |
