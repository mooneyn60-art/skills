"""Parametric creature builder for tools/drawn.py: a new animal is a short config, not new drawing code.

    from drawn_creatures import build
    ACTORS["silverfish2"] = build({"plan": "insect", "body": "carrot", "color": "#bcc6cf", "tails": 3, ...})

Body plans (all in the drawn_kit house style: thick ink outline, flat colour + one cel shade, a cartoon face):
  insect     side view, facing right: head + body (round | long | carrot), 6 legs, antennae, wings (clear | shell),
             tail filaments, stripes / sheen
  arachnid   front view: cephalothorax + abdomen, 8 legs, eyes (pair | jumper | row), fangs, fuzz, pattern
             (hourglass | stripe | spots)
  centipede  side view: n segments with a leg pair each (0 legs = a worm), antennae, long last legs, stripes
  mite       microscopic: shape round (front view, 8 spread legs, hairs) or long (side view worm body with 8
             stubby legs up front)
  fish       side view: body, tail fin, dorsal fin, stripes, teeth, lure (deep-sea angler)
  bird       side view: body, head, beak (short | long | hook), flapping wing, legs, tail, crest
  mammal     side view small mammal: body, head + snout, ears (round | pointed | long), tail (thin | fluffy),
             4 legs, whiskers
  reptile    side view lizard: long body, tapering tail, 4 sprawled legs, spikes, or a turtle shell

Config keys (all optional): plan, color, dark, accent, belly, length, height, legs, leg_len, ant (antennae
length), wings, tails, tail_len, stripes, sheen, eye_r, eyes, mouth, fangs, teeth, pattern, hairs, mood (the
default expression), s (the stage scale that makes it read big next to Meatball), xray (empty | gut | venom |
heart: what the x-ray reveals), label (what it is, for the authoring tool).
Per-frame params (spec "p"): mood, look, talk, walking/phase (from drawn.py), bite (0..1), chew (0..1),
xray (0..1), wrapped (0..1), wave (0..1 front legs up), crouch (0..1), fly (wings), hidden.
Base point: y = 0 is the ground under the feet (fish: the body centre; they float).
"""
import math
import random

from drawn_kit import INK, OUT, PAL, darker, eyes, flat, hexc, ink, lighter, limb, mouth, p_blob, p_ellipse, \
    p_poly, p_rrect, p_smooth, shape, src, stroke


def _c(cfg, key, default):
    v = cfg.get(key, default)
    return hexc(v) if isinstance(v, str) else v


def _banded(ctx, pts, w, col, band=None):
    limb(ctx, pts, w, col, OUT * 0.5)
    if band:
        ctx.save()
        p_smooth(ctx, pts, close=False)
        ctx.set_dash([w * 1.6, w * 2.2])
        src(ctx, band)
        ctx.set_line_width(w)
        ctx.stroke()
        ctx.restore()


def _overlays(ctx, cfg, p, path, cx, cy, rx, ry):
    """X-ray reveal and silk wrapping, shared by every plan (path draws the body outline)."""
    xr = p.get("xray", 0.0)
    if xr > 0:
        ctx.save()
        path(ctx)
        src(ctx, (0.55, 0.85, 1.0), 0.85 * xr)
        ctx.fill_preserve()
        ink(ctx, OUT, xr)
        ctx.stroke()
        what = cfg.get("xray", "gut")
        if what == "empty":
            ctx.set_dash([10, 8])
            p_ellipse(ctx, cx, cy, rx * 0.4, ry * 0.4)
            ink(ctx, 5, xr)
            ctx.stroke()
            ctx.set_dash([])
            stroke(ctx, [(cx - rx * 0.35, cy + ry * 0.4), (cx + rx * 0.35, cy - ry * 0.4)], 7, color=PAL["red"], a=xr)
        elif what == "venom":
            shape(ctx, lambda c: p_ellipse(c, cx + rx * 0.3, cy, rx * 0.3, ry * 0.4), hexc("#7bd14a"), OUT * 0.6,
                  None, a=xr)
        elif what == "heart":
            shape(ctx, lambda c: p_ellipse(c, cx, cy, rx * 0.22, ry * 0.3), PAL["red"], OUT * 0.6, None, a=xr)
        else:   # gut: a winding tube
            pts = [(cx + rx * 0.7 - k * rx * 0.2, cy + ry * 0.25 * math.sin(k * 1.7)) for k in range(8)]
            stroke(ctx, pts, max(8, ry * 0.12), smooth=True, color=hexc("#e58a5c"), a=xr)
        ctx.restore()
    w = p.get("wrapped", 0.0)
    if w > 0:
        shape(ctx, lambda c: p_ellipse(c, cx, cy, rx * 1.15, ry * 1.25), (1, 1, 1), OUT * 0.5, None, a=0.75 * w)
        for k in range(7):
            a = k * 0.45
            stroke(ctx, [(cx - rx * math.cos(a), cy - ry * math.sin(a)), (cx + rx * math.cos(a + 0.6),
                                                                         cy + ry * math.sin(a + 0.6))],
                   4, color=(0.85, 0.85, 0.85), a=w)


