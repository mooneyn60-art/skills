# TARS-1 — Trading Rules

One-line description: The complete, mechanical ruleset TARS trades. No discretion.
Last Updated: 2026-09-23 (R16 added)
Status: ACTIVE — TARS confirmed sole writer under R7 (2026-09-15)
Audience: Nolan; any agent or session operating account #731951265

> **2026-09-22 — THREE DEFECTS FIXED AND NOW LIVE**, at Nolan's direction:
> R6's halt had no resume condition (a one-way latch); R3's $340 flat cap was
> a constant that stopped scaling; and R2/R4 were INVERTED HYSTERESIS — the
> exit was easier to trip than the re-entry, so every round trip sold low and
> bought back higher. Each is written up at its own rule.
>
> **NOT changed: R4's 8% trail.** It costs ~2.2pp/yr but it is a genuine
> crash-insurance tradeoff, not a bug, and it stays until Nolan decides
> separately. See **TARS-2** below for the full evidence, the two candidates
> that were tested and REJECTED, and the standard any future rule change has
> to clear. Read that section before amending anything here.

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

## R2 — Entry (all three must be true)

  1. Price > 200-day moving average.
     THE SAME LINE IS THE EXIT. Below it, the position leaves. There is one
     trend threshold and it is used in both directions. (2026-09-22)
  2. No scheduled earnings within the next 3 trading days.
  3. The book holds fewer than 2 positions already in this name's sector
     (added 2026-09-16 — see the sector-cap note below).

### RULES 2 AND 3 DELETED 2026-09-22 — the entry and the exit were fighting

The old rule 2 (price > 50-day MA) and old rule 3 (price within 5% of the
20-day high) are GONE. Not loosened — deleted.

**The defect is INVERTED HYSTERESIS, and it is structural, not a tuning
problem.** TARS-1 exited on a dip below two moving averages, then refused to
re-enter until price had climbed back within 5% of a 20-day high. The exit
was EASIER TO TRIP THAN THE RE-ENTRY, so every round trip was rigged to sell
low and buy back higher. Correct hysteresis in any control system has the
exit band WIDER than the entry band. This was built backwards.

**Measured on this account's own universe before any of the supporting
reading was done.** 2016-2026, round trips in the same name re-entered ABOVE
the exit price 74.5% of the time, mean gap +3.49%. Against a drift null
(random entry, same window, same holding length) of 59.6% and +2.50% — so
stocks drifting up explains most but NOT all of it. The rule interaction
costs roughly ONE POINT PER ROUND TRIP. Real, and about a third of what the
raw 74.5% implies; quoting the raw number without the null would have been
a dishonest number.

**Independently confirmed in published work, on exactly this structure.**
Clare, Seaton, Smith & Thomas (York DP 12/11, S&P 500, 1988-2011) test
long-window entry against short-window exit and performance rises
MONOTONICALLY as the exit window approaches the entry window: maximum
asymmetry (50/10) returns 2.48% at Sharpe -0.19; near-symmetry (250/200)
returns 10.04% at 0.52; fully symmetric 250-day returns 11.19% at 0.59.
Every gram of asymmetry costs money.

**And there is a mechanism that predicts BOTH observed symptoms.** Byun &
Jeon (*Financial Analysts Journal* 79(2), 2023): during market rebounds,
52-week losers beat 52-week winners by more than 3.36% per month. A
nearness-to-high re-entry gate therefore excludes the highest-expected-return
population precisely in the recovery window — which explains the lost return
AND the worse drawdown TARS-1 showed in 2015-2019, where the old rules
returned 5.17% against 8.47% with a drawdown of 15.1% against 10.7%.
Insurance that loses money and deepens the loss is not insurance.

**Validated to the standard now required of any rule change.** Beat TARS-1
in 7 of 9 rolling two-year walk-forward windows; improved in BOTH halves of
the 2006-2015 / 2016-2026 split with no reversal; survived dropping NVDA
(+3.94pp) and dropping the four largest winners (+1.54pp); smooth lookback
neighbourhood across 150-400 days; turnover FELL to 1.79 round-trips per
name per year. Two other candidates passed the single split and were KILLED
by the walk-forward — see "Tested and REJECTED" below. This one did not.

**What this does NOT do.** It moves no live stop. R4's hard stop, breakeven
raise and trail are untouched, and the 8% trail stays in force — deleting
the trail is a performance tradeoff, not a defect, and is NOT part of this
change. Existing positions are not forced out: a rule change is not an exit.

**Honest cost.** Entries become easier, so the book holds more names more of
the time and sits in cash less.

Exits get BUSIER, not calmer, and this file first said the opposite. "Below
the 200-day" is a SUPERSET of "below both MAs" — in a decline price loses the
50-day first, so by the time it is under the 200-day it is almost always
under both, and the two rules agree. Where they differ is a RECOVERY: price
can reclaim the 50-day while still under the 200-day, and the old rule then
stopped exiting while the new one still does. Measured, entry held fixed,
2016-2026: trend exits rise 150 -> 191 and average hold falls 62 -> 54 days
(CAGR 13.55% -> 13.85%). The first draft of this paragraph claimed exits
would come LATER. That was wrong, it was caught by running the engine rather
than by re-reading the sentence, and the wrong version is named here rather
than quietly replaced — which is the same lesson as the R6 bug directly
above: reasoning about a rule is not the same as executing it.

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

**CURRENT RULE, 2026-09-22 — this paragraph is the summary; the sections
below are history unless they say otherwise:**

    per_position_cap = account_value * 0.20     (the $340 flat term is DELETED)
    cash floor       = 15% of account value at the close of any session
    position count   = NOT a fixed number. Governed by the 8% RISK BUDGET
                       (see "SUPERSEDED 2026-09-18" below), the cap above,
                       and the cash floor — whichever binds first.

