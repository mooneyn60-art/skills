# 20 — Retention and swipe-away: what the evidence says, and what to change

Researched 2026-10-23. Scope: Meatball Myths, a TRUE/FALSE animal-myth quiz with a stick-figure mascot. It uses real photos with Ken Burns zooms, a TTS voice, word-by-word captions, a 3-2-1 countdown, a reveal and a punchline card. Shorts run 30-45 s. Long-form episodes run 10 min with 12 myths.

Current numbers: about 40% "stayed to watch" and about 11 s average view duration on 30-45 s Shorts, which works out to roughly 25-35% average percentage viewed (APV).

**Evidence grades used below**
- **[OFFICIAL]**: YouTube or TikTok primary page.
- **[LEAK]**: MrBeast handbook, authenticity not officially confirmed.
- **[3P-DATA]**: third-party dataset with a stated sample.
- **[3P-OPINION]**: vendor or creator blog with no disclosed method.
- **[UNVERIFIED]**: figure seen only second-hand.
- **[INFERENCE]**: my reasoning, not a sourced finding.

Many popular "benchmark" numbers online are vendor marketing. Each is graded where it appears.

---

## 0. Definitions you need first (they changed twice)

- **"Viewed vs. swiped away" (also "Stayed to watch")** [OFFICIAL]: "the percentage of times that viewers viewed your Shorts versus swiped away." YouTube publishes no threshold and says to compare only against your own Shorts of the same format. Sources: https://support.google.com/youtube/answer/12942217?hl=en&co=YOUTUBE._YTVideoType%3Dshorts and the Help-center wording "the percentage of times viewers stayed to watch past the initial seconds of a Short," quoted via https://www.creatoressentials.com/glossary/stayed-to-watch/.
- **Engaged views** [OFFICIAL]: "How many times viewers stayed to watch past the initial seconds, not including any loops." Shorts AVD is computed from engaged views and their watch time. YPP earnings are based on engaged views. See the search-result summary of support.google.com and https://blog.youtube/inside-youtube/engaged-views-youtube-explained/.
- **Shorts public "views" since 2025-03-31** [OFFICIAL, via press]: these count every start or replay, with no minimum watch time. The old metric was renamed "engaged views." https://techcrunch.com/2025/03/26/youtube-is-changing-how-youtube-shorts-views-are-counted
- **All formats since 2026-08-24** [OFFICIAL]: a view counts from the first frame. CTR, AVD, retention and the recommendation system "are still based on engaged views" and are unchanged. https://blog.youtube/inside-youtube/engaged-views-youtube-explained/

What this means for us: the 40% figure is the hook metric. The roughly 11 s AVD is measured only over the engaged 40%. So even people who chose to stay leave at about a quarter to a third of the way through.

---

## 1. Shorts swipe rate: what decides it in the first 0.5-2 s

### Benchmarks (none of them official)

| Source | "Viewed" target | Grade |
|---|---|---|
| YouTube | No universal threshold; compare like-for-like | [OFFICIAL] https://support.google.com/youtube/answer/12942217 |
| Galloway "3.3B views" study, as retold | 70-90% performed best; under 60% saw "rapid distribution collapse" | [UNVERIFIED] second-hand: https://www.bytecap.io/research/best-hooks-for-youtube-shorts and related search results. The original 2023 study (33 channels, 5,400 Shorts) is summarized at https://nowbam.com/?p=100983 |
| Creator blogs | 75-80% goal; under 50% means the hook is failing | [3P-OPINION] https://subscribr.ai/youtube-strategy/youtube-shorts-analytics-metrics-viral, https://www.shortimize.com/blog/how-does-youtube-shorts-algorithm-work |
| Jenny Hoyos (podcast summary) | "Retention doesn't matter as much as the percentage of people swiping away" | [3P-OPINION/secondary] https://www.mfmpod.com/the-formula-to-break-100-million-views-on-shorts-ft-jenny-hoyos/ |

**Reading for us:** 40% stayed is far below every heuristic. A realistic first target is 60%; 70% or more is the "distribution" zone [INFERENCE from the ranges above]. The swipe metric is the bottleneck: a better middle cannot help viewers who left in second one.

