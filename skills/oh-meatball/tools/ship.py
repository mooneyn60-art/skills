#!/usr/bin/env python3
"""Ship a batch of drawn Shorts with ONE command: lint -> render -> gates -> contact sheets -> (push) -> payloads.

  ship.py OUTLINE.yaml [OUTLINE2.yaml ...] [--only yt|tt] [--out /dev/shm/ship/<batch>]
          [--push | --dry-push] [--schedule-json] [--jobs N] [--rerender] [--force] [--copy] [-m "commit subject"]
          [--repo DIR --repo-subdir skills/oh-meatball --branch B]

What the agent still does: write the outlines, glance at the contact sheets, make the Metricool calls
(<out>/schedule.json holds every createScheduledPost call ready to send) and append the printed posted.csv rows.

Phases (renders are CPU bound, so they run one at a time; nothing else blocks on them):
  1 preflight  every outline at once (3 threads): outline_lint + drawn_quick.py --no-render (sameness gate, spec
               JSON, spoken length, TTS fetched and cached) -> length problems show up before the first render
  2 render     drawn_quick.py per outline and cut, sequentially; the gates of video N run while N+1 renders
  3 push       (--push) the passing mp4s + contact sheets + outlines + specs, one commit built with a temporary
               GIT_INDEX_FILE on origin/<branch>, pushed by SHA (fast-forward only; rebuilt if origin moved), raw
               URLs verified HTTP 200. The local branch is then fast-forwarded ONLY if it has no commits that are
               not on origin (compare-and-swap), the index (never the worktree) is reset, and the new paths that are
               not on disk get skip-worktree. Renders are not copied into the worktree on / unless --copy.
               Refuses main/master and a detached HEAD unless --branch says so. Trailers: $SHIP_TRAILER, else the
               current session (from $CLAUDE_CODE_REMOTE_SDK_URL).
               A re-run with the same --out reuses a render whose outline, spec, data/tt_headers.json and renderer
               tools/*.py are unchanged (render, look at the sheets, then re-run with --push --schedule-json: no second
               render; --rerender forces one). Re-pushing files origin already has makes no new commit.
  4 payloads   (--schedule-json) Metricool payloads + posted.csv rows; results table + <out>/results.json
A failure in one outline never stops the batch; every gate is reported, and a gate that never ran counts as a
failure. Exit 1 if any video fails, the push fails, or a pushed raw URL does not answer 200.

Gates per video:
  lint        channel-brain outline_lint.py (blocks the render unless --force)
  sameness    tools/sameness.py on the outline (run here too: drawn_quick --force would skip it silently)
  length      spoken length inside ship's window (yt 15-20 s, tt 61-65 s; --force renders anyway, the gate stays FAIL)
  render      drawn_quick.py exit 0 (also its ffprobe check: audio+video, < 50 MB)
  duration    rendered length by cut: yt 15-20 s, tt 61-65 s (TT short loopers post the yt cut: 15-25 s)
  size        1080x1920
  first_voice voice onset < 0.1 s, measured two ways, both must pass: the first TTS sample in the render plan
              (|x| > 0.01, the lf_gates method) and the energy onset of the final mix (250-4000 Hz, 10 ms frames,
              first frame above 25% of the 90th-percentile frame RMS)
  zaps        the approved 2.5 kHz alarm detector (mono 24 kHz, 2400-sample hanning windows, hop 2400; zap if
              max(2400-2600 Hz) > 15 and max/(median(900-4000 Hz)+1e-9) > 120); must be 0
  vidcheck    channel-brain vidcheck.py (yt only)
  contact     a 2 fps contact sheet exists (drawn_quick writes it; made here if missing)

Optional outline keys for --schedule-json: yt_title (else title), yt_date / tt_date ("YYYY-MM-DD HH:MM", New York;
yt_date falls back to data/sequel-related-video-map.csv), yt_text (YouTube description), tt_caption (else
tiktok_caption), pinned (first comment; else "Part 1 is in the Related video" for a mapped sequel, else the
caption's question), tt_cut: short|long (which render the TikTok post uses; default long when the outline has a tt act).
"""
import argparse
import concurrent.futures as cf
import csv
import filecmp
import datetime as dt
import glob
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import zoneinfo

import numpy as np
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BRAIN = next((p for p in (os.environ.get("CHANNEL_BRAIN_TOOLS", ""), os.path.join(ROOT, "..", "channel-brain", "tools"),
                          os.path.join(ROOT, "channel-brain", "tools")) if p and os.path.exists(os.path.join(p, "vidcheck.py"))), None)
WINDOWS = {"yt": (15.0, 20.0), "tt": (61.0, 65.0), "tt_short": (15.0, 25.0)}
SIZE = (1080, 1920)
SR = 24000
BLOG_ID, TZ = "7521392", "America/New_York"
OWNER_REPO = "mooneyn60-art/skills"
GATES = ("lint", "sameness", "length", "render", "duration", "size", "first_voice", "zaps", "vidcheck", "contact")


