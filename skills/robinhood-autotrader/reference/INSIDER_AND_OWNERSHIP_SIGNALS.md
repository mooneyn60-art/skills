# Insider Trading & Institutional Ownership Signals — Reading Form 4, 13F, and Short Interest

Sourced research on what corporate insiders' trades (Form 4 / Section 16),
institutional managers' quarterly holdings (13F), and short interest actually
tell you — the real academic findings on the buy/sell asymmetry, why 10b5-1
plans mute a specific sale's information content, why "cloning" 13F picks is
mostly a mirage once the 45-day lag and costs are counted, and an honest line
between useful context and a new mechanical rule.

Last Updated: 2026-09-16 · Status: active · Audience: TARS, and anyone reading
over its shoulder

## Overview

This account's own research already surfaced a Form 4 headline in passing —
an Ovintiv (OVV) insider disclosed a stock sale while OVV was being
researched as a sector-diversification candidate — without ever pausing to
explain what that class of disclosure is actually worth. That is the real
gap this file closes. `FUNDAMENTAL_ANALYSIS.md` already covers how to read
the *company* (statements, earnings quality, moats). This file covers a
different question: what do the *people who run the company* and the
*investors who hold large stakes in it* appear to be doing with their own
capital, and how much of that is signal versus noise once you understand the
mechanics of how and when it's disclosed. Short answer, argued in full below:
insider **selling** is common and mostly uninformative; insider **buying**,
especially clustered buying by multiple insiders, is the more reliable
direction; 13F filings are real but stale by design; and none of this
produces a new rule for a mechanical technical system — it's a context check,
the same role `options.md`'s research protocol already gives analyst targets
and earnings dates.

---

## 1. Form 4 / Section 16 — who has to tell you, how fast, and what it leaves out

