# 37 — Packaging & conversion (Packaging & Conversion Lead, 2026-10-24)

Goal: make each upload convert better at three points: the click (CTR), the decision to keep watching (stayed-to-watch / 30 s retention), and the subscribe.
Builds on research/23, 25 (Thumbnail Spec v4), 29, 31 and 34; it doesn't repeat them.

**Legend.** [OFF] YouTube's own help page or blog. [3P] third-party write-up. [M] measured here with a tool (vidIQ, Metricool, pixels). [I] my inference. [UNVERIFIED] not confirmed.
**vidIQ spend: 145 credits** (11 thumbnail scores = 55, 1 outliers = 5, 1 similar-thumbnails = 5, 16 title scores = 80). Balance went 1,878 → 1,468 during this run; the other 265 were spent by other agents on the shared account.

## 0. The short version
1. **Thumbnail B beats A on all 5 episodes** in vidIQ's model, by 3-16 points. Three unpublished episodes are queued in Metricool **with A** (md5-checked). **Recommended swaps (Mayor/Scheduler, not done by me):**
   - **myths-05, 10/26 2 PM:** A 30 → **B 46**. Swap.
   - **myths-03, 10/27 2 PM:** A 29 → **B 43**. Swap.
   - **myths-06, 10/28 2 PM:** A 21 → **B 24**. Swap, but only as a tie-break: +3 is inside the model's noise. B also follows Spec v4 better (1 hero animal, 3-word headline, 1 red device).
   - Then Nolan adds the other thumbnail as variant 2 in **Test & Compare** on each one, so real watch-time data decides.
2. Titles: vidIQ's title scorer barely separates our options (82-93). Two Shorts titles worth changing: **breeds** (82 → 92) and **moose** (88 → 92). Details in §2.
3. What breaks out in our niche right now (§3) is **A-vs-B quiz panels** (outlier quiz channels) and **illustrated stick-figure "why" scenes** (a 26.6K-sub channel at 1.06M views, 284x). Our B layout is close to both. Spec v4 gets four amendments (§3.3).
4. §4 is a one-sitting Studio checklist for Nolan; §5 is the per-upload checklist for the Producer and Postmaster.

## 1. Thumbnail scores [M]

**Method.**
- vidIQ `score_thumbnail` refuses raw.githubusercontent.com, jsDelivr and other non-YouTube hosts ("Image URL host is not supported").
- It does accept an inline base64 data URI, so each thumbnail was sent as a 192×108 WebP (q45). That is about feed size; Spec v4 rule 14 is judged at 168 px.
- Format check: myths-03 A scored 29 as both a JPEG and a WebP, so the encoding doesn't move the score. myths-05 was scored at 240 px JPEG (the first working run).
- `videoId` is a required field. I used our own long-form `gFhrONKK0rI` as a carrier, because the score is driven by the image plus the title text passed in.
- **Caveat.** vidIQ's model is unvalidated. Spec v4 §7 says to treat it as a tie-breaker, and Test & Compare watch-time share is the real verdict. Here it agrees with the spec's own rules, which is why it's acted on.

| Episode | Publishes | Title scored | A (thumb.jpg) | B (thumb_b.jpg) | Δ | Queued now | Action |
|---|---|---|---|---|---|---|---|
| myths-05 | 10/26 2 PM | 12 Animal Facts That Sound FAKE But Are 100% Real | **30** | **46** | +16 | A | **Swap to B** |
| myths-03 | 10/27 2 PM | Jaws & Disney Lied To You… (Metricool now has "12 Animal 'Facts' Movies Lied To You About (Jaws, Lion King, Nemo)") | **29** | **43** | +14 | A | **Swap to B** |
| myths-06 | 10/28 2 PM | 12 Things You Believe About Your Cat and Dog (Most Are Wrong) | **21** | **24** | +3 | A | Swap (tie-break) |
| myths-04 | already out | Playing Dead Can Get You Killed… | **38** | **51** | +13 | — | Studio: B as variant in Test & Compare |
| history-01 | already out | How Wolves Became Dogs… | **27** | **40** | +13 | — | Studio: B as variant in Test & Compare |

