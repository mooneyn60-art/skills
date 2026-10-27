#!/usr/bin/env python3
"""History-case cast for tools/drawn.py ("Meatball Investigates" TikTok cuts), in the drawn_kit style.
Generic drawn people and things only: no real person's likeness, no lettering anywhere.

This file registers itself without touching the shared tools: run a spec through it instead of drawn.py
  python3 tools/drawn_cases2.py SPEC.json OUT.mp4 [--work DIR] [--stills 1,5,9]
and it adds its actors and scenes to drawn.ACTORS / drawn.SCENES, then hands over to drawn.main().
drawn_quick.py --no-render still writes and length-checks the spec (it never draws a frame).

Scenes (floor y = 1500): night_sea (p: day, storm), radar_room, isle (storm clifftop), keeper_room,
  tundra, classroom, village (p: school = draw the school house, locked)
Actors: destroyer (fire, light), torpedo_boat (ghost, wake), operator (person + headphones + radar console;
  blips, ghost, sweat), jet, tv (show: podium | flames), lighthouse (lit), isle_rock (lit), big_wave (rise),
  steamer (flare), keeper (oilskin person), coat_pegs (coats), wall_clock, drill_rig, section (depth 0..1,
  fossils, heat), well_cap, mic_cable, student (laugh 0..1, cry), desks, hut
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from drawn_kit import BG_OUT, INK, OUT, PAL, darker, flat, hexc, ink, lighter, limb, p_blob, p_ellipse, \
    p_poly, p_rrect, p_smooth, shape, src, starburst, stroke  # noqa: E402
from drawn_cast import person  # noqa: E402

P = PAL
NAVY = hexc("#5d6873")
NAVY_DK = hexc("#46505a")
YEL = hexc("#f2c230")
GREEN = hexc("#5dff8a")


def _sea_strip(ctx, t, w=900, y=30, amp=10, color=None):
    pts = [(x, y + amp * math.sin(x / 70 + t * 2.6)) for x in range(-w, w + 60, 50)]
    ctx.save()
    p_poly(ctx, pts + [(w, 260), (-w, 260)])
    src(ctx, color or P["sea_dk"])
    ctx.fill()
    ctx.restore()
    stroke(ctx, pts, 7, color=P["foam"], a=0.8)


# ================================================================= scenes

def night_sea(ctx, t, layer, p):
    day = p.get("day")
    storm = p.get("storm")
    layer(0.3)
    sky = hexc("#8fd3f4") if day else (hexc("#151b30") if storm else hexc("#1b2440"))
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), sky)
    if not day:
        rng = random.Random(3)
        for _ in range(60 if not storm else 0):
            x, y = rng.uniform(-600, 1700), rng.uniform(-300, 1000)
            flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 4, 4), (1, 1, 1), a=0.5 + 0.4 * math.sin(t * 2 + x))
        if storm:
            for i, x0 in enumerate((-200, 500, 1200)):
                x = x0 + (t * 25) % 1800 - 300
                flat(ctx, lambda c, x=x: p_blob(c, x, 250, 520, 170, 0.1, seed=int(x0)), hexc("#262c44"))
    else:
        shape(ctx, lambda c: p_ellipse(c, 1100, 250, 110, 110), P["sun"], BG_OUT, None)
    layer(0.6)
    sea = hexc("#2f7fc0") if day else hexc("#16294a")
    flat(ctx, lambda c: c.rectangle(-3000, 1100, 8000, 3000), sea)
    stroke(ctx, [(-3000, 1100), (5000, 1100)], BG_OUT)
    layer(1.0)
    for row in range(7):
        y = 1150 + row * 120
        amp = (22 if storm else 8) + row * 2
        pts = [(x, y + amp * math.sin(x / 90 + t * (1.3 + row * 0.2) + row)) for x in range(-1500, 3000, 60)]
        stroke(ctx, pts, 5 + row, color=P["foam"], a=0.25 + 0.06 * row)
    if storm:
        rng = random.Random(9)
        for _ in range(70):
            x, y = rng.uniform(-400, 1500), rng.uniform(-200, 2000)
            y = (y + t * 1400) % 2200 - 200
            stroke(ctx, [(x, y), (x - 30, y + 90)], 4, color=(0.8, 0.85, 1.0), a=0.35)


def radar_room(ctx, t, layer, p):
    layer(0.5)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), hexc("#2c3a3a"))
    for x in range(-600, 2200, 260):
        flat(ctx, lambda c, x=x: c.rectangle(x, -2000, 12, 3600), hexc("#243030"))
        for y in range(-200, 1500, 140):
            flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x + 40, y, 7, 7), hexc("#1d2727"))
    for y in (180, 260):
        stroke(ctx, [(-1500, y), (3000, y)], 26, color=hexc("#506060"))
    glow = 0.5 + 0.5 * math.sin(t * 2.0)
    shape(ctx, lambda c: p_ellipse(c, 540, 330, 50, 50), hexc("#d8322a"), BG_OUT, None)
    flat(ctx, lambda c: p_ellipse(c, 540, 330, 160, 160), hexc("#ff3a2a"), a=0.12 + 0.08 * glow)
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 1000), hexc("#3a4646"))
    for x in range(-1500, 3000, 120):
        stroke(ctx, [(x, 1500), (x - 60, 2100)], 4, color=hexc("#2e3838"))
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)
    ctx.save()   # red night lighting over everything
    ctx.identity_matrix()
    ctx.rectangle(0, 0, 1080, 1920)
    src(ctx, (0.35, 0.05, 0.05), 0.12)
    ctx.fill()
    ctx.restore()


def isle(ctx, t, layer, p):
    layer(0.3)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), hexc("#3d4656"))
    for i, x0 in enumerate((-300, 400, 1100, 1800)):
        x = x0 + (t * 40) % 2000 - 500
        flat(ctx, lambda c, x=x, i=i: p_blob(c, x, 200 + 60 * (i % 2), 480, 150, 0.12, seed=i), hexc("#2c3342"))
    layer(0.5)
    flat(ctx, lambda c: c.rectangle(-3000, 1050, 8000, 3000), hexc("#24364f"))
    for row in range(3):
        pts = [(x, 1090 + row * 60 + 14 * math.sin(x / 70 + t * 2 + row)) for x in range(-1500, 3000, 50)]
        stroke(ctx, pts, 6, color=P["foam"], a=0.5)
    layer(1.0)
    ground = lambda c: p_poly(c, [(-3000, 1500), (-3000, 1330), (-200, 1380), (400, 1430), (1200, 1440),  # noqa: E731
                                  (2200, 1360), (4000, 1350), (4000, 2600), (-3000, 2600)])
    shape(ctx, ground, hexc("#55704a"), BG_OUT, (0, 0.1))
    flat(ctx, lambda c: c.rectangle(-3000, 1560, 8000, 1200), hexc("#6b6760"))
    for x in range(-1500, 3000, 90):
        stroke(ctx, [(x, 1500), (x + 18 * math.sin(t * 3 + x), 1440)], 9, color=hexc("#3f5a37"))
    rng = random.Random(5)
    for _ in range(80):
        x, y = rng.uniform(-400, 1500), rng.uniform(-200, 2000)
        y = (y + t * 1300) % 2200 - 200
        stroke(ctx, [(x, y), (x - 40, y + 90)], 4, color=(0.8, 0.85, 1.0), a=0.3)


def keeper_room(ctx, t, layer, p):
    layer(0.6)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), hexc("#e6e0cf"))
    for y in range(-400, 1500, 150):
        stroke(ctx, [(-2000, y), (3000, y)], 4, color=hexc("#d3ccb8"))
    shape(ctx, lambda c: p_rrect(c, 40, 380, 300, 380, 20), hexc("#22305a"), BG_OUT, None)   # window, storm outside
    stroke(ctx, [(190, 380), (190, 760)], 12)
    stroke(ctx, [(40, 570), (340, 570)], 12)
    rng = random.Random(2)
    for _ in range(12):
        x, y = rng.uniform(60, 320), rng.uniform(400, 740)
        y = 400 + (y - 400 + t * 400) % 340
        stroke(ctx, [(x, y), (x - 10, y + 30)], 3, color=(0.8, 0.85, 1.0), a=0.6)
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 1000), hexc("#8a6f55"))
    for x in range(-1500, 3000, 160):
        stroke(ctx, [(x, 1500), (x, 2100)], 4, color=hexc("#735a43"))
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)
    shape(ctx, lambda c: p_rrect(c, 1180, 1100, 420, 400, 14), hexc("#3a3a3a"), BG_OUT, (0.1, 0))   # stove
    shape(ctx, lambda c: c.rectangle(1240, 1180, 160, 110), hexc("#1d1d1d"), BG_OUT * 0.7, None)


def tundra(ctx, t, layer, p):
    layer(0.3)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), hexc("#c7d3dc"))
    flat(ctx, lambda c: c.rectangle(-3000, 700, 8000, 600), hexc("#d9e2e8"))
    layer(0.5)
    shape(ctx, lambda c: p_poly(c, [(-2000, 1250), (-600, 950), (200, 1150), (900, 980), (1800, 1200),
                                    (3000, 1000), (3000, 1300), (-2000, 1300)]), hexc("#9aa8b4"), BG_OUT, None)
    for x in (-300, 1500):
        shape(ctx, lambda c, x=x: c.rectangle(x, 1060, 220, 200), hexc("#9b5a3c"), BG_OUT, None)
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1300, 8000, 1400), hexc("#f2f5f7"))
    stroke(ctx, [(-3000, 1300), (5000, 1300)], BG_OUT)
    rng = random.Random(1)
    for _ in range(40):
        x, y = rng.uniform(-1000, 2200), rng.uniform(1340, 2000)
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 40, 8), hexc("#dfe7ec"))
    for _ in range(50):
        x, y = rng.uniform(-400, 1500), rng.uniform(-200, 2000)
        y = (y + t * 160) % 2200 - 200
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x + 20 * math.sin(t + y), y, 7, 7), (1, 1, 1), a=0.85)


def classroom(ctx, t, layer, p):
    layer(0.6)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), hexc("#e8c98a"))
    flat(ctx, lambda c: c.rectangle(-3000, 1050, 8000, 600), hexc("#c98f5a"))
    shape(ctx, lambda c: p_rrect(c, 120, 330, 780, 480, 10), hexc("#2f4f3a"), BG_OUT * 1.4, None)   # chalkboard
    for k in range(4):   # chalk scribbles, no letters
        stroke(ctx, [(180 + 40 * k, 420 + 90 * k) if i == 0 else (180 + 40 * k + i * 60, 420 + 90 * k + 18 * math.sin(i))
                     for i in range(8)], 6, color=(0.95, 0.95, 0.9), a=0.8)
    for x in (-420, 1080):
        shape(ctx, lambda c, x=x: p_rrect(c, x, 330, 300, 420, 10), hexc("#9fd3ee"), BG_OUT, None)
        stroke(ctx, [(x + 150, 330), (x + 150, 750)], 10)
        flat(ctx, lambda c, x=x: p_ellipse(c, x + 230, 420, 40, 40), P["sun"])
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 1000), hexc("#9a6e44"))
    for y in range(1500, 2100, 70):
        stroke(ctx, [(-3000, y), (5000, y)], 4, color=hexc("#845a35"))
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)


def village(ctx, t, layer, p):
    layer(0.3)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), hexc("#9fdcf6"))
    shape(ctx, lambda c: p_ellipse(c, 1150, 260, 110, 110), P["sun"], BG_OUT, None)
    flat(ctx, lambda c: c.rectangle(-3000, 1000, 8000, 300), hexc("#3d8fc4"))   # the lake
    stroke(ctx, [(-3000, 1000), (5000, 1000)], BG_OUT * 0.8)
    layer(0.6)
    for x in (-500, 60, 1400, 1900):
        _banana(ctx, x, 1300, 1.0, t)
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1280, 8000, 1400), hexc("#c88d5a"))
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 1200), hexc("#b97a48"))
    stroke(ctx, [(-3000, 1280), (5000, 1280)], BG_OUT)
    if p.get("school"):
        school(ctx, 540, 1500, 1.0, t, p.get("locked", 0.0))
    for x, s in p.get("huts", []):
        ctx.save()
        ctx.translate(x, 1500)
        ctx.scale(s, s)
        hut(ctx, t, {})
        ctx.restore()


def _banana(ctx, x, y, s, t):
    stroke(ctx, [(x, y), (x + 10, y - 520 * s)], 40 * s, color=hexc("#7a6a3a"))
    for k in range(6):
        a = -math.pi / 2 + (k - 2.5) * 0.5 + 0.05 * math.sin(t * 1.5 + k)
        ex, ey = x + 10 + 360 * s * math.cos(a), y - 520 * s + 260 * s * math.sin(a) + 80
        shape(ctx, lambda c, ex=ex, ey=ey: p_poly(c, [(x + 10, y - 520 * s), ((x + 10 + ex) / 2, (y - 560 * s + ey) / 2 - 60),
                                                    (ex, ey)]), hexc("#4f9a3d"), BG_OUT * 0.8, None)


def school(ctx, x, y, s, t, locked):
    shape(ctx, lambda c: c.rectangle(x - 520, y - 520, 1040, 520), hexc("#f0e2c0"), BG_OUT, (0.1, 0))
    shape(ctx, lambda c: p_poly(c, [(x - 600, y - 500), (x, y - 780), (x + 600, y - 500)]), hexc("#9aa3ab"),
          BG_OUT, (0, 0.15))
    for xx in (x - 400, x - 230, x + 230, x + 400):
        shape(ctx, lambda c, xx=xx: c.rectangle(xx - 60, y - 400, 120, 120), hexc("#3a5a7a"), BG_OUT * 0.8, None)
    shape(ctx, lambda c: c.rectangle(x - 90, y - 320, 180, 320), hexc("#8a5a30"), BG_OUT, (0.1, 0))
    if locked > 0.01:
        stroke(ctx, [(x - 120, y - 200), (x + 120, y - 120)], 26, color=P["steel_dk"], a=locked)
        stroke(ctx, [(x + 120, y - 200), (x - 120, y - 120)], 26, color=P["steel_dk"], a=locked)
        shape(ctx, lambda c: p_rrect(c, x - 40, y - 190, 80, 70, 10), YEL, OUT * 0.6, None, a=locked)
        ctx.new_sub_path()
        ctx.arc(x, y - 190, 28, math.pi, 2 * math.pi)
        ink(ctx, 12, a=locked)
        ctx.stroke()


# ================================================================= actors

def destroyer(ctx, t, p):
    """A grey US destroyer side-on, bow to the right, waterline at y = 0. p: fire (0..1 muzzle flashes),
    light (searchlight sweep)."""
    bob = 7 * math.sin(t * 1.4)
    ctx.translate(0, bob)
    shape(ctx, lambda c: p_poly(c, [(-700, -120), (620, -150), (760, -190), (660, 40), (-660, 40)]), NAVY, OUT,
          (0, 0.18))
    shape(ctx, lambda c: p_rrect(c, -260, -330, 380, 210, 10), NAVY, OUT, (0.12, 0))
    shape(ctx, lambda c: p_rrect(c, 120, -440, 200, 320, 10), NAVY, OUT, (0.12, 0))
    for x in (140, 200, 260):
        shape(ctx, lambda c, x=x: c.rectangle(x - 18, -410, 36, 30), P["window"], OUT * 0.5, None)
    for x in (-160, 0):
        shape(ctx, lambda c, x=x: p_rrect(c, x - 40, -470, 80, 150, 12), NAVY_DK, OUT * 0.8, None)
    stroke(ctx, [(230, -440), (230, -720)], 10)
    stroke(ctx, [(170, -650), (290, -650)], 8)
    for gx, d in ((480, 1), (-520, -1)):
        shape(ctx, lambda c, gx=gx: p_rrect(c, gx - 70, -230, 140, 90, 30), NAVY_DK, OUT * 0.8, None)
        stroke(ctx, [(gx + 50 * d, -200), (gx + 220 * d, -230)], 16)
    flat(ctx, lambda c: c.rectangle(-660, 0, 1330, 30), hexc("#a83a30"))
    fire = p.get("fire", 0.0)
    if fire > 0.01:
        for k, (gx, d) in enumerate(((480, 1), (-520, -1))):
            u = (t * 3 + k * 0.5) % 1
            if u < 0.35:
                starburst(ctx, gx + 250 * d, -232, 70 * fire * (1 - u), n=9)
    if p.get("light"):
        a = 0.25 + 0.15 * math.sin(t * 3)
        ctx.save()
        p_poly(ctx, [(230, -700), (1400, -900 + 300 * math.sin(t * 0.8)), (1400, -400 + 300 * math.sin(t * 0.8))])
        src(ctx, P["light"], a)
        ctx.fill()
        ctx.restore()
    ctx.translate(0, -bob)
    _sea_strip(ctx, t, 900, 30, 10, hexc("#1d3558"))


def torpedo_boat(ctx, t, p):
    """A small fast patrol boat, bow right, waterline y = 0. p: ghost (0..1 = a see-through radar phantom),
    wake (spray behind it)."""
    a = 1.0 - 0.75 * p.get("ghost", 0.0)
    bob = 8 * math.sin(t * 2.4 + 2)
    ctx.translate(0, bob)
    shape(ctx, lambda c: p_poly(c, [(-260, -60), (220, -80), (300, -110), (240, 20), (-250, 20)]), hexc("#6d7a6a"),
          OUT * 0.8, (0, 0.18), a=a)
    shape(ctx, lambda c: p_rrect(c, -80, -170, 140, 110, 8), hexc("#6d7a6a"), OUT * 0.7, (0.1, 0), a=a)
    shape(ctx, lambda c: c.rectangle(-55, -150, 90, 30), P["window"], OUT * 0.4, None, a=a)
    for x in (-200, 120):
        shape(ctx, lambda c, x=x: p_rrect(c, x - 50, -100, 100, 36, 16), hexc("#4c574a"), OUT * 0.5, None, a=a)
    if p.get("wake", 1.0):
        for k in range(5):
            u = (t * 2 + k * 0.2) % 1
            flat(ctx, lambda c, u=u: p_ellipse(c, -280 - u * 260, -10 - u * 30, 40 * (1 - u) + 10, 25 * (1 - u) + 6),
                 P["foam"], a=0.7 * (1 - u) * a)


def operator(ctx, t, p):
    """A sailor at a radar console: person with headphones, the round scope to his right (+x).
    p: blips (0..1 how many contacts show), ghost (blips flicker in and out), sweat, mood, talk."""
    ctx.translate(-220, 0)   # drawn left of its mark so the console stays on screen at the macro hero spot
    q = {"skin": P["skin2"], "body": hexc("#3a5a8c"), "hat": "sailor", "mood": p.get("mood", "worry"),
         "arm": "point", "mouth": "o" if p.get("mood") == "shock" else "flat"}
    q.update({k: v for k, v in p.items() if k in ("blink", "talk", "sweat", "look", "phase", "walking")})
    person(ctx, t, q)
    for s in (-1, 1):   # headphones
        shape(ctx, lambda c, s=s: p_rrect(c, s * 128 - 28, -890, 56, 100, 20), INK, OUT * 0.4, None)
    ctx.new_sub_path()
    ctx.arc(0, -860, 140, math.pi * 1.05, math.pi * 1.95)
    ink(ctx, 16)
    ctx.stroke()
    # console in front of him (covers his legs), the round scope on its face
    cx, cy, R = 20, -300, 165
    shape(ctx, lambda c: p_rrect(c, -300, -540, 640, 540, 24), hexc("#5a6660"), OUT, (0.12, 0))
    shape(ctx, lambda c: p_ellipse(c, cx, cy, R, R), hexc("#0c2a14"), OUT, None)
    for r in (55, 110, R - 5):
        ctx.new_sub_path()
        ctx.arc(cx, cy, r, 0, 2 * math.pi)
        src(ctx, GREEN, 0.35)
        ctx.set_line_width(4)
        ctx.stroke()
    ang = t * 2.4
    ctx.save()
    ctx.move_to(cx, cy)
    ctx.arc(cx, cy, R - 5, ang - 0.6, ang)
    ctx.close_path()
    src(ctx, GREEN, 0.3)
    ctx.fill()
    ctx.restore()
    stroke(ctx, [(cx, cy), (cx + (R - 5) * math.cos(ang), cy + (R - 5) * math.sin(ang))], 5, color=GREEN)
    n = int(round(6 * p.get("blips", 0.0)))
    rng = random.Random(4)
    for k in range(n):
        r, a0 = rng.uniform(40, R - 20), rng.uniform(0, 6.28)
        vis = 1.0 if not p.get("ghost") else max(0.0, math.sin(t * (3 + k) + k * 1.7))
        flat(ctx, lambda c, r=r, a0=a0: p_ellipse(c, cx + r * math.cos(a0), cy + r * math.sin(a0), 13, 13),
             GREEN, a=vis)
    for k in range(3):
        shape(ctx, lambda c, k=k: p_ellipse(c, 240, -460 + k * 90, 26, 26), (hexc("#e2b13c"), hexc("#d8322a"),
                                                                            hexc("#5dbb6a"))[k], OUT * 0.6, None)


def jet(ctx, t, p):
    """A small navy jet flying right, centre origin, about 900 wide."""
    ctx.translate(0, 12 * math.sin(t * 2))
    shape(ctx, lambda c: p_smooth(c, [(-420, -10), (-200, -50), (300, -40), (450, 0), (300, 40), (-200, 40)]),
          hexc("#8f9ba6"), OUT, (0, 0.2))
    shape(ctx, lambda c: p_poly(c, [(-60, 0), (120, 0), (-160, 220), (-260, 220)]), hexc("#7a8691"), OUT * 0.8, None)
    shape(ctx, lambda c: p_poly(c, [(-330, -20), (-250, -20), (-380, -170), (-430, -170)]), hexc("#7a8691"),
          OUT * 0.8, None)
    shape(ctx, lambda c: p_ellipse(c, 230, -45, 90, 35), hexc("#9fe3f0"), OUT * 0.7, None)
    for k in range(4):
        u = (t * 3 + k * 0.25) % 1
        flat(ctx, lambda c, u=u: p_ellipse(c, -440 - u * 200, 0, 40 * (1 - u) + 8, 22 * (1 - u) + 5), hexc("#ffb347"),
             a=0.8 * (1 - u))


def tv(ctx, t, p):
    """An old TV set on legs, base y = 0, screen ~ 600 x 450. p: show = "podium" (a speaker at a podium, a
    flag-free seal) or "flames"."""
    for x in (-250, 250):
        stroke(ctx, [(x, -300), (x * 1.2, 0)], 26)
    shape(ctx, lambda c: p_rrect(c, -400, -900, 800, 620, 50), hexc("#8a5a30"), OUT, (0.12, 0.05))
    shape(ctx, lambda c: p_rrect(c, -330, -840, 560, 480, 60), hexc("#1b2a3a"), OUT, None)
    show = p.get("show", "podium")
    ctx.save()
    p_rrect(ctx, -330, -840, 560, 480, 60)
    ctx.clip()
    if show == "flames":
        flat(ctx, lambda c: c.rectangle(-340, -850, 600, 500), hexc("#3a0d08"))
        for k in range(7):
            x = -280 + k * 80
            h = 180 + 60 * math.sin(t * 7 + k * 1.3)
            shape(ctx, lambda c, x=x, h=h: p_poly(c, [(x - 50, -360), (x, -360 - h), (x + 50, -360)]),
                  hexc("#ff7a1a") if k % 2 else hexc("#ffd23a"), 0, None)
    else:
        flat(ctx, lambda c: c.rectangle(-340, -850, 600, 500), hexc("#3d5a8c"))
        shape(ctx, lambda c: p_ellipse(c, -50, -660, 55, 62), P["skin2"], OUT * 0.5, None)
        shape(ctx, lambda c: p_rrect(c, -130, -600, 160, 140, 30), P["suit"], OUT * 0.5, None)
        shape(ctx, lambda c: p_poly(c, [(-170, -480), (70, -480), (40, -360), (-140, -360)]), P["podium"], OUT * 0.5,
              None)
        shape(ctx, lambda c: p_ellipse(c, -50, -430, 30, 30), P["seal"], OUT * 0.4, None)
    ctx.restore()
    for k in range(int(500 / 8)):   # scan lines
        flat(ctx, lambda c, k=k: c.rectangle(-330, -840 + k * 8, 560, 2), (0, 0, 0), a=0.15)
    for y in (-760, -620):
        shape(ctx, lambda c, y=y: p_ellipse(c, 320, y, 28, 28), P["steel"], OUT * 0.6, None)


def lighthouse(ctx, t, p):
    """A white stone lighthouse with its keepers' cottage, base y = 0, tower ~1250 tall. p: lit (0..1)."""
    shape(ctx, lambda c: c.rectangle(-560, -330, 420, 330), hexc("#f2efe6"), OUT, (0.12, 0))
    shape(ctx, lambda c: p_poly(c, [(-590, -320), (-350, -470), (-110, -320)]), hexc("#5a5a5a"), OUT, None)
    shape(ctx, lambda c: c.rectangle(-420, -200, 90, 200), hexc("#4b3a2a"), OUT * 0.8, None)
    shape(ctx, lambda c: c.rectangle(-260, -250, 80, 80), hexc("#22305a"), OUT * 0.7, None)
    shape(ctx, lambda c: p_poly(c, [(-170, 0), (-110, -1050), (110, -1050), (170, 0)]), hexc("#f6f3ea"), OUT,
          (0.12, 0))
    shape(ctx, lambda c: c.rectangle(-150, -1110, 300, 60), hexc("#2a2a2a"), OUT * 0.8, None)
    lit = p.get("lit", 0.0)
    shape(ctx, lambda c: c.rectangle(-100, -1270, 200, 160), lighter(P["light"], 0.2) if lit > 0.5
          else hexc("#40485a"), OUT * 0.8, None)
    for x in (-50, 0, 50):
        stroke(ctx, [(x, -1270), (x, -1110)], 5)
    shape(ctx, lambda c: p_poly(c, [(-130, -1270), (0, -1380), (130, -1270)]), hexc("#2a2a2a"), OUT * 0.8, None)
    if lit > 0.01:
        a = math.cos(t * 1.6)
        ctx.save()
        w = 900 * a
        p_poly(ctx, [(0, -1200), (w, -1350), (w, -1050)])
        src(ctx, P["light"], 0.35 * lit)
        ctx.fill()
        ctx.restore()


