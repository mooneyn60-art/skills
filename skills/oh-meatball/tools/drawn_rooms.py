"""House rooms and macro worlds for tools/drawn.py ("Things Living In Your House"), in the drawn_kit style.

Scenes (floor y = 1500 unless noted; the camera usually frames x 0..1080):
  bathroom   night bathroom: blue tiles, tub, floor drain, toilet, moonlit window
  bedroom    night bedroom: striped wallpaper, a bed whose mattress top is y = 1180, lamp, window
  fibers     macro pillow fabric: giant woven threads underfoot, drifting skin flakes (the dust-mite world)
  skin       macro face skin in cross-section: surface y = 1100, follicles (pores) down to y = 1900, hairs
  study      a study at night: a bookshelf wall, wallpaper, a desk lamp glow
  sill       macro windowsill: the sill is the floor, a big sunny window behind (p: "night")
Props (actors): book, trex, sleeper, pillow_face
"""
import math
import random

from drawn_kit import (BG_OUT, INK, OUT, PAL, darker, eyes, flat, hexc, ink, lighter, limb, mouth, p_blob,
                       p_ellipse, p_poly, p_rrect, p_smooth, shape, src, stroke)

P = PAL
C = {k: hexc(v) for k, v in {
    "tile": "#bfe0ea", "tile_dk": "#9cc6d4", "grout": "#86aebb", "floor_t": "#d9d3c4", "floor_t2": "#c9c2b1",
    "porcelain": "#f6f6f2", "night_win": "#22305a", "moon": "#f4f1d0",
    "paper1": "#6f7fae", "paper2": "#6576a3", "bedwood": "#8a5a30", "sheet": "#e9eef7", "sheet_dk": "#c8d2e6",
    "blanket": "#c2504a", "blanket_dk": "#9d3c37", "pillow": "#fbf7ef", "lamp": "#f2c75c",
    "thread": "#efe6d2", "thread_dk": "#d4c6a6", "fab_bg": "#e9dcc0", "fab_bg2": "#dccdab", "flake": "#f7efe0",
    "skin_s": "#f0b99a", "skin_m": "#e7a283", "skin_d": "#d68b6c", "fat": "#f6d9a8", "oil": "#f3d45c",
    "hairc": "#4a3426", "study": "#5d4a6e", "study_dk": "#4e3d5e", "shelf": "#7a5233",
    "book1": "#c0453c", "book2": "#3f6fa8", "book3": "#d9a441", "book4": "#4f8a5a", "book5": "#8a5ba0",
    "sillw": "#f2efe8", "sill_dk": "#d6d0c2", "garden": "#7cc46a", "garden_dk": "#5aa54d", "trunk": "#7a5233",
    "rex": "#6fae5a", "rex_dk": "#4f8c42", "rex_belly": "#d9e6a6",
}.items()}


def _tiles(ctx, x0, y0, x1, y1, s, c1, c2, seed=1):
    rng = random.Random(seed)
    y = y0
    while y < y1:
        x = x0
        while x < x1:
            flat(ctx, lambda c, x=x, y=y: p_rrect(c, x + 3, y + 3, s - 6, s - 6, 6),
                 c1 if rng.random() < 0.7 else c2)
            x += s
        y += s


def _night_window(ctx, x, y, w, h, t):
    shape(ctx, lambda c: c.rectangle(x - 20, y - 20, w + 40, h + 40), P["wood"], BG_OUT, None)
    flat(ctx, lambda c: c.rectangle(x, y, w, h), C["night_win"])
    flat(ctx, lambda c: p_ellipse(c, x + w * 0.7, y + h * 0.3, 44, 44), C["moon"])
    for i in range(6):
        sx, sy = x + (37 * i * 7) % w, y + (53 * i * 3) % (h * 0.8) + 20
        a = 0.5 + 0.5 * math.sin(t * 2 + i)
        flat(ctx, lambda c, sx=sx, sy=sy: p_ellipse(c, sx, sy, 5, 5), (1, 1, 0.9), a=a)
    stroke(ctx, [(x + w / 2, y), (x + w / 2, y + h)], BG_OUT)
    stroke(ctx, [(x, y + h / 2), (x + w, y + h / 2)], BG_OUT)
    ctx.rectangle(x, y, w, h)
    ink(ctx, BG_OUT)
    ctx.stroke()