def _face(ctx, cfg, p, x, y, r, lid, mouth_dy=None, side=True):
    look = p.get("look", (1, 0) if side else (0, 0))
    eyes(ctx, x, y, r, r * 1.05, look, (p.get("mood") or cfg.get("mood", "calm")), p.get("blink", 0), OUT * 0.6, lid=lid)
    my = y + (mouth_dy if mouth_dy is not None else r * 1.9)
    mx = x + (r * 0.6 if side else 0)
    talk = max(p.get("talk", 0.0), p.get("chew", 0.0) * abs(math.sin(p.get("phase", 0) * 1.3 + 3)))
    if cfg.get("fangs"):
        b = p.get("bite", 0.0)
        for s in (-1, 1):
            shape(ctx, lambda c, s=s: p_poly(c, [(mx + s * r * 0.25, my), (mx + s * r * 0.6, my),
                                                 (mx + s * r * 0.4, my + r * (0.5 + 0.5 * b))]),
                  _c(cfg, "fang_color", "#5a1a14"), OUT * 0.45, None)
    mouth(ctx, mx, my, r * 1.3, p.get("mouth", cfg.get("mouth", "smile")), talk, OUT * 0.55,
          teeth=bool(cfg.get("teeth")))


def _walk(p, k, side):
    ph = p.get("phase", 0.0)
    if not p.get("walking"):
        return 0.0, 0.0
    q = ph * 1.5 + k * 1.9 + (math.pi if side else 0)
    return 30 * math.sin(q), -28 * max(0.0, math.cos(q))


# ================================================================= plans

def insect(ctx, t, cfg, p):
    L, H = cfg.get("length", 520), cfg.get("height", 170)
    col, dk = _c(cfg, "color", "#8a4b25"), _c(cfg, "dark", None)
    dk = dk or darker(col, 0.72)
    by = -H * 0.55 - cfg.get("leg_len", 120) * 0.45 + 3 * math.sin(t * 2.4)
    body = cfg.get("body", "round")
    x0, x1 = -L * 0.5, L * 0.32
    if body == "carrot":
        path = lambda c: p_smooth(c, [(x0, by + H * 0.05), (x0 * 0.5, by - H * 0.3), (x1 * 0.4, by - H * 0.55),  # noqa
                                      (x1, by - H * 0.5), (x1 + H * 0.15, by), (x1, by + H * 0.4),
                                      (x0 * 0.5, by + H * 0.35)])
    elif body == "long":
        path = lambda c: p_rrect(c, x0, by - H / 2, x1 - x0, H, H / 2)  # noqa
    else:
        path = lambda c: p_ellipse(c, (x0 + x1) / 2, by, (x1 - x0) / 2, H / 2)  # noqa
    ll = cfg.get("leg_len", 120)
    nl = cfg.get("legs", 6) // 2

    def legs(far):
        for i in range(nl):
            hx = x1 - (x1 - x0) * (0.25 + 0.5 * i / max(nl - 1, 1))
            dx, dy = _walk(p, i, far)
            fx = hx + (1 - i) * ll * 0.5 + dx - (20 if far else 0)
            _banded(ctx, [(hx, by + H * 0.3), (hx + (1 - i) * ll * 0.25 + 15, by + H * 0.3 + ll * 0.2 - ll * 0.6),
                          (fx, dy - (14 if far else 0))], cfg.get("leg_w", 11), dk if far else col)
    legs(True)
    for k in range(cfg.get("tails", 0)):
        sw = 12 * math.sin(t * 5 + k)
        a = (k - (cfg["tails"] - 1) / 2) * 0.35
        tl = cfg.get("tail_len", L * 0.55)
        stroke(ctx, [(x0, by), (x0 - tl * 0.5, by + tl * 0.5 * math.sin(a) + sw),
                     (x0 - tl, by + tl * math.sin(a) + sw)], 7, smooth=True)
    hr = H * cfg.get("head_r", 0.48)
    hx = x1 + hr * 0.7
    for k in range(2 if cfg.get("ant", 0) else 0):
        sw = 22 * math.sin(t * 4 + k)
        A = cfg["ant"]
        stroke(ctx, [(hx + hr * 0.3, by - hr * 0.6), (hx + A * 0.4, by - A * 0.55 - 40 * k + sw),
                     (hx + A, by - A * 0.45 - 50 * k + sw)], 7, smooth=True)
    wings = cfg.get("wings")
    if wings == "clear":
        flap = math.sin(t * 60) if p.get("fly") else 0.0
        for k in (0, 1):
            shape(ctx, lambda c, k=k: p_ellipse(c, (x0 + x1) / 2 - 20 + k * 30, by - H * 0.6 - 25 * flap,
                                                L * 0.32, H * 0.3, -0.4 + 0.3 * flap),
                  hexc("#d8ecf7"), OUT * 0.5, None, a=0.75)
    shape(ctx, path, col, OUT, (0.0, 0.22), hi=(0.35, 0.2, 0.22))
    ctx.save()
    path(ctx)
    ctx.clip()
    for k in range(cfg.get("stripes", 0)):
        x = x1 - (k + 1) * (x1 - x0) / (cfg["stripes"] + 1)
        stroke(ctx, [(x, by - H), (x - 15, by + H)], 5, color=dk)
    if cfg.get("sheen"):
        stroke(ctx, [(x0 * 0.8, by - H * 0.05), (x1 * 0.9, by - H * 0.3)], H * 0.1, color=lighter(col, 0.5), a=0.8)
    if wings == "shell":
        stroke(ctx, [(x0, by - H * 0.1), (x1, by - H * 0.15)], 6, color=dk)
    ctx.restore()
    shape(ctx, lambda c: p_ellipse(c, hx, by - H * 0.05, hr, hr * 0.9), _c(cfg, "head", None) or dk, OUT,
          (0.08, 0.15))
    _face(ctx, cfg, p, hx + hr * 0.1, by - hr * 0.3, cfg.get("eye_r", hr * 0.32), dk, hr * 0.6)
    legs(False)
    _overlays(ctx, cfg, p, path, (x0 + x1) / 2, by, (x1 - x0) / 2, H / 2)


