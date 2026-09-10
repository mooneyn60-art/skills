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
