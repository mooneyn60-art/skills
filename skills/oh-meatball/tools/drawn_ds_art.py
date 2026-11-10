"""Pictures for the "Don't squish it" long-form (tools/drawn_dontsquish.py), in the locked drawn_kit style.

World actors (drawn like every drawn.py actor: origin = the actor's pos, local units, scaled by its "s"):
  carol           the long-bodied cellar spider (Pholcus phalangioides) hanging upside down: a small pale carapace,
                  a long cylinder abdomen (about 3x as long as wide), eight hair-thin legs about 5x the body with dark
                  knee rings. Origin = carapace centre. p: mood, look, blink, talk, work (hind legs spin silk), walk,
                  wave (front leg), flick (0..1 hind legs throw silk), flick_to [x, y], whirl (0..1 the blur),
                  eggs (0..1 bundle in the jaws), reach (0..1 legs forward, body back), shrug, hat, shades, eyes8
                  (0..1: the three eye groups drawn big for the face close-up), still (no idle sway)
  ds_web          a messy cellar-spider tangle in a ceiling corner (origin = the corner); p: w, h, dust (0..1), seed
  giant_spider    the giant house spider (Eratigena): big, hairy, banded long legs, 3/4 side view on the ground
                  (origin = feet line); p: walk, wrapped (0..1 silk bundle), mood, look
  ds_shadow       a long dark shadow of the giant house spider walking (floor-level shot)
  house_sp_small  the common house spider (Tegenaria domestica), small, for piles and lineups; p: dead, wrapped
  crane_fly       crane fly: insect, six long legs, two long wings, three body parts
  woodlouse       a woodlouse (segmented grey shell, 14 short legs); p: wrapped, walk
  false_widow     noble false widow (Steatoda nobilis): bulbous brown abdomen with a cream "skull" band
  redback         redback: black widow body with the red stripe on the back
  ds_tag          a paper name tag on a thread; p: text, on (0..1 pop)
  ds_dim          a measuring bracket from (0, 0) to p["to"] with a label; p: grow, text
  ds_label        a world-space label pill; p: text, color, on
  ds_prop         simple props by p["kind"]: vacuum, broom, jar, paper, spray, caulk, calendar, growth, radiator,
                  door, plate, tweezers, tray, contract, lamp_blaze, bill, bottle, cricket, box, tv, suitcase
  ds_board        the shed leftovers board: 102 remains that sort into piles; p: n (0..102), sort (0..1), sort2 (0..1)
  ds_pie          a pie chart: p: frac (0..1 sweep), label
  ds_lineup       a police-lineup wall with height lines and three spots; p: lit [0..1 x3]
  ds_map          a plain map card with a pin: p: place (KANSAS | BRITAIN | CALIFORNIA | FINLAND | AUSTRALIA), pin (0..1)
  ds_arena        a clear lab arena (petri box); p: grey (0..1 a lost round)
  ds_houses       a row of little houses; p: n, lit (0..1 share lit), stamp text
  ds_chip_src     a source chip pill (e.g. "PENN STATE EXTENSION"); p: text, on
Scenes: ds_corner (the bedroom ceiling corner at night), ds_floor (floorboards at night, low camera), ds_lab,
ds_shed, ds_wall (a plain night wall for the dramatised hunt), ds_board_bg (a dark card background)
Screen overlays (identity matrix, drawn by drawn_dontsquish): see that module.
"""
import math
import random

import cairo

from drawn_kit import (BG_OUT, INK, OUT, PAL, back_out, darker, ease, eyes, flat, hexc, ink, lighter, limb, mouth,
                       p_blob, p_ellipse, p_poly, p_rrect, p_smooth, shape, src, stroke)
import drawn_anatomy
from drawn_bugs import _wrapped

C = {k: hexc(v) for k, v in {
    "cell": "#e2d3b0", "cell_dk": "#bda983", "cell_leg": "#cdb994", "cell_knee": "#5b4a35", "cell_mark": "#9c8461",
    "ceil": "#8d97bf", "ceil_dk": "#7c86ae", "paperL": "#6f7fae", "paperL2": "#6576a3", "paperR": "#5d6c98",
    "paperR2": "#55638d", "mould": "#e6e1d3", "mould_dk": "#c9c2b0", "lamp": "#f2c75c",
    "shoe": "#d8322a", "shoe_dk": "#a92620", "sole": "#f1ece2", "sole_dk": "#cfc6b5", "tread": "#7d7466",
    "giant": "#7b5a3c", "giant_dk": "#4f3824", "giant_band": "#3e2c1c", "giant_lt": "#a98660",
    "wood1": "#9a6a3e", "wood2": "#8a5c33", "wood3": "#a87646", "board": "#2c3a33", "chalk": "#f2f2ea",
    "lab_wall": "#dfe7ea", "lab_wall2": "#cfdadf", "lab_bench": "#9aa7b0", "lab_bench_dk": "#7d8a93",
    "shed1": "#7a5636", "shed2": "#6b4a2e", "shed3": "#86613f",
    "lice": "#8d939b", "lice_dk": "#5f656d", "crane": "#a8865a", "crane_dk": "#7a5e3a", "wing": "#d8ecf7",
    "fw": "#6e4630", "fw_dk": "#4a2c1c", "fw_mark": "#efe0bf", "red": "#e5383b", "green": "#3fb950",
    "yellow": "#ffd34d", "map": "#d9cfb2", "map_dk": "#b9ad8c", "sea": "#9cc3d8",
}.items()}

_TXT = {}


def text(ctx, s, x, y, px, color="#ffffff", stroke_w=None, a=1.0, rot=0.0):
    """Anton text centred at (x, y) in the current (world or screen) frame, via drawn_keepkill.text_img."""
    import drawn_keepkill as kk
    im = kk.text_img(s, int(px), color, stroke_w, rot)
    kk.blit(ctx, im, x, y, 1.0, a)
    return im[0].get_width(), im[0].get_height()


# ================================================================================================ Carol

def _leg3(ctx, pts, w, col, lw, knee_k=1.0):
    limb(ctx, pts, w, col, lw, smooth=False)
    kx, ky = pts[1]
    ax, ay = pts[2]
    # Pholcus knee: a dark ring at the femur tip, a pale ring just after (its signature "knees")
    flat(ctx, lambda c: p_ellipse(c, kx, ky, w * 1.15 * knee_k, w * 1.15 * knee_k), C["cell_knee"])
    t2 = (kx + (ax - kx) * 0.07, ky + (ay - ky) * 0.07)
    flat(ctx, lambda c: p_ellipse(c, t2[0], t2[1], w * 0.95, w * 0.95), (1, 1, 1), a=0.9)


# leg fan for the right side, front (I) to back (IV): femur (len, deg above horizontal), tibia (len, deg), tarsus
LEGS = [((330, 80), (470, 34), (330, 52)),
        ((290, 60), (420, 10), (290, 22)),
        ((240, 34), (340, -20), (250, -6)),
        ((260, 12), (380, -40), (270, -28))]


def _carol_body(ctx, t, p, ox=0.0, oy=0.0, alpha=1.0):
    """One drawing of Carol, offset by (ox, oy). Legs first, then the abdomen, the carapace and the face."""
    still = p.get("still", False)
    sway = 0.0 if still else 5 * math.sin(t * 1.5)
    bx, by = ox + (-90 * p.get("reach", 0.0)) * p.get("reach_dir", 1), oy + sway
    work = p.get("work", 0.0)
    walk = 1.0 if p.get("walking") else p.get("walk", 0.0)
    flick = p.get("flick", 0.0)
    wave = p.get("wave", 0.0)
    shrug = p.get("shrug", 0.0)
    reach = p.get("reach", 0.0)
    w, lw = 7.0, 3.6
    tips = {}
    for side in (-1, 1):
        for i, (fem, tib, tar) in enumerate(LEGS):
            hx, hy = bx + side * (14 - i * 3), by + 8 + i * 4
            fa = math.radians(fem[1])
            ta = math.radians(tib[1])
            ra = math.radians(tar[1])
            q = t * 9 + i * 1.7 + (side > 0) * 3.1
            sw = 0.10 * math.sin(q) * walk
            if i == 3:   # the hind legs: spin silk (work) and throw it (flick), alternating left / right
                ph = t * 7 + (0 if side > 0 else math.pi)
                sw += 0.42 * work * math.sin(t * 6 + side)
                sw += 0.55 * flick * max(0.0, math.sin(ph))
            if i < 2 and shrug:
                sw += 0.35 * shrug * (0.5 + 0.5 * math.sin(t * 5))
            if i == 0 and side > 0 and wave:
                sw += 0.6 * wave * (0.6 + 0.4 * math.sin(t * 9))
            if i < 2 and reach:
                ta -= 0.25 * reach
            fa += sw * 0.6
            k = (hx + side * fem[0] * math.cos(fa), hy - fem[0] * math.sin(fa))
            a2 = (k[0] + side * tib[0] * math.cos(ta - sw * 0.4), k[1] - tib[0] * math.sin(ta - sw * 0.4))
            tp = (a2[0] + side * tar[0] * math.cos(ra - sw * 0.2), a2[1] - tar[0] * math.sin(ra - sw * 0.2))
            if reach and i < 2:
                tp = (tp[0] + side * 160 * reach, tp[1] + 40 * reach)
            tips[(side, i)] = tp
            col = C["cell_leg"] if i < 2 else darker(C["cell_leg"], 0.86)
            _leg3(ctx, [(hx, hy), k, a2, tp], w if i < 2 else w * 0.9, col, lw)
    # silk from the spinnerets to the working hind legs
    spin = (bx - 170, by + 110)
    if work > 0 or flick > 0:
        for side in (-1, 1):
            tp = tips[(side, 3)]
            stroke(ctx, [spin, ((spin[0] + tp[0]) / 2, (spin[1] + tp[1]) / 2 + 30), tp], 2.2, smooth=True,
                   color=(1, 1, 1), a=0.85 * max(work, flick))
    if flick > 0:   # thrown silk: thick bright strands with a blue edge so they read over the web, in alternating volleys
        tx, ty = p.get("flick_to", (700, 120))
        for side in (-1, 1):
            tp = tips[(side, 3)]
            ph = (t * 7 + (0 if side > 0 else math.pi)) % (2 * math.pi)
            u = ph / (2 * math.pi)
            for k in range(5):
                uu = min(1.0, u * 1.5 + k * 0.06)
                ex, ey = tp[0] + (tx - tp[0]) * uu, tp[1] + (ty - tp[1]) * uu
                mx, my = (tp[0] + ex) / 2 + (k - 2) * 20, (tp[1] + ey) / 2 - 140 + k * 26
                pts = [tp, (mx, my), (ex + (k - 2) * 30, ey + (k - 2) * 22)]
                a = 0.95 * flick * (1 - 0.6 * u)
                stroke(ctx, pts, 9.0, smooth=True, color=(0.45, 0.65, 0.95), a=a * 0.6)
                stroke(ctx, pts, 4.5, smooth=True, color=(1, 1, 1), a=a)
            for k in range(3):   # motion ticks at the flicking foot
                ang = 0.6 * k - 0.6
                stroke(ctx, [(tp[0] + 30 * math.cos(ang), tp[1] - 30 * math.sin(ang)),
                             (tp[0] + 70 * math.cos(ang), tp[1] - 70 * math.sin(ang))], 5, a=0.8 * flick)
    # abdomen: a long cylinder tilted down and back, shaded like a tube (dark underside, a light stripe on top,
    # three faint segment rings) so it never reads as a flat disc
    mar = p.get("marbled", 0.0)
    acol = C["cell"] if not mar else hexc("#b8ab93")
    rot = math.radians(32)
    ax_, ay_ = bx - 78, by + 52
    ctx.save()
    p_ellipse(ctx, ax_, ay_, 112, 38, rot)
    src(ctx, darker(acol, 0.62))
    ctx.fill_preserve()
    ctx.clip()
    p_ellipse(ctx, ax_ - 6, ay_ - 9, 108, 27, rot)
    src(ctx, acol)
    ctx.fill()
    p_ellipse(ctx, ax_ - 14, ay_ - 20, 80, 8, rot)
    src(ctx, lighter(acol, 0.55))
    ctx.fill()
    for k in (-50, 0, 50):
        cx_, cy_ = ax_ + k * math.cos(rot), ay_ + k * math.sin(rot)
        p_ellipse(ctx, cx_, cy_, 7, 38, rot)
        ink(ctx, 2.2, 0.35)
        ctx.stroke()
    if mar:   # marbled cellar spider: dark marbling all over
        rng = random.Random(7)
        for k in range(16):
            u = rng.uniform(-90, 90)
            flat(ctx, lambda c, u=u, k=k: p_blob(c, ax_ + u * math.cos(rot), ay_ + u * math.sin(rot) + rng.uniform(-22, 22),
                                                 rng.uniform(8, 16), rng.uniform(5, 10), 0.3, k), hexc("#5a4c3a"), a=0.75)
    ctx.restore()
    p_ellipse(ctx, ax_, ay_, 112, 38, rot)
    ink(ctx, OUT * 0.6)
    ctx.stroke()
    shape(ctx, lambda c: p_ellipse(c, bx, by, 48, 42), C["cell"], OUT * 0.6, (0.0, 0.15), hi=(0.3, 0.25, 0.25))
    flat(ctx, lambda c: p_ellipse(c, bx, by + 4, 16, 18), C["cell_mark"], a=0.75)   # the dark mark on the carapace
    # eyes: the median pair (cartoon) + two triads of side eyes, the "three little clusters"
    e8 = p.get("eyes8", 0.0)
    mood = p.get("mood", "calm")
    blink = p.get("blink", 0.0)
    eyes(ctx, bx, by - 20, 13, 14, p.get("look", (0, 0.2)), mood, blink, OUT * 0.45, lid=C["cell"])
    r3 = 5.5 + 3.5 * e8
    for side in (-1, 1):
        cx, cy = bx + side * (30 + 16 * e8), by - 30 - 4 * e8
        for j, (dx, dy) in enumerate(((0, 0), (side * 10 * (1 + 0.5 * e8), -9 * (1 + 0.5 * e8)),
                                      (side * 12 * (1 + 0.5 * e8), 8 * (1 + 0.4 * e8)))):
            bl = e8 > 0 and (math.sin(t * 3.1 + j * 2.3 + side * 1.7) > 0.93)
            if bl:
                stroke(ctx, [(cx + dx - r3, cy + dy), (cx + dx + r3, cy + dy)], 2.2)
            else:
                shape(ctx, lambda c, dx=dx, dy=dy: p_ellipse(c, cx + dx, cy + dy, r3, r3), INK, 0, None)
                flat(ctx, lambda c, dx=dx, dy=dy: p_ellipse(c, cx + dx - r3 * 0.3, cy + dy - r3 * 0.35, r3 * 0.35,
                                                             r3 * 0.35), (1, 1, 1))
    if p.get("eggs", 0.0) > 0:
        e = p["eggs"]
        ex, ey = bx + 4, by + 56
        shape(ctx, lambda c: p_ellipse(c, ex, ey, 40 * e, 36 * e), hexc("#f3ead2"), OUT * 0.5, (0.0, 0.2))
        rng = random.Random(4)
        for k in range(14):
            a, r = rng.uniform(0, 6.28), rng.uniform(0, 26)
            flat(ctx, lambda c, a=a, r=r: p_ellipse(c, ex + r * math.cos(a) * e, ey + r * math.sin(a) * e, 7 * e, 7 * e),
                 hexc("#d9c79f"), OUT * 0.15)
        for k in range(4):
            stroke(ctx, [(ex - 38 * e, ey - 10 + k * 8), (ex + 38 * e, ey - 18 + k * 10)], 1.6, color=(1, 1, 1), a=0.8)
        for s in (-1, 1):   # the chelicerae gripping it
            shape(ctx, lambda c, s=s: p_ellipse(c, bx + s * 12, by + 24, 7, 10), C["cell_dk"], OUT * 0.3, None)
    else:
        mouth(ctx, bx, by + 18, 16, p.get("mouth", "smile"), p.get("talk", 0.0), OUT * 0.4)
    if p.get("hat", 0.0) > 0:
        h = p["hat"]
        shape(ctx, lambda c: p_poly(c, [(bx - 26 * h, by - 34), (bx + 26 * h, by - 34), (bx + 4, by - 34 - 80 * h)]),
              hexc("#4fa3e0"), OUT * 0.4, (0.0, 0.2))
        for k in range(3):
            flat(ctx, lambda c, k=k: p_ellipse(c, bx - 10 + k * 9, by - 46 - k * 16, 5, 5), hexc("#ffd34d"))
        flat(ctx, lambda c: p_ellipse(c, bx + 4, by - 116 * h, 9, 9), hexc("#e5383b"))
    if p.get("hat2", 0.0) > 0:
        h = p["hat2"]
        shape(ctx, lambda c: p_poly(c, [(bx + 10, by - 100), (bx + 50 * h, by - 104), (bx + 34, by - 100 - 70 * h)]),
              hexc("#e5383b"), OUT * 0.4, (0.0, 0.2))
        flat(ctx, lambda c: p_ellipse(c, bx + 34, by - 100 - 76 * h, 8, 8), hexc("#ffd34d"))
    if p.get("bite", 0.0) > 0:
        from drawn_kit import starburst
        starburst(ctx, bx + 60, by + 40, 40 * p["bite"], 8, (1, 0.86, 0.2), OUT * 0.4, t * 3)
    if p.get("shades", 0.0) > 0:
        for s in (-1, 1):
            shape(ctx, lambda c, s=s: p_rrect(c, bx + s * 14 - 14, by - 30, 28, 18, 6), INK, OUT * 0.3, None)
        stroke(ctx, [(bx - 2, by - 24), (bx + 2, by - 24)], 3)
    return tips


