#!/usr/bin/env python3
"""Shorts v4 animal layer (research/45): find the animal in a shot's photo, cut it out whole, and make it act.

Used by tools/v3.py when a script has "style": "v4". Three jobs:
  1. subject(path, crop): rembg (isnet, as in the thumbnails) on the crop plus a margin around it (the
     whole photo if the animal runs past that), so the cut-out is the WHOLE animal even where the shot's
     crop clips it. Returns the subject's boxes, a head guess and a verdict: "ok", or why the shot falls
     back to the v3 still. Hard rules (Nolan, 10/25): the animal may not touch the photo's edge (it is
     cropped in the original), and cleaning the matte may not lose more than 3% of its area.
     Cached per photo region in ~/.cache/meatball-subjects (MEATBALL_SUBJECT_CACHE overrides).
  2. layers(...): the blurred, dimmed photo with the animal painted out (so a move reveals no ghost), and
     the animal as a sticker: the full matte with holes filled, contour smoothed at render resolution, eroded
     1 px under a uniform white stroke (so no background fringe shows), soft drop shadow.
  3. transform(...): the animal's 2D move per frame (bob, drift, lunge, strike, shake, turn).

Script fields: beat "animal": "lunge@kick" (move@word|seconds; a list for several), beat "contact": true
(Meatball may touch it: a poke, sting or kick), spec "subjects": {obs: {"head": [...], "cutout": false,
"idle": "drift"}} (photo fractions).
"""
import hashlib
import json
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageEnhance

CACHE = os.environ.get("MEATBALL_SUBJECT_CACHE", os.path.expanduser("~/.cache/meatball-subjects"))
MAX_SIDE = 2048   # rembg input cap (isnet runs at 1024 internally; the soft matte is upsampled)
_SESSION = None
VERSION = 5       # cache version (v3: whole-animal region mattes, loss vs nearby raw pieces)

# quality gate: a cut-out that fails any of these falls back to the v3 still for that shot
MIN_AREA = 0.02   # subject share of the crop
MAX_SOFT = 0.70   # share of the matte that is semi-transparent (water, glass, fog)
MIN_EDGE = 14.0   # mean Lab difference across the matte edge (low = camouflage, dark water)
MAX_LOSS = 0.03   # cleaning the matte may drop at most this share of the raw subject
STROKE = 7        # white outline width, px at base resolution (~6 px on screen)


def _session():
    global _SESSION
    if _SESSION is None:
        from rembg import new_session
        _SESSION = new_session("isnet-general-use")
    return _SESSION


def _key(path, reg):
    raw = f"v{VERSION}|{os.path.basename(path)}|{os.path.getsize(path)}|{tuple(round(c, 4) for c in reg)}"
    return hashlib.sha1(raw.encode()).hexdigest()[:16]


def _region(crop, grow=True):
    c = crop or [0, 0, 1, 1]
    if not grow:
        return [0.0, 0.0, 1.0, 1.0]
    w, h = c[2] - c[0], c[3] - c[1]
    return [max(0.0, c[0] - 0.6 * w), max(0.0, c[1] - 0.3 * h), min(1.0, c[2] + 0.6 * w), min(1.0, c[3] + 0.3 * h)]


def _px(path, reg):
    W, H = Image.open(path).size
    return int(reg[0] * W), int(reg[1] * H), int(reg[2] * W), int(reg[3] * H)


def matte(path, reg):
    """(region image, soft rembg matte at region resolution), cached per photo region."""
    os.makedirs(CACHE, exist_ok=True)
    f = f"{CACHE}/{_key(path, reg)}.png"
    im = Image.open(path).convert("RGB").crop(_px(path, reg))
    if not os.path.exists(f):
        from rembg import remove
        s = min(1.0, MAX_SIDE / max(im.size))
        small = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS) if s < 1 else im
        # same pre-boost as thumb3.cutout: rembg separates saturated subjects better
        boost = ImageEnhance.Color(ImageEnhance.Contrast(small).enhance(1.12)).enhance(1.3)
        remove(boost, session=_session(), only_mask=True).save(f)
    a = np.asarray(Image.open(f).convert("L").resize(im.size, Image.BILINEAR))
    return im, a


def _fill(m, frac=0.01):
    """Fill the matte's holes (pinholes in fur, a dark eye) but not the big enclosed gaps of real background,
    such as between legs whose toes touch: a hole bigger than `frac` of the animal stays open."""
    flood = np.pad(m, 1).copy()
    cv2.floodFill(flood, None, (0, 0), 1)
    holes = (1 - flood[1:-1, 1:-1]).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(holes, connectivity=4)
    small = [k for k in range(1, n) if st[k, cv2.CC_STAT_AREA] <= frac * m.sum()]
    return m | np.isin(lab, small).astype(np.uint8)