def trailer():
    """Attribution lines for THIS session: $SHIP_TRAILER (literal, \\n-separated) wins; else the session id from the
    remote session URL (cse_X -> session_X); else the lead session's lines as of 11/3."""
    if os.environ.get("SHIP_TRAILER"):
        return os.environ["SHIP_TRAILER"].replace("\\n", "\n").strip()
    m = re.search(r"/sessions/cse_(\w+)", os.environ.get("CLAUDE_CODE_REMOTE_SDK_URL", ""))
    sid = m.group(1) if m else "01B6g5mJGtBmh6CLoEx3Vyyw"
    return f"Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_{sid}"


def run(cmd, env=None, cwd=None, inp=None, split=False):
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=cwd, input=inp)
    return (p.returncode, p.stdout, p.stderr) if split else (p.returncode, p.stdout + p.stderr)


def log(msg):
    print(f"[ship {time.strftime('%H:%M:%S')}] {msg}", flush=True)


# ---------------------------------------------------------------- audio gates
def decode(mp4, sr=SR):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def zap_count(x, sr=SR):
    """The approved beep check, unchanged: count 100 ms windows with a narrow 2.4-2.6 kHz tone."""
    n = 2400
    f = np.fft.rfftfreq(n, 1 / sr)
    band, ref = (f >= 2400) & (f <= 2600), (f >= 900) & (f <= 4000)
    win = np.hanning(n)
    zaps = []
    for i in range(0, len(x) - n + 1, n):
        mag = np.abs(np.fft.rfft(x[i:i + n] * win))
        b = mag[band].max()
        if b > 15 and b / (np.median(mag[ref]) + 1e-9) > 120:
            zaps.append(round(i / sr, 2))
    return zaps


def energy_onset(x, sr=SR):
    """Seconds to the first 10 ms frame whose voice-band RMS passes 25% of the 90th-percentile frame RMS."""
    spec = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / sr)
    spec[(f < 250) | (f > 4000)] = 0
    y = np.fft.irfft(spec, len(x))
    hop = sr // 100
    rms = np.sqrt(np.mean(y[:len(y) // hop * hop].reshape(-1, hop) ** 2, 1))
    if not len(rms) or rms.max() <= 0:
        return None
    on = np.nonzero(rms > 0.25 * np.percentile(rms, 90))[0]
    return round(on[0] * hop / sr, 3) if len(on) else None


def plan_onset(spec_path, work):
    """First TTS sample (|x| > 0.01) of the first line in drawn.plan (cached TTS), in a child process."""
    code, out = run([sys.executable, os.path.abspath(__file__), "--_onset", spec_path, work])
    m = re.search(r"ONSET (\S+)", out)
    return float(m.group(1)) if m and m.group(1) != "None" else None


def _onset_child(spec_path, work):
    sys.path.insert(0, HERE)
    import contextlib
    import drawn
    with contextlib.redirect_stdout(io.StringIO()):
        beats, _ = drawn.plan(drawn.drawn_macros.expand(json.load(open(spec_path))), work)
    on = np.nonzero(np.abs(beats[0]["audio"]) > 0.01)[0]
    print("ONSET", round(beats[0]["t0"] + on[0] / drawn.SR, 3) if len(on) else None)


def probe(mp4):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height:format=duration",
                          "-of", "json", mp4], capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    return float(j["format"]["duration"]), (v["width"], v["height"]), sorted(s["codec_type"] for s in j["streams"])


def contact(mp4, jpg, dur):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-vf", f"fps=2,scale=216:384,tile=10x{int(dur * 2 / 10) + 1}",
                    "-frames:v", "1", "-q:v", "4", jpg], check=True)


def g(ok, detail):
    return {"pass": bool(ok), "detail": detail}


