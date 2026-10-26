#!/usr/bin/env python3
"""Procedural music beds for "Meatball Investigates" (Nolan 10/25: "intriguing and maybe even mysterious music,
something that attracts people to keep watching"). Original, made here from oscillators and noise: no samples,
no third-party licence (we release these beds CC0).

Each bed is rendered to the exact length of the video and follows its timeline:
  * it builds slowly over the whole clip and rises into every reveal (a filtered-noise riser, denser ticks),
  * it drops out for a beat right before each verdict stamp, so the silence lands the payoff,
  * a small hit (low boom + bell) plays on the stamp,
  * the end crossfades into the start, so a looping Short has no seam.

Kinds:
  "mystery"    (main) low pulsing bass in eighths, clock ticks, plucked minor-second tension, airy pad, 96 bpm
  "detective"  (alternate) lighter curious pizzicato: walking pizz bass, staccato pizz melody, snaps, 112 bpm

Usage from v3.py: spec "music": "gen:mystery" | "gen:detective"; the stamp times come from beat "stamp" fields.
CLI: music.py KIND SECONDS OUT.wav [reveal_s ...]   (a preview without a video)
"""
import math
import sys
import wave

import numpy as np

SR = 48000
A4 = 440.0


def hz(n):
    """MIDI note -> Hz."""
    return A4 * 2 ** ((n - 69) / 12)


def env_adsr(n, a, d, s, r, sr=SR):
    a, d, r = int(a * sr), int(d * sr), int(r * sr)
    e = np.full(n, s, np.float32)
    if a:
        e[:min(a, n)] = np.linspace(0, 1, a, dtype=np.float32)[:n]
    if d and a < n:
        e[a:a + d] = np.linspace(1, s, d, dtype=np.float32)[:max(0, n - a)]
    if r and n > r:
        e[-r:] *= np.linspace(1, 0, r, dtype=np.float32)
    return e


def lp_fast(x, fc):
    """Static one-pole low-pass via IIR in numpy (scipy-free): exact for a constant cut-off."""
    a = 1 - math.exp(-2 * math.pi * fc / SR)
    # y[n] = (1-a) y[n-1] + a x[n]: closed form with an FFT convolution against the decaying kernel
    k = int(min(len(x), max(64, 6 * SR / (2 * math.pi * fc))))
    h = a * (1 - a) ** np.arange(k, dtype=np.float64)
    return fftconv(x, h)[:len(x)].astype(np.float32)


def fftconv(x, h):
    n = len(x) + len(h) - 1
    m = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(h, m), m)[:n]


def pluck(f, dur, bright=0.5, decay=0.996, seed=0):
    """Karplus-Strong plucked string."""
    rng = np.random.default_rng(seed)
    N = max(2, int(SR / f))
    n = int(dur * SR)
    y = np.zeros(n + N, np.float32)
    y[:N] = rng.uniform(-1, 1, N) * bright + (1 - bright) * np.sin(np.linspace(0, 2 * np.pi, N))
    for i in range(N, n + N, N):
        prev = y[i - N:i]
        nxt = 0.5 * (prev + np.roll(prev, 1)) * decay
        y[i:i + N] = nxt[:len(y[i:i + N])]
    out = y[N:N + n]
    out *= env_adsr(n, 0.002, 0.0, 1.0, min(0.05, dur / 3))
    return out


def saw(f, n, detune=0.0, phase=0.0):
    t = np.arange(n) / SR
    return (2 * ((t * f * (1 + detune) + phase) % 1.0) - 1).astype(np.float32)


def sine(f, n, phase=0.0):
    return np.sin(2 * np.pi * f * np.arange(n) / SR + phase).astype(np.float32)


def add(buf, sig, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf) or i + len(sig) <= 0:
        return
    if i < 0:
        sig, i = sig[-i:], 0
    m = min(len(sig), len(buf) - i)
    buf[i:i + m] += sig[:m] * gain


def reverb(x, secs=2.2, mix=0.28, seed=3):
    rng = np.random.default_rng(seed)
    n = int(secs * SR)
    ir = rng.standard_normal(n).astype(np.float32) * np.exp(-np.arange(n) / (SR * secs / 6.5)).astype(np.float32)
    ir = lp_fast(ir, 5200)
    ir /= np.sqrt((ir ** 2).sum()) + 1e-9
    wet = fftconv(x, ir)[:len(x)].astype(np.float32)
    return x * (1 - mix) + wet * mix * 1.6


