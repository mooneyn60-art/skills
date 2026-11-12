#!/usr/bin/env python3
"""Post kit: the checks and chores between a finished spec and a scheduled post, as commands instead of hand work.

  postkit.py render SPEC OUT.mp4 --work DIR       render with drawn.py, refuse a stale file, then voicecheck
  postkit.py voicecheck SPEC MP4 [--model small.en]
  postkit.py sheet MP4 OUT.jpg [--step 1.5] [--cols 9]
  postkit.py lint SPEC [SPEC ...] [--mp4 FILE]    titles, descriptions, tags, hashtags, captions, swear words, lengths
  postkit.py payload SPEC --net youtube|tiktok --when 2026-11-13T16:00:00 --media URL [--cover-ms 1900] [--update ID UUID]
  postkit.py log --net youtube|tiktok --when "2026-11-13 16:00" --file OUT.mp4 --spec SPEC [--uuid U --id I --media URL]
  postkit.py rawurl FILE [--sha SHA]              raw.githubusercontent.com URL of a pushed file (checks it is in that commit)
  postkit.py rehost URL FILE                      the scheduler's copy has the same size as the local file
  postkit.py kw "seed" ["seed" ...] [--search "query" ...] [--out PREFIX]
  postkit.py ttpage URL [URL ...] [--json OUT]

Why each exists (all from 2026-11-12, research 92 and 93):
  render      drawn.py exits non-zero and leaves the OLD mp4 in place when the voice service returns no audio.
              One of 14 cuts kept its old file that way and only a transcript showed it. This renders to
              OUT.new.mp4 and moves it over OUT only after the voice check passes.
  voicecheck  the voice service can drop a word or stop a line early with no error.
  lint        the metadata standard in MASTER_ORDERS ("Tags and everything, from every angle") as a gate.
  payload     Metricool's update call needs the whole post again; hand-typed payloads lose a word or an emoji.
              It runs lint first and prints nothing for a spec that fails.
  log         data/posted.csv must follow every scheduling change; data/post-ids.csv keeps each post's uuid.
  kw, ttpage  what people type (YouTube and Google suggestions, top results) and what TikTok shows for a video
              (plays, category label, its own suggested searches), from public pages only.
Nothing here schedules, posts or spends credits. Exit code 1 means a FAIL line was printed.
"""
import argparse
import csv
import difflib
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # skills/oh-meatball
REPO = os.path.dirname(os.path.dirname(ROOT))      # repository root
GITHUB = "mooneyn60-art/skills"
BRAND = "7521392"                                  # Metricool brand (blogId)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

MILD = {"damn", "hell", "ass", "dumbass", "badass", "bastard", "bastards"}          # allowed in YouTube speech
STRONG = {"fuck", "fucks", "fucking", "fucked", "fucker", "fuckers", "motherfucker", "shit", "shits", "shitty",
          "bullshit", "bitch", "bitches", "asshole", "assholes", "crap", "piss", "pissed", "dick", "cock", "pussy"}
BANNED_TITLE = ["true or false", "myth", "believe", "cartoons", "lied", "did you know"]
TT_DEAD_TAGS = {"fyp", "foryou", "foryoupage", "viral", "fypシ", "xyzbca"}
EMOJI = re.compile("[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]")


def u16(s):
    """Length the way YouTube and TikTok count it: UTF-16 units (an emoji is 2)."""
    return len(s.encode("utf-16-le")) // 2


