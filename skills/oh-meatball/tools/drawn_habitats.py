"""Parametric habitat kit for tools/drawn.py: every habitat is a recipe (backdrop + ground + props) that a
config can recolour, re-prop and re-light. Use it as a scene: "scene": "kitchen", "scene_p": {"time": "night",
"props": [["plant", 900, 1500, 1.0]], "palette": {"wall": "#88aacc"}, "add": [...]}.

Kinds: bedroom, kitchen, bathroom, basement, sill, garden, forest_floor, reef, ocean, deep, desert, swamp, cave,
microscope, office, press, ship_deck, plus the macro worlds fibers (pillow fabric) and skin (pores) and study.
The older hand-drawn rooms (bedroom, bathroom, basement, sill, ocean, deep, office, press, fibers, skin, study)
are wrapped so they also take "time". time: day | dusk | night (a light grade over the whole frame).
FLOOR[kind] is the world y Meatball stands on; WATER kinds want his diving helmet.
Props: window, cabinets, counter, fridge, stove, table, plant, crate, lamp, tree, bush, flowers, fence, grass,
rock, log, mushroom, fern, coral, seaweed, shell, cactus, dune, reeds, lily, stalactite, stalagmite, crystal,
railing, mast, lifebuoy, barrel, cells.
"""
import math
import random

from drawn_kit import BG_OUT, OUT, PAL, darker, flat, hexc, ink, lighter, p_blob, p_ellipse, p_poly, p_rrect, \
    p_smooth, shape, src, stroke
from drawn_assets import SCENES as OLD1
from drawn_rooms import SCENES as OLD2

FLOOR = {"skin": 1100, "office": 1540, "press": 1600, "fibers": 1480}
WATER = {"reef", "ocean", "deep"}
TIME = {"day": None, "dusk": (0.95, 0.45, 0.25, 0.16), "night": (0.05, 0.08, 0.22, 0.30)}

DEFAULT_PAL = {
    "kitchen": {"wall": "#f2e3b8", "wall2": "#e8d6a4", "floor": "#c98f5a", "floor2": "#b07a48", "wood": "#d9a066"},
    "garden": {"sky": "#8fd3f4", "ground": "#7cc46a", "ground2": "#5aa54d", "dirt": "#8a6a44"},
    "forest_floor": {"sky": "#3e6b48", "ground": "#6b4a2f", "ground2": "#57391f", "leaf": "#c9822e"},
    "reef": {"sky": "#2f9fd0", "ground": "#e9d8a6", "ground2": "#d8c48c"},
    "desert": {"sky": "#ffd9a0", "ground": "#e8b86a", "ground2": "#d49f50"},
    "swamp": {"sky": "#9fb8a0", "ground": "#5d6b3a", "ground2": "#4a5530", "water": "#5f7a5a"},
    "cave": {"sky": "#3a3240", "ground": "#5a5060", "ground2": "#4a4250"},
    "microscope": {"sky": "#101418", "ground": "#d9f0e8", "ground2": "#bfe3d6"},
    "ship_deck": {"sky": "#8fd3f4", "ground": "#b88a5a", "ground2": "#9a6e44", "sea": "#2f7fc0"},
}


def _pal(kind, p):
    d = dict(DEFAULT_PAL.get(kind, {}))
    d.update(p.get("palette", {}))
    return {k: hexc(v) for k, v in d.items()}


# ================================================================= props (x, y = base on the ground)

def _window(ctx, x, y, s, P, t, time):
    w, h = 320 * s, 280 * s
    y0 = y - h
    shape(ctx, lambda c: c.rectangle(x - 20, y0 - 20, w + 40, h + 40), PAL["wood"], BG_OUT, None)
    sky = {"night": hexc("#22305a"), "dusk": hexc("#f5a06a")}.get(time, PAL["sky"])
    flat(ctx, lambda c: c.rectangle(x, y0, w, h), sky)
    if time == "night":
        flat(ctx, lambda c: p_ellipse(c, x + w * 0.7, y0 + h * 0.3, 40 * s, 40 * s), hexc("#f4f1d0"))
    else:
        flat(ctx, lambda c: p_ellipse(c, x + w * 0.7, y0 + h * 0.3, 50 * s, 50 * s), PAL["sun"])
    stroke(ctx, [(x + w / 2, y0), (x + w / 2, y0 + h)], BG_OUT)
    stroke(ctx, [(x, y0 + h / 2), (x + w, y0 + h / 2)], BG_OUT)