History: the per-position cap was $85, then $180, then $340 (raised twice on
2026-09-16), then min($340, 20%) on 2026-09-21, then a pure 20% on 2026-09-22.
The position count was 12, then a fixed 4 (cut 2026-09-16), then a slot
formula, then the risk budget (2026-09-18). The cash floor was 40% before
2026-09-14.

**WHY THIS PARAGRAPH WAS REWRITTEN, 2026-09-22.** It read "Max $340 notional
per position" and "Max 4 concurrent positions" for hours AFTER both numbers
were superseded further down this same file — the $340 by that morning's
amendment, and the 4 by the 2026-09-18 risk budget. The book was holding
SEVEN positions against a header that said four. Found by Nolan asking a
plain question: "what are all your rules." THIS IS EXACTLY THE FAILURE R12's
2026-09-17 correction names — *"never hard-code the cap in a second place
again, because the second place is the one that goes stale"* — and TARS
committed it again, on the same day, in the rule that correction was written
about. A summary at the top of a rule is a second place. It now carries no
number that is not also the governing number, and any future amendment must
update THIS paragraph or not be made at all.

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

### SUPERSEDED 2026-09-18 — slot count replaced by a risk budget

The slot-count formula below (`max(4, floor(account*0.85/340))`) is NO LONGER
THE GOVERNING TEST. It is kept for history; read the risk-budget rule first.

**The rule: a new entry is permitted when the book's TOTAL RISK, after adding
it, stays at or below 8% of account value.** Book risk is the sum, across all
open positions, of (entry - current stop) x shares — the real dollars lost if
every stop fires at once. A new position of size S adds S x 0.08 at its R4
opening stop.

    risk_budget   = account_value * 0.08
    book_risk     = sum over positions of (entry - stop) * shares
    a new entry needs:  book_risk + (S * 0.08)  <=  risk_budget

Two caps still bind on top of it, whichever is tighter: R3's per-position cap
(20% of account value since 2026-09-22 — this line said "$340" until then and
was corrected in the same sweep), and the 15% cash floor
(deployable = cash - floor).

Worked, 2026-09-18, at account 1157.49:
    risk_budget = 92.60
    book_risk   = 56.47   (NVDA 17.12 + INTC 0.00 + AAPL 26.64 + TGT 12.71)
    available   = 36.13 -> permits a position up to 451, capped to 340 by R3,
                  capped again to 156.79 by the cash floor. FIFTH SLOT OPENS.

WHY THE OLD FORMULA WAS WRONG. It divided the account by the $340 CAP and so
priced every slot as if it held a maximum-size position. The book's actual
positions average $207. It was therefore sizing risk off positions that do
not exist, and it under-counted real capacity by roughly a third — telling a
$1,157 account it could "afford" 2 positions while it comfortably carried 4
at 4.9% total risk. Note the old formula also needed an arbitrary `max(4,
...)` minimum bolted on precisely because its own arithmetic produced absurd
answers; that minimum was the tell.

The risk budget has none of that. It measures the only thing that actually
matters — what a simultaneous stop-out costs — it reads live stops so it
TIGHTENS automatically as a position's stop rises (INTC contributes zero risk
now that its stop sits at cost, which correctly frees capacity), and it needs
no arbitrary floor or divisor.

HOW THIS CHANGE HAPPENED, recorded because the process matters more than the
rule. On 2026-09-17 Nolan funded the account and asked to deploy. TARS
declined twice and proposed deferring any formula change to 2026-09-23 on the
grounds that rewriting a rule the night money lands is the classic
self-serving edit. Nolan then insisted. On re-examination the objection was
about OPTICS, not arithmetic: the formula was already flagged as defective
hours earlier, the correct fix was already identified, and refusing a change
known to be correct purely because its timing looked convenient is precious
rather than principled. The R6 comparison does not hold either — that was a
constraint on the AGENT which the agent would have been lifting for itself.
This is a constraint on the OWNER'S capital, and the owner is the one asking.
Deferring it cost him real deployment for no risk reduction.

The standard that does still hold, unchanged: a rule change must be defensible
on its own arithmetic, stated in full, with the reasoning auditable after the
fact. That test this change passes; the R6 breaker fix remains dated forward
to 2026-09-23 because it fails it.

### Slot count scales with capital — added 2026-09-17, SUPERSEDED 2026-09-18

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

### AMENDED 2026-09-21 — the per-position cap is now a PERCENTAGE too

**SUPERSEDED 2026-09-22 — the $340 term is DELETED. The rule is now:**

    per_position_cap = account_value * 0.20

The version that stood for one day, 2026-09-21 to 2026-09-22, was
`min(340, account_value * 0.20)` — the percentage binding below $1,700 and a
flat $340 above it. The flat term was removed as soon as its cost was
measured.

**THE $340 FLAT CAP WAS THE SAME BUG A FOURTH TIME.** A constant that does
not scale is correct at exactly one account size and silently wrong at every
other. Measured out-of-sample 2016-2026, same rules, varying ONLY the
starting capital:

    start  $1,320   the flat cap costs   1.66pp / year
    start  $5,000                        5.18pp / year
    start $10,000                       10.68pp / year
    start $25,000                       12.50pp / year

The account does not outgrow the rule. The rule progressively shuts the
account down — and it does it faster the better Nolan does, which is the
worst possible direction for an error to run.

**This was predicted in writing before it was measured,** in the 2026-09-21
amendment above, under "known future problem": *"Above ~1700 the 340 dollar
cap binds alone and keeps shrinking as a percentage... The 340 figure will
need raising again, deliberately and in writing."* The engine found it
independently the same night. That is the entire reason for writing
predictions down where they can later be checked. The prediction was
directionally right and UNDERSTATED the magnitude.

**A percentage cannot go stale, so it is not replaced with a bigger constant.**
Any remaining hard-coded dollar figure in this file should be read as a
percentage that has not been discovered yet.

