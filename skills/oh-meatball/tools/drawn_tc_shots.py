"""The hand-made shots for the Christmas-tree long-form (tools/drawn_treecheck.py): spec line id -> recipe + args.
One entry per outline line (s<segment>.l<line>), drawn from that line's `vis` note. Word anchors fall back to a
share of the line ("word|40%"). World conventions: the living room floor is y = 900 with the tree at x = 960;
close-ups sit on tc_bokeh; boards on ds_board_bg are centred on (0, 0).

Format keys a shot may carry (read by drawn_treecheck.expand): chapter, meter_in, meter_at, meter_big_to/_at/_back,
chip_text, chip_at, stamps [{text, color, at, x, y, px, rot}], four (cold-open stamps), check_at, list_step,
tick_at, list_all, card_at, card_y, card_x, card_w, no_card, pad, flash, shake, sheet_at, norecut."""
import copy

from drawn_dontsquish import GREEN, RED, YEL, actor, cam, mb, pop

HID = {"hidden": True, "pose": "neutral", "pos": [-3000, 1500], "size": 600}
LR_TREE = [960, 905]
WIDE = [960, 560, 0.95]


def table():
    T = {}

    def S(scene, c0, to=None, actors=(), shots=None, scene_p=None, mbx=None, sfx=(), **kw):
        d = {"r": "scene", "scene": scene, "scene_p": scene_p or {}, "cam": c0,
             "to": to if to is not None else [c0[0], c0[1], round(c0[2] * 1.06, 3)], "actors": list(actors),
             "mb": mbx or HID, "sfx": list(sfx)}
        if shots:
            d["shots"] = shots
        d.update(kw)
        return d

    def A(idn, typ, pos, s=1.0, p=None, at=None, sets=None, moves=None, front=False, flip=False, rot=0.0, dur=0.3):
        pp = dict(p or {})
        st = list(sets or [])
        if at:
            pp["on"] = 0.0
            st = [{"at": at, "dur": dur, "p": {"on": 1.0}}] + st
        return actor(idn, typ, pos, s, pp, st or None, moves, front=front, flip=flip, rot=rot)

    def lab(idn, text, pos, at=None, px=56, color="#ffffff"):
        return A(idn, "ds_label", pos, 1.0, {"text": text, "px": px, "color": color}, at=at, front=True)

    def chip(idn, text, pos, at=None, px=48):
        return A(idn, "ds_chip_src", pos, 1.0, {"text": text, "px": px}, at=at, front=True)

    def prop(idn, kind, pos, s=1.0, p=None, at=None, sets=None, moves=None, front=False, rot=0.0):
        return A(idn, "tc_prop", pos, s, dict({"kind": kind}, **(p or {})), at=at, sets=sets, moves=moves, front=front,
                 rot=rot)

    def twig(pos, s=1.0, idn="twig", **p):
        return A(idn, "tc_twig", pos, s, p)

    def ooth(pos, s=1.0, idn="case", sets=None, moves=None, front=False, **p):
        return A(idn, "tc_ooth", pos, s, p, sets=sets, moves=moves, front=front)

    def tree(pos=None, s=0.7, idn="xtree", sets=None, **p):
        return A(idn, "tc_xtree", list(pos or LR_TREE), s, p, sets=sets)

    def stamp(text, at, x, y, color=GREEN, px=120, rot=-8):
        return {"text": text, "at": at, "x": x, "y": y, "color": color, "px": px, "rot": rot}

    def M(pose, pos, size=600, look="viewer", **kw):
        return mb(pose, tuple(pos), size, look=look, **kw)

    def mv(at, dur, pos, **kw):
        return dict({"at": at, "dur": dur, "pos": list(pos)}, **kw)

    def set_(at, dur=0.3, **p):
        return {"at": at, "dur": dur, "p": p}

    IGN = lambda at, x=560, y=330, px=110: stamp("IGNORE", at, x, y, GREEN, px)  # noqa: E731

    # =========================================================================================== 0. cold open
    T["s0.l0"] = S("tc_bokeh", [960, 560, 1.12], [960, 570, 1.2],
                   [twig([960, 720], 1.1), ooth([960, 720], 1.75, quiver=1.0),
                    A("ring", "ds_ring", [960, 560], 1.0, {"on": 0.0, "r": 250, "lw": 8}, sets=[set_("check|55%", 0.3, on=1.0)])],
                   card_at="check|55%", sfx=["sting@0.02", "thud@check|55%"], sheet_at=0.0)
    T["s0.l1"] = S("tc_bokeh", [960, 560, 1.0], [960, 560, 1.04],
                   [twig([700, 700], 0.9), ooth([620, 700], 1.45, quiver=0.4),
                    A("marsh", "tc_marsh", [2600, 560], 1.25, moves=[mv(0.05, 0.45, [1500, 560])])],
                   sfx=["whoosh@0.05", "pop@marshmallow|60%"])
    T["s0.l2"] = S("ds_board_bg", [0, 60, 1.0], [0, 60, 1.05],
                   [ooth([-330, 330], 2.2, xray=0.0, quiver=0.3, sets=[set_("Inside|5%", 0.5, xray=1.0)]),
                    A("cnt", "tc_counter", [480, -60], 1.0, {"v": 0.0, "px": 230},
                      sets=[set_("hundred|35%", 0.6, v=100.0), set_("several|70%", 0.0, text="100+")])],
                   scene_p={"color": "#1b1724"}, sfx=["whoosh@Inside|5%", "tink@hundred|35%"], norecut=True)
    T["s0.l3"] = S("tc_living", [760, 420, 1.25], [800, 430, 1.3],
                   [prop("thermo", "thermostat", [430, 330], 0.9, {"glow": 0.0, "dial": 0.2},
                         sets=[set_("warm|25%", 0.8, glow=1.0, dial=0.9)]),
                    twig([1420, 470], 0.85), ooth([1060, 470], 1.1, crack=0.0, quiver=0.6, sets=[set_("spring|55%", 0.5, crack=1.0)])],
                   scene_p={"fireplace": False}, tint=[1.0, 0.55, 0.15, 0.08], sfx=["tink@warm|25%", "crunch@spring|55%"])
    T["s0.l4"] = S("tc_living", [1110, 690, 2.6], None,
                   [tree(qmarks=0.0, sets=[set_("Nine|40%", 1.4, qmarks=1.0)]),
                    ooth([1105, 693], 0.22, front=True)],
                   shots=[cam([1110, 680, 2.6], [1110, 680, 2.7]), cam([1110, 680, 2.7], WIDE, at="stowaway|35%", dur=0.9)],
                   mbx=M("point", (1560, 900), 560, look="xtree", moves=[mv("Nine|40%", 0.4, (1500, 900), hop=60)]),
                   chip_text="9 STOWAWAYS", chip_at="Nine|45%", sfx=["whoosh@stowaway|35%", "pop@Nine|45%"])
    four = {"items": [["IGNORE", "x6", GREEN], ["VACUUM", "x1", YEL], ["CLIP", "x1", YEL], ["CHECK THE TRUNK", "x1", RED]],
            "at": ["Six|3%", "vacuum|30%", "clip|52%", "outside|75%"], "y": 640}
    T["s0.l5"] = S("ds_board_bg", [0, 0, 1.0], [0, 0, 1.03],
                   [A("sil1", "house_sp_small", [-700, -40], 0.5, at="Six|3%"),
                    A("sil1b", "tc_barkbeetle", [-560, -30], 0.42, at="Six|3%"),
                    A("vac", "tc_aphid", [-250, -40], 0.55, at="vacuum|30%"),
                    twig([150, -110], 0.3, idn="tw"), ooth([150, -110], 0.75, idn="c2", sets=[{"at": 0, "p": {"grow": 0.0}}, set_("clip|52%", 0.3, grow=1.0)]),
                    A("slf", "tc_slf_eggs", [630, -120], 0.8, at="outside|75%")],
                   scene_p={"color": "#1b1724"}, four=four, norecut=True)
    T["s0.l6"] = S("tc_living", WIDE, [960, 560, 1.02],
                   [tree(lit=1.0)],
                   mbx=M("neutral", (1480, 900), 600, look="viewer", gest=[["twenty|25%", "shock", 1.6], ["check|70%", "point", 1.2]]),
                   card_at="twenty|25%", card_y=170, meter_in="check|65%", shake=["twenty|25%"],
                   sfx=["thud@twenty|25%", "boing@thousand|45%"])
    # =========================================================================================== 1. the 25,000
    T["s1.l0"] = S("tc_cork", [800, 540, 1.0], [900, 520, 1.06],
                   [A("n25", "tc_note", [700, 560], 1.0, {"text": "25,000", "px": 170, "w": 700, "h": 300}),
                    A("str", "tc_string", [1000, 520], 1.0, {"to": [1300, -500], "grow": 0.0}, sets=[set_("Where|30%", 0.8, grow=1.0)], front=True)],
                   chapter=True, sfx=["tink@Where|30%"])
    T["s1.l1"] = S("tc_cork", [520, 540, 1.0], None,
                   [A("str", "tc_string", [-200, 300], 1.0, {"to": [1000, 160], "grow": 0.0}, sets=[set_("university|25%", 0.8, grow=1.0)], front=True),
                    A("map", "tc_map", [800, 520], 0.72, {"place": "NORWAY", "pin": 0.0, "px": -60, "py": 40}, sets=[set_("Norway|30%", 0.5, pin=1.0)]),
                    A("cal", "ds_prop", [1450, 540], 0.95, {"kind": "calendar", "label": "DEC 2012"}, at="December|55%"),
                    A("str2", "tc_string", [900, 400], 1.0, {"to": [450, 40], "grow": 0.0}, sets=[set_("December|50%", 0.5, grow=1.0)], front=True)],
                   shots=[cam([520, 540, 1.0], [800, 540, 1.0]), cam([800, 540, 1.0], [1120, 540, 1.0], at="December|45%", dur=0.7)],
                   sfx=["pop@Norway|30%", "pop@December|55%"])
    T["s1.l2"] = S("ds_lab", [900, 620, 0.95], [920, 600, 1.0],
                   [A("sci", "person", [520, 900], 0.62, {"body": "#f4f4f4", "glasses": "round", "hair": "#6b4a2f",
                                                         "mood": "calm", "arm": "point", "talk": 0.0}),
                    A("bub", "tc_speech", [1210, 380], 1.0, {"lines": ["AS MANY AS...", "IN SOME TREES"], "px": 78, "w": 800,
                                                             "h": 300, "under": 0.0},
                      at="said|20%", sets=[set_("some|75%", 0.5, under=1.0)])],
                   sfx=["pop@said|20%", "scratch@some|75%"])
    T["s1.l3"] = S("tc_snowwood", [960, 560, 0.95], [1000, 560, 1.0],
                   [A("spr", "tc_wild", [640, 920], 0.78, {"kind": "spruce"}), A("pine", "tc_wild", [1290, 920], 0.78, {"kind": "pine"}),
                    lab("l1", "SPRUCE", [640, 290], "Spruce|10%", 64), lab("l2", "PINE", [1290, 160], "pine|20%", 64)],
                   sfx=["pop@Spruce|10%", "pop@pine|20%"])
    xs = [560, 760, 960, 1160, 1360]
    words = ["Springtails|25%", "bark|42%", "mites|58%", "moth|72%", "spider|88%"]
    crit = [("tc_springtail", 0.42, {}), ("tc_barklouse", 0.42, {}), ("tc_mite", 0.32, {"egg": False}), ("sp.moth", 0.32, {}),
            ("house_sp_small", 0.3, {})]
    names = ["SPRINGTAIL", "BARK LOUSE", "MITE", "MOTH", "SPIDER"]
    acts = [twig([960, 720], 1.0)]
    for i, (x, w, (typ, sc, pp), nm) in enumerate(zip(xs, words, crit, names)):
        y = 690 if typ != "tc_mite" else 650
        acts.append(A(f"c{i}", typ, [x, y], sc, pp))
        acts.append(lab(f"n{i}", nm, [x, 470 if i % 2 == 0 else 400], w, 44, YEL))
    acts.append(A("lens", "tc_prop", [xs[0], 640], 0.62, {"kind": "lens"}, front=True,
                  moves=[mv(w, 0.3, (x, 640)) for x, w in zip(xs, words)]))
    T["s1.l4"] = S("tc_bokeh", [960, 580, 1.0], [960, 580, 1.04], acts, sfx=["tink@Springtails|25%", "tink@moth|72%"], norecut=True)
    T["s1.l5"] = S("tc_cork", [900, 640, 0.95], [920, 640, 1.0],
                   [prop("cab", "cabinet", [700, 1060], 1.05, {"open": 0.0}, sets=[set_("doesn't|10%", 0.5, open=1.0)]),
                    A("pp1", "ds_prop", [700, 380], 0.6, {"kind": "paper"}, at="counted|40%",
                      moves=[mv("counted|40%", 0.8, (420, 200))], rot=30)],
                   mbx=M("think", (1060, 1060), 640, look="viewer", gest=[["counted|35%", "shrug", 2.0], ["find|70%", "facepalm", 1.5]],
                         moves=[mv("doesn't|10%", 0.3, (1000, 1060), hop=50)]),
                   stamps=[stamp("NO METHOD GIVEN", "behind|60%", 1230, 330, RED, 96, 6)], meter_at="find|70%",
                   sfx=["scratch@doesn't|10%"])
    T["s1.l6"] = S("tc_cork", [900, 560, 1.0], [960, 560, 1.04],
                   [A("map", "tc_map", [640, 520], 0.75, {"place": "NETHERLANDS", "pin": 0.0, "px": -40, "py": 0},
                      sets=[set_("Netherlands|55%", 0.5, pin=1.0)]),
                    A("nd", "tc_note", [1350, 300], 1.0, {"text": "NO DUTCH NUMBERS", "px": 64, "w": 620, "h": 150, "rot": 3},
                      at="yet|60%")],
                   mbx=M("shrug", (1350, 1050), 600, look="viewer", gest=[["nobody|35%", "shrug", 3.0]]),
                   sfx=["pop@Netherlands|55%", "pop@yet|60%"])
    T["s1.l7"] = S("tc_living", [900, 640, 1.1], [900, 640, 1.16],
                   [prop("sheet", "sheet", [820, 905], 1.0, {"specks": 0}, sets=[set_("Shake|50%", 2.0, specks=7)]),
                    A("fall", "tc_fall", [790, 900], 1.0, {"on": 0.0, "w": 260, "h": 360, "n": 10}, sets=[set_("Shake|45%", 0.3, on=1.0)])],
                   mbx=M("present", (1160, 905), 620, look="viewer", prop="smalltree", gest=[["Shake|45%", "present", 3.0]]),
                   scene_p={"fireplace": False}, sfx=["scratch@Shake|45%", "tink@look|80%"])
    T["s1.l8"] = S("tc_cork", [880, 600, 1.0], [880, 600, 1.05],
                   [A("n25", "tc_note", [560, 620], 1.0, {"text": "25,000", "px": 170, "w": 700, "h": 300, "strike": 0.0},
                      sets=[set_("Iowa|25%", 0.4, strike=1.0)]),
                    A("few", "tc_note", [1330, 660], 1.0, {"text": "A FEW", "px": 64, "w": 480, "h": 130, "col": "#2f7a4a", "rot": 4},
                      at="few|60%", sets=[set_("several|78%", 0.0, text="SEVERAL HUNDRED")]),
                    chip("src", "IOWA STATE", [1330, 860], "Iowa|20%")],
                   card_at="few|60%", card_y=150, sfx=["scratch@Iowa|25%", "pop@few|60%"])
    T["s1.l9"] = S("tc_farm", [960, 640, 1.0], [960, 640, 1.06],
                   [A("one", "ds_ring", [1190, 690], 1.0, {"on": 0.0, "r": 120, "lw": 10}, sets=[set_("hundred|55%", 0.4, on=1.0)], front=True)],
                   scene_p={"snow": 1.0}, card_at="perhaps|30%", sfx=["tink@hundred|55%"])
    T["s1.l10"] = S("tc_combo", [-200, 560, 0.9], None,
                    [A("wild", "tc_wild", [-300, 920], 0.75, {"kind": "spruce"}),
                     A("spk", "tc_specks", [-300, 600], 1.0, {"n": 9, "w": 160, "h": 200, "r": 10, "col": "#2a1f1a"}, at="bugs|35%"),
                     A("farm1", "tc_farmtree", [4000 + 300, 900], 0.75), A("farm2", "tc_farmtree", [4000 + 560, 900], 0.75),
                     A("farm3", "tc_farmtree", [4000 + 820, 900], 0.75),
                     lab("lf", "FOREST", [-300, 230], "forest|60%", 60), lab("lr", "FARM", [4560, 230], "farm|85%", 60)],
                    scene_p={"a": "tc_snowwood", "pa": {}, "b": "tc_farm", "pb": {"snow": 1.0}, "bx": 200, "dx": 3800, "seam": True},
                    shots=[cam([-200, 560, 0.9], [-260, 560, 0.95]), cam([-260, 560, 0.95], [2180, 560, 0.5], at="bugs|30%", dur=0.8),
                           cam([2180, 560, 0.5], [2200, 560, 0.52], at="forest|60%")],
                    mbx=M("present", (60, 920), 560, look="viewer", gest=[["Cut", "point", 1.2]]),
                    sfx=["whoosh@bugs|30%", "pop@farm|85%"], norecut=True)
    T["s1.l11"] = S("tc_farm", [960, 600, 1.0], [960, 640, 1.25],
                    [A("big", "tc_farmtree", [960, 1060], 1.35, {"snow": 1.0}),
                     A("a1", "tc_aphid", [860, 760], 0.22, {"mood": "sleepy"}), A("b1", "tc_barkbeetle", [1060, 920], 0.22, {"mood": "sleepy"}),
                     A("z1", "tc_zz", [0, 0], 1.0, {"on": 0.0, "x": 900, "y": 680, "px": 46}, sets=[set_("winter|40%", 0.4, on=1.0)]),
                     A("z2", "tc_zz", [0, 0], 1.0, {"on": 0.0, "x": 1100, "y": 850, "px": 46}, sets=[set_("winter|55%", 0.4, on=1.0)])],
                    scene_p={"snow": 1.0, "fall": True}, sfx=["tink@winter|50%"])
    T["s1.l12"] = S("tc_yard", [800, 560, 0.95], [700, 560, 1.0],
                    [A("z1", "tc_zz", [1500, 760], 1.0, {"on": 1.0, "px": 46}, moves=[mv(0.0, 1.8, (720, 760))],
                       sets=[set_("heat|45%", 0.25, on=0.0)]),
                     A("bang", "ds_label", [720, 600], 1.0, {"text": "!", "px": 90, "color": YEL, "on": 0.0}, sets=[set_("heat|50%", 0.3, on=1.0)],
                       front=True)],
                    mbx=M("present", (1500, 905), 600, look="viewer", prop="carrytree", moves=[mv(0.0, 1.8, (560, 905), walk=True)]),
                    sfx=["step@Bring|10%", "pop@heat|50%"])
    T["s1.l13"] = S("tc_bokeh", [960, 560, 0.85], [960, 580, 1.25],
                    [twig([960, 720], 1.1), ooth([960, 720], 1.75, quiver=1.0)],
                    mbx=M("neutral", (400, 980), 560, float=True, look="viewer", gest=[["breathe|10%", "deadpan", 1.0], ["check|45%", "point", 2.0]]),
                    sfx=["sting@one|75%"], norecut=True)
    # =========================================================================================== 2. the mantis egg case
    T["s2.l0"] = S("tc_snowwood", [900, 600, 1.15], [900, 600, 1.22],
                   [twig([960, 760], 1.0), A("mantis", "tc_mantis", [780, 742], 0.62, {"look": [0.4, 0.3]}),
                    ooth([1360, 760], 1.1)],
                   chapter=True, sfx=["pop@mantis|55%"])
    T["s2.l1"] = S("tc_bokeh", [900, 580, 1.0], [960, 590, 1.08],
                   [twig([960, 760], 1.0),
                    ooth([1040, 760], 1.1, grow=0.0, wet=1.0, sets=[set_("glues|25%", 1.2, grow=1.0), set_("hardens|60%", 0.8, wet=0.0)]),
                    A("mantis", "tc_mantis", [1200, 742], 0.62, {"lay": 0.0, "look": [-0.3, 0.5]},
                      sets=[set_("glues|20%", 0.5, lay=1.0), set_("foam#2|55%", 0.4, lay=0.0)],
                      moves=[mv("hardens|60%", 1.0, (1800, 742), walk=True)]),
                    A("pages", "tc_pages", [960, 300], 0.8, {"on": 0.0, "n": 3}, at="hardens|55%")],
                   sfx=["splash@glues|25%", "whoosh@hardens|60%"])
    T["s2.l2"] = S("ds_lab", [960, 560, 1.0], [960, 560, 1.04],
                   [twig([860, 500], 0.5), ooth([860, 500], 1.6),
                    prop("can", "foamcan", [1450, 820], 0.85, at="spray|15%"),
                    prop("ruler", "ruler", [860, 800], 1.0, {"w": 900, "ppi": 266}, at="inch|45%"),
                    A("dim", "ds_dim", [660, 690], 1.0, {"to": [400, 0], "grow": 0.0, "text": "1.5 INCHES", "ly": -70, "px": 60},
                      sets=[set_("inch|60%", 0.5, grow=1.0)], front=True)],
                   sfx=["pop@spray|15%", "whoosh@inch|60%"])
    T["s2.l3"] = S("tc_bokeh", [960, 580, 1.0], [960, 580, 1.05],
                   [twig([720, 640], 0.9), ooth([680, 640], 1.6),
                    prop("ball", "pingpong", [2300, 660], 1.6, moves=[mv("ping|30%", 0.8, (1260, 660), rot=-360)]),
                    lab("cm", "CHINESE MANTIS", [680, 250], "Chinese|20%", 56, YEL)],
                   sfx=["pop@Chinese|20%", "boing@ping|45%"])
    T["s2.l4"] = S("ds_board_bg", [900, 520, 0.85], None,
                   [twig([600, 330], 0.75, idn="t1"), ooth([560, 330], 1.0, idn="c1"),
                    twig([1250, 760], 0.85, idn="t2"), ooth([1250, 760], 1.2, idn="c2", kind="carolina"),
                    lab("l1", "CHINESE", [560, 120], None, 54), lab("l2", "CAROLINA", [1250, 560], "Carolina|10%", 60, YEL)],
                   shots=[cam([900, 520, 0.85], [920, 520, 0.88]), cam([920, 520, 0.88], [1250, 700, 1.6], at="tan|60%", dur=0.6)],
                   sfx=["pop@Carolina|10%", "whoosh@tan|60%"], norecut=True)
    acts = [twig([960, 760], 1.25, idn="tw")]
    for i, (x, col, kind) in enumerate(((330, "#c9a86a", "chinese"), (760, "#8cbf4f", "chinese"), (1190, "#9c9a7c", "carolina"),
                                        (1620, "#a7b05a", "carolina"))):
        acts.append(A(f"m{i}", "tc_mantis", [x - 60, 742], 0.36, {"col": col}, at=f"four|{20 + i * 10}%"))
        acts.append(ooth([x + 150, 760], 0.55, idn=f"o{i}", kind=kind))
    acts.append(chip("src", "PENN STATE", [960, 260], "Penn|5%"))
    T["s2.l5"] = S("tc_bokeh", [960, 560, 1.0], [960, 560, 1.03], acts, sfx=["pop@four|20%", "pop@four|50%"], norecut=True)
    T["s2.l6"] = S("ds_board_bg", [0, 60, 1.0], [0, 60, 1.03],
                   [ooth([0, 260], 1.6, xray=1.0),
                    chip("c1", "MISSOURI EXTENSION", [-520, -130], "Missouri|20%", 46),
                    A("n1", "tc_note", [-520, 40], 1.0, {"text": "ABOUT 100", "px": 72, "w": 460, "h": 140, "col": "#2f7a4a"}, at="hundred|40%"),
                    chip("c2", "MISSISSIPPI STATE", [520, -130], "Mississippi|60%", 46),
                    A("n2", "tc_note", [520, 40], 1.0, {"text": "SEVERAL HUNDRED", "px": 64, "w": 560, "h": 140, "rot": 3}, at="several|80%")],
                   scene_p={"color": "#1b1724"}, sfx=["pop@hundred|40%", "pop@several|80%"])
    T["s2.l7"] = S("tc_living", [1000, 640, 1.2], [1000, 640, 1.26],
                   [tree(), ooth([1130, 640], 0.3, front=True, quiver=1.0)],
                   mbx=M("nervous", (1420, 905), 600, look="case", gest=[["several|50%", "shock", 1.0]]),
                   card_at="hundred|25%", card_y=150, sfx=["boing@several|50%"])
    T["s2.l8"] = S("tc_snowwood", [960, 560, 1.0], [960, 560, 1.06],
                   [twig([960, 640], 1.1, snow=1.0), ooth([960, 640], 1.5),
                    A("pages", "tc_pages", [960, 330], 0.9, {"n": 4}),
                    lab("sp", "SPRING", [960, 230], "spring|50%", 70, GREEN)],
                   scene_p={"fall": True}, sfx=["whoosh@Outside|10%", "pop@spring|50%"])
    nymphs = []
    for i in range(9):
        x0, y0 = 980, 520
        path = [(1000 + i * 30, 560), (1200 + i * 60, 640 + (i % 3) * 30), (1300 + i * 70, 1000)]
        nymphs.append(A(f"ny{i}", "tc_nymph", [x0, y0], 0.11, {"look": [0.5, 0.6], "hidden": True},
                        sets=[{"at": f"hatches+{0.1 * i:.1f}|{55 + i}%", "p": {"hidden": False}}],
                        moves=[mv(f"hatches+{0.1 * i:.1f}|{55 + i}%", 0.9, path[1], walk=True),
                               mv(f"dozens+{0.08 * i:.2f}|{80 + i}%", 0.9, path[2], walk=True)]))
    T["s2.l9"] = S("tc_bokeh", [1060, 600, 1.0], [1060, 620, 1.08],
                   [twig([960, 560], 1.0, idn="tw"), A("baub", "tc_bauble", [1430, 560], 0.9, {"col": "#3b7dd8"}),
                    ooth([960, 560], 1.3, split=0.0, quiver=0.6, sets=[set_("hatches|45%", 0.5, split=1.0)])] + nymphs,
                   card_at="dozens|80%", card_y=150, sfx=["crunch@hatches|45%", "pop@dozens|80%"])
    T["s2.l10"] = S("ds_board_bg", [100, 60, 1.0], [100, 60, 1.03],
                    [A("race", "tc_race", [-380, -60], 1.0, {"a": 0.0, "b": 0.0, "w": 1050},
                       sets=[set_("fresh|10%", 2.4, a=0.97), set_("three|30%", 2.0, b=0.97), set_("photo|60%", 0.4, a=1.0, b=1.0)])],
                    scene_p={"color": "#1b1724"}, flash=["finish|80%"], sfx=["whoosh@fresh|10%", "tink@finish|80%"], norecut=True)
    T["s2.l11"] = S("tc_living", [1080, 800, 2.0], [1090, 800, 2.08],
                    [A("ny", "tc_nymph", [800, 905], 0.16, {"mood": "worry", "look": [1, 0]},
                       sets=[set_("sad|20%", 0.2, look=[1, 0.2]), set_("nothing|45%", 0.2, look=[1, -0.4]), set_("eat|70%", 0.2, look=[-1, 0.1], mood="sleepy")]),
                     prop("cane", "candycane", [980, 905], 0.45), prop("gift", "gift", [1170, 905], 0.45, {"col": "#2c6fbf", "rib": "#f4f4f4"}),
                     prop("sock", "sock", [1350, 905], 0.4)],
                    scene_p={"fireplace": False}, sfx=["tink@nothing|45%"])
    T["s2.l12"] = S("tc_living", [760, 820, 2.4], None,
                    [A("n1", "tc_nymph", [640, 905], 0.2, {"mood": "angry", "look": [1, 0]}),
                     A("n2", "tc_nymph", [880, 905], 0.2, {"mood": "angry", "look": [1, 0]}, flip=True)],
                    shots=[cam([760, 830, 2.4], [760, 830, 2.5]), cam([760, 830, 2.5], [220, 300, 1.6], at="other|35%", dur=0.35)],
                    scene_p={"fireplace": False}, sfx=["whoosh@other|35%"], pad=0.25, norecut=True)
    T["s2.l13"] = S("tc_bokeh", [960, 600, 1.0], [960, 600, 1.06],
                    [A("baub", "tc_bauble", [960, 300], 1.2, {"col": "#c0392b"}),
                     A("ny", "tc_nymph", [990, 470], 0.32, {"mood": "worry", "look": [0, 0.8]},
                       sets=[set_("starve|60%", 0.6, mood="sleepy")]),
                     chip("src", "ILLINOIS EXTENSION", [960, 920], "Illinois|15%")],
                    sfx=["pop@Illinois|15%"])
    row = [A(f"ny{i}", "tc_nymph", [640 + i * 95, 905], 0.14, {"napkin": 1.0, "mood": "happy", "look": [1, -0.2]}) for i in range(5)]
    T["s2.l14"] = S("tc_living", [1080, 740, 1.4], [1090, 740, 1.46],
                    row + [prop("tub", "tub", [1240, 905], 0.75, at="crickets|60%"),
                           A("fly", "sp.fly", [1150, 640], 0.22, {}, at="flies|45%", moves=[mv("flies|45%", 1.2, (900, 700))])],
                    mbx=M("present", (1530, 905), 620, look="viewer", prop="tweezers", gest=[["crickets|65%", "present", 2.0]],
                          moves=[mv("feeding|35%", 0.4, (1500, 905), hop=40)]),
                    scene_p={"fireplace": False}, sfx=["pop@flies|45%", "pop@crickets|60%"])
    T["s2.l15"] = S("tc_cork", [960, 560, 1.0], [980, 560, 1.06],
                    [chip("src", "UNIVERSITY OF MISSOURI EXTENSION", [1150, 420], 0.02, 56)],
                    mbx=M("point", (520, 1010), 640, look="viewer", moves=[mv(0.0, 0.25, (560, 1010), hop=60)]),
                    sfx=["pop@0.05", "boing@making|50%"], pad=0.35)
    T["s2.l16"] = S("tc_lot", [760, 600, 1.0], [780, 600, 1.05],
                    [A("lt", "tc_xtree", [600, 905], 0.72, {"deco": 0.0, "lit": 0.0, "stand": False, "gifts": False}),
                     ooth([740, 520], 0.35, front=True)],
                    mbx=M("point", (1040, 905), 600, look="case", prop="magnifier", gest=[["look|40%", "point", 2.0]]),
                    check_at="look|40%", sfx=["pop@marshmallow|80%"])
    T["s2.l17"] = S("tc_bokeh", [900, 600, 1.05], [900, 600, 1.12],
                    [twig([800, 640], 0.9), ooth([760, 640], 1.3),
                     prop("shears", "shears", [1600, 600], 1.1, {"snip": 0.0}, sets=[set_("Clip|55%", 0.25, snip=1.0)],
                          moves=[mv("crush|25%", 0.5, (1180, 640))], rot=180, front=True)],
                    stamps=[stamp("CLIP", "Clip|60%", 520, 330, YEL, 130)], sfx=["crunch@Clip|60%"])
    T["s2.l18"] = S("tc_yard", [900, 600, 1.0], [880, 610, 1.06],
                    [A("shrub", "tc_shrub", [700, 905], 1.0, {"snow": 1.0})],
                    mbx=M("present", (1300, 905), 600, look="shrub", prop="twig", moves=[mv("Tuck|10%", 0.7, (1050, 905), walk=True)]),
                    check_at="evergreen|50%", sfx=["step@Tuck|10%"])
    ants = [A(f"ant{i}", "sp.ant", [1700 + i * 110, 905], 0.14, {}, flip=True,
              moves=[mv(0.0, 2.6, (1020 + i * 90, 905), walk=True)]) for i in range(5)]
    T["s2.l19"] = S("tc_yard", [1000, 700, 1.25], [1000, 700, 1.3],
                    ants + [prop("tw", "shrubtwig", [880, 880], 0.9, moves=[mv("eat|55%", 0.6, (700, 560))])],
                    mbx=M("present", (560, 905), 600, look="tw", gest=[["eat|50%", "present", 2.0]]),
                    stamps=[stamp("NOT ON THE GROUND", "ground|15%", 760, 330, RED, 80, -5)], sfx=["step@ants|35%", "whoosh@eat|55%"])
    T["s2.l20"] = S("ds_board_bg", [0, 60, 1.0], [0, 60, 1.05],
                    [A("map", "tc_map", [-120, 60], 1.0, {"place": "USA", "pin": 0.0, "ships": 0.0, "label": ""},
                       sets=[set_("big|35%", 1.2, ships=1.0)])],
                    scene_p={"color": "#1b2440"}, sfx=["whoosh@big|35%"])
    mts = [("CHINESE", "#c9a86a", -560, "Chinese|8%"), ("EUROPEAN", "#8cbf4f", -60, "European|25%"), ("CAROLINA", "#9c9a7c", 440, "Carolina|70%")]
    acts = []
    for i, (nm, col, x, w) in enumerate(mts):
        acts.append(A(f"m{i}", "tc_mantis", [x, 330], 0.5, {"col": col, "look": [0.2, 0.4]}, at=w))
        acts.append(lab(f"l{i}", nm, [x + 40, -20], w, 52, "#ffffff"))
    acts += [lab("t", "LATE 1800s", [-300, -260], "late|30%", 70, YEL),
             A("badge", "ds_stamp", [0, 0], 1.0, {"on": 0.0, "text": "NATIVE", "color": GREEN, "x": 1040, "y": 620, "px": 70, "rot": 8},
               sets=[set_("native|65%", 0.25, on=1.0)], front=True)]
    T["s2.l21"] = S("ds_board_bg", [-60, 60, 1.0], None, acts,
                    shots=[cam([-60, 60, 1.0], [-60, 60, 1.03]), cam([-60, 60, 1.03], [-300, 100, 1.12], at="late|28%", dur=0.6),
                           cam([-300, 100, 1.12], [180, 120, 1.15], at="Illinois|55%", dur=0.6)],
                    scene_p={"color": "#1b2440"}, sfx=["pop@late|30%", "stamp@native|65%"], norecut=True)
    # =========================================================================================== 3. the one people call a tick
    T["s3.l0"] = S("tc_living", [1000, 720, 1.3], [1000, 720, 1.36],
                   [prop("gift", "gift", [1000, 905], 1.6, {"col": "#c0392b"}),
                    A("aph", "tc_aphid", [740, 633], 0.4, {}, moves=[mv(0.2, 2.4, (1180, 633), walk=True)])],
                   mbx=M("neutral", (1540, 905), 560, look="aph", gest=[["tick|70%", "shock", 1.0]]),
                   scene_p={"fireplace": False}, chapter=True, sfx=["boing@tick|70%"])
    drops = [A(f"a{i}", "tc_aphid", [700 + i * 170, 330], 0.3, {"look": [0, 1]},
               moves=[mv(f"Walking+{0.15 * i:.2f}|{45 + 5 * i}%", 0.6, (720 + i * 170, 690))]) for i in range(4)]
    T["s3.l1"] = S("tc_living", [960, 330, 2.2], None,
                   [twig([960, 330], 1.0, idn="tw"), prop("g1", "gift", [800, 905], 1.2, {"col": "#c0392b"}),
                    prop("g2", "gift", [1200, 905], 1.0, {"col": "#2c6fbf", "rib": "#f4f4f4", "w": 260})] + drops,
                   shots=[cam([880, 290, 2.0], [880, 290, 2.1]), cam([880, 290, 2.1], [960, 560, 0.95], at="Walking|40%", dur=0.7)],
                   scene_p={"fireplace": False}, meter_at="presents|70%", sfx=["whoosh@Walking|40%", "thud@presents|70%"], norecut=True)
    T["s3.l2"] = S("tc_bokeh", [960, 580, 1.0], [960, 580, 1.04],
                   [prop("ruler", "ruler", [960, 760], 1.0, {"w": 1000, "ppi": 3360}),
                    A("aph", "tc_aphid", [990, 700], 1.0, {"look": [0, 0]}),
                    A("dim", "ds_dim", [780, 880], 1.0, {"to": [420, 0], "grow": 0.0, "text": "UP TO 1/8 INCH", "ly": 60, "px": 60},
                      sets=[set_("eighth|60%", 0.5, grow=1.0)], front=True)],
                   card_at="giant|20%", sfx=["pop@giant|20%", "whoosh@eighth|60%"])
    T["s3.l3"] = S("tc_farm", [960, 600, 1.0], [960, 600, 1.06],
                   [twig([960, 760], 1.0), A("aph", "tc_aphid", [800, 742], 0.75, {"flex": 0.0, "mood": "smug"}, sets=[set_("largest|40%", 0.4, flex=1.0)]),
                    A("small", "tc_aphid", [1280, 742], 0.16, {"col": "#8fcf5a", "mood": "worry", "look": [-1, -0.5]}),
                    chip("src", "N.C. STATE", [960, 300], "State|10%")],
                   scene_p={"snow": 0.0}, sfx=["boing@largest|40%"])
    T["s3.l4"] = S("tc_bokeh", [960, 600, 1.0], [960, 600, 1.05],
                   [A("aph", "tc_aphid", [700, 800], 0.65, {"look": [1, 0]}), A("tick", "sp.tick", [1260, 800], 0.55, {}),
                    lab("q", "?", [960, 420], "mistake|55%", 120, YEL), lab("tl", "TICK", [1260, 280], "ticks|80%", 56),
                    prop("lens", "lens", [600, 600], 0.95, moves=[mv("people|20%", 1.2, (1180, 600))], front=True)],
                   sfx=["whoosh@people|20%", "pop@mistake|55%"])
    T["s3.l5"] = S("ds_board_bg", [0, 60, 1.0], [0, 60, 1.03],
                   [A("aph", "tc_aphid", [-420, 120], 0.78, {"top": True, "count": 0.0}, sets=[set_("count|20%", 1.6, count=6.0)]),
                    A("tick", "tc_tick_top", [380, 120], 0.78, {"count": 0.0}, sets=[set_("Ticks|5%", 1.4, count=8.0)]),
                    lab("la", "APHID", [-420, 500], "aphid|30%", 56), lab("lt", "TICK", [380, 500], "Ticks|5%", 56)],
                   scene_p={"color": "#1b1724"}, card_at="eight|85%", card_y=150, meter_at="eight|85%", sfx=["tink@six|50%", "tink@eight|85%"],
                   norecut=True)
    T["s3.l6"] = S("ds_board_bg", [-60, 80, 1.0], None,
                   [prop("i1", "icon", [-560, 80], 1.0, {"icon": "tooth", "x": 0.0}, sets=[set_("bite|25%", 0.3, x=1.0)]),
                    prop("i2", "icon", [-200, 80], 1.0, {"icon": "sting", "x": 0.0}, sets=[set_("sting|35%", 0.3, x=1.0)]),
                    prop("i3", "icon", [160, 80], 1.0, {"icon": "germ", "x": 0.0}, sets=[set_("disease|45%", 0.3, x=1.0)]),
                    prop("plant", "plant", [1900, 420], 1.1), A("aph", "tc_aphid", [1650, 420], 0.3, {"look": [1, -0.5]}),
                    A("ok", "tc_tick", [2150, -120], 1.0, {"on": 0.0}, sets=[set_("houseplants|70%", 0.3, on=1.0)], front=True)],
                   shots=[cam([-200, 80, 1.0], [-200, 80, 1.03]), cam([-200, 80, 1.03], [1950, 100, 1.0], at="And|55%", dur=0.6)],
                   scene_p={"color": "#1b1724"}, sfx=["stamp@bite|25%", "tink@houseplants|70%"], norecut=True)
    yawners = [A(f"a{i}", "tc_aphid", [620 + i * 230, 742], 0.32, {"yawn": 1.0, "mood": "sleepy"},
                 sets=[set_("wakes|30%", 0.3, yawn=0.0, mood="calm")], moves=[mv("wander|60%", 1.0, (900 + i * 230, 742), walk=True)])
               for i in range(3)]
    T["s3.l7"] = S("tc_bokeh", [960, 620, 1.0], [1060, 620, 1.05], [twig([960, 760], 1.2)] + yawners, sfx=["boing@wakes|30%"])
    T["s3.l8"] = S("tc_living", [960, 560, 0.95], [960, 580, 1.0],
                   [twig([700, 230], 0.9, idn="tw", col="#7f8a3c"), A("baub", "tc_bauble", [520, 250], 0.6, {"col": "#f2c14e"}),
                    prop("chair", "armchair", [1180, 905], 1.0)] +
                   [A(f"a{i}", "tc_aphid", [760 + i * 90, 250], 0.2, {}, moves=[mv(f"move+{0.2 * i:.1f}|{30 + 6 * i}%", 1.2, (1080 + i * 90, 585))])
                    for i in range(3)] + [A("a3", "tc_aphid", [520, 520], 0.16, {})],
                   scene_p={"fireplace": False}, sfx=["step@move|35%", "thud@furniture|80%"])
    T["s3.l9"] = S("tc_living", [1080, 640, 1.15], [1080, 640, 1.2],
                   [A("aph", "tc_aphid", [960, 960], 0.32, {"mood": "shock", "look": [1, -0.8]})],
                   mbx=M("neutral", (1300, 960), 680, look="aph", prop="slipper", gest=[["rule|30%", "wave", 4.0]]),
                   scene_p={"fireplace": False}, sfx=["whoosh@rule|30%", "thud@squash|80%"], shake=["squash|80%"])
    T["s3.l10"] = S("tc_living", [620, 760, 1.4], None,
                    [prop("gift", "gift", [620, 905], 1.4, {"col": "#f4f4f4", "rib": "#e5383b", "stain": 0.0},
                          sets=[set_("stain|35%", 0.5, stain=1.0)]),
                     A("rug", "tc_stain", [1500, 960], 1.0, {"rug": True, "grow": 0.0}, sets=[set_("Carpet|55%", 0.5, grow=1.0)])],
                    shots=[cam([620, 760, 1.4], [620, 760, 1.46]), cam([620, 760, 1.46], [1500, 860, 1.4], at="Carpet|50%", dur=0.5)],
                    scene_p={"fireplace": False}, card_at="purple|25%", meter_at="stain|40%", sfx=["crunch@stain|35%", "whoosh@Carpet|50%"],
                    norecut=True)
    suck = [A(f"a{i}", "tc_aphid", [1080 + i * 110, 960], 0.2, {}, moves=[mv(f"hose+{0.15 * i:.2f}|{40 + 6 * i}%", 0.35, (900, 700), s=0.01)])
            for i in range(3)]
    T["s3.l11"] = S("tc_living", [980, 700, 1.15], [980, 700, 1.2],
                    [prop("vac", "canvac", [380, 960], 0.9, {"tip": [560, -280], "suck": 1.0}),
                     prop("brush", "brushhead", [1350, 960], 0.9),
                     A("x", "ds_cross", [1350, 870], 1.0, {"on": 0.0, "r": 140}, sets=[set_("brush|65%", 0.3, on=1.0)], front=True)] + suck,
                    scene_p={"fireplace": False}, stamps=[stamp("VACUUM", "Vacuum|10%", 560, 330, YEL, 120)], check_at="hose|40%",
                    sfx=["whoosh@hose|40%"])
    winged = [A(f"w{i}", "tc_aphid", [800 + i * 160, 520 - (i % 2) * 120], 0.18, {"winged": True}, at=f"breed|{55 + 8 * i}%") for i in range(3)]
    T["s3.l12"] = S("tc_living", [960, 560, 0.9], [960, 560, 0.95],
                    [A("rb", "tc_rootball", [960, 905], 1.0)] + winged +
                    [A(f"q{i}", "tc_qm", [880 + i * 160, 440 - (i % 2) * 120], 1.0, {"on": 0.0, "px": 70, "ph": i}, sets=[set_(f"breed|{60 + 8 * i}%", 0.3, on=1.0)],
                       front=True) for i in range(3)] + [chip("src", "PENN STATE", [560, 290], "Penn|60%")],
                    scene_p={"fireplace": False}, sfx=["pop@root|40%", "pop@breed|60%"])
    T["s3.l13"] = S("tc_trunk", [960, 560, 1.0], [960, 560, 1.08],
                    [A("tick", "sp.tick", [880, 680], 0.32, {}),
                     A("tag", "ds_tag", [1040, 560], 0.8, {"on": 0.0, "text": "RARE"}, sets=[set_("few|45%", 0.35, on=1.0)])],
                    mbx=M("deadpan", (1320, 1120), 560, float=True, look="viewer", gest=[["few#2|85%", "deadpan", 1.0]]),
                    sfx=["pop@few|45%"])
    T["s3.l14"] = S("ds_board_bg", [60, 60, 1.0], [60, 60, 1.03],
                    [A("strip", "tc_strip", [-120, 120], 0.78, {"done": 2, "blur": 0.0, "glow9": 0.0},
                       sets=[set_("six|25%", 1.2, blur=1.0), set_("matters|70%", 0.5, glow9=1.0)])],
                    scene_p={"color": "#1b1724"}, sfx=["whoosh@six|25%", "tink@matters|70%"], norecut=True)
    # =========================================================================================== 4. 3 to 8, the ones you can ignore
    T["s4.l0"] = S("tc_bokeh", [960, 600, 1.4], None,
                   [twig([960, 760], 1.0), A("sp", "house_sp_small", [900, 742], 0.32, {}),
                    A("sl", "tc_spiderlings", [1160, 720], 0.9, {"n": 12}),
                    A("aph", "tc_aphid", [520, 742], 0.3, {}),
                    lab("la", "APHIDS", [520, 470], "aphids|50%", 54), lab("ls", "SPIDERS", [960, 470], "spiders#2|60%", 54)],
                   shots=[cam([1000, 640, 1.5], [1020, 640, 1.56]), cam([1020, 640, 1.56], [860, 600, 1.0], at="Iowa|35%", dur=0.6),
                          cam([860, 600, 1.0], [1080, 680, 1.45], at="most|65%", dur=0.6)],
                   chapter=True, sfx=["pop@aphids|50%", "pop@spiders#2|60%"], norecut=True)
    T["s4.l1"] = S("tc_living", [960, 600, 0.95], [960, 610, 1.0],
                   [tree(LR_TREE, 0.7), A("sp", "house_sp_small", [860, 780], 0.13, {}),
                    A("dog", "tc_dog", [1380, 905], 0.6, {"sniff": 1.0}, flip=True)],
                   no_card=True, stamps=[IGN("die|55%", 520, 330)], sfx=["step@pets|40%"])
    T["s4.l2"] = S("tc_living", [960, 800, 1.6], [980, 800, 1.66],
                   [tree(LR_TREE, 0.9, deco=1.0), A("dust", "tc_sawdust", [1080, 905], 1.0),
                    A("bb", "tc_barkbeetle", [880, 905], 0.32, {}, moves=[mv("beetles|25%", 1.2, (1180, 905), walk=True)]),
                    lab("lb", "BARK BEETLE", [1020, 600], "Bark|15%", 52, YEL)],
                   sfx=["pop@Bark|15%", "tink@sawdust|80%"])
    T["s4.l3"] = S("tc_living", [960, 760, 1.4], [960, 760, 1.46],
                   [prop("table", "table", [900, 905], 1.0),
                    A("bb", "tc_barkbeetle", [1300, 905], 0.36, {"shake": 0.0}, flip=True,
                      moves=[mv(0.05, 0.6, (1180, 905), walk=True), mv("damp|55%", 1.2, (1700, 905), walk=True, face=1)],
                      sets=[set_("No|25%", 0.2, shake=1.0), set_("damp|55%", 0.2, shake=0.0)])],
                   scene_p={"fireplace": False}, no_card=True, stamps=[IGN("dry|65%", 560, 330)], sfx=["tink@No|25%"])
    T["s4.l4"] = S("tc_trunk", [880, 560, 1.0], [880, 560, 1.05],
                   [A("ad", "tc_adelgid", [800, 560], 1.0, {"poke": 0.0}, sets=[set_("stay|50%", 0.2, poke=1.0)]),
                    lab("l", "ADELGIDS", [800, 220], "Adelgids|35%", 60, YEL)],
                   mbx=M("point", (1300, 1080), 620, float=True, look="ad", gest=[["stay|50%", "point", 1.0], ["harmless|80%", "shrug", 1.0]]),
                   no_card=True, stamps=[IGN("harmless|75%", 560, 360)], sfx=["pop@Adelgids|35%", "boing@stay|50%"])
    T["s4.l5"] = S("tc_living", [220, 470, 2.2], [240, 470, 2.3],
                   [A("cr", "tc_crawlers", [60, 540], 1.0, {"n": 10, "len": 320, "u": 0.0, "gone": 0.0},
                      sets=[set_("walking|20%", 2.4, u=1.0), set_("Wipe|70%", 0.6, gone=1.0)]),
                    prop("cloth", "cloth", [-200, 520], 0.6, moves=[mv("Wipe|70%", 0.6, (480, 520))], front=True),
                    lab("l", "SCALE CRAWLERS", [220, 380], "Scale|45%", 30, YEL)],
                   scene_p={"fireplace": False}, no_card=True, stamps=[IGN("towel|85%", 1250, 760)], sfx=["scratch@Wipe|70%"])
    T["s4.l6"] = S("tc_bokeh", [960, 600, 1.0], [960, 600, 1.06],
                   [twig([960, 780], 1.0), A("mite", "tc_mite", [880, 560], 1.1, {"eat": 0.0}, sets=[set_("Penn|20%", 3.0, eat=0.9)]),
                    lab("l", "MITE", [880, 300], "Mites|10%", 60, YEL)],
                   no_card=True, stamps=[IGN("bite|60%", 1250, 360)], sfx=["crunch@predatory|50%"])
    T["s4.l7"] = S("tc_living", [1000, 560, 0.95], [1000, 570, 1.0],
                   [tree(LR_TREE, 0.7),
                    A("nest", "tc_nest", [1050, 520], 0.42, {}, moves=[mv("take|50%", 0.6, (1230, 470))]),
                    A("mites", "tc_specks", [1050, 500], 1.0, {"n": 6, "w": 40, "h": 20, "r": 4, "col": "#e0873a"}, at="mites|80%",
                      moves=[mv("take|50%", 0.6, (1230, 450))])],
                   mbx=M("present", (1330, 905), 580, look="nest", prop="tongs", gest=[["take|50%", "present", 3.0]]),
                   check_at="take|55%", sfx=["scratch@take|50%"])
    T["s4.l8"] = S("tc_living", [940, 620, 1.2], [940, 620, 1.26],
                   [prop("rad", "radiator", [940, 905], 1.0) if False else A("rad", "ds_prop", [940, 905], 1.0, {"kind": "radiator"}),
                    A("bl1", "tc_barklouse", [820, 380], 0.36, {}, sets=[set_("kills|55%", 0.5, hidden=True)]),
                    A("bl2", "tc_barklouse", [1040, 320], 0.34, {}, flip=True, sets=[set_("kills+0.15|60%", 0.5, hidden=True)]),
                    A("bl3", "tc_barklouse", [1180, 430], 0.32, {}, sets=[set_("kills+0.3|65%", 0.5, hidden=True)]),
                    lab("l", "BARK LICE", [960, 220], "Bark|10%", 56, YEL)],
                   scene_p={"fireplace": False}, no_card=True, stamps=[IGN("quickly|70%", 560, 360)], sfx=["pop@kills|55%"])
    six = [("house_sp_small", {}, 0.36, 0), ("tc_barkbeetle", {}, 0.42, 0), ("tc_adelgid", {"n": 5}, 0.42, -40),
           ("tc_crawlers", {"n": 6, "len": 160}, 1.0, -30), ("tc_mite", {"egg": False}, 0.55, -60), ("tc_barklouse", {}, 0.55, 0)]

    def six_row(fade_at=None):
        acts = []
        for i, (typ, pp, sc, dy) in enumerate(six):
            x = -720 + i * 245
            sets = [set_(fade_at, 0.8, a=0.0)] if fade_at else None
            acts.append(A(f"s{i}", "ds_sil", [x, 200 + dy], 1.0, {"kind": typ, "kp": pp, "a": 0.9}, sets=sets) if typ != "tc_crawlers"
                        else A(f"s{i}", "ds_sil", [x - 80, 160], 1.0, {"kind": typ, "kp": pp, "a": 0.9}, sets=sets))
            acts[-1]["s"] = sc if typ != "tc_crawlers" else 1.0
        return acts
    T["s4.l9"] = S("ds_board_bg", [-120, 120, 1.0], [-120, 120, 1.03], six_row(),
                   scene_p={"color": "#d8dee6"},
                   stamps=[stamp("IGNORE", f"{20 + 12 * i}%", 240 + i * 245, 700, GREEN, 54, -6 + 3 * i)
                           for i in range(6)],
                   sfx=["whoosh@0.1"], norecut=True)
    T["s4.l10"] = S("ds_lab", [960, 640, 1.8], [960, 640, 1.9],
                    [prop("rice", "grain", [760, 620], 1.2), A("speck", "tc_aphid", [1080, 650], 0.15, {}),
                     A("sl", "tc_spiderlings", [1240, 640], 0.45, {"n": 2, "w": 30, "h": 10})],
                    card_at="sixteenth|60%", sfx=["tink@sixteenth|60%"])
    T["s4.l11"] = S("ds_board_bg", [-120, 120, 1.0], [-120, 120, 1.04], six_row("starve|20%"),
                    scene_p={"color": "#d8dee6"}, sfx=["whoosh@starve|20%"], norecut=True)
    T["s4.l12"] = S("tc_living", [800, 560, 0.95], None,
                    [tree([700, 905], 0.7), A("sp", "tc_specks", [1420, 300], 1.0, {"n": 1, "r": 12})],
                    shots=[cam([760, 540, 1.0], [760, 540, 1.04]), cam([760, 540, 1.04], [700, 600, 1.25], at="until|28%", dur=0.6),
                           cam([700, 600, 1.25], [1150, 520, 1.0], at="vacuum|55%", dur=0.6)],
                    mbx=M("neutral", (1180, 905), 620, look="viewer", prop="hose", gest=[["vacuum|55%", "wave", 4.0]]),
                    chip_done="tree#2|40%", sfx=["whoosh@vacuum|55%"], norecut=True)
    # =========================================================================================== 5. the lanternfly
    T["s5.l0"] = S("tc_trunk", [960, -200, 1.0], None,
                   [A("eggs", "tc_slf_eggs", [960, 1040], 1.0)],
                   shots=[cam([960, -200, 1.0], [960, 760, 1.15], at=0.3, dur=3.2)],
                   chapter=True, sfx=["sting@county|80%"], norecut=True, sheet_at=0.95)
    T["s5.l1"] = S("ds_board_bg", [0, 60, 1.3], None,
                   [A("eggs", "tc_slf_eggs", [-380, 120], 1.3),
                    A("lt", "tc_xtree", [420, 500], 0.5, {"deco": 0.0, "lit": 0.0, "gifts": False}, at="Christmas|80%"),
                    chip("src", "PENN STATE", [0, 380], "Penn|30%"), lab("u", "UNLIKELY", [0, 300], "unlikely|45%", 56, YEL)],
                   shots=[cam([-380, 120, 1.6], [-380, 120, 1.65]), cam([-380, 120, 1.65], [0, 160, 1.0], at="Penn|30%", dur=0.6)],
                   scene_p={"color": "#1b1724"},
                   card_at="Spotted|10%", sfx=["pop@unlikely|45%"], norecut=True)
    T["s5.l2"] = S("tc_trunk", [960, 580, 1.8], [960, 580, 1.9],
                   [A("eggs", "tc_slf_eggs", [960, 600], 1.0)], sfx=["tink@mud|80%"])
    T["s5.l3"] = S("tc_living", [220, 470, 2.2], [210, 470, 2.3],
                   [A("ny", "tc_slf_nymphs", [210, 540], 0.5, {"n": 4, "gone": 0.0}, sets=[set_("die|55%", 0.6, gone=1.0)])],
                   scene_p={"fireplace": False}, sfx=["pop@hatch|25%"])
    T["s5.l4"] = S("tc_combo", [600, 660, 0.75], None,
                   [A("car", "tc_car", [-300, 990], 0.7, {}, moves=[mv(0.0, 2.6, (2000, 990), linear=True)]),
                    A("shrub", "tc_shrub", [4600 + 700, 905], 0.9, {"spring": 1.0}),
                    A("ny", "tc_slf_nymphs", [4600 + 1080, 900], 0.6, {"n": 4}),
                    ],
                   scene_p={"a": "tc_road", "pa": {"sign": 1100}, "b": "tc_yard", "pb": {"spring": 1.0}, "bx": 3000, "dx": 4600},
                   shots=[cam([300, 700, 0.75], [1500, 700, 0.75], dur=2.4), cam([1500, 700, 0.75], [5560, 620, 0.95], at="hatch|60%", dur=0.5)],
                   sfx=["whoosh@ride|20%", "whoosh@hatch|60%"], norecut=True)
    T["s5.l5"] = S("tc_lot", [900, 600, 1.0], [920, 600, 1.05],
                   [A("lt", "tc_xtree", [1060, 905], 0.72, {"deco": 0.0, "lit": 0.0, "stand": False, "gifts": False})],
                   mbx=M("point", (560, 905), 600, look="lt", prop="torch", gest=[["trunk|60%", "point", 2.0]]),
                   check_at="trunk|60%", stamps=[stamp("CHECK THE TRUNK", "trunk|65%", 640, 330, RED, 76)], sfx=["click@check|50%"])
    T["s5.l6"] = S("tc_trunk", [960, 600, 1.2], [980, 600, 1.26],
                   [A("eggs", "tc_slf_eggs", [880, 560], 1.0, {"off": 0.0}, sets=[set_("Scrape|20%", 0.9, off=1.0)],
                      moves=[mv("Scrape|20%", 0.9, (1120, 700), s=0.6)]),
                    prop("scr", "scraper", [520, 590], 0.9, moves=[mv("Scrape|20%", 0.9, (1000, 690))], front=True),
                    prop("bag", "zipbag", [1240, 1000], 0.9, front=True)],
                   sfx=["scratch@Scrape|20%", "crunch@smash|85%"], shake=["smash|85%"])
    T["s5.l7"] = S("tc_living", [960, 560, 1.0], [960, 560, 1.05],
                   [prop("phone", "phone", [760, 900], 1.1, {}, at="Outside|5%")],
                   mbx=M("point", (1230, 905), 600, look="phone", gest=[["Report|55%", "point", 1.5]]),
                   scene_p={"fireplace": False}, sfx=["pop@Outside|5%", "tink@Report|55%"])
    T["s5.l8"] = S("tc_curb", [960, 600, 1.0], [960, 610, 1.05],
                   [A("lying", "tc_tree_lying", [520, 830], 0.75, {"dry": 0.5}),
                    A("tag", "ds_tag", [800, 760], 0.85, {"on": 0.0, "text": "RECYCLE"}, sets=[set_("chipping|55%", 0.35, on=1.0)])],
                   sfx=["pop@chipping|55%"])
    # =========================================================================================== 6. the mistake
    T["s6.l0"] = S("tc_living", [1060, 560, 0.95], [1060, 560, 1.15],
                   [tree(lit=1.0)],
                   mbx=M("point", (1520, 905), 600, look="xtree", prop="aerosol", gest=[["spray|75%", "shock", 1.0]]),
                   chapter=True, flash=["spray|75%"], sfx=["stamp@spray|75%"])
    T["s6.l1"] = S("ds_board_bg", [0, 100, 1.0], [0, 100, 1.04],
                   [prop("can", "aerosol", [-180, 560], 1.3, {"flame": 0.0}, sets=[set_("flammable|40%", 0.6, flame=1.0)]),
                    chip("src", "PENN STATE", [-180, -170], "Penn|5%")],
                   mbx=M("shock", (560, 560), 600, float=True, look="can", gest=[["flammable|45%", "shock", 2.0]]),
                   scene_p={"color": "#1b1724"}, sfx=["whoosh@flammable|40%"])
    T["s6.l2"] = S("ds_board_bg", [0, 140, 1.0], [0, 140, 1.04],
                   [prop("can", "aerosol", [-200, 640], 1.1, {"flame": 1.0}),
                    A("x", "ds_cross", [-200, 400], 1.0, {"on": 0.0, "r": 200}, sets=[set_("never|60%", 0.3, on=1.0)], front=True),
                    chip("src", "ILLINOIS EXTENSION", [-200, 820], "Illinois|5%")],
                   mbx=M("deadpan", (420, 600), 560, float=True, look="viewer"),
                   scene_p={"color": "#1b1724"}, card_at="never|50%", card_y=150, check_at="never|60%", sfx=["stamp@never|60%"])
    T["s6.l3"] = S("tc_living", [980, 560, 1.0], [960, 560, 1.06],
                   [tree(lit=1.0, sets=[set_("lights|45%", 0.4, lit=1.0)]),
                    A("glow", "ds_ring", [960, 500], 1.0, {"on": 0.0, "r": 380, "lw": 16}, sets=[set_("fire|75%", 0.4, on=1.0)])],
                   mbx=M("nervous", (1380, 905), 600, look="xtree", prop="aerosol_down", moves=[mv("fire|70%", 1.0, (1560, 905), walk=True)]),
                   chip_done=None, sfx=["boing@fire|75%"])
    T["s6.l4"] = S("tc_living", [1000, 640, 1.2], [1000, 640, 1.26],
                   [prop("table", "table", [900, 905], 1.0, {"open": 0.0}, sets=[set_("need|25%", 0.4, open=1.0), set_("recommended|85%", 0.4, open=0.0)]),
                    prop("can", "aerosol", [1240, 640], 0.5, moves=[mv("need|35%", 0.8, (900, 520), s=0.01)])],
                   mbx=M("neutral", (1420, 905), 600, look="viewer", gest=[["recommended|85%", "laugh", 1.0]]),
                   scene_p={"fireplace": False}, meter_at="recommended|80%", sfx=["thud@recommended|85%"])
    T["s6.l5"] = S("tc_combo", [900, 560, 0.95], None,
                   [A("p1", "person", [560, 905], 0.6, {"body": "#2f7a4a", "arm": "up", "mood": "happy", "hair": "#3a2a1e"}),
                    prop("sg1", "sign", [560 + 138, 905 - 468], 0.6, {"text": "HOSE IT", "col": "#e8f6ff", "tcol": "#2c6fbf"}),
                    chip("c1", "N.C. STATE", [560, 870], "North|8%", 40),
                    A("p2", "person", [1260, 905], 0.6, {"body": "#7a2f2f", "arm": "up", "mood": "angry", "hair": "#d9b44a"}, at="Norwegian|35%"),
                    prop("sg2", "sign", [1260 + 138, 905 - 468], 0.6, {"text": "DON'T", "col": "#ffe0e0", "tcol": "#c0392b"}, at="Norwegian|35%"),
                    chip("c2", "THE NORWEGIAN BIOLOGIST", [1260, 870], "Norwegian|35%", 40),
                    A("shk", "tc_shaker", [4600 + 700, 905], 0.95, {"shake": 0.0, "fall": 0.0},
                      sets=[set_("Shaking|70%", 0.3, shake=1.0, fall=1.0)]),
                    A("pile", "tc_specks", [4600 + 700, 880], 1.0, {"n": 16, "w": 160, "h": 10, "r": 8, "col": "#2a1f1a"}, at="advice|85%"),
                    A("lying", "tc_tree_lying", [4600 + 1060, 860], 0.5, {}, at="agrees|88%", moves=[mv("agrees|88%", 0.8, (4600 + 1500, 860))])],
                   scene_p={"a": "tc_yard", "pa": {"house_w": 200}, "b": "tc_lot", "pb": {}, "bx": 3000, "dx": 4600},
                   shots=[cam([700, 560, 1.0], [760, 560, 1.02]), cam([760, 560, 1.02], [600, 520, 1.3], at="can|22%", dur=0.5),
                          cam([600, 520, 1.3], [960, 560, 0.95], at="Norwegian|35%", dur=0.6),
                          cam([960, 560, 0.95], [1260, 520, 1.3], at="washing|52%", dur=0.5),
                          cam([1260, 520, 1.3], [5560, 560, 0.95], at="Shaking|68%", dur=0.45)],
                   mbx=M("think", (900, 905), 520, look="viewer", gest=[["Shaking|68%", "point", 1.0]]),
                   check_at="Shaking|72%", sfx=["whoosh@Shaking|68%", "scratch@agrees|88%"], norecut=True)
    T["s6.l6"] = S("tc_living", [1180, 640, 0.95], None,
                   [A("pile", "tc_prop", [560, 905], 1.0, {"kind": "logs", "n": 9}),
                    A("bb", "tc_barkbeetle", [600, 600], 0.22, {"look": [1, 0]}, at="wake|65%"),
                    A("x", "ds_cross", [560, 700], 1.0, {"on": 0.0, "r": 200}, sets=[set_("wake|75%", 0.3, on=1.0)], front=True),
                    prop("arm", "logs", [1300, 905], 0.9, {"n": 2}, at="day|30%")],
                   shots=[cam([1300, 660, 1.0], [1360, 660, 1.04]), cam([1360, 660, 1.04], [1300, 760, 1.4], at="Illinois|22%", dur=0.5),
                           cam([1300, 760, 1.4], [900, 660, 0.95], at="because|60%", dur=0.6)],
                   scene_p={"fireplace": True, "fx": 1700}, sfx=["thud@day|30%", "pop@wake|65%"], norecut=True)
    # =========================================================================================== 7. the tree check (list = right half)
    T["s7.l0"] = S("tc_living", [960, 560, 0.95], [940, 560, 1.0],
                   [tree([420, 905], 0.68, lit=1.0)],
                   mbx=M("present", (760, 905), 580, look="viewer"), sfx=["whoosh@0.05"])
    T["s7.l1"] = S("tc_lot", [700, 600, 1.0], None,
                   [A("end", "tc_tree_end", [420, 620], 0.7, {"peek": 0.0}, sets=[set_("scan|55%", 0.5, peek=1.0)]),
                    ooth([470, 560], 0.3, front=True)],
                   shots=[cam([720, 600, 1.0], [720, 600, 1.03]), cam([720, 600, 1.03], [600, 640, 1.25], at="look|30%", dur=0.5),
                           cam([600, 640, 1.25], [600, 560, 1.7], at="scan|55%", dur=0.7)],
                   mbx=M("think", (860, 905), 560, look="end", prop="magnifier", gest=[["look|40%", "point", 2.0]]),
                   list_step=1, tick_at="marshmallow|85%", sfx=["whoosh@scan|55%"], norecut=True)
    T["s7.l2"] = S("tc_combo", [520, 600, 1.0], None,
                   [twig([560, 640], 0.8), ooth([460, 640], 1.1),
                    prop("shears", "shears", [1000, 620], 1.0, {"snip": 0.0}, sets=[set_("Clip|15%", 0.25, snip=1.0)], rot=180, front=True),
                    A("shrub", "tc_shrub", [4600 + 300, 905], 0.9, {"snow": 1.0})],
                   scene_p={"a": "tc_bokeh", "pa": {}, "b": "tc_yard", "pb": {}, "bx": 3000, "dx": 4600},
                   shots=[cam([520, 600, 1.0], [520, 600, 1.04]), cam([520, 600, 1.04], [4600 + 520, 600, 1.0], at="tuck|55%", dur=0.45)],
                   mbx=M("present", (4600 + 740, 905), 560, look="shrub", prop="twig"),
                   list_step=2, tick_at="evergreen|85%", sfx=["crunch@Clip|15%", "whoosh@tuck|55%"], norecut=True)
    T["s7.l3"] = S("tc_lot", [560, 600, 1.0], None,
                   [A("shk", "tc_shaker", [420, 905], 0.85, {"shake": 0.0, "fall": 0.0},
                      sets=[set_("Shake|8%", 0.3, shake=1.0, fall=1.0), set_("move|60%", 0.3, shake=0.0, fall=0.0)]),
                    A("pile", "tc_specks", [420, 880], 1.0, {"n": 14, "w": 150, "h": 8, "r": 8}, at="shaker|40%")],
                   mbx=M("present", (800, 905), 520, look="shk", prop="carrytree", moves=[mv("move|60%", 1.2, (900, 905), walk=True)]),
                   list_step=3, tick_at="back|85%", sfx=["scratch@Shake|8%", "step@move|60%"], norecut=True)
    T["s7.l4"] = S("tc_trunk", [700, 560, 1.0], [680, 560, 1.05],
                   [A("nest", "tc_nest", [400, 400], 0.6, {}, moves=[mv("Pull|20%", 0.5, (-300, 200))]),
                    prop("torch", "flashlight", [140, 760], 0.9, {"beam": 0.0}, sets=[set_("check|60%", 0.3, beam=1.0)], rot=-15, front=True)],
                   scene_p={"x0": 160, "x1": 760}, list_step=4, tick_at="trunk|85%", sfx=["whoosh@Pull|20%", "click@check|60%"])
    T["s7.l5"] = S("ds_board_bg", [960, 540, 1.0], [960, 540, 1.02],
                   [prop("vac", "canvac", [170, 760], 0.42, {"tip": [420, -360]}, at="vacuum|20%"),
                    A("ok", "tc_tick", [230, 360], 0.8, {"on": 0.0}, sets=[set_("vacuum|25%", 0.3, on=1.0)], front=True),
                    prop("sl", "slipper", [490, 700], 0.6, at="squash|50%"),
                    A("x1", "ds_cross", [490, 640], 1.0, {"on": 0.0, "r": 110}, sets=[set_("squash|55%", 0.3, on=1.0)], front=True),
                    prop("can", "aerosol", [790, 780], 0.6, at="spray|78%"),
                    A("x2", "ds_cross", [790, 640], 1.0, {"on": 0.0, "r": 110}, sets=[set_("spray|82%", 0.3, on=1.0)], front=True)],
                   scene_p={"color": "#1b1724"}, list_step=5, tick_at="spray|90%", sfx=["stamp@squash|55%", "stamp@spray|82%"], norecut=True)
    T["s7.l6"] = S("tc_living", [960, 560, 0.95], [940, 560, 1.0],
                   [tree([420, 905], 0.68, lit=1.0)],
                   mbx=M("laugh", (760, 905), 580, look="viewer", moves=[mv(0.05, 0.4, (760, 905), hop=90)]),
                   list_all=True, pad=1.35, sfx=["boing@0.05"])
    # =========================================================================================== 8. the verdict
    T["s8.l0"] = S("tc_living", [1380, 600, 1.25], [1380, 600, 1.3],
                   [tree(lit=1.0)],
                   mbx=M("neutral", (1460, 905), 600, look="viewer", gest=[["one|50%", "laugh", 1.5]]),
                   meter_big_to=1.0, meter_big_at="0%", meter_at="one|40%", meter_big_back="100%", pad=0.7, sfx=["tink@one|40%"], list_hide=True)
    T["s8.l1"] = S("tc_living", [960, 560, 0.95], None,
                   [tree(lit=1.0, zs=1.0), A("sp", "tc_specks", [900, 560], 1.0, {"n": 3, "w": 120, "h": 120, "r": 9})],
                   shots=[cam(WIDE, [960, 560, 1.0]), cam([960, 560, 1.0], [1000, 600, 1.3], at="outdoor|28%", dur=0.5),
                           cam([1000, 600, 1.3], [880, 520, 2.0], at="sleepy|50%", dur=0.7)],
                   sfx=["tink@sleepy|50%"], norecut=True, list_in=True)
    T["s8.l2"] = S("tc_yard", [700, 560, 0.95], [620, 560, 1.0],
                   [], mbx=M("laugh", (1400, 905), 600, look="viewer", prop="carrytree", moves=[mv(0.0, 1.8, (520, 905), walk=True)]),
                   sfx=["step@go|50%"])
    hatch = []
    for i in range(7):
        hatch.append(A(f"ny{i}", "tc_nymph", [980, 640], 0.09, {"hidden": True, "mood": "happy"},
                       sets=[{"at": f"hatches+{0.12 * i:.2f}|{60 + 2 * i}%", "p": {"hidden": False}}],
                       moves=[mv(f"hatches+{0.12 * i:.2f}|{60 + 2 * i}%", 1.0, (760 + i * 70, 560 + (i % 3) * 60), walk=True)]))
    T["s8.l3"] = S("tc_yard", [920, 640, 1.2], [960, 620, 1.35],
                   [A("shrub", "tc_shrub", [900, 905], 1.1, {"spring": 1.0}), ooth([980, 640], 0.5, split=0.0, sets=[set_("hatches|55%", 0.4, split=1.0)]),
                    A("fly", "sp.fly", [1300, 400], 0.18, {}, moves=[mv("eat|80%", 1.0, (1050, 520))])] + hatch,
                   scene_p={"spring": 1.0}, sfx=["pop@hatches|55%", "tink@eat|85%"])
    T["s8.l4"] = {"r": "scene", "scene": "ds_corner", "scene_p": {}, "cam": [720, 520, 1.25], "to": [720, 500, 1.35],
                  "actors": [actor("web", "ds_web", [700, 150], 1.0, {"w": 720, "h": 820}),
                             actor("hero", "carol", [720, 610], 0.6, {"mood": "happy", "look": [0, 0.3], "wave": 0.0},
                                   [{"at": "squish|60%", "dur": 0.3, "p": {"wave": 1.0}}])],
                  "mb": HID, "sfx": ["pop@spider|30%"]}
    for sh in T.values():   # drawn_cast.person takes colour tuples
        for a in sh.get("actors", []):
            if a.get("type") == "person":
                for k in ("body", "hair"):
                    if isinstance(a["p"].get(k), str):
                        h = a["p"][k].lstrip("#")
                        a["p"][k] = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return T
