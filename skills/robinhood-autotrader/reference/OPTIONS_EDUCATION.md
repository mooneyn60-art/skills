# Options — Complete Reference

How options actually work, every major strategy, and how to pick between them.
Last updated: 2026-09-14 · Status: active · Audience: TARS, and anyone reading
over its shoulder

## Overview and how this file fits with `options.md`

This file is the textbook: mechanics, Greeks, and the full strategy catalog,
written so someone with zero options background can read start to finish and
understand every common way to use them. It does not repeat the account-specific
measurements — `options.md` in this same folder is the lab notebook: what has
actually been tested on THIS account, with real numbers (the ALOY loss, the
wheel simulation, the ruin-probability tables). Read this file for "how does X
work and when do people use it." Read `options.md` for "does X actually work
here, and what did we measure." Where they'd repeat each other, this file links
to `options.md` instead of re-deriving it.

---

## 1. What an option actually is

A **call** is the right (not obligation) to **buy** 100 shares of a stock at a
fixed price (the **strike**) on or before a fixed date (**expiration**). A
**put** is the same right to **sell**. Every option has exactly two sides:

| | Call | Put |
|---|---|---|
| **Long** (you bought it) | Right to buy at strike | Right to sell at strike |
| **Short** (you sold it) | Obligation to sell at strike if assigned | Obligation to buy at strike if assigned |

Buying an option costs a **premium**, paid up front, and that premium is your
entire maximum loss as a buyer — it cannot go negative. Selling an option
collects that premium up front, and your risk runs the other way: a sold call
has theoretically unlimited loss (the stock can rise forever); a sold put's max
loss is the strike (the stock can only fall to zero). This asymmetry is the
single most important fact in options and it explains almost every rule that
follows.

**One contract = 100 shares.** A quote of "$0.58" for a call means one contract
costs $58 (0.58 × 100), and if exercised it buys or sells exactly 100 shares.

### Intrinsic value vs. extrinsic (time) value

A call's price splits into two parts:

- **Intrinsic value** = how far the stock is above the strike (0 if the stock
  is below it). A $26 call with the stock at $27 has $1 of intrinsic value.
- **Extrinsic (time) value** = everything else — the market's payment for the
  chance the option becomes more valuable before expiration.

At expiration, extrinsic value is exactly zero. An option is worth only its
intrinsic value at that instant. Everything an option loses to time between
now and expiration comes out of the extrinsic portion — this is **theta decay**,
covered in §3.

### Moneyness

| Term | Call | Put |
|---|---|---|
| **ITM** (in the money) | stock > strike | stock < strike |
| **ATM** (at the money) | stock ≈ strike | stock ≈ strike |
| **OTM** (out of the money) | stock < strike | stock > strike |

