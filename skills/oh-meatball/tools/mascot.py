#!/usr/bin/env python3
"""Meatball 2.0 rig: the channel's stick-figure mascot, drawn in code so every frame is on-model.

Usage: mascot.py OUTDIR            -> renders every pose to OUTDIR/<pose>.png (+ sheet.png)
       from mascot import draw; draw("point", 600) -> RGBA PIL image (stills, thumbnails)
       mascot.animate(pose, size, words, dur, fps, outdir) -> talking PNG frames (video)
Poses: neutral, point, present, shrug, think, shock, laugh, facepalm, wave, deadpan, nervous
Props (drawn beside him, never animated): prop("fork", height)

The body is a skeleton (hip, knees, spine, neck, shoulders, head) with shoulder/elbow/wrist ANGLES per
arm. Poses are angle sets (or IK targets on the face/chest), and animation blends between them with
eased, anticipating, slightly overshooting transitions. How he moves: research/41-animator.md.
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

INK = (17, 17, 17, 255)
MEAT = (150, 78, 44, 255)
MEAT_DARK = (112, 54, 30, 255)
SHINE = (214, 140, 98, 255)
SAUCE = (196, 38, 30, 255)
PARSLEY = (64, 150, 60, 255)
WHITE = (255, 255, 255, 255)
DROP = (120, 190, 240, 255)

# Skeleton in the 1000-unit drawing (rest): hip (500,790), feet (440,960)/(560,960), shoulders (500,560),
# spine top (500,505), head centre (500,360) radius 150. Arm bones are fixed lengths so poses stay on-model.
HIP, FEET = (500.0, 790.0), ((440.0, 960.0), (560.0, 960.0))
SPINE_UP, SHOULDER_UP, HEAD_UP = 285.0, 230.0, 145.0  # hip->spine top, hip->shoulders, spine top->head centre
UPPER, FORE, PALM = 105.0, 95.0, 8.0
LIMB, HAND_R = 26, 22
HEAD_C, HEAD_R = (500, 360), 150
CONTENT = (0.94, -0.34)  # default direction of the photo/text panel from Meatball: screen right, a bit up

# Arm = (shoulder, elbow, wrist) degrees. Shoulder 0 = hanging down, 90 = straight out to that side,
# 180 = straight up; elbow/wrist are relative bends (+ = further out/up). ("ik", ref, (dx, dy), bend) puts
# the hand on a point relative to the head centre or shoulders instead. "aim" points along CONTENT.
REST = (38, -24, 0)
POSES = {
    "neutral":  {"l": REST, "r": REST, "mouth": "smile", "brow": "calm", "gaze": "viewer"},
    "point":    {"l": REST, "r": "aim", "lean": 2.5, "tilt": 3, "mouth": "talk", "brow": "up", "gaze": "content"},
    "present":  {"l": REST, "r": (64, 34, 12), "lean": 1.5, "tilt": 2, "mouth": "smile", "brow": "calm",
                 "gaze": "content"},
    "shrug":    {"l": (78, 58, 10), "r": (78, 58, 10), "shrug": 9, "tilt": -5, "mouth": "flat", "brow": "up",
                 "gaze": "viewer"},
    "think":    {"l": (30, -42, 0), "r": ("ik", "head", (42, 72), -1), "tilt": -6, "lean": -1, "mouth": "flat",
                 "brow": "tilt", "gaze": "up"},
    "shock":    {"l": ("ik", "head", (-136, 52), -1), "r": ("ik", "head", (136, 52), -1), "lean": -3, "knee": 5,
                 "shrug": 6, "mouth": "o", "brow": "up", "gaze": "viewer"},
    "laugh":    {"l": (32, -50, 0), "r": (32, -50, 0), "lean": -3, "tilt": -6, "mouth": "laugh", "brow": "up", "eyes": "bliss",
                 "gaze": "viewer"},
    "facepalm": {"l": REST, "r": ("ik", "head", (30, 8), -1), "tilt": 7, "lean": 2, "mouth": "frown",
                 "brow": "cross", "gaze": "viewer"},
    "wave":     {"l": REST, "r": (100, 40, 0), "tilt": 3, "mouth": "smile", "brow": "calm", "gaze": "viewer"},
    # Ask kit (research/46): arm straight out and down to screen right, toward the platform's follow button.
    "subpoint": {"l": REST, "r": (52, 2, 0), "lean": 3, "tilt": 5, "mouth": "talk", "brow": "up", "gaze": "viewer"},
    # Showrunner persona (research/39): half-lidded and unimpressed; and food-anxious, hands clasped, one sweat drop.
    "deadpan":  {"l": (30, -20, 0), "r": (30, -20, 0), "mouth": "flat", "brow": "lid", "gaze": "viewer"},
    "nervous":  {"l": ("ik", "shoulder", (-12, 112), 1), "r": ("ik", "shoulder", (12, 112), 1), "knee": 4,
                 "shrug": 5, "mouth": "wobble", "brow": "worry", "gaze": "viewer"},
}
BIG = {"shock", "shrug", "wave", "laugh"}   # moves that get an anticipation crouch
REALIZE = {"shock", "laugh"}               # moves that land with a scale-pop
GLOWS = {"white": None, "yellow": (255, 214, 10), "red": (232, 46, 36), "green": (70, 205, 90)}
PERSONA = {"deadpan", "nervous", "think", "facepalm", "subpoint"}  # held for the whole line (the point too)
TRANSIENT = {"shock": 1.2, "laugh": 1.5, "wave": 1.4}   # real reaction beats only, then he moves on
SECONDARY = {"point": ["present", "shrug"], "present": ["point", "shrug"], "shrug": ["present", "point"],
             "neutral": ["present", "point"], "shock": ["present", "point"], "laugh": ["present"],
             "wave": ["present"]}
AFTER = {"shock": "present", "laugh": "neutral", "wave": "neutral"}
STRESS = {"every", "never", "all", "only", "really", "not", "no", "exactly", "whole", "too", "still", "nothing",
          "always", "huge", "tiny", "million", "thousand", "both", "even", "true", "false", "actually", "zero"}
YOU = {"you", "your", "you'll", "you're", "yourself", "you've"}


# ---------------------------------------------------------------- skeleton

def _rot(v, deg):
    a = math.radians(deg)
    return (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a))


def _add(a, b, s=1.0):
    return (a[0] + b[0] * s, a[1] + b[1] * s)


def _dir(side, ang):
    """Unit vector of an arm angle; side -1 = screen-left arm (mirrored), +1 = screen-right."""
    a = math.radians(ang)
    return (side * math.sin(a), math.cos(a))


def _angle(side, v):
    return math.degrees(math.atan2(side * v[0], v[1]))


def _ik(root, target, l1, l2, side, bend):
    """Two-bone IK: (first-bone angle, relative bend) that put the chain's end on target."""
    dx, dy = target[0] - root[0], target[1] - root[1]
    d = min(max(math.hypot(dx, dy), abs(l1 - l2) + 1), l1 + l2 - 0.01)
    phi = _angle(side, (dx, dy))
    alpha = math.degrees(math.acos((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)))
    s = phi + bend * alpha
    mid = _add(root, _dir(side, s), l1)
    return s, _angle(side, (target[0] - mid[0], target[1] - mid[1])) - s


