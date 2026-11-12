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
