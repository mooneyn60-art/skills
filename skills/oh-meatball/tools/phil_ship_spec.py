"""Writes scripts/drawn-house/tt-philosophy-ship.json and yt-philosophy-ship.json (Ship of Theseus test, 11/18)."""
import json
import sys

OUT = "/home/user/skills/skills/oh-meatball/scripts/drawn-house/"

S = {  # source keys -> one line each (full quotes live in side-hustles channels/scripts/philosophy-ship-of-theseus.md)
    "SM21": "Sender R, Milo R. The distribution of cellular turnover in the human body. Nat Med 27:45-48 (2021), "
            "Weizmann Institute, doi:10.1038/s41591-020-01182-9, https://pubmed.ncbi.nlm.nih.gov/33432173/ : "
            "'In terms of cell numbers, close to 90% of the (0.33 +/- 0.02) x 10^12 cells per day turnover was blood "
            "cells.' Body text: 'a reference 70 kg person with 30 trillion host cells ... produces this number of "
            "cells every 80 d ... not all parts of the human body are ever replaced (for example, most brain neurons "
            "and cells of the eye lens ...) and hence complete turnover never happens.'",
    "SFM16": "Sender R, Fuchs S, Milo R. Revised Estimates for the Number of Human and Bacteria Cells in the Body. PLoS "
             "Biol 14:e1002533 (2016), Weizmann Institute, https://pubmed.ncbi.nlm.nih.gov/27541692/ : 'For human cells, "
             "we identify the dominant role of the hematopoietic lineage to the total count (~90%) and revise past "
             "estimates to 3.0x10^13 human cells.'",
    "SP05": "Spalding KL et al. Retrospective birth dating of cells in humans. Cell 122:133-143 (2005), Karolinska "
            "Institute, https://pubmed.ncbi.nlm.nih.gov/16009139/ : 'whereas nonneuronal cells are exchanged, "
            "occipital neurons are as old as the individual'",
    "PLU": "Plutarch, Life of Theseus (Dryden tr.), https://classics.mit.edu/Plutarch/theseus.html : 'The ship wherein "
           "Theseus and the youth of Athens returned had thirty oars, and was preserved by the Athenians ... for they "
           "took away the old planks as they decayed, putting in new and stronger timber in their place, insomuch "
           "that this ship became a standing example among the philosophers ... one side holding that the ship "
           "remained the same, and the other contending that it was not the same.'",
    "SEP-IT": "Stanford Encyclopedia of Philosophy, 'Identity Over Time' (rev. Jan 12 2026), "
              "https://plato.stanford.edu/entries/identity-time/ : 'Over a long period all of the planks composing a "
              "certain ship are replaced one by one. Eventually a ship indiscernible from the original, but composed "
              "of entirely different planks, results.'",
    "SEP-MC": "Stanford Encyclopedia of Philosophy, 'Material Constitution', "
              "https://plato.stanford.edu/entries/material-constitution/ : 'Thomas Hobbes imagined a scenario in which "
              "a custodian collects the original planks and puts them back in the original arrangement. ... we are "
              "left with two seafaring vessels ... But where is the original Ship of Theseus? Some will say that it "
              "is with the museum, since boats can survive the gradual replacement of parts. Others will say that it "
              "is with the custodian, since constructs can survive being taken apart and put back together. Both "
              "arguments seem compelling, but together they imply that the ship survives twice over.'",
}

Y, R, Wh, Gn, Bl = "#ffd34d", "#ff4b3e", "#ffffff", "#7cd67a", "#5fa8e8"


def card(rows, at=0.0, y=300, pop=False):
    c = {"rows": rows, "y": y, "at": at}
    if pop:
        c["pop"] = True
    return c


def A(id_, type_, pos, s=1.0, p=None, moves=None, set_=None, front=False):
    return {"id": id_, "type": type_, "pos": pos, "s": s, "front": front, "rot": 0.0, "p": p or {},
            "moves": moves or [], "set": set_ or []}


def mb(pose, pos=(860, 1500), size=420, gest=None, moves=None, look=None, prop=None):
    d = {"pose": pose, "pos": list(pos), "size": size, "gest": gest or [], "moves": moves or []}
    if look:
        d["look"] = look
    if prop:
        d["prop"] = prop
    return d


