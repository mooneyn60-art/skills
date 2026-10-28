"""Automatic acting and automatic gags for drawn Shorts (Nolan 10/28: "more animations with the animal", "I like how
you put stuff in about what you were talking about").

act()       runs in drawn.plan() once a line's word timings are known. It keys 2-4 actions to the spoken words
            (bite -> lunge + snap, run -> dash, dig -> dig wiggle, sleep -> slump, eat -> chomp bobs, jump -> hop,
            venom/sting -> shake, spin/twist -> spin), fills quiet stretches with idle business (head bob, weight
            shift, glances at the camera), and turns the animal toward a creature that pops in. Every action is an
            excursion that returns to where the animal was, so gags placed on the animal, the next line's
            inheritance and hand-set moves all stay valid. Hand-set and macro moves win: actions only go into the
            gaps between them. Everything is written as plain "moves" (pos, hop, walk, face, rot, s) and "set" params
            (bite, chew, mood, look), which both the drawn creatures and the photo cut-out (drawn_photo) read.
auto_gag()  runs in drawn_macros for a line without a `gag:`: picks a drawn_gags gag from the line's words, timed to
            the keyword ("word#n|pct": the word, or the share of the line if the TTS spells it differently). It never
            shows a count that wasn't spoken.
Turn either off per spec ("acting": false) or per line in an outline ("acting": false, "gag": false).
"""
import math
import re

# ------------------------------------------------------------------ verbs -> actions

VERBS = [
    ("lunge", r"(bite|bites|bit|biting|bitten|snap\w*|attack\w*|strike\w*|grab\w*|fight\w*|kill\w*|pounce\w*)"),
    ("dash", r"(run|runs|ran|running|chase\w*|race\w*|racing|dash\w*|sprint\w*|flee\w*|fled|trot\w*|escape\w*|"
             r"charge\w*|rush\w*|breaking|hunt|hunts|hunting)"),
    ("dig", r"(dig|digs|dug|digging|burrow\w*|tunnel\w*|claws?|scratch\w*)"),
    ("slump", r"(sleep\w*|slept|nap|naps|napping|hibernat\w*|tired|asleep|lazy|snooze\w*)"),
    ("chomp", r"(eat|eats|ate|eaten|eating|chew\w*|munch\w*|feed|feeds|feeding|feast\w*|devour\w*|swallow\w*|"
              r"gulp\w*|rip|rips|ripping|tear|tears|nibble\w*)"),
    ("hop", r"(jump\w*|hop|hops|hopping|leap\w*|climb\w*|bounc\w*|spring\w*)"),
    ("shake", r"(venom\w*|sting|stings|stinging|stung|poison\w*|toxi\w*|shock\w*|zap\w*|shiver\w*|shake\w*|shook|stink)"),
    ("spin", r"(spin\w*|spun|twist\w*|turns?|roll\w*|flip\w*)"),
]
VERBS = [(a, re.compile("^" + r + "$")) for a, r in VERBS]
LENGTH = {"lunge": 0.55, "dash": 0.95, "dig": 0.75, "slump": 0.6, "chomp": 0.85, "hop": 0.45, "shake": 0.55,
          "spin": 0.5, "bob": 0.55, "shift": 0.85, "turn": 0.75}
PRONOUNS = {"it", "its", "it's", "he", "his", "she", "her", "they", "their", "you", "your"}
TITLE_FLOOR = 440   # screen y the animal's head must stay below (TikTok title bar ends ~400)


def norm(w):
    return "".join(ch for ch in w.lower() if ch.isalnum() or ch == "'").strip("'")


def verb(word):
    w = norm(word)
    for action, rx in VERBS:
        if rx.match(w):
            return action
    return None


# ------------------------------------------------------------------ the actions (all return to rest)

