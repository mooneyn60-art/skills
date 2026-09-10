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


**A desk's universe is the one you give it.** A performance desk handed five
trades reported the account's realised P&L as a fraction of the true figure,
because two closed trades were never in its brief. It was not wrong; it was
under-informed, and the error was the orchestrator's. Verify any desk claim that
contradicts the broker's own data against the primary source before acting, and
prefer giving desks a tool call they can run themselves over a summary you typed.

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

## Constructing the trade: order of operations

**The defining process failure is acting first and analysing second.** In one
session every stop on the book was placed from ATR heuristics and round numbers,
and a Technical Levels desk later found *all five* badly placed — one sitting
inside a dense shelf of prior lows, one exactly on a double bottom, one two cents
above a low it would have been swept by twice that week, one so far away it was
inert rather than protective. In the same session a position was bought and
described as a diversifier; a Scenario desk later measured it at +0.95 beta to
the sector the book was already concentrated in, with correlation to the largest
holding *rising* to 0.59 on down days. Both failures had one cause: the desks
were doing forensics on decisions already executed.

Run these in order. Each step's output is the next step's input.

**1. Level first — before size, before deciding to buy at all.** Pull
historicals and ATR. The stop belongs *below* structure: a swing low, a volume
shelf, a double bottom. Never *at* a prior low and never inside a cluster of
lows — those are where stops get swept, which is a different thing from where a
thesis breaks. Minimum ~1.5 ATR from entry. **If the chart offers no clean level,
there is no trade.** A position you cannot define a stop for is a position you
cannot size.

**2. Size from the stop, not from a dollar habit.** This is the core inversion.
Sizing by a fixed dollar band and then placing a stop wherever leaves risk as
whatever falls out. Instead fix the risk and solve for size:

```
shares = risk_budget / (entry - stop)
```

with `risk_budget` a small fixed fraction of the account (~1–1.25%). A wide-stop
name gets a small position, a tight-stop name a larger one, and **every trade
risks the same amount** regardless of price or volatility. Then apply the caps
(≤20% of equity per new position, none above ~30%) and one more: **skip anything
whose resulting notional is too small to matter.** A position that cannot move
the book is a tax on attention — one account carried a $23 holding that could
not be stopped, hedged, or meaningfully sized up, and existed only to be
reported on.

**3. Prefer whole shares.** Stop orders **cannot be fractional.** Every
fractional share bought is therefore permanently unstoppable. In one account the
slivers left outside stop coverage — the 0.10 of a share here, the 0.84 there —
totalled 7.5% of the account with no protection at all, purely as an artifact of
buying "$75 of a thing" instead of "7 shares." Round down to whole shares unless
the share price makes that impossible.

**4. Test correlation before the buy, and test it on down days.** Never call
something a diversifier because of its sector label. Pull returns for the
candidate and the largest holdings and measure. Correlations rise in
drawdowns — the number that matters is the one conditional on the market falling,
not the unconditional one.

**5. Portfolio heat.** Sum `(price - stop) x stopped shares` across every open
position. That total is what the book loses if everything stops out at once. Keep
it under a fixed ceiling (~6% of the account) and report it every check-in. It is
the only number that answers "how much am I actually risking right now."

**6. Recompute concentration after every fill — including sells.** A sell is a
concentration event. Trimming half of one position mechanically raised another
holding to 33.8% of equity, breaching a 30% cap that had been respected before
the "risk-reducing" trade.

**7. Stops are resting orders, not notes.** A level recorded in a prompt only
works if the session happens to be awake when price reaches it. Place real GTC
stops. Then re-check every stop on every pass against **both** structure and cost
basis, because a winner that runs turns its own stop defective — see the gain
protection gate below.

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

**4. Gain protection.** Before setting *or accepting* any stop, check it against
cost basis. A stop that hands back most of an existing gain is a defect, not a
plan. This recurs because chart levels and cost basis are computed by different
people at different times: a stop placed at a moving average sat 1.5% above cost
on the book's largest position and would have surrendered 84% of the gain; a
stop later raised on a winner *still* sat below cost after the position ran, so
triggering it would have converted a profit into a loss. Two mechanical checks
catch both: what dollar gain remains if this stop fires, and is this stop above
or below cost? Label every stop **loss-taking** or **gain-protecting** and never
let the two be confused.

