# Second-model check: dog-chocolate (#72), YouTube and TikTok cuts, 2026-11-16

Checker label: check-dog-chocolate. Checked: `scripts/drawn-house/dog-chocolate-v6-yt.json` and `scripts/drawn-house/tts-dog-chocolate.json` against the live source pages, not the pack.

## Verdict

CLEARED, with the changes below. The main fact holds on the FDA page as worded. One real error was fixed: the "9 mg per pound" line never said 9 mg of what. Said bare, a viewer reads it as 9 mg of chocolate, which is about 25 times too small (a 10-pound dog: 90 mg of theobromine is about 0.4 oz of 70-85% dark chocolate by the FDA table, not a 90 mg crumb). The title had the same problem. Theobromine is now named in the spoken line 3 of both cuts, the line 3 card, the title and the TikTok caption. Lint passes on both specs with 0 fail and 0 warn.

## Sources opened today

- FDA, "Leave Chocolate Out of Rover's Celebrations" (Content current as of 04/29/2024), fetched with curl 2026-11-16: https://www.fda.gov/animal-veterinary/animal-health-literacy/leave-chocolate-out-rovers-celebrations
  - "Chocolate is toxic to dogs." (carries the spoken "No.")
  - "Theobromine can cause mild signs in dogs with doses as low as 9 mg per pound of body weight, and severe signs starting around 18 mg per pound of body weight." The dose is of theobromine, per pound of the dog.
  - Table "Approximate amount of theobromine in 1 ounce (mg)": Milk chocolate 57, Semisweet chocolate chips 136, Dark chocolate with 70-85% cacao 227, Unsweetened baking chocolate 364. 227 / 57 = 3.98 (my arithmetic), so "about four times" holds for the 70-85% row, theobromine only, per ounce.
  - "your dog's size, and how sensitive your dog is to theobromine" are listed as factors (carries "small dog: less chocolate gets there").
  - "If your pet is sick or has a veterinary emergency, call your veterinarian. If your veterinarian is unavailable, call your local emergency animal hospital or an animal poison control center."
  - "keep chocolate stored safely out of their reach."
- ASPCA Animal Poison Control, "People Foods to Avoid Feeding Your Pets", fetched with curl 2026-11-16: https://www.aspca.org/pet-care/animal-poison-control/people-foods-avoid-feeding-your-pets
  - "if you suspect your pet has eaten any of the following foods, please note the amount ingested and contact your veterinarian or poison control" (chocolate is on the list). This carries the trigger "Dog ate some? Call your vet". FDA's own trigger is only "if your pet is sick", so without this page the "ate some" half of the line had no source. Added to `sources` and to the description's Sources line.
  - "The darker (higher cacao percentage) the chocolate ... the greater the risk for toxicity." Agrees with the direction of the FDA table.

## Changes

| Where | Old | New | Why |
|---|---|---|---|
| YT line 3, spoken | "The FDA says mild signs can start at nine milligrams per pound of dog." | "FDA says mild signs can start at nine milligrams of theobromine per pound of dog." | FDA's 9 mg is theobromine. Bare "nine milligrams" after the cake gag is heard as 9 mg of chocolate. "The" cut to offset the two added words (the writer's own first trim if over length). |
| TT line 3, spoken | "The FDA says mild signs can start at nine milligrams per pound of dog." | "The FDA says mild signs can start at nine milligrams of theobromine per pound of dog." | Same. The TikTok cut has room (20 to 26 s), so "The" stays. Attribution still said clean, the swear after. |
| YT and TT line 3 card, row 2 | "FDA: MILD SIGNS CAN START" (48 px) | "OF THEOBROMINE: MILD SIGNS CAN START (FDA)" (46 px, measured 866 px wide with Anton, fits 1080) | The card "9 MG PER POUND OF DOG" alone reads as 9 mg of chocolate. |
| YT and TT line 1 card, row 2 | "THE THEOBROMINE OF MILK, PER OUNCE" | "THE THEOBROMINE OF MILK CHOCOLATE, PER OUNCE" (890 px wide, fits) | FDA's row is "Milk chocolate"; milk the drink has no theobromine. Free on the card. The spoken "of milk" stays: a normal ellipsis after "dark chocolate", and the time budget is tight. |
| Title (both specs) | "If Dogs Eat Chocolate: Mild Signs Can Start at 9 mg Per Pound 🍫 (Things Living In Your House #72)" | "If Dogs Eat Chocolate: 9 mg/lb Theobromine Can Cause Mild Signs 🍫 (Things Living In Your House #72)" | Same error as line 3, in the most-read line. New wording is FDA's own order ("Theobromine can cause mild signs"), hedge "can" kept. 100 of 100 units. |
| TikTok caption | "and mild signs can start at 9 mg per pound of the dog, so small dogs need less." | "and mild signs can start at 9 mg of theobromine per pound of the dog, so a small dog needs less chocolate." | Same error; "need less" did not say less of what. |
| Description, Sources line (both specs) | "Sources: U.S. FDA, Animal Health Literacy page on chocolate and dogs (fda.gov)." | adds "; ASPCA Animal Poison Control, people foods to avoid feeding your pets (aspca.org)." | The description's "If your dog ate chocolate ... call your veterinarian" and the card "DOG ATE SOME? CALL YOUR VET" rest on the ASPCA page for the "ate" trigger. |
| `sources` array (both specs) | FDA only | FDA plus the ASPCA quote and link | Same reason. |
| `_note` (both specs) | "not yet checked by a second model." | points to this file and lists the fix | Record only. |

