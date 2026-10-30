"""Species-accurate creatures for tools/drawn.py, in the locked house style (drawn_kit: thick ink, flat colour,
one cel shade, cartoon eyes). Built by TARS 10/30 because every creature was the same round blob with legs.

The rule: an animal reads from its SILHOUETTE, not its face. Each builder draws the real body plan (the right
segments, the right number of jointed legs, the 2-3 signature features exaggerated) and only then adds the
cartoon eyes, kept small enough that the body still reads.

    from drawn_anatomy import ANATOMY
    ACTORS.update(ANATOMY)                      # in drawn.py, next to the other ACTORS imports
    actor type "cassowary" | "camel_cricket" | "cockroach" | "black_widow" | "brown_recluse" | "wolf_spider"
               "jumping_spider" | "camel_spider" | "scabies_mite" | "house_centipede"

Every builder: f(ctx, t, p). Base point: x = 0 is the body centre, y = 0 the ground under the feet; the animal
faces right (+x). Per-frame params p (all optional): walk (0..1 gait cycle speed), lunge (0..1), mood, look,
xray (0..1, cassowary: the claw glows). Size: about 500-700 px long at scale 1; use the actor "s" to fit.
"""
import math

from drawn_kit import INK, OUT, darker, eyes, flat, hexc, ink, lighter, limb, mouth, p_ellipse, p_poly, p_smooth, \
    shape, stroke


def _leg(ctx, base, segs, w, col, t=0.0, phase=0.0, walk=0.0, lift=14):
    """A jointed leg: base point + list of (length, angle) segments; walking swings the first joint."""
    x, y = base
    pts = [(x, y)]
    sw = math.sin(t * 9 + phase) * walk
    for k, (ln, ang) in enumerate(segs):
        a = math.radians(ang) + (0.18 * sw if k == 0 else 0.08 * sw)
        x, y = x + ln * math.cos(a), y + ln * math.sin(a)
        if k == len(segs) - 1:
            y -= max(0.0, sw) * lift
        pts.append((x, y))
    limb(ctx, pts, w, col, smooth=False)
    for jx, jy in pts[1:-1]:  # knobbly joints read as "arthropod"
        shape(ctx, lambda c, jx=jx, jy=jy: p_ellipse(c, jx, jy, w * 0.62, w * 0.62), darker(col, 0.85), OUT * 0.5, None)
    return pts[-1]


def _bristles(ctx, cx, cy, rx, ry, n, ln, a0=-170, a1=-10, lw=3.0):
    ink(ctx, lw)
    for i in range(n):
        a = math.radians(a0 + (a1 - a0) * i / max(1, n - 1))
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        ctx.move_to(x, y)
        ctx.line_to(x + ln * math.cos(a), y + ln * math.sin(a))
    ctx.stroke()


# ------------------------------------------------------------------------------------------- spiders (3/4 top view)