def carol(ctx, t, p):
    if p.get("thread"):
        stroke(ctx, [(0, -30), (0, -p["thread"])], 3.0, color=(1, 1, 1), a=0.9)
    wh = p.get("whirl", 0.0)
    if wh <= 0.01:
        _carol_body(ctx, t, p)
        return
    # the whirl: she spins round and round in her web (BAS: "a blur"); ghosts trail around a circle
    R, om = 46 * wh, 26.0
    for k in range(6, 0, -1):
        ph = t * om - k * 0.55
        ctx.push_group()
        _carol_body(ctx, t, dict(p, still=True), R * math.cos(ph), R * math.sin(ph) * 0.8)
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(0.16 * wh)
    for r in (70, 140, 260, 420):
        ctx.save()
        ctx.new_sub_path()
        a0 = t * om * 0.5
        ctx.arc(0, 0, r * (0.6 + 0.4 * wh), a0, a0 + 4.2)
        ctx.set_source_rgba(1, 1, 1, 0.35 * wh)
        ctx.set_line_width(4)
        ctx.stroke()
        ctx.restore()
    ph = t * om
    ctx.push_group()
    _carol_body(ctx, t, dict(p, still=True, mood="shock"), R * math.cos(ph), R * math.sin(ph) * 0.8)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(1.0 - 0.45 * wh)


# ================================================================================================ web

def ds_web(ctx, t, p):
    """A cellar-spider tangle: an untidy mesh of straight, non-sticky threads hung from a ceiling corner (origin).
    p: w (half width), h (depth below the corner), dust 0..1 (grey and thick), seed, a (alpha), spread (0..1 grow)."""
    rng = random.Random(p.get("seed", 3))
    W, Hh = p.get("w", 720), p.get("h", 820)
    dust = p.get("dust", 0.0)
    g = p.get("spread", 1.0)
    col = lighter(hexc("#a9a9a9"), 0.9 - 0.6 * dust)
    a = p.get("a", 0.8)
    pts = [(0, 0)]
    for k in range(40):
        u = rng.random()
        side = -1 if k % 2 else 1
        x = side * W * (0.15 + 0.85 * rng.random()) * g
        y = Hh * (0.1 + 0.9 * rng.random() ** 1.3) * g - 0.55 * abs(x) * (1 - u * 0.5)
        pts.append((x, max(-0.4 * abs(x), y)))
    anchors = [(-W * 1.1 * g, -0.42 * W * g), (W * 1.1 * g, -0.42 * W * g), (-W * 0.6 * g, -0.25 * W * g),
               (W * 0.6 * g, -0.25 * W * g), (0, Hh * 1.1 * g), (-W * 0.9 * g, Hh * 0.5 * g), (W * 0.9 * g, Hh * 0.6 * g)]
    lw = 1.6 + 2.2 * dust
    import cairo as _c
    ctx.push_group()
    for k in range(int(p.get("n", 52))):
        p1 = pts[rng.randrange(len(pts))]
        p2 = pts[rng.randrange(len(pts))] if rng.random() < 0.75 else anchors[rng.randrange(len(anchors))]
        wob = 2.5 * math.sin(t * 1.3 + k)
        stroke(ctx, [p1, ((p1[0] + p2[0]) / 2 + wob, (p1[1] + p2[1]) / 2 + 10 + wob), p2], lw, smooth=True,
               color=col, a=a * (0.55 + 0.45 * rng.random()))
    if dust > 0:
        for k in range(int(30 * dust)):
            x, y = pts[rng.randrange(len(pts))]
            flat(ctx, lambda c, x=x, y=y: p_blob(c, x, y, 14 + 20 * rng.random(), 8 + 10 * rng.random(), 0.3, k),
                 hexc("#9a958c"), a=0.55 * dust)
    pat = ctx.pop_group()
    ctx.set_source(pat)   # the source locks to the current transform here; the mask below is in screen space
    ctx.save()
    ctx.identity_matrix()
    Hs = ctx.get_target().get_height()
    g = _c.LinearGradient(0, 0, 0, Hs)
    fc = 0.3 if p.get("fade_card") else 1.0
    for y, a_ in ((0.0, 1.0), (0.11, 1.0), (0.13, fc), (0.30, fc), (0.33, 1.0), (0.80, 1.0), (0.85, 0.28), (1.0, 0.28)):
        g.add_color_stop_rgba(y, 0, 0, 0, a_)
    ctx.mask(g)
    ctx.restore()


# ================================================================================================ other animals

GIANT = {"color": "#7b5a3c", "dark": "#4f3824", "abd": (170, 118), "mark": "giantmark", "hair": True, "leg": 1.55,
         "leg_w": 19, "knee": 1.15}


def _giant_mark(ctx, cfg, ax, ay, arx, ary):
    dk = hexc("#3e2c1c")
    lt = hexc("#a98660")
    stroke(ctx, [(ax + arx * 0.8, ay - 10), (ax - arx * 0.85, ay - 6)], 16, color=lt)
    for k in range(4):
        x = ax + 90 - k * 55
        stroke(ctx, [(x, ay - 70), (x - 26, ay - 40), (x, ay - 14)], 9, color=dk)
        stroke(ctx, [(x, ay + 2), (x - 26, ay + 30), (x, ay + 58)], 9, color=dk)


_orig_mark = drawn_anatomy._spider_mark


def _mark(ctx, cfg, ax, ay, arx, ary):
    m = cfg.get("mark")
    if m == "giantmark":
        return _giant_mark(ctx, cfg, ax, ay, arx, ary)
    if m == "falsewidow":   # cream "skull" band on the bulbous brown abdomen
        mk = C["fw_mark"]
        shape(ctx, lambda c: p_smooth(c, [(ax + 110, ay - 40), (ax + 40, ay - 80), (ax - 60, ay - 70), (ax - 100, ay - 30),
                                          (ax - 50, ay - 40), (ax + 30, ay - 50)]), mk, OUT * 0.4, None)
        for k in range(3):
            flat(ctx, lambda c, k=k: p_ellipse(c, ax + 40 - k * 50, ay - 10 + k * 12, 12, 9), mk)
        return
    if m == "redback":   # the red stripe down the back
        shape(ctx, lambda c: p_smooth(c, [(ax + 120, ay - 70), (ax - 110, ay - 90), (ax - 130, ay - 60), (ax + 110, ay - 45)]),
              hexc("#e1261c"), OUT * 0.4, None)
        return
    return _orig_mark(ctx, cfg, ax, ay, arx, ary)


drawn_anatomy._spider_mark = _mark


def _legband(ctx, t, cfg, s=1.0):
    pass


def giant_spider(ctx, t, p):
    walk = 1.0 if p.get("walking") else p.get("walk", 0.25)
    drawn_anatomy._spider(ctx, t, {**p, "walk": walk, "mood": p.get("mood", "angry"), "look": p.get("look", (0.5, 0.1))},
                          GIANT)
    if p.get("wrapped", 0.0) > 0:
        _wrapped(ctx, -40, -190, 330, 190, p["wrapped"])


def house_sp_small(ctx, t, p):
    """Common house spider (Tegenaria domestica) for piles: brown, banded legs; p: dead (legs curled), wrapped."""
    if p.get("dead"):
        col, dk = hexc("#8a6a48"), hexc("#5c4430")
        for k in range(8):
            a = math.pi * (0.1 + 0.8 * k / 7)
            x1, y1 = 60 * math.cos(a) * (1 if k < 4 else -1), -40 - 50 * math.sin(a)
            stroke(ctx, [(0, -40), (x1, y1), (x1 * 0.7, y1 - 40)], 8, smooth=True, color=dk)
        shape(ctx, lambda c: p_ellipse(c, -30, -40, 60, 44), col, OUT * 0.6, (0, 0.2))
        shape(ctx, lambda c: p_ellipse(c, 40, -40, 38, 32), col, OUT * 0.6, (0, 0.2))
        for s in (-1, 1):
            stroke(ctx, [(30 + s * 10, -54), (40 + s * 10, -44)], 4)
            stroke(ctx, [(40 + s * 10, -54), (30 + s * 10, -44)], 4)
        return
    drawn_anatomy._spider(ctx, t, {**p, "walk": p.get("walk", 0.3)},
                          {"color": "#8a6a48", "dark": "#5c4430", "abd": (130, 100), "mark": "stripes", "hair": True,
                           "leg": 1.15, "leg_w": 14})
    if p.get("wrapped", 0.0) > 0:
        _wrapped(ctx, -40, -170, 260, 160, p["wrapped"])


def false_widow(ctx, t, p):
    drawn_anatomy._spider(ctx, t, {**p, "walk": p.get("walk", 0.2), "mood": p.get("mood", "angry")},
                          {"color": "#6e4630", "dark": "#4a2c1c", "abd": (175, 150), "mark": "falsewidow", "leg": 0.95,
                           "leg_w": 15, "fang": "#2a1a12"})
    if p.get("wrapped", 0.0) > 0:
        _wrapped(ctx, -40, -170, 280, 190, p["wrapped"])


def redback(ctx, t, p):
    drawn_anatomy._spider(ctx, t, {**p, "walk": p.get("walk", 0.2), "mood": p.get("mood", "angry")},
                          {"color": "#16161a", "dark": "#0b0b0d", "abd": (165, 150), "mark": "redback", "leg": 1.15,
                           "leg_w": 12})
    if p.get("wrapped", 0.0) > 0:
        _wrapped(ctx, -40, -170, 290, 200, p["wrapped"])


def recluse(ctx, t, p):
    drawn_anatomy._spider(ctx, t, {**p, "walk": p.get("walk", 0.2), "mood": p.get("mood", "calm")},
                          {"color": "#c09160", "dark": "#94693f", "abd": (135, 92), "violin": True, "leg": 1.0,
                           "leg_w": 14, "eye_pairs": True, "knee": 0.62})


def jumper(ctx, t, p):
    drawn_anatomy._spider(ctx, t, {**p, "walk": p.get("walk", 0.2), "mood": p.get("mood", "smug")},
                          {"color": "#2b2b2f", "dark": "#18181b", "abd": (120, 100), "mark": "chevrons", "hair": True,
                           "big_eyes": True, "leg": 0.75, "leg_w": 18, "fang": "#3fb6a8"})


