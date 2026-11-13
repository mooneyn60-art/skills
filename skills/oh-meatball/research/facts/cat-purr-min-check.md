# Second-model check: cat-purr TikTok minute cut (tt-cat-purr.json), 2026-11-13

Checker label: check-cat-purr. I did not write this script. I opened the sources myself, not the pack.

## Verdict
CLEARED, with one change. Line 6 said "cats asking for food add a higher, cry-like sound inside the purr", which reads as all cats. The University of Sussex page says "Not all cats, however, use this solicitation purring". I added "some" to the line and to its card. Every other spoken line, card, search_top row, tiktok_title and tiktok_caption is carried by the sources as worded. Lint after the change: pass (0 fail, 0 warn; 16 strong words, none shown in full in the captions; caption 463 of 2,200 units, 5 hashtags). The cut stays well over 65 s (planned 87.06 s; one added word).

## Changes
| Where | Old | New | Why |
|---|---|---|---|
| Line 6, `say` | A 2009 study found cats asking for food add a higher, cry-like sound inside the purr. | A 2009 study found some cats asking for food add a higher, cry-like sound inside the purr. | Sussex page: "Not all cats, however, use this solicitation purring." Without "some" the line covers every cat asking for food. |
| Line 6, card row 2 | 2009 STUDY: CATS ASKING FOR FOOD (size 48) | 2009 STUDY: SOME CATS ASKING FOR FOOD (size 44) | Same hedge on screen; size cut so the longer row fits the same width. |
| `_note` | NOT yet checked by a second model, not rendered. | Checked 11/13 by check-cat-purr (...): one hedge added (...); not rendered. | Record that the check ran. |

## Sources I opened (11/13, curl, raw text)
- Herbst et al. 2023, Current Biology 33(21):4727-4732.e4, abstract via NCBI efetch, PMID 37794583. "all eight excised larynges produced self-sustained oscillations at typical cat purring rates"; "connective tissue masses, up to 4 mm in diameter, embedded in the vocal fold. This vocal fold specialization appears to allow the unusually low fo values"; "neurally driven electromyographic burst patterns (typically at 20-30 Hz) cause the intrinsic laryngeal muscles to actively modulate the respiratory airflow" (the old idea); "our data do not fully reject the AMC hypothesis"; "sounds in the purr regime with fundamental frequencies of 25 to 30 Hz without neural input or muscular contraction"; "potentially augmented by AMC".
- NC State College of Veterinary Medicine, Dr. Barbara Sherman, July 30, 2012: "purring may occur just prior to sleep or, surprisingly, when in pain. When veterinarians examine a cat presented for emergency treatment after having been hit by a car, they may note that it is purring."
- Washington State University, Ask Dr. Universe, 2023-09-21, quoting Dr. Sarah Guess, "a veterinarian at Washington State University": "cats purr when they're content and when they're stressed out"; "But experts don't agree on the answer yet" (on why cats purr).
- University of Sussex news item on McComb et al. 2009 (archive.sussex.ac.uk/broadcast/read/1208, dated 13 July 2009): "When humans were played purrs recorded while cats were actively seeking food at equal volume to purrs recorded in non-solicitation contexts, even those with no experience of cats judged the 'solicitation' purrs to be more urgent and less pleasant."; "an unusual high-frequency element - reminiscent of a cry or meow - embedded within the naturally low-pitched purr"; "Not all cats, however, use this solicitation purring".