def _spider(ctx, t, p, cfg):
    """True spider plan: small carapace in front, bigger abdomen behind (joined by a thin waist), 8 legs from the
    carapace, each femur-knee-tibia with the knee ABOVE the body (the spider 'tent'), pedipalps + fangs in front."""
    col, dk = hexc(cfg["color"]), hexc(cfg.get("dark", cfg["color"]))
    walk = p.get("walk", 0.0)
    L = cfg.get("leg", 1.0)
    cx, cy = 60, -150          # carapace centre
    ax, ay = -150, -165        # abdomen centre
    arx, ary = cfg.get("abd", (150, 120))
    # far legs first (behind the body), then the body, then the near legs
    feet = [235, 125, -95, -235]          # where each leg pair lands, front -> back (x, before L scale)
    knees = [(110, 150), (60, 165), (-40, 160), (-110, 140)]  # knee x offset, knee height above the body line
    for side, shade_k in ((-1, 0.72), (1, 1.0)):
        if side == 1:
            # waist, abdomen, carapace between the two leg layers
            shape(ctx, lambda c: p_ellipse(c, -40, -150, 26, 18), dk, OUT * 0.8, None)
            shape(ctx, lambda c: p_ellipse(c, ax, ay, arx, ary, -0.08), col, OUT, (0.0, 0.25), hi=(0.3, 0.2, 0.25))
            _spider_mark(ctx, cfg, ax, ay, arx, ary)
            if cfg.get("hair"):
                _bristles(ctx, ax, ay, arx, ary, 22, 14, -175, -5, 3.5)
            shape(ctx, lambda c: p_ellipse(c, cx, cy, 105, 78), col, OUT, (0.0, 0.25), hi=(0.3, 0.2, 0.2))
            if cfg.get("violin"):  # brown recluse: dark violin on the carapace, neck pointing back
                shape(ctx, lambda c: p_smooth(c, [(cx + 55, cy - 28), (cx + 10, cy - 34), (cx - 60, cy - 8),
                                                  (cx - 60, cy + 6), (cx + 10, cy + 10), (cx + 55, cy + 4)]),
                      hexc("#4a2c18"), 0, None)
        for i in range(4):
            sw = math.sin(t * 9 + i * 1.7 + (0 if side == 1 else 3.1)) * walk
            bx, by = cx + 40 - i * 25, cy + 25
            kx, kh = knees[i]
            knee = (cx + kx * L + 15 * sw, cy - kh * L * (0.85 if side == -1 else 1.0))
            foot = (cx + feet[i] * L + 30 * sw + (15 if side == 1 else -15), (0 if side == 1 else -35) - max(0, sw) * 12)
            c_leg = col if side == 1 else darker(col, shade_k)
            w = cfg.get("leg_w", 15)
            limb(ctx, [(bx, by), knee, foot], w, c_leg, smooth=False)
            shape(ctx, lambda c, k=knee: p_ellipse(c, k[0], k[1], w * 0.62, w * 0.62), darker(c_leg, 0.85), OUT * 0.5, None)
            if cfg.get("hair"):
                _bristles(ctx, (knee[0] + foot[0]) / 2, (knee[1] + foot[1]) / 2, 4, 30, 3, 9, -160, -20, 2.5)
    # pedipalps + chelicerae (fangs)
    for k in (-1, 1):
        limb(ctx, [(cx + 85, cy + 15 + k * 8), (cx + 140, cy + 5 + k * 14), (cx + 160, cy + 40 + k * 10)],
             11, col, smooth=True)
    fang = hexc(cfg.get("fang", "#2a1a12"))
    jaw = cfg.get("jaws", 1.0)
    shape(ctx, lambda c: p_poly(c, [(cx + 92, cy + 22), (cx + 92 + 46 * jaw, cy + 38), (cx + 100, cy + 60)]),
          fang, OUT * 0.6, None)
    # eyes: a row of small eyes, front pair big when the species hunts by sight (jumping spider)
    big = cfg.get("big_eyes", False)
    ex, ey = cx + 70, cy - 30
    if big:
        eyes(ctx, ex + 8, ey + 10, 30, 40, p.get("look", (0.4, 0.1)), p.get("mood", "calm"), 0.0, pupil=0.6)
    else:
        eyes(ctx, ex, ey, 17, 26, p.get("look", (0.3, 0.1)), p.get("mood", "calm"), 0.0)
    for k in range(4):
        shape(ctx, lambda c, k=k: p_ellipse(c, ex - 30 - k * 14, ey - 8 - (k % 2) * 6, 5, 5), INK, 0, None)


def _spider_mark(ctx, cfg, ax, ay, arx, ary):
    m = cfg.get("mark")
    if m == "hourglass":   # black widow: red hourglass (shown on the side so it reads in profile)
        red = hexc("#e1261c")
        shape(ctx, lambda c: p_poly(c, [(ax - 30, ay + 40), (ax + 30, ay + 40), (ax, ay + 70), (ax + 30, ay + 100),
                                        (ax - 30, ay + 100), (ax, ay + 70)]), red, OUT * 0.5, None)
    elif m == "stripes":   # wolf spider: pale stripes along the back
        for k in (-1, 0, 1):
            flat(ctx, lambda c, k=k: p_ellipse(c, ax + 10, ay - 30 + k * 32, arx * 0.75, 8, -0.08), lighter(hexc(cfg["color"]), 0.4))
    elif m == "chevrons":
        for k in range(3):
            stroke(ctx, [(ax - 60 + k * 45, ay - 40), (ax - 40 + k * 45, ay - 15), (ax - 60 + k * 45, ay + 10)], 7,
                   color=lighter(hexc(cfg["color"]), 0.5))


def black_widow(ctx, t, p):
    _spider(ctx, t, p, {"color": "#16161a", "dark": "#0b0b0d", "abd": (165, 150), "mark": "hourglass", "leg": 1.15,
                        "leg_w": 12})


