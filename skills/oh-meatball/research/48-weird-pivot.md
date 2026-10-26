# 48 · Meatball Investigates the weird: pillars, mix, packaging, pilot (Showrunner, 2026-10-26)

**Brief (Nolan, after outside opinions):** "Animals are too boring. We need weird topics people will find interesting:
strange facts, myths, include conspiracy theories, anything that grabs and holds attention."
**Answer in one line:** keep Meatball, the channel and the voice; change the promise to **"Meatball investigates the
weird, and tells you what's actually true."** Conspiracies and mysteries lead, strange history follows, and animals stay
as one pillar for the strongest ones only.

**Credits:** vidIQ **25** (outliers ×2 = 10, keyword research ×2 = 10, one youtube_search that errored but was charged = 5).
Balance 625 → 600. Free sources on top: yt-dlp search of the top 15 YouTube results for 24 topics (views, length), the
Wikipedia/Commons file metadata for every photo. `vidiq_generate_music` costs 25 credits a track (over the 15-credit cap),
so the music is original and procedural instead (tools/music.py, §6).

## 1. Evidence

### 1a. vidIQ outliers (last month for Shorts, last 6 months for long-form)
**Shorts (≥50K views):** strange-history and "unexplained" Shorts from tiny channels break out hardest.
| Short | Channel size | Views | Breakout |
|---|---|---|---|
| Worlds Oldest Murder (dark history) | 694 subs | 860K | **2,899x** |
| How monks ACTUALLY mummified themselves alive (3D animation) | 386 subs | 620K | **665x** |
| They Could Have Changed the World… Then Vanished | 15K | 4.2M | 488x |
| Amelia Earhart's plane location remains a mystery | 313K (news) | 417K | 438x |
| The True Story of Mike the Headless Chicken (2:53) | 61K | 2.7M | 363x |
| The Story of Carlos Hathcock's Impossible Shot: MythBusters Got It Wrong Twice | 772 subs | 1.8M | 317x |
| People That Science Still Cannot Explain | 7K | 3.3M | 261x |
| Bob Lazar: "They View Us as CONTAINERS" (UFO clip) | 1.5K | 411K | 134x |
| Top Places In The World Where People Vanish | 3.9K | 142K | 101x |
| Fish Fall From the Sky in This Town | 112K | 2.7M | 64x |
| Scientists Dug 7 Miles Deep… Then Heard Screams From HELL (the Kola "Well to Hell" hoax, told as true) | 60K | 569K | 29x |

**Long-form (channels <500K subs):** mystery compilations and declassified-history explainers.
| Video | Channel | Views | Breakout |
|---|---|---|---|
| Banned History Facts Schools Refuse to Teach (62 min) | 1.1K | 246K | **2,547x** |
| Roswell: Aliens, UFOs, Secret Weapons or a Government Cover-Up? | 30K | 524K | **1,222x** |
| 3 Creepy Emergency Calls That Were Never Solved | 1.9K | 209K | 742x |
| 25 of America's Strangest Mysteries & Bizarre True Stories | 2.5K | 219K | 678x |
| U-530: The U-Boat that Escaped to Argentina | 1.5K | 223K | 494x |
| FBI's Secret Files: The Argentina Escape | 39K | 555K | 485x |
| Conspiracies that Turned Out to be True (81 min) | 22K | 682K | 52x |

Read: the winners are **(1) a real record or document that sounds impossible, (2) a promised verdict** ("Case Closed",
"Turned Out True", "MythBusters Got It Wrong"), **(3) archival images**. Many of the long-form hits are AI-labeled, hour-long
"documentary for sleep" slop with weak sourcing: our edge is a character, a verdict and real sources, in 5-7 minutes.

### 1b. Search demand (vidIQ keyword research, monthly searches)
| Keyword | Est. monthly searches | Competition | Trend |
|---|---|---|---|
| weird history | 437,029 | 62 | -16.5% |
| conspiracy theories | 193,635 | 66 | -15.7% |
| conspiracy | 126,329 | 71 | -3.2% |
| conspiracy theory | 96,596 | 65 | **+44.7%** |
| weird facts | 96,443 | 50 | -31.3% |
| conspiracy theories that are true | 55,586 | 51 (low for its size) | -57.4% |
| operation northwoods | 33,729 | 63 | **+50.9%** |
| weird history facts | 27,968 | **46** | **+29.5%** |
| urban legends that turned out to be true | 16,966 | 70 | -17.6% |
| operation mockingbird | 17,040 | 48 | +1.8% |
| cold war secrets | 13,532 | **42** | **+91.1%** |
| conspiracy theories that turned out to be true | 12,842 | 70 | -16.8% |
| history explained | 724,101 | 55 | +27.9% |

