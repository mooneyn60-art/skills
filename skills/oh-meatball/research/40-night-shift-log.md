# 40 — Night shift (R&D) log

The 21:37 run (redteam, showrunner, studio, intel lab) digs one avenue per night, in this rotation, and logs it here.
Next night takes the next letter; after g, start again at a.

| Letter | Avenue |
|---|---|
| a | A new breakout format in animal/edu Shorts (vidiq_outliers + IG/TikTok outliers; watch 2 winners) |
| b | Competitor teardown: one rival's top 5 videos |
| c | A 2026 platform rule change (monetization, AI labels, originality) |
| d | A new revenue or distribution avenue not in research/32, 35 or 36 |
| e | Audience question mine (vidiq_comment_insights) → 10 ideas |
| f | Retention autopsy: this week's best and worst video (audience_retention) |
| g | A tooling upgrade that enforces a finding automatically |

| Date | Letter | Avenue | Finding (one line) | Build | vidIQ credits |
|---|---|---|---|---|---|
| 2026-10-25 | a | Breakout formats | 62 s cartoon explainer (1.6M, 10.3x) holds its promised answer to 69%; all 8 of our deep dives give the answer in line 1 | `tools/openloop.py`, `scripts/v4-one-weakness-pangolin.json`, `research/40-openloop-gate.diff` | 30 |
| 2026-10-26 | b | Competitor teardown (Voggle) | 5/5 of Voggle's top Shorts (2.7M-350K, 86-173 s) open on a past-tense scene mid-action; 5 of our 83 scripted Shorts do (1 of the 6 pilot cases); their famous Emu War did 9.5K vs a 27K median | `tools/coldopen.py`, `scripts/investigates-a119-moon-bomb.json` | 35 |
| 2026-10-28 | c | YouTube "inauthentic content" (July 2026 clarification) | Bucket 1 demonetizes template videos "with little variation"; 5 of our YT cuts share one exact skeleton and the new batch was converging on another (hook-solo x6-punch, 4 outlines) | `tools/sameness.py`, gate in `tools/drawn_quick.py` | 0 (balance ~28, below 300) |

**Next night: d** (a new revenue or distribution avenue).

---

## 2026-10-25 — a. Breakout format: the "One Weakness" open loop for 60 s+ deep dives

**Spend:** 30 vidIQ credits (balance 765 at start): `vidiq_outliers` Shorts 5, `vidiq_instagram_tiktok_outlier_search` 5,
two `vidiq_watch_shortform_content` 20.

### What the outlier pulls showed (last 30 days)
- YouTube Shorts, "weird animal facts explained by a cartoon character", 100k+ views: 24 results. Most are meme/skit
  clips (Oops Zoo hand-drawn animal moments 4.1M and 5.6M, ~35x). The edu ones are "how/why" question titles:
  "HOW Do Hunters Catch Giant Iguanas at Night?" 230k, 37x; "Why Is It Difficult To Put Fish Into the Ship Tank?" 626k, 20x.
- IG + TikTok, format search: the explainers that broke out are all **"why" animated explainers with a twist ending**:
  - @chanchostagram "Why Dachshunds Were Bred" (Zack D Films reupload): 834k, **443x** the account median.
  - @mikmok.exe "Why You Should Talk Back To Your Cat When It Meows": 2.2M, 4.6x.
  - @lilpotatestiktok T. rex 2D cartoon explainer: **1.6M, 10.3x, 62 s**. This is the closest rival to our TikTok deep dive.
  - @ezzies_aquatics "things mudskippers do that will make you question your choice of pet": 1.1M, 10.3x (hyperbolic list).

### Watched 1: @lilpotatestiktok T. rex, 62 s, 1.6M (TikTok 7693231022183320865)
- 0:00-0:07 hook: "Did you know the dinosaur with the strongest bite **had exactly one weakness?** And once you know it,
  **even you could survive it.**" A promise plus a "you" stake.
- 0:07-0:33: builds the threat (40 ft, 8 tons, 60 teeth, bone-shattering bite).
- 0:33-0:44: a **decoy** (everyone laughs at the tiny arms, but each curls ~200 kg), then "its one real weakness was hiding
  in plain sight. **It's the legs.**" The answer lands at **0:43, 69% of the runtime**.