def bathroom(ctx, t, layer, p):
    layer(0.85)
    _tiles(ctx, -700, -500, 2300, 1520, 120, C["tile"], C["tile_dk"])
    flat(ctx, lambda c: c.rectangle(-700, 1040, 3000, 26), C["grout"])
    _night_window(ctx, 560, 260, 300, 260, t)
    # mirror + sink, left
    shape(ctx, lambda c: p_rrect(c, -120, 330, 360, 430, 30), hexc("#cfe7f2"), BG_OUT, (0.0, 0.0))
    stroke(ctx, [(-60, 420), (40, 360)], 10, color=(1, 1, 1), a=0.7)
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-700, 1500, 3000, 600), C["floor_t"])
    for x in range(-700, 2300, 160):
        stroke(ctx, [(x, 1500), (x - 120, 2100)], 3, color=C["floor_t2"])
    stroke(ctx, [(-700, 1500), (2300, 1500)], BG_OUT)
    # sink pedestal
    shape(ctx, lambda c: p_rrect(c, -80, 880, 280, 90, 40), C["porcelain"], BG_OUT, (0, 0.25))
    shape(ctx, lambda c: p_poly(c, [(20, 960), (100, 960), (120, 1500), (0, 1500)]), C["porcelain"], BG_OUT,
          (0.15, 0))
    # tub, right
    shape(ctx, lambda c: p_rrect(c, 1180, 1120, 900, 380, 60), C["porcelain"], BG_OUT, (0.0, 0.2))
    stroke(ctx, [(1180, 1160), (2080, 1160)], BG_OUT)
    shape(ctx, lambda c: c.rectangle(1240, 1040, 30, 90), P["steel"], BG_OUT * 0.8, None)
    # floor drain
    shape(ctx, lambda c: p_ellipse(c, 840, 1560, 70, 18), P["steel_dk"], BG_OUT * 0.8, None)
    for k in range(-2, 3):
        stroke(ctx, [(840 + k * 22, 1548), (840 + k * 22, 1572)], 4)
    if p.get("dark", True):
        layer(1.0)
        ctx.save()
        ctx.identity_matrix()
        ctx.rectangle(0, 0, 1080, 1920)
        src(ctx, (0.05, 0.08, 0.2), 0.18)
        ctx.fill()
        ctx.restore()


def bedroom(ctx, t, layer, p):
    layer(0.85)
    flat(ctx, lambda c: c.rectangle(-700, -500, 3000, 2100), C["paper1"])
    for x in range(-700, 2300, 120):
        flat(ctx, lambda c, x=x: c.rectangle(x, -500, 46, 2100), C["paper2"])
    _night_window(ctx, 760, 240, 340, 300, t)
    # lamp on a side table, left
    shape(ctx, lambda c: c.rectangle(-150, 1150, 260, 350), P["wood"], BG_OUT, (0.1, 0))
    shape(ctx, lambda c: c.rectangle(-30, 960, 20, 190), P["steel_dk"], BG_OUT * 0.7, None)
    shape(ctx, lambda c: p_poly(c, [(-110, 960), (70, 960), (30, 840), (-70, 840)]), C["lamp"], BG_OUT, (0.1, 0))
    ctx.save()
    p_ellipse(ctx, -20, 960, 260, 200)
    src(ctx, C["lamp"], 0.16 + 0.02 * math.sin(t * 3))
    ctx.fill()
    ctx.restore()
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-700, 1500, 3000, 600), P["floor"])
    stroke(ctx, [(-700, 1500), (2300, 1500)], BG_OUT)
    # the bed: headboard left, mattress top y = 1180
    shape(ctx, lambda c: p_rrect(c, 160, 760, 70, 740, 20), C["bedwood"], BG_OUT, (0.15, 0))
    shape(ctx, lambda c: p_rrect(c, 180, 1180, 1500, 230, 30), C["sheet"], BG_OUT, (0, 0.25))
    shape(ctx, lambda c: c.rectangle(180, 1400, 1500, 100), C["bedwood"], BG_OUT, (0, 0.2))
    shape(ctx, lambda c: p_smooth(c, [(620, 1190), (900, 1150), (1300, 1160), (1690, 1190), (1690, 1430),
                                      (620, 1430)]), C["blanket"], BG_OUT, (0.05, 0.2))
    for x in range(700, 1690, 140):
        stroke(ctx, [(x, 1180), (x + 30, 1430)], 4, color=C["blanket_dk"])
    if not p.get("no_pillow"):
        shape(ctx, lambda c: p_blob(c, 380, 1130, 170, 70, 0.05, seed=2), C["pillow"], BG_OUT, (0.08, 0.2))


