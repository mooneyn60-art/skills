#!/usr/bin/env python3
"""Explainer builder (Kelevin-style): Meatball reacts on the left; the right panel shows a real
Creative Commons wildlife photo, a bold text card, or an AI illustration. Voiceover + slow zoom, 1080p.

Beats JSON: {"voice": "en-US-AndrewNeural", "beats": [
   {"say": "...", "pose": "point", "photo": "Struthio camelus", "n": 0},   # n-th best iNaturalist photo
   {"say": "...", "pose": "shrug", "text": "NOT HIDING.\\nPARENTING."},
   {"say": "...", "pose": "think", "img": "illustration prompt"} ]}
Optional comedy fields (research/39, classic style): "prop": "fork" stands a still prop beside Meatball,
"aside": "(small comfort)" adds a small grey footnote under the panel, "hold": 0.6 adds silence after the
line (a deadpan beat), "sting": "tink" plays the show's one signature sound at the start of the beat.
Spec "pitch" (e.g. "-2Hz") shifts the voice; omitted, voices and cached audio are unchanged.
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
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request

STYLE = (", simple flat vector cartoon, clean thick black outlines, bright flat colors, minimal detail, "
         "no texture, plain solid white background, simple cartoon style")
# SDXL-Turbo in bf16 fits a 15 GB CPU box (~11 s/image at 768x512, 2 steps).
MODEL = os.environ.get("SDXL_TURBO", "/tmp/claude-0/-home-user/f2581a8c-fe42-5876-b5f9-d941a863a7fa/scratchpad/models/sdxlturbo")
W, H, FPS = 1920, 1080, 30
MUSIC = None  # background bed, set from the spec's "music" (path relative to brand/)
BG = (250, 248, 242)
PANEL = (700, 90, 1180, 900)  # x, y, w, h of the right-hand panel
TEXT_PANEL = (680, 90, 1200, 900)  # text cards have no frame, so they can use more width
SAUCE = (196, 38, 30)
MASCOT = (1150, (-275, -62))  # size, top-left position: the star, head high and big beside the panel
BLEED_MASCOT = (480, (30, H - 480 - 10))  # "bleed" beats: Meatball over a full-frame photo
COVER = False
ANIMATE = False  # set in main(): Meatball is overlaid as animated frames (mascot.animate) instead of a still
PUNCH = False  # "style": "punch" in the spec: full-bleed photos, outlined text, stamps, SFX, progress bar
COUNT_S = 1.0  # seconds per countdown number
PITCH = "+0Hz"  # spec "pitch"; the default keeps every existing voice-over cache key
YELLOW = (255, 214, 10)
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
ASIDE_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-BoldOblique.ttf"  # typed footnote look
# Only licenses that allow commercial reuse; CC-BY/BY-SA need the credit line.
LICENSES = "cc0,cc-by"  # no share-alike: thumbnails cut out and remix photos (research/30)


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


def photo(taxon, n, work, obs=None, size="large"):
    """size="original" fetches the full-resolution file (full-bleed Shorts crop deep into it).
    A pinned iNaturalist observation's photo when `obs` is given (hand-reviewed picks: search
    rankings shift as votes come in, so an index can silently land on a different, unreviewed photo);
    otherwise the n-th most-faved landscape research-grade photo of the taxon."""
    path = f"{work}/photos/{taxon.replace(' ', '_')}_{f'obs{str(obs).replace(":", "_")}' if obs else n}.jpg"
    if size != "large":
        path = path[:-4] + f"_{size}.jpg"
    if os.path.exists(path):
        return path
    os.makedirs(f"{work}/photos", exist_ok=True)
    if isinstance(obs, str) and obs.startswith("met:"):
        # The Met Open Access object: public domain (CC0) art and artifacts for history beats.
        api = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obs[4:]}"
        o = json.load(urllib.request.urlopen(urllib.request.Request(api, headers={"User-Agent": "MeatballMyths/1.0"}), timeout=60))
        if not o.get("isPublicDomain"):
            raise SystemExit(f"{obs}: not public domain")
        req = urllib.request.Request(o["primaryImage"] or o["primaryImageSmall"], headers={"User-Agent": "MeatballMyths/1.0"})
        open(path, "wb").write(urllib.request.urlopen(req, timeout=120).read())
        open(path + ".credit", "w").write(f"{taxon}: \"{o['title']}\" ({o.get('objectDate') or 'n.d.'}), The Metropolitan Museum of Art (public domain), via metmuseum.org")
        return path
    if isinstance(obs, str) and obs.startswith("wm:"):
        return wm_photo(obs[3:], taxon, path)
    if isinstance(obs, str) and obs.startswith("ov:"):
        # Openverse id (CC/public-domain art, fossils, museum pieces) for history beats with no live animal.
        o = json.load(urllib.request.urlopen(urllib.request.Request(
            f"https://api.openverse.org/v1/images/{obs[3:]}/", headers={"User-Agent": "MeatballMyths/1.0"}), timeout=60))
        if o["license"] not in ("cc0", "pdm", "by", "by-sa"):
            raise SystemExit(f"{obs}: license {o['license']} not reusable")
        url = o["url"].split("?")[0]
        if "upload.wikimedia.org/wikipedia/commons/" in url and "/thumb/" not in url:
            # Commons refuses originals to our shared egress (429): take a standard-width thumbnail
            head, name = url.rsplit("/", 1)
            w = 1920 if (o.get("width") or 0) >= 1600 else 1280
            data = _wm_get(head.replace("/commons/", "/commons/thumb/") + f"/{name}/{w}px-{name}", as_json=False)
        else:
            data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "MeatballMyths/1.0"}),
                                          timeout=60).read()
        open(path, "wb").write(data)
        lic = "public domain" if o["license"] in ("cc0", "pdm") else f"CC {o['license'].upper()} {o['license_version']}"
        open(path + ".credit", "w").write(f"{taxon}: \"{o['title']}\" by {o.get('creator') or 'unknown'} ({lic}), via {o['source']}")
        return path
    if obs:
        o = json.load(urllib.request.urlopen(f"https://api.inaturalist.org/v1/observations/{obs}", timeout=60))
        p = o["results"][0]["photos"][0]
        # Photos already pinned in scripts may be CC BY-SA (credited); new picks are CC0/CC BY only.
        if p.get("license_code") not in LICENSES.split(",") + ["cc-by-sa"]:
            raise SystemExit(f"observation {obs}: photo license {p.get('license_code')} not reusable")
        urllib.request.urlretrieve(p["url"].replace("square", size), path)
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
    urllib.request.urlretrieve(p["url"].replace("square", size), path)
    open(path + ".credit", "w").write(f"{taxon}: {html.unescape(p['attribution'])} — iNaturalist photo {p['id']}")
    return path


WM_OK = ("public domain", "cc0", "cc by ", "pd", "no restrictions")   # no share-alike (research/30)


def _wm_get(url, as_json=True):
    """Wikimedia GET with backoff: the shared egress gets 429s in bursts. Originals are refused (429), so
    images come from the standard thumbnail widths only."""
    import time
    for k in range(6):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "MeatballMythsBot/1.0 (research)"}),
                                       timeout=90)
            return json.load(r) if as_json else r.read()
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503):
                raise
            time.sleep(6 * (k + 1))
    raise SystemExit(f"wikimedia: still rate-limited on {url}")


def wm_photo(title, label, path):
    """A Wikimedia Commons file ("wm:File name.jpg"): public domain, CC0 or CC BY only (license read from the
    file page's metadata via en.wikipedia's API), fetched as a standard-width thumbnail, credited."""
    import re
    q = urllib.parse.urlencode({"action": "query", "titles": "File:" + title, "prop": "imageinfo",
                                "iiprop": "extmetadata|size|url", "format": "json"})
    page = next(iter(_wm_get("https://en.wikipedia.org/w/api.php?" + q)["query"]["pages"].values()))
    ii = page["imageinfo"][0]
    meta = ii.get("extmetadata", {})
    lic = meta.get("LicenseShortName", {}).get("value", "?")
    if not lic.lower().startswith(WM_OK) or "sa" in lic.lower().split():
        raise SystemExit(f"wm:{title}: license {lic} not reusable (PD, CC0 or CC BY only)")
    src = ii["url"].split("?")[0]
    head, name = src.rsplit("/", 1)
    data = None
    for w in (1920, 1280, 960):
        if w > ii["width"] * 1.6 and w != 960:
            continue
        thumb = head.replace("/commons/", "/commons/thumb/") + f"/{name}/{w}px-{name}"
        if name.lower().endswith((".png", ".gif", ".tif", ".tiff")) and not name.lower().endswith(".png"):
            thumb += ".jpg"
        try:
            data = _wm_get(thumb, as_json=False)
            break
        except urllib.error.HTTPError:
            continue
    if data is None:
        raise SystemExit(f"wm:{title}: no thumbnail")
    open(path, "wb").write(data)
    artist = re.sub(r"<[^>]+>", "", html.unescape(meta.get("Artist", {}).get("value", ""))).strip() or "unknown"
    open(path + ".credit", "w").write(f"{label}: \"{title}\" by {artist[:80]} ({lic}), via Wikimedia Commons")
    return path


def vo_path(b, work, name, rate):
    # Keyed by content, not position, so inserting or reordering beats never reuses the wrong line.
    tag = f"{name}|{rate}" + (f"|{PITCH}" if PITCH != "+0Hz" else "")
    key = hashlib.sha1(f"{tag}|{b['say']}".encode()).hexdigest()[:16]
    return f"{work}/vo/{key}.mp3"


def voice(beats, work, name, rate="+8%"):
    from facts import speak  # reuse the proxy-aware, retrying TTS
    os.makedirs(f"{work}/vo", exist_ok=True)
    if name.startswith("vidiq:"):
        # Premium narrator: audio comes pre-cut from tools/premium_voice.py; never mix in another voice.
        import shutil
        import premium_voice as pv
        missing = [b["say"] for b in beats if not pv.cached(name, b["say"])]
        if missing:
            os.makedirs(pv.CACHE, exist_ok=True)
            with open(f"{pv.CACHE}/missing.txt", "a") as f:
                f.writelines(json.dumps({"voice": name, "say": t}) + "\n" for t in missing)
            sys.exit(f"premium voice: {len(missing)} line(s) not voiced yet; run premium_voice.py prep-missing")
        for b in beats:
            src = pv.cached(name, b["say"])
            mp3 = vo_path(b, work, name, rate)
            shutil.copy(src, mp3)
            shutil.copy(src + ".words.json", mp3 + ".words.json")
        return
    if name.startswith("kokoro:"):
        # Free local narrator (tools/free_voice.py): generated on demand into the same cache, no prep step.
        import shutil
        import free_voice
        for b in beats:
            src = free_voice.make(name, b["say"])
            mp3 = vo_path(b, work, name, rate)
            shutil.copy(src, mp3)
            shutil.copy(src + ".words.json", mp3 + ".words.json")
        return
    for b in beats:
        mp3 = vo_path(b, work, name, rate)
        if not os.path.exists(mp3) or not os.path.exists(mp3 + ".words.json"):
            json.dump(asyncio.run(speak(b["say"], name, mp3, rate, PITCH)), open(mp3 + ".words.json", "w"))


def vertical():
    """Shorts layout: panel on top, Meatball bottom-left, word captions in between."""
    global W, H, PANEL, TEXT_PANEL, MASCOT, COVER, BLEED_MASCOT
    W, H = 1080, 1920
    PANEL = TEXT_PANEL = (40, 140, 1000, 1000)
    MASCOT = (860, (-120, H - 860 + 60))
    BLEED_MASCOT = (600, (-70, 1260))  # over a full-bleed photo: smaller, clear of the Shorts UI bar
    COVER = True


# Shot grammar (research/41): Meatball is the host, not a corner sticker. Each picture picks a framing:
#   show     sharp full-bleed photo, Meatball big (~42% of the frame) entering lower-left, cut at the waist
#   host     Meatball 60-75% of the frame in front of the photo, dimmed and blurred so he pops
#   together Meatball standing in the photo scene beside the animal (nervous / shock lines)
#   close    face and upper body fill the frame on the off-white background, slow push-in (punchlines)
#   card     text/quiz cards: the classic panel with Meatball under it
# "frame" (or "shot"): "show|host|together|close|card" on a beat or shot overrides the choice.
KINDS = ("show", "host", "together", "close", "card")


def shot_kind(s, prev=None, first=False):
    """Framing for one picture. first = frame 0 of a Short or its loop tail (the animal must be clear)."""
    want = s.get("frame") or s.get("shot")  # writers' scripts use "shot" for the same field
    want = "close" if want == "closeup" else want
    if want in KINDS:
        return want
    if any(k in s for k in ("text", "quiz", "img")):
        return "card"
    if "photo" not in s:
        return "close"
    if H <= W or PUNCH:
        return "card"  # long-form keeps the photo panel beside a big Meatball
    if first:
        return "show"
    if s.get("pose") in ("nervous", "shock") and prev != "together":
        return "together"
    return "show" if prev == "host" else "host"


def shot_layout(kind):
    """Mascot placement for a framing: size (px per 1000 drawing units), pos (screen point of unit 0,0),
    optional push-in, shadow, the caption anchor (ASS tags) and the direction he points/looks."""
    if H > W:
        return {
            "show": dict(size=1750, pos=(-645, 657), shadow=True, cap=r"{\an3\pos(1050,960)}", content=(0.9, -0.45)),
            "host": dict(size=1560, pos=(-310, 353), cap=r"{\an2\pos(540,1520)}", content=(0.6, -0.8)),
            "together": dict(size=1050, pos=(-225, 766), shadow=True, cap=r"{\an2\pos(600,1520)}", content=(0.9, -0.4)),
            "close": dict(size=2570, pos=(-745, -145), push=0.0006, anchor=(500, 360), cap=r"{\an2\pos(540,1560)}",
                          content=(0.94, -0.34)),
        }.get(kind, dict(size=1600, pos=(-260, 506), cap=r"{\an2\pos(540,1860)}", content=(0.5, -0.87)))
    if kind == "close":
        return dict(size=1445, pos=(238, -80), push=0.0006, anchor=(500, 360), content=(0.94, -0.34))
    return dict(size=MASCOT[0], pos=MASCOT[1], content=(0.94, -0.2))


def _captions(words, path, spans):
    """Word captions (facts.py style) placed per shot so they never sit on Meatball: spans = [(start s, tags)]."""
    from facts import captions
    captions(words, path)
    out = []
    for line in open(path).read().split("\n"):
        if line.startswith("Dialogue:"):
            t0 = line.split(",")[1].split(":")
            t0 = int(t0[0]) * 3600 + int(t0[1]) * 60 + float(t0[2])
            tags = [tg for st, tg in spans if st <= t0 + 0.01][-1:] or [spans[0][1]]
            head, txt = line.split(",Cap,", 1)
            line = f"{head},Cap,{tags[0]}{txt}"
        out.append(line)
    open(path, "w").write("\n".join(out))
    return path


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


def _panel_image(path, box=None):
    from PIL import Image, ImageFilter
    px, py, pw, ph = box or PANEL
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


def _quiz_short(statement, bg, count=None):
    """Shorts quiz card: the animal's photo is on screen from frame one (a text-only opener lost 60% of
    viewers in the first second), with the header and claim above it and the countdown on the photo."""
    from PIL import Image, ImageDraw, ImageFont
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    box = (60, 560, W - 120, 600)
    layer.alpha_composite(_panel_image(bg, box))
    d = ImageDraw.Draw(layer)
    head = ImageFont.truetype(BOLD, 96)
    label = "TRUE OR FALSE?"
    d.text(((W - d.textlength(label, font=head)) / 2, 110), label, font=head, fill=SAUCE)
    lines = statement.split("\n")
    size = 112
    while size > 70:
        font = ImageFont.truetype(BOLD, size)
        widths = [d.textlength(line, font=font) for line in lines]
        if max(widths) < W - 100 and size * 1.12 * len(lines) < 330:
            break
        size -= 4
    y = 235 + (330 - size * 1.12 * len(lines)) / 2
    for line, w in zip(lines, widths):
        d.text(((W - w) / 2, y), line, font=font, fill=(17, 17, 17))
        y += size * 1.12
    if count:
        r = 110
        cx, cy = W - 60 - r - 30, 560 + 600 - r - 30
        d.ellipse([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8], fill=(255, 255, 255))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SAUCE)
        f = ImageFont.truetype(BOLD, int(r * 1.3))
        d.text((cx - d.textlength(str(count), font=f) / 2, cy - r * 0.78), str(count), font=f, fill=(255, 255, 255))
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


def _cover(path, blur=0, dim=1.0, crop=None):
    """Photo scaled to fill the whole frame (crop the overflow), optionally blurred and darkened.
    crop = [x0, y0, x1, y1] as fractions of the photo: the region to fill the frame with."""
    from PIL import Image, ImageEnhance, ImageFilter
    im = Image.open(path).convert("RGB")
    if crop:
        im = im.crop((int(crop[0] * im.width), int(crop[1] * im.height), int(crop[2] * im.width), int(crop[3] * im.height)))
    s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    im = im.crop((l, t, l + W, t + H))
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    if dim != 1.0:
        im = ImageEnhance.Brightness(im).enhance(dim)
    return im.convert("RGBA")


def _framed(path):
    """Full-bleed in landscape. In a tall frame a center crop of a landscape photo cuts off heads, so the
    photo sits big in the middle (2/3 of its width kept) over a blurred, darkened copy of itself."""
    from PIL import Image
    if W >= H:
        return _cover(path)
    canvas = _cover(path, blur=24, dim=0.5)
    im = Image.open(path).convert("RGB")
    fh = int(H * 0.6)
    s = fh / im.height
    im = im.resize((max(W, int(im.width * s)), fh), Image.LANCZOS)
    l = (im.width - W) // 2
    canvas.paste(im.crop((l, 0, l + W, fh)), (0, int(H * 0.2)))
    return canvas


def _outlined(d, xy, text, font, fill, stroke=None):
    d.text(xy, text, font=font, fill=fill, stroke_width=stroke or max(4, font.size // 11), stroke_fill=(0, 0, 0))


def _fit(d, lines, max_w, max_h, start, floor=70):
    from PIL import ImageFont
    size = start
    while size > floor:
        font = ImageFont.truetype(BOLD, size)
        if max(d.textlength(x, font=font) for x in lines) < max_w and size * 1.12 * len(lines) < max_h:
            break
        size -= 6
    return ImageFont.truetype(BOLD, size)


def _punch_text(layer, text, cy, max_h, yellow_last=True):
    """Big white outlined lines centered on cy; the last line yellow (the punchline)."""
    from PIL import ImageDraw
    d = ImageDraw.Draw(layer)
    lines = text.split("\n")
    font = _fit(d, lines, W - 200, max_h, 160 if H > W else 150)
    total = font.size * 1.12 * len(lines)
    y = cy - total / 2
    for k, line in enumerate(lines):
        fill = YELLOW if yellow_last and k == len(lines) - 1 and len(lines) > 1 else (255, 255, 255)
        _outlined(d, ((W - d.textlength(line, font=font)) / 2, y), line, font, fill)
        y += font.size * 1.12


def _pill(layer, label, cy, fill=SAUCE, size=None):
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(layer)
    f = ImageFont.truetype(BOLD, size or (86 if H > W else 70))
    tw = d.textlength(label, font=f)
    x0, y0 = (W - tw) / 2 - 40, cy - f.size * 0.75
    d.rounded_rectangle([x0, y0, x0 + tw + 80, y0 + f.size * 1.5], 30, fill=fill, outline=(255, 255, 255), width=6)
    d.text((x0 + 40, y0 + f.size * 0.18), label, font=f, fill=(255, 255, 255))


def _stamp(layer, verdict):
    """Rotated TRUE/FALSE stamp slammed over the reveal photo."""
    from PIL import Image, ImageDraw, ImageFont
    true = verdict == "TRUE"
    col = (24, 170, 70) if true else SAUCE
    f = ImageFont.truetype(BOLD, 200 if H > W else 170)
    label = ("TRUE" if true else "FALSE") + (" \u2713" if true else " \u2717")
    tmp = Image.new("RGBA", (1400, 400), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    tw = d.textlength(label, font=f)
    d.rounded_rectangle([20, 20, tw + 120, 20 + f.size * 1.35], 40, fill=col + (235,), outline=(255, 255, 255), width=12)
    d.text((70, 20 + f.size * 0.12), label, font=f, fill=(255, 255, 255))
    tmp = tmp.crop(tmp.getbbox()).rotate(-8, expand=True, resample=Image.BICUBIC)
    layer.alpha_composite(tmp, (int((W - tmp.width) / 2), int(H * (0.16 if H > W else 0.08))))


def _counter(layer, n, total):
    """MYTH 3/12 badge, top-left: viewers always know how far in they are (and how much is left)."""
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(layer)
    f = ImageFont.truetype(BOLD, 54)
    label = f"MYTH {n}/{total}"
    tw = d.textlength(label, font=f)
    x, y = int(W * 0.08), int(H * 0.09)  # inside the area the Ken Burns zoom never crops
    d.rounded_rectangle([x, y, x + tw + 50, y + 84], 22, fill=(17, 17, 17, 220))
    d.text((x + 25, y + 12), label, font=f, fill=YELLOW)


def compose_punch(beat, i, work, picks, out, count=None, ctx=None):
    from PIL import Image, ImageFilter
    from mascot import draw
    ctx = ctx or {}
    bg = ctx.get("bg")
    if "photo" in beat:
        canvas = _framed(beat.get("_path") or photo(beat["photo"], beat.get("n", 0), work, beat.get("obs")))
    elif bg:  # quiz and text cards sit on the myth's photo so the animal is on screen from frame one
        canvas = _cover(bg, blur=0 if "quiz" in beat else 14, dim=0.55 if "quiz" in beat else 0.45)
    else:
        canvas = Image.new("RGBA", (W, H), (20, 20, 24, 255))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tall = H > W
    if "quiz" in beat:
        _pill(layer, "TRUE or FALSE?", H * (0.13 if tall else 0.14))
        _punch_text(layer, beat["quiz"], H * (0.36 if tall else 0.47), H * (0.30 if tall else 0.48), yellow_last=False)
        if count:
            from PIL import ImageDraw, ImageFont
            d = ImageDraw.Draw(layer)
            r = 130 if tall else 110
            cx, cy = W // 2, int(H * (0.62 if tall else 0.82))
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SAUCE + (255,), outline=(255, 255, 255), width=10)
            f = ImageFont.truetype(BOLD, int(r * 1.35))
            d.text((cx - d.textlength(str(count), font=f) / 2, cy - r * 0.82), str(count), font=f, fill=(255, 255, 255))
    elif "text" in beat:
        _punch_text(layer, beat["text"], H * (0.36 if tall else 0.45), H * (0.38 if tall else 0.62))
    if ctx.get("verdict"):
        _stamp(layer, ctx["verdict"])
    if ctx.get("n") and not tall:
        _counter(layer, ctx["n"], ctx["total"])
    canvas.alpha_composite(layer)
    if tall and "photo" in beat:  # photo beats belong to the animal; the bottom of a Short is under the app UI anyway
        canvas.convert("RGB").save(out)
        return None
    size = 420 if tall else 400
    # Clear of the zoom crop and, in Shorts, above the caption/like-button zone at the bottom.
    pos = (int(W * 0.06), int(H * 0.74) - size) if tall else (int(W * 0.08), int(H * 0.92) - size)
    if ANIMATE:  # build() overlays a talking, moving Meatball on top of the zoomed background
        canvas.convert("RGB").save(out)
        return beat.get("pose", "point"), size, pos
    m = draw(beat.get("pose", "point"), size)
    halo = m.split()[3].filter(ImageFilter.MaxFilter(15))
    canvas.paste((255, 255, 255, 255), pos, halo)
    canvas.alpha_composite(m, pos)
    canvas.convert("RGB").save(out)




def _aside(text, low=False):
    """Small grey footnote in a white pill under the panel: the narrator's inner voice, read not spoken.
    low: bottom-right of the frame, clear of a close-up Meatball."""
    from PIL import Image, ImageDraw, ImageFont
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = ImageFont.truetype(ASIDE_FONT, 50 if H > W else 42)
    px, py, pw, ph = PANEL
    tw = d.textlength(text, font=f)
    x, y = px + pw - tw - 70, py + ph - f.size - 60
    if low:  # close-up: top right, above his cap and clear of the fork
        x, y = W - tw - 70, 150 if H > W else 60
    d.rounded_rectangle([x - 26, y - 14, x + tw + 26, y + f.size + 20], 26, fill=(255, 255, 255, 235),
                        outline=(200, 200, 200, 255), width=3)
    d.text((x, y), text, font=f, fill=(110, 110, 110))
    return layer


def _prop(canvas, name, close=False, card=False):
    """Still prop standing on the floor to Meatball's left-hand side of the frame (his right)."""
    from PIL import ImageFilter
    from mascot import prop
    size, (mx, my) = MASCOT
    p = prop(name, int(size * 0.5))
    x, y = mx + int(size * 0.80), my + int(size * 0.80) - p.height
    if card:  # Shorts card shot: beside the big Meatball, right of him
        p = prop(name, int(H * 0.32))
        x, y = W - p.width - 70, H - p.height - 60
    if close:  # close-up: a big fork standing at the right edge, beside his shoulder
        p = prop(name, int(H * 0.42))
        x, y = W - int(p.width * 0.75), H - p.height - (260 if H > W else 40)
    halo = p.split()[3].filter(ImageFilter.MaxFilter(11))
    canvas.paste((255, 255, 255, 255), (x, y), halo)
    canvas.alpha_composite(p, (x, y))