def _smooth(m, sigma):
    return (cv2.GaussianBlur(m.astype(np.float32), (0, 0), sigma) > 0.5).astype(np.uint8)


def _head(m, facing=None):
    """Head box guess (pixels): the top band of an upright subject, else the snout end of a long one."""
    ys, xs = np.nonzero(m)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    w, h = x1 - x0 + 1, y1 - y0 + 1
    if h >= 0.8 * w:
        band = m[y0:y0 + int(0.28 * h)]
        cols = np.nonzero(band.any(0))[0]
        return [int(cols.min()), int(y0), int(cols.max()), int(y0 + 0.28 * h)], "top"
    sl = int(0.3 * w)
    left, right = m[:, x0:x0 + sl].sum(), m[:, x1 - sl:x1 + 1].sum()
    side = facing or ("left" if left < right else "right")
    xa, xb = (x0, x0 + sl) if side == "left" else (x1 - sl, x1)
    rows = np.nonzero(m[:, xa:xb + 1].any(1))[0]
    return [int(xa), int(rows.min()), int(xb), int(rows.max())], side


def _mask(path, crop, reg):
    """(region image, raw hard mask of the subject's components, cleaned mask) in region pixels."""
    im, a = matte(path, reg)
    rx0, ry0, rx1, ry1 = _px(path, reg)
    cx0, cy0, cx1, cy1 = _px(path, crop or [0, 0, 1, 1])
    hard = (a > 128).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(hard, connectivity=8)
    inside = np.zeros_like(hard)
    inside[max(0, cy0 - ry0):cy1 - ry0, max(0, cx0 - rx0):cx1 - rx0] = 1
    if n < 2:
        return im, a, hard, hard
    score = np.bincount(lab[inside.astype(bool)].ravel(), minlength=n)[1:]
    if score.max() == 0:
        return im, a, np.zeros_like(hard), np.zeros_like(hard)
    main = int(score.argmax()) + 1
    big = st[main, cv2.CC_STAT_AREA]
    near = [k + 1 for k in range(n - 1) if score[k] > 0]          # everything rembg found that reaches the shot
    keep = [k for k in near if st[k, cv2.CC_STAT_AREA] >= 0.15 * big or k == main]
    m = np.isin(lab, keep).astype(np.uint8)
    # raw = every piece rembg found within reach of the animal (2% of the region); far-off specks (marine
    # snow, leaves) are not the animal, nearby pieces (a tentacle the matte broke off) are
    reach = cv2.dilate(m, np.ones((2 * int(0.02 * max(m.shape)) + 1,) * 2, np.uint8))
    raw = np.isin(lab, [k for k in near if (reach[lab == k]).any()]).astype(np.uint8)
    m = _smooth(_fill(m), max(1.0, 0.0015 * max(m.shape)))      # holes filled, jaggies off; no opening
    return im, a, raw, m


def subject(path, crop, parent=None):
    """Subject facts for one shot, boxes in crop fractions (a whole animal may extend past 0..1). A tighter
    re-cut of a shot (`parent` = the shot's crop) uses its parent's region, so both share one outline."""
    for grow in (True, False):
        reg = _region(parent or crop, grow)
        jf = f"{CACHE}/{_key(path, reg)}_{_key(path, crop or [0, 0, 1, 1])}.json"
        if os.path.exists(jf):
            info = json.load(open(jf))
        else:
            im, a, raw, m = _mask(path, crop, reg)
            info = _facts(path, crop, reg, im, a, raw, m)
            os.makedirs(CACHE, exist_ok=True)
            json.dump(info, open(jf, "w"))
        info["crop"] = list(crop or [0, 0, 1, 1])
        if not info.get("interior"):   # whole animal inside this region, or it already is the photo
            break
    return info


