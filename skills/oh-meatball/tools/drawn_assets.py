"""Scenes and actors for tools/drawn.py, all drawn in code in the drawn_kit style.

A SCENE draws a habitat in world units for a camera; it gets layer(depth) to set parallax (depth 1 = moves
with the camera, < 1 = far away, > 1 = foreground). An ACTOR draws one character or prop at the origin
(feet / base at y = 0) in local units; drawn.py has already translated, scaled and flipped the context.
Both receive t (seconds into the beat's shot) and the spec's params, so everything can move every frame.

Scenes:  basement, ocean, deep, office, press
Actors:  harvestman, cellar_spider, web, chair, arm, glomar, soviet_ship, sub, sub_bow, claw, us_sub,
         billionaire, burglar, papers, newspaper, spokesman, reporters, bubbles, debris, flashes
"""
import math
import random

from drawn_kit import (BG_OUT, INK, OUT, PAL, darker, ease, eyes, flat, hexc, ink, lighter, limb, mouth,
                       p_blob, p_ellipse, p_poly, p_rrect, p_smooth, shape, src, starburst, stroke, sweat,
                       motion_lines)

P = PAL


# ================================================================= scenes

def basement(ctx, t, layer, p):
    """A house basement corner, world 1600 x 1920, floor at y = 1500."""
    layer(0.82)
    flat(ctx, lambda c: c.rectangle(-600, -400, 2800, 1950), P["wall"])
    rng = random.Random(4)
    for row in range(17):
        y = 140 + row * 82
        off = (row % 2) * 105
        for col in range(-3, 14):
            x = col * 210 + off
            tone = P["wall"] if rng.random() < 0.6 else P["wall_dk"]
            ctx.save()
            p_rrect(ctx, x + 5, y + 5, 200, 72, 6)
            src(ctx, tone)
            ctx.fill_preserve()
            ink(ctx, 3.0, 0.35)
            ctx.stroke()
            ctx.restore()
    # joists + pipe
    flat(ctx, lambda c: c.rectangle(-600, -400, 2800, 540), P["wood_dk"], BG_OUT)
    for x in range(-500, 2700, 260):
        shape(ctx, lambda c, x=x: c.rectangle(x, -400, 70, 560), P["wood"], BG_OUT, (0.0, 0.0))
    shape(ctx, lambda c: p_rrect(c, -600, 175, 3400, 34, 17), P["pipe"], BG_OUT, (0, 0.25))
    for x in (120, 760, 1400):
        shape(ctx, lambda c, x=x: c.rectangle(x, 168, 26, 48), P["steel_dk"], BG_OUT * 0.8, None)
    # window + light beam
    shape(ctx, lambda c: c.rectangle(1080, 300, 300, 160), P["wood"], BG_OUT, None)
    shape(ctx, lambda c: c.rectangle(1100, 318, 260, 124), P["window"], BG_OUT * 0.8, None)
    stroke(ctx, [(1230, 318), (1230, 442)], BG_OUT * 0.8)
    layer(1.0)
    # stairs on the left
    for i in range(7):
        y = 640 + i * 125
        x = -260 + i * 85
        shape(ctx, lambda c, x=x, y=y: c.rectangle(x, y, 330, 36), P["wood"], BG_OUT, (0, 0.3))
    shape(ctx, lambda c: p_poly(c, [(-300, 560), (-200, 560), (420, 1500), (300, 1500)]), P["wood_dk"], BG_OUT,
          (0.1, 0))
    # floor
    flat(ctx, lambda c: c.rectangle(-600, 1480, 2800, 600), P["floor"], 0)
    flat(ctx, lambda c: c.rectangle(-600, 1480, 2800, 34), P["floor_dk"], 0)
    stroke(ctx, [(-600, 1482), (2800, 1482)], BG_OUT)
    for a, b in (((300, 1640), (520, 1700)), ((900, 1580), (1080, 1610)), ((1300, 1760), (1550, 1700))):
        stroke(ctx, [a, ((a[0] + b[0]) / 2, b[1] + 14), b], 3.5, smooth=True, a=0.5)
    # boxes stack, right
    shape(ctx, lambda c: p_rrect(c, 1330, 1180, 300, 310, 8), P["box"], BG_OUT, (0.14, 0.1))
    shape(ctx, lambda c: p_rrect(c, 1380, 960, 230, 225, 8), P["box"], BG_OUT, (0.14, 0.1))
    stroke(ctx, [(1330, 1300), (1630, 1300)], 4, color=P["box_dk"])
    stroke(ctx, [(1380, 1060), (1610, 1060)], 4, color=P["box_dk"])
    # hanging bulb, swaying
    sw = 0.07 * math.sin(t * 1.4)
    ctx.save()
    ctx.translate(640, 200)
    ctx.rotate(sw)
    stroke(ctx, [(0, 0), (0, 240)], 4)
    ctx.save()
    p_ellipse(ctx, 0, 300, 150, 150)
    src(ctx, P["glow"], 0.22)
    ctx.fill()
    ctx.restore()
    shape(ctx, lambda c: c.rectangle(-16, 236, 32, 30), P["steel"], OUT * 0.7, None)
    shape(ctx, lambda c: p_ellipse(c, 0, 296, 34, 40), P["bulb"], OUT * 0.7, None)
    ctx.restore()


