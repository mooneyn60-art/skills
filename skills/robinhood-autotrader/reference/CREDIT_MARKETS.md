# Credit Markets — Reading Credit Stress Before It Reaches Equities

Sourced research on credit spreads, the yield curve, CDS markets, and funding-
stress indicators as leading signals of equity-market stress — what each one
actually measures, the real evidenced track record (not folklore), and an
honest line between "useful context" and "a new signal for this account."

Last Updated: 2026-09-16 · Status: active · Audience: TARS, and anyone reading
over its shoulder

## Overview

`FED_AND_RATES.md` already covers how the Fed enforces its rate band, the dot
plot, and QE/QT. This file covers a different, related gap: **credit
markets** — corporate bond spreads, the yield curve as a recession predictor
specifically, CDS markets, and short-term funding stress — as leading
indicators that something is wrong before it shows up in stock prices. The
core idea across every section below is the same: credit investors and
equity investors are pricing the same underlying company risk, but credit
investors are structurally asymmetric (they get their coupon and principal
back if things go fine, and lose money if the company defaults — no upside
participation in a rally), which several of the sources below argue makes
them faster to reprice deteriorating conditions than equity holders, who
still have a call option on the upside.

That said, this document draws a hard, honest line between what is
**well-evidenced** and what is **repeated so often in financial commentary
that it sounds evidenced but isn't precisely quantified anywhere
peer-reviewed.** Where a specific number (a lead time in weeks, a spread
level with "100% reliability") could not be traced to a real, citable study,
this file says so explicitly and describes the mechanism qualitatively
instead — per this repo's standing no-fabrication policy.

---

## 1. Credit spreads — what widening actually means, and the real track record

