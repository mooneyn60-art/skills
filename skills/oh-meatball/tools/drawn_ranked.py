#!/usr/bin/env python3
"""16:9 "House Bugs Ranked" flagship long-form (TASKS [MEATBALL] FLAGSHIP LONG-FORM #1, LONG-FORM ANIMATION FIXES,
QUALITY FIRST). A 2 AM mystery: six suspects, one room each, every bug ranked on a four-row tier board
(HARMLESS / ANNOYING / GROSS / GET OUT). Format layer on top of tools/drawn_dontsquish.py (1920x1080 renderer,
music envelope, chapter/stamp actors) and tools/drawn.py; the v3 vertical look (drawn_cine: push/punch, BUG CAM,
SECURITY CAM, BUG ID card, freak-out hair, sound hits) is re-done here for 16:9.

  build OUTLINE.json SPEC.json        outline -> spec (every `say` kept, ids s<seg>.l<line>, a shot per line from
                                      SHOTS below; a shot edited in the spec with "_keep": true survives a rebuild)
  render SPEC.json OUT.mp4 [--lines A-B] [--work DIR]
  linesheet SPEC.json OUT.jpg [--only ids] [--frac 0.6]    one frame per line, tiled (part sheets of 30)
  check SPEC.json                     plan only: runtime, longest hold between cuts/moves, Meatball sizes
  voice SPEC.json                     voice every line now

Voice: one mp3 per line cached by sha1(text, voice, rate, pitch) in episodes/longform-house-bugs-ranked-v3/
.voice-cache; each line uses its own outline rate/pitch (else the outline's base), so a fact-check fix re-voices
only the changed line. Captions always use `say` (`tts` = a pronunciation respelling).

Screen layer (drawn after the world, before the captions; beat key "rk"):
  suspect   the "SUSPECT n OF 6" re-hook slam (1.5 s, full width, sting + hit)
  idcard    the BUG ID card (right half): name + up to 3 sourced rows from the outline cards, the new row slides in
  tier      the full-screen tier board: HARMLESS / ANNOYING / GROSS / GET OUT, each bug's drawn icon in its row;
            the line's new bug drops in (slam + shake); "sil": the cold open's six dark silhouettes
  cam       BUG CAM (magnifier ring), SPIDER CAM (eight-eye vignette), SECURITY CAM (green night vision, REC,
            timestamp): an interrupt window inside a line
World layer: v3 light (lamp pools on the bug and on Meatball, or a flashlight cone; a bright subject, the room
never below ~45 % dark), the freak-out hair (beat key "freak"), the rk_photo / rk_scene props below.
"""
import copy
import hashlib
import json
import math
import os
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import drawn_dontsquish as ds  # noqa: E402  (1920x1080 renderer, music envelope, ds_* actors)
import drawn_treecheck  # noqa: E402,F401  (tc_* actors and scenes: counters, cork, props)
import drawn_catlife  # noqa: E402,F401  (cl_* actors: calendar, clock)
import drawn  # noqa: E402
import drawn_keepkill as kk  # noqa: E402
import cairo  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402
from drawn_kit import OUT, BG_OUT, PAL, ease, back_out, flat, hexc, ink, p_ellipse, p_poly, p_rrect, shape, src, stroke  # noqa: E402

W, H = 1920, 1080
ROOT = os.path.dirname(HERE)
EP = os.path.join(ROOT, "episodes", "longform-house-bugs-ranked-v3")
CACHE = os.path.join(EP, ".voice-cache")
FONT = drawn.FONT
YEL, RED, GREEN = "#ffd34d", "#e5383b", "#3fb950"
TIERS = ["HARMLESS", "ANNOYING", "GROSS", "GET OUT"]
TCOL = {"HARMLESS": "#3fb950", "ANNOYING": "#ffd34d", "GROSS": "#ff9f43", "GET OUT": "#e5383b"}
TTS = {}   # pronunciation respellings (captions always use say)
drawn.SFX_MAX, drawn.SFX_GAP = 3, 0.35   # the re-hook card needs its sting and its hit

# ================================================================================================ bugs

BUGS = {   # name -> actor type, scale for a wide two-shot, body width / height at s = 1 (world px), label
    "silverfish": ("sp.silverfish", 0.62, 1150, 260, "SILVERFISH"),
    "mite": ("sp.dust_mite", 0.55, 1100, 480, "DUST MITE"),
    "spider": ("cellar_spider", 2.6, 260, 300, "HOUSE SPIDER"),
    "centipede": ("sp.house_centipede", 0.5, 1900, 620, "HOUSE CENTIPEDE"),
    "roach": ("sp.roach", 0.72, 850, 360, "GERMAN COCKROACH"),
    "bedbug": ("sp.bed_bug", 1.2, 560, 240, "BED BUG"),
}
ORDER = ["silverfish", "mite", "spider", "centipede", "roach", "bedbug"]
RANK = {"silverfish": "ANNOYING", "mite": "ANNOYING", "spider": "ANNOYING", "centipede": "ANNOYING",
        "roach": "GROSS", "bedbug": "GET OUT"}

