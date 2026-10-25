# Intel playbook

Desk id: `intel`. Absorbs: Analyst, Scout, Trend Hunter, Forecaster, Lab. Read this before every run and append lessons after.

## Read first
- research/26 math
- research/28 virality
- research/34 vidIQ playbook
- tools/stats.py, tools/rivals.py
- data/experiments.csv, data/forecasts.csv

## Rules (proven)
- YouTube Analytics lags 2-3 days; always say which dates a number covers. Use engagedViews for comparisons.
- Baseline 10/19-24: Shorts feed 4,547 views, 40% engaged, 130% average view; myth Shorts peak at about 780 views.
- vidIQ files our channel under Lifestyle/Entertainment (reaction legacy) until Studio keywords are fixed.
- Metricool TikTok analytics returned zeros until TikTok is reconnected; do not report zeros as real.
- Follow-up rule: a Short at 3x the median gets 3 follow-ups plus a Part 2 within 48 h.
- Score yesterday's forecasts against actuals every evening.

## KPIs this desk owns
- Forecast accuracy
- Experiments concluded per week
- Breakouts spotted within 24 h

## Lessons log (newest last; date, what happened, what we learned, the number)
- 2026-10-24: desk created by merging the roles above.
- 2026-10-24 (marketing desk): vidiq_trending_videos (Shorts, vph, after 10/17) with titleQuery "animal facts myths" returned 0 videos at 0 credits; "animal facts" returned 15 (5 credits). Use 1-2 word titleQueries. Top risers: VN danger Shorts (decapitated snake still bites 898K/19K subs, 101 s), lioness-saves-cub story (632K/34K, 163 s), FurrFact "Animals No Animal Dares to Hunt" (306K, 95 s). 90-160 s English and Vietnamese lead vph again.
- 2026-10-24 forecast: all six 10/25-10/26 YouTube Shorts still open on the "True or false?" quiz card (no animal at frame 0), so the hook test can't separate them; ranked by topic class instead. Both originals (shrimp, tiger) already hold the 1 PM slots. Score these in data/forecasts.csv on 10/27-10/28.
- tiktok_music_trending (tiktok-correct5): 0 tracks again (7DAY). Third empty pull, so stop retrying until Nolan confirms the connector is the Business/CML account.
- 2026-10-24 (evening): one vidiq_user_videos call with all three videoTypes (5 credits) replaces separate shorts/long pulls (10). Metricool YTEV01/02/05/06 give subscribers, views and subs gained/lost for free (lags ~3 days). TikTok TKPO/TKEV07 for 10/17-24 came back as one zero row after the reconnect.
- 2026-10-25 (night lab, 30 credits): Shorts outliers for cartoon animal facts are mostly meme skits; the edu breakouts on IG/TikTok are "why" animated explainers (Dachshunds 443x, T. rex 10.3x at 62 s, cat meows 2.2M). vidiq_watch_shortform_content (10 credits) gives shot timings and exact VO; two watches were enough to see the pattern. Format search (embeddingType "format") surfaces structure better than concept.
- 2026-10-25 (marketing desk, 5 credits): vidiq_outliers Shorts, keyword "dangerous or gross animal facts explained", maxSubs 500K, sort breakoutScore: 14 hits. Top: "Giraffes Can't Lie Down Too Long!" (CuteAnimalsUS, 11.7M, 916x, 60 s); "The secret to a cat's lightning reflexes" (18.8K subs, 1.9M, 72x, 35 s); "Is this kind of fox dangerous?" (1.1M, 30x, 21 s); "Never Put Your Hand in a Sea Turtle's Mouth" (1M, 22x, 16 s). Patterns: body-limit claims ("X can't do Y"), "Never do X with Y" warnings, "the secret to" pet superpowers. Next trend pull (10/26) alternates back to IG/TikTok outlier search.