def brown_recluse(ctx, t, p):
    _spider(ctx, t, p, {"color": "#b58a5a", "dark": "#8d6740", "abd": (130, 95), "violin": True, "leg": 1.25,
                        "leg_w": 11})


def wolf_spider(ctx, t, p):
    _spider(ctx, t, p, {"color": "#7a5a3a", "dark": "#5a3f26", "abd": (150, 110), "mark": "stripes", "hair": True,
                        "leg": 1.05, "leg_w": 17})


def jumping_spider(ctx, t, p):
    _spider(ctx, t, p, {"color": "#2b2b2f", "dark": "#18181b", "abd": (120, 100), "mark": "chevrons", "hair": True,
                        "big_eyes": True, "leg": 0.75, "leg_w": 18, "fang": "#3fb6a8"})


def camel_spider(ctx, t, p):
    """Solifuge: NOT a true spider. Huge forward jaws as big as its head (the signature), long hairy pedipalps
    held forward like a 5th leg pair, a soft segmented abdomen, pale sandy hair all over."""
    col, dk = hexc("#d9b77e"), hexc("#b89355")
    walk = p.get("walk", 0.0)
    feet = [200, 70, -120, -260]
    for side in (-1, 1):
        c_leg = col if side == 1 else darker(col, 0.75)
        if side == 1:
            for s_ in range(5):  # segmented abdomen, back to front
                x = -230 + s_ * 40
                shape(ctx, lambda c, x=x, s_=s_: p_ellipse(c, x, -125, 52 + s_ * 3, 60 + s_ * 3), col, OUT * 0.8, (0.0, 0.2))
            _bristles(ctx, -150, -125, 130, 60, 24, 16, -175, -5, 3.0)
            shape(ctx, lambda c: p_ellipse(c, 30, -135, 80, 68), col, OUT, (0.0, 0.25), hi=(0.3, 0.2, 0.2))
            op = 0.3 + 0.6 * p.get("lunge", 0.0)
            for j in (-1, 1):  # the jaws: two pincers, each as big as the head
                jaw = [(80, -150 + j * 12), (170, -170 + j * (25 + 40 * op)), (235, -140 + j * (20 + 30 * op)),
                       (200, -135 + j * 6), (110, -125 + j * 6)]
                shape(ctx, lambda c, jaw=jaw: p_smooth(c, jaw), hexc("#c99a5c"), OUT, (0.0, 0.2))
                stroke(ctx, [(195, -150 + j * 22), (228, -140 + j * 18)], 6, color=hexc("#3a2414"))
            eyes(ctx, 40, -190, 12, 15, p.get("look", (0.4, 0.0)), p.get("mood", "angry"), 0.0)
        for i in range(4):
            sw = math.sin(t * 11 + i * 1.6 + (0 if side == 1 else 3.1)) * walk
            base = (40 - i * 22, -110)
            knee = ((base[0] + feet[i]) / 2 + 12 * sw, -230 - (0 if side == 1 else -20))
            foot = (feet[i] + 25 * sw + (15 if side == 1 else -15), 0 if side == 1 else -30)
            limb(ctx, [base, knee, foot], 11, c_leg, smooth=False)
            _bristles(ctx, (knee[0] + foot[0]) / 2, (knee[1] + foot[1]) / 2, 4, 40, 4, 10, -160, -20, 2.5)
        limb(ctx, [(90, -120), (190, -230 + (0 if side == 1 else 15)), (330, -170)], 15, c_leg, smooth=True)  # pedipalp
        _bristles(ctx, 260, -200, 70, 20, 6, 12, -170, -10, 2.5)


# ------------------------------------------------------------------------------------------- insects (side view)

def _insect_legs(ctx, t, p, col, body_y, hind=1.0, near=True, w=12, spiky=False):
    walk = p.get("walk", 0.0)
    c = col if near else darker(col, 0.72)
    specs = [((70, body_y), [(70, 120), (90, 70), (35, 100)]),          # front
             ((10, body_y), [(70, 95), (95, 85), (35, 110)]),           # middle
             ((-40, body_y), [(140 * hind, -150), (190 * hind, 95), (45, 160)])]  # hind: big femur up and back
    for i, (base, segs) in enumerate(specs):
        end = _leg(ctx, base, segs, w * (1.5 if i == 2 and hind > 1 else 1), c, t, i * 2.1 + (0 if near else 1.5), walk)
        if spiky:
            ink(ctx, 3)
            for s in range(4):
                ctx.move_to(end[0] - 20 - s * 18, end[1] - 30 - s * 10)
                ctx.line_to(end[0] - 12 - s * 18, end[1] - 44 - s * 10)
            ctx.stroke()