def beat(say, scene, scene_p, shots, actors, m, crd=None, sfx=None, f=None, pad=0.08, **kw):
    b = {"say": say, "scene": scene, "scene_p": scene_p, "shots": shots, "actors": actors, "mb": m, "pad": pad,
         "recut": False, "_f": f or []}
    if crd:
        b["card"] = crd
    if sfx:
        b["sfx"] = sfx
    b.update(kw)
    return b


def sh(at, cam, to):
    return {"at": at, "cam": cam, "to": to}


LAB = {"wall": "#1f2d4f"}


# ------------------------------------------------------------------ shared beats
def b_hook():
    return beat("Most of your body's cells get swapped out over the years. So are you even still you?",
                "ph_lab", LAB,
                [sh(0.0, [520, 1060, 1.3], [530, 1050, 1.36]), sh("So|55%", [560, 1010, 1.05], [560, 1000, 1.1])],
                [A("body", "ph_body", [380, 1500], 0.95, {"swap": 0.0}, set_=[{"at": 0.0, "p": {"swap": 1.0}, "dur": 3.2}]),
                 A("qm", "ph_qm", [800, 760], 0.7, {"on": 0.0}, set_=[{"at": "still|80%", "p": {"on": 1.0}, "dur": 0.3}],
                   front=True)],
                mb("shock", (790, 1500), 380, gest=[["So|55%", "point", 1.2]], look="body"),
                card([["ARE YOU STILL YOU?", Y, 96]], at="still|80%", y=200, pop=True),
                sfx=["pop@still|80%"], f=["SM21", "SFM16"], transition="cut")


def b_count():
    blood = [A(f"rb{k}", "ph_blood", [60 + 120 * k, 620 + (k * 137) % 560], 0.9 + 0.25 * (k % 3), {"spin": 0.8 + 0.2 * k},
               moves=[{"at": 0.0, "dur": 4.6, "pos": [700 + 130 * k, 560 + (k * 211) % 600]}]) for k in range(7)]
    return beat("Scientists counted. Your body replaces about three hundred and thirty billion cells a day.",
                "microscope", {},
                [sh(0.0, [540, 960, 1.0], [540, 960, 1.05]), sh("three|45%", [540, 900, 1.15], [540, 900, 1.2])],
                blood,
                mb("present", (820, 1500), 380, gest=[["three|45%", "shock", 1.0]]),
                card([["330 BILLION CELLS", Y, 104], ["EVERY DAY", Wh, 60, True]], at="three|45%", y=260, pop=True),
                sfx=["whoosh@0.1"], f=["SM21"])


def b_blood():
    return beat("Close to ninety percent of that is blood.",
                "ph_vein", {},
                [sh(0.0, [540, 960, 1.0], [540, 940, 1.12])],
                [A("rbA", "ph_blood", [420, 1000], 2.6, {"spin": 0.5}),
                 A("rbB", "ph_blood", [250, 1300], 1.4, {"spin": -0.7}),
                 A("rbC", "ph_blood", [640, 760], 1.2, {"spin": 0.9})],
                mb("point", (880, 1500), 400, look="rbA"),
                card([["CLOSE TO 90%: BLOOD", R, 96]], at="ninety|30%", y=260),
                f=["SM21"])


def b_neuron(short=False):
    say = ("But not everything. Most of your brain's neurons never get replaced. So you're part new, part original."
           if not short else
           "But most of your brain's neurons never get replaced. So you're part new, part original.")
    return beat(say, "classroom", {},
                [sh(0.0, [480, 960, 1.05], [480, 940, 1.12]), sh("part|62%", [460, 1020, 0.95], [460, 1010, 1.0])],
                [A("neu", "ph_neuron", [420, 900], 1.25, {"glow": 0.0, "lock": 0.0},
                   set_=[{"at": "never|35%", "p": {"lock": 1.0, "glow": 1.0}, "dur": 0.3},
                         {"at": "part|62%", "p": {"hidden": True}}]),
                 A("body2", "ph_body", [400, 1500], 0.95, {"swap": 0.65, "brain": 0.0, "hidden": True},
                   set_=[{"at": "part|62%", "p": {"hidden": False, "brain": 1.0}}])],
                mb("think", (880, 1500), 400, gest=[["never|35%", "point", 1.0]]),
                card([["MOST NEURONS: NEVER REPLACED", Y, 70]], at="never|35%", y=230),
                sfx=["pop@never|35%"], f=["SM21", "SP05"])


