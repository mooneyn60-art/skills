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
drawn.SFX_MAX, drawn.SFX_GAP = 4, 0.3   # the re-hook card needs its sting and its hit

# ================================================================================================ bugs

BUGS = {   # name -> actor type, scale for a wide two-shot, body width / height at s = 1 (world px), label
    "silverfish": ("sp.silverfish", 0.62, 1150, 260, "SILVERFISH"),
    "mite": ("sp.dust_mite", 0.55, 1100, 480, "DUST MITE"),
    "spider": ("cellar_spider", 1.3, 760, -640, "HOUSE SPIDER"),
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
    k = min(1.7 * S / bw, 0.75 * S / max(abs(bh), 1), 3.0)
    ctx.translate(S, S * 0.82 if bh > 0 else -S * 0.12)
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
    top = o.get("top", 60)
    drawn.paste(arr, im, cx + dx, top + im.height // 2)
    if new and 0 <= v < 0.5 and show == n:   # flash on the new row
        y = top + tops[n - 1] + 20
        q = 1 - v / 0.5
        flash = Image.new("RGBA", (im.width - 40, 70), (255, 211, 77, int(110 * q)))
        drawn.paste(arr, flash, cx + dx, y + 20)


def _tier_layout(sil=False):
    return (40, 160, 440) if sil else (14, 214, 380)


def ov_tier(arr, b, t, o):
    """The full-screen tier board (Studio 11/17: big icons, one bug lands per beat with a hit, Meatball on screen).
    o: placed [[bug, tier], ...] already there; drops [[bug, tier, at], ...] each falls in at its own time (the old
    drop + at is one drop); sil (the cold open's six silhouettes); pulse [[tier, at]]; shake [[bug, at]]; mb_slot
    (Meatball lands in HARMLESS); mb (pose for the reaction bubble, default by the newest drop; False = none);
    in / off (the board pops on / off at these times)."""
    sil = bool(o.get("sil"))
    top, rh, lw = _tier_layout(sil)
    ton = drawn.at_time(b["words"], o.get("in", 0.0))
    if t < ton:
        return
    if o.get("off") is not None and t > drawn.at_time(b["words"], o["off"]):
        return
    if o.get("full", True):
        arr[..., :3] = np.array([40, 26, 20], np.uint8)   # BGR: dark navy
    rows = TIERS if not o.get("only_sil") else []
    for i, tname in enumerate(rows):
        y0 = top + i * rh
        col = hexc(TCOL[tname])
        pul = 0.0
        for pt in o.get("pulse", []):
            v = t - drawn.at_time(b["words"], pt[1])
            if pt[0] == tname and 0 <= v < 1.2:
                pul = math.sin(v / 1.2 * math.pi)
        lab = _tier_label(tname, lw, rh - 14, col)
        drawn.paste(arr, _scaled(lab, 1 + 0.08 * pul), 30 + lw // 2, y0 + rh // 2)
        drawn.paste(arr, _tier_row(W - lw - 70, rh - 14, int(40 + 70 * pul)), 50 + lw + (W - lw - 70) // 2, y0 + rh // 2)
    drops = [list(d) for d in o.get("drops", [])]
    if o.get("drop"):
        drops.append(list(o["drop"]) + [o.get("at", "90%")])
    slots = {k: 0 for k in TIERS}
    iw, ih, step = 340, rh - 46, 350
    items = [(bug, tn, None) for bug, tn in o.get("placed", [])] + [(d[0], d[1], d[2]) for d in drops]
    newest = None
    for bug, tname, at in items:
        i = TIERS.index(tname)
        k = slots[tname]
        slots[tname] += 1
        cx = 50 + lw + 30 + iw // 2 + k * step
        cy = top + i * rh + rh // 2 - 14
        im = icon(bug, iw, ih)
        shake = 0
        if at is not None:
            v = t - drawn.at_time(b["words"], at)
            if v < -0.3:
                continue
            newest = (bug, tname)
            if v < 0:   # falling in from above, big, then shrinking into its slot
                q = (v + 0.3) / 0.3
                cy = int(-260 + (cy + 260) * q * q)
                im = _scaled(im, 1.7 - 0.7 * q)
            elif v < 0.5:
                q = v / 0.5
                im = _scaled(im, 1 + 0.3 * math.sin(q * math.pi) * (1 - q))
                shake = int(18 * (1 - q) * math.sin(v * 80))
        for pt in o.get("shake", []):
            if pt[0] == bug:
                v = t - drawn.at_time(b["words"], pt[1])
                if 0 <= v < 1.0:
                    shake = int(16 * math.sin(v * 60) * (1 - v))
        drawn.paste(arr, im, cx + shake, cy)
        drawn.paste(arr, txt(BUGS[bug][4], 38, "#ffffff"), cx, top + i * rh + rh - 34)
    if o.get("mb_slot"):
        a = drawn.at_time(b["words"], o["mb_slot"])
        if t >= a:
            q = min(1.0, (t - a) / 0.4)
            drawn.paste(arr, _scaled(_mb_pose("laugh", 300), 0.6 + 0.4 * back_out(q)), 50 + lw + 30 + iw // 2, top + rh // 2)
    pose = o.get("mb")
    if pose is None:
        pose = {"GET OUT": "shock", "GROSS": "nervous", "ANNOYING": "shrug", "HARMLESS": "laugh"}[newest[1]] if newest else "think"
    if pose and not sil:   # Meatball's reaction bubble, bottom right (GROSS / GET OUT rows hold one bug at most)
        cx, cy, r = W - 250, H - 330, 225
        bub = Image.new("RGBA", (2 * r + 16, 2 * r + 16), (0, 0, 0, 0))
        d = ImageDraw.Draw(bub)
        d.ellipse((8, 8, 2 * r + 8, 2 * r + 8), fill=(255, 226, 150, 255), outline=(15, 15, 15, 255), width=10)
        mbim = _mb_bust(pose, 2 * r)
        bob = int(8 * math.sin(t * 7))
        m = Image.new("L", bub.size, 0)
        ImageDraw.Draw(m).ellipse((14, 14, 2 * r + 2, 2 * r + 2), fill=255)
        layer = Image.new("RGBA", bub.size, (0, 0, 0, 0))
        layer.alpha_composite(mbim, (max(0, (bub.width - mbim.width) // 2), 30 + bob))
        layer.putalpha(Image.fromarray(np.minimum(np.asarray(layer.getchannel("A")), np.asarray(m))))
        bub.alpha_composite(layer)
        drawn.paste(arr, bub, cx, cy)
    if sil:   # cold open: six suspects in silhouette under the board, twitching as they appear
        for j, bug in enumerate(ORDER):
            cx = 230 + j * 292
            cy = 830 if not o.get("only_sil") else 760
            v = t - (drawn.at_time(b["words"], o.get("sil_at", "0%")) + j * 0.25)
            if v < 0:
                continue
            tw = 8 * math.sin(t * 30 + j) * max(0.0, 1 - abs(v - 0.3) / 0.3) if v < 0.6 else 0
            plate = Image.new("RGBA", (280, 190), (230, 220, 200, 255))
            ImageDraw.Draw(plate).rounded_rectangle((0, 0, 279, 189), radius=18, outline=(15, 15, 15, 255), width=5)
            drawn.paste(arr, plate, cx, cy)
            drawn.paste(arr, icon(bug, 260, 160, sil=True), cx + int(tw), cy + 6)
            drawn.paste(arr, txt("?", 70, RED), cx + 110, cy - 70)


_TL = {}


def _tier_label(tname, w, h, col):
    key = (tname, w, h)
    if key not in _TL:
        lab = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(lab).rounded_rectangle((0, 0, w - 1, h - 1), radius=24, fill=tuple(int(c * 255) for c in col) + (255,),
                                              outline=(15, 15, 15, 255), width=6)
        tim = txt(tname, 88 if len(tname) > 6 else 100, "#1a1a1a", 0)
        lab.alpha_composite(tim, ((w - tim.width) // 2, (h - tim.height) // 2))
        _TL[key] = lab
    return _TL[key]


def _tier_row(w, h, a):
    key = ("row", w, h, a)
    if key not in _TL:
        row = Image.new("RGBA", (w, h), (255, 255, 255, a))
        ImageDraw.Draw(row).rounded_rectangle((0, 0, w - 1, h - 1), radius=24, outline=(255, 255, 255, 140), width=4)
        _TL[key] = row
    return _TL[key]


_MBP = {}


def _mb_bust(pose, size):
    """Meatball's head and shoulders, about `size` px tall, for the reaction bubble."""
    if ("bust", pose, size) not in _MBP:
        im = _mb_pose(pose, 900)
        im = im.crop((0, 0, im.width, int(im.height * 0.5)))
        k = size * 0.92 / im.height
        _MBP[("bust", pose, size)] = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
    return _MBP[("bust", pose, size)]


def _mb_pose(pose, px):
    if (pose, px) not in _MBP:
        import mascot
        st = mascot.states(pose, [(0.0, 0.3, "x")], 1.0, 30, seed=3, enter=False, size=px)[20]
        got = mascot.render(st, px, 2, (0, 0), (px * 2, px * 2))
        im = got[0] if got else Image.new("RGBA", (10, 10))
        bb = im.getbbox()
        _MBP[(pose, px)] = im.crop(bb) if bb else im
    return _MBP[(pose, px)]


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
        sec = o.get("clock", 2 * 3600 + 14 * 60) + int(t - a)
        ty = o.get("title_y", 110)
        drawn.paste(arr, txt(o.get("title", "SECURITY CAM"), o.get("title_px", 96), "#dcffdc"), o.get("title_x", 360), ty)
        drawn.paste(arr, txt("%s  %d:%02d:%02d AM" % (o.get("place", "BASEMENT"), sec // 3600, sec // 60 % 60, sec % 60), 64, "#dcffdc"), 1450, ty)
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
        drawn.paste(arr, txt(lab, 96, YEL, plate=(18, 22, 40, 235)), 300 if kind != "spidercam" else 960, 930 if kind != "spidercam" else 110)
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
    card = b.get("card")
    if card and any(o["type"] == "cam" for o in b.get("rk", [])) and t >= drawn.at_time(b["words"], card.get("at", 0.0)):
        im = drawn.card_img(card["rows"])   # the card stays readable over a BUG CAM / night-vision window
        drawn.paste(arr, im, card.get("x", W // 2), card.get("y", 760) + im.height // 2)
    for o in b.get("rk", []):
        if o["type"] in OVS:
            OVS[o["type"]](arr, b, t, o)
    for o in b.get("rk", []):
        if o["type"] == "zoom":
            ov_zoom(arr, b, t, o)


def ov_zoom(arr, b, t, o):
    """A camera move on the finished screen (boards are screen graphics): from [cx, cy, z] to [cx, cy, z]."""
    a = drawn.at_time(b["words"], o.get("at", 0.0))
    if o.get("until") is not None and t >= drawn.at_time(b["words"], o["until"]):
        return
    if t < a and o.get("wait"):
        return
    d = o.get("dur") or max(0.3, b["dur"] - a)
    u = min(1.0, max(0.0, (t - a) / d))
    u = u if o.get("linear") else ease(u)
    c = [x + (y - x) * u for x, y in zip(o["from"], o["to"])]
    z = max(1.0, c[2])
    if z <= 1.001:
        return
    w, h = W / z, H / z
    x0 = min(max(0.0, c[0] - w / 2), W - w)
    y0 = min(max(0.0, c[1] - h / 2), H - h)
    im = Image.frombuffer("RGBA", (W, H), arr.tobytes(), "raw", "RGBA", 0, 1)
    im = im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + w, y0 + h))
    arr[:] = np.asarray(im)


_orig_counter = drawn.draw_counter


def _draw_counter(arr, T):
    screen_layer(arr, T)
    _orig_counter(arr, T)


drawn.draw_counter = _draw_counter
_orig_frame_at = drawn.frame_at


def _frame_at(f):
    """Captions sit in the lower third (Studio 11/17: 2x size, bold, black outline); a beat may move them (cap_y)."""
    G = drawn.G
    beats = G.get("beats") or []
    if beats and G.get("cap_px"):
        T = f / G["fps"]
        b = beats[max(i for i, bb in enumerate(beats) if bb["t0"] <= T + 1e-9)]
        G.setdefault("cap_y0", G["cap_y"])
        G["cap_y"] = b.get("cap_y", G["cap_y0"])
    return _orig_frame_at(f)


drawn.frame_at = _frame_at

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
    if lt.get("off_at") is not None and t >= drawn.at_time(b["words"], lt["off_at"]):
        return
    dark = lt.get("dark", 0.42 if kind == "lamp" else 0.6)
    pools = []
    hb = _act_pos(b, "hero", t)
    if hb and hb[3].get("p", {}).get("hidden"):
        hb = None
    if lt.get("target"):
        hx, hy = _scr(cam, *lt["target"])
        pools.append((hx, hy, 420 * cam[2]))
    elif hb:
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


def _draw_prop(ctx, prop, hx, hy, k, t, beam=True):
    if prop in drawn_treecheck.MB_PROPS:
        return drawn_treecheck._draw_prop(ctx, prop, hx, hy, k, t)
    return drawn_treecheck._orig_draw_prop(ctx, prop, hx, hy, k, t, beam=beam)


drawn.draw_prop = _draw_prop

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
        stroke(ctx, [(x, 1500), (x - 160, 2400)], 3, color=hexc("#777777"))


def rk_board_bg(ctx, t, layer, p):
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-4000, -4000, 9000, 9000), hexc(p.get("color", "#141a2e")))


drawn.ACTORS["rk_photo"] = rk_photo
drawn.SCENES.update(rk_roof=rk_roof, rk_hall=rk_hall, rk_garage=rk_garage, rk_board_bg=rk_board_bg)


def rk_rope(ctx, t, p):
    """A timeline rope on the floor from 0 to p["w"], with posts at p["marks"]; origin = its left end."""
    w = p.get("w", 1400)
    stroke(ctx, [(0, 0), (w, 0)], 16, color=hexc("#c9a46a"))
    stroke(ctx, [(0, -6), (w, -6)], 4, color=hexc("#e8cf9c"))
    for x in p.get("marks", [0, w / 2, w]):
        shape(ctx, lambda c, x=x: p_rrect(c, x - 12, -90, 24, 100, 6), PAL["wood"], OUT * 0.7, None)


def rk_washer(ctx, t, p):
    """A front-load washer (or dryer, p dryer) 420 wide, feet at y 0; p spin (laundry turns), label, dial 0..1."""
    shape(ctx, lambda c: p_rrect(c, -210, -520, 420, 520, 24), (0.95, 0.96, 0.97), OUT, (0.05, 0.12))
    flat(ctx, lambda c: c.rectangle(-190, -500, 380, 80), hexc("#d5dae0"))
    ang = math.radians(-120 + 240 * p.get("dial", 0.5))
    shape(ctx, lambda c: p_ellipse(c, 120, -460, 30, 30), hexc("#2a2f3a"), OUT * 0.6, None)
    stroke(ctx, [(120, -460), (120 + 26 * math.cos(ang), -460 + 26 * math.sin(ang))], 6, color=(1, 0.8, 0.3))
    shape(ctx, lambda c: p_ellipse(c, 0, -230, 150, 150), hexc("#9aa4b0"), OUT, None)
    flat(ctx, lambda c: p_ellipse(c, 0, -230, 120, 120), hexc("#3d5f8a" if not p.get("dryer") else "#6b5048"))
    sp = t * p.get("spin", 4.0)
    for k, col in enumerate(("#e5383b", "#ffd34d", "#f2f2f2", "#3fb950")):
        a = sp + k * 1.57
        flat(ctx, lambda c, a=a: p_ellipse(c, 60 * math.cos(a), -230 + 60 * math.sin(a), 40, 26, a), hexc(col))
    if p.get("rider"):   # a bed bug riding the drum
        ctx.save()
        a = sp * 0.8
        ctx.translate(55 * math.cos(a), -230 + 55 * math.sin(a))
        ctx.rotate(a + 1.57)
        ctx.scale(0.16, 0.16)
        drawn.ACTORS["sp.bed_bug"](ctx, t, {"mood": "calm"})
        ctx.restore()
    ctx.arc(0, -230, 120, math.radians(200), math.radians(250))
    ctx.set_source_rgba(1, 1, 1, 0.5)
    ctx.set_line_width(14)
    ctx.stroke()


def rk_pile(ctx, t, p):
    """A tall laundry pile (feet at y 0, ~700 tall) that wobbles; p wob."""
    w = p.get("wob", 0.0) * math.sin(t * 9) * 8
    cols = ["#e5383b", "#3d7bd9", "#ffd34d", "#f2f2f2", "#3fb950", "#a86bd1", "#ff9f43"]
    import random
    rng = random.Random(5)
    for k in range(26):
        y = -40 - k * 26
        half = 360 - k * 12
        x = rng.uniform(-half, half) + w * (k / 26)
        shape(ctx, lambda c, x=x, y=y, k=k: p_ellipse(c, x, y, 120 - k * 2, 46, rng.uniform(-0.4, 0.4)),
              hexc(cols[k % len(cols)]), OUT * 0.6, None)


def rk_file(ctx, t, p):
    """A case-file folder stamped CASE #2 with a dark mystery silhouette; origin = its centre."""
    shape(ctx, lambda c: p_rrect(c, -300, -220, 600, 440, 18), hexc("#d9b26a"), OUT, (0.05, 0.1))
    shape(ctx, lambda c: p_rrect(c, -300, -260, 220, 60, 12), hexc("#d9b26a"), OUT, None)
    flat(ctx, lambda c: p_ellipse(c, -80, 40, 140, 90), hexc("#1d1b28"))
    for k in range(4):
        stroke(ctx, [(-80 + (k - 1.5) * 60, 80), (-80 + (k - 1.5) * 80, 150)], 12, color=hexc("#1d1b28"))
    im = txt("CASE #2", 84, RED, 0)
    s2, keep = drawn.pil_to_surface(im)
    ctx.save()
    ctx.translate(150, -120)
    ctx.rotate(-0.15)
    ctx.set_source_surface(s2, -im.width / 2, -im.height / 2)
    ctx.paint()
    ctx.restore()
    q = txt("?", 150, YEL, 10)
    s3, k3 = drawn.pil_to_surface(q)
    ctx.set_source_surface(s3, 140 - q.width / 2, 90 - q.height / 2)
    ctx.paint()


def rk_stick(ctx, t, p):
    """A toothpick lying flat, 520 long; origin = its centre."""
    shape(ctx, lambda c: p_poly(c, [(-260, 0), (-230, -9), (230, -9), (260, 0), (230, 9), (-230, 9)]), hexc("#e7c48a"), OUT * 0.6, None)


def rk_glow(ctx, t, p):
    """A pulsing red glow (the bite mark); p r, on."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    r = p.get("r", 60) * (1 + 0.15 * math.sin(t * 8))
    g = cairo.RadialGradient(0, 0, 0, 0, 0, r * 2.2)
    g.add_color_stop_rgba(0, 1, 0.25, 0.2, 0.9 * on)
    g.add_color_stop_rgba(1, 1, 0.25, 0.2, 0)
    ctx.set_source(g)
    ctx.arc(0, 0, r * 2.2, 0, 2 * math.pi)
    ctx.fill()
    shape(ctx, lambda c: p_ellipse(c, 0, 0, r * 0.45, r * 0.35), hexc("#e5383b"), OUT * 0.4, None)


def rk_speck(ctx, t, p):
    """Tiny glinting scales / specks scattered over p w x p h (origin = top left)."""
    import random
    rng = random.Random(p.get("seed", 2))
    for k in range(int(p.get("n", 40))):
        x, y = rng.uniform(0, p.get("w", 400)), rng.uniform(0, p.get("h", 120))
        a = 0.5 + 0.5 * math.sin(t * 6 + k)
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 7, 5), hexc(p.get("col", "#e8eef5")), a=a)


BURST = [("#ffd34d", "#ffb02e"), ("#7fd1ff", "#4aa8e8"), ("#ff8a7a", "#f2665a"), ("#9be37a", "#6cc94f")]


def rk_burst(ctx, t, p):
    """A full-screen comic reaction burst (screen space): alternating rays from the centre-top."""
    if p.get("on", 0.0) < 0.5:
        return
    c1, c2 = p.get("col", BURST[0])
    ctx.identity_matrix()
    ctx.rectangle(0, 0, W, H)
    ctx.set_source_rgb(*hexc(c1))
    ctx.fill()
    cx, cy = W / 2, H * 0.42
    n = 22
    rot = t * 0.15
    ctx.set_source_rgb(*hexc(c2))
    for k in range(n):
        a0 = rot + 2 * math.pi * k / n
        a1 = a0 + math.pi / n
        ctx.move_to(cx, cy)
        ctx.line_to(cx + 3000 * math.cos(a0), cy + 3000 * math.sin(a0))
        ctx.line_to(cx + 3000 * math.cos(a1), cy + 3000 * math.sin(a1))
        ctx.close_path()
        ctx.fill()


drawn.ACTORS.update(rk_burst=rk_burst, rk_rope=rk_rope, rk_washer=rk_washer, rk_pile=rk_pile, rk_file=rk_file, rk_stick=rk_stick,
                    rk_glow=rk_glow, rk_speck=rk_speck)
BUGS.update(widow=("black_widow", 1.0, 520, 260, "BLACK WIDOW"), recluse=("brown_recluse", 1.0, 520, 230, "BROWN RECLUSE"))

# ================================================================================================ rooms (world kits)
# floor y = 1500 in every room. mx = Meatball's mark, bug = the chapter's suspect and its mark (feet), light default.

ROOMS = {
    "hall": {"scene": "rk_hall", "sp": {}, "mx": 560, "bug": "centipede", "bpos": [1350, 980], "bs": 0.5, "light": "flashlight"},
    "bath": {"scene": "bathroom", "sp": {"dark": False}, "mx": 560, "bug": "silverfish", "bpos": [1620, 1124], "bs": 0.55, "light": "lamp"},
    "sill": {"scene": "sill", "sp": {}, "mx": 300, "bug": "silverfish", "bpos": [1150, 1500], "bs": 0.6, "light": "off"},
    "study": {"scene": "study", "sp": {}, "mx": 1450, "bug": "silverfish", "bpos": [700, 1500], "bs": 0.4, "light": "lamp"},
    "living": {"scene": "tp_living", "sp": {}, "mx": 1520, "bug": "mite", "bpos": [880, 1272], "bs": 0.32, "light": "lamp"},
    "scope": {"scene": "microscope", "sp": {}, "mx": None, "bug": "mite", "bpos": [960, 1300], "bs": 0.75, "light": "off"},
    "garage": {"scene": "rk_garage", "sp": {}, "mx": 560, "bug": "spider", "bpos": [1400, 420], "bs": 1.3, "light": "flashlight"},
    "base": {"scene": "basement", "sp": {}, "mx": 520, "bug": "centipede", "bpos": [1250, 1490], "bs": 0.5, "light": "lamp"},
    "skin": {"scene": "skin", "sp": {"night": False}, "mx": None, "bug": "centipede", "bpos": [960, 1100], "bs": 0.6, "light": "off"},
    "kitchen": {"scene": "kitchen", "sp": {}, "mx": 1450, "bug": "roach", "bpos": [480, 1016], "bs": 0.6, "light": "off"},
    "bed": {"scene": "bedroom", "sp": {}, "mx": 1900, "bug": "bedbug", "bpos": [1180, 1186], "bs": 1.0, "light": "lamp"},
    "cork": {"scene": "tc_cork", "sp": {"papers": []}, "mx": 1450, "bug": None, "light": "off"},
    "roof": {"scene": "rk_roof", "sp": {}, "mx": 960, "bug": None, "light": "off"},
    "house": {"scene": "ds_house_ext", "sp": {}, "mx": 1500, "bug": None, "light": "off"},
    "board": {"scene": "rk_board_bg", "sp": {}, "mx": None, "bug": None, "light": "off"},
}
CH_ROOM = ["hall", "bath", "living", "garage", "base", "kitchen", "bed", "roof"]
CH_BUG = [None, "silverfish", "mite", "spider", "centipede", "roach", "bedbug", None]
MB_SIZE = 700
POSE_ROT = ["point", "think", "present", "shrug", "subpoint", "deadpan", "nervous", "lean"]


def A(idn, typ, pos, s=1.0, p=None, **kw):
    a = {"id": idn, "type": typ, "pos": list(pos), "s": s, "p": dict(p or {})}
    a.update(kw)
    return a


def lab(idn, text, pos, at=None, px=64, color="#ffffff", **kw):
    a = A(idn, "ds_label", pos, 1.0, {"text": text, "px": px, "color": color, "on": 0.0 if at else 1.0}, **kw)
    if at:
        a["set"] = [{"at": at, "dur": 0.3, "p": {"on": 1.0}}]
    return a


def popset(at, key="on", dur=0.3, v=1.0):
    return [{"at": at, "dur": dur, "p": {key: v}}]


def stamp(text, at, color=RED, x=W // 2, y=520, px=150, rot=-10):
    return {"stamp": {"text": text, "color": color, "at": at, "x": x, "y": y, "px": px, "rot": rot}}


# ------------------------------------------------------------------ the shot table: line id -> recipe
# f: framings in order (w wide two-shot, m Meatball close, M Meatball face, b bug close, i bug left of frame for
#    the BUG ID card, k a free camera from "cams"); a line longer than ~3.6 s cycles them so no framing holds long.
# pose / mb (Meatball overrides, "hidden": True), bug (suspect overrides, None = not in shot), x (extra actors),
# room, light, sfx, cuts (framing boundaries), freak, shake, flash, ov (screen overlays), card (False = none).

def _table():
    T = {}
    # ------------------------------------------------------------------ cold open: the hallway, 2 AM
    T["s0.l0"] = dict(f="bM", cuts=["something|45%"], pose="nervous", bug={"s": 0.62, "pos": [1250, 980], "p": {"mood": "angry"}},
                      light={"kind": "flashlight", "snap": True}, mb={"gest": [["bit|80%", "shock", 1.0]]},
                      sfx=["click@0", "sting@0.05", "thud@something|45%"], zb=1.65)
    T["s0.l1"] = dict(f="kk", pose="deadpan", cams=[[640, 1060, 1.6, 1.75], [575, 1020, 2.4, 2.6]], cuts=["exactly|40%"],
                      bug=None, light="lamp", sfx=["click@exactly|40%"], mb={"prop": "flashlight"})
    T["s0.l2"] = dict(cap_y=1000, f="k", room="board", cams=[[960, 540, 1.0, 1.0]], bug=None, mb={"hidden": True},
                      ov=[{"type": "tier", "sil": True, "sil_at": "Six|30%", "in": 0.0}, {"type": "zoom", "from": [960, 540, 1.0], "to": [960, 700, 1.15], "at": 0.4}], sfx=["hit@0", "pop@Six|30%"])
    T["s0.l3"] = dict(cap_y=1000, f="k", room="board", cams=[[960, 540, 1.0, 1.0]], bug=None, mb={"hidden": True}, card=False,
                      ov=[{"type": "tier", "sil": True, "slide": False, "sil_at": "0%", "pulse": [["HARMLESS", "harmless|30%"], ["GET OUT", "get|60%"]]},
                          {"type": "zoom", "from": [300, 760, 1.7], "to": [1650, 760, 1.7], "at": 0.0, "linear": True}],
                      sfx=["whoosh@0.05", "tink@harmless|30%", "hit@get|60%"])
    T["s0.l4"] = dict(f="Mm", pose="you", bug=None, light={"kind": "flashlight", "from": (W / 2, H + 400), "w": 420},
                      flash=[0.05], sfx=["whoosh@0"], mb={"prop": "flashlight", "look": "viewer"})
    T["s0.l5"] = dict(f="bw", cuts=["not|45%"], pose="point", bug={"moves": [{"at": "one|30%", "dur": 0.5, "pos": [2900, 980], "linear": True}]},
                      mb={"prop": "flashlight", "moves": [{"at": "think|60%", "dur": 1.2, "pos": [1300, 1500], "walk": True}]},
                      sfx=["sting@one|30%", "scratch@one|35%"], light="flashlight")
    # ------------------------------------------------------------------ 1 silverfish: the bathroom
    T["s1.l0"] = dict(f="wb", cuts=["bathtub|55%"], pose="lean", mb={"prop": "flashlight"}, light="flashlight")
    T["s1.l1"] = dict(f="bi", cuts=["400|45%"], pose="present", ov=[{"type": "cam", "kind": "bugcam", "at": "0%", "to": "400|45%"}],
                      bug={"p": {"mood": "calm", "look": [-1, 0.3]}}, zb=1.4)
    T["s1.l2"] = dict(f="kk", room="board", cuts=["twice|35%"], cams=[[500, 1150, 0.95, 1.0], [1050, 1150, 0.95, 1.0]], bug=None,
                      roomscene="desert", light="off", pose="present",
                      mb={"pos": [60, 1500], "size": 640, "moves": [{"at": "twice|20%", "dur": 1.0, "pos": [600, 1500], "walk": True},
                                                                      {"at": "dinosaurs|60%", "dur": 1.0, "pos": [1450, 1500], "walk": True}]},
                      x=[A("rope", "rk_rope", [0, 1520], 1.0, {"w": 1700, "marks": [0, 800, 1700]}),
                         lab("now", "TODAY", [0, 1250], px=60), A("rex", "trex", [800, 1500], 0.42, {}),
                         lab("dl", "DINOSAURS", [800, 1080], "twice|30%", px=60, color=YEL),
                         A("sf", "sp.silverfish", [1700, 1500], 0.38, {"mood": "calm", "look": [-1, 0]}, flip=True),
                         lab("sl", "SILVERFISH FOSSILS", [1650, 1250], "dinosaurs|60%", px=60, color=YEL)],
                      sfx=["step@twice|25%", "pop@dinosaurs|70%"])
    T["s1.l3"] = dict(f="ib", cuts=["flat|55%"], pose="shock", look="hero",
                      bug={"moves": [{"at": "rapidly|15%", "dur": 0.35, "pos": [1900, 1124]}, {"at": "sideways|35%", "dur": 0.35, "pos": [1350, 1124]},
                                     {"at": "flat|55%", "dur": 0.4, "pos": [1600, 1124]}]}, sfx=["scratch@rapidly|15%", "whoosh@sideways|35%"])
    T["s1.l4"] = dict(f="mw", pose="lean", look="hero", light={"kind": "lamp", "dark": 0.62}, sfx=["click@0.05"])
    T["s1.l5"] = dict(f="bb", pose="think", zb=2.0, x=[A("book", "book", [1700, 1124], 0.55, {})],
                      bug={"pos": [1540, 1124]}, sfx=["scratch@scrape|45%"])
    T["s1.l6"] = dict(f="wk", room="cork", cams=[[1000, 1000, 1.0, 1.05], [760, 760, 1.6, 1.7]], cuts=["paper|35%"], pose="point", look=[760, 760],
                      x=[A("ph", "rk_photo", [760, 760], 1.0, {"bug": "silverfish", "on": 0.0}, set=popset("That's|5%"))],
                      sfx=["thud@That's|10%"])
    T["s1.l7"] = dict(f="kk", room="cork", cams=[[760, 760, 1.5, 1.6], [900, 900, 1.05, 1.1]], cuts=["disease|60%"], pose="present",
                      x=[A("ph", "rk_photo", [760, 760], 1.0, {"bug": "silverfish"})],
                      **stamp("NO DISEASE", "disease|40%", GREEN, 760, 470, 120), sfx=["stamp@disease|40%"])
    T["s1.l8"] = dict(f="wm", room="sill", pose="point", look="hero", card="WHY IS IT IN MY HOUSE?",
                      bug={"pos": [-300, 1500], "s": 0.5, "moves": [{"at": "invade|20%", "dur": 3.0, "pos": [1700, 1500], "walk": True}]},
                      x=[A("sf2", "sp.silverfish", [-800, 1500], 0.4, {}, moves=[{"at": "invade|30%", "dur": 3.0, "pos": [1200, 1500], "walk": True}])],
                      mb={"pos": [300, 1500]})
    T["s1.l9"] = dict(f="wb", room="sill", pose="shrug", look="hero", bug={"pos": [1500, 1500], "s": 0.5},
                      x=[lab("sum", "SUMMER", [1150, 700], "summer|20%", px=120, color="#ff9f43"),
                         A("sun", "rk_glow", [1500, 500], 1.0, {"r": 160, "on": 0.0}, set=popset("summer|20%", dur=0.6))],
                      tint=[1.0, 0.7, 0.2, 0.12], mb={"pos": [300, 1500]})
    T["s1.l10"] = dict(f="kb", cams=[[1450, 1150, 1.3, 1.4]], pose="think",
                       bug={"pos": [1300, 1360], "rot": -70, "s": 0.45, "moves": [
                           {"at": "fall|10%", "dur": 0.6, "pos": [1300, 1180]}, {"at": "climb|45%", "dur": 0.3, "pos": [1300, 1380]},
                           {"at": "slippery|65%", "dur": 0.6, "pos": [1300, 1200]}, {"at": "sides|85%", "dur": 0.3, "pos": [1300, 1390]}]},
                       sfx=["whoosh@climb|45%", "whoosh@sides|85%"])
    T["s1.l11"] = dict(f="mk", cams=[[840, 1450, 2.4, 2.7]], cuts=["drain|50%"], pose="lean", bug=None,
                       mb={"prop": "flashlight", "pos": [520, 1500]}, light={"kind": "flashlight", "target": [840, 1560]},
                       x=[lab("nada", "NOTHING", [840, 1380], "either|60%", px=60, color=YEL)])
    T["s1.l12"] = dict(f="mb", room="study", cuts=["scales|45%"], pose="present", card="WHAT SHOULD YOU DO?", zb=1.6,
                       bug={"pos": [700, 1440], "s": 0.35}, mb={"prop": "flashlight"},
                       x=[A("bk", "book", [700, 1500], 0.9, {}), A("sp", "rk_speck", [430, 1380], 1.0, {"w": 560, "h": 120, "n": 50})])
    T["s1.l13"] = dict(f="wb", pose="wave", look="hero", bug={"p": {"look": [-1, -0.4]}, "moves": [{"at": "history|40%", "dur": 0.3, "pos": [1630, 1118]}, {"at": "loses|60%", "dur": 0.3, "pos": [1620, 1124]}]})
    T["s1.l14"] = dict(tier="silverfish")
    T["s1.l15"] = dict(f="wk", room="living", cams=[[600, 1100, 0.85, 0.9]], cuts=["couch|55%"], pose="point", bug=None,
                       mb={"prop": "flashlight", "pos": [1700, 1500], "moves": [{"at": "trail|30%", "dur": 1.5, "pos": [1350, 1500], "walk": True}]},
                       light={"kind": "flashlight", "target": [900, 1300]},
                       x=[A("tr%d" % k, "skin_flake", [1250 - k * 110, 1495 - (k > 4) * 0], 0.28, {}) for k in range(6)])
    # ------------------------------------------------------------------ 2 dust mites: the living room couch
    T["s2.l0"] = dict(f="wM", cuts=["see|60%"], pose="think", look=[880, 1260], bug={"hidden": True})
    T["s2.l1"] = dict(f="ki", room="scope", cuts=["half|40%"], cams=[[960, 1100, 0.6, 0.9]], bug={"p": {"look": [0.5, 0]}},
                      ov=[{"type": "cam", "kind": "mitecam", "at": "0%", "to": "half|40%"}], zb=1.0)
    T["s2.l2"] = dict(f="im", pose="think", bug={"s": 0.45, "pos": [880, 1272]}, zb=1.5,
                      x=[A("fl%d" % k, "skin_flake", [700 + 90 * k, 300], 0.3, {}, moves=[{"at": "%d%%" % (10 + 12 * k), "dur": 2.0, "pos": [700 + 90 * k + 40, 1270]}]) for k in range(5)],
                      mb={"gest": [["skin|30%", "think", 1.2]]})
    T["s2.l3"] = dict(f="kk", cams=[[880, 1200, 1.5, 1.2], [1000, 1060, 0.9, 0.78]], cuts=["sofas|45%"], pose="present", bug={"s": 0.3},
                      x=[lab("b1", "BEDS", [500, 800], "beds|30%", px=80, color=YEL), lab("b2", "SOFAS", [900, 900], "sofas|50%", px=80, color=YEL),
                         lab("b3", "CHAIRS", [1300, 800], "chairs|80%", px=80, color=YEL)])
    T["s2.l4"] = dict(f="mw", pose="lean", look="hero", light={"kind": "lamp", "dark": 0.62}, sfx=["click@0.05"])
    T["s2.l5"] = dict(f="kk", room="scope", cams=[[960, 1100, 0.8, 0.85], [960, 1150, 1.0, 1.08]], cuts=["biting|50%"],
                      bug={"p": {"mood": "calm", "look": [0, 0]}}, **stamp("CLEARED OF THE BITE", "biting|50%", GREEN, 960, 300, 110), card=False,
                      sfx=["stamp@biting|50%"])
    T["s2.l6"] = dict(f="kk", room="house", cams=[[700, 1000, 0.75, 0.8], [700, 1250, 1.2, 1.3]], cuts=["Every|50%"], pose="present",
                      x=[A("hs", "ds_houses", [500, 1700], 1.6, {"n": 10, "cols": 5, "lit": 1.0})], mb={"pos": [1500, 1600]})
    T["s2.l7"] = dict(f="Mw", pose="nervous",
                      x=[lab("al1", "CAST SKIN", [1250, 1400], "skins|40%", px=56, color="#ffffff",
                             moves=[{"at": "skins|40%", "dur": 2.0, "pos": [1350, 700]}]),
                         lab("al2", "DROPPINGS", [1700, 1400], "droppings|50%", px=56, color="#ffffff",
                             moves=[{"at": "droppings|50%", "dur": 1.6, "pos": [1600, 760]}])])
    T["s2.l8"] = dict(f="Mk", room="board", roomscene="keeper_room", cams=[[900, 1150, 1.0, 1.05], [1100, 1150, 1.6, 1.75]], cuts=["dry|60%"], pose="present",
                      x=[A("wash", "rk_washer", [1100, 1500], 1.3, {"spin": 5.0, "dial": 0.2}, set=[{"at": "hot|30%", "dur": 0.5, "p": {"dial": 0.9}}]),
                         lab("hot", "HOT", [1400, 1000], "hot|30%", px=80, color=RED)],
                      mb={"pos": [450, 1500]}, sfx=["click@hot|30%"])
    T["s2.l9"] = dict(f="wm", room="board", roomscene="keeper_room", cams=None, pose="shock", look=[1250, 1100],
                      x=[A("pile", "rk_pile", [1250, 1500], 1.2, {"wob": 1.0}),
                         A("pm", "sp.dust_mite", [1260, 760], 0.18, {"mood": "calm"})],
                      bugpos_for_frame=[1250, 1300], mb={"pos": [500, 1500]}, sfx=["boing@scarier|50%"])
    T["s2.l10"] = dict(f="Mk", cams=[[880, 1240, 1.5, 1.7]], pose="shock", look=[880, 1260], bug={"s": 0.36})
    T["s2.l11"] = dict(tier="mite")
    T["s2.l12"] = dict(f="kw", room="garage", cams=[[1400, 760, 1.4, 1.55]], cuts=["garage|50%"], pose="think", bug={"hidden": True},
                       x=[A("web", "ds_web", [1680, 520], 0.8, {"w": 520, "h": 600})], light={"kind": "flashlight", "target": [1400, 760]})
    # ------------------------------------------------------------------ 3 spiders: the garage
    T["s3.l0"] = dict(f="Mi", cuts=["belly|45%"], pose="point", look="hero",
                      x=[A("web", "ds_web", [1680, 520], 0.8, {"w": 520, "h": 600})])
    T["s3.l1"] = dict(f="iM", cuts=["small|55%"], pose="present", look="hero", x=[A("web", "ds_web", [1680, 520], 0.8, {"w": 520, "h": 600})],
                      mb={"gest": [["small|60%", "shrug", 1.0]]})
    T["s3.l2"] = dict(f="kM", cams=[[560, 1010, 2.2, 2.6]], pose="lean", look="viewer", ov=[{"type": "cam", "kind": "spidercam", "at": "0%", "to": "spider|50%"}],
                      cuts=["spider|50%"], light={"kind": "lamp", "dark": 0.6}, sfx=["click@0.05", "whoosh@spider|50%"])
    T["s3.l3"] = dict(f="bbb", cuts=["squeezed|25%", "lain|55%"], zb=1.5,
                      x=[lab("q1", "SQUEEZED", [1400, 520], "squeezed|25%", px=100, color=YEL),
                         lab("q2", "LAIN ON", [1400, 520], "lain|55%", px=100, color=YEL),
                         lab("q3", "PROVOKED", [1400, 520], "provoked|80%", px=100, color=YEL)],
                      sfx=["pop@squeezed|25%", "pop@lain|55%", "pop@provoked|80%"])
    T["s3.l4"] = dict(f="mw", pose="nervous", bug=None, x=[A("sheet", "tc_prop", [1200, 1500], 1.0, {"kind": "sheet"})], look=[1200, 1450])
    T["s3.l5"] = dict(f="Mm", pose="think", mb={"gest": [["bee|60%", "shrug", 1.2]]}, cuts=["bee|55%"])
    T["s3.l6"] = dict(f="kb", cams=[[200, 900, 1.0, 1.0]], card="WHY IS IT IN MY HOUSE?", pans=[[200, 900, 1.0], [1300, 850, 1.05]],
                      mb={"hidden": True}, x=[A("web", "ds_web", [1680, 520], 0.8, {"w": 520, "h": 600})], light={"kind": "flashlight", "target": [1400, 700]})
    T["s3.l7"] = dict(f="ki", cams=[[1400, 450, 2.0, 2.1]], cuts=["harmful|40%"], x=[lab("cs", "CELLAR SPIDER", [1160, 330], "cellar|20%", px=72, color=YEL)], zb=1.3)
    T["s3.l8"] = dict(f="kk", room="garage", cams=[[960, 700, 0.9, 0.95], [700, 700, 1.4, 1.5]], cuts=["toxic|60%"], bug=None, mb={"hidden": True},
                      x=[A("w1", "rk_photo", [650, 700], 1.1, {"bug": "widow", "on": 0.0, "tilt": -6}, set=popset("widows|20%")),
                         A("w2", "rk_photo", [1300, 700], 1.1, {"bug": "recluse", "on": 0.0, "tilt": 5}, set=popset("recluses|40%")),
                         lab("wa", "VERY TOXIC VENOM", [960, 420], "venom|60%", px=90, color=RED)],
                      sfx=["thud@widows|20%", "thud@recluses|40%"], light="lamp")
    T["s3.l9"] = dict(f="wk", room="board", roomscene="office", cams=[[1300, 1100, 1.3, 1.4]], cuts=["county|50%"], pose="present", bug=None,
                      mb={"pos": [400, 1500], "moves": [{"at": "Save|25%", "dur": 1.6, "pos": [900, 1500], "walk": True}], "prop": None},
                      x=[A("jar", "tp_jar", [520, 1180], 1.6, {}, moves=[{"at": "Save|25%", "dur": 1.6, "pos": [1040, 1180]}]),
                         A("desk", "desk", [1500, 1500], 1.0, {}), lab("ext", "COUNTY EXTENSION OFFICE", [1450, 950], "county|50%", px=70, color=YEL)])
    T["s3.l10"] = dict(f="Mm", room="garage", pose="point", bug=None, x=[A("ph", "cl_phone", [780, 1180], 1.1, {})], sfx=["tink@doctor|60%"])
    T["s3.l11"] = dict(tier="spider")
    T["s3.l12"] = dict(f="kb", room="base", cams=[[300, 1100, 1.0, 1.1]], mb={"hidden": True}, light="flashlight", zb=1.1,
                       bug={"pos": [800, 1490], "moves": [{"at": "legs|30%", "dur": 0.7, "pos": [-600, 900], "linear": True}]},
                       sfx=["scratch@legs|30%", "sting@legs|35%"])
    # ------------------------------------------------------------------ 4 house centipede: the basement
    T["s4.l0"] = dict(f="kk", cams=[[960, 1150, 0.82, 0.82], [960, 1150, 0.82, 0.82]], cuts=["security|35%"], mb={"hidden": True}, light="off",
                      bug={"pos": [-500, 1490], "moves": [{"at": "security|40%", "dur": 1.2, "pos": [2400, 1490], "linear": True}]},
                      ov=[{"type": "cam", "kind": "seccam", "at": "security|35%"}], sfx=["scratch@security|45%"])
    T["s4.l1"] = dict(f="kk", cuts=["clocked|35%"], cams=[[1000, 1200, 0.9, 0.95], [900, 1250, 1.0, 1.06]],
                      bug={"pos": [-400, 1490], "moves": [{"at": "clocked|20%", "dur": 1.2, "pos": [800, 1490], "linear": True}]}, light="off",
                      x=[A("rul", "tc_prop", [1100, 1560], 1.4, {"kind": "ruler", "w": 1500}),
                         A("ctr", "tc_counter", [600, 880], 1.0, {"v": 0, "fmt": "{} IN/SEC", "px": 110}, set=[{"at": "about|50%", "dur": 0.9, "p": {"v": 16}}])],
                      sfx=["scratch@clocked|20%", "tink@sixteen|70%"])
    T["s4.l2"] = dict(f="ik", cams=[[1250, 1000, 0.75, 0.8]], cuts=["walls|50%"], zb=0.95,
                      bug={"pos": [1500, 1490], "moves": [{"at": "run|30%", "dur": 0.3, "pos": [1700, 1480], "rot": -90},
                                                          {"at": "walls|50%", "dur": 1.2, "pos": [1700, 500]}]}, sfx=["scratch@run|30%"])
    T["s4.l3"] = dict(f="kb", cams=[[1650, 1200, 3.2, 3.6]], zb=1.6, idx=480, bug={"p": {"look": [-1, 0.1]}}, sfx=["tink@faceted|60%"])
    T["s4.l4"] = dict(f="mM", pose="point", look="hero", cuts=["biter|60%"], **stamp("GET OUT", "biter|60%", RED, 1300, 420, 190, -12),
                      sfx=["whoosh@hunts|40%", "stamp@biter|60%"], shake=["biter|60%"])
    T["s4.l5"] = dict(f="Mw", pose="shock", look="hero", sfx=["scratch@0.02", "hit@twist|60%"], cuts=["twist|55%"])
    T["s4.l6"] = dict(f="M", pose="you", look="viewer", card=False,
                      ov=[{"type": "big", "at": "0%", "rows": [["WHICH ONE IS IN", 110, "#ffffff"], ["YOUR HOUSE?", 150, YEL], ["COMMENT IT", 110, "#ffffff"]], "dim": 0.45, "y": 210},
                          {"type": "tier", "sil": True, "full": False, "slide": False, "sil_at": "0%", "only_sil": True}],
                      sfx=["hit@0.05", "pop@Comment|40%"])
    T["s4.l7"] = dict(f="bm", pose="deadpan", cuts=["accidentally|50%"], zb=1.3)
    T["s4.l8"] = dict(f="kk", room="board", roomscene="rk_board_bg", cams=[[0, -110, 0.7, 0.75], [0, -40, 0.95, 1.05]], cuts=["piercing|45%"], bug=None, mb={"hidden": True},
                      x=[A("fg", "ds_fangs", [0, 0], 1.6, {"dip": 0.0}, set=[{"at": "piercing|50%", "dur": 0.8, "p": {"dip": 1.0}}]),
                         ], sfx=["tink@piercing|55%"], center=True)
    T["s4.l9"] = dict(f="mw", pose="facepalm", look="hero", sfx=["boing@never|30%"])
    T["s4.l10"] = dict(f="wb", pose="present", look="hero", card="WHY IS IT IN MY HOUSE?",
                       x=[A("v1", "sp.roach", [1700, 1490], 0.22, {}, flip=True), A("v2", "sp.silverfish", [1850, 1490], 0.2, {}, flip=True),
                          A("v3", "sp.roach", [2000, 1490], 0.2, {}, flip=True)], bug={"pos": [1100, 1490], "s": 0.4})
    T["s4.l11"] = dict(f="kk", room="bath", cams=[[1620, 1050, 1.6, 1.7], [1620, 1050, 1.6, 1.7]], mb={"hidden": True},
                       tint=[0.6, 0.5, 0.9, 0.18], bug={"p": {"mood": "calm", "look": [-1, 0]}}, x=[lab("fb", "FLASHBACK", [1620, 760], None, px=64, color=YEL)])
    T["s4.l12"] = dict(f="kb", cams=[[1200, 1250, 1.2, 1.3]], cuts=["lassoing|50%"], zb=1.1, mb={"hidden": True},
                       bug={"pos": [900, 1490], "moves": [{"at": "pouncing|20%", "dur": 0.4, "pos": [1350, 1490], "hop": 120}]},
                       x=[A("prey", "sp.roach", [1500, 1490], 0.22, {}, flip=True)], sfx=["boing@pouncing|25%", "whoosh@lassoing|55%"])
    T["s4.l13"] = dict(f="wm", pose="point", look="hero", card="WHAT SHOULD YOU DO?",
                       mb={"moves": [{"at": "grab|40%", "dur": 0.3, "pos": [700, 1500]}, {"at": "grab+0.4", "dur": 0.2, "pos": [520, 1500]}],
                           "gest": [["grab|50%", "shock", 1.0]]}, sfx=["boing@grab|55%"])
    T["s4.l14"] = dict(f="Mw", pose="present", mb={"gest": [["counted|40%", "point", 0.8], ["single|70%", "subpoint", 0.8]]},
                       **stamp("SINGLE DIGITS", "single|65%", YEL, 1300, 330, 120, -8), sfx=["stamp@single|65%"])
    T["s4.l15"] = dict(cuts=["arrested|45%"], f="bw", pose="shrug", look="hero",
                       x=[A("ph", "rk_photo", [700, 1150], 0.5, {"bug": "centipede"}, moves=[{"at": "arrested|40%", "dur": 1.0, "pos": [1150, 1300]}])])
    T["s4.l16"] = dict(tier="centipede")
    T["s4.l17"] = dict(f="kw", cams=[[100, 1000, 1.0, 1.1]], cuts=["kitchen|50%"], pose="point", bug={"hidden": True},
                       mb={"prop": "flashlight", "moves": [{"at": "checking|40%", "dur": 1.0, "pos": [200, 1400], "walk": True}]},
                       light={"kind": "flashlight", "target": [0, 700]})
    # ------------------------------------------------------------------ 5 cockroach: the kitchen
    T["s5.l0"] = dict(f="wb", cuts=["flip|45%"], pose="shock", look="hero", light={"kind": "flashlight", "off_at": "light|40%"}, flash=["light|40%"],
                      x=[A("r%d" % k, "sp.roach", [300 + 90 * k, 1016], 0.35, {}, moves=[{"at": "light|45%", "dur": 0.5, "pos": [-400 + 90 * k * (k % 2), 1016], "linear": True}]) for k in range(4)],
                      sfx=["click@light|40%", "scratch@light|45%"])
    T["s5.l1"] = dict(f="bi", cuts=["light|40%"], zb=1.6, ov=[{"type": "cam", "kind": "bugcam", "at": "0%", "to": "light|40%"}],
                      x=[A("toast", "tp_toaster", [700, 1016], 1.3, {})], bug={"pos": [420, 1016]})
    T["s5.l2"] = dict(f="ib", cuts=["crack|60%"], zb=1.5, bug={"moves": [{"at": "crack|50%", "dur": 0.6, "pos": [300, 1016], "s": 0.6}]},
                      x=[A("gauge", "tc_prop", [330, 960], 0.6, {"kind": "ruler", "w": 400}), lab("gg", "1/16-INCH GAP", [330, 860], "crack|40%", px=48, color=YEL)])
    T["s5.l3"] = dict(f="ik", cams=[[480, 900, 1.5, 1.6]], zb=1.5, bug={"hidden": True},
                      x=[A("ooth", "tc_ooth", [480, 1016], 1.5, {}), A("ctr", "tc_counter", [480, 690], 1.0, {"v": 0, "fmt": "ABOUT {}", "px": 100},
                                                                       set=[{"at": "contains|25%", "dur": 1.0, "p": {"v": 30}}])],
                      sfx=["tink@30|60%"])
    T["s5.l4"] = dict(f="mw", pose="lean", look="hero", light={"kind": "lamp", "dark": 0.62}, sfx=["click@0.05"])
    T["s5.l5"] = dict(f="kb", cams=[[500, 900, 1.0, 1.05], [450, 950, 1.4, 1.5]], cuts=["reported|55%"], mb={"hidden": True}, light="lamp",
                      x=[A("c%d" % k, "sp.roach", [80 + (k % 6) * 150, 1016 - 70 * (k // 6)], 0.25, {}, flip=bool(k % 2)) for k in range(12)] +
                        [lab("eh", "EXTREMELY HEAVY", [500, 650], "extremely|20%", px=90, color=RED)], tint=[0.3, 0.25, 0.1, 0.25])
    T["s5.l6"] = dict(f="wb", pose="deadpan", look="viewer", x=[lab("one", "ONE ROACH", [480, 800], "one|30%", px=80, color=YEL)], flash=[0.02])
    T["s5.l7"] = dict(f="Mk", cams=[[600, 900, 1.4, 1.5]], pose="nervous",
                      x=[lab("dp", "DROPPINGS", [400, 800], "droppings|30%", px=60,
                                                                           moves=[{"at": "droppings|30%", "dur": 2.0, "pos": [700, 700]}])])
    T["s5.l8"] = dict(f="kb", cams=[[600, 900, 1.3, 1.4]], card="WHY IS IT IN MY HOUSE?", bug={"pos": [600, 830], "moves": [{"at": "grocery|40%", "dur": 0.8, "pos": [350, 1016]}]},
                      x=[A("bag", "cl_box", [620, 1016], 1.8, {})], zb=1.4)
    T["s5.l9"] = dict(f="wb", pose="shrug", bug={"pos": [100, 1016], "moves": [{"at": "clean|20%", "dur": 2.0, "pos": [650, 1016], "walk": True}]},
                      x=[A("sp%d" % k, "spark", [200 + k * 260, 700 + 60 * (k % 2)], 1.0, {}) for k in range(5)])
    T["s5.l10"] = dict(f="mw", pose="shrug", card="WHAT SHOULD YOU DO?",
                       x=[A("can", "tc_prop", [1250, 1500], 0.8, {"kind": "aerosol"}, moves=[{"at": "alone|40%", "dur": 1.0, "pos": [800, 1500], "rot": 90}])],
                       sfx=["thud@alone|45%"])
    T["s5.l11"] = dict(f="wk", cams=[[480, 900, 1.5, 1.6]], cuts=["exclusion|50%"], pose="present",
                       x=[lab("w1", "WIPE IT CLEAN", [480, 700], "sanitation|20%", px=72, color=GREEN), lab("w2", "SEAL THE CRACKS", [480, 820], "exclusion|50%", px=72, color=GREEN)])
    T["s5.l12"] = dict(f="kk", room="board", roomscene="kitchen", cams=[[960, 1150, 1.0, 1.05], [1300, 1250, 1.5, 1.6]], cuts=["sprays|60%"], mb={"hidden": True}, bug=None,
                       x=[A("bait", "cl_box", [650, 1500], 1.2, {}), lab("bl", "BAIT", [650, 1150], "baits|30%", px=90, color=GREEN),
                          A("can", "tc_prop", [1300, 1500], 0.9, {"kind": "aerosol"}),
                          A("x", "ds_cross", [1300, 1330], 1.0, {"on": 0.0, "r": 200}, set=popset("sprays|60%"))], sfx=["pop@baits|30%", "stamp@sprays|60%"])
    T["s5.l13"] = dict(f="kk", room="board", roomscene="kitchen", cams=[[960, 1150, 1.0, 1.05], [960, 1250, 1.4, 1.5]], cuts=["hazardous|55%"], mb={"hidden": True}, bug=None,
                       x=[A("bomb", "tc_prop", [960, 1500], 1.0, {"kind": "foamcan"})], **stamp("NO", "bombs|35%", RED, 960, 500, 220, -12), sfx=["stamp@bombs|35%"])
    T["s5.l14"] = dict(f="kM", cams=[[650, 820, 1.5, 1.65]], pose="point", x=[A("inh", "tc_prop", [650, 1016], 0.9, {"kind": "aerosol"}), lab("rd", "READ THE LABEL", [650, 560], "label|20%", px=64, color=YEL)])
    T["s5.l15"] = dict(f="Mw", pose="nervous", mb={"shake": 1.0}, shake=["shower|50%"], sfx=["boing@shower|50%"])
    T["s5.l16"] = dict(tier="roach")
    T["s5.l17"] = dict(f="Mk", cams=[[1500, 1150, 2.6, 2.8]], pose="think", bug=None,
                       x=[A("bite", "rk_glow", [1530, 1180], 1.0, {"r": 40, "on": 0.0}, front=True, lit=True, set=popset("blood|50%", dur=0.5))], cuts=["blood|45%"])
    T["s5.l18"] = dict(f="kw", cams=[[1500, 1000, 1.3, 1.5]], pose="deadpan", look="viewer", bug={"hidden": True},
                       light={"kind": "lamp", "dark": 0.7}, sfx=["scratch@mine|60%"], mb={"moves": [{"at": "mine|50%", "dur": 1.5, "pos": [1900, 1500], "walk": True}]})
    # ------------------------------------------------------------------ 6 bed bugs: Meatball's bedroom
    T["s6.l0"] = dict(f="wk", cams=[[1180, 1150, 1.4, 1.5]], cuts=["bed|60%"], pose="nervous", look="hero", bug={"hidden": True}, sfx=["thud@last|40%", "thud@bed|70%"])
    T["s6.l1"] = dict(f="kM", cams=[[600, 1180, 1.8, 1.8], [1100, 1180, 1.8, 2.0]], cuts=["seam|40%"], pose="lean", bug={"hidden": True},
                      mb={"prop": "flashlight"}, light={"kind": "flashlight", "target": [900, 1200]}, pans=[[500, 1180, 1.8], [1150, 1190, 2.2]])
    T["s6.l2"] = dict(f="Mbw", cuts=["bug#2|35%", "There's|65%"], pose="shock", freak=[0.15, "There's|65%"], shake=[0.15, "bug#2|35%", "There's|65%"],
                      flash=[0.1], mb={"shake": 1.0, "moves": [{"at": 0.12, "dur": 0.55, "pos": [1900, 1500], "hop": 420},
                                                                {"at": "There's|65%", "dur": 0.5, "pos": [1850, 1500], "hop": 300}]},
                      bug={"p": {"mood": "angry"}}, sfx=["sting@0.1", "boing@0.15", "hit@There's|65%"], zb=1.5)
    T["s6.l3"] = dict(f="wM", pose="nervous", look="hero", mb={"shake": 0.8, "moves": [{"at": "out#2|35%", "dur": 0.5, "pos": [2100, 1500], "hop": 200}]},
                      sfx=["boing@out#2|35%"], card_px=150)
    T["s6.l4"] = dict(f="bi", cuts=["reddish|40%"], zb=1.7, bug={"p": {"look": [-0.5, 0.2]}})
    T["s6.l5"] = dict(ring_k=True, f="ik", cams=[[300, 1050, 2.0, 2.1]], zb=1.7, x=[A("tp", "rk_stick", [330, 1000], 0.7, {}, rot=90)],
                      bug={"moves": [{"at": "toothpick|40%", "dur": 1.0, "pos": [250, 1060], "s": 0.5}]})
    T["s6.l6"] = dict(ring_k=True, f="ikkk", cams=[[600, 1200, 2.3, 2.4], [400, 1430, 2.2, 2.3], [210, 900, 2.0, 2.1]], cuts=["seams|20%", "springs|45%", "frames|65%"], zb=1.7,
                      x=[A("h1", "sp.bed_bug", [600, 1200], 0.25, {}), A("h2", "sp.bed_bug", [400, 1440], 0.25, {}), A("h3", "sp.bed_bug", [215, 900], 0.25, {}, rot=-90)])
    T["s6.l7"] = dict(f="Mm", pose="deadpan", mb={"gest": [["Yes|50%", "nervous", 1.0]]})
    T["s6.l8"] = dict(f="kb", cams=[[900, 1150, 0.95, 1.05]], tint=[0.25, 0.3, 0.7, 0.2], mb={"hidden": True},
                      x=[A("zz", "tp_zzz", [600, 1000], 1.4, {"on": 1.0}), lab("fb", "FLASHBACK", [900, 560], None, px=64, color=YEL),
                         ],
                      bug={"pos": [1500, 1190], "moves": [{"at": "bite|20%", "dur": 3.0, "pos": [900, 1190], "walk": True}]}, zb=1.4)
    T["s6.l9"] = dict(f="kb", cams=[[600, 1100, 1.5, 1.6]], cuts=["seldom|50%"], tint=[0.25, 0.3, 0.7, 0.2], mb={"hidden": True},
                      x=[A("zz", "tp_zzz", [600, 1000], 1.4, {"on": 1.0})], bug={"pos": [800, 1190]})
    T["s6.l10"] = dict(f="Mk", cams=[[1900, 1150, 2.4, 2.6]], pose="think", card="AS LONG AS 14 DAYS · IN SOME PEOPLE",
                       x=[A("bite", "rk_glow", [1930, 1180], 1.0, {"r": 40, "on": 0.0}, front=True, lit=True, set=[{"at": "develop|50%", "dur": 1.2, "p": {"on": 1.0}}])], bug={"hidden": True})
    T["s6.l11"] = dict(f="mM", cams=[[1900, 950, 1.8, 1.9]], cuts=["Serious|55%"], pose="think", bug={"hidden": True},
                       x=[lab("am", "3 AM", [1500, 700], "Serious|55%", px=110, color=YEL)], mb={"gest": [["itching|20%", "nervous", 1.0]]})
    T["s6.l12"] = dict(f="Mw", pose="laugh", look="viewer", bug={"hidden": True})
    T["s6.l13"] = dict(f="wk", room="cork", cams=[[760, 760, 1.5, 1.6]], cuts=["biter|50%"], pose="point", look=[760, 760],
                       x=[A("ph", "rk_photo", [760, 760], 1.0, {"bug": "bedbug"})], **stamp("CASE CLOSED", "closed|30%", RED, 760, 500, 130), sfx=["stamp@closed|30%"])
    T["s6.l14"] = dict(f="wb", pose="point", look="hero", card="WHY IS IT IN MY HOUSE?",
                       x=[A("suit", "tp_suitcase", [1250, 1186], 1.4, {})], bug={"pos": [1250, 1186], "s": 0.5, "moves": [{"at": "hitchhike|30%", "dur": 1.2, "pos": [900, 1186], "walk": True}]})
    T["s6.l15"] = dict(f="wk", room="board", roomscene="keeper_room", cams=[[1100, 1150, 1.6, 1.75]], cuts=["heat|45%"], pose="present", bug=None,
                       x=[A("dry", "rk_washer", [1100, 1500], 1.3, {"dryer": True, "spin": 6.0, "dial": 0.2}, set=[{"at": "high|30%", "dur": 0.5, "p": {"dial": 1.0}}]),
                          lab("hi", "HIGH HEAT", [1100, 700], "high|30%", px=80, color=RED), lab("tm", "30 MIN", [1100, 820], "30|50%", px=80, color=YEL)],
                       mb={"pos": [450, 1500]}, sfx=["click@high|30%", "tink@30|60%"])
    T["s6.l16"] = dict(f="kk", room="board", roomscene="keeper_room", cams=[[1100, 1100, 1.0, 1.05], [1100, 1250, 2.0, 2.2]], cuts=["kill|40%"], mb={"hidden": True}, bug=None,
                       x=[A("wash", "rk_washer", [1100, 1500], 1.3, {"spin": 5.0, "rider": True})], **stamp("NOT ENOUGH", "kill|50%", RED, 960, 330, 130))
    T["s6.l17"] = dict(f="kkk", room="board", roomscene="tc_living", cams=[[500, 1250, 1.4, 1.5], [1000, 1250, 1.4, 1.5], [1500, 1250, 1.4, 1.5]],
                       cuts=["propane|35%", "fireplace|70%"], mb={"hidden": True}, bug=None,
                       x=[A("th", "tc_prop", [500, 1250], 0.9, {"kind": "thermostat"}), A("ht", "cl_box", [1000, 1500], 1.3, {}),
                          A("lg", "tc_prop", [1500, 1500], 1.0, {"kind": "logs", "n": 6}),
                          A("x1", "ds_cross", [500, 1250], 1.0, {"on": 0.0, "r": 190}, set=popset("thermostat|25%")),
                          A("x2", "ds_cross", [1000, 1350], 1.0, {"on": 0.0, "r": 190}, set=popset("heater|60%")),
                          A("x3", "ds_cross", [1500, 1350], 1.0, {"on": 0.0, "r": 190}, set=popset("fireplace|85%")),
                          lab("l1", "THERMOSTAT", [500, 1020], "thermostat|20%", px=56), lab("l2", "SPACE HEATER", [1000, 1020], "heater|50%", px=56),
                          lab("l3", "FIREPLACE", [1500, 1020], "fireplace|80%", px=56)],
                       sfx=["stamp@thermostat|25%", "stamp@heater|60%", "stamp@fireplace|85%"])
    T["s6.l18"] = dict(f="k", room="board", roomscene="tc_living", cams=[[1000, 1300, 0.85, 1.0]], mb={"hidden": True}, bug=None,
                       x=[A("th", "tc_prop", [500, 1250], 0.9, {"kind": "thermostat"}), A("ht", "cl_box", [1000, 1500], 1.3, {}),
                          A("lg", "tc_prop", [1500, 1500], 1.0, {"kind": "logs", "n": 6}),
                          A("x1", "ds_cross", [500, 1250], 1.0, {"on": 1.0, "r": 190}), A("x2", "ds_cross", [1000, 1350], 1.0, {"on": 1.0, "r": 190}),
                          A("x3", "ds_cross", [1500, 1350], 1.0, {"on": 1.0, "r": 190}), lab("dg", "DANGEROUS", [1000, 800], "dangerous|50%", px=110, color=RED)])
    T["s6.l19"] = dict(f="wk", room="house", cams=[[700, 1300, 1.3, 1.4]], cuts=["outdoor|50%"], pose="point", bug=None, mb={"pos": [1600, 1600]},
                       x=[A("can", "tc_prop", [400, 1600], 0.9, {"kind": "aerosol"}, moves=[{"at": "pesticide|20%", "dur": 1.0, "pos": [600, 1600]}]),
                          A("sg", "tc_prop", [800, 1600], 1.0, {"kind": "sign", "text": "NO", "col": "#e5383b", "tcol": "#ffffff", "px": 110})])
    T["s6.l20"] = dict(f="wM", room="board", roomscene="jh_office", pose="shock", bug=None, mb={"pos": [600, 1500]}, look=[1200, 1300],
                       x=[A("cash", "tp_money", [1250, 1500], 1.6, {"q": 1.0}, set=[{"at": "expensive|40%", "dur": 1.5, "p": {"s": 0.3}}])],
                       sfx=["tink@expensive|40%"])
    T["s6.l21"] = dict(f="mM", room="house", pose="point", look="viewer", bug=None, mb={"pos": [900, 1600]},
                       x=[A("ph", "cl_phone", [1120, 1240], 1.3, {})], sfx=["tink@hire|30%"])
    T["s6.l22"] = dict(f="mk", room="house", cams=[[1250, 1300, 1.0, 1.1]], cuts=["heat|55%"], pose="present", look=[1500, 1300], bug=None,
                       mb={"pos": [700, 1600]},
                       x=[A("unit", "cl_box", [2400, 1600], 1.4, {}, moves=[{"at": "methods|20%", "dur": 1.5, "pos": [1500, 1600]}]),
                          lab("hu", "HEAT", [1500, 1150], "heat|55%", px=100, color="#ff7a30")])
    T["s6.l23"] = dict(f="wM", room="roof", pose="deadpan", look="viewer", bug=None, tint=[0.05, 0.08, 0.3, 0.45],
                       mb={"pos": [960, 1500]}, x=[A("bagz", "tp_zzz", [1150, 900], 1.2, {"on": 1.0})])
    T["s6.l24"] = dict(tier="bedbug", big=True)
    # ------------------------------------------------------------------ the final board: the roof at dawn
    T["s7.l0"] = dict(f="wk", room="roof", cams=[[960, 1000, 1.3, 1.35]], cuts=["final|50%"], pose="laugh", bug=None, mb={"pos": [960, 1500]},
                      ov=[{"type": "tier", "in": "board|65%", "placed": [], "mb": "point"}], sfx=["whoosh@board|65%"])
    T["s7.l1"] = dict(f="k", room="board", cams=[[960, 540, 1, 1]], bug=None, mb={"hidden": True}, card=False, cap_y=980,
                      ov=[{"type": "tier", "placed": [], "mb": "shrug",
                           "drops": [["silverfish", "ANNOYING", "Silverfish|5%"], ["mite", "ANNOYING", "dust|20%"],
                                     ["spider", "ANNOYING", "spiders|45%"], ["centipede", "ANNOYING", "centipede|65%"]],
                           "pulse": [["ANNOYING", "annoying|80%"]]},
                          {"type": "zoom", "from": [700, 335, 1.3], "to": [1250, 335, 1.3], "at": 0.0, "linear": True}],
                      sfx=["stamp@Silverfish|5%", "stamp@dust|20%", "stamp@spiders|45%", "stamp@centipede|65%"])
    T["s7.l2"] = dict(f="k", room="board", cams=[[960, 540, 1, 1]], bug=None, mb={"hidden": True}, card=False, cap_y=980,
                      ov=[{"type": "tier", "placed": [[b, RANK[b]] for b in ORDER[:4]],
                           "drops": [["roach", "GROSS", "cockroach|15%"], ["bedbug", "GET OUT", "bed|60%"]],
                           "pulse": [["GROSS", "gross|30%"], ["GET OUT", "get|75%"]]},
                          {"type": "zoom", "from": [900, 560, 1.15], "to": [900, 760, 1.3], "at": 0.0}],
                      sfx=["stamp@cockroach|15%", "hit@bed|60%", "sting@get|75%"])
    T["s7.l3"] = dict(f="k", room="board", cams=[[960, 540, 1, 1]], bug=None, mb={"hidden": True}, card=False, cap_y=980,
                      ov=[{"type": "tier", "placed": [[b, RANK[b]] for b in ORDER], "mb_slot": "mine|50%", "mb": "laugh",
                           "pulse": [["HARMLESS", "Harmless|10%"]]},
                          {"type": "big", "at": "mine|55%", "rows": [["HARMLESS: MEATBALL", 90, YEL]], "x": 1300, "y": 120},
                          {"type": "zoom", "from": [960, 540, 1.0], "to": [760, 230, 1.4], "at": 0.0}],
                      sfx=["pop@mine|55%"])
    T["s7.l4"] = dict(f="wk", room="hall", cams=[[1100, 1350, 1.6, 1.7]], cuts=["case|55%"], pose="point", bug=None, light="off",
                      x=[A("file", "rk_file", [-300, 1440], 0.6, {}, moves=[{"at": "Wednesday|20%", "dur": 0.8, "pos": [1050, 1420]}])],
                      mb={"pos": [1500, 1500]}, sfx=["whoosh@Wednesday|25%"])
    T["s7.l5"] = dict(f="Mm", room="roof", pose="you", look="viewer", bug=None, mb={"pos": [960, 1500]})
    T["s7.l6"] = dict(f="mk", room="bed", cams=[[1180, 1150, 1.4, 1.5]], cuts=["mattress|45%"], pose="deadpan", look="viewer",
                      mb={"prop": "flashlight", "pos": [1700, 1500]}, bug={"hidden": True}, light={"kind": "flashlight", "target": [1100, 1200]})
    return T


SHOTS = _table()

# ================================================================================================ build


def build(outline, out_spec):
    o = json.load(open(outline))
    old = {}
    if os.path.exists(out_spec):
        for ln in json.load(open(out_spec)).get("lines", []):
            old[ln["id"]] = ln
    lines, todo = [], 0
    for si, seg in enumerate(o["segments"]):
        for li, ln in enumerate(seg["lines"]):
            if not ln.get("say", "").strip():   # the end-screen hold: the last spoken line carries it
                continue
            sid = f"s{si}.l{li}"
            L = dict(ln, id=sid, seg=si)
            prev = old.get(sid)
            if prev and prev.get("shot", {}).get("_keep"):
                L["shot"] = prev["shot"]
            elif sid in SHOTS:
                L["shot"] = copy.deepcopy(SHOTS[sid])
            else:
                todo += 1
                L["shot"] = {"f": "wm", "_todo": True}
            tts = L["say"]
            for pat, rep in TTS.items():
                tts = re.sub(pat, rep, tts)
            if tts != L["say"]:
                L["tts"] = tts
            lines.append(L)
    segs = [{k: v for k, v in s.items() if k != "lines"} for s in o["segments"]]
    spec = {"_note": "Built by tools/drawn_ranked.py build from " + os.path.basename(outline) +
                     ". Each line: id (s<seg>.l<line>), the outline fields (say/vis/card/rate/pitch/src) and shot (the "
                     "SHOTS recipe in tools/drawn_ranked.py; \"_keep\": true keeps a hand edit across rebuilds).",
            "voice": "kokoro:adam-puck", "formant": 1.05, "rate": o.get("rate", "+32%"), "pitch": o.get("pitch", "+2Hz"),
            "music": "mystery", "music_db": -16, "tempo": {"lead": 0.0, "tail": 0.02, "thr": 0.01, "cam": 0.7}, "pad": 0.08, "speed_k": 0.70,
            "beat_lines": BEATS, "captions": 122, "caption_y": 870, "cut_whoosh": True, "sfx_gain": 0.24,
            "cap_key": ["bite", "bit", "biter", "harmless", "annoying", "gross", "get", "out", "suspect", "bed", "bug",
                        "silverfish", "mites", "spider", "centipede", "cockroach", "roach", "400", "million", "sixteen",
                        "30", "14", "blood", "disease", "doctor", "never", "twist", "closed", "dinosaurs"],
            "end_hold": float(o.get("end_screen_seconds", 20)), "end_label": o.get("end_screen_video"),
            "segments": segs, "titles": o.get("titles"), "pinned_comment": o.get("pinned_comment"), "lines": lines}
    json.dump(spec, open(out_spec, "w"), indent=1, ensure_ascii=False)
    print(f"{out_spec}: {len(lines)} lines, {sum(len(L['say'].split()) for L in lines)} words, "
          f"{len(lines) - todo} with hand-made shots, {todo} on the default shot")


# ================================================================================================ voice


def _vkey(text, voice, rate, pitch):
    return hashlib.sha1(json.dumps([text, voice, rate, pitch]).encode()).hexdigest()[:16]


def _lv(spec, L):
    return spec["voice"], L.get("rate", spec["rate"]), L.get("pitch", spec["pitch"])


# ---- voice E (Studio 11/17 "VOICE PICK: E"): Kokoro am_adam, every line acted. Directions -> per-line params
# (free_voice: speed = Kokoro speed, pitch = semitones, gain = dB, pause = longest inner silence kept, s).
ACT = {"fact": dict(speed=1.22, pitch=0.0, gain=0.0), "story": dict(speed=1.16, pitch=0.5, gain=0.0),
       "curious": dict(speed=1.14, pitch=1.5, gain=0.0), "scared": dict(speed=1.32, pitch=3.0, gain=1.5),
       "smug": dict(speed=1.02, pitch=-1.0, gain=0.0), "shocked": dict(speed=1.24, pitch=2.5, gain=2.0),
       "shout": dict(speed=1.3, pitch=4.0, gain=4.0)}
DIRECT = {  # line -> direction; the rest: outline +20 % lines = fact, +34 % = scared, others = story
    "s0.l1": "curious", "s0.l5": "smug", "s1.l0": "curious", "s1.l4": "curious", "s1.l6": "smug", "s1.l13": "smug",
    "s2.l0": "curious", "s2.l4": "curious", "s2.l9": "smug", "s2.l10": "shocked", "s3.l0": "curious", "s3.l2": "curious",
    "s4.l0": "curious", "s4.l4": "shout", "s4.l5": "shocked", "s4.l6": "curious", "s4.l9": "smug", "s4.l15": "smug",
    "s5.l0": "shocked", "s5.l4": "curious", "s5.l6": "smug", "s5.l15": "shocked", "s6.l0": "scared", "s6.l1": "scared",
    "s6.l2": "shout", "s6.l3": "shout", "s6.l7": "shocked", "s6.l13": "smug", "s6.l23": "smug", "s7.l3": "smug",
    "s7.l5": "curious"}
PAUSE_IN = 0.2


def direction(L):
    if L.get("act"):   # an outline that directs every line itself (the bathroom episode)
        return L["act"]
    if L["id"] in DIRECT:
        return DIRECT[L["id"]]
    r = L.get("rate")
    return "fact" if r == "+20%" else ("scared" if r == "+34%" else "story")


def _kvoice(spec, L):
    """The line's Kokoro voice string, e.g. kokoro:adam@speed=1.22,pitch=0,gain=0,pause=0.2."""
    a = dict(ACT[L["shot"].get("act") or direction(L)])
    a["speed"] = round(a["speed"] * spec.get("speed_k", 1.0), 3)
    v = "%s@speed=%s,pitch=%s,gain=%s,pause=%s" % (spec["voice"].split("@")[0], a["speed"], a["pitch"], a["gain"], PAUSE_IN)
    if spec.get("formant"):   # voice E2 (Nolan 11/17): formant up 5 %
        v += ",formant=%s" % spec["formant"]
    return v


def _kok(spec):
    return spec["voice"].startswith("kokoro:")


def _kmake(job):
    import free_voice
    v, text = job
    return free_voice.make(v, text)


def _kpath(spec, L):
    import free_voice
    import premium_voice as pv
    v = _kvoice(spec, L)
    return pv.cached(free_voice.cache_name(v), L["say"]), v


def voice_cache(spec, lines):
    """Make sure every line's take is in the cache (5 tries each, empty/silent takes refused)."""
    import asyncio
    if _kok(spec):
        jobs = [(_kvoice(spec, L), L["say"]) for L in lines if not _kpath(spec, L)[0]]
        if jobs:
            print(f"voice E: {len(jobs)} new line(s)", flush=True)
            import multiprocessing as mp
            with mp.get_context("spawn").Pool(int(os.environ.get("KOKORO_JOBS", "3"))) as pool:
                for k, _ in enumerate(pool.imap_unordered(_kmake, jobs)):
                    if k % 10 == 0:
                        print(f"  voiced {k + 1}/{len(jobs)}", flush=True)
        return
    from facts import speak
    os.makedirs(CACHE, exist_ok=True)
    todo = {}
    for L in lines:
        v, r, p = _lv(spec, L)
        text = L.get("tts", L["say"])
        c = os.path.join(CACHE, _vkey(text, v, r, p) + ".mp3")
        if not (os.path.exists(c + ".words.json") and ds._good(c, json.load(open(c + ".words.json")))):
            todo[c] = (text, v, r, p)

    async def one(c, text, v, r, p, sem):
        async with sem:
            for k in range(5):
                tmp = c + ".tmp.mp3"
                try:
                    words = await speak(text, v, tmp, r, p)
                except Exception as e:  # noqa: BLE001
                    print(f"  tts retry {k + 1}/5 ({type(e).__name__}): {text[:50]}", flush=True)
                    await asyncio.sleep(2 + 2 * k)
                    continue
                if ds._good(tmp, words):
                    os.replace(tmp, c)
                    json.dump(words, open(c + ".words.json", "w"))
                    return
                await asyncio.sleep(2 + 2 * k)
            raise SystemExit(f"ranked: no usable voice after 5 tries for: {text!r}")

    async def run():
        sem = asyncio.Semaphore(4)
        await asyncio.gather(*(one(c, *a, sem) for c, a in todo.items()))
    if todo:
        print(f"voice: {len(todo)} new line(s)", flush=True)
        asyncio.run(run())


def _cpath(spec, L):
    if _kok(spec):
        return _kpath(spec, L)[0]
    v, r, p = _lv(spec, L)
    return os.path.join(CACHE, _vkey(L.get("tts", L["say"]), v, r, p) + ".mp3")


def durations(spec, lines):
    out = {}
    for L in lines:
        c = _cpath(spec, L)
        try:
            w = json.load(open(c + ".words.json"))
            out[L["id"]] = max(0.5, w[-1][1] - w[0][0] + 0.05)
        except (OSError, ValueError, IndexError):
            out[L["id"]] = max(1.0, len(L["say"].split()) / 3.4)
    return out


def voice_into(spec, beats, lines, work):
    import shutil
    os.makedirs(work, exist_ok=True)
    for i, (b, L) in enumerate(zip(beats, lines)):
        v, r, p = _lv(spec, L)
        if _kok(spec):
            v = b["voice"]
        c = _cpath(spec, L)
        mp3 = f"{work}/v{i:02d}.mp3"
        shutil.copy(c, mp3)
        shutil.copy(c + ".words.json", mp3 + ".words.json")
        open(mp3 + ".key", "w").write(drawn.line_key(b["say"], v, r, p))


# ================================================================================================ expand


def _parse_card(card):
    """Outline card -> (suspect text, id dict {name, rows: [...]}, tier, other rows)."""
    out = {"suspect": None, "id": None, "tier": None, "rows": []}
    if not card:
        return out
    parts = [x.strip() for x in card.split("·")]
    mode = None
    for x in parts:
        if x.startswith("SUSPECT "):
            out["suspect"] = x
            mode = None
        elif x.startswith("BUG ID:"):
            out["id"] = {"name": x.split(":", 1)[1].strip(), "rows": []}
            mode = "id"
        elif re.match(r"^(ID )?ROW \d:", x):
            out["id"] = out["id"] or {"name": None, "rows": []}
            out["id"]["rows"].append(x.split(":", 1)[1].strip())
            mode = "id"
        elif x.startswith("TIER:"):
            out["tier"] = x.split(":", 1)[1].strip()
            mode = None
        elif x.startswith("#"):
            continue
        elif mode == "id" and out["id"]["rows"] and not out["id"]["name"] is None and len(out["id"]["rows"]) and False:
            pass
        elif mode == "id" and out["id"] and out["id"]["rows"]:
            out["id"]["rows"][-1] += (", " if len(x.split()) <= 2 else ": ") + x   # "CELLAR SPIDER: NOT KNOWN..."
        elif mode == "id" and out["id"] and not out["id"]["rows"]:
            out["id"]["rows"].append(x.split(":", 1)[-1].strip() if x.startswith("FOSSILS") is False else x)
        else:
            out["rows"].append(x)
            mode = None
    return out


def states(spec):
    """Per line: the chapter's BUG ID rows so far (name, rows before, rows after, first?), tier placements before."""
    st, ids, placed = {}, {}, []
    for L in spec["lines"]:
        c = _parse_card(L.get("card"))
        seg = L["seg"]
        bug = CH_BUG[seg]
        cur = ids.get(seg)
        idinfo = None
        if c["id"] and bug:
            if cur is None:
                cur = {"name": c["id"]["name"] or BUGS[bug][4], "rows": []}
                first = True
            else:
                first = False
            n0 = len(cur["rows"])
            cur["rows"] = cur["rows"] + c["id"]["rows"]
            ids[seg] = cur
            idinfo = {"name": cur["name"], "rows": list(cur["rows"]), "n0": n0, "first": first, "bug": bug}
        tier = None
        if L["shot"].get("tier"):
            b = L["shot"]["tier"]
            tier = {"placed": [list(x) for x in placed], "drop": [b, RANK[b]]}
            placed.append([b, RANK[b]])
        st[L["id"]] = {"card": c, "id": idinfo, "tier": tier}
    return st


def _cams(kind, kit, hero, mbx, a, i):
    """A framing -> [cam, to]."""
    msize = MB_SIZE
    fy = a.get("_mby", 1500)   # Meatball's feet (1500 in the rooms, 1600 outside the house)
    bpos = hero["pos"] if hero else kit.get("bpos") or [960, 1300]
    bug = kit.get("bug_key")
    bw, bh = (BUGS[bug][2], BUGS[bug][3]) if bug else (500, 300)
    s = hero["s"] if hero else 0.5
    if a.get("bugpos_for_frame"):
        bpos = a["bugpos_for_frame"]
    if kind == "w":
        if mbx is None:
            cx, z = bpos[0], 0.95
        else:
            cx = (mbx + bpos[0]) / 2
            span = abs(bpos[0] - mbx) + 1000
            z = max(0.78, min(1.1, 1750 / span))
        cy = fy - 420 / z
        top = min(bpos[1] - bh * s, fy - 0.85 * msize)
        cy = min(cy, top + (540 - 120) / z)
        c = [cx, cy, z]
        return [c, [cx + (18 if i % 2 else -18) / z, cy - 6 / z, z * 1.07]]
    if kind in ("m", "M"):
        z = 1.5 if kind == "m" else 2.3
        hy = fy - 0.72 * msize
        cy = hy + (540 - (330 if kind == "m" else 470)) / z
        cx = mbx + (90 if kind == "m" else 0) * (1 if i % 2 else -1)
        c = [cx, cy, z]
        return [c, [cx, cy - 8 / z, z * (1.08 if kind == "m" else 1.06)]]
    if kind in ("b", "i"):
        zb = a.get("zb") or max(1.0, min(3.0, 1300 / (bw * s)))
        cx = bpos[0] + (470 / zb if kind == "i" else 0)
        cy = bpos[1] - 0.45 * bh * s
        c = [cx, cy, zb]
        return [c, [cx - (25 / zb if kind == "b" else 0), cy, zb * 1.08]]
    raise ValueError(kind)


def expand(spec, lines, durs):
    segs = spec["segments"]
    allL = spec["lines"]
    ST = states(spec)
    beats = []
    for L in lines:
        a = L["shot"]
        seg = L["seg"]
        st = ST[L["id"]]
        last = L["id"] == allL[-1]["id"]
        pad = _pad(spec, L)
        D0 = durs[L["id"]]
        D = D0 + pad
        b = {"say": L["say"], "rate": _lv(spec, L)[1], "pitch": _lv(spec, L)[2], "norecut": True, "recut": False}
        if _kok(spec):
            b["voice"] = _kvoice(spec, L)
        if L.get("tts"):
            b["tts"] = L["tts"]
        rk = []
        sfx = list(a.get("sfx", []))
        if a.get("tier"):   # ---- the tier board drop
            bug = a["tier"]
            t_ = st["tier"]
            b.update(scene="rk_board_bg", scene_p={}, actors=[], mb=dict(ds.HIDDEN))
            b["shots"] = [{"cam": [960, 540, 1.0], "to": [960, 540, 1.0]}]
            word = a.get("drop_at") or {"ANNOYING": "annoying", "GROSS": "gross", "GET OUT": "get"}[t_["drop"][1]] + "|85%"
            rk.append({"type": "tier", "placed": t_["placed"], "drops": [t_["drop"] + [word]]})
            ry = 14 + TIERS.index(t_["drop"][1]) * 214 + 107
            rk.append({"type": "zoom", "from": [960, 540, 1.0], "to": [960, 500, 1.06], "at": 0.0, "until": "45%"})
            rk.append({"type": "zoom", "from": [1150, ry - 40, 1.4], "to": [1150, ry, 1.48], "at": "45%", "wait": True})
            rk.append({"type": "big", "at": word, "rows": [[t_["drop"][1], 130, TCOL[t_["drop"][1]]]], "x": 1000, "y": 560})
            sfx = ["whoosh@0.02", ("stamp@" if not a.get("big") else "sting@") + word, "hit@" + word.split("|")[0] + "+0.12|95%"]
            b["cap_y"] = 980
            if a.get("big"):
                b["flash"] = [word]
                rk[-1]["rows"] = [["GET OUT  #1", 150, RED]]
        else:
            room = a.get("room", CH_ROOM[seg])
            kit = dict(ROOMS[room])
            scene = a.get("roomscene", kit["scene"])
            bug = kit.get("bug") if room not in ("cork", "board", "roof", "house") else None
            bug = bug if room != "board" else None
            if room in ("cork", "board", "roof", "house"):
                bug = None
            kit["bug_key"] = bug
            actors = []
            hero = None
            if bug and a.get("bug", 0) is not None:
                bo = a.get("bug") or {}
                typ = BUGS[bug][0]
                hero = A("hero", typ, bo.get("pos", kit["bpos"]), bo.get("s", kit["bs"]),
                         dict({"mood": "calm", "look": [-0.6, 0.1]}, **bo.get("p", {})))
                hero["p"]["hidden"] = bool(bo.get("hidden"))   # explicit: drawn.plan carries actor params line to line
                for k in ("moves", "rot", "flip", "set"):
                    if k in bo:
                        hero[k] = copy.deepcopy(bo[k])
                if typ != "cellar_spider" and kit["bpos"][0] > (kit.get("mx") or 0) and "flip" not in bo:
                    hero["flip"] = True   # face Meatball
                actors.append(hero)
            actors += copy.deepcopy(a.get("x", []))
            mbo = dict(a.get("mb", {}))
            mbx = None if kit.get("mx") is None and not mbo.get("pos") else (mbo.get("pos") or [kit["mx"]])[0]
            if mbo.get("hidden") or kit.get("mx") is None and not mbo.get("pos"):
                mbd = dict(ds.HIDDEN)
                mbx = None
            else:
                pose = a.get("pose") or POSE_ROT[sum(map(ord, L["id"])) % len(POSE_ROT)]
                look = a.get("look", "hero" if hero is not None and not hero["p"].get("hidden") else "viewer")
                mbd = {"pose": pose, "pos": list(mbo.get("pos", [kit["mx"], 1500])), "size": mbo.get("size", MB_SIZE),
                       "look": look, "prop": mbo.get("prop"), "hidden": False}
                for k in ("moves", "gest", "shake"):
                    if k in mbo:
                        mbd[k] = copy.deepcopy(mbo[k])
            b.update(scene=scene, scene_p=dict(kit["sp"]), actors=actors, mb=mbd)
            # ---- camera: framings, each a cut, each a push; long lines cycle them (<= ~3.6 s a framing)
            f = a.get("f", "wm")
            cams = a.get("cams") or []
            cuts = list(a.get("cuts", []))[:max(0, len(f) - 1)]
            if cuts and len(cuts) == len(f) - 1:
                ats = [0.0] + cuts
            else:
                n_ = max(len(f), math.ceil(D / 2.6))
                ats = [0.0] + [round(D * k / n_, 2) for k in range(1, n_)]
            kinds = [f[j % len(f)] for j in range(len(ats))]
            # Studio 11/17 (scene detect): no framing longer than MAXSEG s. Resolve the word anchors on the cached take,
            # then split any long stretch with a hard contrast cut (bug close-up <-> Meatball face, or a big punch-in).
            wds = _words_of(spec, L)
            tt = [0.0] + [_at_s(wds, x, D0) for x in ats[1:]]
            order = sorted(range(len(ats)), key=lambda q: tt[q])
            ats, kinds, tt = [ats[q] for q in order], [kinds[q] for q in order], [tt[q] for q in order]
            bug_on = hero is not None and not hero["p"].get("hidden")
            mb_on = not mbd.get("hidden")
            k2, a2, t2 = [], [], []
            for q in range(len(ats)):
                end = tt[q + 1] if q + 1 < len(ats) else D
                pieces = max(1, math.ceil((end - tt[q]) / MAXSEG))
                for r_ in range(pieces):
                    st_ = tt[q] + (end - tt[q]) * r_ / pieces
                    if r_ == 0:
                        k2.append(kinds[q])
                        a2.append(ats[q])
                    else:
                        prevk = k2[-1]
                        if prevk in "mMw" and bug_on:
                            k2.append("b")
                        elif prevk in "bi" and mb_on:
                            k2.append("M")
                        elif prevk == "m" or prevk == "w":
                            k2.append("M" if mb_on else "P")
                        elif prevk == "M" and mb_on:
                            k2.append("w")
                        else:
                            k2.append("P")   # a hard punch-in on the previous framing
                        a2.append(round(st_, 2))
                    t2.append(st_)
            kinds, ats = k2, a2
            n = len(ats)
            shots = []
            ki = 0
            for j in range(n):
                kind = kinds[j]
                if kind == "P":
                    pc = shots[-1]["to"] if shots else [960, 1000, 1.0]
                    c0 = [pc[0], pc[1] - 40 / pc[2], round(min(4.0, pc[2] * 1.7), 3)]
                    c1 = [c0[0], c0[1], round(c0[2] * 1.05, 3)]
                elif kind == "k":
                    cc = cams[ki % len(cams)] if cams else [960, 1000, 1.0, 1.05]
                    ki += 1
                    c0, c1 = [cc[0], cc[1], cc[2]], [cc[0] + (12 if j % 2 else -12) / cc[2], cc[1], cc[3]]
                    if a.get("pans") and j == 0:
                        c0, c1 = a["pans"][0], a["pans"][1]
                else:
                    c0, c1 = _cams(kind, kit, hero, mbx if mbx is not None else (kit.get("mx") or 960),
                                   dict(a, _mby=mbd["pos"][1] if not mbd.get("hidden") else 1500), j)
                if j and shots and abs(shots[-1]["to"][2] - c0[2]) / c0[2] < 0.25 and abs(shots[-1]["to"][0] - c0[0]) * c0[2] < 400:
                    # Studio 11/17 (scene detect missed the soft re-frames): the same framing twice becomes a hard
                    # punch-in (x1.55) on the subject or a pull-back, so every cut reads as a cut
                    kz = 1.55 if j % 2 else 0.68
                    c0 = [c0[0], c0[1] - (0 if kz < 1 else 60 / c0[2]), round(max(0.6, c0[2] * kz), 3)]
                    c1 = [c0[0], c0[1], round(c0[2] * 1.05, 3)]
                sh = {"cam": [round(x, 3) for x in c0], "to": [round(x, 3) for x in c1]}
                if j:
                    sh["at"] = ats[j]
                shots.append(sh)
            b["shots"] = shots
            # Studio 11/17 (scene detect, same-palette rooms): every bug close-up is a BUG CAM (dark ring), so the
            # cut into and out of it reads as a cut; not on lines with their own interrupt, the ID card or a board
            has_cam = any(o.get("type") == "cam" for o in a.get("ov", [])) or room in ("scope", "board", "cork")
            if not has_cam and (bug_on or a.get("ring_k")) and not a.get("no_bugcam"):
                for j in range(n):
                    if kinds[j] == "b" or (kinds[j] == "P" and j and kinds[j - 1] == "b") or (kinds[j] == "k" and a.get("ring_k")):
                        rk.append({"type": "cam", "kind": "bugcam", "at": ats[j] if j else 0.0,
                                   "to": ats[j + 1] if j + 1 < n else None, "nolabel": j > 0 and kinds[j - 1] == "b"})
            # Meatball's face close-ups get a comic reaction burst behind him (a hard, readable cut in every room)
            ms = [j for j in range(n) if kinds[j] == "M"]
            bmode = spec.get("burst", "all")   # "loud": only shocked / shout / scared lines (or a shot's burst: true)
            if bmode == "loud" and not a.get("burst") and direction(L) not in ("shocked", "shout", "scared"):
                ms = []
            if ms and not mbd.get("hidden") and not a.get("no_burst"):
                sets = []
                for j in ms:
                    sets.append({"at": ats[j] if j else 0.0, "p": {"on": 1.0}})
                    if j + 1 < n:
                        sets.append({"at": ats[j + 1], "p": {"on": 0.0}})
                b["actors"].insert(0, A("burst", "rk_burst", [0, 0], 1.0, {"on": 0.0, "col": BURST[sum(map(ord, L["id"])) % len(BURST)]}, set=sets))
            if not mbd.get("hidden"):
                mx_ = mbd["pos"][0]
                zs = [sh[k][2] for sh in shots for k in ("cam", "to") if abs((mx_ - sh[k][0]) * sh[k][2]) < 1100]
                if zs:
                    need = 600 / min(zs)   # 0.785 * size * z >= 0.44 * 1080
                    if need > mbd["size"]:
                        mbd["size"] = round(min(1150, need))
            lt = a.get("light", kit.get("light", "off"))
            if lt != "off":
                b["light"] = lt if isinstance(lt, dict) else {"kind": lt}
            for k in ("tint", "flash", "shake", "freak", "cap_y"):
                if a.get(k):
                    b[k] = a[k]
            if a.get("stamp"):
                stp = a["stamp"]
                b["actors"].append({"id": "stamp", "type": "ds_stamp", "pos": [0, 0], "front": True,
                                    "p": dict({"on": 0.0}, **{k: v for k, v in stp.items() if k != "at"}),
                                    "set": [{"at": stp.get("at", "40%"), "dur": 0.25, "p": {"on": 1.0}}]})
        # ---- re-hook card, BUG ID card, screen overlays
        c = st["card"]
        if c["suspect"]:
            n_ = c["suspect"].split()[1]
            rk.append({"type": "suspect", "text": c["suspect"], "at": 0.0, "kicker": segs[seg]["chapter"].split(":")[-1].strip().upper()})
            sfx = ["sting@0", "hit@0.05"] + sfx
        if st["id"]:
            ii = st["id"]
            f_ = a.get("f", "")
            rk.append({"type": "idcard", "name": ii["name"], "rows": ii["rows"], "kind": ii["bug"], "n": len(ii["rows"]),
                       "new": True, "first": ii["first"], "in": a.get("id_in", "35%" if c["suspect"] else ("0%" if not ii["first"] else _first_i(a))),
                       "at": a.get("id_at", "45%" if c["suspect"] else ("10%" if not ii["first"] else _first_i(a))),
                       "x": a.get("idx", 1430)})
            sfx = sfx + [f"pop@{rk[-1]['at']}"]
        rk += copy.deepcopy(a.get("ov", []))
        prev = allL[allL.index(L) - 1] if allL.index(L) else None
        if prev is not None and prev["shot"].get("tier") and not a.get("tier"):   # the drop lands: hold it through the cut
            pt = ST[prev["id"]]["tier"]
            rk.append({"type": "tier", "placed": pt["placed"] + [pt["drop"]], "off": 0.45,
                       "mb": "shock" if pt["drop"][1] == "GET OUT" else "point"})
        b["rk"] = rk
        # ---- the outline card (other rows) at the top
        rows = c["rows"] if a.get("card") is None else ([x.strip() for x in a["card"].split("·")] if a.get("card") else [])
        if rows and not a.get("tier"):
            px = a.get("card_px", 92)
            cx = a.get("card_x", 700 if st["id"] else W // 2)
            mw = 1150 if st["id"] else 1700
            crow = []
            for k, r in enumerate(rows):
                f = ImageFont.truetype(FONT, px if k == 0 else int(px * 0.8))
                p_ = px if k == 0 else int(px * 0.8)
                while f.getlength(r) > mw and p_ > 50:
                    p_ -= 6
                    f = ImageFont.truetype(FONT, p_)
                crow.append([r, YEL if k == 0 else "#ffffff", p_])
            b["card"] = {"rows": crow, "y": 24, "at": a.get("card_at", "8%" if not c["suspect"] else "1.5"), "x": cx}
        b["sfx"] = sfx
        if last:
            b["actors"].append({"id": "end", "type": "kk_end", "pos": [0, 0], "front": True,
                                "p": {"on": 0.0, "label": spec.get("end_text", "HOUSE CENTIPEDE  ·  HOUSE GUESTS")},
                                "set": [{"at": "100%", "dur": 0.5, "p": {"on": 1.0}}]})
            b["pad"] = spec.get("end_hold", 20.0)
        else:
            b["pad"] = pad
        b["ds_id"] = L["id"]
        b["kk_shots"] = copy.deepcopy(b["shots"])   # already 16:9 camera terms (drawn_keepkill keeps them as they are)
        beats.append(b)
    return beats


# Voice fix (Studio 11/17 "KILL THE PAUSES"): lines butt together (gap <= 0.12 s, spec "pad" + the TTS trim);
# a 0.3 s beat only on the gap BEFORE a punchline or reveal, at most one per 30 s (the gap lint checks it).
BEATS = ["s0.l4", "s1.l12", "s2.l8", "s3.l10", "s4.l8", "s6.l1", "s7.l2"]
BEAT_PAD = 0.3


MAXSEG = 2.8   # longest framing (s); with a hard contrast cut at each split


def _words_of(spec, L):
    try:
        w = json.load(open(_cpath(spec, L) + ".words.json"))
        s0 = w[0][0]
        return [(a - s0, b - s0, x) for a, b, x in w]
    except (OSError, ValueError, IndexError, TypeError):
        return []


def _at_s(words, at, D0):
    if isinstance(at, (int, float)):
        return float(at)
    try:
        return drawn.at_time(words, at) if words else _pct(at) / 100 * D0
    except SystemExit:
        return _pct(at) / 100 * D0


def _pad(spec, L):
    a = L["shot"]
    if "pad" in a:
        return a["pad"]
    if L["id"] in spec.get("beat_lines", BEATS):
        return BEAT_PAD
    return spec.get("pad", 0.08)


def _pct(x):
    if isinstance(x, (int, float)):
        return 0.0
    m = re.search(r"(\d+)%$", x)
    return float(m.group(1)) if m else 50.0


def _first_i(a):
    """When the ID card lands on its first line: at the cut to the 'i' framing."""
    f = a.get("f", "")
    if "i" in f and f.index("i") > 0 and a.get("cuts"):
        return a["cuts"][f.index("i") - 1]
    return "8%"


def drawn_spec(spec, lines):
    durs = durations(spec, lines)
    out = {k: spec[k] for k in ("voice", "rate", "pitch", "music", "music_db", "captions", "caption_y", "cut_whoosh",
                                "cap_key", "sfx_gain", "tempo") if k in spec}
    out.update(beats=expand(spec, lines, durs), recut=False, stage={}, ds={"pause": [], "music_out": []})
    return out


# ================================================================================================ render / sheets


def _pick(spec, rng):
    if not rng:
        return spec["lines"]
    if re.match(r"^s\d+$", rng):   # a chapter
        return [L for L in spec["lines"] if L["seg"] == int(rng[1:])]
    a, b = rng.split("-")
    return spec["lines"][int(a):int(b) + 1]


def render(spec_path, out, rng=None, work=None):
    spec = json.load(open(spec_path))
    lines = _pick(spec, rng)
    voice_cache(spec, lines)
    dsx = drawn_spec(spec, lines)
    work = work or os.path.join("/dev/shm", ".work-" + os.path.splitext(os.path.basename(out))[0])
    os.makedirs(work, exist_ok=True)
    voice_into(spec, dsx["beats"], lines, work)
    sp = os.path.join(work, "drawn_spec.json")
    json.dump(dsx, open(sp, "w"), indent=1)
    sys.argv = ["drawn.py", sp, out, "--work", work]
    os.environ.setdefault("CRF", "24")
    os.environ.setdefault("DRAWN_PRESET", "veryfast")
    drawn.main()
    drawn_treecheck.loudness(out)


def _setup_one(spec, L, work):
    dsx = drawn_spec(spec, [L])
    w = os.path.join(work, L["id"])
    voice_into(spec, dsx["beats"], [L], w)
    beats, total = drawn.plan(drawn.drawn_macros.expand(dsx), w)
    drawn.G.update(fps=30, beats=beats, rigs=drawn.rig_tracks(beats, 30), caps=drawn.caption_chunks(beats),
                   cap_px=dsx.get("captions", 60), cap_y=dsx.get("caption_y", 990), counter=None,
                   cap_key=set(dsx.get("cap_key", ())), ticks=[], raw_out=False, nocap_out=False)
    return beats


def _frame(spec, L, frac, work):
    beats = _setup_one(spec, L, work)
    f = int(frac * beats[0]["speech"] * 30)
    arr = np.frombuffer(drawn.frame_at(f)[-1], np.uint8).reshape(H, W, 4)
    return Image.fromarray(arr[..., [2, 1, 0]].copy()), beats[0]["dur"]


def linesheet(spec_path, out, only=None, frac=0.6, work="/dev/shm/ranked-lines", cols=5, big=None, fracs=None):
    spec = json.load(open(spec_path))
    sel = [L for L in spec["lines"] if not only or L["id"] in only]
    voice_cache(spec, sel)
    tiles = []
    for L in sel:
        for fr in (fracs or [L["shot"].get("sheet_at", frac)]):
            im, dur = _frame(spec, L, fr, work)
            if big:
                im.save(os.path.join(big, f"{L['id']}-{fr}.png"))
            im = im.resize((480, 270))
            d = ImageDraw.Draw(im)
            d.rectangle((0, 246, 170, 270), fill=(0, 0, 0))
            d.text((4, 250), f"{L['id']} {dur:.1f}s @{fr}", fill=(255, 255, 0))
            tiles.append(im)

    def sheet(ts, path):
        rows = (len(ts) + cols - 1) // cols
        s = Image.new("RGB", (480 * cols, 270 * rows))
        for i, im in enumerate(ts):
            s.paste(im, ((i % cols) * 480, (i // cols) * 270))
        s.save(path, quality=82)
    if len(tiles) <= 30:
        sheet(tiles, out)
    else:
        base = os.path.splitext(out)[0]
        for k in range(0, len(tiles), 30):
            sheet(tiles[k:k + 30], f"{base}-{k // 30 + 1}.jpg")
    print("linesheet:", out, len(tiles))


def check(spec_path, quiet=False):
    """Plan the whole episode (voice from the cache): runtime, the longest hold between camera events, MB sizes."""
    spec = json.load(open(spec_path))
    voice_cache(spec, spec["lines"])
    durs = durations(spec, spec["lines"])
    dsx = drawn_spec(spec, spec["lines"])
    work = "/dev/shm/ranked-check"
    voice_into(spec, dsx["beats"], spec["lines"], work)
    beats, total = drawn.plan(drawn.drawn_macros.expand(dsx), work)
    ev = []
    for b in beats:
        ev.append((b["t0"], b["ds_id"]))
        for s in b["shots"][1:]:
            ev.append((b["t0"] + s["at"], b["ds_id"]))
    ev.sort()
    if quiet:
        return beats, total
    gaps = sorted(((ev[i + 1][0] - ev[i][0], ev[i][1], ev[i][0]) for i in range(len(ev) - 1)), reverse=True)[:8]
    print(f"runtime {total:.1f} s ({int(total // 60)}:{total % 60:04.1f}), {len(beats)} lines, {len(ev)} cuts")
    for g, i, t in gaps:
        print(f"  hold {g:.2f} s from {t:.1f} s ({i})")
    for b in beats:
        if b["ds_id"].endswith(".l0"):
            print(f"  {b['ds_id']} starts {int(b['t0'] // 60)}:{b['t0'] % 60:04.1f}")
    return beats, total


def gap_lint(spec_path, wav, report):
    """Voice-only stem on the render's timeline + ffmpeg silencedetect (-40 dB, 0.25 s). FAIL on any gap over 0.3 s
    that is not a marked beat (the gap after a line in spec "beat_lines") or the end screen. Writes the report."""
    import wave
    spec = json.load(open(spec_path))
    beats, total = check(spec_path, quiet=True)
    SR = drawn.SR
    n = int(total * SR) + SR
    v = np.zeros(n, np.float32)
    for b in beats:
        o = int(b["t0"] * SR)
        v[o:o + len(b["audio"])] += b["audio"][:max(0, n - o)]
    v = v[:int(total * SR)]
    with wave.open(wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(v, -1, 1) * 32767).astype("<i2").tobytes())
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", wav, "-af", "silencedetect=noise=-40dB:d=0.25", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)] + [total]
    beat_ids = set(spec.get("beat_lines", BEATS))
    last_speech = beats[-1]["t0"] + beats[-1]["speech"]
    words = sum(len(b["say"].split()) for b in beats)
    lines, fails, beat_times = [], 0, []
    for a, z in zip(starts, ends):
        g = z - a
        nxt = [i for i, b in enumerate(beats) if abs(b["t0"] - z) < 0.12]   # the silence runs into a line's start
        if nxt and nxt[0] > 0:
            bi, inside = nxt[0] - 1, False
        else:
            bi = max(i for i, b in enumerate(beats) if b["t0"] <= a + 1e-6)
            inside = True
        b = beats[bi]
        where = f"{b['ds_id']} {'inside the line' if inside else 'after the line'}"
        if a >= last_speech - 0.1:
            verdict = "ok (end screen: music only)"
        elif g <= 0.3:
            verdict = "ok (<= 0.3 s)"
        elif not inside and b["ds_id"] in beat_ids and g <= 0.45:
            verdict = "ok (marked beat before a punchline/reveal)"
            beat_times.append(a)
        else:
            verdict = "FAIL"
            fails += 1
        lines.append(f"{int(a // 60)}:{a % 60:05.2f}  gap {g:.2f} s  {where}  {verdict}")
    close = [(x, y) for x, y in zip(beat_times, beat_times[1:]) if y - x < 30]
    gaps = [beats[i + 1]["t0"] - (beats[i]["t0"] + beats[i]["speech"]) for i in range(len(beats) - 1)]
    head = [f"GAP LINT {'PASS' if not fails and not close else 'FAIL'}: {os.path.basename(wav)}",
            f"rule: silencedetect -40 dB, d=0.25 s; fail any gap > 0.3 s that is not a marked beat (max 1 per 30 s)",
            f"runtime {total:.1f} s ({int(total // 60)}:{total % 60:04.1f}) incl. the {spec.get('end_hold', 20):.0f} s end screen; "
            f"speech ends {int(last_speech // 60)}:{last_speech % 60:04.1f}",
            f"words {words}; pace {words / (last_speech / 60):.0f} wpm over the spoken part",
            f"line-to-line gaps (end of one take to the start of the next, after the trim): median {sorted(gaps)[len(gaps) // 2]:.3f} s, "
            f"max {max(gaps):.3f} s; marked beats: {', '.join(sorted(beat_ids))} (0.3 s)",
            f"silences >= 0.25 s found: {len(lines)}; fails: {fails}; beats closer than 30 s: {len(close)}", ""]
    open(report, "w").write("\n".join(head + lines) + "\n")
    print("\n".join(head[:6]))
    return not fails and not close


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("spec")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--lines")
    ap.add_argument("--work")
    ap.add_argument("--only")
    ap.add_argument("--big")
    ap.add_argument("--frac", type=float, default=0.6)
    ap.add_argument("--fracs")
    x = ap.parse_args()
    if x.cmd == "build":
        build(x.spec, x.out)
    elif x.cmd == "render":
        render(x.spec, x.out, x.lines, x.work)
    elif x.cmd == "linesheet":
        linesheet(x.spec, x.out, x.only.split(",") if x.only else None, x.frac, x.work or "/dev/shm/ranked-lines", big=x.big,
                  fracs=[float(v) for v in x.fracs.split(",")] if x.fracs else None)
    elif x.cmd == "check":
        check(x.spec)
    elif x.cmd == "lint":
        if x.out and x.out.lower().endswith((".mp4", ".mov", ".mkv")):   # 11/18: lint once wrote its wav over the render
            sys.exit("lint: OUT is the voice-stem .wav to write, not the video (%s)" % x.out)
        ok = gap_lint(x.spec, x.out, os.path.splitext(x.out)[0] + "-gaps.txt" if not x.work else x.work)
        sys.exit(0 if ok else 1)
    elif x.cmd == "voice":
        spec = json.load(open(x.spec))
        voice_cache(spec, spec["lines"])
    else:
        raise SystemExit(__doc__)
