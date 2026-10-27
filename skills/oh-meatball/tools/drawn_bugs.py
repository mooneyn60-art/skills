"""House creatures for tools/drawn.py ("Things Living In Your House"), drawn in the drawn_kit style.
Every animal has a cartoon face but keeps its real body plan so it is recognisable:

  house_centipede  15 pairs of long banded legs, three dark body stripes, leg-like antennae, long last legs
  roach, fly       prey; p: wrapped (silk), dead
  dust_mite        8-legged round arachnid, hairy; p: chew, pellets (droppings beside it)
  demodex          follicle mite: long ringed worm body, 8 stubby legs up front; tail at y = 0, head up
  silverfish       carrot-shaped, silver scales, 2 antennae, 3 tail filaments; p: chew, shed (moulted skin)
  jumping_spider   front view: 2 huge front eyes + 6 smaller, fuzzy, green fangs; p: crouch, wave, tether
  widow, wolf_spider  other spiders for the cellar spider to hunt; p: wrapped
  silk_throw       streaks of thrown silk from the origin to p["to"]; p: u (0..1 progress)
Base point y = 0 is the ground under the feet unless noted. p always has "phase", "walking", "blink".
"""
import math
import random

from drawn_kit import (INK, OUT, PAL, darker, eyes, flat, hexc, ink, lighter, limb, mouth, p_blob, p_ellipse,
                       p_poly, p_rrect, p_smooth, shape, src, starburst, stroke)

C = {k: hexc(v) for k, v in {
    "cent": "#cdb27c", "cent_dk": "#a88b55", "cent_st": "#4a3b2c", "cent_leg": "#dcc493",
    "roach": "#8a4b25", "roach_dk": "#6b3618", "fly": "#4a4f57", "wing": "#d8ecf7",
    "mite": "#f1e2c4", "mite_dk": "#d6c29a", "poo": "#7a5a3c",
    "demo": "#f3e6d2", "demo_dk": "#d9c6a8",
    "silver": "#bcc6cf", "silver_dk": "#8e9aa6", "silver_lt": "#e6ecf1",
    "js": "#2b2b2e", "js_hair": "#55555a", "js_spot": "#f4f4f4", "fang": "#2fbf9e", "fang2": "#5a7ce0",
    "widow": "#1d1d22", "hour": "#e0261e", "wolf": "#8a6a44", "wolf_dk": "#5e452a", "wolf_st": "#c9a874",
    "silk": "#ffffff",
}.items()}


def _banded(ctx, pts, w, col, band):
    limb(ctx, pts, w, col, OUT * 0.45)
    ctx.save()
    p_smooth(ctx, pts, close=False)
    ctx.set_dash([w * 1.6, w * 2.2])
    src(ctx, band)
    ctx.set_line_width(w)
    ctx.stroke()
    ctx.restore()


# ================================================================= house centipede