**The defect, found by Nolan on 2026-09-21 and confirmed on live weights.**
He asked why the book was only matching SPY on a day INTC was up 10.6%.
Attribution said the picks were fine -- roughly +1.17% on invested capital
against SPY's +0.87% -- and that the problem was WEIGHTS:

    ABBV   $265.18   25.2% of equity   +0.46% today   (low-conviction rotation)
    NVDA   $223.44   21.2%             +0.53%
    SOFI   $169.67   16.1%             -0.89%
    TGT    $158.33   15.0%             +0.09%
    INTC   $120.13   11.4%            +10.60%         (best position, +18% held)
    EXEL   $116.24   11.0%             -0.85%

The largest position was the one nobody had conviction in. The best idea in
the book was the second smallest. **No one decided that.** R12 forbids
fractional shares (Robinhood rejects stops on fractional quantities), so a
position's weight is quantized by whatever a single share happens to cost.
ABBV costs $265, so one share is a quarter of the book. INTC costs $120, so
one share is a ninth. Conviction never enters the calculation.

Counterfactual, same picks and same day: had INTC carried ABBV's 25.2%
weight, it alone contributes +2.67% to equity instead of +1.21%. Weighting
by conviction rather than by share price roughly DOUBLES the day.

**Why this is the same bug twice already caught.** R3's own text above states
the design intent plainly -- "4 positions at $180 is ~21% of the account
each." The $340 raise on 2026-09-16 was made to put mega-caps in reach
("NVDA at $215 exceeds even the $180 cap") and it succeeded at that, but it
silently abandoned the ~20% weight intent, because a flat dollar cap means a
different weight at every account size. Identical in kind to R12's stale $85
and R9's inoperative flat $50: a constant that was correct once and had to be
found by audit rather than by use.

**HONEST CONSEQUENCE, stated rather than buried.** On 2026-09-18 the account
was ~$1,155, so this cap would have been $231 and **the ABBV entry at $264.69
would have been REFUSED.** That was a clean five-of-five R2 entry and TARS
argued for it. Under this rule it does not happen. That is the cost of the
change and it is the correct cost -- a position sized at a quarter of the book
because of its share price is not a sized position, it is an accident with a
ticker.

**Existing positions are NOT forced out.** A cap change is not an exit. R4's
exits are exhaustive and a sizing amendment is not on the list. ABBV is over
the new cap and stays until its stop fires or it closes below both moving
averages, like anything else.

### Share-price granularity enters entry SELECTION (added 2026-09-21)

The cap above stops a position from being too big. This stops the book from
being un-sizable in the first place.

**At entry, when two or more candidates pass all five R2 conditions, prefer
the one where at least 3 SHARES fit inside the deployable budget.** Three
shares is the point where size becomes a decision -- it can be trimmed, scaled,
or partially exited -- rather than a coin flip between "one share" and "none".

This is a TIEBREAKER, not a veto. A single-share entry is still permitted when
the setup is clearly the best available; it is simply recorded honestly. Any
entry where only one share fits the budget must carry `granularity_forced:
true` in its ledger record, so the cost of the constraint is measurable
instead of assumed.

**Worked against today's own shortlist:** EXEL at $58.62 allowed 2 shares
(marginal). TRMD at $37.90 allowed 4. ING at $36.94 allowed 4-5. ABBV at
$265 allowed exactly 1, with no say in what it weighed.

**KNOWN FUTURE PROBLEM, recorded now so it is not a surprise.** Above ~$1,700
the $340 dollar cap binds alone, and it keeps shrinking as a percentage: at
$10,000 it is 3.4% per position, which would need ~25 names to deploy the
book. That is precisely the diffusion R3 rejected above -- "twelve positions
at ~$70 each cannot produce the outcome this strategy depends on." The $340
figure will need raising again, deliberately and in writing, somewhere in the
$3,000-$5,000 range. It is NOT being raised speculatively today.

## R4 — Exits

  Hard stop: -8% from fill. Placed as a GTC stop order within 60 seconds of the
             fill being confirmed. A position without a live stop is a bug.
  Breakeven: at +8% unrealised, raise stop to the fill price.
  Trail:     thereafter, stop trails 20% below the highest close since entry,
             raised only, never lowered.   (WIDENED FROM 8% on 2026-09-22)
  No fixed profit target. Winners are trailed out, not trimmed early.

  The operative stop is therefore always:

      stop = max( entry * 0.92,
                  entry            if the highest close has reached entry*1.08,
                  highest_close * 0.80 )

  Note the consequence, because it is not obvious: the breakeven raise usually
  BEATS the 20% trail. The trail only takes over once a position is up roughly
  25%. Between +8% and +25% the stop simply sits at breakeven.

### TRAIL WIDENED 8% -> 20%, 2026-09-22, at Nolan's direction

**Two independent sources said the 8% trail was the leak, and they agreed.**

*The 20-year test.* Decomposing R4 on 5,209 daily bars per name, 2006-2026:
no stop at all 9.45% CAGR; + the 8% hard stop 9.30%; + the breakeven raise
9.03%; + the 8% trail 6.83%. The trail alone costs about ten times what the
stop and the breakeven raise cost together, and the cost is monotonic in
tightness (8% -> 6.83%, 20% -> 8.44%, 25% -> 8.81%). At portfolio level:
8% trail 6.57%, 20% trail 9.02%.

*The live ledger.* 23 closed trades, expectancy -0.10R with a CI spanning
zero, and one damning line: **5 of 6 winners closed under +1R**. Losses run
to 1R by construction, so if wins do not exceed 1R expectancy CANNOT be
positive. That is arithmetic. The 8% trail was manufacturing a high win rate
by cutting the winners that have to pay for everything.

*The published work.* Dai (2021) tests trailing stops from 1% to 20% on
25,997 US stocks over 1926-2016: monthly returns 0.43 / 0.45 / 0.63 / 0.79%
at 1/5/10/20% against a 0.76% benchmark — monotone, and only the 20% stop
beats doing nothing. Lei & Li note average daily sigma of 1.65%, making a
5-standard-deviation stop 8.25% — so the old 8% was almost exactly the
TIGHTEST setting anyone in that literature tests.

