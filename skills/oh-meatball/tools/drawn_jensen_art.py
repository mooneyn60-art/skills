"""Pictures for the Jensen Huang allegations TikTok / Short (scripts/drawn-house/tt-jensen-huang.json, 11/13), in the
locked drawn_kit look (flat fills, one cel shade, thick ink outlines). Same conventions as tools/drawn_tc_art.py: an
actor draws at its origin in local units (feet at y = 0, y up is negative), scaled by its "s"; a scene draws in world
units (the default camera [540, 960, 1] shows x 0..1080, y 0..1920; floors sit at y = 1500).

The only words these pictures draw are the script's signs (j7 stamps, j12 door sign), passed in by the spec.

Actors:  jensen (cartoon CEO: stick limbs, round head, swept silver hair, rectangular glasses, black leather jacket
         with collar, zip and shine; p arm, gpu, mood, sweat, look, sparkle, flap, badge, spin, smoke, spark),
         jh_gpu (graphics card with two fans; p spin, smoke, spark), jh_screen (keynote slide: p a, b icons, flip),
         jh_podium, jh_micstand (p badge 0..1 hung), jh_desk (desk + laptop + huge paper-plane key; p press),
         jh_mail (envelopes that fly and multiply; p n 0..1), jh_paper (newspaper front page, blank lines; p tilt),
         jh_stamps (three rubber stamps; p n 0..3, texts), jh_line (stock line that falls off a cliff; p fall),
         jh_pile (newspapers burying him; p h 0..1), jh_cpu (chip with glowing threads; p on, spin), jh_door (office
         door; p sign 0..1, text), jh_resume (crayon resume, scribbles only), jh_doors (huge double doors; p shut),
         jh_popcorn (bucket, kernels pop), jh_phone (a phone Meatball reads), jh_drop (a falling card prop)
Scenes:  jh_stage (keynote stage, spotlight; p spot 0..1, sx), jh_office (office at night, city window),
         jh_living (Meatball's living room: sofa, lamp, window), jh_chart (a big stock-chart wall),
         jh_hall (office corridor), jh_capitol (marble hall with columns)
"""
import math
import random

from drawn_kit import (BG_OUT, INK, OUT, back_out, darker, ease, flat, hexc, lighter, limb, mouth, p_ellipse,
                       p_poly, p_rrect, p_smooth, shape, starburst, stroke, sweat)
from drawn_ds_art import text

C = {k: hexc(v) for k, v in {
    "skin": "#e8b48a", "hair": "#c9cdd4", "hair_dk": "#9aa0aa", "jacket": "#1d1d24", "jacket_lt": "#3a3a46",
    "tee": "#111116", "pants": "#2b3140", "shoe": "#141418", "zip": "#c8ccd4", "glass": "#202028",
    "gpu": "#3a3f48", "gpu_dk": "#2a2e35", "gpu_lt": "#8c939e", "pcb": "#2f6b3f", "gold": "#f2c14e",
    "fan": "#22252b", "smoke": "#9a9ea6", "spark": "#ffd34d", "red": "#e5383b", "green": "#3fb950",
    "yellow": "#ffd34d", "paper": "#f7f1df", "paper_dk": "#d9d0b4", "line": "#8d8778", "env": "#f4ecd6",
    "env_dk": "#d8c9a2", "wood": "#8a5a36", "wood_dk": "#6b4428", "steel": "#9aa3ab", "steel_dk": "#6f7882",
    "navy": "#141a33", "navy2": "#1c2448", "curtain": "#5a1f2e", "curtain_dk": "#43161f", "stage": "#3b2a22",
    "stage_lt": "#5a4030", "screen": "#0f1a2e", "screen_lt": "#1f3a63", "light": "#fff3b0", "wall": "#4b5a73",
    "wall_dk": "#3c4a60", "night": "#1b2440", "carpet": "#5c6a7c", "sofa": "#c0572e", "sofa_dk": "#9a4322",
    "lwall": "#e7c98f", "lwall2": "#dcbb7d", "floor": "#a8754a", "floor_dk": "#8a5c36", "door": "#a8754a",
    "door_dk": "#7e5634", "marble": "#e9e4d8", "marble_dk": "#cfc8b6", "crayon": "#e5383b", "crayon2": "#3b7dd8",
    "chip": "#2a2e35", "chip_lt": "#4a505a", "thread": "#5ee0ff", "pop": "#fff6d8", "bucket": "#e5383b",
}.items()}


def _rng(seed):
    return random.Random(seed)


def glow(ctx, x, y, r, col, a):
    import cairo
    rg = cairo.RadialGradient(x, y, 0, x, y, r)
    rg.add_color_stop_rgba(0, col[0], col[1], col[2], a)
    rg.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
    ctx.set_source(rg)
    ctx.arc(x, y, r, 0, 2 * math.pi)
    ctx.fill()


# ================================================================================================ the graphics card