def gate_video(v):
    """All post-render gates for one video; fills v['gates'] (runs in a worker thread)."""
    G = v["gates"]
    mp4 = v["mp4"]
    try:
        dur, wh, kinds = probe(mp4)
        v["duration"] = round(dur, 2)
        lo, hi = WINDOWS[v["cut"]]
        G["duration"] = g(lo <= dur <= hi and kinds == ["audio", "video"], f"{dur:.2f} s (window {lo:g}-{hi:g}), streams {kinds}")
        G["size"] = g(tuple(wh) == SIZE, f"{wh[0]}x{wh[1]}")
        x = decode(mp4)
        e_on, p_on = energy_onset(x), plan_onset(v["spec"], v["work"])
        G["first_voice"] = g(e_on is not None and p_on is not None and e_on < 0.1 and p_on < 0.1,
                             f"plan {p_on} s, mix energy {e_on} s (< 0.1)")
        z = zap_count(x)
        G["zaps"] = g(not z, f"{len(z)} zap(s)" + (f" at {z[:8]} s" if z else ""))
        if v["cut"] == "yt":
            if BRAIN:
                code, out = run([sys.executable, os.path.join(BRAIN, "vidcheck.py"), mp4])
                G["vidcheck"] = g(code == 0, " ".join(out.split())[:200])
            else:
                G["vidcheck"] = g(False, "channel-brain vidcheck.py not found (set CHANNEL_BRAIN_TOOLS)")
        if not os.path.exists(v["contact"]):
            contact(mp4, v["contact"], dur)
        G["contact"] = g(os.path.exists(v["contact"]), v["contact"])
    except Exception as e:   # a broken file is a failed gate, not a crashed batch
        G["error"] = g(False, f"gate error: {e}"[:300])
    v["pass"] = passed(v)
    return v


def passed(v):
    """Every gate this cut needs was RUN and passed: a gate that never ran (crash, early exit) is a failure."""
    need = [k for k in GATES if not (k == "vidcheck" and v["cut"] != "yt")]
    G = v["gates"]
    return all(k in G for k in need) and all(x["pass"] for x in G.values())


# ---------------------------------------------------------------- outline -> render
def load(path):
    return yaml.safe_load(open(path))


def cuts_for(o, only):
    if only:
        return [only]
    return ["yt"] + (["tt"] if o.get("tt") else [])


def child_env(out, **kw):
    """Children write their temp files (facts.py TTS, tempfile users) to the batch dir in /dev/shm, never to /tmp on /."""
    tmp = os.path.join(out, "tmp")
    os.makedirs(tmp, exist_ok=True)
    return dict(os.environ, TMPDIR=tmp, **kw)


def drawn_quick(outline, cut, work, render_dir, jobs, force, render):
    env = child_env(os.path.dirname(work), DRAWN_OUT=render_dir, DRAWN_WORK=work, DRAWN_JOBS=str(jobs))
    cmd = [sys.executable, os.path.join(HERE, "drawn_quick.py"), outline, "--only", cut, "--work", work]
    cmd += [] if render else ["--no-render"]
    cmd += ["--force"] if force else []
    code, out = run(cmd, env=env)
    m = re.search(rf"^{cut}: ([\d.]+) s \((.*?)\)", out, re.M)
    return code, out, (float(m.group(1)) if m else None), (m.group(2) if m else "no length line")


def lint(outline):
    if not BRAIN:
        return g(False, "channel-brain outline_lint.py not found (set CHANNEL_BRAIN_TOOLS)")
    code, out = run([sys.executable, os.path.join(BRAIN, "outline_lint.py"), outline])
    return g(code == 0, " | ".join(x.strip() for x in out.strip().splitlines())[:300])


def preflight(outline, args):
    """Lint + spec + spoken length (TTS cached) for every cut of one outline, before any render."""
    o = load(outline)
    slug = o["slug"]
    lint_g = lint(outline)
    # run on its own: drawn_quick --force skips the sameness gate silently, so --force must not hide it here
    code, out = run([sys.executable, os.path.join(HERE, "sameness.py"), outline])
    same_g = g(code == 0, " | ".join(x.strip() for x in out.strip().splitlines() if x.strip())[-300:])
    vids = []
    for cut in cuts_for(o, args.only):
        work = os.path.join(args.out, "work", f"{slug}-{cut}")
        rdir = os.path.join(args.out, "render", slug)
        os.makedirs(work, exist_ok=True)
        os.makedirs(rdir, exist_ok=True)
        code, out, L, note = drawn_quick(outline, cut, os.path.join(args.out, "work"), rdir, args.jobs, args.force, False)
        v = {"outline": os.path.abspath(outline), "slug": slug, "cut": cut, "episode_dir": o.get("out", "episodes/drawn-house"),
             "spec": os.path.join(ROOT, o.get("specs", "scripts/drawn-house"), f"{slug}-{cut}.json"),
             "work": work, "render_dir": rdir, "mp4": os.path.join(rdir, f"{cut}-{slug}.mp4"),
             "contact": os.path.join(rdir, f"{cut}-{slug}-contact-2fps.jpg"), "spoken_s": L, "pass": False,
             "gates": {"lint": lint_g, "sameness": same_g}}
        lo, hi = WINDOWS[cut]   # ship's window, not drawn_quick's looser one: a too-long cut never costs a render
        # --force lets the render go ahead, but the gate still reports the truth (a forced cut never ships as PASS)
        v["gates"]["length"] = g(code == 0 and L is not None and lo <= L <= hi,
                                 f"{L} s spoken, window {lo:g}-{hi:g} ({note})" if L else out.strip()[-300:])
        vids.append(v)
    return vids


