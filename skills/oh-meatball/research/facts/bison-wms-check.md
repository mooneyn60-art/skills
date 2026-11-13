# Second-model check: bison-wms (Would Meatball Survive? #5)

Checker: check-bison-wms, 2026-11-12. I did not write these specs.
Specs: `scripts/drawn-house/bison-wms-v6-yt.json` (YouTube) and `scripts/drawn-house/tts-bison-wms.json` (TikTok).

## Verdict
CLEARED after 2 wording changes in each spec. The main fact holds word for word on the live page. Both specs pass `postkit.py lint` with 0 fail, 0 warn (YouTube title 99 of 100, 10 tags; TikTok caption 705 units, 5 hashtags, 5 strong words, none shown in full in captions).

## How the sources were opened
I fetched both pages myself with curl on 2026-11-12, stripped the tags and searched the text. I did not use the fact pack's quotes.
- Yellowstone Safety, https://www.nps.gov/yell/planyourvisit/safety.htm, "Last updated: July 28, 2026" on the page. Word for word on the page today:
  - "Bison may appear tranquil, but these large animals have injured more people in Yellowstone than any other animal."
  - "They can run 3x faster than humans, making it very important to give them plenty of space."
  - "Keep at least 25 yards (23 meters) from bison at all times and never approach a bison to take a photo."
  - "If need be, turn around and go the other way if a bison walks within 25 yards."
  - Heading "Run away if a bison charges", then "If approached too closely, bison may respond by bluff charging, head bobbing while staring at you, pawing, bellowing, or raising its tail. These are warning signs that you are too close and that a charge is imminent—do not stand your ground! Immediately walk or run away from the animal. If the bison follows you, spray bear spray as you are moving away, and seek cover behind nearby trees or cars."
  - The same page, general rule: "at least 25 yards (23 m) away from all other animals, including bison and elk", and 100 yards for bears, wolves and cougars. The bear advice on the same page is "stand your ground", the opposite of the bison advice. The specs have no bear line.
- Yellowstone Bison, https://www.nps.gov/yell/learn/nature/bison.htm, "Last updated: May 4, 2026". Used for the drawing only: "All bison have a protruding shoulder hump.", "Both sexes have relatively short horns that curve upward", a bull's "beard is thicker". All on the page.

## Changes
| Where | Old | New | Why |
|---|---|---|---|
| Both specs, beat 4 `say` | "Yellowstone's rule is at least twenty-five yards from bison. They can run three times faster than humans." | "Yellowstone says at least twenty-five yards from bison. They can run three times faster than humans." | The 3x is the Park Service's own ratio with no human speed and no source behind it (the pack, section 0). Spoken without a credit it sounded like the narrator's fact. "Yellowstone says" carries the credit into the 3x sentence, matches the page (an instruction, "Keep at least 25 yards"), and is shorter, so length cannot go up. The anchor word "they" for the chase is unchanged. The card keeps "PARK SERVICE" on the 3x row. |
| Both specs, `tags` | "how to survive a bison attack" | (removed; 10 tags left) | The video gives what to do when a bison charges (walk or run away) and how to avoid one (25 yards). It gives nothing about surviving an attack once a bison makes contact, and the page has no such advice. MASTER_ORDERS: no tag that promises advice the video does not give. "what to do if a bison attacks" stays: it is the YouTube search phrase and the video answers the charge. |
| Both specs, `_note` | "NOT yet checked by a second model." | A line naming this check and the two changes. | Record only. |

