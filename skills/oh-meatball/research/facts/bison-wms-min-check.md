# Second-model check: bison-wms TikTok minute cut (Would Meatball Survive? #5)

Checker: check-bison-wms, 2026-11-16. I did not write this script.
Spec: `scripts/drawn-house/tt-bison-wms.json` (16 lines, 268 spoken words after the changes; planned 87.99 s before them, about 1 s more now, still inside 65 to 92 s).

## Verdict
CLEARED after two wording changes in the spoken lines and a fix to the spec's `sources` record. Every number, credit and safety line is on a live Park Service page today, as worded. `postkit.py lint` passes: 0 fail, 0 warn (14 strong words spoken, none shown in full in captions; caption 705 of 2,200 units, 5 hashtags).

## How the sources were opened
I fetched all four pages myself with curl on 2026-11-16, stripped the tags and searched the text. I did not use the pack's quotes.
- Yellowstone Safety, https://www.nps.gov/yell/planyourvisit/safety.htm, "Last updated: July 28, 2026". On the page word for word: "Bison may appear tranquil, but these large animals have injured more people in Yellowstone than any other animal."; "They can run 3x faster than humans"; "Keep at least 25 yards (23 meters) from bison at all times and never approach a bison to take a photo."; "If need be, turn around and go the other way if a bison walks within 25 yards."; "If approached too closely, bison may respond by bluff charging, head bobbing while staring at you, pawing, bellowing, or raising its tail. These are warning signs that you are too close and that a charge is imminent—do not stand your ground! Immediately walk or run away from the animal. If the bison follows you, spray bear spray as you are moving away, and seek cover behind nearby trees or cars."
- Yellowstone Bison, https://www.nps.gov/yell/learn/nature/bison.htm, "Last updated: May 4, 2026": "The bison is the largest land mammal in North America. Males (bulls) weigh up to 2,000 pounds (900 kg)"; "Both sexes have relatively short horns that curve upward".
- Wind Cave Safety, https://www.nps.gov/wica/planyourvisit/safety.htm, "Last updated: July 26, 2025": "Bison are more aggressive during the calving and mating season from May through August."
- Grand Teton Safety, https://www.nps.gov/grte/planyourvisit/safety.htm, "Last updated: June 25, 2026": "Maintain a distance of at least 100 yards (300 feet) from bears and wolves and 25 yards (75 feet) from all other wildlife."

## Changes
| Where | Old | New | Why |
|---|---|---|---|
| Beat 6 `say` | "Meatball was at two. Holy shit." | "Meatball was at two yards. Holy shit." | Said right after "seventy-five feet", a bare "two" is heard as two feet, while the card says "MEATBALL: 2 YARDS". The spoken gag now matches the card. |
| Beat 13 `say` | "...turn around and go the other way, the Park Service says." | "...turn around and go the other way if need be, the Park Service says." | The page says "If need be, turn around and go the other way". Without the hedge the line was firmer than the source. Credit stays clean, the swear stays in the joke after it. |
| `sources`, Bison page | "used for the drawing only" | "used for the drawing and for beats 7 and 11", with the 2,000-pound sentence quoted | Beats 7 and 11 now take their facts from that page, so "drawing only" was no longer true. |
| `sources` | (no entry) | Wind Cave Safety and Grand Teton Safety, with dates and quotes | Beats 12 and 6 use them; every number carries its source. |
| `_note` | "NOT yet checked by a second model and not rendered." | A line naming this check and its changes; "Not rendered." | Record only. |

## Lines checked and left as they are
- Beat 1 (hook): the first spoken sentence is the searched phrase word for word. "The Park Service says walk or run away. Don't stand your ground." is said clean with its credit; the condition is in the question and on the card ("IF IT CHARGES: U.S. PARK SERVICE"). The swear is the reaction after it.
- Beats 2 and 3: the selfie gag and the tail are actions and jokes on Meatball; the cards carry the page's rule ("NEVER APPROACH A BISON TO TAKE A PHOTO: PARK SERVICE") and the sign ("RAISED TAIL / A WARNING SIGN: PARK SERVICE").
- Beat 4: "a warning sign you're too close, like pawing or bellowing" is on the page with its credit and does not claim every bison shows every sign. "Meatball missed every sign" is a joke on Meatball. The card lists four of the page's five signs, all as worded.
- Beat 5: "Yellowstone says at least twenty-five yards from bison. They can run three times faster than humans." No mph anywhere in the cut (do-not-say kept); the card credits the 3x to the Park Service.
- Beat 7: "Bulls weigh up to 2,000 pounds, the Park Service says." Keeps "up to"; the card's "largest land mammal in North America" is on the Bison page.
- Beat 8: "His dog, Noodle," with the comma; Noodle gets the donut, an action, no fact.
- Beat 10: "may look calm" keeps the page's "may appear tranquil", and "in Yellowstone" stays on the injury line. No count, no "killed". "Calm, my ass" is a roast of the look that the page's own "but" answers, not a new claim.
- Beat 11: "Males and females both have horns" is the page's "Both sexes".
- Beat 12: "more aggressive May through August" is Wind Cave's wording; no "attack". The card credits Wind Cave and the Park Service. "Meatball went in July" is a joke on Meatball.
- Beat 14: the bear-spray line keeps its trigger ("If it follows you"), "as you move away", the cover behind trees or cars, and the credit, all said clean. Nothing says spray works. No bear advice anywhere in the cut.
- Beat 15: "his cat, Sauce," with the comma; Sauce walks off, an action, not a feeling.
- Beat 16: "Meatball fucking lived. Nothing's guaranteed." credits no tactic. The question asks how far away, never how close; the corner pill matches.
- No insult is aimed at the viewer; no swear sits inside a credit or a safety instruction.
- `search_top` "WHAT TO DO IF / A BISON CHARGES YOU", `tiktok_title` and `tiktok_caption`: unchanged since the cleared short cut; each sentence is on the Safety page with its condition, the quick pick asks how far away, five topic hashtags, no #fyp.

## What I could not verify
- No render or sheet: lengths after the two added words (about 1 s), the donut and Sauce drawings and the horns were not seen. The render's transcript must be compared with beats 6 and 13 as now worded.
- The "3x faster than humans" ratio has no human speed or source on the page; it is checked only as the Park Service's sentence.
- Wind Cave's "May through August" is that park's page; Yellowstone's Bison page gives mating late July through August and calving late April or May, which fits but is not the same sentence. The line names Wind Cave, so it is carried.
- The searched-phrase rank is from the brief and the first check; not re-run here.