def render_key(v):
    """Outline + spec + title-bar table content + renderer mtimes: same key = the mp4 on disk is still this render.
    data/tt_headers.json is in it because drawn_quick burns its title bar into both cuts; ship.py itself is not."""
    h = hashlib.sha256(open(v["outline"], "rb").read() + open(v["spec"], "rb").read())
    hdr = os.path.join(ROOT, "data", "tt_headers.json")
    h.update(open(hdr, "rb").read() if os.path.exists(hdr) else b"")
    h.update(str(max(os.path.getmtime(p) for p in glob.glob(os.path.join(HERE, "*.py"))
                     if os.path.basename(p) != "ship.py")).encode())
    return h.hexdigest()


def render(v, args):
    t0 = time.time()
    keyf = os.path.join(v["work"], "render.key")
    if not args.rerender and os.path.exists(v["mp4"]) and os.path.exists(keyf) and open(keyf).read() == render_key(v):
        v["render_s"] = 0
        v["gates"]["render"] = g(True, "reused: outline, spec and renderer unchanged since the last render (--rerender to redo)")
        return True
    code, out, _, _ = drawn_quick(v["outline"], v["cut"], os.path.join(args.out, "work"), v["render_dir"], args.jobs, args.force, True)
    v["render_s"] = round(time.time() - t0)
    lines = out.strip().splitlines()
    cause = [x.strip() for x in lines if re.match(r"\s*\w*(Error|Exception)\b", x) and "CalledProcessError" not in x][:1]
    tail = cause or [x for x in lines if "frame " not in x][-3:]   # the root cause (e.g. KeyError: 'sp.<creature>')
    ok = code == 0 and os.path.exists(v["mp4"])
    v["gates"]["render"] = g(ok, f"{v['render_s']} s" + ("" if ok else " | " + " | ".join(tail)[-300:] +
                                                         f" (log {v['work']}/render.log)"))
    open(os.path.join(v["work"], "render.log"), "w").write(out)
    if ok:
        open(keyf, "w").write(render_key(v))
    return ok


# ---------------------------------------------------------------- push
NET = re.compile(r"could not resolve|unable to access|connection|timed out|rpc failed|early eof|hung up|"
                 r"tls|ssl|http 5\d\d|\b50[234]\b|reset by peer", re.I)
NONFF = re.compile(r"non-fast-forward|fetch first|\[rejected\]|failed to update ref|stale info", re.I)


def git(repo, *a, env=None, check=True, inp=None):
    """stdout only (a warning on stderr must never end up inside a SHA or a path list)."""
    code, out, err = run(["git", "-C", repo, *a], env=env, inp=inp, split=True)
    if check and code:
        raise RuntimeError(f"git {' '.join(a)} failed: {(out + err).strip()[-400:]}")
    return out.strip()


def with_retry(fn, what):
    for k, wait in enumerate((2, 4, 8, 16, None)):
        code, out = fn()
        if code == 0 or not NET.search(out) or wait is None:
            return code, out
        log(f"{what}: network error, retry {k + 1}/4 in {wait} s")
        time.sleep(wait)


def repo_layout(args):
    code, top = run(["git", "-C", ROOT, "rev-parse", "--show-toplevel"])
    repo = args.repo or (top.strip() if code == 0 else "/home/user/skills")
    sub = os.path.relpath(ROOT, repo) if code == 0 and not args.repo else args.repo_subdir
    branch = args.branch or git(repo, "branch", "--show-current")
    if not branch:
        raise RuntimeError(f"{repo} has a detached HEAD: pass --branch")
    if branch in ("main", "master") and not args.branch:
        raise RuntimeError(f"{repo} is on {branch!r}: refusing to push there by default (pass --branch {branch} to mean it)")
    return repo, sub, branch


def push_files(vids, sub):
    """(source path, repo path) pairs for the passing videos: mp4 + contact sheet + outline + spec."""
    files = {}
    for v in vids:
        d = f"{sub}/{v['episode_dir']}"
        files[f"{d}/{os.path.basename(v['mp4'])}"] = v["mp4"]
        files[f"{d}/{os.path.basename(v['contact'])}"] = v["contact"]
        rel = os.path.relpath(v["outline"], ROOT)
        files[f"{sub}/{rel if not rel.startswith('..') else 'scripts/drawn-house/outlines/' + os.path.basename(v['outline'])}"] = v["outline"]
        files[f"{sub}/{os.path.relpath(v['spec'], ROOT)}"] = v["spec"]
        v["repo_path"] = f"{d}/{os.path.basename(v['mp4'])}"
    return files


