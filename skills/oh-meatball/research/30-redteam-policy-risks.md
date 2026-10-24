# 30 — Red team: what gets Meatball Myths rejected or throttled (2026-10-24)

The Inspector's brief: assume the plan is too optimistic and find what fails YPP review, limits reach or is quietly wrong.
Tags: [OFF] YouTube/CC official text. [3P] third-party. [M] measured in this repo. [I] inference. [UNVERIFIED] not confirmed.
Severity: **P0** = can sink the YPP application, **P1** = limits reach or revenue or carries legal exposure, **P2** = quality or hygiene.

## 0. Reality check before anything else
- YPP ads tier: 1,000 subs + 4,000 public long-form watch hours in 12 months. Shorts views do not count toward the hours; the Shorts route needs 10M Shorts views in 90 days [OFF] https://support.google.com/youtube/answer/72851
- Today [M] (data/views.csv): long-form has 0-10 views per episode, and the channel gained 0 subscribers from ~5.6k views (research/24).
  4,000 h in 30 days means ~133 watch-hours a day, roughly 2,300 episode views a day at 3.5 min AVD. **Monetized in 30 days is not on the current trajectory.** Plan the 30 days as "be review-ready the day we cross the thresholds".
- A rejection has a cost [OFF] https://support.google.com/youtube/answer/9235730 , https://support.google.com/youtube/answer/9564590 :
  - a first rejection means 30 days before reapplying, and any later one means 90;
  - an appeal is possible within 21 days, as an unlisted video of under 5 min that explains the whole channel.
  - **So apply once, clean.**

## 1. What reviewers actually look at [OFF] https://support.google.com/youtube/answer/1311392
- Policy text: "Reviewers can't check every video", so they look at the channel's **main theme, most viewed videos, newest videos, biggest proportion of watch time, and video metadata (titles, thumbnails, descriptions)**, plus the channel description for reused content.
- **Inauthentic content** (renamed from "repetitious content" on 2025-07-15). The policy targets content that "looks like it's made with a template" or "may feel repetitive after several videos in a row". It names these as not allowed:
  - "Similar or repetitive content with low educational value, commentary, narratives";
  - "Image slideshows, templated storylines, or scrolling text with minimal or no narrative";
  - "AI-generated content made with generic or unoriginal templates".
- Allowed under the same policy: "Same intro and outro … but the bulk of your content is different", and series where each video has "a distinct storyline, focus, or concept".
- **Reused content** is about "content that's already on YouTube" from others. "Content that primarily features the uploading creator" is allowed. [I] Cutting Shorts from our own episodes is not reused content, so it is low risk.
- Creator reports [3P]: I found no first-hand Reddit rejection thread through search, so treat the following as weak evidence.
  - Rejection-fix sellers and blogs consistently name "slideshow with stock images and a generic AI voiceover" and "template clones/overposting" as the flagged patterns. They also say approvals come when the narration adds analysis or personality (vidiq.com/blog/post/types-youtube-channels-dont-get-monetized; podcastle.ai/blog/can-you-monetize-ai-generated-videos-on-youtube; hackernoon "AI slop crackdown").
  - Treat claims of "AI voice = auto-reject" as overstated; the policy text never says that.

## 2. Risk register

