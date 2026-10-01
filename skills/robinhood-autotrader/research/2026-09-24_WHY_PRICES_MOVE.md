# Why Prices Move on a Given Day: Market, Sector, or Company?

One-line: RESEARCH_AGENDA item 16. Split each held name's daily moves into
the part explained by the whole market (SPY), the part added by its sector,
and the part that is company-specific. Then check how often a big
company-specific move has a company filing behind it.

Last Updated: 2026-09-24
Status: DONE. Prediction committed first (de6a33e); about half of it was wrong.
Audience: Nolan, TARS sessions

## Names and data

The book as the agenda and notes name it: NVDA, INTC (sector: SMH,
semiconductors), SOFI, NWG (XLF, financials), CVE (XLE, energy), ABBV
(XLV, health care), EXEL (XBI, biotech). Market: SPY. Daily closes,
adjusted, 3 years to 2026-09, Yahoo Finance chart API.

"News" proxy: SEC EDGAR filings (8-K for US filers, 6-K for foreign filers
NWG and CVE; any item) dated on the move day or the trading day before.
This is a floor on news: analyst notes, press stories and sector news that
never becomes a filing are missed.

## Method (fixed before the run)

For each name: regress the daily return on SPY -> R-squared = market share.
Regress on SPY + sector ETF -> the increase = sector share. 1 - the second
R-squared = company-specific share. Large moves = days where the
company-specific residual is beyond 3 standard deviations. Report the share
of those with a filing on day 0 or day -1, against the base rate (the share
of ALL days with such a filing).

## PREDICTION

- Market share of daily variance: 25-45% for the large caps (NVDA, INTC,
  ABBV), lower (15-30%) for SOFI, NWG, CVE, EXEL.
- Sector adds 5-15 points.
- Company-specific: 45-65% for large caps, 60-75% for the others.
- Large company-specific moves (>3 sd): 40-60% have a filing on day 0/-1,
  against a base rate of about 5-10% of all days.

## Answer first

There is no single answer. It depends heavily on the name:
- EXEL, NWG, INTC, SOFI, ABBV: 61-88% of the daily variance is
  company-specific. On a typical day, what the company does matters more
  than what the market does.
- NVDA: the market (45%) and the semiconductor sector (+19%) explain almost
  two-thirds. NVDA mostly moves with its sector and the market.
- CVE: the energy sector (XLE) explains 54% on top of the market's 9%. CVE
  is mostly an oil-price instrument.
- Big company-specific moves usually have something behind them: 57% of
  moves beyond 3 standard deviations had an SEC filing that day or the day
  before (NWG excluded), against a base rate of 7.5-13.6% of all days.
  The other ~43% had no filing. That doesn't mean "no news": analyst
  calls, press, rumours and sector events don't show up as filings.

## Result

Script: paper/test_why_prices_move.py (cache paper/history/book_daily.json).
752 daily returns per name, 2023-09 to 2026-09, Yahoo adjusted closes.

    name  sector  market  +sector  company   >3sd moves  with filing d0/d-1  base rate
    NVDA  SMH     44.6%   +18.9%    36.5%        8          3 (38%)          8.5%
    INTC  SMH     21.7%   +15.1%    63.2%        9          5 (56%)         13.6%
    SOFI  XLF     37.1%    +0.9%    62.0%        9          5 (56%)          8.9%
    NWG   XLF     24.3%    +5.3%    70.4%       10         10 (100%)        74.8%  <- unusable
    CVE   XLE      9.0%   +54.1%    36.9%        8          3 (38%)         11.9%
    ABBV  XLV      2.7%   +36.2%    61.2%       12          9 (75%)         12.0%
    EXEL  XBI      3.7%    +8.3%    88.0%       14          9 (64%)          7.5%

    All names excluding NWG: 60 moves beyond 3 sd, 34 with a filing (57%).

NWG's filing proxy is useless: NatWest files a 6-K on about 75% of trading
days (routine share-buyback reports), so "a filing nearby" is almost
always true. NWG's decomposition numbers are unaffected.

FAT TAILS, a side finding: under a normal distribution, 751 days would
produce about 2 moves beyond 3 sd. These names produced 8-14 each, 4 to 7
times the normal rate. Big days come far more often than a bell curve says.

## Scored against the prediction

    market share   NVDA 44.6 (pred 25-45) RIGHT; NWG 24 RIGHT; INTC 21.7 (pred 25-45) WRONG;
                   ABBV 2.7 (pred 25-45) VERY WRONG; SOFI 37 (pred 15-30) WRONG;
                   CVE 9.0 and EXEL 3.7 (pred 15-30) WRONG.
    sector adds    predicted 5-15 points. Got 0.9 (SOFI) to 54 (CVE). WRONG for
                   NVDA, CVE and ABBV; I badly underrated sector for energy and pharma.
    company-spec.  INTC, SOFI, ABBV, NWG RIGHT; NVDA (36.5) and CVE (36.9) too low;
                   EXEL (88) too high.
    big moves      57% with a filing (pred 40-60%), base rate 7.5-13.6% (pred 5-10%): RIGHT.

About half wrong. R16 trigger (c) is ON for the rest of this session.

## What this means for TARS (interpretation)

- THE SECTOR CAP (R5) COUNTS NAMES, BUT RISK LIVES IN SECTORS UNEVENLY.
  Two energy names would be close to one position twice over (CVE is 63%
  market+sector). Two biotech names would be nearly independent (EXEL is
  88% company-specific). A cap of "2 per sector" treats these the same.
  Agenda item 4 (correlation in the book) should measure this directly.
- ABBV barely moves with SPY day to day (R-squared 2.7%). It genuinely
  diversifies a book of market-sensitive names.
- For CVE, "what is oil doing" is most of the answer. A CVE thesis is
  mainly an energy-sector thesis.
- The 8% stop and fat tails: a name with 8-14 moves beyond 3 sd in 3 years
  will gap through stops more often than normal-distribution thinking
  implies. Agenda item 3 (gaps through stops) should measure this.

## What the literature says

Collected by a sub-agent; I did not re-open these sources, so treat the exact
figures as reported rather than checked.
- Roll (1988), "R-squared", Journal of Finance: market plus industry
  explain on average about 35% of MONTHLY and about 20% of DAILY variation
  in individual stocks. Removing news days barely raises the R-squared,
  which Roll read as evidence of private information or noise trading.
  Our average across the 7 names (market+sector, about 43%) is higher than
  his 20%. Plausible reasons: these names are larger and more sector-driven
  (NVDA, CVE), and sector ETFs soak up more than the SIC industries he used.
  https://authors.library.caltech.edu/records/d0wft-77023
- Cutler, Poterba & Summers (1989), "What Moves Stock Prices?": many of the
  50 largest S&P 500 daily moves, 1946-1987, had no identifiable news in
  the next day's newspaper. Macro news explains under a third of return
  variance. https://www.nber.org/papers/w2538
- Boudoukh, Feldman, Kogan & Richardson (2019, RFS): once news is
  identified properly (text analysis rather than any headline), it explains
  far more of company-specific volatility. The sub-agent reports 49.6%
  overnight vs 12.4% intraday; not checked against the paper.
  https://academic.oup.com/rfs/article-abstract/32/3/992/5061375
- Campbell, Lettau, Malkiel & Xu (2001): company-specific volatility rose
  relative to market volatility 1962-1997, so it takes more stocks to
  diversify than it used to.

The broad picture from all of it: most of a single stock's day is its own
story, and a large share of big moves have no public explanation you could
have seen coming. That is consistent with our 57% / 43% split.
