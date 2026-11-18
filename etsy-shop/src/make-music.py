"""Original synthesized arrangements of public-domain melodies (royalty-free, safe for ads).
- jingle.wav : "Jingle Bells" (J. Pierpont, 1857 — public domain) with glockenspiel, bass, sleigh bells
- planner.wav: original light pop chord loop (no melody borrowed)
"""
import numpy as np, wave, os
SR = 44100
OUT = os.path.join(os.path.dirname(__file__), "..", "tiktok")
os.makedirs(OUT, exist_ok=True)
NOTE = {n: i for i, n in enumerate("C C# D D# E F F# G G# A A# B".split())}
def hz(n, octv): return 440 * 2 ** ((NOTE[n] + 12 * (octv + 1) - 69) / 12)

def tone(f, dur, kind="glock", amp=0.3):
    t = np.arange(int(SR * dur)) / SR
    if kind == "glock":   # bright bell: fundamental + inharmonic partials, fast decay
        w = np.sin(2*np.pi*f*t) + .4*np.sin(2*np.pi*f*2.76*t)*np.exp(-t*9) + .2*np.sin(2*np.pi*f*5.4*t)*np.exp(-t*14)
        env = np.exp(-t * 3.2)
    elif kind == "bass":
        w = np.sin(2*np.pi*f*t) + .3*np.sin(2*np.pi*2*f*t)
        env = np.minimum(1, t*40) * np.exp(-t * 2.5)
    elif kind == "pad":
        w = sum(np.sin(2*np.pi*f*k*t)/k for k in (1, 2, 3))
        env = np.minimum(1, t*6) * np.exp(-t*1.2)
    else:  # piano-ish
        w = np.sin(2*np.pi*f*t) + .5*np.sin(2*np.pi*2*f*t)*np.exp(-t*3) + .25*np.sin(2*np.pi*3*f*t)*np.exp(-t*5)
        env = np.minimum(1, t*200) * np.exp(-t * 2.8)
    return amp * w * env

def bells(dur, amp=0.12, seed=0):  # sleigh-bell shake: filtered noise burst
    rng = np.random.default_rng(seed)
    n = int(SR * dur); t = np.arange(n) / SR
    x = rng.standard_normal(n)
    x = x - np.concatenate([[0], x[:-1]])          # crude high-pass
    x = x * np.abs(np.sin(2*np.pi*55*t))            # shimmer
    return amp * x * np.exp(-t * 18)

def place(buf, sig, start):
    i = int(start * SR); j = min(len(buf), i + len(sig))
    if i < len(buf): buf[i:j] += sig[:j - i]

def write(name, x):
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.85
    fade = int(SR * 1.2); x[-fade:] *= np.linspace(1, 0, fade)
    st = np.stack([x, np.roll(x, 220)], 1)          # tiny stereo widening
    with wave.open(os.path.join(OUT, name), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())

# ---------- Jingle Bells chorus (public domain) ----------
BEAT = 60 / 168
mel = ("E1 E1 E2 E1 E1 E2 E1 G1 C1.5 D.5 E4 "
       "F1 F1 F1.5 F.5 F1 E1 E1 E.5 E.5 E1 D1 D1 E1 D2 G2 "
       "E1 E1 E2 E1 E1 E2 E1 G1 C1.5 D.5 E4 "
       "F1 F1 F1.5 F.5 F1 E1 E1 E.5 E.5 G1 G1 F1 D1 C4").split()
chords = "C C C C F C G G C C C C F C G C".split()   # one per bar
total = 64 * BEAT
x = np.zeros(int(SR * (total + 2)))
t = 0.0
for tok in mel:
    n, d = tok[0], float(tok[1:])
    octv = 6 if n == "C" and tok in ("C1.5", "C4") else 5
    place(x, tone(hz(n, octv), d*BEAT + .6, "glock", .32), t)
    t += d * BEAT
ROOT = {"C": ("C", "E", "G"), "F": ("F", "A", "C"), "G": ("G", "B", "D")}
for bar, ch in enumerate(chords):
    b0 = bar * 4 * BEAT
    r, th, fi = ROOT[ch]
    for k, nn in enumerate([r, fi, r, fi]):          # oom-pah bass
        place(x, tone(hz(nn, 2), BEAT*.9, "bass", .35), b0 + k*BEAT)
    for k in (1, 3):                                  # off-beat chord stabs
        for nn in (r, th, fi):
            place(x, tone(hz(nn, 4), BEAT*.5, "piano", .07), b0 + k*BEAT)
for k in range(64 * 2):                               # sleigh bells on 8ths
    place(x, bells(.25, .10 if k % 2 == 0 else .06, k), k * BEAT / 2)
write("jingle.wav", x)