def fibers(ctx, t, layer, p):
    """Macro pillow fabric. Ground (top of the weave) y = 1500."""
    layer(0.4)
    flat(ctx, lambda c: c.rectangle(-2000, -2000, 5000, 5000), C["fab_bg"])
    for i in range(7):
        y = -300 + i * 300
        stroke(ctx, [(-1500 + 40 * math.sin(i), y), (2500, y + 200)], 140, color=C["fab_bg2"], a=0.6)
    layer(0.7)
    for i in range(6):   # far threads
        x = -400 + i * 330
        stroke(ctx, [(x, -400), (x + 200, 600), (x + 120, 1500)], 110, smooth=True, color=C["thread_dk"])
        stroke(ctx, [(x, -400), (x + 200, 600), (x + 120, 1500)], 110, smooth=True, color=C["thread_dk"])
    layer(1.0)
    # the weave underfoot: rounded thread bumps
    for row in range(3):
        y = 1500 + row * 150
        for k in range(-6, 16):
            x = k * 220 + (row % 2) * 110
            shape(ctx, lambda c, x=x, y=y: p_rrect(c, x, y - 40, 230, 150, 70), C["thread"], BG_OUT,
                  (0, 0.22), hi=(0.3, 0.25, 0.25))
            for j in range(3):
                stroke(ctx, [(x + 40 + j * 60, y - 30), (x + 70 + j * 60, y + 100)], 3, color=C["thread_dk"])
    # drifting skin flakes
    rng = random.Random(5)
    for _ in range(int(p.get("flakes", 10))):
        x0, y0 = rng.uniform(-200, 1300), rng.uniform(0, 1300)
        y = (y0 + t * 30) % 1500 - 100
        x = x0 + 30 * math.sin(t * 0.8 + x0)
        r = rng.uniform(30, 70)
        shape(ctx, lambda c, x=x, y=y, r=r: p_blob(c, x, y, r, r * 0.55, 0.2, seed=int(x0)), C["flake"],
              BG_OUT * 0.7, None, a=0.85)


