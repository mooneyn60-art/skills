# Creature art: drop-in, species-accurate animals

Ten redrawn creatures for the drawn renderer, so animals stop being the same round blob with legs. Made by TARS for Nolan (10/30).

Last Updated: 2026-10-30
Status: ready to drop in
Audience: Meatball Town (Studio)

## Overview
`drawn_anatomy.py` draws each animal from its real body plan, in the existing house style (`drawn_kit`: thick ink, flat colour, one cel shade, cartoon eyes). See `preview.png`.

- **The animals:** cassowary, camel cricket, cockroach, black widow, brown recluse, wolf spider, jumping spider, camel spider, scabies mite, house centipede.
- **Why they read:** each has its silhouette and 2-3 signature features. True spiders get a carapace + abdomen and 8 legs with high knees (the "tent"); the black widow gets its red hourglass; the cassowary gets its blue neck, helmet, wattles and dagger claw; the house centipede gets its fringe of 30 long legs; the camel spider gets jaws as big as its head.

## Install (3 steps, nothing else changes)
1. Copy `drawn_anatomy.py` into `skills/oh-meatball/tools/`.
2. In `tools/drawn.py`, next to the other ACTORS imports:
   ```python
   from drawn_anatomy import ANATOMY  # noqa: E402
   ```
   and where the ACTORS dicts are merged, add `ANATOMY`.
3. Use the type name as the actor (e.g. `{"id": "hero", "type": "black_widow", "pos": [700, 1500], "s": 0.9}`), or set the outline's `creature:` to it.

Params:
- `walk` (0..1): legs cycle
- `lunge` (0..1): cassowary kick / camel spider jaws open / cricket jump
- `xray` (>0.5): the cassowary claw glows red for the "dagger" beat
- `mood`, `look`: as before

Check the look anytime: `python3 preview_sheet.py out.png`.

## The rule from now on (Nolan: stop changing everything)
- **This is the creature style. It doesn't change again.**
- A new animal is made by copying the closest builder (spider, insect, mite, bird) and changing only:
  - colour
  - proportions
  - its 2-3 signature features, taken from a real photo
- Before it's used, it goes on the preview sheet next to the others. If a stranger can't name it, fix the signature feature, not the style.
- **One creature per day is plenty. No restyles, no new body plans, no new render pipelines.**
