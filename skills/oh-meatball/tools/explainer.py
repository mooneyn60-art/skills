#!/usr/bin/env python3
"""Explainer builder (Kelevin-style): Meatball reacts on the left; the right panel shows a real
Creative Commons wildlife photo, a bold text card, or an AI illustration. Voiceover + slow zoom, 1080p.

Beats JSON: {"voice": "en-US-AndrewNeural", "beats": [
   {"say": "...", "pose": "point", "photo": "Struthio camelus", "n": 0},   # n-th best iNaturalist photo
   {"say": "...", "pose": "shrug", "text": "NOT HIDING.\\nPARENTING."},
   {"say": "...", "pose": "think", "img": "illustration prompt"} ]}
Usage:  explainer.py beats.json WORKDIR build OUT.mp4        (photos/voice cached in WORKDIR)
        explainer.py beats.json WORKDIR images [--seeds 3]   (only needed for "img" beats)
Photo credits are written to WORKDIR/credits.txt — paste them into the video description.
"""
import argparse
import asyncio
import hashlib
import html
import json
import os
import subprocess
import urllib.parse
import urllib.request

STYLE = (", simple flat vector cartoon, clean thick black outlines, bright flat colors, minimal detail, "
         "no texture, plain solid white background, children's book style")
# SDXL-Turbo in bf16 fits a 15 GB CPU box (~11 s/image at 768x512, 2 steps).
MODEL = os.environ.get("SDXL_TURBO", "/tmp/claude-0/-home-user/f2581a8c-fe42-5876-b5f9-d941a863a7fa/scratchpad/models/sdxlturbo")
W, H, FPS = 1920, 1080, 30
BG = (250, 248, 242)
PANEL = (540, 90, 1340, 900)  # x, y, w, h of the right-hand panel
TEXT_PANEL = (500, 90, 1400, 900)  # text cards have no frame, so they can use more width
SAUCE = (196, 38, 30)
MASCOT = (760, (-60, H - 760 + 40))  # size, top-left position
COVER = False
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
# Only licenses that allow commercial reuse; CC-BY/BY-SA need the credit line.
LICENSES = "cc0,cc-by,cc-by-sa"


def images(beats, work, seeds):
    import torch
    from diffusers import AutoPipelineForText2Image
    torch.set_num_threads(os.cpu_count())
    pipe = AutoPipelineForText2Image.from_pretrained(MODEL, torch_dtype=torch.bfloat16, variant="fp16")
    os.makedirs(f"{work}/img", exist_ok=True)
    for i, b in enumerate(beats):
        if "img" not in b:
            continue
        for s in range(seeds):
            path = f"{work}/img/{i:02d}_s{s}.png"
            if not os.path.exists(path):
                g = torch.Generator().manual_seed(1000 * i + s)
                pipe(b["img"] + STYLE, num_inference_steps=2, guidance_scale=0.0, width=768, height=512,
                     generator=g).images[0].save(path)
                print("img", path, flush=True)


def photo(taxon, n, work, obs=None):
    """A pinned iNaturalist observation's photo when `obs` is given (hand-reviewed picks: search
    rankings shift as votes come in, so an index can silently land on a different, unreviewed photo);
    otherwise the n-th most-faved landscape research-grade photo of the taxon."""
    path = f"{work}/photos/{taxon.replace(' ', '_')}_{f'obs{obs}' if obs else n}.jpg"
    if os.path.exists(path):
        return path
    os.makedirs(f"{work}/photos", exist_ok=True)
    if obs:
        o = json.load(urllib.request.urlopen(f"https://api.inaturalist.org/v1/observations/{obs}", timeout=60))
        p = o["results"][0]["photos"][0]
        if p.get("license_code") not in LICENSES.split(","):
            raise SystemExit(f"observation {obs}: photo license {p.get('license_code')} not reusable")
        urllib.request.urlretrieve(p["url"].replace("square", "large"), path)
        open(path + ".credit", "w").write(f"{taxon}: {html.unescape(p['attribution'])} — iNaturalist photo {p['id']}")
        return path
    q = urllib.parse.urlencode({"taxon_name": taxon, "photo_license": LICENSES, "quality_grade": "research",
                                "per_page": 40, "order_by": "votes", "photos": "true"})
    data = json.load(urllib.request.urlopen(f"https://api.inaturalist.org/v1/observations?{q}", timeout=60))
    picks = []
    for o in data["results"]:
        p = o["photos"][0]
        dim = p.get("original_dimensions") or {}
        if p.get("license_code") in LICENSES.split(",") and dim.get("width", 0) > dim.get("height", 1) * 1.2:
            picks.append(p)
    p = picks[n]
    urllib.request.urlretrieve(p["url"].replace("square", "large"), path)
    open(path + ".credit", "w").write(f"{taxon}: {html.unescape(p['attribution'])} — iNaturalist photo {p['id']}")
    return path