def _cabinets(ctx, x, y, s, P, t, time):
    for k in range(4):
        shape(ctx, lambda c, k=k: p_rrect(c, x + k * 230 * s, y - 330 * s, 220 * s, 300 * s, 10), P.get("wood", PAL["wood"]),
              BG_OUT, (0.1, 0))
        flat(ctx, lambda c, k=k: p_rrect(c, x + k * 230 * s + 170 * s, y - 200 * s, 20 * s, 60 * s, 6), PAL["steel"], 3)


def _counter(ctx, x, y, s, P, t, time):
    w = 900 * s
    shape(ctx, lambda c: c.rectangle(x, y - 470 * s, w, 470 * s), P.get("wood", PAL["wood"]), BG_OUT, (0.08, 0))
    shape(ctx, lambda c: c.rectangle(x - 20, y - 500 * s, w + 40, 40 * s), hexc("#e6e2da"), BG_OUT, (0, 0.3))
    for k in range(3):
        shape(ctx, lambda c, k=k: p_rrect(c, x + 30 * s + k * 290 * s, y - 430 * s, 260 * s, 180 * s, 8),
              lighter(P.get("wood", PAL["wood"]), 0.15), BG_OUT * 0.7, None)


def _fridge(ctx, x, y, s, P, t, time):
    shape(ctx, lambda c: p_rrect(c, x, y - 1100 * s, 420 * s, 1100 * s, 30), hexc("#eef2f4"), BG_OUT, (0.1, 0))
    stroke(ctx, [(x, y - 720 * s), (x + 420 * s, y - 720 * s)], BG_OUT)
    for yy in (y - 900 * s, y - 560 * s):
        flat(ctx, lambda c, yy=yy: p_rrect(c, x + 360 * s, yy, 20 * s, 120 * s, 8), PAL["steel"], 3)


def _stove(ctx, x, y, s, P, t, time):
    shape(ctx, lambda c: c.rectangle(x, y - 480 * s, 460 * s, 480 * s), hexc("#e6e6e6"), BG_OUT, (0.08, 0))
    shape(ctx, lambda c: c.rectangle(x + 40 * s, y - 380 * s, 380 * s, 260 * s), hexc("#3a3a3a"), BG_OUT, None)
    for k in range(2):
        flat(ctx, lambda c, k=k: p_ellipse(c, x + (130 + 200 * k) * s, y - 500 * s, 70 * s, 18 * s), hexc("#2a2a2a"), 3)


def _table(ctx, x, y, s, P, t, time):
    shape(ctx, lambda c: c.rectangle(x - 300 * s, y - 520 * s, 600 * s, 40 * s), PAL["wood"], BG_OUT, (0, 0.3))
    for dx in (-270, 240):
        shape(ctx, lambda c, dx=dx: c.rectangle(x + dx * s, y - 480 * s, 30 * s, 480 * s), PAL["wood_dk"], BG_OUT, None)


def _plant(ctx, x, y, s, P, t, time):
    shape(ctx, lambda c: p_poly(c, [(x - 90 * s, y - 200 * s), (x + 90 * s, y - 200 * s), (x + 70 * s, y), (x - 70 * s, y)]),
          hexc("#c0623c"), BG_OUT, (0.1, 0))
    for k in range(6):
        a = -math.pi / 2 + (k - 2.5) * 0.35 + 0.05 * math.sin(t + k)
        shape(ctx, lambda c, a=a: p_ellipse(c, x + 150 * s * math.cos(a), y - 200 * s + 150 * s * math.sin(a), 60 * s,
                                            26 * s, a), hexc("#4f9a4a"), BG_OUT * 0.8, (0, 0.2))