def _action(kind, a, rx, ry, d, room, hop_max, s0, base):
    """(moves, sets) for one action at time a; rest (rx, ry), facing d (+1 right / -1 left)."""
    P = [rx, ry]
    mv, st = [], []
    if kind == "lunge":
        D = min(70, room)
        mv = [{"at": a, "dur": 0.13, "pos": [rx + d * D, ry]}, {"at": a + 0.26, "dur": 0.28, "pos": P}]
        st = [{"at": a, "dur": 0.08, "p": {"bite": 1.0, "mood": "angry"}},
              {"at": a + 0.3, "dur": 0.12, "p": {"bite": base.get("bite", 0.0)}},
              {"at": a + 0.5, "p": {"mood": base.get("mood")}}]
    elif kind == "dash":
        D = min(170, room)
        if D < 60:   # no room: feet scramble on the spot (a cartoon run-in-place)
            mv = [{"at": a, "dur": 0.55, "pos": P, "walk": True, "hop": 25}]
        else:
            mv = [{"at": a, "dur": 0.32, "pos": [rx + d * D, ry], "walk": True, "linear": True},
                  {"at": a + 0.4, "dur": 0.42, "pos": P, "walk": True, "face": -d},
                  {"at": a + 0.86, "dur": 0.05, "pos": P, "face": d}]
    elif kind == "dig":   # nose-down scrabbling; rotation is in screen space, so "nose down" depends on facing
        for k in range(3):
            mv += [{"at": a + 0.22 * k, "dur": 0.09, "pos": [rx + d * 8, ry], "rot": d * 13},
                   {"at": a + 0.22 * k + 0.11, "dur": 0.09, "pos": P, "rot": d * 3}]
        mv.append({"at": a + 0.66, "dur": 0.09, "pos": P, "rot": 0})
        st = [{"at": a, "dur": 0.1, "p": {"mood": "angry"}}, {"at": a + 0.7, "p": {"mood": base.get("mood")}}]
    elif kind == "slump":   # sinks and stays down to the end of the line (the next line resets s and rot)
        mv = [{"at": a, "dur": 0.5, "pos": P, "rot": -d * 5, "s": s0 * 0.93}]
        st = [{"at": a, "p": {"mood": "sleepy", "look": [0, 1]}}]
    elif kind == "chomp":
        for k in range(3):
            mv += [{"at": a + 0.27 * k, "dur": 0.1, "pos": P, "rot": d * 8},
                   {"at": a + 0.27 * k + 0.13, "dur": 0.11, "pos": P, "rot": 0}]
        st = [{"at": a, "dur": 0.1, "p": {"chew": 1.0}}, {"at": a + 0.82, "dur": 0.1, "p": {"chew": base.get("chew", 0.0)}}]
    elif kind == "hop":
        mv = [{"at": a, "dur": 0.42, "pos": P, "hop": max(30, min(130, hop_max))}]
    elif kind == "shake":
        for k in range(6):
            mv.append({"at": a + 0.07 * k, "dur": 0.06, "pos": [rx + (14 if k % 2 == 0 else -14), ry], "linear": True})
        mv.append({"at": a + 0.42, "dur": 0.08, "pos": P})
        st = [{"at": a, "p": {"mood": "shock"}}, {"at": a + 0.55, "p": {"mood": base.get("mood")}}]
    elif kind == "spin":
        h = max(20, min(60, hop_max))
        mv = [{"at": a, "dur": 0.16, "pos": P, "hop": h, "face": -d}, {"at": a + 0.24, "dur": 0.16, "pos": P, "hop": h, "face": d}]
    elif kind == "bob":   # idle: a head bob (a rock on the feet) and a glance
        mv = [{"at": a, "dur": 0.15, "pos": P, "rot": -d * 4}, {"at": a + 0.18, "dur": 0.15, "pos": P, "rot": d * 3},
              {"at": a + 0.36, "dur": 0.15, "pos": P, "rot": 0}]
    elif kind == "shift":   # idle: a little shuffle back and forth
        D = min(34, max(0, room))
        mv = [{"at": a, "dur": 0.38, "pos": [rx - d * D, ry], "walk": True},
              {"at": a + 0.42, "dur": 0.38, "pos": P, "walk": True}]
    return mv, st


# ------------------------------------------------------------------ act on one beat