def camel_cricket(ctx, t, p):
    """Camel (cave) cricket: a hunched, arched back like a camel, NO wings, banded brown, enormous spiny hind
    legs, antennae longer than the body. The hunch + the legs are what make it read."""
    col, dk = hexc("#b5834f"), hexc("#8a5e33")
    jump = p.get("lunge", 0.0)
    ctx.save()
    ctx.translate(0, -60 * jump)
    _insect_legs(ctx, t, p, col, -150, hind=1.6, near=False, w=10, spiky=True)
    # humped body: head low at the front, the arch peaking over the middle, abdomen tapering down at the back
    body = [(150, -150), (120, -235), (40, -290), (-60, -285), (-160, -230), (-220, -160), (-180, -130),
            (-60, -130), (60, -125)]
    shape(ctx, lambda c: p_smooth(c, body), col, OUT, (0.0, 0.25), hi=(0.3, 0.2, 0.25))
    for k in range(5):  # segment bands over the hump
        x = 60 - k * 45
        stroke(ctx, [(x, -282 + abs(k - 1.5) * 8), (x - 18, -140)], 6, smooth=False, color=dk)
    # head tucked down, long curving antennae
    shape(ctx, lambda c: p_ellipse(c, 165, -165, 52, 58, 0.3), col, OUT, (0.0, 0.2))
    eyes(ctx, 175, -185, 14, 0.1, p.get("look", (0.5, 0.1)), p.get("mood", "calm"), 0.0)
    ant = math.sin(t * 3) * 20
    for k, off in ((0, 0), (1, 30)):
        stroke(ctx, [(205, -205), (320, -330 - off), (470, -340 - off + ant), (600, -260 - off + ant)], 4,
               smooth=True)
    _insect_legs(ctx, t, p, col, -150, hind=1.6, near=True, w=12, spiky=True)
    ctx.restore()


def cockroach(ctx, t, p):
    """American cockroach: flat glossy oval, reddish-brown wings over the body, a pale-rimmed shield behind the
    head, spiny legs, long whip antennae. Gloss highlight is the signature."""
    col, dk = hexc("#7a3b1c"), hexc("#55260f")
    _insect_legs(ctx, t, p, col, -70, hind=1.0, near=False, w=9, spiky=True)
    shape(ctx, lambda c: p_smooth(c, [(170, -95), (60, -140), (-120, -138), (-250, -105), (-260, -70), (-120, -55),
                                      (60, -55), (170, -65)]), col, OUT, (0.0, 0.3), hi=(0.3, 0.2, 0.35))
    stroke(ctx, [(60, -140), (-250, -88)], 4, color=dk)                      # wing line
    flat(ctx, lambda c: p_ellipse(c, -40, -122, 120, 10, -0.08), lighter(col, 0.55), a=0.8)   # gloss
    shape(ctx, lambda c: p_ellipse(c, 150, -95, 55, 40), hexc("#c99a62"), OUT, (0.0, 0.2))   # pronotum shield
    flat(ctx, lambda c: p_ellipse(c, 150, -95, 30, 20), dk)
    shape(ctx, lambda c: p_ellipse(c, 205, -75, 30, 28), dk, OUT, None)
    eyes(ctx, 212, -84, 9, 0.1, p.get("look", (0.5, 0.0)), p.get("mood", "calm"), 0.0)
    sw = math.sin(t * 4) * 25
    for off in (0, 25):
        stroke(ctx, [(228, -90), (360, -180 - off), (520, -170 - off + sw), (640, -120 - off + sw)], 3.5, smooth=True)
    _insect_legs(ctx, t, p, col, -70, hind=1.0, near=True, w=10, spiky=True)


