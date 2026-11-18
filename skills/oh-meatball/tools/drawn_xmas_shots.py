"""The shot table for the 11/25 Christmas-tree flagship (tools/drawn_xmas.py, on the drawn_ranked engine): one recipe
per outline line id, drawn from that line's `vis` note. Keys: drawn_ranked's (f framings, cams, cuts, pose, look,
mb, x, room, roomscene, light, sfx, freak, shake, flash, tint, card, card_at, stamp, ov, act ...) plus the HUD keys
read by drawn_xmas (meter_in, meter_at, meter_big_to, check_at, list_step, tick_at, list_all, no_meter, no_list).

World: the tc_* scenes have the floor at y = 900 (Meatball stands there); in the living room the tree stands at
x = 960 (s 0.8, top near y = 100), the fireplace is at x 1500..2000. Close-ups ("case") sit on tc_bokeh with the
twig at y = 720. Boards (rk_board_bg) are centred on (0, 0).
"""
import drawn_ranked as R
from drawn_kit import hexc

A, lab, popset, stamp = R.A, R.lab, R.popset, R.stamp
YEL, RED, GREEN = R.YEL, R.RED, R.GREEN
FY = 900
TREE_X = 960
CASE_ON_TREE = [1126, 663]


def pop(a, at, dur=0.25):
    """The actor pops in (scale from ~0) at `at`."""
    s = a["s"]
    a["s"] = 0.0005
    a.setdefault("moves", []).insert(0, {"at": at, "dur": dur, "pos": list(a["pos"]), "s": s})
    return a


def tree(idn="tree", x=TREE_X, s=0.8, **p):
    return A(idn, "tc_xtree", [x, FY + 5], s, dict({"deco": 1.0, "lit": 1.0}, **p))


def case_on_tree(idn="oc", s=0.25, **p):
    return A(idn, "tc_ooth", CASE_ON_TREE, s, p, front=True)


def twig(pos=(960, 720), s=1.1, idn="twig", **p):
    return A(idn, "tc_twig", list(pos), s, p)


def ooth(pos=(960, 720), s=1.75, idn="case", **p):
    return A(idn, "tc_ooth", list(pos), s, p)


def prop(idn, kind, pos, s=1.0, front=False, **p):
    a = A(idn, "tc_prop", list(pos), s, dict({"kind": kind}, **p))
    if front:
        a["front"] = True
    return a


def mv(at, dur, pos, **kw):
    return dict({"at": at, "dur": dur, "pos": list(pos)}, **kw)


def st(at, dur=0.3, **p):
    return {"at": at, "dur": dur, "p": p}


def MB(x, y=FY, **kw):
    return dict({"pos": [x, y]}, **kw)


HID = {"hidden": True}
CASE = [twig(), ooth()]