def isle_rock(ctx, t, p):
    """The small far island with its lighthouse, waterline y = 0, about 1100 wide. p: lit (0..1)."""
    shape(ctx, lambda c: p_poly(c, [(-560, 20), (-480, -220), (-300, -330), (60, -360), (300, -300), (480, -160),
                                    (560, 20)]), hexc("#4a4f58"), OUT, (0.1, 0.12))
    shape(ctx, lambda c: p_poly(c, [(-380, -270), (-300, -330), (60, -360), (300, -300), (240, -270)]),
          hexc("#55704a"), OUT * 0.6, None)
    ctx.save()
    ctx.translate(40, -330)
    ctx.scale(0.32, 0.32)
    lighthouse(ctx, t, p)
    ctx.restore()
    _sea_strip(ctx, t, 800, 10, 16, hexc("#16294a"))


def big_wave(ctx, t, p):
    """A huge curling wave, base y = 0, crest up to ~1200 * rise."""
    r = max(0.05, p.get("rise", 1.0))
    h = 1200 * r
    body = lambda c: p_smooth(c, [(-800, 60), (-500, -0.3 * h), (-100, -0.8 * h), (250, -h), (480, -0.85 * h),  # noqa
                                  (380, -0.65 * h), (200, -0.7 * h), (300, -0.3 * h), (800, 60)])
    shape(ctx, body, hexc("#2f6fa8"), OUT, (0.1, 0.1), hi=(0.4, 0.3, 0.2))
    for k in range(8):
        a = k * 0.8 + t * 4
        flat(ctx, lambda c, k=k, a=a: p_ellipse(c, 250 + 230 * math.cos(a * 0.3) - k * 30, -h + 40 * math.sin(a), 60, 40),
             P["foam"], a=0.9)


