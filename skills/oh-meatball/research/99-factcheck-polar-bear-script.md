# 99 - Fact-check of the polar bear long-form script (2026-11-13)

A second model (not the writer) checked `scripts/longform-born-as-polar-bear.outline.json` line by line: every spoken line with a "src", its card and picture note, every joke and Meatball line, the titles, the verdict, the description and the pinned comment. Facts: `research/98-polar-bear-life-factpack.md`. Pattern: `research/88`. Rules: MASTER_ORDERS, "Watch hours", "Direction change" rules 1 to 7, "The YouTube play".

## Verdict

**Cleared for the build, with the 16 wording fixes below applied.** No safety problem was found. Two lines were wrong as worded, not only loose: the daily-swim line (the full paper counts days, not bears) and the coat joke (cubs are born nearly hairless, so "you were born in yours" was a new false fact). Spoken words: 1,818 before, 1,850 after (sum of the words in every "say"). At 3.1 words a second that is about 9 minutes 57 seconds.

Still Nolan's call: title 1 has the word "sucks".

## How the sources were opened (today, 2026-11-13)

- Opened myself with curl as raw text: the USGS Alaska Science Center polar bear page, the USFWS species page, the Hinterland Who's Who profile (Environment Canada, 2002, text by I. Stirling), the Manitoba Polar Bear Alert brochure PDF (file created 2010-12-24), the Parks Canada Prince of Wales Fort bear page, the NOAA Arctic Report Card 2025 headline and sea-ice pages, the USGS publication records 1012949, 70251899, 70029716, 70136255, 70036174, 70028385, 70193125 (abstracts), PubMed abstracts 21639050, 29946080, 27617359, 26214910, 41611752, and two full texts on PMC: Lone 2018 (PMC6018667) and Aars 2026 (PMC12855275).
- COSEWIC 2008 chapter 5 and executive summary (canada.ca): curl got an empty reply from the server twice. Read through the fetch tool instead, which returns a summary with the quoted sentences. The sentences for 0.6 kg, 8 months, 43%, 10 to 12 kg, "no natural predators", "not uncommon" and "excavated in snow" and "Few polar bears live longer than 25 years" were all found as the pack quotes them.

## Every change

