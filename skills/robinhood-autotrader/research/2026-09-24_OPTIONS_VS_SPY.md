# Do Options Beat SPY? Buying vs Selling, Index Level, 1986-2026

One-line: RESEARCH_AGENDA item 15, Nolan's priority. Nolan believes "options
are how we beat the SPY a lot." This note tests that belief on the longest
public data available, separating BUYING options from SELLING them.

Last Updated: 2026-09-24
Status: DONE. Belief tested and NOT supported. Predictions committed first (28f48b0).
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

## Answer first

NOLAN'S BELIEF IS NOT SUPPORTED. On 20 to 38 years of data:
- BUYING options loses to the S&P 500 by a wide margin. A strategy of
  holding at-the-money calls instead of the index (rest in T-bills) made
  -0.35% a year against the S&P's +11.37%, 1991-2026.
- SELLING options (the CBOE put-write and buy-write indexes) earned LESS
  than the S&P 500 in every version tested, with lower volatility and
  smaller drawdowns. Since 2007 the put-write index trails by 3.9pp a year
  (t = -2.26) and beat the S&P in only 1 of 9 windows, the 2007-09 crash.
- Nothing here beats SPY "a lot". The honest case for selling is "a bit
  less return, noticeably less risk", and even that case has been weak
  since about 2009.

Where the belief comes from, and it isn't irrational: individual option
trades CAN return 5x, 10x. What that misses is that the price of the
option already includes that chance plus a fee (the volatility risk
premium). Across hundreds of trades the fee wins.

## Result

Scripts: paper/fetch_options_indices.py (writes
paper/history/options_indices.json), paper/test_options_vs_spy.py (prints
everything below). Benchmark is the S&P 500 TOTAL return (dividends in), the
fair comparison for total-return option indices. All returns are pre-tax
and ignore trading costs except where stated.

### O1 selling puts: CBOE PutWrite (PUT) vs S&P 500 TR, 2007-01 to 2026-09 (236 months)

    PUT        CAGR  7.17%  vol 10.7%  Sharpe 0.56  maxDD -32.7%
    S&P 500 TR CAGR 11.04%  vol 15.4%  Sharpe 0.66  maxDD -50.9%
    monthly difference -0.348pp, t=-2.26
    split: 2007-2016 -0.100pp (t=-0.47), 2016-2026 -0.596pp (t=-2.70)
    walk-forward: PUT ahead in 1 of 9 windows (2007-02 to 2009-03, +1.14pp/month)
    drop best & worst year: PUT 8.00%/yr vs S&P 13.80%/yr

Long run, from the 6 scattered pre-2007 CBOE points only:
1991-03 to 2004-03, PUT 12.31%/yr vs S&P TR 11.11%/yr. Two points, so no
t-statistic is possible. It fits the published finding (Bondarenko, below)
that put-writing roughly matched the S&P before 2007 with less risk.

NOTE ON A BUG CAUGHT BEFORE WRITING THIS UP: the first run fed those 6
scattered points in as if they were monthly returns and printed a 20% CAGR
for the S&P, which is impossible. The comparison was restricted to the daily
history from 2007, as the data section intended. The design didn't change.

### O2 selling calls: buy-write indexes vs S&P 500 TR

    BXM  (ATM covered call) 2002-03 to 2026-09, 294 months
      BXM  CAGR  6.20%  vol 10.7%  Sharpe 0.46  maxDD -35.8%
      S&P  CAGR 10.17%  vol 14.9%  Sharpe 0.61  maxDD -50.9%
      monthly difference -0.352pp, t=-2.78; BXM ahead in 2 of 9 windows

    BXMD (30-delta covered call) 1988-01 to 2026-09, 464 months
      BXMD CAGR 10.92%  vol 12.3%  Sharpe 0.67  maxDD -42.7%
      S&P  CAGR 11.51%  vol 14.6%  Sharpe 0.62  maxDD -50.9%
      monthly difference -0.070pp, t=-1.08; ahead in 4 of 9 windows
      split: 1988-2007 +0.080pp (t=+0.95), 2007-2026 -0.221pp (t=-2.24)

The 30-delta version is the best showing for options anywhere in this note:
about the S&P's return (-0.6pp/yr) with less volatility and a slightly
higher Sharpe ratio over 38 years. But the entire advantage sits in
1988-2009 and has been negative in every window since.

### O3 buying, simulated: 1-month SPX options, 428 monthly rolls, 1991-2026