def b_greece():
    return beat("Philosophers have argued about this since ancient Greece, with a boat.",
                "study", {},
                [sh(0.0, [540, 1000, 1.0], [560, 1010, 1.04]), sh("boat|80%", [380, 1150, 1.5], [380, 1150, 1.6])],
                [A("ship", "ph_ship", [380, 1290], 0.55, {"new": 0.0, "seed": 3})],
                mb("present", (880, 1500), 380, look="ship", prop="mic"),
                card([["SINCE ANCIENT GREECE", Y, 92]], at="since|35%", y=240),
                sfx=["boing@boat|80%"], f=["PLU"])


def b_planks():
    return beat("The Athenians kept the ship of Theseus. As the old planks decayed, they swapped in new timber.",
                "ocean", {},
                [sh(0.0, [540, 1080, 1.1], [540, 1060, 1.15]), sh("As|45%", [500, 1180, 1.45], [500, 1170, 1.55])],
                [A("ship", "ph_ship", [520, 1330], 0.85, {"new": 0.0, "seed": 3},
                   set_=[{"at": "As|45%", "p": {"new": 0.45}, "dur": 2.0}]),
                 A("pk1", "ph_plank", [380, 1260], 0.8, {"old": True},
                   moves=[{"at": "As|45%", "dur": 0.9, "pos": [-200, 1700], "rot": -60}]),
                 A("pk2", "ph_plank", [1300, 900], 0.8, {"old": False},
                   moves=[{"at": "new|75%", "dur": 0.6, "pos": [640, 1260], "rot": 0}])],
                mb("present", (900, 1500), 360, look="ship"),
                card([["THE SHIP OF THESEUS", Y, 96], ["PLUTARCH", Wh, 50, True]], at=0.2, y=230),
                sfx=["whoosh@As|45%", "pop@new|75%"], f=["PLU"])


def b_none():
    return beat("Plank by plank, until not one original plank is left.",
                "night_sea", {},
                [sh(0.0, [520, 1180, 1.4], [520, 1180, 1.5]), sh("until|45%", [540, 1060, 1.0], [540, 1050, 1.05])],
                [A("ship", "ph_ship", [520, 1330], 0.85, {"new": 0.45, "seed": 3},
                   set_=[{"at": 0.0, "p": {"new": 1.0}, "dur": 2.0}])] +
                [A(f"fl{k}", "ph_plank", [300 + 120 * k, 1250], 0.6, {"old": True, "spin": 2.0},
                   moves=[{"at": 0.15 + 0.3 * k, "dur": 0.8, "pos": [-300 + 400 * (k % 2) * 4, 1800 - 900 * (k % 2)],
                           "rot": 120}]) for k in range(4)],
                mb("shock", (900, 1500), 360, look="ship"),
                card([["ZERO ORIGINAL PLANKS", R, 92]], at="until|45%", y=240),
                f=["SEP-IT"])


def b_vote(first=True):
    say = "Same ship, or new ship? Pick one, no fence-sitting." if first else \
        "So, same ship or new ship? Pick one, no fence-sitting."
    return beat(say, "tp_set" if first else "jh_stage",
                {"wall": "#2a3358", "wall2": "#323d6a", "floor": "#1d2340"} if first else {},
                [sh(0.0, [540, 960, 1.0], [540, 950, 1.06]), sh("Pick|55%", [540, 900, 1.12], [540, 900, 1.16])],
                [A("split", "ph_split", [540, 820], 1.0, {"on": 0.0, "a": Bl, "b": R},
                   set_=[{"at": 0.05, "p": {"on": 1.0}, "dur": 0.3}])],
                mb("point", (860, 1500), 400, gest=[["Pick|55%", "you", 1.2]]),
                card([["SAME SHIP OR NEW SHIP?", Y, 88], ["PICK ONE. NO FENCE-SITTING.", Wh, 50, True]], at=0.0, y=220,
                     pop=True),
                sfx=["pop@0.05"], f=[])


