# Second-model check: cat-lilies (#71), YouTube and TikTok cuts, 2026-11-16

Checker label: check-cat-lilies. Checked: `scripts/drawn-house/cat-lilies-v6-yt.json` and `scripts/drawn-house/tts-cat-lilies.json` against the live source pages, not the pack.

## Verdict

CLEARED, with one wording change on both cuts. The main fact holds on the FDA page as worded: the whole plant of the "true lily" and "daylily" families is toxic to cats, pollen and vase water included, and a small amount "can cause your cat to develop fatal kidney failure in less than 3 days". The one fix: spoken line 3 said "Licking pollen or drinking vase water can cause fatal kidney failure..." with no lily and no cat in the sentence. Heard alone (or clipped), it says any pollen or any vase water causes kidney failure, in anyone. It now says "Lily pollen or vase water can give a cat fatal kidney failure in under three days." Same syllable count (23), so the length should not move. Lint passes on both specs with 0 fail and 0 warn.

## Sources opened today

- FDA, "Lovely Lilies and Curious Cats: A Dangerous Combination" (Content current as of: 09/16/2021), fetched with curl 2026-11-16: https://www.fda.gov/animal-veterinary/animal-health-literacy/lovely-lilies-and-curious-cats-dangerous-combination
  - "Lilies in the "true lily" and "daylily" families are very dangerous for cats. The entire lily plant is toxic: the stem, leaves, flowers, pollen, and even the water in a vase."
  - "Eating just a small amount of a leaf or flower petal, licking a few pollen grains off its fur while grooming, or drinking the water from the vase can cause your cat to develop fatal kidney failure in less than 3 days."
  - "The toxin, which only affects cats, has not been identified. Dogs that eat lilies may have minor stomach upset but they don't develop kidney failure."
  - "if treatment is delayed by 18 hours or more after ingestion, the cat will generally have irreversible kidney failure."
  - Table "most dangerous lilies for cats": Asiatic, Daylily, Easter, Japanese Show, Oriental, Rubrum, Stargazer, Tiger, Wood.
  - "Other plants may have the word "lily" in their name but they aren't in the "true lily" or "daylily" families and don't cause kidney failure in cats." Calla and peace lilies are under "Less Harmful "Lilies"" ("The signs usually go away on their own").
  - "If you suspect that your cat has eaten any part of a lily or its pollen or has drunk water from a vase containing lilies, immediately call your veterinarian or a pet poison control center."
- ASPCA, Lily page, fetched 2026-11-16: https://www.aspca.org/pet-care/animal-poison-control/toxic-and-non-toxic-plants/lily : "Scientific Name: Lilium species ... Toxicity: Toxic to Cats Non-Toxicity: Non-Toxic to Dogs, Non-Toxic to Horses Toxic Principles: Unknown Clinical Signs: Cats: kidney failure." Also "A consultation fee may apply."
- ASPCA, Easter Lily page, fetched 2026-11-16: "Toxic to Cats ... Non-Toxic to Dogs ... Cats are only species known to be affected."
- ASPCA, Plants Toxic to Cats list, fetched 2026-11-16: https://www.aspca.org/pet-care/animal-poison-control/cats-plant-list : "Day Lilies (many varieties) | Scientific Names: Hemerocallis spp." (also "Orange Day Lily", Hemerocallis graminea).

## Changes

| Where | Old | New | Why |
|---|---|---|---|
| YT line 3, spoken | "Licking pollen or drinking vase water can cause fatal kidney failure in under three days." | "Lily pollen or vase water can give a cat fatal kidney failure in under three days." | The sentence named neither lilies nor cats. FDA's claim is lily pollen and water from a vase with lilies, in cats (fact pack trap: "loses 'to cats'"). Same 23 syllables, so no length change expected. "can" and "under three days" (FDA "less than 3 days") kept. |
| TT line 4, spoken | "Licking pollen or drinking vase water can cause fatal kidney failure in under three days. Holy shit." | "Lily pollen or vase water can give a cat fatal kidney failure in under three days. Holy shit." | Same. The swear stays after the fact as a pure reaction. |
| `_note`, both specs | "NOT yet checked by a second model." | "Checked by a second model 11/16 (research/facts/cat-lilies-check.md): line 3 now names the lily and the cat." | Record only. |

## Lines read and left as they are

