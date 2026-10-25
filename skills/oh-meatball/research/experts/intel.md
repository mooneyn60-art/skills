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
- **Every evening: long-form retention (research/47).** For each long-form older than 48 h, pull vidiq_channel_analytics report=audience_retention (filters video==ID; 5 credits each). Log every drop of 5+ points in data/retention.csv with the line on screen at that time (script timeline or a whisper of ep.mp4) and its cause. Send the top drop cause to the Showrunner, so the next script and tools/retention.py thresholds adapt.

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
- 2026-10-25 (evening): vidIQ analytics for "last 7 days" really covers ~10/18-10/23 (2-3 day lag), so it shows none of the v3/v4 Shorts; use stats.py public counts for anything under 72 h. Public Shorts +6,065 in 24 h (v3/v4: Portia ~1.1k/7 h, cassowary ~1.1k/9 h, ghost crab ~770/4 h). Median public Short 717. Metricool TikTok post data stops at 10/24 23:04 and returns no watch time.
- 2026-10-25 (Retention desk, 20 credits): only gFhrONKK0rI (2:15 quiz pilot) has a retention curve. 11 viewers; drops at 0:02 quiz card, 0:04 answer given, 0:14 agenda line (biggest), 0:18, 0:28, 0:46, 1:12. RwbgzQisvYM and Uqj0QL8G0d4 return no Analytics rows yet (lag). The dimensions video + creatorContentType can't be combined (the call errors at 0 credits); identify long-forms by AVD/AVP-derived length instead.
- 2026-10-25 (Sunday Summit): Analytics still lags 2-3 days, so no v3/v4 Short has a curve; daddy longlegs audience_retention returned 0 rows (5 credits wasted; check top_videos first and only pull curves for IDs it lists). Goldfish curve is the baseline to beat: 0.74 at 47%, 0.38 at 75%. Weird niche: Mike the Headless Chicken 2.7M/363x, Napoleon chess robot 6.4M/202x; 'cold war secrets' +91% search, comp 42.
