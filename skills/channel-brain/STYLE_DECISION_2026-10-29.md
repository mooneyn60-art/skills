# Style decision: realistic animals

The one look change for Meatball Myths, why, and the rule that stops it from changing again.

Last Updated: 2026-10-29
Status: DECIDED by Nolan's direction; test 6 vs 6, then lock for 8 weeks
Audience: Nolan, Meatball Town (all desks)

## Overview
Nolan (10/29), after seeing the drawn v2 renders: "they don't look like animals, I kinda want the animals to be more realistic... I want to have to change it once." This page is that one change.

## The evidence (yt-dlp, public view counts, 10/29)
| Channel | Style | Shorts checked | Median views | Note |
|---|---|---|---|---|
| Odd Animal Specimens | **real animals**: real specimens and close-up footage, a hand for scale | 40 | **9,250,000** | lowest was 589,000 |
| Nostril Animation | 2.5D cartoon animals | 10 | **3,800** | one 4.2M fluke; the rest 15-25K |
| Casual Geographic | real wildlife footage plus a funny narrator | (long-form) | "How to Not Get Unsubscribed from Life by Animals": 4.5M | |
| Global Data / Zoom Life / Data Ball | realistic 3D animals, scale comparisons | | 7-18M on single videos | |

**Caveat:** Odd Animal Specimens is a big channel, so its raw numbers aren't a forecast for us. The signal is **consistency**: real animals never flop there (40 of 40 over half a million), while the cartoon channel lives or dies on one fluke. Cartoon creatures also failed Nolan's own eye test.

TARS note: on 10/27 TARS first said "real footage", then withdrew it after vidIQ outliers showed drawn winners. What's different now: those drawn winners were the exception on their channels (Nostril's median is 3.8K), the town's drawn creatures don't read as animals, and the channel owner wants real. Decision made; no more flipping.

## The new look
1. **The animal is real and fills the screen.** Use real footage first, licensed:
   - Pexels / Pixabay video (free licence)
   - Wikimedia Commons (CC0 / CC-BY, credited)
   - USFWS / NPS / NOAA (public domain)
   - iNaturalist CC-BY clips
   - Microscope footage for mites and bed bugs from Wikimedia / NIH / CDC (public domain)

   Log every clip in `wm-licenses.json`, as with photos.
2. **Video, not photos.** Never a still with a zoom; a still is allowed only as a 1-second "proof" cutaway.
3. **Scale every time:** a hand, a coin or a ruler beside it. Odd Animal Specimens' whole format is "look how big / weird this real thing is."
4. **Meatball is the voice and the brand, not pasted into the scene.** Keep:
   - his narration voice
   - a small round "reaction bubble" in a corner for 1-2 seconds at the "oh no" moment (like a facecam)
   - the end card / loop line

   **Never a cartoon body standing on top of real footage**: that's the old look that failed.
5. **Actions real footage can't show** (a cassowary charging the viewer, a mite tunnelling):
   - first choice: real behaviour footage of the same action (a cassowary running, a mite under the microscope)
   - second choice: realistic AI video, labelled as altered/synthetic content in YouTube Studio, as policy requires. Needs Higgsfield credits (0 today).

   Keep AI under half of any video.
6. **Everything else stays:**
   - the two shows plus Spider, numbered
   - ≤20 s on YouTube, 5 lines, a hook in the first second
   - an "oh no" moment and a twist ending
   - captions of 2-4 words
   - `outline_lint.py` before making it, `vidcheck.py` before queueing

## Titles (Odd Animal Specimens pattern)
One bizarre, specific claim about one real animal, no question marks needed:
- "This Insect Is Born Pregnant"
- "The World's Largest Cricket"
- "The Fish With The Most Teeth"

For us: "This Mite Is Digging a Tunnel in Your Skin" (Things Living In Your House #26), "This Bird Has a Dagger on Each Foot" (Would You Survive? #10).

## The test, then the lock
- **6 realistic vs the last 6 drawn**, same shows, alternating slots, posted at 12:00 / 16:00 ET.
- **Score at 48 h:** stayed-to-watch and views (`abtest.py`).
- **TARS prediction:** realistic wins stayed-to-watch by 10+ points, about 65%.
- **If realistic wins** (or ties, since Nolan prefers it): it is THE look for **8 weeks**. No style, format or show changes in that window; only hooks, titles and topics may change, one per week.
- **If drawn wins clearly** (10+ points): bring the numbers to Nolan; it's his call.
- **Until the 6 v 6 is read:** no new drawn renders and no more drawn re-renders. Finish what's queued, and put the work into sourcing footage.