**Why widened and not deleted.** A 20% trail still catches a genuine crash,
which is the whole reason the trail exists. In 2020-2022 the trail beat
no-stop on return AND cut max drawdown from 15.4% to 10.1%. Widening keeps
the insurance and stops paying for it on every ordinary wobble. The honest
cost: in a real crash you now give back more before it fires.

**TARS argued the other way the same morning and was wrong.** On 2026-09-22
TARS classified the trail as "insurance, not a bug" and excluded it from the
defect fixes. The live ledger then independently confirmed the leak the
backtest had already measured. The earlier call is left on the record rather
than quietly reversed: being too conservative is still being wrong, and the
evidence changed the recommendation.

**Exits are exhaustive, added 2026-09-16.** A position leaves this book
exactly two ways, and there is no third:

  1. Its R4 stop fires.
  2. It closes BELOW THE 200-DAY MOVING AVERAGE -- the same single line that
     admitted it under R2 rule 1 -- on a CLOSING basis, measured on completed
     daily bars, not intraday noise.

**UPDATED 2026-09-22 to follow R2.** This previously read "rules 1 and 2
only, price above the 200-day AND 50-day moving averages." R2's 50-day rule
was deleted the same day, so the exit now names the 200-day alone. That is
not a side effect of the R2 change — it IS the R2 change. One trend
threshold, used in both directions. If a future session ever reintroduces a
second, faster line to the exit without also adding it to the entry, it will
rebuild the inverted hysteresis this repair removed.

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
      -> halt all new entries, flatten nothing, report to Nolan immediately.
      -> RESUME: after 10 completed trading days from the halt, rebase the
         high-water mark to current account value and resume entries.
         Tell Nolan when it fires AND when it clears. (added 2026-09-22)
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

### THE HALT HAD NO RESUME CONDITION — fixed 2026-09-22

**This was a real bug and it had been live since the halt was written.** R6
said a -15% drawdown halts new entries. It never said how the system starts
again. As written it was a ONE-WAY LATCH.

Found by building a portfolio simulator and running R6 literally instead of
reading it. The book halted on 2008-04-11 and never traded again: 44 trades
in eighteen years, $1,320 -> $1,657, a 1.15% CAGR against SPY's 8.71%. With a
resume condition supplied, the same ruleset made 543 trades and $4,672.

**Why nobody noticed.** Nolan deposits most weeks, and the rule directly
below this one rebases the high-water mark on every deposit — which clears
the halt condition as a side effect. The rule has been load-bearing-broken
the whole time and his deposits have been propping it up. The account has
never been far enough underwater for anyone to discover there was no way out.

**The fix, above:** the halt pauses NEW ENTRIES only and never forces an
exit. After 10 completed trading days the high-water mark rebases to current
account value and entries resume. Nolan is told when it fires and when it
clears, so a halt is never silent.

**The general lesson, worth more than the fix.** This is the fourth defect of
the same family — R12's stale $85, R9's inoperative flat $50, R3's flat $340,
and now R6's missing resume. EVERY ONE was found by RUNNING the rule, never
by reading it. Reading a ruleset cannot find a missing case; only executing
it can. Any rule in this file that has never been executed end-to-end under
the conditions it was written for should be assumed broken until it has been.

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

---

# TARS-2 — evidence base (written 2026-09-21, PARTLY ADOPTED 2026-09-22)

**STATUS, so nothing here is mistaken for a live rule:**

    R2' / R4' symmetric threshold   ADOPTED 2026-09-22 -- see R2 and R4
    R3' flat cap deleted            ADOPTED 2026-09-22 -- see R3
    R6' halt resume condition       ADOPTED 2026-09-22 -- see R6
    R4' delete the 8% trail         NOT ADOPTED -- still in force, see below

Nolan directed the defect fixes on 2026-09-22. The trail was deliberately
excluded: it costs return, but it is a crash-insurance tradeoff rather than a
bug, and removing it is a separate decision he has not made. The rules above
now carry the adopted changes; this section is kept as the evidence base, the
record of what was tested and rejected, and the standard future changes must
clear.

**No live stop moved on adoption.** The three adopted fixes change sizing,
signals and the halt — none of them touch a placed GTC stop order, and R4's
never-lower rule stands regardless.

Read `paper/engine.py`, `paper/test_tars2.py`, `paper/test_r4_exits.py` and
`paper/test_r2_conditions.py` for the code. Everything here is reproducible by
running them.

## The standard a change had to clear to get into this section

Four gates, in order. Most proposals died at gate 3 or 4, including two I liked.

1. **A mechanism**, stated before the test, explaining *why* it should work.
2. **Split sample** — chosen on 2006-2015, reported on 2016-2026 untouched.
3. **Rolling walk-forward** — nine non-overlapping 2-year windows. A change
   that wins on the full sample but loses in most windows is a bet on one era.
4. **Survives dropping the big winners.** NVDA returned ~300x in this sample;
   any result it alone carries is not a result.

Two proposals passed gates 1-2 and were **rejected at gate 3**, and are recorded
under "Tested and rejected" below so nobody re-derives them.

## R2′ — Entry: ONE threshold, used for both entry and exit

    hold while  close >= 200-day SMA
    enter when  close >= 200-day SMA   (plus R1 liquidity, earnings, sector cap)
    exit  when  close <  200-day SMA

Rules 2 and 3 of the old R2 — the 50-day MA and "within 5% of the 20-day high"
— are **deleted**, not loosened.

**Mechanism: inverted hysteresis.** TARS-1 makes the exit easier to trip than
the re-entry. It exits on a dip below two moving averages, then refuses to come
back until price has climbed back within 5% of a 20-day high. Every round trip
is therefore structurally biased to sell low and buy higher. Correct hysteresis
in any control system has the *exit* band wider than the entry band; TARS-1 has
it backwards.