**5. Never buy because the user asked.** A user pushing for activity is not
evidence. Re-run the work when pushed — genuinely re-run it, since the pressure
may be pointing at a real gap — but if nothing clears, "nothing qualifies" is the
answer. The corollary matters too: when a user's push *does* surface something
real, act on the evidence and say which evidence changed the call, so neither of
you confuses compliance with analysis.

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

- **Stop orders cannot be fractional**, and a position under one whole share
  cannot be stopped at all. Stops also cover only the whole-share portion, so a
  1.10-share holding with a 1-share stop leaves 0.10 unprotected. Plan share
  counts accordingly at purchase — this is not fixable afterwards.
- **A stop is a trigger, not a price.** If the underlying gaps below the stop
  overnight or on a pre-market print, the order triggers and fills at the *open*,
  not at the stop price. Stops protect against a slide, never against a gap. The
  only hedge for gap risk is position size.
- **A stop sells whole shares FIFO, not at blended average cost.** Estimating the
  realised P&L of a stop using the broker's displayed average cost overstates it
  whenever the oldest lot is the expensive one. Pull the actual tax lots. In one
  case the naive blended estimate was 35% too high because FIFO sold an
  underwater lot first.
- **Use specified-lot selling on partial exits.** Pull tax lots and sell the
  highest-cost lots first to minimise the realised gain. Default FIFO will
  cheerfully sell the cheapest lot and hand the user a larger tax bill for the
  identical trade.

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


### Options in a small account: run the multiplier first

Users ask for options because the upside is real. The gating fact is arithmetic,
not caution: **one contract is 100 shares.** Check that against the account
before any research into strikes or expirations, because it usually ends the
question.

- **Covered calls** require 100 shares of the underlying. A covered call is only
  conservative when that block is a modest slice of the book, which means
  **account >= ~400x the share price** for 100 shares to be ~25% of it. Below
  that threshold the "safe" income trade is a 70–90% single-name concentration
  bet wearing a conservative label.
- **Cash-secured puts** require 100 x strike in cash. Divide available cash by
  100 to get the maximum strike; on a small account that lands below the price of
  anything worth owning.
- **Protective puts do not work on fractional positions.** This is the argument
  that is easiest to miss and hardest to recover from. A put on 100 shares held
  against a 1.1-share position is not insurance — it is a naked short-delta bet
  hedging ~90x more stock than is owned. Check share count against contract size
  before calling anything a hedge.
- **A hedge must be measured against the loss it removes, not bought on
  narrative.** A delta-matched index put priced at the best available execution
  paid *zero* across the entire realistic drawdown range and only fired past a
  two-day index drop the chain itself priced at ~2.6%. It made the modelled worst
  case worse by the premium. The at-the-money put that *would* have covered the
  loss cost ~31% of the account. Price the payoff table before concluding a hedge
  hedges.
- **Cheap contracts are cheap because they have no bid.** Below a certain premium
  the quotes go one-sided — you can buy, but there is nothing to sell into.
  Screen on open interest and round-trip spread as a percentage of mark;
  spreads of 20–40% make positive expected value arithmetically unreachable long
  before direction matters. Brokers often publish a probability-of-profit field:
  on affordable far-OTM contracts it is routinely ~5%.
- **The evidence base is not ambiguous.** Studies using actual retail fills put
  average retail option purchase returns around -4%, with the losses attributed
  largely to transaction costs rather than wrong direction.

The constructive version is a threshold rather than a refusal: name the account
size at which each structure becomes genuinely conservative, and revisit then. If
a process has not yet demonstrated a payoff ratio above 1 in equities, adding an
instrument that decays and can go to zero is leverage on an unmeasured edge.

### Share count is a distance-to-support measurement in disguise

A run of candidates was rejected for "resolves to only 1 share" — four out of
fourteen in a single session. That reads like a sizing rule being fussy on a small
account. It is not. It is the sizing arithmetic correctly detecting a bad entry,
and the diagnosis is worth making explicit because the symptom looks financial
and the cause is technical.