def gpu(ctx, x, y, s, t, spin=0.0, smoke=0.0, spark=0.0, rot=0.0):
    """A chunky graphics card centred at (x, y): shroud, two fans (spin 0..1 speed), gold fingers; smoke and
    spark 0..1."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    shape(ctx, lambda c: c.rectangle(-150, 40, 300, 22), C["pcb"], OUT * 0.6, None)
    for k in range(10):
        flat(ctx, lambda c, k=k: c.rectangle(-120 + k * 18, 62, 12, 14), C["gold"])
    shape(ctx, lambda c: p_rrect(c, -165, -70, 330, 120, 18), C["gpu"], OUT * 0.9, (0.04, 0.12))
    stroke(ctx, [(-150, -60), (150, -60)], 6, color=C["gpu_lt"])
    flat(ctx, lambda c: c.rectangle(-165, -12, 330, 8), C["green"])
    for fx in (-78, 78):
        shape(ctx, lambda c, fx=fx: p_ellipse(c, fx, -10, 54, 54), C["fan"], OUT * 0.7, None)
        ang = t * (2 + 40 * spin)
        for b in range(7):
            a = ang + b * 2 * math.pi / 7
            stroke(ctx, [(fx + 10 * math.cos(a), -10 + 10 * math.sin(a)),
                         (fx + 44 * math.cos(a + 0.5), -10 + 44 * math.sin(a + 0.5))], 9, color=C["gpu_lt"],
                   a=0.5 if spin > 0.5 else 0.95)
        if spin > 0.5:
            ctx.save()
            ctx.new_path()
            ctx.arc(fx, -10, 40, 0, 2 * math.pi)
            ctx.set_source_rgba(0.6, 0.65, 0.7, 0.25)
            ctx.fill()
            ctx.restore()
        flat(ctx, lambda c, fx=fx: p_ellipse(c, fx, -10, 13, 13), C["gpu_lt"])
    ctx.restore()
    if smoke > 0.01:
        for k in range(7):
            u = ((t * 0.9 + k / 7) % 1.0)
            r = (20 + 60 * u) * s
            px = x + (math.sin(k * 2.3 + t * 2) * 40 + (k - 3) * 22) * s
            py = y - (60 + 360 * u) * s
            ctx.save()
            ctx.new_path()
            ctx.arc(px, py, r, 0, 2 * math.pi)
            ctx.set_source_rgba(0.55, 0.57, 0.6, 0.75 * smoke * (1 - u))
            ctx.fill_preserve()
            ctx.set_source_rgba(0.07, 0.07, 0.07, 0.6 * smoke * (1 - u))
            ctx.set_line_width(4 * s)
            ctx.stroke()
            ctx.restore()
    if spark > 0.01:
        rg = _rng(int(t * 12))
        for k in range(3):
            if rg.random() < spark:
                sx = x + rg.uniform(-170, 170) * s
                sy = y + rg.uniform(-80, 40) * s
                starburst(ctx, sx, sy, rg.uniform(28, 46) * s, 6, C["spark"], OUT * 0.5 * s, rg.random())


def jh_gpu(ctx, t, p):
    gpu(ctx, 0, -60, 1.0, t, p.get("spin", 0.0), p.get("smoke", 0.0), p.get("spark", 0.0), p.get("rot", 0.0))


# ================================================================================================ Jensen

ARMS = {   # (left hand, right hand) targets; right = the side he faces
    "down": ((-120, -380), (120, -380)),
    "hold": ((-120, -400), (150, -930)),        # the graphics card up like a trophy
    "hold2": ((-150, -900), (150, -930)),       # both hands up, card overhead
    "low": ((-40, -520), (110, -520)),          # holding the card (or a paper) in front, looking down at it
    "tug": ((-120, -390), (45, -650)),          # tugging his collar
    "facepalm": ((-110, -420), (20, -800)),
    "wipe": ((-120, -390), (-20, -870)),        # wiping his forehead
    "press": ((-110, -420), (250, -470)),       # pressing a key
    "up": ((-190, -950), (190, -950)),          # hands up
    "reach": ((-120, -390), (260, -600)),       # setting something down / hanging the badge
    "shrug": ((-210, -620), (210, -620)),
    "point": ((-120, -390), (270, -760)),
    "hips": ((-150, -440), (150, -440)),
}


def _arm_pts(side, tg, sh):
    el = ((sh[0] + tg[0]) / 2 + side * 55, (sh[1] + tg[1]) / 2 + 40)
    if tg[1] < sh[1] - 120:   # raised arm: the elbow goes out to the side
        el = ((sh[0] + tg[0]) / 2 + side * 80, (sh[1] + tg[1]) / 2 + 20)
    return [sh, el, tg]


def jensen(ctx, t, p):
    """Cartoon Jensen, feet at y = 0, about 950 tall at scale 1, facing right. p: arm (ARMS key; "walk" swings),
    gpu (True: the card in his right hand), mood (calm | proud | shock | sweat | mortified), sweat (0..1),
    look ([x, y]), sparkle (0..1 a glint on the jacket), flap (0..1 the jacket flaps), badge (lanyard badge),
    spin / smoke / spark (the card's fans), walking / phase (from drawn.py)."""
    ph = p.get("phase", 0.0)
    walking = p.get("walking")
    st = 55 * math.sin(ph) if walking else 0.0
    hip = (0, -340)
    # legs (dark trousers) and shoes
    for s_, o in ((-1, st), (1, -st)):
        knee = (s_ * 30 + o * 0.6, -175)
        foot = (s_ * 45 + o, -14)
        limb(ctx, [hip, knee, foot], 34, C["pants"], OUT * 0.8, smooth=False)
        shape(ctx, lambda c, foot=foot: p_ellipse(c, foot[0] + 22, foot[1] + 2, 48, 20), C["shoe"], OUT * 0.7, None)
    flap = p.get("flap", 0.0)
    # torso: black tee, then the jacket
    flat(ctx, lambda c: p_poly(c, [(-60, -660), (60, -660), (55, -400), (-55, -400)]), C["tee"])
    w = 7 * math.sin(t * 30) * flap
    jacket = [(-110, -655), (-60, -680), (60, -680), (110, -655), (118, -330 + w), (60, -315 - w),
              (-60, -320 + w), (-118, -330 - w)]
    if flap > 0.05:   # the hem flies up behind him
        jacket = jacket[:5] + [(150 + 20 * math.sin(t * 25), -300 - 60 * flap), (-60, -330)] + jacket[7:]
    shape(ctx, lambda c: p_poly(c, jacket), C["jacket"], OUT, (0.08, 0.1))
    # open front: tee strip, zip runners on both edges
    flat(ctx, lambda c: p_poly(c, [(-28, -640), (28, -640), (22, -330), (-22, -330)]), C["tee"])
    for s_ in (-1, 1):
        stroke(ctx, [(s_ * 28, -640), (s_ * 22, -330)], 6, color=C["zip"])
        for k in range(8):
            yy = -620 + k * 36
            stroke(ctx, [(s_ * 26, yy), (s_ * 34, yy)], 3, color=C["zip"])
    flat(ctx, lambda c: p_rrect(c, 16, -470, 14, 30, 4), C["zip"])   # zip pull
    # collar: two lapels
    for s_ in (-1, 1):
        shape(ctx, lambda c, s_=s_: p_poly(c, [(s_ * 30, -680), (s_ * 105, -662), (s_ * 72, -585), (s_ * 34, -620)]),
              C["jacket_lt"], OUT * 0.8, None)
    # pockets with zips, the shine
    for s_ in (-1, 1):
        stroke(ctx, [(s_ * 55, -450), (s_ * 95, -400)], 5, color=C["zip"])
    stroke(ctx, [(-92, -630), (-98, -520), (-90, -420)], 10, smooth=True, color=(1, 1, 1), a=0.35)
    stroke(ctx, [(75, -610), (84, -560)], 8, color=(1, 1, 1), a=0.3)
    if p.get("badge"):
        stroke(ctx, [(-45, -660), (0, -540), (45, -660)], 6, color=C["green"])
        shape(ctx, lambda c: p_rrect(c, -36, -545, 72, 90, 8), (1, 1, 1), OUT * 0.6, None)
        flat(ctx, lambda c: c.rectangle(-24, -520, 48, 30), hexc("#b9c3cf"))
    # arms: leather sleeves, skin hands
    arm = p.get("arm", "down")
    if walking and arm == "walk":
        tg = ((-110 - st * 0.9, -390), (110 + st * 0.9, -390))
    else:
        tg = ARMS.get(arm, ARMS["down"])
    if arm in ("tug", "wipe", "facepalm"):   # a little rub
        r = tg[1]
        tg = (tg[0], (r[0] + 10 * math.sin(t * 14), r[1] + 6 * math.cos(t * 14)))
    hands = []
    for side, h in zip((-1, 1), tg):
        sh = (side * 95, -640)
        limb(ctx, _arm_pts(side, h, sh), 40, C["jacket"], OUT * 0.8, smooth=True)
        hands.append(h)
    # head
    hx = 6 * math.sin(t * 2.2)
    hc = (hx, -800)
    look = p.get("look", [0.4, 0])
    mood = p.get("mood", "calm")
    if mood == "shock":
        hc = (hx, -812)
    flat(ctx, lambda c: c.rectangle(-22, -705, 44, 40), C["skin"])   # neck
    stroke(ctx, [(-22, -700), (-22, -670)], 5)
    stroke(ctx, [(22, -700), (22, -670)], 5)
    shape(ctx, lambda c: p_ellipse(c, hc[0], hc[1], 112, 118), C["skin"], OUT, (0.08, 0.1))
    flat(ctx, lambda c: p_ellipse(c, hc[0] - 106, hc[1] + 8, 18, 26), C["skin"])   # ear
    stroke(ctx, [(hc[0] - 110, hc[1] - 12), (hc[0] - 122, hc[1] + 10), (hc[0] - 106, hc[1] + 32)], 6, smooth=True)
    # swept silver hair: a sweep from the forehead back over the crown
    hair = [(hc[0] - 112, hc[1] - 10), (hc[0] - 118, hc[1] - 80), (hc[0] - 60, hc[1] - 140),
            (hc[0] + 40, hc[1] - 142), (hc[0] + 110, hc[1] - 92), (hc[0] + 122, hc[1] - 40),
            (hc[0] + 70, hc[1] - 72), (hc[0] + 10, hc[1] - 62), (hc[0] - 50, hc[1] - 52), (hc[0] - 90, hc[1] - 20)]
    shape(ctx, lambda c: p_smooth(c, hair), C["hair"], OUT * 0.9, (0.05, 0.12))
    for k in range(4):
        stroke(ctx, [(hc[0] - 70 + k * 40, hc[1] - 60 - 8 * k), (hc[0] - 20 + k * 40, hc[1] - 118 + 6 * k)], 5,
               smooth=False, color=C["hair_dk"])
    # eyes behind rectangular glasses
    lx, ly = look[0] * 7, look[1] * 6
    ey = hc[1] - 4
    blink = p.get("blink", 0.0)
    for s_ in (-1, 1):
        ex = hc[0] + 18 + s_ * 44
        ctx.save()
        p_rrect(ctx, ex - 36, ey - 26, 72, 52, 10)
        src_a = (0.85, 0.93, 1.0, 0.35)
        ctx.set_source_rgba(*src_a)
        ctx.fill()
        ctx.restore()
        if blink > 0.5:
            stroke(ctx, [(ex - 14 + lx, ey + ly), (ex + 14 + lx, ey + ly)], 6)
        elif mood == "shock":
            shape(ctx, lambda c, ex=ex: p_ellipse(c, ex + lx, ey + ly, 15, 18), (1, 1, 1), OUT * 0.5, None)
            flat(ctx, lambda c, ex=ex: p_ellipse(c, ex + lx, ey + ly, 7, 8), INK)
        else:
            flat(ctx, lambda c, ex=ex: p_ellipse(c, ex + lx, ey + ly, 11, 13), INK)
        ctx.save()
        p_rrect(ctx, ex - 36, ey - 26, 72, 52, 10)
        ctx.set_source_rgb(*C["glass"])
        ctx.set_line_width(8)
        ctx.stroke()
        ctx.restore()
    stroke(ctx, [(hc[0] + 10, ey - 6), (hc[0] + 26, ey - 6)], 7, color=C["glass"])
    stroke(ctx, [(hc[0] - 44, ey - 10), (hc[0] - 98, ey - 18)], 6, color=C["glass"])
    # brows
    by = ey - 42
    if mood in ("shock", "sweat", "mortified"):
        for s_ in (-1, 1):
            ex = hc[0] + 18 + s_ * 44
            stroke(ctx, [(ex - 24 * s_, by + 8), (ex + 22 * s_, by - 8)], 7)
    elif mood == "proud":
        for s_ in (-1, 1):
            ex = hc[0] + 18 + s_ * 44
            stroke(ctx, [(ex - 22, by + 2), (ex, by - 10), (ex + 22, by + 2)], 7, smooth=True)
    # nose and mouth
    stroke(ctx, [(hc[0] + 22, ey + 22), (hc[0] + 30, ey + 40), (hc[0] + 18, ey + 44)], 5, smooth=True)
    mx, my = hc[0] + 18, hc[1] + 70
    talk = p.get("talk", 0.0)
    if mood == "shock":
        mouth(ctx, mx, my, 40, "o")
    elif mood == "mortified":
        mouth(ctx, mx, my, 58, "wobble")
    elif mood == "sweat":
        mouth(ctx, mx, my, 50, "flat" if talk < 0.1 else "smile", talk * 0.5)
    elif mood == "proud":
        mouth(ctx, mx, my - 6, 70, "grin", talk * 0.6, teeth=True)
    else:
        mouth(ctx, mx, my, 56, "smile", talk * 0.6)
    sw = p.get("sweat", 0.0)
    if sw > 0.02 or mood in ("sweat", "mortified"):
        k = max(sw, 0.6)
        dy = 30 * ((t * 1.3) % 1.0)
        sweat(ctx, hc[0] + 110, hc[1] - 50 + dy, 26 * k)
        if k > 0.7:
            sweat(ctx, hc[0] - 100, hc[1] - 70 + dy * 0.6, 20 * k)
    if mood == "mortified":   # blush lines
        for k in range(3):
            stroke(ctx, [(hc[0] - 70 + k * 14, hc[1] + 30), (hc[0] - 78 + k * 14, hc[1] + 46)], 5, color=C["red"])
    # hands and the card
    for h in hands:
        shape(ctx, lambda c, h=h: p_ellipse(c, h[0], h[1], 24, 24), C["skin"], OUT * 0.7, None)
    if p.get("gpu"):
        h = hands[1]
        if arm == "low":
            gpu(ctx, (hands[0][0] + h[0]) / 2, h[1] - 50, 0.75, t, p.get("spin", 0.0), p.get("smoke", 0.0),
                p.get("spark", 0.0))
        else:
            gpu(ctx, h[0], h[1] - 70, 0.7, t, p.get("spin", 0.0), p.get("smoke", 0.0), p.get("spark", 0.0),
                0.08 * math.sin(t * 3))
    sp = p.get("sparkle", 0.0)
    if sp > 0.02:
        r = 40 * back_out(min(1.0, sp)) * (0.8 + 0.2 * math.sin(t * 16))
        for (sx, sy) in ((-75, -560), (88, -470)):
            _twinkle(ctx, sx, sy, r, t)


def _twinkle(ctx, x, y, r, t):
    pts = []
    for i in range(8):
        rr = r if i % 2 == 0 else r * 0.22
        a = math.pi * i / 4 + t * 2
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    shape(ctx, lambda c: p_poly(c, pts), (1, 1, 0.85), OUT * 0.4, None)


# ================================================================================================ stage

def jh_stage(ctx, t, layer, p):
    """Keynote stage: dark hall, red side curtains, wooden stage front with lights; floor y 1500 (stage lip 1560);
    p spot (0..1 the spotlight on the floor at x sx), crowd (heads at the bottom)."""
    layer(0.9)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), C["navy"])
    for k in range(9):
        flat(ctx, lambda c, k=k: c.rectangle(-3000, 200 + k * 140, 8000, 70), C["navy2"], a=0.5)
    for x0, s_ in ((-700, 1), (1780, -1)):
        shape(ctx, lambda c, x0=x0: c.rectangle(x0, -500, 400, 2100), C["curtain"], BG_OUT, None)
        for k in range(5):
            stroke(ctx, [(x0 + 40 + k * 80, -500), (x0 + 40 + k * 80, 1600)], 6, color=C["curtain_dk"])
    layer(1.0)
    shape(ctx, lambda c: c.rectangle(-3000, 1430, 8000, 140), C["stage"], BG_OUT, None)
    stroke(ctx, [(-3000, 1470), (5000, 1470)], 4, color=C["stage_lt"])
    shape(ctx, lambda c: c.rectangle(-3000, 1560, 8000, 1200), hexc("#20161a"), BG_OUT, None)
    for k in range(-10, 30):
        flat(ctx, lambda c, k=k: p_ellipse(c, k * 160 + 60, 1590, 26, 12), C["light"], a=0.7)
    if p.get("crowd", True):
        rg = _rng(5)
        for k in range(-12, 32):
            x = k * 90 + rg.uniform(-20, 20)
            y = 1700 + rg.uniform(-20, 30) + (k % 2) * 40
            flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 52, 58), hexc("#0c0c14"))
            flat(ctx, lambda c, x=x, y=y: c.rectangle(x - 70, y + 40, 140, 300), hexc("#0c0c14"))
    sp = p.get("spot", 1.0)
    if sp > 0:
        sx = p.get("sx", 540)
        ctx.save()
        ctx.new_path()
        ctx.move_to(sx - 60, -400)
        ctx.line_to(sx + 60, -400)
        ctx.line_to(sx + 330, 1500)
        ctx.line_to(sx - 330, 1500)
        ctx.close_path()
        ctx.set_source_rgba(1, 0.96, 0.75, 0.13 * sp)
        ctx.fill()
        ctx.restore()
        ctx.save()
        p_ellipse(ctx, sx, 1500, 340, 52)
        ctx.set_source_rgba(1, 0.96, 0.75, 0.33 * sp)
        ctx.fill()
        ctx.restore()