- 0:44-0:55: the science (bone stress at a sprint, ~12 mph). 0:55-1:01: pun ending ("couldn't catch you... but it could
  catch feelings for you").
- 26 visual changes, **2.4 s per visual**; 3 jokes; the ending's stare loops into the opening.

### Watched 2: "Why Dachshunds Were Bred", 41 s, 834k (IG DeF2JABMT81)
- 11 shots; the animated part cuts every **2.65 s**. A chain of body-part → job facts (short legs → badger holes; paws →
  dig; deep ribs → protect organs; big teeth → hold the badger).
- At 0:26.5 it cuts to **14 s of real footage of a lazy dachshund upside down on a couch**: the only joke, and it is the
  contrast. No "you", no loop.

### The finding
**The 60 s winners withhold.** The T. rex video promises one answer at 0:03 and makes the viewer wait to 69% for it,
through two wrong guesses. Our TikTok deep dives do the opposite. `tools/openloop.py` on packs 1-2:

| Script | Deep dives | Open loop in lines 1-3 | Withheld payoff | Decoys |
|---|---|---|---|---|
| tiktok-pack-01 | 7 (bombardier, horned lizard, sea cucumber, gila, vulture, bullet ant, tarantula hawk) | 0 | 0 | 0 |
| tiktok-pack-02 | 1 so far (secretarybird) | 0 | 0 | 0 |

Every one opens with the whole fact as line 1 ("Horned lizards squirt blood from their eyes.") and then lists more facts.
That is right for a 20-25 s Short (research/38: claim-first wins there), but in a 62 s video nothing pulls a viewer past
30 s except the next fact. Creator Rewards pays only on 60 s+ views, so the back half is where the money is.
[I] Unmeasured on our account: TikTok analytics have returned zeros since the reconnect (intel playbook), so the
retention cost is inferred from the rival, not from our curves. The test below measures it.

### The build
1. **`tools/openloop.py`** (new, standalone). Lints every deep dive (`"_len": "deep"` or 25+ beats):
   - R1: a promise in lines 1-3 (`"promise": true`, or a cue such as "one weakness", "but", "?").
   - R2: exactly one `"payoff": true` beat, starting at 50-80% of the spoken words.
   - R3: at least 2 `"decoy": true` beats before the payoff.
   - R4 (warning only): a re-hook line ("Wait...", "the weird part") at 30-60%.
   - Exit 1 on failure. Shorts are skipped.
   - Result today: 8 of 8 existing deep dives FAIL; the prototype passes.
2. **`research/40-openloop-gate.diff`**: wires the check into `tools/episode.py`, so a failing deep dive stops the render
   (`--no-openloop` for old packs). Not merged: episode.py is in use by the Pack 2 render tonight. **Mayor: merge after
   Pack 2 finishes** (`git apply skills/oh-meatball/research/40-openloop-gate.diff`); merged mid-pack it would stop the
   secretarybird re-render.
3. **`scripts/v4-one-weakness-pangolin.json`**: a v4 deep dive in the new shape (prototype, not for posting):
   - 0:00 "This animal is armored against lions. **But it has exactly one weakness.**"
   - decoy 1: the soft belly? No, it rolls into a ball (Meatball knocks: "Nobody answered.");
   - decoy 2: no teeth? True, it swallows stones to grind ants. "Kind of genius."
   - re-hook: "Wait. It walks on its back legs?"
   - **payoff at 60% of the words:** "The weakness is the ball itself. Lions can't open it. But people just pick it up.
     That's why it's the most trafficked mammal." (CITES Appendix I since 2016.)
   - Meatball's ending: "Rolling up is my plan too. I'm already a ball. A delicious ball." (Meatball *is* a ball: the
     gag only works for him.)
   - Ground pangolin photos: iNaturalist research-grade, wild, CC0/CC BY (obs 341230008, 93016098, 130263150,
     325086870, 246955251, 192256680), picked by eye from a contact sheet; sources on the hook beat.
   - Render test results are in the section below.