- Line 1, both cuts: "Are lilies poisonous to cats? True lilies and daylilies (fucking) are." The searched words are the first spoken sentence. The condition (true lilies and daylilies) is FDA's. Card "TOXIC TO CATS / TRUE LILIES + DAYLILIES. EVEN VASE WATER": FDA word for word in meaning. OK.
- Line 2 gag, both cuts: "Meatball bought lilies, saw his cat, Sauce, and walked them the hell (fuck) out." Card "LILIES? / MEATBALL READ THE LABEL". An action by Meatball; no number, no danger claim, no feeling or motive for Sauce, does not say it saved Sauce. "Read the label" is a joke about Meatball, not a claim that lilies carry a label. One mild word on YouTube (hell). OK, borderline only on the card's wording, kept as the brief's gag.
- TT line 3: "Meatball wanted a hug. Sauce walked off. Fucking typical." The want is Meatball's; Sauce only acts. "Fucking typical" is a reaction to the running gag, not a claim about cats. Card "NO HUG / SAUCE WALKED OFF": action only. OK.
- Line 3 card, both cuts: "POLLEN OR VASE WATER / CAN CAUSE KIDNEY FAILURE IN UNDER 3 DAYS". Claims less than FDA (no "fatal"); "can" kept. Sits under the spoken line that now names the lily and the cat. Left as is: "LILY POLLEN OR VASE WATER" at 88 px would likely run wider than the frame. OK.
- Line 4 (YT) / line 5 (TT): "Untreated 18 hours? Generally permanent damage. Call the vet now. (Fuck.)" FDA: delayed 18 hours or more, "generally" irreversible kidney failure. "Generally" kept; "or more" is on the card ("18+ HOURS UNTREATED"). The instruction is said clean, the swear after it. Its trigger is on the card ("ANY BITE, LICK OR SIP? CALL THE VET" = FDA's eaten any part, pollen, vase water). FDA says vet or pet poison control center; "the vet" is the half of that we say, not a different instruction. No dose, no home remedy. OK.
- Last line, both cuts, the corner pill and the pinned comment: a question about the viewer's cat, no claim, no insult at the viewer; TT "worst fucking thing" sits on the thing. Loops into "Are lilies poisonous to cats?". OK.
- `search_top` "ARE LILIES POISONOUS / TO CATS?": the searched phrase. OK.
- YouTube title "True Lilies Are Poisonous to Cats, Even the Vase Water 💐 (Things Living In Your House #71)": searched words start at character 6; "True" keeps the condition; vase water is FDA's. 91 of 100 units. OK.
- Description, both specs: every line matches the FDA page (true lily and daylily families; whole plant; small amount, a few pollen grains, vase water; "can", "less than 3 days"; 18 hours or more, "generally irreversible"; the trigger and "veterinarian or a pet poison control center"; Easter, Stargazer, Tiger, Asiatic, daylilies are in FDA's table; peace and calla lilies "not true lilies" and "milder" = FDA "Less Harmful", never "safe"). "The ASPCA lists true lilies as non-toxic to dogs": ASPCA Lily (Lilium species) page. OK.
- Tags (12): "are lilies poisonous to cats", "are lilies toxic to cats", "lilies toxic to cats", "lilies and cats", "cat lily pollen", "lilies cats pollen" are answered by lines 1 and 3; "are lilies dangerous to cats" and "are lilies deadly to cats" by "can give a cat fatal kidney failure" (hedge in the answer); "cat lily poisoning" by the call-the-vet line; it promises no treatment advice beyond that. OK.
- TikTok caption: the FDA attribution is clean; "the whole plant is toxic to cats, even the pollen and the vase water" and "can cause fatal kidney failure in under 3 days" are FDA's; the safety line keeps its trigger ("may have eaten any, licked the pollen or drunk the vase water") and FDA's two contacts; the gag line and the share line add no claim; the pick question is open. Five hashtags, no #fyp. OK.
- TikTok title: no new claim. OK.
- Do-not-say list: no "all lilies", no peace lily or calla as deadly, no "one lick always kills", no dogs at risk, no death rate, no "it is free", no home remedy, no named toxin. All clear.

## What I could not verify

- Length after the change. Not rendered here. The new line has the same 23 syllables as the old one; the writer's plan was 19.26 s (YT) and 24.86 s (TT). Check the render: the YT cut must stay at or under 20.05 s. Re-transcribe: "Lily pollen" should be heard as two words.
- The drawn prop in the gag is a generic leafy potted plant (`tc_prop` kind "plant"), not a lily bouquet; the card "LILIES?" names it. Not a fact error, but the picture does not show a lily. If the main session registers `cl_lily` in `tools/drawn.py` (the spec `_note` says how), the gag matches the words.
- The three outcome papers (Fitzgerald 2010, Slater 2011, Bennett 2013) were not opened: no spoken line, card or text uses them.
- Pet Poison Helpline was not re-opened: no line cites it.
- Search ranks of "are lilies poisonous to cats" (YouTube and Google): the brief's numbers, not re-checked (no YouTube pages allowed).
- Hashtags: the YouTube description has two topic hashtags (#cats #catfacts), where the standard asks for three from the topic's own feeds; the TikTok five were not measured against TikTok's suggested searches. True either way; a metadata pass, not a fact issue.
- The FDA page is dated 09/16/2021. It is still live on the FDA site today; I found nothing newer that contradicts it.