def house_centipede(ctx, t, p):
    """Side view facing right, ~1900 wide with antennae and last legs. p: mood, look, bite (0..1 fangs snap),
    talk, pairs (leg pairs, default 15)."""
    ph = p.get("phase", 0.0)
    walking = p.get("walking", False)
    by = -230 + (5 * math.sin(ph * 2) if walking else 4 * math.sin(t * 2))
    n = int(p.get("pairs", 15))   # babies hatch with 4 pairs and add more at each moult
    hips = [(250 - i * 36 * 15 / max(n, 4), by + 10) for i in range(n)]

    def leg(i, far):
        hx, hy = hips[i]
        reach = 560 - i * 85 * 14 / max(n - 1, 3)
        fx, fy = hx + reach * (0.85 if far else 1.0) + (-40 if far else 0), (-34.0 if far else 0.0)
        q = ph * 1.4 - i * 0.75 + (math.pi if far else 0)
        if walking:
            fx += 55 * math.sin(q)
            fy -= 40 * max(0.0, math.cos(q))
        else:
            fx += 8 * math.sin(t * 2 + i)
        kh = (150 if far else 175) + abs(7 - i * 14 / max(n - 1, 3)) * 9
        kx = hx + (fx - hx) * 0.45
        pts = [(hx, hy), (kx, min(hy, fy) - kh), (fx, fy)]
        if i == n - 1:  # the very long last legs trail back like a second pair of antennae
            sw = 20 * math.sin(t * 3 + far)
            pts = [(hx, hy), (hx - 280, by - 230 - (50 if far else 0) + sw), (hx - 720, by - 120 + sw),
                   (hx - 980, by - 20 + sw)]
        return pts

    for i in range(n):
        _banded(ctx, leg(i, True), 8, darker(C["cent_leg"], 0.7), darker(C["cent_st"], 0.8))
    for k in (0, 1):  # antennae: as long and banded as legs, so you can't tell which end is the head
        sw = 25 * math.sin(t * 2.5 + k)
        _banded(ctx, [(300, by - 30), (470, by - 260 - 70 * k), (760, by - 330 - 90 * k + sw),
                      (1060, by - 240 - 100 * k + sw)], 9, C["cent_leg"], C["cent_st"])
    body = lambda c: p_smooth(c, [(-300, by + 14), (-260, by - 50), (0, by - 66), (230, by - 60),
                                  (290, by - 20), (280, by + 38), (0, by + 46), (-260, by + 44)])
    shape(ctx, body, C["cent"], OUT, (0.0, 0.2), hi=(0.4, 0.2, 0.2))
    ctx.save()
    body(ctx)
    ctx.clip()
    for dy in (-40, -8, 24):
        stroke(ctx, [(-310, by + dy), (300, by + dy - 6)], 12, color=C["cent_st"])
    for i in range(15):
        x = 262 - i * 38
        stroke(ctx, [(x, by - 80), (x - 6, by + 50)], 4, color=C["cent_dk"])
    ctx.restore()
    body(ctx)
    ink(ctx, OUT)
    ctx.stroke()
    shape(ctx, lambda c: p_ellipse(c, 320, by - 14, 84, 66), C["cent"], OUT, (0.08, 0.15), hi=(0.3, 0.25, 0.2))
    b = p.get("bite", 0.0)
    for s in (-1, 1):
        x0, y0 = 360, by + 42
        tip = (x0 + 95, y0 + 40 + s * 32 * (1 - b))
        stroke(ctx, [(x0, y0 + s * 10), (x0 + 70, y0 + 30 + s * 30 * (1 - b)), tip], 13, smooth=True)
        stroke(ctx, [(x0, y0 + s * 10), (x0 + 70, y0 + 30 + s * 30 * (1 - b)), tip], 7, smooth=True,
               color=hexc("#9a4a26"))
    eyes(ctx, 335, by - 38, 26, 28, p.get("look", (1, 0)), p.get("mood", "calm"), p.get("blink", 0), OUT * 0.6,
         lid=C["cent"])
    mouth(ctx, 360, by + 16, 30, p.get("mouth", "smile"), p.get("talk", 0.0), OUT * 0.5)
    for i in range(n):
        _banded(ctx, leg(i, False), 12, C["cent_leg"], C["cent_st"])


# ================================================================= prey

def _wrapped(ctx, x, y, rx, ry, w):
    if w <= 0:
        return
    shape(ctx, lambda c: p_ellipse(c, x, y, rx * 1.1, ry * 1.2), (1, 1, 1), OUT * 0.5, None, a=0.75 * w)
    for k in range(7):
        a = k * 0.45
        stroke(ctx, [(x - rx * math.cos(a), y - ry * math.sin(a) - 10), (x + rx * math.cos(a + 0.6),
                                                                          y + ry * math.sin(a + 0.6))],
               4, color=(0.85, 0.85, 0.85), a=w)


