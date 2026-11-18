#!/usr/bin/env python3
"""16:9 Saturday long-form "What Happens If You Leave a House Centipede in Your Bathroom" (4:25): one question,
followed through one week in Meatball's bathroom. Episode layer on top of tools/drawn_ranked.py (the flagship
engine: v4 look, voice E with per-line acting, pause rules, gap lint, scene-detect-safe cuts, BUG CAM, freak-out,
captions); this file only adds the bathroom's rooms and times of night, a few props, the typed opening question,
the chapter re-hook cards and the shot table. The flagship build is untouched (its outline has no "act" fields).

  build OUTLINE.json SPEC.json      outline -> spec (voice kokoro:adam-puck, formant 1.05, each line's "act" directs it)
  render SPEC.json OUT.mp4          (drawn_ranked render)
  lint SPEC.json STEM.wav --work REPORT.txt     voice-only stem + silencedetect gap report
  linesheet SPEC.json OUT.jpg [--only ids] [--fracs a,b]
  check SPEC.json                   runtime and holds

Constraints from the brief (Studio 11/18): no prop is shown going outside in the snow, and the "escort it outdoors"
method is never acted out (the card states it; the picture stays inside: QA #10 11/18, Meatball holds the front door
open with a bow, a paper cup and card in paw, and the cup is never over the bug).
"""
import copy
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import drawn_ranked as R  # noqa: E402
import drawn  # noqa: E402
from drawn_kit import OUT, PAL, ease, flat, hexc, p_ellipse, p_poly, p_rrect, shape, stroke  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

W, H = R.W, R.H
YEL, RED, GREEN = R.YEL, R.RED, R.GREEN
A, lab, popset, stamp = R.A, R.lab, R.popset, R.stamp


# ================================================================================================ props


def rk_mat(ctx, t, p):
    """A bath mat on the floor (perspective), 520 wide; p lump (0..1 a bump where something hides)."""
    lump = p.get("lump", 0.0)
    shape(ctx, lambda c: p_poly(c, [(-240, -40), (240, -40), (270, 20), (-270, 20)]), hexc("#5aa7c9"), OUT, None)
    for k in range(-3, 4):
        stroke(ctx, [(k * 70, -36), (k * 77, 16)], 5, color=hexc("#3f8db0"))
    if lump > 0.01:
        shape(ctx, lambda c: p_ellipse(c, 40, -44, 90, 18 * lump), hexc("#5aa7c9"), OUT * 0.6, None)


def rk_antennae(ctx, t, p):
    """Two antenna tips feeling around out of a gap (origin = the gap)."""
    for k in (-1, 1):
        w = math.sin(t * 6 + k) * 18
        stroke(ctx, [(k * 10, 0), (k * 50 + w, -70), (k * 120 + w * 1.6, -120)], 5, smooth=True, color=hexc("#3a2a1a"))


def rk_towel(ctx, t, p):
    """A towel draped from the sink rim (origin) down to the floor at p dx, p dy."""
    dx, dy = p.get("dx", 260), p.get("dy", 600)
    on = p.get("on", 1.0)
    if on <= 0.01:
        return
    dy *= ease(min(1.0, on))
    shape(ctx, lambda c: p_poly(c, [(-60, 0), (60, 0), (dx + 90, dy), (dx - 90, dy)]), hexc("#f2c75c"), OUT, None)
    for k in range(1, 4):
        stroke(ctx, [(-60 + 120 * k / 4, 0), (dx - 90 + 180 * k / 4, dy)], 3, color=hexc("#d9a83a"))


def rk_fan(ctx, t, p):
    """A wall exhaust fan: a square grille, blades that spin when p spin > 0 (p dead: a puff of dust)."""
    shape(ctx, lambda c: p_rrect(c, -130, -130, 260, 260, 18), (0.93, 0.93, 0.9), OUT, None)
    a0 = t * 14 * p.get("spin", 0.0)
    for k in range(4):
        a = a0 + k * math.pi / 2
        shape(ctx, lambda c, a=a: p_ellipse(c, 55 * math.cos(a), 55 * math.sin(a), 52, 20, a), hexc("#9aa4b0"), OUT * 0.5, None)
    for y in range(-110, 120, 28):
        stroke(ctx, [(-110, y), (110, y)], 3, a=0.5)
    if p.get("dust", 0.0) > 0.01:
        d = p["dust"]
        for k in range(6):
            flat(ctx, lambda c, k=k: p_ellipse(c, -60 + 25 * k, 150 + 60 * d + 10 * (k % 2), 30 * d, 22 * d), (0.7, 0.68, 0.62), a=0.8 * (1 - d * 0.5))


def rk_trap(ctx, t, p):
    """A small yellow sticky trap card on the floor; p bugs (0..1 tiny specks appear on it)."""
    shape(ctx, lambda c: p_rrect(c, -120, -40, 240, 50, 8), hexc("#ffd34d"), OUT * 0.7, None)
    n = int(6 * p.get("bugs", 0.0))
    for k in range(n):
        flat(ctx, lambda c, k=k: p_ellipse(c, -90 + 33 * k, -16 + 9 * (k % 2), 7, 4), hexc("#2a2018"))


def rk_snow(ctx, t, p):
    """Snow falling inside a window rectangle (origin = top left, p w, h): seen from indoors only."""
    w, h = p.get("w", 300), p.get("h", 260)
    ctx.save()
    ctx.rectangle(0, 0, w, h)
    ctx.clip()
    for k in range(40):
        x = (k * 53.3) % w + 8 * math.sin(t + k)
        y = ((k * 37.1) + t * 60 * (0.6 + 0.4 * (k % 3))) % h
        flat(ctx, lambda c, x=x, y=y: p_ellipse(c, x, y, 5, 5), (1, 1, 1), a=0.9)
    ctx.restore()


def rk_steam(ctx, t, p):
    """Steam curling up (origin = the bottom of the plume)."""
    for k in range(4):
        y = -((t * 60 + k * 90) % 360)
        a = 0.35 * (1 + y / 360)
        flat(ctx, lambda c, k=k, y=y: p_ellipse(c, 30 * math.sin(t * 1.5 + k), y, 70 + 20 * k % 40, 40), (1, 1, 1), a=max(0.0, a))


