"""Pictures for the house-cat long-form ("Why It Sucks to Be Born as a House Cat", tools/drawn_catlife.py).
Same locked drawn look (drawn_kit shapes, ink outlines, flat fills), 1920x1080 world: a room's floor is y = 900,
boards on ds_board_bg are centred on (0, 0).

The cat is the kit's side-view mammal (drawn_creatures.mammal) with the channel cat Short's config (orange, pointed
ears, thin tail, whiskers); cl_cat adds the ages (kitten / adult / senior / wild), shut eyes, sitting, a cone, a cast,
a party hat, radar arcs and tabby stripes on top of it. Only labels the outline's `vis` names are drawn as text.

Scenes: cl_blanket, cl_room (living / kitchen / bath / clinic / hall / door), cl_village, cl_street, cl_shelter.
Actors: see ACTORS at the bottom."""
import math
import random

import cairo

from drawn_creatures import mammal
from drawn_ds_art import text
from drawn_kit import (BG_OUT, INK, OUT, PAL, back_out, darker, ease, eyes, flat, hexc, ink, lighter, limb, mouth,
                       p_blob, p_ellipse, p_poly, p_rrect, p_smooth, shape, src, stroke)

C = {k: hexc(v) for k, v in {
    "wall": "#e9d6b4", "wall2": "#e0c9a2", "wain": "#f3ead8", "floor": "#b9804e", "floor2": "#a46e40",
    "sky": "#9fd4f0", "sand": "#e3c38a", "sand2": "#d4ae70", "mud": "#c79a62", "mud2": "#b0844f", "dusk": "#3b3560",
    "parch": "#f1e2b8", "parch2": "#d9c18a", "red": "#e5383b", "green": "#3fb950", "yel": "#ffd34d", "blue": "#3b7dd8",
    "milk": "#fbfaf4", "steel": "#b7c0c9", "night": "#1b2240", "teal": "#2f8f8a", "lily": "#fbf7ee", "pollen": "#f0a020",
    "xray": "#13293d", "xline": "#bfe6ff", "board": "#1b1724", "paper": "#fbf8ef", "pink": "#f2a7a7",
}.items()}

# the channel cat Short's cat (outline: "the same cat as the channel's cat Short")
CAT = {"plan": "mammal", "label": "cat", "color": "#e39a4a", "dark": "#b06f2a", "belly": "#f6e3c8",
       "tail_color": "#e39a4a", "length": 520, "height": 250, "leg_len": 150, "leg_w": 30, "ears": "pointed",
       "tail": "thin", "tail_w": 22, "whiskers": True}
KITTEN = dict(CAT, length=330, height=215, leg_len=78, leg_w=24, tail_w=15)
WILD = dict(CAT, color="#cdb27c", dark="#8f7647", belly="#f0e4c6", tail_color="#cdb27c")
DOG = {"plan": "mammal", "label": "dog", "color": "#c98a4a", "dark": "#8f5e2e", "belly": "#efd6b0", "length": 560,
       "height": 270, "leg_len": 170, "leg_w": 38, "ears": "floppy", "tail": "thin", "tail_w": 20, "whiskers": False}


# ================================================================================================ the cat

def _cat_cfg(p):
    age = p.get("age", "adult")
    cfg = dict(KITTEN if age == "kitten" else (WILD if age == "wild" else CAT))
    if p.get("ears_flat"):
        cfg["ears"] = "tiny"
    sit = max(0.0, min(1.0, p.get("sit", 0.0)))
    cfg["leg_len"] = cfg["leg_len"] * (1 - 0.82 * sit)
    return cfg


def cl_cat(ctx, t, p):
    """The cat, side view, facing right, origin = feet. p: age (kitten | adult | senior | wild), shut (eyes shut),
    sit (0..1 legs tucked: sitting or lying), wiggle (newborn squirm), ears_flat, stripes (tabby bands; on for wild),
    cone, cast, hat, radar (0..1 sound arcs at the ears), sil (0..1 dark silhouette), a (alpha), mood, look."""
    cfg = _cat_cfg(p)
    a = p.get("a", 1.0)
    if a <= 0.01:
        return
    q = dict(p)
    if p.get("shut"):
        q["blink"] = 1.0
        q["mood"] = p.get("mood", "calm")
    if p.get("age") == "senior" and not p.get("shut"):
        q["blink"] = max(q.get("blink", 0.0), 0.0)
        q.setdefault("mood", "sleepy")
    ctx.save()
    if p.get("wiggle"):
        ctx.rotate(p["wiggle"] * 0.06 * math.sin(t * 9))
    sil = p.get("sil", 0.0)
    if a < 0.999 or sil > 0:
        ctx.push_group()
    L, H, ll = cfg["length"], cfg["height"], cfg["leg_len"]
    mammal(ctx, t, cfg, q)
    by = -ll - H * 0.35 + 3 * math.sin(t * 2.5)
    hx, hy, hr = L * 0.48, by - H * 0.38, H * 0.48
    if p.get("stripes", p.get("age") == "wild"):
        ctx.save()
        p_ellipse(ctx, 0, by, L / 2, H / 2)
        ctx.clip()
        dk = darker(hexc(cfg["color"]), 0.62)
        for k in range(6):
            x = -L * 0.36 + k * L * 0.105
            stroke(ctx, [(x - 8, by - H * 0.52), (x + 10, by - H * 0.1), (x - 4, by + H * 0.12)], 13, smooth=True, color=dk)
        ctx.restore()
        for k in range(3):   # forehead lines
            stroke(ctx, [(hx - hr * 0.05 + k * hr * 0.18, hy - hr * 0.85), (hx + k * hr * 0.15, hy - hr * 0.55)], 6,
                   color=darker(hexc(cfg["color"]), 0.62))
    if p.get("age") == "senior":   # a pale grey muzzle and brow
        flat(ctx, lambda c: p_ellipse(c, hx + hr * 0.85, hy + hr * 0.25, hr * 0.47, hr * 0.34), hexc("#d9d6d0"), a=0.85)
        flat(ctx, lambda c: p_ellipse(c, hx + hr * 0.15, hy - hr * 0.55, hr * 0.42, hr * 0.12), hexc("#d9d6d0"), a=0.55)
        flat(ctx, lambda c: p_ellipse(c, hx + hr * 1.25, hy + hr * 0.15, hr * 0.13, hr * 0.11), INK)
        for k in (-1, 0, 1):
            stroke(ctx, [(hx + hr * 1.05, hy + hr * 0.3), (hx + hr * 1.8, hy + hr * (0.3 + 0.2 * k))], 3)
    if p.get("cast"):   # a small white cast on the near front leg
        x = L * 0.3
        shape(ctx, lambda c: p_rrect(c, x - 26, by + H * 0.25, 52, -by - H * 0.25 + 6, 18), (0.97, 0.97, 0.95), OUT * 0.8,
              (0.05, 0.1))
        for k in range(3):
            y = by + H * 0.35 + k * (-by - H * 0.3) / 3
            stroke(ctx, [(x - 22, y), (x + 22, y + 8)], 3, color=hexc("#c9c9c0"))
    if p.get("cone"):   # the cone of shame: a translucent funnel around the neck, opening forward
        nx = hx - hr * 0.45
        pts = [(nx, hy - hr * 0.75), (nx + hr * 1.7, hy - hr * 1.75), (nx + hr * 1.7, hy + hr * 1.6), (nx, hy + hr * 0.75)]
        shape(ctx, lambda c: p_poly(c, pts), (0.85, 0.93, 1.0), OUT * 0.8, None, a=0.55)
        stroke(ctx, [pts[1], pts[2]], 8, color=(0.7, 0.82, 0.95))
    if p.get("hat"):   # a party hat, tipped forward
        ctx.save()
        ctx.translate(hx - hr * 0.1, hy - hr * 0.8)
        ctx.rotate(0.25)
        shape(ctx, lambda c: p_poly(c, [(-hr * 0.45, 0), (0, -hr * 1.5), (hr * 0.45, 0)]), C["blue"], OUT * 0.8, (0.1, 0))
        for k in range(3):
            flat(ctx, lambda c, k=k: p_ellipse(c, -hr * 0.2 + k * hr * 0.2, -hr * (0.3 + 0.35 * (k % 2)), 9, 9), C["yel"])
        flat(ctx, lambda c: p_ellipse(c, 0, -hr * 1.55, 16, 16), C["red"])
        ctx.restore()
    rad = p.get("radar", 0.0)
    if rad > 0.01:   # each ear on its own: sound arcs, out of step
        for k, ex in enumerate((hx - hr * 0.5, hx + hr * 0.05)):
            ph = (t * 1.6 + k * 0.5) % 1
            for j in range(2):
                u = (ph + j * 0.5) % 1
                ctx.new_sub_path()
                ang = -1.9 + (0.5 if k else -0.4) * math.sin(t * 2.3 + k * 2)
                ctx.arc(ex, hy - hr * 1.1, 40 + 90 * u, ang - 0.5, ang + 0.5)
                ctx.set_source_rgba(1, 1, 1, rad * (1 - u))
                ctx.set_line_width(7)
                ctx.stroke()
    if a < 0.999 or sil > 0:
        pat = ctx.pop_group()
        if sil > 0:
            ctx.push_group()
            ctx.set_source(pat)
            ctx.paint()
            ctx.set_operator(cairo.OPERATOR_ATOP)
            ctx.set_source_rgba(0.08, 0.08, 0.12, sil)
            ctx.paint()
            pat = ctx.pop_group()
        ctx.set_source(pat)
        ctx.paint_with_alpha(a)
    ctx.restore()


cl_cat.cfg = CAT


def cl_dog(ctx, t, p):
    """The kit's dog (mammal, floppy ears), facing right; p: queasy (0..1: a green tinge and a wobbly mouth)."""
    q = dict(p)
    qz = p.get("queasy", 0.0)
    if qz > 0.3:
        q["mood"] = "worry"
        q["mouth"] = "wobble"
    mammal(ctx, t, DOG, q)
    if qz > 0.01:
        L, H, ll = DOG["length"], DOG["height"], DOG["leg_len"]
        by = -ll - H * 0.35 + 3 * math.sin(t * 2.5)
        hx, hy, hr = L * 0.48, by - H * 0.38, H * 0.48
        flat(ctx, lambda c: p_ellipse(c, hx + hr * 0.4, hy + hr * 0.15, hr * 0.5, hr * 0.3), hexc("#9fd36a"), a=0.45 * qz)
        for k in range(3):   # a little wobble line over the belly (tummy ache)
            x0 = -L * 0.1 + k * 40
            stroke(ctx, [(x0, by + 10), (x0 + 12, by + 22), (x0 + 24, by + 10)], 5, color=hexc("#6b8f3a"), a=qz)


cl_dog.cfg = DOG


def cl_mouse(ctx, t, p):
    """A small grey mouse, side view facing right; p: freeze (0..1 ears up, still), label (0..1 a nutrition tag)."""
    col = hexc("#9a8f88")
    by = -60 - (0 if p.get("freeze") else 4 * abs(math.sin(t * 9)) * (1 if p.get("walking") else 0))
    stroke(ctx, [(-90, by + 20), (-170, by + 10), (-220, by - 20)], 7, smooth=True, color=hexc("#c99a95"))
    for x in (-50, 40):
        limb(ctx, [(x, by + 20), (x, 0)], 12, darker(col, 0.8), OUT * 0.5)
    shape(ctx, lambda c: p_ellipse(c, 0, by, 100, 58), col, OUT, (0.05, 0.15))
    shape(ctx, lambda c: p_ellipse(c, 95, by - 18, 58, 44), col, OUT, (0.05, 0.15))
    for ex, ey in ((70, by - 66), (108, by - 62)):
        shape(ctx, lambda c, ex=ex, ey=ey: p_ellipse(c, ex, ey, 26 + 6 * p.get("freeze", 0), 28 + 6 * p.get("freeze", 0)),
              lighter(col, 0.3), OUT * 0.7, None)
        flat(ctx, lambda c, ex=ex, ey=ey: p_ellipse(c, ex, ey, 14, 16), C["pink"])
    eyes(ctx, 112, by - 26, 10, 10, (1, 0), "shock" if p.get("freeze", 0) > 0.5 else "calm", 0, OUT * 0.5)
    flat(ctx, lambda c: p_ellipse(c, 152, by - 12, 8, 7), INK)
    for k in (-1, 1):
        stroke(ctx, [(140, by - 8), (190, by - 8 + 14 * k)], 2.5)
    lab = p.get("label", 0.0)
    if lab > 0.01:   # the nutrition label the vis names
        ctx.save()
        ctx.translate(-20, by - 150)
        s = back_out(min(1.0, lab))
        ctx.scale(s, s)
        stroke(ctx, [(0, 60), (10, 110)], 3)
        shape(ctx, lambda c: p_rrect(c, -170, -50, 340, 112, 10), C["paper"], OUT * 0.7, None)
        text(ctx, "CARBS:", 0, -18, 40, "#222222", 0)
        text(ctx, "ALMOST NONE", 0, 30, 40, "#c0392b", 0)
        ctx.restore()


# ================================================================================================ scenes