def compose(beat, i, work, picks, out, count=None, ctx=None):
    if PUNCH:
        return compose_punch(beat, i, work, picks, out, count, ctx)
    from PIL import Image, ImageFilter
    from mascot import draw
    canvas = Image.new("RGBA", (W, H), BG + (255,))
    size, pos = MASCOT
    kind = beat.get("_kind")
    if ANIMATE and kind in ("show", "host", "together") and "photo" in beat:
        src = photo(beat["photo"], beat.get("n", 0), work, beat.get("obs"), "original")
        canvas = _cover(src, crop=beat.get("crop"), blur=9 if kind == "host" else 0, dim=0.8 if kind == "host" else 1.0)
        if beat.get("aside") and count is None:
            canvas.alpha_composite(_aside(beat["aside"]))
        canvas.convert("RGB").save(out)
        return beat.get("pose", "point"), size, pos, {"kind": kind, **shot_layout(kind)}
    if ANIMATE and kind == "close":
        if beat.get("aside") and count is None:
            canvas.alpha_composite(_aside(beat["aside"], low=True))
        if beat.get("prop"):
            _prop(canvas, beat["prop"], close=True)
        canvas.convert("RGB").save(out)
        return beat.get("pose", "point"), size, pos, {"kind": kind, **shot_layout(kind)}
    if beat.get("bleed") and "photo" in beat:  # Shorts v2: the animal fills the frame, Meatball sits on it
        canvas = _cover(photo(beat["photo"], beat.get("n", 0), work, beat.get("obs"), "original"), crop=beat.get("crop"))
        size, pos = BLEED_MASCOT
    elif "photo" in beat:
        canvas.alpha_composite(_panel_image(photo(beat["photo"], beat.get("n", 0), work, beat.get("obs"))))
    elif "quiz" in beat and H > W and (ctx or {}).get("bg"):
        canvas.alpha_composite(_quiz_short(beat["quiz"], ctx["bg"], count))
    elif "quiz" in beat:
        canvas.alpha_composite(_panel_quiz(beat["quiz"], count))
    elif "text" in beat:
        canvas.alpha_composite(_panel_text(beat["text"]))
    elif "img" in beat:
        canvas.alpha_composite(_panel_image(f"{work}/img/{i:02d}_s{picks.get(str(i), 0)}.png"))
    if beat.get("aside") and count is None:
        canvas.alpha_composite(_aside(beat["aside"]))
    big = ANIMATE and H > W and not PUNCH and not beat.get("bleed") and "quiz" not in beat  # quiz cards keep room
    if beat.get("prop"):
        _prop(canvas, beat["prop"], card=big)
    if ANIMATE:
        canvas.convert("RGB").save(out)
        lay = shot_layout("card") if big else dict(shot_layout("card"), size=size, pos=pos)
        return beat.get("pose", "point"), size, pos, {"kind": "card", **lay}
    m = draw(beat.get("pose", "point"), size)
    halo = m.split()[3].filter(ImageFilter.MaxFilter(15))  # white outline keeps him readable over panels
    canvas.paste((255, 255, 255, 255), pos, halo)
    canvas.alpha_composite(m, pos)
    canvas.convert("RGB").save(out)


