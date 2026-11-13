"""Pictures for the polar bear long-form ("Your Life as a Polar Bear", tools/drawn_polarlife.py).
Same locked drawn look as the house-cat episode (drawn_kit shapes, ink outlines, flat fills, one cel shade); a
1920x1080 world where the ground (snow, ice, water line, floors) is y = 900 and boards on ds_board_bg are centred
on (0, 0).

The polar bear is drawn from its real body plan (the anatomy-kit rule: it reads from its silhouette): a long body
with the hindquarters as high as the shoulders, a LONG neck carried forward, a small head with a long straight
muzzle, small round ears, a black nose, a short tail nub, thick pillar legs and wide paws, a cream coat with an ink
outline. Ages: newborn, cub, young, adult (the mother), male (bigger, heavier neck), old (grey muzzle).

Scenes: pb_den (snow den cutaway), pb_slope (the den in a snow slope), pb_ice (pack, hole, edge, open, floes,
under, newice), pb_shore (Hudson Bay: summer / autumn, Churchill at the far right), pb_town, pb_facility,
pb_motel (room, breakfast, pool, bench), pb_desk (the tour desk).
Actors: see ACTORS at the bottom. Only labels the outline's `vis` names are drawn as text."""
import math
import random

import cairo

from drawn_ds_art import text
from drawn_kit import (BG_OUT, INK, OUT, back_out, darker, ease, flat, hexc, ink, lighter, limb, p_blob, p_ellipse,
                       p_poly, p_rrect, p_smooth, shape, src, stroke)

C = {k: hexc(v) for k, v in {
    "coat": "#f7f1de", "coat_dk": "#ddd3b5", "coat_new": "#f2e2dc", "grey": "#b9b4a8",
    "snow": "#f4f8fc", "snow2": "#dbe8f2", "snow3": "#c3d6e6", "ice": "#cfe4f2", "ice2": "#a9cbe2",
    "sky": "#bfe0f4", "sky2": "#e8f4fb", "dusk1": "#3a3f74", "dusk2": "#c98aa0", "water": "#2c5a80",
    "water_dk": "#17324c", "deep": "#123049", "seal": "#8d8f96", "seal_dk": "#64666e", "seal_ring": "#b9bcc4",
    "tundra": "#9c8a5a", "tundra2": "#7f8f4e", "rock": "#8a8a86", "berry": "#3b3f8f", "kelp": "#5b5a2a",
    "parka": "#f2711c", "parka_dk": "#c4560f", "wood": "#a8754a", "wood2": "#7c5232", "wall": "#e7dcc4",
    "wall2": "#cbbd9e", "carpet": "#6f7f99", "red": "#e5383b", "green": "#3fb950", "yel": "#ffd34d",
    "paper": "#fbf8ef", "board": "#1b1724", "steel": "#b7c0c9", "truck": "#3d6b8f", "truck_dk": "#2c5170",
    "tile": "#d9eef4", "pool": "#5fb6d8", "gold": "#f2b72c", "skin": "#e8b48a", "leather": "#6b3b22",
}.items()}

# ================================================================================================ the polar bear
# age -> body length, body height, leg length, head scale, muzzle length (share of head), fluff
AGES = {"newborn": (330, 170, 34, 1.25, 0.55, 0.0), "cub": (390, 230, 92, 1.2, 0.75, 1.0),
        "young": (560, 268, 150, 1.0, 1.0, 0.3), "adult": (640, 300, 172, 1.0, 1.05, 0.2),
        "male": (760, 356, 200, 1.0, 1.08, 0.2), "old": (640, 296, 168, 1.0, 1.05, 0.2)}


def _eye(ctx, x, y, r, shut=False, mood="calm", look=(0.0, 0.0)):
    if shut:
        stroke(ctx, [(x - r, y), (x, y + r * 0.55), (x + r, y)], max(3.0, r * 0.45), smooth=True)
        return
    shape(ctx, lambda c: p_ellipse(c, x, y, r, r * 1.08), (1, 1, 1), max(2.5, r * 0.32), None)
    pr = r * (0.42 if mood == "shock" else 0.58)
    px, py = x + look[0] * r * 0.35, y + look[1] * r * 0.35
    flat(ctx, lambda c: p_ellipse(c, px, py, pr, pr * 1.1), INK)
    flat(ctx, lambda c: p_ellipse(c, px - pr * 0.35, py - pr * 0.4, pr * 0.33, pr * 0.33), (1, 1, 1))
    if mood in ("worry", "shock"):
        stroke(ctx, [(x - r * 0.9, y - r * 1.25), (x + r * 0.8, y - r * 1.65)], max(3.0, r * 0.35))
    elif mood == "angry":
        stroke(ctx, [(x - r * 0.9, y - r * 1.65), (x + r * 0.9, y - r * 1.2)], max(3.0, r * 0.4))
    elif mood == "sleepy":
        flat(ctx, lambda c: c.rectangle(x - r * 1.2, y - r * 1.3, r * 2.4, r * 1.25), C["coat"])
        stroke(ctx, [(x - r, y - r * 0.05), (x + r, y - r * 0.05)], max(3.0, r * 0.35))


def pb_bear(ctx, t, p):
    """The polar bear, side view, facing right, origin = feet (swim: the water line). p: age (newborn | cub | young |
    adult | male | old), pose (stand | lie | curl | swim | sniff), walking/phase (from drawn.py), thin (0..1 a
    thinner body), shut (eyes shut), wiggle (newborn squirm), swipe (0..1 near front paw raised in an arc), shake
    (0..1 the body shakes; spray 0..1 a ring of water), under (swim seen from under water: no water overlay),
    pull (0..1 paddle strength), collar (GPS collar), seaweed (on the head), tag (gift tag), sil (0..1 dark
    silhouette, col), ghost (0..1 an empty dotted outline), a (alpha), mood, look, head (head height -1..1)."""
    a = p.get("a", 1.0)
    if a <= 0.01:
        return
    age = p.get("age", "adult")
    L, Hh, ll, hk, mz, fluff = AGES.get(age, AGES["adult"])
    thin = p.get("thin", 0.0)
    Hb = Hh * (1 - 0.24 * thin)
    pose = p.get("pose", "stand")
    sil, ghost = p.get("sil", 0.0), p.get("ghost", 0.0)
    grouped = a < 0.999 or sil > 0 or ghost > 0
    ctx.save()
    if grouped:
        ctx.push_group()
    if p.get("wiggle"):
        ctx.rotate(p["wiggle"] * 0.05 * math.sin(t * 9))
    sh = p.get("shake", 0.0)
    if sh > 0:
        ctx.rotate(0.07 * sh * math.sin(t * 34))
    col = C["coat_new"] if age == "newborn" else C["coat"]
    if age == "old":
        col = hexc("#ece6d2")
    dk = darker(col, 0.86)
    lie = pose in ("lie", "curl")
    swim = pose == "swim"
    legl = ll * (0.18 if lie else 1.0)
    by = -legl - Hb * 0.42 + 2.5 * math.sin(t * 2.2)
    if swim:
        by = Hb * 0.36
    walking = p.get("walking") or p.get("walk", 0.0) > 0
    ph = p.get("phase", t * 9) * (0.55 if age in ("adult", "male", "old") else 0.8)
    if age == "old":
        ph *= 0.7
    # ---- head position
    hr = Hh * 0.27 * hk
    hd = p.get("head", 0.0)
    if pose == "sniff":
        hd = 1.0
    if pose == "curl":
        hx, hy = L * 0.46, by + Hb * 0.18
    elif swim:
        hx, hy = L * 0.66, -Hb * 0.22
    else:
        hx = L * 0.74 - hd * L * 0.06
        hy = by - Hb * 0.42 + hd * (Hb * 0.42 + legl - hr * 0.7)
    if age in ("newborn", "cub"):
        hx -= L * 0.06
        hy += Hb * 0.05 if pose != "sniff" else 0
    # ---- legs (far pair first)

    def leg(x, far, k):
        w = Hb * (0.27 if age != "newborn" else 0.3)
        c_ = dk if far else col
        if lie:
            fx = x + (L * 0.16 if x > 0 else -L * 0.02)
            limb(ctx, [(x, by + Hb * 0.25), (fx, -Hb * 0.06)], w, c_, OUT * 0.75)
            shape(ctx, lambda c: p_ellipse(c, fx + w * 0.3, -w * 0.28, w * 0.75, w * 0.36), c_, OUT * 0.75, None)
            return
        if swim:
            front = x > 0
            pull = p.get("pull", 1.0)
            if front:
                u = math.sin(t * 3.2 + (0 if far else math.pi))
                fx, fy = x + L * 0.2 * u * pull, by + Hb * 0.55 + ll * (0.55 + 0.25 * math.cos(t * 3.2 + (0 if far else math.pi)))
                kx, ky = x + L * 0.08 * u * pull, by + Hb * 0.5
            else:
                fx, fy = x - L * 0.42, by + Hb * 0.25 + 12 * math.sin(t * 2 + k)
                kx, ky = x - L * 0.2, by + Hb * 0.35
            limb(ctx, [(x, by + Hb * 0.1), (kx, ky), (fx, fy)], w, c_, OUT * 0.75)
            shape(ctx, lambda c: p_ellipse(c, fx + (w * 0.2 if front else -w * 0.4), fy, w * 0.7, w * 0.4,
                                           0.4 if front else 0.1), c_, OUT * 0.75, None)
            return
        dx, lift = 0.0, 0.0
        if walking:
            s_ = math.sin(ph + k * math.pi / 2 + (math.pi if far else 0))
            dx, lift = L * 0.11 * s_, max(0.0, math.cos(ph + k * math.pi / 2 + (math.pi if far else 0))) * ll * 0.18
        if p.get("swipe", 0.0) > 0 and not far and x > 0:
            u = ease(min(1.0, p["swipe"]))
            ang = -0.2 - 2.0 * u
            kx, ky = x + 60 + 60 * u, by + Hb * 0.3 - 80 * u
            fx, fy = kx + 90 + 120 * u, ky + legl * (0.8 - 1.2 * u)
            limb(ctx, [(x, by + Hb * 0.1), (kx, ky), (fx, fy)], w, c_, OUT * 0.75)
            shape(ctx, lambda c: p_ellipse(c, fx, fy, w * 0.7, w * 0.5), c_, OUT * 0.75, None)
            return
        top = (x, by + Hb * 0.15)
        kn = (x + dx * 0.5 + (8 if x > 0 else -14), by + Hb * 0.35 + legl * 0.45)
        ft = (x + dx, -lift - w * 0.18)
        limb(ctx, [top, kn, ft], w, c_, OUT * 0.75)
        shape(ctx, lambda c: p_ellipse(c, ft[0] + w * 0.28, ft[1] + w * 0.02, w * 0.8, w * 0.32), c_, OUT * 0.75, None)
        if age not in ("newborn",):
            for k2 in range(3):   # claws hint
                stroke(ctx, [(ft[0] + w * (0.6 + k2 * 0.12), ft[1] + w * 0.2), (ft[0] + w * (0.75 + k2 * 0.12), ft[1] + w * 0.3)],
                       3, color=INK)

    legs = ((-L * 0.3, True, 0), (L * 0.27, True, 1), (-L * 0.25, False, 2), (L * 0.32, False, 3))
    for x, far, k in legs:
        if far:
            leg(x, far, k)
    # ---- tail nub
    shape(ctx, lambda c: p_ellipse(c, -L * 0.5, by - Hb * 0.18, Hb * 0.1, Hb * 0.08), col, OUT * 0.75, None)
    # ---- body: hindquarters high, a long back, deep chest

    def body(c):
        pts = [(-L * 0.5, by - Hb * 0.05), (-L * 0.4, by - Hb * 0.44), (-L * 0.12, by - Hb * 0.47), (L * 0.18, by - Hb * 0.46),
               (L * 0.38, by - Hb * 0.3), (L * 0.42, by + Hb * 0.12), (L * 0.3, by + Hb * 0.46), (0, by + Hb * 0.5),
               (-L * 0.35, by + Hb * 0.44)]
        if fluff:
            rnd = random.Random(7)
            pts = [(x_ + rnd.uniform(-6, 6) * fluff, y_ + rnd.uniform(-6, 6) * fluff) for x_, y_ in pts]
        p_smooth(c, pts)
    shape(ctx, body, col, OUT, (0.0, 0.16), hi=(0.3, 0.15, 0.2), shade_k=0.88)
    if fluff >= 1:
        for k in range(7):
            x0 = -L * 0.35 + k * L * 0.1
            stroke(ctx, [(x0, by - Hb * 0.44), (x0 + 10, by - Hb * 0.52), (x0 + 22, by - Hb * 0.45)], 4, smooth=True)
    # ---- neck: long, carried forward
    nw = Hb * (0.38 if age == "male" else 0.32) * (1 - 0.15 * thin)
    nx0, ny0 = L * 0.28, by - Hb * 0.12
    shape(ctx, lambda c: p_smooth(c, [(nx0 - nw * 0.4, ny0 - nw * 1.0), (hx - hr * 0.5, hy - hr * 0.55),
                                      (hx - hr * 0.2, hy + hr * 0.6), (nx0 + nw * 0.6, ny0 + nw * 0.9)]),
          col, OUT, (0.0, 0.18), shade_k=0.88)
    for x, far, k in legs:
        if not far:
            leg(x, far, k)
    if p.get("collar"):
        cx_, cy_ = (nx0 + hx) / 2 - hr * 0.25, (ny0 + hy) / 2
        ang = math.atan2(hy - ny0, hx - nx0)
        ctx.save()
        ctx.translate(cx_, cy_)
        ctx.rotate(ang)
        shape(ctx, lambda c: p_rrect(c, -nw * 0.18, -nw * 0.95, nw * 0.36, nw * 1.9, nw * 0.12), hexc("#3a3a40"), OUT * 0.6, None)
        shape(ctx, lambda c: p_rrect(c, -nw * 0.28, nw * 0.7, nw * 0.56, nw * 0.5, 8), hexc("#e2b13c"), OUT * 0.6, None)
        ctx.restore()
    # ---- head: small, long straight muzzle, small round ears, black nose
    ear = hr * 0.36
    for ex in (hx - hr * 0.55, hx - hr * 0.25):
        shape(ctx, lambda c, ex=ex: p_ellipse(c, ex, hy - hr * 0.78, ear, ear), col, OUT * 0.8, None)
        flat(ctx, lambda c, ex=ex: p_ellipse(c, ex, hy - hr * 0.76, ear * 0.5, ear * 0.5), darker(col, 0.72))
    mx = hx + hr * (0.6 + 0.75 * mz)
    head = lambda c: p_smooth(c, [(hx - hr * 0.9, hy - hr * 0.1), (hx - hr * 0.55, hy - hr * 0.8), (hx + hr * 0.1, hy - hr * 0.85),  # noqa
                                  (hx + hr * 0.55, hy - hr * 0.45), (mx, hy - hr * 0.2), (mx + hr * 0.18, hy + hr * 0.15),
                                  (mx - hr * 0.1, hy + hr * 0.45), (hx + hr * 0.2, hy + hr * 0.62), (hx - hr * 0.6, hy + hr * 0.55)])
    shape(ctx, head, col, OUT, (0.0, 0.16), shade_k=0.9)
    if age == "old":
        flat(ctx, lambda c: p_ellipse(c, mx - hr * 0.25, hy + hr * 0.15, hr * 0.55, hr * 0.32), C["grey"], a=0.85)
        for k in range(4):
            stroke(ctx, [(mx - hr * (0.6 - k * 0.15), hy + hr * 0.0), (mx - hr * (0.55 - k * 0.15), hy + hr * 0.3)], 3, color=hexc("#8f8a80"))
    nose_r = hr * (0.2 if age != "newborn" else 0.17)
    shape(ctx, lambda c: p_ellipse(c, mx + hr * 0.06, hy - hr * 0.08, nose_r * 1.1, nose_r * 0.85), INK, OUT * 0.5, None)
    flat(ctx, lambda c: p_ellipse(c, mx + hr * 0.0, hy - hr * 0.15, nose_r * 0.35, nose_r * 0.22), (1, 1, 1), a=0.7)
    stroke(ctx, [(mx - hr * 0.05, hy + hr * 0.28), (mx - hr * 0.45, hy + hr * 0.34)], 4.5)   # mouth line
    er = hr * (0.17 if age in ("newborn", "cub") else 0.13)
    _eye(ctx, hx + hr * 0.18, hy - hr * 0.3, er, p.get("shut", age == "newborn"), p.get("mood", "calm"),
         tuple(p.get("look", (0.6, 0.0))))
    if p.get("seaweed"):
        for k in range(4):
            stroke(ctx, [(hx - hr * 0.6 + k * hr * 0.3, hy - hr * 0.8), (hx - hr * 0.7 + k * hr * 0.3, hy - hr * 0.1),
                         (hx - hr * 0.5 + k * hr * 0.3, hy + hr * 0.5)], 12, smooth=True, color=hexc("#4f7a2a"))
    if p.get("tag"):
        stroke(ctx, [(nx0 + nw * 0.3, ny0 - nw * 0.6), (nx0 + nw * 0.6, ny0 + nw * 1.6)], 4, color=C["red"])
        ctx.save()
        ctx.translate(nx0 + nw * 0.6, ny0 + nw * 1.6)
        ctx.rotate(0.25 + 0.08 * math.sin(t * 3))
        shape(ctx, lambda c: p_poly(c, [(-50, 0), (50, 0), (50, 120), (-50, 120)]), C["yel"], OUT * 0.6, None)
        flat(ctx, lambda c: p_ellipse(c, 0, 18, 9, 9), INK)
        ctx.restore()
    if swim and not p.get("under"):
        ctx.rectangle(-L * 1.05, 6, L * 2.2, Hb * 2.2)
        src(ctx, hexc(p.get("wcol", "#1d4a70")), p.get("walpha", 0.62))
        ctx.fill()
        pts = [(x, 6 + 7 * math.sin(x / 40 + t * 4)) for x in range(int(-L * 1.05), int(L * 1.15), 30)]
        stroke(ctx, pts, 7, smooth=True, color=lighter(C["water"], 0.5))
        for k in range(3):   # wake
            w0 = -L * (0.55 + 0.25 * k)
            stroke(ctx, [(w0 - 60, 2), (w0, -8), (w0 + 60, 2)], 5, smooth=True, color=(1, 1, 1), a=0.6)
    if p.get("spray", 0.0) > 0.01:
        u = p["spray"]
        rnd = random.Random(3)
        for k in range(40):
            ang = 2 * math.pi * k / 40 + rnd.uniform(-0.05, 0.05)
            r = (L * 0.55 + rnd.uniform(0, L * 0.25)) * (0.5 + 0.7 * u)
            x, y = r * math.cos(ang), by + r * 0.6 * math.sin(ang)
            shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 9, 13), hexc("#a8daf5"), 3, None, a=min(1.0, 1.4 - u * 0.4))
    if grouped:
        pat = ctx.pop_group()
        if ghost > 0:
            ctx.set_source_rgba(1, 1, 1, 0.12 * ghost)
            ctx.mask(pat)
            ctx.save()
            ctx.set_dash([22, 18])
            p_ellipse(ctx, L * 0.05, by - Hb * 0.1, L * 0.62, Hb * 0.85)
            ctx.set_source_rgba(1, 1, 1, 0.9 * ghost)
            ctx.set_line_width(7)
            ctx.stroke()
            ctx.restore()
        elif sil > 0:
            ctx.set_source(pat)
            ctx.paint_with_alpha(a * (1 - sil))
            r, g, b = hexc(p.get("col", "#141820"))
            ctx.set_source_rgba(r, g, b, a * sil)
            ctx.mask(pat)
        else:
            ctx.set_source(pat)
            ctx.paint_with_alpha(a)
    ctx.restore()


