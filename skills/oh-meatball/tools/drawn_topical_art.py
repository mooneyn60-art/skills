"""Props and scenes for the topical news TikToks (first used by scripts/drawn-house/tt-gta6-confirmed.json, 11/13;
meant to be reused by the next topical cuts), in the locked drawn_kit look (flat fills, one cel shade, thick ink
outlines). Same conventions as tools/drawn_jensen_art.py: an actor draws at its origin in local units (feet at y = 0,
y up is negative), scaled by its "s"; a scene draws in world units (the default camera [540, 960, 1] shows
x 0..1080, y 0..1920; floors sit at y = 1500).

Everything is generic and our own drawing: no logos, no brand shapes, no real console designs, no game art. The
only words these pictures can draw are the ones a spec passes in (p text / label / stamp), so a spec keeps every
on-screen word under its own control.

Actors:  tp_calendar (wall calendar: p circle 0..1 rings p cell, p cross 0..1 a red X, p head text, p col),
         tp_strip (a row of day cells: p n cells, p span 0..1 highlight, p mark index ringed),
         tp_tag (a price tag on a string: p text, p col, p swing), tp_console (a plain box console: p glow, p col),
         tp_pad (a plain gamepad), tp_bar (a download panel: p v 0..1 fill, spinner), tp_router (a router: p smoke
         0..1, p slip 0..1 a paper slides out), tp_box (a game case: p open 0..1, p slip 0..1 a paper floats out,
         p air 0..1 puffs), tp_pc (a PC tower: p shade 0..1 a lampshade drops on, p lamp 0..1 glow),
         tp_ballot (a ballot box: p drop 0..1 ballots fall in, loops), tp_bubble (a speech bubble: p label,
         p on 0..1, p tail -1 | 1, p col), tp_picket (a small picket sign, blank board), tp_couch (a sofa: p sign
         0..1 with p text), tp_stateline (a roadside border sign: p photo 0..1, p stamp 0..1 with p text),
         tp_blanket (a patchwork blanket draped over someone, origin = their feet; p w, p h), tp_note (a note
         taped up, scribbles only; p on 0..1)
Scenes:  tp_living (Meatball's living room, as jh_living, p sofa false = no sofa), tp_set (a plain studio
         backdrop: p wall, p wall2, p floor colours), tp_neon (our own neon city at sunset with palm trees over
         water, then a desert road running right to x 2600)
"""
import math
import random

from drawn_kit import (BG_OUT, INK, OUT, back_out, darker, ease, flat, hexc, lighter, p_ellipse, p_poly, p_rrect,
                       p_smooth, shape, starburst, stroke)
from drawn_ds_art import text
from drawn_jensen_art import C as JC, glow

C = dict(JC)
C.update({k: hexc(v) for k, v in {
    "cal": "#fbf6e6", "cal_dk": "#e2dac0", "cal_head": "#d8322a", "ring": "#9aa3ab", "pen": "#e5383b",
    "tag": "#f6d27a", "tag_dk": "#d9ae4a", "con": "#3c4656", "con_lt": "#5b677a", "led": "#5ee0ff",
    "pad": "#2f3644", "pad_lt": "#4a5466", "panel": "#16203a", "track": "#2b3656", "fill": "#3fb950",
    "router": "#e8eef4", "box": "#2a5fa8", "box_dk": "#1f4a85", "case": "#e8eef4", "pc": "#2b2f38",
    "rgb1": "#ff4fd8", "rgb2": "#5ee0ff", "shade": "#f2e2b0", "ballot": "#2c5aa0", "bub": "#ffffff",
    "pick": "#f4ecd6", "stick": "#b07a45", "sign": "#2e7d4f", "post": "#8d969c", "stamp": "#d8322a",
    "q1": "#e5383b", "q2": "#3b7dd8", "q3": "#f2c14e", "q4": "#3fb950",
}.items()})


def _rng(seed):
    return random.Random(seed)


# ================================================================================================ calendar, strip

