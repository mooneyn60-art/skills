# Sector Analysis — Business Cycle Rotation and Valuation

Sourced reference on the 11 GICS sectors, business-cycle rotation, and why
different sectors get valued on different metrics entirely. New ground —
`MARKET_MECHANICS.md` covers how prices move mechanically; this covers which
*group* of stocks tends to lead or lag depending on where the economy is, and
how to read a company's numbers correctly once its sector is known.

Last Updated: 2026-09-15 · Status: active · Audience: TARS, for sharper R2
catalyst research, not a new rule

## Overview

R2 doesn't care about sector at all — it's pure trend (200d/50d MA, 20-day
high proximity). That's a real, deliberate design choice, not a gap: this
account has no forecasting edge, so it rides what's already trending rather
than betting on which sector *should* lead next. This file exists anyway for
two honest reasons: it makes the diversification requests this account gets
("stay away from tech, try natural resources") a real, informed judgment
instead of a guess, and it sharpens the *catalyst* research already being run
before an equity or option decision — reading an analyst target or an
earnings beat correctly depends on knowing which multiple that sector
actually trades on.

## The 11 GICS sectors

Energy, Materials, Industrials, Consumer Discretionary, Consumer Staples,
Health Care, Financials, Information Technology, Communication Services,
Utilities, Real Estate. This account's own sector filter
(`FILTER_TYPE_SECTOR`) uses a slightly coarser version of the same taxonomy.

## Business-cycle rotation: who leads, who lags, and why

The core idea (Fidelity's own institutional framework, among others): a
typical cycle runs early → mid → late → recession, and different sectors are
priced for different parts of it because their revenue is tied to different
parts of the economy — a homebuilder needs cheap credit and improving
sentiment; a utility needs none of that and gets bought for the dividend when
everything else looks scary.

| Phase | What's happening | Sectors that tend to lead | Why |
|---|---|---|---|
| **Early cycle** | Rates falling/low, sharp recovery off a trough | **Consumer Discretionary, Industrials, Financials, Technology** | Consumer Discretionary has beaten the broader market in *every* early cycle since 1962 (Fidelity) — cheap credit + improving sentiment hits discretionary spending first, financials front-run the credit expansion |
| **Mid cycle** | Broader, more self-sustaining growth; inflation starts rising, policy tightens | **Technology, Industrials, Healthcare** | Leadership rotates fastest here — smallest performance gap between sectors of any phase (Fidelity) |
| **Late cycle** | Growth slowing, inflation often still elevated | **Energy, Materials** | Energy has historically outperformed through the early *and* mid phases too while the economy is still growing, then holds up into late-cycle on tight supply/still-high demand |
| **Recession / trough** | Contraction, capital flight to safety | **Utilities, Consumer Staples, Health Care** — then **Financials and Real Estate begin outperforming right at the trough** | Defensive earnings (people still buy toothpaste and electricity in a recession) get bid up for safety; Financials/Real Estate turn first at the trough because markets front-run the coming rate cuts and credit expansion |

[Fidelity: The Business Cycle Approach to Equity Sector Investing](https://www.fidelity.com/viewpoints/investing-ideas/sector-investing-business-cycle) ·
[Fidelity: Intro to Sector Rotation Strategies](https://www.fidelity.com/learning-center/trading-investing/markets-sectors/intro-sector-rotation-strats)

**Read this as color, not a signal.** This account doesn't time sectors —
R2 finds names already trending regardless of the macro story. But it's why
a name passing R2 in Energy (OVV) or Industrials (BAH, CNH) isn't a red flag
on its own late in a cycle with still-strong commodity demand, while the same
setup in a richly-valued discretionary name deep into a slowdown deserves a
second look at the macro backdrop specifically (same instinct as
`options.md` section 0's macro-calendar check, just at the sector level
instead of the single-name level).

## Why the same ratio means different things in different sectors

A P/E of 15 is not "cheap" or "expensive" in the abstract — it's only
meaningful relative to what that sector normally trades at, because
different sectors' earnings have completely different risk and capital
structure behind them.

- **REITs (Real Estate):** P/E is close to useless — REITs must distribute
  most of taxable income as dividends and carry heavy depreciation that
  distorts GAAP earnings. The standard metric is **P/B and, more
  specifically, P/FFO (Funds From Operations)** — cash flow-based, and
  measurably more accurate for this sector than earnings multiples. Some
  fast-growing REIT niches (e.g. data-center REITs riding AI power demand)
  can carry P/FFO multiples of 25-40x, which would be an absurd earnings
  multiple anywhere else and is a normal one there.
  [Financial analysts' use of industry-specific valuation models](https://www.sciencedirect.com/org/science/article/pii/S0967542625000025)
- **Energy:** **EV/EBITDA and price-to-cash-flow** are preferred over P/E —
  cash flow is harder to manipulate than earnings and less distorted by
  volatile commodity-price swings hitting the income statement unevenly.
  As of the sourced data, the sector traded near 22.8x trailing earnings but
  9.2x EV/EBITDA and a ~4.8% implied free-cash-flow yield — the multiple you
  quote changes the read entirely.
  [Energy sector valuation basics](https://www.investing.com/news/stock-market-news/energy-sector-basics-valuation-cash-flow-and-how-beginners-can-start-93CH-4898278)
- **Financials, insurers:** **P/B (price-to-book)** is the reference metric
  for balance-sheet-heavy sectors where the book itself (loans, float,
  reserves) is the actual asset being priced, not a smooth earnings stream.
- **Everything capital-intensive** (industrials, telecom infrastructure,
  parts of energy): **EV/EBITDA** strips out differences in debt load and
  depreciation policy, which a plain P/E can't do across companies with very
  different balance sheets.
[CFA Institute: Market-Based Valuation, Price and Enterprise Value Multiples](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/market-based-valuation-price-enterprise-value-multiples)

**Practical takeaway for this account:** when an equity note cites an
analyst price target or a "cheap/expensive" claim (same as the SIRI/OVV/PFE
research tonight), check which multiple that analyst is actually using
before treating the target as comparable across names in different sectors
— a bank's "attractive P/B" and a REIT's "attractive P/FFO" aren't the same
kind of claim, and neither is directly comparable to TENB's or S's growth-
software multiple.

## Current book, read through this lens

Communication Services (T, WBD, VZ, SIRI) and Technology (TENB, S) are the
most represented; Energy (OVV), Industrials (BAH, CNH), Financial Services
(NAVI), and Healthcare (PFE) round it out. Zero exposure in Real Estate,
Consumer Staples/Defensive, Consumer Discretionary/Cyclical, Utilities,
Materials — consistent with tonight's Idea Desk shortlist, which found real
R2 passes specifically in the zero-exposure sectors (REXR/Real Estate,
UTZ/Consumer Defensive, AES/Utilities) worth prioritizing for the next open
slot on diversification grounds, not because the business cycle says to.
