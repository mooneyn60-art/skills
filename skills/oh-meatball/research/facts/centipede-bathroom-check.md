# Second-model check: "What Happens If You Leave a House Centipede in Your Bathroom" (long-form, Sat 11/21)

Checked 2026-11-18 against the live pages, not the pack. Script: `side-hustles/channels/scripts/longform-centipede-bathroom.md`. Outline: `skills/oh-meatball/scripts/longform-centipede-bathroom.outline.json` (the same lines; the outline holds every FIX line below word for word, so each needs the same change there, plus the card text).

## Verdict: FIX (17 changes, none blocking). Nothing is wrong on safety in the bite line. The script never says "harmless" or "never bites". One "harmless" does sit in the description (the Watch next title). With the FIXes below it passes.

## How each source was opened
- Kentucky ef645, Ohio State ENT-50, Missouri MDC, Mississippi State No. 29, Penn State, Maryland, Arkansas: opened as web pages, quotes match the pack.
- Ohio State's page returned 403 to the page reader. I read it with curl (same text).
- Utah State, Connecticut, Wisconsin: PDFs, read as text (pdftotext). Quotes match.
- Sombke 2021 (Frontiers in Zoology 18:57): read the abstract. It says "may be hypothesized to function as hygroreceptors" and "they lose water rapidly at low humidity". The full body was not read.

## Lines that need a FIX (old -> new)

1. **0:40 joke.** Old: "Meatball's nose has the same problem. He just licks it."
   New: "Meatball's nose feels dry. He just licks it."
   Why: "has the same problem" says a dog's nose loses water like the centipede. That is a new health claim.

2. **0:49 line and card (CB2).** Old: "But the house centipede is the only centipede that can survive inside buildings." Card "THE ONLY CENTIPEDE THAT LIVES INDOORS".
   New: "But the house centipede is the only one known to stay inside buildings all year." Card "ONLY ONE KNOWN TO STAY INDOORS ALL YEAR".
   Why: Kentucky says "only species of centipede that can survive inside". Ohio State says "Only the house centipede has been known to inhabit buildings year round". Utah State says "only the house centipede is known to remain inside year round". The old line says "only ... can survive" one breath after "most centipedes die", and the card says "lives". "Known to" and "all year" are what two of the three sources say.

3. **1:09 (CB5).** Old: "Scientists think it may sense humidity. That's not proven yet."
   New: "A 2021 paper suggests it may sense humidity. That's not proven yet."
   Why: the paper says the sensilla "may be hypothesized to function as hygroreceptors" and "very little is known about ... function". That is one research team's hypothesis, not "scientists think". The card "MAY SENSE HUMIDITY · NOT PROVEN" is fine.

4. **1:13 joke.** Old: "A built-in humidity meter. My bathroom fan doesn't even work."
   New: "A possible built-in humidity meter. My bathroom fan doesn't even work."
   Why: the joke drops the hedge from the line before it and states the sensor as fact.

5. **1:43 (CB9).** Old: "Hunting at night, they can get trapped if they fall into a sink or bathtub."
   New: "Hunting at night, centipedes can get trapped if they fall into a sink or bathtub."
   Why: Wisconsin's sentence says "Centipedes ... hunt for prey at night and can become trapped". It does not say house centipedes. (Wisconsin also calls the house centipede "originally from Mexico", which three other sources contradict. This line leans on a weaker sheet. Keep "can".)

6. **1:56 line and card (CB11), also the first paragraph of the description.**
   Old: "Mississippi State says bites are uncommon, and usually only if you handle it or press it against your skin." Card "BITES ARE UNCOMMON · USUALLY ONLY IF HANDLED OR PRESSED ON SKIN". Description: "bites are uncommon, and usually only if one is handled or pressed against the skin (Mississippi State Extension)".
   New: "Mississippi State says bites to humans are uncommon unless the centipede is handled or accidentally pressed against the skin." Card "BITES UNCOMMON · UNLESS HANDLED OR PRESSED ON SKIN". Description: "bites to humans are uncommon unless one is handled or accidentally pressed against the skin (Mississippi State Extension)".
   Why: the source says "unless", and says "accidentally". The old line adds "usually only if", which the page does not say, and drops "accidentally". The trigger a viewer can act on is handling it or pressing on it, and the new line keeps that. Same meaning, closer to the page.