def tick(n=0.018, f=3200, seed=0):
    rng = np.random.default_rng(seed)
    k = int(n * SR)
    s = rng.standard_normal(k).astype(np.float32) * np.exp(-np.arange(k) / (SR * 0.003)).astype(np.float32)
    return s * 0.6 + sine(f, k) * np.exp(-np.arange(k) / (SR * 0.004)).astype(np.float32)


def boom(dur=1.1):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 46 + 70 * np.exp(-t * 14)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-t * 4.0)).astype(np.float32)


def bell(f, dur=1.4):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * d) for a, r, d in
            ((1, 1, 2.5), (0.5, 2.76, 4), (0.3, 5.4, 6), (0.2, 8.93, 9)))
    return (s * env_adsr(n, 0.002, 0, 1, 0.05)).astype(np.float32)


def intensity(t, total, reveals):
    """0..1: a slow build across the clip (back to the start level at the end, for the loop), plus a rise into
    each reveal over ~3 s."""
    base = 0.35 + 0.35 * np.sin(np.pi * np.clip(t / max(total, 1e-6), 0, 1)) ** 1.5
    rise = np.zeros_like(t)
    for r in reveals:
        u = np.clip((t - (r - 3.0)) / 3.0, 0, 1) * (t < r)
        rise = np.maximum(rise, u ** 2)
    return np.clip(base + 0.45 * rise, 0, 1)


def gaps(t, reveals, pre=0.42):
    """Gain 1, falling to 0 for `pre` s right before each reveal (the drop-out), back in on the stamp."""
    g = np.ones_like(t)
    for r in reveals:
        a = r - pre
        fade = np.clip((t - (a - 0.08)) / 0.08, 0, 1)          # 80 ms duck into the silence
        g = np.minimum(g, np.where((t >= a - 0.08) & (t < r), 1 - fade, 1.0))
    return g


PROG = [(57, "m"), (53, "M"), (50, "m"), (52, "M")]   # Am  F  Dm  E  (i VI iv V): mystery, never resolved
TRIAD = {"m": (0, 3, 7), "M": (0, 4, 7)}


