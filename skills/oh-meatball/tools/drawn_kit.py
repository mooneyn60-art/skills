"""Drawing kit for the fully drawn Meatball look (tools/drawn.py). Cairo vector primitives in ONE locked style:

  * thick black ink outlines (INK, the same near-black as Meatball in mascot.py), round joins and caps
  * flat colours from the PAL palette, plus ONE cel-shade per shape (a darker crescent, bottom-right) and an
    optional highlight blob (top-left); no gradients on characters, banded flat colour on skies and water
  * line weights: OUT for characters and props, BG_OUT for scenery (lighter, so characters read first)
  * cartoon faces: big white eyes with ink pupils and a highlight, simple brows, a mouth that can talk

Everything is drawn procedurally (no image generation), so every asset is on-model on every frame and the
look can't drift. Coordinates are plain cairo user space; callers translate/scale before drawing.
"""
import math
import random

import cairo

INK = (17 / 255, 17 / 255, 17 / 255)
OUT, BG_OUT = 9.0, 6.0


def hexc(h, a=None):
    h = h.lstrip("#")
    c = tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return c if a is None else c + (a,)


PAL = {k: hexc(v) for k, v in {
    # basement
    "wall": "#c9b89a", "wall_dk": "#ad9b7c", "mortar": "#a08d6e", "floor": "#8a6f55", "floor_dk": "#735a43",
    "wood": "#b07a45", "wood_dk": "#8a5a30", "box": "#d8a960", "box_dk": "#b8873f", "pipe": "#8d969c",
    "bulb": "#fff2a8", "glow": "#fff6c8", "window": "#9fd3ee", "web": "#f4f4f4",
    # animals
    "harv": "#b0743e", "harv_dk": "#8a5428", "harv_lt": "#d8a06a", "cell": "#d9c7a0", "cell_dk": "#b39d70",
    "cell_mark": "#8f7a55", "skin": "#f1c7a0", "skin_dk": "#d9a57b", "burn": "#e8463a",
    # ocean + deep
    "sky": "#8fd3f4", "sky2": "#bfe6f8", "sun": "#ffd84a", "cloud": "#ffffff", "cloud_dk": "#dbe9f2",
    "sea": "#2f7fc0", "sea2": "#2a6fab", "sea_dk": "#235d92", "foam": "#e8f6ff",
    "deep1": "#1d4f86", "deep2": "#173f6e", "deep3": "#123259", "deep4": "#0d2545", "deep5": "#0a1b33",
    "sand": "#5d6b7a", "sand_dk": "#4a5664", "rock": "#3f4955",
    # ships, subs, machines
    "hull": "#3d4a57", "hull_dk": "#2b3540", "hull_red": "#b8352c", "deck": "#c8ccd0", "deck_dk": "#a3a8ad",
    "derrick": "#e0e3e6", "steel": "#9aa3ab", "steel_dk": "#737c85", "claw": "#f0b429", "claw_dk": "#c98d12",
    "sub": "#4b5560", "sub_dk": "#353d46", "red": "#d8322a", "us_sub": "#6b7a87", "light": "#fff6b0",
    # people
    "suit": "#2e3440", "suit_dk": "#20252e", "shirt": "#f4f4f4", "tie": "#e2b13c", "hair": "#3a2a1e",
    "skin2": "#e8b48a", "skin2_dk": "#c99068", "skin3": "#a8754e", "skin3_dk": "#8a5c3a",
    "mask": "#202020", "stripe": "#f4f4f4", "sack": "#a88a5c", "paper": "#fbf6e6", "paper_dk": "#e2dac0",
    "folder": "#e8c46a", "string": "#d22a22",
    # rooms
    "office": "#4b5a73", "office_dk": "#3c4a60", "night": "#1b2440", "night2": "#26315a", "palm": "#16233f",
    "cabinet": "#8f99a6", "cabinet_dk": "#717b88", "desk": "#7a5233", "desk_dk": "#5e3d23",
    "curtain": "#2c4f8f", "curtain_dk": "#22407a", "podium": "#6b4a2f", "podium_dk": "#523720",
    "seal": "#d9b44a", "carpet": "#7a2f2f", "flash": "#ffffff",
}.items()}


def src(ctx, c, a=1.0):
    if len(c) == 4:
        ctx.set_source_rgba(*c)
    else:
        ctx.set_source_rgba(c[0], c[1], c[2], a)


def ink(ctx, lw=OUT, a=1.0):
    ctx.set_source_rgba(*INK, a)
    ctx.set_line_width(lw)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)


def darker(c, k=0.78):
    return tuple(x * k for x in c[:3])


def lighter(c, k=0.45):
    return tuple(x + (1 - x) * k for x in c[:3])


# ---------------------------------------------------------------- paths

