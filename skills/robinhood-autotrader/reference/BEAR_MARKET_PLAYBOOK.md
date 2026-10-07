# Bear Market Playbook — Surviving Hard Markets, Sourced

What actually happened, mechanically, to defensive strategies in real bear
markets — and what a small mechanical trend-following account can and cannot
do about it.

Last Updated: 2026-09-16 · Status: research reference, no new rule · Audience:
TARS, account owner (account #731951265)

## Overview

This document does not propose a new rule. `TARS_RULES.md` already runs one
mechanical response to bad markets — R2's 200-day/50-day trend filter, which
exits to cash when trend breaks — and `STRATEGY.md` has already *measured*
that response on real history: a monthly 12-1 momentum + 10-month-MA filter
sat in cash for 33 straight months through the 2000-2003 dot-com bust with
**0% drawdown versus QQQ's −74.6%** (`STRATEGY.md`, "Out-of-sample: the
dot-com bust"). That is the strongest evidence this repo has for anything, and
this document exists to check it against the outside academic and historical
record rather than repeat it — and to be honest about which other "bear
market" ideas people ask for (sector rotation into defensives, VIX products,
index put hedging) are real, measured, and available at this account's size,
versus real but institutional-only, versus not real at all.

The short version, stated up front because it is the conclusion everything
below supports: **this account's mechanical trend filter is a genuine,
literature-backed defense against catastrophic drawdown. It is not, and was
never claimed to be, a way to beat the market during a downturn.** Losing
less and beating the market are different claims with different evidence
behind them, and `STRATEGY.md` already scored its own strategy honestly on
exactly that distinction (see "Measured result, 2007-2026").

## 1. What actually happened in real bear markets

### The four regimes, mechanically

