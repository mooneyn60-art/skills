---
name: scoreboard
description: Read how Meatball Myths videos are doing on YouTube and TikTok and turn it into a decision, with the source of every number. Use this for the daily scoreboard, any "how did it do", "check the numbers", "why did views drop", "did that work" question, a scheduled read of a test, or before changing the queue because of performance. It lists which data source answers which question, including the ones that are easy to forget.
---

# Scoreboard: which number comes from where

Read-only unless a rule in `skills/channel-brain/MASTER_ORDERS.md` says a result triggers a change (a winner at twice its group's median gets a sequel within 48 hours; a failed slot gets refilled). The read dates and pass marks for running tests are in MASTER_ORDERS; check them first so a test is read on its day and not early. Run commands from `skills/oh-meatball`.

Nolan wants the result in one or two short lines with the source, and what could not be measured said plainly. The detail goes in a research file.

## YouTube
| Question | Source | How |
|---|---|---|
| Public views now, age | yt-dlp flat listing | `yt-dlp --flat-playlist -J https://www.youtube.com/channel/UCw98RQD81t_339LX5EJqcrg/shorts` (and `/videos`). Views are rounded to two digits above 1,000. Never open watch pages from this machine. |
| Did it post, its video id | Metricool | `getScheduledPosts`, brand `7521392`, one or two days per call; published posts carry `publicUrl`. |
| Views, engaged views, average % viewed, likes, shares, subscribers gained, per video per day | Windsor.ai, connector `youtube` | fields `video`, `video_title`, `date`, `views`, `engaged_views`, `average_view_percentage`, `shares`, `subscribers_gained`, `creator_content_type`. Two to three days behind. |
| Where the views came from (Shorts feed, search, suggested, subscribers) | Windsor.ai, field `traffic_source` | combine with `video`, `views`, `engaged_views`. Search share shows which titles earn search; the engaged share inside `SHORTS` shows whether feed viewers stayed. First used 11/12. |
| Who watches | Windsor.ai | `viewer_age_group`, `viewer_gender` with `viewer_percentage`; `country` with `views`. |
| Retention curve, impressions, click-through, "shown in feed", swipe-away | not available here | Studio only (a screenshot from Nolan), or vidIQ's retention report at 5 credits a video once credits reset. |

Reading rules that hold (research 90): a Short gets about 90% of its views on day 0, so judge it at 12 to 15 hours against about 1,000 views; an engaged share under 0.39 in the first days means viewers swiped; tiny views with a normal share means it was not shown. Compare a Short with its own style and topic group, never with all videos, and never read a gap of 100 to 200 views: public counts are rounded.

## TikTok
| Question | Source | How |
|---|---|---|
| Views, likes, comments, shares per post | Metricool analytics, or the public page | `python3 tools/postkit.py ttpage URL ...` |
| TikTok's category label, its suggested searches, review or penalty flags, the AI label | public page | same command (`labels`, `suggested_words`, `is_reviewing`, `penalty`, `aigc_label_type`). One request per video, no loops. |
| Watch time, finish rate, For You against Search | not available here | TikTok Studio only (ask Nolan for one screenshot when a test depends on it). |

Baselines (research 91, 81 posts): median 229 views, middle half 196 to 316, likes 2.2%, comments 0.05%, shares 0.06%.

## Writing it up
- A dated file `research/NN-scoreboard-MMDD.md`: answer first, then tables, then "Could not measure". Rows as CSV in `research/data/`.
- Every number with its source and its age (hours since posting, or the last data day).
- Say what would settle an open question and who can get it.
- Then the queue check: gaps, a creature twice in a day, anything off the current direction. Fix what a standing order covers; put anything bigger to Nolan as options with the numbers.
- Commit and push; update MASTER_ORDERS when a read changes a rule.