def roach(ctx, t, p):
    """A cockroach seen from the side-top, facing right, ~520 long."""
    ph = p.get("phase", 0.0)
    wk = p.get("walking", False)
    for i in range(3):
        for far in (1, 0):
            hx = 60 - i * 90
            q = ph * 1.6 + i * 2 + far * math.pi
            fx = hx + (1 - i) * 90 + (35 * math.sin(q) if wk else 0)
            limb(ctx, [(hx, -80), (hx + 20 - i * 40, -150), (fx, 0)], 9,
                 C["roach_dk"] if far else C["roach"], OUT * 0.45)
    for k in (0, 1):
        sw = 20 * math.sin(t * 4 + k)
        stroke(ctx, [(200, -120), (380, -260 - 40 * k + sw), (520, -200 - 50 * k + sw)], 6, smooth=True)
    shape(ctx, lambda c: p_ellipse(c, -20, -110, 230, 80), C["roach"], OUT, (0.05, 0.2), hi=(0.3, 0.2, 0.2))
    stroke(ctx, [(-240, -110), (110, -112)], 5, color=C["roach_dk"])
    shape(ctx, lambda c: p_ellipse(c, 170, -110, 70, 62), C["roach_dk"], OUT, (0.05, 0.15))
    if p.get("dead"):
        for s in (-1, 1):
            stroke(ctx, [(170 + s * 22 - 14, -140), (170 + s * 22 + 14, -112)], 6)
            stroke(ctx, [(170 + s * 22 + 14, -140), (170 + s * 22 - 14, -112)], 6)
    else:
        eyes(ctx, 175, -126, 18, 22, p.get("look", (1, 0)), p.get("mood", "worry"), p.get("blink", 0), OUT * 0.5,
             lid=C["roach_dk"])
    _wrapped(ctx, -10, -110, 260, 100, p.get("wrapped", 0.0))


def fly(ctx, t, p):
    """A house fly, side view facing right, hovering (y = 0 is its body centre)."""
    flap = math.sin(t * 60)
    for k in (0, 1):
        shape(ctx, lambda c, k=k: p_ellipse(c, -40 + k * 20, -80 - 30 * flap, 120, 50, -0.5 + 0.3 * flap),
              C["wing"], OUT * 0.5, None, a=0.7)
    for i in range(3):
        stroke(ctx, [(-20 + i * 40, 30), (-40 + i * 50, 110)], 7)
    shape(ctx, lambda c: p_ellipse(c, -40, 0, 110, 66), C["fly"], OUT, (0.05, 0.2), hi=(0.3, 0.25, 0.2))
    shape(ctx, lambda c: p_ellipse(c, 90, -10, 64, 60), C["fly"], OUT, (0.05, 0.2))
    eyes(ctx, 96, -24, 22, 20, p.get("look", (1, 0)), p.get("mood", "calm"), p.get("blink", 0), OUT * 0.5,
         lid=hexc("#b8423a"))
    _wrapped(ctx, 0, 0, 160, 80, p.get("wrapped", 0.0))


# ================================================================= dust mite