Priced at VIX, plus 1% of premium as cost:

    option           mean on premium  t      median   lose money  expire worthless
    ATM call           -9.5%        -1.95   -47.3%     59.8%        35.7%
    5% OTM call       -76.7%       -17.08  -100.0%     93.5%        87.4%
    ATM put           -45.8%        -8.79  -100.0%     77.8%        64.3%

    1x calls + T-bills  CAGR -0.35%  maxDD -60.6%
    2x calls + T-bills  CAGR -3.89%  maxDD -90.1%
    S&P 500 TR          CAGR 11.37%  maxDD -54.1%

Priced at 0.9 x VIX (the generous case, since VIX sits above at-the-money
implied vol because of put skew):

    ATM call           +0.4%         +0.08   -41.7%     57.7%
    5% OTM call       -70.2%        -12.24  -100.0%     92.5%
    ATM put           -39.6%         -6.85  -100.0%     77.1%
    1x calls + T-bills  CAGR 2.36%   2x  CAGR 1.41%   S&P 500 TR 11.37%

Both halves (1991-2008 and 2008-2026) agree: the S&P beats every buying
strategy in both. The OTM call, the classic "cheap lottery ticket", loses
70-77% of what is paid for it on average, and 87% of them expire worthless.

Why a call strategy can lose money while the market rises 11% a year: an
at-the-money 1-month call at VIX 20 costs about 2.3% of the index every
month, ~27% a year. The index's upside months have to pay that back first.
The volatility risk premium is this gap between the vol priced in and the
vol that happened.

### O4 this account's own option trades

12 closed option trades, 2026-09-11 to 2026-09-17: mean -0.08R, t=-0.38.
11 of 12 lost money; the one winner was a 19-minute F call round trip
(+2.00R). Too few to prove anything on their own, but they point the same
way as everything above.

## Scored against the predictions

    O1 PUT     predicted 0.5-2pp below S&P, t not significant
               GOT 3.9pp below, t=-2.26: WORSE than predicted.
               "Similar or higher Sharpe": WRONG, Sharpe 0.56 vs 0.66.
               "PUT ahead 2000-2009, behind 2010-2026": RIGHT in shape.
    O2 BXM     predicted 1-4pp below: GOT 4.0pp below. At the edge of the range.
       BXMD    "closer to the S&P": RIGHT, -0.6pp/yr.
    O3         ATM puts -15% to -30%: GOT -40% to -46%, WORSE than predicted.
               ATM calls -10% to +10%, 55-65% losing: RIGHT.
               OTM calls worse than ATM, 75%+ worthless: RIGHT (87%).
               1x calls 2-5pp below S&P: WRONG, 9-12pp below. I underestimated
               how expensive it is to rent the upside every month.
               2x calls below S&P with >60% drawdown: RIGHT (-80% to -90%).
    O4         negative mean R: RIGHT.

The OVERALL prediction (false for buying, not "a lot" for selling) held.
Every miss was in the direction of options doing WORSE than I thought.
None of these misses refutes the stated hypothesis, so R16 (c) is not
triggered.

## What the research literature says

Retail option traders (verified against the sources):
- SEBI, India's regulator, Sept 2024: 93% of 11.3 million individual
  equity F&O traders lost money FY22-FY24, aggregate losses over 1.8 lakh
  crore rupees (~$21B).
  https://www.sebi.gov.in/media-and-notifications/press-releases/sep-2024/updated-sebi-study-reveals-93-of-individual-traders-incurred-losses-in-equity-fando-between-fy22-and-fy24-aggregate-losses-exceed-1-8-lakh-crores-over-three-years_86906.html
- Bauer, Cosemans & Eichholtz (2009), Journal of Banking & Finance, 26,266
  Dutch retail option traders: they lose 1.81% per month on option
  positions, much more than equity traders. The study blames bad market
  timing (overreacting to past returns) and high costs, and names gambling
  and entertainment as the main motives.
  https://papers.ssrn.com/sol3/papers.cfm?abstract_id=965810
- Bryzgalova, Pavlova & Sikorskaya (2023), Journal of Finance: US retail
  prefers cheap weekly options with an average bid-ask spread of 12.6%, and
  loses money on average. (A sub-agent reported aggregate losses of $2.1B
  for Nov 2019 to Jun 2021; I have not checked that figure against the
  paper.) https://onlinelibrary.wiley.com/doi/full/10.1111/jofi.13285
