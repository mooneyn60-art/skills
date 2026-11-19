"""Per-line whisper check: each scripted line transcribed from its own time span of the rendered mix."""
import sys, os, difflib, re
sys.path.insert(0, "/home/user/skills/skills/oh-meatball/tools")
import numpy as np, soundfile as sf, scipy.signal as ss
import cutout2 as c
from faster_whisper import WhisperModel
script, wav = sys.argv[1], sys.argv[2]
c.SEQ[:] = {"v3": c.SEQ_V3, "v4": c.SEQ_V4}.get(script, c.SEQ)
lines, segs, ev, end = c.build()
a, sr = sf.read(wav, dtype="float32")
m = WhisperModel("small.en", device="cpu", compute_type="int8")
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " "))
bad = 0
for i, l in enumerate(lines):
    x = a[int(max(0, l["t0"] - 0.15) * sr):int((l["start"] + l["dur"] + 0.25) * sr)]
    x16 = ss.resample_poly(x, 160, 441).astype(np.float32)
    heard = " ".join(s.text.strip() for s in m.transcribe(x16, language="en", beam_size=5,
                                                          condition_on_previous_text=False)[0])
    said = " ".join(w[2] for w in l["words"])
    r = difflib.SequenceMatcher(None, norm(said).split(), norm(heard).split()).ratio()
    flag = "OK  " if r >= 0.6 else "LOW "
    bad += r < 0.6
    print(f"{flag}{i + 1:2d} {l['who']:8s} {r:.2f} | {heard}", flush=True)
print("lines below 0.6 match:", bad)
