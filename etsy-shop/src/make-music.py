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

# =====================================================================================
# Nov 19 "variety pack": a DIFFERENT soundtrack per video format. Everything below is either an
# original composition or our own arrangement of a public-domain composition (no recordings used).
#   xmas-lofi.wav      original cozy lo-fi Christmas beat (Rhodes chords, swung hats, vinyl, bells)  -> texting Santa
#   xmas-popdrums.wav  original upbeat pop (four-on-floor, claps, synth stabs, pluck hook)            -> Notes checklist
#   xmas-pizzicato.wav original playful/comedic pizzicato + woodblock                                -> rating meter
#   xmas-wewish.wav    "We Wish You a Merry Christmas" (trad. English carol, PD), brass-ish waltz    -> comment reply
#   xmas-musicbox.wav  "Silent Night" (F. Gruber 1818, PD), slow music-box lullaby                   -> fireplace
#   xmas-deckhalls.wav "Deck the Halls" (trad. Welsh, PD), ukulele strum + glock + snaps             -> elf day-in-life
#   xmas-gameshow.wav  original game-show quiz loop (square lead, tick-tock)                         -> naughty/nice quiz
#   xmas-toymarimba.wav original toy-piano/marimba bounce                                            -> paper stop-motion
#   calm-acoustic.wav  original fingerpicked acoustic guitar (sage, non-Christmas)                   -> 2027 wall calendar
#   calm-lofirain.wav  original mellow lo-fi with soft rain (non-Christmas)                          -> budget planner
#   calm-piano.wav     original soft felt-piano (non-Christmas)                                      -> 2027 planner
# =====================================================================================
def lp(x, k=6):                                       # cheap low-pass (moving average)
    return np.convolve(x, np.ones(k)/k, "same")
def pluck(f, dur, amp=.3, damp=.994, bright=.5, seed=0):   # Karplus-Strong string (period-vectorised)
    rng = np.random.default_rng(seed); N = max(2, int(SR/f)); n = int(SR*dur)
    y = rng.uniform(-1, 1, N); y = bright*y + (1-bright)*np.convolve(y, np.ones(3)/3, "same"); out = []
    while sum(len(o) for o in out) < n:
        out.append(y); y = damp*.5*(y + np.roll(y, 1))
    x = np.concatenate(out)[:n]; t = np.arange(n)/SR
    return amp*x*np.minimum(1, t*300)
def inst(f, dur, kind, amp=.3):
    t = np.arange(int(SR*dur))/SR
    if kind == "rhodes":
        w = np.sin(2*np.pi*f*t + .8*np.sin(2*np.pi*f*t)*np.exp(-t*3)) * (1 + .15*np.sin(2*np.pi*4.5*t))
        env = np.minimum(1, t*80)*np.exp(-t*1.6)
    elif kind == "musicbox":
        w = np.sin(2*np.pi*f*t) + .35*np.sin(2*np.pi*f*4.02*t)*np.exp(-t*6) + .12*np.sin(2*np.pi*f*7.1*t)*np.exp(-t*12)
        env = np.minimum(1, t*400)*np.exp(-t*2.2)
    elif kind == "marimba":
        w = np.sin(2*np.pi*f*t) + .25*np.sin(2*np.pi*f*3.93*t)*np.exp(-t*20)
        env = np.minimum(1, t*500)*np.exp(-t*7)
    elif kind == "square":
        w = np.sign(np.sin(2*np.pi*f*t))*.5 + .5*np.sin(2*np.pi*f*t)
        env = np.minimum(1, t*200)*np.exp(-t*4)
    elif kind == "brass":
        w = sum(np.sin(2*np.pi*f*k*t)/k**1.2 for k in range(1, 7))
        env = np.minimum(1, t*25)*np.exp(-t*1.8)
    elif kind == "saw":
        w = sum(np.sin(2*np.pi*f*k*t)/k for k in range(1, 9))
        env = np.minimum(1, t*300)*np.exp(-t*6)
    elif kind == "felt":
        w = np.sin(2*np.pi*f*t) + .3*np.sin(2*np.pi*2*f*t)*np.exp(-t*4) + .08*np.sin(2*np.pi*3*f*t)*np.exp(-t*6)
        env = np.minimum(1, t*60)*np.exp(-t*1.4)
    else:
        return tone(f, dur, kind, amp)
    return amp*w*env
