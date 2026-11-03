#!/usr/bin/env python3
"""Procedural music beds for "Meatball Investigates" (Nolan 10/25: "intriguing and maybe even mysterious music,
something that attracts people to keep watching"). Original, made here from oscillators and noise: no samples,
no third-party licence (we release these beds CC0).

Each bed is rendered to the exact length of the video and follows its timeline:
  * it builds slowly over the whole clip and rises into every reveal (a filtered-noise riser, denser ticks),
  * it drops out for a beat right before each verdict stamp, so the silence lands the payoff,
  * a small hit (low boom + bell) plays on the stamp,
  * the end crossfades into the start, so a looping Short has no seam.

Kinds (tools/themes.py maps each script "theme" to one):
  "mystery" / "conspiracy"  dark pulsing synth: bass in eighths, clock ticks, plucked minor-second tension, pad, 96 bpm
  "cold-war"   tense ticking strings: staccato string ostinato, cello pedal, clock tick, 120 bpm
  "ufo"        eerie theremin (gliding vibrato sine) over hollow pads and a high shimmer, 72 bpm
  "ocean"      low drones, wave wash and sonar pings (faster into each reveal), 60 bpm
  "absurd"     mischievous pizzicato march: oom-pah pizz bass, bouncy staccato tune, woodblock, 126 bpm
  "science"    electric and bright: square-wave arpeggio, sub pulse, static crackle into reveals, 124 bpm
  "waltz"      eerie music-box waltz in 3/4 over oom-pah-pah plucks and a low drone, 150 bpm
  "detective"  lighter curious pizzicato: walking pizz bass, staccato pizz melody, snaps, 112 bpm
  "playful"    bright, light explainer pop (Q&A explainers): marimba motif + glock, soft kick, claps/snaps,
               off-beat hats + 16th shakers, bouncing bass, pumping pad; D major, 160 bpm; continuous (no
               drop-out: small risers + a bright chime on each reveal)

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


def _grid(total, bpm):
    beat = 60 / bpm
    bar = 4 * beat
    n = int((total + 2 * bar + 3) * SR)
    return beat, bar, n, np.arange(n) / SR, int(math.ceil((total + bar) / bar)) + 1


def cold_war(total, reveals, seed=3):
    """Tense ticking strings: a staccato string ostinato in sixteenths (bowed saws, short), a low cello
    pedal, a dry clock tick, a held high violin note that tightens into each reveal. 120 bpm, D minor."""
    beat, bar, n, t, nbar = _grid(total, 120.0)
    I = intensity(t, total, reveals)
    ost, cel, tk, hi = (np.zeros(n, np.float32) for _ in range(4))
    figure = [0, 3, 7, 3, 0, 3, 8, 3, 0, 3, 7, 3, 1, 3, 7, 3]   # minor, with a b2 / b6 rub
    for b in range(nbar):
        root = (62, 62, 58, 61)[b % 4]   # Dm Dm Bb C#dim colour
        t0 = b * bar
        for k, iv in enumerate(figure):
            m = int(beat / 4 * SR * 0.55)
            note = hz(root + iv)
            s = (saw(note, m, 0.003) + saw(note, m, -0.003)) * env_adsr(m, 0.006, 0.05, 0.5, 0.02)
            add(ost, s, t0 + k * beat / 4, 0.9 if k % 4 == 0 else 0.6)
        m = int(bar * SR)
        add(cel, saw(hz(root - 24), m) * env_adsr(m, 0.05, 0.2, 0.8, 0.1), t0)
        for k in range(4):
            add(tk, tick(0.02, 2400, seed=b * 4 + k), t0 + k * beat)
        add(hi, sine(hz(root + 24), m) * env_adsr(m, 0.4, 0.0, 1.0, 0.3), t0)
    ost, cel = lp_fast(ost, 3200), lp_fast(cel, 700)
    return ost * 0.32 * (0.6 + 0.6 * I) + cel * 0.35 + tk * 0.22 + hi * 0.05 * I, bar


def ufo(total, reveals, seed=4):
    """Eerie theremin and pads: a sine 'theremin' with slow vibrato gliding between notes of a whole-tone
    line, a hollow pad, a shimmering high cluster, 72 bpm."""
    beat, bar, n, t, nbar = _grid(total, 72.0)
    I = intensity(t, total, reveals)
    line = [69, 73, 71, 75, 69, 77, 73, 71]
    f = np.zeros(n, np.float32)
    for k in range(len(f) // int(bar / 2 * SR) + 2):
        a, z = int(k * bar / 2 * SR), int((k + 1) * bar / 2 * SR)
        f[a:z] = hz(line[k % len(line)])
    f = lp_fast(f, 1.6)   # portamento: glide between notes
    f = f * (1 + 0.012 * np.sin(2 * np.pi * 5.2 * t))   # vibrato
    ther = np.sin(2 * np.pi * np.cumsum(f) / SR).astype(np.float32)
    ther *= (0.55 + 0.45 * np.sin(2 * np.pi * t / (bar / 2) - np.pi / 2) ** 2).astype(np.float32)
    pad = np.zeros(n, np.float32)
    for b in range(nbar):
        m = int(bar * SR) + int(0.8 * SR)
        ch = sum(saw(hz(n_), m, d) for n_ in (45, 52, 55, 61) for d in (-0.003, 0.003))
        add(pad, ch * env_adsr(m, 1.2, 0, 1, 0.8) / 8, b * bar)
    pad = lp_fast(pad, 800)
    shimmer = sum(sine(hz(n_), n) for n_ in (93, 95, 98)) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * t)).astype(np.float32)
    return ther * 0.28 * (0.6 + 0.6 * I) + pad * 0.4 + shimmer * 0.015, bar


def ocean(total, reveals, seed=5):
    """Low drones and sonar pings: a deep two-note drone with slow swells, filtered-noise waves, a sonar ping
    (sine blip + long echo) every bar that comes faster into each reveal. 60 bpm."""
    beat, bar, n, t, nbar = _grid(total, 60.0)
    I = intensity(t, total, reveals)
    drone = (sine(hz(33), n) + 0.6 * sine(hz(40), n) + 0.3 * saw(hz(33), n)) * (0.7 + 0.3 * np.sin(2 * np.pi * t / 7))
    drone = lp_fast(drone.astype(np.float32), 300)
    waves = lp_fast(np.random.default_rng(seed).standard_normal(n).astype(np.float32), 500)
    waves *= (0.5 + 0.5 * np.sin(2 * np.pi * t / 5.5) ** 2).astype(np.float32)
    ping = np.zeros(n, np.float32)
    k = int(0.9 * SR)
    blip = sine(hz(91), k) * np.exp(-np.arange(k) / (SR * 0.12)).astype(np.float32)
    tt = 0.5
    while tt < total + bar:
        add(ping, blip, tt)
        for e in (0.45, 0.9, 1.35):   # echo
            add(ping, blip * 0.35 ** (e / 0.45), tt + e)
        near = any(0 < r - tt < 3.0 for r in reveals)
        tt += 0.9 if near else 2 * beat
    return drone * 0.55 + waves * 0.10 * (0.6 + I) + ping * 0.30, bar


def absurd(total, reveals, seed=6):
    """Mischievous pizzicato march: oom-pah pizz bass, a bouncy staccato major-key tune with a sneaky
    chromatic step, a woodblock on the off-beats, 126 bpm."""
    beat, bar, n, t, nbar = _grid(total, 126.0)
    I = intensity(t, total, reveals)
    low, mel, perc = (np.zeros(n, np.float32) for _ in range(3))
    tune = [7, None, 9, 10, 11, None, 12, None, 7, None, 4, None, 6, 7, None, None]
    for b in range(nbar):
        root = (48, 53, 55, 48)[b % 4]   # C F G C
        t0 = b * bar
        for k in range(4):
            note = root - 12 if k % 2 == 0 else root - 5
            add(low, pluck(hz(note), 0.4, 0.4, 0.992, seed=b * 4 + k), t0 + k * beat, 0.9)
        for k, iv in enumerate(tune):
            if iv is not None:
                add(mel, pluck(hz(root + 12 + iv), 0.2, 0.8, 0.983, seed=b * 16 + k), t0 + k * beat / 4, 0.6)
        for k in range(4):
            add(perc, bell(1200, 0.08) * 0.6, t0 + k * beat + beat / 2)
    return low * 0.7 + mel * (0.45 + 0.2 * I) + perc * 0.12, bar


def science(total, reveals, seed=7):
    """Electric and bright: a pulsing square-ish arpeggio in sixteenths (major 7ths), a sub pulse, and crackling
    static bursts that thicken into each reveal. 124 bpm."""
    beat, bar, n, t, nbar = _grid(total, 124.0)
    I = intensity(t, total, reveals)
    arp, sub = np.zeros(n, np.float32), np.zeros(n, np.float32)
    shape = [0, 4, 7, 11, 12, 11, 7, 4]
    for b in range(nbar):
        root = (60, 57, 65, 62)[b % 4]
        t0 = b * bar
        for k in range(16):
            m = int(beat / 4 * SR * 0.7)
            note = hz(root + shape[k % 8])
            sq = np.sign(sine(note, m)) * 0.5 + saw(note * 2, m) * 0.2
            add(arp, sq * env_adsr(m, 0.002, 0.04, 0.3, 0.02), t0 + k * beat / 4)
        for k in range(4):
            m = int(beat * SR * 0.6)
            add(sub, sine(hz(root - 24), m) * env_adsr(m, 0.005, 0.2, 0.3, 0.05), t0 + k * beat)
    arp = lp_fast(arp, 2600 + 0 * I.mean())
    rng = np.random.default_rng(seed)
    crackle = (rng.random(n) > 0.9993).astype(np.float32) * rng.standard_normal(n).astype(np.float32)
    crackle = crackle - lp_fast(crackle, 2000)
    return arp * 0.22 * (0.6 + 0.6 * I) + sub * 0.5 + crackle * 0.6 * I, bar


def waltz(total, reveals, seed=8):
    """Eerie dancing waltz (strange history): a minor music-box tune in 3/4 over oom-pah-pah plucks and a low
    drone; a little detuned, as if it won't stop. 150 bpm (3 beats a bar)."""
    beat = 60 / 150.0
    bar = 3 * beat
    n = int((total + 2 * bar + 3) * SR)
    t = np.arange(n) / SR
    I = intensity(t, total, reveals)
    low, box = np.zeros(n, np.float32), np.zeros(n, np.float32)
    tune = [12, 15, 14, 12, 11, 12, 7, 8, 7, 3, 2, 3]
    nbar = int(math.ceil((total + bar) / bar)) + 1
    for b in range(nbar):
        root = (57, 57, 52, 53)[(b // 2) % 4]   # Am Am E F
        t0 = b * bar
        add(low, pluck(hz(root - 24), 0.5, 0.35, 0.993, seed=b * 3), t0, 1.0)
        for k in (1, 2):
            add(low, pluck(hz(root - 12 + 7), 0.25, 0.5, 0.99, seed=b * 3 + k) * 0.5, t0 + k * beat)
            add(low, pluck(hz(root - 12 + 3), 0.25, 0.5, 0.99, seed=b * 3 + k + 50) * 0.4, t0 + k * beat)
        for k in range(3):
            iv = tune[(b * 3 + k) % len(tune)]
            note = hz(root + 12 + iv) * (1 + 0.004 * math.sin(b + k))   # slightly out of tune
            add(box, pluck(note, 0.6, 0.9, 0.996, seed=b * 7 + k), t0 + k * beat, 0.6)
    drone = lp_fast(saw(hz(33), n) * 0.5 + sine(hz(45), n), 250)
    return low * 0.6 + box * (0.35 + 0.25 * I) + drone * 0.25, bar


def sleep(total, reveals, seed=9):
    """Sleep compilations (C1 "Weird Animal Facts to Fall Asleep To"): a soft, slow pad and a warm noise wash,
    no beat, no hits. Three-note chords (Am9 -> Fmaj7 -> Cmaj7 -> G6) swell over 12 s each, low-passed, with a
    slow 'breathing' wash under them. Mixed very low under the voice (spec "music_lufs" about -34)."""
    n = int((total + 3) * SR)
    t = (np.arange(n) / SR).astype(np.float32)
    chords = [(57, 64, 71), (53, 60, 69), (48, 55, 64), (55, 62, 64)]
    pad = np.zeros(n, np.float32)
    seg = int(12 * SR)
    win = np.sin(np.linspace(0, np.pi, 2 * seg, dtype=np.float32)) ** 2   # overlapping 24 s swells
    for k, start in enumerate(range(-seg, n, seg)):
        notes = chords[k % len(chords)]
        a, z = max(0, start), min(n, start + 2 * seg)
        if z <= a:
            continue
        tt = t[a:z]
        tone = sum(np.sin(2 * np.pi * hz(m) * tt + j) + 0.3 * np.sin(2 * np.pi * hz(m) * 2.003 * tt) for j, m in enumerate(notes))
        pad[a:z] += (tone * win[a - start:z - start]).astype(np.float32)
    pad = lp_fast(pad, 900)
    wash = lp_fast(np.random.default_rng(seed).standard_normal(n).astype(np.float32), 350)
    wash *= (0.55 + 0.45 * np.sin(2 * np.pi * t / 9.0) ** 2).astype(np.float32)   # slow breathing
    return pad * 0.5 + wash * 0.18, 12.0


def marimba(f, dur=0.5, bright=1.0, seed=0):
    """Mallet: a sine with a marimba's tuned upper partials (x3.93, x9.2) that die fast, and a soft mallet click."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    d = 5.0 + f / 140.0                       # higher bars ring shorter
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t * d)
         + 0.30 * bright * np.sin(2 * np.pi * f * 3.93 * t) * np.exp(-t * d * 3.2)
         + 0.08 * bright * np.sin(2 * np.pi * f * 9.2 * t) * np.exp(-t * d * 6.5))
    k = int(0.004 * SR)
    s[:k] += np.random.default_rng(seed).standard_normal(k) * np.exp(-np.arange(k) / (SR * 0.0007)) * 0.18 * bright
    return (s * env_adsr(n, 0.0015, 0, 1, 0.02)).astype(np.float32)


def soft_kick(dur=0.26):
    """A short, round kick (pitch drops 160 -> 56 Hz) with a little beater click: punch without sub weight."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 56 + 104 * np.exp(-t * 40)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 17)
    k = int(0.003 * SR)
    s[:k] += np.random.default_rng(5).standard_normal(k) * np.exp(-np.arange(k) / (SR * 0.0006)) * 0.25
    return (s * env_adsr(n, 0.002, 0, 1, 0.03)).astype(np.float32)


def env_train(n, hits, attack, decay):
    """Sum of attack/exp-decay envelopes at (time, gain) hits: one buffer for a whole noise-percussion voice."""
    e = np.zeros(n, np.float32)
    k = int((attack + 6 * decay) * SR)
    tt = np.arange(k) / SR
    shape = (np.minimum(1, tt / max(attack, 1e-4)) * np.exp(-np.maximum(0, tt - attack) / decay)).astype(np.float32)
    for t0, g in hits:
        add(e, shape, t0, g)
    return e


# playful: I - vi - IV - V in D major, one chord a bar (8 eighth-note slots per bar; None = rest)
PL_CHORDS = [(38, (62, 66, 69)), (35, (62, 66, 71)), (43, (62, 67, 71)), (45, (61, 64, 69))]   # D Bm G A
PL_PAD = [(54, 57, 62, 66), (54, 59, 62, 66), (55, 59, 62, 67), (52, 57, 61, 64)]   # warm low voicings
PL_A = [[69, None, 74, 69, 71, None, 69, 66], [66, None, 64, 66, 69, None, None, None],
        [67, None, 71, 67, 74, None, 73, 71], [69, 71, 69, 66, 64, None, None, None],
        [69, None, 74, 69, 71, None, 69, 66], [66, None, 64, 66, 69, None, None, None],
        [67, None, 71, 67, 74, None, 73, 71], [71, 73, 74, None, 78, None, 76, None]]
PL_B = [[None, 62, 66, 69, None, 69, 71, 69], [66, None, 62, None, 64, 66, 62, None],
        [None, 59, 62, 67, None, 67, 69, 71], [69, None, 64, None, 61, None, 64, None],
        [None, 62, 66, 69, None, 69, 71, 69], [66, None, 69, None, 71, 69, 66, None],
        [67, 69, 71, None, 74, None, 71, None], [73, None, 69, None, 67, 66, 64, 61]]


PL_MIX = dict(mel=0.70, glk=0.39, cnt=1.45, bass=0.20, pad=0.76, kick=0.65, clap=1.57, snap=1.24, hat=0.50,
              shaker=0.22, riser=0.70)   # stem gains, tuned so the bed's spectrum matches the reference brightness


def playful(total, reveals, seed=10):
    """Playful, light, curious explainer pop: a catchy 4-bar marimba motif (answered and varied every 8 bars,
    a glockenspiel doubling and a plucked counter-line join as it builds), soft kick on 1 and 3, clap + snap on
    2 and 4, bright off-beat hats and 16th shakers, a warm round bouncing bass, a gentle pumping chord pad.
    Major key (D), ~160 bpm (80 half-time feel), nudged so the clip is a whole number of bars: the loop
    crossfade then lands on the beat (no flams at the seam), and the bars past the end replay bar 0 (same chord,
    motif and hat noise), so the seam blends the top into itself. Continuous: small risers (noise swell + a
    mallet run up the scale) lift into each reveal, but it never drops out (render() skips the drop for this
    kind and limits its rare stacked peaks, so it lands near -18 LUFS)."""
    bars = max(1, round(total / (240.0 / 160.0)))
    beat, bar, n, t, nbar = _grid(total, bars * 240.0 / total)
    e8 = beat / 2
    I = intensity(t, total, reveals)
    clap_h, snap_h, hat_h, shk_h = [], [], [], []
    mel, glk, cnt, bass, pd, kk = (np.zeros(n, np.float32) for _ in range(6))
    for b in range(nbar):
        t0 = b * bar
        bb = b % bars                             # bars past the end replay the top: the loop crossfade blends
        root, triad = PL_CHORDS[bb % 4]           # bar 0 into bar 0 (same chord + motif), no A-over-D smear
        voicing = PL_PAD[bb % 4]
        sec = bb // 8
        frac = (sec * 8 * bar) / max(total, 1e-6)
        motif = (PL_A, PL_B)[sec % 2][bb % 8]
        lift = 0.2 <= frac < 0.85                 # middle sections: glock doubling
        counter = 0.4 <= frac < 0.85              # later still: plucked counter-line
        for k, m in enumerate(motif):
            if m is None:
                continue
            ts = t0 + k * e8
            v = 0.95 if k % 2 == 0 else 0.75
            add(mel, marimba(hz(m), 0.55, 1.0, seed=bb * 8 + k), ts, v)
            if sec % 2 and k + 1 < 8 and motif[k + 1] is None:          # variation: a bouncy 16th repeat
                add(mel, marimba(hz(m), 0.3, 0.8, seed=bb * 8 + k + 99), ts + e8 / 2, 0.4)
            if lift:
                add(glk, bell(hz(m + 24), 0.5), ts, 0.5 * v)
        if counter:                                # plucked arpeggio of the chord on the off-beats
            for k in (1, 3, 5, 7):
                note = triad[(k // 2) % 3] + 12
                add(cnt, pluck(hz(note), 0.3, 0.55, 0.988, seed=bb * 4 + k), t0 + k * e8, 0.5)
        for k, iv, d in ((0, 0, 0.34), (3, 0, 0.16), (4, 7, 0.32), (6, 12, 0.15)):   # bouncy root-fifth-octave
            m = int(d * SR)
            f = hz(root + iv)
            s = sine(f, m) + 0.5 * sine(2 * f, m) + 0.2 * sine(3 * f, m)
            add(bass, s * env_adsr(m, 0.006, 0.12, 0.6, 0.04), t0 + k * e8, 1.0 if k in (0, 4) else 0.75)
        m = int(bar * SR) + int(0.3 * SR)          # pad: detuned saws on the chord, softly low-passed
        ch = sum(saw(hz(x), m, dt) for x in voicing for dt in (-0.0035, 0.003))
        add(pd, ch * env_adsr(m, 0.12, 0.0, 1.0, 0.3) / 8, t0)
        for k in (0, 4):
            add(kk, soft_kick(), t0 + k * e8)
        for k in (2, 6):
            clap_h += [(t0 + k * e8 + j * 0.009, (1.0, 0.7, 0.85)[j]) for j in range(3)]
            snap_h.append((t0 + k * e8, 1.0))
        if bb % 8 == 7 or bb == bars - 1:          # little fill into the next 8 bars (and back to the top)
            snap_h += [(t0 + 6 * e8 + e8 / 2, 0.6), (t0 + 7 * e8, 0.75), (t0 + 7 * e8 + e8 / 2, 0.9)]
        for k in range(8):
            hat_h.append((t0 + k * e8, 1.0 if k % 2 else 0.45))
        for k in range(16):
            shk_h.append((t0 + k * e8 / 2, (0.55, 0.3, 0.85, 0.3)[k % 4]))
    rng = np.random.default_rng(seed)
    wn = rng.standard_normal(n).astype(np.float32)
    wn = wn[np.arange(n) % max(1, int(round(total * SR)))]   # noise repeats each clip: the seam fades hat into the
    hp7 = wn - lp_fast(wn, 7000)                              # same hat (no uncorrelated-noise -3 dB dip)
    bp = lp_fast(wn, 7500) - lp_fast(wn, 2600)
    cl = lp_fast(lp_fast(wn, 3000), 3000) - lp_fast(wn, 800)
    hats = hp7 * env_train(n, hat_h, 0.0008, 0.018)
    shaker = bp * env_train(n, shk_h, 0.006, 0.022)
    claps = cl * env_train(n, clap_h, 0.0006, 0.028)
    snaps = (lp_fast(wn, 6000) - lp_fast(wn, 1800)) * env_train(n, snap_h, 0.0004, 0.008)
    # gentle sidechain pump on the pad and bass from the kick
    pump = 1 - 0.3 * env_train(n, [(b * bar + k * e8, 1.0) for b in range(nbar) for k in (0, 4)], 0.004, 0.11)
    pd = lp_fast(lp_fast(pd, 1600), 2400) * pump
    bass = lp_fast(bass, 900) * (0.6 + 0.4 * pump)
    riser = np.zeros(n, np.float32)
    for r in reveals:                              # swell of brightening noise + a quantized mallet run up into it
        a, z = int(max(0, r - 2.0) * SR), int(r * SR)
        if z > a:
            u = np.linspace(0, 1, z - a, dtype=np.float32)
            riser[a:z] += (lp_fast(wn[a:z], 1500) * (1 - u) + hp7[a:z] * 2.2 * u) * u ** 2 * 0.5
        end = math.floor(r / (e8 / 2) + 1e-6) * (e8 / 2)
        for j, m in enumerate((62, 64, 66, 67, 69, 71, 73, 74)):
            add(mel, marimba(hz(m + 12), 0.25, 0.9, seed=int(r * 10) + j), end - (8 - j) * e8 / 2, 0.35 + 0.05 * j)
    d = int(3 * e8 / 2 * SR)                       # dotted-8th echo on the mallets fills the motif's rests
    echo = np.zeros(n, np.float32)
    echo[d:] += mel[:-d] * 0.32
    echo[2 * d:] += mel[:-2 * d] * 0.14
    mel = mel + lp_fast(echo, 6000)
    perc_I = 0.75 + 0.35 * I
    stems = dict(mel=mel, glk=glk, cnt=cnt, bass=bass, pad=pd, kick=kk, clap=claps, snap=snaps, hat=hats * perc_I,
                 shaker=shaker * perc_I, riser=riser)
    return sum(stems[k] * g for k, g in PL_MIX.items()), bar


PLAYFUL_HIT = 86   # D6: the bright reveal chime for the playful bed


def hit_sound(kind):
    """The payoff hit on each reveal: low boom + bell (dark beds) or a bright chime + soft kick (playful)."""
    if kind in CONTINUOUS:
        n = int(1.6 * SR)
        air = np.random.default_rng(11).standard_normal(n).astype(np.float32)
        air = (air - lp_fast(air, 6000)) * np.exp(-np.arange(n) / (SR * 0.35)).astype(np.float32)
        s = np.zeros(n, np.float32)
        add(s, bell(hz(HIT[kind]), 1.4) * 0.22 + bell(hz(HIT[kind] + 7), 1.4) * 0.12, 0)
        add(s, soft_kick() * 0.5, 0)
        return s + air * 0.05
    return boom(1.4) * 0.55 + bell(hz(HIT[kind])) * 0.25


CONTINUOUS = {"playful"}   # beds that never drop out before a reveal (continuous explainer bed)
PL_CREST = 17.0            # dB peak over RMS a continuous bed is limited to: ~-18 LUFS once normalised to 0.7 peak


def limit(x, crest_db=PL_CREST, max_gr_db=4.0, look=0.003, release=0.06):
    """Transparent lookahead peak limiter (1 ms blocks, circular so the loop seam sees the same gain on both
    sides): shaves the rare stacked peaks (kick + clap + mallet run into a reveal) down to `crest_db` over the
    RMS, at most `max_gr_db`, so a peak-normalised continuous bed is not quiet."""
    ceil_ = max(float(np.sqrt(np.mean(x ** 2))) * 10 ** (crest_db / 20), float(np.abs(x).max()) * 10 ** (-max_gr_db / 20))
    blk = int(0.001 * SR)
    nb = -(-len(x) // blk)
    pk = np.abs(np.pad(x, (0, nb * blk - len(x)))).reshape(nb, blk).max(1)
    g = np.minimum(1.0, ceil_ / (pk + 1e-12))
    L = max(1, int(round(look / 0.001)))
    g = np.lib.stride_tricks.sliding_window_view(np.pad(g, L, mode="wrap"), 2 * L + 1).min(1)
    a = 1 - math.exp(-0.001 / release)           # release: recover towards 1, never above the needed gain
    gl, prev = g.tolist(), 1.0
    for _ in range(2):                           # second lap starts from the loop end's state
        for i, v in enumerate(gl):
            prev = gl[i] = min(v, prev + (1 - prev) * a)
    g = np.array(gl)
    w = 2 * L + 1                                # box no wider than the min window: peaks keep their full reduction
    g = np.convolve(np.pad(g, w // 2, mode="wrap"), np.ones(w) / w, "valid")
    gs = np.interp(np.arange(len(x)), np.arange(nb) * blk + blk / 2, g)
    return (x * gs).astype(np.float32)

BEDS = {"sleep": sleep, "waltz": waltz, "mystery": mystery, "conspiracy": mystery, "detective": detective, "cold-war": cold_war, "ufo": ufo,
        "ocean": ocean, "absurd": absurd, "science": science, "playful": playful}
VERB = {"sleep": (3.5, 0.45), "waltz": (2.0, 0.28), "mystery": (2.4, 0.30), "conspiracy": (2.4, 0.30), "ufo": (3.0, 0.40), "ocean": (3.2, 0.38),
        "cold-war": (1.4, 0.18), "detective": (1.2, 0.18), "absurd": (0.9, 0.12), "science": (1.2, 0.18),
        "playful": (1.0, 0.14)}
HIT = {"sleep": 69, "waltz": 81, "mystery": 81, "conspiracy": 81, "detective": 74, "cold-war": 74, "ufo": 85, "ocean": 79, "absurd": 84,
       "science": 88, "playful": PLAYFUL_HIT}


def render(kind, total, reveals=(), out=None, turn=None, turn_kind="mystery", drop=True, hit=True):
    """The bed as stereo float32 (n, 2) at SR, exactly `total` s long, loop-safe; written to `out` if given.
    drop/hit = False: the reveals only raise the build (no drop-out before them, no boom + bell on them).
    CONTINUOUS kinds ("playful") never drop out, and their hit is a bright chime instead of the boom.
    turn = seconds of the story's dark turn: a comic bed ("absurd", "waltz", "detective") crossfades over 1 s into
    the tense `turn_kind` bed there (Voggle shape, research/40: comic until the story turns dark)."""
    reveals = sorted(r for r in reveals if 0.5 < r < total)
    mix, bar = BEDS[kind](total, reveals)
    mix = reverb(mix, *VERB[kind])
    if turn is not None and 0 < turn < total and turn_kind != kind:
        dark, _ = BEDS[turn_kind](total, reveals)
        dark = reverb(dark, *VERB[turn_kind])
        m = min(len(mix), len(dark))
        w = np.clip((np.arange(m) / SR - turn) / 1.0, 0, 1).astype(np.float32)
        rms = lambda x: float(np.sqrt(np.mean(x ** 2)) + 1e-9)
        mix = mix[:m] * (1 - w) + dark[:m] * w * (rms(mix[:m]) / rms(dark[:m]))
    N = int(total * SR)
    xf = int(min(1.2, total / 6) * SR)
    sig = mix[:N + xf].copy()
    t = np.arange(len(sig)) / SR
    if drop and kind not in CONTINUOUS:
        sig *= gaps(t, reveals)
    hs = hit_sound(kind) if hit else None
    for r in (reveals if hit else ()):   # the payoff hit: low boom + a bell a fifth over the key (or a chime)
        add(sig, hs, r)
    ramp = np.linspace(0, 1, xf, dtype=np.float32)   # loop: the tail fades into the head
    head = sig[:xf] * ramp + sig[N:N + xf] * (1 - ramp)
    sig = sig[:N]
    sig[:xf] = head
    if kind in CONTINUOUS:                           # no drop-outs = less headroom needed: limit the stacked peaks
        sig = limit(sig)
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
    if len(sys.argv) < 4 or sys.argv[1] not in BEDS:
        sys.exit("usage: music.py KIND SECONDS OUT.wav [reveal_s ...]   kinds: " + " ".join(sorted(BEDS)))
    kind, secs, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
    render(kind, secs, [float(x) for x in sys.argv[4:]], out)   # (no dark turn from the CLI)
    print("ok", out)
