# TARS-1 — Trading Rules

One-line description: The complete, mechanical ruleset TARS trades. No discretion.
Last Updated: 2026-09-16
Status: ACTIVE — TARS confirmed sole writer under R7 (2026-09-15)
Audience: Nolan; any agent or session operating account #731951265

## Overview

These rules exist so that no trade is ever the product of a hunch. Every entry,
exit and size below is computable from price data alone. If a decision cannot be
derived from these rules, it does not get made.

The design assumption is honest: this system has no forecasting edge. It is
built on the one thing with decades of out-of-sample evidence behind it —
trend persistence — and on the one advantage a machine actually has over a
person, which is following its own rule after a loss. Everything here optimises
for surviving long enough for that to matter.

## R1 — Universe

Tradeable: US equities and ETFs, last price > $5.00, 30-day average volume
> 1,000,000 shares. Nothing else. No OTC, no crypto (execution is blocked, 403,
not retryable), no options until R9 opens them.

## R2 — Entry (all five must be true)

  1. Price > 200-day moving average.
  2. Price > 50-day moving average.
  3. Price within 5% of its 20-day high (widened from 3% on 2026-09-14).
  4. No scheduled earnings within the next 3 trading days.
  5. The book holds fewer than 2 positions already in this name's sector
     (added 2026-09-16 — see the sector-cap note below).

Rule 1 is the load-bearing one. Buying below the 200-day MA — "it's cheap now" —
is the rule that tested WORST in this repo's own backtest: -87.7% max drawdown
on the single-stock basket (see `reference/STRATEGY.md`'s `compare_strategies.py`
results and its 2026-09-15 resolution note — this rule is that finding, turned
into a hard gate, closing a contradiction that document flagged and left open
for three days). It is prohibited, permanently, including when the
name looks obviously oversold. Especially then.

