"""Pictures for the philosophy test (11/18, Ship of Theseus TikTok + Short; scripts/drawn-house/tt-philosophy-ship.json
and yt-philosophy-ship.json), in the locked drawn_kit look (flat fills, one cel shade, thick ink outlines).
Same conventions as tools/drawn_topical_art.py: an actor draws at its origin in local units (feet / waterline at
y = 0, up is negative), scaled by its "s"; a scene draws in world units (default camera shows x 0..1080,
y 0..1920; floors sit at y = 1500). No words are drawn: every on-screen word comes from a spec card.

Actors:  ph_ship (a Greek galley, side view, origin = waterline centre, about 860 wide: p new 0..1 share of planks
         swapped to fresh wood, in a fixed random order; p seed; p glow 0..1 a gold rim; p ghost 0..1 fades it;
         p bob 0..1 sways on water; p sail colour; p eye (default True) the painted bow eye),
         ph_plank (one plank centred at its origin, 300 x 46: p old True = grey rotten wood, False = fresh),
         ph_pile (a stack of old planks, feet y 0: p n 0..1 how many are stacked),
         ph_body (a person silhouette full of cells, feet y 0, about 900 tall: p swap 0..1 share of cells flipped
         from blue to green in random order; p brain 0..1 rings the gold neurons in the head that never flip),
         ph_neuron (one gold neuron centred at its origin, about 420 wide: p glow 0..1, p lock 0..1 a padlock),
         ph_blood (a red blood cell disc centred at its origin, 160 wide; p spin),
         ph_phone (a smartphone centred at its origin, 300 x 600: p crack 0..1 cracks spread, p fix 0..1 a new
         screen slides down over them, p glow),
         ph_scale (a balance scale, feet y 0, 700 wide: p tilt -1..1 left pan down .. right pan down),
         ph_split (a vote split badge: two half discs, p a / p b colours, p on 0..1 pops in),
         ph_qm (a big bouncing question mark centred at its origin, p on 0..1, p col)
Scenes:  ph_harbor (an ancient harbour: banded sky, a temple on a hill, sea, a wooden dock floor at y 1500;
         p time "day" | "dusk"), ph_museum (a museum hall: marble wall, columns, spotlights, a plinth line, rope
         posts; floor y 1500), ph_shed (a plank-walled workshop with a lantern; floor y 1500), ph_lab (a plain
         science backdrop: dark blue wall with a cell-dot pattern; floor y 1500; p wall colour)
"""
import math
import random

import cairo

from drawn_kit import (BG_OUT, OUT, back_out, darker, flat, hexc, lighter, p_ellipse, p_poly, p_rrect, p_smooth,
                       shape, stroke)

C = {k: hexc(v) for k, v in {
    "old": "#7d6c58", "old_dk": "#5f5142", "rot": "#4f5a3c", "new": "#e3b26a", "new_dk": "#c48f45",
    "hull_line": "#3b2a1c", "mast": "#8a5a30", "sail": "#f4ecd6", "sail2": "#d8322a", "gold": "#ffd34d",
    "eye": "#f4f4f4", "sky": "#8fd3f4", "sky2": "#bfe6f8", "dusk1": "#f7a35c", "dusk2": "#f3c27a",
    "sea": "#2f7fc0", "sea2": "#2a6fab", "foam": "#e8f6ff", "hill": "#9cc26a", "hill_dk": "#7fa653",
    "marble": "#efe8da", "marble_dk": "#d6ccb8", "dock": "#a8764a", "dock_dk": "#83592f",
    "cellA": "#5fa8e8", "cellB": "#7cd67a", "body": "#2b3656", "neuron": "#ffcf4a", "blood": "#d8322a",
    "phone": "#2b2f38", "screen": "#5ee0ff", "wall_m": "#c9bfae", "shed": "#9a6a3e", "shed_dk": "#7a5230",
    "lab": "#1f2d4f", "lab2": "#263862", "rope": "#b8352c", "brass": "#d9b44a",
}.items()}


