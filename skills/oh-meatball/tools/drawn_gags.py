"""Fact gags for drawn Shorts (Nolan 10/28: "something is missing that other channels have").

Breakout drawn explainers SHOW each fact with a visual gag; ours only said it. Each gag here is a drawn actor whose
animation is driven by a numeric param that the line's "set" ramps (drawn.py interpolates numbers), plus a builder
that turns an outline line's `gag:` into actors and sound cues. No text anywhere (no pop-up text rule).

Outline usage (one dict or a list per line):
  gag: {pile: cube, n: 6}            objects pop out of the animal's rear and stack (cube, egg, rock, poop, coin,
                                     fish, bone, baby, leaf, tick, heart)
  gag: {zap: true}                   lightning bolts crackle out of the animal; everything flashes
  gag: {heart: 4}                    a big heart pounds next to the animal, N beats per second
  gag: {mark: sweat}                 a reaction on the animal's head: sweat, shock, hearts, anger, zzz, alarm, stars,
                                     stink, dizzy, ice (it follows the animal as it moves)
  gag: {meter: 1.0}                  a dial whose needle swings up to 0..1 and shakes in the red
  gag: {clock: 4}                    a clock whose hands spin N turns (time flying by)
  gag: {prop: trophy}                a prop pops in over the animal: trophy, magnifier, ruler, rock, skull, moon,
                                     snowflake, rocket, crown, bed
  gag: {thought: fish}               a thought bubble over the animal holding one of the pile objects
  any gag: at (default "20%"), dur, x/y nudges.
"""
import math

from drawn_kit import OUT, PAL, back_out, ease, hexc, ink, p_ellipse, p_poly, p_rrect, shape, src, stroke, starburst, sweat

P = PAL
OBJ = {  # kind -> fill colour
    "cube": "#8a6440", "egg": "#f5ecd8", "rock": "#8d8f94", "poop": "#6e4a2c", "coin": "#f2c94c", "fish": "#7fb3d5",
    "bone": "#f1ead9", "baby": "#d9b08c", "leaf": "#6aa84f", "tick": "#5a3b2a", "heart": "#e2504c",
}


def _heart_path(c, x, y, r):
    c.move_to(x, y + r * 0.9)
    c.curve_to(x - r * 1.6, y - r * 0.2, x - r * 0.7, y - r * 1.3, x, y - r * 0.45)
    c.curve_to(x + r * 0.7, y - r * 1.3, x + r * 1.6, y - r * 0.2, x, y + r * 0.9)
    c.close_path()


