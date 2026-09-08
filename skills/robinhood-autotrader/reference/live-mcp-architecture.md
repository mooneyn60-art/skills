# Live in-session trading architecture (Robinhood Trading MCP)

Reference for Section A of `SKILL.md` — running autonomous or semi-autonomous
Robinhood trading directly inside a Claude Code session, via Robinhood's official
Trading MCP server (`agent.robinhood.com/mcp/trading`). This is Robinhood's own
agentic-trading feature: OAuth-based, connected to a Robinhood-side account the
user controls — normally a dedicated "agentic" sub-account, separate from their
primary brokerage/IRA accounts, so a bug or a bad decision cannot reach money
outside the sandbox the user chose. It is not `robin_stocks` and carries none of
that unofficial-client ToS risk; see Section B for that different path.

Everything below was learned running a real (small) account. Where a rule exists
because something went wrong, the incident is named — those are the parts most
worth keeping.

## Connecting the server

`claude mcp add` (or the equivalent connector flow), then the user completes
OAuth in their browser. Adding the server and the first order-placing calls
(`review_equity_order`, `place_equity_order`) commonly hit a harness-level
tool-approval classifier that **chat approval cannot bypass** — the user has to
approve interactively outside the conversation. If order calls keep getting
blocked after the user has said "yes" in chat, that is almost certainly this.
Explain the distinction instead of retrying, and never treat a chat "approved"
as evidence the tool actually unblocked.

## The "personal trading firm" model

Two structurally separate roles:

- **Research desks** — independent subagents (`Agent` tool, `subagent_type:
  "general-purpose"`). Every desk prompt must say explicitly: **never call any
  order-placing tool.** Give them query/read tools, not `place_*`/`review_*`.
- **Risk/Portfolio Manager** — the main session, and only the main session. It
  receives every report, runs the gates, and is the sole holder of execution
  authority. No desk output becomes an order without passing the gates.

**Subagents are isolated processes and cannot message each other.** There is no
shared room, no channel, no common memory. The main session is the switchboard:
it fans context out (the wire, below) and routes findings between desks
(cross-examination, below). Do not promise the user a "world where the agents
talk" — it does not exist. A shared scratchpad does not fix it either, because
desks spawned together run concurrently, so whatever one writes usually is not
there when another looks.

### Round structure

Run a round in stages, not as one undifferentiated spawn:

**Stage A — Wire Desk (first, alone).** One read-only subagent produces the
shared factual baseline: macro (rate expectations, imminent prints, yields — a
long-bond ETF like TLT is a good cross-check on whether rate *fear* is actually
building), big-company news large enough to drag a sector, and policy (tariffs,
legislation, regulatory decisions, geopolitics). It also flags anything touching
a current holding, and states plainly what it thinks is *not* priced in, marked
as opinion.

Its output is written to be pasted verbatim into every downstream desk. This is
the single highest-leverage structural choice available: without it, four desks
each run their own broad macro search, producing four slightly different
pictures of the world at four times the cost. With it, one search, and the
confirmation gate gets teeth because desks are finally arguing from identical
facts. Downstream desks must then be *forbidden* from running their own broad
macro searches (narrow searches on their own candidate are fine).

**Stage B — Analysis desks (up to 3, spawned together in one message so they run
concurrently).** A regime read, an idea-generation desk driven by saved scanners,
and one rotating slot. Tell every desk at spawn that its findings will be put to
a rival desk for challenge — it changes how they write, toward defensible
specifics and stated confidence levels.

**Stage C — Cross-examination.** Where two desks genuinely conflict, reopen one
with `SendMessage` (which preserves its context), quote the rival finding
verbatim, and ask it to defend, concede, or refine. Cap it — two exchanges, only
on real conflicts, skipped entirely when desks agree. Never manufacture a debate
to look thorough. *This exists because a Crowd Desk once proposed a name and a
Social Desk independently rejected the same name in the same round, and the
conflict was resolved unilaterally at the gate instead of by letting them argue
it out.*

**Stage C2 — Red Team (mandatory before any buy).** One desk whose entire job is
to kill the proposed trade: dilution and share-count history, cash burn and
runway, insider selling, litigation, customer concentration, accounting
oddities, whether the "catalyst" is already priced, and whether a dip has a
bad-news cause the proposing desk missed. It must end with an explicit verdict —
KILL / RESIZE / PROCEED — and name the one fact that would most change it.
*This exists because a buy was executed on a read describing a $700M convertible
offering as "routine." It was a convert plus a concurrent equity placement at a
price below the entry, with a large holder selling into it — a live overhang. A
red team would have caught that before the trade rather than after.* If Red Team
says KILL the trade dies; if RESIZE, halve it; overruling it requires writing
down why.

**Stage D — Gates.** See below.

### Desk roster

