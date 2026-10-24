# Position Count Test — Concentration Rejected

One-line: concentrating the book below four positions is destructive; four
through eight are indistinguishable, so the current book needs no change.

Last Updated: 2026-09-23
Status: CLOSED — proposal tested and rejected
Audience: TARS sessions, Nolan

## Overview

On 2026-09-22 TARS proposed concentrating the book from seven positions to
three or four, on the argument that whole-share quantization (R12) lets the
share price rather than conviction set position weight — ABBV occupied the
full 20% R3 cap on a single share while NWG sat at 2.8%, a 7.1x spread that
reflected nothing but price tags.

THE PROPOSAL WAS TESTED AND FAILED. It is recorded here rather than quietly
dropped, because TARS recommended it to the account owner before testing it.

## Method

TARS-2 ruleset (symmetric 200-day entry and exit, breakeven raise, 20% cap,
no flat cap, no trail), 14 symbols, 5,209 daily bars each, 2006-01 to
2026-09, whole shares, 5bp slippage per side. max_positions swept 1..8.
All four standing hurdles applied.

## Results

Full period, CAGR by max_positions:

    n=1   3.69%    n=5  17.73%
    n=2   6.69%    n=6  20.92%
    n=3  14.73%    n=7  15.28%
    n=4  16.92%    n=8  20.17%

SPY buy and hold over the same window: 8.89%, max drawdown -54.3%.

Adjacent settings at the top of the curve swing 5.6 points (n=6 20.9, n=7
15.3, n=8 20.2). A parameter whose neighbours disagree that violently is
fitting noise, so no single value in the plateau can be claimed as best.

Split sample: n=1 and n=2 are worst in both halves. Above n=4 the ranking
reshuffles — the first half's winner (n=8) ranks second in the second half.

Rolling walk-forward, 9 windows: n=1 and n=2 NEVER win a window, and n=1
returns negative in two of them. Best-n by window is [4,5,6,5,8,5,5,5,6];
n=5 wins 5 of 9, which is the most consistent but not dominant.

Drop the big winners: the curve shape survives all five universes (full 14,
minus NVDA, minus NVDA+AAPL, minus those plus AMZN, minus all five
megacaps). n=1 and n=2 stay worst in every row. THE FINDING IS ABOUT
DIVERSIFICATION, NOT ABOUT OWNING ONE STOCK.

## Verdict

NO RULE CHANGE. The book already runs six mechanical positions plus one
carved-out holding, which sits inside the plateau. The only claim the
evidence supports is a floor: never run fewer than four positions.

## Why the mechanism was backwards

Trend following pays through a small number of large winners that cannot be
identified at entry. Fewer slots does not sharpen the bet, it buys fewer
tickets in a game where the winning ticket is unknowable in advance. The
live book demonstrates it: two names are 101% of open profit, and neither
was distinguishable from the other five on the day it was bought.

The quantization complaint that motivated the proposal is REAL and remains
unfixed — share price still sets position weight at this account size.
Concentration is simply not the remedy.

## Caveat that must travel with this result

Stripped of the five megacaps, the best setting returns 6.8% against SPY's
8.9%. De-winnered, this system does not beat the index at any position
count. Concentration does not clear that wall and nothing tested so far
does.
