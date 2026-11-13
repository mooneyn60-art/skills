# 104 - Check of the house cat long video's on-screen text (2026-11-13)

A second model (not the builder, not the writer) checked every on-screen string the builder added beyond the cards of `scripts/longform-born-as-house-cat.outline.json`: the strings in `tools/drawn_catlife.py` (deal meter, chips), `tools/drawn_cl_shots.py` (shots table, stamps, clock and counter values) and `tools/drawn_cl_art.py` (every `text(...)` call in the boards and props), plus the pictures that state a fact without words. What the viewer sees was read from `/dev/shm/cat-sheets/lines-contact-1.jpg` to `-5.jpg` (one frame per line). Facts: `research/87`. Script check: `research/88`. Pattern: `research/101`.

"Covered by 88" means the string is word for word a card, or a label named in that line's `vis` note, which research 88 checked. Nothing was edited: the fix below is for the main session.

## Verdict

One fix. No number on screen is wrong, and no bar, dial or count is drawn against its label. The fix: the declaw bill board spells "PHLANGECTOMY". That spelling is in the bill's first two drafts (S5532, S5532A); the version that passed and was signed (S5532B, chapter 107, 2019-07-22) spells it "PHALANGECTOMY". The outline's `vis` note says "spelled as the bill spells them", so the board should match the signed law.

## Sources opened today (2026-11-13)

- https://www.nysenate.gov/legislation/bills/2019/S5532 : curl got 403 (the site's wall, as in research 88). The Senate API wants a key (401). Read through the fetch tool instead, which quoted: S5532 and S5532A "PARTIAL OR COMPLETE PHLANGECTOMY OR TENDONECTOMY"; S5532B "PARTIAL OR COMPLETE PHALANGECTOMY OR TENDONECTOMY"; actions "Jul 22, 2019 | signed chap.107", after S5532B passed both houses on Jun 4, 2019. The page does not name the chaptered version in words; S5532B being the signed text is read from the order of actions (it is the active version, marked "Signed By Governor").
- Nothing else needed a live source: every other string with a number, year or claim is a card or a `vis` label covered by 88.

## The table

