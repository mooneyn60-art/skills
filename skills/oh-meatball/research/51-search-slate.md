# 51 · Search-first long-form slate (Growth desk, 2026-10-26)

**Why search, not feed.** Our long-forms have 102 views between them (yt-dlp 10/26: wolves 55, animal-facts 39,
extinct 4, 12-myths 4) while our Shorts have about 14,900. Browse/Suggested hasn't picked up a single
long-form. A video that answers a question people type gets a second chance every day through search. Each case
long-form is also the page the case Shorts' Related video can point to (data/related-video-map.csv). One search hit
at 5k-50k views and 3 min AVD is 250-2,500 watch hours. That's the only realistic path to the 4,000 h (research/31).

**Rules for every slate episode** (adds to OPERATIONS "Long-form reset" and research/47):
- The title starts with the searched phrase, word for word, then the promise. Max 60 characters before the brackets.
- Say the searched phrase in the first 10 s and put it in the first description line. Chapters named with the
  sub-questions people search ("What happened to Flight 19?").
- Every case gets a verdict stamp. Sources go in the description. The red list applies (OPERATIONS).
- 5:00-7:00 and `tools/retention.py` must pass (R1-R7). One theme per episode (tools/themes.py).
- The thumbnail follows research/42 §2 and research/48 §4: Meatball's face, one archival image, 1-3 words.
- Publish it first, then cut 3-6 case Shorts from it, so each Short's Related video points at it on day one.

**Keyword numbers** are vidIQ estimates (10/26 pulls in this file, plus research/48 §1b). Volume is estimated
monthly YouTube searches. Competition runs 0-100, lower is easier. Growth is search demand vs the prior period.
Caveat: some head terms draw a large share of searches from PK, IN or VN (vidIQ topMarkets). That audience is
real, but it earns a lower RPM than the US.

## The slate (ranked by demand × winnability × how cleanly Meatball can give a verdict)

| # | Title (search phrase first) | Keyword evidence | Theme | Verdict shape | Status |
|---|---|---|---|---|---|
| 0 | **Conspiracy Theories That Turned Out To Be TRUE** | "conspiracy theories that are true" 55.6K/mo, comp 51; "conspiracy theory" 96.6K, **+44.7%** (research/48) | cold-war | PROVEN ×4 | **Rendered, not queued.** Publish first (research/51 lever 1) |
| 1 | **Is the Bermuda Triangle Real? Every Famous Disappearance, Checked** | Top-15 median **2.98M views**, top 32.2M (research/48 §1c, the biggest demand of any case); our Case #1 Short is already on it | ocean-mystery | BUSTED overall, one still odd (USS Cyclops) | **Scripted:** `scripts/longform-bermuda-triangle.json` (retention.py passes) |
| 2 | **The Lost Colony of Roanoke: What Really Happened?** | "the lost colony of roanoke" **73.7K/mo, +64.7%**, comp 59; "croatoan" 18.8K, **+392%**, comp 42; "roanoke lost colony" 19.9K, **+386%**, comp 47; "what really happened to roanoke's lost colonists" 14.0K, comp 48 | strange-history | UNSOLVED, with the best evidence (Hatteras/Croatoan finds) | **Scripted:** `scripts/longform-roanoke.json` (retention.py passes) |
| 3 | **Historical Mysteries That Still Can't Be Solved** (5 cases, best last) | "historical mysteries" **181K/mo, comp 39** (the lowest competition of any big head term we've measured); "unsolved mysteries" 475K, comp 62 | strange-history | UNSOLVED ×5, honest "best explanation" for each | Next |
| 4 | **What Really Happened to Rome's Lost Ninth Legion?** | 18.2K/mo, comp 49 (the "what really happened" pull) | strange-history | UNSOLVED (likely disbanded or lost in the east, not wiped out in Scotland) | Next |
| 5 | **What Really Happened to the Neanderthals?** | 19.9K/mo, **+122%**, comp 43 | science-myth | EXPLAINED (they interbred with us; 1-2% of many people's DNA) | Next |
| 6 | **What Really Happened to Dead Bodies in the Old West?** | 13.1K/mo, **+223%**, comp 36 | absurd-history | TRUE (embalming, "ice" coffins, propped-up outlaw photos) | Next. Gross history wins (research/28); no real victims' faces |
| 7 | **The Green Children of Woolpit: History's Strangest Mystery** | "where did the green children of woolpit come from?" 5.2K/mo, **comp 29** | strange-history | UNSOLVED, best explanation (illness/diet, Flemish refugees) | Next. Low volume but nearly no competition |
| 8 | **The Weirdest Wars in History** (Emu War, Pig War, War of the Bucket, the 38-minute war) | "weird history" 437K/mo, comp 62; "weird history facts" 28K, **comp 46, +29.5%** (research/48); Emu and Pig War case Shorts already made | absurd-history | TRUE ×4 | Next. Its case Shorts need a home |

Already scripted elsewhere: **Secret Cold War Projects That Were Actually Real** ("cold war secrets" 13.5K, comp 42,
+91%; `scripts/longform-cold-war-secrets.json`, Tue 11/10).

**Skipped on purpose:** the celebrity "what really happened to [person]" rows. They are 60% of the
"what really happened" pull. They involve living people, and the red list rules them out. Also skipped:
"history for sleep" (998K, comp 40). It's real demand, but it needs 1-3 h calm narration, which isn't our format.
research/51-growth-levers.md lever 11 has a compilation test instead.

## Hand-off
- **Showrunner:** the top two are written in the house long-form shape: cold-open promise, `counter` chapters, best
  case last, a twist or jeopardy beat at least every 75 s, the early ask kit, one theme. Both pass `tools/retention.py`. Punch up the jokes
  against research/39 before rendering (TOWN standing duty).
- **Factdesk:** every `wm:` and `ov:` photo in both scripts is a candidate. Licence-check each one (PD/CC0/CC BY, no SA)
  and confirm it matches its line before the render. The facts are in each script's `sources`.
- **Runtime check:** both estimate 5.2-5.6 min at the Kokoro pace that retention.py assumes. Themed edge voices run faster (atempo 1.12), so after the render run `retention.py SCRIPT --timeline WORK/timeline.json`. If it is under 5:00, add one beat to the shortest chapter.
- **Studio:** render with `episode.py scripts/longform-<slug>.json <slug> --skip-shorts`, one job at a time, then
  `rm -rf /tmp/meatball-build/<slug>` (disk is tight).
- **Packager:** 3 thumbnails each (research/42 §2), scored with vidIQ. Titles stay the search phrase as written above.
- **Postmaster:** queue the long-form in a Tue/Sat 14:00 slot, then its Shorts. The Related video map gets a row per Short.
