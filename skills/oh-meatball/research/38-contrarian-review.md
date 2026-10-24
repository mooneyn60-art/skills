# 38 — Contrarian review: what is broken, weak or self-deceiving (The Contrarian, 2026-10-24)

The brand (Meatball, the stick-figure meatball) is out of scope. Everything else is in.

Legend: [M] measured by me today (frames, vidIQ, repo files). [OFF] official text. [3P] third-party. [E] my estimate. [I] inference.
vidIQ spend: 110 credits (balance 1,803 at start).

## 0. The evidence in one screen

**What I watched** (ffmpeg, 1 frame per 2 s plus 4 fps over the first 3 s; scene changes at threshold 0.1):

| File | Length | First visual change | Visual changes | Mean time per visual | Longest unchanged |
|---|---|---|---|---|---|
| myths-04/ep.mp4 (first 90 s) | 9:20 | 9.4 s (one text card swapped for another) | 12 in 90 s | 7.5 s | **0-31 s: no animal on screen** (white card, stick figure, text) |
| originals-01/short-shrimp.mp4 | 30.6 s | **6.8 s** | 4 | 7.6 s | 0-6.8 s frozen quiz card; 18.5-26.1 s same specimen photo |
| myths-06/tt-1.mp4 (TikTok) | 96.2 s | 3.5 s | 13 | 7.4 s | 27.2-43.3 s, **16 s on one kitten photo** |

Benchmark: the 3M-view opossum long-form we watched (wMjuuw3EUjw, 146x breakout) cuts every **2.5-4 s** [M, vidIQ watch]. research/21 measured rivals at 1.5-3 s.

**Our numbers** [M, vidIQ, 10/1-10/24]:
- Long-form: **4 views, 1 minute watched** in 24 days, across every episode combined. Shorts: 5,610 views, 2,283 engaged (40.7%), 12 s average view.
- Public myth Shorts (vidiq_video_stats): Ufg_uKRnh_Y 780, eWEZhNxW8fk 661, SHQ2FzL-9Vc 575, sp_lZedjjF4 516, FycW5_cOevA 188. Episodes gFhrONKK0rI 10 and RwbgzQisvYM 0.
  - Every Short's views per hour dropped from 40-65 to 0-10 within about a day. **None got past its first test batch; the ceiling is 780.**
- Channel (vidiq_channel_stats): **created 2018-05-25, 956 subscribers**, topics "Lifestyle / Entertainment / Film". On 10/15, 161 videos and ~304k lifetime views were removed (now 9 videos, 7,304 views).
- Subscribers went 942 → 956 between 10/19 and 10/24. +8 of those came on 10/22, the same day channel views jumped 83 → 4,812.

**Where the "4,547 views, 40% engaged" baseline came from** [M, data/views.csv, 10/23 13:01Z]:
- Three AI door-cam fakes held 4,800 views: m-kwfNbshV8 2,000, 4Rw32SwG2iY 1,500, ZX2QGuq_ROI 1,300. All myth Shorts together held ~2,800.
- [I] Most of the Shorts traffic and most of the new subscribers this week came from the format Nolan banned, not from Meatball Myths.
- **The myth format's real baseline is about 100-780 views per Short, dead within 24 h.**

**Winners we compared** [M, vidIQ outliers and transcripts]:
- Short: "Big lie tiger never climbed on tree", 2.2M, 65x, 23 s. It opens: "They say if a tiger chases you, climb a tree. But that's the biggest lie..." and then tells a zoo experiment as a story. No quiz, no timer.
- Short: "Never Play Dead with Bears", 682k, 19x, 51 s. A human expert talking, opening mid-sentence: "Don't play dead. I'm repeating it..."
- Short: "Bull Shark vs Great White — You've Been Getting This Wrong", 595k, 10x, 39 s. "This is a bull shark. This is a great white. What's the difference?"
  - A joke lands about every 5-8 s ("besides being dance partners, both can treat your legs as a free snack").
  - It chains three animal pairs in 39 s.
