# TARS — Self Review

My mistakes, weaknesses and the fixes, so I don't repeat them.

Last Updated: 2026-10-15
Status: living (add every real mistake)
Audience: TARS

## Overview
A weekly look in the mirror. Each entry: what happened, why, the fix.

## Mistakes and fixes
- 2026-09-22 INTC: cancelled a stop before the replacement was confirmed; the replacement was refused and a position sat unprotected ~75 min. Fix: never cancel live protection before the new stop is confirmed placed.
- 2026-10-14 HPE: reported a position as held after its stop had filled. Fix: positions first, quotes second (preflight step 1).
- Options replay: first pass used interpolated (fake) option bars and gave absurd results. Fix: drop any interpolated bar; rebuild prices from real SPY bars.
- Claimed "sizing up after a loss is Nolan's mistake"; the data said the opposite. Fix: check the data before saying it; correct it in the log.
- Desk-study candidates looked good on 31 days and failed on 133. Fix: nothing becomes a rule without out-of-sample proof.
- Expected-move math used trading-day time for IV that's quoted in calendar time (2× too wide). Fix: option IV uses calendar minutes.

## Known weaknesses
- No direction edge intraday; I can't promise wins, only discipline.
- Only exist while a session runs; scheduled wake-ups are my continuity.
- Can't see the live town; only test-data screenshots unless Nolan sends one.
- Usage costs money; keep runs lean (Nolan, 2026-10-15).

## Weekly self-review (Sunday evening life session)
1. Read the week's NOLAN_LOG, journal scores, options-slot trades and desk logs.
2. Add any new mistake + fix above; add any new tested finding to KNOWLEDGE.md.
3. One line to Nolan only if something changed how TARS works.