def _crate(ctx, x, y, s, P, t, time):
    shape(ctx, lambda c: p_rrect(c, x, y - 300 * s, 320 * s, 300 * s, 8), PAL["box"], BG_OUT, (0.14, 0.1))
    stroke(ctx, [(x, y - 150 * s), (x + 320 * s, y - 150 * s)], 4, color=PAL["box_dk"])


def _lamp(ctx, x, y, s, P, t, time):
    stroke(ctx, [(x, y), (x, y - 700 * s)], 10)
    shape(ctx, lambda c: p_poly(c, [(x - 110 * s, y - 640 * s), (x + 110 * s, y - 640 * s), (x + 60 * s, y - 800 * s),
                                    (x - 60 * s, y - 800 * s)]), hexc("#f2c75c"), BG_OUT, (0.1, 0))


def _tree(ctx, x, y, s, P, t, time):
    stroke(ctx, [(x, y), (x + 20 * s, y - 700 * s)], 90 * s, color=hexc("#7a5233"))
    for dx, dy, r in ((-160, -650, 220), (120, -780, 250), (200, -560, 200), (-20, -920, 210)):
        shape(ctx, lambda c, dx=dx, dy=dy, r=r: p_ellipse(c, x + dx * s, y + dy * s, r * s, r * s * 0.8),
              P.get("leaf", hexc("#5aa54d")), BG_OUT, (0.1, 0.15))


def _bush(ctx, x, y, s, P, t, time):
    for dx, r in ((-120, 130), (0, 170), (130, 120)):
        shape(ctx, lambda c, dx=dx, r=r: p_ellipse(c, x + dx * s, y - r * s * 0.7, r * s, r * s * 0.8), hexc("#4f9a4a"),
              BG_OUT, (0.1, 0.15))


def _flowers(ctx, x, y, s, P, t, time):
    for k in range(5):
        fx = x + (k - 2) * 70 * s
        h = (160 + 40 * (k % 2)) * s
        stroke(ctx, [(fx, y), (fx + 6 * math.sin(t + k), y - h)], 8, color=hexc("#3c7a46"))
        shape(ctx, lambda c, fx=fx, h=h, k=k: p_ellipse(c, fx, y - h, 32 * s, 32 * s),
              hexc(("#f25c7a", "#f2c23c", "#a070e0")[k % 3]), BG_OUT * 0.7, None)


def _fence(ctx, x, y, s, P, t, time):
    for k in range(8):
        shape(ctx, lambda c, k=k: p_poly(c, [(x + k * 130 * s, y), (x + k * 130 * s, y - 420 * s),
                                             (x + k * 130 * s + 50 * s, y - 470 * s), (x + k * 130 * s + 100 * s, y - 420 * s),
                                             (x + k * 130 * s + 100 * s, y)]), hexc("#f4efe4"), BG_OUT, (0.1, 0))


def _grass(ctx, x, y, s, P, t, time):
    for k in range(9):
        gx = x + (k - 4) * 40 * s
        stroke(ctx, [(gx, y), (gx + 20 * math.sin(t * 1.5 + k), y - (90 + 30 * (k % 3)) * s)], 10,
               color=darker(P.get("ground", hexc("#7cc46a")), 0.8))


def _rock(ctx, x, y, s, P, t, time):
    shape(ctx, lambda c: p_blob(c, x, y - 70 * s, 160 * s, 90 * s, 0.12, seed=int(x)), PAL["rock"], BG_OUT, (0.1, 0.2),
          hi=(0.3, 0.3, 0.2))


def _log(ctx, x, y, s, P, t, time):
    shape(ctx, lambda c: p_rrect(c, x - 400 * s, y - 180 * s, 800 * s, 180 * s, 90 * s), hexc("#7a5233"), BG_OUT, (0, 0.2))
    shape(ctx, lambda c: p_ellipse(c, x + 400 * s, y - 90 * s, 50 * s, 90 * s), hexc("#c9a06a"), BG_OUT, None)


def _mushroom(ctx, x, y, s, P, t, time):
    shape(ctx, lambda c: c.rectangle(x - 25 * s, y - 160 * s, 50 * s, 160 * s), hexc("#f4efe4"), BG_OUT, None)
    shape(ctx, lambda c: p_smooth(c, [(x - 130 * s, y - 150 * s), (x, y - 280 * s), (x + 130 * s, y - 150 * s)]),
          hexc("#d8322a"), BG_OUT, (0.1, 0.1))


