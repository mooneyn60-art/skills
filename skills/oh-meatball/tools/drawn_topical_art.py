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


# ================================================================================================ office / outage props
# (11/13 Microsoft outage TikTok: all generic; no brand icons, colours or window shapes; a plain laptop, a plain
#  envelope icon, a plain chart with no numbers)

def tp_desk(ctx, t, p):
    """A plain wooden desk (feet y 0, top surface at y -420, x -380..380), one drawer block on the left."""
    shape(ctx, lambda c: p_rrect(c, -390, -440, 780, 44, 10), C["wood"], OUT, (0.02, 0.2))
    for x in (-360, 330):
        shape(ctx, lambda c, x=x: c.rectangle(x, -400, 30, 400), C["wood_dk"], OUT * 0.8, None)
    shape(ctx, lambda c: c.rectangle(-330, -400, 220, 250), C["wood_dk"], OUT * 0.8, None)
    for y in (-330, -230):
        stroke(ctx, [(-250, y), (-190, y)], 8, color=C["gold"])


def _env_icon(ctx, x, y, s):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    shape(ctx, lambda c: c.rectangle(-60, -40, 120, 80), hexc("#f4ecd6"), OUT * 0.6, None)
    stroke(ctx, [(-60, -40), (0, 8), (60, -40)], OUT * 0.6)
    ctx.restore()


def tp_laptop(ctx, t, p):
    """A plain grey laptop (base centre at the origin, feet y 0; screen 420 x 270 above). p mode:
    "spin" (a spinning loading wheel and a sad face), "inbox" (one empty tray icon, a check mark), "flood" (rows of
    plain envelope lines scroll in, a red badge swells with p n 0..1; no numbers), "garble" (rows of random blocky
    glyph marks, no letters), "off" (dark). p glow 0..1 a screen glow."""
    mode = p.get("mode", "spin")
    shape(ctx, lambda c: p_poly(c, [(-250, -30), (250, -30), (290, 0), (-290, 0)]), hexc("#b8c0c8"), OUT, (0.02, 0.2))
    shape(ctx, lambda c: p_rrect(c, -230, -330, 460, 300, 18), hexc("#9aa3ab"), OUT, None)
    scr = hexc("#16203a") if mode == "off" else hexc("#eef3f8")
    flat(ctx, lambda c: c.rectangle(-210, -312, 420, 264), scr)
    cx, cy = 0, -180
    if mode == "spin":
        for k in range(10):
            a = t * 6 + k * 2 * math.pi / 10
            flat(ctx, lambda c, a=a, k=k: p_ellipse(c, cx - 90 + 30 * math.cos(a), cy - 20 + 30 * math.sin(a), 7, 7),
                 hexc("#5b677a"), a=0.15 + 0.85 * k / 9)
        for ex in (40, 100):
            flat(ctx, lambda c, ex=ex: p_ellipse(c, ex, cy - 40, 10, 12), INK)
        stroke(ctx, [(30, cy + 30), (70, cy + 10), (110, cy + 30)], 9, smooth=True)
        flat(ctx, lambda c: p_ellipse(c, 118, cy - 10, 7, 11), hexc("#5ee0ff"), a=0.9)   # a tear
    elif mode == "inbox":
        shape(ctx, lambda c: p_poly(c, [(-110, cy - 10), (-70, cy - 80), (70, cy - 80), (110, cy - 10), (110, cy + 60),
                                        (-110, cy + 60)]), hexc("#dfe8f4"), OUT * 0.7, None)
        stroke(ctx, [(-110, cy - 10), (-40, cy - 10), (-25, cy + 15), (25, cy + 15), (40, cy - 10), (110, cy - 10)],
               OUT * 0.6)
        stroke(ctx, [(130, cy - 60), (160, cy - 30), (200, cy - 100)], 14, color=C["green"])
    elif mode == "flood":
        n = p.get("n", 0.0)
        rows = 8
        off = (t * 6 * min(1.0, n * 2)) % 1.0
        ctx.save()
        ctx.rectangle(-210, -312, 420, 264)
        ctx.clip()
        for k in range(-1, rows):
            y = -300 + (k + off) * 34
            _env_icon(ctx, -175, y + 12, 0.22)
            flat(ctx, lambda c, y=y, k=k: c.rectangle(-140, y + 4, 230 if k % 2 else 300, 10), hexc("#7a8a9c"))
            flat(ctx, lambda c, y=y: c.rectangle(-140, y + 20, 160, 7), hexc("#b7c1cc"))
        ctx.restore()
        r = 20 + 60 * min(1.0, n)
        shape(ctx, lambda c: p_ellipse(c, 190, -310, r, r), C["pen"], OUT * 0.6, None)
        stroke(ctx, [(190, -310 - r * 0.45), (190, -310 + r * 0.15)], max(4, r * 0.18), color=(1, 1, 1))
        flat(ctx, lambda c: p_ellipse(c, 190, -310 + r * 0.42, r * 0.1, r * 0.1), (1, 1, 1))
    elif mode == "garble":
        rg = _rng(int(t * 8))
        for row in range(7):
            x = -190
            while x < 180:
                w = rg.choice((14, 18, 24))
                flat(ctx, lambda c, x=x, row=row, w=w: c.rectangle(x, -296 + row * 34, w, 20), hexc("#3a3f48"))
                x += w + rg.choice((4, 6, 14))
    g = p.get("glow", 0.0)
    if g > 0.01:
        glow(ctx, 0, -180, 360, hexc("#cfe8ff"), 0.35 * g)


def tp_confetti(ctx, t, p):
    """Confetti falling over a 1000 x 1400 area above the origin (origin = the bottom centre); p on 0..1."""
    on = p.get("on", 0.0)
    if on <= 0.01:
        return
    rg = _rng(21)
    cols = [C["q1"], C["q2"], C["q3"], C["q4"], hexc("#ff4fd8")]
    for k in range(60):
        x0 = rg.uniform(-500, 500)
        sp = rg.uniform(0.25, 0.5)
        u = (t * sp + rg.random()) % 1.0
        x = x0 + 30 * math.sin(t * 3 + k)
        y = -1400 + 1400 * u
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(t * 4 + k)
        flat(ctx, lambda c: c.rectangle(-10, -5, 20, 10), cols[k % 5], a=min(1.0, on))
        ctx.restore()


def tp_chart(ctx, t, p):
    """A plain report chart board centred at its origin (760 x 480): axes, a flat line that spikes straight up as
    p v goes 0..1, a red glow at the tip; p dir -1: a line that was high steps down again instead. No numbers."""
    shape(ctx, lambda c: p_rrect(c, -380, -240, 760, 480, 24), hexc("#f4f7fb"), OUT, None)
    stroke(ctx, [(-320, -190), (-320, 190), (330, 190)], 8)
    for y in (-110, -30, 50, 130):
        stroke(ctx, [(-310, y), (320, y)], 3, color=hexc("#d0d8e2"))
    v = max(0.0, min(1.0, p.get("v", 0.0)))
    if p.get("dir", 1) < 0:   # a line that was high and steps down again as v goes 0..1
        pts = [(-310, -60), (-230, -110), (-150, -40), (-70, 40), (10, 70)]
        u = ease(v)
        tip = (10 + 300 * u, 70 + 110 * u)
        pts += [(10 + 100 * u, 70 + 20 * u), (10 + 180 * u, 70 + 80 * u), tip]
    else:
        pts = [(-310, 170), (-220, 166), (-130, 172), (-40, 168), (40, 170)]
        tip = (90, 170 - 360 * ease(v))
        pts += [(70, 165), tip]
    stroke(ctx, pts, 12, color=C["pen"])
    if v > 0.05:
        glow(ctx, tip[0], tip[1], 70, C["pen"], 0.5 * v)
        shape(ctx, lambda c: p_ellipse(c, tip[0], tip[1], 14, 14), C["pen"], OUT * 0.5, None)