def jh_screen(ctx, t, p):
    """The keynote slide screen, centred at its origin (900 x 520 local); p a / b: icon on each side ("gpu", "coins",
    "heart", "chart", "blank"), flip 0..1 (turns over to b, with a squash)."""
    fl = min(1.0, max(0.0, p.get("flip", 0.0)))
    side = p.get("a", "gpu") if fl < 0.5 else p.get("b", "heart")
    sx = abs(math.cos(fl * math.pi))
    ctx.save()
    ctx.scale(max(0.02, sx), 1)
    shape(ctx, lambda c: p_rrect(c, -470, -280, 940, 560, 22), hexc("#0a0a10"), OUT, None)
    flat(ctx, lambda c: p_rrect(c, -440, -250, 880, 500, 12), C["screen"])
    flat(ctx, lambda c: p_rrect(c, -440, -250, 880, 500, 12), C["screen_lt"], a=0.35)
    _icon(ctx, side, t)
    ctx.restore()


def _icon(ctx, kind, t):
    if kind == "gpu":
        gpu(ctx, 0, 10, 1.6, t, 0.2)
    elif kind == "coins":
        for k in range(5):
            for j in range(3):
                x = -220 + j * 220
                y = 150 - k * 46 - (j % 2) * 20
                shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 80, 28), C["gold"], OUT * 0.7, None)
        stroke(ctx, [(-330, -140), (-200, -60), (-60, -150), (120, -40), (320, -200)], 14, color=C["green"])
        shape(ctx, lambda c: p_poly(c, [(320, -200), (270, -190), (310, -150)]), C["green"], OUT * 0.5, None)
    elif kind == "heart":
        def hp(c, dx=0, rot=0.0):
            c.save()
            c.translate(dx, 0)
            c.rotate(rot)
            c.move_to(0, 170)
            c.curve_to(-260, 0, -170, -230, 0, -110)
            c.curve_to(170, -230, 260, 0, 0, 170)
            c.close_path()
            c.restore()
        shape(ctx, hp, C["red"], OUT, (0.05, 0.1))
        stroke(ctx, [(0, -110), (-30, -40), (30, 10), (-20, 80), (0, 170)], 12, color=hexc("#0f1a2e"))
        for k in range(3):   # coins falling out
            y = ((t * 0.7 + k / 3) % 1) * 200
            shape(ctx, lambda c, k=k, y=y: p_ellipse(c, -60 + k * 60, 150 + y * 0.5, 24, 24), C["gold"], OUT * 0.5, None)
    elif kind == "chart":
        stroke(ctx, [(-360, 160), (-200, 60), (-60, 100), (120, -60), (340, -200)], 16, color=C["green"])


