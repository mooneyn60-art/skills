# Hold Through Earnings or Sell Before? (Swarm Queue Item 4)

One-line: For names the momentum screen would hold, the earnings reaction
averaged -0.78% (n=142, 2025-26) and about 1 in 7 went 8%+ against the
holder. Sitting out earnings gave up nothing on average and removed the gap risk.

Last Updated: 2026-11-08
Status: DONE. Holding momentum names through earnings has not paid: mean reaction -0.78% (t=-1.13, n=142), with 14.8% of events closing 8%+ down (through a stop). Not significant, so not a rule; but the evidence leans toward selling before. Prediction committed first (8e7b315).
Audience: Nolan, TARS sessions

## Why now, and why not items 2 or the R15 task

- R15 task: skipped. R16 trigger (b) can't be verified OFF: no high-water-mark
  rebase row exists after the 10/15 R6 drawdown halt, and PLTR (11/2) and
  NVDA (11/5) both closed at a loss on stops within 5 days (owner positions;
  if R6 counts them, the circuit breaker runs to about 11/10).
- Item 2 (Options Apprentice Stage 2): still blocked; paper/history/owner_trips.json
  has not been committed.
- Item 4 is live-relevant: BE (10/22) and ASX (10/15 pre-market gap) both
  went straight through their stops on news, and the book holds names
  reporting soon.

## Data

- Earnings dates and timing: paper/history/earnings_reports.json (8 names)
  plus earnings_reports_wide.json (33 names, fetched 2026-11-08 via
  Robinhood get_earnings_results; trailing up to 8 quarters each, so about
  2024-2026 only). About 300 events at most. This is a 2-year sample.
- Prices: daily_ohlcv*.json.

## Test (fixed before running)

- Event day: for "am" reports the reaction is close(d-1) -> close(d); for
  "pm" it's close(d) -> close(d+1). "Sell before" exits at the last close
  before the reaction; "hold" keeps the position through it.
- Momentum names: at the pre-reaction close, close > 200-day SMA AND 12-1
  momentum > 0 (the live screen's core). Others are the control.
- Measures, per event: reaction return R (the gap day), the share of events
  where R would have gone through an 8% stop (R <= -8%), and post-event drift
  over the next 20 trading days (does a sell-before investor miss it?).
- Hold-through value = mean R (that's what selling before forgoes). With
  stops, the downside is capped only if there's no gap; the gap is the point.
- Splits: momentum vs not; first year vs second year; megacaps vs the rest;
  t on per-event R. Bootstrap the mean with 10,000 resamples clustered by date.

## PREDICTION

- Momentum names' mean reaction R between -0.5% and +1.5%, |t| < 2
  (earnings gaps are close to fair bets; there's a small positive drift in
  the literature for winners, e.g. post-earnings drift).
- About 10-15% of momentum-name events gap 8%+ against the holder (through
  the stop), more for the volatile names than for the megacaps.
- No reliable difference between momentum names and the rest (|t| < 2).
- Verdict expected: neither rule is clearly better on mean; selling before
  only cuts tail risk. That makes it a sizing question, not an edge, which goes
  to Nolan as information.

## Results (python3 paper/research_scripts/earnings_hold.py)

251 usable events, 41 names, 2025-01 to 2026-08 (40 skipped: no price
history, or no 20 days after). 2 years only; in-sample; price returns.
Two data checks: the wide file was hand-transcribed by the worker, and
PLTR and BAC were spot-checked against Robinhood live: they match. A smoke
run on the original 8 names was seen after the prediction commit and before
the full data (n=56; same direction).

| Group | n | Reaction mean (t) | 90% bootstrap (by date) | Close <= -8% | Open <= -8% | 20d drift after (t) |
|---|---|---|---|---|---|---|
| All | 251 | -0.64% (-1.16) | -1.60 .. +0.32 | 17.1% | 13.1% | +4.05% (+4.41) |
| **Momentum names** | 142 | **-0.78% (-1.13)** | -2.06 .. +0.46 | **14.8%** | 8.5% | +2.24% (+2.04) |
| Other names | 109 | -0.47% (-0.51) | -2.03 .. +1.13 | 20.2% | 19.3% | +6.40% (+4.18) |
| Momentum, 1st half | 68 | -0.79% | | 17.6% | 8.8% | +3.27% |
| Momentum, 2nd half | 74 | -0.76% | | 12.2% | 8.1% | +1.29% |
| Momentum, megacaps | 21 | +0.55% | | 9.5% | 4.8% | +0.61% |
| Momentum, non-megacaps | 121 | -1.01% (-1.32) | | 15.7% | 9.1% | +2.52% |

Momentum minus other reaction: -0.31pp, Welch t=-0.27.
Worst momentum events by name (mean over few events, read with care):
UPST -18.7% (1), RIVN -7.9% (3), MARA -6.7% (1), HOOD -6.3% (3), COIN -6.0%
(2), NFLX -5.8% (4).

## Reading it

- For a name TARS holds, the earnings day was a slightly NEGATIVE bet:
  -0.78% on average, the same in both years (-0.79 / -0.76), not
  significant (t=-1.13, bootstrap interval spans 0).
- The cost of holding is mostly the tail: about 1 in 7 momentum events
  closed 8%+ down on the reaction day, and 1 in 12 OPENED there, which is
  below the stop before it can act (BE 10/22 is one). Megacaps were much tamer
  (4.8% gapped through), the volatile names much worse.
- The 20-day drift after the event is positive (+2.2%), but it comes
  AFTER the reaction, so a seller-before can rebuy and still get it. 2025-26
  was a rising market, so part of that drift is just the market (not
  separated here).
- Practical: there's no evidence that holding through earnings earns
  anything. There's clear evidence it adds gap risk the 8% stop can't
  control. The live screen already skips entries with earnings within 3 days.
  The open question is exits: sell the close before and rebuy after the
  reaction if still eligible. Untested as a full rule (it needs a backtest
  with longer earnings history than 8 quarters per name). Goes to Nolan as
  information, not a rule change.

## Hurdles

Split halves: same sign and size. Megacaps dropped: holds (-1.01%). Walk-
forward: not meaningful on 2 years of quarterly events (about 18 events per
window). t >= 2: not met. So: a consistent lean, not a proven edge.

## Prediction scorecard

- Momentum mean reaction between -0.5% and +1.5%, |t| < 2: **WRONG** on
  the mean (-0.78%, below the band); right on |t|.
- About 10-15% gap 8%+ against: RIGHT (14.8% at the close; 8.5% at the open).
  More for volatile than megacaps: RIGHT (15.7% vs 9.5%).
- No difference momentum vs the rest: RIGHT (t=-0.27).
- Neither rule clearly better on mean; selling before cuts tail risk: RIGHT,
  though the mean also leans toward selling.
