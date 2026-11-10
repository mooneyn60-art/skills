"""Pictures for the Christmas-tree long-form (tools/drawn_treecheck.py), in the locked drawn_kit look (flat fills,
one cel shade, thick ink outlines, cartoon eyes). Same conventions as tools/drawn_ds_art.py: an actor draws at its
origin in local units (y up is negative), scaled by its "s"; a scene draws in world units.

Plants:     tc_xtree (decorated Christmas tree: star, lights, garland, baubles, gifts; p: lit, deco, dry, qmarks,
            zs, gifts, glow, sway), tc_twig (fir twig close-up, horizontal, origin = top of the twig where an egg
            case sits), tc_wild (spruce | pine in snow), tc_farmtree (a sheared cone tree), tc_shrub (garden
            evergreen; p: snow, spring), tc_tree_end (a cut tree lying on its side, seen from the cut end),
            tc_tree_lying (a cut tree lying sideways, side view), tc_rootball (balled-and-burlapped tree)
Creatures:  tc_mantis (triangular head turned to camera, big eyes, long neck, raised spiked forelegs; p: strike,
            lay, nymph, col), tc_nymph, tc_ooth (egg case: chinese | carolina; p: quiver, crack, xray, split, grow),
            tc_aphid (giant conifer aphid, side view or top view, SIX legs; p: top, count, winged, yawn, flex,
            small), tc_tick_top (EIGHT legs, top view; p: count), tc_barkbeetle, tc_mite (predatory mite eating an
            egg; p: eat), tc_springtail, tc_barklouse, tc_spiderlings, tc_crawlers (scale crawlers walking),
            tc_slf_eggs (spotted lanternfly egg mass: grey cracked mud-like smear), tc_slf_nymphs, tc_adelgid
            (white cottony tufts), tc_nest, tc_dog, tc_specks (generic dust specks), tc_fall (specks falling)
Props:      tc_prop by p["kind"] (see PROPS), tc_marsh (toasted marshmallow on a stick), tc_counter (big rolling
            number), tc_map (NORWAY | NETHERLANDS | USA, plain shapes, a pin), tc_string (red string), tc_note
            (pinned card), tc_qm (question mark), tc_zz (sleep Z's), tc_race (two racing bars), tc_strip (2 of 9
            progress), tc_car (car with a tree on the roof), tc_shaker (mechanical tree shaker), tc_ship
Scenes:     tc_living (living room at night with a window, fireplace and stockings), tc_bokeh (warm out-of-focus
            Christmas lights, for close-ups), tc_lot (tree lot at dusk), tc_snowwood (wild snowy forest),
            tc_farm (tree farm rows), tc_yard (front yard: winter, or spring with p["spring"]), tc_cork
            (corkboard), tc_trunk (bark close-up), tc_road (road with a county line), tc_curb (street curb)
"""
import math
import random

import cairo

from drawn_kit import (BG_OUT, INK, OUT, PAL, back_out, darker, ease, eyes, flat, hexc, lighter, limb, mouth,
                       p_blob, p_ellipse, p_poly, p_rrect, p_smooth, shape, starburst, stroke)
from drawn_ds_art import text, house_sp_small

C = {k: hexc(v) for k, v in {
    "fir": "#2f8050", "fir_dk": "#22603b", "fir_lt": "#4fa86a", "dry": "#7f8a3c", "trunk": "#7a5233",
    "trunk_dk": "#5a3a22", "cut": "#e2c08a", "ring": "#c49a5e", "stand": "#c0392b", "gold": "#f2c14e",
    "snow": "#f4f7fb", "snow_dk": "#d5dfea", "case": "#d8b47e", "case_dk": "#b58b55", "toast": "#9a6a34",
    "mantis": "#8cbf4f", "mantis_tan": "#c9a86a", "carolina": "#9c9a7c", "nymph": "#efe4c0",
    "aphid": "#3d302b", "aphid_lt": "#6d5d55", "tick": "#7a3b26", "tick_dk": "#3a1a12", "beetle": "#5b3a24",
    "mite": "#e0873a", "mud": "#8e8a82", "mud_dk": "#6d6a64", "nest": "#8a6a44", "nest_dk": "#5e452a",
    "wall": "#7d3f3f", "wall2": "#743939", "wood": "#a8754a", "wood_dk": "#8a5c36", "rug": "#2f5a7a",
    "night": "#1d2a4a", "cork": "#c89a62", "cork_dk": "#b3864f", "bark": "#6e4b30", "bark_dk": "#4f3420",
    "red": "#e5383b", "green": "#3fb950", "yellow": "#ffd34d", "blue": "#3b7dd8", "sky": "#9fd0ee",
    "grass": "#7cc061", "grass_dk": "#5ea24a", "road": "#555b66", "siding": "#d9cbb0", "siding_dk": "#c2b392",
}.items()}

BULBS = [hexc("#ff5a5a"), hexc("#ffd34d"), hexc("#5ab0ff"), hexc("#5ee07a"), hexc("#ff9f40")]


def _rng(seed):
    return random.Random(seed)


def glow(ctx, x, y, r, col, a):
    rg = cairo.RadialGradient(x, y, 0, x, y, r)
    rg.add_color_stop_rgba(0, col[0], col[1], col[2], a)
    rg.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
    ctx.set_source(rg)
    ctx.arc(x, y, r, 0, 2 * math.pi)
    ctx.fill()


def _mix(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a[:3], b[:3]))


# ================================================================================================ trees

def _tier_pts(cx, top, bot, half, k=0):
    """A fir tier: apex, jagged sides (branch tips), drooping scallops along the bottom."""
    pts = [(cx, top)]
    n_side = 3
    for i in range(1, n_side + 1):
        u = i / (n_side + 0.3)
        y = top + (bot - top) * u
        w = half * u
        pts.append((cx + w * 0.86, y - 8))
        pts.append((cx + w * 1.0 + 10, y + 14))
    pts.append((cx + half + 14, bot + 6))
    nb = 6
    for i in range(nb + 1):
        x = cx + half - 2 * half * i / nb
        pts.append((x, bot + (22 if i % 2 == 0 else -4) + (6 if k % 2 else 0)))
    pts.append((cx - half - 14, bot + 6))
    for i in range(n_side, 0, -1):
        u = i / (n_side + 0.3)
        y = top + (bot - top) * u
        w = half * u
        pts.append((cx - w * 1.0 - 10, y + 14))
        pts.append((cx - w * 0.86, y - 8))
    return pts


TIERS = [(-90, -440, 390), (-300, -620, 310), (-480, -780, 236), (-650, -910, 160), (-790, -1010, 92)]


def _fir(ctx, t, p, tiers=TIERS, col=None, snow=0.0, seed=1, sway=0.0):
    col = col or _mix(C["fir"], C["dry"], p.get("dry", 0.0))
    rg = _rng(seed)
    for k, (bot, top, half) in enumerate(tiers):
        ctx.save()
        ctx.translate(sway * (k + 1) * 3, 0)
        pts = _tier_pts(0, top, bot, half, k)
        shape(ctx, lambda c, pts=pts: p_poly(c, pts), col, OUT * 0.9, (0.1, 0.12), shade_k=0.82)
        for j in range(int(half / 22)):   # needle texture strokes
            u = rg.random()
            y = top + (bot - top) * (0.35 + 0.6 * u)
            x = (rg.random() - 0.5) * 2 * half * (0.35 + 0.6 * u) * 0.85
            stroke(ctx, [(x, y), (x + (8 if x > 0 else -8), y + 22)], 5, color=darker(col, 0.7), a=0.8)
        if snow > 0:
            sp = [(0, top)] + [(w, top + (bot - top) * 0.25 + 10 * math.sin(w)) for w in (half * 0.25,)] + \
                 [(half * 0.25, top + (bot - top) * 0.33), (0, top + (bot - top) * 0.22),
                  (-half * 0.25, top + (bot - top) * 0.33)]
            shape(ctx, lambda c, sp=sp: p_smooth(c, sp), C["snow"], OUT * 0.5, None, a=snow)
            for s in (-1, 1):
                bx = s * half * 0.7
                shape(ctx, lambda c, bx=bx: p_ellipse(c, bx, bot - 4, half * 0.22, 14), C["snow"], OUT * 0.4, None, a=snow)
        ctx.restore()


def _trunk_stand(ctx, stand=True):
    shape(ctx, lambda c: c.rectangle(-30, -130, 60, 130), C["trunk"], OUT * 0.8, (0.1, 0))
    if stand:
        shape(ctx, lambda c: p_poly(c, [(-110, -80), (110, -80), (90, 0), (-90, 0)]), C["stand"], OUT, (0.1, 0.1))
        stroke(ctx, [(-104, -60), (104, -60)], 6, color=hexc("#8e2a20"))


def _garland_path(k, bot, top, half):
    y0 = bot + (top - bot) * 0.42
    y1 = bot + (top - bot) * 0.18
    w0 = half * 0.62
    w1 = half * 0.86
    return [(-w0, y0), (-w0 * 0.3, y0 + 34), (w0 * 0.4, y1 + 10), (w1, y1 - 20)]


def tc_xtree(ctx, t, p):
    """A Christmas tree, about 1010 tall, origin = floor under the stand. p: deco (0..1 decorations), lit (0..1
    lights on), dry, qmarks (0..1 nine blinking question marks), zs (0..1 sleepy Z's), gifts (bool), stand (bool),
    sway (rad), snow (0..1), glowcalm."""
    deco = p.get("deco", 1.0)
    lit = p.get("lit", 1.0)
    sway = p.get("sway", 0.0) * math.sin(t * 14) if p.get("sway") else 0.0
    if p.get("gifts", deco > 0.5):
        _gift(ctx, -250, 0, 150, 120, hexc("#c0392b"), hexc("#f2c14e"))
        _gift(ctx, 230, 0, 170, 100, hexc("#2c6fbf"), hexc("#f4f4f4"))
        _gift(ctx, 30, 30, 120, 90, hexc("#2f9a5a"), hexc("#e5383b"))
    _trunk_stand(ctx, p.get("stand", True))
    _fir(ctx, t, p, snow=p.get("snow", 0.0), seed=p.get("seed", 1), sway=sway)
    if deco > 0.01:
        a = min(1.0, deco)
        for k, (bot, top, half) in enumerate(TIERS[:4]):
            g = _garland_path(k, bot, top, half)
            stroke(ctx, g, 16, smooth=True, a=a)
            stroke(ctx, g, 9, smooth=True, color=C["gold"], a=a)
        rg = _rng(7)
        orn = []
        for k, (bot, top, half) in enumerate(TIERS[:4]):
            for j in range(4 - k // 2):
                u = (j + 0.5) / (4 - k // 2)
                x = (u - 0.5) * 2 * half * 0.78
                y = bot - 16 + rg.uniform(-30, 10)
                orn.append((x, y, rg.choice([hexc("#e5383b"), hexc("#3b7dd8"), hexc("#f2c14e"), hexc("#d8d8e0"),
                                              hexc("#b04ad8")]), rg.uniform(24, 34)))
        for (x, y, col, r) in orn:
            stroke(ctx, [(x, y - r - 14), (x, y - r)], 3, a=a)
            shape(ctx, lambda c, x=x, y=y, r=r: p_ellipse(c, x, y, r, r), col, OUT * 0.7, (0.12, 0.12),
                  hi=(0.3, 0.25, 0.28), a=a)
            shape(ctx, lambda c, x=x, y=y, r=r: c.rectangle(x - r * 0.35, y - r - 8, r * 0.7, 10), PAL["steel"], OUT * 0.4, None, a=a)
        # lights along the garlands
        i = 0
        for k, (bot, top, half) in enumerate(TIERS[:4]):
            g = _garland_path(k, bot, top, half)
            for j in range(7):
                u = (j + 0.5) / 7
                seg = min(2, int(u * 3))
                uu = u * 3 - seg
                x = g[seg][0] + (g[seg + 1][0] - g[seg][0]) * uu
                y = g[seg][1] + (g[seg + 1][1] - g[seg][1]) * uu + 10
                col = BULBS[i % len(BULBS)]
                tw = 0.65 + 0.35 * math.sin(t * 3.1 + i * 1.7)
                if lit > 0.01:
                    glow(ctx, x, y, 42, col, 0.55 * lit * tw)
                bc = _mix(darker(col, 0.55), col, lit * tw)
                shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 9, 13), bc, OUT * 0.45, None, a=a)
                i += 1
        # star
        sy = TIERS[-1][1] - 18
        if lit > 0.01:
            glow(ctx, 0, sy, 150, hexc("#fff2a0"), 0.5 * lit)
        starburst(ctx, 0, sy, 72, n=5, fill=hexc("#ffd34d"), rot=-math.pi / 2)
    if p.get("qmarks", 0.0) > 0.01:
        pos = [(-250, -200), (60, -260), (260, -170), (-150, -420), (150, -470), (-60, -560), (90, -680), (-90, -770),
               (20, -880)]
        for k, (x, y) in enumerate(pos):
            bl = 0.55 + 0.45 * math.sin(t * 5 + k * 2.1)
            u = max(0.0, min(1.0, p["qmarks"] * 9 - k))
            if u > 0:
                text(ctx, "?", x, y, 74, "#ffd34d", 7, a=u * bl)
    zs = p.get("zs", 0.0)
    if zs > 0.01:
        for k, (x, y) in enumerate([(-200, -230), (180, -330), (-80, -560), (110, -720)]):
            tc_zz(ctx, t + k * 0.7, {"on": zs, "x": x, "y": y, "px": 54})


def _gift(ctx, x, y, w, h, col, rib):
    shape(ctx, lambda c: c.rectangle(x - w / 2, y - h, w, h), col, OUT * 0.8, (0.1, 0.1))
    flat(ctx, lambda c: c.rectangle(x - 10, y - h, 20, h), rib)
    flat(ctx, lambda c: c.rectangle(x - w / 2, y - h * 0.55, w, 18), rib)
    stroke(ctx, [(x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2, y), (x - w / 2, y), (x - w / 2, y - h)], OUT * 0.8)
    for s in (-1, 1):
        shape(ctx, lambda c, s=s: p_ellipse(c, x + s * 22, y - h - 14, 24, 14, s * 0.4), rib, OUT * 0.6, None)


def tc_twig(ctx, t, p):
    """A fir twig, horizontal, about p["len"] (1500) long centred on x = 0; origin = the top of the twig at x = 0
    (where an egg case sits). Flat needles in two rows, side shoots, optional snow. p: len, snow, seed, needle."""
    ln = p.get("len", 1500)
    rg = _rng(p.get("seed", 3))
    col = hexc(p.get("col", "#2f8050"))
    sway = 4 * math.sin(t * 1.3)
    th = p.get("th", 34)
    pts = [(-ln / 2, 26 + sway), (-ln / 4, 14 + sway * 0.5), (0, th / 2), (ln / 4, th / 2 - 8), (ln / 2, th / 2 - 22)]
    # side shoots
    for k in range(5):
        x = -ln / 2 + ln * (k + 0.6) / 5.4
        if abs(x) < 160:
            continue
        s = -1 if k % 2 else 1
        ex, ey = x + 260, th / 2 + s * 200
        _needled(ctx, [(x, th / 2), (x + 120, th / 2 + s * 90), (ex, ey)], col, rg, 11, 70)
    _needled(ctx, pts, col, rg, 18, 90, wood=True, th=th)
    if p.get("snow", 0.0) > 0.01:
        for k in range(9):
            x = -ln / 2 + ln * (k + 0.5) / 9
            if abs(x) < 150:
                continue
            shape(ctx, lambda c, x=x: p_ellipse(c, x, -12, 70, 22), C["snow"], OUT * 0.45, None, a=p["snow"])


def _needled(ctx, pts, col, rg, w, nl, wood=False, th=18):
    """A stem along pts with flat needles both sides (fir)."""
    segs = []
    for (a, b) in zip(pts, pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = int(L / 24)
        for i in range(n):
            u = i / max(n, 1)
            segs.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, math.atan2(b[1] - a[1], b[0] - a[0])))
    dk = darker(col, 0.72)
    for k, (x, y, ang) in enumerate(segs):   # far row (dark)
        a2 = ang - 1.15 + rg.uniform(-0.12, 0.12)
        stroke(ctx, [(x, y), (x + nl * math.cos(a2), y + nl * math.sin(a2))], 15, color=INK)
        stroke(ctx, [(x, y), (x + nl * math.cos(a2), y + nl * math.sin(a2))], 9, color=dk)
    limb(ctx, pts, th if wood else w, C["trunk"], OUT * 0.6, smooth=True)
    for k, (x, y, ang) in enumerate(segs):   # near row (light), angled forward and down
        a2 = ang + 1.05 + rg.uniform(-0.12, 0.12)
        stroke(ctx, [(x, y), (x + nl * math.cos(a2), y + nl * math.sin(a2))], 16, color=INK)
        stroke(ctx, [(x, y), (x + nl * math.cos(a2), y + nl * math.sin(a2))], 10, color=col)