drawn.ACTORS.update(rk_mat=rk_mat, rk_antennae=rk_antennae, rk_towel=rk_towel, rk_fan=rk_fan, rk_trap=rk_trap,
                    rk_snow=rk_snow, rk_steam=rk_steam)


# QA #10 (11/18 12:47 PM) visual fixes: nothing on screen dies (0:41), the bug bomb's mist stops at the cabinet edge
# (3:22), Meatball holds the front door open with a bow, cup and card in paw, the cup never over the bug (3:30).
def rk_greysil(ctx, t, p):
    """Any actor (p kind, its params kp) as a flat grey silhouette: a still icon, it never moves or tips over."""
    ctx.push_group()
    drawn.ACTORS[p["kind"]](ctx, 0.0, dict(p.get("kp", {})))
    pat = ctx.pop_group()
    r, g, b = p.get("col", (0.55, 0.56, 0.6))
    ctx.set_source_rgba(r, g, b, p.get("a", 1.0))
    ctx.mask(pat)


def rk_card(ctx, t, p):
    """A plain cream card (origin = centre), p w, h."""
    w, h = p.get("w", 1300), p.get("h", 560)
    shape(ctx, lambda c: p_rrect(c, -w / 2, -h / 2, w, h, 36), hexc(p.get("fill", "#f3ead6")), OUT, None)


def rk_vanity(ctx, t, p):
    """A bathroom vanity cabinet, origin = bottom centre, p w (580), h (500); a dark crack in the baseboard at p crack
    (x offset from the origin) where the house centipede waits."""
    w, h = p.get("w", 580), p.get("h", 500)
    shape(ctx, lambda c: p_rrect(c, -w / 2, -h, w, h, 10), hexc("#c99a62"), OUT, None)
    shape(ctx, lambda c: p_rrect(c, -w / 2 - 20, -h - 40, w + 40, 46, 10), hexc("#eef2f4"), OUT, None)
    flat(ctx, lambda c: c.rectangle(-w / 2 + 10, -40, w - 20, 34), hexc("#4a3424"))
    for dx in (-w / 4, w / 4):
        shape(ctx, lambda c, dx=dx: p_rrect(c, dx - w / 4 + 22, -h + 30, w / 2 - 44, h - 90, 8), hexc("#d8ad78"), OUT * 0.6, None)
        shape(ctx, lambda c, dx=dx: p_ellipse(c, dx + (-w / 4 + 50 if dx > 0 else w / 4 - 50), -h / 2, 12, 12), hexc("#8a8f99"), OUT * 0.5, None)
    cx = p.get("crack")
    if cx is not None:
        flat(ctx, lambda c: p_poly(c, [(cx - 70, -6), (cx + 70, -6), (cx + 60, -48), (cx + 20, -40), (cx - 10, -56), (cx - 60, -42)]),
             hexc("#14100c"))


def rk_mist(ctx, t, p):
    """Bug-bomb mist rolling in from the right along the floor (origin = the stop line on the floor): its front edge
    never passes x 0 (the cabinet edge); p reach 0..1, len (how far right it starts)."""
    reach, ln = p.get("reach", 0.0), p.get("len", 1200)
    if reach <= 0.01:
        return
    front = ln * (1 - ease(min(1.0, reach)))
    ctx.save()
    ctx.rectangle(0, -2000, 6000, 2200)
    ctx.clip()
    for k in range(26):
        x = front + (k * 97.3) % (ln + 300) + 14 * math.sin(t * 1.3 + k)
        y = -40 - (k * 61.7) % 460 + 12 * math.sin(t * 1.7 + 2 * k)
        r = 90 + (k * 37) % 70
        shape(ctx, lambda c, x=x, y=y, r=r: p_ellipse(c, x, y, r, r * 0.7), hexc("#b8cf8f"), OUT * 0.35, None, a=0.85)
    for k in range(5):   # the curl where it bunches up against the cabinet
        y = -60 - k * 95
        bx = front + 40 + 10 * math.sin(t * 3 + k)
        shape(ctx, lambda c, bx=bx, y=y: p_ellipse(c, bx, y, 70, 55), hexc("#cfe0a8"), OUT * 0.35, None, a=0.9)
    ctx.restore()


def rk_frontdoor(ctx, t, p):
    """The front door from inside, swung open (origin = the floor at the frame's left edge, 420 wide, 1120 tall):
    the night porch and falling snow show through; the door leaf opens in toward the room on the right."""
    w, h = 420, 1120
    shape(ctx, lambda c: c.rectangle(-30, -h - 30, w + 60, h + 30), hexc("#3a2a20"), OUT, None)
    flat(ctx, lambda c: c.rectangle(0, -h, w, h), hexc("#16204a"))
    flat(ctx, lambda c: c.rectangle(0, -230, w, 230), hexc("#dfe8f2"))
    stroke(ctx, [(0, -230), (w, -230)], 4, color=hexc("#b9c6d6"))
    ctx.save()
    ctx.translate(0, -h)
    rk_snow(ctx, t, {"w": w, "h": h})
    ctx.restore()
    flat(ctx, lambda c: p_ellipse(c, w * 0.75, -h + 160, 46, 46), hexc("#f6f1c8"))
    shape(ctx, lambda c: p_poly(c, [(w, -h), (w + 210, -h - 60), (w + 210, 60), (w, 0)]), hexc("#8a3b2c"), OUT, None)
    for y0, y1 in ((-h + 60, -h * 0.55), (-h * 0.47, -60)):
        shape(ctx, lambda c, y0=y0, y1=y1: p_poly(c, [(w + 40, y0 - 8), (w + 170, y0 - 40), (w + 170, y1 + 40), (w + 40, y1 + 8)]),
              hexc("#9c4a38"), OUT * 0.5, None)
    shape(ctx, lambda c: p_ellipse(c, w + 185, -h * 0.5, 14, 18), hexc("#e3c25a"), OUT * 0.5, None)
    shape(ctx, lambda c: p_poly(c, [(-40, 0), (w + 40, 0), (w + 70, 40), (-70, 40)]), hexc("#6b4a2e"), OUT * 0.7, None)