### 1c. Topic demand: top 15 YouTube results per topic (yt-dlp, free, 2026-10-26)
Median views of the top 15 results is the demand signal; the top video shows the ceiling; "Shorts" counts results ≤3 min.

## 2. The 20 topics, ranked
Score = demand (median/top views, searches) × outlier strength × how cleanly Meatball can deliver a verdict, minus policy risk.

| # | Topic | Pillar | Median views (top 15) | Top video | Outlier / search signal | Verdict type |
|---|---|---|---|---|---|---|
| 1 | **Bermuda Triangle** | Mystery | **2.98M** | 32.2M | "Places where people vanish" 101x | BUSTED |
| 2 | **Area 51 / Roswell** | Conspiracy | 0.76M | 15.3M | Roswell doc **1,222x**; Lazar clip 134x | Cover-up TRUE, aliens BUSTED |
| 3 | **MKUltra** | Turned out true | 1.12M | 6.3M | "turned out true" 55.6K/mo | PROVEN |
| 4 | **Great Emu War** | Strange history | 0.33M | 28.7M | top Short 1.1M | TRUE |
| 5 | **Mike the Headless Chicken** | Strange history | 0.03M | 3.2M | Short **2.77M**, Voggle 363x this month | TRUE |
| 6 | **Operation Northwoods** | Turned out true | 0.01M | 2.2M | **33.7K/mo, +50.9%** | PROVEN |
| 7 | **Moon landing hoax** | Conspiracy | 0.61M | 9.9M | evergreen | BUSTED |
| 8 | **Amelia Earhart** | Mystery | 0.44M | 15.4M | Shorts 438x and 171x this month | UNSOLVED (best evidence) |
| 9 | **Loch Ness** | Mystery | 0.53M | 2.5M | | BUSTED (eDNA study) |
| 10 | **Kola Superdeep / "Well to Hell"** | Mystery / hoax | 0.16M | 12.2M | "screams from hell" Short 569K, told as true | BUSTED |
| 11 | Mandela effect | Everyday myth / brain | 0.33M | 3.5M | | EXPLAINED |
| 12 | Denver Airport | Conspiracy | 0.32M | 4.1M | | BUSTED |
| 13 | Birds Aren't Real (satire) | Conspiracy (joke) | 0.25M | 5.8M | 3 Shorts in top 15 | SATIRE, said plainly |
| 14 | Dyatlov Pass | Mystery | 1.47M | 8.5M | | BEST EXPLANATION (avalanche); handle with care, 9 deaths |
| 15 | Voynich manuscript | Mystery | 0.19M | 10.3M | | UNSOLVED |
| 16 | Tarrare | Strange history / body | 0.13M | 20.6M | | TRUE |
| 17 | Dancing Plague of 1518 | Strange history | 0.09M | 2.6M | Short 0.21M | TRUE |
| 18 | Great Molasses Flood | Strange history | 0.09M | 3.1M | | TRUE (21 deaths, 1919: respectful) |
| 19 | Gulf of Tonkin | Turned out true | 0.08M | 2.0M | "cold war secrets" +91% | PROVEN |
| 20 | Acoustic Kitty (CIA spy cat) | Turned out true | <0.01M | 0.2M | low demand, great hook | PROVEN |
Also weak: Titanic switch theory (top 1.2M, 4 tiny Shorts), Paul is dead (median 0.05M). Lightning-strikes-twice and other
everyday myths have no single-topic demand, but "weird facts" (96K/mo) and "myths" carry them; they are cheap fillers.

**Top 10 for the next month:** Bermuda Triangle, Roswell/Area 51, MKUltra, Emu War, Mike the Headless Chicken,
Operation Northwoods, moon landing, Amelia Earhart, Loch Ness, Kola "Well to Hell".

## 3. Pillars and mix (the data decides)
| Pillar | Share | Why |
|---|---|---|
| **Conspiracies and mysteries, investigated** (incl. "turned out TRUE") | **40%** | Highest demand by far (Bermuda 2.98M median; "conspiracy theory" +44.7%); long-form outliers are almost all here. Every one ends with a verdict stamp |
| **Strange history, weird science and the body, everyday myths** | **35%** | The biggest *Shorts* breakouts from tiny channels (2,899x, 665x, 363x); "weird history facts" has low competition (46) and +29.5% growth. Everyday myths sit here at ~1 in 10 videos as cheap fillers |
| **Weird animals** (strongest only: deadliest, weirdest bodies, animal mysteries) | **25%** | Our only proven Shorts audience (6,002 views in 30 days, research/42); keep it so we don't lose it. Prefer animals that touch the new promise (Emu War, Mike the chicken, "animals science can't explain") |
The proposed 40/30/30 moves 5 points from animals to history because history Shorts outperform in the outliers.
Re-score after 3 weeks (OPERATIONS.md experiment rules): each pillar must hold the channel median Shorts views.

