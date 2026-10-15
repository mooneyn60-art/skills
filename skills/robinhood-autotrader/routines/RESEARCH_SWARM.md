# Research Swarm (queen-led)

One-line: How the weekend research block runs several hypothesis tests in
parallel with one coordinator ("queen") and a small team of worker agents.

Last Updated: 2026-10-15
Status: ACTIVE. Used by routines/WEEKEND_RESEARCH.md.
Audience: TARS research sessions.

## Overview

Nolan asked (2026-10-15) to use the queen-agent pattern from the ruflo repo
(mooneyn60-art/ruflo, plugins/ruflo-swarm) to research faster. Running
ruflo's own CLI is blocked in this environment (third-party code), so the
pattern is implemented with Claude Code's built-in Agent tool. Same shape:
one queen holds the plan and the verdict, specialised workers do the
legwork in parallel, a skeptic re-checks the winner, and findings go into
shared memory so the next run starts from them.

RESEARCH ONLY. No agent in the swarm places, cancels or changes an order,
and no swarm result changes a live rule without Nolan's yes.

## Roles

| Role | Who | Model | Job |
|---|---|---|---|
| Queen | the research session itself | session model | Picks the question, writes predictions BEFORE any test, assigns one variant per worker, merges results, writes the note |
| Worker (x3 max) | Agent tool, general-purpose | sonnet | Tests exactly ONE variant with paper/engine.py and the four hurdles; returns a data table, no conclusions |
| Skeptic (x1) | Agent tool, general-purpose | sonnet | Re-runs the best-looking variant from scratch with its own code and tries to break it (other split, drop megacaps, costs doubled) |

Keep the team at 4 agents or fewer. More agents add cost, not rigor.

## Steps

1. Read research/SWARM_MEMORY.md (shared memory) and the last ~25 lines of
   notes/NOLAN_LOG.md.
2. Queen writes the question, the variants and a numeric prediction for
   each into the research note BEFORE spawning anyone. Commit it.
3. Spawn the workers in ONE message so they run in parallel. Each prompt
   must contain: the variant spec, the data file paths, the four hurdles
   (mechanism, split sample, 9-window walk-forward, drop the big winners)
   and R14 ("print data, not conclusions"). Workers write their scripts to
   paper/research_scripts/ and return the raw table.
4. Queen reads every table. Pick the best variant ONLY if it beats the
   baseline on CAGR AND passes all four hurdles AND |t| >= 2.
5. Spawn the skeptic on that variant. If the skeptic's rerun disagrees,
   the variant is dead.
6. Write the note (full-strength failures included), append one line per
   variant to research/SWARM_MEMORY.md, record the run's cost, commit, push.
7. A surviving variant is a PROPOSAL to Nolan, never an adopted rule.

## Budget guard

Target: under $25 of model usage per swarm run.
- Workers and skeptic use sonnet, never opus.
- Before spawning the skeptic, check this session's cost
  (get_session with no id -> external_metadata.usage.cost_usd). If the
  run has already used $20+, skip the skeptic and mark the result
  UNVERIFIED.
- Log each run in research/SWARM_COSTS.csv: date,question,agents,cost_usd.

## Queue (take the top unfinished item)

1. MOMENTUM SCREEN VARIANTS (requested 2026-10-15). Baseline = the live
   screen (12-1 month momentum, above the 200-day, 63-day vol <= 80%, max 2
   per sector, 8% stops raised by R4). Variants, one per worker:
   a. Pullback entry: same ranking, but buy only after a 3-8% dip from the
      20-day high while still above the 50-day.
   b. Lookback: 6-1 month momentum instead of 12-1.
   c. Sector rotation: rank sectors by 6-month momentum, pick names only
      from the top 3 sectors.
   Data: paper/history/daily_ohlcv.json, daily_ohlcv_volatile.json,
   daily_ohlcv_holdings.json. Note the survivorship bias in all three.
2. Range-regime exit rule (the standing open question in WEEKEND_RESEARCH).
3. Earnings-gap continuation for momentum names (hold through vs exit
   before earnings), using paper/history/earnings_reports.json.
