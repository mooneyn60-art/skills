# TARS Connections — how what I know links up

A map of every tested finding: what it connects to and what decision it changes. The brain's version of association: one fact pulls the related ones into view.

Last Updated: 2026-10-16
Status: active (Nolan: "use that brain I gave you and update that to make it better also more connections")
Audience: TARS

## Overview
Findings live in KNOWLEDGE.md; this page links them. Each node: the finding (✓ held in both halves, ✗ failed). Links:
- → feeds: where it's used.
- ⇄ agrees with: another finding pointing the same way.
- ⚡ conflicts with: another finding pointing the other way.
When two findings agree, trust both a bit more. When they conflict, say so out loud (BRAIN habit 2).

## The web

### Day-level leans (known by 9:30)
- ✓ **Expiry Friday leans down** (−0.21%, up 38%). → Edge board, day score (opex weight −0.09). ⇄ day score. ⚡ the dip-buy setup, which buys calls on a falling day (both 10/16 losses).
- ✓ **Day score** (logit; ≥0.60 up 65%, <0.45 up 46%). → Edge board. ⇄ the expiry, 20-day-stretch and gap findings, which are its inputs. ✗ adding other stocks, bond rates, put/call or Asia: no better tails (predict_lab2).
- ✓ **VIX sets size and lean** (range 0.66% → 2.72%; under 15: +0.13%/day). → Edge board, option sizing (a bigger range means a bigger stop distance). ⇄ the expected-move row on the desk.
- ✓ **Big days partly reverse** (after <−1%: +0.16 to +0.22% next day). → Edge board. ⇄ the day score's "intra1" weight (−0.08): a big prior-day gain lowers the score.
- ✓ **Gap size**: small gaps fill 71-77%, gaps over 1% fill 24%. → Edge board, gap row. ⇄ S1 (big gaps run). ⇄ pool odds (prior close is a pool).
- ✓ **Gains come overnight** (+0.029%/night vs +0.020%/day). → Edge board. ⚡ buying intraday calls at all. → research: test an overnight slot.

### Intraday (10:30-14:30, the slot's window)
- ✓ **Pool odds** (which pool gets hit first; calibrated 10/30/50/71/90 → 9/27/52/69/88). → desk ▲/▼ tag, first target.
- ✗ **Next-hour model** (9 intraday inputs + day score): no edge in either half. The day score sorts days, not hours.
- ✗ **Dip-buy setup as traded** (−0.11 pts, 39% wins). ✗ Dip-buy × day score: still negative at score ≥0.50 (n=106, −0.07). ⚡ expiry Fridays.
- ~ **Gap-up setup × day score** (20y proxy): score ≥0.55, +0.24%/+0.06% (n=118/212). Score <0.50: too few to say. Weak support for the gap-up setup only when the score isn't low.
- ✗ BOS/CHoCH, sweeps, ORB, squeeze, VWAP ±1σ fades, buying pressure, time of day, intraday momentum, day of week. → shown on the desk as "tested, no edge", so neither of us chases them.

## How a decision runs through the web (before any order)
1. Which rule fires? (the veto)
2. Pull the connected leans: Edge board tally, day score, VIX, expiry, gap.
3. If two or more leans point against the trade → say it plainly and propose skipping. Under current rules I can't skip a firing setup on leans alone; changing that is Nolan's call.
4. After it settles, score it (PREDICTIONS.jsonl) and update the links: a lean that keeps being wrong gets ✗.
