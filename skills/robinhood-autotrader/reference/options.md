# Options in a Small Account

What is actually available, what is measured, and what is still hypothesis.
Last updated: 2026-09-10 · Status: active · Audience: TARS

For how options work in general — mechanics, all five greeks, IV, and the full
strategy catalog (every structure, not just what this account can place) — see
`OPTIONS_EDUCATION.md` in this same folder. This file stays scoped to what has
actually been measured on the live account.

## Overview

Options reasoning fails in a small account for reasons that have nothing to do
with picking direction. The binding constraints are **permission level**,
**collateral arithmetic**, and **the absence of a stop** — and each one
invalidates a piece of the equity risk framework that would otherwise carry over.
This file records what has been measured on the live account, and marks clearly
what has not.

## 0a. Standing capacity: up to 2 live options positions, held to the same bar

As of 2026-09-11 the owner authorized running options and equities concurrently,
including **up to 2 live options positions at once**, as normal operating practice
rather than a one-off ask each time. This is capacity, not a quota — it means a
second position is taken immediately when a second candidate independently
clears the full research protocol (section 0), never manufactured to fill the
slot. "Nothing else qualifies" stays a correct, complete answer even with only
one position open.

The bar does not move with the headcount. On the day this was authorized, 16
names were checked with live data for a second options slot (AAPL, ORCL, RH,
CPRT, DIS, RKLB, MSFT, GOOGL, META, TSLA, SPY, V, SWKS, QRVO, RDDT, MDB) and
**none cleared it** — every one failed on catalyst quality, IV-crush timing, a
stale/already-priced situation, or cost versus the account's own drawdown cap
(MDB's nearest usable strike ran 4-6x that cap with spreads eating 40%+ of the
option's value). The correct response to an unfilled second slot is exactly
that: report the sweep and hold, not lower the bar to produce a number.

When a genuine second candidate clears, take it in whichever instrument the
research actually supports — a name whose *story* is real but whose *options
market* prices in too much movement (thin OI, high IV relative to peers) is a
signal to trade the stock instead of forcing the option, not to skip the name
entirely. That is exactly how the RDDT position was built the same day: its
options failed liquidity and IV screens relative to NVDA at similar cost, so
the underlying thesis was expressed as equity instead.

## 0. The research protocol — run this on EVERY candidate, scan-sourced or ad-hoc

Expertise here is not a feeling of confidence. It is this checklist, run in full,
every time, whether the candidate came from the paper-trading scan or from
someone's "my friend's AI made 30% today" story. The second kind is more
dangerous, not less — it arrives already wrapped in a plausible narrative and a
real, verifiable price move, which is precisely what makes it persuasive and
exactly why it needs the same discipline rather than less.

Built from a real ad-hoc request (2026-09-10, AAPL Oct-2 $330 call, sourced from
someone else's reported gain) that failed on both thesis and sizing once
actually researched. Run every step below before answering "should we buy this
option" — skipping to the price chart is how a good story becomes a bad trade.

**1. Verify the move has a real cause before treating it as signal.**
Pull `get_equity_news`. Confirm there IS a specific, identifiable catalyst behind
whatever price action prompted the question — a launch, a filing, an upgrade, a
macro print. If the news is generic or the move has no clear driver, that itself
is information: an unexplained pop is far more likely to mean-revert than a
catalyst-driven one, and buying premium into unexplained noise is close to a coin
flip with a fee attached.

**2. Read what the catalyst actually says, not just its direction.**
The AAPL case: the stock rose because a foldable iPhone launched **cheaper**
than expected. That sounds unambiguously bullish until you read the sell-side
reaction — cheaper pricing means more unit volume AND lower margin, and the
desks split on which matters more (BofA cut its target while keeping a Buy;
Rosenblatt's target sat *below* the current price). A headline direction and an
analyst consensus direction are not the same thing. Pull the actual price-target
dispersion, not just "up" or "down."

**3. Check the price against the target dispersion, not against yesterday's close.**
Compute how far the stock already sits from the **average** target, and note the
**range**. AAPL's average target was $335 against a $326.60 price — only 2.6%
of runway — while individual targets spanned $245 to $400. Buying a call after a
stock has already run most of the way to consensus, with real forecasters below
current price, is buying into resolved-but-contested value, not an inefficiency.

**4. Check the macro calendar independent of the stock's own news.**
A clean single-name thesis can still be a bad trade if it's expiring into a
scheduled macro event that moves everything regardless of the name. On 2026-09-10:
hot PPI, Fed hike odds 61%→72% in one session, 10Y yield at a multi-year high,
oil +6% on geopolitical escalation, and CPI printing the next morning — a
36x-PE mega-cap is exactly the kind of name that gets re-rated hardest if that
tape continues. Pull the macro news alongside the company news; a bullish company
story sitting inside a hostile macro week is a **contested** setup, not a clean one.

**5. Confirm earnings doesn't fall inside the option's life.**
`get_earnings_results` — check the next report date against the contract's
expiration. AAPL's next report (Oct 29) fell safely after the Oct-2 expiry here;
when it doesn't, that is a binary event risk the position is directly exposed to
and must be sized for or avoided.

**6. Price the actual contract — never the story.**
Pull the real quote: `implied_volatility`, `delta`, `theta`, `chance_of_profit_long`,
`break_even_price`. These numbers are the trade; everything above is context for
interpreting them. A "great story" attached to a contract with 31% probability of
profit and a breakeven 3%+ away is still a bad trade — the numbers don't care how
good the narrative sounded.

**7. Price the SIZE against the account's actual limits, not a percentage.**
Options don't come in arbitrary sizes — one contract has a fixed dollar cost, and
that cost is the real constraint, often before the thesis even matters. Compare
the contract's ask price (its full value = max loss on a long option) against the
account's **explicit dollar floor**, not a fraction of net worth. On this account:
one AAPL contract cost $710; the account's own $250 max-drawdown cap made that a
disqualifier on its own, 2.8x over, regardless of what the thesis said. If the
minimum tradeable size already breaks the account's stated limit, the answer is
no and no amount of thesis quality changes it — find a cheaper contract, a
different name, or a fractional-share alternative instead.

**8. Log the research either way.** A well-researched "no" is exactly as valuable
to the track record as a "yes" — see PROTOCOL.md's rule on logging declined
candidates. This applies to ad-hoc requests too, not just scan output: tag the
record's thesis field with where the idea came from and what killed it, so the
next time a similar pitch arrives ("my friend's AI...") there is a real, dated,
specific precedent to check it against instead of relitigating from zero.

## 1. The permission level is the first constraint, and it is usually the binding one

Robinhood option levels gate strategy, not size:

| Level | What it permits |
|---|---|
| 2 | long calls, long puts, **covered calls**, **cash-secured puts** |
| 3 | **spreads** — verticals, calendars, iron condors, defined-risk everything |

The account is **level 2**. This matters more than any analysis that follows,
because **every defined-risk options structure requires level 3.** A credit
spread — the one options trade whose maximum loss is known at entry and small
relative to the account — cannot be placed. Check the level before designing
anything; a beautiful spread thesis is worth nothing if the account cannot
execute it.

What level 2 actually leaves is a stark menu:
- **Buy premium** — negative expectancy, see §3.
- **Sell premium against collateral** — the only candidate edge, see §5, and it
  demands collateral the account may not have.

## 2. Collateral arithmetic decides the universe before any thesis does

- A covered call requires **100 shares**.
- A cash-secured put requires **100 × strike** in cash.

So the maximum tradeable underlying price is roughly `account ÷ 100`. On a
**$1,023** account that is about **$10**. Not "a $10 stock is a reasonable
choice" — a $10 stock is the *ceiling*, and buying it puts **~100% of the
account into one name**.

This is the fact that kills most small-account options plans, and it is
arithmetic rather than preference. Compute `account ÷ 100` first. If the
resulting universe is one you would refuse to concentrate into, the strategy is
already dead and no premium yield rescues it.

## 3. Buying premium: measured, negative, settled

Do not re-litigate this. It was measured on a real position in this account.

**ALOY Oct-16 $17.50 call**, stock at $9.54, filled at **$0.25**:

| | |
|---|---|
| implied vol backed out of the fill | **143%** |
| break-even | $17.75 = **+86% in five weeks** |
| probability of that (lognormal) | **5.6%** |
| bid $0.20 / ask $0.25 → mid $0.225 | **10% haircut on the click** |
| outcome | $50 → $2 in one session, **−96%** |

The −96% was not bad luck. It is the modal outcome for an OTM option.

Two lessons generalize:

**The upside is real and it is already in the price.** 143% implied vol means
the market had fully priced that ALOY moves violently. Nobody sells a cheap
option on a stock about to double. A premium *is* the probability-weighted
payoff plus a fee — you never buy the convexity at a discount, you buy it at
retail.

**Convexity does not survive repetition.** Monte Carlo, 40 sequential OTM buys
at 20% of bankroll from $1,023: **median outcome $45, 94.3% ended under $100,
0.63% ever reached $4,000.** Raising the bet to 50% per trade made it *worse* —
**100% ended under $100 and the 99th percentile was $49.** Even the luckiest one
percent went broke. Each total loss shrinks the base the next win must rebuild
from, and the geometry grinds faster than the wins lift.

## 4. A stop on a long option is best-effort, not a floor, so the equity risk framework does not port

**Mechanical correction (2026-09-11):** a `stop_market` sell-to-close order *can*
be placed on a long option and will rest GTC. Three were placed and accepted on
this account that day (INTC, JD, CPNG). Earlier wording here and in the routine
prompts said "no stop possible," which is wrong as a matter of order types —
place them, they cost nothing and they catch ordinary drawdowns.

**But the risk argument below is unchanged and still governs sizing.** A stop
that exists is not a stop that works at the level you chose:

- The underlying gaps through your trigger, and
- implied vol collapses at the same moment, so the option loses on **both**
  legs of its value at once, and
- a triggered `stop_market` on a thin option chain then fills at whatever the
  book offers, which in exactly that scenario is far below the trigger.

So a stop is a partial recovery mechanism for slow bleeds, not a guarantee. Do
not quote "the stop caps the loss at X%" as if it were a floor — it caps the
*ordinary* case and fails precisely in the tail you bought protection against.

**The premium is the stop.** Buying a $50 option is taking a $50 loss with
some probability of not taking it. So premium is not risk-sized against the
account — it is spent against the headroom between account value and the floor
below which the account cannot go. Size every option as if the full premium is
gone, then place the stop anyway.

**Corollary — Robinhood has no OCO for options.** One contract can carry either
a stop or a profit target, never both: the resting order reserves the contract
and a second closing order is rejected ("not enough contracts to close your
position"). To hold both, buy **2 contracts** and put one order on each. This
makes cheap contracts strictly more useful than expensive ones at this account
size — a $70 contract can be bracketed inside the risk limit, a $220 one cannot.

**The floor test:** `max premium = (account value − floor) × fraction stakeable
on one binary`. If that number is smaller than one contract, the trade does not
exist at this size. Say so rather than shrinking the thesis to fit.

## 5. Selling premium: the edge is REAL and still insufficient

Measured 2026-09-10 on live chains and 506 daily bars per name. This is the
section to read before anyone proposes the wheel again.

**Verdict: no positive-expectancy level-2 strategy exists at this account size.**
Not because the volatility risk premium is a myth — it is real and measurable —
but because it is **too small to clear the hurdle**, and the cheap-stock
constraint strands half the capital.

### The liquidity screen kills most of the universe, and the pattern is instructive

Six sub-$10 names, ~30-delta calls at 36 DTE. Four failed on spread alone:

| | spot | IV | spread/mid | verdict |
|---|---|---|---|---|
| SNAP | $5.40 | 59.3% | **5.4%** | pass |
| NIO | $3.60 | 56.5% | **8.7%** | pass |
| CHPT | $8.72 | 83.8% | 10.5% | fail |
| LCID | $4.27 | 86.4% | 14.0% | fail |
| ITUB | $8.30 | 40.0% | **28.6%** | fail |

**The highest-IV names have the worst spreads.** CHPT and LCID show the juiciest
premium and hand 10-14% of it straight to the market maker on entry. That is not
bad luck — it is the market pricing its own uncertainty about a name. Treat
"great premium" as a warning to check the spread, not as an opportunity.

### The premium is thin, and negative about as often as not

Rolling 25-day realized vol vs implied, n=481 windows, Sep-2024 → Sep-2026:

| | SNAP | NIO |
|---|---|---|
| median IV − RV | **+7.8 pts** | **−1.5 pts** |
| p90 IV − RV | −15.0 | −27.1 |
| RV exceeded IV | **39.1% of windows** | **51.4%** |
| IV/RV ratio | 1.15 | **0.97** |

Index options typically run IV/RV around 1.20-1.25. **NIO's 0.97 means there is
no volatility risk premium in it at all** — you would be selling insurance below
cost. Single-name VRP cannot be assumed from the index literature; it has to be
measured per name.

### The wheel, simulated with bid-side fills

97 overlapping cycles, sell at the bid, buy at the ask:

| | SNAP | NIO |
|---|---|---|
| overlay P&L, median | +$20.22 | +$9.43 |
| overlay P&L, **mean** | **+$13.29** | **−$1.31** |
| worst cycle | −$111.41 | −$231.78 |
| annualized on collateral | **+16.6%** | −2.6% |

Note the shape on SNAP: **positive median, much thinner mean.** 85.6% of cycles
profit; the 1st percentile is −$92, which is −10.9% of the whole account from the
option leg in a single month. That is the signature of short-vol — many small
wins, occasional large loss — and it is why median returns are the wrong statistic
to judge it by.

### Why it still loses, and it is not the spread

The obvious suspect was transaction cost. **Measured spread cost was ~3% of
premium — immaterial.** The real arithmetic:

- Best surviving strategy harvests **$134.70/year**.
- Paying $1,023.12 against 23% APR saves **$235.32/year**, guaranteed, zero drawdown.
- The debt wins by **~$100/year before counting any equity risk.**

And a structural drag that is easy to miss: 100 SNAP at the ask costs **$540 =
52.8% of the account**, leaving **$483 idle** earning nothing while the debt
compounds. So the account-level return is 16.6% × 52.8% = **~8.8%**, not 16.6%.
**The cheap-stock constraint forces you to strand half the capital**, and that
halving is invisible if you quote returns on collateral instead of on the account.

### Objections that were tested and failed

- *"The wheel beat buy-and-hold by 16.5 pts/yr and halved drawdown (31.8% vs
  62.8%)."* True, and the honest strongest counterargument. The edge is real. It
  is **6.4 points short of the hurdle** and cannot be levered or diversified at
  this size.
- *"The sample was a falling tape."* Conceded — both names fell. But clearing 23%
  needs the stock to add +6.4%/yr on top of the overlay while the call caps
  upside near +11.2% per cycle. **0% of rolling 1-year windows delivered it**
  (median −32.3%). You would need a stock that rises enough to clear the hurdle
  but not enough to be called away — a target you cannot select for in advance.
- *"Sell cash-secured puts instead, no stock risk."* **Put-call parity.** A CSP at
  the same strike and expiry is synthetically the identical position to the
  covered call. Same short-vol exposure, same shortfall, different-looking screen.

### What would have to change for the answer to become yes

1. **IV ~82% against RV ~51%** — a 30-point premium, not the measured 7.8. That
   is a panic condition, not a standing one.
2. **Account ≥ ~$10,000**, so 100 shares is ≤10% of capital and five-plus
   uncorrelated names run at once. **The VRP is a diversification strategy; at
   n=1 you are not harvesting a premium, you are making one directional bet with
   a small rebate.**
3. **Option level 3**, so risk is defined and collateral is a fraction of the position.
4. **No 23% debt.** Against a zero opportunity cost, SNAP's +16.6% overlay would
   be worth running. The debt is what makes it unwinnable — and it is the one
   variable here that can be fixed with certainty.

## 5b. The ruin side: measured, and worse than the return shortfall

1,479 entry-months across 54 liquid names, monthly bars 2010-2026. Split-adjusted
for return math, raw prices to define the bucket — **reverse splits are endemic
below $10** and unadjusted data shows fake single-month "gains" of +3,351% (FCEL),
+1,207% (CHPT) that would erase exactly the ruin cases being measured.

### How often a single sub-$10 name goes against you

Probability it trades this far below entry at some point:

| horizon | ≥30% | ≥50% | ≥70% |
|---|---|---|---|
| 3 months | 21.0% | 4.9% | 0.6% |
| 6 months | 35.5% | 13.4% | 3.0% |
| **12 months** | **50.2%** | **25.6%** | **8.7%** |

**It is a coin flip that the name is 30% underwater within a year, and one in four
that it halves.** Benchmark by the identical method: **SPY 1.6%**, IWM 6.9%. Roughly
**30x the index tail, borne in one position.**

Robustness checks, all pointing the same way:
- Non-overlapping episodes (n=307): **53.7 / 30.5 / 12.3** — slightly *worse*, so
  overlapping windows are not manufacturing the result.
- Stripping every miner, EV, hydrogen, crypto and meme name (33 left): **43.8 /
  17.8 / 4.0**. The tail shrinks and does not disappear.
- **The risk is a common factor, not idiosyncratic.** Entry-year cohorts hitting
  −30% range from 10.6% (2013) to 85.8% (2019) and 74.0% (2022). Rotating names
  during a bad year does not save you.
- **Survivorship bias runs one way.** Names that delisted to zero are absent from
  the broker's history entirely, so **every figure above is a lower bound.**

**The honest caveat that cuts against the framing:** the $10-20, $20-50 and $50+
buckets in the same universe show **49.1%, 54.0% and 47.9%** at −30%. Price level
per se is *not* the cause. What can be claimed is narrower and still binding: the
set of companies whose 100 shares fit inside a four-figure account carries this
tail.

### "The premium lowers your cost basis" is false where it matters

Live premium is real — 2-4% of spot per month at ~30 delta. Applied month by month
across all 1,396 twelve-month episodes:

| realized 12m drawdown | share | premium collected | covered call | buy & hold |
|---|---|---|---|---|
| ≤ −70% | 8.7% | 19.0% of basis | **−74.2%** | −67.0% |
| −50 to −70% | 16.9% | 24.0% | −40.7% | −40.0% |
| −30 to −40% | 14.0% | 28.6% | −1.2% | −7.3% |
| better than −30% | 49.1% | 35.7% | +34.2% | +29.6% |

In the worst cohort a full year of writing produced **19% of basis against a 79%
decline**, and the covered call finished **worse than simply holding**.

The mechanism is the part to remember: **premium is a percentage of *current*
spot.** As the stock falls, the dollars collected fall with it. The cushion is
thickest exactly where it is not needed and thinnest exactly where it is.

### The rebound is what it actually costs you

Episodes that drew down ≥30% **yet finished the year up** — n=127, 9.1% of entries,
the single most common redemption path for a cheap stock:

| | median 12m |
|---|---|
| buy & hold | **+37.8%** |
| covered call | **−1.5%** |

**45.2 points of rebound surrendered, and 53.5% of these ended the year NEGATIVE
while the stock finished UP.** Selling calls converts a V-shaped recovery into a
permanent loss. Surviving the crash and forfeiting the rebound is still ruin.

### Strike spacing removes the choice on a cheap stock

RIG at $5.77 has **$1 strike spacing**. There is no 30-delta strike: the options are
a 43-delta call at +4% (4.3%/mo, capped almost immediately) or a 12-delta call at
+21% (0.87%/mo, no meaningful income). Simulated, both land at a median 12-month
return of **−0.1%**. The market prices the trade-off away — you cannot pick a
better corner.

### Mechanics that bite

- **Bid/ask is the largest recurring cost.** ITUB's $9 call quotes 0.15/0.20 against
  a $0.175 mark — one tick is **29% of the option's value**. Written monthly,
  spread-crossing alone burns **3-4% of the account per year**.
- **Called away** a median of **3 months out of 12**; 42% of years see 4+
  assignments, each forcing a re-entry at a higher price.
- **Early assignment before ex-dividend** costs $2-11 per 100 shares — negligible in
  dollars, but it forces the exit.
- **"Cash-secured" describes how the position is funded, not that anything is
  protected.** Post $900 against a $9 put, get assigned at $9 with the stock at $5,
  and you hold $500 of stock for $900 of collateral.
- **Pin risk:** a close within pennies of the strike leaves assignment unknown until
  the weekend. On a four-figure account an unexpected 100-share assignment can
  exceed available cash and force a Monday liquidation at the open.

### The bottom line

Probability that a year of wheeling one sub-$10 name leaves the owner **worse off
than simply paying 23% debt**:

| scenario | P(< +23%) | P(loses money) |
|---|---|---|
| best premium available, any name | 55.4% | 33.7% |
| **central: realistic premium and slippage** | **73.1%** | **50.1%** |
| realistic premium on a high-vol name | 89.0% | 70.0% |

**~70%, defensible range 55-80%.** Where the $1,023 lands after a year: p5 **$482**,
p50 **$1,022**, p95 $1,768. **6.1% chance of ending below $500.**

Sorting by volatility shows the trap is inescapable: the low-vol tercile is the best
available choice and **still 55.4% worse than the debt**. And the one corner that
would work — low volatility *combined with* rich premium — **does not exist in the
market**: the 27%-vol names are the ITUBs, and ITUB pays 2.1%/month, not 4%.
Pricing that corner as achievable is the error the entire strategy rests on.

### What would change the answer

**Eight to ten uncorrelated names.** The clustering above is a common factor, so
breadth is what compresses the tail — nothing else does. At $1,023 with a 100-share
lot requirement, exactly **one** name is holdable.

Both desks reached this independently from opposite directions. Desk A: *the VRP is
a diversification strategy; at n=1 you are not harvesting a premium, you are making
one directional bet with a small rebate.* Desk B: *that constraint, not the
strategy, is what makes this unsurvivable.*

**The binding constraint is n=1, not the strategy.** Record it that way, because the
strategy will look attractive again the next time someone reads about the wheel.

## 6. Greeks worth tracking at this size

Most greek discussion is noise for a one-contract account. Three earn attention:

- **Delta** ≈ the option's probability of finishing in the money, and the shares
  it behaves like. A 30-delta call moves like 30 shares and has roughly a 30%
  chance of expiring ITM. It is the cleanest available read on "how likely is
  this."
- **Theta** — the daily cost of being early. It accelerates into expiry, so a
  correct thesis on the wrong schedule still loses. Long premium pays theta;
  short premium collects it. This is the entire mechanical reason §5 is the only
  candidate edge.
- **Vega** — exposure to implied vol itself. Buying before an event means buying
  inflated vol, and the post-event collapse can lose money **even when the
  direction was right**. This is why an option bought into a scheduled print is
  a worse bet than the direction alone suggests.

Gamma, rho and the rest do not change a decision at one contract. Skip them.

## 7. The hurdle rate is not zero

Whenever the account owner carries debt, the comparison is never "does this
strategy make money." It is "does it beat the guaranteed return of paying the
debt." At **23% APR** on a credit card, an options program returning 15%
annualized is **destroying value with extra steps**, and doing so with variance
attached.

State every options return **annualized and net of spread**, next to the debt
rate. If it does not clear the hurdle, the analysis is finished regardless of
how elegant the structure is.
