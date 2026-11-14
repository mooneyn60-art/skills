# Live Momentum Screen vs SPY: Does It Beat Just Holding the Index?

One-line: The live momentum screen matches SPY on return (+0.33pp over
20 years, +2.3pp over 5) with far smaller drawdowns, but it fails every
hurdle for BEATING SPY. Its live record is 3 winners in 12, -0.43R average.

Last Updated: 2026-10-25
Status: DONE. The screen is NOT shown to beat SPY: walk-forward 3-4 of 9, halves flip, daily t below 0.3, and without megacaps it trails SPY by 6pp (LONG). What it really does is cut drawdowns (-17% vs -56%). Prediction committed first (7c7d2ba); every line scored RIGHT.
Audience: Nolan, TARS sessions

## Overview

Last week's swarm (research/2026-10-18_MOMENTUM_SCREEN_SWARM.md) found no
variant better than the live screen. It didn't test whether the screen
itself beats SPY. Since 10/01 the whole equity book is this screen, with no
index core ("drop the spy, I want to beat it not ride it", Nolan 10/01).
So the question that matters is whether it does.

## Test (fixed before running)

- Harness: paper/research_scripts/mom_screen_base.py, baseline as is (12-1,
  above the 200-day, vol <= 80%, 2 per sector, 8 slots, 15% cash, stops by R4,
  5bp per side, next-open fills).
- Benchmarks: (1) SPY buy-and-hold, price only; (2) 85% SPY + 15% cash,
  rebalanced daily, which matches the screen's cash floor.
- Universes LONG (14 names, 2007-2026) and WIDE (41 names, 2021-12 on).
- Hurdles: split halves; 9 walk-forward windows (screen ahead of SPY in >= 5);
  drop the megacaps; t on the daily return difference (screen minus SPY) >= 2.
  Bonferroni bar for calling it an edge: |t| >= 3.9.
- Live: every closed momentum_satellite / rebalance_momentum trade in
  paper/trades.jsonl with a planned_risk, scored in R.

## PREDICTION

- LONG: screen minus SPY within +/-2pp CAGR. Daily t between -1 and +1.
  Walk-forward ahead of SPY in 4-5 of 9. Megacaps dropped: the screen trails
  SPY by more than 4pp (2.99% vs 8.94% CAGR is already in last week's run).
- WIDE: screen ahead of SPY by 0-4pp; daily t < 1.5.
- Against 85% SPY: the screen looks slightly better than against SPY, but
  still t < 2.
- Live trades: mean below -0.3R, n under 15, so it means nothing either way.
- Verdict: the screen is NOT shown to beat SPY. If so, that goes to Nolan as
  information (his call), not as a rule change.

## Results (python3 paper/research_scripts/mom_screen_vs_spy.py, data through 2026-10-22)

Backtests: in-sample, mechanical, price returns, survivorship-biased names.

| Cut | Screen CAGR / maxDD | SPY CAGR / maxDD | Diff vs SPY | t | Diff vs 85% SPY |
|---|---|---|---|---|---|
| LONG full 2007-2026 | 9.27% / -17.3% | 8.94% / -56.5% | +0.33pp | -0.26 | +1.45pp (t +0.19) |
| LONG 1st half | 7.88% | 4.70% | +3.19pp | +0.23 | +3.61pp |
| LONG 2nd half (2016-26) | 10.58% | 13.35% | **-2.77pp** | -0.72 | -0.90pp |
| LONG megacaps dropped | 2.97% | 8.94% | **-5.97pp** | -1.82 | -4.84pp |
| WIDE full 2021-12 to 2026 | 13.74% / -23.6% | 11.45% / -25.4% | +2.30pp | +0.26 | +3.89pp (t +0.54) |
| WIDE 1st half | 2.03% | 6.13% | -4.10pp | -0.42 | -3.39pp |
| WIDE 2nd half | 24.72% | 17.02% | +7.70pp | +0.67 | +10.24pp |
| WIDE megacaps dropped | 15.57% | 11.45% | +4.12pp | +0.45 | +5.71pp |

Walk-forward, screen minus SPY by window: LONG +26.2 -17.2 +0.2 -3.3 +5.2
+0.1 -9.3 -1.3 -6.8 (**4 of 9**); WIDE +3.8 -13.2 -7.0 -10.6 -31.6 +50.3 -15.1
-16.9 +40.0 (**3 of 9**).

Note on LONG full: CAGR is higher but the mean daily difference is slightly
negative (t -0.26). The screen holds about 15% cash and sits out of
downtrends, so it avoids SPY's volatility drag. Its edge in CAGR comes from
not falling 56% in 2008, not from picking better.

### Live trades

The ledger has a numeric planned_risk for only 3 of the sleeve's closed
trades (RVMD -1.03R, GH -1.01R, MU -0.19R by the ledger's figure; the desk
logged MU as -1.12R, so the ledger's MU risk value looks wrong). The desk's
own R figures in routines/HOURLY_TRADING_CHECK.md cover 12 closes:
RVMD -1.03, GH -1.01, MU -1.12, HPE -1.0, ASX -1.72, ATI -0.51, TECK -0.10,
ILMN -0.62, NVT -0.64 (the last four closed by the owner), HALO +1.29 (half),
VLO +1.0, FRO +0.25. That's **n=12, 3 winners, mean -0.43R.** That's far too
few to judge, and it fits the backtest's 31% win rate with a long right tail
that hasn't shown up yet.

## Verdict

- Against the hurdles for "beats SPY": split halves FLIP on both universes;
  walk-forward 4/9 and 3/9 (bar 5/9); daily t never above +0.7 (bar 2);
  without megacaps on 20 years it trails SPY by 6pp. **Not shown to beat SPY.**
- What holds up: much smaller drawdowns on LONG (-17% vs -56%), in both
  halves (-16.9% / -17.3%). That's what a 200-day filter plus stops is
  known to do (KNOWLEDGE: "every approach reduces drawdown, none raises
  return", now eight families).
- For Nolan's 10/01 goal ("I want to beat it not ride it"): the evidence
  says this screen rides about level with SPY with less pain, and doesn't
  beat it. The 2016-26 decade, the closest to today's market, has it
  -2.8pp a year behind SPY. That's information for his decision, not a rule
  change. The screen stays as is unless he says otherwise.
- Data fix for the desk: 9 of 12 sleeve closes have no numeric
  planned_risk in trades.jsonl, and MU's looks wrong. Without it, the
  monthly audit can't score the sleeve.

## Prediction scorecard

Every pre-committed line came out RIGHT: LONG within +/-2pp (+0.33),
t in -1..+1 (-0.26), 4-5/9 (4), megacaps trail by > 4pp (-5.97); WIDE
0-4pp ahead (+2.30), t < 1.5 (+0.26); vs 85% SPY slightly better but t < 2
(+0.19 / +0.54); live mean below -0.3R (-0.43R desk, -0.74R ledger), n < 15;
not shown to beat SPY. A full sweep is unusual here. The cause is that
these predictions were conservative null calls, so this isn't evidence
that I'm well calibrated.