def snare(amp=.3, seed=3):
    rng = np.random.default_rng(seed); n = int(SR*.2); t = np.arange(n)/SR
    return amp*(rng.standard_normal(n)*np.exp(-t*22) + .5*np.sin(2*np.pi*190*t)*np.exp(-t*30))
def woodblock(f=900, amp=.35):
    t = np.arange(int(SR*.08))/SR
    return amp*np.sin(2*np.pi*f*t)*np.exp(-t*60)
def snap(amp=.3, seed=4):
    rng = np.random.default_rng(seed); n = int(SR*.06); t = np.arange(n)/SR
    x = rng.standard_normal(n); x = x - np.concatenate([[0], x[:-1]])
    return amp*x*np.exp(-t*80)
def vinyl(dur, amp=.05, seed=11):
    rng = np.random.default_rng(seed); n = int(SR*dur)
    x = lp(rng.standard_normal(n), 30)*.3
    pops = (rng.random(n) < 4/SR)*rng.uniform(.4, 1, n)
    return amp*(x + np.convolve(pops, np.exp(-np.arange(60)/8), "same"))
def rain(dur, amp=.06, seed=12):
    rng = np.random.default_rng(seed); n = int(SR*dur); x = rng.standard_normal(n)
    x = x - lp(x, 40)                                 # hiss band
    drops = (rng.random(n) < 30/SR)*rng.uniform(.2, 1, n)
    return amp*(.4*x + np.convolve(drops, np.exp(-np.arange(200)/20)*np.sin(np.arange(200)*.9), "same"))
def chord_notes(name, octv):
    Q = {"maj7": (0, 4, 7, 11), "m7": (0, 3, 7, 10), "7": (0, 4, 7, 10), "maj": (0, 4, 7), "m": (0, 3, 7), "add9": (0, 4, 7, 14), "sus": (0, 5, 7)}
    root = name[:2] if len(name) > 1 and name[1] == "#" else name[:1]; q = name[len(root):] or "maj"
    base = NOTE[root] + 12*(octv+1)
    return [440*2**((base+i-69)/12) for i in Q[q]]
def mf(n):   # "E5" / "C#4" -> Hz
    return hz(n[:-1], int(n[-1]))
def melody(buf, seq, beat, kind, amp, t0=0.0, octshift=0, sustain=.3):
    t = t0
    for tok in seq.split():
        n, d = tok.split(":"); d = float(d)
        if n != "r":
            f = mf(n)*2**octshift
            sig = pluck(f, d*beat+sustain, amp) if kind == "pluck" else inst(f, d*beat+sustain, kind, amp)
            place(buf, sig, t)
        t += d*beat
    return t
def loop_to(x, secs):
    n = int(SR*secs); reps = int(np.ceil(n/len(x)))
    return np.tile(x, reps)[:n]

LEN = 34.0   # every track covers the longest video (+ margin)

# ---- 1. cozy lo-fi Christmas (original): 78 BPM, Rhodes 7ths, swung hats, vinyl, sleigh-bell shimmer
B = 60/78; prog = ["Fmaj7", "Em7", "Dm7", "Cmaj7"]; x = np.zeros(int(SR*(16*B+2)))
for bar, c in enumerate(prog):
    b0 = bar*4*B
    for k, f in enumerate(chord_notes(c, 3)): place(x, inst(f, 3.6*B, "rhodes", .13), b0 + k*.012)
    place(x, inst(chord_notes(c, 1)[0], 3*B, "bass", .35) if False else tone(chord_notes(c, 1)[0], 3*B, "bass", .35), b0)
    for k in range(4):
        place(x, kick(.6), b0 + k*B) if k in (0, 2) or (k == 3 and bar % 2) else None
        if k in (1, 3): place(x, lp(snare(.22, bar*4+k), 4), b0 + k*B)
        for s in (0, .62): place(x, hat(.05, bar*8+k), b0 + k*B + s*B)
    place(x, bells(.4, .05, bar), b0 + 3.5*B)
