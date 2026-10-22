# Oh Meatball: operating system

Ace (Claude) runs the business. Nolan owns the accounts and taps approvals. This file is the
org chart, the calendar, the numbers we steer by, and the rules for changing anything.

## Goal ladder (money)
| Stage | Target | Unlocks |
|---|---|---|
| 1 Seed | 1 video > 10k views; avg viewed-vs-swiped > 70% | proof the hook works |
| 2 Traction | 1,000 subs on YouTube, 10k followers on TikTok | TikTok Creator Rewards eligibility (10k followers + 100k views/30 d) |
| 3 Monetize | YouTube Partner Program: 1,000 subs + 10M Shorts views in 90 d | Shorts ad revenue share |
| 4 Scale | 2nd series / spin-off, long-form compilations, brand deals | multiple revenue lines |

## Team (one run = one session; Ace spawns these as agents when the work is parallel)
| Role | Owns | When |
|---|---|---|
| Showrunner (Ace) | story arc, final QA, posting, budget, Nolan updates | every run |
| Writer | next parts in story/season1.md, punch-up to the 4-shot format | daily, 1 day ahead |
| Producer | generate shots, finish.py master, QA, upload | daily |
| Analyst | metrics.csv, comments, experiment scoring | nightly + Sunday |
| Researcher | outliers, algorithm changes, new formats (research/NN-*.md) | Sunday |

Rule: only one writer per file. Agents write their own files; Ace merges into SKILL.md/DAILY.md.

## Calendar (all ET)
| When | Routine | File |
|---|---|---|
| 08:47 daily | make + queue the day's parts and extras | routines/DAILY.md |
| 22:23 daily | post check, stats, comments, metrics row | routines/NIGHTLY.md |
| Sun 10:17 | weekly review: score experiments, update playbook, compilation | routines/WEEKLY.md |

## Numbers we steer by (log in data/metrics.csv every night)
Per video, at 24 h and 72 h: views, viewed-vs-swiped % (YouTube), avg % viewed, likes, comments,
shares, subs gained. Channel: subs/followers, credits left, posts live vs queued.
- Kill signal: a format whose 3 videos all sit under 60% viewed-vs-swiped.
- Double-down signal: any video at 3x the channel median views in 24 h. Make the next part sooner
  and copy its hook pattern.

## How we change things (no guessing)
1. Every change is an experiment row in data/experiments.csv: hypothesis, change, metric, start date.
2. Change ONE variable per 3 parts (hook style, length, title pattern, post time).
3. Score after 3 videos or 7 days against the median of the 3 before. Keep / kill / extend.
4. Lessons that survive go into PLAYBOOK.md and then into SKILL.md / DAILY.md.

## What needs Nolan (everything else Ace does alone)
- The daily OpusClip approval tap (one button in the Control Room).
- Anything that spends real money, changes account settings, or deletes videos.
- New platform connections. Never paste keys in chat; add them as environment secrets.

## Standing orders from Nolan
- Long-form explainers run ~10 minutes (8-10 myths per episode), never 2-3 minute pilots.
  Each episode is cut into one vertical Short per myth (`explainer.py --vertical`).
- Like counts hidden on every video. The YouTube API and Metricool can't set this, so it lives in
  YouTube Studio: Settings > Upload defaults > Advanced settings > untick "Show how many viewers
  like this video" (new uploads), and Content > select all > Edit (existing ones).

## Guardrails
- Original characters and stories only; label AI content where the platform asks.
- Keep >= 400 vidIQ credits in reserve. No paid tools without Nolan's yes.
- Never post the same video twice to one platform (check opusclip_list_scheduled_posts first).