def tc_wild(ctx, t, p):
    """A wild conifer in snow, origin = ground at the trunk; p: kind (spruce | pine), snow, h (height scale)."""
    kind = p.get("kind", "spruce")
    snow = p.get("snow", 1.0)
    if kind == "pine":
        shape(ctx, lambda c: p_poly(c, [(-34, 0), (34, 0), (18, -900), (-18, -900)]), hexc("#9a5a32"), OUT * 0.8, (0.1, 0))
        rg = _rng(p.get("seed", 5))
        for k, (x, y, rx, ry) in enumerate([(-170, -640, 190, 90), (160, -760, 200, 95), (-60, -900, 230, 110),
                                            (120, -1000, 160, 80), (-180, -820, 150, 70)]):
            stroke(ctx, [(0, y + 40), (x * 0.7, y + 10)], 14, color=hexc("#7a4a2a"))
            shape(ctx, lambda c, x=x, y=y, rx=rx, ry=ry, k=k: p_blob(c, x, y, rx, ry, 0.12, k + 2, 18), hexc("#3f7a4a"),
                  OUT * 0.8, (0.08, 0.12))
            if snow > 0:
                shape(ctx, lambda c, x=x, y=y, rx=rx, ry=ry, k=k: p_blob(c, x, y - ry * 0.55, rx * 0.8, ry * 0.38, 0.1, k + 9, 14),
                      C["snow"], OUT * 0.45, None, a=snow)
        return
    tiers = [(-60 - k * 150, -330 - k * 150, 330 - k * 52) for k in range(6)]
    shape(ctx, lambda c: c.rectangle(-26, -110, 52, 110), C["trunk_dk"], OUT * 0.7, None)
    _fir(ctx, t, {}, tiers=tiers, col=hexc(p.get("col", "#2b6e48")), snow=snow, seed=p.get("seed", 4))


def tc_farmtree(ctx, t, p):
    """A neat sheared farm tree (a smooth cone), origin = ground."""
    h = p.get("h", 620)
    col = hexc(p.get("col", "#35884f"))
    shape(ctx, lambda c: c.rectangle(-18, -60, 36, 60), C["trunk_dk"], OUT * 0.6, None)
    pts = [(0, -h)] + [(math.copysign(1, 0.5 - i / 10) * 0, 0) for i in ()]
    pts = [(0, -h), (h * 0.18, -h * 0.62), (h * 0.3, -h * 0.25), (h * 0.36, -50), (0, -38), (-h * 0.36, -50),
           (-h * 0.3, -h * 0.25), (-h * 0.18, -h * 0.62)]
    shape(ctx, lambda c: p_smooth(c, pts), col, OUT * 0.8, (0.1, 0.08))
    for k in range(5):
        y = -h * (0.2 + k * 0.15)
        stroke(ctx, [(-h * 0.25 * (1 - k * 0.17), y), (0, y + 30), (h * 0.25 * (1 - k * 0.17), y)], 4, smooth=True,
               color=darker(col, 0.75), a=0.7)
    if p.get("snow", 0.0) > 0:
        shape(ctx, lambda c: p_smooth(c, [(0, -h), (h * 0.12, -h * 0.72), (0, -h * 0.78), (-h * 0.12, -h * 0.72)]),
              C["snow"], OUT * 0.4, None, a=p["snow"])


def tc_shrub(ctx, t, p):
    """A garden evergreen shrub (a rounded yew), origin = ground. p: snow (0..1), spring (0..1 fresh tips)."""
    col = hexc("#2f6e44")
    for k, (x, y, rx, ry) in enumerate([(-170, -170, 170, 150), (160, -180, 180, 160), (0, -290, 220, 190),
                                        (-40, -150, 230, 150)]):
        shape(ctx, lambda c, x=x, y=y, rx=rx, ry=ry, k=k: p_blob(c, x, y, rx, ry, 0.08, k + 11, 20), col, OUT * 0.85,
              (0.08, 0.12))
    rg = _rng(21)
    for j in range(46):
        x, y = rg.uniform(-320, 320), rg.uniform(-440, -60)
        if (x / 330) ** 2 + ((y + 220) / 230) ** 2 > 1:
            continue
        sp = p.get("spring", 0.0)
        stroke(ctx, [(x, y), (x + 14, y - 18)], 6, color=_mix(darker(col, 0.7), hexc("#9fdc6a"), sp))
    if p.get("snow", 0.0) > 0:
        for k, (x, y, rx) in enumerate([(-170, -300, 120), (160, -320, 130), (0, -460, 150)]):
            shape(ctx, lambda c, x=x, y=y, rx=rx, k=k: p_blob(c, x, y, rx, 40, 0.1, k + 3, 12), C["snow"], OUT * 0.45,
                  None, a=p["snow"])


def tc_tree_end(ctx, t, p):
    """A cut tree lying on its side, seen from the cut end: the trunk's cut face (rings) in front, branches fanning
    round it, the tree body tapering away. Origin = centre of the cut face. p: peek (0..1 dark interior gaps)."""
    rg = _rng(31)
    col = C["fir"]
    # tapering body behind (far end smaller, up-right)
    shape(ctx, lambda c: p_smooth(c, [(-430, 60), (-300, -330), (60, -470), (460, -380), (760, -150), (820, 40),
                                      (700, 220), (300, 330), (-200, 300)]), darker(col, 0.85), OUT, (0.06, 0.1))
    # branch fans radiating from the cut end
    for k in range(18):
        a = 2 * math.pi * k / 18 + rg.uniform(-0.1, 0.1)
        L = rg.uniform(260, 380)
        ex, ey = L * math.cos(a), L * math.sin(a) * 0.82
        _needled(ctx, [(0, 0), (ex * 0.5, ey * 0.5), (ex, ey)], col if k % 2 else C["fir_lt"], rg, 8, 46)
    if p.get("peek", 0.0) > 0:
        flat(ctx, lambda c: p_ellipse(c, 0, 0, 120, 100), hexc("#0f2a18"), a=0.5 * p["peek"])
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 62, 62), C["cut"], OUT, (0.06, 0.06))
    for r in (44, 28, 14):
        ctx.new_sub_path()
        ctx.arc(0, 0, r, 0, 2 * math.pi)
        ctx.set_source_rgb(*C["ring"])
        ctx.set_line_width(4)
        ctx.stroke()
    stroke(ctx, [(0, -60), (0, 60)], 3, color=C["ring"], a=0.5)


def _tree_side(ctx, ln=900, col=None, dry=0.0):
    """A cut tree lying sideways (trunk end at x = 0, tip at x = ln), side view; origin = trunk centre."""
    col = col or _mix(C["fir"], C["dry"], dry)
    shape(ctx, lambda c: c.rectangle(-70, -22, 140, 44), C["trunk"], OUT * 0.8, (0, 0.2))
    shape(ctx, lambda c: p_ellipse(c, -70, 0, 14, 22), C["cut"], OUT * 0.6, None)
    for k in range(5):
        x0 = 40 + k * ln * 0.17
        hw = 230 * (1 - k * 0.17)
        pts = [(x0, 0), (x0 + 60, -hw), (x0 + ln * 0.26, -hw * 0.65), (x0 + ln * 0.3, 0), (x0 + ln * 0.26, hw * 0.65),
               (x0 + 60, hw)]
        shape(ctx, lambda c, pts=pts: p_poly(c, pts), col if k % 2 == 0 else darker(col, 0.9), OUT * 0.8, (0.06, 0.1))


def tc_tree_lying(ctx, t, p):
    _tree_side(ctx, p.get("len", 900), dry=p.get("dry", 0.0))


def tc_rootball(ctx, t, p):
    """A balled-and-burlapped tree: a small fir on a burlap ball tied with twine. Origin = floor."""
    shape(ctx, lambda c: p_ellipse(c, 0, -150, 200, 150), hexc("#b89462"), OUT, (0.1, 0.12))
    for k in range(-3, 4):
        stroke(ctx, [(k * 50, -290), (k * 62, -150), (k * 50, -10)], 4, smooth=True, color=hexc("#8a6a3e"))
    stroke(ctx, [(-196, -170), (0, -120), (196, -170)], 6, smooth=True, color=hexc("#5e452a"))
    stroke(ctx, [(-150, -260), (0, -300), (150, -260)], 6, smooth=True, color=hexc("#5e452a"))
    ctx.save()
    ctx.translate(0, -270)
    ctx.scale(0.62, 0.62)
    shape(ctx, lambda c: c.rectangle(-28, -150, 56, 150), C["trunk"], OUT, None)
    _fir(ctx, t, {}, tiers=[(b - 60, tp - 60, h) for (b, tp, h) in TIERS])
    ctx.restore()


# ================================================================================================ scenes

def _snowfall(ctx, t, x0, x1, y0, y1, n=60, seed=2, a=0.8):
    rg = _rng(seed)
    for k in range(n):
        x = rg.uniform(x0, x1) + 30 * math.sin(t * 0.8 + k)
        sp = rg.uniform(40, 90)
        y = y0 + ((rg.uniform(0, 1) * (y1 - y0) + t * sp) % (y1 - y0))
        r = rg.uniform(3, 7)
        flat(ctx, lambda c, x=x, y=y, r=r: p_ellipse(c, x, y, r, r), (1, 1, 1), a=a)


def tc_living(ctx, t, layer, p):
    """A living room at night: deep red wallpaper, wainscot, wood floor from y = 900, a snowy night window at
    x 0..420, a fireplace with stockings at x 1500..2000 (p fire), a rug. The tree stands at about x = 960."""
    layer(0.95)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 4000), C["wall"])
    for x in range(-3000, 5000, 140):
        flat(ctx, lambda c, x=x: c.rectangle(x, -3000, 54, 3900), C["wall2"])
    for x in range(-3000, 5000, 140):   # little gold diamonds
        for y in range(-1600, 600, 160):
            flat(ctx, lambda c, x=x, y=y: p_poly(c, [(x + 97, y), (x + 105, y + 10), (x + 97, y + 20), (x + 89, y + 10)]),
                 hexc("#b8873f"), a=0.5)
    shape(ctx, lambda c: c.rectangle(-3000, 640, 8000, 260), hexc("#e8dcc4"), BG_OUT, None)
    for x in range(-3000, 5000, 260):
        stroke(ctx, [(x, 670), (x, 870)], 4, color=hexc("#cdbf9f"))
    # window
    shape(ctx, lambda c: c.rectangle(-20, 40, 460, 520), hexc("#f1e6cf"), BG_OUT, None)
    flat(ctx, lambda c: c.rectangle(10, 70, 400, 460), C["night"])
    ctx.save()
    ctx.rectangle(10, 70, 400, 460)
    ctx.clip()
    _snowfall(ctx, t, 10, 410, 70, 530, 22, 4, 0.9)
    flat(ctx, lambda c: p_ellipse(c, 300, 140, 34, 34), hexc("#f4f0d8"))
    flat(ctx, lambda c: c.rectangle(10, 470, 400, 60), C["snow"])
    ctx.restore()
    stroke(ctx, [(210, 70), (210, 530)], BG_OUT * 1.6, color=hexc("#f1e6cf"))
    stroke(ctx, [(10, 300), (410, 300)], BG_OUT * 1.6, color=hexc("#f1e6cf"))
    shape(ctx, lambda c: c.rectangle(-50, 540, 520, 30), hexc("#f1e6cf"), BG_OUT, None)
    # fireplace
    if p.get("fireplace", True):
        fx = p.get("fx", 1700)
        shape(ctx, lambda c: c.rectangle(fx - 300, 380, 600, 520), hexc("#b0563c"), BG_OUT, (0.05, 0.05))
        for y in range(400, 900, 50):
            stroke(ctx, [(fx - 300, y), (fx + 300, y)], 3, color=hexc("#8e4430"))
        shape(ctx, lambda c: p_rrect(c, fx - 170, 580, 340, 320, 150), hexc("#2a1712"), BG_OUT, None)
        if p.get("fire", 1.0) > 0:
            for k in range(3):
                fl = 1 + 0.12 * math.sin(t * 9 + k * 2)
                shape(ctx, lambda c, k=k, fl=fl: p_smooth(c, [(fx - 90 + k * 90, 880), (fx - 130 + k * 90, 820),
                                                              (fx - 90 + k * 90, 820 - 110 * fl), (fx - 50 + k * 90, 820)]),
                      hexc("#ffb03b"), BG_OUT * 0.6, None)
            glow(ctx, fx, 800, 300, hexc("#ffb03b"), 0.35)
        shape(ctx, lambda c: c.rectangle(fx - 340, 350, 680, 40), hexc("#6b3f25"), BG_OUT, None)
        for k, col in enumerate((hexc("#e5383b"), hexc("#2f9a5a"), hexc("#e5383b"))):
            sx = fx - 200 + k * 200
            shape(ctx, lambda c, sx=sx, col=col: p_poly(c, [(sx - 34, 390), (sx + 34, 390), (sx + 34, 520), (sx + 70, 540),
                                                            (sx + 60, 580), (sx - 20, 570), (sx - 34, 530)]), col, BG_OUT, None)
            shape(ctx, lambda c, sx=sx: c.rectangle(sx - 40, 386, 80, 34), (1, 1, 1), BG_OUT, None)
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 900, 8000, 3000), C["wood"])
    for y in (960, 1040, 1150):
        stroke(ctx, [(-3000, y), (5000, y)], 4, color=C["wood_dk"])
    stroke(ctx, [(-3000, 900), (5000, 900)], BG_OUT)
    if p.get("rug", True):
        shape(ctx, lambda c: p_ellipse(c, 960, 990, 620, 70), C["rug"], BG_OUT, None)
        ctx.new_sub_path()
        ctx.save()
        ctx.translate(960, 990)
        ctx.scale(560, 56)
        ctx.arc(0, 0, 1, 0, 2 * math.pi)
        ctx.restore()
        ctx.set_source_rgb(*hexc("#f2c14e"))
        ctx.set_line_width(5)
        ctx.stroke()
    ctx.save()   # warm evening grade
    ctx.identity_matrix()
    ctx.rectangle(0, 0, ctx.get_target().get_width(), ctx.get_target().get_height())
    ctx.set_source_rgba(0.08, 0.04, 0.12, 0.12)
    ctx.fill()
    ctx.restore()


def tc_bokeh(ctx, t, layer, p):
    """Warm, out-of-focus Christmas lights and a blurred ornament: the background of every close-up."""
    layer(0.6)
    flat(ctx, lambda c: c.rectangle(-4000, -4000, 9000, 9000), hexc(p.get("color", "#2a1f2e")))
    rg = _rng(p.get("seed", 8))
    for k in range(34):
        x, y = rg.uniform(-900, 2900), rg.uniform(-600, 1700)
        r = rg.uniform(50, 130)
        col = BULBS[k % len(BULBS)]
        a = 0.18 + 0.12 * math.sin(t * 1.2 + k)
        glow(ctx, x, y, r, col, a + 0.1)
        flat(ctx, lambda c, x=x, y=y, r=r: p_ellipse(c, x, y, r * 0.55, r * 0.55), col, a=a * 0.6)
    for (x, y, r, col) in ((1650, 120, 160, hexc("#b8322c")), (150, 820, 120, hexc("#2c6fbf"))):
        flat(ctx, lambda c, x=x, y=y, r=r: p_ellipse(c, x, y, r, r), darker(col, 0.8), a=0.55)
        flat(ctx, lambda c, x=x, y=y, r=r: p_ellipse(c, x - r * 0.3, y - r * 0.3, r * 0.3, r * 0.25), lighter(col, 0.5), a=0.35)
    if p.get("green", True):   # soft fir mass behind
        for k in range(9):
            x = -600 + k * 420
            flat(ctx, lambda c, x=x, k=k: p_blob(c, x, 1300 + 60 * (k % 2), 330, 260, 0.12, k), hexc("#1e4a30"), a=0.6)