def _rng(seed):
    return random.Random(seed)


# ================================================================================================ ship + planks

HULL = [(-430, -150), (430, -150), (400, -90), (330, 0), (230, 70), (-230, 70), (-340, 0), (-410, -90)]


def _hull_path(c):
    p_smooth(c, HULL)


def ph_ship(ctx, t, p):
    """A Greek galley (side view), origin = waterline centre: plank rows (old grey-brown or fresh honey, by p new),
    a stern curl, a mast with a striped square sail, a row of oars and the painted bow eye."""
    new = max(0.0, min(1.0, p.get("new", 0.0)))
    ghost = 1.0 - p.get("ghost", 0.0)
    if ghost <= 0.02:
        return
    bob = p.get("bob", 1.0)
    ctx.save()
    if bob:
        ctx.translate(0, 8 * bob * math.sin(t * 2.1 + p.get("seed", 0)))
        ctx.rotate(0.012 * bob * math.sin(t * 1.7 + 0.5))
    if ghost < 1:
        ctx.push_group()
    # mast + sail behind the hull
    stroke(ctx, [(0, -150), (0, -640)], 22, color=C["mast"])
    stroke(ctx, [(0, -150), (0, -640)], 6)
    stroke(ctx, [(-240, -600), (240, -600)], 14, color=C["mast"])
    sail = hexc(p["sail"]) if p.get("sail") else C["sail"]
    puff = 18 * math.sin(t * 1.3)

    def sail_path(c):
        p_smooth(c, [(-230, -595), (230, -595), (250 + puff, -400), (230, -230), (-230, -230), (-250 - puff, -400)])
    shape(ctx, sail_path, sail, OUT, (0.04, 0.08))
    ctx.save()
    sail_path(ctx)
    ctx.clip()
    for x in (-150, -50, 50, 150):
        flat(ctx, lambda c, x=x: c.rectangle(x - 22, -620, 44, 420), C["sail2"])
    ctx.restore()
    sail_path(ctx)
    ctx.set_source_rgba(0.07, 0.07, 0.07, 1)
    ctx.set_line_width(OUT)
    ctx.stroke()
    # stern curl + bow ram
    stroke(ctx, [(-400, -140), (-450, -230), (-410, -300), (-360, -270)], 26, smooth=True, color=C["new_dk"] if new > 0.95 else C["old_dk"])
    stroke(ctx, [(-400, -140), (-450, -230), (-410, -300), (-360, -270)], 7, smooth=True)
    # hull: plank rows clipped to the hull shape
    rows, cols = 4, 9
    order = list(range(rows * cols))
    _rng(p.get("seed", 7)).shuffle(order)
    n_new = int(round(new * rows * cols))
    fresh = set(order[:n_new])
    ctx.save()
    _hull_path(ctx)
    ctx.clip()
    for r in range(rows):
        y0 = -150 + r * 55
        off = (r % 2) * 50
        for k in range(cols + 1):
            x0 = -480 + k * 105 - off
            idx = (r * cols + k) % (rows * cols)
            col = C["new"] if idx in fresh else C["old"]
            flat(ctx, lambda c, x0=x0, y0=y0: c.rectangle(x0, y0, 105, 55), col)
            flat(ctx, lambda c, x0=x0, y0=y0: c.rectangle(x0, y0 + 40, 105, 15), darker(col, 0.85))
            if idx not in fresh and (idx * 7) % 3 == 0:
                flat(ctx, lambda c, x0=x0, y0=y0: p_ellipse(c, x0 + 52, y0 + 26, 16, 9), C["rot"])
            stroke(ctx, [(x0, y0), (x0, y0 + 55)], 4, color=C["hull_line"])
        stroke(ctx, [(-500, y0 + 55), (500, y0 + 55)], 4, color=C["hull_line"])
    ctx.restore()
    _hull_path(ctx)
    ctx.set_source_rgba(0.07, 0.07, 0.07, 1)
    ctx.set_line_width(OUT)
    ctx.stroke()
    # rail + oars
    stroke(ctx, [(-430, -150), (430, -150)], 14, color=C["mast"])
    stroke(ctx, [(-430, -150), (430, -150)], 4)
    for k in range(6):
        x = -260 + k * 100
        sw = 0.25 * math.sin(t * 2.4 + k * 0.4)
        stroke(ctx, [(x, -110), (x - 60 + 40 * sw, 130)], 10, color=C["mast"])
    if p.get("eye", True):
        shape(ctx, lambda c: p_ellipse(c, 300, -95, 34, 20), C["eye"], OUT * 0.6, None)
        flat(ctx, lambda c: p_ellipse(c, 308, -95, 12, 12), hexc("#111111"))
    g = p.get("glow", 0.0)
    if g > 0.01:
        _hull_path(ctx)
        ctx.set_source_rgba(*C["gold"], 0.9 * g)
        ctx.set_line_width(20)
        ctx.stroke()
    if ghost < 1:
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(ghost)
    ctx.restore()