def skin(ctx, t, layer, p):
    """Macro skin cross-section: surface y = 1100; follicles (pores) at x = 0, 540, 1080 reach down to ~1900."""
    layer(0.5)
    sky = hexc("#2a2244") if p.get("night", True) else hexc("#f7d9c4")
    flat(ctx, lambda c: c.rectangle(-2000, -2000, 5000, 5000), sky)
    if p.get("night", True):
        rng = random.Random(3)
        for _ in range(40):
            x, y = rng.uniform(-800, 1900), rng.uniform(-600, 1000)
            flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 4, 4), (1, 1, 0.9),
                 a=0.4 + 0.4 * math.sin(t * 2 + x))
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-1000, 1100, 3100, 1400), C["skin_m"])
    flat(ctx, lambda c: c.rectangle(-1000, 1100, 3100, 70), C["skin_s"])
    flat(ctx, lambda c: c.rectangle(-1000, 1650, 3100, 900), C["fat"])
    stroke(ctx, [(-1000, 1650), (2100, 1650)], 4, color=C["skin_d"])
    for x in (-540, 0, 540, 1080, 1620):
        # follicle tube with an oil gland
        shape(ctx, lambda c, x=x: p_smooth(c, [(x - 70, 1100), (x - 60, 1400), (x - 55, 1750), (x, 1820),
                                                 (x + 55, 1750), (x + 60, 1400), (x + 70, 1100)], close=False),
              C["skin_d"], BG_OUT, None)
        shape(ctx, lambda c, x=x: p_blob(c, x + 120, 1450, 70, 90, 0.1, seed=x), C["oil"], BG_OUT * 0.8,
              (0.1, 0.1))
        stroke(ctx, [(x + 60, 1440), (x + 80, 1450)], BG_OUT)
        # hair shaft growing out
        sway = 20 * math.sin(t * 0.9 + x)
        limb(ctx, [(x, 1800), (x + 6, 1100), (x + 40 + sway, 500), (x + 120 + sway * 2, -100)], 34, C["hairc"],
             BG_OUT * 0.8)
    stroke(ctx, [(-1000, 1100), (-610, 1100)], BG_OUT)
    for a, b in ((-470, -70), (70, 470), (610, 1010), (1150, 1550), (1690, 2100)):
        pts = [(x, 1100 + 6 * math.sin(x / 40)) for x in range(a, b, 20)] + [(b, 1100)]
        stroke(ctx, pts, BG_OUT)


def study(ctx, t, layer, p):
    layer(0.85)
    flat(ctx, lambda c: c.rectangle(-700, -500, 3000, 2100), C["study"])
    for x in range(-700, 2300, 150):
        flat(ctx, lambda c, x=x: c.rectangle(x, -500, 20, 2100), C["study_dk"])
    # bookshelf
    shape(ctx, lambda c: c.rectangle(-100, 140, 1280, 1360), C["shelf"], BG_OUT, (0.04, 0))
    rng = random.Random(8)
    cols = [C["book1"], C["book2"], C["book3"], C["book4"], C["book5"]]
    for k, y in enumerate((180, 520, 860, 1200)):
        shape(ctx, lambda c, y=y: c.rectangle(-80, y, 1240, 300), darker(C["shelf"], 0.7), BG_OUT * 0.6, None)
        x = -70
        while x < 1140:
            w = rng.uniform(50, 95)
            h = rng.uniform(210, 290)
            col = rng.choice(cols)
            shape(ctx, lambda c, x=x, y=y, w=w, h=h: p_rrect(c, x, y + 300 - h, w, h, 6), col, BG_OUT * 0.7,
                  (0.12, 0))
            stroke(ctx, [(x + 10, y + 330 - h), (x + w - 10, y + 330 - h)], 5, color=C["book3"])
            x += w + 4
        shape(ctx, lambda c, y=y: c.rectangle(-100, y + 300, 1280, 40), C["shelf"], BG_OUT, (0, 0.3))
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-700, 1500, 3000, 600), P["floor_dk"])
    stroke(ctx, [(-700, 1500), (2300, 1500)], BG_OUT)
    ctx.save()
    p_ellipse(ctx, 900, 400, 420, 340)
    src(ctx, C["lamp"], 0.1)
    ctx.fill()
    ctx.restore()


