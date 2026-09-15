# TARS-1 — Trading Rules

One-line description: The complete, mechanical ruleset TARS trades. No discretion.
Last Updated: 2026-09-14
Status: ACTIVE — pending single-writer confirmation
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

## R2 — Entry (all four must be true)

  1. Price > 200-day moving average.
  2. Price > 50-day moving average.
  3. Price within 5% of its 20-day high (widened from 3% on 2026-09-14).
  4. No scheduled earnings within the next 3 trading days.

Rule 1 is the load-bearing one. Buying below the 200-day MA — "it's cheap now" —
is the rule that tested WORST in this repo's own backtest: -87.7% max drawdown
on the single-stock basket. It is prohibited, permanently, including when the
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

## R3 — Sizing

Max $85 notional per position at entry (raised from $50 on 2026-09-14, still under 10% of account). Max 12 concurrent positions (raised from 8 on
2026-09-14). Minimum 15% of account value held in cash at the close of any
session (lowered from 40% on 2026-09-14 -- see note below).

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