def obj(ctx, kind, x, y, r, rot=0.0):
    """One small object, centred at x, y, radius ~r."""
    col = hexc(OBJ.get(kind, "#999999"))
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    if kind == "cube":
        shape(ctx, lambda c: p_rrect(c, -r, -r, 2 * r, 2 * r, r * 0.18), col, OUT * 0.7, (0.12, 0.12), hi=(0.3, 0.3, 0.2))
    elif kind in ("egg", "baby"):
        shape(ctx, lambda c: p_ellipse(c, 0, 0, r * 0.8, r), col, OUT * 0.7, (0.1, 0.1), hi=(0.3, 0.3, 0.25))
        if kind == "baby":
            for sx in (-0.3, 0.3):
                shape(ctx, lambda c, sx=sx: p_ellipse(c, sx * r, -r * 0.25, r * 0.12, r * 0.12), (0.1, 0.1, 0.1), 0)
    elif kind == "rock":
        shape(ctx, lambda c: p_poly(c, [(-r, r * 0.5), (-r * 0.7, -r * 0.6), (r * 0.2, -r * 0.9), (r, -r * 0.1),
                                        (r * 0.8, r * 0.6)]), col, OUT * 0.7, (0.15, 0.15))
    elif kind == "poop":
        for k, (yy, rr) in enumerate(((r * 0.4, r), (-r * 0.25, r * 0.72), (-r * 0.8, r * 0.42))):
            shape(ctx, lambda c, yy=yy, rr=rr: p_ellipse(c, 0, yy, rr, rr * 0.55), col, OUT * 0.6, (0.12, 0.12))
    elif kind == "coin":
        shape(ctx, lambda c: p_ellipse(c, 0, 0, r, r), col, OUT * 0.7, (0.12, 0.12), hi=(0.3, 0.3, 0.3))
    elif kind == "fish":
        shape(ctx, lambda c: (p_ellipse(c, 0, 0, r, r * 0.5)), col, OUT * 0.6, (0.12, 0.12))
        shape(ctx, lambda c: p_poly(c, [(r * 0.8, 0), (r * 1.5, -r * 0.5), (r * 1.5, r * 0.5)]), col, OUT * 0.6, None)
    elif kind == "bone":
        shape(ctx, lambda c: p_rrect(c, -r, -r * 0.2, 2 * r, r * 0.4, r * 0.2), col, OUT * 0.6, None)
        for sx in (-1, 1):
            for sy in (-1, 1):
                shape(ctx, lambda c, sx=sx, sy=sy: p_ellipse(c, sx * r, sy * r * 0.25, r * 0.3, r * 0.3), col, OUT * 0.6, None)
    elif kind == "leaf":
        shape(ctx, lambda c: p_ellipse(c, 0, 0, r, r * 0.45, 0.5), col, OUT * 0.6, (0.12, 0.12))
    elif kind == "tick":
        shape(ctx, lambda c: p_ellipse(c, 0, 0, r * 0.8, r * 0.6), col, OUT * 0.6, None)
        for k in range(4):
            for sx in (-1, 1):
                stroke(ctx, [(sx * r * 0.5, (k - 1.5) * r * 0.3), (sx * r * 1.1, (k - 1.5) * r * 0.45)], 4)
    elif kind == "heart":
        shape(ctx, lambda c: _heart_path(c, 0, 0, r * 0.8), col, OUT * 0.7, (0.12, 0.12), hi=(0.3, 0.3, 0.25))
    ctx.restore()


def pile(ctx, t, p):
    """Objects fly out of the source (sx, sy, relative) in an arc and stack into a little pyramid at the origin.
    p: kind, n (ramped 0..N), r (object radius), sx, sy."""
    kind, n, r = p.get("kind", "cube"), p.get("n", 0.0), p.get("r", 34)
    sx, sy = p.get("sx", -220), p.get("sy", -120)
    slots, row, x0 = [], 0, 0
    while len(slots) < 40:
        cnt = max(1, 5 - row)
        for i in range(cnt):
            slots.append(((i - (cnt - 1) / 2) * r * 2.05, -r - row * r * 1.95))
        row += 1
    for i in range(int(math.ceil(n))):
        u = min(1.0, (n - i) * 2.2)   # each object takes ~0.45 of a step to fly in
        tx, ty = slots[i]
        x = sx + (tx - sx) * u
        y = sy + (ty - sy) * u - 260 * 4 * u * (1 - u)
        sc = back_out(min(1.0, u * 1.4))
        obj(ctx, kind, x, y, r * max(0.2, sc), (1 - u) * 3.0)


def bolt(ctx, t, p):
    """Crackling lightning bolts radiating from the origin; on (0..1) fades them, len is the reach."""
    on = p.get("on", 0.0)
    if on <= 0:
        return
    reach = p.get("len", 420)
    seed = int(t * 18)
    for k in range(p.get("count", 5)):
        a = (k / 5) * 2 * math.pi + 0.5 * math.sin(seed * 1.7 + k)
        pts, x, y = [(0, 0)], 0.0, 0.0
        for j in range(1, 7):
            d = reach * j / 6
            jit = 40 * math.sin(seed * 3.1 + k * 7 + j * 2.3)
            x, y = d * math.cos(a) - jit * math.sin(a), d * math.sin(a) + jit * math.cos(a)
            pts.append((x, y))
        stroke(ctx, pts, 22, color=(1.0, 0.95, 0.5), a=0.45 * on)
        stroke(ctx, pts, 9, color=(1.0, 1.0, 0.85), a=on)
    ctx.save()
    p_ellipse(ctx, 0, 0, 140, 140)
    src(ctx, (1.0, 0.98, 0.7), 0.25 * on * (0.6 + 0.4 * math.sin(t * 40)))
    ctx.fill()
    ctx.restore()


