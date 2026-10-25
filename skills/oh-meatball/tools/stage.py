#!/usr/bin/env python3
"""Shorts v4 staging (research/45). Two jobs:
  1. Meatball's mark and facing: on cut-out shots he keeps his left-hand mark (v3.HOME_V4); on a v3 still
     (the animal can't move) place() keeps him off its head (a pinned head box) unless the beat is a contact.
  2. frame_fit(): re-frame a cut-out shot around the whole animal, as large as fits, with room for its moves,
     in the free space beside (or above) him, above the captions and inside the frame.
track() re-aims mascot.act_track so he faces the animal and flees, peeks and cowers on the far side.
Boxes are screen pixels (1080x1920).
"""
import math

from PIL import Image

W, H = 1080, 1920
FLOOR = 1430
Z_RANGE = (1.0, 1.14)
# Meatball's body box around his hip mark, in drawing units at size 1000 (hat to feet, arms in)
MB_HALF_W, MB_TOP = 255, 860
_SIZES = {}


def crop_size(path, crop):
    if path not in _SIZES:
        _SIZES[path] = Image.open(path).size
    w, h = _SIZES[path]
    c = crop or [0, 0, 1, 1]
    return (c[2] - c[0]) * w, (c[3] - c[1]) * h


def to_screen(path, crop, box, z, R=1.15):
    """Crop-fraction box -> screen box at zoom z (the v3 base: cover W*R x H*R, centre-crop, view())."""
    cw, ch = crop_size(path, crop)
    bw, bh = int(W * R), int(H * R)
    s = max(bw / cw, bh / ch)
    l, t = (int(cw * s) + 1 - bw) // 2, (int(ch * s) + 1 - bh) // 2
    k = (W / bw) * z
    f = lambda fx, fy: (k * (fx * cw * s - l - bw / 2) + W / 2, k * (fy * ch * s - t - bh / 2) + H / 2)
    x0, y0 = f(box[0], box[1])
    x1, y1 = f(box[2], box[3])
    return [x0, y0, x1, y1]


def union(boxes):
    boxes = [b for b in boxes if b]
    if not boxes:
        return None
    return [min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes)]


def clip(b):
    if not b:
        return None
    b = [max(0, b[0]), max(0, b[1]), min(W, b[2]), min(H, b[3])]
    return b if b[2] > b[0] and b[3] > b[1] else None


def area(b):
    return 0.0 if not b else max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])


def inter(a, b):
    if not a or not b:
        return 0.0
    return area([max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])]) if (
        min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1])) else 0.0


def mb_box(x, size):
    k = size / 1000.0
    return [x * W - MB_HALF_W * k, FLOOR - MB_TOP * k, x * W + MB_HALF_W * k, FLOOR]


def shot_boxes(sh):
    """(head box, body box, body centre x) on screen for a shot with subject info, else Nones."""
    info = sh.get("subj")
    if not info or "head" not in info:
        return None, None, None
    head = clip(union([to_screen(sh["path"], sh["crop"], info["head"], z) for z in Z_RANGE]))
    body = clip(union([to_screen(sh["path"], sh["crop"], info["box"], z) for z in Z_RANGE]))
    cx = to_screen(sh["path"], sh["crop"], [info["cx"], info["cy"], info["cx"], info["cy"]], 1.0)[0]
    return head, body, cx


def place(shots, n, contact=False, home=0.24, size=1000):
    """Meatball's mark over v3 stills (the animal can't move there): (x, size, side, head overlap), clear of
    the animal's head (a pinned head box) unless the beat is a contact. side = +1 when the animal is to his
    right. Shots are weighted by screen time; host (blurred) shots don't count. Without facts: the v3 mark."""
    facts = [(shot_boxes(s), max(1, s["f1"] - s["f0"])) for s in shots]
    facts = [(f, w) for (f, w), s in zip(facts, shots) if f[0] is not None and not s.get("blur")]
    if not facts:
        return home, size, 1, None
    tot = sum(w for _, w in facts)
    cx = sum(f[2] * w for f, w in facts) / tot
    heads = union([f[0] for f, _ in facts])
    best = None
    for k in (1.0, 0.9, 0.8):
        sz = int(size * k)
        lo = MB_HALF_W * sz / 1000 / W + 0.02   # keep his whole body on screen
        for i in range(31):
            x = lo + (1 - 2 * lo) * i / 30
            mb = mb_box(x, sz)
            head_ov = sum(w * inter(mb, f[0]) / max(1.0, area(f[0])) for f, w in facts) / tot
            body_ov = sum(w * inter(mb, f[1]) / area(mb) for f, w in facts) / tot
            if contact:  # touch the head from the free side: overlap it by about a fifth of his width
                d = 0.2 * (mb[2] - mb[0])
                cost = min(abs(mb[2] - (heads[0] + d)), abs(mb[0] - (heads[2] - d))) / W + 0.4 * (1 - k)
            else:
                cost = 12 * head_ov + 1.2 * body_ov + 1.5 * (1 - k) + 0.15 * abs(x - home)
            if best is None or cost < best[0]:
                best = (cost, x, sz, head_ov)
    _, x, sz, head_ov = best
    return x, sz, (1 if cx >= x * W else -1), head_ov


# ---------------------------------------------------------------- fitting a cut-out (v4)

