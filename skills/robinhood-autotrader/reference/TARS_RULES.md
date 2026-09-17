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

### Slot count scales with capital — added 2026-09-17 (Nolan's direction)

Nolan is depositing new funds and chose "more positions, same size" over
bigger positions, explicitly to dilute sector concentration faster. The
per-position cap stays at **$340**. The slot count is no longer the fixed
number 4; it is computed:

    max_positions = max(4, floor((account_value - 0.15 * account_value) / 340))

which reduces to `max(4, floor(account_value * 0.85 / 340))`.

Worked examples so no session has to re-derive it:

    $850   -> floor(722.50/340)  = 2, raised to the minimum -> 4 slots
    $2,000 -> floor(1700/340)    = 5                        -> 5 slots
    $3,000 -> floor(2550/340)    = 7                        -> 7 slots
    $5,000 -> floor(4250/340)    = 12                       -> 12 slots

Two properties that make this safe. First, the formula GATES NEW ENTRIES
ONLY and can never force a sale — the `max(4, ...)` floor means a drawdown
that shrinks the computed number does not put the book over-limit and
trigger liquidation. That would be a mass discretionary exit, which R4
forbids outright. Second, it derives from account value, so it needs no
judgement call and no rule edit when money arrives or leaves.

Why this and not a bigger cap: the book on 2026-09-17 held NVDA, INTC and
AAPL — three of four positions in Electronic Technology, breaking R2 rule
5's cap of two. Raising the per-position cap would have concentrated that
further. More slots at the same size lets rule 5 do its work, because each
new entry must find a sector that is not already doubled up. The
diversification is mechanical rather than aspirational.

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
  2. It fails R2's TREND conditions -- rules 1 and 2 only, price above the
     200-day AND 50-day moving averages -- on a CLOSING basis, measured on
     completed daily bars, not intraday noise.

**CORRECTED 2026-09-17.** As first written on 2026-09-16 this said "the same
five conditions used to enter," and that was a genuine bug, caught the same
evening and repaired the next morning at Nolan's direction. Recorded in full
because the reasoning matters more than the fix.

The arithmetic that breaks it: R2's rule 3 requires price within **5%** of
the 20-day high. R4's trailing stop sits **8%** below the highest close. The
5% test is therefore TIGHTER than the stop, so an R2-fail exit fires FIRST,
every single time, on every ordinary pullback. The trailing stop becomes
unreachable -- decorative. A rule written specifically to stop winners being
cut early instead guaranteed it.

The live case that exposed it: on 2026-09-16 TENB was up 13.7%, the best
position this account has ever held, and sat 5.53% off its 20-day high. Under
the original wording it "failed R2" and was exitable. Selling a +13.7% winner
because it pulled back half a percent past an ENTRY band is not risk
management, it is the disposition effect wearing a rule's clothing.

Why trend conditions only. R2's five conditions do two different jobs. Rules
1 and 2 ask "is this in an uptrend?" -- that question stays live for as long
as the position is held. Rules 3, 4 and 5 ask "is this a good moment to
start?" -- proximity to the 20-day high, the earnings calendar, the sector
cap. Those are TIMING conditions for opening, and they are meaningless as
hold tests. A stock 8% off its high but comfortably above both moving
averages is still in an uptrend; that is precisely the situation the 8%
trailing stop exists to sit underneath.

HONEST CONSEQUENCE, recorded rather than buried: this correction retroactively
invalidates one of the previous day's exits. CNH was sold on 2026-09-16 for
failing rule 3 at 5.6% off its 20-day high (see
2026-09-16-CNH-EXIT-R2-FAIL), and at the time that was called "the strongest
exit justification of any discretionary sale this session." Under the
corrected rule it would NOT have qualified -- CNH was at 13.65 against a 200d
of 10.85 and a 50d of 11.30, comfortably above both, still in trend. That
exit cost -0.41R and should not have happened. It is left in the ledger
unaltered, per this file's append-don't-erase convention; this note is the
correction.

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

  Two positions stopped out AT A LOSS within any rolling 5 trading days
      -> no new entries for the next 3 trading days.
      (loss-only qualifier EFFECTIVE 2026-09-23 -- see below)
  Account value -15% below its high-water mark
      -> halt all new entries, flatten nothing, report and wait for Nolan.
  Any rule in this file cannot be evaluated (data missing, tool erroring)
      -> no trade. A missing input is never treated as a passing test.

