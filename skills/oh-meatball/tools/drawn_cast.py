"""People, ships and machines for tools/drawn.py (the conspiracy-case cast), in the drawn_kit style.
Generic drawn people only: no real person's likeness (the "billionaire" is a stock cartoon type).
Origins: ships = waterline centre; subs = hull centre; claw = centre of its frame; people = between the feet."""
import math
import random

from drawn_kit import (INK, OUT, PAL, darker, eyes, flat, hexc, ink, lighter, limb, mouth, p_blob, p_ellipse,
                       p_poly, p_rrect, p_smooth, shape, src, starburst, stroke, sweat)

P = PAL


def _star(ctx, cx, cy, r, color):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.42
        a = -math.pi / 2 + math.pi * i / 5
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    flat(ctx, lambda c: p_poly(c, pts), color)


# ================================================================= ships and machines

def glomar(ctx, t, p):
    """The big recovery ship: long dark hull, white stern block and bridge, a tall lattice derrick midships.
    p: pipe (length of pipe string hanging below the derrick, 0 = none), bob."""
    bob = 6 * math.sin(t * 1.3)
    ctx.translate(0, bob)
    pipe = p.get("pipe", 0)
    if pipe:
        shape(ctx, lambda c: c.rectangle(-22, -100, 44, pipe + 100), P["steel"], OUT * 0.8, None)
        for y in range(0, int(pipe), 260):
            flat(ctx, lambda c, y=y: c.rectangle(-30, y, 60, 22), P["steel_dk"], OUT * 0.5)
    # derrick
    for k in range(9):
        y0, y1 = -150 - k * 85, -150 - (k + 1) * 85
        w0, w1 = 130 - k * 9, 130 - (k + 1) * 9
        stroke(ctx, [(-w0, y0), (w1, y1)], 6)
        stroke(ctx, [(w0, y0), (-w1, y1)], 6)
        stroke(ctx, [(-w1, y1), (w1, y1)], 6)
    stroke(ctx, [(-130, -150), (-50, -915)], 13)
    stroke(ctx, [(130, -150), (50, -915)], 13)
    stroke(ctx, [(-130, -150), (-50, -915)], 6, color=P["derrick"])
    stroke(ctx, [(130, -150), (50, -915)], 6, color=P["derrick"])
    shape(ctx, lambda c: c.rectangle(-70, -950, 140, 40), P["red"], OUT * 0.8, None)
    # hull
    hull = lambda c: p_poly(c, [(-760, -150), (740, -185), (790, -150), (690, 60), (-720, 60)])  # noqa: E731
    shape(ctx, hull, P["hull"], OUT, (0.0, 0.18))
    ctx.save()
    hull(ctx)
    ctx.clip()
    flat(ctx, lambda c: c.rectangle(-900, 10, 1800, 80), P["hull_red"])
    ctx.restore()
    hull(ctx)
    ink(ctx, OUT)
    ctx.stroke()
    # stern block + bridge
    shape(ctx, lambda c: p_rrect(c, -720, -400, 330, 250, 10), P["deck"], OUT, (0.12, 0))
    shape(ctx, lambda c: p_rrect(c, -660, -500, 200, 100, 8), P["deck"], OUT, (0.12, 0))
    for x in range(-690, -420, 62):
        shape(ctx, lambda c, x=x: c.rectangle(x, -350, 40, 34), P["window"], OUT * 0.5, None)
    shape(ctx, lambda c: p_rrect(c, 430, -350, 220, 200, 8), P["deck"], OUT, (0.12, 0))
    for x in range(450, 640, 55):
        shape(ctx, lambda c, x=x: c.rectangle(x, -310, 36, 30), P["window"], OUT * 0.5, None)
    for x in (-300, 250):
        stroke(ctx, [(x, -150), (x + 60, -420), (x + 230, -330)], 8)  # cranes
    # water in front of the hull
    ctx.translate(0, -bob)
    pts = [(x, 30 + 10 * math.sin(x / 70 + t * 2.5)) for x in range(-1000, 1050, 50)]
    ctx.save()
    p_poly(ctx, pts + [(1000, 200), (-1000, 200)])
    src(ctx, P["sea"])
    ctx.fill()
    ctx.restore()
    stroke(ctx, pts, 8, color=P["foam"], a=0.9)