def b_twist():
    return beat("But here's the version that breaks everyone's brain.",
                "deep", {},
                [sh(0.0, [540, 1100, 1.25], [540, 1100, 1.35])],
                [A("qm1", "ph_qm", [230, 1180], 1.0, {"on": 0.0}, set_=[{"at": "breaks|60%", "p": {"on": 1.0}, "dur": 0.3}]),
                 A("qm2", "ph_qm", [850, 1120], 0.8, {"on": 0.0, "col": "#ff4b3e"},
                   set_=[{"at": "brain|85%", "p": {"on": 1.0}, "dur": 0.3}])],
                mb("nervous", (560, 1500), 470),
                card([["THE TWIST", R, 110]], at="breaks|60%", y=230, pop=True),
                sfx=["hit@breaks|60%"], f=[], transition="smash", freakout="brain|85%")


def b_hobbes(short=False):
    return beat("Thomas Hobbes asked: what if someone collected every old plank, and put them back together in the "
                "original arrangement?" if not short else
                "Thomas Hobbes asked: what if someone collected all the old planks, and put the ship back together?",
                "ph_shed", {},
                [sh(0.0, [540, 1100, 1.1], [520, 1100, 1.15]), sh("put|55%", [560, 1150, 1.0], [560, 1140, 1.04])],
                [A("guy", "person", [-150, 1500], 0.5, {"hat": "sailor", "item": "sack", "arm": "hold", "walk": 1.0},
                   moves=[{"at": 0.0, "dur": 1.8, "pos": [200, 1500], "walk": True}]),
                 A("pile", "ph_pile", [420, 1500], 1.3, {"n": 0.0}, set_=[{"at": 0.3, "p": {"n": 1.0}, "dur": 2.0},
                                                                         {"at": "put|55%", "p": {"hidden": True}}]),
                 A("old", "ph_ship", [560, 1380], 0.7, {"new": 0.0, "seed": 3, "bob": 0.0, "ghost": 1.0, "hidden": True},
                   set_=[{"at": "put|55%", "p": {"hidden": False}}, {"at": "put|55%", "p": {"ghost": 0.0}, "dur": 1.6}])],
                mb("think", (930, 1500), 340, look="old"),
                card([["HOBBES'S TWIST", Y, 96], ["REBUILT FROM THE OLD PLANKS", Wh, 50, True]], at=0.0, y=220),
                sfx=["whoosh@put|55%"], f=["SEP-MC"])


def two_ships(glow_l=None, glow_r=None, y=1330):
    l = A("shipL", "ph_ship", [270, y], 0.48, {"new": 1.0, "seed": 3, "sail": "#f4ecd6"})
    r = A("shipR", "ph_ship", [800, y], 0.48, {"new": 0.0, "seed": 5, "sail": "#e8dcc0"})
    if glow_l:
        l["set"] = [{"at": glow_l, "p": {"glow": 1.0}, "dur": 0.25}]
    if glow_r:
        r["set"] = [{"at": glow_r, "p": {"glow": 1.0}, "dur": 0.25}]
    return [l, r]


def b_two():
    return beat("Now there are two ships. So which one is the real Ship of Theseus?",
                "isle", {},
                [sh(0.0, [540, 1100, 1.0], [540, 1090, 1.05]), sh("which|45%", [540, 1180, 1.2], [540, 1180, 1.25])],
                two_ships(y=1270) + [A("qm", "ph_qm", [540, 760], 0.8, {"on": 0.0}, set_=[{"at": "real|70%", "p": {"on": 1.0}, "dur": 0.3}])],
                mb("shrug", (540, 1720), 330),
                card([["TWO SHIPS. WHICH ONE IS REAL?", Y, 74]], at="two|20%", y=230),
                sfx=["pop@real|70%"], f=["SEP-MC"])


def b_sides():
    return beat("Some say the one in Athens, because a boat can survive new parts.",
                "ph_harbor", {"time": "day"},
                [sh(0.0, [330, 1180, 1.35], [320, 1180, 1.42])],
                two_ships(glow_l="Athens|30%"),
                mb("think", (540, 1720), 300),
                card([["NEW PARTS? STILL THE SHIP.", Bl, 70]], at=0.0, y=230),
                f=["SEP-MC"])