| Line | Old | New | Why | Source opened |
|---|---|---|---|---|
| s0.l4 (hook) say | "Her fast can run up to eight months." | "Her fast can go past eight months." | The newer USGS paper says the fast "can exceed 8 months". "Up to eight" reads as a ceiling and COSEWIC's 8 months rests on a 1995 paper nobody opened. The pack's lesson 5 says use the newer paper. | USGS pub 70251899 (Journal of Mammalogy 2024, abstract) |
| s0.l4 card, vis, src | "UP TO 8 MONTHS WITHOUT FOOD", src "PB11 PB12" | "FAST CAN TOP 8 MONTHS (USGS, 2024)", src "PB12 PB11" | Same. | Same |
| s2.l1 say | "The adults were inactive about half the time." | "...about half the time they were out." | A percentage needs what it is a share of: 49.5% is of the 37.5 hours watched outside the den. | USGS pub 70029716 (abstract) |
| s2.l4 card and vis | "(ALASKA, 1995 STUDY)" | "(ALASKA, 1995 PAPER)" | The study ran twelve years; 1995 is the year of the paper. The study years are not in the abstract. | USGS pub 1012949 (abstract) |
| s8.l3 card and vis | "(ALASKA, 1995 STUDY)" | "(ALASKA, 1995 PAPER)" | Same. | Same |
| s4.l2 say | "In one tracking study, three in four of the bears swam every day from May to July." | "In one tracking study of 57 females in Svalbard, more than three in four of the daily records from May to July included a swim." | The abstract says "75% of the polar bears swam daily (May-July)", but the full text says "during May, June, and July, over 75% of the daily records included swimming". It is a share of bear-days, not of bears, and the bears are Svalbard (Barents Sea) females. | PMC6018667 (Lone 2018, full text) |
| s4.l2 card and vis | "3 IN 4 TRACKED BEARS SWAM DAILY, MAY TO JULY"; four bear icons | "MAY TO JULY: OVER 3 IN 4 TRACKED DAYS INCLUDED A SWIM"; four day boxes, three with a swim mark; small print adds SVALBARD | Same. | Same |
| s4.l9 say | "Two months later, researchers caught her again." | "Two months after her first capture, researchers caught her again." | Captured late August, recaptured late October 2008. "Two months later" after the 1,800 km line reads as two months after the swim. | USGS pub 70036174 (Durner 2011, abstract) |
| s5.l6 say | "In 24 years of work in that sea, the authors had not seen other cases." | "In 24 years of research off northern Alaska, the authors had not seen other cases." | The sentence is in the abstract: "During 24 years of research on polar bears in the southern Beaufort Sea region of northern Alaska and 34 years in northwestern Canada, we have not seen other incidents of polar bears stalking, killing, and eating other polar bears." The 24 years are the Alaskan side, not the whole sea. | USGS pub 70028385 (Amstrup 2006, abstract) |
| s6.l2 say | "...says that where the ice melts completely, the whole population..." | "...says that in places like Hudson Bay, where most or all of the pack ice melts, the whole population..." | The page says "In areas such as eastern Baffin Island and Hudson Bay, where most or all of the pack ice melts by mid- to late summer". "Completely" dropped "most or". The writer's own fallback named the place. | hww.ca/?p=7931 |
| s7.l2 say | "Bears that won't stay away are caught and held until the ice forms. Manitoba's brochure lists..." | "Manitoba says bears that won't stay away are caught and held until the ice forms. Its brochure lists..." | Manitoba says they are released once the ice forms. Parks Canada says some are instead "relocated by helicopter". So the line is said as Manitoba's. | Manitoba brochure PDF; Parks Canada page |
| s7.l7 say | "In 144 years." | "In about 145 years." | 1870 to 2014 counted both ends is 145 years; 144 is the subtraction. | Arithmetic on USGS pub 70193125 |
| s7.l8 say | "The authors found underfed adult males were the most likely to be a threat to people. So: rare on the record, and not harmless." | "The authors found nutritionally stressed adult males were the most likely to pose a threat to people. They call reported attacks extremely rare. Rare, and not harmless." | "Underfed" is not the paper's word. The abstract does say "reported attacks have been extremely rare", so the writer's "rare on the record" can now be credited to the authors. No motive is given (D9). | USGS pub 70193125 (Wilder 2017, abstract) |
| s8.l5 say | "For younger adults, 77 to 92." | "For bears aged two to four, and other adults, 77 to 92." | The paper's class is "2-4 year-olds and adults", not younger adults. | PubMed 21639050 (Stirling 2011, abstract) |
| s8.l5 vis | "YOUNGER ADULTS 77 TO 92% A YEAR" | "AGES 2 TO 4 AND ADULTS 77 TO 92% A YEAR" | Same. | Same |
| s9.l5 say (joke) | "You were born in yours." | "You grew yours." | The joke added a false fact: cubs are born "covered with hair so fine that in some early descriptions the cubs were reported to be hairless" (and the script's own s0 says so). The thick coat comes later. | hww.ca/?p=7931 |
| description | "A pregnant bear may fast for up to 8 months and may lose as much as 43%..." | "A mother's fast can exceed 8 months (USGS, 2024), and a pregnant bear may lose as much as 43%..." | Same as s0.l4. | USGS pub 70251899 |
| description | "numbers fell 25 to 50% in the southern Beaufort Sea after 2004 to 2006" | "low survival from 2004 to 2006 cut numbers in the southern Beaufort Sea by 25 to 50%" | The paper says the low survival of 2004 to 2006 led to the drop; "after 2004 to 2006" puts the drop at the wrong time. | PubMed 26214910 (Bromaghin 2015, abstract) |
| description | "the 2026 Svalbard body-condition paper (PMID 41611752)" | "Aars and others 2026 (Svalbard body condition, Scientific Reports)" | The journal and authors are on the PubMed record; the pack had not named them. | PubMed 41611752 |
| _factcheck | "NOT DONE YET..." | One sentence naming this file and the date. | Brief. | |

## Checked and left as written

- Hook (s0.l0 to s0.l6): December or January (USGS page), den "probably" in snow (COSEWIC "generally excavated in snow"), eyes closed (Environment Canada 2002), about 600 grams and "a little over a pound" (0.6 kg is 1.32 lb), the nine-day swim (Durner 2011). The first joke is s1.l3 at about 47 seconds (words before it counted at 3.1 a second). Nothing before 0:25 is a joke.
- s1.l5: "may lose as much as 43 percent", credited to Canada's 2008 status report. COSEWIC cites Atkinson and Ramsay 1995 (Functional Ecology). Crossref has no abstract for it and it sits on JSTOR, so it was not opened. The line keeps its credit and both hedges, so it stands as the report's claim.
- s2.l4 and s2.l5 (cub survival): the abstract has "annual survival" from "a 12-year study in the Alaskan Beaufort Sea", first year 0.651, second year 0.860, of radio-collared females' dependent young. Place, length, paper year and "chance" are all in the line. The study's calendar years are not in the abstract and were not found.
- s3.l5 and s3.l6 (smell): no source for 20 miles (the line says so). Environment Canada 2002: breathing holes "covered by layers of ice and snow 90 cm or more thick and up to a kilometre away". The line keeps "breathing hole" and "up to". 1 km is about 0.62 mile (small print "about 0.6 mile" is right).
- s4.l4 to s4.l8 (swims): 52 GPS-collared adult females, 2004 to 2009, 50 long swims by 20 bears, over 50 km (Pagano 2012). 687 km in 9 days, then 1,800 km more (Durner 2011). 687 km is 426.9 miles, so "more than four hundred miles" is right. The two papers are kept apart, no "record" claim, no cause for the cub.
- s5.l4 and s5.l5 (2004 cases): three confirmed cases between 24 January and 10 April 2004; one a "parturient female killed at her maternal den", the den "apparently discovered ... by scent". No cause is given in the script (the authors' ice hypothesis stays out).
- s6.l3 and s6.l4: 142 bears held near Churchill, 2009 to 2014, water but no food, median 17 days, median loss 1.0 kg a day. 1 kg is 2.2 lb, so "about two pounds" is right.
- s7.l4 (safety line): Manitoba's six points, said clean, credited, trigger "If you meet a polar bear", polar bears only, no other animal and no swear. The phone number is left out (Churchill only). The gag after it (s7.l5) is Meatball's handwriting, not the advice.
- s8.l1 (few live past 25), s8.l3 and s8.l4 (97% a year; 85% of documented adult female deaths shot by local hunters; "the study documented" keeps it in its time).
- s9.l4 (fur and skin): Environment Canada 2002: "Polar bear hair is translucent ... absorbed by the black skin." The line gives no mechanism and the picture draws no light in the hairs.
- s9.l7 (26,000 as of 2023, USFWS), s10.l4 (NOAA 2025: "All of the 19 lowest September minimum ice extents have occurred in the last 19 years", 47-year satellite record), s10.l1 to s10.l3 (southern Beaufort Sea 2004 to 2006; Svalbard, 770 adult bears, 1995 to 2019, condition fell until 2000 then rose; the authors "underline the importance not to extrapolate findings across populations").
- Verdict (s10.l8): said as "an opinion, not a finding", conditional ("if you get through it", "the fine print is your ice"). No forecast anywhere ("No forecast from us"). Every sea-ice or population line names its place and years.
- Titles: none promises only misery. Title 1 ("Sucks") needs Nolan's yes. Title 2 ("Terrible Deal (Until You Grow Up)") and title 3 match a mixed verdict.
- Jokes and Meatball lines: no joke adds a number, a danger or health claim, a bear's feeling or motive, or a safety instruction, except s9.l5 (fixed above). "One star" is Meatball's rating of his own try, not a fact about bears: fine. Mild words only (damn, hell, ass, badass); none inside a credit or the safety line. No insult aimed at the viewer ("Rude-ass guests" is the tourist in the story). Meatball never shares a close frame with a wild bear: his gags are at his own snow hole, his own ice hole, the motel, the truck, and the holding facility door with no bear in the frame; s9.l5 is a split screen.
- Pinned comment: no number beyond Meatball's 1 star, no swear, open question. Fine.

## Lines that stand on an abstract only

s2.l1 (Smith 2007), s2.l4, s2.l5, s8.l3, s8.l4 (Amstrup and Durner 1995), s4.l4 (Pagano 2012), s4.l5 to s4.l9 (Durner 2011), s5.l4 to s5.l6 (Amstrup 2006), s6.l3, s6.l4 (Pilfold 2016), s7.l6 to s7.l8 (Wilder 2017), s8.l5 and the "other places" part of s2.l5 (Stirling 2011), s10.l1 (Bromaghin 2015), s0.l4 (Andersen 2024). In s8.l5 "yearly" is the normal reading of capture-recapture survival, but the abstract does not say "annual": a full-text read would settle it.

Full text read: s2.l6 and s4.l2 (Lone 2018), s10.l2 and s10.l3 (Aars 2026).

## Lines that rest on an agency page citing papers nobody opened

s0.l2, s1.l5, s1.l8, s4.l13, s5.l7, s10.l7 (COSEWIC 2008, read through the fetch tool's summary, not raw); s1.l1, s1.l4, s3.l3, s3.l6, s4.l10, s5.l1, s6.l2, s6.l6, s9.l3, s9.l4 (Environment Canada 2002, no method named); s7.l2 (Manitoba brochure, 2010 file; the cell count may have changed).

## Could not open or measure

- COSEWIC 2008 pages as raw text: the server sent an empty reply to curl twice; read through the fetch tool only.
- Atkinson and Ramsay 1995 (the 8 months and 43% in COSEWIC): no abstract on Crossref, the paper is on JSTOR. Not opened.
- Full texts of Amstrup and Durner 1995, Stirling 2011, Wilder 2017, Durner 2011, Amstrup 2006, Pilfold 2016: not opened (journal pages, not tried past the abstract). So the 1995 study's calendar years are unknown.
- Whether "Keep your own score as we go" at about 23 seconds counts as a "comment ask before 0:25": it asks for no comment, so it was left. The main session can move it after 0:25 if it reads the rule wider.

## For the main session

- `python3 tools/postkit.py lint scripts/longform-born-as-polar-bear.outline.json` gives 1 fail ("no title") before and after this check: the outline has a "titles" list, not the "title" key a spec has, and lint reads no spoken lines from it ("0 mild words"). The brief said keys stay unchanged, so no key was added. Lint should run on the build spec made from this outline.
- The description's first sentence and hashtags are still the writer's guess (no `postkit.py kw` run). That goes through the post-metadata skill before posting.
