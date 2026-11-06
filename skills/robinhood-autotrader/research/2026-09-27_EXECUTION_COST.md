# Execution Cost: What Do Spreads and Slippage Actually Cost This Account?

One-line: RESEARCH_AGENDA item 9. Backtests assume a 5bp one-way cost. Is
that right for the names we trade, and do costs eat a meaningful share of
a trade's R?

Last Updated: 2026-09-27
Status: DONE. Prediction committed first (a9363bc). Stock execution cost is real but tiny: ~0.007R per round trip.
Audience: Nolan, TARS sessions

## The data problem, stated first

paper/trades.jsonl never recorded the bid/ask at order time (no quote
field on any row), so "fill vs quote" can't be measured directly. Two
substitutes, both standard:

X1  Corwin-Schultz (2012) bid-ask spread estimator from daily highs and
    lows. For the 14 backtest names (daily_stocks.json) and current
    holdings (daily_ohlcv_holdings.json), 2024-09 to 2026-09: median
    estimated spread per name, in basis points. Known to be noisy and to
    overstate spreads for very liquid names.
X2  Live fills against the market at that minute: each live EQUITY fill
    with a timestamp in trades.jsonl, compared to the close of the
    1-minute Yahoo bar containing the fill time. Signed so positive =
    paid more than the market (buys above, sells below). Yahoo keeps
    1-minute bars for ~30 days, which covers the whole live record.
X3  Cost in R: round-trip cost / 8% stop distance, to compare with the
    size of a typical trade result (+0.77R for the TENB win).

## PREDICTION

X1: large caps 5-20bp; holdings 10-40bp; SOFI and EXEL the widest.
X2: median absolute gap to the minute bar 2-10bp; mean signed cost
    0 to +10bp.
X3: a round trip costs at most ~0.03R. Immaterial next to a +0.77R trade;
    the engine's 5bp assumption is about right for stocks. (Options are a
    different story, already measured in reference/options.md and item 19.)

## Answer first

- STOCK EXECUTION COSTS THIS ACCOUNT ABOUT 2.7 BASIS POINTS EACH WAY.
  Across 55 live stock fills (2026-09-10 to 09-25), fills averaged 2.7bp
  worse than the market price in that minute (t = +2.16, so small but real);
  the typical gap was 3.2bp and 90% of fills were within 13bp.
- IN R TERMS IT'S NOTHING: a round trip costs about 0.007R at an 8% stop.
  The TENB win (+0.77R) paid roughly 1% of itself in execution. The
  engine's 5bp-per-side assumption (0.0125R per round trip) is slightly
  conservative, so the backtests are not flattered by it.
- THE HIGH/LOW SPREAD ESTIMATOR IS USELESS FOR THESE NAMES: Corwin-Schultz
  put their spreads at 17-60bp, 5-15x what the fills show. For large,
  liquid US stocks it measures intraday volatility more than spread. Don't
  use it to size costs here.
- WHERE COST DOES MATTER: options (item 15/19: retail weekly spreads ~12.6%,
  our own small-name chains 3-28%) and trading frequency. Stocks at this
  account's size are not where money leaks.

## Result

Script: paper/test_execution_cost.py. Minute bars: Yahoo 1-minute, cached in
paper/history/minute_bars_fills.json.

    X2 live equity fills vs the 1-minute bar close at the fill time
       all 57 unique fills:        mean -9.7bp (t=-0.55), median +2.1bp
       excluding 2 TENB rows:      n=55  mean +2.7bp  t=+2.16  median +2.1bp
                                   median |gap| 3.2bp  90th percentile |gap| 12.9bp
       2 fills (SOFI and NEM, 2026-09-21 ~13:15-13:22 UTC) had no minute bar:
       they filled before the regular session, pre-market.

    X3 round trip at an 8% stop
       engine assumption 5bp/side   10.0bp = 0.0125R
       measured mean 2.7bp/side      5.4bp = 0.0067R
       measured median gap 3.2bp     6.5bp = 0.0081R

    X1 Corwin-Schultz median spread estimate, 2024-09 to 2026-09
       14 backtest names: 21.6bp (IBM, XOM) to 52.8bp (NVDA)
       holdings: NWG 16.8, ABBV 29.9, INTC 36.1, CVE 38.6, TGT 42.1,
       SOFI 52.5, EXEL 59.7bp

## Data problems found and handled (recorded so nobody repeats them)

1. Every buy appeared twice: exit rows in trades.jsonl repeat the entry
   price and time of the position they close. Deduplicated on
   (symbol, minute, side, price) before measuring.
2. Two TENB rows are not fills: after the 2026-09-16 top-up, the ledger
   records the BLENDED average entry ($33.20) with the top-up's timestamp,
   when the market was $36.75. That shows up as -965bp and +262bp. They're
   excluded from the headline and reported separately. The exclusion rule
   (TENB rows beyond 100bp) was chosen after seeing the output; the
   all-fills median (+2.1bp) is unaffected by it.
3. The comparison price is the minute bar's last trade, not the NBBO at the
   moment of the order. It includes up to a minute of price drift, so
   treat the 2.7bp as "cost plus noise", not a clean spread.
4. The ledger never recorded the quote at order time. PROPOSAL (not
   adopted): the desk should log bid, ask and time on every order. That
   turns this estimate into a direct measurement at no cost.

## Scored against the prediction

    X1 large caps 5-20bp: WRONG (22-53bp; the estimator overstates, as flagged
       beforehand). Holdings 10-40bp: partly WRONG (17-60bp). SOFI and EXEL
       widest: RIGHT (EXEL 59.7, SOFI 52.5; NVDA also 52.8).
    X2 median gap 2-10bp: RIGHT (3.2bp). Mean 0 to +10bp: RIGHT (+2.7bp).
    X3 at most ~0.03R, engine's 5bp about right: RIGHT (0.007R; 5bp slightly conservative).
