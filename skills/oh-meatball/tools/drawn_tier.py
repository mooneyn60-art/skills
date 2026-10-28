"""Drawn tier board (S / A / B / C / D / F) for ranked drawn videos ("I Ranked Every Creature Living In Your House").

One actor, "tierboard", drawn at its pos (top centre of the board, local width 900, row height 150). Params:
  icons    [{"type": actor name, "p": {...}} | {"cfg": inline creature config}, "tier": "F"], in drop order
  drop     0..1: how far the LAST icon has fallen into its row (1 = landed; earlier icons are already in place)
  hide_s   true: the S row is covered by a dark "?" panel (the top-tier reveal is saved for the end)
  unveil   0..1: slides the S cover away
  glow     0..1: a pulse behind the newest icon's row
Icons are the same drawn creatures the segments use, scaled to fit a slot. The tier letters are the only text
(part of the drawn board, like a sign in a scene). drawn.py registers it: ACTORS["tierboard"].
"""
import math
import os

import cairo

from drawn_kit import INK, OUT, back_out, ease, hexc, ink, p_rrect, src

ACT = {}           # drawn.py fills this with its ACTORS table
ROW, W, LAB = 150, 900, 150
TIERS = "SABCDF"
COL = {"S": "#ff5a5a", "A": "#ff9f43", "B": "#ffd34d", "C": "#8be06a", "D": "#6ab7ff", "F": "#b8b8c8"}
FONT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "brand/fonts/Anton-Regular.ttf")
_LET, _ICON = {}, {}


def _letter(ch, px=110):
    if ch not in _LET:
        from PIL import Image, ImageDraw, ImageFont
        f = ImageFont.truetype(FONT, px)
        im = Image.new("RGBA", (px * 2, px * 2), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.text((px, px), ch, font=f, fill=(255, 255, 255, 255), anchor="mm", stroke_width=6, stroke_fill=(17, 17, 17, 255))
        import numpy as np
        a = np.asarray(im, dtype=np.uint16)
        al = a[..., 3:4]
        pre = (a[..., :3] * al // 255).astype(np.uint8)
        buf = np.concatenate([pre[..., ::-1], al.astype(np.uint8)], axis=2).copy()
        _LET[ch] = (cairo.ImageSurface.create_for_data(memoryview(buf), cairo.FORMAT_ARGB32, im.width, im.height,
                                                       im.width * 4), buf, px)
    return _LET[ch]


def _icon(ic):
    """A recording of the creature drawn once, plus the scale/offset that fits it into a 130 px slot."""
    key = repr(sorted((k, repr(v)) for k, v in ic.items() if k != "tier"))
    if key not in _ICON:
        rec = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, None)
        c = cairo.Context(rec)
        p = dict({"mood": "happy", "look": [0, 0]}, **ic.get("p", {}))
        if "cfg" in ic:
            ACT["creature"](c, 0.0, dict(p, cfg=ic["cfg"]))
        else:
            ACT[ic["type"]](c, 0.0, p)
        x, y, w, h = rec.ink_extents()
        k = min(140 / max(w, 1), 124 / max(h, 1))
        _ICON[key] = (rec, k, x + w / 2, y + h / 2)
    return _ICON[key]


def _slot(icons, i):
    tier = icons[i]["tier"]
    n = sum(1 for ic in icons[:i] if ic["tier"] == tier)
    return TIERS.index(tier), n


def board(ctx, t, p):
    icons = p.get("icons", [])
    drop = p.get("drop", 1.0)
    hide = p.get("hide_s", False)
    unveil = p.get("unveil", 0.0)
    glow = p.get("glow", 0.0)
    x0 = -W / 2
    # frame
    ctx.save()
    p_rrect(ctx, x0 - 16, -16, W + 32, ROW * 6 + 32, 26)
    src(ctx, hexc("#3a2c22"))
    ctx.fill_preserve()
    ink(ctx, OUT * 1.2)
    ctx.restore()
    newest = len(icons) - 1
    for r, tier in enumerate(TIERS):
        y = r * ROW
        ctx.save()   # row body
        ctx.rectangle(x0 + LAB, y, W - LAB, ROW)
        src(ctx, hexc("#2b2b33") if r % 2 == 0 else hexc("#33333d"))
        ctx.fill()
        if glow > 0 and icons and _slot(icons, newest)[0] == r:
            pulse = 0.5 + 0.5 * math.sin(t * 9)
            ctx.rectangle(x0 + LAB, y, W - LAB, ROW)
            c = hexc(COL[tier])
            ctx.set_source_rgba(c[0], c[1], c[2], 0.32 * glow * (0.6 + 0.4 * pulse))
            ctx.fill()
        ctx.rectangle(x0, y, LAB, ROW)   # label
        src(ctx, hexc(COL[tier]))
        ctx.fill()
        surf, _, px = _letter(tier)
        ctx.set_source_surface(surf, x0 + LAB / 2 - px, y + ROW / 2 - px + 4)
        ctx.paint()
        ctx.restore()
    ctx.save()   # grid lines
    for r in range(1, 6):
        ctx.move_to(x0, r * ROW)
        ctx.line_to(x0 + W, r * ROW)
    ctx.move_to(x0 + LAB, 0)
    ctx.line_to(x0 + LAB, ROW * 6)
    ink(ctx, OUT * 0.7)
    ctx.restore()
    for i, ic in enumerate(icons):
        r, n = _slot(icons, i)
        cx = x0 + LAB + 75 + n * 150
        cy = r * ROW + ROW / 2
        a = 1.0
        if i == newest and drop < 1.0:
            u = back_out(min(1.0, drop * 1.05)) if drop > 0 else 0.0
            cy = -260 + (cy + 260) * u
            a = min(1.0, drop * 4)
        rec, k, ox, oy = _icon(ic)
        ctx.save()
        ctx.rectangle(x0 + LAB, -400, W - LAB, ROW * 6 + 400)
        ctx.clip()
        bob = 3 * math.sin(t * 3 + i)
        ctx.translate(cx, cy + bob)
        sq = 1.0
        if i == newest and 0.85 < drop < 1.0:   # landing squash
            sq = 1 - 0.25 * math.sin((drop - 0.85) / 0.15 * math.pi)
        ctx.scale(k * (2 - sq), k * sq)
        ctx.translate(-ox, -oy)
        ctx.set_source_surface(rec, 0, 0)
        ctx.paint_with_alpha(a)
        ctx.restore()
    if hide and unveil < 1.0:   # the S cover: a dark panel with a big "?" that slides off to the right
        off = ease(unveil) * (W - LAB + 40)
        ctx.save()
        ctx.rectangle(x0 + LAB, 0, W - LAB, ROW)
        ctx.clip()
        ctx.translate(off, 0)
        ctx.rectangle(x0 + LAB, 0, W - LAB, ROW)
        src(ctx, hexc("#141418"))
        ctx.fill()
        for j in range(5):   # "blurred" silhouettes behind the cover
            ctx.set_source_rgba(0.6, 0.1, 0.1, 0.22 + 0.06 * math.sin(t * 2 + j))
            ctx.arc(x0 + LAB + 90 + j * 150, ROW / 2, 46, 0, 2 * math.pi)
            ctx.fill()
        surf, _, px = _letter("?")
        wob = 6 * math.sin(t * 4)
        ctx.set_source_surface(surf, x0 + LAB + (W - LAB) / 2 - px, ROW / 2 - px + 4 + wob)
        ctx.paint()
        ctx.restore()


ACTORS = {"tierboard": board}