def jh_podium(ctx, t, p):
    """A lectern, feet at y 0, top at y -460 (p gpu: the card lies on top)."""
    shape(ctx, lambda c: p_poly(c, [(-120, -440), (120, -440), (95, 0), (-95, 0)]), hexc("#1f2430"), OUT, (0.06, 0.1))
    shape(ctx, lambda c: p_poly(c, [(-160, -470), (160, -470), (140, -420), (-140, -420)]), hexc("#2c3342"), OUT, None)
    flat(ctx, lambda c: p_ellipse(c, 0, -250, 40, 40), C["green"], a=0.6)
    if p.get("gpu"):
        gpu(ctx, 10, -515, 0.55, t, p.get("spin", 0.1))


def jh_micstand(ctx, t, p):
    """A mic stand, feet at y 0, mic at y -820; p badge 0..1 (a lanyard badge swings onto the stand)."""
    shape(ctx, lambda c: p_ellipse(c, 0, -8, 90, 18), C["steel_dk"], OUT * 0.7, None)
    stroke(ctx, [(0, -10), (0, -760)], 18, color=C["steel_dk"])
    stroke(ctx, [(0, -10), (0, -760)], 8, color=C["steel"])
    stroke(ctx, [(0, -760), (60, -820)], 14)
    shape(ctx, lambda c: p_rrect(c, 40, -880, 60, 100, 28), hexc("#2a2a30"), OUT * 0.7, None)
    b = p.get("badge", 0.0)
    if b > 0.01:
        u = ease(min(1.0, b))
        sw = 0.25 * math.sin(t * 6) * (1 - min(1, b)) + 0.08 * math.sin(t * 3)
        ctx.save()
        ctx.translate(0, -720 - 200 * (1 - u))
        ctx.rotate(sw)
        stroke(ctx, [(-30, 0), (0, 150), (30, 0)], 6, color=C["green"])
        shape(ctx, lambda c: p_rrect(c, -40, 140, 80, 100, 8), (1, 1, 1), OUT * 0.6, None)
        flat(ctx, lambda c: c.rectangle(-26, 165, 52, 34), hexc("#b9c3cf"))
        ctx.restore()


