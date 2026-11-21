# How Gut Feel Works in Trading, and How to Score Nolan's Calls Fairly

One-line: RESEARCH_AGENDA item 21. When is expert intuition reliable, does
trading qualify, and what scoring method would tell us whether Nolan's gut
beats the market's own odds?

Last Updated: 2026-09-24
Status: DONE. Prediction committed first (a5b7d63) and held.
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

## Answer first

- INTUITION IS RELIABLE ONLY WHERE TWO CONDITIONS HOLD (Kahneman & Klein
  2009): the environment has stable, learnable regularities, AND the person
  gets lots of practice with fast, clear feedback. Firefighters, nurses and
  chess players qualify. Stock picking is their named example of a
  LOW-validity environment: patterns are weak, feedback is slow and noisy,
  and confident intuition turns into systematic error.
- The base rates agree. The most active 20% of retail traders earned 11.4%
  a year against the market's 17.9% (Barber & Odean 2000). About 9 in 10
  professional US large-cap funds trail the S&P 500 over 15 years (SPIVA,
  as reported). Among Taiwanese day traders, only a small minority stay
  profitable year after year.
- Gut feel isn't nothing. London traders who were better at sensing their
  own heartbeat made more money and lasted longer (Kandasamy, Coates et al.
  2016). Bodily signals can carry learned information. But that's selected
  professionals making thousands of fast decisions, not occasional calls on
  single stocks months out.
- HOW TO SCORE NOLAN FAIRLY: against the market's probability, not against
  zero. A call on a 40% event that comes true is worth +0.6; one that
  doesn't is -0.4. Averaged over many calls, a positive score means the gut
  sees something the options market didn't. notes/GUT_CALLS.md already
  logs TARS's market-based probability next to each call. What's missing
  is Nolan's own confidence number, which would allow a Brier score and a
  calibration check (Tetlock's method).
- HOW LONG IT TAKES: see the table. Even a strong edge needs dozens of
  calls. A modest one needs hundreds. The SOFI call alone can't tell us
  anything either way, and that's no reflection on Nolan.

## Result

Script: paper/sim_gut_calls.py. Market probability per call uniform on
30-60%; 20,000 simulated records per cell. Figures are the share of records
reaching t >= 2 ("power").

    true edge     10 calls  25   50   100  200  400
    +5 points        6%     7%  10%  16%  29%  51%
    +10 points      10%    18%  29%  51%  81%  98%
    +20 points      28%    54%  83%  98% 100% 100%
    no edge, 100 calls: 2.2% false positives

The formula n = (2 x 0.5 / edge)^2 gives 400 / 100 / 25 calls for a 50%
chance of detection, and the simulation agrees. For an 80% chance, double
it.

## Scored against the prediction

    ~100 calls at +10, ~25 at +20, ~400 at +5; formula close to simulation: RIGHT on all.

## Proposed changes to notes/GUT_CALLS.md (not made here; Nolan decides)

1. Log Nolan's confidence with each call ("60%", "80%") as well as yes/no.
2. Log calls that FEEL strong and calls that don't. Only logging the
   memorable ones is the same survivorship problem as item 5.
3. Keep the market-probability column; score the running total of
   (outcome - market probability), and don't read anything into it before
   ~25 calls.

## Literature (sub-agent; flagged items not checked against the primary source)

- Kahneman & Klein (2009), American Psychologist 64(6). https://pubmed.ncbi.nlm.nih.gov/19739881/
- Barber & Odean (2000), JF: 66,465 households 1991-1996; most active
  quintile 11.4%/yr vs market 17.9%. https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00226
- Barber, Lee, Liu & Odean, Taiwan day traders: about 5% reliably
  profitable, heavy attrition (sub-agent figures, not checked).
  https://faculty.haas.berkeley.edu/odean/papers/Day%20Traders/Day%20Trade%20040330.pdf
- Kandasamy, Coates et al. (2016), Scientific Reports 6:32986. https://www.nature.com/articles/srep32986
- Tetlock: calibration and Brier scoring; "superforecasters" win through
  probabilistic, frequently updated judgments. (Sub-agent's "+30% vs
  analysts" figure not checked.)
- SPIVA US scorecard: ~89.5% of large-cap funds behind the S&P 500 over 15
  years (sub-agent; not checked). https://www.spglobal.com/spdji/en/spiva/article/spiva-us/