`shares = risk_budget / (entry − stop)`, and the stop is placed below real
structure. So share count is inversely proportional to **the distance from the
entry to the nearest support**. Measured on the rejected names: the only clean
stop sat 9.7%, 9.3% and 8.2% below the entry respectively. None of those was an
ATR problem — an ordinary 3%-ATR name at 1.5 ATR needs only a 4.5% stop and sizes
to four or five shares comfortably. The stops were wide because the stocks had
already travelled far above their last swing low.

**So "this resolves to 1 share" and "this entry is extended" are the same
finding.** It also unifies with the range-location test: entries in the top
quartile of *that name's* 60-session range drew down ≥9.5% within ten sessions
**20.1%** of the time, against **8.3%** from its bottom quartile (a per-name
gradient — pooled across names the effect is nearly flat; see the location test
below). Extended entry → distant
support → wide stop → few shares → and, independently measured, a materially
higher chance of a deep drawdown. Three symptoms, one cause.

The trap this creates is that **a momentum screen manufactures the problem it is
meant to solve.** A "≥2% day change" filter selects, by construction, for names
that have just moved away from their support. The screen built to find movers is
the same screen that produces unsizeable, high-drawdown entries — and the failure
arrives disguised as a position-sizing complaint, three steps downstream, where
nobody connects it back to the filter. Lower the day-change threshold, or add an
explicit proximity-to-structure screen, and the share counts fix themselves.

**Corollary for building a diversified book on a small account.** In a five-name
book where two positions are 61% of equity, "diversification" is not a sector
problem — the two largest measured at 0.18 correlation and were not a bloc. It is
a **position-count and position-size** problem, and single-name risk (a guidance
cut, a fraud, a failed trial) is what actually hurts. So the fix is more
positions, smaller each, which runs directly into the share-count arithmetic
above. Two checks make the budget concrete rather than aspirational:

- **Heat is the real position budget.** Room for new positions = (heat cap −
  current heat) ÷ per-trade risk. At a 6% cap on ~$1,100 with heat at 2.9%, that
  is roughly $34 of headroom, or three to five more positions at full budget —
  a number, not a vibe.
- **When the notional cap binds before the risk budget, you are in the right
  price band.** In the $8–35 range every candidate produced four to nine whole
  shares and hit the 20%-of-equity notional ceiling first. That is the signature
  of a sizeable entry. When the *share count* binds first, the entry is extended
  and the problem is location, not price.

### Calibrating the veto: a Red Team that always kills is a wall, not a filter

A mandatory adversarial review before every entry is the highest-value gate in
the process — it has caught two inverted-sign theses that no other desk saw. It
also drifts, in a specific and predictable direction: **an agent asked to find
what is wrong will always find something, and absent a rule about what counts,
every finding gets treated as fatal.** Measured symptom: a 100% kill rate. At
that point the desk is not filtering, and its output carries no information.

The drift is not a sign the desk is wrong. Both kills looked correct on
evidence. It is a sign the *verdict mapping* is missing — the step between
"I found a flaw" and "therefore no trade."

**Only three findings should kill:**

1. **The thesis has the wrong sign.** The position makes money in the opposite
   state of the world from the one it was bought for. This is the classic and it
   is unfixable by price or size.
2. **A load-bearing fact cannot be verified.** Not any unverified fact — one the
   trade depends on. State which, and why it is load-bearing.
3. **The risk is uncontainable.** No stop placement bounds the loss: gap risk on
   a binary event, an unhedgeable overnight, a structure that can go to zero
   without trading through the stop.

**Everything else is RESIZE or REPRICE, not KILL.** Entry too high, stop on the
wrong level, position too large, timing poor, valuation rich, guidance soft — none
of these mean the trade is wrong. They mean *this version* of it is wrong, and the
correct output is the version that is right: a different price, a different stop, a
smaller size, or a named condition to wait for. A desk that answers "no" when it
could answer "not here, but at $10.90 with a stop at $10.20" is destroying
information it already produced.

Three rules keep it honest:

- **State the cost of being wrong.** Every KILL must say what the trade does if the
  objection is invalid — the forgone move, in dollars, at the proposed size. A veto
  with no downside attached will be used freely.