### Proposed experiment (for the Mayor; one variable)
E-OL: the next 3 TikTok deep dives use the open-loop shape; compare average watch time and the share of views past 60 s
against the 3 deep dives before them (same voice, same length band). Keep it if watch time is +10% or better.

### Render test (scratch copy of the skill, CRF 30; nothing posted, render folders deleted)
- **65.4 s**, v3 gate: 91 events, longest gap **2.10 s**. Payoff ("THE WEAKNESS", Meatball tumbles onto the ball) lands at
  **~39.5 s = 60%**, inside the window; the T. rex rival's lands at 69%.
- Render 1: v4 gate **22/38 shots** as cut-outs. Obs 341230008 failed edge contrast (4.2), so frame 0 fell back to a
  scales-only crop with no head (a frame-0 rule break); obs 192256680 (night, torch-lit) cut out as a glowing blob.
  Both were swapped out. Render 2: **32/38 cut-outs**; the 6 stills are obs 93016098 ("matte in pieces"), which still
  shows the whole animal.
- V4 QA: Meatball over the animal 2 frames (contact knock) and 5 frames (payoff tumble), 0 frames under captions, 0 clipped.
- Frames: `research/40-night/2026-10-25-pangolin-sheet.jpg` (1 per 2.5 s), `...-payoff.jpg` (4 fps at the payoff).
- **Weak spots seen in the frames:**
  - The v4 inpaint leaves a flat beige or pink smudge where the animal was painted out. It is visible behind Meatball at
    0:00 and on every ball shot. This is a Studio item.
  - At frame 0 the pangolin cut-out is small (about 1/5 of the frame width). That is v4's known cost (research/45 §7).
- **Factdesk:** still needs the by-eye cut-out check. Obs 325086870 carries a grass stem along the cut-out's belly.

---

## 2026-10-26 — b. Competitor teardown: Voggle (weird-history Shorts)

**Pick.** vidiq_outliers (Shorts, "conspiracies, mysteries and strange history", 5K-400K subs, 100K+ views) returned 30
hits. Voggle (`UCOGuvK0sWCY-Vq9oQFwlAYg`, 60.9K subs, AU) is the closest rival to us: Shorts only, photo cut-outs with
cartoon eyes and mouths (our v4 look), one narrator, strange true history. Its Mike the Headless Chicken is the 363x
outlier already in research/48.
**Credits: 35** (outliers 5, video metadata 5, 2 × watch_shortform 20, 1 transcript 5). Balance 553 → ~518. Free:
yt-dlp channel listing (27 Shorts, view counts) and auto-captions for 2 Shorts. YouTube now bot-walls yt-dlp video
downloads from our egress ("Sign in to confirm you're not a bot"), so frames came from vidIQ's watch, not local files.

### The channel
27 Shorts, **median 27K views**. Shorts only (no long-form tab). Top 5:
| Short | Views | Outlier | Length | Likes/views | First line (verbatim) |
|---|---|---|---|---|---|
| The True Story of Mike the Headless Chicken | 2.72M | 363x | 2:53 | 10.1% | "The axe cut off the rooster's head, but as it dropped into the dirt..." |
| They Brought Slugs Into War | 1.44M | 530x | 1:26 | 8.9% | "They took a slug into the trenches and put the sloppy little slime ball on lookout." |
| They Taught a Horse Math | 846K | 186x | 2:16 | 12.0% | "The horse tapped out the answer to each maths problem with his hoof..." |
| The King's Ship Sucks (Vasa, 1628) | 374K (1 day) | 40x | 2:21 | 4.9% | "30 men sprinted back and forth across the deck of the brand new warship..." |
| The Best Day Out in Texas (Crash at Crush) | 350K | 8.8x | 2:28 | 4.1% | "The trains smashed head-on at full speed, and both boilers exploded..." |
| *The Emu War (contrast)* | *9.5K* | *2.9x* | *2:13* | *5.4%* | — |

