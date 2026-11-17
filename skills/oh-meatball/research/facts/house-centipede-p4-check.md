# Second-model check: House centipede Part 4 (TikTok, 11/17)

Spec: `scripts/drawn-house/tt-house-centipede-p4.json`. Checked 2026-11-17 by a different model than the writer. Every source URL was fetched live that day. The four web pages were read as text. The Acosta PDF is a scan: I read its text layer and then looked at the page 3 image itself.

Result: CLEARED after 8 wording changes. Lint: pass (0 fail, 0 warn).

## The sources, opened live
- Acosta (2003), J. Ky. Acad. Sci. 64(1), NKU PDF (200 OK, 6 scanned pages). Quotes below are from the page images.
- University of Arkansas Arthropod Museum, house centipede (200 OK).
- University of Kentucky Entomology ef645 (200 OK).
- Mississippi State Extension, Bug's Eye View No. 29 (200 OK).

## Line by line

| # | Where | Verdict | Source quote | Note |
|---|---|---|---|---|
| 1 | Hook "made the Guinness Book of World Records" | FIX | Acosta p.4: "...impressive enough to be listed as among the fastest arthropods in the 1973 Guinness Book of World Records." | "Made the Guinness Book" reads as a record. The source says a listing, "among the fastest arthropods", in the 1973 edition. Not the fallback: the fallback line would repeat line 3's "one mile an hour". |
| 2 | Hook card "GUINNESS BOOK, 1973 / AMONG THE FASTEST ARTHROPODS" | PASS | same | Matches the source. |
| 3 | "Meatball has a trophy too. He bought it online." + card | PASS | none needed | Joke on Meatball. No number, danger, feeling or advice. |
| 4 | "Clocked at about sixteen inches a second. Close to one mile an hour." | PASS | Acosta: "clocked at 420 mm./sec with a 33 mm stride". MSU: "reaching speeds approaching one MPH." | 420 mm/s = 16.54 in/s = 0.94 mph (16.54 x 3600 / 63,360). Both pages agree. "About sixteen" is a touch under 16.5, and "about" covers it. "Close to" matches "approaching". |
| 5 | Card "16 INCHES A SECOND / CLOSE TO 1 MPH" | FIX | same | The card dropped the "about" that the voice says, so it read as an exact figure. |
| 6 | "Meatball's top speed is the walk to the fridge." + card | PASS | none needed | Joke on Meatball. |
| 7 | "It darts, stops dead, and can freeze for a while." | FIX | Arkansas: "often seen darting across floors at high speed, occasionally stopping suddenly and remaining motionless for some time before racing off once more." | "Occasionally" was dropped for the stops. Hedge restored. "Can freeze for a while" matches "for some time". |
| 8 | "Meatball froze too. Longer." | FIX | Arkansas gives no length ("for some time"). | "Longer" compares against a freeze time nobody measured. Joke now stands on Meatball alone. |
| 9 | Card "RUN. STOP. FREEZE. / THEN IT'S GONE" | PASS | Arkansas: "racing off once more". | Fine. |
| 10 | "It catches its food by half pouncing, half lassoing." + card | PASS | Arkansas: "They capture prey by half pouncing and half lassoing them." | Word for word, "food" for "prey". |
| 11 | "Meatball tried a lasso once. He caught his own damn foot." + card | PASS | none needed | Joke on Meatball. "Damn" is mild and sits well after 7 s. |
| 12 | "It can run up your walls to hunt." | PASS | UKY ef645: "To aid in hunting, house centipedes can run very quickly across floors and up walls." | Fine. |
| 13 | "Meatball checked his ceiling. Hell no." | FIX | UKY says walls. Arkansas, UKY, MSU and Acosta say nothing about ceilings (the pack also notes this). | A viewer hears "ceiling" as a climbing claim. Now "walls". "Hell no" is Meatball's reaction, mild, after 7 s. |
| 14 | "Unlike most centipedes, it has big faceted eyes." + card "BIG FACETED EYES" | FIX | Arkansas: "Unlike most other centipedes, house centipedes and their close relatives have well-developed, faceted eyes." Acosta p.3: "well-developed compound eyes", and elsewhere in the review "large heads, prominent compound eyes". | "Big" is in no source. "Well-developed" is the source's word. The card "RARE FOR A CENTIPEDE" stays: "unlike most" means a minority. |
| 15 | "Meatball's eyes need coffee." | PASS | none needed | Joke on Meatball. |
| 16 | "But the weirdest part? How it cleans itself." | PASS | none needed | Framing, no claim. |
| 17 | "On a strict schedule, it pulls each leg through its mouthparts. Like floss." + card | PASS | Acosta p.3: "House centipedes meticulously groom themselves on a strict schedule (Le Moli and Parmigiani 1976). The antennae and legs are gripped by the forcipules and passed through the cleaning setae on the first maxillae (Verhoeff 1938b)." | Fair. The first maxillae are mouthparts, so "mouthparts" is right. Acosta: grooming runs "legs 1 through 15 of the same side", so "each leg" holds. "Like floss" is a simile. These are old studies (1938, 1976) read through a 2003 review, and the review states them as fact, so the script does too. |
| 18 | "It even tries to clean legs it doesn't have anymore. Damn. Meatball skips the legs he has." + card | PASS | Acosta p.4: "Grooming behavior appears to be genetically hard-wired because house centipedes will still attempt to clean legs that have been amputated." | "Tries" keeps the hedge. "Damn" is a reaction, after 7 s. The Meatball joke adds nothing about the animal. |
| 19 | "It breathes through holes down the middle of its back. Meatball breathes through his mouth. Loudly." + card | PASS | Acosta p.3: "The seven tergites each bear a median dorsal spiracle for gas exchange, unlike the lateral paired spiracles of other myriapods." | Tergites = back plates, dorsal = on the back, median = down the middle, spiracle = breathing opening. "Holes" is the plain word. |
| 20 | "Moms lay eggs one at a time, in soil." + card "EGGS IN SOIL / ONE AT A TIME" | PASS | Acosta p.3, read on the page image: "Females lay relatively few eggs (average four eggs per day; Lewis 1981), singly in soil. Laying and hatching occurs from late spring through early summer." | The verb is NOT missing. The page image reads "lay" clearly. The pack's "[lay]" bracket was wrong, and the text layer only garbles it. Claim supported. The fallback is not needed. "Moms" is casual for "females". |
| 21 | "His dog, Noodle, heard soil and started digging." | PASS | none needed | Noodle is the channel's own drawn dog, a gag. It says nothing about the centipede. |
| 22 | "A male that just molted is especially likely to get eaten by a female." | FIX | Acosta p.4: "Newly molted male house centipedes are especially susceptible to predation by females." | "Susceptible" means open to it. "Especially likely" is a probability claim the source does not make. |
| 23 | Card "JUST MOLTED? / FEMALES MAY EAT HIM" | PASS | same | "May" keeps the hedge. |
| 24 | "Meatball cancelled his date." | PASS | none needed | Joke on Meatball. It does not say the animals mate when this happens. |
| 25 | "So, does the speedy roommate stay, or get squished?" + card | PASS | none needed | Question for the viewer. No advice. |
| 26 | "Part 5 drops tomorrow. Follow so you don't miss it." + card | PASS, with a flag | Not a source claim. It is Social Studio's order (side-hustles TASKS.md, 11/17 7:00 AM, "End line... On-screen too"). | Not follow-for-follow. MASTER_ORDERS bans a spoken "Follow" outro on Shorts, but the Studio note wins where it says so. FLAG for the main session: the line is false unless a new Part 5 posts Wed 11/18 (status.md says it is built tonight for Wed 7 PM). An older file `tt-house-centipede-5.mp4` posted 11/15 with no "Part 5" in its title, so the naming clashes. |
| 27 | Title "House Centipede Part 4 🐛" | PASS | none needed | Clean. |
| 28 | `tiktok_title` "...Guinness Speed, Leg Floss and Back Holes" | PASS | none needed | Nobody sees this field. "Guinness Speed" is loose, left as is. |

