# oh-meatball production tools

Needs `ffmpeg`/`ffprobe`, `python3` and Pillow (`pip install Pillow`). All videos come out as H.264 + AAC 48 kHz with `+faststart`, normalized to -14 LUFS (two-pass loudnorm, `lib.sh`). Set `CRF=30` for small previews (the default is 20).

| Tool | Usage |
|---|---|
| `camify.sh` | `./camify.sh IN.mp4 OUT.mp4 PRESET [LABEL] [DATETIME]` |
| `compile.sh` | `./compile.sh OUT.mp4 vertical\|horizontal clip1.mp4 clip2.mp4 ...` |
| `frame_thumb.py` | `./frame_thumb.py VIDEO OUT.jpg --time 4 --text "HE CAME BACK" [--circle x,y,r] [--arrow x1,y1,x2,y2] [--size 1280x720\|1080x1920] [--crop-y 0-1]` |
| `meta.py` | `./meta.py --type doorbell\|security\|dashcam\|phone\|compilation --animal raccoon --hook "stole a package" [--n 6] [--seed 1]` |

**camify.sh presets** (output is always 720x1280; the timestamp starts at DATETIME and ticks in real time):
- `doorbell_night`: grayscale IR, fisheye, vignette, heavy noise, date top-left, `● LIVE`, LABEL bottom-right (`"FRONT DOOR"`)
- `security_day`: slightly desaturated with noise, boxed timestamp, LABEL bottom-left (`"CAM 02 BACKYARD"`), blinking REC
- `dashcam`: wide-lens warp, slight blur, timestamp bottom-left, speed bottom-right (`SPEED="41 MPH"` env, default 34 MPH)
- `phone`: light noise and a subtle handheld shake (an animated crop); LABEL is optional

DATETIME is any `date -d` string, e.g. `"2026-10-14 03:12:44"`. When it is omitted, the script picks a random time two days ago (3 AM for night).

**compile.sh** counts down `#N … #1` (yellow, outlined, first 2 s of each clip) with hard cuts in the order you pass the clips. `vertical` is 720x1280 and warns when the result runs past 60 s. `horizontal` is 1920x1080 and places each clip centered over a blurred, zoomed copy of itself. Clips with mixed sample rates, mono audio or no audio are all resampled to 48 kHz stereo. Set `COUNTDOWN=0` to turn the countdown off.

**frame_thumb.py** boosts contrast and saturation and draws 2–4 words of white/yellow text with a thick black stroke (auto-sized). The red circle and arrow use OUTPUT pixel coordinates. When the clip is vertical and the output is 16:9, the frame goes on a blurred fill; pass `--crop-y 0.6` to zoom-crop instead (0 = top, 1 = bottom).

**meta.py** prints JSON with `title` (≤70 chars), `description` (2 lines + 5–7 hashtags) and `tags` (≤480 chars). Write `--hook` as a past-tense phrase. Edit the wording banks in `templates.json`.

```bash
./camify.sh raw.mp4 out/door.mp4 doorbell_night "FRONT DOOR" "2026-10-14 03:12:44"
./compile.sh out/top6.mp4 horizontal a.mp4 b.mp4 c.mp4 d.mp4 e.mp4 f.mp4
./frame_thumb.py out/door.mp4 out/thumb.jpg --time 4 --text "HE CAME BACK" --crop-y 0.6 --circle 700,470,190
./meta.py --type doorbell --animal raccoon --hook "stole a package" > out/meta.json
```

`samples/` holds example outputs from the test clips.

## Drawn videos, fast lane (`drawn_quick.py`)

One short YAML outline makes both cuts of a fully drawn video: the YouTube Short (14-20 s; outline_lint.py before, vidcheck.py after) and the TikTok deep cut (61-75 s, the outline's `tt:` lines are its second act). It writes both specs, checks their spoken length before rendering, renders, ffprobe-checks (both streams, under 50 MB, length in range; nothing is written under the final name until it passes) and writes 2 fps contact sheets.

```bash
python3 tools/drawn_quick.py scripts/drawn-house/outlines/silverfish.yaml            # specs + renders + contact sheets
python3 tools/drawn_quick.py OUTLINE.yaml --no-render                                # lengths only (seconds)
python3 tools/drawn_quick.py --scaffold "booklouse | study | Tiny bugs are eating the glue in your books." --facts facts.txt > outline.yaml
python3 tools/drawn.py scripts/drawn-house/silverfish-tt.json /tmp/x.mp4 --stills 0,3,6   # QA frames before a render
```

Each outline line is `{macro: "the spoken line", ...overrides}`. Macros (`drawn_macros.py`): `hook`, `name`, `fact`, `xray`, `scale`, `count`, `escalate`, `chase`, `calm`, `punch`, `tease`. The tease ("Subscribe. Part N is ...") is added from `next:`. Overrides: `scene`, `scene_p`, `with` (extra creatures or props), `hero: false`, `hero_at`, `act`, `mb_x`, `pose`, `prop`, `mood`.

- **New animal:** add a config to `drawn_species.py` (plans: insect, arachnid, centipede, worm, mite, fish, bird, mammal, reptile; see `drawn_creatures.py`). No drawing code.
- **New place:** pick a habitat from `drawn_habitats.py` and pass `scene_p` (`time: day|dusk|night`, `palette`, `props`, `add`).
- Facts go in `sources:` with the URL and what each source supports; the specs carry them through.