def _spider_top(ctx, t, walk=1.0, hair=True):
    """A big hairy spider seen from above (for shadows and silhouettes), facing right; origin = body centre."""
    col = (0, 0, 0)
    for side in (-1, 1):
        for i in range(4):
            q = t * 10 + i * 1.6 + (side > 0) * 3.1
            sw = 0.22 * math.sin(q) * walk
            base = 70 - i * 34
            ang = math.radians([-30, -70, -110, -150][i]) * -side + sw
            ang = math.radians([35, 75, 105, 145][i]) * side + sw
            k1 = (base + 230 * math.cos(ang), side * 0 + 230 * math.sin(ang))
            ang2 = ang + side * (-0.15 if i < 2 else 0.15)
            k2 = (k1[0] + 300 * math.cos(ang2 - side * 0.4 * (i < 2)), k1[1] + 300 * math.sin(ang2))
            stroke(ctx, [(base, 0), k1, k2], 30 - i * 2, color=col)
            if hair:
                for j in range(5):
                    u = 0.2 + j * 0.16
                    hx, hy = k1[0] + (k2[0] - k1[0]) * u, k1[1] + (k2[1] - k1[1]) * u
                    stroke(ctx, [(hx, hy), (hx + 14 * math.cos(ang2 + 1.2), hy + 14 * math.sin(ang2 + 1.2))], 6, color=col)
    flat(ctx, lambda c: p_ellipse(c, 70, 0, 110, 90), col)
    flat(ctx, lambda c: p_ellipse(c, -150, 0, 175, 120), col)
    for k in range(30):
        a = 2 * math.pi * k / 30
        stroke(ctx, [(-150 + 175 * math.cos(a), 120 * math.sin(a)), (-150 + 200 * math.cos(a), 140 * math.sin(a))], 7,
               color=col)
    for s in (-1, 1):   # palps
        stroke(ctx, [(170, s * 30), (240, s * 60), (270, s * 40)], 22, color=col)


def ds_shadow(ctx, t, p):
    """The giant house spider's long shadow on the floor: a hairy top-down spider silhouette, stretched by a low
    lamp, soft-edged. p: a (darkness), stretch."""
    ctx.save()
    ctx.scale(1.0, p.get("squash", 0.55))
    ctx.push_group()
    _spider_top(ctx, t, 1.0)
    pat = ctx.pop_group()
    for k, (dx, a) in enumerate(((0, 1.0), (14, 0.35), (-14, 0.35))):
        ctx.save()
        ctx.translate(dx, dx * 0.5)
        ctx.set_source_rgba(0.02, 0.02, 0.06, p.get("a", 0.6) * a)
        ctx.mask(pat)
        ctx.restore()
    ctx.restore()


def crane_fly(ctx, t, p):
    """Crane fly: an insect: three body parts, six very long thin legs, two long narrow wings, (halteres)."""
    ph = t * 3
    bob = 6 * math.sin(t * 2.4)
    by = -330 + bob
    col, dk = C["crane"], C["crane_dk"]
    for k, (hx, fx) in enumerate(((40, 420), (10, 120), (-20, -330))):
        for far in (1, 0):
            kx = hx + (fx - hx) * 0.45 + (30 if far else -30)
            foot = (fx + (-50 if far else 50) + 10 * math.sin(ph + k), 0)
            limb(ctx, [(hx, by + 20), (kx, by - 140 - 20 * far), foot], 5, darker(col, 0.8) if far else col, OUT * 0.35,
                 smooth=False)
    for s in (0, 1):   # wings: long, narrow, angled back
        flap = 0.08 * math.sin(t * 30 + s)
        shape(ctx, lambda c, s=s: p_ellipse(c, -90 - s * 20, by - 60 - s * 30, 230, 34, -0.35 - 0.25 * s + flap),
              C["wing"], OUT * 0.4, None, a=0.75)
    shape(ctx, lambda c: p_ellipse(c, -170, by + 10, 170, 30, 0.12), col, OUT * 0.55, (0, 0.2))   # long abdomen
    for k in range(5):
        stroke(ctx, [(-90 - k * 40, by - 14 + k * 5), (-94 - k * 40, by + 34 + k * 5)], 3, color=dk)
    shape(ctx, lambda c: p_ellipse(c, 30, by - 6, 62, 46), col, OUT * 0.6, (0, 0.2))   # thorax
    shape(ctx, lambda c: p_ellipse(c, 112, by - 18, 32, 30), col, OUT * 0.6, (0, 0.2))   # head
    stroke(ctx, [(138, by - 10), (176, by + 6)], 6, color=dk)   # snout
    for s in (-1, 1):
        stroke(ctx, [(120, by - 42), (150 + 20 * s, by - 100), (170 + 30 * s, by - 120)], 3, smooth=True)
    eyes(ctx, 116, by - 24, 12, 10, p.get("look", (0.5, 0)), p.get("mood", "worry"), p.get("blink", 0), OUT * 0.4,
         lid=col)


def woodlouse(ctx, t, p):
    """A woodlouse: grey segmented oval shell, short antennae, 14 short legs (side-top view, facing right)."""
    walk = 1.0 if p.get("walking") else p.get("walk", 0.0)
    for i in range(7):
        x = -120 + i * 40
        q = t * 12 + i
        limb(ctx, [(x, -40), (x + 10 + 8 * math.sin(q) * walk, -6)], 7, C["lice_dk"], OUT * 0.35)
    shape(ctx, lambda c: p_ellipse(c, 0, -70, 170, 64), C["lice"], OUT * 0.8, (0, 0.25), hi=(0.3, 0.2, 0.2))
    for k in range(8):
        x = -130 + k * 34
        stroke(ctx, [(x, -128 + abs(k - 4) * 3), (x - 8, -18 - abs(k - 4) * 2)], 4, color=C["lice_dk"])
    for s in (-1, 1):
        stroke(ctx, [(160, -78), (220, -110 + 20 * s), (250, -100 + 30 * s)], 5, smooth=True)
    eyes(ctx, 140, -84, 11, 9, p.get("look", (0.5, 0)), p.get("mood", "worry"), p.get("blink", 0), OUT * 0.4,
         lid=C["lice"])
    if p.get("wrapped", 0.0) > 0:
        _wrapped(ctx, 0, -70, 200, 90, p["wrapped"])


# ================================================================================================ small world props

def ds_tag(ctx, t, p):
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    s = back_out(min(1.0, on))
    sw = 0.08 * math.sin(t * 2.2)
    ctx.save()
    ctx.rotate(sw)
    stroke(ctx, [(0, -140), (0, 0)], 2.4, color=(1, 1, 1), a=0.9)
    ctx.scale(s, s)
    shape(ctx, lambda c: p_rrect(c, -110, 0, 220, 86, 14), PAL["paper"], OUT * 0.6, (0, 0.2))
    flat(ctx, lambda c: p_ellipse(c, 0, 14, 7, 7), INK)
    text(ctx, p.get("text", "CAROL"), 0, 52, 52, "#c0392b", 0)
    ctx.restore()


def ds_dim(ctx, t, p):
    """A measuring bracket: (0, 0) -> to, grows in with p['grow'], label pill p['text'] at the middle."""
    g = p.get("grow", 1.0)
    if g <= 0.01:
        return
    tx, ty = p.get("to", (300, 0))
    ex, ey = tx * g, ty * g
    col = hexc(p.get("color", "#ffd34d"))
    n = math.hypot(tx, ty) or 1
    nx, ny = -ty / n * 26, tx / n * 26
    for (x, y) in ((0, 0), (ex, ey)):
        stroke(ctx, [(x - nx, y - ny), (x + nx, y + ny)], 12)
        stroke(ctx, [(x - nx, y - ny), (x + nx, y + ny)], 6, color=col)
    stroke(ctx, [(0, 0), (ex, ey)], 12)
    stroke(ctx, [(0, 0), (ex, ey)], 6, color=col)
    if g > 0.6 and p.get("text"):
        a = min(1.0, (g - 0.6) / 0.3)
        lx, ly = ex / 2 + p.get("lx", 0), ey / 2 + p.get("ly", -60)
        text(ctx, p["text"], lx, ly, p.get("px", 64), p.get("color", "#ffd34d"), None, a)


def ds_label(ctx, t, p):
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    s = back_out(min(1.0, on))
    ctx.save()
    ctx.scale(s, s)
    w, h = text(ctx, p["text"], 0, 0, p.get("px", 60), p.get("color", "#ffffff"), None, 0.0)
    shape(ctx, lambda c: p_rrect(c, -w / 2 - 18, -h / 2 - 6, w + 36, h + 12, (h + 12) / 2), hexc(p.get("bg", "#121628")),
          OUT * 0.5, None, a=0.92)
    text(ctx, p["text"], 0, 0, p.get("px", 60), p.get("color", "#ffffff"), 0)
    ctx.restore()


def _shoe(ctx, k=1.0, tie=0.0):
    """A red sneaker in profile, toe right, sole down; origin = the middle of the sole's bottom edge."""
    ctx.save()
    ctx.scale(k, k)
    up = [(-300, -40), (-318, -130), (-290, -230), (-200, -262), (-120, -250), (-60, -300), (10, -292), (40, -236),
          (130, -190), (250, -140), (318, -86), (320, -40)]
    shape(ctx, lambda c: p_smooth(c, up), C["shoe"], OUT, (0.0, 0.2), hi=(0.35, 0.25, 0.2))
    shape(ctx, lambda c: p_smooth(c, [(170, -168), (270, -128), (322, -80), (318, -42), (180, -40), (150, -110)]),
          (0.97, 0.96, 0.93), OUT * 0.7, (0, 0.2))   # toe cap
    stroke(ctx, [(-250, -90), (-80, -160), (60, -110)], 16, smooth=True, color=(0.97, 0.96, 0.93))   # side stripe
    for i in range(4):   # laces
        x = -40 + i * 42
        stroke(ctx, [(x - 14, -262 + i * 18), (x + 26, -240 + i * 18)], 9, color=(0.97, 0.96, 0.93))
    shape(ctx, lambda c: p_rrect(c, -320, -50, 650, 56, 26), C["sole"], OUT, (0.0, 0.25))   # midsole
    shape(ctx, lambda c: p_rrect(c, -312, -8, 632, 26, 12), C["tread"], OUT * 0.8, None)   # tread
    for i in range(14):
        x = -290 + i * 44
        flat(ctx, lambda c, x=x: c.rectangle(x, 6, 20, 14), darker(C["tread"], 0.7))
    if tie > 0:   # the case for the shoe: a little lawyer's tie
        shape(ctx, lambda c: p_poly(c, [(-60, -300), (-30, -300), (-30, -270), (-16, -180), (-45, -150), (-74, -180),
                                        (-60, -270)]), hexc("#2c4f8f"), OUT * 0.6, None, a=tie)
    ctx.restore()


def ds_shoe(ctx, t, p):
    """The viewer's shoe, hovering over the spider from the top of the frame, in SCREEN space next to this actor's
    screen point (its pos is the spider's carapace). Height follows the meter: v 0 = touching distance, 100 = out of
    frame. p: v (meter), lift (0..1 extra climb out), enter (0..1 swing in from above), twitch (0..1), k (size),
    tie (0..1), spot (0..1 spotlight), dx (screen offset px)."""
    mx = ctx.get_matrix()
    k = math.hypot(mx.xx, mx.yx)
    x0, y0 = mx.x0, mx.y0
    v = max(0.0, min(100.0, p.get("v", 30.0)))
    enter = p.get("enter", 1.0)
    if enter <= 0.01:
        return
    ks = p.get("k", 1.0) * min(1.1, max(0.45, k * 1.05))
    gap = (60 + 6.5 * v - 150 * p.get("nudge", 0.0)) * ks + 1600 * p.get("lift", 0.0)
    sole_y = y0 - 330 * k - gap
    sole_y -= (1 - ease(enter)) * 900
    tw = p.get("twitch", 0.0)
    sole_y += tw * 26 * math.sin(t * 34)
    sx = x0 + p.get("dx", 60) + 30 * (1 - ease(enter))
    rot = -0.28 + 0.06 * math.sin(t * 1.3) + 0.5 * (1 - ease(enter)) + tw * 0.05 * math.sin(t * 29)
    ctx.identity_matrix()
    # its shadow on the wall and web: bigger and fainter when it's high, smaller and darker when it's close
    close = 1 - v / 100.0
    sa = (0.18 + 0.32 * close) * ease(enter) * (1 - p.get("lift", 0.0))
    if sa > 0.01:
        ctx.save()
        p_ellipse(ctx, sx - 20, y0 - 40 * k, (420 - 140 * close) * ks, (120 - 30 * close) * ks, -0.15)
        rg = cairo.RadialGradient(sx - 20, y0 - 40 * k, 10, sx - 20, y0 - 40 * k, (420 - 140 * close) * ks)
        rg.add_color_stop_rgba(0, 0.02, 0.02, 0.08, sa)
        rg.add_color_stop_rgba(1, 0.02, 0.02, 0.08, 0)
        ctx.set_source(rg)
        ctx.fill()
        ctx.restore()
    if p.get("spot", 0.0) > 0:
        ctx.save()
        rg = cairo.RadialGradient(sx, sole_y - 150 * ks, 50, sx, sole_y - 150 * ks, 600 * ks)
        rg.add_color_stop_rgba(0, 1, 0.95, 0.7, 0.45 * p["spot"])
        rg.add_color_stop_rgba(1, 1, 0.95, 0.7, 0)
        ctx.set_source(rg)
        ctx.paint()
        ctx.restore()
    ctx.translate(sx, sole_y)
    ctx.rotate(rot)
    _shoe(ctx, 0.95 * ks, p.get("tie", 0.0))


def ds_prop(ctx, t, p):
    kind = p.get("kind")
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    s = back_out(min(1.0, on))
    ctx.save()
    ctx.scale(s, s)
    PROPS[kind](ctx, t, p)
    ctx.restore()


def _plate(ctx, t, p):
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 120, 30), (0.97, 0.97, 0.97), OUT * 0.6, (0, 0.3))
    shape(ctx, lambda c: p_ellipse(c, 0, -4, 80, 18), (0.9, 0.9, 0.92), OUT * 0.3, None)


def _calendar(ctx, t, p):
    """A wall calendar; p: day (float, flips pages as it rises), label."""
    shape(ctx, lambda c: p_rrect(c, -150, -190, 300, 330, 18), (0.98, 0.97, 0.94), OUT, (0, 0.15))
    shape(ctx, lambda c: c.rectangle(-150, -190, 300, 80), C["red"], OUT, None)
    for x in (-80, 80):
        shape(ctx, lambda c, x=x: p_ellipse(c, x, -196, 14, 22), PAL["steel"], OUT * 0.6, None)
    d = p.get("day", 1.0)
    fl = d - math.floor(d)
    lbl = p.get("label")
    if lbl:
        text(ctx, lbl, 0, 10, 92, "#222222", 0)
    else:
        text(ctx, p.get("unit", "DAY"), 0, -150, 44, "#ffffff", 0)
        text(ctx, str(int(math.floor(d))), 0, 30, 150, "#222222", 0)
    if 0 < fl < 0.999 and not lbl:   # a page flipping up
        h = 330 * (1 - fl)
        shape(ctx, lambda c: c.rectangle(-150, -110, 300, max(1, h * 0.75)), (0.93, 0.92, 0.88), OUT * 0.6, None)