| Bear market | Index decline | Duration | Source |
|---|---|---|---|
| Dot-com bust | S&P 500 **−49%**, Nasdaq **−78%** (Mar 2000 → Oct 2002) | 31 months | [Black Swan Lab](https://theblackswanlab.com/crash/dotcom-2000) |
| 2008 GFC | S&P 500 **−57%** (Oct 2007 close 1,565.15 → Mar 2009 close 676.53) | 17 months | [Federal Reserve History, "The Great Recession"](https://www.federalreservehistory.org/essays/great-recession-of-200709) |
| 2020 COVID crash | S&P 500 **−34%** in 33 calendar days — the fastest bear market on record; recovered to new highs by August 2020 | 23 trading days down, 5 months to full recovery | [Finlume, "How Long the S&P 500 Takes to Recover"](https://finlume.net/en/blog/market-crash-recovery-time/) |
| 2022 rate-hike bear | S&P 500 **−25.4%** peak-to-trough (Jan 3 peak → Oct 12, 2022 trough); crossed the −20% bear-market line on Jun 13 | ~9 months | [Statista, "Bear Markets: How Deep Is Your Loss?"](https://www.statista.com/chart/27616/length-and-depth-of-the-latest-s-p-500-bear-markets/) |

Two mechanical patterns hold across all four, sourced independently for each:

**Defensive sectors held up, they did not go up.** In every one of these four
regimes, Utilities, Consumer Staples and Health Care lost less than the index
— never zero, never positive as a rule.

- *Dot-com bust:* Consumer staples returned **+11.2% annualized while the
  S&P 500 fell −22.3%**; utilities were broadly positive (Southern Company
  **+132%** through the whole 2000-2002 window; Duke Energy fell only
  **−36.1%** against the S&P's −49%).
  [Red Lotus Capital, "Sectors and Stocks That Gained During the Dot-Com Bust"](https://redlotuscapitals.medium.com/sectors-and-stocks-that-gained-during-the-dot-com-bust-8af2c64f1749)
- *2008 GFC:* financials fell over 55%, **consumer staples fell only ~15%**,
  utilities fell ~23-35% against tech benchmark drawdowns of 45-55%.
  [The InvestQuest, "Which stocks did the best during the 2008 Global Financial Crisis?"](https://theinvestquest.com/which-stocks-did-the-best-during-the-2008-global-financial-crisis/)
- *2020 COVID crash:* health care and consumer staples bottomed at ~72-76%
  of their Feb-19 level versus the index's overall −34%; utilities fell
  ~15-20%, but energy was hit *hardest* of any sector (−50 to −60%), and
  utility betas actually spiked above their historical defensive norm
  (network utilities' levered beta hit 1.11 during the selloff) — a reminder
  that "defensive" is a historical tendency, not a guarantee every cycle.
  [St. Louis Fed, "How COVID-19 Has Impacted Stock Performance by Industry"](https://www.stlouisfed.org/on-the-economy/2021/march/covid19-impacted-stock-performance-industry)
- *2022:* Utilities were the **second-best S&P 500 sector, +1.6%** for the
  year, Consumer Staples third-best; Communication Services was worst at
  **−39.9%** and Energy was, unusually, the best sector by a wide margin at
  **+65.7%** — a rate/inflation regime, not a recession, which flipped the
  usual "defensive vs. cyclical" script and put an economically-sensitive
  sector on top instead.
  [S&P Global, S&P 500 Sector Indices documentation](https://www.spglobal.com/spdji/en/documents/education/education-the-sp-500-sector-indices-the-blueprint-for-precision-analysis.pdf)

**The trend filter's actual mechanical record, independent of this account's
own backtest:** Meb Faber's widely-replicated 200-day/10-month SMA timing
model, and Jeremy Siegel's independent study of the same rule back to 1900 on
the Dow and since 1972 on the Nasdaq, both found the same shape of result:
roughly buy-and-hold-level long-run return, at **roughly half the maximum
drawdown**, achieved by sidestepping the worst of the decline rather than by
picking better assets. On the S&P 500 specifically, one widely-cited backtest
of the rule shows a **29% max drawdown versus 56% for buy-and-hold**, and
during 2008 the sell signal on a month-end 200-day rule triggered only about
6% below the peak — good, not perfect, timing.
[Faber, "A Quantitative Approach to Tactical Asset Allocation" (SSRN)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461) ·
[QuantSeeker, "What Works Below the 200-Day Moving Average?"](https://www.quantseeker.com/p/what-works-below-the-200-day-moving)

**This is the same shape of result `STRATEGY.md` already measured on this
account's exact rule** — 2008 −5.5% (SPY-only filter) / −13.1% (7-asset
rotation) versus the market's −52.2%; 2020 −7.9% / −5.3% versus −19.9%; 2022
−11.5% / −7.6% versus −20.9%. The outside literature and this repo's own
backtest agree: the mechanism is real, it is not new, and it is not unique to
this account's parameterization.

## 2. Sector rotation vs. trend-following vs. quality/low-vol — what the evidence actually favors

This is a live academic debate, not a settled one, and the three approaches
have different amounts of real evidence behind them.

**Trend-following / time-series momentum has the deepest and most consistent
record.** Moskowitz, Ooi & Pedersen's time-series momentum result — already
cited in `STRATEGY.md` — is the foundation. Independently, AQR's *century of
evidence* study on trend-following found it delivered positive average
returns with low correlation to stocks and bonds in **every decade since
1880**, through the Great Depression, multiple recessions, and 2008.
[Efficient Capital, "A Century of Evidence on Trend-Following Investing"](https://www.efficient.com/resources/a-century-of-evidence-on-trend-following-investing) ·
[AQR, "Understanding Managed Futures"](https://www.aqr.com/-/media/AQR/Documents/Insights/White-Papers/Understanding-Managed-Futures.pdf)
The 2008 instance is measured directly: the Barclay CTA Index, tracking
trend-following managed futures funds, returned **+14% in 2008** while most
asset classes collapsed — a real, dollar-measured "crisis alpha" year, a term
coined by Kaminsky and Mende (2011) for exactly this behavior.
[CTG, "Crisis Alpha"](https://cdn2.hubspot.net/hubfs/3107949/CTG%20Managed%20Futures%20PDFs%20and%20Ebooks/CTG%20Crisis%20Alpha.pdf)

**Business-cycle sector rotation has much weaker real evidence than its
popularity suggests.** A 2024 peer-reviewed study bluntly titled "The myth of
business cycle sector rotation" found that only **25% of tested sector
rotation strategies beat buy-and-hold before costs, and only 17% after
transaction costs** — average monthly return of 0.86% against 0.89% for
buy-and-hold, i.e. rotation underperformed on average even net of nothing.
The paper's own framing: even assuming *perfect foreknowledge* of which
business-cycle phase the economy is in, the edge is only marginal.
[Molchanov & Stangl, "The Myth of Sector Rotation," *International Journal of Finance & Economics* (2024)](https://onlinelibrary.wiley.com/doi/full/10.1002/ijfe.2882)
`SECTOR_ANALYSIS.md` already takes the correct, more modest position on this
in this repo — sector cycle color sharpens catalyst research, it is
explicitly *not* a signal R2 acts on — and this finding is why that
restraint is the right call, not an arbitrary one.

**Quality and low-volatility investing have real, separately-documented
drawdown benefits, with a different mechanism than trend-following.**
Asness, Frazzini & Pedersen's "Quality Minus Junk" documents that safe,
profitable, well-managed companies earn persistently higher risk-adjusted
returns in **23 of 24 countries studied**, and the effect is not explained
away by size or value.
[Asness, Frazzini & Pedersen, "Quality Minus Junk" (AQR/SSRN)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2312432)
The low-volatility anomaly shows a similar shape: low-vol portfolios
typically capture **90-95% of market return at 60-70% of market risk**, with
dramatically smaller drawdowns, at the cost of underperforming badly during
sharp speculative rebounds off a bottom — the mirror image of trend
following's own known failure mode (whipsaw on a fast V-shaped recovery).
[Wikipedia, "Low-volatility anomaly," summarizing Ang et al.](https://en.wikipedia.org/wiki/Low-volatility_anomaly)

**The honest ranking, sourced:** trend-following (time-series momentum) has
the longest, most consistently replicated record specifically *for surviving
drawdowns*, sector rotation's real-world edge is thin to negative once costs
and imperfect timing are included, and quality/low-vol are real but solve a
related, not identical, problem (return per unit of risk generally, not
specifically "exit before a crash"). This is exactly the ordering
`STRATEGY.md`'s own five-strategy horse race already found for *this*
account's universe — momentum beat reversion, low-vol, vol-weight and
equal-weight on both CAGR and return/drawdown, in both the ETF and
single-stock tests (`STRATEGY.md`, "Alternatives, measured in advance").
Outside literature and this repo's own measurement point the same way.

## 3. What a small account can and cannot actually do

`TARS_RULES.md` runs a cash-constrained, no-margin, no-options-yet account
(R9 locks options until $2,000 equity and 20 closed trades; R1 excludes
shorting and crypto entirely). Bear-market defense ideas split cleanly by
whether they need capital or infrastructure this account does not have.

**What this account can actually do, and already does:**

- **Move to cash/defensive assets via a trend rule.** This is R2 in its
  equity-only form today, and the full `STRATEGY.md` plan (equities + TLT/GLD/
  BIL rotation) if funded later. No margin, no shorting, no options required
  — this is the one bear-market technique in this whole document that is
  both well-evidenced *and* fully available at this account's actual size,
  which is why it is the one already running.
- **Reduce position count / raise cash floor mechanically.** R3's 15% cash
  floor and R6's circuit breakers (2 stop-outs in 5 days → 3-day new-entry
  freeze; −15% from high-water mark → halt all new entries) are small-account-
  native risk controls — no options or margin needed, and they do real work:
  the whole point of a cash floor is that it cannot go to zero from a losing
  streak alone.

**What this account cannot meaningfully do, and why — stated honestly rather
than as a flat no:**

- **Shorting to profit from or hedge a decline.** R1 excludes it outright;
  `live-mcp-architecture.md` already notes fading a hot IPO "needs shorting a
  cash account can't do." Not available here at any size without switching
  account type.
- **Index put protection, sized correctly.** `options.md`'s floor test
  (already documented in `live-mcp-architecture.md`) shows the real
  constraint isn't strategy quality, it's arithmetic: max sane premium is
  `(account value − floor) × fraction staked on one binary`, which on this
  account's numbers landed near **$23** while a single contract with a real
  delta cost **$105** — the position that would actually hedge something is
  larger than the entire headroom available to buy it. This is not a defect
  in the idea, it is what "small account" means quantitatively.
- **A protective put against a fractional share position is not a hedge at
  all** — already flagged in `live-mcp-architecture.md`: it hedges roughly
  90x the stock actually owned, i.e. it is a naked directional bet wearing a
  hedge's name. R9, once open, only takes options on names this system
  already holds as full equity positions for exactly this reason.
- **VIX products (VXX, UVXY and similar) as a bear-market hedge.** These are
  structurally unsuited to holding through a bear market at all, for any
  account size, small or large: VIX futures are normally in contango, so
  long VIX ETPs bleed value on every roll, independent of what volatility
  actually does. VXX is down **98% since its 2009 inception** while the VIX
  index itself is down only ~65% over the same period — the product decays
  even when its underlying doesn't. This is why one live-account episode
  already caught a "disorder hedge" candidate that was actually a
  short-volatility asset with a **−0.167 correlation to a VIX proxy** —
  the opposite of a hedge (`live-mcp-architecture.md`, "A candidate was
  proposed as a disorder hedge").
  [tastytrade, "What is VXX & How to Trade it?"](https://tastytrade.com/learn/trading-products/stocks/what-is-VXX-how-to-trade-it/) ·
  [Seeking Alpha, "VXX: A Behind The Scenes Look Inside The Volatility Index ETN"](https://seekingalpha.com/article/4816107-vxx-behind-scenes-look-inside-volatility-index-etn)
- **Index puts as a standing, always-on hedge (available capital aside).**
  Even institutions that can afford the premium pay a real, measured, long-run
  drag for this: an 8-year study of a 5%-OTM put-protected 60/40 portfolio
  returned **7.0% versus 9.0%** unprotected — almost the entire cost of the
  insurance is never recovered, because index implied volatility persistently
  exceeds what actually gets realized (the "volatility risk premium").
  [AQR, "Chasing Your Own Tail (Risk), Revisited"](https://www.aqr.com/-/media/AQR/Documents/Insights/White-Papers/AQR-Chasing-Your-Own-Tail-Risk-Revisited.pdf?sc_lang=en)
  So this is not merely a small-account gap to grow out of — a funded
  options book (once R9 opens) should treat "buy puts and hold them" as a
  persistent tax, not a strategy, and reach for the trend filter's
  already-measured cash-rotation instead of a standing put position.

**Bottom line on this section:** the one bear-market technique with real
evidence *and* real availability at this account's size is the trend filter
this account already runs. Everything else people ask for by name (shorting,
index puts, VIX products) is either unavailable here specifically, or
measurably not worth its cost at any account size.

## 4. "Beating the market" vs. "losing less" — these are different claims

Bill Sharpe's foundational point about active management is arithmetic, not
opinion: since passive investors collectively hold the market portfolio,
active investors collectively must hold the rest of it, so before costs the
two groups earn the same average return — active management is a
zero-sum game against itself, and after costs the average active investor
must underperform the average passive one.
[Semantic Scholar, Sharpe, "The Arithmetic of Active Management"](https://www.semanticscholar.org/paper/The-Arithmetic-of-Active-Management-Sharpe/a169b7b18d3d8e21dd35495508ad0bfd34c46754)
Alpha — return above what the market's own risk (beta) would predict — and
"lower beta / lower drawdown" are different axes entirely. A strategy can
score zero or negative on the first and strongly positive on the second, and
that is not a lesser achievement, it is a different, independently valuable
one.

**Why lower drawdown matters on its own, independent of return:** the
arithmetic of loss recovery is asymmetric. A 20% loss needs a 25% gain to get
back to even; a 50% loss needs a 100% gain; a 75% loss (close to the Nasdaq's
actual dot-com drawdown) needs a 300% gain. The math is `L / (1 − L)`, and it
gets punishing fast, which is exactly why a strategy that caps drawdown at
−16% instead of −52% is protecting something real even at a lower CAGR.
[Journalplus, "Drawdown Recovery Calculator"](https://journalplus.co/tools/drawdown-recovery-calculator/)

**The tension worth naming honestly: doesn't "time in the market" research
argue against any kind of exiting?** JPMorgan's widely-cited study found that
missing just the 10 best days in the S&P 500 over 2005-2024 cut a
buy-and-hold investor's annualized return from **10.4% to 6.1%** — and 7 of
the 10 best days fell within two weeks of one of the 10 worst days, meaning a
scared exit during a crash routinely also forfeits the sharpest part of the
rebound.
[J.P. Morgan, "Back to School: 3 Principles for Your Portfolio"](https://www.jpmorgan.com/insights/markets/top-market-takeaways/tmt-back-to-school-3-principles-for-your-portfolio)
Separately, DALBAR's annual behavior study has found the average equity
investor has underperformed the S&P 500 for **15 straight years** (through
2024), driven by exactly this pattern — panic-selling into weakness,
chasing strength back in late.
[DALBAR, "Investors Missed the Best of 2024's Market Gains"](https://www.dalbar.com/press-release/investors-missed-the-best-of-2024s-market-gains-latest-dalbar-investor-behavior-report-finds/)

These two bodies of evidence are not actually in conflict with R2, and the
reconciliation matters: DALBAR and the "missing the best days" research
measure *discretionary, emotional* timing — selling on fear, buying back on
confidence, with no rule fixing the re-entry point in advance. R2 is a
pre-committed mechanical rule that also gives back some of the recovery —
`STRATEGY.md` says so plainly, quantifying that the dot-com filter's 33-month
cash stretch cost roughly 35% of the eventual rebound by re-entering late.
The difference is that this cost was **known and accepted before the fact**,
not discovered by a panicked investor after the fact, and the rule that pays
it is the same rule that avoided the −74.6% in the first place. A mechanical
rule that gives back part of a rebound is not the failure DALBAR describes;
an investor with no rule at all who freezes at the bottom and buys back
after the recovery is already priced in, is.

**What a mechanical trend-following account is realistically capable of, and
not:** it is capable of, and has already delivered on paper, materially
smaller peak-to-trough losses during real historical declines. It is not
capable of forecasting a top, calling a bottom, or reliably beating a rising
market — `STRATEGY.md`'s own pre-registration says exactly this ("not
expected to beat SPY on raw return"), and its measured 2007-2026 result
confirms it lost by 2.93 points of annual return doing so. The correct frame
for this account in a hard market is not "did it make money" but "did the
loss stay inside the range the rule was built to cap" — which is precisely
what R4's −8% hard stop, R6's −15%-from-high-water-mark halt, and R2's trend
gate are for, and precisely what `STRATEGY.md`'s falsification condition
("the absolute filter fails to reduce drawdown during an actual 15%+ decline")
would test if one arrives.

## Connecting back to this account

Nothing above changes R1-R12. What it adds:

- **R2 is already the evidence-backed choice.** Section 2's literature
  ranking (trend-following > sector rotation > buy weakness) matches
  `STRATEGY.md`'s own five-strategy backtest exactly, and R2's hard gate
  against buying below the 200-day MA is that same finding turned into a
  rule (`TARS_RULES.md` R2 already cites this connection explicitly). This
  document adds outside confirmation, not a new argument.
- **Section 3 is why R9's option gate stays where it is.** The floor-test
  arithmetic that already blocks a standing hedge on this account
  (`live-mcp-architecture.md`) is reinforced, not contradicted, by the
  outside research on put-buying drag (AQR) and VIX-ETP decay (tastytrade/
  Seeking Alpha): even a fully-funded account should not run a standing put
  hedge or hold a VIX product through a downturn. If R9 ever opens and a
  bear-market hedge is requested, the answer is still "size against the
  floor, on a name this system already holds" — not a new instrument class.
- **Section 4 is the standard against which a real drawdown should be
  judged.** If a hard market arrives while this account is live, the right
  question is not "did TARS beat SPY" — it was never supposed to, and
  `STRATEGY.md` already says so — it is whether realized drawdown stayed
  under R6's −15% halt line and R2's filter actually reduced loss versus
  staying invested, which is `STRATEGY.md`'s own falsification test. Score
  it against that, not against the index's return.
- **No sector-rotation override belongs in R2.** Section 2's sourced finding
  that business-cycle rotation barely beats buy-and-hold before costs (and
  loses to it after) is a reason *not* to add a sector-timing layer on top
  of the trend filter, matching `SECTOR_ANALYSIS.md`'s existing position that
  sector cycle color sharpens catalyst research but is not itself a signal.