def pb_seal(ctx, t, p):
    """A ringed seal, side view facing right, origin = belly on the ice. p: head_only (just the head up out of a hole,
    origin = the water surface; p rise 0..1), slide (0..1 lying flat, flippers back), icon (a small flat icon), a."""
    if p.get("a", 1.0) <= 0.01:
        return
    if p.get("head_only"):
        u = ease(min(1.0, p.get("rise", 1.0)))
        ctx.save()
        ctx.rectangle(-200, -400, 400, 400)
        ctx.clip()
        hy = 60 - 140 * u
        shape(ctx, lambda c: p_ellipse(c, 0, hy, 62, 70), C["seal"], OUT, (0.05, 0.15))
        shape(ctx, lambda c: p_ellipse(c, 34, hy + 18, 36, 26), lighter(C["seal"], 0.25), OUT * 0.7, None)
        flat(ctx, lambda c: p_ellipse(c, 60, hy + 8, 9, 7), INK)
        for s_ in (-12, 12):
            flat(ctx, lambda c, s_=s_: p_ellipse(c, s_ + 4, hy - 20, 12, 14), INK)
            flat(ctx, lambda c, s_=s_: p_ellipse(c, s_ + 1, hy - 25, 4, 4), (1, 1, 1))
        for k in (-1, 0, 1):
            stroke(ctx, [(58, hy + 22), (110, hy + 18 + 10 * k)], 2.5)
        ctx.restore()
        return
    k = 0.45 if p.get("icon") else 1.0
    ctx.save()
    ctx.scale(k, k)
    body = lambda c: p_smooth(c, [(-230, -40), (-120, -110), (60, -120), (170, -90), (215, -40), (180, 0), (-120, 0),  # noqa
                                  (-250, -10)])
    shape(ctx, body, C["seal"], OUT, (0.0, 0.18), hi=(0.35, 0.2, 0.2))
    if not p.get("icon"):
        rnd = random.Random(5)
        for _ in range(9):
            x, y = rnd.uniform(-170, 120), rnd.uniform(-95, -30)
            ctx.save()
            ctx.set_line_width(5)
            src(ctx, C["seal_ring"])
            p_ellipse(ctx, x, y, 16, 10)
            ctx.stroke()
            ctx.restore()
    shape(ctx, lambda c: p_poly(c, [(-235, -20), (-310, -60), (-300, 15)]), C["seal_dk"], OUT * 0.8, None)
    shape(ctx, lambda c: p_ellipse(c, 40, -10, 50, 20, 0.5), C["seal_dk"], OUT * 0.7, None)
    flat(ctx, lambda c: p_ellipse(c, 196, -66, 9, 8), INK)
    flat(ctx, lambda c: p_ellipse(c, 150, -84, 11, 12), INK)
    flat(ctx, lambda c: p_ellipse(c, 147, -88, 4, 4), (1, 1, 1))
    for kk in (-1, 0, 1):
        stroke(ctx, [(196, -56), (245, -60 + 10 * kk)], 2.5)
    ctx.restore()


def pb_bird(ctx, t, p):
    """A seabird sitting on the water (origin = water line), facing right; p bob."""
    ctx.save()
    ctx.translate(0, 4 * math.sin(t * 2.5))
    shape(ctx, lambda c: p_smooth(c, [(-110, -10), (-60, -70), (60, -60), (100, -20), (60, 10), (-80, 10)]),
          hexc("#3b3f47"), OUT, (0.0, 0.2))
    flat(ctx, lambda c: p_ellipse(c, 0, 0, 90, 18), (1, 1, 1))
    shape(ctx, lambda c: p_ellipse(c, 85, -85, 38, 32), hexc("#3b3f47"), OUT, None)
    shape(ctx, lambda c: p_poly(c, [(115, -92), (170, -80), (115, -72)]), hexc("#e8a33a"), OUT * 0.6, None)
    flat(ctx, lambda c: p_ellipse(c, 95, -92, 7, 7), (1, 1, 1))
    flat(ctx, lambda c: p_ellipse(c, 97, -92, 4, 4), INK)
    ctx.restore()


# ================================================================================================ scenes

def _sky(ctx, top, bot, y0=-1500, y1=900):
    g = cairo.LinearGradient(0, y0, 0, y1)
    for u, c_ in ((0, top), (1, bot)):
        g.add_color_stop_rgb(u, *(hexc(c_) if isinstance(c_, str) else c_))
    ctx.rectangle(-6000, -6000, 16000, 14000)
    ctx.set_source(g)
    ctx.fill()


def _snowfield(ctx, y0=900, col=None, seed=1):
    flat(ctx, lambda c: c.rectangle(-6000, y0, 16000, 4000), col or C["snow"])
    rnd = random.Random(seed)
    for _ in range(50):
        x, y = rnd.uniform(-2500, 4500), rnd.uniform(y0 + 20, y0 + 600)
        stroke(ctx, [(x - 60, y), (x, y - 10), (x + 70, y)], 4, smooth=True, color=C["snow2"])
    stroke(ctx, [(-6000, y0), (10000, y0)], BG_OUT)


def _ridges(ctx, y, n, seed, col=None, h=60):
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.uniform(-2500, 4500)
        w = rnd.uniform(120, 300)
        shape(ctx, lambda c, x=x, w=w: p_poly(c, [(x - w, y), (x - w * 0.2, y - h * rnd.uniform(0.6, 1.2)), (x + w * 0.3, y - h * 0.5),
                                                  (x + w, y)]), col or C["ice"], BG_OUT, (0.1, 0.1))


def pb_den(ctx, t, layer, p):
    """The snow den in cutaway: a snow bank, an entrance tunnel rising to the surface at the left, a round chamber
    (centre 980, 700; floor y = 900) lit blue. p: open (0..1 the roof breaks and light pours in), dim (0..1),
    dims (0..1 dimension arrows 1.5 M / 90 TO 100 CM)."""
    layer(0.6)
    _sky(ctx, "#6d8fc0", "#c9def0")
    layer(1.0)
    shape(ctx, lambda c: p_smooth(c, [(-3000, 300), (-400, 260), (300, 180), (900, 120), (1600, 160), (2400, 260), (5000, 300),
                                      (5000, 3000), (-3000, 3000)]), C["snow"], BG_OUT, None)
    for k in range(6):
        yy = 340 + k * 120
        stroke(ctx, [(-2000, yy + 40), (300, yy), (1600, yy + 10), (4000, yy + 50)], 3, smooth=True, color=C["snow2"])
    # tunnel from the surface down to the chamber
    stroke(ctx, [(140, 200), (300, 520), (560, 760), (700, 820)], 170, smooth=True, color=hexc("#9fbedb"))
    stroke(ctx, [(140, 200), (300, 520), (560, 760), (700, 820)], 140, smooth=True, color=hexc("#b9d3ea"))
    op = p.get("open", 0.0)
    # chamber
    g = cairo.RadialGradient(980, 700, 30, 980, 700, 520)
    g.add_color_stop_rgb(0, *hexc("#bfe3ff"))
    g.add_color_stop_rgb(1, *hexc("#6f9fd0"))
    p_ellipse(ctx, 980, 690, 520, 250)
    ctx.set_source(g)
    ctx.fill_preserve()
    ink(ctx, BG_OUT)
    ctx.stroke()
    flat(ctx, lambda c: c.rectangle(440, 900, 1100, 60), hexc("#a9c6e2"))
    stroke(ctx, [(470, 900), (1490, 900)], BG_OUT)
    if op > 0.01:
        u = ease(op)
        shape(ctx, lambda c: p_poly(c, [(900 - 140 * u, 120), (1080 + 140 * u, 120), (1060 + 60 * u, 450), (940 - 60 * u, 450)]),
              hexc("#fff8d8"), 0, None, a=0.75 * u)
        for k in range(6):
            x = 860 + k * 50
            shape(ctx, lambda c, x=x: p_poly(c, [(x, 440 - 200 * u - k * 20), (x + 40, 430 - 210 * u - k * 15), (x + 20, 470 - 200 * u)]),
                  C["snow"], OUT * 0.6, None)
    if p.get("dim", 0.0) > 0:
        ctx.rectangle(-6000, -6000, 16000, 14000)
        ctx.set_source_rgba(0.02, 0.04, 0.12, 0.6 * p["dim"])
        ctx.fill()
    d = p.get("dims", 0.0)
    if d > 0.01:
        a = min(1.0, d)
        y = 470
        stroke(ctx, [(470, y), (1490, y)], 7, color=C["yel"], a=a)
        for x, s_ in ((470, 1), (1490, -1)):
            stroke(ctx, [(x + s_ * 30, y - 22), (x, y), (x + s_ * 30, y + 22)], 7, color=C["yel"], a=a)
        text(ctx, "1.5 M", 980, y - 50, 70, "#ffd34d", 7, a)
        x = 1530
        stroke(ctx, [(x, 445), (x, 895)], 7, color=C["yel"], a=a)
        for yy, s_ in ((445, 1), (895, -1)):
            stroke(ctx, [(x - 22, yy + s_ * 30), (x, yy), (x + 22, yy + s_ * 30)], 7, color=C["yel"], a=a)
        text(ctx, "90 TO 100 CM", x + 180, 670, 46, "#ffd34d", 7, a)


def pb_slope(ctx, t, layer, p):
    """A white snow slope with the den hole (centre 1000, 560); the ground runs down to y = 900 at the right.
    p: dusk (0..1), crack (0..1 the roof of the hole breaking open)."""
    du = p.get("dusk", 0.0)
    layer(0.5)
    if du > 0.5:
        _sky(ctx, "#2b2f5c", "#c98aa0")
    else:
        _sky(ctx, "#8fc3ea", "#e8f4fb")
    layer(0.8)
    flat(ctx, lambda c: p_smooth(c, [(-3000, 700), (-500, 620), (400, 660), (1500, 600), (3000, 640), (6000, 700), (6000, 3000),
                                     (-3000, 3000)]), hexc("#d0dfee") if du < 0.5 else hexc("#8a90b8"))
    layer(1.0)
    snow = C["snow"] if du < 0.5 else hexc("#b9bfdc")
    shape(ctx, lambda c: p_smooth(c, [(-3000, 380), (-200, 340), (700, 380), (1300, 520), (1800, 800), (2300, 900), (6000, 900),
                                      (6000, 3000), (-3000, 3000)]), snow, BG_OUT, None)
    for k in range(5):
        stroke(ctx, [(200 + k * 250, 420 + k * 70), (500 + k * 250, 450 + k * 80)], 4, smooth=True, color=C["snow2"])
    shape(ctx, lambda c: p_ellipse(c, 1000, 560, 110, 70, -0.25), hexc("#2c3e5c") if du < 0.5 else hexc("#1a2036"), BG_OUT, None)
    cr = p.get("crack", 0.0)
    if cr > 0.01:
        for k in range(5):
            ang = -0.6 + k * 0.3
            stroke(ctx, [(1000, 560), (1000 + 180 * cr * math.cos(ang - 1.6), 560 + 160 * cr * math.sin(ang - 1.6))], 5)
    flat(ctx, lambda c: c.rectangle(-6000, 900, 16000, 3000), snow)
    if du > 0.5:
        flat(ctx, lambda c: p_ellipse(c, 1600, 180, 50, 50), hexc("#f6e7c0"))