def soviet_ship(ctx, t, p):
    """A small grey trawler with a red-banded funnel and a sailor watching through binoculars."""
    bob = 8 * math.sin(t * 1.6 + 1)
    ctx.translate(0, bob)
    shape(ctx, lambda c: p_poly(c, [(-330, -110), (330, -140), (290, 40), (-300, 40)]), P["steel_dk"], OUT,
          (0, 0.18))
    shape(ctx, lambda c: p_rrect(c, -170, -300, 220, 190, 8), P["deck"], OUT, (0.12, 0))
    for x in (-145, -85, -25):
        shape(ctx, lambda c, x=x: c.rectangle(x, -260, 40, 34), P["window"], OUT * 0.5, None)
    shape(ctx, lambda c: c.rectangle(-60, -430, 90, 130), P["steel"], OUT, (0.15, 0))
    shape(ctx, lambda c: c.rectangle(-60, -400, 90, 40), P["red"], OUT * 0.6, None)
    _star(ctx, -15, -380, 16, hexc("#ffd84a"))
    stroke(ctx, [(200, -140), (200, -420)], 8)
    stroke(ctx, [(120, -380), (280, -380)], 6)
    # sailor with binoculars
    ctx.save()
    ctx.translate(150, -122)
    ctx.scale(0.55, 0.55)
    person(ctx, t, {"skin": P["skin2"], "body": hexc("#1f3c66"), "hat": "sailor", "binoculars": True,
                    "mood": "calm", "blink": p.get("blink", 0)})
    ctx.restore()
    ctx.translate(0, -bob)
    pts = [(x, 30 + 9 * math.sin(x / 60 + t * 2.8)) for x in range(-450, 460, 40)]
    ctx.save()
    p_poly(ctx, pts + [(450, 160), (-450, 160)])
    src(ctx, P["sea"])
    ctx.fill()
    ctx.restore()
    stroke(ctx, pts, 7, color=P["foam"], a=0.9)


def _sub_body(ctx, p, cut=None):
    hull = lambda c: (p_rrect(c, -700, -110, 1400, 220, 110))  # noqa: E731
    shape(ctx, hull, P["sub"], OUT, (0.0, 0.22), hi=(0.4, 0.2, 0.25))
    shape(ctx, lambda c: p_poly(c, [(-130, -95), (-90, -330), (170, -330), (210, -95)]), P["sub"], OUT, (0.1, 0))
    for k, x in enumerate((-70, 30, 130)):
        shape(ctx, lambda c, x=x: p_ellipse(c, x + 10, -330, 38, 12), P["sub_dk"], OUT * 0.6, None)
    _star(ctx, 50, -230, 42, P["red"])
    shape(ctx, lambda c: p_poly(c, [(-700, 0), (-800, -110), (-790, 110)]), P["sub_dk"], OUT * 0.9, None)
    shape(ctx, lambda c: p_ellipse(c, -810, 0, 26, 80), P["steel_dk"], OUT * 0.8, None)
    for x in (-520, -380, 360, 500):
        shape(ctx, lambda c, x=x: p_ellipse(c, x, -10, 22, 22), P["sub_dk"], OUT * 0.5, None)
    if p.get("missiles", 0) > 0:
        a = p["missiles"]
        shape(ctx, lambda c: p_poly(c, [(-115, -100), (-85, -320), (165, -320), (195, -100)]),
              (0.55, 0.85, 1.0), OUT, None, a=0.9 * a)
        for x in (-50, 40, 130):
            shape(ctx, lambda c, x=x: p_rrect(c, x - 22, -300, 44, 190, 20), (0.95, 0.95, 0.95), OUT * 0.6, None,
                  a=a)
            shape(ctx, lambda c, x=x: p_poly(c, [(x - 22, -270), (x, -318), (x + 22, -270)]), P["red"],
                  OUT * 0.6, None, a=a)


def sub(ctx, t, p):
    """K-129 drawn as a cartoon diesel missile sub (bow to the right, three missile hatches in the sail).
    p: missiles (0..1 cut-away showing the three missiles), split (0..1: everything behind the bow breaks
    away and falls), wreck (tilted, darker)."""
    split = p.get("split", 0.0)
    cut = 360
    if split <= 0:
        _sub_body(ctx, p)
        return
    ctx.save()  # the aft part, falling away
    ctx.translate(-120 * split, 1400 * split * split)
    ctx.rotate(0.35 * split)
    ctx.save()
    ctx.rectangle(-1000, -600, 1000 + cut, 1200)
    ctx.clip()
    _sub_body(ctx, p)
    ctx.restore()
    ctx.restore()
    ctx.save()  # the bow piece they kept
    jag = [(cut, -340), (cut - 30, -60), (cut + 25, 0), (cut - 20, 60), (cut + 15, 140)]
    p_poly(ctx, jag + [(1000, 140), (1000, -340)])
    ctx.clip()
    _sub_body(ctx, p)
    ctx.restore()
    stroke(ctx, jag[1:], OUT)