def ocean(ctx, t, layer, p):
    """Open ocean surface, world x -400..2400, horizon y = 900; the sea goes down to 1920."""
    layer(0.3)
    bands = [P["sky2"], lighter(P["sky"], 0.2), P["sky"]]
    for i, c in enumerate(bands):
        flat(ctx, lambda cc, i=i: cc.rectangle(-3000, -2000 + i * 1000 if i else -3000, 8000, 6000), c)
    sky = p.get("sky")
    if sky == "sunset":
        for i, c in enumerate(("#ffd29a", "#ffb37a", "#f58c6a")):
            flat(ctx, lambda cc, i=i: cc.rectangle(-3000, -600 + i * 500 if i else -3000, 8000, 6000), hexc(c))
    if sky == "night":
        flat(ctx, lambda cc: cc.rectangle(-3000, -3000, 8000, 6000), P["night"])
    sun = P["sun"] if sky != "night" else hexc("#f4f1d0")
    sx = 1500 if sky != "sunset" else 900
    sy = 300 if sky != "sunset" else 820
    shape(ctx, lambda c: p_ellipse(c, sx, sy, 110, 110), sun, BG_OUT, None)
    layer(0.5)
    for i, (x, y, s) in enumerate(((100, 260, 1.0), (900, 160, 0.8), (1900, 330, 1.2), (2700, 200, 0.9))):
        x = x + (t * 18 * s) % 3200 - 400
        for dx, dy, r in ((-90, 10, 70), (0, -30, 95), (100, 5, 75), (30, 30, 80)):
            shape(ctx, lambda c, dx=dx, dy=dy, r=r: p_ellipse(c, x + dx * s, y + dy * s, r * s, r * s * 0.8),
                  P["cloud"], BG_OUT * 0.8, (0, 0.18), shade_k=0.92)
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 900, 8400, 1400), P["sea"])
    flat(ctx, lambda c: c.rectangle(-3000, 1420, 8400, 1400), P["sea2"])
    flat(ctx, lambda c: c.rectangle(-3000, 1720, 8400, 1400), P["sea_dk"])
    stroke(ctx, [(-2000, 900), (4400, 900)], BG_OUT)
    for row in range(6):
        y = 960 + row * 160
        ph = t * (1.2 + row * 0.2) + row
        pts = [(x, y + 10 * math.sin(x / 90 + ph)) for x in range(-2000, 4400, 60)]
        stroke(ctx, pts, 4 + row, color=P["foam"], a=0.55)


def deep(ctx, t, layer, p):
    """The deep sea in cross-section: world y 0 (surface glow) .. 9000 (sea floor at ~8600)."""
    layer(1.0)
    cols = [P["deep1"], P["deep2"], P["deep3"], P["deep4"], P["deep5"]]
    for i, c in enumerate(cols):
        flat(ctx, lambda cc, i=i: cc.rectangle(-3000, -2000 + i * 2200 if i else -3000, 8000, 2400 if i else 3400),
             c)
    # light rays near the surface
    for i in range(4):
        x = -200 + i * 420 + 40 * math.sin(t * 0.5 + i)
        ctx.save()
        p_poly(ctx, [(x, -400), (x + 160, -400), (x + 420, 2200), (x + 200, 2200)])
        src(ctx, (1, 1, 1), 0.06)
        ctx.fill()
        ctx.restore()
    # marine snow drifting
    rng = random.Random(9)
    for _ in range(420):
        x, y = rng.uniform(-1500, 3000), rng.uniform(-500, 9000)
        y = (y + t * 25) % 9500 - 500
        r = rng.uniform(2, 6)
        p_ellipse(ctx, x + 8 * math.sin(t + y), y, r, r)
        src(ctx, (1, 1, 1), 0.35)
        ctx.fill()
    # sea floor
    floor = 8600
    pts = [(x, floor + 40 * math.sin(x / 260) + 18 * math.sin(x / 90)) for x in range(-3000, 5000, 80)]
    ctx.save()
    p_poly(ctx, pts + [(5000, 12000), (-3000, 12000)])
    src(ctx, P["sand"])
    ctx.fill_preserve()
    ink(ctx, BG_OUT)
    ctx.stroke()
    ctx.restore()
    for x, s in ((-300, 1.0), (350, 0.7), (1400, 1.3), (2100, 0.8)):
        shape(ctx, lambda c, x=x, s=s: p_blob(c, x, floor + 10, 140 * s, 70 * s, 0.12, seed=int(x)), P["rock"],
              BG_OUT, (0.1, 0.2))