def countdown(b, i, work, picks, ctx=None):
    """3-2-1 after a quiz claim: one second per number with a tick, so viewers lock in a guess."""
    segs = []
    for c in (3, 2, 1):
        img, seg = f"{work}/frame{i:02d}_c{c}.png", f"{work}/seg{i:02d}_c{c}.mp4"
        m = compose(b, i, work, picks, img, count=c, ctx=ctx)
        raw = seg.replace(".mp4", "_raw.mp4") if m else seg
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", img,
                        "-f", "lavfi", "-i", "sine=frequency=1100:duration=0.07",
                        "-vf", f"scale={W}:{H},format=yuv420p", "-af", "apad", "-t", f"{COUNT_S}",
                        "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-r", str(FPS),
                        "-c:a", "aac", "-ar", "48000", "-ac", "2", raw], check=True)
        if m:  # thinking face while the viewer guesses
            overlay_mascot(raw, ("think",) + m[1:], [], COUNT_S, f"{work}/m{i:02d}_c{c}", seg, pop=c == 3,
                           enter=c == 3, exit=c == 1)
        segs.append(seg)
    return segs


def contexts(beats, work):
    """Per-beat extras for the punch style: the myth's photo behind quiz/text cards, the TRUE/FALSE
    verdict on the reveal beat, and the myth number for the on-screen counter."""
    myths = list(dict.fromkeys(b.get("myth") for b in beats if b.get("myth") not in (None, "intro", "outro")))
    photos = [photo(b["photo"], b.get("n", 0), work, b.get("obs")) if "photo" in b else None for b in beats]
    out = []
    for i, b in enumerate(beats):
        c = {}
        m = b.get("myth")
        if m in myths:
            c["n"], c["total"] = myths.index(m) + 1, len(myths)
        same = [j for j in range(len(beats)) if photos[j] and beats[j].get("myth") == m]
        nxt = [j for j in same if j > i] or [j for j in range(i + 1, len(beats)) if photos[j]]
        prv = [j for j in same if j < i] or [j for j in range(i) if photos[j]]
        pick = (nxt or prv) if "quiz" in b else (prv or nxt)
        if pick:
            c["bg"] = photos[pick[0] if pick is nxt else pick[-1]]
        if photos[i]:  # a second photo of the same myth to cut to halfway through a long line
            alts = [photos[j] for j in same if photos[j] != photos[i]]
            if alts:
                c["alt"] = alts[(same.index(i) + 1) % len(alts)] if i in same else alts[0]
        if i and "quiz" in beats[i - 1]:
            w = b["say"].split()[0].strip(".,!?").upper() if b["say"].split() else ""
            if b.get("verdict") or w in ("TRUE", "FALSE"):
                c["verdict"] = b.get("verdict") or w
        out.append(c)
    return out