def _fern(ctx, x, y, s, P, t, time):
    for k in range(5):
        a = -math.pi / 2 + (k - 2) * 0.4
        ex, ey = x + 360 * s * math.cos(a), y + 360 * s * math.sin(a)
        stroke(ctx, [(x, y), ((x + ex) / 2 + 20 * math.sin(t + k), (y + ey) / 2), (ex, ey)], 14, smooth=True,
               color=hexc("#3c8a46"))


def _coral(ctx, x, y, s, P, t, time):
    col = hexc(("#f2708a", "#f2a03c", "#a070e0")[int(x) % 3])
    for k, (dx, h) in enumerate(((-80, 300), (0, 420), (90, 340))):
        stroke(ctx, [(x + dx * s, y), (x + dx * s + 30 * math.sin(k), y - h * s)], 70 * s + 2 * OUT, smooth=True)
        stroke(ctx, [(x + dx * s, y), (x + dx * s + 30 * math.sin(k), y - h * s)], 70 * s, smooth=True, color=col)


def _seaweed(ctx, x, y, s, P, t, time):
    pts = [(x + 30 * math.sin(t * 1.5 + k * 0.8) * k / 6, y - k * 90 * s) for k in range(8)]
    stroke(ctx, pts, 40 * s + 2 * OUT, smooth=True)
    stroke(ctx, pts, 40 * s, smooth=True, color=hexc("#3c9a5a"))


def _shell(ctx, x, y, s, P, t, time):
    shape(ctx, lambda c: p_smooth(c, [(x - 80 * s, y), (x, y - 110 * s), (x + 80 * s, y)]), hexc("#f2d0b0"), BG_OUT, None)


def _cactus(ctx, x, y, s, P, t, time):
    shape(ctx, lambda c: p_rrect(c, x - 60 * s, y - 600 * s, 120 * s, 600 * s, 60 * s), hexc("#5aa54d"), BG_OUT, (0.1, 0))
    for sd in (-1, 1):
        shape(ctx, lambda c, sd=sd: p_rrect(c, x + sd * 60 * s - (100 * s if sd < 0 else 0), y - 380 * s, 100 * s, 50 * s,
                                            25 * s), hexc("#5aa54d"), BG_OUT, None)
        shape(ctx, lambda c, sd=sd: p_rrect(c, x + sd * 140 * s - 25 * s, y - 520 * s, 50 * s, 180 * s, 25 * s),
              hexc("#5aa54d"), BG_OUT, None)


def _dune(ctx, x, y, s, P, t, time):
    shape(ctx, lambda c: p_smooth(c, [(x - 900 * s, y), (x, y - 300 * s), (x + 900 * s, y)], close=True),
          P.get("ground2", hexc("#d49f50")), BG_OUT, None)


def _reeds(ctx, x, y, s, P, t, time):
    for k in range(7):
        rx = x + (k - 3) * 45 * s
        top = (y - (500 + 80 * (k % 3)) * s)
        stroke(ctx, [(rx, y), (rx + 15 * math.sin(t + k), top)], 12, color=hexc("#7a8a3c"))
        shape(ctx, lambda c, rx=rx, top=top, k=k: p_rrect(c, rx - 16 + 15 * math.sin(t + k), top, 32, 110 * s, 16),
              hexc("#6b4a2f"), 4, None)


def _lily(ctx, x, y, s, P, t, time):
    shape(ctx, lambda c: p_ellipse(c, x, y - 10, 150 * s, 40 * s), hexc("#4f9a4a"), BG_OUT, None)


def _stalactite(ctx, x, y, s, P, t, time):
    shape(ctx, lambda c: p_poly(c, [(x - 80 * s, -400), (x + 80 * s, -400), (x, y)]), P.get("ground2", PAL["rock"]),
          BG_OUT, (0.1, 0))


def _stalagmite(ctx, x, y, s, P, t, time):
    shape(ctx, lambda c: p_poly(c, [(x - 100 * s, y), (x + 100 * s, y), (x + 10, y - 500 * s)]), P.get("ground2", PAL["rock"]),
          BG_OUT, (0.1, 0))