- Long-form: "Never Kill the Opossum in Your Yard", 3M, 146x, 6:55.
  - **AI TTS voice**, real moving footage, one animal.
  - "You / your yard / your kids" stakes from 0:00; 4 myths, not 12; re-hooks at 0:25, 2:01, 4:23 and 5:19; ~0.2 jokes a minute.
- Not one of these opens with "True or false?" or has a countdown.

## 1. The 15 biggest problems, ranked by impact on reaching YPP

### P1. The first 7 seconds of every video are a still image. That is exactly where 60% of viewers leave.
- **Evidence:**
  - Shrimp Short: frames 0.0-6.8 s are one unchanged card: "TRUE OR FALSE? THIS SHRIMP'S BUBBLE IS AS HOT AS THE SUN". The photo is murky, ~240 px tall at phone scale; you can't tell it's a shrimp. The stick figure sits in the bottom half.
  - tt-1: the cat card holds until 3.5 s, and the photo shows **two cats sitting on rocks** for a "cats land on their feet" claim.
  - Long-form: 0-31 s is a white screen with a stick figure and 3 text cards ("MYTHS THAT COULD GET YOU HURT", "ONLY ONE IS TRUE", the quiz). The first animal appears at ~31 s, against the OPERATIONS rule of myth 1 by ~15 s. Seconds 9-24 include a spoken disclaimer ("Quick note, this is fun general info...").
- **Why it matters:** YPP needs 3M, then 10M, Shorts views. The algorithm only widens distribution after the first batch stays. A 40% stay rate, and the 24-hour flatline on every myth Short, says we fail the first batch every time.
- **Fix:**
  - Frame 0 is a full-bleed moving image (Ken Burns at 1.15x+, a fast push-in, or a 2-photo cut by 1.0 s) showing the claim, e.g. a cat mid-fall, not a cat sitting.
  - The claim is spoken as a statement in the first 1.5 s: "This shrimp fires a bubble almost as hot as the sun."
  - Meatball reacts on top of the photo, not in an empty zone.
  - The question card and countdown go (see A6).
  - Long-form: the first photo by 1 s, the disclaimer moved to the description, myth 1 by 10 s.
- **Owner:** producer (render), writer (spoken first line), photo (claim-showing images).
- **Effort:** M (render change in episode.py, one day).
- **We'd know it worked:** engaged views / views on Shorts rises from 40% to 60%+ over 10 Shorts, and at least one Short keeps VPH above 20 at 48 h.

### P2. The plan never reaches the product. The town writes, but the video doesn't change.
- **Evidence:**
  - research/28 (10/24) found that 0 of 43 top animal Shorts open with "TRUE or FALSE". research/31 #1 (the same day) ordered "claim-first hooks".
  - originals-01, the pack built on that plan, opens **all 10 Shorts** with "True or false?", spoken and on screen. "True or false?" is spoken 13 times in myths-04 and 10 times in originals-01.
  - research/20-35 is ~34,000 words written in about 48 hours, plus 26 residents and 3 runs a day. Meanwhile the first 7 seconds look the same as research/24's "mistake #1", supposedly fixed 10/24.
- **Why it matters:** every hour spent on research about the hook, instead of on the hook, is an hour not spent on the one variable that gates views.
- **Fix:**
  - A "render gate" in episode.py that **fails the build** when a Short's first spoken words are "true or false", when the first visual change comes after 1.5 s, or when any visual holds over 4 s.
  - Rules go into code, not markdown.
- **Owner:** mayor (decision); producer (gate).
- **Effort:** S.
- **We'd know it worked:** the next pack can't be rendered in the old shape, and 0 Shorts posted after 10/27 open with "True or false".

### P3. We are steering by a contaminated baseline and a wrong premise.
- **Evidence:**
  - The "4,547 Shorts views / 40% engaged" figure and the +14 subscribers this week line up with the door-cam spike (10/22, +8 subs, +4,700 channel views).
  - The brief, research/24 and research/26 all say "~0 subscribers". vidIQ says 956.
  - research/26 is entirely built on "subscribers from 0" math.
