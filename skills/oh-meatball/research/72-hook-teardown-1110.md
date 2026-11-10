# 72 - Hook / pacing / re-hook teardown (2026-11-10) - PARTIAL

**Status: the reference teardown could not be done.** YouTube's watch pages return `HTTP 429` then "Sign in to confirm you're not a bot" for every full yt-dlp extraction from this machine (tried: 3 videos, plain, with `--js-runtimes node`, and after ~5 minutes of waiting). Search listings (`--flat-playlist`) and thumbnails (`i.ytimg.com`) still work. That means **no "Most replayed" heatmaps, no timed transcripts, no like counts** for any reference video. I stopped rather than work around the block (a further attempt via third-party YouTube front-ends was refused by the permission classifier, correctly).

What this file therefore contains: (1) the candidate pool with the metadata I could get, (2) thumbnail observations, (3) full measurements of OUR scripts, with our retention events mapped onto them, (4) provisional rewrites that rest only on our own retention curve, clearly marked as untested against references, (5) a checklist. It contains **no pattern claims or quotes about reference videos**, because I have not read any of them. Sections (b) and the reference columns of (a) are empty on purpose.

To unblock (pick one): export a `cookies.txt` from a logged-in browser and pass `--cookies`; or allow vidIQ credit spend (`vidiq_video_transcript` is 5 credits per video, gives transcripts but NOT heatmaps); or re-run from a different network. Heatmap caveat for when it runs: "Most replayed" is a proxy (counts replays and seeks, normalised per video), not YouTube's private retention graph.

### Update 11/10 (coordinator constraint, read from `channel-brain/MASTER_ORDERS.md` section "Studio data 11/3" and `KNOWLEDGE.md`)
Question asked: do the best-holding references use quiz or prediction devices, where, and does the curve reward them? **Answer: I cannot say.** The same extraction block means I have read no reference video and have no heatmap, so any statement about what holders do would be invented. What is known: (1) our own Studio data penalises quiz-style hooks on Shorts, and that is the only own-channel evidence; (2) the rewrites below now follow it. This question is the first one to answer when extraction works: for each reference, flag any "guess / what do you think / pause and predict" device, its timestamp, and the heatmap value in the 10 s around it versus the video's mean.

## (a) Candidate pool (search metadata only; hold metrics pending)

| id | channel | min | views | title | hold rank |
|---|---|---|---|---|---|
| 1B6tensgwfw | BuzzFeed Multiplayer | 4:32 | 3.9M | Do You Really Swallow Spiders When You Sleep? | pending |
| zKjFuU9d0X8 | MyWildBackyard | 23:10 | 861K | The Worst Stings in the US Ranked | pending |
| c9tv5yjmNU0 | MyWildBackyard | 21:25 | 211K | EVERY Insect in Your Backyard... | pending |
| GoBIGeoqmhY | MyWildBackyard | 7:39 | 787K | What Happens if a Cellar Spider BITES You? | pending |
| g9BMcIxrkF4 | TierZoo | 27:59 | 10.1M | The Insect Tier List | pending |
| TEyt3i8g9WU | What If | 6:03 | 154K | What If Bed Bugs Were the Size of Humans? | pending |
| YAs1Qa3a1uM | Data Ball | 6:49 | 7.3M | If Insects' Size Increased to 1000 Times | pending |
| snmgvIikuas | Insider Science | 3:19 | 501K | The Bugs That Lay Eggs All Over Your Body | pending |
| YW2eGaUzq7E | Deep Look | 3:28 | 4.6M | These Face Mites Really Grow on You | pending |
| RQE5NBDmuTY | Benny Goes Wild | 11:11 | 189K | From the Cutest Bug to the One That Causes 600,000 Deaths a Year | pending |
| 4GO3N98rzis | MyWildBackyard | 8:07 | 2.5M | What Happens if a Daddy Long Legs BITES You? | pending (extra, on-topic) |
| 99DNlvZLN0o | MyWildBackyard | 16:17 | 2.0M | EVERY Spider in Your House... | pending (extra) |
| 0HPKKFugajE | TierZoo | 10:11 | 4.4M | How Ants and Bees Broke the Game | pending (3-12 min) |
| lOfUZvOZ400 | TierZoo | 8:15 | 5.4M | The Spider Tier List | pending (3-12 min) |
| 7_e0CA_nhaE | Kurzgesagt | 7:15 | 28.6M | The World War of the Ants - The Army Ant | pending (animated) |
| cqECNYmM23A | Kurzgesagt | 8:12 | 22.3M | The Billion Ant Mega Colony... | pending (animated) |
| PUe80HnKE3E | TED-Ed | 5:12 | 2.0M | The world's most painful insect sting | pending (animated) |
| V6rifwIaio | TED-Ed | 4:43 | 2.2M | Why mosquitoes bite some people more than others | pending (animated) |
| F4sVhVi0Ijo | TED-Ed | 6:24 | 339K | Why is it so hard to get rid of bed bugs? | pending (animated) |
| BtwxvD1JYAk / 7rd6HWqvaHQ | Zack D. Films | 27:22 / 6:08 | 3.1M / 7.8M | long-form compilation / The 10-Second Time Machine | pending |