def vo_path(b, work, name, rate):
    # Keyed by content, not position, so inserting or reordering beats never reuses the wrong line.
    key = hashlib.sha1(f"{name}|{rate}|{b['say']}".encode()).hexdigest()[:16]
    return f"{work}/vo/{key}.mp3"


def voice(beats, work, name, rate="+8%"):
    from facts import speak  # reuse the proxy-aware, retrying TTS
    os.makedirs(f"{work}/vo", exist_ok=True)
    for b in beats:
        mp3 = vo_path(b, work, name, rate)
        if not os.path.exists(mp3) or not os.path.exists(mp3 + ".words.json"):
            json.dump(asyncio.run(speak(b["say"], name, mp3, rate)), open(mp3 + ".words.json", "w"))


def vertical():
    """Shorts layout: panel on top, Meatball bottom-left, word captions in between."""
    global W, H, PANEL, TEXT_PANEL, MASCOT, COVER
    W, H = 1080, 1920
    PANEL = TEXT_PANEL = (40, 140, 1000, 1000)
    MASCOT = (860, (-120, H - 860 + 60))
    COVER = True


def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 path], capture_output=True, text=True, check=True).stdout)


def _rounded(im, r=36):
    from PIL import Image, ImageDraw
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.width, im.height], r, fill=255)
    out = Image.new("RGBA", im.size)
    out.paste(im, (0, 0), mask)
    return out


def _panel_image(path):
    from PIL import Image, ImageFilter
    px, py, pw, ph = PANEL
    im = Image.open(path).convert("RGB")
    s = (max if COVER else min)(pw / im.width, ph / im.height)
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    if COVER:  # fill the whole panel; landscape photos would otherwise float small in a tall frame
        l, t = (im.width - pw) // 2, (im.height - ph) // 2
        im = im.crop((l, t, l + pw, t + ph))
    im = _rounded(im)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x, y = px + (pw - im.width) // 2, py + (ph - im.height) // 2
    shadow = Image.new("RGBA", im.size, (0, 0, 0, 90))
    layer.paste(shadow, (x + 14, y + 18), im.split()[3])
    layer = layer.filter(ImageFilter.GaussianBlur(14))
    layer.alpha_composite(im, (x, y))
    return layer


def _panel_text(text, top_pad=0, punch=True):
    from PIL import Image, ImageDraw, ImageFont
    px, py, pw, ph = TEXT_PANEL
    py, ph = py + top_pad, ph - 2 * top_pad
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    lines = text.split("\n")
    size = 150
    while size > 80:  # below ~80 px a card stops reading on a phone; split long lines in the script instead
        font = ImageFont.truetype(BOLD, size)
        widths = [d.textlength(line, font=font) for line in lines]
        if max(widths) < pw - 80 and size * 1.15 * len(lines) < ph - 80:
            break
        size -= 6
    total = size * 1.15 * len(lines)
    y = py + (ph - total) / 2
    for k, (line, w) in enumerate(zip(lines, widths)):
        # Punchline (last line) in the mascot's sauce red.
        fill = SAUCE if punch and k == len(lines) - 1 and len(lines) > 1 else (17, 17, 17)
        d.text((px + (pw - w) / 2, y), line, font=font, fill=fill)
        y += size * 1.15
    return layer


def _panel_quiz(statement, count=None):
    """Interactive beat: TRUE OR FALSE? header, the claim, and an optional countdown number."""
    from PIL import Image, ImageDraw, ImageFont
    px, py, pw, ph = TEXT_PANEL
    layer = _panel_text(statement, top_pad=int(ph * 0.15), punch=False)
    d = ImageDraw.Draw(layer)
    head = ImageFont.truetype(BOLD, int(min(pw / 9, 110)))
    label = "TRUE OR FALSE?"
    d.text((px + (pw - d.textlength(label, font=head)) / 2, py), label, font=head, fill=SAUCE)
    if count:
        r = int(min(pw, ph) * 0.13)
        cx, cy = px + pw // 2, py + ph - r
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SAUCE)
        f = ImageFont.truetype(BOLD, int(r * 1.3))
        s = str(count)
        d.text((cx - d.textlength(s, font=f) / 2, cy - r * 0.78), s, font=f, fill=(255, 255, 255))
    return layer