def arachnid(ctx, t, cfg, p):
    col = _c(cfg, "color", "#2b2b2e")
    dk = _c(cfg, "dark", None) or lighter(col, 0.25)
    acc = _c(cfg, "accent", "#e0261e")
    cr = p.get("crouch", 0.0)
    by = -320 + 80 * cr + 4 * math.sin(t * 2.6)
    cw, chh = cfg.get("ceph", (200, 150))
    ar = cfg.get("abdomen", 180)
    ll = cfg.get("leg_len", 1.0)
    big_abd = cfg.get("abdomen_front", False)
    if not big_abd:
        shape(ctx, lambda c: p_ellipse(c, 0, by - chh * 0.9, ar, ar * 0.7), col, OUT, (0.1, 0.15))
    for s in (-1, 1):
        for i in range(4):
            dx, dy = _walk(p, i, s > 0)
            front = i == 0
            hx, hy = s * (cw * 0.5 + i * 18), by + 20 + i * 12
            if front and p.get("wave", 0) > 0:
                w = 30 * math.sin(t * 10)
                pts = [(hx, hy), (s * 300, by - 180 - 80 * p["wave"] + w), (s * 380, by - 360 * p["wave"] + w)]
            else:
                pts = [(hx, hy), (s * (cw + 30 + i * 70) * ll, by - 120 * ll + i * 30 + 40 * cr),
                       (s * (cw + 60 + i * 95) * ll + dx, dy)]
            _banded(ctx, pts, cfg.get("leg_w", 22) * (1.3 if front else 1.0), col, dk if cfg.get("bands") else None)
    if big_abd:   # widow style: the big glossy abdomen faces you, the small body below it
        shape(ctx, lambda c: p_ellipse(c, 0, by - ar * 0.75, ar, ar * 1.05), col, OUT, (0.1, 0.15),
              hi=(0.3, 0.2, 0.18))
    path = lambda c: p_rrect(c, -cw, by - chh, 2 * cw, 2 * chh, chh * 0.8)  # noqa
    if big_abd:
        path = lambda c: p_ellipse(c, 0, by + chh * 0.4, cw * 0.55, chh * 0.6)  # noqa
    shape(ctx, path, col, OUT, (0.1, 0.12), hi=(0.3, 0.2, 0.2))
    pat = cfg.get("pattern")
    if pat == "hourglass":
        ay = by - ar * 0.75
        flat(ctx, lambda c: p_poly(c, [(-50, ay - 80), (50, ay - 80), (8, ay), (50, ay + 80), (-50, ay + 80),
                                       (-8, ay)]), acc, OUT * 0.5)
    elif pat == "stripe":
        stroke(ctx, [(0, by - chh - ar * 0.5), (0, by - chh * 0.9)], 30, color=acc)
    elif pat == "spots":
        for x in (-90, 0, 90):
            flat(ctx, lambda c, x=x: p_ellipse(c, x, by - chh - ar * 0.3, 20, 14), acc, OUT * 0.4)
    if cfg.get("fuzz"):
        for k in range(36):
            a = 2 * math.pi * k / 36
            x, y = cw * 1.02 * math.cos(a), by + chh * 1.02 * math.sin(a)
            stroke(ctx, [(x, y), (x + 16 * math.cos(a + 0.3), y + 16 * math.sin(a + 0.3))], 5, color=dk)
    fy = by + (chh * 0.9 if big_abd else chh)
    fc = _c(cfg, "fang_color", "#5a1a14")
    for s in (-1, 1):
        if cfg.get("fangs") == "big":
            shape(ctx, lambda c, s=s: p_ellipse(c, s * 45, fy + 20, 44, 58), fc, OUT * 0.7, (0.12, 0.1),
                  hi=(0.3, 0.2, 0.3))
        else:
            b = p.get("bite", 0.0)
            shape(ctx, lambda c, s=s: p_poly(c, [(s * 10, fy), (s * 38, fy), (s * 22, fy + 40 + 30 * b)]), fc,
                  OUT * 0.4, None)
    ey = by - (0 if not big_abd else -chh * 0.2)
    style = cfg.get("eyes", "pair")
    look = p.get("look", (0, 0))
    if style == "jumper":
        for s in (-1, 1):
            shape(ctx, lambda c, s=s: p_ellipse(c, s * cw * 0.84, ey - 40, 30, 30), INK, OUT * 0.5, None)
            ex = s * cw * 0.36
            shape(ctx, lambda c, ex=ex: p_ellipse(c, ex, ey, cw * 0.34, cw * 0.35), hexc("#1a1a1e"), OUT * 0.8, None)
            flat(ctx, lambda c, ex=ex: p_ellipse(c, ex + look[0] * 18, ey + look[1] * 18, cw * 0.22, cw * 0.22),
                 hexc("#3a2a20"))
            flat(ctx, lambda c, ex=ex: p_ellipse(c, ex - 20 + look[0] * 8, ey - 24 + look[1] * 8, 20, 22), (1, 1, 1))
            if p.get("blink", 0) > 0:
                flat(ctx, lambda c, ex=ex: p_ellipse(c, ex, ey, cw * 0.35, cw * 0.36), col)
    else:
        er = cfg.get("eye_r", 30 if not big_abd else 22)
        eyes(ctx, 0, ey, er, er * 1.4, look, (p.get("mood") or cfg.get("mood", "angry")), p.get("blink", 0), OUT * 0.5,
             lid=col)
        if style == "row":
            for k in range(4):
                flat(ctx, lambda c, k=k: p_ellipse(c, -66 + k * 44, ey + er * 2.1, 12, 12), INK)
    _overlays(ctx, cfg, p, path, 0, by, cw, chh)