def _facts(path, crop, reg, im, a, raw, m):
    H, W = m.shape
    rx0, ry0, rx1, ry1 = _px(path, reg)
    cx0, cy0, cx1, cy1 = _px(path, crop or [0, 0, 1, 1])
    info = dict(reg=reg)
    if m.sum() < 50:
        return dict(info, quality="no subject found")
    b = 2
    edges = {"top": m[:b].any(), "bottom": m[-b:].any(), "left": m[:, :b].any(), "right": m[:, -b:].any()}
    photo_edge = {"top": reg[1] <= 0, "bottom": reg[3] >= 1, "left": reg[0] <= 0, "right": reg[2] >= 1}
    touch = [k for k, v in edges.items() if v and photo_edge[k]]
    interior = [k for k, v in edges.items() if v and not photo_edge[k]]
    parts = cv2.connectedComponents(m, connectivity=8)[0] - 1
    loss = float((raw & (1 - m)).sum()) / max(1.0, float(raw.sum()))
    in_crop = m[max(0, cy0 - ry0):cy1 - ry0, max(0, cx0 - rx0):cx1 - rx0]
    area = float(in_crop.sum()) / max(1.0, float((cx1 - cx0) * (cy1 - cy0)))
    soft = float(((a > 25) & (a < 230) & (cv2.dilate(m, np.ones((9, 9), np.uint8)) > 0)).sum()) / max(1.0, float(m.sum()))
    lab = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2LAB).astype(np.float32)
    k = max(3, int(0.012 * max(W, H)))
    ker = np.ones((k, k), np.uint8)
    inner = (m - cv2.erode(m, ker)).astype(bool)
    outer = (cv2.dilate(m, ker) - m).astype(bool)
    edge = float(np.linalg.norm(lab[inner].mean(0) - lab[outer].mean(0))) if inner.any() and outer.any() else 0.0
    ys, xs = np.nonzero(m)
    hb, side = _head(m)
    cw, ch = cx1 - cx0, cy1 - cy0
    f = lambda r: [round((r[0] + rx0 - cx0) / cw, 4), round((r[1] + ry0 - cy0) / ch, 4),
                   round((r[2] + 1 + rx0 - cx0) / cw, 4), round((r[3] + 1 + ry0 - cy0) / ch, 4)]
    q = "ok"
    if interior:
        q = "runs past the search region"
    elif touch:
        q = f"animal cropped in the photo (touches the {'/'.join(touch)} edge)"
    elif parts > 2:
        q = f"matte in pieces ({parts} parts: broken tentacles or legs)"
    elif loss > MAX_LOSS:
        q = f"matte clean-up would lose {loss:.0%} of the animal"
    elif area < MIN_AREA:
        q = f"subject too small ({area:.0%})"
    elif soft > MAX_SOFT:
        q = f"soft, see-through matte ({soft:.0%})"
    elif edge < MIN_EDGE:
        q = f"low edge contrast ({edge:.1f})"
    return dict(info, quality=q, interior=interior, touch=touch, loss=round(loss, 4), area=round(area, 4),
                soft=round(soft, 3), edge=round(edge, 1), box=f([xs.min(), ys.min(), xs.max(), ys.max()]),
                head=f(hb), head_from=side, cx=round((float(xs.mean()) + rx0 - cx0) / cw, 4),
                cy=round((float(ys.mean()) + ry0 - cy0) / ch, 4))


# ---------------------------------------------------------------- pictures

def photo_box(path, info):
    """The subject's box in photo pixels (from subject()'s crop-fraction box)."""
    cx0, cy0, cx1, cy1 = _px(path, info["crop"])
    b = info["box"]
    cw, ch = cx1 - cx0, cy1 - cy0
    return [cx0 + b[0] * cw, cy0 + b[1] * ch, cx0 + b[2] * cw, cy0 + b[3] * ch]