def act(b, words, dur, hero, info, at_time, track, cam_at, half_w, top_h):
    """Add keyed actions to hero["moves"] / hero["set"] (in place). info = the macro's b["acting"]."""
    s0 = hero.get("s", 1.0)
    base = dict(hero.get("p", {}))
    moves = [dict(m, at=at_time(words, m.get("at"), 0.0)) for m in hero.get("moves", [])]
    moves.sort(key=lambda m: m["at"])
    sets = [dict(x, at=at_time(words, x.get("at"), 0.0)) for x in hero.get("set", [])]
    busy = [(m["at"] - 0.04, m["at"] + m.get("dur", 0.5) + 0.04) for m in moves]
    start = hero.get("pos", (0, 0))

    def rest(t):
        x, y, *_ = track(start, moves, words, t, s0, hero.get("rot", 0.0))
        return x, y

    def facing(t):
        if info.get("side"):
            flip = hero.get("flip")
            for m in moves:
                if "face" in m and m["at"] <= t:
                    flip = m["face"] < 0
            return -1 if flip else 1
        mbx = info.get("mb_x")
        x = rest(t)[0]
        tgt = mbx if mbx is not None else 540
        return -1 if tgt < x else 1

    def free(a, L):
        return 0.03 <= a and a + L <= dur - 0.04 and all(a + L <= b0 or a >= b1 for b0, b1 in busy)

    def room(a, x, d):
        cam, _ = cam_at(b, a)
        z = cam[2]
        sx = (x - cam[0]) * z + 540
        hw = half_w * z
        r = (1060 - (sx + hw)) / z if d > 0 else ((sx - hw) - 20) / z
        mbx = info.get("mb_x")
        if mbx is not None and (mbx - x) * d > 0:   # never shove into Meatball: keep 120 px of air in front
            r = min(r, abs(mbx - x) - half_w - 120)
        return max(0.0, r)

    def hop_room(a, y):
        cam, _ = cam_at(b, a)
        top = (y - top_h - cam[1]) * cam[2] + 960
        return max(0.0, (top - TITLE_FLOOR) / cam[2])

    placed = []   # (start, end, kind)
    slumped = [False]

    def place(kind, t, keyed=True):
        L = LENGTH[kind]
        tries = [t, t - 0.12, t + 0.2, t + 0.4] if keyed else [t]
        tries += sorted((b1 for _, b1 in busy if t - 0.7 < b1 < t + 0.7), key=lambda b1: abs(b1 - t))   # right after a walk
        for a in tries:
            if slumped[0] or not free(a, L):
                continue
            if any(abs(a - p0) < 0.45 for p0, _, _ in placed):
                continue
            x, y = rest(a)
            d = facing(a)
            mv, st = _action(kind, a, x, y, d, room(a, x, d), hop_room(a, y), s0, base)
            moves.extend(mv)
            sets.extend(st)
            busy.append((a - 0.05, a + L + 0.05))
            placed.append((a, a + L, kind))
            if kind == "slump":
                slumped[0] = True
            return True
        if kind in ("chomp", "slump", "shake", "lunge") and keyed and not slumped[0]:   # no room to move: act anyway
            _, st = _action(kind, t, 0, 0, 1, 0, 0, s0, base)
            sets.extend(st)
            placed.append((t, t + L, kind))
            return True
        return False

    # 1. verbs, keyed to the word that says them (one action per verb kind per 0.8 s)
    last = {}
    for s, e, w in words:
        k = verb(w)
        if k and s - last.get(k, -9) > 0.8 and len(placed) < 4:
            if place(k, s):
                last[k] = s

    # 2. a creature pops in: turn to look at it, then back
    for ex, ea in info.get("extras", []):
        ea = at_time(words, ea, 0.0)
        x, _ = rest(ea)
        d = facing(ea)
        side = 1 if ex > x else -1
        if info.get("side") and side != d and free(ea, LENGTH["turn"]) and len(placed) < 4:
            moves.extend([{"at": ea, "dur": 0.05, "pos": [x, rest(ea)[1]], "face": side},
                          {"at": ea + 0.7, "dur": 0.05, "pos": [x, rest(ea)[1]], "face": d}])
            busy.append((ea - 0.05, ea + 0.8))
            placed.append((ea, ea + 0.75, "turn"))
        else:
            sets += [{"at": ea, "p": {"look": [side * d, 0]}}, {"at": ea + 0.7, "p": {"look": base.get("look", [1, 0])}}]

    # 3. idle business on the line's longer words until there are 2-3 actions
    want = 2 if dur < 2.2 else 3
    cands = [(s, w) for s, e, w in words if len(norm(w)) >= 4]
    n_idle = 0
    for s, w in cands:
        if len(placed) >= want:
            break
        if place("bob" if n_idle % 2 == 0 else "shift", s):
            n_idle += 1
    for frac in (0.15, 0.55, 0.35, 0.75):   # still too few (short line or few long words): time-based
        if len(placed) >= want:
            break
        if place("bob" if n_idle % 2 == 0 else "shift", frac * dur, keyed=False):
            n_idle += 1

    # 4. glances: at the camera when the line talks to "you" or about it ("it", "his", its name), then back
    look0 = base.get("look", [1, 0])
    subj = set(info.get("subject", [])) | PRONOUNS
    g = next((s for s, e, w in words if norm(w) in subj and s < 0.75 * dur), None)
    if g is None and dur > 1.6:
        g = 0.45 * dur
    if g is not None and not slumped[0]:
        sets += [{"at": g, "p": {"look": [0, 0]}}, {"at": min(dur - 0.05, g + 0.65), "p": {"look": look0}}]

    moves.sort(key=lambda m: m["at"])
    sets.sort(key=lambda x: x["at"])
    hero["moves"] = moves
    hero["set"] = sets
    hero.setdefault("p", {})["idle"] = True
    return [k for _, _, k in sorted(placed)]