def body(p):
    """Joint positions for body params p (lean, tilt, knee, shrug, breath, hip_x; v3 "feet" = moved feet)."""
    hip = (HIP[0] + p.get("hip_x", 0.0), HIP[1] + p.get("knee", 0.0))
    feet = p.get("feet") or FEET
    knees = []
    for side, foot in ((-1, feet[0]), (1, feet[1])):
        half = max(math.dist(HIP, FEET[0]), math.dist(hip, foot) + 2) / 2
        s, e = _ik(foot, hip, half, half, -side, 1)  # knees bend outward; zero bend = the old straight legs
        knees.append(_add(foot, _dir(-side, s), half))
    lean, b = p.get("lean", 0.0), p.get("breath", 0.0)
    top = _add(hip, _rot((0, -(SPINE_UP + b)), lean))
    sh = _add(hip, _rot((0, -(SHOULDER_UP + b + p.get("shrug", 0.0))), lean))
    head = _add(top, _rot((0, -HEAD_UP), lean + p.get("tilt", 0.0)))
    return {"hip": hip, "knees": knees, "top": top, "sh": sh, "head": head, "feet": feet}


def arm_angles(spec, side, j, content=CONTENT):
    if spec == "aim":
        return min(max(_angle(1, content), 95), 135), -6.0, 0.0
    if spec[0] == "ik":
        _, ref, (dx, dy), bend = spec
        base = j["head"] if ref == "head" else j["sh"]
        s, e = _ik(j["sh"], (base[0] + dx, base[1] + dy), UPPER, FORE, side, bend)
        return s, e, 0.0
    return tuple(float(x) for x in spec)


def arm_points(j, side, ang):
    s, e, w = ang
    elbow = _add(j["sh"], _dir(side, s), UPPER)
    wrist = _add(elbow, _dir(side, s + e), FORE)
    return elbow, wrist, _add(wrist, _dir(side, s + e + w), PALM)


# ---------------------------------------------------------------- drawing

class _Pen:
    """ImageDraw in 1000-unit coordinates at scale k, offset by origin (in units)."""

    def __init__(self, im, k, origin=(0.0, 0.0)):
        self.d, self.k, self.o = ImageDraw.Draw(im), k, origin

    def p(self, x, y):
        return ((x - self.o[0]) * self.k, (y - self.o[1]) * self.k)

    def box(self, x0, y0, x1, y1):
        return [*self.p(x0, y0), *self.p(x1, y1)]

    def w(self, u):
        return max(1, int(round(u * self.k)))

    def line(self, a, b, w=LIMB):
        self.d.line([self.p(*a), self.p(*b)], fill=INK, width=self.w(w))
        for q in (a, b):
            self.d.ellipse(self.box(q[0] - w / 2, q[1] - w / 2, q[0] + w / 2, q[1] + w / 2), fill=INK)


def _head_base(pen, cx, cy):
    r = HEAD_R
    # Lumpy meatball silhouette: a circle perturbed by a few low-frequency bumps.
    pts = [pen.p(cx + (r + 7 * math.sin(5 * t) + 4 * math.sin(9 * t + 1)) * math.cos(t),
                 cy + (r + 7 * math.sin(5 * t) + 4 * math.sin(9 * t + 1)) * math.sin(t))
           for t in [i * 2 * math.pi / 180 for i in range(180)]]
    pen.d.polygon(pts, fill=MEAT, outline=INK, width=pen.w(14))
    for (x, y, s) in [(-70, -60, 16), (60, -85, 12), (85, 30, 18), (-95, 45, 13), (10, 95, 15), (-30, -110, 10)]:
        pen.d.ellipse(pen.box(cx + x - s, cy + y - s, cx + x + s, cy + y + s), fill=MEAT_DARK)
    pen.d.ellipse(pen.box(cx - 95, cy - 105, cx - 45, cy - 70), fill=SHINE)
    # Tomato-sauce cap with a parsley fleck: the brand detail.
    pen.d.chord(pen.box(cx - 120, cy - 175, cx + 120, cy - 40), 200, 340, fill=SAUCE, outline=INK, width=pen.w(10))
    pen.d.ellipse(pen.box(cx + 20, cy - 150, cx + 48, cy - 132), fill=PARSLEY, outline=INK, width=pen.w(4))


def _lid(pen, cx, cy, ex, half):
    if half:  # half-closed: the top half of the eye under a lid
        pen.d.chord(pen.box(cx + ex - 27, cy - 33, cx + ex + 27, cy + 23), 180, 360, fill=MEAT, outline=INK,
                    width=pen.w(6))
        pen.d.line([pen.p(cx + ex - 26, cy - 5), pen.p(cx + ex + 26, cy - 5)], fill=INK, width=pen.w(8))
    else:
        pen.d.ellipse(pen.box(cx + ex - 27, cy - 33, cx + ex + 27, cy + 23), fill=MEAT, outline=INK, width=pen.w(6))
        pen.d.line([pen.p(cx + ex - 24, cy - 4), pen.p(cx + ex + 24, cy - 4)], fill=INK, width=pen.w(8))