OTM options are pure extrinsic value — cheaper, more leveraged, lower
probability of finishing profitable. ITM options carry real intrinsic value —
more expensive, behave more like the stock itself, higher probability of
finishing profitable. There is no free lunch between these: cheaper always
means lower odds, not a better deal (this account's own pricing comparisons in
`options.md` §0 and the live VZ/T contract comparisons earlier this session
show the same $-per-probability-point tradeoff every time it's checked).

### Exercise, assignment, and expiration mechanics

- **Exercise**: the option holder invokes their right (rare before expiration —
  it throws away remaining extrinsic value; almost everyone sells the contract
  instead of exercising it early).
- **Assignment**: the option *seller* gets forced into the trade because the
  buyer exercised (or because it expired ITM — most brokers auto-exercise any
  option ITM by $0.01 or more at expiration, "pin risk" if the stock closes
  right at the strike).
- **American-style** options (all single stocks) can be exercised any time
  before expiration. **European-style** (most index options — SPX, NDX) can
  only be exercised at expiration. This account trades only American-style
  single-stock and ETF options.
- **Weeklies vs. monthlies**: standard monthly expirations fall on the third
  Friday; many liquid names also have weekly expirations every Friday (and
  some, dailies). Shorter-dated = more theta decay per day, less room for the
  thesis to play out — see the T $26c comparison across Sep-18 vs Oct-16 done
  live on this account: same strike, cheaper AND (for a near-the-money strike)
  slightly better modeled odds short-dated, but roughly double the daily
  theta bleed if the stock stalls.

---

## 2. The Greeks — all five, not just the headline three

`options.md` §6 deliberately limits itself to the three that matter at one
contract. Here is the complete picture, since the ask this time is "all of it."

| Greek | What it measures | Practical read |
|---|---|---|
| **Delta** | $ change in option price per $1 move in the stock; also ≈ probability of finishing ITM | A 0.30 delta call gains ~$30 (per contract) if the stock rises $1, and behaves like owning 30 shares. Ranges 0 to 1.00 for calls, 0 to -1.00 for puts. |
| **Gamma** | Rate of change of delta itself | High gamma = delta shifts fast as the stock moves — near-the-money, near-expiration options have the highest gamma. This is why a near-ATM option close to expiry can swing from "safe" to "worthless" in a single bad session. |
| **Theta** | $ lost per day from time decay alone, all else equal | Always negative for a long option, positive for a short one. Decay accelerates as expiration nears — the last week of an option's life bleeds faster than any prior week. This is the mechanical reason buying premium is a negative-expectancy game on average (§3) and selling it collects a real, measurable edge (§5) — the argument in both sections of `options.md` runs entirely through this one number. |
| **Vega** | $ change in option price per 1-point change in implied volatility | Buying an option before a scheduled catalyst (earnings, FDA decision, Fed meeting) means buying inflated IV; if the event resolves and IV collapses afterward ("IV crush"), the option can lose value even if the stock moved the right direction. Vega is the reason "the direction was right and I still lost money" happens constantly around earnings. |
| **Rho** | $ change in option price per 1% change in interest rates | Matters for long-dated options (LEAPS, 1yr+); irrelevant at the DTE this account trades (30-45 days or less). |

Gamma and rho don't change a one-contract decision at this account's size
(`options.md` §6's judgment call, still correct) — included here for
completeness since the ask was "all of it," not because they should drive a
decision here.

---

## 3. Implied volatility (IV) in more depth

IV is the market's forecast of how much the stock will move, expressed as an
annualized percentage, backed out of the option's price (the option price is
observable; IV is solved for). It is not a prediction of direction — a stock
priced at 60% IV is expected to move a lot, not necessarily up.

- **IV rank / IV percentile**: where current IV sits versus its own trailing
  range (e.g., 52-week high/low). High IV rank = premium is rich *relative to
  this stock's own history* — the textbook signal for preferring to sell
  premium over buy it. Low IV rank = premium is cheap relative to history —
  the textbook signal for preferring to buy.
- **IV crush**: IV predictably collapses right after the uncertainty resolves
  (post-earnings, post-FDA-decision, post-Fed). An option bought the day
  before earnings is paying peak IV for a one-day event; even a correct
  direction call can lose money if the pop is smaller than the priced-in move.
- **Realized vol (RV)** is what the stock *actually* did, in hindsight. The
  IV − RV gap is the actual edge (or lack of one) in selling premium —
  `options.md` §5 measured this per-name rather than assuming an index-level
  volatility risk premium applies to single stocks, and found it usually
  doesn't (NIO's IV/RV ratio of 0.97 meant selling insurance below cost).

---

## 4. The complete strategy catalog

Organized by market view. For each: the setup, max profit, max loss, when
it's used, and the honest tradeoff. **Level flag** shows what this account's
current Level 2 permits — Level 3 strategies cannot be placed here regardless
of how good the thesis is (`options.md` §1).

### Bullish, defined risk

**Long call** — *Level 2.* Buy a call. Max loss = premium paid. Max profit =
unlimited. Cheapest way to make a leveraged bet the stock rises; extrinsic
value bleeds daily (theta) and the whole premium can go to zero. This is
essentially every equity-paired option this account has traded (T, VZ, OVV
comparisons this session).

