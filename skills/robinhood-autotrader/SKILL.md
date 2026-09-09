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
  "desks" as subagents (the `Agent` tool, `subagent_type: "general-purpose"`).
  Every desk gets explicit instructions to never call an order-placing tool. The main
  session is the only place with execution authority — it receives every desk's report
  and is the sole Risk/Portfolio-Manager. **Subagents are isolated and cannot message
  each other**; the main session is the switchboard.
- **Run rounds in stages, not one big spawn.** A **Wire Desk** goes first and alone,
  producing one shared macro/company/policy brief that is pasted verbatim into every
  downstream desk — one search instead of four, and the gates get teeth because desks
  finally argue from identical facts. Then up to three analysis desks concurrently,
  then cross-examination of genuine conflicts (reopen a desk with `SendMessage`, which
  preserves its context), then a mandatory **Red Team** pass before any buy.
- **Desk roster** (research angles, expand thoughtfully rather than by rote): Wire,
  Regime, Idea (scanner-driven momentum + mean-reversion), Portfolio Review, Performance,
  Red Team, Political Flow, Popularity/Crowd, Options Flow (signal-only), Earnings/
  Catalyst, Social Sentiment, Crypto. See the reference doc for each desk's mandate and
  the incidents that motivated Red Team and Performance.
- **Gates every idea must clear before it can execute:**
  1. **Confirmation** — cross-check against the wire, the Regime call, other desks, any
     cross-examination outcome, and the Red Team verdict. Corroboration raises
     conviction; an unanswered contradiction kills the idea.
  2. **Risk & PDT** — new position ≤~20% of equity, no position above ~30%, PDT budget
     (≤3 same-day round trips per rolling 5 business days), and a daily hard-stop floor
     (prior close equity minus the user's chosen loss limit) that halts new buys.
     **Rebase the floor for deposits/withdrawals, never for losses — and always tell
     the user when you rebase and why.**
  3. **Sizing** — a default band, halved when Red Team says RESIZE, the name is
     pre-revenue or cash-burning, it correlates with an existing large holding, or a
     major macro print lands within 48 hours.
- **Constructing a trade — run it in this order, and never backwards.** Find the
  **stop level first** (below structure, never at a prior low or inside a cluster
  of them; no clean level = no trade), then **size from that stop**
  (`shares = risk_budget / (entry - stop)`, ~1–1.25% of the account) rather than
  from a fixed dollar habit, then **prefer whole shares** because stop orders
  cannot be fractional and every fraction bought is permanently unstoppable, then
  **measure correlation on down days** before calling anything a diversifier.
  Track **portfolio heat** — the sum of `(price - stop) x stopped shares` across
  the book — against a ceiling, and recompute concentration after *sells* as well
  as buys, since trimming one position mechanically inflates another. The
  reference doc explains each with the failure that produced it: one session
  placed five stops before doing any level work and a desk later found all five
  wrong.
- **Cadence — the hard-won part.** The scheduled Routine *is* the cadence. Do NOT build
  a self-chaining fast tick: doing exactly that exhausted a session's rate limit by
  11:35am ET on a live trading day and left the account with **zero monitoring for 4.5
  hours**, including an unwatched stop level. Run a cheap **light tick** every firing
  (no subagents) and gate full desk rounds to at most twice a day; unused capacity is
  the monitoring reserve. Honest 1-hour monitoring beats promised 5-minute monitoring
  that dies at lunchtime — say so if the user asks for a cadence the budget can't hold.
  **Guard the calendar before the first tool call** (weekends, holidays, early closes):
  when the market is closed nothing in the account can change, so any pull is waste.
- **Optional live dashboard:** publish an HTML Artifact with the `db` capability and
  write account/risk/desk-status/decision-log/trade-log snapshots to it on every
  check-in; the page subscribes live via `onSnapshot`, so no republish is needed for
  routine updates. Add the `sample` capability for an in-page chat box, but be explicit
  in the UI that it's a separate, memory-less quick-answer assistant that **cannot
  place trades** — log the user's message to a shared doc too, so the actual trading
  session can give a real ("live") answer at its next check-in.
- **Hard constraints worth knowing before you hit them** — see
  `reference/live-mcp-architecture.md` for the full list (harness tool-approval gates
  that chat "yes" can't bypass; fractional/dollar orders being market + regular_hours
  only; **a `regular_hours` order placed pre-market queues and fills at the open**,
  which turns "I must be awake at 9:30" into a decision that executes itself; and that
  crypto agentic execution can be regulatorily blocked for some account residencies —
  check before promising it, and keep any crypto desk research-only if blocked).
- **What not to hunt.** Users ask for these by name; research them, then usually decline.
  Buying a hot IPO on day one is a documented retail loser (the pop accrues to
  allocation holders; the real structures are lockup expiries and quiet-period-end
  initiations, and fading supply needs shorting a cash account can't do). Buying *into*
  an earnings print is a coin flip — the defensible version is post-earnings drift,
  entering after the surprise, and even that must be checked against the regime, since
  in a rate-driven compression tape drift can run negative and every beat fades.
  **Options in a small account** deserve the multiplier check before any research:
  one contract is 100 shares, so covered calls need the account to be roughly
  **400x the share price** before that block is a sane slice of the book, cash-
  secured puts need 100 x strike in cash, and a protective put bought against a
  *fractional* position is not a hedge but a naked bet on ~90x the stock actually
  owned. Price a hedge's payoff table against the loss it removes before assuming
  it removes one. Answer with the account size at which each structure turns on,
  not a flat no.
- **Long options fail the *floor* test, not the friction test — check which.** The
  multiplier kills covered calls and cash-secured puts, but not long calls/puts, and
  "the spreads are prohibitive" is an assumption people substitute for measuring.
  Measure it: liquid mid-caps routinely quote a **penny wide** 30–45 days out on
  five-figure open interest, which is better execution than most equity fills. The
  real blocker is that a long option can go to zero, so its premium is spent against
  the **drawdown headroom left before the account's floor** — not against a
  percentage of equity. `max premium = (total value − floor) × the fraction of the
  remaining bankroll you'll stake on one binary`. On a $1,101 account with a $1,007
  floor that caps premium near $23, where only 12–18%-probability tickets live, while
  the one contract with a real delta and a real market costs $105 — more than the
  entire headroom, so it breaches the floor unaided. State the threshold, not a verdict.
- **Give options their own desks, ordered Structure → Liquidity → Risk.** *Structure*
  asks whether an option is the right expression of an already-passing thesis and
  which one (at level 2 there are no spreads, so "defined risk" means 100% of
  premium). *Liquidity* publishes the measured spread/OI/round-trip table. *Risk* runs
  the floor and multiplier tests last. Running Risk first yields a budget, and a budget
  makes the desk shop for whatever fits it — which is how a process ends up defending a
  far-OTM lottery ticket on price. Red Team stays mandatory on top: an option that gaps
  to zero has no stop underneath it.
- **If the user names a big target, do the arithmetic once, plainly.** From ~$1,000,
  reaching $1M is ~1,000x: about 37 years at 20% a year, ~17 at 50%, still a decade at
  100% *every* year — which essentially nobody sustains. At small account sizes deposits
  dominate returns. Say it without moralising, then write into the routine that the
  ambition never justifies loosening a gate, oversizing, chasing, or skipping a
  "nothing qualifies" answer.
- **Standing autopilot (no per-trade confirmation) is opt-in, not a default** — only run
  fully autonomously once the user has explicitly and repeatedly granted that in chat.
  A fresh request for this setup should start with research-only or confirm-before-
  execute, the same posture Section B defaults to. Whatever the authorization level,
  **report faithfully**: lead with the bad news and name a failure before the user finds
  it.

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
