# Second-model check: can dogs eat turkey (#70, slug dog-turkey)

Checker: check-dog-turkey (a different model from the writer). Date: 2026-11-12.
Files checked: `scripts/drawn-house/dog-turkey-v6-yt.json` (YouTube) and `scripts/drawn-house/tts-dog-turkey.json` (TikTok).

## Verdict

CLEARED, with the four wording changes below. The main fact holds word for word on the live ASPCA page. The FDA lines hold word for word on the live FDA page. Every safety line keeps its trigger (sharing turkey, bones, the trash) and ends with the agency's own action. No joke adds a number, a danger, a feeling or a motive. Lint: both specs pass, 0 fail, 0 warn.

One render risk: the YouTube cut was 19.53 s before "Noodle" was added (writer's scratch render). The cap is 20.05 s. If the new render runs over, cut "damn" in line 2 (the mild word) before anything else, and send the new wording back here.

## Sources opened by the checker (curl, tags stripped, 2026-11-12)

- ASPCA, Thanksgiving Safety Tips, https://www.aspca.org/pet-care/general-pet-care/thanksgiving-safety-tips (HTTP 200). Word for word: "While we recommend sticking to your pet's normal diet on Thanksgiving, ..." "If you do decide to feed your pet a small bite of turkey or other meat, make sure it's boneless and fully cooked. Raw or undercooked turkey may contain salmonella bacteria and poultry bones can be a major choking hazard."
- FDA, Keep Your Dogs and Cats Safe From Holiday Hazards, https://www.fda.gov/consumers/consumer-updates/keep-your-dogs-and-cats-safe-holiday-hazards (HTTP 200, "Content current as of: 12/17/2025"). Word for word: "And be careful what you put in the trash can. Dogs, especially, are notorious for helping themselves to the turkey carcass or steak bones, which can get stuck in your dog's esophagus, stomach, or trachea. Sharp pieces of bones can also injure your dog's mouth, esophagus, and stomach, and can cause severe internal injuries. Once your holiday meal is done, securely wrap up the table scraps and bones and dispose of them in a trash bin that your pets can't get into."
- Confirmed the fact pack's two corrections to the brief: the FDA page names "string" only with tinsel and ribbons, not in the trash paragraph; the FDA page does not mention gravy. Neither appears in the specs.
- AVMA, Household hazards: HTTP 200 but a bot-check page (Incapsula) with no text, by curl and by WebFetch; the archive.org copy could not be reached (connection reset). Not verified by me, so it was taken out (change 3).

## Changes

| Where | Old | New | Why |
|---|---|---|---|
| YouTube line 2 (spoken) | "His dog got the damn carcass out of the trash." | "His dog Noodle got the damn carcass out of the trash." | MASTER_ORDERS "What he picked to build next": Meatball's dog is Noodle, named with "his dog" the first time in every pet video from 11/12. The gag "Noodle ends up with Meatball's food" is the running gag. |
| TikTok line 2 (spoken) | "His dog got the carcass out of the trash." | "His dog Noodle got the carcass out of the trash." | Same order. |
| TikTok caption | "His dog got the carcass out of the trash." | "His dog Noodle got the carcass out of the trash." | Same order; the caption repeats the gag in the video's own words. |
| Description (both specs) and `sources` | "The AVMA says cooked turkey bones can splinter and damage a pet's mouth or digestive system." ... "Sources: ...; AVMA, Household hazards." plus the AVMA `sources` entry | "The FDA adds that sharp pieces of bones can injure a dog's mouth, esophagus and stomach." ... "Sources: ASPCA, Thanksgiving Safety Tips; FDA, Keep Your Dogs and Cats Safe From Holiday Hazards." AVMA entry removed. | The AVMA page could not be opened by the writer or the checker; the claim rested on a pack copy nobody can show. The FDA sentence is on the page I opened, with its "can" kept and "severe internal injuries" left out (no scare wording). |
| `_note` (both specs) | "Not yet checked by a second model." and the DOGT7 / DOGT5 lines | Says it was checked here, what changed, DOGT5 now in the description, DOGT7 not used | Keeps the note true for the next reader. Not on screen. |

## Lines checked and left as they are

- Line 1, both cuts: "Can dogs eat turkey? The ASPCA says if you share, make it boneless and fully cooked." The searched words open the first sentence. "If you share" keeps the ASPCA's condition ("If you do decide to feed"); the action is the agency's own. The hook card adds "IF YOU SHARE A SMALL BITE" and "NOT SURE? ASK YOUR VET". No amount is given as safe. TikTok "Fancy as fuck." is a reaction after a clean attribution.
- Line 3: "The FDA says dogs are notorious for that." "That" is the carcass out of the trash, which is the FDA's own context ("be careful what you put in the trash can"). Card "NOTORIOUS / THE FDA'S OWN WORD" is true. "Notorious" is a habit, not a motive. TikTok "Fucking notorious." is a reaction.
- Line 4: "Bones can get stuck. So wrap them up, and use a trash bin your dog can't get into." "Can" kept; trigger (bones) and the FDA's action kept, said clean. The FDA says "pets"; "your dog" is inside that. Card joke "MEATBALL CAN'T OPEN IT EITHER" and the TikTok "Meatball can't open the fucking thing either." are on Meatball and add no claim.
- Line 5: the comment question. TikTok's strong word sits in the question, not aimed at the viewer as an insult. Matches the pill and the pinned comment.
- Title: "If Dogs Eat Turkey: Boneless and Fully Cooked, Says the ASPCA". Conditional and attributed; no bare "dogs can eat turkey". It does not hold the exact searched phrase "can dogs eat turkey" (lint fails a question title) and does not lead with "Your dog"; the writer's reason in `_note` stands.
- Description: every other sentence matches the ASPCA or FDA page with its condition. Ends with "ask your vet".
- Tags: all answered by the video or its description. "can dogs eat raw turkey" is answered by "fully cooked" on the card and the salmonella line in the description, not by a spoken line. Kept.
- TikTok caption: attributions clean, conditions kept ("If you do decide to share a small bite", "can get stuck"), agency action and "Ask your vet" present, five topic hashtags, no #fyp.
- search_top: "CAN DOGS / EAT TURKEY?" is the searched phrase.

## Could not verify

- The AVMA page (bot check; archive unreachable). Now unused.
- The Google Trends numbers (mean interest 13 in November against 2 in other months), the YouTube suggestion rank and "0 Shorts found" in the brief: not re-run by the writer or me. They decide the topic, not any line in the video.
- How long the YouTube cut runs after "Noodle": not rendered by me (see the render risk above).
