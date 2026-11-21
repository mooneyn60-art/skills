# Animation kit: better Shorts with the tools you already have

A hands-on guide for Meatball Town's Studio and Writer: what to type to get a Short that moves, tells a story, and fits in 20 s.

Last Updated: 2026-10-29
Status: active (use with CONTENT_REVIEW_2026-10-29.md)
Audience: Meatball Town (Writer, Studio, Showrunner)

## Overview
Your renderer (`tools/drawn.py` + `drawn_macros.py`) can already do chases, x-rays, shrink-downs, scale gags, jump scares and camera punch-ins. **You almost never use them.** Across 60 YouTube scripts (10/27-29):

| Macro | Times used |
|---|---|
| solo | 54 |
| fact | 36 |
| xray | 9 |
| chase | 3 |
| tiny | 1 |
| scale | 0 |
| shrink | 0 |

"fact" and "solo" make the slideshow. The action macros make the video. This kit says what to type.

## Rule of thumb
**Every YouTube Short = 5 lines, ≤52 words, ≥2 action lines, ≤1 fact.** Check it before rendering:
```
python3 <channel-brain>/tools/outline_lint.py scripts/drawn-house/outlines/<slug>.yaml
```
It fails the Short if it's too long, has no action, deflates at the end, has a vague tease, or has no show and part number. After rendering: `tools/vidcheck.py episodes/.../yt-<slug>.mp4` (20 s gate).

## Cheat sheet: what each macro looks like on screen
| Macro | What viewers see | Use it when the line says... |
|---|---|---|
| **chase** | the creature runs at Meatball and he flees | runs, chases, attacks, jumps at, charges |
| **xray** | the body goes see-through and shows the inside (set `xray: venom / gut / heart` in creature_cfg) | venom, eggs, inside, stomach, blood |
| **scale** (`how: shrink` or `grow`) | Meatball shrinks next to it, or it grows over him | how big, taller than, longer than |
| **tiny** (+ `scene:`) | Meatball bug-sized inside the creature's world; change `scene` each line to travel | microscopic, in your skin / bed / drain |
| **shrink** | "Meatball Goes Tiny" in the home scene | starting a tiny journey |
| **calm** | relaxed, then a snap zoom and a jump scare on the last words | "the good news is..." then the bad news |
| **count** | creatures pop in one at a time while Meatball counts | "three of them", "9 out of 10 houses" |
| **escalate** | shake, punch-in, red danger pulse | "and it gets worse" |
| hook / punch | frame 0 mid-action / back to the hook framing (loop) | first line / last line |
| fact / solo | static two-shot / creature alone, slow push-in | **at most one of each** |

**Translate verbs into macros.** If a line says something happens (chases, kicks, digs, bites), the picture must show it happening. "Kicks with a dagger claw" over a lightning-bolt overlay is the template failing.

## Five story shapes (copy one, swap the creature)
Each is 5 lines and ~18-20 s. Worked, lint-passing examples are in `examples/`.