def tp_worker(ctx, t, p):
    """A generic stick-figure office worker (feet y 0, about 420 tall, facing right): round head with dot eyes and a
    smile, a shirt and tie torso, stick limbs; p walk 0..1 swings the legs; p sandwich True holds a sandwich up;
    p shirt colour, p skin colour."""
    sk = hexc(p.get("skin", "#e8b48a"))
    sh = hexc(p.get("shirt", "#7aa7d8"))
    w = p.get("walk", 0.0)
    ph = t * 9 + p.get("ph", 0)
    sw = 28 * w * math.sin(ph)
    for s_ in (1, -1):
        stroke(ctx, [(0, -170), (s_ * sw, -80), (s_ * sw * 1.4 + 10, 0)], 12)
    shape(ctx, lambda c: p_rrect(c, -40, -320, 80, 160, 24), sh, OUT * 0.8, (0.04, 0.1))
    shape(ctx, lambda c: p_poly(c, [(-10, -312), (10, -312), (14, -230), (0, -210), (-14, -230)]), C["red"],
          OUT * 0.4, None)
    stroke(ctx, [(-30, -300), (-60 - sw * 0.5, -230), (-50, -170)], 11)
    if p.get("sandwich", True):
        stroke(ctx, [(30, -300), (80, -280), (90, -330)], 11)
        ctx.save()
        ctx.translate(95, -345)
        ctx.rotate(-0.2)
        shape(ctx, lambda c: p_rrect(c, -46, -20, 92, 40, 12), hexc("#e8c46a"), OUT * 0.5, None)
        flat(ctx, lambda c: c.rectangle(-48, -4, 96, 8), C["green"])
        flat(ctx, lambda c: c.rectangle(-44, 4, 88, 6), C["red"])
        ctx.restore()
    else:
        stroke(ctx, [(30, -300), (60 + sw * 0.5, -230), (50, -170)], 11)
    shape(ctx, lambda c: p_ellipse(c, 0, -385, 62, 66), sk, OUT * 0.8, (0.06, 0.1))
    for ex in (-18, 22):
        flat(ctx, lambda c, ex=ex: p_ellipse(c, ex, -395, 7, 9), INK)
    stroke(ctx, [(-18, -360), (4, -348), (26, -362)], 6, smooth=True)


def tp_globe(ctx, t, p):
    """A plain drawn globe centred at its origin (r 300): blue sea, blobby green land that drifts round, p n 0..1
    red dots pop up, p snow 0..1 snow falls over it and caps the top."""
    r = 300
    shape(ctx, lambda c: p_ellipse(c, 0, 0, r, r), hexc("#2f7fc0"), OUT, (0.05, 0.08), (0.3, 0.25, 0.25))
    ctx.save()
    p_ellipse(ctx, 0, 0, r - 4, r - 4)
    ctx.clip()
    off = (t * 30) % 800
    rg = _rng(3)
    for k in range(7):
        bx = rg.uniform(-400, 400)
        by = rg.uniform(-220, 220)
        rx, ry = rg.uniform(60, 130), rg.uniform(40, 100)
        for dx in (-800, 0, 800):
            x = (bx + off + 400) % 800 - 400 + dx
            shape(ctx, lambda c, x=x, by=by, rx=rx, ry=ry: p_ellipse(c, x, by, rx, ry, 0.3), C["green"],
                  BG_OUT * 0.6, None)
    n = p.get("n", 0.0)
    rg = _rng(8)
    for k in range(int(40 * min(1.0, n))):
        x, y = rg.uniform(-250, 250), rg.uniform(-230, 230)
        if x * x + y * y > (r - 30) ** 2:
            continue
        pr = 12 + 3 * math.sin(t * 6 + k)
        shape(ctx, lambda c, x=x, y=y, pr=pr: p_ellipse(c, x, y, pr, pr), C["pen"], OUT * 0.4, None)
    sn = p.get("snow", 0.0)
    if sn > 0.01:
        flat(ctx, lambda c: p_ellipse(c, 0, -r, r * 0.8, 90 * min(1.0, sn)), (1, 1, 1), a=0.95)
    ctx.restore()
    if sn > 0.01:
        rg = _rng(13)
        for k in range(40):
            x0 = rg.uniform(-480, 480)
            u = (t * rg.uniform(0.15, 0.3) + rg.random()) % 1.0
            flat(ctx, lambda c, x0=x0, u=u, k=k: p_ellipse(c, x0 + 20 * math.sin(t * 2 + k), -520 + 1040 * u, 9, 9),
                 (1, 1, 1), a=min(1.0, sn) * 0.9)


def tp_rack(ctx, t, p):
    """A server rack (feet y 0, 300 wide, 640 tall): stacked units with blinking lights; p sweat 0..1 sweat drops
    fly off and the lights go red; p wobble 0..1 it rocks; p spin 0..1 an updating wheel on the front; p dark 0..1
    every light goes out (a server going dark)."""
    wb = p.get("wobble", 0.0)
    ctx.save()
    ctx.rotate(math.radians(4 * wb * math.sin(t * 11)))
    shape(ctx, lambda c: p_rrect(c, -150, -640, 300, 640, 14), hexc("#2b2f38"), OUT, (0.03, 0.06))
    sw = p.get("sweat", 0.0)
    for k in range(7):
        y = -610 + k * 84
        shape(ctx, lambda c, y=y: p_rrect(c, -125, y, 250, 66, 8), hexc("#3a3f48"), OUT * 0.5, None)
        for j in range(4):
            on = math.sin(t * 9 + k * 1.3 + j * 2) > -0.2 and p.get("dark", 0.0) < 0.5
            col = C["pen"] if sw > 0.3 else hexc("#3fb950")
            flat(ctx, lambda c, y=y, j=j: p_ellipse(c, 70 + j * -26, y + 33, 7, 7), col if on else hexc("#555b66"))
        flat(ctx, lambda c, y=y: c.rectangle(-105, y + 26, 90, 14), hexc("#1d2128"))
    sp = p.get("spin", 0.0)
    if sp > 0.01 and p.get("dark", 0.0) < 0.5:   # an "updating" wheel on the front (no words)
        shape(ctx, lambda c: p_ellipse(c, 0, -330, 95, 95), hexc("#16203a"), OUT * 0.6, None, a=min(1.0, sp))
        for k in range(10):
            a_ = t * 6 + k * 2 * math.pi / 10
            flat(ctx, lambda c, a_=a_, k=k: p_ellipse(c, 55 * math.cos(a_), -330 + 55 * math.sin(a_), 11, 11),
                 hexc("#5ee0ff"), a=min(1.0, sp) * (0.15 + 0.85 * k / 9))
    dk = p.get("dark", 0.0)
    if dk > 0.01:
        flat(ctx, lambda c: p_rrect(c, -150, -640, 300, 640, 14), hexc("#05070c"), a=0.55 * min(1.0, dk))
    ctx.restore()
    if sw > 0.01:
        for k in range(6):
            u = (t * 1.2 + k / 6) % 1.0
            side = 1 if k % 2 else -1
            x = side * (150 + 160 * u)
            y = -560 + k * 40 - 200 * math.sin(u * math.pi)
            shape(ctx, lambda c, x=x, y=y: p_poly(c, [(x, y - 26), (x + 14, y), (x, y + 12), (x - 14, y)]),
                  hexc("#8fd3f4"), OUT * 0.4, None, a=min(1.0, sw) * (1 - u))


def tp_padlock(ctx, t, p):
    """A big closed padlock (centre at the origin, body 260 x 220, shackle above): intact; p shine 0..1 a sparkle
    sweep, p check 0..1 a green check badge."""
    ctx.save()
    p_smooth(ctx, [(-90, -60), (-90, -170), (0, -240), (90, -170), (90, -60)], close=False)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(56)
    ctx.stroke()
    p_smooth(ctx, [(-90, -60), (-90, -170), (0, -240), (90, -170), (90, -60)], close=False)
    ctx.set_source_rgb(*hexc("#9aa3ab"))
    ctx.set_line_width(38)
    ctx.stroke()
    ctx.restore()
    shape(ctx, lambda c: p_rrect(c, -130, -80, 260, 220, 30), C["gold"], OUT, (0.04, 0.1), (0.25, 0.2, 0.25))
    flat(ctx, lambda c: p_ellipse(c, 0, 10, 24, 24), INK)
    flat(ctx, lambda c: p_poly(c, [(-12, 20), (12, 20), (18, 80), (-18, 80)]), INK)
    sh = p.get("shine", 0.0)
    if sh > 0.01:
        x = -130 + 260 * ((t * 0.8) % 1.0)
        ctx.save()
        p_rrect(ctx, -130, -80, 260, 220, 30)
        ctx.clip()
        flat(ctx, lambda c: p_poly(c, [(x, -90), (x + 40, -90), (x - 40, 150), (x - 80, 150)]), (1, 1, 1), a=0.5 * sh)
        ctx.restore()
    ck = p.get("check", 0.0)
    if ck > 0.01:
        u = back_out(min(1.0, ck))
        ctx.save()
        ctx.translate(150, 110)
        ctx.scale(u, u)
        shape(ctx, lambda c: p_ellipse(c, 0, 0, 60, 60), C["green"], OUT * 0.7, None)
        stroke(ctx, [(-26, 0), (-6, 22), (30, -24)], 14, color=(1, 1, 1))
        ctx.restore()