def centipede(ctx, t, cfg, p):
    n = int(p.get("pairs", cfg.get("legs", 15)))
    L, H = cfg.get("length", 600), cfg.get("height", 110)
    col = _c(cfg, "color", "#cdb27c")
    dk = _c(cfg, "dark", None) or darker(col, 0.6)
    leg_c = _c(cfg, "leg_color", None) or lighter(col, 0.2)
    ll = cfg.get("leg_len", 1.0)
    ph = p.get("phase", 0.0)
    walking = p.get("walking", False)
    by = -(230 * ll if n else H * 0.5) + 4 * math.sin(t * 2)
    x0, x1 = -L / 2, L / 2
    segs = max(n, cfg.get("segments", 12))
    if not n:   # a worm: wriggling ringed tube
        pts = [(x0 + (x1 - x0) * k / 10, by + 18 * math.sin(t * 4 + k * 0.9)) for k in range(11)]
        stroke(ctx, pts, H + 2 * OUT, smooth=True)
        stroke(ctx, pts, H, smooth=True, color=col)
        for k in range(1, 10):
            x, y = pts[k]
            stroke(ctx, [(x, y - H * 0.45), (x, y + H * 0.45)], 4, color=dk)
        _face(ctx, cfg, p, x1 - H * 0.25, pts[-1][1] - H * 0.15, H * 0.2, col, H * 0.3)
        return
    hips = [(x1 - 40 - i * (L - 60) / n, by + 10) for i in range(n)]

    def leg(i, far):
        hx, hy = hips[i]
        reach = (560 - i * 85 * 14 / max(n - 1, 3)) * ll
        fx, fy = hx + reach * (0.85 if far else 1.0) - (40 if far else 0), -34.0 if far else 0.0
        q = ph * 1.4 - i * 0.75 + (math.pi if far else 0)
        if walking:
            fx += 55 * math.sin(q)
            fy = min(fy - 40 * max(0.0, math.cos(q)), 0.0)
        pts = [(hx, hy), (hx + (fx - hx) * 0.45, min(hy, fy) - (160 + abs(7 - i * 14 / max(n - 1, 3)) * 9) * ll),
               (fx, fy)]
        if i == n - 1 and cfg.get("long_last", True):
            sw = 20 * math.sin(t * 3 + far)
            pts = [(hx, hy), (hx - 280 * ll, by - 230 * ll + sw), (hx - 720 * ll, by - 120 * ll + sw),
                   (hx - 980 * ll, by - 20 + sw)]
        return pts
    for i in range(n):
        _banded(ctx, leg(i, True), 8, darker(leg_c, 0.75), darker(dk, 0.9) if cfg.get("bands", True) else None)
    A = cfg.get("ant", 760)
    for k in range(2 if A else 0):
        sw = 25 * math.sin(t * 2.5 + k)
        _banded(ctx, [(x1 + 50, by - 30), (x1 + 50 + A * 0.22, by - 260 - 70 * k), (x1 + 50 + A * 0.6, by - 330 - 90 * k + sw),
                      (x1 + 50 + A, by - 240 - 100 * k + sw)], 9, leg_c, dk if cfg.get("bands", True) else None)
    path = lambda c: p_rrect(c, x0, by - H / 2, L, H, H / 2)  # noqa
    shape(ctx, path, col, OUT, (0.0, 0.2), hi=(0.4, 0.2, 0.2))
    ctx.save()
    path(ctx)
    ctx.clip()
    for k in range(cfg.get("stripes", 3)):
        y = by - H * 0.3 + k * H * 0.3
        stroke(ctx, [(x0, y), (x1, y - 6)], H * 0.11, color=dk)
    for i in range(segs):
        x = x1 - i * L / segs
        stroke(ctx, [(x, by - H), (x - 6, by + H)], 4, color=darker(col, 0.8))
    ctx.restore()
    hr = H * 0.75
    shape(ctx, lambda c: p_ellipse(c, x1 + hr * 0.4, by - 8, hr, hr * 0.8), col, OUT, (0.08, 0.15))
    _face(ctx, cfg, p, x1 + hr * 0.5, by - hr * 0.35, hr * 0.32, col, hr * 0.55)
    for i in range(n):
        _banded(ctx, leg(i, False), 12, leg_c, dk if cfg.get("bands", True) else None)
    _overlays(ctx, cfg, p, path, 0, by, L / 2, H / 2)