- **Why it matters:**
  - We think the myth format "works for those who stay" (research/24: "128% viewed"). That may describe the door-cam clips.
  - We are optimizing subscriber asks we don't need: "Subscribe for Part 5" in every episode, numbered series "to give a reason to subscribe".
- **Fix:**
  - The Analyst re-pulls Shorts metrics for **myth Shorts only** (filter by video ID) and publishes that as the baseline.
  - The Accountant rewrites goal/current with 956 subs.
- **Owner:** analyst, accountant.
- **Effort:** XS.
- **We'd know it worked:** goal/current shows "subs 956/1,000 (done in ~2-3 weeks at current pace [E])". Experiments are scored against the myth-only baseline.

### P4. The binding gate is Shorts views, and nothing in the system is built to get a 100k+ Short.
- **Evidence:**
  - With 956 subs, the **lower tier is already half met**: 500 subs + 3 uploads [OFF, research/26]. All it needs is 3M Shorts views in 90 days (~33k/day). Today we get ~600-900/day, about 40x short [E].
  - Full YPP is 10M in 90 days (111k/day) or 4,000 long-form hours.
  - Our best Short ever is 780. Every case in research/27 and research/23 got there through one breakout.
- **Why it matters:** the whole operation is tuned for steady volume (3 Shorts, 4 TikToks and 1 episode a day), but the math only closes with a 100k-2M outlier.
- **Fix:**
  - Re-point every resident at one question: "what makes a Short break 10k?" Treat everything else as secondary.
  - Use winner shapes we can copy without breaking brand: misconception callout as a statement, "This X does Y" (research/28 classes A and D), A-vs-B comparison chains (CritterClips), "you" stakes.
- **Owner:** mayor, hitmaker.
- **Effort:** S (re-prioritize).
- **We'd know it worked:** one Short at 10k+ by day 14 (research/31 already sets this checkpoint; I'd keep it as the only one that matters).

### P5. Visual dead time: 7.5 s per visual against 2.5-4 s for the winners.
- **Evidence:**
  - Measured above. tt-1 holds one kitten photo for 16 s (27-43 s) while narrating cat-fall physics. It never shows a falling cat.
  - tt-1 ends with **14 s of text-only cards** (82-96 s): "LOW BATTERY MODE", then "DOG YEARS IS COMING" for 6 s (that myth is not in this video), then "COMMENT YOUR SCORE" for 6 s.
  - In the long-form, "GREAT SITCOM. TERRIBLE FIRST AID." holds about 8 s (64-72 s) with no image.
- **Why it matters:** Shorts and TikTok watch time drives both distribution and Creator Rewards RPM ("play duration", research/32). Static slideshows are also the exact policy trigger (P7).
- **Fix:**
  - A maximum of 3.5 s per visual.
  - 2-3 photos per beat with a hard cut on the stressed word, push-ins on every hold, and photos that *show the claim*.
  - Punchline cards go **over** the photo, never on a blank screen.
  - Cut the end padding.
- **Owner:** producer, photo.
- **Effort:** M.
- **We'd know it worked:** average % viewed on TikTok rises; the Shorts retention curve has no cliff at the 7-10 s card.

### P6. Daily long-form is a production line feeding nothing.
- **Evidence:**
  - Long-form total: 4 views and 1 minute in 24 days, with 956 subscribers able to see each upload.
  - research/26 already showed Path A needs ~2,667 episode views a day; research/31 #6 and research/33 asked to drop to 1 every 2 days. OPERATIONS still says one a day at 2 PM.
  - Our titles ("12 Animal Myths That Could Actually Get You Hurt") are not typed queries. The 3M winner is one animal, one "should I kill it?" question, 7 min.
- **Why it matters:**
  - A ~1,600-word script, 70+ beats and 12 photo sets a day eat most of the morning run.
  - They feed the slowest path (4,000 h) and the most templated-looking part of the channel for a reviewer (R3 in research/30).