def us_sub(ctx, t, p):
    """A small light-grey US spy sub with a sweeping searchlight; p: light (0..1), flash (0..1)."""
    if p.get("light", 0) > 0:
        sw = 0.18 * math.sin(t * 1.7)
        ctx.save()
        ctx.rotate(sw)
        p_poly(ctx, [(-380, 10), (-1500, -380), (-1500, 520)])
        src(ctx, P["light"], 0.28 * p["light"])
        ctx.fill()
        ctx.restore()
    shape(ctx, lambda c: p_rrect(c, -420, -80, 840, 160, 80), P["us_sub"], OUT, (0, 0.22), hi=(0.4, 0.2, 0.25))
    shape(ctx, lambda c: p_poly(c, [(-60, -70), (-30, -220), (110, -220), (140, -70)]), P["us_sub"], OUT, (0.1, 0))
    shape(ctx, lambda c: p_poly(c, [(420, 0), (500, -80), (495, 80)]), darker(P["us_sub"]), OUT * 0.8, None)
    shape(ctx, lambda c: p_ellipse(c, -410, 10, 34, 34), P["light"], OUT * 0.7, None)
    if p.get("flash", 0) > 0:
        starburst(ctx, -440, 10, 160 * p["flash"], 12, (1, 1, 0.9), OUT * 0.6, t)


def claw(ctx, t, p):
    """The giant capture claw on its pipe: a yellow frame with hooked fingers. p: close (0 open .. 1 shut
    under the sub), broken (0..1: the left fingers snap off and fall away)."""
    cl = p.get("close", 0.0)
    br = p.get("broken", 0.0)
    shape(ctx, lambda c: c.rectangle(-26, -4000, 52, 3880), P["steel"], OUT * 0.8, None)
    xs = [-560, -330, -100, 130, 360, 590]
    for k, x in enumerate(xs):
        gone = br > 0 and k < 3
        ctx.save()
        ctx.translate(x, 40)
        if gone:
            ctx.translate(-60 * br, 900 * br * br)
            ctx.rotate(-0.8 * br)
        side = -1 if k < 3 else 1
        ctx.rotate(math.radians(-side * (14 - 30 * cl)))
        f = lambda c: p_poly(c, [(-34, 0), (34, 0), (40, 420), (-side * 10 + 0, 560), (-side * 150, 610),  # noqa
                                 (-side * 140, 540), (-side * 20, 470), (-34, 420)])
        shape(ctx, f, P["claw"] if not gone else darker(P["claw"], 0.9), OUT, (0.15, 0.05))
        ctx.restore()
    shape(ctx, lambda c: p_rrect(c, -700, -120, 1400, 190, 20), P["claw"], OUT, (0.0, 0.22))
    for x in range(-640, 700, 140):
        stroke(ctx, [(x, -110), (x + 110, 60)], 6, color=P["claw_dk"])
    if br > 0 and br < 0.5:
        starburst(ctx, -330, 60, 220 * (1 - br * 2), 12, (1, 0.85, 0.2), OUT * 0.6, t * 3)


# ================================================================= people

