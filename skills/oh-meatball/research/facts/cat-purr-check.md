# Second-model check: cat-purr (series 68), YT and TT, 2026-11-12

Checker label: check-cat-purr. I did not write the script. I opened the sources myself, not the pack.

## Verdict
CLEARED, with one change (the YouTube title, used in both specs). The main fact holds: the PubMed abstract says all eight larynges taken from eight domestic cats made purr-range sound (25 to 30 Hz) with no neural input. The "not only a happy sound" fact holds on two live vet school pages. Every spoken line, card, search_top row, description, tag, pinned comment and TikTok caption is carried by those pages as worded. Lint after the change: YT pass (0 fail, 0 warn), TT pass (0 fail, 0 warn).

## Sources I opened (11/12)
- Herbst et al. 2023, Current Biology 33(21):4727-4732.e4. Abstract fetched raw from NCBI efetch, PMID 37794583 (https://pubmed.ncbi.nlm.nih.gov/37794583/). Quotes: "the fundamental frequency (fo) ranges of eight domestic cats ... were investigated in an excised larynx setup"; "all eight excised larynges produced self-sustained oscillations at typical cat purring rates"; "connective tissue masses, up to 4 mm in diameter, embedded in the vocal fold. This vocal fold specialization appears to allow the unusually low fo values"; "While our data do not fully reject the AMC hypothesis ... cat larynges can easily produce sounds in the purr regime with fundamental frequencies of 25 to 30 Hz without neural input or muscular contraction"; "potentially augmented by AMC".
- NC State College of Veterinary Medicine, Dr. Barbara Sherman, Q&A dated July 30, 2012 (raw HTML with curl): https://cvm.ncsu.edu/news/why-do-cats-purr-nc-state-university-college-of-veterinary-medicine-behavior-expert-explains/ . Quote: "purring may occur just prior to sleep or, surprisingly, when in pain. When veterinarians examine a cat presented for emergency treatment after having been hit by a car, they may note that it is purring." The page also says purring "is associated with positive cat-human interactions or positive cat-cat interactions".
- Washington State University, Ask Dr. Universe, September 21, 2023 (raw HTML with curl): https://askdruniverse.wsu.edu/2023/09/21/7364/ . Byline confirmed: the column quotes Dr. Sarah Guess, "a veterinarian at Washington State University". Quotes: "cats purr when they're content and when they're stressed out"; "But experts don't agree on the answer yet."; "This is a hotly debated topic among scientists".
- University of Sussex news item on McComb et al. 2009 (raw HTML): https://archive.sussex.ac.uk/broadcast/read/1208 . Not used in either cut; it gives no cat or listener count.

## Line by line
| Where | Verdict | Why |
|---|---|---|
| YT/TT hook "Why do cats purr? It's not only a happy (fucking) sound." | OK | NC State "when in pain", WSU "stressed out". Searched words are the first spoken sentence. |
| YT/TT hook card, TT search_top "WHY DO CATS / PURR?" | OK | Searched phrase word for word. |
| YT line 2 / TT lines 2-3, the lawn mower gag, "His cat left (the room. Then the house.)" | OK | On Meatball; no number, danger, feeling or motive. The cat leaving is an action, not a motive. |
| YT/TT "Vets say cats may purr when hurt or stressed, too." + card | OK | Two vets on the pages (Sherman, Guess). "May" kept. Attribution clean on TT, "Shit." after it. |
| YT/TT "Eight cat voice boxes all made a purr-like sound in a lab. No brain attached, same as (fucking) Meatball." | OK | 8 of 8 excised larynges, "without neural input". "Purr-like" and "in a lab" keep it to the setup. The insult is on Meatball. |
| Card "8 OF 8 VOICE BOXES / LAB TEST: 25 TO 30 VIBRATIONS A SECOND" | OK | Abstract: 25 to 30 Hz, the excised result (not the 20 to 30 Hz of the old muscle theory). |
| YT/TT last line "Experts still don't agree on the big one" into the hook | OK | WSU: experts do not agree on why. Runs into "Why do cats purr?". It says nothing about how, so it does not claim science has no idea. |
| Corner pill and pinned comment | OK | Open questions, no claim. |
| Title | CHANGED | See table below. |
| Description | OK | Every clause matches the abstract or the two pages. "When air was passed through them" is how an excised larynx setup works (the abstract calls it MEAD, myoelastic-aerodynamic); the abstract does not say "air", so it is a fair plain-word gloss, not a quote. |
| Tags (12) | OK | Each answered: why, how (voice boxes), stressed, frequency (card), meaning (not only happy). "how do cats purr anatomy" is answered by the voice box line and the description's tissue pads. |
| TikTok caption and title | OK | Hedge "may" kept, attribution clean, no swear, "lab study" and "8 cats" as in the abstract, five topic hashtags, no #fyp. |
| Swear count | OK | YT one mild word (damn). TT about one a line; the vets line and lab line are said clean with the reaction after. |

## Changes
| Where | Old | New | Why |
|---|---|---|---|
| `title` in cat-purr-v6-yt.json and tts-cat-purr.json | Why Cats Purr: 8 Voice Boxes Made the Sound Alone in a Lab 🐱 (Things Living In Your House #68) | Why Cats Purr: 8 Voice Boxes Made a Purr-Like Sound in a Lab 🐱 (Things Living In Your House #68) | "Alone" says the voice box does it all; the authors say their data "do not fully reject" the muscle idea and purring is "potentially augmented" by it. "The Sound" says it was the purr itself; the abstract says "sounds in the purr regime". The new words match the spoken line. 97 of 100 units. |
| `_note` in both specs | (draft note) | one sentence added that names this check | Record that the check ran. |

## Could not verify
- Herbst 2023 full text (methods, how the larynges were obtained, ethics): Cell Press returned a bot check (HTTP 403). I did not get around it. Nothing in the cuts depends on it; the cuts do not say how the cats died.
- The word "air" in the abstract: absent. Description wording rests on what an excised larynx setup is.
- McComb 2009: PubMed record has no abstract; the paper is behind the same bot check. Not used in either cut, so it blocks nothing. Number of cats and listeners: not confirmed.
- Library of Congress "Everyday Mysteries": HTTP 403 (bot check); the Wayback copy reset the connection. Not used in either cut; the two vet school pages carry the second fact.
- EurekAlert release: HTTP 403 this time. Not used in either cut.
- No share of cats that purr in pain or stress exists on either page. The cuts give none.