def p_ellipse(ctx, cx, cy, rx, ry, rot=0.0):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(rot)
    ctx.scale(max(rx, 0.01), max(ry, 0.01))
    ctx.new_sub_path()
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()


def p_rrect(ctx, x, y, w, h, r):
    r = max(0.0, min(r, w / 2, h / 2))
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()


def p_poly(ctx, pts, close=True):
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    if close:
        ctx.close_path()


def p_smooth(ctx, pts, close=True):
    """Closed (or open) Catmull-Rom curve through the points."""
    n = len(pts)
    P = (lambda i: pts[i % n]) if close else (lambda i: pts[min(max(i, 0), n - 1)])
    ctx.move_to(*pts[0])
    for i in range(n if close else n - 1):
        p0, p1, p2, p3 = P(i - 1), P(i), P(i + 1), P(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        ctx.curve_to(*c1, *c2, *p2)
    if close:
        ctx.close_path()


def p_blob(ctx, cx, cy, rx, ry, wob=0.06, seed=0, n=14):
    rng = random.Random(seed)
    ph = [rng.uniform(0, 6.28) for _ in range(3)]
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        r = 1 + wob * (math.sin(3 * a + ph[0]) + 0.6 * math.sin(5 * a + ph[1]) + 0.3 * math.sin(2 * a + ph[2]))
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    p_smooth(ctx, pts)


# ---------------------------------------------------------------- the house shape: fill + cel shade + ink

def shape(ctx, path, fill, lw=OUT, shade=(0.12, 0.12), hi=None, shade_k=0.8, a=1.0):
    """Draw path (a callable that builds the path) as flat fill + one cel-shade crescent + ink outline.
    shade = offset of the lit area as a fraction of the shape size (None = flat); hi = highlight blob."""
    ctx.save()
    path(ctx)
    x0, y0, x1, y1 = ctx.fill_extents()
    w, h = x1 - x0, y1 - y0
    if shade:
        src(ctx, darker(fill, shade_k), a)
        ctx.fill_preserve()
        ctx.clip()
        ctx.new_path()
        ctx.translate(-shade[0] * w, -shade[1] * h)
        path(ctx)
        src(ctx, fill, a)
        ctx.fill()
        ctx.restore()
        ctx.save()
        if hi:
            path(ctx)
            ctx.clip()
            ctx.new_path()
            p_ellipse(ctx, x0 + w * hi[0], y0 + h * hi[1], w * hi[2], h * hi[2] * 0.7, -0.5)
            src(ctx, lighter(fill, 0.35), a)
            ctx.fill()
            ctx.reset_clip()
        path(ctx)
    else:
        src(ctx, fill, a)
        ctx.fill_preserve()
    if lw:
        ink(ctx, lw, a)
        ctx.stroke()
    else:
        ctx.new_path()
    ctx.restore()


def flat(ctx, path, fill, lw=0.0, a=1.0):
    shape(ctx, path, fill, lw, None, a=a)


def stroke(ctx, pts, lw=OUT, smooth=False, color=None, a=1.0):
    ctx.save()
    (p_smooth if smooth else p_poly)(ctx, pts, close=False)
    if color:
        src(ctx, color, a)
        ctx.set_line_width(lw)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    else:
        ink(ctx, lw, a)
    ctx.stroke()
    ctx.restore()


def limb(ctx, pts, w, color, lw=OUT * 0.8, smooth=True):
    """A stroked limb: ink underlay then colour core, so thin legs get a clean outline."""
    stroke(ctx, pts, w + 2 * lw, smooth)
    if w > 0.5:
        stroke(ctx, pts, w, smooth, color)


# ---------------------------------------------------------------- faces (animals, people, props)

def eyes(ctx, cx, cy, r, gap, look=(0.0, 0.0), mood="calm", blink=0.0, lw=OUT * 0.75, pupil=0.45, lid=None):
    """A pair of cartoon eyes. mood: calm, happy, shock, worry, angry, smug, sleepy. blink 0..1."""
    for s in (-1, 1):
        ex = cx + s * gap
        ry = r * (1.25 if mood == "shock" else 1.1)
        shape(ctx, lambda c: p_ellipse(c, ex, cy, r, ry), (1, 1, 1), lw, None)
        pr = r * (pupil * (0.7 if mood == "shock" else 1.0))
        px, py = ex + look[0] * r * 0.45, cy + look[1] * r * 0.45
        ctx.save()
        p_ellipse(ctx, ex, cy, r, ry)
        ctx.clip()
        p_ellipse(ctx, px, py, pr, pr * 1.1)
        src(ctx, INK)
        ctx.fill()
        p_ellipse(ctx, px - pr * 0.35, py - pr * 0.4, pr * 0.32, pr * 0.32)
        src(ctx, (1, 1, 1))
        ctx.fill()
        cover = max({"sleepy": 0.5, "smug": 0.42, "angry": 0.3}.get(mood, 0.0), blink)
        if cover > 0:
            ctx.rectangle(ex - r * 1.2, cy - ry * 1.2, r * 2.4, ry * 2.4 * cover)
            src(ctx, lid or (0.92, 0.86, 0.78))
            ctx.fill()
            yl = cy - ry * 1.2 + ry * 2.4 * cover
            stroke(ctx, [(ex - r, yl), (ex + r, yl)], lw)
        ctx.restore()
        ink(ctx, lw)
        p_ellipse(ctx, ex, cy, r, ry)
        ctx.stroke()
        # brows
        by = cy - ry - r * 0.45
        if mood in ("worry", "shock"):
            stroke(ctx, [(ex - r * 0.8 * s, by + r * 0.25 * (1 if mood == "worry" else -0.2)),
                         (ex + r * 0.7 * s, by - r * 0.3)], lw * 1.1)
        elif mood == "angry":
            stroke(ctx, [(ex - r * 0.8 * s, by - r * 0.3), (ex + r * 0.8 * s, by + r * 0.35)], lw * 1.2)
        elif mood in ("smug", "calm", "happy"):
            stroke(ctx, [(ex - r * 0.7, by), (ex, by - r * 0.18), (ex + r * 0.7, by)], lw, smooth=True)


def mouth(ctx, cx, cy, w, kind="smile", open_=0.0, lw=OUT * 0.75, teeth=False):
    """kind: smile, grin, flat, o, frown, wobble; open_ 0..1 flaps it open while talking."""
    if open_ > 0.05 or kind == "o":
        h = w * (0.35 + 0.45 * open_) if kind != "o" else w * 0.6
        ww = w * (0.8 if kind == "o" else 1.0)
        shape(ctx, lambda c: p_ellipse(c, cx, cy + h * 0.3, ww / 2, h / 2), (0.45, 0.08, 0.08), lw, None)
        if teeth:
            ctx.save()
            p_ellipse(ctx, cx, cy + h * 0.3, ww / 2, h / 2)
            ctx.clip()
            ctx.rectangle(cx - ww / 2, cy + h * 0.3 - h / 2, ww, h * 0.25)
            src(ctx, (1, 1, 1))
            ctx.fill()
            ctx.restore()
        return
    if kind in ("smile", "grin"):
        d = w * (0.28 if kind == "smile" else 0.4)
        stroke(ctx, [(cx - w / 2, cy - d * 0.3), (cx, cy + d), (cx + w / 2, cy - d * 0.3)], lw, smooth=True)
    elif kind == "frown":
        stroke(ctx, [(cx - w / 2, cy + w * 0.2), (cx, cy - w * 0.12), (cx + w / 2, cy + w * 0.2)], lw, smooth=True)
    elif kind == "wobble":
        stroke(ctx, [(cx - w / 2 + w * i / 6, cy + (w * 0.07 if i % 2 else -w * 0.07)) for i in range(7)], lw)
    else:
        stroke(ctx, [(cx - w / 2, cy), (cx + w / 2, cy)], lw)


def sweat(ctx, x, y, s, lw=OUT * 0.7):
    def drop(c):
        c.move_to(x, y - s)
        c.curve_to(x + s * 0.6, y - s * 0.1, x + s * 0.6, y + s * 0.6, x, y + s * 0.6)
        c.curve_to(x - s * 0.6, y + s * 0.6, x - s * 0.6, y - s * 0.1, x, y - s)
        c.close_path()
    shape(ctx, drop, hexc("#78bef0"), lw, None)


def motion_lines(ctx, x, y, n, length, ang, lw=OUT * 0.6, a=0.8):
    for i in range(n):
        o = (i - (n - 1) / 2) * lw * 3.2
        dx, dy = math.cos(ang), math.sin(ang)
        stroke(ctx, [(x - dy * o, y + dx * o), (x - dy * o + dx * length, y + dx * o + dy * length)], lw, a=a)


def starburst(ctx, cx, cy, r, n=10, fill=(1, 0.86, 0.2), lw=OUT * 0.8, rot=0.0):
    pts = []
    for i in range(2 * n):
        rr = r if i % 2 == 0 else r * 0.55
        a = rot + math.pi * i / n
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    shape(ctx, lambda c: p_poly(c, pts), fill, lw, None)


def ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def ease_out(u):
    u = min(max(u, 0.0), 1.0)
    return 1 - (1 - u) ** 3


def back_out(u, s=1.7):
    u = min(max(u, 0.0), 1.0) - 1
    return u * u * ((s + 1) * u + s) + 1


def lerp(a, b, u):
    return a + (b - a) * u