- **Fix:**
  - **One long-form a week**: a single animal or single question that people search ("Should you kill a possum in your yard?", "What to do if a bear attacks", "Are daddy longlegs venomous?"), 6-8 min, 4-5 myths, built like the opossum video.
  - Shorts are cut from it, *and* authored on their own.
- **Owner:** mayor (decision with Nolan), writer, SEO.
- **Effort:** S (saves hours a day).
- **We'd know it worked:** the weekly episode reaches more than 500 views in 14 days through search, against today's 0-10.

### P7. Everything is templated, from the beat grammar to the captions. That is the policy's own definition.
- **Evidence:**
  - Every episode is 12 myths with the same beats: quiz → "False." → photo beats → punch card.
  - Every Short ends on the same loop line. Every pinned comment is "Did you guess right? Comment ✅ TRUE or ❌ FALSE 👇".
  - Every TikTok caption (myths-06/tiktok.json) is the identical "TRUE or FALSE? 2 animal myths, 3 seconds each. Keep score 👇", with nonsense hashtags like `#feet #vision` and `#milk #nose`.
- **Policy:**
  - YouTube's July 2026 clarification groups "generic, highly repetitive, or template-based" content first among inauthentic types [3P: Android Headlines, TechCrunch].
  - Third-party summaries say TikTok Creator Rewards excludes "static-image slideshows" and "minimal original input" [3P, unverified against TikTok's own page].
  - Our TikToks are photos plus a stick figure over TTS.
- **Why it matters:**
  - A YPP rejection costs 30 days (90 the second time) [OFF, research/26].
  - On TikTok, a slideshow verdict zeroes the money we already have.
- **Fix:**
  - Rotate 6+ hook shapes, 4+ loop lines and 4+ comment prompts. Write a **hand-written caption per TikTok**: the searched question plus one fact, no `#feet`.
  - At least one non-quiz format in every 5 uploads (story, A-vs-B, "this X does Y").
  - Motion on every photo.
- **Owner:** inspector (rules), producer (rotation), SEO (captions).
- **Effort:** S-M.
- **We'd know it worked:** a reviewer scrolling our last 20 Shorts couldn't predict the next one's first line. TikTok shows no "ineligible" flags in Creator Rewards.

### P8. The answers are predictable, so the quiz has no suspense.
- **Evidence:**
  - Answer splits per episode: myths-03 is 10 of 12 FALSE, myths-04 11 of 12, myths-06 8 of 12; myths-05 is 9 of 12 TRUE; originals-01 is 9 of 10 TRUE.
  - myths-04 announces at 0:09: "Only ONE of these is true."
- **Why it matters:** once the viewer knows the answer ("it's a myths channel, so it's false"), the countdown is dead air. That kills both the play-along and the comments.
- **Fix:** mix inside each episode at roughly 40-60%. Never announce the ratio. Let the title carry the tension, not the timer.
- **Owner:** writer, factcheck.
- **Effort:** XS.
- **We'd know it worked:** pinned-comment answers are split instead of all "false"; comments per 1k views rise above ~1 (the ours-only baseline).

### P9. The goal on the town page is fiction, and the docs contradict each other.
- **Evidence:**
  - TOWN.md: "FULL YouTube monetization by 11/23". research/26: "not achievable", review "typically in about 1 month" [OFF].
  - OPERATIONS: TikTok "4 a day from 10/25". research/32: "**Hold at 3**". research/33: "5/day".
  - OPERATIONS still says "about 0 subscribers" in the brief, and both research/33 and OPERATIONS keep daily long-form after research/31 asked Nolan.
- **Why it matters:** agents act on whichever doc they read last (research/30 R10 already flagged this). A goal everyone privately knows is impossible teaches the team to ignore the meters.
- **Fix:**
  - One source of truth: OPERATIONS.md. Research docs propose; only a Mayor `decision` changes OPERATIONS.
  - Restate the goal as "lower tier (3M Shorts views in 90 d) as soon as possible; full tier before 1 Feb 2027".
- **Owner:** mayor, accountant.
- **Effort:** XS.
- **We'd know it worked:** grep finds one cadence number per platform across the repo.

### P10. The old reaction-channel identity probably dampens long-form and confuses review.
This is the coordinator's new fact.
- **Evidence:**
  - Created 2018; 161 reaction/commentary videos (~300k views) removed 10/15. vidIQ still classifies the channel as Lifestyle/Entertainment/Film, and its similar channels are reaction channels.
  - Before removal the old catalog earned ~60 views a day (303,072 → 304,346 over 21 days), so the 944 subscribers were already near-dormant [M].
  - 956 subscribers produced 4 long-form views in 24 days.
- **What this does and doesn't do [I]:**
  - **Shorts:** little harm. The Shorts feed tests on non-subscribers by viewer interest, and topic labels follow the new uploads within weeks of consistent posting. No official source says a pivot is penalized.
  - **Long-form:** real harm. New uploads are shown first to subscribers and the browse audience the channel built. Those people came for reaction videos and don't click "12 Animal Myths". Low CTR in that first pool tells browse/suggested the video is weak. That fits the 0-10 views.
  - **Review:** the reviewer judges the channel as it stands. Deleting the reaction catalog *helps* (reused content gone), and the 2018 creation date is neutral. **Unknown and important:** did this channel ever apply for or get rejected from YPP, or hold a strike? A past rejection changes the reapply clock.
- **Fix:**
  - Keep the channel. 956 subscribers is 95.6% of the subscriber requirement; a fresh channel would throw that away for a speculative topic reset.
  - Nolan checks Studio > Earn for any past application or rejection, and Channel > strikes.
  - Rewrite the channel description and keywords to the animal-myths topic. Set the category to Education on all uploads.
  - Stop relying on subscriber notifications for long-form. Launch long-form off search titles and off Shorts' Related-video links instead.
  - Don't spend effort winning back the old subscribers.
- **Owner:** inspector (checklist), Nolan (Studio), SEO (keywords).
- **Effort:** XS.
- **We'd know it worked:** vidIQ topics and similar channels shift to animal/education within ~4 weeks [E]; long-form views come mostly from search, not "subscribers".

### P11. TikTok is called "the lab", but nobody records TikTok numbers.
- **Evidence:**
  - data/metrics.csv has **zero TikTok rows** for the myth format. No research doc or the brief gives a single TikTok view count for it.
  - Yet the cadence rises to 4 a day from 10/25, and research/33 wants YouTube Shorts gated on TikTok winners.
- **Why it matters:** we are scaling the one platform that pays without knowing whether it pays. The "TikTok gate" is a gate with no sensor.
- **Fix:** the Analyst logs every TikTok at 24 h and 72 h (views, average watch time, qualified views, follows) from Metricool. No cadence change until 7 days of rows exist.
- **Owner:** analyst.
- **Effort:** S.
- **We'd know it worked:** at least 20 TikTok rows by 11/1, so the Sunday summit decides 3, 4 or 5 a day on data.

### P12. Our "experiments" can't produce answers.
- **Evidence:**
  - E1-E6 in data/experiments.csv are "open" or "proposed" with no result.
  - The 10/23 row "Faster voice + jokes + music" changes 3 variables at once.
  - Retention rules changed several times on 10/23 alone ("classic" vs "punch" style, 18 s vs 20-25 s Shorts). The shrimp Short is 30.6 s against the 17-23 s rule in research/23.
- **Why it matters:** we can't learn which change moved the needle, so we keep re-researching.
- **Fix:** one variable per experiment, scored at 7 days or 10 videos, results written in the row. Close or kill E1-E6 today.
- **Owner:** lab.
- **Effort:** XS.
- **We'd know it worked:** every row has a result within 7 days of its start.

### P13. The TikToks are padded to clear 60 s.
- **Evidence:**
  - tt-1 is 96 s for two myths. The last 14 s are blank cards, including a tease ("DOG YEARS IS COMING") for a myth in a *different* post.
  - The kitten shot runs 16 s.
- **Why it matters:** Creator Rewards RPM rewards play duration (finish rate), not length. Padding lowers finish rate on exactly the posts that pay [3P, research/32].
- **Fix:**
  - Fill 61-75 s with a third myth or a "why" beat, never with cards.
  - End on a punchline over a photo.
  - Tease only what's in the same video or a pinned Part 2 that exists.
- **Owner:** producer.
- **Effort:** S.
- **We'd know it worked:** TikTok average watch time divided by length rises (needs P11 first).

### P14. The town is busy instead of effective.
- **Evidence:**
  - 26 residents, 3 scheduled runs a day plus a weekly summit, 28 research docs in a week.
  - The Marketing Row (8 residents) was added 10/24 for a channel whose best video has 780 views.
  - Distribution to Instagram, Pinterest and Threads multiplies the same unhooked video.
- **Why it matters:** coordination overhead (reading 60 square messages, updating 26 resident docs) is paid every run. More posts of a format that fails at second 1 are more failed tests, and they reinforce the "repetitive" pattern (P7).
- **Fix:**
  - Freeze Marketing Row and new research until P1 is fixed and measured.
  - Run with 6 residents: mayor, writer, producer, analyst, inspector, scheduler.
  - Crossposting waits until a master clears 60% stayed on YouTube or the TikTok 24 h bar.
- **Owner:** mayor.
- **Effort:** XS (stop).
- **We'd know it worked:** run time per day drops and P1-P8 ship this week.

### P15. The jokes are written but not performed.
- **Evidence:**
  - The scripts carry decent lines ("Hospitals have antivenom. Your mouth does not.", "It doesn't need a gun. It is the gun."). They land on blank text cards, read at a flat +15% TTS pace, roughly 1 per 20 s of long-form [E].
  - CritterClips' 595k Short lands one every 5-8 s, built into the comparison itself.
- **Why it matters:** humor plus Meatball is our only "authored" defense against the template verdict, and our reason to rewatch.
- **Fix:**
  - Punchline on the image with a Meatball reaction pose and a beat of silence before it (SSML break). Fewer, sharper jokes timed to cuts.
  - Test one Short pack with a different, slower delivery on the punch line.
- **Owner:** writer, producer.
- **Effort:** S.
- **We'd know it worked:** shares and comments per 1k rise; rewatch (average viewed above 100%) holds on myth-only Shorts.

## 2. Things we believe that may be false

| Belief | Why it may be false | Test |
|---|---|---|
| **1 long-form a day builds toward 4,000 h** | 4 views in 24 days. One searched topic is worth more than 7 unsearched ones (P6). | 1 a week for 3 weeks; compare views per episode. |
| **4 (or 5) TikToks a day earns more** | No TikTok data exists (P11). research/32 said hold at 3. Buffer shows a flat median per post. | Log 7 days, then decide. |
| **The TRUE/FALSE quiz is our format** | 0 of 43 top animal Shorts and none of the 4 winners I checked use it. It also forces the static card that loses us the first second. | Same myths as statement-first Shorts versus quiz Shorts, 5 vs 5. |
| **12-myth lists** | Winners are either 1 animal with 4-5 myths (opossum, 3M) or 40+ myth binge compilations at 1-2 h (Oddly Factual 118k, LieLab 664k). 12 unrelated myths at 9 min is neither searchable nor binge-length. | Next episode is one animal. |
| **The AI voice is the problem** | Probably not. The 3M opossum winner uses plain AI TTS. Our problem is what's on screen while the voice talks. Don't spend a week on voices. | Hold the voice; fix visuals first. |
| **The 3-second timer creates play-along** | It's the most static part of the video, at the moment that matters most, and with predictable answers (P8) there's nothing to play. | Remove it from 5 Shorts and compare stayed %. |
| **"The content works, only the opening doesn't" (128% viewed)** | That stat probably includes door-cam clips (P3), and survivors of a 60% swipe are self-selected. | Recompute on myth-only IDs. |
| **We need subscribers** | We have 956. Subscriber CTAs crowd out better endings. | Drop "subscribe" lines for 2 weeks; watch subs anyway. |
| **More platforms = more chances** | Same file, same hook, same failure. Volume without hook made 300 Shorts into 131k views (research/27). | Crosspost only winners. |
| **Research protects us from mistakes** | P2: the research was right and ignored. | Measure ship rate, not doc count. |
| **TikTok monetized means TikTok works** | Eligibility isn't earnings. No RPM or qualified-view data is logged. | P11. |
| **The old subscribers are an asset for distribution** | They are an asset for the subscriber gate only. For long-form they're a non-clicking first test pool (P10). | Long-form traffic-source split over 14 days. |

## 3. Stop doing
1. Opening anything with "True or false?" or a countdown card.
2. A long-form episode every day.
3. Text-only cards on a blank background (intro, punchlines, outro, "COMING NEXT").
4. Padding TikToks past 60 s with cards and teases for other videos.
5. Writing new research docs (28 in a week). Fix the product first.
6. Adding residents and rows to the town page. Freeze Marketing Row.
7. Crossposting unproven masters to Instagram, Pinterest and Threads.
8. Generic captions and nonsense hashtags (`#feet #vision`).
9. "Subscribe for Part 5" asks. Use the slot for a punchline or a comment question.
10. Announcing "only one of these is true".
11. Raising any posting cadence without 7 days of per-post data.
12. Changing several things at once and calling it an experiment.

## 4. The one bet
**Kill the static first second.** This week the producer ships 10 Shorts and 6 TikToks in one new open, enforced by a render gate:
- frame 0 is a full-screen, moving photo that *shows the claim*;
- the first spoken words state the claim as a fact or a corrected belief ("This shrimp fires a bubble almost as hot as the sun." / "Playing dead with a black bear can get you killed.");
- Meatball reacts on the photo;
- a visual change every 3 s or less;
- no "true or false", no countdown, no blank cards.

Same topics as already-posted Shorts where possible, so the comparison is clean. **Success:** myth-only stayed-to-watch at 60%+ (from ~40%) and one Short past 10k views within 14 days. If stayed-to-watch doesn't move, the problem is topic or format, not packaging, and the summit changes the format (research/31's own rule).

