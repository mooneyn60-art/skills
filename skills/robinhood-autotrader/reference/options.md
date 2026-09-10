# Options in a Small Account

What is actually available, what is measured, and what is still hypothesis.
Last updated: 2026-09-10 · Status: active · Audience: TARS

## Overview

Options reasoning fails in a small account for reasons that have nothing to do
with picking direction. The binding constraints are **permission level**,
**collateral arithmetic**, and **the absence of a stop** — and each one
invalidates a piece of the equity risk framework that would otherwise carry over.
This file records what has been measured on the live account, and marks clearly
what has not.

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

## 4. There is no stop on a long option, so the equity risk framework does not port

The equity framework sizes from the stop: `shares = risk_budget ÷ (entry − stop)`.
That machinery assumes an exit at a known price. A long option has no such exit:

- The underlying gaps through any level you had in mind, and
- implied vol collapses at the same moment, so the option loses on **both**
  legs of its value at once.

**The premium is the stop.** Buying a $50 option is taking a $50 loss with
some probability of not taking it. So premium is not risk-sized against the
account — it is spent against the headroom between account value and the floor
below which the account cannot go.

**The floor test:** `max premium = (account value − floor) × fraction stakeable
on one binary`. If that number is smaller than one contract, the trade does not
exist at this size. Say so rather than shrinking the thesis to fit.

## 5. Selling premium is the only candidate edge — and it is UNVERIFIED here

The volatility risk premium — implied vol systematically exceeding subsequent
realized vol — is the one documented edge reachable at level 2. Sellers of
options are, on average, paid for insurance that on average does not pay out.

**This is hypothesis, not established fact, for this account.** As of
2026-09-10 two desks are measuring (a) whether the premium survives real
bid-ask spreads on sub-$10 underlyings, and (b) how often such names draw down
30/50/70%, which is the concentration risk §2 forces. **Do not act on the wheel
until those come back with numbers.** Update this section when they do.

The known objections, to be tested rather than assumed away:
- **Capped upside, uncapped downside.** A covered call keeps every dollar of
  the decline and surrenders the rebound above the strike. Surviving the crash
  and forfeiting the recovery is still ruin, just slower.
- **"Premium lowers your cost basis"** is the reassuring phrase. 2-4% a month
  against a 40% drawdown is not protection, and the sentence should be treated
  as marketing until the arithmetic is done.
- **Assignment is not symmetric.** Short calls can be assigned early before an
  ex-dividend date; a CSP assigned well below strike leaves shares worth far
  less than the collateral posted.

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
