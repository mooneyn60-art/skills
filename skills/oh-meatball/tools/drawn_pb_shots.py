"""The hand-made shots for the polar bear long-form (tools/drawn_polarlife.py): spec line id -> recipe + args, one
entry per outline line (s<segment>.l<line>), drawn from that line's `vis`. Word anchors fall back to a share
("word|40%"). World: scenes have the ground at y = 900 and fill x 0..1920 at zoom 1; boards (ds_board_bg) are centred
on (0, 0). Cards sit at the top (screen y 150), so every subject is kept below screen y ~300.

Meatball is never drawn near a wild bear: he is at the tour truck, his own snow hole or ice hole, the motel, the
holding facility's front door (no bear in frame), the tour desk, or his own half of a split screen.

Format keys a shot may carry (read by drawn_catlife.expand): meter_in, meter_at, meter_blink, meter_swing,
meter_climb, chips8 {n0, filled0, y, sets}, stamps [...], card_at, card_y, card_x, card_w, card_px, no_card, pad,
tint, flash, shake, sheet_at, norecut, recut (False), top_actors."""
from drawn_dontsquish import actor, cam, mb
from drawn_pb_art import AGES

HID = {"hidden": True, "pose": "neutral", "pos": [-3000, 1500], "size": 600}
WIDE = [960, 540, 1.0]
B = "ds_board_bg"
BOARD = {"color": "#1f1b2e"}


def head(pos, s, age="adult", pose="stand"):
    """World point of the bear's head centre (for close-ups)."""
    L, Hh, ll, hk, mz, fl = AGES[age]
    legl = ll * (0.18 if pose in ("lie", "curl") else 1.0)
    by = -legl - Hh * 0.42
    if pose == "curl":
        hx, hy = L * 0.46, by + Hh * 0.18
    else:
        hx, hy = L * 0.74, by - Hh * 0.42
    if age in ("newborn", "cub"):
        hx -= L * 0.06
        hy += Hh * 0.05
    return [pos[0] + hx * s, pos[1] + hy * s]