def house_centipede(ctx, t, p):
    """Scutigera: 15 pairs of VERY long striped legs (the signature: it looks like a fringe), short body,
    antennae as long as the body at both ends."""
    col = hexc("#c8a77a")
    stripe = hexc("#5b4a6e")
    walk = p.get("walk", 0.6)
    n = 15
    for side in (-1, 1):
        for i in range(n):
            u = i / (n - 1)                       # 0 = front, 1 = back
            x = 150 - u * 320
            foot_x = 330 - u * 700                # feet spread far wider than the body: the fringe
            c = col if side == 1 else darker(col, 0.75)
            sw = math.sin(t * 14 + i * 0.7 + (0 if side == 1 else 3.1)) * walk * 18
            knee = ((x + foot_x) / 2 + sw, -200 - 40 * math.sin(math.pi * u) - (0 if side == 1 else 25))
            foot = (foot_x + sw, 0 if side == 1 else -30)
            limb(ctx, [(x, -95), knee, foot], 6, c, smooth=False)
            stroke(ctx, [knee, ((knee[0] + foot[0]) / 2, (knee[1] + foot[1]) / 2)], 6, color=stripe)
    shape(ctx, lambda c: p_smooth(c, [(170, -110), (-170, -115), (-180, -80), (170, -75)]), col, OUT, (0.0, 0.25))
    for k in range(3):
        stroke(ctx, [(150, -97 + (k - 1) * 10), (-165, -100 + (k - 1) * 10)], 5, color=stripe)
    eyes(ctx, 175, -100, 9, 0.1, p.get("look", (0.5, 0.0)), p.get("mood", "calm"), 0.0)
    for end, d in ((180, 1), (-180, -1)):
        stroke(ctx, [(end, -100), (end + d * 150, -230), (end + d * 330, -200)], 3.5, smooth=True)


# ------------------------------------------------------------------------------------------- mite (microscope view)

def scabies_mite(ctx, t, p):
    """Sarcoptes as seen under the microscope: a round, pale, turtle-like oval with fine skin ridges, rows of
    peg-like spines on the back, and 8 SHORT stubby legs (4 clustered at the front corners, 4 under the rear)."""
    col, dk = hexc("#efe4cf"), hexc("#cdb894")
    walk = p.get("walk", 0.0)
    for side in (-1, 1):  # front leg pairs poke out at the front corners, rear pairs under the back
        for i, (bx, ang) in enumerate(((130, -25), (100, 10), (-90, 160), (-120, 185))):
            segs = [(55, ang + side * 8), (45, ang + 30 * (1 if bx > 0 else -1))]
            _leg(ctx, (bx, -110 + side * 10), segs, 16, col if side == 1 else darker(col, 0.8), t, i + side, walk, 6)
    shape(ctx, lambda c: p_ellipse(c, 0, -120, 175, 120), col, OUT, (0.0, 0.25), hi=(0.3, 0.2, 0.3))
    for k in range(5):  # fine skin ridges
        ctx.save()
        ink(ctx, 2.5, 0.55)
        ctx.arc(0, -40 - k * 6, 120 + k * 12, math.radians(205), math.radians(335))
        ctx.stroke()
        ctx.restore()
    for r in range(3):  # pegs on the back
        for k in range(5):
            x = -70 + k * 35
            y = -170 + r * 26
            shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 5, 9), dk, OUT * 0.3, None)
    # mouthparts (the "head" is just a small cone at the front) + small cartoon eyes
    shape(ctx, lambda c: p_poly(c, [(165, -140), (215, -118), (165, -96)]), dk, OUT * 0.7, None)
    eyes(ctx, 120, -150, 14, 26, p.get("look", (0.4, 0.0)), p.get("mood", "sneaky"), 0.0)


# ------------------------------------------------------------------------------------------- cassowary (side view)

