---
name: reply-drafts
description: Draft replies to YouTube comments on Oh Meatball videos, including "it's fake / AI" comments, turning them into engagement without ever claiming the footage is real. Use when asked to answer comments, draft replies, or handle a comment section.
---

# Reply drafts (it drafts, you decide)

Replying in the first hour lifts early engagement ([algorithm.md §4 Comment bait, §5 Days 4-30](../../oh-meatball/playbook/algorithm.md)).
Pinned-comment templates live in [seo-packaging.md §5c](../../oh-meatball/playbook/seo-packaging.md). Drafts only:
the human approves before anything is posted.

## Get the comments
- vidIQ connected: `vidiq_video_comments` (video id) or `vidiq_comment_insights` for themes.
- Otherwise paste them in. Never post automatically; `vidiq_reply_to_comment` only after explicit approval of each reply.

## Hard rules
1. **Never claim it is real.** No "100% real", "my actual camera", "this happened". The clips are AI fiction.
2. Don't argue. One reply per thread, max 2 sentences, at most 1 emoji.
3. No engagement bait ("like if…", "comment 1 if…"). Questions are fine.
4. Ignore/hide spam, links, slurs; don't reply to hostile users more than once.
5. No promises you can't keep ("Part 2 tomorrow") unless it is in [weekly-plan](../weekly-plan/SKILL.md).

## Reply types
| Comment type | Goal | Template |
|---|---|---|
| "Fake" / "AI" / "this is AI slop" | own it, redirect to the craft | "Yep, AI 🍝 We try to make them as realistic as possible. What gave it away for you?" |
| "Is this real?" | honest + curiosity | "It's AI-made (see the label). Which part looked most real to you?" |
| "LOL" / emoji | keep them talking | "The second raccoon is my favorite. Did you spot him before the light came on?" |
| Story / name idea | turn into a future video | "Adding 'moose + dashcam' to the list. What should he do?" |
| Criticism of realism | thank, ask specifics | "Fair. Was it the paws or the motion? Helps us fix the next one." |
| Animal-welfare worry | reassure | "No animals involved at all, it's fully AI. He's a digital raccoon 🦝" |
| Request for more | point to the series | "New ones every day at 10 AM + 4 PM ET, compilation on Saturday." |

## Output format
```
@user1: "this is so fake lmao"
  -> "100% AI 🍝 We go for max realism, what gave it away?"   [type: fake]
@user2: "name him Gerald"
  -> "Gerald it is. Gerald returns Thursday."                 [type: idea; only if planned]
@spam: "check my channel"                                      [skip]
```
Collect recurring comment themes (best guesses, requested animals) and pass them to
[weekly-plan](../weekly-plan/SKILL.md) as idea seeds.
