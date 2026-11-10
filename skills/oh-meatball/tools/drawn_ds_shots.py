"""The hand-made shots for "Don't squish it" episode 1 (tools/drawn_dontsquish.py): spec line id -> recipe + args.
drawn_dontsquish._shots_table() builds the cold open and the first 13 lines of question 1; extend() adds every other
line. Word anchors fall back to a share of the line ("word|40%"). Coordinates: the corner scene's ceiling corner is
at (700, 150), Carol hangs at (720, 610) at scale 0.6; board scenes are centred on (0, 0)."""
import copy


def extend(T):
    from drawn_dontsquish import (CAROL, CS, GREEN, RED, YEL, HIDDEN, actor, cam, carol, mb, pop, push)  # noqa: F401

    def C(c0, to=None, **kw):   # a corner shot
        d = {"r": "corner", "cam": c0, "to": to if to is not None else push(c0, 1.07)}
        d.update(kw)
        return d

    def S(scene, c0, to=None, actors=(), **kw):   # any other scene
        d = {"r": "scene", "scene": scene, "cam": c0, "to": to if to is not None else push(c0, 1.06), "actors": list(actors)}
        d.update(kw)
        return d

    def B(c0, to=None, actors=(), color="#1b1724", **kw):   # the dark board background
        return S("ds_board_bg", c0, to, actors, scene_p={"color": color}, norecut=True, **kw)

    def lab(idn, text, pos, at=None, px=56, color="#ffffff", front=True):
        return actor(idn, "ds_label", pos, 1.0, {"text": text, "px": px, "color": color, "on": 0.0 if at else 1.0},
                     sets=pop(at) if at else None, front=front)

    def chip(idn, text, pos, at=None):
        return actor(idn, "ds_chip_src", pos, 1.0, {"text": text, "on": 0.0 if at else 1.0}, sets=pop(at) if at else None,
                     front=True)

    def prop(idn, kind, pos, s=1.0, p=None, at=None, sets=None, moves=None, front=False, rot=0.0):
        pp = dict({"kind": kind, "on": 0.0 if at else 1.0}, **(p or {}))
        st = (pop(at) if at else []) + (sets or [])
        return actor(idn, "ds_prop", pos, s, pp, sets=st or None, moves=moves, front=front, rot=rot)

    def tagc(idn="tag", pos=None, at=None):
        return actor(idn, "ds_tag", pos or [CAROL[0] - 230, CAROL[1] + 40], 0.8, {"on": 0.0 if at else 1.0, "text": "CAROL"},
                     sets=pop(at, 0.35) if at else None)

    def giant(idn="giant", pos=(1050, 960), s=0.55, p=None, moves=None, sets=None, flip=True, rot=0.0):
        return actor(idn, "giant_spider", list(pos), s, dict({"mood": "angry"}, **(p or {})), sets, moves, flip=flip, rot=rot)

    MBF = lambda pose, pos=(1230, 900), size=460, **kw: mb(pose, pos, size, float=True, look=kw.pop("look", "hero"), **kw)  # noqa: E731
    DARK = [0.03, 0.03, 0.10, 0.42]

    # ------------------------------------------------------------------------------------------ question 1 (rest)
    T["s1.l8"]["shots"] = [cam([250, 1000, 0.82], [560, 1000, 0.86]),
                           cam([700, 1120, 1.7], [760, 1130, 1.8], at="summer|55%", dur=0.4)]   # cut to the tray
    pie = [[63, "#c98a4a", "63 HOUSE SPIDERS"], [6, "#e2d3b0", "6 CELLAR SPIDERS"], [33, "#8a94a6", "33 UNIDENTIFIED SPIDER BITS"]]
    T["s1.l12"] = B([0, 0, 1.0], [0, 0, 1.02], [actor("pie", "ds_pie", [-470, 40], 1.0,
                     {"slices": pie, "R": 360, "lx": 440, "px": 66, "gap": 150, "w0": 1.0, "w1": 0.0, "w2": 0.0},
                     sets=[{"at": 0.0, "dur": 0.4, "p": {"w1": 1.0}}, {"at": "rest|12%", "dur": 0.9, "p": {"w2": 1.0}}])],
                    card_at="Every|55%", card_x=1400, card_w=820, sfx=["pop@0.05", "whoosh@rest|12%", "stamp@Every|60%"])
    T["s1.l13"] = S("ds_floor", [700, 760, 1.0], [640, 740, 1.1],
                    [actor("shadow", "ds_shadow", [-500, 900], 1.3, {"a": 0.6}, rot=8,
                           moves=[{"at": 0, "dur": 1.8, "pos": [760, 860], "linear": True}])], sfx=["thud@0.1", "step@size|60%"])
    T["s1.l15"] = B([0, 120, 1.0], [0, 130, 1.04], [actor("row", "ds_fade_row", [0, 360], 1.0, {"gone": 0.0},
                                                          sets=[{"at": "why|35%", "dur": 2.4, "p": {"gone": 5.0}}]),
                                                    lab("brit", "BRITAIN", [0, -300], "British|8%", 60)],
                    sfx=["whoosh@why|35%"])
    T["s1.l16"] = S("ds_wall", [820, 520, 0.85], [840, 580, 0.95],
                    [actor("gshadow", "ds_shadow", [1130, -420], 1.0, {"a": 0.38, "squash": 0.9}, rot=95,
                           moves=[{"at": "big|35%", "dur": 1.6, "pos": [1130, 500]}]),
                     giant("giant", (900, -300), 0.75, {"mood": "angry"}, rot=90, flip=False,
                           moves=[{"at": "big|35%", "dur": 1.6, "pos": [900, 620], "walk": True}]),
                     prop("clock", "clock", [300, 260], 0.9, {"hour": 2.0}, at="Two|20%")],
                    scene_p={"dark": True}, sfx=["tink@Two|20%", "scratch@fast|80%"])
    T["s1.l17"] = C([760, 560, 0.92], [740, 580, 0.98], carol_s=0.52, carol={"still": True, "mood": "worry", "look": [0.6, 0.8]},
                    extras=[giant("giant", (1700, 1180), 0.95, moves=[{"at": 0, "dur": 2.0, "pos": [1380, 1180], "walk": True}])],
                    sfx=["step@fraction|30%"])
    T["s1.l18"] = C([700, 620, 0.9], [700, 640, 0.95], carol={"still": True, "mood": "shock", "look": [0.8, 0.9]},
                    carol_sets=[{"at": "under|50%", "dur": 0.6, "p": {"look": [-0.8, 0.9]}}],
                    extras=[giant("giant", (1800, 1080), 0.7, moves=[{"at": 0.1, "dur": 2.2, "pos": [-400, 1080], "walk": True, "linear": True}])],
                    sfx=[])
    T["s1.l19"] = S("ds_board_bg", [0, 60, 1.0], [0, 60, 1.04],
                    [actor("split", "ds_split", [0, 0]), carol({"mood": "smug", "thread": 500, "look": [1, 0]}, [-480, -60], 0.45, idn="hero"),
                     giant("giant", (500, 330), 0.62, {"mood": "angry", "look": [-1, 0]})],
                    vs={"left": "CAROL", "right": "THE BIG ONE", "panels": False, "name_y": 900, "at": "beat|60%"},
                    norecut=True, sfx=["thud@beat|60%"])
    T["s1.l20"] = C([800, 660, 1.15], [800, 650, 1.22], carol_pos=[560, 600], carol={"mood": "smug", "look": [1, 0.5], "reach_dir": 1},
                    carol_sets=[{"at": "distance|25%", "dur": 0.6, "p": {"reach": 1.0}}],
                    extras=[giant("giant", (1080, 960), 0.52, {"mood": "worry"}),
                            actor("gap", "ds_dim", [640, 700], 1.0, {"to": [330, 120], "grow": 0.0, "text": ""},
                                  sets=[{"at": "legs|60%", "dur": 0.5, "p": {"grow": 1.0}}])], sfx=["whoosh@legs|60%"])
    T["s1.l22"] = C([960, 820, 1.6], [980, 830, 1.72], carol_pos=[560, 600],
                    carol={"flick": 1.0, "flick_to": [(1000 - 560) / CS, (720 - 600) / CS], "mood": "angry", "look": [1, 0.4]},
                    extras=[giant("giant", (1000, 900), 0.52, {"mood": "shock", "wrapped": 0.45, "walk": 0.8},
                                  sets=[{"at": 0.1, "dur": 2.6, "p": {"wrapped": 1.0}}])],
                    sfx=["whoosh@Left|5%", "whoosh@burrito|60%"], norecut=True)
    T["s1.l23"] = C([800, 720, 1.25], [860, 760, 1.4], carol_pos=[560, 600], carol={"mood": "angry", "look": [1, 0.5]},
                    carol_moves=[{"at": "moves|35%", "dur": 0.8, "pos": [820, 700], "walk": True}],
                    carol_sets=[{"at": "bites|75%", "dur": 0.1, "p": {"bite": 1.0}}, {"at": "bites+0.4|90%", "dur": 0.3, "p": {"bite": 0.0}}],
                    extras=[giant("giant", (1000, 900), 0.52, {"mood": "shock", "wrapped": 1.0})], sfx=["step@moves|35%", "crunch@bites|75%"])
    T["s1.l24"] = S("bedroom", [820, 1060, 0.92], [820, 1040, 1.0],
                    [prop("blanket", "lump", [860, 1260], 1.3, front=True), prop("clock", "clock", [-20, 820], 0.6, {"hour": 2.0})],
                    scene_p={"time": "night"},
                    mb=mb("nervous", (860, 1300), 760, look="viewer", gest=[["respected|70%", "deadpan", 2.0]],
                          moves=[{"at": "respected|75%", "dur": 0.25, "pos": [860, 1312]}, {"at": "respected+0.3|85%", "dur": 0.25, "pos": [860, 1300]}]),
                    sfx=["tink@sleep|50%"])
    T["s1.l25"] = C([720, 520, 1.2], [1080, 470, 1.15], carol={"look": [1, 0], "mood": "smug"},
                    carol_moves=[{"at": 0.1, "dur": 2.1, "pos": [1380, 430], "walk": True}], sfx=["step@0.2", "step@home|60%"])
    T["s1.l26"] = S("ds_wall", [800, 450, 1.0], [820, 450, 1.08],
                    [actor("orb", "ds_orb", [1050, 450], 1.0, {"r": 380}),
                     actor("owner", "house_sp_small", [1050, 560], 0.32, {"mood": "calm"}),
                     carol({"mood": "smug", "look": [1, 0]}, [100, 250], 0.48, moves=[{"at": "walk|20%", "dur": 1.4, "pos": [720, 330], "walk": True}])],
                    sfx=["step@walk|25%", "boing@purpose|80%"])
    T["s1.l27"] = B([0, 0, 1.0], [0, 0, 1.03], [
        actor("fly", "fly", [-560, 100], 0.9, {"mood": "worry"}), actor("eggs", "ds_bundle", [0, -330], 1.6, {"len": 140}),
        actor("own", "house_sp_small", [560, 260], 0.55, {"mood": "worry"}),
        lab("l1", "INSECTS", [-560, 330], None, 52), lab("l2", "EGGS", [0, 330], None, 52), lab("l3", "THE OWNER", [560, 330], None, 52),
        actor("x1", "ds_cross", [-560, 60], 1.0, {"on": 0.0, "r": 150}, sets=[{"at": "insects|30%", "dur": 0.3, "p": {"on": 1.0}}], front=True),
        actor("x2", "ds_cross", [0, 0], 1.0, {"on": 0.0, "r": 150}, sets=[{"at": "eggs|55%", "dur": 0.3, "p": {"on": 1.0}}], front=True),
        actor("x3", "ds_cross", [560, 100], 1.0, {"on": 0.0, "r": 150}, sets=[{"at": "spider|85%", "dur": 0.3, "p": {"on": 1.0}}], front=True)],
        sfx=["stamp@insects|30%", "stamp@eggs|55%"])
    T["s1.l28"] = S("ds_lab", [900, 700, 0.95], [940, 700, 1.02],
                    [actor("arena", "ds_arena", [560, 900], 1.25), carol({"mood": "smug"}, [560, 790], 0.25, idn="hero")],
                    mb=mb("present", (1150, 900), 600, look="viewer", prop="paper"), card_at="aggressive|40%", sfx=["tink@aggressive|40%"])
    T["s1.l29"] = S("ds_wall", [850, 450, 1.1], [820, 430, 1.16],
                    [actor("orb", "ds_orb", [1050, 450], 1.0, {"r": 380, "jiggle": 0.0},
                           sets=[{"at": "jiggle|25%", "dur": 0.2, "p": {"jiggle": 1.0}}, {"at": "lure|50%", "dur": 0.2, "p": {"jiggle": 0.0}}]),
                     actor("owner", "house_sp_small", [1050, 560], 0.32, {"mood": "calm", "wrapped": 0.0},
                           moves=[{"at": "owner|45%", "dur": 0.7, "pos": [800, 420], "walk": True}],
                           sets=[{"at": "eat|78%", "dur": 0.4, "p": {"wrapped": 1.0}}]),
                     carol({"mood": "smug", "look": [1, 0]}, [640, 300], 0.45, sets=[{"at": "jiggle|25%", "dur": 0.2, "p": {"wave": 1.0}}])],
                    sfx=["zap@jiggle|25%", "crunch@eat|78%"])
    T["s1.l30"] = S("ds_wall", [880, 700, 0.95], [900, 700, 1.02],
                    [actor("door", "ds_doorbell", [900, 1000], 1.0, {"ring": 0.0, "open": 0.0},
                           sets=[{"at": "doorbell|30%", "dur": 0.2, "p": {"ring": 1.0}}, {"at": "answers|75%", "dur": 0.4, "p": {"open": 1.0, "ring": 0.0}}]),
                     carol({"mood": "smug", "look": [1, 0.4]}, [1220, 480], 0.42, sets=[{"at": "doorbell|30%", "dur": 0.2, "p": {"wave": 1.0}}]),
                     actor("owner", "house_sp_small", [880, 990], 0.25, {"mood": "happy", "hidden": True},
                           sets=[{"at": "answers|80%", "p": {"hidden": False}}])],
                    mb=mb("facepalm", (1600, 1250), 560, float=True, look="viewer"), sfx=["tink@doorbell|30%", "pop@answers|80%"])
    T["s1.l31"] = B([0, 120, 1.0], [0, 120, 1.05], [actor("rec", "recluse", [0, 420], 0.9, {"mood": "calm"}),
                                                    lab("rl", "BROWN RECLUSE", [0, 520], "recluses|60%", 64),
                                                    lab("q", "?", [420, -150], "recluses|70%", 200, YEL)],
                    sfx=["boing@recluses|70%"])
    T["s1.l32"] = S("ds_lab", [800, 680, 0.95], [820, 680, 1.0],
                    [actor("arena", "ds_arena", [560, 900], 1.4),
                     carol({"mood": "angry", "look": [1, 0.3]}, [420, 760], 0.24, idn="hero"),
                     actor("rec", "recluse", [690, 900], 0.32, {"mood": "worry"}, flip=True),
                     lab("sar", "SOUTH AMERICAN RECLUSE", [560, 470], "Brazil|25%", 46),
                     actor("scale", "ds_scale", [1350, 900], 0.7, {"tilt": 0.0, "label": "5x"},
                           sets=[{"at": "five|60%", "dur": 0.6, "p": {"tilt": 1.0}}])],
                    card_at="five|60%", sfx=["thud@five|60%"])
    T["s1.l33"] = S("ds_lab", [560, 760, 1.5], [580, 770, 1.6],
                    [actor("arena", "ds_arena", [560, 900], 1.4),
                     carol({"mood": "happy", "look": [-1, 0.3]}, [520, 760], 0.24, idn="hero",
                           moves=[{"at": "insects|60%", "dur": 0.6, "pos": [430, 780]}]),
                     actor("rec", "recluse", [690, 900], 0.32, {"mood": "calm"}, flip=True,
                           sets=[{"at": "insects|70%", "dur": 0.2, "p": {"mood": "angry"}}]),
                     actor("fly", "fly", [350, 800], 0.16, {"wrapped": 0.0}, sets=[{"at": "insects|70%", "dur": 0.5, "p": {"wrapped": 1.0}}]),
                     lab("huh", "!?", [700, 760], "insects|80%", 90, YEL)], sfx=["pop@insects|80%"], norecut=True)
    T["s1.l34"] = B([0, 60, 1.0], [0, 60, 1.03], [actor("map", "ds_map", [-520, 60], 0.85, {"place": "KANSAS", "pin": 0.0},
                                                        sets=[{"at": "Kansas|20%", "dur": 0.5, "p": {"pin": 1.0}}]),
                                                  actor("houses", "ds_houses", [420, -100], 0.55, {"n": 50, "cols": 10, "lit": 0.0}),
                                                  lab("fifty", "50 HOUSES", [420, 380], "fifty|70%", 60)],
                    sfx=["pop@Kansas|25%", "tink@fifty|70%"])
    T["s1.l35"] = B([0, 260, 1.0], [0, 260, 1.05], [actor("houses", "ds_houses", [0, 0], 0.9, {"n": 50, "cols": 10, "lit": 0.0},
                                                          sets=[{"at": "found|30%", "dur": 2.0, "p": {"lit": 0.68}}])],
                    sfx=["whoosh@found|30%"])
    T["s1.l36"] = B([0, 260, 0.92], [0, 260, 0.96], [actor("houses", "ds_houses", [0, 0], 0.9, {"n": 50, "cols": 10, "lit": 0.68})],
                    no_card=True, stamp={"text": "NOT A CURE", "color": RED, "at": "limited|70%", "y": 520, "px": 150},
                    sfx=["stamp@limited|70%"])
    T["s1.l37"] = C([720, 580, 1.6], [720, 590, 1.7], carol={"mood": "smug", "look": [0, 0.2]},
                    carol_sets=[{"at": "bonus|60%", "dur": 0.3, "p": {"shrug": 1.0}}], shoe=False, sfx=["boing@bonus|60%"])
    T["s1.l38"] = C([800, 560, 1.0], [800, 550, 1.06], carol={"mood": "happy", "look": [0.6, 0.6]},
                    extras=[giant("giant", (1080, 950), 0.45, {"wrapped": 1.0, "mood": "shock"}), tagc()],
                    sfx=["tink@answered|40%"])
    T["s1.l39"] = C([720, 470, 1.3], [720, 450, 1.38], carol={"mood": "worry", "look": [-0.6, -0.4]},
                    shoe_sets=[{"at": "heard|40%", "dur": 1.0, "p": {"nudge": 0.6}}],
                    extras=[actor("wh", "ds_whisper", list(CAROL), 0.8, {"on": 0.0}, sets=pop("other|55%"))], sfx=["whoosh@other|55%"])
    # ------------------------------------------------------------------------------------------ question 2
    T["s2.l0"] = C([620, 520, 1.25], [640, 520, 1.3], chapter=True, carol={"mood": "worry"}, shoe_nudge=0.6)
    T["s2.l1"] = C([720, 520, 1.45], [720, 520, 1.55], carol={"mood": "shock", "look": [0.6, -0.6]},
                   extras=[actor("bub", "ds_bubble", [800, 470], 0.75, {"on": 0.0, "kind": "skull"}, sets=pop("deadliest|35%", 0.4), front=True)],
                   card_at="rumor|15%", sfx=["boing@deadliest|35%"])
    T["s2.l2"] = C([860, 520, 1.05], [880, 520, 1.1], carol={"mood": "worry", "look": [1, -0.2]},
                   mb=MBF("present", (1240, 930), 470, look="viewer"),
                   extras=[prop("shoe2", "shoe", [1370, 650], 1.0, {"k": 0.45, "rot": -0.4}, at="shoe|60%", front=True)],
                   sfx=["pop@shoe|60%"])
    T["s2.l7"] = copy.deepcopy(T["s2.l6"])
    T["s2.l7"].update(cam=[700, 760, 0.98], to=[700, 760, 1.03], sfx=["boing@agree|45%"])
    acts = [a for a in T["s2.l7"]["actors"] if not a["id"].startswith("lab")]
    for a in acts:
        if a["id"] in ("lineup", "mask"):
            a["p"]["lit"] = [1, 1, 1]
            a.pop("set", None)
    acts += [actor("ar1", "ds_arrow", [250, 900], 1.0, {"to": [330, -40], "grow": 0.0}, sets=[{"at": "rumor|25%", "dur": 0.4, "p": {"grow": 1.0}}], front=True),
             actor("ar2", "ds_arrow", [820, 870], 1.0, {"to": [330, -120], "grow": 0.0}, sets=[{"at": "agree|50%", "dur": 0.4, "p": {"grow": 1.0}}], front=True),
             actor("ar3", "ds_arrow", [1150, 980], 1.0, {"to": [-900, 20], "grow": 0.0, "color": "#ff9f1c"}, sets=[{"at": "animal|80%", "dur": 0.4, "p": {"grow": 1.0}}], front=True)]
    T["s2.l7"]["actors"] = acts
    T["s2.l8"] = copy.deepcopy(T["s2.l7"])
    T["s2.l8"]["actors"] = [a for a in T["s2.l8"]["actors"] if not a["id"].startswith("ar")] + \
        [prop("cm", "comment", [1620, 360], 1.0, at="comments|30%", front=True)]
    T["s2.l8"].update(cam=[880, 760, 0.9], to=[900, 760, 0.94], mb=mb("subpoint", (1730, 1330), 640, look="viewer"), sfx=["pop@comments|30%"])
    T["s2.l9"] = B([0, 60, 1.0], [0, 60, 1.04], [actor("rumor", "ds_rumor", [0, 120], 1.0, {"crack": 0.0})], no_card=True,
                   stamp={"text": "URBAN LEGEND", "color": RED, "at": "legend|75%", "y": 560, "px": 150}, sfx=["stamp@legend|75%"])
    T["s2.l10"] = C([800, 620, 1.5], [800, 620, 1.58], carol={"mood": "smug", "look": [1, 0.4]}, shoe=False,
                    extras=[prop("bottle", "bottle", [990, 860], 0.9, {"label": "REGULAR"}, at="venom|20%")], sfx=["pop@venom|20%"])
    T["s2.l11"] = B([0, 60, 1.0], [0, 60, 1.05], [actor("globe", "ds_globe", [0, 100], 1.15, {"rot": 0.0, "hi": "AUSTRALIA", "pin": 0.0},
                                                         sets=[{"at": 0.1, "dur": 2.0, "p": {"rot": 135.0}}, {"at": "Australian|55%", "dur": 0.5, "p": {"pin": 1.0}}])],
                    sfx=["whoosh@0.1", "pop@Australian|60%"])
    T["s2.l12"] = S("ds_wall", [950, 640, 0.95], [960, 640, 1.0],
                    [actor("rb", "redback", [900, 950], 0.45, {"wrapped": 0.6, "mood": "shock"}),
                     lab("rbl", "REDBACK", [900, 1060], "redbacks|20%", 54),
                     carol({"mood": "smug", "look": [0.4, 0.8]}, [760, 520], 0.45, idn="hero"),
                     actor("bub", "ds_bubble", [1400, 680], 0.85, {"on": 0.0, "text": "SUPER VENOM?", "px": 60}, sets=pop("worse|65%", 0.4), front=True)],
                    mb=mb("shock", (1450, 1250), 520, float=True, look="hero"), sfx=["boing@worse|65%"])
    T["s2.l13"] = C([860, 760, 1.45], [880, 770, 1.55], carol_pos=[560, 600], norecut=True,
                    carol={"flick": 0.0, "flick_to": [(980 - 560) / CS, (760 - 600) / CS], "mood": "smug", "look": [1, 0.4]},
                    carol_sets=[{"at": "wraps|50%", "dur": 0.2, "p": {"flick": 1.0}}],
                    extras=[actor("rb", "redback", [990, 900], 0.4, {"wrapped": 0.5, "mood": "shock"},
                                  sets=[{"at": "wraps|50%", "dur": 1.0, "p": {"wrapped": 1.0}}])], sfx=["whoosh@wraps|50%"])
    T["s2.l14"] = S("ds_lab", [800, 700, 0.95], [820, 700, 1.02],
                    [prop("bottle", "bottle", [560, 900], 1.4, {"label": "VENOM"}), actor("arena", "ds_arena", [140, 900], 0.9),
                     carol({"mood": "worry"}, [140, 800], 0.18, idn="hero")],
                    mb=mb("think", (1150, 900), 600, look="viewer", prop="magnifier"), card_at="2019|25%", sfx=["tink@2019|25%"])
    T["s2.l15"] = S("ds_lab", [700, 760, 1.25], [720, 760, 1.3],
                    [prop("cricket", "cricket", [560, 900], 1.0, moves=[{"at": "crickets|20%", "dur": 0.5, "pos": [760, 900], "hop": 260}]),
                     lab("par", "PARALYSIS", [760, 560], "Paralysis|70%", 70, YEL)],
                    sfx=["boing@crickets|20%", "zap@Paralysis|70%"])
    T["s2.l16"] = S("ds_lab", [900, 740, 1.05], [900, 720, 1.1], [prop("bottle", "bottle", [600, 900], 1.0, {"label": "VENOM"})],
                    mb=mb("think", (1150, 900), 640, look="viewer", gest=[["deadly|60%", "laugh", 1.5]]), card_at="deadly|55%",
                    sfx=["pop@deadly|60%"])
    T["s2.l17"] = C([720, 540, 1.45], [720, 540, 1.5], carol={"mood": "happy"},
                    extras=[actor("bub", "ds_bubble", [800, 470], 0.75, {"on": 1.0, "kind": "skull", "pop": 0.0},
                                  sets=[{"at": "rumor|60%", "dur": 0.35, "p": {"pop": 1.0}}], front=True)], sfx=["pop@rumor|60%"])
    T["s2.l18"] = B([0, 100, 1.0], [0, 100, 1.05], [actor("fangs", "ds_fangs", [0, 300], 1.0, {"dip": 0.0},
                                                          sets=[{"at": "skin|55%", "dur": 0.6, "p": {"dip": 1.0}}]),
                                                    lab("fl", "FANGS", [-420, -150], "fangs|15%", 64, YEL)],
                    sfx=["tink@fangs|15%", "thud@skin|60%"])
    T["s2.l19"] = B([300, 100, 1.0], [320, 100, 1.04], [
        actor("box", "ds_arena", [300, 330], 2.0), actor("arm", "arm", [380, 160], 0.75, {"burn": 0.0}),
        carol({"mood": "angry", "still": True}, [430, -60], 0.17, idn="hero"),
        prop("tv", "tv", [1250, 160], 2.2, at="TV|15%"), lab("tvl", "ON CAMERA", [1250, -230], "camera|80%", 54)],
        sfx=["pop@TV|15%", "click@camera|80%"])
    T["s2.l20"] = S("bedroom", [900, 1100, 1.0], [900, 1080, 1.08], [lab("ow", "ow", [1060, 760], "sting|40%", 70, "#ffffff")],
                    scene_p={"time": "night"},
                    mb=mb("shock", (900, 1500), 900, look="viewer", gest=[["faded|70%", "shrug", 1.4]]), sfx=["pop@sting|40%"])
    T["s2.l21"] = B([0, 120, 1.0], [-60, 60, 1.35], [prop("fist", "fist", [0, 380], 1.6, {"dot": 0.0}, sets=[{"at": "sore|45%", "dur": 0.3, "p": {"dot": 1.0}}]),
                                                    prop("ruler", "ruler", [-40, 40], 0.9),
                                                    actor("ring", "ds_ring", [-104, 108], 1.0, {"on": 0.0, "r": 40}, sets=pop("sore|50%"), front=True)],
                    card_at="millimeter|65%", sfx=["tink@sore|50%"])
    T["s2.l22"] = B([0, 60, 1.0], [0, 100, 0.95], [actor("rumor", "ds_rumor", [0, 120], 1.0, {"crack": 0.0},
                                                         sets=[{"at": "fails|20%", "dur": 2.4, "p": {"crack": 1.0}}])],
                    sfx=["crunch@fails|20%", "thud@bite|85%"])
    T["s2.l23"] = C([700, 470, 1.0], [700, 480, 1.05], carol={"mood": "happy"},
                    extras=[chip("ps", "PENN STATE EXTENSION", [340, 470], "Penn|10%")], sfx=["pop@Penn|10%"])
    T["s2.l24"] = S("study", [700, 1050, 0.85], [720, 1040, 0.9], [chip("ucr", "UC RIVERSIDE", [700, 560], "Riverside|35%")],
                    scene_p={"time": "night"}, mb=mb("think", (700, 1500), 900, look="viewer", prop="paper"), sfx=["pop@Riverside|35%"])
    T["s2.l25"] = C([780, 500, 1.1], [780, 500, 1.16], carol={"mood": "happy", "look": [0.6, 0.2]},
                    carol_sets=[{"at": "mild|70%", "dur": 0.3, "p": {"wave": 1.0}}], mb=MBF("point", (1230, 900), 470),
                    sfx=["tink@Barely|40%"])
    T["s2.l26"] = S("bedroom", [700, 1050, 0.85], [720, 1040, 0.9],
                    [prop("lump", "lump", [1050, 1200], 1.1), prop("lamp", "lamp_blaze", [-20, 1150], 1.0),
                     prop("bill", "bill", [700, 560], 1.0, at="electric|60%")],
                    scene_p={"time": "night"}, sfx=["pop@electric|60%"])
    # ------------------------------------------------------------------------------------------ question 3
    T["s3.l0"] = C([700, 470, 1.0], [700, 480, 1.05], carol={"mood": "happy"}, meter_big_to=1.0, meter_big_at="Meter|5%",
                   meter_big_back="winning|85%", sfx=["tink@Meter|5%"])
    T["s3.l1"] = C([720, 380, 1.3], [720, 360, 1.38], carol={"mood": "worry", "look": [0.2, -1]},
                   shoe_sets=[{"at": "shoe|50%", "dur": 0.4, "p": {"spot": 1.0}}, {"at": "good|80%", "dur": 0.3, "p": {"tie": 1.0}}],
                   sfx=["zap@shoe|50%", "pop@good|80%"])
    T["s3.l2"] = C([720, 600, 1.6], [720, 600, 1.7], chapter=True, carol={"mood": "calm", "work": 0.5})
    T["s3.l3"] = C([700, 470, 1.0], [700, 470, 1.06], carol={"mood": "smug"},
                   extras=[tagc("t1", [480, 650], "More|10%"), tagc("t2", [960, 560], "Carols|40%"), tagc("t3", [300, 420], "Carols|65%"),
                           tagc("t4", [1150, 380], "Carols|85%")], sfx=["pop@More|10%", "pop@Carols|65%"])
    T["s3.l5"] = C([724, 650, 3.0], [724, 650, 3.4], carol={"eggs": 1.0, "mood": "happy", "look": [0, 0.8], "still": True},
                   shoe=False, card_y=150, card_at="dozen|30%", sfx=["tink@dozen|30%"])
    T["s3.l6"] = C([800, 560, 1.15], [800, 560, 1.2], carol={"eggs": 1.0, "mood": "calm", "look": [1, 0]},
                   carol_sets=[{"at": "parks|25%", "dur": 0.3, "p": {"eggs": 0.0}}, {"at": "picks|75%", "dur": 0.3, "p": {"eggs": 1.0}}],
                   extras=[actor("bund", "ds_bundle", [930, 470], 0.7, {"on": 0.0, "len": 110},
                                 sets=[{"at": "parks|25%", "dur": 0.3, "p": {"on": 1.0}}, {"at": "picks|75%", "dur": 0.3, "p": {"on": 0.0}}]),
                           actor("fly", "fly", [1500, 300], 0.28, {"wrapped": 0.0}, moves=[{"at": "eats|45%", "dur": 0.4, "pos": [1050, 620]}],
                                 sets=[{"at": "eats|55%", "dur": 0.4, "p": {"wrapped": 1.0}}])],
                   sfx=["pop@parks|25%", "crunch@eats|55%"])
    T["s3.l7"] = S("ds_lab", [700, 640, 1.0], [700, 640, 1.05],
                   [prop("shelf", "bundles", [700, 640], 1.0, {"n": 2.0}, sets=[{"at": "two|45%", "dur": 1.6, "p": {"n": 8.0}}]),
                    lab("tok", "TOKYO", [700, 300], "Tokyo|15%", 64)], sfx=["tink@two|45%", "tink@eight|85%"])
    T["s3.l8"] = B([0, 60, 1.0], [0, 60, 1.04], [prop("cal", "calendar", [-450, 120], 1.2, {"day": 1.0, "unit": "WEEK"},
                                                       sets=[{"at": "Two|10%", "dur": 1.4, "p": {"day": 3.0}}]),
                                                 actor("eggs", "ds_bundle", [350, -330], 2.0, {"len": 150, "burst": 0.0},
                                                       sets=[{"at": "hatch|70%", "dur": 0.8, "p": {"burst": 1.0}}])],
                   sfx=["tink@weeks|40%", "pop@hatch|70%"])
    T["s3.l9"] = C([700, 380, 0.95], [700, 360, 1.0], carol={"mood": "happy", "look": [0, -0.5]},
                   extras=[actor("babies", "ds_babies", [700, 230], 1.0, {"u": 0.0, "n": 16},
                                 sets=[{"at": "go|50%", "dur": 1.8, "p": {"u": 1.0}}])], sfx=["whoosh@go|50%"])
    T["s3.l10"] = S("bedroom", [800, 900, 0.62], [800, 880, 0.66],
                    [actor(f"w{k}", "ds_web", [x, y], 0.32, {"w": 600, "h": 700, "seed": k + 3, "spread": 0.0},
                           sets=[{"at": f"{20 + k * 18}%", "dur": 0.5, "p": {"spread": 1.0}}]) for k, (x, y) in
                     enumerate(((-480, 60), (300, 60), (1300, 60), (2080, 60)))], scene_p={"time": "night"},
                    sfx=["pop@20%", "pop@56%"])
    T["s3.l11"] = S("ds_wall", [900, 650, 1.0], [900, 660, 1.06],
                    [prop("chart", "growth", [1150, 1100], 1.1, {"g": 0.15}, sets=[{"at": "months|35%", "dur": 1.6, "p": {"g": 0.95}}]),
                     carol({"mood": "happy", "still": True}, [820, 800], 0.12, idn="hero",
                           moves=[{"at": "months|35%", "dur": 1.6, "s": 0.4, "pos": [820, 560]}])],
                    sfx=["boing@year|80%"])
    T["s3.l12"] = C([720, 560, 1.55], [720, 560, 1.65], carol={"mood": "happy", "look": [0, 0.2]},
                    carol_sets=[{"at": "year|30%", "dur": 0.3, "p": {"hat": 1.0}}, {"at": "two|85%", "dur": 0.3, "p": {"hat2": 1.0}}],
                    sfx=["pop@year|30%", "pop@two|85%"])
    T["s3.l13"] = C([700, 500, 0.62], [700, 500, 0.58], carol={"mood": "worry"}, web={"dust": 0.6},
                    extras=[actor(f"dw{k}", "ds_web", [x, y], 0.6, {"dust": 0.8, "seed": 10 + k}) for k, (x, y) in
                            enumerate(((-600, -90), (1900, -40), (100, 900)))], sfx=["whoosh@0.05"])
    T["s3.l14"] = B([0, 60, 1.0], [0, 60, 1.03], [actor("orb", "ds_orb", [-470, 120], 0.85, {"r": 380}),
                                                  actor("tangle", "ds_web", [470, -230], 0.62, {"w": 720, "h": 820, "a": 1.0}),
                                                  lab("l1", "NEAT WHEEL", [-470, -330], "neat|25%", 60),
                                                  lab("l2", "TANGLE", [470, -330], "tangle|75%", 60, YEL),
                                                  actor("x", "ds_cross", [-470, 120], 1.0, {"on": 0.0, "r": 120},
                                                        sets=[{"at": "not|15%", "dur": 0.3, "p": {"on": 1.0}}], front=True)],
                    sfx=["pop@neat|25%", "pop@tangle|75%"])
    T["s3.l15"] = C([700, 380, 1.5], [700, 390, 1.6], carol={"mood": "worry"}, web={"dust": 0.0},
                    shots=None, carol_sets=[], sfx=["whoosh@builds|20%"])
    T["s3.l15"]["web_sets"] = [{"at": "builds|15%", "dur": 2.0, "p": {"dust": 1.0}}]
    T["s3.l16"] = C([700, 470, 0.95], [700, 470, 1.0], carol={"mood": "worry"}, web={"w": 900, "h": 700},
                    extras=[prop("towel", "towel", [720, 520], 1.15, at="towel|65%", front=True)], sfx=["tink@towel|65%"])
    T["s3.l17"] = B([0, 120, 1.0], [0, 120, 1.04], [actor("bld", "ds_building", [-150, 520], 0.72, {"webs": 0.0},
                                                          sets=[{"at": "colonies|40%", "dur": 2.0, "p": {"webs": 1.0}}]),
                                                    lab("fin", "FINLAND", [-150, -310], "Finland|25%", 60),
                                                    prop("cal", "calendar", [620, 230], 0.9, {"day": 1.0, "unit": "YEAR"},
                                                         sets=[{"at": "ten|70%", "dur": 1.0, "p": {"day": 10.0}}])],
                    color="#22304a", card_x=1350, card_w=700, sfx=["pop@Finland|25%", "whoosh@ten|70%"])
    T["s3.l18"] = C([700, 430, 0.9], [700, 420, 0.95], carol={"mood": "smug"}, shoe_nudge=1.0,
                    extras=[actor("babies", "ds_babies", [700, 230], 1.4, {"u": 1.0, "n": 20})] +
                    [tagc(f"t{k}", [x, y]) for k, (x, y) in enumerate(((300, 420), (480, 650), (960, 560), (1150, 380), (1350, 620), (100, 600)))],
                    sfx=["thud@ceiling|70%"])
    T["s3.l19"] = C([720, 470, 1.15], [720, 460, 1.22], carol={"mood": "shock", "look": [0, -1]}, shoe_nudge=1.0,
                    meter_big_to=0.7, meter_big_at="meter|25%", meter_big_back="front|90%", sfx=["zap@meter|25%"])
    T["s3.l20"] = S("ds_court", [600, 800, 0.8], [620, 780, 0.86],
                    [actor("sheet", "ds_sheet", [550, 250], 1.0, {"unroll": 0.0, "line": ""},
                           sets=[{"at": "charge|40%", "dur": 1.0, "p": {"unroll": 1.0}}])],
                    mb=mb("present", (1350, 1500), 800, look="viewer"), sfx=["whoosh@charge|40%"])
    T["s3.l21"] = S("ds_court", [550, 560, 1.15], [550, 560, 1.2],
                    [actor("sheet", "ds_sheet", [550, 250], 1.0, {"unroll": 1.0, "line": ""},
                           sets=[{"at": "Messy|75%", "p": {"line": "1. COBWEBS"}}]),
                     chip("uc", "UC IPM", [550, 1000], "California|15%")], sfx=["stamp@Messy|75%"])
    T["s3.l22"] = S("ds_court", [800, 800, 0.95], [820, 790, 1.0],
                    [actor("sheet", "ds_sheet", [550, 250], 1.0, {"unroll": 1.0, "line": "1. COBWEBS", "small": 1.0})],
                    mb=mb("think", (1150, 1500), 760, look="hero", prop="magnifier", gest=[["charge|70%", "shrug", 1.4]]),
                    sfx=["tink@main|40%"])
    T["s3.l23"] = C([760, 520, 1.15], [760, 520, 1.2], carol={"mood": "happy", "look": [0, 0.3]}, shoe=True,
                    extras=[chip("ky", "KENTUCKY: HARMLESS", [380, 380], "harmless|35%"),
                            chip("ut", "UTAH STATE: BENEFICIAL", [1120, 760], "beneficial|85%")],
                    sfx=["stamp@harmless|35%", "stamp@beneficial|85%"])
    T["s3.l24"] = S("bedroom", [1100, 1050, 0.8], [1100, 1040, 0.84],
                    [prop("vac", "vacuum", [2500, 1500], 1.0, moves=[{"at": "tool|50%", "dur": 0.5, "pos": [1800, 1500]},
                                                                      {"at": "get|85%", "dur": 0.4, "pos": [2500, 1500]}])],
                    scene_p={"time": "night"}, mb=mb("deadpan", (900, 1500), 860, look="viewer", gest=[["tool|55%", "point", 1.0]]),
                    sfx=["whoosh@tool|50%"])
    T["s3.l25"] = C([760, 560, 1.1], [760, 560, 1.18], carol={"mood": "worry", "look": [1, 0.6]}, tint=DARK,
                    extras=[actor("eyes", "ds_eyes", [1250, 860], 0.8, {"on": 0.0}, sets=[{"at": "safe|60%", "dur": 0.4, "p": {"on": 1.0}}])],
                    sfx=["thud@safe|60%"])
    T["s3.l26"] = C([800, 600, 1.05], [800, 600, 1.12], carol={"mood": "shock", "look": [1, 0.5]},
                    extras=[actor("js", "js_front", [1700, 1010], 0.32, {"mood": "smug", "look": [-0.6, -0.2]},
                                  moves=[{"at": "jumping|25%", "dur": 0.8, "pos": [1250, 990], "walk": True}]),
                            lab("jsl", "JUMPING SPIDER", [1250, 1080], "jumping|40%", 50)], sfx=["step@jumping|30%"])
    T["s3.l27"]["extras"] = [actor("js", "js_front", [1250, 990], 0.32, {"mood": "smug", "look": [-0.6, -0.2], "crouch": 0.5})]
    T["s3.l28"] = C([860, 600, 1.25], [880, 600, 1.32], carol={"mood": "calm"},
                    carol_sets=[{"at": "whirls|65%", "dur": 0.3, "p": {"whirl": 1.0}}],
                    mb=MBF("point", (1180, 900), 480, gest=[["Touch|40%", "point", 1.0]]), sfx=["tink@Touch|45%", "whoosh@whirls|65%"])
    shim = []
    for k, q in enumerate((60, 68, 76, 84, 92)):
        shim += [{"at": f"{q}%", "dur": 0.1, "p": {"whirl": 0.35}}, {"at": f"{q + 3}%", "dur": 0.1, "p": {"whirl": 0.0}}]
    T["s3.l29"] = C([700, 560, 0.95], [700, 560, 1.0], carol={"mood": "calm"},
                    carol_sets=[{"at": "jumping|8%", "dur": 0.2, "p": {"whirl": 1.0}}, {"at": "Hunters|52%", "dur": 0.2, "p": {"whirl": 0.0}}] + shim,
                    extras=[actor("js", "js_front", [1250, 990], 0.3, {"mood": "smug"},
                                  moves=[{"at": "Hunters|50%", "dur": 0.5, "pos": [1900, 990]}]),
                            actor("par", "ds_parade", [700, 920], 1.0, {"u": 0.0}, sets=[{"at": "Hunters|52%", "dur": 2.6, "p": {"u": 1.0}}])],
                    sfx=["whoosh@jumping|8%", "step@Hunters|55%"])
    T["s3.l30"] = B([0, 100, 1.0], [0, 100, 1.06], [actor("js", "js_front", [0, 420], 0.85, {"mood": "worry", "look": [1, 0]},
                                                           sets=[{"at": f"{q}%", "p": {"look": lk}} for q, lk in
                                                                 ((15, [0, 1]), (25, [-1, 0]), (35, [0, -1]), (45, [1, 0]), (55, [0, 1]), (65, [-1, 0]))],
                                                           moves=[{"at": "onto|80%", "dur": 0.6, "pos": [1500, 420], "walk": True}])],
                    sfx=["boing@blur|30%", "step@onto|80%"])
    T["s3.l31"] = C([720, 560, 1.25], [720, 580, 1.4], carol={"mood": "worry", "still": True}, tint=[0.02, 0.02, 0.08, 0.5],
                    sfx=["thud@win|70%"])
    T["s3.l32"] = B([0, 60, 1.0], [0, 60, 1.03], [actor("ar", "ds_arenas", [0, 30], 1.0, {"grey": 0.0}),
                                                  lab("fwl", "NOBLE FALSE WIDOW", [0, -330], "widows|70%", 60, YEL)],
                    sfx=["pop@ten|35%", "pop@widows|75%"])
    T["s3.l33"] = B([0, 60, 0.96], [0, 60, 0.99], [actor("ar", "ds_arenas", [0, 30], 1.0, {"grey": 0.0},
                                                         sets=[{"at": "Seven|5%", "dur": 2.4, "p": {"grey": 7.0}}])],
                    card_at="dead|50%", sfx=["thud@Seven|10%", "thud@dead|50%"])
    T["s3.l34"] = B([0, 60, 1.0], [0, 60, 1.03], [
        actor("map", "ds_map", [-560, 60], 0.75, {"place": "CALIFORNIA", "pin": 0.0}, sets=[{"at": "California|10%", "dur": 0.5, "p": {"pin": 1.0}}]),
        carol({"mood": "worry", "look": [-1, 0], "thread": 400}, [620, -60], 0.32, idn="hero",
              moves=[{"at": "pushed|65%", "dur": 0.7, "pos": [1300, -60]}]),
        carol({"mood": "smug", "look": [1, 0], "marbled": 1.0, "thread": 400}, [150, -60], 0.36, idn="marbled",
              moves=[{"at": "pushed|65%", "dur": 0.7, "pos": [560, -60]}]),
        lab("ml", "MARBLED CELLAR SPIDER", [300, 330], "marbled|45%", 52)],
        sfx=["pop@California|10%", "whoosh@pushed|65%"])
    T["s3.l35"] = C([700, 700, 0.5], [700, 680, 0.55], carol={"mood": "worry", "still": True}, tint=[0.02, 0.02, 0.08, 0.45],
                    shoe=False, sfx=["thud@neighborhood|80%"])
    T["s3.l36"] = S("ds_house_ext", [500, 900, 2.2], [550, 950, 0.62], [], norecut=True, sfx=["whoosh@0.1"])
    T["s3.l37"] = S("cave", [560, 780, 0.85], [580, 800, 0.92],
                    [actor("cw1", "ds_web", [180, 330], 0.45, {"seed": 4}), actor("cw2", "ds_web", [880, 470], 0.4, {"seed": 6}),
                     carol({"mood": "happy", "still": True}, [210, 620], 0.3, idn="hero")], scene_p={"time": "day"},
                    sfx=["whoosh@wild|15%"])
    T["s3.l38"] = B([0, 60, 1.0], [0, 60, 1.04], [
        actor("globe", "ds_globe", [0, 160], 1.0, {"rot": 0.0}, sets=[{"at": 0.1, "dur": 3.0, "p": {"rot": 220.0}}]),
        prop("sc1", "suitcase", [-500, -100], 0.8, moves=[{"at": "carried|40%", "dur": 0.6, "pos": [0, -260], "hop": 180},
                                                         {"at": "around|70%", "dur": 0.6, "pos": [500, -100], "hop": 180}]),
        carol({"mood": "happy", "still": True}, [-500, -230], 0.14, idn="hero",
              moves=[{"at": "carried|40%", "dur": 0.6, "pos": [0, -390], "hop": 180}, {"at": "around|70%", "dur": 0.6, "pos": [500, -230], "hop": 180}])],
        sfx=["boing@carried|40%", "boing@around|70%"])
    T["s3.l39"] = S("basement", [600, 1000, 0.85], [620, 1000, 0.9],
                    [prop("boiler", "boiler", [950, 1500], 1.0), prop("win", "snowwin", [250, 600], 1.0),
                     carol({"mood": "happy", "still": True}, [760, 820], 0.3, idn="hero"),
                     lab("cel", "CELLAR", [600, 260], "cellar|80%", 70, YEL)], scene_p={"time": "night"}, sfx=["pop@cellar|80%"])
    rads = [(-300, 300), (-280, 170), (-330, 40), (-300, -90), (-350, -200)]
    T["s3.l40"] = B([0, 60, 1.0], [0, 60, 1.03], [actor("map", "ds_map", [-300, 60], 0.95, {"place": "BRITAIN", "pin": 0.0})] +
                    [prop(f"r{k}", "radiator", [x + 0, y + 60], 0.16, at=f"{30 + k * 12}%") for k, (x, y) in enumerate(rads)] +
                    [lab("ch", "CENTRAL HEATING", [520, 60], "heating|80%", 64, YEL)], sfx=["pop@north|30%", "tink@heating|80%"])
    T["s3.l41"] = S("ds_wall", [800, 720, 1.0], [800, 720, 1.08],
                    [prop("rad", "radiator", [800, 1080], 1.2), carol({"mood": "happy", "shades": 1.0, "still": True}, [800, 560], 0.45, idn="hero")],
                    sfx=["tink@climate|60%"])
    T["s3.l42"] = S("kitchen", [800, 1050, 0.82], [820, 1040, 0.88],
                    [prop("door", "door", [1250, 1500], 1.0, {"open": 0.0}, sets=[{"at": "outside|25%", "dur": 0.5, "p": {"open": 1.0}},
                                                                                     {"at": "cold|75%", "dur": 0.4, "p": {"open": 0.0}}]),
                     prop("jar", "jar", [640, 1130], 0.45, front=True), carol({"mood": "worry", "still": True}, [640, 1030], 0.08, idn="hero", front=True),
                     lab("jan", "JANUARY", [1250, 560], "January|50%", 60)],
                    scene_p={"time": "night"}, mb=mb("think", (800, 1500), 860, look="viewer", gest=[["cold|75%", "shock", 1.0]]),
                    sfx=["whoosh@outside|25%", "thud@cold|78%"])
    # ------------------------------------------------------------------------------------------ the deal
    T["s4.l0"] = C([860, 520, 1.05], [860, 520, 1.1], carol={"mood": "calm", "look": [1, 0]},
                   mb=MBF("present", (1220, 880), 480, look="viewer"),
                   extras=[prop("con", "contract", [1360, 760], 0.55, at="deal|40%", front=True)], sfx=["pop@deal|40%"])
    T["s4.l1"] = C([720, 560, 1.4], [720, 560, 1.48], carol={"mood": "happy"}, web={"dust": 0.6},
                   carol_sets=[{"at": "spider|25%", "dur": 0.3, "p": {"wave": 1.0}}], card_at="Keep|10%", sfx=["tink@Lose|60%"])
    T["s4.l2"] = C([760, 560, 1.0], [760, 560, 1.05], carol={"mood": "happy", "look": [1, 0.6]},
                   extras=[actor("dusty", "ds_web", [1200, 520], 0.5, {"dust": 1.0, "seed": 21, "a": 0.9},
                                 sets=[{"at": "webs|35%", "dur": 0.8, "p": {"a": 0.0, "spread": 0.2}}]),
                           actor("sac", "ds_bundle", [1300, 460], 0.8, {"len": 120}, sets=[{"at": "egg|55%", "dur": 0.4, "p": {"on": 0.0}}]),
                           prop("noz", "nozzle", [1250, 1300], 1.0, {"suck": 1.0}, moves=[{"at": "vacuum|10%", "dur": 0.6, "pos": [1250, 780]}]),
                           chip("uk", "UNIVERSITY OF KENTUCKY", [380, 820], "Kentucky|70%")],
                   sfx=["whoosh@vacuum|10%", "pop@Kentucky|70%"])
    T["s4.l3"] = B([0, 60, 1.0], [0, 60, 1.03], [actor("cg", "ds_calgrid", [-220, 80], 0.95, {"u": 0.0},
                                                       sets=[{"at": "vacuum|40%", "dur": 2.0, "p": {"u": 1.0}}]),
                                                 chip("ia", "IOWA STATE", [600, -330], "Iowa|30%")], sfx=["pop@Iowa|30%"])
    T["s4.l4"] = B([0, 80, 1.0], [0, 80, 1.04], [prop("spray", "spray", [-350, 420], 1.1, {"x": 0.0}, sets=[{"at": "Skip|5%", "dur": 0.4, "p": {"x": 1.0}}]),
                                                 chip("ia", "IOWA STATE: WORKS POORLY", [430, -120], "Iowa|25%"),
                                                 chip("uc", "UC IPM: NOT NEEDED", [430, 160], "California|65%")],
                   sfx=["stamp@Skip|8%", "pop@California|65%"])
    T["s4.l5"] = S("kitchen", [700, 1000, 0.8], [720, 1000, 0.86],
                   [prop("caulk", "caulk", [560, 780], 0.6, moves=[{"at": "Seal|10%", "dur": 1.6, "pos": [880, 780]}]),
                    prop("box1", "box", [-100, 1500], 0.9, moves=[{"at": "clutter|45%", "dur": 0.6, "pos": [-900, 1500]}]),
                    prop("box2", "box", [-80, 1300], 0.7, moves=[{"at": "clutter|50%", "dur": 0.6, "pos": [-900, 1300]}])],
                   scene_p={"time": "night"}, mb=mb("point", (300, 1500), 800, look="viewer"), sfx=["scratch@Seal|10%", "whoosh@clutter|45%"])
    T["s4.l6"] = S("bedroom", [560, 980, 1.0], [600, 900, 0.95],
                   [carol({"mood": "calm", "still": True}, [380, 930], 0.22, idn="hero",
                          moves=[{"at": "carry|82%", "dur": 0.7, "pos": [1500, 200]}]),
                    prop("jar", "jar", [380, 600], 0.42, front=True,
                         moves=[{"at": "jar|40%", "dur": 0.4, "pos": [380, 1010]}, {"at": "carry|82%", "dur": 0.7, "pos": [1500, 280]}], rot=180),
                    prop("paper", "paper", [-200, 1010], 0.5, front=True,
                         moves=[{"at": "paper|58%", "dur": 0.4, "pos": [380, 1010]}, {"at": "carry|82%", "dur": 0.7, "pos": [1500, 280]}])],
                   scene_p={"time": "night"}, sfx=["thud@jar|42%", "scratch@paper|60%"])
    T["s4.l7"] = S("basement", [500, 1050, 0.85], [800, 1050, 0.85],
                   [prop("jar", "jar", [350, 1140], 0.35, front=True, moves=[{"at": 0.1, "dur": 2.0, "pos": [950, 1140], "walk": True}]),
                    carol({"mood": "happy", "still": True, "wave": 1.0}, [350, 1065], 0.07, idn="hero", front=True,
                          moves=[{"at": 0.1, "dur": 2.0, "pos": [950, 1065], "walk": True}])],
                   scene_p={"time": "night"},
                   mb=mb("present", (200, 1500), 760, look="viewer", moves=[{"at": 0.1, "dur": 2.0, "pos": [800, 1500], "walk": True}]),
                   sfx=["step@0.2", "step@basement|60%"])
    # ------------------------------------------------------------------------------------------ the verdict
    T["s5.l0"] = C([720, 520, 1.1], [720, 520, 1.14], carol={"mood": "worry"}, tint=DARK, meter_big_to=1.0, meter_big_at="Final|5%",
                   sfx=["thud@Final|5%"])
    T["s5.l1"] = C([820, 560, 1.0], [820, 560, 1.06], carol={"mood": "smug", "look": [0.6, 0.6]},
                   extras=[giant("giant", (1080, 950), 0.45, {"wrapped": 1.0, "mood": "shock"})],
                   three=["HUNTING?"], three_at=["hunting|10%"], sfx=["pop@hunting|10%"])
    T["s5.l2"] = B([0, 60, 1.0], [0, 60, 1.04], [actor("rumor", "ds_rumor", [-200, 160], 0.85, {"crack": 0.3})],
                   three=["HUNTING?", "HURT YOU?"], three_at=["0%", "hurt|10%"], sfx=["pop@hurt|10%"])
    T["s5.l3"] = C([760, 560, 1.0], [760, 560, 1.06], carol={"mood": "smug"},
                   carol_sets=[{"at": "bodyguard|65%", "dur": 0.3, "p": {"shades": 1.0}}],
                   extras=[prop("noz", "nozzle", [380, 1300], 0.9, {"suck": 0.0}, moves=[{"at": "vacuum|35%", "dur": 0.5, "pos": [380, 860]}])],
                   three=["HUNTING?", "HURT YOU?", "LEAVE IT?"], three_at=["0%", "0%", "leave|8%"], sfx=["pop@vacuum|35%", "boing@bodyguard|65%"])
    T["s5.l5"] = C([720, 560, 0.95], [720, 560, 1.0], carol={"mood": "smug", "look": [1, 0.8]}, shoe=False,
                   extras=[giant("giant", (1800, 1000), 0.55, moves=[{"at": "comes|50%", "dur": 1.2, "pos": [1100, 980], "walk": True}])],
                   sfx=["step@comes|55%"])
    T["s5.l6"] = C([860, 760, 1.4], [880, 770, 1.5], carol_pos=[560, 600], shoe=False, norecut=True,
                   carol={"flick": 0.0, "flick_to": [(1000 - 560) / CS, (720 - 600) / CS], "mood": "angry", "look": [1, 0.4]},
                   carol_sets=[{"at": "got|30%", "dur": 0.2, "p": {"flick": 1.0}}],
                   extras=[giant("giant", (1000, 900), 0.52, {"mood": "shock", "wrapped": 0.0}, sets=[{"at": "got|30%", "dur": 1.0, "p": {"wrapped": 0.6}}])],
                   sfx=["whoosh@got|30%"])
    T["s5.l7"] = S("bathroom", [560, 1250, 1.0], [560, 1250, 1.06],
                   [actor("hc", "ds_sil", [560, 1480], 0.75, {"kind": "house_centipede", "a": 0.88, "kp": {"walk": 0.6}},
                          moves=[{"at": 0.0, "dur": 2.5, "pos": [760, 1480], "walk": True}])],
                   scene_p={"time": "night"}, sfx=["scratch@thirty|25%"])
    T["s5.l8"] = S("bedroom", [700, 1050, 0.85], [720, 1040, 0.9], [], scene_p={"time": "night"},
                   mb=mb("subpoint", (800, 1500), 880, look="viewer", gest=[["eight|60%", "point", 1.0]]), sfx=["pop@Subscribe|5%"])
    # ------------------------------------------------------------------------------------------ run-breakers (contact sheet 1)
    T["s1.l4"] = C([720, 610, 2.3], [720, 600, 2.5], shoe=False, carol={"still": True, "mood": "calm", "look": [0, 0.3]},
                   carol_sets=[{"at": "waits|80%", "dur": 0.25, "p": {"look": [-0.8, 0.2]}}, {"at": "waits+0.5", "dur": 0.25, "p": {"look": [0.8, 0.2]}}],
                   sfx=["whoosh@0"])
    T["s1.l10"].update(cam=[-330, 260, 1.45], to=[-360, 270, 1.55])
    T["s1.l11"].update(cam=[330, 230, 1.6], to=[340, 230, 1.65])
    for a in T["s1.l11"]["actors"]:
        if a["id"] == "carolw":
            a.update(pos=[560, 60], s=0.24)
            a["p"]["thread"] = 500
        if a["id"] == "notes":
            a["pos"] = [640, 0]
    T["s1.l16"]["actors"][1]["moves"] = [{"at": 0.05, "dur": 2.2, "pos": [900, 620], "walk": True}]
    T["s1.l16"]["actors"][1]["pos"] = [900, -120]
    T["s1.l16"]["actors"][0]["moves"] = [{"at": 0.05, "dur": 2.2, "pos": [1130, 500]}]
    T["s1.l17"].update(cam=[720, 620, 1.55], to=[740, 640, 1.62], shoe=False)
    T["s1.l17"]["extras"] = [giant("giant", (1500, 1080), 0.95, moves=[{"at": 0, "dur": 2.0, "pos": [1300, 1060], "walk": True}])]
    T["s1.l22"].update(cam=[620, 660, 2.0], to=[640, 670, 2.1])
    T["s1.l23"].update(cam=[760, 780, 0.9], to=[780, 760, 0.98])
    T["s1.l24"]["actors"][0]["pos"] = [860, 1430]
    T["s1.l24"]["mb"].update(pos=[860, 1330], size=820)
    T["s1.l38"] = S("ds_wall", [800, 640, 1.0], [800, 640, 1.06],
                    [giant("giant", (1000, 960), 0.7, {"wrapped": 1.0, "mood": "shock"}),
                     carol({"mood": "happy", "look": [0.8, 0.6], "thread": 500}, [620, 440], 0.5, idn="hero")],
                    scene_p={"dark": True}, sfx=["tink@answered|40%"])
    T["s2.l0"] = S("ds_wall", [760, 560, 1.1], [760, 560, 1.15], [carol({"mood": "worry", "thread": 600}, [760, 520], 0.55, idn="hero")],
                   chapter=True)
    T["s2.l2"] = S("bedroom", [900, 1100, 1.0], [920, 1090, 1.06],
                   [prop("shoe2", "shoe", [1130, 900], 1.0, {"k": 0.55, "rot": -0.2}, at="shoe|55%", front=True)],
                   scene_p={"time": "night"}, mb=mb("present", (900, 1500), 900, look="viewer"), sfx=["pop@shoe|55%"])
    for sid, c0, to in (("s2.l4", [260, 760, 1.35], [240, 760, 1.42]), ("s2.l5", [700, 760, 1.35], [720, 760, 1.42]),
                        ("s2.l6", [1180, 720, 1.3], [700, 760, 0.98])):
        T[sid].update(cam=c0, to=to)
    for a in T["s2.l12"]["actors"]:
        if a["id"] == "rbl":
            a["pos"] = [1180, 860]
    T["s2.l16"] = S("study", [700, 1050, 0.9], [720, 1040, 0.95], [prop("bottle", "bottle", [1060, 1500], 1.0, {"label": "VENOM"})],
                    scene_p={"time": "night"}, mb=mb("think", (700, 1500), 900, look="viewer", gest=[["deadly|60%", "laugh", 1.5]]),
                    card_at="deadly|55%", sfx=["pop@deadly|60%"])
    T["s3.l0"] = B([0, 120, 1.0], [0, 120, 1.03], [carol({"mood": "happy", "thread": 600}, [-520, 120], 0.45, idn="hero")],
                   mb=mb("point", (420, 760), 600, float=True, look="viewer"), meter_big_to=1.0, meter_big_at="Meter|5%",
                   meter_big_back="winning|85%", sfx=["tink@Meter|5%"])
    T["s3.l2"] = S("ds_wall", [760, 560, 1.1], [760, 560, 1.15], [carol({"mood": "calm", "thread": 600, "eggs": 1.0}, [760, 520], 0.55, idn="hero")],
                   chapter=True)
    T["s3.l5"] = B([0, 60, 1.0], [0, 60, 1.06], [actor("eggs", "ds_bundle", [0, -400], 3.2, {"len": 160}),
                                                 actor("ring", "ds_ring", [0, 130], 1.0, {"on": 0.0, "r": 210}, sets=pop("dozen|30%"))],
                   card_y=150, card_at="dozen|30%", sfx=["tink@dozen|30%"])
    T["s3.l21"].update(cam=[550, 450, 1.6], to=[550, 450, 1.68])
    T["s3.l26"] = S("ds_wall", [760, 600, 1.0], [760, 600, 1.06],
                    [actor("js", "js_front", [1700, 1000], 0.6, {"mood": "smug", "look": [-1, -0.3]},
                           moves=[{"at": "jumping|20%", "dur": 0.9, "pos": [1050, 980], "walk": True}]),
                     lab("jsl", "JUMPING SPIDER", [1050, 380], "jumping|35%", 60, YEL),
                     carol({"mood": "shock", "thread": 500, "look": [1, 0.6]}, [420, 420], 0.4, idn="hero")],
                    scene_p={"dark": True}, sfx=["step@jumping|25%"])
    T["s3.l28"].update(cam=[1020, 700, 1.7], to=[1030, 700, 1.78])
    T["s3.l29"] = B([0, 100, 1.0], [0, 100, 1.03], [
        carol({"mood": "calm", "thread": 600}, [-200, -40], 0.45, idn="hero",
              sets=T["s3.l29"]["carol_sets"]),
        actor("js", "js_front", [650, 330], 0.4, {"mood": "smug"}, moves=[{"at": "Hunters|50%", "dur": 0.5, "pos": [1500, 330]}]),
        actor("par", "ds_parade", [0, 420], 1.0, {"u": 0.0}, sets=[{"at": "Hunters|52%", "dur": 2.6, "p": {"u": 1.0}}])],
        sfx=["whoosh@jumping|8%", "step@Hunters|55%"])
    T["s3.l41"]["actors"][0]["pos"] = [800, 1250]
    T["s3.l41"]["actors"][1]["pos"] = [800, 520]
    T["s4.l1"] = B([0, 100, 1.0], [0, 100, 1.04], [carol({"mood": "happy", "thread": 500}, [-420, 40], 0.5, idn="hero",
                                                         sets=[{"at": "spider|25%", "dur": 0.3, "p": {"wave": 1.0}}]),
                                                   actor("dusty", "ds_web", [420, -200], 0.55, {"dust": 1.0, "seed": 30}),
                                                   actor("x", "ds_cross", [420, 120], 1.0, {"on": 0.0, "r": 200},
                                                         sets=[{"at": "Lose|60%", "dur": 0.3, "p": {"on": 1.0}}], front=True)],
                   card_y=780, card_at="Keep|10%", sfx=["stamp@Lose|60%"])
    T["s5.l3"] = B([0, 100, 1.0], [0, 100, 1.04], [
        prop("vac", "vacuum", [-450, 560], 0.9, at="vacuum|35%"),
        carol({"mood": "smug", "thread": 500}, [150, 40], 0.5, idn="hero", sets=[{"at": "bodyguard|65%", "dur": 0.3, "p": {"shades": 1.0}}])],
        three=["HUNTING?", "HURT YOU?", "LEAVE IT?"], three_at=["0%", "0%", "leave|8%"], sfx=["pop@vacuum|35%", "boing@bodyguard|65%"])
    T["s5.l5"] = S("ds_floor", [700, 760, 1.0], [720, 750, 1.08],
                   [actor("shadow", "ds_shadow", [1900, 1000], 1.25, {"a": 0.62}, rot=-8,
                          moves=[{"at": "comes|40%", "dur": 1.6, "pos": [500, 860], "linear": True}])],
                   sfx=["thud@start|40%", "step@comes|60%"])
    return T