def steamer(ctx, t, p):
    """A small black-hulled relief steamer, bow right, waterline y = 0. p: flare (0..1 a red flare rising)."""
    bob = 8 * math.sin(t * 1.5)
    ctx.translate(0, bob)
    shape(ctx, lambda c: p_poly(c, [(-520, -120), (460, -150), (560, -190), (470, 30), (-470, 30)]), hexc("#22262c"),
          OUT, (0, 0.18))
    flat(ctx, lambda c: c.rectangle(-470, -40, 940, 26), hexc("#a83a30"))
    shape(ctx, lambda c: p_rrect(c, -160, -300, 300, 180, 8), hexc("#e8e2d0"), OUT, (0.12, 0))
    shape(ctx, lambda c: c.rectangle(-40, -500, 100, 200), hexc("#d9a541"), OUT, (0.15, 0))
    flat(ctx, lambda c: c.rectangle(-40, -500, 100, 40), INK)
    for k in range(4):
        u = (t * 0.6 + k * 0.25) % 1
        flat(ctx, lambda c, u=u: p_ellipse(c, 10 - u * 260, -540 - u * 300, 50 + u * 60, 40 + u * 40),
             hexc("#9aa3ab"), a=0.7 * (1 - u))
    for x in (-380, 330):
        stroke(ctx, [(x, -140), (x, -620)], 10)
    f = p.get("flare", 0.0)
    if f > 0.01:
        y = -700 - 900 * f
        stroke(ctx, [(300, -620), (330, y)], 6, color=hexc("#ffb0a0"), a=0.6)
        starburst(ctx, 330, y, 60, n=8, fill=hexc("#ff4a3a"))
    ctx.translate(0, -bob)
    _sea_strip(ctx, t, 750, 30, 12, hexc("#1d3558"))