**Turned-out-true is the safest, strongest sub-format:** it is real (documented, declassified), it gets the conspiracy
click, and the verdict is PROVEN, so it never risks presenting a false theory as true.

## 4. Rebrand without confusing YouTube
- **Keep:** the channel, its name "Meatball Myths" (myths still fits: we check them), the handle, Meatball, the voice, the
  look, Tuesday/Saturday long-forms. YouTube clusters by who watches, not by labels (research/42 §1), and the same host and
  packaging keeps the audience one audience.
- **Change the promise:** banner and About to "Meatball investigates the weird: myths, mysteries and conspiracy theories,
  and what's actually true." The subscribe line becomes "Subscribe. I investigate something weird daily."
- **One series name everywhere: "Meatball Investigates"**, with a running case number ("CASE #12"). Built in as reusable
  features (§6): a case-file tag on every frame, a case-file card + sting on the hook, verdict stamps, evidence boards.
  Playlists: "Meatball Investigates: Conspiracies", "...: Turned Out TRUE", "...: Strange History", "...: Weird Animals".
- **Transition:** for 2 weeks, alternate (weird, animal, weird) so the existing Shorts audience is carried over, then go to
  the 40/35/25 mix. Animal Shorts also get the series tag ("CASE #: Do Bats Really...").
- **Titles:** the searched topic first, then the promise. Patterns that win in this niche:
  1. "**X** Was REAL" / "The Conspiracy That Turned Out TRUE" (Northwoods, MKUltra)
  2. "What REALLY Happened at **X**?" / "What REALLY Crashed at Roswell?"
  3. "Is **X** Real?" (Bermuda Triangle, Loch Ness): a question with a promised verdict
  4. "**X**: Scientists Still Can't Explain…" only when it's true (Voynich); never for solved cases
  5. "The **X** of 1518 Was REAL" (year + REAL for strange history)
  Never "PROOF aliens exist", never "they don't want you to know" for a false theory.
- **Thumbnails** (research/42 §2 still applies): Meatball's huge reacting face + ONE archival image (a document, a
  balloon, a ship, an engraving) + a red verdict stamp or "CLASSIFIED" as the 1-3 words ("IT WAS REAL", "BUSTED",
  "CASE CLOSED"). Red string or a circled detail is the niche's visual shorthand. No fake "caught on camera" images,
  no AI "alien" images.

## 5. Policy and honesty rules for this pillar (YouTube misinformation and harmful-content policies)
1. The payoff is always what the evidence says. A debunk is stamped BUSTED and said plainly; "turned out true" only for
   documented, declassified or court/Congress-confirmed facts (sources on every hook beat).
2. Never: medical or vaccine conspiracies, elections, anything targeting a group, real private people, recent tragedies or
   mass-casualty events (9/11, shootings, recent disasters). Old tragedies (Molasses Flood, Dyatlov) only with respect,
   no jokes about the victims.