def sill(ctx, t, layer, p):
    """Macro windowsill: the sill top is the floor (y = 1500); window glass behind, garden outside."""
    night = p.get("night", False)
    layer(0.35)
    flat(ctx, lambda c: c.rectangle(-2000, -2000, 5000, 5000), C["night_win"] if night else P["sky"])
    if not night:
        flat(ctx, lambda c: p_ellipse(c, 900, 200, 120, 120), P["sun"], BG_OUT)
    layer(0.55)
    for x, s in ((-200, 1.3), (500, 1.0), (1200, 1.4)):
        stroke(ctx, [(x, 1500), (x + 20, 700)], 60 * s, color=C["trunk"])
        for dx, dy, r in ((-150, -50, 200), (100, -150, 230), (180, 40, 190), (-30, -260, 200)):
            shape(ctx, lambda c, dx=dx, dy=dy, r=r, x=x, s=s: p_ellipse(c, x + dx * s, 650 + dy * s, r * s,
                                                                         r * s * 0.8),
                  C["garden_dk"] if night else C["garden"], BG_OUT, (0.1, 0.15))
    flat(ctx, lambda c: c.rectangle(-2000, 1250, 5000, 900), C["garden_dk"])
    layer(1.0)
    # glass glare + window frame
    for x in (-60, 640):
        ctx.save()
        p_poly(ctx, [(x, 0), (x + 120, 0), (x - 200, 1450), (x - 320, 1450)])
        src(ctx, (1, 1, 1), 0.18)
        ctx.fill()
        ctx.restore()
    for x in (-260, 520, 1300):
        shape(ctx, lambda c, x=x: c.rectangle(x, -600, 80, 2100), C["sillw"], BG_OUT, (0.15, 0))
    shape(ctx, lambda c: c.rectangle(-700, 1380, 3000, 120), C["sillw"], BG_OUT, (0, 0.2))
    flat(ctx, lambda c: c.rectangle(-700, 1500, 3000, 600), C["sill_dk"])
    flat(ctx, lambda c: c.rectangle(-700, 1500, 3000, 70), C["sillw"])
    stroke(ctx, [(-700, 1500), (2300, 1500)], BG_OUT)
    for x in (120, 760, 1180):
        flat(ctx, lambda c, x=x: p_ellipse(c, x, 1540, 40, 10), C["sill_dk"])


SCENES = {"bathroom": bathroom, "bedroom": bedroom, "fibers": fibers, "skin": skin, "study": study, "sill": sill}


# ================================================================= props

def book(ctx, t, p):
    """A big open book lying on the floor, seen from the front-above; base at y = 0, about 900 wide.
    p: holes (0..1 silverfish damage: thin patches and ragged holes), glue (0..1 shows the glued spine)."""
    shape(ctx, lambda c: p_poly(c, [(-470, 0), (470, 0), (450, -60), (-450, -60)]), C["book1"], OUT, (0, 0.2))
    for s in (-1, 1):
        page = lambda c, s=s: p_smooth(c, [(0, -40), (s * 200, -90), (s * 440, -70), (s * 440, -420),
                                           (s * 220, -440), (0, -400)])
        shape(ctx, page, P["paper"], OUT, (0.05 * s, 0.08))
        for r in range(6):
            y = -360 + r * 50
            stroke(ctx, [(s * 60, y + 10), (s * 380, y)], 7, a=0.55)
    hl = p.get("holes", 0.0)
    if hl > 0:
        rng = random.Random(4)
        for k in range(9):
            x, y = rng.uniform(-400, 400), rng.uniform(-380, -100)
            r = (25 + 40 * rng.random()) * min(1, hl * 1.5 - k * 0.05)
            if r > 2:
                shape(ctx, lambda c, x=x, y=y, r=r: p_blob(c, x, y, r, r * 0.8, 0.25, seed=k), darker(P["paper"], 0.55),
                      OUT * 0.4, None)
    g = p.get("glue", 0.0)
    if g > 0:
        stroke(ctx, [(0, -40), (0, -400)], 26, color=hexc("#f0d58a"), a=g)


