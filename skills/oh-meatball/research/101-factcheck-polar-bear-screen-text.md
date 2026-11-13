# 101 - Check of the polar bear long video's on-screen text, description, tags, pinned comment and thumbnails (2026-11-13)

A second model (not the builder, not the writer) checked everything research 99 did not: the text the builder drew beyond the cards (`tools/drawn_pb_shots.py`, the board and scene functions of `tools/drawn_pb_art.py`), the pictures that state a fact without words, `episodes/longform-born-as-polar-bear/description.txt`, `tags.txt`, `pinned_comment.txt`, and the three thumbnails `pb_a`, `pb_b`, `pb_c`. What a viewer sees was read from `lines-contact-1.jpg` to `-4.jpg`. Facts: `research/98`. Rules: MASTER_ORDERS ("Watch hours", "Direction change", "Tags and everything", "The YouTube play").

"Covered by 99" means the string is word for word a card or a label named in that line's `vis` note in `scripts/longform-born-as-polar-bear.outline.json`, which research 99 checked line by line. Nothing was edited: the fixes below are for the main session.

## Verdict

Three fixes and one cut. No number on screen is wrong, and no bar, dial, chart or count is drawn at a value different from its label. The fixes are: the safety checklist board and the description drop "at all times" from Manitoba's "back away" line; the status-report board's commas tie "for food" to cub killing that the report gives another reason for; and the description sends viewers to a repo file they cannot open.

## Sources opened today (2026-11-13, 09:40 to 10:10 UTC)

- With curl, raw: USGS publication pages 70193125 (Wilder 2017), 70036174 (Durner 2011), 70029716 (Smith 2007), 70136255 (Pagano 2012), 1012949 (Amstrup and Durner 1995), 70028385 (Amstrup 2006); the Manitoba Polar Bear Alert brochure PDF (pdfinfo: created and modified 2010-12-24); PMC12855275 (Aars 2026, full text page, journal meta "Scientific Reports"); PMC6018667 (Lone 2018, full text).
- COSEWIC 2008 chapter 5: curl got an empty reply from the server again (as in research 99). Read through the fetch tool instead, which quoted: "The killing of cubs to bring females into estrus, or killing of cubs and adults for food, is not uncommon" and "Polar bears have no natural predators."

## The table