| Where | Text as shown | Verdict | Replacement | Source |
|---|---|---|---|---|
| all lines | meter RAW DEAL / SWEET DEAL (faces, ticks, no digits); chip "1 OF 8" ... "8 OF 8", THE OTHER DEAL, THE VERDICT | ok (format labels, opinion meter) | | none needed |
| s1.l0 ... s10.l0 | chapter cards THE DEAL YOU NEVER SIGNED, THE FIVE-WEEK WINDOW, YOUR SENSES, YOUR DINNER, YOUR HOUSE, THE CARRIER, YOUR HUMAN, YOUR OWN BODY, THE OTHER DEAL, THE VERDICT | ok (outline chapter names; "five-week" = weeks 2 to 7, the checked s2.l1) | | |
| s0.l0 | BORN A HOUSE CAT | covered by 88 (card) | | |
| s0.l1 | calendar 7 to 10 | covered by 88 (vis: flips 7, 8, 9, 10) | | |
| s0.l2 | LITTER: ABOUT 4; counter 1 to 4; four kittens | covered by 88 (card, vis) | | |
| s0.l3 | parchment THE DEAL, paw print | covered by 88 (vis) | | |
| s0.l4 | 8 THINGS; eight chips | covered by 88 (card, vis) | | |
| s1.l1, s1.l5 | 979 CATS; ABOUT 9,500 YEARS; map with no names, dots on the Near East and Cyprus | covered by 88 (cards, vis) | | |
| s1.l2 to s1.l4, s10.l16, s10.l17 | village, grain jars, wildcat, mouse (no text) | ok | | |
| s1.l7 | wall clock at 2:50 (no digits) | ok (the joke "a clock already running"; no claim) | | |
| s2.l1 | WEEKS 2 TO 7; week numbers 0 to 12, weeks 2 to 7 lit, red marker at 7 | covered by 88 (card, vis: weeks 2 to 7 lit). Lit band drawn 2 to 7 on the axis | | |
| s2.l2 | heart over the kitten | ok (no text) | | |
| s2.l3 | wall clock at 3:00 | ok (prop beside "three weeks old"; no number written) | | |
| s3.l1 | SWEET GENE: BROKEN; two puzzle pieces, one cracked | covered by 88 | | |
| s3.l6 | 6X IN DIM LIGHT | covered by 88 (card) | | |
| s3.l8 | 48 Hz TO 85 kHz (2 CATS) | covered by 88 (card) | | |
| s4.l1 | OBLIGATE CARNIVORE; mouse label CARBS: / ALMOST NONE | covered by 88 (card, vis) | | |
| s4.l2 | TAURINE: FROM FOOD; factory TAURINE with sign CLOSED | covered by 88 (card, vis). Note only: CLOSED reads as "none" where the say has "very little"; 88 passed the vis as written | | |
| s4.l3, s4.l7 | 1987 (card, desk calendar, can label) | covered by 88 (card, vis) | | |
| s4.l4 | 21 CATS; four cans, one turns to "?" | covered by 88 | | |
| s4.l6 | REVERSIBLE; weak line becomes strong | covered by 88 | | |
| s4.l8 | bowl CASEIN DIET; eye dims | covered by 88 (vis) | | |
| s4.l9 | TAURINE factory, underlined | covered by 88 (vis) | | |
| s4.l10 | MILK: CAN CAUSE DIARRHEA | covered by 88 (card) | | |
| s4.l11 | mop in the corner, nothing happens | covered by 88 (vis) | | |
| s5.l2 | TRUE LILIES + DAYLILIES | covered by 88 (card) | | |
| s5.l4 | CAN KILL IN UNDER 3 DAYS; three calendar pages, no numbers | covered by 88 | | |
| s5.l5 | "?" over the lily; dog with a tummy ache | covered by 88 (vis) | | |
| s5.l6 | THINK IT TOUCHED ONE? CALL A VET NOW; 24-hour clock with a red "18" | covered by 88 (card; vis "a clock runs toward 18"). Trigger and action on the card | | |
| s5.l7 | caution sign "!" by the peace and calla lilies | covered by 88 (vis: smaller caution sign) | | |
| s5.l9, s5.l10, s5.l19 | NEVER HUMAN PAIN PILLS; bottle EXTRA / STRENGTH, closed, no pills | covered by 88 (card, vis) | | |
| s5.l11 | X-ray gut with a red tangle | covered by 88 (vis) | | |
| s5.l13, s5.l14 | 119 CATS; 119 CATS: 109 LIVED; a row of 14 cat icons; tick | covered by 88 (cards). The 14 icons are a row, not labelled as a count | | |
| s5.l15 | tick with "*"; vet bill with coins | covered by 88 (vis) | | |
| s5.l16 | 46% BROKEN LIMBS; cat in a cast | covered by 88 (card) | | |
| s5.l17 | ALWAYS LANDS / ON ITS FEET with "*" | covered by 88 (vis) | | |
| s5.l18 | barrier clicks into the window | covered by 88 (vis) | | |
| s5.l19, s9.l0 | 5 of 8 chips filled, then 8 of 8 | covered by 88 (vis) | | |
| s6.l1 | VET: AT LEAST YEARLY; 10 unlabelled year boxes, one paw stamp each, two in the last three | covered by 88 (card, vis "one paw-stamp per year, then two"). No ages written, so the boxes state no senior age | | |
| s6.l3 | carrier lit as a dungeon | covered by 88 (vis) | | |
| s6.l4 | 1 IN 5; five cats, one faded | covered by 88 | | |
| s6.l5 | clinic door, cone on a hook, green cross | ok (prop, no claim) | | |
| s6.l6 | +30% vs +12%; two dials, needles at 0.85 and 0.40 of the sweep, no digits | covered by 88 (card, vis). Larger needle on the first, right direction | | |
| s6.l7 | LINKED TO LONGER LIFE; two unlabelled bars, second longer | covered by 88 (card, vis); no scale shown | | |
| s6.l9, s6.l10 | clipper and tray; NEW YORK 2019: BANNED; red cross | covered by 88 (card) | | |
| s6.l11 | bill page: ONYCHECTOMY (DECLAWING) / PHLANGECTOMY / TENDONECTOMY, underlined in turn | FIX: the signed version (S5532B) spells it PHALANGECTOMY; PHLANGECTOMY is the spelling of the two earlier drafts only. The spoken line already says "phalangectomy" | ONYCHECTOMY (DECLAWING) / PHALANGECTOMY / TENDONECTOMY | https://www.nysenate.gov/legislation/bills/2019/S5532 (fetch tool; curl 403) |
| s6.l12 | two papers, a tick stamp and a cross stamp | covered by 88 (vis) | | |
| s7.l1, s7.l2 | TAIL END: WORST; petting map red at the tail end, green between eyes and ears | covered by 88 | | |
| s7.l4 | NEGATIVE-BEHAVIOUR SCORE: FAMILIAR 8.5 / STRANGER 5.0; bars FAMILIAR, STRANGER, values 8.5 and 5.0 | covered by 88 (card, vis). Bars drawn at 8.5 x 60 and 5.0 x 60 px: in proportion | | |
| s7.l6 | speech bubbles with scribbles (no letters), one glows | covered by 88 (vis) | | |
| s7.l7 | UNDER 1 IN 10 MEOWED | covered by 88 (card) | | |
| s7.l9 to s7.l11 | A CRY INSIDE THE PURR; waveform; listeners mark rating cards | covered by 88 | | |
| s7.l12 | baby silhouette over the cat | covered by 88 (vis) | | |
| s7.l13 | wall clock at 5:00, night kitchen | covered by 88 (vis: 5 AM) | | |
| s8.l1 | SIGNS CAN BE SUBTLE | covered by 88 (card) | | |
| s8.l2 to s8.l4 | 100 CATS; 92 OF 100: X-RAY SIGNS; three films, "?" | covered by 88 | | |
| s8.l5, s8.l6 | clipboards 11% and 77% / EARLY STAGES COUNTED; 11% OR 77% | covered by 88 (vis, card) | | |
| s8.l8 | 3 IN 4: NO PEEING CHANGE SEEN; four litter boxes | covered by 88 | | |
| s8.l9 | 129 OF 129: DENTAL; dentist's mirror | covered by 88 | | |
| s8.l10 | hairball with a flag (no text) | covered by 88 (vis) | | |
| s8.l11 | TIRED, NOT EATING, RETCHING: VET | covered by 88 (card) | | |
| s9.l2 | 2,444 CATS; a row of 15 cat icons | covered by 88 (card); icons not labelled as a count | | |
| s9.l3, s9.l4 | ROADS: 165 OF 362 DEATHS; 41 OF 67 KITTEN DEATHS; street, no impact | covered by 88 | | |
| s9.l5 | FERAL COLONIES: 3 IN 4 GONE BY 6 MONTHS; four kittens, three fade | covered by 88 | | |
| s9.l6 | 2025: 3 MILLION IN; shelter corridor | covered by 88 (card). Note only: the card drops "about", which the say and the vis keep ("2025: ABOUT 3 MILLION IN"); not a must-change because 88 cleared the card | | |
| s10.l0 to s10.l8 | ledger with minus and plus heads, unlabelled lines, footnote "*" | ok (no words; column fill is opinion) | | |
| s10.l1, s10.l2 | 11.74 YEARS; HALF PASSED 14 (ENGLAND, 2009-12) | covered by 88 (cards) | | |
| s10.l4, s10.l5 | 38 YEARS; party hat, cake with candles (count not a claim) | covered by 88 | | |
| s10.l6 | UNDER 4% A YEAR (AGES 0-8, MINIMUM); flat line chart, no labels | covered by 88 | | |
| s10.l8 | ESSENTIAL (NOT OPTIONAL) | covered by 88 (card) | | |
| s10.l9 to s10.l14 | box on a shelf, four stations, toy mouse, green spot, window barrier | covered by 88 (vis pillars) | | |
| s10.l13 | THE 5 PILLARS | covered by 88 (card) | | |
| s10.l18 | stamp SWEET DEAL (IF...); book THE / MANUAL upside down | covered by 88 (card, vis) | | |
| s10.l19 | end screen WATCH NEXT | ok (format label) | | |