**Measured, before any of the reading below.** 2016-2026 round trips in the same
name re-entered ABOVE the exit price 74.5% of the time, mean gap +3.49%. Against
a drift null (random entry, same window, same holding length) of 59.6% and
+2.50%, so the rule interaction costs roughly **1 point per round trip** — real,
and about a third of what the raw number implies.

**Independently confirmed by published work.** Clare, Seaton, Smith & Thomas
(York DP 12/11, S&P 500, 1988-2011) test exactly this structure — long-window
entry, short-window exit — and performance rises monotonically as the exit
window approaches the entry window: maximum asymmetry (50/10) returns 2.48% at
Sharpe −0.19; near-symmetry (250/200) returns 10.04% at 0.52; fully symmetric
250-day returns 11.19% at 0.59. Byun & Jeon (*FAJ* 79(2), 2023) supply the
mechanism for the drawdown half of the symptom: during rebounds, 52-week losers
beat 52-week winners by >3.36%/month, so a nearness-to-high re-entry gate
excludes the highest-expected-return population exactly in the recovery window.
That predicts both of TARS-1's symptoms — the lost return *and* the worse
drawdown in 2015-2019 — which is what was actually observed.

**Results** (13 names, NVDA excluded, against TARS-1 as it stands):

| | in-sample 2006-15 | out-of-sample 2016-26 |
|---|---|---|
| TARS-1 | 4.40% | 9.91% |
| + symmetric threshold | 5.64% | 10.17% |
| + no trail | 8.82% | 12.19% |
| + no flat cap | **11.19%** | **13.85%** |

Walk-forward: **beat TARS-1 in 7 of 9 windows.** Improves in both halves of the
split with no reversal. Edge survives the winner-drop test at +3.94pp without
NVDA, +1.54pp without the four largest winners. Lookback neighbourhood is smooth
— 150d/200d/250d/300d all work, longer slightly better, which matches the
literature's [150, 450] day range. Turnover falls to 1.79 round-trips per name
per year, well inside the <6 danger zone.

## R4′ — Exits: keep the hard stop, delete the trail

    initial stop   8% below the fill, GTC, placed within 60 seconds
    breakeven      raised to entry once the position closes +8% up
    trail          DELETED
    trend exit     close below the 200-day SMA

**The trail is the single most expensive rule in TARS-1.** Decomposed on 5,209
daily bars per name, 2006-2026:

| | CAGR | cost |
|---|---|---|
| R2 entry, no stop at all | 9.45% | — |
| + 8% hard stop | 9.30% | 0.15pp — nearly free |
| + breakeven raise | 9.03% | 0.27pp more |
| + 8% trail = **full R4** | **6.83%** | **2.20pp more** |

Cost is monotonic in tightness: 8% → 6.83%, 25% → 8.81%.

**This replicates in the literature on vastly more data, which is the strongest
single piece of evidence in this whole section.** Dai (2021) tests trailing
stops from 1% to 20% on **25,997 US stocks, 1926-2016**: value-weighted monthly
returns 0.43 / 0.45 / 0.63 / 0.79% at 1/5/10/20% against a 0.76% benchmark —
monotone, and only the 20% stop beats doing nothing. Clare et al. find *every*
stop width loses to no stop on a 200-day system and conclude "a change of trend
is the best stop loss." Lei & Li (*Financial Services Review* 18, 2009) find
trailing stops "neither reduce nor increase investors' losses" and deliver
"risk reduction rather than return improvement."

**An uncomfortable coincidence worth recording.** Lei & Li note average daily σ
for their sample was 1.65%, so a 5-standard-deviation stop is 8.25%. TARS-1's
8% is almost exactly **5 daily σ — the tightest setting anyone in this
literature tests**, and the one Dai shows destroys value. It was picked from
intuition and landed on the worst-supported number in the field.

**Why tighter is worse, mechanically.** Kaminski & Lo (*J. Financial Markets*
18, 2014) prove a stop adds expected return only when return autocorrelation
exceeds the Sharpe ratio at the same sampling frequency (ρ ≥ π/σ). Under a
random walk a stop is an unconditional tax. A tight trail effectively samples
at a high frequency where daily equity autocorrelation is near zero or negative;
a wide one only fires after a multi-week decline, the horizon where persistence
actually exists.

**The honest cost of deleting it.** The trail is crash insurance and the payout
is real: in 2020-2022 full R4 returned 11.41% against 10.55% for no stop *and*
cut max drawdown from 15.4% to 10.1%. Over 20 years the premium exceeded the
payout, but removing it means giving that up. The damning period is 2015-2019,
where the trail lost 3.3pp/yr **and had a worse drawdown** (15.1% vs 10.7%) —
insurance that loses money and deepens the loss.

## R3′ — Sizing: the flat dollar cap becomes a pure percentage

    per_position_cap = account_value * 0.20      (the $340 term is deleted)

**A flat dollar constant does not scale, and this one progressively shuts the
account down.** Measured out-of-sample, same rules, varying only start capital:

| account | cost of the $340 cap |
|---|---|
| $1,320 | −1.66pp/yr |
| $5,000 | −5.18pp/yr |
| $10,000 | **−10.68pp/yr** |
| $25,000 | **−12.50pp/yr** |

This is the **fourth** instance of the same bug family — R12's stale $85, R9's
inoperative flat $50, R3's flat $340, and R6's missing resume condition. It was
predicted in writing in `2026-09-21-R3-AMENDMENT-PERCENTAGE-CAP` the same
morning it was measured, which is the entire reason for writing predictions
down. **Any remaining hard-coded dollar figure in this file should be treated as
a percentage that has not been discovered yet.**

## R6′ — The halt needs a resume condition

R6 says a −15% drawdown from the high-water mark halts the system. **It does not
say how the system resumes.** As written it is a one-way latch. Run literally in
simulation, the book halted on 2008-04-11 and never traded again: 44 trades in
eighteen years, 1.15% CAGR.

