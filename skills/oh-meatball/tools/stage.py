#!/usr/bin/env python3
"""Shorts v4 staging (research/45). Two jobs:
  1. Meatball's mark and facing: on cut-out shots he is tucked against the left edge (tuck()); on a v3 still
     (the animal can't move) place() keeps him off its head (a pinned head box) unless the beat is a contact.
  2. frame_fit(): re-frame a cut-out shot around the whole animal, as large as fits, with room for its moves,
     beside him (or leaning over his head where its outline leaves room: keepout(), strips()), above the
     captions and inside the frame.
track() re-aims mascot.act_track so he faces the animal and flees, peeks and cowers on the far side.
Boxes are screen pixels (1080x1920; configure() sets the 1920x1080 long-form layout).
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

SAFE = (0.015 * W, 130.0, 0.985 * W, 1465.0)   # the animal stays inside this: clear of the Shorts UI and captions
GAP = 18.0    # clear air between Meatball (who leans and trembles) and the animal
PAD = 10.0    # the sticker's white stroke and a little more
GMAX = 2.0    # largest scale, screen px per photo px (photos are ~2048 px; the outline is redrawn at this scale)
REACH = {"lunge": (0.12, 1.18), "strike": (0.09, 1.10)}   # forward reach (frame widths), peak scale
REACHES = (1.0, 0.5)   # full forward reach, or a shorter one when the full one would shrink the animal
ROT = {"lunge": 6.0, "strike": 5.0, "shake": 3.5}          # peak tilt (degrees) about the feet


LEAN = {"peek": 0.17, "loop_out": 0.17}   # acts that lean his head toward the animal (frame widths at size 1000)


def tuck(size):
    """v4 bigger: Meatball's mark tucked against the frame's left edge at this size (whole body on screen)."""
    return (MB_HALF_W * size / 1000 + 0.02 * W) / W


AIRBORNE = ("tumble", "launch")   # acts that pass through the space above his mark


def keepout(x, size, side, top=None, contact=False, act=None):
    """Where the animal and its moves may not go: dict(box = Meatball's body plus clear air, out to the frame
    edge behind him; top = below a pop-in label). A contact beat lets the animal's move envelope reach
    almost halfway into him (its outline sits inside that envelope, so it still touches him). On acts where
    he falls in from above or is flung up, nothing may lean over his head."""
    top = SAFE[1] if top is None else top
    mb = mb_box(x, size)
    d = -0.45 * (mb[2] - mb[0]) if contact else GAP + LEAN.get(act, 0.0) * W * size / 1000
    d += 0.0 if contact or act not in AIRBORNE else 2 * GAP   # he spins as he falls or flies
    y = -1e9 if act in AIRBORNE else mb[1] if contact else mb[1] - GAP
    return dict(box=[-1e9, y, mb[2] + d, 1e9] if side == 1 else [mb[0] - d, y, 1e9, 1e9], top=top)


SOLO = dict(box=[-1e9, -1e9, -1e9, -1e9], top=SAFE[1])   # no Meatball on screen (before a peek)


def configure(w, h, floor, safe):
    """Another frame layout (v3.landscape(): 1920x1080 long-forms): frame size, Meatball's floor, the safe box."""
    global W, H, FLOOR, SAFE
    W, H, FLOOR, SAFE = w, h, floor, tuple(safe)
    SOLO["top"] = SAFE[1]


def strips(sil, g, moves, idle, toward, contact, reach=1.0):
    """The screen strips (x0, x1, top, bottom) the animal's outline can sweep during its moves, at scale g with
    its photo origin at (0, 0): peak scale and tilt about its feet, a turn's mirror image, the idle bob or drift,
    and (unless the beat is a contact) its forward reach toward Meatball and the wind-up back."""
    names = [m for m, _ in moves]
    sc = max([1 + (REACH[m][1] - 1) * reach for m in names if m in REACH] + [1.02])
    fwd = 0.0 if contact else max([REACH[m][0] for m in names if m in REACH] + [0.0]) * W * reach
    back = 0.045 * W * reach if fwd else 0.0
    rot = math.sin(math.radians(max([ROT[m] for m in names if m in ROT] + [1.0])))
    x0, x1, feet = min(s[0] for s in sil) * g, max(s[1] for s in sil) * g, max(s[3] for s in sil) * g
    cx = (x0 + x1) / 2
    src = [(a * g, b * g, t * g, u * g) for a, b, t, u in sil]
    if "turn" in names:
        src += [(2 * cx - b, 2 * cx - a, t, u) for a, b, t, u in src]
    out = []
    for a, b, t, u in src:
        a, b = cx + sc * 1.02 * (a - cx), cx + sc * 1.02 * (b - cx)   # 1.02: the squash widens it
        t, u = feet - sc * (feet - t), feet - sc * (feet - u)
        hx, hy = (feet - t) * rot, max(abs(a - cx), abs(b - cx)) * rot
        a, b, t, u = a - hx, b + hx, t - hy, u + hy
        if idle == "drift":
            a, b, t, u = a - 0.02 * W, b + 0.02 * W, t - 0.05 * W, u + 0.012 * W
        else:
            a, b, t, u = a - 4, b + 4, t - 0.012 * W, u + 4
        if fwd:
            t -= 0.03 * W
            a, b = (a - fwd, b + back) if toward == -1 else (a - back, b + fwd)
        out.append((a - PAD, b + PAD, t - PAD, u + PAD))
    return out


