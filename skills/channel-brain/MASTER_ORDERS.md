# Master orders: Meatball Myths

The whole operating plan for the channel agent in one page. From here on, the job is: make, check, post, measure.

Last Updated: 2026-10-29
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
- **YouTube:** 2 a day, **12:00 and 16:00 ET** (viewers peak Mon 2-3 pm). Queue ≤7 days ahead.
- **TikTok:** 2-3 a day in the 12-5 pm window.
- **Title:** one bizarre, specific claim ("This Bird Has a Dagger on Each Foot"). No "Did you know", no TRUE/FALSE.
- **Description:** line 1 restates the claim with the search words (daddy long legs, venomous spider...), then "Sources:" and the credit lines from `footage/<slug>/credits.json` (required for CC BY / BY-SA).
- **Pinned comment:** one question that's easy to answer ("Would you keep it in your house? yes / no").
- **AI-made shots** (if any): turn on "altered or synthetic content" in YouTube Studio.

## Watch hours (the hard part of YPP)
- **Nolan, 10/30 (overrides the compilation below):** the weekly long-form is a **Meatball Investigates case file**, 8-12 min, one real story told properly. Use the style and voice of "Conspiracy Theories That Turned Out To Be TRUE" (10/27; `scripts/longform-turned-out-true.json`, style v4, voice kokoro:eric-michael, music gen:mystery).
  - Every claim is sourced and labelled proven or debunked; never present a false conspiracy as true.
  - It needs a cold open, a twist at the end and its own story arc. It is never stitched-together Shorts.
  - Case files stay long-form only; case Shorts got 1-4 views.
  - First episode: Sunday 11/8. The 11/1 tier list stays.
- **Every Sunday:** one 30-60 min compilation of a show ("Every Spider in Your House, Ranked: The Complete Collection").
  - a new cold open
  - Meatball linking segments
  - a countdown spine
  - chapters in the description

  Never a raw stitch.
- 4,000 hours ≈ 32-40K compilation views at 6-8 min average watch. Pin the newest compilation as the channel trailer.

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
