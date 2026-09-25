# Correlation Inside the Book: How Concentrated Is the Risk Really?

One-line: RESEARCH_AGENDA item 4. Measure how the current holdings move
together, whether same-sector pairs are the ones that matter, and how
many independent bets the book actually holds.

Last Updated: 2026-09-25
Status: PREDICTION COMMITTED, TESTS NOT YET RUN
Audience: Nolan, TARS sessions

## Data and method (fixed before running)

Holdings: NVDA, SOFI, INTC, TGT, ABBV, EXEL, NWG, CVE (as listed in
research/2026-09-24_EARNINGS_MOVES.md). Daily close-to-close returns,
2023-09 to 2026-09: daily_ohlcv_holdings.json for seven names, NVDA from
book_daily.json (split-adjusted), SPY from book_daily.json. Common dates.

C1  Pairwise correlation matrix; average over all pairs; same-sector pairs
    (NVDA-INTC semis, SOFI-NWG financials) vs cross-sector pairs.
C2  The same on stress days only (SPY down more than 1.5%).
C3  Effective number of independent bets for an equal-weight book:
    N_eff = N / (1 + (N - 1) x average correlation).
C4  Which pairs are most correlated, sector labels aside.

## PREDICTION

C1  NVDA-INTC 0.45-0.60; SOFI-NWG 0.30-0.40; cross-sector average
    0.20-0.30. Same-sector pairs clearly above cross-sector.
C2  Correlations rise on stress days by 0.10-0.20 on average.
C3  N_eff 3-4 on normal days, 2-3 on stress days (from 8 names).
C4  The top pair is NVDA-INTC.

## Result

(not yet run)
