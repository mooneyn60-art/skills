# 62 · vidIQ findings: BLOCKED on credits (2026-11-02)

This session was meant to run the vidIQ pass: the TikTok breakdown, the 11/5 Azorian title scores, and outlier research for both lanes. **It could not run any of it.** This page records the blocker, the free data it did get, and the exact call plan for when credits exist. No numbers below come from paid vidIQ calls. Nothing was rendered, scheduled or changed in Metricool.

## 1. Credit balance (vidiq_balance, 2026-11-02)

| Bucket | Now | Max |
|---|---|---|
| Renewable | **0** | 2,000 (resets **2026-11-24 14:30 UTC**) |
| Add-on | **3** | 1,120 |
| **Total** | **3** | |

Every call needed for this task costs 5 or more (title score 5, keyword research 5, outliers 5, short-form watch 10). **3 credits buy zero calls.** The 2,000 renewable credits were spent before this session; the job list shows ~20 `vidiq_watch_shortform_content` runs on 10/26-10/27, so probably there.

**Free calls made (0 credits):** balance, user_channels, jobs_list, bookmarks_list, two job polls.
- user_channels: Meatball Myths has **976 subs, 33,645 views, 48 videos** (24 subs short of YPP's 1,000). The account also has StoneMindStoic (54 subs).
- Bookmarks: none saved.
- The two past watch jobs I polled were other creators' videos (an IG eye-colour explainer and a T-Rex TikTok by @lilpotatestiktok), not the @vibecodingiseasy video. Its ID (7701822100725566750) is newer than every job in the list, so it has never been analysed.

## 2. What to decide now without vidIQ (title for Thu 11/5, 5 PM ET)

Research 61 already made this call from web evidence; vidIQ scoring would only confirm or reorder it.
- **Test & Compare: (a), (b), (c).**
  - (a) "Why the CIA Says "We Can Neither Confirm Nor Deny"" is the angle none of the big Azorian videos lead with (fern 5.57M, Dark Docs 1.41M, Megaprojects 840K).
  - (b) "The CIA Built a Fake Mining Ship to Steal a Soviet Sub" uses actor + verb + absurd object.
  - (c) "Project Azorian: The CIA's Giant Claw Heist" carries the search term.
- **Drop (d).** "Part of" weakens it, and it nearly copies fern's 5.57M title.
- These are **not vidIQ-scored.** If credits arrive before Thursday, scoring all four costs 20 credits (section 3, step 2).

## 3. Call plan when credits exist (~80 credits, highest value first)

Run in this order and stop when credits run out. Channel ID for scoring: `UCw98RQD81t_339LX5EJqcrg`.

| # | Call | Credits | Why first |
|---|---|---|---|
| 1 | `vidiq_watch_shortform_content` url=`https://www.tiktok.com/@vibecodingiseasy/video/7701822100725566750` (the full URL; the tool rejects /t/ short links) | 10 | Nolan asked for it directly |
| 2 | `vidiq_score_title` ×4 (a-d), type=long, channelId above | 20 | Time-boxed: needed before Thu 11/5 |
| 3 | `vidiq_keyword_research` keyword="project azorian" (research) | 5 | Checks that (c) carries real search volume |
| 4 | `vidiq_outliers` keyword="bugs living in your house", maxSubscribers=200000, publishedWithin=sixMonths, limit=25 | 5 | House-bug lane outliers |
| 5 | `vidiq_outliers` keyword="declassified CIA operation", maxSubscribers=200000, publishedWithin=sixMonths, limit=25 | 5 | Case-file lane outliers |
| 6 | `vidiq_keyword_research` mode=rising, niche="house bugs and insects" | 5 | Topic demand, lane 1 |
| 7 | `vidiq_keyword_research` mode=rising, niche="declassified history cold war" | 5 | Topic demand, lane 2 |
| 8 | `vidiq_outliers` contentType=short, same two keywords | 10 | Shorts-side outliers for both lanes |
| 9 | `vidiq_comment_insights` mode=validate on the top 2 picks per lane | 20 | Only if credits remain |

**Getting credits:**
- **Before 11/5:** buy an add-on pack in vidIQ (Nolan's call; it costs money). About 35 credits cover steps 1-3.
- **Free:** wait for the 2,000-credit reset on 11/24, then run the whole plan in one session.

## 4. Not done here (and why)

- **TikTok breakdown, title scores, outliers, top-5 topics:** all need paid vidIQ calls. Pulling them from web search instead would break this session's brief ("use vidIQ for all of this") and MASTER_ORDERS' once-a-week research limit (research 61 already ran today).
- No renders, no scheduling, no Metricool changes. The style lock was respected: no new looks were proposed.
