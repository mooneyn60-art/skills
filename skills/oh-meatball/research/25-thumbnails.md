# 25 — Thumbnails: evidence, outlier coding, and THUMBNAIL SPEC v4 (2026-10-24)

**Legend.** [OFF] YouTube's own page or staff. [SCI] peer-reviewed lab research. [3P] third-party data (vendor studies, so they have an interest). [M] measured here. [I] my inference. [UNVERIFIED] not confirmed. [FOLK] common advice with no evidence found.
Working files (not in repo): `/tmp/claude-0/-home-user/f2581a8c-fe42-5876-b5f9-d941a863a7fa/scratchpad/thumbresearch/` (contact sheets `outliers_1.jpg`, `outliers_2.jpg`, `low.jpg`, `feedsize_outliers.jpg`; `scripts/metrics.py`).

## 0. The one-paragraph answer
Our long-form problem today is **impressions, not CTR**. CTR only exists once YouTube shows the thumbnail, and for a channel with no viewer history YouTube first matches the video's *topic* to viewers' interests; "if no interested audience emerges, impressions stop" ([3P] report of Creator Insider, Sept 2026). Three independent datasets (ours, Eden's 2,960, the 1of10 300k summary) find that **design features barely separate breakouts from flops inside the same channel**; topic and promise do. So the thumbnail is a **gate** (it must read in one glance at 168 px) more than a growth lever. The spec below fixes legibility failures we can see in our own thumbnails, and leaves the open questions (white vs colour, one animal vs several) to Test & Compare.

## 1. How thumbnails work in YouTube's system (2025-2026)
- **Impression** = the thumbnail was on screen for more than 1 s with at least 50% visible. Counted on Search, Home, feeds, Up Next and playlists. Not counted: end screens, cards, embeds, the mobile web site [OFF] https://support.google.com/youtube/answer/9314486
- **"Good" CTR.** "Half of all channels and videos on YouTube have an impressions CTR that can range between 2% and 10%". New channels (under a week old) and videos with fewer than 100 views "can see an even wider range". CTR naturally falls when a video reaches Home [OFF] https://support.google.com/youtube/answer/7628154
  - Beaupré (YouTube Growth & Discovery): "probably all your videos have about maybe a 10% or less click-through rate", and "even your best videos, 90% of the time, your subscribed audience isn't deciding to watch". "No metric on its own is a good indicator of value." CTR drops as impressions reach people outside the core audience ([3P] write-up of Creator Insider, 2026-09-01, https://www.youtube.com/watch?v=rHLjxrbXmmY) https://ppc.land/subscribers-skip-90-of-uploads-in-their-feed-youtube-director-says/
  - [I] For us, a CTR on a few hundred impressions is noise. Judge a thumbnail on its CTR **within one traffic source** (Search vs Browse vs Suggested), never on the blended number.
- **CTR × average view duration (AVD).** "You can tell if your thumbnail is clickbait if it's getting high CTR but low average view duration", and clickbait "is less likely to get recommended" [OFF] (answer/7628154). The system also uses satisfaction surveys alongside clicks and watch time ([3P] SEJ interview with Beaupré) https://www.searchenginejournal.com/how-youtubes-recommendation-system-works-in-2025/538379/
- **Browse vs Suggested.** Home is personalised per viewer ("hey Rene is here"). For a new channel with no history, the system matches the topic to stated interests and keeps showing it only while engagement arrives ([3P], ppc.land above). Videos are sometimes recommended many times (an experiment once capped it at 8) before someone clicks, so one ignored impression is not a verdict [3P].
  - No official source describes how Suggested weighs the thumbnail [UNVERIFIED]. [I] Suggested sits next to a video the viewer is already watching, so the topic link (the title) matters more there than visual punch.
- **Test & Compare (A/B).** Up to 3 thumbnails and/or titles, desktop Studio only, long-form only (**not Shorts**). The winner is the variant with the highest **watch-time share**, "over other metrics, like click-through-rate". Results are *Winner* (statistically significant), *Performed same* or *Inconclusive* (the first upload stays). A test runs up to about 2 weeks and stops if you edit the title or thumbnail mid-test [OFF] https://support.google.com/youtube/answer/13861714
  - YouTube's advice for first tests: start with "bigger differences between thumbnails" (layout, image), then refine details. Its stated goal is "thumbnails that make a promise and videos that deliver on it" [OFF] https://blog.youtube/creator-and-artist-stories/renes-top-five-june-14-2024/
- **Thumbnail vs title vs topic.**
  - Eden (507k videos; 1,486 breakout vs 1,474 underperformer thumbnails, same channels' medians): brightness 40.9 vs 40.5, contrast 23.5 vs 23.1, saturation 35.2 vs 34.7, faces 84.2% vs 82.2%, i.e. **flat**. Real but small edges: 4-6 words of text (30.6% vs 26.5%) and drawn-on arrows/circles (41.8% vs 38.1%) [3P] https://eden.so/blog/what-makes-a-good-youtube-thumbnail/
  - 1of10 (300k+ outliers, as summarised by SEJ): thumbnails with and without faces "perform similarly"; faces help only bigger channels, and modestly [3P] https://www.searchenginejournal.com/do-faces-help-youtube-thumbnails-heres-what-the-data-says/563944/
  - Our own pixel metrics (section 3) show the same flatness.
  - **Conclusion:** topic and promise come first, the title is second (it carries search), and thumbnail craft is a hygiene factor that cannot rescue a topic nobody wants.

## 2. Perception research at feed size
Display sizes (third-party, no official spec): the desktop sidebar is about **168×94**, desktop Home and Search about 360×202, and mobile search about 156-170 px wide [3P] https://tubecore.xpanddigital.io/blog/youtube-thumbnail-size-guide . At 168 px wide the image is shrunk 7.6x, so a 1 px detail at feed size is about 8 px at 1280.
- **Faces pull the eye first.** In free viewing, people fixate a face with over 80% probability within the first two fixations (500 ms) [SCI] (Cerf, Harel, Einhäuser & Koch, NeurIPS 2007). Faces and text drew 16.6x and 11.1x more looks than equal-sized regions [SCI] (Cerf, Frady & Koch, J. Vision 2009) https://resolver.caltech.edu/CaltechAUTHORS:20130816-103355264
  - [I] The face and the text should be the two things we place deliberately. They will be looked at first whatever else is on the canvas.
- **Emotion.** Schematic threatening faces were found faster than friendly ones in crowds [SCI] (Öhman et al. 2001) https://pubmed.ncbi.nlm.nih.gov/11300573/
  - In the wild, though, exaggerated "shock" faces are rare among breakouts: 5-6% in vidIQ's 500, 8.5% vs 7.7% (breakout vs flop) in Eden's sample, about 11% in Thumbnail Bench's [3P] https://vidiq.com/research/youtube-thumbnail-study/ , https://www.netinfluencer.com/?p=53558
  - **"Shocked face = more clicks" is [FOLK].** Emotion that tells the story ("this is wrong", "gross", "smug") is the defensible use.
- **Gaze direction steers attention.** Schematic cartoon eyes looking left or right shift observers' attention reflexively, even when the gaze doesn't predict anything [SCI] (Friesen & Kingstone 1998, as described in later papers, original not read) https://pmc.ncbi.nlm.nih.gov/articles/PMC1855005
  - [I] This is the cheapest measurable win available: Meatball should **look at the hero animal**, not at the viewer.
- **Text size and word count.** vidIQ 500 breakouts: 28% have no text, 24% have 1-3 words, 17% 4-5, and the median among thumbnails with text is 5 words; it describes usage, not cause [3P]. Eden finds the 4-6 word band slightly over-represented in breakouts [3P].
  - "3 words max" is [FOLK]: no study shows it.
  - Legibility is physics [I]: at 168×94, a cap height under about 9-10 px is unreadable, which means **≥12% of frame height** at 720.
- **Number of elements.** No study counts objects vs CTR [UNVERIFIED]. vidIQ's most common top-50 layout is a "face filling roughly one-third of the frame, with a short, bold hook", with text "opposite the face" [3P]. Beaupré's "often less is more" was about feed density, not thumbnails [3P], so do not cite it as thumbnail evidence.
- **Colour against YouTube's UI.** Brightness, saturation and warmth are flat between breakouts and flops (Eden) [3P]. "Never use white backgrounds, they vanish in light mode" is [FOLK]: the biggest channel in our niche (What Gives?) uses 57-68% white pixels [M], and so does Sam O'Nella (54%) [M].
- **Curiosity gap.** The information-gap theory says curiosity comes from a *specific* known gap (Loewenstein 1994, Psych. Bulletin) [SCI, not re-read].
  - Clickbait evidence is mixed. Question headlines made readers more negative about the story (Scacco & Muddiman, Engaging News Project) [SCI-ish] https://www.journalism.co.uk/readers-perceive-question-based-headlines-more-negatively-study-shows/ . Clickbait did not raise curiosity more than plain headlines (Molina et al., CHI 2021) [SCI] https://pike.psu.edu/publications/chi21.pdf
  - [I] Use a *concrete* gap ("THE MOST DANGEROUS IS…" + two named options, HI17), not a vague "?!".
- **Title and thumbnail: one story, not the same story.** In Eden's sample, thumbnail text repeated the title verbatim in only 6.3% of breakouts vs 6.8% of flops, and 39% share no words with the title [3P].
  - The MrBeast production guide treats title and thumbnail as one promise the video must keep, and puts them first in production [3P] https://simonwillison.net/2024/Sep/15/how-to-succeed-in-mrbeast-production/
  - "Complement, don't repeat" is practitioner consensus with no controlled test [FOLK-plus].

## 3. Outlier coding: our niche [M]
Method: yt-dlp flat extraction of the newest ~60 long-form uploads per channel (2026-10-24), each video's views ÷ the channel median, thumbnails from i.ytimg.com. Coded by eye from the contact sheets.
- **HI (21):** the top 3 per niche channel, plus 1 each from WildNature Lab, Sam O'Nella and Casually Explained. Ratios run 4-50x, except Sam O'Nella 1.9x and Casually Explained 3x.
- **LO (10):** the lowest ratio per channel, skipping the newest 3 uploads. Ratios run 0.0-0.16x.
- Bias: some LO videos may be early-channel or unlisted. Quiz Madness HI15/16 are off-niche personality quizzes.

| Feature (count) | HI n=21 | LO n=10 |
|---|---|---|
| Main headline 1-4 words | 18 (median 3) | 5 (median 3.5) |
| 6+ words incl. labels | 2 (HI16, HI17) | 4 |
| Any face (human / cartoon / animal) | 16 (6 / 5 / 5) | 8 |
| Exaggerated emotion (shock, scream, fear, disgust) | 6 | 3 |
| Picture elements ≤3 / ≥4 | 11 / 10 | 6 / 4 |
| Background: white / light parchment / dark or photo / saturated tiles | 5 / 4 / 9 / 3 | 3 / 0 / 5 / 2 |
| Red arrow | 7 (all creature channels) | 2 |
| Red X or MYTH/LIE/SCAM stamp | 4 (X on animals: 1, HI04) | 1 |
| Split "before → after" / A-vs-B panels | 6 | 1 |
| Text adds info (not a restatement of the title) | 13 | 5 |
| Pixel medians: luminance / contrast / white share / saturation / edge density at 168 px | .50 / .26 / .02 / .40 / .30 | .51 / .30 / .13 / .30 / .31 |
| Ours (3 thumbs), same metrics | .72 / .32 / .53 / .15 / .29 | |

What the table supports:
1. **Short headlines dominate** among the HI (18/21 have 1-4 words), and long word-salad shows up more in LO (4/10). Small n.
2. **Style does not explain flops inside a channel.** What Gives? LO04 "YOU ARE LIARS" and LO05 "Life As TREX" use the identical white + stick-face + drawings template as HI06-08 and still got 0.09-0.16x. Mysterious-Fact LO07 uses its own Myth→Reality split and got 0.0x. **Topic decided those.**
3. **Pixel statistics are flat** (HI ≈ LO), which matches Eden.
4. **Two families of breakout grammar exist in our niche:**
   - (a) white page, a crude stick-figure face reacting in the top-left at ~30-35% of frame height, 3-5 drawn animals, a 3-word coloured headline (What Gives?, Sam O'Nella, Casually Explained);
   - (b) dark, dramatic "MYTH → REALITY" / "EXTINCT → ALIVE" two-panel with a red arrow and 1-2 words (Myths-creature, Mysterious-Fact; 49x, 24x, 22x).
5. Nobody in the HI set puts a red X on several photos the way our v3 does. Lying Pie's HI04 does it on *drawings* with a single "MYTH" stamp.

**Our three thumbnails, judged against this:**
- myths-06 A: 4 stickers and 4 X's, and the X marks land on the *neighbouring* animal (the big X sits on the cat but belongs to the dog). "LIES" is clipped by the dog's ear. Meatball's head is ~15% of the width and stares at the viewer, and his legs waste ~25% of the frame height. Cut-out halos show.
- myths-05: "FACTS ~~FAKE~~ REAL?!" contradicts itself; the flamingo and hummingbird are faded and tiny.
- myths-06 B (sunburst): the most legible at 168 px (3 words, one big animal, a stamp), but the cut-out ghosting is visible.

## 4. Faceless and mascot specifics: does Meatball's face work like a human face?
- **Evidence for:** schematic faces produce face-like N170 brain responses, larger for angry ones [SCI] https://www.aimspress.com/article/doi/10.3934/Neuroscience.2015.3.172 . Schematic faces show the threat-detection advantage (Öhman) and drive gaze cueing (Friesen & Kingstone) [SCI]. Simplified faces such as emoticons and stick figures can be read for emotion *faster* than photos, though the evidence is mixed for more detailed cartoons [SCI review] https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2021.687974/full
- **Evidence in the market:** 5 of the 21 HI are stick-figure faces, including channels with 4-5M subscribers [M].
- **Evidence missing:** no study compares a mascot with a human face on CTR [UNVERIFIED]. 1of10 even finds human faces neutral overall [3P].
- [I] Meatball's face plausibly gets the attention advantage, *if* it is big enough to resolve at 168 px. At feed size his eyes should be at least 3 px, which means pupils ≥ ~2% of the frame width at 1280. The expression must be a single readable shape (an open mouth, raised brows). He is our only ownable brand asset, so he should be in every thumbnail at the same place and scale. That builds recognition for returning viewers, which matters more than the shock value itself.

## 5. THUMBNAIL SPEC v4 (rules the generator enforces; [E] = evidence-based, [I] = inference, [T] = to be settled by Test & Compare)
1. **Words.** The headline is **2-4 words**, with no more than 5 words of text in total including the badge. No labels on individual animals. [E: HI 18/21; Eden 4-6 band]
2. **Text size.** Headline cap height **≥12% of H (≥86 px at 720)**. No text anywhere under 8% of H (58 px). At most 2 lines. [I: legibility at 168×94]
3. **Text contrast.** Luminance contrast ratio of at least **7:1** against the pixels directly behind it; dark ink on white, or white with a ≥8 px black stroke on colour. Measure it on the 168 px render. [I]
4. **Title relationship.** Thumbnail text shares **at most 1 content word** with the title (the subject noun). It adds the verdict, the twist or the stakes; it does not repeat the question. [E-weak: Eden 6.3% verbatim; FOLK-plus]
5. **Element budget.** At most **3 picture elements**: Meatball, the hero animal and at most one secondary animal, plus 1 text block and an optional badge. [I; HI split 11/10, so [T] for list episodes]
6. **Hero animal.** The largest element, with height **≥45% of H**. A photo where the **animal's face and eyes are visible** and facing the camera or Meatball. Saturation and contrast boosted, never faded. [E: faces attract gaze, Cerf]
7. **Meatball scale.** Head + shoulders only (crop above the waist, **no stick legs**). Head height **≥33% of H** (today ~31%, with ~25% wasted on legs). Pupils ≥2% of W. Same corner every time, bottom-left. [E: vidIQ face ≈ 1/3 frame; I]
8. **Meatball gaze.** His pupils point at the hero animal or the key word; never straight out on a list or single-myth thumbnail. [E: gaze cueing]
9. **Meatball expression.** One of 3 storytelling poses, mapped to the format: `aghast` (myth list), `smug-wrong` (single myth, where he is about to be wrong), `curious` (history). Default shock is not a strategy. [E: shock rare in breakouts]
10. **Red is the verdict.** One red device per thumbnail: one strike-through *or* one X *or* one stamp *or* one arrow. **Never more than one X**, and an X must sit fully inside the sticker it judges. [M: our X's land on neighbours; HI never stacks X's on photos]
11. **Background.** Keep the brand off-white paper, with white-pixel share **≤60%** (ours 0.53-0.61, What Gives? 0.57-0.68). The animal photo and Meatball must touch at least 2 frame edges, so the tile doesn't float in light mode. White vs coloured is [T], not a rule. [M; FOLK on "white vanishes"]
12. **Safe zones.** Nothing essential in the **bottom-right 22% W × 18% H** (the duration stamp) or the bottom 4% (the watch-progress bar). Keep 3% margins for the rounded corners. Series badge top-right, ≤8% of the area. [I: UI observation]
13. **Cut-out quality gate.** Hard alpha (as thumb3 does) plus a white rim ≥8 px. Reject a cut-out if more than 2% of the rim pixels sit at mid-grey alpha (halo), and fall back to a framed photo tile. [M: halos on myths-06]
14. **One-glance gate.** The generator also writes `thumb_168.png` (168×94) and `thumb_360.png` next to the full size and prints the measured headline cap height in px, the word count and the element count. A human looks at the 168 px version for 1 second and must be able to name the animal and the promise. [I]
15. **Don'ts.** No self-contradicting headlines ("FACTS FAKE REAL?!"); no 4-animal X collage; no Meatball full body; no text in the safe zones; no title echo; and no claim the video doesn't pay off in its first 30 s (high CTR + low AVD is penalised [OFF]).

## 6. Three layout templates (1280×720)
**A. Myth list ("12 Cat & Dog Myths").** Headline across the top 25%: `CAT LIES` (2 words) or `<SUBJECT> ~~FACTS~~` in black Anton, with one red marker strike. The hero animal photo takes the right 55%, 50-60% of H tall, face toward the left. One secondary animal (≤60% of the hero's height) sits behind it, top-right, with no X. Meatball's head and shoulders fill the bottom-left, head at 35% of H, eyes on the hero, `aghast`. One red X on the hero sticker's top-left corner (inside it). A `#6` badge top-right. The bottom-right corner stays clear.

**B. Single shocking myth ("Do Ostriches Really Bury Their Heads?").** Two panels split at 55/45, borrowing the creature channels' MYTH → REALITY grammar but on white:
- Left panel: a Meatball-drawn gag of the myth (an ostrich with its head in sand), labelled `MYTH` in red.
- Right panel: the real photo of the animal, labelled `REAL` in black.
- A red hand-drawn arrow from left to right, the only red device besides the label. Meatball's head peeks in from the bottom-left corner, `smug-wrong`, looking at the arrow.
- Title variant: the question; thumbnail text: only `MYTH` / `REAL` (2 words).

**C. Meatball Explains (history).** Sam O'Nella register: white page, a 2-word serif headline (`PLINY LIED`, `DISNEY'S FAKE`). The culprit (a Pliny stick figure, or a single archival image or still in a framed tile, slightly rotated) takes the right 50%. Meatball takes the left 40% at head height ≥35% of H, `curious`, holding a prop such as a scroll or magnifier, eyes on the culprit. No X, no stamp; at most one red underline under the culprit's name. Badge `EXPLAINS #3` top-right.

## 7. Measurement plan (Test & Compare)
- **Eligibility.** Long-form only, desktop Studio, set at upload (Nolan task). Shorts can't be tested, so Shorts first frames stay governed by research/24.
- **Reality check.** With 0-10 views per episode, tests will come back *Inconclusive* until impressions exist. Fix distribution first: link each Short's "Related video" to its episode, and give each episode a search title (research/24). Upload 3 variants anyway: it costs nothing and starts collecting once impressions arrive.
- **Design.** One factor per test series, with big differences first, as YouTube advises:
  1. Week 1-2: **Layout A vs current v3 vs sunburst v2** (the big swing).
  2. Then **Meatball big + gaze-at-animal vs Meatball small + gaze-at-viewer**.
  3. Then **1 animal vs 3 animals**.
  4. Then **white vs colour background**.
- **Decision rule.** Count only *Winner* results. A factor is adopted after it wins **5 of 5** or **8+ of 10** episodes (one-sided sign test p ≈ 0.03 / 0.055). "Performed same" counts as no evidence, never as a loss.
- **Logging.** One row per test in data/experiments.csv: episode, factor, variants (file hashes), result, watch-time share, and Studio CTR **by traffic source** (Search, Browse, Suggested) for each variant over the first 7 days.
- **Guardrails.** A winning variant must not cut 30-second retention by more than 5 points. If CTR rises while AVD falls, treat it as clickbait and reject it [OFF].
- **Proxy until impressions exist.** Score each new thumbnail against the spec's automatic checks (rules 1, 2, 3, 5, 10, 11, 12, 13) and run the 1-second human test at 168 px. vidIQ's `score_thumbnail` is a model whose validity is unverified, so treat it only as a tie-breaker.