def person(ctx, t, p):
    """A generic drawn person, feet at y = 0, about 900 units tall. p: skin, body (jacket colour), tie,
    hair, hat (None, "fedora", "beanie", "sailor"), glasses ("shades", "round"), mask (burglar band),
    stripes, mood, talk, arm ("up", "point", "hold", "down"), item ("rock", "flashlight", "papers", "sack",
    "notepad"), binoculars, sweat, walk (tiptoe stride on p["phase"])."""
    skin = p.get("skin", P["skin2"])
    body = p.get("body", P["suit"])
    ph = p.get("phase", 0.0)
    stride = 40 * math.sin(ph) if p.get("walking") else 0.0
    bob = 6 * math.sin(t * 2.2 + p.get("seed", 0))
    # legs
    for s, off in ((-1, stride), (1, -stride)):
        limb(ctx, [(s * 40, -380 + bob), (s * 50 + off * 0.6, -190), (s * 50 + off, 0)], 46,
             p.get("pants", P["suit_dk"]), OUT * 0.8, smooth=False)
        shape(ctx, lambda c, s=s, off=off: p_ellipse(c, s * 62 + off, -4, 52, 22), INK, OUT * 0.5, None)
    # torso
    torso = lambda c: p_rrect(c, -125, -720 + bob, 250, 370, 60)  # noqa: E731
    shape(ctx, torso, body, OUT, (0.14, 0.05))
    if p.get("stripes"):
        ctx.save()
        torso(ctx)
        ctx.clip()
        for y in range(-700, -340, 64):
            flat(ctx, lambda c, y=y: c.rectangle(-140, y + bob, 280, 30), P["stripe"])
        ctx.restore()
        torso(ctx)
        ink(ctx, OUT)
        ctx.stroke()
    if p.get("tie"):
        flat(ctx, lambda c: p_poly(c, [(-45, -718 + bob), (45, -718 + bob), (0, -600 + bob)]), P["shirt"], OUT * 0.6)
        shape(ctx, lambda c: p_poly(c, [(-14, -700 + bob), (14, -700 + bob), (22, -520 + bob), (0, -490 + bob),
                                        (-22, -520 + bob)]), p["tie"], OUT * 0.6, None)
    # arms
    arm = p.get("arm", "down")
    hl = (-150, -440 + bob)
    lhand = (-170, -400 + bob)
    rsh = (120, -680 + bob)
    rhand = {"down": (170, -400), "up": (230, -980), "point": (430, -760), "hold": (260, -640),
             "beam": (300, -560)}.get(arm, (170, -400))
    rhand = (rhand[0] + 6 * math.sin(t * 3), rhand[1] + bob)
    relbow = ((rsh[0] + rhand[0]) / 2 + 40, (rsh[1] + rhand[1]) / 2 + 40)
    limb(ctx, [(-120, -680 + bob), (-170, -560 + bob), lhand], 40, body, OUT * 0.8, smooth=False)
    shape(ctx, lambda c: p_ellipse(c, lhand[0], lhand[1], 30, 30), skin, OUT * 0.7, None)
    # head
    hy = -830 + bob
    shape(ctx, lambda c: c.rectangle(-28, hy + 60, 56, 60), skin, OUT * 0.7, None)
    shape(ctx, lambda c: p_ellipse(c, 0, hy, 120, 135), skin, OUT, (0.1, 0.08))
    hair = p.get("hair")
    if hair:
        shape(ctx, lambda c: p_poly(c, [(-122, hy - 10), (-110, hy - 110), (-30, hy - 150), (80, hy - 140),
                                        (125, hy - 60), (118, hy - 20), (60, hy - 90), (-60, hy - 80)]) if False
              else p_smooth(c, [(-122, hy - 5), (-105, hy - 105), (-20, hy - 145), (85, hy - 128),
                                (124, hy - 40), (70, hy - 85), (-40, hy - 82), (-100, hy - 40)]), hair, OUT * 0.8,
              (0.1, 0.1))
    mood = p.get("mood", "calm")
    gl = p.get("glasses")
    if p.get("mask"):
        shape(ctx, lambda c: p_rrect(c, -126, hy - 60, 252, 66, 30), P["mask"], OUT * 0.6, None)
        for s in (-1, 1):
            shape(ctx, lambda c, s=s: p_ellipse(c, s * 45, hy - 27, 26, 20), (1, 1, 1), OUT * 0.4, None)
            flat(ctx, lambda c, s=s: p_ellipse(c, s * 45 + 6, hy - 25, 9, 10), INK)
    elif gl == "shades":
        for s in (-1, 1):
            shape(ctx, lambda c, s=s: p_rrect(c, s * 48 - 40, hy - 52, 80, 50, 16), INK, OUT * 0.5, None)
            flat(ctx, lambda c, s=s: p_ellipse(c, s * 48 - 16, hy - 38, 10, 7), (1, 1, 1), a=0.7)
        stroke(ctx, [(-8, hy - 32), (8, hy - 32)], 6)
    elif not p.get("binoculars"):
        eyes(ctx, 0, hy - 30, 24, 46, p.get("look", (0, 0)), mood, p.get("blink", 0), OUT * 0.6, lid=skin)
        if gl == "round":
            for s in (-1, 1):
                ctx.new_sub_path()
                ctx.arc(s * 46, hy - 30, 40, 0, 2 * math.pi)
                ink(ctx, 7)
                ctx.stroke()
    mouth(ctx, 0, hy + 55, 64, p.get("mouth", "smile" if mood in ("calm", "happy", "smug") else "flat"),
          p.get("talk", 0.0), OUT * 0.7)
    if p.get("sweat"):
        sweat(ctx, 140, hy - 70 + 10 * ((t * 1.5) % 1), 26)
    hat = p.get("hat")
    if hat == "fedora":
        shape(ctx, lambda c: p_ellipse(c, 0, hy - 112, 175, 30), P["suit_dk"], OUT * 0.8, None)
        shape(ctx, lambda c: p_rrect(c, -105, hy - 230, 210, 125, 40), P["suit_dk"], OUT * 0.8, (0.1, 0))
        flat(ctx, lambda c: c.rectangle(-105, hy - 140, 210, 22), P["tie"], OUT * 0.5)
    elif hat == "beanie":
        shape(ctx, lambda c: p_poly(c, [(-124, hy - 60), (-110, hy - 150), (0, hy - 190), (110, hy - 150),
                                        (124, hy - 60)]), P["mask"], OUT * 0.8, (0.1, 0))
    elif hat == "sailor":
        shape(ctx, lambda c: p_rrect(c, -120, hy - 170, 240, 80, 30), (1, 1, 1), OUT * 0.8, (0, 0.2))
        flat(ctx, lambda c: c.rectangle(-120, hy - 110, 240, 24), hexc("#1f3c66"))
    if p.get("binoculars"):
        for s in (-1, 1):
            shape(ctx, lambda c, s=s: p_rrect(c, s * 45 - 32, hy - 70, 64, 90, 18), INK, OUT * 0.4, None)
            flat(ctx, lambda c, s=s: p_ellipse(c, s * 45, hy - 64, 20, 10), (0.6, 0.8, 1.0))
        rhand = (60, hy + 30)
        relbow = (190, hy + 160)
    limb(ctx, [rsh, relbow, rhand], 40, body, OUT * 0.8, smooth=False)
    shape(ctx, lambda c: p_ellipse(c, rhand[0], rhand[1], 30, 30), skin, OUT * 0.7, None)
    item = p.get("item")
    hx, hy2 = rhand
    if item == "rock":
        shape(ctx, lambda c: p_blob(c, hx + 10, hy2 - 50, 70, 55, 0.15, seed=3), P["rock"], OUT * 0.8, (0.12, 0.15),
              hi=(0.3, 0.3, 0.2))
    elif item == "flashlight":
        p_poly(ctx, [(hx + 20, hy2 - 10), (hx + 900, hy2 - 280), (hx + 900, hy2 + 300)])
        src(ctx, P["light"], 0.25)
        ctx.fill()
        shape(ctx, lambda c: p_rrect(c, hx - 30, hy2 - 22, 90, 44, 10), P["steel_dk"], OUT * 0.6, None)
    elif item == "papers":
        ctx.save()
        ctx.translate(hx, hy2 - 60)
        ctx.rotate(-0.2)
        shape(ctx, lambda c: c.rectangle(-60, -90, 150, 190), P["paper"], OUT * 0.7, (0.1, 0.1))
        for r in range(4):
            stroke(ctx, [(-40, -60 + r * 36), (60, -60 + r * 36)], 7)
        ctx.restore()
    elif item == "sack":
        shape(ctx, lambda c: p_blob(c, -200, -650 + bob, 150, 170, 0.08, seed=5), P["sack"], OUT, (0.15, 0.1))
    elif item == "notepad":
        shape(ctx, lambda c: c.rectangle(hx - 50, hy2 - 120, 100, 130), P["paper"], OUT * 0.6, None)


