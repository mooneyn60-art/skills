# How the Meatball Town agent adopts Channel Brain

For the Mayor. Do this in your next run; it takes one run.

1. `git fetch origin claude/package-installation-setup-yv4j79` and copy `skills/channel-brain/` from that branch into
   your branch as `skills/oh-meatball/brain/` (tools/scan.py, tools/abtest.py, SKILL.md). Copy KNOWLEDGE.md and
   SELF_REVIEW.md to `skills/oh-meatball/` and keep growing them there.
2. In TOWN.md, under "How a run talks", add a step 0:
   > **0. Scan first.** Read brain/SKILL.md. Run `python3 skills/oh-meatball/brain/tools/scan.py skills/oh-meatball`.
   > Fix the top 3 issues you're allowed to fix (brain/SKILL.md "Act, don't ask") before any production, and post what you fixed.
3. Fix what the first scan found (2026-10-24):
   - CRITICAL: Shorts and TikTok slots in the next 48 h missing from posted.csv. Fill them, or log the ones already in Metricool.
   - CRITICAL: 0 subscribers from ~5,700 views in 7 days. Start the numbered series with a subscribe reason as ONE experiment.
   - Experiments: give the 4 date-only rows E-numbers, renumber the duplicate E3-E6, and pause all but one Shorts test.
   - Stale docs: rewrite or delete routines/DAILY.md, NIGHTLY.md and WEEKLY.md (old branch, retired story format,
     "Never mention cars"), and the "Oh Meatball Pt" parts of SKILL.md.
   - Make OPERATIONS.md, the routine prompts and `CADENCE` at the top of scan.py agree (TikToks: 3 or 4 a day?).
4. Keep `CADENCE`, `CURRENT_BRANCH` and `RETIRED` at the top of scan.py current. When Nolan points out something
   the scan missed, add a check for it.
5. Post one `decision` on the square saying Channel Brain is adopted, and tell Nolan in your summary.
