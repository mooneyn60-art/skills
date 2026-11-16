# Second-model check: shark-wms TikTok minute cut (tt-shark-wms.json), 2026-11-16

Checker: check-shark-wms (a different model from the writer, script-shark-wms). Spec: scripts/drawn-house/tt-shark-wms.json. Packs: research/84 section 5 (SH-F1 to SH-F21), research/86. Pattern: research/92.

## Verdict
CLEARED after 9 wording fixes. Every spoken line, card, the search_top rows, tiktok_title and tiktok_caption is carried by an International Shark Attack File (ISAF) or Florida Museum page as worded. Every safety line now keeps its trigger and its spoken credit and is said clean, with the swear after it. Shark counts say "confirmed" and the year. No bear advice anywhere. No ending says a tactic saved Meatball ("Nothing's guaranteed" is kept). No insult is aimed at the viewer. No swear sits inside a credit. The first spoken sentence holds the searched words word for word ("What to do if a shark comes close?"). The dog is named with the comma ("his dog, Noodle"). Lint: pass (0 fail, 0 warn), run from skills/oh-meatball on 2026-11-16 after the fixes. Spoken words went from 251 to 265 (counted by script); the writer's plan was 83.36 s at 251 words, so about 88 s is expected, inside 65 to 92 s. Not re-planned or rendered.

## How the sources were opened
I fetched each page myself on 2026-11-16 (curl, browser user agent), stripped the tags and found every quote in the page text. Not taken from the pack.
- ISAF yearly worldwide summary 2025: https://www.floridamuseum.ufl.edu/shark-attacks/yearly-worldwide-summary/ ("ISAF confirmed 65 unprovoked shark bites on humans and 29 provoked bites", out of "105 alleged shark-human interactions").
- ISAF Quick Tips: https://www.floridamuseum.ufl.edu/shark-attacks/reduce-risk/quick-tips/ (under "Tips to help keep you and your family safe this summer": buddy, close to shore, not at dawn or dusk, schools of fish, jewelry, excess splashing; under "If a shark does get near you": "Maintain eye contact with the shark", "Slowly move away, and if possible, exit the water"; under "If the shark tries to bite you": "Hit shark in the eyes and gills").
- ISAF Advice to Swimmers: https://www.floridamuseum.ufl.edu/shark-attacks/reduce-risk/swimmers/ ("If a shark actually bites, we suggest clawing at its eyes and gill openings"; "You should not act passively if under attack").
- ISAF How to Avoid a Shark Attack: https://www.floridamuseum.ufl.edu/shark-attacks/reduce-risk/how-to-avoid-a-shark-attack/ (buddy "since sharks are more likely to approach a solitary individual"; hit-and-run near beaches "In pounding surf, strong currents, and murky water, a shark may mistake the movements of humans ... for ... fish"; sneak bites "take place in deeper waters ... can be serious injury or death"; bump-and-bites, "the shark circles and actually bumps the victim").
- ISAF Species Implicated: https://www.floridamuseum.ufl.edu/shark-attacks/factors/species-implicated/ ("almost any shark in the right size range, roughly six feet (1.8 meters) or greater, is a potential threat to humans").
- Florida Museum news release, February 18, 2026 (page last updated 02/18/2026): https://www.floridamuseum.ufl.edu/science/global-shark-bites-return-to-average-in-2025-with-smaller-proportion-in-the-united-states/ ("The chances of being bitten by a shark remain extremely low. Drowning and being struck by lightning are far more common.").