def mystery(total, reveals, seed=1):
    bpm = 96.0
    beat = 60 / bpm
    bar = 4 * beat
    n = int((total + 2 * bar + 3) * SR)
    t = np.arange(n) / SR
    bass, ticks, plucks, pad = (np.zeros(n, np.float32) for _ in range(4))
    I = intensity(t, total, reveals)
    nbar = int(math.ceil((total + bar) / bar)) + 1
    for b in range(nbar):
        root, q = PROG[(b // 2) % 4]
        t0 = b * bar
        # pad: detuned saws on the chord, slow swell, darkened
        m = int(bar * SR) + int(0.6 * SR)
        ch = sum(saw(hz(root + 12 + iv), m, d) for iv in TRIAD[q] for d in (-0.004, 0.0035))
        ch = ch * env_adsr(m, 0.9, 0.0, 1.0, 0.6)
        add(pad, ch / 6, t0)
        # bass: eighth-note pulse, sine + soft saw, plucky envelope
        for k in range(8):
            ts = t0 + k * beat / 2
            m = int(beat / 2 * SR * 0.92)
            note = hz(root - 24) * (2 if k in (3, 7) else 1)
            s = sine(note, m) * 0.8 + saw(note, m) * 0.25
            add(bass, s * env_adsr(m, 0.004, 0.12, 0.35, 0.03), ts, 0.9 if k % 2 == 0 else 0.6)
        # ticks: sixteenths, accented on beats (density rises with intensity, handled by gain below)
        for k in range(16):
            add(ticks, tick(seed=b * 16 + k), t0 + k * beat / 4, 1.0 if k % 4 == 0 else 0.45)
        # plucked tension: minor second + fifth figure on the off-beats
        for k, iv in ((1, 7), (3, 8), (5, 7), (6, 13), (7, 12)):
            add(plucks, pluck(hz(root + 12 + iv), 0.9, 0.55, 0.9965, seed=b * 8 + k), t0 + k * beat / 2 + beat / 4,
                0.55)
    pad = lp_fast(pad, 1100)
    air = lp_fast(np.random.default_rng(seed).standard_normal(n).astype(np.float32), 5000) * 0.05
    air -= lp_fast(air, 900)
    riser = np.zeros(n, np.float32)
    rn = np.random.default_rng(seed + 9).standard_normal(n).astype(np.float32)
    for r in reveals:   # a filtered noise swell over the 2.5 s into each reveal
        a, z = int(max(0, r - 2.5) * SR), int(r * SR)
        if z > a:
            u = np.linspace(0, 1, z - a, dtype=np.float32)
            seg = rn[a:z] - lp_fast(rn[a:z], 400 + 3000 * 0.5)
            riser[a:z] += seg * (u ** 2.2) * 0.22
    mix = (bass * (0.55 + 0.45 * I) + ticks * 0.16 * (0.4 + 0.9 * I) + plucks * 0.42 * (0.5 + 0.6 * I)
           + pad * 0.32 + air * (0.6 + I) + riser)
    return mix, bar


def detective(total, reveals, seed=2):
    bpm = 112.0
    beat = 60 / bpm
    bar = 4 * beat
    n = int((total + 2 * bar + 3) * SR)
    t = np.arange(n) / SR
    I = intensity(t, total, reveals)
    low, mel, perc = (np.zeros(n, np.float32) for _ in range(3))
    walk = [0, 3, 5, 6, 7, 6, 5, 3]          # walking minor line with the blue note
    tune = [12, None, 15, 14, None, 12, 10, None, 7, None, 10, 11, 12, None, None, None]
    nbar = int(math.ceil((total + bar) / bar)) + 1
    for b in range(nbar):
        root = (50, 50, 53, 52)[b % 4]       # Dm Dm F E
        t0 = b * bar
        for k in range(8):
            add(low, pluck(hz(root - 12 + walk[k]), 0.45, 0.35, 0.993, seed=b * 9 + k), t0 + k * beat / 2, 0.9)
        for k, iv in enumerate(tune):
            if iv is not None and (b % 2 == 0 or k < 8):
                add(mel, pluck(hz(root + 12 + iv), 0.22, 0.75, 0.985, seed=b * 17 + k), t0 + k * beat / 4, 0.55)
        for k in (1, 3):                      # finger snaps on 2 and 4
            sn = tick(0.05, 1800, seed=b * 4 + k)
            add(perc, sn, t0 + k * beat, 0.8)
        for k in range(8):                    # soft brush on the eighths
            add(perc, tick(0.03, 7000, seed=b * 40 + k) * 0.5, t0 + k * beat / 2, 0.25)
    mix = low * 0.7 + mel * (0.45 + 0.25 * I) + perc * 0.2 * (0.6 + 0.6 * I)
    return mix, bar


def render(kind, total, reveals=(), out=None):
    """The bed as stereo float32 (n, 2) at SR, exactly `total` s long, loop-safe; written to `out` if given."""
    reveals = sorted(r for r in reveals if 0.5 < r < total)
    mix, bar = (mystery if kind == "mystery" else detective)(total, reveals)
    mix = reverb(mix, 2.4 if kind == "mystery" else 1.2, 0.30 if kind == "mystery" else 0.18)
    N = int(total * SR)
    xf = int(min(1.2, total / 6) * SR)
    sig = mix[:N + xf].copy()
    t = np.arange(len(sig)) / SR
    sig *= gaps(t, reveals)
    for r in reveals:   # the payoff hit: low boom + a bell a fifth over the key
        add(sig, boom(1.4) * 0.55 + bell(hz(81 if kind == "mystery" else 74)) * 0.25, r)
    ramp = np.linspace(0, 1, xf, dtype=np.float32)   # loop: the tail fades into the head
    head = sig[:xf] * ramp + sig[N:N + xf] * (1 - ramp)
    sig = sig[:N]
    sig[:xf] = head
    sig /= np.abs(sig).max() + 1e-9
    sig *= 0.7
    width = np.roll(sig, int(0.011 * SR))            # a little width: Haas-delayed copy at low level
    st = np.stack([sig * 0.92 + width * 0.08, sig * 0.92 - width * 0.08], 1).astype(np.float32)
    if out:
        with wave.open(out, "wb") as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((np.clip(st, -1, 1) * 32767).astype("<i2").tobytes())
    return st


if __name__ == "__main__":
    kind, secs, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
    render(kind, secs, [float(x) for x in sys.argv[4:]], out)
    print("ok", out)