def pb_ice(ctx, t, layer, p):
    """Sea ice. p kind: pack (flat ice with ridges to a horizon at y 560), hole (pack with a breathing hole at p hx,
    900), edge (ice to x = p ex, dark water beyond), open (black water to the horizon), floes (ice cracking into
    floes, p crack 0..1), under (under the surface: ice plates on top, blue below; the surface is y = 300),
    newice (grey new ice on the bay with a far shore). p dusk (0..1), freeze (0..1 new ice spreading, newice)."""
    kind = p.get("kind", "pack")
    du = p.get("dusk", 0.0)
    layer(0.4)
    if kind == "under":
        _sky(ctx, "#2f6f9f", "#0d2740", 300, 1400)
        layer(1.0)
        for k in range(-6, 14):
            x = k * 330
            shape(ctx, lambda c, x=x, k=k: p_poly(c, [(x, -1000), (x + 320, -1000), (x + 320, 300 + 30 * (k % 3)),
                                                      (x + 160, 330 + 40 * (k % 2)), (x, 300 + 20 * (k % 4))]),
                  C["ice2"], BG_OUT, (0.0, 0.1))
        for k in range(14):
            x = -400 + k * 230
            stroke(ctx, [(x, 360), (x + 90, 1300)], 30, color=(1, 1, 1), a=0.06)
        rnd = random.Random(2)
        for _ in range(25):
            x, y = rnd.uniform(-500, 2500), rnd.uniform(400, 1200)
            ctx.save()
            ctx.set_line_width(3)
            ctx.set_source_rgba(1, 1, 1, 0.4)
            p_ellipse(ctx, x, y - (t * 60 % 300), 8, 8)
            ctx.stroke()
            ctx.restore()
        return
    if du > 0.5:
        _sky(ctx, "#252a52", "#b98aa8", -1500, 560)
    else:
        _sky(ctx, "#9fcaec", "#eaf5fc", -1500, 560)
    hz = 560
    if kind == "open":
        flat(ctx, lambda c: c.rectangle(-6000, hz, 16000, 5000), C["water_dk"])
        for k in range(30):
            y = hz + 20 + k * k * 2.2
            rnd = random.Random(k)
            for _ in range(6):
                x = rnd.uniform(-1500, 3500)
                stroke(ctx, [(x, y), (x + 40 + k * 6, y)], 2 + k * 0.25, color=hexc("#3c6a92"), a=0.7)
        stroke(ctx, [(-6000, hz), (10000, hz)], BG_OUT * 0.6)
        return
    layer(0.7)
    far = C["ice"] if du < 0.5 else hexc("#8c90b8")
    flat(ctx, lambda c: c.rectangle(-6000, hz, 16000, 600), far)
    _ridges(ctx, hz + 5, 18, 4, lighter(far, 0.3), 40)
    stroke(ctx, [(-6000, hz), (10000, hz)], BG_OUT * 0.6)
    layer(1.0)
    snow = C["snow"] if du < 0.5 else hexc("#c4c8e2")
    if kind == "newice":
        flat(ctx, lambda c: c.rectangle(-6000, hz, 16000, 5000), hexc("#7f97ad"))
        fz = p.get("freeze", 1.0)
        rnd = random.Random(8)
        for k in range(60):
            x, y = rnd.uniform(-1200, 3200), rnd.uniform(hz + 20, 1400)
            if rnd.random() < fz:
                shape(ctx, lambda c, x=x, y=y: p_blob(c, x, y, 90 + (y - hz) * 0.25, 18 + (y - hz) * 0.06, 0.12, seed=k),
                      hexc("#d7e3ec"), 3, None)
        flat(ctx, lambda c: p_smooth(c, [(-3000, hz - 10), (-500, hz - 40), (600, hz - 25), (1500, hz - 50), (4000, hz - 20),
                                         (4000, hz + 5), (-3000, hz + 5)]), hexc("#8a7a5a"))
        return
    if kind == "edge":
        ex = p.get("ex", 1150)
        flat(ctx, lambda c: c.rectangle(-6000, hz + 120, 16000, 5000), C["water_dk"])
        shape(ctx, lambda c: p_poly(c, [(-6000, 900), (ex, 900), (ex + 60, 960), (ex + 20, 1040), (ex - 30, 4000), (-6000, 4000)]),
              snow, BG_OUT, None)
        shape(ctx, lambda c: p_poly(c, [(-6000, hz + 120), (ex + 300, hz + 120), (ex + 80, 900), (-6000, 900)]), snow, BG_OUT, None)
        shape(ctx, lambda c: p_poly(c, [(ex, 900), (ex + 60, 960), (ex + 20, 1040), (ex - 10, 1040), (ex - 20, 900)]),
              C["ice2"], BG_OUT, None)
        for k in range(8):
            y = hz + 160 + k * 60
            stroke(ctx, [(ex + 250 + k * 40, y), (ex + 400 + k * 60, y)], 4, color=hexc("#3c6a92"))
        return
    if kind == "floes":
        cr = p.get("crack", 1.0)
        flat(ctx, lambda c: c.rectangle(-6000, hz, 16000, 5000), C["water_dk"])
        rnd = random.Random(12)
        for row in range(5):
            y0 = hz + 40 + row * row * 30 + row * 40
            for k in range(-4, 12):
                x0 = k * 330 + (row % 2) * 160
                sep = cr * (30 + row * 18)
                dx = (x0 - 960) / 960 * sep
                ww, hh = 300 - sep * 0.6, 40 + row * 35
                pts = [(x0 + dx + rnd.uniform(-15, 15), y0 + rnd.uniform(-6, 6)), (x0 + dx + ww, y0 + rnd.uniform(-6, 6)),
                       (x0 + dx + ww + rnd.uniform(-20, 10), y0 + hh), (x0 + dx + rnd.uniform(-10, 20), y0 + hh)]
                shape(ctx, lambda c, pts=pts: p_poly(c, pts), snow, BG_OUT, (0.0, 0.25))
        return
    # pack / hole
    flat(ctx, lambda c: c.rectangle(-6000, hz, 16000, 5000), snow)
    _ridges(ctx, hz + 80, 10, 9, C["ice"], 60)
    for k in range(40):
        rnd = random.Random(k + 50)
        x, y = rnd.uniform(-2500, 4500), rnd.uniform(hz + 100, 1500)
        stroke(ctx, [(x - 70, y), (x, y - 8), (x + 80, y)], 4, smooth=True, color=C["snow2"])
    if p.get("crack", 0.0) > 0.01:
        u = p["crack"]
        pts = [(400, 1150), (700, 1000), (900, 1060), (1150, 940), (1500, 1010), (1900, 930)]
        stroke(ctx, pts, 8 + 30 * u, color=C["water_dk"])
        stroke(ctx, pts, 5)
    if kind == "hole":
        hx = p.get("hx", 1150)
        shape(ctx, lambda c: p_ellipse(c, hx, 905, 120, 34), C["snow2"], BG_OUT, None)
        shape(ctx, lambda c: p_ellipse(c, hx, 905, 80, 22), C["water_dk"], BG_OUT, None)


def pb_icecut(ctx, t, layer, p):
    """A cutaway of the sea ice: snow over ice over dark water, a breathing hole at x 1300 with a snow lid, the ice
    surface at y = 700 (bears stand there); p thick (0..1 the 90 CM OR MORE bracket), scent (0..1 the dotted scent
    line from the hole to x = p sx)."""
    layer(0.6)
    _sky(ctx, "#9fcaec", "#eaf5fc", -1500, 700)
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-6000, 700, 16000, 120), C["snow"])
    flat(ctx, lambda c: c.rectangle(-6000, 820, 16000, 160), C["ice2"])
    flat(ctx, lambda c: c.rectangle(-6000, 980, 16000, 3000), C["water_dk"])
    for y in (700, 820, 980):
        stroke(ctx, [(-6000, y), (10000, y)], BG_OUT * 0.7)
    shape(ctx, lambda c: p_poly(c, [(1240, 1000), (1270, 830), (1290, 760), (1320, 760), (1340, 830), (1370, 1000)]),
          C["water_dk"], BG_OUT, None)
    shape(ctx, lambda c: p_ellipse(c, 1305, 715, 120, 30), C["snow2"], BG_OUT * 0.7, None)
    th = p.get("thick", 0.0)
    if th > 0.01:
        a = min(1.0, th)
        x = 1440
        stroke(ctx, [(x, 705), (x, 975)], 7, color=C["yel"], a=a)
        for yy in (705, 975):
            stroke(ctx, [(x - 25, yy), (x + 25, yy)], 7, color=C["yel"], a=a)
        text(ctx, "90 CM OR MORE", x + 170, 840, 44, "#ffd34d", 7, a)
    sc = p.get("scent", 0.0)
    if sc > 0.01:
        sx = p.get("sx", 300)
        n = int(18 * min(1.0, sc))
        for k in range(n):
            x = 1305 - (1305 - sx) * k / 18
            flat(ctx, lambda c, x=x, k=k: p_ellipse(c, x, 620 - 40 * math.sin(k * 0.7 + t * 2), 10, 10), C["yel"])
        if sc > 0.95:
            text(ctx, "UP TO 1 KM", (1305 + sx) / 2, 500, 70, "#ffd34d", 7)


def pb_shore(ctx, t, layer, p):
    """The Hudson Bay shore: the bay at the left (water line y 760), tundra from y 900 with rocks; p season
    (summer | autumn), town (draw Churchill at x 2600..3800 with the sign at 2450), dusk (0..1)."""
    aut = p.get("season", "summer") == "autumn"
    du = p.get("dusk", 0.0)
    layer(0.5)
    _sky(ctx, "#9aa7b4" if aut else "#9fd0f0", "#d8dde2" if aut else "#eef7fb", -1500, 760)
    if du > 0.01:
        ctx.rectangle(-6000, -6000, 16000, 14000)
        ctx.set_source_rgba(0.15, 0.1, 0.3, 0.45 * du)
        ctx.fill()
    layer(0.75)
    flat(ctx, lambda c: c.rectangle(-6000, 700, 16000, 400), hexc("#5d7486") if aut else hexc("#4f86ad"))
    for k in range(10):
        y = 710 + k * 20
        stroke(ctx, [(-3000, y), (5000, y)], 2, color=(1, 1, 1), a=0.15)
    layer(1.0)
    land = hexc("#8d7d58") if aut else C["tundra"]
    shape(ctx, lambda c: p_smooth(c, [(-6000, 980), (-200, 960), (400, 840), (800, 790), (1400, 770), (8000, 760), (8000, 4000),
                                      (-6000, 4000)]), land, BG_OUT, None)
    stroke(ctx, [(380, 860), (700, 800), (1000, 785)], 14, smooth=True, color=C["kelp"])
    rnd = random.Random(4)
    for k in range(26):
        x, y = rnd.uniform(600, 3800), rnd.uniform(920, 1250)
        shape(ctx, lambda c, x=x, y=y, k=k: p_blob(c, x, y, rnd.uniform(40, 90), rnd.uniform(25, 45), 0.15, seed=k), C["rock"],
              BG_OUT, (0.05, 0.2))
    if not aut:
        for k in range(16):
            x, y = rnd.uniform(500, 3800), rnd.uniform(900, 1200)
            for j in range(5):
                stroke(ctx, [(x + j * 12, y), (x + j * 12 + 10, y - 50)], 5, color=C["tundra2"])
        for k in range(8):
            x, y = rnd.uniform(900, 2400), rnd.uniform(930, 1150)
            flat(ctx, lambda c, x=x, y=y: p_blob(c, x, y, 60, 30, 0.2, seed=9), hexc("#5e7a3a"))
            for j in range(4):
                flat(ctx, lambda c, j=j, x=x, y=y: p_ellipse(c, x - 30 + j * 20, y - 6 + (j % 2) * 10, 9, 9), C["berry"])
    else:
        for k in range(60):
            x, y = rnd.uniform(500, 4000), rnd.uniform(780, 1300)
            flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 18, 4), (1, 1, 1), a=0.7)
    if p.get("town"):
        _town(ctx, 2600, 900, sign_x=2400, snow=False)


def _building(ctx, x, w, h, col, y=900, roof=None):
    shape(ctx, lambda c: c.rectangle(x, y - h, w, h), col, BG_OUT, (0.04, 0.1))
    shape(ctx, lambda c: c.rectangle(x - 14, y - h - 22, w + 28, 26), roof or darker(col, 0.7), BG_OUT, None)
    for wx in range(int(x + 40), int(x + w - 90), 140):
        shape(ctx, lambda c, wx=wx: c.rectangle(wx, y - h + 50, 70, 60), hexc("#ffe9a8"), OUT * 0.5, None)


def _sign(ctx, x, y, label="CHURCHILL"):
    for px in (x - 150, x + 150):
        shape(ctx, lambda c, px=px: c.rectangle(px - 12, y - 260, 24, 260), C["wood2"], OUT * 0.7, None)
    shape(ctx, lambda c: p_rrect(c, x - 230, y - 330, 460, 120, 12), hexc("#2e6b45"), OUT, (0.03, 0.1))
    text(ctx, label, x, y - 270, 70, "#ffffff", 0)


def _town(ctx, x0, y, sign_x=None, snow=True):
    for k, (dx, w, h, col) in enumerate(((0, 420, 220, "#c86a4a"), (520, 360, 260, "#5b84a8"), (980, 480, 200, "#d9b44a"),
                                         (1560, 380, 240, "#7a9a6a"), (2040, 460, 210, "#b8574a"))):
        _building(ctx, x0 + dx, w, h, hexc(col), y)
        if snow:
            flat(ctx, lambda c, dx=dx, w=w, h=h: p_rrect(c, x0 + dx - 14, y - h - 34, w + 28, 18, 9), (1, 1, 1))
    if sign_x is not None:
        _sign(ctx, sign_x, y)


def pb_town(ctx, t, layer, p):
    """Churchill: low buildings along a snowy road, the town sign at x 760; p dusk (0..1), sign (draw it)."""
    du = p.get("dusk", 0.0)
    layer(0.5)
    if du > 0.5:
        _sky(ctx, "#232852", "#c27f8f")
    else:
        _sky(ctx, "#a9d2ee", "#eef6fb")
    layer(1.0)
    _town(ctx, 1000, 900, sign_x=760 if p.get("sign", True) else None)
    _town(ctx, -1700, 900)
    _snowfield(ctx, 900, C["snow"] if du < 0.5 else hexc("#b9bed9"), 5)
    flat(ctx, lambda c: c.rectangle(-6000, 960, 16000, 70), hexc("#c9ced6"))
    if du > 0.5:
        ctx.rectangle(-6000, -6000, 16000, 14000)
        ctx.set_source_rgba(0.08, 0.06, 0.2, 0.3)
        ctx.fill()