# ================================================================================================ office

def jh_office(ctx, t, layer, p):
    """An office at night: blue wall, a big window with a city skyline at x 80..1000, y 380..1100, floor y 1500."""
    layer(0.9)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), C["wall"])
    for x in range(-3000, 5000, 220):
        flat(ctx, lambda c, x=x: c.rectangle(x, -3000, 110, 4500), C["wall_dk"], a=0.4)
    shape(ctx, lambda c: c.rectangle(60, 360, 960, 760), hexc("#d8dde6"), BG_OUT, None)
    flat(ctx, lambda c: c.rectangle(90, 390, 900, 700), C["night"])
    ctx.save()
    ctx.rectangle(90, 390, 900, 700)
    ctx.clip()
    rg = _rng(3)
    x = 90
    while x < 1000:
        w = rg.uniform(70, 140)
        h = rg.uniform(160, 520)
        flat(ctx, lambda c, x=x, w=w, h=h: c.rectangle(x, 1090 - h, w, h), hexc("#2a3560"))
        for wy in range(int(1090 - h + 20), 1080, 40):
            for wx in range(int(x + 12), int(x + w - 12), 26):
                if rg.random() < 0.45:
                    flat(ctx, lambda c, wx=wx, wy=wy: c.rectangle(wx, wy, 12, 16), hexc("#ffe08a"), a=0.8)
        x += w + 8
    flat(ctx, lambda c: p_ellipse(c, 860, 470, 40, 40), hexc("#f4f0d8"))
    ctx.restore()
    stroke(ctx, [(540, 390), (540, 1090)], BG_OUT * 1.6, color=hexc("#d8dde6"))
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 3000), C["carpet"])
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)
    if p.get("plant", True):
        shape(ctx, lambda c: p_poly(c, [(-60, 1500), (-20, 1340), (120, 1340), (160, 1500)]), C["wood_dk"], BG_OUT, None)
        for k in range(5):
            a = -2.4 + k * 0.4
            shape(ctx, lambda c, a=a: p_ellipse(c, 50 + 120 * math.cos(a), 1300 + 140 * math.sin(a), 40, 90,
                                                 a + 1.57), C["green"], BG_OUT, None)


def jh_desk(ctx, t, p):
    """A desk (feet y 0, top y -420, x -380..380) with a laptop and a huge round key with a paper-plane icon
    (no words); p press 0..1 (the key goes down), glow."""
    shape(ctx, lambda c: c.rectangle(-380, -440, 760, 50), C["wood"], OUT, (0.02, 0.2))
    for x0 in (-360, 290):
        shape(ctx, lambda c, x0=x0: c.rectangle(x0, -395, 70, 395), C["wood_dk"], OUT, None)
    # laptop (screen faces him, we see the back and a sliver of glow)
    shape(ctx, lambda c: p_poly(c, [(-330, -440), (-60, -440), (-90, -460), (-300, -460)]), C["steel"], OUT * 0.7, None)
    shape(ctx, lambda c: p_poly(c, [(-300, -460), (-90, -460), (-120, -700), (-330, -700)]), C["steel_dk"], OUT * 0.8,
          (0.05, 0.1))
    flat(ctx, lambda c: p_ellipse(c, -215, -585, 24, 24), C["steel"])
    # the huge key
    pr = ease(min(1.0, p.get("press", 0.0)))
    shape(ctx, lambda c: p_rrect(c, 20, -500, 300, 64, 18), hexc("#2a2a30"), OUT, None)
    top = -620 + 50 * pr
    shape(ctx, lambda c: p_rrect(c, 40, top, 260, 130 - 50 * pr, 26), C["red"], OUT, (0.04, 0.15))
    cx, cy = 170, top + 45
    shape(ctx, lambda c: p_poly(c, [(cx - 60, cy), (cx + 60, cy - 30), (cx + 10, cy + 30), (cx - 5, cy + 12)]),
          (1, 1, 1), OUT * 0.5, None)
    if pr > 0.5:
        for k in range(6):
            a = -math.pi / 2 + (k - 2.5) * 0.4
            stroke(ctx, [(170 + 160 * math.cos(a), -540 + 140 * math.sin(a)),
                         (170 + 220 * math.cos(a), -540 + 190 * math.sin(a))], 8, color=C["yellow"])


def _envelope(ctx, x, y, s, rot):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    shape(ctx, lambda c: c.rectangle(-80, -50, 160, 100), C["env"], OUT * 0.8, (0.03, 0.1))
    stroke(ctx, [(-80, -50), (0, 15), (80, -50)], OUT * 0.7)
    flat(ctx, lambda c: p_ellipse(c, 0, 12, 14, 14), C["red"])
    ctx.restore()