mel = "A5:1.5 G5:.5 E5:1 r:1 G5:1.5 E5:.5 D5:2 F5:1.5 E5:.5 C5:1 r:1 D5:.75 E5:.75 G5:2.5"
melody(x, mel, B, "musicbox", .10)
x = lp(x, 5) + vinyl(len(x)/SR, .05)
write("xmas-lofi.wav", loop_to(x[:int(SR*16*B)], LEN))

# ---- 2. upbeat pop drums (original): 124 BPM, I-V-vi-IV in G, saw stabs, pluck hook, claps
B = 60/124; prog = ["G", "D", "Em", "C"]; x = np.zeros(int(SR*(32*B+2)))
for bar in range(8):
    c = prog[bar % 4]; b0 = bar*4*B; cn = chord_notes(c if len(c) > 1 else c, 4)
    for k in range(4):
        place(x, kick(.8), b0 + k*B)
        if k in (1, 3): place(x, clap(.4, bar*4+k), b0 + k*B); place(x, snare(.15, bar*4+k), b0 + k*B)
        for s in (.5,): place(x, hat(.09, bar*8+k), b0 + k*B + s*B)
        for f in cn: place(x, inst(f, .35*B, "saw", .045), b0 + k*B + .5*B)
    for k in range(8): place(x, tone(chord_notes(c, 1)[0]*(2 if k % 2 else 1), .45*B, "bass", .28), b0 + k*B/2)
hook = "B5:.5 D6:.5 B5:.5 A5:.5 G5:1 r:1 A5:.5 B5:.5 A5:.5 F#5:.5 D5:2 E5:.5 G5:.5 B5:.5 G5:.5 E5:1 r:1 C6:.5 B5:.5 A5:.5 G5:.5 A5:2"
melody(x, hook + " " + hook, B, "pluck", .22)
write("xmas-popdrums.wav", loop_to(x[:int(SR*32*B)], LEN))

# ---- 3. playful pizzicato (original): 116 BPM, sneaky staccato strings + woodblock + bassoon-ish bass
B = 60/116; x = np.zeros(int(SR*(32*B+2)))
line = ("C5:.5 r:.5 E5:.5 r:.5 G5:.5 F5:.5 E5:.5 D5:.5 C5:.5 r:.5 E5:.5 r:.5 G5:1 r:1 "
        "A5:.5 r:.5 G5:.5 r:.5 F5:.5 E5:.5 D5:.5 C5:.5 B4:.5 r:.5 D5:.5 r:.5 G4:1 r:1 "
        "C5:.5 E5:.5 G5:.5 C6:.5 B5:.5 G5:.5 A5:.5 F5:.5 E5:.5 G5:.5 D5:.5 F5:.5 E5:1 r:1 "
        "F5:.25 E5:.25 D5:.5 r:.5 G5:.25 F5:.25 E5:.5 r:.5 D5:.5 B4:.5 C5:1 r:2")
melody(x, line, B, "pluck", .3, octshift=0)
bassl = "C3:1 G2:1 C3:1 G2:1 " * 2 + "F2:1 C3:1 G2:1 D3:1 " * 2 + "C3:1 E3:1 F3:1 G3:1 A2:1 B2:1 C3:2 " + "F2:1 G2:1 C3:2 r:4"
melody(x, bassl, B, "pluck", .35)
for k in range(32):
    place(x, woodblock(1200 if k % 2 else 850, .18), k*B)
write("xmas-pizzicato.wav", loop_to(x[:int(SR*32*B)], LEN))

# ---- 4. "We Wish You a Merry Christmas" (trad., PD): 3/4 waltz, brass-ish lead, oom-pah-pah, bells
B = 60/170; x = np.zeros(int(SR*(48*B+2)))
ww = ("G4:1 C5:1 C5:.5 D5:.5 C5:.5 B4:.5 A4:1 A4:1 A4:1 D5:1 D5:.5 E5:.5 D5:.5 C5:.5 B4:1 G4:1 "
      "G4:1 E5:1 E5:.5 F5:.5 E5:.5 D5:.5 C5:1 A4:1 G4:.5 G4:.5 A4:1 D5:1 B4:1 C5:2 r:1")
