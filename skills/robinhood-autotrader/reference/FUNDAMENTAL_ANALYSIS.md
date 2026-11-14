# Fundamental Analysis — Reading the Business Behind the Ticker

The one pillar missing until now: everything else in `reference/` covers
price action, options mechanics, macro, sectors, and psychology — none of it
explains how to read whether the *company* itself is actually healthy. This
does, sourced rather than recalled.

Last Updated: 2026-09-15 · Status: active · Audience: TARS, for sharper
catalyst research, not a new entry rule

## Overview

R2 never looks at a balance sheet — it's pure trend, deliberately, because
this account has no forecasting edge and isn't pretending otherwise. But
every catalyst check already run tonight (SIRI's Deutsche Bank upgrade,
OVV's Stifel initiation, PFE's BMO target raise) cited an analyst target
without ever asking *what the analyst is actually pricing* — earnings power,
balance sheet risk, whether the number is real. This file is the missing
layer underneath those checks, not a new gate to add to R2.

## The three statements, and why none of them alone is the whole picture

- **Income statement** — did the company make money this period. Revenue
  minus costs and expenses, down to net income. Covers a *period* (a quarter
  or a year).
- **Balance sheet** — what the company owns and owes *right now*, a single
  point in time. Assets = Liabilities + Equity, always, by construction —
  if it doesn't balance, something's wrong with the data, not the company.
- **Cash flow statement** — where cash actually came from and went:
  operating, investing, financing. This is the one that can't be dressed up
  by accounting choices the way net income can.

[SEC: Beginners' Guide to Financial Statements](https://www.sec.gov/about/reports-publications/investorpubsbegfinstmtguide) ·
[CFI: The Three Financial Statements](https://corporatefinanceinstitute.com/resources/accounting/three-financial-statements/)

**Why read all three together, not just one:** a company can report growing
net income while actually running out of cash — the income statement alone
would miss it. Reading all three together shows whether reported profit is
real or just an accounting artifact, which is exactly the check the next
section formalizes.

## Earnings quality: is the profit real?

Net income is *accrual* accounting — revenue and expense get recognized when
earned/incurred, not when cash actually changes hands. That gap is normal in
small amounts and a real warning sign when it grows.

**The single most useful check:** compare operating cash flow to net income.
- **Cash flow ≈ or > net income:** healthy — the reported profit is backed
  by real cash coming in the door.
- **Cash flow well below net income, and the gap widening over several
  quarters:** a real red flag. It usually means profit is sitting in
  accounts receivable (shipped the product, booked the revenue, hasn't been
  paid yet) or inventory, or the company is using aggressive accounting
  estimates. [Cash Flow Quality Guide](https://www.investing.com/academy/analysis/cash-flow-quality-guide/)
- **A specific pattern worth naming:** revenue and accounts receivable both
  rising is normal; **accounts receivable rising *faster* than revenue** is
  the classic sign of channel-stuffing (aggressive quarter-end shipping just
  to book revenue) — a company can look like it's growing while actually
  just pulling sales forward from next quarter.
  [Earnings Quality Erosion via Cash Flow](https://site.financialmodelingprep.com/education/statements/how-to-detect-earnings-quality-erosion-via-cash-flow-statement)

This is a real, practical filter to run on any name before treating an
earnings beat as clean: a beat backed by real cash generation is a different
signal than a beat backed by a receivables pileup, even though both show up
as the same green "beat" headline the market reacts to identically at first.

## The moat: is the advantage durable, or just a good quarter

Buffett's own framing, and the one that gets cited constantly and understood
loosely: an economic moat is a **sustainable competitive advantage that lets
a company earn excess returns on capital for a long time and keep
competitors out** — the metaphor being a castle's moat keeping invaders from
eroding market share and pricing power.
[Morningstar: Economic Moat](https://www.morningstar.com/investing-terms/economic-moat) ·
[Wikipedia: Economic Moat](https://en.wikipedia.org/wiki/Economic_moat)

**The word that actually matters is durability**, not the advantage itself.
Buffett's own line: "The key to investing is not assessing how much an
industry is going to affect society, or how much it will grow, but rather
determining the competitive advantage of any given company and, above all,
**the durability of that advantage.**" A hot product cycle is not a moat if
a competitor can replicate it next year. Real, durable sources of one:

- **Network effects** — the product gets more valuable as more people use it
  (a marketplace, a payment network)
- **Economies of scale** — genuinely lower cost per unit than any competitor
  could match without matching the scale first
- **Switching costs** — expensive or disruptive for a customer to leave,
  independent of whether a competitor's product is actually better
- **Brand** — genuine pricing power from trust/reputation, not just
  familiarity

**Practical takeaway for catalyst research:** when a name passes R2 on a
sharp move (SentinelOne's cybersecurity pop, TENB's sector-wide rally), the
honest question isn't "is this a good company" — R2 already answered the
trend question — it's "is whatever drove this move a durable re-rating or a
one-quarter event that fades," which is exactly what `options.md`'s section
0 protocol is checking when it separates a real catalyst from an unexplained
pop that mean-reverts.

## How this connects to what's already being done here

`SECTOR_ANALYSIS.md` explains why the *ratio* changes by sector (P/FFO for
REITs, EV/EBITDA for energy). This file explains what to actually check
underneath that ratio once it's chosen: does the earnings number backing it
hold up against real cash flow, and is whatever is driving the stock's move
a durable advantage or a one-quarter story. Neither becomes a new R2
condition — R2 stays exactly what it is, pure trend, no discretion. This is
purely for sharpening the catalyst write-up that already happens before an
option gets researched or a diversification pick gets chosen, the same way
tonight's SIRI/OVV/PFE checks already tried to do informally.