def _ground_snow(ctx, y, x0=-3000, x1=5000):
    flat(ctx, lambda c: c.rectangle(x0, y, x1 - x0, 4000), C["snow"])
    stroke(ctx, [(x0, y), (x1, y)], BG_OUT * 0.8, color=C["snow_dk"])
    for k in range(-20, 40):
        x = k * 230
        flat(ctx, lambda c, x=x: p_ellipse(c, x, y + 60 + (k % 3) * 40, 90, 10), C["snow_dk"], a=0.6)


def tc_lot(ctx, t, layer, p):
    """A Christmas tree lot at dusk: navy sky, string lights on poles, rows of netted trees leaning on rails, snowy
    ground from y = 900, a small hut on the right."""
    layer(0.7)
    for k, col in enumerate(("#26305c", "#34407a", "#4a4f8a", "#6a5e93")):
        flat(ctx, lambda c, k=k, col=col: c.rectangle(-3000, -3000 + k * 900 if k else -3000, 8000, 4000), hexc(col))
    flat(ctx, lambda c: c.rectangle(-3000, 500, 8000, 500), hexc("#7a6a9a"))
    layer(0.85)
    for k in range(-6, 14):
        x = k * 230
        ctx.save()
        ctx.translate(x, 900)
        ctx.rotate(math.radians(8 * math.sin(k)))
        ctx.scale(0.42, 0.42)
        _fir(ctx, t, {}, col=hexc("#2a6e46") if k % 2 else hexc("#317a4d"), seed=k + 20)
        stroke(ctx, [(-120, -900), (100, -100)], 3, color=(1, 1, 1), a=0.35)
        ctx.restore()
    shape(ctx, lambda c: c.rectangle(-3000, 820, 8000, 24), hexc("#8a5c36"), BG_OUT, None)
    # hut
    shape(ctx, lambda c: c.rectangle(2100, 380, 520, 520), hexc("#a8452f"), BG_OUT, (0.05, 0))
    shape(ctx, lambda c: p_poly(c, [(2060, 390), (2360, 220), (2660, 390)]), hexc("#f4f7fb"), BG_OUT, None)
    shape(ctx, lambda c: c.rectangle(2200, 520, 320, 140), hexc("#ffe7a0"), BG_OUT, None)
    text(ctx, "TREES", 2360, 470, 64, "#ffffff", 6)
    # string lights
    for k in range(-3, 6):
        x0, x1 = k * 700, (k + 1) * 700
        stroke(ctx, [(x0, 140), (x0, 900)], BG_OUT * 1.4, color=hexc("#5a3a22"))
        pts = [(x0 + (x1 - x0) * u / 10, 160 + 90 * math.sin(math.pi * u / 10)) for u in range(11)]
        stroke(ctx, pts, 4, color=INK)
        for j, (x, y) in enumerate(pts[1:-1]):
            col = BULBS[(j + k) % len(BULBS)]
            glow(ctx, x, y + 14, 34, col, 0.5)
            flat(ctx, lambda c, x=x, y=y, col=col: p_ellipse(c, x, y + 14, 8, 11), col)
    layer(1.0)
    _ground_snow(ctx, 900)


def tc_snowwood(ctx, t, layer, p):
    """A wild Norwegian winter forest: pale sky, distant blue spruces, snowy ground at y = 900, falling snow."""
    layer(0.5)
    flat(ctx, lambda c: c.rectangle(-4000, -4000, 9000, 9000), hexc("#cfe0ee"))
    flat(ctx, lambda c: c.rectangle(-4000, 300, 9000, 900), hexc("#e2ecf4"))
    for k in range(-10, 18):
        x = k * 190 + (k % 3) * 40
        ctx.save()
        ctx.translate(x, 760)
        ctx.scale(0.3, 0.3 + 0.05 * (k % 3))
        _fir(ctx, t, {}, col=hexc("#5f8aa0"), snow=0.8, seed=k)
        ctx.restore()
    layer(0.8)
    for k in range(-5, 10):
        x = k * 420 + 100
        ctx.save()
        ctx.translate(x, 860)
        ctx.scale(0.55, 0.6)
        _fir(ctx, t, {}, col=hexc("#3d6e5a"), snow=0.9, seed=k + 40)
        ctx.restore()
    layer(1.0)
    _ground_snow(ctx, 900)
    if p.get("fall", True):
        ctx.save()
        ctx.identity_matrix()
        _snowfall(ctx, t, 0, 1920, 0, 1080, 70, 3, 0.85)
        ctx.restore()


def tc_farm(ctx, t, layer, p):
    """A tree farm: neat rows of sheared cone trees in perspective; winter (snow) or green. Ground from y = 700."""
    snow = p.get("snow", 1.0)
    layer(0.5)
    flat(ctx, lambda c: c.rectangle(-4000, -4000, 9000, 9000), hexc("#a8d4ef") if snow < 0.5 else hexc("#c9dceb"))
    for k in range(-3, 6):
        flat(ctx, lambda c, k=k: p_ellipse(c, k * 700, 700, 600, 160), hexc("#9fb7a6") if snow < 0.5 else hexc("#e6edf3"))
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-4000, 700, 9000, 4000), C["grass"] if snow < 0.5 else C["snow"])
    for row in range(5):
        y = 720 + row * row * 28 + row * 40
        k = 0.35 + row * 0.22
        n = 16 - row * 2
        for j in range(-n, n + 1):
            x = 960 + j * 380 * k
            ctx.save()
            ctx.translate(x, y)
            ctx.scale(k, k)
            tc_farmtree(ctx, t, {"snow": snow, "h": 600 + (j % 3) * 30})
            ctx.restore()
    if snow > 0.5 and p.get("fall", False):
        ctx.save()
        ctx.identity_matrix()
        _snowfall(ctx, t, 0, 1920, 0, 1080, 50, 6, 0.8)
        ctx.restore()


def tc_yard(ctx, t, layer, p):
    """A front yard: the house's siding and a door on the left, lawn from y = 900 (snowy, or green with p spring)."""
    spring = p.get("spring", 0.0) > 0.5
    layer(0.6)
    flat(ctx, lambda c: c.rectangle(-4000, -4000, 9000, 9000), C["sky"] if spring else hexc("#b9c9da"))
    if spring:
        flat(ctx, lambda c: p_ellipse(c, 1700, 120, 80, 80), hexc("#ffd84a"))
    layer(0.9)
    shape(ctx, lambda c: c.rectangle(-3000, 100, 3000 + p.get("house_w", 700), 800), C["siding"], BG_OUT, None)
    for y in range(130, 900, 50):
        stroke(ctx, [(-3000, y), (p.get("house_w", 700), y)], 3, color=C["siding_dk"])
    shape(ctx, lambda c: c.rectangle(250, 380, 230, 520), hexc("#8a3a2a"), BG_OUT, (0.05, 0))
    flat(ctx, lambda c: p_ellipse(c, 440, 640, 12, 12), C["gold"])
    if not spring:
        shape(ctx, lambda c: p_ellipse(c, 365, 330, 70, 70), hexc("#2f8050"), BG_OUT, None)   # wreath
        flat(ctx, lambda c: p_ellipse(c, 365, 330, 34, 34), C["siding"])
        shape(ctx, lambda c: p_ellipse(c, 365, 395, 22, 14), C["red"], BG_OUT * 0.6, None)
    layer(1.0)
    if spring:
        flat(ctx, lambda c: c.rectangle(-4000, 900, 9000, 4000), C["grass"])
        rg = _rng(5)
        for k in range(70):
            x, y = rg.uniform(-600, 2600), rg.uniform(920, 1200)
            stroke(ctx, [(x, y), (x + 6, y - 26)], 4, color=C["grass_dk"])
        for k in range(10):
            x = 900 + k * 140
            flat(ctx, lambda c, x=x, k=k: p_ellipse(c, x, 950 + (k % 3) * 30, 12, 12), [hexc("#ff7aa8"), hexc("#ffd34d"),
                                                                                      hexc("#b48cff")][k % 3])
    else:
        _ground_snow(ctx, 900)


def tc_cork(ctx, t, layer, p):
    """A corkboard filling the frame: speckled cork, a wooden frame edge at the far left and top."""
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-4000, -4000, 9000, 9000), C["cork"])
    rg = _rng(9)
    for k in range(900):
        x, y = rg.uniform(-1500, 3500), rg.uniform(-1000, 2200)
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 5, 4), C["cork_dk"], a=0.7)
    for k, (x, y, w, h, r) in enumerate(p.get("papers", [(150, 150, 300, 220, -4), (1500, 700, 280, 200, 5),
                                                         (300, 760, 260, 180, 3)])):
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(math.radians(r))
        shape(ctx, lambda c, w=w, h=h: c.rectangle(-w / 2, -h / 2, w, h), PAL["paper"], OUT * 0.6, (0, 0.1))
        for j in range(4):
            stroke(ctx, [(-w / 2 + 30, -h / 2 + 50 + j * 36), (w / 2 - 40 - (j % 2) * 50, -h / 2 + 50 + j * 36)], 6,
                   color=hexc("#9aa3ab"))
        flat(ctx, lambda c, h=h: p_ellipse(c, 0, -h / 2 + 18, 14, 14), C["red"])
        ctx.restore()


def tc_trunk(ctx, t, layer, p):
    """A bark close-up: the trunk fills the middle of the frame (x 460..1460), fir twigs at the edges, bokeh behind."""
    tc_bokeh(ctx, t, layer, {"green": True})
    layer(1.0)
    x0, x1 = p.get("x0", 460), p.get("x1", 1460)
    shape(ctx, lambda c: c.rectangle(x0, -3000, x1 - x0, 7000), C["bark"], BG_OUT, None)
    rg = _rng(p.get("seed", 12))
    for k in range(26):   # bark plates and ridges
        x = rg.uniform(x0 + 30, x1 - 30)
        y = rg.uniform(-300, 1400)
        w, h = rg.uniform(60, 140), rg.uniform(120, 260)
        shape(ctx, lambda c, x=x, y=y, w=w, h=h, k=k: p_blob(c, x, y, w, h, 0.12, k), lighter(C["bark"], 0.12),
              BG_OUT * 0.5, None)
    for k in range(14):
        x = x0 + 40 + k * (x1 - x0 - 80) / 13
        stroke(ctx, [(x, -300), (x + 14 * math.sin(k), 400), (x - 10, 1400)], 7, smooth=True, color=C["bark_dk"])
    stroke(ctx, [(x0, -3000), (x0, 4000)], BG_OUT, color=INK)
    stroke(ctx, [(x1, -3000), (x1, 4000)], BG_OUT, color=INK)
    if p.get("twigs", True):
        for (x, y, s) in ((x0, 120, -1), (x1, 420, 1), (x0, 860, -1)):
            ctx.save()
            ctx.translate(x, y)
            ctx.scale(s * 0.6, 0.6)
            _needled(ctx, [(0, 0), (260, -40), (560, -60)], C["fir"], rg, 14, 80, wood=True, th=22)
            ctx.restore()


def tc_road(ctx, t, layer, p):
    """A winter road seen from the side: sky, snowy fields, the road surface from y = 860 to 1080 with dashes,
    a COUNTY LINE sign at x = p["sign"] (default 1300)."""
    layer(0.5)
    flat(ctx, lambda c: c.rectangle(-4000, -4000, 12000, 9000), hexc("#b9d3ea"))
    for k in range(-6, 30):
        flat(ctx, lambda c, k=k: p_ellipse(c, k * 500, 700, 420, 120), hexc("#e8eff5"))
    for k in range(-10, 60):
        x = k * 260
        ctx.save()
        ctx.translate(x, 720)
        ctx.scale(0.18, 0.18)
        _fir(ctx, t, {}, col=hexc("#4f7f6a"), snow=0.7, seed=k)
        ctx.restore()
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-4000, 720, 16000, 140), C["snow"])
    flat(ctx, lambda c: c.rectangle(-4000, 860, 16000, 400), C["road"])
    for k in range(-20, 80):
        flat(ctx, lambda c, k=k: c.rectangle(k * 220, 960, 110, 14), hexc("#f2d36b"))
    sx = p.get("sign", 1300)
    stroke(ctx, [(sx, 860), (sx, 560)], 14)
    stroke(ctx, [(sx, 860), (sx, 560)], 8, color=PAL["steel"])
    shape(ctx, lambda c: p_rrect(c, sx - 190, 420, 380, 150, 12), hexc("#2f7a4a"), OUT, None)
    stroke(ctx, [(sx - 175, 435), (sx + 175, 435), (sx + 175, 555), (sx - 175, 555), (sx - 175, 435)], 5,
           color=(1, 1, 1))
    text(ctx, "COUNTY LINE", sx, 495, 54, "#ffffff", 0)
    ctx.set_dash([26, 20])
    stroke(ctx, [(sx, 860), (sx, 1300)], 8, color=(1, 1, 1), a=0.9)
    ctx.set_dash([])


def tc_curb(ctx, t, layer, p):
    """A street curb in January: house front behind, sidewalk and curb, snowbank; ground at y = 900."""
    layer(0.7)
    flat(ctx, lambda c: c.rectangle(-4000, -4000, 9000, 9000), hexc("#c3d2e2"))
    shape(ctx, lambda c: c.rectangle(-600, 120, 1300, 640), hexc("#9fb0c8"), BG_OUT, None)
    shape(ctx, lambda c: p_poly(c, [(-700, 130), (50, -260), (800, 130)]), hexc("#6a5a7a"), BG_OUT, None)
    for (x, y) in ((-380, 330), (300, 330)):
        shape(ctx, lambda c, x=x, y=y: c.rectangle(x, y, 200, 180), hexc("#ffe7a0"), BG_OUT, None)
    shape(ctx, lambda c: c.rectangle(1100, 200, 1300, 560), hexc("#b7a59a"), BG_OUT, None)
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-4000, 760, 9000, 140), hexc("#d9d9de"))
    shape(ctx, lambda c: c.rectangle(-4000, 880, 9000, 40), hexc("#b9b9c2"), BG_OUT, None)
    flat(ctx, lambda c: c.rectangle(-4000, 920, 9000, 400), C["road"])
    for k in range(-10, 20):
        flat(ctx, lambda c, k=k: p_ellipse(c, k * 300, 770, 160, 34), C["snow"])


# ================================================================================================ creatures

def _lerp_pt(a, b, u):
    return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)