def _mouth(pen, cx, my, mouth, level):
    """Expression mouth; level 0 = its closed shape, 1-3 = small/mid/open while talking."""
    d, box = pen.d, pen.box
    if mouth == "talk" or (level and mouth not in ("o", "laugh")):
        lv = 3 if mouth == "talk" and not level else level
        hw, top, bot = [(24, 6, 12), (32, 14, 22), (38, 22, 30)][lv - 1]
        d.chord(box(cx - hw, my - top, cx + hw, my + bot), 0, 180, fill=INK)
    elif mouth == "smile":
        d.arc(box(cx - 45, my - 40, cx + 45, my + 20), 20, 160, fill=INK, width=pen.w(10))
    elif mouth == "o":
        s = 0.8 + 0.1 * level
        d.ellipse(box(cx - 22 * s, my + 4 - 26 * s, cx + 22 * s, my + 4 + 26 * s), fill=INK)
    elif mouth == "laugh":
        s = 0.85 + 0.08 * level
        d.chord(box(cx - 55, my - 30 * s, cx + 55, my + 45 * s), 0, 180, fill=INK)
        d.chord(box(cx - 30, my + 5 * s, cx + 30, my + 40 * s), 0, 180, fill=SAUCE)
    elif mouth == "wobble":
        pts = [pen.p(cx - 36 + 9 * k, my + 8 + (6 if k % 2 else -6)) for k in range(9)]
        d.line(pts, fill=INK, width=pen.w(8), joint="curve")
    elif mouth == "frown":
        d.arc(box(cx - 40, my, cx + 40, my + 50), 200, 340, fill=INK, width=pen.w(10))
    else:
        d.line([pen.p(cx - 32, my + 6), pen.p(cx + 32, my + 6)], fill=INK, width=pen.w(10))


def _face(pen, cx, cy, mouth, brow, look=(0, 0), level=0, blink=0, eyes=None):
    """Expressions SNAP between clean drawings (research/41-stickman-reference): eyes, one brow shape,
    one mouth. eyes: None (whites + pupils), "bliss" (closed arcs), "x" (defeated)."""
    d, box = pen.d, pen.box
    lx, ly = look  # pupil shift: toward the photo, at the viewer, or up while thinking
    for ex in (-48, 48):
        if eyes == "bliss":
            d.arc(box(cx + ex - 24, cy - 18, cx + ex + 24, cy + 22), 200, 340, fill=INK, width=pen.w(10))
        elif eyes == "x":
            for s_ in (-1, 1):
                d.line([pen.p(cx + ex - 18, cy - 22 * s_ - 5), pen.p(cx + ex + 18, cy + 22 * s_ - 5)], fill=INK,
                       width=pen.w(9))
        else:
            d.ellipse(box(cx + ex - 24, cy - 30, cx + ex + 24, cy + 20), fill=WHITE, outline=INK, width=pen.w(6))
            d.ellipse(box(cx + ex - 11 + lx, cy - 12 + ly, cx + ex + 11 + lx, cy + 10 + ly), fill=INK)
    if eyes:
        blink = 0
    if brow == "calm":  # short level dashes: he always has eyebrows now
        for ex in (-48, 48):
            d.line([pen.p(cx + ex - 20, cy - 46), pen.p(cx + ex + 20, cy - 48)], fill=INK, width=pen.w(8))
    elif brow == "cross":  # inner ends down: annoyed
        d.line([pen.p(cx - 72, cy - 54), pen.p(cx - 26, cy - 40)], fill=INK, width=pen.w(9))
        d.line([pen.p(cx + 26, cy - 40), pen.p(cx + 72, cy - 54)], fill=INK, width=pen.w(9))
    elif brow == "up":
        for ex in (-48, 48):
            d.arc(box(cx + ex - 28, cy - 62, cx + ex + 28, cy - 22), 200, 340, fill=INK, width=pen.w(9))
    elif brow == "lid":  # upper lids drawn down over half of each eye: the deadpan look
        for ex in (-48, 48):
            _lid(pen, cx, cy, ex, True)
    elif brow == "worry":  # inner ends raised, plus one sweat drop
        d.line([pen.p(cx - 76, cy - 40), pen.p(cx - 24, cy - 56)], fill=INK, width=pen.w(9))
        d.line([pen.p(cx + 24, cy - 56), pen.p(cx + 76, cy - 40)], fill=INK, width=pen.w(9))
        sx, sy = cx + 178, cy - 40
        d.polygon([pen.p(sx, sy - 58), pen.p(sx - 27, sy), pen.p(sx + 27, sy)], fill=DROP, outline=INK,
                  width=pen.w(6))
        d.ellipse(box(sx - 28, sy - 22, sx + 28, sy + 34), fill=DROP, outline=INK, width=pen.w(6))
        d.polygon([pen.p(sx, sy - 52), pen.p(sx - 21, sy - 4), pen.p(sx + 21, sy - 4)], fill=DROP)
    elif brow == "tilt":
        d.line([pen.p(cx - 76, cy - 44), pen.p(cx - 24, cy - 34)], fill=INK, width=pen.w(9))
        d.line([pen.p(cx + 22, cy - 50), pen.p(cx + 76, cy - 58)], fill=INK, width=pen.w(9))
    if blink:
        for ex in (-48, 48):
            _lid(pen, cx, cy, ex, blink == 1)
    _mouth(pen, cx, cy + 62, mouth, level)


_HEAD_CACHE = {}
HEAD_BOX = (-215, -235, 230, 165)  # head layer bounds around the head centre (cap, sweat drop, neck)


def _head_layer(k, mouth, brow, look, level, blink, eyes=None):
    if k not in _HEAD_CACHE:
        if len(_HEAD_CACHE) > 2:  # a push-in changes scale every frame: keep the cache small
            _HEAD_CACHE.clear()
        w, h = int((HEAD_BOX[2] - HEAD_BOX[0]) * k) + 2, int((HEAD_BOX[3] - HEAD_BOX[1]) * k) + 2
        base = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        _head_base(_Pen(base, k), -HEAD_BOX[0], -HEAD_BOX[1])
        _HEAD_CACHE[k] = base
    im = _HEAD_CACHE[k].copy()
    _face(_Pen(im, k), -HEAD_BOX[0], -HEAD_BOX[1], mouth, brow, look, level, blink, eyes)
    return im


