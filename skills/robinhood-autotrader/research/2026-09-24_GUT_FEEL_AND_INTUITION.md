# How Gut Feel Works in Trading, and How to Score Nolan's Calls Fairly

One-line: RESEARCH_AGENDA item 21. When is expert intuition reliable, does
trading qualify, and what scoring method would tell us whether Nolan's gut
beats the market's own odds?

Last Updated: 2026-09-24
Status: PREDICTION COMMITTED, CALCULATION NOT YET RUN
Audience: Nolan, TARS sessions

## The one calculation (fixed before running)

A gut call is fairly scored against the probability the MARKET gave the
same event at the time (from option-implied volatility, as TARS does in
notes/GUT_CALLS.md). Per call, edge = outcome (1/0) - market probability.
Question: how many calls before an edge of +5, +10 or +20 percentage points
is distinguishable from zero at t = 2? Simulated with market probabilities
drawn like the calls so far (30-60%), 20,000 trials per case.

## PREDICTION

About 100 calls for a +10-point edge; about 25 for +20 points; about 400
for +5 points (from sd ~ 0.5 per call, n = (2 x 0.5 / edge)^2). The simple
formula will be close to the simulation.

## Result

(not yet run)