## Lines checked and left as they are
- Hook, both cuts: the searched phrase "what to do if a bison charges you" is the first spoken sentence, word for word. "Walk or run away, says the Park Service" (YouTube) and "The Park Service says walk or run away. Don't stand your ground. Holy shit." (TikTok): carried by the page under "Run away if a bison charges"; the condition (if it charges) is in the question and on the card ("IF IT CHARGES: U.S. PARK SERVICE"). On TikTok the instruction is said clean and the swear is the reaction after it.
- Beat 2, the selfie gag: adds no fact. "SELFIE AT 2 YARDS" is Meatball's distance in the gag, and the card's second row is the page's own rule he breaks ("never approach a bison to take a photo"). Joke on Meatball ("Tiny damn/fucking selfie stick").
- Beat 3: "Its tail went up. That's a warning sign." The page lists raising its tail among the warning signs that you are too close and a charge is imminent. No cause claim, no feeling or motive given to the bison. "Meatball waved back" is a joke on Meatball.
- Beat 4, TikTok extra: "Meatball is not a fast fucking human." A joke on Meatball, adds no number.
- Beat 5: "Meatball lived. Nothing's guaranteed, so" credits no tactic (MASTER_ORDERS rule 7) and loops into the hook. Corner pill "CLOSEST YOU'VE BEEN TO A BISON? COMMENT" is a question, no claim.
- Title: "What to Do If a Bison Charges You: It Can Run 3x Faster Than Humans". Keeps "can" and "than humans", no mph. It has no room for the credit (99 of 100 units); the description's first lines credit the Park Service. The video answers the title (walk or run away).
- Description: every sentence matches the page, with the bear-spray condition ("If the bison follows you", "as you are moving away") and no claim that spray works; "in Yellowstone" kept on the injury line; ends "General information, not safety training."
- Pinned comment: an open question, no claim.
- TikTok caption: the attribution and the instruction are clean and keep their condition ("If a bison charges"); 25 yards is "from bison"; the 3x is "it says". The share line is aimed at a friend who would take the selfie, not at the viewer, and states no fact. Five topic hashtags, no #fyp.
- search_top "WHAT TO DO IF / A BISON CHARGES YOU": the searched phrase, no claim.
- Remaining tags: each is answered by the video ("can you outrun a bison": 3x faster than humans, Park Service; "bison tail up meaning": a warning sign; "how far to stay from bison": at least 25 yards at Yellowstone; "are bison dangerous" and "yellowstone bison attack": topic tags, answered by the charge advice and the warning sign).
- Nothing in either cut says bison injure the most people anywhere, and no mph figure appears anywhere.

## What I could not verify
- The searched-phrase ranks (Google rank 1, YouTube rank 1) are from the brief and the writer's `postkit kw` run; I did not re-run them.
- The "3x faster than humans" ratio has no human speed or source on the page, so it can only be checked as the Park Service's sentence, which it is. Other NPS pages give up to 30 or 35 mph; the specs use none of them.
- Whether "25 yards" is a legal regulation in Yellowstone or only advice: the Safety page states it as an instruction and separately says it is illegal to approach wildlife "within any distance that disturbs". The specs say "Yellowstone says", which the page carries either way. The card row "FROM BISON: YELLOWSTONE'S RULE" reads the instruction as the park's rule, which is how the page presents it.
- The drawing (the "mic" prop standing in for a selfie stick, the bison turned away for the tail line) was not rendered; I checked wording only. After the render, the transcript must be compared with beat 4's new wording.

## Second pass
Checker: check-bison-wms, 2026-11-12, after the main session's changes (new closing question, a cut line in beat 3, thicker horns).

### Verdict
CLEARED after one change, made in four places on both cuts: the closing question now asks "how far away", not "how close". The main facts hold: I fetched the Yellowstone Safety page again today with curl (tags stripped, "Last updated: July 28, 2026") and every quoted sentence is still there word for word (3x faster than humans; at least 25 yards from bison and never approach a bison to take a photo; raising its tail listed among the warning signs that you are too close and a charge is imminent; do not stand your ground, walk or run away). Lint after the change: YouTube pass (0 fail, 0 warn; title 99 of 100, 10 tags, 1 mild word); TikTok pass (0 fail, 0 warn; caption 705 units, 5 hashtags, 5 strong words, none shown in full in captions).