**Bull call spread (debit spread)** — *Level 3 — unavailable here.* Buy a call
at a lower strike, sell a call at a higher strike, same expiration. Max loss =
net premium paid. Max profit = capped at the strike width minus premium. Costs
less than a naked long call (the short leg's premium subsidizes it) in exchange
for giving up unlimited upside. The standard way to express "bullish, but not
infinitely" once collateral or account size makes an outright long call feel
too binary.

**Bull put spread (credit spread)** — *Level 3 — unavailable here.* Sell a put
at a higher strike, buy a put at a lower strike for protection, same
expiration. You collect premium up front; max loss is defined and capped at
the strike width minus the credit received. This is the standard "collect
income, bullish-to-neutral, defined risk" trade — exactly the structure
`options.md` §1 flags as unavailable at Level 2, which is the single biggest
reason this account cannot run a clean income strategy: the one options trade
whose max loss is small and known cannot be placed.

### Bullish, undefined/large risk (income-generating)

**Covered call** — *Level 2, needs 100 shares.* Own 100 shares, sell a call
against them. Collects premium; caps upside at the strike (if it runs past the
strike, the shares get called away); the stock can still fall the full amount
below the premium collected. Requires `account ÷ 100` in share price just to
enter — on this account that ceiling is well under any name actually held (see
`options.md` §2's collateral-arithmetic argument, which is the reason this
strategy was ruled out here specifically, not in general).

**Cash-secured put (CSP)** — *Level 2, needs 100 × strike in cash.* Sell a put,
hold the full strike price in cash as collateral. If assigned, buy 100 shares
at the strike (offset by the premium already collected); if not, keep the
premium. By put-call parity this is mathematically the same payoff as a
covered call at the same strike — `options.md` §5 measured this equivalence
directly and it holds exactly. "Do the CSP instead, no stock risk" is a common
pitch and it is not actually a different trade.

### Bearish, defined risk

**Long put** — *Level 2.* Mirror of the long call: right to sell at the
strike. Max loss = premium. Max profit = capped (the stock can only fall to
zero) but still large relative to premium paid. Used to bet on a decline, or
as portfolio insurance (see Protective Put below).

**Bear put spread (debit spread)** — *Level 3 — unavailable here.* Mirror of
the bull call spread: buy a put, sell a further-OTM put for a partial rebate.
Cheaper than a naked put, capped profit.

**Bear call spread (credit spread)** — *Level 3 — unavailable here.* Sell a
call, buy a further-OTM call for protection. Collects premium betting the
stock stays below the short strike. The bearish mirror of the bull put spread,
same Level-3 gate applies.

### Hedging / protective

**Protective put** — *Level 2.* Own the stock, buy a put below it as
insurance. Costs premium (an ongoing drag, like an insurance bill) in exchange
for a hard floor on losses. Rarely used on a small, single-position account
because the insurance cost is a large percentage of a small book; more common
institutionally on a concentrated large holding.

**Collar** — *Level 2, needs 100 shares.* Own the stock, buy a protective put,
sell a call to pay for it (often structured for near-zero net cost). Caps both
upside and downside in a band. Used to protect an existing large gain without
selling and triggering taxes, or to survive a known binary event (earnings,
FDA decision) without full exposure either way.

### Volatility plays (betting on movement size, not direction)

**Long straddle** — *Level 2 (two long legs, each fine individually).* Buy a
call and a put at the same strike, same expiration. Profits if the stock moves
far enough in *either* direction to cover the combined premium; loses
everything if it sits still. Expensive — you're paying two premiums, both
decaying. Used going into a genuinely uncertain binary event where direction
is unknown but a big move is expected (this is a pure long-vega bet — see §3
on why buying into elevated pre-event IV is a headwind even here).

**Long strangle** — *Level 2.* Same idea as a straddle but with an OTM call
and an OTM put instead of both at-the-money — cheaper than a straddle, but
needs an even bigger move to profit since both legs start further from the
money.

**Iron condor** — *Level 3 — unavailable here.* Sell a call spread above the
market and a put spread below it simultaneously — collects two premiums,
profits if the stock stays inside a range by expiration. The classic
"defined-risk, sell volatility, direction-agnostic" income trade. Requires
Level 3 for the same reason bull put / bear call spreads do: each side is a
credit spread.

**Iron butterfly** — *Level 3 — unavailable here.* Same idea as an iron
condor but both short strikes sit at the same at-the-money point instead of a
range — higher premium collected, narrower profitable range, more like betting
the stock pins near a specific price.

### Time-based (calendar / diagonal)

**Calendar spread** — *Level 3 — unavailable here.* Sell a near-dated option,
buy a longer-dated option at the same strike. Profits from the near-dated
leg's faster theta decay relative to the far-dated leg. A pure bet on the
*shape* of the volatility term structure, nearly direction-neutral near the
strike.

**Diagonal spread** — *Level 3 — unavailable here.* Same as a calendar but the
two legs use different strikes as well as different expirations — adds a
directional tilt on top of the time-decay bet.

### Stock replacement

**Deep ITM long call (LEAPS or shorter)** — *Level 2.* A call deep enough in
the money (delta 0.80+) behaves almost like owning the shares outright but
ties up far less capital, at the cost of an extrinsic-value premium and a hard
expiration date the stock itself doesn't have. This is exactly the shape of
the T $24c/$25c comparisons priced live on this account earlier — high delta,
high modeled probability of profit, much higher dollar cost than an OTM
lottery-ticket strike, functioning much closer to synthetic stock ownership
than to a speculative bet.

---

## 5. Choosing between them — a practical framework

1. **What's your account's Level?** Rules out roughly half this catalog before
   any thesis matters (`options.md` §1). This account is Level 2: no spreads,
   no condors, no calendars. Only long calls/puts, covered calls, and
   cash-secured puts are structurally possible, and this account's own R9 has
   further narrowed that to plain long calls/puts on names already held as
   equity.
2. **What's your actual view?** Direction (bullish/bearish), magnitude
   (small move vs. big move), and timing (by when) determine the strategy
   family before a specific strike is even considered.
3. **Price the actual contract, not the story** — IV, delta, theta,
   probability of profit, breakeven, exactly as `options.md` §0 step 6
   insists. A great thesis attached to a 15%-probability contract is still a
   bad trade.
4. **Size against the account's real dollar floor**, not a percentage of net
   worth (`options.md` §0 step 7, §4's "the premium is the stop" framing).
   The whole premium is the realistic loss scenario for a long option; size
   accordingly before the thesis is even considered.
5. **Check the calendar independent of the stock's own news** — earnings
   inside the option's life is a binary event the position is directly
   exposed to; a scheduled macro print (Fed, CPI, jobs) can move an unrelated
   position regardless of the single-name thesis (`options.md` §0 steps 4-5).
6. **Log the decision either way.** A well-researched pass is exactly as
   valuable to the record as a taken trade (`options.md` §0 step 8) — this is
   why the declined VZ $52.50c candidate earlier this session got a full
   trades.jsonl entry despite never being placed.

---

## 6. Where this account actually stands today

- **Level 2.** Every Level-3 strategy above (all four spread types, both iron
  structures, calendars, diagonals) is catalog knowledge, not something this
  account can place. If the account ever upgrades, this file's catalog is
  already the reference for what opens up.
- **R9 (TARS_RULES.md):** options originated by this system are locked until
  the account clears $2,000 and 20 closed equity trades, and once open are
  scoped to names already held as equity (2026-09-14 additions to R9).
- **Collateral arithmetic (`options.md` §2)** rules out covered calls and CSPs
  at this size regardless of R9 — `account ÷ 100` gives a share-price ceiling
  under $10, concentrating the whole account into one name to even qualify.
- **The measured verdict on selling premium (`options.md` §5, §5b)** is a
  hard no at this size even if permission and collateral existed — not a
  matter of finding the right name, but of insufficient breadth (n=1 instead
  of the eight-to-ten uncorrelated names the diversification actually
  requires) and a debt hurdle rate the edge doesn't clear.
- **The measured verdict on buying premium (`options.md` §3)** is negative
  expectancy under repetition, not a single bad trade — the Monte Carlo on
  this account's own starting capital showed 94.3% of repeated OTM buys
  ending under $100.

None of this means "options are always bad" — it means this specific account,
at this specific size, on this specific permission level, has a narrow legal
and rational strategy space: long calls or puts, on names it already has real
equity conviction in, sized as if the whole premium is gone, bought with real
odds priced in rather than chased for a cheap ticket. That is the entire
playbook available here, and it is a real, usable one — just not the same
size as the full catalog above.