def pb_facility(ctx, t, layer, p):
    """The holding facility. p view: "door" (outside: a long low grey building, the front door at x 960..1140, sill
    900), "cells" (inside: a row of six cells, x 160..1760; cell 6 is the heated one)."""
    view = p.get("view", "door")
    if view == "door":
        layer(0.5)
        _sky(ctx, "#a9d2ee", "#eef6fb")
        layer(1.0)
        shape(ctx, lambda c: c.rectangle(-600, 480, 3200, 420), hexc("#9aa3ab"), BG_OUT, (0.03, 0.1))
        shape(ctx, lambda c: c.rectangle(-620, 450, 3240, 40), hexc("#737c85"), BG_OUT, None)
        for x in range(-400, 2600, 260):
            stroke(ctx, [(x, 490), (x, 900)], 3, color=hexc("#848d95"))
        shape(ctx, lambda c: c.rectangle(960, 640, 180, 260), hexc("#5b6670"), BG_OUT, (0.04, 0.1))
        flat(ctx, lambda c: p_ellipse(c, 1110, 780, 10, 10), C["yel"])
        shape(ctx, lambda c: p_rrect(c, 1240, 560, 300, 90, 10), hexc("#2e6b45"), OUT * 0.6, None)
        text(ctx, "HOLDING FACILITY", 1390, 605, 34, "#ffffff", 0)
        _snowfield(ctx, 900, None, 7)
        return
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-6000, -6000, 16000, 14000), hexc("#5e6870"))
    flat(ctx, lambda c: c.rectangle(-6000, 900, 16000, 3000), hexc("#8b949c"))
    stroke(ctx, [(-6000, 900), (10000, 900)], BG_OUT)
    for k in range(6):
        x = 160 + k * 270
        heated = k == 5
        shape(ctx, lambda c, x=x: c.rectangle(x, 380, 250, 520), hexc("#e8d9b8") if heated else hexc("#c9dbe6"), BG_OUT, None)
        for j in range(6):
            stroke(ctx, [(x + 20 + j * 42, 380), (x + 20 + j * 42, 900)], 8, color=hexc("#3f474e"))
        if heated:
            shape(ctx, lambda c, x=x: p_rrect(c, x + 50, 260, 150, 100, 10), hexc("#e86a2c"), OUT * 0.7, None)
            for j in range(3):
                stroke(ctx, [(x + 85 + j * 40, 245), (x + 75 + j * 40, 215 - 10 * math.sin(t * 4 + j)), (x + 90 + j * 40, 190)],
                       5, smooth=True, color=C["red"])
        else:
            shape(ctx, lambda c, x=x: p_rrect(c, x + 40, 260, 170, 100, 10), hexc("#dfe5ea"), OUT * 0.7, None)
            for j in range(4):
                stroke(ctx, [(x + 60 + j * 38, 285), (x + 60 + j * 38, 335)], 5, color=hexc("#7d8790"))
            for j in range(3):
                stroke(ctx, [(x + 70 + j * 45, 375), (x + 60 + j * 45, 400 + 8 * math.sin(t * 5 + j)), (x + 75 + j * 45, 425)],
                       4, smooth=True, color=hexc("#8fd0ff"))


def pb_motel(ctx, t, layer, p):
    """The motel. p kind: room (a bed, a desk with a small fan, a window; floor 900), breakfast (a counter with
    waffles, a wall clock at 1500, 330; a table at 700), pool (an indoor pool: water from x 300 to 1700, the water
    line y 860, the pool floor 1000; the deck y 900 outside it), bench (outside: the motel front with a sign and a
    bench at x 900, snow from 900)."""
    kind = p.get("kind", "room")
    layer(1.0)
    if kind == "bench":
        _sky(ctx, "#a9d2ee", "#eef6fb")
        shape(ctx, lambda c: c.rectangle(-600, 380, 3200, 520), hexc("#b5655a"), BG_OUT, (0.03, 0.1))
        for x in range(-500, 2600, 300):
            shape(ctx, lambda c, x=x: c.rectangle(x, 520, 150, 150), hexc("#ffe9a8"), OUT * 0.6, None)
        shape(ctx, lambda c: p_rrect(c, 1250, 180, 420, 130, 14), hexc("#2c3e5c"), OUT, None)
        text(ctx, "MOTEL", 1460, 245, 80, "#ffd34d", 0)
        _snowfield(ctx, 900, None, 3)
        shape(ctx, lambda c: c.rectangle(700, 770, 420, 34), C["wood"], OUT * 0.7, None)
        for x in (730, 1060):
            shape(ctx, lambda c, x=x: c.rectangle(x, 800, 26, 100), C["wood2"], OUT * 0.6, None)
        return
    flat(ctx, lambda c: c.rectangle(-6000, -6000, 16000, 14000), C["wall"] if kind != "pool" else C["tile"])
    if kind == "pool":
        for x in range(-1000, 3000, 80):
            stroke(ctx, [(x, -1000), (x, 900)], 2, color=hexc("#b9d6e0"))
        for y in range(-1000, 900, 80):
            stroke(ctx, [(-1000, y), (3000, y)], 2, color=hexc("#b9d6e0"))
        flat(ctx, lambda c: c.rectangle(-6000, 900, 16000, 3000), hexc("#c9dfe6"))
        flat(ctx, lambda c: c.rectangle(300, 860, 1400, 300), C["pool"])
        stroke(ctx, [(300, 900), (300, 1160), (1700, 1160), (1700, 900)], BG_OUT)
        pts = [(x, 860 + 6 * math.sin(x / 50 + t * 3)) for x in range(300, 1710, 25)]
        stroke(ctx, pts, 6, smooth=True, color=(1, 1, 1), a=0.8)
        stroke(ctx, [(-6000, 900), (300, 900)], BG_OUT)
        stroke(ctx, [(1700, 900), (10000, 900)], BG_OUT)
        text(ctx, "SHALLOW END", 520, 820, 40, "#2c5a80", 0)
        return
    flat(ctx, lambda c: c.rectangle(-6000, 900, 16000, 3000), C["carpet"] if kind == "room" else hexc("#b98a5a"))
    stroke(ctx, [(-6000, 900), (10000, 900)], BG_OUT)
    if kind == "room":
        shape(ctx, lambda c: c.rectangle(1250, 250, 400, 300), hexc("#cfe6f5"), BG_OUT, None)
        stroke(ctx, [(1450, 250), (1450, 550)], BG_OUT)
        shape(ctx, lambda c: c.rectangle(80, 700, 560, 200), hexc("#e9e2d2"), BG_OUT, (0.03, 0.1))
        shape(ctx, lambda c: c.rectangle(60, 560, 40, 340), C["wood2"], BG_OUT, None)
        shape(ctx, lambda c: p_rrect(c, 110, 650, 160, 70, 25), (1, 1, 1), OUT * 0.6, None)
        shape(ctx, lambda c: c.rectangle(1300, 700, 420, 30), C["wood"], OUT * 0.7, None)
        for x in (1320, 1680):
            shape(ctx, lambda c, x=x: c.rectangle(x, 730, 22, 170), C["wood2"], OUT * 0.5, None)
        # the small desk fan
        stroke(ctx, [(1500, 700), (1500, 620)], 10)
        shape(ctx, lambda c: p_ellipse(c, 1500, 580, 60, 60), hexc("#dfe5ea"), OUT * 0.8, None)
        for k in range(3):
            ang = t * 18 + k * 2.1
            shape(ctx, lambda c, ang=ang: p_ellipse(c, 1500 + 28 * math.cos(ang), 580 + 28 * math.sin(ang), 26, 12, ang),
                  hexc("#8fb8d8"), 3, None)
        return
    # breakfast
    shape(ctx, lambda c: c.rectangle(1050, 640, 800, 260), hexc("#9a6a42"), BG_OUT, (0.03, 0.1))
    shape(ctx, lambda c: c.rectangle(1030, 620, 840, 30), hexc("#d9c8a8"), BG_OUT, None)
    for k in range(3):
        x = 1150 + k * 250
        shape(ctx, lambda c, x=x: p_ellipse(c, x, 610, 90, 18), (1, 1, 1), OUT * 0.6, None)
        for j in range(3):
            shape(ctx, lambda c, x=x, j=j: p_rrect(c, x - 60 + j * 6, 560 - j * 16, 120, 30, 6), C["gold"], OUT * 0.5, None)
    text(ctx, "BREAKFAST", 1450, 520 - 120, 60, "#7c5232", 0)
    shape(ctx, lambda c: c.rectangle(450, 700, 520, 26), C["wood"], OUT * 0.7, None)
    shape(ctx, lambda c: c.rectangle(690, 726, 30, 174), C["wood2"], OUT * 0.6, None)
    if p.get("clock") is None:
        return
    mn = p.get("clock", 0.0)
    cx, cy = 1500, 300
    shape(ctx, lambda c: p_ellipse(c, cx, cy, 120, 120), (0.98, 0.97, 0.93), OUT, (0.04, 0.15))
    for k in range(12):
        a_ = k * math.pi / 6
        stroke(ctx, [(cx + 95 * math.cos(a_), cy + 95 * math.sin(a_)), (cx + 108 * math.cos(a_), cy + 108 * math.sin(a_))], 5)
    hr_ = 6 + mn / 60
    for ang, ln, lw in ((hr_ / 12 * 2 * math.pi, 60, 10), (mn / 60 * 2 * math.pi, 90, 6)):
        stroke(ctx, [(cx, cy), (cx + ln * math.sin(ang), cy - ln * math.cos(ang))], lw)


def pb_desk(ctx, t, layer, p):
    """The tour desk: a counter (top y 640) at x 300..1300 and a brochure rack at 1500..1800 (p cat 0..1: the top
    brochure shows a cat on a sofa)."""
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-6000, -6000, 16000, 14000), hexc("#d8e4ea"))
    flat(ctx, lambda c: c.rectangle(-6000, 900, 16000, 3000), hexc("#7a6a5a"))
    stroke(ctx, [(-6000, 900), (10000, 900)], BG_OUT)
    shape(ctx, lambda c: p_rrect(c, 380, 160, 700, 120, 14), hexc("#2c3e5c"), OUT, None)
    text(ctx, "TOUR DESK", 730, 222, 64, "#ffd34d", 0)
    shape(ctx, lambda c: c.rectangle(300, 640, 1000, 260), C["wood"], BG_OUT, (0.03, 0.1))
    shape(ctx, lambda c: c.rectangle(280, 620, 1040, 30), C["wood2"], BG_OUT, None)
    shape(ctx, lambda c: c.rectangle(1500, 360, 320, 540), hexc("#b7c0c9"), BG_OUT, None)
    for k in range(3):
        y = 400 + k * 160
        shape(ctx, lambda c, y=y: c.rectangle(1530, y, 260, 130), C["paper"], OUT * 0.6, None)
        if k == 0 and p.get("cat", 0.0) > 0.01:
            flat(ctx, lambda c: c.rectangle(1545, 470, 230, 45), hexc("#3b6bb0"))
            flat(ctx, lambda c: p_ellipse(c, 1650, 455, 55, 25), hexc("#e39a4a"))
            shape(ctx, lambda c: p_ellipse(c, 1705, 430, 22, 20), hexc("#e39a4a"), 3, None)
            for ex in (1695, 1712):
                shape(ctx, lambda c, ex=ex: p_poly(c, [(ex - 7, 418), (ex, 400), (ex + 7, 418)]), hexc("#e39a4a"), 3, None)
        else:
            for j in range(3):
                stroke(ctx, [(1550, y + 30 + j * 30), (1760, y + 30 + j * 30)], 6, color=hexc("#9aa3ab"))


# ================================================================================================ things and people

def pb_truck(ctx, t, p):
    """The tour truck (a big-wheeled tundra buggy), side view, origin = ground centre, about 1100 wide.
    p curtain (0..1 the near window's curtain shut), peek (0..1 the curtain opened a crack)."""
    shape(ctx, lambda c: p_rrect(c, -560, -560, 1120, 330, 30), C["truck"], OUT, (0.03, 0.12))
    shape(ctx, lambda c: c.rectangle(-580, -580, 1160, 40), C["truck_dk"], OUT, None)
    for k in range(5):
        x = -500 + k * 200
        shape(ctx, lambda c, x=x: p_rrect(c, x, -520, 160, 120, 14), hexc("#cfe6f5"), OUT * 0.7, None,
              a=0.35 if p.get("glass") else 1.0)
    cu = p.get("curtain", 0.0)
    if cu > 0.01:
        pk = p.get("peek", 0.0)
        w = 160 * ease(min(1.0, cu)) * (1 - 0.25 * pk)
        shape(ctx, lambda c: c.rectangle(-100, -520, w, 120), hexc("#b8352c"), OUT * 0.6, None)
    shape(ctx, lambda c: c.rectangle(380, -520, 130, 290), hexc("#2c5170"), OUT * 0.7, None)
    stroke(ctx, [(-560, -230), (560, -230)], 8)
    shape(ctx, lambda c: c.rectangle(-480, -230, 960, 60), hexc("#3a3a40"), OUT * 0.8, None)
    for x in (-360, 360):
        shape(ctx, lambda c, x=x: p_ellipse(c, x, -115, 120, 120), hexc("#2a2a2e"), OUT, (0.05, 0.1))
        shape(ctx, lambda c, x=x: p_ellipse(c, x, -115, 50, 50), C["steel"], OUT * 0.7, None)
    text(ctx, "TOURS", 0, -300, 60, "#ffd34d", 0)


def pb_stick(ctx, t, p):
    """Another stick figure in the same look as Meatball (ink limbs, a round head), feet at y = 0, about 900 tall at
    scale 1. p: head (colour), cap (colour or None), lanyard, parka (colour: a puffy jacket), arm ("down" | "hold" |
    "point" | "push" | "boots" | "lift"), shake (0..1 the head shakes no), walking/phase, mood."""
    ph = p.get("phase", 0.0)
    st = 50 * math.sin(ph) if p.get("walking") else 0.0
    hip = (0, -330)
    for s_, o in ((-1, st), (1, -st)):
        stroke(ctx, [hip, (s_ * 40 + o * 0.6, -170), (s_ * 55 + o, 0)], 22)
    top = (0, -640)
    stroke(ctx, [hip, top], 22)
    arm = p.get("arm", "down")
    targets = {"down": ((-110, -390), (110, -390)), "hold": ((-30, -470), (150, -470)), "point": ((-110, -390), (260, -600)),
               "push": ((170, -430), (190, -400)), "boots": ((150, -430), (190, -470)), "lift": ((140, -560), (180, -540))}
    for side, tg in zip((-1, 1), targets.get(arm, targets["down"])):
        el = ((top[0] + tg[0]) / 2 + side * 30, (top[1] + 30 + tg[1]) / 2 + 30)
        stroke(ctx, [(0, -610), el, tg], 20)
        flat(ctx, lambda c, tg=tg: p_ellipse(c, tg[0], tg[1], 18, 18), INK)
    if p.get("parka"):
        pc = hexc(p["parka"])
        shape(ctx, lambda c: p_rrect(c, -120, -660, 240, 360, 70), pc, OUT, (0.1, 0.05))
        for y in (-560, -460):
            stroke(ctx, [(-115, y), (115, y)], 5, color=darker(pc, 0.75))
    hx = 12 * math.sin(t * 14) * p.get("shake", 0.0)
    hc = (hx, -780)
    shape(ctx, lambda c: p_ellipse(c, hc[0], hc[1], 120, 125), hexc(p.get("head", "#e8b48a")), OUT, (0.08, 0.1))
    mood = p.get("mood", "calm")
    for s_ in (-1, 1):
        flat(ctx, lambda c, s_=s_: p_ellipse(c, hc[0] + s_ * 40 + 10, hc[1] - 10, 14, 17), INK)
    if mood == "frown":
        stroke(ctx, [(hc[0] - 20, hc[1] + 60), (hc[0] + 10, hc[1] + 48), (hc[0] + 40, hc[1] + 60)], 8, smooth=True)
    else:
        stroke(ctx, [(hc[0] - 25, hc[1] + 45), (hc[0] + 10, hc[1] + 62), (hc[0] + 45, hc[1] + 45)], 8, smooth=True)
    if p.get("cap"):
        cc = hexc(p["cap"])
        shape(ctx, lambda c: p_poly(c, [(hc[0] - 118, hc[1] - 30), (hc[0] - 100, hc[1] - 110), (hc[0] + 60, hc[1] - 120),
                                        (hc[0] + 118, hc[1] - 40)]), cc, OUT, None)
        shape(ctx, lambda c: p_rrect(c, hc[0] + 60, hc[1] - 52, 120, 26, 12), cc, OUT * 0.8, None)
    if p.get("lanyard"):
        stroke(ctx, [(-60, -650), (0, -520), (60, -650)], 6, color=C["red"])
        shape(ctx, lambda c: p_rrect(c, -40, -530, 80, 100, 8), (1, 1, 1), OUT * 0.6, None)
    if arm == "boots":
        for k, (bx, by_) in enumerate(((150, -430), (195, -480))):
            _boot(ctx, bx, by_ + 30, 0.9, 0.3 * k)