def dust_mite(ctx, t, p):
    """Front view, ~760 wide, ~520 tall. p: mood, look, chew (0..1), pellets (count), talk, flake (0..1)."""
    ph = p.get("phase", 0.0)
    wk = p.get("walking", False)
    by = -270 + (8 * math.sin(ph * 2) if wk else 5 * math.sin(t * 2.4))
    for s in (-1, 1):
        for i in range(4):
            q = ph * 1.5 + i * 1.3 + (s > 0) * math.pi
            hx, hy = s * (150 + i * 14), by + 10 + i * 34
            fx = s * (330 + i * 75) + (25 * math.sin(q) if wk else 4 * math.sin(t * 3 + i))
            fy = -(30 * max(0, math.cos(q)) if wk else 0)
            kx, ky = s * (300 + i * 60), by - 110 + i * 45
            limb(ctx, [(hx, hy), (kx, ky), (fx, fy)], 24, C["mite_dk"], OUT * 0.65, smooth=False)
            for u in (0.35, 0.7):
                x, y = kx + (fx - kx) * u, ky + (fy - ky) * u
                stroke(ctx, [(x, y), (x + s * 40, y - 30)], 4)
    shape(ctx, lambda c: p_blob(c, 0, by, 250, 195, 0.04, seed=3), C["mite"], OUT, (0.1, 0.12),
          hi=(0.3, 0.25, 0.25))
    for k in range(3):
        stroke(ctx, [(-150 + k * 20, by - 120 + k * 90), (0, by - 100 + k * 90), (150 - k * 20, by - 120 + k * 90)],
               4, smooth=True, color=C["mite_dk"])
    for k in range(9):   # body hairs
        a = -math.pi * (0.1 + 0.8 * k / 8)
        x, y = 225 * math.cos(a), by + 200 * math.sin(a)
        stroke(ctx, [(x, y), (x * 1.35, by + 200 * math.sin(a) * 1.35 + 10 * math.sin(t * 3 + k))], 5)
    eyes(ctx, 0, by - 60, 40, 58, p.get("look", (0, 0)), p.get("mood", "happy"), p.get("blink", 0), OUT * 0.6,
         lid=C["mite"])
    ch = p.get("chew", 0.0)
    shape(ctx, lambda c: p_ellipse(c, 0, by + 95, 52, 38), C["mite_dk"], OUT * 0.7, None)
    mouth(ctx, 0, by + 92, 48, p.get("mouth", "smile"),
          max(p.get("talk", 0.0), ch * (0.5 + 0.5 * abs(math.sin(t * 12)))), OUT * 0.55)
    if p.get("flake", 0) > 0:
        shape(ctx, lambda c: p_blob(c, 70, by + 150, 90, 50, 0.25, seed=7), hexc("#f7efe0"), OUT * 0.6, None,
              a=p["flake"])
    for k in range(int(p.get("pellets", 0))):
        x = -330 - (k % 4) * 70
        y = -30 - (k // 4) * 55
        shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 30, 24), C["poo"], OUT * 0.5, (0.1, 0.2))


def mite_crowd(ctx, t, p):
    """Rows of small dust mites filling the ground (a pull-back gag); p: n (how many are shown, rises), rows."""
    n = int(p.get("n", 30))
    rng = random.Random(6)
    spots = []
    for r in range(int(p.get("rows", 4))):
        for k in range(10):
            spots.append(((k - 4.5) * 260 + (r % 2) * 130 + rng.uniform(-30, 30), r * 150, 0.28 + 0.04 * r))
    for i, (x, y, sc) in enumerate(spots[:n]):
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(sc, sc)
        dust_mite(ctx, t + i, {"mood": ("happy", "smug", "calm")[i % 3], "blink": 0,
                               "chew": float(i % 2), "phase": t * 9 + i, "walking": False})
        ctx.restore()


def skin_flake(ctx, t, p):
    shape(ctx, lambda c: p_blob(c, 0, -60, 170, 70, 0.22, seed=p.get("seed", 3)), hexc("#f7efe0"), OUT * 0.8,
          (0.05, 0.2))
    m = p.get("mold", 0.0)
    if m > 0:   # micro-mould growing on the flake
        rng = random.Random(1)
        for k in range(14):
            x, y = rng.uniform(-130, 130), rng.uniform(-110, -30)
            r = (10 + 12 * rng.random()) * m
            flat(ctx, lambda c, x=x, y=y, r=r: p_ellipse(c, x, y, r, r), hexc("#7fae4a"), OUT * 0.3)
            stroke(ctx, [(x, y), (x + 4, y - 30 * m)], 3, color=hexc("#5d8a34"))


# ================================================================= demodex face mite