- **Score the vetoes.** Log every kill with the price at the time and a review date,
  and mark it to market later. A rejection log that is never scored measures nothing,
  and the desk that generates rejections should be the one held to their outcome.
  Score the *thesis*, not the next session: a kill premised on behavior around an
  event is not scoreable until the event happens.
- **Report near-misses.** "PROCEED, and here is the strongest surviving objection"
  is more useful than either a clean pass or a kill, because it tells the operator
  what to watch after entry.

The underlying asymmetry is real and worth stating plainly: a bad trade costs the
risk budget, and a missed trade costs the whole gain. On a small non-replenishable
bankroll the first feels worse and the second is invisible, which is exactly why an
unscored veto ratchets tighter over time until nothing passes.

### Match the correlation test to the claimed ROLE, not to the book

Two trades have now died on an inverted sign, and the second one passed every
test the idea desk ran. That is the interesting part: the tests were real, the
arithmetic was right, and the variable was wrong.

A candidate was proposed as a **disorder hedge** for an AI-heavy book — the pitch
was that an interdealer broker earns fees on trading volume and is therefore paid
by the same chaos that would hurt the rest of the portfolio. The desk tested it
against the book: beta to the largest holding **+0.02**, beta to the sector ETF
**−0.06**, a coin flip on that holding's 21 worst days. Genuinely orthogonal, and
every number held up on re-check.

Then Red Team tested it against **volatility itself**, which is what the thesis
actually claimed:

| | |
|---|---|
| correlation to a VIX proxy | **−0.167** |
| top 20 volatility-**spike** days | +0.045%, up 8/20 |
| top 20 volatility-**collapse** days | **+1.317%, up 15/20** |

It is a short-volatility asset. Every dollar it earned on a macro-sensitive day, it
earned when volatility *fell*. It would have been bought as protection against a
volatility event, two days before a scheduled one, with volatility already at a
one-year low.

**The rule: a correlation test answers only the question you asked it.**
"Uncorrelated to what I own" and "rises when the thing I fear happens" are
different claims requiring different regressors, and passing the first says
nothing about the second. Before running the numbers, write down the role the
position is supposed to play, then pick the regressor from the role:

| Claimed role | Regress against |
|---|---|
| Diversifier | the existing book, and each holding separately |
| Volatility hedge | a VIX proxy — *not* the book |
| Inflation hedge | breakevens or a rates proxy, on print days specifically |
| Defensive / risk-off | the market, conditioned on down days only |

The failure has a signature worth memorising: **any thesis of the form "X profits
from chaos" is where inverted signs hide** — chaos beneficiaries are the most
narratively appealing and least frequently measured trades on the board. Gold "the
inflation hedge" is really a real-rates asset. Brokers "paid by volatility" really
get paid by volume, which in practice arrives on relief rallies. Test the sign
before the size.

Two supporting checks that came out of the same review and are cheap to run:

- **Locate the entry within the range — but compute the buckets PER NAME.** The
  candidate sat at the **80th percentile** of its trailing 60-session range, and on
  its own history entries from the top quartile went on to a ≥9.5% close-basis
  drawdown **20.1%** of the time within 10 sessions against **8.3%** from the bottom
  quartile — a real 2.4x gradient, and a 2.89 ATR stop sat inside two prior declines
  from that exact price. ⚠️ **This effect does NOT generalise, and an early version of
  this page wrongly said it did.** Pooled across four names and five years (4,756
  observations) the buckets came out **Q1 24.7% / Q2 19.9% / Q3 19.5% / Q4 21.4%** —
  nearly flat, non-monotonic, and with the *bottom* quartile the worst of the four
  (falling knives). So the location test is a per-name diagnostic, never a universal
  law: run the buckets on the actual candidate, and if the gradient is flat, the test
  says nothing and the decision has to rest on something else.
- **Explain the bar your stop rests on.** The structure supporting the stop was a
  single high-volume day. Once identified, that day turned out to be a
  sector-wide repricing on a macro relief headline — peers moved together against a
  flat index — so it was regime residue, not accumulation. Support built by a
  regime disappears when the regime does. An unexplained volume shelf is not
  support; it is an open question wearing support's clothes.

### The risk before a scheduled print is whipsaw, not ruin

The instinct before a known macro event is to de-risk. Measure first — twice now
the measurement has reversed the instinct.

