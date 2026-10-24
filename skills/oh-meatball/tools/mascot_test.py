#!/usr/bin/env python3
"""Meatball rig test: OLD (tools-original/mascot.py) vs NEW (this mascot.py) acting the same lines.

Usage: mascot_test.py OUT_DIR [--work DIR] [--old PATH/TO/tools-original]
Writes OUT_DIR/compare.mp4 and OUT_DIR/contact.png (2 s of consecutive frames at 8 fps for each rig).
compare.mp4 = part A: Meatball alone on white, OLD | NEW, same lines and word timings (edge-tts, the way
explainer.py makes them); then part B: the same lines as a vertical Short built by each explainer.py
(OLD corner sticker | NEW shot grammar: show, host, together, close-up). Part B needs network for the
iNaturalist photos and the voice.
"""
import argparse
import asyncio
import importlib.util
import json
import os
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FPS, W, H, SIZE = 30, 960, 1080, 720
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
# The Showrunner's test line, split the way a script would beat it (research/39 persona).
BEATS = [("shock", "True! Every tiger's stripes are different, like a fingerprint."),
         ("nervous", "So if one eats you, you'll know exactly who did it."),
         ("deadpan", "I don't LOVE that.")]
VOICE, RATE, PITCH = "en-US-AndrewMultilingualNeural", "+4%", "-3Hz"
POS = (-90, 260)                  # mascot canvas top-left inside a half
PANEL = (520, 120, 400, 520)      # stand-in "photo" panel he points and looks at


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # worker processes pickle frame jobs by module name
    spec.loader.exec_module(mod)
    return mod


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True, check=True).stdout)


def background(path, label):
    im = Image.new("RGB", (W, H), (250, 248, 242))
    d = ImageDraw.Draw(im)
    x, y, w, h = PANEL
    d.rounded_rectangle([x, y, x + w, y + h], 30, fill=(160, 170, 150), outline=(90, 90, 90), width=4)
    d.text((x + w / 2, y + h / 2), "photo", font=ImageFont.truetype(BOLD, 48), fill=(240, 240, 240), anchor="mm")
    d.text((30, 30), label, font=ImageFont.truetype(BOLD, 56), fill=(196, 38, 30))
    im.save(path)


def render(mod, fps, label, voices, work):
    bg = f"{work}/{label}_bg.png"
    background(bg, label)
    segs = []
    for i, ((pose, _), (mp3, words)) in enumerate(zip(BEATS, voices)):
        d = dur(mp3) + 0.35
        frames = f"{work}/{label}_f{i}"
        shutil.rmtree(frames, ignore_errors=True)
        kw = {"content": (PANEL[0] + PANEL[2] / 2 - (POS[0] + SIZE / 2), PANEL[1] + PANEL[3] / 2 - (POS[1] + SIZE * 0.36))} \
            if label == "NEW" else {}
        mod.animate(pose, SIZE, words, d, fps, frames, seed=i, **kw)
        pad = int(SIZE * 0.25)
        seg = f"{work}/{label}_s{i}.mp4"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", bg,
                        "-framerate", str(fps), "-i", f"{frames}/%04d.png", "-i", mp3, "-filter_complex",
                        f"[1:v]fps={FPS}[m];[0:v][m]overlay={POS[0] - pad}:{POS[1] - pad}:eof_action=repeat,format=yuv420p[v];"
                        "[2:a]apad[a]", "-map", "[v]", "-map", "[a]", "-t", f"{d:.3f}", "-r", str(FPS),
                        "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-c:a", "aac", "-ar", "48000", seg],
                       check=True)
        shutil.rmtree(frames, ignore_errors=True)
        segs.append(seg)
    lst = f"{work}/{label}.txt"
    open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    out = f"{work}/{label}.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out],
                   check=True)
    return out


def contact(videos, out, start=1.0, secs=2.0, rate=8, cell=(240, 300)):
    rows = []
    for v in videos:
        tmp = v + "_contact"
        shutil.rmtree(tmp, ignore_errors=True)
        os.makedirs(tmp)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(start), "-t", str(secs), "-i", v,
                        "-vf", f"fps={rate}", f"{tmp}/%02d.png"], check=True)
        rows.append([Image.open(f"{tmp}/{f}").crop((0, 250, 600, 1050)).resize(cell, Image.LANCZOS)
                     for f in sorted(os.listdir(tmp))])
        shutil.rmtree(tmp)
    n = max(len(r) for r in rows)
    sheet = Image.new("RGB", (n * cell[0], len(rows) * (cell[1] + 40)), "white")
    d = ImageDraw.Draw(sheet)
    for y, (v, r) in enumerate(zip(videos, rows)):
        for x, im in enumerate(r):
            sheet.paste(im, (x * cell[0], y * (cell[1] + 40) + 40))
            d.text((x * cell[0] + 6, y * (cell[1] + 40) + 8), f"{start + x / rate:.3f}s", fill=(0, 0, 0),
                   font=ImageFont.truetype(BOLD, 20))
        d.text((n * cell[0] - 120, y * (cell[1] + 40) + 8), os.path.basename(v)[:-4], fill=(196, 38, 30),
               font=ImageFont.truetype(BOLD, 24))
    sheet.save(out)