def _tweezers(ctx, t, p):
    stroke(ctx, [(0, 0), (160, -40)], 14)
    stroke(ctx, [(0, 0), (160, -40)], 8, color=PAL["steel"])
    stroke(ctx, [(0, 0), (160, -10)], 14)
    stroke(ctx, [(0, 0), (160, -10)], 8, color=PAL["steel"])


def _tray(ctx, t, p):
    shape(ctx, lambda c: p_rrect(c, -200, -40, 400, 60, 14), PAL["steel"], OUT, (0, 0.2))
    for k in range(int(p.get("n", 0))):
        x = -150 + (k % 6) * 60
        y = -50 - (k // 6) * 30
        house_sp_small(ctx, t, {"dead": True}) if False else flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 18, 12),
                                                                    hexc("#6a4e34"), OUT * 0.3)


def _vacuum(ctx, t, p):
    """An upright vacuum, ~600 tall, floor at y = 0."""
    shape(ctx, lambda c: p_rrect(c, -150, -70, 300, 70, 20), hexc("#5b6b7a"), OUT, (0, 0.2))
    shape(ctx, lambda c: p_rrect(c, -90, -420, 180, 360, 50), hexc("#e5383b"), OUT, (0.1, 0.1), hi=(0.3, 0.2, 0.2))
    shape(ctx, lambda c: p_rrect(c, -60, -380, 120, 150, 30), hexc("#cfd6dc"), OUT * 0.7, None, a=0.9)
    stroke(ctx, [(0, -420), (0, -620)], 22)
    stroke(ctx, [(0, -420), (0, -620)], 12, color=hexc("#5b6b7a"))
    shape(ctx, lambda c: p_rrect(c, -50, -650, 100, 40, 18), hexc("#2c3440"), OUT * 0.7, None)
    for s in (-1, 1):
        shape(ctx, lambda c, s=s: p_ellipse(c, s * 110, -10, 26, 26), INK, OUT * 0.4, None)


def _broom(ctx, t, p):
    stroke(ctx, [(0, -700), (0, -170)], 22)
    stroke(ctx, [(0, -700), (0, -170)], 13, color=PAL["wood"])
    shape(ctx, lambda c: p_poly(c, [(-50, -180), (50, -180), (130, 0), (-130, 0)]), hexc("#e2b84a"), OUT, (0, 0.2))
    for k in range(9):
        stroke(ctx, [(-40 + k * 10, -150), (-120 + k * 30, -4)], 3, color=hexc("#b88a2a"))


def _jar(ctx, t, p):
    shape(ctx, lambda c: p_rrect(c, -130, -300, 260, 300, 40), (0.85, 0.95, 1.0), OUT, None, a=0.45)
    ctx.rectangle(-130, -300, 260, 300)
    shape(ctx, lambda c: p_rrect(c, -140, -330, 280, 50, 16), PAL["steel"], OUT, (0, 0.2))
    stroke(ctx, [(-90, -250), (-90, -60)], 10, color=(1, 1, 1), a=0.6)


def _paper(ctx, t, p):
    shape(ctx, lambda c: c.rectangle(-170, -10, 340, 20), PAL["paper"], OUT * 0.7, None)


def _spray(ctx, t, p):
    shape(ctx, lambda c: p_rrect(c, -80, -360, 160, 360, 30), hexc("#7aa83c"), OUT, (0.1, 0.1), hi=(0.3, 0.2, 0.2))
    shape(ctx, lambda c: p_rrect(c, -40, -420, 80, 60, 12), PAL["steel"], OUT, None)
    shape(ctx, lambda c: p_rrect(c, -60, -260, 120, 120, 12), (0.97, 0.97, 0.92), OUT * 0.6, None)
    flat(ctx, lambda c: p_ellipse(c, 0, -200, 34, 24), INK)   # a bug silhouette on the label
    x = p.get("x", 1.0)
    if x > 0:
        for s in (-1, 1):
            stroke(ctx, [(-200, -380 * (1 if s > 0 else 0) - 20 * (s < 0)), (200, -20 if s > 0 else -400)], 46 * x)
            stroke(ctx, [(-200, -380 * (1 if s > 0 else 0) - 20 * (s < 0)), (200, -20 if s > 0 else -400)], 30 * x,
                   color=C["red"])


def _caulk(ctx, t, p):
    shape(ctx, lambda c: p_rrect(c, -260, -60, 360, 80, 30), hexc("#e8e2d0"), OUT, (0, 0.2))
    shape(ctx, lambda c: p_poly(c, [(100, -40), (230, -26), (230, -14), (100, -10)]), hexc("#e8e2d0"), OUT * 0.8, None)
    shape(ctx, lambda c: p_rrect(c, -330, -80, 90, 120, 14), hexc("#e5383b"), OUT, (0, 0.2))
    stroke(ctx, [(-300, 40), (-340, 190)], 26)
    stroke(ctx, [(-300, 40), (-340, 190)], 16, color=hexc("#e5383b"))


def _growth(ctx, t, p):
    shape(ctx, lambda c: p_rrect(c, -90, -700, 180, 700, 12), (0.98, 0.95, 0.85), OUT, (0, 0.1))
    for k in range(14):
        y = -40 - k * 48
        stroke(ctx, [(-90, y), (-90 + (60 if k % 2 == 0 else 30), y)], 5)
    g = p.get("g", 1.0)
    stroke(ctx, [(-120, -60 - 560 * g), (120, -60 - 560 * g)], 10, color=C["red"])


def _radiator(ctx, t, p):
    for k in range(8):
        x = -280 + k * 72
        shape(ctx, lambda c, x=x: p_rrect(c, x, -420, 60, 400, 26), hexc("#e9e6df"), OUT * 0.8, (0.1, 0))
    shape(ctx, lambda c: c.rectangle(-290, -60, 580, 30), hexc("#d2cec4"), OUT * 0.8, None)
    for k in range(3):   # heat shimmer
        x = -150 + k * 150
        stroke(ctx, [(x + 20 * math.sin(t * 3 + j * 0.8 + k), -460 - j * 40) for j in range(6)], 6, smooth=True,
               color=hexc("#ffb36b"), a=0.7)


def _door(ctx, t, p):
    """An open front door onto a blizzard; p: open (0..1)."""
    o = p.get("open", 1.0)
    shape(ctx, lambda c: c.rectangle(-230, -760, 460, 760), hexc("#dfe9f2"), OUT, None)
    rng = random.Random(9)
    for k in range(60):
        x = -220 + rng.random() * 440
        y = -750 + ((rng.random() * 760 + t * 420 * (0.6 + rng.random())) % 750)
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x + 20 * math.sin(t * 2 + k), y, 7, 7), (1, 1, 1))
    w = 460 * (1 - 0.82 * o)
    shape(ctx, lambda c: c.rectangle(-230, -760, w, 760), hexc("#8a5a30"), OUT, (0.1, 0))
    shape(ctx, lambda c: p_ellipse(c, -230 + w - 40, -380, 14, 14), PAL["claw"], OUT * 0.5, None)
    shape(ctx, lambda c: c.rectangle(-260, -790, 520, 34), hexc("#6b4626"), OUT, None)


def _contract(ctx, t, p):
    shape(ctx, lambda c: p_rrect(c, -130, -340, 260, 340, 10), PAL["paper"], OUT, (0, 0.15))
    for k in range(6):
        stroke(ctx, [(-90, -290 + k * 40), (90 - (k == 5) * 70, -290 + k * 40)], 6, color=(0.6, 0.6, 0.6))
    stroke(ctx, [(-90, -50), (-10, -70), (60, -40)], 6, smooth=True, color=hexc("#2c4f8f"))


def _bill(ctx, t, p):
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 120, 120), (0.95, 0.95, 0.95), OUT, (0, 0.1))
    a = t * 9
    stroke(ctx, [(0, 0), (90 * math.cos(a), 90 * math.sin(a))], 10, color=C["red"])
    text(ctx, "$", 0, -60, 54, "#2b7a3c", 0)


def _bottle(ctx, t, p):
    shape(ctx, lambda c: p_rrect(c, -60, -180, 120, 180, 26), hexc("#9fd8b0"), OUT, (0.1, 0.1), hi=(0.3, 0.2, 0.2))
    shape(ctx, lambda c: c.rectangle(-26, -240, 52, 60), hexc("#9fd8b0"), OUT * 0.8, None)
    shape(ctx, lambda c: c.rectangle(-32, -270, 64, 32), hexc("#6b4626"), OUT * 0.8, None)
    shape(ctx, lambda c: c.rectangle(-60, -130, 120, 70), PAL["paper"], OUT * 0.5, None)
    if p.get("label"):
        text(ctx, p["label"], 0, -96, 34, "#222222", 0)


def _cricket(ctx, t, p):
    shape(ctx, lambda c: p_ellipse(c, 0, -60, 120, 46), hexc("#5a4630"), OUT, (0, 0.2))
    shape(ctx, lambda c: p_ellipse(c, 110, -70, 40, 36), hexc("#5a4630"), OUT, (0, 0.2))
    limb(ctx, [(-40, -50), (-150, -170), (-190, 0)], 14, hexc("#4a3a26"), OUT * 0.5, smooth=False)
    for x in (40, 80):
        limb(ctx, [(x, -30), (x + 20, 0)], 8, hexc("#4a3a26"), OUT * 0.4)
    stroke(ctx, [(140, -90), (280, -200)], 4)
    eyes(ctx, 118, -80, 10, 8, (0.5, 0), p.get("mood", "shock"), 0, OUT * 0.4)


def _box(ctx, t, p):
    shape(ctx, lambda c: p_rrect(c, -160, -200, 320, 200, 10), PAL["box"], OUT, (0.1, 0.1))
    stroke(ctx, [(-160, -150), (160, -150)], 6, color=PAL["box_dk"])


def _tv(ctx, t, p):
    shape(ctx, lambda c: p_rrect(c, -150, -120, 230, 140, 20), INK, OUT, None)
    shape(ctx, lambda c: p_ellipse(c, -40, -50, 50, 50), hexc("#3a3a40"), OUT * 0.6, None)
    shape(ctx, lambda c: p_ellipse(c, -40, -50, 26, 26), hexc("#7aa0d0"), OUT * 0.4, None)
    flat(ctx, lambda c: p_ellipse(c, 60, -90, 10, 10), C["red"], a=0.5 + 0.5 * (math.sin(t * 6) > 0))
    stroke(ctx, [(-40, 20), (-90, 140)], 10)
    stroke(ctx, [(-40, 20), (10, 140)], 10)


def _suitcase(ctx, t, p):
    shape(ctx, lambda c: p_rrect(c, -110, -150, 220, 150, 18), hexc("#b0683a"), OUT, (0.1, 0.1))
    shape(ctx, lambda c: p_rrect(c, -40, -190, 80, 50, 14), None or hexc("#6b4626"), OUT * 0.7, None)
    stroke(ctx, [(-110, -80), (110, -80)], 6, color=hexc("#6b4626"))


def _skull(ctx, t, p):
    shape(ctx, lambda c: p_ellipse(c, 0, -40, 70, 64), (0.97, 0.97, 0.95), OUT * 0.8, (0, 0.1))
    shape(ctx, lambda c: p_rrect(c, -40, 0, 80, 40, 10), (0.97, 0.97, 0.95), OUT * 0.8, None)
    for s in (-1, 1):
        flat(ctx, lambda c, s=s: p_ellipse(c, s * 26, -44, 18, 20), INK)
    for s in (-1, 1):
        stroke(ctx, [(-90, -120 * (s > 0) + 80 * (s < 0)), (90, 80 * (s > 0) - 120 * (s < 0))], 22)
        stroke(ctx, [(-90, -120 * (s > 0) + 80 * (s < 0)), (90, 80 * (s > 0) - 120 * (s < 0))], 12,
               color=(0.97, 0.97, 0.95))


def _lamp_blaze(ctx, t, p):
    shape(ctx, lambda c: c.rectangle(-12, -260, 24, 260), PAL["steel_dk"], OUT * 0.7, None)
    shape(ctx, lambda c: p_poly(c, [(-110, -260), (110, -260), (60, -380), (-60, -380)]), C["lamp"], OUT, (0.1, 0))
    rg = cairo.RadialGradient(0, -260, 20, 0, -260, 700)
    rg.add_color_stop_rgba(0, 1, 0.93, 0.6, 0.55 + 0.05 * math.sin(t * 5))
    rg.add_color_stop_rgba(1, 1, 0.93, 0.6, 0)
    ctx.save()
    ctx.set_source(rg)
    ctx.arc(0, -260, 700, 0, 2 * math.pi)
    ctx.fill()
    ctx.restore()


def _lump(ctx, t, p):
    """A roommate-shaped lump under a blanket (no face, no likeness), breathing."""
    b = 1 + 0.03 * math.sin(t * 2)
    shape(ctx, lambda c: p_blob(c, 0, -110 * b, 330, 120 * b, 0.08, 5), hexc("#c2504a"), OUT, (0.05, 0.2))


def _ruler(ctx, t, p):
    shape(ctx, lambda c: c.rectangle(-400, -50, 800, 100), hexc("#f2d36b"), OUT, (0, 0.2))
    for k in range(41):
        x = -380 + k * 19
        stroke(ctx, [(x, -50), (x, -50 + (40 if k % 5 == 0 else 20))], 4)


PROPS = {"plate": _plate, "calendar": _calendar, "tweezers": _tweezers, "tray": _tray, "vacuum": _vacuum,
         "broom": _broom, "jar": _jar, "paper": _paper, "spray": _spray, "caulk": _caulk, "growth": _growth,
         "radiator": _radiator, "door": _door, "contract": _contract, "bill": _bill, "bottle": _bottle,
         "cricket": _cricket, "box": _box, "tv": _tv, "suitcase": _suitcase, "skull": _skull, "lamp_blaze": _lamp_blaze,
         "lump": _lump, "ruler": _ruler}


# ================================================================================================ charts and boards

