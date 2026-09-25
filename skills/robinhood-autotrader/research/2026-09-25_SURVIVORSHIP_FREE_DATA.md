# Survivorship-Free Data: What Exists, What It Costs, Is Free Good Enough?

One-line: RESEARCH_AGENDA item 5. Every backtest here uses 14-15 large caps
picked in 2026, all of which survived. What would it take to test on the
stocks that were actually in the index at the time, including the ones
that later failed?

Last Updated: 2026-09-25
Status: DONE. Research only; nothing signed up for or bought.
Audience: Nolan, TARS sessions

## Answer first

- A survivorship-free test needs two things: (1) WHO was in the index on
  each date, and (2) PRICES for the stocks that later left or died.
- (1) IS FREE AND GOOD ENOUGH. The GitHub project fja05680/sp500 has
  point-in-time S&P 500 membership from 1996 to now (Andreas Clenow's list,
  kept up to date from Wikipedia changes). I read the README myself. The
  maintainer warns that 1996-2000 may be missing a few names (487-494
  instead of ~500) and suggests starting in 2001. That still gives 25 years.
- (2) IS THE PROBLEM. Yahoo, our current free source, only keeps current
  tickers; delisted history is now behind its paid tier. The README says
  plainly "if you want to backtest stocks, you are going to need to
  purchase data."
- CHEAPEST OPTIONS (as reported by a sub-agent; prices not checked on a
  live pricing page):
  - Tiingo free tier: claims to keep delisted tickers (stable IDs with
    end dates), 50 symbols an hour. Free, but needs an account and API
    key. Pulling ~1,000 historical S&P names would take ~20 hours of
    throttled fetching. Coverage quality unverified.
  - Sharadar direct (sharadar.com): $9-69/month, personal-use licence,
    point-in-time S&P 500 membership back to 1957 AND delisted prices from
    ~1998. The best value on paper for exactly this job.
  - Norgate Data: ~$630-790/year, deepest history (1950/1990), no REST API
    (desktop tool plus a Python plugin). Used by the author of the
    membership list.
  - EODHD: delisted data appears to need the $99.99/month plan.
  - CRSP (via WRDS): the academic gold standard, not sold to individuals.
- RECOMMENDATION (Nolan decides; nothing done): try the free route first:
  fja05680 membership + Tiingo free tier. If Tiingo's delisted coverage
  turns out patchy, one month of Sharadar (the cheapest plan that
  includes the needed tables) is enough to download the history once for
  personal research, if its licence allows keeping the data (check
  before paying). Needs Nolan to create any account; TARS must not.

## Why it's worth doing

Items 8 and 18 show the repository's positive results are weak and
flattered by the 14-name universe (all survivors, several megacap
winners). A survivorship-free re-run of R2 and R15 over 2001-2026 on the
real S&P 500 membership is the single most useful test left. It would
tell us whether the 200-day gate's risk control and R15's stressed-market
reversal hold on stocks that DIDN'T make it.

## Comparison (sub-agent table; "unverified" where it couldn't confirm on an opened page)

    source                     cost             delisted prices  index membership      start
    fja05680/sp500 (GitHub)    free             no               yes, point-in-time    1996 (use 2001+)
    Wikipedia S&P 500 page     free             no               current + partial log  -
    Tiingo                     free-$50+/mo     yes (claimed)    no                     varies
    Alpha Vantage              free/paid        delisted LISTS   no                     full history unverified
    Stooq                      free             unverified       no                     ~20 yrs
    Yahoo Finance              paid tier        paywalled        no                     -
    EODHD                      $0-99.99/mo      top plan only    not documented         ~2000
    Massive (ex-Polygon)       free-$199/mo     yes, "spotty"    no                     2003
    Sharadar (direct)          $9-69/mo         yes              yes, since 1957        ~1998
    Norgate Data               ~$630-790/yr     yes              yes                    1990 / 1950
    CRSP via WRDS              institutional    yes              yes                    1925

Sources: https://github.com/fja05680/sp500 (README read directly);
https://www.tiingo.com/products/end-of-day-stock-price-data;
https://sharadar.com/subscribe; https://eodhd.com/pricing;
https://massive.com/pricing; https://www.alphavantage.co/documentation/;
https://wrds-www.wharton.upenn.edu/pages/about/data-vendors/center-for-research-in-security-prices-crsp/;
Norgate price via a third-party review (https://alvarezquanttrading.com/blog/norgate-data-review/).