def _spikes(ctx, a, b, n, side, ln, w=5):
    """Small spikes along segment a -> b, on one side (side = +1 / -1 of the direction)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L * side, dx / L * side
    for i in range(n):
        u = (i + 0.7) / (n + 0.4)
        x, y = a[0] + dx * u, a[1] + dy * u
        shape(ctx, lambda c, x=x, y=y: p_poly(c, [(x - dx / L * 7, y - dy / L * 7), (x + nx * ln, y + ny * ln),
                                                  (x + dx / L * 7, y + dy / L * 7)]), (0.95, 0.92, 0.8), w * 0.5, None)


def tc_mantis(ctx, t, p):
    """Praying mantis, side view facing right, feet at y = 0, about 760 long: a long abdomen under folded wings, a
    long raised neck (prothorax), a TRIANGULAR head turned to camera with two big bulging eyes, and two raised
    spiked forelegs folded in front. p: col (hex), mood, look, strike (0..1 forelegs shoot out), lay (0..1 the
    abdomen tip bends down), nymph (pale, thin, no wings), walk, tilt (head tilt)."""
    nymph = p.get("nymph", False)
    col = hexc(p.get("col", "#efe4c0" if nymph else "#8cbf4f"))
    dk = darker(col, 0.72)
    wk = 1.0 if p.get("walking") else p.get("walk", 0.0)
    ph = p.get("phase", t * 9)
    lw = OUT * (0.7 if nymph else 0.9)
    th = 0.55 if nymph else 1.0   # limb thickness factor
    bob = 4 * math.sin(t * 1.6)
    lay = p.get("lay", 0.0)

    def leg(base, knee, foot, w, c, k):
        sw = 22 * math.sin(ph + k * 1.7) * wk
        limb(ctx, [base, (knee[0] + sw * 0.5, knee[1] - abs(sw) * 0.3), (foot[0] + sw, foot[1])], w * th, c, lw * 0.8,
             smooth=False)
    # far legs (darker)
    leg((-30, -185 + bob), (40, -260), (90, 0), 11, dk, 0)
    leg((-80, -180 + bob), (-170, -250), (-250, 0), 11, dk, 1)
    # abdomen (tip bends down while laying)
    tip = (-430, -210 + 150 * lay)
    ab = [(-20, -222 + bob), (-140, -238 + bob), (-300, -236 + bob), (tip[0], tip[1] - 6), (tip[0] + 6, tip[1] + 22),
          (-300, -160 + bob + 40 * lay), (-150, -150 + bob), (-30, -165 + bob)]
    shape(ctx, lambda c: p_smooth(c, ab), col, lw, (0.06, 0.16))
    for k in range(5):
        x = -110 - k * 55
        stroke(ctx, [(x, -232 + bob + (k * 6 * lay)), (x - 6, -168 + bob + k * 8 * lay)], 3, color=dk, a=0.8)
    if not nymph:   # folded wings on top, lighter, with a vein
        wg = [(-30, -228 + bob), (-200, -256 + bob), (-400, -232 + bob + 120 * lay), (-380, -214 + bob + 110 * lay),
              (-200, -222 + bob), (-40, -206 + bob)]
        shape(ctx, lambda c: p_smooth(c, wg), lighter(col, 0.3), lw * 0.8, None)
        stroke(ctx, [(-50, -220 + bob), (-220, -238 + bob), (-370, -224 + bob + 115 * lay)], 3, smooth=True, color=dk)
    # near walking legs
    leg((-20, -180 + bob), (70, -270), (150, 0), 13, col, 2)
    leg((-70, -175 + bob), (-190, -270), (-320, 0), 13, col, 3)
    # thorax + long neck rising to the head
    neck = [(-40, -195 + bob), (60, -260 + bob), (150, -360 + bob)]
    limb(ctx, neck, (40 if not nymph else 26), col, lw)
    hx, hy = 168, -400 + bob
    st = ease(p.get("strike", 0.0))
    # forelegs (far one first, darker), folded "praying" pose -> strike
    for far in (1, 0):
        c = dk if far else col
        o = (-14, -6) if far else (0, 0)
        base = (110 + o[0], -300 + bob + o[1])
        knee = _lerp_pt((150 + o[0], -228 + bob), (210 + o[0], -300 + bob), st)
        fem_end = _lerp_pt((262 + o[0], -322 + bob + o[1]), (420 + o[0], -360 + bob), st)
        tib_end = _lerp_pt((178 + o[0], -282 + bob + o[1]), (560 + o[0], -300 + bob), st)
        limb(ctx, [base, knee], 16 * th, c, lw * 0.8, smooth=False)
        limb(ctx, [knee, fem_end], 24 * th, c, lw * 0.8, smooth=False)   # thick spiked femur
        if not far:
            _spikes(ctx, knee, fem_end, 4, 1, 22 * th, lw)
        limb(ctx, [fem_end, tib_end], 13 * th, c, lw * 0.8, smooth=False)
        if not far:
            _spikes(ctx, fem_end, tib_end, 3, -1 if st < 0.5 else 1, 14 * th, lw)
        stroke(ctx, [tib_end, (tib_end[0] + 16 * (1 - 2 * st) * -1, tib_end[1] - 14)], 5 * th + 3)
    # head: an inverted triangle facing camera, big eyes on the two top corners, antennae
    hs = 1.25 if nymph else 1.0
    tilt = p.get("tilt", 0.0) + 0.06 * math.sin(t * 1.1)
    ctx.save()
    ctx.translate(hx, hy)
    ctx.rotate(tilt)
    ctx.scale(hs, hs)
    for s in (-1, 1):
        stroke(ctx, [(s * 14, -40), (s * 40, -120), (s * 90 + 30, -200)], 3.5, smooth=True)
    tri = [(-74, -40), (0, -52), (74, -40), (40, 30), (0, 58), (-40, 30)]
    shape(ctx, lambda c: p_smooth(c, tri), col, lw, (0.08, 0.1))
    eyes(ctx, 0, -34, 30, 56, p.get("look", (0.2, 0.3)), p.get("mood", "calm"), p.get("blink", 0), OUT * 0.6,
         lid=col)
    mouth(ctx, 0, 34, 22, p.get("mouth", "smile"), p.get("talk", 0.0), OUT * 0.55)
    ctx.restore()


def tc_nymph(ctx, t, p):
    """A just-hatched mantis nymph (pale, thin, no wings, big head). p: napkin (0..1), look, mood."""
    tc_mantis(ctx, t, dict(p, nymph=True))
    if p.get("napkin", 0.0) > 0.01:   # a tiny white napkin tucked under the chin
        ctx.save()
        ctx.translate(168 + 6, -340)
        ctx.scale(1.25, 1.25)
        shape(ctx, lambda c: p_poly(c, [(-34, 0), (34, 0), (0, 70)]), (1, 1, 1), OUT * 0.5, None, a=p["napkin"])
        ctx.restore()


def _foam(ctx, cx, cy, rx, ry, seed, col, dk, toast=1.0):
    shape(ctx, lambda c: p_blob(c, cx, cy, rx, ry, 0.07, seed, 22), col, OUT, (0.08, 0.12), hi=(0.3, 0.25, 0.3))
    rg = _rng(seed)
    if toast > 0:   # toasted patches on top
        for k in range(5):
            x = cx + rg.uniform(-0.6, 0.6) * rx
            y = cy - ry * rg.uniform(0.35, 0.7)
            flat(ctx, lambda c, x=x, y=y, k=k: p_blob(c, x, y, rx * 0.22, ry * 0.15, 0.2, k + seed), C["toast"], a=0.45 * toast)
    for k in range(26):   # foam bubbles
        a = rg.uniform(0, 2 * math.pi)
        r = rg.uniform(0.1, 0.85)
        x, y = cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)
        rr = rg.uniform(5, 11) * rx / 120
        ctx.new_sub_path()
        ctx.arc(x, y, rr, 0, 2 * math.pi)
        ctx.set_source_rgba(*dk, 0.6)
        ctx.set_line_width(2.4)
        ctx.stroke()


def tc_ooth(ctx, t, p):
    """A mantis egg case glued to a twig; origin = the twig's top surface under the case.
    p: kind (chinese: round tan foamy blob about 220 x 190 here, "toasted marshmallow"; carolina: slim, ribbed, along
    the twig), quiver (0..1 shiver), crack (0..1 a crack opens), xray (0..1 cutaway with rows of eggs), split (0..1
    the hatch: the case opens and pale heads poke out), grow (0..1 the froth being laid), wet (0..1 froth: paler)."""
    kind = p.get("kind", "chinese")
    q = p.get("quiver", 0.0)
    jx = q * (3.2 * math.sin(t * 47) + 1.5 * math.sin(t * 71))
    jy = q * 1.8 * math.sin(t * 59)
    g = p.get("grow", 1.0)
    if g <= 0.01:
        return
    ctx.save()
    ctx.translate(jx, jy)
    ctx.scale(g, g)
    wet = p.get("wet", 0.0)
    col = _mix(C["case"], hexc("#f4ecd8"), wet)
    if kind == "carolina":
        pts = [(-170, 6), (-150, -40), (-60, -70), (60, -76), (160, -46), (185, 4), (60, 22), (-60, 22)]
        shape(ctx, lambda c: p_smooth(c, pts), hexc("#b89a6a"), OUT, (0.06, 0.15))
        for k in range(11):
            x = -140 + k * 28
            stroke(ctx, [(x, -62 + abs(k - 5) * 3), (x + 6, 12)], 3.5, color=hexc("#8a6e44"))
        stroke(ctx, [(-150, -48), (-40, -76), (80, -78), (165, -48)], 6, smooth=True, color=hexc("#8a6e44"))
        ctx.restore()
        return
    rx, ry = 124, 100
    cy = -ry + 30
    pts = [(-118, cy + 40), (-128, cy - 10), (-104, cy - 66), (-44, cy - 98), (30, cy - 100), (96, cy - 72),
           (128, cy - 16), (120, cy + 46), (60, cy + 92), (-60, cy + 92)]
    shape(ctx, lambda c: p_smooth(c, pts), col, OUT, (0.07, 0.12), hi=(0.28, 0.22, 0.32))
    ctx.save()
    p_smooth(ctx, pts)
    ctx.clip()
    ctx.new_path()
    for k in range(6):   # the layered froth: soft curved bands
        y = cy - 70 + k * 30
        stroke(ctx, [(-140, y + 14), (-60, y - 6), (40, y - 8), (140, y + 10)], 5, smooth=True, color=C["case_dk"], a=0.55)
    rg = _rng(4)
    for k in range(40):   # foam bubbles
        x, y = rg.uniform(-110, 110), rg.uniform(cy - 90, cy + 80)
        rr = rg.uniform(4, 9)
        ctx.new_sub_path()
        ctx.arc(x, y, rr, 0, 2 * math.pi)
        ctx.set_source_rgba(*lighter(col, 0.45), 0.9)
        ctx.fill_preserve()
        ctx.set_source_rgba(*C["case_dk"], 0.7)
        ctx.set_line_width(2)
        ctx.stroke()
    for (x, y, rx2, ry2) in ((-40, cy - 70, 60, 22), (40, cy - 58, 48, 20)):   # toasted tops
        flat(ctx, lambda c, x=x, y=y, rx2=rx2, ry2=ry2: p_blob(c, x, y, rx2, ry2, 0.2, int(x) + 50), C["toast"], a=0.35 * (1 - wet))
    ctx.restore()
    cr = p.get("crack", 0.0)
    if cr > 0.01:
        pts = [(-60, cy - 70), (-20, cy - 40), (-34, cy - 4), (10, cy + 18), (0, cy + 50)]
        n = max(2, int(len(pts) * cr + 0.999))
        stroke(ctx, pts[:n], 7, color=INK)
    xr = p.get("xray", 0.0)
    if xr > 0.01:
        ctx.save()
        p_blob(ctx, 0, cy, rx * 0.86, ry * 0.82, 0.07, 4, 22)
        ctx.clip()
        ctx.new_path()
        flat(ctx, lambda c: c.rectangle(-rx, cy - ry, 2 * rx, 2 * ry), hexc("#3a2a3e"), a=0.85 * xr)
        for row in range(6):
            for k in range(9):
                x = -rx * 0.8 + k * 22 + (row % 2) * 11
                y = cy - ry * 0.7 + row * 26
                flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 8, 11), hexc("#ffe9a8"), a=xr)
        ctx.restore()
    sp = p.get("split", 0.0)
    if sp > 0.01:   # the hatch: the case opens along the top, pale heads with eyes poke out
        shape(ctx, lambda c: p_ellipse(c, 0, cy - ry * 0.55, rx * 0.7 * sp, 20 * sp), hexc("#3a2a20"), OUT * 0.6, None)
        for k in range(5):
            x = -rx * 0.55 + k * rx * 0.28
            y = cy - ry * 0.6 - 26 * sp + 6 * math.sin(t * 6 + k)
            shape(ctx, lambda c, x=x, y=y: p_poly(c, [(x - 16, y - 10), (x + 16, y - 10), (x, y + 18)]), C["nymph"],
                  OUT * 0.4, None, a=min(1.0, sp * 2))
            for s in (-1, 1):
                flat(ctx, lambda c, x=x, y=y, s=s: p_ellipse(c, x + s * 9, y - 10, 5, 5), INK, a=min(1.0, sp * 2))
    ctx.restore()


def tc_marsh(ctx, t, p):
    """A toasted marshmallow on a stick (the stick goes off to the left); origin = marshmallow centre."""
    stroke(ctx, [(-600, 40), (-30, 0)], 22)
    stroke(ctx, [(-600, 40), (-30, 0)], 13, color=hexc("#a8754a"))
    shape(ctx, lambda c: p_rrect(c, -100, -90, 200, 170, 60), hexc("#f2e6cc"), OUT, (0.08, 0.12), hi=(0.3, 0.25, 0.3))
    for (x, y, rx, ry) in ((-30, -60, 60, 26), (40, -40, 48, 30), (-50, 30, 40, 22), (50, 40, 42, 20)):
        flat(ctx, lambda c, x=x, y=y, rx=rx, ry=ry: p_blob(c, x, y, rx, ry, 0.2, int(x)), hexc("#c08a48"), a=0.7)
    flat(ctx, lambda c: p_blob(c, 10, -30, 50, 22, 0.2, 3), hexc("#8a5a2a"), a=0.5)
    stroke(ctx, [(-100, -30), (-100, 30)], OUT)


def _legs_top(ctx, n_side, cx, cy, L, w, col, t, spread=(40, 140), body=60, **_):
    """Top-view legs, head UP: n_side per side, fanned from `spread` degrees (0 = straight ahead) and spaced along
    the body; returns the leg tips in order (left side front to back, then right side front to back)."""
    tips = []
    for side in (-1, 1):
        for i in range(n_side):
            u = i / max(n_side - 1, 1)
            a = math.radians(spread[0] + (spread[1] - spread[0]) * u) + 0.05 * math.sin(t * 3 + i + side)
            bx, by = cx + side * 20, cy - body / 2 + body * u
            dx, dy = side * math.sin(a), -math.cos(a)
            kx, ky = bx + dx * L * 0.5, by + dy * L * 0.5 - 30
            fx, fy = bx + dx * L, by + dy * L + (20 if i == n_side - 1 else 0)
            limb(ctx, [(bx, by), (kx, ky), (fx, fy)], w, col, OUT * 0.6, smooth=False)
            tips.append((fx + dx * 44, fy + dy * 44))
    return tips


def _count_labels(ctx, tips, count, col="#ffd34d"):
    for k, (x, y) in enumerate(tips):
        u = max(0.0, min(1.0, (count - k) * 2.5))
        if u <= 0:
            continue
        s = back_out(u)
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)
        shape(ctx, lambda c: p_ellipse(c, 0, 0, 36, 36), hexc(col), OUT * 0.6, None)
        text(ctx, str(k + 1), 0, 2, 50, "#1a1a1a", 0)
        ctx.restore()


def tc_aphid(ctx, t, p):
    """Giant conifer aphid (Cinara): dark, round, long-legged, SIX legs, long antennae, two little cornicles.
    Side view (origin = feet line, about 420 long) or p["top"] (origin = body centre, legs numbered by "count").
    p: col, mood, look, yawn (0..1), flex (0..1 puffs up), winged, small (a normal tiny green aphid: col green)."""
    col = hexc(p.get("col", "#3d302b"))
    lt = lighter(col, 0.25)
    if p.get("top"):
        tips = _legs_top(ctx, 3, 0, -20, 290, 11, darker(col, 0.9), t, spread=(45, 140), body=90)
        for s in (-1, 1):
            stroke(ctx, [(s * 18, -150), (s * 60, -260), (s * 120, -330)], 5, smooth=True)
        shape(ctx, lambda c: p_ellipse(c, 0, 40, 120, 150), col, OUT, (0.08, 0.1), hi=(0.3, 0.2, 0.3))
        for s in (-1, 1):
            shape(ctx, lambda c, s=s: p_rrect(c, s * 52 - 10, 150, 20, 46, 8), col, OUT * 0.5, None)
        shape(ctx, lambda c: p_ellipse(c, 0, -130, 70, 60), col, OUT, (0.08, 0.1))
        eyes(ctx, 0, -138, 16, 30, p.get("look", (0, -0.3)), p.get("mood", "calm"), p.get("blink", 0), OUT * 0.5, lid=col)
        _count_labels(ctx, tips, p.get("count", 0.0))
        return
    ph = p.get("phase", t * 9)
    wk = 1.0 if p.get("walking") else p.get("walk", 0.0)
    fl = 1.0 + 0.18 * p.get("flex", 0.0)
    for k, (bx, kx, fx) in enumerate(((50, 120, 200), (0, 30, 40), (-50, -150, -230))):   # far legs
        sw = 18 * math.sin(ph + k * 2 + 1) * wk
        limb(ctx, [(bx + 10, -110), (kx + 10, -240), (fx + 20 + sw, 0)], 9, darker(col, 0.75), OUT * 0.5, smooth=False)
    if p.get("winged"):
        shape(ctx, lambda c: p_ellipse(c, -60, -250, 190, 60, 0.35), hexc("#dcecf6"), OUT * 0.5, None, a=0.8)
    ctx.save()
    ctx.translate(-30, -130)
    ctx.scale(fl, fl)
    shape(ctx, lambda c: p_ellipse(c, -20, 0, 140, 110), col, OUT, (0.08, 0.12), hi=(0.3, 0.2, 0.3))
    rg = _rng(5)
    for k in range(18):   # the grey waxy dusting
        x, y = rg.uniform(-130, 80), rg.uniform(-90, 60)
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 5, 4), lt, a=0.7)
    for dx in (-110, -80):
        shape(ctx, lambda c, dx=dx: p_poly(c, [(dx - 10, -80), (dx + 10, -84), (dx - 6, -140), (dx - 18, -136)]), col,
              OUT * 0.5, None)
    ctx.restore()
    shape(ctx, lambda c: p_ellipse(c, 120, -150, 54, 48), col, OUT, (0.08, 0.1))
    for s in (0, 1):
        stroke(ctx, [(140, -190), (190 + s * 30, -300), (250 + s * 50, -330)], 4.5, smooth=True)
    stroke(ctx, [(150, -110), (170, -60)], 5)   # beak
    eyes(ctx, 130, -160, 15, 24, p.get("look", (0.5, 0)), p.get("mood", "calm"), p.get("blink", 0), OUT * 0.5, lid=col)
    yw = p.get("yawn", 0.0)
    if yw > 0.01:
        mouth(ctx, 140, -124, 26, "o", yw, OUT * 0.5)
    for k, (bx, kx, fx) in enumerate(((60, 140, 230), (10, 60, 80), (-40, -140, -250))):   # near legs
        sw = 18 * math.sin(ph + k * 2) * wk
        limb(ctx, [(bx, -100), (kx, -250), (fx + sw, 0)], 11, col, OUT * 0.6, smooth=False)


def tc_tick_top(ctx, t, p):
    """A tick from above (EIGHT legs, four per side, numbered by "count"), head up; origin = body centre."""
    col = C["tick"]
    tips = _legs_top(ctx, 4, 0, -40, 260, 12, darker(col, 0.85), t, spread=(30, 150), body=110)
    shape(ctx, lambda c: p_rrect(c, -22, -190, 44, 70, 14), C["tick_dk"], OUT * 0.7, None)   # mouthparts
    shape(ctx, lambda c: p_smooth(c, [(0, -140), (110, -60), (130, 80), (60, 170), (-60, 170), (-130, 80), (-110, -60)]),
          col, OUT, (0.08, 0.1), hi=(0.3, 0.25, 0.3))
    shape(ctx, lambda c: p_smooth(c, [(0, -140), (80, -80), (60, 10), (-60, 10), (-80, -80)]), C["tick_dk"], OUT * 0.6, None)
    eyes(ctx, 0, -70, 15, 28, p.get("look", (0, -0.3)), p.get("mood", "angry"), p.get("blink", 0), OUT * 0.5,
         lid=C["tick_dk"])
    _count_labels(ctx, tips, p.get("count", 0.0))


def tc_barkbeetle(ctx, t, p):
    """A tiny bark beetle, side view facing right: a short dark-brown cylinder, head tucked under the front,
    clubbed antennae, six short legs. Origin = feet line, about 330 long. p: shake (0..1 head shake), walk, mood."""
    col = C["beetle"]
    ph = p.get("phase", t * 9)
    wk = 1.0 if p.get("walking") else p.get("walk", 0.0)
    for k, x in enumerate((-80, 0, 70)):
        sw = 14 * math.sin(ph + k * 2) * wk
        limb(ctx, [(x + 10, -50), (x + 30, -24), (x + 44 + sw, 0)], 9, darker(col, 0.75), OUT * 0.5, smooth=False)
    shape(ctx, lambda c: p_rrect(c, -160, -150, 290, 110, 55), col, OUT, (0.06, 0.15), hi=(0.25, 0.2, 0.3))
    stroke(ctx, [(-10, -148), (-10, -42)], 4, color=darker(col, 0.7))
    stroke(ctx, [(-140, -110), (-30, -110)], 2.5, color=darker(col, 0.7), a=0.6)
    sh = 0.25 * math.sin(t * 16) * p.get("shake", 0.0)
    ctx.save()
    ctx.translate(140, -90)
    ctx.rotate(sh)
    shape(ctx, lambda c: p_ellipse(c, 10, 0, 46, 42), darker(col, 0.85), OUT, (0.06, 0.1))
    for s in (0, 1):
        stroke(ctx, [(30, -26), (60 + s * 10, -60), (80 + s * 16, -64)], 4)
        shape(ctx, lambda c, s=s: p_ellipse(c, 82 + s * 16, -66, 9, 12), darker(col, 0.8), OUT * 0.4, None)
    eyes(ctx, 18, -6, 12, 18, p.get("look", (0.6, 0)), p.get("mood", "calm"), p.get("blink", 0), OUT * 0.45,
         lid=darker(col, 0.85))
    ctx.restore()
    for k, x in enumerate((-70, 10, 80)):
        sw = 14 * math.sin(ph + k * 2 + 3) * wk
        limb(ctx, [(x, -46), (x + 24, -24), (x + 34 + sw, 0)], 10, col, OUT * 0.5, smooth=False)


def tc_sawdust(ctx, t, p):
    """A small pinch of very fine pale sawdust on the floor, a few grains still drifting down. Origin = floor."""
    rg = _rng(3)
    for k in range(130):
        x = rg.gauss(0, 60)
        y = -abs(rg.gauss(0, 14)) * (1 - min(1.0, abs(x) / 160))
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 3.2, 2.4), hexc("#e8d2a6"))
    for k in range(8):
        x = rg.uniform(-30, 30)
        y = -((t * 60 + k * 50) % 400)
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 3, 3), hexc("#e8d2a6"), a=p.get("drift", 1.0))


def tc_mite(ctx, t, p):
    """A predatory mite from above (pear-shaped, orange-tan, EIGHT legs) eating an egg in front of it.
    Origin = body centre, head to the right. p: eat (0..1 the egg shrinks), egg (bool)."""
    col = hexc("#e0873a")
    ctx.save()
    ctx.rotate(math.pi / 2)
    _legs_top(ctx, 4, 0, 0, 170, 9, darker(col, 0.85), t * 2, spread=(30, 150), body=80)
    ctx.restore()
    shape(ctx, lambda c: p_smooth(c, [(110, 0), (60, -70), (-60, -90), (-130, -40), (-130, 40), (-60, 90), (60, 70)]),
          col, OUT, (0.08, 0.1), hi=(0.3, 0.25, 0.3))
    for s in (-1, 1):
        shape(ctx, lambda c, s=s: p_ellipse(c, 64, s * 22, 14, 15), (1, 1, 1), OUT * 0.45, None)
        flat(ctx, lambda c, s=s: p_ellipse(c, 70, s * 22, 7, 7), INK)
    chew = 6 * math.sin(t * 14)
    stroke(ctx, [(110, -10), (140 + chew, -4)], 6)
    stroke(ctx, [(110, 10), (140 + chew, 4)], 6)
    if p.get("egg", True):
        e = max(0.05, 1 - p.get("eat", 0.0))
        shape(ctx, lambda c: p_ellipse(c, 190, 0, 46 * e, 50 * e), hexc("#f6efd2"), OUT * 0.6, (0.08, 0.1), hi=(0.3, 0.25, 0.3))


def tc_springtail(ctx, t, p):
    """A springtail (grey-blue, long body, forked tail under it, short antennae), side view, origin = feet."""
    col = hexc("#7d8fa8")
    for k, x in enumerate((-30, 10, 50)):
        limb(ctx, [(x, -50), (x + 16, 0)], 7, darker(col, 0.8), OUT * 0.4, smooth=False)
    shape(ctx, lambda c: p_ellipse(c, -10, -80, 120, 44, -0.08), col, OUT * 0.8, (0.06, 0.12))
    stroke(ctx, [(-110, -60), (-60, -24), (20, -20)], 6)
    shape(ctx, lambda c: p_ellipse(c, 110, -96, 38, 34), col, OUT * 0.8, None)
    for s in (0, 1):
        stroke(ctx, [(130, -122), (170 + s * 20, -180)], 4)
    eyes(ctx, 118, -100, 10, 14, (0.6, 0), "calm", p.get("blink", 0), OUT * 0.4, lid=col)


def tc_barklouse(ctx, t, p):
    """A bark louse (psocid): pale, bulging face, long thin antennae, roof-shaped wings. Side view, origin = feet."""
    col = hexc("#cdbfa0")
    for k, x in enumerate((-40, 0, 40)):
        limb(ctx, [(x, -40), (x + 20, -20), (x + 30, 0)], 7, darker(col, 0.8), OUT * 0.4, smooth=False)
    shape(ctx, lambda c: p_ellipse(c, -30, -80, 90, 50), col, OUT * 0.8, (0.06, 0.12))
    shape(ctx, lambda c: p_smooth(c, [(30, -118), (-120, -170), (-190, -120), (-150, -70), (0, -64)]), hexc("#e8f2f8"), OUT * 0.5, None, a=0.75)
    shape(ctx, lambda c: p_ellipse(c, 80, -100, 48, 46), lighter(col, 0.1), OUT * 0.8, (0.06, 0.1))
    for s in (0, 1):
        stroke(ctx, [(96, -140), (150 + s * 30, -230), (210 + s * 40, -250)], 3, smooth=True)
    eyes(ctx, 90, -108, 11, 16, (0.6, 0), "calm", p.get("blink", 0), OUT * 0.4, lid=col)


def tc_spiderlings(ctx, t, p):
    """A cluster of tiny spiderlings (n), each a pale dot with eight short legs, milling about. Origin = centre."""
    n = int(p.get("n", 14))
    rg = _rng(p.get("seed", 6))
    for k in range(n):
        x = rg.uniform(-1, 1) * p.get("w", 160) + 10 * math.sin(t * 2 + k)
        y = rg.uniform(-1, 1) * p.get("h", 70) + 6 * math.cos(t * 2.3 + k)
        r = rg.uniform(8, 12)
        for s in (-1, 1):
            for j in range(4):
                a = math.radians(-50 + j * 34)
                kx, ky = x + s * r * 1.3 * math.cos(a), y + r * 1.3 * math.sin(a) - r * 0.8
                stroke(ctx, [(x, y), (kx, ky), (kx + s * r * 0.9 * math.cos(a), ky + r * 1.6)], 2.6)
        shape(ctx, lambda c, x=x, y=y, r=r: p_ellipse(c, x, y, r, r * 0.9), hexc("#e9d9b0"), OUT * 0.3, None)


def tc_crawlers(ctx, t, p):
    """Scale crawlers: tiny orange-yellow walking specks along a line (x from 0 to p["len"]); p: u (0..1 progress),
    n, gone (0..1 wiped away: they vanish left to right)."""
    n = int(p.get("n", 12))
    ln = p.get("len", 700)
    rg = _rng(4)
    gone = p.get("gone", 0.0)
    for k in range(n):
        x = (k / n) * ln * 0.6 + p.get("u", 0.0) * ln * 0.4 + rg.uniform(-14, 14)
        y = rg.uniform(-24, 24)
        if gone > 0 and x < gone * (ln + 100):
            continue
        for s in (-1, 1):
            for j in range(3):
                stroke(ctx, [(x - 6 + j * 6, y), (x - 8 + j * 6 + 3 * math.sin(t * 20 + k + j), y + s * 12)], 2.5)
        shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 10, 7), hexc("#f0a830"), OUT * 0.3, None)


def tc_slf_eggs(ctx, t, p):
    """A spotted lanternfly egg mass: a grey, cracked, mud-like smear (about 340 x 130 here = about an inch on the
    bark close-up). Origin = centre. p: off (0..1 scraped off: slides right and away)."""
    off = p.get("off", 0.0)
    ctx.save()
    ctx.translate(220 * ease(off), 40 * ease(off))
    shape(ctx, lambda c: p_blob(c, 0, 0, 170, 64, 0.1, 7, 20), C["mud"], OUT * 0.8, (0.06, 0.15), hi=(0.25, 0.2, 0.25))
    rg = _rng(8)
    for k in range(5):   # rows hinted under the cover
        y = -36 + k * 18
        stroke(ctx, [(-130 + abs(k - 2) * 14, y), (130 - abs(k - 2) * 14, y + 4)], 3, color=C["mud_dk"], a=0.5)
    for k in range(7):   # cracks
        x = rg.uniform(-130, 120)
        y = rg.uniform(-40, 30)
        stroke(ctx, [(x, y), (x + rg.uniform(10, 30), y + rg.uniform(-14, 14)), (x + rg.uniform(30, 50), y + rg.uniform(-10, 18))],
               3.5, color=INK, a=0.8)
    ctx.restore()


def tc_slf_nymphs(ctx, t, p):
    """A few early spotted lanternfly nymphs (black, white spots, long legs). p: n, gone (0..1 fade), hop."""
    n = int(p.get("n", 4))
    a = 1 - p.get("gone", 0.0)
    if a <= 0.01:
        return
    for k in range(n):
        x = k * 110 - (n - 1) * 55
        y = -abs(30 * math.sin(t * 4 + k * 1.3)) * p.get("hop", 1.0)
        for s in (-1, 1):
            for j in range(3):
                stroke(ctx, [(x - 10 + j * 12, y - 20), (x - 20 + j * 18, y - 40), (x - 30 + j * 26 + s * 4, y)], 4, a=a)
        shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y - 34, 30, 22), hexc("#18181c"), OUT * 0.4, None, a=a)
        for (dx, dy) in ((-14, -42), (4, -48), (16, -30), (-4, -26)):
            flat(ctx, lambda c, x=x, y=y, dx=dx, dy=dy: p_ellipse(c, x + dx, y + dy, 4, 4), (1, 1, 1), a=a)


def tc_adelgid(ctx, t, p):
    """White cottony adelgid tufts on bark (n), origin = centre of the patch. p: poke (0..1 one tuft wobbles)."""
    rg = _rng(p.get("seed", 5))
    n = int(p.get("n", 9))
    for k in range(n):
        x, y = rg.uniform(-260, 260), rg.uniform(-200, 200)
        r = rg.uniform(26, 48)
        wob = 1 + (0.15 * math.sin(t * 18) * p.get("poke", 0.0) if k == 0 else 0)
        shape(ctx, lambda c, x=x, y=y, r=r, k=k, wob=wob: p_blob(c, x, y, r * wob, r * 0.85, 0.22, k + 3, 16),
              hexc("#f7f7f2"), OUT * 0.45, (0.06, 0.12), shade_k=0.9)
        for j in range(3):
            a2 = rg.uniform(0, 6.28)
            stroke(ctx, [(x, y), (x + r * 1.4 * math.cos(a2), y + r * 1.4 * math.sin(a2))], 2, color=(1, 1, 1), a=0.8)


def tc_nest(ctx, t, p):
    """An old bird nest: a woven twig cup, straggly ends. Origin = bottom centre, about 300 wide."""
    shape(ctx, lambda c: p_smooth(c, [(-150, -120), (150, -120), (130, -40), (60, 0), (-60, 0), (-130, -40)]), C["nest"],
          OUT, (0.06, 0.12))
    flat(ctx, lambda c: p_ellipse(c, 0, -118, 130, 26), C["nest_dk"])
    rg = _rng(2)
    for k in range(26):
        y = rg.uniform(-115, -10)
        x0 = rg.uniform(-150, 0)
        stroke(ctx, [(x0, y), (x0 + rg.uniform(80, 180), y + rg.uniform(-14, 14))], 4, color=C["nest_dk"])
    for k in range(6):
        x = rg.uniform(-160, 160)
        stroke(ctx, [(x, -100), (x + rg.uniform(-60, 60), -150 - rg.uniform(0, 40))], 4, color=C["nest_dk"])


def tc_dog(ctx, t, p):
    """A friendly dog (side view, facing right) sniffing; origin = feet. p: sniff (0..1 head bobs), wag."""
    col = hexc("#c98a4a")
    dk = darker(col, 0.75)
    for x in (-150, -90, 90, 150):
        limb(ctx, [(x, -170), (x, 0)], 34, dk if x in (-90, 90) else col, OUT * 0.7)
    wag = 0.4 * math.sin(t * 12) * p.get("wag", 1.0)
    ctx.save()
    ctx.translate(-200, -230)
    ctx.rotate(-0.8 + wag)
    limb(ctx, [(0, 0), (-40, -60), (-60, -110)], 18, col, OUT * 0.7)
    ctx.restore()
    shape(ctx, lambda c: p_rrect(c, -230, -300, 430, 150, 70), col, OUT, (0.06, 0.15))
    sn = 8 * math.sin(t * 16) * p.get("sniff", 1.0)
    ctx.save()
    ctx.translate(220, -310 + sn)
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 90, 80), col, OUT, (0.06, 0.12))
    shape(ctx, lambda c: p_rrect(c, 40, -10, 110, 70, 30), lighter(col, 0.3), OUT, None)
    shape(ctx, lambda c: p_ellipse(c, 148, 6, 20, 16), INK, OUT * 0.4, None)
    shape(ctx, lambda c: p_smooth(c, [(-50, -50), (-10, -60), (-30, 60), (-80, 50)]), dk, OUT * 0.8, None)
    shape(ctx, lambda c: p_ellipse(c, 34, -24, 12, 14), (1, 1, 1), OUT * 0.45, None)
    flat(ctx, lambda c: p_ellipse(c, 38, -20, 6, 7), INK)
    ctx.restore()


def tc_specks(ctx, t, p):
    """Generic tiny specks (n), drifting; p: col, w, h, r, sleep (Z's)."""
    rg = _rng(p.get("seed", 3))
    for k in range(int(p.get("n", 8))):
        x = rg.uniform(-1, 1) * p.get("w", 200) + 4 * math.sin(t * 2 + k)
        y = rg.uniform(-1, 1) * p.get("h", 100)
        r = p.get("r", 9)
        shape(ctx, lambda c, x=x, y=y, r=r: p_ellipse(c, x, y, r, r * 0.8), hexc(p.get("col", "#3a2a24")), OUT * 0.3, None,
              a=p.get("a", 1.0))


def tc_fall(ctx, t, p):
    """Specks falling out of a shaken tree: within width w, from y = -h to 0 (the sheet), looping; p: on, n."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    rg = _rng(p.get("seed", 5))
    h, w = p.get("h", 700), p.get("w", 500)
    for k in range(int(p.get("n", 18))):
        x = rg.uniform(-w / 2, w / 2)
        sp = rg.uniform(0.6, 1.0)
        u = ((t * sp * 0.9) + rg.random()) % 1.0
        y = -h + h * u * u
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 7, 6), hexc(p.get("col", "#2a1f1a")), a=on)
    for k in range(int(p.get("landed", 0))):
        x = rg.uniform(-w / 2, w / 2)
        flat(ctx, lambda c, x=x: p_ellipse(c, x, -4, 7, 5), hexc(p.get("col", "#2a1f1a")), a=on)


def tc_zz(ctx, t, p):
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    x0, y0, px = p.get("x", 0), p.get("y", 0), p.get("px", 60)
    for k in range(3):
        u = (t * 0.5 + k / 3) % 1
        text(ctx, "Z", x0 + 30 * k + 10 * math.sin(t + k), y0 - 90 * u - k * 20, px * (0.6 + 0.3 * k), "#ffffff", 5,
             a=on * (1 - u))


# ================================================================================================ props

def _shears(ctx, t, p):
    """Pruning shears (bypass), blades to the right; p: snip (0..1 closes the blades)."""
    o = 0.45 * (1 - ease(p.get("snip", 0.0)))
    for s in (-1, 1):
        ctx.save()
        ctx.rotate(s * o / 2)
        shape(ctx, lambda c, s=s: p_smooth(c, [(-20, s * 6), (60, s * 18), (190, s * 4), (200, -s * 4), (60, -s * 2)]),
              PAL["steel"], OUT * 0.7, (0, 0.2), hi=(0.3, 0.3, 0.2))
        shape(ctx, lambda c, s=s: p_rrect(c, -260, s * 12 - 18, 240, 36, 18), C["red"], OUT * 0.8, (0, 0.2))
        ctx.restore()
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 16, 16), PAL["steel_dk"], OUT * 0.6, None)


def _slipper(ctx, t, p):
    """A fuzzy slipper, sole down, toe right; origin = middle of the sole."""
    shape(ctx, lambda c: p_smooth(c, [(-200, 0), (-210, -60), (-120, -90), (60, -110), (190, -70), (210, -10), (160, 10),
                                      (-160, 10)]), hexc("#8a5ac8"), OUT, (0.06, 0.2), hi=(0.3, 0.25, 0.2))
    shape(ctx, lambda c: p_rrect(c, -215, -6, 430, 34, 16), hexc("#e9e2f2"), OUT * 0.8, None)
    flat(ctx, lambda c: p_ellipse(c, 90, -100, 60, 22), hexc("#f2ecfa"))


def _aerosol(ctx, t, p):
    """An aerosol bug spray can; p: flame (0..1 the label flips to a flame symbol), aim (nozzle to the right)."""
    shape(ctx, lambda c: p_rrect(c, -80, -380, 160, 380, 26), hexc("#3a8a3a"), OUT, (0.08, 0.1), hi=(0.3, 0.2, 0.2))
    shape(ctx, lambda c: p_poly(c, [(-80, -380), (80, -380), (50, -420), (-50, -420)]), PAL["steel"], OUT, None)
    shape(ctx, lambda c: p_rrect(c, -30, -460, 60, 44, 10), (0.95, 0.95, 0.95), OUT * 0.8, None)
    flat(ctx, lambda c: p_ellipse(c, 34, -440, 6, 6), INK)
    fl = p.get("flame", 0.0)
    sx = abs(math.cos(math.pi * min(1.0, fl)))
    ctx.save()
    ctx.translate(0, -200)
    ctx.scale(max(0.02, sx), 1)
    if fl < 0.5:
        shape(ctx, lambda c: p_rrect(c, -64, -90, 128, 180, 10), (0.97, 0.97, 0.92), OUT * 0.6, None)
        flat(ctx, lambda c: p_ellipse(c, 0, -10, 30, 22), INK)
        for s in (-1, 1):
            for j in range(3):
                stroke(ctx, [(s * 20, -20 + j * 14), (s * 44, -30 + j * 20)], 4)
        stroke(ctx, [(-50, -60), (50, 50)], 10, color=C["red"])
    else:
        shape(ctx, lambda c: p_poly(c, [(0, -90), (80, 60), (-80, 60)]), hexc("#ff9f1c"), OUT * 0.8, None)
        shape(ctx, lambda c: p_smooth(c, [(0, -50), (26, 0), (18, 40), (-18, 40), (-26, 0)]), C["red"], OUT * 0.5, None)
    ctx.restore()


def _foamcan(ctx, t, p):
    """A can of spray-foam insulation with its long straw nozzle and a squiggle of foam."""
    shape(ctx, lambda c: p_rrect(c, -80, -400, 160, 400, 24), hexc("#f2b632"), OUT, (0.08, 0.1), hi=(0.3, 0.2, 0.2))
    shape(ctx, lambda c: p_rrect(c, -60, -300, 120, 140, 10), (0.97, 0.97, 0.92), OUT * 0.6, None)
    for k in range(3):
        stroke(ctx, [(-40, -270 + k * 34), (40, -270 + k * 34)], 6, color=hexc("#9aa3ab"))
    shape(ctx, lambda c: p_rrect(c, -30, -450, 60, 52, 10), INK, OUT * 0.5, None)
    stroke(ctx, [(20, -430), (220, -520)], 12)
    stroke(ctx, [(20, -430), (220, -520)], 6, color=hexc("#e9e9e9"))
    shape(ctx, lambda c: p_smooth(c, [(220, -520), (260, -560), (300, -520), (330, -560), (320, -500), (270, -490)]),
          hexc("#f2dc9a"), OUT * 0.6, (0.06, 0.1))


def _pingpong(ctx, t, p):
    shape(ctx, lambda c: p_ellipse(c, 0, -100, 100, 100), (0.98, 0.98, 0.97), OUT, (0.1, 0.12), hi=(0.3, 0.25, 0.3))


def _ruler2(ctx, t, p):
    """A ruler with inch marks; p: label (text under the bracket), mark (0..1 a yellow bracket over p["span"] px)."""
    w = p.get("w", 900)
    shape(ctx, lambda c: c.rectangle(-w / 2, -60, w, 120), hexc("#f2d36b"), OUT, (0, 0.2))
    ppi = p.get("ppi", 160)
    k = 0
    x = -w / 2 + 20
    while x < w / 2 - 10:
        ln = 50 if k % 8 == 0 else (34 if k % 4 == 0 else 20)
        stroke(ctx, [(x, -60), (x, -60 + ln)], 4)
        x += ppi / 8
        k += 1
    m = p.get("mark", 0.0)
    if m > 0.01:
        span = p.get("span", 240) * ease(m)
        x0 = -w / 2 + 20
        stroke(ctx, [(x0, -100), (x0 + span, -100)], 14)
        stroke(ctx, [(x0, -100), (x0 + span, -100)], 8, color=hexc("#ffd34d"))
        for xx in (x0, x0 + span):
            stroke(ctx, [(xx, -124), (xx, -76)], 10)
    if p.get("label") and m > 0.6:
        text(ctx, p["label"], -w / 2 + 20 + p.get("span", 240) / 2, -170, 64, "#ffd34d", 7)


def _zipbag(ctx, t, p):
    """A zip bag with clear hand-sanitizer gel in it (label HAND SANITIZER)."""
    shape(ctx, lambda c: p_rrect(c, -170, -360, 340, 360, 20), (0.86, 0.95, 1.0), OUT * 0.8, None, a=0.55)
    flat(ctx, lambda c: p_rrect(c, -160, -180, 320, 172, 16), hexc("#8fd6e8"), a=0.65)
    shape(ctx, lambda c: c.rectangle(-170, -360, 340, 30), hexc("#5ab0ff"), OUT * 0.6, None)
    text(ctx, p.get("label", "HAND SANITIZER"), 0, -250, 40, "#1f5f8b", 0)
    for k in range(4):
        flat(ctx, lambda c, k=k: p_ellipse(c, -100 + k * 60, -120 + (k % 2) * 30, 10, 10), (1, 1, 1), a=0.7)


def _scraper(ctx, t, p):
    """A plastic card used as a scraper, held at an angle; origin = the scraping edge."""
    shape(ctx, lambda c: p_rrect(c, 0, -120, 260, 160, 14), hexc("#2c6fbf"), OUT * 0.8, (0.05, 0.15))
    flat(ctx, lambda c: c.rectangle(0, -90, 260, 26), INK, a=0.8)
    stroke(ctx, [(30, 0), (140, 0)], 6, color=(1, 1, 1), a=0.6)


def _phone(ctx, t, p):
    """A phone showing a generic state agriculture department report screen (no real logo)."""
    shape(ctx, lambda c: p_rrect(c, -170, -640, 340, 640, 40), hexc("#22262e"), OUT, None)
    flat(ctx, lambda c: p_rrect(c, -146, -610, 292, 560, 20), hexc("#eef3f6"))
    flat(ctx, lambda c: c.rectangle(-146, -590, 292, 100), hexc("#2f7a4a"))
    text(ctx, p.get("title", "STATE AG DEPT"), 0, -540, 42, "#ffffff", 0)
    shape(ctx, lambda c: p_ellipse(c, 0, -380, 70, 46), hexc("#9aa3ab"), OUT * 0.4, None)
    stroke(ctx, [(-40, -380), (40, -380)], 6, color=INK)
    for k in range(3):
        stroke(ctx, [(-110, -290 + k * 40), (110 - k * 30, -290 + k * 40)], 8, color=hexc("#b9c3ca"))
    shape(ctx, lambda c: p_rrect(c, -110, -170, 220, 70, 30), C["red"], OUT * 0.5, None)
    text(ctx, p.get("button", "REPORT"), 0, -135, 40, "#ffffff", 0)


def _logs(ctx, t, p):
    """Firewood: n logs stacked (2 = an armful, 9 = a big pile); origin = floor."""
    n = int(p.get("n", 3))
    k = 0
    row = 0
    while k < n:
        per = max(1, 4 - row)
        for j in range(per):
            if k >= n:
                break
            x = (j - (per - 1) / 2) * 150
            y = -55 - row * 100
            shape(ctx, lambda c, x=x, y=y: p_rrect(c, x - 80, y - 50, 160, 100, 46), hexc("#8a5a34"), OUT * 0.8, (0, 0.2))
            shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x + 60, y, 34, 46), C["cut"], OUT * 0.6, None)
            ctx.new_sub_path()
            ctx.arc(x + 60, y, 18, 0, 2 * math.pi)
            ctx.set_source_rgb(*C["ring"])
            ctx.set_line_width(3)
            ctx.stroke()
            k += 1
        row += 1


def _thermostat(ctx, t, p):
    """A round wall thermostat; p: glow (0..1 orange warmth), dial (0..1 turns up)."""
    g = p.get("glow", 0.0)
    if g > 0.01:
        glow(ctx, 0, 0, 260, hexc("#ff9f40"), 0.6 * g)
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 150, 150), (0.96, 0.95, 0.92), OUT, (0.06, 0.1))
    ctx.new_sub_path()
    ctx.arc(0, 0, 110, math.radians(140), math.radians(140 + 260 * max(0.15, p.get("dial", 0.3))))
    ctx.set_source_rgb(*_mix(hexc("#5ab0ff"), hexc("#ff7a30"), p.get("dial", 0.3)))
    ctx.set_line_width(22)
    ctx.stroke()
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 70, 70), hexc("#2a2f3a"), OUT * 0.6, None)
    a = math.radians(140 + 260 * p.get("dial", 0.3))
    stroke(ctx, [(0, 0), (60 * math.cos(a), 60 * math.sin(a))], 8, color=(1, 1, 1))


def _candycane(ctx, t, p):
    pts = [(0, 0), (0, -260), (10, -310), (50, -330), (90, -310), (100, -270)]
    stroke(ctx, pts, 46, smooth=True)
    stroke(ctx, pts, 30, smooth=True, color=(1, 1, 1))
    ctx.save()
    ctx.set_dash([18, 18])
    stroke(ctx, pts, 30, smooth=True, color=C["red"])
    ctx.restore()


def _gift_prop(ctx, t, p):
    _gift(ctx, 0, 0, p.get("w", 220), p.get("h", 170), hexc(p.get("col", "#c0392b")), hexc(p.get("rib", "#f2c14e")))
    if p.get("stain", 0.0) > 0.01:
        flat(ctx, lambda c: p_blob(c, -40, -60, 46 * p["stain"], 26 * p["stain"], 0.25, 3), hexc("#7a1f6e"), a=0.85)


def _sock(ctx, t, p):
    shape(ctx, lambda c: p_poly(c, [(-50, -300), (50, -300), (50, -90), (130, -40), (110, 10), (-20, 0), (-50, -60)]),
          C["red"], OUT, (0.06, 0.1))
    shape(ctx, lambda c: c.rectangle(-60, -320, 120, 60), (1, 1, 1), OUT, None)


def _tub(ctx, t, p):
    shape(ctx, lambda c: p_poly(c, [(-150, -260), (150, -260), (130, 0), (-130, 0)]), (0.92, 0.95, 0.97), OUT, (0.05, 0.1))
    shape(ctx, lambda c: p_rrect(c, -160, -290, 320, 40, 12), hexc("#5ab0ff"), OUT * 0.8, None)
    shape(ctx, lambda c: p_rrect(c, -110, -200, 220, 80, 8), hexc("#f2d36b"), OUT * 0.5, None)
    text(ctx, p.get("label", "CRICKETS"), 0, -160, 44, "#3a2a24", 0)


def _tongs(ctx, t, p):
    o = 0.12 * (1 - p.get("grip", 1.0))
    for s in (-1, 1):
        ctx.save()
        ctx.rotate(s * o)
        stroke(ctx, [(0, 0), (300, s * 20), (380, s * 8)], 16)
        stroke(ctx, [(0, 0), (300, s * 20), (380, s * 8)], 9, color=PAL["steel"])
        ctx.restore()


def _cabinet(ctx, t, p):
    """A filing cabinet, three drawers; p: open (0..1 the top drawer slides out to the right... toward camera)."""
    shape(ctx, lambda c: c.rectangle(-170, -640, 340, 640), PAL["cabinet"], OUT, (0.06, 0.05))
    for k in range(3):
        y = -620 + k * 205
        o = p.get("open", 0.0) * 140 if k == 0 else 0
        shape(ctx, lambda c, y=y, o=o: c.rectangle(-150 + o * 0.3, y + o * 0.1, 300, 180), PAL["cabinet_dk"] if k else
              lighter(PAL["cabinet"], 0.1), OUT * 0.7, None)
        shape(ctx, lambda c, y=y, o=o: p_rrect(c, -50 + o * 0.3, y + 70 + o * 0.1, 100, 26, 10), PAL["steel"], OUT * 0.5, None)
        shape(ctx, lambda c, y=y, o=o: c.rectangle(-40 + o * 0.3, y + 26 + o * 0.1, 80, 30), PAL["paper"], OUT * 0.4, None)


def _plant(ctx, t, p):
    """A houseplant in a pot; origin = floor."""
    shape(ctx, lambda c: p_poly(c, [(-110, -200), (110, -200), (85, 0), (-85, 0)]), hexc("#c0623c"), OUT, (0.08, 0.1))
    shape(ctx, lambda c: p_rrect(c, -125, -230, 250, 40, 10), hexc("#d07a50"), OUT * 0.8, None)
    for k in range(7):
        a = math.radians(-160 + k * 23)
        ex, ey = 260 * math.cos(a), -230 + 280 * math.sin(a) * 0.9 - 60
        stroke(ctx, [(0, -230), (ex * 0.5, ey * 0.7 - 40), (ex, ey)], 6, smooth=True, color=hexc("#3d7a3a"))
        shape(ctx, lambda c, ex=ex, ey=ey, a=a: p_ellipse(c, ex, ey, 70, 30, a), hexc("#4fa860"), OUT * 0.6, (0.06, 0.12))


def _sheet(ctx, t, p):
    """A white bedsheet spread on the floor (perspective); origin = its centre."""
    shape(ctx, lambda c: p_poly(c, [(-520, -60), (520, -60), (600, 80), (-600, 80)]), (0.98, 0.98, 0.97), OUT, None)
    for k in range(3):
        stroke(ctx, [(-400 + k * 300, -50), (-430 + k * 320, 70)], 4, color=hexc("#d9dde2"))
    rg = _rng(4)
    for k in range(int(p.get("specks", 0))):
        x, y = rg.uniform(-440, 440), rg.uniform(-40, 60)
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 7, 5), hexc("#2a1f1a"))


def _canvac(ctx, t, p):
    """A canister vacuum with a long hose to a plain nozzle (no brush); origin = floor under the canister.
    p: tip ([x, y] the nozzle end, relative), suck (0..1 lines into the nozzle)."""
    tx, ty = p.get("tip", (500, -400))
    shape(ctx, lambda c: p_rrect(c, -190, -200, 330, 200, 70), C["red"], OUT, (0.06, 0.12), hi=(0.3, 0.2, 0.2))
    for s in (-1, 1):
        shape(ctx, lambda c, s=s: p_ellipse(c, -30 + s * 110, -10, 34, 34), INK, OUT * 0.4, None)
    pts = [(140, -120), (260, -60), (tx * 0.6, ty * 0.3), (tx - 120, ty + 30)]
    stroke(ctx, pts, 34, smooth=True)
    stroke(ctx, pts, 22, smooth=True, color=hexc("#7d8a93"))
    ang = math.atan2(ty - (ty + 30), tx - (tx - 120))
    ctx.save()
    ctx.translate(tx - 120, ty + 30)
    ctx.rotate(ang)
    shape(ctx, lambda c: p_rrect(c, 0, -14, 130, 28, 10), PAL["steel"], OUT * 0.7, None)
    shape(ctx, lambda c: p_poly(c, [(120, -20), (170, -34), (170, 34), (120, 20)]), hexc("#2c3440"), OUT * 0.7, None)
    ctx.restore()
    if p.get("suck", 0.0) > 0.01:
        for k in range(4):
            u = (t * 2 + k / 4) % 1
            r = 90 * (1 - u)
            a2 = ang + math.pi + (k - 1.5) * 0.4
            x, y = tx + 40 * math.cos(ang) + r * math.cos(a2 + math.pi), ty + 40 * math.sin(ang) + r * math.sin(a2 + math.pi)
            stroke(ctx, [(x, y), (x + 18 * math.cos(ang), y + 18 * math.sin(ang))], 4, color=(1, 1, 1), a=p["suck"])


def _brushhead(ctx, t, p):
    """A rotating-brush (beater bar) floor head, on its own; origin = floor."""
    shape(ctx, lambda c: p_rrect(c, -200, -90, 400, 90, 20), hexc("#5b6b7a"), OUT, (0.05, 0.15))
    for k in range(9):
        stroke(ctx, [(-170 + k * 42, -6), (-160 + k * 42, 16)], 6, color=hexc("#e2b84a"))
    stroke(ctx, [(0, -90), (40, -300)], 26)
    stroke(ctx, [(0, -90), (40, -300)], 16, color=PAL["steel"])


def _icon(ctx, t, p):
    """Little icons: tooth (bite), sting, germ (disease), check, x."""
    k = p.get("icon", "tooth")
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 120, 120), (0.97, 0.97, 0.95), OUT, None)
    if k == "tooth":
        shape(ctx, lambda c: p_smooth(c, [(-50, -50), (0, -64), (50, -50), (46, 10), (26, 60), (6, 20), (-6, 20),
                                          (-26, 60), (-46, 10)]), (1, 1, 1), OUT * 0.8, (0.06, 0.1))
    elif k == "sting":
        shape(ctx, lambda c: p_poly(c, [(-60, -40), (60, -10), (-60, 20)]), hexc("#2a2a2a"), OUT * 0.6, None)
        shape(ctx, lambda c: p_ellipse(c, -60, -10, 30, 40), hexc("#f2c14e"), OUT * 0.6, None)
    elif k == "germ":
        for j in range(8):
            a = j * math.pi / 4
            stroke(ctx, [(46 * math.cos(a), 46 * math.sin(a)), (76 * math.cos(a), 76 * math.sin(a))], 8)
            shape(ctx, lambda c, a=a: p_ellipse(c, 80 * math.cos(a), 80 * math.sin(a), 12, 12), hexc("#6abf4a"), OUT * 0.4, None)
        shape(ctx, lambda c: p_blob(c, 0, 0, 52, 48, 0.1, 2), hexc("#6abf4a"), OUT * 0.7, None)
    xo = p.get("x", 0.0)
    if xo > 0.01:
        for (a, b) in (((-80, -80), (80, 80)), ((80, -80), (-80, 80))):
            e = (a[0] + (b[0] - a[0]) * min(1.0, xo), a[1] + (b[1] - a[1]) * min(1.0, xo))
            stroke(ctx, [a, e], 30)
            stroke(ctx, [a, e], 18, color=C["red"])


def _armchair(ctx, t, p):
    col = hexc(p.get("col", "#4a6a8a"))
    shape(ctx, lambda c: p_rrect(c, -260, -560, 520, 420, 90), col, OUT, (0.06, 0.1))
    shape(ctx, lambda c: p_rrect(c, -300, -320, 600, 200, 60), lighter(col, 0.12), OUT, (0.06, 0.12))
    for s in (-1, 1):
        shape(ctx, lambda c, s=s: p_rrect(c, s * 270 - 70, -420, 140, 320, 60), darker(col, 0.9), OUT, (0.06, 0.1))
        stroke(ctx, [(s * 230, -100), (s * 240, 0)], 18)


def _shrubtwig(ctx, t, p):
    """A short fir twig with an egg case on it (prop size, for snipping and tucking); origin = twig centre."""
    rg = _rng(4)
    _needled(ctx, [(-220, 10), (0, 0), (220, -16)], C["fir"], rg, 10, 50, wood=True, th=16)
    ctx.save()
    ctx.scale(0.55, 0.55)
    tc_ooth(ctx, t, {"kind": p.get("case", "chinese")})
    ctx.restore()


def _grain(ctx, t, p):
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 120, 44, 0.1), (0.98, 0.97, 0.93), OUT * 0.8, (0.06, 0.12), hi=(0.3, 0.25, 0.3))


def _lens(ctx, t, p):
    """A big magnifying glass; origin = lens centre; handle down-right."""
    stroke(ctx, [(140, 140), (330, 330)], 54)
    stroke(ctx, [(140, 140), (330, 330)], 36, color=PAL["wood_dk"])
    flat(ctx, lambda c: p_ellipse(c, 0, 0, 200, 200), (0.85, 0.95, 1.0), a=0.18)
    ctx.new_sub_path()
    ctx.arc(0, 0, 200, 0, 2 * math.pi)
    ctx.set_source_rgb(*INK)
    ctx.set_line_width(30)
    ctx.stroke()
    ctx.arc(0, 0, 200, 0, 2 * math.pi)
    ctx.set_source_rgb(*PAL["steel"])
    ctx.set_line_width(18)
    ctx.stroke()
    flat(ctx, lambda c: p_ellipse(c, -80, -100, 50, 24, -0.6), (1, 1, 1), a=0.5)


def _sign(ctx, t, p):
    """A picket sign on a stick; p: text, col."""
    stroke(ctx, [(0, 0), (0, -420)], 22)
    stroke(ctx, [(0, 0), (0, -420)], 13, color=PAL["wood"])
    shape(ctx, lambda c: p_rrect(c, -190, -560, 380, 180, 12), hexc(p.get("col", "#ffffff")), OUT, (0.04, 0.1))
    text(ctx, p.get("text", "SIGN"), 0, -470, p.get("px", 72), p.get("tcol", "#1a1a1a"), 0)


def _flashlight(ctx, t, p):
    """A flashlight pointing right with its beam; origin = the lens."""
    on = p.get("beam", 1.0)
    if on > 0.01:
        ctx.save()
        ctx.move_to(0, -30)
        ctx.line_to(700, -200)
        ctx.line_to(700, 200)
        ctx.line_to(0, 30)
        ctx.close_path()
        ctx.set_source_rgba(1, 0.97, 0.7, 0.3 * on)
        ctx.fill()
        ctx.restore()
    shape(ctx, lambda c: p_rrect(c, -260, -26, 220, 52, 14), hexc("#2c3440"), OUT * 0.8, None)
    shape(ctx, lambda c: p_poly(c, [(-50, -30), (0, -46), (0, 46), (-50, 30)]), PAL["steel"], OUT * 0.8, None)


def _table(ctx, t, p):
    """A side table with one drawer; p: open (0..1)."""
    shape(ctx, lambda c: c.rectangle(-260, -420, 520, 40), PAL["desk"], OUT, None)
    shape(ctx, lambda c: c.rectangle(-240, -380, 480, 120), PAL["desk_dk"], OUT, None)
    o = p.get("open", 0.0) * 60
    shape(ctx, lambda c: c.rectangle(-180 - o * 0.2, -366 + o, 360, 92), PAL["desk"], OUT * 0.8, None)
    flat(ctx, lambda c: p_rrect(c, -40 - o * 0.2, -330 + o, 80, 18, 8), PAL["steel"])
    for x in (-220, 220):
        stroke(ctx, [(x, -260), (x, 0)], 34)
        stroke(ctx, [(x, -260), (x, 0)], 20, color=PAL["desk_dk"])


def _hosewand(ctx, t, p):
    """A vacuum hose wand held in the hand: the wand points right to a plain nozzle; the hose trails down-left."""
    stroke(ctx, [(0, 0), (-60, 160), (-200, 400), (-260, 700)], 30, smooth=True)
    stroke(ctx, [(0, 0), (-60, 160), (-200, 400), (-260, 700)], 18, smooth=True, color=hexc("#7d8a93"))
    shape(ctx, lambda c: p_rrect(c, -10, -14, 300, 28, 10), PAL["steel"], OUT * 0.7, None)
    shape(ctx, lambda c: p_poly(c, [(290, -20), (350, -34), (350, 34), (290, 20)]), hexc("#2c3440"), OUT * 0.7, None)


PROPS = {"shears": _shears, "hosewand": _hosewand, "slipper": _slipper, "aerosol": _aerosol, "foamcan": _foamcan, "pingpong": _pingpong,
         "ruler": _ruler2, "zipbag": _zipbag, "scraper": _scraper, "phone": _phone, "logs": _logs,
         "thermostat": _thermostat, "candycane": _candycane, "gift": _gift_prop, "sock": _sock, "tub": _tub,
         "tongs": _tongs, "cabinet": _cabinet, "plant": _plant, "sheet": _sheet, "canvac": _canvac,
         "brushhead": _brushhead, "icon": _icon, "armchair": _armchair, "shrubtwig": _shrubtwig, "grain": _grain,
         "lens": _lens, "sign": _sign, "flashlight": _flashlight, "table": _table}


def tc_prop(ctx, t, p):
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    s = back_out(min(1.0, on))
    ctx.save()
    ctx.scale(s, s)
    PROPS[p["kind"]](ctx, t, p)
    ctx.restore()


# ================================================================================================ boards, maps, gags

_MAPS = {   # plain shapes (no flags), in a 760 x 760 card
    "NORWAY": [(-40, 300), (-150, 240), (-200, 120), (-170, 20), (-90, -60), (-10, -150), (80, -230), (190, -300),
               (260, -310), (250, -250), (150, -200), (80, -100), (40, 0), (10, 120), (40, 230)],
    "NETHERLANDS": [(-200, 220), (-230, 120), (-160, 40), (-140, -80), (-60, -200), (60, -240), (190, -200), (220, -60),
                    (160, 40), (190, 160), (60, 260), (-60, 240)],
    "USA": [(-330, -150), (-150, -170), (60, -160), (200, -170), (260, -120), (330, -150), (320, -40), (240, 20),
            (220, 120), (140, 140), (60, 150), (0, 210), (-80, 140), (-200, 130), (-300, 60), (-340, -40)],
}


def tc_map(ctx, t, p):
    """A plain map card with a pin: p place (NORWAY | NETHERLANDS | USA), pin (0..1 drops in), px, py (pin spot),
    county (0..1 a dashed county line on the USA map), ships (0..1 two little ships arriving from the east), label."""
    place = p.get("place", "NORWAY")
    shape(ctx, lambda c: p_rrect(c, -380, -380, 760, 760, 30), hexc("#9cc3d8"), OUT, None)
    shape(ctx, lambda c: p_poly(c, _MAPS[place]), hexc("#d9cfb2"), OUT, (0.05, 0.1))
    if p.get("county", 0.0) > 0.01:
        ctx.save()
        ctx.set_dash([18, 12])
        stroke(ctx, [(60, -160), (70, -40), (40, 60), (60, 150)][:max(2, int(4 * p["county"] + 0.99))], 7, color=C["red"])
        ctx.restore()
    if p.get("ships", 0.0) > 0.01:
        for k in range(2):
            u = ease(p["ships"])
            tc_ship(ctx, t, {"x": 420 - 100 * u + k * 40, "y": -40 + k * 110, "s": 0.5})
    pin = p.get("pin", 1.0)
    if pin > 0:
        px, py = p.get("px", 0), p.get("py", 0)
        dy = -260 * (1 - back_out(min(1.0, pin)))
        shape(ctx, lambda c: (c.move_to(px, py + dy), c.curve_to(px - 60, py - 70 + dy, px - 50, py - 130 + dy, px, py - 130 + dy),
                              c.curve_to(px + 50, py - 130 + dy, px + 60, py - 70 + dy, px, py + dy)), C["red"], OUT, (0.1, 0.1))
        flat(ctx, lambda c: p_ellipse(c, px, py - 92 + dy, 20, 20), (1, 1, 1))
    if p.get("label", place):
        text(ctx, p.get("label", place), 0, 330, 64, "#ffffff")


def tc_ship(ctx, t, p):
    x, y, s = p.get("x", 0), p.get("y", 0), p.get("s", 1.0)
    ctx.save()
    ctx.translate(x, y + 4 * math.sin(t * 3 + x))
    ctx.scale(s, s)
    shape(ctx, lambda c: p_poly(c, [(-100, 0), (100, 0), (70, 50), (-70, 50)]), hexc("#7a4a2a"), OUT * 0.8, None)
    stroke(ctx, [(0, 0), (0, -160)], 8)
    shape(ctx, lambda c: p_poly(c, [(6, -150), (90, -40), (6, -30)]), (1, 1, 1), OUT * 0.6, None)
    shape(ctx, lambda c: p_poly(c, [(-6, -130), (-70, -40), (-6, -36)]), (0.95, 0.95, 0.9), OUT * 0.6, None)
    ctx.restore()


def tc_string(ctx, t, p):
    """Red string from (0, 0) to p["to"], growing with p["grow"]; pins at both ends."""
    g = p.get("grow", 1.0)
    tx, ty = p.get("to", (400, 0))
    ex, ey = tx * g, ty * g
    mid = (ex / 2, ey / 2 + 30 * g)
    stroke(ctx, [(0, 0), mid, (ex, ey)], 9, smooth=True)
    stroke(ctx, [(0, 0), mid, (ex, ey)], 5, smooth=True, color=C["red"])
    for (x, y) in ((0, 0),) + (((ex, ey),) if g > 0.98 else ()):
        shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 16, 16), C["red"], OUT * 0.5, None)


def tc_note(ctx, t, p):
    """A pinned card with big text; p: text, px, w, h, col (text), rot, on, strike (0..1 crossed out)."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    s = back_out(min(1.0, on))
    ctx.save()
    ctx.rotate(math.radians(p.get("rot", -3)))
    ctx.scale(s, s)
    w, h = p.get("w", 640), p.get("h", 260)
    shape(ctx, lambda c: c.rectangle(-w / 2, -h / 2, w, h), hexc(p.get("bg", "#fbf6e6")), OUT * 0.8, (0, 0.08))
    text(ctx, p.get("text", ""), 0, 0, p.get("px", 110), p.get("col", "#e5383b"), 0)
    flat(ctx, lambda c: p_ellipse(c, 0, -h / 2 + 18, 16, 16), C["red"])
    st = p.get("strike", 0.0)
    if st > 0.01:
        stroke(ctx, [(-w / 2 + 20, 10), (-w / 2 + 20 + (w - 40) * min(1.0, st), -10)], 22)
        stroke(ctx, [(-w / 2 + 20, 10), (-w / 2 + 20 + (w - 40) * min(1.0, st), -10)], 13, color=C["red"])
    ctx.restore()


def tc_counter(ctx, t, p):
    """A big rolling number in world space: p: v (float, shown as an int), fmt ("{}"), px, col, on."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    v = p.get("v", 0.0)
    s = p.get("fmt", "{}").format(int(round(v)))
    if p.get("text"):
        s = p["text"]
    text(ctx, s, 0, 0, p.get("px", 160), p.get("col", "#ffd34d"), 10, a=min(1.0, on))


def tc_qm(ctx, t, p):
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    bl = 0.6 + 0.4 * math.sin(t * 5 + p.get("ph", 0))
    text(ctx, "?", 0, 0, p.get("px", 90), "#ffd34d", 8, a=on * bl)


def tc_race(ctx, t, p):
    """Two racing bars to a finish flag: p: a (0..1 top bar), b (0..1 bottom bar), la, lb (labels), w."""
    w = p.get("w", 1100)
    for k, (key, lab, col) in enumerate((("a", p.get("la", "TREE DOWN"), "#2f8050"), ("b", p.get("lb", "EGGS HATCH"), "#d8b47e"))):
        y = k * 200
        shape(ctx, lambda c, y=y: p_rrect(c, 0, y - 50, w, 100, 50), hexc("#2a2f3a"), OUT * 0.8, None)
        u = max(0.0, min(1.0, p.get(key, 0.0)))
        if u > 0.01:
            shape(ctx, lambda c, y=y, u=u: p_rrect(c, 6, y - 44, (w - 12) * u, 88, 44), hexc(col), OUT * 0.5, None)
        text(ctx, lab, -230, y, 60, "#ffffff", 6)
    stroke(ctx, [(w, -110), (w, 310)], 10)
    for k in range(6):
        for j in range(2):
            flat(ctx, lambda c, k=k, j=j: c.rectangle(w + j * 26, -110 + k * 26, 26, 26),
                 (1, 1, 1) if (k + j) % 2 else INK)


def tc_strip(ctx, t, p):
    """The 9-stowaway progress strip: slots 1..9; p: done (ticked count), blur (0..1 six silhouettes flash past),
    glow9 (0..1)."""
    for k in range(9):
        x = (k - 4) * 190
        shape(ctx, lambda c, x=x: p_rrect(c, x - 80, -80, 160, 160, 24), hexc("#2a2f3a"), OUT * 0.8, None)
        text(ctx, str(k + 1), x, -120, 48, "#ffffff", 5)
        if k < p.get("done", 2):
            stroke(ctx, [(x - 40, 0), (x - 10, 34), (x + 44, -36)], 22, color=INK)
            stroke(ctx, [(x - 40, 0), (x - 10, 34), (x + 44, -36)], 13, color=C["green"])
        elif k < 8:
            bl = p.get("blur", 0.0)
            u = max(0.0, min(1.0, bl * 6 - (k - 2)))
            if u > 0:
                flat(ctx, lambda c, x=x: p_ellipse(c, x, 0, 50, 34), (0.85, 0.85, 0.9), a=0.8 * u)
                for s in (-1, 1):
                    for j in range(3):
                        stroke(ctx, [(x - 20 + j * 20, 0), (x - 30 + j * 26, s * 60)], 6, color=(0.85, 0.85, 0.9), a=0.8 * u)
        else:
            g = p.get("glow9", 0.0)
            if g > 0.01:
                glow(ctx, x, 0, 200, hexc("#ffd34d"), 0.7 * g)
            text(ctx, "?", x, 0, 110, "#ffd34d", 8, a=max(0.3, g))


def tc_car(ctx, t, p):
    """A small car (side view, facing right) with a cut tree tied on the roof; origin = road under the middle.
    p: roll (wheel spin), bounce, tree (bool)."""
    b = 6 * math.sin(t * 12) * p.get("bounce", 1.0)
    for x in (-280, 260):
        shape(ctx, lambda c, x=x: p_ellipse(c, x, -70, 72, 72), INK, OUT * 0.5, None)
        shape(ctx, lambda c, x=x: p_ellipse(c, x, -70, 34, 34), PAL["steel"], OUT * 0.4, None)
        a = t * 12 * p.get("roll", 1.0)
        stroke(ctx, [(x - 30 * math.cos(a), -70 - 30 * math.sin(a)), (x + 30 * math.cos(a), -70 + 30 * math.sin(a))], 5)
    ctx.save()
    ctx.translate(0, b)
    shape(ctx, lambda c: p_smooth(c, [(-470, -100), (-460, -240), (-240, -260), (-150, -400), (190, -400), (290, -260),
                                      (470, -230), (480, -100)]), hexc(p.get("col", "#3b7dd8")), OUT, (0.05, 0.15),
          hi=(0.3, 0.2, 0.2))
    for (x0, x1) in ((-130, 10), (40, 175)):
        shape(ctx, lambda c, x0=x0, x1=x1: p_poly(c, [(x0, -380), (x1, -380), (x1 + (40 if x1 > 100 else 0), -270),
                                                      (x0 - 40 if x0 < -100 else x0, -270)]), hexc("#cfe8f5"), OUT * 0.7, None)
    shape(ctx, lambda c: p_ellipse(c, 450, -190, 24, 18), hexc("#fff2a8"), OUT * 0.5, None)
    if p.get("tree", True):
        ctx.save()
        ctx.translate(-330, -440)
        ctx.scale(0.75, 0.42)
        _tree_side(ctx, 860)
        ctx.restore()
        for x in (-80, 120):
            stroke(ctx, [(x, -400), (x - 10, -560), (x + 6, -400)], 5, color=hexc("#c0392b"))
    ctx.restore()


def tc_shaker(ctx, t, p):
    """A mechanical tree shaker at a lot: a steel frame with a motor box, a cut tree standing in its clamp; p: shake
    (0..1 rattles the tree), fall (0..1 specks drop)."""
    sh = p.get("shake", 0.0)
    shape(ctx, lambda c: p_rrect(c, -260, -150, 520, 150, 20), hexc("#e0a03a"), OUT, (0.05, 0.15))   # base + motor
    shape(ctx, lambda c: p_rrect(c, 120, -260, 170, 110, 14), hexc("#5b6b7a"), OUT * 0.8, None)
    for k in range(3):
        stroke(ctx, [(140, -230 + k * 30), (270, -230 + k * 30)], 5, color=INK)
    for x in (-220, 220):
        stroke(ctx, [(x, 0), (x, 30)], 20)
    stroke(ctx, [(0, -150), (0, -260)], 40)
    stroke(ctx, [(0, -150), (0, -260)], 26, color=PAL["steel"])
    ctx.save()
    ctx.translate(14 * sh * math.sin(t * 50), -240)
    ctx.rotate(0.03 * sh * math.sin(t * 43))
    ctx.scale(0.72, 0.72)
    shape(ctx, lambda c: c.rectangle(-30, -130, 60, 130), C["trunk"], OUT, None)
    _fir(ctx, t, {}, seed=11)
    ctx.restore()
    if sh > 0.01:
        for k in range(3):
            for s in (-1, 1):
                stroke(ctx, [(s * (330 + k * 30), -500 - k * 60), (s * (370 + k * 30), -530 - k * 60)], 7, a=sh)
    if p.get("fall", 0.0) > 0.01:
        ctx.save()
        ctx.translate(0, -60)
        tc_fall(ctx, t, {"on": p["fall"], "w": 520, "h": 600, "n": 26})
        ctx.restore()


ACTORS = {"tc_xtree": tc_xtree, "tc_twig": tc_twig, "tc_wild": tc_wild, "tc_farmtree": tc_farmtree, "tc_shrub": tc_shrub,
          "tc_tree_end": tc_tree_end, "tc_tree_lying": tc_tree_lying, "tc_rootball": tc_rootball,
          "tc_mantis": tc_mantis, "tc_nymph": tc_nymph, "tc_ooth": tc_ooth, "tc_marsh": tc_marsh, "tc_aphid": tc_aphid,
          "tc_tick_top": tc_tick_top, "tc_barkbeetle": tc_barkbeetle, "tc_sawdust": tc_sawdust, "tc_mite": tc_mite,
          "tc_springtail": tc_springtail, "tc_barklouse": tc_barklouse, "tc_spiderlings": tc_spiderlings,
          "tc_crawlers": tc_crawlers, "tc_slf_eggs": tc_slf_eggs, "tc_slf_nymphs": tc_slf_nymphs,
          "tc_adelgid": tc_adelgid, "tc_nest": tc_nest, "tc_dog": tc_dog, "tc_specks": tc_specks, "tc_fall": tc_fall,
          "tc_zz": tc_zz, "tc_prop": tc_prop, "tc_map": tc_map, "tc_ship": tc_ship, "tc_string": tc_string,
          "tc_note": tc_note, "tc_counter": tc_counter, "tc_qm": tc_qm, "tc_race": tc_race, "tc_strip": tc_strip,
          "tc_car": tc_car, "tc_shaker": tc_shaker}
SCENES = {"tc_living": tc_living, "tc_bokeh": tc_bokeh, "tc_lot": tc_lot, "tc_snowwood": tc_snowwood, "tc_farm": tc_farm,
          "tc_yard": tc_yard, "tc_cork": tc_cork, "tc_trunk": tc_trunk, "tc_road": tc_road, "tc_curb": tc_curb}


# ================================================================================================ extras

def tc_speech(ctx, t, p):
    """A speech bubble (tail to the lower left) with up to two lines; p: lines, px, on, under (0..1 underlines
    line 2), w, h."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    s = back_out(min(1.0, on))
    ctx.save()
    ctx.scale(s, s)
    w, h = p.get("w", 760), p.get("h", 300)
    shape(ctx, lambda c: p_rrect(c, -w / 2, -h / 2, w, h, 60), (1, 1, 1), OUT, None)
    shape(ctx, lambda c: p_poly(c, [(-w / 2 + 80, h / 2 - 6), (-w / 2 + 170, h / 2 - 6), (-w / 2 - 20, h / 2 + 110)]),
          (1, 1, 1), OUT, None)
    flat(ctx, lambda c: c.rectangle(-w / 2 + 84, h / 2 - 16, 80, 20), (1, 1, 1))
    lines = p.get("lines", [])
    px = p.get("px", 70)
    for k, ln in enumerate(lines):
        y = (k - (len(lines) - 1) / 2) * px * 1.25
        tw, th = text(ctx, ln, 0, y, px, "#1a1a1a", 0)
        if k == len(lines) - 1 and p.get("under", 0.0) > 0.01:
            u = min(1.0, p["under"])
            stroke(ctx, [(-tw / 2 + 6, y + px * 0.62), (-tw / 2 + 6 + (tw - 12) * u, y + px * 0.62)], 10, color=hexc("#e5383b"))
    ctx.restore()


def tc_tick(ctx, t, p):
    """A big green tick mark that pops in (p on)."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    s = back_out(min(1.0, on))
    ctx.save()
    ctx.scale(s, s)
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 90, 90), hexc("#3fb950"), OUT, None)
    stroke(ctx, [(-42, 0), (-12, 32), (46, -36)], 30, color=INK)
    stroke(ctx, [(-42, 0), (-12, 32), (46, -36)], 18, color=(1, 1, 1))
    ctx.restore()


def tc_stain(ctx, t, p):
    """A purple-red smear (p grow 0..1) on an optional white rug patch (p rug)."""
    if p.get("rug"):
        shape(ctx, lambda c: p_ellipse(c, 0, 0, 380, 90), (0.97, 0.96, 0.94), BG_OUT, (0.04, 0.12))
        for k in range(-6, 7):
            stroke(ctx, [(k * 60, 86), (k * 62, 104)], 4, color=(0.9, 0.88, 0.84))
    g = p.get("grow", 1.0)
    if g > 0.01:
        flat(ctx, lambda c: p_blob(c, 0, 0, 110 * g, 34 * g, 0.25, 5, 16), hexc("#7a1f6e"), a=0.9)
        flat(ctx, lambda c: p_blob(c, 70 * g, -8, 40 * g, 14 * g, 0.25, 9, 12), hexc("#a02a5a"), a=0.8)


def tc_bauble(ctx, t, p):
    """A big glass ornament hanging from a hook (origin = the hook top)."""
    col = hexc(p.get("col", "#c0392b"))
    sw = 0.05 * math.sin(t * 1.4)
    ctx.save()
    ctx.rotate(sw)
    stroke(ctx, [(0, 0), (0, 80)], 4)
    shape(ctx, lambda c: c.rectangle(-36, 70, 72, 40), PAL["steel"], OUT * 0.7, None)
    r = p.get("r", 150)
    shape(ctx, lambda c: p_ellipse(c, 0, 110 + r, r, r), col, OUT, (0.12, 0.12), hi=(0.3, 0.25, 0.28))
    stroke(ctx, [(-r * 0.9, 110 + r * 0.8), (0, 110 + r * 1.1), (r * 0.9, 110 + r * 0.8)], 10, smooth=True, color=C["gold"])
    ctx.restore()


def tc_pages(ctx, t, p):
    """Blank calendar pages drifting across (no text): p on, n."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    for k in range(int(p.get("n", 4))):
        u = (t * 0.35 + k / 4) % 1
        x = -700 + 1400 * u
        y = -200 + 120 * math.sin(u * 6 + k) + k * 60
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(math.sin(t * 2 + k) * 0.5)
        shape(ctx, lambda c: c.rectangle(-90, -100, 180, 200), (0.98, 0.97, 0.94), OUT * 0.6, None, a=on)
        flat(ctx, lambda c: c.rectangle(-90, -100, 180, 46), C["red"], a=on)
        ctx.restore()


def _cloth(ctx, t, p):
    """A damp towel (folded cloth), origin = its centre."""
    shape(ctx, lambda c: p_rrect(c, -170, -70, 340, 140, 30), hexc("#5ab0d8"), OUT, (0.05, 0.15))
    for k in range(4):
        stroke(ctx, [(-150 + k * 100, -60), (-160 + k * 100, 60)], 4, color=hexc("#3f8ab0"))
    for k in range(3):
        flat(ctx, lambda c, k=k: p_ellipse(c, -60 + k * 60, 90 + 14 * ((t * 3 + k) % 1), 8, 11), hexc("#8fd6e8"))


PROPS["cloth"] = _cloth


def tc_combo(ctx, t, layer, p):
    """Two scenes in one world, for a whip-pan inside a line: scene p["a"] (params pa) everywhere left of world x
    p["bx"], and scene p["b"] (params pb) shifted right by p["dx"], right of it."""
    from drawn import SCENES as ALL
    ALL[p["a"]](ctx, t, layer, p.get("pa", {}))
    ctx.save()
    layer(1.0)
    ctx.rectangle(p["bx"], -20000, 100000, 40000)
    ctx.restore()
    ctx.save()
    layer(1.0)
    ctx.rectangle(p["bx"], -20000, 100000, 40000)
    ctx.clip()
    dx = p.get("dx", 4000)

    def lay(d):
        layer(d)
        ctx.translate(dx, 0)
    ALL[p["b"]](ctx, t, lay, p.get("pb", {}))
    ctx.restore()
    if p.get("seam", False):
        layer(1.0)
        stroke(ctx, [(p["bx"], -20000), (p["bx"], 20000)], 30, color=hexc("#ffd34d"))


ACTORS.update({"tc_speech": tc_speech, "tc_tick": tc_tick, "tc_stain": tc_stain, "tc_bauble": tc_bauble,
               "tc_pages": tc_pages})
SCENES["tc_combo"] = tc_combo