def _remain_icon(ctx, kind, x, y, r, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    if kind == "hs":   # a dead house spider: brown body, curled legs
        for k in range(4):
            a = 0.5 + k * 0.7
            for s in (-1, 1):
                stroke(ctx, [(0, 0), (s * r * 1.1 * math.cos(a * 0.6), -r * 0.9 * math.sin(a)),
                             (s * r * 0.7, -r * 1.4 + k * 4)], max(2.0, r * 0.14), smooth=True, color=hexc("#4e3826"))
        shape(ctx, lambda c: p_ellipse(c, -r * 0.35, 0, r * 0.7, r * 0.5), hexc("#8a6a48"), OUT * 0.3, None)
        shape(ctx, lambda c: p_ellipse(c, r * 0.45, -r * 0.05, r * 0.42, r * 0.36), hexc("#8a6a48"), OUT * 0.3, None)
    elif kind == "sp":   # another cellar spider: pale, tiny body, very long legs
        for k in range(4):
            for s in (-1, 1):
                stroke(ctx, [(0, 0), (s * r * 0.8, -r * 1.0 + k * r * 0.3), (s * r * 1.7, -r * 0.3 + k * r * 0.45)],
                       max(3.0, r * 0.14))
                stroke(ctx, [(0, 0), (s * r * 0.8, -r * 1.0 + k * r * 0.3), (s * r * 1.7, -r * 0.3 + k * r * 0.45)],
                       max(1.5, r * 0.07), color=C["cell_leg"])
        shape(ctx, lambda c: p_ellipse(c, -r * 0.25, r * 0.15, r * 0.45, r * 0.2, 0.5), C["cell"], OUT * 0.3, None)
        shape(ctx, lambda c: p_ellipse(c, r * 0.1, 0, r * 0.22, r * 0.2), C["cell"], OUT * 0.3, None)
    elif kind == "fly":
        shape(ctx, lambda c: p_ellipse(c, 0, 0, r * 0.7, r * 0.45), hexc("#4a4f57"), OUT * 0.3, None)
        flat(ctx, lambda c: p_ellipse(c, -r * 0.2, -r * 0.5, r * 0.6, r * 0.25, -0.5), C["wing"], a=0.8)
    else:   # woodlouse / other bits
        shape(ctx, lambda c: p_ellipse(c, 0, 0, r * 0.75, r * 0.42), C["lice"], OUT * 0.3, None)
    ctx.restore()


def ds_board(ctx, t, p):
    """The shed's leftovers: a pin board of 102 remains. n (0..102) pinned so far (rolls up), sort (0..1) moves the 63
    house spiders into a big pile at the left, sort2 (0..1) moves 6 other spiders into a second pile; count shows the
    tally on a chalk strip above. Origin = board centre."""
    Wb, Hb = 1500, 820
    shape(ctx, lambda c: p_rrect(c, -Wb / 2, -Hb / 2, Wb, Hb, 26), hexc("#b98a55"), OUT, (0, 0.06))
    flat(ctx, lambda c: p_rrect(c, -Wb / 2 + 30, -Hb / 2 + 30, Wb - 60, Hb - 60, 18), hexc("#d4ac77"))
    n = p.get("n", 102)
    srt, srt2 = ease(p.get("sort", 0.0)), ease(p.get("sort2", 0.0))
    rng = random.Random(11)
    kinds = ["hs"] * 63 + ["sp"] * 6 + ["fly"] * 20 + ["wl"] * 13
    rng.shuffle(kinds)
    grid = [(-Wb / 2 + 110 + (k % 17) * 76, -Hb / 2 + 150 + (k // 17) * 92) for k in range(102)]
    pile1 = [(-560 + (k % 9) * 50 - (k // 9) * 4, 300 - (k // 9) * 38) for k in range(63)]
    pile2 = [(260 + (k % 3) * 80, 290 - (k // 3) * 60) for k in range(6)]
    i1 = i2 = 0
    for k, kind in enumerate(kinds):
        if k >= n:
            break
        gx, gy = grid[k]
        x, y = gx, gy
        if kind == "hs" and srt > 0:
            tx, ty = pile1[i1]
            uu = max(0.0, min(1.0, srt * 1.6 - i1 / 63 * 0.6))
            x, y = gx + (tx - gx) * ease(uu), gy + (ty - gy) * ease(uu) - 120 * math.sin(math.pi * uu)
            i1 += 1
        elif kind == "sp" and srt2 > 0:
            tx, ty = pile2[i2]
            uu = ease(srt2)
            x, y = gx + (tx - gx) * uu, gy + (ty - gy) * uu - 120 * math.sin(math.pi * uu)
            i2 += 1
        else:
            if kind == "hs":
                i1 += 1
            elif kind == "sp":
                i2 += 1
        pop = min(1.0, (n - k) * 1.5)
        _remain_icon(ctx, kind, x, y, 30 * back_out(pop), (k % 5 - 2) * 0.2)
    if p.get("count", True) and n > 0:
        text(ctx, str(int(round(n))), Wb / 2 - 150, -Hb / 2 + 70, 96, "#ffffff")
    if srt > 0.5:
        a = min(1.0, (srt - 0.5) * 3)
        text(ctx, "HOUSE SPIDERS", -380, 365, 56, "#ffd34d", None, a)
    if srt2 > 0.5:
        a = min(1.0, (srt2 - 0.5) * 3)
        text(ctx, p.get("label2", "OTHER SPIDERS"), 340, 365, 56, "#ffffff", None, a)


def ds_pie(ctx, t, p):
    if p.get("slices"):
        return _pie_slices(ctx, t, p)
    fr = p.get("frac", 69 / 102.0) * ease(p.get("sweep", 1.0))
    R = 330
    shape(ctx, lambda c: p_ellipse(c, 0, 0, R, R), hexc("#8a94a6"), OUT, None)
    if fr > 0:
        ctx.save()
        ctx.move_to(0, 0)
        ctx.arc(0, 0, R, -math.pi / 2, -math.pi / 2 + 2 * math.pi * fr)
        ctx.close_path()
        src(ctx, hexc("#ff9f1c"))
        ctx.fill_preserve()
        ink(ctx, OUT)
        ctx.stroke()
        ctx.restore()
    if p.get("label") and fr > 0.3:
        a = min(1.0, (fr - 0.3) * 4)
        mid = -math.pi / 2 + math.pi * fr
        text(ctx, p["label"], 0.55 * R * math.cos(mid), 0.55 * R * math.sin(mid), 84, "#ffffff", None, a)
    if p.get("sub"):
        text(ctx, p["sub"], 0, R + 80, 64, "#ffd34d", None, min(1.0, fr * 2))


def _pie_slices(ctx, t, p):
    """A full circle chart: slices [[value, colour, label], ...]; p["w"] = per-wedge progress (0..1 each, drawn one at a
    time with the narration), else one sweep; legend at the right (p: R, lx, px, gap)."""
    sl = p["slices"]
    tot = float(sum(s[0] for s in sl))
    R = p.get("R", 330)
    w = [p.get(f"w{k}", 0.0) for k in range(len(sl))] if "w0" in p else [ease(p.get("sweep", 1.0))] * len(sl)
    a0 = -math.pi / 2
    for k, (v, col, lab) in enumerate(sl):
        a1 = a0 + 2 * math.pi * v / tot
        u = ease(max(0.0, min(1.0, w[k])))
        if u > 0:
            e = a0 + (a1 - a0) * u
            ctx.save()
            ctx.move_to(0, 0)
            ctx.arc(0, 0, R * (0.92 + 0.08 * u), a0, e)
            ctx.close_path()
            src(ctx, hexc(col))
            ctx.fill_preserve()
            ink(ctx, OUT)
            ctx.stroke()
            ctx.restore()
        a0 = a1
    ctx.save()
    ctx.arc(0, 0, R, 0, 2 * math.pi)
    ink(ctx, OUT, 0.5)
    ctx.stroke()
    ctx.restore()
    lx, px, gp = p.get("lx", 460), p.get("px", 70), p.get("gap", 150)
    for k, (v, col, lab) in enumerate(sl):
        a = max(0.0, min(1.0, w[k] * 3))
        if a <= 0:
            continue
        y = (k - (len(sl) - 1) / 2) * gp
        shape(ctx, lambda c, y=y: p_rrect(c, lx, y - 45, 90, 90, 16), hexc(col), OUT * 0.7, None, a=a)
        ctx.save()
        im_w, im_h = text(ctx, lab, 0, 0, px, "#ffffff", None, 0.0)
        ctx.restore()
        text(ctx, lab, lx + 120 + im_w / 2, y, px, "#ffffff", None, a)


def ds_lineup(ctx, t, p):
    """A police-lineup wall: height lines, three numbered spots; lit [a, b, c] lights each spot (0..1)."""
    Wl, Hl = 1800, 1000
    flat(ctx, lambda c: c.rectangle(-Wl / 2, -Hl, Wl, Hl), hexc("#3a4150"))
    for k in range(9):
        y = -k * 110
        stroke(ctx, [(-Wl / 2, y), (Wl / 2, y)], 4 if k % 2 else 7, color=hexc("#c9ced8"), a=0.6)
        if k % 2 == 0 and k:
            text(ctx, f"{k // 2}", -Wl / 2 + 40, y - 30, 38, "#c9ced8", 0, 0.7)
    lit = p.get("lit", [0, 0, 0])
    for i in range(3):
        x = (i - 1) * 560
        a = lit[i] if i < len(lit) else 0
        ctx.save()
        rg = cairo.RadialGradient(x, -500, 40, x, -500, 360)
        rg.add_color_stop_rgba(0, 1, 0.96, 0.8, 0.5 * a)
        rg.add_color_stop_rgba(1, 1, 0.96, 0.8, 0)
        ctx.set_source(rg)
        ctx.rectangle(x - 300, -Hl, 600, Hl)
        ctx.fill()
        ctx.restore()
    flat(ctx, lambda c: c.rectangle(-Wl / 2, 0, Wl, 300), hexc("#2a2f3a"))


_MAPS = {   # crude outlines (no flags, no borders): a recognisable blob per place, in a 600x600 box
    "KANSAS": [(-260, -150), (260, -150), (270, 150), (-260, 150)],
    "BRITAIN": [(-40, -270), (60, -240), (40, -150), (110, -60), (150, 60), (210, 160), (150, 230), (-60, 250),
                (-130, 200), (-40, 120), (-110, 40), (-60, -60), (-120, -150)],
    "CALIFORNIA": [(-150, -270), (20, -270), (20, -80), (230, 130), (210, 250), (60, 250), (-40, 140), (-150, -20),
                   (-200, -150)],
    "FINLAND": [(-20, -280), (70, -250), (60, -120), (140, -20), (130, 140), (40, 250), (-120, 230), (-150, 100),
                (-60, -40), (-90, -160)],
    "AUSTRALIA": [(-280, -40), (-160, -160), (-20, -130), (40, -220), (120, -100), (240, -40), (280, 90), (180, 210),
                  (40, 190), (-60, 120), (-220, 150), (-290, 70)],
}


def ds_map(ctx, t, p):
    place = p.get("place", "KANSAS")
    shape(ctx, lambda c: p_rrect(c, -380, -380, 760, 760, 30), C["sea"], OUT, None)
    shape(ctx, lambda c: p_poly(c, _MAPS[place]), C["map"], OUT, (0.05, 0.1))
    pin = p.get("pin", 1.0)
    if pin > 0:
        px, py = p.get("px", 0), p.get("py", 0)
        dy = -260 * (1 - back_out(min(1.0, pin)))
        shape(ctx, lambda c: (c.move_to(px, py + dy), c.curve_to(px - 60, py - 70 + dy, px - 50, py - 130 + dy, px, py - 130 + dy),
                              c.curve_to(px + 50, py - 130 + dy, px + 60, py - 70 + dy, px, py + dy)), C["red"], OUT, (0.1, 0.1))
        flat(ctx, lambda c: p_ellipse(c, px, py - 92 + dy, 20, 20), (1, 1, 1))
    text(ctx, place, 0, 330, 64, "#ffffff")


def ds_arena(ctx, t, p):
    """A clear plastic lab box seen from the front; p: grey (0..1: this round was lost)."""
    shape(ctx, lambda c: p_rrect(c, -260, -340, 520, 340, 20), (0.85, 0.95, 1.0), OUT, None, a=0.35)
    stroke(ctx, [(-220, -300), (-220, -60)], 8, color=(1, 1, 1), a=0.5)
    g = p.get("grey", 0.0)
    if g > 0:
        flat(ctx, lambda c: p_rrect(c, -260, -340, 520, 340, 20), hexc("#2a2a30"), a=0.55 * g)


def ds_houses(ctx, t, p):
    n = int(p.get("n", 10))
    lit = p.get("lit", 0.0)
    cols = int(p.get("cols", 10))
    for k in range(n):
        x = (k % cols - (cols - 1) / 2) * 150
        y = (k // cols) * 150
        on = (k * 7 % n) < lit * n
        body = hexc("#f2c75c") if on else hexc("#8a94a6")
        shape(ctx, lambda c, x=x, y=y: c.rectangle(x - 50, y - 70, 100, 70), body, OUT * 0.5, None)
        shape(ctx, lambda c, x=x, y=y: p_poly(c, [(x - 62, y - 66), (x, y - 120), (x + 62, y - 66)]), hexc("#b8352c"),
              OUT * 0.5, None)


def ds_lineup_mask(ctx, t, p):
    """Front layer of the lineup: each suspect stays in shadow until lit (lit [0..1 x3]); spacing 560."""
    lit = p.get("lit", [0, 0, 0])
    for i in range(3):
        a = 0.86 * (1 - (lit[i] if i < len(lit) else 0))
        if a > 0.01:
            flat(ctx, lambda c, i=i: c.rectangle((i - 1) * 560 - 280, -1000, 560, 1000), hexc("#0c0e14"), a=a)
    for i in range(3):   # the number plates, in front of everything, low and to the left of each suspect
        x = (i - 1) * 560 - 215
        shape(ctx, lambda c, x=x: p_rrect(c, x - 55, -130, 110, 90, 12), hexc("#f2f2ea"), OUT * 0.6, None)
        text(ctx, str(i + 1), x, -84, 70, "#222222", 0)


def ds_chip_src(ctx, t, p):
    """A source chip: a small labelled pill (world space)."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    ds_label(ctx, t, {"text": p["text"], "px": p.get("px", 48), "color": "#ffffff", "bg": "#1f5f8b", "on": on})


def ds_bubble(ctx, t, p):
    """A thought bubble holding text or a skull; p: on, text, kind ("skull"), pop (0..1 it pops)."""
    on = p.get("on", 1.0)
    pop = p.get("pop", 0.0)
    if on <= 0.01 or pop >= 1:
        return
    s = back_out(min(1.0, on)) * (1 + 0.6 * pop)
    a = 1 - pop
    ctx.save()
    ctx.scale(s, s)
    for (x, y, r) in ((0, 0, 16), (30, -40, 26)):
        shape(ctx, lambda c, x=x, y=y, r=r: p_ellipse(c, x, y, r, r), (1, 1, 1), OUT * 0.6, None, a=a)
    shape(ctx, lambda c: p_blob(c, 120, -190, 200, 120, 0.06, 3), (1, 1, 1), OUT * 0.7, None, a=a)
    if p.get("kind") == "skull":
        ctx.save()
        ctx.translate(120, -170)
        ctx.scale(0.8, 0.8)
        _skull(ctx, t, {})
        ctx.restore()
    if p.get("text"):
        text(ctx, p["text"], 120, -190, p.get("px", 56), "#e5383b", 0, a)
    ctx.restore()


# ================================================================================================ scenes

def _grade_night(ctx):
    ctx.save()
    ctx.identity_matrix()
    ctx.rectangle(0, 0, ctx.get_target().get_width(), ctx.get_target().get_height())
    src(ctx, (0.05, 0.08, 0.22), 0.22)
    ctx.fill()
    ctx.restore()


def ds_corner(ctx, t, layer, p):
    """The bedroom ceiling corner at night, looking up into it: corner point (700, 150), ceiling above, the left wall
    in the bedroom's striped wallpaper, the right wall in shade, crown moulding, a warm lamp glow from below left."""
    layer(1.0)
    cx, cy = 700, 150
    flat(ctx, lambda c: c.rectangle(-3000, -2000, 7000, 6000), C["paperL"])
    for x in range(-3000, cx, 120):
        flat(ctx, lambda c, x=x: c.rectangle(x, -2000, 46, 6000), C["paperL2"])
    flat(ctx, lambda c: c.rectangle(cx, -2000, 4000, 6000), C["paperR"])
    for x in range(cx + 60, 4000, 120):
        flat(ctx, lambda c, x=x: c.rectangle(x, -2000, 40, 6000), C["paperR2"])
    ceil = [(-3000, -2400), (4000, -2400), (4000, -500), (cx, cy), (-3000, -620)]
    flat(ctx, lambda c: p_poly(c, ceil), C["ceil"])
    for k in range(1, 6):   # faint ceiling texture lines toward the corner
        stroke(ctx, [(cx, cy), (cx - 3000, cy - 600 - k * 300)], 3, color=C["ceil_dk"], a=0.4)
        stroke(ctx, [(cx, cy), (cx + 3000, cy - 500 - k * 300)], 3, color=C["ceil_dk"], a=0.4)
    # crown moulding along both ceiling edges
    for sgn, ex, ey in ((-1, -3000, -620), (1, 4000, -500)):
        pts = [(cx, cy), (ex, ey), (ex, ey + 70), (cx, cy + 62)]
        shape(ctx, lambda c, pts=pts: p_poly(c, pts), C["mould"], BG_OUT, None)
        stroke(ctx, [(cx, cy + 30), (ex, ey + 36)], 4, color=C["mould_dk"])
    stroke(ctx, [(cx, cy + 62), (cx, 4000)], BG_OUT * 0.8, color=darker(C["paperR"], 0.7))   # the wall seam
    # warm lamp glow from below left + a cool moon wash from the right
    ctx.save()
    rg = cairo.RadialGradient(-200, 1500, 50, -200, 1500, 1900)
    rg.add_color_stop_rgba(0, 1.0, 0.85, 0.5, 0.35)
    rg.add_color_stop_rgba(1, 1.0, 0.85, 0.5, 0.0)
    ctx.set_source(rg)
    ctx.rectangle(-3000, -2400, 7000, 6400)
    ctx.fill()
    ctx.restore()
    _grade_night(ctx)


def ds_wall(ctx, t, layer, p):
    """A plain bedroom wall at night (the dramatised hunt): wallpaper, a low lamp throwing long light upward."""
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), C["paperL"])
    for x in range(-3000, 5000, 120):
        flat(ctx, lambda c, x=x: c.rectangle(x, -3000, 46, 8000), C["paperL2"])
    ctx.save()
    rg = cairo.RadialGradient(500, 1700, 50, 500, 1700, 1700)
    rg.add_color_stop_rgba(0, 1.0, 0.85, 0.5, 0.42)
    rg.add_color_stop_rgba(1, 1.0, 0.85, 0.5, 0.0)
    ctx.set_source(rg)
    ctx.paint()
    ctx.restore()
    ctx.save()
    ctx.identity_matrix()
    ctx.rectangle(0, 0, ctx.get_target().get_width(), ctx.get_target().get_height())
    src(ctx, (0.03, 0.04, 0.14), 0.36 if p.get("dark") else 0.24)
    ctx.fill()
    ctx.restore()


def ds_floor(ctx, t, layer, p):
    """Floorboards at night from a low camera: the wall and skirting board at the top (y < 300), boards below with
    perspective joints converging upward, a lamp pool of warm light."""
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, -2000, 8000, 2300), C["paperL"])
    for x in range(-3000, 5000, 120):
        flat(ctx, lambda c, x=x: c.rectangle(x, -2000, 46, 2300), C["paperL2"])
    shape(ctx, lambda c: c.rectangle(-3000, 200, 8000, 100), hexc("#e6e1d3"), BG_OUT, None)
    flat(ctx, lambda c: c.rectangle(-3000, 300, 8000, 3000), C["wood1"])
    vx = 700
    for k in range(-30, 31):   # board joints in perspective
        x0 = vx + k * 180
        stroke(ctx, [(vx + k * 60, 300), (x0 + k * 260, 2400)], 5, color=C["wood2"])
    for k, y in enumerate((380, 480, 620, 820, 1100, 1500)):
        off = (k * 137) % 400
        for j in range(-8, 10):
            x = vx - 1600 + j * (300 + k * 120) + off
            stroke(ctx, [(x, y), (x + 20, y + 40 + k * 30)], 4, color=C["wood2"], a=0.6)
    ctx.save()
    rg = cairo.RadialGradient(1300, 900, 50, 1300, 900, 1300)
    rg.add_color_stop_rgba(0, 1.0, 0.86, 0.52, 0.4)
    rg.add_color_stop_rgba(1, 1.0, 0.86, 0.52, 0.0)
    ctx.set_source(rg)
    ctx.rectangle(-3000, -2000, 8000, 6000)
    ctx.fill()
    ctx.restore()
    _grade_night(ctx)


def ds_lab(ctx, t, layer, p):
    """A simple lab: tiled pale wall, a bench top at y = 900 (things stand on it), a shelf of flasks."""
    layer(0.9)
    flat(ctx, lambda c: c.rectangle(-3000, -2000, 8000, 5000), C["lab_wall"])
    for y in range(-2000, 900, 110):
        stroke(ctx, [(-3000, y), (5000, y)], 3, color=C["lab_wall2"])
    for x in range(-3000, 5000, 160):
        stroke(ctx, [(x, -2000), (x, 900)], 3, color=C["lab_wall2"])
    shape(ctx, lambda c: c.rectangle(-3000, 120, 8000, 30), hexc("#b9c3ca"), BG_OUT, None)
    for k, x in enumerate(range(-900, 2400, 260)):
        col = [hexc("#9fd8b0"), hexc("#f2c75c"), hexc("#7aa0d0"), hexc("#e59a9a")][k % 4]
        shape(ctx, lambda c, x=x: p_poly(c, [(x - 20, 0), (x + 20, 0), (x + 20, 50), (x + 60, 118), (x - 60, 118),
                                              (x - 20, 50)]), col, BG_OUT, (0.1, 0.1))
    layer(1.0)
    shape(ctx, lambda c: c.rectangle(-3000, 900, 8000, 60), C["lab_bench"], BG_OUT, None)
    flat(ctx, lambda c: c.rectangle(-3000, 960, 8000, 3000), C["lab_bench_dk"])


def ds_shed(ctx, t, layer, p):
    """A garden-shed interior in summer: plank walls, a dusty window with a light beam, shelves with pots, cobwebs in
    every corner. Floor at y = 1500."""
    layer(0.9)
    flat(ctx, lambda c: c.rectangle(-3000, -2000, 8000, 5000), C["shed1"])
    for x in range(-3000, 5000, 150):
        flat(ctx, lambda c, x=x: c.rectangle(x, -2000, 8, 5000), C["shed2"])
        flat(ctx, lambda c, x=x: c.rectangle(x + 40, -2000, 30, 5000), C["shed3"], a=0.4)
    shape(ctx, lambda c: c.rectangle(820, 160, 420, 320), hexc("#cfe6c0"), BG_OUT, None)
    stroke(ctx, [(1030, 160), (1030, 480)], BG_OUT)
    stroke(ctx, [(820, 320), (1240, 320)], BG_OUT)
    ctx.save()
    ctx.move_to(820, 160)
    ctx.line_to(1240, 160)
    ctx.line_to(700, 1500)
    ctx.line_to(-100, 1500)
    ctx.close_path()
    src(ctx, (1, 0.97, 0.8), 0.12)
    ctx.fill()
    ctx.restore()
    for y in (700, 1000):
        shape(ctx, lambda c, y=y: c.rectangle(-500, y, 900, 26), hexc("#5a3f26"), BG_OUT, None)
        for k in range(4):
            x = -420 + k * 220
            shape(ctx, lambda c, x=x, y=y: p_poly(c, [(x - 50, y - 90), (x + 50, y - 90), (x + 36, y), (x - 36, y)]),
                  hexc("#c0623c"), BG_OUT, (0.1, 0.1))
    for (wx, wy, seed) in ((-700, -60, 1), (1600, -60, 2), (430, 120, 3), (1400, 560, 4), (-300, 420, 5)):
        ctx.save()
        ctx.translate(wx, wy)
        ctx.scale(0.55, 0.55)
        ds_web(ctx, t, {"w": 600, "h": 700, "seed": seed, "a": 0.6})
        ctx.restore()
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 3000), hexc("#5e452a"))
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)


def ds_board_bg(ctx, t, layer, p):
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-4000, -4000, 9000, 9000), hexc(p.get("color", "#1b1724")))
    ctx.save()
    ctx.set_source_rgba(1, 1, 1, 0.04)
    ctx.set_line_width(2)
    for x in range(-4000, 5000, 80):
        ctx.move_to(x, -4000)
        ctx.line_to(x, 5000)
    ctx.stroke()
    ctx.restore()


ACTORS = {"carol": carol, "ds_web": ds_web, "giant_spider": giant_spider, "ds_shadow": ds_shadow,
          "house_sp_small": house_sp_small, "crane_fly": crane_fly, "woodlouse": woodlouse, "false_widow": false_widow,
          "redback": redback, "recluse": recluse, "jumper": jumper, "ds_tag": ds_tag, "ds_dim": ds_dim,
          "ds_label": ds_label, "ds_shoe": ds_shoe, "ds_prop": ds_prop, "ds_board": ds_board, "ds_pie": ds_pie,
          "ds_lineup": ds_lineup, "ds_map": ds_map, "ds_arena": ds_arena, "ds_houses": ds_houses,
          "ds_chip_src": ds_chip_src, "ds_lineup_mask": ds_lineup_mask, "ds_bubble": ds_bubble}
SCENES = {"ds_corner": ds_corner, "ds_floor": ds_floor, "ds_lab": ds_lab, "ds_shed": ds_shed, "ds_wall": ds_wall,
          "ds_board_bg": ds_board_bg}


# ================================================================================================ phase 2 pictures

import drawn_bugs as _bugs   # noqa: E402


def js_front(ctx, t, p):
    """Jumping spider, front view: compact fuzzy body, two huge forward eyes, short thick legs (drawn_bugs)."""
    _bugs.jumping_spider(ctx, t, p)


def ds_orb(ctx, t, p):
    """A neat wheel (orb) web: radials + a spiral; origin = hub. p: r, a, jiggle (0..1 the web shakes)."""
    R = p.get("r", 380)
    a = p.get("a", 0.9)
    jg = p.get("jiggle", 0.0) * 14 * math.sin(t * 30)
    n = 14
    for k in range(n):
        ang = 2 * math.pi * k / n
        stroke(ctx, [(0, 0), (R * math.cos(ang) + jg, R * math.sin(ang))], 2.6, color=(1, 1, 1), a=a)
    pts = []
    for j in range(260):
        ang = j * 2 * math.pi / n * 0.5
        r = 40 + (R - 50) * j / 260
        pts.append((r * math.cos(ang) + jg * r / R, r * math.sin(ang)))
    stroke(ctx, pts, 2.0, color=(1, 1, 1), a=a * 0.85)


_CONT = [  # (longitude deg, latitude, rx, ry, name) crude blobs for a cartoon globe
    (-100, -45, 70, 70, "NA"), (-60, 40, 45, 80, "SA"), (15, -55, 60, 40, "EU"), (20, 20, 60, 80, "AF"),
    (90, -40, 100, 60, "AS"), (135, 75, 60, 40, "AUSTRALIA")]


def ds_globe(ctx, t, p):
    """A cartoon globe; p: rot (degrees, the spin), hi (name of a blob to highlight in yellow), pin (0..1)."""
    R = 300
    shape(ctx, lambda c: p_ellipse(c, 0, 0, R, R), hexc("#4f8fc6"), OUT, (0.1, 0.1), hi=(0.3, 0.25, 0.25))
    rot = p.get("rot", 0.0)
    ctx.save()
    p_ellipse(ctx, 0, 0, R, R)
    ctx.clip()
    for lon, lat, rx, ry, name in _CONT:
        a = math.radians(lon - rot)
        if math.cos(a) <= 0.05:
            continue
        x = R * math.sin(a)
        col = hexc("#ffd34d") if name == p.get("hi") else hexc("#7cc46a")
        shape(ctx, lambda c, x=x, lat=lat, rx=rx, ry=ry, a=a, name=name: p_blob(c, x, lat * 2.2, rx * max(0.2, math.cos(a)),
                                                                              ry, 0.15, len(name)), col, OUT * 0.6, None)
    ctx.restore()
    ctx.save()
    p_ellipse(ctx, 0, 0, R, R)
    ink(ctx, OUT)
    ctx.stroke()
    ctx.restore()
    if p.get("pin", 0.0) > 0 and p.get("hi"):
        lon, lat = next((c[0], c[1]) for c in _CONT if c[4] == p["hi"])
        x = R * math.sin(math.radians(lon - rot))
        pp = back_out(min(1.0, p["pin"]))
        y = lat * 2.2
        shape(ctx, lambda c: (c.move_to(x, y), c.curve_to(x - 40, y - 50, x - 34, y - 90, x, y - 90),
                              c.curve_to(x + 34, y - 90, x + 40, y - 50, x, y)), C["red"], OUT * 0.7, None, a=min(1.0, pp))
        text(ctx, p["hi"], x, y + 60, 54, "#ffffff", None, min(1.0, pp))


def _bundle(ctx, x, y, r, burst=0.0, t=0.0):
    if burst < 0.99:
        shape(ctx, lambda c: p_ellipse(c, x, y, r * (1 - burst), r * 0.9 * (1 - burst)), hexc("#f3ead2"), OUT * 0.45, (0, 0.2))
        rng = random.Random(4)
        for k in range(12):
            a, rr = rng.uniform(0, 6.28), rng.uniform(0, r * 0.65)
            flat(ctx, lambda c, a=a, rr=rr: p_ellipse(c, x + rr * math.cos(a) * (1 - burst), y + rr * math.sin(a) * (1 - burst),
                                                      r * 0.18, r * 0.18), hexc("#d9c79f"), OUT * 0.12)
    if burst > 0:
        rng = random.Random(8)
        for k in range(26):
            a, d = rng.uniform(0, 6.28), rng.uniform(0.4, 1.0)
            sx, sy = x + math.cos(a) * d * 260 * burst, y + math.sin(a) * d * 200 * burst
            flat(ctx, lambda c, sx=sx, sy=sy: p_ellipse(c, sx, sy, 6, 6), hexc("#e8dcc0"), OUT * 0.2)
            for s in (-1, 1):
                stroke(ctx, [(sx, sy), (sx + s * 10, sy - 8), (sx + s * 16, sy + 2)], 2, a=0.8)


def ds_bundle(ctx, t, p):
    """An egg bundle hanging on a strand (origin = the anchor above); p: len, burst (0..1 hatches), on."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    ln = p.get("len", 120)
    sw = 6 * math.sin(t * 2)
    stroke(ctx, [(0, 0), (sw, ln)], 2.4, color=(1, 1, 1), a=0.9 * (1 - p.get("burst", 0.0)))
    _bundle(ctx, sw, ln + 40 * on, 44 * on, p.get("burst", 0.0), t)


def ds_babies(ctx, t, p):
    """Spiderlings fanning out from the origin along a ceiling line; p: u (0..1 spread), n, dir (+1/-1 both)."""
    u = ease(p.get("u", 0.0))
    n = int(p.get("n", 14))
    rng = random.Random(5)
    for k in range(n):
        ang = rng.uniform(-0.25, 0.25)
        d = (300 + 1200 * rng.random()) * u
        sd = -1 if k % 2 else 1
        x, y = sd * d * math.cos(ang), d * math.sin(ang) * 0.4 + rng.uniform(-30, 30)
        bob = 4 * math.sin(t * 12 + k)
        for s in (-1, 1):
            for j in range(4):
                stroke(ctx, [(x, y + bob), (x + s * (18 + j * 4), y - 16 + j * 9 + bob), (x + s * (30 + j * 6), y - 2 + j * 12 + bob)],
                       2.4, color=hexc("#3a3024"))
        shape(ctx, lambda c, x=x, y=y, bob=bob: p_ellipse(c, x, y + bob, 9, 7), C["cell"], OUT * 0.25, None)


def ds_doorbell(ctx, t, p):
    """A tiny front door built into the web corner with a doorbell; p: ring (0..1), open (0..1)."""
    o = p.get("open", 0.0)
    shape(ctx, lambda c: c.rectangle(-110, -300, 220, 300), hexc("#2a2018"), OUT, None)
    w = 220 * (1 - 0.8 * o)
    shape(ctx, lambda c: c.rectangle(-110, -300, w, 300), hexc("#b0683a"), OUT, (0.1, 0))
    flat(ctx, lambda c: p_ellipse(c, -110 + w - 26, -150, 10, 10), hexc("#ffd34d"))
    shape(ctx, lambda c: c.rectangle(-140, -330, 280, 34), hexc("#6b4626"), OUT, None)
    shape(ctx, lambda c: p_rrect(c, 130, -200, 50, 70, 10), hexc("#e6e1d3"), OUT * 0.6, None)
    shape(ctx, lambda c: p_ellipse(c, 155, -165, 14, 14), hexc("#e5383b"), OUT * 0.5, None)
    r = p.get("ring", 0.0)
    if r > 0:
        for k in range(3):
            rr = 40 + k * 30 + 10 * math.sin(t * 20)
            ctx.new_sub_path()
            ctx.arc(155, -165, rr, -1.0, 1.0)
            ink(ctx, 5, r)
            ctx.stroke()
        text(ctx, "DING-DONG", 160, -330, 54, "#ffd34d", None, r)


def ds_court(ctx, t, layer, p):
    """A courtroom: wood-panelled wall, a judge's bench across the back; floor y = 1500."""
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, -2000, 8000, 5000), hexc("#7a5233"))
    for x in range(-3000, 5000, 220):
        shape(ctx, lambda c, x=x: c.rectangle(x + 20, 200, 180, 1000), hexc("#8a6040"), BG_OUT * 0.6, None)
    shape(ctx, lambda c: c.rectangle(-300, 900, 1700, 600), hexc("#5e3d23"), BG_OUT, (0, 0.1))
    shape(ctx, lambda c: c.rectangle(-340, 860, 1780, 60), hexc("#6b4626"), BG_OUT, None)
    shape(ctx, lambda c: p_ellipse(c, 550, 500, 150, 150), hexc("#d9b44a"), BG_OUT, (0.1, 0.1))
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 3000), hexc("#4a3220"))
    _grade_night(ctx)