def b_sides_short():
    return beat("Team Athens says new parts are fine. Team rebuilt says it's the same wood.",
                "ph_harbor", {"time": "day"},
                [sh(0.0, [330, 1180, 1.35], [320, 1180, 1.4]), sh("rebuilt|55%", [780, 1180, 1.35], [790, 1180, 1.4])],
                two_ships(glow_l="Athens|10%", glow_r="rebuilt|55%"),
                mb("think", (540, 1720), 300),
                card([["NEW PARTS? STILL THE SHIP.", Bl, 66], ["SAME WOOD? STILL THE SHIP.", R, 66]], at=0.0, y=230),
                f=["SEP-MC", "SEP-IT"])


def b_sides2():
    return beat("Others say the rebuilt one, because things can survive being taken apart and put back together.",
                "ph_museum", {},
                [sh(0.0, [540, 1150, 1.1], [540, 1150, 1.15]), sh("apart|60%", [540, 1250, 1.45], [540, 1250, 1.5])],
                [A("shipR", "ph_ship", [540, 1380], 0.6, {"new": 0.0, "seed": 5, "bob": 0.0, "glow": 0.0},
                   set_=[{"at": "rebuilt|15%", "p": {"glow": 1.0}, "dur": 0.25}]),
                 A("pk", "ph_plank", [540, 1050], 0.8, {"old": True},
                   moves=[{"at": "apart|60%", "dur": 0.35, "pos": [540, 700], "rot": 30},
                          {"at": "back|85%", "dur": 0.35, "pos": [540, 1250], "rot": 0}])],
                mb("point", (900, 1500), 340, look="shipR"),
                card([["SAME WOOD? STILL THE SHIP.", R, 70]], at=0.0, y=230),
                f=["SEP-MC"])


def b_twice():
    return beat("Agree with both, and the ship exists twice. That's not a ship, that's a damn glitch.",
                "tp_neon", {},
                [sh(0.0, [540, 1100, 1.0], [540, 1100, 1.06]), sh("glitch|85%", [540, 1150, 1.3], [540, 1150, 1.35])],
                two_ships(glow_l=0.0, glow_r=0.0),
                mb("facepalm", (540, 1720), 330),
                card([["THE SHIP EXISTS TWICE?", R, 86]], at="twice|40%", y=230, pop=True),
                sfx=["hit@glitch|85%"], f=["SEP-MC"], shake=["glitch|85%"], flash=["glitch|85%"])


def b_ruling():
    return beat("Meatball's ruling: It's NOT the same ship.",
                "office", {},
                [sh(0.0, [540, 1150, 1.25], [540, 1150, 1.35])],
                [A("shipN", "ph_ship", [280, 1440], 0.4, {"new": 1.0, "seed": 3, "bob": 0.0})],
                mb("deadpan", (650, 1500), 520, gest=[["NOT|60%", "point", 1.0]]),
                card([["IT'S NOT THE SAME SHIP.", Y, 92]], at="NOT|55%", y=230, pop=True),
                sfx=["hit@NOT|55%"], f=[])


def b_phone():
    return beat("And if you disagree, you've never replaced a phone screen.",
                "tp_living", {"sofa": True},
                [sh(0.0, [540, 1000, 1.0], [540, 1000, 1.05]), sh("phone|75%", [400, 980, 1.25], [400, 980, 1.3])],
                [A("ph", "ph_phone", [380, 1000], 0.9, {"crack": 0.0, "rot": -0.08},
                   set_=[{"at": "replaced|55%", "p": {"crack": 1.0}, "dur": 0.4}])],
                mb("you", (860, 1500), 400, look="viewer"),
                card([["EVER REPLACED A PHONE SCREEN?", Wh, 66, True]], at="replaced|55%", y=230),
                sfx=["hit@replaced|55%"], f=[])


def b_phone2():
    return beat("New screen, and that phone was never the same again. Neither was my wallet.",
                "kitchen", {},
                [sh(0.0, [400, 980, 1.2], [400, 980, 1.25]), sh("Neither|65%", [620, 1150, 1.05], [620, 1140, 1.1])],
                [A("ph", "ph_phone", [380, 1000], 0.9, {"crack": 1.0, "fix": 0.0, "rot": -0.08},
                   set_=[{"at": 0.1, "p": {"fix": 1.0}, "dur": 0.8}])],
                mb("laugh", (860, 1500), 400, gest=[["Neither|65%", "facepalm", 1.2]]),
                f=[])