def tp_login(ctx, t, p):
    """A plain login box centred at its origin (600 x 300): a user row and a password row; p n 0..1 types p text
    into the password row letter by letter (the spec's word, shown in the clear) with a blinking cursor."""
    shape(ctx, lambda c: p_rrect(c, -300, -150, 600, 300, 26), hexc("#f4f7fb"), OUT, None)
    flat(ctx, lambda c: p_rrect(c, -300, -150, 600, 54, 26), hexc("#5b677a"))
    flat(ctx, lambda c: c.rectangle(-300, -120, 600, 24), hexc("#5b677a"))
    for k, y in enumerate((-50, 60)):
        shape(ctx, lambda c, y=y: p_rrect(c, -250, y - 36, 500, 72, 14), (1, 1, 1), OUT * 0.6, None)
        shape(ctx, lambda c, y=y, k=k: p_ellipse(c, -215, y, 16, 16), hexc("#9aa3ab"), 0, None)
    flat(ctx, lambda c: c.rectangle(-180, -58, 140, 14), hexc("#b7c1cc"))
    txt = p.get("text", "")
    n = int(round(len(txt) * max(0.0, min(1.0, p.get("n", 0.0)))))
    shown = txt[:n]
    w = 0
    if shown:
        import drawn_keepkill as kk
        w = kk.text_img(shown, int(p.get("px", 60)), "#1b1b1b", 0, 0.0)[0].get_width()
        text(ctx, shown, -180 + w / 2, 62, p.get("px", 60), "#1b1b1b", 0)
    if math.sin(t * 8) > 0:
        x = -180 + (w if shown else 0) + 8
        flat(ctx, lambda c: c.rectangle(x, 32, 6, 60), INK)


def tp_clock(ctx, t, p):
    """A round wall clock centred at its origin (r 200); p speed (turns a second of the minute hand) spins the hands;
    p wobble 0..1 it shakes."""
    sp = p.get("speed", 1.0)
    ctx.save()
    ctx.rotate(math.radians(3 * p.get("wobble", 0.0) * math.sin(t * 20)))
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 200, 200), (1, 1, 1), OUT * 1.2, (0.04, 0.06))
    for k in range(12):
        a = k * math.pi / 6
        stroke(ctx, [(170 * math.cos(a), 170 * math.sin(a)), (148 * math.cos(a), 148 * math.sin(a))], 8)
    am = t * sp * 2 * math.pi - math.pi / 2
    ah = am / 12 - math.pi / 3
    if "h0" in p:   # sweep the hour hand from p h0 to p h1 o'clock as p u goes 0..1 (minute hand races)
        hh = p["h0"] + (p.get("h1", p["h0"]) - p["h0"]) * ease(min(1.0, max(0.0, p.get("u", 0.0))))
        ah = hh / 12 * 2 * math.pi - math.pi / 2
        am = (hh % 1.0) * 2 * math.pi - math.pi / 2
    stroke(ctx, [(0, 0), (90 * math.cos(ah), 90 * math.sin(ah))], 16)
    stroke(ctx, [(0, 0), (140 * math.cos(am), 140 * math.sin(am))], 10, color=C["pen"])
    flat(ctx, lambda c: p_ellipse(c, 0, 0, 14, 14), INK)
    ctx.restore()


def tp_keyboard(ctx, t, p):
    """A big plain keyboard seen from the front (centre at the origin, 640 x 220) with blank keys; p q 0..1 three
    question marks float up off it."""
    shape(ctx, lambda c: p_rrect(c, -320, -110, 640, 220, 24), hexc("#d9dee6"), OUT, (0.02, 0.1))
    for r in range(4):
        for k in range(11):
            x = -290 + k * 53 + (r % 2) * 12
            if x > 250:
                continue
            shape(ctx, lambda c, x=x, r=r: p_rrect(c, x, -88 + r * 46, 44, 38, 8), (1, 1, 1), OUT * 0.35, None)
    q = p.get("q", 0.0)
    if q > 0.01:
        for k in range(3):
            u = (t * 0.6 + k / 3) % 1.0
            text(ctx, "?", -160 + k * 160, -150 - 220 * u, 90, "#ffd34d", 6, a=min(1.0, q) * (1 - u * 0.8))


def tp_money(ctx, t, p):
    """A stack of plain green bills (feet y 0, 360 wide) with a big question mark bobbing over it; p q 0..1."""
    for k in range(8):
        y = -k * 34
        x = 6 * math.sin(k * 1.7)
        shape(ctx, lambda c, x=x, y=y: p_rrect(c, x - 180, y - 34, 360, 34, 6), hexc("#7cc061"), OUT * 0.6, None)
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y - 17, 24, 11), hexc("#4f9a3a"))
    q = p.get("q", 1.0)
    if q > 0.01:
        sc = back_out(min(1.0, q))
        text(ctx, "?", 0, -380 + 12 * math.sin(t * 3), int(220 * sc), "#ffd34d", 10)


def tp_zzz(ctx, t, p):
    """A sleep bubble (no letters): three growing rings drift up from the origin; p on 0..1."""
    on = p.get("on", 0.0)
    if on <= 0.01:
        return
    for k in range(3):
        u = (t * 0.5 + k / 3) % 1.0
        r = 14 + 30 * u
        shape(ctx, lambda c, u=u, r=r: p_ellipse(c, 60 * u, -200 * u, r, r), hexc("#dff2ff"), OUT * 0.4, None,
              a=min(1.0, on) * (1 - u))


ACTORS.update({"tp_desk": tp_desk, "tp_laptop": tp_laptop, "tp_confetti": tp_confetti, "tp_chart": tp_chart,
               "tp_worker": tp_worker, "tp_globe": tp_globe, "tp_rack": tp_rack, "tp_padlock": tp_padlock,
               "tp_login": tp_login, "tp_clock": tp_clock, "tp_keyboard": tp_keyboard, "tp_money": tp_money,
               "tp_zzz": tp_zzz})


# ================================================================================================ Jensen part 2 props
# (11/13: generic household props; the only words are those a spec passes in)

def tp_jar(ctx, t, p):
    """A glass coin jar (feet y 0, 170 wide, 230 tall) holding a few coins; tip it with the actor's rot; p spill
    0..1 coins fly out of the mouth."""
    shape(ctx, lambda c: p_rrect(c, -85, -200, 170, 200, 30), hexc("#cfe8f4"), OUT, None, a=0.75)
    for k in range(9):
        x = -55 + (k % 4) * 36 + (k // 4) * 12
        y = -22 - (k // 4) * 18
        shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 18, 9), C["gold"], OUT * 0.4, None)
    shape(ctx, lambda c: p_rrect(c, -70, -232, 140, 40, 10), hexc("#8d969c"), OUT * 0.8, None)
    sp = p.get("spill", 0.0)
    if sp > 0.01:
        for k in range(6):
            u = min(1.0, sp * 1.4 - k * 0.07)
            if u <= 0:
                continue
            x = -40 + k * 18 + 140 * u
            y = -240 - 160 * math.sin(u * math.pi) + 260 * u * u
            shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 16, 16), C["gold"], OUT * 0.4, None)


def tp_shelf(ctx, t, p):
    """A wall shelf plank on two brackets, top surface at the origin, p w wide (default 360)."""
    w = p.get("w", 360)
    shape(ctx, lambda c: c.rectangle(-w / 2, 0, w, 26), C["wood"], OUT * 0.8, None)
    for x in (-w / 3, w / 3):
        shape(ctx, lambda c, x=x: p_poly(c, [(x - 8, 26), (x + 8, 26), (x + 8, 90), (x - 8, 70)]), C["wood_dk"],
              OUT * 0.6, None)


