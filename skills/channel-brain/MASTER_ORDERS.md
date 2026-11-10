# Master orders: Meatball Myths

The whole operating plan for the channel agent in one page. From here on, the job is: make, check, post, measure.

Last Updated: 2026-11-05
Status: ACTIVE; replaces every older plan where they disagree (Nolan's words win over this page)
Audience: Meatball Town (all desks), Nolan

## Overview
Nolan (10/29): "set the channel up to the point all he has to do is make and post." This page is that setup. Detail lives in:
- `AUDIT_2026-10-29.md`: why it loops
- `CONTENT_REVIEW_2026-10-29.md`: what's wrong on screen
- `ANIMATION_KIT.md`: the drawn tools, for the test half only
- `STYLE_DECISION_2026-10-29.md`: realistic look, test, lock
- `CALENDAR_REALISTIC.md`: 30 ready episodes
- `SKILL.md` v3: the work gate

**Where we are (10/28):**
- 967 subs; 1,000 needed for YPP
- 63.6 of 4,000 watch hours
- stayed-to-watch 39.5%
- 2.5% of viewers return
- TikTok: already monetized

## STYLE LOCK (Nolan, 11/1): no more style changes
- **The look is locked:** the drawn style with stick-figure Meatball and TARS's species-accurate animals (`art/drawn_anatomy.py`). Nolan approved it on 10/30 ("way better, continue this style").
- **The voice is locked:** kokoro:fenrir, unless Nolan picks another from the 10/30 samples.
- **Locked for 8 weeks from 11/1.** No style tests, no photo/realistic/hybrid samples, no new render pipelines.
- **Allowed to change, one per week:** hooks, titles, topics, and new animals built with the same anatomy kit.
- **Nolan, 11/1:** "I like the style we have going. Only changes: more animations, more visibly exciting and engaging." That means more movement inside the SAME look: the animal acts out every line (walks, lunges, turns), camera punch-ins on the oh-no beat, more scene changes, a visual gag on each wow fact. It is not a new look.
- **Every Short (Nolan 11/1, approved on House Centipede Part 2 v2):** the Andrew voice (+10%, +3Hz), animals that hop and lunge, and **at least 3 locations**. Give each middle line its own `scene:`; the hook and the last line share a room so the loop is seamless.
- **Anyone proposing a style change must bring numbers to Nolan first.** Never send a sample instead.

## Studio data 11/3 (Nolan's Studio AI paste at 980 subs; detail in `oh-meatball/research/64-studio-ai-1103.md`)
- **YouTube Shorts are ~80% "Things Living In Your House"**, the rest "Is This Spider Venomous?" and "Would Meatball Survive?". Fill YT by subs per 1k views: household pests (1.8), house spiders (1.4), Would Meatball Survive (1.2), exotic (0.7), history/myths (0.2).
- **No "TRUE or FALSE" / quiz-style titles or hooks on YouTube** (20-28% stayed vs 55-63% for house creatures). Banned title words: TRUE or FALSE, Myth, Believe, Cartoons, Lied, "Did you know".
- **Titles say "in your house/kitchen/bed/basement" + a creepy specific fact**, 45-65 characters, a concrete number, one creature emoji and the series tag "(Things Living In Your House #N)" or the show tag.
- **Loop what's working:** sequels of proven winners before any new topic (house centipede, window spider, cockroach, dust mites, bed bugs, basement spider, mouse, a Would Meatball Survive), with new sourced facts; pinned comment "Part 1 is in the Related video." Then November pests (stink bugs, Asian lady beetles, boxelder bugs, cluster flies, mice, house spiders moving in).
- **YT times:** weekdays 10:00 + 16:00 ET, weekends 08:00 + 14:00 ET (second slot ≥6 h after the first; replaces 12:00 + 16:00 below). TikTok unchanged.
- **The v6 template (every render from 11/3):** narration from 0.00 s; frame 0 is the animal close-up already moving (Meatball hops in at ~2.3 s, smaller); a visceral "you" + number hook; line 2 (3-7 s) is action or danger, never the name or anatomy; no spoken or visual outro (no Subscribe, Part X, Follow or end card); the last line flows into the hook in the hook's room; the comment question is a top-corner pill on the last line and the pinned comment; a new fact or visual every second, cuts every 1.5-2.5 s, keyword cards in seconds 1-4, center captions. YT 15-20 s, TT 61-75 s.
- **Topic queue additions:** "Can 'Mommy Longlegs' Hurt You?" first (a reply to real comments), then "What Happens If You Squish a House Centipede?", "The Bugs Living In Your Bathroom Drain", and the search topics in research 64 (brown recluse bite signs: CDC/university facts, "see a doctor").
- **TikTok (Metricool 10/23-11/3):** 50/50 short loopers (15-25 s, the YT v6 cut) and 61-65 s Rewards cuts only for proven series (house centipede, house spiders, cockroach, bed bugs); new slots alternate short/long. Captions open with the creepy fact, poll last, no "Follow for Part X" ("Part 1 in my playlist"). No TikTok case-file Shorts except the weekly one. Search is 18% of TikTok views: the plain search phrase leads the caption and is on screen in the first 2 s. Rewards pays ~$0 and followers are net -58/28 days: keep TikTok on-niche, never stretch a weak topic to 61 s.
- **Next long-form** (week of 11/9 plan): "Every Creature Living In Your House, Ranked by Danger", 16:9, case-file quality, opening straight on creature #1 (26-44% leave in the first 12 s).

## Day 1 (do these before making anything new)
1. `git pull` the channel-brain folder from TARS's branch `claude/package-installation-setup-yv4j79`, then run:
   ```
   python3 <channel-brain>/tools/scan.py skills/oh-meatball
   ```
   Fix every CRITICAL.
2. **Rebuild the queue:**
   - Move every one-off fact Short out of the YouTube queue (to `held.csv`, or keep it on TikTok).
   - Unschedule everything past 7 days.
   - The next 7 days of YouTube are only the shows.
3. **Stop:**
   - all drawn re-renders
   - new research docs
   - paid promotion
   - every experiment except E-new (the style test, below)

   Close or pause the other 11 with one line each.
4. **Start tracking** (they're empty or stale today):
   - `tiktok-rewards.csv` weekly: you're paid there
   - `retention.csv` for every series Short at 48 h
   - returning viewers weekly

## The look (decided; see STYLE_DECISION)
- **Real animals, full screen, real video. Scale in every shot.**
- **Meatball is the narrator voice, a corner reaction bubble at the "oh no" moment, and the end card.** Never a cartoon body pasted on footage.
- **Test week:** 6 realistic vs 6 already-made drawn Shorts, alternating, same shows. Score at 48 h with `abtest.py`.
- **Then lock the winner for 8 weeks.** No style, format or show changes; one hook/title/topic change per week max.

## The shows (nothing else on YouTube)
1. **Things Living In Your House #N**: house bugs and mites (the best first-second hold: 58.6%).
2. **Is This Spider Venomous? #N**: spiders (the top search terms: daddy long legs, venomous spider).
3. **Would Meatball Survive? #N**: big dangerous animals (the best at bringing viewers back).

Pick episodes from `CALENDAR_REALISTIC.md`, top down. Any Short that beats 2x the median gets a Part 2 within 48 h.

## The production line (one Short, every time, in this order)
1. **Outline** (5 lines, ≤52 words, hook → oh no → scale → twist → loop). Check it:
   ```
   python3 <channel-brain>/tools/outline_lint.py outline.yaml
   ```
   (For realistic Shorts, the macro names in the outline mean the beat type; the action rule is met by footage that shows the action.)
2. **Facts:** one solid source per number, written in `sources`.
3. **Voice:** render the narration with your TTS (kokoro fenrir), one wav.
4. **Footage:**
   ```
   python3 <channel-brain>/tools/footage.py "<animal>" --get 4 --out footage/<slug>
   ```
   Needs `PEXELS_API_KEY` and `PIXABAY_API_KEY` (free) for depth; Wikimedia works without keys. Pick clips that SHOW each line (running, biting, under the microscope, next to a hand).
5. **Assemble:**
   ```
   python3 <channel-brain>/tools/realcut.py spec.json episodes/real/<slug>.mp4
   ```
   That gives the banner, 2-4-word captions, the key-number card, a slow push on every shot, and the reaction bubble. Set each shot's `dur` to its narration line's length.
6. **Check:**
   - `vidcheck.py` (≤20 s)
   - frame 0 alone: would a stranger stop?
   - one watch with the sound off: does the picture tell the story?
7. **TikTok cut:** the same footage, 60-75 s (add 3-4 more facts), for Creator Rewards.

## Posting
- **YouTube (Nolan 11/6, from the Metricool read):** **3 Shorts a day**, house shows only: **weekdays 10:00 + 16:00 + 19:00 ET, weekends 08:00 + 14:00 + 19:00 ET**. Each Short gets ~1,000 views from its test batch and none break out yet, so daily views track the upload count (7-8/day = 6-7K views, 1-2/day = 0.7-2.4K). Queue ≤7 days ahead. Never put a Short in the same slot as the long-form.
- **TikTok:** 2-3 a day in the 12-5 pm window.
- **Title:** one bizarre, specific claim ("This Bird Has a Dagger on Each Foot"). No "Did you know", no TRUE/FALSE.
- **Description:** line 1 restates the claim with the search words (daddy long legs, venomous spider...), then "Sources:" and the credit lines from `footage/<slug>/credits.json` (required for CC BY / BY-SA).
- **Pinned comment (Studio AI, 11/5):** an open question that pulls a story or a debate ("What's the weirdest bug you've found in your room?", "Did you actually check your mattress after this?"), not yes/no. Yes/no prompts got skipped: most comments were our own. Once real replies come in, pin the funniest viewer reply instead of our prompt.
- **AI-made shots** (if any): turn on "altered or synthetic content" in YouTube Studio.

## Case-file Shorts (Nolan 11/2)
- **Look:** drawn scenes (stick Meatball acting it out) alternating with real archive photos pinned as prints. Model: `episodes/case-batbomb-tt/tt-batbomb-mix.mp4`, built with `tools/drawn_casefile.py`.
- **Voice and music:** the case-file voice (kokoro:eric-michael) with mystery music.
- **Length:** TikTok cuts 61-75 s.
- **Branding:** a FILE badge, a PROVEN/DEBUNKED stamp and a two-option comment poll.
- **Sourcing:** every claim is sourced; single-source claims are said as "One account says…".

## Watch hours (the hard part of YPP)
**Nolan, 11/5 (overrides the 10/30 case-file plan and the Sunday compilation; detail in `oh-meatball/research/65-longform-reset.md`):**
- **One show:** every long-form is a **Things Living In Your House** long edition, about the creatures our Shorts already win with (house centipede, house spiders, cockroach, bed bugs, dust mites, mice). Same locked look, Andrew voice (+10%, +3Hz), 16:9.
- **A full episode, never Shorts put together.** It is scripted and rendered as its own video (like `scripts/longform-kill-or-keep.json`):
  - one promise in the title, paid off in the first 5 s, with narration starting on the creature at 0.0 s
  - no joke, intro or comment ask before 0:25
  - its own arc, with a new peak every 20-30 s and a payoff at the end that the cold open set up
  - never a stitch, compilation, recut of posted Shorts, or blurred-side vertical
  - target 8-12 min once retention holds; 5-7 min is fine until then
- **Two slots (Nolan 11/10: "push more long form"):** **Saturday 08:00 ET** plus a midweek long-form (**Wed or Thu 17:00 ET**). Kill-or-Keep Part 1 broke out: 114 views in 2 days, CTR 5%, 44% avg viewed, 96% from recommendations. First midweek: House Bug Myths, Thu 11/12.
- **Format plan (Nolan 11/10 delegated the choice to the data; yt-dlp search 11/10):** a ranking/tier list (211K-10M in-niche) > 3D size what-if (154K-7.3M) > a single-question myth (1.5-3.9M) >> lists of bug myths (~1K). Long-form order: Thu 11/12 spider-swallow myth episode, Wed 11/18 "Every Bug in Your House, Ranked From Harmless to Nightmare", then Kill-or-Keep sequels and a 3D what-if.
- **Expansion (Nolan 11/10):** backyard creatures come first after house bugs (MyWildBackyard is the comparable channel: 200K-860K views). Pets' bugs stay out for now (close to the bite/medical topics that flop).
- **Case files are DROPPED** (Nolan 11/9: the Azorian teaser Short did terribly). No case-file Shorts, long-forms or teasers. Don't propose them again unless Nolan asks.
- **No Sunday compilation** until a weekly long-form passes 500 views.
- **The bridge (Nolan, Studio):** every on-topic Short's Related video points at the newest long-form, with the pinned comment "Full list in the Related video 👆". Re-point the links every Saturday.
- **Packaging:** number + creature + "your house" + enforcement in the title, 3 titles in Test & Compare, and one creature filling the thumbnail (≤3 words, readable at 168 px).
- **Cadence rule (updated 11/10):** two a week now (Nolan's call). If midweek long-forms average under 50 views at 7 days for 3 weeks running, drop back to Saturday only.

## Weekly scorecard (Sunday, 3 numbers only)
| Number | Now | 4-week target |
|---|---|---|
| Returning viewers (7 days) | ~2,847 per 90 days | 2x |
| Subs per 1,000 views | ~0.3 | 1.0 |
| Stayed-to-watch, show Shorts | 39.5% channel | ≥ 50% |

Plus watch hours (12-month) and TikTok rewards. One change per week, picked from the worst number.

## The work gate (every task)
"Which post in the next 7 days, or which scorecard number, does this change?" No answer → `later.md`, don't do it. Research once a week max, and it must end in a queue change.

## Nolan's jobs (Studio only)
1. Make 3 playlists (one per show) and set each Short's **Related video** to its show's playlist or newest compilation.
2. Pin the 11/1 house tier list.
3. Get free **Pexels and Pixabay API keys** and add them as environment variables for the channel agent.
4. Optional: Higgsfield credits if AI shots are wanted for actions no real footage shows.