def big_heart(ctx, t, p):
    """A pounding heart; rate = beats per second, on fades it in."""
    on = p.get("on", 0.0)
    if on <= 0:
        return
    beat = abs(math.sin(math.pi * t * p.get("rate", 2.0))) ** 6
    r = 120 * (0.9 + 0.22 * beat) * back_out(min(1.0, on))
    shape(ctx, lambda c: _heart_path(c, 0, 0, r), hexc("#e2504c"), OUT, (0.15, 0.15), hi=(0.32, 0.3, 0.3))
    for k in range(3):
        a = -0.6 + k * 0.6
        stroke(ctx, [(r * 1.3 * math.cos(a - 1.57), r * 1.3 * math.sin(a - 1.57)),
                     ((r * 1.3 + 50 * beat) * math.cos(a - 1.57), (r * 1.3 + 50 * beat) * math.sin(a - 1.57))], 8, a=beat)


def mark(ctx, t, p):
    """A reaction drawn over the animal's head; on scales it in."""
    on = p.get("on", 0.0)
    if on <= 0:
        return
    s = back_out(min(1.0, on)) * p.get("size", 1.0)
    kind = p.get("kind", "sweat")
    ctx.save()
    ctx.scale(s, s)
    if kind == "sweat":
        for k, (x, y) in enumerate(((-90, -10), (80, -40), (20, -110))):
            sweat(ctx, x, y + 20 * math.sin(t * 6 + k), 36)
    elif kind == "shock":
        for k in range(9):
            a = math.pi + k * math.pi / 8
            r0 = 90 + 12 * math.sin(t * 20 + k)
            stroke(ctx, [(r0 * math.cos(a), r0 * math.sin(a)), ((r0 + 70) * math.cos(a), (r0 + 70) * math.sin(a))], 10)
    elif kind == "hearts":
        for k in range(3):
            u = (t * 0.7 + k / 3) % 1
            x = -80 + k * 80 + 20 * math.sin(t * 3 + k)
            ctx.save()
            ctx.translate(x, -u * 220)
            shape(ctx, lambda c: _heart_path(c, 0, 0, 34), hexc("#e2504c"), OUT * 0.7, None, a=1 - u)
            ctx.restore()
    elif kind == "anger":
        c = hexc("#d8322a")
        for sx in (-1, 1):
            for sy in (-1, 1):
                stroke(ctx, [(sx * 18, sy * 60), (sx * 18, sy * 18), (sx * 60, sy * 18)], 14, color=c)
    elif kind == "zzz":
        for k in range(3):
            u = (t * 0.6 + k / 3) % 1
            z = 26 + 14 * k
            x, y = 40 * k + 30 * u, -60 * k - 120 * u
            stroke(ctx, [(x - z, y - z), (x + z, y - z), (x - z, y + z), (x + z, y + z)], 9, a=1 - u * 0.7)
    elif kind == "alarm":
        for k in range(3):
            x = (k - 1) * 70
            j = 6 * math.sin(t * 30 + k)
            shape(ctx, lambda c, x=x, j=j: p_poly(c, [(x - 16 + j, -150), (x + 16 + j, -150), (x + 6, -40), (x - 6, -40)]),
                  P["red"], OUT * 0.6, None)
            shape(ctx, lambda c, x=x: p_ellipse(c, x, -10, 16, 16), P["red"], OUT * 0.6, None)
    elif kind == "stars":
        for k in range(5):
            a = t * 3 + k * 2 * math.pi / 5
            starburst(ctx, 130 * math.cos(a), -20 + 40 * math.sin(a), 28, 5, (1, 0.86, 0.2), OUT * 0.5, a)
    elif kind == "stink":
        for k in range(3):
            x = (k - 1) * 70
            pts = [(x + 22 * math.sin(t * 4 + j * 0.9 + k), -j * 30) for j in range(8)]
            stroke(ctx, pts, 12, smooth=True, color=hexc("#8bbf5a"))
    elif kind == "dizzy":
        for k in range(4):
            a = t * 4 + k * math.pi / 2
            p_ellipse(ctx, 110 * math.cos(a), -10 + 30 * math.sin(a), 18, 18)
            src(ctx, (1, 0.86, 0.2))
            ctx.fill_preserve()
            ink(ctx, OUT * 0.5)
            ctx.stroke()
    elif kind == "ice":
        for k in range(6):
            a = k * math.pi / 3
            stroke(ctx, [(0, -60), (80 * math.cos(a), -60 + 80 * math.sin(a))], 10, color=hexc("#9fd3ee"))
    ctx.restore()


