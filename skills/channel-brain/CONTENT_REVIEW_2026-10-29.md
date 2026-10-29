# Content review: the new drawn Shorts

A frame-by-frame critique of the newest drawn Shorts, with fixes and a worked rewrite. Written by TARS for Nolan and Meatball Town.

Last Updated: 2026-10-29
Status: delivered
Audience: Nolan, Meatball Town (Showrunner, Studio, Writer)

## Overview
Watched at 1 frame per second, with the scripts read:
- House #22 (scabies), 25.0 s
- House #25 (camel cricket), 35.0 s
- Spider #8 (camel spider), 28.5 s
- Would Meatball Survive? (cassowary), 29.8 s

All rendered 10/28-29. The drawn style is a real step up from stick-figure-on-photos, and the hooks are mostly strong. The problems are in what happens after the first second.

## What's good (keep it)
- **Hooks are strong:**
  - "Soldiers said a giant desert spider would chase you down and scream."
  - "Turn on your basement light, and a hunchbacked cricket jumps out of the dark."
  - "Tiny mites can burrow into your skin and lay eggs there."
- **One drawn world:** no photos, plus a series banner with a part number.
- **The scabies skin cross-section** (0:09-0:12) is the best shot in all four: the viewer sees something they can't see in real life. More of this.

## What's wrong (in order of damage)
### 1. Every video is the same picture
- Meatball on the left, the creature on the right, one background, for 20-30 seconds. Only Meatball's pose and a clip-art prop (ruler, gauge, trophy, magnifier, clock) change.
- Line the four contact sheets up and they look like one video with different colours.
- **It's a drawn slideshow.** It's also the exact pattern YouTube names as unmonetizable: "template-based content with little variation."

### 2. The creature isn't recognisable
- The mite, the camel spider and the camel cricket are all the same template: a round blob body, two eyes, stick legs.
- The camel spider reads as a mushroom with legs.
- **The cassowary is a black crow-shaped blob.** No blue neck, no casque, no red wattle, and **the dagger feet (the whole title) are never shown.** You can't see the bird's feet in any frame.
- If frame 0 doesn't say "WHAT is that?!", people swipe.

### 3. Meatball never does the thing
- The script says "chase you down and scream", but nothing chases anyone.
- The script says "kicks at you with a dagger claw", but nothing kicks; a lightning-bolt overlay plays instead.
- Meatball stands, points and sweats. **The playbook's #1 rule ("Meatball acts inside the scene") isn't happening.**

### 4. Too long
- 25-35 s vs Nolan's measured sweet spot of ≤20 s (Daddy Longlegs 19.8 s is still the best Short).
- Filler beats cause it: "About thirty miles an hour" repeats the km/h line; "It first showed up in a Minnesota greenhouse in 1898" is trivia nobody stays for.

### 5. The script is one template with the animal swapped
- Every script runs hook → escalate → name → fact → fact → punch → tease, written by `drawn_quick.py`.
- **There's no story, no stakes and no twist.**

### 6. Endings deflate
- Camel cricket: "it's completely harmless to you."
- Cassowary: "Would Meatball survive? **Yes.**"
- The best moment of a Survive episode is the verdict, and it's a one-word anticlimax.
- The teases are vague ("More things living in your house, soon"). A tease must name the next creature and the scary thing it does.

### 7. Captions are 1-2 word fragments
- "AND A", "IT CAUSES", "TIME", "FROM HERE", "OF NORTH" mean nothing on their own, and they sit small and low.
- Use 2-4-word phrases that read alone ("4-INCH DAGGER CLAW"), big and centred, with the key word in yellow.

### 8. "Would Meatball Survive?" isn't on the cassowary at all
The banner says "THE BIRD WITH DAGGER FEET" with no show name or number, so the series that brings viewers back isn't branded.

## The fixes
**For every Short:**
1. **18-20 s, 5 beats, one story.** Setup (Meatball does something) → it goes wrong → the scary fact, shown → twist → loop line. Drop every fact that doesn't push the story.
2. **Meatball does the thing the script says.** If the line says "chase", it's a chase. If it says "kick", we see the kick land (on a log, a fence, or Meatball's sandwich).
3. **At least 3 different shots:**
   - wide (where we are)
   - close-up (the scary body part, e.g. the claw, fangs or eggs)
   - impossible view (x-ray, cross-section, shrink-down, slow-mo)

   No two consecutive seconds should look the same.
4. **Recognisable creatures:** draw each one from a reference photo with its 2-3 signature features exaggerated (cassowary: blue neck, casque, giant dagger toe). Retire the shared blob template.
5. **Frame 0 is the scariest image,** not Meatball standing next to a calm creature.
6. **The ending pays off:**
   - Survive verdicts get a twist ("Survive? Yes. Unless you're holding food. Meatball is holding food.")
   - the tease names the next creature: "Next: the spider that lives in your shower drain. Part 26."
7. **Show name and number on every episode,** Survive included.
8. Before queueing, run `tools/vidcheck.py` (length gate) and look at the frame-0 still: would a stranger stop on it?

**For the scripts:**
- Stop generating scripts from one outline template. Each episode needs one **"oh no" moment**: the beat where the viewer thinks "wait, WHAT?". Build the 20 s around it.
- Every Short must end on a line that leads back into its first line (the loop).

## Worked example: House #22 rewritten (about 18 s)
| Time | Picture | Line |
|---|---|---|
| 0-3 s | Extreme close-up: a mite's face and claws digging into skin texture | "Something is digging a tunnel in your skin right now." |
| 3-7 s | Meatball scratching in bed at night; the clock spins 4 weeks ahead | "And you won't feel it for a whole month." |
| 7-11 s | Cross-section: the mite tunnelling, eggs popping out behind it | "It's the scabies mite. It lays eggs as it digs." |
| 11-15 s | Meatball shakes hands with a friend; a mite hops across, with a red flash | "It moves to the next person through a long touch." |
| 15-18 s | Meatball freezes, staring at his hand | "So... who did YOU touch today?" (loops to "Something is digging...") |

Five shots, one story, a twist, and a loop, in 18 s, using facts already in the CDC source.