# ================================================================================================ icons (PIL)

_ICON = {}


def icon(kind, w, h, sil=False, p=None):
    """A drawn actor rendered into a w x h RGBA PIL image (fit to the box), or a dark silhouette of it."""
    key = (kind, w, h, sil, json.dumps(p or {}))
    if key in _ICON:
        return _ICON[key]
    typ, _, bw, bh, _ = BUGS.get(kind, (kind, 1, 600, 400, ""))
    fn = drawn.ACTORS[typ]
    S = 1200
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, S * 2, S)
    ctx = cairo.Context(surf)
    k = min(1.7 * S / bw, 0.75 * S / max(bh, 1), 3.0)
    ctx.translate(S, S * 0.82)
    ctx.scale(k, k)
    fn(ctx, 0.4, dict({"mood": "calm", "look": [0.6, 0.2]}, **(p or {})))
    surf.flush()
    a = np.ndarray((S, S * 2, 4), np.uint8, surf.get_data()).copy()
    al = a[..., 3]
    ys, xs = np.where(al > 8)
    if not len(xs):
        im = Image.new("RGBA", (w, h))
    else:
        a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        alf = a[..., 3:4].astype(np.float32)
        rgb = np.where(alf > 0, a[..., [2, 1, 0]].astype(np.float32) * 255 / np.maximum(alf, 1), 0)
        if sil:
            rgb = rgb * 0 + np.array([22, 20, 34], np.float32)
        im = Image.fromarray(np.concatenate([np.clip(rgb, 0, 255), alf], -1).astype(np.uint8), "RGBA")
        sc = min(w / im.width, h / im.height)
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    _ICON[key] = im
    return im


_TXT = {}


def txt(text, px, color="#ffffff", stroke_w=None, plate=None):
    key = (text, px, color, stroke_w, plate)
    if key not in _TXT:
        f = ImageFont.truetype(FONT, px)
        sw = max(4, px // 12) if stroke_w is None else stroke_w
        d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
        x0, y0, x1, y1 = d.textbbox((0, 0), text, font=f, stroke_width=sw)
        pad = (34, 16) if plate else (4, 4)
        im = Image.new("RGBA", (x1 - x0 + 2 * pad[0], y1 - y0 + 2 * pad[1]), (0, 0, 0, 0))
        dr = ImageDraw.Draw(im)
        if plate:
            dr.rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=min(40, im.height // 2), fill=plate,
                                 outline=(255, 255, 255, 255), width=5)
        c = tuple(int(color.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)) + (255,)
        dr.text((pad[0] - x0, pad[1] - y0), text, font=f, fill=c, stroke_width=sw, stroke_fill=(10, 10, 10, 255))
        _TXT[key] = im
    return _TXT[key]


def _scaled(im, k):
    if abs(k - 1) < 1e-3:
        return im
    return im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.BILINEAR)


def _dim(arr, a):
    if a > 0.001:
        arr[..., :3] = (arr[..., :3].astype(np.float32) * (1 - a)).astype(np.uint8)


# ================================================================================================ screen overlays