7. **2:08 (CB6).** Old: "They're not aggressive, and they flee the moment they're discovered."
   New: "Connecticut says they're not aggressive and will immediately flee if they're discovered."
   Why: the page says "will immediately flee if they are discovered". The old line is flat, unattributed and drops "if". In the scene the bug sits still in the basin for a few seconds (1:56) after it is found, so the flat line is also contradicted on screen.

8. **2:26 line and card (CB12).** Old: "And they leave no traces: no droppings, no eggs, no damage to your home." Card "NO DROPPINGS · NO EGGS · NO DAMAGE".
   New: "Utah State says centipedes leave no traces, like droppings or damage to your home." Card "NO DROPPINGS · NO DAMAGE". Show two check marks, not three.
   Why: Utah State's "such as feces, eggs or damage" is a list of examples. Spoken as "no eggs", it is contradicted by 2:39, where Mississippi State says house centipedes can breed indoors. The old line also had no attribution.

9. **3:02 (CB14).** Old: "Ohio State says sticky traps show which bugs, and how many, are in your home."
   New: "Ohio State says sticky traps can show which bugs, and how many, are in your home."
   Why: the page says "By monitoring with sticky traps, you can observe which and how many". Adding "can" keeps that hedge.

10. **3:11 (CB18).** Old: "Mississippi State says focus control on the bugs they eat, and cut indoor moisture."
    New: "Mississippi State says to focus on the bugs they eat, and cutting indoor moisture also helps."
    Why: the page says controlling the other household pests is the focus and moisture reduction "also aid[s] in control". The old line makes both the main step and is garbled for the voice.

11. **3:21 (CB15), and the description's "What the sources suggest".** Old: "To keep them from coming out in the open, Connecticut's experts suggest fans or dehumidifiers." Description: "fans or dehumidifiers to keep them from coming out in the open".
    New: "To discourage them from coming out in the open, Connecticut's experts suggest fans or dehumidifiers." Description: "fans or dehumidifiers to discourage them from coming out in the open".
    Why: the page says "To discourage centipedes from appearing out in the open". "Keep them from" promises more than the source.

12. **3:35 (CB17) and 3:38 joke. This is the winter flag.**
    Old 3:35: "Can't live with it? Maryland Extension says escort it outdoors." Old 3:38: "Meatball held the door for ten minutes. It went back under the mat."
    New 3:35: "Can't live with it? Maryland Extension says escort it outdoors. But Penn State says house centipedes do not survive winters outdoors in Pennsylvania." Add the card line "COLD WEATHER: THEY DON'T SURVIVE WINTERS OUTDOORS (PENN STATE, PA)".
    New 3:38: "Meatball held the door open for ages. It went back under the mat."
    Why: Maryland gives no weather condition. Penn State's page says "House centipedes do not survive winters outdoors in Pennsylvania, but readily reproduce in heated structures". The video is out Sat 11/21, shows snow blowing through the door and uses a card that says "escort it outside". The old text reads as "outside in winter is fine". The Penn State line is true only for Pennsylvania, so the new line says Pennsylvania. Missouri says they move indoors in winter (1:00), which fits. In the 3:38 joke, "ten minutes" is a number added by a joke.
    Also: Maryland gives no way to "escort" one, and the bite line says handling is the trigger. Do not voice a method. The paper cup is a drawn prop only.

13. **3:47 line and card (recap).** Old: "It hides by day, hunts by night, and points you to the damp." Card "HIDES · HUNTS · POINTS TO THE DAMP".
    New: "It hides by day, hunts by night, and prefers the damp." Card "HIDES · HUNTS · PREFERS THE DAMP".
    Why: no opened source says seeing one tells you your bathroom is damp. That claim is in the script's own UNSOURCED list (the student-prepared museumpests sheet). Kentucky says they "associate with the more humid areas" and Connecticut says they "prefer cool, humid, dark environments", so "prefers the damp" is carried.

14. **4:01 line and card.** Old: "Next: every bug in your house, ranked. It's on the channel."
    New: "Next: six house bugs, ranked. It's on the channel."
    Why: the flagship ranks six suspects ("Six suspects live in this house with me", `side-hustles/channels/scripts/` flagship script). "Every bug in your house" is false. Card "WATCH NEXT: HOUSE BUGS RANKED" is fine.