def demodex(ctx, t, p):
    """Follicle mite, tail at y = 0 and head up at y = -700. p: mood, look, wiggle (legs), talk."""
    wig = p.get("wiggle", 0.0) + (1 if p.get("walking") else 0)
    sway = 10 * math.sin(t * 2)
    body = lambda c: p_smooth(c, [(0, 10), (-48, -60), (-62, -300), (-80, -480), (-78, -620), (-40, -700),
                                  (40, -700), (78, -620), (80, -480), (62, -300), (48, -60)])
    for s in (-1, 1):
        for i in range(4):
            y = -620 + i * 55
            k = math.sin(t * 10 + i + (s > 0) * 1.5) * 18 * wig
            limb(ctx, [(s * 70, y), (s * 125, y + 10 + k), (s * 150, y + 40 + k)], 20, C["demo_dk"], OUT * 0.55,
                 smooth=False)
            stroke(ctx, [(s * 150, y + 40 + k), (s * 172, y + 34 + k)], 5)
    ctx.save()
    ctx.translate(sway * 0.3, 0)
    shape(ctx, body, C["demo"], OUT, (0.12, 0.05), hi=(0.3, 0.2, 0.2))
    ctx.save()
    body(ctx)
    ctx.clip()
    for y in range(-400, 0, 34):
        stroke(ctx, [(-90, y + 8), (0, y), (90, y + 8)], 4, smooth=True, color=C["demo_dk"])
    ctx.restore()
    shape(ctx, lambda c: p_ellipse(c, 0, -712, 26, 20), C["demo_dk"], OUT * 0.6, None)
    eyes(ctx, 0, -620, 26, 32, p.get("look", (0, -1)), p.get("mood", "calm"), p.get("blink", 0), OUT * 0.5,
         lid=C["demo"])
    mouth(ctx, 0, -560, 34, p.get("mouth", "smile"), p.get("talk", 0.0), OUT * 0.5)
    ctx.restore()


# ================================================================= silverfish

def silverfish(ctx, t, p):
    """Side-top view facing right, ~900 long with tails. p: mood, look, chew, shed (0..1 moulted skin behind),
    talk."""
    ph = p.get("phase", 0.0)
    wk = p.get("walking", False)
    wav = 8 * math.sin(ph * 2) if wk else 0
    sh = p.get("shed", 0.0)

    def body_path(c, dx=0.0):
        p_smooth(c, [(-330 + dx, -70), (-150 + dx, -120 + wav), (100 + dx, -185), (280 + dx, -190),
                     (345 + dx, -120), (300 + dx, -55), (100 + dx, -45), (-150 + dx, -48 - wav * 0.5)])

    if sh > 0:
        ctx.save()
        ctx.set_dash([14, 10])
        body_path(ctx, -420)
        src(ctx, C["silver_lt"], 0.5 * sh)
        ctx.fill_preserve()
        ink(ctx, OUT * 0.5, sh)
        ctx.stroke()
        ctx.restore()
    for i in range(3):
        for far in (1, 0):
            hx = 220 - i * 100
            q = ph * 1.8 + i * 2 + far * math.pi
            fx = hx + 50 + (35 * math.sin(q) if wk else 0)
            limb(ctx, [(hx, -60), (hx + 40, -30), (fx, 0)], 12, C["silver_dk"] if far else C["silver"], OUT * 0.4)
    for k, (a, b) in enumerate(((-150, -40), (-180, 0), (-150, 40))):   # three tail filaments
        sw = 12 * math.sin(t * 5 + k)
        stroke(ctx, [(-320, -66), (-480, -66 + a * 0.6 + sw), (-660, -66 + a + b + sw)], 8, smooth=True)
    for k in (0, 1):
        sw = 22 * math.sin(t * 4 + k)
        stroke(ctx, [(320, -150), (460, -330 - 50 * k + sw), (640, -310 - 60 * k + sw)], 8, smooth=True)
    shape(ctx, body_path, C["silver"], OUT, (0.0, 0.25), hi=(0.4, 0.15, 0.25))
    ctx.save()
    body_path(ctx)
    ctx.clip()
    for k in range(11):
        x = 280 - k * 55
        stroke(ctx, [(x, -200), (x - 18, -30)], 5, color=C["silver_dk"])
    stroke(ctx, [(-300, -100), (250, -160)], 14, color=C["silver_lt"], a=0.8)
    ctx.restore()
    body_path(ctx)
    ink(ctx, OUT)
    ctx.stroke()
    eyes(ctx, 270, -130, 24, 27, p.get("look", (1, 0)), p.get("mood", "smug"), p.get("blink", 0), OUT * 0.55,
         lid=C["silver"])
    ch = p.get("chew", 0.0)
    mouth(ctx, 300, -80, 34, p.get("mouth", "grin"),
          max(p.get("talk", 0.0), ch * abs(math.sin(t * 14))), OUT * 0.5)