1. **"It's in you right now"** (micro creatures: mites, bed bugs, dust mites): hook → **tiny** (shrink into the skin/bed) → escalate → **xray** → punch that turns it on the viewer ("So... who did YOU touch today?"). See `examples/scabies-v2.yaml`.
2. **"Would Meatball Survive?"** (big animals): hook = Meatball walks into the situation with a reason (a sandwich, a dare) → **chase** → **xray** on the weapon → **scale** → verdict with a twist ("Only if he drops the sandwich. He didn't."). See `examples/cassowary-v2.yaml`.
3. **"Turn on the light"** (basement and kitchen bugs): hook (the light clicks on, it's mid-action) → **count** ("9 of 10 houses") → **chase** (it jumps at Meatball) → **scale** → punch ("And it's in yours. Check behind the water heater.").
4. **"The good news is..."**: hook → fact → **calm** (good news, then a jump scare) → **xray** → punch.
5. **"Is this spider venomous?"**: hook (the scary rumour) → **chase** (act the rumour out) → **xray** (`venom`) → **scale** (the real size, Meatball's hand for scale) → verdict with a twist.

## Make the creature recognisable (frame 0 decides everything)
Before building any creature, look at a real photo and write its **2-3 signature features**. Exaggerate those and nothing else. If a stranger can't name it from frame 0, redraw it.

| Creature | Signature features (exaggerate these) | Builder keys |
|---|---|---|
| Cassowary | electric-blue neck, brown helmet (casque), red wattles, a giant dagger toe | bird + the patch below (`neck`, `casque`, `wattle`, `claw`) |
| Camel spider | huge pincer jaws as big as its head, pale sandy hair, 10 "legs" | arachnid `fangs` big, `fuzz`, sandy colour; draw jaws open in the hook |
| Camel cricket | humped back, giant hind legs, antennae longer than its body | insect `body: round`, long `leg_len`, long `ant` |
| Bed bug | flat apple-seed oval, rusty red, swells up red after feeding | insect `body: round`, flat `height`; animate the swelling as the punch |
| Cockroach | glossy brown, long antennae, keeps running headless (the hook) | insect `sheen`, long `ant` |
| Pillbug | grey armour bands, rolls into a ball | centipede/insect with bands; the roll is the action |

**Stop using one blob template for everything.** The mite, camel spider and camel cricket currently look the same: a round body, two eyes and stick legs.

## Camera: 3 shots minimum per Short
Use beat-level `shots[]` (drawn.py) for a close-up on the scary part:
```json
"shots": [{"at": "claw", "cam": [0, 0, 1.0], "to": [340, 120, 2.4], "dur": 0.35}]
```
(the camera eases from a wide shot to 2.4x on the creature's foot as the word "claw" is said). Every Short needs:
- a **wide** (where are we)
- a **close-up** of the weapon or body part
- an **impossible view** (xray / tiny / cross-section)

## Captions
`drawn.py caption_chunks()` splits speech into 1-3-word chunks, which produce fragments like "AND A" and "IT CAUSES". Change it to 2-4-word phrases that read on their own, and yellow the key word. Key numbers and weapons get their own card: "4-INCH DAGGER CLAW", "30 MPH".

## Patch: a cassowary that looks like a cassowary
**Untested.** Insert into `drawn_creatures.bird()`; uses only your existing helpers.
```python
# 1) after `hx, hy, hr = ...` (before the beak): a long blue neck lifts the head
nk = cfg.get("neck", 0)
if nk:
    hy -= nk
    stroke(ctx, [(L * 0.3, by - H * 0.3), (hx, hy + hr * 0.5)], hr * 1.1, color=_c(cfg, "neck_color", "#2f6fd6"))
    if cfg.get("wattle"):
        shape(ctx, lambda c: p_ellipse(c, hx + hr * 0.3, hy + hr * 1.3, hr * 0.18, hr * 0.45),
              _c(cfg, "wattle", "#d8342c"), OUT * 0.5, None)
# 2) after the head shape: the helmet
if cfg.get("casque"):
    shape(ctx, lambda c: p_ellipse(c, hx - hr * 0.1, hy - hr * 1.05, hr * 0.45, hr * 0.6),
          _c(cfg, "casque", "#8a6a3a"), OUT * 0.7, (0.05, 0.2))
# 3) inside the feet loop, after the foot ellipse: the dagger toe (claw_len up for the close-up)
if cfg.get("claw"):
    cl = cfg.get("claw_len", 46)
    shape(ctx, lambda c, k=k: p_poly(c, [(k * 30 + 20, -10), (k * 30 + 20 + cl, -14), (k * 30 + 24, 4)]),
          _c(cfg, "claw_color", "#2b2b2b"), OUT * 0.6, None)
```
Config: `{plan: bird, color: '#1b1b1b', neck: 120, neck_color: '#2f6fd6', wattle: '#d8342c', casque: '#8a6a3a', claw: true, claw_len: 60, leg_len: 200, s: 1.3}`

## Before anything is queued
1. `outline_lint.py`: PASS.
2. Render.
3. `vidcheck.py`: PASS (≤20 s).
4. Look at frame 0 alone. Would a stranger know what it is, and want to know more? If not, fix the hook frame.
5. Watch it once with the sound off. Does the picture tell the story? If it's Meatball standing beside a creature for 3+ seconds, add a move.