**Who files.** Section 16(a) of the Securities Exchange Act of 1934 requires
three groups — a company's **officers**, its **directors**, and any
**beneficial owner of more than 10%** of a registered class of its equity
securities — to report their transactions in that company's stock. These are
collectively "Section 16 insiders" or "reporting persons."
[SEC: Updated Investor Bulletin — Insider Transactions and Forms 3, 4, and 5](https://www.sec.gov/resources-for-investors/investor-alerts-bulletins/updated-investor-bulletin-insider-transactions-forms-3-4-5-0)

**The three forms:**
- **Form 3** — initial statement of beneficial ownership, filed within **10
  days** of becoming an officer, director, or >10% owner (or, for a newly
  public company, at the time of the IPO).
- **Form 4** — the one that actually matters day to day: reports a change in
  beneficial ownership (any purchase, sale, option exercise, grant, or
  gift), and must be filed within **two business days** of the transaction
  date — not the settlement date.
- **Form 5** — an annual catch-all for anything that should have been on a
  Form 4 but was eligible for deferred reporting (mainly small gifts and a
  few exempt transaction types), due within 45 days of fiscal year-end.

[SEC: Updated Investor Bulletin — Insider Transactions and Forms 3, 4, and 5](https://www.sec.gov/resources-for-investors/investor-alerts-bulletins/updated-investor-bulletin-insider-transactions-forms-3-4-5-0)

All three are filed electronically on EDGAR and are public within minutes of
filing — this is one of the fastest-disclosed data sets in all of securities
law, in sharp contrast to the 13F lag covered in §3.

**What a Form 4 does NOT tell you:**
- **Why.** The form reports the transaction, the price, and the resulting
  ownership — never a reason. That reason has to be inferred (see §2 on
  10b5-1 plans, which is the single biggest source of "sales that mean
  nothing").
- **Conviction relative to net worth.** A CEO selling 5,000 shares out of 2
  million held is a rounding error; the same 5,000-share sale by a small
  company's newly appointed VP could be most of their liquid net worth. The
  form gives you the share count and the resulting position, not the
  person's full balance sheet, so scale the transaction against the
  **remaining stake**, not just the trade size.
- **Anything about non-officers/directors/10%-owners.** A key scientist, a
  star trader, or a senior-but-not-"officer" employee with real inside
  knowledge files nothing at all under Section 16.

## 2. Why insider BUYING is the stronger signal, and selling mostly isn't

The foundational academic study here is **Lakonishok and Lee (2001), "Are
Insider Trades Informative?"** (*Review of Financial Studies*), which
analyzed essentially the full universe of insider transactions reported to
the SEC on the NYSE, AMEX, and Nasdaq from **1975 to 1995**.
[Lakonishok & Lee — paper PDF](https://www.lsvasset.com/pdf/research-papers/Insider-Trades-Informative.pdf) ·
[secondary summary with figures](https://www.insidermonkey.com/blog/insider-trading-returns-calculated-by-josef-lakonishok-and-inmoo-lee-546/)

Their central, and most-replicated, finding is an **asymmetry**: firms with
heavy insider **buying** subsequently outperformed firms with heavy insider
**selling** by **7.8%** over the following 12 months (narrowing to **4.8%**
once size and book-to-market are controlled for, since insider purchases
skew toward smaller, higher book-to-market firms and insider sales skew
toward larger, richer-valued ones). Insider **purchases carried real,
statistically significant predictive power**; insider **sales, in
aggregate, did not reliably predict underperformance at all**. The paper
also found insider trading was **more informative in smaller-cap names**
than in large caps, where far more shares are in institutional and index
hands and any one insider's information edge is diluted.

**Why the asymmetry exists — the mechanism, not just the statistic.** An
insider can sell for dozens of reasons that have nothing to do with a view
on the company: diversification (most of their net worth is already
concentrated in one stock), funding a home purchase or tax bill, exercising
options that are about to expire, estate planning, a pre-scheduled 10b5-1
plan set up months earlier (§2 below), or simply portfolio rebalancing.
**There is essentially only one reason to buy stock with personal, already-
taxed cash on the open market: the belief that it will go up.** This
"many reasons to sell, one reason to buy" framing is an old Wall Street
adage — one of its earliest traceable appearances in print is a March 1991
*Los Angeles Times* line ("There are a number of good reasons to sell stock.
But there is only one reason to buy stock. You think it will go up.") — that
the Lakonishok-Lee data gave real statistical backing to.
[Etymology/citation of the "many reasons to sell" line](https://barrypopik.com/index.php/new_york_city/entry/there_are_many_possible_reasons_to_sell_a_stock_but_only_one_reason_to_buy)

**Cluster buying — multiple insiders buying at once — is a stronger signal
than any one insider buying alone.** Two later, more targeted studies extend
Lakonishok-Lee specifically on this point:

- **Kang, Kim & Wang, "Cluster Trading of Corporate Insiders"** (analyzing
  U.S. insider transactions from 1986–2016) found that cluster purchases —
  multiple insiders at the same firm buying within a short window of each
  other — produced abnormal returns of roughly **3.8% over the next 21
  trading days versus ~2% for non-cluster (solitary) purchases**, with the
  gap widening to about **2.5 percentage points at a 90-day horizon**.
  Cluster buys also showed a stronger market reaction on disclosure than
  solitary buys, consistent with the market itself treating clustering as
  higher-quality information.
  [Kang, Kim & Wang — paper PDF](https://opis-cdn.tinkoffjournal.ru/mercury/insider-pdf-002.pdf) ·
  [secondary summary](https://www.2iqresearch.com/blog/what-is-cluster-buying-and-why-is-it-such-a-powerful-insider-signal)
- **Alldredge et al., "Do Insiders Cluster Trades with Colleagues? Evidence
  from Daily Insider Trading"** (*Journal of Financial Research*, 2019)
  found insiders do systematically cluster their trades around colleagues'
  trades, more so when information asymmetry is high, and that purchases
  made within roughly two days of a peer insider's purchase earned
  abnormal returns of about **2.1% over the following month — meaningfully
  higher than solitary purchases**.
  [Alldredge et al. — Journal of Financial Research (Wiley)](https://onlinelibrary.wiley.com/doi/10.1111/jfir.12172) ·
  [secondary summary with figures](https://www.2iqresearch.com/blog/what-is-cluster-buying-and-why-is-it-such-a-powerful-insider-signal)

**Could not verify / left out:** several blog aggregators quote a standalone
"insider buys in small-caps delivered 7.4% abnormal returns over 12 months"
figure attributed to Lakonishok-Lee; that specific number could not be
traced back to the original paper (paywalled/garbled PDF) with confidence,
so it's omitted here in favor of the paper's own headline 7.8%/4.8% figures,
which multiple independent secondary sources agree on.

## 3. 10b5-1 plans — why a specific sale might mean nothing at all

**Rule 10b5-1**, adopted by the SEC in 2000, gives insiders an affirmative
legal defense against insider-trading liability if they trade under a plan
that was set up **in advance**, while they did **not** possess material
non-public information, specifying (or using a formula to determine) the
amount, price, and timing of future trades — which then execute
automatically, months later, regardless of what the insider knows or
believes at the moment of execution.
[Harvard Law School Forum on Corporate Governance — Rule 10b5-1 Plans: What You Need to Know](https://corpgov.law.harvard.edu/2013/02/05/rule-10b5-1-plans-what-you-need-to-know/)

**Why this matters for reading a Form 4:** a sale executed under a 10b5-1
plan adopted six months ago has, by construction, **no connection to
whatever is happening at the company today** — it was scheduled before
today's news existed. Treating a 10b5-1 sale the same as an open-market,
discretionary sale made *this week* is exactly the mistake this file exists
to prevent: it conflates a pre-committed liquidity/diversification
transaction with a fresh, information-driven decision.

**The SEC tightened this in December 2022** specifically because 10b5-1
plans were being used opportunistically (adopted and then traded almost
immediately, or cancelled/modified around bad news). The amendments, in
effect for Section 16 filings since April 2023:
- Impose a **cooling-off period** between plan adoption/modification and the
  first trade: for **directors and officers**, the *later* of 90 days after
  adoption or two business days after the issuer's next 10-Q/10-K covering
  the quarter of adoption is filed (capped at 120 days); for other insiders,
  a flat **30 days**.
- Require the insider to certify, at adoption, that they are **not aware of
  material non-public information** and are acting in **good faith**.
- Added a **mandatory checkbox on Forms 4 and 5** where the filer must
  affirmatively indicate the transaction was made under a 10b5-1 plan, and
  disclose the plan's **adoption date**.

[SEC Press Release — Amendments to Modernize Rule 10b5-1](https://www.sec.gov/newsroom/press-releases/2022-222) ·
[Skadden summary of the amendments](https://www.skadden.com/insights/publications/2022/12/sec-amends-rules-for-rule-10b51-trading-plans-and-adds-new-disclosure-requirement)

**How to actually tell a 10b5-1 sale apart from an opportunistic one, in the
filing itself:** check that checkbox and the disclosed adoption date. If the
box is checked and the plan was adopted well before the current news cycle
(months, ideally with the 90/120-day cooling-off period already elapsed),
the sale is close to pure noise for research purposes — it says nothing
about the insider's view today. If the box is **unchecked**, the transaction
was discretionary and made in the open market with (presumably) current
information in hand, which is a materially different — and more
informative, especially if it's a purchase — signal than a scheduled sale.

**Honest caveat on how much the checkbox actually fixes:** research
comparing plan and non-plan sales still finds evidence of **opportunistic
timing even inside 10b5-1 plans** — insiders can choose *when* to adopt a
plan, choose parameters that front-load favorable-looking trades, or
selectively modify/cancel plans — so "10b5-1 checked" should be read as
"materially less informative," not "fully explained away." One study
following the 2022 amendments found **sell-side informativeness measurably
weaker post-reform** than before it, consistent with the reform doing at
least part of its intended job.
[ScienceDirect — When and how are Rule 10b5-1 plans used for insider stock sales?](https://www.sciencedirect.com/science/article/abs/pii/S0304405X23000697)

## 4. 13F filings — what they are, why they're stale, and whether "cloning" them works

**What a 13F actually is.** Any institutional investment manager exercising
investment discretion over **$100 million or more** in "Section 13(f)
securities" (most exchange-listed U.S. equities, plus certain equity
options/ADRs/convertibles) must file Form 13F, disclosing its **long**
equity positions, quarterly, with the SEC.
[SEC — Frequently Asked Questions About Form 13F](https://www.sec.gov/rules-regulations/staff-guidance/division-investment-management-frequently-asked-questions/frequently-asked-questions-about-form-13f) ·
[Investor.gov — Form 13F glossary entry](https://www.investor.gov/introduction-investing/investing-basics/glossary/form-13f-reports-filed-institutional-investment)

**The real staleness problem.** Each 13F is due **within 45 days of quarter-
end** — so a Q2 (June 30) filing isn't public until roughly mid-August. A
position shown in that filing reflects a snapshot from **up to 6.5 weeks
earlier**, and the manager is under no obligation to still hold it, or to
still hold it at the same size, by the time anyone reads the filing — it
could already be fully closed out. This is the single biggest reason 13F
data is a lagging, not a live, indicator.
[Finrep — SEC Form 13F Filing Deadline: The 45-Day Rule Explained](https://www.finrep.ai/blog/sec-form-13f-filing-deadline-the-45-day-rule-explained-2026)

**What it structurally leaves out**, independent of the lag:
- **Only long positions.** Short positions are explicitly excluded — a
  manager may not net a short against a long in the same name — so a fund
  that is long $10B and short $9B (net exposure ~$1B) reports the same long
  book as a fund that is long $10B and short nothing (net exposure $10B).
  [SEC 13F FAQ — long positions only, no netting of shorts](https://www.sec.gov/rules-regulations/staff-guidance/division-investment-management-frequently-asked-questions/frequently-asked-questions-about-form-13f)
- **U.S.-listed equities only** — foreign-listed holdings, cash, bonds, and
  most derivatives beyond listed options don't appear.
- A manager can request **confidential treatment** to delay disclosure of
  specific positions it's still building, and can later **restate** prior
  filings — both of which further blur the "what do they actually hold
  right now" picture.

**Does "cloning" 13F picks actually work, net of staleness and costs?**
The honest answer from the peer-reviewed literature is **mixed to
skeptical**, not a clean yes:

- **Griffin & Xu, "How Smart Are the Smart Guys? A Unique View from Hedge
  Fund Stock Holdings"** (*Review of Financial Studies*, 2009) — using
  ~300 hedge funds' quarterly 13F-sourced holdings from 1980–2004, found
  hedge funds outperformed mutual funds' stock-picking by only about
  **1.3–1.4 percentage points a year before fees**, that most of even this
  small edge came from just two years (1999–2000) and was **not
  statistically significant** once those years were excluded, that hedge
  funds showed **no sector-timing or style-picking skill**, and — the
  finding most relevant here — that **aggregate hedge fund holdings did not
  predict the cross-section of future stock returns**. This is a
  peer-reviewed, widely cited result and the most direct evidence that,
  net of the disclosure lag, 13F-based hedge fund long books are not the
  gold mine retail "13F cloning" content often implies.
  [Griffin & Xu — SSRN abstract](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=924242) ·
  [Oxford Academic — Review of Financial Studies](https://academic.oup.com/rfs/article-abstract/22/7/2531/1601313)
- **Verbeek & Wang, "Better than the Original? The Relative Success of
  Copycat Funds"** (*Journal of Banking & Finance*, 2013) is more
  favorable in a narrower sense: copycat portfolios that mechanically
  replicate a mutual fund's *disclosed* holdings can match or modestly beat
  their target fund net of estimated trading costs, and copying **past
  winners specifically** can beat most mutual funds — but this study used
  mutual funds' (not hedge funds') disclosed holdings, a different (often
  shorter) disclosure lag than 13F's 45 days, and still found **wide
  dispersion** in copycat success — it is not evidence that copying a
  random well-known 13F filer's stale quarterly picks reliably works.
  [Verbeek & Wang — SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1566794) ·
  [ScienceDirect — Journal of Banking & Finance](https://www.sciencedirect.com/science/article/abs/pii/S0378426613002070)

**Could not verify / left out:** a widely-circulated SSRN working paper
claims cloned 13F portfolios beat the S&P 500 by "24.3% annualized,
risk-adjusted" across 150,000+ portfolios (2013–2023). It is a single,
not-yet-peer-reviewed working paper with a strikingly large claimed edge,
and independent replication could not be found — it is omitted here rather
than repeated as established fact. Take the Griffin & Xu and Verbeek & Wang
peer-reviewed results as the load-bearing evidence instead: 13F cloning is,
at best, a costly, noisy, highly manager-specific strategy — not a reliable
edge for a retail account trading 45-day-old information with real
transaction costs and no ability to see the short book.

## 5. Short interest — the related, but distinct, disclosure signal

`MARKET_MECHANICS.md` §5 already covers the mechanics of short selling and
short squeezes qualitatively (borrow shares, sell, buy back cheaper; a
squeeze is forced covering feeding on itself). This section adds the
**disclosure mechanics and data** underneath that explanation, without
repeating it.

**How short interest is actually reported.** In the U.S., FINRA requires
member firms to report aggregate short positions in every equity security
**twice a month** — as of mid-month (the 15th, or the prior business day if
the 15th isn't a settlement date) and as of month-end. Firms have until
**6:00 p.m. ET on the second business day** after the settlement date to
report, and FINRA disseminates the compiled figures several trading days
later — so even "current" published short interest is typically **a week
or more old** by the time it's public, an important companion fact to the
13F lag above.
[FINRA — Short Interest Reporting](https://www.finra.org/filing-reporting/regulatory-filing-systems/short-interest)

**Days-to-cover** (also called the "short interest ratio") is the reported
short position divided by the stock's average daily trading volume — an
estimate of how many trading days it would take short sellers to
collectively buy back every borrowed share at typical volume. It is a
liquidity/crowding measure, not a timing signal by itself: a stock can sit
at a high days-to-cover for a long time with no squeeze if nothing forces
covering.
[Strasmore — When Is Short Interest Released?](https://www.strasmore.com/blog/when-is-short-interest-released)

**Short interest as % of float** (rather than % of shares outstanding) is
the more meaningful crowding measure, since float excludes insider- and
strategically-locked shares that can never actually be lent out to short
sellers — the same float concept `MARKET_MECHANICS.md` uses elsewhere for
index-weighting and liquidity discussions.

**A forthcoming, complementary disclosure regime:** the SEC adopted **Rule
13f-2 / Form SHO** in October 2023, which will require large institutional
short sellers (those with gross short positions ≥$10M, or ≥2.5% of a
reporting company's outstanding shares, in a given month) to report their
own short positions directly to the SEC — the short-side mirror of the long-
only 13F described in §3. As of this writing the SEC has granted a
**multi-year compliance extension**, pushing the first required filings out
to **February 2028**, so this data source is not yet live; worth knowing it
exists and is coming, not something to rely on today.
[Ropes & Gray — SEC Adopts New Reporting Regime for Short Sales](https://www.ropesgray.com/en/insights/alerts/2023/10/sec-adopts-new-reporting-regime-for-short-sales) ·
[Note on the 2025 compliance-date extension to Feb 2028](https://natlawreview.com/article/sec-rule-13f-2-and-form-sho-new-short-position-reporting-requirements-certain)

**Could not verify / left out:** GameStop's January 2021 short interest is
widely cited in press coverage at figures ranging from roughly 120% to well
over 140% of float, and "days to cover" figures circulated even higher
because reported short interest can exceed 100% of float when the same lent
shares are re-borrowed and re-shorted multiple times. The SEC's own October
2021 staff report on the episode ("Staff Report on Equity and Options Market
Structure Conditions in Early 2021") is the authoritative primary source,
but its exact figures could not be reliably extracted here from the source
PDF, so no specific number is asserted for GameStop in this file — the
mechanism (extreme short interest + low float + forced covering = feedback
loop) is the durable, well-sourced takeaway, not any single headline
percentage.
[SEC Staff Report on Equity and Options Market Structure Conditions in Early 2021](https://www.sec.gov/files/staff-report-equity-options-market-struction-conditions-early-2021.pdf)

---

## 6. Honest actionability for this account — context, not a new rule

**R2 is pure price/moving-average technical, with no discretion, and that
should not change here.** Everything in this file — Form 4 direction and
clustering, whether a sale is 10b5-1-scheduled or opportunistic, a fund's
stale 13F position, a stock's short interest and days-to-cover — is a
fundamentally **discretionary, qualitative** signal. None of it is a price
or moving-average condition, none of it has a clean, replicable mechanical
trigger threshold, and bolting any of it onto R2 as an automated buy/sell
condition would break the "pure trend, no discretion" property that makes
R2 auditable in the first place. **Do not build an automated rule out of
any of this.**

Where it *is* legitimately useful is exactly the role `FUNDAMENTAL_ANALYSIS.md`
already carved out, and the same role `options.md`'s §0 research protocol
already gives analyst price targets and the earnings calendar: **one more
context check when researching a specific catalyst or sizing conviction on
a discretionary options or diversification pick that already passed R2 or
the sector screen.** Concretely, when a name is already on the table for
research (a scan hit, an analyst-upgrade headline, a sector-diversification
candidate like OVV was):

- Pull recent Form 4s. A cluster of **open-market purchases** (checkbox
  unticked, multiple insiders, recent) modestly *raises* conviction on a
  bullish thesis already built from price action and the catalyst check —
  it never substitutes for either. A single insider **sale** — especially
  one with the 10b5-1 box checked — should usually be read as close to
  **no signal at all**, not a red flag, and is not, on its own, a reason to
  avoid or exit a position.
  This is the direct fix for the OVV gap that motivated this file: an
  insider sale headline surfacing in research is a data point almost
  never worth acting on by itself, and should be labeled as such in the
  written thesis rather than left unexplained.
- Check whether large, well-known institutional holders' most recent 13F
  shows them adding or trimming the name — as directional color on how
  "smart money" was positioned **6+ weeks ago**, not a live signal, and
  never a reason to buy or sell on its own given the Griffin & Xu / Verbeek
  & Wang evidence above.
- Check short interest and days-to-cover as one more input into whether a
  sharp move has room to keep running (a heavily-shorted name squeezing) or
  is already crowded and vulnerable to unwind — again, context for sizing
  and stop placement on a trade R2 or the options protocol already
  produced, never the reason for the trade itself.

Log any of this the same way `options.md` §0's step 8 already logs
research: as thesis-strengthening or thesis-weakening **context**, dated
and sourced, so a future session can see it was actually checked rather than
mentioned in passing and dropped, the way the OVV Form 4 line was.

## Cross-references

- `MARKET_MECHANICS.md` §5 — the short-selling and short-squeeze mechanics
  this file's §5 adds disclosure data and sourcing underneath.
- `FUNDAMENTAL_ANALYSIS.md` — reading the company itself (statements,
  earnings quality, moats); this file reads what insiders and large holders
  are *doing*, a related but distinct question.
- `options.md` §0 — the research protocol this file's §6 slots into as one
  more context check, not a new gate.
- `HIDDEN_MARKET_DRIVERS.md` — other non-price-action mechanical drivers
  (gamma hedging, index-reconstitution flows, buyback blackouts) that, like
  this file, are explanatory context rather than new R2 signals.