def cl_blanket(ctx, t, layer, p):
    """A soft knitted blanket filling the frame (the newborn's close-up); p: col."""
    layer(1.0)
    col = hexc(p.get("col", "#8fb3d9"))
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), col)
    for k in range(-20, 40):   # soft folds
        y = k * 90
        pts = [(x, y + 26 * math.sin(x / 210 + k * 0.7)) for x in range(-2000, 4000, 120)]
        stroke(ctx, pts, 30, smooth=True, color=darker(col, 0.9), a=0.55)
        stroke(ctx, [(x, y2 + 18) for x, y2 in pts], 10, smooth=True, color=lighter(col, 0.25), a=0.5)
    for x in range(-2000, 4000, 70):   # knit stitches
        for y in range(-2000, 3000, 70):
            if (x // 70 + y // 70) % 2 == 0:
                stroke(ctx, [(x, y), (x + 14, y + 16), (x + 28, y)], 4, color=darker(col, 0.86), a=0.35)


def _floor(ctx, y0=900):
    flat(ctx, lambda c: c.rectangle(-3000, y0, 8000, 3000), C["floor"])
    for k in range(-30, 60):
        stroke(ctx, [(k * 160, y0), (k * 160 - 80, y0 + 900)], 3, color=C["floor2"], a=0.7)
    stroke(ctx, [(-3000, y0), (5000, y0)], BG_OUT)


def _window(ctx, x, y, w, h, t, sky="#9fd4f0", open_=0.0, curtain=0.0, barrier=0.0):
    shape(ctx, lambda c: c.rectangle(x - 26, y - 26, w + 52, h + 52), hexc("#f6f0e2"), BG_OUT, None)
    flat(ctx, lambda c: c.rectangle(x, y, w, h), hexc(sky))
    flat(ctx, lambda c: p_ellipse(c, x + w * 0.3, y + h * 0.35, w * 0.25, h * 0.08), (1, 1, 1), a=0.8)
    flat(ctx, lambda c: c.rectangle(x, y + h * 0.78, w, h * 0.22), hexc("#8fbf78"))
    if open_ > 0.01:   # the lower sash slides up: an open gap
        g = h * 0.45 * open_
        shape(ctx, lambda c: c.rectangle(x, y + h * 0.5 - g, w, h * 0.5), (0.85, 0.93, 1.0), BG_OUT * 0.8, None, a=0.6)
    else:
        stroke(ctx, [(x, y + h / 2), (x + w, y + h / 2)], BG_OUT * 2.4, color=hexc("#f6f0e2"))
    stroke(ctx, [(x + w / 2, y), (x + w / 2, y + h * (0.5 if open_ > 0.01 else 1.0))], BG_OUT * 2.4, color=hexc("#f6f0e2"))
    if barrier > 0.01:   # a window barrier: a mesh panel in the opening
        ctx.save()
        ctx.rectangle(x, y + h * 0.5 - h * 0.45 * open_, w, h * 0.45 * open_ * min(1.0, barrier))
        ctx.clip()
        for k in range(0, int(w), 26):
            stroke(ctx, [(x + k, y), (x + k, y + h)], 3, color=(0.3, 0.3, 0.3))
        for k in range(0, int(h), 26):
            stroke(ctx, [(x, y + k), (x + w, y + k)], 3, color=(0.3, 0.3, 0.3))
        ctx.restore()
        stroke(ctx, [(x, y + h * 0.5 - h * 0.45 * open_ + h * 0.45 * open_ * min(1.0, barrier)),
                     (x + w, y + h * 0.5 - h * 0.45 * open_ + h * 0.45 * open_ * min(1.0, barrier))], 10, color=(0.95, 0.95, 0.95))
    sw = curtain * 40 * math.sin(t * 2.2)
    for s in (-1, 1):
        cx = x - 40 if s < 0 else x + w + 40
        pts = [(cx - 50, y - 50), (cx + 50, y - 50), (cx + 50 + (sw if s > 0 else 0) * 0.3, y + h * 0.6),
               (cx + 60 + (sw if s > 0 else -sw), y + h + 60), (cx - 60 + (sw if s > 0 else -sw), y + h + 60)]
        shape(ctx, lambda c, pts=pts: p_smooth(c, pts), hexc("#c8574a"), BG_OUT, (0.1, 0.1))
    stroke(ctx, [(x - 120, y - 50), (x + w + 120, y - 50)], 12, color=hexc("#6b4a2f"))


def _sofa(ctx, x, y):
    col = hexc("#5d7fa8")
    shape(ctx, lambda c: p_rrect(c, x - 330, y - 330, 660, 210, 50), col, BG_OUT, (0.05, 0.15))
    shape(ctx, lambda c: p_rrect(c, x - 360, y - 170, 720, 150, 40), lighter(col, 0.12), BG_OUT, (0.05, 0.15))
    for s in (-1, 1):
        shape(ctx, lambda c, s=s: p_rrect(c, x + s * 330 - 60, y - 250, 120, 230, 50), darker(col, 0.92), BG_OUT, (0.05, 0.1))
    for s in (-1, 1):
        shape(ctx, lambda c, s=s: c.rectangle(x + s * 300 - 14, y - 22, 28, 22), hexc("#5a3d24"), BG_OUT * 0.8, None)


def cl_room(ctx, t, layer, p):
    """A room of the cat's house, floor at y = 900. p: kind (living | kitchen | bath | clinic | hall | door), time
    (day | dusk | night), dark (0..1 lights down), window_open, curtain, barrier, door_open (front door to a dusk
    street), cab_open (bathroom cabinet), wall (colour)."""
    layer(0.97)
    kind = p.get("kind", "living")
    wall = hexc(p.get("wall", {"bath": "#bfdce0", "clinic": "#d3e8dc", "kitchen": "#f2e3b8", "hall": "#d8c6a8"}
                     .get(kind, "#e9d6b4")))
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 4000), wall)
    if kind == "bath":
        for x in range(-1000, 3200, 90):
            for y in range(-600, 900, 90):
                shape(ctx, lambda c, x=x, y=y: c.rectangle(x, y, 90, 90), wall, 2.0, None)
    else:
        for x in range(-3000, 5000, 150):
            flat(ctx, lambda c, x=x: c.rectangle(x, -3000, 60, 3900), darker(wall, 0.96))
        shape(ctx, lambda c: c.rectangle(-3000, 660, 8000, 240), C["wain"], BG_OUT, None)
        for x in range(-3000, 5000, 260):
            stroke(ctx, [(x, 690), (x, 870)], 4, color=hexc("#ddd2bc"))
    sky = {"day": "#9fd4f0", "dusk": "#e79a6a", "night": "#1b2240"}.get(p.get("time", "day"), "#9fd4f0")
    if kind in ("living", "kitchen", "hall") and not p.get("nowin"):
        _window(ctx, p.get("wx", 180), 130, 420, 430, t, sky, p.get("window_open", 0.0), p.get("curtain", 0.0),
                p.get("barrier", 0.0))
    if kind == "living":
        _sofa(ctx, p.get("sofa_x", 1480), 900)
        shape(ctx, lambda c: p_ellipse(c, 960, 960, 520, 60), hexc("#a5514a"), BG_OUT, None, a=1.0)
        shape(ctx, lambda c: p_ellipse(c, 960, 960, 430, 42), hexc("#c46e5c"), 0, None)
        flat(ctx, lambda c: c.rectangle(1120, 210, 260, 190), hexc("#6b4a2f"))   # a picture frame
        flat(ctx, lambda c: c.rectangle(1140, 230, 220, 150), hexc("#a8c8a0"))
        flat(ctx, lambda c: p_ellipse(c, 1250, 330, 80, 40), hexc("#6f9e64"))
    elif kind == "kitchen":
        shape(ctx, lambda c: c.rectangle(860, 560, 1100, 340), hexc("#d9a066"), BG_OUT, (0.03, 0.1))
        shape(ctx, lambda c: c.rectangle(840, 540, 1140, 30), hexc("#f2f2ee"), BG_OUT, None)
        for x in range(900, 1900, 260):
            shape(ctx, lambda c, x=x: p_rrect(c, x, 600, 220, 250, 10), hexc("#e2b07a"), BG_OUT * 0.7, None)
        for x in range(900, 1900, 260):
            shape(ctx, lambda c, x=x: p_rrect(c, x, 80, 220, 260, 10), hexc("#d9a066"), BG_OUT, (0.03, 0.1))
    elif kind == "bath":
        shape(ctx, lambda c: p_rrect(c, 300, 560, 520, 340, 30), hexc("#f4f6f8"), BG_OUT, (0.05, 0.2))
        shape(ctx, lambda c: p_rrect(c, 820, 520, 380, 80, 30), hexc("#f4f6f8"), BG_OUT, (0.05, 0.2))
        shape(ctx, lambda c: c.rectangle(960, 600, 60, 300), hexc("#e8ecef"), BG_OUT, None)
        stroke(ctx, [(1010, 520), (1010, 470), (960, 470)], 14, color=C["steel"])
        cab_open = p.get("cab_open", 0.0)
        cx, cy, cw, ch = 860, 90, 320, 360
        if p.get("nocab"):
            cw = 0
        if cw: shape(ctx, lambda c: c.rectangle(cx, cy, cw, ch), hexc("#f2efe6"), BG_OUT, (0.03, 0.1))
        if cw and cab_open > 0.01:   # shelves inside (no pills shown)
            flat(ctx, lambda c: c.rectangle(cx + 14, cy + 14, cw - 28, ch - 28), hexc("#e0dccf"))
            for k in range(1, 3):
                stroke(ctx, [(cx + 14, cy + k * ch / 3), (cx + cw - 14, cy + k * ch / 3)], 8, color=hexc("#c8bfa8"))
            for k in range(3):
                shape(ctx, lambda c, k=k: p_rrect(c, cx + 40 + k * 90, cy + ch / 3 - 90, 60, 86, 10),
                      [hexc("#9fc3e8"), hexc("#f2c14e"), hexc("#e8a0a0")][k], OUT * 0.6, None)
        dw = cw * (1 - 0.85 * ease(min(1.0, cab_open)))
        if cw:
            shape(ctx, lambda c: c.rectangle(cx, cy, dw, ch), hexc("#cfe3ea"), BG_OUT, (0.05, 0.1))
            flat(ctx, lambda c: c.rectangle(cx + dw * 0.1, cy + 30, dw * 0.8, ch - 60), (1, 1, 1), a=0.35)
    elif kind == "clinic":
        shape(ctx, lambda c: p_rrect(c, 1100, 620, 640, 60, 12), C["steel"], BG_OUT, (0.03, 0.2))
        for x in (1160, 1680):
            stroke(ctx, [(x, 680), (x, 900)], 22, color=darker(C["steel"], 0.8))
        shape(ctx, lambda c: c.rectangle(200, 160, 380, 260), hexc("#ffffff"), BG_OUT, None)
        for k in range(4):
            stroke(ctx, [(230, 200 + k * 50), (540, 200 + k * 50)], 6, color=hexc("#9fb8c8"))
    elif kind in ("hall", "door"):
        dx, do = p.get("door_x", 1300), p.get("door_open", 0.0)
        shape(ctx, lambda c: c.rectangle(dx - 230, 180, 460, 720), hexc("#f6f0e2"), BG_OUT, None)
        ctx.save()
        ctx.rectangle(dx - 200, 210, 400, 690)
        ctx.clip()
        g = cairo.LinearGradient(0, 210, 0, 900)
        for u, c_ in ((0, "#2b2a5a"), (0.55, "#c86a5a"), (1.0, "#f0a860")):
            r, gg, b = hexc(c_)
            g.add_color_stop_rgb(u, r, gg, b)
        ctx.set_source(g)
        ctx.paint()
        for k in range(4):   # the houses across the street
            flat(ctx, lambda c, k=k: c.rectangle(dx - 260 + k * 150, 560 - (k % 2) * 60, 120, 400), hexc("#2a2740"))
            flat(ctx, lambda c, k=k: c.rectangle(dx - 230 + k * 150, 620 - (k % 2) * 60, 30, 30), hexc("#f6d36a"))
        flat(ctx, lambda c: c.rectangle(dx - 200, 820, 400, 80), hexc("#4a4a58"))
        ctx.restore()
        w = 400 * (1 - 0.88 * ease(min(1.0, do)))
        shape(ctx, lambda c: c.rectangle(dx - 200, 210, w, 690), hexc("#8a5a3a"), BG_OUT, (0.04, 0.1))
        for k in range(2):
            shape(ctx, lambda c, k=k: p_rrect(c, dx - 200 + w * 0.15, 260 + k * 320, w * 0.7, 260, 12), hexc("#9a6a48"),
                  BG_OUT * 0.6, None)
        flat(ctx, lambda c: p_ellipse(c, dx - 200 + w * 0.88, 560, 14, 14), C["yel"])
        if p.get("screen"):   # a screen door: mesh over the opening
            for k in range(0, 400, 22):
                stroke(ctx, [(dx - 200 + k, 210), (dx - 200 + k, 900)], 2, color=(0.2, 0.2, 0.2), a=0.6)
            for k in range(0, 690, 22):
                stroke(ctx, [(dx - 200, 210 + k), (dx + 200, 210 + k)], 2, color=(0.2, 0.2, 0.2), a=0.6)
    _floor(ctx, 900)
    tm = p.get("time", "day")
    grade = {"dusk": (0.95, 0.45, 0.25, 0.14), "night": (0.05, 0.08, 0.22, 0.32)}.get(tm)
    ctx.identity_matrix()
    if grade:
        ctx.rectangle(0, 0, 1920, 1080)
        ctx.set_source_rgba(*grade)
        ctx.fill()
    dk = p.get("dark", 0.0)
    if dk > 0.01:
        ctx.rectangle(0, 0, 1920, 1080)
        ctx.set_source_rgba(0.02, 0.03, 0.08, 0.72 * dk)
        ctx.fill()