def mite(ctx, t, cfg, p):
    col = _c(cfg, "color", "#f1e2c4")
    dk = _c(cfg, "dark", None) or darker(col, 0.85)
    if cfg.get("shape", "round") == "long":   # follicle mite: worm body, 8 stubby legs up front, side view
        L, H = cfg.get("length", 700), cfg.get("height", 150)
        by = -H * 0.5 - 40
        x0, x1 = -L / 2, L / 2
        wig = p.get("wiggle", 0.0) + (1.0 if p.get("walking") else 0.0)
        path = lambda c: p_smooth(c, [(x0, by), (x0 + 60, by - H * 0.35), (x1 - 240, by - H * 0.5),  # noqa
                                      (x1 - 40, by - H * 0.45), (x1, by - H * 0.1), (x1 - 30, by + H * 0.4),
                                      (x1 - 240, by + H * 0.5), (x0 + 60, by + H * 0.35)])
        for far in (True, False):
            for i in range(4):
                x = x1 - 90 - i * 55
                k = math.sin(t * 10 + i + far * 1.5) * 16 * wig
                limb(ctx, [(x, by + H * 0.3), (x + 10 + k, by + H * 0.6), (x + 22 + k, -4 - (12 if far else 0))],
                     18, dk if far else col, OUT * 0.55, smooth=False)
            if far:
                shape(ctx, path, col, OUT, (0.05, 0.18), hi=(0.4, 0.2, 0.2))
                ctx.save()
                path(ctx)
                ctx.clip()
                for x in range(int(x0) + 30, int(x1) - 260, 30):
                    stroke(ctx, [(x, by - H), (x + 8, by + H)], 4, color=dk)
                ctx.restore()
                shape(ctx, lambda c: p_ellipse(c, x1 + 8, by + 10, 26, 22), dk, OUT * 0.6, None)
                _face(ctx, cfg, p, x1 - 80, by - H * 0.12, H * 0.17, col, H * 0.3)
        _overlays(ctx, cfg, p, path, 0, by, L / 2, H / 2)
        return
    ph = p.get("phase", 0.0)
    wk = p.get("walking", False)
    rx, ry = cfg.get("rx", 250), cfg.get("ry", 195)
    by = -270 + (8 * math.sin(ph * 2) if wk else 5 * math.sin(t * 2.4))
    for s in (-1, 1):
        for i in range(4):
            dx, dy = _walk(p, i, s > 0)
            hx, hy = s * (rx * 0.6 + i * 14), by + 10 + i * 34
            kx, ky = s * (rx * 1.2 + i * 60), by - 110 + i * 45
            fx = s * (rx * 1.32 + i * 75) + dx
            limb(ctx, [(hx, hy), (kx, ky), (fx, dy)], 24, dk, OUT * 0.65, smooth=False)
            for u in (0.35, 0.7):
                x, y = kx + (fx - kx) * u, ky + (dy - ky) * u
                stroke(ctx, [(x, y), (x + s * 40, y - 30)], 4)
    path = lambda c: p_blob(c, 0, by, rx, ry, 0.04, seed=3)  # noqa
    shape(ctx, path, col, OUT, (0.1, 0.12), hi=(0.3, 0.25, 0.25))
    for k in range(3):
        stroke(ctx, [(-rx * 0.6 + k * 20, by - ry * 0.6 + k * 90), (0, by - ry * 0.5 + k * 90),
                     (rx * 0.6 - k * 20, by - ry * 0.6 + k * 90)], 4, smooth=True, color=dk)
    for k in range(9 if cfg.get("hairs", True) else 0):
        a = -math.pi * (0.1 + 0.8 * k / 8)
        x, y = rx * 0.95 * math.cos(a), by + ry * math.sin(a)
        stroke(ctx, [(x, y), (x * 1.3, by + ry * math.sin(a) * 1.35 + 10 * math.sin(t * 3 + k))], 5)
    shape(ctx, lambda c: p_ellipse(c, 0, by + ry * 0.5, 52, 38), dk, OUT * 0.7, None)
    _face(ctx, cfg, p, 0, by - ry * 0.3, cfg.get("eye_r", 40), col, ry * 0.78, side=False)
    if p.get("pellets"):
        for k in range(int(p["pellets"])):
            x, y = -rx * 1.4 - (k % 4) * 70, -30 - (k // 4) * 55
            shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 30, 24), hexc("#7a5a3c"), OUT * 0.5, (0.1, 0.2))
    _overlays(ctx, cfg, p, path, 0, by, rx, ry)