def office(ctx, t, layer, p):
    """A company office at night, world 1600 x 1920, floor y = 1540, window with palms and city lights."""
    layer(0.85)
    flat(ctx, lambda c: c.rectangle(-600, -400, 2800, 2400), P["office"])
    for x in range(-600, 2800, 160):
        flat(ctx, lambda c, x=x: c.rectangle(x, -400, 80, 1940), P["office_dk"])
    # window
    shape(ctx, lambda c: c.rectangle(720, 300, 720, 620), P["desk_dk"], BG_OUT, None)
    flat(ctx, lambda c: c.rectangle(745, 325, 670, 570), P["night"])
    flat(ctx, lambda c: c.rectangle(745, 700, 670, 195), P["night2"])
    rng = random.Random(3)
    for _ in range(26):
        x, y = rng.uniform(760, 1400), rng.uniform(720, 880)
        flat(ctx, lambda c, x=x, y=y: c.rectangle(x, y, 10, 14), P["light"], a=0.8)
    flat(ctx, lambda c: p_ellipse(c, 1300, 420, 46, 46), hexc("#f4f1d0"))
    for px, h in ((860, 420), (1250, 360)):
        stroke(ctx, [(px, 895), (px + 20, 895 - h * 0.5), (px + 10, 895 - h)], 16, smooth=True, color=P["palm"])
        for a in range(6):
            ang = -math.pi + a * math.pi / 5
            stroke(ctx, [(px + 10, 895 - h), (px + 10 + 110 * math.cos(ang), 895 - h + 70 * math.sin(ang) + 40)],
                   12, smooth=True, color=P["palm"])
    stroke(ctx, [(1080, 300), (1080, 920)], BG_OUT)
    stroke(ctx, [(720, 610), (1440, 610)], BG_OUT)
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-600, 1540, 2800, 600), P["carpet"])
    stroke(ctx, [(-600, 1540), (2800, 1540)], BG_OUT)
    # filing cabinets
    for x in (-40, 250):
        shape(ctx, lambda c, x=x: p_rrect(c, x, 840, 260, 700, 8), P["cabinet"], BG_OUT, (0.12, 0))
        for k in range(4):
            y = 870 + k * 168
            shape(ctx, lambda c, x=x, y=y: p_rrect(c, x + 22, y, 216, 140, 6), P["cabinet"], BG_OUT * 0.8, None)
            shape(ctx, lambda c, x=x, y=y: p_rrect(c, x + 100, y + 20, 60, 18, 6), P["steel_dk"], 3, None)
    # safe
    shape(ctx, lambda c: p_rrect(c, 1450, 1180, 300, 360, 14), P["hull"], BG_OUT, (0.12, 0.1))
    shape(ctx, lambda c: p_ellipse(c, 1600, 1350, 60, 60), P["steel"], BG_OUT, None)


def press(ctx, t, layer, p):
    """A press briefing room: curtain, flags, podium with a round seal (no lettering). Floor y = 1600."""
    layer(0.8)
    flat(ctx, lambda c: c.rectangle(-800, -400, 3200, 2400), P["curtain"])
    for x in range(-800, 2400, 120):
        flat(ctx, lambda c, x=x: c.rectangle(x, -400, 50, 2400), P["curtain_dk"])
    # flags either side (stripes only)
    for fx in (120, 1320):
        stroke(ctx, [(fx, 500), (fx, 1600)], 12, color=P["seal"])
        ctx.save()
        ctx.translate(fx + 6, 520)
        w = 8 * math.sin(t * 2 + fx)
        for k in range(7):
            col = P["red"] if k % 2 == 0 else (1, 1, 1)
            flat(ctx, lambda c, k=k: p_poly(c, [(0, k * 40), (170, k * 40 + w), (170, k * 40 + 40 + w),
                                                  (0, k * 40 + 40)]), col)
        flat(ctx, lambda c: p_poly(c, [(0, 0), (80, 4), (80, 160), (0, 160)]), hexc("#2a3f86"))
        ink(ctx, BG_OUT)
        p_poly(ctx, [(0, 0), (170, w), (170, 280 + w), (0, 280)])
        ctx.stroke()
        ctx.restore()
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-800, 1600, 3200, 600), P["carpet"])
    stroke(ctx, [(-800, 1600), (2400, 1600)], BG_OUT)


SCENES = {"basement": basement, "ocean": ocean, "deep": deep, "office": office, "press": press}