### R1 P0: the channel's most-viewed videos were fake AI "camera" clips and a cat soap opera
- Evidence [M], from data/views.csv, the yt-dlp public snapshot of 2026-10-23 13:17Z:
  - `m-kwfNbshV8` "Left him alone for 5 minutes… 😨🐕" had **2,000 views**, the top video on the channel;
  - `4Rw32SwG2iY` "Checked the porch camera…" 1,500; `ZX2QGuq_ROI` "Checked the doorbell camera at 3am…" 1,300; plus `Nz06MveAOiw` and `WZU9GYP9c-Y` (#caughtoncamera) and `SEHovKjFADA` (beaver);
  - four "Oh Meatball Pt N" Veo cat-drama Shorts.
  - They are absent from the 15:20Z and 22:42Z snapshots, which may only reflect tab truncation. **Unverified whether they are now private.**
- Why it matters:
  - The most-viewed videos are reviewer criterion #2. Photoreal fake doorbell footage is exactly "a realistic scene that didn't occur", the core of the disclosure policy.
  - Three formats in three weeks means there is no "main theme".
  - The team brief says the door-cam clips "are drafts and not posted"; that is only true of the Metricool drafts.
- Fix (Nolan, Studio > Content):
  - set every door-cam, trail-cam, beaver and "Oh Meatball Pt" video to **Private** before applying (they hold almost no long-form watch hours, so nothing is lost);
  - confirm in Studio, not via yt-dlp;
  - update the channel description and banner to say only "Meatball Myths".

### R2 P0: the Shorts are templated, with little teaching in them
- Evidence [M]: `shorts_split.tighten(mb, 2)` keeps the quiz plus at most 2 beats (the reveal line and the punch card), so most Shorts drop the explanation.
  - myths-04 "bees": "False. The bees just wait for you to come up for air" → "water is a waiting room". It never says what to do.
  - "venom": "False. Every cowboy movie lied to you" → "Hospitals have antivenom." No action is given.
- Every Short also carries the same structure, the same loop line "So be honest. Did you really think" (episode.py `loop()`), the same comment "Did you guess right? Comment ✅ TRUE or ❌ FALSE 👇", and the same description template and hashtags.
- At 3 a day, that reads as "templated … with low educational value" in exactly the "several videos in a row" view a reviewer gets on the Shorts tab.
- Fix:
  - `tighten(mb, 3)` in tools/episode.py, with the rule that the kept body beat must be the **why** beat (add `"short": "why"` in the scripts);
  - rotate 4-6 loop lines and comment prompts, picked by the hash of the myth id;
  - give each Short a one-line unique `bonus` fact in the description, not only in the comment.

### R3 P0/P1: long-form looks like a slideshow, and the format template never varies
- Evidence [M]:
  - all 5 myth scripts have exactly 12 myths and the same beat grammar: quiz → "False." → 3-4 photo beats → punch card;
  - "True or false?" is spoken 60 times across 5 episodes;
  - titles follow one mould: "12 … Myths … (TRUE or FALSE?)";
  - myths-06 reuses photos: only 34 unique of 48 photo beats, and `157484476` and `95617403` show in both "vision" and "wag";
  - every script is `"style": "classic"`, although OPERATIONS "Retention rules" says every script sets "punch".
- Fix:
  - Writer adds one non-template segment per episode (a running "Meatball was wrong" bit, a viewer-comment answer, a sourced "how scientists found out" mini-story);
  - Photo editor rule: **no photo obs repeated within an episode** (add a check in episode.py that fails on duplicate `obs`);
  - vary the title formula (research/24 search titles); set `style` per the standing order or fix the order.

### R4 P1: AI disclosure is set the wrong way round
- Policy [OFF] https://support.google.com/youtube/answer/14328491 :
  - disclosure is required for content that "seems realistic" (a real person saying something, altered real footage, "a realistic scene that didn't occur", AI music as the main focus);
  - "don't need to disclose non-realistic content that's made with AI", including fully animated video and AI help with "script, outline, thumbnail, title, or ideas";
  - "Disclosing AI content alone won't limit a video's audience or affect its eligibility to earn money". For animated or non-photoreal content the label shows in the expanded description.
- Our case: a stick-figure cartoon, real unaltered photos, a TTS narrator who is no real person, and a background music bed (not "main focus"). **None of it requires the label on YouTube.** The only content that did (R1) is the old door-cam set.
- Recommendation:
  - YouTube myth and history uploads: **Altered/synthetic = No**. Put one honest line in each description: "Narrated with a synthetic voice; animal photos are real (iNaturalist)."
  - [I] There is no official reach penalty for over-labelling, but labelling every upload synthetic puts "AI content" on every video in the reviewer's sample during a review that hunts "AI-generated content made with generic templates".
  - TikTok: keep the AI label on. TikTok's rule covers realistic AI audio, and our voice is realistic [I, check TikTok's current text].
  - Keep "Yes" for anything photoreal-AI ever again. playbook/seo-packaging.md item 1 ("disclose every time … realistic footage") was written for the door-cam era: rewrite it.

