#!/usr/bin/env python3
"""Post kit: the checks and chores between a finished spec and a scheduled post, as commands instead of hand work.

  postkit.py render SPEC OUT.mp4 --work DIR       render with drawn.py, refuse a stale file, then voicecheck
  postkit.py voicecheck SPEC MP4 [--model small.en]
  postkit.py sheet MP4 OUT.jpg [--step 1.5] [--cols 9]
  postkit.py lint SPEC [SPEC ...] [--mp4 FILE]    titles, descriptions, tags, hashtags, captions, swear words, lengths
  postkit.py selftest                             lint on built-in good and bad specs; fails if a rule stopped working
  postkit.py payload SPEC --net youtube|tiktok --when 2026-11-13T16:00:00 --media https://URL
                     [--call | --update ID UUID] [--cover-ms 1900] [--kind short|video] [--thumb URL] [--first-comment TEXT]
  postkit.py log --net youtube|tiktok --when "2026-11-13 16:00" --file OUT.mp4 (--title T | --spec SPEC)
                 [--episode E] [--uuid U --id I --media URL]
  postkit.py rawurl FILE [--sha SHA]              raw.githubusercontent.com URL of a pushed file (same bytes, answers 200)
  postkit.py rehost URL FILE                      the scheduler's copy has the same size as the local file
  postkit.py kw "seed" ["seed" ...] [--search "query" ...] [--out FILE] [--n 25]
  postkit.py ttpage URL [URL ...] [--json OUT] [--csv FILE]

What each prints:
  payload     default: the Metricool post object (the "info" of a create or update call).
              --call: the exact arguments of createScheduledPost, {"blogId", "date" with the New York offset, "info"}.
              --update ID UUID: the exact arguments of updateScheduledPost, {"blogId", "id", "uuid", "info"}.
              It runs lint first and prints nothing on stdout when lint fails or the spec is for the other network.
  log         a row is found by (network, file name), plus the episode when --episode is given. Two or more rows
              match: it stops and asks for --episode. No row: it adds one (episode = --episode or "drawn-house").
  ttpage      --csv appends one row per video that returned data (date_utc, video_id, url, plays, likes, comments,
              shares, saves, label, ai_label = TikTok's aigcLabelType, flag = "reviewing" or "penalty N",
              suggested_words joined by "|"). It stops at the first "no page data" answer; never retry in a loop.

Why each exists (all from 2026-11-12, research 92 to 94):
  render      drawn.py exits non-zero and leaves the OLD mp4 in place when the voice service returns no audio.
              One of 14 cuts kept its old file that way and only a transcript showed it. This renders to
              OUT.new.mp4 and moves it over OUT only after the voice check passes.
  voicecheck  the voice service can drop a word or stop a line early with no error.
  lint        the metadata standard in MASTER_ORDERS ("Tags and everything, from every angle") as a gate.
  payload     Metricool's update call needs the whole post again; hand-typed payloads lose a word or an emoji.
  log         data/posted.csv must follow every scheduling change; data/post-ids.csv keeps each post's uuid.
  kw, ttpage  what people type (YouTube and Google suggestions, top results) and what TikTok shows for a video
              (plays, category label, its own suggested searches), from public pages only. Both read formats
              nobody promised to keep: suggestqueries JSON and TikTok's page JSON, both last seen working 2026-11-12.
Nothing here schedules, posts or spends credits. Exit code 1 means a FAIL line was printed.
"""
import argparse
import contextlib
import copy
import csv
import datetime
import difflib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # skills/oh-meatball
REPO = os.path.dirname(os.path.dirname(ROOT))      # repository root

# ---------------------------------------------------------------- every fixed value, with where it comes from
CFG = {
    "brand": "7521392",               # Metricool brand id (blogId) of the channel
    "github": "mooneyn60-art/skills", # where rawurl points
    "tz": "America/New_York",         # Metricool posts are scheduled in New York time
    "yt_title_max": 100,              # YouTube title limit, UTF-16 units (MASTER_ORDERS "Tags and everything" item 1)
    "yt_desc_max": 5000,              # YouTube description limit (research 93, section 1)
    "yt_tag_max": 30,                 # each tag 30 characters or fewer (MASTER_ORDERS item 3, research 93)
    "yt_tags_total_max": 500,         # all tags together (research 93, section 1)
    "yt_tags_count": (8, 12),         # 8 to 12 tags (MASTER_ORDERS item 3)
    "yt_hashtags": 4,                 # two topic, #meatballmyths, #shorts last (MASTER_ORDERS item 2)
    "tt_caption_max": 2200,           # TikTok caption, UTF-16 units (research 93, section 2, TikTok API docs)
    "tt_hashtags": 5,                 # five topic hashtags (MASTER_ORDERS item 4)
    "short_s": (15.0, 20.05),         # YouTube Short length: no Short under 15 s, run 16 to 20 s (MASTER_ORDERS)
    "tt_short_s": (20.0, 26.5),       # TikTok search-led cut: 20 to 26 s (MASTER_ORDERS, search-led test)
    "tt_rewards_s": 61.0,             # a TikTok Rewards cut runs 61 s or more
    "mild_max": 2,                    # mild words in a YouTube Short, two at most (MASTER_ORDERS)
}
GITHUB, BRAND, TZ = CFG["github"], CFG["brand"], CFG["tz"]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
WHEN_FMT = "%Y-%m-%dT%H:%M:%S"

MILD = {"damn", "hell", "ass", "dumbass", "badass", "bastard", "bastards"}          # allowed in YouTube speech
STRONG = {"fuck", "fucks", "fucking", "fucked", "fucker", "fuckers", "motherfucker", "shit", "shits", "shitty",
          "bullshit", "bitch", "bitches", "asshole", "assholes", "crap", "piss", "pissed", "dick", "cock", "pussy"}
STRONG_STEM = re.compile(r"fuck|shit|bitch|asshole|pussy")   # also catches shitballs, motherfucking, dipshit
BANNED_TITLE = ["true or false", "myth", "believe", "cartoons", "lied", "did you know"]   # MASTER_ORDERS, banned title words
PLACEHOLDER = re.compile(r"\b(UNCHECKED|TODO|PLACEHOLDER|FIXME|TBD)\b", re.I)
TT_DEAD_TAGS = {"fyp", "foryou", "foryoupage", "viral", "fypシ", "xyzbca"}
BARE_DOMAIN = re.compile(r"\b[\w-]+\.(com|net|org|io|ly|gg|tv|co|us|me|app|link)\b", re.I)
TT_URL = re.compile(r"https://(www\.)?tiktok\.com/@[^/?#\s]+/video/\d+")
_EMO = "\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\u2300-\u23FF\u203C\u2049"
# one visible emoji = a flag pair, or a base with an optional skin tone or U+FE0F, joined by U+200D to more of them
EMOJI = re.compile("(?:[\U0001F1E6-\U0001F1FF]{2}|[%s](?:[\U0001F3FB-\U0001F3FF]|\uFE0F)?"
                   "(?:\u200D[%s](?:[\U0001F3FB-\U0001F3FF]|\uFE0F)?)*)" % (_EMO, _EMO))