def fish(ctx, t, cfg, p):
    L, H = cfg.get("length", 600), cfg.get("height", 300)
    col = _c(cfg, "color", "#f29a3c")
    dk = _c(cfg, "dark", None) or darker(col, 0.75)
    wag = math.sin(t * 6) * 0.25
    x0, x1 = -L / 2, L / 2
    ctx.save()
    ctx.translate(x0 + 20, 0)
    ctx.rotate(wag)
    shape(ctx, lambda c: p_poly(c, [(0, 0), (-H * 0.7, -H * 0.55), (-H * 0.5, 0), (-H * 0.7, H * 0.55)]), dk, OUT,
          None)
    ctx.restore()
    shape(ctx, lambda c: p_poly(c, [(-L * 0.15, -H * 0.4), (L * 0.05, -H * 0.85), (L * 0.2, -H * 0.42)]), dk, OUT,
          None)
    path = lambda c: p_smooth(c, [(x0, 0), (x0 + L * 0.3, -H / 2), (x1 - L * 0.15, -H * 0.42), (x1, 0),  # noqa
                                  (x1 - L * 0.15, H * 0.42), (x0 + L * 0.3, H / 2)])
    shape(ctx, path, col, OUT, (0.0, 0.22), hi=(0.35, 0.2, 0.25))
    ctx.save()
    path(ctx)
    ctx.clip()
    for k in range(cfg.get("stripes", 0)):
        x = x1 - L * 0.3 - k * L * 0.18
        stroke(ctx, [(x, -H), (x - 20, H)], L * 0.06, color=_c(cfg, "accent", "#ffffff"))
    ctx.restore()
    shape(ctx, lambda c: p_poly(c, [(L * 0.05, H * 0.1), (-L * 0.1, H * 0.35), (L * 0.12, H * 0.25)]), dk, OUT * 0.7,
          None)
    if cfg.get("lure"):
        sw = 20 * math.sin(t * 2)
        stroke(ctx, [(x1 - L * 0.2, -H * 0.4), (x1 + 60, -H * 1.1 + sw), (x1 + 160, -H * 0.8 + sw)], 8, smooth=True)
        shape(ctx, lambda c: p_ellipse(c, x1 + 160, -H * 0.8 + sw, 34, 34), PAL["light"], OUT * 0.6, None)
        flat(ctx, lambda c: p_ellipse(c, x1 + 160, -H * 0.8 + sw, 90, 90), PAL["light"], a=0.25)
    _face(ctx, cfg, p, x1 - L * 0.2, -H * 0.12, cfg.get("eye_r", H * 0.12), col, H * 0.22)
    _overlays(ctx, cfg, p, path, 0, 0, L / 2, H / 2)