def ph_plank(ctx, t, p):
    """One plank centred at its origin (300 x 46); p old True = grey rotten wood, False = fresh."""
    old = p.get("old", True)
    col = C["old"] if old else C["new"]
    ctx.save()
    ctx.rotate(p.get("rot", 0.0) + p.get("spin", 0.0) * t)
    shape(ctx, lambda c: p_rrect(c, -150, -23, 300, 46, 8), col, OUT * 0.7, (0.02, 0.2))
    for x in (-90, 10, 90):
        stroke(ctx, [(x - 30, -6), (x + 30, -4)], 3, color=darker(col, 0.7))
    if old:
        flat(ctx, lambda c: p_ellipse(c, -40, 4, 22, 10), C["rot"])
        flat(ctx, lambda c: p_ellipse(c, 70, -6, 12, 7), C["rot"])
    ctx.restore()


def ph_pile(ctx, t, p):
    """A stack of old planks (feet y 0, about 420 wide); p n 0..1 how many of the 9 are stacked."""
    n = int(round(max(0.0, min(1.0, p.get("n", 1.0))) * 9))
    k = 0
    for row, cnt in enumerate((4, 3, 2)):
        for j in range(cnt):
            if k >= n:
                return
            x = (j - (cnt - 1) / 2) * 105
            y = -26 - row * 48
            ctx.save()
            ctx.translate(x, y)
            ctx.rotate(math.pi / 2 * 0 + (0.04 if (k % 2) else -0.03))
            ctx.scale(0.36, 1.0)
            ph_plank(ctx, 0, {"old": True})
            ctx.restore()
            k += 1


# ================================================================================================ body + cells

def _body_path(c):
    pts = [(0, -900), (70, -880), (105, -810), (95, -730), (60, -690), (190, -650), (250, -560), (290, -330),
           (240, -320), (200, -520), (170, -420), (160, -330), (150, 0), (40, 0), (20, -330), (-20, -330), (-40, 0),
           (-150, 0), (-160, -330), (-170, -420), (-200, -520), (-240, -320), (-290, -330), (-250, -560),
           (-190, -650), (-60, -690), (-95, -730), (-105, -810), (-70, -880)]
    p_smooth(c, pts)