def _place(st, keep, side, idle, outer=None):
    """(tx, ty) for envelope strips st, or None: inside SAFE (below keep["top"]) and clear of Meatball's
    keep-out box. outer (default st): the strips that must stay inside SAFE; on a contact beat they also hold
    the forward reach that st leaves out, so a lunge into him never leaves the frame. A walker stands on
    SAFE's floor; a drifter centres, rising clear of him if it must. Then it slides toward him as far as
    stays clear, so the two read as a scene."""
    k, top = keep["box"], keep["top"]
    outer = outer or st
    ex0, ex1 = min(s[0] for s in outer), max(s[1] for s in outer)
    ey0, ey1 = min(s[2] for s in outer), max(s[3] for s in outer)
    if ex1 - ex0 > SAFE[2] - SAFE[0] or ey1 - ey0 > SAFE[3] - top:
        return None
    tx = SAFE[2] - ex1 if side == 1 else SAFE[0] - ex0       # start as far from him as possible
    ty = SAFE[3] - ey1 if idle != "drift" else ((top + SAFE[3]) - (ey0 + ey1)) / 2
    hit = lambda tx, ty: max([s[3] + ty - k[1] for s in st if s[1] + tx > k[0] and s[0] + tx < k[2]] + [0.0])
    if hit(tx, ty) > 0:
        if idle != "drift":
            return None
        ty -= hit(tx, ty) + GAP
    if ey0 + ty < top:
        return None
    lim = (SAFE[0] - ex0) if side == 1 else (SAFE[2] - ex1)
    while abs(tx - lim) > 1e-6:
        nx = max(lim, tx - 6.0) if side == 1 else min(lim, tx + 6.0)
        if hit(nx, ty) > 0:
            break
        tx = nx
    return tx, ty


def _largest(fit, gmax):
    """(g, (tx, ty)) for the largest scale up to gmax that fit() places, or None."""
    pos = fit(gmax)
    if pos:
        return gmax, pos
    lo, hi, pos = 0.02, gmax, None
    for _ in range(16):
        mid = (lo + hi) / 2
        p = fit(mid)
        lo, hi, pos = (mid, hi, p) if p else (lo, mid, pos)
    return (lo, pos) if pos else None


def frame_fit(sil, moves, idle, side, contact, keep, gmax=GMAX):
    """Re-frame a cut-out shot around the whole animal. sil = its outline strips in photo px (animal.outline).
    Returns dict(g, tx, ty, env): screen = (tx, ty) + g * photo px, the largest scale (up to gmax) at which the
    animal and the room its moves need fit the frame without reaching Meatball. The test uses the animal's
    real outline, so a tall animal may lean over his head where its body leaves room. fit["reach"] scales
    the forward travel of its lunge or strike (animal.transform) where the full reach would cost size."""
    best = None
    for reach in REACHES:   # a lunge or strike that would cost the animal size reaches less far instead
        st = lambda g, r=reach: strips(sil, g, moves, idle, -side, contact, r)
        so = lambda g, r=reach: strips(sil, g, moves, idle, -side, False, r)
        fit = _largest(lambda g: _place(st(g), keep, side, idle, so(g)), gmax) or (0.02, (SAFE[0], SAFE[1]))
        if best is None or fit[0] > best[0][0] * 1.08:
            best = (fit, reach, so)
    (g, (tx, ty)), reach, so = best
    e = so(g)
    env = [min(s[0] for s in e) + tx, min(s[2] for s in e) + ty, max(s[1] for s in e) + tx, max(s[3] for s in e) + ty]
    return dict(g=g, tx=tx, ty=ty, env=env, reach=reach)


# acts whose v3 track already moves the right way when the animal is on Meatball's RIGHT (+1) or LEFT (-1)
BASE_SIDE = {"launch": -1, "run_off": -1, "peek": -1, "loop_out": -1}
TRAVEL = ("run_in", "run_off", "run_across", "launch")


def track(mascot, act, n, fps, t_act, home, side, seed):
    """mascot.act_track re-aimed for the v4 layout: he faces the animal, flees and is flung away from it,
    peeks and cowers from the far edge, and a peek ends on his mark instead of a fixed spot. A peek's entries
    carry "peek" (0 off screen .. 1 on his mark), which pulls a cut-out back from its solo framing."""
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
            e["peek"] = 0.0 if e.get("hidden") else min(1.0, max(0.0, p))   # 0 off screen .. 1 on his mark
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