**Model the event, do not narrate it.** Replaying the actual CPI and PPI sessions
of 2026 through a live book cost **$12.91** on the worst of them. The largest
single-day loss in the same three-month sample came from a **non**-CPI day. The
scheduled print was not the tail event; an ordinary Thursday was.

**Overnight gaps are small; full-day moves are large.** Measured worst 3-month
overnight gaps ran −3.11% to −7.41% across five names, while single-day closes
reached −11%. So stop-fill slippage below the opening print is modest, and the
real damage accrues *intraday, after the stops have already filled*. This inverts
the usual worry: the gap is survivable, and being liquidated into it is the cost.

**Which produces the actual failure mode.** On one hot-print session a position
gapped −4.94%, tripped its stop, filled 2.2% below the stop price — and then
closed **+2.83%**. The stop worked exactly as designed and still sold the low of a
day that rallied. Against a scheduled binary, a stop is not protection so much as
a coin-flip liquidation trigger, and tightening one beforehand raises the odds of
being the seller at the worst print of the week.

**Check whether the floor is even reachable before paying to defend it.** Binary
search on the shock size is a two-minute calculation and it ends most de-risking
arguments: with cash at ~38% of the account, the book needed a **−28% single
session** to reach its stop-trading floor, against a −3.01% worst observed gap —
off by roughly an order of magnitude. Selling a winner to hedge a 9-sigma event is
not caution, it is a certain cost against a hypothetical benefit, and on small
positions the spread alone is a material percentage.

**A concentration figure built from sector labels is not a measurement.** Three
names sharing an "AI" label showed a pairwise correlation of **0.18**, falling to
**−0.18 on down days** — not a bloc. Meanwhile the tightest pair in the same book
was a quantum microcap and a consumer fintech at **0.68**. Compute the correlation
matrix, and compute it again conditioned on down days, before calling anything a
concentration or a diversifier. The label has now been wrong three times running.

One caveat that belongs in the same breath: these are calm-regime correlations,
and a common-factor shock compresses dispersion toward 1. Run the stress case with
`max(full-sample beta, down-day beta)` so the conclusion does not depend on the
benign reading being right.

### R-multiple trailing rules break when R is smaller than the noise

The standard asymmetric-exit ladder — breakeven at +1R, trail 1.5 ATR below the
highest close at +2R — is sound in spirit and quietly broken in two specific
ways. Both were caught the same afternoon, on two different positions, and both
produce a stop sitting *inside* normal daily noise. A stop inside noise does not
protect a gain; it donates one.

**Failure 1 — breakeven at +1R, when the entry stop was tighter than 1.5 ATR.**
This one is arithmetic, not bad luck. At exactly +1R, price = entry + R, and
breakeven = entry, so the gap between price and the new stop is **exactly R**.
Therefore moving to breakeven is safe *only if R itself is at least 1.5 ATR*. If
the original stop was placed closer than that, the breakeven stop is guaranteed
to land inside the noise band, on every trade, forever. Measured: a position with
R = $0.54 against ATR(14) = $0.596 — R was **0.91 ATR**, so its breakeven stop
would have sat 0.91 ATR from price, against a 1.5 ATR floor. The real defect was
upstream at entry, and the trailing rule merely inherited and propagated it.

**Failure 2 — "1.5 ATR below the highest close" after a pullback.** The anchor is
the *high*, so once price retreats from it the computed stop can end up far
tighter than intended relative to where the stock actually is — or above it
outright. Measured on the same day: one name's highest close was $230.36 with ATR
$7.46, giving $219.17, only **0.68 ATR** below the $224.27 spot. A second name was
worse — highest close $19.18, ATR $0.82, giving $17.95, which was **above** the
$17.44 market. A rule that can output a stop above the current price is not a
rule you apply literally.

**The fix, in both cases: treat the R-ladder as a request for a tighter stop, not
as a coordinate.** Compute the candidate, then run it through the placement rules
that already exist:

1. Compute both anchors — 1.5 ATR below the highest close, and 1.5 ATR below the
   *current* price.
2. Take the ladder's candidate, but never accept anything closer than 1.5 ATR to
   current price.
3. Move the survivor DOWN to the nearest clean structure level — below a swing
   low or volume shelf, never at one.
