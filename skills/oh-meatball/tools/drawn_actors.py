"""Animal and prop actors for tools/drawn.py (house-and-garden cast). Each draws at its base point (y = 0 is
the ground or the anchor it hangs from) in local units, in the drawn_kit style. p = the spec's params plus
the per-frame values drawn.py adds ("phase" = walk cycle, "blink" 0..1, "talk" 0..1)."""
import math

from drawn_kit import (OUT, PAL, eyes, flat, ink, limb, mouth, p_ellipse, p_poly, p_rrect, shape, src, stroke,
                       sweat, starburst)

P = PAL


def _leg_ik(hip, foot, knee_h):
    """A harvestman-style leg: up from the hip to a high knee, then down to the foot."""
    kx = hip[0] + (foot[0] - hip[0]) * 0.45
    return [hip, (kx, min(hip[1], foot[1]) - knee_h), foot]


def harvestman(ctx, t, p):
    """Harvestman (Opiliones): ONE fused oval body, two eyes on a little turret, eight very long legs.
    p: mood, phase (walk), wave (0..1 lifts the front-right leg), xray (0..1), look, talk."""
    ph = p.get("phase", 0.0)
    walking = p.get("walking", False)
    bob = 6 * math.sin(ph * 2) if walking else 3 * math.sin(t * 2.2)
    by = -190 + bob
    wave = p.get("wave", 0.0)
    feet = [(-400, 0), (-300, 0), (-190, 0), (-90, 0), (90, 0), (190, 0), (300, 0), (420, 0)]
    hips = [(-30, by + 8), (-22, by + 2), (-14, by - 2), (-6, by - 4), (6, by - 4), (14, by - 2), (22, by + 2),
            (30, by + 8)]
    order = [0, 4, 2, 6, 1, 5, 3, 7]
    for k, i in enumerate(order):
        fx, fy = feet[i]
        if walking:
            q = ph + (k % 2) * math.pi
            fx += 26 * math.sin(q)
            fy -= 22 * max(0.0, math.cos(q))
        hip = hips[i]
        knee_h = 150 + 30 * (i in (1, 6))
        pts = _leg_ik(hip, (fx, fy), knee_h)
        if i == 7 and wave > 0:  # waving hello with a leg
            w = math.sin(t * 9) * 25
            pts = [hip, (hip[0] + 150, by - 230 - 60 * wave), (hip[0] + 310, by - 170 - 190 * wave + w)]
        limb(ctx, pts, 7, P["harv_dk"], OUT * 0.55)
    xr = p.get("xray", 0.0)
    body = (lambda c: p_ellipse(c, 0, by, 78, 58))
    shape(ctx, body, P["harv"], OUT, (0.1, 0.14), hi=(0.32, 0.25, 0.22))
    if xr > 0:
        ctx.save()
        body(ctx)
        src(ctx, (0.55, 0.85, 1.0), 0.85 * xr)
        ctx.fill_preserve()
        ink(ctx, OUT)
        ctx.stroke()
        # empty inside where glands would be: a dashed outline circle with a slash
        ctx.set_dash([10, 8])
        p_ellipse(ctx, 0, by + 10, 30, 22)
        ink(ctx, 5, xr)
        ctx.stroke()
        ctx.set_dash([])
        stroke(ctx, [(-26, by + 28), (26, by - 8)], 7, color=P["red"], a=xr)
        ctx.restore()
    # turret with eyes on top
    shape(ctx, lambda c: p_ellipse(c, 0, by - 58, 34, 22), P["harv_lt"], OUT * 0.8, None)
    eyes(ctx, 0, by - 70, 20, 21, p.get("look", (0, 0)), p.get("mood", "happy"), p.get("blink", 0), OUT * 0.6,
         lid=P["harv_lt"])
    mouth(ctx, 0, by + 18, 34, p.get("mouth", "smile"), p.get("talk", 0.0), OUT * 0.6)


def cellar_spider(ctx, t, p):
    """Cellar spider (Pholcus): small round head part + long pale abdomen, eight hair-thin legs, hanging
    from its web (y = 0 is the thread anchor above it). p: mood, shiver (the real whirl defence), fangs (0..1)."""
    sh = p.get("shiver", 0.0)
    jx = sh * 18 * math.sin(t * 40)
    jy = sh * 10 * math.cos(t * 33)
    cy = 260 + 8 * math.sin(t * 1.6)
    stroke(ctx, [(0, 0), (jx, cy - 40 + jy)], 3, color=(1, 1, 1), a=0.9)
    ctx.save()
    ctx.translate(jx, jy)
    spread = [(-330, -150), (-380, 40), (-340, 210), (-250, 330), (250, 330), (340, 210), (380, 40), (330, -150)]
    for i, (fx, fy) in enumerate(spread):
        hip = (-8 if i < 4 else 8, cy + 6)
        side = -1 if i < 4 else 1
        knee = (hip[0] + fx * 0.42 + side * 20, cy + fy * 0.3 - 140 + 4 * math.sin(t * 3 + i))
        limb(ctx, [hip, knee, (fx, cy + fy)], 4, P["cell_dk"], OUT * 0.45)
    # abdomen hangs below
    shape(ctx, lambda c: p_ellipse(c, 0, cy + 95, 40, 82), P["cell"], OUT * 0.85, (0.12, 0.08))
    for k in range(3):
        flat(ctx, lambda c, k=k: p_ellipse(c, 0, cy + 60 + k * 34, 16 - k * 2, 8), P["cell_mark"])
    shape(ctx, lambda c: p_ellipse(c, 0, cy, 44, 38), P["cell"], OUT * 0.85, (0.1, 0.12))
    eyes(ctx, 0, cy - 6, 15, 16, p.get("look", (0, 0)), p.get("mood", "worry"), p.get("blink", 0), OUT * 0.5,
         lid=P["cell"])
    f = p.get("fangs", 0.0)
    if f > 0:
        for s in (-1, 1):
            shape(ctx, lambda c, s=s: p_poly(c, [(s * 6, cy + 22), (s * 18, cy + 22), (s * 10, cy + 22 + 22 * f)]),
                  (0.3, 0.12, 0.08), OUT * 0.4, None)
        shape(ctx, lambda c: p_ellipse(c, 12, cy + 52 * f, 5, 7), (0.5, 0.85, 0.35), OUT * 0.35, None, a=f)
    else:
        mouth(ctx, 0, cy + 22, 18, p.get("mouth", "wobble"), p.get("talk", 0.0), OUT * 0.45)
    ctx.restore()