# ---------- Planner: original upbeat loop ----------
BEAT = 60 / 112
prog = [("C", "E", "G", "B"), ("A", "C", "E", "G"), ("F", "A", "C", "E"), ("G", "B", "D", "F")]
y = np.zeros(int(SR * (BEAT * 32 + 2)))
for bar in range(8):
    ch = prog[bar % 4]; b0 = bar * 4 * BEAT
    for k in range(8):                                 # arpeggio 8ths
        nn = ch[[0, 1, 2, 3, 2, 1, 2, 3][k]]
        place(y, tone(hz(nn, 5), BEAT*.8, "piano", .16), b0 + k*BEAT/2)
    place(y, tone(hz(ch[0], 2), BEAT*4, "bass", .3), b0)
    for nn in ch[:3]:
        place(y, tone(hz(nn, 4), BEAT*4, "pad", .04), b0)
    for k in range(4):                                 # soft shaker
        place(y, bells(.12, .05, bar*8 + k), b0 + k*BEAT + BEAT/2)
write("planner.wav", y)
print("ok")

# ---------- v3: punchy 180-BPM "Jingle Bells" (public domain) for fast-cut ads ----------
# 1 beat = 1/3 s, so a 4-beat scene = 1.333 s; beat 0 lands at t=0 (renderer syncs zoom punches to it).
def kick(amp=.9):
    t = np.arange(int(SR*.28))/SR
    f = 50 + 110*np.exp(-t*30)
    return amp*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*11)
def clap(amp=.35, seed=1):
    rng = np.random.default_rng(seed); n = int(SR*.18); t = np.arange(n)/SR
    x = rng.standard_normal(n); x = x - np.concatenate([[0], x[:-1]])
    env = np.exp(-t*28) + .6*np.exp(-np.maximum(0, t-.012)*30)*(t > .012)
    return amp*x*env
def hat(amp=.08, seed=2):
    rng = np.random.default_rng(seed); n = int(SR*.05); t = np.arange(n)/SR
    x = rng.standard_normal(n); x = x - np.concatenate([[0], x[:-1]])
    return amp*x*np.exp(-t*90)

BEAT = 60 / 180
total = 64 * BEAT
z = np.zeros(int(SR * (total + 2)))
t = 0.0
for tok in mel:
    n, d = tok[0], float(tok[1:])
    octv = 6 if n == "C" and tok in ("C1.5", "C4") else 5
    place(z, tone(hz(n, octv), d*BEAT + .4, "glock", .30), t)
    place(z, tone(hz(n, octv+1), d*BEAT*.6, "glock", .06), t)        # sparkle double
    t += d * BEAT
for bar, ch in enumerate(chords):
    b0 = bar * 4 * BEAT
    r, th, fi = ROOT[ch]
    for k in range(8):                                               # pumping octave bass 8ths
        place(z, tone(hz(r, 2 + (k % 2)), BEAT*.45, "bass", .30), b0 + k*BEAT/2)
    for k in range(4):
        place(z, kick(), b0 + k*BEAT)                                # four on the floor
        if k in (1, 3): place(z, clap(seed=bar*4+k), b0 + k*BEAT)    # claps on 2 and 4
        for nn in (r, th, fi):                                       # off-beat stabs
            place(z, tone(hz(nn, 4), BEAT*.3, "piano", .05), b0 + k*BEAT + BEAT/2)
    for k in range(8): place(z, hat(seed=bar*8+k), b0 + k*BEAT/2 + BEAT/4)
for k in range(64 * 2):
    place(z, bells(.2, .07 if k % 2 == 0 else .04, k), k * BEAT / 2)
write("jingle-punch.wav", z)

# ---------- v3 sound effects (mixed in at cuts / moments by build-tiktok-anim.js) ----------
def write_sfx(name, x):
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.9
    st = np.stack([x, x], 1)
    with wave.open(os.path.join(OUT, name), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())
rng = np.random.default_rng(7)
n = int(SR*.35); tt = np.arange(n)/SR                                # whoosh: noise swell, rising tone
wh = rng.standard_normal(n); wh = np.convolve(wh, np.ones(12)/12, "same")
write_sfx("sfx-whoosh.wav", wh*np.sin(np.pi*tt/.35)**2 + .15*np.sin(2*np.pi*np.cumsum(300+1500*tt/.35)/SR)*np.sin(np.pi*tt/.35))
n = int(SR*.12); tt = np.arange(n)/SR                                # pop: pitch-dropping blip
write_sfx("sfx-pop.wav", np.sin(2*np.pi*np.cumsum(900-600*tt/.12)/SR)*np.exp(-tt*30))
n = int(SR*1.0); tt = np.arange(n)/SR                                # ding: two bright bells (price reveal)
write_sfx("sfx-ding.wav", tone(hz("E", 6), 1.0, "glock", .5)[:n] + np.concatenate([np.zeros(int(SR*.09)), tone(hz("B", 6), 1.0, "glock", .5)])[:n])
n = int(SR*.6); tt = np.arange(n)/SR                                 # boom: sub drop + noise hit (hook)
write_sfx("sfx-boom.wav", np.sin(2*np.pi*np.cumsum(40+140*np.exp(-tt*9))/SR)*np.exp(-tt*5) + .4*rng.standard_normal(n)*np.exp(-tt*25))
print("ok v3")
