---
name: compilation
description: Build the weekly Oh Meatball compilation (48-60 s vertical Short and, from week 3, an 8-12 min long-form) with compile.sh, a countdown, chapters and the required added-value through-line. Use on Saturdays or when asked for a compilation, a recap, a top-N video or long-form content.
---

# Weekly compilation

Spec: [algorithm.md §2 Compilation spec, §6 Compilation extras](../../oh-meatball/playbook/algorithm.md); titles
[seo-packaging.md §2b](../../oh-meatball/playbook/seo-packaging.md); thumbnails §4; description §5b. Tool:
[compile.sh](../../oh-meatball/tools/compile.sh).

## Added value is required (inauthentic / reused-content rule)
Pure back-to-back clips is the pattern YouTube names as non-monetizable. Every compilation must have:
1. A ranked countdown (`#N … #1`, built into compile.sh) with a theme ("Porch Pirates", "3 AM visitors").
2. A through-line: one caption per clip (rating "Chaos 9/10", or a running joke), added below.
3. **30%+ unseen clips** (new generations, not in this week's Shorts).
4. Chapters (long-form) named after each twist.

## Short version (48-60 s, Saturday 10:00 ET)
Pick 5-6 clips: this week's best by Viewed % (from [analytics-review](../analytics-review/SKILL.md)) + 2 new.
Order: 2nd-best first (hook), weakest in the middle, best last (#1).
```bash
cd skills/oh-meatball/tools
./compile.sh ../new-format/comp_w43_short.mp4 vertical c6.mp4 c5.mp4 c4.mp4 c3.mp4 c2.mp4 c1.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 ../new-format/comp_w43_short.mp4   # must be <= 60
```
compile.sh warns past 60 s; cut a clip rather than speeding up.

## Long-form (8-12 min, from week 3 when you have 25-40 clips)
```bash
./compile.sh ../new-format/comp_w45_long.mp4 horizontal $(cat ../new-format/comp_w45_order.txt)
```
`horizontal` = 1920x1080, each vertical clip centered over a blurred fill. Open with the single best twist (0-15 s hook,
no intro/logo), best first, second-best last (end-screen window), weakest in the middle third.

Per-clip captions (the through-line), burned in after compiling, one drawtext per clip window:
```bash
ffmpeg -y -i comp.mp4 -vf "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSansBold.ttf:text='Chaos rating 9/10':fontsize=44:fontcolor=yellow:borderw=4:x=40:y=h-120:enable='between(t,2,9)'" -c:a copy comp_cap.mp4
```

## Chapters (description, long-form)
Compute starts from clip durations: start(i) = sum of previous durations.
```bash
t=0; i=$#; for c in "$@"; do printf '%d:%02d #%d %s\n' $((t/60)) $((t%60)) $i "$(basename $c .mp4)"; t=$((t+$(ffprobe -v error -show_entries format=duration -of csv=p=0 $c | cut -d. -f1))); i=$((i-1)); done
```
Rules: first chapter `0:00`, at least 3, each >= 10 s (merge short clips into theme blocks), name = the twist
("0:42 Raccoon returns the package").

## Package + publish
- Title: §2b template with a number + "Caught on Camera" + "(AI)", e.g. "25 Animals Caught Stealing on Camera (AI)".
- Thumbnail: `./thumbnail.py comp.mp4 thumb.jpg --time 4 --text "HE CAME BACK" --crop-y 0.6 --circle 700,470,190`
  (concepts in §4b; one hero animal, 2-4 words, one red circle max).
- Description from §5b with the chapters; tags from the "Compilation" set (§3) via [tags-seo](../tags-seo/SKILL.md).
- [publish](../publish/SKILL.md): Short -> `type: "short"`; long-form -> `type: "video"`, `isAiGeneratedContent: true`.
- After it is live, set it as the Related video on every Short of the next week; end screen in the last 5-20 s.