def meter(ctx, t, p):
    """A dial; v (0..1) swings the needle, shaking when it hits the red."""
    on = p.get("on", 1.0)
    if on <= 0:
        return
    v = p.get("v", 0.0)
    R = 170
    ctx.save()
    ctx.scale(back_out(min(1.0, on)), back_out(min(1.0, on)))
    shape(ctx, lambda c: (c.arc(0, 0, R, math.pi, 2 * math.pi), c.close_path()), hexc("#f6f1e4"), OUT, None)
    for k, col in enumerate(("#6aa84f", "#f2c94c", "#d8322a")):
        ctx.save()
        ctx.arc(0, 0, R - 26, math.pi + k * math.pi / 3, math.pi + (k + 1) * math.pi / 3)
        ctx.set_line_width(30)
        src(ctx, hexc(col))
        ctx.stroke()
        ctx.restore()
    jit = 0.06 * math.sin(t * 50) if v > 0.9 else 0.0
    a = math.pi + math.pi * min(1.0, v) + jit
    stroke(ctx, [(0, 0), ((R - 30) * math.cos(a), (R - 30) * math.sin(a))], 12, color=hexc("#3a2a1e"))
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 20, 20), hexc("#3a2a1e"), 0, None)
    ctx.restore()


def clock(ctx, t, p):
    """A wall clock; turns (ramped) spins the minute hand that many times, the hour hand 1/12 as fast."""
    on = p.get("on", 1.0)
    if on <= 0:
        return
    turns = p.get("turns", 0.0)
    ctx.save()
    sc = back_out(min(1.0, on))
    ctx.scale(sc, sc)
    shape(ctx, lambda c: p_ellipse(c, 0, 0, 150, 150), hexc("#f6f1e4"), OUT, (0.08, 0.08))
    for k in range(12):
        a = k * math.pi / 6
        stroke(ctx, [(120 * math.cos(a), 120 * math.sin(a)), (138 * math.cos(a), 138 * math.sin(a))], 7)
    am = -math.pi / 2 + turns * 2 * math.pi
    ah = -math.pi / 2 + turns * 2 * math.pi / 12
    stroke(ctx, [(0, 0), (110 * math.cos(am), 110 * math.sin(am))], 9)
    stroke(ctx, [(0, 0), (70 * math.cos(ah), 70 * math.sin(ah))], 13)
    ctx.restore()