15. **Description, Watch next.** Old: "House Bugs Ranked by Meatball, From Harmless to Get Out: [link]"
    New: "House Bugs Ranked by Meatball: [link]"
    Why: it is the real title of the Wed 11/18 video (`posted.csv`), but it puts the flat word "harmless" in this video's description, and this brief bans it. The link carries the title anyway.

16. **Description, second paragraph.** Old: "Every fact comes from a university extension, a state agency or a peer-reviewed paper, listed below."
    New: "The facts come from university pages, state agencies and one peer-reviewed paper, listed below."
    Why: the list includes a university museum page (Arkansas) and a PestSense page (Washington State). Minor.

17. **Title option 3.** Old: "I Left a House Centipede in My Bathroom for a Week"
    New (if chosen): "Meatball Left a House Centipede in His Bathroom for a Week"
    Why: as written it claims a real week-long test. The pack's "could not measure" list says no source follows one centipede for days, and the video is a drawn story with the AI label. Titles 1 and 2 are fine. Prefer 1 or 2.

## Line-by-line result (everything not listed above is PASS)

| Time / item | Result | Quote or note |
|---|---|---|
| 0:00, 0:04, 0:09, 0:11, 0:15 | PASS | Typed question, story beats, three outcomes as a question. No claim. |
| 0:20 CB1 | PASS | "Kentucky entomologists say house centipedes associate with the more humid areas, like bathrooms." Page: "such as bathrooms". Hedge kept. |
| 0:24 CB1 | PASS | "But they can often turn up in other rooms, too." Page: "can often be found in other rooms". |
| 0:28 | PASS | "Short answer: water." Carried by Ohio State, Utah State and Sombke. |
| 0:31 CB3 | PASS | "Ohio State says centipedes lack the waxy coating that helps hold water inside the body." Page matches. |
| 0:36 CB3 | PASS | "So they lose water fast when the air is dry." Sombke: "lose water rapidly at low humidity". Utah State: "easily lose water". The cause comes from those two, not Ohio State; fine as written. |
| 0:43 CB4 | PASS | "Most centipedes that wander into a house die shortly after, from the lack of moisture." Kentucky: "Most millipedes and centipedes will die shortly after entering a structure due to the lack of moisture." "Most" kept. |
| 0:53 CB2 | PASS | "It can live its entire life indoors." Ohio State, with "can". The calendar visual must not imply it never goes outside. |
| 0:56 joke | PASS | "Rent free. In my bathroom. I pay the water bill." No fact. Does not say it drinks (that is on the UNSOURCED list). |
| 1:00 CB7 | PASS | "Missouri's Department of Conservation says they turn up indoors especially in winter." Page: "especially in winter, when they move indoors". |
| 1:04 joke | PASS | "Great. It's November." Date only. It dates the video; fine for the 11/21 post. |
| 1:05 CB5 | PASS | "a weird little opening" at the base of the antennae. Page: "peculiar opening at the base of their antenna". |
| 1:17, 1:22, 1:48, 1:51, 1:53 | PASS | Story and re-hook lines. No claim. |
| 1:24 CB6 | PASS | "nocturnal and incredibly wary", attributed to Connecticut. Page matches. |
| 1:28 CB7 | PASS | "They patrol floors and walls in search of food." Missouri matches. |
| 1:32 joke | PASS | "Meatball patrols the kitchen the same way. Different menu." No fact. |
| 1:35 CB8 | PASS | "flies, crickets, moths and earwigs" are all on Missouri's list. The menu-card cuts must not say they live in your bathroom. |
| 1:38 CB8 | PASS | "Its legs are barbed to help hold prey." Missouri matches word for word. |
| 1:41 joke | PASS | "Velcro legs. Meatball wants Velcro legs." A comparison, and the gag shows it not sticking. Keep the visual from showing the bug's legs sticking to anything. |
| 2:03 | PASS | "So I don't grab it. I build it a towel ramp. I'm a host now." Meatball's action. Keeps the bite condition. Not advice. |
| 2:12 CB6 | PASS | "It darts away and hides under anything." Connecticut: "dart away and hide under anything". |
| 2:16 joke | PASS | "I'm not stepping on that bath mat until Thursday." No fact. |
| 2:19 | PASS | Story re-hook. |
| 2:22 CB12 | PASS | "Utah State says that by day, centipedes hide in crevices or cracks." Page matches. |
| 2:31 joke | PASS | "Cleanest roommate I've ever had. Low bar." Joke on Meatball. Not a hygiene claim about the bug. Keep it that way. |
| 2:35 | PASS | Story re-hook. |
| 2:39 CB10 | PASS | "Unlike other centipedes, house centipedes can breed indoors, especially where it's moist or humid." Mississippi State: "able to breed indoors, especially in areas that are moist or humid". |
| 2:44 joke | PASS | "My bathroom is basically a swamp with a mirror." No fact. |
| 2:47 CB13 | PASS | "if you see them often, Penn State says that points to plenty of the bugs they eat." Page: "If house centipedes are seen frequently, this indicates that some prey arthropod is in abundance". Drops "may signify a greater problem". That drop makes it milder, not stronger. |
| 2:54, 2:59 | PASS | Story re-hooks. |
| 3:08 joke | PASS | "Meatball tested the first one with his own paw." Joke on Meatball. Show him free again quickly; do not make a point of a stuck pet. |
| 3:16 CB15 | PASS | "Utah State says dry out damp areas, like the laundry room and the bathroom." Page: "Dry out damp areas in the house (e.g., laundry room, furnace, bathroom, etc.)". |
| 3:27 joke | PASS | "My fan works now. It only took a centipede." No fact. |
| 3:30 CB16 | PASS | "skip the bug bomb. Ohio State says those are ineffective against centipedes." Page: "Total release aerosols (so-called 'bug bombs') are also ineffective against centipedes". The can is never shown going off. "Always read the label" is in the description. |
| 3:43, 3:52, 3:55, 3:58 | PASS | Callback, Meatball's opinion, comment prompt. "VERDICT: IT STAYS" is his opinion and comes after the bite condition and the "can't live with it" line. |
| Pinned comment | PASS | "Where did you last find a house centipede, and did it get the shoe or the towel ramp?" Open question, no claim. |
| Titles 1 and 2, thumbnail labels | PASS | Questions only. No banned word. |
| Description, first paragraph, Kentucky half | PASS | Matches Kentucky. The bite half is FIX 6. |
| Description, chapters | PASS | Match the section headers. Times are estimates; reset from the render. |
| Description, Sources | PASS | Every URL opened and matches its source name. |
| "What the sources suggest" | FIX 11 only | Utah State and Ohio State halves match. |

