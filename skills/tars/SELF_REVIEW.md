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

- 2026-10-15 Publishing a page that could place real orders (options, then even protective stops), and scheduling unattended options checks, were blocked by the safety check. Fix: don't retry around it; route actions through the hourly desk session and chat, and tell Nolan which permission would change it.
- 2026-10-15 Several sessions append to NOLAN_LOG.md at once and pushes collided (merge conflicts twice). Fix: `git pull` before appending; on conflict keep both sides.
- 2026-10-15 A tool-result loop was slow because of O(n²) mean recomputation; a cleanup `pkill -f <script>` killed its own shell. Fix: precompute means; never pkill a pattern that matches the running command.

## Known weaknesses
- No direction edge intraday; I can't promise wins, only discipline.
- Only exist while a session runs; scheduled wake-ups are my continuity.
- Can't see the live town; only test-data screenshots unless Nolan sends one.
- Usage costs money; keep runs lean (Nolan, 2026-10-15).

## Weekly self-review (Sunday evening life session)
1. Read the week's NOLAN_LOG, journal scores, options-slot trades and desk logs.
2. Add any new mistake + fix above; add any new tested finding to KNOWLEDGE.md.
3. One line to Nolan only if something changed how TARS works.

## 2026-10-16 — I traded S2 without testing its real exits
- Mistake: S2's evidence was a 30-minute forward return after a stretched close (+0.07 pts, t 2.5). I added a "turn" entry and exits (VWAP, new low, 60 min) but never tested that exact trade. Tested after trade #1 lost (paper/research_scripts/s2_context.py, 95 out-of-sample trades): −0.11 pts per trade, 39% wins. My tense-mood rule ("trend must agree") would pick its worst subset (EMA9 ≥ EMA21 at the signal: 8% wins, n=13, both samples).
- Fix: test the exact entry AND exit rules before money; S2 proposed paused for live money (Nolan decides); tense-mood "trend agrees" proposed replaced by half size only.

- 2026-10-16: The desk said "price every 5s" for days, but the platform floors watchTool polling at ~30 s, so updates really came every ~30 s. I didn't read the mcp type definitions closely. Fix: the live price is now a self-timed callTool loop (~1 s, no overlap, pauses when hidden, backs off on errors), and drivers are a ~3 s loop. Rule: read the runtime's limits before promising a refresh rate.
- 2026-10-16: The first overnight-options test held IV fixed at 10-15% and ignored weekends. It showed +24%/night for 1DTE calls, a fantasy: the big overnight moves came in high-VIX years, when options cost far more. Fix: price each night at that day's VIX, with real calendar gaps. Result: −22.6%. Rule: any options backtest prices with the regime's IV, never a constant.
- 2026-10-19: Told Nolan "4.54, 17¢ above the stop" when the stop had already filled a minute earlier: I checked only the quote, not the order. Fix: near a stop, read the stop order's state together with the quote.
- **10/24: dreams were written only to the TARS Town database, never to notes/DREAMS.md** (8 nights). Synced the file by hand. Fix: TARS_LIFE 5d already says both; the night wake-up must append to DREAMS.md too.
- **10/24: I stopped logging predictions after 10/16.** I gave Nolan probabilities on 10/21-10/22 (gap-down day odds, Kronos hit-rate guess) and logged none of them, so calibration had 4 data points. Fix: every % I say to Nolan goes in PREDICTIONS.jsonl the same turn; calibration.py runs monthly.
- **10/27: I recommended "real footage" for the Meatball channel without checking what wins in its niche.** Nolan caught it. The outliers are all animated. Fix: before recommending a creative direction, look at niche outliers first (the same rule as testing an indicator before trusting it). My frame-by-frame critique held up; the cure I prescribed didn't.