def prop(ctx, t, p):
    """A single prop that pops in (on) and bobs."""
    on = p.get("on", 0.0)
    if on <= 0:
        return
    kind = p.get("kind", "trophy")
    s = back_out(min(1.0, on))
    ctx.save()
    ctx.translate(0, 10 * math.sin(t * 2.5))
    ctx.scale(s, s)
    gold = hexc("#f2c94c")
    if kind == "trophy":
        shape(ctx, lambda c: p_poly(c, [(-90, -160), (90, -160), (60, -40), (-60, -40)]), gold, OUT, (0.15, 0.15), hi=(0.3, 0.3, 0.2))
        for sx in (-1, 1):
            ctx.save()
            ctx.arc(sx * 95, -110, 40, 0, 2 * math.pi)
            ink(ctx, 14)
            ctx.stroke()
            ctx.restore()
        shape(ctx, lambda c: p_rrect(c, -18, -40, 36, 50, 6), gold, OUT, None)
        shape(ctx, lambda c: p_rrect(c, -70, 10, 140, 40, 8), hexc("#8a5a30"), OUT, None)
        starburst(ctx, 0, -110, 26, 5, (1, 1, 1), OUT * 0.4, t)
    elif kind == "magnifier":
        ctx.save()
        ctx.arc(0, -60, 90, 0, 2 * math.pi)
        src(ctx, (0.75, 0.9, 1.0), 0.45)
        ctx.fill_preserve()
        ink(ctx, 18)
        ctx.stroke()
        ctx.restore()
        stroke(ctx, [(64, 4), (150, 90)], 30, color=hexc("#8a5a30"))
    elif kind == "ruler":
        shape(ctx, lambda c: p_rrect(c, -200, -40, 400, 60, 6), hexc("#f2d36b"), OUT, None)
        for k in range(17):
            stroke(ctx, [(-190 + k * 23.75, -40), (-190 + k * 23.75, -40 + (28 if k % 4 == 0 else 16))], 5)
    elif kind in ("rock", "skull", "snowflake", "rocket", "crown", "moon", "bed"):
        if kind == "rock":
            obj(ctx, "rock", 0, -60, 80)
        elif kind == "skull":
            shape(ctx, lambda c: p_ellipse(c, 0, -80, 80, 70), hexc("#f1ead9"), OUT, (0.1, 0.1))
            shape(ctx, lambda c: p_rrect(c, -40, -30, 80, 40, 10), hexc("#f1ead9"), OUT, None)
            for sx in (-1, 1):
                shape(ctx, lambda c, sx=sx: p_ellipse(c, sx * 30, -85, 20, 22), (0.15, 0.12, 0.1), 0, None)
        elif kind == "snowflake":
            for k in range(6):
                a = k * math.pi / 3 + t * 0.5
                stroke(ctx, [(0, -60), (90 * math.cos(a), -60 + 90 * math.sin(a))], 12, color=hexc("#9fd3ee"))
        elif kind == "rocket":
            shape(ctx, lambda c: p_poly(c, [(0, -220), (45, -120), (45, 0), (-45, 0), (-45, -120)]), hexc("#e8e8ec"), OUT, (0.12, 0.12))
            shape(ctx, lambda c: p_ellipse(c, 0, -120, 22, 22), hexc("#7fb3d5"), OUT * 0.7, None)
            for k in range(3):
                shape(ctx, lambda c, k=k: p_ellipse(c, (k - 1) * 22, 30 + 20 * abs(math.sin(t * 20 + k)), 18, 40),
                      hexc("#f29b38"), 0, None)
        elif kind == "crown":
            shape(ctx, lambda c: p_poly(c, [(-110, 0), (-110, -110), (-55, -50), (0, -130), (55, -50), (110, -110),
                                            (110, 0)]), gold, OUT, (0.15, 0.15), hi=(0.3, 0.3, 0.2))
        elif kind == "moon":
            shape(ctx, lambda c: p_ellipse(c, 0, -60, 100, 100), hexc("#f6efc2"), OUT, (0.1, 0.1))
        elif kind == "bed":
            shape(ctx, lambda c: p_rrect(c, -180, -80, 360, 80, 12), hexc("#5a7fbf"), OUT, None)
            shape(ctx, lambda c: p_rrect(c, -170, -120, 120, 50, 20), hexc("#f6f1e4"), OUT, None)
    ctx.restore()


def thought(ctx, t, p):
    """A thought bubble over the head holding one object (kind); on pops it in."""
    on = p.get("on", 0.0)
    if on <= 0:
        return
    s = back_out(min(1.0, on))
    ctx.save()
    ctx.scale(s, s)
    for (x, y, r) in ((0, 0, 18), (34, -46, 28)):
        shape(ctx, lambda c, x=x, y=y, r=r: p_ellipse(c, x, y, r, r), (1, 1, 1), OUT * 0.7, None)
    shape(ctx, lambda c: p_ellipse(c, 90, -170, 140, 100), (1, 1, 1), OUT * 0.8, None)
    obj(ctx, p.get("kind", "fish"), 90, -170 + 6 * math.sin(t * 4), 52)
    ctx.restore()


ACTORS = {"g.pile": pile, "g.bolt": bolt, "g.heart": big_heart, "g.mark": mark, "g.meter": meter, "g.clock": clock,
          "g.prop": prop, "g.thought": thought}

# Soft cues only (Nolan 10/28 "get rid of the loud beeps"): no zap crackle, one click per clock.
SFX = {"pile": ["pop@{a}", "pop@{b}", "tink@{c}"], "zap": ["thud@{a}"], "heart": ["thud@{a}", "thud@{b}"],
       "mark": ["tink@{a}"], "meter": ["whoosh@{a}", "thud@{c}"], "clock": ["click@{a}"],
       "prop": ["tink@{a}"], "thought": ["pop@{a}"]}