def bird(ctx, t, cfg, p):
    L, H = cfg.get("length", 420), cfg.get("height", 260)
    col = _c(cfg, "color", "#6b8fd1")
    dk = _c(cfg, "dark", None) or darker(col, 0.75)
    bel = _c(cfg, "belly", None) or lighter(col, 0.5)
    fly = p.get("fly", 0.0)
    by = -cfg.get("leg_len", 140) - H / 2 - (60 * fly)
    if not fly:
        for k in (-1, 1):
            stroke(ctx, [(k * 30, by + H * 0.4), (k * 30 + 10, -4)], 9, color=hexc("#e0a030"))
            stroke(ctx, [(k * 30 - 20, 0), (k * 30 + 50, 0)], 8, color=hexc("#e0a030"))
    shape(ctx, lambda c: p_poly(c, [(-L * 0.4, by), (-L * 0.85, by - H * 0.25), (-L * 0.8, by + H * 0.15)]), dk, OUT,
          None)
    path = lambda c: p_ellipse(c, 0, by, L / 2, H / 2)  # noqa
    shape(ctx, path, col, OUT, (0.0, 0.2))
    flat(ctx, lambda c: p_ellipse(c, L * 0.08, by + H * 0.18, L * 0.3, H * 0.28), bel)
    hx, hy, hr = L * 0.42, by - H * 0.42, H * 0.38
    beak = cfg.get("beak", "short")
    bl = {"short": hr * 0.8, "long": hr * 2.0, "hook": hr * 0.9}.get(beak, hr)
    shape(ctx, lambda c: p_poly(c, [(hx + hr * 0.8, hy - hr * 0.15), (hx + hr * 0.8 + bl, hy + (hr * 0.3 if beak == "hook" else 0.1)),
                                    (hx + hr * 0.8, hy + hr * 0.3)]), hexc("#f2b33d"), OUT * 0.8, None)
    shape(ctx, lambda c: p_ellipse(c, hx, hy, hr, hr), col, OUT, (0.08, 0.15))
    if cfg.get("crest"):
        for k in range(3):
            stroke(ctx, [(hx - 10, hy - hr * 0.8), (hx - 40 - k * 20, hy - hr * 1.6 + k * 15)], 10, color=dk)
    _face(ctx, cfg, p, hx + hr * 0.2, hy - hr * 0.15, hr * 0.32, col, hr * 0.5)
    flap = math.sin(t * 18) if fly else 0.2 * math.sin(t * 2)
    shape(ctx, lambda c: p_ellipse(c, -L * 0.08, by - H * 0.05 - 40 * flap, L * 0.32, H * 0.25, -0.3 - 0.6 * flap),
          dk, OUT, (0.0, 0.2))
    _overlays(ctx, cfg, p, path, 0, by, L / 2, H / 2)


def mammal(ctx, t, cfg, p):
    L, H = cfg.get("length", 520), cfg.get("height", 280)
    col = _c(cfg, "color", "#9a8a7a")
    dk = _c(cfg, "dark", None) or darker(col, 0.75)
    bel = _c(cfg, "belly", None) or lighter(col, 0.45)
    ll = cfg.get("leg_len", 110)
    by = -ll - H * 0.35 + 3 * math.sin(t * 2.5)
    tail = cfg.get("tail", "thin")
    sw = 20 * math.sin(t * 3)
    if tail == "fluffy":
        shape(ctx, lambda c: p_blob(c, -L * 0.62, by - H * 0.45 + sw * 0.5, L * 0.22, H * 0.55, 0.12, seed=4), col,
              OUT, (0.1, 0.1))
    else:
        stroke(ctx, [(-L * 0.45, by), (-L * 0.75, by + H * 0.1 + sw), (-L * 1.05, by - H * 0.2 + sw)],
               cfg.get("tail_w", 14), smooth=True, color=_c(cfg, "tail_color", None) or lighter(col, 0.3))
    for k, (x, far) in enumerate(((-L * 0.3, True), (L * 0.25, True), (-L * 0.25, False), (L * 0.3, False))):
        dx, dy = _walk(p, k, far)
        limb(ctx, [(x, by), (x + dx * 0.5, by + ll * 0.6), (x + dx, dy)], cfg.get("leg_w", 34),
             dk if far else col, OUT * 0.7)
    path = lambda c: p_ellipse(c, 0, by, L / 2, H / 2)  # noqa
    shape(ctx, path, col, OUT, (0.0, 0.2), hi=(0.35, 0.2, 0.22))
    flat(ctx, lambda c: p_ellipse(c, L * 0.05, by + H * 0.2, L * 0.32, H * 0.22), bel)
    hx, hy, hr = L * 0.48, by - H * 0.38, H * 0.48
    ears = cfg.get("ears", "round")
    for k, ex in enumerate((hx - hr * 0.5, hx + hr * 0.05)):
        if ears == "long":
            shape(ctx, lambda c, ex=ex: p_ellipse(c, ex, hy - hr * 1.3, hr * 0.28, hr * 0.85, -0.2), col, OUT,
                  (0.1, 0))
        elif ears == "pointed":
            shape(ctx, lambda c, ex=ex: p_poly(c, [(ex - hr * 0.35, hy - hr * 0.5), (ex, hy - hr * 1.4),
                                                   (ex + hr * 0.35, hy - hr * 0.5)]), col, OUT, None)
        else:
            shape(ctx, lambda c, ex=ex: p_ellipse(c, ex, hy - hr * 0.85, hr * 0.42, hr * 0.42), col, OUT, None)
            flat(ctx, lambda c, ex=ex: p_ellipse(c, ex, hy - hr * 0.85, hr * 0.24, hr * 0.24), hexc("#f2b5b5"))
    shape(ctx, lambda c: p_ellipse(c, hx, hy, hr, hr * 0.9), col, OUT, (0.08, 0.15))
    shape(ctx, lambda c: p_ellipse(c, hx + hr * 0.85, hy + hr * 0.25, hr * 0.45, hr * 0.32), bel, OUT * 0.8, None)
    flat(ctx, lambda c: p_ellipse(c, hx + hr * 1.25, hy + hr * 0.15, hr * 0.13, hr * 0.11), INK)
    if cfg.get("whiskers", True):
        for k in (-1, 0, 1):
            stroke(ctx, [(hx + hr * 1.05, hy + hr * 0.3), (hx + hr * 1.8, hy + hr * (0.3 + 0.2 * k))], 3)
    _face(ctx, cfg, p, hx + hr * 0.15, hy - hr * 0.2, hr * 0.3, col, hr * 0.62)
    _overlays(ctx, cfg, p, path, 0, by, L / 2, H / 2)


