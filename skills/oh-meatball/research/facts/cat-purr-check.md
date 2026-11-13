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

## Second pass (11/12, check-cat-purr)

### Verdict
CLEARED, no changes. The main session's new wording (the cat's name, the closing question, the corner pill, the TikTok share line and quick pick) adds no claim, drops no hedge, condition or credit, and puts no feeling or motive on Sauce. The sourced lines are unchanged and still carried by the pages re-read in the first pass. Lint after this pass: YT pass (0 fail, 0 warn; 1 mild word, title 97 of 100 units, 12 tags), TT pass (0 fail, 0 warn; 6 strong words, none shown in full in the captions; caption 462 of 2,200 units, 5 hashtags).

### What I re-opened
- WSU Ask Dr. Universe, 2023-09-21, raw HTML again (https://askdruniverse.wsu.edu/2023/09/21/7364/). Context of the "experts" line: "Scientists have two ideas about why cats purr. ... But experts don't agree on the answer yet." So the answer they do not agree on is why cats purr. Byline still Dr. Sarah Guess, "a veterinarian at Washington State University".
- `tools/drawn.py` `at_time`: "word#2|75%" means the second spoken word that starts with "sauce", else 75% of the line.

### Changed wording, line by line
| Where | Verdict | Why |
|---|---|---|
| YT line 2 "Meatball purred back at his cat Sauce. Broken damn lawn mower. Sauce left." | OK | "his cat Sauce" names the cat the first time, as MASTER_ORDERS asks. The joke is on Meatball. "Sauce left" is an action, no motive, no fact. One mild word (damn). |
| YT beat 2 anchors "sauce#2\|75%" (gest and hero_moves) | OK | "Sauce" is spoken twice ("his cat Sauce." and "Sauce left."), so #2 lands on "Sauce left", where the cat walks out. No other word in the line starts with "sauce". The 75% fallback stays. |
| TT line 2 "Meatball purred back at his cat Sauce. Broken lawn mower. Fucking tragic." | OK | Same as YT. "Fucking tragic" is a reaction to Meatball, not a claim. Anchors "tragic" and "fucking" are both in the line. |
| TT line 3 "Sauce left the room. Then the fucking house." and card "SAUCE LEFT / THE ROOM. THEN THE HOUSE." | OK | An action acted out on screen, no feeling or motive, no fact. |
| YT last line "So when does your cat purr the loudest? And" | OK | A question to the viewer, no claim. It runs into the hook ("And / Why do cats purr?"). Cutting "Experts still don't agree on the big one" loses no hedge the cut needs: no YT line says why cats purr, and the description still says "Experts do not yet agree on why cats purr." The cut keeps two sourced facts (vets line, lab line). |
| TT last line "Experts still don't agree on why. So when does your cat purr the fucking loudest? And" | OK | WSU: "experts don't agree on the answer yet" to why cats purr; "still ... on why" says the same. The attribution is said clean and the swear is in the next sentence, on a question, not on the viewer. "_f" CATP11 is the right pack row. |
| Corner pill (both) "WHEN DOES YOUR CAT PURR LOUDEST? COMMENT" and the YT pinned comment | OK | Open questions, no claim; match MASTER_ORDERS "Previews and engagement" rule 2. |
| TT caption gag "Meatball purred back at his cat Sauce. Broken lawn mower. Sauce left the room. Then the house." | OK | The video's own words without the swearing. |
| TT caption share line "Send this to someone whose cat purrs like a motorbike." | OK | A simile about someone's cat, no number, sound level, health claim or motive. Not a spoken outro. |
| TT caption quick pick "When does your cat purr the loudest: dinner time or bedtime?" | OK | A question about the viewer's own cat; it asserts nothing. It does not say cats purr for food or to ask for food (McComb 2009 stays out). Bedtime sits next to NC State's "just prior to sleep". |

### Rest of both cuts, read once more
Hook, vets line, lab line, cards, search_top, title, description, tags and hashtags are as cleared in the first pass and unchanged. Searched words "why do cats purr" are still the first spoken sentence on both cuts. "May" kept on the vets line and card. No healing line anywhere. No insult aimed at the viewer.

### Changes
None.

### Could not verify (this pass)
- Nothing new. The first pass's list stands (Herbst full text and McComb 2009 behind a bot check; neither changes a spoken line).
- Whether the speech model hears "Sauce" (and not "sauce" as a common word or "source") on the render: that is for the render's voice check, not this check.