3. Satire is labelled as satire in the video (Birds Aren't Real: "it's a joke, and the joke is the point").
4. Photos: public domain (US government, NOAA, NASA, NARA, pre-1930 art), CC0 or CC BY only, credited; no share-alike for
   cut-outs; public officials only in public-domain government or press photos; no identifiable private people.
5. AI label on. No door-cam or fake-camera footage. No invented quotes (we paraphrase and cite).

## 6. What was built (tools)
- **tools/investigate.py** (new) + hooks in **tools/v3.py**, all driven by script fields:
  - spec `"series": {"text": "MEATBALL INVESTIGATES"}` + hook `"case": "CASE #3"`: a case-file tag top left on every frame
    (so the loop seam still matches) and a manila case-file card that drops in on the hook with a "case" sting
    (typewriter clacks into a low dun-DUN, synthesized).
  - beat `"stamp": {"text": "BUSTED", "at": "word"}`: a worn rubber stamp slams onto the picture with a thud and a shake.
    TRUE/PROVEN green, FALSE/BUSTED/CLASSIFIED red; `"reveal": false` for a hook stamp that shouldn't drop the music.
  - shot `"board": {"notes": [...], "stamp": "CLASSIFIED"}`: the photo becomes a pinned polaroid on a cork evidence board
    with index-card notes tied on with red string.
  - spec `"captions": "bold"`: Inter Black, 12% bigger, thicker outline.
- **tools/music.py** (new): original procedural beds rendered to each video's own timeline, CC0 by us. Main bed
  **"mystery"** (Nolan 10/25: intriguing, mysterious): a low pulsing bass in eighths, clock ticks, plucked minor-second
  tension, an airy pad, a slow build that **rises into each reveal, drops out for 0.42 s right before the verdict stamp**,
  then a low boom + bell hit on the stamp; the end crossfades into the start (loop-safe). Alternate **"detective"**: a
  lighter curious pizzicato (walking pizz bass, staccato pizz tune, snaps). Mixed by loudness: voice -16 LUFS, music
  -20 LUFS ducked under the voice, master -14 LUFS. Pick per Short with hook `"music": "gen:mystery" | "gen:detective"`.
- **tools/explainer.py**: `"obs": "wm:File name.jpg"` fetches a Wikimedia Commons file (licence read from the file page;
  PD/CC0/CC BY only), as a standard thumbnail because Commons refuses originals to our shared egress; licences already
  verified are cached in `data/wm-licenses.json` so a 429 storm doesn't stop a render. `ov:` Openverse items hosted on
  Commons now take the same thumbnail path.
- **tools/episode.py** passes `series`, `captions` and a per-hook `music` to each Short; Short descriptions take
  `short_hashtags` and `photo_source` from the spec.

## 7. Pilot pack (episodes/weird-pilot/, scripts/weird-pilot.json): NOT scheduled, for Nolan
| Short | Pillar | Verdict | Music |
|---|---|---|---|
| short-bermuda | Mystery (debunk) | BUSTED | mystery |
| short-northwoods | Conspiracy that turned out TRUE | TOP SECRET → PROVEN | mystery |
| short-roswell | Conspiracy (mixed) | COVER-UP TRUE + ALIENS BUSTED | detective |
| short-emuwar | Strange history | EMUS WIN | mystery |
| short-dancing | Strange history | TRUE | detective |
| short-lightning | Everyday myth | FALSE | mystery |
Plus `compare.mp4`: a pilot Short beside a current animal v4 Short. Ask kit early on every one (guess card ~3-6 s,
subscribe pill ~6-10 s, reminder before the loop).

## 8. Ten long-form ideas (5-7 min, tools/retention.py structure: cold-open promise, counter, best case last)
1. **Conspiracy Theories That Turned Out To Be TRUE** (scripted: `scripts/longform-turned-out-true.json`, passes the gate):
   Acoustic Kitty → Gulf of Tonkin → Operation Northwoods → MKUltra (5 → 1 countdown).
2. **Is the Bermuda Triangle Real?** Five famous disappearances, each checked; verdict BUSTED, with the one that's still odd.
3. **What REALLY Crashed at Roswell?** 1947 → Project Mogul → the 1990s Air Force reports → Area 51's spy planes.
4. **The Weirdest Wars in History:** the Emu War, the Pig War (1859), the War of the Bucket, the Anglo-Zanzibar war (38 min).
5. **Strange Plagues That Really Happened:** Dancing Plague 1518, Tanganyika laughter epidemic 1962, the June Bug epidemic.
6. **Did We Really Land on the Moon?** The hoax claims vs the evidence: retroreflectors still in use, LRO photos of the sites,
   382 kg of moon rock (NASA public-domain images throughout).
7. **The Mandela Effect, Explained:** why whole crowds misremember (memory research), with Meatball misremembering his own sauce.
8. **Secret Cold War Projects That Were Real:** Project Iceworm, Acoustic Kitty, Project A119 (the plan to nuke the Moon),
   Operation Popeye (weather control) ("cold war secrets" +91%).
9. **The Deepest Hole on Earth and the "Well to Hell" Hoax:** the Kola borehole's real science, then the hoax's origin.
10. **Animals That Fooled Scientists:** Mike the Headless Chicken, the platypus "hoax", the coelacanth (bridges the
    animal audience into the new show).

## 9. How we'll know
- Pilot: post 2 weird Shorts per day beside 1 animal Short for 7 days after Nolan picks the music; compare views/48 h,
  engaged view %, subs/1K (OPERATIONS.md experiment row).
- Keep the pivot if the weird Shorts' median views ≥ the animal median and subs/1K ≥ 3; kill a sub-pillar whose 3 Shorts all
  land under half the median.
- Long-form: "Conspiracy Theories That Turned Out To Be TRUE" judged by the research/47 bar (AVD > 2:00, 0:30 retention > 60%).
