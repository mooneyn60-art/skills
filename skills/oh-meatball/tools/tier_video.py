#!/usr/bin/env python3
"""Ranked drawn video (tier list) from one YAML: per-creature drawn segments + a tier board that fills in.

  tier_video.py specs  TIERS.yaml            write one drawn.py spec per segment (open, each creature, end) and print
                                             the planned spoken length of each and the total
  tier_video.py render TIERS.yaml [--only k] render the segments ONE at a time (skips finished masters)
  tier_video.py longform TIERS.yaml OUT.mp4  16:9 YouTube cut: a "#N NAME" title bar on each segment, pillarboxed
                                             like tools/drawn_compile.py, hard cuts, chapters one per tier
  tier_video.py tiktok TIERS.yaml FULL.mp4 TOP5.mp4
                                             9:16 cuts from the same masters: the full ranking (each creature's
                                             naming line + its board verdict) and the top 5 deadliest
Masters live in $TIER_WORK (default /tmp/tier-work/<yaml name>), outside the repo. Outline: scripts/tier-house/*.yaml.
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
STAGE_KEYS = ("creature", "actor", "s", "scene", "scene_p", "creature_cfg", "wild", "wild_p", "hero_p")
BOARD = {"pos": [540, 430], "s": 0.92}
BOARD_SCENE = {"scene": "study", "scene_p": {"time": "night"}}
FIT_CAM = [540, 960, 1.0]
S_ROW_CAM = [540, 640, 1.22]


def load(path):
    import yaml
    return yaml.safe_load(open(os.path.join(ROOT, path) if not os.path.isabs(path) else path))


def work_dir(yaml_path):
    d = os.environ.get("TIER_WORK", os.path.join("/tmp/tier-work", os.path.splitext(os.path.basename(yaml_path))[0]))
    os.makedirs(d, exist_ok=True)
    return d


def stage_of(c):
    if "stage" in c:
        return dict(c["stage"])
    o = load(c["outline"])
    return {k: o[k] for k in STAGE_KEYS if k in o}


def sources_of(c):
    if "sources_from" in c:
        return load(c["sources_from"])["sources"]
    return load(c["outline"])["sources"]


def icon_of(c):
    st = stage_of(c)
    if st.get("actor") and st["actor"] != "creature":
        return {"type": st["actor"], "tier": c["tier"]}
    if st.get("creature_cfg") and st.get("actor") == "creature":
        from drawn_species import SPECIES
        return {"cfg": dict(SPECIES.get(st["creature"], {}), **st["creature_cfg"]), "tier": c["tier"]}
    return {"type": "sp." + st["creature"], "tier": c["tier"]}


def line(item):
    import drawn_quick
    return drawn_quick.line(item)


def board_beat(say, icons, *, drop=False, hide_s=True, unveil=False, shots=None, pose="point", gest="shrug",
               sfx=None, glow=True):
    p = {"icons": icons, "hide_s": hide_s, "drop": 0.0 if drop else 1.0}
    sets = []
    if unveil:
        p["unveil"] = 0.0
        sets.append({"at": "5%", "dur": 0.7, "p": {"unveil": 1.0}})
    if drop:
        sets.append({"at": "30%" if unveil else "12%", "dur": 0.75, "p": {"drop": 1.0}})
        if glow:
            sets.append({"at": "35%", "dur": 0.3, "p": {"glow": 1.0}})
    return dict(BOARD_SCENE, say=say, pad=0.25,
                shots=shots or [{"cam": FIT_CAM, "to": [540, 930, 1.05]}],
                actors=[dict(BOARD, id="board", type="tierboard", p=p, set=sets)],
                mb={"pose": pose, "pos": [150, 1890], "size": 560, "look": "board", "gest": [["55%", gest, 1.2]]},
                sfx=sfx or (["whoosh@10%", "boing@32%"] if drop else ["tink@10%"]))


def build(o):
    """[(name, spec, roles)] in play order; roles name each beat (open, body0, body, verdict, tease, end)."""
    base = {"voice": "kokoro:fenrir", "music": o.get("music", "mystery"), "music_db": -20, "captions": 66,
            "caption_y": 1640, "photo_credits": []}
    segs = []
    op = o["open"]
    ost = load(op["outline"])
    beats = [line(x) for x in op["lines"]] + [board_beat(s, [], shots=[{"cam": [540, 700, 1.15], "to": FIT_CAM}]
                                                         if k == 0 else None, pose="shock" if k == 0 else "point")
                                              for k, s in enumerate(op["board"])]
    segs.append(("00-open", dict(base, stage={k: ost[k] for k in STAGE_KEYS if k in ost}, sources=ost["sources"],
                                 beats=beats), ["open"] * len(beats)))
    icons = []
    for i, c in enumerate(o["creatures"]):
        ic = icon_of(c)
        body = [line(x) for x in c["body"]]
        reveal = c["tier"] == "S" and not any(x["tier"] == "S" for x in icons)
        icons_now = icons + [ic]
        bb = [board_beat(c["verdict"], icons_now, drop=True, hide_s=c["tier"] != "S" or reveal, unveil=reveal)]
        roles = ["body0"] + ["body"] * (len(body) - 1) + ["verdict"]
        if c.get("tease"):
            bb.append(board_beat(c["tease"], icons_now, hide_s=True, pose="think", gest="shock",
                                 shots=[{"cam": FIT_CAM, "to": S_ROW_CAM}], sfx=["whoosh@5%", "tink@60%"]))
            roles.append("tease")
        segs.append((f'{i + 1:02d}-{c["slug"]}', dict(base, stage=stage_of(c), sources=sources_of(c), beats=body + bb),
                     roles))
        icons = icons_now
    end = [board_beat(s, icons, hide_s=False, pose="point" if k == 0 else "wave",
                      shots=[{"cam": FIT_CAM, "to": [540, 940, 1.06]}] if k == 0 else
                      [{"cam": [540, 930, 1.06], "to": [540, 900, 1.12]}]) for k, s in enumerate(o["end"])]
    segs.append(("99-end", dict(base, stage=segs[-1][1]["stage"], sources=[], beats=end), ["end"] * len(end)))
    return segs


def plan_times(spec_path, work):
    import drawn
    os.makedirs(work, exist_ok=True)
    spec = drawn.drawn_macros.expand(json.load(open(spec_path)))
    beats, total = drawn.plan(spec, work)
    return [(b["t0"], b["t0"] + b["dur"]) for b in beats], total


def write_specs(yaml_path):
    o = load(yaml_path)
    wd = work_dir(yaml_path)
    spec_dir = os.path.join(os.path.dirname(os.path.abspath(yaml_path)), "specs")
    os.makedirs(spec_dir, exist_ok=True)
    man = []
    for name, spec, roles in build(o):
        sp = os.path.join(spec_dir, name + ".json")
        json.dump(spec, open(sp, "w"), indent=1, ensure_ascii=False)
        man.append({"name": name, "spec": sp, "roles": roles})
    json.dump(man, open(os.path.join(wd, "manifest.json"), "w"), indent=1)
    return man, wd


def cmd_specs(a):
    man, wd = write_specs(a.yaml)
    tot = 0.0
    for m in man:
        times, L = plan_times(m["spec"], os.path.join(wd, "w-" + m["name"]))
        assert len(times) == len(m["roles"]), (m["name"], len(times), len(m["roles"]))
        m["times"] = times
        tot += L
        print(f'{m["name"]:24s} {L:6.1f} s   total {tot:6.1f} s ({int(tot // 60)}:{int(tot % 60):02d})', flush=True)
    json.dump(man, open(os.path.join(wd, "manifest.json"), "w"), indent=1)


def cmd_render(a):
    man, wd = write_specs(a.yaml)
    for m in man:
        if a.only and a.only not in m["name"]:
            continue
        out = os.path.join(wd, m["name"] + ".mp4")
        if os.path.exists(out) and not a.force:
            continue
        tmp = out + ".part.mp4"
        subprocess.run([sys.executable, os.path.join(HERE, "drawn.py"), m["spec"], tmp, "--work",
                        os.path.join(wd, "w-" + m["name"])], check=True)
        os.replace(tmp, out)
        for f in os.listdir(os.path.join(wd, "w-" + m["name"])):   # keep the voice cache, drop frame scratch
            if f.endswith((".png", ".wav")) and not f.startswith("v"):
                os.remove(os.path.join(wd, "w-" + m["name"], f))


def manifest(yaml_path):
    wd = work_dir(yaml_path)
    man = json.load(open(os.path.join(wd, "manifest.json")))
    for m in man:
        if "times" not in m:
            m["times"], _ = plan_times(m["spec"], os.path.join(wd, "w-" + m["name"]))
        m["mp4"] = os.path.join(wd, m["name"] + ".mp4")
    return man, wd


def dur(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True, check=True).stdout.strip())


def stamp(t):
    t = int(round(t))
    return f"{t // 60}:{t % 60:02d}"


def cmd_longform(a):
    import tt_style
    o = load(a.yaml)
    man, wd = manifest(a.yaml)
    crs = {f'{i + 1:02d}-{c["slug"]}': c for i, c in enumerate(o["creatures"])}
    parts, chapters, t, seen = [], [], 0.0, set()
    crf = os.environ.get("CRF", "24")
    for m in man:
        c = crs.get(m["name"])
        if c:
            title, sub = f'#{c["rank"]} {c["label"]}', "HOUSE CREATURES: HARMLESS TO DEADLY"
            if c["tier"] not in seen:
                seen.add(c["tier"])
                chapters.append(f'{stamp(t)} {c["tier"]} Tier: {o["tiers"][c["tier"]]}')
        elif m["name"].endswith("open"):
            title, sub = "HARMLESS TO DEADLY", "EVERY CREATURE IN YOUR HOUSE, RANKED"
            chapters.append(f"{stamp(t)} The Tier List")
        else:
            title, sub = "WHICH ONE IS IN YOUR HOUSE?", "COMMENT THE TIER"   # < 10 s: no chapter of its own
        p = os.path.join(wd, f'L-{m["name"]}.mkv')
        vf = (f"[0:v]{tt_style.bar(title, sub)},split=2[a][b];"
              "[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:3,eq=brightness=-0.18[bg];"
              "[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0,format=yuv420p[v]")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", m["mp4"], "-filter_complex", vf, "-map", "[v]", "-map",
                        "0:a", "-r", "30", "-c:v", "libx264", "-preset", "veryfast", "-crf", crf, "-g", "60",
                        "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", p], check=True)
        parts.append(p)
        t += dur(p)
        print(f"  {stamp(t)}  {m['name']}", flush=True)
    lst = os.path.join(wd, "L-list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", a.out], check=True)
    for p in parts:
        os.remove(p)
    open(os.path.splitext(a.out)[0] + ".chapters.txt", "w").write("\n".join(chapters) + "\n")
    print(f"done {a.out}  {stamp(dur(a.out))}  {os.path.getsize(a.out) / 1e6:.1f} MB")


def cut(pieces, out, title, sub):
    """pieces: [(mp4, t0, t1)] -> one 9:16 mp4 with a title bar, short audio fades at every join."""
    import tt_style
    ins, fc = [], []
    for k, (mp4, t0, t1) in enumerate(pieces):
        ins += ["-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", mp4]
        d = t1 - t0
        fc.append(f"[{k}:v]setpts=PTS-STARTPTS,fps=30[v{k}];[{k}:a]asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d=0.04,afade=t=out:st={max(0, d - 0.06):.3f}:d=0.06[a{k}]")
    fc.append("".join(f"[v{k}][a{k}]" for k in range(len(pieces))) + f"concat=n={len(pieces)}:v=1:a=1[cv][ca]")
    fc.append(f"[cv]{tt_style.bar(title, sub)}[ov]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[ov]", "-map",
                    "[ca]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-c:a", "aac", "-b:a", "160k",
                    "-ar", "48000", "-movflags", "+faststart", out], check=True)
    print(f"done {out}  {stamp(dur(out))}  {os.path.getsize(out) / 1e6:.1f} MB")


def pick(m, roles):
    """[(mp4, t0, t1)] for the beats with these roles (adjacent beats merged)."""
    out = []
    for (t0, t1), r in zip(m["times"], m["roles"]):
        if r in roles:
            if out and abs(out[-1][2] - t0) < 1e-3:
                out[-1] = (m["mp4"], out[-1][1], t1)
            else:
                out.append((m["mp4"], t0, t1))
    if out and m["times"][-1][1] - out[-1][2] < 0.6:   # the last beat runs to the end of the file
        out[-1] = (m["mp4"], out[-1][1], dur(m["mp4"]))
    return out


def cmd_tiktok(a):
    o = load(a.yaml)
    man, _ = manifest(a.yaml)
    ranks = {f'{i + 1:02d}-{c["slug"]}': c["rank"] for i, c in enumerate(o["creatures"])}
    full, top = [], []
    for m in man:
        r = ranks.get(m["name"])
        if r is None:
            full += pick(m, {"open", "end"})
            if m["name"].endswith("open"):
                top += [(m["mp4"], *m["times"][0])]
            else:
                top += [(m["mp4"], m["times"][-1][0], dur(m["mp4"]))]
            continue
        full += pick(m, {"body0", "verdict"})
        if r <= 5:
            top += pick_first_body(m) if r <= a.top_extra else pick(m, {"body0", "verdict"})
    cut(full, a.full, "EVERY HOUSE CREATURE, RANKED", "HARMLESS TO DEADLY")
    cut(top, a.top5, "TOP 5 DEADLIEST IN YOUR HOUSE", "RANKED BY REAL DANGER")


def pick_first_body(m):
    """body0 + the next body line + verdict."""
    keep = set()
    for k, r in enumerate(m["roles"]):
        if r == "body0":
            keep |= {k, k + 1}
        if r == "verdict":
            keep.add(k)
    out = []
    for k, (t0, t1) in enumerate(m["times"]):
        if k in keep:
            if out and abs(out[-1][2] - t0) < 1e-3:
                out[-1] = (m["mp4"], out[-1][1], t1)
            else:
                out.append((m["mp4"], t0, t1))
    return out


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("specs")
    s.add_argument("yaml")
    r = sp.add_parser("render")
    r.add_argument("yaml")
    r.add_argument("--only")
    r.add_argument("--force", action="store_true")
    lf = sp.add_parser("longform")
    lf.add_argument("yaml")
    lf.add_argument("out")
    tk = sp.add_parser("tiktok")
    tk.add_argument("yaml")
    tk.add_argument("full")
    tk.add_argument("top5")
    tk.add_argument("--top-extra", type=int, default=0, help="ranks <= N also keep their second line")
    a = ap.parse_args()
    {"specs": cmd_specs, "render": cmd_render, "longform": cmd_longform, "tiktok": cmd_tiktok}[a.cmd](a)


if __name__ == "__main__":
    main()