def _pct(at, off):
    if isinstance(at, str) and "|" in at:   # "word#n|pct" (drawn_acting.auto_gag): offset both forms
        w, p = at.split("|", 1)
        return f"{w}+{off * 0.02:g}|{_pct(p, off)}"
    if isinstance(at, str) and at.endswith("%"):
        return f"{min(97, float(at[:-1]) + off):g}%"
    return at


def build(gags, hero, top_dy, face_left=True, tag="g"):
    """Outline `gag:` -> (actors, sfx). hero: the line's hero actor (gags follow it through "attach");
    top_dy: offset from the hero's feet to just above its head (negative, world px)."""
    gags = gags if isinstance(gags, list) else [gags]
    actors, sfx = [], []
    hx, hy = hero["pos"]
    for mv in hero.get("moves", []):   # place gags where the animal ends up, not where it starts
        if "pos" in mv:
            hx, hy = mv["pos"]
    back = 1 if face_left else -1    # the animal's rear is on the right when it faces left
    for k, g in enumerate(gags):
        at = g.get("at", "20%")
        dur = g.get("dur", 1.4)
        gid = f"{tag}-gag{k}"   # unique per line, so a later line never inherits this gag's state
        cues = {"a": at, "b": _pct(at, 15), "c": _pct(at, 30)}
        kind = next(x for x in ("pile", "zap", "heart", "mark", "meter", "clock", "prop", "thought") if x in g)
        sfx += [c.format(**cues) for c in SFX[kind]]
        a = {"id": gid, "type": "g." + ("bolt" if kind == "zap" else kind), "s": g.get("s", 1.0), "front": True}
        if kind == "pile":
            n = g.get("n", 6)
            px = max(170, min(910, hx + back * (230 + g.get("x", 0))))
            a.update(pos=[px, hy + 40 + g.get("y", 0)],
                     p={"kind": g["pile"], "n": 0.0, "r": g.get("r", 50), "sx": hx - px, "sy": top_dy * 0.35},
                     set=[{"at": at, "dur": dur, "p": {"n": float(n)}}])
        elif kind == "zap":
            a.update(attach="hero", pos=[g.get("x", 0), top_dy * 0.45 + g.get("y", 0)], p={"on": 0.0, "len": g.get("len", 460)},
                     set=[{"at": at, "dur": 0.1, "p": {"on": 1.0}}, {"at": _pct(at, 45), "dur": 0.3, "p": {"on": 0.0}}])
        elif kind == "heart":
            a.update(attach="hero", pos=[g.get("x", -back * 30), top_dy - 150 + g.get("y", 0)],
                     p={"on": 0.0, "rate": float(g["heart"])}, set=[{"at": at, "dur": 0.4, "p": {"on": 1.0}}])
        elif kind == "mark":
            a.update(attach="hero", pos=[g.get("x", 0), top_dy + g.get("y", 0)], p={"on": 0.0, "kind": g["mark"]},
                     set=[{"at": at, "dur": 0.3, "p": {"on": 1.0}}])
        elif kind == "meter":
            a.update(pos=[g.get("x", 820), hy + top_dy - 120 + g.get("y", 0)], p={"on": 0.0, "v": 0.0},
                     set=[{"at": at, "dur": 0.3, "p": {"on": 1.0}}, {"at": _pct(at, 8), "dur": dur, "p": {"v": float(g["meter"])}}])
        elif kind == "clock":
            a.update(pos=[g.get("x", 820), hy + top_dy - 140 + g.get("y", 0)], p={"on": 0.0, "turns": 0.0},
                     set=[{"at": at, "dur": 0.3, "p": {"on": 1.0}}, {"at": _pct(at, 5), "dur": dur, "p": {"turns": float(g["clock"])}}])
        elif kind == "prop":
            a.update(attach="hero", pos=[g.get("x", 0), top_dy - 40 + g.get("y", 0)], p={"on": 0.0, "kind": g["prop"]},
                     set=[{"at": at, "dur": 0.35, "p": {"on": 1.0}}])
        elif kind == "thought":
            a.update(attach="hero", pos=[g.get("x", -back * 60), top_dy + g.get("y", 0)], p={"on": 0.0, "kind": g["thought"]},
                     set=[{"at": at, "dur": 0.35, "p": {"on": 1.0}}])
        actors.append(a)
    return actors, sfx