def ds_sheet(ctx, t, p):
    """A charge sheet scroll unrolling downward from its top bar; p: unroll 0..1, line (big text), small (0..1)."""
    u = ease(p.get("unroll", 1.0))
    Hs = 620 * u
    shape(ctx, lambda c: c.rectangle(-300, 0, 600, max(2, Hs)), PAL["paper"], OUT, (0, 0.06))
    shape(ctx, lambda c: p_rrect(c, -330, -30, 660, 50, 25), PAL["paper_dk"], OUT, None)
    if u > 0.3:
        text(ctx, "CHARGES", 0, 60, 60, "#222222", 0, min(1.0, (u - 0.3) * 3))
    if p.get("line") and u > 0.6:
        text(ctx, p["line"], 0, 200, 92, "#c0392b", 0, min(1.0, (u - 0.6) * 3))
    if p.get("small", 0.0) > 0 and u > 0.8:
        for k in range(6):
            stroke(ctx, [(-220, 330 + k * 30), (220 - (k == 5) * 200, 330 + k * 30)], 4, color=(0.5, 0.5, 0.5),
                   a=p["small"])


def ds_rumor(ctx, t, p):
    """THE RUMOR as a paper card; p: crack (0..1: splits in two, the halves fall away), text."""
    cr = p.get("crack", 0.0)
    txt = p.get("text", "THE RUMOR")
    for half in (-1, 1):
        ctx.save()
        dx = half * 60 * cr
        dy = 500 * cr * cr
        ctx.translate(dx, dy)
        ctx.rotate(half * 0.5 * cr)
        ctx.save()
        if half < 0:
            ctx.rectangle(-500, -300, 500, 600)
        else:
            ctx.rectangle(0, -300, 500, 600)
        ctx.clip()
        shape(ctx, lambda c: p_rrect(c, -420, -170, 840, 340, 18), PAL["paper"], OUT, (0, 0.1))
        text(ctx, txt, 0, -40, 120, "#c0392b", 0)
        for k in range(3):
            stroke(ctx, [(-330, 70 + k * 36), (330 - k * 90, 70 + k * 36)], 6, color=(0.6, 0.6, 0.6))
        ctx.restore()
        ctx.restore()
    if 0 < cr < 0.3:
        stroke(ctx, [(0, -170), (20, -80), (-15, 10), (15, 90), (0, 170)], 8, a=1 - cr * 3)


