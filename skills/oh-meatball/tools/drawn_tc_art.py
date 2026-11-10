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