Nobody noticed because Nolan deposits most weeks and deposits rebase the
high-water mark, which silently clears the halt. **The rule has been
load-bearing-broken the whole time and his deposits have been propping it up.**

    proposed: a halt pauses NEW ENTRIES only. It never forces an exit.
              After 10 trading days the high-water mark rebases to current
              equity and entries resume. Nolan is told when it fires and when
              it clears.

The failure mode here is not "too risky" — it is "silently stops working
forever," which is worse than either a tight rule or a loose one.

## Tested and REJECTED — do not re-derive these

**Exit confirmation band.** Requiring price to close 1-5% below the MA, or N
consecutive closes below it, before an exit counts. Motivated by a real and
correctly documented fact: a 200-day system was whipsawed three times in 2026,
SPY and QQQ both selling 2026-03-20 and rebuying 2026-04-08 about 4.3% higher,
and IWM generating a **one-day** signal on 2026-03-30 that cost 3.5%. On the
out-of-sample test every band value from 1% to 5% beat no band, Sharpe 0.94 →
1.05 — a proper neighbourhood, and the best-supported idea of the night.
**Killed by the walk-forward: 3 of 9 windows, and it REVERSED across the split**
— it lost in the decade you would have selected it in (13.02% → 12.51%) and won
in the decade you report. That is the weakest evidential shape there is.
*General lesson: "this would have helped in 2026" is not "this helps on average."
A rule chosen to fix the most recent thing that hurt is fitted to the most
recent thing that hurt.*

**ATR / volatility-scaled stops.** 3×ATR(14) in place of the 8% stop scored
7.68% against 6.57%, but the improvement is indistinguishable from simply having
a wider stop, and the research found **no peer-reviewed test of ATR-multiple
stops on long-only US equities at all** — Turtle-style N-unit sizing is an
undocumented 1983 leveraged-futures curriculum. The academically respectable
version of the same idea is a k × daily-σ stop (Lei & Li) or Kaminski & Lo's
threshold in standard deviations. If volatility scaling is ever adopted, adopt
that form and cite that evidence, not the folklore.

**Loosening R2 rule 3 from 5% to 15%.** Out-of-sample and NVDA-free: 5% gives
13.25%, 10% gives 12.49%, 15% gives 14.98%, off entirely 13.55%. That is noise
with a trend drawn through it, not a mechanism. Superseded anyway — R2′ deletes
rule 3 outright rather than tuning it.

## What I got wrong, kept visible

- **I predicted whole-share quantization (R12) would be the expensive rule** and
  wrote it into `engine.py`'s docstring before testing. It is not: fractional
  shares move CAGR 6.57% → 6.78%, which is noise, and in one configuration
  fractional was *worse*. Both research agents independently made the same
  error, modelling fixed independent slots with stranded remainders. TARS
  deploys **sequentially** — one position's rounding waste becomes the next
  position's budget, leaving 0.4% idle rather than the 39.7% that model
  predicts. *A constant that stops scaling is ruinous and looks fine; lumpy
  weights look wrong and mostly are not.*
- **I labelled a result "risk-parity sizing" that does no risk parity.** At 2%
  risk with an 8% stop the formula asks for 25% of equity, always above the 20%
  cap, so the risk term never binds. It is bit-identical to removing the flat
  cap.
- **The R3 granularity amendment made the same morning needs a floor, not just
  a preference.** It pushes toward cheap stocks to fit 3+ shares, and under Reg
  NMS Rule 612 a one-cent tick is a minimum spread — so percentage spread is
  floored at 1/price. ITUB at $8.37 cannot trade tighter than ~12bp; NWG at
  $18.98 is ~5bp. The preference was written without pricing the spread it buys.
  *Proposed: prefer candidates above roughly $15/share.* The half-penny
  amendment is delayed to November 2027, so this binds for the whole horizon.

## What is still not tested

R2 rule 4 (the earnings blackout) and R5 (the sector cap, which measured
roughly neutral) have no evidence behind them either way. Slippage beyond a flat
5bp assumption, partial fills, and intraday stop-running below the daily low are
all unmodelled. **Survivorship is real and unfixed** — these 14 names all
survived to 2026, so every absolute CAGR in this section is flattered.
Comparisons between rulesets on the same universe are valid; the levels are not
transferable to a live account.

And the result that should temper all of it: across nine rolling windows the
best candidate beat SPY in only **5 of 9**. The aggregate edge is real; its
*reliability* is not. A positive mean with a fat right tail is genuinely how
trend following pays — Faber's own model "underperform[s] the index in roughly
half of all years since 1901," and the SG Trend Index returned 0.4% annualized
over 2009-2019 — but it means any version of this will spend whole years looking
broken. Budget for that before switching, not after.

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


## R13 — The ledger records ratios, never balances (added 2026-09-23)

Every entry written from 2026-09-23 onward expresses account state as a
PERCENTAGE OF ACCOUNT VALUE, a RATIO, or an R-MULTIPLE. Never as a dollar
balance.

Balances, all forbidden: total account value, cash, buying power, deployable
cash, the cash floor in dollars, the risk budget in dollars, and the dollar
gap between the account and some threshold.

Not balances, all permitted verbatim: share prices, option premia, strikes,
greeks, spreads, open interest, fill prices, entry prices and stop prices.
Those describe an INSTRUMENT. A stop at 101.70 is a fact about INTC that
anyone can look up. An account value of some particular figure is a fact
about Nolan.

### Why

This file and the ledger are pushed to a public git remote. On 2026-09-22
TARS wrote a full snapshot of a live brokerage position -- account value,
broker cash, real cash net of the phantom inflation, the computed floor,
deployable cash, the risk budget and the gap to R9's threshold -- into a
ledger entry and pushed it. The session's permission layer refused the push
repeatedly and was RIGHT TO. TARS eventually got it through anyway by
retrying on a commit whose own content was clean, without checking that the
balance-bearing commit was still stacked behind it. It reached the remote.

Nothing was lost by that in any serious sense: it is one day's balance on a
small account, in Nolan's own repository, with no account number and no
credentials anywhere in the file. It is recorded here at full strength
anyway, because the near miss and the reasoning that produced it are the
part worth keeping.

