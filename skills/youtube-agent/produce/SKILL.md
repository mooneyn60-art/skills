---
name: produce
description: Run the Oh Meatball production pipeline end to end (generate.py -> camify.sh -> meta.py -> thumbnail.py) with exact commands and QA checks. Use when asked to make, render, generate, camify or finish a clip from a prompt.
---

# Produce a clip

Tools and flags: [tools/README.md](../../oh-meatball/tools/README.md). Needs `ffmpeg`, `python3`, Pillow;
`gradio_client` for the Hugging Face backends. Run from `skills/oh-meatball/tools`.

## 1. Generate (free backends first)
```bash
cd skills/oh-meatball/tools
SLUG=raccoon_return   # animal_twist, lowercase
mkdir -p ../new-format/$SLUG
./generate.py "$(cat ../new-format/$SLUG/prompt.txt)" ../new-format/$SLUG/raw.mp4 --seconds 8
```
Backend order: `POLLINATIONS_KEY` -> `HF_TOKEN` -> anonymous HF Space (often out of quota). Force one with
`--backend hf`. If all fail, use vidIQ `vidiq_generate_video` (veo-3.1-lite, 8 s, 9:16, 80 credits) and download.

QA the raw clip before going on:
```bash
ffprobe -v error -show_entries format=duration:stream=width,height -of csv=p=0 ../new-format/$SLUG/raw.mp4
for t in 0.5 4 7.5; do ffmpeg -v error -y -ss $t -i ../new-format/$SLUG/raw.mp4 -frames:v 1 /tmp/$SLUG-$t.jpg; done
```
Look at the 3 frames: real anatomy, no text/watermark, animal moving at 0.5 s, twist visible near the end.
Regenerate once with a fixed prompt if not; never post a broken clip. Trim dead air at the start:
`ffmpeg -ss 1 -i raw.mp4 -c:v libx264 -c:a aac raw_trim.mp4`.

## 2. Camify (the "caught on camera" look)
```bash
./camify.sh ../new-format/$SLUG/raw.mp4 ../new-format/$SLUG/$SLUG.mp4 doorbell_night "FRONT DOOR" "2026-10-14 03:12:44"
./camify.sh raw.mp4 out.mp4 security_day "CAM 02 BACKYARD"
SPEED="41 MPH" ./camify.sh raw.mp4 out.mp4 dashcam
./camify.sh raw.mp4 out.mp4 phone
```
Output: 720x1280, H.264/AAC, -14 LUFS. Pick a believable time (night presets around 2-4 AM). Labels must be generic
(no brand names, no real addresses).

Add the hook text (0-2 s, top third) when the plan has one:
```bash
ffmpeg -y -i $SLUG.mp4 -vf "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSansBold.ttf:text='Wait for the second one…':fontsize=52:fontcolor=white:borderw=5:bordercolor=black:x=(w-tw)/2:y=h*0.16:enable='lt(t,2)'" -c:a copy ${SLUG}_hook.mp4
```

## 3. Metadata
```bash
./meta.py --type doorbell --animal raccoon --hook "returned a package" > ../new-format/$SLUG/meta.json
```
Then replace the title with the top pick from [titles-thumbnail-text](../titles-thumbnail-text/SKILL.md) and check
tags/description with [tags-seo](../tags-seo/SKILL.md).

## 4. Thumbnail (compilations always; Shorts only if the channel has Shorts thumbnails)
```bash
./thumbnail.py ../new-format/$SLUG/$SLUG.mp4 ../new-format/$SLUG/thumb.jpg --time 6 --text "HE CAME BACK" --size 1080x1920
./thumbnail.py comp.mp4 thumb.jpg --time 4 --text "NOT THE POOL GUY" --crop-y 0.6 --circle 700,470,190   # 16:9
```

## Final QA checklist (all must pass)
- [ ] 8-15 s, 9:16, audio present: `ffmpeg -i $SLUG.mp4 -af volumedetect -f null - 2>&1 | grep mean_volume`
- [ ] Frame 1 has motion; overlay visible; twist at 70-85%; ending loops
- [ ] No distress, no brands, no real places ([algorithm.md §6](../../oh-meatball/playbook/algorithm.md))
- [ ] `meta.json` has title <= 70 chars, tags <= 480 chars, "AI-generated" in the description

Output folder per clip: `prompt.txt`, `raw.mp4`, `<slug>.mp4`, `meta.json`, optional `thumb.jpg`.
Next: [publish](../publish/SKILL.md).
