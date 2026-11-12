# 68 · Hook A/B test: new opening vs old opening (2026-11-08)

Nolan, 11/8: "Test both styles to see what's really doing better."

## Why
Studio, last 28 days: **45.4% stayed to watch, 54.6% swiped away**. Shorts get tested on ~1K viewers and stop there ("view jail"). 92% of views come from the Shorts feed, so the first second decides the push.

## The two styles
- **NEW (hook):** frame 1 is a 2.0-2.6x punch-in on the creature with no series banner, plus 2 lines of hook text (Anton, white + yellow) from 0.0 s. At ~1.5-2.2 s it eases out to the normal shot. For the 3D silverfish, the dead "Meatball…" + 0.6 s of silence is also cut. Tool: `tools/hook_open.py`.
- **OLD:** wide shot with the "TITLE / Things Living In Your House #" banner, small creature, word captions only.
- **v6 (reference):** the newer drawn renders already open close-up with a big title stamp (mouse, mommy longlegs, lady beetle). Tracked as a third group, not part of the A/B.

## Schedule (YouTube, ET)
| Date | Slot | Short | Group | Hook text |
|---|---|---|---|---|
| 11/9 | 10:00 | House mouse | v6 | n/a |
| 11/9 | 16:00 | Mommy longlegs | v6 | n/a |
| 11/9 | 19:00 | Giant house spider | NEW | 4-INCH SPIDER / ON YOUR FLOOR |
| 11/10 | 16:00 | Lady beetle | v6 | n/a |
| 11/11 | 10:00 | Wolf spider | NEW | IS THIS SPIDER / VENOMOUS? |
| 11/11 | 16:00 | Camel cricket | NEW | IT JUMPS OUT / IN YOUR BASEMENT |
| 11/11 | 19:00 | Termite | OLD | n/a |
| 11/12 | 10:00 | False widow | OLD | n/a |
| 11/12 | 16:00 | Carpenter ant | OLD | n/a |
| 11/12 | 19:00 | Earwig | NEW | DOES IT CRAWL / IN YOUR EAR? |
| 11/13 | 10:00 | Silverfish (3D) | NEW | IT'S EATING / YOUR BOOKS |
| 11/13 | 16:00 | House fly (3D) | OLD | n/a |

Every time slot has both groups in it. The 3D pair is silverfish (NEW) vs house fly (OLD).

## How to read it (48 h after each post, in Studio → each Short → Analytics)
For every Short, note: **Stayed to watch %**, views at 48 h, and average % viewed.

| Short | Group | Stayed % | Views 48h | Avg % viewed |
|---|---|---|---|---|
| (fill in) | | | | |

**Decision rule (Sat 11/15):**
- If NEW averages ≥5 points higher stayed-to-watch than OLD, NEW becomes the default opening for every Short in both pipelines.
- If the gap is under 5 points, the opening isn't the problem, and the next test is length and loop (15-20 s vs 30 s).
- Also compare v6 against both: if v6 beats NEW, keep v6 (it needs no extra step).

Small sample (5 vs 4), so treat a gap under ~5 points as noise.

## Update 11/8 (Nolan: "start the new stuff as soon as you can")
The OLD group was converted too: termite, false widow, carpenter ant and house fly now carry NEW openings. The comparison is now **NEW (all 9 banner-style Shorts, 11/9-11/13) vs the 28-day baseline of 45.4% stayed to watch**, plus v6 (mouse, mommy longlegs, lady beetle) as the second style.
Decision rule: if NEW averages ≥55% stayed (10 points over baseline), it stays the default.

## TikTok 3D test (11/11-11/13)
Six off-niche TikToks (giraffe, kangaroo, booby, archerfish, dung beetle, armadillo) were replaced by 3D house Shorts at 14:30 and 17:00: roach, jumping spider, bed bugs, centipede, silverfish (hook), house fly. Compare their views and avg watch time against the drawn house TikToks at 12:00 the same days.