### Findings
1. **Hook = the most physical moment, mid-action, past tense (5/5).** No topic label, no question, no verdict, no date.
   The date comes later, in a rewind: "See, during World War I..." (0:21), "See, in 1896..." (0:11), "See, the ship
   belonged to King Gustav..." (0:27). Ours: `tools/coldopen.py` finds a scene-first line 1 in **5 of 83** scripted
   Shorts across the pilot, TikTok packs 1-2 and all v4 scripts; **1 of the 6 pilot cases** (emuwar), and none of the
   5 that open on a verdict or label ("The Roswell cover-up was real.", "In 1518, a town couldn't stop dancing.").
2. **Pacing is not the gap.** Shot changes listed by vidIQ: Mike 88 in 173 s = **5.1 per 10 s** (9 in the first 10 s),
   Clever Hans 60 in 136 s = **4.4 per 10 s**; about 2 s a shot. Narration is continuous at **182-191 words a minute**
   (captions, slugs 271 words/85 s, Texas 445/147 s). Our v4 renders already run 14 visual events per 10 s (pangolin,
   longest gap 2.1 s). vidIQ's own summary line said "3.1 cuts per 10 s" for Mike, which its list contradicts.
3. **The verdict is one plain sentence, not a stamp, and it lands mid-video.** Mike: "Mike wasn't a miracle. He'd just
   been really, really badly beheaded." at 1:13-1:38 (42-57%), over an anatomy diagram. Hans: the psychologist "stopped
   watching the horse and started watching the humans" at 1:05-1:35 (48-70%), POV through binoculars, music drops to a
   tick-tock bed, a chime on the reveal. Same window as openloop.py's 50-80% rule.
4. **They end on an ironic kicker, no CTA, no loop line.** "...killed his golden goose" (cut to a goose on stage);
   Crush "fired... and the next day, quietly hired him back"; the Vasa captain "was eventually promoted"; von Osten
   "died still totally convinced". Every pilot case ends on "Did you guess right? Comment."
5. **Fame does not carry a topic.** Their Emu War, the most famous story they've told, is their 15th-best at 9.5K
   (0.35x median). The obscure ones (WW1 gas-detector slugs, Clever Hans) are their top 3. Emu War is #4 on our
   research/48 list and one of the 6 pilot cases. [I] One rival, one data point: it is a warning, not a verdict.
6. **Length: 86-173 s (mean 2:13).** Every hit is a long Short: well past TikTok's 60 s Creator Rewards bar. Our
   E19 cases are 14-18 s by word count.
