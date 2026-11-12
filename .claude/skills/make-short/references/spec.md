# Spec keys for Shorts and TikTok cuts

The source of truth is the docstring at the top of `skills/oh-meatball/tools/drawn.py` (and `tools/drawn_gags.py` for props and marks). If this page and the docstring differ, the docstring wins. Copy a recent pair instead of starting empty: `scripts/drawn-house/cat-sugar-v6-yt.json` and `scripts/drawn-house/tts-cat-sugar.json`.

## Keys you touch most
| Key | Use |
|---|---|
| `voice`, `rate`, `pitch` | `en-US-AndrewMultilingualNeural`, `+10%`, `+3Hz` (locked) |
| `loop` | `true`: the last line ends in the first room so the video loops |
| `cap_swap` | TikTok only: the caption spelling of each swear used; the voice still says the word |
| `search_top` | TikTok only: the search phrase on screen at the start, 150 px down |
| `title`, `description`, `tags`, `pinned_comment` | YouTube text (see the `post-metadata` skill) |
| `tiktok_caption` | TikTok text; the only published text field |
| `sources`, `_note`, `_f` on beats | where each fact came from, the reason for any accepted WARN, what a check changed |

## Beats
One spoken line each: `{"m": macro, "say": line, "scene": room, "pad": pause, "card": {...}, "gag": {...}}`. Every middle line gets its own `scene`; the first and last line share a room; at least three rooms. Pads are 0.2 to 0.35 s: trim pads before words when a cut runs long.

## Lengths
YouTube 16 to 20 s, never under 15 (MASTER_ORDERS). TikTok search-led cut 20 to 26 s; one-minute cuts are in MASTER_ORDERS, "Posting". Check with `postkit.py lint SPEC --mp4 FILE`.

## Drawing options for dogs, big animals and underwater scenes
From the pet and survival builds of 11/11 and 11/12 (`tools/drawn_gags.py`, `drawn_macros.py`, `drawn_creatures.py`):
- `ears: "floppy"` for dogs.
- `gag: {"wag": 1 | -1}` shows a dog from behind with the tail leaning to its own right or left.
- A line's `mb` can lay Meatball down: `{"moves": [{"at": "45%", "rot": 90, "s": 480, "pos": [175, 1445]}]}`. Use a light scene so he shows.
- `open_zoom` and `open_dx` widen the opening close-up for a long animal. `recut: false` keeps the camera wide on a long line.
- A big animal needs stage `s` about 0.85 with `open_zoom` 1.55. At 0.6 a grizzly looks dog-sized next to Meatball.
- Underwater scenes are `reef`, `deep` and `ocean` only.
- Props for the line-2 gag include `cake` and `donut` (`tools/drawn_gags.py` lists the rest).