def build_commit(repo, branch, files, msg, env):
    base = git(repo, "rev-parse", f"refs/remotes/origin/{branch}", env=env)
    git(repo, "read-tree", base, env=env)
    for path, src in sorted(files.items()):
        sha = git(repo, "hash-object", "-w", "--no-filters", src, env=env)
        git(repo, "update-index", "--add", "--cacheinfo", f"100644,{sha},{path}", env=env)
    tree = git(repo, "write-tree", env=env)
    if tree == git(repo, "rev-parse", f"{base}^{{tree}}", env=env):   # a re-run: these exact files are already on origin
        log(f"origin/{branch} already holds these exact files: no new commit")
        return base, base
    return base, git(repo, "commit-tree", tree, "-p", base, env=env, inp=msg)


def commit_message(vids, args):
    subj = args.message or f"Ship {len(vids)} drawn Short(s): " + ", ".join(f"{v['cut']}-{v['slug']}" for v in vids)
    body = "\n".join(f"- {v['cut']}-{v['slug']} ({v.get('duration')} s): " + ", ".join(f"{k} PASS" for k in v["gates"])
                     for v in vids)
    return f"{subj}\n\nGates (tools/ship.py):\n{body}\n\n{trailer()}\n"


def push(vids, args):
    """One commit with only the passing files, on origin/<branch>, without touching the real index."""
    repo, sub, branch = repo_layout(args)
    files = push_files(vids, sub)
    dry = args.dry_push
    env = dict(os.environ, GIT_INDEX_FILE=os.path.join(args.out, "git-index"))
    if dry:   # objects go to a scratch store in /dev/shm (repo objects readable as alternates): the repo is untouched
        objs = os.path.join(args.out, "git-objects")
        os.makedirs(objs, exist_ok=True)
        common = os.path.join(repo, git(repo, "rev-parse", "--git-common-dir"))
        env.update(GIT_OBJECT_DIRECTORY=objs, GIT_ALTERNATE_OBJECT_DIRECTORIES=os.path.join(common, "objects"))
    copies = [(src, os.path.join(repo, path)) for path, src in files.items()
              if os.path.abspath(src) != os.path.abspath(os.path.join(repo, path))]
    need = sum(os.path.getsize(s) for s, _ in copies) * 2 + 150e6
    free = shutil.disk_usage(repo).free
    copy = args.copy and free > need   # default: renders stay in /dev/shm; the worktree gets skip-worktree entries
    blobs = sum(os.path.getsize(s) for s in files.values())
    if not dry and free < blobs + 100e6:
        raise RuntimeError(f"only {free / 1e6:.0f} MB free on the repo disk; the commit's blobs need {blobs / 1e6:.0f} MB + 100 MB")
    if args.copy and not copy:
        log(f"only {free / 1e6:.0f} MB free on the repo disk (need {need / 1e6:.0f}): not copying mp4s into the worktree")
    msg = commit_message(vids, args)
    open(os.path.join(args.out, "commit-message.txt"), "w").write(msg)
    # explicit refspec: origin/<branch> is updated even if remote.origin.fetch is narrowed
    fetch = lambda: run(["git", "-C", repo, "fetch", "origin", f"+refs/heads/{branch}:refs/remotes/origin/{branch}"])   # noqa: E731
    for attempt in range(4):
        if dry:
            log(f"DRY: git -C {repo} fetch origin {branch}   (skipped; using the local origin/{branch})")
        else:
            code, out = with_retry(fetch, "fetch")
            if code:
                raise RuntimeError(f"fetch failed: {out[-300:]}")
        base, sha = build_commit(repo, branch, files, msg, env)
        log(f"commit {sha} on origin/{branch} {base[:9]} ({len(files)} files)")
        if dry:
            for c in [f"cp {s} {d}" for s, d in copies] if copy else []:
                log(f"DRY: {c}")
            log(f"DRY: git -C {repo} push origin {sha}:refs/heads/{branch}")
            log(f"DRY: git -C {repo} update-ref refs/heads/{branch} {sha} <HEAD, only if HEAD is an ancestor>; "
                f"reset -q (index only); skip-worktree for the new paths missing on disk")
            break
        code, out = with_retry(lambda: run(["git", "-C", repo, "push", "origin", f"{sha}:refs/heads/{branch}"]), "push")
        if code == 0:
            break
        if NONFF.search(out) and attempt < 3:
            log("push rejected (origin moved): re-fetching and rebuilding the commit")
            continue
        raise RuntimeError(f"push failed: {out[-400:]}")
    show = git(repo, "show", "--stat", "--format=%H%n%P%n%B", sha, env=env)
    if not dry:
        for src, dst in copies if copy else []:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
        try:   # the push already landed: a failed local sync (e.g. another agent holds index.lock) must not hide that
            sync_worktree(repo, branch, sha, files, copy)
        except Exception as e:
            log(f"pushed {sha[:9]} OK, but the local checkout was not synced: {e}")
    for v in vids:
        v["sha"] = sha
        v["raw_url"] = f"https://raw.githubusercontent.com/{OWNER_REPO}/{sha}/{urllib.parse.quote(v['repo_path'])}"
        v["url_ok"] = None if dry else url_ok(v["raw_url"])
    return sha, show