def ph_body(ctx, t, p):
    """A person silhouette filled with little cells; p swap 0..1 flips them blue -> green in random order (each
    flip pops); p brain 0..1 rings the gold neurons in the head, which never flip."""
    sw = max(0.0, min(1.0, p.get("swap", 0.0)))
    br = p.get("brain", 0.0)
    shape(ctx, _body_path, C["body"], OUT, (0.03, 0.05))
    ctx.save()
    _body_path(ctx)
    ctx.clip()
    rng = _rng(3)
    cells = []
    for yy in range(-880, 0, 44):
        for xx in range(-300, 300, 44):
            cells.append((xx + (22 if (yy // 44) % 2 else 0), yy))
    ranks = list(range(len(cells)))
    rng.shuffle(ranks)
    n = len(cells)
    for i, (x, y) in enumerate(cells):
        head = y < -720 and abs(x) < 80
        if head:
            col = C["neuron"]
        else:
            r = ranks[i] / n
            col = C["cellB"] if r < sw else C["cellA"]
            pop = (sw - r) * n / 12.0
            if 0 <= pop < 1:
                col = lighter(col, 0.6 * (1 - pop))
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 17, 17), col)
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x + 3, y + 3, 6, 6), darker(col, 0.7))
    ctx.restore()
    _body_path(ctx)
    ctx.set_source_rgba(0.07, 0.07, 0.07, 1)
    ctx.set_line_width(OUT)
    ctx.stroke()
    if br > 0.01:
        rr = 110 + 12 * math.sin(t * 6)
        ctx.save()
        ctx.set_source_rgba(*C["gold"], min(1, br))
        ctx.set_line_width(14)
        p_ellipse(ctx, 0, -800, rr, rr)
        ctx.stroke()
        ctx.restore()


def ph_neuron(ctx, t, p):
    """A gold cartoon neuron centred at its origin (about 420 wide): dendrites, a soma with a nucleus, a long axon
    with terminals; p glow 0..1 pulses a rim; p lock 0..1 a padlock pops on the soma."""
    w = 1 + 0.03 * math.sin(t * 4)
    for a in range(7):
        ang = a / 7 * math.tau + 0.3
        x1, y1 = 150 * math.cos(ang) * w, 150 * math.sin(ang) * w
        stroke(ctx, [(0, 0), (x1 * 0.6, y1 * 0.6 + 10), (x1, y1)], 26, smooth=True)
        stroke(ctx, [(0, 0), (x1 * 0.6, y1 * 0.6 + 10), (x1, y1)], 14, smooth=True, color=C["neuron"])
    stroke(ctx, [(60, 20), (200, 60), (330, 40), (420, 80)], 26, smooth=True)
    stroke(ctx, [(60, 20), (200, 60), (330, 40), (420, 80)], 14, smooth=True, color=C["neuron"])
    for dy in (-30, 20, 60):
        stroke(ctx, [(420, 80), (470, 80 + dy)], 10)
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 90, 80), C["neuron"], OUT, (0.06, 0.1), hi=(0.3, 0.3, 0.2))
    shape(ctx, lambda c: p_ellipse(c, 6, 4, 32, 30), hexc("#e08a2a"), OUT * 0.6, None)
    g = p.get("glow", 0.0)
    if g > 0.01:
        ctx.save()
        ctx.set_source_rgba(1, 0.95, 0.6, 0.5 * g * (0.7 + 0.3 * math.sin(t * 8)))
        p_ellipse(ctx, 0, 0, 150, 140)
        ctx.set_line_width(18)
        ctx.stroke()
        ctx.restore()
    lk = p.get("lock", 0.0)
    if lk > 0.01:
        s = back_out(min(1.0, lk))
        ctx.save()
        ctx.translate(0, 110)
        ctx.scale(s, s)
        stroke(ctx, [(-34, -10), (-34, -50), (0, -78), (34, -50), (34, -10)], 16, smooth=True, color=hexc("#9aa3ab"))
        shape(ctx, lambda c: p_rrect(c, -60, -14, 120, 96, 14), C["brass"], OUT * 0.8, (0.04, 0.12))
        flat(ctx, lambda c: p_ellipse(c, 0, 26, 12, 12), hexc("#5e3d23"))
        ctx.restore()


def ph_blood(ctx, t, p):
    """A red blood cell disc (160 wide) centred at its origin; p spin turns it."""
    ctx.save()
    ctx.rotate(p.get("spin", 0.6) * t + p.get("rot", 0.0))
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 80, 62), C["blood"], OUT * 0.7, (0.05, 0.1))
    flat(ctx, lambda c: p_ellipse(c, 0, 0, 38, 26), darker(C["blood"], 0.75))
    ctx.restore()