4. Ratchet up only. If the result is not above the existing stop, do nothing.
5. Do not tighten at all when a macro print lands within 48 hours: a stop is a
   trigger, not a price, and a tightened stop into a gap just guarantees selling
   at the worst print of the week.

Worked example of step 3: at a +1R trigger of $16.03 with ATR $0.596, breakeven
was $15.49 (0.91 ATR — rejected), the 1.5 ATR line was $15.14, and the nearest
structure was a pair of lows at $15.16 and $15.175, so the correct stop was
**$15.10** — just under both, 1.56 ATR from price, and still a ratchet up from the
resting $14.95. Breakeven would have been 40 cents too tight on a name that
routinely travels 60.

The deeper lesson is that **R and ATR must be reconciled at entry, not at exit.**
Sizing from the stop is correct, but if the stop itself is closer than 1.5 ATR the
position is mis-built from the first second, and every downstream rule that
references R inherits the error.

### Audit the floor across the whole book, not just at entry

Reconciling R and ATR at entry is necessary but not sufficient, because ATR moves
after the stop is placed. A stop set at a legitimate 1.6 ATR drifts inside the
floor the moment volatility expands, and nothing announces it. The only way to
catch this is to periodically recompute `(price - stop) / ATR(14)` for **every**
resting stop and read the column.

Measured on a nine-position book: **seven of nine stops sat inside the 1.5 ATR
floor**, two of them at 0.60-0.62 ATR — a stop less than two thirds of one average
daily range from spot, which an ordinary session touches by chance. The book was
configured to donate on noise, and no single decision had created it. It was the
accumulated drift of stops placed correctly at different times under different
volatility, plus a batch placed in a hurry to cover unstopped overnight risk.
Entry discipline had been fine each time. The *portfolio* had still degraded.

Run the audit as a table, not per-position — the pattern is only visible pooled.

### The floor does not apply to a stop that sits above cost

This is the exemption that nearly got missed, and getting it wrong would have
been expensive. The 1.5 ATR floor governs an **initial-risk** stop, where the
question is "how much am I willing to lose." A stop that has ratcheted above cost
basis is answering a completely different question — "how much locked profit am I
willing to give back to avoid being shaken out" — and the floor has no authority
over it.

In the audited book, the two worst offenders by ATR multiple were also the only
two stops above cost. One locked **+$6.13/share** on a position whose basis was
$208.37 with the stop at $214.50. Mechanically applying the floor would have
pushed that stop to $208.22 and converted a guaranteed winner into a scratch, in
the name of risk management. Widening a profit stop to satisfy a risk rule is not
risk management; it is surrendering realized edge to a rule that was never
scoped to it.

So partition the book by `stop vs cost basis` **before** applying the floor:
- stop below cost → initial-risk stop → the 1.5 ATR floor governs
- stop above cost → profit-protecting stop → the floor is silent; the trade-off
  is give-back versus shakeout, and it is decided on structure, not on ATR

### Test the widening rule against motivated reasoning

Widening a stop on a position that is down is the single most self-serving action
available, and every rationalization for it sounds like risk management. Before
acting on a floor violation, run the test: **does the rule fire on ATR, or does it
fire on PnL?**

The audited book passed the test cleanly, and the proof was in which names were
*not* touched. The largest loser on the book, down **21.7%**, needed no change —
its stop was already 1.83 ATR out. A position sitting essentially flat, down
0.2%, *did* need widening at 0.97 ATR. The correction set was uncorrelated with
the loss set, which is what distinguishes a rule from an excuse.

If a floor audit ever proposes widening stops on exactly the losers and nothing
else, the rule is not the thing driving it. Stop and re-derive.

### Cost basis: the position endpoint is not the tax lot

Three separate errors have now come from treating a broker's displayed average
cost as the basis. They are worth separating because they have different causes.

**1. After a partial sell, the displayed average is recomputed and no longer
matches the remaining lot.** Measured: a position endpoint reported an average
buy price of $206.84 while the single remaining tax lot carried a cost per share
of **$208.37** — a $1.53 gap on a one-share position, and it silently propagated
into a locked-gain figure that was overstated by 25%. The tax lot is the
authority for what is actually held. Pull it before quoting basis, locked gain,
or recovery price on any position that has ever been partially sold.