end = melody(x, ww, B, "brass", .22)
melody(x, ww, B, "brass", .22, t0=end)
harm = ["C", "C", "F", "F", "D", "G", "E", "E", "Am", "F", "G", "C"] * 2
for bar, c in enumerate(harm):
    b0 = (bar*3 + 1)*B; cn = chord_notes(c, 4)
    place(x, tone(chord_notes(c, 2)[0], B*.9, "bass", .35), b0)
    for k in (1, 2):
        for f in cn: place(x, tone(f, B*.5, "piano", .05), b0 + k*B)
    place(x, bells(.3, .07, bar), b0)
write("xmas-wewish.wav", loop_to(x[:int(SR*end*1.0)*2 if False else int(SR*2*end)], LEN))

# ---- 5. "Silent Night" (F. X. Gruber, 1818, PD): slow music box in 6/8, soft pad
B = 60/150   # eighth note
sn = ("G5:3 A5:1 G5:2 E5:6 G5:3 A5:1 G5:2 E5:6 D6:4 D6:2 B5:6 C6:4 C6:2 G5:6 "
      "A5:4 A5:2 C6:3 B5:1 A5:2 G5:3 A5:1 G5:2 E5:6 A5:4 A5:2 C6:3 B5:1 A5:2 G5:3 A5:1 G5:2 E5:6 "
      "D6:4 D6:2 F6:3 D6:1 B5:2 C6:6 E6:6 C6:3 G5:3 E5:3 G5:3 F5:1 D5:2 C5:12")
x = np.zeros(int(SR*(LEN+4)))
end = melody(x, sn, B, "musicbox", .30, sustain=1.0)
pads = [("C", 12), ("C", 12), ("G", 6), ("C", 6), ("F", 6), ("C", 6), ("F", 6), ("C", 6), ("G", 6), ("C", 6), ("C", 6), ("G", 3), ("C", 9)]
t = 0
for c, d in pads:
    for f in chord_notes(c, 3): place(x, tone(f, d*B+.5, "pad", .035), t)
    t += d*B
write("xmas-musicbox.wav", x[:int(SR*LEN)])

# ---- 6. "Deck the Halls" (trad. Welsh, PD): 144 BPM ukulele strums, glock melody, finger snaps
B = 60/144; x = np.zeros(int(SR*(LEN+2)))
dh = ("G5:1.5 F5:.5 E5:1 D5:1 C5:1 D5:1 E5:1 C5:1 D5:.5 E5:.5 F5:.5 D5:.5 E5:1.5 D5:.5 C5:1 B4:1 C5:2 r:2 "
      "G5:1.5 F5:.5 E5:1 D5:1 C5:1 D5:1 E5:1 C5:1 D5:.5 E5:.5 F5:.5 D5:.5 E5:1.5 D5:.5 C5:1 B4:1 C5:2 r:2 "
      "D5:1.5 E5:.5 F5:1 D5:1 E5:1.5 F5:.5 G5:1 D5:1 E5:.5 F#5:.5 G5:1 A5:.5 B5:.5 C6:1 B5:1 A5:1 G5:2 r:2 "
      "G5:1.5 F5:.5 E5:1 D5:1 C5:1 D5:1 E5:1 C5:1 A5:.5 A5:.5 A5:.5 A5:.5 G5:1.5 F5:.5 E5:1 D5:1 C5:2 r:2")