# ------------------------------------------------------------------ automatic gags (expand time: no word timings yet)

NUM = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
       "eleven": 11, "twelve": 12, "dozen": 12, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "hundred": 100,
       "hundreds": 100, "thousand": 1000, "thousands": 1000, "million": 10 ** 6, "millions": 10 ** 6, "billion": 10 ** 9}
FOOD = {"fish": "fish", "fishes": "fish", "egg": "egg", "eggs": "egg", "leaf": "leaf", "leaves": "leaf", "roots": "leaf",
        "berries": "leaf", "plants": "leaf", "grass": "leaf", "fruit": "leaf", "seeds": "leaf", "honey": "baby",
        "larvae": "baby", "bees": "baby", "babies": "baby", "grubs": "baby", "bones": "bone", "meat": "bone",
        "mice": "bone", "prey": "bone", "rocks": "rock", "stones": "rock", "ticks": "tick", "coins": "coin",
        "poop": "poop", "dung": "poop"}
RULES = [   # (gag builder, regex over a normalized word); first rule with a matching word wins
    (lambda k: {"mark": "stars"}, r"(resist\w*|immune|immunity|shrug\w*|survive\w*|unharmed|tough)"),
    (lambda k: {"mark": "zzz"}, r"(sleep\w*|slept|asleep|nap|naps|hibernat\w*|snooze\w*)"),
    (lambda k: {"mark": "stink"}, r"(stink\w*|smell\w*|odou?r|stench|reek\w*|musk\w*)"),
    (lambda k: {"meter": 1.0}, r"(venom\w*|poison\w*|toxi\w*|sting|stings|stung|hot|heat|burn\w*|fire|boil\w*|"
                                r"fast|faster|fastest|speed|quick)"),
    (lambda k: {"mark": "ice"}, r"(cold|colder|ice|icy|freez\w*|frozen|snow\w*)"),
    (lambda k: {"prop": "moon"}, r"(night|nights|nighttime|nocturnal|dark)"),
    ("number", None),
    (lambda k: {"clock": 6 if k in ("years", "year", "decades", "century", "centuries", "ancient", "old", "older") else 2},
     r"(years?|days?|hours?|minutes?|weeks?|months?|decades?|century|centuries|lifetime|lifespan|ancient|old|older|ages)"),
    (lambda k: {"prop": "rock"}, r"(heavy|heavier|weigh\w*|tons?|pounds?|kilos?|kilograms?)"),
    (lambda k: {"prop": "ruler"}, r"(size|thick|thicker|big|bigger|biggest|huge|giant|tall|taller|long|longer|length|small|smaller|"
                                   r"tiny|wide|inch\w*|feet|foot|meters?|metres?|centimet\w*|cm)"),
    ("food", r"(eat|eats|ate|eaten|eating|food|feed\w*|diet|snack\w*|meal\w*|hunt\w*|prey|feast\w*|devour\w*|"
             r"honey|larvae|insects|fish|mice|berries|roots|eggs|leaves|meat)"),
    (lambda k: {"mark": "anger"}, r"(bite|bites|bit|attack\w*|fight\w*|angry|fierce|furious|rage)"),
    (lambda k: {"mark": "alarm"}, r"(danger\w*|deadly|kill\w*|predators?|enemy|enemies|threat\w*|warning|escape\w*|"
                                   r"breaking|break|broke)"),
    (lambda k: {"mark": "sweat"}, r"(afraid|fear\w*|scare\w*|nervous|panic\w*|terrif\w*)"),
    (lambda k: {"mark": "hearts"}, r"(love\w*|mates?|mating|babies|baby|mother|mom|cute|pet|pets|friend\w*|rescue\w*|cuddl\w*)"),
    (lambda k: {"prop": "trophy"}, r"(smart\w*|clever\w*|learn\w*|record\w*|best|champion\w*|strongest|genius|win|wins|winning|won)"),
    (lambda k: {"prop": "magnifier"}, r"(stud\w*|scientists?|researchers?|discover\w*|found|filmed|documentary|camera|"
                                       r"spotted|noticed)"),
]
TIME = re.compile(r"^(years?|days?|hours?|minutes?|weeks?|months?|decades?|century|centuries|lifetime|lifespan)$")
RULES = [(f, re.compile("^" + r + "$") if r else None) for f, r in RULES]
NEG = {"nothing", "never", "no", "not", "isn't", "doesn't", "don't", "can't", "won't"}