## Read 11/11 (07:48 ET, before today's 10:00 post)
Sources: yt-dlp flat view counts (rounded to 2 digits above 1K), Windsor.ai (average % viewed ends 11/8), posted.csv. Row data: `data/80-youtube.csv`; full report: `80-scoreboard-1111.md`.

| Short | Group | Posted ET | Age h | Views | Avg % viewed | Stayed % |
|---|---|---|---|---|---|---|
| Giant house spider (4-inch spider) | NEW | 11/9 19:00 | 36.8 | ~1,100 | not available (after Windsor lag) | not available |
| House mouse | v6 | 11/9 10:00 | 45.8 | ~1,100 | not available | not available |
| Mommy longlegs | v6 | 11/9 16:00 | 39.8 | ~1,300 | not available | not available |
| Lady beetle | v6 | 11/10 16:00 | 15.8 | 132 | not available | not available |
| v6 older, 48 h or more (roaches, bed mites, bed bugs, cellar spider) | v6 | 11/7-11/8 | 66-94 | median ~1,550 | median 104 (82.6, 147.0, 87.9, 120.3; partial windows) | not available |

Read: **no NEW-opening Short has reached 48 h**, so there is no verdict. The only NEW Short so far (giant house spider, 36.8 h) sits at about 1,100 views, the same range as v6 Shorts at a similar age (mouse 1,094 at 24 h, mommy longlegs 1,193 at 18 h), so no visible lift or drop yet. n = 1 for NEW. Stayed-to-watch and the 45.4% baseline cannot be pulled by any tool here (Studio only); average % viewed is a different measure and must not be compared with 45.4%. Next read: Thu 11/12 for giant spider, Sat 11/13 for the wolf spider and camel cricket.

## Read 11/12 (07:45 ET, before today's 10:00 post)
Sources: yt-dlp flat view counts (rounded to 2 digits above 1K), Windsor.ai (average % viewed, window 11/7-11/9, last data day 11/9), posted.csv. Row data: `data/89-youtube.csv`; full report: `89-scoreboard-1112.md`.

| Short | Group | Posted ET | Age h | Views | Avg % viewed | Stayed % |
|---|---|---|---|---|---|---|
| Giant house spider | NEW | 11/9 19:00 | 60.8 | 1.2K | 73.5 (partial window) | not available |
| Wolf spider | NEW | 11/11 10:00 | 21.8 | 1.0K | not available | not available |
| Camel cricket | NEW | 11/11 16:00 | 15.8 | 50 | not available | not available |
| Termite | NEW | 11/11 19:00 | 12.8 | 31 | not available | not available |
| House mouse | v6 | 11/9 10:00 | 69.8 | 1.2K | 75.6 (partial window) | not available |
| Mommy longlegs | v6 | 11/9 16:00 | 63.8 | 1.8K | 108.4 | not available |
| Lady beetle | v6 | 11/10 16:00 | 39.8 | 257 | not available | not available |
| v6 older, 48 h or more (6 Shorts incl. mouse and mommy longlegs) | v6 | 11/7-11/9 | 64-118 | median 1,550 | median 99 | not available |

Read: **no verdict.** Only one NEW Short (giant house spider, 1.2K at 60.8 h) is past 48 h, and that is below three. It sits at 0.8x the v6 median of about 1,550, level with the mouse (1.2K) and below mommy longlegs (1.8K); its 73.5% average viewed is under the v6 median of 99 but covers only the first hours of 11/9. The three younger NEW Shorts are split: wolf spider is healthy at 1.0K in 21.8 h, but camel cricket (50) and termite (31) are far under, the same pattern as the lady beetle (v6, 257 at 39.8 h). Two weak Shorts in the same batch point to topic or slot more than opening style, but n is too small to say. Stayed-to-watch is Studio-only and cannot be compared with the 45.4% baseline. Next read: Fri 11/13 (wolf spider passes 48 h Fri 10:00).