### How fast the decision is made
- Jenny Hoyos, in a YouTube-published Creator Insider interview with Shorts product lead Todd Sherman (2025-01-28): "I really do think you have one second to hook someone, especially on Shorts." [OFFICIAL blog, creator quote] https://blog.youtube/creator-and-artist-stories/youtube-shorts-deep-dive/
- TikTok-style user study (Dashlet, Princeton, 500 videos): swipes cluster near the start and near the end of videos, and are rare in the middle. About 29% of swipes happen in the first 20% of a video. [3P-DATA, academic] https://arxiv.org/pdf/2204.12954 (figures via search summary; PDF text was not machine-readable).
- Crowdsourced QoE study: an initial loading delay makes users about 3x more likely to swipe within 10 s than mid-video stalling does. Dead time at the start is uniquely costly. [3P-DATA, academic] https://opus.bibliothek.uni-augsburg.de/opus4/frontdoor/index/index/docId/125900
- TikTok: "over 63% of the highest-CTR videos highlight their key message or product within the first 3 seconds." [OFFICIAL, ads context] https://ads.tiktok.com/business/en-US/blog/9-creative-tips-to-drive-auction-ad-performance

### First-frame and first-second patterns that raise "viewed"
1. **Payoff or most visual frame first; no intro.** Several creator sources say to open on the most visually loaded frame and cut pre-rolls. Hoyos's "$1 chicken sandwich" opens with the claim as text and the object in shot. Her test: the hook should be "so good that you can be watching the video on mute and still know what it's about." [3P-OPINION/creator] https://vidiq.com/blog/post/how-jenny-hoyos-gets-10m-views-per-youtube-short/
2. **Show the subject, not a blank card.** TikTok/CreatorIQ research found that a person on screen in the first seconds raised "hooking power" by 50%. [UNVERIFIED, ads research, second-hand] https://marketingbrew.com/stories/2023/12/18/pay-attention-to-me-report-shares-brand-tips-for-catching-users-interest-on-tiktok. For an animal channel the analogue is the animal's face or eyes, full-bleed, in frame 1 [INFERENCE].
3. **Motion from frame 1.** The eye goes to motion first in a feed (anecdotal: https://www.fingerlakes1.com/2026/03/06/static-images-are-losing-the-internet-heres-why-motion-is-taking-over/). Still photos with a pan or zoom are a valid format for info-dense niches, but captions and voice pacing matter more than visual style (https://kineclip.com/blog/animated-vs-still-faceless-video-2026/). [3P-OPINION] A slow Ken Burns zoom reads as static at 0.5 s; a fast punch-in does not [INFERENCE].
4. **Large text, inside the safe zone.** Keep key text in the middle third, clear of the title, channel and subscribe overlay at the bottom and the action rail on the right. The most-cited margins on 1080x1920 are 288 px top, 672 px bottom, 48 px left and 192 px right; Google publishes these for Shorts ads, not organic posts. [3P, conflicting] https://reap.video/blog/short-form-video-safe-zones, https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention
   - **Problem in our layout:** the mascot sits at the bottom of the frame, exactly where YouTube's title and channel overlay sits.
5. **The audio hook starts at 0.0 s.** TikTok recommends sound as storytelling and says fast tracks "above 120 BPM" often drive higher view-through. [OFFICIAL, ads] https://ads.tiktok.com/business/en-US/blog/9-creative-tips-to-drive-auction-ad-performance. A spoken claim beats a generic "True or false?" preamble because it puts the content in the first syllables [INFERENCE].
6. **Curiosity gap with a specific claim.** "Did you know" and "have you heard about" openers work through curiosity and FOMO, and the more specific the claim, the better. [3P-OPINION] https://vidiq.com/blog/post/viral-video-hooks-youtube-shorts, https://air.io/en/youtube-hacks/13-types-of-shorts-that-always-go-viral-with-examples. The Myth-vs-Truth and countdown-tension structures are listed among faceless-Short structures that perform well. [3P-OPINION] https://virvid.ai/blog/viral-shorts-structures-faceless-2026
7. **Contrast and pattern interrupt.** A white card with black text looks like a slide or an ad. It also looks the same on every video, so regular viewers learn to swipe it [INFERENCE]. The YouTube "inauthentic content" policy flags "a template with little to no variation across videos." [OFFICIAL] https://support.google.com/youtube/answer/1311392
8. **Starting mid-sentence.** No source tested mid-sentence starts against conventional openers ([3P] search: https://vidiq.com/blog/post/analyzing-popular-youtube-shorts-viral/). The underlying principle, zero dead air before content, is well supported (the QoE study and TikTok's 63% figure above).

### Examples from the fact/quiz space
- **Zack D. Films** (3D fact animations): a scroll-stopping open followed by rapid escalation and a twist. No rigorous teardown exists. [3P-OPINION, self-promotional] https://www.freelancer.de/projects/ghostwriting/fresh-edutainment-story-scripts
- **Top-viewed Shorts in vidIQ's analysis** (Zach King, Dude Perfect, Mountain Rug Cleaning, Justin Flom): all open on an already-moving visual with a promised reveal or before/after, never on a title card. [3P] https://vidiq.com/blog/post/analyzing-popular-youtube-shorts-viral/
- **Hoyos's "content buckets"**: repeatable title formats (for example "$1 X vs restaurant") get linked by YouTube for viewers who liked an earlier entry. A consistent myth-series title format can help. [3P/creator] https://vidiq.com/blog/post/how-jenny-hoyos-gets-10m-views-per-youtube-short/

---

## 2. Shorts retention

### Length
- **Paddy Galloway** (2023; 33 channels, 5,400 Shorts): 50-60 s Shorts averaged the most views (1.7M). Shorts with AVD over 50 s averaged 4.1M views, against 1.8M for 40-50 s AVD. He warns that longer only helps if retention holds. [3P-DATA, older] https://nowbam.com/?p=100983, https://news.thepublishpress.com/p/are-shorts-worth-it
- **Todd Sherman** (YouTube Shorts PM, 2023 Creator Insider): "What we try to do in recommendations is independent of duration, to figure out if someone really enjoyed the video." [OFFICIAL quote, second-hand] https://piktochart.com/blog/how-long-youtube-shorts.md
- **quso.ai** (about 508K posts from 1,900+ creators, published 2026-06): median Shorts view-through is about 45%, the top 10% reach about 91%, and 11-20 s Shorts earn the highest median views. [3P-DATA] https://quso.ai/research/video-retention-benchmarks
- **OpusClip** claims 15-30 s gets above 80% retention and educational Shorts should run 35-45 s "if the payoff is clear." No dataset is disclosed. [3P-OPINION] https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention
- **Hoyos teardown**: about 34 s is her sweet spot. [3P-OPINION] https://thedigitalheirloom.beehiiv.com/p/7-tips-viral-content-wildly-successful-18yearold-youtuber
- **Verdict for us** [INFERENCE]: one myth per Short at **20-28 s**. Retention above 70% is plausible at that length, and our 30-45 s runtime is currently being watched for 11 s. Go longer only once APV clears about 70%.

### Pacing
- **Cut rate:** OpusClip claims high performers average a cut every 2-4 s. Its TikTok piece claims "pattern interrupts every 4 s ≈ 58% retention vs 41% static." [3P-OPINION, undisclosed method] https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention, https://www.opus.pro/blog/tiktok-length-format-retention-data
- **Story beats:** a new visual or story beat every 5-7 s for story Shorts. [3P-OPINION] same source.
- **Rhythm:** Hoyos uses a five-part rhythm (fast hook, medium middle, fast peak, medium resolution, quick end) and peak-end theory. [3P/creator] https://vidiq.com/blog/post/how-jenny-hoyos-gets-10m-views-per-youtube-short/
- **Practical rule for us** [INFERENCE]: a new visual event every 2-3 s. That can be a new photo, a punch-in, a crop change, a caption emphasis, the mascot changing pose, or an SFX.

### Looping endings
- Engaged views exclude loops [OFFICIAL], but public views count replays (since March 2025) and replays feed watch time. A seamless ending that flows back to the start is widely recommended; the claim that even 10% replays boosts distribution has no supporting data. [3P-OPINION] https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention
- The swipe-timing study shows swipes cluster at the end, so an end that "feels over" (outro, logo, blank card) loses people before the loop. [3P-DATA + 3P-OPINION] https://arxiv.org/pdf/2204.12954, https://faceless.so/blog/youtube-shorts-analytics-metrics-that-matter

### The 3-second countdown: help or hurt?
- No study tests countdowns in Shorts.
- **For:** a short countdown "creates urgency and forces the viewer to commit before the reveal." [3P-OPINION] https://typito.com/blog/how-to-create-true-or-false-trivia-videos-that-get-more-engagement/. Committing to an answer is the engagement mechanic of a quiz, and true/false testing improves memory of the fact. [ACADEMIC, Uner, Tekin & Roediger 2021] https://profiles.wustl.edu/en/publications/truefalse-tests-enhance-retention-relative-to-rerea/
- **Against:** a 3 s countdown in a 30-45 s Short is 7-10% of runtime with no new information. Dead time is exactly what drives swipes (QoE study). Our current countdown is static, with only tick sounds [INFERENCE].
- **Recommendation** [INFERENCE]:
  - Keep the "commit" beat but compress it to about 1.5-2 s.
  - Fill it with motion: a ring timer, the photo zooming toward a hidden detail, the mascot's eyes darting between TRUE and FALSE.
  - Put the countdown AFTER the strongest visual, never before the first image appears.
  - A/B test it with the variant described in §5.

### Ending CTAs ("comment your score")
- No study quantifies the cost. Practitioner guidance: keep any CTA short and close to the payoff, because long or pushy CTAs "cut off the payoff effect," and drop-offs in the last 1-2 s point to outros or blank space. [3P-OPINION] https://www.gofaceless.ai/en/blog/high-retention-youtube-shorts-attributes, https://faceless.so/blog/youtube-shorts-analytics-metrics-that-matter
- **Recommendation** [INFERENCE]: put the CTA over the reveal as a text overlay in the same beat (for example "Did you get it? 👇"), not as a separate end card. End on the punchline and cut to black at the loop point.

### Captions
- **Verizon/Publicis survey** (5,616 US adults, 2019): 80% said they were more likely to finish a video with captions. This is stated intent, not behavior. [3P-DATA] https://adaccessibility.org/adaccessibility/2024/06/26/verizon-media-and-publicis-media-find-viewers-want-captions
- **Facebook internal tests:** captions raised view time by 12% on average. [OFFICIAL-ish, via press] https://www.3playmedia.com/blog/captions-increase-viewership-for-facebook-video-ads/
- **TikTok:** 40% of top-view-through ads use text overlays. [OFFICIAL, ads] https://ads.tiktok.com/business/en-US/blog/9-creative-tips-to-drive-auction-ad-performance
- **Verdict:** keep word-by-word captions. Make them large and high-contrast, place them in the middle third, and highlight key words such as TRUE, FALSE and numbers.

### AI voice
- **Research:** modern TTS and human narration show no significant learning differences (Craig & Schroeder 2017), but human voices rate higher on humanness and engagement (Craig & Schroeder 2019). [ACADEMIC, second-hand] https://link.springer.com/article/10.1007/s10639-025-13654-x, https://arxiv.org/pdf/2412.10384
- **Policy:** YouTube's July 15, 2025 "inauthentic content" policy targets mass-produced, template-like content with little variation, and enforcement is channel-wide. A synthetic voice alone is not listed as a violation. [OFFICIAL] https://support.google.com/youtube/answer/1311392; coverage at https://gulfnews.com/technology/youtube-updates-monetisation-policies-ai-and-repetitive-content-ban-begins-july-15-1.500192660
- **Verdict:** use an expressive TTS voice and give it a character (Meatball's voice, with a consistent persona and jokes). Avoid a flat narrator. Run speech at about 1.1-1.2x the default with trimmed pauses (speed advice: [3P-OPINION] OpusClip). Vary scripts, photos and punchlines so each video's substance clearly differs, to stay safe under the policy.

---

## 3. Long-form (10 min, 12 myths)

### Benchmarks
- **Retention Rabbit 2025** (10,000+ videos):
  - Average YouTube retention is 23.7%.
  - 5-10 min videos average 31.5% (the length "sweet spot").
  - 10+ min videos average about 20-25%.
  - Educational how-to averages 42.1%.
  - 55%+ of viewers are lost in the first minute.
  - First-minute retention above 65% correlates with 58% higher AVD.

  [UNVERIFIED: these come second-hand via Stripo; the primary report was not reachable] https://research.stripo.email/youtube-benchmarks
- **Realistic targets** [INFERENCE]: about 35% APV for a 10-min list or quiz video is good, about 45% is excellent, and below 25% means something is broken.
- **YouTube's own "Intro" metric** is the % still watching at 30 s. The fix YouTube gives: align the title and thumbnail with the opening, and experiment with the first 30 s. [OFFICIAL] https://support.google.com/youtube/answer/9314415

### First 30 s hook formula
- **MrBeast handbook:** "The first minute of each video is the most important minute." "Stop telling people what they will be watching and start showing them." The first minute must prove the thumbnail's promise. [LEAK] https://www.alexanderjarvis.com/memo-how-to-succeed-in-mrbeast-production/
- **Value proposition timing:** a clear value proposition in the first 15 s correlates with 18% higher 1-minute retention. [UNVERIFIED] https://research.stripo.email/youtube-benchmarks
- **Formula for us** [INFERENCE from the above]:
  - **0-5 s:** the single most shocking myth claim over its best photo. Do not use myth #1; use a teaser of the strongest myth, which is answered later.
  - **5-15 s:** the stakes, for example "12 'facts' you learned as a kid — at least 8 are FALSE, and #12 fooled scientists for 100 years." Show a montage of upcoming photos.
  - **15-30 s:** go straight into myth #1. No channel intro and no "welcome back."

### Re-hooks and open loops
- **MrBeast handbook** names minutes 1-3 and 3-6 as the next most important stretches and says to re-engage there. "Strong payoffs at the end of videos boost retention." [LEAK] https://www.alexanderjarvis.com/memo-how-to-succeed-in-mrbeast-production/
- **Open loops:** tease the next part every 2-3 minutes. [3P-OPINION] https://outlierkit.com/resources/youtube-hooks-and-retention/
- **Secondary drop at 55-65%:** 10+ min videos show about a 15% secondary drop at the 55-65% mark. [UNVERIFIED] Stripo. Place a re-hook just before 5:30-6:30.

### Progress counter ("MYTH 3/12")
- No direct study found. It aligns with the "focused, structured" advice and with the swipe evidence that viewers leave when content feels over. Counters also mitigate the end-of-video drop by showing how many items remain [INFERENCE].
- **Recommendation:** a persistent small "3/12" badge, plus a running scoreboard ("YOU: 2 · MEATBALL: 1") that viewers mentally play along with.

### Pattern interrupts
- A pattern interrupt every 10-20 s in long-form: a shot change, an insert or a caption. [3P-OPINION] https://www.revid.ai/blog/youtube-video-editing
- George Blackman on Ryan Trahan: a fast, music-timed hook followed by a deliberate slowdown, where the pace change itself acts as an interrupt. [3P/editor analysis] https://georgeblackman.substack.com/p/retention-review-7-he-fixed-retention?open=false
- Hayden Hillier-Smith analysis: no public material found. [UNVERIFIED]
- **For us:**
  - a new photo or crop every 4-8 s in long-form;
  - a mascot pose change on every beat;
  - one "big" interrupt every 45-60 s (a stinger SFX, a full-screen stamp, a mascot reaction, a scoreboard update).

### Sound effects, B-roll and mascot
- Fast editing with SFX is common across top Shorts (Zach Choi, MrBeast). [3P] https://vidiq.com/blog/post/analyzing-popular-youtube-shorts-viral/
- **Extend the SFX set:** whooshes on photo changes, a "ding" or "buzzer" on reveals, and a pop on caption keywords.
- **B-roll:** 3-5 photos or short clips per myth instead of 1-2. Public-domain or CC wildlife video clips beat stills where available [INFERENCE].
- **Mascot:** static poses are the weakest element. Cheap programmatic animation keeps the cast "alive": squash and stretch on beats, eye blinks, a head tilt on the countdown, a "shock" pose on FALSE. No study isolates mascot animation [INFERENCE].

### Chapters
- No primary evidence on the retention effect. Vendor claims of 8-10% to 64% conflict and are unsourced. [3P-OPINION] https://timeskip.io/blog/how-chapter-markers-can-boost-viewer-retention
- Chapters help search and "Key Moments" but invite skipping [INFERENCE].
- **Recommendation:** add chapters, but use teaser-style names that don't give away the answer ("Myth 7: The goldfish thing").

### Ordering 12 items
- **Best last:** the MrBeast handbook says strong end payoffs boost retention [LEAK]. A guide recommends saving one of the best items for the end because the last 10-20% drops sharply. [3P-OPINION] https://tubecore.xpanddigital.io/blog/youtube-audience-retention-guide
- **Strong early:** YouTube's own guidance is that if top moments fall late, introduce compelling content earlier, because audiences "typically decrease over the length of the video." [OFFICIAL] https://support.google.com/youtube/answer/9314415
- **Order for us** [INFERENCE that reconciles both]:
  - **#1:** the second-strongest myth, a fast FALSE with a great visual.
  - **#2-#4:** strong.
  - **#5-#6:** a re-hook ("halfway — you're 3/5? the next one breaks most people").
  - **#7-#11:** mix in a "TRUE" surprise to break the expectation that everything is false.
  - **#12:** the strongest myth, which was teased in the first 5 s.

---

## 4. TikTok-specific

- **Signals** [OFFICIAL]: finishing a longer video from beginning to end is a strong signal. "Likes, comments, and replays" seed early recommendations. https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you
- **Hook window** [OFFICIAL]:
  - TikTok Creator Academy: hook "ideally within the first 5 seconds" (via search summary; page body did not render). https://www.tiktok.com/creator-academy/en/article/elements-of-tiktok-video?lang=en
  - TikTok Ads: the hook in the first 6 s, the key message in the first 3 s. https://ads.tiktok.com/help/article/creative-best-practices
  - Practitioner claim: viewers decide in about 0.9 s. [UNVERIFIED, Iron Light Labs via blog] https://teleprompter.com/blog/tiktok-3-second-rule
- **Text-on-screen convention** [OFFICIAL, ads]: 40% of top-view-through ads use text overlays. One in three address the viewer directly or ask questions, which fits "TRUE OR FALSE?" well. Native 9:16 gives 25% higher 6-s watch-through. https://ads.tiktok.com/business/en-US/blog/9-creative-tips-to-drive-auction-ad-performance
- **Over 60 s** [OFFICIAL via press]:
  - TikTok said users spend about half their app time on videos longer than 1 minute, and that creators posting 1-minute+ videos grew followers 5x faster (Oct 2023). https://www.tubefilter.com/2023/11/27/tiktok-long-form-video-watch-time/
  - Longer-video viewership rose about 40% in six months (Mar 2024). https://techcrunch.com/2024/03/05/tiktok-says-its-revamped-creator-fund-has-increased-total-creator-revenue-by-over-250/amp
  - The Creator Rewards Program pays only on videos over 1 minute, on qualified For You views of 5 s or more (eligibility: 10K followers and 100K views in 30 days). [3P, verify on TikTok] https://influencermarketinghub.com/?p=222403
- **Practitioner length data:** 21-34 s videos average about 62% completion against about 48% for videos over 60 s; longer videos can win on total watch time if retention stays above 60%. [3P-OPINION, undisclosed method] https://www.opus.pro/blog/tiktok-length-format-retention-data
- **For us** [INFERENCE]:
  - TikTok gets two cuts: the 20-28 s single-myth Short (reach), and a 65-90 s "3-myth speed round" with a running score (monetizable, holds via the counter).
  - For videos over 60 s: re-hook at about 15 s and about 30 s (that guidance is [3P-OPINION], same Opus page), and add a visible progress indicator.

---

## 5. Ranked: the 15 highest-impact renderer and script changes

Ranked by expected effect on (a) stayed-to-watch, which is the current bottleneck at 40%, then (b) APV. Every item can be implemented programmatically.

1. **Kill the white-card opening. Frame 0 = full-bleed animal photo, already moving, with the claim burned in large.**
   - Render: start at 115% scale and punch in to 125% over 0.4 s.
   - The claim sits in the middle third with a heavy stroke, no more than 7 words (for example "GOLDFISH: 3-SECOND MEMORY?").
   - Evidence: Hoyos's mute-test and one-second hook ([blog.youtube deep dive](https://blog.youtube/creator-and-artist-stories/youtube-shorts-deep-dive/), [vidIQ](https://vidiq.com/blog/post/how-jenny-hoyos-gets-10m-views-per-youtube-short/)); TikTok's 63%-in-3-s figure ([TikTok](https://ads.tiktok.com/business/en-US/blog/9-creative-tips-to-drive-auction-ad-performance)); dead time drives early swipes ([QoE](https://opus.bibliothek.uni-augsburg.de/opus4/frontdoor/index/index/docId/125900)).
2. **Voice starts at t=0.00 with the claim itself, not "True or false?"**
   - Script: "Goldfish only remember 3 seconds — true or false?" puts content in the first syllable.
   - Trim the TTS leading silence to under 50 ms.
   - Evidence: the same sources as #1.
3. **Move the mascot out of the bottom 35% (the UI overlay zone). Put him mid-left or upper-right and make him react.** The current position sits under YouTube's title and channel overlay ([safe zones](https://reap.video/blog/short-form-video-safe-zones)).
4. **Cut Shorts to 20-28 s, with one myth and 2 explanation beats maximum.** The 11 s AVD shows the second half is unwatched. Evidence: quso 11-20 s band ([quso](https://quso.ai/research/video-retention-benchmarks)), Opus 62% vs 48% completion ([Opus](https://www.opus.pro/blog/tiktok-length-format-retention-data)), Hoyos about 34 s. Revisit longer lengths (Galloway's 50-60 s finding) only once APV is above 70%.
5. **Compress and animate the countdown: 3 × 1 s becomes about 1.5 s of motion.** Use a ring timer, a fast zoom toward the clue in the photo, and a rising-pitch tick. Do not hold a static frame. Evidence: dead time loses viewers; the commitment beat supports engagement ([Typito](https://typito.com/blog/how-to-create-true-or-false-trivia-videos-that-get-more-engagement/), [Roediger](https://profiles.wustl.edu/en/publications/truefalse-tests-enhance-retention-relative-to-rerea/)). The exact duration is [INFERENCE]; A/B test 0 s, 1.5 s and 3 s.
6. **A visual event every 2-3 s in Shorts.** Use photo swaps (3-5 photos per myth), hard punch-ins instead of slow Ken Burns, and caption keyword pops. Evidence: [Opus Shorts](https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention) (2-4 s cuts, [3P-OPINION]); fast editing is common in top Shorts ([vidIQ](https://vidiq.com/blog/post/analyzing-popular-youtube-shorts-viral/)).
7. **Reveal hard and early: an answer stamp (giant TRUE ✅ / FALSE ❌) with a buzzer or ding SFX at no later than 8-10 s.** The payoff is the peak of a peak-end structure ([vidIQ/Hoyos](https://vidiq.com/blog/post/how-jenny-hoyos-gets-10m-views-per-youtube-short/)). Early payoffs correlate with higher retention ([Opus TikTok](https://www.opus.pro/blog/tiktok-length-format-retention-data), [3P-OPINION]).
8. **Loop ending: the last line flows into the first frame, with no end card, logo or blank.** Example: punchline, then "…so next time someone says goldfish only remember 3 seconds —" which cuts straight to frame 0. Evidence: [Opus](https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention); end-cluster swipes ([Dashlet](https://arxiv.org/pdf/2204.12954)); outros cause last-second drops ([faceless.so](https://faceless.so/blog/youtube-shorts-analytics-metrics-that-matter)).
9. **Fold the CTA into the reveal ("Got it right? 👇") and drop any separate CTA card.** Evidence: [gofaceless](https://www.gofaceless.ai/en/blog/high-retention-youtube-shorts-attributes) (long CTAs cut off the payoff, [3P-OPINION]).
10. **Animate Meatball cheaply.** Squash and stretch on each word-beat, blinks, a "thinking" head tilt during the countdown, and a pose per verdict. This removes the most static element on screen [INFERENCE]. It also helps the video read as authored, not templated, under the [inauthentic-content policy](https://support.google.com/youtube/answer/1311392).
11. **TTS persona and pacing: an expressive voice, 1.1-1.2x speed, inter-sentence pauses capped at about 150 ms, and pitch or energy up on reveals.** Evidence: TTS is equal on comprehension but weaker on engagement and humanness ([Springer 2025 review](https://link.springer.com/article/10.1007/s10639-025-13654-x)), so the voice has to compensate with energy and character.
12. **Captions: large and high-contrast in the middle third, 1-3 words at a time, keyword color pops (FALSE in red, TRUE in green, numbers in yellow).** Evidence: [Verizon/Publicis](https://adaccessibility.org/adaccessibility/2024/06/26/verizon-media-and-publicis-media-find-viewers-want-captions) (survey) and [Facebook +12% view time](https://www.3playmedia.com/blog/captions-increase-viewership-for-facebook-video-ads/). Captions must not collide with the mascot or the overlay.
13. **Long-form cold open: 0-5 s strongest myth teaser, 5-15 s stakes ("8 of these are FALSE") and a photo montage, then myth #1 by 15-20 s. No channel intro.** Evidence: [MrBeast handbook](https://www.alexanderjarvis.com/memo-how-to-succeed-in-mrbeast-production/) [LEAK], [YouTube Intro metric](https://support.google.com/youtube/answer/9314415), 55% first-minute loss ([Stripo/Retention Rabbit](https://research.stripo.email/youtube-benchmarks), [UNVERIFIED]).
14. **Long-form structure: a persistent "MYTH 3/12" badge, a running score, re-hooks at about 1:00, about 3:00 and about 5:30-6:30, a TRUE-surprise mixed into the middle, the strongest myth last (teased at 0:00), and one big interrupt every 45-60 s.** Evidence: MrBeast re-engagement at minutes 1-3 and 3-6 [LEAK]; a secondary drop at 55-65% [UNVERIFIED]; open loops every 2-3 min ([outlierkit](https://outlierkit.com/resources/youtube-hooks-and-retention/)); YouTube says to put compelling content earlier ([YouTube](https://support.google.com/youtube/answer/9314415)).
15. **Per-video variety and an A/B harness.**
    - Rotate opening styles (photo-claim, close-up-eye reveal, "Meatball gasps" reaction), caption palettes and music beds.
    - Use YouTube's own method: compare only same-format Shorts on stayed-to-watch ([YouTube](https://support.google.com/youtube/answer/12942217)).
    - Test one variable at a time, in this order: opening frame, countdown length, Short length.
    - Variety also protects against the [inauthentic-content policy](https://support.google.com/youtube/answer/1311392).
    - On TikTok, also ship a 65-90 s "3-myth speed round" with a score counter for Creator Rewards eligibility ([TikTok >1 min data](https://www.tubefilter.com/2023/11/27/tiktok-long-form-video-watch-time/)).

### Targets to track
- Stayed to watch: 40% → **60%** (first milestone) → **70%+**.
- Shorts APV: about 30% → **70%+** at 20-28 s.
- Long-form intro (30 s) retention: **≥70%**; APV: **≥35%**.
- These are [INFERENCE] milestones built from the ranges above. YouTube publishes none.

---

## Gaps and caveats
- No official YouTube or TikTok numeric threshold exists for swipe rate or APV. Every benchmark here is third-party.
- Not found:
  - the original Retention Rabbit report (all figures here are second-hand via Stripo);
  - Paddy Galloway's original VVSA threshold (the 70-90% figure is second-hand);
  - any Hayden Hillier-Smith analysis;
  - any quiz-Short countdown study;
  - any controlled study of chapters, mascots or Ken Burns stills.
- The OpusClip, Subscribr, vidIQ and gofaceless numbers are vendor content without disclosed methods.
- The MrBeast handbook is a leak. Two former producers vouched for it; MrBeast's team declined comment ([Passionfruit](https://passionfru.it/mrbeast-leaked-document-81151/)).