def sync_worktree(repo, branch, sha, files, copy):
    """Bring the shared checkout up to the pushed commit without losing anyone's work:
    - fast-forward only: HEAD must be an ancestor of sha, so a local commit that is not on origin is never orphaned;
    - compare-and-swap on the ref: if another agent commits between the check and the move, it wins and we skip;
    - the index (never the worktree) is reset to HEAD; skip-worktree only for the paths this fast-forward brought in
      that are not on disk (other agents' pushed mp4s, ours with no worktree copy), never for files someone deleted."""
    sym = git(repo, "symbolic-ref", "-q", "HEAD", check=False)
    if sym != f"refs/heads/{branch}":
        log(f"worktree HEAD is {sym or 'detached'!r}, not refs/heads/{branch}: local branch left alone")
        return
    old = git(repo, "rev-parse", "HEAD")
    if old != sha:
        if run(["git", "-C", repo, "merge-base", "--is-ancestor", old, sha])[0]:
            log(f"local {branch} {old[:9]} has commits that are not on origin: NOT moved (push those, then sync it)")
            return
        code, _, err = run(["git", "-C", repo, "update-ref", "-m", "ship.py: fast-forward to the pushed commit",
                            f"refs/heads/{branch}", sha, old], split=True)
        if code:
            log(f"local {branch} moved while shipping: NOT moved ({err.strip()[-200:]})")
            return
    git(repo, "reset", "-q")   # index only, to whatever HEAD is now
    new = git(repo, "diff", "--name-only", "-z", "--diff-filter=d", old, sha).split("\0")
    hide = [p for p in new if p and not os.path.lexists(os.path.join(repo, p))]
    if not copy:   # an OLDER copy of a shipped file in the worktree would show as modified; an identical one is fine
        hide += [p for p, src in files.items() if p not in hide and os.path.isfile(os.path.join(repo, p))
                 and os.path.abspath(src) != os.path.abspath(os.path.join(repo, p))
                 and not filecmp.cmp(src, os.path.join(repo, p), shallow=False)]
    for k in range(0, len(hide), 200):
        git(repo, "update-index", "--skip-worktree", "--", *hide[k:k + 200])
    log(f"local {branch} " + (f"fast-forwarded {old[:9]} -> {sha[:9]}" if old != sha else f"already at {sha[:9]}") +
        f"; {len(hide)} path(s) not on disk (or stale) marked skip-worktree")


def url_ok(url, tries=5):
    for k in range(tries):
        code, out = run(["curl", "-sI", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "30", url])
        if out.strip() == "200":
            return True
        time.sleep(2 * (k + 1))
    return False


# ---------------------------------------------------------------- Metricool payloads
def sequel_map():
    p = os.path.join(ROOT, "data", "sequel-related-video-map.csv")
    return {r["new_title"]: r for r in csv.DictReader(open(p))} if os.path.exists(p) else {}


def question(caption):
    text = caption.split("#")[0].strip()
    qs = [s for s in re.split(r"(?<=[.!])\s+", text) if "?" in s]
    return qs[-1].strip() if qs else ""


def when(s):
    """'YYYY-MM-DD HH:MM' (or a YAML datetime) in New York -> (aware datetime, ISO with offset, local wall time)."""
    t = dt.datetime.strptime(str(s).strip().replace("T", " ")[:16], "%Y-%m-%d %H:%M").replace(tzinfo=zoneinfo.ZoneInfo(TZ))
    return t, t.isoformat(), t.strftime("%Y-%m-%dT%H:%M:%S")