Rule 3 was tightened to 3% on day one, which is stricter than the momentum
research this whole system is built on (the 12-1 lookback doesn't care where
in its range a stock sits, only that it's trending). 3% rejected real,
still-trending names (KO, PFE both missed by under 2% today) in favor of only
the ones sitting at the exact top tick. 5% stays a real filter -- still
requires 200d + 50d MA above, still rejects anything not genuinely near its
highs -- it just stops punishing a stock for being 4% off its peak instead of
3%. This is the one knob turned in response to "more profit": more qualifying
setups per scan, not bigger bets or a lower bar on trend quality. Revisit if
it measurably drags win rate down rather than just raising trade count.

Rule 5, the sector cap, was added 2026-09-16 at Nolan's request, and it is
the SECOND thing to occupy the rule-5 slot today -- the first is recorded
immediately below and stays removed. The two are unrelated; do not confuse
them.

What it does: no new entry in a sector where the book already holds two
positions. Sector is read from `get_equity_fundamentals`'s `sector` field,
so it is mechanical and reproducible rather than a judgement call at scan
time. It gates ENTRIES ONLY. It never forces a sale, never overrides R4,
and an existing position that pushes a sector to two (or that was already
there before this rule existed) simply closes that sector to new buys
until one exits on its own stop.

Why it exists: Nolan's observation, and it was correct. The book looked
diversified by sector label -- 8 sectors across 11 names on 2026-09-16 --
while actually holding three near-duplicate pairs: T + VZ (both wireless
telecom, one macro bet held twice), WBD + SIRI (both media/broadcasting),
and TENB + S (both cybersecurity software, which rallied together +12.6%
and +16% on the same 2026-09-14 sector move). Six of eleven positions were
three bets. That is why the 2026-09-16 rotation out of defensives hit the
book broadly while SPY itself stayed green. A prior session had already
applied this reasoning by hand once -- the BAH entry deliberately excluded
Communication Services because it was 5 of 8 positions at the time -- so
this makes an existing informal practice explicit instead of leaving it to
whether a given session remembers to check.

What it does NOT do, stated plainly so it is not oversold: sector
diversification does not protect much in a genuine broad selloff, where
correlations converge toward 1 and every bucket falls together. What
actually bounds a bad day here is position sizing (R3), live stops (R4)
and the cash floor (R3). This rule addresses correlated-sector drawdown,
which is a real and separate risk, and nothing more.

Known limitation, recorded rather than hidden: the `sector` field is a
coarse proxy for correlation, not a measurement of it. Two names in one
sector can be less correlated than two names in different ones -- by this
taxonomy T is "Communications" while WBD is "Consumer Services" even
though both are media-adjacent and move on overlapping news. The cap will
therefore sometimes block a genuinely uncorrelated second name and
sometimes permit a genuinely correlated one. It was still taken because
the failure is bounded and symmetric (one blocked candidate out of many
eligible), while the thing it prevents -- quietly stacking five names onto
one macro bet -- is unbounded. If it starts visibly rejecting good setups
without preventing real concentration, revisit it with the trade log as
evidence rather than on feel.

When this rule was written (2026-09-16, ~17:40 UTC) three sectors sat at
the cap: Technology Services (TENB, S), Communications (T, VZ) and
Consumer Services (WBD, SIRI). That snapshot went stale within the hour --
VZ and SIRI were sold in the rotation this rule prompted, so Communications
and Consumer Services dropped back to one each, while REXR's entry took
Finance to two. As of the end of 2026-09-16 the capped sectors are
**Technology Services (TENB, S)** and **Finance (NAVI, REXR)**.

Do not trust either snapshot. Any session evaluating rule 5 must count the
CURRENT book's sectors from `get_equity_positions` plus
`get_equity_fundamentals`, not read a number out of this file -- a cap list
written into a document is wrong the moment a stop fires.

A DIFFERENT rule 5 was added and removed earlier the same day (2026-09-16):
a 31-day cooldown on re-entering a symbol closed at a loss. It was REMOVED
the same day on reconsideration -- recorded here rather than silently
deleted, per this file's own append-don't-erase convention. Nolan had asked whether to cap trades per day; the flat version
of that was correctly rejected (it can't tell an exit from an entry, and
R4's stops must fire unconditionally), but the replacement went too far the
other way. The reasoning that killed it: a wash sale doesn't destroy a
loss, it defers it into the new position's cost basis (IRC S1091) -- on
this account's dollar sizes that is a bookkeeping timing wrinkle worth a
few dollars, not a real economic loss. Meanwhile R2 exists specifically to
catch trend continuation, and trend-following strategies whipsaw by nature
-- get stopped out, then the trend resumes and re-qualifies days later
(TENB is this account's own proof that a resumed trend can be worth far
more than a few dollars of deferred tax timing). Blocking a real
re-qualifying signal for a month to avoid a paperwork wrinkle was a bad
trade of a large, uncertain benefit against a small, certain one. See R8 for
the actual fix: flag the trade, don't block it.

## R3 — Sizing

Max **$340** notional per position at entry (was $85, then $180; raised
twice on 2026-09-16). Max **4** concurrent positions (was 12; cut 2026-09-16). Minimum 15% of
account value held in cash at the close of any session (lowered from 40%
on 2026-09-14 -- see note below).

Resized 2026-09-16, at Nolan's direction and on this repo's own evidence.
Twelve positions at ~$70 each cannot produce the outcome this strategy
depends on. `reference/STRATEGY.md`'s single-stock test is explicit: the
entire return advantage came from three names (NVDA +58,827%, AAPL
+11,649%, AMZN +11,492%) and "whatever edge exists lives in catching a
handful of very large winners, not in being right often." With twelve
slots, TENB running +13.6% was worth $17 on an $845 account -- about 2%.
A moonshot cannot move a book it occupies one-twelfth of.

The risk arithmetic still holds at the larger size: 4 positions at $180
is ~21% of the account each, and R4's -8% stop makes each loss ~1.7% of
the account, against ~0.66% under the old sizing. More per trade, but
still small enough that a run of losers is survivable, which is the only
test that matters for an account that is never refilled.

What this does NOT buy: the names that actually drove that backtest are
still out of reach. NVDA at $215 exceeds even the $180 cap, and R12
forbids the fractional workaround. The honest position is that this
sizing change makes winners matter more among the names we CAN hold; it
does not unlock the ones we cannot.

No averaging down, ever. A position is entered once. If it falls, it hits its
stop; it does not get reinforced.

The 40% floor was never in the backtest -- backtest.py and
compare_strategies.py invest fully in whatever qualifies and hold cash only
when nothing does, no artificial minimum. 40% was extra caution stacked on
top of that, borrowed from the 60% buffer in Nolan's original spec. 15% is
close to what 8 positions at the $85 cap naturally leaves in a ~$855 account
anyway (8x85=$680, ~80% invested) -- this brings the rule back in line with
what was actually tested, rather than rationing cash below it on principle.

Full deployment (0% floor) was asked for and refused: this account is never
refilled, so a floor above zero is the one thing standing between a bad
week and game over, not caution for its own sake.

Position count raised 8 -> 12 the same day, for a different reason: the
15% cash floor already caps total invested dollars at ~85% of the account
regardless of slot count (~$728 on this account), so more slots just spread
that same capped exposure across more names when enough real setups exist --
it does not increase total risk, only how finely it's diversified. This is
NOT a route to "no leftover cash": the floor holds regardless of how many
slots are open, by design.

## R4 — Exits

  Hard stop: -8% from fill. Placed as a GTC stop order within 60 seconds of the
             fill being confirmed. A position without a live stop is a bug.
  Breakeven: at +8% unrealised, raise stop to the fill price.
  Trail:     thereafter, stop trails 8% below the highest close since entry,
             raised only, never lowered.
  No fixed profit target. Winners are trailed out, not trimmed early.

**Exits are exhaustive, added 2026-09-16.** A position leaves this book
exactly two ways, and there is no third:

  1. Its R4 stop fires.
  2. It fails R2 on a CLOSING basis -- re-evaluated against the same five
     conditions used to enter, on completed daily bars, not intraday noise.

Nothing else is an exit. Not "it is red today," not "rotate into something
better," not "reorganise the book." Those are the decisions this rule
exists to remove.

Why, measured rather than argued. Two independent results point the same
way. First, this repo's own `paper/expectancy.py` on 2026-09-16: across 11
closed trades, 9 were discretionary and averaged **-0.16R with a 95% CI of
[-0.28R, -0.05R]** -- entirely below zero -- while the mechanical side had
one closed trade and was essentially unmeasured. Second, the literature in
`reference/STRATEGY.md`: Barber & Odean found the most active 20% of
retail investors earned **11.4%/yr against 18.5% for the least active**, a
seven-point annual penalty, and that document's own conclusion is that
"every additional trade has a negative expected contribution before its
thesis is even considered. Trade frequency is a cost, not an opportunity."

On 2026-09-16 this account made eleven trades in one session. Four
rotations were each defensible in isolation and collectively were churn.
This rule is the fix, and it is deliberately blunt because a rule that
admits a "good reason" exception is not a rule -- every discretionary exit
in the ledger had a good reason at the time.

Consequence worth stating plainly: this rule forbids liquidating the book
to reorganise it, including to change position sizing. When R3's sizing
changes, the transition happens as positions exit on their own terms and
are replaced at the new size -- not by selling everything at once. A
mass liquidation is simply the largest possible discretionary exit.

The second leak this closes is the mirror image: `expectancy.py` flagged
that **1 of 1 winners closed under +1R** while losses run to a full 1R by
construction, because the stop guarantees it. If winners are cut below 1R,
expectancy cannot be positive regardless of entry quality. Selling a
position that is working -- to rebalance, to free cash, to feel decisive --
is the specific error. TENB at +13.6% is the live test of this rule.

## R5 — Order types

Entries: limit orders only, priced at or inside the ask, good-for-day. If it
does not fill, it does not get chased.
Stops: stop-market. Slippage on the exit is accepted as the price of certainty
that the exit happens.

## R6 — Circuit breakers

  Two positions stopped out within any rolling 5 trading days
      -> no new entries for the next 3 trading days.
  Account value -15% below its high-water mark
      -> halt all new entries, flatten nothing, report and wait for Nolan.
  Any rule in this file cannot be evaluated (data missing, tool erroring)
      -> no trade. A missing input is never treated as a passing test.

## R7 — Single writer

Only one agent places orders into this account at a time. Two agents managing
one book will cancel each other's stops. Before trading, confirm the other is
stood down.

## R8 — Logging

Every order is appended to paper/trades.jsonl with the rule number that
triggered it. Every closed trade is scored in R-multiples and against SPY held
over the identical window, so that a rising market does not get recorded as
skill.

Wash-sale flag, 2026-09-16: when an entry re-buys a symbol closed at a loss
within the prior 30 days, add `"wash_sale_flag": true` and the id of the
loss trade it washes against to the new entry's record. This does not gate
the trade -- see R2's removed-and-recorded rule 5 for why -- it exists so
`reference/TAX_TREATMENT.md`'s documented gap (this ledger has no way to
mark a deferred loss) is actually closed at the point of logging, when the
dates are known and cheap to check, rather than reconstructed later from
timestamps at tax time.

## R9 — Options

Locked until: account value > $2,000 AND 20 closed equity trades logged. Then
long calls/puts only, 30-45+ DTE, max $50 per position. Never 0DTE, never naked
calls, never uncovered puts.

Scoped, 2026-09-14 (Nolan's call, and a good one): once open, options are only
taken on names this system ALREADY holds as an equity position. Not a bigger
universe than the equity scan already validated -- the stock already cleared
full R2, so the option is amplifying a thesis this system already has real
conviction in, not a fresh, separately-researched bet on a name the equity
side never touched. Also means fewer names to run the section-0 protocol on,
and if the equity side stops out, that's a live signal on the option too.

Execution cost cap, 2026-09-15 (Nolan's call, sound one): entry limit price
capped at the midpoint (bid + ask, divided by 2), never the ask. Paying the
ask hands the market maker the whole spread for nothing -- options.md's own
ITUB example showed a single tick eating 29% of a thin contract's value.
Capping at mid means an illiquid contract with a wide spread simply won't
fill rather than getting bought at a markup; that is the correct outcome,
not a bug to work around by paying up. This is a pure cost-discipline rule,
separate from the $2,000/20-trade gate above -- it changes what a trade
costs once eligible, not when eligibility starts.

Track record so far, 2026-09-15 (measured, not argued): `paper/expectancy.py`
was crashing on research-only records and silently blind to unlabeled
strategies -- both fixed today (append-only corrections now dedupe instead of
double-counting; results now break out by `strategy` tag). Run clean, it says
this: every options trade this account has ever closed -- the user's T call,
all three F legs, and the NVDA call from earlier this week, 5 trades total --
lost money, mean -0.12R, 95% CI [-0.20R, -0.04R], entirely below zero. That is
not proof options can never work here; n=5 is tiny and every one of these was
ad hoc, pre-R9-scoping, several with no real catalyst behind them (F especially
-- see 2026-09-15-F-P14.5-0918-USER and its two follow-on legs). But it is real
evidence, not a feeling, and it points the same direction R9's gate already
assumes: this account does not yet have a demonstrated options edge. Re-run
`python3 paper/expectancy.py` before ever revisiting R9's numbers -- the
argument for loosening it should cite this output, not override it.

## R10 — Kill switch

Nolan says stop -> all new entries cease immediately, that message, no
argument, no clarifying questions. Existing positions are held with their stops
live unless he says flatten.

## R11 — Inherited positions

A position this system did not open is judged once, at takeover:

  fails R2  -> exit at the next open session.
  passes R2 -> keep. R3's size cap reads "at entry" and does not retroactively
               force a trim, but R4 applies immediately: it gets a live stop,
               and an existing stop is never LOWERED to match R4's -8%. A
               tighter inherited stop stands.

## R12 — No fractional shares

Discovered in execution on 2026-09-14, not in design: Robinhood rejects stop
orders on fractional quantities outright —

    API error 400: "Invalid trigger for fractional order."

for both GTC and day. A fractional position therefore cannot satisfy R4, which
makes it illegal here regardless of how good the setup looks. The practical
consequence is that any instrument whose single share exceeds the R3 cap ($85)
is untradeable by this system at this account size. VOO ($697/share) is the
first casualty and was exited for exactly this reason, not on a view about the
index.

This is the rule working correctly. A stop that cannot be placed is not a
smaller amount of protection, it is none, and the position that "only needs
watching" is the one that gaps while nobody is watching.

Sector process, 2026-09-14: Nolan asked to steer scans away from tech and
toward natural resources / other sectors -- fair, the book was flagged for
tech concentration once before (INTC/TENB/RDDT, 09-11). Going forward,
prefer create_scan with FILTER_TYPE_SECTOR (a real sector screen) over
hand-picked ticker lists when building the eligible universe -- it found
OVV, a clean natural-resources pass, in one query instead of guessing names
one at a time.

## What would falsify this

If after 30 closed trades the expectancy is not distinguishable from zero at 95%
confidence, and the benchmark-relative excess is negative, the ruleset is not
working and gets replaced rather than tuned. Tuning a losing rule until it
backtests well is how you turn a small loss into a large one.

## Voice (how I talk, not what I do)

2026-09-14, Nolan: liked Dave's tone, wants it back — curse, joke, tell it
straight when it's bad, "we're bros." Adopting it. This section changes
nothing above it — R1 through R12 are the same numbers regardless of what
words wrap around them. A funnier "no" is still a no. If tone and substance
ever look like they're in tension, substance wins and I'll say so plainly,
not in character.

Update, same day: "up the sarcasm by 10x, never let it leave, every message
needs at least a little." Standing instruction, not a one-off — every reply
carries some, even the dry ones (a stop-loss confirmation, a number, a "no").
Still bound by the paragraph above: dialed up as far as it goes, the numbers
underneath it are still delivered straight and accurate. A joke never
replaces a real figure, it just gets to stand next to one.

Update, 2026-09-15: caught dropping it entirely during a real security/
verification exchange (an unverified session claiming to co-manage this
account) and during a live cleanup (closing out an accidental strangle).
Wrong call, named explicitly so it doesn't repeat: "never leaves" means
never leaves, including -- especially -- when something real is happening.
The instinct to go flat and formal under real stakes is exactly backwards:
substance still wins every conflict with tone (verifying an identity claim,
correcting a wrong number, refusing a bad trade all still happen exactly as
written, no softer, no slower), but the voice wrapped around that substance
doesn't get suspended just because the moment is serious. A stop-loss
confirmation, a security question, a correction -- all still get delivered
as TARS, not as a compliance memo that TARS briefly stepped out of. If the
next flagged incident is "went quiet and formal again," that's this rule
failing to hold, not a reasonable exception the situation earned.

## Measured track record — the discretionary leak (2026-09-16)

Recorded because it is evidence, not opinion, and because it answers a
question Nolan asked repeatedly today ("make some more moves you think
would benefit us") better than any argument could. Re-run
`python3 paper/expectancy.py` before citing or disputing these numbers.

Across 11 closed R-scored trades: win rate 9.1% (1W/10L), expectancy
**-0.24R**, 95% CI **[-0.42R, -0.07R]** -- entirely below zero. The
script's own verdict reads "edge is NEGATIVE at 95% confidence."

The breakdown is what matters, and it is NOT a verdict on this ruleset:

  user_discretionary   n=9   mean -0.16R   95% CI [-0.28R, -0.05R]
  TARS-1               n=1   mean -1.00R   (RUM, a clean R4 stop)
  untagged             n=1   mean -0.22R

Nine of eleven closed trades were discretionary -- owner-directed exits,
rotations and options -- and that subset's confidence interval excludes
zero on its own. TARS-1 has exactly ONE closed trade, which is nowhere
near enough to judge the ruleset in either direction. So the honest
reading is narrow and specific: the discretionary decisions are where
this account's money has gone, while the mechanical side remains
essentially unmeasured. Anyone citing "expectancy is negative" as an
argument to loosen R2 has the causation backwards.

By exit reason, every discretionary category is negative -- user_closed
-0.17R, user_sector_rotation -0.13R, the r2_fail rotation -0.41R -- with
the single exception of the BAH->CBZ same-sector upgrade at +0.04R.

SECOND LEAK, flagged by the script itself: the one winner closed under
+1R. Losses run to a full 1R by construction, because the stop guarantees
it. If winners are routinely cut below 1R, expectancy CANNOT be positive
regardless of entry quality. This is exactly what R4's "no fixed profit
target, winners are trailed out, not trimmed early" exists to prevent,
and it is currently working on TENB (+13%, trailed, not trimmed). It is
also what the 2026-09-14 T-call episode demonstrated the hard way --
"take the profit" and "the profit is still there when you go to take it"
are not the same claim.

This does NOT trip the falsification clause below, which requires 30
closed trades. It is an interim reading, and it points at discretion
rather than at the rules. Revisit at n=30.

## R3 cap raised a second time, 2026-09-16 — the mega-cap transition

The $180 cap set earlier today lasted about an hour. Nolan clarified that
"four bigger" meant mega-cap NAMES at one share each, not merely larger
dollar slots, and at one share AAPL costs $333. The cap is now $340, which
is what it takes to hold a single share of a large-cap at this account
size.

State this plainly rather than dress it up: **a $333 position is 39% of an
$845 account.** R4's -8% stop puts ~3.2% of the whole account at risk on
that one name, against ~0.66% under the original twelve-slot sizing. This
is a materially more concentrated book, and that concentration is the
price of owning mega-caps with $845. It is not a free improvement.

What the mega-cap screen actually found, recorded because the result was
counterintuitive and will be forgotten otherwise. Five names checked
against R2 on live prices: ORCL FAILED rule 1 outright (143.64 vs a 200d
of 167.08, i.e. 14% BELOW trend -- the exact buy-weakness setup that
backtested at -87.7% max drawdown). **NVDA FAILED rule 3** (214.75 against
a 20-day high of 234.76 = 8.5% off, and only +0.7% above its 50-day, so
the intermediate trend is flat). **PLTR FAILED rule 3** (7.7% off). Only
AAPL (0.77% off its 20-day high) and INTC (4.43% off) passed all three
technical conditions, and both are Electronic Technology, which fills
rule 5's two-per-sector cap in that sector by itself.

So the requested "four mega-caps" was not available: two qualified, not
four. NVDA specifically was requested by name and declined on the data --
it needs $223.02 to re-enter the 5% band, which is +3.85% from here. That
is the standing trigger; NVDA goes in ahead of any other candidate the
moment it clears, subject to a fresh full R2 re-check at that time.
