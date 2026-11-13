# 103 - Second-model check of the funny pass on three queued bug Shorts (YouTube), 2026-11-13

Checked: the funny pass in commit 4c4f1c0 (`git diff 4c4f1c0~1 4c4f1c0 -- scripts/drawn-house/`), against MASTER_ORDERS "Make them funnier" and "Direction change", research 78 and each spec's `sources`.
Opened live: British Arachnological Society, Daddy-long-legs spider factsheet 3 (britishspiders.org.uk PDF, read 11/13). Its words: "A study of Daddy-longlegs spiders in a Hampshire garden shed between May and September found that, of the remains of 102 prey items removed from the webs, 63 were of the Common House spider (Tegenaria domestica), six were other Daddy-longlegs spiders, and the rest were unidentifiable spider remains." Also: "recorded eating the much sturdier and considerably heavier large house spiders" and "keeping out of range. Once the prey is trussed, the Daddy-longlegs spider can move in and bite".
Not re-opened: Penn State, UConn CAES, Utah State and Japyassu & Macagnan 2004 (no changed line rests on a new reading of them; research 78 and the spec quotes cover them).

## centipede-vs-spider (18.7 s)
- Line 2 "One waits in a web. One chases. Meatball just screams." and card row MEATBALL SCREAMS: OK. Joke on Meatball, no claim about either animal.
- Cut "Its messy web can hang over pipes.": OK. Nothing left leans on it.
- Line 3, CHANGE: "Threatened, it vibrates until it's hard to see. Meatball tried that at work." -> "Threatened, the spider vibrates until it's hard to see. Meatball tried that at work." Why: the cut removed the spider line that "it" pointed back to. Now "it" follows "One chases. Meatball just screams.", so a listener can hear it as the centipede (or Meatball). The vibrating is the cellar spider's (Penn State: "the spiders will rapidly vibrate in a circular fashion in the web if threatened"). The joke itself is OK (on Meatball).
- Line 4 "The centipede runs prey down at night. Meatball can't catch a damn bus.": OK. Joke on Meatball, no number or claim.
- Title, description, pinned comment: still true.
- Mild words: 1 (damn).
- Sourced facts spoken: 5 (both eat spiders; one waits in a web; vibrates when threatened; runs prey down at night; both in basements).
- Verdict: cleared with the change above.

## cellar-flick (19.2 s)
- Line 2 "It stays out of range and flicks silk. Meatball can't even wrap a damn gift." and card row MEATBALL CAN'T WRAP A GIFT: OK. BAS: throws silk "while keeping out of range". Joke on Meatball.
- Cut "Back legs flick silk while the others hold.": OK. The description and TikTok caption still say "with its back legs"; that is still true (Japyassu & Macagnan 2004: "legs IV"), and a description may say more than the video.
- Cut "Those are much heavier than it is.": OK. The hook "ties up heavier spiders" was in the cleared script before and is not made stronger by the cut. BAS still carries it ("considerably heavier large house spiders", eaten after the silk throw), and line 4 keeps "recorded" and "giant". The title "8 Skinny Legs in Your Corner Tie Up Heavier Spiders" and the pinned comment stay true.
- Line 4 "It's been recorded eating giant house spiders. Meatball lost a fight to a moth.": OK. Hedge "recorded" kept; the moth joke gives the moth no motive or danger.
- Not changed, noted: line 3 "Once it's wrapped, it moves in and bites." drops the factsheet's "can"; it was cleared in research 78 in this form and was not touched by this pass.
- Mild words: 1 (damn).
- Sourced facts spoken: 3 (stays out of range and flicks silk; bites once wrapped; recorded eating giant house spiders), plus the hook.
- Verdict: cleared.

