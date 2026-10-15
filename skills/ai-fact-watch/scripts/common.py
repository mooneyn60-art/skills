"""Shared helpers for AI Fact Watch: paths, fetching, and the fact parsers
(phones, street addresses, opening hours) used by truth.py and compare.py.

Standard library + BeautifulSoup only, so every script runs in a bare Python.
"""

from __future__ import annotations

import json
import re
import ssl
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRUTH_DIR = ROOT / "truth"
ANSWERS_DIR = ROOT / "answers"
FINDINGS_DIR = ROOT / "findings"
DATA_DIR = ROOT / "data"

UA = "Mozilla/5.0 (compatible; AIFactWatch/1.0; +fact-check of public business info)"
DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
DAY_NAMES = {"mon": "Monday", "tue": "Tuesday", "wed": "Wednesday", "thu": "Thursday",
             "fri": "Friday", "sat": "Saturday", "sun": "Sunday"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def slugify(text: str) -> str:
    text = text.lower().replace("'", "").replace("’", "")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")[:60]


def load_json(path: Path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except (FileNotFoundError, ValueError):
        return default


def save_json(path: Path, data) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return path


def fetch(url: str, timeout: int = 25, data: bytes | None = None,
          headers: dict | None = None) -> tuple[int, str, str]:
    """GET (or POST when data is given). Returns (status, final_url, body)."""
    hdrs = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.8"}
    hdrs.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=hdrs)
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        body = r.read(4_000_000).decode("utf-8", "replace")
        return r.status, r.geturl(), body


def clean_text(text: str) -> str:
    text = re.sub(r"[​‌‍﻿\xa0]", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()


# ---------------------------------------------------------------- phones
PHONE_RE = re.compile(r"(?<!\d)(?:\+?1[\s.-]?)?\(?([2-9]\d{2})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})(?!\d)")


def phones_in(text: str) -> list[str]:
    out = []
    for m in PHONE_RE.finditer(text or ""):
        p = f"({m.group(1)}) {m.group(2)}-{m.group(3)}"
        if p not in out:
            out.append(p)
    return out


def phone_digits(p: str) -> str:
    d = re.sub(r"\D", "", p or "")
    return d[-10:]


# -------------------------------------------------------------- addresses
SUFFIX = (r"(?:st|street|ave|avenue|rd|road|blvd|boulevard|dr|drive|hwy|highway|pkwy|parkway|"
          r"ln|lane|way|ct|court|pl|place|trail|trl|pike|sq|square|cir|circle)")
ADDR_RE = re.compile(
    r"\b(\d{1,6})\s+((?:[NSEW]\.?\s+|North\s+|South\s+|East\s+|West\s+)?(?:[A-Z][\w'.]*\s+){0,4}?"
    + SUFFIX + r")\b\.?", re.I)


# "766 W Pearce, Wentzville": AI answers often drop the street suffix
LOOSE_ADDR_RE = re.compile(r"\b(\d{2,6})\s+((?:[NSEW]\.?\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)(?=,)")


def addresses_in(text: str) -> list[dict]:
    """Street addresses as {raw, number, street_key}. street_key is the street
    name minus direction and suffix, lower-case, for loose matching."""
    out = []
    matches = list(ADDR_RE.finditer(text or ""))
    taken = [(m.start(), m.end()) for m in matches]
    matches += [m for m in LOOSE_ADDR_RE.finditer(text or "")
                if not any(a <= m.start() < b for a, b in taken)]
    for m in matches:
        raw = clean_text(m.group(0)).rstrip(".")
        if re.match(r"^\d{4}\s+(?:and|or)\b", raw, re.I):
            continue
        out.append({"raw": raw, "number": m.group(1), "street_key": street_key(m.group(2))})
    return out


def street_key(street: str) -> str:
    words = [w.strip(".").lower() for w in street.split()]
    drop = {"n", "s", "e", "w", "north", "south", "east", "west", "west.", "the"}
    words = [w for w in words if w not in drop]
    if words and re.fullmatch(SUFFIX, words[-1], re.I):
        words = words[:-1]
    return " ".join(words)


# ------------------------------------------------------------------ hours
DAY_ALIASES = {
    "monday": "mon", "mon": "mon", "mondays": "mon",
    "tuesday": "tue", "tues": "tue", "tue": "tue", "tuesdays": "tue",
    "wednesday": "wed", "wed": "wed", "weds": "wed", "wednesdays": "wed",
    "thursday": "thu", "thurs": "thu", "thur": "thu", "thu": "thu", "thursdays": "thu",
    "friday": "fri", "fri": "fri", "fridays": "fri",
    "saturday": "sat", "sat": "sat", "saturdays": "sat",
    "sunday": "sun", "sun": "sun", "sundays": "sun",
}
TOKEN_RE = re.compile(
    r"(?P<day>\b(?:mondays?|tuesdays?|wednesdays?|thursdays?|fridays?|saturdays?|sundays?|"
    r"mon|tues?|weds?|thur?s?|fri|sat|sun)\b\.?)"
    r"|(?P<daily>\b(?:daily|every day|7 days(?: a week)?|seven days)\b)"
    r"|(?P<closed>\bclosed\b)"
    r"|(?P<time>\b(?:noon|midnight|\d{1,2}(?::\d{2})?\s*(?:a\.?m\.?|p\.?m\.?|a|p)\b|\d{1,2}:\d{2}))"
    r"|(?P<range>\s*(?:-|–|—|to|through|thru|until|till)\s*)"
    r"|(?P<open_kw>\bopen(?:s|ing)?\b)|(?P<close_kw>\bclos(?:e|es|ing)\b)",
    re.I)


def _to_24h(tok: str) -> str | None:
    t = tok.lower().replace(".", "").replace(" ", "")
    if t == "noon":
        return "12:00"
    if t == "midnight":
        return "24:00"
    m = re.fullmatch(r"(\d{1,2})(?::(\d{2}))?(am|pm|a|p)?", t)
    if not m:
        return None
    h, mi, ap = int(m.group(1)), int(m.group(2) or 0), m.group(3)
    if ap and ap.startswith("p") and h != 12:
        h += 12
    if ap and ap.startswith("a") and h == 12:
        h = 0
    if not ap and h <= 7:  # bare "9" in "11-9" is evening
        h += 12
    if h > 24 or mi > 59:
        return None
    return f"{h:02d}:{mi:02d}"


def _expand(a: str, b: str) -> list[str]:
    i, j = DAYS.index(a), DAYS.index(b)
    return DAYS[i:j + 1] if i <= j else DAYS[i:] + DAYS[:j + 1]


def parse_hours(text: str) -> dict:
    """Best-effort opening-hours parser for website text and AI answers.

    Returns {day: {"open": "HH:MM"|None, "close": "HH:MM"|None} | "closed"}.
    Handles "Tue: 10a - 9p", "Sun-Thurs : 11am - 8pm", "Fri&Sat 11-9",
    "9:00am - 5:00pm Mon, Tues & Thurs", "closing around 8 PM Monday through
    Wednesday, Saturday and Sunday, and 9 PM Thursday and Friday",
    "11 AM opening daily", "Mon: Closed". Days it cannot place are omitted.
    """
    text = clean_text(text)
    toks = []
    for m in TOKEN_RE.finditer(text):
        kind = m.lastgroup
        val = m.group(0).strip()
        if kind == "day":
            val = DAY_ALIASES.get(val.lower().rstrip("."))
            if not val:
                continue
        if kind == "time":
            val = _to_24h(val)
            if not val:
                continue
        toks.append([kind, val, m.start(), m.end()])

    # merge "time range time" into one span, "day range day" into a day run
    merged, i = [], 0
    while i < len(toks):
        k = toks[i]
        if (k[0] == "time" and i + 2 < len(toks) and toks[i + 1][0] == "range"
                and toks[i + 2][0] == "time" and toks[i + 2][2] - k[3] < 14):
            merged.append(["span", (k[1], toks[i + 2][1]), k[2], toks[i + 2][3]])
            i += 3
            continue
        if (k[0] == "day" and i + 2 < len(toks) and toks[i + 1][0] == "range"
                and toks[i + 2][0] == "day" and toks[i + 2][2] - k[3] < 14):
            merged.append(["days", _expand(k[1], toks[i + 2][1]), k[2], toks[i + 2][3]])
            i += 3
            continue
        if k[0] == "day":
            merged.append(["days", [k[1]], k[2], k[3]])
        elif k[0] == "daily":
            merged.append(["days", list(DAYS), k[2], k[3]])
        elif k[0] != "range":
            merged.append(k)
        i += 1

    result: dict = {}
    pending: list[str] = []      # days waiting for a time
    last_days: list[str] = []    # days that just got a time (for "closed" after)
    held_span = None             # span seen before any days ("9-5 Mon, Tue")
    held_time = None             # lone time waiting for days ("8 PM Monday ...")
    mode = None                  # "open" | "close" for lone times
    prev_end = 0

    def put(days, open_=None, close=None, closed=False):
        for d in days:
            if closed:
                result[d] = "closed"
                continue
            cur = result.get(d)
            cur = cur if isinstance(cur, dict) else {"open": None, "close": None}
            if open_:
                cur["open"] = open_
            if close:
                cur["close"] = close
            result[d] = cur

    chain = None                 # span still applying to a ", & Thu" list
    for kind, val, start, end in merged:
        gap = text[prev_end:start]
        prev_end = end
        if kind != "days":
            chain = None
        if kind == "open_kw":
            mode = "open"
            if held_time and not pending:
                pending = []
            continue
        if kind == "close_kw":
            mode = "close"
            continue
        if kind == "days":
            if "." in gap or len(gap) > 40:
                pending = []
            if held_span and not pending:
                put(val, *held_span)
                last_days, held_span, chain = val, None, held_span
                continue
            if chain and re.fullmatch(r"[\s,&]*(?:and)?[\s,&]*", gap, re.I):
                put(val, *chain)
                last_days = val
                continue
            if held_time and not pending:
                if mode == "open":
                    put(val, open_=held_time)
                else:
                    put(val, close=held_time)
                last_days = val
                continue
            pending = pending + [d for d in val if d not in pending]
            continue
        if kind == "span":
            held_time = None
            if pending:
                put(pending, *val)
                last_days, pending = pending, []
            else:
                held_span = val
            continue
        if kind == "time":
            held_span = None
            if pending and len(gap) < 25:
                if mode == "open":
                    put(pending, open_=val)
                else:
                    put(pending, close=val)
                last_days, pending = pending, []
            else:
                held_time = val
            continue
        if kind == "closed":
            if pending:
                put(pending, closed=True)
                last_days, pending = pending, []
            elif last_days and len(gap) < 6:
                put(last_days, closed=True)
    return result


def hours_to_text(h: dict) -> str:
    if not h:
        return "not stated"
    parts = []
    for d in DAYS:
        v = h.get(d)
        if v is None:
            parts.append(f"{d.title()} not listed")
        elif v == "closed":
            parts.append(f"{d.title()} closed")
        else:
            parts.append(f"{d.title()} {fmt_time(v.get('open'))}-{fmt_time(v.get('close'))}")
    return ", ".join(parts)


def fmt_time(t: str | None) -> str:
    if not t:
        return "?"
    h, m = map(int, t.split(":"))
    if h == 24:
        return "midnight"
    suf = "am" if h < 12 else "pm"
    h12 = h % 12 or 12
    return f"{h12}{'' if m == 0 else f':{m:02d}'}{suf}"


# -------------------------------------------------------------- sentences
ABBREV = {"w", "e", "n", "s", "st", "ave", "blvd", "rd", "dr", "ln", "mr", "mrs", "ms", "inc", "co",
          "vs", "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "sept", "oct", "nov", "dec",
          "no", "ste", "pkwy", "hwy", "mt", "ft", "u.s", "e.g", "i.e", "approx", "jr", "sr"}
BOUNDARY_RE = re.compile(r"[.!?](?=[\s\n]+[\"'\u201c(\-]?[A-Z0-9\-])|\n+")


def sentence_spans(text: str) -> list[tuple[int, int]]:
    """Sentence (start, end) spans that do not split on "W. Pearce", "$30.00",
    "Sep. 22" or other abbreviations."""
    spans, start = [], 0
    for m in BOUNDARY_RE.finditer(text or ""):
        if m.group(0) == ".":
            word = re.search(r"([\w.]+)$", text[start:m.start()])
            if word and word.group(1).lower().rstrip(".") in ABBREV:
                continue
        end = m.end()
        if text[start:end].strip():
            spans.append((start, end))
        start = end
    if text and text[start:].strip():
        spans.append((start, len(text)))
    return spans


def sentence_around(text: str, start: int, end: int, max_len: int = 360) -> str:
    """The exact sentence of `text` containing [start:end], trimmed but never
    paraphrased, so reports can quote the AI verbatim."""
    for a, b in sentence_spans(text):
        if a <= start < b:
            s = text[a:b].strip()
            if len(s) > max_len:
                off = max(0, start - a - max_len // 3)
                s = ("\u2026" if off else "") + text[a + off:a + off + max_len].strip() + "\u2026"
            return s
    return text[max(0, start - 100):end + 100].strip()


def sentences(text: str) -> list[tuple[str, int]]:
    return [(text[a:b].strip(), a) for a, b in sentence_spans(text)]