def ds_fangs(ctx, t, p):
    """Diagram: two small fangs above a cross-section of skin (outer layer, softer layer); p: dip (0..1)."""
    d = ease(p.get("dip", 0.0))
    flat(ctx, lambda c: c.rectangle(-700, 0, 1400, 70), hexc("#f1c7a0"))
    flat(ctx, lambda c: c.rectangle(-700, 70, 1400, 300), hexc("#e7a283"))
    stroke(ctx, [(-700, 0), (700, 0)], 6)
    stroke(ctx, [(-700, 70), (700, 70)], 3, a=0.5)
    for s in (-1, 1):
        x = s * 70
        y = -260 + 290 * d
        shape(ctx, lambda c, x=x, y=y: p_poly(c, [(x - 34, y - 140), (x + 34, y - 140), (x + 6 * s, y), (x - 4 * s, y - 10)]),
              hexc("#3a2418"), OUT * 0.6, (0.1, 0.1))
    shape(ctx, lambda c: p_rrect(c, -170, -500 + 290 * d, 340, 130, 40), C["cell"], OUT * 0.7, (0, 0.2))
    text(ctx, "SKIN", 560, 40, 52, "#ffffff", None)


def ds_scale(ctx, t, p):
    """A balance: the left pan holds a tiny Carol, the right a weight; p: tilt (0..1 the heavy side drops), label."""
    tl = ease(p.get("tilt", 1.0)) * 0.22
    shape(ctx, lambda c: p_poly(c, [(-60, 0), (60, 0), (20, -420), (-20, -420)]), PAL["steel_dk"], OUT, None)
    ctx.save()
    ctx.translate(0, -420)
    ctx.rotate(tl)
    stroke(ctx, [(-380, 0), (380, 0)], 26)
    stroke(ctx, [(-380, 0), (380, 0)], 14, color=PAL["steel"])
    ctx.restore()
    for s in (-1, 1):
        px, py = s * 380 * math.cos(tl), -420 + s * 380 * math.sin(tl)
        stroke(ctx, [(px, py), (px - 110, py + 200)], 4)
        stroke(ctx, [(px, py), (px + 110, py + 200)], 4)
        shape(ctx, lambda c, px=px, py=py: p_ellipse(c, px, py + 200, 140, 30), PAL["steel"], OUT, (0, 0.3))
        if s < 0:
            ctx.save()
            ctx.translate(px, py + 120)
            ctx.scale(0.22, 0.22)
            carol(ctx, t, {"mood": "smug", "still": True})
            ctx.restore()
        else:
            shape(ctx, lambda c, px=px, py=py: p_poly(c, [(px - 90, py + 190), (px + 90, py + 190), (px + 60, py + 50), (px - 60, py + 50)]),
                  hexc("#45454d"), OUT, (0.1, 0.1))
            text(ctx, p.get("label", "5x"), px, py + 125, 80, "#ffffff", 0)


def ds_fade_row(ctx, t, p):
    """A row of big house spiders; the first `gone` of them (float) turn into dashed empty outlines with a '?'."""
    n = int(p.get("n", 5))
    gone = p.get("gone", 0.0)
    for k in range(n):
        x = (k - (n - 1) / 2) * 380
        g = max(0.0, min(1.0, gone - k))
        ctx.save()
        ctx.translate(x, 0)
        ctx.scale(0.42, 0.42)
        if g < 1:
            ctx.push_group()
            giant_spider(ctx, t + k, {"walk": 0.2, "mood": "worry"})
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(1 - g)
        if g > 0:
            ctx.set_dash([18, 14])
            p_ellipse(ctx, -60, -200, 260, 150)
            ink(ctx, 8, g)
            ctx.stroke()
            ctx.set_dash([])
            text(ctx, "?", -60, -200, 220, "#ffd34d", None, g)
        ctx.restore()


def ds_split(ctx, t, p):
    """Versus background: green left half, red right half, a jagged divider (world space, wide)."""
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 3000, 6000), hexc("#2b5f3f"))
    flat(ctx, lambda c: c.rectangle(0, -3000, 3000, 6000), hexc("#6b2a2a"))
    pts = [(0, -3000)] + [((-40 if k % 2 else 40), -1000 + k * 120) for k in range(20)] + [(0, 3000)]
    stroke(ctx, pts, 30, color=(1, 0.83, 0.3))