def jh_mail(ctx, t, p):
    """Envelopes fly up and out of the origin and multiply: p n 0..1 (how many, up to 30), p go (0..1 how far the
    first one has flown)."""
    n = p.get("n", 0.0)
    if n <= 0.001:
        return
    cnt = 1 + int(29 * min(1.0, n))
    rg = _rng(9)
    for k in range(cnt):
        tx, ty = rg.uniform(-560, 560), rg.uniform(-1300, -250)
        ph = (t * 0.8 + rg.random()) % 1.0
        u = ease(min(1.0, (n * 30 - k) / 3 + 0.0)) if k else ease(min(1.0, p.get("go", 1.0)))
        x = tx * u + 20 * math.sin(t * 3 + k)
        y = ty * u + 15 * math.cos(t * 4 + k)
        _envelope(ctx, x, y, 0.6 + 0.5 * u, 0.4 * math.sin(t * 3 + k) + ph * 0.2)


# ================================================================================================ newspaper, stamps

def jh_paper(ctx, t, p):
    """A newspaper front page centred at its origin (800 x 1000 local): a black masthead bar, a headline of thick
    bars, a picture box and columns of grey lines (no words)."""
    ctx.save()
    ctx.rotate(math.radians(p.get("tilt", -3)))
    shape(ctx, lambda c: c.rectangle(-400, -500, 800, 1000), C["paper"], OUT, (0.02, 0.05))
    flat(ctx, lambda c: c.rectangle(-360, -460, 720, 90), hexc("#1b1b1b"))
    stroke(ctx, [(-360, -350), (360, -350)], 5)
    stroke(ctx, [(-360, -340), (360, -340)], 2)
    for k, w in enumerate((680, 520)):
        flat(ctx, lambda c, k=k, w=w: c.rectangle(-340, -300 + k * 80, w, 54), hexc("#2a2a2a"))
    shape(ctx, lambda c: c.rectangle(-340, -120, 330, 260), C["paper_dk"], OUT * 0.5, None)
    shape(ctx, lambda c: p_ellipse(c, -175, -10, 60, 64), hexc("#bdb59c"), 0, None)
    flat(ctx, lambda c: p_rrect(c, -265, 60, 180, 80, 30), hexc("#bdb59c"))
    for col in range(2):
        for k in range(16):
            x0 = -340 + col * 360 if col == 0 else 20
            y = (180 if col == 0 else -120) + k * 26
            if y > 460:
                continue
            w = 320 if (k + col) % 5 else 220
            flat(ctx, lambda c, x0=x0, y=y, w=w: c.rectangle(x0, y, w, 12), C["line"])
    ctx.restore()


def jh_stamps(ctx, t, p):
    """Three rubber-stamp marks, stacked; p n 0..3 (each lands with a squash), texts [3], cols [3]."""
    n = p.get("n", 0.0)
    texts = p.get("texts", ["", "", ""])
    cols = p.get("cols", ["#d8322a", "#d8322a", "#d8322a"])
    pos = p.get("pos", [(0, -230), (-40, 40), (30, 300)])
    rots = (-7, 5, -4)
    for k in range(3):
        u = n - k
        if u <= 0:
            continue
        s = 1.0 + 0.6 * (1 - back_out(min(1.0, u * 2.5)))
        x, y = pos[k]
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(math.radians(rots[k]))
        ctx.scale(s, s)
        col = hexc(cols[k])
        w = p.get("w", [700, 520, 560])[k]
        ctx.save()
        p_rrect(ctx, -w / 2, -70, w, 140, 16)
        ctx.set_source_rgba(col[0], col[1], col[2], 0.95)
        ctx.set_line_width(12)
        ctx.stroke()
        ctx.restore()
        text(ctx, texts[k], 0, 0, p.get("px", [62, 84, 84])[k], cols[k], 0)
        ctx.restore()


# ================================================================================================ chart

def jh_chart(ctx, t, layer, p):
    """A big stock chart wall: dark board, a grid, axes (no numbers); floor y 1500."""
    layer(0.95)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), hexc("#0d1424"))
    for x in range(-1000, 2200, 120):
        stroke(ctx, [(x, -200), (x, 1500)], 3, color=hexc("#1e2a44"))
    for y in range(-200, 1500, 120):
        stroke(ctx, [(-1000, y), (2200, y)], 3, color=hexc("#1e2a44"))
    layer(1.0)
    stroke(ctx, [(50, 700), (50, 1480), (1040, 1480)], 10, color=hexc("#c8d0dc"))
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 3000), hexc("#0a0f1c"))
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)


CLIFF = [(70, 1380), (190, 1270), (300, 1310), (420, 1150), (520, 1190), (620, 1000)]   # rising, then the cliff
DROP = (1000, 1460)


def jh_line(ctx, t, p):
    """The stock line in world units (place at [0, 0]): green up to the peak, then p fall 0..1 draws the cliff in
    red down to DROP, with a red arrow."""
    stroke(ctx, CLIFF, 22, color=C["green"])
    stroke(ctx, CLIFF, 6, color=hexc("#b9f5c6"))
    f = ease(min(1.0, p.get("fall", 0.0)))
    if f > 0.01:
        a = CLIFF[-1]
        e = (a[0] + (DROP[0] - a[0]) * f, a[1] + (DROP[1] - a[1]) * f)
        stroke(ctx, [a, e], 24, color=C["red"])
        ang = math.atan2(DROP[1] - a[1], DROP[0] - a[0])
        hd = [(e[0] + 50 * math.cos(ang), e[1] + 50 * math.sin(ang)),
              (e[0] + 40 * math.cos(ang + 2.2), e[1] + 40 * math.sin(ang + 2.2)),
              (e[0] + 40 * math.cos(ang - 2.2), e[1] + 40 * math.sin(ang - 2.2))]
        shape(ctx, lambda c: p_poly(c, hd), C["red"], OUT * 0.6, None)


# ================================================================================================ pile, CPU

def jh_pile(ctx, t, p):
    """A pile of folded newspapers, base at y 0, p h 0..1 of 720 high; papers keep dropping onto the top."""
    h = 720 * min(1.0, max(0.0, p.get("h", 0.0)))
    rg = _rng(4)
    n = int(h / 34)
    for k in range(n):
        y = -k * 34
        w = 300 + rg.uniform(-30, 40)
        x = rg.uniform(-30, 30)
        r = rg.uniform(-0.08, 0.08)
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(r)
        shape(ctx, lambda c, w=w: c.rectangle(-w, -40, 2 * w, 40), C["paper"], OUT * 0.7, None)
        for j in range(4):
            flat(ctx, lambda c, w=w, j=j: c.rectangle(-w + 30 + j * (w / 2), -30, w / 2 - 50, 8), C["line"])
        ctx.restore()
    if p.get("falling", 1.0) and h > 10:
        for k in range(3):
            u = (t * 1.6 + k / 3) % 1.0
            x = (-200 + 200 * k)
            y = -h - 900 * (1 - u)
            ctx.save()
            ctx.translate(x, y)
            ctx.rotate(u * 3 + k)
            shape(ctx, lambda c: c.rectangle(-150, -24, 300, 48), C["paper"], OUT * 0.7, None)
            ctx.restore()