def payloads(vids, args):
    seq = sequel_map()
    calls, rows = [], []
    by = {(v["slug"], v["cut"]): v for v in vids}
    for slug in dict.fromkeys(v["slug"] for v in vids if "mp4" in v):   # an outline that never loaded has no post
        o = load(next(v for v in vids if v["slug"] == slug)["outline"])
        title = o.get("yt_title", o["title"])
        cap = o.get("tt_caption", o.get("tiktok_caption", ""))
        sq = seq.get(title, {})
        pinned = o.get("pinned") or ("Part 1 is in the Related video 👆" if sq else question(cap))
        ttcut = o.get("tt_cut", "long" if o.get("tt") else "short")
        posts = [("youtube", by.get((slug, "yt")), o.get("yt_date") or sq.get("date"))]
        if o.get("tt_date"):
            posts.append(("tiktok", by.get((slug, "tt" if ttcut == "long" else "yt")), o["tt_date"]))
        for net, v, date in posts:
            probs = []
            if v is None:   # e.g. tt_date set but this batch ran --only yt: say so instead of dropping the post
                calls.append({"slug": slug, "network": net, "file": None, "ready": False, "args": {"date": None},
                              "problems": [f"no {'tt' if net == 'tiktok' and ttcut == 'long' else 'yt'} render in this batch"]})
                continue
            if not v.get("pass"):
                probs.append("video failed a gate")
            if not v.get("raw_url"):
                probs.append("no raw URL (run with --push)")
            elif not v.get("url_ok"):
                probs.append("raw URL not verified 200")
            if not date:
                probs.append(f"no {'yt' if net == 'youtube' else 'tt'}_date in the outline")
            iso = local = None
            if date:
                try:
                    t, iso, local = when(date)
                    if t < dt.datetime.now(zoneinfo.ZoneInfo(TZ)):
                        probs.append(f"date {date} is in the past")
                except ValueError:
                    probs.append(f"date {date!r} is not 'YYYY-MM-DD HH:MM'")
            if net == "youtube" and len(title) > 100:
                probs.append(f"title is {len(title)} chars (YouTube max 100)")
            ask = pinned if "?" in pinned else question(cap)   # the description opens with the pinned question
            text = (o.get("yt_text") or "\n\n".join(x for x in (ask, title, "Sources: " + "; ".join(
                str(s).split(":")[0].split(",")[0] for s in o.get("sources", []))) if x)) if net == "youtube" else cap
            info = {"autoPublish": True, "draft": False, "descendants": [], "firstCommentText": pinned if net == "youtube" else "",
                    "hasNotReadNotes": False, "media": [v.get("raw_url")] if v.get("raw_url") else [], "mediaAltText": [],
                    "providers": [{"network": net}], "publicationDate": {"dateTime": local, "timezone": TZ},
                    "shortener": False, "smartLinkData": {"ids": []}, "text": text}
            if net == "youtube":
                info["youtubeData"] = {"title": title, "type": "short", "privacy": "public", "madeForKids": False,
                                       "isAiGeneratedContent": True, "category": "EDUCATION"}
            else:
                info["tiktokData"] = {"isAigc": True}
            if not str(text).strip():
                probs.append(f"empty post text ({'yt_text/question/title' if net == 'youtube' else 'tt_caption/tiktok_caption'})")
            # args is the exact tool call: the MCP "info" parameter is a JSON STRING; info_preview is for reading
            calls.append({"slug": slug, "network": net, "file": os.path.basename(v["mp4"]), "ready": not probs,
                          "problems": probs, "related_video": sq.get("part1_video_id"),
                          "tool": "mcp__Metricool_Social_Media_Management__createScheduledPost",
                          "args": {"blogId": BLOG_ID, "date": iso, "info": json.dumps(info, ensure_ascii=False)},
                          "info_preview": info})
            if v.get("pass"):
                rows.append([date or "?", net, os.path.basename(v["episode_dir"]), os.path.basename(v["mp4"]),
                             title if net == "youtube" else o.get("tt_title", title)])
    return calls, rows


# ---------------------------------------------------------------- main
def table(vids):
    head = f"{'video':34s} " + " ".join(f"{k[:7]:>7s}" for k in GATES) + "  result"
    lines = [head, "-" * len(head)]
    for v in vids:
        cells = [("PASS" if v["gates"][k]["pass"] else "FAIL") if k in v["gates"] else "-" for k in GATES]
        lines.append(f"{v['cut'] + '-' + v['slug']:34.34s} " + " ".join(f"{c:>7s}" for c in cells) +
                     f"  {'PASS' if v['pass'] else 'FAIL'}  {v.get('duration', '')}")
        lines += [f"    {k}: {x['detail']}" for k, x in v["gates"].items() if not x["pass"]]
    return "\n".join(lines)


