# Execution Cost: What Do Spreads and Slippage Actually Cost This Account?

One-line: RESEARCH_AGENDA item 9. Backtests assume a 5bp one-way cost. Is
that right for the names we trade, and do costs eat a meaningful share of
a trade's R?

Last Updated: 2026-09-27
Status: PREDICTION COMMITTED, TESTS NOT YET RUN
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

## Result

(not yet run)