# ================================================================================================ phone, scale, badges

def ph_phone(ctx, t, p):
    """A plain smartphone centred at its origin (300 x 600): p crack 0..1 spreads cracks from an impact point,
    p fix 0..1 slides a fresh screen down over them; app squares only, no logos."""
    ctx.save()
    ctx.rotate(p.get("rot", 0.0))
    shape(ctx, lambda c: p_rrect(c, -150, -300, 300, 600, 44), C["phone"], OUT, (0.03, 0.06))
    scr = (-128, -270, 256, 540)
    flat(ctx, lambda c: p_rrect(c, *scr, 26), hexc("#16203a"))
    ctx.save()
    p_rrect(ctx, *scr, 26)
    ctx.clip()
    for r in range(5):
        for k in range(3):
            x = -95 + k * 80
            y = -230 + r * 90
            flat(ctx, lambda c, x=x, y=y: p_rrect(c, x, y, 54, 54, 14), [C["screen"], C["gold"], C["cellB"], C["rope"]][(r + k) % 4])
    cr = p.get("crack", 0.0)
    if cr > 0.01:
        rng = _rng(11)
        cx, cy = 30, -60
        for a in range(9):
            ang = a / 9 * math.tau + rng.uniform(-0.2, 0.2)
            L = (180 + rng.uniform(0, 160)) * min(1, cr)
            pts = [(cx, cy)]
            for s_ in (0.35, 0.7, 1.0):
                pts.append((cx + L * s_ * math.cos(ang) + rng.uniform(-18, 18), cy + L * s_ * math.sin(ang) + rng.uniform(-18, 18)))
            stroke(ctx, pts, 5, color=(1, 1, 1), a=0.95)
    fx = p.get("fix", 0.0)
    if fx > 0.01:
        h = 540 * min(1.0, fx)
        flat(ctx, lambda c: c.rectangle(-128, -270, 256, h), hexc("#e8f6ff"))
        flat(ctx, lambda c: c.rectangle(-128, -270 + h - 10, 256, 10), C["screen"])
    ctx.restore()
    g = p.get("glow", 0.0)
    if g > 0.01:
        ctx.set_source_rgba(*C["screen"], 0.5 * g)
        p_rrect(ctx, -165, -315, 330, 630, 52)
        ctx.set_line_width(14)
        ctx.stroke()
    ctx.restore()


def ph_scale(ctx, t, p):
    """A brass balance scale (feet y 0, beam 700 wide at y -620); p tilt -1..1 (left pan down .. right pan down),
    eased, with a little wobble."""
    tilt = p.get("tilt", 0.0) + 0.05 * math.sin(t * 3)
    ang = 0.28 * tilt
    shape(ctx, lambda c: p_poly(c, [(-140, 0), (140, 0), (60, -40), (-60, -40)]), C["brass"], OUT, (0.03, 0.1))
    stroke(ctx, [(0, -40), (0, -640)], 26, color=C["brass"])
    stroke(ctx, [(0, -40), (0, -640)], 6)
    ca, sa = math.cos(ang), math.sin(ang)
    ends = []
    for sgn in (-1, 1):
        ends.append((sgn * 340 * ca, -620 + sgn * 340 * sa))
    stroke(ctx, [ends[0], ends[1]], 22, color=C["brass"])
    stroke(ctx, [ends[0], ends[1]], 5)
    for ex, ey in ends:
        stroke(ctx, [(ex, ey), (ex - 90, ey + 220)], 4)
        stroke(ctx, [(ex, ey), (ex + 90, ey + 220)], 4)
        shape(ctx, lambda c, ex=ex, ey=ey: p_poly(c, [(ex - 130, ey + 220), (ex + 130, ey + 220), (ex + 90, ey + 260),
                                                       (ex - 90, ey + 260)]), C["brass"], OUT * 0.8, None)
    shape(ctx, lambda c: p_ellipse(c, 0, -640, 26, 26), C["brass"], OUT * 0.7, None)


