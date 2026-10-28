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
- 2026-10-24 (marketing desk): getBrandSettings shows only TikTok (MeatballMyths) and YouTube are connected, with no IG/Pinterest/Threads, so I reminded Nolan. Metricool updateScheduledPost worked for YouTube-only Shorts when I sent the full post without twitterData/instagramData. The response re-adds them, which is harmless. New ids: koala 405106378, bats 405106434. Two door-cam bear drafts (draft:true) still sit on the 10/25 and 10/26 4 PM YouTube slots. They won't publish, but delete them in the Metricool app to avoid accidents.
- 2026-10-24 (evening): 10/24-26 queue had 0 ERROR posts and full cadence. Retitled 4 queued bare-question Shorts to claim titles via updateScheduledPost (full post resent, times read back unchanged; ids change, uuids stay). The 10/24 10 PM TikTok is a ~25 s Short, under the 60 s Rewards floor: check length before filling TikTok slots from Shorts.
- 2026-10-25 (marketing desk): Metricool 10/24 12:00-10/25 23:59 has 0 ERROR posts. Published since 10/24 noon: YT elephant, daddy longlegs, cassowary, Portia; TikTok hippo, sloth, spiders, cassowary, tarantula hawk. 10/25 queue: YT Shorts 13:00, 15:00, 16:00, 17:30, 19:30 + explains-01 at 14:00; TikTok 13:30, 16:30, 18:00, 19:00, 20:00, 21:30. Old quiz posts (shark/cat TikToks, bats/shrimp/hippo YT, 10/25 myths-04 long-form) are draft:true and won't publish.
- 2026-10-25 (evening): 0 ERROR posts across 10/24 18:43-10/27 18:43. Caught a 73.2 s render (v4-spiders bolas) in the 19:30 YouTube Shorts slot by ffprobing the Metricool media URL; set it to draft (406058249) and kept the TikTok copy as the 60 s+ deep dive. Lesson: check render length, not just slot coverage; scan.py check 7 now does it for the next 3 days.
- 2026-10-25 (Sunday Summit): firefly (11/10 13:00, now 406096936) and arctic tern (11/10 16:00, now 406096991) YouTube Shorts were 65-67 s renders; set to draft, dates read back, moved to held.csv. Refill both 11/10 slots with 20-25 s v4 kit Shorts. Before scheduling any file, ffprobe it: a short-* name is not proof of length.
- 2026-10-28 (marketing desk): Instagram/Facebook/Threads/Pinterest crossposting is retired (Nolan: YouTube + TikTok only); the "Instagram Reels is the biggest untapped avenue" rule above is obsolete, never remind Nolan. No Metricool post touched today (lead: other helpers are swapping media and moving times; ids change on every update). Scan: the 10/28 16:00 YouTube Short slot has no posted.csv row (today's ledger: 09:30, 13:00, 19:00, 21:30). Not filled or verified in Metricool here; left for the postmaster run that owns the queue.