SAFE = (0.03 * W, 130.0, 0.97 * W, 1465.0)   # the animal stays inside this: clear of the Shorts UI and captions
GAP = 40.0   # clear air between Meatball (who leans and trembles) and the animal
REACH = {"lunge": (0.12, 1.18), "strike": (0.09, 1.10)}   # forward reach (frame widths), peak scale


LEAN = {"peek": 0.17, "loop_out": 0.17}   # acts that lean his head toward the animal (frame widths at size 1000)


def regions(x, size, side, top=SAFE[1], contact=False, act=None):
    """Free screen rectangles for the animal around Meatball's mark: beside him (on the animal's side) and
    above him. A contact beat lets the animal's box reach a quarter of the way into his."""
    mb = mb_box(x, size)
    reach = 0.25 * (mb[2] - mb[0]) if contact else -GAP - LEAN.get(act, 0.0) * W * size / 1000
    beside = [mb[2] - reach, top, SAFE[2], SAFE[3]] if side == 1 else [SAFE[0], top, mb[0] + reach, SAFE[3]]
    above = [SAFE[0], top, SAFE[2], mb[1] - GAP]
    return [r for r in (beside, above) if r[2] - r[0] > 60 and r[3] - r[1] > 60]


def envelope(box, moves, idle, toward, contact):
    """The screen box an animal can occupy during its moves: peak scale about its feet, drift, and (unless
    the beat is a contact) its forward reach toward Meatball."""
    names = [m for m, _ in moves]
    sc = max([REACH[m][1] for m in names if m in REACH] + [1.02])
    fwd = 0.0 if contact else max([REACH[m][0] for m in names if m in REACH] + [0.0]) * W
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    e = [cx + sc * (x0 - cx), y1 + sc * (y0 - y1), cx + sc * (x1 - cx), y1]
    if idle == "drift":
        e = [e[0] - 0.02 * W, e[1] - 0.05 * W, e[2] + 0.02 * W, e[3] + 0.012 * W]
    else:
        e = [e[0] - 4, e[1] - 0.012 * W, e[2] + 4, e[3] + 4]
    if fwd:
        back = 0.045 * W   # the wind-up leans back before the snap
        e = ([e[0] - fwd, e[1] - 0.03 * W, e[2] + back, e[3]] if toward == -1 else
             [e[0] - back, e[1] - 0.03 * W, e[2] + fwd, e[3]])
    return e


def frame_fit(box, moves, idle, side, contact, rects, gmax=1.0):
    """Re-frame a cut-out shot around the whole animal. box = the animal in photo px. Returns
    dict(g, tx, ty): screen = (tx, ty) + g * photo px, the largest scale (up to gmax) at which the animal and
    the room its moves need fit one free rectangle; it stands on that rectangle's floor (floats in the
    middle if it drifts) at the edge nearest Meatball, so the two read as a scene."""
    best = None
    for r, pref in zip(rects, (1.0, 0.5)):   # beside him (on the ground) beats floating above him
        g = gmax
        for _ in range(6):
            e = envelope([v * g for v in box], moves, idle, -side, contact)
            k = min(1.0, (r[2] - r[0]) / (e[2] - e[0]), (r[3] - r[1]) / (e[3] - e[1]))
            if k >= 0.999:
                break
            g *= k * 0.995
        ex = r[0] - e[0] if side == 1 else r[2] - e[2]
        ey = ((r[1] + r[3]) - (e[1] + e[3])) / 2 if idle == "drift" else r[3] - e[3]
        if best is None or g * pref > best[0]:
            best = (g * pref, dict(g=g, tx=ex, ty=ey, env=[e[0] + ex, e[1] + ey, e[2] + ex, e[3] + ey]))
    return best[1]


# acts whose v3 track already moves the right way when the animal is on Meatball's RIGHT (+1) or LEFT (-1)
BASE_SIDE = {"launch": -1, "run_off": -1, "peek": -1, "loop_out": -1}
TRAVEL = ("run_in", "run_off", "run_across", "launch")


def track(mascot, act, n, fps, t_act, home, side, seed):
    """mascot.act_track re-aimed for the v4 layout: he faces the animal, flees and is flung away from it,
    peeks and cowers from the far edge, and a peek ends on his mark instead of a fixed spot."""
    mirror = side != BASE_SIDE.get(act, 1)
    built = 1 - home if (mirror and act in TRAVEL) else home
    out = []
    for e in mascot.act_track(act, n, fps, t_act, built, seed=seed):
        e = dict(e)
        m = mirror
        if act in ("peek", "loop_out"):   # v3 slides in from x=1.4 to 0.9; here from the far edge to the mark
            p = (1.4 - e["x"]) / 0.5
            mark = 1 - home if mirror else home
            e["x"] = 1.4 + (mark - 1.4) * p
        elif act == "hide":               # cower at the edge away from the animal, leaning toward it
            e["x"], e["rot"], m = (0.14 if side == 1 else 0.86), 8.0 * side, False
        if m:
            e["x"] = 1 - e["x"] if (act in TRAVEL or act in ("peek", "loop_out")) else 2 * home - e["x"]
            e["rot"] = -e["rot"]
        face = side
        if act == "run_off" and e.get("run") is not None:
            face = -side                  # bolting away
        elif act == "run_across":
            face = 1
        e["flip"] = face == -1
        out.append(e)
    return out
