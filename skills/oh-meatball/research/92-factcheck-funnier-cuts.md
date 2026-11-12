# 92 - Second-model check of the funnier cuts (7 shorts, YT + TT), 2026-11-12

Checked against research/84 (do-not-say lists), research/86, v6-yt files at 0b9f74c and the two checked TT scripts. All * lines are word-for-word identical to 0b9f74c. Not re-opened: the original papers (relied on 84/86). Cat-sugar and moose facts are not in 84; unchanged lines only.

- moose-wms, YT line 5, CHANGE: "So Meatball ran like hell, and lived, because" -> "Meatball survived, and ran like hell, because" (the order checked in 86). Rule 7: "ran, and lived" reads as the tactic saving him.
- moose-wms, TT line 5, CHANGE: "So Meatball ran like hell, and fucking lived, because" -> "Meatball fucking survived, and ran like hell, because". Rule 7, same reason.
- moose-wms, YT/TT line 4: OK. Instruction clean, "Thank fuck" comes after it (rule 4). Line 3 "Meatball caught both": OK (joke on Meatball).
- cat-sugar YT/TT line 2: OK. "Probably" keeps the hedge (rule 2); card OK.
- cat-sugar YT/TT line 4: OK, borderline. "like you owe it money" is a narrator simile; the staring was already checked.
- cat-sugar YT/TT line 6: OK. "don't bake" is a joke callback, not a safety instruction.
- cat-sugar TT lines 1, 3, 5: OK (pure reactions, hedge "most likely" kept).
- dog-guilty-look YT line 2: OK (Meatball joke, no claim about dogs).
- dog-guilty-look YT line 5: OK. "Unfair as hell" is the narrator's opinion (rule 3); it still stands without the "obeyed" sentence.
- dog-guilty-look TT lines 1-6: OK. Hedge "may not be a confession" kept; line 2 is a simile on the look; line 6 matches the checked TT wording.
- grizzly-wms YT line 2: OK ("Meatball is not a racehorse" is a Meatball joke; "Bears will chase" is as checked).
- grizzly-wms TT line 1: OK. Park Service attribution clean, "Fuck that" after it (rule 4).
- grizzly-wms TT lines 2-5: OK. Play-dead and fight-back instructions are clean with the reaction after (rule 4); "Meatball is now the fucking tennis ball" and "Nothing's guaranteed" are as checked (rule 7).
- cat-name YT/TT line 2 and card "9 YEARS / ONE EAR. ONCE.": OK (Meatball joke, matches "ear/head movement" result).
- cat-name TT lines 3, 4, 5: OK (reactions only). Hedge "probably" kept in lines 1 and 7 (rule 2).
- cat-name TT line 6: OK. CN-F8 supports it (cafe cats did not tell own name from housemates' names; 10 cats, authors guess why). "Awkward as fuck" is an opinion. Borderline: "in the test" would be safer, not required.
- shark-wms YT/TT line 2 and card "MEATBALL: NUMBER 66?": OK. Alone + dusk are ISAF quick tips (SH-F14); swim alone and dusk break two. Joke is about Meatball.
- shark-wms TT line 1: OK, borderline. "That's fucking it" only leans on "the whole world" and the ISAF low-risk view; no new number. Nothing says a tactic saved Meatball (rule 7).
- shark-wms TT lines 3, 4: OK. Instructions clean, "Scary as fuck" / "Fucking hell" come after (rule 4); bear and shark advice never share a line.
- dog-tail-wag YT line 4 and card "LEFT WAG / AWKWARD": OK (Meatball joke; says nothing about the dog's mood).
- dog-tail-wag TT lines 2, 3, 5, 6: OK. "Cute as fuck", "Oh shit", "Fuck" are reactions; line 5 is the checked "acted more anxious" fact; "lean, not a fucking rule" keeps the hedge.
- Rule 6 YT counts: cat-sugar 1 (damn), moose 2 (dumbass, hell), dog-guilty 1 (hell), grizzly 1 (hell, accepted), cat-name 1 (damn), shark 1 (damn), tail wag 2 (hell, damn). All within two, all mild words.
- Rule 8: each video keeps at least two sourced facts (cat-sugar has 3 without tiger/cheetah; moose 3; dog-guilty 3; grizzly 3; cat-name 4; shark 3; tail wag 3 YT, 4 TT).
- Rule 5: nothing aimed at the viewer or a group; no slurs. "You know the face" and the "comment" prompts are not insults.
- cat-sugar, dog-guilty-look, grizzly-wms, cat-name, shark-wms, dog-tail-wag: cleared (YT and TT).
- moose-wms: cleared with the changes above (YT and TT).

## After the check (main session, 11/12 about 11:10 ET)
Small edits made after the lines above were cleared. None adds a claim.
- Trims, to keep the TikTok cuts near 25 s: dog-guilty-look TT lost the sentence "And the effect was bigger in dogs that obeyed." (the line is now the cleared YouTube wording with the TikTok reaction); cat-name TT lost the cat-cafe line.
- Clearer gag lines, same meaning (a bare "his" was swallowed by the voice and heard as "is"): "Meatball baked his cat a birthday cake", "Meatball scolded his dog for an hour", "Meatball has called his cat for nine years".
- cat-name line 5, YouTube and TikTok: "Fewer than one in ten let out a meow." in place of "...meowed or took more than a step." The Andrew voice's "meowed" is heard as "me out" (same finding as in the long-form). It claims less than the cleared line, not more: research 84 row CN-F3 quotes "fewer than 10% of the cats demonstrated vocalisation, tail movement, and displacement". The card now reads "UNDER 1 IN 10 / EVEN MEOWED", the words of the checked title.
- Pauses between lines shortened; no wording effect.
- Voice check: all 14 final renders transcribed (faster-whisper small.en) and compared with their scripts. Word counts are equal on all 14 and every last line is there. What differs is single mis-heard words: hands/hand, it/it's, stalked/stalks, thank/think, yours/ears.
- One trap: `tools/drawn.py` exits with an error and leaves the previous mp4 in place when the voice service returns no audio. The TikTok cat cut kept its old file that way and only the transcript showed it ("baked his a birthday cake"). Re-rendered and re-checked. Check the exit code after every render.
- Final lengths: YouTube 19.9, 18.7, 20.0, 19.4, 19.5, 19.8, 17.8 s; TikTok 22.9, 20.7, 25.8, 25.2, 23.6, 23.6, 23.6 s (cat sugar, moose, dog guilty look, grizzly, cat name, shark, tail wag).
