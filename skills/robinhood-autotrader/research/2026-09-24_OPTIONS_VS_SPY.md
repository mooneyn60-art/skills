# Do Options Beat SPY? Buying vs Selling, Index Level, 1986-2026

One-line: RESEARCH_AGENDA item 15, Nolan's priority. Nolan believes "options
are how we beat the SPY a lot." This note tests that belief on the longest
public data available, separating BUYING options from SELLING them.

Last Updated: 2026-09-24
Status: PREDICTIONS COMMITTED, TESTS NOT YET RUN
Audience: Nolan, TARS sessions

## What already exists (don't repeat it)

reference/options.md already measured SINGLE-NAME, SMALL-ACCOUNT options on
live chains: buying OTM is "measured, negative, settled" (ALOY -96%; 40
sequential OTM buys, median bankroll $1,023 -> $45), and the wheel on sub-$10
names has a real but insufficient edge. This note adds what's missing: the
INDEX level over decades, where the volatility risk premium is best measured
and where "options beat SPY" should show up if it's true anywhere.

## Mechanism

The volatility risk premium. Option buyers pay for insurance and lottery-like
payoffs. On average, implied volatility exceeds the volatility that follows,
so option SELLERS collect a premium and BUYERS pay it. If this is right:
- buying calls in place of the index should UNDERPERFORM the index;
- systematic selling (put-writing, buy-writes) should earn close to equity
  returns with LOWER volatility, and lag in strong bull runs because it caps
  the upside.
Under this mechanism, "options beat SPY a lot" is false for buyers and at
most "similar return, less risk" for sellers.

## Data

- CBOE daily index histories, fetched 2026-09-24 from
  cdn.cboe.com/api/global/us_indices/daily_prices/:
  PUT (S&P 500 PutWrite: sells 1-month ATM SPX puts, fully cash-collateralised
  in T-bills), BXM (S&P 500 BuyWrite: long S&P, sells 1-month ATM call),
  BXMD (30-delta buy-write), SPX (price), VIX.
- S&P 500 TOTAL return (^SP500TR, dividends reinvested), Yahoo Finance chart
  API. This is the fair benchmark: PUT and BXM are total-return indices, and
  SPY's price series in paper/history omits dividends.
- 3-month T-bill (DTB3), FRED.
- Account record: paper/trades.jsonl.

## Tests (fixed before running)

O1  PUT vs S&P 500 TR, month-end returns, common history.
O2  BXM vs S&P 500 TR (2002+), and BXMD vs S&P 500 TR (1986+).
    For O1/O2: CAGR, annualised volatility, Sharpe (vs DTB3), max drawdown,
    mean monthly return difference with t. Hurdles: split sample (halves),
    9-window walk-forward, and in place of "drop the megacaps" (not
    meaningful for an index): drop the single best and single worst
    calendar year for each series.
O3  BUYING, simulated. Each month (21 trading days), buy 1-month SPX options
    priced by Black-Scholes at sigma = VIX, r = DTB3, q = dividend yield
    implied by SP500TR vs SPX over the prior 252 days, plus 1% of premium as
    cost. Variant with sigma = 0.9 x VIX, because VIX includes put skew and
    sits above at-the-money implied vol.
    (a) per-option statistics for ATM calls, 5% OTM calls, ATM puts: mean
        return on premium, median, share expiring worthless;
    (b) "calls instead of stock": notional = 1x equity in ATM calls, the rest
        in T-bills, rolled monthly; and a 2x-notional version. CAGR, vol,
        max drawdown vs S&P 500 TR.
O4  The account's own closed options trades, in R.

## PREDICTIONS (committed before any script exists)

O1 PUT: CAGR within 0.5-2pp BELOW S&P 500 TR over the full history,
   volatility about two-thirds of the S&P's, Sharpe similar or higher.
   Monthly difference not significant (|t| < 2). PUT ahead in 2000-2009,
   behind in 2010-2026.
O2 BXM: CAGR 1-4pp below S&P 500 TR since 2002. BXMD closer to the S&P.
O3 (a) ATM puts lose badly: mean -15% to -30% of premium per month.
       ATM calls: mean between -10% and +10%, 55-65% of them lose money.
       5% OTM calls: mean worse than ATM, 75%+ expire worthless.
   (b) 1x calls-instead-of-stock: CAGR 2-5pp BELOW S&P 500 TR with smaller
       drawdowns. 2x version: CAGR below S&P 500 TR, max drawdown worse
       than 60%.
O4 Negative mean R (R9 already records -0.12R).

OVERALL PREDICTION: Nolan's belief is FALSE for buying and false in the
"a lot" sense for selling. Selling earns about the S&P's return with less
risk; it does not beat it by a lot.

What would prove me wrong: PUT or BXM beating S&P 500 TR by 2pp+/yr with
|t| >= 2 and passing the hurdles; or the 1x or 2x call strategy beating
S&P 500 TR on CAGR.

## Result

(not yet run)