def billionaire(ctx, t, p):
    """A stock cartoon tycoon (not a likeness): sharp suit, gold tie, slick hair, shades, smug grin."""
    q = {"skin": P["skin2"], "body": P["suit"], "tie": P["tie"], "hair": P["hair"], "glasses": "shades",
         "mood": "smug", "mouth": "grin", "arm": "up", "item": "rock"}
    q.update(p)
    person(ctx, t, q)


def burglar(ctx, t, p):
    q = {"skin": P["skin2"], "body": P["mask"], "stripes": True, "mask": True, "hat": "beanie",
         "pants": P["mask"], "mouth": "flat", "arm": "beam", "item": "flashlight"}
    q.update(p)
    person(ctx, t, q)


def spokesman(ctx, t, p):
    """An official at a podium with a round seal (no lettering)."""
    q = {"skin": P["skin3"], "body": P["suit"], "tie": hexc("#2a3f86"), "hair": hexc("#2a2a2a"),
         "glasses": "round", "mood": "calm", "mouth": "flat"}
    q.update(p)
    ctx.save()
    ctx.translate(0, -20)
    person(ctx, t, q)
    ctx.restore()
    shape(ctx, lambda c: p_poly(c, [(-260, -470), (260, -470), (220, 0), (-220, 0)]), P["podium"], OUT, (0.12, 0))
    shape(ctx, lambda c: p_ellipse(c, 0, -280, 110, 110), P["seal"], OUT * 0.8, None)
    shape(ctx, lambda c: p_ellipse(c, 0, -280, 80, 80), hexc("#2a3f86"), OUT * 0.6, None)
    _star(ctx, 0, -284, 55, P["seal"])
    for s in (-1, 1):
        stroke(ctx, [(s * 60, -470), (s * 140, -640)], 10)
        shape(ctx, lambda c, s=s: p_ellipse(c, s * 150, -660, 26, 36), INK, 0, None)