def keeper(ctx, t, p):
    """A lighthouse keeper in a yellow oilskin and sou'wester (generic, no likeness)."""
    q = {"skin": P["skin2"], "body": YEL, "pants": hexc("#2b2f36"), "mood": p.get("mood", "calm"),
         "hair": hexc("#5a3a22")}
    q.update(p)
    a = 1.0 - p.get("fade", 0.0)
    if a < 0.99:
        ctx.push_group()
    person(ctx, t, q)
    shape(ctx, lambda c: p_poly(c, [(-170, -930), (-120, -1000), (120, -1000), (170, -930), (0, -900)]), YEL,
          OUT * 0.8, None)
    if a < 0.99:
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(max(0.0, a))


def coat_pegs(ctx, t, p):
    """A wall board with three pegs at y = -1000..; p: coats (how many oilskins still hang, 0..3)."""
    shape(ctx, lambda c: p_rrect(c, -380, -1060, 760, 60, 10), P["wood"], OUT * 0.8, (0.1, 0))
    n = int(round(p.get("coats", 3)))
    for k, x in enumerate((-250, 0, 250)):
        shape(ctx, lambda c, x=x: p_ellipse(c, x, -1030, 20, 20), P["wood_dk"], OUT * 0.6, None)
        if k < n:
            sw = 4 * math.sin(t * 1.3 + k)
            shape(ctx, lambda c, x=x, sw=sw: p_poly(c, [(x - 40, -1020), (x + 40, -1020), (x + 110 + sw, -480),
                                                        (x - 110 + sw, -480)]), YEL, OUT * 0.8, (0.12, 0))