def tp_table(ctx, t, p):
    """A small restaurant table for two (feet y 0, 420 wide, top at y -300) with a white cloth, two plates, a
    lit candle that flickers and an empty chair on the far side."""
    shape(ctx, lambda c: p_rrect(c, 230, -520, 30, 520, 10), C["wood_dk"], OUT * 0.8, None)
    shape(ctx, lambda c: p_rrect(c, 150, -300, 160, 30, 8), C["wood_dk"], OUT * 0.8, None)
    shape(ctx, lambda c: c.rectangle(160, -270, 18, 270), C["wood_dk"], OUT * 0.6, None)
    stroke(ctx, [(-10, -300), (-10, 0)], 18)
    stroke(ctx, [(-90, 0), (70, 0)], 14)
    shape(ctx, lambda c: p_poly(c, [(-220, -310), (200, -310), (230, -200), (-250, -200)]), (1, 1, 1), OUT, None)
    for x in (-130, 90):
        shape(ctx, lambda c, x=x: p_ellipse(c, x, -318, 60, 14), hexc("#e8eef4"), OUT * 0.5, None)
    shape(ctx, lambda c: c.rectangle(-26, -420, 22, 100), hexc("#f4ecd6"), OUT * 0.6, None)
    fl = 1 + 0.12 * math.sin(t * 17) + 0.06 * math.sin(t * 29)
    glow(ctx, -15, -450, 140, C["light"], 0.5)
    shape(ctx, lambda c: p_smooth(c, [(-15, -480 * fl + 0 * fl), (0, -440), (-15, -425), (-30, -440)]),
          hexc("#ffb02e"), OUT * 0.4, None)


def tp_badge(ctx, t, p):
    """A paper name badge on a safety pin, centred at its origin (240 x 130), with p text in crayon colour;
    p on 0..1 pops it on."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    sc = back_out(min(1.0, on))
    ctx.save()
    ctx.scale(sc, sc)
    ctx.rotate(math.radians(p.get("tilt", -8)))
    shape(ctx, lambda c: p_rrect(c, -120, -65, 240, 130, 10), (1, 1, 1), OUT * 0.8, None)
    stroke(ctx, [(-60, -75), (60, -75)], 6, color=C["steel"])
    if p.get("text"):
        text(ctx, p["text"], 0, 6, p.get("px", 70), p.get("tcol", "#d8322a"), 0)
    ctx.restore()


def tp_tray(ctx, t, p):
    """An office in-tray (feet y 0, 420 wide, 120 deep) on a stand, a label plate with p text (a spec word, e.g.
    PENDING), a sheet lying in it (p paper), a dusty cobweb across one corner (p web 0..1)."""
    shape(ctx, lambda c: p_poly(c, [(-210, -130), (210, -130), (190, -10), (-190, -10)]), hexc("#8d969c"), OUT, None)
    if p.get("paper", True):
        ctx.save()
        ctx.translate(0, -140)
        ctx.rotate(-0.06)
        shape(ctx, lambda c: c.rectangle(-150, -40, 300, 40), C["paper"], OUT * 0.6, None)
        for k in range(3):
            stroke(ctx, [(-120 + k * 90, -24), (-60 + k * 90, -18)], 6, smooth=True, color=C["crayon"])
        ctx.restore()
    shape(ctx, lambda c: p_poly(c, [(-210, -130), (210, -130), (230, -100), (-230, -100)]), hexc("#b7c1cc"), OUT,
          None)
    shape(ctx, lambda c: p_rrect(c, -130, -95, 260, 70, 10), hexc("#f4ecd6"), OUT * 0.6, None)
    if p.get("text"):
        text(ctx, p["text"], 0, -60, p.get("px", 54), "#1b1b1b", 0)
    w = p.get("web", 1.0)
    if w > 0.01:
        cx, cy = 200, -130
        for k in range(5):
            a = math.pi + k * (math.pi / 2) / 4
            stroke(ctx, [(cx, cy), (cx + 170 * math.cos(a), cy - 170 * math.sin(a) * -1)], 3, color=(1, 1, 1),
                   a=0.85 * w)
        for r in (50, 95, 140):
            pts = [(cx + r * math.cos(math.pi + k * (math.pi / 2) / 4), cy + r * math.sin(math.pi + k * (math.pi / 2) / 4))
                   for k in range(5)]
            stroke(ctx, pts, 3, color=(1, 1, 1), a=0.85 * w)


def tp_sidetable(ctx, t, p):
    """A small round side table (feet y 0, top at y -330, 260 wide)."""
    shape(ctx, lambda c: p_ellipse(c, 0, -330, 130, 26), C["wood"], OUT, None)
    stroke(ctx, [(0, -310), (0, -20)], 20)
    stroke(ctx, [(0, -310), (0, -20)], 10, color=C["wood_dk"])
    shape(ctx, lambda c: p_ellipse(c, 0, -10, 80, 14), C["wood_dk"], OUT * 0.7, None)


ACTORS.update({"tp_jar": tp_jar, "tp_shelf": tp_shelf, "tp_table": tp_table, "tp_badge": tp_badge, "tp_tray": tp_tray,
               "tp_sidetable": tp_sidetable})


# ================================================================================================ airport (FAA ground stop)
# (11/13: generic planes, plain white, no airline names, logos or liveries; nothing shows danger in the air)

def _plane(ctx, x, y, s, rot=0.0, flip=False):
    """A plain white side-view airliner centred at (x, y), nose to the right (flip: to the left)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(-s if flip else s, s)
    shape(ctx, lambda c: p_poly(c, [(-230, -20), (-200, -120), (-160, -120), (-130, -30)]), hexc("#dfe6ee"), OUT, None)
    shape(ctx, lambda c: p_smooth(c, [(-240, -10), (150, -30), (240, 0), (150, 34), (-230, 24)]), hexc("#f4f7fb"), OUT,
          (0.02, 0.15))
    for k in range(9):
        flat(ctx, lambda c, k=k: p_ellipse(c, -150 + k * 32, -6, 7, 9), hexc("#5b677a"))
    flat(ctx, lambda c: p_poly(c, [(170, -18), (205, -14), (200, -2), (170, -4)]), hexc("#5b677a"))
    shape(ctx, lambda c: p_poly(c, [(-40, 8), (60, 8), (-10, 70), (-60, 70)]), hexc("#c9d2dc"), OUT * 0.8, None)
    shape(ctx, lambda c: p_rrect(c, -20, 30, 70, 30, 14), hexc("#9aa3ab"), OUT * 0.6, None)
    ctx.restore()


def tp_gate(ctx, t, layer, p):
    """An airport gate hall: grey-blue wall, a big window at x 500..1060, y 560..1200 with sky, tarmac and a row of
    parked plain white planes, a ceiling band, carpet floor at y 1500. p board_wall False leaves the left wall plain.
    The window and planes run on to the right to x 2400. p night 1: dark sky with stars and a moon, darker hall,
    small blinking lights on the parked planes."""
    night = p.get("night", 0)
    layer(0.9)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), hexc("#4a5670" if night else "#8fa3b8"))
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 3300), hexc("#3a4458" if night else "#6f8399"))
    for x0, x1 in ((500, 1060), (1160, 2400)):
        shape(ctx, lambda c, x0=x0, x1=x1: c.rectangle(x0, 560, x1 - x0, 640), hexc("#141c33" if night else "#bfe6f8"),
              BG_OUT, None)
        flat(ctx, lambda c, x0=x0, x1=x1: c.rectangle(x0, 1040, x1 - x0, 160), hexc("#3a3f48" if night else "#7d8790"))
        flat(ctx, lambda c, x0=x0, x1=x1: c.rectangle(x0, 1110, x1 - x0, 8), hexc("#f2c14e"))
    if night:
        rg = _rng(31)
        for k in range(40):
            x, y = rg.uniform(500, 2400), rg.uniform(570, 1000)
            flat(ctx, lambda c, x=x, y=y, k=k: p_ellipse(c, x, y, 3, 3), (1, 1, 1), a=0.5 + 0.5 * math.sin(t * 2 + k))
        flat(ctx, lambda c: p_ellipse(c, 900, 680, 40, 40), hexc("#f4ecd6"))
        flat(ctx, lambda c: p_ellipse(c, 918, 668, 34, 34), hexc("#141c33"))
    else:
        flat(ctx, lambda c: p_ellipse(c, 900, 680, 46, 46), hexc("#ffd84a"))
    for k, px_ in enumerate((640, 930, 1300, 1620, 1940, 2260)):
        _plane(ctx, px_, 1050, 0.55, 0.0, flip=k % 2 == 1)
        if night:
            on = math.sin(t * 4 + k * 1.7) > 0
            for dx, col in ((-120, "#e5383b"), (120, "#3fb950")):
                flat(ctx, lambda c, dx=dx, px_=px_: p_ellipse(c, px_ + dx * (-1 if k % 2 else 1), 1080, 7, 7),
                     hexc(col), a=1.0 if on else 0.35)
            flat(ctx, lambda c, px_=px_: p_ellipse(c, px_, 1035, 6, 6), (1, 1, 1), a=1.0 if not on else 0.3)
    for x0, x1 in ((500, 1060), (1160, 2400)):
        for x in range(x0, x1 + 1, 140):
            stroke(ctx, [(x, 560), (x, 1200)], BG_OUT * 1.4, color=hexc("#5b677a"))
        stroke(ctx, [(x0, 880), (x1, 880)], BG_OUT, color=hexc("#5b677a"))
        shape(ctx, lambda c, x0=x0, x1=x1: c.rectangle(x0, 560, x1 - x0, 640), (1, 1, 1), BG_OUT * 1.4, None, a=0.0)
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 3000), hexc("#2a3550" if night else "#3b4a6b"))
    for k in range(-20, 40):
        flat(ctx, lambda c, k=k: c.rectangle(k * 120, 1560, 60, 10), hexc("#334260"))
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)