def layers(path, crop, reg, g, g_bg, blur=False):
    """The shot re-framed around the whole animal: (background RGB = the whole photo at scale g_bg, blurred
    and dimmed with the animal painted out; premultiplied RGBA sticker of the animal at scale g (screen px
    per photo px); the sticker's offset in g-scaled photo px). The background is scaled at least to cover
    the frame, so it may be larger than the animal's scale; it is only ever seen soft."""
    im, a, raw, m = _mask(path, crop, reg)
    rx0, ry0, _, _ = _px(path, reg)
    photo = Image.open(path).convert("RGB")
    PW, PH = photo.size
    gw, gh = max(1, int(PW * g_bg)), max(1, int(PH * g_bg))
    # background: paint the animal out at a quarter of the output scale, then blur and dim
    sw, sh = max(8, gw // 4), max(8, gh // 4)
    small = np.asarray(photo.resize((sw, sh), Image.BILINEAR))
    full_m = np.zeros((PH, PW), np.uint8)
    full_m[ry0:ry0 + m.shape[0], rx0:rx0 + m.shape[1]] = m
    hole = cv2.dilate(cv2.resize(full_m * 255, (sw, sh), interpolation=cv2.INTER_AREA),
                      np.ones((7, 7), np.uint8))
    fill = cv2.inpaint(small, (hole > 30).astype(np.uint8) * 255, 6, cv2.INPAINT_TELEA)
    bg = cv2.GaussianBlur(cv2.resize(fill, (gw, gh), interpolation=cv2.INTER_LINEAR).astype(np.float32),
                          (0, 0), 14) * 0.78
    # sticker: the subject's box (+ room for the stroke and shadow) at scale g
    yy, xx = np.nonzero(m)
    pad = int((STROKE + 30) / g) + 2
    x0, y0 = max(0, xx.min() - pad), max(0, yy.min() - pad)
    x1, y1 = min(m.shape[1], xx.max() + pad + 1), min(m.shape[0], yy.max() + pad + 1)
    tw, th = max(1, int((x1 - x0) * g)), max(1, int((y1 - y0) * g))
    col = np.asarray(im.crop((x0, y0, x1, y1)).resize((tw, th), Image.LANCZOS)).astype(np.float32)
    # contour at output resolution: resample, smooth, threshold -> one clean curve, no stair steps
    mm = cv2.resize(m[y0:y1, x0:x1].astype(np.float32), (tw, th), interpolation=cv2.INTER_AREA if g < 1 else cv2.INTER_LINEAR)
    mm = (cv2.GaussianBlur(mm, (0, 0), 1.2) > 0.5).astype(np.uint8)
    core = cv2.erode(mm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))  # 1 px in: no fringe
    alpha = cv2.GaussianBlur(core.astype(np.float32), (0, 0), 0.7)
    dist = cv2.distanceTransform((1 - core).astype(np.uint8), cv2.DIST_L2, 5)
    rim = np.clip(STROKE + 0.5 - dist, 0, 1)                                  # uniform-width white stroke
    shadow = cv2.warpAffine(cv2.GaussianBlur(np.maximum(rim, alpha), (0, 0), 8) * 0.42,
                            np.float32([[1, 0, 5], [0, 1, 8]]), (tw, th))
    if blur:  # host shot: the animal stays soft and dim like the rest of the picture, no outline
        A = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 4)
        C = cv2.GaussianBlur(col, (0, 0), 7) * 0.80 * A[..., None]
    else:
        C = np.array([30, 6, 0], np.float32) * shadow[..., None]
        A = shadow
        C = 255 * rim[..., None] + C * (1 - rim[..., None])
        A = rim + A * (1 - rim)
        C = col * alpha[..., None] + C * (1 - alpha[..., None])
        A = alpha + A * (1 - alpha)
    st = np.dstack([np.clip(C, 0, 255), np.clip(A * 255, 0, 255)]).astype(np.uint8)
    return np.clip(bg, 0, 255).astype(np.uint8), st, ((rx0 + x0) * g, (ry0 + y0) * g)


# ---------------------------------------------------------------- acting

MOVES = ("lunge", "kick", "charge", "strike", "snap", "sting", "bob", "breathe", "drift", "shake", "turn", "look")
ALIAS = {"kick": "lunge", "charge": "lunge", "snap": "strike", "sting": "strike", "breathe": "bob", "look": "turn"}
SFX = {"lunge": ("whoosh", -0.16), "strike": ("whoosh", -0.10), "turn": ("whoosh", 0.0)}


def parse(spec):
    """'lunge@kick' or ['drift', 'strike@once'] -> [(move, at)]"""
    if not spec:
        return []
    spec = [spec] if isinstance(spec, str) else spec
    out = []
    for e in spec:
        nm, _, at = e.partition("@")
        out.append((ALIAS.get(nm, nm), at or None))
    return out


def _ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def lunge(dt, toward):
    """Kick / charge toward Meatball: 5-frame wind-up (lean back, squash), 2-frame snap (scale up +
    translate), hold, settle. dt = seconds from the impact frame. Returns (dx, dy, scale, sx, sy, rot)."""
    fps = 30.0
    k = dt * fps
    if k < -5 or k > 22:
        return 0, 0, 1, 1, 1, 0
    if k < -2:            # wind-up: back and down
        u = _ease((k + 5) / 3)
        return -0.035 * toward * u, 0.012 * u, 1 - 0.03 * u, 1 + 0.05 * u, 1 - 0.06 * u, -4 * toward * u
    if k < 0:             # snap: two frames to full extension
        u = (k + 2) / 2
        return (-0.035 + 0.155 * u) * toward, 0.012 - 0.03 * u, 0.97 + 0.21 * u, 1.05 - 0.09 * u, 0.94 + 0.12 * u, (-4 + 10 * u) * toward
    if k < 5:             # impact hold with a tiny overshoot wobble
        w = math.sin(k * 1.9) * math.exp(-k / 2)
        return 0.12 * toward, -0.018, 1.18 + 0.02 * w, 0.96 - 0.02 * w, 1.06 + 0.02 * w, 6 * toward
    u = _ease((k - 5) / 17)  # settle back home
    return 0.12 * toward * (1 - u), -0.018 * (1 - u), 1 + 0.18 * (1 - u), 1 - 0.04 * (1 - u), 1 + 0.06 * (1 - u), 6 * toward * (1 - u)