drawn.ACTORS.update(rk_greysil=rk_greysil, rk_card=rk_card, rk_vanity=rk_vanity, rk_mist=rk_mist, rk_frontdoor=rk_frontdoor)

# Meatball's bow at the door: leaning toward it, the screen-left arm out holding it, cup and card in the right paw.
import mascot  # noqa: E402
mascot.POSES["bow"] = {"l": ("ik", "shoulder", (-230, 60), 1), "r": (40, 70, 10), "lean": -12, "tilt": -18, "knee": 8,
                       "mouth": "smile", "brow": "calm", "eyes": "bliss", "gaze": "viewer"}
mascot.PERSONA.add("bow")
_prev_prop = drawn.draw_prop


def _draw_prop(ctx, prop, hx, hy, k, t, beam=True):
    """cupcard: a paper cup (open side up, never turned over) and an index card, held in the right paw."""
    if prop != "cupcard":
        return _prev_prop(ctx, prop, hx, hy, k, t, beam=beam)
    ctx.save()
    ctx.translate(hx, hy)
    ctx.scale(k, k)
    ctx.save()
    ctx.translate(40, -40)
    ctx.rotate(0.25)
    shape(ctx, lambda c: p_rrect(c, -60, -95, 120, 85, 6), (1, 1, 1), OUT * 0.6, None)
    for y in (-75, -55, -35):
        stroke(ctx, [(-45, y), (45, y)], 3, color=hexc("#7fa7d9"))
    ctx.restore()
    shape(ctx, lambda c: p_poly(c, [(-48, -70), (48, -70), (34, 40), (-34, 40)]), (0.97, 0.97, 0.95), OUT * 0.6, None)
    flat(ctx, lambda c: p_poly(c, [(-44, -40), (44, -40), (41, -18), (-41, -18)]), hexc("#e5383b"))
    shape(ctx, lambda c: p_ellipse(c, 0, -70, 48, 12), (0.88, 0.88, 0.85), OUT * 0.5, None)
    ctx.restore()


drawn.draw_prop = _draw_prop