def wall_clock(ctx, t, p):
    """A round wall clock, centre origin; p: stopped (hands frozen)."""
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 150, 150), P["wood"], OUT, None)
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 120, 120), (1, 1, 0.96), OUT * 0.6, None)
    for k in range(12):
        a = k * math.pi / 6
        flat(ctx, lambda c, a=a: p_ellipse(c, 100 * math.cos(a), 100 * math.sin(a), 8, 8), INK)
    m = 0.9 if p.get("stopped", True) else t * 0.8
    for a, ln, w in ((m * 12, 90, 8), (m, 60, 12)):
        stroke(ctx, [(0, 0), (ln * math.sin(a), -ln * math.cos(a))], w)


def drill_rig(ctx, t, p):
    """The borehole's tall drilling tower inside a boxy sheathed derrick, base y = 0, ~1300 tall."""
    ctx.translate(-150, 0)   # drawn left of its mark so the wide base stays on screen
    shape(ctx, lambda c: c.rectangle(-560, -360, 1120, 360), hexc("#b5563a"), OUT, (0.12, 0))
    for x in range(-500, 560, 140):
        shape(ctx, lambda c, x=x: c.rectangle(x, -300, 80, 70), hexc("#3a5a7a"), OUT * 0.5, None)
    shape(ctx, lambda c: p_poly(c, [(-220, -360), (-120, -1300), (120, -1300), (220, -360)]), hexc("#8f99a6"), OUT,
          (0.12, 0))
    for k in range(8):
        y = -420 - k * 115
        stroke(ctx, [(-200 + k * 12, y), (200 - k * 12, y - 100)], 6)
    shape(ctx, lambda c: c.rectangle(-150, -1360, 300, 70), hexc("#d8322a"), OUT * 0.8, None)
    flat(ctx, lambda c: p_ellipse(c, 0, -1330, 22, 22), P["light"], a=0.5 + 0.5 * math.sin(t * 3))
    flat(ctx, lambda c: c.rectangle(-900, -10, 1800, 30), (1, 1, 1))