def ds_eyes(ctx, t, p):
    """A pair of shining eyes in the dark (something else is in the corner); p: on."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    bl = 0.1 if math.sin(t * 1.7) > 0.96 else 1.0
    for s in (-1, 1):
        shape(ctx, lambda c, s=s: p_ellipse(c, s * 60, 0, 44, 44 * bl), hexc("#1a1a1e"), OUT * 0.5, None, a=on)
        flat(ctx, lambda c, s=s: p_ellipse(c, s * 60 - 12, -14 * bl, 14, 14 * bl), (1, 1, 1), a=on)
        ctx.save()
        rg = cairo.RadialGradient(s * 60, 0, 10, s * 60, 0, 120)
        rg.add_color_stop_rgba(0, 0.7, 1, 0.8, 0.35 * on)
        rg.add_color_stop_rgba(1, 0.7, 1, 0.8, 0)
        ctx.set_source(rg)
        ctx.arc(s * 60, 0, 120, 0, 2 * math.pi)
        ctx.fill()
        ctx.restore()


def ds_building(ctx, t, p):
    """A block of flats in the snow, windows lit; p: webs (0..1: little webs fill the windows)."""
    shape(ctx, lambda c: c.rectangle(-420, -900, 840, 900), hexc("#8a7a6a"), OUT, (0.08, 0))
    shape(ctx, lambda c: p_poly(c, [(-460, -900), (460, -900), (380, -980), (-380, -980)]), hexc("#f2f4f8"), OUT, None)
    wb = p.get("webs", 0.0)
    for r in range(4):
        for k in range(4):
            x, y = -330 + k * 190, -820 + r * 200
            flat(ctx, lambda c, x=x, y=y: c.rectangle(x, y, 120, 130), hexc("#ffd98a"))
            ctx.rectangle(x, y, 120, 130)
            ink(ctx, OUT * 0.6)
            ctx.stroke()
            if wb > (r * 4 + k) / 16.0:
                for j in range(4):
                    a = j * 0.4
                    stroke(ctx, [(x + 4, y + 4), (x + 4 + 90 * math.cos(a), y + 4 + 90 * math.sin(a))], 2, color=(1, 1, 1))
                stroke(ctx, [(x + 40, y + 4), (x + 4, y + 40)], 2, color=(1, 1, 1))
                stroke(ctx, [(x + 70, y + 4), (x + 4, y + 70)], 2, color=(1, 1, 1))
    flat(ctx, lambda c: c.rectangle(-3000, 0, 6000, 900), hexc("#f2f4f8"))
    rng = random.Random(3)
    for k in range(80):
        x = rng.uniform(-1200, 1200)
        y = -1200 + ((rng.uniform(0, 1300) + t * 160 * (0.6 + rng.random())) % 1300)
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x + 15 * math.sin(t + k), y, 6, 6), (1, 1, 1))


def ds_house_ext(ctx, t, layer, p):
    """Outside the house at night: dark sky, a moon, the house with warm windows, lawn; house base at y = 1500."""
    layer(0.7)
    flat(ctx, lambda c: c.rectangle(-4000, -4000, 9000, 8000), hexc("#1b2440"))
    flat(ctx, lambda c: p_ellipse(c, 1500, 0, 90, 90), hexc("#f4f1d0"))
    rng = random.Random(1)
    for k in range(40):
        x, y = rng.uniform(-2500, 3500), rng.uniform(-1500, 700)
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 4, 4), (1, 1, 0.9), a=0.5 + 0.5 * math.sin(t * 2 + k))
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-4000, 1500, 9000, 3000), hexc("#2f5a33"))
    shape(ctx, lambda c: c.rectangle(-200, 600, 1500, 900), hexc("#c9b89a"), BG_OUT, (0.08, 0))
    shape(ctx, lambda c: p_poly(c, [(-300, 620), (1400, 620), (550, 60)]), hexc("#8a3a2c"), BG_OUT, (0.05, 0.1))
    for (x, y) in ((0, 800), (400, 800), (800, 800), (1080, 800), (0, 1150), (800, 1150)):
        shape(ctx, lambda c, x=x, y=y: c.rectangle(x, y, 200, 200), hexc("#ffd98a"), BG_OUT, None)
        stroke(ctx, [(x + 100, y), (x + 100, y + 200)], BG_OUT)
    shape(ctx, lambda c: c.rectangle(420, 1150, 180, 350), hexc("#6b4626"), BG_OUT, None)
    shape(ctx, lambda c: c.rectangle(1000, 240, 120, 300), hexc("#7a3a2c"), BG_OUT, None)
    _grade_night(ctx)


def ds_parade(ctx, t, p):
    """Eight spiders from eight other families walk past in a line (dark silhouettes, all different); p: u (0..1)."""
    u = p.get("u", 0.0)
    cfgs = [(1.0, 130, 100), (0.8, 160, 140), (1.3, 120, 80), (0.9, 150, 150), (0.75, 110, 120), (1.15, 170, 110),
            (0.95, 140, 90), (1.05, 120, 130)]
    for k, (L, ax, ay) in enumerate(cfgs):
        x = 1500 - (u * 3400) + k * 380
        if -1400 < x < 1400:
            ctx.save()
            ctx.translate(x, 0)
            ctx.scale(-0.4, 0.4)
            ctx.push_group()
            drawn_anatomy._spider(ctx, t + k, {"walk": 1.0}, {"color": "#2a2a30", "abd": (ax, ay), "leg": L,
                                                               "leg_w": 12 + k % 3 * 3, "hair": k % 2 == 0})
            pat = ctx.pop_group()
            ctx.set_source_rgba(0.08, 0.08, 0.12, 0.92)
            ctx.mask(pat)
            ctx.restore()


def ds_arenas(ctx, t, p):
    """Ten little lab arenas (5 x 2), each a cellar spider vs a noble false widow; p: grey (0..10 lost so far)."""
    g = p.get("grey", 0.0)
    order = [0, 3, 7, 1, 9, 5, 8]   # the seven that are lost, in the order they go grey
    for k in range(10):
        col, row = k % 5, k // 5
        x, y = (col - 2) * 340, row * 300
        shape(ctx, lambda c, x=x, y=y: p_rrect(c, x - 150, y - 230, 300, 230, 16), (0.85, 0.95, 1.0), OUT * 0.6, None, a=0.35)
        _remain_icon(ctx, "sp", x - 60, y - 70, 46)
        shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x + 70, y - 80, 42, 36), C["fw"], OUT * 0.5, (0, 0.2))
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x + 76, y - 92, 22, 9), C["fw_mark"])
        for s in (-1, 1):
            for j in range(3):
                stroke(ctx, [(x + 70, y - 70), (x + 70 + s * (40 + j * 8), y - 40 + j * 10)], 5, color=C["fw_dk"])
        if k in order:
            gi = order.index(k)
            a = max(0.0, min(1.0, g - gi))
            if a > 0:
                flat(ctx, lambda c, x=x, y=y: p_rrect(c, x - 150, y - 230, 300, 230, 16), hexc("#2a2a30"), a=0.7 * a)
                _wrapped(ctx, x - 60, y - 70, 70, 50, a)


def ds_whisper(ctx, t, p):
    """Gossip: wavy whisper lines and 'psst' around the origin; p: on."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    for k in range(4):
        a = k * 1.6 + 0.3
        x, y = 260 * math.cos(a), 200 * math.sin(a)
        stroke(ctx, [(x + j * 14, y + 10 * math.sin(t * 6 + j)) for j in range(6)], 5, smooth=True, a=on * 0.8)
    text(ctx, "PSST", 230, -200, 60, "#ffffff", None, on)


def ds_arrow(ctx, t, p):
    """A hand-drawn arrow from the origin to p['to']; p: grow, color."""
    g = ease(p.get("grow", 1.0))
    tx, ty = p.get("to", (300, 0))
    ex, ey = tx * g, ty * g
    col = hexc(p.get("color", "#ffd34d"))
    stroke(ctx, [(0, 0), (ex * 0.5, ey * 0.5 - 40), (ex, ey)], 22, smooth=True)
    stroke(ctx, [(0, 0), (ex * 0.5, ey * 0.5 - 40), (ex, ey)], 12, smooth=True, color=col)
    if g > 0.9:
        a = math.atan2(ey - (ey * 0.5 - 40), ex - ex * 0.5)
        for s in (-1, 1):
            stroke(ctx, [(ex, ey), (ex - 50 * math.cos(a + s * 0.5), ey - 50 * math.sin(a + s * 0.5))], 22)
            stroke(ctx, [(ex, ey), (ex - 50 * math.cos(a + s * 0.5), ey - 50 * math.sin(a + s * 0.5))], 12, color=col)


def ds_calgrid(ctx, t, p):
    """A calendar page of four weeks: a vacuum icon on every third week and a web count that drops; p: u (0..1)."""
    u = p.get("u", 1.0)
    shape(ctx, lambda c: p_rrect(c, -520, -380, 1040, 760, 24), (0.98, 0.97, 0.94), OUT, (0, 0.05))
    shape(ctx, lambda c: c.rectangle(-520, -380, 1040, 110), C["red"], OUT, None)
    text(ctx, "EVERY FEW WEEKS", 0, -325, 64, "#ffffff", 0)
    for r in range(4):
        for k in range(7):
            x, y = -450 + k * 130, -230 + r * 150
            stroke(ctx, [(x - 60, y - 60), (x + 60, y - 60)], 2, a=0.3)
            idx = r * 7 + k
            if idx % 10 == 3 and idx / 28 < u:
                ctx.save()
                ctx.translate(x, y + 50)
                ctx.scale(0.16, 0.16)
                _vacuum(ctx, t, {})
                ctx.restore()
    n = max(0, int(round(6 * (1 - u))))
    for k in range(n):
        ctx.save()
        ctx.translate(560 + (k % 2) * 140, -260 + (k // 2) * 180)
        ctx.scale(0.12, 0.12)
        ds_web(ctx, t, {"w": 500, "h": 600, "seed": k, "a": 0.9})
        ctx.restore()


def _clock(ctx, t, p):
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 120, 120), (0.98, 0.97, 0.94), OUT, (0, 0.1))
    for k in range(12):
        a = k * math.pi / 6
        stroke(ctx, [(100 * math.cos(a), 100 * math.sin(a)), (88 * math.cos(a), 88 * math.sin(a))], 5)
    h = p.get("hour", 2.0)
    ah = math.radians(h * 30 - 90)
    stroke(ctx, [(0, 0), (60 * math.cos(ah), 60 * math.sin(ah))], 12)
    stroke(ctx, [(0, 0), (0, -92)], 8)


def _towel(ctx, t, p):
    """A bath-towel outline (dashed), for the size of the biggest web."""
    ctx.set_dash([30, 18])
    p_rrect(ctx, -380, -260, 760, 520, 20)
    src(ctx, hexc("#ffd34d"))
    ctx.set_line_width(12)
    ctx.stroke()
    ctx.set_dash([])
    stroke(ctx, [(-380, 190), (380, 190)], 10, color=hexc("#ffd34d"), a=0.6)


def _comment(ctx, t, p):
    shape(ctx, lambda c: (p_rrect(c, -150, -110, 300, 180, 40)), (1, 1, 1), OUT, None)
    shape(ctx, lambda c: p_poly(c, [(-60, 68), (-20, 68), (-80, 130)]), (1, 1, 1), OUT * 0.8, None)
    for k in range(3):
        flat(ctx, lambda c, k=k: p_ellipse(c, -60 + k * 60, -20, 16, 16), INK)


def _shoe_prop(ctx, t, p):
    ctx.save()
    ctx.rotate(p.get("rot", -0.3))
    _shoe(ctx, p.get("k", 0.45))
    ctx.restore()


def _boiler(ctx, t, p):
    shape(ctx, lambda c: p_rrect(c, -170, -600, 340, 600, 30), hexc("#c9ced8"), OUT, (0.1, 0.1))
    shape(ctx, lambda c: p_ellipse(c, 0, -420, 70, 70), hexc("#2c3440"), OUT, None)
    flat(ctx, lambda c: p_ellipse(c, 0, -420, 40, 40), hexc("#ff9f1c"), a=0.7 + 0.3 * math.sin(t * 8))
    stroke(ctx, [(120, -600), (120, -900)], 26)
    stroke(ctx, [(120, -600), (120, -900)], 16, color=PAL["pipe"])


def _snowwin(ctx, t, p):
    shape(ctx, lambda c: c.rectangle(-180, -140, 360, 280), hexc("#c8dceb"), OUT, None)
    rng = random.Random(2)
    for k in range(30):
        x = -170 + rng.random() * 340
        y = -130 + ((rng.random() * 260 + t * 120) % 260)
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 5, 5), (1, 1, 1))
    flat(ctx, lambda c: c.rectangle(-180, 90, 360, 50), (1, 1, 1))
    stroke(ctx, [(0, -140), (0, 140)], BG_OUT)


def _nozzle(ctx, t, p):
    """A vacuum hose and nozzle reaching up from the bottom; origin = the nozzle mouth; p: suck (0..1 lines)."""
    stroke(ctx, [(0, 0), (60, 300), (20, 700), (120, 1400)], 70)
    stroke(ctx, [(0, 0), (60, 300), (20, 700), (120, 1400)], 54, color=hexc("#5b6b7a"))
    shape(ctx, lambda c: p_poly(c, [(-70, -10), (70, -10), (40, 120), (-40, 120)]), hexc("#e5383b"), OUT, (0, 0.2))
    s = p.get("suck", 0.0)
    if s > 0:
        for k in range(5):
            a = -math.pi / 2 + (k - 2) * 0.35
            r0 = 120 + ((t * 300 + k * 40) % 160)
            stroke(ctx, [(r0 * math.cos(a), -20 + r0 * math.sin(a)), ((r0 - 60) * math.cos(a), -20 + (r0 - 60) * math.sin(a))], 6, a=s)


def _bundles_shelf(ctx, t, p):
    """A lab shelf of egg bundles; p: n (2..8)."""
    shape(ctx, lambda c: c.rectangle(-560, 0, 1120, 30), hexc("#7a5233"), OUT, None)
    n = p.get("n", 2.0)
    for k in range(8):
        a = max(0.0, min(1.0, n - k))
        if a > 0:
            _bundle(ctx, -470 + k * 134, -50, 48 * back_out(a))
    text(ctx, str(int(min(8, max(2, math.floor(n + 0.001))))), 0, 120, 110, "#ffd34d")


def _fist(ctx, t, p):
    """A fist seen from the front with a ruler beside the knuckle and the tiny sore dot; p: dot (0..1)."""
    shape(ctx, lambda c: p_rrect(c, -260, -160, 520, 320, 90), PAL["skin"], OUT, (0.05, 0.2))
    for k in range(4):
        shape(ctx, lambda c, k=k: p_ellipse(c, -195 + k * 130, -150, 66, 50), PAL["skin"], OUT * 0.8, (0, 0.2))
    d = p.get("dot", 0.0)
    if d > 0:
        flat(ctx, lambda c: p_ellipse(c, -65, -170, 7 * d, 7 * d), hexc("#c0392b"))


PROPS.update(clock=_clock, towel=_towel, comment=_comment, shoe=_shoe_prop, boiler=_boiler, snowwin=_snowwin,
             nozzle=_nozzle, bundles=_bundles_shelf, fist=_fist)
ACTORS.update(js_front=js_front, ds_orb=ds_orb, ds_globe=ds_globe, ds_bundle=ds_bundle, ds_babies=ds_babies,
              ds_doorbell=ds_doorbell, ds_sheet=ds_sheet, ds_rumor=ds_rumor, ds_fangs=ds_fangs, ds_scale=ds_scale,
              ds_fade_row=ds_fade_row, ds_split=ds_split, ds_eyes=ds_eyes, ds_building=ds_building, ds_parade=ds_parade,
              ds_arenas=ds_arenas, ds_whisper=ds_whisper, ds_arrow=ds_arrow, ds_calgrid=ds_calgrid)
SCENES.update(ds_court=ds_court, ds_house_ext=ds_house_ext)