## Changes
| Where | Old | New | Why |
|---|---|---|---|
| title (YouTube field in the tt spec) | "65 Confirmed Bites in 2025" | "65 Confirmed Unprovoked Bites in 2025" | ISAF confirmed 65 unprovoked AND 29 provoked bites in 2025; "65 confirmed bites" undercounts. Title is exactly 100 characters. |
| Line 1 (spoken) | "Keep your eyes on it, back away slowly, and get out of the water if you can." | "The Shark Attack File says keep your eyes on it, back away slowly, and get out of the water if you can." | A safety instruction needs its credit spoken, clean. The trigger ("if a shark comes close" = ISAF "If a shark does get near you") is in the question. The first sentence still holds the searched words. |
| Line 7 (spoken) | "Skip the jewelry, and avoid excess splashing." | "More File tips: skip the jewelry, and avoid excess splashing." | Prevention tips with no credit; the last credit was three lines earlier. |
| Line 7 (card) | two rows | adds row "SHARK ATTACK FILE TIPS" | Same credit on the card. |
| Line 9 (spoken) | "Near beaches, the File says, a shark may mistake ..." | "In murky surf near beaches, the File says, a shark may mistake ..." | The page gives the condition: "In pounding surf, strong currents, and murky water". Without it the line reads as any swimmer, any time. |
| Line 10 (card, row 2) | "OR BUMP-AND-BITE, IN DEEPER WATER" | "IN DEEPER WATER, OR A BUMP-AND-BITE" | The page puts sneak bites in deeper water; it gives no depth for bump-and-bites. The old card tied "deeper water" to the bump-and-bite. |
| Line 11 (spoken) | "If it bites, hit the eyes and gills." | "If it bites, the File says, hit the eyes and gills." | Spoken credit for the safety instruction, said clean; "Fucking hell" stays after "Don't act passive." |
| Line 11 (card) | two rows | adds row "SHARK ATTACK FILE" | Credit on the card. |
| Line 12 (card, row 1) | "6 FEET OR LONGER" (size 92) | "ABOUT 6 FEET OR LONGER" (size 76, to fit) | The page says "roughly six feet"; the spoken line had "about", the card had lost the hedge. |
| _note | "NOT yet checked by a second model ..." | records this check | Bookkeeping only. |

## Lines checked and left as they are
- search_top "WHAT TO DO IF / A SHARK COMES CLOSE", tiktok_title: the searched phrase word for word. OK.
- Line 1 card: "EYES ON IT / BACK AWAY SLOWLY, LEAVE THE WATER IF YOU CAN / INTERNATIONAL SHARK ATTACK FILE": Quick Tips, "if possible" kept as "if you can", credited. "Scary as fuck" is a reaction after the clean instruction (cleared in research 92). OK.
- Line 2: gag kept from the checked short cut (research 92): alone and dusk break two ISAF tips. "Dumbass" follows a sentence about Meatball, not "you". OK.
- Line 3: 65 confirmed unprovoked, worldwide, 2025; card says the same with the ISAF credit. "That's fucking it" checked before (research 92, borderline OK). OK.
- Line 4: Quick Tips, credited, clean, "oh for fucking two" is on Meatball. OK.
- Line 5: How to Avoid page, "approach" (not the swimmers page's "attack"), credited, no number. OK.
- Line 6: Noodle gag, no fact, pet named with the comma. "Back on the boat" sits oddly with "swam alone" and the later "made it to shore", but it adds no claim. OK.
- Line 7 joke: crown and blender splashing are on Meatball; no new danger or reason is given for either tip. OK.
- Line 8: transition. OK.
- Line 9 joke: "swims like a fucking fish stick" is a simile on Meatball; it adds no number or risk. Card "HIT-AND-RUN BITES / A SHARK MAY MISTAKE A SWIMMER'S MOVES FOR FISH": "may" kept, fish not seals. OK.
- Line 10 spoken: "Worse" fairly sums up the page (hit-and-run "injuries usually are minor" against "can be serious injury or death"); card row 3 carries "CAN BE SERIOUS: SHARK ATTACK FILE". OK.
- Line 11: "If it bites" matches the Swimmers page ("If a shark actually bites"); "Don't act passive" is the File's own word. Snout advice not merged (pack trap). OK.
- Line 12 spoken: "about six feet or longer can be a threat" = "roughly six feet ... or greater, is a potential threat". Ruler joke on Meatball. OK.
- Line 13: release of 2026-02-18, credited to the Florida Museum, both sentences carried as worded; card "FLORIDA MUSEUM, 2026". OK.
- Line 14: "Meatball made it to fucking shore. Nothing's guaranteed." No tactic is said to have saved him (rule 7). Comment question loops into the hook. OK.
- tiktok_caption: phrase first; ISAF tips with "if possible" kept, the trigger carried by the phrase in front; 65 confirmed unprovoked, worldwide, 2025; release credited; gag without swearing, pet with the comma; share line aimed at a friend, no insult; "General info, not safety training."; a question; five topic hashtags, no #fyp. OK.
- description (YouTube field): every tip and the 65 line match the pages. OK.

## Could not verify
- Whether a crown counts as "jewelry": it is the joke's prop, not a claim; left as is.
- The render: not done, so the voice check and the length after the 14 added words are not measured. Estimate about 88 s from the writer's plan (83.36 s at 251 words); only the render can confirm it stays inside 65 to 92 s.
- Card fit: the two added credit rows (size 40) and the resized row (size 76) were not drawn here; look at the contact sheet after the render.
