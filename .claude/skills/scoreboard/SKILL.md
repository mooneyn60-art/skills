---
name: scoreboard
description: Read how Meatball Myths videos are doing on YouTube and TikTok and turn it into a decision, with the source of every number. Use for "how did it do", "how are we doing", "what are the numbers", "check the numbers", "why did views drop", "did that work", "is it working", "did it go out", "did it post", "view jail", "any winners", the daily scoreboard, a scheduled test read, or before changing the queue because of performance. It lists which data source answers which question.
---

# Scoreboard: which number comes from where

Read-only unless a rule in `skills/channel-brain/MASTER_ORDERS.md` says a result triggers a change (a pet or survival Short at twice its group's median gets a sequel within 48 hours, a bug winner gets none; a failed slot gets refilled). The read dates and pass marks for running tests are in MASTER_ORDERS; check them first so a test is read on its day and not early. Run commands from `skills/oh-meatball`.

Nolan wants the result in one or two short lines with the source, and what could not be measured said plainly. The detail goes in a research file.

## YouTube
| Question | Source | How |
|---|---|---|
| Public views now | yt-dlp flat listing | `yt-dlp --flat-playlist -J https://www.youtube.com/channel/UCw98RQD81t_339LX5EJqcrg/shorts` (and `/videos`). Entries are newest first and have no upload date, so no age. Views are rounded to two digits above 1,000. Never open watch pages from this machine. |
| Age of a video | Metricool or Windsor | Metricool `publicationDate` for the id, or Windsor `published_at` (UTC) once the video has data. |
| Did it post, its video id | Metricool | `getScheduledPosts`, brand `7521392`, one day per call, dates with the offset: `fromDate 2026-11-11T00:00:00-05:00`, `toDate 2026-11-11T23:59:59-05:00`, `timezone America/New_York`. Real posts have `draft:false`; published ones carry `publicUrl`. Rows with `draft:true` are old leftover drafts (status PENDING in a past slot): ignore them, they are not failed slots. |
| Views, engaged views, average % viewed, likes, comments, shares, subscribers gained, per video per day | Windsor.ai, connector `youtube` | fields `video`, `video_title`, `date`, `views`, `engaged_views`, `average_view_percentage`, `likes`, `comments`, `shares`, `subscribers_gained`, `creator_content_type`, `published_at`. Two to three days behind: the last day with data is `max(date)`. No rows for a video younger than 3 days is normal, not an error; use the public count and the Metricool publish time until it appears. Windsor `views` for a day is not the public lifetime count. |
| Where the views came from (Shorts feed, search, suggested, subscribers) | Windsor.ai, field `traffic_source` | One call per video: fields `traffic_source`, `views`, `engaged_views` (add `date` for per-day), filter `[["video","eq","<id>"]]`. Never put `video` in the fields with `traffic_source`: it comes back null. The id is not echoed back, so write it down yourself. Without the filter you get the channel total. Engaged share = `engaged_views` / `views` per source. Search share shows which titles earn search; the engaged share inside `SHORTS` shows whether feed viewers stayed. |
| Who watches | Windsor.ai | `viewer_age_group`, `viewer_gender` with `viewer_percentage`; `country` with `views`. |
| Long-form watch hours (the 4,000 h goal) | Windsor.ai, connector `youtube` | fields `video`, `video_title`, `estimated_minutes_watched`, `views`, `average_view_percentage` over the whole date range (the field is in Windsor's list, checked 11/12; two to three days behind). Keep only the long-form ids (`data/posted.csv`, episodes named `longform-*`). Cross-check in Metricool `getAnalyticsDataByMetrics`: network `youtube`, connector "all videos", metrics `videoId`, `title`, `watchMinutes` (it includes Shorts, so pick the long-forms by id). Append to `data/longform-hours.csv` (date, video id, minutes, hours to date) and write the running total in hours against 4,000, with the source named. |
| Retention curve, impressions, click-through, "shown in feed", swipe-away | not available here | Studio only (a screenshot if Nolan offers one; it is not asked for, see MASTER_ORDERS "Open asks"), or vidIQ once credits return on 11/24. |

Reading rules that hold (research 90): a Short gets about 90% of its views on day 0, so judge it at 12 to 15 hours against about 1,000 views (from the public count and the Metricool publish time, because Windsor is days behind); an engaged share under 0.39 in the first days means viewers swiped; tiny views with a normal share means it was not shown. Compare a Short with its own style and topic group, never with all videos, and never read a gap of 100 to 200 views: public counts are rounded.

## TikTok
| Question | Source | How |
|---|---|---|
| Views, likes, comments, shares, saves per post | public page | `python3 tools/postkit.py ttpage URL... --csv data/tiktok-stats.csv`. Run it on every scoreboard run, so a time series builds up. Take the URLs from Metricool `publicUrl`. One request per video; it stops at the first "no page data" (do not retry in a loop). `plays` means views. `ttpage` prints each video's age in hours (from `created`, UTC). |
| TikTok's category label, its suggested searches, review or penalty flags, the AI label | public page | same command; the plain output shows only the counts, the first label and "TikTok suggests", so read the `flag` ("reviewing" or "penalty N") and `ai_label` columns of the `--csv` file, or add `--json OUT` for these keys: `labels` (first label is the category, for example "Comics & Cartoon, Anime"), `suggested_words`, `is_reviewing` (true = under review), `penalty` (a set of numeric codes; `display_penalty_type` "0" and `is_reviewing` false means no flag seen; what each code means is unverified), `aigc_label_type` ("1" is what our 11/11 test post showed while `is_aigc` read false, so read `aigc_label_type`, not `is_aigc`; a change from "1" is the thing to report). |
| Watch time, finish rate, For You against Search | not available here | TikTok Studio only (a screenshot if Nolan offers one), or Windsor `tiktok_organic` once Nolan has approved the link (MASTER_ORDERS, open ask 1): check `get_connectors` on every run, and if it is there call `get_fields` for `tiktok_organic` and pull watch time, full-watch rate and impression sources per video. |

Baselines (research 91, 81 posts): median 229 views, middle half 196 to 316, likes 2.2%, comments 0.05%, shares 0.06%.

## Why did views drop
Pull SHORTS views by date and by video (Windsor, one call per video), put them next to the posting days and times from Metricool, and compare feed against search and the engaged share (under 0.39 means viewers swiped; 0.40 or more with tiny views means YouTube did not show it). Say which part Windsor cannot show yet (the last 3 days).

## Writing it up
- A dated file `research/NN-scoreboard-MMDD.md`: answer first, then tables, then "Could not measure". Rows as CSV in `research/data/`.
- Every number with its source and its age (hours since posting, or the last data day).
- Say what would settle an open question and who can get it.
- Then the queue check: gaps, a creature twice in a day, anything off the current direction. Fix what a standing order covers; put anything bigger to Nolan as options with the numbers.
- Commit and push; update MASTER_ORDERS when a read changes a rule.

## The one-screen page (Nolan's pick, 11/12)

Nolan has a private scoreboard page for his phone. Its link is in the daily scheduled task's prompt and in chat, never in this repo. The page reads one file, `board.json`; refresh it at the end of every scoreboard run:

1. Update `skills/oh-meatball/data/board/notes.json` by hand if something changed: the long-video hours (value, window, as_of, source), the read dates (same list as MASTER_ORDERS "Read dates and live tests", in plain words), the one open ask (an empty `asks` list hides that card).
2. From `skills/oh-meatball`: `python3 tools/postkit.py ttpage URL ... --csv data/tiktok-stats.csv` for the last 7 days of TikToks (the page's TikTok counts are the newest row per video), then `python3 tools/board.py`. It prints the medians and how many titles it could not match to `data/posted.csv`.
3. Upload the file to the page: `Artifact` publish with `url` = the page link, `file_path` = `skills/oh-meatball/data/board/board.json`, `asset: true`. The result gives a new `/_blob/<id>`.
4. Point the page at it: `ArtifactData` `list` on collection `datasets` (note each `version` and the old blob id in `source.url`), then one `batch` of six `update` writes (doc ids `kpis`, `recent`, `queue`, `dates`, `asks`, `stamp`), each with `if_version` and data `{"source": {"url": "/_blob/<new id>"}, "updated": {"at": "<UTC now>", "by": "Claude"}, "edit": {"via": "claude", "at": "<UTC now>"}}`.
5. Delete the old file: `Artifact` delete with the page `url` and `path` = the old blob id.
6. Commit `data/board/` and `data/tiktok-stats.csv`.

The page itself (`tools/board_page.html`, stored in the page as `files/index.html`) changes only when its layout does: read the Dashboard type's own guide first (`Artifact` read, path `SKILL.md`), test with a stand-in `dash` object at 400 px wide, then `ArtifactData` set `files/index.html` to `{"text": <the file>}`. Every number on the page is a cell of `board.json`, so new arithmetic goes in `tools/board.py`, not in the page.