SFX = {  # synthesized, so there is nothing to license
    "FALSE": "aevalsrc=0.5*sgn(sin(2*PI*140*t))*exp(-5*t):d=0.45:s=48000",
    "TRUE": "aevalsrc=0.4*sin(2*PI*1318*t)*exp(-7*t)+0.4*sin(2*PI*1760*t)*exp(-7*(t-0.12))*gte(t\\,0.12):d=0.7:s=48000",
    # The show's one signature sting (research/39): a fork tapping a plate. Inharmonic partials, fast decay.
    "tink": "aevalsrc=0.30*sin(2*PI*2960*t)*exp(-22*t)+0.18*sin(2*PI*4410*t)*exp(-30*t)+0.10*sin(2*PI*6650*t)*exp(-40*t):d=0.35:s=48000",
}


def overlay_mascot(raw, m, words, dur, frames_dir, seg, pop=True, seed=0, enter=True, exit=True):
    """Composite a talking Meatball (mascot.animate, 30 fps, full transparent frames) over a rendered
    segment. He sits outside the zoom, so the background moves while he keeps acting. m = (pose, size, pos)
    or (pose, size, pos, extra): extra["layouts"] = [(start s, layout)] cuts his framing on shot changes,
    extra["ass"] burns captions on top of him. enter/exit=False carries a pose across segments."""
    import mascot
    pose, size, pos = m[:3]
    extra = m[3] if len(m) > 3 else {}
    layouts = extra.get("layouts") or [(0.0, dict(extra, size=size, pos=pos))]
    sched = [dict(t=t, size=l["size"], pos=l["pos"], push=l.get("push", 0.0), anchor=l.get("anchor", (500, 360)),
                  shadow=l.get("shadow", False)) for t, l in layouts]
    content = layouts[0][1].get("content", (0.94, -0.34))
    shutil.rmtree(frames_dir, ignore_errors=True)
    mascot.animate(pose, size, words, dur, FPS, frames_dir, seed=seed, enter=enter, exit=exit, content=content,
                   canvas=(W, H), layout=sched, glow=extra.get("glow"))
    vf = f"[0:v][1:v]overlay=0:0:eof_action=repeat" + (f",ass={extra['ass']}" if extra.get("ass") else "") + ",format=yuv420p"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", raw, "-framerate", str(FPS), "-i", f"{frames_dir}/%04d.png",
                    "-filter_complex", vf, "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "copy", seg],
                   check=True)
    shutil.rmtree(frames_dir, ignore_errors=True)
    os.remove(raw)