def ph_split(ctx, t, p):
    """A vote badge: a disc split down the middle (p a left colour, p b right colour), a white seam; p on 0..1."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    s = back_out(min(1.0, on))
    ctx.save()
    ctx.scale(s, s)
    ctx.rotate(0.08 * math.sin(t * 3))
    for sgn, col in ((-1, hexc(p.get("a", "#3b7dd8"))), (1, hexc(p.get("b", "#e5383b")))):
        shape(ctx, lambda c, sgn=sgn: (c.move_to(0, -180), c.arc(0, 0, 180, -math.pi / 2, math.pi / 2) if sgn > 0 else
                                       c.arc_negative(0, 0, 180, -math.pi / 2, math.pi / 2), c.close_path()),
              col, OUT, None)
    stroke(ctx, [(0, -200), (0, 200)], 14, color=(1, 1, 1))
    ctx.restore()


def ph_qm(ctx, t, p):
    """A big question mark centred at its origin (about 300 tall); p on 0..1 pops it; p col."""
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    s = back_out(min(1.0, on)) * (1 + 0.04 * math.sin(t * 5))
    col = hexc(p.get("col", "#ffd34d"))
    ctx.save()
    ctx.scale(s, s)
    ctx.rotate(0.1 * math.sin(t * 2.5))
    pts = [(-80, -80), (-60, -150), (0, -170), (70, -140), (80, -80), (40, -30), (0, 0), (0, 50)]
    stroke(ctx, pts, 70, smooth=True)
    stroke(ctx, pts, 46, smooth=True, color=col)
    shape(ctx, lambda c: p_ellipse(c, 0, 125, 32, 32), col, OUT, None)
    ctx.restore()


# ================================================================================================ scenes

def ph_harbor(ctx, t, layer, p):
    """An ancient harbour: banded sky (p time "dusk" = orange), a sun, a green hill with a small columned temple,
    the sea with moving wave dashes from y 1180, and a wooden dock floor at y 1500."""
    dusk = p.get("time") == "dusk"
    layer(0.6)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), C["dusk1"] if dusk else C["sky"])
    for k, y in enumerate((300, 520, 700)):
        flat(ctx, lambda c, y=y: c.rectangle(-3000, y, 8000, 400), C["dusk2"] if dusk else C["sky2"], a=0.35 + 0.15 * k)
    flat(ctx, lambda c: p_ellipse(c, 820, 420, 90, 90), hexc("#ffd84a"))
    layer(0.75)
    shape(ctx, lambda c: p_smooth(c, [(-600, 1220), (-100, 900), (300, 860), (650, 1000), (900, 1220)]), C["hill"],
          BG_OUT, (0.03, 0.1))
    # temple
    shape(ctx, lambda c: p_poly(c, [(100, 760), (300, 690), (500, 760)]), C["marble"], BG_OUT, None)
    shape(ctx, lambda c: c.rectangle(110, 760, 380, 26), C["marble"], BG_OUT, None)
    for x in range(130, 480, 58):
        shape(ctx, lambda c, x=x: c.rectangle(x, 786, 28, 120), C["marble"], BG_OUT * 0.7, None)
    shape(ctx, lambda c: c.rectangle(100, 900, 400, 24), C["marble_dk"], BG_OUT, None)
    layer(0.85)
    flat(ctx, lambda c: c.rectangle(-3000, 1180, 8000, 2000), C["sea"])
    flat(ctx, lambda c: c.rectangle(-3000, 1180, 8000, 90), C["sea2"])
    for r in range(5):
        y = 1210 + r * 60
        for k in range(-6, 14):
            x = k * 220 + (r * 90) + 40 * math.sin(t * 1.2 + r)
            stroke(ctx, [(x, y), (x + 70, y)], 6, color=C["foam"], a=0.8)
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 3000), C["dock"])
    for y in (1500, 1590, 1700, 1830):
        stroke(ctx, [(-3000, y), (5000, y)], 6, color=C["dock_dk"])
    for x in range(-2000, 4000, 240):
        stroke(ctx, [(x, 1590), (x, 1700)], 5, color=C["dock_dk"])
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)


def ph_museum(ctx, t, layer, p):
    """A museum hall: warm marble wall with columns, two spotlight cones, floor y 1500 with tiles, rope posts."""
    layer(0.9)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), C["wall_m"])
    for x in range(-1200, 2400, 420):
        shape(ctx, lambda c, x=x: c.rectangle(x, 300, 90, 1200), C["marble"], BG_OUT, (0.2, 0.0))
        shape(ctx, lambda c, x=x: c.rectangle(x - 20, 270, 130, 40), C["marble_dk"], BG_OUT, None)
    for x in (300, 780):
        ctx.save()
        ctx.set_source_rgba(1, 0.96, 0.75, 0.22)
        p_poly(ctx, [(x - 40, 0), (x + 40, 0), (x + 330, 1500), (x - 330, 1500)])
        ctx.fill()
        ctx.restore()
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 3000), hexc("#8a6f55"))
    for x in range(-2000, 4000, 160):
        stroke(ctx, [(x, 1500), (x - 120, 1920)], 4, color=hexc("#735a43"))
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)
    if p.get("rope", True):
        for x in (-20, 1100):
            stroke(ctx, [(x, 1720), (x, 1560)], 14, color=C["brass"])
        stroke(ctx, [(-20, 1575), (540, 1640), (1100, 1575)], 14, smooth=True, color=C["rope"])


def ph_shed(ctx, t, layer, p):
    """A plank-walled workshop at night: vertical boards, a hanging lantern glow, floor y 1500."""
    layer(0.9)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), C["shed"])
    for x in range(-3000, 5000, 120):
        stroke(ctx, [(x, -3000), (x, 1500)], 6, color=C["shed_dk"])
    ctx.save()
    g = 0.30 + 0.04 * math.sin(t * 7)
    pat = cairo.RadialGradient(780, 520, 10, 780, 520, 700)
    pat.add_color_stop_rgba(0, 1, 0.92, 0.6, g)
    pat.add_color_stop_rgba(1, 1, 0.92, 0.6, 0)
    ctx.set_source(pat)
    ctx.paint()
    ctx.restore()
    stroke(ctx, [(780, 0), (780, 440)], 6)
    shape(ctx, lambda c: p_rrect(c, 740, 440, 80, 110, 16), hexc("#ffd84a"), OUT * 0.7, None)
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 3000), C["shed_dk"])
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)


def ph_lab(ctx, t, layer, p):
    """A plain science backdrop: p wall colour (default deep blue) with a soft pattern of cell dots that drift,
    floor y 1500."""
    wall = hexc(p.get("wall", "#1f2d4f"))
    layer(0.9)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), wall)
    rng = _rng(5)
    for _ in range(70):
        x, y, r = rng.uniform(-400, 1500), rng.uniform(-200, 1500), rng.uniform(20, 60)
        y = (y - 18 * t) % 1700 - 200
        ctx.save()
        ctx.set_source_rgba(*lighter(wall, 0.25), 0.55)
        p_ellipse(ctx, x, y, r, r)
        ctx.set_line_width(6)
        ctx.stroke()
        ctx.restore()
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 3000), darker(wall, 0.7))
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 14), lighter(wall, 0.3))
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)


ACTORS = {"ph_ship": ph_ship, "ph_plank": ph_plank, "ph_pile": ph_pile, "ph_body": ph_body, "ph_neuron": ph_neuron,
          "ph_blood": ph_blood, "ph_phone": ph_phone, "ph_scale": ph_scale, "ph_split": ph_split, "ph_qm": ph_qm}
SCENES = {"ph_harbor": ph_harbor, "ph_museum": ph_museum, "ph_shed": ph_shed, "ph_lab": ph_lab}