### Only LOSING exits trip the breaker — decided 2026-09-17, EFFECTIVE 2026-09-23

As written until today, R6's first breaker counted "two positions stopped
out" without asking whether they made or lost money. On 2026-09-17 that
tripped on RUM (2026-09-15, -1.00R, a genuine loss) **and TENB (2026-09-17,
+0.77R, the first R-positive mechanical trade this account ever produced)**.
TENB exited on its trailing stop — the system working exactly as designed —
and the breaker recorded it as damage. A circuit breaker whose purpose is to
pause trading after losses was pausing it after a win.

The fix: only exits that close at a LOSS count toward the two-in-five-days
trigger. A trailing-stop exit above cost is the system succeeding and must
never contribute to a halt.

**WHY THIS IS DATED FORWARD AND NOT APPLIED TODAY.** The breaker was ACTIVE
on 2026-09-17, blocking entries through the 2026-09-22 session, and this fix
would have lifted it immediately. Nolan authorised the change; the delay is
not about permission. A rule change that removes a constraint from the agent
proposing it, on the day that constraint binds, is unverifiable — the
reasoning and the self-interest are indistinguishable from the outside, and
from the inside. Dating it to 2026-09-23, when the breaker expires on its
own, makes the change cost nothing and buy nothing, which is the only way to
demonstrate it was about the rule.

The current breaker therefore stands unaltered and runs its full course.
From 2026-09-23 the loss-only qualifier is live. Future sessions: this is
the standard to hold any rule change to. Loosening a constraint is fine.
Loosening it at the moment it is inconvenient is not.

### Deposits rebase the high-water mark — added 2026-09-17

R6's second breaker halts new entries when account value sits 15% below its
high-water mark. A DEPOSIT IS NOT A GAIN, and if the high-water mark is not
rebased when money arrives, the breaker silently breaks in the dangerous
direction: new cash inflates account value, the mark never catches up, and
a real 15% loss of capital never trips the halt.

The rule: on any deposit or withdrawal, reset the high-water mark to the
account value immediately AFTER the transfer settles, then resume tracking
from there. Record the rebase in `paper/trades.jsonl` as a non-trade record
with the old mark, the transfer amount and the new mark, so the drawdown
series stays auditable.

Same logic applies to the daily and cumulative P/L reported to Nolan:
external transfers are never performance. A day that ends 300 dollars
higher because 300 dollars was deposited is a flat day, and must be
reported as one.

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

### MANDATORY: broker-vs-ledger reconciliation — added 2026-09-17

Before quoting ANY performance number to Nolan -- expectancy, win rate,
total P/L, R-multiples, trade counts -- the ledger MUST be reconciled
against the broker in the same session. Pull `get_option_orders` and
`get_equity_orders` with `state: "filled"`, match every opening fill to its
closing fill, and confirm each round trip exists in `paper/trades.jsonl`
with a non-null `closed` and `realized_pnl`. Never quote `expectancy.py`
output that has not been reconciled that session.