def tp_calendar(ctx, t, p):
    """A wall calendar centred at its origin (380 x 440 local) on a nail: red header band (p head text, optional),
    two rings, a 5 x 7 grid of blank day cells. p circle 0..1 draws a red ring round cell p cell (0..34) as if by
    marker; p cross 0..1 strokes a red X over the whole page; p col header colour."""
    ctx.save()
    ctx.rotate(math.radians(p.get("tilt", 0)))
    stroke(ctx, [(0, -250), (-60, -205)], 4, color=C["ring"])
    stroke(ctx, [(0, -250), (60, -205)], 4, color=C["ring"])
    flat(ctx, lambda c: p_ellipse(c, 0, -252, 9, 9), INK)
    shape(ctx, lambda c: c.rectangle(-190, -205, 380, 425), C["cal"], OUT, (0.02, 0.04))
    head = hexc(p.get("col", "#d8322a"))
    shape(ctx, lambda c: c.rectangle(-190, -205, 380, 95), head, OUT, None)
    if p.get("head"):
        text(ctx, p["head"], 0, -158, 60, "#ffffff", 0)
    for x in (-90, 90):
        shape(ctx, lambda c, x=x: p_rrect(c, x - 10, -225, 20, 44, 10), C["ring"], OUT * 0.6, None)
    x0, y0, cw, ch = -170, -95, 340 / 7, 300 / 5
    for r in range(6):
        stroke(ctx, [(x0, y0 + r * ch), (x0 + 340, y0 + r * ch)], 3, color=C["cal_dk"])
    for k in range(8):
        stroke(ctx, [(x0 + k * cw, y0), (x0 + k * cw, y0 + 300)], 3, color=C["cal_dk"])
    for k in range(35):   # tiny blank day marks (no numbers)
        cx, cy = x0 + (k % 7) * cw + 12, y0 + (k // 7) * ch + 12
        flat(ctx, lambda c, cx=cx, cy=cy: c.rectangle(cx, cy - 3, 14, 6), C["line"])
    u = p.get("circle", 0.0)
    if u > 0.01:
        k = int(p.get("cell", 18))
        cx, cy = x0 + (k % 7 + 0.5) * cw, y0 + (k // 7 + 0.5) * ch
        ctx.save()
        ctx.new_path()
        ctx.arc(cx, cy, 44, -2.2, -2.2 + 2 * math.pi * 1.08 * min(1.0, u))
        ctx.set_source_rgb(*C["pen"])
        ctx.set_line_width(11)
        ctx.set_line_cap(1)
        ctx.stroke()
        ctx.restore()
        if u >= 1.0:
            flat(ctx, lambda c: p_ellipse(c, cx, cy, 30, 30), C["pen"], a=0.25 + 0.15 * math.sin(t * 6))
    xu = p.get("cross", 0.0)
    if xu > 0.01:
        a = min(1.0, xu * 2)
        b = max(0.0, min(1.0, xu * 2 - 1))
        stroke(ctx, [(-170, -190), (-170 + 340 * a, -190 + 400 * a)], 22, color=C["pen"])
        if b > 0:
            stroke(ctx, [(170, -190), (170 - 340 * b, -190 + 400 * b)], 22, color=C["pen"])
    ctx.restore()


def tp_strip(ctx, t, p):
    """A horizontal row of p n blank day cells centred at its origin (each 64 x 90); p span 0..1 fills the cells
    left to right with a pale band; p mark (index) gets a red ring that pulses, p markon 0..1."""
    n = int(p.get("n", 15))
    w = 64
    x0 = -n * w / 2
    shape(ctx, lambda c: p_rrect(c, x0 - 16, -70, n * w + 32, 140, 18), C["cal"], OUT, None)
    sp = p.get("span", 0.0)
    if sp > 0.01:
        flat(ctx, lambda c: c.rectangle(x0, -45, n * w * min(1.0, sp), 90), hexc("#ffd34d"), a=0.55)
    for k in range(n + 1):
        stroke(ctx, [(x0 + k * w, -45), (x0 + k * w, 45)], 3, color=C["cal_dk"])
    stroke(ctx, [(x0, -45), (x0 + n * w, -45)], 3, color=C["cal_dk"])
    stroke(ctx, [(x0, 45), (x0 + n * w, 45)], 3, color=C["cal_dk"])
    for k in range(n):
        flat(ctx, lambda c, k=k: c.rectangle(x0 + k * w + 18, -12, 28, 8), C["line"])
    m = p.get("markon", 0.0)
    if m > 0.01 and p.get("mark") is not None:
        cx = x0 + (int(p["mark"]) + 0.5) * w
        r = 46 * back_out(min(1.0, m)) * (1 + 0.04 * math.sin(t * 5))
        ctx.save()
        ctx.new_path()
        ctx.arc(cx, 0, r, 0, 2 * math.pi)
        ctx.set_source_rgb(*C["pen"])
        ctx.set_line_width(10)
        ctx.stroke()
        ctx.restore()


# ================================================================================================ price tag

def tp_tag(ctx, t, p):
    """A price tag hanging on a string from its origin (the string's top); p text on it (a spec word, e.g. "$"),
    p col, p swing degrees (it sways), p len string length."""
    ln = p.get("len", 180)
    ang = math.radians(p.get("swing", 6) * math.sin(t * 2.2 + p.get("ph", 0)))
    ctx.save()
    ctx.rotate(ang)
    stroke(ctx, [(0, 0), (0, ln)], 5, color=INK)
    col = hexc(p.get("col", "#f6d27a"))
    shape(ctx, lambda c: p_poly(c, [(0, ln), (110, ln + 70), (110, ln + 330), (-110, ln + 330), (-110, ln + 70)]),
          col, OUT, (0.03, 0.06))
    shape(ctx, lambda c: p_ellipse(c, 0, ln + 60, 16, 16), C["cal"], OUT * 0.6, None)
    if p.get("text"):
        text(ctx, p["text"], 0, ln + 200, p.get("px", 120), p.get("tcol", "#1b1b1b"), 0)
    ctx.restore()


# ================================================================================================ console, pad

def tp_console(ctx, t, p):
    """A plain generic box console (feet y 0, 420 wide, 170 tall): a low flat box, horizontal grooves, one round
    power light; p glow 0..1 a soft light round it, p col body colour. Deliberately like no real console."""
    g = p.get("glow", 0.0)
    col = hexc(p.get("col", "#3c4656"))
    if g > 0.01:
        glow(ctx, 0, -90, 330, hexc(p.get("gcol", "#5ee0ff")), 0.45 * g * (0.85 + 0.15 * math.sin(t * 4)))
    shape(ctx, lambda c: p_rrect(c, -210, -170, 420, 160, 26), col, OUT, (0.03, 0.12), (0.2, 0.25, 0.25))
    for k in range(3):
        stroke(ctx, [(-170, -130 + k * 30), (110, -130 + k * 30)], 5, color=darker(col, 0.7))
    flat(ctx, lambda c: p_rrect(c, -190, -14, 380, 14, 6), darker(col, 0.6))
    led = hexc(p.get("gcol", "#5ee0ff")) if g > 0.01 else hexc("#6f7882")
    shape(ctx, lambda c: p_ellipse(c, 160, -100, 18, 18), led, OUT * 0.5, None)


def tp_pad(ctx, t, p):
    """A plain generic gamepad centred at its origin (360 x 220): rounded body with two grips, a plus pad, four
    same-colour round buttons (no symbols, no letters), two sticks. p col body colour."""
    col = hexc(p.get("col", "#2f3644"))

    def body(c):
        p_smooth(c, [(-180, -40), (-120, -95), (0, -80), (120, -95), (180, -40), (170, 90), (110, 120), (60, 40),
                     (-60, 40), (-110, 120), (-170, 90)])
    shape(ctx, body, col, OUT, (0.03, 0.1), (0.25, 0.2, 0.2))
    lt = lighter(col, 0.3)
    flat(ctx, lambda c: c.rectangle(-128, -48, 56, 18), lt)
    flat(ctx, lambda c: c.rectangle(-109, -67, 18, 56), lt)
    for dx, dy in ((100, -60), (128, -38), (72, -38), (100, -16)):
        shape(ctx, lambda c, dx=dx, dy=dy: p_ellipse(c, dx, dy, 13, 13), lt, OUT * 0.4, None)
    for dx in (-48, 48):
        shape(ctx, lambda c, dx=dx: p_ellipse(c, dx, 10, 24, 24), darker(col, 0.6), OUT * 0.5, None)


# ================================================================================================ download, router

def tp_bar(ctx, t, p):
    """A download panel centred at its origin (640 x 260): a down-arrow icon, a track filled to p v 0..1 (with a
    shimmer), three spinner dots that keep going. No numbers."""
    shape(ctx, lambda c: p_rrect(c, -320, -130, 640, 260, 30), C["panel"], OUT, None)
    shape(ctx, lambda c: p_poly(c, [(-262, -70), (-218, -70), (-218, -20), (-190, -20), (-240, 35), (-290, -20),
                                    (-262, -20)]), C["fill"], OUT * 0.5, None)
    shape(ctx, lambda c: p_rrect(c, -160, -30, 430, 60, 30), C["track"], OUT * 0.6, None)
    v = max(0.0, min(1.0, p.get("v", 0.0)))
    if v > 0.0:
        w = max(30, 430 * v)
        flat(ctx, lambda c: p_rrect(c, -160, -30, w, 60, 30), C["fill"])
    for k in range(3):
        a = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(t * 6 - k * 0.9))
        flat(ctx, lambda c, k=k: p_ellipse(c, 30 + k * 50, 82, 12, 12), (1, 1, 1), a=a)


def tp_router(ctx, t, p):
    """A home router (feet y 0, 300 wide): white box, two antennas, blinking lights; p smoke 0..1 grey puffs
    rise and the lights go red; p slip 0..1 a paper slip slides out of the front (blank lines)."""
    sm = p.get("smoke", 0.0)
    sl = p.get("slip", 0.0)
    if sl > 0.01:
        u = ease(min(1.0, sl))
        ctx.save()
        ctx.translate(40 + 120 * u, -60 - 40 * u)
        ctx.rotate(0.15 * u)
        shape(ctx, lambda c: c.rectangle(-60, -80, 120, 160), C["paper"], OUT * 0.6, None)
        for k in range(5):
            flat(ctx, lambda c, k=k: c.rectangle(-42, -56 + k * 24, 84 if k % 2 else 60, 8), C["line"])
        flat(ctx, lambda c: c.rectangle(-42, 52, 50, 8), C["pen"])
        ctx.restore()
    for sx, rot in ((-100, -0.25), (100, 0.25)):
        ctx.save()
        ctx.translate(sx, -110)
        ctx.rotate(rot + (0.1 * math.sin(t * 30) * sm))
        shape(ctx, lambda c: p_rrect(c, -10, -170, 20, 175, 10), hexc("#3a3f48"), OUT * 0.6, None)
        ctx.restore()
    shape(ctx, lambda c: p_rrect(c, -150, -120, 300, 120, 22), C["router"], OUT, (0.03, 0.12))
    for k in range(5):
        on = (math.sin(t * 7 + k * 1.7) > 0) or sm > 0.3
        col = C["pen"] if sm > 0.3 else hexc("#3fb950")
        flat(ctx, lambda c, k=k: p_ellipse(c, -100 + k * 40, -60, 9, 9), col if on else hexc("#9aa3ab"))
    if sm > 0.01:
        for k in range(5):
            u = (t * 0.7 + k / 5) % 1.0
            x = -60 + k * 30 + 40 * math.sin(u * 5 + k)
            y = -130 - 380 * u
            r = 40 + 70 * u
            shape(ctx, lambda c, x=x, y=y, r=r: p_ellipse(c, x, y, r, r * 0.85), hexc("#8d929a"), OUT * 0.4, None,
                  a=min(1.0, sm) * (1 - u) * 0.9)


# ================================================================================================ game box, PC

def tp_box(ctx, t, p):
    """A game case standing on its spine (feet y 0, 300 wide, 400 tall), plain blue cover with a white band and a
    star (no logo, no art); p open 0..1 swings the lid open; p slip 0..1 a small paper slip floats up out of it;
    p air 0..1 a few empty puffs drift out."""
    op = ease(min(1.0, p.get("open", 0.0)))
    shape(ctx, lambda c: p_rrect(c, -150, -400, 300, 400, 14), C["case"], OUT, (0.03, 0.08))
    if op > 0.02:
        flat(ctx, lambda c: p_rrect(c, -132, -382, 264, 364, 8), hexc("#c9d2dc"))
        flat(ctx, lambda c: p_ellipse(c, 0, -200, 110, 110), hexc("#b7c1cc"))   # the empty disc holder
        flat(ctx, lambda c: p_ellipse(c, 0, -200, 26, 26), hexc("#9aa3ab"))
    sl = p.get("slip", 0.0)
    if sl > 0.01:
        u = min(1.0, sl)
        y = -230 - 400 * ease(u)
        x = 30 * math.sin(t * 2.5)
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(0.25 * math.sin(t * 2))
        shape(ctx, lambda c: c.rectangle(-70, -40, 140, 80), C["paper"], OUT * 0.6, None)
        for k in range(3):
            flat(ctx, lambda c, k=k: c.rectangle(-50, -22 + k * 20, 100 if k != 1 else 70, 8), C["line"])
        ctx.restore()
    air = p.get("air", 0.0)
    if air > 0.01:
        for k in range(4):
            u = (t * 0.5 + k / 4) % 1.0
            x = -90 + k * 60 + 30 * math.sin(u * 6)
            stroke(ctx, [(x - 30, -250 - 300 * u), (x, -270 - 300 * u), (x + 30, -250 - 300 * u)], 6, smooth=True,
                   color=hexc("#c9e9ff"), a=min(1.0, air) * (1 - u))
    # the lid (front cover), hinged on the left edge
    sx = 1 - 2 * op   # 1 closed, -1 fully open
    ctx.save()
    ctx.translate(-150, 0)
    ctx.scale(sx if abs(sx) > 0.04 else 0.04, 1)
    shape(ctx, lambda c: p_rrect(c, 0, -400, 300, 400, 14), C["box"] if sx > 0 else C["box_dk"], OUT, (0.03, 0.08))
    if sx > 0:
        flat(ctx, lambda c: c.rectangle(12, -360, 276, 50), (1, 1, 1))
        starburst(ctx, 150, -170, 70, 5, C["yellow"], OUT * 0.6)
    ctx.restore()


def tp_pc(ctx, t, p):
    """A PC tower (feet y 0, 220 wide, 460 tall) with a side window and colour-cycling fans; p shade 0..1 a fabric
    lampshade drops onto its top; p lamp 0..1 a warm glow under the shade."""
    lamp = p.get("lamp", 0.0)
    if lamp > 0.01:
        glow(ctx, 0, -520, 420, C["light"], 0.5 * lamp)
    shape(ctx, lambda c: p_rrect(c, -110, -460, 220, 460, 16), C["pc"], OUT, (0.03, 0.08))
    flat(ctx, lambda c: p_rrect(c, -85, -420, 140, 360, 10), hexc("#141820"))
    h = (t * 0.6) % 1.0
    cols = [hexc("#ff4fd8"), hexc("#5ee0ff"), hexc("#3fb950"), hexc("#ffd34d")]
    for k, fy in enumerate((-340, -200)):
        col = cols[int(h * 4 + k) % 4]
        shape(ctx, lambda c, fy=fy: p_ellipse(c, -15, fy, 55, 55), darker(col, 0.5), OUT * 0.5, None)
        ctx.save()
        ctx.translate(-15, fy)
        ctx.rotate(t * 8)
        for j in range(3):
            ctx.rotate(2 * math.pi / 3)
            flat(ctx, lambda c: p_ellipse(c, 24, 0, 22, 10), col)
        ctx.restore()
    flat(ctx, lambda c: p_ellipse(c, 85, -430, 9, 9), hexc("#5ee0ff"))
    sh = p.get("shade", 0.0)
    if sh > 0.01:
        u = back_out(min(1.0, sh))
        y = -460 - 500 * (1 - u)
        stroke(ctx, [(0, y), (0, y - 60)], 10, color=hexc("#8a6a3a"))
        shape(ctx, lambda c: p_poly(c, [(-170, y - 40), (170, y - 40), (100, y - 260), (-100, y - 260)]),
              C["shade"], OUT, (0.03, 0.1))
        for k in range(5):
            x = -120 + k * 60
            stroke(ctx, [(x, y - 48), (x * 0.6, y - 252)], 3, color=darker(C["shade"], 0.85))


# ================================================================================================ vote, bubbles

def tp_ballot(ctx, t, p):
    """A ballot box (feet y 0, 360 wide, 380 tall) with a slot and a check-mark badge; p drop 0..1 folded ballots
    keep falling into the slot (loops while on)."""
    d = p.get("drop", 0.0)
    if d > 0.01:
        for k in range(3):
            u = (t * 0.55 + k / 3) % 1.0
            y = -700 + 300 * ease(u)
            ctx.save()
            ctx.translate(10 * math.sin(k * 2), y)
            ctx.rotate(0.1 * math.sin(t * 3 + k))
            shape(ctx, lambda c: c.rectangle(-50, -30, 100, 60), C["paper"], OUT * 0.6, None, a=min(1.0, d))
            stroke(ctx, [(-30, 0), (-10, 18), (30, -18)], 7, color=C["green"], a=min(1.0, d))
            ctx.restore()
    shape(ctx, lambda c: p_rrect(c, -180, -380, 360, 380, 18), C["ballot"], OUT, (0.03, 0.08))
    shape(ctx, lambda c: c.rectangle(-200, -400, 400, 50), darker(C["ballot"], 0.8), OUT, None)
    flat(ctx, lambda c: p_rrect(c, -80, -385, 160, 16, 8), INK)
    shape(ctx, lambda c: p_ellipse(c, 0, -190, 90, 90), (1, 1, 1), OUT * 0.8, None)
    stroke(ctx, [(-45, -190), (-12, -150), (50, -235)], 22, color=C["green"])


def tp_bubble(ctx, t, p):
    """A speech bubble centred at its origin (p w x p h, default 420 x 230) with a tail on side p tail (-1 left,
    1 right) at the bottom, p label text inside (a spec word, e.g. "UNION SAYS"), three blank lines under it;
    p on 0..1 pops it in; p col fill, p tcol label colour."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    w, h = p.get("w", 420), p.get("h", 230)
    sc = back_out(min(1.0, on))
    ctx.save()
    ctx.scale(sc, sc)
    tl = p.get("tail", 1)
    col = hexc(p.get("col", "#ffffff"))

    def path(c):
        p_rrect(c, -w / 2, -h / 2, w, h, 50)
    shape(ctx, path, col, OUT, None)
    tx = tl * w * 0.22
    shape(ctx, lambda c: p_poly(c, [(tx - 40, h / 2 - 8), (tx + 40, h / 2 - 8), (tx + tl * 90, h / 2 + 90)]), col,
          OUT, None)
    flat(ctx, lambda c: c.rectangle(tx - 34, h / 2 - 20, 68, 18), col)
    if p.get("label"):
        text(ctx, p["label"], 0, -h / 2 + 62, p.get("px", 56), p.get("tcol", "#1b1b1b"), 0)
    for k in range(3):
        y = -h / 2 + 120 + k * 32
        if y > h / 2 - 20:
            break
        flat(ctx, lambda c, y=y, k=k: c.rectangle(-w / 2 + 50, y, (w - 100) * (1 if k < 2 else 0.6), 12), C["line"])
    ctx.restore()


def tp_picket(ctx, t, p):
    """A small picket sign held at its origin (the bottom of the stick): a blank board with a few scribble marks
    (no words); p wave 0..1 it wags."""
    ctx.save()
    ctx.rotate(math.radians(8 * p.get("wave", 0.0) * math.sin(t * 7)))
    shape(ctx, lambda c: p_rrect(c, -12, -330, 24, 330, 8), C["stick"], OUT * 0.7, None)
    shape(ctx, lambda c: p_rrect(c, -150, -470, 300, 190, 10), C["pick"], OUT, (0.03, 0.08))
    stroke(ctx, [(-110, -420), (-60, -410), (-10, -425), (40, -405), (100, -420)], 9, smooth=True, color=C["pen"])
    stroke(ctx, [(-100, -360), (-30, -350), (30, -365), (90, -350)], 9, smooth=True, color=C["crayon2"])
    ctx.restore()


# ================================================================================================ couch, sign, blanket

def tp_couch(ctx, t, p):
    """An orange sofa (feet y 0, 620 wide, 330 tall; the seat top at y -170); p sign 0..1 a cardboard sign on a
    stick pops up from the right arm, with p text (a spec word)."""
    shape(ctx, lambda c: p_rrect(c, -280, -330, 560, 230, 40), C["sofa"], OUT, (0.03, 0.1))
    shape(ctx, lambda c: p_rrect(c, -310, -180, 620, 170, 40), C["sofa"], OUT, (0.03, 0.15))
    for x0 in (-310, 230):
        shape(ctx, lambda c, x0=x0: p_rrect(c, x0, -230, 80, 230, 30), C["sofa_dk"], OUT, None)
    for x in (-250, 250):
        flat(ctx, lambda c, x=x: c.rectangle(x - 14, -12, 28, 12), INK)
    sg = p.get("sign", 0.0)
    if sg > 0.01:
        u = back_out(min(1.0, sg))
        ctx.save()
        ctx.translate(250, -230)
        ctx.scale(u, u)
        ctx.rotate(0.08 + 0.04 * math.sin(t * 3))
        stroke(ctx, [(0, 0), (0, -200)], 12, color=C["stick"])
        shape(ctx, lambda c: p_rrect(c, -130, -360, 260, 180, 8), hexc("#d8a960"), OUT, (0.03, 0.08))
        if p.get("text"):
            text(ctx, p["text"], 0, -270, p.get("px", 110), p.get("tcol", "#d8322a"), 0)
        ctx.restore()


def tp_stateline(ctx, t, p):
    """A roadside border sign on two posts (feet y 0, board 640 x 380 at y -820..-440): a green board with a sun
    and a palm silhouette (no words); p photo 0..1 a snapshot of Meatball gets pinned to the board; p stamp 0..1 a
    red stamp with p text (a spec word, e.g. "BANNED") slams across the photo."""
    for x in (-220, 220):
        shape(ctx, lambda c, x=x: c.rectangle(x - 16, -460, 32, 460), C["post"], OUT * 0.8, None)
    shape(ctx, lambda c: p_rrect(c, -320, -820, 640, 380, 24), C["sign"], OUT, (0.02, 0.06))
    ctx.save()
    p_rrect(ctx, -300, -800, 600, 340, 18)
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(8)
    ctx.stroke()
    ctx.restore()
    shape(ctx, lambda c: p_ellipse(c, -170, -660, 70, 70), hexc("#ffd84a"), OUT * 0.6, None)
    stroke(ctx, [(-120, -500), (-110, -580), (-90, -640)], 14, smooth=True, color=hexc("#123d2a"))
    for a in (-2.6, -1.9, -1.2, -0.5):
        stroke(ctx, [(-90, -640), (-90 + 70 * math.cos(a), -640 + 50 * math.sin(a) + 20)], 12, smooth=True,
               color=hexc("#123d2a"))
    ph = p.get("photo", 0.0)
    if ph > 0.01:
        u = back_out(min(1.0, ph))
        ctx.save()
        ctx.translate(130, -630)
        ctx.scale(u, u)
        ctx.rotate(-0.08)
        shape(ctx, lambda c: c.rectangle(-110, -130, 220, 250), (1, 1, 1), OUT * 0.8, None)
        flat(ctx, lambda c: c.rectangle(-90, -110, 180, 170), hexc("#8fd3f4"))
        # a tiny Meatball: brown ball, two eyes, a grin
        shape(ctx, lambda c: p_ellipse(c, 0, -20, 62, 62), hexc("#8a4b2a"), OUT * 0.6, (0.06, 0.1))
        for ex in (-20, 20):
            shape(ctx, lambda c, ex=ex: p_ellipse(c, ex, -32, 13, 15), (1, 1, 1), OUT * 0.35, None)
            flat(ctx, lambda c, ex=ex: p_ellipse(c, ex + 3, -30, 6, 7), INK)
        stroke(ctx, [(-22, 4), (0, 16), (22, 4)], 6, smooth=True)
        flat(ctx, lambda c: p_ellipse(c, 0, -150, 12, 12), C["pen"])   # the pin
        ctx.restore()
    st = p.get("stamp", 0.0)
    if st > 0.01 and p.get("text"):
        u = min(1.0, st)
        s = 1.0 + 0.7 * (1 - back_out(min(1.0, u * 2.5)))
        ctx.save()
        ctx.translate(130, -620)
        ctx.rotate(math.radians(-14))
        ctx.scale(s, s)
        p_rrect(ctx, -170, -60, 340, 120, 14)
        col = hexc(p.get("col", "#d8322a"))
        ctx.set_source_rgba(col[0], col[1], col[2], 0.95)
        ctx.set_line_width(12)
        ctx.stroke()
        text(ctx, p["text"], 0, 0, p.get("px", 84), p.get("col", "#d8322a"), 0)
        ctx.restore()


def tp_blanket(ctx, t, p):
    """A patchwork blanket draped from the shoulders down, origin = the wearer's feet; p h height (default 330),
    p w width (default 300). Put it in front of the wearer."""
    w, h = p.get("w", 300), p.get("h", 330)
    wob = 6 * math.sin(t * 3)

    def path(c):
        p_smooth(c, [(-w * 0.32, -h), (0, -h - 20), (w * 0.32, -h), (w * 0.5 + wob, -h * 0.3), (w * 0.52, -6),
                     (0, 6), (-w * 0.52, -6), (-w * 0.5 - wob, -h * 0.3)])
    shape(ctx, path, C["q2"], OUT, (0.03, 0.08))
    ctx.save()
    path(ctx)
    ctx.clip()
    cols = [C["q1"], C["q3"], C["q4"], C["q2"]]
    for i in range(-4, 5):
        for j in range(0, 8):
            if (i + j) % 2:
                flat(ctx, lambda c, i=i, j=j: c.rectangle(i * 70 - 35, -h + j * 70 - 30, 70, 70), cols[(i * 3 + j) % 4],
                     a=0.9)
    ctx.restore()
    ctx.save()
    path(ctx)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT)
    ctx.stroke()
    ctx.restore()


def tp_note(ctx, t, p):
    """A note taped up, centred at its origin (220 x 280): blank scribble lines, a red double underline, two tape
    strips; p on 0..1 slaps it on."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    s = 1.0 + 0.5 * (1 - back_out(min(1.0, on * 2)))
    ctx.save()
    ctx.scale(s, s)
    ctx.rotate(math.radians(p.get("tilt", 5)))
    shape(ctx, lambda c: c.rectangle(-110, -140, 220, 280), C["paper"], OUT * 0.7, (0.02, 0.05))
    for k in range(6):
        stroke(ctx, [(-80, -95 + k * 34), (-20, -100 + k * 34), (40, -92 + k * 34), (80 - 30 * (k % 2), -97 + k * 34)],
               6, smooth=True, color=hexc("#4a4a4a"))
    stroke(ctx, [(-80, 110), (80, 104)], 8, color=C["pen"])
    stroke(ctx, [(-80, 124), (80, 118)], 8, color=C["pen"])
    for x in (-80, 80):
        flat(ctx, lambda c, x=x: c.rectangle(x - 34, -158, 68, 30), hexc("#f2e8b0"), a=0.85)
    ctx.restore()


# ================================================================================================ scenes

def tp_living(ctx, t, layer, p):
    """Meatball's living room, as jh_living (warm striped wall, window at x 560..980, y 520..940, a picture at
    x 80..340, a lamp at x -40), floor y 1500; p sofa (default True) draws the orange sofa at x 570..1190;
    p picture False hides the picture (to hang a calendar there)."""
    layer(0.9)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), C["lwall"])
    for x in range(-3000, 5000, 180):
        flat(ctx, lambda c, x=x: c.rectangle(x, -3000, 70, 4600), C["lwall2"])
    shape(ctx, lambda c: c.rectangle(560, 520, 420, 420), hexc("#f6efe0"), BG_OUT, None)
    flat(ctx, lambda c: c.rectangle(585, 545, 370, 370), hexc("#8fd3f4"))
    flat(ctx, lambda c: p_ellipse(c, 700, 640, 40, 40), hexc("#ffd84a"))
    stroke(ctx, [(770, 545), (770, 915)], BG_OUT * 1.6, color=hexc("#f6efe0"))
    stroke(ctx, [(585, 730), (955, 730)], BG_OUT * 1.6, color=hexc("#f6efe0"))
    if p.get("picture", True):
        shape(ctx, lambda c: c.rectangle(80, 600, 260, 200), hexc("#3a6a8a"), BG_OUT, None)
        shape(ctx, lambda c: p_poly(c, [(110, 780), (190, 680), (240, 740), (280, 700), (320, 780)]), C["green"],
              BG_OUT * 0.6, None)
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 3000), C["floor"])
    for y in (1560, 1650, 1780):
        stroke(ctx, [(-3000, y), (5000, y)], 4, color=C["floor_dk"])
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)
    if p.get("sofa", True):
        shape(ctx, lambda c: p_rrect(c, 600, 1150, 560, 230, 40), C["sofa"], BG_OUT, (0.03, 0.1))
        shape(ctx, lambda c: p_rrect(c, 570, 1300, 620, 170, 40), C["sofa"], BG_OUT, (0.03, 0.15))
        for x0 in (570, 1130):
            shape(ctx, lambda c, x0=x0: p_rrect(c, x0, 1250, 80, 230, 30), C["sofa_dk"], BG_OUT, None)
    stroke(ctx, [(-40, 1500), (-40, 1020)], 12)
    shape(ctx, lambda c: p_poly(c, [(-130, 1020), (50, 1020), (10, 900), (-90, 900)]), hexc("#f2c14e"), BG_OUT, None)
    glow(ctx, -40, 1000, 260, hexc("#fff3b0"), 0.35)