def section(ctx, t, p):
    """A cut-away of the ground: ground line at y = 0, rock bands down to y = 1700, a thin hole drilled to
    depth (0..1 of 1700), p: fossils (show tiny plankton fossils at 55 %), heat (0..1 red glow at the bottom),
    trench (0..1 show the ocean's deepest trench depth as a dashed mark at 90 %)."""
    bands = ("#8a6f55", "#7a6a5e", "#6b5f63", "#5d5367", "#56486a", "#5a3f5a", "#6a3a40")
    for k, c in enumerate(bands):
        flat(ctx, lambda cc, k=k, c=c: cc.rectangle(-450, k * 245, 900, 250), hexc(c))
    ctx.rectangle(-450, 0, 900, 1715)
    ink(ctx, OUT)
    ctx.stroke()
    rng = random.Random(8)
    for _ in range(40):
        x, y = rng.uniform(-420, 420), rng.uniform(20, 1690)
        flat(ctx, lambda c, x=x, y=y: p_blob(c, x, y, 26, 14, 0.2, seed=int(y)), (0, 0, 0), a=0.15)
    flat(ctx, lambda c: c.rectangle(-450, -70, 900, 70), hexc("#f2f5f7"))
    stroke(ctx, [(-450, 0), (450, 0)], OUT)
    d = 1700 * p.get("depth", 1.0)
    heat = p.get("heat", 0.0)
    if heat > 0.01:
        flat(ctx, lambda c: p_ellipse(c, 0, d, 160, 120), hexc("#ff5a1a"), a=0.5 * heat * (0.8 + 0.2 * math.sin(t * 5)))
    flat(ctx, lambda c: c.rectangle(-9, 0, 18, d), hexc("#111111"))
    if p.get("fossils"):
        for k in range(6):
            x = -160 + 70 * k
            shape(ctx, lambda c, x=x, k=k: p_ellipse(c, x if x < 0 else x + 60, 935 + 18 * math.sin(k), 18, 12),
                  hexc("#f2e6b8"), OUT * 0.4, None)
    if p.get("trench"):
        for x in range(-440, 440, 60):
            stroke(ctx, [(x, 1530), (x + 30, 1530)], 8, color=hexc("#7fd3ff"), a=p["trench"])