def u16(s):
    """Length the way YouTube and TikTok count it: UTF-16 units (an emoji is 2)."""
    return len(s.encode("utf-16-le")) // 2


def words(s):
    s = s.lower().replace("\u2019", "'").replace("\u2018", "'")
    return re.sub(r"[^a-z0-9' ]", " ", s).split()


def swear_tokens(text):
    """Words as a swear check reads them: 's 'd 'll 're 've dropped, a final in' read as ing (fuckin' -> fucking)."""
    out = []
    for w in words(text):
        w = w.lstrip("'")
        if w.endswith("in'"):
            w = w[:-1] + "g"
        w = re.sub(r"'(s|d|ll|re|ve)$", "", w).rstrip("'")
        if w:
            out.append(w)
    return out


def is_strong(w):
    return w in STRONG or bool(STRONG_STEM.search(w))


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def duration(mp4):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4],
                         capture_output=True, text=True).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return 0.0


class Report:
    def __init__(self, name):
        self.name, self.fails, self.warns = name, 0, 0

    def fail(self, msg):
        self.fails += 1
        print("  FAIL %s" % msg)

    def warn(self, msg):
        self.warns += 1
        print("  WARN %s" % msg)

    def ok(self, msg):
        print("  ok   %s" % msg)


# ---------------------------------------------------------------- voicecheck
def speech_libs():
    """None when faster_whisper and soundfile import, else the error text."""
    try:
        import soundfile  # noqa: F401
        import faster_whisper  # noqa: F401
    except Exception as e:                           # ImportError, or a broken native library
        return "%s: %s (run bash tools/setup_env.sh)" % (type(e).__name__, e)
    return None


def transcribe(mp4, model="small.en"):
    import soundfile as sf
    from faster_whisper import WhisperModel
    fd, wav = tempfile.mkstemp(prefix="postkit-", suffix=".wav")
    os.close(fd)
    try:
        p = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-vn", "-ac", "1", "-ar", "16000", wav],
                           capture_output=True, text=True)
        if p.returncode != 0:
            raise RuntimeError("ffmpeg: " + (p.stderr.strip().splitlines() or ["no audio track"])[-1])
        audio, _ = sf.read(wav, dtype="float32")
    finally:
        if os.path.exists(wav):
            os.remove(wav)
    if len(audio) == 0:
        raise RuntimeError("empty audio track")
    m = WhisperModel(model, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(audio, language="en", beam_size=5, condition_on_previous_text=False)
    return " ".join(s.text for s in segs)


def voicecheck(spec_path, mp4, model="small.en", quiet=False):
    """Every line of the spec is heard, in order, to its last words. Returns the number of FAILs."""
    print("voicecheck %s" % os.path.basename(mp4))
    try:
        spec = load(spec_path)
    except (OSError, ValueError) as e:
        print("  FAIL cannot read the spec %s (%s)" % (spec_path, e))
        return 1
    lines = [b["say"] for b in spec.get("beats") or [] if isinstance(b, dict) and b.get("say")]
    if not lines:
        print("  FAIL the spec has no spoken lines (no beats with 'say')")
        return 1
    want, owner = [], []
    for i, line in enumerate(lines):
        w = words(line)
        want += w
        owner += [i] * len(w)
    err = speech_libs()
    if err:
        print("  FAIL the speech model cannot load: %s" % err)
        return 1
    if not os.path.isfile(mp4):
        print("  FAIL no such file: %s" % mp4)
        return 1
    try:
        heard_text = transcribe(mp4, model)
    except Exception as e:                           # no audio stream, a garbage file, a model that fails to load
        print("  FAIL cannot read the audio of %s (%s)" % (mp4, str(e)[:200]))
        return 1
    heard = words(heard_text)
    sm = difflib.SequenceMatcher(None, want, heard, autojunk=False)
    matched = [False] * len(want)
    diffs = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for i in range(i1, i2):
                matched[i] = True
        else:
            diffs.append((tag, " ".join(want[i1:i2]), " ".join(heard[j1:j2])))
    r = Report(mp4)
    print("  (%.1f s, %d words wanted, %d heard, match %.3f)" % (duration(mp4), len(want), len(heard), sm.ratio()))
    for i, line in enumerate(lines):
        idx = [k for k, o in enumerate(owner) if o == i]
        if not idx:
            continue
        got = sum(matched[k] for k in idx) / len(idx)
        tail = idx[-2:]
        if got < 0.6:
            r.fail("line %d mostly missing (%.0f%% heard): %s" % (i + 1, got * 100, line))
        elif not any(matched[k] for k in tail):
            # one mis-heard last word is normal; two unmatched last words means the take stopped early
            r.fail("line %d ends early (last words not heard): %s" % (i + 1, line))
        elif got < 0.85:
            r.warn("line %d only %.0f%% heard: %s" % (i + 1, got * 100, line))
    if abs(len(want) - len(heard)) > max(2, round(0.03 * len(want))):
        r.fail("word count off: wanted %d, heard %d" % (len(want), len(heard)))
    for d in diffs:
        if not quiet:
            print("  note %s: wanted '%s' heard '%s'" % d)
    if not r.fails:
        r.ok("every line heard to its end")
    return r.fails


# ---------------------------------------------------------------- render
def render(spec_path, out, work):
    """Render to a side file and move it over OUT only after the voice check passes, so OUT is never half-new."""
    spec_path, out, work = os.path.abspath(spec_path), os.path.abspath(out), os.path.abspath(work)
    err = speech_libs()                              # check before a 30 s render, not after it
    if err:
        print("FAIL the voice check cannot run, so nothing was rendered: %s" % err)
        return 1
    try:
        os.makedirs(work, exist_ok=True)
    except OSError as e:
        print("FAIL cannot make the work folder %s (%s)" % (work, e))
        return 1
    new = (out[:-4] if out.endswith(".mp4") else out) + ".new.mp4"
    side = new + ".post.json"                        # drawn.py writes this next to its output; it is not ours to keep

    def drop_side():
        if os.path.exists(side):
            os.remove(side)

    if os.path.exists(new):
        os.remove(new)
    log = os.path.join(work, "render.log")
    sheet_path = os.path.join(work, "sheet.jpg")
    if os.path.exists(sheet_path):
        os.remove(sheet_path)
    t0 = time.time()
    with open(log, "w") as f:
        rc = subprocess.run([sys.executable, os.path.join(HERE, "drawn.py"), spec_path, new, "--work", work],
                            stdout=f, stderr=subprocess.STDOUT, cwd=ROOT,
                            env=dict(os.environ, DRAWN_CONTACT=sheet_path)).returncode
    drop_side()
    tail = open(log, errors="replace").read().strip().splitlines()[-3:]
    sheet_line = ("contact sheet: %s" % sheet_path) if os.path.exists(sheet_path) else "no contact sheet was written"
    if rc != 0 or not os.path.exists(new) or duration(new) <= 0:
        print("FAIL render exited %d; %s is unchanged. Last log lines:" % (rc, os.path.basename(out)))
        for line in tail:
            print("     " + line)
        if os.path.exists(new):
            os.remove(new)
        return 1
    fails = voicecheck(spec_path, new)
    if fails:
        print("FAIL voice check; the new render is kept at %s for a look and %s is unchanged" % (new, os.path.basename(out)))
        print(sheet_line)
        return 1
    os.replace(new, out)
    print("rendered %s  %.2f s  %d bytes  in %.0f s" % (out, duration(out), os.path.getsize(out), time.time() - t0))
    print(sheet_line)
    return 0


# ---------------------------------------------------------------- contact sheet
def _frame(mp4, t, w, h, tmp):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.3f" % t, "-i", mp4, "-frames:v", "1",
                    "-vf", "scale=%d:%d" % (w, h), tmp], capture_output=True)
    return os.path.exists(tmp) and os.path.getsize(tmp) > 0