## Line by line
| Line | Verdict | Why |
|---|---|---|
| 1 hook "Why do cats purr? It's not only a happy fucking sound." + card, search_top "WHY DO CATS / PURR?" | OK | Searched words are the first spoken sentence. NC State "when in pain", WSU "stressed out". Cleared before, unchanged. |
| 2 "Meatball purred back at his cat, Sauce. Broken lawn mower. Fucking tragic." | OK | Comma kept. Joke on Meatball, no claim. |
| 3 "Sauce left the room. Then the fucking house." | OK | Action on screen, no feeling or motive. |
| 4 "Vets say cats may purr when hurt or stressed, too. Shit. Meatball just whines." | OK | Two vets (Sherman, Guess). "May" kept. Credit clean, swear after. |
| 5 "One vet school says a cat hit by a car may be purring when the vet examines it. Holy shit." + card | OK | NC State quote, "may" kept, credit clean. "Holy shit" is a bare exclamation. No count of cats implied. |
| 6 2009 study, cry-like sound + card | CHANGED | "Some" added (table above). "Asking for food" says when the purr was recorded (Sussex: "actively seeking food"), not why; I read it as context, not a motive. "Meatball does that at every drive-through" is on Meatball. |
| 7 "Listeners rated those purrs as more urgent and less pleasant, even people with no cat experience. Well, shit." + card | OK | Sussex quote. "Those purrs" keeps it to the food purrs; no listener count said. A rating by people, not a feeling of the cat. |
| 8 "Meatball tried that cry on Sauce. Sauce walked the fuck off. Again." | OK | Action, no motive, no fact. |
| 9 "And how the sound gets made? It gets fucking weirder." | OK | Re-hook, no fact. |
| 10 "The old idea: the brain drives the purr with a rhythm of muscle twitches. A tiny fucking drum solo." + card | OK | Abstract: neurally driven burst patterns make the laryngeal muscles modulate airflow. "Brain" and "muscle twitches" are fair plain words; it is labelled the old idea. Simile adds no number. |
| 11 "Then in a 2023 study, eight cat voice boxes all made a purr-like sound in a lab. No brain attached, same as fucking Meatball." + card "8 OF 8 VOICE BOXES" | OK | 8 of 8 excised larynges, "without neural input". "No brain attached" is about the lab voice boxes only; the insult is on Meatball. |
| 12 "The lab sound ran about 25 to 30 vibrations a second. Low as fuck." + card | OK | 25 to 30 Hz, the excised result, said as the lab sound. "Low" matches the abstract's "unusually low". |
| 13 "Inside the vocal folds, the study found pads of tissue up to 4 millimeters wide. Fucking wild." + card | OK | "up to 4 mm in diameter" kept as a maximum. |
| 14 "The authors think those pads let the folds vibrate that slowly. ... Just a fucking kazoo." + card | OK | "appears to allow" carried by "the authors think". Kazoo is on Meatball. |
| 15 "But the authors don't claim the brain plays no part. Their data don't fully rule out the muscle idea. Sit the fuck down, Meatball." + card | OK | "do not fully reject", "potentially augmented". Swear outside the credit, aimed at Meatball. |
| 16 "Experts still don't agree on why. So when does your cat purr the fucking loudest? And" + corner pill | OK | WSU "experts don't agree" on why. Swear on a question, not on the viewer. Loops into the hook. |
| tiktok_title "Why Do Cats Purr? Not Only a Happy Sound" | OK | Same as hook, clean. |
| tiktok_caption | OK | Searched phrase first, "may" kept, "lab study", "8 cats", "no brain attached" only about the voice boxes, "his cat, Sauce" with the comma, no swear, no healing, five topic hashtags, no #fyp. Unchanged from the cleared short cut. |
| Whole cut | OK | No healing line, no "only when happy", no feeling or motive for Sauce or any cat, no insult with "you", no safety instruction. |

## Could not verify
- McComb 2009 paper itself (Cell Press bot check in the first pass; not retried). The cut uses only the Sussex page's wording, gives no cat or listener count, and keeps "a 2009 study found". Whether the paper's own wording limits the cry to some purrs or some cats beyond the Sussex line: not seen.
- Herbst 2023 full text (methods, how the larynges were obtained): not opened (Cell Press bot check, first pass). The cut does not say how the cats died.
- Whether "Sauce" is heard as the name on the render: for the render's voice check, not this check.