def ov_typed(arr, b, t, o):
    """The opening question typed onto the screen, letter by letter, as the first card."""
    a = drawn.at_time(b["words"], o.get("at", 0.0))
    d = o.get("dur", 1.6)
    if t < a:
        return
    n = max(1, int(len(o["text"]) * min(1.0, (t - a) / d)))
    s = o["text"][:n] + ("|" if n < len(o["text"]) and int(t * 6) % 2 == 0 else "")
    im = R.txt(s, o.get("px", 104), YEL, 9)
    full = R.txt(o["text"], o.get("px", 104), YEL, 9)
    drawn.paste(arr, im, W // 2 - (full.width - im.width) // 2, o.get("y", 90))


R.OVS["typed"] = ov_typed

# ================================================================================================ rooms and times

B = {"scene": "bathroom", "sp": {"dark": False}, "bug": "centipede"}
R.ROOMS.update({
    "bathA": dict(B, mx=1350, bpos=[600, 840], bs=0.42, light="off"),                 # 11 PM, light on, tile by the mirror
    "bathB": dict(B, mx=1350, bpos=[640, 960], bs=0.42, light="lamp"),                # 11 PM, steamy, warm lamp
    "bathN": dict(B, mx=1500, bpos=[900, 1500], bs=0.42, light="flashlight"),         # 2 AM, lights off
    "bathS": dict(B, mx=620, bpos=[60, 897], bs=0.2, light="off"),                    # 3 AM, the sink, light on
    "bathD": dict(B, mx=1200, bpos=[300, 1496], bs=0.3, light="off"),                 # day 3, noon daylight
    "hallM": {"scene": "rk_hall", "sp": {}, "mx": 900, "bug": "centipede", "bpos": [300, 1496], "bs": 0.3, "light": "off"},
    "laundry": {"scene": "keeper_room", "sp": {}, "mx": 700, "bug": None, "light": "off"},
    "kitchenN": {"scene": "kitchen", "sp": {}, "mx": 1450, "bug": None, "light": "lamp"},
    "houseN": {"scene": "ds_house_ext", "sp": {}, "mx": None, "bug": None, "light": "off"},
    "dawn": dict(B, mx=1350, bpos=[600, 840], bs=0.42, light="off"),
})
CH_ROOM = ["bathA", "bathB", "bathN", "bathS", "bathD", "hallM", "dawn"]
CH_TINT = [None, [1.0, 0.95, 0.85, 0.10], None, None, [1.0, 0.92, 0.6, 0.10], [1.0, 0.95, 0.8, 0.06], [1.0, 0.6, 0.6, 0.14]]
R.CH_ROOM = CH_ROOM
R.CH_BUG = ["centipede"] * 7
R.BEATS = ["s0.l1", "s1.l6", "s2.l2", "s3.l5", "s4.l5", "s5.l8"]   # 0.3 s before these punchlines (>= 30 s apart)

_orig_expand = R.expand


def _expand(spec, lines, durs):
    beats = _orig_expand(spec, lines, durs)
    for b in beats:
        seg = int(b["ds_id"].split(".")[0][1:])
        if CH_TINT[seg] and not b.get("tint") and b.get("scene") in ("bathroom", "rk_hall"):
            b["tint"] = CH_TINT[seg]
    return beats


R.expand = _expand

# ================================================================================================ shots

NV = {"type": "cam", "kind": "seccam", "title": "BUG CAM: NIGHT VISION", "title_x": 330, "title_y": 760, "title_px": 72,
      "place": "BATHROOM", "clock": 2 * 3600}
SHOE = lambda idn, pos, s=0.8, **kw: A(idn, "tc_prop", pos, s, {"kind": "slipper"}, **kw)  # noqa: E731
SINK = [60, 897]


def _table():
    T = {}
    # ------------------------------------------------------------------ cold open: 11 PM, the shoe
    T["s0.l0"] = dict(f="bM", cuts=["leave|55%"], pose="shock", zb=1.6, card=False, flash=[0.0],
                      bug={"p": {"mood": "calm"}, "moves": [{"at": 0.0, "dur": 2.5, "pos": [700, 820], "walk": True}]},
                      ov=[{"type": "typed", "text": "WHAT HAPPENS IF YOU LEAVE IT?", "at": 0.05, "dur": 1.8}],
                      sfx=["click@0", "sting@0.05", "thud@leave|55%"], no_bugcam=True)
    T["s0.l1"] = dict(f="wm", cuts=["grabs|60%"], pose="point", look="hero", mb={"prop": "slipper"}, sfx=["whoosh@0.05"])
    T["s0.l2"] = dict(f="Mb", cuts=["Put|30%"], pose="shock", mb={"prop": "slipper", "shake": 0.6}, sfx=["scratch@0.02", "stamp@Stop|10%"],
                      no_bugcam=True, burst=True, **stamp("STOP", "Stop|5%", RED, 960, 420, 190, -8))
    T["s0.l3"] = dict(f="kkk", room="board", roomscene="rk_board_bg", cams=[[0, 0, 1.0, 1.05], [600, 0, 1.0, 1.05], [1200, 0, 1.0, 1.05]],
                      cuts=["leave|35%", "move|70%"], mb={"hidden": True}, bug=None, card=False,
                      x=[A("s1", "sp.house_centipede", [0, 120], 0.35, {}, rot=90), lab("q1", "DIES?", [0, -250], "dry|10%", px=110, color=YEL),
                         A("s2", "sp.house_centipede", [600, 120], 0.35, {}), lab("q2", "LEAVES?", [600, -250], "leave|35%", px=110, color=YEL),
                         A("s3", "sp.house_centipede", [1200, 120], 0.35, {}), A("bag", "tp_suitcase", [1350, 120], 0.6, {}),
                         lab("q3", "MOVES IN?", [1200, -250], "move|70%", px=110, color=YEL)],
                      sfx=["pop@dry|10%", "pop@leave|35%", "pop@move|70%"])
    T["s0.l4"] = dict(f="wk", room="hallM", cams=[[-300, 1000, 1.2, 1.3]], cuts=["leave|30%"], pose="present", bug=None, card_x=1300,
                      mb={"pos": [300, 1500], "prop": "slipper"},
                      x=[A("sign", "ds_label", [-300, 1000], 1.0, {"text": "DO NOT DISTURB: SCIENCE", "px": 54, "color": "#1a1a1a", "bg": "#ffffff", "on": 0.0},
                           set=popset("check|60%"))])
    T["s0.l5"] = dict(f="kb", cams=[[800, 700, 1.1, 1.15]], mb={"hidden": True}, card_x=960,
                      x=[A("doc", "cl_paper", [420, 620], 1.1, {"kind": "paper"}, moves=[{"at": 0.0, "dur": 0.4, "pos": [420, 640]}]),
                         lab("uky", "UNIVERSITY OF KENTUCKY ENTOMOLOGY", [420, 300], "Kentucky|10%", px=48, color="#ffffff"),
                         A("st", "rk_steam", [1000, 1000], 1.5, {})])
    T["s0.l6"] = dict(f="kk", room="houseN", cams=[[600, 1050, 0.8, 0.85], [400, 1250, 1.3, 1.4]], cuts=["rooms|50%"], mb={"hidden": True},
                      x=[A("p1", "sp.house_centipede", [150, 1400], 0.14, {}), lab("l1", "BASEMENT", [150, 1300], "often|20%", px=56, color=YEL),
                         A("p2", "sp.house_centipede", [600, 1100], 0.14, {}), lab("l2", "CLOSET", [600, 1000], "turn|40%", px=56, color=YEL),
                         A("p3", "sp.house_centipede", [1050, 1400], 0.14, {}), lab("l3", "KITCHEN", [1050, 1300], "rooms|60%", px=56, color=YEL)],
                      sfx=["pop@often|20%", "pop@turn|40%", "pop@rooms|60%"])
    # ------------------------------------------------------------------ 11 PM: why the bathroom (steamy)
    T["s1.l0"] = dict(f="wM", cuts=["water|60%"], pose="think", x=[A("st", "rk_steam", [80, 880], 1.4, {})])
    T["s1.l1"] = dict(f="bk", cams=[[1250, 1400, 1.6, 1.7]], cuts=["waxy|50%"], zb=2.4, ov=[{"type": "cam", "kind": "bugcam", "at": 0.0, "to": "waxy|50%"}],
                      x=[A("beetle", "sp.beetle", [1250, 1500], 0.5, {}), lab("wx", "WAXY COAT", [1250, 1560], "waxy|55%", px=56, color=YEL)])
    T["s1.l2"] = dict(f="bm", pose="present", x=[A("dr", "droplets", [600, 900], 1.0, {"n": 8, "r": 300}), lab("da", "DRY AIR", [600, 600], "dry|40%", px=80, color="#ff9f43")],
                      sfx=["whoosh@dry|40%"])
    T["s1.l3"] = dict(f="M", pose="deadpan", look="viewer", bug={"hidden": True}, mb={"gest": [["licks|40%", "laugh", 0.8]]})
    # QA #10: the other centipedes are grey silhouettes on a card under a DRY AIR stamp; nothing marches, tips or wilts
    T["s1.l4"] = dict(f="kkk", room="board", roomscene="rk_board_bg", cams=[[0, 40, 0.95, 1.0], [0, 120, 1.35, 1.42], [0, 60, 1.05, 1.1]],
                      cuts=["house|0%", "lack|0%"], mb={"hidden": True}, bug=None,
                      x=[A("card", "rk_card", [0, 120], 1.0, {"w": 1400, "h": 560}),
                         lab("oth", "OTHER CENTIPEDES", [0, -80], None, px=64, color="#ffffff")] +
                        [A("o%d" % k, "rk_greysil", [-430 + 430 * k, 300], 0.55, {"kind": "house_centipede"}) for k in range(3)],
                      **stamp("DRY AIR", "shortly|40%", "#ff9f43", 960, 600, 150, -8), sfx=["stamp@shortly|40%"])
    T["s1.l5"] = dict(f="bw", pose="shrug", look="hero", light={"kind": "lamp", "dark": 0.5}, x=[lab("only", "ALL YEAR", [600, 640], "year|60%", px=80, color=YEL)])
    T["s1.l6"] = dict(f="kb", cams=[[900, 800, 1.2, 1.3]], mb={"hidden": True},
                      x=[lab("se1", "SPRING", [1000, 520], "live|10%", px=70, color=GREEN), lab("se2", "SUMMER", [1000, 620], "entire|35%", px=70, color=YEL),
                         lab("se3", "FALL", [1000, 720], "life|60%", px=70, color="#ff9f43"), lab("se4", "WINTER", [1000, 820], "indoors|80%", px=70, color="#7fd1ff")],
                      sfx=["tink@live|10%", "tink@entire|35%", "tink@life|60%", "tink@indoors|80%"])
    T["s1.l7"] = dict(f="Mw", pose="deadpan", look="hero", mb={"prop": "paper"}, x=[lab("bill", "WATER BILL", [1550, 800], "water|50%", px=60, color="#ffffff")])
    T["s1.l8"] = dict(f="kb", cams=[[710, 520, 1.6, 1.7]], mb={"hidden": True}, x=[A("snow", "rk_snow", [560, 260], 1.0, {"w": 300, "h": 260})])
    T["s1.l9"] = dict(f="M", pose="deadpan", bug={"hidden": True}, x=[lab("nov", "NOVEMBER", [1650, 640], 0.0, px=70, color=RED)])
    T["s1.l10"] = dict(f="bP", cuts=["opening|50%"], zb=3.0, bug={"p": {"look": [-1, 0]}}, mb={"hidden": True}, ov=[{"type": "cam", "kind": "bugcam", "at": 0.0}],
                       x=[A("gl", "rk_glow", [430, 780], 1.0, {"r": 30, "on": 0.0}, front=True, set=popset("opening|50%", dur=0.5))], no_bugcam=True)
    T["s1.l11"] = dict(room="board", roomscene="microscope", f="kMk", burst=True, pose="think", cams=[[960, 1100, 0.6, 0.65], [960, 1150, 1.3, 1.4]],
                       cuts=["paper|30%", "proven|60%"], mb={"pos": [4000, 1500]}, bug=None, x=[A("c", "sp.house_centipede", [960, 1300], 0.5, {})],
                       **stamp("NOT PROVEN", "proven|60%", RED, 960, 330, 130), sfx=["stamp@proven|60%"])
    T["s1.l12"] = dict(f="wk", cams=[[1400, 600, 1.6, 1.7]], cuts=["fan|55%"], pose="facepalm", bug={"hidden": True},
                       x=[A("fan", "rk_fan", [1400, 600], 0.9, {"spin": 0.0, "dust": 0.0}, set=[{"at": "fan|60%", "dur": 0.6, "p": {"dust": 1.0}}])],
                       sfx=["thud@fan|60%"])
    T["s1.l13"] = dict(f="kM", cams=[[1100, 600, 1.4, 1.5]], pose="think", bug={"hidden": True},
                       x=[A("clk", "wall_clock", [1100, 600], 1.0, {})], flash=["eat|80%"], sfx=["hit@eat|80%"])
    # ------------------------------------------------------------------ 2 AM: night vision
    T["s2.l0"] = dict(f="bk", cams=[[900, 1300, 1.2, 1.3]], ov=[dict(NV, at=1.4)], mb={"hidden": True}, no_bugcam=True,
                      bug={"pos": [1300, 1500], "moves": [{"at": "cam|60%", "dur": 1.5, "pos": [1000, 1500], "walk": True}]})
    T["s2.l1"] = dict(f="bMb", cuts=["station|30%", "nocturnal|60%"], burst=True, pose="nervous", mb={"pos": [2600, 1500]},
                      ov=[dict(NV, at=0.0, to="station|30%", clock=2 * 3600 + 30), dict(NV, at="nocturnal|60%", clock=2 * 3600 + 34)], no_bugcam=True,
                      bug={"pos": [1250, 1500], "moves": [{"at": "nocturnal|30%", "dur": 1.5, "pos": [900, 1500], "walk": True}]})
    T["s2.l2"] = dict(f="kb", cams=[[1300, 1250, 1.0, 1.1]], ov=[dict(NV, at=0.0, clock=2 * 3600 + 60)], mb={"hidden": True}, no_bugcam=True,
                      bug={"pos": [1100, 1500], "moves": [{"at": "floors|20%", "dur": 0.6, "pos": [1450, 1490], "rot": -90},
                                                          {"at": "walls|50%", "dur": 1.4, "pos": [1450, 900]}]})
    T["s2.l3"] = dict(f="mM", room="kitchenN", pose="laugh", look="viewer", bug=None, tint=[0.2, 0.3, 0.6, 0.25], cuts=["menu|60%"])
    T["s2.l4"] = dict(card=False, f="kkkk", room="board", roomscene="rk_board_bg", cams=[[0, 0, 1.4, 1.45], [600, 0, 1.4, 1.45], [1200, 0, 1.4, 1.45], [1800, 0, 1.4, 1.45]],
                      cuts=["crickets|30%", "moths|55%", "earwigs|80%"], mb={"hidden": True}, bug=None, ov=[dict(NV, at=0.0, clock=2 * 3600 + 90)],
                      x=[A("f1", "sp.fly", [0, 120], 0.6, {}), lab("m1", "FLIES", [0, -180], None, px=90),
                         A("f2", "camel_cricket", [600, 120], 0.8, {}), lab("m2", "CRICKETS", [600, -180], None, px=90),
                         A("f3", "sp.moth", [1200, 120], 0.6, {}), lab("m3", "MOTHS", [1200, -180], None, px=90),
                         A("f4", "sp.earwig", [1800, 120], 0.6, {}), lab("m4", "EARWIGS", [1800, -180], None, px=90)],
                      sfx=["pop@flies|5%", "pop@crickets|30%", "pop@moths|55%", "pop@earwigs|80%"])
    T["s2.l5"] = dict(f="bP", zb=2.6, ov=[{"type": "cam", "kind": "bugcam", "at": 0.0}], mb={"hidden": True}, no_bugcam=True,
                      x=[A("moth", "sp.moth", [1000, 1480], 0.2, {}, moves=[{"at": "hold|60%", "dur": 0.3, "pos": [1000, 2200]}])], sfx=["tink@barbed|30%"])
    T["s2.l6"] = dict(f="Mm", pose="shrug", bug={"hidden": True}, light="lamp", mb={"gest": [["Meatball|40%", "point", 0.8]]})
    T["s2.l7"] = dict(f="kb", room="bathS", cams=[[60, 860, 1.8, 2.0]], ov=[dict(NV, at=0.0, clock=2 * 3600 + 160)], mb={"hidden": True}, no_bugcam=True,
                      bug={"pos": [200, 870], "moves": [{"at": "fall|50%", "dur": 0.5, "pos": [60, 897]}]}, sfx=["whoosh@fall|50%"])
    T["s2.l8"] = dict(f="wM", room="bathS", pose="nervous", bug={"hidden": True}, light={"kind": "lamp", "dark": 0.6},
                      mb={"pos": [900, 1500], "moves": [{"at": 0.2, "dur": 1.2, "pos": [700, 1500], "walk": True}]},
                      x=[A("clk", "wall_clock", [1200, 560], 0.8, {})], flash=["bathroom|80%"], sfx=["click@bathroom|80%"])
    # ------------------------------------------------------------------ 3 AM: the sink (the one big freak-out)
    T["s3.l0"] = dict(f="bMw", cuts=["It's#2|40%", "my|70%"], pose="shock", freak=[0.1, "my|70%"], shake=[0.1, "It's#2|40%", "my|70%"],
                      flash=[0.05], zb=2.6, no_bugcam=True,
                      mb={"shake": 1.0, "moves": [{"at": 0.1, "dur": 0.55, "pos": [700, 1500], "hop": 420}, {"at": "my|70%", "dur": 0.5, "pos": [760, 1500], "hop": 300}]},
                      sfx=["sting@0.05", "boing@0.1", "hit@my|70%"])
    T["s3.l1"] = dict(f="Mb", pose="nervous", look="hero", cuts=["bite|50%"])
    T["s3.l2"] = dict(f="bwM", cuts=["handled|40%", "pressed|70%"], pose="think", look="hero", zb=2.2)
    T["s3.l3"] = dict(f="wk", cams=[[300, 1150, 1.0, 1.05]], cuts=["towel|40%"], pose="present", look="hero",
                      x=[A("tw", "rk_towel", [150, 890], 1.0, {"dx": 330, "dy": 610, "on": 0.0}, set=[{"at": "towel|40%", "dur": 0.6, "p": {"on": 1.0}}])],
                      mb={"moves": [{"at": "host|70%", "dur": 0.4, "pos": [900, 1500]}]}, sfx=["whoosh@towel|40%"])
    T["s3.l4"] = dict(f="kb", cams=[[400, 1150, 1.1, 1.15]], mb={"hidden": True}, zb=1.8,
                      x=[A("tw", "rk_towel", [150, 890], 1.0, {"dx": 330, "dy": 610})],
                      bug={"moves": [{"at": "aggressive|30%", "dur": 1.2, "pos": [480, 1490], "rot": 60}, {"at": "flee|60%", "dur": 0.4, "pos": [800, 1496], "rot": 0}]},
                      sfx=["scratch@flee|60%"])
    T["s3.l5"] = dict(f="kb", cams=[[900, 1350, 1.2, 1.3]], mb={"hidden": True}, zb=1.8,
                      x=[A("mat", "rk_mat", [1000, 1510], 1.2, {"lump": 0.0}, front=True, lit=True, set=[{"at": "mat|60%", "dur": 0.4, "p": {"lump": 1.0}}])],
                      bug={"pos": [600, 1496], "moves": [{"at": "darts|10%", "dur": 0.6, "pos": [1000, 1500]}]}, sfx=["scratch@darts|10%"])
    T["s3.l6"] = dict(f="wM", pose="deadpan", bug={"hidden": True}, x=[A("mat", "rk_mat", [1000, 1510], 1.2, {"lump": 1.0})],
                      mb={"pos": [1300, 1500], "moves": [{"at": "stepping|30%", "dur": 1.6, "pos": [1700, 1500], "walk": True}]})
    # ------------------------------------------------------------------ day 3: noon daylight
    T["s4.l0"] = dict(f="wM", cuts=["daylight|50%"], pose="think", bug={"hidden": True},
                      x=[A("mat", "rk_mat", [1000, 1510], 1.2, {}, moves=[{"at": "No|30%", "dur": 0.4, "pos": [1000, 1300], "rot": -20}])])
    T["s4.l1"] = dict(f="kk", cams=[[300, 1440, 2.6, 2.8], [600, 1300, 1.2, 1.3]], cuts=["cracks|55%"], mb={"hidden": True}, bug={"hidden": True},
                      ov=[{"type": "cam", "kind": "bugcam", "at": 0.0, "to": "cracks|55%"}],
                      x=[A("ant", "rk_antennae", [300, 1495], 1.4, {})])
    T["s4.l2"] = dict(f="mk", cams=[[600, 1200, 1.2, 1.3]], cuts=["droppings|40%"], pose="present", bug={"hidden": True}, mb={"prop": "magnifier"},
                      sfx=["tink@droppings|45%", "tink@damage|60%"])
    T["s4.l3"] = dict(f="wM", pose="laugh", look="viewer", bug={"hidden": True},
                      x=[A("pile", "rk_pile", [1650, 1500], 0.4, {}), A("sock", "tc_prop", [1500, 1500], 0.6, {"kind": "sock"})])
    T["s4.l4"] = dict(f="M", burst=True, pose="you", look="viewer", bug={"hidden": True}, sfx=["scratch@0.02", "hit@catch|60%"])
    T["s4.l5"] = dict(f="kM", cams=[[1600, 1050, 1.6, 1.7]], pose="shock", bug={"hidden": True}, x=[A("dr", "droplets", [1600, 1050], 0.8, {"n": 6, "r": 220})])
    T["s4.l6"] = dict(f="Mw", pose="deadpan", bug={"hidden": True}, tint=[1, 1, 1, 0.22], x=[A("st", "rk_steam", [80, 880], 1.6, {})])
    T["s4.l7"] = dict(f="kk", room="board", roomscene="rk_board_bg", cams=[[400, 0, 1.1, 1.15], [800, 60, 1.0, 1.05]], cuts=["plenty|45%"], mb={"hidden": True}, bug=None,
                      x=[A("c", "sp.house_centipede", [0, 120], 0.4, {})] +
                        [A("b%d" % k, ["sp.fly", "sp.moth", "sp.earwig", "sp.roach"][k % 4], [500 + 170 * (k % 6), 120 - 60 * (k // 6)], 0.18, {},
                           set=[{"at": "plenty|%d%%" % (45 + 4 * k), "dur": 0.2, "p": {}}]) for k in range(12)],
                      sfx=["pop@plenty|50%"])
    T["s4.l8"] = dict(f="kM", cams=[[1100, 600, 1.4, 1.5]], pose="think", bug={"hidden": True},
                      x=[A("cal", "ds_prop", [1100, 620], 0.9, {"kind": "calendar", "day": 3.0}, set=[{"at": "mean|30%", "dur": 1.0, "p": {"day": 7.0}}])],
                      sfx=["hit@do|85%"])
    # ------------------------------------------------------------------ day 7: hallway and laundry, morning
    T["s5.l0"] = dict(f="wM", pose="present", bug={"hidden": True}, x=[A("tr", "rk_trap", [1250, 1300], 1.2, {})])
    T["s5.l1"] = dict(f="kk", cams=[[300, 1450, 2.2, 2.4], [600, 1400, 1.4, 1.5]], cuts=["many|55%"], mb={"hidden": True}, bug=None,
                      ov=[{"type": "cam", "kind": "bugcam", "at": 0.0, "to": "many|55%"}],
                      x=[A("t1", "rk_trap", [300, 1496], 1.2, {"bugs": 0.0}, set=[{"at": "bugs|30%", "dur": 1.2, "p": {"bugs": 1.0}}]),
                         A("t2", "rk_trap", [800, 1496], 1.2, {"bugs": 0.0}, set=[{"at": "many|60%", "dur": 1.0, "p": {"bugs": 0.6}}])])
    T["s5.l2"] = dict(f="Mm", pose="nervous", bug={"hidden": True}, mb={"shake": 0.6}, x=[A("tr", "rk_trap", [1080, 1180], 1.3, {})])
    # QA #10: the line is only "focus on the bugs they eat": the crossed-out things are small prey bugs (no water drop)
    T["s5.l3"] = dict(f="kMk", burst=True, pose="point", room="board", roomscene="rk_board_bg", cams=[[300, 0, 1.2, 1.25], [1100, 0, 1.2, 1.25]],
                      cuts=["control|0%", "focus|0%"], mb={"pos": [700, 1500]}, bug=None,
                      x=[A("fl", "sp.fly", [300, 100], 0.5, {}), A("x1", "ds_cross", [300, 0], 1.0, {"on": 0.0, "r": 200}, set=popset("says|30%")),
                         A("p1", "sp.moth", [1000, 60], 0.3, {}), A("p2", "sp.fly", [1200, 140], 0.3, {}), A("p3", "sp.earwig", [1050, 190], 0.3, {}),
                         A("x2", "ds_cross", [1100, 60], 1.0, {"on": 0.0, "r": 220}, set=popset("bugs|30%"))],
                      sfx=["stamp@says|30%", "stamp@bugs|30%"])
    T["s5.l4"] = dict(f="wM", room="laundry", pose="present", bug=None, mb={"prop": "paper"},
                      x=[A("pud", "droplets", [1200, 1480], 0.8, {"n": 6, "r": 120}), lab("dry", "DRY IT OUT", [950, 1150], "dry|20%", px=80, color=GREEN)])
    T["s5.l5"] = dict(f="kw", room="laundry", cams=[[1200, 1250, 1.3, 1.4]], cuts=["dehumidifiers|60%"], pose="point", bug=None,
                      x=[A("dh", "cl_box", [1200, 1500], 0.9, {}), lab("dhl", "DEHUMIDIFIER", [1200, 1050], "dehumidifiers|60%", px=70, color=YEL)])
    # QA #10: the bug bomb's mist rolls in and stops at the cabinet edge; the antennae wave on, safe in the crack
    T["s5.l6"] = dict(f="kkkk", room="bathA", cams=[[700, 1200, 1.1, 1.15], [650, 1330, 1.6, 1.66], [380, 1400, 2.4, 2.5], [700, 1260, 1.25, 1.3]],
                      cuts=["Ohio|0%", "rarely|0%", "where|0%"], mb={"hidden": True},
                      bug={"hidden": True},
                      x=[A("van", "rk_vanity", [690, 1500], 1.0, {"crack": -360}), A("ant", "rk_antennae", [330, 1478], 1.3, {}),
                         A("mist", "rk_mist", [980, 1500], 1.0, {"reach": 0.0, "len": 1300}, front=True,
                           set=[{"at": "skip|0%", "dur": 1.7, "p": {"reach": 1.0}}])],
                      sfx=["whoosh@skip|10%"])
    # QA #10: the escort line: Meatball holds the front door open with a bow, a paper cup and card in paw; the bug stays
    # on the floor far from the cup (the cup is never over it), nothing goes outside
    T["s5.l7"] = dict(f="kkkkkk", room="hallM", cams=[[330, 1000, 0.85, 0.9], [200, 1000, 1.3, 1.36], [380, 1080, 1.6, 1.68],
                                                         [330, 1000, 0.85, 0.9], [-270, 900, 1.5, 1.56], [250, 1030, 1.15, 1.2]],
                      cuts=["Maryland|0%", "escort|0%", "Penn|0%", "survive|0%", "Pennsylvania|0%"], pose="bow", look="viewer", mb={"pos": [330, 1500], "prop": "cupcard"},
                      bug={"pos": [1050, 1496], "p": {"mood": "calm", "look": [-1, 0]}},
                      x=[A("door", "rk_frontdoor", [-480, 1500], 1.0, {})], no_bugcam=True)
    # the card states the method; the picture stays indoors (brief: no prop goes outside, the method is not acted out)
    T["s5.l8"] = dict(f="kkk", room="hallM", cams=[[200, 1000, 1.3, 1.36], [-270, 900, 1.5, 1.56], [330, 1000, 0.85, 0.9]],
                      cuts=["for|0%", "went|0%"], pose="bow", look="viewer",
                      no_bugcam=True, mb={"pos": [330, 1500], "prop": "cupcard"}, card_px=78,
                      bug={"pos": [1050, 1496], "p": {"mood": "calm", "look": [1, 0]}, "flip": False,
                           "moves": [{"at": "went|0%", "dur": 1.6, "pos": [2400, 1496], "walk": True}]},
                      x=[A("door", "rk_frontdoor", [-480, 1500], 1.0, {})])
    T["s5.l9"] = dict(f="Mb", room="bathD", cuts=["mat|55%"], pose="deadpan", look="viewer", bug={"hidden": True}, zb=2.0,
                      x=[A("mat", "rk_mat", [1000, 1510], 1.2, {"lump": 0.6}), A("ant", "rk_antennae", [760, 1490], 1.0, {})],
                      bugpos_for_frame=[850, 1500])
    # ------------------------------------------------------------------ the answer: dawn
    T["s6.l0"] = dict(f="bw", pose="think", look="hero", bug={"p": {"mood": "calm"}})
    T["s6.l1"] = dict(f="kkk", cams=[[300, 1440, 2.6, 2.7], [900, 1300, 1.2, 1.3], [60, 600, 1.5, 1.6]], cuts=["hunts|35%", "prefers|65%"], mb={"hidden": True},
                      bug={"hidden": True}, x=[A("ant", "rk_antennae", [300, 1495], 1.4, {}), A("st", "rk_steam", [80, 880], 1.6, {})],
                      ov=[dict(NV, at="hunts|35%", to="prefers|65%")])
    T["s6.l2"] = dict(f="Mk", cams=[[1400, 600, 1.6, 1.7]], pose="point", bug={"hidden": True},
                      x=[A("fan", "rk_fan", [1400, 600], 0.9, {"spin": 1.0})], **stamp("VERDICT: IT STAYS", "verdict|20%", GREEN, 700, 420, 110, -6),
                      sfx=["stamp@verdict|20%"])
    T["s6.l3"] = dict(f="kw", room="hallM", cams=[[-300, 1100, 1.4, 1.5]], cuts=["closet|55%"], pose="laugh", bug=None, mb={"pos": [200, 1500]},
                      x=[SHOE("shoe", [-300, 1480], 0.8)])
    T["s6.l4"] = dict(f="M", burst=True, pose="you", look="viewer", bug=None, room="hallM", sfx=["hit@comments|70%"])
    T["s6.l5"] = dict(card=False, f="wk", room="hallM", cams=[[-300, 1000, 1.2, 1.3]], cuts=["ranked|50%"], pose="point", bug=None, mb={"pos": [400, 1500]},
                      x=[lab("door", "WATCH NEXT: HOUSE BUGS RANKED", [-300, 760], "six|20%", px=56, color=YEL)])
    return T


SHOTS = _table()


def build(outline, out_spec):
    o = json.load(open(outline))
    R.SHOTS = copy.deepcopy(SHOTS)
    for si, seg in enumerate(o["segments"]):   # the chapter re-hook card (and its sting) on each chapter's first line
        if si == 0:
            continue
        sh = R.SHOTS.setdefault(f"s{si}.l0", {"f": "wm"})
        kick = seg["chapter"].split(":", 1)[-1].strip().upper()
        sh.setdefault("ov", []).insert(0, {"type": "suspect", "text": seg.get("chip") or kick, "kicker": kick, "at": 0.0})
        sh.setdefault("sfx", [])[:0] = ["sting@0", "hit@0.05"]
        sh["card_at"] = 1.5
    R.build(outline, out_spec)
    spec = json.load(open(out_spec))
    spec.update(burst="loud", voice=o.get("voice", "kokoro:adam-puck"), formant=o.get("formant", 1.05), beat_lines=R.BEATS, speed_k=0.70,
                end_text="HOUSE BUGS RANKED  ·  HOUSE CENTIPEDE", end_hold=float(o.get("end_screen_seconds", 20)),
                cap_key=["centipede", "centipedes", "bathroom", "sink", "bite", "water", "humid", "humidity", "night",
                         "nocturnal", "winter", "stop", "shoe", "fan", "traps", "moisture", "flee", "hides", "stays"],
                _note=spec["_note"].replace("tools/drawn_ranked.py build", "tools/drawn_bathroom.py build (drawn_ranked engine)"))
    json.dump(spec, open(out_spec, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("spec")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--lines")
    ap.add_argument("--work")
    ap.add_argument("--only")
    ap.add_argument("--big")
    ap.add_argument("--frac", type=float, default=0.6)
    ap.add_argument("--fracs")
    x = ap.parse_args()
    if x.cmd == "build":
        build(x.spec, x.out)
    elif x.cmd == "render":
        R.render(x.spec, x.out, x.lines, x.work)
    elif x.cmd == "linesheet":
        R.linesheet(x.spec, x.out, x.only.split(",") if x.only else None, x.frac, x.work or "/dev/shm/bath-lines", big=x.big,
                    fracs=[float(v) for v in x.fracs.split(",")] if x.fracs else None)
    elif x.cmd == "check":
        R.check(x.spec)
    elif x.cmd == "lint":
        if x.out and x.out.lower().endswith((".mp4", ".mov", ".mkv")):   # 11/18: never write the stem over a video
            sys.exit("lint: OUT is the voice-stem .wav to write, not the video (%s)" % x.out)
        sys.exit(0 if R.gap_lint(x.spec, x.out, x.work or os.path.splitext(x.out)[0] + "-gaps.txt") else 1)
    elif x.cmd == "voice":
        R.voice_cache(json.load(open(x.spec)), json.load(open(x.spec))["lines"])
    else:
        raise SystemExit(__doc__)
