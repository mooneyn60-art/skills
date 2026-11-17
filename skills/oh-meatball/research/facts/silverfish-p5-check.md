# Fact-check: tt-house-centipede-p5.json (silverfish, Part 5)

Checked 2026-11-17 against the live pages (opened by the checker, not taken from the pack): MDC silverfish-firebrat, UC IPM silverfish-and-firebrats, Penn State bristletails-silverfish-and-firebrats, UMD silverfish-and-firebrats, NC State order-zygentoma. Pack: side-hustles channels/qa/silverfish-p5-1118.md.

Verdict: 4 FIXES + 2 small ones. The rest passes. Nothing in the spec says "never bite", a flat "live 8 years", or reuses the old dinosaurs/books hook.

## Say lines

1. HOOK "Don't squish that silverfish! Squish it, or let it live? Vote at the end." PASS. No claim.
2. "Will it bite you?" PASS. A question. Note: no page says anything about biting people (UC IPM's only "bite" is paper). The next line answers with paper only, which matches the source. Do not add an answer about people.
3. "It has very weak jaws, so it scrapes the surface of paper instead of biting it. And they do not transmit disease." PASS. UC IPM: "very weak mandibles, or jaws, which causes them to scrape, instead of bite" (paper). MDC: "They do not transmit disease, however."
4. "Its fossils date to 400 million years ago. That's about twice as long ago as the dinosaurs. Meatball's lunch is not that old. Probably." PASS. MDC has the sentence word for word. UMD: "fossils dating back over 400 million years" (agrees). Joke adds no number or claim; hedge kept.
5. "They move rapidly, including sideways, and their flat bodies let them hide in narrow crevices. Meatball can't even walk sideways." PASS. Penn State has it word for word (MDC does not mention sideways). Joke is on Meatball.
6. "Males attract females with a mating dance, antennae contact and head wagging, then leave a sperm capsule for her to pick up. Meatball's last date just got a breadstick." PASS. UC IPM: males do the dance, then deposit "a protected capsule containing sperm for the female to pick up". Joke adds nothing.
7. "The babies look like the adults, only whitish and much smaller, and they have no scales at first." PASS. MDC and UC IPM ("small nymphs ... lack scales").
8. "It can pass through 45 to 60 stages, or instars, in its life. Meatball has had three: baby, kid, and snack." **FIX (joke adds a number).** The fact is fine (UC IPM: "passing through 45 to 60 instars or development stages"; "can" kept). "three" is a new number in a joke.
   - Old: `Meatball has had three: baby, kid, and snack.`
   - New: `Meatball's list goes baby, kid, snack.`
9. "Silverfish live about 3 years. In some species, individuals can live for 8 years. That's longer than Meatball's houseplant." PASS for the spoken line. UC IPM: "silverfish about 3 years." MDC (Life Cycle section, about silverfish as a group): "In some species, individuals can live for 8 years". Hedge "some species" and "can" kept. Joke adds no number. Note: UMD says "maximum lifespan in good conditions is 2 to 3 years" and Penn State says "at least two to three years", so the 8 must stay hedged exactly as it is. The card is the problem (see cards).
10. "They can invade new homes from wild areas nearby, especially as those areas dry out in summer. They can also come in on lumber and wallboard." PASS. UC IPM: "Large numbers of these insects can invade new homes from surrounding wild areas, especially as these areas dry out during the summer. They also can come in on lumber, wallboard, and similar products."
11. "And the house centipede you just met eats these. So, squish it, or let it live?" PASS. MDC: "Silverfish are eaten by house centipedes, earwigs, and spiders." The line says it of house centipedes in general, which the source carries. Do not extend it to "always" or "mostly".
12. "Full episode on YouTube, Meatball Myths." **FIX (soft, could not verify).** posted.csv shows only a silverfish Short on YouTube (10/27, "A Bug Older Than Dinosaurs...") and a hook-test Short queued 11/21. No silverfish "full episode" is logged. If no long episode exists, the line promises something that is not there.
   - Old: `Full episode on YouTube, Meatball Myths.`
   - New: `More on YouTube, Meatball Myths.`
   - Same swap in the card (`FULL EPISODE ON YOUTUBE` -> `MORE ON YOUTUBE`) and in tiktok_caption (`Full episode on YouTube, Meatball Myths.` -> `More on YouTube, Meatball Myths.`). If the earlier parts all say "Full episode" and a long edition does exist, keep it.

## On-screen cards

- id_card rows `FOSSILS: ABOUT 400 MILLION YEARS AGO`, `JAWS: VERY WEAK, SCRAPES PAPER`, `DOES NOT TRANSMIT DISEASE`: PASS (MDC, UC IPM, UMD).
- `SQUISH IT OR LET IT LIVE?`, `WILL IT BITE?`, `VERY WEAK JAWS` / `IT SCRAPES PAPER`, `FAST. EVEN SIDEWAYS.` / `FLAT ENOUGH FOR CRACKS`, `A MATING DANCE` / `ANTENNAE + HEAD WAGGING`, `BABIES: NO SCALES` / `WHITISH AND MUCH SMALLER`, `ABOUT 3 YEARS`, `SQUISH OR LET IT LIVE?`, `MEATBALL MYTHS`: PASS.
- `45 TO 60 STAGES` / `IN ONE LIFE`: **FIX (hedge dropped).** The line says "can". Another source (UF/IFAS, in the pack) records 25 to 66 molts, so the card should not read as a flat count.
  - Old row 2: `IN ONE LIFE`
  - New row 2: `CAN HAPPEN IN ONE LIFE`
- `ABOUT 3 YEARS` / `SOME SPECIES: UP TO 8`: **FIX ("UP TO 8" reads as the maximum; UMD says the maximum is 2 to 3 years, and the pack says never "maximum 8").**
  - Old row 2: `SOME SPECIES: UP TO 8`
  - New row 2: `SOME SPECIES: CAN LIVE 8 YEARS`
- `THEY MOVE IN` / `ON LUMBER + WALLBOARD`: **FIX (hedge dropped; the source says "can").**
  - Old row 1: `THEY MOVE IN`
  - New row 1: `THEY CAN MOVE IN`

## tiktok_title

`Silverfish: 400 Million Years, Weak Jaws and a Mating Dance` **FIX (low priority; the title field is not shown).** "400 Million Years" reads as the animal's age; the source says fossils date to 400 million years ago.
- New: `Silverfish: Fossils From 400 Million Years Ago, Weak Jaws and a Mating Dance`

## tiktok_caption

- "Will it bite you? It has very weak jaws, so it scrapes the surface of paper instead of biting it, and silverfish do not transmit disease." PASS (same as lines 2 and 3).
- "Its fossils date to 400 million years ago, about twice as long ago as the dinosaurs." PASS.
- "It moves fast, even sideways, does a mating dance with antennae and head wagging" **FIX.** UC IPM says the males do the dance. As written, every silverfish "does" it.
  - Old: `It moves fast, even sideways, does a mating dance with antennae and head wagging, and can pass through 45 to 60 stages in its life.`
  - New: `It moves fast, even sideways. Males do a mating dance with antennae and head wagging, and a silverfish can pass through 45 to 60 stages in its life.`
- "The house centipede you just met eats these." PASS (MDC).
- "Full episode on YouTube" see line 12.
- Sources line (MDC, UC IPM, Penn State, UMD, NC State): PASS as a list. Fossils: MDC and UMD. Disease: MDC. Jaws, dance, instars, invade: UC IPM. Sideways: Penn State. NC State is not behind any claim in the caption now (its life-span and courtship lines are not used); drop it or leave it, your call.
- Hashtags and the closing question: PASS. No #fyp.

## Jokes (all four "Meatball" lines)
Lunch not that old; can't walk sideways; last date got a breadstick; three stages baby/kid/snack; houseplant. Only the "three" line adds a fact (a number), fixed above. None aims at the viewer. No swears, no safety instruction.

## Could not measure
- Whether a long silverfish episode exists on YouTube (only logged posts checked).
- MDC's 8-year line has no stated source or species; it is the only page with that figure for silverfish. It stays hedged.
- UC IPM says males "attract females" and the capsule is picked up by the female; I did not open a second page that confirms "dance" (NC State describes a silk-thread courtship instead, so "dance" rests on UC IPM alone).
- UF/IFAS PDF not re-opened; its 25 to 66 figure is from the pack.