### R5 P1: CC BY / BY-SA attribution is incomplete, and share-alike is triggered by thumbnails
- CC requirements [OFF] https://creativecommons.org/faq/ :
  - name the creator;
  - give a license notice with a link to the license;
  - give a URI to the work "if reasonable";
  - **indicate modifications** (e.g. "cropped a photo");
  - this may be done "in any reasonable manner", including linking to where the attribution is listed.
- Ours [M]:
  - `episode.py credit_lines()` strips the "iNaturalist photo {id}" (no URI) and drops the license version;
  - there is no modification notice, although every photo is cropped, zoomed and colour-boosted, and the thumbnails are cut-outs;
  - the generic line "used under their licenses (…/by/4.0 · …/by-sa/4.0)" is reasonable for the license link;
  - the long-form description credits are OK; the Shorts credits are OK for names.
- BY-SA:
  - a thumbnail cut-out from a BY-SA photo (thumb3 `cutout()`) is an adaptation;
  - under the FAQ, adaptations of BY-SA material must be shared under BY-SA, and a stylised composite in a video is arguably one too [I; not legal advice].
  - BY-SA photos appear in most episodes (e.g. Ewout Knoester, jfgodeau, Gianluca Congi, Vihansith Kulatunga).
- Fix:
  - `explainer.LICENSES = "cc0,cc-by"` for thumbnails and any cut-out (simplest: drop BY-SA everywhere, since the photo pool is large);
  - in episode.py, append `inaturalist.org/photos/{id}` per credit, or link the pushed `credits.txt` URL (the "reasonable manner" route keeps descriptions short);
  - add "Photos cropped, zoomed and colour-adjusted by Meatball Myths." to every description.
- The Met: the code checks `isPublicDomain` before use, and Met Open Access images are CC0, so this is fine. Don't imply Met endorsement.
- Openverse: it allows `by` and `by-sa` at any version. 2.0/3.0 credits must include the title (the code does), but Openverse metadata can be wrong, so eyeball the source page.

### R6 P1: voice and music licences are unproven for commercial use
- edge-tts calls Microsoft Edge's Read Aloud endpoint through an unofficial client. I found no grant of commercial rights for that output [UNVERIFIED, I].
  - The same voice (en-US-AndrewMultilingualNeural) is sold for commercial use through Azure AI Speech, whose free F0 tier is ~0.5M neural characters a month, roughly our volume [I].
  - Fix: move `explainer.speak()` to the Azure Speech SDK with a free-tier key (an env var, never committed). Output is identical, and the licence trail is clean.
- vidIQ AI music bed (`brand/music/quiz-bed.m4a`): I found no vidIQ terms that confirm monetization rights or Content ID safety [UNVERIFIED].
  - Fix (Nolan): screenshot vidIQ's music licence terms for our plan into brand/music/LICENSE.txt.
  - If they are unclear, swap to a YouTube Audio Library track (monetizable by definition). Watch for Content ID claims in Studio > Content > Restrictions.

### R7 P1: made-for-kids misclassification
- Factors [OFF] https://support.google.com/youtube/answer/9528076 include "animated characters or cartoon figures", "language … intended for children", "activities that appeal to children, such as … games". We hit all three: a mascot, a quiz game, simple words.
  - The same page lists "Animated content that appeals to everyone" as a general-audience example, and says factors don't "automatically" make it for kids.
- If YouTube sets it [OFF] https://support.google.com/youtube/answer/9527654 :
  - comments, the notification bell, end screens and cards, personalised ads, and saving to Watch Later or playlists are all disabled;
  - YouTube "may override" the setting, and we get **one appeal per video**.
  - Those disabled features are our whole engagement and long-form on-ramp plan.
- Fix:
  - Nolan, in Studio > Settings > Channel > Advanced: "No, set this channel as not made for kids". Upload defaults: Audience = No.
  - Verify that Metricool sends `selfDeclaredMadeForKids=false`.
  - Remove "children's book style" from `explainer.STYLE`. Keep no "kids" or "for kids" words in tags or titles, and keep the dry adult jokes ("cheated with the neighbor's cat" register).
  - Category: Education or Pets & Animals.