## tiktok_caption, sentence by sentence
- "the 1973 Guinness Book of World Records listed it among the fastest arthropods": PASS. This already used the right word, "listed". The hook now matches it.
- "clocked at about 16 inches a second, close to one mile an hour": PASS (same sources as line 4).
- "can stop dead and freeze": PASS ("can" is the hedge).
- "half pouncing, half lassoing": PASS.
- "has big faceted eyes, which most centipedes do not": FIX. Now "has well-developed, faceted eyes, which most centipedes do not".
- "On a strict schedule it pulls each leg through its mouthparts, and it even tries to clean legs it no longer has": PASS.
- "It breathes through holes down the middle of its back": PASS.
- "Meatball tried a lasso once and caught his own foot": PASS (joke on Meatball).
- "Missed Part 2? ... the 30-legged bug that hunts the roaches in your house": PASS. 15 pairs = 30 legs; UKY lists cockroaches among its prey.
- Question and five hashtags: PASS. No #fyp, no brand tag, clean words.

## Mild words and the first 7 seconds
Three mild words in the whole script: "damn" (line 11), "hell" (line 13), "damn" (line 18). All are well after 7 s. None is in the title, the caption or on a card.

## Changes made (spec edited in place)

| Where | Old | New | Why |
|---|---|---|---|
| Hook `say` | You just saw a bug that made the Guinness Book of World Records. | You just saw a bug Guinness listed among the fastest arthropods. | The source says listed, not "made it" or a record. |
| Beat 3 card row 1 | 16 INCHES A SECOND (92 px) | ABOUT 16 INCHES A SECOND (84 px) | Keeps the "about". About 855 px wide at 84 px, inside the 1080 px frame. |
| Beat 5 `say` | It darts, stops dead, and can freeze for a while. Meatball froze too. Longer. | It darts, sometimes stops dead, and can freeze for a while. Meatball froze too. Still frozen. | Source says "occasionally"; "Longer" compared against an unmeasured freeze. |
| Beat 8 `say` | ...Meatball checked his ceiling. Hell no. | ...Meatball checked his walls. Hell no. | No source says ceilings. |
| Beat 9 `say` | Unlike most centipedes, it has big faceted eyes. | Unlike most centipedes, it has well-developed, faceted eyes. | "Big" is not in a source. |
| Beat 9 card row 1 | BIG FACETED EYES | FACETED EYES | Same. |
| Beat 15 `say` | ...is especially likely to get eaten by a female. | ...is especially vulnerable to being eaten by a female. | Source says "susceptible to predation", not "likely". |
| `tiktok_caption` | ...has big faceted eyes, which most centipedes do not. | ...has well-developed, faceted eyes, which most centipedes do not. | Same as beat 9. |
| `sources` P4-F7 | Females [lay] ... "(the verb is lost in the scan);" | Females lay ... (bracket and "lost in the scan" note removed) | The verb reads "lay" on the page image. |
| `_note` | NOT yet checked by a second model... (long planning note) | Checked by a second model 11/17 (research/facts/house-centipede-p4-check.md) | Ordered. |

Length: the spoken word count is the same as before, within one or two words (hook two words shorter, "sometimes" and "Still frozen" a word or so longer). The 64.29 s plan should hold within 61 to 65 s. Not rendered, so the real length is unmeasured: check it at render.

## Could not measure
- Real rendered length after the wording changes (not rendered, as ordered).
- Whether the 1973 Guinness listing is in later editions. Not needed: the script says "listed" and gives 1973.
- How fast it climbs walls, how long a freeze lasts, whether it climbs ceilings: no source says.
- The grooming studies (Le Moli and Parmigiani 1976, Verhoeff 1938b) and the egg figures (Lewis 1981) were not opened; I read them as Acosta reports them.
- Ohio State and Oklahoma State pages (403 per the pack): not retried.
- Whether Part 5 posts Wed 11/18 (line 26).

## Pack error to fix
`research/facts/house-centipede-p4.md` still says the egg verb is "[lay]" lost in the scan (F7) and that the Guinness line may say "made" it (could-not-measure list). I did not edit the pack (not in my brief). The first is wrong and the second is now overruled.
