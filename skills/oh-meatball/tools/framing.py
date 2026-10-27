#!/usr/bin/env python3
"""Picture rules for tools/v3.py (TARS review 10/27). Each is a renderer default; the old behaviour stays
behind a spec flag (named in brackets).

  sharp()      a photo's sharpness score: Laplacian variance of its subject region at a fixed size
  subject()    the subject's box in photo fractions: the cut-out matte (tools/animal.py) when it found
               the animal, else a spectral-residual saliency box (no opencv-contrib needed)
  pick_sharp() (e) skip a photo whose short side is under 900 px when a beat has a bigger one
               ["soft_ok": true]
  frame0()     (b) frame 0 shows the beat's sharpest photo, cropped so the subject fills 50%+ of the frame
               ["frame0": false]
  cap_crop()   (e) widen a crop so the photo is never blown up more than 1.5x (the slow push included);
               a photo too small even whole is drawn at 1.5x over its own blurred copy
  dodge()      (c) Meatball's mark and size on the side of the frame the subject leaves free; he shrinks
               (to 62%) before he covers it, after make_room() slides the crop to give him a free side
               ["dodge": false]
"""
import os

import cv2
import numpy as np
from PIL import Image

MIN_SHORT = 900       # px: a smaller photo is soft once it fills a 1080x1920 frame
MAX_UP = 1.5          # never upscale more than this
FILL = 0.5            # frame 0: the subject's share of the frame
_SAL, _SHARP = {}, {}


def size(path):
    with Image.open(path) as im:
        return im.size


def saliency(path):
    """Spectral-residual saliency (Hou & Zhang 2007) -> the main subject's box in photo fractions."""
    if path in _SAL:
        return _SAL[path]
    im = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    h, w = im.shape
    s = cv2.resize(im, (128, 128)).astype(np.float32)
    f = np.fft.fft2(s)
    la = np.log(np.abs(f) + 1e-6)
    res = la - cv2.blur(la, (3, 3))
    sal = np.abs(np.fft.ifft2(np.exp(res + 1j * np.angle(f)))) ** 2
    sal = cv2.GaussianBlur(sal, (0, 0), 3)
    # colour contrast to the photo's mean colour helps on busy backgrounds
    col = cv2.resize(cv2.imread(path), (128, 128)).astype(np.float32)
    lab = cv2.cvtColor(col / 255.0, cv2.COLOR_BGR2LAB)
    con = cv2.GaussianBlur(np.linalg.norm(lab - lab.reshape(-1, 3).mean(0), axis=2), (0, 0), 3)
    m = sal / (sal.max() + 1e-9) + con / (con.max() + 1e-9)
    yy, xx = np.mgrid[0:128, 0:128]
    m *= 1.0 - 0.5 * (((xx - 64) / 64) ** 2 + ((yy - 64) / 64) ** 2) / 2   # photographers centre the subject
    thr = np.percentile(m, 82)
    mask = (m >= thr).astype(np.uint8)
    n, lab_, stats, _ = cv2.connectedComponentsWithStats(mask, 8)
    if n <= 1:
        box = [0.25, 0.25, 0.75, 0.75]
    else:
        k = 1 + int(np.argmax([(m[lab_ == j]).sum() for j in range(1, n)]))
        x, y, bw, bh = stats[k][:4]
        box = [x / 128, y / 128, (x + bw) / 128, (y + bh) / 128]
    _SAL[path] = box
    return box