# ================================================================= spiders

def _fuzz(ctx, cx, cy, rx, ry, col, n=40, ln=18):
    for k in range(n):
        a = 2 * math.pi * k / n
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        stroke(ctx, [(x, y), (x + ln * math.cos(a + 0.3), y + ln * math.sin(a + 0.3))], 5, color=col)


def jumping_spider(ctx, t, p):
    """A bold-jumper-style jumping spider, front view, ~900 wide. p: crouch (0..1), wave (0..1 front legs up,
    the courtship dance), look, mood, fangs (0..1 green shine), tether [x, y] (silk line to that local point)."""
    cr = p.get("crouch", 0.0)
    wv = p.get("wave", 0.0)
    by = -330 + 90 * cr + 5 * math.sin(t * 3)
    tet = p.get("tether")
    if tet:
        stroke(ctx, [(0, by - 160), tuple(tet)], 4, color=C["silk"], a=0.95)
    shape(ctx, lambda c: p_ellipse(c, 0, by - 150, 190, 110), C["js"], OUT, (0.1, 0.15))
    _fuzz(ctx, 0, by - 150, 190, 110, C["js_hair"], 30, 14)
    flat(ctx, lambda c: p_ellipse(c, 0, by - 215, 50, 22), C["js_spot"], OUT * 0.4)
    for s in (-1, 1):
        for i in range(4):
            front = i == 0
            hx, hy = s * (110 + i * 20), by + 40 + i * 12
            if front and wv > 0:
                w = 30 * math.sin(t * 10)
                pts = [(hx, hy), (s * 300, by - 180 - 80 * wv + w), (s * 380, by - 360 * wv + w)]
            else:
                fx = s * (230 + i * 90)
                pts = [(hx, hy), (s * (200 + i * 70), by - 90 + i * 30 + 40 * cr), (fx, 0)]
            _banded(ctx, pts, 30 if front else 22, C["js"], C["js_hair"])
    shape(ctx, lambda c: p_rrect(c, -200, by - 150, 400, 300, 120), C["js"], OUT, (0.1, 0.12),
          hi=(0.3, 0.2, 0.2))
    _fuzz(ctx, 0, by, 205, 150, C["js_hair"])
    stroke(ctx, [(-150, by + 110), (150, by + 110)], 14, color=C["js_spot"], a=0.8)
    f = p.get("fangs", 0.6)
    for s in (-1, 1):
        shape(ctx, lambda c, s=s: p_ellipse(c, s * 45, by + 165, 44, 62), C["fang"], OUT * 0.7, (0.12, 0.1),
              hi=(0.3, 0.2, 0.3))
        flat(ctx, lambda c, s=s: p_ellipse(c, s * 45 - 10, by + 145, 12, 26), C["fang2"], a=0.5 + 0.5 * f)
        pw = 14 * math.sin(t * 6 + s)
        limb(ctx, [(s * 100, by + 120), (s * 140, by + 190 + pw), (s * 120, by + 240 + pw)], 26, C["js_hair"],
             OUT * 0.5)
        shape(ctx, lambda c, s=s, pw=pw: p_ellipse(c, s * 120, by + 250 + pw, 22, 18), C["js_spot"], OUT * 0.5,
              None)
    lk = p.get("look", (0, 0))
    for s in (-1, 1):   # two small side eyes, two tiny top eyes
        shape(ctx, lambda c, s=s: p_ellipse(c, s * 168, by - 50, 30, 30), INK, OUT * 0.5, None)
        flat(ctx, lambda c, s=s: p_ellipse(c, s * 160, by - 60, 9, 9), (1, 1, 1))
        shape(ctx, lambda c, s=s: p_ellipse(c, s * 120, by - 130, 15, 15), INK, OUT * 0.4, None)
    for s in (-1, 1):   # the two huge front eyes
        ex = s * 72
        shape(ctx, lambda c, ex=ex: p_ellipse(c, ex, by - 10, 68, 70), hexc("#1a1a1e"), OUT * 0.8, None)
        ctx.save()
        p_ellipse(ctx, ex, by - 10, 68, 70)
        ctx.clip()
        flat(ctx, lambda c, ex=ex: p_ellipse(c, ex + lk[0] * 18, by - 10 + lk[1] * 18, 44, 44), hexc("#3a2a20"))
        flat(ctx, lambda c, ex=ex: p_ellipse(c, ex - 20 + lk[0] * 8, by - 34 + lk[1] * 8, 20, 22), (1, 1, 1))
        flat(ctx, lambda c, ex=ex: p_ellipse(c, ex + 22 + lk[0] * 8, by + 10 + lk[1] * 8, 8, 8), (1, 1, 1))
        if p.get("blink", 0) > 0:
            flat(ctx, lambda c, ex=ex: c.rectangle(ex - 80, by - 90, 160, 80), C["js"])
        ctx.restore()
    mood = p.get("mood", "calm")
    if mood in ("angry", "smug"):
        for s in (-1, 1):
            stroke(ctx, [(s * 130, by - 100), (s * 20, by - 80 + (20 if mood == "angry" else 0))], 12,
                   color=C["js_hair"])