def tp_board(ctx, t, p):
    """A departures board centred at its origin (420 x 360): dark panel, p rows rows; p flip 0..1 flips them one
    by one (split-flap squash) from blank dots to p text (a spec word, e.g. DELAYED) in amber; p text2 with p flip2
    0..1 flips rows on to a second word (e.g. CANCELLED) in red, in p order (row ranks). No numbers, cities or
    airline names."""
    rows = int(p.get("rows", 5))
    shape(ctx, lambda c: p_rrect(c, -210, -180, 420, 360, 18), hexc("#1b1f2a"), OUT, None)
    stroke(ctx, [(0, -180), (0, -260)], 8)
    fl = p.get("flip", 1.0) * rows
    rh = 300 / rows
    for k in range(rows):
        y = -150 + k * rh + rh / 2
        flat(ctx, lambda c, y=y: p_rrect(c, -185, y - rh * 0.4, 370, rh * 0.8, 6), hexc("#2a3040"))
        u = fl - k
        u2 = p.get("flip2", 0.0) * rows - p.get("order", [k for k in range(rows)])[k] if p.get("text2") else 0.0
        if u2 > 0:   # the row flips on to the second word (e.g. CANCELLED), in red
            sq = 1.0 if u2 >= 1 else abs(u2 - 0.5) * 2
            ctx.save()
            ctx.translate(0, y)
            ctx.scale(1, max(0.05, sq))
            if u2 >= 0.5:
                text(ctx, p["text2"], 0, 0, p.get("px", 46), p.get("col2", "#ff5a4e"), 0)
            else:
                text(ctx, p.get("text", ""), 0, 0, p.get("px", 46), p.get("col", "#ffb02e"), 0)
            ctx.restore()
        elif u >= 1 or (u > 0 and u >= 0.5):
            sq = 1.0 if u >= 1 else (u - 0.5) * 2
            ctx.save()
            ctx.translate(0, y)
            ctx.scale(1, max(0.05, sq))
            text(ctx, p.get("text", ""), 0, 0, p.get("px", 46), p.get("col", "#ffb02e"), 0)
            ctx.restore()
        else:
            sq = 1.0 if u <= 0 else 1 - u * 2
            ctx.save()
            ctx.translate(0, y)
            ctx.scale(1, max(0.05, sq))
            for j in range(7):
                flat(ctx, lambda c, j=j: p_rrect(c, -150 + j * 44, -12, 30, 24, 4), hexc("#4a5160"))
            ctx.restore()


def tp_seats(ctx, t, p):
    """A row of p n linked gate seats (feet y 0, seat top y -230, each 170 wide) on one bar."""
    n = int(p.get("n", 3))
    w = 170
    x0 = -n * w / 2
    stroke(ctx, [(x0 + 20, -90), (x0 + n * w - 20, -90)], 16)
    for x in (x0 + 40, x0 + n * w - 40):
        stroke(ctx, [(x, -90), (x, 0)], 12)
    for k in range(n):
        x = x0 + k * w
        shape(ctx, lambda c, x=x: p_rrect(c, x + 10, -440, w - 20, 210, 30), hexc("#3b7dd8"), OUT * 0.8, (0.03, 0.1))
        stroke(ctx, [(x + w / 2, -200), (x + w / 2, -90)], 12)
        shape(ctx, lambda c, x=x: p_rrect(c, x + 6, -250, w - 12, 60, 20), hexc("#2f6bbf"), OUT * 0.8, None)


def tp_suitcase(ctx, t, p):
    """A carry-on suitcase (feet y 0, 220 wide, 300 tall) with a pulled-up handle and two wheels; p col."""
    col = hexc(p.get("col", "#d8322a"))
    stroke(ctx, [(-50, -300), (-50, -430), (50, -430), (50, -300)], 12, color=hexc("#3a3f48"))
    shape(ctx, lambda c: p_rrect(c, -110, -310, 220, 290, 24), col, OUT, (0.03, 0.08))
    for x in (-50, 0, 50):
        stroke(ctx, [(x, -290), (x, -40)], 5, color=darker(col, 0.75))
    for x in (-70, 70):
        shape(ctx, lambda c, x=x: p_ellipse(c, x, -10, 16, 16), INK, 0, None)


def tp_pretzel(ctx, t, p):
    """A giant soft pretzel centred at its origin (about 300 wide), salt flecks; p gone 0..1: it is eaten and only
    a crumpled paper wrapper is left."""
    g = p.get("gone", 0.0)
    if g < 0.5:
        def loop(c):
            p_smooth(c, [(-20, 60), (-140, -40), (-120, -120), (-30, -110), (0, -40), (30, -110), (120, -120),
                         (140, -40), (20, 60), (0, 120)], close=True)
        ctx.save()
        loop(ctx)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(64)
        ctx.stroke()
        loop(ctx)
        ctx.set_source_rgb(*hexc("#b8702e"))
        ctx.set_line_width(46)
        ctx.stroke()
        ctx.restore()
        rg = _rng(5)
        for k in range(14):
            flat(ctx, lambda c, x=rg.uniform(-130, 130), y=rg.uniform(-120, 80): c.rectangle(x, y, 8, 8), (1, 1, 1))
    else:
        shape(ctx, lambda c: p_poly(c, [(-90, -40), (-30, -70), (40, -50), (90, -60), (70, 20), (90, 60), (10, 50),
                                        (-60, 70), (-80, 20)]), hexc("#f4ecd6"), OUT * 0.7, None)
        for k in range(4):
            stroke(ctx, [(-60 + k * 35, -40), (-50 + k * 35, 40)], 3, color=hexc("#b7a77a"))