def render(st, size, ss=2, origin=None, canvas=None):
    """One frame from a rig state. Without canvas: an RGBA image size x size (the 1000-unit drawing).
    With canvas=(W, H): the figure at scale size/1000 with unit (0, 0) at screen point origin, drawn only
    inside its clipped bounding box; returns (image, (x, y)) for pasting into a W x H frame, or None."""
    k = size / 1000.0
    j = body(st)
    hands = [arm_points(j, side, st[key])[2] for side, key in ((-1, "l"), (1, "r"))]
    hs = max(st.get("head_s", (1.0, 1.0)))  # v3 squash/stretch and puff can grow the head
    xs = [p[0] for p in hands + [j["sh"], j["hip"]] + list(j["feet"]) + j["knees"]] + [j["head"][0] - 240 * hs,
                                                                                      j["head"][0] + 240 * hs]
    ys = [p[1] for p in hands + list(j["feet"])] + [j["head"][1] - 250 * hs - 100 * (hs - 1), j["head"][1] + 170]
    box = [min(xs) - 40, min(ys) - 40, max(xs) + 40, max(ys) + 40]
    if canvas is None:
        origin, box_px = (0.0, 0.0), (0, 0, size, size)
    else:
        box_px = (max(0, int(origin[0] + box[0] * k)), max(0, int(origin[1] + box[1] * k)),
                  min(canvas[0], int(origin[0] + box[2] * k) + 1), min(canvas[1], int(origin[1] + box[3] * k) + 1))
        if box_px[2] <= box_px[0] or box_px[3] <= box_px[1]:
            return None
    kk = k * ss
    im = Image.new("RGBA", ((box_px[2] - box_px[0]) * ss, (box_px[3] - box_px[1]) * ss), (0, 0, 0, 0))
    pen = _Pen(im, kk, ((box_px[0] - origin[0]) / k, (box_px[1] - origin[1]) / k))
    pen.line(j["top"], j["hip"])                                   # spine
    for knee, foot in zip(j["knees"], j["feet"]):                  # legs
        pen.line(j["hip"], knee)
        pen.line(knee, foot)
    tilt = st.get("lean", 0.0) + st.get("tilt", 0.0)
    head = _head_layer(round(kk, 4), st["mouth"], st["brow"], st.get("look", (0, 0)), st.get("level", 0),
                       st.get("blink", 0), st.get("eyes"))
    pivot = (-HEAD_BOX[0] * kk, (-HEAD_BOX[1] + HEAD_UP) * kk)    # the spine top, in layer pixels
    sx, sy = st.get("head_s", (1.0, 1.0))
    if abs(sx - 1) > 0.01 or abs(sy - 1) > 0.01:  # v3: squash/stretch about the neck (hits, stings)
        head = head.resize((max(1, int(head.width * sx)), max(1, int(head.height * sy))), Image.BICUBIC)
        pivot = (pivot[0] * sx, pivot[1] * sy)
    if abs(tilt) > 0.05:
        head = head.rotate(-tilt, resample=Image.BICUBIC, center=pivot)
    top = pen.p(*j["top"])
    im.alpha_composite(head, (int(round(top[0] - pivot[0])), int(round(top[1] - pivot[1]))))
    # Arms go on top of the head so hand-to-face poses (shock, facepalm, think) stay visible.
    for side, key in ((-1, "l"), (1, "r")):
        elbow, wrist, hand = arm_points(j, side, st[key])
        pen.line(j["sh"], elbow)
        pen.line(elbow, wrist)
        pen.line(wrist, hand)
        pen.d.ellipse(pen.box(hand[0] - HAND_R, hand[1] - HAND_R, hand[0] + HAND_R, hand[1] + HAND_R), fill=INK)
    im = im.reduce(ss) if ss > 1 else im
    return im if canvas is None else (im, box_px[:2])


def pose_state(pose, j=None, content=CONTENT):
    p = POSES[pose]
    st = {key: float(p.get(key, 0.0)) for key in ("lean", "tilt", "knee", "shrug")}
    j = j or body(st)
    st["l"], st["r"] = arm_angles(p["l"], -1, j, content), arm_angles(p["r"], 1, j, content)
    st["mouth"], st["brow"], st["eyes"] = p["mouth"], p["brow"], p.get("eyes")
    return st


def draw(pose="neutral", size=600, mouth=None, blink=False, arms=None, look=(0, 0), eyes=None):
    """A still Meatball. mouth/blink override the pose's face; arms = {"l"/"r": (dx, dy)} moves a hand
    (the elbow follows by IK); look shifts the pupils (thumbnails aim his gaze at the animal)."""
    st = pose_state(pose)
    if mouth:
        st["mouth"] = mouth
    st["blink"], st["look"] = (2 if blink else 0), look
    if eyes:
        st["eyes"] = eyes
    if arms:
        j = body(st)
        for side, key in ((-1, "l"), (1, "r")):
            if key in arms:
                _, _, hand = arm_points(j, side, st[key])
                tgt = (hand[0] + arms[key][0], hand[1] + arms[key][1])
                s, e = _ik(j["sh"], tgt, UPPER, FORE + PALM, side, -1 if tgt[1] < j["sh"][1] else 1)
                st[key] = (s, e, 0.0)
    return render(st, size)


# ---------------------------------------------------------------- motion