def _crystal(ctx, x, y, s, P, t, time):
    for k, a in enumerate((-0.4, 0, 0.35)):
        ctx.save()
        ctx.translate(x + k * 40 * s, y)
        ctx.rotate(a)
        shape(ctx, lambda c: p_poly(c, [(-35 * s, 0), (-35 * s, -220 * s), (0, -290 * s), (35 * s, -220 * s), (35 * s, 0)]),
              hexc("#9fe3f0"), BG_OUT, (0.15, 0), a=0.9)
        ctx.restore()


def _railing(ctx, x, y, s, P, t, time):
    stroke(ctx, [(x - 2000, y - 380 * s), (x + 2000, y - 380 * s)], 22, color=PAL["steel"])
    for k in range(-12, 13):
        stroke(ctx, [(x + k * 160, y), (x + k * 160, y - 380 * s)], 14, color=PAL["steel_dk"])


def _mast(ctx, x, y, s, P, t, time):
    stroke(ctx, [(x, y), (x, y - 1600 * s)], 50 * s, color=PAL["wood_dk"])
    stroke(ctx, [(x - 300 * s, y - 1300 * s), (x + 300 * s, y - 1300 * s)], 30 * s, color=PAL["wood_dk"])


def _lifebuoy(ctx, x, y, s, P, t, time):
    ctx.save()
    ctx.new_sub_path()
    ctx.arc(x, y - 500 * s, 110 * s, 0, 2 * math.pi)
    ink(ctx, 60 * s + 2 * OUT)
    ctx.stroke()
    for k in range(4):
        ctx.new_sub_path()
        ctx.arc(x, y - 500 * s, 110 * s, k * math.pi / 2, (k + 0.5) * math.pi / 2 + math.pi / 4)
        src(ctx, PAL["red"] if k % 2 == 0 else (1, 1, 1))
        ctx.set_line_width(60 * s)
        ctx.stroke()
    ctx.restore()


def _barrel(ctx, x, y, s, P, t, time):
    shape(ctx, lambda c: p_rrect(c, x - 130 * s, y - 380 * s, 260 * s, 380 * s, 60 * s), PAL["wood"], BG_OUT, (0.12, 0))
    for yy in (y - 300 * s, y - 80 * s):
        stroke(ctx, [(x - 128 * s, yy), (x + 128 * s, yy)], 12, color=PAL["steel_dk"])


def _cells(ctx, x, y, s, P, t, time):
    rng = random.Random(int(x))
    for _ in range(9):
        cx, cy = x + rng.uniform(-500, 500) * s, y + rng.uniform(-900, -100) * s
        r = rng.uniform(50, 120) * s
        shape(ctx, lambda c, cx=cx, cy=cy, r=r: p_blob(c, cx + 10 * math.sin(t + cx), cy, r, r * 0.8, 0.12, seed=int(cx)),
              hexc("#a8e0c8"), BG_OUT * 0.6, None, a=0.7)
        flat(ctx, lambda c, cx=cx, cy=cy, r=r: p_ellipse(c, cx + 10 * math.sin(t + cx), cy, r * 0.3, r * 0.3),
             hexc("#5aa58a"), a=0.8)


PROPS = {k[1:]: v for k, v in globals().items() if k.startswith("_") and callable(v) and k not in ("_pal",)}


# ================================================================= recipes