### Rulings
1. **The warning-sign fact on the card alone: allowed.** The spoken line is now "Its tail went up. Meatball waved back." It states only an action and a joke on Meatball: no claim, no feeling or motive for the bison. The claim lives on the card "RAISED TAIL / A WARNING SIGN: PARK SERVICE", which keeps its credit and matches the page. The cut removes no condition: the line never carried the page's "you are too close and a charge is imminent", and nothing spoken now says the tail means anything else. The spoken cut still holds at least two sourced facts (walk or run away if it charges; at least 25 yards; 3x faster than humans), so "Make them funnier" rule 2 holds. The tags "bison tail up meaning" and "bison warning signs" are still answered, by the card and by the description. Risk to note, not a fault: a viewer who listens without looking misses the meaning of the tail. Caption key "warning" is now unused in speech; harmless.
2. **"How close have you been to a bison?": changed.** In a video whose gag is Meatball walking up to a bison for a selfie, "how close" makes closeness the score to beat, and the comments it pulls ("2 feet, got the selfie") reward the thing the Park Service says never to do. The question adds no claim, but it pulls against the video's own safety line. "How far away" asks the same story and keeps distance as the thing to report, and on TikTok the quick pick still names the 25 yards. Same length (8 words spoken), same loop into the hook ("How far away were you from a bison? And / What to do if a bison charges you?"). The pinned comment stays open and personal ("Previews and engagement", rule 2; "Posting", pinned comment).
3. **The survival ending:** "Meatball lived. Nothing's guaranteed." (TikTok: "Meatball fucking lived.") still credits no tactic (Direction change, rule 7). The swear is a reaction in a joke line, not inside an attribution or an instruction.
4. **Horns (drawing only):** horn_w 34 and horn_color #d9d2bd are layout keys, not wording; I made no render and did not see a sheet. The Bison page says "Both sexes have relatively short horns that curve upward". The builder must look at the sheet: short, thick, curving up from the side of the head reads as bison; thin and long reads as antennae. If wrong, try horn_w 26 or 42 (builder's call).

### Changes
| Where | Old | New | Why |
|---|---|---|---|
| YouTube spec, beat 5 `say` | "Meatball lived. Nothing's guaranteed. How close have you been to a bison? And" | "Meatball lived. Nothing's guaranteed. How far away were you from a bison? And" | "How close" can read as a dare to get close, next to the selfie gag and against the page's "never approach a bison to take a photo". Same length, same loop. |
| TikTok spec, beat 5 `say` | "Meatball fucking lived. Nothing's guaranteed. How close have you been to a bison? And" | "Meatball fucking lived. Nothing's guaranteed. How far away were you from a bison? And" | Same. |
| Both specs, beat 5 corner pill | "HOW CLOSE HAVE YOU BEEN TO A BISON? COMMENT" | "HOW FAR AWAY WERE YOU FROM A BISON? COMMENT" | The pill must match the spoken question (rule 2). |
| Both specs, `pinned_comment` | "How close have you ever been to a bison, and what did it do?" | "How far away were you when you saw a bison, and what did it do?" | Same reason; still an open question that pulls a story. |
| TikTok spec, `tiktok_caption` quick pick | "How close have you been to a bison: more than 25 yards, or less?" | "How far away were you from a bison: more than 25 yards, or less?" | Matches the spoken question; the 25 yards stays in the pick. |

Lines read again and left as they are: hook (searched phrase word for word, instruction said clean with its condition on the card), beat 2 selfie gag and its card, beat 4 ("Yellowstone says at least twenty-five yards from bison. They can run three times faster than humans." and on TikTok "Meatball is not a fast fucking human."), the title, the description, all 10 tags, search_top and the rest of the TikTok caption. Nothing new in them since the first pass.

### What I could not verify (second pass)
- The horns: no render or sheet existed for me to look at.
- Whether the new question pulls as many comments as "how close" would have: not measurable before posting.
- Lengths after the change (YouTube 20.05 s limit, TikTok 26 s): the builder's render reports them; the spoken word count of the last line is unchanged.
- The render's transcript must be compared with the new last line after the build.
