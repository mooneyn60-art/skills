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
