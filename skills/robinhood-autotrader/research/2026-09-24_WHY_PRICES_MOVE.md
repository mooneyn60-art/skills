# Why Prices Move on a Given Day: Market, Sector, or Company?

One-line: RESEARCH_AGENDA item 16. Split each held name's daily moves into
the part explained by the whole market (SPY), the part added by its sector,
and the part that is company-specific. Then check how often a big
company-specific move has a company filing behind it.

Last Updated: 2026-09-24
Status: PREDICTION COMMITTED, TEST NOT YET RUN
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

## Result

(not yet run)