### R8 P2: advertiser-friendliness is mostly safe; the photos are the risk
- Policy [OFF] https://support.google.com/youtube/answer/6162278 :
  - non-graphic animal violence in nature earns full ads;
  - "focal, prolonged graphic animal injuries" are limited, and graphic thumbnails are limited;
  - "scientifically unproven remedies" get no ads;
  - this applies to the thumbnail, title and first 7 s too.
- Our myths debunk the bad remedies (urine, sucking venom), so the context is right.
- Risks: injury and wound photos (puss-caterpillar rash, an embedded tick, a snakebite) and predation photos with blood. Also, Shorts that state the myth and then cut before the correct action (R2).
- Fix:
  - Photo editor rule: no wound, rash or blood photos, and never in a thumbnail or the first 7 s;
  - every safety myth's Short must keep the correct-action beat (vinegar/hot water for jellyfish stings; keep still and call emergency services for snakebite; "run and get indoors" for bees).

### R9 P2: duplicate and re-cut uploads
- Evidence [M]:
  - "He crashed the wedding … Pt 1" is public twice (`L5pOwnR3ieE`, `iAKwF9YyCpc`; log.csv shows a re-compose "(music)").
  - myths-02's release.json regenerates Shorts for lemming, camel, porcupine and owl, which already exist as `FycW5_cOevA`, `fNmRjqYh3Aw`, `SHQ2FzL-9Vc` and `4IcgbBL0_8s`.
  - The only guard is "check Metricool" by hand.
- Fix: keep a `data/posted.csv` ledger (platform, slug, myth, video id). episode.py/tiktok.py should mark already-posted myths `"skip": true` in release.json, and the Scheduler posts only unmarked rows. Nolan deletes the duplicate Pt 1 (or sets it private, per R1).

### R10 P2: the operating docs contradict each other, so agents act on stale orders
- OPERATIONS.md:
  - the episode goes live at "2 PM" in Cadence but at "10:30 AM ET" in Long-form rules;
  - "8-10 myths, ~10 min" in Standing orders, while the Writer role and every script use 12 (and tiktok.py's END says "twelve-myth quiz");
  - "punch" in the rules vs "classic" in the scripts.
- routines/DAILY.md still lists cat-soap-opera tags ("ai cat, pixar style animation").
- Code fallbacks disagree with the standing order: episode.py voice `en-US-AndrewNeural` and `+8%`; tiktok.py rate `+0%`.
- myths-02 release.json has **no tags**.
- Fix: Showrunner reconciles OPERATIONS.md and DAILY.md into one value each. Make the defaults match, or fail when a script omits `voice`, `rate` or `tags`.

### R11 P2: there is no fact-check gate or sources
- Spot-check of myths-06: the claims are well hedged and match mainstream sources (sweet-taste gene, AVMA dog-age curve, ~22% of grass-eaters vomit). But nothing in the pipeline requires a source.
  - "Wolves raised by people struggle with pointing" is contested; some studies show hand-reared wolves follow points.
- One wrong "fact" on a myth-busting channel is a credibility hit, and sources in the description are visible educational value for reviewers.
- Fix: add a `"sources": [url, …]` field per myth in the scripts. episode.py prints them under the chapters, and the Writer may not ship a myth without one primary or institutional source.

## 3. Pre-application checklist (do in this order)
1. R1: set off-theme videos private; confirm in Studio; rewrite the channel description to the myths premise.
2. R7: set the not-made-for-kids channel default; spot-check 3 live uploads.
3. R4: switch the YouTube altered-content setting to No for myth content, with a synthetic-voice line in each description.
4. R5: drop BY-SA for thumbnails, and add the photo links and the modification line to descriptions.
5. R2 and R3: ship 2 weeks of de-templated Shorts and episodes before applying, because reviewers sample the **newest** videos.
6. R6: get the voice and music licence evidence on file. Then apply once.