def ov_suspect(arr, b, t, o):
    """SUSPECT n OF 6: a dark band slams in, huge yellow words, a red bar; 1.5 s."""
    a = drawn.at_time(b["words"], o.get("at", 0.0))
    v = t - a
    dur = o.get("dur", 1.5)
    if not 0 <= v < dur:
        return
    out = min(1.0, max(0.0, (dur - v) / 0.18))
    _dim(arr, 0.45 * out)
    im = txt(o["text"], 210, YEL, 12)
    k = 1.0 + 0.9 * (1 - ease(min(1.0, v / 0.16)))
    band = Image.new("RGBA", (W, int(im.height + 120)), (14, 12, 22, int(235 * out)))
    ImageDraw.Draw(band).rectangle((0, band.height - 18, W, band.height), fill=(229, 56, 59, int(255 * out)))
    drawn.paste(arr, band, W // 2 - int(W * (1 - ease(min(1.0, v / 0.12)))), 470)
    if o.get("kicker"):
        drawn.paste(arr, txt(o["kicker"], 70, "#ffffff"), W // 2, 470 - im.height // 2 - 20)
    im2 = _scaled(im, k)
    if out < 1:
        im2 = im2.copy()
        im2.putalpha(Image.eval(im2.getchannel("A"), lambda x: int(x * out)))
    drawn.paste(arr, im2, W // 2, 485)


_IDC = {}


def idcard_img(name, rows, kind):
    key = (name, tuple(rows), kind)
    if key in _IDC:
        return _IDC[key]
    Wc = 860
    fN = ImageFont.truetype(FONT, 92 if len(name) < 14 else 74)
    fR = ImageFont.truetype(FONT, 52)
    fH = ImageFont.truetype(FONT, 46)
    hh, nh, ih, rh = 80, 120, 200, 86
    # rows wrap at the card width
    lines = []
    for r in rows:
        words, cur = r.split(), ""
        out = []
        for w_ in words:
            test = (cur + " " + w_).strip()
            if fR.getlength(test) > Wc - 130 and cur:
                out.append(cur)
                cur = w_
            else:
                cur = test
        out.append(cur)
        lines.append(out)
    Hc = hh + nh + ih + sum(rh + 58 * (len(x) - 1) for x in lines) + 30
    im = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle((0, 0, Wc - 1, Hc - 1), radius=34, fill=(20, 24, 38, 242), outline=(255, 255, 255, 255), width=6)
    dr.rounded_rectangle((6, 6, Wc - 7, hh), radius=28, fill=(255, 211, 77, 255))
    dr.rectangle((6, hh - 26, Wc - 7, hh), fill=(255, 211, 77, 255))
    dr.text((30, 14), "BUG ID", font=fH, fill=(20, 20, 20, 255))
    dr.text((Wc - 330, 14), "MEATBALL MYTHS", font=fH, fill=(20, 20, 20, 255))
    dr.text((30, hh + 10), name, font=fN, fill=(255, 255, 255, 255))
    ic = icon(kind, Wc - 120, ih - 20)
    dr.rounded_rectangle((30, hh + nh - 6, Wc - 30, hh + nh + ih - 14), radius=20, fill=(48, 56, 80, 255))
    im.alpha_composite(ic, ((Wc - ic.width) // 2, hh + nh + (ih - 20 - ic.height) // 2))
    y = hh + nh + ih
    tops = []
    for ls in lines:
        tops.append(y)
        dr.rounded_rectangle((30, y + 24, 62, y + 56), radius=7, fill=(255, 211, 77, 255))
        for j, ln in enumerate(ls):
            dr.text((84, y + 4 + 58 * j), ln, font=fR, fill=(255, 255, 255, 255))
        y += rh + 58 * (len(ls) - 1)
    _IDC[key] = (im, tops)
    return _IDC[key]


def ov_idcard(arr, b, t, o):
    """The BUG ID card on one side; rows[:n] shown, row n-1 slides in at `at` (if new)."""
    a = drawn.at_time(b["words"], o.get("at", "15%"))
    v = t - a
    rows = o["rows"]
    n = o.get("n", len(rows))
    new = o.get("new", True)
    show = n if (v >= 0 or not new) else n - 1
    if show <= 0 and v < 0:
        if o.get("card_in", True) and n == 1:
            return
    im, tops = idcard_img(o["name"], rows[:max(show, 0)] if show > 0 else [], o["kind"])
    first = o.get("first", False)   # the card itself slides in
    cx = o.get("x", 1430)
    cy = o.get("y", 470)
    t_in = drawn.at_time(b["words"], o.get("in", 0.0))
    u = min(1.0, max(0.0, (t - t_in) / 0.3)) if first else 1.0
    if first and t < t_in:
        return
    end = o.get("out")
    if end is not None:
        te = drawn.at_time(b["words"], end)
        if t > te + 0.25:
            return
        if t > te:
            u = min(u, 1 - (t - te) / 0.25)
    dx = int((1 - ease(u)) * 900)
    drawn.paste(arr, im, cx + dx, cy - 60 + im.height // 2 - 300 + 300)
    if new and 0 <= v < 0.5 and show == n:   # flash on the new row
        y = cy - 60 + tops[n - 1] + 20
        q = 1 - v / 0.5
        flash = Image.new("RGBA", (im.width - 40, 70), (255, 211, 77, int(110 * q)))
        drawn.paste(arr, flash, cx + dx, y + 20)


def _tier_layout():
    top, rh, lw = 70, 205, 440
    return top, rh, lw


def ov_tier(arr, b, t, o):
    """The full-screen tier board. o: placed [[bug, tier], ...] already there, drop [bug, tier] (lands at `at`),
    sil (six silhouettes waiting under the board), pulse [tier, ...] (rows that pulse), mb_slot (Meatball in HARMLESS)."""
    top, rh, lw = _tier_layout()
    ton = drawn.at_time(b["words"], o.get("in", 0.0))
    if t < ton:
        return
    u_in = min(1.0, (t - ton) / 0.25) if o.get("slide", True) else 1.0
    toff = drawn.at_time(b["words"], o["off"]) if o.get("off") is not None else None
    if toff is not None and t > toff:
        u_in = max(0.0, 1 - (t - toff) / 0.25)
        if u_in <= 0:
            return
    dy = int((1 - ease(u_in)) * -1100)
    if o.get("full", True):
        bg = np.array([40, 26, 20], np.uint8)   # BGR (dark navy)
        yb = max(0, dy + 0)
        arr[yb:, :, :3] = (arr[yb:, :, :3] * (1 - ease(u_in)) * 0.15 + bg * (1 - (1 - ease(u_in)) * 0.15)).astype(np.uint8) \
            if u_in < 1 else bg
    sil = o.get("sil")
    nrows = 4
    for i, tname in enumerate(TIERS):
        y0 = top + i * rh + dy
        col = hexc(TCOL[tname])
        lab = Image.new("RGBA", (lw, rh - 14), tuple(int(c * 255) for c in col) + (255,))
        ImageDraw.Draw(lab).rounded_rectangle((0, 0, lw - 1, rh - 15), radius=24, outline=(15, 15, 15, 255), width=6)
        pul = 0.0
        for pt in o.get("pulse", []):
            tt, at = pt if isinstance(pt, list) else (pt, "0%")
            if tt == tname:
                v = t - drawn.at_time(b["words"], at)
                if 0 <= v < 1.2:
                    pul = math.sin(v / 1.2 * math.pi)
        tim = txt(tname, 92 if len(tname) > 6 else 104, "#1a1a1a", 0)
        lab.alpha_composite(tim, ((lw - tim.width) // 2, (rh - 14 - tim.height) // 2))
        lab = _scaled(lab, 1 + 0.08 * pul)
        drawn.paste(arr, lab, 40 + lw // 2, y0 + rh // 2)
        row = Image.new("RGBA", (W - lw - 100, rh - 14), (255, 255, 255, int(40 + 60 * pul)))
        ImageDraw.Draw(row).rounded_rectangle((0, 0, row.width - 1, rh - 15), radius=24, outline=(255, 255, 255, 140), width=4)
        drawn.paste(arr, row, 60 + lw + row.width // 2, y0 + rh // 2)
    slots = {k: 0 for k in TIERS}
    placed = [list(x) for x in o.get("placed", [])]
    items = placed + ([list(o["drop"])] if o.get("drop") else [])
    for j, (bug, tname) in enumerate(items):
        i = TIERS.index(tname)
        k = slots[tname]
        slots[tname] += 1
        cx = 60 + lw + 190 + k * 330
        cy = top + i * rh + rh // 2 + dy
        im = icon(bug, 300, rh - 40)
        shake = 0
        if o.get("drop") and j == len(items) - 1:
            a = drawn.at_time(b["words"], o.get("at", "55%"))
            v = t - a
            if v < -0.35:
                continue
            if v < 0:   # falling in from above, growing
                q = (v + 0.35) / 0.35
                cy = int(-200 + (cy + 200) * q * q)
                im = _scaled(im, 1.6 - 0.6 * q)
            elif v < 0.5:
                q = v / 0.5
                im = _scaled(im, 1 + 0.25 * math.sin(q * math.pi) * (1 - q))
                shake = int(16 * (1 - q) * math.sin(v * 80))
            name = txt(BUGS[bug][4], 44, "#ffffff")
            if v > 0.15:
                drawn.paste(arr, name, cx, cy + rh // 2 - 34)
        else:
            drawn.paste(arr, txt(BUGS[bug][4], 40, "#ffffff"), cx, cy + rh // 2 - 34)
        for pt in o.get("shake", []):
            if pt[0] == bug:
                v = t - drawn.at_time(b["words"], pt[1])
                if 0 <= v < 1.0:
                    shake = int(14 * math.sin(v * 60) * (1 - v))
        drawn.paste(arr, im, cx + shake, cy - 18)
    if o.get("mb_slot"):
        a = drawn.at_time(b["words"], o["mb_slot"])
        if t >= a:
            q = min(1.0, (t - a) / 0.4)
            mbim = _mb_icon()
            drawn.paste(arr, _scaled(mbim, 0.6 + 0.4 * back_out(q)), 60 + lw + 190, top + rh // 2 + dy - 6)
    if sil:   # cold open: six suspects in silhouette, under the board, twitching as the camera passes
        n_on = o.get("sil_n", 6)
        for j, bug in enumerate(ORDER[:n_on]):
            cx = 230 + j * 292
            cy = 930 + dy
            ph = drawn.at_time(b["words"], o.get("sil_at", "0%")) + j * 0.25
            v = t - ph
            if v < 0:
                continue
            tw = 8 * math.sin(t * 30 + j) * max(0.0, 1 - abs(v - 0.3) / 0.3) if v < 0.6 else 0
            im = icon(bug, 260, 160, sil=True)
            plate = Image.new("RGBA", (280, 190), (230, 220, 200, 255))
            ImageDraw.Draw(plate).rounded_rectangle((0, 0, 279, 189), radius=18, outline=(15, 15, 15, 255), width=5)
            drawn.paste(arr, plate, cx, cy)
            drawn.paste(arr, im, cx + int(tw), cy + 6)
            drawn.paste(arr, txt("?", 70, RED), cx + 110, cy - 70)


_MBI = {}


def _mb_icon():
    if "m" not in _MBI:
        import mascot
        st = mascot.states("laugh", [], 0.5, 30, seed=1, enter=False, size=400)[5]
        got = mascot.render(st, 230, 2, (0, 0), (600, 600))
        im = got[0] if got else Image.new("RGBA", (10, 10))
        bb = im.getbbox()
        _MBI["m"] = im.crop(bb) if bb else im
    return _MBI["m"]


_MASK = {}


def _mask(name, fn):
    if name not in _MASK:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        _MASK[name] = fn(yy, xx).astype(np.float32)
    return _MASK[name]


def ov_cam(arr, b, t, o, T):
    a = drawn.at_time(b["words"], o.get("at", 0.0))
    z = drawn.at_time(b["words"], o["to"]) if o.get("to") is not None else b["dur"] + 1
    if not a <= t < z:
        return
    kind = o["kind"]
    if kind == "seccam":
        f = arr[..., :3].astype(np.float32)
        lum = 0.11 * f[..., 0] + 0.59 * f[..., 1] + 0.30 * f[..., 2]
        lum = 255 * (lum / 255) ** 0.6
        rng = np.random.default_rng(int(T * 30))
        lum = lum + rng.normal(0, 14, lum.shape).astype(np.float32)
        vig = _mask("vig", lambda yy, xx: 1 - 0.5 * np.clip((np.hypot((xx - 960) / 960, (yy - 540) / 540) - 0.5) / 0.7, 0, 1))
        scan = _mask("scan", lambda yy, xx: np.where((yy.astype(np.int32) // 3) % 2 == 0, 1.0, 0.84))
        lum = lum * vig * scan
        arr[..., 0] = np.clip(lum * 0.30, 0, 255).astype(np.uint8)
        arr[..., 1] = np.clip(lum * 1.0 + 12, 0, 255).astype(np.uint8)
        arr[..., 2] = np.clip(lum * 0.42, 0, 255).astype(np.uint8)
        sec = 2 * 3600 + 14 * 60 + int(t - a)
        drawn.paste(arr, txt("SECURITY CAM", 96, "#dcffdc"), 360, 110)
        drawn.paste(arr, txt("BASEMENT  %d:%02d:%02d AM" % (sec // 3600, sec // 60 % 60, sec % 60), 64, "#dcffdc"), 1450, 110)
        if int(T * 2) % 2 == 0:
            drawn.paste(arr, txt("REC", 72, "#ff4646"), 1780, 240)
            im = Image.new("RGBA", (50, 50))
            ImageDraw.Draw(im).ellipse((0, 0, 49, 49), fill=(255, 70, 70, 255))
            drawn.paste(arr, im, 1690, 240)
    elif kind in ("bugcam", "spidercam", "mitecam"):
        cx, cy, r = 960, 520, 470
        if kind == "spidercam":   # eight eyes: a cluster of round lenses
            m = _mask("spi", lambda yy, xx: np.clip(np.minimum.reduce([np.hypot(xx - ex, yy - ey) - er for ex, ey, er in
                      ((700, 520, 330), (1220, 520, 330), (430, 300, 120), (1490, 300, 120), (380, 760, 100), (1540, 760, 100),
                       (860, 170, 90), (1060, 170, 90))]) / 14, 0, 1) * 0.92)
        else:
            m = _mask("ring", lambda yy, xx: np.clip((np.hypot(xx - cx, yy - cy) - r) / 16, 0, 1) * 0.9)
        arr[..., :3] = (arr[..., :3] * (1 - m[..., None])).astype(np.uint8)
        if kind != "spidercam":
            ring = Image.new("RGBA", (2 * r + 80, 2 * r + 80), (0, 0, 0, 0))
            d = ImageDraw.Draw(ring)
            d.ellipse((10, 10, 2 * r + 70, 2 * r + 70), outline=(20, 20, 20, 255), width=50)
            d.ellipse((18, 18, 2 * r + 62, 2 * r + 62), outline=(150, 160, 175, 255), width=34)
            d.arc((90, 90, 2 * r - 10, 2 * r - 10), 200, 245, fill=(255, 255, 255, 140), width=22)
            drawn.paste(arr, ring, cx, cy)
        lab = {"bugcam": "BUG CAM", "spidercam": "SPIDER CAM", "mitecam": "MICROSCOPE CAM"}[kind]
        drawn.paste(arr, txt(lab, 96, YEL, plate=(18, 22, 40, 235)), 300 if kind != "spidercam" else 960, 1000 - 70 if kind != "spidercam" else 960)
    v = t - a
    if v < 2 / 30:
        arr[..., :3] = ((arr[..., :3].astype(np.uint16) + 255) // 2).astype(np.uint8)


def ov_big(arr, b, t, o):
    """A big bold word card (COMMENT IT, GET OUT!, CASE CLOSED style) with a pop."""
    a = drawn.at_time(b["words"], o.get("at", "10%"))
    v = t - a
    if v < 0:
        return
    z = o.get("to")
    if z is not None and t > drawn.at_time(b["words"], z):
        return
    rows = o["rows"]
    k = back_out(min(1.0, v / 0.25))
    y = o.get("y", 300)
    if o.get("dim"):
        _dim(arr, o["dim"] * min(1.0, v / 0.2))
    for i, (s_, px, col) in enumerate(rows):
        im = _scaled(txt(s_, px, col, max(8, px // 11)), max(0.05, k))
        drawn.paste(arr, im, o.get("x", W // 2), y)
        y += int(px * 1.25)


def ov_end(arr, b, t, o):
    pass


OVS = {"suspect": ov_suspect, "idcard": ov_idcard, "tier": ov_tier, "big": ov_big}


def screen_layer(arr, T):
    G = drawn.G
    beats = G.get("beats") or []
    if not beats:
        return
    bi = max(i for i, b in enumerate(beats) if b["t0"] <= T + 1e-9)
    b = beats[bi]
    t = T - b["t0"]
    for o in b.get("rk", []):
        if o["type"] == "cam":
            ov_cam(arr, b, t, o, T)
    for o in b.get("rk", []):
        if o["type"] in OVS:
            OVS[o["type"]](arr, b, t, o)


_orig_counter = drawn.draw_counter


def _draw_counter(arr, T):
    screen_layer(arr, T)
    _orig_counter(arr, T)


drawn.draw_counter = _draw_counter

# ================================================================================================ world layer: light + hair

_orig_world = drawn.draw_world


def _scr(cam, x, y):
    return drawn.world_to_screen(cam, x, y)


def _act_pos(b, idn, t):
    a = b["actors"].get(idn)
    if a is None:
        return None
    x, y, s, *_ = drawn.track(a.get("pos", (0, 0)), a.get("moves", []), b["words"], t, a.get("s", 1.0), a.get("rot", 0.0))
    return x, y, s, a


def light_pass(ctx, cam, b, t, T):
    lt = b.get("light")
    if not lt or lt == "off":
        return
    lt = lt if isinstance(lt, dict) else {"kind": lt}
    kind = lt["kind"]
    dark = lt.get("dark", 0.55 if kind == "lamp" else 0.72)
    pools = []
    hb = _act_pos(b, "hero", t)
    if hb:
        x, y, s, a = hb
        typ = a.get("type")
        bw, bh = next(((v[2], v[3]) for v in BUGS.values() if v[0] == typ), (500, 300))
        hx, hy = _scr(cam, x, y - 0.45 * bh * s)
        pools.append((hx, hy, max(260, 0.75 * bw * s * cam[2])))
    for idn in lt.get("also", []):
        p = _act_pos(b, idn, t)
        if p:
            hx, hy = _scr(cam, p[0], p[1] - 100 * p[2])
            pools.append((hx, hy, 360 * cam[2]))
    mb = b["mb"]
    if not mb.get("hidden"):
        x, y, size, *_ = drawn.track(mb["pos"], mb["moves"], b["words"], t, mb["size"])
        mx, my = _scr(cam, x, y - 0.5 * size)
        pools.append((mx, my, 0.85 * size * cam[2] + 80))
    ctx.identity_matrix()
    ctx.push_group()
    ctx.set_source_rgba(0.02, 0.03, 0.09, dark)
    ctx.paint()
    ctx.set_operator(cairo.OPERATOR_DEST_OUT)
    if kind == "flashlight":
        f = int(round(T * 30))
        flick = 1.0 if (t > 0.12 or not lt.get("snap")) else (0.0 if t < 1 / 30 else 0.7)
        tx, ty = pools[0][:2] if pools else (W * 0.6, H * 0.5)
        sx, sy = lt.get("from", (-120 + 25 * math.sin(T * 1.1), H + 160))
        ang = math.atan2(ty - sy, tx - sx)
        dist = max(1.0, math.hypot(tx - sx, ty - sy))
        nx, ny = -math.sin(ang), math.cos(ang)
        far = dist + 900
        for wk, al in ((1.5, 0.25), (1.15, 0.35), (0.85, 0.45), (0.6, 0.55)):
            w = lt.get("w", 260) * wk
            ex, ey = sx + far * math.cos(ang), sy + far * math.sin(ang)
            ctx.move_to(sx, sy)
            ctx.line_to(ex + nx * w * far / dist, ey + ny * w * far / dist)
            ctx.line_to(ex - nx * w * far / dist, ey - ny * w * far / dist)
            ctx.close_path()
            ctx.set_source_rgba(0, 0, 0, al * flick)
            ctx.fill()
        g = cairo.RadialGradient(tx, ty, 0, tx, ty, lt.get("spot", 520))
        g.add_color_stop_rgba(0, 0, 0, 0, 0.95 * flick)
        g.add_color_stop_rgba(1, 0, 0, 0, 0)
        ctx.set_source(g)
        ctx.paint()
        pools = pools[1:]
    for px, py, r in pools:
        g = cairo.RadialGradient(px, py, 0, px, py, r)
        g.add_color_stop_rgba(0, 0, 0, 0, 0.95)
        g.add_color_stop_rgba(0.6, 0, 0, 0, 0.7)
        g.add_color_stop_rgba(1, 0, 0, 0, 0)
        ctx.set_source(g)
        ctx.paint()
    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.pop_group_to_source()
    ctx.paint()
    if kind == "lamp" and pools:   # warm spill over the subject
        px, py, r = pools[0]
        g = cairo.RadialGradient(px, py - 200, 0, px, py - 200, 900)
        g.add_color_stop_rgba(0, 1.0, 0.86, 0.55, 0.12)
        g.add_color_stop_rgba(1, 1.0, 0.86, 0.55, 0.0)
        ctx.set_source(g)
        ctx.paint()


def hair_pass(ctx, cam, b, t):
    fa = b.get("freak")
    if fa is None or b["mb"].get("hidden"):
        return
    for at in (fa if isinstance(fa, list) else [fa]):
        a = drawn.at_time(b["words"], at)
        v = t - a
        if not 0 <= v < 1.8:
            continue
        mb = b["mb"]
        x, y, size, *_ = drawn.track(mb["pos"], mb["moves"], b["words"], t, mb["size"])
        sh = mb.get("shake") or 0.0
        jx = sh * 10 * math.sin((b["t0"] + t) * 57)
        fx, fy = _scr(cam, x + jx, y)
        k = size * cam[2] / 1000
        hx, hy = fx, fy - 700 * k
        q = ease(min(1.0, v / 0.1)) * (1.0 if v < 1.5 else 1 - (v - 1.5) / 0.3)
        ctx.identity_matrix()
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for lw, col in ((22 * k, (0.08, 0.06, 0.05)), (11 * k, (0.55, 0.36, 0.2))):
            ctx.set_line_width(lw)
            ctx.set_source_rgb(*col)
            for j in range(9):
                ang = math.radians(-90 + (j - 4) * 13)
                wob = 12 * k * math.sin((b["t0"] + t) * 60 + j)
                r0, r1 = 150 * k, 150 * k + 260 * k * q
                x0, y0 = hx + r0 * math.cos(ang), hy + r0 * math.sin(ang)
                x1, y1 = hx + r1 * math.cos(ang) + wob, hy + r1 * math.sin(ang)
                ctx.move_to(x0, y0)
                ctx.line_to((x0 + x1) / 2 + 20 * k, (y0 + y1) / 2)
                ctx.line_to(x1, y1)
            ctx.stroke()
        # eye-pop burst
        if v < 0.5:
            qq = ease(min(1.0, v / 0.12))
            ctx.set_source_rgb(0.08, 0.06, 0.05)
            ctx.set_line_width(14 * k)
            for j in range(10):
                ang = math.radians(-180 + j * 20)
                r0, r1 = 380 * k * (0.9 + 0.2 * qq), 380 * k * (1.0 + 0.5 * qq)
                ctx.move_to(hx + r0 * math.cos(ang), hy + 120 * k + r0 * math.sin(ang))
                ctx.line_to(hx + r1 * math.cos(ang), hy + 120 * k + r1 * math.sin(ang))
            ctx.stroke()


def _draw_world(ctx, cam, b, t, T, bi, rf, ins=None):
    rigs = drawn.G["rigs"]
    drawn.SCENES[b["scene"]](ctx, T, lambda d: drawn.set_layer(ctx, cam, d), b["scene_p"])
    acts = list(b["actors"].values())
    for a in [a for a in acts if not a.get("front")]:
        ctx.save()
        drawn.draw_actor(ctx, cam, a, b, t, b["words"])
        ctx.restore()
    ctx.identity_matrix()
    drawn.draw_meatball(ctx, cam, b, rigs[bi][rf], t)
    for a in [a for a in acts if a.get("front") and a.get("lit")]:   # world props in front of Meatball
        ctx.save()
        drawn.draw_actor(ctx, cam, a, b, t, b["words"])
        ctx.restore()
    light_pass(ctx, cam, b, t, T)
    hair_pass(ctx, cam, b, t)
    for a in [a for a in acts if a.get("front") and not a.get("lit")]:
        ctx.save()
        drawn.draw_actor(ctx, cam, a, b, t, b["words"])
        ctx.restore()


drawn.draw_world = _draw_world

# ================================================================================================ extra actors / scenes


def rk_photo(ctx, t, p):
    """A polaroid of a bug pinned to the case board; p: bug, on, tilt."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    s = back_out(min(1.0, on))
    ctx.save()
    ctx.scale(s, s)
    ctx.rotate(math.radians(p.get("tilt", -4)))
    shape(ctx, lambda c: p_rrect(c, -230, -230, 460, 470, 10), (0.97, 0.96, 0.92), OUT, (0.0, 0.12))
    flat(ctx, lambda c: c.rectangle(-200, -200, 400, 330), hexc("#2a3350"))
    ctx.restore()
    im = icon(p["bug"], 380, 300)
    surf, keep = drawn.pil_to_surface(im)
    ctx.save()
    ctx.scale(s, s)
    ctx.rotate(math.radians(p.get("tilt", -4)))
    ctx.set_source_surface(surf, -im.width / 2, -35 - im.height / 2)
    ctx.paint()
    lab = txt(BUGS[p["bug"]][4], 44, "#1a1a1a", 0)
    s2, k2 = drawn.pil_to_surface(lab)
    ctx.set_source_surface(s2, -lab.width / 2, 170 - lab.height / 2)
    ctx.paint()
    shape(ctx, lambda c: p_ellipse(c, 0, -228, 24, 24), hexc("#e5383b"), OUT * 0.6, None)
    ctx.restore()


def rk_roof(ctx, t, layer, p):
    """A roof at dawn: a pink-orange sky, a low sun, the shingled roof slope; roof ridge at y = 1180."""
    layer(0.6)
    g = cairo.LinearGradient(0, -600, 0, 1500)
    for u, c in ((0, "#3b3f7a"), (0.45, "#e98a8a"), (0.75, "#ffc27a"), (1, "#ffe2a8")):
        g.add_color_stop_rgb(u, *hexc(c))
    ctx.rectangle(-3000, -3000, 8000, 8000)
    ctx.set_source(g)
    ctx.fill()
    flat(ctx, lambda c: p_ellipse(c, 1500, 1180, 200, 200), hexc("#fff1b8"))
    for k, (x, y) in enumerate(((-200, 1240), (600, 1260), (1300, 1250), (2100, 1240))):
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 520, 120), hexc("#4a5a7a"))
    layer(1.0)
    shape(ctx, lambda c: p_poly(c, [(-2500, 1350), (3500, 1350), (3500, 2600), (-2500, 2600)]), hexc("#7a3a30"), BG_OUT, None)
    for y in range(1400, 2600, 80):
        stroke(ctx, [(-2500, y), (3500, y)], 4, color=hexc("#5e2a22"))
    stroke(ctx, [(-2500, 1350), (3500, 1350)], 26, color=hexc("#4a221c"))


def rk_hall(ctx, t, layer, p):
    """An upstairs hallway at night: wallpaper, a door frame left, a framed picture, a skirting board; floor y = 1500."""
    layer(0.9)
    flat(ctx, lambda c: c.rectangle(-3000, -2000, 8000, 3600), hexc("#5d6a92"))
    for x in range(-3000, 5000, 130):
        flat(ctx, lambda c, x=x: c.rectangle(x, -2000, 50, 3600), hexc("#55618a"))
    shape(ctx, lambda c: c.rectangle(-520, 380, 420, 1120), hexc("#3a2a20"), BG_OUT, None)
    shape(ctx, lambda c: c.rectangle(-490, 410, 360, 1090), hexc("#22252f"), BG_OUT * 0.7, None)
    shape(ctx, lambda c: p_rrect(c, 1700, 520, 360, 280, 8), PAL["wood"], BG_OUT, None)
    flat(ctx, lambda c: c.rectangle(1730, 550, 300, 220), hexc("#6aa36f"))
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1440, 8000, 60), hexc("#e8e2d4"))
    stroke(ctx, [(-3000, 1440), (5000, 1440)], BG_OUT)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 800), hexc("#7a5a42"))
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)


def rk_garage(ctx, t, layer, p):
    """ds_shed with a concrete floor and a roll-up door panel (the garage); floor y = 1500."""
    drawn.SCENES["ds_shed"](ctx, t, layer, p)
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 900), hexc("#8d8d8a"))
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)
    for x in range(-3000, 5000, 420):
        stroke(ctx, [(x, 1500), (x - 160, 2400)], 3, color=hexc("#777"))


def rk_board_bg(ctx, t, layer, p):
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-4000, -4000, 9000, 9000), hexc(p.get("color", "#141a2e")))


drawn.ACTORS["rk_photo"] = rk_photo
drawn.SCENES.update(rk_roof=rk_roof, rk_hall=rk_hall, rk_garage=rk_garage, rk_board_bg=rk_board_bg)