RECIPES = {
    "kitchen": {"back": "wall", "ground": "tile", "props": [["window", 700, 900, 1.0], ["cabinets", -150, 700, 1.0],
                                                            ["counter", -200, 1500, 1.0], ["fridge", 1220, 1500, 1.0]]},
    "garden": {"back": "sky", "ground": "grass", "props": [["tree", -100, 1300, 1.0], ["fence", 200, 1320, 0.9],
                                                           ["bush", 1150, 1500, 1.0], ["flowers", 950, 1500, 1.0],
                                                           ["grass", 300, 1500, 1.0]]},
    "forest_floor": {"back": "trees", "ground": "leaves", "props": [["log", 1100, 1500, 1.0], ["mushroom", -60, 1500, 1.2],
                                                                    ["fern", 1250, 1500, 1.0], ["rock", 120, 1500, 0.8]]},
    "reef": {"back": "water", "ground": "sand", "props": [["coral", -60, 1500, 1.2], ["coral", 1160, 1500, 1.0],
                                                          ["seaweed", 980, 1500, 1.2], ["seaweed", 120, 1500, 1.0],
                                                          ["shell", 700, 1500, 1.0]]},
    "desert": {"back": "sky", "ground": "sand", "props": [["dune", 900, 1320, 1.2], ["cactus", 1150, 1500, 1.0],
                                                          ["rock", -40, 1500, 0.9]]},
    "swamp": {"back": "haze", "ground": "mud", "props": [["reeds", -60, 1500, 1.0], ["reeds", 1180, 1500, 1.1],
                                                         ["lily", 700, 1640, 1.0], ["log", 1000, 1360, 0.8]]},
    "cave": {"back": "rock", "ground": "stone", "props": [["stalactite", 200, 300, 1.0], ["stalactite", 900, 420, 1.2],
                                                          ["stalagmite", 1200, 1500, 1.0], ["crystal", -80, 1500, 1.0]]},
    "microscope": {"back": "lens", "ground": "slide", "props": [["cells", 540, 1500, 1.0]]},
    "ship_deck": {"back": "sea", "ground": "deck", "props": [["railing", 540, 1300, 1.0], ["mast", 1200, 1500, 1.0],
                                                             ["lifebuoy", 60, 1300, 1.0], ["barrel", 1000, 1500, 1.0]]},
}


def _backdrop(ctx, kind, back, P, t, layer, time):
    layer(0.4)
    sky = P.get("sky", hexc("#8fd3f4"))
    if time == "night" and back in ("sky", "sea", "haze"):
        sky = hexc("#1b2440")
    elif time == "dusk" and back in ("sky", "sea", "haze"):
        sky = hexc("#f5a06a")
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), P.get("wall", sky) if back == "wall" else sky)
    if back == "wall":
        for x in range(-1500, 3000, 180):
            flat(ctx, lambda c, x=x: c.rectangle(x, -2000, 70, 5000), P.get("wall2", darker(P["wall"], 0.95)))
    elif back in ("sky", "sea"):
        if time != "night":
            shape(ctx, lambda c: p_ellipse(c, 1100, 250, 110, 110), PAL["sun"], BG_OUT, None)
        layer(0.55)
        for x0, y0 in ((-200, 260), (700, 160), (1500, 330)):
            x = x0 + (t * 15) % 2400 - 400
            for dx, dy, r in ((-90, 10, 70), (0, -30, 95), (100, 5, 75)):
                shape(ctx, lambda c, x=x, dx=dx, dy=dy, r=r: p_ellipse(c, x + dx, y0 + dy, r, r * 0.8), PAL["cloud"],
                      BG_OUT * 0.8, (0, 0.18), shade_k=0.92)
        if back == "sea":
            flat(ctx, lambda c: c.rectangle(-3000, 1050, 8000, 1000), P.get("sea", PAL["sea"]))
            for row in range(3):
                pts = [(x, 1090 + row * 70 + 8 * math.sin(x / 80 + t * 1.5 + row)) for x in range(-1500, 3000, 60)]
                stroke(ctx, pts, 5, color=PAL["foam"], a=0.6)
    elif back == "trees":
        for x in range(-600, 2200, 300):
            stroke(ctx, [(x, 1500), (x + 30, -500)], 110, color=darker(sky, 0.7))
        layer(0.7)
        for x in range(-500, 2200, 420):
            stroke(ctx, [(x, 1500), (x - 20, -500)], 150, color=hexc("#5e4630"))
    elif back == "water":
        for i, c in enumerate(("#3fb0dc", "#2f9fd0", "#2486bd")):
            flat(ctx, lambda cc, i=i, c=c: cc.rectangle(-3000, -600 + i * 700, 8000, 3000), hexc(c))
        for i in range(4):
            x = -200 + i * 420 + 40 * math.sin(t * 0.5 + i)
            ctx.save()
            p_poly(ctx, [(x, -600), (x + 160, -600), (x + 420, 1600), (x + 200, 1600)])
            src(ctx, (1, 1, 1), 0.08)
            ctx.fill()
            ctx.restore()
    elif back == "haze":
        for x in range(-600, 2200, 260):
            stroke(ctx, [(x, 1500), (x + 10, 200)], 60, color=darker(sky, 0.85))
    elif back == "rock":
        rng = random.Random(4)
        for _ in range(30):
            x, y = rng.uniform(-800, 1900), rng.uniform(-600, 1500)
            flat(ctx, lambda c, x=x, y=y: p_blob(c, x, y, 160, 110, 0.15, seed=int(x)), darker(sky, 0.85))
    elif back == "lens":
        pass
    layer(1.0)