end = melody(x, dh, B, "glock", .26, sustain=.4)
harm = "C C G C C C G C G C D G C C F C".split()  # 2 beats... one per 4 beats
for bar, c in enumerate(harm * 2):
    b0 = bar*4*B
    if b0 > LEN: break
    for k, pat in enumerate((1, 0, 1, 1, 0, 1, 1, 0)):          # island strum pattern on 8ths
        if pat:
            for j, f in enumerate(chord_notes(c, 4)): place(x, pluck(f, .5, .07, .99, .7, bar*8+k+j), b0 + k*B/2 + j*.008)
    place(x, tone(chord_notes(c, 2)[0], B*1.8, "bass", .3), b0); place(x, tone(chord_notes(c, 2)[2], B*1.8, "bass", .25), b0 + 2*B)
    for k in (1, 3): place(x, snap(.28, bar*4+k), b0 + k*B)
write("xmas-deckhalls.wav", x[:int(SR*LEN)])

# ---- 7. game-show quiz (original): 132 BPM square-lead arpeggios, tick-tock, punchy bass
B = 60/132; x = np.zeros(int(SR*(32*B+2)))
for bar in range(8):
    c = ["Am", "F", "C", "E"][bar % 4] if bar % 4 != 3 else "E"; b0 = bar*4*B
    cn = chord_notes(c if c != "E" else "E", 4)
    for k in range(8):
        place(x, inst(cn[[0, 1, 2, 1, 0, 2, 1, 2][k] % len(cn)]*2, .4*B, "square", .07), b0 + k*B/2)
    for k in range(4):
        place(x, woodblock(1400 if k % 2 == 0 else 1000, .2), b0 + k*B)       # tick-tock
        place(x, tone(chord_notes(c, 2)[0], .8*B, "bass", .32), b0 + k*B)
        if k in (0, 2): place(x, kick(.6), b0 + k*B)
        if k in (1, 3): place(x, snare(.12, bar*4+k), b0 + k*B)
gl = "A5:.5 C6:.5 E6:1 D6:.5 C6:.5 A5:1 F5:.5 A5:.5 C6:1 B5:.5 A5:.5 F5:1 E5:.5 G5:.5 C6:1 E6:1 r:1 B5:.5 G#5:.5 E5:1 r:2"
melody(x, gl + " " + gl, B, "square", .12)
write("xmas-gameshow.wav", loop_to(x[:int(SR*32*B)], LEN))

# ---- 8. toy marimba bounce (original): 104 BPM marimba ostinato + toy piano + clap
B = 60/104; x = np.zeros(int(SR*(16*B+2)))
for bar in range(4):
    c = ["D", "G", "Bm" if False else "Em", "A"][bar]; b0 = bar*4*B; cn = chord_notes(c, 4)
    for k in range(8):
        place(x, inst(cn[[0, 2, 1, 2, 0, 2, 1, 2][k]], .5, "marimba", .2), b0 + k*B/2)
    place(x, inst(chord_notes(c, 2)[0], 1.0, "marimba", .35), b0); place(x, inst(chord_notes(c, 2)[0], 1.0, "marimba", .3), b0 + 2.5*B)
    for k in (1, 3): place(x, clap(.2, bar*4+k), b0 + k*B)
toy = "F#6:.5 A6:.5 F#6:.5 D6:.5 E6:1 r:1 G6:.5 B6:.5 G6:.5 E6:.5 F#6:1 r:1 E6:.5 G6:.5 B6:.5 G6:.5 A6:1.5 r:.5 C#6:.5 E6:.5 A6:.5 G6:.5 F#6:1 r:1"
melody(x, toy, B, "glock", .12)
write("xmas-toymarimba.wav", loop_to(x[:int(SR*16*B)], LEN))

# ---- 9. calm acoustic fingerpick (original, NOT Christmas): 92 BPM, Dadd9-A-Bm7-G
B = 60/92; x = np.zeros(int(SR*(16*B+3)))
for bar, c in enumerate(["Dadd9", "A", "Bm7", "Gmaj7"]):
    b0 = bar*4*B; cn = chord_notes(c, 3); bass = chord_notes(c, 2)[0]
    pat = [bass, cn[1]*2, cn[2]*2, cn[1]*2, chord_notes(c, 2)[2], cn[1]*2, cn[2]*2, cn[-1]*2]
    for k, f in enumerate(pat): place(x, pluck(f, 1.6, .2 if k % 4 == 0 else .13, .997, .35, bar*8+k), b0 + k*B/2)