def words(s):
    return re.sub(r"[^a-z0-9' ]", " ", s.lower().replace("’", "'")).split()


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def duration(mp4):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4],
                         capture_output=True, text=True).stdout.strip()
    return float(out) if out else 0.0


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
def transcribe(mp4, model="small.en"):
    import soundfile as sf
    from faster_whisper import WhisperModel
    wav = "/tmp/postkit-%d.wav" % os.getpid()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-ac", "1", "-ar", "16000", wav], check=True)
    audio, _ = sf.read(wav, dtype="float32")
    os.remove(wav)
    m = WhisperModel(model, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(audio, language="en", beam_size=5, condition_on_previous_text=False)
    return " ".join(s.text for s in segs)


def voicecheck(spec_path, mp4, model="small.en", quiet=False):
    """Every line of the spec is heard, in order, to its last words. Returns the number of FAILs."""
    spec = load(spec_path)
    lines = [b["say"] for b in spec["beats"] if b.get("say")]
    want, owner = [], []
    for i, line in enumerate(lines):
        w = words(line)
        want += w
        owner += [i] * len(w)
    heard_text = transcribe(mp4, model)
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
    print("voicecheck %s  (%.1f s, %d words wanted, %d heard, match %.3f)" % (
        os.path.basename(mp4), duration(mp4), len(want), len(heard), sm.ratio()))
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
    os.makedirs(work, exist_ok=True)
    new = (out[:-4] if out.endswith(".mp4") else out) + ".new.mp4"
    if os.path.exists(new):
        os.remove(new)
    log = os.path.join(work, "render.log")
    sheet_path = os.path.join(work, "sheet.jpg")
    t0 = time.time()
    with open(log, "w") as f:
        rc = subprocess.run([sys.executable, os.path.join(HERE, "drawn.py"), spec_path, new, "--work", work],
                            stdout=f, stderr=subprocess.STDOUT, cwd=ROOT,
                            env=dict(os.environ, DRAWN_CONTACT=sheet_path)).returncode
    tail = open(log, errors="replace").read().strip().splitlines()[-3:]
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
        return 1
    os.replace(new, out)
    print("rendered %s  %.2f s  %d bytes  in %.0f s%s" % (out, duration(out), os.path.getsize(out), time.time() - t0,
          ("  sheet " + sheet_path) if os.path.exists(sheet_path) else ""))
    return 0


# ---------------------------------------------------------------- contact sheet
def sheet(mp4, out, step=1.5, cols=9, w=216):
    from PIL import Image
    dur = duration(mp4)
    ts = [round(0.4 + i * step, 2) for i in range(int(max(dur - 0.5, 0) / step) + 1)]
    h = int(w * 16 / 9)
    rows = (len(ts) + cols - 1) // cols
    img = Image.new("RGB", (w * cols, h * rows), "black")
    for i, t in enumerate(ts):
        tmp = "/tmp/postkit-sheet-%d-%d.png" % (os.getpid(), i)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", mp4, "-frames:v", "1",
                        "-vf", "scale=%d:%d" % (w, h), tmp])
        if os.path.exists(tmp):
            img.paste(Image.open(tmp), ((i % cols) * w, (i // cols) * h))
            os.remove(tmp)
    img.save(out, quality=85)
    print("sheet %s  %d frames every %.1f s" % (out, len(ts), step))
    return 0


# ---------------------------------------------------------------- lint
def spec_kind(path, spec):
    base = os.path.basename(path)
    if base.startswith("tts-") or base.startswith("tt-") or "search_top" in spec:
        return "tiktok"
    return "youtube"


def swears_in(text):
    return [w for w in words(text) if w in STRONG or w in MILD]


def hashtags(text):
    return re.findall(r"#([^\s#]+)", text)


def lint(path, mp4=None):
    spec = load(path)
    kind = spec_kind(path, spec)
    r = Report(path)
    print("lint %s  (%s)" % (path, kind))
    title = spec.get("title", "")
    desc = spec.get("description", "")
    tags = spec.get("tags")
    says = [b.get("say", "") for b in spec.get("beats", [])]
    survival = "would meatball survive" in (spec.get("series", "") + " " + title).lower()

    # --- spoken words
    spoken = words(" ".join(says))
    strong = [w for w in spoken if w in STRONG]
    mild = [w for w in spoken if w in MILD]
    if kind == "youtube":
        if strong:
            r.fail("strong words in a YouTube script: %s" % ", ".join(sorted(set(strong))))
        if len(mild) > 2:
            r.fail("%d mild words in a Short (two at most): %s" % (len(mild), ", ".join(mild)))
        else:
            r.ok("spoken: %d mild word(s), no strong ones" % len(mild))
    else:
        swap = {k.lower() for k in (spec.get("cap_swap") or {})}
        missing = sorted({w for w in strong if w not in swap})
        if missing:
            r.fail("cap_swap has no entry for: %s (the caption would spell them out)" % ", ".join(missing))
        else:
            r.ok("spoken: %d strong word(s), all softened in captions by cap_swap" % len(strong))

    # --- text a viewer reads besides the main fields
    cards = [row[0] for b in spec.get("beats", []) for row in (b.get("card") or {}).get("rows", [])]
    cards += [row[0] for row in (spec.get("search_top") or {}).get("rows", [])]
    for label, text in (("pinned_comment", spec.get("pinned_comment", "")), ("tiktok_title", spec.get("tiktok_title", "")),
                        ("a card", " | ".join(cards))):
        bad = [w for w in swears_in(text) if w in STRONG or kind == "youtube"]
        if bad:
            r.fail("swear word in %s: %s" % (label, ", ".join(sorted(set(bad)))))

    # --- script traps found on 2026-11-12
    joined = " ".join(says)
    if re.search(r"\bhis (a|an|for|to|some)\b", joined, re.I):
        r.warn("a bare 'his' (write 'his cat' or 'his dog': the voice swallows it)")
    if re.search(r"\bmeowed\b", joined, re.I):
        r.warn("'meowed' is heard as 'me out' in this voice (write 'let out a meow')")
    beats = spec.get("beats", [])
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
        elif n > 100:
            r.fail("title is %d units (100 at most): %s" % (n, title))
        else:
            r.ok("title %d of 100 units" % n)
        low = title.lower()
        for b in BANNED_TITLE:
            if re.search(r"\b%s\b" % re.escape(b), low):
                r.fail("banned title word '%s'" % b)
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
            if len(ht) != 4:
                r.warn("description has %d hashtags (the standard is four: two topic, #meatballmyths, #shorts)" % len(ht))
            elif ht[-1].lower() != "shorts" or "meatballmyths" not in [h.lower() for h in ht]:
                r.warn("hashtags should end '#meatballmyths #shorts': %s" % " ".join("#" + h for h in ht))
            if u16(desc) > 5000:
                r.fail("description is %d units (5,000 at most)" % u16(desc))
        if not tags:
            r.warn("no 'tags' list in the spec (payload needs one; 8 to 12 search phrases)")
        else:
            long_ = [t for t in tags if len(t) > 30]
            total = sum(len(t) for t in tags) + len(tags) - 1
            dups = sorted({t for t in tags if [x.lower() for x in tags].count(t.lower()) > 1})
            if long_:
                r.fail("tags over 30 characters: %s" % "; ".join(long_))
            if total > 500:
                r.fail("tags total %d characters (500 at most)" % total)
            if dups:
                r.fail("duplicate tags: %s" % "; ".join(dups))
            if any(swears_in(t) for t in tags):
                r.fail("swear word in a tag")
            if not (8 <= len(tags) <= 12):
                r.warn("%d tags (the standard is 8 to 12)" % len(tags))
            if not long_ and total <= 500 and not dups:
                r.ok("%d tags, %d characters, longest %d" % (len(tags), total, max(len(t) for t in tags)))

    # --- TikTok caption
    if kind == "tiktok":
        cap = spec.get("tiktok_caption", "")
        if not cap:
            r.fail("no tiktok_caption")
        else:
            n = u16(cap)
            if n > 2200:
                r.fail("caption is %d units (2,200 at most)" % n)
            if swears_in(cap):
                r.fail("swear word in the caption: %s" % ", ".join(swears_in(cap)))
            ht = hashtags(cap)
            dead = [h for h in ht if h.lower() in TT_DEAD_TAGS]
            if dead:
                r.fail("hashtags that do nothing: %s" % " ".join("#" + h for h in dead))
            if len(ht) != 5:
                r.warn("caption has %d hashtags (the standard is five topic tags)" % len(ht))
            body = cap.split("#")[0].strip()
            if not body.endswith("?"):
                r.warn("caption text does not end with a question before the hashtags")
            if survival and "General info, not safety training." not in cap:
                r.fail("survival video without 'General info, not safety training.' in the caption")
            st = spec.get("search_top")
            if st:
                phrase = " ".join(row[0] for row in st.get("rows", [])).lower().strip("?")
                head = " ".join(words(cap)[:len(words(phrase)) + 3])
                shared = len(set(words(phrase)) & set(words(head)))
                if shared < max(2, len(set(words(phrase))) // 2):
                    r.warn("caption does not open with the on-screen search phrase '%s'" % phrase)
            if "@" in cap or "http" in cap:
                r.fail("caption has a mention or a link")
            if not r.fails:
                r.ok("caption %d of 2,200 units, %d hashtags" % (n, len(ht)))

    # --- file
    if mp4:
        d = duration(mp4)
        if d <= 0:
            r.fail("cannot read %s" % mp4)
        elif kind == "youtube" and not (15.0 <= d <= 20.05):
            r.fail("YouTube Short is %.2f s (15 to 20)" % d)
        elif kind == "tiktok" and d < 61 and d > 26.5:
            r.warn("TikTok short cut is %.2f s (the search-led cuts run 20 to 26; a Rewards cut runs 61 or more)" % d)
        else:
            r.ok("length %.2f s" % d)
    print("  => %s (%d fail, %d warn)" % ("FAIL" if r.fails else "pass", r.fails, r.warns))
    return r.fails


# ---------------------------------------------------------------- payload
def payload(spec_path, net, when, media, cover_ms=None, first_comment=None, kind="short", thumb=None,
            category="EDUCATION", tz="America/New_York", update=None, no_lint=False):
    spec = load(spec_path)
    if not no_lint:                                  # a post body is only printed for a spec that passes the gate
        real, sys.stdout = sys.stdout, sys.stderr
        try:
            fails = lint(spec_path)
        finally:
            sys.stdout = real
        if fails:
            sys.exit("FAIL lint (see above); no payload printed")
    if spec_kind(spec_path, spec) != net and not (net == "youtube" and kind == "video"):
        print("WARN this spec looks like a %s spec but --net is %s" % (spec_kind(spec_path, spec), net), file=sys.stderr)
    base = {"autoPublish": True, "descendants": [], "draft": False, "hasNotReadNotes": False, "media": [media],
            "mediaAltText": [], "publicationDate": {"dateTime": when, "timezone": tz}, "shortener": False,
            "smartLinkData": {"ids": []}}
    if net == "youtube":
        if not spec.get("tags"):
            sys.exit("FAIL the spec has no 'tags' list")
        fc = first_comment
        if fc is None:
            fc = spec.get("pinned_comment", "")
            if fc and not fc.rstrip().endswith("\U0001F447"):
                fc = fc.rstrip() + " \U0001F447"
        base.update({"firstCommentText": fc, "providers": [{"network": "youtube"}], "text": spec["description"],
                     "youtubeData": {"title": spec["title"], "type": kind, "privacy": "public", "tags": spec["tags"],
                                     "category": category, "madeForKids": False, "isAiGeneratedContent": True}})
        if thumb:
            base["videoThumbnailUrl"] = thumb
        if cover_ms is not None:
            base["videoCoverMilliseconds"] = int(cover_ms)
    else:
        base.update({"firstCommentText": "", "providers": [{"network": "tiktok"}], "text": spec["tiktok_caption"],
                     "tiktokData": {"privacyOption": "PUBLIC_TO_EVERYONE", "title": spec.get("tiktok_title", ""),
                                    "photoCoverIndex": 0, "isAigc": True}})
    if update:
        print(json.dumps({"blogId": BRAND, "id": str(update[0]), "uuid": str(update[1]),
                          "info": json.dumps(base, ensure_ascii=False)}, ensure_ascii=False))
    else:
        print(json.dumps(base, ensure_ascii=False))
    return 0


# ---------------------------------------------------------------- post log
def log_post(net, when, file, title, episode="drawn-house", uuid=None, post_id=None, media=None):
    """Upsert the row for (network, file) in data/posted.csv, and keep the scheduler's ids in data/post-ids.csv."""
    path = os.path.join(ROOT, "data", "posted.csv")
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    hit = [r for r in rows[1:] if len(r) >= 5 and r[1] == net and r[3] == os.path.basename(file)]
    if hit:
        old = list(hit[-1])
        hit[-1][0], hit[-1][2], hit[-1][4] = when, episode, title
        print("posted.csv updated: %s -> %s" % (",".join(old[:1] + old[3:4]), when))
    else:
        rows.append([when, net, episode, os.path.basename(file), title])
        print("posted.csv added: %s %s %s" % (when, net, os.path.basename(file)))
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
        have.append([net, os.path.basename(file), when, str(uuid), str(post_id or ""), media or ""])
        with open(ids, "w", encoding="utf-8", newline="") as f:
            csv.writer(f, lineterminator="\n").writerows(have)
        print("post-ids.csv: uuid %s (the id changes on every update; the uuid does not)" % uuid)
    return 0


# ---------------------------------------------------------------- raw url and re-host check
def rawurl(path, sha=None):
    sha = sha or subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    rel = os.path.relpath(os.path.abspath(path), REPO)
    size = subprocess.run(["git", "-C", REPO, "cat-file", "-s", "%s:%s" % (sha, rel)], capture_output=True, text=True)
    if size.returncode != 0:
        print("FAIL %s is not in commit %s (commit and push first)" % (rel, sha[:9]))
        return 1
    if int(size.stdout.strip()) != os.path.getsize(path):
        print("FAIL the file on disk (%d bytes) differs from the one in %s (%s bytes): commit it first" % (
            os.path.getsize(path), sha[:9], size.stdout.strip()))
        return 1
    pushed = subprocess.run(["git", "-C", REPO, "branch", "-r", "--contains", sha], capture_output=True, text=True).stdout.strip()
    if not pushed:
        print("FAIL commit %s is not on the remote yet (push first)" % sha[:9])
        return 1
    print("https://raw.githubusercontent.com/%s/%s/%s" % (GITHUB, sha, urllib.parse.quote(rel)))
    return 0


def rehost(url, path):
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
    u = ("https://suggestqueries.google.com/complete/search?client=firefox&hl=en&gl=US" +
         ("&ds=yt" if yt else "") + "&q=" + urllib.parse.quote(q))
    try:
        out = subprocess.run(["curl", "-sS", "-m", "15", u], capture_output=True, timeout=25).stdout.decode("utf-8", "replace")
        return json.loads(out)[1]
    except Exception as e:                                           # a failed seed is reported, not fatal
        return ["ERR " + str(e)[:60]]


def kw(seeds, searches, out=None, n=25):
    rows = []
    for s in seeds:
        for src, yt in (("yt", True), ("web", False)):
            for rank, x in enumerate(suggest(s, yt), 1):
                rows.append(["suggest", src, s, rank, x, "", "", ""])
        time.sleep(0.2)
    for q in searches:
        res = subprocess.run(["yt-dlp", "--flat-playlist", "-J", "ytsearch%d:%s" % (n, q)], capture_output=True, timeout=180).stdout
        try:
            entries = json.loads(res).get("entries") or []
        except Exception:
            entries = []
        for rank, e in enumerate(entries, 1):
            if e:
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
    return 0


# ---------------------------------------------------------------- TikTok public page
def ttpage_one(url):
    html = subprocess.run(["curl", "-sS", "-m", "30", "-A", UA, url], capture_output=True).stdout.decode("utf-8", "replace")
    m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return {"url": url, "error": "no page data (blocked or changed); do not retry in a loop"}
    scope = json.loads(m.group(1)).get("__DEFAULT_SCOPE__", {})
    info = (scope.get("webapp.video-detail") or {}).get("itemInfo", {})
    it = info.get("itemStruct") or {}
    if not it:
        return {"url": url, "error": "no video in the page data (removed, private or region-locked)"}
    st = it.get("stats") or {}
    return {"url": url, "id": it.get("id"), "author": (it.get("author") or {}).get("uniqueId"),
            "followers": (it.get("authorStats") or {}).get("followerCount"),
            "created": it.get("createTime"), "seconds": (it.get("video") or {}).get("duration"),
            "plays": st.get("playCount"), "likes": st.get("diggCount"), "comments": st.get("commentCount"),
            "shares": st.get("shareCount"), "saves": st.get("collectCount"),
            "caption": it.get("desc"), "hashtags": [t.get("hashtagName") for t in it.get("textExtra") or [] if t.get("hashtagName")],
            "labels": it.get("diversificationLabels"), "category_type": it.get("CategoryType"),
            "is_aigc": it.get("IsAigc"), "aigc_label_type": it.get("aigcLabelType"), "suggested_words": it.get("suggestedWords"),
            "search_bar_words": [w.get("word") for s in (it.get("videoSuggestWordsList") or {}).get("video_suggest_words_struct") or []
                                 for w in s.get("words") or []] if isinstance(it.get("videoSuggestWordsList"), dict) else None,
            "is_reviewing": it.get("isReviewing"), "penalty": it.get("penaltyContext")}


def ttpage(urls, out=None):
    rows = []
    for u in urls:
        row = ttpage_one(u)
        rows.append(row)
        if "error" in row:
            print("FAIL %s: %s" % (u, row["error"]))
            continue
        like = (100.0 * (row["likes"] or 0) / row["plays"]) if row.get("plays") else 0
        print("%s  plays %s  likes %s (%.2f%%)  comments %s  shares %s  %ss  label %s" % (
            row["id"], row["plays"], row["likes"], like, row["comments"], row["shares"], row["seconds"],
            (row["labels"] or ["?"])[0]))
        print("   caption: %s" % (row["caption"] or "")[:160])
        if row["suggested_words"]:
            print("   TikTok suggests: %s" % "; ".join(row["suggested_words"]))
        time.sleep(1.0)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=1)
        print("wrote %s" % out)
    return 1 if any("error" in r for r in rows) else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("render"); p.add_argument("spec"); p.add_argument("out"); p.add_argument("--work", required=True)
    p = sub.add_parser("voicecheck"); p.add_argument("spec"); p.add_argument("mp4"); p.add_argument("--model", default="small.en")
    p = sub.add_parser("sheet"); p.add_argument("mp4"); p.add_argument("out"); p.add_argument("--step", type=float, default=1.5); p.add_argument("--cols", type=int, default=9)
    p = sub.add_parser("lint"); p.add_argument("specs", nargs="+"); p.add_argument("--mp4")
    p = sub.add_parser("payload"); p.add_argument("spec"); p.add_argument("--net", required=True, choices=["youtube", "tiktok"])
    p.add_argument("--when", required=True); p.add_argument("--media", required=True); p.add_argument("--cover-ms", type=int)
    p.add_argument("--first-comment"); p.add_argument("--kind", default="short", choices=["short", "video"]); p.add_argument("--thumb")
    p.add_argument("--update", nargs=2, metavar=("ID", "UUID")); p.add_argument("--no-lint", action="store_true")
    p = sub.add_parser("log"); p.add_argument("--net", required=True, choices=["youtube", "tiktok"]); p.add_argument("--when", required=True)
    p.add_argument("--file", required=True); p.add_argument("--title"); p.add_argument("--spec"); p.add_argument("--episode", default="drawn-house")
    p.add_argument("--uuid"); p.add_argument("--id"); p.add_argument("--media")
    p = sub.add_parser("rawurl"); p.add_argument("file"); p.add_argument("--sha")
    p = sub.add_parser("rehost"); p.add_argument("url"); p.add_argument("file")
    p = sub.add_parser("kw"); p.add_argument("seeds", nargs="*"); p.add_argument("--search", action="append", default=[]); p.add_argument("--out"); p.add_argument("--n", type=int, default=25)
    p = sub.add_parser("ttpage"); p.add_argument("urls", nargs="+"); p.add_argument("--json")
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
    elif a.cmd == "payload":
        rc = payload(a.spec, a.net, a.when, a.media, a.cover_ms, a.first_comment, a.kind, a.thumb,
                     update=a.update, no_lint=a.no_lint)
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
        rc = ttpage(a.urls, a.json)
    sys.exit(1 if rc else 0)


if __name__ == "__main__":
    main()
