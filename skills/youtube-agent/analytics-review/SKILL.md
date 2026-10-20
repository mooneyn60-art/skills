---
name: analytics-review
description: Run the 48-hour and 7-day performance review for Oh Meatball uploads, log rows to data/metrics.csv, apply the decision rules, and check the day-30 kill/pivot/scale criteria. Use when asked how videos are doing, for a weekly review, stats, what's working, or whether to pivot.
---

# Analytics review (48 h + 7 d)

Benchmarks and kill criteria: [algorithm.md §5](../../oh-meatball/playbook/algorithm.md) (Benchmarks, Kill / pivot criteria).
Log file: [data/metrics.csv](../../oh-meatball/data/metrics.csv). Judge batches of 10+, not single uploads (§0 rule 4).

## 1. Pull numbers
- Metricool: `getAnalyticsAvailableMetrics` (network youtube) then `getAnalyticsDataByMetrics` for views, likes,
  comments, shares, subscribers per post.
- vidIQ (if connected): `vidiq_channel_videos` (shorts), `vidiq_video_stats` per id.
- Viewed vs. swiped and avg % viewed are Studio-only (Shorts -> Analytics -> Engagement): ask the human to paste them.
- Free fallback for public views: `python3 -m yt_dlp --flat-playlist -J https://www.youtube.com/channel/UCw98RQD81t_339LX5EJqcrg/shorts`

## 2. Log (append one row per video per checkpoint; never overwrite)
Existing header — keep it exactly:
```
date,platform,part,video_id,age_h,views,viewed_vs_swiped,avg_pct_viewed,likes,comments,shares,subs_gained
2026-10-22,youtube,raccoon_doorbell,ZX2QGuq_ROI,48,<views>,<viewed%>,<avg%>,<likes>,<comments>,<shares>,<subs>
```
- `part` = clip slug (animal_twist). `age_h` = hours since publish (log at ~48 and ~168).
- Percentages as plain numbers (71 = 71%). Leave a cell empty if unknown; don't guess.
- Keep the per-clip attributes (camera, animal, twist type, hook #, length) in the plan JSON from
  [weekly-plan](../weekly-plan/SKILL.md) so you can join on the slug.

## 3. Decision rules
| Signal (48 h) | Read | Action |
|---|---|---|
| Viewed vs swiped < 50% | hook/frame 1 failed | new hook formula ([hooks](../hooks/SKILL.md)); trim dead air |
| Viewed 60-75% but avg % viewed < 70% | middle sags | shorter (8-10 s), move twist earlier |
| Avg % viewed >= 100% | loop works | reuse the loop ending pattern |
| Views >= 3x channel median | outlier | 3-5 *variations* (same character, new twist), not copies |
| Views >= 10k engaged | scale | variations + feature as #1 in the Saturday compilation |
| Many "fake/AI" comments | debate = engagement | reply with [reply-drafts](../reply-drafts/SKILL.md), pin the disclosure-friendly comment |
At 7 d: rank the week by Viewed %; double down on the top 20% tuples (animal/camera/twist), drop the bottom 20%.

Current baseline (2026-10-20): realistic raccoon doorbell 904 views/13 h vs obvious-AI beaver 2/17 h
([research/14](../../oh-meatball/research/14-pivot-satisfying-ai.md)). Channel median is tiny, so score new clips
vs our own median, the same way [virality](../virality/SKILL.md) scores others.

## 4. Day-30 check (or earlier if triggered) — from algorithm.md §5
- **Pivot content**: after 40+ distinct Shorts, median engaged views < 100 AND Viewed < 55% on most.
- **Fresh channel**: Viewed >= 65% but impressions stay tiny AND the same clips do better on TikTok/Reels.
- **Kill format**: < 100 median views on all platforms after 40+ clips.
- **Stop immediately**: any inauthentic/reused-content notice, any Community Guidelines strike, or YouTube auto-applies
  an AI label we didn't set.

## Output
```
Week 43 review (12 Shorts, 1 comp)
Median views 48 h: 310 (prev 9) | Viewed %: 68 | Avg % viewed: 92
Top: raccoon_return 2.3k (7.4x median) -> 3 variations queued
Bottom: deer_lens 40 (Viewed 41%) -> hook rewrite, drop "deer x doorbell"
Day 30 status: day 12, no trigger
```