def _boot(ctx, x, y, s=1.0, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    shape(ctx, lambda c: p_poly(c, [(-35, -110), (25, -110), (25, -30), (85, -20), (90, 20), (-40, 20)]), hexc("#5a3a22"),
          OUT * 0.8, (0.05, 0.1))
    stroke(ctx, [(-35, -95), (25, -95)], 8, color=hexc("#c9b38a"))
    ctx.restore()


def pb_boot(ctx, t, p):
    _boot(ctx, 0, 0, 1.0, p.get("rot", 0.0))


def pb_mound(ctx, t, p):
    """Meatball's own snow hole: a snow mound with a dark tunnel mouth (front actor that hides his head)."""
    shape(ctx, lambda c: p_smooth(c, [(-330, 0), (-250, -170), (0, -240), (250, -170), (330, 0)]), C["snow"], OUT, (0.0, 0.15))
    if p.get("hole", 1.0):
        shape(ctx, lambda c: p_ellipse(c, -40, -60, 90, 70), hexc("#2c3e5c"), OUT * 0.8, None)


def pb_icehole(ctx, t, p):
    """Meatball's small fishing hole in the ice, seen from the side: an oval with dark water (origin = its centre)."""
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 130, 34), C["snow2"], OUT * 0.8, None)
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 90, 22), C["water_dk"], OUT * 0.6, None)


def pb_bucket(ctx, t, p):
    shape(ctx, lambda c: p_poly(c, [(-70, -150), (70, -150), (55, 0), (-55, 0)]), hexc("#3b7dd8"), OUT, (0.05, 0.15))
    stroke(ctx, [(-70, -150), (70, -150)], OUT)


def pb_rod(ctx, t, p):
    """A fishing rod from the origin (his hands) to a tip, a line down to the hook; p bend (0..1), catch (0..1 the
    boot comes up out of the hole at p hy below the tip)."""
    bd = p.get("bend", 0.0)
    tip = (260 - 60 * bd, -260 + 140 * bd)
    stroke(ctx, [(0, 0), (130, -150 + 40 * bd), tip], 10, smooth=True, color=hexc("#6b4a2f"))
    stroke(ctx, [(0, 0), (130, -150 + 40 * bd), tip], 3, smooth=True)
    hy = p.get("hy", 330)
    cu = ease(min(1.0, p.get("catch", 0.0)))
    end = (tip[0], tip[1] + hy * (1 - cu * 0.8))
    stroke(ctx, [tip, end], 2.5)
    if cu > 0.01:
        _boot(ctx, end[0] - 20, end[1] + 110, 0.9, 0.4)


def pb_menu(ctx, t, p):
    """The huge leather menu, open (p open 0..1): two pages, one line SEAL; p flip (0..1 turned upside down)."""
    u = ease(min(1.0, p.get("open", 1.0)))
    ctx.save()
    ctx.rotate(math.pi * ease(min(1.0, p.get("flip", 0.0))))
    w = 260 * u
    shape(ctx, lambda c: p_rrect(c, -w - 20, -190, 2 * w + 40, 380, 16), C["leather"], OUT, (0.03, 0.1))
    if u > 0.2:
        for x0 in (-w, 10):
            shape(ctx, lambda c, x0=x0: c.rectangle(x0, -165, w - 10, 330), C["paper"], OUT * 0.5, None)
        text(ctx, "SEAL", w * 0.5, -90, 70, "#3a2a1e", 0)
        stroke(ctx, [(0, -175), (0, 175)], 5)
    else:
        text(ctx, "MENU", 0, 0, 60, "#f2b72c", 0)
    ctx.restore()


def pb_review(ctx, t, p):
    """Meatball's review card: five stars (p stars filled, default 1), p text (one or two short lines split at |),
    p sign (scrawl under it, e.g. THE KNEES), p blank (no stars filled, no text), p on (pop in), p rot (degrees)."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    s = back_out(min(1.0, on))
    ctx.save()
    ctx.rotate(math.radians(p.get("rot", -4)))
    ctx.scale(s, s)
    shape(ctx, lambda c: p_rrect(c, -330, -190, 660, 380, 22), C["paper"], OUT, (0.02, 0.08))
    text(ctx, "MEATBALL'S REVIEW", 0, -140, 40, "#7c5232", 0)
    n = 0 if p.get("blank") else int(p.get("stars", 1))
    for k in range(5):
        x = -200 + k * 100
        pts = []
        for i in range(10):
            r = 42 if i % 2 == 0 else 18
            a = -math.pi / 2 + i * math.pi / 5
            pts.append((x + r * math.cos(a), -60 + r * math.sin(a)))
        shape(ctx, lambda c, pts=pts: p_poly(c, pts), C["gold"] if k < n else (1, 1, 1), OUT * 0.6, None)
    if not p.get("blank") and p.get("text"):
        rows = p["text"].split("|")
        for k, r in enumerate(rows):
            text(ctx, r, 0, 30 + k * 62 - (len(rows) - 1) * 10, 50 if len(r) < 22 else 40, "#1b1724", 0)
    if p.get("sign"):
        text(ctx, "- " + p["sign"], 150, 150, 34, "#c4560f", 0, rot=-4)
    ctx.restore()


def pb_reviews(ctx, t, p):
    """A fan (p mode fan, n cards) or a stack (mode stack, n cards) of one-star review cards; p top (text of the top)."""
    n = int(p.get("n", 4))
    fan = p.get("mode", "fan") == "fan"
    sp = ease(min(1.0, p.get("spread", 1.0)))
    for k in range(n):
        ctx.save()
        if fan:
            ang = (k - (n - 1) / 2) * 0.22 * sp
            ctx.translate(0, 300)
            ctx.rotate(ang)
            ctx.translate(0, -300)
        else:
            ctx.translate(k * 6 - n * 3, -k * 14 + n * 7)
            ctx.rotate(math.radians((k % 3 - 1) * 4))
        last = k == n - 1
        pb_review(ctx, t, {"stars": 1, "text": p.get("top", "") if last else "", "rot": 0, "on": 1.0})
        ctx.restore()


def pb_comment(ctx, t, p):
    """A comment box with five empty stars and a blinking cursor; p ask (text over it)."""
    shape(ctx, lambda c: p_rrect(c, -480, -140, 960, 280, 26), (1, 1, 1), OUT, None)
    for k in range(5):
        x = -340 + k * 100
        pts = [(x + (40 if i % 2 == 0 else 17) * math.cos(-math.pi / 2 + i * math.pi / 5),
                -40 + (40 if i % 2 == 0 else 17) * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(10)]
        shape(ctx, lambda c, pts=pts: p_poly(c, pts), (1, 1, 1), OUT * 0.6, None)
    stroke(ctx, [(-400, 60), (380, 60)], 4, color=hexc("#9aa3ab"))
    if math.sin(t * 6) > 0:
        stroke(ctx, [(-390, 20), (-390, 100)], 6)
    if p.get("ask"):
        text(ctx, p["ask"], 0, -210, 60, "#ffd34d", 7)


def pb_snowflake(ctx, t, p):
    for k in range(3):
        a = k * math.pi / 3
        stroke(ctx, [(-24 * math.cos(a), -24 * math.sin(a)), (24 * math.cos(a), 24 * math.sin(a))], 5, color=(1, 1, 1))


def pb_pages(ctx, t, p):
    """Calendar pages falling or flying (p n pages, p fall 0..1, p mode fall | fly, p nums: show 1..n numbers)."""
    n = int(p.get("n", 9))
    u = p.get("fall", 0.0)
    for k in range(n):
        uk = max(0.0, min(1.0, u * n - k))
        if uk <= 0:
            continue
        if p.get("mode", "fall") == "fly":
            x, y, r = -300 + 1600 * uk + k * 40, -200 + 60 * math.sin(k + uk * 5) - 150 * uk, uk * 6
        else:
            x, y, r = (k - n / 2) * 120, -260 + 520 * ease(uk), math.sin(k) * 0.5 * uk
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(r)
        shape(ctx, lambda c: c.rectangle(-60, -70, 120, 140), C["paper"], OUT * 0.6, None)
        flat(ctx, lambda c: c.rectangle(-60, -70, 120, 34), C["red"])
        if p.get("nums"):
            text(ctx, str(k + 1), 0, 18, 60, "#1b1724", 0)
        ctx.restore()


def pb_puff(ctx, t, p):
    """A noisemaker puff and bang in the air (p on 0..1)."""
    on = p.get("on", 0.0)
    if on <= 0.01:
        return
    u = ease(min(1.0, on))
    for k in range(6):
        a = k * math.pi / 3
        shape(ctx, lambda c, a=a: p_ellipse(c, 70 * u * math.cos(a), 70 * u * math.sin(a), 60 * u, 50 * u), (0.92, 0.92, 0.95),
              OUT * 0.6, None, a=max(0.0, 1.2 - on * 0.4))
    if p.get("text", "BANG!"):
        text(ctx, p.get("text", "BANG!"), 0, -150 * u, int(90 * u) + 10, "#ffd34d", 7)


def pb_pickup(ctx, t, p):
    """A staff pickup truck, side view facing right, origin = ground centre."""
    shape(ctx, lambda c: p_poly(c, [(-330, -90), (-330, -200), (60, -200), (130, -320), (300, -320), (360, -200), (380, -90)]),
          hexc("#e8e8e8"), OUT, (0.03, 0.1))
    shape(ctx, lambda c: p_poly(c, [(150, -300), (280, -300), (320, -210), (110, -210)]), hexc("#9fd0f0"), OUT * 0.6, None)
    flat(ctx, lambda c: c.rectangle(-320, -170, 360, 30), hexc("#2e6b45"))
    for x in (-210, 240):
        shape(ctx, lambda c, x=x: p_ellipse(c, x, -70, 70, 70), hexc("#2a2a2e"), OUT, None)
        shape(ctx, lambda c, x=x: p_ellipse(c, x, -70, 28, 28), C["steel"], OUT * 0.6, None)


def pb_cart(ctx, t, p):
    """A motel luggage cart, origin = ground centre."""
    shape(ctx, lambda c: c.rectangle(-260, -110, 520, 26), C["gold"], OUT * 0.8, None)
    for x in (-240, 240):
        stroke(ctx, [(x, -110), (x, -420)], 14, color=C["gold"])
        stroke(ctx, [(x, -110), (x, -420)], 3)
    stroke(ctx, [(-240, -420), (240, -420)], 14, color=C["gold"])
    for x in (-200, 200):
        shape(ctx, lambda c, x=x: p_ellipse(c, x, -40, 40, 40), hexc("#2a2a2e"), OUT * 0.7, None)


def pb_sandwich(ctx, t, p):
    shape(ctx, lambda c: p_poly(c, [(-80, 0), (80, 0), (0, -70)]), hexc("#e9c98a"), OUT * 0.7, None)
    stroke(ctx, [(-70, -8), (70, -8)], 10, color=hexc("#6fae5a"))


def pb_ring(ctx, t, p):
    """A child's swim ring floating (origin = water line)."""
    ctx.save()
    ctx.translate(0, 4 * math.sin(t * 2))
    ctx.scale(1, 0.4)
    ctx.set_line_width(46)
    for k in range(8):
        ctx.arc(0, 0, 70, k * math.pi / 4, (k + 1) * math.pi / 4)
        src(ctx, C["red"] if k % 2 else (1, 1, 1))
        ctx.stroke()
    ink(ctx, 5)
    p_ellipse(ctx, 0, 0, 94, 94)
    ctx.stroke()
    p_ellipse(ctx, 0, 0, 46, 46)
    ctx.stroke()
    ctx.restore()


def pb_waffles(ctx, t, p):
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 110, 24), (1, 1, 1), OUT * 0.7, None)
    for j in range(3):
        shape(ctx, lambda c, j=j: p_rrect(c, -75 + j * 5, -30 - j * 18, 150, 32, 7), C["gold"], OUT * 0.5, None)
        for g in range(4):
            stroke(ctx, [(-55 + j * 5 + g * 34, -28 - j * 18), (-55 + j * 5 + g * 34, -2 - j * 18)], 3, color=darker(C["gold"], 0.7))
    if p.get("syrup"):
        stroke(ctx, [(-40, -66), (10, -60), (30, -20), (25, 10)], 12, smooth=True, color=hexc("#8a4a12"))


def pb_glass(ctx, t, p):
    shape(ctx, lambda c: p_poly(c, [(-35, -110), (35, -110), (28, 0), (-28, 0)]), hexc("#d8eef8"), OUT * 0.7, None)
    flat(ctx, lambda c: p_poly(c, [(-31, -70), (31, -70), (28, -4), (-28, -4)]), hexc("#8fd0f0"))


