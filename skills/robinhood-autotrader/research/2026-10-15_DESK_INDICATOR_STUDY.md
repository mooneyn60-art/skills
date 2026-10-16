# Desk Indicator Study — what each SPY Live Desk tool actually predicts

TARS self-study of every indicator and pattern on the SPY Live Desk, on real SPY 1-minute bars.

Last Updated: 2026-10-15
Status: in-sample findings; nothing promoted to live rules
Audience: Nolan, TARS, research swarm

## Overview
- Data: 31 sessions of real (non-interpolated) SPY 1-minute bars, 2026-09-02 → 2026-10-15 (today partial). Same definitions as `paper/datafarm/live_desk.html`.
- Method: every time an event fires (09:45–15:30 ET), measure the SPY move 15 and 30 minutes later in the direction the idea predicts. Stats clustered by day (t over day-means), and split into first/second half of days. Script: `paper/research_scripts/desk_study.py`, output `paper/datafarm/desk_study.json`.
- About 45 tests were run, so ~2 would pass |t| ≥ 2 by luck alone. Anything that "passed" is a candidate for forward testing, not a rule.

## Findings
| Tool | Result (30-min unless noted) | Verdict |
|---|---|---|
| EMA 9/21 cross, follow (1m, 5m) | −0.04 / +0.03 pts, 47–48% | No edge. On 1-min it's slightly worse than a coin flip. |
| Close crosses VWAP, follow | ≈ 0.00 pts, 50% | No edge alone (it's a location, not a signal). |
| Trend state turns on (VWAP + EMAs agree) | ≈ 0.00 pts | No edge alone. |
| FVG forms, follow (1m) | bull −0.47 pts, 38% (t −1.9) | Chasing a fresh 1-min gap tends to buy the top. |
| FVG first retest, bounce | 1m bull −0.39, 1m bear ≈ 0; 5m mixed | No edge. Gaps hold the wick (1-min gaps only get fully pierced 4–6% of the time on the retest bar) but the bounce doesn't pay. |
| Price tags ±2σ VWAP band, fade | 1m: no; 5m +2σ fade +0.06 pts at 15m, t 2.0, n=16 | Too few to trust. |
| RSI(14) < 30 on 1m, buy | **+0.17 pts, 57%, t 2.3; both halves positive** | Best candidate. Forward-test. |
| RSI(14) > 70 on 1m, fade | +0.01 / −0.03 pts | No edge. The dip-buy works, the top-short doesn't (it's been an up-drift market). |
| Equal highs/lows *broken* (close through), follow | −0.01 / −0.05 pts, 44–49% | No edge. Most "breaks" of small pools go nowhere. |
| Equal lows *swept & reclaimed*, long | +0.79 pts, 82%, n=11 | Strong but tiny sample. Same idea as sweep_reversal. |
| Equal highs swept & reclaimed, short | +0.33 pts, 75%, n=24 (t 0.9) | Leaning right, not proven. |
| ORH/ORL break or sweep | ≈ 0, n 3–21 | No edge yet. |
| PDL broken (close below), short | **+0.79 pts, 76%, t 2.1, both halves positive**, n=17 | Candidate. Small n. |
| PDH broken, long | −0.11 pts | No edge. |
| Fibonacci 50% / 61.8% first touch, bounce | −0.58 / −0.41 pts, 22–35% (worse than a coin flip) | **No edge — and "random" 45%/70% levels behaved the same.** The first touch of a pullback level usually means the pullback keeps going. Confirms the 20-year test: Fib levels aren't special. |
| First-hour direction → rest of day | 14/30 same direction | Coin flip. Morning direction says nothing about the afternoon. |

### Time of day (median SPY move over 15 minutes)
09:30–10:00 0.56 pts · 10:00–11:00 ~0.45 · 11:00–12:00 ~0.35 · 12:00–15:30 0.15–0.29 · 15:30–16:00 0.26.
With an ATM 0DTE delta ~0.5 and theta around −$1.1 per contract-day midday, a typical midday 15-minute SPY move (~0.25 pts) is worth ~$0.12 per share in premium, about the same as what time decay takes over 1–2 hours. **Midday 0DTE scalps need above-normal moves to beat decay; the first 90 minutes is where the movement is.**

## What I learned (plain)
1. Most chart indicators are *descriptions*, not *predictions*. VWAP, EMAs, trend state and FVGs tell you where you are; on their own, none of them called the next 15–30 minutes better than chance.
2. The things that showed signs of an edge are all "**failed move**" ideas: price stretched down (RSI < 30) bounces; a sweep of equal lows that closes back inside reverses. Breakouts and chasing gaps did worse.
3. Fibonacci: no. Treat those lines as ordinary reference levels.
4. Timing matters more than pattern for 0DTE: movement is front-loaded, decay isn't.
5. Sample is 31 days. Everything here is in-sample and needs forward data.

## Next
- Add `rsi30_dip_1m`, `pdl_break_short` and `eql_sweep_reclaim` to the next weekly freeze of the paper trader (not midweek: rules hash is frozen). Forward-test for ≥4 weeks.
- Re-run this study every Friday as more real minute bars accumulate (`FRIDAY_DATA_REFRESH` JOB 4).
- Desk: show the expected 15-minute move for the time of day, and feed these findings to Ask TARS.