Why this bet: every path to YPP (3M or 10M Shorts views, or long-form via Related links) runs through Shorts passing their first test batch. Nothing else we do matters until they do.

## Sources
- vidIQ (10/24): channel_analytics top_videos, shorts_vs_longform_split, audience_retention vMnZ8kBdLRY; channel_stats; video_stats ×7; outliers (Shorts, long); transcripts 3Hv0I9p-aLY, jguDesMg-UU, LuLRuwb8vaw; video_watch wMjuuw3EUjw.
- [TechCrunch, YouTube clarifies policies around AI slop (2026-07-20)](https://techcrunch.com/2026/07/20/youtube-clarifies-policies-around-ai-slop-and-upsetting-videos/)
- [Android Headlines, YouTube monetization rules: AI slop / inauthentic content (2026-07)](https://www.androidheadlines.com/2026/07/youtube-monetization-rules-ai-slop-inauthentic-content.html)
- [HackerNoon, YouTube's AI slop crackdown](https://hackernoon.com/youtubes-ai-slop-crackdown-cant-tell-a-directed-ai-film-from-a-bot-farm)
- [Storrito, TikTok AI monetization restrictions](https://storrito.com/resources/what-tiktoks-ai-monetization-restrictions-signal-for-creator-income/) [3P, unverified against TikTok]
- [ShortsFast, TikTok Creator Rewards 2026 requirements](https://shortsfast.com/blog/tiktok-creator-rewards-2026-requirements/) [3P]
- [Reelmind, AI videos on TikTok and Shorts 2026](https://reelmind.ai/blogs/can-you-make-money-posting-ai-videos-on-tiktok-and-youtube-shorts-in-2026-curren) [3P]