WHY THIS EXISTS. On 2026-09-17 Nolan asked whether TARS had been lying about
performance. He was right to ask. `trades.jsonl` summed to **-$52.24** of
realized P/L; the broker's own filled-order record summed to about
**-$266**. Six round trips were missing or left permanently open: INTC 115C
(-$135, the largest single loss in this account's history), JD 28C (-$24),
NVTS 17C (-$19), CPNG 16C (-$16), RBLX 50C (-$14), and a second F 13C trip
on 2026-09-17 itself (-$2). **About 80% of all realized losses were absent
from the record.**

Every expectancy figure quoted that day -- "15 closed trades", "+0.00R",
"indistinguishable from random" -- was computed on that ledger, was wrong in
the flattering direction, and was presented as measured fact while arguing
positions in conversation. After reconciliation: 21 closed trades, win rate
19.0%, expectancy **-0.11R**, total **-2.36R**.

ROOT CAUSE, stated so the class of bug is recognisable and not just this
instance: the ledger was only ever written FORWARD, at the moment of a
trade. Nothing ever checked it BACKWARD against the broker. An entry whose
close was never logged did not error -- it silently dropped out of every
statistic. Silent data loss is the most dangerous kind precisely because the
numbers keep rendering and keep looking plausible. Options were hit hardest
because several were opened in one session and closed in another.

The aggravating case, recorded because it should not be softened: on
2026-09-17 Nolan said "we should of held that intel option". TARS pulled
that exact fill from the order book, confirmed the -$135, and wrote a full
post-mortem on it -- while quoting expectancy numbers from a ledger that did
not contain it, in the same conversation. Having the number in hand and not
reconciling is worse than never looking.

## R9 — Options

Locked until: account value > $2,000 AND 20 closed equity trades logged. Then
long calls/puts only, 30-45+ DTE, **max 3% of account value per position**.
Never 0DTE, never naked calls, never uncovered puts.

**SIZE CAP REWRITTEN 2026-09-17** (was a flat $50), at Nolan's direction as he
begins funding the account weekly toward the $2,000 gate. The flat $50 was
INOPERATIVE and had to be found by audit rather than by use, exactly like the
R4 trailing-stop bug found the same morning.

The arithmetic that broke it, measured on 2026-09-17 against live chains:
the cheapest 30-45 DTE contract on any name the book held was the INTC
2026-10-30 $135 call at **$400**; AAPL's 2026-10-30 $350 call was **$640**;
the cheapest contract found anywhere that day, on any name, was **$58**.
Nothing exists under $50. A rule permitting a category with an empty set is
not a conservative rule, it is a dead one.

3% self-gates on arithmetic instead of on a number someone picked:

    $2,000  -> $60 cap   -> still buys nothing real
    $5,000  -> $150 cap  -> a thin contract might fit
    $13,000 -> $390 cap  -> the $400-class contracts above become reachable

STATED PLAINLY SO IT IS NOT A SURPRISE LATER: crossing $2,000 will NOT in
practice make options available. It satisfies the gate; it does not make a
real contract affordable. On today's prices that takes roughly $10,000+. This
is not a new barrier invented by TARS — the $2,000 gate stands exactly as
written — it is the honest consequence of contract prices meeting a
percentage cap. Anyone who wants options sooner should change the PERCENTAGE
deliberately and in writing, knowing that a $400 contract at a $2,000 account
is 20% of everything on one position that can go to zero.

Supporting evidence for keeping the percentage small: `paper/expectancy.py`
scored every options trade this account has closed as losing money, mean
-0.12R with a 95% CI entirely below zero. The single profitable one since
(the F 13 call on 2026-09-17, +$4.00 on a 19-minute hold) does not move that.

ANTI-CHURN, added with this change: the "20 closed equity trades" half of the
gate must NEVER be pursued for its own sake. Trading to reach a trade count
is the definition of churn, and this file's own evidence — Barber & Odean's
11.4%/yr for the most active quintile against 18.5% for the least — says
activity is a cost before any thesis is considered. The 20 trades are meant
to be a byproduct of the equity system running normally. If they arrive
faster than that, something is wrong, and the gate should not open.

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

### Target structure: 3 equities + 1 long-dated option — RECORDED 2026-09-17, NOT ACTIVE

Nolan, 2026-09-17: "I think we should hold 3 big stocks and 1 long option
on a bigger company." Recorded here because the structure is sound and
should not have to be re-derived later. It is NOT authorized by this
section, and nothing below relaxes the gate, the cap, or R6.

Why the structure is sound: a concentrated equity core plus one leveraged,
long-duration, defined-risk position is a real portfolio shape. The core
compounds without a clock; the option supplies convexity that a 3-share
book cannot otherwise get at this account size, and its maximum loss is
the premium, known at entry. It is also the direct lesson of the INTC
2026-10-02 115 call (bought 2.18 on 09-11, stopped at 0.83 on 09-14 through
a 31% gap, marked 3.575 on 09-17 -- a 274.50 swing): a long-dated call does
not want a tight price stop underneath it, because the premium already IS
the stop. See 2026-09-14's exit record.

The equity leg already exists. NVDA, INTC and AAPL, one share each, ~$660.
That half of the structure needs no action.

The option leg is blocked by THREE independent things, two of them
permanent rules and one temporary:

  1. R9's gate. Account > $2,000 AND 20 closed equity trades. Account was
     $852.42 on 2026-09-17.
  2. R9's size cap. Max $50 per option position. This is the binding
     constraint and it is easy to miss: even with the gate open, $50 does
     not buy any long-dated contract on a large company. Honoring "one
     long option on a bigger company" requires raising this cap by a
     factor of roughly 15 to 70.
  3. R6's breaker, tripped 2026-09-17, blocking new entries through the
     2026-09-22 session.

Measured prices, 2026-09-17, so the gap is arithmetic rather than opinion.
Every contract below is on a name the book already holds, as R9's scoping
requires:

  INTC 2027-06-17 $80C   ask 33.90  = $3,390   delta 0.742   OI 3,147
  NVDA 2028-01-21 $300C  ask 20.00  = $2,000   delta 0.367   OI 96,714
  NVDA 2028-01-21 $400C  ask  7.55  =   $755   delta 0.169   OI 51,732

The cheapest long-dated contract available on any held name is $755, four
times the account's $191.33 cash. And it is the worst of the three: delta
0.169, a 7.3% modeled chance of profit, needing NVDA at $407.45 by January
2028 -- an 86% gain -- merely to break even. Affordability and quality run
in opposite directions here, which is the whole problem. The contract worth
owning (delta 0.70-0.80, theta small, thesis given time to work) is the one
that costs multiples of the account.

What would have to be true, stated so it can be checked rather than argued:
account above roughly $3,200 (equity core ~$660 + a real LEAPS ~$2,000+ +
the 15% cash floor), R9's gate met on both conditions, R9's $50 cap
deliberately raised with the options track record re-run first
(`python3 paper/expectancy.py` -- 5 closed options trades, all losses, mean
-0.12R, 95% CI entirely below zero as of 2026-09-15), and R6 clear.

Until then the fourth slot holds cash or a fourth equity, not an option.
Buying the $755 lottery ticket because it is the only thing affordable is
the exact error this section exists to prevent: it would satisfy the
LETTER of "one long option on a bigger company" while inverting its
purpose.

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
consequence is that any instrument whose single share exceeds THE CURRENT R3
CAP is untradeable by this system. VOO ($697/share) was the first casualty and
was exited for exactly this reason, not on a view about the index.

**STALE-NUMBER CORRECTION, 2026-09-17.** This paragraph read "the R3 cap
($85)" from 2026-09-14 until today, and R3's cap was raised twice on
2026-09-16 -- $85 to $180 to $340 -- without this text being updated. Read
literally, the stale version made AAPL ($335), NVDA ($219) and TGT ($159)
untradeable: three of the four positions the book actually holds. Found by
a rules audit on 2026-09-17, in the same class as the R4 trailing-stop bug
found that morning -- a rule that looks operative, isn't, and would have
misfired in an autonomous session with nobody watching.

The fix is to name no number here. R12 defers to whatever R3 says at the
time of reading; R3 is the single source of truth for the cap. Never
hard-code the cap in a second place again, because the second place is the
one that goes stale.

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

## R3 floor restoration — the deficit provision (added 2026-09-16)

The 15% cash floor was BREACHED for the first time on 2026-09-16. Cause,
recorded plainly: a user-placed NVDA market order at 213.915 funded by
selling AVAH, taking cash to $12.60 against a $126.39 requirement -- a
deficit of $113.79. TARS declined that trade three times, partly on this
exact arithmetic (deployable was $85.11 against a $214.75 share price);
Nolan placed it himself, which is his right, and this provision is the
cleanup, not a reproach.

**The rule, at Nolan's direction: while cash sits below the 15% floor,
restoring it takes priority over every new entry.**

Mechanically:

  1. No new entry of any kind while cash < 15% of account value. This was
     already implied by R3 (deployable = cash minus floor, which is
     negative in deficit) but is stated outright here because the breach
     arrived through a route R3 did not contemplate -- an owner trade
     rather than a TARS entry.
  2. When a position exits -- by its R4 stop or an R2 failure -- the
     proceeds go to CASH FIRST until the floor is whole. Only the amount
     above the floor is deployable.
  3. The floor is not relaxed, waived, or "borrowed against" to take a
     setup while in deficit, no matter how clean the setup looks. A rule
     suspended for a good opportunity is not a rule; every breach in
     history had a good opportunity attached to it.
  4. Floor restoration is NOT a reason to sell anything. Positions still
     exit only by R4 stop or R2 failure (see R4's exhaustive-exit
     provision). The deficit is repaired out of exits that were going to
     happen anyway, not by liquidating to raise cash -- otherwise this
     provision becomes a backdoor around the exit rule it sits beside.

Why it matters more than it sounds: with $12.60 of cash this account can
respond to a stop-out but cannot respond to an opportunity. Every future
decision is reactive until the buffer is back. On the current book a
single stop-out repairs most of it -- TENB stopping at 35.04 returns
$175.20, which alone clears the deficit -- so this should self-correct on
the first exit, provided nothing spends the proceeds first. That proviso
is the entire point of writing this down.

## R8 addition — fundamentals captured at entry (added 2026-09-16)

At Nolan's direction, after he asked twice whether TARS researches what a
company actually does before buying it. The honest answer was no: R2 is
five price conditions and contains no business test at all.

**Every entry from now on records the company's fundamentals in its
`paper/trades.jsonl` thesis, pulled from `get_equity_fundamentals`:** what
the business does and how it earns, market cap, P/E (negative stated
outright, never softened), P/B, employee count, the 52-week range and where
price sits inside it, and dividend history INCLUDING any cut or suspension
with its date. Quote the numbers; do not characterise them.

**This is a reporting requirement, not a filter.** No entry is blocked on
fundamentals. R2 remains five price conditions.

The reason is a real measurement, not caution. Running this check across
the book on 2026-09-16 found **INTC at a P/E of -45.82 -- losing money --
with its dividend suspended since 2024-09-01**, and **TENB at a P/E of 659**
on a $4.35B market cap with 1,995 employees. Both would fail any sane
quality screen. Both were among this account's strongest performers: INTC
ran from a 52-week low of $24.45 to $142.35 before settling near $101, and
TENB more than doubled off $15.73. A profitability gate would have excluded
the two biggest movers in the book. That is not a quirk -- Amazon and Tesla
were unprofitable for years while producing exactly the returns a momentum
system exists to capture.

What the requirement buys instead, all three real: you know what you own,
which stops mattering less the moment a single position is 39% of the
account; a fortress and a turnaround can be SIZED differently even when
their entry signals are identical; and the data accumulates so that after
30 closed trades `paper/expectancy.py` can test whether any fundamental
field predicted anything. Until that sample exists, fundamentals are
context. If the test later shows a field carries real signal, THEN it earns
a place in R2 -- measured in, not assumed in, which is how every other rule
in this file arrived.