def table():
    T = {}
    # =========================================================================================== 0. cold open
    T["s0.l0"] = dict(room="case", f="kkk", cams=[[960, 470, 1.75, 1.85], [960, 500, 1.05, 1.1], [1250, 520, 1.0, 1.05]],
                      cuts=["check|35%", "toasted|72%"], mb=HID, card_at="check|38%",
                      x=[twig(), ooth(quiver=1.0), A("ring", "ds_ring", [960, 470], 1.0, {"on": 0.0, "r": 280, "lw": 9}, set=[st("check|40%", 0.3, on=1.0)]),
                         A("marsh", "tc_marsh", [2900, 560], 1.25, {}, moves=[mv("toasted|72%", 0.4, [1560, 560])])],
                      sfx=["sting@0.02", "thud@check|40%", "whoosh@toasted|72%"], sheet_at=0.2)
    T["s0.l1"] = dict(room="board", f="kk", cams=[[0, 60, 1.0, 1.05], [-330, 220, 1.7, 1.8]], cuts=["Maybe|55%"], mb=HID,
                      x=[twig([-330, 330], 1.2), ooth([-330, 330], 2.2, xray=0.0, quiver=0.3),
                         A("cnt", "tc_counter", [480, -40], 1.0, {"v": 0.0, "px": 230}, set=[st("hundred|25%", 0.7, v=100.0), st("several|75%", 0.0, text="100+")])],
                      sfx=["whoosh@Inside|5%", "tink@hundred|30%", "pop@several|75%"])
    T["s0.l1"]["x"][1]["set"] = [st("Inside|5%", 0.5, xray=1.0)]
    T["s0.l2"] = dict(room="liv", f="kk", cams=[[1250, 420, 2.0, 2.1], [CASE_ON_TREE[0], 610, 3.6, 3.8]], cuts=["tell|45%"], mb=HID,
                      x=[tree(), prop("thermo", "thermostat", [1250, 420], 0.9, glow=0.0, dial=0.2), case_on_tree(quiver=0.6)],
                      tint=[1.0, 0.55, 0.15, 0.08], sfx=["tink@warm|25%", "crunch@spring|80%"])
    T["s0.l2"]["x"][1]["p"]["glow"] = 0.0
    T["s0.l2"]["x"][1]["set"] = [st("warm|20%", 0.8, glow=1.0, dial=0.9)]
    T["s0.l2"]["x"][2]["set"] = [st("spring|75%", 0.4, crack=1.0)]
    T["s0.l3"] = dict(room="liv", f="Mw", cuts=["toddler|45%"], pose="deadpan", look="viewer", mb=MB(1600),
                      x=[tree(), prop("gift", "gift", [1350, FY], 1.2), lab("gl", "FREE: STARTER PACK", [1350, 640], "starter|60%", px=56, color=YEL)],
                      sfx=["pop@starter|60%"])
    T["s0.l4"] = dict(room="liv", f="kk", cams=[[CASE_ON_TREE[0], 620, 3.0, 3.1], [1150, 520, 0.92, 0.97]], cuts=["Nine|35%"], pose="point", look="tree",
                      mb=MB(1600, moves=[mv("Nine|40%", 0.4, [1560, FY], hop=60)]), card="9 STOWAWAYS", card_at="Nine|45%",
                      x=[tree(qmarks=0.0), case_on_tree()], sfx=["whoosh@Nine|35%", "pop@Nine|45%"])
    T["s0.l4"]["x"][0]["set"] = [st("Nine|40%", 1.4, qmarks=1.0)]
    four = {"type": "four"}
    T["s0.l5"] = dict(room="board", f="kk", cams=[[0, 0, 1.0, 1.03], [0, 60, 1.25, 1.3]], cuts=["outside|70%"], mb=HID, card=False,
                      x=[pop(A("i1", "cellar_spider", [-700, 0], 0.35, {}), "Six|3%"), pop(A("i2", "tc_barkbeetle", [-560, -40], 0.45, {}), "Six|8%"),
                         pop(A("v", "tc_aphid", [-250, -40], 0.55, {}), "vacuum|30%"),
                         pop(twig([150, -110], 0.3, idn="tw"), "clip|50%"), pop(ooth([150, -110], 0.75, idn="c2"), "clip|52%"),
                         pop(A("slf", "tc_slf_eggs", [630, -120], 0.8, {}), "outside|72%"),
                         A("four", "tc_stamps", [0, 0], 1.0, {"n": 0.0, "y": 640, "items": [["IGNORE", "x6", GREEN], ["VACUUM", "x1", YEL],
                                                                                        ["CLIP", "x1", YEL], ["CHECK THE TRUNK", "x1", RED]]},
                           front=True, set=[st("Six|5%", 0.3, n=1.0), st("vacuum|32%", 0.3, n=2.0), st("clip|54%", 0.3, n=3.0), st("outside|75%", 0.3, n=4.0)])],
                      sfx=["stamp@Six|5%", "stamp@vacuum|32%", "stamp@clip|54%", "stamp@outside|75%"])
    T["s0.l6"] = dict(room="liv", f="wM", cuts=["twenty|20%"], pose="shock", look="viewer", mb=MB(1600, gest=[["check|70%", "point", 1.2]]),
                      x=[tree()], card_at="twenty|22%", meter_in="check|62%", shake=["twenty|22%"], burst=True, act="shocked",
                      sfx=["thud@twenty|22%", "boing@thousand|40%"])
    # =========================================================================================== 1. the 25,000 (corkboard)
    T["s1.l0"] = dict(room="cork", f="kM", cams=[[800, 540, 1.0, 1.06]], cuts=["Where|40%"], pose="think", look="viewer", mb=MB(1450, 1500),
                      x=[A("n25", "tc_note", [700, 560], 1.0, {"text": "25,000", "px": 170, "w": 700, "h": 300}),
                         A("str", "tc_string", [1000, 520], 1.0, {"to": [1300, -500], "grow": 0.0}, set=[st("Where|30%", 0.8, grow=1.0)], front=True)],
                      act="curious", sfx=["tink@Where|30%"])
    T["s1.l1"] = dict(room="cork", f="kk", cams=[[700, 540, 1.0, 1.03], [1400, 540, 1.15, 1.2]], cuts=["December|50%"], mb=HID,
                      x=[A("str", "tc_string", [-200, 300], 1.0, {"to": [1000, 160], "grow": 0.0}, set=[st("university|25%", 0.8, grow=1.0)], front=True),
                         A("map", "tc_map", [800, 520], 0.72, {"place": "NORWAY", "pin": 0.0, "px": -60, "py": 40}, set=[st("Norway|30%", 0.5, pin=1.0)]),
                         pop(A("cal", "ds_prop", [1450, 540], 0.95, {"kind": "calendar", "label": "DEC 2012"}), "December|55%")],
                      sfx=["pop@Norway|30%", "pop@December|55%"])
    T["s1.l2"] = dict(room="lab", f="kkk", cams=[[900, 620, 0.95, 1.0], [560, 640, 1.7, 1.75], [1210, 400, 1.5, 1.55]], cuts=["twenty|35%", "trees|72%"], mb=HID,
                      x=[A("sci", "person", [520, 900], 0.62, {"body": hexc("#f4f4f4"), "glasses": "round", "hair": hexc("#6b4a2f"), "mood": "calm", "arm": "point"}, talks=True),
                         pop(A("bub", "tc_speech", [1210, 380], 1.0, {"lines": ["AS MANY AS...", "IN SOME TREES"], "px": 78, "w": 800, "h": 300, "under": 0.0},
                               set=[st("some|80%", 0.5, under=1.0)]), "said|15%")],
                      sfx=["pop@said|15%", "scratch@some|80%"])
    T["s1.l3"] = dict(room="woods", f="kk", cams=[[960, 560, 0.95, 1.0], [1290, 500, 1.4, 1.45]], cuts=["pine|60%"], mb=HID,
                      x=[A("spr", "tc_wild", [640, 920], 0.78, {"kind": "spruce"}), A("pine", "tc_wild", [1290, 920], 0.78, {"kind": "pine"}),
                         lab("l1", "SPRUCE", [640, 290], "Spruce|40%", px=64), lab("l2", "PINE", [1290, 160], "pine|60%", px=64)],
                      sfx=["pop@Spruce|40%", "pop@pine|60%"])
    crit = [("tc_springtail", 0.42), ("tc_barklouse", 0.42), ("tc_mite", 0.32), ("sp.moth", 0.32), ("cellar_spider", 0.22)]
    words = ["Springtails|25%", "bark|42%", "mites|58%", "moth|72%", "spider|88%"]
    names = ["SPRINGTAIL", "BARK LOUSE", "MITE", "MOTH", "SPIDER"]
    xs4 = []
    for i, ((typ, sc), w, nm) in enumerate(zip(crit, words, names)):
        x = 400 + 280 * i
        xs4.append(pop(A(f"c{i}", typ, [x, 600 if typ != "tc_mite" else 560], sc * 1.8, {}), w))
        xs4.append(lab(f"n{i}", nm, [x, 380 + 70 * (i % 2)], w, px=48, color=YEL))
    T["s1.l4"] = dict(room="close", f="kk", cams=[[960, 620, 0.95, 1.0], [900, 600, 1.3, 1.35]], cuts=["moth|70%"], mb=HID,
                      x=[twig([960, 650], 1.3)] + xs4, sfx=["pop@" + w for w in words])
    T["s1.l5"] = dict(room="lab", f="mM", cuts=["couldn't|55%"], pose="nervous", mb=MB(1250, moves=[mv("counted|30%", 0.3, [1300, FY])]),
                      x=[prop("cab", "cabinet", [800, FY], 1.0, open=0.0)],
                      sfx=["thud@couldn't|55%"], **stamp("NO METHOD GIVEN", "behind|75%", RED, 960, 320, 120, -8))
    T["s1.l5"]["x"][0]["set"] = [st("counted|20%", 0.5, open=1.0)]
    T["s1.l5"]["sfx"].append("stamp@behind|75%")
    T["s1.l6"] = dict(room="cork", f="Mk", cams=[[700, 560, 1.4, 1.5]], cuts=["Stellar|65%"], pose="laugh", look="viewer", mb=MB(1450, 1500),
                      x=[A("n25", "tc_note", [700, 560], 1.0, {"text": "25,000", "px": 170, "w": 700, "h": 300, "strike": 0.0}, set=[st("rumor|40%", 0.5, strike=1.0)]),
                         lab("rum", "RUMOR", [700, 330], "rumor|45%", px=110, color=RED)], sfx=["scratch@rumor|40%"])
    T["s1.l7"] = dict(room="cork", f="kk", cams=[[900, 600, 1.0, 1.04], [900, 560, 1.6, 1.65]], cuts=["nobody|45%"], mb=HID,
                      x=[A("map", "tc_map", [900, 520], 0.72, {"place": "NETHERLANDS", "pin": 0.0}, set=[st("Dutch|15%", 0.5, pin=1.0)]),
                         lab("nd", "NO DUTCH NUMBERS", [900, 860], "nobody|50%", px=90, color=YEL)], sfx=["pop@Dutch|15%", "pop@nobody|50%"])
    T["s1.l8"] = dict(room="liv", f="wk", cams=[[1300, 760, 1.6, 1.7]], cuts=["Shake|45%"], pose="present", look="viewer",
                      mb=MB(1450, prop="smalltree"), x=[tree(), prop("sheet", "sheet", [1300, FY + 20], 1.2), A("fall", "tc_fall", [1300, FY + 10], 1.0, {"on": 0.0, "w": 400, "h": 400, "n": 18}, set=[st("Shake|50%", 0.3, on=1.0)])],
                      sfx=["whoosh@Shake|50%"])
    T["s1.l9"] = dict(room="board", f="kk", cams=[[0, 0, 1.0, 1.04], [0, -40, 1.35, 1.4]], cuts=["several|60%"], mb=HID,
                      x=[A("big", "tc_note", [-450, -60], 1.0, {"text": "25,000", "px": 150, "w": 620, "h": 260, "strike": 0.0}, set=[st("buggy|20%", 0.4, strike=1.0)]),
                         A("ctr", "tc_counter", [300, -40], 1.0, {"text": "A FEW", "px": 110, "on": 0.0}, set=[st("few|40%", 0.3, on=1.0), st("several|60%", 0.0, text="SEVERAL HUNDRED", px=80)]),
                         lab("ia", "IOWA STATE", [300, 180], "Iowa|10%", px=60, color=YEL)],
                      sfx=["scratch@buggy|20%", "tink@several|60%"])
    T["s1.l10"] = dict(room="farm", f="kk", cams=[[960, 600, 0.6, 0.62], [1300, 700, 1.6, 1.7]], cuts=["thousand|60%"], mb=HID,
                       x=[A("glow", "rk_glow", [1300, 760], 1.0, {"r": 120, "on": 0.0}, front=True, set=popset("thousand|50%", dur=0.5))],
                       sfx=["tink@thousand|55%"])
    T["s1.l11"] = dict(room="woods", f="kkkk", cams=[[1100, 560, 0.8, 0.84], [700, 600, 1.1, 1.15], [700, 520, 1.6, 1.65], [1500, 600, 1.1, 1.15]], cuts=["Washington|20%", "forest|45%", "farm|72%"], mb=HID,
                       x=[A("wild", "tc_wild", [700, 920], 0.78, {"kind": "spruce"}), A("sp", "tc_specks", [700, 600], 1.0, {"n": 14, "w": 360, "h": 420}),
                          A("ft", "tc_farmtree", [1500, 920], 0.8, {}), lab("w1", "FOREST: MORE LIKELY", [700, 330], "forest|45%", px=60, color=YEL),
                          lab("w2", "FARM-GROWN", [1500, 330], "farm|78%", px=60, color=GREEN)], act="curious", sfx=["pop@forest|45%", "pop@farm|78%"])
    T["s1.l12"] = dict(room="farm", f="kk", cams=[[960, 640, 0.9, 0.95], [1100, 800, 2.0, 2.1]], cuts=["Insects|45%"], mb=HID,
                       x=[A("zs", "tc_specks", [1100, 820], 1.0, {"n": 8, "w": 260, "h": 120, "sleep": 1.0})], roomscene="tc_farm", sfx=["pop@winter|80%"])
    T["s1.l13"] = dict(room="liv", f="kw", cams=[[960, 500, 1.0, 1.05]], cuts=["winter|55%"], pose="shock", look="tree",
                       mb=MB(1600), x=[tree(zs=1.0)], tint=[1.0, 0.55, 0.15, 0.08], sfx=["pop@heat|40%", "pop@over|80%"])
    T["s1.l13"]["x"][0]["set"] = [st("heat|35%", 1.2, zs=0.0)]
    T["s1.l14"] = dict(room="liv", f="Mk", cams=[[CASE_ON_TREE[0], 630, 3.2, 3.4]], cuts=["stowaway|55%"], pose="you", look="viewer",
                       mb=MB(1600), x=[tree(), case_on_tree()], sfx=["sting@stowaway|55%"])
    # =========================================================================================== 2. the mantis egg case
    M_ON_TWIG = [700, 720]
    T["s2.l0"] = dict(room="case", f="kk", cams=[[760, 520, 1.1, 1.15], [960, 560, 1.6, 1.7]], cuts=["egg|55%"], mb=HID,
                      x=[twig(), ooth(), A("man", "tc_mantis", [560, 720], 0.6, {"look": [1, -0.2]})], ring_k=True)
    T["s2.l1"] = dict(room="case", f="kk", cams=[[860, 600, 1.2, 1.25], [960, 580, 1.5, 1.6]], cuts=["hardens|60%"], mb=HID,
                      x=[twig(), ooth(grow=0.0, wet=1.0), A("man", "tc_mantis", [560, 720], 0.6, {"lay": 1.0})],
                      sfx=["scratch@glues|35%", "tink@hardens|70%"])
    T["s2.l1"]["x"][1]["set"] = [st("blob|30%", 1.0, grow=1.0), st("hardens|60%", 0.8, wet=0.0)]
    T["s2.l2"] = dict(room="case", f="kk", cams=[[960, 600, 1.0, 1.05], [1150, 640, 1.4, 1.45]], cuts=["Light|50%"], mb=HID,
                      x=[twig(), ooth(), prop("foam", "foamcan", [1500, 860], 0.8),
                         prop("rul", "ruler", [960, 860], 1.2, w=700, mark=0.0, span=300, label="1.5 INCHES")],
                      sfx=["pop@spray|20%", "tink@inch|80%"])
    T["s2.l2"]["x"][3]["set"] = [st("inch|70%", 0.5, mark=1.0)]
    T["s2.l3"] = dict(room="case", f="kk", cams=[[1100, 560, 1.1, 1.15], [1300, 560, 1.6, 1.7]], cuts=["ping|55%"], mb=HID,
                      x=[twig(), ooth(), A("pp", "tc_prop", [2600, 600], 1.6, {"kind": "pingpong"}, moves=[mv("ping|50%", 0.6, [1450, 600], rot=360)]),
                         lab("cm", "CHINESE MANTIS", [1100, 330], "Chinese|30%", px=70, color=YEL)], sfx=["boing@ping|55%"])
    T["s2.l4"] = dict(room="liv", f="Mk", cams=[[CASE_ON_TREE[0], 640, 3.0, 3.2]], cuts=["Wedged|55%"], pose="deadpan", look="viewer",
                      mb=MB(1600), x=[tree(), case_on_tree(s=0.32)], sfx=["boing@babies|30%"])
    T["s2.l5"] = dict(room="closeG", f="kk", cams=[[960, 600, 1.1, 1.15], [960, 620, 1.7, 1.8]], cuts=["Half|45%"], mb=HID,
                      x=[twig(), ooth(kind="carolina", s=1.6), lab("cl", "CAROLINA MANTIS", [960, 380], "Carolina|20%", px=70, color=GREEN),
                         lab("cn", "NATIVE", [960, 470], "native|10%", px=56, color="#ffffff")], sfx=["pop@Carolina|20%"])
    T["s2.l5"]["x"][1]["s"] = 1.6
    T["s2.l6"] = dict(room="close", f="kk", cams=[[960, 560, 0.85, 0.9], [700, 560, 1.4, 1.45]], cuts=["leave|60%"], mb=HID,
                      x=[twig([960, 720], 1.4)] + [pop(A(f"m{k}", "tc_mantis", [300 + 440 * k, 720], 0.32, {"col": ["#7fbf4a", "#b9a36b", "#9ccf6a", "#8fae5a"][k]}), f"four|{20 + 8 * k}%") for k in range(4)]
                      + [pop(ooth([440 + 440 * k, 720], 0.6, idn=f"o{k}"), f"leave|{55 + 6 * k}%") for k in range(4)],
                      sfx=["pop@four|20%", "pop@four|28%", "pop@four|36%", "pop@four|44%"])
    T["s2.l7"] = dict(room="lot", f="kk", cams=[[960, 560, 0.9, 0.95], [700, 520, 1.6, 1.7]], cuts=["Fraser|50%"], mb=HID,
                      x=[A("ft", "tc_farmtree", [700, 920], 0.8, {}), lab("fr", "FRASER FIR", [700, 140], "Fraser|50%", px=80, color=YEL),
                         pop(A("man", "tc_mantis", [800, 600], 0.25, {}), "prefer|40%")], sfx=["pop@Fraser|50%"])
    T["s2.l8"] = dict(room="liv", f="Mw", cuts=["Fir|65%"], pose="laugh", look="viewer", mb=MB(1600), x=[tree()],
                      ov=[{"type": "big", "at": "Fir|65%", "rows": [["FIR SNOBS", 120, YEL]], "x": 960, "y": 240}], sfx=["pop@Fir|65%"])
    T["s2.l9"] = dict(room="board", f="kkk", cams=[[-300, 0, 1.3, 1.35], [300, 0, 1.3, 1.35], [0, 0, 0.9, 0.95]], cuts=["Mississippi|50%", "several|78%"], mb=HID,
                      x=[A("s1", "ds_chip_src", [-300, -150], 1.0, {"text": "MISSOURI EXTENSION", "px": 52}),
                         A("c1", "tc_counter", [-300, 60], 1.0, {"v": 0, "px": 150, "fmt": "~{}", "on": 0.0}, set=[st("about|25%", 0.2, on=1.0), st("hundred|30%", 0.6, v=100)]),
                         A("s2", "ds_chip_src", [300, -150], 1.0, {"text": "MISSISSIPPI STATE", "px": 52}),
                         A("c2", "tc_counter", [300, 60], 1.0, {"v": 0, "px": 110, "fmt": "{}", "text": "SEVERAL HUNDRED", "on": 0.0}, set=[st("several|75%", 0.3, on=1.0)])],
                      act="curious", sfx=["tink@hundred|30%", "pop@several|75%"])
    T["s2.l10"] = dict(room="liv", f="kM", cams=[[CASE_ON_TREE[0], 630, 3.2, 3.4]], cuts=["depending|60%"], pose="present", mb=MB(1600),
                       x=[tree(), case_on_tree(s=0.3, xray=1.0)])
    T["s2.l11"] = dict(room="close", f="kk", cams=[[960, 600, 1.2, 1.25], [960, 600, 1.5, 1.55]], cuts=["spring|60%"], mb=HID,
                       x=[twig(snow=1.0), ooth(), A("pg", "tc_pages", [960, 300], 0.45, {"on": 1.0, "n": 6})], roomscene="tc_bokeh")
    T["s2.l12"] = dict(room="liv", f="kkM", cams=[[CASE_ON_TREE[0], 640, 2.8, 2.9], [1000, 560, 1.1, 1.15]], cuts=["hatches|45%", "dozens|75%"],
                       pose="shock", mb=MB(1600), act="shocked", burst=True, freak=["dozens|75%"],
                       x=[tree(), case_on_tree(s=0.3, split=0.0)] + [A(f"ny{k}", "tc_nymph", [CASE_ON_TREE[0], 660], 0.0005, {},
                                                                        moves=[mv(f"hatches|{50 + 3 * k}%", 1.4, [860 + 90 * k, 500 + 130 * (k % 3)], s=0.13)]) for k in range(8)],
                       sfx=["crunch@hatches|45%", "sting@dozens|75%"])
    T["s2.l12"]["x"][1]["set"] = [st("hatches|45%", 0.4, split=1.0)]
    T["s2.l13"] = dict(room="board", f="kk", cams=[[0, 0, 1.0, 1.05], [100, 100, 1.35, 1.4]], cuts=["photo|60%"], mb=HID,
                       x=[A("race", "tc_race", [-500, -100], 1.0, {"a": 0.0, "b": 0.0, "la": "TREE DOWN", "lb": "EGGS HATCH", "w": 1100},
                            set=[st("three|20%", 2.2, a=0.95, b=0.93)]),
                          lab("wk", "3-4 WEEKS", [0, 260], "weeks|30%", px=90, color=YEL)], sfx=["whoosh@three|20%", "hit@photo|70%"])
    T["s2.l14"] = dict(room="liv", f="kk", cams=[[1250, 820, 1.6, 1.7], [1450, 820, 1.6, 1.7]], cuts=["eat|50%"], mb=HID,
                       x=[tree(), A("ny", "tc_nymph", [1150, FY - 10], 0.12, {}, moves=[mv("nothing|30%", 1.8, [1400, FY - 10], walk=True)]),
                          prop("cc", "candycane", [1300, FY], 0.6), prop("sock", "sock", [1500, FY], 0.6)], light={"kind": "lamp", "dark": 0.4, "target": [1350, 820]})
    T["s2.l15"] = dict(room="close", f="kM", cams=[[960, 620, 1.6, 1.7]], cuts=["other|65%"], pose="shock", mb=MB(1550, 1300), act="shocked",
                       x=[twig(), A("n1", "tc_nymph", [780, 720], 0.25, {}), A("n2", "tc_nymph", [1140, 720], 0.25, {}, flip=True)], burst=True,
                       sfx=["sting@other|65%"])
    T["s2.l16"] = dict(room="liv", f="Mw", cuts=["siblings|55%"], pose="deadpan", look="viewer", mb=MB(1600), x=[tree()],
                       light={"kind": "lamp", "dark": 0.35})
    T["s2.l17"] = dict(room="liv", f="kM", cams=[[1120, 520, 2.4, 2.5]], cuts=["starve|60%"], pose="nervous", mb=MB(1600),
                       x=[tree(), A("ba", "tc_bauble", [1120, 380], 0.6, {"col": "#c0392b"}), A("ny", "tc_nymph", [1120, 470], 0.07, {})])
    T["s2.l18"] = dict(room="liv", f="kw", cams=[[1400, 760, 1.5, 1.6]], cuts=["crickets|65%"], pose="present", mb=MB(1650, prop="tweezers"),
                       x=[tree()] + [A(f"ny{k}", "tc_nymph", [1200 + 80 * k, FY], 0.1, {"napkin": 1.0}) for k in range(4)] +
                         [prop("tub", "tub", [1500, FY], 0.6, label="CRICKETS")], sfx=["pop@crickets|65%"])
    T["s2.l19"] = dict(room="liv", f="M", pose="point", look="viewer", mb=MB(1600, gest=[["making|40%", "you", 1.0]]),
                       x=[tree()], card="UNIVERSITY OF MISSOURI EXTENSION", card_at="0%")
    T["s2.l20"] = dict(room="liv", f="Mk", cams=[[1250, 820, 1.5, 1.6]], cuts=["daycare|50%"], pose="laugh", look="viewer", mb=MB(1600),
                       x=[tree()] + [A(f"ny{k}", "tc_nymph", [1050 + 90 * k, FY], 0.1, {}) for k in range(5)] +
                         [lab("dc", "TINY CANNIBAL DAYCARE", [1250, 560], "daycare|55%", px=60, color=YEL)], sfx=["pop@daycare|55%"])
    T["s2.l21"] = dict(room="liv", f="wk", cams=[[CASE_ON_TREE[0], 630, 2.6, 2.7]], cuts=["marshmallow|60%"], pose="point", look="tree", mb=MB(1600, prop="magnifier"),
                       x=[tree(), case_on_tree()], check_at="Step|30%", sfx=["pop@marshmallow|60%"])
    T["s2.l22"] = dict(room="case", f="kkk", cams=[[960, 560, 1.2, 1.25], [960, 560, 1.2, 1.25], [1100, 700, 1.5, 1.55]], cuts=["crush|30%", "Clip|65%"], mb=HID,
                       x=[twig(), ooth(), A("sl", "tc_prop", [1350, 520], 1.0, {"kind": "slipper"}, moves=[mv(0.1, 0.4, [1250, 440])]),
                          A("x", "ds_cross", [1250, 440], 1.0, {"on": 0.0, "r": 200}, set=popset("crush|30%"), front=True),
                          A("sh", "tc_prop", [1500, 760], 1.2, {"kind": "shears", "snip": 0.0}, set=[st("twig|80%", 0.2, snip=1.0)], front=True)],
                       sfx=["stamp@crush|30%", "click@twig|80%"])
    T["s2.l23"] = dict(room="yard", f="wk", cams=[[900, 700, 1.6, 1.7]], cuts=["evergreen|50%"], pose="present", look=[900, 650],
                       mb=MB(1250, prop="twig", moves=[mv("Tuck|10%", 0.8, [1150, FY], walk=True)]),
                       x=[A("sh", "tc_shrub", [800, FY], 0.9, {"snow": 0.6}), pop(A("tw", "tc_prop", [880, 640], 0.5, {"kind": "shrubtwig"}), "evergreen|60%")],
                       check_at="evergreen|55%", sfx=["pop@evergreen|60%"])
    T["s2.l24"] = dict(room="yard", f="kM", cams=[[700, 820, 1.8, 1.9]], cuts=["eggs|70%"], pose="nervous", mb=MB(1250),
                       x=[A("tw", "tc_prop", [700, FY], 0.6, {"kind": "shrubtwig"}, moves=[mv("ants|50%", 0.5, [700, 680])]),
                          A("ants", "tc_crawlers", [300, FY], 1.0, {"u": 0.0, "n": 10, "len": 380, "col": "#2a1a10"}, set=[st("Not|10%", 2.0, u=1.0)]),
                          A("x", "ds_cross", [700, 820], 1.0, {"on": 0.0, "r": 160}, set=popset("ground|25%"), front=True)],
                       sfx=["stamp@ground|25%"])
    T["s2.l25"] = dict(room="board", f="kk", cams=[[0, 0, 1.0, 1.04], [0, 0, 1.4, 1.45]], cuts=["big|60%"], mb=HID,
                       x=[A("map", "tc_map", [0, 0], 1.0, {"place": "USA", "ships": 0.0}, set=[st("from|60%", 1.2, ships=1.0)])], sfx=["whoosh@from|60%"])
    T["s2.l26"] = dict(room="board", f="kkk", cams=[[0, 0, 1.0, 1.04], [-230, 20, 1.5, 1.55], [450, 20, 1.5, 1.55]], cuts=["European|30%", "Illinois|55%"], mb=HID,
                       x=[lab("t", "LATE 1800s", [0, -240], "1800s|30%", px=100, color=YEL),
                          A("m1", "tc_mantis", [-450, 120], 0.38, {"col": "#9ccf6a"}), lab("l1", "CHINESE", [-450, -120], "Chinese|10%", px=50),
                          A("m2", "tc_mantis", [0, 120], 0.38, {"col": "#b9a36b"}), lab("l2", "EUROPEAN", [0, -120], "European|20%", px=50),
                          A("m3", "tc_mantis", [450, 120], 0.38, {"col": "#7fbf4a"}), lab("l3", "CAROLINA: NATIVE", [450, -120], "Carolina|70%", px=50, color=GREEN)],
                       sfx=["pop@1800s|30%", "pop@Carolina|70%"])
    # =========================================================================================== 3. the giant conifer aphid (living room)
    def aph(idn, pos, s=0.35, **kw):
        return A(idn, "tc_aphid", list(pos), s, {}, **kw)
    T["s3.l0"] = dict(room="liv", f="kk", cams=[[1200, 820, 1.7, 1.8], [1150, 760, 1.2, 1.25]], cuts=["tick|60%"], mb=HID,
                      x=[tree(), aph("a", [1000, FY - 30], 0.3, moves=[mv(0.6, 2.5, [1250, FY - 30], walk=True)])], sfx=["scratch@tick|60%"])
    T["s3.l1"] = dict(room="liv", f="kk", cams=[[1200, 760, 1.5, 1.6], [1180, 840, 2.4, 2.5]], cuts=["Walking|50%"], mb=HID,
                      x=[tree()] + [aph(f"a{k}", [1050 + 80 * k, 600], 0.18, moves=[mv(f"Long|{20 + 8 * k}%", 0.6, [1050 + 80 * k, FY - 40 - 20 * (k % 2)])]) for k in range(4)],
                      sfx=["thud@Dark|10%", "thud@Round|25%", "scratch@Walking|55%"])
    T["s3.l2"] = dict(room="liv", f="Mw", cuts=["Very#3|65%"], pose="deadpan", look="viewer", mb=MB(1600), x=[tree(), aph("a", [1250, FY - 30], 0.25)])
    T["s3.l3"] = dict(room="close", f="kk", cams=[[900, 600, 1.2, 1.25], [900, 600, 1.6, 1.7]], cuts=["Up|50%"], mb=HID,
                      x=[twig([960, 720], 1.0), aph("a", [900, 700], 0.8),
                         prop("rul", "ruler", [900, 830], 1.0, w=700, mark=0.0, span=420, label="UP TO 1/8 INCH")], ring_k=True, sfx=["tink@eighth|80%"])
    T["s3.l3"]["x"][2]["set"] = [st("eighth|70%", 0.5, mark=1.0)]
    T["s3.l4"] = dict(room="board", f="kk", cams=[[0, 0, 1.0, 1.04], [100, 60, 1.25, 1.3]], cuts=["largest|50%"], mb=HID,
                      x=[A("big", "tc_aphid", [-300, 150], 0.9, {"flex": 0.0}, set=[st("largest|50%", 0.5, flex=1.0)]),
                         A("small", "tc_aphid", [450, 150], 0.25, {"col": "#7fbf4a"}), lab("l1", "GIANT CONIFER APHID", [-300, -300], "N.C.|10%", px=64, color=YEL),
                         lab("l2", "A NORMAL APHID", [450, 0], "largest|60%", px=48)], sfx=["boing@largest|50%"])
    T["s3.l5"] = dict(room="board", f="kk", cams=[[0, 0, 1.0, 1.05], [0, 0, 1.3, 1.35]], cuts=["ticks|70%"], mb=HID,
                      x=[A("ap", "tc_aphid", [-420, 150], 0.7, {}), A("tk", "tc_tick_top", [420, 0], 0.8, {}),
                         A("lens", "tc_prop", [0, -40], 1.4, {"kind": "lens"}, moves=[mv("mistake|50%", 0.8, [380, -40])], front=True)],
                      sfx=["whoosh@mistake|50%"])
    T["s3.l6"] = dict(room="board", f="kk", cams=[[0, 0, 1.0, 1.04], [400, 0, 1.4, 1.45]], cuts=["Ticks|60%"], mb=HID,
                      x=[A("ap", "tc_aphid", [-420, 0], 0.8, {"top": True, "count": 0.0}, set=[st("aphid|25%", 1.2, count=6.0)]),
                         A("tk", "tc_tick_top", [420, 0], 0.8, {"count": 0.0}, set=[st("eight|70%", 1.4, count=8.0)])],
                      sfx=["tink@six|30%", "tink@eight|75%"])
    T["s3.l7"] = dict(room="liv", f="Mk", cams=[[1250, 780, 1.8, 1.9]], cuts=["aphid|55%"], pose="facepalm", look="viewer", mb=MB(1600),
                      x=[tree(), aph("a", [1250, FY - 30], 0.3)])
    T["s3.l8"] = dict(room="board", f="kk", cams=[[0, 0, 1.0, 1.04], [500, 0, 1.4, 1.45]], cuts=["houseplants|70%"], mb=HID,
                      x=[A("i1", "tc_prop", [-600, -60], 1.4, {"kind": "icon", "icon": "tooth", "x": 0.0}, set=[st("bite|30%", 0.3, x=1.0)]),
                         A("i2", "tc_prop", [-200, -60], 1.4, {"kind": "icon", "icon": "sting", "x": 0.0}, set=[st("sting|40%", 0.3, x=1.0)]),
                         A("i3", "tc_prop", [200, -60], 1.4, {"kind": "icon", "icon": "germ", "x": 0.0}, set=[st("disease|50%", 0.3, x=1.0)]),
                         A("pl", "tc_prop", [600, 200], 1.0, {"kind": "plant"}), pop(A("ok", "tc_tick", [700, -80], 1.0, {}), "houseplants|80%")],
                      sfx=["stamp@bite|30%", "stamp@sting|40%", "stamp@disease|50%", "pop@houseplants|80%"])
    T["s3.l9"] = dict(room="liv", f="kk", cams=[[1100, 620, 1.8, 1.9], [1150, 560, 1.2, 1.25]], cuts=["wander|55%"], mb=HID,
                      x=[tree()] + [aph(f"a{k}", [1050 + 50 * k, 560 + 60 * k], 0.12, moves=[mv("wander|50%", 2.0, [1350 + 60 * k, 560 + 60 * k], walk=True)]) for k in range(3)])
    T["s3.l10"] = dict(room="liv", f="kk", cams=[[1150, 560, 1.0, 1.05], [1500, 800, 1.6, 1.7]], cuts=["furniture|60%"], mb=HID,
                       x=[tree(), prop("chair", "armchair", [1600, FY], 1.0)] + [aph(f"a{k}", [1150 + 40 * k, 480], 0.12, moves=[mv("furniture|50%", 1.2, [1500 + 60 * k, 760])]) for k in range(3)],
                       sfx=["whoosh@furniture|55%"])
    T["s3.l11"] = dict(room="liv", f="wM", cuts=["squash|55%"], pose="shock", look="viewer", act="shout", burst=True,
                       mb=MB(1550, prop="slipper", shake=0.6), x=[tree(), aph("a", [1250, FY - 30], 0.3)],
                       **stamp("DON'T SQUASH", "squash|60%", RED, 960, 400, 150, -8), sfx=["stamp@squash|60%"])
    T["s3.l12"] = dict(room="board", f="kk", cams=[[0, 0, 1.0, 1.04], [300, 120, 1.5, 1.55]], cuts=["Carpet|55%"], mb=HID, roomscene="rk_board_bg",
                       x=[A("gift", "tc_prop", [-400, 150], 1.6, {"kind": "gift", "stain": 0.0}, set=[st("purple|30%", 0.6, stain=1.0)]),
                          A("rug", "tc_stain", [400, 180], 2.0, {"grow": 0.0, "rug": True}, set=[st("Carpet|55%", 0.8, grow=1.0)])],
                       card_y=150, sfx=["tink@purple|30%"])
    T["s3.l13"] = dict(room="liv", f="kk", cams=[[1350, 760, 1.4, 1.45], [1200, 820, 1.9, 2.0]], cuts=["brush|60%"], mb=HID,
                       x=[tree(), prop("vac", "canvac", [1700, FY], 1.0, suck=1.0, tip=[-400, -80]), aph("a", [1280, FY - 70], 0.2),
                          prop("bh", "brushhead", [1100, FY], 0.8), A("x", "ds_cross", [1100, 820], 1.0, {"on": 0.0, "r": 140}, set=popset("brush|65%"), front=True)],
                       check_at="instead|35%", sfx=["whoosh@hose|45%", "stamp@brush|65%"])
    T["s3.l13"]["x"][2]["moves"] = [mv("hose|40%", 0.5, [1310, FY - 80], s=0.02)]
    T["s3.l14"] = dict(room="liv", f="kk", cams=[[900, 480, 0.85, 0.9], [950, 430, 1.5, 1.6]], cuts=["breed|60%"], mb=HID,
                       x=[A("rb", "tc_rootball", [900, FY], 1.0, {})] + [pop(A(f"w{k}", "tc_aphid", [800 + 120 * k, 450], 0.12, {"winged": 1.0}), f"breed|{65 + 5 * k}%") for k in range(3)] +
                         [lab("q", "?", [1100, 330], "breed|75%", px=140, color=YEL)], sfx=["pop@breed|65%"])
    T["s3.l15"] = dict(room="trunk", f="kk", cams=[[960, 540, 1.0, 1.05], [960, 540, 1.8, 1.9]], cuts=["few#2|75%"], mb=HID,
                       x=[A("tk", "tc_tick_top", [960, 560], 0.35, {}), lab("rare", "RARE", [960, 400], "recorded|50%", px=80, color=GREEN)],
                       act="curious", sfx=["pop@recorded|55%"])
    T["s3.l16"] = dict(room="board", f="kk", cams=[[0, 0, 1.0, 1.04], [500, 0, 1.4, 1.45]], cuts=["matters|70%"], mb=HID,
                       x=[A("strip", "tc_strip", [0, 0], 1.0, {"done": 1.0, "blur": 0.0, "glow9": 0.0},
                            set=[st("two|10%", 0.4, done=2.0), st("next|30%", 1.6, blur=1.0), st("matters|70%", 0.6, glow9=1.0)])],
                       sfx=["tink@two|10%", "whoosh@next|30%", "sting@matters|70%"])
    # =========================================================================================== 4. 3 to 8: the ones you can ignore
    IGN = lambda at, x=1150, y=430: stamp("IGNORE", at, GREEN, x, y, 130, -8)  # noqa: E731
    T["s4.l0"] = dict(room="closeG", f="kk", cams=[[960, 600, 1.2, 1.25], [960, 600, 1.7, 1.8]], cuts=["Iowa|35%"], mb=HID,
                      x=[twig(), A("sp", "cellar_spider", [800, 690], 0.5, {}), A("sl", "tc_spiderlings", [1150, 660], 1.8, {})], ring_k=True)
    T["s4.l1"] = dict(room="liv", f="kk", cams=[[1200, 760, 1.4, 1.5], [1100, 600, 1.0, 1.05]], cuts=["die|55%"], mb=HID,
                      x=[tree(), A("dog", "tc_dog", [1350, FY], 0.6, {"sniff": 1.0, "wag": 1.0}, flip=True)])
    T["s4.l2"] = dict(room="trunk", f="kk", cams=[[960, 520, 1.6, 1.7], [960, 900, 1.6, 1.7]], cuts=["sawdust|55%"], mb=HID,
                      x=[A("bb", "tc_barkbeetle", [960, 520], 0.6, {}), A("sd", "tc_sawdust", [960, 1000], 1.4, {"drift": 1.0})], ring_k=True)
    T["s4.l3"] = dict(room="liv", f="kM", cams=[[1450, 780, 1.6, 1.7]], cuts=["damp|55%"], pose="shrug", mb=MB(1650), act="curious",
                      x=[tree(), prop("tab", "table", [1400, FY], 1.0), A("bb", "tc_barkbeetle", [1300, FY], 0.15, {}, moves=[mv("No|30%", 0.8, [1000, FY], face=-1)])])
    T["s4.l4"] = dict(room="trunk", f="kk", cams=[[960, 540, 1.2, 1.25], [960, 540, 1.8, 1.9]], cuts=["Adelgids|50%"], mb=HID,
                      x=[A("ad", "tc_adelgid", [960, 540], 1.4, {"poke": 0.0}, set=[st("stay|65%", 0.5, poke=1.0)])], **IGN("harmless|80%", 960, 280),
                      sfx=["stamp@harmless|80%"])
    T["s4.l5"] = dict(room="liv", f="kk", cams=[[300, 520, 1.6, 1.7], [300, 520, 2.2, 2.3]], cuts=["Wipe|65%"], mb=HID,
                      x=[tree(), A("cr", "tc_crawlers", [100, 590], 1.0, {"u": 0.0, "n": 12, "len": 380, "gone": 0.0}, set=[st("walking|25%", 2.0, u=1.0), st("Wipe|75%", 0.8, gone=1.0)]),
                         A("cl", "tc_prop", [-300, 560], 1.0, {"kind": "cloth"}, moves=[mv("Wipe|70%", 0.8, [600, 560])], front=True)],
                      **IGN("towel|90%", 300, 260), sfx=["whoosh@Wipe|70%", "stamp@towel|90%"])
    T["s4.l6"] = dict(room="close", f="kk", cams=[[960, 600, 1.3, 1.35], [960, 600, 1.9, 2.0]], cuts=["predatory|50%"], mb=HID,
                      x=[twig(), A("mi", "tc_mite", [960, 640], 0.8, {"eat": 1.0})], ring_k=True, **IGN("bite|85%", 960, 260), sfx=["stamp@bite|85%"])
    T["s4.l7"] = dict(room="liv", f="wk", cams=[[1000, 450, 1.6, 1.7]], cuts=["Nests|55%"], pose="present", look="tree",
                      mb=MB(1450, prop="tongs_nest", moves=[mv("take|35%", 0.6, [1350, FY])]), x=[tree(), A("nest", "tc_nest", [1000, 470], 0.4, {}, set=[st("take|35%", 0.0, hidden=True)])],
                      check_at="out|45%")
    T["s4.l8"] = dict(room="liv", f="kk", cams=[[600, 700, 1.6, 1.7], [600, 700, 2.2, 2.3]], cuts=["dry|60%"], mb=HID,
                      x=[tree(), A("bl", "tc_barklouse", [600, 760], 0.3, {}, set=[st("kills|70%", 0.0, hidden=True)]),
                         A("sp", "tc_specks", [600, 700], 1.0, {"n": 10, "w": 300, "h": 100, "col": "#e8e0c8"}, set=[st("kills|70%", 0.0, hidden=True)])],
                      **IGN("quickly|85%", 600, 260), tint=[1.0, 0.6, 0.3, 0.1], sfx=["stamp@quickly|85%"])
    T["s4.l9"] = dict(room="close", f="kk", cams=[[960, 640, 1.3, 1.35], [960, 680, 1.9, 2.0]], cuts=["honeydew|65%"], mb=HID,
                      x=[twig(), A("cr", "tc_crawlers", [700, 700], 1.0, {"u": 0.4, "n": 6, "len": 500}),
                         A("drop", "droplets", [960, 780], 0.6, {"n": 4, "r": 120})], act="curious")
    T["s4.l10"] = dict(room="board", f="kk", cams=[[0, 0, 1.0, 1.03], [0, 0, 1.25, 1.3]], cuts=["multiply|60%"], mb=HID,
                       x=[A(f"s{k}", t_, [-750 + 300 * k, 60], sc, {}) for k, (t_, sc) in enumerate(
                           [("cellar_spider", 0.25), ("tc_barkbeetle", 0.4), ("tc_adelgid", 0.6), ("tc_crawlers", 1.0), ("tc_mite", 0.4), ("tc_barklouse", 0.4)])] +
                         [lab(f"x{k}", "IGNORE", [-750 + 300 * k, 260], f"{20 + 12 * k}%", px=60, color=GREEN) for k in range(6)],
                       sfx=[f"stamp@{20 + 12 * k}%" for k in range(0, 6, 2)])
    T["s4.l11"] = dict(room="board", f="kk", cams=[[0, 0, 1.4, 1.45], [0, 0, 2.2, 2.3]], cuts=["sixteenth|55%"], mb=HID,
                       x=[prop("rice", "grain", [-120, 0], 1.0), A("sl", "tc_spiderlings", [170, 0], 0.6, {"n": 1}), A("ap", "tc_aphid", [300, 20], 0.1, {})],
                       card_y=150)
    T["s4.l12"] = dict(room="liv", f="kk", cams=[[960, 560, 1.0, 1.05], [960, 560, 1.3, 1.35]], cuts=["dry|55%"], mb=HID,
                       x=[tree()] + [A(f"s{k}", t_, [700 + 130 * k, FY - 10], 0.12, {}, set=[st(f"dry|{55 + 5 * k}%", 0.0, hidden=True)]) for k, t_ in
                                     enumerate(["cellar_spider", "tc_barkbeetle", "tc_mite", "tc_barklouse", "tc_aphid"])], tint=[1.0, 0.6, 0.3, 0.12])
    T["s4.l13"] = dict(room="liv", f="Mw", cuts=["Dry|55%"], pose="laugh", look="viewer", mb=MB(1600), x=[tree()],
                       ov=[{"type": "big", "at": "worst|30%", "rows": [["1 STAR", 130, YEL], ["DRY · FOODLESS · TERRIBLE", 70, "#ffffff"]], "x": 900, "y": 230}],
                       sfx=["pop@worst|30%"])
    T["s4.l14"] = dict(room="liv", f="wk", cams=[[1200, 200, 1.4, 1.5]], cuts=["vacuum|65%"], pose="point", look=[1200, 150],
                       mb=MB(1450, prop="hose"), x=[tree(), A("sp", "tc_specks", [1200, 150], 1.0, {"n": 3, "w": 60, "h": 40, "col": "#2a2018"})])
    # =========================================================================================== 5. the spotted lanternfly (the trunk)
    T["s5.l0"] = dict(room="trunk", f="kk", pans=[[960, 200, 1.0], [960, 900, 1.1]], cams=[[960, 300, 1.0, 1.05], [960, 700, 1.6, 1.7]],
                      cuts=["county|60%"], mb=HID, x=[A("slf", "tc_slf_eggs", [960, 760], 0.9, {})], sfx=["sting@county|60%"])
    T["s5.l1"] = dict(room="trunk", f="kk", cams=[[960, 700, 1.4, 1.45], [960, 700, 2.0, 2.1]], cuts=["unlikely|50%"], mb=HID,
                      x=[A("slf", "tc_slf_eggs", [960, 760], 0.9, {})], ring_k=True)
    T["s5.l2"] = dict(room="trunk", f="kk", cams=[[960, 740, 2.0, 2.1], [960, 740, 2.6, 2.7]], cuts=["mud|60%"], mb=HID,
                      x=[A("slf", "tc_slf_eggs", [960, 760], 0.9, {}), lab("mud", "LOOKS LIKE DRIED MUD", [960, 560], "mud|60%", px=44, color=YEL)], ring_k=True)
    T["s5.l3"] = dict(room="liv", f="kk", cams=[[250, 520, 1.8, 1.9], [250, 520, 2.4, 2.5]], cuts=["die|60%"], mb=HID,
                      x=[tree(), A("ny", "tc_slf_nymphs", [250, 590], 0.4, {"n": 4, "gone": 0.0}, set=[st("die|60%", 1.0, gone=1.0)])])
    T["s5.l4"] = dict(room="road", f="kk", cams=[[600, 700, 0.9, 0.95], [1300, 760, 1.2, 1.25]], cuts=["hatch|65%"], mb=HID,
                      x=[A("car", "tc_car", [-300, 960], 0.9, {"roll": 1.0, "bounce": 1.0, "tree": True}, moves=[mv(0.0, 3.0, [1500, 960], linear=True)])],
                      sfx=["whoosh@ride|20%"])
    T["s5.l5"] = dict(room="lot", f="wk", cams=[[1100, 700, 1.6, 1.7]], cuts=["trunk|55%"], pose="lean", look=[1050, 700],
                      mb=MB(1300, prop="torch"), x=[A("tl", "tc_tree_lying", [700, FY], 0.6, {})], check_at="trunk|55%",
                      light={"kind": "flashlight", "target": [1050, 780]})
    T["s5.l6"] = dict(room="trunk", f="kk", cams=[[960, 740, 1.6, 1.7], [1100, 740, 1.6, 1.7]], cuts=["sanitizer|50%"], mb=HID,
                      x=[A("slf", "tc_slf_eggs", [960, 760], 0.9, {"off": 0.0}, set=[st("Scrape|20%", 1.0, off=1.0)]),
                         A("sc", "tc_prop", [1300, 700], 1.0, {"kind": "scraper"}, moves=[mv("Scrape|15%", 1.0, [700, 780])], front=True),
                         pop(A("bag", "tc_prop", [1250, 850], 0.9, {"kind": "zipbag"}), "sanitizer|50%")], sfx=["scratch@Scrape|20%"])
    T["s5.l7"] = dict(room="liv", f="Mk", cams=[[1500, 600, 1.8, 1.9]], cuts=["Report|45%"], pose="point", look="viewer", mb=MB(1650, prop="phone"),
                      x=[tree(), A("ph", "tc_prop", [1500, 600], 1.0, {"kind": "phone"})], act="curious")
    T["s5.l8"] = dict(room="curb", f="wk", cams=[[800, 700, 1.3, 1.35]], cuts=["chipping|50%"], pose="present", mb=MB(1350),
                      x=[A("tl", "tc_tree_lying", [500, FY], 0.5, {"dry": 1.0}), lab("rc", "TREE RECYCLING", [700, 480], "chipping|50%", px=64, color=GREEN)])
    # =========================================================================================== 6. the mistake (living room at night)
    T["s6.l0"] = dict(room="livN", f="kM", cams=[[1150, 560, 1.1, 1.15]], cuts=["spray|70%"], pose="shock", mb=MB(1600, prop="aerosol"), act="shocked", burst=True,
                      x=[tree()], **stamp("NO", "spray|75%", RED, 960, 380, 220, -10), sfx=["stamp@spray|75%"])
    T["s6.l1"] = dict(room="board", f="kk", cams=[[0, 0, 1.0, 1.05], [0, 100, 1.5, 1.55]], cuts=["usually|60%"], mb=HID,
                      x=[A("can", "tc_prop", [0, 200], 1.6, {"kind": "aerosol", "flame": 0.0}, set=[st("flammable|45%", 0.4, flame=1.0)]),
                         lab("ni", "NOT FOR INDOOR USE", [0, -260], "indoor|75%", px=60, color=YEL)], sfx=["tink@flammable|45%"])
    T["s6.l2"] = dict(room="livN", f="wM", cuts=["never|60%"], pose="point", look="viewer", mb=MB(1600), x=[tree()], check_at="never|70%",
                      sfx=["hit@never|60%"])
    T["s6.l3"] = dict(room="livN", f="kw", cams=[[960, 500, 1.4, 1.5]], cuts=["lights|55%"], pose="nervous", look="tree",
                      mb=MB(1600, prop="aerosol_down", moves=[mv("fire|60%", 1.2, [1800, FY], walk=True)]), x=[tree(lit=1.0)])
    T["s6.l4"] = dict(room="livN", f="Mk", cams=[[960, 560, 1.0, 1.05]], cuts=["Whoever|35%"], pose="deadpan", look="viewer", mb=MB(1600),
                      x=[tree(), A("coal", "tc_prop", [1300, FY], 0.8, {"kind": "logs", "n": 1})], card=False)
    T["s6.l5"] = dict(room="liv", f="kM", cams=[[1450, 760, 1.5, 1.6]], cuts=["Iowa|40%"], pose="laugh", mb=MB(1650),
                      x=[tree(), prop("tab", "table", [1400, FY], 1.0, open=1.0), A("can", "tc_prop", [1400, 520], 0.5, {"kind": "aerosol"}, moves=[mv("need|30%", 0.6, [1400, 640])])])
    T["s6.l6"] = dict(room="yard", f="kkk", cams=[[600, 600, 1.0, 1.05], [1200, 600, 1.0, 1.05], [960, 600, 0.9, 0.95]], cuts=["Norwegian|40%", "Shaking|75%"],
                      mb=HID, x=[A("p1", "tc_prop", [600, FY], 1.0, {"kind": "sign", "text": "HOSE IT", "col": "#3fb950"}),
                                 A("p2", "tc_prop", [1200, FY], 1.0, {"kind": "sign", "text": "DON'T", "col": "#e5383b"}),
                                 A("t", "tc_xtree", [960, FY], 0.6, {"deco": 0.0, "lit": 0.0, "sway": 0.0, "gifts": False}, set=[st("Shaking|75%", 0.0, sway=0.08)])],
                      check_at="Shaking|80%", sfx=["pop@can|25%", "pop@Norwegian|45%", "whoosh@Shaking|75%"])
    T["s6.l7"] = dict(room="liv", f="kkk", cams=[[1750, 760, 1.4, 1.5], [1150, 600, 0.9, 0.95], [1200, 760, 1.5, 1.55]], cuts=["Illinois|30%", "wake|70%"], mb=HID,
                      x=[tree(), prop("lg", "logs", [1750, FY], 1.0, n=2), prop("pile", "logs", [1200, FY], 1.0, n=9),
                         A("bb", "tc_barkbeetle", [1200, 760], 0.15, {}), A("x", "ds_cross", [1200, 760], 1.0, {"on": 0.0, "r": 180}, set=popset("wake|70%"), front=True)],
                      sfx=["stamp@wake|70%"])
    # =========================================================================================== 7. the tree check (the lot)
    T["s7.l0"] = dict(room="lot", f="w", pose="present", look="viewer", mb=MB(1200), sfx=["hit@check|60%"])
    T["s7.l1"] = dict(room="lot", f="kk", cams=[[600, 700, 1.0, 1.05], [500, 700, 1.6, 1.7]], cuts=["scan|60%"], mb=MB(1000, prop="torch"), pose="lean",
                      x=[A("te", "tc_tree_end", [500, FY], 0.6, {"peek": 0.0}, set=[st("look|30%", 1.0, peek=1.0)])], list_step=1)
    T["s7.l2"] = dict(room="yard", f="kk", cams=[[600, 700, 1.3, 1.35], [400, 700, 1.3, 1.35]], cuts=["tuck|60%"], mb=MB(800, prop="shears", moves=[mv("tuck|60%", 0.8, [600, FY], walk=True)]),
                      pose="present", x=[A("sh", "tc_shrub", [300, FY], 0.9, {"snow": 0.6})], list_step=2)
    T["s7.l3"] = dict(room="lot", f="kk", cams=[[500, 600, 1.0, 1.05], [800, 700, 1.0, 1.05]], cuts=["move|55%"], mb=MB(1100, moves=[mv("move|55%", 1.2, [1300, FY], walk=True)]),
                      pose="point", x=[A("shk", "tc_shaker", [500, FY], 0.8, {"shake": 0.0, "fall": 0.0}, set=[st("Shake|10%", 0.3, shake=1.0, fall=1.0), st("move|50%", 0.3, shake=0.0)])],
                      list_step=3, sfx=["whoosh@Shake|10%"])
    T["s7.l4"] = dict(room="lot", f="kk", cams=[[800, 600, 1.3, 1.35], [800, 700, 1.8, 1.9]], cuts=["trunk|60%"], mb=MB(1100, prop="tongs_nest"), pose="present",
                      x=[A("tl", "tc_tree_lying", [500, FY], 0.6, {})], list_step=4)
    T["s7.l5"] = dict(room="liv", f="kk", cams=[[1100, 600, 1.0, 1.05], [1200, 700, 1.3, 1.35]], cuts=["squash|55%"], mb=MB(1300, prop="hose"), pose="present",
                      x=[tree(), A("x1", "ds_cross", [1450, 760], 1.0, {"on": 0.0, "r": 120}, set=popset("squash|60%"), front=True),
                         A("x2", "ds_cross", [1650, 760], 1.0, {"on": 0.0, "r": 120}, set=popset("spray|85%"), front=True),
                         prop("sl", "slipper", [1450, FY], 0.8), prop("can", "aerosol", [1650, FY], 0.6)], list_step=5, sfx=["stamp@squash|60%", "stamp@spray|85%"])
    T["s7.l6"] = dict(room="lot", f="M", pose="laugh", look="viewer", mb=MB(1200), list_all=True, act="smug")
    # =========================================================================================== 8. the verdict
    T["s8.l0"] = dict(room="liv", f="kk", cams=[[960, 540, 1.0, 1.04], [960, 500, 1.2, 1.25]], cuts=["one|60%"], mb=MB(1600), pose="laugh",
                      x=[tree()], meter_big_to=1.0, meter_big_at="45%", meter_at="one|60%", slam_dur=0.9, tint=[0.6, 1.0, 0.6, 0.06], sfx=["sting@one|60%"])
    T["s8.l1"] = dict(room="liv", f="kk", cams=[[960, 560, 1.0, 1.05], [960, 500, 1.6, 1.7]], cuts=["outdoor|45%"], mb=HID,
                      x=[tree(zs=1.0)], meter_big=1.0, meter_big_to=0.0, meter_big_at="35%")
    T["s8.l2"] = dict(room="yard", f="wM", cuts=["go|55%"], pose="laugh", look="viewer", mb=MB(1300, prop="carrytree", moves=[mv("go|50%", 1.4, [700, FY], walk=True, face=-1)]))
    T["s8.l3"] = dict(room="yardS", f="kk", cams=[[800, 700, 1.0, 1.05], [800, 650, 1.7, 1.8]], cuts=["spring|40%"], mb=HID,
                      x=[A("sh", "tc_shrub", [800, FY], 1.0, {"spring": 1.0}), A("tw", "tc_prop", [880, 640], 0.5, {"kind": "shrubtwig"})] +
                        [A(f"ny{k}", "tc_nymph", [880, 640], 0.0005, {}, moves=[mv(f"hatches|{45 + 4 * k}%", 1.2, [700 + 60 * k, 560 + 50 * (k % 3)], s=0.07)]) for k in range(6)],
                      tint=[0.7, 1.0, 0.6, 0.06], act="story")
    T["s8.l4"] = dict(room="liv", f="wk", cams=[[1500, 300, 1.6, 1.7]], cuts=["skinny|30%"], pose="point", look=[1500, 250], mb=MB(1600),
                      x=[tree(), A("sp", "cellar_spider", [1500, 220], 0.3, {}), A("web", "ds_web", [1500, 150], 0.5, {"w": 400, "h": 400})])
    return T
