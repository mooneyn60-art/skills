# Correlation Inside the Book: How Concentrated Is the Risk Really?

One-line: RESEARCH_AGENDA item 4. Measure how the current holdings move
together, whether same-sector pairs are the ones that matter, and how
many independent bets the book actually holds.

Last Updated: 2026-09-25
Status: DONE. Prediction committed first (ed69a9b); more than half of it was wrong.
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

## Answer first

- THE BOOK IS ABOUT 3.9 INDEPENDENT BETS, NOT 8 (3.4 on stress days).
  That's better diversified than I expected. Average pairwise correlation
  is only 0.15.
- THE SECTOR CAP IS AIMED AT THE WRONG THING. The pair that moves together
  most is NVDA-SOFI (0.37), a chip maker and a fintech the cap treats as
  unrelated. NVDA-INTC, the "same sector" pair the cap was written for, is
  only 0.32 over three years and slightly NEGATIVE on stress days
  (INTC's own story dominated 2024-2026; see item 17).
- WHAT ACTUALLY LINKS THE NAMES IS MARKET SENSITIVITY: NVDA (0.67 with SPY),
  SOFI (0.61), NWG (0.49) and INTC (0.47) are the high-beta cluster; ABBV
  (0.16) and EXEL (0.19) barely move with the market. Two high-beta names
  in different sectors are more of a concentrated bet than two pharma
  names in the same sector.
- Correlations rose only a little on stress days (+0.04 on average; 19 of
  28 pairs up). With just 35 stress days each stress correlation has a
  sampling error of about +/-0.17, so that part is weakly measured.

## Result

Script: paper/test_book_correlation.py. 751 daily returns, 2023-09-25 to
2026-09-23; stress days = SPY down more than 1.5% (35 days).

                        all days   stress days
    average pairwise     +0.150     +0.195
    same-sector pairs    +0.339     +0.152
      NVDA-INTC          +0.324     -0.047
      SOFI-NWG           +0.353     +0.351
    cross-sector pairs   +0.136     +0.198
    N_eff (of 8)          3.90       3.39

    highest pairs, all days: NVDA-SOFI +0.37, SOFI-NWG +0.35, NVDA-INTC +0.32,
      SOFI-INTC +0.25, NVDA-NWG +0.25, INTC-NWG +0.23
    lowest: NVDA-ABBV -0.06, EXEL-CVE -0.02, SOFI-ABBV +0.00, NVDA-EXEL +0.03
    correlation with SPY: NVDA +0.67, SOFI +0.61, NWG +0.49, INTC +0.47,
      TGT +0.32, CVE +0.30, EXEL +0.19, ABBV +0.16

Caveats: NVDA and SPY use split-adjusted closes (book_daily.json); the other
seven use raw closes (no splits in the window; dividends ignored).
Correlations computed only on stress days are biased by the selection
itself, so compare them loosely.

## Scored against the prediction

    NVDA-INTC 0.45-0.60: WRONG (0.32)       SOFI-NWG 0.30-0.40: RIGHT (0.35)
    cross-sector 0.20-0.30: WRONG (0.14)    same > cross: RIGHT
    stress rise 0.10-0.20: WRONG (+0.04)    N_eff 3-4: RIGHT (3.90)
    stress N_eff 2-3: WRONG (3.39)          top pair NVDA-INTC: WRONG (NVDA-SOFI)

R16 (c) remains on for this session.

## Proposal (not adopted; needs the four hurdles as a sizing test first)

Replace or supplement R5's "2 per sector" with a limit on combined MARKET
SENSITIVITY: e.g. no more than N positions with correlation to SPY above
0.5, or a cap on the book's total beta. The sector label is a proxy for
correlation, and this data says it's a weak one. Test it in paper/engine.py
before anyone proposes it for adoption.