mel = "F#5:1.5 E5:.5 D5:2 E5:1 C#5:1 A4:2 D5:1.5 F#5:.5 B5:2 A5:1 G5:.5 F#5:.5 E5:2"
melody(x, mel, B, "pluck", .14, t0=0)
x = lp(x, 3)
write("calm-acoustic.wav", loop_to(x[:int(SR*16*B)], LEN))

# ---- 10. mellow lo-fi + rain (original, NOT Christmas): 70 BPM, Ebmaj7-Cm7-Abmaj7-Bb7 (no bells)
B = 60/70; x = np.zeros(int(SR*(16*B+2)))
for bar, c in enumerate(["D#maj7", "Cm7", "G#maj7", "A#7"]):
    b0 = bar*4*B
    for k, f in enumerate(chord_notes(c, 3)): place(x, inst(f, 3.8*B, "felt", .11), b0 + .3*B + k*.02)
    place(x, tone(chord_notes(c, 1)[0], 3.5*B, "bass", .32), b0)
    for k in range(4):
        if k in (0, 2) or (k == 2): place(x, kick(.5), b0 + k*B + (.0 if k == 0 else .25*B))
        if k in (1, 3): place(x, lp(snare(.18, bar*4+k), 8), b0 + k*B)
        for s in (0, .66): place(x, lp(hat(.06, bar*8+k), 2), b0 + k*B + s*B)
x = lp(x, 7) + rain(len(x)/SR, .07) + vinyl(len(x)/SR, .03, 21)
write("calm-lofirain.wav", loop_to(x[:int(SR*16*B)], LEN))

# ---- 11. soft felt piano (original, NOT Christmas): 84 BPM, Cmaj7-G/B-Am7-Fmaj7, gentle melody
B = 60/84; x = np.zeros(int(SR*(16*B+4)))
for bar, c in enumerate(["Cmaj7", "G", "Am7", "Fmaj7"]):
    b0 = bar*4*B; cn = chord_notes(c, 3)
    place(x, inst(chord_notes(c, 2)[0], 4*B+1, "felt", .22), b0)
    for k, f in enumerate([cn[0], cn[2], cn[1]*2 if len(cn) > 2 else cn[1], cn[2]]*2): place(x, inst(f, 1.2, "felt", .09), b0 + k*B/2)
mel = "E5:2 G5:1 B5:1 D5:3 r:1 C5:2 E5:1 A5:1 C5:2 G4:1 A4:1"
melody(x, mel, B, "felt", .16, sustain=.8)
write("calm-piano.wav", loop_to(x[:int(SR*16*B)], LEN))
print("ok variety music")

# ---------- variety SFX ----------
rng = np.random.default_rng(31)
def click(f=2500, dec=200, amp=1.0, seed=0):
    r = np.random.default_rng(seed); n = int(SR*.03); t = np.arange(n)/SR
    return amp*(r.standard_normal(n)*.6 + np.sin(2*np.pi*f*t))*np.exp(-t*dec)