def strike(dt, toward):
    """Fast jab and return (sting, snap, bite): 3-frame cock back, 2-frame jab, 6-frame return."""
    k = dt * 30.0
    if k < -3 or k > 9:
        return 0, 0, 1, 1, 1, 0
    if k < -1:
        u = _ease((k + 3) / 2)
        return -0.025 * toward * u, 0, 1 - 0.02 * u, 1, 1, -3 * toward * u
    if k < 1:
        u = (k + 1) / 2
        return (-0.025 + 0.115 * u) * toward, -0.01 * u, 0.98 + 0.12 * u, 1, 1, (-3 + 8 * u) * toward
    u = _ease((k - 1) / 8)
    return 0.09 * toward * (1 - u), -0.01 * (1 - u), 1.10 - 0.10 * u, 1, 1, 5 * toward * (1 - u)


def idle(t, kind, seed):
    """Always-on motion so a cut-out is never frozen: a breathing bob, or a slow drift for floaters."""
    ph = (seed * 1.7) % 6.28
    if kind == "drift":   # jellyfish / fish: float up and sideways, the bell pulses
        pulse = math.sin(2 * math.pi * 0.9 * t + ph)
        return (0.018 * math.sin(2 * math.pi * 0.23 * t + ph), -0.014 * t + 0.01 * math.sin(2 * math.pi * 0.4 * t),
                1.0, 1 + 0.025 * pulse, 1 - 0.03 * pulse, 2.0 * math.sin(2 * math.pi * 0.3 * t + ph))
    b = math.sin(2 * math.pi * 0.75 * t + ph)
    return 0.0, -0.0045 * (1 - math.cos(2 * math.pi * 0.75 * t)) / 2, 1.0, 1 - 0.006 * b, 1 + 0.010 * b, 0.6 * b


def shake(dt, dur=0.7):
    if dt < 0 or dt > dur:
        return 0.0, 0.0
    env = math.exp(-dt * 3) * 1.0
    return 0.012 * env * math.sin(2 * math.pi * 14 * dt), 3.5 * env * math.sin(2 * math.pi * 11 * dt + 1)


def transform(moves, t, toward, seed, idle_kind="bob", n_left=None, ts=None, n_from=None):
    """Combined move at beat time t (s); ts = seconds into the shot (the idle restarts each shot).
    moves = [(name, t_at)]. Returns dict(dx, dy (frame-width fractions), s, sx, sy, rot (deg),
    flip (0..1 progress of a turn: sx goes 1 -> -1 through a squash)). n_left / n_from = frames to the end /
    from the start of the Short: the move eases to rest there, so the loop's last frame matches frame 0."""
    dx, dy, s, sx, sy, rot = idle(t if ts is None else ts, idle_kind, seed)
    flip = 0.0
    for nm, ta in moves:
        dt = t - ta
        if nm == "lunge":
            m = lunge(dt, toward)
        elif nm == "strike":
            m = strike(dt, toward)
        elif nm == "shake":
            x, r = shake(dt)
            m = (x, 0, 1, 1, 1, r)
        elif nm == "turn":
            u = _ease(dt / 0.22)
            flip = max(flip, u)
            sq = math.sin(math.pi * u) if 0 < u < 1 else 0
            m = (0, 0.006 * sq, 1, 1, 1 - 0.07 * sq, 0)
        else:
            continue
        dx, dy, rot = dx + m[0], dy + m[1], rot + m[5]
        s, sx, sy = s * m[2], sx * m[3], sy * m[4]
    edge = min(n_left if n_left is not None else 99, n_from if n_from is not None else 99)
    if edge < 8:   # ease to rest at the loop seam (last frame = frame 0)
        e = _ease(edge / 8)
        dx, dy, rot, s, sx, sy = dx * e, dy * e, rot * e, 1 + (s - 1) * e, 1 + (sx - 1) * e, 1 + (sy - 1) * e
    return dict(dx=dx, dy=dy, s=s, sx=sx, sy=sy, rot=rot, flip=flip)
