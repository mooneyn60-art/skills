#!/usr/bin/env python3
""""Meatball Investigates" visuals for tools/v3.py (research/48): the series card, verdict stamps, evidence
boards, and the two sound effects they use. All drawn here (PIL); nothing to license.

Script fields (v3/v4 specs):
  spec "series": {"text": "MEATBALL INVESTIGATES", "case": "CASE #3"}
      a small case-file tag top left on every frame (so the loop seam still matches frame 0), and on the first
      beat a big manila case-file card that drops in from frame 4 with the "case" sting
  beat "stamp": {"text": "BUSTED", "at": "word", "y": 0.42, "reveal": true}  (or a list of them; "reveal":
      false = no music drop-out/hit for it, e.g. a CLASSIFIED stamp in the hook)
      a rubber stamp slams onto the picture on the word, with a thud, a screen shake and the music's drop-out
      and hit (tools/music.py). Colours: TRUE / PROVEN / REAL green; FALSE / BUSTED / MYTH red;
      CLASSIFIED / TOP SECRET red; anything else ink blue. "color": [r, g, b] overrides
  shot "board": {"notes": ["1962", "TOP SECRET"], "stamp": "CLASSIFIED"}
      the shot's photo becomes a pinned polaroid on a cork evidence board, with index-card notes tied to it by
      red string (and an optional stamp printed on the photo). Board shots are drawn as v3 stills (no cut-out)
  spec "captions": "bold"   heavier captions (Inter Black, bigger, thicker outline)
"""
import math
import os
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

INTER_BLACK = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
DEJAVU_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
GREEN, RED, BLUE = (30, 165, 70), (215, 30, 35), (35, 70, 170)
MANILA, INK = (236, 205, 140), (40, 30, 20)


def font(path, size):
    for p in (path, INTER_BLACK, DEJAVU_BOLD):
        if p and os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def _find_inter():
    global INTER_BLACK
    if os.path.exists(INTER_BLACK):
        return
    for root, _, files in os.walk("/usr/share/fonts"):
        for f in files:
            if f.replace(" ", "").lower() in ("inter-black.ttf", "inter-black.otf"):
                INTER_BLACK = os.path.join(root, f)
                return


_find_inter()


def stamp_color(text):
    t = text.upper()
    if any(w in t for w in ("TRUE", "PROVEN", "REAL", "CONFIRMED", "SOLVED")):
        return GREEN
    if any(w in t for w in ("FALSE", "BUSTED", "MYTH", "CLASSIFIED", "SECRET", "FAKE", "DEBUNKED")):
        return RED
    return BLUE