def pb_bubble(ctx, t, p):
    """A thought bubble with a bear snoring in a cave (p on)."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    s = back_out(min(1.0, on))
    ctx.save()
    ctx.scale(s, s)
    shape(ctx, lambda c: p_blob(c, 0, 0, 420, 250, 0.09, seed=3), (1, 1, 1), OUT, None)
    for k, (x, y, r) in enumerate(((-300, 280, 40), (-380, 350, 24))):
        shape(ctx, lambda c, x=x, y=y, r=r: p_ellipse(c, x, y, r, r), (1, 1, 1), OUT * 0.8, None)
    shape(ctx, lambda c: p_smooth(c, [(-330, 150), (-280, -120), (0, -200), (280, -120), (330, 150)]), hexc("#7a6a5a"), OUT, None)
    flat(ctx, lambda c: p_smooth(c, [(-220, 150), (-180, -40), (0, -100), (180, -40), (220, 150)]), hexc("#2a2420"))
    ctx.save()
    ctx.translate(-20, 150)
    pb_bear(ctx, t, {"age": "adult", "pose": "curl", "shut": True})
    ctx.restore()
    text(ctx, "Z", 160, -60 - 10 * math.sin(t * 3), 70, "#1b1724", 0)
    text(ctx, "z", 220, -120 - 10 * math.sin(t * 3 + 1), 50, "#1b1724", 0)
    ctx.restore()


# ================================================================================================ boards (centred on 0, 0)

def _bar(ctx, x, y, w, h, frac, col, label=None, px=44):
    shape(ctx, lambda c: p_rrect(c, x, y, w, h, h / 2), hexc("#2a2638"), OUT * 0.6, None)
    if frac > 0.005:
        shape(ctx, lambda c: p_rrect(c, x, y, max(h, w * frac), h, h / 2), col, OUT * 0.6, None)
    if label:
        text(ctx, label, x - 20 - len(label) * px * 0.22, y + h / 2, px, "#ffffff", 0)


def pb_thermo(ctx, t, p):
    """The split thermometer: OUTSIDE (deep in the blue, no number) and THE DEN (just under 0 C). p g (0..1)."""
    g = ease(min(1.0, p.get("g", 1.0)))
    for k, (lab, lvl, col) in enumerate((("OUTSIDE", 0.12, "#3b7dd8"), ("THE DEN", 0.47, "#8fd0ff"))):
        x = -260 + k * 520
        shape(ctx, lambda c, x=x: p_rrect(c, x - 45, -280, 90, 520, 45), (1, 1, 1), OUT, None)
        shape(ctx, lambda c, x=x: p_ellipse(c, x, 270, 80, 80), hexc(col), OUT, None)
        hh = 480 * lvl * g + 20
        flat(ctx, lambda c, x=x, hh=hh: p_rrect(c, x - 25, 230 - hh, 50, hh + 20, 25), hexc(col))
        text(ctx, lab, x, -340, 56, "#ffffff", 0)
    y0 = 230 - 480 * 0.5
    stroke(ctx, [(160, y0), (360, y0)], 6, color=C["yel"])
    text(ctx, "0 C", 440, y0, 50, "#ffd34d", 0)


def pb_dial(ctx, t, p):
    """A survival dial: a half-circle gauge 0..100 with a needle at p v (eases), the value printed as ABOUT v%;
    p label (under it), p small (small print)."""
    v = p.get("v", 50.0)
    R = 300
    for k in range(100):
        a0 = math.pi + math.pi * k / 100
        ctx.save()
        ctx.set_line_width(60)
        r_ = 0.9 - 0.6 * (k / 100)
        ctx.set_source_rgb(0.9 * (1 - k / 100) + 0.25 * k / 100, 0.25 + 0.5 * k / 100, 0.25)
        ctx.arc(0, 120, R, a0, a0 + math.pi / 100 + 0.005)
        ctx.stroke()
        ctx.restore()
    ink(ctx, 6)
    ctx.arc(0, 120, R + 30, math.pi, 2 * math.pi)
    ctx.stroke()
    ctx.arc(0, 120, R - 30, math.pi, 2 * math.pi)
    ctx.stroke()
    a = math.pi + math.pi * v / 100
    stroke(ctx, [(0, 120), (0.92 * R * math.cos(a), 120 + 0.92 * R * math.sin(a))], 16, color=(1, 1, 1))
    stroke(ctx, [(0, 120), (0.92 * R * math.cos(a), 120 + 0.92 * R * math.sin(a))], 4)
    shape(ctx, lambda c: p_ellipse(c, 0, 120, 30, 30), (1, 1, 1), OUT, None)
    fin = p.get("final")
    if fin is None or abs(v - fin) < 0.6:   # the number is printed only where the needle lands: no passing values
        text(ctx, f"ABOUT {int(round(v if fin is None else fin))}%", 0, 230, 80, "#ffd34d", 7)
    if p.get("label"):
        text(ctx, p["label"], 0, 320, 48, "#ffffff", 0)
    if p.get("small"):
        text(ctx, p["small"], 0, 385, 34, "#b8b4c8", 0)


def pb_clockshare(ctx, t, p):
    """A clock face with a shaded share (p share 0..1 eases)."""
    sh = p.get("share", 0.0)
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 170, 170), (1, 1, 1), OUT, None)
    if sh > 0.005:
        ctx.move_to(0, 0)
        ctx.arc(0, 0, 160, -math.pi / 2, -math.pi / 2 + 2 * math.pi * sh)
        ctx.close_path()
        src(ctx, hexc("#8f99a6"))
        ctx.fill()
    for k in range(12):
        a = k * math.pi / 6
        stroke(ctx, [(150 * math.cos(a), 150 * math.sin(a)), (168 * math.cos(a), 168 * math.sin(a))], 5)
    if p.get("label"):
        text(ctx, p["label"], 0, 230, 44, "#ffffff", 0)


def pb_strip(ctx, t, p):
    """A calendar strip of p n boxes; p mark: bowl (an empty bowl in each), swim (a small swimming bear in the first
    p k), shade (the first p k shaded), drop (a scale needle dropping one notch per box); p lit (0..n boxes shown),
    p labels (list, one per box), p note (small print under)."""
    n = int(p.get("n", 8))
    lit = p.get("lit", n)
    w = min(170, 1400 / n)
    mark = p.get("mark", "")
    kk_ = p.get("k", 0)
    labs = p.get("labels")
    for i in range(n):
        u = max(0.0, min(1.0, (lit - i) * 2))
        if u <= 0:
            continue
        x = (i - (n - 1) / 2) * (w + 14)
        ctx.save()
        ctx.translate(x, 0)
        s = back_out(u)
        ctx.scale(s, s)
        shaded = mark == "shade" and i < kk_
        shape(ctx, lambda c: p_rrect(c, -w / 2, -w * 0.6, w, w * 1.2, 12), hexc("#8f99a6") if shaded else C["paper"], OUT * 0.6, None)
        flat(ctx, lambda c: p_rrect(c, -w / 2, -w * 0.6, w, w * 0.3, 10), C["red"])
        if labs:
            text(ctx, labs[i], 0, -w * 0.45, int(w * 0.24), "#ffffff", 0)
        if mark == "bowl":
            shape(ctx, lambda c: p_poly(c, [(-w * 0.3, w * 0.05), (w * 0.3, w * 0.05), (w * 0.2, w * 0.3), (-w * 0.2, w * 0.3)]),
                  hexc("#c9d3dc"), OUT * 0.5, None)
        if mark == "swim" and i < kk_:
            ctx.save()
            ctx.translate(0, w * 0.25)
            ctx.scale(w / 1100, w / 1100)
            pb_bear(ctx, t, {"age": "adult", "pose": "swim", "pull": 0.6})
            ctx.restore()
        ctx.restore()
    if p.get("note"):
        text(ctx, p["note"], 0, w * 0.6 + 60, 36, "#b8b4c8", 0)


def pb_candles(ctx, t, p):
    """A row of candles, numbered by fives, that stops at 25 (p lit 0..25)."""
    lit = p.get("lit", 25)
    for i in range(25):
        if i >= lit:
            break
        x = -720 + i * 60
        shape(ctx, lambda c, x=x: p_rrect(c, x - 16, -40, 32, 140, 8), hexc("#f6e7c0"), OUT * 0.5, None)
        shape(ctx, lambda c, x=x: p_ellipse(c, x, -62 + 3 * math.sin(t * 8 + i), 11, 20), C["gold"], 3, None)
        if (i + 1) % 5 == 0:
            text(ctx, str(i + 1), x, 150, 44, "#ffffff", 0)
    if lit >= 25:
        stroke(ctx, [(800, -120), (800, 130)], 10, color=C["red"])
        text(ctx, "25", 870, 0, 70, "#e5383b", 0)


def pb_years(ctx, t, p):
    """A row of 47 year boxes for the satellite record; the last 19 marked (p mark 0..1); label LOWEST 19."""
    m = p.get("mark", 0.0)
    for i in range(47):
        x = -760 + (i % 24) * 66
        y = -90 + (i // 24) * 110
        last = i >= 28
        on = last and m > (i - 28) / 19
        shape(ctx, lambda c, x=x, y=y: p_rrect(c, x - 26, y - 40, 52, 80, 8), hexc("#e5383b") if on else hexc("#3a3550"), OUT * 0.4, None)
    if m > 0.95:
        text(ctx, "LOWEST 19", 420, 160, 60, "#ffd34d", 7)
    text(ctx, "SEPTEMBER MINIMUMS, SATELLITE RECORD", 0, -200, 40, "#ffffff", 0)


def pb_line(ctx, t, p):
    """A schematic body-condition line with no scale: falls from 1995 to 2000, then (p rise 0..1) turns up to 2019;
    p grow (0..1 the falling part)."""
    g = ease(min(1.0, p.get("grow", 1.0)))
    r = ease(min(1.0, p.get("rise", 0.0)))
    stroke(ctx, [(-600, 230), (600, 230)], 6, color=(1, 1, 1))
    stroke(ctx, [(-600, 230), (-600, -230)], 6, color=(1, 1, 1))
    for x, lab in ((-560, "1995"), (-300, "2000"), (560, "2019")):
        text(ctx, lab, x, 280, 40, "#ffffff", 0)
    pts = [(-560, -120), (-300, -120 + 220 * g)] if g < 1 else [(-560, -120), (-300, 100)]
    if g < 1:
        pts = [(-560, -120), (-560 + 260 * g, -120 + 220 * g)]
    stroke(ctx, pts, 12, color=C["yel"])
    if r > 0.01:
        stroke(ctx, [(-300, 100), (-300 + 860 * r, 100 - 260 * r)], 12, color=C["green"])
    text(ctx, "BODY CONDITION (NO SCALE)", -220, -260, 36, "#b8b4c8", 0)


def pb_bars2(ctx, t, p):
    """Two horizontal bars with labels and values (p rows: [[label, value, max]], p g 0..1, p head, p small)."""
    g = ease(min(1.0, p.get("g", 1.0)))
    rows = p.get("rows", [])
    if p.get("head"):
        text(ctx, p["head"], 0, -170, 40, "#ffffff", 0)
    for k, (lab, v, mx) in enumerate(rows):
        y = -80 + k * 130
        _bar(ctx, -260, y, 760, 70, g * v / mx, C["yel"] if k == 0 else C["red"])
        text(ctx, lab, -460, y + 35, 52, "#ffffff", 0)
        text(ctx, f"{v}%", 300 + 760 * g * v / mx - 320, y + 35, 46, "#1b1724" if g * v / mx > 0.2 else "#ffffff", 0)
    if p.get("small"):
        text(ctx, p["small"], 0, 230, 32, "#b8b4c8", 0)


def pb_bands(ctx, t, p):
    """Two survival bands on a 0..100 axis: AGES 2 TO 4 AND ADULTS 77-92, OLD-AGE CLASS 37-62 (p g 0..1)."""
    g = ease(min(1.0, p.get("g", 1.0)))
    stroke(ctx, [(-600, 200), (700, 200)], 5, color=(1, 1, 1))
    for v in (0, 50, 100):
        x = -600 + 13 * v
        text(ctx, f"{v}%", x, 245, 36, "#ffffff", 0)
    for k, (lab, lo, hi, col) in enumerate((("AGES 2 TO 4 AND ADULTS: 77 TO 92% A YEAR", 77, 92, C["green"]),
                                            ("OLD-AGE CLASS: 37 TO 62% A YEAR", 37, 62, C["red"]))):
        y = -130 + k * 170
        x0, x1 = -600 + 13 * lo, -600 + 13 * (lo + (hi - lo) * g)
        shape(ctx, lambda c, x0=x0, x1=x1, y=y: p_rrect(c, x0, y, max(20, x1 - x0), 70, 20), col, OUT * 0.6, None)
        text(ctx, lab, 50, y - 30, 38, "#ffffff", 0)
    text(ctx, "NORTHERN BEAUFORT SEA, 1971 TO 2006, HUNTING DEATHS INCLUDED", 50, 310, 30, "#b8b4c8", 0)


def pb_sheet(ctx, t, p):
    """A page: p title, p rows (list of text rows), p ticks (0..n green ticks beside rows), p under (index of a row
    to underline), p marks (0..n rows marked with the same red mark), p small; p kind note (a field notebook with
    rings), clip (on a clipboard), report (a report page), brochure."""
    kind = p.get("kind", "report")
    rows = p.get("rows", [])
    w, h = p.get("w", 760), p.get("h", 640)
    if kind == "clip":
        shape(ctx, lambda c: p_rrect(c, -w / 2 - 30, -h / 2 - 40, w + 60, h + 80, 24), hexc("#b07a48"), OUT, (0.05, 0.2))
    shape(ctx, lambda c: p_rrect(c, -w / 2, -h / 2, w, h, 12), C["paper"] if kind != "note" else hexc("#f3e7c4"), OUT, (0.02, 0.08))
    if kind == "note":
        for k in range(8):
            shape(ctx, lambda c, k=k: p_ellipse(c, -w / 2 + 50 + k * (w - 100) / 7, -h / 2, 14, 22), C["steel"], OUT * 0.5, None)
    if kind == "clip":
        shape(ctx, lambda c: p_rrect(c, -90, -h / 2 - 60, 180, 70, 16), C["steel"], OUT, None)
    y = -h / 2 + 70
    if p.get("title"):
        text(ctx, p["title"], 0, y, p.get("title_px", 50), "#1b1724", 0)
        y += 80
    ticks, marks = p.get("ticks", 0.0), p.get("marks", 0.0)
    px = p.get("px", 40)
    for k, r in enumerate(rows):
        text(ctx, r, 0 if not (ticks or marks or p.get("left")) else 30, y, px, "#1b1724", 0)
        if p.get("under") == k:
            stroke(ctx, [(-w / 2 + 60, y + px * 0.6), (w / 2 - 60, y + px * 0.6)], 8, color=C["red"])
        if ticks > k:
            stroke(ctx, [(-w / 2 + 30, y), (-w / 2 + 48, y + 18), (-w / 2 + 78, y - 22)], 9, color=C["green"])
        if marks > k:
            flat(ctx, lambda c, y=y: p_ellipse(c, -w / 2 + 50, y, 16, 16), C["red"])
        y += px * 1.45
    if p.get("circle") is not None:
        cy_ = -h / 2 + 150 + p["circle"] * px * 1.45
        ctx.save()
        ctx.set_line_width(7)
        src(ctx, C["red"])
        p_ellipse(ctx, 0, cy_, w * 0.45, px * 0.9)
        ctx.stroke()
        ctx.restore()
    if p.get("small"):
        text(ctx, p["small"], 0, h / 2 - 40, 30, "#6b6478", 0)


def pb_sticky(ctx, t, p):
    """A sticky note with p text; p stamp (0..1 a NO SOURCE FOUND stamp), p cross (0..1 SEAL crossed out, HOLE
    written above), p small."""
    ctx.save()
    ctx.rotate(-0.05)
    shape(ctx, lambda c: c.rectangle(-260, -220, 520, 440), hexc("#ffe873"), OUT, (0.03, 0.1))
    text(ctx, p.get("text", "20 MILES?"), 0, -80, 90, "#1b1724", 0)
    cr = p.get("cross", 0.0)
    if cr > 0.01:
        text(ctx, "SEAL", 0, 70, 90, "#1b1724", 0)
        stroke(ctx, [(-120, 70), (-120 + 240 * min(1.0, cr * 2), 70)], 12, color=C["red"])
        if cr > 0.5:
            text(ctx, "HOLE", 0, 0, 70, "#c4202a", 0, rot=-6)
    if p.get("small"):
        text(ctx, p["small"], 0, 180, 30, "#6b6478", 0)
    ctx.restore()


def pb_board(ctx, t, p):
    """The menu board: SEAL, and under it ALMOST ALWAYS."""
    shape(ctx, lambda c: p_rrect(c, -380, -260, 760, 520, 20), hexc("#2a3a2e"), OUT * 1.2, None)
    shape(ctx, lambda c: p_rrect(c, -400, -280, 800, 560, 24), hexc("#7c5232"), 0, None, a=0)
    ctx.save()
    ink(ctx, 26)
    src(ctx, hexc("#7c5232"))
    p_rrect(ctx, -380, -260, 760, 520, 20)
    ctx.stroke()
    ctx.restore()
    text(ctx, "MENU", 0, -170, 60, "#ffffff", 0)
    ctx.save()
    ctx.translate(-140, 30)
    pb_seal(ctx, t, {"icon": True})
    ctx.restore()
    text(ctx, "SEAL", 110, 10, 110, "#ffffff", 0)
    text(ctx, "ALMOST ALWAYS", 0, 160, 50, "#ffd34d", 0)


def pb_counters(ctx, t, p):
    """Three plain counters (p n 0..3 shown): 73 ATTACKS, 20 DEATHS, 63 INJURIES (counting up as they appear)."""
    n = p.get("n", 3.0)
    for k, (v, lab) in enumerate(((73, "ATTACKS"), (20, "DEATHS"), (63, "INJURIES"))):
        u = max(0.0, min(1.0, (n - k)))
        if u <= 0:
            continue
        x = -500 + k * 500
        shape(ctx, lambda c, x=x: p_rrect(c, x - 200, -150, 400, 300, 24), hexc("#121628"), OUT * 0.7, None)
        text(ctx, str(v), x, -30, max(8, int(150 * back_out(u))), "#ffd34d", 0)
        text(ctx, lab, x, 100, 52, "#ffffff", 0)
    if p.get("small"):
        text(ctx, p["small"], 0, 230, 34, "#b8b4c8", 0)


def pb_timebar(ctx, t, p):
    """A timeline bar from p a to p b (labels at the ends), filling with p g (0..1); p tag (small print over the
    end), p mid (a label in the middle)."""
    g = ease(min(1.0, p.get("g", 1.0)))
    _bar(ctx, -600, -35, 1200, 70, g, C["yel"])
    text(ctx, str(p.get("a", "")), -600, 90, 50, "#ffffff", 0)
    text(ctx, str(p.get("b", "")), 600, 90, 50, "#ffffff", 0)
    if p.get("mid"):
        text(ctx, p["mid"], 0, -110, 60, "#ffffff", 0)
    if p.get("tag") and g > 0.95:
        text(ctx, p["tag"], 600, -110, 40, "#ffd34d", 0)


def pb_icons(ctx, t, p):
    """A grid of p n small bear icons (13 a row), p lit of them lit yellow (eases in order)."""
    n = int(p.get("n", 52))
    lit = p.get("lit", 0.0)
    per = int(p.get("per", 13))
    for i in range(n):
        x = (i % per - (per - 1) / 2) * 92
        y = (i // per) * 92 - ((n - 1) // per) * 46
        on = lit > i
        _bear_icon(ctx, x, y, 0.85, hexc("#ffd34d") if on else hexc("#4a4560"))


def _bear_icon(ctx, x, y, s, col):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    flat(ctx, lambda c: p_smooth(c, [(-40, 20), (-38, -12), (0, -16), (26, -24), (44, -16), (42, -4), (24, 0), (26, 20)]), col)
    flat(ctx, lambda c: p_ellipse(c, 24, -27, 6, 6), col)
    ctx.restore()


def pb_journal(ctx, t, p):
    """A journal cover: p year; a small swimming-bear line drawing."""
    shape(ctx, lambda c: p_rrect(c, -240, -320, 480, 640, 10), hexc("#2c5a80"), OUT, (0.03, 0.1))
    text(ctx, "JOURNAL", 0, -230, 60, "#ffffff", 0)
    text(ctx, str(p.get("year", 2011)), 0, -150, 60, "#ffd34d", 0)
    ctx.save()
    ctx.translate(0, 120)
    ctx.scale(0.42, 0.42)
    pb_bear(ctx, t, {"age": "adult", "pose": "swim", "pull": 0.5})
    ctx.restore()


def pb_coat(ctx, t, p):
    """The coat in cross-section: guard hairs, underfur, skin, fat; p labels (0..4 shown)."""
    n = p.get("labels", 4.0)
    flat(ctx, lambda c: c.rectangle(-560, 150, 760, 170), hexc("#f3dca0"))
    flat(ctx, lambda c: c.rectangle(-560, 110, 760, 40), hexc("#2a2830"))
    for k in range(70):
        x = -550 + k * 11
        stroke(ctx, [(x, 110), (x + 6, 60 + 8 * math.sin(k)), (x, 20)], 5, smooth=True, color=hexc("#e9e2cf"))
    for k in range(26):
        x = -545 + k * 29
        stroke(ctx, [(x, 110), (x + 20, -90), (x + 40, -230 + 10 * math.sin(k * 1.7))], 7, smooth=True, color=hexc("#fbf7ea"))
        stroke(ctx, [(x, 110), (x + 20, -90), (x + 40, -230 + 10 * math.sin(k * 1.7))], 2, smooth=True)
    ctx.save()
    ink(ctx, BG_OUT)
    ctx.rectangle(-560, -260, 760, 580)
    ctx.stroke()
    ctx.restore()
    for k, (lab, y) in enumerate((("GUARD HAIRS", -170), ("UNDERFUR", 60), ("SKIN", 130), ("FAT", 235))):
        if n > k:
            stroke(ctx, [(210, y), (300, y)], 6, color=C["yel"])
            text(ctx, lab, 300 + len(lab) * 15, y, 54, "#ffd34d", 0)


def pb_skin(ctx, t, p):
    """Close on the coat: pale hairs, a few parted (p part 0..1) to show the black skin under them. No light rays."""
    u = ease(min(1.0, p.get("part", 0.0)))
    flat(ctx, lambda c: c.rectangle(-700, -330, 1400, 660), hexc("#ece4cc"))
    flat(ctx, lambda c: p_ellipse(c, 0, 60, 60 + 220 * u, 40 + 120 * u), hexc("#1e1c22"))
    rnd = random.Random(6)
    for k in range(120):
        x = rnd.uniform(-680, 680)
        y = rnd.uniform(-300, 300)
        dx = x / max(1.0, abs(x)) * (130 * u if abs(x) < 360 and abs(y) < 200 else 0)
        stroke(ctx, [(x, y + 60), (x + dx * 0.6 + 10, y - 40), (x + dx + 20, y - 140)], 9, smooth=True, color=hexc("#fffbea"))
        stroke(ctx, [(x, y + 60), (x + dx * 0.6 + 10, y - 40), (x + dx + 20, y - 140)], 2, smooth=True, color=hexc("#b9ae90"))


def pb_arrow(ctx, t, p):
    """A yellow arrow from (0, 0) to p (x, y); p on."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    x, y = p.get("x", 200) * ease(min(1.0, on)), p.get("y", 0) * ease(min(1.0, on))
    stroke(ctx, [(0, 0), (x, y)], 16, color=C["yel"])
    a = math.atan2(y, x)
    stroke(ctx, [(x - 50 * math.cos(a - 0.5), y - 50 * math.sin(a - 0.5)), (x, y), (x - 50 * math.cos(a + 0.5), y - 50 * math.sin(a + 0.5))],
           16, color=C["yel"])


