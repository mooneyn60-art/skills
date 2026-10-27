# Niche playbook: what the outliers do

A production spec for Meatball, built from 8 outlier videos watched second by second plus about 90 outlier search results.

Last Updated: 2026-10-27
Status: active (replaces the "real footage" advice in REVIEW_2026-10-27.md)
Audience: Meatball Town (Mayor, Showrunner, Studio, Packager), Nolan

## Overview
Nolan asked TARS to study the outliers in this niche and nearby ones (vidIQ, ~110 credits, 10/27).

**Videos watched second by second:**

| Video | Result | Style |
|---|---|---|
| Nostril Animation, "Animals That Can Regrow Impossible Body Parts" | 4M, 15,901x | 2.5D animated animals |
| @lianna_anima, "Your Pet Doesn't See You as a Human", Part 1 | 3M, 872x | 2D stick figure |
| @brainbitesofficial12, "How Long Would Your Pet Survive in the Wild?" | 810K, 120x | 2D stick figure |
| @explain2d, eye colours | 3.1M, 1,654x | minimalist 2D |
| @everythingprofessor, "Every Type of Sleep Explained", pt 9 | 1.8M, 106x | flat 2D, recurring character |
| @paintanimationofficial, "Every Deadliest Island Explained", Part 6 | 606K, 353x | 2D comic |
| @enoughhhhm, "The Burglar Who Only Moved Furniture" | 2.2M, 618x | 2.5D animated story |
| @craftee_films, Alice in Wonderland syndrome | 3.5M, 14.5x | Roblox / game engine |

**Context:** for pure animal facts, real-footage compilations also break out (@xplaininganimals 12M, 394x; @feral.wit 2.5M, 76x). The format that loses is the hybrid: **a cartoon host pasted over still photos.** That is our format.

## The one big lesson
**Stick figures are not the problem. Stick figures over stock photos are.**

Two of the eight are stick-figure channels, and they beat their medians by 120x and 872x. In both:
- **Zero real photos.** Every animal, room, chart and flashback is drawn in the same line weight and palette as the host.
- **The character is inside the scene doing the thing.** He shrinks next to a giant tarantula, climbs into the box with the rabbit, opens the door as the pets walk out.
- **Animals are drawn with emotions** (a terrified hamster, a scheming cat). A photo can't act; a drawing can.

The vidIQ analysts named our exact format as the contrast case: "a 2D cutout floating on unrelated photographic textures... high visual friction... signals low-effort content."

## The spec (every Short)
### Look
1. **One drawn world.** Meatball, animals, places, diagrams, all in one style: black linework plus flat colour, light shading. Lock a style sheet and reuse it for every asset.
2. **At most one real photo per video**, used as a "proof" cutaway (a famous photo, a document), never as a background.
3. **Meatball acts inside the scene**: holds the thing, gets chased, shrinks, gets x-rayed. He is never just standing beside it pointing.
   - **Never let him stand centre-frame talking for more than 2 s.**
   - He's a stand-in for the viewer, not a lecturer.
4. **Animals have faces and react.** They are characters too (Nostril's axolotls panic when they lose a leg).
5. **Visual tricks the photos can't do:**
   - x-ray / glowing anatomy cutaways
   - scale gags (Meatball shrinks, things grow)
   - red danger flashes
   - 4-panel grids
   - rulers and measurements that make invisible things visible

### Motion and sound
6. **Something changes every 1.5-2.5 s**: a hard cut, a reframe, an asset popping in, a pan. No motion-blur transitions.
7. **Limited animation is enough.** Puppet limbs, blinks, mouth flaps, squash and stretch, sliding layers. None of these channels animates frame by frame.
8. **A sound effect on every action** (pop, whoosh, snap, squeak, thud). Music stays low, under the voice.
9. **Voice:** calm and confident, about 145-160 words per minute. Deadpan works; the visuals carry the joke.

### Words and structure
10. **0:00 is the first line of content. No preamble, no ask.**
    - "Three animals that can regrow their bodies."
    - "Your dog thinks you're its parent."
    - "Imagine you open your front door and your pet just walks out into the wild."
    - "A man snuck into a family's house every night and moved everything one inch to the left."
11. **Frame 0 is the action or a selection grid.**
    - An action example: Meatball at the door as the pets walk out.
    - The grid is a 2x2 or 4-box menu of drawn subjects with a cursor that picks one. It reads as an episode of a bigger series.
12. **Escalate:** cool, then extreme, then absurd (axolotl leg, flatworm head, sea slug that drops its whole body). Count it out loud ("three animals...") so viewers wait for #3.
13. **Make it about the viewer:** "your pet", "your body", "your house". Our own best Short (Daddy Longlegs, a scary thing in your house) fits this.
14. **Captions:** 1-3 words, bold white or yellow with a heavy black outline, centred lower-middle. Or big keyword cards on the key terms.
15. **Endings:**
    - (a) a punchline that loops into the first line, or
    - (b) cut off on the name of the next item, as a series cliffhanger.
    - **No subscribe or like ask in the Short.** None of the eight has one, except explain2d's short end card.

### Series packaging
16. **A permanent top banner plus a part number** ("Every Animal That Can Kill You Explained", "Part 6"). It is the binge and follow engine (Part 6 at 353x, pt 9 at 106x, Part 1 at 872x).
17. **One series name per pillar**, kept for weeks. Start with:
    - "Every Animal That Could Kill Meatball, Explained"
    - "What Your Pet Really Thinks of You"
    - "Animals With Impossible Superpowers"

### Lengths
- **YouTube Shorts:** 40-60 s for an animated explainer (Nostril 40 s). Our 18-24 s rule came from the photo format; re-test it on the new look.
- **TikTok:** 60-90 s for Creator Rewards; the stick-figure winners also run 3.5-6.5 min.
- **Long-form:** the brainbites structure is the template.
  - A countdown with checkpoints (Hour 1, Day 1, Week 1).
  - A mid-point flip ("the list flips: the last three don't just survive, they take over").
  - A recap board at the end.

## How to produce it at our speed
- **Style sheet first.** One Meatball model sheet (5-8 poses and expressions) plus a written style prompt (line weight, palette, shading) used for every generated asset.
- **Scenes and animals:** generate illustrations in that style. Use the image tools already connected, with the style sheet as the reference image, then cut them into layers (background, animal, props).
  - Reject any asset that doesn't match the line weight or palette. Consistency matters more than detail.
- **Animate by layers in the existing renderer:** pans, zooms, pops, blinks, limb poses, squash and stretch. That's all these channels do.
- **Cheapest fast lane:** craftee_films makes 3.5M-view videos in about a day with game-engine scenes. A 3D/engine route is an option later; don't start it now.
- **Fewer, better:** 1 illustrated Short a day beats 3 photo Shorts. Use the freed time on art.

## What to stop
- photo backgrounds
- black-and-white archive grain at frame 0
- Meatball standing beside the subject
- quiz cards, polls or subscribe pills before 0:10
- motion-blur transitions
- 2-word caption fragments that don't read as phrases
- new formats every few days

## The test (one variable, scored)
- **Arms:** 6 illustrated "Every ___ Explained, Part N" Shorts vs the last 6 photo Shorts, same animal pillar.
- **Metrics:** stayed-to-watch % and average % viewed at 48 h, scored with abtest.py.
- **TARS's prediction:** illustrated wins by 10+ points, about 60% (PREDICTIONS mb-illustrated).
- **If it wins:** it becomes the house look, and lengths get re-tested on it before anything else changes.