def _spider_front(ctx, t, p, col, dark, ab_r, legw, legc, eye_r):
    ph = p.get("phase", 0.0)
    wk = p.get("walking", False)
    by = -300 + (6 * math.sin(ph * 2) if wk else 4 * math.sin(t * 2.4))
    for s in (-1, 1):
        for i in range(4):
            q = ph * 1.5 + i * 1.4 + (s > 0) * math.pi
            fx = s * (260 + i * 110) + (25 * math.sin(q) if wk else 0)
            fy = -(30 * max(0, math.cos(q)) if wk else 0)
            _banded(ctx, [(s * 60, by + 20 + i * 10), (s * (230 + i * 80), by - 200 + i * 60), (fx, fy)], legw,
                    legc, dark)
    return by


def widow(ctx, t, p):
    """A black widow, front view: big glossy black abdomen with the red hourglass, thin black legs."""
    by = _spider_front(ctx, t, p, C["widow"], hexc("#3a3a44"), 0, 14, C["widow"], 0)
    shape(ctx, lambda c: p_ellipse(c, 0, by - 170, 210, 220), C["widow"], OUT, (0.1, 0.15), hi=(0.3, 0.2, 0.18))
    flat(ctx, lambda c: p_poly(c, [(-50, by - 280), (50, by - 280), (8, by - 200), (50, by - 120),
                                   (-50, by - 120), (-8, by - 200)]), C["hour"], OUT * 0.5)
    shape(ctx, lambda c: p_ellipse(c, 0, by + 60, 110, 90), C["widow"], OUT, (0.1, 0.15))
    eyes(ctx, 0, by + 40, 22, 34, p.get("look", (0, 0)), p.get("mood", "angry"), p.get("blink", 0), OUT * 0.5,
         lid=C["widow"])
    for s in (-1, 1):
        shape(ctx, lambda c, s=s: p_poly(c, [(s * 14, by + 110), (s * 36, by + 110), (s * 22, by + 150)]),
              hexc("#5a1a14"), OUT * 0.4, None)
    _wrapped(ctx, 0, by - 60, 260, 300, p.get("wrapped", 0.0))