def jh_cpu(ctx, t, p):
    """A small CPU chip centred at its origin, p on 0..1 (pops in), spin; many glowing threads wind out of it."""
    on = p.get("on", 0.0)
    if on <= 0.01:
        return
    s = back_out(min(1.0, on))
    ctx.save()
    ctx.scale(s, s)
    ctx.rotate(t * 2.5 * p.get("spin", 1.0))
    for k in range(16):   # glowing threads
        a = k * 2 * math.pi / 16
        pts = []
        for j in range(8):
            r = 120 + j * 40
            pts.append((r * math.cos(a + j * 0.25 + math.sin(t * 6 + k) * 0.1),
                        r * math.sin(a + j * 0.25 + math.sin(t * 6 + k) * 0.1)))
        stroke(ctx, pts, 16, smooth=True, color=C["thread"], a=0.35)
        stroke(ctx, pts, 6, smooth=True, color=(0.85, 1, 1))
    for side in range(4):
        ctx.save()
        ctx.rotate(side * math.pi / 2)
        for k in range(6):
            flat(ctx, lambda c, k=k: c.rectangle(-75 + k * 28, -125, 12, 30), C["gold"])
        ctx.restore()
    shape(ctx, lambda c: p_rrect(c, -100, -100, 200, 200, 14), C["chip"], OUT, (0.05, 0.1))
    shape(ctx, lambda c: p_rrect(c, -55, -55, 110, 110, 8), C["chip_lt"], OUT * 0.6, None)
    glow(ctx, 0, 0, 120, C["thread"], 0.35 + 0.15 * math.sin(t * 9))
    ctx.restore()


# ================================================================================================ living room

def jh_living(ctx, t, layer, p):
    """Meatball's living room: warm wall, a window, a lamp, an orange sofa at x 600..1000; floor y 1500; the door
    gap is off frame left."""
    layer(0.9)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), C["lwall"])
    for x in range(-3000, 5000, 180):
        flat(ctx, lambda c, x=x: c.rectangle(x, -3000, 70, 4600), C["lwall2"])
    shape(ctx, lambda c: c.rectangle(560, 520, 420, 420), hexc("#f6efe0"), BG_OUT, None)
    flat(ctx, lambda c: c.rectangle(585, 545, 370, 370), hexc("#8fd3f4"))
    flat(ctx, lambda c: p_ellipse(c, 700, 640, 40, 40), hexc("#ffd84a"))
    stroke(ctx, [(770, 545), (770, 915)], BG_OUT * 1.6, color=hexc("#f6efe0"))
    stroke(ctx, [(585, 730), (955, 730)], BG_OUT * 1.6, color=hexc("#f6efe0"))
    shape(ctx, lambda c: c.rectangle(80, 600, 260, 200), hexc("#3a6a8a"), BG_OUT, None)   # a picture
    shape(ctx, lambda c: p_poly(c, [(110, 780), (190, 680), (240, 740), (280, 700), (320, 780)]), C["green"], BG_OUT * 0.6,
          None)
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 3000), C["floor"])
    for y in (1560, 1650, 1780):
        stroke(ctx, [(-3000, y), (5000, y)], 4, color=C["floor_dk"])
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)
    # sofa
    shape(ctx, lambda c: p_rrect(c, 600, 1150, 560, 230, 40), C["sofa"], BG_OUT, (0.03, 0.1))
    shape(ctx, lambda c: p_rrect(c, 570, 1300, 620, 170, 40), C["sofa"], BG_OUT, (0.03, 0.15))
    for x0 in (570, 1130):
        shape(ctx, lambda c, x0=x0: p_rrect(c, x0, 1250, 80, 230, 30), C["sofa_dk"], BG_OUT, None)
    # lamp
    stroke(ctx, [(-40, 1500), (-40, 1020)], 12)
    shape(ctx, lambda c: p_poly(c, [(-130, 1020), (50, 1020), (10, 900), (-90, 900)]), hexc("#f2c14e"), BG_OUT, None)
    glow(ctx, -40, 1000, 260, hexc("#fff3b0"), 0.35)


def jh_phone(ctx, t, p):
    """A phone held up, screen lit with blank text lines (no words)."""
    ctx.save()
    ctx.rotate(math.radians(p.get("rot", -10)))
    shape(ctx, lambda c: p_rrect(c, -60, -110, 120, 220, 18), hexc("#1d1d24"), OUT * 0.8, None)
    flat(ctx, lambda c: p_rrect(c, -48, -95, 96, 190, 10), hexc("#dff2ff"))
    for k in range(6):
        flat(ctx, lambda c, k=k: c.rectangle(-36, -78 + k * 28, 72 if k % 3 else 50, 9), hexc("#7a8a9c"))
    ctx.restore()


def jh_popcorn(ctx, t, p):
    """A striped popcorn bucket (base y 0), kernels popping up out of it."""
    shape(ctx, lambda c: p_poly(c, [(-80, -220), (80, -220), (60, 0), (-60, 0)]), (1, 1, 1), OUT * 0.8, None)
    for k in range(3):
        x = -55 + k * 50
        flat(ctx, lambda c, x=x: p_poly(c, [(x, -220), (x + 25, -220), (x + 20, 0), (x + 3, 0)]), C["bucket"])
    stroke(ctx, [(-80, -220), (-60, 0), (60, 0), (80, -220)], OUT * 0.8)
    for k in range(7):
        flat(ctx, lambda c, k=k: p_ellipse(c, -66 + k * 22, -232 - 14 * (k % 2), 22, 20), C["pop"])
    for k in range(3):
        u = (t * 1.4 + k / 3) % 1.0
        x = -40 + k * 40 + 30 * math.sin(k * 3)
        y = -240 - 160 * math.sin(u * math.pi)
        shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 16, 15), C["pop"], OUT * 0.4, None)


# ================================================================================================ doors

def jh_hall(ctx, t, layer, p):
    """An office corridor: grey-blue wall with a skirting board, floor y 1500."""
    layer(0.9)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), hexc("#9fb0c4"))
    for x in range(-3000, 5000, 300):
        stroke(ctx, [(x, -3000), (x, 1500)], 4, color=hexc("#8d9eb2"))
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1440, 8000, 60), hexc("#e8eef4"))
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 3000), hexc("#6e7b8c"))
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)


