"""Scene macros for tools/drawn.py: a spec can be ~10 short lines instead of a hand-placed timeline.

A macro spec has a "stage" and beats with "m" (the macro) and "say" (the line):
  "stage": {"creature": "silverfish", "scene": "study", "scene_p": {"time": "night"}}
  "beats": [{"m": "hook", "say": "Something older than dinosaurs is eating your books."}, ...]

Every macro is timed to the line's own TTS ("40%" = 40 % of the way through the spoken line), places the hero
creature and Meatball on the same stage, and picks camera moves, Meatball poses and sound effects for itself.
Macros:
  hook      frame 0 = the creature already doing its creepy thing; Meatball jumps; camera pushes in
  name      the creature turns to camera; Meatball points ("Silverfish. Three tails.")
  fact      a plain fact line; four rotating stagings so consecutive facts never look the same
  xray      the anatomy reveal (the creature's config says what the x-ray shows)
  scale     Meatball shrinks next to it (how: "shrink") or it grows (how: "grow")
  count     "three things": the "with" creatures pop in one by one while Meatball counts
  escalate  creepier: shake, punch-in, a red danger pulse
  chase     it runs at Meatball, he flees
  calm      calm-then-drop: a relaxed half, then a snap zoom and a jump scare on the last words
  punch     the punchline: back to the hook's framing so the loop reads
  tease     "Subscribe. Part N is ...": the only ask, on the last line
  solo      a full scene change: the creature ALONE in its wild habitat (stage "wild", or the line's "scene"), big and
            centred, no Meatball, slow push-in; use 2-3 per video so it doesn't stay in one room (Nolan, 10/27)
Per-line overrides: scene, scene_p, with (list of species names, or {"sp" | "type", "x", "y", "s", "p", "front",
"pop": false = there from frame 0, "set", "moves"} for any actor), hero (false = not on
stage, or a dict of creature params), act (creature params set at 30 %), hero_at {x, y, rot}, hero_moves, mb_x (Meatball's mark), pose, prop, mood, sfx, pad.
"""
import copy

from drawn_species import SPECIES

SIDE = {"insect", "centipede", "worm", "fish", "bird", "mammal", "reptile"}
WATER = {"reef", "ocean", "deep"}
FLOOR = {"skin": 1100, "office": 1540, "press": 1600, "fibers": 1480}
MB_X, HERO_X = 330, 820
RESET = {"chew": 0.0, "pellets": 0, "xray": 0.0, "bite": 0.0, "wave": 0.0, "wrapped": 0.0, "talk": 0.0,
         "mood": None, "fly": 0.0}   # one-line actions never leak into the next line


def _cams(F):
    return {"wide": [560, F - 430, 1.1], "two": [600, F - 450, 1.18], "close": [660, F - 430, 1.3],
            "pull": [560, F - 560, 0.92], "mb": [430, F - 520, 1.25]}


class Stage:
    def __init__(self, st):
        self.name = st.get("creature")
        self.cfg = dict(SPECIES.get(self.name, {}), **st.get("creature_cfg", {}))
        self.type = st.get("actor") or ("sp." + self.name)
        self.scene = st.get("scene", "basement")
        self.scene_p = st.get("scene_p", {})
        self.wild = st.get("wild")
        self.wild_p = st.get("wild_p", {})
        self.hero_p = st.get("hero_p", {})
        self.side = self.cfg.get("plan") in SIDE or self.cfg.get("shape") == "long"
        self.s = st.get("s", self.cfg.get("s", 0.9))

    def floor(self, scene):
        return FLOOR.get(scene, 1500)

    def hero_y(self, F):
        return F if self.cfg.get("floor", True) else F - 560


def _hero(stage, F, x=HERO_X, s=None, p=None, moves=None, sets=None, front=False):
    a = {"id": "hero", "type": stage.type, "pos": [x, stage.hero_y(F)], "s": s or stage.s, "flip": stage.side,
         "front": front, "p": {"look": [1, 0] if stage.side else [-1, 0], **RESET, **stage.hero_p, **(p or {})}}
    if moves:
        a["moves"] = moves
    if sets:
        a["set"] = sets
    return a