def cl_village(ctx, t, layer, p):
    """A mud-brick farming village (the Near East, long ago): pale sky, flat-roofed houses with dark doorways, sand
    from y = 900. The middle house's doorway is at x 880..1080 (sill y = 900)."""
    layer(0.6)
    g = cairo.LinearGradient(0, -400, 0, 900)
    for u, c_ in ((0, "#9fd0ea"), (1.0, "#f3dcae")):
        r, gg, b = hexc(c_)
        g.add_color_stop_rgb(u, r, gg, b)
    ctx.rectangle(-4000, -4000, 12000, 9000)
    ctx.set_source(g)
    ctx.fill()
    flat(ctx, lambda c: p_ellipse(c, 1500, 120, 70, 70), hexc("#fff2b0"))
    for k in range(-4, 8):   # far hills
        flat(ctx, lambda c, k=k: p_ellipse(c, k * 520, 760, 420, 150), hexc("#d9bd88"))
    layer(0.97)
    for (x, w, h, col) in ((-420, 520, 420, C["mud2"]), (220, 560, 520, C["mud"]), (760, 440, 600, C["mud"]),
                           (1260, 600, 470, C["mud2"]), (1900, 520, 400, C["mud"])):
        shape(ctx, lambda c, x=x, w=w, h=h: c.rectangle(x, 900 - h, w, h), col, BG_OUT, (0.04, 0.12))
        shape(ctx, lambda c, x=x, w=w, h=h: c.rectangle(x - 16, 900 - h - 26, w + 32, 30), darker(col, 0.85), BG_OUT, None)
        for k in range(int(h // 70)):   # brick courses
            yy = 900 - h + 40 + k * 70
            stroke(ctx, [(x + 10, yy), (x + w - 10, yy)], 3, color=darker(col, 0.88), a=0.6)
        for bx in range(x + 20, x + w - 60, 140):   # roof beams sticking out
            shape(ctx, lambda c, bx=bx, x=x, h=h: c.rectangle(bx, 900 - h - 8, 40, 22), hexc("#7a5a3a"), OUT * 0.5, None)
    # doorways
    for (x, w, h) in ((880, 200, 330), (350, 150, 250), (1420, 170, 270)):
        shape(ctx, lambda c, x=x, w=w, h=h: p_poly(c, [(x, 900), (x, 900 - h + w / 2), (x + w / 2, 900 - h),
                                                      (x + w, 900 - h + w / 2), (x + w, 900)]), hexc("#3a2a1e"), BG_OUT, None)
    flat(ctx, lambda c: c.rectangle(-4000, 900, 12000, 3000), C["sand"])
    for k in range(40):
        rr = random.Random(k)
        flat(ctx, lambda c, rr=rr: p_ellipse(c, rr.uniform(-1500, 3500), rr.uniform(920, 1300), rr.uniform(20, 60), 8),
             C["sand2"])
    stroke(ctx, [(-4000, 900), (8000, 900)], BG_OUT)


def cl_street(ctx, t, layer, p):
    """A street at dusk: a purple-orange sky, houses with lit windows, a pavement from y = 760 to 830, a kerb, a wet
    road below; p: lights (0..1 headlights sweeping across, no car shown hitting anything), fence (a lot with a
    chain-link fence instead of the houses)."""
    layer(0.5)
    g = cairo.LinearGradient(0, -300, 0, 760)
    for u, c_ in ((0, "#2b2a5a"), (0.6, "#b4607a"), (1.0, "#f0a860")):
        r, gg, b = hexc(c_)
        g.add_color_stop_rgb(u, r, gg, b)
    ctx.rectangle(-4000, -4000, 12000, 9000)
    ctx.set_source(g)
    ctx.fill()
    layer(0.85)
    for k in range(-3, 10):
        x = k * 330
        h = 360 + (k % 3) * 70
        flat(ctx, lambda c, x=x, h=h: c.rectangle(x, 760 - h, 280, h), hexc("#2a2740"))
        flat(ctx, lambda c, x=x, h=h: p_poly(c, [(x - 20, 760 - h), (x + 140, 760 - h - 120), (x + 300, 760 - h)]),
             hexc("#2a2740"))
        for j in range(2):
            flat(ctx, lambda c, x=x, h=h, j=j: c.rectangle(x + 50 + j * 120, 760 - h + 90, 60, 70), hexc("#f6d36a"),
                 a=0.85 if (k + j) % 3 else 0.3)
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-4000, 760, 12000, 70), hexc("#8a8494"))
    flat(ctx, lambda c: c.rectangle(-4000, 822, 12000, 16), hexc("#c8c2cc"))
    flat(ctx, lambda c: c.rectangle(-4000, 838, 12000, 3000), hexc("#3a3846"))
    for k in range(-10, 30):
        flat(ctx, lambda c, k=k: c.rectangle(k * 300, 1000, 150, 14), hexc("#e8e0a0"), a=0.7)
    for k in range(-10, 30):   # wet shine
        flat(ctx, lambda c, k=k: p_ellipse(c, k * 260 + 80, 920, 70, 6), hexc("#f0a860"), a=0.25)
    lt = p.get("lights", 0.0)
    if lt > 0.01:   # headlights: two soft beams and their reflection, sweeping left to right
        x0 = -600 + 3200 * ((t * 0.35) % 1) if p.get("sweep", True) else p.get("lx", 600)
        for dy in (0, 40):
            g2 = cairo.RadialGradient(x0, 900 + dy, 10, x0, 900 + dy, 520)
            g2.add_color_stop_rgba(0, 1, 0.97, 0.8, 0.85 * lt)
            g2.add_color_stop_rgba(1, 1, 0.97, 0.8, 0)
            ctx.save()
            ctx.translate(0, 0)
            p_ellipse(ctx, x0 + 300, 900 + dy, 700, 120)
            ctx.set_source(g2)
            ctx.fill()
            ctx.restore()
        for dx in (0, 90):
            flat(ctx, lambda c, dx=dx: p_ellipse(c, x0 + dx, 900, 22, 16), hexc("#fffbe0"), a=lt)
    ctx.identity_matrix()
    ctx.rectangle(0, 0, 1920, 1080)
    ctx.set_source_rgba(0.1, 0.05, 0.25, 0.12)
    ctx.fill()


def cl_lot(ctx, t, layer, p):
    """An empty lot at dusk behind a chain-link fence (the feral colony); ground from y = 900."""
    layer(0.5)
    g = cairo.LinearGradient(0, -300, 0, 900)
    for u, c_ in ((0, "#3b3a6a"), (1.0, "#d98a6a")):
        r, gg, b = hexc(c_)
        g.add_color_stop_rgb(u, r, gg, b)
    ctx.rectangle(-4000, -4000, 12000, 9000)
    ctx.set_source(g)
    ctx.fill()
    layer(0.8)
    for k in range(-3, 10):
        flat(ctx, lambda c, k=k: c.rectangle(k * 420, 380 + (k % 2) * 60, 360, 600), hexc("#3a3550"))
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-4000, 900, 12000, 3000), hexc("#6f6a4f"))
    for k in range(60):
        rr = random.Random(k)
        stroke(ctx, [(rr.uniform(-1500, 3500), 910 + rr.uniform(0, 300)), (rr.uniform(-1500, 3500), 900 + rr.uniform(0, 300))],
               4, color=hexc("#8a8a5a"), a=0.5)


def cl_fence(ctx, t, p):
    """A chain-link fence in front of the lot; origin = bottom centre, width p w, height p h."""
    w, h = p.get("w", 2400), p.get("h", 560)
    ctx.save()
    ctx.rectangle(-w / 2, -h, w, h)
    ctx.clip()
    for k in range(-60, 60):
        x = k * 46
        stroke(ctx, [(x, -h), (x + h, 0)], 3.5, color=(0.75, 0.78, 0.8), a=0.85)
        stroke(ctx, [(x, 0), (x + h, -h)], 3.5, color=(0.75, 0.78, 0.8), a=0.85)
    ctx.restore()
    for x in range(int(-w / 2), int(w / 2) + 1, 400):
        stroke(ctx, [(x, 0), (x, -h - 20)], 16, color=(0.55, 0.58, 0.6))
    stroke(ctx, [(-w / 2, -h), (w / 2, -h)], 10, color=(0.55, 0.58, 0.6))


def cl_shelter(ctx, t, layer, p):
    """A shelter corridor in one-point perspective: kennel doors down both sides, a long floor."""
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), hexc("#cfd8d4"))
    vx, vy = 960, 470
    flat(ctx, lambda c: p_poly(c, [(-800, 1500), (vx - 120, vy + 80), (vx + 120, vy + 80), (2720, 1500)]), hexc("#9aa8a4"))
    flat(ctx, lambda c: p_poly(c, [(-800, -400), (vx - 120, vy - 140), (vx + 120, vy - 140), (2720, -400)]), hexc("#e8eeec"))
    flat(ctx, lambda c: c.rectangle(vx - 120, vy - 140, 240, 220), hexc("#f6f4e8"))
    for s in (-1, 1):
        for k in range(6):
            u0, u1 = 0.08 + k * 0.15, 0.08 + k * 0.15 + 0.11
            def P(u, yy, s=s):
                x = (960 + s * 1700) + (vx + s * 120 - (960 + s * 1700)) * u
                y = yy + (vy - yy) * u
                return x, y
            a, b = P(u0, -100), P(u1, -100)
            c_, d = P(u1, 1300), P(u0, 1300)
            a = (a[0], a[1] + (1 - u0) * 300)
            b = (b[0], b[1] + (1 - u1) * 300)
            c_ = (c_[0], c_[1] - (1 - u1) * 80)
            d = (d[0], d[1] - (1 - u0) * 80)
            shape(ctx, lambda c, q=(a, b, c_, d): p_poly(c, list(q)), hexc("#7f8c88"), BG_OUT * 0.6, None)
            for j in range(1, 6):
                f = j / 6
                top = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
                bot = (d[0] + (c_[0] - d[0]) * f, d[1] + (c_[1] - d[1]) * f)
                stroke(ctx, [top, bot], 4, color=(0.85, 0.88, 0.86))
    ctx.identity_matrix()
    ctx.rectangle(0, 0, 1920, 1080)
    ctx.set_source_rgba(0.1, 0.15, 0.2, 0.12)
    ctx.fill()


# ================================================================================================ props and diagrams

def cl_jar(ctx, t, p):
    """A big clay grain jar; origin = bottom centre; p: grain (0..1 grain spilling at the lip)."""
    col = hexc(p.get("col", "#b8704a"))
    shape(ctx, lambda c: p_smooth(c, [(-70, 0), (-130, -150), (-110, -290), (-60, -330), (60, -330), (110, -290), (130, -150),
                                      (70, 0)]), col, OUT, (0.05, 0.2), hi=(0.3, 0.2, 0.2))
    shape(ctx, lambda c: p_rrect(c, -78, -360, 156, 40, 12), darker(col, 0.85), OUT * 0.8, None)
    for k in range(2):
        stroke(ctx, [(-120, -200 + k * 40), (120, -200 + k * 40)], 5, color=darker(col, 0.75), a=0.7)
    if p.get("grain", 0.0) > 0.01:
        for k in range(14):
            rr = random.Random(k)
            flat(ctx, lambda c, rr=rr: p_ellipse(c, rr.uniform(-60, 60), -360 - rr.uniform(0, 30), 9, 6), hexc("#e8c86a"))


