# Spec keys for `tools/drawn.py` (Shorts and TikTok cuts)

The full list is the docstring at the top of `skills/oh-meatball/tools/drawn.py`. These are the keys the v6 Shorts and the TikTok cuts actually use. Copy a recent pair (`scripts/drawn-house/cat-sugar-v6-yt.json`, `scripts/drawn-house/tts-cat-sugar.json`) rather than starting empty.

## Top level
| Key | Use |
|---|---|
| `voice`, `rate`, `pitch` | `en-US-AndrewMultilingualNeural`, `+10%`, `+3Hz` (locked) |
| `music`, `music_db` | `mystery` on YouTube, `detective` on TikTok |
| `loop` | `true`: the last line ends on the first frame so the video loops |
| `stage` | the animal: `creature`, `scene`, size `s` (a big animal needs about 0.85 with `open_zoom` 1.55), `creature_cfg` |
| `cap_key` | words drawn yellow in the captions |
| `cap_swap` | TikTok only: caption spelling for each swear used (`{"fucking": "f**king", ...}`); the voice still says the word |
| `search_top` | TikTok only: `{"rows": [[text, "#hex", px], ...], "y": 150, "until": 2.5}`, the search phrase on screen at the start; keep it 150 px down so TikTok's top bar does not cover it |
| `series`, `title`, `description`, `tags`, `pinned_comment` | YouTube text (see the `post-metadata` skill) |
| `tiktok_caption`, `tiktok_title` | TikTok text; only the caption is published |
| `sources`, `_note`, `_f` on beats | where each fact came from and what a check changed |

## Beats (one spoken line each)
`{"m": macro, "say": line, "scene": room, "pad": pause after, "card": {...}, "gag": {...}, "mood": ..., "mb": {...}}`
- Macros `m`: `hook` (first line, with `"open": "animal"`), `fact`, `tiny`, `scale`, `escalate`, `chase`, `calm`, `punch` (last line).
- `card`: `{"rows": [[text, "#hex", px, chip?], ...], "y": 470, "at": "45%"}`. `at` is seconds, a share of the line, or a spoken word.
- `gag`: one of `{"prop": "cake" | "donut" | "trophy" | "magnifier" | "ruler" | "rock" | "skull" | "snowflake" | "rocket" | "crown" | "moon" | "bed"}`, `{"mark": "sweat" | "shock" | "hearts" | "anger" | "zzz" | "alarm" | "stars" | "stink" | "dizzy" | "ice"}`, `{"wag": 1 | -1}`, `pile`, `zap`, `heart`, `meter`, `clock`, `thought`; `false` turns the automatic gag off. A new prop is a small function in `tools/drawn_gags.py`.
- Every middle line gets its own `scene`; the first and last line share a room. At least three rooms.
- `pad` is the pause after a line: 0.2 to 0.35 s; trim pads before trimming words when a cut runs long.

## Lengths
YouTube 15 to 20 s. TikTok short cut 20 to 26 s. Check with `postkit.py lint SPEC --mp4 FILE`.