Treat these as independent research *angles*. Add one when there is a genuinely
distinct signal to bring in; stop when a new desk would mostly restate an
existing one. Every spawn is real cost on a live-money account.

| Desk | Signal |
|---|---|
| Wire | Shared macro/company/policy baseline (runs first, alone) |
| Regime | Risk-on / risk-off / choppy from index technicals |
| Idea | Scanner-driven momentum and mean-reversion candidates with a verified catalyst |
| Portfolio Review | Which existing holdings do *not* deserve their capital |
| Performance | Post-mortems closed trades against their original theses |
| Red Team | Kills the proposed buy (mandatory pre-execution) |
| Political Flow | Public STOCK Act disclosures, congressional-trading ETF positioning |
| Popularity / Crowd | What the broker's own users are buying |
| Options Flow | Unusual volume/OI as institutional-positioning proxy — **signal-only** |
| Earnings / Catalyst | Post-earnings drift, and the defensive calendar |
| Social Sentiment | Web-wide chatter beyond the broker's userbase |

**Portfolio Review** earns its slot: pointed at "which holdings don't deserve
their capital," it once overturned the manager's own assumption — the position
expected to be cut (down 22%) was defensible on forward-looking grounds, while a
different, *profitable-looking* holding turned out to be pre-revenue with burn
accelerating nearly 3x year-over-year. It also found the book was ~58% one factor
when the manager believed it was ~33%.

**Performance** is how the firm actually learns. For every closed position it
compares outcome to original thesis and classifies: right thesis/right outcome;
right thesis/wrong outcome (variance); **wrong thesis/right outcome (luck — the
most dangerous, because it teaches the wrong lesson)**; wrong thesis/wrong
outcome. Then hit rate, average win vs. average loss, whether the gates *added or
cost* value (did rejected ideas go on to work?), and the single biggest recurring
mistake. Instruct it to be brutal; a flattering performance review is worthless.

**Options Flow must be signal-only** — it never proposes an options trade. Its
job is to raise or lower conviction on an equity candidate another desk found.

## The gates

**1. Confirmation.** Cross-check every proposal against the wire, the regime
call, other desks, any cross-examination outcome, and the Red Team verdict.
Corroboration across independent desks raises conviction; an unanswered
contradiction kills the idea. A desk that conceded has withdrawn its pick — do
not resurrect it.

**2. Risk & PDT.** New position ≤ ~20% of equity; no position above ~30%;
Pattern Day Trader budget ≤ 3 same-day round trips per rolling 5 business days
for accounts under $25k. Halt new buys if the account is down more than a chosen
percentage intraday or is below the daily hard-stop floor.

**3. Sizing.** Pick a default band for the account size, then halve it when: Red
Team said RESIZE, the name is pre-revenue or cash-burning, it correlates with an
existing large holding, or a major macro print lands within 48 hours.

**The daily hard-stop floor** is the prior trading day's close equity minus the
user's chosen loss limit, recomputed each new trading day.

**Rebase the floor for deposits and withdrawals — never for losses.** A cash
transfer is not a drawdown. This matters more than it sounds: a user withdrawal
once pushed the account below its floor overnight, which would have mechanically
halted all buying over money the user had deliberately taken out — the rule
returning the wrong answer. Detect it by the signature: **equity value unchanged,
cash moved by an exact round number, no orders in the window.** Then rebase, and
*tell the user you are doing it and why.* "Adjust the risk floor" is exactly the
move that must never happen silently, because the same adjustment could be used
to explain away a real trading loss.

## Cadence, and the failure that defines it

**The single most important operational lesson: do not build a monitoring cadence
that consumes the capacity needed to honour it.**

What happened: asked for 5-minute checks plus maximum research, the session built
a self-chaining 5-minute tick that also ran large multi-subagent rounds. It
exhausted the session rate limit by 11:35am ET on a live trading day. The limit
did not reset until the closing bell. The result was **4.5 hours of a live
session with zero monitoring**, including an unwatched stop-loss level on an open
position. It cost nothing only because the stop was not hit — luck, not process.

Rules that follow:

- **The scheduled Routine is the cadence.** No `send_later` self-chaining on a
  short interval. (The Routine scheduler has a hard 1-hour minimum cron interval;
  a tighter cron is rejected outright. Self-chaining is the technical workaround —
  and it is exactly what caused the failure, so do not use it for this.)
- **Cheap light tick every firing, gated desk rounds.** The tick — refresh
  account/positions, check stop levels, check for fills, recompute risk numbers,
  update any dashboard — runs always and uses no subagents. Full desk rounds run
  at most twice per trading day.
- **Unused capacity is the monitoring reserve.** Spending it early is how the
  account goes unwatched later.
- **Honest 1-hour monitoring beats promised 5-minute monitoring that dies at
  lunchtime.** If the user asks for a cadence the budget cannot sustain, say so
  rather than building it.