def wolf_spider(ctx, t, p):
    """A wolf spider, front view: hairy brown, stripes, two big eyes over a row of four small ones."""
    by = _spider_front(ctx, t, p, C["wolf"], C["wolf_dk"], 0, 26, C["wolf"], 0)
    shape(ctx, lambda c: p_ellipse(c, 0, by - 170, 170, 180), C["wolf"], OUT, (0.1, 0.15))
    stroke(ctx, [(0, by - 330), (0, by - 30)], 30, color=C["wolf_st"])
    shape(ctx, lambda c: p_rrect(c, -150, by - 80, 300, 230, 100), C["wolf"], OUT, (0.1, 0.12))
    _fuzz(ctx, 0, by + 35, 152, 115, C["wolf_dk"], 34, 16)
    for s in (-1, 1):
        stroke(ctx, [(s * 60, by - 70), (s * 70, by + 140)], 18, color=C["wolf_st"])
    eyes(ctx, 0, by + 10, 30, 42, p.get("look", (0, 0)), p.get("mood", "angry"), p.get("blink", 0), OUT * 0.5,
         lid=C["wolf"])
    for k in range(4):
        flat(ctx, lambda c, k=k: p_ellipse(c, -66 + k * 44, by + 70, 12, 12), INK)
    _wrapped(ctx, 0, by - 40, 230, 260, p.get("wrapped", 0.0))


def silk_throw(ctx, t, p):
    """Streaks of silk flung from the origin toward p['to'] (local), p['u'] 0..1 = how far they've flown."""
    tx, ty = p.get("to", (600, 0))
    u = p.get("u", 1.0)
    for k in range(5):
        o = (k - 2) * 26
        pts = [(0, 0), (tx * 0.5 * u, ty * 0.5 * u - 60 * u + o), (tx * u, ty * u + o)]
        stroke(ctx, pts, 4, smooth=True, color=C["silk"], a=0.9)


def heart(ctx, t, p):
    """A little red heart that bobs (the mites found a mate); base at its point."""
    b = 1 + 0.08 * math.sin(t * 8)
    ctx.scale(b, b)
    shape(ctx, lambda c: (c.move_to(0, 0), c.curve_to(-120, -80, -110, -200, -50, -200),
                          c.curve_to(-20, -200, 0, -170, 0, -150), c.curve_to(0, -170, 20, -200, 50, -200),
                          c.curve_to(110, -200, 120, -80, 0, 0)), hexc("#e8463a"), OUT * 0.8, (0.1, 0.1),
          hi=(0.3, 0.25, 0.25))


def eggs(ctx, t, p):
    """A clutch of p['n'] pale oval eggs on the ground (pops in egg by egg as p['n'] rises)."""
    n = int(p.get("n", 8))
    rng = random.Random(2)
    for k in range(n):
        x, y = (k % 5) * 70 - 140 + rng.uniform(-12, 12), -30 - (k // 5) * 55
        shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 32, 24), hexc("#f8f2e2"), OUT * 0.5, (0.1, 0.2),
              hi=(0.3, 0.25, 0.3))


def droplets(ctx, t, p):
    """Water droplets drifting in toward the origin from all around (moisture soaked out of the air);
    p: n, r (start radius)."""
    n = int(p.get("n", 10))
    R = p.get("r", 520)
    for k in range(n):
        a = 2 * math.pi * k / n + 0.3
        u = (t * 0.45 + k / n) % 1
        rr = R * (1 - u)
        x, y = rr * math.cos(a), rr * math.sin(a) * 0.8
        s = 26 * (1 - 0.6 * u)
        shape(ctx, lambda c, x=x, y=y, s=s: (c.move_to(x, y - s), c.curve_to(x + s * 0.7, y, x + s * 0.6, y + s * 0.8,
                                                                             x, y + s * 0.8),
                                             c.curve_to(x - s * 0.6, y + s * 0.8, x - s * 0.7, y, x, y - s)),
              hexc("#78bef0"), OUT * 0.45, None, a=min(1, 3 * (1 - u)))


ACTORS = {"heart": heart, "eggs": eggs, "droplets": droplets, "house_centipede": house_centipede, "roach": roach, "fly": fly, "dust_mite": dust_mite,
          "skin_flake": skin_flake, "mite_crowd": mite_crowd, "demodex": demodex, "silverfish": silverfish,
          "jumping_spider": jumping_spider, "widow": widow, "wolf_spider": wolf_spider, "silk_throw": silk_throw}