def reptile(ctx, t, cfg, p):
    L, H = cfg.get("length", 700), cfg.get("height", 170)
    col = _c(cfg, "color", "#6fae5a")
    dk = _c(cfg, "dark", None) or darker(col, 0.72)
    by = -H * 0.5 - cfg.get("leg_len", 60) + 3 * math.sin(t * 2)
    sw = 25 * math.sin(t * 2.5)
    if not cfg.get("shell"):
        shape(ctx, lambda c: p_smooth(c, [(-L * 0.35, by - H * 0.3), (-L * 0.8, by + sw * 0.5), (-L * 1.15, by + H * 0.1 + sw),
                                          (-L * 0.8, by + H * 0.25 + sw * 0.5), (-L * 0.35, by + H * 0.4)], close=True),
              col, OUT, (0, 0.2))
    for k, (x, far) in enumerate(((-L * 0.25, True), (L * 0.22, True), (-L * 0.2, False), (L * 0.27, False))):
        dx, dy = _walk(p, k, far)
        limb(ctx, [(x, by + H * 0.2), (x + 40 + dx * 0.5, by + H * 0.5), (x + 60 + dx, dy)], 30,
             dk if far else col, OUT * 0.7)
    if cfg.get("shell"):
        path = lambda c: p_smooth(c, [(-L * 0.42, by + H * 0.4), (-L * 0.3, by - H * 0.9), (L * 0.3, by - H * 0.9),  # noqa
                                      (L * 0.42, by + H * 0.4)])
        shape(ctx, path, _c(cfg, "accent", "#8a6a3c"), OUT, (0.05, 0.2), hi=(0.35, 0.2, 0.2))
        for x in (-L * 0.15, L * 0.15):
            stroke(ctx, [(x, by - H * 0.8), (x * 1.3, by + H * 0.35)], 6, color=darker(_c(cfg, "accent", "#8a6a3c")))
    else:
        path = lambda c: p_ellipse(c, 0, by, L * 0.42, H * 0.5)  # noqa
        shape(ctx, path, col, OUT, (0.0, 0.22), hi=(0.35, 0.2, 0.22))
        for k in range(cfg.get("spikes", 0)):
            x = -L * 0.3 + k * L * 0.6 / max(cfg["spikes"] - 1, 1)
            shape(ctx, lambda c, x=x: p_poly(c, [(x - 18, by - H * 0.45), (x, by - H * 0.85), (x + 18, by - H * 0.45)]),
                  dk, OUT * 0.6, None)
        for k in range(cfg.get("stripes", 0)):
            x = -L * 0.25 + k * 90
            stroke(ctx, [(x, by - H * 0.45), (x + 20, by + H * 0.4)], 12, color=dk)
    hx, hy, hr = L * 0.5, by - H * 0.15, H * 0.45
    shape(ctx, lambda c: p_rrect(c, hx - hr, hy - hr * 0.8, hr * 2.6, hr * 1.6, hr * 0.7), col, OUT, (0.08, 0.15))
    _face(ctx, cfg, p, hx + hr * 0.3, hy - hr * 0.35, hr * 0.32, col, hr * 0.7)
    _overlays(ctx, cfg, p, path, 0, by, L * 0.42, H * 0.5)


PLANS = {"insect": insect, "arachnid": arachnid, "centipede": centipede, "worm": centipede, "mite": mite,
         "fish": fish, "bird": bird, "mammal": mammal, "reptile": reptile}


def build(cfg):
    """An actor function (ctx, t, p) for one creature config."""
    plan = PLANS[cfg.get("plan", "insect")]
    if cfg.get("plan") == "worm":
        cfg = dict(cfg, legs=0)

    def actor(ctx, t, p):
        plan(ctx, t, cfg, p)
    actor.cfg = cfg
    return actor


def creature(ctx, t, p):
    """Generic actor: p["cfg"] is an inline config (or a SPECIES name)."""
    from drawn_species import SPECIES
    cfg = p.get("cfg", "roach")
    cfg = SPECIES[cfg] if isinstance(cfg, str) else cfg
    PLANS[cfg.get("plan", "insect")](ctx, t, dict(cfg, legs=0) if cfg.get("plan") == "worm" else cfg, p)
