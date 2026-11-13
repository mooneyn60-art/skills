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