def compose(beat, i, work, picks, out, count=None):
    from PIL import Image, ImageFilter
    from mascot import draw
    canvas = Image.new("RGBA", (W, H), BG + (255,))
    if "photo" in beat:
        canvas.alpha_composite(_panel_image(photo(beat["photo"], beat.get("n", 0), work, beat.get("obs"))))
    elif "quiz" in beat:
        canvas.alpha_composite(_panel_quiz(beat["quiz"], count))
    elif "text" in beat:
        canvas.alpha_composite(_panel_text(beat["text"]))
    elif "img" in beat:
        canvas.alpha_composite(_panel_image(f"{work}/img/{i:02d}_s{picks.get(str(i), 0)}.png"))
    size, pos = MASCOT
    m = draw(beat.get("pose", "point"), size)
    halo = m.split()[3].filter(ImageFilter.MaxFilter(15))  # white outline keeps him readable over panels
    canvas.paste((255, 255, 255, 255), pos, halo)
    canvas.alpha_composite(m, pos)
    canvas.convert("RGB").save(out)


def countdown(b, i, work, picks):
    """3-2-1 after a quiz claim: one second per number with a tick, so viewers lock in a guess."""
    segs = []
    for c in (3, 2, 1):
        img, seg = f"{work}/frame{i:02d}_c{c}.png", f"{work}/seg{i:02d}_c{c}.mp4"
        compose(b, i, work, picks, img, count=c)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", img,
                        "-f", "lavfi", "-i", "sine=frequency=1100:duration=0.07",
                        "-vf", f"scale={W}:{H},format=yuv420p", "-af", "apad", "-t", "1",
                        "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-r", str(FPS),
                        "-c:a", "aac", "-ar", "48000", "-ac", "2", seg], check=True)
        segs.append(seg)
    return segs


def build(beats, work, out, picks, name, rate="+8%"):
    voice(beats, work, name, rate)
    segs = []
    for i, b in enumerate(beats):
        img, mp3, seg = f"{work}/frame{i:02d}.png", vo_path(b, work, name, rate), f"{work}/seg{i:02d}.mp4"
        compose(b, i, work, picks, img)
        dur = duration(mp3) + 0.35
        frames = int(dur * FPS)
        # Slow Ken Burns: alternate zoom-in / zoom-out so consecutive beats don't feel identical.
        z = "min(1.0+0.0008*on,1.08)" if i % 2 == 0 else "max(1.08-0.0008*on,1.0)"
        vf = (f"scale={W*2}:{H*2}:flags=lanczos,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
              f":d={frames}:s={W}x{H}:fps={FPS},format=yuv420p")
        if H > W:  # Shorts are mostly watched muted: burn word-by-word captions on photo beats
            if "text" not in b and "quiz" not in b:  # a quiz caption would read "FALSE" before the countdown
                from facts import captions
                ass = f"{work}/cap{i:02d}.ass"
                captions(json.load(open(mp3 + ".words.json")), ass)
                # facts.py centers captions mid-screen; drop them into the gap between panel and Meatball
                txt = open(ass).read().replace("-1,1,7,3,5,0", "-1,1,7,3,2,700")
                open(ass, "w").write(txt)
                vf += f",ass={ass}"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-i", img, "-i", mp3,
                        "-vf", vf, "-t", f"{dur:.2f}", "-c:v", "libx264", "-crf", "20", "-preset", "medium",
                        "-c:a", "aac", "-ar", "48000", "-ac", "2", "-af", "apad", seg], check=True)
        segs.append(seg)
        if "quiz" in b:
            segs += countdown(b, i, work, picks)
    # Only the photos actually used, so the description never credits a swapped-out image.
    used = sorted({photo(b["photo"], b.get("n", 0), work, b.get("obs")) for b in beats if "photo" in b})
    open(f"{work}/credits.txt", "w").write("".join(open(u + ".credit").read() + "\n" for u in used))
    lst = f"{work}/list.txt"
    open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-af", "loudnorm=I=-14:TP=-1.5", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", out], check=True)
    print(f"ok {out} {duration(out):.1f}s")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("beats")
    ap.add_argument("work")
    ap.add_argument("stage", choices=["images", "build"])
    ap.add_argument("out", nargs="?")
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--pick")
    ap.add_argument("--vertical", action="store_true", help="1080x1920 Shorts layout with captions")
    a = ap.parse_args()
    spec = json.load(open(a.beats))
    if a.vertical:
        vertical()
    if a.stage == "images":
        images(spec["beats"], a.work, a.seeds)
    else:
        picks = json.load(open(a.pick)) if a.pick else {}
        build(spec["beats"], a.work, a.out, picks, spec.get("voice", "en-US-AndrewNeural"), spec.get("rate", "+8%"))


if __name__ == "__main__":
    main()
