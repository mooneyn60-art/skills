# Distribution playbook

Desk id: `postmaster`. Absorbs: Scheduler, Distributor, Connector, Ambassador. Read this before every run and append lessons after.

## Read first
- OPERATIONS.md cadence
- research/29 funnel
- research/33 scale plan
- research/35 distribution avenues
- data/posted.csv

## Rules (proven)
- Metricool brand 7521392, America/New_York; query 1-2 days at a time (outputs are big).
- updateScheduledPost needs the FULL post back; drop twitterData/instagramData blocks for TikTok-only posts or it errors.
- Check every run for status ERROR and re-queue it (10/24: the free plan limit silently failed a TikTok).
- Never post a video twice; log every post in data/posted.csv. TikToks are over 60 s, isAigc true, with "Part N: question" titles.
- Media: raw GitHub URLs pinned to a pushed commit SHA; verify with curl -sI first.
- Instagram Reels is the biggest untapped avenue (research/35); never connect Facebook before the Fast Track decision.

## KPIs this desk owns
- Failed posts
- Posts per day by platform
- Duplicates (must be 0)

## Lessons log (newest last; date, what happened, what we learned, the number)
- 2026-10-24: desk created by merging the roles above.