def ease_inout(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def ease_back(u, c=0.6):
    """Ease in-out with a small anticipation dip at the start and a small overshoot before settling."""
    u = min(max(u, 0.0), 1.0)
    c2 = c * 1.525
    if u < 0.5:
        return ((2 * u) ** 2 * ((c2 + 1) * 2 * u - c2)) / 2
    return ((2 * u - 2) ** 2 * ((c2 + 1) * (u * 2 - 2) + c2) + 2) / 2


def _syllables(word):
    w = word.lower().strip(".,!?'\"")
    groups, prev = 0, False
    for ch in w:
        v = ch in "aeiouy"
        groups += v and not prev
        prev = v
    if w.endswith("e") and groups > 1 and not w.endswith(("le", "ee")):
        groups -= 1
    return max(1, min(groups, 5))


def emphasis(words):
    """(time, score) of stressed words: capitalised mid-sentence or ALL CAPS, stress words, numbers, and
    words right before a pause (punctuation). Function words never count."""
    out = []
    for i, (s, e, w) in enumerate(words):
        raw = w.strip(".,!?\"")
        low = raw.lower()
        gap_after = (words[i + 1][0] - e) if i + 1 < len(words) else 9.0
        gap_before = (s - words[i - 1][1]) if i else 9.0
        score = 0.0
        if len(raw) > 1 and raw.isupper():
            score += 3
        elif raw[:1].isupper() and raw != "I" and gap_before < 0.2:
            score += 1.5  # a capital mid-sentence: a name or a stressed word
        if low in STRESS:
            score += 1.5
        if any(c.isdigit() for c in raw):
            score += 1.5
        if gap_after > 0.18 and len(low) > 3:
            score += 1.5  # the word before punctuation carries the stress
        if len(low) >= 8:
            score += 0.8
        if i == 0 and low in ("true", "false"):
            score += 2
        if len(low) <= 2 and not raw.isupper():
            score = 0.0
        if score >= 1.5:
            out.append((s, score))
    return out


def _space(cands, gap, lo, hi):
    picked = []
    for t, sc in sorted(cands, key=lambda c: (-c[1], c[0])):
        if lo <= t <= hi and all(abs(t - p) >= gap for p in picked):
            picked.append(t)
    return sorted(picked)


def plan(pose, words, dur, fps=30, seed=0, enter=True, exit=True):
    """Acting plan for one line: keypose events [(start, pose, frames)], accents and gaze overrides.
    The beat's pose is the primary choice; extra gestures only on emphasis words, at most one per 1.5 s,
    each held at least ~1 s, settling to a relaxed idle in pauses and at the end of the line."""
    rng = random.Random(f"{pose}|{seed}|{len(words)}")
    pose = pose if pose in POSES else "point"
    T = max(5, min(7, round(0.23 * fps)))       # 7 frames per gesture, 8 to enter or settle (at 30 fps)
    lead = (T * 0.6) / fps                      # start early so the pose lands on the stressed syllable
    start_pose = "neutral" if enter else pose
    ev = [(-9.0, start_pose, T)]
    speech0 = words[0][0] if words else 0.0
    speech1 = words[-1][1] if words else 0.0
    end = dur - (T + 4) / fps                   # last moment a settle can start and still finish
    if enter and pose != "neutral":
        ev.append((max(0.1, speech0 - lead), pose, T + 1))
    emph = emphasis(words)
    accents = []
    if pose in PERSONA:
        accents = _space(emph, 1.2, speech0 + 0.6, speech1)
    else:
        first = ev[-1][0] if len(ev) > 1 else 0.0
        hits = _space(emph, 1.5, first + 1.5, speech1 - 0.6)
        cur, k = pose, 0
        hold_to = first + TRANSIENT.get(pose, 99)
        for t in hits:
            if t - lead > hold_to:  # a reaction pose has had its moment: move on before the next hit
                ev.append((hold_to, AFTER[pose], T + 1))
                cur, hold_to = AFTER[pose], 99
            k += 1
            pal = SECONDARY.get(pose, ["present"])
            nxt = pose if (k % 2 == 0 and pose not in TRANSIENT) else pal[rng.randrange(len(pal))]
            nxt = AFTER.get(pose, "present") if nxt == cur else nxt
            ev.append((t - lead, nxt, T))
            cur = nxt
            hold_to = 99
        if pose in TRANSIENT and hold_to < 99 and hold_to < speech1:
            ev.append((hold_to, AFTER[pose], T + 1))
        # Long stretches with no stressed word: relax after a couple of seconds instead of freezing.
        filled = []
        for a, b in zip(ev[1:], ev[2:] + [(speech1 + 0.15, None, T)]):
            filled.append(a)
            if a[1] != "neutral" and b[0] - a[0] > 3.0:
                filled.append((a[0] + 2.2, "neutral", T + 1))
        ev = ev[:1] + filled
    kept = ev[:2]
    for e in ev[2:]:  # every pose is held at least ~1 s before the next one starts
        if e[0] - kept[-1][0] >= 1.0:
            kept.append(e)
    ev = kept
    if exit:
        settle = min(max(speech1 + 0.12, (ev[-1][0] + 0.9) if len(ev) > 1 else 0), end)
        if ev[-1][1] != "neutral":
            ev.append((max(settle, ev[-1][0] + 0.3), "neutral", T + 1))
    looks = [(s, e) for s, e, w in words if w.lower().strip(".,!?") in YOU]
    return {"events": ev, "accents": accents, "looks": looks, "T": T}


def _mix(t, events, ease, fps, lag=0.0):
    """Blend weights of the keyposes at time t: each event eases from whatever was showing into its pose."""
    m = {events[0][1]: 1.0}
    for t0, pose, frames in events[1:]:
        if t < t0 + lag:
            break
        w = ease((t - t0 - lag) / (frames / fps + lag))
        m = {k: v * (1 - w) for k, v in m.items()}
        m[pose] = m.get(pose, 0.0) + w
    return m


def _bump(t, at, width):
    u = (t - at) / width
    return math.sin(math.pi * u) ** 2 if 0 <= u <= 1 else 0.0


def mouth_track(words, n, fps):
    """Mouth opening level (0-3) per frame from word timings: each syllable opens then closes; the
    level moves at most one step per frame, so it eases and never flickers."""
    target = [0] * n
    for s, e, w in words:
        syl = _syllables(w)
        span = max(e - s, 0.06)
        vowels = [c for c in w.lower() if c in "aeiouy"] or ["e"]
        for k in range(syl):
            a, b = s + span * k / syl, s + span * (k + 1) / syl
            v = vowels[min(k, len(vowels) - 1)]
            lv = 3 if v in "ao" else 2 if v in "eu" else 1
            if len(w) <= 2:
                lv = min(lv, 2)
            for f in range(int(a * fps), min(n, int(math.ceil((a + (b - a) * 0.7) * fps)))):
                target[f] = max(target[f], lv)
    out, cur = [0] * n, 0
    for f in range(n):
        cur += (target[f] > cur) - (target[f] < cur)
        out[f] = cur
    return out


def states(pose, words, dur, fps, seed=0, enter=True, exit=True, content=CONTENT, size=600):
    """Every frame's rig state for one line (deterministic for a seed)."""
    pose = pose if pose in POSES else "point"
    pl = plan(pose, words, dur, fps, seed, enter, exit)
    ev, n = pl["events"], max(1, int(dur * fps))
    rng = random.Random(f"blink|{seed}|{pose}")
    blinks, t = [], 0.9 + rng.uniform(0, 1.6)
    while t < dur - 0.4:
        blinks.append(t)
        t += rng.uniform(2.5, 5.0)
    mouth = mouth_track(words, n, fps)
    cycles = round(dur / 3.5)
    amp = 1.6 * 1000.0 / size                    # breathing: 1.6 output pixels, whatever his size
    norm = math.hypot(*content)
    cdir = (content[0] / norm, content[1] / norm)
    gaze_of = {"viewer": (0.0, 0.0), "content": (9 * cdir[0], 9 * cdir[1]), "up": (7.0, -9.0)}
    out = []
    for f in range(n):
        t = f / fps
        last = exit and f >= n - 2               # loop seam: the last frames are exactly the rest state
        am = _mix(t, ev, ease_back, fps)
        bm = _mix(t, ev, ease_inout, fps, lag=2.0 / fps)  # torso and head follow the hands a beat later
        st = {}
        for key in ("lean", "tilt", "knee", "shrug"):
            st[key] = sum(w * POSES[p].get(key, 0.0) for p, w in bm.items())
        st["breath"] = 0.0 if (cycles < 1 or last) else amp * (1 - math.cos(2 * math.pi * cycles * t / dur)) / 2
        st["pop"] = 1.0
        for t0, p, _ in ev[1:]:
            if p in BIG:  # anticipation: a quick crouch as the big move starts
                st["knee"] += 9 * _bump(t, t0 - 0.06, 0.3)
            if p in REALIZE:  # realization: a quick scale-pop as the pose lands
                st["pop"] += 0.07 * _bump(t, t0 + 0.12, 0.3)
        if not last:
            acc = sum(_bump(t, a - 0.05, 0.4) for a in pl["accents"])
            st["tilt"] += 1.4 * acc if pose != "nervous" else 0.0
            laugh = am.get("laugh", 0.0)
            if laugh > 0 and any(s <= t <= e for s, e, _ in words):
                st["shrug"] += laugh * 2.0 * abs(math.sin(2 * math.pi * 4 * t))
        j = body(st)
        for side, key in ((-1, "l"), (1, "r")):
            ang = [0.0, 0.0, 0.0]
            for p, w in am.items():
                spec = POSES[p][key]
                if p == "nervous" and spec[0] == "ik":  # fidget: clasped hands rub slowly
                    spec = ("ik", spec[1], (spec[2][0] + 3 * math.sin(2 * math.pi * 1.1 * t), spec[2][1]), spec[3])
                a = arm_angles(spec, side, j, content)
                ang = [x + w * y for x, y in zip(ang, a)]
            if key == "r" and not last:
                ang[1] += 16 * am.get("wave", 0.0) * math.sin(2 * math.pi * 2.2 * t)
            ang[0] += 0.9 * st["breath"] / amp if amp else 0.0
            st[key] = tuple(ang)
        dom = max(am, key=am.get)
        face = pose if pose in PERSONA else dom
        st["mouth"], st["brow"], st["eyes"] = POSES[face]["mouth"], POSES[face]["brow"], POSES[face].get("eyes")
        if st["mouth"] == "talk":
            st["mouth"] = "smile"
        gx = sum(w * gaze_of[POSES[p]["gaze"]][0] for p, w in bm.items())
        gy = sum(w * gaze_of[POSES[p]["gaze"]][1] for p, w in bm.items())
        you = max([_ramp(t, s, e) for s, e in pl["looks"]] + [0.0])
        st["look"] = (round(gx * (1 - you)), round(gy * (1 - you)))
        st["level"] = 0 if last else mouth[f]
        st["blink"] = 0
        for b in blinks:
            k = int((t - b) * fps)
            if 0 <= k < 3:
                st["blink"] = (1, 2, 1)[k]
        if last:
            st["look"] = (0, 0) if pose not in ("think",) else st["look"]
        out.append(st)
    return out


def _ramp(t, s, e, r=0.12):
    if t < s - r or t > e + 0.3 + r:
        return 0.0
    return min(1.0, (t - (s - r)) / r, ((e + 0.3 + r) - t) / r)


def _sticker(im, size, shadow, glow=None):
    """White rim (and optional soft drop shadow, optional emotion glow = (rgb, strength)) around the
    figure, as one RGBA image the same size."""
    import numpy as np
    import cv2
    r = max(13, int(size / 66)) | 1  # the old 13 px rim at the usual size; thicker when he is big
    a = np.asarray(im.split()[3])
    halo = cv2.dilate(a, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (r, r)))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    if glow and glow[1] > 0.01:  # emotion glow: yellow = warning, red = danger, green = good
        g = cv2.dilate(a, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (r * 3 | 1, r * 3 | 1)))
        g = cv2.GaussianBlur(g, (0, 0), max(6.0, size / 45.0)).astype(np.float32)
        g = np.clip(g * 1.6 * glow[1], 0, 255).astype(np.uint8)
        col = Image.new("RGBA", im.size, glow[0] + (255,))
        col.putalpha(Image.fromarray(g))
        out.alpha_composite(col)
    if shadow:  # soft drop shadow so he reads on a busy full-frame photo
        sh = cv2.GaussianBlur(halo, (0, 0), max(4.0, size / 90.0))
        dx, dy = size // 110, size // 70
        sh = np.roll(np.roll(sh, dy, axis=0), dx, axis=1)
        shade = Image.new("RGBA", im.size, (0, 0, 0, 255))
        shade.putalpha(Image.fromarray((sh.astype(np.float32) * 0.45).astype(np.uint8)))
        out.alpha_composite(shade)
    rim = Image.new("RGBA", im.size, WHITE)
    rim.putalpha(Image.fromarray(halo))
    out.alpha_composite(rim)
    out.alpha_composite(im)
    return out