ty = np.zeros(int(SR*1.6))                                             # keyboard typing burst
for k in range(14): place(ty, click(2000 + 600*rng.random(), 220, .5 + .5*rng.random(), k), k*.105 + .03*rng.random())
write_sfx("sfx-typing.wav", ty)
tw = np.zeros(int(SR*.25)); place(tw, click(1400, 120, 1, 5), 0); place(tw, .5*click(600, 60, 1, 6), .015)   # typewriter key clack
write_sfx("sfx-typewriter.wav", tw)
n = int(SR*.25); tt = np.arange(n)/SR                                  # message sent: quick rising swoosh-blip
write_sfx("sfx-send.wav", lp(rng.standard_normal(n), 8)*np.sin(np.pi*tt/.25)**2*.5 + np.sin(2*np.pi*np.cumsum(600+1400*tt/.25)/SR)*np.exp(-((tt-.12)/.05)**2))
n = int(SR*.5); tt = np.arange(n)/SR                                   # message received: soft two-note marimba ding
rc = np.zeros(n); place(rc, inst(hz("G", 5), .45, "marimba", .6), 0); place(rc, inst(hz("D", 6), .4, "marimba", .6), .08); write_sfx("sfx-recv.wav", rc)
n = int(SR*2.2); tt = np.arange(n)/SR                                  # printer whirr: motor hum + stepper clicks
pr = .5*np.sin(2*np.pi*(118 + 6*np.sin(2*np.pi*3*tt))*tt)*np.minimum(1, tt*8)*np.minimum(1, (2.2-tt)*8) + .25*lp(rng.standard_normal(n), 3)*(np.sin(2*np.pi*22*tt) > .7)
write_sfx("sfx-printer.wav", pr)
n = int(SR*LEN); cr = lp(rng.standard_normal(n), 60)*.25                # fire crackle bed (long, quiet rumble + pops)
pops = (rng.random(n) < 9/SR)*rng.uniform(.2, 1, n)
cr += np.convolve(pops*np.sign(rng.standard_normal(n)), np.exp(-np.arange(220)/18)*rng.standard_normal(220), "same")*.8
write_sfx("sfx-crackle.wav", cr)
n = int(SR*.18); tt = np.arange(n)/SR                                  # check tick: pencil scratch + blip
write_sfx("sfx-check.wav", lp(rng.standard_normal(n), 3)*np.exp(-tt*25)*.6 + np.sin(2*np.pi*1600*tt)*np.exp(-tt*40))
n = int(SR*1.0); tt = np.arange(n)/SR                                  # meter rise
write_sfx("sfx-rise.wav", (np.sign(np.sin(2*np.pi*np.cumsum(200+900*tt**1.5)/SR))*.3 + np.sin(2*np.pi*np.cumsum(200+900*tt**1.5)/SR))*np.minimum(1, (1-tt)*20)*(.4+.6*tt))
n = int(SR*.5); tt = np.arange(n)/SR                                   # buzzer (wrong answer / naughty)
write_sfx("sfx-buzz.wav", np.sign(np.sin(2*np.pi*110*tt))*.6 + np.sign(np.sin(2*np.pi*116*tt))*.4)
n = int(SR*.07); tt = np.arange(n)/SR                                  # stop-motion shutter click
sc = np.zeros(int(SR*.12)); place(sc, click(3000, 300, 1, 9), 0); place(sc, click(1800, 250, .7, 10), .05); write_sfx("sfx-shutter.wav", sc)
n = int(SR*.4); tt = np.arange(n)/SR                                   # paper slide / page turn swish
write_sfx("sfx-paper.wav", (rng.standard_normal(n) - lp(rng.standard_normal(n), 5))*np.sin(np.pi*tt/.4)**3)
n = int(SR*1.2); ta = np.zeros(n)                                      # ta-da fanfare (original 3-note)
for k, (nn, o, at) in enumerate([("C", 5, 0), ("E", 5, .1), ("G", 5, .2), ("C", 6, .3)]): place(ta, inst(hz(nn, o), .9 - at, "brass", .5), at)
write_sfx("sfx-tada.wav", ta)
n = int(SR*1.4); tt = np.arange(n)/SR; dr = np.zeros(n)                # drum roll
for k in range(40): place(dr, snare(.2 + .6*k/40, 50+k), k*.033)
write_sfx("sfx-drumroll.wav", dr)
n = int(SR*.5); tt = np.arange(n)/SR                                   # record scratch ("wait what")
write_sfx("sfx-scratch.wav", lp(rng.standard_normal(n), 2)*np.abs(np.sin(2*np.pi*np.cumsum(8 + 30*np.sin(2*np.pi*3*tt))/SR))*np.exp(-tt*4))
n = int(SR*1.5); tt = np.arange(n)/SR                                  # soft chime (calm videos)
ch = np.zeros(n)
for k, (nn, o) in enumerate([("D", 6), ("A", 6), ("F#", 6)]): place(ch, inst(hz(nn, o), 1.3, "musicbox", .4), k*.12)
write_sfx("sfx-chime.wav", ch)
print("ok variety sfx")