def b_end():
    return beat("Half of you are wrong. And remember...",
                "skin", {},
                [sh(0.0, [520, 1000, 1.0], [520, 1000, 1.02])],
                [A("body", "ph_body", [400, 1500], 0.95, {"swap": 0.0})],
                mb("you", (860, 1500), 430, look="viewer"),
                card([["HALF OF YOU ARE WRONG.", Y, 92], ["COMMENTS.", Wh, 70, True]], at=0.0, y=200, pop=True),
                f=[], pad=0.08)


BASE = {
    "series": "Meatball Philosophy (test)",
    "photo_credits": [],
    "voice": "kokoro:adam-puck",
    "music": "mystery",
    "music_db": -18,
    "captions": 124,
    "cap_words": 1,
    "caption_y": 1660,
    "cap_swap": {"damn": "#@%!"},
    "cap_key": ["cells", "you", "billion", "ninety", "blood", "neurons", "never", "greece", "theseus", "planks",
                "plank", "timber", "same", "new", "ship", "hobbes", "two", "real", "twice", "not", "phone", "screen",
                "wallet", "original", "half"],
    "cine": {"light": "off", "shots": "off"},
    "loop": True,
    "cut_whoosh": False,
    "sources": [k + " " + v for k, v in S.items()],
}


def build(kind):
    if kind == "tt":
        beats = [b_hook(), b_count(), b_blood(), b_neuron(), b_greece(), b_planks(), b_none(), b_vote(True),
                 b_twist(), b_hobbes(), b_two(), b_sides(), b_sides2(), b_twice(), b_ruling(), b_phone(), b_phone2(),
                 b_vote(False), b_end()]
        meta = {"title": "Ship of Theseus: Are You Still You?",
                "tiktok_title": "Ship of Theseus: Are You Still You?",
                "tiktok_caption": "Ship of Theseus: are you still you? #shipoftheseus #philosophy #thoughtexperiment #meatballmyths"}
    else:
        beats = [b_hook(), b_neuron(short=True), b_planks(), b_none(), b_vote(True), b_twist(), b_hobbes(short=True),
                 b_two(), b_sides_short(), b_twice(), b_ruling(), b_phone(), b_vote(False), b_end()]
        meta = {"title": "The Ship of Theseus: Replace Every Plank and It's Not the Same Ship 🚢",
                "description": ("If you replace every plank of a ship, is it still the same ship? Meatball says no. Plutarch's "
                                "Ship of Theseus, Thomas Hobbes's rebuilt-ship twist, and your own body: most of your cells "
                                "get replaced over time, but most of your brain's neurons never do.\n\n"
                                "Sources: Sender & Milo, Nature Medicine 2021 (cell turnover); Spalding et al., Cell 2005 "
                                "(neurons); Plutarch, Life of Theseus; Stanford Encyclopedia of Philosophy, 'Identity Over "
                                "Time' and 'Material Constitution'.\n\nSame ship or new ship? Pick one in the comments.\n\n#shipoftheseus #philosophy #meatballmyths #shorts"),
                "tags": ["ship of theseus", "ship of theseus paradox", "philosophy", "thought experiment",
                         "identity paradox", "are you still the same person", "cell replacement", "thomas hobbes",
                         "plutarch", "philosophy shorts", "meatball myths"],
                "pinned_comment": "Hot take: if you replace every plank, the old ship is the REAL one. Fight me 🍝"}
    spec = dict(BASE, **meta)
    if kind == "yt":
        spec.pop("series")
    spec["_note"] = ("Philosophy test 11/18 (Studio notes 2:50/2:55/2:58/3:05 PM in side-hustles TASKS.md). Script + "
                     "sources: side-hustles channels/scripts/philosophy-ship-of-theseus.md. Hand-made beats; pictures in "
                     "tools/drawn_phil_art.py (ph_). Voice E2 plain (kokoro:adam-puck, no speed/pitch/formant/drive), "
                     "one-word captions (cap_words 1), one light swear (line 'damn glitch', after 7 s; captions show "
                     "#@%!). Written by tools/phil_ship_spec.py; edit that and rerun it (both cuts together).")
    spec["beats"] = beats
    return spec


if __name__ == "__main__":
    for kind, name in (("tt", "tt-philosophy-ship.json"), ("yt", "yt-philosophy-ship.json")):
        json.dump(build(kind), open(OUT + name, "w"), indent=1, ensure_ascii=False)
        print("wrote", OUT + name)