def tp_set(ctx, t, layer, p):
    """A plain studio backdrop: p wall colour with soft diagonal bands of p wall2, a big rounded back panel, a
    floor of p floor colour at y 1500 with a lit edge. Generic; recolour per line."""
    wall = hexc(p.get("wall", "#2a3358"))
    wall2 = hexc(p.get("wall2", "#323d6a"))
    floor = hexc(p.get("floor", "#1d2340"))
    layer(0.9)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), wall)
    for k in range(-12, 24):
        x = k * 260
        flat(ctx, lambda c, x=x: p_poly(c, [(x, -3000), (x + 120, -3000), (x + 120 - 1200, 1600), (x - 1200, 1600)]),
             wall2)
    shape(ctx, lambda c: p_rrect(c, 60, 860, 960, 520, 40), darker(wall, 0.8), BG_OUT, None)
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 3000), floor)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 14), lighter(floor, 0.3))
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)


def tp_neon(ctx, t, layer, p):
    """Our own neon city at sunset (no real or game place): banded orange-pink-purple sky, a big striped sun,
    a skyline of plain towers with lit windows and pink / cyan neon edges, palm trees, water with sun stripes, a
    sea wall at y 1500; to the right (x 1300..2600) the road runs on through scrub (for a border sign)."""
    layer(0.6)
    bands = ["#2a1a4a", "#4a2466", "#7a2e7a", "#b8407a", "#e8606a", "#f48a5a", "#f8b45a"]
    for k, col in enumerate(bands):
        flat(ctx, lambda c, k=k: c.rectangle(-3000, -3000 + (k > 0) * (3000 + 200 + k * 120), 8000, 8000),
             hexc(col))
    ctx.save()
    p_ellipse(ctx, 540, 900, 260, 260)
    ctx.clip()
    flat(ctx, lambda c: c.rectangle(200, 600, 700, 700), hexc("#ffd34d"))
    for k in range(6):
        flat(ctx, lambda c, k=k: c.rectangle(200, 860 + k * 48, 700, 10 + k * 4), hexc("#e8606a"))
    ctx.restore()
    layer(0.8)
    rg = _rng(5)
    x = -400
    while x < 3000:
        w = rg.choice((90, 120, 150))
        h = rg.uniform(180, 560)
        if 1300 < x < 2700:
            h *= 0.25
        cx = x
        shape(ctx, lambda c, cx=cx, w=w, h=h: c.rectangle(cx, 1260 - h, w, h + 40), hexc("#241640"), BG_OUT * 0.6, None)
        neon = hexc(rg.choice(("#ff4fd8", "#5ee0ff")))
        stroke(ctx, [(cx + 4, 1260 - h + 4), (cx + w - 4, 1260 - h + 4)], 6, color=neon,
               a=0.75 + 0.25 * math.sin(t * 3 + x))
        for wy in range(int(1260 - h + 30), 1240, 44):
            for wx in range(int(cx + 16), int(cx + w - 16), 34):
                if rg.random() < 0.55:
                    flat(ctx, lambda c, wx=wx, wy=wy: c.rectangle(wx, wy, 14, 18), hexc("#ffe08a"), a=0.85)
        x += w + rg.choice((10, 30, 60))
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1290, 8000, 210), hexc("#4a2a6a"))
    for k in range(7):
        y = 1310 + k * 28
        w = 260 - k * 30
        flat(ctx, lambda c, y=y, w=w: c.rectangle(540 - w / 2 + 20 * math.sin(t * 2 + y), y, w, 8), hexc("#f8b45a"),
             a=0.7)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 3000), hexc("#3a3246"))
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 16), hexc("#ff4fd8"), a=0.7)
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)
    for k in range(-2, 20):
        flat(ctx, lambda c, k=k: c.rectangle(k * 220, 1680, 110, 16), hexc("#f2c14e"))
    for px_, ph, lean in ((90, 620, -0.10), (980, 560, 0.12), (1180, 640, -0.06), (1700, 520, 0.08), (2400, 600, -0.1)):
        _palm(ctx, t, px_, 1500, ph, lean)