def cl_parch(ctx, t, p):
    """The parchment: mode "deal" (title THE DEAL, lines of small print, a paw print stamped at the bottom) or
    "ledger" (two columns; p left / right 0..1 fill the column lines; p foot 0..1 unrolls a small-print footnote).
    p: paw (0..1 the paw print), unroll (0..1 the sheet opens), w, h."""
    w, h = p.get("w", 760), p.get("h", 900)
    u = ease(min(1.0, p.get("unroll", 1.0)))
    if u <= 0.01:
        return
    hh = h * u
    ctx.save()
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2 + 10, -h / 2 + hh), (-w / 2 - 10, -h / 2 + hh)]
    shape(ctx, lambda c: p_poly(c, pts), C["parch"], OUT, (0.06, 0.15))
    for s in (-1, 1):   # rolled ends
        yy = -h / 2 if s < 0 else -h / 2 + hh
        shape(ctx, lambda c, yy=yy: p_rrect(c, -w / 2 - 30, yy - 26, w + 60, 52, 26), C["parch2"], OUT, (0.05, 0.2))
    ctx.rectangle(-w / 2, -h / 2 + 26, w, max(0, hh - 52))
    ctx.clip()
    mode = p.get("mode", "deal")
    if mode == "deal":
        text(ctx, "THE DEAL", 0, -h / 2 + 120, 110, "#5a3d24", 0)
        for k in range(9):
            y = -h / 2 + 230 + k * 50
            stroke(ctx, [(-w / 2 + 70, y), (w / 2 - 70 - (k % 3) * 60, y)], 9, color=hexc("#8a6a44"), a=0.55)
        paw = p.get("paw", 1.0)
        if paw > 0.01:
            ctx.save()
            ctx.translate(w * 0.18, h / 2 - 170)
            s = 1.0 if paw >= 1 else 1.6 - 0.6 * ease(paw)
            ctx.scale(s, s)
            col = (0.62, 0.22, 0.16)
            flat(ctx, lambda c: p_ellipse(c, 0, 20, 62, 50), col, a=min(1.0, paw * 2))
            for k, (x, y) in enumerate(((-58, -40), (-22, -72), (22, -72), (58, -40))):
                flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 21, 27), col, a=min(1.0, paw * 2))
            ctx.restore()
            stroke(ctx, [(-w / 2 + 70, h / 2 - 120), (-w / 2 + 300, h / 2 - 120)], 5, color=hexc("#5a3d24"))
    else:   # ledger: two columns
        stroke(ctx, [(0, -h / 2 + 80), (0, h / 2 - 80)], 7, color=hexc("#8a6a44"))
        stroke(ctx, [(-w / 2 + 50, -h / 2 + 150), (w / 2 - 50, -h / 2 + 150)], 7, color=hexc("#8a6a44"))
        flat(ctx, lambda c: p_ellipse(c, -w / 4, -h / 2 + 100, 34, 34), C["red"], a=0.9)   # minus / plus heads
        stroke(ctx, [(-w / 4 - 18, -h / 2 + 100), (-w / 4 + 18, -h / 2 + 100)], 8, color=(1, 1, 1))
        flat(ctx, lambda c: p_ellipse(c, w / 4, -h / 2 + 100, 34, 34), C["green"], a=0.9)
        stroke(ctx, [(w / 4 - 18, -h / 2 + 100), (w / 4 + 18, -h / 2 + 100)], 8, color=(1, 1, 1))
        stroke(ctx, [(w / 4, -h / 2 + 82), (w / 4, -h / 2 + 118)], 8, color=(1, 1, 1))
        for side, key in ((-1, "left"), (1, "right")):
            f = p.get(key, 0.0)
            n = 8
            for k in range(n):
                if f * n <= k:
                    break
                y = -h / 2 + 210 + k * 62
                x0 = -w / 2 + 50 if side < 0 else 30
                x1 = -30 if side < 0 else w / 2 - 50
                part = min(1.0, f * n - k)
                stroke(ctx, [(x0, y), (x0 + (x1 - x0 - (k % 3) * 30) * part, y)], 9, color=hexc("#6a4a2a"), a=0.7)
        ft = p.get("foot", 0.0)
        if ft > 0.01:
            pass
    ctx.restore()
    ft = p.get("foot", 0.0)
    if mode != "deal" and ft > 0.01:   # the small-print footnote unrolling below
        fh = 260 * ease(min(1.0, ft))
        shape(ctx, lambda c: p_rrect(c, -w * 0.35, h / 2 + 10, w * 0.7, fh, 10), C["parch"], OUT * 0.8, (0.05, 0.1))
        for k in range(int(fh // 34)):
            stroke(ctx, [(-w * 0.3, h / 2 + 40 + k * 34), (w * 0.28 - (k % 2) * 40, h / 2 + 40 + k * 34)], 5,
                   color=hexc("#8a6a44"), a=0.6)
        text(ctx, "*", -w * 0.32, h / 2 + 30, 60, "#5a3d24", 0)


def cl_map(ctx, t, p):
    """A simple map of the eastern Mediterranean and the Near East (no names): sea, land, Cyprus. p: near (0..1 a dot
    pulses on the Near East), cyprus (0..1 a dot on Cyprus), w."""
    w = p.get("w", 1300)
    k = w / 1300
    ctx.save()
    ctx.scale(k, k)
    shape(ctx, lambda c: p_rrect(c, -650, -400, 1300, 800, 30), hexc("#7fb6d9"), OUT, None)
    ctx.save()
    p_rrect(ctx, -650, -400, 1300, 800, 30)
    ctx.clip()
    land = hexc("#e9d3a0")
    # Anatolia (top), the Levant coast and the Fertile Crescent (right), Egypt / north Africa (bottom)
    shape(ctx, lambda c: p_smooth(c, [(-700, -420), (700, -420), (700, -150), (520, -130), (300, -170), (60, -150),
                                      (-200, -180), (-420, -130), (-700, -160)]), land, OUT * 0.8, None)
    shape(ctx, lambda c: p_smooth(c, [(700, -160), (300, -170), (230, -60), (210, 80), (160, 200), (120, 420), (700, 420)]),
          land, OUT * 0.8, None)
    shape(ctx, lambda c: p_smooth(c, [(-700, 250), (-300, 230), (0, 260), (130, 300), (150, 420), (-700, 420)]), land, OUT * 0.8,
          None)
    # Cyprus
    shape(ctx, lambda c: p_smooth(c, [(-60, -40), (40, -70), (110, -60), (60, -20), (-30, -10)]), land, OUT * 0.7, None)
    # the rivers of the Fertile Crescent
    stroke(ctx, [(380, -150), (430, -40), (520, 60), (640, 160)], 6, smooth=True, color=hexc("#5a9ec9"))
    stroke(ctx, [(470, -150), (560, -40), (640, 80)], 6, smooth=True, color=hexc("#5a9ec9"))
    ctx.restore()
    for key, (x, y) in (("near", (430, -60)), ("cyprus", (30, -40))):
        u = p.get(key, 0.0)
        if u <= 0.01:
            continue
        s = back_out(min(1.0, u))
        ph = (t * 1.2) % 1
        ctx.new_sub_path()
        ctx.arc(x, y, (20 + 70 * ph) * s, 0, 2 * math.pi)
        ctx.set_source_rgba(0.9, 0.22, 0.23, (1 - ph) * min(1.0, u))
        ctx.set_line_width(7)
        ctx.stroke()
        shape(ctx, lambda c, x=x, y=y, s=s: p_ellipse(c, x, y, 20 * s, 20 * s), C["red"], OUT * 0.7, None)
    ctx.restore()


def cl_cal(ctx, t, p):
    """A tear-off calendar: p mode "flip" (a big number, pages flipping as p day rises; numbers only), "three"
    (p n 0..3 pages side by side, no numbers), "years" (a grid of year boxes; p stamps 0..N paw stamps, p two_from =
    the box from which each year gets two stamps), "label" (p label shown big, e.g. 1987)."""
    mode = p.get("mode", "flip")
    if mode == "three":
        n = p.get("n", 3.0)
        for k in range(3):
            u = max(0.0, min(1.0, (n - k) * 2))
            if u <= 0:
                continue
            ctx.save()
            ctx.translate((k - 1) * 330, 0)
            s = back_out(u)
            ctx.scale(s, s)
            ctx.rotate(math.radians((k - 1) * 4))
            shape(ctx, lambda c: p_rrect(c, -140, -180, 280, 330, 16), (0.98, 0.97, 0.94), OUT, (0, 0.15))
            shape(ctx, lambda c: c.rectangle(-140, -180, 280, 70), C["red"], OUT, None)
            for j in range(4):
                stroke(ctx, [(-100, -60 + j * 50), (100, -60 + j * 50)], 8, color=hexc("#c8c0b0"))
            ctx.restore()
        return
    if mode == "years":
        st = p.get("stamps", 0.0)
        two = p.get("two_from", 99)
        cols, n = 5, p.get("boxes", 10)
        idx = 0
        for k in range(n):
            x, y = (k % cols - (cols - 1) / 2) * 190, (k // cols - 0.5) * 210
            shape(ctx, lambda c, x=x, y=y: p_rrect(c, x - 80, y - 90, 160, 180, 14), (0.98, 0.97, 0.94), OUT * 0.8, None)
            shape(ctx, lambda c, x=x, y=y: c.rectangle(x - 80, y - 90, 160, 40), C["red"], OUT * 0.8, None)
            for j in range(2 if k >= two else 1):
                if st > idx:
                    u = min(1.0, st - idx)
                    ox = (j - (0.5 if k >= two else 0)) * 60
                    _paw(ctx, x + ox, y + 25, 0.45 * (1.4 - 0.4 * ease(u)), (0.62, 0.22, 0.16), min(1.0, u * 2))
                idx += 1
        return
    shape(ctx, lambda c: p_rrect(c, -150, -190, 300, 330, 18), (0.98, 0.97, 0.94), OUT, (0, 0.15))
    shape(ctx, lambda c: c.rectangle(-150, -190, 300, 80), C["red"], OUT, None)
    for x in (-80, 80):
        shape(ctx, lambda c, x=x: p_ellipse(c, x, -196, 14, 22), PAL["steel"], OUT * 0.6, None)
    if mode == "label":
        text(ctx, p.get("label", ""), 0, 20, p.get("px", 110), "#222222", 0)
        return
    d = p.get("day", 1.0)
    text(ctx, str(int(math.floor(d + 1e-6))), 0, 30, 150, "#222222", 0)
    fl = d - math.floor(d + 1e-6)
    if 0.02 < fl < 0.98:
        hgt = 300 * (1 - fl)
        shape(ctx, lambda c: c.rectangle(-150, -110, 300, max(1, hgt * 0.8)), (0.93, 0.92, 0.88), OUT * 0.6, None)


def _paw(ctx, x, y, s, col, a=1.0):
    flat(ctx, lambda c: p_ellipse(c, x, y + 20 * s, 62 * s, 50 * s), col, a=a)
    for (dx, dy) in ((-58, -40), (-22, -72), (22, -72), (58, -40)):
        flat(ctx, lambda c, dx=dx, dy=dy: p_ellipse(c, x + dx * s, y + dy * s, 21 * s, 27 * s), col, a=a)


def cl_count(ctx, t, p):
    """A small counter plate showing a whole number (p v rounds down; numbers only)."""
    v = int(math.floor(p.get("v", 0.0) + 1e-6))
    if p.get("on", 1.0) <= 0.01 or v <= 0:
        return
    shape(ctx, lambda c: p_rrect(c, -90, -80, 180, 160, 30), hexc("#121628"), OUT * 0.7, None, a=0.92)
    text(ctx, str(v), 0, 4, 120, "#ffd34d", 0)


def cl_timeline(ctx, t, p):
    """A weeks bar 0..12 with week numbers; p lit (0..1) lights weeks a..b (default 2..7) from the left; p mode "life":
    two bars (p g1, g2 0..1 grow), the second longer."""
    if p.get("mode") == "life":
        for k, (key, ln, col) in enumerate((("g1", 900, C["steel"]), ("g2", 1100, C["green"]))):
            g = ease(min(1.0, p.get(key, 1.0)))
            y = -110 + k * 220
            shape(ctx, lambda c, y=y: p_rrect(c, -600, y - 50, 1200, 100, 50), hexc("#2a2638"), OUT * 0.8, None)
            if g > 0.01:
                shape(ctx, lambda c, y=y, g=g, ln=ln: p_rrect(c, -600, y - 50, ln * g, 100, 50), col, OUT * 0.8, (0.05, 0.15))
        return
    n, a, b = 12, p.get("a", 2), p.get("b", 7)
    x0, x1 = -760, 760
    shape(ctx, lambda c: p_rrect(c, x0, -50, x1 - x0, 100, 50), hexc("#2a2638"), OUT, None)
    lit = ease(min(1.0, p.get("lit", 1.0)))
    xa, xb = x0 + (x1 - x0) * a / n, x0 + (x1 - x0) * b / n
    if lit > 0.01:
        shape(ctx, lambda c: p_rrect(c, xa, -50, (xb - xa) * lit, 100, 30), C["yel"], OUT, (0.05, 0.15))
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        stroke(ctx, [(x, 50), (x, 80)], 5, color=(1, 1, 1))
        text(ctx, str(k), x, 125, 54, "#ffd34d" if a <= k <= b and lit > 0.5 else "#ffffff", 0)
    run = p.get("run", None)
    if run is not None:   # a "you are here" marker
        x = x0 + (x1 - x0) * run / n
        shape(ctx, lambda c: p_poly(c, [(x - 26, -110), (x + 26, -110), (x, -62)]), C["red"], OUT * 0.8, None)


def cl_puzzle(ctx, t, p):
    """The sweet receptor as two puzzle pieces on a tongue outline; p crack (0..1: the second piece cracks and
    slips)."""
    shape(ctx, lambda c: p_smooth(c, [(-420, -330), (420, -330), (460, 80), (300, 360), (0, 420), (-300, 360), (-460, 80)]),
          hexc("#e98a8a"), OUT, (0.05, 0.15))
    stroke(ctx, [(0, -300), (0, 300)], 8, color=hexc("#c86a6a"))
    cr = ease(min(1.0, p.get("crack", 0.0)))

    def piece(x, y, col, side):
        pts = [(-130, -130), (-30, -130), (-30, -170), (30, -170), (30, -130), (130, -130), (130, 130), (-130, 130)]
        if side > 0:
            pts = [(-130, -130), (130, -130), (130, 130), (-130, 130), (-130, 30), (-170, 30), (-170, -30), (-130, -30)]
        shape(ctx, lambda c: p_poly(c, [(x + a, y + b) for a, b in pts]), col, OUT, (0.05, 0.2))
    piece(-150, 0, hexc("#5aa0e0"), -1)
    ctx.save()
    ctx.translate(30 * cr, 40 * cr)
    ctx.rotate(0.18 * cr)
    piece(150, 0, hexc("#f2c14e"), 1)
    if cr > 0.01:
        stroke(ctx, [(160, -130), (130, -60), (190, -10), (140, 60), (170, 130)], 10, color=INK, a=cr)
    ctx.restore()


def cl_hearing(ctx, t, p):
    """A hearing bar that stretches: p grow 0..1 (left end fixed, right end runs out), with tick marks; a small ear at
    the left."""
    g = ease(min(1.0, p.get("grow", 1.0)))
    x0, x1 = -720, -720 + 1440 * g
    shape(ctx, lambda c: p_rrect(c, x0, -45, max(90, x1 - x0), 90, 45), hexc("#2a2638"), OUT, None)
    if x1 - x0 > 20:
        gr = cairo.LinearGradient(x0, 0, x1, 0)
        for u, c_ in ((0, "#5aa0e0"), (0.5, "#a06ae0"), (1.0, "#e05a9a")):
            r, gg, b = hexc(c_)
            gr.add_color_stop_rgb(u, r, gg, b)
        p_rrect(ctx, x0 + 8, -37, max(10, x1 - x0 - 16), 74, 37)
        ctx.set_source(gr)
        ctx.fill()
    for k in range(int(30 * g) + 1):
        x = x0 + k * 48
        stroke(ctx, [(x, 50), (x, 70 + (14 if k % 5 == 0 else 0))], 4, color=(1, 1, 1))
    for k in range(3):   # wave rings off the right end
        u = (t * 1.5 + k / 3) % 1
        ctx.new_sub_path()
        ctx.arc(x1, 0, 50 + 80 * u, -0.7, 0.7)
        ctx.set_source_rgba(1, 1, 1, 0.8 * (1 - u))
        ctx.set_line_width(6)
        ctx.stroke()


def cl_factory(ctx, t, p):
    """The taurine "factory": a small brick building with a chimney (no smoke), the label TAURINE and a hanging CLOSED
    sign; p closed (0..1 the sign drops in), under (0..1 the label is underlined), smoke (0..1)."""
    shape(ctx, lambda c: c.rectangle(-300, -260, 600, 300), hexc("#b5523e"), OUT, (0.05, 0.15))
    shape(ctx, lambda c: p_poly(c, [(-330, -260), (-180, -380), (-30, -260), (120, -380), (270, -260), (330, -260)]),
          hexc("#8a3d2e"), OUT, None)
    shape(ctx, lambda c: c.rectangle(170, -520, 70, 200), hexc("#8a3d2e"), OUT, None)
    for k in range(3):
        for j in range(2):
            shape(ctx, lambda c, k=k, j=j: c.rectangle(-250 + k * 120, -200 + j * 90, 70, 60), hexc("#2a3040"), OUT * 0.6, None)
    shape(ctx, lambda c: c.rectangle(150, -120, 110, 160), hexc("#5a3d24"), OUT * 0.8, None)
    shape(ctx, lambda c: p_rrect(c, -280, 70, 560, 110, 14), hexc("#121628"), OUT * 0.7, None)
    text(ctx, "TAURINE", 0, 125, 80, "#ffd34d", 0)
    un = p.get("under", 0.0)
    if un > 0.01:
        stroke(ctx, [(-230, 200), (-230 + 460 * ease(min(1.0, un)), 200)], 14, color=C["red"])
    cl = p.get("closed", 1.0)
    if cl > 0.01:
        ctx.save()
        ctx.translate(205, -160 + (1 - ease(min(1.0, cl))) * -260)
        ctx.rotate(0.08 * math.sin(t * 3))
        stroke(ctx, [(-60, -90), (0, -150), (60, -90)], 4)
        shape(ctx, lambda c: p_rrect(c, -130, -90, 260, 100, 10), C["red"], OUT * 0.8, None)
        text(ctx, "CLOSED", 0, -40, 60, "#ffffff", 0)
        ctx.restore()


def cl_can(ctx, t, p):
    """A cat-food can; p label: "" (a fish picture), a year ("1987") or "?" (a question mark); spin (0..1 turns round
    to show the label side)."""
    sp = p.get("spin", 1.0)
    sx = abs(math.cos(math.pi * (1 - min(1.0, sp)))) if sp < 1 else 1.0
    ctx.save()
    ctx.scale(max(0.08, sx), 1)
    shape(ctx, lambda c: c.rectangle(-120, -230, 240, 230), C["steel"], OUT, (0.05, 0.25))
    shape(ctx, lambda c: p_ellipse(c, 0, -230, 120, 26), lighter(C["steel"], 0.3), OUT * 0.8, None)
    shape(ctx, lambda c: c.rectangle(-120, -190, 240, 150), hexc(p.get("col", "#3b7dd8")), OUT * 0.8, None)
    lab = p.get("label", "")
    if sp >= 0.5 and lab:
        text(ctx, lab, 0, -112, 96 if len(lab) < 3 else 74, "#ffffff", 0)
    else:   # a little fish
        shape(ctx, lambda c: p_ellipse(c, -10, -115, 60, 32), hexc("#f2c14e"), OUT * 0.6, None)
        shape(ctx, lambda c: p_poly(c, [(45, -115), (85, -145), (85, -85)]), hexc("#f2c14e"), OUT * 0.6, None)
        flat(ctx, lambda c: p_ellipse(c, -45, -122, 6, 6), INK)
    ctx.restore()


def cl_heartline(ctx, t, p):
    """A heartbeat trace scrolling on a dark monitor; p strong (0..1 weak, flat-ish beats -> strong, tall beats)."""
    w, h = p.get("w", 1300), p.get("h", 480)
    shape(ctx, lambda c: p_rrect(c, -w / 2, -h / 2, w, h, 30), hexc("#0f1c1a"), OUT, None)
    ctx.save()
    p_rrect(ctx, -w / 2 + 20, -h / 2 + 20, w - 40, h - 40, 20)
    ctx.clip()
    for k in range(-10, 11):
        stroke(ctx, [(k * 70, -h / 2), (k * 70, h / 2)], 2, color=(0.2, 0.5, 0.35), a=0.4)
    st = ease(min(1.0, p.get("strong", 0.0)))
    pts = []
    for i in range(0, w + 1, 6):
        x = -w / 2 + i
        ph = ((i / w) * 4 + t * 0.9) % 1
        amp = 30 + 150 * st
        y = 0
        if 0.40 < ph < 0.44:
            y = -amp * (ph - 0.40) / 0.04
        elif 0.44 <= ph < 0.48:
            y = -amp + (amp * 1.4) * (ph - 0.44) / 0.04
        elif 0.48 <= ph < 0.52:
            y = amp * 0.4 * (1 - (ph - 0.48) / 0.04)
        y += (1 - st) * 6 * math.sin(i * 0.3 + t * 7)
        pts.append((x, y))
    stroke(ctx, pts, 12, color=(0.1, 0.4, 0.25), a=0.6)
    stroke(ctx, pts, 6, color=(0.45, 1.0, 0.6) if st > 0.5 else (1.0, 0.8, 0.35))
    ctx.restore()
    # a small heart at the corner, beating
    b = 1 + 0.12 * max(0.0, math.sin(t * 7)) * (0.3 + st)
    ctx.save()
    ctx.translate(w / 2 - 110, -h / 2 + 100)
    ctx.scale(b * 0.6, b * 0.6)
    _heart(ctx, C["red"])
    ctx.restore()


def _heart(ctx, col, a=1.0):
    shape(ctx, lambda c: p_smooth(c, [(0, 70), (-90, -10), (-80, -70), (-30, -80), (0, -40), (30, -80), (80, -70), (90, -10)]),
          col, OUT, (0.05, 0.15), a=a)


def cl_heart(ctx, t, p):
    """A small pink heart that pops in (p on) and floats."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    ctx.save()
    ctx.translate(0, -20 * math.sin(t * 2))
    s = back_out(min(1.0, on))
    ctx.scale(s, s)
    _heart(ctx, hexc("#f06a8a"))
    ctx.restore()


def cl_saucer(ctx, t, p):
    """A saucer of milk; origin = its bottom centre."""
    shape(ctx, lambda c: p_ellipse(c, 0, -14, 170, 34), hexc("#f4f4f8"), OUT, (0.05, 0.25))
    shape(ctx, lambda c: p_ellipse(c, 0, -22, 120, 20), C["milk"], OUT * 0.5, None)
    flat(ctx, lambda c: p_ellipse(c, -30, -26, 40, 6), (1, 1, 1))


def cl_bowl(ctx, t, p):
    """A food bowl; p full (0..1 kibble), label (text on a lab bowl, e.g. CASEIN DIET), col."""
    col = hexc(p.get("col", "#3b7dd8"))
    shape(ctx, lambda c: p_poly(c, [(-130, -80), (130, -80), (100, 0), (-100, 0)]), col, OUT, (0.05, 0.2))
    f = p.get("full", 0.0)
    if f > 0.01:
        for k in range(16):
            rr = random.Random(k)
            flat(ctx, lambda c, rr=rr: p_ellipse(c, rr.uniform(-100, 100), -84 - rr.uniform(0, 26 * f), 14, 10),
                 hexc("#a8682e"))
    else:
        flat(ctx, lambda c: p_ellipse(c, 0, -80, 125, 14), darker(col, 0.6))
    if p.get("label"):
        shape(ctx, lambda c: p_rrect(c, -230, 30, 460, 90, 12), C["paper"], OUT * 0.7, None)
        text(ctx, p["label"], 0, 75, 54, "#222222", 0)


def cl_lily(ctx, t, p):
    """A glass vase of true lilies (white trumpets, orange pollen); p horror (0..1 an eerie underlight), petal (0..1 a
    single falling petal), glow (0..1 pollen glows), kind ("lily" | "peace" | "calla"), caution (0..1 a small caution
    sign by it)."""
    kind = p.get("kind", "lily")
    if kind == "lily":
        shape(ctx, lambda c: p_smooth(c, [(-80, 0), (-100, -120), (-60, -260), (60, -260), (100, -120), (80, 0)]),
              (0.75, 0.9, 1.0), OUT, None, a=0.6)
        flat(ctx, lambda c: p_smooth(c, [(-88, -10), (-98, -110), (98, -110), (88, -10)]), (0.55, 0.8, 0.95), a=0.5)
        stems = [(-60, -560), (10, -640), (70, -540), (-20, -470)]
        for (x, y) in stems:
            stroke(ctx, [(0, -240), (x * 0.5, (y - 240) / 2), (x, y)], 10, smooth=True, color=hexc("#4f8f3a"))
        for k, (x, y) in enumerate(stems):   # leaves
            shape(ctx, lambda c, x=x, y=y, k=k: p_ellipse(c, x * 0.4 + (40 if k % 2 else -40), (y - 240) / 2 + 30, 26, 80,
                                                          0.6 if k % 2 else -0.6), hexc("#6fae4a"), OUT * 0.7, None)
        for k, (x, y) in enumerate(stems):   # the trumpets
            ctx.save()
            ctx.translate(x, y)
            ctx.rotate([-0.5, 0.1, 0.6, -0.1][k])
            for j in range(5):
                ang = -math.pi / 2 + (j - 2) * 0.55
                shape(ctx, lambda c, ang=ang: p_ellipse(c, 70 * math.cos(ang), 70 * math.sin(ang), 24, 72, ang + math.pi / 2),
                      C["lily"], OUT * 0.7, None)
            for j in range(4):
                ang = -math.pi / 2 + (j - 1.5) * 0.4
                stroke(ctx, [(0, 0), (60 * math.cos(ang), 60 * math.sin(ang))], 4, color=hexc("#6f9e4a"))
                flat(ctx, lambda c, ang=ang: p_ellipse(c, 64 * math.cos(ang), 64 * math.sin(ang), 12, 7, ang), C["pollen"])
            ctx.restore()
        gl = p.get("glow", 0.0)
        if gl > 0.01:
            for (x, y) in stems:
                g2 = cairo.RadialGradient(x, y - 50, 5, x, y - 50, 110)
                g2.add_color_stop_rgba(0, 1, 0.75, 0.2, 0.7 * gl)
                g2.add_color_stop_rgba(1, 1, 0.75, 0.2, 0)
                ctx.set_source(g2)
                ctx.arc(x, y - 50, 110, 0, 2 * math.pi)
                ctx.fill()
    else:   # peace lily / calla in a pot: a different, milder problem
        shape(ctx, lambda c: p_poly(c, [(-110, -200), (110, -200), (80, 0), (-80, 0)]), hexc("#b8704a"), OUT, (0.05, 0.2))
        for k in range(5):
            ang = -math.pi / 2 + (k - 2) * 0.35
            shape(ctx, lambda c, ang=ang: p_ellipse(c, 220 * math.cos(ang), -200 + 220 * math.sin(ang), 46, 130, ang + math.pi / 2),
                  hexc("#3f7f3a"), OUT * 0.7, None)
        for k in range(2):
            x = -60 + k * 120
            stroke(ctx, [(x * 0.3, -200), (x, -470)], 8, color=hexc("#4f8f3a"))
            if kind == "peace":
                shape(ctx, lambda c, x=x: p_ellipse(c, x, -520, 40, 80), C["lily"], OUT * 0.7, None)
                flat(ctx, lambda c, x=x: p_ellipse(c, x + 6, -510, 10, 34), hexc("#f2e6a0"))
            else:
                shape(ctx, lambda c, x=x: p_smooth(c, [(x - 10, -470), (x - 60, -560), (x + 10, -600), (x + 40, -520)]),
                      hexc("#f4f0e8"), OUT * 0.7, None)
    cau = p.get("caution", 0.0)
    if cau > 0.01:
        ctx.save()
        ctx.translate(190, -60)
        s = back_out(min(1.0, cau)) * 0.75
        ctx.scale(s, s)
        stroke(ctx, [(0, 0), (0, 70)], 10, color=hexc("#5a3d24"))
        shape(ctx, lambda c: p_poly(c, [(-70, 0), (0, -120), (70, 0)]), C["yel"], OUT, None)
        text(ctx, "!", 0, -38, 70, "#111111", 0)
        ctx.restore()
    hor = p.get("horror", 0.0)
    if hor > 0.01:
        g2 = cairo.RadialGradient(0, 0, 20, 0, -300, 700)
        g2.add_color_stop_rgba(0, 0.4, 1.0, 0.5, 0.35 * hor)
        g2.add_color_stop_rgba(1, 0.4, 1.0, 0.5, 0)
        ctx.set_source(g2)
        ctx.arc(0, -300, 700, 0, 2 * math.pi)
        ctx.fill()


def cl_petal(ctx, t, p):
    """Close-ups for the lily line: p kind "petal" (one white petal), "pollen" (a patch of orange fur with yellow
    pollen grains), "water" (a vase's water level, a little cloudy)."""
    kind = p.get("kind", "petal")
    if kind == "petal":
        shape(ctx, lambda c: p_ellipse(c, 0, 0, 120, 340, 0.4), C["lily"], OUT, (0.05, 0.2))
        stroke(ctx, [(-40, 250), (0, 0), (60, -260)], 6, smooth=True, color=hexc("#e8dcc8"))
    elif kind == "pollen":
        flat(ctx, lambda c: c.rectangle(-700, -400, 1400, 800), hexc("#e39a4a"))
        for k in range(160):
            rr = random.Random(k)
            x, y = rr.uniform(-680, 680), rr.uniform(-380, 380)
            stroke(ctx, [(x, y), (x + 40, y - 20)], 8, color=hexc("#b06f2a"), a=0.6)
        for k in range(30):
            rr = random.Random(100 + k)
            flat(ctx, lambda c, rr=rr: p_ellipse(c, rr.uniform(-200, 200), rr.uniform(-140, 140), 12, 10), C["pollen"])
    else:
        shape(ctx, lambda c: p_rrect(c, -260, -420, 520, 840, 60), (0.75, 0.9, 1.0), OUT, None, a=0.6)
        flat(ctx, lambda c: p_rrect(c, -248, -60, 496, 470, 50), hexc("#b8d8b0"), a=0.75)
        stroke(ctx, [(-248, -60), (248, -60)], 6, color=hexc("#7fa878"))
        for k in range(3):
            stroke(ctx, [(-60 + k * 60, -420), (-30 + k * 50, 300)], 12, color=hexc("#4f8f3a"))


def cl_qm(ctx, t, p):
    """A big question mark that bobs (no other text); p on, px."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    ctx.save()
    ctx.translate(0, 10 * math.sin(t * 3))
    s = back_out(min(1.0, on))
    ctx.scale(s, s)
    text(ctx, "?", 0, 0, p.get("px", 220), p.get("color", "#ffd34d"), 12)
    ctx.restore()


def cl_clock(ctx, t, p):
    """p mode "dial": a 24-hour stopwatch dial with a mark at 18 and the label 18; the hand runs to p h (hours).
    mode "wall": a big wall clock with a ticking second hand (p hr, mn for the hour and minute hands)."""
    if p.get("mode", "dial") == "wall":
        shape(ctx, lambda c: p_ellipse(c, 0, 0, 260, 260), (0.98, 0.97, 0.93), OUT * 1.4, (0.04, 0.15))
        for k in range(12):
            a = k * math.pi / 6
            stroke(ctx, [(220 * math.sin(a), -220 * math.cos(a)), (245 * math.sin(a), -245 * math.cos(a))], 10)
        hr, mn = p.get("hr", 3.0), p.get("mn", 0.0)
        ha, ma = (hr % 12 + mn / 60) * math.pi / 6, mn * math.pi / 30
        stroke(ctx, [(0, 0), (130 * math.sin(ha), -130 * math.cos(ha))], 18)
        stroke(ctx, [(0, 0), (190 * math.sin(ma), -190 * math.cos(ma))], 12)
        sa = math.floor(t) * math.pi / 30
        stroke(ctx, [(0, 0), (215 * math.sin(sa), -215 * math.cos(sa))], 5, color=C["red"])
        flat(ctx, lambda c: p_ellipse(c, 0, 0, 16, 16), INK)
        return
    shape(ctx, lambda c: p_rrect(c, -40, -330, 80, 60, 10), C["steel"], OUT, None)
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 280, 280), (0.98, 0.97, 0.93), OUT * 1.4, (0.04, 0.15))
    h = max(0.0, min(24.0, p.get("h", 0.0)))
    if h > 0.05:   # the elapsed wedge
        ctx.move_to(0, 0)
        ctx.arc(0, 0, 250, -math.pi / 2, -math.pi / 2 + h / 24 * 2 * math.pi)
        ctx.close_path()
        ctx.set_source_rgba(0.9, 0.22, 0.23, 0.25 + 0.25 * (h >= 18))
        ctx.fill()
    for k in range(24):
        a = k * math.pi / 12
        r0 = 225 if k % 6 else 200
        stroke(ctx, [(r0 * math.sin(a), -r0 * math.cos(a)), (255 * math.sin(a), -255 * math.cos(a))], 6 if k % 6 else 11)
    a18 = 18 * math.pi / 12
    stroke(ctx, [(170 * math.sin(a18), -170 * math.cos(a18)), (260 * math.sin(a18), -260 * math.cos(a18))], 16, color=C["red"])
    text(ctx, "18", 120 * math.sin(a18), -120 * math.cos(a18), 80, "#e5383b", 0)
    a = h / 24 * 2 * math.pi
    stroke(ctx, [(0, 0), (230 * math.sin(a), -230 * math.cos(a))], 14, color=INK)
    flat(ctx, lambda c: p_ellipse(c, 0, 0, 18, 18), INK)


def cl_bottle(ctx, t, p):
    """A pill bottle, closed (no pills shown), label EXTRA STRENGTH; origin = bottom centre."""
    shape(ctx, lambda c: p_rrect(c, -110, -330, 220, 330, 24), hexc("#e08a3a"), OUT, (0.05, 0.2), hi=(0.3, 0.2, 0.2))
    shape(ctx, lambda c: p_rrect(c, -125, -400, 250, 90, 16), (0.97, 0.97, 0.95), OUT, (0.05, 0.15))
    for k in range(6):
        stroke(ctx, [(-110 + k * 44, -395), (-110 + k * 44, -315)], 4, color=hexc("#c8c8c0"))
    shape(ctx, lambda c: c.rectangle(-110, -270, 220, 180), C["paper"], OUT * 0.7, None)
    text(ctx, "EXTRA", 0, -215, 52, "#c0392b", 0)
    text(ctx, "STRENGTH", 0, -150, 46, "#c0392b", 0)


def cl_gut(ctx, t, p):
    """An X-ray panel with a simple gut outline; p tangle (0..1 a red string tangle in it)."""
    shape(ctx, lambda c: p_rrect(c, -460, -340, 920, 680, 30), C["xray"], OUT, None)
    stroke(ctx, [(-380, -200), (-200, -250), (60, -220), (300, -160), (360, 0), (260, 140), (0, 180), (-220, 150),
                 (-300, 40), (-120, -40), (120, -40), (180, 60), (40, 100), (-80, 60)], 26, smooth=True, color=C["xline"], a=0.8)
    stroke(ctx, [(-380, -200), (-200, -250), (60, -220), (300, -160), (360, 0), (260, 140), (0, 180), (-220, 150),
                 (-300, 40), (-120, -40), (120, -40), (180, 60), (40, 100), (-80, 60)], 12, smooth=True, color=C["xray"])
    tg = p.get("tangle", 0.0)
    if tg > 0.01:
        pts = [(140 + 70 * math.cos(k * 1.3) * (0.6 + 0.4 * math.sin(k)), -40 + 50 * math.sin(k * 1.7)) for k in range(int(18 * tg) + 2)]
        stroke(ctx, pts, 9, smooth=True, color=C["red"])


def cl_string(ctx, t, p):
    """A loose piece of string on the floor (p pull 0..1 a paw drags its end)."""
    pu = p.get("pull", 0.0) + 0.1 * math.sin(t * 4)
    pts = [(-260, 0), (-150, -30), (-40, 10), (60, -20 + 20 * pu), (160 + 60 * pu, -10 - 30 * pu)]
    stroke(ctx, pts, 8, smooth=True, color=C["red"])


def cl_carrier(ctx, t, p):
    """The cat carrier (front three-quarter): a plastic box with a wire door and a handle; p open (0..1 door swings
    open), dungeon (0..1 lit from below in green), shadow (draw only its long shadow on the floor, p a)."""
    if p.get("shadow"):
        ctx.save()
        ctx.scale(1, 0.35)
        shape(ctx, lambda c: p_poly(c, [(-300, 0), (300, 0), (500, -600), (-100, -600)]), (0.05, 0.05, 0.1), 0, None,
              a=p.get("a", 0.5))
        flat(ctx, lambda c: p_rrect(c, 60, -700, 260, 80, 40), (0.05, 0.05, 0.1), a=p.get("a", 0.5))
        ctx.restore()
        return
    col = hexc("#9aa8b8")
    shape(ctx, lambda c: p_rrect(c, -300, -380, 600, 380, 40), col, OUT, (0.05, 0.2), hi=(0.3, 0.2, 0.2))
    shape(ctx, lambda c: p_rrect(c, -110, -470, 220, 110, 40), darker(col, 0.8), OUT, None)
    flat(ctx, lambda c: p_rrect(c, -70, -450, 140, 60, 26), hexc("#1b1724"))
    for k in range(4):
        flat(ctx, lambda c, k=k: p_rrect(c, 150, -320 + k * 70, 110, 30, 12), darker(col, 0.75))
    op = ease(min(1.0, p.get("open", 0.0)))
    flat(ctx, lambda c: p_rrect(c, -250, -320, 330, 270, 30), hexc("#1b1724"))
    ctx.save()
    ctx.translate(-250, 0)
    ctx.scale(1 - 0.8 * op, 1)
    for k in range(7):
        stroke(ctx, [(20 + k * 48, -320), (20 + k * 48, -50)], 8, color=C["steel"])
    stroke(ctx, [(10, -300), (320, -300)], 9, color=C["steel"])
    stroke(ctx, [(10, -70), (320, -70)], 9, color=C["steel"])
    ctx.restore()
    dg = p.get("dungeon", 0.0)
    if dg > 0.01:
        g2 = cairo.RadialGradient(0, 40, 10, 0, 40, 620)
        g2.add_color_stop_rgba(0, 0.3, 1.0, 0.4, 0.5 * dg)
        g2.add_color_stop_rgba(1, 0.3, 1.0, 0.4, 0)
        ctx.set_source(g2)
        p_ellipse(ctx, 0, 40, 620, 620)
        ctx.fill()


def cl_cone(ctx, t, p):
    """An empty cone of shame hanging on a hook (front view)."""
    stroke(ctx, [(0, -260), (0, -200), (30, -180)], 8, color=C["steel"])
    shape(ctx, lambda c: p_poly(c, [(-180, -170), (180, -170), (90, 120), (-90, 120)]), (0.85, 0.93, 1.0), OUT, None, a=0.75)
    shape(ctx, lambda c: p_ellipse(c, 0, 120, 90, 24), (0.7, 0.82, 0.95), OUT * 0.8, None)


def cl_scale(ctx, t, p):
    """A pet scale: a platform and a round dial on a post at its right end; p v (0..1 how far the needle swings)."""
    shape(ctx, lambda c: p_rrect(c, -260, -60, 520, 60, 14), C["steel"], OUT, (0.05, 0.2))
    stroke(ctx, [(230, -60), (230, -300)], 18, color=darker(C["steel"], 0.85))
    cx, cy = 230, -390
    shape(ctx, lambda c: p_ellipse(c, cx, cy, 110, 110), (0.98, 0.97, 0.93), OUT, (0.05, 0.15))
    for k in range(9):
        a = -2.3 + k * 4.6 / 8
        stroke(ctx, [(cx + 85 * math.sin(a), cy - 85 * math.cos(a)), (cx + 100 * math.sin(a), cy - 100 * math.cos(a))], 5)
    a = -2.3 + 4.6 * ease(min(1.0, p.get("v", 0.0))) + 0.04 * math.sin(t * 9) * (p.get("v", 0) > 0)
    stroke(ctx, [(cx, cy), (cx + 80 * math.sin(a), cy - 80 * math.cos(a))], 9, color=C["red"])
    flat(ctx, lambda c: p_ellipse(c, cx, cy, 10, 10), INK)


def cl_bill(ctx, t, p):
    """A page of bill text: lines of print with the three terms spelled as the bill spells them and underlined in
    turn (p under 0..3)."""
    shape(ctx, lambda c: p_rrect(c, -520, -420, 1040, 840, 14), C["paper"], OUT, (0.03, 0.12))
    terms = ["ONYCHECTOMY (DECLAWING)", "PHLANGECTOMY", "TENDONECTOMY"]
    rows = [None, None, 0, None, 1, None, 2, None]
    un = p.get("under", 0.0)
    for k, r in enumerate(rows):
        y = -330 + k * 92
        if r is None:
            for j in range(2):
                stroke(ctx, [(-440, y + j * 34 - 14), (440 - (k * 37 % 120) - j * 60, y + j * 34 - 14)], 8, color=hexc("#a8a49a"))
        else:
            text(ctx, terms[r], 0, y, 64, "#222222", 0)
            u = max(0.0, min(1.0, un - r))
            if u > 0:
                wpx = [760, 470, 460][r]
                stroke(ctx, [(-wpx / 2, y + 40), (-wpx / 2 + wpx * ease(u), y + 40)], 10, color=C["red"])


def cl_petmap(ctx, t, p):
    """The petting map: the adult cat with glowing zones; p red (0..1 the tail end glows red), green (0..1 between the
    eyes and ears glows green). Origin = the cat's feet."""
    cl_cat(ctx, t, {"age": "adult", "mood": p.get("mood", "calm"), "look": [1, 0], "ears_flat": p.get("ears_flat")})
    L, H, ll = CAT["length"], CAT["height"], CAT["leg_len"]
    by = -ll - H * 0.35
    hx, hy, hr = L * 0.48, by - H * 0.38, H * 0.48
    for key, (x, y, rx, ry), col in (("red", (-L * 0.42, by - 10, 110, 95), (0.9, 0.2, 0.2)),
                                     ("green", (hx - hr * 0.1, hy - hr * 0.62, 70, 48), (0.2, 0.85, 0.3))):
        u = p.get(key, 0.0)
        if u <= 0.01:
            continue
        pulse = 1 + 0.08 * math.sin(t * 6)
        g2 = cairo.RadialGradient(x, y, 5, x, y, rx * 1.4 * pulse)
        g2.add_color_stop_rgba(0, col[0], col[1], col[2], 0.85 * u)
        g2.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
        ctx.set_source(g2)
        p_ellipse(ctx, x, y, rx * 1.4 * pulse, ry * 1.4 * pulse)
        ctx.fill()


def cl_bars(ctx, t, p):
    """Two score bars (FAMILIAR, STRANGER) growing up from a baseline; p g (0..1), values a, b (bar heights by score)."""
    g = ease(min(1.0, p.get("g", 1.0)))
    for k, (lab, v, col) in enumerate((("FAMILIAR", p.get("a", 8.5), C["red"]), ("STRANGER", p.get("b", 5.0), C["steel"]))):
        x = -220 + k * 440
        hgt = v * 60 * g
        shape(ctx, lambda c, x=x, hgt=hgt: p_rrect(c, x - 120, -hgt, 240, max(4, hgt), 16), col, OUT, (0.05, 0.2))
        text(ctx, lab, x, 60, 58, "#ffffff", 0)
        if g > 0.95:
            text(ctx, f"{v:.1f}", x, -hgt - 60, 70, "#ffd34d", 0)
    stroke(ctx, [(-440, 0), (440, 0)], 8, color=(1, 1, 1))


def cl_bubbles(ctx, t, p):
    """Speech bubbles full of scribbles (random words, no letters); one bubble (p name index) glows when p glow."""
    pos = [(-560, -120), (-180, -260), (220, -150), (560, -260), (-380, 140), (380, 120)]
    gl = p.get("glow", 0.0)
    for k, (x, y) in enumerate(pos):
        n = p.get("n", 6.0)
        u = max(0.0, min(1.0, (n - k) * 2))
        if u <= 0:
            continue
        is_name = k == p.get("name", 2)
        ctx.save()
        ctx.translate(x, y + 6 * math.sin(t * 2 + k))
        s = back_out(u) * (1 + 0.15 * gl if is_name else 1)
        ctx.scale(s, s)
        col = C["yel"] if (is_name and gl > 0.3) else (0.97, 0.97, 0.97)
        shape(ctx, lambda c: p_ellipse(c, 0, 0, 160, 90), col, OUT, None)
        shape(ctx, lambda c: p_poly(c, [(-40, 70), (-90, 140), (10, 80)]), col, OUT, None)
        flat(ctx, lambda c: p_ellipse(c, 0, 0, 158, 88), col)
        rr = random.Random(k)
        for j in range(2):
            pts = [(-100 + i * 20, -20 + j * 40 + rr.uniform(-10, 10)) for i in range(11)]
            stroke(ctx, pts, 7, smooth=True, color=(0.3, 0.3, 0.3))
        if is_name and gl > 0.01:   # the name: a little paw print instead of letters
            _paw(ctx, 0, 0, 0.6, (0.62, 0.22, 0.16), gl)
        ctx.restore()


def cl_wave(ctx, t, p):
    """A purr waveform (low rumble) with a smaller sharp wave inside it; p hi (0..1 the sharp wave highlighted), cry
    (1 shown, 0 erased)."""
    w = 1400
    shape(ctx, lambda c: p_rrect(c, -w / 2, -260, w, 520, 30), hexc("#14182a"), OUT, None)
    cry = p.get("cry", 1.0)
    hi = p.get("hi", 0.0)
    pts, pts2 = [], []
    for i in range(0, w - 80, 5):
        x = -w / 2 + 40 + i
        y = 120 * math.sin(i * 0.035 + t * 4) * (0.7 + 0.3 * math.sin(i * 0.004))
        pts.append((x, y))
        if 0.35 * w < i < 0.75 * w:
            pts2.append((x, y + 40 * math.sin(i * 0.5 + t * 20)))
    stroke(ctx, pts, 12, color=(0.4, 0.7, 1.0))
    if cry > 0.01 and pts2:
        if hi > 0.01:
            x0, x1 = pts2[0][0], pts2[-1][0]
            shape(ctx, lambda c: p_rrect(c, x0 - 20, -220, x1 - x0 + 40, 440, 20), C["yel"], 0, None, a=0.22 * hi)
        stroke(ctx, pts2, 6, color=(1.0, 0.45, 0.4) if hi > 0.3 else (0.9, 0.9, 1.0), a=cry)
    er = p.get("erase", 0.0)
    if er > 0.01 and pts2:   # an eraser block wiping across
        x0, x1 = pts2[0][0], pts2[-1][0]
        x = x0 + (x1 - x0) * ease(min(1.0, er))
        shape(ctx, lambda c: p_rrect(c, x - 50, -110, 100, 70, 12), hexc("#f2a7a7"), OUT * 0.8, None)
        shape(ctx, lambda c: p_rrect(c, x - 50, -40, 100, 26, 8), hexc("#3b7dd8"), OUT * 0.8, None)


def cl_listener(ctx, t, p):
    """A simple listener (head and shoulders) with headphones and a rating card; p wince (0..1), mark (0..1 the pen
    marks the card), col (shirt)."""
    col = hexc(p.get("col", "#5d7fa8"))
    shape(ctx, lambda c: p_smooth(c, [(-170, 0), (-150, -150), (150, -150), (170, 0)]), col, OUT, (0.05, 0.15))
    shape(ctx, lambda c: p_ellipse(c, 0, -260, 105, 120), hexc(p.get("skin", "#f0c8a0")), OUT, (0.05, 0.15))
    wn = p.get("wince", 0.0)
    eyes(ctx, 0, -270, 18, 40, (0, 0), "angry" if wn > 0.5 else "calm", 0.6 * wn if wn > 0.5 else 0.0, OUT * 0.6)
    mouth(ctx, 0, -205, 50, "frown" if wn > 0.5 else "smile", 0.0, OUT * 0.6)
    ctx.new_sub_path()
    ctx.arc(0, -270, 125, math.pi * 1.05, math.pi * 1.95)
    ctx.set_line_width(18)
    src(ctx, INK)
    ctx.stroke()
    for s in (-1, 1):
        shape(ctx, lambda c, s=s: p_rrect(c, s * 118 - 30, -320, 60, 100, 20), hexc("#333344"), OUT * 0.8, None)
    shape(ctx, lambda c: p_rrect(c, 60, -110, 170, 120, 10), C["paper"], OUT * 0.8, None)
    for k in range(3):
        shape(ctx, lambda c, k=k: c.rectangle(80 + k * 50, -80, 34, 34), (1, 1, 1), OUT * 0.5, None)
    mk = p.get("mark", 0.0)
    if mk > 0.01:
        k = int(p.get("box", 2))
        stroke(ctx, [(84 + k * 50, -60), (96 + k * 50, -48), (116 + k * 50, -78)], 7, color=C["red"], a=min(1.0, mk * 2))


def cl_baby(ctx, t, p):
    """A baby-shaped silhouette (p a alpha)."""
    a = p.get("a", 0.5)
    if a <= 0.01:
        return
    col = (0.95, 0.85, 1.0)
    flat(ctx, lambda c: p_ellipse(c, 0, -260, 110, 115), col, a=a)
    flat(ctx, lambda c: p_ellipse(c, 0, -60, 130, 120), col, a=a)
    for s in (-1, 1):
        flat(ctx, lambda c, s=s: p_ellipse(c, s * 140, -110, 40, 70, s * 0.6), col, a=a)
        flat(ctx, lambda c, s=s: p_ellipse(c, s * 60, 50, 50, 40), col, a=a)


def cl_lightbox(ctx, t, p):
    """An X-ray light box with films of a cat's skeleton; p n (0..3 films slid in), spots (0..1 joint marks glow),
    q (0..1 a small question mark by a paw)."""
    shape(ctx, lambda c: p_rrect(c, -720, -380, 1440, 760, 24), hexc("#d8e8f0"), OUT, (0.03, 0.1))
    n = p.get("n", 3.0)
    for k in range(3):
        u = max(0.0, min(1.0, n - k))
        if u <= 0:
            continue
        x = -460 + k * 460 + (1 - ease(u)) * 900
        ctx.save()
        ctx.translate(x, 0)
        shape(ctx, lambda c: p_rrect(c, -210, -320, 420, 640, 10), C["xray"], OUT * 0.7, None)
        # a little cat skeleton, side view
        stroke(ctx, [(-150, -20), (-60, -60), (40, -60), (110, -30)], 10, smooth=True, color=C["xline"])
        for j in range(8):
            flat(ctx, lambda c, j=j: p_ellipse(c, -140 + j * 32, -40 - 20 * math.sin(j * 0.4), 9, 12), C["xline"])
        flat(ctx, lambda c: p_ellipse(c, 150, -60, 50, 38), C["xline"], a=0.85)
        for lx in (-110, 70):
            stroke(ctx, [(lx, -30), (lx - 10, 90), (lx + 10, 200)], 9, color=C["xline"])
            sp = p.get("spots", 0.0)
            if sp > 0.01:
                for jy in (90, 200):
                    flat(ctx, lambda c, lx=lx, jy=jy: p_ellipse(c, lx - 10 + (jy == 200) * 20, jy, 22, 22), (1.0, 0.5, 0.2),
                         a=sp * (0.6 + 0.4 * math.sin(t * 6)))
        stroke(ctx, [(-170, -30), (-230, -120)], 7, smooth=True, color=C["xline"])
        ctx.restore()
    if p.get("q", 0.0) > 0.01:
        cl_qm(ctx, t, {"on": p["q"], "px": 120})


def cl_clip(ctx, t, p):
    """A clipboard with a big figure (p text, e.g. 11%) and an optional sub-label (p sub)."""
    shape(ctx, lambda c: p_rrect(c, -230, -310, 460, 620, 24), hexc("#b07a48"), OUT, (0.05, 0.2))
    shape(ctx, lambda c: c.rectangle(-195, -260, 390, 540), C["paper"], OUT * 0.8, None)
    shape(ctx, lambda c: p_rrect(c, -90, -340, 180, 70, 16), C["steel"], OUT, None)
    for k in range(3):
        stroke(ctx, [(-150, 140 + k * 40), (150 - k * 30, 140 + k * 40)], 7, color=hexc("#b8b4a8"))
    if p.get("text"):
        on = p.get("on", 1.0)
        if on > 0.01:
            text(ctx, p["text"], 0, -100, 150, "#c0392b", 0, a=min(1.0, on * 2))
            if p.get("sub"):
                text(ctx, p["sub"], 0, 40, 34, "#222222", 0, a=min(1.0, on * 2))


def cl_litter(ctx, t, p):
    """A litter box (side view); origin = bottom centre."""
    shape(ctx, lambda c: p_poly(c, [(-170, -110), (170, -110), (150, 0), (-150, 0)]), hexc(p.get("col", "#6aa0c8")), OUT,
          (0.05, 0.2))
    flat(ctx, lambda c: p_ellipse(c, 0, -110, 165, 16), hexc("#d9cfb8"))


def cl_hairball(ctx, t, p):
    """A hairball on the rug with a tiny flag stuck in it (p flag 0..1)."""
    shape(ctx, lambda c: p_blob(c, 0, -30, 70, 34, 0.25, seed=3), hexc("#b07a48"), OUT, (0.05, 0.2))
    for k in range(6):
        a = k * 1.1
        stroke(ctx, [(40 * math.cos(a), -30 + 18 * math.sin(a)), (75 * math.cos(a + 0.2), -30 + 30 * math.sin(a + 0.2))], 4,
               color=hexc("#8a5a2a"))
    f = p.get("flag", 0.0)
    if f > 0.01:
        ctx.save()
        ctx.translate(10, -50)
        s = back_out(min(1.0, f))
        ctx.scale(s, s)
        stroke(ctx, [(0, 0), (0, -140)], 6)
        shape(ctx, lambda c: p_poly(c, [(0, -140), (80, -118 + 6 * math.sin(t * 6)), (0, -96)]), C["green"], OUT * 0.7, None)
        ctx.restore()


def cl_mirror(ctx, t, p):
    """A dentist's mirror (long handle, small round mirror)."""
    stroke(ctx, [(-260, 120), (60, -20)], 22, color=C["steel"])
    stroke(ctx, [(60, -20), (110, -60)], 10, color=C["steel"])
    shape(ctx, lambda c: p_ellipse(c, 140, -80, 52, 52), (0.85, 0.92, 1.0), OUT, None)
    flat(ctx, lambda c: p_ellipse(c, 125, -95, 16, 10, -0.5), (1, 1, 1))


def cl_row(ctx, t, p):
    """A long row of small cat silhouettes (sitting); p n (how many), fade (indices that fade to outlines, with p f
    0..1), w (spacing), outline (0..1 every cat drawn as a pale outline instead)."""
    n = int(p.get("n", 10))
    sp = p.get("w", 160)
    fades = p.get("fade", [])
    f = p.get("f", 0.0)
    ol = p.get("outline", 0.0)
    for k in range(n):
        x = (k - (n - 1) / 2) * sp
        a = 1.0 - (f * 0.85 if k in fades else 0.0)
        ctx.save()
        ctx.translate(x, 0)
        s = p.get("s", 1.0)
        ctx.scale(s, s)
        col = hexc(p.get("col", "#efe6d2"))
        pts = [(-40, 0), (-48, -90), (-30, -150), (-34, -205), (-18, -180), (0, -185), (18, -180), (34, -205), (30, -150),
               (48, -90), (40, 0)]
        if k in fades and f > 0.01:
            shape(ctx, lambda c: p_smooth(c, pts), (1, 1, 1), 5, None, a=0.0)
            ctx.save()
            p_smooth(ctx, pts)
            ctx.set_source_rgba(1, 1, 1, 0.9)
            ctx.set_line_width(5)
            ctx.stroke()
            ctx.restore()
        shape(ctx, lambda c: p_smooth(c, pts), col, 0, None, a=a)
        stroke(ctx, [(38, -10), (80, -30), (90, -80)], 12, smooth=True, color=col, a=a)
        ctx.restore()


def cl_kitout(ctx, t, p):
    """Four kitten outlines in a row; three fade out in turn (p f 0..3)."""
    f = p.get("f", 0.0)
    for k in range(4):
        x = (k - 1.5) * 220
        a = 1.0 if k == 3 else max(0.0, 1.0 - max(0.0, f - k))
        if a <= 0.01:
            continue
        ctx.save()
        ctx.translate(x, 0)
        ctx.scale(0.55, 0.55)
        cl_cat(ctx, t, {"age": "kitten", "sil": 0.0, "a": a, "look": [1, 0]})
        ctx.restore()


def cl_cake(ctx, t, p):
    """A slice of birthday cake with a candle (p lit 0..1 flame), or p mode "big": a round cake with candles that the old
    cat blows out (p out 0..1)."""
    if p.get("mode") == "big":
        shape(ctx, lambda c: p_rrect(c, -230, -170, 460, 170, 20), hexc("#f2d0a0"), OUT, (0.05, 0.2))
        shape(ctx, lambda c: p_rrect(c, -230, -190, 460, 60, 20), hexc("#f7b8c8"), OUT, None)
        out = p.get("out", 0.0)
        for k in range(5):
            x = -160 + k * 80
            shape(ctx, lambda c, x=x: c.rectangle(x - 10, -280, 20, 90), [C["blue"], C["yel"], C["red"]][k % 3], OUT * 0.6, None)
            fa = max(0.0, 1.0 - out * 1.5 + k * 0.1) if out > 0 else 1.0
            if fa > 0.05:
                flat(ctx, lambda c, x=x: p_ellipse(c, x + 6 * math.sin(t * 12 + k), -300, 12, 20), hexc("#ffb030"), a=min(1.0, fa))
            else:
                stroke(ctx, [(x, -290), (x + 10, -330), (x - 5, -370)], 5, smooth=True, color=(0.7, 0.7, 0.7), a=0.6)
        return
    shape(ctx, lambda c: p_poly(c, [(-120, 0), (120, 0), (120, -110), (-120, -60)]), hexc("#f2d0a0"), OUT, (0.05, 0.2))
    shape(ctx, lambda c: p_poly(c, [(-120, -60), (120, -110), (120, -135), (-120, -80)]), hexc("#f7b8c8"), OUT * 0.8, None)
    stroke(ctx, [(-120, -40), (120, -60)], 7, color=hexc("#c86a8a"))
    shape(ctx, lambda c: c.rectangle(20, -220, 18, 100), C["blue"], OUT * 0.6, None)
    flat(ctx, lambda c: p_ellipse(c, 29 + 4 * math.sin(t * 12), -238, 10, 17), hexc("#ffb030"))


def cl_box(ctx, t, p):
    """A cardboard box on a high shelf (a safe place); origin = shelf top centre."""
    shape(ctx, lambda c: p_rrect(c, -330, 0, 660, 34, 6), hexc("#8a5a3a"), OUT, None)
    for s in (-1, 1):
        shape(ctx, lambda c, s=s: p_poly(c, [(s * 290, 34), (s * 290, 110), (s * 230, 34)]), hexc("#6b4a2f"), OUT * 0.7, None)
    shape(ctx, lambda c: c.rectangle(-200, -230, 400, 230), hexc("#c99a5a"), OUT, (0.05, 0.15))
    shape(ctx, lambda c: p_poly(c, [(-200, -230), (-260, -300), (-120, -300), (-80, -230)]), hexc("#b8884a"), OUT * 0.8, None)
    shape(ctx, lambda c: p_poly(c, [(200, -230), (260, -300), (120, -300), (80, -230)]), hexc("#b8884a"), OUT * 0.8, None)


def cl_station(ctx, t, p):
    """One of the four stations: p kind "food" (bowl), "water" (water bowl), "litter", "scratch" (a sisal post)."""
    k = p.get("kind", "food")
    if k == "food":
        cl_bowl(ctx, t, {"full": 1.0, "col": "#e5383b"})
    elif k == "water":
        shape(ctx, lambda c: p_poly(c, [(-120, -70), (120, -70), (95, 0), (-95, 0)]), C["blue"], OUT, (0.05, 0.2))
        flat(ctx, lambda c: p_ellipse(c, 0, -70, 112, 12), hexc("#9fd4f0"))
    elif k == "litter":
        cl_litter(ctx, t, {})
    else:
        shape(ctx, lambda c: p_rrect(c, -150, -30, 300, 30, 8), hexc("#8a5a3a"), OUT, None)
        shape(ctx, lambda c: c.rectangle(-45, -420, 90, 390), hexc("#d9b87a"), OUT, (0.05, 0.15))
        for j in range(12):
            stroke(ctx, [(-45, -400 + j * 32), (45, -390 + j * 32)], 4, color=hexc("#b8945a"))
        shape(ctx, lambda c: p_rrect(c, -110, -450, 220, 40, 10), hexc("#8a5a3a"), OUT, None)


def cl_toy(ctx, t, p):
    """A toy: p kind "mouse" (a toy mouse on a string, p sx/sy string start offset), "ball" (a yarn ball); p blur
    (0..1 the toy goes soft: drawn as faint offset copies)."""
    bl = p.get("blur", 0.0)
    offs = [(0, 0, 1.0)] if bl < 0.05 else [(dx * 14 * bl, dy * 14 * bl, 0.3) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
    for dx, dy, a in offs:
        ctx.save()
        ctx.translate(dx, dy)
        if p.get("kind", "ball") == "ball":
            shape(ctx, lambda c: p_ellipse(c, 0, -60, 60, 60), C["red"], OUT if bl < 0.05 else 0, (0.05, 0.2), a=a)
            for j in range(4):
                ctx.new_sub_path()
                ctx.arc(-10 + j * 8, -60, 30 + j * 8, 0.5 + j, 2.6 + j)
                ctx.set_source_rgba(0.6, 0.1, 0.1, a)
                ctx.set_line_width(4)
                ctx.stroke()
        else:
            shape(ctx, lambda c: p_ellipse(c, 0, -30, 60, 32), hexc("#9a9aa8"), OUT, (0.05, 0.2), a=a)
            shape(ctx, lambda c: p_ellipse(c, 40, -56, 18, 18), hexc("#c8c8d0"), OUT * 0.7, None, a=a)
            stroke(ctx, [(-60, -30), (-120, -10), (-220 + p.get("sx", 0), -40 + p.get("sy", 0))], 4, smooth=True,
                   color=(0.3, 0.3, 0.3), a=a)
        ctx.restore()


def cl_eyes(ctx, t, p):
    """Two glowing cat eyes in the dark that blink (p blink 0..1)."""
    bl = p.get("blink", 0.0)
    for s in (-1, 1):
        ctx.save()
        ctx.translate(s * 60, 0)
        ctx.scale(1, max(0.06, 1 - bl))
        g2 = cairo.RadialGradient(0, 0, 4, 0, 0, 70)
        g2.add_color_stop_rgba(0, 0.9, 1.0, 0.5, 0.6)
        g2.add_color_stop_rgba(1, 0.9, 1.0, 0.5, 0)
        ctx.set_source(g2)
        ctx.arc(0, 0, 70, 0, 2 * math.pi)
        ctx.fill()
        shape(ctx, lambda c: p_ellipse(c, 0, 0, 34, 26), hexc("#d8f060"), OUT * 0.6, None)
        flat(ctx, lambda c: p_ellipse(c, 0, 0, 8, 22), INK)
        ctx.restore()


def cl_chair(ctx, t, p):
    """A simple wooden chair (side view); origin = floor."""
    col = hexc("#8a5a3a")
    stroke(ctx, [(-90, 0), (-90, -230)], 22, color=col)
    stroke(ctx, [(90, 0), (90, -230)], 22, color=col)
    shape(ctx, lambda c: p_rrect(c, -120, -250, 240, 34, 8), lighter(col, 0.15), OUT, None)
    stroke(ctx, [(-100, -250), (-110, -520)], 22, color=col)
    shape(ctx, lambda c: p_rrect(c, -130, -520, 50, 200, 10), lighter(col, 0.15), OUT, None)


def cl_dropper(ctx, t, p):
    """A dropper; p drip (0..1 a drop falls)."""
    shape(ctx, lambda c: p_rrect(c, -40, -320, 80, 110, 34), hexc("#e5383b"), OUT, (0.05, 0.2))
    shape(ctx, lambda c: p_poly(c, [(-28, -215), (28, -215), (12, 0), (-12, 0)]), (0.85, 0.93, 1.0), OUT, None, a=0.8)
    flat(ctx, lambda c: p_poly(c, [(-20, -120), (20, -120), (10, -10), (-10, -10)]), hexc("#f2d36a"), a=0.8)
    d = p.get("drip", 0.0)
    if 0.01 < d < 1:
        shape(ctx, lambda c: p_ellipse(c, 0, 30 + 200 * ease(d), 14, 20), hexc("#f2d36a"), OUT * 0.6, None)


def cl_eye(ctx, t, p):
    """An eye diagram (side section): lens and the light-sensing layer at the back, which dims (p dim 0..1)."""
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 300, 260), (0.98, 0.97, 0.94), OUT, (0.05, 0.12))
    dm = p.get("dim", 0.0)
    ctx.new_sub_path()
    ctx.arc(0, 0, 250, math.pi * 0.62, math.pi * 1.38)
    ctx.set_source_rgba(1.0 - 0.6 * dm, 0.75 - 0.5 * dm, 0.25 - 0.1 * dm, 1)
    ctx.set_line_width(40)
    ctx.stroke()
    shape(ctx, lambda c: p_ellipse(c, 200, 0, 50, 110), (0.8, 0.9, 1.0), OUT * 0.8, None)
    for k in range(3):
        stroke(ctx, [(560, -60 + k * 60), (240, -20 + k * 20)], 5, color=C["yel"], a=0.8)


def cl_desk(ctx, t, p):
    """A vet's desk (1987): a desk, a stack of heart scans (sheets with a heart outline), a lamp."""
    shape(ctx, lambda c: c.rectangle(-500, -320, 1000, 50), hexc("#8a5a3a"), OUT, (0.03, 0.15))
    for x in (-460, 420):
        shape(ctx, lambda c, x=x: c.rectangle(x, -270, 40, 270), hexc("#6b4a2f"), OUT * 0.8, None)
    for k in range(5):
        ctx.save()
        ctx.translate(-150 + k * 4, -330 - k * 12)
        ctx.rotate(0.05 * (k % 2) - 0.02)
        shape(ctx, lambda c: c.rectangle(-170, -110, 340, 120), C["xray"], OUT * 0.6, None)
        ctx.restore()
    ctx.save()
    ctx.translate(-150 + 16, -380)
    ctx.scale(0.45, 0.45)
    shape(ctx, lambda c: p_smooth(c, [(0, 70), (-90, -10), (-80, -70), (-30, -80), (0, -40), (30, -80), (80, -70), (90, -10)]),
          C["xray"], 8, None)
    ctx.set_source_rgb(*C["xline"])
    ctx.set_line_width(10)
    p_smooth(ctx, [(0, 70), (-90, -10), (-80, -70), (-30, -80), (0, -40), (30, -80), (80, -70), (90, -10)])
    ctx.stroke()
    ctx.restore()
    stroke(ctx, [(330, -320), (330, -520), (250, -580)], 12, color=hexc("#3a3a4a"))
    shape(ctx, lambda c: p_poly(c, [(190, -620), (300, -560), (240, -520)]), hexc("#2f8f8a"), OUT * 0.8, None)


def cl_mop(ctx, t, p):
    """A mop leaning in the corner."""
    ctx.save()
    ctx.rotate(0.15)
    stroke(ctx, [(0, -620), (0, -80)], 16, color=hexc("#c8a070"))
    shape(ctx, lambda c: p_rrect(c, -80, -100, 160, 40, 10), C["steel"], OUT, None)
    for k in range(9):
        stroke(ctx, [(-70 + k * 17, -60), (-80 + k * 19, 10)], 12, color=hexc("#ece6d6"))
    ctx.restore()


def cl_paper(ctx, t, p):
    """A sheet: p kind "bill" (a vet bill: lines and a coin stack, no figures), "paper" (a study page; p verdict "tick" |
    "cross" | "q" stamped in a circle with p stamp 0..1), "under4" (a small flat line chart, no labels)."""
    k = p.get("kind", "paper")
    shape(ctx, lambda c: p_rrect(c, -220, -290, 440, 580, 12), C["paper"], OUT, (0.03, 0.12))
    if k == "under4":
        stroke(ctx, [(-170, 200), (180, 200)], 7)
        stroke(ctx, [(-170, 200), (-170, -200)], 7)
        stroke(ctx, [(-160, 150), (170, 145)], 12, color=C["red"])
        return
    for j in range(7):
        stroke(ctx, [(-170, -220 + j * 50), (170 - (j * 41 % 90), -220 + j * 50)], 8, color=hexc("#b8b4a8"))
    if k == "bill":
        for j in range(4):
            shape(ctx, lambda c, j=j: p_ellipse(c, 100, 200 - j * 22, 70, 20), hexc("#f2c14e"), OUT * 0.7, None)
        return
    st = p.get("stamp", 0.0)
    if st > 0.01:
        ctx.save()
        ctx.translate(40, 150)
        s = 1.0 if st >= 1 else 1.6 - 0.6 * ease(st)
        ctx.scale(s, s)
        v = p.get("verdict", "tick")
        col = {"tick": C["green"], "cross": C["red"], "q": C["yel"]}[v]
        ctx.new_sub_path()
        ctx.arc(0, 0, 90, 0, 2 * math.pi)
        r, g, b = col
        ctx.set_source_rgba(r, g, b, min(1.0, st * 2))
        ctx.set_line_width(14)
        ctx.stroke()
        if v == "tick":
            stroke(ctx, [(-40, 0), (-10, 34), (46, -36)], 16, color=col)
        elif v == "cross":
            stroke(ctx, [(-36, -36), (36, 36)], 16, color=col)
            stroke(ctx, [(36, -36), (-36, 36)], 16, color=col)
        else:
            text(ctx, "?", 0, 4, 120, "#d8a020", 0)
        ctx.restore()


def cl_tick(ctx, t, p):
    """A big green tick, with p star (0..1) a big asterisk added beside it."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    s = back_out(min(1.0, on))
    ctx.save()
    ctx.scale(s, s)
    stroke(ctx, [(-120, 0), (-30, 100), (150, -130)], 64)
    stroke(ctx, [(-120, 0), (-30, 100), (150, -130)], 42, color=C["green"])
    st = p.get("star", 0.0)
    if st > 0.01:
        text(ctx, "*", 230, -100, int(260 * back_out(min(1.0, st))), "#ffd34d", 12)
    ctx.restore()


def cl_words(ctx, t, p):
    """The words ALWAYS LANDS ON ITS FEET with a big hand-drawn asterisk (p star 0..1)."""
    text(ctx, "ALWAYS LANDS", 0, -80, 130, "#ffffff", 10)
    text(ctx, "ON ITS FEET", -40, 70, 130, "#ffffff", 10)
    st = p.get("star", 0.0)
    if st > 0.01:
        text(ctx, "*", 420, -10, int(320 * back_out(min(1.0, st))), "#ffd34d", 14)


def cl_book(ctx, t, p):
    """THE MANUAL: a book held up (p upside 1: the title upside down)."""
    shape(ctx, lambda c: p_rrect(c, -170, -230, 340, 460, 14), hexc("#2f6f9f"), OUT, (0.05, 0.2))
    shape(ctx, lambda c: c.rectangle(-170, -230, 34, 460), hexc("#24557a"), OUT * 0.7, None)
    ctx.save()
    if p.get("upside", 1.0) > 0.5:
        ctx.rotate(math.pi)
    text(ctx, "THE", 10, -70, 70, "#ffd34d", 0)
    text(ctx, "MANUAL", 10, 10, 70, "#ffd34d", 0)
    _paw(ctx, 10, 120, 0.5, hexc("#ffd34d"))
    ctx.restore()


def cl_clipper(ctx, t, p):
    """A nail clipper (small) or p kind "tray": a steel surgical tray with plain instruments."""
    if p.get("kind") == "tray":
        shape(ctx, lambda c: p_rrect(c, -330, -60, 660, 60, 14), C["steel"], OUT, (0.05, 0.25))
        for k in range(4):
            stroke(ctx, [(-250 + k * 150, -80), (-140 + k * 150, -100)], 10, color=lighter(C["steel"], 0.4))
        return
    shape(ctx, lambda c: p_rrect(c, -120, -24, 240, 48, 20), C["steel"], OUT, (0.05, 0.2))
    stroke(ctx, [(-100, -24), (90, -70)], 14, color=darker(C["steel"], 0.8))


def cl_clinicdoor(ctx, t, p):
    """A vet clinic door with a cross sign, frosted glass; a cone hangs on a hook beside it (p cone)."""
    shape(ctx, lambda c: c.rectangle(-230, -760, 460, 760), hexc("#f6f0e2"), BG_OUT, None)
    shape(ctx, lambda c: c.rectangle(-200, -730, 400, 730), hexc("#5d8fa8"), BG_OUT, (0.04, 0.1))
    shape(ctx, lambda c: p_rrect(c, -150, -660, 300, 300, 14), (0.85, 0.93, 1.0), BG_OUT * 0.7, None, a=0.8)
    flat(ctx, lambda c: p_ellipse(c, 150, -360, 16, 16), C["yel"])
    shape(ctx, lambda c: p_rrect(c, -80, -560, 160, 160, 20), (1, 1, 1), OUT * 0.6, None)
    flat(ctx, lambda c: c.rectangle(-22, -540, 44, 120), C["green"])
    flat(ctx, lambda c: c.rectangle(-60, -502, 120, 44), C["green"])
    if p.get("cone"):
        ctx.save()
        ctx.translate(430, -420)
        ctx.scale(0.7, 0.7)
        cl_cone(ctx, t, {})
        ctx.restore()


def cl_window(ctx, t, p):
    """A window as an actor (origin = middle of its sill): p w, h, open (0..1), curtain (0..1 sway), barrier (0..1 a
    mesh barrier clicks into the opening), sky."""
    w, h = p.get("w", 420), p.get("h", 430)
    _window(ctx, -w / 2, -h, w, h, t, p.get("sky", "#9fd4f0"), p.get("open", 0.0), p.get("curtain", 0.0), p.get("barrier", 0.0))
    shape(ctx, lambda c: c.rectangle(-w / 2 - 80, 0, w + 160, 30), hexc("#f6f0e2"), BG_OUT, None)


def cl_cabinet(ctx, t, p):
    """The bathroom medicine cabinet (origin = top-left), door swinging open with p open (0..1); bottles inside, no
    pills shown."""
    cab_open = p.get("open", 0.0)
    cw, ch = 320, 360
    shape(ctx, lambda c: c.rectangle(0, 0, cw, ch), hexc("#f2efe6"), BG_OUT, (0.03, 0.1))
    if cab_open > 0.01:
        flat(ctx, lambda c: c.rectangle(14, 14, cw - 28, ch - 28), hexc("#e0dccf"))
        for k in range(1, 3):
            stroke(ctx, [(14, k * ch / 3), (cw - 14, k * ch / 3)], 8, color=hexc("#c8bfa8"))
        for k in range(3):
            shape(ctx, lambda c, k=k: p_rrect(c, 40 + k * 90, ch / 3 - 90, 60, 86, 10),
                  [hexc("#9fc3e8"), hexc("#f2c14e"), hexc("#e8a0a0")][k], OUT * 0.6, None)
    dw = cw * (1 - 0.85 * ease(min(1.0, cab_open)))
    shape(ctx, lambda c: c.rectangle(0, 0, dw, ch), hexc("#cfe3ea"), BG_OUT, (0.05, 0.1))
    flat(ctx, lambda c: c.rectangle(dw * 0.1, 30, dw * 0.8, ch - 60), (1, 1, 1), a=0.35)


def cl_tint(ctx, t, p):
    """A screen-wide grade (front actor): p mode "grey" (drains colour by p a), "dark" (lights down by p a)."""
    a = p.get("a", 0.0)
    if a <= 0.01:
        return
    ctx.identity_matrix()
    if p.get("mode", "dark") == "grey":
        ctx.set_operator(cairo.OPERATOR_HSL_SATURATION)
        ctx.set_source_rgba(0.5, 0.5, 0.5, min(1.0, a))
        ctx.paint()
        ctx.set_operator(cairo.OPERATOR_OVER)
    else:
        ctx.rectangle(0, 0, 1920, 1080)
        ctx.set_source_rgba(0.02, 0.03, 0.08, min(0.95, a))
        ctx.fill()


def cl_phone(ctx, t, p):
    """A phone held up mid-call: a plain handset icon on the screen and call rings (no text)."""
    shape(ctx, lambda c: p_rrect(c, -80, -150, 160, 300, 24), hexc("#2a2638"), OUT, (0.05, 0.2))
    flat(ctx, lambda c: p_rrect(c, -64, -126, 128, 240, 12), hexc("#3fb950"))
    stroke(ctx, [(-30, -10), (-20, 30), (20, 40)], 22, smooth=True, color=(1, 1, 1))
    for k in range(2):
        u = (t * 1.2 + k * 0.5) % 1
        ctx.new_sub_path()
        ctx.arc(0, 0, 70 + 70 * u, -0.9, -0.2)
        ctx.set_source_rgba(1, 1, 1, 0.8 * (1 - u))
        ctx.set_line_width(7)
        ctx.stroke()


def cl_rug(ctx, t, p):
    shape(ctx, lambda c: p_ellipse(c, 0, 0, p.get("w", 380), 44), hexc("#a5514a"), OUT, None)


ACTORS = {"cl_cat": cl_cat, "cl_dog": cl_dog, "cl_mouse": cl_mouse, "cl_jar": cl_jar, "cl_parch": cl_parch, "cl_map": cl_map,
          "cl_cal": cl_cal, "cl_count": cl_count, "cl_timeline": cl_timeline, "cl_puzzle": cl_puzzle,
          "cl_hearing": cl_hearing, "cl_factory": cl_factory, "cl_can": cl_can, "cl_heartline": cl_heartline,
          "cl_heart": cl_heart, "cl_saucer": cl_saucer, "cl_bowl": cl_bowl, "cl_lily": cl_lily, "cl_petal": cl_petal,
          "cl_qm": cl_qm, "cl_clock": cl_clock, "cl_bottle": cl_bottle, "cl_gut": cl_gut, "cl_string": cl_string,
          "cl_carrier": cl_carrier, "cl_cone": cl_cone, "cl_scale": cl_scale, "cl_bill": cl_bill, "cl_petmap": cl_petmap,
          "cl_bars": cl_bars, "cl_bubbles": cl_bubbles, "cl_wave": cl_wave, "cl_listener": cl_listener, "cl_baby": cl_baby,
          "cl_lightbox": cl_lightbox, "cl_clip": cl_clip, "cl_litter": cl_litter, "cl_hairball": cl_hairball,
          "cl_mirror": cl_mirror, "cl_row": cl_row, "cl_kitout": cl_kitout, "cl_cake": cl_cake, "cl_box": cl_box,
          "cl_station": cl_station, "cl_toy": cl_toy, "cl_eyes": cl_eyes, "cl_chair": cl_chair, "cl_dropper": cl_dropper,
          "cl_eye": cl_eye, "cl_desk": cl_desk, "cl_mop": cl_mop, "cl_paper": cl_paper, "cl_tick": cl_tick,
          "cl_words": cl_words, "cl_book": cl_book, "cl_clipper": cl_clipper, "cl_clinicdoor": cl_clinicdoor,
          "cl_fence": cl_fence, "cl_rug": cl_rug, "cl_window": cl_window, "cl_cabinet": cl_cabinet, "cl_tint": cl_tint, "cl_phone": cl_phone}
SCENES = {"cl_blanket": cl_blanket, "cl_room": cl_room, "cl_village": cl_village, "cl_street": cl_street, "cl_lot": cl_lot,
          "cl_shelter": cl_shelter}