SHORT = {"voice": VOICE, "rate": RATE, "pitch": PITCH, "style": "classic", "beats": [
    {"say": "Every tiger's stripes are different, like a fingerprint.", "pose": "point", "bleed": True, "shots": [
        {"photo": "Panthera tigris", "obs": 130812240, "crop": [0.18, 0.05, 0.56, 1.0], "frame": "show"},
        {"photo": "Panthera tigris", "obs": 383845724, "crop": [0.32, 0.1, 0.76, 1.0], "frame": "host", "at": "like"}]},
    {"say": "So if one eats you, you'll know exactly who did it.", "pose": "nervous", "bleed": True, "shots": [
        {"photo": "Panthera tigris", "obs": 342934458, "crop": [0.12, 0.0, 0.58, 1.0], "frame": "together"}]},
    {"say": "I don't LOVE that.", "pose": "deadpan", "prop": "fork", "shots": [{"frame": "close"}]}]}


def short(tools, spec, work, out):
    os.makedirs(work, exist_ok=True)
    subprocess.run(["nice", "-n", "10", "python3", f"{tools}/explainer.py", spec, work, "build", out, "--vertical"],
                   check=True, cwd=tools)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--work", default="/tmp/meatball-rig-test")
    ap.add_argument("--old", default=os.path.join(HERE, "..", "..", "tools-original"))
    a = ap.parse_args()
    a.work = os.path.abspath(a.work)
    os.makedirs(a.work, exist_ok=True)
    os.makedirs(a.out, exist_ok=True)
    import sys
    sys.path.insert(0, HERE)
    from facts import speak
    voices = []
    for i, (_, line) in enumerate(BEATS):
        mp3 = f"{a.work}/vo{i}.mp3"
        if not os.path.exists(mp3 + ".words.json"):
            json.dump(asyncio.run(speak(line, VOICE, mp3, RATE, PITCH)), open(mp3 + ".words.json", "w"))
        voices.append((mp3, [tuple(w) for w in json.load(open(mp3 + ".words.json"))]))
    old = render(load(os.path.join(a.old, "mascot.py"), "mascot_old"), 15, "OLD", voices, a.work)
    new = render(load(os.path.join(HERE, "mascot.py"), "mascot_new"), FPS, "NEW", voices, a.work)
    spec = f"{a.work}/short.json"
    json.dump(SHORT, open(spec, "w"), indent=1)
    s_old = short(os.path.abspath(a.old), spec, f"{a.work}/short_old", f"{a.work}/short_old.mp4")
    s_new = short(HERE, spec, f"{a.work}/short_new", f"{a.work}/short_new.mp4")
    label = ("drawtext=fontfile=" + BOLD + ":text='{}':x=24:y=24:fontsize=44:fontcolor=0xC4261E:"
             "box=1:boxcolor=white@0.8:boxborderw=8")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", old, "-i", new, "-i", s_old, "-i", s_new,
                    "-filter_complex",
                    "[0:v][1:v]hstack=inputs=2,fps=30,setsar=1[a];"
                    f"[2:v]scale=540:960,{label.format('OLD')}[o];[3:v]scale=540:960,{label.format('NEW shot grammar')}[n];"
                    "[o][n]hstack=inputs=2,pad=1920:1080:420:60:color=0xF6F4EE,fps=30,setsar=1[b];"
                    "[1:a]aresample=48000[aa];[3:a]aresample=48000[ab];"
                    "[a][aa][b][ab]concat=n=2:v=1:a=1[v][au]", "-map", "[v]", "-map", "[au]",
                    "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "aac", f"{a.out}/compare.mp4"],
                   check=True)
    contact([old, new], f"{a.out}/contact.png")
    print("ok", f"{a.out}/compare.mp4", f"{a.out}/contact.png")


if __name__ == "__main__":
    main()
