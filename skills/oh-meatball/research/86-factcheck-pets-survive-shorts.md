# 86 - Fact-check of the five new-direction Shorts (2026-11-12)

A second model (not the writer) checked every spoken line, card, title, description and pinned comment of five Shorts against the live sources. It opened the pages itself: PMC full texts, the PubMed abstracts through the Europe PMC API (PubMed served a cookie wall), the Park Service and Glacier pages, the Alaska bear-safety PDF, and the International Shark Attack File pages. Scripts: `scripts/drawn-house/{dog-guilty-look,grizzly-wms,cat-name,shark-wms,dog-tail-wag}-v6-yt.json`. Facts: `research/84-pets-and-survive-factpack.md`.

Result: no line was wrong on safety. 21 wordings were softened and applied before the final renders. Nothing was cut.

## What the checker changed

| Short | Was | Now | Why |
|---|---|---|---|
| Dog guilty look | "scolding hit harder on dogs that obeyed" | "The effect was bigger in dogs that obeyed." | The study says the effect of scolding was "more pronounced"; "hit harder" suggests the dogs were hurt. |
| Dog guilty look | "Poor bastards." | "Unfair as hell." | A reaction must not add a feeling claim; the study tests the look, not what dogs feel. |
| Dog guilty look | card "SCOLDING / BROUGHT OUT THE LOOK" | "SCOLDING / MORE OF THE LOOK" | "Brought out" is more causal than "more such behaviours were seen". |
| Dog guilty look | "So that face reacts to you" | "So that face reacts to your cues" | Source: "a response to owner cues". |
| Dog guilty look | description "owners could not tell" | "owners did no better than chance" | Source: "no more than expected by chance". |
| Cat name | "Your cat can tell its name from other words." and the title | "Your cat can probably tell...", title "Your Cat Can Likely Tell Its Name" | Only cats that first got used to the four words were analysed (11 of 16, 20 of 33). |
| Cat name | "Most cats answered with an ear flick or a head turn." | "More than half of the cats moved their ears or heads." | Source: "more than half of the cats responded to voice stimuli by moving their ears and heads". |
| Cat name | card "MEOWED OR MOVED A STEP" | "MEOWED OR TOOK MORE THAN A STEP" | The paper counts "more than one step" of both hind paws. |
| Cat name | description "The cats could tell their name" | "Cats that had settled down during the other words reacted more to their own name." | Same reason as the first row. |
| Tail wag | "the wag leans to the dog's right" / "it leans left" and both cards | "leans more to its right" / "leans more to its left" | A bias, not every wag. |
| Tail wag | "got faster heartbeats" | "acted more anxious" | The abstract says "higher cardiac activity and higher scores of anxious behavior", not heart rate. |
| Tail wag | title "Wags More to the Right When It Sees You" | "May Wag More to Its Right When It Sees You" | The hedge, and whose right. |
| Tail wag | "watch which way that ass leans" | "It's a lean, not a damn rule. So watch which way yours leans" | The old line invited reading any dog's mood from its tail. |
| Tail wag | description "does not mean a dog is friendly" | "does not always mean" | Wagging goes with good and bad arousal. |
| Grizzly | "Bears chase what runs" | "Bears will chase what runs" | Source: "they will chase fleeing animals". |
| Grizzly | "If a grizzly you surprised attacks, play dead: stomach down, hands behind your neck." | "If a surprised grizzly knocks you down, play dead, hands behind your neck." | A viewer cannot tell a defensive attack from a hunting one; Alaska's guide says lie down only after a defensive bear makes contact. |
| Grizzly | card "PLAY DEAD" | "PLAY DEAD / ONLY IF IT KNOCKS YOU DOWN / STOMACH DOWN, HANDS BEHIND YOUR NECK" | A bare "play dead" is the worst error in the pack. |
| Grizzly | "Meatball survived by lying still" | "Meatball lived. Nothing's guaranteed" | The Park Service says no strategy guarantees safety. |
| Grizzly | description: three sentences | credited to the Park Service; "stalked you then attacked or attacked in your tent" | "Surprised" is Alaska's word, not the Park Service's; the black-bear rule is the Park Service's. |
| Shark | title "65 Unprovoked Shark Bites" | "65 Confirmed Unprovoked Shark Bites" | 65 is the count of confirmed cases. |
| Shark | "Don't play dead." | "Don't act passive." | The File says "You should not act passively"; it never mentions playing dead. |