def jh_door(ctx, t, p):
    """An office door (feet y 0, 420 wide, 980 tall) with a gap under it; p sign 0..1 (a sign with p text drops
    in on two strings and swings), p open 0..1."""
    shape(ctx, lambda c: c.rectangle(-240, -1010, 480, 1010), hexc("#e8eef4"), OUT, None)   # frame
    shape(ctx, lambda c: c.rectangle(-210, -980, 420, 965), C["door"], OUT, (0.03, 0.08))
    for y0 in (-930, -470):
        shape(ctx, lambda c, y0=y0: c.rectangle(-160, y0, 320, 380), darker(C["door"], 0.9), OUT * 0.5, None)
    shape(ctx, lambda c: p_ellipse(c, 160, -480, 22, 22), C["gold"], OUT * 0.6, None)
    flat(ctx, lambda c: c.rectangle(-210, -15, 420, 15), hexc("#1a1a1a"))   # the gap under it
    sg = p.get("sign", 0.0)
    if sg > 0.01 and p.get("text"):
        u = ease(min(1.0, sg))
        sw = 0.2 * math.sin(t * 7) * max(0.0, 1.4 - sg) + 0.03 * math.sin(t * 3)
        ctx.save()
        ctx.translate(0, -1010 - 500 * (1 - u))
        ctx.rotate(sw)
        stroke(ctx, [(-120, 0), (-150, 140)], 5)
        stroke(ctx, [(120, 0), (150, 140)], 5)
        shape(ctx, lambda c: p_rrect(c, -210, 130, 420, 140, 14), hexc("#1d2a4a"), OUT * 0.8, None)
        text(ctx, p["text"], 0, 200, 78, "#ffd34d", 0)
        ctx.restore()


def jh_resume(ctx, t, p):
    """A crayon resume: a sheet with wobbly crayon scribbles and a smiley (no words)."""
    ctx.save()
    ctx.rotate(math.radians(p.get("rot", 0)))
    if True:
        shape(ctx, lambda c: c.rectangle(-110, -150, 220, 300), (1, 1, 1), OUT * 0.7, None)
        for k in range(5):
            stroke(ctx, [(-80 + j * 26, -40 + k * 34 + (10 if j % 2 else -6)) for j in range(7)], 7,
                   color=C["crayon"] if k % 2 else C["crayon2"])
        flat(ctx, lambda c: p_ellipse(c, -40, -100, 30, 30), C["yellow"])
        stroke(ctx, [(-55, -95), (-40, -85), (-25, -95)], 4, smooth=True)
    ctx.restore()


def jh_capitol(ctx, t, layer, p):
    """A marble hall with columns, floor y 1500 (the huge doors stand at x 540)."""
    layer(0.9)
    flat(ctx, lambda c: c.rectangle(-3000, -3000, 8000, 8000), C["marble"])
    for x in (-420, -140, 1220, 1500):
        shape(ctx, lambda c, x=x: c.rectangle(x - 70, -400, 140, 1900), C["marble"], BG_OUT, (0.15, 0.0))
        for k in range(3):
            stroke(ctx, [(x - 40 + k * 40, -380), (x - 40 + k * 40, 1480)], 4, color=C["marble_dk"])
    layer(1.0)
    flat(ctx, lambda c: c.rectangle(-3000, 1500, 8000, 3000), hexc("#b9a98a"))
    for x in range(-3000, 5000, 200):
        stroke(ctx, [(x, 1500), (x - 200, 1920)], 3, color=hexc("#a39374"))
    stroke(ctx, [(-3000, 1500), (5000, 1500)], BG_OUT)


def jh_doors(ctx, t, p):
    """Huge double doors (feet y 0, 1000 wide, 1300 tall) in a stone frame; p shut 0..1 swings both leaves shut
    (open = leaves turned edge-on, dark room behind)."""
    shape(ctx, lambda c: p_poly(c, [(-600, 0), (-600, -1330), (0, -1480), (600, -1330), (600, 0)]),
          C["marble_dk"], OUT, None)
    flat(ctx, lambda c: c.rectangle(-500, -1300, 1000, 1300), hexc("#1a1410"))
    sh = ease(min(1.0, max(0.0, p.get("shut", 1.0))))
    for s_ in (-1, 1):
        w = 500 * max(0.06, sh)
        x0 = s_ * 500
        x1 = x0 - s_ * w
        pts = [(x0, -1300), (x1, -1300 - 40 * (1 - sh)), (x1, 0 + 30 * (1 - sh)), (x0, 0)]
        shape(ctx, lambda c, pts=pts: p_poly(c, pts), C["door_dk"], OUT, (0.03, 0.05))
        if sh > 0.5:
            for y0 in (-1220, -620):
                xa, xb = sorted((x0 - s_ * 60, x1 + s_ * 60))
                shape(ctx, lambda c, xa=xa, xb=xb, y0=y0: c.rectangle(xa, y0, xb - xa, 520), darker(C["door_dk"], 0.85),
                      OUT * 0.5, None)
            shape(ctx, lambda c, s_=s_: p_ellipse(c, s_ * 60, -640, 26, 26), C["gold"], OUT * 0.6, None)


def jh_drop(ctx, t, p):
    """The graphics card on its own (it slips and falls; spin by actor rot)."""
    gpu(ctx, 0, 0, p.get("k", 0.7), t, p.get("spin", 0.0), p.get("smoke", 0.0), p.get("spark", 0.0))


def jh_dust(ctx, t, p):
    """A puff of dust / impact lines at the origin; p on 0..1."""
    on = p.get("on", 0.0)
    if on <= 0.01 or on >= 0.99:
        return
    for k in range(8):
        a = math.pi + k * math.pi / 7
        r0, r1 = 80 + 200 * on, 140 + 300 * on
        stroke(ctx, [(r0 * math.cos(a), r0 * math.sin(a) * 0.6), (r1 * math.cos(a), r1 * math.sin(a) * 0.6)], 10,
               a=1 - on)


ACTORS = {"jensen": jensen, "jh_gpu": jh_gpu, "jh_screen": jh_screen, "jh_podium": jh_podium,
          "jh_micstand": jh_micstand, "jh_desk": jh_desk, "jh_mail": jh_mail, "jh_paper": jh_paper,
          "jh_stamps": jh_stamps, "jh_line": jh_line, "jh_pile": jh_pile, "jh_cpu": jh_cpu, "jh_phone": jh_phone,
          "jh_popcorn": jh_popcorn, "jh_door": jh_door, "jh_resume": jh_resume, "jh_doors": jh_doors,
          "jh_drop": jh_drop, "jh_dust": jh_dust}
SCENES = {"jh_stage": jh_stage, "jh_office": jh_office, "jh_living": jh_living, "jh_chart": jh_chart,
          "jh_hall": jh_hall, "jh_capitol": jh_capitol}