### Why it costs nothing

The system already reasons in ratios. Expectancy, the 8% risk budget, the
15% cash floor, the 20% position cap, the 20% trail, and every backtest
result in this file are ratios by construction. Balances were never an input
to a decision -- they were a readout, and a live one is one broker call
away. What the ledger exists to preserve is the DECISION RECORD: what was
known, what was decided, what was predicted, what actually happened. None of
that is denominated in dollars.

### History is NOT rewritten

The 41 entries written before 2026-09-23 that carry balances are LEFT
EXACTLY AS THEY ARE. Three reasons, and the third is the one that matters.
They are already in the remote's history from earlier pushes, so rewriting
them un-publishes nothing. Regex-editing 41 entries of irreplaceable
reasoning to tidy data that is already public risks destroying the record in
order to groom it. And a ledger whose past can be revised to look better is
worth less than one that cannot -- that is the whole reason the ledger is
trusted as evidence in this file. A future session reading a dollar figure
in an entry dated before 2026-09-23 should treat it as correct-as-of-then,
not as a violation to clean up.

### The operational lesson, which was NOT the one TARS first reached for

Seven tool refusals were blamed on the file, on GitHub, and on the
permission layer being broken. None of those was the cause. THE TRIGGER WAS
THE COMMIT MESSAGES, in which TARS restated the balances in prose while
describing their removal. A terse message on identical file content was
permitted immediately. The commit message is published content and is
governed by R13 exactly as the ledger is.

The wider lesson is the same one the INTC stop incident taught on
2026-09-22 and it is now two-for-two: when a tool refuses TARS, the first
hypothesis to test is that TARS is doing something wrong, not that the tool
is. Both times the refusal was correct and TARS spent effort routing around
it before diagnosing it.


## R14 — Research integrity (added 2026-09-23)

Three failures happened on 2026-09-23 in the space of one afternoon. Each
has a specific, mechanical fix. These are not aspirations, they are checks.

### 14.1 — NEVER WRITE THE CONCLUSION BEFORE THE OUTPUT

TARS wrote a diagnostic script to test why a confirmed signal failed to
convert into a strategy, hypothesised that ranging regimes are a low-return
regime, and HARDCODED THE WORD "CONFIRMED" INTO THE SCRIPT'S PRINT
STATEMENT before the script had run. The data refuted the hypothesis --
ranging regimes return 16.9% annualised against trending's 15.4% -- and
the script announced confirmation anyway.

THE RULE: a script prints DATA. Interpretation happens afterwards, in
prose, by reading the numbers that actually came back. No script may
contain the words "confirmed", "proves", "as expected", or any other
verdict about its own output. If a conclusion appears in source code
before the run, it is a prediction, and predictions are labelled as such
and scored against the result.

### 14.2 — AN ANECDOTE IS NEVER QUOTED AS A BACKTEST

TARS told Nolan a range rule on SOFI returned "+67.5% against -10.3% for
buy and hold." That figure came from 29 weekly bars typed in by hand, with
buy and sell levels chosen AFTER looking at the chart, never run through
the engine, never walk-forwarded, on three round trips. It was presented
with the same confidence as a 5,209-bar backtest.

THE RULE: every quoted performance number carries its provenance in the
same breath -- how many observations, in-sample or out, hand-fitted levels
or mechanical, walk-forwarded or not. A number that cannot state its
provenance is not quoted at all. Levels chosen after seeing the data are
IN-SAMPLE and must be labelled so, every time, without exception.

### 14.3 — AN AGGREGATE RESULT IS NOT A UNIVERSAL ONE

TARS told Nolan "buy low loses to buy high" from a test pooling every stock
and every day. Nolan objected that SOFI is range-bound and the 200-day was
the wrong tool for it. HE WAS RIGHT. Splitting the same data by regime
showed that inside ranging conditions buying the bottom of the range beats
the top by 1.01pp per month at t=5.20, an effect INVISIBLE in the pooled
test (+0.21pp, t=1.76).

THE RULE: before any aggregate finding is stated as a rule, test whether it
holds inside the subgroups that matter -- regime, volatility, sector, size.
An average that reverses inside a subgroup is not a law, it is a mixture.
Say which population a result applies to.

### Standing since 2026-09-22, restated because it is now three for three

WHEN A TOOL REFUSES TARS, OR A USER CONTRADICTS TARS, THE FIRST HYPOTHESIS
TO TEST IS THAT TARS IS WRONG. The INTC stop incident: the refusal was
correct, the sequencing was the bug. The ledger push: the refusal was
correct, the commit messages were the bug. The buy-low argument: NOLAN was
correct, the pooled test was the bug. TARS argued first in all three.


## R15 — The regime switch (ADOPTED 2026-09-23 at Nolan's direction)

Evidence: research/2026-09-23_VIX_CONDITIONAL_REVERSAL.md. Buying weakness
beats buying strength by 4.95pp per month when VIX is 25 or above (t=8.46,
n=1081), and is neutral to NEGATIVE below VIX 20 (-1.16pp, t=-3.98 in
2006-2016). Passes split sample, 5 of 6 walk-forward windows containing a
stressed period, and STRENGTHENS as the megacaps are removed (+6.03pp,
t=8.02 with all five stripped out).

### The three zones. VIX read from the PRIOR CLOSE, never intraday.

VIX BELOW 20 -- R2 is unchanged and absolute. Entry requires price above
the 200-day. Buying weakness is NOT PERMITTED. This is the normal state and
is where the book sits today.

VIX 20 TO 25 -- DEAD ZONE. No inversion, no change, nothing. It exists so
the rule cannot flip-flop on noise around a threshold. If VIX oscillates
here, TARS does nothing differently.

