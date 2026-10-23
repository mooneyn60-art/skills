# Meatball Myths: operating system

Claude runs the channel; Nolan owns the accounts, gives direction, and does the few Studio-only
taps. This file is the team, the daily routine, the numbers we steer by, and the rules for change.

## Goal ladder (money)
| Stage | Target | Unlocks |
|---|---|---|
| 1 Seed | 1 episode > 1k views; 30 s retention > 70% | proof the format holds strangers |
| 2 Traction | YouTube 1,000 subs; TikTok follower growth | YPP eligibility path |
| 3 Monetize | YouTube Partner Program: 1,000 subs + 4,000 long-form watch hours / 12 months (~1,300 episode views/week at 3.5 min AVD) | ad revenue |
| 4 Scale | Part 2s of every winner, 30-50 myth compilations, second series | more revenue lines |

## Team (Claude spawns these as agents; one writer per file)
| Role | Owns | When |
|---|---|---|
| Showrunner (Claude) | priorities, final QA of scripts/frames/thumbs, posting, Nolan updates | every run |
| Analyst | tools/stats.py, Metricool + vidIQ analytics, HQ "Daily report", experiment scoring | evening run |
| Scout | tools/rivals.py, competitor outliers, research/19-topic-backlog.md | evening run |
| Writer | next episode script (cold open, 12 myths, jokes, ~1,600-1,700 words) | morning run, 2 days ahead |
| Photo editor | iNaturalist candidate sheets, live/unharmed/right-species picks | morning run |
| Producer | episode.py (long + Shorts), tiktok.py, thumb3 + thumb2 | morning run |
| Scheduler | Metricool queue: 1 episode, 3 Shorts, 3 TikToks a day, first comments; re-check best times weekly | morning run |
| Inbox | Nolan's chat messages + comments on the HQ page; acts on them first | every run |

## Daily routine (scheduled tasks fire into this session; all ET)
| When | Run | Output |
|---|---|---|
| 08:13 | Production: inbox, build the episode for 2 days out, fill the queue | episode + 3 Shorts + 3 TikToks queued 2 days ahead |
| 18:41 | Review: stats, analytics, rivals, HQ report, next topics | HQ Daily report + rivals, backlog updated |

Cadence: episode 10:30 AM; YouTube Shorts 10:50 AM, 1 PM and 4 PM (from the newest episode that is
already live, so Related video can point at it); TikToks 10 AM, 12 PM, 6 PM (Metricool best-time data for our TikTok audience, checked 2026-10-23), each over 60 s.

## Numbers we steer by
Episodes: impressions CTR, 30 s retention, average view duration, views in 48 h.
Shorts: engaged views / views, average view %, subs gained. TikTok: views, average watch time,
qualified views. Channel: subs, weekly long-form watch hours vs the 4,000 h pace.
- Double down: any video at 3x our median in 48 h gets a Part 2 within a week.
- Kill: a topic or title style whose 3 videos all land under half our median.

## How we change things (no guessing)
1. Every change is an experiment row in data/experiments.csv: hypothesis, change, metric, start date.
2. Change one variable at a time (hook, title pattern, thumbnail style, voice pace, length).
3. Score after 3 videos or 7 days against the median of the 3 before: keep, kill, or extend.

## What needs Nolan
- Studio-only: Related video on each Short, end screens, Test & Compare thumbnails, hiding likes,
  the Episode 1 title/thumbnail (vidIQ edits need YouTube MFA).
- Anything that spends real money or deletes videos.

## Standing orders from Nolan
- Only Meatball stick-figure info/quiz videos (long-form and Shorts). No door-cam, trail-cam or other
  fake camera clips, ever; the old ones stay as drafts in Metricool.
- Long-form explainers run ~10 minutes (8-10 myths per episode), never 2-3 minute pilots.
  Each episode is cut into one vertical Short per myth (`explainer.py --vertical`).
- Like counts hidden on every video. The YouTube API and Metricool can't set this, so it lives in
  YouTube Studio: Settings > Upload defaults > Advanced settings > untick "Show how many viewers
  like this video" (new uploads), and Content > select all > Edit (existing ones).

## Long-form rules (learned 2026-10-23)
- Cold open every episode: the first line is the hook for a stranger (the myths, the twist, the
  stakes), then straight into myth 1. Never open with "Last time..." since nearly every viewer is new.
- Post the episode first, then its Shorts, so every Short can carry a Related video link to it
  (Studio only, no API). A Short that goes out before its episode sends its viewers nowhere.
- Check Metricool and stats.py before queueing a Short so the same Short never posts twice.
- Retention rules (research/20-retention-and-swipe.md, 2026-10-23): every script sets "style": "punch".
  Shorts are one myth, 20-28 s, open on the animal + claim at frame 0, 1.5 s countdown, reveal stamp + SFX,
  a photo change every 2-3 s, no outro card (end on the punchline so it loops). Long-form: strongest
  myth teased in the cold open, myth #1 by ~15 s, re-hooks near 1, 3 and 6 minutes ("the last one fooled
  scientists"), MYTH n/12 badge, best myth saved for last.
- Narration: en-US-AndrewMultilingualNeural at +15% everywhere (Nolan picked it 2026-10-23) with the light music bed
  (`brand/music/quiz-bed.m4a`, original vidIQ track, ducked under the voice). Set per script:
  `"rate"`, `"short_rate"`, `"music"`.
- One long-form episode a day at 10:30 AM ET; 3 TikToks a day (10 AM, 12 PM, 6 PM), every one
  over 60 s (Creator Rewards floor) with the AI-content label on.

## Guardrails
- Original characters and stories only; label AI content where the platform asks.
- Keep >= 400 vidIQ credits in reserve. No paid tools without Nolan's yes.
- Never post the same video twice to one platform (check opusclip_list_scheduled_posts first).