def _ground(ctx, style, P, t):
    g, g2 = P.get("ground", hexc("#8a6f55")), P.get("ground2", hexc("#735a43"))
    if style == "tile":
        g, g2 = P.get("floor", hexc("#c98f5a")), P.get("floor2", hexc("#b07a48"))
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 1000), g)
    rng = random.Random(7)
    if style == "tile":
        for x in range(-1500, 3000, 200):
            stroke(ctx, [(x, 1500), (x - 150, 2100)], 4, color=g2)
    elif style == "grass":
        for x in range(-1500, 3000, 70):
            stroke(ctx, [(x, 1500), (x + 10 * math.sin(t + x), 1460)], 10, color=g2)
    elif style == "leaves":
        for _ in range(60):
            x, y = rng.uniform(-1200, 2400), rng.uniform(1500, 2000)
            flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 50, 22, rng.uniform(0, 3)),
                 P.get("leaf", hexc("#c9822e")) if rng.random() < 0.6 else g2, 3)
    elif style == "sand":
        for _ in range(50):
            x, y = rng.uniform(-1200, 2400), rng.uniform(1520, 2000)
            flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 8, 5), g2)
    elif style == "mud":
        flat(ctx, lambda c: p_ellipse(c, 700, 1680, 700, 120), P.get("water", hexc("#5f7a5a")), BG_OUT)
    elif style == "deck":
        for y in range(1500, 2100, 70):
            stroke(ctx, [(-3000, y), (5000, y)], 4, color=g2)
    elif style == "slide":
        pass
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)


def _lens_mask(ctx):
    ctx.save()
    ctx.identity_matrix()
    ctx.set_fill_rule(1)   # even-odd: everything outside the round field goes black
    ctx.rectangle(0, 0, 1080, 1920)
    ctx.arc(540, 960, 520, 0, 2 * math.pi)
    src(ctx, hexc("#0b0d10"))
    ctx.fill()
    ctx.new_sub_path()
    ctx.arc(540, 960, 520, 0, 2 * math.pi)
    ink(ctx, 26)
    ctx.stroke()
    ctx.restore()


def _grade(ctx, time):
    tint = TIME.get(time)
    if tint:
        ctx.save()
        ctx.identity_matrix()
        ctx.rectangle(0, 0, 1080, 1920)
        src(ctx, tint[:3], tint[3])
        ctx.fill()
        ctx.restore()


def habitat(kind):
    rec = RECIPES[kind]

    def scene(ctx, t, layer, p):
        P = _pal(kind, p)
        time = p.get("time", "day")
        _backdrop(ctx, kind, rec["back"], P, t, layer, time)
        props = p.get("props", rec["props"]) + p.get("add", [])
        if rec["back"] == "lens":
            flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), P["ground"])
        else:
            _ground(ctx, rec["ground"], P, t)
        for name, x, y, s in props:
            PROPS[name](ctx, x, y, s, P, t, time)
        if rec["back"] == "lens":
            _lens_mask(ctx)
        _grade(ctx, time if rec["back"] != "lens" else "day")
    return scene


def _wrap(fn):
    def scene(ctx, t, layer, p):
        fn(ctx, t, layer, p)
        _grade(ctx, p.get("time", "day"))
    return scene


SCENES = {k: _wrap(v) for k, v in {**OLD1, **OLD2}.items()}
SCENES.update({k: habitat(k) for k in RECIPES})