def web(ctx, t, p):
    """A messy cellar-spider web in a ceiling corner, centred on the anchor, radius ~420."""
    ctx.save()
    a = 0.75
    for k in range(9):
        ang = math.pi * (0.05 + 0.9 * k / 8)
        stroke(ctx, [(0, -60), (430 * math.cos(ang), 430 * math.sin(ang) - 60)], 2.4, color=(1, 1, 1), a=a)
    for r in (110, 190, 270, 360):
        pts = [(r * math.cos(math.pi * (0.05 + 0.9 * k / 8)) + 6 * math.sin(k * 7 + r),
                r * math.sin(math.pi * (0.05 + 0.9 * k / 8)) - 60) for k in range(9)]
        stroke(ctx, pts, 2.0, smooth=True, color=(1, 1, 1), a=a * 0.8)
    ctx.restore()


def chair(ctx, t, p):
    """A plain wooden kitchen chair, seat top at y = -440, 400 wide."""
    for x in (-170, 140):
        shape(ctx, lambda c, x=x: c.rectangle(x, -440, 34, 440), P["wood_dk"], OUT * 0.8, None)
    for x in (-150, 120):
        shape(ctx, lambda c, x=x: c.rectangle(x, -900, 30, 470), P["wood_dk"], OUT * 0.8, None)
    for y in (-880, -780):
        shape(ctx, lambda c, y=y: p_rrect(c, -160, y, 320, 50, 12), P["wood"], OUT * 0.8, (0, 0.2))
    shape(ctx, lambda c: p_rrect(c, -205, -470, 410, 52, 14), P["wood"], OUT * 0.85, (0, 0.25))
    shape(ctx, lambda c: c.rectangle(-160, -190, 330, 22), P["wood_dk"], OUT * 0.6, None)


def arm(ctx, t, p):
    """A generic person's forearm reaching in from the left (no face, no likeness). The bite spot fades
    in at p['burn'] (0..1) and out again; y = 0 is the arm's centre line, the hand at x = 0."""
    shape(ctx, lambda c: p_rrect(c, -1500, -95, 1250, 190, 95), P["skin"], OUT, (0, 0.18))
    shape(ctx, lambda c: p_rrect(c, -1500, -118, 420, 236, 30), P["curtain"], OUT, (0, 0.18))
    def hand(c):
        p_rrect(c, -300, -120, 260, 230, 100)
    shape(ctx, hand, P["skin"], OUT, (0.05, 0.18))
    for k in range(4):
        y = -100 + k * 58
        shape(ctx, lambda c, y=y: p_rrect(c, -80, y, 150, 50, 25), P["skin"], OUT * 0.8, (0, 0.2))
    b = p.get("burn", 0.0)
    if b > 0:
        ctx.save()
        p_ellipse(ctx, -620, -20, 40 * b, 30 * b)
        src(ctx, P["burn"], 0.35 * b)
        ctx.fill()
        p_ellipse(ctx, -620, -20, 13, 10)
        src(ctx, P["burn"], b)
        ctx.fill()
        ctx.restore()
        if p.get("ouch", 0) > 0:
            starburst(ctx, -620, -190, 70 * p["ouch"], 9, (1, 0.9, 0.35), OUT * 0.6, t * 2)


def spark(ctx, t, p):
    """A little yellow pow star (impact, discovery)."""
    s = p.get("s", 1.0)
    starburst(ctx, 0, 0, 90 * s, 10, (1, 0.86, 0.2), OUT * 0.8, t * 1.5)


def danger(ctx, t, p):
    """A red danger flash ring (the playbook's 'red danger flash'), pulses."""
    a = 0.5 + 0.5 * math.sin(t * 14)
    ctx.save()
    p_ellipse(ctx, 0, 0, 460, 460)
    ctx.set_line_width(60)
    src(ctx, P["red"], 0.35 * a)
    ctx.stroke()
    ctx.restore()


ACTORS = {"harvestman": harvestman, "cellar_spider": cellar_spider, "web": web, "chair": chair, "arm": arm,
          "spark": spark, "danger": danger}
