#!/usr/bin/env python3
"""Assemble a realistic-look Short from real footage (STYLE_DECISION_2026-10-29.md). One JSON spec -> one 1080x1920 mp4.

    python3 realcut.py SPEC.json OUT.mp4

Spec:
{
  "banner": "THINGS LIVING IN YOUR HOUSE #26",          top strip: show name + part (every episode)
  "voice": "narration.wav",                              Meatball's full narration (make it with your TTS first)
  "music": "bed.mp3", "music_db": -20,                   optional
  "bubble": "meatball_shock.png",                        optional round reaction bubble (Meatball's face, PNG)
  "shots": [                                             one per beat, in order; durations should add up to the voice
    {"clip": "footage/cassowary/a.webm", "in": 3.0, "dur": 3.2, "zoom": "in",       zoom: in | out | none (slow push)
     "focus": [0.5, 0.6],                                where to crop/centre (x, y as 0-1 of the source frame)
     "say": "Each foot hides a four-inch dagger claw",   the caption source for this shot
     "big": "4-INCH DAGGER CLAW",                        optional key card (big centred, yellow) for 1.2 s
     "bubble_at": 0.6}                                   optional: show the reaction bubble here (s into the shot)
  ],
  "credits": ["Video by X on Pexels", ...]               printed for the description (not burned in)
}
Captions: the shot's "say" is split into 2-4-word phrases, timed evenly across the shot, big white with a black
outline, lower-middle. Needs: ffmpeg (or imageio-ffmpeg) and Pillow.
"""
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

try:
    import imageio_ffmpeg
    FF = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FF = "ffmpeg"
W, H, FPS = 1080, 1920, 30
FONTS = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
         "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "C:/Windows/Fonts/arialbd.ttf"]


def font(px):
    for f in FONTS:
        if os.path.exists(f):
            return ImageFont.truetype(f, px)
    return ImageFont.load_default()


def text_png(path, text, px, color=(255, 255, 255), y=None, box=False):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font(px)
    lines, cur = [], ""
    for w in text.split():  # wrap to ~90% width
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > W * 0.9 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = t
    lines.append(cur)
    lh = int(px * 1.15)
    y0 = (y if y is not None else H // 2) - lh * len(lines) // 2
    if box:
        d.rectangle([0, y0 - 18, W, y0 + lh * len(lines) + 12], fill=(0, 0, 0, 200))
    for i, ln in enumerate(lines):
        x = (W - d.textlength(ln, font=f)) / 2
        d.text((x, y0 + i * lh), ln, font=f, fill=color, stroke_width=max(4, px // 12), stroke_fill=(0, 0, 0))
    im.save(path)


def phrases(say):
    w = say.split()
    out, k = [], 0
    while k < len(w):
        n = 3 if len(w) - k != 4 else 4  # 2-4 words, never a lone word at the end
        if len(w) - k - n == 1:
            n += 1
        out.append(" ".join(w[k:k + n]))
        k += n
    return out


def bubble_png(src, path, d=330):
    im = Image.open(src).convert("RGBA")
    s = min(im.size)
    im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2)).resize((d, d))
    mask = Image.new("L", (d, d), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, d - 1, d - 1], fill=255)
    out = Image.new("RGBA", (d + 16, d + 16), (0, 0, 0, 0))
    ImageDraw.Draw(out).ellipse([0, 0, d + 15, d + 15], fill=(255, 255, 255, 255))
    out.paste(im, (8, 8), mask)
    out.save(path)