def _extras(stage, line, F, at=("25%", "50%", "75%")):
    out = []
    slots = [(1080, F, False), (150, F + 60, True), (960, F - 640, False), (700, F + 80, True)]
    for k, w in enumerate(line.get("with", [])):
        w = {"sp": w} if isinstance(w, str) else w
        cfg = SPECIES.get(w.get("sp"), {})
        x, y, front = slots[k % len(slots)]
        if not cfg.get("floor", True):
            y = F - 640
        side = cfg.get("plan") in SIDE
        out.append({"id": f"x{k}", "type": w.get("type") or "sp." + w["sp"], "pos": [w.get("x", x), w.get("y", y)],
                    "s": 0.0, "front": w.get("front", front), "flip": w.get("flip", side and w.get("x", x) > MB_X),
                    "p": dict({"mood": w.get("mood", "shock"), "look": [1, 0] if side else [0, 0]}, **w.get("p", {})),
                    "moves": [{"at": at[k % len(at)], "dur": 0.3, "s": w.get("s", cfg.get("s", 0.8) * 0.8)}]})
        if w.get("pop", True) is False:   # already there from the first frame
            out[-1].update(s=w.get("s", cfg.get("s", 0.8) * 0.8), moves=[])
        if w.get("set"):
            out[-1]["set"] = w["set"]
        if w.get("moves"):
            out[-1]["moves"] = out[-1]["moves"] + w["moves"]
    return out


def _beat(stage, line, F, shots, hero, mb, sfx, extra=None, **kw):
    scene = line.get("scene", stage.scene)
    b = {"say": line["say"], "scene": scene, "scene_p": line.get("scene_p", stage.scene_p if scene == stage.scene else {}),
         "shots": shots, "actors": [], "mb": mb, "sfx": line.get("sfx", sfx), "pad": line.get("pad", 0.15)}
    if hero is not None and line.get("hero", True) is not False:
        if isinstance(line.get("hero"), dict):
            hero["p"].update(line["hero"])
        if line.get("hero_at"):   # a special mark for this line: {"x", "y", "rot"}, e.g. down inside a pore
            h = line["hero_at"]
            hero["pos"] = [h.get("x", hero["pos"][0]), h.get("y", hero["pos"][1])]
            hero["rot"] = h.get("rot", 0)
            hero.pop("moves", None)
        if line.get("hero_moves"):
            hero["moves"] = line["hero_moves"]
        if line.get("act"):
            hero.setdefault("set", []).append({"at": "30%", "dur": 0.3, "p": line["act"]})
        b["actors"].append(hero)
    b["actors"] += _extras(stage, line, F) + (extra or [])
    if line.get("mb_x"):   # move Meatball's mark (and any walk) when the room needs it
        dx = line["mb_x"] - mb["pos"][0]
        mb["pos"][0] += dx
        for mv in mb.get("moves", []):
            if "pos" in mv:
                mv["pos"] = [mv["pos"][0] + dx, mv["pos"][1]]
    if line.get("pose"):
        mb["pose"] = line["pose"]
    if line.get("prop"):
        mb["prop"] = line["prop"]
    if line.get("mood") and b["actors"] and b["actors"][0]["id"] == "hero":
        b["actors"][0]["p"]["mood"] = line["mood"]
    b.update(kw)
    return b


def _mb(stage, F, pose, x=MB_X, moves=None, gest=None, **kw):
    scene_water = kw.pop("water", False)
    m = {"pose": pose, "pos": [x, F], "size": 980, "look": "hero", "prop": None}
    if scene_water:
        m.update(helmet=True, float=True)
    if moves:
        m["moves"] = moves
    if gest:
        m["gest"] = gest
    m.update(kw)
    return m