def stamp_img(text, color=None, scale=1.0):
    """A rubber stamp: double border, worn ink, tilted -9 degrees. RGBA numpy array."""
    color = tuple(color or stamp_color(text))
    f = font(INTER_BLACK, int(150 * scale))
    lines = text.upper().split("\n")
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = int(max(d.textlength(x, font=f) for x in lines))
    lh = int(160 * scale)
    pad = int(48 * scale)
    w, h = tw + 2 * pad, lh * len(lines) + 2 * pad - int(20 * scale)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    b = int(14 * scale)
    dr.rounded_rectangle([b // 2, b // 2, w - b // 2, h - b // 2], int(26 * scale), outline=color + (255,), width=b)
    dr.rounded_rectangle([b * 2, b * 2, w - b * 2, h - b * 2], int(14 * scale), outline=color + (255,), width=max(2, b // 3))
    for k, line in enumerate(lines):
        dr.text(((w - dr.textlength(line, font=f)) / 2, pad - int(18 * scale) + k * lh), line, font=f,
                fill=color + (255,))
    a = np.asarray(im).copy()
    rng = np.random.default_rng(abs(hash(text)) % 2 ** 32)
    wear = rng.random(a.shape[:2])   # worn ink: speckle holes and a slightly uneven density
    blot = np.asarray(Image.fromarray((rng.random((h // 24 + 2, w // 24 + 2)) * 255).astype(np.uint8))
                      .resize((w, h), Image.BICUBIC)) / 255.0
    keep = (wear > 0.07) & (blot > 0.12)
    a[..., 3] = (a[..., 3] * keep * (0.78 + 0.22 * blot)).astype(np.uint8)
    out = Image.fromarray(a).rotate(9, expand=True, resample=Image.BICUBIC)
    return np.asarray(out)


def series_imgs(series, W):
    """(card, tag): the big case-file card for the hook, and the small persistent tag."""
    text = series.get("text", "MEATBALL INVESTIGATES").upper()
    case = series.get("case", "").upper()
    # card: manila folder with a tab, typed case number, red rule
    f1, f2 = font(INTER_BLACK, 74), font(MONO, 50)
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = int(d.textlength(text, font=f1))
    w = min(W - 60, tw + 110)
    h = 196 if case else 140
    im = Image.new("RGBA", (w, h + 46), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([24, 0, 24 + int(w * 0.36), 70], 16, fill=MANILA + (255,))   # the folder tab
    dr.rounded_rectangle([0, 34, w - 1, 34 + h], 18, fill=MANILA + (255,), outline=(120, 90, 40, 255), width=4)
    dr.text(((w - tw) / 2, 52), text, font=f1, fill=INK)
    if case:
        cw = dr.textlength(case, font=f2)
        dr.line([(40, 148), (w - 40, 148)], fill=RED + (255,), width=4)
        dr.text(((w - cw) / 2, 160), case, font=f2, fill=RED)
    card = np.asarray(im.filter(ImageFilter.SMOOTH))
    # tag: small dark pill, magnifier dot, "MEATBALL INVESTIGATES · CASE #3"
    f3 = font(INTER_BLACK, 34)
    label = text + (f"  {case}" if case else "")
    lw = int(d.textlength(label, font=f3))
    tag = Image.new("RGBA", (lw + 92, 62), (0, 0, 0, 0))
    td = ImageDraw.Draw(tag)
    td.rounded_rectangle([0, 0, lw + 91, 61], 30, fill=(15, 15, 18, 200), outline=(236, 205, 140, 255), width=3)
    td.ellipse([16, 14, 44, 42], outline=(255, 214, 10, 255), width=5)        # magnifier
    td.line([(40, 38), (54, 52)], fill=(255, 214, 10, 255), width=6)
    td.text((70, 10), label, font=f3, fill=(255, 255, 255))
    return card, np.asarray(tag)


# ---------------------------------------------------------------- evidence board

def _cork(w, h, seed=7):
    rng = np.random.default_rng(seed)
    base = np.zeros((h, w, 3), np.float32) + np.array([158, 112, 66], np.float32)
    for s, amp in ((3, 26), (9, 18), (40, 14)):
        n = rng.standard_normal((h // s + 2, w // s + 2)).astype(np.float32)
        n = np.asarray(Image.fromarray(n).resize((w, h), Image.BICUBIC))
        base += n[..., None] * amp
    speck = rng.random((h, w)) > 0.985
    base[speck] *= 0.55
    yy, xx = np.mgrid[0:h, 0:w]
    vig = 1 - 0.35 * (((xx / w - 0.5) ** 2 + (yy / h - 0.5) ** 2) * 2.2)
    return Image.fromarray(np.clip(base * vig[..., None], 0, 255).astype(np.uint8))


def _pin(dr, x, y, r=16):
    dr.ellipse([x - r + 4, y - r + 6, x + r + 4, y + r + 6], fill=(0, 0, 0, 90))
    dr.ellipse([x - r, y - r, x + r, y + r], fill=(205, 25, 30, 255), outline=(120, 10, 10, 255), width=3)
    dr.ellipse([x - r // 3 - 3, y - r // 3 - 3, x - r // 3 + 4, y - r // 3 + 4], fill=(255, 190, 190, 255))


def _string(dr, a, b, sag=40):
    pts = []
    for k in range(25):
        u = k / 24
        pts.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u + sag * 4 * u * (1 - u)))
    dr.line([(x + 3, y + 4) for x, y in pts], fill=(0, 0, 0, 80), width=7)
    dr.line(pts, fill=(200, 20, 25, 255), width=6)


def board(path, spec, work, vertical=True):
    """Compose the evidence board for a shot photo; returns the new image path (credit copied)."""
    notes = list(spec.get("notes") or [])
    key = f"{os.path.basename(path)}|{'|'.join(notes)}|{spec.get('stamp', '')}|{vertical}"
    out = f"{work}/photos/board_{abs(hash(key)) % 10 ** 10}.jpg"
    if os.path.exists(out):
        return out
    W, H = (1300, 2311) if vertical else (2311, 1300)
    bd = _cork(W, H).convert("RGBA")
    ph = Image.open(path).convert("RGB")
    pw = int(W * (0.66 if vertical else 0.40))
    phh = int(pw * min(1.25, max(0.62, ph.height / ph.width)))
    s = max(pw / ph.width, phh / ph.height)
    ph = ph.resize((int(ph.width * s) + 1, int(ph.height * s) + 1), Image.LANCZOS)
    l, t = (ph.width - pw) // 2, (ph.height - phh) // 2
    ph = ph.crop((l, t, l + pw, t + phh))
    m = int(pw * 0.05)
    pol = Image.new("RGBA", (pw + 2 * m, phh + m + int(m * 3.2)), (250, 248, 240, 255))
    pol.paste(ph, (m, m))
    if spec.get("stamp"):
        st = Image.fromarray(stamp_img(spec["stamp"], scale=pw / 1500))
        pol.alpha_composite(st, (pol.width - st.width - m // 2, pol.height - st.height - m // 2))
    pol = pol.rotate(-3.5, expand=True, resample=Image.BICUBIC)
    cx, cy = (int(W * 0.58), int(H * 0.36)) if vertical else (int(W * 0.62), int(H * 0.45))
    shadow = Image.new("RGBA", pol.size, (0, 0, 0, 0))
    shadow.putalpha(pol.getchannel("A").point(lambda v: v * 0.45))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    bd.alpha_composite(shadow, (cx - pol.width // 2 + 14, cy - pol.height // 2 + 18))
    bd.alpha_composite(pol, (cx - pol.width // 2, cy - pol.height // 2))
    dr = ImageDraw.Draw(bd)
    top_pin = (cx, cy - pol.height // 2 + 30)
    spots = ([(0.22, 0.13), (0.80, 0.70), (0.20, 0.70)] if vertical else [(0.16, 0.18), (0.18, 0.72), (0.88, 0.85)])
    fn = font(MONO, int(W * (0.050 if vertical else 0.030)))
    pins = []
    for k, note in enumerate(notes[:3]):
        nx, ny = int(spots[k][0] * W), int(spots[k][1] * H)
        tw = int(dr.textlength(note, font=fn))
        card = Image.new("RGBA", (tw + 70, int(fn.size * 2.1)), (255, 246, 170, 255))
        cd = ImageDraw.Draw(card)
        for yl in range(int(fn.size * 0.55), card.height, int(fn.size * 0.5)):
            cd.line([(0, yl), (card.width, yl)], fill=(150, 180, 220, 120), width=2)
        cd.line([(0, int(fn.size * 0.35)), (card.width, int(fn.size * 0.35))], fill=(230, 80, 80, 160), width=2)
        cd.text((35, int(fn.size * 0.5)), note, font=fn, fill=(25, 25, 60))
        card = card.rotate([4, -5, 3][k], expand=True, resample=Image.BICUBIC)
        bd.alpha_composite(card, (nx - card.width // 2, ny - card.height // 2))
        pins.append((nx, ny - card.height // 2 + 22))
    for p in pins:
        _string(dr, top_pin, p)
    _pin(dr, *top_pin)
    for p in pins:
        _pin(dr, *p, 13)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bd.convert("RGB").save(out, quality=92)
    if os.path.exists(path + ".credit"):
        open(out + ".credit", "w").write(open(path + ".credit").read())
    return out


# ---------------------------------------------------------------- sounds

def _write(path, a, sr=48000):
    a = np.clip(a / (np.abs(a).max() + 1e-9) * 0.7, -1, 1)
    st = np.stack([a, a], 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((st * 32767).astype("<i2").tobytes())


def ensure_sfx(sfx_dir):
    """stamp.wav (rubber-stamp thump + paper slap) and case.wav (the series sting: typewriter clacks into a
    low two-note "dun-DUN"), synthesized; written once."""
    sr = 48000
    rng = np.random.default_rng(11)
    p = os.path.join(sfx_dir, "stamp.wav")
    if not os.path.exists(p):
        n = int(0.45 * sr)
        t = np.arange(n) / sr
        thump = np.sin(2 * np.pi * (70 + 90 * np.exp(-t * 30)) * t) * np.exp(-t * 16)
        slap = rng.standard_normal(n) * np.exp(-t * 60)
        slap = np.convolve(slap, np.ones(6) / 6, "same")
        _write(p, thump * 0.9 + slap * 0.6)
    p = os.path.join(sfx_dir, "case.wav")
    if not os.path.exists(p):
        n = int(1.5 * sr)
        t = np.arange(n) / sr
        a = np.zeros(n)
        for k, t0 in enumerate((0.0, 0.09, 0.17)):   # three typewriter clacks
            i = int(t0 * sr)
            m = int(0.04 * sr)
            a[i:i + m] += rng.standard_normal(m) * np.exp(-np.arange(m) / (sr * 0.004)) * 0.5
        for t0, f, d in ((0.32, 98.0, 0.35), (0.62, 92.5, 0.9)):   # dun-DUN (G2 then F#2)
            i = int(t0 * sr)
            m = int(d * sr)
            tt = np.arange(m) / sr
            tone = sum(np.sin(2 * np.pi * f * h * tt) / h for h in (1, 2, 3, 4, 5)) * np.exp(-tt * (3.5 / d))
            a[i:i + m] += tone[:n - i] * (0.7 if t0 < 0.5 else 1.0)
        _write(p, a)