def shot_cmd(s, out, tmp, i):
    """Render one shot to a silent 1080x1920 clip: crop to 9:16 around focus, slow push, captions, key card."""
    fx, fy = s.get("focus", [0.5, 0.5])
    dur = float(s["dur"])
    nf = max(1, int(dur * FPS))
    z = {"in": f"1+0.10*on/{nf}", "out": f"1.10-0.10*on/{nf}", "none": "1"}[s.get("zoom", "in")]
    # cover 9:16, crop around focus, then a smooth slow push with zoompan (one output frame per input frame)
    vf = (f"fps={FPS},scale='max({W}/iw,{H}/ih)*iw':'max({W}/iw,{H}/ih)*ih',"
          f"crop={W}:{H}:x='(iw-ow)*{fx}':y='(ih-oh)*{fy}',"
          f"zoompan=z='{z}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},setsar=1")
    inputs = ["-ss", str(s.get("in", 0)), "-t", f"{dur:.3f}", "-i", s["clip"]]
    overlays, n = [], 1
    caps = phrases(s.get("say", ""))
    for k, c in enumerate(caps):
        p = os.path.join(tmp, f"c{i}_{k}.png")
        text_png(p, c.upper(), 92, y=int(H * 0.72))
        a, b = dur * k / len(caps), dur * (k + 1) / len(caps)
        inputs += ["-i", p]
        overlays.append((n, f"between(t,{a:.2f},{b:.2f})", 0, 0))
        n += 1
    if s.get("big"):
        p = os.path.join(tmp, f"big{i}.png")
        text_png(p, s["big"], 130, color=(255, 214, 0), y=int(H * 0.42))
        inputs += ["-i", p]
        overlays.append((n, f"between(t,0.15,{min(dur, 1.35):.2f})", 0, 0))
        n += 1
    if s.get("bubble_png"):
        inputs += ["-i", s["bubble_png"]]
        a = float(s.get("bubble_at", 0.3))
        overlays.append((n, f"between(t,{a:.2f},{min(dur, a + 1.6):.2f})", W - 380, int(H * 0.16)))
        n += 1
    if s.get("banner_png"):
        inputs += ["-i", s["banner_png"]]
        overlays.append((n, "1", 0, 0))
        n += 1
    graph, last = [f"[0:v]{vf}[v0]"], "v0"
    for j, (idx, en, x, y) in enumerate(overlays):
        graph.append(f"[{last}][{idx}:v]overlay={x}:{y}:enable='{en}'[v{j + 1}]")
        last = f"v{j + 1}"
    return [FF, "-v", "error", "-y", *inputs, "-filter_complex", ";".join(graph), "-map", f"[{last}]",
            "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20", out]


def main(spec_path, out):
    spec = json.load(open(spec_path))
    base = os.path.dirname(os.path.abspath(spec_path))
    rel = lambda p: p if os.path.isabs(p) else os.path.join(base, p)  # noqa: E731
    with tempfile.TemporaryDirectory() as tmp:
        banner = os.path.join(tmp, "banner.png")
        text_png(banner, spec.get("banner", ""), 60, y=150, box=True)
        bub = None
        if spec.get("bubble"):
            bub = os.path.join(tmp, "bubble.png")
            bubble_png(rel(spec["bubble"]), bub)
        parts = []
        for i, s in enumerate(spec["shots"]):
            s = dict(s, clip=rel(s["clip"]), banner_png=banner)
            if bub and "bubble_at" in s:
                s["bubble_png"] = bub
            p = os.path.join(tmp, f"s{i}.mp4")
            subprocess.run(shot_cmd(s, p, tmp, i), check=True)
            parts.append(p)
        lst = os.path.join(tmp, "list.txt")
        open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
        silent = os.path.join(tmp, "silent.mp4")
        subprocess.run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent], check=True)
        cmd = [FF, "-v", "error", "-y", "-i", silent]
        if spec.get("voice"):
            cmd += ["-i", rel(spec["voice"])]
        if spec.get("music"):
            cmd += ["-stream_loop", "-1", "-i", rel(spec["music"])]
        if spec.get("voice") and spec.get("music"):
            cmd += ["-filter_complex", f"[2:a]volume={spec.get('music_db', -20)}dB[m];[1:a][m]amix=inputs=2:duration=first[a]",
                    "-map", "0:v", "-map", "[a]"]
        elif spec.get("voice"):
            cmd += ["-map", "0:v", "-map", "1:a"]
        cmd += ["-c:v", "copy", "-c:a", "aac", "-shortest", out]
        subprocess.run(cmd, check=True)
    total = sum(float(s["dur"]) for s in spec["shots"])
    print(f"wrote {out} ({total:.1f} s, {len(spec['shots'])} shots)")
    if total > 20.5:
        print("WARNING: over 20 s; YouTube Shorts on this channel do best at <= 20 s")
    for c in spec.get("credits", []):
        print("credit:", c)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