def core(path):
    """The subject's solid core in photo fractions, for Meatball to stay clear of: the cut-out matte with thin
    parts (legs, antennae, tails, fins) eroded away, its largest piece, grown 12%. Saliency's top 6% else."""
    if ("core", path) in _SAL:
        return _SAL[("core", path)]
    box = None
    try:
        import animal
        _, _, _, m = animal._mask(path, [0, 0, 1, 1], [0.0, 0.0, 1.0, 1.0])
        if m.sum() > 50:
            h, w = m.shape
            k = max(3, int(0.045 * max(w, h)))
            e = cv2.erode(m, np.ones((k, k), np.uint8))
            if e.sum() < 20:
                e = cv2.erode(m, np.ones((k // 2, k // 2), np.uint8))
            src = e if e.sum() >= 20 else m
            n, lab, st, _ = cv2.connectedComponentsWithStats(src, 8)
            j = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
            x, y, bw, bh = st[j][:4]
            gx, gy = 0.12 * bw + k / 2, 0.12 * bh + k / 2
            box = [max(0, (x - gx) / w), max(0, (y - gy) / h), min(1, (x + bw + gx) / w), min(1, (y + bh + gy) / h)]
    except Exception:
        box = None
    if box is None or (box[2] - box[0]) * (box[3] - box[1]) > 0.8:
        box = saliency(path)
    _SAL[("core", path)] = box
    return box


def subject(path, info=None):
    """Subject box (photo fractions) from a cut-out's facts (animal.subject on the whole photo), else saliency."""
    if info is None:
        try:
            import animal
            info = animal.subject(path, None)
        except Exception:   # rembg missing or failed: saliency still works
            info = None
    if info and "box" in info and info.get("quality") != "no subject found":
        b = info["box"]
        if 0.01 < (b[2] - b[0]) * (b[3] - b[1]) < 0.92:
            c = info.get("crop") or [0, 0, 1, 1]
            cw, ch = c[2] - c[0], c[3] - c[1]
            return [c[0] + b[0] * cw, c[1] + b[1] * ch, c[0] + b[2] * cw, c[1] + b[3] * ch], "matte"
    return saliency(path), "saliency"


def sharp(path, box=None):
    """Sharpness: Laplacian variance of the subject region resampled to 512 px (comparable across photos)."""
    key = (path, tuple(box or ()))
    if key not in _SHARP:
        im = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        h, w = im.shape
        if box:
            im = im[int(box[1] * h):max(int(box[3] * h), int(box[1] * h) + 8),
                    int(box[0] * w):max(int(box[2] * w), int(box[0] * w) + 8)]
        k = 512 / max(im.shape)
        im = cv2.resize(im, (max(8, int(im.shape[1] * k)), max(8, int(im.shape[0] * k))), interpolation=cv2.INTER_AREA)
        _SHARP[key] = float(cv2.Laplacian(im, cv2.CV_64F).var())
    return _SHARP[key]


def score(path, crop=None):
    """Bigger is better: sharpness of the subject, halved for a photo under MIN_SHORT px."""
    w, h = size(path)
    c = crop or [0, 0, 1, 1]
    short = min((c[2] - c[0]) * w, (c[3] - c[1]) * h)
    box, _ = subject(path)
    return sharp(path, box) * (1.0 if short >= MIN_SHORT else 0.5 * short / MIN_SHORT)


def soft(path, crop=None):
    w, h = size(path)
    c = crop or [0, 0, 1, 1]
    return min((c[2] - c[0]) * w, (c[3] - c[1]) * h) < MIN_SHORT


def upscale(path, crop, W, H):
    """Screen px per photo px when the crop covers the W x H frame at zoom 1 (v3's R margin cancels out)."""
    pw, ph = size(path)
    c = crop or [0, 0, 1, 1]
    return max(W / ((c[2] - c[0]) * pw), H / ((c[3] - c[1]) * ph))


def cap_crop(path, crop, W, H, R=1.15, zmax=1.0):
    """(crop, fit): crop widened around its centre so it covers the frame at <= MAX_UP / zmax. fit = the base
    scale (base px per photo px) to draw the whole photo at MAX_UP over its own blur when even the whole photo
    would need more. v3 then stops the slow push where it would pass MAX_UP (push_cap())."""
    pw, ph = size(path)
    c = list(crop or [0, 0, 1, 1])
    umax = MAX_UP / zmax
    u = upscale(path, c, W, H)
    if u <= umax + 1e-6:
        return c, None
    g = u / umax
    cw, ch = (c[2] - c[0]) * pw, (c[3] - c[1]) * ph
    nw, nh = min(pw, cw * g), min(ph, ch * g)
    cx, cy = (c[0] + c[2]) / 2 * pw, (c[1] + c[3]) / 2 * ph
    x0 = min(max(0, cx - nw / 2), pw - nw)
    y0 = min(max(0, cy - nh / 2), ph - nh)
    c2 = [x0 / pw, y0 / ph, (x0 + nw) / pw, (y0 + nh) / ph]
    if upscale(path, c2, W, H) > umax + 1e-3:
        return c2, umax * R     # base = R x frame; the photo inside it at umax screen px per photo px
    return c2, None


def push_cap(path, crop, W, H, fit=None):
    """Largest zoom of the slow push that keeps the picture within MAX_UP (>= 1.0)."""
    u = (fit / 1.15) if fit else upscale(path, crop, W, H)
    return max(1.0, MAX_UP / u)


def frame0_crop(path, box, W, H, R=1.15, zmax=1.07):
    """Crop (photo fractions, frame aspect) around the subject so it fills >= FILL of the frame where the
    1.5x upscale cap allows; the largest such crop (most of the animal) wins."""
    pw, ph = size(path)
    a = W / H
    bx0, by0, bx1, by1 = box[0] * pw, box[1] * ph, box[2] * pw, box[3] * ph
    cx, cy = (bx0 + bx1) / 2, (by0 + by1) / 2
    min_w = max(W, H * a) / (MAX_UP / zmax)              # narrowest crop that keeps the upscale cap
    max_w = min(pw, ph * a)
    if min_w > max_w:
        return None
    best = None
    for k in range(60):
        cw = min_w + (max_w - min_w) * k / 59
        ch = cw / a
        x0 = min(max(0, cx - cw / 2), pw - cw)
        y0 = min(max(0, cy - ch / 2), ph - ch)
        iw = max(0, min(bx1, x0 + cw) - max(bx0, x0))
        ih = max(0, min(by1, y0 + ch) - max(by0, y0))
        fill = iw * ih / (cw * ch)
        crop = [x0 / pw, y0 / ph, (x0 + cw) / pw, (y0 + ch) / ph]
        if fill >= FILL:
            best = (fill, crop)            # keep widening while the subject still fills half the frame
        elif best is None and k == 0:
            best = (fill, crop)            # can't reach FILL inside the cap: the tightest allowed crop
    return [float(v) for v in best[1]], float(best[0])


def make_room(path, crop, W, H, need=0.44, prefer=-1):
    """(c) Slide a crop sideways inside the photo (size unchanged) so the subject's core leaves a free strip of
    `need` x the frame width for Meatball, on his home side (prefer -1 = left) when possible. Returns the crop."""
    pw, ph = size(path)
    c = list(crop or [0, 0, 1, 1])
    cw = c[2] - c[0]
    if cw >= 0.999:
        return c
    k = core(path)
    def free(x0):
        l = (k[0] - x0) / cw
        r = (x0 + cw - k[2]) / cw
        return l, r
    l, r = free(c[0])
    if max(l, r) >= need:
        return c
    opts = []
    for side in (prefer, -prefer):
        x0 = k[0] - need * cw if side < 0 else k[2] + need * cw - cw
        x0 = min(max(0.0, x0), 1.0 - cw)
        fl, fr = free(x0)
        opts.append((max(fl, fr) >= need - 1e-3, -abs(x0 - c[0]) * 0.01 + (fl if side < 0 else fr), x0))
    ok = [o for o in opts if o[0]]
    x0 = (ok[0] if ok else max(opts, key=lambda o: o[1]))[2]
    return [round(float(x0), 4), float(c[1]), round(float(x0 + cw), 4), float(c[3])]


def dodge(boxes, W, H, floor, home=0.24, size=1000, half_w=255, top=860):
    """(x, size, overlap): Meatball's mark and size clear of the subject's screen boxes (one per shot of the
    line, weighted equally). He keeps his size where a free side fits him, else shrinks to 55% before he
    covers the subject. overlap = the share of the subject box he still covers (0 when he fits)."""
    boxes = [b for b in boxes if b]
    if not boxes:
        return home, size, 0.0
    best = None
    for k in (1.0, 0.9, 0.8, 0.7, 0.62):
        sz = int(size * k)
        hw, tp = half_w * sz / 1000, top * sz / 1000
        lo, hi = (hw + 0.02 * W) / W, 1 - (hw + 0.02 * W) / W
        for i in range(41):
            x = lo + (hi - lo) * i / 40
            mb = [x * W - hw, floor - tp, x * W + hw, floor]
            ov = 0.0
            for b in boxes:
                iw = max(0, min(mb[2], b[2]) - max(mb[0], b[0]))
                ih = max(0, min(mb[3], b[3]) - max(mb[1], b[1]))
                ov = max(ov, iw * ih / max(1.0, (b[2] - b[0]) * (b[3] - b[1])))
            cost = 20 * ov + 1.2 * (1 - k) + 0.25 * abs(x - home)
            if best is None or cost < best[0]:
                best = (cost, x, sz, ov)
    return best[1], best[2], best[3]


def to_screen(path, crop, box, W, H, R=1.15, z=1.0, fit=None):
    """Photo-fraction box -> screen box for a v3 base (cover crop at R, centred) seen at zoom z."""
    pw, ph = size(path)
    c = crop or [0, 0, 1, 1]
    cw, ch = (c[2] - c[0]) * pw, (c[3] - c[1]) * ph
    bw, bh = int(W * R), int(H * R)
    s = fit or max(bw / cw, bh / ch)
    l, t = (cw * s - bw) / 2, (ch * s - bh) / 2
    k = (W / bw) * z
    f = lambda fx, fy: (k * (((fx - c[0]) * pw) * s - l - bw / 2) + W / 2,
                        k * (((fy - c[1]) * ph) * s - t - bh / 2) + H / 2)
    x0, y0 = f(box[0], box[1])
    x1, y1 = f(box[2], box[3])
    return [max(0, x0), max(0, y0), min(W, x1), min(H, y1)]


if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        b, src = subject(p)
        print(os.path.basename(p), size(p), src, [round(v, 3) for v in b], f"sharp {sharp(p, b):.0f}",
              "SOFT" if soft(p) else "")