def _frame(job):
    st, size, pad, path, shadow, place, glow = job
    if place is None:  # classic: a square sprite with 25% padding, positioned by the caller
        im = render(st, size)
        canvas = Image.new("RGBA", (size + 2 * pad, size + 2 * pad), (0, 0, 0, 0))
        canvas.alpha_composite(_sticker(im, size, shadow, glow), (pad, pad))
    else:  # placed in the video frame (shot layouts, push-ins)
        cw, origin, k_size, margin = place
        pop = st.get("pop", 1.0)  # scale-pop about the hips
        origin = (origin[0] + 500 * k_size / 1000 * (1 - pop), origin[1] + 790 * k_size / 1000 * (1 - pop))
        k_size *= pop
        canvas = Image.new("RGBA", cw, (0, 0, 0, 0))
        ss = 2 if k_size <= 1400 else 1
        got = render(st, k_size, ss, origin, cw)
        if got:
            im, (x, y) = got
            pad_im = Image.new("RGBA", (im.width + 2 * margin, im.height + 2 * margin), (0, 0, 0, 0))
            pad_im.alpha_composite(im, (margin, margin))
            canvas.alpha_composite(_sticker(pad_im, k_size, shadow, glow), (x - margin, y - margin))
    canvas.save(path, compress_level=1)