def well_cap(ctx, t, p):
    """The rusty welded metal cap over the hole, on a concrete pad, base y = 0."""
    shape(ctx, lambda c: p_rrect(c, -420, -60, 840, 80, 14), hexc("#a9a9a3"), OUT, (0, 0.2))
    shape(ctx, lambda c: p_ellipse(c, 0, -80, 170, 50), hexc("#9b5a3c"), OUT, (0, 0.2))
    shape(ctx, lambda c: p_ellipse(c, 0, -100, 120, 34), hexc("#b8693f"), OUT * 0.8, None)
    for k in range(8):
        a = k * math.pi / 4
        flat(ctx, lambda c, a=a: p_ellipse(c, 100 * math.cos(a), -100 + 28 * math.sin(a), 10, 6), hexc("#6a3a22"))


def mic_cable(ctx, t, p):
    """A microphone hanging on a long cable from y = -1400 down to the origin, swinging a little."""
    sw = 20 * math.sin(t * 1.4)
    stroke(ctx, [(0, -1400), (sw * 0.5, -700), (sw, -120)], 8, smooth=True)
    shape(ctx, lambda c: p_rrect(c, sw - 45, -130, 90, 130, 40), P["steel_dk"], OUT * 0.8, (0.12, 0))
    for y in (-110, -85, -60):
        stroke(ctx, [(sw - 35, y), (sw + 35, y)], 4, color=P["steel"])