## Lines read and left as they are

- YT/TT line 1 "Can dogs eat chocolate? No. Dark chocolate can have about four times the theobromine of milk." Searched words are the first spoken sentence. "No" = FDA "Chocolate is toxic to dogs." "Can have about" keeps the hedge; 70-85% and per ounce are on the card. TT "fucking" sits on "theobromine", not inside an attribution. OK.
- YT/TT line 2 gag (cake on the top shelf, Noodle stares up, Meatball asks for a ladder). Actions only, no feeling or motive for Noodle, no number, no danger claim. The top shelf agrees with FDA's "out of their reach" and is not said as advice. Joke is on Meatball. "damn" (YT) is the one mild word. OK.
- YT line 3 second half and TT "Meatball counts on his (fucking) fingers": joke on Meatball, no claim. OK.
- YT line 3 card row 3 "DOG ATE SOME? CALL YOUR VET": the only instruction is "call your vet", with its trigger; carried by ASPCA (ate) and FDA (sick). No home treatment. OK.
- TT line 3 card "SMALL DOG: LESS CHOCOLATE GETS THERE": FDA's per-pound dose and "your dog's size". OK.
- TT line 4 "Dog ate some, or seems sick? Call your vet. Meatball's vet knows his fucking voice." Instruction said clean with both triggers; the joke after is on Meatball and adds no claim about dogs. Card "CALL YOUR VET / FDA: IF YOUR PET IS SICK" matches FDA word for word in meaning. OK.
- Last line, both cuts, the corner pill and the pinned comment: a question about the viewer's dog, no claim, no insult at the viewer (TT "worst fucking thing" sits on the thing, not on the viewer). Loops into "Can dogs eat chocolate?". OK.
- `search_top` "CAN DOGS / EAT CHOCOLATE?": the searched phrase. OK.
- Description body: every number and condition matches the FDA page (9 and 18 mg per pound of body weight; 227 and 57 mg per ounce, 70-85% cacao; the unavailable-vet line credited to FDA). "General information, not advice for your dog" kept. OK.
- Tags (9): "can dogs eat chocolate", "can dogs eat dark chocolate", "is chocolate toxic to dogs", "chocolate toxic to dogs", "chocolate poisonous to dogs" are answered by line 1 and the description; "dog ate chocolate" is answered by the call-your-vet line; "can dogs eat chocolate cake" is answered only through "chocolate is toxic to dogs" (the cake is chocolate; the video gives no cake number, and the tag does not promise one). Kept, borderline.
- TikTok title, the rest of the caption, the five hashtags, the share line and the yes-or-no pick: no new claim; the safety line keeps its trigger ("ate chocolate or seems sick"). OK.
- Do-not-say list: no safe amount, no single dose for all dogs (always "per pound"), no "always kills", no "4 times as deadly", no home treatment, no white chocolate. All clear.

## What I could not verify

- Length after the change. edge-tts failed here (TLS to speech.platform.bing.com is refused through this machine's proxy), so neither cut was rendered or timed. The YouTube cut gained one word net ("of theobromine" in, "The" out); the writer estimated 18.5 to 19.8 s before it. If the render runs over 20.05 s, the writer's next trim is "chocolate" in line 2 ("Meatball's cake: top shelf."), which needs no new check (it removes a word and adds no claim). Re-transcribe after the render: "theobromine" is a hard word for the voice and the speech model.
- USDA FoodData Central, the FDA's own source for the table: not opened (the pack's attempt was rate limited; I did not retry). The FDA page is the agency source for the 227 and 57.
- The Merck Veterinary Manual chapter and the Weingart 2021 paper were not re-opened: no line in either cut uses them.
- The hashtags "#dogs #chocolate" (YouTube) and the five TikTok hashtags were not measured against hashtag feeds or TikTok's suggested searches; the standard asks for three topic hashtags on YouTube and this description has two. Wording is true either way; that is a metadata pass, not a fact issue.
- The Things Living In Your House series name on a pet Short follows "The shows"; the title leads with the searched words rather than "Your dog". Not a fact question.