**What vidIQ's feedback said** (feature, point impact):
- **A (white page, 3-5 cut-out stickers, several X's).** The dominant penalty is *negative space / composition cluttered or empty*, −6 to −25. *Visual entropy unoptimized/too busy*, −9 to −11, hits 05A and 06A. *Promise overhyped*, −5/−6 on 04A and 05A, matches what Spec v4 rule 15 already says about "FACTS FAKE REAL?!" and the X collage.
- **B (saturated sunburst, 1 hero animal, 2-3 words + stamp).** Its "sharp and crisp" strength is bigger (+9 to +23) and its clutter penalties are smaller. The remaining minuses repeat:
  - "face and text competing" (05B, 04B)
  - "low-energy", meaning more saturation (05B, 04B, 06B)
  - "too much empty space" (03B, −40). The shark photo floats as a framed tile.
  - "face too small" (06B, Meatball)
  - "no visual guidance, add an arrow" (06B, history A)
- **myths-06 B is the weakest B.** The cat cut-out has a ghosted halo (rule 13), and "YOUR CAT LIED" covers half the title's promise (cat *and* dog). Fix for the next build (Producer): the dog's face beside the cat's, as a secondary at ≤60% of the hero's height. Or keep the cat and change the headline to `CAT LIES?`.

## 2. Title tests (Shorts, queued) [M]

`vidiq_score_title`, type `short`, channel UCw98RQD81t_339LX5EJqcrg. Every alternative was fact-checked against the Short's answer (research/34 rule: accuracy beats score).

| Short (episode) | Current | Score | Alternatives (score) | Pick |
|---|---|---|---|---|
| breeds (history-01) | How Old Are Dog Breeds? 🐕 | 82 | **Most Dog Breeds Are Less Than 200 Years Old?! 🐕 (92)** · Your Dog's Breed Is Way Younger Than You Think 🐕 (89) · Did the Victorians Invent Most Dog Breeds? 🐕 (84) | **Change → "Most Dog Breeds Are Less Than 200 Years Old?! 🐕"** (it's the Short's own claim, so it is accurate) |
| moose (myths-04) | Are Moose Dangerous? 🫎 | 88 | **Gentle Giant? Moose Are More Dangerous Than You Think 🫎 (92)** · Never Walk Up to a Moose. Here's Why 🫎 (88) · Moose Hurt More People Than Bears? 🫎 (86) | **Change → "Gentle Giant? Moose Are More Dangerous Than You Think 🫎"** |
| turtle (originals-01) | Can a Turtle Come Out of Its Shell? 🐢 | 93 | A Turtle's Shell Isn't a House. It's Bones 🐢 (93) · Cartoons Lied: Turtles Can't Leave Their Shells 🐢 (91) · Why a Turtle Can't Crawl Out of Its Shell 🐢 (90) | Keep |
| duck (myths-05) | Does a Duck's Quack Echo? 🦆 | 92 | A Duck's Quack Doesn't Echo? Scientists Tested It 🦆 (93) · Why You Never Hear a Duck's Echo 🦆 (90, **rejected: misleading**, the quack does echo) · The Duck Echo "Fact" Is a Total Lie 🦆 (86) | Keep (+1 is noise) |

**What the title test says** [I]:
- The scorer gives 82-93 to almost anything clear, so treat a gap under ~5 points as a tie.
- The two clear wins both turn a vague question ("How old…", "Are… dangerous?") into a **specific claim with a number or a contradiction**. That is the research/23 and 28 pattern ("Big lie…", "…Than You Think").
- **Rule for the Writer:** a Short title must carry the specific claim (a number, a superlative or "than you think"), never a bare "How/Are X?".
- These are Short titles, so Test & Compare can't check them. Log the change in data/experiments.csv: 2 changed titles vs the same pack's unchanged titles, metric = engaged views/views and views at 48 h.

## 3. What winning niche thumbnails share right now

### 3.1 Long-form outliers [M]
Source: `vidiq_outliers`, long-form, "animal myths and facts true or false quiz", last 6 months, 24 results. I coded 12 thumbnails by eye.

The breakouts are two families:
- **(a) "A vs B" quiz panels.** About 9 of the 12 coded (Quiz Kingdom 853K subs, 112x/54x; Genius Dolphin Quiz 3.4K subs, **171x**; Quiz Layer 2.5K, 93x; Quiz Ninja; Quiz Dino):
  - a full-width header bar (yellow or white on red/blue) asking a **superlative question**: `THE MOST DANGEROUS IS…`, `WHOSE BITE IS STRONGER?`, `THE DEADLIEST IS…`
  - two big, saturated animal close-ups (teeth, eyes, a bite on skin), each in a rounded panel
  - `A` / `B` circle badges with white label pills (one word each)
  - nothing else, and no faces
- **(b) Myth-list explainers.** "42 Animal Myths You've Believed Your Whole Life" (Oddly Factual, 10.6K subs, 102x, 1:50 h): parchment page, a 4-word headline, a shocked human face bottom-right holding "I BELIEVED THESE!", sketched animals.
- Also seen: a guess-the-animal grid and "Guess the animal sound" (519x). These are kids-leaning formats, not ours.

Sources (thumbnails): [PnCcso9m1to](https://www.youtube.com/watch?v=PnCcso9m1to), [WqoUe_y2jc4](https://www.youtube.com/watch?v=WqoUe_y2jc4), [20lsSvhNkPY](https://www.youtube.com/watch?v=20lsSvhNkPY), [nG7RuisTswA](https://www.youtube.com/watch?v=nG7RuisTswA), [yKjgTtMawTQ](https://www.youtube.com/watch?v=yKjgTtMawTQ), [RDPqFoNKezo](https://www.youtube.com/watch?v=RDPqFoNKezo).

### 3.2 Look-alikes of our own style [M]
Source: `vidiq_similar_thumbnails`, description: "stick-figure mascot + one real animal photo on a bright background, 2-3 word headline, red stamp", 6 months, ≥20k views.
- Most matches were off-niche (games, cartoons), so the exact Meatball look is **rare**. That gives us distinctiveness, but also no proof that it performs.
- The on-niche matches are one cluster: **illustrated stick-figure "why" explainers**:
  - "Why Are There Big Cats But No Big Dogs?" (Tp Dossier, **26.6K subs, 1.06M views, 284x**, [GBVK3t6JQOs](https://www.youtube.com/watch?v=GBVK3t6JQOs))
  - "How Humans Lost Their Tails?" (2.6K subs, 48x, [8rJGEuINdls](https://www.youtube.com/watch?v=8rJGEuINdls))
  - "Why Do Animals Save Humans?" (3K subs, 39x, [fIHCX_q8GYc](https://www.youtube.com/watch?v=fIHCX_q8GYc))
  - "Why Humans Live Longer Than Most Wild Animals" (4.4K subs, [lqUAehejMok](https://www.youtube.com/watch?v=lqUAehejMok)). That is the same 176K-search question research/34 found.
- Their shared grammar:
  - one **full-bleed drawn scene** (grass, sky, cliff), not stickers on paper
  - the stick figure is **big (40-60% of frame height) and doing something with the animal** (pulled by a bear, between a lion and a wolf)
  - a **2-4 word question headline** in yellow with a heavy black outline across the top ("NO TAIL?", "WHY NOT BIG DOGS?")
  - 1-2 animals, drawn in the same style
- [I] This is the format of our planned Saturday "Meatball Explains" and search-first episodes, and it is winning on small channels now.

### 3.3 Proposed amendments to Spec v4 (call it v4.1; the Producer owns the generator)
Evidence weight: vidIQ 5/5 A-vs-B pairs favour colour + one hero (model, weak); niche outliers (observational, moderate). Test & Compare remains the referee.
1. **Rule 11 (background):** the default becomes a **saturated full-bleed background** (the B sunburst, or a drawn scene for Explains). The white page drops to a Test & Compare variant, no longer the default. Five of five pairs went that way in vidIQ, and the outlier quiz channels never use a white page.
2. **New template D, "Which is worse?"** (for danger/superlative episodes such as myths-04 and future "deadliest" lists):
   - a header bar with the superlative question
   - 2 animal close-ups in rounded panels with `A`/`B` badges and 1-word labels
   - Meatball's head peeking between the panels, eyes on the scarier one
   - word budget ≤6 including labels. That relaxes rule 1 for this template only, the same way HI16/17 in research/25 do.
3. **Template C (Meatball Explains) changes to the scene grammar:**
   - Meatball drawn **at 45-60% of frame height, interacting** with the animal (being pulled, pointing, hiding behind)
   - a full-bleed drawn scene
   - a yellow question headline with a ≥8 px black outline
   - It replaces "white page + framed archival tile". Archival images go inside the video, not on the thumbnail.
4. **Rule 6/13 (hero fill and halos):** the hero animal must **touch at least one frame edge or overlap Meatball**. No floating framed tile (03B: −40 "empty space"). A ghosted halo is a reject, as it is today on 06B.
- Unchanged: 2-4 word headline, one red device, Meatball's gaze on the animal, the safe zones, the 168 px glance test.

## 4. Channel-page setup checklist (Nolan, YouTube Studio, desktop, ~25 min once)

Prerequisites (one-time):
- [ ] **Advanced features on** (Studio → Settings → Channel → Feature eligibility). Test & Compare and Posts need it. [OFF] https://support.google.com/youtube/answer/13861714
- [ ] **Audience = "No, not made for kids"** at channel level. Made-for-kids kills end screens and the watermark. [OFF] https://support.google.com/youtube/answer/6388789

**Home tab (Customization → Home tab → Layout)** [OFF] https://support.google.com/youtube/answer/3219384
- [ ] **Channel trailer (non-subscribers):** use **myths-04 "Playing Dead Can Get You Killed"** until a better hook exists. It is the strongest danger-to-you topic (research/28) and scores highest on both thumbnails.
  - Later, cut a 45-60 s trailer: Meatball wrong about 3 myths in a row, then "new quiz every day, keep your score", then subscribe.
  - The trailer is shown only to non-subscribers, and only until they've watched it.
- [ ] **Featured video for returning subscribers** (Spotlight): "Latest upload".
- [ ] **Sections, in this order (≤12 allowed):**
  1. Popular uploads
  2. Playlist "Every Meatball Myth (in order)"
  3. Playlist "Myths That Can Hurt You" (danger)
  4. Playlist "Cat & Dog Myths" (pets)
  5. Playlist "Ocean & Shark Myths"
  6. Playlist "Meatball Explains (Animal History)"
  7. Shorts
- **Playlists by animal/series** (create these first):
  - [ ] **Every Meatball Myth (in order):** turn on "Set as official series" (desktop, playlist settings). A video can be in only one series playlist, so make *this* one the series. [OFF] https://support.google.com/youtube/answer/6084043
  - [ ] The themed playlists are normal playlists. Title each one with a search phrase, not a brand phrase: "Dangerous Animal Myths That Can Hurt You", "Cat and Dog Myths Debunked", "Shark Myths and Ocean Animal Facts", "Animal History Explained (Funny)". Write 2-line descriptions with the keywords.
  - [ ] Each themed playlist starts with its strongest episode.
- [ ] **Banner text** (2048×1152, text inside the central 1235×338 safe area):
  - `ANIMAL MYTHS · TRUE OR FALSE`, with `New quiz every day · Can you beat Meatball?` on the second line
  - Meatball on the left, pointing at the text
- [ ] **Channel description** (first 2 lines show in search). Draft:
  > Animal myths, busted daily. Meatball, a very confident stick figure, quizzes you TRUE or FALSE on the animal "facts" everyone believes: do sharks smell blood a mile away, should you play dead for a bear, do cats always land on their feet? Keep score and beat Meatball. New animal myths quiz every day, plus "Meatball Explains" animal history on Saturdays. Animal facts, wildlife myths, pet myths and fun science for curious people of all ages.
  - Don't say "for kids": that invites a made-for-kids flag.
- [ ] **Links** (Customization → Basic info): TikTok @MeatballMyths. Add a store or Patreon link only when one exists.
- [ ] **Video watermark** (Customization → Profile): Meatball's head on a transparent PNG, 150×150, "End of video". The desktop hover shows a Subscribe button. Not shown on made-for-kids videos. [OFF] https://support.google.com/youtube/answer/10456525
- [ ] **Upload defaults** (Settings → Upload defaults): category Pets & Animals, language English, comments on, "show likes" unticked (standing order). Description template ending `Full playlist: <Every Meatball Myth URL>`.

## 5. Conversion checklist: every upload (Producer builds, Postmaster/Scheduler queues, Nolan does the Studio-only rows)

**Long-form, before queueing (Producer)**
- [ ] Two thumbnails per episode in **v4.1 layout B or D**; `thumb_b` = the colour/one-hero version. Run the 168 px one-glance test (Spec v4 rule 14).
- [ ] **Queue the higher-scoring thumbnail** in Metricool. Score both with `vidiq_score_thumbnail` (WebP data-URI method, §1, 10 credits) only when they differ by layout. The other thumbnail goes to Test & Compare.
- [ ] Title: score 3 candidates (research/34). Pick the highest *accurate* one; treat gaps under 5 points as ties and prefer the searched question.
- [ ] The first 30 s pays off the thumbnail: the animal on the thumbnail is myth #1 or teased in the cold open by 0:15. High CTR with low AVD gets penalised [OFF] https://support.google.com/youtube/answer/7628154
- [ ] Chapters from 0:00 named as the searched questions (research/29 §6). The description's first line restates the title question.
- [ ] Last 20 s of the render holds a clean end-screen zone: no text in the left or right thirds. End screens need ≥25 s of video and use the last 5-20 s [OFF] https://support.google.com/youtube/answer/6388789

**Long-form, after it goes live (Nolan, desktop Studio, ~3 min)**
- [ ] **Test & Compare:** add the second thumbnail (and optionally a second title). Up to 3 variants, desktop only, long-form only; the winner is decided on **watch time**; a test runs ≤2 weeks. Don't edit the title or thumbnail mid-test. No API, so it is Studio only. [OFF] https://support.google.com/youtube/answer/13861714
- [ ] **End screen:** Import from the previous episode (best-for-viewer video + "Every Meatball Myth" playlist + Subscribe).
- [ ] **Pin** the Metricool first comment (score check + answer key).
- [ ] Add to "Every Meatball Myth" plus one themed playlist.

**Shorts, before queueing (Producer/Writer)**
- [ ] Title carries the specific claim: a number, a superlative or "than you think" (§2). The animal is named in the first 2 words where possible (research/28).
- [ ] The Short's question appears word-for-word as a chapter title in its episode, so the funnel matches (research/29 §2).
- [ ] The last 3 s carry the verbal and visual "full quiz above ⬆" before the loop line (research/23 loop rules unchanged).
- [ ] No Test & Compare for Shorts: it is officially unavailable [OFF] (above). A 2026 third-party claim that vertical tests exist is unverified [3P] https://gyre.pro/blog/how-to-change-thumbnail-on-youtube-shorts. **First-frame packaging is the Short's thumbnail.**

**Shorts, after it goes live (Nolan, desktop)**
- [ ] **Related video** → the episode containing that myth. The only tappable link a Short has; description and comment URLs aren't clickable. Set in Studio → Details. [OFF via research/29] https://blog.youtube/creator-and-artist-stories/youtube-related-videos-traffic-guide/ ; [3P] https://support.vevo.com/hc/en-us/articles/53791074157083-YouTube-Shorts
- [ ] Rule: the episode goes live **before** its Shorts (OPERATIONS.md).

**Weekly (Analyst, Sunday)**
- [ ] Read the Test & Compare results. Log Winner / Same / Inconclusive per episode in data/experiments.csv (Spec v4 §7 decision rule: 5 of 5 or 8+ of 10 wins adopts a factor).
- [ ] **Community/Posts:** one poll a week ("TRUE or FALSE: owls turn their heads 360°?") linking to the episode. Posts need advanced features, not a subscriber count [3P] https://air.io/en/youtube-glossary/what-is-the-youtube-community-tab [UNVERIFIED against the Help Center].
- [ ] **Hype:** not usable yet. It needs YPP membership and is for channels under 500K subs, on long-form uploads in their first 7 days [3P] https://outlierkit.com/resources/youtube-hype-feature-small-creators-growth-2026/ , https://www.tubefilter.com/2025/08/26/youtube-hype-feature-launches-united-states-global/ . Put it in the post-YPP playbook: ask "hype if you beat Meatball" in week 1.
- [ ] Note: from 2026-08-24 public views count from the first frame. Judge Shorts on **engaged views** (Analytics → Advanced) and stayed-to-watch, never on raw views [3P] https://dexerto.com/entertainment/youtube-is-making-a-major-change-to-how-long-form-video-views-are-counted-3399287

## 6. Shorts → long-form funnel: what's new vs research/29
- Nothing official changed in 2026 for the Related-video link that I could find. research/29's ranking stands: Related video on every Short is still action #1.
- The quiz-panel outliers (§3.1) suggest a cross-format bridge: a Short titled "Which Is Deadlier: Mosquito or Tick?" whose Related video is a Template-D episode with the same matchup on its thumbnail. The Short and the thumbnail then make the same promise, which research/29 §2 says converts best [I].
- Track "Related video clicks per 1k engaged views" weekly (Reach tab, Nolan screenshot), as research/29 already specifies.

## Gaps
- vidIQ's thumbnail and title scores are model output, not CTR. Two months of Test & Compare results will overrule them.
- There is no official 2026 Help page for the Shorts Related-video link (search engines returned only third-party coverage). Community Posts eligibility and Hype points are third-party.
- The myths-03 thumbnail was scored with its old title. The Metricool title has since changed to "12 Animal 'Facts' Movies Lied To You About (Jaws, Lion King, Nemo)". The A/B ranking is unlikely to flip, since both thumbnails were scored against the same title.