| Where | Text as shown | Verdict | Replacement for a FIX | Source opened |
|---|---|---|---|---|
| all lines | meter RAW DEAL / SWEET DEAL; chapter chip "1 OF 8" ... "8 OF 8", WHAT YOU GOT, THE VERDICT | ok (format labels, opinion meter) | | none needed |
| s0.l1 | DEC, JAN | covered by 99 (vis) | | |
| s0.l2 | 0.6 KG | covered by 99 (card ABOUT 0.6 KG AT BIRTH) | | |
| s0.l3 | 8 chips | covered by 99 (card 8 THINGS) | | |
| s0.l4 | 8 bowl boxes under FAST CAN TOP 8 MONTHS | ok: 8 boxes under "can top 8" does not cap it | | https://pubs.usgs.gov/publication/70251899 (via 99) |
| s0.l5 | flying pages numbered 1 to 9 | ok (nine days, Durner 2011) | | https://pubs.usgs.gov/publication/70036174 |
| s0.l6 | YOUR SCORE? | covered by 99 (vis) | | |
| s1.l1 | 1.5 M; 90 TO 100 CM | covered by 99 (vis) | | |
| s1.l2, s1.l6, s2.l2, s3.l4, s4.l3, s5.l3, s6.l5, s7.l3, s8.l2, s10.l9 | review cards: MEATBALL'S REVIEW; NO LEGROOM. NO ROOM SERVICE.; TOO MUCH CARDIO.; THE MENU IS SEAL. COULD NOT CATCH ONE.; TOO MUCH WATER.; RUDE GUESTS.; KITCHEN CLOSED FOR MONTHS.; THE BEARS GOT THE AIR CONDITIONING.; 1 STAR. - THE KNEES; WOULD NOT BE BORN AGAIN. | covered by 99 (each is in the outline's say or vis; jokes on Meatball, no new number or danger) | | |
| s1.l3, s3.l2, s4.l3, s6.l5, s7.l3 | scene signs TOURS, TOUR DESK, MENU, SEAL, MOTEL, SHALLOW END, BREAKFAST, MOTEL ROOM (fan bubble) | ok (props, no claim) | | none needed |
| s1.l4 | OUTSIDE, THE DEN, 0 C | covered by 99 (vis) | | |
| s1.l5 | two bears on scales, the second's needle drops from 0.75 to 0.43, arrow, no labels | ok: 0.75 to 0.43 is a 43% drop; no "always" implied, card keeps "MAY" | | COSEWIC 2008 ch. 5 (fetch tool) |
| s1.l7 | stamp ONLY PREGNANT FEMALES | ok: shown with the card ONLY PREGNANT FEMALES DEN ALL WINTER (card at 60%, stamp at 65% of the line) | | https://www.fws.gov/species/polar-bear-ursus-maritimus (via 99) |
| s2.l1 | SHARE OF TIME OUTSIDE THE DEN SPENT INACTIVE; ADULTS 49.5%; CUBS 13.4%; 8 ADULTS, 14 CUBS, ALASKA, MARCH 2002 AND 2003 | covered by 99 (vis), and re-read: "8 adults and 14 dependent cubs outside dens for 37.5 h", "March 2002 and 2003", "inactive 49.5% ... 13.4%". Bars drawn at 49.5 and 13.4 of 100 | | https://pubs.usgs.gov/publication/70029716 |
| s2.l3 | map dot ALASKAN BEAUFORT SEA | covered by 99 (vis) | | |
| s2.l4 | dial ABOUT 65%; ALASKAN BEAUFORT SEA, 12-YEAR STUDY | covered by 99 (vis, card); "12-year study in the Alaskan Beaufort Sea" re-read | | https://pubs.usgs.gov/publication/1012949 |
| s2.l5 | dial ABOUT 86%; OTHER POPULATIONS AND YEARS DIFFER | covered by 99 (vis, card) | | |
| s2.l6 | 57 TRACKED FEMALES; one cub drawn | covered by 99 (vis). Picture: one cub is not contradicted (the paper is about females with cubs of the year, no litter size). Re-read: "57 adult female polar bears that were captured in Svalbard" | | https://pmc.ncbi.nlm.nih.gov/articles/PMC6018667/ |
| s2.l7 | timebar BIRTH / 2 YEARS; SOMETIMES LONGER | covered by 99 (vis: two-year bar, SOMETIMES LONGER) | | |
| s3.l1 | MENU / SEAL / ALMOST ALWAYS | covered by 99 (vis) | | |
| s3.l5 | sticky 20 MILES?; stamp NO SOURCE FOUND | covered by 99 (card 20 MILES? NO SOURCE FOUND) | | |
| s3.l6 | 90 CM OR MORE; UP TO 1 KM | covered by 99 (vis) | | |
| s3.l7 | 20 MILES? crossed; HOLE / SEAL; 1 KM = ABOUT 0.6 MILE | covered by 99 | | |
| s4.l2 | 4 day boxes, 3 with a swim mark; 57 TRACKED FEMALES, SVALBARD | covered by 99 (its own fix) | | |
| s4.l4 | map dots SOUTHERN BEAUFORT SEA, CHUKCHI SEA; 52 icons, 20 lit | covered by 99 (vis, card); re-read "52 adult female polar bears", "southern Beaufort and Chukchi seas", "50 long-distance swims by 20 bears" | | https://pubs.usgs.gov/publication/70136255 |
| s4.l5 | JOURNAL 2011; bear scales up in place | covered by 99 (vis: journal cover dated 2011). The year labels the paper, not the swim (the say gives 2008). The scale-up is the vis "icon zooms up" done in place: no fact shown | | https://pubs.usgs.gov/publication/70036174 |
| s4.l8 | SCHEMATIC, NOT THE REAL TRACK | ok (says what the line is) | | none needed |
| s4.l9 | LATE AUGUST 2008; LATE OCTOBER 2008; BETWEEN TWO CAPTURES; second bear thinner, cub as a ghost | covered by 99 (vis); re-read "Between an initial capture in late August and a recapture in late October 2008 ... lost 22% of her body mass and her yearling cub" | | https://pubs.usgs.gov/publication/70036174 |
| s4.l12 | 4 of 8 chips; fan of cards 1 STAR; YOUR REVIEW SO FAR? | covered by 99 (vis) | | |
| s5.l4 | map dot BEAUFORT SEA; JANUARY TO APRIL 2004; CASE 1 to CASE 3 | covered by 99 (vis); re-read "Between 24 January and 10 April 2004 ... three instances" | | https://pubs.usgs.gov/publication/70028385 |
| s5.l6 | notebook 24 YEARS; EARLY 2004: 3 CASES | ok: "During 24 years of research ... in the southern Beaufort Sea region of northern Alaska ... we have not seen other incidents" and the three 2004 cases | | https://pubs.usgs.gov/publication/70028385 |
| s5.l7 | STATUS REPORT (CANADA, 2008) / IN THE BEAR FAMILY, / POLAR BEARS INCLUDED, / KILLING CUBS, OR CUBS / AND ADULTS, FOR FOOD, / IS NOT UNCOMMON | FIX: with the comma after ADULTS, "for food" reads as the reason for killing cubs too. The report gives a different reason for killing cubs: "to bring females into estrus" | rows: "IN THE BEAR FAMILY," / "POLAR BEARS INCLUDED," / "KILLING CUBS TO BRING" / "FEMALES INTO ESTRUS, OR" / "CUBS AND ADULTS FOR FOOD," / "IS NOT UNCOMMON" (6 rows; if it will not fit, the smallest change is "AND ADULTS, FOR FOOD," to "AND ADULTS FOR FOOD," so the board at least matches the checked say) | COSEWIC 2008 ch. 5 (fetch tool; curl got an empty reply) |
| s5.l8 | NO NATURAL PREDATORS*; *JUST RELATIVES | covered by 99 (vis, say) | | |
| s6.l1 | map dot HUDSON BAY, ice melts, bears appear on the shore | covered by 99 (card) | | |
| s6.l2 | HUDSON BAY AND EASTERN BAFFIN ISLAND; strip 4 months shaded; clock 82% shaded, INACTIVE | covered by 99 (vis); 0.82 is "over 80%" | | https://www.hww.ca/?p=7931 (via 99) |
| s6.l3 | 142 BEARS / 2009 TO 2014 / WATER, NO FOOD / MEDIAN 17 DAYS / HELD NEAR CHURCHILL | covered by 99 (vis) | | |
| s6.l4 | scale needle steps down; 4 day boxes | ok (no number drawn beyond the card) | | |
| s6.l6 | TRYING | covered by 99 (say/vis) | | |
| s7.l1 | sign CHURCHILL; puff "BANG!" | covered by 99 (vis: "a puff and a bang") | | |
| s7.l2 | BROCHURE PDF DATED 2010; sign HOLDING FACILITY | covered by 99 (vis); pdfinfo re-read: created 2010-12-24. "Holding facility" is the brochure's word | | https://gov.mb.ca/fish-wildlife/pubs/fish_wildlife/polarbearalertbrochure%20(1).pdf |
| s7.l4 | IF YOU MEET A POLAR BEAR (MANITOBA) | ok: trigger and agency named | | Manitoba brochure PDF |
| s7.l4 | STAY CALM | ok | | Manitoba brochure PDF |
| s7.l4 | STAY WITH YOUR GROUP | ok | | Manitoba brochure PDF |
| s7.l4 | BACK AWAY, FACING THE BEAR | FIX: the brochure says "Back away, facing the polar bear at all times." The spoken line keeps "at all times"; the board drops it, and a safety instruction must not lose its condition | BACK AWAY, FACING THE BEAR AT ALL TIMES | Manitoba brochure PDF |
| s7.l4 | DO NOT TURN AND RUN | ok ("Do not turn and run away.") | | Manitoba brochure PDF |
| s7.l4 | DO NOT PLAY DEAD | ok | | Manitoba brochure PDF |
| s7.l4 | GET INTO A VEHICLE OR A BUILDING | ok ("Get into your vehicle or a building as rapidly as possible"; the say keeps "as fast as you can") | | Manitoba brochure PDF |
| s7.l6 | five country names on the map; timebar 1870 / 2014 | covered by 99 (vis); re-read "5 polar bear Range States (Canada, Greenland, Norway, Russia, and United States)" | | https://pubs.usgs.gov/publication/70193125 |
| s7.l7 | 73 ATTACKS, 20 DEATHS, 63 INJURIES; RECORDED ATTACKS, FIVE COUNTRIES | ok: "documented 73 attacks ... 20 human fatalities and 63 human injuries" (deaths and injuries are people, so they add to more than 73; the small print says ATTACKS only for the 73) | | https://pubs.usgs.gov/publication/70193125 |
| s8.l1 | candles numbered 5, 10, 15 ... and a red 25 | covered by 99 (vis: candles stop at 25) | | |
| s8.l3 | dial ABOUT 97%; ADULT FEMALES; ALASKAN BEAUFORT SEA, 12-YEAR STUDY | ok: S = 0.969 for adult females, 12-year study | | https://pubs.usgs.gov/publication/1012949 |
| s8.l4 | DOCUMENTED ADULT FEMALE DEATHS; 7 rows, 6 marked; LOCAL HUNTERS, THAT STUDY ONLY | covered by 99 (vis); 6 of 7 is 86%, close to 85% and not labelled as a count | | |
| s8.l5 | AGES 2 TO 4 AND ADULTS: 77 TO 92% A YEAR; OLD-AGE CLASS: 37 TO 62% A YEAR; axis 0%, 50%, 100%; NORTHERN BEAUFORT SEA, 1971 TO 2006, HUNTING DEATHS INCLUDED | covered by 99 (vis). Bands are drawn at about 77-92 and 37-62 on the axis | | |
| s9.l1 | tag on the newborn | ok (no text on the tag) | | none needed |
| s9.l3 | GUARD HAIRS, UNDERFUR, SKIN, FAT | covered by 99 (vis) | | |
| s9.l7 | map fills with bear dots | covered by 99 (card ESTIMATED 26,000 WORLDWIDE (2023)); the dots are not a count | | |
| s10.l0 | ledger RAW / SWEET; "?" on the map | ok (opinion props) | | none needed |
| s10.l1 | map dot SOUTHERN BEAUFORT SEA; bar DOWN 25 TO 50%; BEAR NUMBERS | covered by 99 (card); drop is drawn downward, right direction | | |
| s10.l2, s10.l3 | BODY CONDITION (NO SCALE); axis 1995, 2000, 2019; line falls to 2000 then rises; 770 ADULTS, 1995 TO 2019 | covered by 99 (vis); re-read "770 adult bears, 1188 captures, in March-May 1995-2019, in Svalbard" and "BCI declined until 2000 ... increased afterwards". Direction right | | https://pmc.ncbi.nlm.nih.gov/articles/PMC12855275/ |
| s10.l4 | SEPTEMBER MINIMUMS, SATELLITE RECORD; 47 boxes, last 19 red; LOWEST 19 | covered by 99 (vis) | | |
| s10.l5 | map dots SOUTHERN BEAUFORT SEA, SVALBARD; DEPENDS WHERE | covered by 99 (say/vis) | | |
| s10.l8 | stamp RAW START. SWEET IF YOU GET THROUGH.; DEPENDS ON YOUR ICE; meter dips to 40, settles at 56 | covered by 99 (vis: "wobbles, then settles a little on the sweet side"); 56 is a little past the middle (50). Opinion, said as one | | |
| s10.l10 | empty comment box; YOUR REVIEW? | ok | | none needed |
| map (all boards) | schematic ring of land; country names; sea dots | ok: each dot sits on the right side of the ring (Alaska seas together, Hudson Bay on the Canada side, Svalbard by Norway). Schematic, no distances claimed | | none needed |
| description.txt | opening paragraph ("The life of a polar bear, from the inside ... left a review.") | ok (no number; "8 things" is the video's own count) | | |
| description.txt | searched-phrase paragraph | ok. Each phrase is answered in the video: life cycle (den to old age), mother and cubs in the den (s0 to s1), how far can a polar bear swim (52 females, 20 made swims over 50 km, one recorded 687 km swim; this answers with study records, not a maximum, and the paragraph promises no maximum), sense of smell (s3), attacks on people (s7), what to do if you see a polar bear (Manitoba's advice for meeting one), how many are left (26,000, 2023 estimate). Not a fact issue: it is a bare keyword list, which YouTube's spam rules dislike in bulk; nine phrases is short, left to the post-metadata skill | | |
| description.txt | chapter list 0:00 to 9:05 | could not verify independently (BUILD_NOTES says the times were taken from the render; video is 630.1 s by ffprobe, so 9:05 fits) | | |
| description.txt | Cubs ... December or January at about 0.6 kg ... eyes closed ... 10 to 12 kg | covered by 99 | | |
| description.txt | A mother's fast can exceed 8 months (USGS, 2024) ... 43% | covered by 99 (its own fix) | | |
| description.txt | 12-year study ... (published 1995) ... first year about 65% ... adult female about 97% | ok: 0.651 and 0.969, "12-year study in the Alaskan Beaufort Sea" | | https://pubs.usgs.gov/publication/1012949 |
| description.txt | One collared female swam 687 km in 9 days in 2008 (Durner and others 2011) | ok | | https://pubs.usgs.gov/publication/70036174 |
| description.txt | breathing hole up to a kilometre; no source for '20 miles' | covered by 99 | | |
| description.txt | 1870 to 2014, 73 recorded attacks, 20 deaths (Wilder and others 2017) | ok | | https://pubs.usgs.gov/publication/70193125 |
| description.txt | "Manitoba's advice if you meet a polar bear: stay calm, stay with your group, back away facing the bear, do not run, do not play dead, get into a vehicle or a building." | FIX: same as the board, "at all times" is dropped, and "do not run" loses "turn and" | "Manitoba's advice if you meet a polar bear: stay calm, stay with your group, back away facing the bear at all times, do not turn and run, do not play dead, get into a vehicle or a building as fast as you can." | Manitoba brochure PDF |
| description.txt | 26,000 as of 2023; southern Beaufort 25 to 50% after low survival 2004 to 2006; Svalbard rose after 2000 | covered by 99 (its own fixes) | | |
| description.txt | verdict is our opinion | ok | | |
| description.txt | Sources line, "Aars and others 2026 (Svalbard body condition, Scientific Reports)" | ok (journal meta on the PMC page: Scientific Reports) | | https://pmc.ncbi.nlm.nih.gov/articles/PMC12855275/ |
| description.txt | "Full list with links: research/98-polar-bear-life-factpack.md." | CUT: a viewer cannot open a file in our repo; it reads as a broken promise | delete the sentence (or replace it with the main source links, if the main session wants links) | none needed |
| description.txt | safety line "General information, not a safety guide. In polar bear country, follow the instructions of the local wildlife agency." | ok | | |
| description.txt | #polarbear #polarbearfacts #arctic #meatballmyths | ok (no #shorts on a long video; no banned title word, no "sucks") | | |
| tags.txt | polar bear; life of a polar bear; polar bear life cycle; polar bear facts; polar bear cub; polar bear mother and cubs; the life of a baby polar bear; how far can a polar bear swim; polar bear sense of smell; polar bear attacks; how many polar bears are left | ok: 11 tags, each 30 characters or fewer, each answered by the video, none promises advice | | |
| pinned_comment.txt | Meatball's review: 1 star. "No legroom. The menu is seal. Kitchen closed for months. Would not be born again." ... how many stars ... which of the 8 gets you first? | covered by 99 (pinned comment checked); the four quotes are on screen in the video | | |
| thumbnail pb_a | RAW START (bear with a tear) | ok: first half of the stated verdict, opinion; does not promise only misery | | |
| thumbnail pb_b | 687 KM ONE SWIM | ok: "a continuous swim of 687 km over 9 days" | | https://pubs.usgs.gov/publication/70036174 |
| thumbnail pb_c | BORN A POLAR BEAR? | ok (question) | | |

Counts (table rows; a row can hold several strings of one board, such as the ten review cards or the eleven tags): 85 rows, 46 covered by 99, 34 ok, 3 FIX, 1 CUT, 1 could not verify.

## Must change before scheduling

1. `tools/drawn_pb_shots.py`, s7.l4, search `"BACK AWAY, FACING THE BEAR"`. New: `"BACK AWAY, FACING THE BEAR AT ALL TIMES"`. Look at the sheet after: the row is 37 characters against the longest now (32); px 44 on a 980 wide sheet.
2. `tools/drawn_pb_shots.py`, s5.l7, search `"KILLING CUBS, OR CUBS",` and `"AND ADULTS, FOR FOOD,"`. New rows: `"IN THE BEAR FAMILY,", "POLAR BEARS INCLUDED,", "KILLING CUBS TO BRING", "FEMALES INTO ESTRUS, OR", "CUBS AND ADULTS FOR FOOD,", "IS NOT UNCOMMON"`. Smallest fallback if six rows will not fit: `"AND ADULTS, FOR FOOD,"` to `"AND ADULTS FOR FOOD,"`.
3. `episodes/longform-born-as-polar-bear/description.txt`, search `back away facing the bear, do not run, do not play dead, get into a vehicle or a building.` New: `back away facing the bear at all times, do not turn and run, do not play dead, get into a vehicle or a building as fast as you can.`
4. `episodes/longform-born-as-polar-bear/description.txt`, search ` Full list with links: research/98-polar-bear-life-factpack.md.` Delete it.

After 1 and 2: re-render s5.l7 and s7.l4 and look at their sheets.

## Notes for the main session (not fixes)

- The spoken s5.l7 ("killing cubs, or cubs and adults for food") was cleared by research 99 and is not re-checked here. It is the same ambiguity as the board in a softer form; if the main session wants it fully true, "killing cubs to bring females into estrus, or killing cubs and adults for food" is the report's wording.
- `postkit.py lint scripts/longform-born-as-polar-bear.json` gives 2 fail ("no title", "no description") and 2 warn (no emoji, no tags list). This file changed nothing, so these are the spec's own: the title, description and tags live in `episodes/longform-born-as-polar-bear/` and must be put into the spec (or the payload) before scheduling.

## Could not verify

- COSEWIC 2008 chapter 5 as raw text: the server sent an empty reply to curl. Its two sentences were read through the fetch tool's summary only.
- The description's chapter times: not re-measured against the render (BUILD_NOTES says they came from it).
- Hinterland Who's Who and the USGS 2024 paper were not re-opened: every string resting on them was covered by research 99.