def place(layout, f, fps):
    """Screen placement for frame f from a layout schedule: [{"t": sec, "size": px per 1000 units,
    "pos": screen point of unit (0, 0), "push": zoom per frame, "anchor": unit point held still while
    pushing in, "shadow": bool}]. Returns (origin, size, shadow)."""
    cur = layout[0]
    for lay in layout:
        if lay.get("t", 0) * fps <= f:
            cur = lay
    f0 = int(round(cur.get("t", 0) * fps))
    size = cur["size"] * (1 + cur.get("push", 0.0) * (f - f0))
    ax, ay = cur.get("anchor", (500, 360))
    ox = cur["pos"][0] + ax * cur["size"] / 1000 - ax * size / 1000
    oy = cur["pos"][1] + ay * cur["size"] / 1000 - ay * size / 1000
    return (ox, oy), size, cur.get("shadow", False)


def animate(pose, size, words, dur, fps, outdir, seed=0, pop=True, enter=True, exit=True, content=CONTENT,
            shadow=False, canvas=None, layout=None, glow=None):
    """PNG frames of Meatball acting a line (outdir/0000.png ...). enter/exit start and end the line on
    the relaxed rest pose, so consecutive lines and the Short loop seam never jump; pass False to carry a
    pose across segments (the quiz countdown). content = direction of the panel he points and looks at.
    Default output: square sprites (size + 50% padding) for the caller to overlay. With canvas=(W, H) and
    a layout schedule (see place()), each frame is the full W x H transparent frame with Meatball placed,
    sized and pushed in per shot, so one continuous performance can cut between shot sizes.
    glow = "yellow" | "red" | "green" adds a soft emotion halo that fades in and out with the line.
    pop is kept for old callers and unused. Returns frame count."""
    os.makedirs(outdir, exist_ok=True)
    pad = int(size * 0.25)
    sts = states(pose, words, dur, fps, seed, enter, exit, content, size)
    jobs, col, n = [], GLOWS.get(glow) if isinstance(glow, str) else glow, len(sts)
    fade = max(1, int(0.25 * fps))
    for f, st in enumerate(sts):
        g = (col, min(1.0, (f + 1) / fade if enter else 1.0, (n - f) / fade if exit else 1.0)) if col else None
        if canvas and layout:
            origin, k_size, sh = place(layout, f, fps)
            margin = max(13, int(k_size / 66)) * (6 if col else 1) + 2
            jobs.append((st, size, pad, f"{outdir}/{f:04d}.png", sh, (tuple(canvas), origin, k_size, margin), g))
        else:
            jobs.append((st, size, pad, f"{outdir}/{f:04d}.png", shadow, None, g))
    n_proc = int(os.environ.get("MEATBALL_JOBS", "2"))
    if n_proc > 1 and len(jobs) > 20:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(n_proc) as pool:
            pool.map(_frame, jobs, chunksize=8)
    else:
        for j in jobs:
            _frame(j)
    return len(jobs)


# ---------------------------------------------------------------- v3 action moves (research/44)
# Shorts v3 puts Meatball in jeopardy: things happen TO him. An action move is a per-frame body transform
# laid over the talking rig (lip-sync, face, blinks stay): where his hip is on screen, a rotation, a body
# squash, a head squash/puff, running legs, a tremble, and face overrides (X eyes when hit).
ACTS = ("stand", "run_in", "run_off", "run_across", "launch", "tumble", "shake", "peek", "hide", "hit", "puff",
        "puffed", "deflate", "loop_out")
JITTER = {"shake": 9.0, "peek": 4.0, "hide": 8.0, "puff": 6.0, "puffed": 6.0}  # tremble amplitude, drawing units


def _clamp01(u):
    return min(max(u, 0.0), 1.0)


def _squash(f):
    """Impact squash and stretch over frames since the hit: flat, tall, settle (sx, sy)."""
    seq = [(1.32, 0.68), (1.28, 0.72), (0.86, 1.18), (0.9, 1.14), (1.06, 0.95), (1.03, 0.98)]
    return seq[f] if 0 <= f < len(seq) else (1.0, 1.0)