def reporters(ctx, t, p):
    """A front row of reporters seen from behind: heads, shoulders, raised mics and a flashing camera."""
    rng = random.Random(2)
    for k, x in enumerate((-620, -260, 140, 520)):
        hair = (hexc("#3a2a1e"), hexc("#d9b86a"), hexc("#222222"), hexc("#7a3b20"))[k]
        coat = (hexc("#5b6b7a"), hexc("#8a4b3c"), hexc("#3c5a46"), hexc("#4b4f7a"))[k]
        y = 30 * math.sin(t * 2 + k)
        shape(ctx, lambda c, x=x, y=y: p_rrect(c, x - 170, -260 + y, 340, 360, 110), coat, OUT, (0.1, 0.05))
        shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x, -380 + y, 115, 125), hair, OUT, (0.1, 0.1))
        if k in (0, 2):
            stroke(ctx, [(x + 150, -200 + y), (x + 220, -520 + y)], 22)
            shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x + 225, -560 + y, 34, 42), P["steel"], OUT * 0.7, None)
        if k == 3:
            shape(ctx, lambda c, x=x, y=y: p_rrect(c, x - 90, -620 + y, 180, 120, 14), INK, OUT * 0.5, None)
            shape(ctx, lambda c, x=x, y=y: p_ellipse(c, x, -560 + y, 40, 40), P["steel"], OUT * 0.5, None)
            on = (t * 1.7 + rng.random()) % 1 < 0.12
            if on:
                starburst(ctx, x, -650 + y, 140, 12, (1, 1, 0.92), OUT * 0.5, t)


# ================================================================= paper, props, effects

def papers(ctx, t, p):
    """A secret file: photo of the tycoon pinned to a round seal by red string, redaction bars, no words."""
    ctx.rotate(-0.06 + 0.02 * math.sin(t * 1.5))
    shape(ctx, lambda c: c.rectangle(-330, -430, 660, 860), P["folder"], OUT, (0.04, 0.03))
    shape(ctx, lambda c: c.rectangle(-300, -460, 600, 860), P["paper"], OUT, (0.04, 0.03))
    shape(ctx, lambda c: c.rectangle(-250, -400, 220, 260), hexc("#d8e6ee"), OUT * 0.8, None)
    ctx.save()
    ctx.translate(-140, -160)
    ctx.scale(0.28, 0.28)
    billionaire(ctx, t, {"arm": "down", "item": None})
    ctx.restore()
    shape(ctx, lambda c: p_ellipse(c, 150, -270, 110, 110), P["seal"], OUT * 0.8, None)
    shape(ctx, lambda c: p_ellipse(c, 150, -270, 78, 78), hexc("#2a3f86"), OUT * 0.6, None)
    _star(ctx, 150, -274, 50, P["seal"])
    pull = p.get("string", 1.0)
    stroke(ctx, [(-40, -270), (55 * pull - 40 + 0, -230), (40 + 0 * pull, -270)], 8, smooth=True,
           color=P["string"], a=min(1, pull * 1.5))
    for (x, y) in ((-140, -400), (150, -380)):
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 16, 16), P["red"], OUT * 0.5)
    for r in range(6):
        y = -60 + r * 62
        w = 480 if r % 3 else 300
        stroke(ctx, [(-250, y), (-250 + w, y)], 9)
        if r in (1, 4):
            flat(ctx, lambda c, y=y: c.rectangle(-120, y - 20, 260, 40), INK)