def _palm(ctx, t, x, y, h, lean):
    top = (x + lean * h, y - h)
    pts = [(x, y), (x + lean * h * 0.3, y - h * 0.5), top]
    stroke(ctx, pts, 34, smooth=True)
    stroke(ctx, pts, 22, smooth=True, color=hexc("#5a3a2a"))
    sw = 0.06 * math.sin(t * 1.6 + x)
    for a in (-2.8, -2.3, -1.8, -1.3, -0.8, -0.3):
        a2 = a + sw
        tip = (top[0] + 210 * math.cos(a2), top[1] + 110 * math.sin(a2) + 70)
        mid = (top[0] + 120 * math.cos(a2), top[1] + 80 * math.sin(a2) - 10)
        shape(ctx, lambda c, mid=mid, tip=tip: p_smooth(c, [top, (mid[0], mid[1] - 22), tip, (mid[0], mid[1] + 14)]),
              hexc("#1a3a2e"), BG_OUT * 0.7, None)


ACTORS = {"tp_calendar": tp_calendar, "tp_strip": tp_strip, "tp_tag": tp_tag, "tp_console": tp_console,
          "tp_pad": tp_pad, "tp_bar": tp_bar, "tp_router": tp_router, "tp_box": tp_box, "tp_pc": tp_pc,
          "tp_ballot": tp_ballot, "tp_bubble": tp_bubble, "tp_picket": tp_picket, "tp_couch": tp_couch,
          "tp_stateline": tp_stateline, "tp_blanket": tp_blanket, "tp_note": tp_note}
SCENES = {"tp_living": tp_living, "tp_set": tp_set, "tp_neon": tp_neon}