Pool is ~20, not the 40-60 asked; I stopped expanding it once extraction was blocked. `research/data/70-outliers.csv` did not exist when checked. Failed/blocked: every video above (all fail at the watch-page step).

Shorts: I found no reliable way to list on-topic high-view Shorts with flat search (it mostly returns kids' content and compilations). Channel shorts tabs worked for a few channels (Zack D. Films' top Shorts are 10-16M views, e.g. "What If Humans Had Hummingbird Hearts", "Football Player Finds Snake In His Helmet"; 1 Minute Animals' top is 547K, "Hummingbird Moth"), but outlier score and likes per 1,000 views need the channel median and like counts, which need the same blocked extraction (or vidIQ `vidiq_outliers` with `contentType: short`, 5 credits per call). Retention of Shorts cannot be measured from outside in any case.

### Thumbnail observations (viewed, 10 thumbnails)
All ten pair a title that asks a question or states a stake with **one large, readable subject and 0-4 words of text**:
- BuzzFeed spider: a spider on a sleeping man's open mouth, lightning-burst background. The thumbnail *is* the title's question.
- MyWildBackyard (stings, cellar spider): extreme close-up of the animal, "THIS ONE'S BAD..." (4 words) or a finger holding the spider (zero text); green frame, small logo.
- MyWildBackyard backyard: giant insect, "THIS IS IN YOUR YARD" (domestic-stakes phrase).
- What If: a man in bed with a huge bed bug beside him, "MASSIVE BED BUGS IN YOUR BED" (the human is in the frame for scale and fear).
- Data Ball: insects over a city road, "Insects Size Scaled to 1000 Times".
- TierZoo: pixel-art duel with an "Overpowered?" arrow. Insider Science: surprised face, "WORMS UNDER YOUR SKIN". Deep Look: one clean microscope image, no text. Benny: a 9-up grid of bugs with one flagged "BITES INTO THE SKIN" and a scared human.
Ours for comparison: see `episodes/longform-*/thumb_*.jpg` (not reviewed against these here).
Pattern that is visible without any transcript: the subject is in or on the viewer's own bed/body/yard ("your"), and the unknown is a single question the title asks. Treat as an observation of 10, not a rule.

## Measurements of OUR scripts

Timing: chapter stamps from `episodes/*/description*.txt` (real render) are used where available; estimates are words / 3.08 words per second (calibrated on Kill-or-Keep v2: 842 words = 273 s, which includes pauses).

| | KoK Part 1 (v2) | House Bug Myths | Bugs Ranked | KoK Part 2 |
|---|---|---|---|---|
| runtime | 4:33 | ~4:00 (chapters to 3:37 + ~25 s) | ~6:20 | ~5:07 |
| narration words | 842 | 741 | 1148 | 946 |
| words/min (incl. pauses) | 185 | 185 | 185 | 185 |
| avg sentence (words) | 7.4 | 3.8 | 4.8 | 7.5 |
| question marks | 9 | 27 | 17 | 14 |
| "you/your" per 100 w | 4.3 | 3.1 | 4.5 | 3.9 |
| items | 9 (3 keep, 4 kill, 2 danger) | 8 myths | 12 tiers | 8 (3 keep, 5 kill) |
| seconds per item | 25-33 | 24-44 | 27-34 | 31-38 |
| hook (first line) | claim: "One bug in your house can put you in the hospital." | question: "Do you really swallow spiders in your sleep?" | promise: "Number one on this list is probably in your basement right now." | cold fact: "The moth in your closet never eats." |
| time to first concrete payoff | 0:06 (centipede named), first fact 0:12 | ~0:20 (no evidence, vibrations) | 0:13+ (camel cricket joke at ~0:35) | 0:11 (wolf spider), first fact ~0:15 |
| main open loop and payoff | "the one I promised" brown recluse: opened 0:00, paid 3:49 (88% into video) | "roach with no head": opened 0:07, paid 3:37 (92%) | "number one" = brown recluse: opened 0:00, paid 5:42 (90%); "three land where you'd never guess": twists at 1:16, 2:47, 3:47 | "who ate the hole in your sweater": opened 0:03, paid 4:03 (80%) |
| repeated item shape | name / 4-5 facts / "Verdict: X" x9 | claim / facts / "Myth or true? Lock it in. 3-2-1" x8 | facts / "Lock it in. 3-2-1" / one-line tier x12 | name / facts / "Verdict" x8 |
| transition style | verdict then name next item; only seg9 has a teaser ("the one I promised") | line-end teaser every item ("The next one's named after a body part. Yours.") | "Next: ..." teaser at end of 9 of 12 | "And the next one? Whatever you do, don't squish it." only once |
| humour | one ("free pest control, working the night shift") | few ("I'm taping my mouth shut") | roommate gags x2 (cricket, mouse) | one ("a really good mom") |
| ending / CTA | "Which one is living in your house? Tell me in the comments." | "Which one fooled you? Tell me below." | comments + "watch this next" (best end) | comments only |

### Our Part 1 retention events mapped onto the script
Real chapter times (description-v2.txt): centipede 0:00-0:36, cellar spider 0:36-1:02, jumping spider 1:02-1:29, **carpet beetle (first "Kill") 1:29**, bed bugs 1:56, **cockroach 2:21**, mouse 2:47, black widow 3:20, **brown recluse 3:49**.
- **-45% in the first 60 s.** The 6-second hook promises "hospital" and "the one that protects you." The next 56 s are two *reassuring* "keep" items (centipede, cellar spider). The only hospital bug is paid at 3:49. In the opening minute the viewer is shown the opposite of the promise (safe bugs), with no countdown or stake that says when the dangerous one arrives. Hypothesis, supported by our own curve; not yet checked against any reference.
- **Flat 1:00-2:00** = the survivors; the three keep items use an identical shape (name, 5 facts, "Verdict: keep it") so there is nothing new to leave or to return for. Flat is good news about those viewers; it means the leak is upstream.
- **Second drop ~2:20** coincides with the *cockroach* chapter (2:21), not with the keep-to-kill switch (1:29). Check the Studio curve against the chapter list: if the drop really is at 2:21, the line is "The next three can actually make you sick. The cockroach." (a third kill item in a row, the fourth consecutive same-shape item since 1:29). If it is at 1:29, it is the label change. Either way the fix is the same (change shape; interleave).
- 25% at the end: the hospital bug is last, so people who leave at 2:20 never get the payoff the title/hook sold.

## (c) Provisional first-60-s rewrites
These apply our own diagnosis (promise-versus-delivery mismatch; repeated shape; late payoff) and conventional script craft. They have **not** been validated against reference videos. "[SRC]" marks a new fact that needs a source. Existing facts are kept verbatim where possible.

### Kill-or-Keep Part 1 (v2), first 60 s
Idea: pay a piece of the hospital promise inside the first 20 s, give a count and an order, then use the "keep" bugs as the reassuring beat, with a stake at each seam.
| t | line | note |
|---|---|---|
| 0:00 | One bug in your house can put you in the hospital. | keep; card "HOSPITAL" |
| 0:04 | Another one is guarding you, and you squish it anyway. | keep |
| 0:08 | Nine bugs. Three you never touch, four you kill, and two that can put you in the hospital. The worst one comes last. | count + order (3+4+2 = 9, matches the chapter list); hospital wording is already in our script (seg8) |
| 0:16 | First, the one you probably squished this week. The house centipede. Thirty legs, across your bathroom floor. | name + visual; drop "First, the shocker" |
| 0:23 | It hunts cockroach babies, bed bugs, and silverfish. | payoff, one line |
| 0:28 | Grab it by a leg, and the leg pops off. It's built to break. | keep |
| 0:33 | Can it sting you? Only if you handle it roughly. Rare, and not dangerous. Verdict: keep it. | merge the verdict; cut "Free pest control, night shift" to the next beat |
| 0:41 | Next: the spider hanging in your basement corner. It hunts other spiders, black widows included. | black widow prey: UNSOURCED in this script, the drawn cellar-spider Short says "hunts black widows" [SRC: Burke Museum spider-myths page already listed in that Short] |
| 0:49 | The cellar spider. Poke its web and it blurs. People say its venom is the deadliest on Earth. Spider experts found no evidence it's dangerous to people. | myth-bust as the hook of the item |
| 0:58 | Verdict: keep it. And the next one is on your windowsill, watching you. | stake line into jumping spider |
Seam fixes: after each verdict, end on the next item's *stake*, not its name. Midpoint (~2:00): add a re-hook, "That's the safe half. Now the four I'd squish on sight, and one of them is not the bug you'd guess." Interleave rather than block: keep, keep, **kill (cockroach)**, keep (jumping spider), kill, kill, danger... so the same shape never runs more than two items. Move one danger item (black widow) to about 1:30-2:00 and leave brown recluse last. Add a countdown chip on screen ("9 bugs: 3 keep, 4 kill, 2 danger"). Ending: tell them which video to watch next (Part 2) rather than only "comments."

### House Bug Myths, first 60 s (REVISED 11/10: no quiz opening)
Channel constraint (MASTER_ORDERS "Studio data 11/3"): quiz/true-or-false hooks held 20-28% against 55-63% for house-creature hooks, and "TRUE or FALSE, Myth, Believe, Cartoons, Lied, Did you know" are banned title words. That data is from Shorts, so it is not proof for long-form, but it is our only own evidence, and it points the same way. Applied here: open on a concrete creepy claim about your bed/mouth at night with the animal moving from frame 0, give the reveal inside the same breath, and drop "Myth or true? Lock it in." Every claim below is already in the current script and keeps its sourcing.
| t | line | note |
|---|---|---|
| 0:00 | Eight spiders a year. That's how many you supposedly swallow in your sleep. | frame 0: spider already crawling over a pillow; the number is the claim, stated as what people say, not as fact |
| 0:05 | Mouth open, eight legs walking in. Nope. I'm taping my mouth shut tonight. | existing gag, moved up; viscerally "you" |
| 0:11 | Spider experts say there's no evidence it happens. Zero. And nobody knows where the eight a year number started. | the reveal at 0:11, 6 s after the claim |
| 0:19 | Here's why. To a spider, you're a giant, snoring earthquake. Your heartbeat and your breathing send vibrations, and vibrations mean danger. | |
| 0:28 | Spiders want bugs and quiet corners. Not your face. Could one wander in? Maybe, once in your life. | keep; "once in your life" stays in the script as is (no new fact) |
| 0:35 | Spiders aren't the only story your house tells wrong. The daddy longlegs is three different animals, and only one is a spider. | transition and stake in one; "tells wrong" instead of "lie" |
| 0:44 | The one you see in your basement does have venom, and it eats other spiders. But nobody has ever shown it's deadly to people. | pays the "deadliest venom" claim at once instead of after the harvestman and crane fly detour |
| 0:52 | And the most famous bit of that story? The fangs are too short to bite you. That part's wrong too. | **[SRC]** per the cellar-spider Short, UC Riverside (spiders.ucr.edu/daddy-long-legs-myth) says the "fangs too short" claim is false; script 1.1 currently states it as "the story" only |
Seam fixes: keep the end-of-item teasers (the one thing in all four scripts that works at seams); add a visible "1 of 8" chip; remove the 3-2-1 clips entirely (eight x about 2.5 s of one-word clips, plus the "Lock it in" lines). Midpoint (~2:00): "Four stories down. The next four sound fake, and they're real." (no banned words; also reword the on-screen "True:" chapter labels to plain claims, e.g. "Spiders can fly"). Ending: callback to the headless roach, then a named next video.
Title (banned-word check): the current title "Do You Really Swallow Spiders in Your Sleep? (And 7 More House Bug Myths, Tested)" contains "Myth". Untested alternatives built on the channel's own formula: "You Don't Swallow 8 Spiders a Year. Here's What Spiders Do Near Your Bed (And 7 More House Bug Stories)" is too long (>65 chars); shorter: "Do Spiders Crawl Into Your Mouth at Night? 8 House Bug Stories Checked". The chapter titles in `episodes/longform-house-bug-myths/description.txt` are phrased as quiz questions ("Do earwigs crawl into your ears?"); the searched phrasing is fine for search, but it is not what our Studio data supports for hooks.

### Bugs Ranked, first 60 s (REVISED 11/10: true opening, fewer prompts)
**Claim that the video later walks back:** line 0.0 "Number one on this list is probably in your basement right now." Number one is the brown recluse, and the same script (12.4) says it lives in the south-central U.S. and "outside that, you very likely don't have one." The opening is false for most viewers. Same problem, smaller, in 12.0 "The one hiding in your basement." The rewrite must not claim presence in the viewer's house; it can claim what the script supports (hides in shoes at night, needs a doctor if it bites, lives in one region).
Other claims I audited in the four scripts (not fixed in the JSON, I did not edit scripts):
- Ranked 0.1 "Every bug in your house" vs a mouse in the list; title "Every Bug..." is loose (soften to "Every Creature" or "12 Things").
- Kill-or-Keep v2 0.1 "the bug you squish most" (1.0) is an unsourced superlative; "One bug in your house can put you in the hospital" is true only of the two danger spiders and only in range for the recluse; say "One spider...".
- Cockroach headless: Kill-or-Keep v2 (6.4) and Ranked (9.3) say "weeks without its head"; Myths (7.0) says "a week". Pick one and cite it.
- Part 2 4.0 "Now, the kill pile. But this first one? Don't squish it." with verdict "kill it, but don't crush it": the label contradicts the chapter name "Kill:".
| t | line | note |
|---|---|---|
| 0:00 | Twelve things in your house, ranked from harmless to nightmare. | countable promise; stake in the word nightmare |
| 0:04 | The one at number one hides in shoes and basement corners, and its bite needs a doctor. But it lives in only one part of the country. | true to 12.1-12.4; pays no payoff yet, keeps the open loop |
| 0:12 | And three of these land in a tier you'd never guess. | keep (existing 0.2) |
| 0:15 | We start at the bottom. You flip on the basement light, and something jumps at your face. The camel cricket. | animal moving at frame 0; no "guess along with me" |
| 0:23 | Humped back, giant legs, crazy long antennae. No wings. Can't chirp. Jumps anyway, just to scare you. | keep |
| 0:31 | My roommate screamed louder than the cricket. | joke at 0:31 (existing 1.6, move up) |
| 0:34 | It eats dead bits and rotting plants. Your basement's cleanup crew. Harmless. | verdict: no countdown |
| 0:41 | Next: the fuzzy spider on your windowsill. It's watching you. Right now. | stake teaser |
| 0:47 | No web. It stalks, then pounces, up to forty times its body length. | |
Countdowns ("Lock it in. Three. Two. One." x11, about 2.5 s each plus the "Where does it go?" lines, roughly 40 s of a 6:20 runtime): what holders do with prediction devices is **not known from this research**, because no reference was read. From our own evidence only: guess-style prompts are the format our Studio data penalises on Shorts, and they are the same shape repeated 11 times (checklist rule 5). Recommendation, to be A/B tested rather than assumed: **cut** the spoken 3-2-1 and "Lock it in" from nine of the twelve items, **keep one** guess beat where the video has a twist (house centipede, bed bugs, carpet beetle: the three "twists"), and make that beat a pause-and-reveal ("Where do you put the bed bug? Nightmare? Here's the twist: annoying, not dangerous"), not a countdown. Use the on-screen tier board filling in as the visual reward instead. If you want the data, publish the cut version and compare Studio's retention at the first three item seams against the current version.
Seam fixes: stake goes in the teaser, not "Next: X" with no stake. Midpoint (~3:00): "Half the board is down. So far, nothing here can hurt you. The next six can." (verify the claim before using: bed bugs bite and cockroaches can trigger asthma, so say "nothing here is dangerous", or reword to "The next six are the ones that need a plan."). Keep the "watch this next" ending.

### Kill-or-Keep Part 2, first 60 s
Already the strongest cold open (a concrete fact, a promise, a visual). Keep lines 0.0-0.1. The weakness is 133 words in the first item and three consecutive keep items. Tighten wolf spider to 90 words (cut lines 1.4, 1.5), put a second promise at 0:50 ("two of the next five I'd kill without a second thought"), and interleave one kill item (stink bug) between earwig and camel cricket. Pay "who ate the hole in your sweater" earlier than 4:03 if possible (80% into runtime is a leak risk by our own Part 1 evidence).

## (d) Shorts: our measurements only
No reference Short was measured; retention of any Short cannot be read from outside, so the rules below come from our own data (45% stay / 55% swipe; best loop 148% avg viewed; `research/68-hook-ab-test.md` is running).
- Our 3D explainers: 7-10 lines, 48-54 words, 15-20 s, lines of 3-8 words, alternating P/M, 0.3-0.48 s gap. Loop by cranking back to the opening framing; "Sweet dreams." / "Read it a bedtime story." / "It does. In roaches." are the closers.
- Our drawn Shorts: 7 beats, ~55-60 words, `hook / name / fact / escalate / punch / tease`. The last beat is "Subscribe. Part N ..." which competes with the loop.
- Rewritten openings (hypotheses for the A/B queue):
  1. Bed bugs (3D), currently "Meatball, your bed bit me 3 times!": **"Something bit me three times last night."** (cut "Meatball," as address; the vocative delays the stake by ~0.6 s) then M: "Bed bugs. Apple-seed size. In your mattress seams." Loop closer "Sweet dreams." now returns to a line that begins with the stake.
  2. House centipede (3D), currently "Meatball, there's a 30-legged bug in my bathroom.": **"Thirty legs. In my bathroom. Right now."** then P: "Do I squish it?" M: "Don't! It eats your roaches."
  3. Cellar spider (drawn), currently good: "There's a spider in your basement that hunts black widows." Keep, but replace the final "Subscribe. Part six..." with a loop line that re-enters the hook: "...and it's still down there." so the cut back to line 1 reads as a continuation.

## (e) Checklist (one page, applies to every script)
1. First line is a stake or a question about *the viewer's own house/body*, not a topic. No vocative, no "Welcome," no "Today."
2. Within 15 s: a count and an order ("seven bugs, worst one last") and one visible payoff.
3. The thing promised in the first sentence appears, at least in part, before 1:00 (a tease with a visual counts as a partial payoff, not as nothing).
3b. Every claim in the hook must still be true when the video reaches the item (no "in your basement" for a range-limited animal).
4. Never open with the *reassuring* item when the hook is danger. Put the first scary visual in the first 20 s.
5. No more than two consecutive items with the same shape (name / facts / verdict). Change the shape: a myth, a gag, a countdown, a size comparison, a guess.
6. End every item with the *stake* of the next ("on your windowsill, watching you"), not just its name.
7. One open loop at a time that is longer than 2 minutes; give it a visible chip ("hospital bug: last").
8. Re-hook at the midpoint and every ~45 s: a question, a stake, or a reversal, written down in the script, not improvised.
9. No quiz hooks on the first line or in titles (channel data, Shorts: 20-28% stayed vs 55-63%). No "Myth", "True or false", "Lied", "Did you know", "Believe" in titles or narration. Prediction beats (not 3-2-1 clips) only at a real twist, max 3 per video, never on the first item. Untested on long-form.
10. A joke or character beat every 30-40 s (the roommate lines work; we have 2 per video, aim for 6).
11. Every new fact tagged with a source in the script JSON; a fact with no source is cut, not softened.
12. Last 20 s: callback to the opening promise, then a "watch this next" that names the video, not "tell me in the comments."
13. Shorts: <=55 words, <=8 words per line, stake in the first 2 s, last line connects grammatically to line 1.
14. After posting: compare our Studio curve at 0:30, 1:00 and each chapter boundary with this list and record which rule the leak maps to.