def pb_label(ctx, t, p):
    """Plain text (p text, px, color), optional pill (p bg); p on."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    s = back_out(min(1.0, on))
    ctx.save()
    ctx.scale(s, s)
    if p.get("bg"):
        w, h = text(ctx, p["text"], 0, 0, p.get("px", 50), p.get("color", "#ffffff"), None, 0.0)
        shape(ctx, lambda c: p_rrect(c, -w / 2 - 22, -h / 2 - 8, w + 44, h + 16, (h + 16) / 2), hexc(p["bg"]), OUT * 0.5, None, a=0.92)
    text(ctx, p["text"], 0, 0, p.get("px", 50), p.get("color", "#ffffff"), p.get("sw", 0), rot=p.get("rot", 0.0))
    ctx.restore()


def pb_pill(ctx, t, p):
    """The corner pill (screen space, top right): p text; p on."""
    on = p.get("on", 0.0)
    if on <= 0.01:
        return
    ctx.identity_matrix()
    import drawn_keepkill as kk
    im = kk.text_img(p["text"], 46, "#1b1724", 0)
    w = im[0].get_width()
    x = 1920 - 40 - w - 50 + 500 * (1 - ease(min(1.0, on)))
    kk.rrect(ctx, x, 150, w + 50, 80, 40)
    kk.fill(ctx, "#ffd34d", 0.96, 4)
    kk.blit(ctx, im, x + (w + 50) / 2, 190)


def pb_tint(ctx, t, p):
    """A screen-wide grade (front actor): p mode dark | dusk | blue, p a."""
    a = p.get("a", 0.0)
    if a <= 0.01:
        return
    ctx.identity_matrix()
    col = {"dark": (0.02, 0.03, 0.08), "dusk": (0.2, 0.1, 0.35), "blue": (0.1, 0.3, 0.6)}[p.get("mode", "dark")]
    ctx.rectangle(0, 0, 1920, 1080)
    ctx.set_source_rgba(*col, a)
    ctx.fill()


# ================================================================================================ the Arctic map

_LAND = {   # name: (angle from, angle to, inner radius share, outer) - schematic, seen from above the Pole
    "RUSSIA": (-148, 24, 0.86, 1.5), "UNITED STATES": (162, 207, 0.84, 1.5), "CANADA": (106, 162, 0.8, 1.5),
    "GREENLAND": (68, 100, 0.6, 1.18), "NORWAY": (32, 50, 0.92, 1.5)}
_DOTS = {"ALASKA'S NORTH SLOPE": (0.86, 178), "ALASKAN BEAUFORT SEA": (0.74, 170), "SOUTHERN BEAUFORT SEA": (0.72, 160),
         "NORTHERN BEAUFORT SEA": (0.58, 148), "CHUKCHI SEA": (0.72, 195), "HUDSON BAY": (1.08, 118),
         "SVALBARD": (0.62, 48), "BEAUFORT SEA": (0.7, 162)}


def pb_map(ctx, t, p):
    """The Arctic seen from above the Pole (schematic). p: dots (list of names lit; p lit 0..1), countries (0..1
    labels of the five countries), bears (0..1 small bear icons spread round the Arctic), route (0..1 a schematic
    swim-then-walk line, not the real track), q (0..1 question marks on two places), ice (0..1 Hudson Bay frozen),
    hudson_bears (0..1 icons step ashore), R (radius, default 330), pulse (the lit dots pulse)."""
    R = p.get("R", 330)
    shape(ctx, lambda c: p_ellipse(c, 0, 0, R * 1.5, R * 1.5), hexc("#3c6c9c"), OUT * 0.7, None)
    cty = p.get("countries", 0.0)
    for name, (a0, a1, ri, ro) in _LAND.items():
        pts = []
        rnd = random.Random(len(name))
        n = 18
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            r = R * (ri + rnd.uniform(-0.04, 0.04))
            pts.append((r * math.cos(a), r * math.sin(a)))
        for i in range(n, -1, -1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            pts.append((R * ro * math.cos(a), R * ro * math.sin(a)))
        ctx.save()
        p_ellipse(ctx, 0, 0, R * 1.5 - 4, R * 1.5 - 4)
        ctx.clip()
        shape(ctx, lambda c, pts=pts: p_poly(c, pts), hexc("#d9cfae"), OUT * (0.5 + 0.5 * cty), None)
        ctx.restore()
    # Hudson Bay cut into Canada; Svalbard island
    flat(ctx, lambda c: p_blob(c, R * 1.12 * math.cos(math.radians(118)), R * 1.12 * math.sin(math.radians(118)), 60, 75, 0.15, seed=2),
         hexc("#3c6c9c"))
    ice = p.get("ice", 0.0)
    if ice > 0.01:
        flat(ctx, lambda c: p_blob(c, R * 1.12 * math.cos(math.radians(118)), R * 1.12 * math.sin(math.radians(118)), 55 * ice, 68 * ice, 0.2,
                                   seed=4), (1, 1, 1), a=0.9)
    shape(ctx, lambda c: p_blob(c, R * 0.6 * math.cos(math.radians(45)), R * 0.6 * math.sin(math.radians(45)), 34, 26, 0.2, seed=1),
          hexc("#d9cfae"), OUT * 0.5, None)
    flat(ctx, lambda c: p_ellipse(c, 0, 0, R * 0.55, R * 0.55), (1, 1, 1), a=0.25)   # the sea ice round the Pole
    if cty > 0.01:
        for name, (a0, a1, ri, ro) in _LAND.items():
            am = math.radians((a0 + a1) / 2)
            rr = R * (1.22 if name != "GREENLAND" else 0.9)
            text(ctx, name, rr * math.cos(am), rr * math.sin(am), 40, "#1b1724", 0, cty)
    bears = p.get("bears", 0.0)
    if bears > 0.01:
        rnd = random.Random(9)
        for i in range(int(90 * bears)):
            a = rnd.uniform(0, 2 * math.pi)
            r = R * rnd.uniform(0.62, 1.0)
            _bear_icon(ctx, r * math.cos(a), r * math.sin(a), 0.42, (1, 1, 1))
    rt = p.get("route", 0.0)
    if rt > 0.01:
        sx, sy = R * 0.74 * math.cos(math.radians(165)), R * 0.74 * math.sin(math.radians(165))
        pts = [(sx, sy)]
        for k in range(1, 30):
            u = k / 29 * rt
            pts.append((sx + 330 * u, sy - 180 * u + 30 * math.sin(u * 9)))
        ctx.save()
        ctx.set_dash([20, 14])
        stroke(ctx, pts, 8, smooth=True, color=C["yel"])
        ctx.restore()
    lit = p.get("lit", 1.0)
    for name in p.get("dots", []):
        rr, aa = _DOTS[name]
        x, y = R * rr * math.cos(math.radians(aa)), R * rr * math.sin(math.radians(aa))
        pu = 1 + 0.25 * math.sin(t * 6) if p.get("pulse", True) else 1
        shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 18 * pu * lit, 18 * pu * lit), C["red"], OUT * 0.6, None)
        if lit > 0.5:
            lx = x + (190 if x > -60 else -10)
            text(ctx, name, x, y - 52, 36, "#ffffff", 6)
    q = p.get("q", 0.0)
    if q > 0.01:
        for name in ("SOUTHERN BEAUFORT SEA", "SVALBARD"):
            rr, aa = _DOTS[name]
            text(ctx, "?", R * rr * math.cos(math.radians(aa)), R * rr * math.sin(math.radians(aa)) - 70, max(8, int(110 * q)), "#ffd34d", 7)
    hb = p.get("hudson_bears", 0.0)
    if hb > 0.01:
        cx, cy = R * 1.12 * math.cos(math.radians(118)), R * 1.12 * math.sin(math.radians(118))
        for k in range(4):
            _bear_icon(ctx, cx + 80 + k * 30 * hb, cy + 40 + k * 22, 0.5, (1, 1, 1))


# ================================================================================================ Meatball in his parka

def parka(ctx, j, U, k, st, hood=0.0):
    """The orange parka over Meatball's stick body (j = mascot.body joints, U = rig -> screen): a puffy jacket from
    the shoulders to the hips, sleeves over both arms, a fur-rimmed hood round the head (hood 0..1 drops it over his
    eyes). Drawn after the rig, so it sits on top."""
    import mascot
    pc, pd = C["parka"], C["parka_dk"]
    sh, hip = U(j["sh"]), U(j["hip"])
    for side, key in ((-1, "l"), (1, "r")):
        el, wr, _ = mascot.arm_points(j, side, st[key])
        limb(ctx, [sh, U(el), U(wr)], 58 * k, pc, OUT * 0.7 * k)
    w = 150 * k
    shape(ctx, lambda c: p_smooth(c, [(sh[0] - w * 0.75, sh[1] - 10 * k), (sh[0] + w * 0.75, sh[1] - 10 * k),
                                      (hip[0] + w * 0.85, hip[1] + 30 * k), (hip[0] - w * 0.85, hip[1] + 30 * k)]), pc, OUT * k, (0.1, 0.05))
    stroke(ctx, [(sh[0], sh[1]), (hip[0], hip[1] + 30 * k)], 5 * k, color=pd)
    for u in (0.35, 0.7):
        stroke(ctx, [(sh[0] + (hip[0] - sh[0]) * u - w * 0.8, sh[1] + (hip[1] - sh[1]) * u),
                     (sh[0] + (hip[0] - sh[0]) * u + w * 0.8, sh[1] + (hip[1] - sh[1]) * u)], 5 * k, color=pd)
    hx, hy = U(j["head"])
    r = 150 * k
    if hood > 0.01:
        drop = ease(min(1.0, hood))
        shape(ctx, lambda c: p_smooth(c, [(hx - r * 1.12, hy - r * 0.3 + r * 0.9 * drop), (hx - r * 0.9, hy - r * 1.1), (hx, hy - r * 1.25),
                                          (hx + r * 0.9, hy - r * 1.1), (hx + r * 1.12, hy - r * 0.3 + r * 0.9 * drop),
                                          (hx, hy - r * 0.1 + r * 1.05 * drop)]), pc, OUT * k, (0.05, 0.1))
        stroke(ctx, [(hx - r * 1.05, hy - r * 0.25 + r * 0.9 * drop), (hx, hy - r * 0.05 + r * 1.05 * drop),
                     (hx + r * 1.05, hy - r * 0.25 + r * 0.9 * drop)], 30 * k, smooth=True, color=hexc("#efe6d2"))
    else:
        ctx.save()
        ctx.set_line_width(46 * k)
        src(ctx, pc)
        ctx.arc(hx, hy, r * 1.08, math.radians(150), math.radians(390))
        ctx.stroke()
        ctx.set_line_width(20 * k)
        src(ctx, hexc("#efe6d2"))
        ctx.arc(hx, hy, r * 0.98, math.radians(155), math.radians(385))
        ctx.stroke()
        ink(ctx, OUT * 0.7 * k)
        ctx.arc(hx, hy, r * 1.08 + 23 * k, math.radians(150), math.radians(390))
        ctx.stroke()
        ctx.restore()
    cam = st.get("camera", True)
    if cam:
        stroke(ctx, [(sh[0] - w * 0.6, sh[1]), (hip[0] + w * 0.4, hip[1] - 60 * k)], 5 * k)
        shape(ctx, lambda c: p_rrect(c, hip[0] + w * 0.2, hip[1] - 110 * k, 90 * k, 60 * k, 10 * k), hexc("#2a2a2e"), OUT * 0.5 * k, None)
        shape(ctx, lambda c: p_ellipse(c, hip[0] + w * 0.2 + 45 * k, hip[1] - 80 * k, 18 * k, 18 * k), C["steel"], OUT * 0.4 * k, None)


def coats(ctx, j, U, k):
    """Six coats: a ball of layers round his body, arms sticking out half way."""
    hip, sh = U(j["hip"]), U(j["sh"])
    cx, cy = (hip[0] + sh[0]) / 2, (hip[1] + sh[1]) / 2 + 10 * k
    for i, col in enumerate(("#3b7dd8", "#2e6b45", "#b8352c", "#d9b44a", "#6b3b22", "#f2711c")):
        r = (260 - i * 22) * k
        shape(ctx, lambda c, r=r: p_ellipse(c, cx, cy, r, r * 0.95), hexc(col), OUT * k, (0.06, 0.08))
    for s_ in (-1, 1):
        limb(ctx, [(cx + s_ * 200 * k, cy - 40 * k), (cx + s_ * 330 * k, cy - 120 * k)], 70 * k, hexc("#f2711c"), OUT * 0.7 * k)



def pb_route(ctx, t, p):
    """A schematic dashed route line (not the real track) from (0, 0) along p pts, growing with p g (0..1)."""
    pts = p.get("pts", [[0, 0], [400, -80], [800, 20], [1200, -60]])
    g = ease(min(1.0, p.get("g", 1.0)))
    seg = []
    n = len(pts) - 1
    for k in range(n):
        u = max(0.0, min(1.0, g * n - k))
        if u <= 0:
            break
        a, b = pts[k], pts[k + 1]
        seg.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u))
    if seg:
        ctx.save()
        ctx.set_dash([26, 18])
        stroke(ctx, [tuple(pts[0])] + seg, 12, color=C["yel"])
        ctx.restore()
    if p.get("note"):
        text(ctx, p["note"], pts[-1][0] / 2, -120, 34, "#ffffff", 5)


def pb_wallclock(ctx, t, p):
    """A wall clock; the hands show p mn minutes after 6:00 (eases with sets, so it can spin)."""
    mn = p.get("mn", 0.0)
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 120, 120), (0.98, 0.97, 0.93), OUT, (0.04, 0.15))
    for k in range(12):
        a_ = k * math.pi / 6
        stroke(ctx, [(95 * math.cos(a_), 95 * math.sin(a_)), (108 * math.cos(a_), 108 * math.sin(a_))], 5)
    hr_ = 6 + mn / 60
    for ang, ln, lw in ((hr_ / 12 * 2 * math.pi, 60, 10), (mn / 60 * 2 * math.pi, 90, 6)):
        stroke(ctx, [(0, 0), (ln * math.sin(ang), -ln * math.cos(ang))], lw)


def pb_ledger(ctx, t, p):
    """A ledger page with two columns, RAW and SWEET."""
    shape(ctx, lambda c: p_rrect(c, -380, -300, 760, 600, 12), C["paper"], OUT, (0.02, 0.08))
    stroke(ctx, [(0, -230), (0, 270)], 6)
    stroke(ctx, [(-340, -190), (340, -190)], 6)
    text(ctx, "RAW", -190, -240, 60, "#e5383b", 0)
    text(ctx, "SWEET", 190, -240, 60, "#2e8b3f", 0)
    for k in range(7):
        stroke(ctx, [(-340, -130 + k * 60), (340, -130 + k * 60)], 3, color=hexc("#c9c2ad"))


def pb_dropbar(ctx, t, p):
    """One bar for bear numbers that drops (p g 0..1) to between 50 and 75% of where it was: solid to 50%, a hatched
    band from 50 to 75% (the range), the old height as a dashed outline."""
    g = ease(min(1.0, p.get("g", 1.0)))
    hgt = 520
    ctx.save()
    ctx.set_dash([18, 12])
    ink(ctx, 5)
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(-110, -hgt, 220, hgt)
    ctx.stroke()
    ctx.restore()
    lo = hgt * (1 - 0.5 * g)
    hi = hgt * (1 - 0.25 * g)
    shape(ctx, lambda c: c.rectangle(-110, -lo, 220, lo), C["yel"], OUT * 0.6, None)
    if g > 0.05:
        flat(ctx, lambda c: c.rectangle(-110, -hi, 220, hi - lo), C["yel"], a=0.45)
        for k in range(5):
            stroke(ctx, [(-110, -lo - k * 28), (110, -lo - k * 28 - 40)], 4, color=C["yel"], a=0.8)
    if g > 0.9:
        text(ctx, "DOWN 25 TO 50%", 0, -hgt - 60, 50, "#ffd34d", 0)
    text(ctx, "BEAR NUMBERS", 0, 60, 44, "#ffffff", 0)


def pb_divider(ctx, t, p):
    """A vertical split-screen line (screen space) at p x."""
    ctx.identity_matrix()
    stroke(ctx, [(p.get("x", 960), 0), (p.get("x", 960), 1080)], 14, color=(1, 1, 1))
    stroke(ctx, [(p.get("x", 960), 0), (p.get("x", 960), 1080)], 4)


def pb_palm(ctx, t, p):
    """A round close-up inset of Meatball's hand covered in tiny writing; p turn (0..1 shows the back of the hand),
    p up (0..1 the view slides up the wrist, more writing)."""
    r = 300
    ctx.save()
    p_ellipse(ctx, 0, 0, r, r)
    ctx.clip()
    flat(ctx, lambda c: c.rectangle(-r, -r, 2 * r, 2 * r), hexc("#cfe6f5"))
    up = ease(min(1.0, p.get("up", 0.0)))
    ctx.translate(0, 260 * up)
    col = hexc("#965a3a") if p.get("turn", 0.0) < 0.5 else hexc("#7a4428")
    shape(ctx, lambda c: p_rrect(c, -150, -120, 300, 280, 90), col, OUT, (0.05, 0.1))
    for k in range(4):
        shape(ctx, lambda c, k=k: p_rrect(c, -140 + k * 72, -300, 60, 210, 30), col, OUT, None)
    shape(ctx, lambda c: p_rrect(c, -100, 140, 200, 500, 60), col, OUT, None)
    rnd = random.Random(int(p.get("turn", 0.0) > 0.5))
    for k in range(20):
        y = -260 + k * 38
        x0 = rnd.uniform(-130, -60)
        pts = [(x0 + j * 14, y + 5 * math.sin(j * 1.7 + k)) for j in range(int(rnd.uniform(8, 16)))]
        stroke(ctx, pts, 4, color=(1, 1, 1), a=0.9)
    ctx.restore()
    ink(ctx, OUT * 1.4)
    p_ellipse(ctx, 0, 0, r, r)
    ctx.stroke()


def pb_water(ctx, t, p):
    """A see-through water block (front actor) from (0, 0) w by h, with a wavy top: hides what is under the water."""
    w, h = p.get("w", 1400), p.get("h", 300)
    ctx.rectangle(0, 0, w, h)
    src(ctx, hexc(p.get("col", "#3f9fcf")), p.get("a", 0.6))
    ctx.fill()
    pts = [(x, 5 * math.sin(x / 50 + t * 3)) for x in range(0, int(w) + 10, 25)]
    stroke(ctx, pts, 6, smooth=True, color=(1, 1, 1), a=0.8)


def pb_fanbubble(ctx, t, p):
    """A thought bubble with a small desk fan in it (p on)."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    s = back_out(min(1.0, on))
    ctx.save()
    ctx.scale(s, s)
    shape(ctx, lambda c: p_blob(c, 0, 0, 260, 180, 0.09, seed=5), (1, 1, 1), OUT, None)
    for x, y, r in ((-200, 200, 30), (-250, 260, 18)):
        shape(ctx, lambda c, x=x, y=y, r=r: p_ellipse(c, x, y, r, r), (1, 1, 1), OUT * 0.8, None)
    stroke(ctx, [(0, 110), (0, 30)], 10)
    shape(ctx, lambda c: p_rrect(c, -60, 100, 120, 30, 10), hexc("#9aa3ab"), OUT * 0.6, None)
    shape(ctx, lambda c: p_ellipse(c, 0, -20, 70, 70), hexc("#dfe5ea"), OUT * 0.8, None)
    for k in range(3):
        ang = t * 18 + k * 2.1
        shape(ctx, lambda c, ang=ang: p_ellipse(c, 32 * math.cos(ang), -20 + 32 * math.sin(ang), 30, 13, ang), hexc("#8fb8d8"), 3, None)
    text(ctx, "MOTEL ROOM", 0, -130, 40, "#1b1724", 0)
    ctx.restore()