VISUAL = ("photo", "obs", "n", "text", "quiz", "img", "crop", "aside", "shots")
MAX_HOLD = 3.0  # Shorts gate (research/38): no single picture on screen longer than this


def shots(b):
    """A beat's pictures. A "shots" list cuts between several pictures under one voice line; each shot
    is a dict of visual fields (photo/obs/crop, text, aside, or {} for Meatball alone on white) and may
    start on a spoken word with "at". Non-visual beat fields (pose, prop, bleed...) apply to every shot."""
    if "shots" not in b:
        return [b]
    base = {k: v for k, v in b.items() if k not in VISUAL}
    return [dict(base, **s) for s in b["shots"]]


def _shot_frames(b, words, frames):
    """Frame index where each shot starts: on its "at" word (first match after the previous cut), else
    an even split."""
    sh, n = b["shots"], len(b["shots"])
    starts, wi = [0], 0
    for k in range(1, n):
        at = (sh[k].get("at") or "").lower().strip(".,!?")
        hit = next((j for j in range(wi, len(words)) if at and words[j][2].lower().strip(".,!?") == at), None)
        if hit is None:
            starts.append(int(frames * k / n))
        else:
            starts.append(int(words[hit][0] * FPS))
            wi = hit + 1
    return starts + [frames]