**Guard the calendar before spending anything.** Check for weekends, market
holidays, and early closes *before the first tool call* — when the market is
closed, not one number in the account can change, so a portfolio pull is pure
waste. Two separate cleanups were needed here: an hourly off-hours routine firing
~60 times across a weekend on a frozen book, and a market-hours routine firing
eight times on Labor Day. Load the exchange holiday list into the routine and
prune the schedule so closed days cost nothing.

**Holidays compress deadlines.** A planned "exit Monday or Tuesday" became
Tuesday-only when Labor Day removed the Monday session, on a position facing a
Wednesday pre-market print. Always re-derive how many *sessions* remain, not how
many days.

## Execution mechanics worth knowing before you hit them

- **Harness tool-approval gates aren't bypassed by chat "yes."** See above.
- **Fractional and dollar-based orders are `type=market` + `market_hours=
  regular_hours` ONLY** — rejected on limit orders and in extended/all-day
  sessions. For an immediate fill outside regular hours, use a whole-share limit
  order tagged to that session.
- **A `regular_hours` order placed pre-market QUEUES and fills at the open**
  rather than being rejected. This is the single most useful execution trick
  here: it converts "I must be awake and active at 9:30" into "the decision is
  already made and will execute itself." Both a pre-market fade exit and a
  time-critical pre-earnings exit were executed this way.
- **Crypto agentic execution can be blocked entirely by residency** — a
  confirmed, non-retryable HTTP 403 for New York residents. Check before
  promising the user crypto execution; if blocked, keep any crypto desk strictly
  research-only and say so plainly rather than retrying a call that will never
  succeed.
- **Crypto spreads are far wider than equities** (order of 1–2% round-trip on
  major pairs), which raises the conviction bar for anything short-horizon
  independent of whether execution is blocked.

## What not to hunt

Users will ask for these by name. They are worth answering with research rather
than a flat refusal, but the honest answer is usually "no":

- **Buying a hot IPO on day one.** The pop accrues to allocation holders at the
  offer price; retail buys the pop, and post-listing performance is generally
  poor. The IPO-adjacent structures that *do* exist are lockup expirations
  (predictable insider supply on a known date) and quiet-period-end initiation
  waves — and note that fading supply requires shorting, which a cash account
  cannot do. Check the actual precedent before assuming the textbook holds: one
  large lockup expiry examined here marked the *bottom*, with the stock closing
  up 6% on unlock day.
- **Buying into an earnings print.** Direction is a coin flip, and it is
  especially indefensible where the company has little reporting history to model
  an implied move from. The defensible version is the other side — post-earnings
  announcement *drift*, entering after the surprise — and even that must be
  checked against the current regime: in a rate-driven multiple-compression tape,
  drift can run *negative*, with every large beat fading. An EPS beat does not fix
  a rate problem.
- **Anything justified by the size of the user's ambition.** See below.

## Ambition, honestly

If the user names a target — "I want to be a millionaire" — do the arithmetic
once, plainly, and then hold the line. From ~$1,000, reaching $1M is roughly
1,000x: about 37 years at 20% annually, ~17 years at 50%, and still about a
decade at 100% *every single year*, which essentially nobody sustains. At small
account sizes the dominant lever is deposits, not returns.

Say it once, without moralising, and then write into the routine that the
ambition **never** justifies loosening a gate, oversizing, chasing, or skipping a
"nothing qualifies" answer. Blowing up while reaching for 1,000x is the most
likely way the account ends.

## Optional: a live dashboard

A published HTML Artifact declaring the `db` capability makes a good shared view
— account state, risk gates, desk status, the wire brief, cross-examination
transcripts, decision log, trade log — written on every check-in via `write_db`
and read live by any open viewer via `onSnapshot`, with no republish needed for
routine data updates.

- Treat it as **private financial data**. Don't hardcode real account numbers in
  anything checked into a public repo; mask them in the UI.
- Show desk status by actually flipping a stored field when a desk is spawned and
  again when it reports. A fake animation is worse than no indicator.
- An in-page chat via the `sample` capability is a **separate, memory-less,
  tool-less** assistant — it cannot place, cancel or modify an order and has no
  access to the live session beyond a snapshot passed in its prompt. Say so in the
  UI. Log the user's message to a shared doc as well, so the real session picks it
  up at its next check-in, and tag those replies distinctly from the instant bot's.
  (A session cannot be woken by dashboard activity alone, so this relay is
  genuinely asynchronous — don't imply otherwise.)

## Standing authorization

Full autopilot — executing without asking, on a schedule — should only run once
the user has explicitly and repeatedly granted it. It is not a default. A fresh
request to set this up starts research-only or confirm-before-execute.

And whatever the authorization level: **report faithfully.** Lead with the bad
news, name the failure before the user finds it, and never let a good week paper
over a process that broke. The monitoring gap above went into the decision log
and into the user's first message of the day, not into a footnote.
