# Packaging & Search playbook

Desk id: `packager`. Absorbs: Thumbnail Artist, Packager, SEO Specialist. Read this before every run and append lessons after.

## Read first
- research/25 thumbnail spec v4
- research/37 packaging and conversion
- research/34 vidIQ playbook

## Rules (proven)
- Score 3 title candidates (vidiq_score_title); keep the best ACCURATE one. Rejected a 98 that contradicted the episode.
- Claim-style titles beat bare "How/Are X?" (Dog breeds: 82 to 92).
- Thumbnail B beat A on every episode (vidIQ, 10/24). vidIQ refuses GitHub URLs, so send thumbnails inline at about 192 px.
- Test & Compare is long-form only, desktop only, with no API: Nolan adds the B thumbnail after an episode goes live.
- Every episode: pinned answer key, chapters, an end screen; every Short: a Related video link and a claim title.

## KPIs this desk owns
- Title score deltas
- CTR on episodes
- Title test log (data/title-tests.csv)

## Lessons log (newest last; date, what happened, what we learned, the number)
- 2026-10-24: desk created by merging the roles above.
- 2026-10-24 (marketing desk, 35 credits): claim titles beat question titles again on 3 Shorts. Koala 79→84 and bats 84→92 (dropped "TRUE or FALSE") were updated in Metricool. Hippo 91→95 (+4) was kept because it missed the +5 bar. Log: data/title-tests.csv. vidIQ keyword "are koalas bears" <750/mo, but "koala bear" is 8.4K/mo, so put the common (wrong) phrase in a claim title.

## Meatball-system thumbnails v2 (2026-10-24, research/42 §2)
Tool: `tools/thumbnail.py --photo inat:ID --pose shock|terror|disgust|smug --text "≤3 WORDS" --out x.jpg [--layout left|right] [--crop ...] [--flip] [--arrow auto]`. Writes `x_168.jpg` and `x.credit`; refuses CC BY-SA photos, >3 words and quiz/score text. The old frame-grab tool is now `tools/frame_thumb.py`.

vidIQ `score_thumbnail` (192 px WebP data URI, carrier gFhrONKK0rI, live Metricool title), 13 calls = 65 credits:

| Episode | Current in post | v2 variants | Kept as thumb_v2 | Action |
|---|---|---|---|---|
| myths-05 (10/26) | thumb_b **49** | wombat "CUBE POOP?" 45 · elephant "CAN'T JUMP?" 41 | wombat | keep thumb_b |
| myths-03 (10/27) | thumb_b **40** | shark "JAWS LIED?" 39 · hyena "LION KING LIED?" 27 | shark | keep thumb_b |
| myths-06 (10/28) | thumb_b 25 | dog "SEES COLOR?" **57** · cat "NO MILK?!" 42 | dog | **swapped in Metricool** |
| myths-07 (10/29) | thumb 20 | widow "OVERRATED?" **31** · widow "NOT DEADLIEST?" + arrow 25 | widow | **swapped in Metricool** |

Lessons:
- A face-forward subject with eyes (the dog) scored best of everything, and got the only "genuine expression" bonus. Profile animals with no visible eye (wombat, shark, spider) score 20-45 points lower.
- vidIQ reads Meatball's face as the face. Smug (deadpan + smile) beat shock and disgust in both episodes that tested it.
- vidIQ never complained that the subject was too small. It did complain twice that "Subject is too dominant" (wombat, elephant), so a big subject alone doesn't help.
- The red arrow didn't help: 07 with the arrow scored 25 vs 31 without it.
- rembg isnet fails on animals in water (platypus, open-water shark) and on dark spiders on dark ground (funnel-web). Pick photos with a contrasting background before writing copy. bria-rmbg needs about 9 GB of RAM, which is too much on the shared box.
- The remaining penalties are "too busy" (the rays) and "negative space". Next test: `--no-rays` on a front-facing subject.
- 2026-10-25 (marketing desk, 25 credits): 10/26 long-form title said "Are 100% Real" while 3 of its 12 are fakes (inaccurate). "Weird Animal Facts You Didn't Know (3 Are Fake. Can You Spot Them?)" scored 98 vs 88 and is accurate, so it was swapped in Metricool (date read back 10/26 14:00; tag "animal facts you didn't know" added, 8.8K/mo, +39%). Badger Short: claim version 84 vs 83, kept. A 30-credit run covers 1 trend pull + 1 keyword pull + 2 title pairs, not 6 titles: score current+alt only where the current title is weak or inaccurate.
- 2026-10-25 (Sunday Summit): weird-pivot titles follow the breakouts: a concrete impossible thing + who/when ('The Chess Robot That Caught Napoleon Cheating', 6.4M; 'The True Story of Mike the Headless Chicken', 2.7M). Long-form case titles = the search phrase ('cold war secrets' 13.5K/mo, +91%, comp 42; 'operation northwoods' 33.7K, +51%).