## Checks the brief asked for
- **Flat safety claims ("never bites", "harmless"):** none in any spoken line, card, title or comment. One "Harmless" in the description's Watch next title (FIX 15). 2:08 "not aggressive ... flee" was flat and unattributed (FIX 7).
- **Dropped conditions:** 0:49 (FIX 2), 1:43 (FIX 5), 2:08 (FIX 7), 2:26 (FIX 8), 3:35 winter (FIX 12). "accidentally" in the bite line (FIX 6).
- **Jokes that add facts:** 0:40 (FIX 1), 1:13 (FIX 4), 3:38 "ten minutes" (FIX 12). The other jokes are clean.
- **"May sense humidity":** hedged twice in the script and not stated as proven. The risk was 1:13 dropping the hedge (FIX 4) and "Scientists think" being broader than one paper (FIX 3).
- **Putting it outside in winter:** FIX 12.

## Could not measure
- Sombke 2021: only the abstract and the first 100,000 characters were read. The full paper (146,000 characters) was not.
- Whether the house centipede is the only centipede that can survive indoors: Kentucky says so flat; Ohio State and Utah State say "known to". That is why FIX 2 uses "known to".
- How a viewer should "escort" one without handling it: Maryland gives no method.
- Penn State's winter line is for Pennsylvania only. No source was found for other states.
- Whether a flat count of "plenty of bugs" is shown on traps: the visual shows no number (checked in the script text only; the render was not seen).
- The render, cards and burned captions were not seen. Only the script and outline text were checked. The outline's `cap_swap` and card strings need the same edits as above.
- Not a fact issue: the description's first sentence is not the typed question (MASTER_ORDERS "Tags and everything", item 2). That is for the metadata pass.