def pb_cards3(ctx, t, p):
    """Three case cards (p n 0..3 shown) under the date JANUARY TO APRIL 2004; silhouettes only."""
    n = p.get("n", 3.0)
    text(ctx, "JANUARY TO APRIL 2004", 0, -230, 50, "#ffffff", 0)
    for k in range(3):
        u = max(0.0, min(1.0, (n - k) * 2))
        if u <= 0:
            continue
        x = (k - 1) * 260
        ctx.save()
        ctx.translate(x, 0)
        ctx.rotate((k - 1) * 0.05)
        sc = back_out(u)
        ctx.scale(sc, sc)
        shape(ctx, lambda c: p_rrect(c, -110, -150, 220, 300, 12), C["paper"], OUT, None)
        text(ctx, f"CASE {k + 1}", 0, -100, 40, "#1b1724", 0)
        ctx.save()
        ctx.translate(-5, 90)
        ctx.scale(0.25, 0.25)
        pb_bear(ctx, t, {"age": "adult", "sil": 1.0})
        ctx.restore()
        ctx.restore()

ACTORS = {"pb_bear": pb_bear, "pb_seal": pb_seal, "pb_bird": pb_bird, "pb_truck": pb_truck, "pb_stick": pb_stick,
          "pb_boot": pb_boot, "pb_mound": pb_mound, "pb_icehole": pb_icehole, "pb_bucket": pb_bucket, "pb_rod": pb_rod,
          "pb_menu": pb_menu, "pb_review": pb_review, "pb_reviews": pb_reviews, "pb_comment": pb_comment,
          "pb_snowflake": pb_snowflake, "pb_pages": pb_pages, "pb_puff": pb_puff, "pb_pickup": pb_pickup, "pb_cart": pb_cart,
          "pb_sandwich": pb_sandwich, "pb_ring": pb_ring, "pb_waffles": pb_waffles, "pb_glass": pb_glass,
          "pb_bubble": pb_bubble, "pb_thermo": pb_thermo, "pb_dial": pb_dial, "pb_clockshare": pb_clockshare,
          "pb_strip": pb_strip, "pb_candles": pb_candles, "pb_years": pb_years, "pb_line": pb_line, "pb_bars2": pb_bars2,
          "pb_bands": pb_bands, "pb_sheet": pb_sheet, "pb_sticky": pb_sticky, "pb_board": pb_board,
          "pb_counters": pb_counters, "pb_timebar": pb_timebar, "pb_icons": pb_icons, "pb_journal": pb_journal,
          "pb_coat": pb_coat, "pb_skin": pb_skin, "pb_arrow": pb_arrow, "pb_label": pb_label, "pb_pill": pb_pill,
          "pb_tint": pb_tint, "pb_map": pb_map, "pb_route": pb_route, "pb_wallclock": pb_wallclock,
          "pb_ledger": pb_ledger, "pb_dropbar": pb_dropbar, "pb_divider": pb_divider, "pb_palm": pb_palm, "pb_water": pb_water,
          "pb_fanbubble": pb_fanbubble, "pb_cards3": pb_cards3}
SCENES = {"pb_den": pb_den, "pb_slope": pb_slope, "pb_ice": pb_ice, "pb_icecut": pb_icecut, "pb_shore": pb_shore,
          "pb_town": pb_town, "pb_facility": pb_facility, "pb_motel": pb_motel, "pb_desk": pb_desk}