def sheet(mp4, out, step=1.5, cols=9, w=216):
    from PIL import Image
    dur = duration(mp4)
    if dur <= 0:
        print("FAIL cannot read %s" % mp4)
        return 1
    ts = [round(0.4 + i * step, 2) for i in range(int(max(dur - 0.5, 0) / step) + 1)]
    last = max(dur - 0.05, 0.0)                      # the loop frame: always on the sheet
    if not ts or last - ts[-1] > 0.2:
        ts.append(last)
    h = int(w * 16 / 9)
    rows = (len(ts) + cols - 1) // cols
    img = Image.new("RGB", (w * cols, h * rows), "black")
    shown = []
    with tempfile.TemporaryDirectory(prefix="postkit-sheet-") as tmpd:
        for i, t in enumerate(ts):
            tmp = os.path.join(tmpd, "%03d.png" % i)
            got = _frame(mp4, t, w, h, tmp)
            if not got and i == len(ts) - 1:         # the very end can fall past the last video frame
                for back in (0.15, 0.3, 0.6):
                    t = max(dur - back, 0.0)
                    if _frame(mp4, t, w, h, tmp):
                        got = True
                        break
            if got:
                with Image.open(tmp) as fr:
                    img.paste(fr.convert("RGB"), ((i % cols) * w, (i // cols) * h))
                shown.append(t)
    img.save(out, quality=85)
    print("sheet %s  %d frames every %.1f s, last frame at %.2f s of %.2f s" % (
        out, len(shown), step, shown[-1] if shown else 0, dur))
    return 0 if shown else 1


# ---------------------------------------------------------------- lint
def spec_kind(path, spec):
    base = os.path.basename(path)
    if base.startswith("tts-") or base.startswith("tt-") or "search_top" in spec:
        return "tiktok"
    return "youtube"


def swears_in(text):
    """Strong words by stem (fuck, shit, ...) after dropping 's and reading in' as ing; mild words as written,
    so a place name such as Hell's Canyon stays clean."""
    strong = [w for w in swear_tokens(text) if is_strong(w)]
    return strong + [w for w in words(text) if w in MILD]


def screen_words(spec):
    """What drawn.py will print as captions: each spoken line in capitals with cap_swap applied the way
    drawn.caption_chunks applies it (a whole-word swap on the capitalised text)."""
    swap = spec.get("cap_swap") or {}
    shown = []
    for b in spec.get("beats") or []:
        txt = " ".join((b.get("say") or "").split()).upper()
        for k, v in swap.items():
            txt = re.sub(r"\b%s\b" % re.escape(k.upper()), v.upper(), txt)
        shown.append(txt)
    return shown


def hashtags(text):
    return re.findall(r"#([^\s#]+)", text)


def banned_title_words(title):
    low = re.sub(r"\s+", " ", title.lower())
    hits = []
    for b in BANNED_TITLE:
        parts = b.split()
        parts[-1] = parts[-1].rstrip("s") if len(parts[-1]) > 3 else parts[-1]
        pat = r"\b" + r"\s*".join(re.escape(p) for p in parts) + r"(s|d|ed)?\b"
        if re.search(pat, low):
            hits.append(b)
    return hits


def lint(path, mp4=None):
    try:
        spec = load(path)
    except (OSError, ValueError) as e:
        print("lint %s\n  FAIL cannot read the spec (%s)\n  => FAIL (1 fail, 0 warn)" % (path, e))
        return 1
    kind = spec_kind(path, spec)
    r = Report(path)
    print("lint %s  (%s)" % (path, kind))
    title = spec.get("title", "")
    desc = spec.get("description", "")
    tags = spec.get("tags")
    beats = [b for b in spec.get("beats") or [] if isinstance(b, dict)]
    says = [b.get("say", "") for b in beats]
    survival = "would meatball survive" in (spec.get("series", "") + " " + title).lower()
    cards = [str(row[0]) for b in beats for row in (b.get("card") or {}).get("rows", []) if row]
    cards += [str(row[0]) for row in (spec.get("search_top") or {}).get("rows", []) if row]

    # --- placeholder text left in anything a viewer sees or hears
    fields = [("title", title), ("description", desc), ("pinned_comment", spec.get("pinned_comment", "")),
              ("tiktok_title", spec.get("tiktok_title", "")), ("tiktok_caption", spec.get("tiktok_caption", "")),
              ("spoken lines", " ".join(says)), ("a card", " | ".join(cards))]
    if isinstance(tags, list):
        fields.append(("tags", " | ".join(str(t) for t in tags)))
    for label, text in fields:
        m = PLACEHOLDER.search(text or "")
        if m:
            r.fail("placeholder text '%s' in %s" % (m.group(0), label))

    # --- spoken words
    spoken = swear_tokens(" ".join(says))
    strong = [w for w in spoken if is_strong(w)]
    mild = [w for w in words(" ".join(says)) if w in MILD]
    if kind == "youtube":
        if strong:
            r.fail("strong words in a YouTube script: %s" % ", ".join(sorted(set(strong))))
        if len(mild) > CFG["mild_max"]:
            r.fail("%d mild words in a Short (two at most): %s" % (len(mild), ", ".join(mild)))
        elif not strong:
            r.ok("spoken: %d mild word(s), no strong ones" % len(mild))
    else:
        if spec.get("captions", 66):
            left = []
            for txt in screen_words(spec):
                left += [tok.rstrip(",.!?") for tok in txt.split() if any(is_strong(w) for w in swear_tokens(tok))]
            if left:
                r.fail("captions would show: %s (add a cap_swap entry for each spelling)" % ", ".join(sorted(set(left))))
            else:
                r.ok("spoken: %d strong word(s), none shown in full in the captions" % len(strong))
        else:
            r.ok("captions are off; nothing spoken is spelled on screen")

    # --- text a viewer reads besides the main fields
    for label, text in (("pinned_comment", spec.get("pinned_comment", "")), ("tiktok_title", spec.get("tiktok_title", "")),
                        ("a card", " | ".join(cards))):
        bad = [w for w in swears_in(text) if is_strong(w) or kind == "youtube"]
        if bad:
            r.fail("swear word in %s: %s" % (label, ", ".join(sorted(set(bad)))))

    # --- script traps found on 2026-11-12
    joined = " ".join(says)
    if re.search(r"\bhis (a|an|for|to|some)\b", joined, re.I):
        r.warn("a bare 'his' (write 'his cat' or 'his dog': the voice swallows it)")
    if re.search(r"\bmeowed\b", joined, re.I):
        r.warn("'meowed' is heard as 'me out' in this voice (write 'let out a meow')")
    facts = sum(1 for b in beats if b.get("_f"))
    if facts and facts < 2:                          # only specs that use fact ids are held to the count
        r.warn("%d line(s) carry a fact id '_f' (keep at least two sourced facts)" % facts)
    if spec.get("loop") and len(beats) > 2:
        first = beats[0].get("scene") or (spec.get("stage") or {}).get("scene")
        last = beats[-1].get("scene") or first
        if first and last and first != last:
            r.warn("loop is on but the last line is in '%s' and the first in '%s'" % (last, first))
    st_y = (spec.get("search_top") or {}).get("y")
    if st_y is not None and st_y < 120:
        r.warn("search_top y=%s sits under TikTok's top bar (use 120 or more)" % st_y)

    # --- YouTube title, description, tags (a TikTok spec carries the YouTube copies too; they are checked on the YouTube spec)
    if kind == "youtube":
        n = u16(title)
        core = re.sub(r"\s*\([^()]*\)\s*$", "", title)
        if not title:
            r.fail("no title")
        elif n > CFG["yt_title_max"]:
            r.fail("title is %d units (100 at most): %s" % (n, title))
        else:
            r.ok("title %d of 100 units" % n)
        low = re.sub(r"\s+", " ", title.lower())
        for b in banned_title_words(title):
            r.fail("banned title word '%s' (or a form of it)" % b)
        if "?" in core:
            r.fail("question title on YouTube (statement form only): %s" % core)
        if swears_in(title):
            r.fail("swear word in the title: %s" % ", ".join(swears_in(title)))
        emo = EMOJI.findall(title)
        if len(emo) != 1:
            r.warn("title has %d emoji (the standard is one)" % len(emo))
        series = (spec.get("series") or "").split(",")[0].strip()
        if series and series.lower() not in low:
            r.warn("title lacks the series tag '%s'" % series)
        if not desc:
            r.fail("no description")
        else:
            if swears_in(desc):
                r.fail("swear word in the description: %s" % ", ".join(swears_in(desc)))
            if not re.search(r"^Sources?:", desc, re.M):
                r.fail("description has no Sources line")
            if survival and "General information, not safety training." not in desc:
                r.fail("survival video without 'General information, not safety training.'")
            first = re.split(r"(?<=[.?!])\s", desc.strip(), maxsplit=1)[0]
            if not first.endswith("?"):
                r.warn("description does not open with the searched question: %s" % first[:80])
            ht = hashtags(desc)
            if len(ht) != CFG["yt_hashtags"]:
                r.warn("description has %d hashtags (the standard is four: two topic, #meatballmyths, #shorts)" % len(ht))
            elif ht[-1].lower() != "shorts" or "meatballmyths" not in [h.lower() for h in ht]:
                r.warn("hashtags should end '#meatballmyths #shorts': %s" % " ".join("#" + h for h in ht))
            if u16(desc) > CFG["yt_desc_max"]:
                r.fail("description is %d units (5,000 at most)" % u16(desc))
        if tags is None or tags == []:
            r.warn("no 'tags' list in the spec (payload needs one; 8 to 12 search phrases)")
        elif not isinstance(tags, list) or not all(isinstance(t, str) and t.strip() for t in tags):
            r.fail("tags must be a list of non-empty strings, like [\"cat facts\", \"can cats taste sugar\"]")
        else:
            st = [t.strip() for t in tags]
            if any(t != s for t, s in zip(tags, st)):
                r.warn("a tag has spaces at its start or end (payload sends it trimmed)")
            long_ = [t for t in st if len(t) > CFG["yt_tag_max"]]
            total = sum(len(t) for t in st) + len(st) - 1
            lows = [t.lower() for t in st]
            dups = sorted({t for t in st if lows.count(t.lower()) > 1})
            if long_:
                r.fail("tags over 30 characters: %s" % "; ".join(long_))
            if total > CFG["yt_tags_total_max"]:
                r.fail("tags total %d characters (500 at most)" % total)
            if dups:
                r.fail("duplicate tags: %s" % "; ".join(dups))
            if any(swears_in(t) for t in st):
                r.fail("swear word in a tag")
            lo, hi = CFG["yt_tags_count"]
            if not (lo <= len(st) <= hi):
                r.warn("%d tags (the standard is 8 to 12)" % len(st))
            if not long_ and total <= CFG["yt_tags_total_max"] and not dups:
                r.ok("%d tags, %d characters, longest %d" % (len(st), total, max(len(t) for t in st)))

    # --- TikTok caption
    if kind == "tiktok":
        cap = spec.get("tiktok_caption", "")
        fails_before = r.fails
        if not cap:
            r.fail("no tiktok_caption")
        else:
            n = u16(cap)
            if n > CFG["tt_caption_max"]:
                r.fail("caption is %d units (2,200 at most)" % n)
            if swears_in(cap):
                r.fail("swear word in the caption: %s" % ", ".join(swears_in(cap)))
            ht = hashtags(cap)
            dead = [h for h in ht if h.lower() in TT_DEAD_TAGS]
            if dead:
                r.fail("hashtags that do nothing: %s" % " ".join("#" + h for h in dead))
            if len(ht) != CFG["tt_hashtags"]:
                r.warn("caption has %d hashtags (the standard is five topic tags)" % len(ht))
            body = cap.split("#")[0].strip()
            if not body.endswith("?"):
                r.warn("caption text does not end with a question before the hashtags")
            if survival and "General info, not safety training." not in cap:
                r.fail("survival video without 'General info, not safety training.' in the caption")
            stp = spec.get("search_top")
            if stp:
                phrase = " ".join(str(row[0]) for row in stp.get("rows", []) if row).lower().strip("?")
                head = " ".join(words(cap)[:len(words(phrase)) + 3])
                shared = len(set(words(phrase)) & set(words(head)))
                if shared < max(2, len(set(words(phrase))) // 2):
                    r.warn("caption does not open with the on-screen search phrase '%s'" % phrase)
            if "@" in cap or re.search(r"https?://|www\.", cap, re.I) or BARE_DOMAIN.search(cap):
                r.fail("caption has a mention or a link (TikTok captions cannot carry links)")
            if r.fails == fails_before:
                r.ok("caption %d of 2,200 units, %d hashtags" % (n, len(ht)))

    # --- file
    if mp4:
        d = duration(mp4)
        lo, hi = CFG["short_s"]
        tlo, thi = CFG["tt_short_s"]
        if d <= 0:
            r.fail("cannot read %s" % mp4)
        elif kind == "youtube" and not (lo <= d <= hi):
            r.fail("YouTube Short is %.2f s (15 to 20)" % d)
        elif kind == "tiktok" and d < tlo:
            r.warn("TikTok cut is %.2f s, under 20 s (the search-led cuts run 20 to 26): wrong or cut-off file?" % d)
        elif kind == "tiktok" and thi < d < CFG["tt_rewards_s"]:
            r.warn("TikTok short cut is %.2f s (the search-led cuts run 20 to 26; a Rewards cut runs 61 or more)" % d)
        else:
            r.ok("length %.2f s" % d)
    print("  => %s (%d fail, %d warn)" % ("FAIL" if r.fails else "pass", r.fails, r.warns))
    return r.fails


# ---------------------------------------------------------------- selftest
def _fixtures():
    yt = {
        "series": "Things Living In Your House",
        "title": "Your Cat Likely Can't Taste Sweet or Sugar: 1 Broken Gene \U0001F431 (Things Living In Your House #64)",
        "description": ("Can cats taste sweet things or sugar? In cats, one gene of the sweet taste receptor is broken. "
                        "Hell's Canyon has nothing to do with it.\n\n#cats #catfacts #meatballmyths #shorts\n\n"
                        "Sources: Li et al. 2005, PLoS Genetics."),
        "pinned_comment": "Does your cat blink back when you slow blink at it?",
        "tags": ["can cats taste sweet", "can cats taste sugar", "why cats can't taste sweet", "cats can't taste sweet",
                 "cat facts", "cat facts you didn't know", "cat slow blink meaning", "things living in your house",
                 "Meatball Myths"],
        "beats": [{"say": "Your cat most likely can't taste sugar. Damn."},
                  {"say": "One gene for tasting sweet is broken. Hello class, assess this."},
                  {"say": "Blink slowly at it instead."}],
    }
    tt = copy.deepcopy(yt)
    tt.update({
        "beats": [{"say": "Your cat most likely can't taste fucking sugar."},
                  {"say": "That shit's wild. Holy shit."},
                  {"say": "Blink slowly at it instead. Weird as fuck."}],
        "search_top": {"rows": [["CAN CATS", "#ffffff", 86], ["TASTE SUGAR?", "#ffd34d", 86]], "y": 150},
        "tiktok_title": "Can Cats Taste Sugar? Most Likely Not",
        "tiktok_caption": ("can cats taste sugar or sweet things? Most likely not: one gene for tasting sweet is broken. "
                           "Does your cat beg for sweets? #catfacts #catsoftiktok #cat #cats #funfacts"),
        "cap_swap": {"shit": "sh*t", "fuck": "f**k", "fucking": "f**king"},
    })

    def ch(base, **kw):
        s = copy.deepcopy(base)
        for k, v in kw.items():
            if v is None:
                s.pop(k, None)
            elif callable(v):
                s[k] = v(s.get(k))
            else:
                s[k] = v
        return s

    def say(i, text):
        return lambda beats: [dict(b, say=text) if j == i else b for j, b in enumerate(beats)]

    return [
        # (name, network, spec, should pass, words the FAIL line must hold)
        ("YouTube spec that follows every rule", "yt", yt, True, None),
        ("TikTok spec, every swear softened (shit's shown as SH*T'S)", "tt", tt, True, None),
        ("TikTok spec with captions off", "tt", ch(tt, cap_swap={}, captions=0), True, None),
        ("strong word on YouTube", "yt", ch(yt, beats=say(1, "That shit's wild.")), False, 'strong words in a YouTube script'),
        ("strong word on YouTube, curly apostrophe fuckin\u2019", "yt", ch(yt, beats=say(1, "It's fuckin\u2019 wild.")), False, 'strong words in a YouTube script'),
        ("compound swear on YouTube (shitballs)", "yt", ch(yt, beats=say(1, "Holy shitballs.")), False, 'strong words in a YouTube script'),
        ("TikTok shit's with no 'shit' cap_swap entry", "tt",
         ch(tt, cap_swap={"fuck": "f**k", "fucking": "f**king"}), False, "SHIT'S"),
        ("TikTok fuckin' with only a 'fucking' entry", "tt", ch(tt, beats=say(0, "Fuckin' wild, right?")), False, "captions would show: FUCKIN'"),
        ("TikTok fuckin\u2019 (curly) with only a 'fucking' entry", "tt", ch(tt, beats=say(0, "Fuckin\u2019 wild.")), False, 'captions would show: FUCKIN’'),
        ("banned title word", "yt", ch(yt, title="The Cat Sugar Myth: 1 Broken Gene \U0001F431 (Things Living In Your House #64)"), False, "banned title word 'myth'"),
        ("banned title word, plural", "yt", ch(yt, title="Cat Sugar Myths: 1 Broken Gene \U0001F431 (Things Living In Your House #64)"), False, "banned title word 'myth'"),
        ("banned title word, past tense", "yt", ch(yt, title="Believed for Years: 1 Broken Gene \U0001F431 (Things Living In Your House #64)"), False, "banned title word 'believe'"),
        ("banned title phrase with a non-breaking space", "yt",
         ch(yt, title="Did\u00a0you know Cats Can't Taste Sugar \U0001F431 (Things Living In Your House #64)"), False, "banned title word 'did you know'"),
        ("tag over 30 characters", "yt", ch(yt, tags=lambda t: t + ["why do cats knead with their paws"]), False, 'tags over 30 characters'),
        ("duplicate tag with a trailing space", "yt", ch(yt, tags=lambda t: t + ["cat facts "]), False, 'duplicate tags'),
        ("tags given as one string", "yt", ch(yt, tags="cat facts, can cats taste sugar"), False, 'tags must be a list'),
        ("empty tag", "yt", ch(yt, tags=lambda t: t + [""]), False, 'tags must be a list'),
        ("missing Sources line", "yt", ch(yt, description=yt["description"].split("\n\nSources")[0]), False, 'no Sources line'),
        ("placeholder text in the description", "yt",
         ch(yt, description=yt["description"].replace("Sources: Li", "Sources: UNCHECKED, Li")), False, "placeholder text 'UNCHECKED' in description"),
        ("placeholder text in a TikTok caption", "tt",
         ch(tt, tiktok_caption=tt["tiktok_caption"].replace("Most likely", "TODO most likely")), False, "placeholder text 'TODO' in tiktok_caption"),
        ("bare domain in a TikTok caption", "tt",
         ch(tt, tiktok_caption=tt["tiktok_caption"].replace("Does your", "See example.com. Does your")), False, 'a mention or a link'),
        ("strong word in a TikTok caption", "tt",
         ch(tt, tiktok_caption=tt["tiktok_caption"].replace("Most likely", "Shit, most likely")), False, 'swear word in the caption'),
    ]


def selftest():
    bad = 0
    fx = _fixtures()
    with tempfile.TemporaryDirectory(prefix="postkit-selftest-") as d:
        for i, (name, net, spec, want_pass, why) in enumerate(fx, 1):
            fn = ("tts-selftest-%02d.json" if net == "tt" else "selftest-%02d-v6-yt.json") % i
            path = os.path.join(d, fn)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(spec, f, ensure_ascii=False)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                fails = lint(path)
            got_pass = fails == 0
            fail_lines = [ln for ln in buf.getvalue().splitlines() if ln.strip().startswith("FAIL")]
            right_reason = want_pass or any(why in ln for ln in fail_lines)
            if got_pass == want_pass and right_reason:
                print("ok   %-60s %s as it should" % (name, "pass" if got_pass else "FAIL"))
            else:
                bad += 1
                print("FAIL %-60s gave %s, should %s%s" % (name, "pass" if got_pass else "FAIL", "pass" if want_pass else "FAIL",
                                                           "" if want_pass else " with '%s'" % why))
                for line in buf.getvalue().splitlines():
                    print("     " + line)
    print("selftest: %d of %d fixtures gave the right verdict" % (len(fx) - bad, len(fx)))
    return 1 if bad else 0


# ---------------------------------------------------------------- payload
def ny_offset_date(when, tz=TZ):
    from zoneinfo import ZoneInfo
    dt = datetime.datetime.strptime(when, WHEN_FMT).replace(tzinfo=ZoneInfo(tz))
    return dt.isoformat()


def payload(spec_path, net, when, media, cover_ms=None, first_comment=None, kind="short", thumb=None,
            category="EDUCATION", tz=TZ, update=None, no_lint=False, call=False):
    """Prints nothing on stdout unless every check passes; every refusal is a FAIL line on stderr and exit 1."""
    def stop(msg):
        print("FAIL " + msg, file=sys.stderr)
        sys.exit(1)

    if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d", when or ""):
        stop("--when must look like 2026-11-13T16:00:00 (got %r)" % when)
    try:
        date = ny_offset_date(when, tz)
    except ValueError as e:
        stop("--when is not a real date and time: %s" % e)
    if not (media or "").startswith("https://"):
        stop("--media must be an https:// link (got %r)" % media)
    if net == "tiktok" and cover_ms is not None:
        stop("--cover-ms is for YouTube only here (a TikTok cover is not set through this post)")
    if call and update:
        stop("give --call or --update, not both")
    try:
        spec = load(spec_path)
    except (OSError, ValueError) as e:
        stop("cannot read the spec %s (%s)" % (spec_path, e))
    k = spec_kind(spec_path, spec)
    if k != net and not (net == "youtube" and kind == "video"):
        stop("this is a %s spec; --net %s would skip its %s checks (use the %s spec)" % (k, net, net, net))
    if not no_lint:                                  # a post body is only printed for a spec that passes the gate
        real, sys.stdout = sys.stdout, sys.stderr
        try:
            fails = lint(spec_path)
        finally:
            sys.stdout = real
        if fails:
            stop("lint (see above); no payload printed")
    base = {"autoPublish": True, "descendants": [], "draft": False, "hasNotReadNotes": False, "media": [media],
            "mediaAltText": [], "publicationDate": {"dateTime": when, "timezone": tz}, "shortener": False,
            "smartLinkData": {"ids": []}}
    if net == "youtube":
        tags = spec.get("tags")
        if not tags or not isinstance(tags, list):
            stop("the spec has no 'tags' list")
        if not spec.get("title") or not spec.get("description"):
            stop("the spec has no title or no description")
        fc = first_comment
        if fc is None:
            fc = spec.get("pinned_comment", "")
            if fc and not fc.rstrip().endswith("\U0001F447"):
                fc = fc.rstrip() + " \U0001F447"
        base.update({"firstCommentText": fc, "providers": [{"network": "youtube"}], "text": spec["description"],
                     "youtubeData": {"title": spec["title"], "type": kind, "privacy": "public",
                                     "tags": [t.strip() for t in tags],
                                     "category": category, "madeForKids": False, "isAiGeneratedContent": True}})
        if thumb:
            base["videoThumbnailUrl"] = thumb
        if cover_ms is not None:
            base["videoCoverMilliseconds"] = int(cover_ms)
    else:
        if not spec.get("tiktok_caption"):
            stop("the spec has no tiktok_caption")
        base.update({"firstCommentText": "", "providers": [{"network": "tiktok"}], "text": spec["tiktok_caption"],
                     "tiktokData": {"privacyOption": "PUBLIC_TO_EVERYONE", "title": spec.get("tiktok_title", ""),
                                    "photoCoverIndex": 0, "isAigc": True}})
    info = json.dumps(base, ensure_ascii=False)
    if update:
        print(json.dumps({"blogId": BRAND, "id": str(update[0]), "uuid": str(update[1]), "info": info}, ensure_ascii=False))
    elif call:
        print(json.dumps({"blogId": BRAND, "date": date, "info": info}, ensure_ascii=False))
    else:
        print(info)
    return 0


# ---------------------------------------------------------------- post log
def log_post(net, when, file, title, episode=None, uuid=None, post_id=None, media=None):
    """Update or add the row for (network, file name[, episode]) in data/posted.csv; keep the scheduler's ids in
    data/post-ids.csv."""
    path = os.path.join(ROOT, "data", "posted.csv")
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    base = os.path.basename(file)
    hit = [r for r in rows[1:] if len(r) >= 5 and r[1] == net and r[3] == base and (episode is None or r[2] == episode)]
    if len(hit) > 1:
        print("FAIL %d rows in posted.csv for %s %s (episodes: %s); give --episode" % (
            len(hit), net, base, ", ".join(r[2] for r in hit)))
        return 1
    if hit:
        old = list(hit[0])
        hit[0][0], hit[0][4] = when, title
        if episode:
            hit[0][2] = episode
        print("posted.csv updated: %s %s %s -> %s" % (old[0], old[2], base, when))
    else:
        rows.append([when, net, episode or "drawn-house", base, title])
        print("posted.csv added: %s %s %s %s" % (when, net, episode or "drawn-house", base))
    with open(path, "w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)
    if uuid:
        ids = os.path.join(ROOT, "data", "post-ids.csv")
        have = []
        if os.path.exists(ids):
            with open(ids, encoding="utf-8", newline="") as f:
                have = list(csv.reader(f))
        if not have:
            have = [["network", "file", "when_et", "uuid", "id", "media"]]
        have = [r for r in have if not (len(r) >= 4 and r[3] == str(uuid))]
        have.append([net, base, when, str(uuid), str(post_id or ""), media or ""])
        with open(ids, "w", encoding="utf-8", newline="") as f:
            csv.writer(f, lineterminator="\n").writerows(have)
        print("post-ids.csv: uuid %s (the id changes on every update; the uuid does not)" % uuid)
    return 0


# ---------------------------------------------------------------- raw url and re-host check
def _git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, text=True)


def rawurl(path, sha=None):
    if not os.path.isfile(path):
        print("FAIL no such file: %s" % path)
        return 1
    rel = os.path.relpath(os.path.realpath(path), os.path.realpath(REPO))
    if rel.startswith(".."):
        print("FAIL %s is not inside the repository" % path)
        return 1
    res = _git("rev-parse", "--verify", "--quiet", "%s^{commit}" % (sha or "HEAD"))
    if res.returncode != 0 or not res.stdout.strip():
        print("FAIL %s is not a commit here" % (sha or "HEAD"))
        return 1
    full = res.stdout.strip()
    blob = _git("rev-parse", "--verify", "--quiet", "%s:%s" % (full, rel))
    if blob.returncode != 0:
        print("FAIL %s is not in commit %s (commit and push first)" % (rel, full[:9]))
        return 1
    disk = _git("hash-object", os.path.realpath(path))
    if disk.returncode != 0 or disk.stdout.strip() != blob.stdout.strip():
        print("FAIL the file on disk differs from the one in commit %s (commit and push it first)" % full[:9])
        return 1
    pushed = _git("branch", "-r", "--contains", full).stdout.strip()
    if not pushed:
        print("FAIL commit %s is not on the remote yet (push first)" % full[:9])
        return 1
    url = "https://raw.githubusercontent.com/%s/%s/%s" % (GITHUB, full, urllib.parse.quote(rel))
    code = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-m", "30", "-L", url],
                          capture_output=True, text=True).stdout.strip()
    if code != "200":
        print("FAIL the raw link answers HTTP %s, not 200: %s" % (code or "nothing", url))
        return 1
    print(url)
    return 0


def rehost(url, path):
    if not os.path.isfile(path):
        print("FAIL no such file: %s" % path)
        return 1
    head = subprocess.run(["curl", "-sSI", "-m", "30", url], capture_output=True, text=True).stdout
    m = re.search(r"(?im)^content-length:\s*(\d+)", head)
    want = os.path.getsize(path)
    if not m:
        print("FAIL no content-length from %s" % url)
        return 1
    if int(m.group(1)) != want:
        print("FAIL the copy is %s bytes, the local file is %d" % (m.group(1), want))
        return 1
    print("ok   same size (%d bytes)" % want)
    return 0


# ---------------------------------------------------------------- keywords
def suggest(q, yt=True):
    """The suggestion list, or None after printing a FAIL line on stderr."""
    u = ("https://suggestqueries.google.com/complete/search?client=firefox&hl=en&gl=US" +
         ("&ds=yt" if yt else "") + "&q=" + urllib.parse.quote(q))
    try:
        p = subprocess.run(["curl", "-sS", "-m", "15", u], capture_output=True, timeout=25)
        if p.returncode != 0:
            raise RuntimeError("curl exit %d: %s" % (p.returncode, p.stderr.decode("utf-8", "replace").strip()[:120]))
        out = json.loads(p.stdout.decode("utf-8", "replace"))[1]
        if not isinstance(out, list):
            raise RuntimeError("unexpected answer format")
        return out
    except Exception as e:
        print("FAIL suggest %s '%s': %s" % ("yt" if yt else "web", q, str(e)[:160]), file=sys.stderr)
        return None


def kw(seeds, searches, out=None, n=25):
    rows, rc = [], 0
    for s in seeds:
        for src, yt in (("yt", True), ("web", False)):
            got = suggest(s, yt)
            if got is None:
                rc = 1
                continue
            for rank, x in enumerate(got, 1):
                rows.append(["suggest", src, s, rank, x, "", "", ""])
        time.sleep(0.2)
    for q in searches:
        try:
            p = subprocess.run(["yt-dlp", "--flat-playlist", "-J", "ytsearch%d:%s" % (n, q)], capture_output=True, timeout=180)
            if p.returncode != 0:
                raise RuntimeError("yt-dlp exit %d: %s" % (p.returncode, p.stderr.decode("utf-8", "replace").strip()[-160:]))
            entries = [e for e in (json.loads(p.stdout).get("entries") or []) if e]
            if not entries:
                raise RuntimeError("no results came back")
        except Exception as e:
            print("FAIL search '%s': %s" % (q, str(e)[:200]), file=sys.stderr)
            rc = 1
            continue
        for rank, e in enumerate(entries, 1):
            rows.append(["search", "yt", q, rank, (e.get("title") or "").replace("\n", " "), e.get("view_count"),
                         e.get("duration"), e.get("channel")])
    head = ["kind", "source", "query", "rank", "text", "views", "duration_s", "channel"]
    if out:
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(head)
            w.writerows(rows)
        print("wrote %d rows to %s" % (len(rows), out))
    for s in seeds:
        got = [r[4] for r in rows if r[0] == "suggest" and r[1] == "yt" and r[2] == s]
        print("yt  %-34s -> %s" % (s, " ; ".join(got[:8])))
    for q in searches:
        top = sorted([r for r in rows if r[0] == "search" and r[2] == q], key=lambda r: -(r[5] or 0))[:6]
        print("top results for '%s':" % q)
        for r in top:
            print("   %10s  %4ss  %s  [%s]" % (r[5], int(r[6] or 0), r[4][:80], r[7]))
    return rc


# ---------------------------------------------------------------- TikTok public page
NO_PAGE_DATA = "no page data"


def _int(x):
    try:
        return int(x) if x is not None else None
    except (TypeError, ValueError):
        return None


def ttpage_one(url):
    p = subprocess.run(["curl", "-sS", "-m", "30", "-A", UA, "-w", "\n%{http_code}", url], capture_output=True)
    text = p.stdout.decode("utf-8", "replace")
    html, _, code = text.rpartition("\n")
    if p.returncode != 0:
        return {"url": url, "error": "%s: curl exit %d (%s)" % (
            NO_PAGE_DATA, p.returncode, p.stderr.decode("utf-8", "replace").strip()[:120])}
    m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return {"url": url, "error": "%s (HTTP %s; blocked or the page changed); do not retry in a loop" % (NO_PAGE_DATA, code)}
    try:
        scope = json.loads(m.group(1)).get("__DEFAULT_SCOPE__", {})
    except ValueError:
        return {"url": url, "error": "%s (HTTP %s; the page JSON did not parse)" % (NO_PAGE_DATA, code)}
    detail = scope.get("webapp.video-detail") or {}
    it = (detail.get("itemInfo") or {}).get("itemStruct") or {}
    if not it:
        return {"url": url, "error": "no video in the page data (HTTP %s, TikTok statusCode %s: removed, private or "
                                     "region-locked)" % (code, detail.get("statusCode"))}
    st = it.get("stats") or {}
    return {"url": url, "id": it.get("id"), "author": (it.get("author") or {}).get("uniqueId"),
            "followers": _int((it.get("authorStats") or {}).get("followerCount")),
            "created": _int(it.get("createTime")), "seconds": (it.get("video") or {}).get("duration"),
            "plays": _int(st.get("playCount")), "likes": _int(st.get("diggCount")), "comments": _int(st.get("commentCount")),
            "shares": _int(st.get("shareCount")), "saves": _int(st.get("collectCount")),
            "caption": it.get("desc"), "hashtags": [t.get("hashtagName") for t in it.get("textExtra") or [] if t.get("hashtagName")],
            "labels": it.get("diversificationLabels"), "category_type": it.get("CategoryType"),
            "is_aigc": it.get("IsAigc"), "aigc_label_type": it.get("aigcLabelType"), "suggested_words": it.get("suggestedWords"),
            "search_bar_words": [w.get("word") for s in (it.get("videoSuggestWordsList") or {}).get("video_suggest_words_struct") or []
                                 for w in s.get("words") or []] if isinstance(it.get("videoSuggestWordsList"), dict) else None,
            "is_reviewing": it.get("isReviewing"), "penalty": it.get("penaltyContext")}


TT_CSV_HEAD = ["date_utc", "video_id", "url", "plays", "likes", "comments", "shares", "saves", "label", "ai_label",
               "flag", "suggested_words"]


def tt_flag(row):
    if row.get("is_reviewing"):
        return "reviewing"
    pen = row.get("penalty")
    if isinstance(pen, dict):
        v = pen.get("display_penalty_type")
        if v not in (None, "", "0", 0):
            return "penalty %s" % v
    return ""


def ttpage(urls, out=None, csv_out=None):
    bad = [u for u in urls if not TT_URL.fullmatch(u.split("?")[0])]
    if bad:
        for u in bad:
            print("FAIL not a TikTok video link (https://www.tiktok.com/@name/video/NUMBER): %s" % u)
        return 1
    rows = []
    for i, u in enumerate(urls):
        if i:
            time.sleep(1.0)
        row = ttpage_one(u)
        rows.append(row)
        if "error" in row:
            print("FAIL %s: %s" % (u, row["error"]))
            if row["error"].startswith(NO_PAGE_DATA):
                left = len(urls) - i - 1
                if left:
                    print("stopped: %d link(s) not fetched (TikTok gave no page data; do not retry in a loop)" % left)
                break
            continue
        like = (100.0 * (row["likes"] or 0) / row["plays"]) if row.get("plays") else 0
        age = ("  age %.1f h" % ((time.time() - row["created"]) / 3600.0)) if row.get("created") else ""
        print("%s  plays %s  likes %s (%.2f%%)  comments %s  shares %s  saves %s  %ss%s  label %s" % (
            row["id"], row["plays"], row["likes"], like, row["comments"], row["shares"], row["saves"], row["seconds"],
            age, (row["labels"] or ["?"])[0]))
        print("   caption: %s" % (row["caption"] or "")[:160])
        if row["suggested_words"]:
            print("   TikTok suggests: %s" % "; ".join(row["suggested_words"]))
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=1)
        print("wrote %s" % out)
    if csv_out:
        good = [r for r in rows if "error" not in r]
        new = not os.path.exists(csv_out) or os.path.getsize(csv_out) == 0
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with open(csv_out, "a", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            if new:
                w.writerow(TT_CSV_HEAD)
            for r in good:
                w.writerow([now, r["id"], r["url"], r["plays"], r["likes"], r["comments"], r["shares"], r["saves"],
                            (r["labels"] or [""])[0], r.get("aigc_label_type") if r.get("aigc_label_type") is not None else "",
                            tt_flag(r), "|".join(r["suggested_words"] or [])])
        print("appended %d row(s) to %s" % (len(good), csv_out))
    return 1 if any("error" in r for r in rows) or len(rows) < len(urls) else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("render"); p.add_argument("spec"); p.add_argument("out"); p.add_argument("--work", required=True)
    p = sub.add_parser("voicecheck"); p.add_argument("spec"); p.add_argument("mp4"); p.add_argument("--model", default="small.en")
    p = sub.add_parser("sheet"); p.add_argument("mp4"); p.add_argument("out"); p.add_argument("--step", type=float, default=1.5); p.add_argument("--cols", type=int, default=9)
    p = sub.add_parser("lint"); p.add_argument("specs", nargs="+"); p.add_argument("--mp4")
    sub.add_parser("selftest")
    p = sub.add_parser("payload"); p.add_argument("spec"); p.add_argument("--net", required=True, choices=["youtube", "tiktok"])
    p.add_argument("--when", required=True, help="YYYY-MM-DDTHH:MM:SS, New York time"); p.add_argument("--media", required=True, help="https:// link")
    p.add_argument("--cover-ms", type=int, help="YouTube only")
    p.add_argument("--first-comment"); p.add_argument("--kind", default="short", choices=["short", "video"]); p.add_argument("--thumb")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--update", nargs=2, metavar=("ID", "UUID"), help="print the updateScheduledPost arguments")
    g.add_argument("--call", action="store_true", help="print the createScheduledPost arguments")
    p.add_argument("--no-lint", action="store_true")
    p = sub.add_parser("log"); p.add_argument("--net", required=True, choices=["youtube", "tiktok"]); p.add_argument("--when", required=True)
    p.add_argument("--file", required=True); p.add_argument("--title"); p.add_argument("--spec")
    p.add_argument("--episode", help="no default: needed when the file name is used by more than one episode")
    p.add_argument("--uuid"); p.add_argument("--id"); p.add_argument("--media")
    p = sub.add_parser("rawurl"); p.add_argument("file"); p.add_argument("--sha")
    p = sub.add_parser("rehost"); p.add_argument("url"); p.add_argument("file")
    p = sub.add_parser("kw"); p.add_argument("seeds", nargs="*"); p.add_argument("--search", action="append", default=[])
    p.add_argument("--out", metavar="FILE", help="CSV file to write"); p.add_argument("--n", type=int, default=25)
    p = sub.add_parser("ttpage"); p.add_argument("urls", nargs="+"); p.add_argument("--json"); p.add_argument("--csv", metavar="FILE")
    a = ap.parse_args()
    if a.cmd == "render":
        rc = render(a.spec, a.out, a.work)
    elif a.cmd == "voicecheck":
        rc = voicecheck(a.spec, a.mp4, a.model)
    elif a.cmd == "sheet":
        rc = sheet(a.mp4, a.out, a.step, a.cols)
    elif a.cmd == "lint":
        if a.mp4 and len(a.specs) > 1:
            sys.exit("--mp4 goes with one spec")
        rc = sum(lint(s, a.mp4) for s in a.specs)
    elif a.cmd == "selftest":
        rc = selftest()
    elif a.cmd == "payload":
        rc = payload(a.spec, a.net, a.when, a.media, a.cover_ms, a.first_comment, a.kind, a.thumb,
                     update=a.update, no_lint=a.no_lint, call=a.call)
    elif a.cmd == "log":
        title = a.title
        if not title and a.spec:
            sp = load(a.spec)
            title = sp.get("title") if a.net == "youtube" else sp.get("tiktok_title")
        if not title:
            sys.exit("give --title or --spec")
        rc = log_post(a.net, a.when.replace("T", " ")[:16], a.file, title, a.episode, a.uuid, a.id, a.media)
    elif a.cmd == "rawurl":
        rc = rawurl(a.file, a.sha)
    elif a.cmd == "rehost":
        rc = rehost(a.url, a.file)
    elif a.cmd == "kw":
        rc = kw(a.seeds, a.search, a.out, a.n)
    else:
        rc = ttpage(a.urls, a.json, a.csv)
    sys.exit(1 if rc else 0)


if __name__ == "__main__":
    main()