**2. A blended average hides lot dispersion, and dispersion is what a stop
actually sells.** A 1.11-share position showed a tidy $170.47 blended cost. The
lots underneath were **0.31 @ $136.29** and **0.80 @ $183.71** — a $47 spread, one
lot deeply green and the other deeply red. Blended math priced a stop-out at
−$4.97. FIFO priced it at **−$3.50**, because FIFO sells the *oldest* lot first
and the oldest lot here was the winner. Same trade, 30% different answer.

**3. Stops are always FIFO and cannot be told otherwise.** Specified-lot selling
is rejected on stop orders at the API layer — the `tax_lots` parameter is not
accepted alongside `stop_market` or `stop_limit`. So every resting stop liquidates
oldest-lot-first no matter what the tax-efficient choice would have been. This has
a consequence worth planning around: on the position above, a stop selling one
whole share consumes the entire profitable lot plus most of the losing one and
leaves **0.11 shares of the worst lot behind, unstoppable** — the position is
reduced to an unprotected fragment of its own worst entry. When lot dispersion is
wide, a *manual* specified-lot exit and a *stop* exit are materially different
trades, and only one of them is selectable.

The general rule: **call the tax-lot endpoint before any exit decision, and model
the exit FIFO unless you are placing a market or limit order that can actually
carry a `tax_lots` selection.** Blended cost is a display convenience, not a
basis, and the error it produces is not random — it is largest exactly when lots
are most dispersed, which is exactly when the exit decision matters most.

### The floor test: what actually blocks a small-account option

The multiplier check above kills covered calls and cash-secured puts outright.
It does **not** kill a long call or put, and the reflex reason usually given for
killing those — "the friction is prohibitive on cheap contracts" — is an
assumption, not a measurement. Measure it before using it.

Measured on a liquid mid-cap (SOFI at $17.44, 37 DTE, Oct-16 chain):

| Strike | Mark | Bid/ask spread | Open interest | Delta | Broker P(profit) |
|--------|------|----------------|---------------|-------|------------------|
| $18 | $1.045 | **$0.01 (1.0%)** | 11,144 | 0.50 | 30.7% |
| $19 | $0.675 | $0.01 (1.5%) | 11,746 | 0.37 | 24.1% |
| $20 | $0.435 | $0.01 (2.3%) | 26,837 | 0.27 | 17.8% |
| $21 | $0.285 | $0.01 (3.5%) | 9,276 | 0.19 | 12.8% |

Friction is a non-issue here. A penny-wide market on a $1.045 mark is better
execution than most equity trades get. So the honest blocker is somewhere else,
and it is this:

> **A long option can go to zero. Therefore the premium is not risk-sized against
> the account — it is spent against the drawdown headroom the account has left
> before its floor. Premium must be less than that headroom, not less than some
> percentage of equity.**

Run it as one line: `max premium = (total value - floor) x (fraction of the
remaining bankroll you will stake on one binary)`. On an account at $1,101 with a
$1,007 floor, headroom is $94. Staking even a quarter of the *entire remaining
life of the account* on one contract caps premium near $23 — and at $23 the only
contracts available are the 12-18% probability tickets at the bottom of the table,
which the gates already forbid as lottery tickets. The one contract with a real
delta and a real market costs $105, which exceeds the total headroom: buying it
and having it expire worthless breaches the floor by itself, with no adverse move
required anywhere else in the book.

That is a clean, arithmetic no — and it fails for a different reason than the
covered call does, so say which one. Note also what the test implies: the
constraint tightens as the account approaches its floor and loosens as it earns.
It is a threshold, not a verdict.

### Options desks

When a user asks for options coverage, standing desks beat an ad-hoc round: the
qualifying case is rare and narrow, so something has to be looking for it daily
rather than only when asked. Four desks, none of which can execute:

| Desk | Job | Never |
|------|-----|-------|
| **Options Structure** | Given a thesis that already passed the equity gates, decide whether an option is the *right expression* of it, and which one: direction, strike, expiration, and the reason a share position would not do the same job better. | Propose a structure the account's approval level cannot trade. Level 2 is long calls/puts, covered calls and cash-secured puts — **no spreads**, so "defined risk" means 100% of premium, not a debit spread's width. |
| **Options Liquidity** | Measure, never assume: bid/ask as a percentage of mark, open interest, contract volume, and the round-trip cost of getting back out. Publish the table. | Accept a mark as tradable without checking there is a bid to sell into. |
| **Options Risk** | Run the floor test and the multiplier check. Convert premium into "percentage of the account's remaining life." Size or kill. | Express option risk as a percentage of equity. A long option is a binary against the floor. |
| **Options Flow** (existing, signal-only) | Unusual volume/OI as an institutional-positioning proxy. | Propose a trade. It reads the tape; it does not take it. |

The order is fixed and it is not the intuitive one: **Structure first, Liquidity
second, Risk last.** Running Risk first produces a budget, and a budget makes the
desk shop for whatever fits it — which is precisely how a process ends up holding
a 13%-probability far-OTM ticket it can defend on price. Thesis, then execution
quality, then affordability. If affordability kills it, that is the correct
outcome and the research was not wasted: it produces a *threshold* to revisit.

Red Team remains mandatory on top of all four. An options KILL is cheaper than an
equity KILL, because the loss is not bounded by a stop — there is no stop on a
long option that gaps to zero over a weekend.

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

### A resting limit below the market is adverse-selected by the event

This is the disqualifier that killed an otherwise-clean candidate, and it is not
obvious, so it is worth stating as a rule.

A research desk proposed the standard patient entry: rest a limit **below** the
market into a scheduled macro print, on the reasoning that it costs nothing if
unfilled and only fills at a better price. That reasoning is wrong whenever the
print is what moves the price, because it ignores **what the fill is conditioned
on**.

The limit fills on the hot print and does not fill on the cool one. So the
position is acquired *only in the macro state that hurts*, and the "better price"
is better precisely because the scenario is worse. That is adverse selection, not
patience.

It compounds badly when the name's measured correlation to the existing book is
positive in the current regime: the fill arrives on the day the rest of the book
is also down, so the new position adds beta at the exact moment of maximum
drawdown. In the case that produced this rule, the candidate's headline
correlation to the book was **−0.15** over three months but **+0.42** over the
most recent 13 sessions, and **+0.45** on the days the book's largest holding
fell. The trade was pitched as diversification and would have delivered
concentration, on the worst possible day, by construction.

Rules that follow:
- A resting buy limit below the market is only patient when the thing that would
  fill it is *noise*. Into a scheduled binary event, the event is not noise, and
  the limit becomes a conditional bet on the bad outcome.
- Before resting any limit through an event, ask: *in which macro state does this
  fill, and do I want this exposure in that state?* If the answer is "it fills in
  the state I'm hurt by," don't place it.
- Correlation must be quoted over the regime being traded, not the longest window
  available. A diversification label from a prior regime is not evidence.

### A moving-average filter detects MA collapse, not price strength

A screen requiring "price above its 100-day MA" was doing almost none of the work
it was designed for. Reviewed against the actual hits, **five of eight candidates
sat above a flat or falling 100-day MA** — the filter was passing names whose
average was descending toward the price rather than names whose price was leading
a rising average. One hit was 2.9% "above" a 100-day MA that had fallen from
32.93 to 32.63 over four sessions.

`price > MA` is a *position* test. Trend requires a *slope* test, and they diverge
exactly during the topping process the screen exists to avoid.

Where the expression language exposes no lag or offset operator (so a true slope
`MA_t > MA_{t-n}` cannot be written), the workable proxy is a **shorter average
over a longer one** — `closeAvg(50d) / closeAvg(100d)`. Note the threshold
matters more than it looks: at `> 1.0` the proxy is nearly useless, because a
100-day average that has just rolled over still sits below its 50-day for weeks.
The name with the visibly-falling MA above scored **1.0080** and passed. Requiring
**`> 1.02`** — the intermediate trend decisively, not marginally, above the long
trend — removed it and five other marginal-trend names, cutting the hit list from
35 to 29 while keeping every candidate that had survived on fundamentals.

Generalize: when a filter is a proxy for the thing you actually want, calibrate
its threshold against a known-bad example, not against intuition. A proxy at its
natural boundary usually screens out nothing.