**Mechanically, a credit spread is simple.** It's the extra yield a corporate
bond pays over a Treasury of the same maturity, compensating the lender for
the risk the Treasury doesn't have: the corporation, unlike the U.S.
government, can default. When that spread widens, the bond market is
literally repricing — demanding more compensation per unit of credit risk on
the *same* company for the *same* maturity, which only happens if the market's
estimate of default probability, loss-given-default, or the price of bearing
that risk at all has gone up. The standard public benchmark for this is the
ICE BofA US High Yield Index Option-Adjusted Spread (ticker `BAMLH0A0HYM2`),
a capitalization-weighted, daily-updated spread of below-investment-grade
(BB and lower) U.S. dollar corporate bonds over the matched-maturity Treasury
curve — a widely followed, real-time gauge of default risk and broad
financial-market stress.
[FRED: ICE BofA US High Yield Index Option-Adjusted Spread (BAMLH0A0HYM2)](https://fred.stlouisfed.org/series/BAMLH0A0HYM2)

**The rigorous academic case that credit spreads lead the real economy** comes
from Gilchrist and Zakrajšek's "Credit Spreads and Business Cycle
Fluctuations" (*American Economic Review*, 2012). They decompose corporate
credit spreads into (a) a component explained by each firm's own expected
default risk, and (b) a residual "excess bond premium" (EBP) that reflects the
risk-bearing capacity and risk appetite of the financial sector itself —
separate from default risk. Their central finding: it's specifically the EBP,
not the raw spread, that predicts declines in economic activity and asset
prices, because a rising EBP signals a *contraction in the supply of credit*
as intermediaries pull back risk-bearing capacity, which then feeds into
weaker output. The Federal Reserve took this seriously enough to start
publishing the EBP and an associated 12-month recession probability as a
standing monthly release.
[Gilchrist & Zakrajšek, "Credit Spreads and Business Cycle Fluctuations," *AER* 102(4), 2012](https://www.aeaweb.org/articles?id=10.1257%2Faer.102.4.1692)
· [NBER Working Paper 17021 (earlier version)](https://www.nber.org/papers/w17021)
· [Federal Reserve: "Updating the Recession Risk and the Excess Bond Premium" (Oct 2016)](https://www.federalreserve.gov/econres/notes/feds-notes/updating-the-recession-risk-and-the-excess-bond-premium-20161006.html)

**Real, dated episodes where credit stress visibly ran ahead of equities:**

- **2007-08.** Credit market stress became publicly undeniable on **August 9,
  2007**, when BNP Paribas froze redemptions on three funds exposed to U.S.
  subprime mortgages, citing a total evaporation of liquidity in parts of the
  securitization market — the event widely cited as the start of the credit
  crunch, and one that visibly froze short-term interbank lending that same
  day. The S&P 500 did not make its cycle high until **October 2007**, roughly
  two and a half months later, and did not enter its recognized bear market
  until well into 2008. [CNBC: "BNP Freezes $2.2 Billion of Funds Over
  Subprime" (Aug 9, 2007)](https://www.cnbc.com/2007/08/09/bnp-freezes-22-billion-of-funds-over-subprime.html)
  High-yield spreads then went on to reach their historical extreme —
  commonly reported around 2,000+ basis points — in **December 2008**, well
  after Lehman's September 2008 failure, tracking the FOMC's own December 2008
  discussion of financial conditions.
  [FOMC Minutes, December 15-16, 2008](https://www.federalreserve.gov/monetarypolicy/fomcminutes20081216.htm)
- **2015-16 energy credit stress.** Collapsing oil prices from mid-2014
  through early 2016 drove a real, measured, *sector-contained* credit event:
  Morningstar's year-end wrap reported the broad high-yield index spread
  widened by 191 basis points to end 2015 at roughly +695 bps, but the
  energy-sector component alone widened almost 660 bps to roughly +1,415 bps
  — more than double the market-wide move. [Morningstar: "2015 Corporate Bond
  Wrap-Up and First-Quarter 2016 Outlook"](https://www.morningstar.com/bonds/2015-corporate-bond-wrap-up-first-quarter-2016-outlook)
  Separate research found oil-price moves explained over 70% of the spread
  widening in energy-firm bonds specifically over that window. This is the
  cleanest real-world illustration that a credit blowout is not automatically
  an equity-market-wide signal: the S&P 500 saw a sharp but short correction
  in January-February 2016 and no bear market, because the credit stress was
  genuinely concentrated in one sector's balance sheets, not systemic.
- **2020 COVID crash.** The Federal Reserve's own account states credit
  spreads "reached their peak at about 5% for BBB-rated corporate bonds and
  11% for high-yield bonds" in mid-March 2020, with the high-yield spread
  rising from roughly 4% in February to roughly 11% by March 23 — the day the
  Fed announced its Primary and Secondary Market Corporate Credit Facilities,
  which rapidly reversed the widening.
  [Federal Reserve: "The Corporate Bond Market Crises and the Government Response" (Oct 2020)](https://www.federalreserve.gov/econres/notes/feds-notes/the-corporate-bond-market-crises-and-the-government-response-20201007.html)
  · [St. Louis Fed: "Corporate Bond Spreads and the Pandemic"](https://www.stlouisfed.org/on-the-economy/2020/april/effects-covid-19-monetary-policy-response-corporate-bond-market)
  Here credit and equity stress moved almost simultaneously (the S&P 500 fell
  34% over the same weeks — see `BEAR_MARKET_PLAYBOOK.md`), a case where the
  shock (a pandemic-driven stop in economic activity) hit both markets at
  once rather than credit leading equities by any real margin.
- **2022 — the honest counter-example.** The 2022 bear market (S&P 500 down
  roughly 25.4% peak-to-trough, per `BEAR_MARKET_PLAYBOOK.md`) is the case
  that argues *against* treating credit spreads as a universal leading
  indicator: it was a rate-driven, discount-rate-channel bear market (see
  `FED_AND_RATES.md`'s discount-rate mechanism), not a credit-driven one, and
  high-yield spreads stayed comparatively contained throughout — commentary
  citing spread peaks below 600 bps even during the March 2023 regional-bank
  stress episode, versus multi-thousand-bp peaks in 2008. Credit spreads did
  not blow out ahead of, or during, the 2022 equity decline the way they did
  in 2008 or 2020, because the driver was valuation compression from rising
  discount rates, not rising default risk.

**Honest caveat on precision — what could not be verified.** Financial
commentary widely asserts specific lead-time figures ("credit leads equity by
2-6 weeks," "HY OAS leads equity drawdowns by 1-3 months") and specific
threshold claims ("spreads above 800bps predict recession with 100%
reliability"). None of these specific numbers could be traced to a
peer-reviewed or primary-source study during this research pass — they
circulate on financial-commentary and aggregator sites without a clearly
cited underlying methodology, and this file will not repeat them as fact.
What **is** well-evidenced, per Gilchrist & Zakrajšek above, is the more
modest and qualitative claim: the excess bond premium component of credit
spreads has genuine, published predictive power for GDP growth, industrial
production, and unemployment over roughly a one-to-four-quarter horizon —
and the 2007-08 and 2020 episodes above show credit stress visibly present
before or alongside the worst of the equity decline, without a single
universal "lead time in weeks" number attached.

**A related, well-documented false-positive episode worth naming honestly:**
the August-September 1998 Russian default and Long-Term Capital Management
crisis produced a real, sharp widening in credit spreads and a "flight to
quality" into Treasuries — but because the Federal Reserve responded with
three successive 25-basis-point rate cuts, no U.S. recession followed, and
the spread widening reversed within months. [Federal Reserve Bank of Chicago,
"The crisis of 1998 and the role of the central bank"](https://www.chicagofed.org/-/media/publications/economic-perspectives/2001/1qepart1-pdf.pdf)
A credit-spread spike is a real signal of stress in the moment it happens; it
is not a guarantee that stress becomes a recession or a bear market — policy
response and whether the shock is systemic both matter.

---

## 2. Investment-grade vs. high-yield vs. leveraged loans — the real risk hierarchy

These three sit in a genuine, sourced order of both **seniority** (who gets
paid first in a default) and **sensitivity** (how fast the market price moves
when conditions change):

| Instrument | Typical seniority | Rate structure | Historical recovery in default | Sensitivity |
|---|---|---|---|---|
| Investment-grade bonds (BBB-/Baa3 and above) | Usually unsecured, senior | Fixed | Highest of the three (lowest expected loss) | Slowest to reprice — the credit-quality floor is high, so marginal news moves spreads the least |
| High-yield ("junk") bonds (BB+ and below) | Often unsecured or subordinated | Fixed | Historically **~30-40 cents on the dollar** | Fastest-moving of the bond tiers — the whole point of §1 above |
| Leveraged (bank) loans | Usually senior secured, first-lien against company assets | **Floating rate**, resetting every 1-3 months | Historically **~60-70 cents on the dollar** — higher than HY bonds because of seniority and collateral | Fast-moving on rates specifically, since coupons reset with short-term rates; historically lower default rate and volatility than HY bonds, but see below |

Recovery-rate figures per [Marquette Associates, "We're Not So Different: High
Yield Bonds and Leveraged Loans"](https://www.marquetteassociates.com/wp-content/uploads/2023/12/Were-Not-So-Different-High-Yield-Bonds-and-Leveraged-Loans.pdf)
and [J.P. Morgan Asset Management, "The Case for Leveraged Loans"](https://am.jpmorgan.com/us/en/asset-management/liq/insights/portfolio-insights/fixed-income/fixed-income-perspectives/the-case-for-leveraged-loans/).

**Why high-yield specifically, not investment-grade, is the more sensitive
early-warning instrument:** investment-grade issuers are, by construction,
already judged unlikely to default — spreads there move on macro discount-rate
and liquidity factors more than on rising default fear, and the 2020 data
above actually shows IG spreads moved *proportionally* less than HY spreads
even as absolute dollar amounts of stress were large. High-yield issuers sit
close enough to the default boundary that incremental bad news (earnings
miss, sector shock, funding-cost increase) has a real chance of tipping a
name into distress, so HY spreads carry more information about *changing*
default risk per unit of news — which is exactly why the GZ excess-bond-premium
literature above is built primarily from these instruments.

**Leveraged loans and private credit — the newer, less liquid layer of this
same hierarchy.** A 2026 Federal Reserve note comparing leveraged loans and
private credit found private-credit spreads running near 500 bps versus
roughly 400 bps for broadly-syndicated leveraged loans, with private-credit
borrowers materially more levered (median debt-to-EBITDA near 5x vs. 3.2x)
and a much larger share rated single-B. Critically, private credit has **no
active secondary market** — loans are held directly by a small group of
lenders and valued quarterly via internal models, versus daily-priced
leveraged loans distributed to CLOs, loan mutual funds, and ETFs — meaning
private-credit stress can build for a long time without showing up in any
publicly observable spread at all, unlike the publicly-traded HY and
leveraged-loan markets this section otherwise describes.
[Federal Reserve: "Private Credit and Leveraged Loan Markets: Similarities,
Differences, and Substitution" (Aug 2026)](https://www.federalreserve.gov/econres/notes/feds-notes/private-credit-and-leveraged-loan-markets-similarities-differences-and-substitution-20260811.html)
This is worth naming precisely because it's the opposite of a leading
indicator — it's a genuinely *hidden* one, for now, that this document cannot
turn into anything checkable.

---

## 3. The yield curve as a recession predictor — the specific, replicated evidence

`FED_AND_RATES.md` already explains the mechanics of how the Fed's target
range and the yield curve relate. This section is narrower: the actual,
published, replicated research on the yield curve's **recession-predicting**
power specifically.

**The foundational, real, citable study** is Arturo Estrella and Frederic
Mishkin's "The Yield Curve as a Predictor of U.S. Recessions" (Federal Reserve
Bank of New York, *Current Issues in Economics and Finance*, Vol. 2, No. 7,
June 1996). Using the spread between the 10-year Treasury note and the
3-month Treasury bill, they found this single spread "significantly
outperforms other financial and macroeconomic indicators in predicting
recessions two to six quarters ahead" — i.e., roughly **six months to a year
and a half** of typical lead time, using a probit model.
[Federal Reserve Bank of New York: "The Yield Curve as a Predictor of U.S.
Recessions"](https://www.newyorkfed.org/medialibrary/media/research/current_issues/ci2-7.pdf)
This is not a one-off backtest — the NY Fed maintains it as a **standing,
monthly-updated model**, using the formula P(Recession) =
Φ(−0.5333 − 0.6330 × Spread), where the spread is the 10-year minus 3-month
Treasury yield and Φ is the standard normal cumulative distribution function.
[Federal Reserve Bank of New York: "The Yield Curve as a Leading Indicator"](https://www.newyorkfed.org/research/capital_markets/ycfaq)

**Why the 3-month/10-year spread specifically, not 2s10s.** The NY Fed's own
published model is built and maintained on the 3-month/10-year spread, not
the 2-year/10-year spread that gets more attention in financial media.
Both spreads have inverted ahead of most post-war U.S. recessions, but the
NY Fed's own citable, replicated, formally-published research uses the
3-month tenor — worth knowing so a "2s10s hasn't inverted yet" headline isn't
mistaken for "the NY Fed's model says no recession risk," when those are two
different spreads with two different track records attached.

**The honest caveat: false positives and "this time is different" claims
have a mixed record.** The clearest real example is the brief, shallow
3-month/10-year inversion around 2019, which was followed by the 2020
recession — but that recession was caused by an exogenous public-health shock
(COVID-19) and the associated policy shutdown, not by the credit-cycle
dynamics (tightening financial conditions choking off business investment
and consumption) the yield curve model is built to capture. Commentary
broadly treats this as a case where the timing "worked" by coincidence rather
than by mechanism, though this specific interpretive judgment is a matter of
financial commentary rather than a peer-reviewed reclassification, and this
file flags it as such rather than asserting it as settled fact.
[S&P Global Market Intelligence: "Yield curve inversion could be false alarm
for US economy amid COVID upheavals"](https://www.spglobal.com/marketintelligence/en/news-insights/latest-news-headlines/yield-curve-inversion-could-be-false-alarm-for-us-economy-amid-covid-upheavals-68704354)
More generally: Estrella and Mishkin's own model is a *probability*, not a
certainty, and a two-to-six-quarter window is wide enough that "it inverted
and nothing happened yet" is not distinguishable, in real time, from "it
inverted and the recession hasn't arrived yet" — the honest position is that
this is a genuinely useful, well-replicated probabilistic tool, not a
crystal ball with a fixed countdown clock.

---

## 4. CDS markets — a faster, more liquid stress signal in some crises

**The real mechanics, not just the definition.** A credit default swap (CDS)
is a contract where the protection buyer pays a periodic premium (quoted in
basis points of notional) to the protection seller, who agrees to pay out if
the reference entity (a company or sovereign) suffers a defined credit event
(default, restructuring). Unlike a cash bond, a CDS requires no upfront
principal to trade and can be shorted with far less friction — sell
protection to go long credit risk, buy protection to go short it — which is
precisely why CDS markets can move faster and more visibly than the
underlying bond market during a fast-moving crisis: taking a bearish credit
view via CDS doesn't require sourcing and shorting an actual bond, an
operationally harder trade. Standardized CDS **indices** (CDX in North
America, iTraxx in Europe/Asia) bundle a fixed basket of names (e.g., CDX.NA.IG
holds 125 investment-grade names, CDX.NA.HY holds 100 high-yield names),
roll to a new series twice a year, and trade with deep enough liquidity to
function as a single quoted number for "market-wide credit stress" the way
the S&P 500 does for equities.
[Wikipedia: "Credit default swap index"](https://en.wikipedia.org/wiki/Credit_default_swap_index)
· [Wikipedia: "iTraxx"](https://en.wikipedia.org/wiki/ITraxx)

**2008 — single-name bank CDS as an early, if imperfect, warning.** Research
using bank CDS spreads found Bear Stearns' CDS spread was already the widest
in a 45-bank sample by **July 2007** (reported around 55 bps against a
roughly 12 bps median) — eight months before its March 2008 forced sale to
JPMorgan — a real, dated, single-name early-warning signal.
[NBER Working Paper 14904 (bank CDS spreads during the crisis)](https://www.nber.org/system/files/working_papers/w14904/w14904.pdf)
Lehman Brothers' case is the important counter-example inside the same
crisis: its CDS spread stayed comparatively stable through most of summer
2008 — reportedly around 250 bps in June 2008, up from roughly 80 bps in
September 2007, a real deterioration but not a scream — and did not spike
sharply until the week of its actual bankruptcy filing in September 2008.
One interpretation raised in the same research: the market's assumption that
regulators would rescue any systemically important firm (having just rescued
Bear Stearns) may have suppressed Lehman's CDS spread even as its underlying
condition worsened — a reminder that CDS pricing reflects the market's belief
about *whether a bailout is coming*, not only the entity's raw credit
quality.

**The European sovereign debt crisis — CDS on sovereigns, not just banks.**
The 2010-2013 European crisis extended the same instrument to sovereign
credit risk itself: sovereign CDS spreads reflect the market's expectation of
government default risk, and the interconnection between bank and sovereign
CDS pricing became a real, published stress channel in its own right, since
domestic banks are typically large holders of their own government's debt —
a sovereign CDS blowout and a domestic-bank CDS blowout tend to move together
because a sovereign crisis directly threatens the banks holding that
sovereign's bonds.
[ECB Financial Stability Review, June 2009, Box 3](https://www.ecb.europa.eu/press/financial-stability-publications/fsr/focus/2009/pdf/ecb~5d83ef45dd.fsrbox200906_03.pdf)
Since September 2008, CDS spreads have on average run *wider* than
equivalent-maturity cash-bond spreads on the same names — a "flight to
liquidity" effect where the CDS market, being more liquid and easier to
trade in size during stress, moved to price risk before the less-liquid cash
bond market fully caught up, which is the concrete mechanical reason CDS can
lead cash-bond spreads (and by extension equities) during acute crises
specifically, even though in calm markets the two track closely together.

---

## 5. TED spread and repo-market stress — funding/liquidity risk, not solvency risk

This is the section that most directly extends `FED_AND_RATES.md`'s
ON-RRP/standing-repo-facility content, and it is mechanically **different**
from every section above: credit spreads, CDS, and (indirectly) the yield
curve are pricing **solvency/default risk** — will this borrower actually pay
me back. A funding-stress spike prices something else entirely: can I get
cash *right now*, at any reasonable price, even from a borrower nobody
doubts is solvent.

**The TED spread**, historically the difference between 3-month interbank
(LIBOR-based) lending rates and the 3-month Treasury bill yield, captured
both credit and liquidity risk in the banking sector: a wider TED spread
meant banks were charging each other more to lend overnight/short-term,
reflecting either fear of counterparty default or a scramble for scarce
cash (or both). It sat in a normal range of roughly 10-50 bps and spiked to a
recorded **464 bps on October 10, 2008** — right after Lehman's failure, as
interbank lending effectively froze on mutual counterparty fear.
[Wikipedia: "TED spread"](https://en.wikipedia.org/wiki/TED_spread)
The TED spread itself is now a **discontinued, historical-only series**: the
underlying USD LIBOR panel stopped publishing after June 30, 2023, as part of
the industry-wide LIBOR-to-SOFR transition, so this exact metric no longer
exists as a live indicator — [FRED: TED Spread (DISCONTINUED)](https://fred.stlouisfed.org/series/TEDRATE) —
though the *concept* it captured (interbank/short-term funding stress vs. a
risk-free rate) still matters; it's simply measured through other funding
spreads and repo-rate behavior today, which is exactly what September 2019
demonstrated.

**September 2019 — a real, dated, non-solvency funding-stress event.** On
September 17, 2019, the Secured Overnight Financing Rate (SOFR) jumped from
2.43% to 5.25%, with intraday repo rates briefly trading as high as 10% —
more than 300 basis points above the top of the Fed's target range at the
time. Nobody's solvency was in question; the New York Fed and multiple
subsequent studies attribute the spike to a **confluence of technical
factors** — a corporate tax-payment date draining bank reserves, a wave of
Treasury settlement/issuance absorbing cash, and an overall lower level of
reserves in the system than the plumbing needed — that individually would
have been minor but combined into a real, sharp, short-term cash crunch. The
Fed responded within days by announcing a schedule of repo operations to add
reserves, and by October 2019 had resumed outright Treasury bill purchases.
[Federal Reserve: "What Happened in Money Markets in September 2019?"](https://www.federalreserve.gov/econres/notes/feds-notes/what-happened-in-money-markets-in-september-2019-20200227.html)
· [Office of Financial Research: "Anatomy of the Repo Rate Spikes in
September 2019"](https://www.financialresearch.gov/working-papers/files/OFRwp-23-04_anatomy-of-the-repo-rate-spikes-in-september-2019.pdf)
· [Wikipedia: "September 2019 events in the U.S. repo market"](https://en.wikipedia.org/wiki/September_2019_events_in_the_U.S._repo_market)

**Why this genuinely differs from a credit-spread widening.** A widening HY
OAS or a CDS blowout says "the market now believes this specific borrower (or
this basket of borrowers) is more likely to default." A repo/funding-stress
spike like September 2019 says "the plumbing that moves cash overnight
between institutions is jammed," independent of anyone's actual credit
quality — precisely the same floor-and-ceiling mechanical system
`FED_AND_RATES.md` describes (IORB/ON-RRP floor, standing-repo-facility
ceiling) exists specifically to prevent this kind of pure funding-liquidity
spike from recurring at the scale it did in September 2019, by giving banks a
standing, pre-committed source of overnight cash against safe collateral
rather than forcing them to bid against each other in a suddenly cash-short
market.

---

## 6. Is any of this actionable for this account? — an honest answer

**No — and that's consistent with how this repo already treats adjacent
context.** `BEAR_MARKET_PLAYBOOK.md` is explicit that its outside research
adds "outside confirmation, not a new argument" on top of R2's existing trend
rule, and `HIDDEN_MARKET_DRIVERS.md` is explicit that its whole catalogue of
mechanical price drivers is "explanatory context for separating a real
catalyst from an 'unexplained pop,' not a new R2 signal." This document
belongs in the same category, for the same reasons:

| Signal | Update frequency this account could realistically use | Should R2 gate on it? | Why it matters anyway |
|---|---|---|---|
| HY OAS / credit spreads | Available daily (FRED, free) | No — R2 is a pure price/MA technical system with no macro-data input, and §1 shows the lead-time claims precise enough to act on couldn't be verified | Explains *why* a sector or the market may be under pressure before it shows up as a stopped-out position — read after the fact, not traded on |
| Yield curve / 3m10y spread | Available daily, NY Fed model updates monthly | No — a 2-to-6-quarter recession probability has no actionable translation into a daily-bar stop-loss system, and §3's honest caveat is that the timing is genuinely uncertain in real time | Context for *why* R2's 200-day trend filter might be about to flip, not a reason to front-run it |
| CDS spreads (CDX/iTraxx, single-name bank/sovereign) | Not freely available at retail; typically dealer/terminal-only | No — this account has no data feed for it at all | Historical/explanatory value only for understanding past crises (2008, European sovereign crisis) |
| TED spread / repo stress | TED spread itself discontinued; SOFR-vs-Treasury proxies exist but are specialist data | No — a funding-liquidity event like September 2019 is a plumbing problem the Fed's own standing facilities (per `FED_AND_RATES.md`) exist to contain, not a signal this account's tools can observe or act on in time | Distinguishes "the market thinks a company might default" from "the banking system's cash plumbing seized up" when reading news about a market-wide sell-off |

**The honest summary:** every mechanism in this file is real, sourced, and
worth understanding to correctly interpret *why* a drawdown is happening —
whether it's credit-driven (2008, arguably faster and more informative),
rate/valuation-driven (2022, where credit spreads stayed calm), or an
exogenous shock (2020, where credit and equity moved together with no useful
lead time at all). None of it changes what R2 actually does, which is react
to price and moving averages after the fact. The value of this document is
the same as `HIDDEN_MARKET_DRIVERS.md`'s: giving an honest, checkable answer
to "is what's happening to the market credit-driven, funding-driven, or
something else" when a position gets stopped out during a broader selloff —
not a new input this account's mechanical rule should start watching.
