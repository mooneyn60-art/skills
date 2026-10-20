---
name: titles-thumbnail-text
description: Generate and score 10 title options plus 5 thumbnail-text options for an Oh Meatball clip or compilation (Shorts or long-form). Use when asked for titles, a better title, thumbnail words, or packaging for a video.
---

# Titles + thumbnail text

Source of truth for formulas: [seo-packaging.md §2a (Shorts, 27 templates), §2b (long-form, 16), §4 (thumbnails)](../../oh-meatball/playbook/seo-packaging.md).
Do not copy those tables here; open them and fill them in.

## Steps
1. Get the clip facts: animal, camera, location, twist, hook text, Short or long-form.
2. Write **10 titles**, each from a different template number. Fill with our real scenario.
3. Score each 0-10 with the rubric below; sort descending; flag the top 2.
4. Write **5 thumbnail-text options** (2-4 words) that add to the title, never repeat it.
5. Optional: if vidIQ is connected, run `vidiq_score_title` on the top 3 and report its numbers next to ours.

## Rubric (1 point each, max 10)
1. Animal word in the first 3 words (search + context).
2. Hook inside the first 40 characters (mobile truncation).
3. Length 40-70 chars (Shorts) / 50-70 (long-form).
4. Curiosity gap: the payoff is NOT in the title.
5. Camera type named (doorbell, security cam, dashcam, trail cam).
6. Specific detail (time, number, object): "3:12 AM", "the second shoe".
7. At most 1 emoji, at the end.
8. 0-2 niche title hashtags only (`#doorbellcam`, `#plotwist`); never `#shorts` in the title.
9. No "REAL", "not fake", "BREAKING", brand names (Ring, Nest), real places.
10. Not a near-duplicate of the last 10 titles (inauthentic-content rule).

Rules 9 and 10 are hard gates: a title failing either scores 0.

## Shorts vs long-form
| | Shorts (8-15 s) | Long-form (8-12 min) |
|---|---|---|
| Style | plot-twist, first person, one scene | number + superlative + "Caught on Camera" |
| AI word | optional in title (disclosure is on anyway) | add "(AI)" where natural |
| Thumbnail | not shown in feed; skip unless the channel is verified | essential: one hero animal, cam overlay, 2-4 words, one red circle max |

Proven: "Raccoon doorbell cam" with a plot-twist title = 904 views in 13 h; the "satisfying" title on obvious AI = 2
([research/14](../../oh-meatball/research/14-pivot-satisfying-ai.md)).

## Example output
```
Clip: raccoon, doorbell night, takes a package then returns it, 9 s, Short
 9/10  Raccoon Took the Package… Then Came Back 😳 #plotwist        (#15)
 9/10  3:12 AM. Doorbell Cam. Raccoon. Nope. 😨                     (#7)
 8/10  The Most Polite Package Thief Ever 🦝                        (#21, animal word late: -1)
 8/10  Doorbell Cam Caught Who's Been Taking Packages               (#5)
 ...6 more
Thumbnail text: HE CAME BACK · WAIT FOR IT · 3:12 AM… · RETURNED?? · NOT AGAIN
```
Render the chosen thumbnail with [produce](../produce/SKILL.md) (`thumbnail.py --text`).
