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

**Next night: b** (competitor teardown).

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
