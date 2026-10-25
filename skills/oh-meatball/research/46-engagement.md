# 46 · Engagement: more comments and subs per view (Growth desk, 2026-10-25)

Nolan: "We need to fish more like comments and subs." Then, mid-run: "do it in the beginning so people will actually be watching."
Rules held: no wrong facts as bait, no invented comments, no promises we won't keep, no sub4sub language.

**Credits: 15 vidIQ** (channel_analytics 5, outliers ×2 = 10; one get_videos_by_ids call failed and cost 0). Balance 680 → 665.

## 1. Measured (YouTube Analytics, 10/11-10/25, dimension = video)

The Analytics API lags about 2 days, so the 10/23-10/25 Shorts (goldfish 932, elephant 877, daddy longlegs 730 public views
on 10/24, data/views.csv) are **not in this report yet**. What it does contain:

| Video | Views | Comments | Likes | Subs | Subs / 1k | Comments / 1k | Ending / ask style |
|---|---|---|---|---|---|---|---|
| Sharks in the RIVER?! (Ufg_uKRnh_Y), v1 quiz Short | 623 | 0 | 11 | 1 | **1.61** | 0 | quiz loop + "Did you guess right? Comment ✅ TRUE or ❌ FALSE" |
| Ostriches bury heads? (sp_lZedjjF4), v1 quiz Short | 456 | 0 | 6 | 1 | **2.19 (best)** | 0 | same |
| Porcupines (SHQ2FzL-9Vc), v1 quiz Short | 437 | 0 | 3 | 0 | 0 | 0 | same |
| Camel myth (fNmRjqYh3Aw), v1 quiz Short | 110 | 0 | 0 | 0 | 0 (worst, tied) | 0 | same |
| vMnZ8kBdLRY (no longer public; vidIQ can't resolve it) | 87 | 1 | 1 | 0 | 0 | **11.5 (best)** | unknown |
| Everything You Know About Animals Is WRONG (gFhrONKK0rI), long-form | 9 | 1 | 1 | 0 | 0 | 111 (1 comment, "First 😎") | score-out-of-12 ask |
| 30 other rows (old/private uploads) | 77 total | 0 | ~0 | 0 | 0 | 0 | |
| **Channel** | **1,799** | **2** | | **2** | **1.11** | **1.11** | |

What drove it (honest read, tiny sample):
- **Subs came only from the two quiz Shorts with the biggest reach** (sharks, ostrich). One sub each, so 1.6-2.2 per 1k is noise-level;
  the research/42 target is ≥ 3 per 1k. Nothing we post asks for the subscribe *with a reason* inside the video.
- **Comments are near zero.** The only on-topic viewer answer we have (research/comment-readouts.md) came from the **binary,
  emoji-tappable ask** on the owl quiz ("Comment ✅ TRUE or ❌ FALSE" → "True 🎉🎉"). Open questions ("Who told you this as a kid?",
  "What's the heaviest thing you've ever pulled?") have drawn nothing. Binary + emoji is the only ask style with a hit.
- Every ask we make sits at the **end** of the Short, after most viewers have swiped. Shorts retention falls steadily through the
  video, so a 3-6 s ask is seen by far more people than a 20 s one.

## 2. Rivals (vidiq_outliers, Shorts, ≥50k views, last month)

- Comment-bait that works in animal/kids Shorts is a **pick-one or guess question in the title or on screen from the start**:
  "Guess which one is correct🤔" (1.7M, 22x), "Who's the REAL King of the Jungle?" (938K, 59x), "Choose 5 Animals To Defend You"
  (1.6M), "Bear vs Gorilla: One Move Could Change Everything!" (1.7M, 96x), "Which Animal Has the Strongest Punch?" (352K).
- The ask is part of the premise (viewers answer *while* watching), not a tag-on at the end.
- The outlier tool doesn't return comment counts, so this is the ask *shape*, not measured comment rates.

## 3. What we changed

1. **Ask kit in tools/v3.py (v4 Shorts)** — beat fields `ask` and `sub`, sample `episodes/ask-kit/short-raven-askkit.mp4`:
   - 0-3 s: hook only.
   - ~3-6 s: **guess-first card** ("WHY FAKE IT? 🦹 FOOL THIEVES / 🎭 JUST FOR FUN", voiced "Guess before I tell you."). The Short
     then answers it, which also builds suspense.
   - ~6-9 s: **subscribe pill**: Meatball points down at the follow button, red SUBSCRIBE pill pops and is pressed with a click,
     voiced with a concrete, true reason ("Subscribe. I face a new animal every day." — we post new animals daily).
   - Before the loop: one-line reminder card "GUESSED RIGHT? 👇". The last frame still matches frame 0 (mean diff 3.1/255).
   - The gate warns on any ask before 3 s, a guess card after 7 s, or a pill outside 5.5-10.5 s.
2. **131 queued posts rewritten (58 YouTube, 73 TikTok, 10/25-11/10)**: one-tap emoji question first; YouTube first comment
   leads with it; description subscribe line now "Subscribe: Meatball faces a new animal every day 🍝". Log: data/engagement-edits.csv.
3. Rules in OPERATIONS.md "Always ask"; Host replies to the first 10 comments (research/experts/host.md).

## 4. How we'll know (Intel desk, weekly)
Score subs/1k and comments/1k on the first 6 ask-kit Shorts against the 6 v4 Shorts before them (data/experiments.csv row).
Keep if comments/1k ≥ 3 and subs/1k ≥ 3; if the early ask raises swipe-away (engaged views/views drops 10%+), move the guess card to 4-7 s.