Counts: 72 rows; 63 covered by 88, 8 ok, 1 FIX, 0 CUT, 0 could not verify (one source read only through the fetch tool, below).

## Must change before posting

1. `tools/drawn_cl_art.py`, line 1160, search `"PHLANGECTOMY"`. New: `"PHALANGECTOMY"`. The underline width for that row is `wpx = [760, 470, 460][r]`: make the middle value about 500 so the underline still spans the longer word, then re-render s6.l11 and look at its sheet.
   Also, so nobody restores the old spelling: the `vis` note of s6.l11 in `scripts/longform-born-as-house-cat.outline.json` (line 450) and the built spec (line 6041) say `PHLANGECTOMY`; change it to `PHALANGECTOMY` there too. The `vis` is not seen by viewers.

## Notes for the main session (not must-change)

- s9.l6 card "2025: 3 MILLION IN" lost its "ABOUT" against its own `vis` ("2025: ABOUT 3 MILLION IN"). 88 cleared the card; adding "ABOUT" would keep the hedge on screen.
- s4.l2 sign CLOSED on the taurine factory reads stronger than "very little"; 88 cleared it as drawn.
- `postkit.py lint scripts/longform-born-as-house-cat.json`: 2 fail ("no title", "no description"), 2 warn (no emoji, no tags list). This check changed no file; these are the spec's own, as with the polar bear (research 101). Title, description and tags must go into the spec or the payload before scheduling.

## Could not verify / could not measure

- The New York bill page as raw text: curl got 403 and the Senate API needs a key. The spellings and the signing order were read through the fetch tool's summary only. That S5532B is the chaptered text is inferred from the action order (the page does not say it in words).
- The frames between sheet points: one frame per line was read, not every second of the video.