def table():
    T = {}

    def S(scene, c0, to=None, actors=(), shots=None, scene_p=None, mbx=None, sfx=(), **kw):
        d = {"r": "scene", "scene": scene, "scene_p": dict(scene_p or ({} if scene != B else BOARD)), "cam": c0,
             "to": to if to is not None else [c0[0], c0[1], round(c0[2] * 1.06, 3)], "actors": list(actors),
             "mb": mbx or HID, "sfx": list(sfx)}
        if shots:
            d["shots"] = shots
        d.update(kw)
        return d

    def A(idn, typ, pos, s=1.0, p=None, at=None, sets=None, moves=None, front=False, flip=False, rot=0.0, dur=0.3):
        pp = dict(p or {})
        st_ = list(sets or [])
        if at:
            pp["on"] = 0.0
            st_ = [{"at": at, "dur": dur, "p": {"on": 1.0}}] + st_
        return actor(idn, typ, pos, s, pp, st_ or None, moves, front=front, flip=flip, rot=rot)

    def bear(pos, s=0.8, idn="hero", sets=None, moves=None, flip=False, front=False, **p):
        p.setdefault("age", "adult")
        return actor(idn, "pb_bear", pos, s, p, sets, moves, front=front, flip=flip)

    def M(pose, pos, size=520, look="viewer", **kw):
        # every key the parka wrapper reads is set on every line: drawn.plan carries mb keys over from the last line
        for k, v in (("parka", True), ("coats", False), ("floaties", False), ("gloves", False), ("sweat", False),
                     ("hood", 0.0), ("hood_at", None), ("camera", True)):
            kw.setdefault(k, v)
        return mb(pose, tuple(pos), size, look=look, **kw)

    def mv(at, dur, pos, **kw):
        return dict({"at": at, "dur": dur, "pos": list(pos)}, **kw)

    def st(at, dur=0.3, **p):
        return {"at": at, "dur": dur, "p": p}

    def review(text, at="70%", pos=(1480, 430), s=0.75, **p):
        return A("rev", "pb_review", list(pos), s, dict({"text": text, "stars": 1}, **p), at=at, front=True, dur=0.35)

    def pill(text, at="30%"):
        return A("pill", "pb_pill", [0, 0], 1.0, {"text": text}, at=at, front=True, dur=0.4)

    def label(idn, text, pos, px=44, at=None, bg="#121628", **p):
        return A(idn, "pb_label", list(pos), 1.0, dict({"text": text, "px": px, "bg": bg}, **p), at=at, front=True)

    def truck(pos=(1400, 900), s=0.7, **p):
        return A("truck", "pb_truck", list(pos), s, p)

    def guide(pos, s=0.62, idn="guide", **p):
        p.setdefault("cap", "#2e6b45")
        p.setdefault("lanyard", True)
        p.setdefault("head", "#d9a57b")
        return actor(idn, "pb_stick", list(pos), s, p, p.pop("sets", None), p.pop("moves", None))

    ICE = {"kind": "pack"}

    # =========================================================================================== 0. day one (cold open)
    mom0, nb0 = [760, 900], [1120, 900]
    hn = head(nb0, 1.0, "newborn", "lie")
    den_pair = [bear(mom0, 0.78, "mom", pose="curl", shut=True),
                bear(nb0, 1.0, "hero", age="newborn", pose="lie", wiggle=1.0, flip=True)]
    T["s0.l0"] = S("pb_den", [hn[0] - 120, hn[1] - 40, 2.3], [hn[0] - 160, hn[1] - 30, 2.1], den_pair,
                   card_at="polar|50%", sfx=["sting@0.02"], sheet_at=0.75, recut=False,
                   shots=[cam([hn[0] - 120, hn[1] - 40, 2.3], [hn[0] - 170, hn[1] - 30, 2.05])])
    # the newborn is flipped (faces the mother): its head is on its left
    hnf = [nb0[0] - (hn[0] - nb0[0]), hn[1]]
    T["s0.l0"]["cam"] = [hnf[0] + 60, hnf[1] - 40, 2.3]
    T["s0.l0"]["shots"] = [cam([hnf[0] + 60, hnf[1] - 40, 2.3], [hnf[0] + 20, hnf[1] - 30, 2.05])]
    T["s0.l1"] = S("pb_den", [980, 640, 1.0], None, den_pair + [
                   A("dec", "pb_label", [980, 330], 1.0, {"text": "DEC", "px": 90, "bg": "#b8352c"}, at="December|25%",
                     sets=[st("January|40%", 0.2, on=0.0)], front=True),
                   A("jan", "pb_label", [980, 330], 1.0, {"text": "JAN", "px": 90, "bg": "#b8352c"}, at="January|40%", front=True)],
                   shots=[cam([980, 640, 1.0], [980, 650, 1.08]),
                          cam([hnf[0] + 40, hnf[1] - 20, 4.2], [hnf[0] + 40, hnf[1] - 20, 4.5], at="eyes|72%", dur=0.5)],
                   sfx=["whoosh@0.02", "tink@December|25%", "tink@January|40%"])
    T["s0.l2"] = S("pb_den", [980, 700, 1.25], [980, 710, 1.32],
                   [A("scale", "cl_scale", [940, 900], 0.95, {"v": 0.0}, sets=[st("weigh|20%", 0.8, v=0.06)]),
                    bear([830, 840], 0.85, age="newborn", pose="lie", wiggle=0.6),
                    label("kg", "0.6 KG", [1160, 470], 50, at="weigh|30%")],
                   card_at="600|35%", sfx=["tink@weigh|25%"], norecut=True)
    T["s0.l3"] = S("pb_den", [1000, 780, 1.6], [1000, 780, 1.68], den_pair,
                   chips8={"n0": 0.0, "y": 330, "sets": [st("Eight|5%", 1.6, n=8.0)]},
                   card_at="Eight|10%", sfx=["pop@Eight|10%", "tink@order|70%"], norecut=True)
    T["s0.l4"] = S("pb_den", [760, 640, 1.15], [780, 650, 1.2],
                   [bear(mom0, 0.78, "mom", pose="curl", shut=True, thin=0.3),
                    bear([1120, 900], 0.95, "hero", age="newborn", pose="lie", wiggle=0.6, flip=True),
                    A("strip", "pb_strip", [770, 500], 0.7, {"n": 8, "mark": "bowl", "lit": 0.0},
                      sets=[st("eating|30%", 1.6, lit=8.0)], front=True)],
                   card_at="fast|55%", meter_at="months|80%", sfx=["tink@eating|30%"], norecut=True)
    T["s0.l5"] = S("pb_ice", [960, 640, 1.0], [960, 660, 1.1],
                   [bear([960, 760], 0.32, pose="swim", pull=0.8, wcol="#17324c", walpha=0.85),
                    A("pages", "pb_pages", [960, 380], 0.8, {"n": 9, "fall": 0.0, "nums": True, "mode": "fly"},
                      sets=[st("swim|30%", 1.6, fall=1.0)], front=True)],
                   scene_p={"kind": "open"}, sfx=["splash@0.05", "whoosh@nine|70%"], norecut=True)
    T["s0.l6"] = S("pb_den", [1050, 760, 1.5], [1060, 770, 1.58], den_pair + [pill("YOUR SCORE?", "score|25%")],
                   meter_in="Raw|30%", sfx=["boing@sweet|80%"])
    # =========================================================================================== 1. the den
    T["s1.l0"] = S("pb_slope", WIDE, [960, 560, 1.06],
                   [bear([1000, 600], 0.35, age="cub", pose="lie"),
                    bear([1150, 590], 0.4, "mom", pose="lie", flip=True)], sfx=["whoosh@den|40%"])
    T["s1.l1"] = S("pb_den", [980, 600, 0.98], [980, 610, 1.03],
                   [bear([800, 900], 0.72, "mom", pose="lie"),
                    bear([1180, 900], 0.75, "hero", age="newborn", pose="lie", wiggle=0.5, flip=True)],
                   scene_p={"dims": 1.0}, card_at="metre|40%", card_w=1700, sfx=["tink@across|45%", "tink@high|80%"])
    T["s1.l2"] = S("pb_ice", WIDE, [940, 560, 1.06],
                   [truck((1350, 900), 0.75),
                    A("blank", "pb_review", [1460, 380], 0.6, {"blank": True}, at="review|55%", front=True, dur=0.35)],
                   scene_p=ICE, mbx=M("wave", (600, 905), 540, prop="ticket",
                                       gest=[["package|30%", "present", 1.4], ["review|55%", "point", 1.4]]),
                   sfx=["pop@Meatball|15%", "pop@review|55%"])
    mnd = [720, 900]
    T["s1.l3"] = S("pb_ice", [900, 640, 1.15], [920, 650, 1.2],
                   [truck((1650, 900), 0.6), A("mound", "pb_mound", mnd, 1.35, front=True),
                    guide([1080, 900], 0.6, arm="down", sets=[st("stuck|45%", 0.2, arm="push"), st("Hell|70%", 0.2, arm="boots")])],
                   scene_p=ICE, mbx=M("shock", (mnd[0], 400), 620, shake=1.0, moves=[mv(0.0, 0.01, (mnd[0], 400), rot=180)]),
                   sfx=["thud@stuck|40%", "boing@Hell|70%"])
    T["s1.l4"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [A("th", "pb_thermo", [0, 120], 0.95, {"g": 0.0}, sets=[st("freezing|30%", 1.2, g=1.0)])],
                   card_at="freezing|30%", sfx=["tink@freezing|35%"], norecut=True)
    T["s1.l5"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [A("sc1", "cl_scale", [-420, 330], 0.85, {"v": 0.75}),
                    bear([-520, 270], 0.42, "m1", pose="stand"),
                    A("sc2", "cl_scale", [420, 330], 0.85, {"v": 0.75}, sets=[st("lose|55%", 1.0, v=0.43)]),
                    bear([320, 270], 0.42, "m2", thin=0.0, sets=[st("lose|55%", 1.0, thin=1.0)]),
                    A("arr", "pb_arrow", [-130, 60], 1.0, {"x": 220, "y": 0, "on": 0.0}, sets=[st("lose|50%", 0.5, on=1.0)])],
                   card_at="43|70%", meter_at="43|75%", sfx=["whoosh@lose|55%"], norecut=True)
    T["s1.l6"] = S("pb_ice", [960, 600, 1.1], [980, 610, 1.15],
                   [truck((1600, 900), 0.6), review("NO LEGROOM.|NO ROOM SERVICE.", "star|35%", (1300, 470), 0.8)],
                   scene_p=ICE, mbx=M("present", (700, 905), 520, prop="clip", gest=[["legroom|55%", "deadpan", 1.4]]),
                   sfx=["stamp@star|35%", "boing@service|85%"])
    T["s1.l7"] = S("pb_slope", WIDE, [960, 560, 1.05],
                   [A("bub", "pb_bubble", [960, 560], 0.85, at="den|15%")],
                   stamps=[{"text": "ONLY PREGNANT FEMALES", "at": "pregnant|65%", "px": 90, "y": 760, "color": "#e5383b"}],
                   card_at="pregnant|60%", sfx=["pop@den|15%"])
    T["s1.l8"] = S("pb_den", [980, 650, 1.05], [980, 640, 1.1],
                   [A("scale", "cl_scale", [1180, 900], 0.85, {"v": 0.06}, sets=[st("ten|15%", 1.0, v=0.7)]),
                    bear([1090, 845], 0.6, "hero", age="cub", pose="stand"),
                    bear([620, 900], 0.6, "mom", pose="stand", sets=[st("breaks|50%", 0.4, swipe=1.0)])],
                   scene_p={"open": 1.0}, card_at="ten|15%", flash=["breaks|55%"], sfx=["tink@ten|20%", "crunch@breaks|55%"])
    T["s1.l8"]["shots"] = [cam([980, 650, 1.05], [990, 660, 1.1]), cam([1120, 700, 1.4], [1130, 700, 1.45], at="ten|25%", dur=0.5),
                           cam([980, 420, 1.0], [980, 400, 1.06], at="breaks|50%", dur=0.6)]
    T["s1.l8"]["norecut"] = True
    # =========================================================================================== 2. the odds
    T["s2.l0"] = S("pb_slope", [1000, 560, 1.2], [1000, 560, 1.28],
                   [bear([1040, 600], 0.3, age="cub", pose="lie", look=[1, 0.3])], sfx=["whoosh@odds|50%"])
    T["s2.l1"] = S(B, [0, 0, 1.0], [0, 15, 1.03],
                   [A("bars", "pb_bars2", [140, -10], 0.95,
                      {"rows": [["ADULTS", 49.5, 100], ["CUBS", 13.4, 100]], "g": 0.0,
                       "head": "SHARE OF TIME OUTSIDE THE DEN SPENT INACTIVE", "small": "8 ADULTS, 14 CUBS, ALASKA, MARCH 2002 AND 2003"},
                      sets=[st("inactive|50%", 1.2, g=1.0)]),
                    bear([-700, 400], 0.32, "mom", pose="lie"),
                    bear([560, 400], 0.36, "hero", age="cub",
                         moves=[mv(0.3, 0.8, (680, 400), rot=360), mv(1.3, 0.8, (800, 400), rot=720), mv(2.4, 0.8, (680, 400), rot=1080),
                                mv(3.5, 0.8, (800, 400), rot=1440)])],
                   card_at="inactive|55%", card_px=96, sfx=["pop@cubs|30%"], norecut=True)
    T["s2.l2"] = S("pb_ice", WIDE, [960, 560, 1.04],
                   [truck((1050, 900), 0.6), A("flake", "pb_snowflake", [520, 300], 1.0, moves=[mv("lay|55%", 1.6, (535, 820))], front=True),
                    review("TOO MUCH|CARDIO.", "star|75%", (1450, 420), 0.7)],
                   scene_p=ICE, mbx=M("neutral", (200, 905), 480,
                                      moves=[mv(0.1, 1.2, (1650, 905), walk=True), mv(1.4, 1.3, (520, 905), walk=True),
                                             mv("lay|50%", 0.3, (520, 880), rot=-90)]),
                   sfx=["step@lap|20%", "thud@lay|52%", "stamp@star|75%"])
    T["s2.l3"] = S(B, [0, 0, 1.0], [0, 10, 1.05],
                   [A("map", "pb_map", [0, 100], 0.62, {"dots": ["ALASKAN BEAUFORT SEA"], "lit": 0.0},
                      sets=[st("place|50%", 0.4, lit=1.0)])],
                   sfx=["pop@place|50%"], norecut=True)
    T["s2.l4"] = S(B, [0, 0, 1.0], [-30, 10, 1.04],
                   [A("dial", "pb_dial", [-260, -10], 0.95, {"v": 0.0, "final": 65, "small": "ALASKAN BEAUFORT SEA, 12-YEAR STUDY"},
                      sets=[st("chance|50%", 1.4, v=65.0)]),
                    bear([450, 380], 0.42, "mom", collar=True), bear([700, 380], 0.42, "hero", age="cub")],
                   card_at="65|80%", meter_at="65|85%", sfx=["click@chance|50%"], norecut=True)
    T["s2.l5"] = S(B, [-260, 60, 1.25], [-260, 60, 1.3],
                   [A("dial", "pb_dial", [-260, -10], 0.95, {"v": 65.0, "final": 86, "small": "OTHER POPULATIONS AND YEARS DIFFER"},
                      sets=[st("86|30%", 1.0, v=86.0)])],
                   card_at="86|30%", meter_at="86|40%", sfx=["click@86|30%"], norecut=True)
    T["s2.l6"] = S("pb_ice", [900, 600, 1.0], [960, 610, 1.05],
                   [bear([200, 900], 0.62, "mom", moves=[mv(0.2, 5.0, (760, 900), walk=True)]),
                    bear([-80, 900], 0.42, "c1", age="cub", moves=[mv(0.4, 5.0, (470, 900), walk=True)]),
                    label("note", "57 TRACKED FEMALES", [1500, 340], 40)],
                   scene_p={"kind": "edge", "ex": 1200}, sfx=["splash@water|30%"])
    T["s2.l7"] = S("pb_ice", [960, 640, 1.2], [960, 650, 1.26],
                   [bear([1180, 900], 0.75, "mom", flip=True, look=[1, 0.4]),
                    bear([760, 900], 0.62, "hero", age="cub", look=[1, -0.8]),
                    A("tb", "pb_timebar", [960, 460], 0.55, {"a": "BIRTH", "b": "2 YEARS", "g": 0.0, "tag": "SOMETIMES LONGER"},
                      sets=[st("two|60%", 1.0, g=1.0)], front=True)],
                   scene_p=ICE, sfx=["tink@two|60%"])
    # =========================================================================================== 3. seal school
    T["s3.l0"] = S("pb_ice", [960, 700, 1.4], [960, 700, 1.48],
                   [A("seal", "pb_seal", [960, 905], 1.0, {"head_only": True, "rise": 0.0}, sets=[st("Seal|30%", 0.4, rise=1.0)])],
                   scene_p={"kind": "hole", "hx": 960}, sfx=["splash@Seal|30%"])
    T["s3.l1"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [A("menu", "pb_board", [80, 20], 0.9), bear([-680, 400], 0.5, "hero", age="cub", look=[1, -0.5])],
                   card_at="seals|45%", sfx=["tink@seals|45%"], norecut=True)
    T["s3.l2"] = S("pb_desk", WIDE, [960, 560, 1.05],
                   [guide([620, 900], 0.62, arm="hold"),
                    A("menu", "pb_menu", [930, 560], 0.85, {"open": 0.0, "flip": 0.0},
                      sets=[st("menu|40%", 0.4, open=1.0), st("short|80%", 0.5, flip=1.0)], front=True)],
                   mbx=M("shock", (1250, 905), 520, gest=[["short|80%", "deadpan", 1.4]]),
                   sfx=["thud@menu|40%", "boing@short|80%"])
    T["s3.l3"] = S("pb_ice", [1000, 680, 1.15], [1020, 690, 1.2],
                   [bear([420, 900], 0.5, "cub", age="cub"),
                    bear([830, 900], 0.82, "mom", sets=[st("blow|55%", 0.25, swipe=1.0), st("blow+0.6|75%", 0.3, swipe=0.0)]),
                    A("seal", "pb_seal", [1250, 905], 0.9, {"head_only": True, "rise": 0.0},
                      sets=[st("air|30%", 0.4, rise=1.0), st("blow|55%", 0.1, a=0.0)]),
                    A("seal2", "pb_seal", [1500, 900], 0.55, {"a": 0.0}, sets=[st("flips|75%", 0.3, a=1.0)]),
                    A("splash", "pb_puff", [1250, 860], 1.0, {"text": ""}, at="blow|55%", sets=[st("blow+0.5|72%", 0.4, on=2.5)], front=True)],
                   scene_p={"kind": "hole", "hx": 1250}, card_at="blow|55%", meter_at="blow|60%",
                   sfx=["splash@blow|55%", "thud@flips|75%"], shake=["blow|56%"])
    T["s3.l4"] = S("pb_ice", [960, 600, 1.08], [980, 610, 1.12],
                   [A("hole", "pb_icehole", [1180, 905], 1.0), A("bucket", "pb_bucket", [720, 905], 1.0),
                    A("rod", "pb_rod", [900, 640], 1.0, {"bend": 0.0, "catch": 0.0, "hy": 340},
                      sets=[st("tried|30%", 0.3, bend=1.0), st("caught|50%", 0.8, catch=1.0, bend=0.3)], front=True),
                    review("THE MENU IS SEAL.|COULD NOT CATCH ONE.", "star|85%", (1450, 400), 0.7)],
                   scene_p=ICE, mbx=M("present", (780, 905), 500, look=[1180, 700], gest=[["own|70%", "shock", 1.4]]),
                   sfx=["click@tried|30%", "boing@caught|50%", "stamp@star|85%"])
    hy5 = head([600, 900], 1.3, "young")
    T["s3.l5"] = S("pb_ice", [hy5[0] + 200, hy5[1] + 40, 1.9], [hy5[0] + 220, hy5[1] + 50, 2.0],
                   [bear([600, 900], 1.3, "hero", age="young", head=0.25),
                    A("note", "pb_sticky", [hy5[0] + 500, hy5[1] + 170], 0.42, {"text": "20 MILES?"}, at="heard|30%", front=True)],
                   scene_p=ICE, stamps=[{"text": "NO SOURCE FOUND", "at": "no|80%", "px": 90, "y": 760, "color": "#e5383b"}],
                   card_at="no|80%", sfx=["tink@heard|30%"])
    T["s3.l6"] = S("pb_icecut", [900, 660, 1.0], [920, 660, 1.04],
                   [bear([180, 700], 0.5, "hero", age="young", pose="sniff")],
                   scene_p={"thick": 1.0, "scent": 1.0, "sx": 560}, card_at="kilometre|80%", meter_at="kilometre|85%",
                   sfx=["tink@centimetres|55%", "whoosh@kilometre|80%"])
    T["s3.l7"] = S(B, [0, 0, 1.0], [0, 10, 1.05],
                   [A("note", "pb_sticky", [0, 40], 0.95, {"text": "20 MILES?", "cross": 0.0, "small": "1 KM = ABOUT 0.6 MILE"},
                      sets=[st("hole|20%", 0.8, cross=1.0)])],
                   sfx=["scratch@hole|20%", "boing@nose|80%"], norecut=True)
    T["s3.l8"] = S("pb_ice", [900, 620, 1.12], [920, 630, 1.16],
                   [truck((1500, 900), 0.6)], scene_p=ICE,
                   mbx=M("nervous", (850, 905), 520, gloves=True,
                         gest=[["gloves|30%", "think", 1.2], ["hands|70%", "facepalm", 1.5]],
                         moves=[mv("find|20%", 0.6, (1000, 905), walk=True), mv("gloves|45%", 0.6, (820, 905), walk=True)]),
                   sfx=["boing@hands|75%"])
    T["s3.l9"] = S("pb_ice", [960, 600, 1.0], None,
                   [bear([860, 900], 0.75, "mom", flip=True, moves=[mv("school|30%", 3.0, (-200, 900), walk=True)]),
                    bear([1060, 900], 0.62, "hero", age="young", moves=[mv("school|35%", 3.2, (1650, 900), walk=True)])],
                   scene_p={"kind": "pack", "crack": 1.0},
                   shots=[cam([960, 600, 1.0], [960, 610, 1.05]), cam([960, 650, 1.2], [970, 650, 1.25], at="own|45%", dur=0.5),
                          cam([1150, 980, 1.9], [1160, 990, 2.0], at="floor|75%", dur=0.6)],
                   norecut=True, sfx=["crunch@frozen|85%"])
    # =========================================================================================== 4. the ice
    T["s4.l0"] = S("pb_ice", [960, 560, 0.85], [960, 560, 0.92],
                   [bear([700, 900], 0.35, "hero", age="young", moves=[mv(0.1, 2.0, (900, 900), walk=True)])],
                   scene_p=ICE, sfx=["whoosh@ice|50%"])
    T["s4.l1"] = S("pb_ice", [960, 560, 1.0], [980, 580, 1.06],
                   [bear([900, 380], 0.9, "hero", age="young", pose="swim", under=True)],
                   scene_p={"kind": "under"}, card_at="marine|30%", sfx=["splash@0.05", "whoosh@swim|80%"])
    T["s4.l2"] = S(B, [0, 0, 1.0], [0, 15, 1.04],
                   [A("strip", "pb_strip", [0, 80], 1.25, {"n": 4, "mark": "swim", "k": 3, "lit": 0.0,
                                                          "note": "57 TRACKED FEMALES, SVALBARD"},
                      sets=[st("records|45%", 1.2, lit=4.0)])],
                   card_at="three|55%", card_w=1700, card_px=96, meter_at="swim|90%", sfx=["tink@three|55%"], norecut=True)
    T["s4.l3"] = S("pb_motel", [1000, 700, 1.25], [1010, 700, 1.3],
                   [A("ring", "pb_ring", [400, 870], 1.0, moves=[mv(0.2, 4.5, (1500, 870))]),
                    A("water", "pb_water", [300, 862], 1.0, {"w": 1400, "h": 300}, front=True),
                    review("TOO MUCH|WATER.", "Still|60%", (1450, 480), 0.65)],
                   scene_p={"kind": "pool"},
                   mbx=M("neutral", (1000, 940), 460, floaties=True,
                         gest=[["Floaties|45%", "shock", 1.0], ["counts|75%", "laugh", 1.5]],
                         moves=[mv("Shallow|35%", 0.4, (1000, 990)), mv("Floaties|50%", 0.4, (1000, 940))]),
                   sfx=["splash@Shallow|35%", "boing@counts|80%"])
    T["s4.l4"] = S(B, [0, 0, 1.0], [0, 10, 1.03],
                   [A("map", "pb_map", [-560, 150], 0.62, {"dots": ["SOUTHERN BEAUFORT SEA", "CHUKCHI SEA"], "lit": 0.0},
                      sets=[st("southern|35%", 0.4, lit=1.0)]),
                    A("icons", "pb_icons", [400, 150], 0.62, {"n": 52, "lit": 0.0}, sets=[st("Twenty|75%", 1.2, lit=20.0)])],
                   card_at="Twenty|75%", sfx=["pop@southern|35%", "tink@Twenty|75%"], norecut=True)
    T["s4.l5"] = S("pb_ice", [960, 600, 1.05], [970, 610, 1.1],
                   [bear([800, 900], 0.85, "hero", collar=True, sets=None, moves=[mv(0.0, 0.01, (800, 900), s=0.1), mv(0.05, 0.6, (800, 900), s=0.85)]),
                    A("jr", "pb_journal", [1520, 520], 0.6, {"year": 2011}, at="paper|60%", front=True)],
                   scene_p={"kind": "edge", "ex": 1250}, sfx=["whoosh@0.05", "pop@paper|60%"])
    T["s4.l6"] = S("pb_ice", [960, 660, 1.0], [960, 670, 1.12],
                   [bear([960, 820], 0.22, "hero", pose="swim", pull=0.7, wcol="#17324c", walpha=0.85)],
                   scene_p={"kind": "open"}, card_at="687|35%", sfx=["sting@687|35%"], norecut=True)
    T["s4.l7"] = S("pb_ice", [900, 640, 1.2], [920, 640, 1.26],
                   [bear([1100, 820], 0.3, "hero", pose="swim", pull=0.7, wcol="#17324c", walpha=0.85),
                    A("pages", "pb_pages", [960, 360], 0.8, {"n": 9, "fall": 0.0}, sets=[st("Nine|30%", 2.5, fall=1.0)], front=True)],
                   scene_p={"kind": "open"}, card_at="Nine|30%", meter_at="miles|80%", sfx=["splash@Nine|35%"])
    T["s4.l8"] = S("pb_ice", [960, 640, 1.0], [980, 650, 1.05],
                   [A("route", "pb_route", [300, 800], 1.0, {"g": 0.0, "pts": [[0, 0], [350, -60], [700, 20], [1050, -80], [1350, -20]],
                                                           "note": "SCHEMATIC, NOT THE REAL TRACK"},
                      sets=[st("swam|20%", 3.0, g=1.0)], front=True),
                    bear([500, 760], 0.3, "hero", moves=[mv("swam|20%", 3.0, (1500, 760), walk=True)])],
                   scene_p={"kind": "floes", "crack": 0.5}, card_at="1,800|60%", sfx=["whoosh@swam|20%"])
    T["s4.l9"] = S(B, [0, 0, 1.0], [0, 10, 1.03],
                   [label("l1", "LATE AUGUST 2008", [-390, 295], 40), label("l2", "LATE OCTOBER 2008", [470, 295], 40, at="lost|50%"),
                    bear([-560, 250], 0.5, "m1"), bear([-220, 250], 0.5, "y1", age="cub"),
                    bear([300, 250], 0.5, "m2", thin=1.0, a=0.0, sets=[st("lost|50%", 0.4, a=1.0)]),
                    bear([640, 250], 0.5, "y2", age="cub", ghost=0.0, sets=[st("yearling|80%", 0.5, ghost=1.0)]),
                    label("sm", "BETWEEN TWO CAPTURES", [40, 360], 30)],
                   card_at="lost|55%", meter_at="yearling|85%", sfx=["whoosh@lost|50%", "thud@yearling|85%"], norecut=True)
    T["s4.l10"] = S("pb_ice", [1100, 700, 1.2], [1120, 700, 1.26],
                    [bear([1250, 1000], 0.75, "hero", age="young", flip=True, moves=[mv(0.1, 0.8, (1000, 900), walk=True)],
                          sets=[st("shake|55%", 0.2, shake=1.0, spray=1.0), st("dog|85%", 0.3, shake=0.0)])],
                    scene_p={"kind": "edge", "ex": 1220}, sfx=["splash@0.1", "whoosh@shake|55%"])
    T["s4.l11"] = S("pb_ice", [960, 600, 1.08], [980, 610, 1.12],
                    [truck((1500, 900), 0.7)], scene_p=ICE,
                    mbx=M("neutral", (500, 905), 520, hood_at="hood|25%", shake=1.0,
                          gest=[["eyes|45%", "shock", 1.0], ["truck|85%", "facepalm", 1.5]],
                          moves=[mv("walked|55%", 1.0, (1080, 905), walk=True), mv("truck|85%", 0.3, (1020, 950), rot=-15)]),
                    sfx=["thud@truck|85%"], shake=["truck|86%"])
    T["s4.l11"]["mb"]["shake"] = 0.0
    T["s4.l12"] = S(B, [0, 0, 1.0], [0, 15, 1.04],
                    [A("fan", "pb_reviews", [0, 260], 0.75, {"n": 4, "mode": "fan", "spread": 0.0, "top": "1 STAR"},
                       sets=[st("reviews|25%", 1.0, spread=1.0)]), pill("YOUR REVIEW SO FAR?", "yours|75%")],
                    chips8={"n0": 8.0, "filled0": 4.0, "y": 300, "sets": [st(0.1, 0.1, pulse=1.0)]},
                    meter_blink="four|10%", sfx=["stamp@star|40%", "stamp@star#2|50%", "stamp@star#3|60%", "stamp@star#4|70%"],
                    norecut=True)
    T["s4.l13"] = S("pb_ice", [960, 600, 1.05], [960, 610, 1.1],
                    [bear([800, 900], 0.62, "hero", age="young"),
                     bear([2600, 900], 1.25, "big", age="male", sil=1.0, flip=True, moves=[mv("catch|70%", 1.2, (1750, 900), walk=True)])],
                    scene_p=ICE, card_at="predators|50%", sfx=["thud@catch|75%"])
    # =========================================================================================== 5. bigger bears
    T["s5.l0"] = S("pb_ice", [1100, 560, 1.1], [1100, 560, 1.16],
                   [bear([1300, 900], 1.3, "big", age="male", sil=1.0, flip=True), bear([500, 900], 0.55, "hero", age="young")],
                   scene_p=ICE, sfx=["sting@0.05"])
    T["s5.l1"] = S("pb_ice", [960, 520, 0.7], [960, 540, 0.78],
                   [bear([960, 900], 0.4, "hero", age="young", mood="worry", moves=[mv(0.5, 3.0, (1100, 900), walk=True)])],
                   scene_p=ICE, card_at="difficult|40%", sfx=["whoosh@alone|85%"])
    T["s5.l2"] = S("pb_ice", [960, 620, 1.0], [960, 630, 1.04],
                   [A("seal", "pb_seal", [1060, 900], 0.5, {"slide": 1.0}),
                    bear([760, 900], 0.55, "hero", age="young",
                         moves=[mv("likely|60%", 1.2, (380, 900))], sets=[st("likely|60%", 0.3, mood="worry")]),
                    bear([2400, 900], 0.95, "big", age="male", flip=True, moves=[mv("larger|40%", 1.5, (1450, 900), walk=True)])],
                   scene_p=ICE, meter_at="take|85%", sfx=["step@larger|40%", "boing@take|85%"])
    T["s5.l3"] = S("pb_motel", [960, 640, 1.1], [980, 650, 1.14],
                   [A("sand", "pb_sandwich", [1010, 690], 1.0, moves=[mv("took|40%", 0.4, (1180, 520)), mv("took+0.4|55%", 2.0, (2300, 520))]),
                    A("big", "pb_stick", [1900, 900], 0.7, {"parka": "#f2711c", "head": "#d9a57b", "arm": "down"},
                      moves=[mv(0.3, 1.4, (1250, 900), walk=True), mv("took+0.4|55%", 2.0, (2400, 900), walk=True)],
                      sets=[st("took|40%", 0.2, arm="lift")]),
                    review("RUDE GUESTS.", "star|80%", (560, 430), 0.7)],
                   scene_p={"kind": "bench"},
                   mbx=M("present", (900, 905), 400, gest=[["sandwich|20%", "laugh", 1.0], ["him|65%", "deadpan", 1.8]]),
                   sfx=["step@bigger|30%", "pop@took|42%", "stamp@star|80%"])
    T["s5.l4"] = S(B, [0, 0, 1.0], [0, 10, 1.03],
                   [A("map", "pb_map", [-540, 150], 0.6, {"dots": ["BEAUFORT SEA"], "lit": 0.0}, sets=[st("Beaufort|40%", 0.4, lit=1.0)]),
                    A("cards", "pb_cards3", [420, 170], 0.95, {"n": 0.0}, sets=[st("three|60%", 1.0, n=3.0)])],
                   card_at="three|60%", sfx=["pop@Beaufort|40%", "tink@three|60%"], norecut=True)
    T["s5.l5"] = S("pb_slope", [980, 520, 1.15], [990, 520, 1.2],
                   [bear([700, 395], 0.55, "big", age="male", pose="sniff", sil=1.0)],
                   scene_p={"dusk": 1.0}, meter_at="scent|85%", sfx=["thud@killed|35%"])
    T["s5.l6"] = S(B, [0, 0, 1.0], [0, 15, 1.04],
                   [A("nb", "pb_sheet", [0, 100], 0.9, {"kind": "note", "title": "24 YEARS", "title_px": 70,
                                                       "rows": ["- - - - - - - - - - - -"] * 4 + ["EARLY 2004: 3 CASES"],
                                                       "px": 44, "circle": None},
                      sets=[st("other|50%", 0.2, circle=4.0)])],
                   card_at="24|30%", sfx=["scratch@other|50%"], norecut=True)
    T["s5.l7"] = S(B, [0, 0, 1.0], [0, 15, 1.04],
                   [A("rep", "pb_sheet", [0, 110], 0.9, {"kind": "report", "title": "STATUS REPORT (CANADA, 2008)", "title_px": 44,
                                                        "rows": ["IN THE BEAR FAMILY,", "POLAR BEARS INCLUDED,", "KILLING CUBS TO BRING",
                                                                 "FEMALES INTO ESTRUS, OR", "CUBS AND ADULTS FOR FOOD,",
                                                                 "IS NOT UNCOMMON"],
                                                        "px": 46, "under": None},
                      sets=[st("uncommon|80%", 0.2, under=5)])],
                   card_at="uncommon|85%", sfx=["scratch@uncommon|85%"], norecut=True)
    T["s5.l8"] = S("pb_ice", [960, 560, 1.15], [960, 560, 1.2],
                   [A("truck", "pb_truck", [960, 960], 0.9, {"curtain": 0.0, "peek": 0.0, "glass": True},
                      sets=[st("relatives|45%", 0.4, curtain=1.0), st("family|75%", 0.3, peek=1.0)], front=True),
                    label("np", "NO NATURAL PREDATORS*", [960, 330], 60, color="#ffd34d"),
                    label("jr", "*JUST RELATIVES", [960, 410], 50, at="relatives|40%", color="#ffffff")],
                   scene_p=ICE, mbx=M("shock", (920, 700), 280, parka=True),
                   meter_at="relatives|45%", sfx=["whoosh@relatives|45%", "boing@family|80%"])
    T["s5.l9"] = S("pb_ice", [960, 600, 1.0], [960, 620, 1.06],
                   [bear([960, 760], 0.4, "hero", age="young", mood="worry")],
                   scene_p={"kind": "floes", "crack": 0.9}, sfx=["crunch@0.1", "crunch@population|60%"], shake=["population|60%"])
    # =========================================================================================== 6. the summer with no food
    T["s6.l0"] = S("pb_shore", WIDE, [960, 560, 1.06], [bear([1300, 900], 0.5, "hero", pose="lie")],
                   scene_p={"season": "summer"}, sfx=["whoosh@food|60%"])
    T["s6.l1"] = S(B, [0, 0, 1.0], [0, 10, 1.03],
                   [A("map", "pb_map", [0, 100], 0.62, {"dots": ["HUDSON BAY"], "lit": 1.0, "ice": 1.0, "hudson_bears": 0.0},
                      sets=[st("breaks|40%", 1.2, ice=0.0), st("land|75%", 0.8, hudson_bears=1.0)])],
                   card_at="July|65%", sfx=["crunch@breaks|40%", "step@land|75%"], norecut=True)
    T["s6.l2"] = S("pb_shore", [960, 640, 1.0], [980, 650, 1.04],
                   [bear([620, 960], 0.62, "hero", pose="lie", shut=True),
                    A("strip", "pb_strip", [1300, 610], 0.62, {"n": 4, "mark": "shade", "k": 2},
                      sets=[st("four|35%", 0.6, k=4)], front=True),
                    A("clk", "pb_clockshare", [1680, 800], 0.55, {"share": 0.0, "label": "INACTIVE"}, sets=[st("inactive|80%", 1.0, share=0.82)],
                      front=True),
                    label("sm", "HUDSON BAY AND EASTERN BAFFIN ISLAND", [520, 700], 32)],
                   scene_p={"season": "summer"}, card_at="ashore|40%", card_w=1700, card_px=90, meter_at="80|90%", norecut=True,
                   sfx=["tink@four|35%", "tink@80|85%"])
    T["s6.l3"] = S(B, [0, 0, 1.0], [0, 15, 1.04],
                   [A("clip", "pb_sheet", [0, 110], 0.85, {"kind": "clip", "title": "142 BEARS",
                                                          "rows": ["2009 TO 2014", "WATER, NO FOOD", "MEDIAN 17 DAYS"], "px": 56,
                                                          "small": "HELD NEAR CHURCHILL", "h": 600}, at="measured|40%")],
                   card_at="142|65%", sfx=["pop@measured|40%"], norecut=True)
    T["s6.l4"] = S(B, [0, 0, 1.0], [0, 15, 1.04],
                   [A("sc", "cl_scale", [-260, 380], 1.0, {"v": 0.9},
                      sets=[st("15%", 0.2, v=0.8), st("35%", 0.2, v=0.7), st("55%", 0.2, v=0.6), st("75%", 0.2, v=0.5)]),
                    A("pages", "pb_strip", [450, 40], 0.85, {"n": 4, "lit": 0.0}, sets=[st("15%", 2.6, lit=4.0)])],
                   card_at="kilogram|35%", meter_at="day|90%", sfx=["tink@15%", "tink@35%", "tink@55%", "tink@75%"], norecut=True)
    T["s6.l5"] = S("pb_motel", [960, 620, 1.05], [970, 630, 1.1],
                   [A("clock", "pb_wallclock", [380, 330], 0.9, {"mn": 0.0}, sets=[st("sunrise|25%", 2.8, mn=240.0)]),
                    A("plate", "pb_waffles", [1100, 610], 1.0, moves=[mv("waffles|40%", 1.4, (1700, 610))]),
                    A("plate2", "pb_waffles", [830, 690], 0.9, {"syrup": True, "on": 0.0}, sets=[st("face|60%", 0.1, on=1.0)]),
                    A("glass", "pb_glass", [560, 700], 0.8),
                    review("KITCHEN CLOSED|FOR MONTHS.", "star|85%", (1420, 760), 0.6)],
                   scene_p={"kind": "breakfast"},
                   mbx=M("deadpan", (700, 905), 460, look=[1100, 610],
                         moves=[mv("face|58%", 0.35, (760, 905), rot=55)], gest=[["waffles|35%", "think", 1.2]]),
                   sfx=["tink@sunrise|25%", "thud@face|60%", "stamp@star|85%"])
    T["s6.l6"] = S("pb_shore", [1500, 820, 1.5], None,
                   [bear([1300, 1000], 0.6, "b1", pose="sniff"),
                    bear([300, 860], 0.55, "b2", pose="swim", seaweed=True, wcol="#4f86ad", walpha=0.8),
                    A("bird", "pb_bird", [-300, 850], 0.8),
                    bear([-520, 980], 0.6, "b3", pose="swim", under=True, sil=0.85, col="#1d3550"),
                    label("tr", "TRYING", [-300, 620], 60, at="word|85%", color="#ffd34d")],
                   scene_p={"season": "summer"},
                   shots=[cam([1500, 820, 1.5], [1480, 820, 1.55]), cam([360, 760, 1.6], [340, 760, 1.65], at="seaweed|30%", dur=0.4),
                          cam([-330, 760, 1.5], [-330, 750, 1.55], at="seabirds|55%", dur=0.4)],
                   norecut=True, sfx=["whoosh@seaweed|30%", "splash@seabirds|55%", "scratch@word|85%"])
    T["s6.l7"] = S("pb_shore", [900, 640, 1.0], None,
                   [bear([600, 920], 0.5, "b1", pose="lie"), bear([1050, 960], 0.55, "b2"), bear([1400, 930], 0.5, "b3", pose="lie", flip=True)],
                   scene_p={"season": "autumn", "town": True},
                   shots=[cam([900, 640, 1.0], [960, 640, 1.04]), cam([1150, 760, 1.5], [1170, 760, 1.55], at="wait|35%", dur=0.5),
                          cam([1170, 760, 1.55], [2700, 640, 1.0], at="town|70%", dur=1.2)],
                   norecut=True, sfx=["whoosh@town|70%"])
    # =========================================================================================== 7. the town
    T["s7.l0"] = S("pb_town", [960, 600, 1.15], [960, 600, 1.22], [], sfx=["whoosh@town|50%"])
    T["s7.l1"] = S("pb_town", [900, 640, 1.0], [920, 650, 1.05],
                   [bear([-300, 900], 0.5, "hero", moves=[mv(0.1, 1.5, (250, 900), walk=True), mv("noisemakers|65%", 2.0, (-500, 900), walk=True, face=-1)]),
                    A("pick", "pb_pickup", [2000, 905], 0.85, flip=True, moves=[mv("chases|35%", 1.2, (1500, 905))]),
                    A("puff", "pb_puff", [700, 720], 1.0, {}, at="noisemakers|60%", sets=[st("occasionally|75%", 0.4, on=2.8)], front=True)],
                   scene_p={"sign": True}, card_at="Churchill|5%", meter_at="away|50%",
                   sfx=["thud@noisemakers|60%", "hit@noisemakers|62%"], shake=["noisemakers|61%"])
    T["s7.l2"] = S("pb_facility", [960, 620, 1.0], [980, 630, 1.04],
                   [bear([1635, 900], 0.42, "cub", age="cub", pose="lie"), label("sm", "BROCHURE PDF DATED 2010", [500, 980], 30)],
                   scene_p={"view": "cells"}, card_at="five|50%", card_w=1700, card_px=92, meter_at="held|35%",
                   sfx=["tink@five|50%", "tink@heated|80%"])
    T["s7.l3"] = S("pb_facility", [1000, 620, 1.05], [1020, 630, 1.1],
                   [A("fb", "pb_fanbubble", [560, 330], 0.75, at="fan|25%", sets=[st("suitcase|45%", 0.3, on=0.0)]),
                    guide([1180, 900], 0.62, idn="staff", cap=None, lanyard=True, head="#c99068", arm="down",
                          sets=[st("no|80%", 0.2, shake=1.0, arm="point", mood="frown")]),
                    review("THE BEARS GOT|THE AIR CONDITIONING.", "star|92%", (1450, 380), 0.65)],
                   scene_p={"view": "door"},
                   mbx=M("point", (860, 905), 500, prop="suitcase", sweat=True, look=[1050, 700],
                         moves=[mv(0.0, 0.01, (300, 905)), mv("suitcase|45%", 1.0, (860, 905), walk=True)],
                         gest=[["no|80%", "shock", 1.5]]),
                   sfx=["step@suitcase|45%", "boing@no|80%", "stamp@star|92%"])
    T["s7.l4"] = S(B, [0, 0, 1.0], [0, 15, 1.03],
                   [A("br", "pb_sheet", [0, 170], 0.8, {"kind": "brochure", "title": "IF YOU MEET A POLAR BEAR (MANITOBA)",
                                                        "title_px": 42, "left": True, "px": 44, "w": 980, "h": 620, "ticks": 0.0,
                                                        "rows": ["STAY CALM", "STAY WITH YOUR GROUP", "BACK AWAY, FACING THE BEAR AT ALL TIMES",
                                                                 "DO NOT TURN AND RUN", "DO NOT PLAY DEAD",
                                                                 "GET INTO A VEHICLE OR A BUILDING"]},
                      sets=[st("calm|25%", 0.2, ticks=1.0), st("group|35%", 0.2, ticks=2.0), st("facing|50%", 0.2, ticks=3.0),
                            st("run|62%", 0.2, ticks=4.0), st("dead|72%", 0.2, ticks=5.0), st("vehicle|85%", 0.2, ticks=6.0)])],
                   card_at="visitors|15%", card_px=96, sfx=["tink@calm|25%", "tink@group|35%", "tink@facing|50%", "tink@run|62%",
                                                           "tink@dead|72%", "tink@vehicle|85%"], norecut=True)
    T["s7.l5"] = S("pb_motel", [1000, 620, 1.05], [1010, 620, 1.1],
                   [A("palm", "pb_palm", [1380, 520], 0.9, {"turn": 0.0, "up": 0.0}, at="hand|75%",
                      sets=[st("hand+0.6|88%", 0.3, turn=1.0), st("hand+1.2|95%", 0.8, up=1.0)], front=True)],
                   scene_p={"kind": "room"},
                   mbx=M("think", (760, 905), 500, gest=[["hand|75%", "think", 1.5]]), sfx=["scratch@wrote|65%"])
    T["s7.l6"] = S(B, [0, 0, 1.0], [0, 10, 1.03],
                   [A("map", "pb_map", [-480, 150], 0.62, {"countries": 0.0}, sets=[st("five|50%", 0.8, countries=1.0)]),
                    A("tb", "pb_timebar", [460, 160], 0.55, {"a": 1870, "b": 2014, "g": 0.0}, sets=[st("1870|80%", 1.2, g=1.0)])],
                   sfx=["pop@five|50%", "whoosh@1870|80%"], norecut=True)
    T["s7.l7"] = S(B, [0, 0, 1.0], [0, 10, 1.04],
                   [A("cnt", "pb_counters", [0, 120], 1.0, {"n": 0.0, "small": "RECORDED ATTACKS, FIVE COUNTRIES"},
                      sets=[st("73|5%", 0.6, n=1.0), st("20|25%", 0.6, n=2.0), st("63|50%", 0.6, n=3.0)])],
                   card_at="73|5%", card_px=96, sfx=["stamp@73|5%", "stamp@20|25%", "stamp@63|50%"], norecut=True)
    T["s7.l8"] = S("pb_town", [700, 600, 1.0], [720, 610, 1.05],
                   [bear([-100, 900], 0.32, "hero", age="male", thin=1.0, sil=0.9, flip=False, moves=[mv(0.5, 6.0, (250, 900), walk=True)])],
                   scene_p={"dusk": 1.0, "sign": False}, card_at="rare|70%", sfx=["thud@harmless|90%"])
    T["s7.l9"] = S("pb_ice", [960, 600, 1.0], [980, 610, 1.05],
                   [bear([500, 900], 0.6, "hero", age="male", moves=[mv(0.2, 3.0, (1300, 900), walk=True)]),
                    A("pages", "pb_pages", [700, 380], 0.8, {"n": 6, "fall": 0.0, "mode": "fly"}, sets=[st("Time|60%", 1.6, fall=1.0)], front=True)],
                   scene_p={"kind": "newice", "freeze": 0.8}, sfx=["whoosh@Time|60%"])
    # =========================================================================================== 8. time
    T["s8.l0"] = S("pb_ice", WIDE, [960, 560, 1.06],
                   [A("pages", "pb_pages", [300, 450], 1.0, {"n": 8, "fall": 0.0, "mode": "fly"}, sets=[st(0.1, 2.0, fall=1.0)])],
                   scene_p=ICE, sfx=["whoosh@0.1"])
    T["s8.l1"] = S(B, [0, 0, 1.0], [0, 15, 1.04],
                   [A("cand", "pb_candles", [-40, 150], 1.0, {"lit": 0.0}, sets=[st("few|20%", 2.0, lit=25.0)])],
                   card_at="25|80%", sfx=["tink@25|85%"], norecut=True)
    T["s8.l2"] = S("pb_ice", [960, 600, 1.05], [960, 610, 1.08],
                   [A("cart", "pb_cart", [2300, 905], 1.0, moves=[mv("wheeled|45%", 0.01, (2300, 905)), mv("wheeled+0.1|47%", 2.0, (900, 905))]),
                    guide([2600, 900], 0.6, arm="push", moves=[mv("wheeled+0.1|47%", 2.0, (1200, 900), walk=True)]),
                    review("1 STAR.", "star|90%", (1450, 420), 0.65, sign="THE KNEES")],
                   scene_p=ICE,
                   mbx=M("neutral", (300, 905), 480, prop="stick",
                         moves=[mv("afternoon|20%", 1.0, (600, 905), walk=True), mv("wheeled|45%", 0.01, (2350, 790), rot=-85),
                                mv("wheeled+0.1|47%", 2.0, (950, 790), rot=-85)]),
                   sfx=["step@tried|25%", "boing@wheeled|45%", "stamp@star|90%"])
    T["s8.l2"]["mb"]["shake"] = 0.4
    T["s8.l2"]["sheet_at"] = 0.85
    T["s8.l3"] = S(B, [0, 0, 1.0], [-30, 10, 1.04],
                   [A("dial", "pb_dial", [-260, -10], 0.95, {"v": 86.0, "final": 97, "label": "ADULT FEMALES",
                                                            "small": "ALASKAN BEAUFORT SEA, 12-YEAR STUDY"},
                      sets=[st("chance|50%", 0.6, v=97.0)]),
                    bear([500, 380], 0.48, "mom")],
                   card_at="97|80%", meter_at="97|85%", sfx=["click@97|80%"], norecut=True)
    T["s8.l4"] = S(B, [0, 0, 1.0], [0, 15, 1.04],
                   [A("list", "pb_sheet", [0, 180], 0.75, {"kind": "report", "title": "DOCUMENTED ADULT FEMALE DEATHS", "title_px": 40,
                                                         "rows": ["- - - - - - - - - - - -"] * 7, "marks": 0.0, "px": 44,
                                                         "small": "LOCAL HUNTERS, THAT STUDY ONLY"},
                      sets=[st("Shooting|20%", 1.6, marks=6.0)])],
                   card_at="85|60%", meter_at="85|70%", sfx=["tink@Shooting|20%"], norecut=True)
    T["s8.l5"] = S(B, [0, 0, 1.0], [0, 15, 1.03],
                   [A("bands", "pb_bands", [0, 60], 0.9, {"g": 0.0}, sets=[st("class|30%", 1.2, g=1.0)]),
                    bear([-1000, 470], 0.3, "hero", age="old", moves=[mv(0.5, 9.0, (-650, 470), walk=True)])],
                   card_at="37|45%", card_px=96, meter_at="62|55%", sfx=["whoosh@class|30%"], norecut=True)
    # =========================================================================================== 9. what you got
    T["s9.l0"] = S("pb_ice", [960, 600, 1.0], [960, 610, 1.05],
                   [bear([960, 900], 0.55, "hero", age="old", pose="lie")],
                   scene_p={"kind": "pack", "dusk": 1.0},
                   chips8={"n0": 8.0, "filled0": 8.0, "y": 300, "sets": [st(0.1, 0.1, pulse=1.0)]},
                   meter_blink="Raw|60%", sfx=["boing@Raw|60%"])
    T["s9.l1"] = S("pb_den", [hnf[0] + 40, hnf[1] - 20, 2.0], [hnf[0] + 20, hnf[1] - 20, 2.1],
                   [bear(mom0, 0.78, "mom", pose="curl", shut=True),
                    bear(nb0, 1.0, "hero", age="newborn", pose="lie", wiggle=0.6, flip=True, tag=True)],
                   sfx=["tink@handed|60%"])
    hm = head([700, 900], 1.25, "male")
    T["s9.l2"] = S("pb_ice", [880, 450, 0.95], [900, 450, 1.0],
                   [bear([560, 900], 1.25, "hero", age="male", look=[0.8, 0])],
                   scene_p=ICE, card_at="largest|40%", meter_at="predator|80%", sfx=["sting@largest|40%"])
    T["s9.l3"] = S(B, [0, 0, 1.0], [0, 15, 1.04],
                   [A("coat", "pb_coat", [-120, 90], 1.0, {"labels": 0.0},
                      sets=[st("coat|15%", 0.3, labels=1.0), st("underfur|35%", 0.3, labels=2.0), st("fat|55%", 0.3, labels=4.0)])],
                   meter_at="cold|90%", sfx=["tink@coat|15%", "tink@underfur|35%", "tink@fat|55%"], norecut=True)
    T["s9.l4"] = S(B, [0, 0, 1.0], [0, 10, 1.06],
                   [A("skin", "pb_skin", [0, 120], 1.0, {"part": 0.0}, sets=[st("black|75%", 1.0, part=1.0)])],
                   card_at="black|80%", meter_at="black|85%", sfx=["whoosh@black|75%"], norecut=True)
    T["s9.l5"] = S("pb_ice", WIDE, [960, 560, 1.03],
                   [bear([420, 900], 0.6, "hero", age="male"), A("div", "pb_divider", [0, 0], 1.0, {"x": 960}, front=True)],
                   scene_p=ICE,
                   mbx=M("think", (1400, 905), 400, coats=True, parka=False,
                         gest=[["arms|30%", "shock", 1.0]],
                         moves=[mv("Badass|80%", 0.15, (1400, 905), rot=0), mv("grew|65%", 1.4, (1750, 960), rot=300)]),
                   sfx=["boing@arms|30%", "whoosh@grew|65%"])
    T["s9.l6"] = S("pb_slope", [1500, 640, 1.15], [1500, 640, 1.2], [],
                   mbx=M("present", (1500, 600), 400, coats=True, parka=False, prop="card", moves=[mv(0.0, 0.01, (1500, 600), rot=180)]),
                   sfx=["stamp@star|40%"])
    T["s9.l7"] = S(B, [0, 0, 1.0], [0, 10, 1.03],
                   [A("map", "pb_map", [0, 100], 0.62, {"bears": 0.0}, sets=[st("estimates|30%", 2.0, bears=1.0)])],
                   card_at="26,000|60%", meter_at="2023|85%", sfx=["tink@26,000|60%"], norecut=True)
    # =========================================================================================== 10. the verdict
    T["s10.l0"] = S(B, [0, 0, 1.0], [0, 10, 1.03],
                    [A("map", "pb_map", [-480, 140], 0.6, {"q": 0.0}, sets=[st("ice|70%", 0.4, q=1.0)]),
                     A("led", "pb_ledger", [460, 150], 0.75, at="ledger|30%")],
                    sfx=["pop@ledger|30%", "boing@ice|70%"], norecut=True)
    T["s10.l1"] = S(B, [0, 0, 1.0], [0, 10, 1.03],
                    [A("map", "pb_map", [-480, 140], 0.6, {"dots": ["SOUTHERN BEAUFORT SEA"]}),
                     A("bar", "pb_dropbar", [480, 380], 0.85, {"g": 0.0}, sets=[st("drop|70%", 1.0, g=1.0)])],
                    card_at="drop|70%", meter_at="drop|80%", sfx=["thud@drop|70%"], norecut=True)
    T["s10.l2"] = S(B, [0, 0, 1.0], [0, 10, 1.03],
                    [A("map", "pb_map", [-560, 140], 0.55, {"dots": ["SVALBARD"]}),
                     A("line", "pb_line", [380, 150], 0.7, {"grow": 0.0}, sets=[st("fell|60%", 1.0, grow=1.0)])],
                    sfx=["pop@Svalbard|10%", "whoosh@fell|60%"], norecut=True)
    T["s10.l3"] = S(B, [80, 60, 1.25], [80, 60, 1.32],
                    [A("line", "pb_line", [380, 150], 0.7, {"grow": 1.0, "rise": 0.0}, sets=[st("rose|10%", 1.4, rise=1.0)]),
                     label("sm", "770 ADULTS, 1995 TO 2019", [380, 400], 30)],
                    card_at="rose|15%", meter_at="rose|20%", sfx=["boing@rose|15%"], norecut=True)
    T["s10.l4"] = S(B, [0, 0, 1.0], [0, 10, 1.03],
                    [A("yrs", "pb_years", [0, 150], 1.0, {"mark": 0.0}, sets=[st("19|60%", 1.5, mark=1.0)])],
                    card_at="19|60%", card_px=96, meter_at="years|90%", sfx=["tink@19|60%"], norecut=True)
    T["s10.l5"] = S(B, [0, 0, 1.0], [0, 10, 1.04],
                    [A("map", "pb_map", [0, 160], 0.75, {"dots": ["SOUTHERN BEAUFORT SEA", "SVALBARD"]}),
                     label("dw", "DEPENDS WHERE", [0, -200], 80, color="#ffd34d", at="deal|60%")],
                    sfx=["pop@deal|60%"], norecut=True)
    T["s10.l6"] = S("pb_den", [hnf[0] + 60, hnf[1] - 40, 2.3], [hnf[0] + 20, hnf[1] - 30, 2.05], den_pair,
                    sfx=["whoosh@0.05"], recut=False,
                    shots=[cam([hnf[0] + 60, hnf[1] - 40, 2.3], [hnf[0] + 20, hnf[1] - 30, 2.05]),
                           cam([hnf[0] - 40, hnf[1] - 10, 3.2], [hnf[0] - 40, hnf[1] - 10, 3.4], at="Eyes|60%", dur=0.5)])
    T["s10.l7"] = S("pb_ice", [960, 620, 1.1], [960, 620, 1.15],
                    [bear([900, 900], 1.3, "nb", age="newborn", pose="lie", wiggle=0.4, sets=[st("grow|25%", 1.0, a=0.0)]),
                     bear([820, 900], 0.95, "hero", age="male", pose="lie", a=0.0, sets=[st("grow|25%", 1.0, a=1.0)])],
                    scene_p=ICE, meter_at="badass|80%", sfx=["whoosh@grow|25%"])
    T["s10.l8"] = S("pb_ice", [960, 600, 1.0], [960, 610, 1.04],
                    [bear([1400, 900], 0.45, "hero", age="male", moves=[mv(0.3, 8.0, (600, 900), walk=True)], flip=True),
                     label("fine", "DEPENDS ON YOUR ICE", [960, 750], 44, at="fine|75%")],
                    scene_p=ICE, no_card=True,
                    stamps=[{"text": "RAW START. SWEET IF YOU GET THROUGH.", "at": "start|35%", "px": 72, "y": 560, "color": "#e5383b"}],
                    meter_swing=[40, "start|35%", "sweet|60%"], meter_at="sweet|60%", sfx=["boing@sweet|60%"])
    T["s10.l9"] = S("pb_desk", WIDE, [960, 560, 1.04],
                    [A("stack", "pb_reviews", [960, 430], 0.6, {"n": 9, "mode": "stack", "top": "WOULD NOT BE|BORN AGAIN."},
                       at="review|20%", front=True),
                     guide([1350, 900], 0.62, arm="down", sets=[st("again|85%", 0.2, arm="boots")])],
                    mbx=M("present", (650, 905), 500, gest=[["star|45%", "point", 1.2]]),
                    sfx=["stamp@star|45%", "boing@again|85%"])
    T["s10.l10"] = S(B, [0, 0, 1.0], [0, 10, 1.03],
                     [A("cm", "pb_comment", [0, 220], 1.0, at="pinned|15%"), pill("YOUR REVIEW?", "yours|35%")],
                     chips8={"n0": 8.0, "filled0": 8.0, "y": 380, "sets": []}, sfx=["pop@pinned|15%"], norecut=True)
    T["s10.l11"] = S("pb_desk", WIDE, [960, 560, 1.04], [],
                     scene_p={"cat": 1.0},
                     mbx=M("point", (1050, 905), 500, prop="ticket_new", look=[1650, 450],
                           gest=[["Indoors|35%", "present", 1.0], ["litter|55%", "laugh", 1.2], ["right|90%", "point", 1.5]]),
                     sfx=["thud@booked|15%", "boing@litter|55%"])
    # unique actor ids per line: drawn.plan merges an actor's p, rot and flip from the last line when the id and
    # type match, so a pose, a tumble or a silhouette would leak into the next shot
    for sid, d in T.items():
        if d.get("norecut") and not d.get("shots"):   # a still board gets a soft push every fifth of the line (no framing > 4 s)
            c0, c1 = list(d["cam"]), list(d["to"])
            steps = [c0]
            for k in range(1, 6):
                u = k / 5
                steps.append([round(c0[0] + (c1[0] - c0[0]) * u + (12 if k % 2 else -8), 2),
                              round(c0[1] + (c1[1] - c0[1]) * u + (6 if k % 2 else 0), 2),
                              round(c0[2] + (c1[2] - c0[2]) * u + 0.015 * (1 if k % 2 else -1), 4)])
            d["shots"] = [cam(steps[0], steps[1])] + [cam(steps[k], steps[k + 1], at=f"{20 * k}%", dur=0.6) for k in range(1, 5)]
        for a in d["actors"]:
            a["id"] = a["id"] + "@" + sid
            a.setdefault("rot", 0.0)
            a.setdefault("flip", False)
    return T
