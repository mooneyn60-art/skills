# Second-model check: cat name, TikTok minute cut (tt-cat-name.json), 2026-11-14

Checker: check-cat-name (a different model from the writer). Spec: `scripts/drawn-house/tt-cat-name.json`.

## Verdict
CLEARED, with three wording fixes (below). Every number in the cut is in the paper as worded. Lint: pass, 0 fail, 0 warn (`python3 tools/postkit.py lint scripts/drawn-house/tt-cat-name.json`, 11/14). Length is not shortened (line 11 lost two words; the plan was 82.32 s).

Source opened by the checker (not the pack): Saito, Shinozuka, Ito & Hasegawa 2019, Scientific Reports, full text at https://pmc.ncbi.nlm.nih.gov/articles/PMC6449508/ (fetched 11/14). What it says, word for word:
- Abstract: "These results indicate that cats are able to discriminate their own names from other words." and "café cats did not discriminate their own names from other cohabiting cats' names".
- Method: five recordings per cat, "four different general nouns" and then the name, played with a 15-s gap through "a speaker (Sony SRS-Z100), which was hidden from the test cat"; owners "out of their cat's sight". Experiments 1 to 3 used the owners' voices; Experiment 4 "two women unfamiliar to the tested cats".
- Experiment 1: "16 domestic cats", each living "with 2 or fewer other cats"; "eleven out of the 16 test cats decreased their average response magnitude from noun 1 to noun 4"; "nine out of the eleven habituated cats increased their response magnitude from noun 4 to their own name" (P = 0.007).
- All experiments: "more than half of the cats responded to voice stimuli by moving their ears and heads; fewer than 10% of the cats demonstrated vocalisation, tail movement, and displacement". Displacement (Table 1): "More than one step of displacement of both hind paws". This is a share of all cats tested, for all voice stimuli, not only the name.
- Experiment 4: 33 cats; "20 out of the 33 test cats decreased..."; "13 out of the 20 habituated cats increased their response magnitude from noun 4 to their own name" (P = 0.049, borderline).
- Cafe: 10 cafe cats from one cafe; the authors: "we cannot assure their generalisability".
- Why: "the association between hearing their names and receiving rewards or punishments might affect the behaviour of cats", with "food, petting, and play" and "a veterinary clinic or ... a bath" as examples.
- Training: "such discrimination is acquired without explicit discrimination training, instead emerging from the patterns of natural daily communication".

## Changes
| Where | Old | New | Why |
|---|---|---|---|
| Line 11, spoken | "cats living in a cat cafe could not tell their own name from the names of the other cats there" | "cats from one cat cafe failed to tell their own name from the names of the other cats there" | The paper says they "did not discriminate" in the test, at one cafe only, and says it cannot generalise. "Could not" said they are unable; "failed to tell" is the test result. Research 92 had flagged this line as borderline. |
| Line 11, card row 2 | "OWN NAME OR A HOUSEMATE'S? COULD NOT TELL" | "OWN NAME OR A HOUSEMATE'S? FAILED TO TELL" | Same reason; same length (14 letters). |
| description | "Cats living in a cat cafe could not tell..." | "Cats from one cat cafe failed to tell..." | Same reason. TikTok does not publish this field; changed so the spec says one thing. |
| tiktok_caption | "Cats that had settled down during the other words reacted more to their own name." | "Most cats that had settled down during the other words reacted more to their own name." | Read as "all of them". It was 9 of 11 and 13 of 20 (paper). The do-not-say list (research 84, CN) bans "every cat can do it" and gives "Most of the cats that settled down". |

## Lines checked and fine (no change)
- search_top "DO CATS KNOW / THEIR NAMES?", tiktok_title, line 1: the searched words open the first spoken sentence; "your cat ... probably" keeps the hedge.
- Line 2 and line 3: Meatball gags; "his cat, Sauce," with the comma; "Sauce walked the fuck off" is an action on screen, no motive said.
- Line 4: "A 2019 study tested it. A hidden speaker played four other words, and then the cat's name." Matches the method. Credit said clean.
- Lines 5 and 6: 11 of 16, "their reaction faded" (response went down from noun 1 to noun 4), 9 of those 11 "perked up again" (response went up at the name). "Meatball, in every meeting" is a joke on Meatball.
- Line 7: "More than half of the cats moved their ears or heads." Matches; it does not say "at their name".
- Line 8 and its card: "Fewer than one in ten let out a meow" is inside "fewer than 10% ... vocalisation, tail movement, and displacement" (cleared in research 92).
- Line 9: "Only a few took more than a step" is the pack's safe wording for displacement under 10%; the study had no come-when-called task. The swear comes after the clean clause and is aimed at Meatball.
- Line 12: Experiment 4 voices were strangers' recordings; 13 of 20 settled cats; "still reacted more" claims no more than the borderline result. The joke is on Meatball.
- Line 13: credited as "The authors' guess"; the paper's examples are food, petting, the vet. "Shit. The vet." is a reaction, no feeling of the cat said.
- Line 14: Noodle gag, "his dog, Noodle," with the comma; no claim.
- Line 15: "with no training" is the paper's "without explicit discrimination training"; credit clean; the flashcards joke is on Meatball.
- Line 16: "yours probably heard its name" keeps the hedge; the swear is not aimed at the viewer; the corner card is the question.
- No line says cats ignore anyone on purpose, come or never come when called, know the name means them, or that every cat can do it. No joke adds a number, danger, health claim or safety instruction. No insult uses "you".

## What could not be verified
- How the Andrew voice reads "failed to tell" and "one cat cafe": the cut is not rendered yet. The render's transcript check must confirm both lines.
- The nine-years gag is Meatball's story, not a fact (cleared as a gag in research 92).
- Nothing outside the 2019 paper was opened; the cut uses no other source.
