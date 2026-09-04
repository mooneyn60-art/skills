# Live in-session trading architecture (Robinhood Trading MCP)

Reference for Section A of `SKILL.md` — running autonomous or semi-autonomous
Robinhood trading directly inside a Claude Code session, via Robinhood's official
Trading MCP server (`agent.robinhood.com/mcp/trading`). This is Robinhood's own
agentic-trading feature: OAuth-based, connected to a Robinhood-side account the user
controls (normally a dedicated "agentic" sub-account, separate from their primary
brokerage/IRA accounts so a bug or a bad decision can't reach money outside the
sandbox the user chose for this). It is not `robin_stocks` and doesn't carry that
unofficial-client ToS risk — see Section B for that different path.

## Connecting the server

`claude mcp add` (or the equivalent connector-setup flow) for the Robinhood Trading
MCP server, then the user completes OAuth in their browser. Adding an MCP server and
the first few tool calls against it (`review_equity_order`, `place_equity_order`, and
similar) commonly hit a harness-level tool-approval classifier that **chat approval
cannot bypass** — the user has to approve interactively outside the conversation (e.g.
via `/permissions` or an approval prompt in their client). If a trade-placing call
keeps getting blocked after the user has said "yes" in chat, that's very likely this —
explain the distinction rather than retrying the same call, and don't assume the user
saying "approved" changed anything if the tool itself hasn't visibly unblocked.

## The "personal trading firm" model

Two structurally separate roles:

- **Research desks** — independent subagents, spawned via the `Agent` tool
  (`subagent_type: "general-purpose"`, `run_in_background: false`, all desks launched
  in **one message** so they run concurrently rather than serially). Every desk's
  prompt must explicitly instruct it to **never call any order-placing tool** — desks
  propose, they do not execute. Keep desks read-only in practice, not just in
  instruction: give them query/read tools, not `place_*_order`/`review_*_order`.
- **Risk/Portfolio-Manager** — the main session, and only the main session. It receives
  every desk's report, runs the two gates below, and is the sole place execution
  authority lives. Never let a desk's output translate directly into an order without
  passing through both gates in the main session first.

### Desk roster

Treat this as a set of independent research *angles*, not a fixed list — add a desk
when there's a genuinely distinct signal to bring in, and skip adding more once new
desks would mostly restate what an existing one already covers (diminishing returns,
and every desk spawn is real API/token cost on a live-money account). A reasonably
maximal, non-redundant set:

| Desk | Signal | Typical tools |
|---|---|---|
| Regime | Risk-on / risk-off / choppy read on the broad market | index & equity quotes, technical indicators (RSI) on SPY/QQQ-equivalents |
| Momentum | Breakout candidates with a real catalyst (not just price action) | a saved momentum scan, news, technicals |
| Oversold / Mean-Reversion | Dip-buy candidates with **no** bad-news justification (a bounce candidate, not a falling knife) | a saved oversold scan, news to rule out a real reason for the drop |
| Crypto | Crypto regime + whether any pair clears the round-trip spread with room to spare | crypto quotes; note execution may be blocked (see Hard constraints) |
| Popularity / Crowd | What other users of the broker are actually buying/holding right now | the broker's own popular-watchlist / most-bought data, cross-checked against news for substance vs. hype |
| Options Flow | Unusual options volume/open-interest as an institutional-positioning proxy | option chains/quotes on names other desks already flagged. **Signal-only** — it should never propose its own options trade, only raise or lower conviction on an equity candidate another desk found |
| Earnings / Catalyst | Recent surprises or near-term upcoming earnings worth reacting to | earnings calendar + results |
| Social Sentiment | Broad "what people are buying/talking about" beyond the broker's own users | web search for trending-ticker chatter across financial media, cross-checked against news |

Pass every desk the current account snapshot (equity, buying power, current holdings)
pulled fresh in the main session first (Stage 0 / "light tick"), so sizing suggestions
are grounded in reality rather than assumptions the desk would otherwise have to guess.

### Gate 1 — Confirmation Gate (main session, not a desk)

Cross-check every surviving proposal against:
- The Regime Desk's call — a momentum/breakout/crowd-following idea generally needs a
  risk-on or trending regime to survive; an oversold/mean-reversion idea needs the
  regime to not be a genuine downtrend.
- Other desks' findings — a pick corroborated by a second, independent desk (e.g. it
  shows up on both the Popularity Desk and Social Sentiment, or Options Flow shows
  unusual call buying in a name the Oversold Desk already flagged) is materially higher
  conviction than a single desk's isolated pick. A pick directly contradicted by
  another desk's read dies here, named explicitly in the decision log.

### Gate 2 — Risk & PDT Checks-and-Balances Gate (main session, not a desk)

Every survivor must clear **all** of:
- New position size ≤ a chosen fraction of account equity (a commonly used starting
  point is ~20% per new position).
- No single position, after the trade, exceeds a chosen concentration cap (~30% is a
  reasonable starting point) of account equity.