def render_shots(b, i, work, picks, mp3, dur, seg, loop_in, loop_out):
    """Multi-shot beat: one zoompan per picture (each moving from its first frame), hard cuts on the
    words, captions over the whole line. loop_in starts the first shot at zoom 1.0; loop_out ends the
    last one at 1.0, so the Short's last frame matches its first. Returns (mascot, [shot seconds])."""
    words = json.load(open(mp3 + ".words.json"))
    frames = int(dur * FPS)
    bounds = _shot_frames(b, words, frames)
    vis = shots(b)
    m, inputs, chains, holds, layouts = None, [], [], [], []
    k_ = 0.0012  # zoom per frame: about 3.6% a second, visible but calm
    prev = PREV_KIND[0]
    for k, sb in enumerate(vis):
        img = f"{work}/frame{i:02d}s{k}.png"
        kind = shot_kind(sb, prev, first=(loop_in and k == 0) or (loop_out and k == len(vis) - 1)) if ANIMATE else None
        prev = kind
        mk = compose(dict(sb, _kind=kind), i, work, picks, img)
        if mk:
            layouts.append((bounds[k] / FPS, mk[3] if len(mk) > 3 else dict(size=mk[1], pos=mk[2])))
        m = m or mk
        d = max(1, bounds[k + 1] - bounds[k])
        holds.append(d / FPS)
        if loop_in and k == 0:
            z = f"1.0+{k_}*on"
        elif loop_out and k == len(vis) - 1:
            z = f"1.0+{k_}*({d - 1}-on)"
        else:
            z = f"min(1.0+{k_}*on,1.12)" if (i + k) % 2 == 0 else f"max(1.10-{k_}*on,1.0)"
        inputs += ["-loop", "1", "-i", img]
        chains.append(f"[{k}:v]scale={W * 2}:{H * 2}:flags=lanczos,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':"
                      f"y='ih/2-(ih/zoom/2)':d={d}:s={W}x{H}:fps={FPS},trim=end_frame={d},setpts=PTS-STARTPTS[v{k}]")
    n = len(vis)
    PREV_KIND[0] = prev
    vf = ";".join(chains) + ";" + "".join(f"[v{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=0"
    if m and len(m) > 3:  # placed Meatball: captions go on top of him, positioned per shot
        cap = None
        if H > W and not any("text" in x for x in vis):
            cap = _captions(words, f"{work}/cap{i:02d}.ass", [(t, l.get("cap", "")) for t, l in layouts])
        m = m[:3] + ({"layouts": layouts, "ass": cap, "glow": _glow(b)},)
    elif H > W and not any("text" in x for x in vis):  # muted viewers: captions on every non-card line
        from facts import captions
        ass = f"{work}/cap{i:02d}.ass"
        captions(words, ass)
        txt = open(ass).read()
        txt = txt.replace("-1,1,7,3,5,0", "-1,1,7,3,2,760") if b.get("bleed") else txt
        open(ass, "w").write(txt)
        vf += f",ass={ass}"
    vf += ",format=yuv420p[vout]"
    audio = ["-i", mp3]
    if b.get("sting") in SFX:
        audio += ["-f", "lavfi", "-i", SFX[b["sting"]]]
        vf += f";[{n}:a]apad[vo];[{n + 1}:a]volume=0.5[s];[vo][s]amix=inputs=2:duration=first:normalize=0[aout]"
    else:
        vf += f";[{n}:a]apad[aout]"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y"] + inputs + audio + ["-filter_complex", vf, "-map", "[vout]",
                    "-map", "[aout]", "-t", f"{dur:.2f}", "-c:v", "libx264", "-crf", "20", "-preset", "medium",
                    "-c:a", "aac", "-ar", "48000", "-ac", "2", seg], check=True)
    return m, holds


PREV_KIND = [None]  # the last framing used, so consecutive pictures alternate show/host