def tp_usmap(ctx, t, p):
    """A plain outline map of the contiguous United States centred at its origin (about 940 x 600; no labels, no
    state lines), small parked plane icons on it; p land 0..1 three planes in the air finish their arcs and come
    down to land normally at their dots; p park 0..1 the parked planes pop in; p divert 1: one of them lands at a
    different airport instead (calm, no drama)."""
    pts = [(40, 40), (430, 60), (520, 110), (560, 90), (600, 130), (650, 120), (820, 60), (880, 20), (930, 50),
           (900, 110), (860, 170), (840, 230), (800, 280), (790, 340), (760, 400), (730, 440), (755, 500), (770, 545),
           (750, 560), (720, 510), (690, 470), (620, 470), (560, 480), (520, 500), (470, 540), (430, 560), (400, 520),
           (360, 470), (310, 480), (280, 440), (250, 450), (200, 430), (120, 410), (80, 380), (50, 330), (20, 250),
           (10, 180), (30, 100)]
    pts = [(x - 470, y - 300) for x, y in pts]
    shape(ctx, lambda c: p_smooth(c, pts), hexc("#e8eef4"), OUT, (0.01, 0.03))
    dots = [(-330, -120), (-240, 60), (-80, -60), (60, 40), (180, -110), (300, -40), (230, 120), (-370, 30),
            (100, 160), (360, -170)]
    pk = p.get("park", 1.0)
    for k, (x, y) in enumerate(dots):
        u = back_out(min(1.0, max(0.0, pk * 10 - k)))
        if u > 0.01:
            _plane(ctx, x, y, 0.13 * u, 0.0, flip=k % 2 == 0)
    oc = p.get("ocean", 0.0)
    if p.get("home"):   # a red ring round one dot (Meatball's airport)
        hx, hy = p["home"]
        ctx.save()
        ctx.new_path()
        ctx.arc(hx, hy, 34 + 3 * math.sin(t * 5), 0, 2 * math.pi)
        ctx.set_source_rgb(*C["pen"])
        ctx.set_line_width(8)
        ctx.stroke()
        ctx.restore()
    if p.get("mode") == "ocean":   # a plane leaves the west coast out over the ocean, one leaves the east coast
        u = ease(min(1.0, max(0.0, oc)))
        for (x0, y0), (x1, y1), fl in (((-420, -40), (-760, -120), True), ((400, -150), (760, -260), False)):
            stroke(ctx, [(x0, y0), (x0 + (x1 - x0) * u, y0 + (y1 - y0) * u)], 4, color=hexc("#9aa3ab"), a=0.6)
            _plane(ctx, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, 0.15, 0.0, flip=fl)
        return
    ld = p.get("land", 0.0)
    legs = [((-420, -200), (-240, 60)), ((420, -220), (180, -110)), ((-60, -260), (60, 40))]
    if p.get("divert", 0):   # the last plane calmly lands at another airport instead (its planned arc stays faint)
        (x0, y0), (x1, y1) = legs[2]
        stroke(ctx, [(x0, y0), (x0 + (x1 - x0) * 0.5, y0 + (y1 - y0) * 0.5 - 120), (x1, y1)], 4, smooth=True,
               color=hexc("#9aa3ab"), a=0.25)
        legs[2] = ((-60, -260), (230, 120))
    for k, ((x0, y0), (x1, y1)) in enumerate(legs):
        u = ease(min(1.0, max(0.0, ld)))
        x = x0 + (x1 - x0) * u
        y = y0 + (y1 - y0) * u - 120 * math.sin(u * math.pi)
        stroke(ctx, [(x0, y0), (x0 + (x1 - x0) * 0.5, y0 + (y1 - y0) * 0.5 - 120), (x1, y1)], 4, smooth=True,
               color=hexc("#9aa3ab"), a=0.6)
        _plane(ctx, x, y, 0.13, 0.0, flip=x1 < x0)


def tp_tower(ctx, t, p):
    """A generic airport control tower (feet y 0, about 760 tall): a shaft, a glass cab with a lit band and an
    antenna; p blink 0..1 the beacon blinks."""
    shape(ctx, lambda c: p_poly(c, [(-60, 0), (60, 0), (45, -520), (-45, -520)]), hexc("#d9dee6"), OUT, (0.03, 0.06))
    shape(ctx, lambda c: p_poly(c, [(-130, -520), (130, -520), (160, -640), (-160, -640)]), hexc("#8fd3f4"), OUT, None)
    for x in (-90, -30, 30, 90):
        stroke(ctx, [(x * 1.1, -525), (x * 1.2, -635)], 6, color=hexc("#5b677a"))
    shape(ctx, lambda c: p_rrect(c, -170, -680, 340, 44, 10), hexc("#5b677a"), OUT, None)
    stroke(ctx, [(0, -680), (0, -760)], 8)
    if math.sin(t * 5) > 0 or p.get("blink", 1.0) < 0.5:
        flat(ctx, lambda c: p_ellipse(c, 0, -766, 12, 12), C["pen"])


def tp_static(ctx, t, p):
    """A radio link from the origin to (p dx, p dy): smooth dashed waves while p bad is 0, a jagged grey static
    zigzag with a broken middle as p bad goes to 1."""
    dx, dy = p.get("dx", 600), p.get("dy", -200)
    bad = p.get("bad", 0.0)
    n = 24
    pts = []
    rg = _rng(int(t * 12))
    for k in range(n + 1):
        u = k / n
        x, y = dx * u, dy * u
        nx, ny = -dy, dx
        ln = math.hypot(nx, ny) or 1
        amp = (1 - bad) * 14 * math.sin(u * 30 - t * 10) + bad * rg.uniform(-40, 40)
        pts.append((x + nx / ln * amp, y + ny / ln * amp))
    if bad < 0.5:
        stroke(ctx, pts, 7, smooth=True, color=hexc("#5ee0ff"))
    else:
        stroke(ctx, pts[:10], 7, color=hexc("#9aa3ab"))
        stroke(ctx, pts[14:], 7, color=hexc("#9aa3ab"))
        mx, my = pts[12]
        starburst(ctx, mx, my, 36, 8, hexc("#cfd6de"), OUT * 0.5)


def tp_radar(ctx, t, p):
    """A radar desk (feet y 0, 600 wide, top y -360): a round green radar screen with a sweeping line, two
    headsets lying on the desk; p dim 0..1 the screen fades to static grey."""
    shape(ctx, lambda c: c.rectangle(-300, -380, 600, 40), hexc("#5b677a"), OUT, None)
    shape(ctx, lambda c: c.rectangle(-280, -340, 560, 340), hexc("#3a3f48"), OUT * 0.8, None)
    shape(ctx, lambda c: p_rrect(c, -160, -700, 320, 300, 24), hexc("#2b2f38"), OUT, None)
    dm = p.get("dim", 0.0)
    flat(ctx, lambda c: p_ellipse(c, 0, -550, 120, 120), hexc("#0f2a1a"))
    if dm < 0.5:
        for r in (40, 80, 118):
            ctx.save()
            ctx.new_path()
            ctx.arc(0, -550, r, 0, 2 * math.pi)
            ctx.set_source_rgba(0.24, 0.73, 0.31, 0.6)
            ctx.set_line_width(3)
            ctx.stroke()
            ctx.restore()
        a = t * 3
        stroke(ctx, [(0, -550), (118 * math.cos(a), -550 + 118 * math.sin(a))], 6, color=hexc("#3fb950"))
        for k in range(3):
            flat(ctx, lambda c, k=k: p_ellipse(c, -60 + k * 50, -580 + k * 30, 8, 8), hexc("#7cff8a"))
    else:
        rg = _rng(int(t * 15))
        for k in range(60):
            x, y = rg.uniform(-110, 110), rg.uniform(-110, 110)
            if x * x + y * y < 110 * 110:
                flat(ctx, lambda c, x=x, y=y: c.rectangle(x, -550 + y, 8, 4), hexc("#9aa3ab"))
    for hx in (-190, 190):
        ctx.save()
        ctx.new_path()
        ctx.arc(hx, -400, 50, math.pi, 2 * math.pi)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(14)
        ctx.stroke()
        ctx.restore()
        for sx in (-50, 50):
            shape(ctx, lambda c, hx=hx, sx=sx: p_ellipse(c, hx + sx, -400, 20, 24), hexc("#3a3f48"), OUT * 0.5, None)


def tp_gymbag(ctx, t, p):
    """A gym bag (feet y 0, 340 wide) with a strap and a zip; p dust 0..1 a couple of dust motes and a cobweb."""
    stroke(ctx, [(-110, -150), (-60, -260), (60, -260), (110, -150)], 12, smooth=True)
    shape(ctx, lambda c: p_rrect(c, -170, -170, 340, 170, 70), hexc("#3b7dd8"), OUT, (0.03, 0.1))
    stroke(ctx, [(-120, -160), (120, -160)], 6, color=hexc("#e8eef4"))
    flat(ctx, lambda c: p_rrect(c, -40, -110, 80, 40, 10), hexc("#e8eef4"))
    d = p.get("dust", 0.0)
    if d > 0.01:
        for k in range(5):
            u = (t * 0.3 + k / 5) % 1.0
            flat(ctx, lambda c, k=k, u=u: p_ellipse(c, -120 + k * 60, -200 - 160 * u, 6, 6), hexc("#d9d0b4"),
                 a=d * (1 - u))
        for r in (30, 60):
            ctx.save()
            ctx.new_path()
            ctx.arc(170, -170, r, math.pi / 2, math.pi)
            ctx.set_source_rgba(1, 1, 1, 0.8 * d)
            ctx.set_line_width(3)
            ctx.stroke()
            ctx.restore()