def trex(ctx, t, p):
    """A cartoon T. rex (side view, facing right), feet at y = 0, ~1400 tall. p: roar (0..1), mood."""
    roar = p.get("roar", 0.0)
    bob = 8 * math.sin(t * 2)
    ctx.translate(0, bob)
    shape(ctx, lambda c: p_smooth(c, [(-900, -700), (-400, -820), (-100, -900), (60, -800), (20, -560),
                                      (-300, -500), (-600, -560)]), C["rex"], OUT, (0.05, 0.15))
    shape(ctx, lambda c: p_blob(c, -120, -760, 300, 230, 0.05, seed=1), C["rex"], OUT, (0.1, 0.15))
    for s, ox in ((-1, -90), (1, 40)):
        col = C["rex_dk"] if s < 0 else C["rex"]
        shape(ctx, lambda c, ox=ox, col=col: p_ellipse(c, -170 + ox, -560, 140, 190, 0.3), col, OUT, (0.1, 0.1))
        limb(ctx, [(-160 + ox, -440), (-80 + ox, -230), (-150 + ox, -20)], 80, col, OUT)
        shape(ctx, lambda c, ox=ox: p_ellipse(c, -110 + ox, -14, 120, 36), C["rex_dk"], OUT * 0.7, None)
    shape(ctx, lambda c: p_blob(c, -60, -680, 180, 140, 0.05, seed=2), C["rex_belly"], OUT * 0.7, None)
    limb(ctx, [(60, -760), (120, -700), (170, -730)], 26, C["rex"], OUT * 0.7)   # tiny arm
    ctx.save()
    ctx.translate(150, -1000)
    ctx.rotate(-0.25 * roar)
    shape(ctx, lambda c: p_rrect(c, -170, -150, 430, 230, 90), C["rex"], OUT, (0.08, 0.15))
    jaw = 60 + 120 * roar
    shape(ctx, lambda c: p_rrect(c, -110, 30, 340, 80 + jaw * 0.2, 40), C["rex_dk"], OUT, None)
    if roar > 0.05:
        flat(ctx, lambda c: p_rrect(c, -60, 60, 280, jaw * 0.6, 20), (0.45, 0.08, 0.08), OUT * 0.6)
    for k in range(6):
        x = -60 + k * 50
        flat(ctx, lambda c, x=x: p_poly(c, [(x, 70), (x + 26, 70), (x + 13, 100)]), (1, 1, 1), OUT * 0.4)
    eyes(ctx, 40, -70, 34, 0.1, p.get("look", (1, 0)), p.get("mood", "angry"), p.get("blink", 0), OUT * 0.6,
         lid=C["rex"])
    ctx.restore()


def sleeper(ctx, t, p):
    """A generic sleeping person's head on a pillow (no likeness), lying in bed: base y = 0 is the pillow's
    bottom, head centre about (0, -170). p: zz (0..1 shows snore bubbles), skin."""
    sk = p.get("skin", P["skin2"])
    shape(ctx, lambda c: p_blob(c, 0, -90, 260, 100, 0.05, seed=2), C["pillow"], OUT, (0.08, 0.2))
    breath = 1 + 0.02 * math.sin(t * 1.6)
    shape(ctx, lambda c: p_ellipse(c, 0, -190, 150 * breath, 140), sk, OUT, (0.1, 0.08))
    shape(ctx, lambda c: p_smooth(c, [(-150, -170), (-120, -300), (0, -340), (120, -300), (150, -200),
                                      (60, -270), (-60, -260)]), P["hair"], OUT * 0.8, (0.1, 0.1))
    for s in (-1, 1):
        stroke(ctx, [(s * 70 - 30, -200), (s * 70, -186), (s * 70 + 30, -200)], 8, smooth=True)
    mouth(ctx, 0, -120, 40, "o" if p.get("snore") else "flat", 0, OUT * 0.6)
    z = p.get("zz", 0.0)
    if z > 0:
        for k in range(3):
            u = (t * 0.6 + k / 3) % 1
            shape(ctx, lambda c, u=u, k=k: p_ellipse(c, 160 + 120 * u, -300 - 260 * u, 18 + 22 * u, 18 + 22 * u),
                  (1, 1, 1), OUT * 0.5, None, a=z * (1 - u))
    shape(ctx, lambda c: p_smooth(c, [(-300, -40), (0, -70), (500, -60), (900, -30), (900, 10), (-300, 10)]),
          C["blanket"], OUT, (0.05, 0.2))


def pillow_face(ctx, t, p):
    """A huge close-up cheek with pores as a curved landscape edge (for the face-mite zoom), base y = 0."""
    shape(ctx, lambda c: p_ellipse(c, 0, 500, 900, 700), P["skin2"], OUT, (0.06, 0.1))
    rng = random.Random(1)
    for _ in range(26):
        x, y = rng.uniform(-600, 600), rng.uniform(-50, 600)
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 9, 6), P["skin2_dk"])


ACTORS = {"book": book, "trex": trex, "sleeper": sleeper, "pillow_face": pillow_face}