def student(ctx, t, p):
    """A schoolgirl in a blue school dress. p: laugh (0..1: shakes with uncontrollable laughter), cry (tears),
    look, mood."""
    lg = p.get("laugh", 0.0)
    q = {"skin": P["skin3"], "body": hexc("#3f74c4"), "pants": P["skin3"], "hair": hexc("#1d1712"),
         "mood": "happy" if lg > 0.3 else p.get("mood", "calm"), "arm": "down"}
    if lg > 0.3:
        q.update(mouth="grin", talk=0.4 + 0.6 * abs(math.sin(t * 15 + p.get("seed", 0))))
    q.update({k: v for k, v in p.items() if k in ("blink", "look", "phase", "walking", "seed")})
    ctx.save()
    if lg > 0.01:
        ctx.translate(10 * lg * math.sin(t * 30 + p.get("seed", 0)), -18 * lg * abs(math.sin(t * 15)))
        ctx.rotate(0.05 * lg * math.sin(t * 11))
    person(ctx, t, q)
    bob = 6 * math.sin(t * 2.2 + p.get("seed", 0))
    hy = -830 + bob
    shape(ctx, lambda c: p_poly(c, [(-125, -400 + bob), (125, -400 + bob), (175, -150), (-175, -150)]),
          q["body"], OUT, (0.12, 0))   # the skirt of the school dress
    for s in (-1, 1):   # two hair puffs
        shape(ctx, lambda c, s=s: p_ellipse(c, s * 120, hy - 110, 55, 55), q["hair"], OUT * 0.8, None)
    if lg > 0.3:   # squeezed-shut laughing eyes
        for s in (-1, 1):
            flat(ctx, lambda c, s=s: p_ellipse(c, s * 46, hy - 30, 36, 40), q["skin"])
            stroke(ctx, [(s * 46 - 26, hy - 20), (s * 46, hy - 44), (s * 46 + 26, hy - 20)], 9)
    if p.get("cry"):
        for s in (-1, 1):
            u = (t * 1.5 + (s + 1) * 0.3) % 1
            flat(ctx, lambda c, s=s, u=u: p_ellipse(c, s * 50, -820 + u * 150, 12, 18), hexc("#7fd3ff"), a=1 - u)
    ctx.restore()


def desks(ctx, t, p):
    """A front row of wooden school desks, base y = 0, ~1400 wide."""
    for x in (-500, 0, 500):
        shape(ctx, lambda c, x=x: p_rrect(c, x - 220, -380, 440, 60, 10), P["desk"], OUT * 0.8, (0, 0.2))
        shape(ctx, lambda c, x=x: c.rectangle(x - 200, -320, 400, 140), P["desk_dk"], OUT * 0.8, None)
        for s in (-1, 1):
            stroke(ctx, [(x + s * 180, -180), (x + s * 190, 0)], 18)
        shape(ctx, lambda c, x=x: c.rectangle(x - 60, -420, 140, 40), P["paper"], OUT * 0.5, None)


def hut(ctx, t, p):
    """A round mud-walled hut with a thatched cone roof, base y = 0, ~700 wide."""
    shape(ctx, lambda c: c.rectangle(-300, -380, 600, 380), hexc("#b07a4a"), OUT, (0.12, 0))
    shape(ctx, lambda c: p_poly(c, [(-380, -340), (0, -760), (380, -340)]), hexc("#d9b46a"), OUT, (0.1, 0.1))
    for k in range(6):
        stroke(ctx, [(-300 + k * 110, -360), (0, -740)], 4, color=hexc("#b8924a"))
    shape(ctx, lambda c: p_rrect(c, -70, -240, 140, 240, 50), hexc("#3a2a1e"), OUT * 0.8, None)


ACTORS = {k: v for k, v in {
    "destroyer": destroyer, "torpedo_boat": torpedo_boat, "operator": operator, "jet": jet, "tv": tv,
    "lighthouse": lighthouse, "isle_rock": isle_rock, "big_wave": big_wave, "steamer": steamer, "keeper": keeper,
    "coat_pegs": coat_pegs, "wall_clock": wall_clock, "drill_rig": drill_rig, "section": section,
    "well_cap": well_cap, "mic_cable": mic_cable, "student": student, "desks": desks, "hut": hut}.items()}
SCENES = {"night_sea": night_sea, "radar_room": radar_room, "isle": isle, "keeper_room": keeper_room,
          "tundra": tundra, "classroom": classroom, "village": village}


def register(drawn_mod):
    drawn_mod.ACTORS.update(ACTORS)
    drawn_mod.SCENES.update(SCENES)


if __name__ == "__main__":
    import drawn
    register(drawn)
    drawn.main()