def tp_toaster(ctx, t, p):
    """A toaster (feet y 0, 260 wide, 190 tall) with a cord running left p cord px to a wall outlet; p pull 0..1
    the plug comes out of the outlet and dangles."""
    cord = p.get("cord", 360)
    pull = ease(min(1.0, p.get("pull", 0.0)))
    ox, oy = -cord, -140
    shape(ctx, lambda c: p_rrect(c, ox - 34, oy - 50, 68, 100, 10), (1, 1, 1), OUT * 0.7, None)
    for dy in (-20, 20):
        flat(ctx, lambda c, dy=dy: c.rectangle(ox - 14, oy + dy - 4, 28, 8), INK)
    px, py = ox + 60 + 40 * pull, oy + 140 * pull
    stroke(ctx, [(-130, -40), ((px - 130) / 2, -10 + 40 * pull), (px, py)], 8, smooth=True)
    shape(ctx, lambda c: p_rrect(c, px - 14, py - 26, 42, 52, 8), hexc("#3a3f48"), OUT * 0.5, None)
    if pull > 0.3:
        for k in (-1, 1):
            stroke(ctx, [(px - 14, py + k * 12), (px - 34, py + k * 12)], 5, color=hexc("#c8ccd4"))
    shape(ctx, lambda c: p_rrect(c, -130, -190, 260, 190, 40), hexc("#c8ccd4"), OUT, (0.03, 0.1), (0.25, 0.2, 0.2))
    for x in (-50, 40):
        flat(ctx, lambda c, x=x: p_rrect(c, x - 30, -196, 60, 14, 6), INK)
    shape(ctx, lambda c: p_rrect(c, 110, -120, 40, 22, 6), INK, 0, None)


def tp_bed(ctx, t, p):
    """A bed seen from the side (feet y 0, 760 wide, mattress top y -260): headboard on the left, a pillow, a
    blanket; p col blanket colour."""
    shape(ctx, lambda c: p_rrect(c, -400, -560, 60, 560, 16), C["wood_dk"], OUT, None)
    shape(ctx, lambda c: p_rrect(c, 340, -330, 40, 330, 12), C["wood_dk"], OUT, None)
    shape(ctx, lambda c: c.rectangle(-350, -200, 700, 120), C["wood"], OUT, None)
    shape(ctx, lambda c: p_rrect(c, -350, -270, 700, 90, 24), (1, 1, 1), OUT, None)
    shape(ctx, lambda c: p_rrect(c, -330, -340, 220, 90, 40), hexc("#f4ecd6"), OUT, (0.03, 0.1))
    shape(ctx, lambda c: p_rrect(c, -60, -290, 430, 110, 30), hexc(p.get("col", "#3b7dd8")), OUT, (0.03, 0.1))


ACTORS.update({"tp_board": tp_board, "tp_seats": tp_seats, "tp_suitcase": tp_suitcase, "tp_pretzel": tp_pretzel,
               "tp_usmap": tp_usmap, "tp_tower": tp_tower, "tp_static": tp_static, "tp_radar": tp_radar,
               "tp_gymbag": tp_gymbag, "tp_toaster": tp_toaster, "tp_bed": tp_bed})
SCENES.update({"tp_gate": tp_gate})


def tp_plane(ctx, t, p):
    """One plain white airliner in level flight, centred at its origin (about 480 wide); p flip faces it left; it
    bobs gently. No livery, no names."""
    y = 6 * math.sin(t * 2)
    _plane(ctx, 0, y, 1.0, 0.0, flip=bool(p.get("flip")))
    if p.get("lights"):   # navigation and beacon lights blink
        on = math.sin(t * 5) > 0
        sx = -1 if p.get("flip") else 1
        flat(ctx, lambda c: p_ellipse(c, -60 * sx, y + 70, 10, 10), C["red"], a=1.0 if on else 0.4)
        flat(ctx, lambda c: p_ellipse(c, 20 * sx, y + 70, 10, 10), C["green"], a=0.4 if on else 1.0)
        flat(ctx, lambda c: p_ellipse(c, -210 * sx, y - 120, 9, 9), (1, 1, 1), a=1.0 if on else 0.3)


ACTORS.update({"tp_plane": tp_plane})


# ================================================================================================ ground stop update

def tp_mailbox(ctx, t, p):
    """A tiny mailbox on a short post (feet y 0, about 200 tall) with a red flag; p drop 0..1 an envelope drops in
    and the flag pops up."""
    stroke(ctx, [(0, 0), (0, -90)], 14, color=C["wood_dk"])
    shape(ctx, lambda c: p_smooth(c, [(-70, -90), (-70, -170), (0, -200), (70, -170), (70, -90)]), hexc("#3b7dd8"),
          OUT, (0.03, 0.1))
    dr = p.get("drop", 0.0)
    fl = 0.0 if dr < 0.8 else 1.0
    ctx.save()
    ctx.translate(70, -130)
    ctx.rotate(-math.pi / 2 * fl)
    shape(ctx, lambda c: c.rectangle(0, -6, 60, 12), C["pen"], OUT * 0.5, None)
    shape(ctx, lambda c: c.rectangle(44, -26, 22, 26), C["pen"], OUT * 0.5, None)
    ctx.restore()
    if 0.01 < dr < 0.8:
        u = dr / 0.8
        y = -420 + 260 * ease(u)
        ctx.save()
        ctx.translate(0, y)
        ctx.rotate(0.3 * math.sin(t * 6))
        shape(ctx, lambda c: c.rectangle(-50, -32, 100, 64), hexc("#f4ecd6"), OUT * 0.6, None)
        stroke(ctx, [(-50, -32), (0, 4), (50, -32)], OUT * 0.5)
        ctx.restore()


def tp_quilt(ctx, t, p):
    """A patchwork blanket lying flat over someone, origin = its bottom centre, p w x p h (default 640 x 110)."""
    w, h = p.get("w", 640), p.get("h", 110)
    wob = 4 * math.sin(t * 2)

    def path(c):
        p_smooth(c, [(-w / 2, 0), (-w / 2 + 20, -h + wob), (0, -h - 20 + wob), (w / 2 - 20, -h + wob), (w / 2, 0)])
    shape(ctx, path, C["q2"], OUT, None)
    ctx.save()
    path(ctx)
    ctx.clip()
    cols = [C["q1"], C["q3"], C["q4"], C["q2"]]
    for i in range(-8, 9):
        for j in range(0, 3):
            if (i + j) % 2:
                flat(ctx, lambda c, i=i, j=j: c.rectangle(i * 60 - 30, -h - 20 + j * 60, 60, 60), cols[(i * 3 + j) % 4])
    ctx.restore()
    ctx.save()
    path(ctx)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(OUT)
    ctx.stroke()
    ctx.restore()


def tp_vending(ctx, t, p):
    """A plain vending machine (feet y 0, 340 wide, 720 tall): glass front with rows of plain snacks, a slot, a
    small lit panel; no brand."""
    shape(ctx, lambda c: p_rrect(c, -170, -720, 340, 720, 20), hexc("#3b4a6b"), OUT, (0.03, 0.06))
    flat(ctx, lambda c: p_rrect(c, -140, -690, 210, 520, 12), hexc("#bfe6f8"))
    cols = [C["q1"], C["q3"], C["q4"], hexc("#ff9f6a")]
    for r in range(5):
        stroke(ctx, [(-135, -600 + r * 100), (65, -600 + r * 100)], 5, color=hexc("#8d969c"))
        for k in range(4):
            shape(ctx, lambda c, r=r, k=k: p_rrect(c, -125 + k * 48, -660 + r * 100, 36, 56, 6), cols[(r + k) % 4],
                  OUT * 0.4, None)
    flat(ctx, lambda c: p_rrect(c, 85, -660, 60, 90, 8), hexc("#16203a"))
    flat(ctx, lambda c: p_rrect(c, 95, -650, 40, 30, 4), hexc("#3fb950"), a=0.6 + 0.4 * math.sin(t * 3))
    for k in range(3):
        for j in range(3):
            flat(ctx, lambda c, k=k, j=j: p_ellipse(c, 100 + j * 15, -540 + k * 18, 5, 5), hexc("#c8ccd4"))
    flat(ctx, lambda c: p_rrect(c, -130, -130, 190, 60, 10), hexc("#16203a"))