## cellar-102 (19.8 s)
- Line 2 "Meatball's leftovers? Cold pizza." with card MEATBALL'S LEFTOVERS / COLD PIZZA: OK. Joke on Meatball. The shed fact is carried by the hook ("One shed had 102") and line 3.
- Line 3, CHANGE: "That shed's webs held 102 prey remains." -> "That shed's webs held 102 prey remains in one summer." Why: BAS counts the remains "removed from the webs" between May and September. Without a time, "held 102" reads as one cleaning, which the source does not say. "One summer" is the wording research 78 accepted for May to September.
  - Length: this adds about 0.5 s to a 19.8 s Short (the lint limit is 20.05 s). If the render runs over, also change line 6 "The rest: spider bits, too broken to name." -> "The rest: broken spider bits." (BAS: "unidentifiable spider remains"; close to research 78's cleared "The rest were broken spider bits"). Do not drop "in one summer" to make room.
- Line 5 "Six were other cellar spiders. Hell of a family dinner.": OK. BAS: "six were other Daddy-longlegs spiders", the same species as the spider in the video, so "family" is true in the loose sense and true as a taxonomic family. It is an exclamation: it claims no kinship, feeling or motive, the same call as "Just relatives. Hell of a family." in research 99.
- Line 6 "The rest: spider bits, too broken to name." then line 7 "Every single leftover was a spider.": OK. BAS: "the rest were unidentifiable spider remains", so all 102 were spiders (research 78, row 19).
- Title "Your Corner Spider Leaves Spider Leftovers: 102 in One Shed", description and pinned comment: still true. "English" and "over a summer" stay in the description; Hampshire is in England.
- Mild words: 1 (hell).
- Sourced facts spoken: 4 (102 remains in the shed's webs; 63 common house spiders; 6 other cellar spiders; the rest spider bits).
- Verdict: cleared with the change above.

## Rules checked on all three
- No joke aims at the viewer or a group; every joke is on Meatball.
- No joke adds a number, a danger or health claim, an animal's feeling or motive, or a safety instruction.
- Hedges kept ("recorded" stays). The only other hedge, "can" in the pipes line, left with that cut line.
- Mild words only, one each, none in a title, description or pinned comment.
- `python3 tools/postkit.py lint SPEC` on the three specs as committed: pass, 0 fail, 3 warn each (description does not open with the searched question; 5 hashtags; no `tags` list). These warnings come from before the funny pass. The two changes above are wording only and do not touch what lint checks, but lint runs again after they are applied.

## Could not measure
- The rendered length after the two changes (needs a render; I did not render).
- How the voice says "the spider" and "in one summer" (needs the transcript after the render).
- Whether viewers hear "it" in centipede line 3 as the centipede: a judgment, not measured.

## Second group (six Shorts), 11/13
Checked: the funny pass in commit 3581e99 (`git diff 3581e99~1 3581e99 -- scripts/drawn-house/`), same rules as above. Each Short read top to bottom for pronouns.
Opened live 11/13: University of Kentucky ENTFACT-646 (House Dust Mites); UC IPM Pest Notes: Carpet Beetles (now at ipm.ucanr.edu/home-and-landscape/carpet-beetles/; the old pn7436 address returns an empty page); Penn State Extension, Insects on Real Christmas Trees.
Not re-opened: UKY ENTFACT-609, UC IPM Clothes Moths and Pantry Pests, Penn State and Colorado State cluster-fly pages, Clemson and Utah State booklice pages. No changed line rests on a new reading of them; the spec `sources` quotes cover what is still spoken.

### dust-mites (17.9 s)
- Line 2 "Meatball hasn't washed his damn sheets since March." with card MEATBALL'S SHEETS / LAST WASHED: MARCH: OK. Joke on Meatball. It gives no order to the viewer and no health claim. The link it hints at (unwashed bedding, more mites) is one the source makes itself: "Bedding is an extremely important source for dust mite development" and "launder bedding weekly in hot water" (UKY ENTFACT-646). "March" is a fact about Meatball, not a number about mites.
- Cut "They're most numerous in beds, sofas, and carpet.": OK. The hook still says "Your bed's", and the title and description ("in your bed") stay true (UKY: "most numerous in beds").
- Line 3, CHANGE: "In ideal conditions, they're adults in a month." -> "In ideal conditions, eggs are adults in about a month." Why: (1) "they" now follows the sheets gag, and the nearest plural is "sheets"; the line it pointed back to was cut. "Eggs" also says where the month starts (UKY: "development from egg to adult", the card's EGG TO ADULT). (2) UKY says "takes about one month"; the hedge "about" was missing. The description already says "about a month". Adds about 0.3 s to 17.9 s.
- Line 4 "Adults live about one to two months. Longer than Meatball's diets.": OK. Joke on Meatball; "about" kept (UKY: "approximately 1-2 months").
- Line 5, CHANGE: "Keep humidity under 50 percent, and they struggle." -> "Keep humidity under 50 percent, and mites struggle." Why: "they" now follows "Meatball's diets", so the nearest plural is the diets. Same length.
- Title, description, pinned comment: still true.
- Mild words: 1 (damn).
- Sourced facts spoken: 4 (about 50 eggs; egg to adult in about a month; adults about 1 to 2 months; struggle under 50% humidity).
- Verdict: cleared with the two changes above.

### carpet-beetle-window (18.2 s)
- Line 2 "It lays them on wool, fur, and carpet. Meatball's whole closet is wool." and card row MEATBALL'S CLOSET: ALL WOOL: OK. "It" and "them" still point at the window bug and its eggs (line 1 is right before). Joke on Meatball.
- Cut "The eggs hatch in about 2 weeks.": OK. Title, description and pinned comment never said it.
- Line 3 "Larvae live up to 630 days, eating wool. Meatball's sweater is now a damn vest.": OK. It does not overstate: UC IPM says the larvae feed on wool, "often causing serious damage", and that carpet beetles "are more likely to damage a large area on one portion of a garment". Lost sleeves is a cartoon of that damage on Meatball's own sweater, with no number or rate. "Up to" kept (UC IPM: "220 to 630 days").
- Line 4 "They leave bristly, shed skins behind.": OK. No plural noun comes between "Larvae" and "They" (the gag has only "sweater" and "vest"). UC IPM: larvae "leave brown, shell-like, bristly-looking cast skins". This keeps the pinned comment's "shed skin" true.
- Title, description, pinned comment: still true.
- Mild words: 1 (damn).
- Sourced facts spoken: 5 (40 eggs; laid on wool, fur, carpet; larvae up to 630 days eating wool; shed skins; adults at windows, drawn to light).
- Verdict: cleared.

### christmas-tree-bugs (19.9 s)
- Line 2 "Your warm living room can hatch them. Meatball screamed.": OK. "Them" is the eggs of line 1. The scream is Meatball's reaction, not a danger claim about mantises (same call as "Meatball just screams" above).
- Line 4, CHANGE: "No food indoors, so they eat each other. Merry damn Christmas." -> "With no food, they eat each other. Merry damn Christmas." Why: Penn State says they "will eat each other if no other food is present, as is usually the case indoors during the winter". "No food indoors" drops "usually" and says every house has none. The new wording keeps the source's condition and is shorter (helps at 19.9 s, lint limit 20.05 s). The card NO FOOD / THEY EAT EACH OTHER already reads as the condition. "Merry damn Christmas" is OK: an exclamation, with no feeling or motive given to the mantises. "They" is the baby mantises of line 3.
- Title, description, pinned comment: still true.
- Mild words: 1 (damn).
- Sourced facts spoken: 6 (about 100 eggs; warmth can hatch them; dozens of babies; eat each other with no food; foamy case on twigs; clip the twig and put it in an evergreen outside).
- Verdict: cleared with the change above.

### pantry-vs-clothes-moth (18.2 s)
- Line 2 "They hatch into caterpillars that eat wool. Meatball blamed the damn dryer." and card row MEATBALL BLAMED THE DRYER: OK. "They" is the eggs of line 1. Joke on Meatball; it adds no number or damage beyond "eat wool" (UKY: "fabric-eating larvae").
- Line 3 "The adults don't eat. The larvae do. Meatball eats for both.": OK. Joke on Meatball (UKY: "Clothes moth adults do not feed").
- Cut "Clothes moths avoid light, so they're rarely seen.": OK. Line 4 "Moths in your kitchen may be different." keeps "may" and is still true on its own (UKY: kitchen moths "are possibly grain moths"). "They usually arrive in a package of food" still points at the kitchen moths. The description's "dark closets" is still true (UKY: "dark, undisturbed areas such as closets"); a description may say more than the video.
- Title, description, pinned comment: still true.
- Mild words: 1 (damn).
- Sourced facts spoken: 5 (40 to 50 eggs; larvae eat wool; adults don't eat; kitchen moths may be different and usually arrive in food packages; larvae do the eating in both).
- Verdict: cleared.

### cluster-flies (19.8 s)
- Line 2 "One warm day wakes them. They crawl out. Meatball needs three alarms." and card row MEATBALL: THREE ALARMS: OK. "Three" counts Meatball's alarms, not flies, so it adds no number about the animal. Joke on Meatball.
- Line 3, CHANGE: "They crowd your sunny windows, dazed and sluggish. Meatball, every Monday." -> "Flies crowd your sunny windows, dazed and sluggish. Meatball, every Monday." Why: "They" now comes right after "three alarms", the nearest plural. "Flies" is one syllable like "They", so the length does not change (19.8 s against the 20.05 s limit). The joke is OK: it says Meatball is sluggish, not how the flies feel. "Sluggish" is Penn State's word.
- Cut "Slightly bigger than house flies, with golden hairs.": OK. Title, description and pinned comment never said it.
- Lines 4 to 6 ("They can't breed in your house", "Their babies...", "They're just lost..."): OK. No plural noun comes between them and the flies.
- Title, description, pinned comment: still true.
- Mild words: 0. Allowed under "at most two", but under MASTER_ORDERS "Make them funnier" rule 4 ("YouTube: mild words, one or two"). Not a truth problem. If the main session wants one: "Meatball needs three damn alarms." (on Meatball, adds no claim).
- Sourced facts spoken: 5 (thousands in walls; a warm day wakes them and they crawl out; crowd windows, sluggish; can't breed indoors; young grow in earthworms outdoors).
- Verdict: cleared with the change above.

### booklice-cupboard (19.8 s)
- Line 2 "And flour, cereal, and dried fruit. Meatball's cereal expired years ago." and card row MEATBALL'S CEREAL: EXPIRED YEARS AGO: OK. Joke on Meatball. It gives no storage instruction and no health claim. "Years" is about Meatball's box, not the bugs.
- Line 3 "They like 75 to 90 percent humidity.": OK. "They" already followed a food list before the gag; the gag adds only singular nouns.
- Line 4 "They gather around leaking, sweating pipes. Meatball calls it a water feature.": OK. An opinion said by Meatball; it does not say leaks are harmless or harmful (Utah State: "around leaking/sweating pipes").
- Not changed, noted: line 5 "Dry air can wipe them out within weeks." comes after "pipes", as it did before this pass. The gag between them has only "it". Left as cleared.
- Title, description, pinned comment: unchanged and not touched by the cut (there was no cut here).
- Mild words: 0. Same note as cluster flies. If wanted: "Meatball calls it a damn water feature."
- Sourced facts spoken: 6 (about 1 mm, eating mold; flour, cereal, dried fruit; 75 to 90% humidity; leaking, sweating pipes; dry air kills within weeks; under 50%).
- Verdict: cleared.

### Rules checked on all six
- Every joke is on Meatball. None aims at the viewer or a group.
- No joke adds a number about an animal, a danger or health claim, an animal's feeling or motive, or a safety instruction. "March", "three alarms" and "years ago" are about Meatball.
- Hedges kept ("about", "up to", "can", "may", "usually"). The Christmas-tree change puts back Penn State's condition that the old wording had dropped.
- Mild words: 1, 1, 1, 1, 0, 0. None strong, none in a title, description or pinned comment.
- At least two sourced facts spoken in every Short (4 to 6).
- `python3 tools/postkit.py lint SPEC` on the six specs as committed (11/13): pass, 0 fail each. Warnings (2 or 3 each) are from before the pass: the description does not open with the searched question (four of the six), 5 hashtags, no `tags` list. The four changes are wording only. Run lint again after they go in.

### Could not measure
- The rendered lengths after the changes. Dust mites gains about 0.3 s (17.9 s, room to spare). Christmas tree gets shorter. Cluster flies should not change. I did not render.
- How the voice says "eggs are adults", "mites struggle" and "Flies crowd". Also whether "washed his damn sheets" comes out with "his" heard as "is" (the voice trap in "Make them funnier"). Needs the transcript after the render.
- Whether viewers hear "They" as the alarms or the sheets: a judgment, not measured.