Also changed by the writer after the check, same claims in clearer words (the transcription check heard them wrong): "Whether they ate it or not" (was "Ate it or not"), "four other words, and then the cat's name", "yours probably heard its name" (was "heard you", heard as "hurt you"). "Both are on the damn don't list" became "That breaks two damn safety tips" (swim with a buddy is a do, not a don't). The cat-cafe line was added to the cat Short for length; the checker had passed the same claim in the description. On the grizzly card a third row credits the black-bear rule to the Park Service.

## Left open
- Tail wag: the 2007 and 2013 originals are paywalled. Directions come from the open 2024 review; whose left and right comes from the 2022 iScience paper. The review page does not say whose side it means.
- Glacier's sentence "Never run from a surprised bear because it can cause a predatory reaction" is in the fact pack but the checker's fetch of the page did not show it. No script line depends on it (the title rests on the Park Service's "Do NOT run").
- The shark Short's spoken lines carry no "extremely low" risk line; it is in the description.

## Lessons for the next scripts
1. "Your cat" or "your dog" plus a lab result needs "probably", "likely" or "may".
2. A reaction word must not carry a feeling or a motive ("Poor bastards", "lazy").
3. Safety cards carry their condition on the card itself.
4. After the render, transcribe: three lines were clear on paper and unclear by ear.

## Second part: the two one-minute TikTok cuts (same day, same checker)

Scripts: `scripts/drawn-house/tt-dog-guilty-look.json` (19 lines, 92.6 s, 19 f-words) and `tt-grizzly-wms.json` (16 lines, 92.3 s, 16 f-words). Two rounds: a full check, then a confirmation of the rewritten lines. Extra pages the checker opened: the Hare 2002, Scheider 2013, Muller 2015 and Andics 2016 abstracts (Europe PMC), the Park Service's Bear Spray and Firearms page, Alaska's bear-spray sheet, Yellowstone's Bear Management and Safety pages.

What it found and what changed:
- **A swear inside a safety instruction is not allowed.** "hold your fucking ground", "fight back like fucking hell", "Punch that fucker in the snout" and "So don't fucking waste that shit" became clean instructions with the reaction after them ("...stop and hold your ground. Scary as fuck."). The play-dead line was already clean.
- **A gap, not a wrong line: no spoken line said when to use bear spray.** Added: "Use it only on a charging or attacking bear" (the Park Service's sentence), with the 7 to 9 seconds credited to Alaska's wildlife agency. Spray "rides on your belt or chest, never in your backpack" (the old line only said where not to keep it).
- "Lie still until it leaves" became "Lie still until it's gone, then wait a few minutes more" (Yellowstone: "After the bear leaves, wait several minutes before moving").
- The black-bear line keeps the Park Service's order: reach a car or building if you can; if not, hit its face and muzzle. The card says "ESCAPE OR FIGHT: PARK SERVICE".
- "1 in 3.3 million visits" now carries "higher in the backcountry" (that figure is all visitors, most of them near roads), and the "now breathe" order before it was cut. The roads-versus-backcountry numbers were cut for length; their units differ (visits against person travel days) and "different planet" invited a comparison the units do not allow.
- The 91% card now says what it is 91% of: people bears injured since 1970. The tip after it is the park's own: hike in groups of three or more.
- Title "What to Do, Step by Step" became "What the Agencies Say" (the agencies differ on parts), and the caption carries "General info, not safety training."
- "You are now the fucking tennis ball" became "Meatball is now the fucking tennis ball" (the viewer is not the one who gets caught).
- Dog cut: "ran it with 96 dogs. Big fucking upgrade" became "tested 96 dogs. Bigger fucking sample" (a different design, no scolding); "Zero fucking tells" became "No fucking tells found"; "really can read" became "can read in tests"; the researcher's read keeps "better described as"; "trained on the happy face" became "rewarded for"; the Hare 2002 abstract says "human communicative signals", not pointing, so that line says "your signals" (the pointing line rests on Scheider 2013, which is about pointing); "So say good boy like you fucking mean it" (advice beyond a brain-scan study) became "Praise in a flat voice didn't fucking light them up".
- Kept on purpose: "Be fucking honest." at the end. The rule is no insult or swear aimed at the viewer; a comment prompt is allowed, and the checker agreed.
- After the render the transcription heard three lines wrong; they were re-worded for the ear with the same meaning ("in dogs that obeyed", "Praise in a flat voice", "A black bear attack is different.").

Why the grizzly cut has 16 f-words against the ordered 20 to 25: its safety instructions are said clean, and there are a lot of them.