def newspaper(ctx, t, p):
    """A front page flying in and spinning: a heavy masthead bar, a picture of the ship, column scribbles."""
    sp = p.get("spin", 0.0)
    ctx.rotate(sp * 6.28 * 2)
    ctx.scale(max(0.05, min(1.0, p.get("grow", 1.0))), max(0.05, min(1.0, p.get("grow", 1.0))))
    shape(ctx, lambda c: c.rectangle(-360, -470, 720, 940), P["paper"], OUT, (0.04, 0.03))
    flat(ctx, lambda c: c.rectangle(-310, -420, 620, 90), INK)
    shape(ctx, lambda c: c.rectangle(-310, -290, 620, 330), P["sky2"], OUT * 0.7, None)
    ctx.save()
    ctx.translate(0, -60)
    ctx.scale(0.36, 0.36)
    glomar(ctx, t, {})
    ctx.restore()
    for col in (-310, 10):
        for r in range(6):
            stroke(ctx, [(col, 90 + r * 58), (col + 290, 90 + r * 58)], 8)


def desk(ctx, t, p):
    """An office desk seen from the front (Meatball hides behind it); top at y = -420."""
    shape(ctx, lambda c: p_rrect(c, -380, -440, 760, 60, 10), P["desk"], OUT, (0, 0.25))
    shape(ctx, lambda c: c.rectangle(-350, -385, 700, 385), P["desk_dk"], OUT, (0.1, 0))
    for y in (-340, -220, -100):
        shape(ctx, lambda c, y=y: c.rectangle(130, y, 190, 90), P["desk"], OUT * 0.6, None)
    shape(ctx, lambda c: p_poly(c, [(-300, -440), (-260, -560), (-180, -560), (-140, -440)]), P["claw"], OUT * 0.7,
          None)
    stroke(ctx, [(-220, -560), (-220, -620), (-300, -680)], 10)
    shape(ctx, lambda c: p_poly(c, [(-360, -700), (-240, -720), (-250, -640)]), hexc("#3c7a46"), OUT * 0.6, None)


def bubbles(ctx, t, p):
    rng = random.Random(p.get("seed", 1))
    for _ in range(int(p.get("n", 14))):
        x0 = rng.uniform(-200, 200)
        sp = rng.uniform(80, 200)
        r = rng.uniform(10, 30)
        y = -((t * sp + rng.uniform(0, 900)) % 900)
        x = x0 + 18 * math.sin(t * 3 + x0)
        ctx.new_sub_path()
        ctx.arc(x, y, r, 0, 2 * math.pi)
        ctx.set_source_rgba(0.85, 0.95, 1.0, 0.35)
        ctx.fill_preserve()
        ctx.set_source_rgba(1, 1, 1, 0.9)
        ctx.set_line_width(4)
        ctx.stroke()


def ruler(ctx, t, p):
    """A depth ruler: a tall strip from y = 0 down to y = length with a tick every 500 units (no numbers)."""
    L = p.get("length", 8600)
    shape(ctx, lambda c: c.rectangle(-40, 0, 80, L), hexc("#ffd84a"), OUT, None)
    for y in range(0, int(L) + 1, 250):
        stroke(ctx, [(-40, y), (0 if y % 1000 else 30, y)], 7)


def gull(ctx, t, p):
    f = math.sin(t * 8 + p.get("seed", 0))
    stroke(ctx, [(-70, -20 * f), (-30, 10), (0, 0), (30, 10), (70, -20 * f)], 10, smooth=True)


ACTORS = {"glomar": glomar, "soviet_ship": soviet_ship, "sub": sub, "us_sub": us_sub, "claw": claw,
          "person": person, "billionaire": billionaire, "burglar": burglar, "spokesman": spokesman,
          "reporters": reporters, "papers": papers, "newspaper": newspaper, "desk": desk, "bubbles": bubbles,
          "ruler": ruler, "gull": gull}