def main():
    if len(sys.argv) == 4 and sys.argv[1] == "--_onset":
        return _onset_child(sys.argv[2], sys.argv[3])
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outlines", nargs="+")
    ap.add_argument("--only", choices=["yt", "tt"])
    ap.add_argument("--out", help="batch dir (default /dev/shm/ship/<YYYYMMDD-HHMM>)")
    ap.add_argument("--push", action="store_true", help="commit + push the passing videos, verify raw URLs")
    ap.add_argument("--dry-push", action="store_true", help="build the commit in a scratch object store; no push/reset")
    ap.add_argument("--copy", action="store_true", help="also copy the mp4s/jpgs into the worktree on the root disk "
                    "(default: no copy, the new paths are marked skip-worktree; / is nearly full)")
    ap.add_argument("--no-copy", action="store_true", help=argparse.SUPPRESS)   # the default now; kept for old commands
    ap.add_argument("--schedule-json", action="store_true")
    ap.add_argument("--jobs", type=int, default=int(os.environ.get("DRAWN_JOBS", "4")), help="render processes")
    ap.add_argument("--rerender", action="store_true", help="render even if this batch dir already holds the same render")
    ap.add_argument("--force", action="store_true", help="render past lint/length failures (gates still report)")
    ap.add_argument("-m", "--message", help="commit subject (the gate list and trailers are appended)")
    ap.add_argument("--repo", help="git repo (default: the repo holding tools/, else /home/user/skills)")
    ap.add_argument("--repo-subdir", default="skills/oh-meatball", help="channel dir inside --repo when tools/ is outside it")
    ap.add_argument("--branch", help="default: the repo's current branch")
    args = ap.parse_args()
    t0 = time.time()
    args.out = os.path.abspath(args.out or f"/dev/shm/ship/{time.strftime('%Y%m%d-%H%M')}")
    if not args.out.startswith("/dev/shm/") and not os.environ.get("SHIP_ALLOW_DISK"):
        sys.exit(f"ship: --out {args.out} is not on /dev/shm (the root disk is nearly full); set SHIP_ALLOW_DISK=1 to override")
    os.makedirs(args.out, exist_ok=True)
    log(f"batch {args.out}: {len(args.outlines)} outline(s), jobs {args.jobs}, channel-brain {BRAIN}")

    vids = []
    with cf.ThreadPoolExecutor(3) as ex:   # network-bound (TTS): all outlines at once
        futs = {ex.submit(preflight, p, args): p for p in args.outlines}
        for f in futs:
            try:
                vids += f.result()
            except Exception as e:
                vids.append({"outline": futs[f], "slug": os.path.basename(futs[f]), "cut": args.only or "yt", "pass": False,
                             "gates": {"lint": g(False, f"can't preflight: {e}")}})
    log(f"preflight done in {time.time() - t0:.0f} s")
    for v in vids:
        log(f"  {v['cut']}-{v['slug']}: " + ", ".join(f"{k} {'ok' if x['pass'] else 'FAIL'}" for k, x in v["gates"].items()))

    with cf.ThreadPoolExecutor(1) as gx:   # gates of video N overlap the render of N+1
        pend = []
        for v in vids:
            if "mp4" not in v or (not args.force and not all(x["pass"] for x in v["gates"].values())):
                continue
            log(f"render {v['cut']}-{v['slug']} ...")
            try:
                ok = render(v, args)
            except Exception as e:   # one broken render never stops the batch
                v["gates"]["render"] = g(False, f"render error: {e}"[:300])
                ok = False
            if ok:
                log(f"{v['cut']}-{v['slug']}: {v['gates']['render']['detail'][:40]}; gating in the background")
                pend.append(gx.submit(gate_video, v))
        for f in pend:
            f.result()

    passing = [v for v in vids if v["pass"]]
    sha, push_ok = None, True
    if (args.push or args.dry_push) and passing:
        try:
            sha, show = push(passing, args)
            print(show)
        except Exception as e:
            log(f"PUSH FAILED: {e}")
            push_ok = False
    elif args.push or args.dry_push:
        log("nothing passed: no commit")

    calls, rows = payloads(vids, args) if args.schedule_json else ([], [])
    if calls:
        json.dump(calls, open(os.path.join(args.out, "schedule.json"), "w"), indent=1, ensure_ascii=False)
    print("\n" + table(vids))
    if args.push or args.dry_push:
        for v in passing:
            print(f"  {v.get('raw_url')}  {'HTTP 200' if v.get('url_ok') else 'dry-push: not pushed' if args.dry_push else 'NOT 200'}")
    if calls:
        print(f"\nMetricool: {sum(c['ready'] for c in calls)}/{len(calls)} ready in {args.out}/schedule.json")
        for c in calls:
            print(f"  {c['network']:8s} {c['args']['date']}  {c['file']}  " + ("ready" if c["ready"] else "; ".join(c["problems"])))
        buf = io.StringIO()
        csv.writer(buf, lineterminator="\n").writerows(rows)
        print("\nposted.csv rows to append (not written):\n" + buf.getvalue().rstrip())
    res = {"out": args.out, "sha": sha, "elapsed_s": round(time.time() - t0), "videos": vids}
    json.dump(res, open(os.path.join(args.out, "results.json"), "w"), indent=1, ensure_ascii=False)
    print(f"\n{len(passing)}/{len(vids)} passed in {time.time() - t0:.0f} s; results {args.out}/results.json")
    if args.push and not args.dry_push and sha and not all(v.get("url_ok") for v in passing):
        push_ok = False
        log("a raw URL did not answer HTTP 200: do not schedule those posts")
    # 0 only if every video passed AND (when asked) the push landed and every raw URL answers 200
    sys.exit(0 if vids and len(passing) == len(vids) and push_ok else 1)


if __name__ == "__main__":
    main()