def expand(spec):
    if not any("m" in b for b in spec.get("beats", [])):
        return spec
    stage = Stage(spec.get("stage", {}))
    out = []
    nfact = 0
    for i, line in enumerate(spec["beats"]):
        if "m" not in line:
            out.append(line)
            continue
        m = line["m"]
        if m == "solo" and "scene" not in line and stage.wild:
            line = dict(line, scene=stage.wild, scene_p=line.get("scene_p", stage.wild_p))
        scene = line.get("scene", stage.scene)
        F = stage.floor(scene)
        C = _cams(F)
        water = scene in WATER
        hero = _hero(stage, F)
        if m == "hook":
            hero = _hero(stage, F, x=HERO_X + 260, p={"mood": "smug"},
                         moves=[{"at": 0, "dur": 1.2, "pos": [HERO_X, stage.hero_y(F)], "walk": True}])
            hero["p"].update(line.get("act", {}))
            mb = _mb(stage, F, "shock", water=water, shake=0.5,
                     moves=[{"at": "30%", "dur": 0.45, "pos": [MB_X - 30, F], "hop": 220}])
            b = _beat(stage, line, F, [{"cam": C["wide"], "to": C["two"]}, {"at": "55%", "cam": C["two"], "to": C["close"]}],
                      hero, mb, ["scratch@0", "boing@30%", "pop@55%"])
            b["pad"] = line.get("pad", 0.1)
        elif m == "name":
            hero["p"].update({"mood": "happy", "wave": 1.0})
            b = _beat(stage, line, F, [{"cam": C["close"], "to": [C["close"][0] - 10, C["close"][1], 1.36]}], hero,
                      _mb(stage, F, "point", water=water, gest=[["60%", "think", 1.0]]), ["tink@15%", "pop@60%"])
        elif m == "fact":
            v = nfact % 4
            nfact += 1
            if v == 0:
                b = _beat(stage, line, F, [{"cam": C["wide"], "to": C["two"]}], hero,
                          _mb(stage, F, "think", water=water, gest=[["65%", "point", 1.0]]), ["tink@20%", "pop@65%"])
            elif v == 1:
                hero["p"]["mood"] = "smug"
                b = _beat(stage, line, F, [{"cam": C["close"], "to": [C["close"][0] - 10, C["close"][1] + 10, 1.36]},
                                           {"at": "60%", "cam": C["two"]}], hero,
                          _mb(stage, F, "nervous", water=water), ["whoosh@5%", "tink@60%"])
            elif v == 2:
                b = _beat(stage, line, F, [{"cam": C["two"], "to": [C["two"][0] + 60, C["two"][1], 1.2]}], hero,
                          _mb(stage, F, "point", water=water, moves=[{"at": "10%", "dur": 0.6, "pos": [MB_X + 90, F], "walk": True}],
                              gest=[["70%", "shrug", 1.0]]), ["scratch@10%", "pop@70%"])
            else:
                hero["p"]["mood"] = "happy"
                b = _beat(stage, line, F, [{"cam": C["mb"], "to": C["wide"]}], hero,
                          _mb(stage, F, "deadpan", water=water, look="viewer", gest=[["50%", "shrug", 1.2]]),
                          ["tink@10%", "pop@50%"])
        elif m == "xray":
            hero["set"] = [{"at": "25%", "dur": 0.3, "p": {"xray": 1.0}}, {"at": "92%", "dur": 0.25, "p": {"xray": 0.0}}]
            b = _beat(stage, line, F, [{"cam": C["close"], "to": [C["close"][0] - 20, C["close"][1] + 20, 1.42]}], hero,
                      _mb(stage, F, "think", water=water, gest=[["30%", "shock", 1.0]]), ["zap@25%", "tink@60%", "pop@92%"])
        elif m == "scale":
            if line.get("how", "shrink") == "grow":
                hero["moves"] = [{"at": "30%", "dur": 0.6, "s": stage.s * 1.6}]
                mb = _mb(stage, F, "shock", water=water, shake=0.5, moves=[{"at": "30%", "dur": 0.4, "pos": [MB_X - 60, F], "hop": 200}])
                shots = [{"cam": C["two"], "to": C["pull"]}]
            else:
                mb = _mb(stage, F, "shock", water=water, moves=[{"at": "30%", "dur": 0.5, "s": 620, "pos": [MB_X + 60, F], "hop": 160}])
                shots = [{"cam": C["two"], "to": [C["two"][0], C["two"][1] + 60, 1.3]}]
            b = _beat(stage, line, F, shots, hero, mb, ["whoosh@30%", "boing@60%"])
        elif m == "count":
            mb = _mb(stage, F, "think", water=water, gest=[["25%", "point", 0.6], ["50%", "point", 0.6], ["75%", "shock", 1.0]])
            b = _beat(stage, line, F, [{"cam": C["two"], "to": C["pull"]}], hero, mb, ["pop@25%", "pop@50%", "pop@75%"])
        elif m == "escalate":
            hero["p"].update({"mood": "angry", "bite": 1.0})
            dg = {"id": "flash", "type": "danger", "pos": [HERO_X, F - 300], "s": 1.0, "p": {"hidden": True},
                  "set": [{"at": "55%", "p": {"hidden": False}}]}
            b = _beat(stage, line, F, [{"cam": C["two"], "to": C["two"]}, {"at": "55%", "cam": C["close"], "to": [C["close"][0] - 40, C["close"][1] + 20, 1.42]}],
                      hero, _mb(stage, F, "nervous", water=water, shake=0.7, gest=[["55%", "shock", 1.2]]),
                      ["thud@10%", "zap@55%", "hit@60%"], extra=[dg], shake=["55%"])
        elif m == "chase":
            hero["moves"] = [{"at": "15%", "dur": 1.0, "pos": [MB_X + 260, stage.hero_y(F)], "walk": True, "linear": True}]
            hero["p"]["mood"] = "angry"
            mb = _mb(stage, F, "shock", water=water, shake=0.4,
                     moves=[{"at": "20%", "dur": 0.8, "pos": [MB_X - 140, F], "walk": True},
                            {"at": "70%", "dur": 0.4, "pos": [MB_X - 140, F], "hop": 200}])
            b = _beat(stage, line, F, [{"cam": C["two"], "to": [C["wide"][0] - 80, C["wide"][1], 1.12]}], hero, mb,
                      ["scratch@15%", "whoosh@25%", "boing@70%"])
        elif m == "calm":
            hero["p"]["mood"] = "calm"
            hero["set"] = [{"at": "65%", "dur": 0.15, "p": {"mood": "angry", "bite": 1.0}}]
            hero["moves"] = [{"at": "65%", "dur": 0.25, "pos": [HERO_X - 120, stage.hero_y(F)]}]
            b = _beat(stage, line, F, [{"cam": C["wide"], "to": C["two"]},
                                       {"at": "65%", "cam": [C["close"][0] - 60, C["close"][1] + 30, 1.5], "dur": 0.25}],
                      hero, _mb(stage, F, "laugh", water=water, gest=[["65%", "shock", 1.4]],
                                moves=[{"at": "66%", "dur": 0.4, "pos": [MB_X - 40, F], "hop": 220}]),
                      ["tink@15%", "thud@65%", "boing@67%"], flash=["65%"])
        elif m == "punch":
            b = _beat(stage, line, F, [{"cam": C["two"], "to": C["wide"]}], hero,
                      _mb(stage, F, "deadpan", water=water, look="viewer", gest=[["60%", "laugh", 1.4]]), ["pop@60%"])
        elif m == "solo":
            hy = stage.hero_y(F)
            hero = _hero(stage, F, x=540, s=stage.s * line.get("zoom", 1.3), p={"mood": line.get("mood", "smug")})
            hero["p"].update(line.get("act", {}))
            cy = hy - 300 if stage.cfg.get("floor", True) else hy + 200
            b = _beat(stage, line, F, [{"cam": [540, cy, 1.15], "to": [540, cy + 20, 1.32]}], hero,
                      _mb(stage, F, "think", hidden=True), ["whoosh@2%", "tink@60%"])
        elif m == "tease":
            nscene = line.get("scene", stage.scene)
            F = stage.floor(nscene)
            C = _cams(F)
            b = _beat(stage, line, F, [{"cam": C["two"], "to": [C["two"][0] - 30, C["two"][1] + 20, 1.26]}],
                      hero if nscene == stage.scene else None,
                      _mb(stage, F, "point", look="viewer", water=nscene in WATER, gest=[["55%", "psst", 1.4]]),
                      ["pop@2%", "whoosh@60%"])
            b["pad"] = line.get("pad", 0.45)
        else:
            raise SystemExit(f"drawn_macros: unknown macro {m!r}")
        out.append(b)
    spec = copy.deepcopy(spec)
    spec["beats"] = out
    return spec