def _at(toks, i):
    """'word#n|pct': the n-th spoken word starting with this one, or (if the TTS spells it differently) the share."""
    key = norm(toks[i]).replace("'", "")
    nth = sum(1 for t in toks[:i + 1] if norm(t).startswith(key)) or 1
    pct = max(8, min(85, round(100 * i / max(1, len(toks)))))
    return f"{key}#{nth}|{pct}%"


def _number(toks):
    for i, t in enumerate(toks):
        w = norm(t).replace(",", "")
        if w.isdigit():
            return i, int(w)
        if w in NUM:
            return i, NUM[w]
    return None


def auto_gag(say, skip=()):
    """A gag for a line from its own words, or None. skip: the animal's own name words ("honey" in honey badger)."""
    toks = say.split()
    words = [norm(t) for t in toks]
    words = ["" if w in skip else w for w in words]
    for build, rx in RULES:
        if build == "number":
            hit = _number(toks)
            if not hit:
                continue
            i, n = hit
            kind = next((FOOD[w] for w in words if w in FOOD), None)
            if kind and 2 <= n <= 8:   # a pile is a count: only the spoken count, only of a thing that was named
                return {"pile": kind, "n": n, "r": 40, "at": _at(toks, i), "dur": 0.25 * n}
            if any(TIME.match(w) for w in words):
                continue   # "20 years": the clock rule shows time passing without a number
            return {"meter": 1.0 if n >= 100 else 0.7, "at": _at(toks, i)}
        for i, w in enumerate(words):
            if not rx.match(w):
                continue
            if build == "food":
                if i and words[i - 1] in ("got", "get", "gets", "was", "were", "be", "being", "is", "are"):
                    continue   # "it got eaten": it is the food, not the eater
                kind = next((FOOD[x] for x in words if x in FOOD), "bone")
                return {"thought": kind, "at": _at(toks, i)}
            if rx.pattern.startswith("^(afraid") and NEG & set(words):
                break   # "afraid of nothing" is the opposite of sweating
            return dict(build(w), at=_at(toks, i))
    return None