def tp_status(ctx, t, p):
    """A phone held up showing a generic flight-status screen (no airline name): a plane icon, three status rows
    with bars, the first with a red X badge; p on 0..1 pops it in."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    sc = back_out(min(1.0, on))
    ctx.save()
    ctx.scale(sc, sc)
    ctx.rotate(math.radians(p.get("rot", -6)))
    shape(ctx, lambda c: p_rrect(c, -130, -240, 260, 480, 36), hexc("#1d1d24"), OUT, None)
    flat(ctx, lambda c: p_rrect(c, -110, -210, 220, 420, 20), hexc("#eef3f8"))
    _plane(ctx, 0, -150, 0.3)
    for k in range(3):
        y = -60 + k * 80
        flat(ctx, lambda c, y=y: p_rrect(c, -95, y - 28, 190, 56, 10), (1, 1, 1))
        flat(ctx, lambda c, y=y: c.rectangle(-80, y - 10, 100, 10), hexc("#7a8a9c"))
        flat(ctx, lambda c, y=y: c.rectangle(-80, y + 6, 60, 8), hexc("#b7c1cc"))
        col = C["pen"] if k == 0 else hexc("#ffb02e")
        shape(ctx, lambda c, y=y, col=col: p_ellipse(c, 65, y, 18, 18), col, OUT * 0.4, None)
        if k == 0:
            stroke(ctx, [(57, y - 8), (73, y + 8)], 5, color=(1, 1, 1))
            stroke(ctx, [(73, y - 8), (57, y + 8)], 5, color=(1, 1, 1))
    ctx.restore()


def tp_buzz(ctx, t, p):
    """Vibration marks round the origin (a buzzing phone): two arcs each side that pulse; p on 0..1."""
    on = p.get("on", 1.0)
    if on <= 0.01 or math.sin(t * 9) < -0.3:
        return
    for sd in (-1, 1):
        for r in (60, 90):
            ctx.save()
            ctx.new_path()
            a0 = 0 if sd > 0 else math.pi
            ctx.arc(0, 0, r, a0 - 0.5, a0 + 0.5)
            ctx.set_source_rgba(*INK, 0.8 * on)
            ctx.set_line_width(7)
            ctx.stroke()
            ctx.restore()


ACTORS.update({"tp_mailbox": tp_mailbox, "tp_quilt": tp_quilt, "tp_vending": tp_vending, "tp_status": tp_status,
               "tp_buzz": tp_buzz})


# ================================================================================================ ground stop lifted

def tp_cabin(ctx, t, layer, p):
    """A plain airliner cabin seen side-on: curved pale wall with a row of oval windows (night sky outside), an
    overhead bin band, a bathroom door at x 860..1060 with a small round person icon (no words), carpet aisle at
    y 1500."""
    layer(0.9)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), hexc("#e8eef4"))
    flat(ctx, lambda c: c.rectangle(-3000, 380, 8000, 160), hexc("#cfd6de"))
    stroke(ctx, [(-3000, 540), (5000, 540)], BG_OUT)
    for k in range(-6, 12):
        x = k * 200
        shape(ctx, lambda c, x=x: p_ellipse(c, x, 860, 50, 70), hexc("#141c33"), BG_OUT, None)
        flat(ctx, lambda c, x=x: p_ellipse(c, x + 12, 840, 6, 6), (1, 1, 1), a=0.7)
    layer(1.0)
    shape(ctx, lambda c: c.rectangle(860, 640, 200, 860), hexc("#c8ccd4"), OUT, (0.03, 0.06))
    shape(ctx, lambda c: p_ellipse(c, 960, 760, 34, 34), hexc("#3b7dd8"), OUT * 0.5, None)
    flat(ctx, lambda c: p_ellipse(c, 960, 748, 8, 8), (1, 1, 1))
    flat(ctx, lambda c: p_rrect(c, 952, 758, 16, 22, 5), (1, 1, 1))
    shape(ctx, lambda c: p_rrect(c, 880, 1060, 28, 60, 8), hexc("#9aa3ab"), OUT * 0.5, None)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 3000), hexc("#3b4a6b"))
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)


def tp_cabinrow(ctx, t, p):
    """A row of p n plain airline seats seen from behind-side (feet y 0, each 220 wide, backs 520 tall); put it in
    front of someone sitting so only the head shows."""
    n = int(p.get("n", 3))
    w = 220
    x0 = -n * w / 2
    for k in range(n):
        x = x0 + k * w
        shape(ctx, lambda c, x=x: p_rrect(c, x + 12, -520, w - 24, 400, 40), hexc(p.get("col", "#3b4a6b")), OUT,
              (0.03, 0.08))
        shape(ctx, lambda c, x=x: p_rrect(c, x + 40, -560, w - 80, 70, 24), hexc("#e8eef4"), OUT * 0.7, None)
        shape(ctx, lambda c, x=x: c.rectangle(x + 20, -130, w - 40, 30), hexc("#2a3550"), OUT * 0.7, None)
        stroke(ctx, [(x + w / 2, -100), (x + w / 2, 0)], 12)


def tp_routers(ctx, t, p):
    """A wall rack of p n (default 6) plain routers on two shelves (feet y 0, 600 wide), lights blinking out of
    sync; p sync 0..1 brings them back in step."""
    sy = p.get("sync", 0.0)
    for r in range(2):
        y = -60 - r * 260
        shape(ctx, lambda c, y=y: c.rectangle(-300, y, 600, 22), C["steel_dk"], OUT * 0.7, None)
        for k in range(3):
            x = -200 + k * 200
            for sx_ in (-50, 50):
                stroke(ctx, [(x + sx_, y - 100), (x + sx_ * 1.3, y - 200)], 10, color=hexc("#3a3f48"))
            shape(ctx, lambda c, x=x, y=y: p_rrect(c, x - 85, y - 100, 170, 100, 16), C["router"], OUT * 0.8, None)
            for j in range(4):
                ph = (1 - sy) * (k * 1.9 + r * 2.7 + j * 0.8)
                on = math.sin(t * (6 + (1 - sy) * (k + r)) + ph) > 0
                flat(ctx, lambda c, x=x, y=y, j=j: p_ellipse(c, x - 50 + j * 33, y - 50, 9, 9),
                     hexc("#3fb950") if on else hexc("#9aa3ab"))


def tp_plug(ctx, t, p):
    """A pulled plug held up at its origin, its cord hanging down to the floor p len px below."""
    ln = p.get("len", 200)
    stroke(ctx, [(0, 20), (-30, ln * 0.5), (10, ln)], 8, smooth=True)
    shape(ctx, lambda c: p_rrect(c, -22, -30, 44, 56, 8), hexc("#3a3f48"), OUT * 0.6, None)
    for dx in (-10, 10):
        stroke(ctx, [(dx, -30), (dx, -58)], 6, color=hexc("#c8ccd4"))


def tp_flipphone(ctx, t, p):
    """An old flip phone, open, centred at its origin (110 x 260): a tiny screen, number keys as dots, a stubby
    antenna."""
    ctx.save()
    ctx.rotate(math.radians(p.get("rot", -10)))
    stroke(ctx, [(35, -130), (35, -175)], 10)
    shape(ctx, lambda c: p_rrect(c, -55, -130, 110, 125, 16), hexc("#8d969c"), OUT * 0.7, None)
    flat(ctx, lambda c: p_rrect(c, -38, -112, 76, 70, 6), hexc("#9fd3a0"))
    shape(ctx, lambda c: p_rrect(c, -55, 0, 110, 130, 16), hexc("#8d969c"), OUT * 0.7, None)
    for r in range(4):
        for k in range(3):
            flat(ctx, lambda c, r=r, k=k: p_ellipse(c, -28 + k * 28, 24 + r * 26, 8, 6), hexc("#3a3f48"))
    ctx.restore()


ACTORS.update({"tp_cabinrow": tp_cabinrow, "tp_routers": tp_routers, "tp_plug": tp_plug, "tp_flipphone": tp_flipphone})
SCENES.update({"tp_cabin": tp_cabin})