def cassowary(ctx, t, p):
    """Southern cassowary: a big black shaggy body (hair-like plumage, no visible wings), a long BLUE neck with
    two red wattles, a tall brown casque (helmet), thick grey legs and three toes with a long DAGGER inner claw.
    xray (0..1) makes the dagger claw glow red for the 'four-inch dagger' beat."""
    walk = p.get("walk", 0.0)
    lunge = p.get("lunge", 0.0)
    black, blue, red = hexc("#1a1a1c"), hexc("#2e7ad1"), hexc("#d8342c")
    leg, casque = hexc("#8e8f86"), hexc("#7a5a32")
    kick = lunge * 60

    def foot(fx, k):
        sw = math.sin(t * 7 + k * 3.1) * walk
        knee = (fx - 10 + 30 * sw, -230)
        ankle = (fx + 30 * sw + (kick if k == 1 else 0), -95 - (kick * 0.8 if k == 1 else 0))
        toe = (ankle[0] + 15, -12 - (kick * 0.6 if k == 1 else 0))
        c = leg if k == 1 else darker(leg, 0.75)
        limb(ctx, [(fx, -330), knee, ankle, toe], 46, c, smooth=False)
        for dx in (-55, 25, 70):   # three thick toes
            limb(ctx, [toe, (toe[0] + dx, toe[1] + 10)], 20, c, smooth=False)
        # the dagger: the inner toe's claw, long, curved, dark
        claw = [(toe[0] + 20, toe[1] - 4), (toe[0] + 120, toe[1] - 22), (toe[0] + 175, toe[1] + 8),
                (toe[0] + 110, toe[1] + 2), (toe[0] + 25, toe[1] + 16)]
        glow = p.get("xray", 0.0)
        shape(ctx, lambda c_: p_smooth(c_, claw), red if glow > 0.5 else hexc("#2b2622"), OUT * 0.7, None)

    foot(-20, 0)
    # shaggy body: a big dome with hair-like plumes at the edge
    body = [(190, -420), (90, -520), (-80, -540), (-230, -480), (-300, -380), (-260, -310), (-80, -290), (120, -320)]
    shape(ctx, lambda c: p_smooth(c, body), black, OUT, (0.0, 0.25), hi=(0.3, 0.2, 0.15))
    ink(ctx, 4)
    for i in range(16):
        a = math.radians(150 + i * 7)
        x0, y0 = -60 + 230 * math.cos(a), -400 + 130 * math.sin(a)
        ctx.move_to(x0, y0)
        ctx.curve_to(x0 - 30, y0 + 40, x0 - 50, y0 + 80, x0 - 40 + (i % 3) * 8, y0 + 120)
    ctx.stroke()
    for i in range(10):  # shaggy hem
        x = -260 + i * 42
        shape(ctx, lambda c, x=x: p_poly(c, [(x, -305), (x + 20, -250 - (i % 2) * 20), (x + 40, -300)]), black, OUT * 0.6, None)
    foot(30, 1)
    # neck: long, blue, up and forward; head with casque, beak, wattles
    hx, hy = 250 + 40 * lunge, -720 + 60 * lunge
    limb(ctx, [(120, -440), (200, -560), (hx - 10, hy + 40)], 70, blue, smooth=True)
    flat(ctx, lambda c: p_ellipse(c, 175, -480, 28, 70, 0.4), hexc("#7b3fa8"), a=0.6)  # purple at the base
    shape(ctx, lambda c: p_ellipse(c, hx, hy, 52, 42), blue, OUT, (0.0, 0.2))
    shape(ctx, lambda c: p_smooth(c, [(hx - 30, hy - 30), (hx - 20, hy - 120), (hx + 25, hy - 135), (hx + 45, hy - 40)]),
          casque, OUT, (0.05, 0.2), hi=(0.3, 0.2, 0.25))
    shape(ctx, lambda c: p_poly(c, [(hx + 40, hy - 12), (hx + 125, hy + 6), (hx + 40, hy + 18)]), hexc("#2b2622"),
          OUT * 0.8, None)
    for k in (0, 1):
        shape(ctx, lambda c, k=k: p_ellipse(c, hx - 15 + k * 22, hy + 85 + k * 10, 14, 42), red, OUT * 0.6, None)
    eyes(ctx, hx + 12, hy - 8, 15, 0.1, p.get("look", (0.6, 0.1)), p.get("mood", "angry"), 0.0, pupil=0.55)


ANATOMY = {"cassowary": cassowary, "camel_cricket": camel_cricket, "cockroach": cockroach,
           "black_widow": black_widow, "brown_recluse": brown_recluse, "wolf_spider": wolf_spider,
           "jumping_spider": jumping_spider, "camel_spider": camel_spider, "scabies_mite": scabies_mite,
           "house_centipede": house_centipede}


def _alive(fn):
    # drawn.py sets p["walking"] on a moving actor (the old creatures read that); these builders read p["walk"].
    # Without this bridge the new animals glide with frozen legs. Idle 0.15 keeps legs twitching when standing.
    def draw(ctx, t, p):
        w = 1.0 if p.get("walking") else p.get("walk", 0.15)
        return fn(ctx, t, {**p, "walk": w})
    return draw


ANATOMY = {k: _alive(v) for k, v in ANATOMY.items()}
