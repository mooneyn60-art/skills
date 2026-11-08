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