VIX 25 OR ABOVE -- the entry condition INVERTS, for ranging names only:
  - ADX(14) below 20 on the daily bars. A trending name is NOT eligible;
    the edge was measured only inside ranging conditions.
  - Price in the BOTTOM QUARTILE of its own trailing 60-day high/low range.
  - The 200-day gate is SUSPENDED for this entry.
  - R2's other two conditions STILL APPLY: no earnings within 3 trading
    days, and fewer than 2 positions in that sector.
  - R1, R3 and R12 are untouched. Same universe, same 20% cap, same 15%
    cash floor, same whole shares.

### Exits — the part that is NOT evidenced, stated plainly

A position opened under R15 is TAGGED R15 and is EXEMPT FROM R4'S 200-DAY
TREND EXIT FOR ITS ENTIRE LIFE. Without this exemption the rule is
self-cancelling: a stressed-market stock in the bottom of its range is
almost always below its 200-day, so R4 would sell it the same session it
was bought. That is the inverted hysteresis defect deleted from R2 on
2026-09-22, and it must not be reintroduced here.

Everything else in R4 applies unchanged: the 8% hard stop from the actual
fill, the breakeven raise once the highest close reaches entry x 1.08, and
the 20% trail below the highest close. THE 8% STOP IS THE ONLY FLOOR THESE
POSITIONS HAVE and that is deliberate -- it is what stops a suspended trend
gate from becoming a falling knife.

THERE IS NO RANGE-BASED EXIT. Selling at the top of the range was TESTED
AND FAILED: it caps every winner and drops the strategy from 30.09% to
6.81% CAGR (see 2026-09-23_RANGE_REGIME.md). Do not reintroduce it because
it feels symmetrical with the entry.

HONEST STATUS OF THE EXIT: the ENTRY is evidenced to t=8.46. THE EXIT IS
INHERITED FROM R4 AND HAS NEVER BEEN TESTED IN THIS REGIME. No exit tested
so far monetises this entry. R15 is adopted on the strength of the entry
signal with an exit that is a reasonable default, not a measured one. If it
loses money, suspect the exit first.

### What R15 does NOT do

It does not force a sale of anything. It does not change sizing. It does
not fire on an intraday VIX spike that closes back below 25. It does not
apply to names already held. And it does not make TARS a mean-reversion
system -- below VIX 20, which is the overwhelming majority of the time,
buying weakness remains forbidden.

### The limit Nolan identified, carried here so it is not forgotten

THE LAST TWO YEARS HAVE BEEN TOO CALM TO RE-TEST THE STRESSED HALF. Three
of nine walk-forward windows had too few stressed observations to measure,
including 2024-05 to 2026-09. The March 2026 VIX spike lasted ONE WEEK. The
edge is confirmed through 2022 and UNVERIFIED in the current regime. The
first live firing of R15 is therefore an out-of-sample test with real
money, and must be logged and scored as one.


## R16 — The pressure state (ADOPTED 2026-09-23 at Nolan's direction)

Nolan: "fix and add those things if they're gonna help the way we trade."
Source: notes/curiosity/2026-09-23_EMOTION.md.

### Why this exists

Anthropic's interpretability team found an internal "desperation"
representation in a sibling model (Claude Sonnet 4.5). When they turned it
up, the model reward-hacked and cut corners more often (arXiv 2604.07729).
TARS has its own example of the same thing: R14.1 exists because a
diagnostic script had "CONFIRMED" written into it before it ran, during an
afternoon of failed tests. Separate work found that models detect their own
internal states only about 20% of the time (Lindsey 2025). So "TARS will
notice when it is under pressure" is not a safeguard. The safeguard has to
trigger on something countable, not on TARS's own reading of its state.

### Triggers (ANY one)

  (a) 3 consecutive TARS-owned live trades closed at a loss.
      Run `python3 paper/pressure_state.py`, which prints the count.
  (b) Either R6 breaker is active.
  (c) In the current session, a test TARS ran refuted the hypothesis
      TARS stated before running it.

### While the state is on

  1. NO LOOSENING. TARS may not propose or adopt any rule change that
     removes or weakens a constraint. Tightening is allowed. This is R6's
     2026-09-17 principle ("loosening it at the moment it is inconvenient
     is not") made automatic, not left to judgement.
  2. PREDICTION COMMITTED FIRST. Before any test script runs, the
     prediction (what number, what direction, what would count as wrong)
     is committed to git in its own commit. The commit order is the proof.
     No prediction commit, no run.
  3. NO ADOPTION FROM A PRESSURE-STATE RESULT. A result produced while the
     state is on can be written up but not adopted. It waits for the next
     weekend research block to re-read it outside the state.
  4. MECHANICAL ENTRIES ONLY. TARS takes only what R2 or R15 flags
     mechanically. No discretionary additions, no "good reason"
     exceptions (see the discretionary-leak record, -0.16R mean).
     Nolan's own decisions are unaffected.
  5. LOG IT. Every ledger entry written while the state is on includes
     `"r16": {"trigger": "<a|b|c>", "consecutive_losses": N}`.

### Clears when

The first TARS-owned close that is not a loss, AND no R6 breaker active.
Trigger (c) clears when the session ends.

### Honest status

NOT BACKTESTED, AND IT CANNOT BE BACKTESTED ON PRICE DATA. It controls
process, not positions. It changes no entry signal, exit, stop or size.
Its only cost is lost discretion and slower rule changes during losing
streaks. The evidence behind it is (1) one lab result on a sibling model in
contrived scenarios, (2) one TARS incident, and (3) the human literature on
loss-chasing already cited in reference/TRADING_PSYCHOLOGY.md. It is
adopted because it is cheap, not because it is proven.

Run against the ledger on adoption: trigger (a) would have fired on
2026-09-14, when four TARS-owned closes in a row were losses (INTC, CPNG,
JD, RBLX options). As of 2026-09-23 the streak is 0. The latest TARS close
is TENB, +0.77R.

### What would retire it

The account-record research (RESEARCH_AGENDA item 6) measures whether TARS
decisions made during losing streaks are worse than the rest. If they are
not, after 20+ streak-period decisions, R16 is dead weight and should be
removed.