7. **Titles and descriptions:** 3-6 plain words, wry, no emoji, no hashtags ("They Taught a Horse Math", "The King's
   Ship Sucks"); the description does the search work in one sentence: "This is the [bizarre/unlikely] true story of
   [name], [what], in [place] in [year]." Thumbnails are auto frames.
8. **Music and voice:** a human British male narrator, mid-tempo storyteller with comic asides ("nominative
   determinism"). Music is comic, not spooky: fingerpicked banjo (Mike), ragtime pizzicato/accordion (Hans), switching
   to tense strings only for the dark turn (Mike's death). For the per-topic theme system: strange history = comic
   pizzicato bed ("detective"), the mystery bed only for real unsolved/creepy cases.

### The build
1. **`tools/coldopen.py`** (new, standalone; exit 1 on fail): C1 scene-first line 1 (past-tense verb; no `?`, verdict
   or stance word, date-first opening or hook stamp), C2 a rewind cue at 5-40% of the words, C3 `"kicker": true` on the
   last story line. FAIL for 45 s+ groups, WARN under 45 s (research/38's claim-first finding still governs 20-25 s
   Shorts; `"cold_open": "claim"` marks a deliberate choice). Tested: 5/5 Voggle hooks pass C1; pilot exits 0 with
   warnings; the pangolin prototype and TikTok pack 1 fail (no rewind, no kicker).
2. **`scripts/investigates-a119-moon-bomb.json`**: a Meatball Investigates case in Voggle's shape. Project A119, the
   1958 US Air Force study on setting off a nuclear bomb on the Moon (turned-out-TRUE, Cold War, research/48 #8).
   - 0:00 "A physicist in Chicago worked out how to set off a nuclear bomb on the Moon."
   - "Opening the file." → "See, in 1958, the Soviets had just launched Sputnik."
   - decoys: a moon base (no), aliens ("I checked. No aliens in the file. Phew."); re-hook "Wait. The flash had to be
     visible from Earth."
   - payoff at 54%: "It was a warning." PROVEN stamp.
   - Meatball: "The Moon is round. I'm round. I'm taking this personally."
   - kicker: "the world only found out because Sagan mentioned the secret project on a fellowship application."
   - 189 words, ~65 s, `"theme": "conspiracy"`. Passes coldopen.py and openloop.py. Photos TBD (NASA PD); the
     factdesk must verify 4 sources, especially the Sagan detail. Concept only: not rendered, not scheduled.

### Proposed experiment (for the Mayor; one variable)
E-CO: after E19's first 6 cases, make 3 cases 60-75 s long in the cold-open shape (scene line 1, rewind, kicker) and
post them as TikToks against the 3 E19 TikToks before them. Metric: average watch time and the share of views past 60 s.
Keep it if watch time is +10% or better. YouTube 9:30 cases stay 20-25 s claim-first until E19 is scored.

## 2026-10-28 — c. Platform rule: YouTube "inauthentic content" (template sameness)

### The finding
- On 2026-07-16 YouTube clarified that three kinds of "inauthentic content" can't earn in YPP. Matt Halprin (trust and safety) announced it on Creator Insider; TechCrunch covered it 7/20.
  1. Generic, repetitive or template-based videos, "easy to mass-produce with AI, CGI or templates, with little variation", that "don't really have a narrative arc".
  2. Distressing or manipulative bait, e.g. staged animal rescues.
  3. AI personas giving health, finance or legal advice.
- A channel with "too much" of any bucket can't monetize. YouTube gives no number for "too much" and sets no upload-volume limit. AI itself is allowed: "you can create a higher volume of high-quality content that we want to encourage".
- Sources: https://techcrunch.com/2026/07/20/youtube-clarifies-policies-around-ai-slop-and-upsetting-videos/ ;
  https://www.androidheadlines.com/2026/07/youtube-monetization-rules-ai-slop-inauthentic-content.html
- What this means for us:
  - Bucket 2: we're safe. We stage no distress or rescues.
  - Bucket 3: we're safe. Meatball is a cartoon and gives no advice.
  - Bucket 1 is the live risk, because the reviewer looks at a channel, not one video.
  - It answers Nolan's 10/28 question "are we posting too much". Volume isn't penalized; sameness is.
- Audit of 55 drawn outlines (`tools/sameness.py`):
  - 32 distinct YT skeletons. The most common, hook-name-fact-xray-escalate-calm, appears 5 times.
  - The batch started 10/28 was converging on hook-solo-solo-solo-solo-solo-solo-punch: drain fly, fruit fly, carpet beetle and polar bear.
  - Stock lines: "Here's the weird part." and "Now the gross part." are each in 4 outlines.
  - Hook and title openers: "This bird/fish/animal..." 10 times.
  - TikTok cuts are fine: 54 distinct skeletons out of 55.

### The build
1. **`tools/sameness.py`.** It runs on its own and exits 1 on a FAIL.
   - S1 (FAIL): exactly the same macro skeleton as 3+ other outlines in the same cut.
   - S2 (WARN): the hook's first two words are shared by 25% or more of outlines.
   - S3 (WARN): the title's first two words are shared by 25% or more of outlines.
   - S4 (WARN): the same sentence appears in 3+ outlines; subscribe lines are exempt.
   - With no arguments it reports on every outline.
   - Tested: moose passes; octopus fails S1, as expected.
2. **`tools/drawn_quick.py`.** It now runs the gate before rendering and refuses on S1 unless `--force` is given. Already-rendered and scheduled cuts are left alone.
3. **Contrarian alert.** Sent to the producer batch: vary the YT beat order from the next outline on, and drop the two stock lines.

### Proposed rule (for the Mayor)
- Before 11/15, when the monetization review window opens, no two Shorts posted on the same day share a skeleton.
- No hook opener is used more than twice a week.