- de Silva, Smith & So, "Losing is Optional": retail losses concentrate
  around earnings announcements, where they overpay for implied volatility.
  (The sub-agent reported 5-9% average losses and 10-14% around
  high-volatility announcements; not checked against the paper.)
  https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4050165

Volatility risk premium and strategy literature (collected by a sub-agent
from PDFs it opened; items it couldn't open are marked):
- The gap exists and is large: 1990-2018, average VIX 19.3% against
  average realised S&P volatility 15.1%, a 4.2-point premium (Bondarenko
  2019, CBOE-published). Ilmanen (2012, AQR) shows it "almost always
  positive" 1986-2012.
  https://cdn.cboe.com/resources/education/research_publications/PutWriteCBOE19_v14_by_Prof_Oleg_Bondarenko_as_of_June_14.pdf
- PUT, 1986-2018: 9.54%/yr vs S&P 9.80%/yr, volatility 9.95% vs 14.93%,
  Sharpe 0.65 vs 0.49 (Bondarenko 2019). ROUGHLY EQUAL RETURN, LOWER RISK.
  This disagrees with O1 above only in period: O1 covers 2007-2026, where
  PUT trails by 3.9pp. Both are right. The long-run story is "equal return,
  less risk", and the last ~15 years have been an exception, or the premium
  has shrunk as more money sells it. This data can't tell which.
- Coval & Shumway (2001): at-the-money zero-beta S&P straddles lost about
  3% PER WEEK, 1986-1995. Puts earn below the risk-free rate.
  https://ideas.repec.org/a/bla/jfinan/v56y2001i3p983-1009.html
- Israelov & Nielsen (2015), "Covered Calls Uncovered": the short-vol piece
  of a covered call has a Sharpe ratio near 1.0, but it is only ~10% of the
  position's risk. Most of the risk is plain equity plus an uncompensated
  "equity reversal" bet. A covered call is mostly a stock position with a
  worse shape. https://www.aqr.com/-/media/AQR/Documents/Insights/Journal-Article/Covered-Calls-Uncovered.pdf
- Ilmanen (2012): across markets, SELLING insurance and lottery tickets has
  been rewarded and BUYING them has not. Example: long VIX futures lost
  28%/yr Dec 2005 to Aug 2011, even though VIX tripled over that period.
- LEAPS as stock replacement: no verifiable primary evidence found either
  way (sub-agent could not open the sources). Unknown, not "fine".
- Whaley (2002) on BXM: original not opened; commonly cited as higher Sharpe
  than the S&P 1988-2001. Unverified exact figures.

## What is actually feasible at ~$1,500-2,000

- THE ACCOUNT IS LEVEL 2 (reference/options.md §1): long calls/puts,
  covered calls, cash-secured puts. No spreads.
- Index put-writing, the one strategy with a decades-long record, is out
  of reach. One SPY cash-secured put needs roughly 100 x the SPY price in
  collateral, ~$70,000+. Even the mini-SPX (XSP) is ~$7,700 of notional.
  A put credit spread on SPY could fit ($500 of risk for a $5-wide spread),
  but it needs level 3, it gives up most of the premium to the long leg,
  and O1 says the underlying strategy has trailed the S&P since 2007.
- Single-stock cash-secured puts: collateral = 100 x strike, so a $15
  stock ties up $1,500, i.e. 75-100% of the account in one name.
  options.md §5 and §5b measured this: real but insufficient premium,
  and a large ruin risk with no diversification.
- Buying: R9's 3% cap is $45-60 at this size; real 30-45 DTE contracts cost
  $58-$640 (R9's 2026-09-17 survey). And O3 says buying has negative
  expectancy regardless of size.
- Conclusion: at this account size there is no options strategy with
  evidence of beating the S&P, and the only one with a long record of
  matching it (with less risk) can't be placed.

## Proposed, not adopted

No R9 change. The evidence argues AGAINST loosening R9, not for it. If Nolan
still wants options exposure, the defensible version is: after R9's gate,
a 30-delta covered call on a position already held (the BXMD profile, the
best result here), treated as a way to cut volatility, NOT as a way to beat
SPY. That needs 100 shares of the name, so it is a large-account idea.

## What would change this answer

- A sustained regime like 2000-2009 (flat-to-falling market, high implied
  vol): selling premium beat the S&P then, in every version.
- Evidence that implied vol has fallen persistently BELOW realized vol
  (the premium disappearing). That would make buying fair, not profitable.
- Neither is observable in advance, and neither makes options beat SPY "a
  lot".