def act_track(act, n, fps, t_act=0.25, home=0.5, seed=0):
    """Per-frame transform of an action move for a line of n frames. t_act = the impact / start moment (s).
    Each entry: x (hip position as a fraction of frame width; <0 or >1 is off-screen), y (drawing units,
    + = down), rot (degrees, + = clockwise), body (sx, sy), head (sx, sy), run (stride phase or None),
    flip (faces left), eyes / pose overrides, jitter (tremble amplitude)."""
    rng = random.Random(f"act|{act}|{seed}")
    ph = rng.uniform(0, 6.28)
    fa = int(round(t_act * fps))
    out = []
    for f in range(n):
        t = f / fps
        e = dict(x=home, y=0.0, rot=0.0, body=(1.0, 1.0), head=(1.0, 1.0), run=None, flip=False, eyes=None,
                 pose=None, jitter=JITTER.get(act, 0.0), hidden=False)
        if act == "run_in":  # sprint in from the left, skid to a stop on his mark
            u = _clamp01(t / 0.55)
            e["x"] = -0.45 + (home + 0.45) * (1 - (1 - u) ** 2)
            if u < 1:
                e["run"], e["rot"] = 2 * math.pi * 3.6 * t, 9.0 * (1 - u)
            elif f - int(0.55 * fps) < 6:
                e["body"] = _squash(f - int(0.55 * fps) + 2)
        elif act == "run_off":  # stand, then bolt off to the right
            if f >= fa:
                u = _clamp01((t - t_act) / 0.5)
                e["x"] = home + 1.05 * u * u
                e["run"], e["rot"] = 2 * math.pi * 4.2 * (t - t_act), 10.0
                e["pose"], e["eyes"] = "shock", None
            if e["x"] > 1.45:
                e["hidden"] = True
        elif act == "run_across":  # panic sprint left to right across the whole line
            e["x"] = -0.4 + 1.8 * t / max(n / fps, 0.1)
            e["run"], e["rot"], e["pose"] = 2 * math.pi * 4.0 * t, 10.0, "shock"
        elif act == "launch":  # kicked: squash, then flung up and out with a spinning arc
            if f >= fa:
                k = f - fa
                u = (t - t_act) / 0.75
                if k < 2:
                    e["body"], e["head"] = _squash(k), (1.3, 0.72)
                else:
                    e["x"] = home + 0.95 * u
                    e["y"] = -2600 * u + 900 * u * u
                    e["rot"] = 760 * u
                e["eyes"], e["pose"] = "x", "shock"
                if u > 1.05:
                    e["hidden"] = True
        elif act == "tumble":  # falls in spinning from above, lands with a squash, dazed
            if f < fa:
                u = f / max(fa, 1)
                e["x"] = home + 0.22 * (1 - u)
                e["y"] = -2200 * (1 - u) ** 2
                e["rot"] = -540 * (1 - u)
                e["pose"] = "shock"
            else:
                k = f - fa
                e["body"] = _squash(k)
                e["head"] = (1.0 + 0.6 * (e["body"][0] - 1), 1.0 + 0.6 * (e["body"][1] - 1))
                if k < int(0.6 * fps):
                    e["eyes"], e["rot"] = "x", 6 * math.sin(2 * math.pi * 3 * (t - t_act)) * math.exp(-3 * (t - t_act))
        elif act == "peek":  # leans in from the right edge, trembling
            u = _clamp01(t / 0.25)
            e["x"] = 1.4 - 0.5 * ease_inout(u)
            e["rot"], e["pose"] = -16.0, "nervous"
        elif act == "loop_out":  # the loop tail: peek, then slide back out so the last frame = frame 0
            T = n / fps
            u = _clamp01((T - t) / 0.3)
            e["x"] = 1.4 - 0.5 * ease_inout(u)
            e["rot"], e["pose"] = -16.0, "nervous"
            if f >= n - 1:
                e["hidden"] = True
        elif act == "hide":  # cowering low at the left edge, trembling
            e["x"], e["y"], e["rot"], e["pose"] = 0.14, 120.0, 8.0, "nervous"
        elif act == "hit":  # hit reaction: head squash and stretch, knocked back, X eyes
            if f >= fa:
                k = f - fa
                e["head"] = _squash(k)
                e["x"] = home - 0.07 * math.exp(-(t - t_act) * 5) * min(1.0, k / 2 + 0.5)
                e["rot"] = -12 * math.exp(-(t - t_act) * 4)
                if t - t_act < 0.7:
                    e["eyes"], e["pose"] = "x", "shock"
        elif act == "puff":  # stung: the head swells and stays swollen, trembling
            if f >= fa:
                k = f - fa
                g = [1.15, 1.35, 1.55, 1.62, 1.55, 1.5][k] if k < 6 else 1.5
                e["head"], e["pose"] = (g, g), "shock"
            else:
                e["jitter"] = 0.0
        elif act == "puffed":  # still swollen from the last line
            e["head"], e["pose"] = (1.5, 1.5), "shock"
        elif act == "deflate":  # swollen until t_act, then shrinks back with a wobble
            if f < fa:
                e["head"], e["pose"], e["jitter"] = (1.5, 1.5), "shock", 6.0
            else:
                k = f - fa
                g = [1.3, 1.05, 0.88, 0.95, 1.04, 1.0][k] if k < 6 else 1.0
                e["head"] = (g, 2 - g if k < 6 else 1.0)
        elif act == "shake":
            e["pose"] = "nervous"
        if e["jitter"] and not e["hidden"]:
            e["jx"] = e["jitter"] * math.sin(2 * math.pi * 17 * t + ph)
            e["jy"] = 0.4 * e["jitter"] * math.sin(2 * math.pi * 23 * t + 2 * ph)
            e["rot"] += 0.25 * e["jitter"] * math.sin(2 * math.pi * 13 * t + ph)
        out.append(e)
    return out


def apply_run(st, phase):
    """Scissor stride on a rig state: feet swing and lift, hips bob, arms swing opposite, lean forward."""
    s = math.sin(phase)
    lf = (FEET[0][0] + 85 * s, FEET[0][1] - 55 * max(0.0, math.cos(phase)))
    rf = (FEET[1][0] - 85 * s, FEET[1][1] - 55 * max(0.0, -math.cos(phase)))
    st = dict(st, feet=(lf, rf), knee=st.get("knee", 0.0) + 22 + 10 * abs(s), lean=st.get("lean", 0.0) + 9)
    st["l"] = (38 - 50 * s, -60.0, 0.0)
    st["r"] = (38 + 50 * s, -60.0, 0.0)
    return st


def prop(name, height):
    """A still prop that stands beside Meatball (RGBA, `height` px tall). The fork is the show's silent
    running gag: it turns up, upright and unexplained, whenever a line is about eating (research/39)."""
    im = Image.new("RGBA", (300, 1000), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if name == "fork":
        steel, hi = (196, 200, 206, 255), (236, 238, 242, 255)
        d.rounded_rectangle([118, 430, 182, 980], 30, fill=steel, outline=INK, width=12)       # handle
        d.polygon([(70, 300), (230, 300), (190, 450), (110, 450)], fill=steel, outline=INK)     # neck
        d.line([(70, 300), (110, 450), (190, 450), (230, 300)], fill=INK, width=12)
        for x in (70, 123, 177, 230):                                                          # tines
            d.rounded_rectangle([x - 16, 40, x + 16, 320], 16, fill=steel, outline=INK, width=10)
        d.rounded_rectangle([136, 500, 152, 900], 8, fill=hi)                                  # shine
    else:
        raise ValueError(f"unknown prop {name}")
    return im.resize((int(300 * height / 1000), height), Image.LANCZOS)


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    sheet = Image.new("RGBA", (300 * len(POSES), 340), (255, 255, 255, 255))
    for i, name in enumerate(POSES):
        im = draw(name, 300)
        im.save(f"{out}/{name}.png")
        sheet.alpha_composite(im, (300 * i, 0))
        ImageDraw.Draw(sheet).text((300 * i + 120, 310), name, fill=INK)
    sheet.convert("RGB").save(f"{out}/sheet.png")
    print("ok", out)