def split_long(b, mp3):
    """Vertical Shorts cut every ~1.5-2.5 s (research/41-stickman-reference): a photo shot longer than 2.6 s
    is split on the word nearest its middle into two shots of the same picture, which then get different
    framings (show / host). Loop tails are left alone so the seam frame stays exact."""
    if not (ANIMATE and H > W and not PUNCH) or b.get("loop") or ("photo" not in b and "shots" not in b):
        return b
    words = json.load(open(mp3 + ".words.json")) if os.path.exists(mp3 + ".words.json") else []
    if not words:
        return b
    raw = b.get("shots") or [{k: b[k] for k in VISUAL if k in b}]
    total = int((duration(mp3) + 0.35 + float(b.get("hold", 0))) * FPS)
    bounds = _shot_frames({"shots": raw}, words, total)
    out = []
    for k, sh in enumerate(raw):
        out.append(sh)
        a, z = bounds[k] / FPS, bounds[k + 1] / FPS
        if "photo" not in sh or z - a <= 2.6:
            continue
        cands = [w for w in words if a + 1.0 <= w[0] <= z - 1.0]
        if cands:
            w = min(cands, key=lambda w: abs(w[0] - (a + z) / 2))
            out.append(dict({kk: vv for kk, vv in sh.items() if kk != "at"}, at=w[2]))
    if len(out) == len(raw) and "shots" not in b:
        return b
    return dict({k: v for k, v in b.items() if k not in VISUAL}, shots=out)


def _glow(b):
    """Emotion glow for a line: the beat's "glow" (yellow warning, red danger, green good), else green
    when a reveal opens on "True"."""
    if b.get("glow"):
        return b["glow"]
    return "green" if b.get("say", "").lower().startswith("true") else None


def gate(beats, holds):
    """Shorts v2 render gate (research/38): warn when a Short opens without a photo or holds one picture
    longer than MAX_HOLD seconds. Warnings only; the build still completes."""
    warn = []
    first = shots(beats[0])[0] if beats else {}
    if "photo" not in first:
        warn.append("opens without a photo (frame 0 should be the animal)")
    for label, sec in holds:
        if sec > MAX_HOLD + 0.05:
            warn.append(f"{label} holds one picture for {sec:.1f}s (max {MAX_HOLD:.0f}s)")
    for w in warn:
        print(f"GATE WARN: {w}", flush=True)
    return warn