- Pattern Day Trader budget: accounts under $25k equity are limited to 3 day-trades
  (same-symbol same-day round trips) per rolling 5 business days — check recent order
  history before executing anything that would count as one.
- Daily loss circuit breaker: recompute a hard-stop floor each new trading day as
  **prior trading day's close equity minus the user's chosen dollar (or percentage)
  loss limit**, and halt all new buys once today's account value is at or below it, or
  down more than a chosen percentage from this morning. This floor is a hard "wait
  until the next session" stop, not a target to trade up to.

Only orders that clear both gates get `review_equity_order` → `place_equity_order` (or
the crypto equivalents, where execution isn't blocked) — and only the main session
calls them.

### Decision log

Every round should report, concisely: what each desk proposed, which gate (if any) it
died at, and what — if anything — actually executed. Don't force a trade just to have
something to report; "N desks ran, 0 ideas survived to execution, here's why" is a
complete and correct outcome on plenty of rounds.

## Cadence

Scheduled Routines (`create_trigger`, bound to the persistent session so context
carries forward) drive check-ins. Two things worth knowing before configuring cadence:

- **The platform's Routine scheduler has a hard 1-hour minimum cron interval.** A
  tighter cron (e.g. `*/5 * * * *`) is rejected outright with an error naming the
  floor — don't fight this by retrying, and don't assume it means faster cadence is
  impossible.
- **Faster cadence during active hours is achieved by self-chaining, not by cron.** At
  the end of a check-in, if still within the window that warrants fast checks (e.g.
  regular market hours), call `send_later` with a short delay (e.g. 5 minutes) and a
  message telling the future firing to run the same protocol and re-chain again if
  still in-window. Keep the hourly cron Routine as a fallback in case the chain breaks
  (a crash, a session restart) — it re-establishes the chain on its next firing.
- **Split every fast tick into a cheap "light tick" and a gated "full round."** Running
  every research desk on every 5-minute tick is mostly pure redundancy — regime calls,
  earnings calendars, and popularity lists don't meaningfully change minute to minute —
  and burns real API/token budget for no new signal. A light tick (refresh
  account/positions, check for new fills, recompute risk numbers) should run every
  firing; the full multi-desk round should be gated on elapsed time since the last one
  (e.g. ≥15 minutes) or a material change (a new fill, a large index move, a risk gate
  nearing breach).

## Optional: a live dashboard

A published HTML Artifact with the `db` runtime capability declared makes a good
shared view of account state, risk gates, desk status, the decision log, and the trade
log — written to on every check-in via `write_db`, read live by any open viewer via
`onSnapshot` (no republish needed for routine data updates). A few things that matter
if you build one:

- Treat it as **private financial data** — don't share it publicly, and avoid
  hardcoding real account numbers in anything checked into a public repo; mask them
  (e.g. `••••1234`) in the UI instead.
- Show desk status (idle/running) by actually flipping a stored status field when you
  spawn a desk and again when it reports back — a fake animation that doesn't reflect
  real activity is worse than no status indicator.
- If you add an in-page chat via the `sample` capability, be explicit in the UI that
  it's a **separate, memory-less, tool-less** quick-answer assistant — it cannot place,
  cancel, or modify any order, and has no access to the live trading session beyond a
  static data snapshot you pass it in the prompt. Log the user's message to a shared
  doc as well (not just the instant reply) so the actual trading session — which can't
  be woken by dashboard activity alone — picks it up and gives a real answer at its
  next check-in, tagged distinctly from the instant quick-answer bot so the user can
  tell which is which.

## Hard constraints worth knowing before you hit them

- **Harness tool-approval gates aren't bypassed by chat "yes."** See "Connecting the
  server" above — applies to `claude mcp add` and to order-placing tools alike.
- **Fractional and dollar-based equity orders are only valid on `type=market` with
  `market_hours=regular_hours`** — rejected on limit orders and on extended/all-day
  hours sessions. If you need an immediate fill outside regular hours, use a
  whole-share limit order tagged to that session instead.
- **A `regular_hours`-tagged order placed before the market opens queues** (state:
  "queued") rather than being rejected, and fills automatically at the open — useful
  when a pre-market thesis needs a fractional/dollar-based regular-hours order that
  can't itself be tagged `extended_hours`.
- **Crypto agentic execution can be entirely blocked for some account residencies** —
  e.g. a confirmed, non-retryable HTTP 403 for New York residents ("agentic trading is
  not available to New York residents"). Check for this before promising the user
  crypto execution works; if blocked, keep any Crypto Desk strictly research-only and
  say so plainly rather than repeatedly retrying a call that will never succeed.
- **Crypto spreads are much wider than equities** — order of ~1-2% round-trip on major
  pairs on Robinhood — which raises the conviction bar considerably for anything
  short-horizon, independent of whether execution is blocked.

## Standing autopilot authorization

Full autopilot (executing without asking first, on an ongoing schedule) should only run
once the user has explicitly and repeatedly said so in chat — it is not a default for
this setup. A fresh request to set this up should start research-only or
confirm-before-execute, matching the safety posture Section B defaults to, until the
user grants standing authorization themselves.