def build(beats, work, out, picks, name, rate="+8%"):
    voice(beats, work, name, rate)
    ctxs = contexts(beats, work) if PUNCH or H > W else [None] * len(beats)
    if beats and beats[-1].get("loop") and ctxs[0] is not None:
        ctxs[-1] = dict(ctxs[-1], bg=ctxs[0].get("bg"))  # loop frame must match frame 0 exactly
    segs, holds = [], []
    looping = any(x.get("loop") for x in beats)
    PREV_KIND[0] = None
    for i, b in enumerate(beats):
        img, mp3, seg = f"{work}/frame{i:02d}.png", vo_path(b, work, name, rate), f"{work}/seg{i:02d}.mp4"
        ctx = ctxs[i]
        b = split_long(b, mp3)
        if "shots" in b:
            dur = duration(mp3) + 0.35 + float(b.get("hold", 0))
            raw = seg.replace(".mp4", "_raw.mp4")
            m, sh = render_shots(b, i, work, picks, mp3, dur, raw, looping and i == 0, bool(b.get("loop")))
            holds += [(f"beat {i} shot {k}", t) for k, t in enumerate(sh)]
            if m:
                overlay_mascot(raw, m, json.load(open(mp3 + ".words.json")), dur, f"{work}/m{i:02d}", seg, seed=i)
            else:
                os.replace(raw, seg)
            segs.append(seg)
            continue
        kind = None
        if ANIMATE and not PUNCH:
            kind = shot_kind(b, PREV_KIND[0], first=(looping and i == 0) or bool(b.get("loop")))
            PREV_KIND[0] = kind
        m = compose(dict(b, _kind=kind) if kind else b, i, work, picks, img, ctx=ctx)
        if m and len(m) > 3:
            m = m[:3] + (dict(m[3], glow=_glow(b)),)
        final, seg = seg, (seg.replace(".mp4", "_raw.mp4") if m else seg)
        dur = duration(mp3) + (0.15 if PUNCH else 0.35) + float(b.get("hold", 0))
        frames = int(dur * FPS)
        if PUNCH and i == 0:  # snap-in on the very first frame: motion before the viewer can swipe
            z = "if(lt(on,8),1.08-0.01*on,1.0+0.0015*(on-8))"
        elif PUNCH:
            z = "min(1.0+0.0015*on,1.14)" if i % 2 == 0 else "max(1.14-0.0015*on,1.0)"
        elif b.get("loop") or (i == 0 and any(x.get("loop") for x in beats)):
            z = "1.0"  # loop ends: still frames, so the last frame cuts invisibly into the first
        else:
            # Slow Ken Burns: alternate zoom-in / zoom-out so consecutive beats don't feel identical.
            z = "min(1.0+0.0008*on,1.08)" if i % 2 == 0 else "max(1.08-0.0008*on,1.0)"
        zp = "scale={w}:{h}:flags=lanczos,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={d}:s={W}x{H}:fps={FPS}"
        split = PUNCH and ctx.get("alt") and "photo" in b and dur > 3.6
        if split:
            # Something new on screen every 2-3 s: the second half of a long line cuts to another photo.
            img2 = f"{work}/frame{i:02d}b.png"
            compose(dict(b, photo=b["photo"], obs=None, _path=ctx["alt"]), i, work, picks, img2, ctx=dict(ctx, verdict=None))
            half = int(frames / 2)
            z2 = "max(1.14-0.0015*on,1.0)" if i % 2 == 0 else "min(1.0+0.0015*on,1.14)"
            vf = (f"[0:v]{zp.format(w=W*2, h=H*2, z=z, d=half, W=W, H=H, FPS=FPS)},trim=end_frame={half}[a];"
                  f"[2:v]{zp.format(w=W*2, h=H*2, z=z2, d=frames - half, W=W, H=H, FPS=FPS)},trim=end_frame={frames - half}[b];"
                  f"[a][b]concat=n=2:v=1:a=0,format=yuv420p")
        else:
            vf = zp.format(w=W*2, h=H*2, z=z, d=frames, W=W, H=H, FPS=FPS) + ",format=yuv420p"
        if PUNCH and ctx and ctx.get("verdict"):  # 6-frame screen shake as the stamp lands
            sh = f"crop={W - 24}:{H - 24}:x='12+12*sin(n*9)*lt(n,6)':y='12+12*cos(n*7)*lt(n,6)',scale={W}:{H},"
            vf = vf[:-len("format=yuv420p")] + sh + "format=yuv420p"
        top_cap = None
        if H > W and m and len(m) > 3 and "text" not in b and "quiz" not in b:  # captions on top of Meatball
            top_cap = _captions(json.load(open(mp3 + ".words.json")), f"{work}/cap{i:02d}.ass", [(0.0, m[3].get("cap", ""))])
            m = m[:3] + (dict(m[3], ass=top_cap),)
        if H > W and not top_cap:  # Shorts are mostly watched muted: burn word-by-word captions on photo beats
            if "text" not in b and "quiz" not in b:  # a quiz caption would read "FALSE" before the countdown
                from facts import captions
                ass = f"{work}/cap{i:02d}.ass"
                captions(json.load(open(mp3 + ".words.json")), ass)
                # facts.py centers captions mid-screen; drop them into the gap between panel and Meatball
                txt = open(ass).read()
                txt = (txt.replace("-1,1,7,3,5,0", "-1,1,8,3,2,620").replace(",96,", ",124,") if PUNCH
                       else txt.replace("-1,1,7,3,5,0", "-1,1,7,3,2,700"))
                open(ass, "w").write(txt)
                vf += f",ass={ass}"
        if PUNCH and ctx and ctx.get("verdict"):  # buzzer or ding under the reveal line
            audio = ["-f", "lavfi", "-i", SFX[ctx["verdict"]], "-filter_complex",
                     "[1:a]apad[v];[2:a]volume=0.8[s];[v][s]amix=inputs=2:duration=first:normalize=0[a]",
                     "-map", "0:v", "-map", "[a]"]
        elif b.get("sting") in SFX:  # quiet, under the voice, at the top of the beat
            audio = ["-f", "lavfi", "-i", SFX[b["sting"]], "-filter_complex",
                     "[1:a]apad[v];[2:a]volume=0.5[s];[v][s]amix=inputs=2:duration=first:normalize=0[a]",
                     "-map", "0:v", "-map", "[a]"]
        else:
            audio = ["-af", "apad"]
        if split:  # image inputs 0 and 2, voice 1 (SFX, if any, stays input 2 in the mix below -> renumber)
            if ctx.get("verdict"):
                audio = ["-f", "lavfi", "-i", SFX[ctx["verdict"]]]
                mix = ";[1:a]apad[vo];[3:a]volume=0.8[s];[vo][s]amix=inputs=2:duration=first:normalize=0[aout]"
            else:
                audio, mix = [], ";[1:a]apad[aout]"
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-i", img, "-i", mp3, "-loop", "1",
                            "-i", img2] + audio + ["-filter_complex", vf + "[vout]" + mix, "-map", "[vout]",
                            "-map", "[aout]", "-t", f"{dur:.2f}", "-c:v", "libx264", "-crf", "20", "-preset",
                            "medium", "-c:a", "aac", "-ar", "48000", "-ac", "2", seg], check=True)
        else:
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-i", img, "-i", mp3] + audio +
                           ["-vf", vf, "-t", f"{dur:.2f}", "-c:v", "libx264", "-crf", "20", "-preset", "medium",
                            "-c:a", "aac", "-ar", "48000", "-ac", "2", seg], check=True)
        if m:
            looped = i == 0 and any(x.get("loop") for x in beats)  # no pop-in at the loop seam
            overlay_mascot(seg, m, json.load(open(mp3 + ".words.json")), dur, f"{work}/m{i:02d}", final, seed=i,
                           pop=not looped)
        seg = final
        segs.append(seg)
        holds.append((f"beat {i}", dur))
        if "quiz" in b and not b.get("nocount"):
            segs += countdown(b, i, work, picks, ctx)
    if H > W:
        gate(beats, holds)
    # Only the photos actually used, so the description never credits a swapped-out image.
    used = sorted({photo(v["photo"], v.get("n", 0), work, v.get("obs")) for b in beats for v in shots(b) if "photo" in v})
    open(f"{work}/credits.txt", "w").write("".join(open(u + ".credit").read() + "\n" for u in used))
    lst = f"{work}/list.txt"
    open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    if MUSIC and os.path.exists(MUSIC):
        # Looped bed, ducked under the narrator by a sidechain so it lifts only in the pauses.
        af = ["-stream_loop", "-1", "-i", MUSIC, "-filter_complex",
              "[0:a]asplit[v][key];[1:a]volume=0.12" + ("" if any(b.get("loop") for b in beats) else ",afade=t=in:d=2") + "[m];"
              "[m][key]sidechaincompress=threshold=0.02:ratio=6:attack=30:release=500[d];"
              "[v][d]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5[a]",
              "-map", "0:v", "-map", "[a]"]
    else:
        af = ["-af", "loudnorm=I=-14:TP=-1.5"]
    if PUNCH and H > W:
        # Progress bar across the top: a visible "almost done" keeps people to the end of a Short.
        total = sum(duration(x) for x in segs)
        vcodec = ["-vf", f"drawbox=x=0:y=0:w='iw*t/{total:.2f}':h=16:color=0xFFD60A@1:t=fill",
                  "-c:v", "libx264", "-crf", "21", "-preset", "medium"]
    else:
        vcodec = ["-c:v", "copy"]
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst] + af + vcodec +
                   ["-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out], check=True)
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
    global PUNCH, ANIMATE, COUNT_S, PITCH
    ANIMATE = spec.get("style") != "static"
    PITCH = spec.get("pitch", PITCH)
    if a.vertical:
        COUNT_S = 0.5  # a 1.5 s countdown in Shorts; the full 3 s is where viewers swiped
    if spec.get("style") == "punch":
        PUNCH, COUNT_S = True, (0.5 if a.vertical else 0.7)
    if spec.get("music"):
        global MUSIC
        MUSIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "brand", spec["music"])
    if a.vertical:
        vertical()
    if spec.get("style") in ("v3", "v4") and a.stage == "build":  # Shorts v3/v4 (research/44, 45): tools/v3.py
        import v3
        # "aspect": "16:9" = a v3/v4 long-form (1920x1080, v3.landscape()); everything else stays a vertical Short
        wide = spec.get("aspect") == "16:9" and not a.vertical
        return v3.build(spec, a.work, a.out, MUSIC, vertical=not wide)  # v3 imports explainer afresh: pass the bed
    if a.stage == "images":
        images(spec["beats"], a.work, a.seeds)
    else:
        picks = json.load(open(a.pick)) if a.pick else {}
        build(spec["beats"], a.work, a.out, picks, spec.get("voice", "en-US-AndrewNeural"), spec.get("rate", "+8%"))


if __name__ == "__main__":
    main()
