"""The hand-made shots for the house-cat long-form (tools/drawn_catlife.py): spec line id -> recipe + args, one entry
per outline line (s<segment>.l<line>), drawn from that line's `vis`. Word anchors fall back to a share ("word|40%").
World: rooms (cl_room), the village and the street have their floor at y = 900 and fill x 0..1920 at zoom 1; boards
(ds_board_bg) are centred on (0, 0). Cards sit at the top (screen y 150) unless a shot moves them, so every subject
is kept below screen y ~300.

Format keys a shot may carry (read by drawn_catlife.expand): meter_in, meter_at, meter_blink, meter_swing,
meter_climb, chips8 {n0, filled0, y, sets}, stamps [...], card_at, card_y, card_x, card_w, card_px, no_card, pad,
tint, flash, shake, sheet_at, norecut, recut (False), top_actors."""
from drawn_dontsquish import GREEN, RED, YEL, actor, cam, mb

HID = {"hidden": True, "pose": "neutral", "pos": [-3000, 1500], "size": 600}
WIDE = [960, 540, 1.0]
B = "ds_board_bg"
BOARD = {"color": "#1f1b2e"}
R = "cl_room"


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
        st = list(sets or [])
        if at:
            pp["on"] = 0.0
            st = [{"at": at, "dur": dur, "p": {"on": 1.0}}] + st
        return actor(idn, typ, pos, s, pp, st or None, moves, front=front, flip=flip, rot=rot)

    def cat(pos, s=0.55, idn="hero", sets=None, moves=None, flip=False, front=False, **p):
        p.setdefault("look", [1, 0])
        return actor(idn, "cl_cat", pos, s, p, sets, moves, front=front, flip=flip)

    def M(pose, pos, size=600, look="viewer", **kw):
        return mb(pose, tuple(pos), size, look=look, **kw)

    def mv(at, dur, pos, **kw):
        return dict({"at": at, "dur": dur, "pos": list(pos)}, **kw)

    def st(at, dur=0.3, **p):
        return {"at": at, "dur": dur, "p": p}

    def tint(mode, a0, a1=None, at="10%", dur=0.8):
        sets = [st(at, dur, a=a1)] if a1 is not None else None
        return A("tint", "cl_tint", [0, 0], 1.0, {"mode": mode, "a": a0}, sets=sets, front=True)

    def head(pos, s, age="adult"):
        """World point of a standing cat's head centre (for close-ups)."""
        L, Hh, ll = (330, 215, 78) if age == "kitten" else (520, 250, 150)
        by = -ll - Hh * 0.35
        return [pos[0] + L * 0.48 * s + Hh * 0.1 * s, pos[1] + (by - Hh * 0.38) * s]

    # =========================================================================================== 0. day one (cold open)
    k0 = [900, 860]
    hk = head(k0, 1.6, "kitten")
    T["s0.l0"] = S("cl_blanket", [hk[0] - 60, hk[1] - 100, 1.55], [hk[0] - 140, hk[1] - 80, 1.4],
                   [cat(k0, 1.6, age="kitten", shut=True, wiggle=1.0, mood="calm")],
                   card_at="cat|60%", sfx=["sting@0.02"], sheet_at=0.75, recut=False,
                   shots=[cam([hk[0] - 60, hk[1] - 100, 1.55], [hk[0] - 100, hk[1] - 85, 1.47]),
                          cam([hk[0] - 100, hk[1] - 85, 1.47], [hk[0] - 160, hk[1] - 70, 1.38], at="house|50%", dur=0.9)])
    T["s0.l1"] = S("cl_blanket", [hk[0] + 30, hk[1] + 10, 3.0], [hk[0] + 30, hk[1] + 20, 3.25],
                   [cat(k0, 1.6, age="kitten", shut=True, wiggle=0.5),
                    A("cal", "cl_cal", [hk[0] - 210, hk[1] + 40], 0.32, {"day": 7.0}, at="open|30%",
                      sets=[st("week|45%", 2.2, day=10.0)], front=True)],
                   sfx=["whoosh@0.02", "tink@ten|85%"])
    kits = [cat([520, 880], 0.95, "k1", age="kitten", shut=True, wiggle=1.0),
            cat([830, 900], 1.0, "k2", age="kitten", shut=True, wiggle=0.8, flip=True),
            cat([1130, 870], 0.95, "hero", age="kitten", shut=True, wiggle=1.0),
            cat([1430, 900], 0.9, "k4", age="kitten", shut=True, wiggle=0.7, flip=True)]
    T["s0.l2"] = S("cl_blanket", [960, 640, 1.5], None, kits + [
                   A("cnt", "cl_count", [960, 540], 0.85, {"v": 0.0}, sets=[st("siblings|25%", 1.6, v=4.4)], front=True)],
                   shots=[cam([1000, 680, 1.55], [960, 640, 1.0], dur=1.4)], card_at="Litters|45%",
                   sfx=["pop@average|40%", "pop@four|85%"], norecut=True)
    T["s0.l3"] = S("cl_blanket", [960, 600, 1.0], [960, 580, 1.05],
                   [cat([960, 1010], 0.9, age="kitten", shut=True, wiggle=0.6),
                    A("deal", "cl_parch", [960, 540], 0.82, {"mode": "deal", "paw": 0.0, "unroll": 0.0},
                      sets=[st("deal|15%", 0.9, unroll=1.0), st("thousands|60%", 0.35, paw=1.0)], front=True)],
                   sfx=["whoosh@deal|15%", "stamp@thousands|60%"], norecut=True)
    T["s0.l4"] = S("cl_blanket", [960, 560, 1.0], [960, 560, 1.04],
                   [cat([960, 1000], 1.1, age="kitten", shut=True, wiggle=0.5)],
                   chips8={"n0": 0.0, "y": 470, "sets": [st("Eight|5%", 1.6, n=8.0)]},
                   card_at="Eight|10%", card_y=150, sfx=["pop@Eight|10%", "tink@order|70%"], norecut=True)
    T["s0.l5"] = S("cl_blanket", [1060, 640, 1.25], [1100, 650, 1.32],
                   [cat([900, 900], 1.3, age="kitten", shut=True, wiggle=0.8)],
                   meter_in="Raw|30%", sfx=["boing@sweet|80%"])
    # =========================================================================================== 1. the deal you never signed
    T["s1.l0"] = S("cl_village", WIDE, [960, 560, 1.05],
                   [cat([2100, 900], 0.55, age="wild", moves=[mv(0.1, 2.0, (1250, 900), walk=True)], flip=True)],
                   sfx=["step@deal|40%"])
    T["s1.l1"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [A("map", "cl_map", [0, 130], 0.95, {"near": 0.0}, sets=[st("Near|50%", 0.4, near=1.0)])],
                   card_at="979|35%", sfx=["pop@Near|50%"], norecut=True)
    jars = [A("j1", "cl_jar", [470, 900], 0.75), A("j2", "cl_jar", [640, 905], 0.6, {"col": "#c98a5a"}),
            A("j3", "cl_jar", [1280, 900], 0.8, {"grain": 1.0}), A("j4", "cl_jar", [1500, 905], 0.65, {"col": "#a8603e"})]
    T["s1.l2"] = S("cl_village", [900, 560, 1.15], [1000, 580, 1.0], jars, sfx=["whoosh@0.05"])
    T["s1.l3"] = S("cl_village", [900, 640, 1.2], [960, 640, 1.26], jars + [
                   cat([150, 900], 0.5, age="wild", moves=[mv(0.05, 2.4, (820, 900), walk=True)]),
                   A("mouse", "cl_mouse", [1120, 900], 0.55, {"freeze": 0.0}, sets=[st("mice|50%", 0.2, freeze=1.0)])],
                   card_at="mice|45%", sfx=["step@ancestors|25%", "pop@mice|55%"])
    T["s1.l4"] = S("cl_village", [990, 720, 1.6], [990, 730, 1.68], jars + [
                   cat([760, 905], 0.55, age="wild", sets=[st("moved|45%", 0.6, sit=0.75, mood="smug")],
                       moves=[mv(0.05, 0.9, (930, 905), walk=True)])],
                   sfx=["thud@moved|50%"])
    T["s1.l5"] = S(B, [0, 0, 1.0], [-40, 20, 1.05],
                   [A("map", "cl_map", [0, 130], 0.95, {"near": 1.0, "cyprus": 0.0}, sets=[st("Cyprus|40%", 0.4, cyprus=1.0)])],
                   card_at="9,500|60%", sfx=["pop@Cyprus|40%"], norecut=True)
    T["s1.l6"] = S("cl_village", [960, 620, 1.05], [960, 640, 1.1],
                   [cat([360, 905], 0.5, "feral", age="wild", stripes=True, look=[1, 0.1]),
                    cat([1380, 905], 0.5, "hero", age="wild", look=[-1, 0.1], flip=True)],
                   mbx=M("think", (960, 905), 560, look="feral", gest=[["tabby|45%", "deadpan", 1.0], ["wildcat|80%", "think", 1.0]]),
                   sfx=["tink@tabby|45%"])
    T["s1.l7"] = S(R, [900, 720, 1.55], [920, 730, 1.62],
                   [A("box", "cl_litter", [920, 905], 1.1, {"col": "#6aa0c8"}),
                    cat([840, 870], 0.62, age="kitten", mood="angry", look=[1, 0], stripes=True),
                    A("clk", "cl_clock", [1330, 450], 0.45, {"mode": "wall", "hr": 2.0, "mn": 50.0}, at="clock|70%")],
                   scene_p={"kind": "living"}, meter_at="clock|70%", sfx=["boing@litter|45%", "tink@clock|70%"])
    # =========================================================================================== 2. the five-week window
    T["s2.l0"] = S(R, WIDE, [960, 560, 1.05],
                   [cat([1400, 900], 0.55, age="kitten", moves=[mv(0.1, 1.6, (900, 900), walk=True)], flip=True)],
                   scene_p={"kind": "living"}, sfx=["step@five|50%"])
    T["s2.l1"] = S(B, [0, 0, 1.0], [0, 10, 1.04],
                   [A("tl", "cl_timeline", [0, 120], 1.0, {"lit": 0.0, "run": 0.0}, sets=[st("socialization|40%", 1.4, lit=1.0, run=7.0)])],
                   card_at="two|65%", sfx=["whoosh@socialization|40%"], norecut=True)
    T["s2.l2"] = S(R, [1050, 560, 1.15], [1060, 570, 1.2],
                   [A("hrt", "cl_heart", [1180, 330], 0.5, at="outgoing|55%", front=True)],
                   mbx=M("present", (1180, 905), 640, look="viewer", prop="kitten", gest=[["outgoing|55%", "laugh", 1.5]]),
                   scene_p={"kind": "living"}, sfx=["pop@outgoing|55%"])
    T["s2.l3"] = S(R, [960, 560, 1.0], [960, 580, 1.06],
                   [A("clk", "cl_clock", [1250, 400], 0.75, {"mode": "wall", "hr": 3.0, "mn": 0.0}),
                    cat([700, 900], 0.5, age="kitten", mood="happy",
                        moves=[mv(0.2, 0.45, (760, 900), face=-1), mv(0.7, 0.45, (700, 900), face=1), mv(1.2, 0.45, (760, 900), face=-1),
                               mv(1.7, 0.45, (700, 900), face=1), mv(2.2, 0.45, (760, 900), face=-1), mv(2.7, 0.45, (700, 900), face=1)])],
                   scene_p={"kind": "living"}, sfx=["tink@running|45%", "boing@three|80%"])
    T["s2.l4"] = S(R, [960, 560, 1.3], [980, 570, 1.36], [],
                   mbx=M("present", (900, 905), 660, look="viewer", prop="kitten_sub", gest=[["sandwich|80%", "deadpan", 1.5]]),
                   scene_p={"kind": "living"}, sfx=["boing@sandwich|80%"], meter_at="sandwich|75%")
    # =========================================================================================== 3. your senses
    T["s3.l0"] = S(R, WIDE, [960, 560, 1.05],
                   [cat([800, 900], 0.55, sit=0.6, look=[1, -0.3]), A("rug", "cl_rug", [800, 920], 0.6)],
                   scene_p={"kind": "living"}, sfx=["whoosh@senses|50%"])
    T["s3.l1"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [A("pz", "cl_puzzle", [0, 150], 0.8, {"crack": 0.0}, sets=[st("broken|70%", 0.5, crack=1.0)])],
                   card_at="broken|70%", meter_at="broken|75%", sfx=["crunch@broken|70%"], norecut=True)
    T["s3.l2"] = S(R, [960, 600, 1.1], [980, 600, 1.16],
                   [cat([660, 905], 0.55, mood="smug", look=[0.8, -0.7])],
                   mbx=M("present", (1200, 905), 640, look="hero", prop="cake", gest=[["wasted|45%", "shrug", 1.4]]),
                   scene_p={"kind": "living"}, sfx=["pop@cake|15%"])
    T["s3.l3"] = S(R, WIDE, [980, 560, 1.06],
                   [cat([960, 900], 0.55, look=[1, -0.2]),
                    A("grey", "cl_tint", [0, 0], 1.0, {"mode": "grey", "a": 0.0}, sets=[st("fewer|30%", 1.2, a=0.6)], front=True)],
                   scene_p={"kind": "living"}, sfx=["whoosh@fewer|30%"])
    hc = head([700, 900], 0.8)
    T["s3.l4"] = S(R, [hc[0] + 150, hc[1] - 40, 2.0], [hc[0] + 170, hc[1] - 30, 2.08],
                   [cat([700, 900], 0.8, look=[1, 0.2]),
                    A("toy", "cl_toy", [hc[0] + 260, hc[1] + 120], 0.7, {"kind": "ball", "blur": 0.0}, sets=[st("limited|55%", 0.8, blur=1.0)])],
                   scene_p={"kind": "living"}, sfx=["whoosh@limited|55%"])
    T["s3.l5"] = S(R, WIDE, [960, 560, 1.06],
                   [cat([960, 900], 0.55, look=[1, -0.2]), tint("dark", 0.0, 0.6, "here's|20%", 1.0)],
                   scene_p={"kind": "living"}, sfx=["click@here's|20%"])
    T["s3.l6"] = S(R, WIDE, [960, 560, 1.05],
                   [A("chair", "cl_chair", [760, 900], 1.0),
                    cat([1800, 900], 0.5, moves=[mv(0.1, 2.6, (300, 900), walk=True)], flip=True), tint("dark", 0.6)],
                   mbx=M("neutral", (250, 905), 600, look="viewer", moves=[mv(0.1, 1.0, (640, 905), walk=True)],
                         gest=[["six|50%", "shock", 1.5]]),
                   shake=["six|50%"], card_at="dim|20%", meter_at="six|60%", sfx=["thud@six|50%"])
    T["s3.l7"] = S(R, WIDE, [960, 560, 1.04],
                   [A("chair", "cl_chair", [760, 900], 1.0), tint("dark", 0.6, 0.94, "dark|10%", 0.5),
                    A("eyes", "cl_eyes", [1500, 760], 0.7, {"blink": 0.0}, front=True,
                      sets=[st("myth|35%", 0.12, blink=1.0), st("myth|45%", 0.12, blink=0.0)],
                      moves=[mv("still|55%", 0.8, (870, 760))])],
                   shake=["light|90%"], sfx=["thud@light|90%"])
    T["s3.l8"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [A("hb", "cl_hearing", [0, 160], 1.0, {"grow": 0.08}, sets=[st("hertz|40%", 2.0, grow=1.0)])],
                   card_at="hertz|45%", card_w=1600, sfx=["whoosh@hertz|40%"], norecut=True)
    T["s3.l9"] = S(R, [hc[0] - 30, hc[1] - 70, 1.7], [hc[0] - 30, hc[1] - 60, 1.78],
                   [cat([700, 900], 0.8, look=[1, -0.3], radar=1.0)],
                   scene_p={"kind": "living"}, sfx=["tink@widest|40%"])
    T["s3.l10"] = S(R, [950, 760, 1.6], [960, 770, 1.68],
                    [cat([760, 905], 0.55, look=[1, 0.8], mood="worry"), A("bowl", "cl_bowl", [1180, 905], 0.75)],
                    scene_p={"kind": "living"}, sfx=["boing@menu|70%"])
    # =========================================================================================== 4. your dinner
    T["s4.l0"] = S(R, WIDE, [960, 560, 1.05],
                   [cat([700, 900], 0.55, look=[1, 0.6]), A("bowl", "cl_bowl", [1050, 900], 0.75)],
                   scene_p={"kind": "kitchen"}, sfx=["tink@menu|60%"])
    T["s4.l1"] = S("cl_village", [960, 680, 1.25], [980, 690, 1.3],
                   [cat([620, 905], 0.55, age="wild", look=[1, 0.3]),
                    A("mouse", "cl_mouse", [1200, 905], 0.7, {"freeze": 1.0, "label": 0.0}, sets=[st("carbs|50%", 0.4, label=1.0)], flip=True)],
                   card_at="obligate|25%", sfx=["pop@carbs|50%"])
    T["s4.l2"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [cat([-60, 500], 1.0, look=[1, 0], xray=0.0, sets=[st("taurine|30%", 0.6, xray=1.0)]),
                    A("fac", "cl_factory", [-70, 290], 0.36, {"closed": 0.0}, sets=[st("little|45%", 0.5, closed=1.0)], front=True)],
                   scene_p={"color": "#3a4660"}, card_at="food|70%", sfx=["whoosh@taurine|30%", "thud@little|50%"], norecut=True)
    T["s4.l3"] = S(R, [900, 560, 1.0], [940, 570, 1.06],
                   [A("desk", "cl_desk", [760, 905], 0.95), A("cal", "cl_cal", [1500, 470], 0.65, {"mode": "label", "label": "1987"})],
                   scene_p={"kind": "clinic"}, card_at="1987|10%", card_x=700, sfx=["pop@1987|10%"])
    cans = [A(f"c{i}", "cl_can", [-480 + i * 320, 330], 0.95, {"col": ["#3b7dd8", "#c0392b", "#2f8f8a", "#d98a2a"][i]}) for i in range(4)]
    cans[2]["p"].update(spin=0.0, label="?")
    cans[2]["set"] = [st("commercial|60%", 0.8, spin=1.0)]
    T["s4.l4"] = S(B, [0, 0, 1.0], [0, 20, 1.04], cans, card_at="21|35%", sfx=["whoosh@commercial|60%"], norecut=True)
    T["s4.l5"] = S(B, [0, 40, 1.0], [0, 40, 1.08],
                   [A("drop", "cl_dropper", [0, 200], 1.1, {"drip": 0.0}, sets=[st("taurine|50%", 0.7, drip=0.99)]),
                    A("bowl", "cl_bowl", [0, 520], 1.0, {"full": 1.0, "col": "#c0392b"})],
                   sfx=["tink@taurine|70%"], norecut=True)
    T["s4.l6"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [A("ekg", "cl_heartline", [0, 160], 1.0, {"strong": 0.0}, sets=[st("heart|25%", 1.4, strong=1.0)])],
                   card_at="normal|70%", meter_at="normal|70%", sfx=["tink@normal|75%"], norecut=True)
    T["s4.l7"] = S(R, [960, 560, 1.15], [990, 570, 1.2],
                   [A("can", "cl_can", [1280, 545], 0.75, {"label": "1987", "col": "#c0392b"})],
                   mbx=M("think", (900, 905), 640, look="can", gest=[["Actual|55%", "shock", 1.2], ["Damn|85%", "deadpan", 1.0]]),
                   scene_p={"kind": "kitchen"}, sfx=["boing@Actual|55%"])
    T["s4.l8"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [A("bowl", "cl_bowl", [-480, 300], 1.1, {"full": 1.0, "label": "CASEIN DIET", "col": "#b7c0c9"}),
                    A("eye", "cl_eye", [380, 120], 0.8, {"dim": 0.0}, at="light|55%", sets=[st("down|80%", 1.0, dim=1.0)])],
                   sfx=["pop@light|55%", "whoosh@down|80%"], norecut=True)
    T["s4.l9"] = S(B, [0, 0, 1.0], [0, 20, 1.05],
                   [A("fac", "cl_factory", [0, 170], 0.95, {"closed": 1.0, "under": 0.0}, sets=[st("suspect|50%", 0.5, under=1.0)])],
                   meter_at="suspect|55%", sfx=["scratch@suspect|50%"], norecut=True)
    T["s4.l10"] = S(R, [960, 600, 1.05], [980, 600, 1.1],
                    [cat([480, 905], 0.5, look=[1, 0.4]),
                     A("sau", "cl_saucer", [840, 905], 1.0, at="saucer|20%", moves=[mv("saucer|20%", 0.5, (840, 905))])],
                    mbx=M("present", (1150, 905), 640, look="sau", gest=[["ASPCA|50%", "shock", 1.4]]),
                    scene_p={"kind": "living"}, card_at="diarrhea|80%", sfx=["tink@saucer|25%"])
    T["s4.l11"] = S(R, [1150, 600, 1.1], [1170, 600, 1.16],
                    [cat([520, 905], 0.5, look=[1, 0.4], sit=0.5), A("sau", "cl_saucer", [840, 905], 1.0),
                     A("mop", "cl_mop", [1780, 905], 1.0)],
                    mbx=M("nervous", (1250, 905), 640, look="mop", gest=[["regret|40%", "nervous", 2.0]]),
                    scene_p={"kind": "living"}, meter_at="least|70%", sfx=["tink@regret|40%"])
    # =========================================================================================== 5. your house (safety block: no gags)
    T["s5.l0"] = S(R, WIDE, [980, 560, 1.06],
                   [cat([1400, 735], 0.45, sit=0.85, look=[-1, 0], flip=True)],
                   scene_p={"kind": "living"}, sfx=["whoosh@house|50%"])
    T["s5.l1"] = S(R, [960, 640, 1.2], [960, 620, 1.35],
                   [A("lily", "cl_lily", [960, 905], 0.75, {"horror": 0.0}, sets=[st("flowers|30%", 0.6, horror=1.0)]),
                    tint("dark", 0.0, 0.35, "flowers|30%", 0.6)],
                   scene_p={"kind": "living"}, sfx=["sting@flowers|35%"])
    T["s5.l2"] = S(R, [960, 620, 1.1], [980, 620, 1.15],
                   [A("lily", "cl_lily", [560, 905], 0.7, {"horror": 0.6}), cat([1300, 905], 0.5, look=[-1, -0.2], flip=True)],
                   scene_p={"kind": "living"}, card_at="lilies|35%", card_x=1150, card_w=1250, sfx=["thud@fatal|65%"])
    T["s5.l3"] = S(B, [-2000, 540, 1.0], None,
                   [A("pet", "cl_petal", [-2000, 540], 1.0, {"kind": "petal"}, rot=10),
                    A("pol", "cl_petal", [0, 540], 1.0, {"kind": "pollen"}),
                    A("wat", "cl_petal", [2000, 560], 0.85, {"kind": "water"})],
                   shots=[cam([-2000, 540, 1.0], [-2000, 540, 1.06]), cam([0, 540, 1.05], [0, 540, 1.12], at="pollen|30%", dur=0.05),
                          cam([2000, 560, 1.0], [2000, 560, 1.07], at="water|75%", dur=0.05)],
                   sfx=["whoosh@pollen|30%", "whoosh@water|75%"], norecut=True)
    T["s5.l4"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [A("cal", "cl_cal", [0, 230], 1.1, {"mode": "three", "n": 0.0}, sets=[st("kidney|20%", 1.4, n=3.0)])],
                   card_at="three|70%", meter_at="three|75%", sfx=["pop@kidney|25%", "pop@three|70%"], norecut=True)
    T["s5.l5"] = S(R, [960, 620, 1.1], [980, 630, 1.15],
                   [A("lily", "cl_lily", [720, 905], 0.7),
                    actor("dog", "cl_dog", [1300, 905], 0.5, {"queasy": 0.0, "look": [-1, 0]},
                          [st("only|35%", 0.8, queasy=1.0)], flip=True),
                    A("qm", "cl_qm", [720, 280], 1.0, {"px": 200}, at="nobody|65%", front=True)],
                   scene_p={"kind": "living"}, sfx=["pop@nobody|65%"])
    T["s5.l6"] = S(R, WIDE, [970, 560, 1.04],
                   [A("clk", "cl_clock", [520, 650], 0.62, {"h": 0.0}, sets=[st("treatment|10%", 2.8, h=18.0)]),
                    A("car", "cl_carrier", [1720, 905], 0.42)],
                   mbx=M("neutral", (1420, 905), 580, look="viewer", prop="phone", gest=[["vet|80%", "point", 1.4]]),
                   scene_p={"kind": "living", "nowin": True}, card_at="vet|78%", card_x=600, card_w=900, card_px=96,
                   sfx=["tink@eighteen|30%", "click@vet|80%"])
    T["s5.l7"] = S(R, [960, 620, 1.1], [980, 620, 1.15],
                   [A("pl1", "cl_lily", [700, 905], 0.75, {"kind": "peace", "caution": 0.0}, sets=[st("different|55%", 0.4, caution=1.0)]),
                    A("pl2", "cl_lily", [1250, 905], 0.75, {"kind": "calla", "caution": 0.0}, sets=[st("milder|75%", 0.4, caution=1.0)])],
                   scene_p={"kind": "living"}, sfx=["pop@different|55%", "pop@milder|75%"])
    T["s5.l8"] = S(R, [1020, 380, 1.4], [1020, 390, 1.5],
                   [A("cab", "cl_cabinet", [860, 90], 1.0, {"open": 0.0}, sets=[st("medicine|30%", 0.8, open=1.0)])],
                   scene_p={"kind": "bath", "nocab": True}, sfx=["scratch@medicine|30%"])
    T["s5.l9"] = S(R, [1000, 640, 1.2], [1020, 650, 1.26],
                   [A("cab", "cl_cabinet", [860, 90], 1.0, {"open": 1.0}),
                    cat([700, 905], 0.5, sit=0.6, look=[1, -0.3]), A("bot", "cl_bottle", [1230, 905], 0.7)],
                   scene_p={"kind": "bath", "nocab": True}, card_at="acetaminophen|55%", meter_at="kill|75%", sfx=["thud@kill|75%"])
    T["s5.l10"] = S(R, [1000, 600, 1.15], [1010, 610, 1.2],
                    [A("cab", "cl_cabinet", [860, 90], 1.0, {"open": 1.0}), A("bot", "cl_bottle", [880, 520], 0.4)],
                    mbx=M("neutral", (1300, 905), 640, look="viewer", prop="phone", gest=[["vet|50%", "point", 1.5]]),
                    scene_p={"kind": "bath", "nocab": True}, sfx=["click@vet|50%"])
    T["s5.l11"] = S(R, WIDE, [960, 560, 1.04],
                    [cat([420, 905], 0.5, mood="happy", look=[1, 0.4]), A("str", "cl_string", [760, 905], 1.0, {"pull": 1.0}),
                     A("gut", "cl_gut", [1380, 470], 0.62, {"tangle": 0.0}, at="block|30%", sets=[st("gut|50%", 1.0, tangle=1.0)])],
                    scene_p={"kind": "living"}, sfx=["pop@block|30%"])
    win = lambda **p: A("win", "cl_window", [700, 600], 1.0, dict({"open": 1.0, "curtain": 1.0}, **p))  # noqa: E731
    T["s5.l12"] = S(R, [700, 400, 1.35], [700, 420, 1.45], [win()],
                    scene_p={"kind": "living", "nowin": True}, sfx=["whoosh@window|60%"])
    T["s5.l13"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                    [A("row", "cl_row", [0, 330], 0.85, {"n": 14, "w": 125, "col": "#efe6d2"})],
                    card_at="119|50%", sfx=["pop@119|50%"], norecut=True)
    T["s5.l14"] = S(B, [0, 0, 1.0], [0, 10, 1.03],
                    [A("row", "cl_row", [0, 420], 0.75, {"n": 14, "w": 125}),
                     A("tick", "cl_tick", [0, 80], 1.0, {"on": 0.0}, sets=[st("lived|30%", 0.35, on=1.0)])],
                    card_at="lived|30%", sfx=["tink@lived|30%"], norecut=True)
    T["s5.l15"] = S(B, [0, 0, 1.0], [40, 20, 1.04],
                    [A("tick", "cl_tick", [-250, 80], 1.0, {"on": 1.0, "star": 0.0}, sets=[st("Four|10%", 0.4, star=1.0)]),
                     A("bill", "cl_paper", [520, 160], 0.8, {"kind": "bill"}, at="cost|65%")],
                    sfx=["pop@Four|10%", "pop@cost|65%"], norecut=True)
    T["s5.l16"] = S(R, [960, 680, 1.4], [970, 690, 1.46],
                    [cat([830, 905], 0.6, cast=True, sit=0.25, mood="worry", look=[1, 0])],
                    scene_p={"kind": "clinic"}, card_at="half|20%", sfx=["tink@limbs|35%"])
    T["s5.l17"] = S(B, [0, 0, 1.0], [0, 10, 1.04],
                    [A("w", "cl_words", [-80, 120], 1.0, {"star": 0.0}, sets=[st("asterisk|50%", 0.4, star=1.0)])],
                    sfx=["stamp@asterisk|55%"], norecut=True)
    T["s5.l18"] = S(R, [900, 560, 1.05], [920, 560, 1.1],
                    [win(barrier=0.0, sets=None), cat([560, 600], 0.36, look=[1, 0], mood="worry")],
                    mbx=M("present", (1180, 905), 640, look="win", gest=[["barriers|60%", "present", 1.5]]),
                    scene_p={"kind": "living", "nowin": True}, meter_at="help|80%", sfx=["click@barriers|65%"])
    T["s5.l18"]["actors"][0]["set"] = [st("barriers|60%", 0.5, barrier=1.0)]
    T["s5.l19"] = S(R, WIDE, [960, 570, 1.06],
                    [A("lily", "cl_lily", [330, 905], 0.6), A("bot", "cl_bottle", [1650, 905], 0.5),
                     A("str", "cl_string", [1350, 905], 0.9), cat([950, 905], 0.55, sit=0.5, mood="worry", look=[-1, 0], flip=True)],
                    scene_p={"kind": "living"}, meter_blink="five|5%",
                    chips8={"n0": 8.0, "filled0": 5.0, "y": 220, "sets": [st("five|5%", 0.3, pulse=1.0)]},
                    sfx=["tink@five|10%", "boing@winning|80%"])
    T["s5.l20"] = S(R, WIDE, [960, 560, 1.05],
                    [cat([640, 905], 0.55, mood="shock", look=[1, 0]),
                     A("shd", "cl_carrier", [2400, 935], 1.6, {"shadow": True, "a": 0.55}, moves=[mv(0.2, 2.2, (1350, 935))])],
                    scene_p={"kind": "living"}, sfx=["sting@intentions|60%"])
    # =========================================================================================== 6. the carrier
    T["s6.l0"] = S(R, [960, 640, 1.2], [960, 650, 1.28],
                   [A("car", "cl_carrier", [960, 905], 0.9, {"open": 0.0}, sets=[st("carrier|30%", 1.0, open=1.0)])],
                   scene_p={"kind": "hall"}, sfx=["scratch@carrier|35%"])
    T["s6.l1"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [A("cal", "cl_cal", [0, 230], 1.0, {"mode": "years", "boxes": 10, "two_from": 7, "stamps": 0.0},
                      sets=[st("examined|20%", 1.8, stamps=7.0), st("six|70%", 1.2, stamps=13.0)])],
                   card_at="year|35%", sfx=["stamp@examined|25%", "stamp@six|70%"], norecut=True)
    T["s6.l2"] = S(R, [960, 640, 1.15], [960, 650, 1.2],
                   [A("car", "cl_carrier", [1380, 905], 0.8, {"open": 1.0}),
                    cat([1060, 905], 0.55, mood="angry", ears_flat=True, look=[-1, 0], flip=True)],
                   mbx=M("present", (620, 905), 640, look="hero", gest=[["drive|45%", "nervous", 1.0], ["clinic|80%", "shock", 1.0]]),
                   scene_p={"kind": "hall"}, shake=["drive|45%"], sfx=["thud@drive|45%"])
    T["s6.l3"] = S(R, [900, 620, 1.1], [920, 620, 1.16],
                   [tint("dark", 0.55), A("car", "cl_carrier", [760, 905], 0.95, {"dungeon": 1.0, "open": 0.0}, front=True,
                                          moves=[mv("anyway|70%", 0.5, (1180, 760))])],
                   mbx=M("neutral", (1320, 905), 640, look="car", gest=[["Go|70%", "present", 1.5]]),
                   scene_p={"kind": "hall"}, sfx=["sting@dungeon|45%", "thud@Go|75%"])
    T["s6.l4"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [A("row", "cl_row", [0, 400], 1.5, {"n": 5, "w": 220, "fade": [3], "f": 0.0}, sets=[st("hadn't|45%", 0.8, f=1.0)])],
                   card_at="five|40%", meter_at="hadn't|50%", sfx=["whoosh@hadn't|45%"], norecut=True)
    T["s6.l5"] = S(R, [900, 560, 1.05], [920, 570, 1.1],
                   [A("door", "cl_clinicdoor", [700, 905], 1.0, {"cone": True})],
                   scene_p={"kind": "clinic"}, sfx=["tink@surgery|25%"])
    T["s6.l6"] = S(B, [0, 0, 1.0], [0, 20, 1.03],
                   [A("sc1", "cl_scale", [-500, 470], 0.9, {"v": 0.0}, sets=[st("thirty|40%", 1.0, v=0.85)]),
                    cat([-640, 418], 0.42, "c1", sit=0.5),
                    A("sc2", "cl_scale", [420, 470], 0.9, {"v": 0.0}, sets=[st("twelve|80%", 0.8, v=0.4)]),
                    cat([280, 418], 0.42, "c2", sit=0.5)],
                   card_at="intact|60%", sfx=["boing@thirty|40%", "tink@twelve|80%"], norecut=True)
    T["s6.l7"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [A("tl", "cl_timeline", [80, 200], 1.0, {"mode": "life", "g1": 0.0, "g2": 0.0},
                      sets=[st("British|20%", 0.8, g1=1.0), st("longer|60%", 1.0, g2=1.0)]),
                    cat([-720, 140], 0.25, "c1"), cat([-720, 360], 0.25, "c2")],
                   card_at="longer|60%", meter_at="longer|70%", sfx=["whoosh@longer|60%"], norecut=True)
    T["s6.l8"] = S(R, [960, 560, 0.95], [960, 600, 1.15],
                   [cat([900, 905], 0.6, cone=True, mood="sleepy", look=[1, -0.1], sit=0.5)],
                   scene_p={"kind": "living"}, sfx=["boing@trade|85%"])
    T["s6.l9"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [A("clip", "cl_clipper", [-150, 240], 2.0, moves=[mv("surgery|30%", 0.5, (-1300, 240))]),
                    A("tray", "cl_clipper", [1500, 300], 2.0, {"kind": "tray"}, moves=[mv("surgery|40%", 0.6, (0, 300))])],
                   sfx=["whoosh@surgery|35%"], norecut=True)
    T["s6.l10"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                    [A("tray", "cl_clipper", [0, 330], 2.0, {"kind": "tray"}),
                     A("x", "ds_cross", [0, 290], 1.0, {"on": 0.0, "r": 160}, sets=[st("banned|25%", 0.3, on=1.0)])],
                    card_at="banned|25%", sfx=["stamp@banned|30%"], norecut=True)
    T["s6.l11"] = S(B, [0, 40, 1.0], [0, 40, 1.03],
                    [A("bill", "cl_bill", [0, 90], 0.8, {"under": 0.0}, sets=[st("declawing|35%", 0.5, under=1.0),
                                                                           st("phalangectomy|55%", 0.5, under=2.0),
                                                                           st("tendonectomy|80%", 0.5, under=3.0)])],
                    sfx=["scratch@declawing|35%", "scratch@tendonectomy|80%"], norecut=True)
    T["s6.l12"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                    [A("p1", "cl_paper", [-330, 200], 0.9, {"verdict": "tick", "stamp": 0.0}, sets=[st("mixed|40%", 0.3, stamp=1.0)]),
                     A("p2", "cl_paper", [330, 200], 0.9, {"verdict": "cross", "stamp": 0.0}, sets=[st("pain|65%", 0.3, stamp=1.0)])],
                    meter_at="lasts|80%", sfx=["stamp@mixed|40%", "stamp@pain|65%"], norecut=True)
    T["s6.l13"] = S(R, [1000, 560, 1.05], [1020, 570, 1.1],
                    [cat([500, 905], 0.55, mood="worry", look=[1, -0.2])],
                    mbx=M("wave", (1300, 905), 660, look="viewer", gest=[["love|60%", "present", 2.0]]),
                    scene_p={"kind": "hall"}, sfx=["boing@love|65%"])
    # =========================================================================================== 7. your human
    T["s7.l0"] = S(R, [960, 420, 1.7], [960, 430, 1.85], [],
                   mbx=M("wave", (960, 905), 720, look="viewer", gest=[["means|60%", "laugh", 1.4]]),
                   scene_p={"kind": "living"}, sfx=["boing@well|80%"])
    T["s7.l1"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [A("map", "cl_petmap", [80, 460], 1.25, {"red": 0.0}, sets=[st("tail|55%", 0.6, red=1.0)])],
                   scene_p={"color": "#3a4660"}, card_at="tail|60%", sfx=["pop@tail|60%"], norecut=True)
    T["s7.l2"] = S(B, [0, 20, 1.04], [60, 0, 1.12],
                   [A("map", "cl_petmap", [80, 460], 1.25, {"red": 1.0, "green": 0.0}, sets=[st("between|45%", 0.6, green=1.0)])],
                   scene_p={"color": "#3a4660"}, sfx=["tink@between|50%"], norecut=True)
    T["s7.l3"] = S(R, [800, 620, 1.2], [820, 630, 1.26],
                   [cat([880, 905], 0.6, look=[1, 0], sets=[st("tail|40%", 0.2, ears_flat=True, mood="angry")])],
                   mbx=M("point", (420, 905), 640, look="hero", moves=[mv(0.05, 0.5, (470, 905), walk=True)],
                         gest=[["Every|70%", "deadpan", 1.4]]),
                   scene_p={"kind": "living"}, sfx=["scratch@tail|45%"])
    T["s7.l4"] = S(B, [0, 0, 1.0], [0, 15, 1.03],
                   [A("bars", "cl_bars", [0, 330], 0.65, {"g": 0.0}, sets=[st("negative|45%", 1.2, g=1.0)])],
                   card_at="rude|15%", card_px=92, meter_at="stranger|85%", sfx=["boing@stranger|85%"], norecut=True)
    T["s7.l5"] = S(R, [900, 560, 1.15], [920, 570, 1.2],
                   [cat([1500, 905], 0.5, moves=[mv(0.2, 2.0, (2100, 905), walk=True)])],
                   mbx=M("nervous", (800, 905), 640, look="viewer", gest=[["research|50%", "facepalm", 1.6]]),
                   scene_p={"kind": "living"}, sfx=["tink@research|60%"])
    T["s7.l6"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [A("bub", "cl_bubbles", [0, 140], 0.85, {"n": 0.0, "glow": 0.0},
                      sets=[st("calls|10%", 1.2, n=6.0), st("tell|55%", 0.4, glow=1.0)]),
                    cat([-90, 520], 0.4, sit=0.5, look=[0.4, -0.8])],
                   sfx=["pop@calls|15%", "tink@tell|55%"], norecut=True)
    hc7 = head([760, 900], 0.75)
    T["s7.l7"] = S(R, [hc7[0] + 60, hc7[1] - 20, 1.5], [hc7[0] + 60, hc7[1] - 10, 1.58],
                   [cat([760, 900], 0.75, look=[1, -0.2], radar=0.0, sets=[st("ears|25%", 0.4, radar=1.0)])],
                   scene_p={"kind": "living"}, card_at="meow|75%", sfx=["tink@ears|25%"])
    T["s7.l8"] = S(R, [hc7[0] + 40, hc7[1] - 40, 2.0], [hc7[0] + 40, hc7[1] - 30, 2.1],
                   [cat([760, 900], 0.75, mood="sleepy", look=[1, 0], sit=0.4)],
                   scene_p={"kind": "living"}, sfx=["tink@purr|70%"])
    T["s7.l9"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [A("wave", "cl_wave", [0, 180], 0.85, {"hi": 0.0}, sets=[st("cry|60%", 0.5, hi=1.0)])],
                   card_at="cry|60%", sfx=["tink@cry|60%"], norecut=True)
    lis = [A(f"l{i}", "cl_listener", [-560 + i * 560, 360], 1.0,
             {"col": ["#5d7fa8", "#c8574a", "#4f8f3a"][i], "skin": ["#f0c8a0", "#c08a60", "#e8b890"][i], "box": [2, 2, 1][i],
              "wince": 0.0, "mark": 0.0}, sets=[st("urgent|35%", 0.4, wince=1.0), st("pleasant|60%", 0.4, mark=1.0)])
           for i in range(3)]
    T["s7.l10"] = S(B, [0, 0, 1.0], [0, 20, 1.04], lis, scene_p={"color": "#3a4660"}, sfx=["tink@pleasant|60%"], norecut=True)
    lis2 = [A(f"l{i}", "cl_listener", [-560 + i * 560, 420], 0.7,
              {"col": ["#5d7fa8", "#c8574a", "#4f8f3a"][i], "skin": ["#f0c8a0", "#c08a60", "#e8b890"][i], "wince": 1.0, "mark": 0.0},
              sets=[st("dropped|60%", 0.4, wince=0.0)]) for i in range(3)]
    T["s7.l11"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                    [A("wave", "cl_wave", [0, -60], 0.6, {"hi": 1.0, "cry": 1.0, "erase": 0.0},
                       sets=[st("Take|5%", 1.0, erase=1.0), st("out|30%", 0.3, cry=0.0, hi=0.0)])] + lis2,
                    scene_p={"color": "#3a4660"}, sfx=["scratch@Take|10%", "tink@dropped|65%"], norecut=True)
    T["s7.l12"] = S(R, [960, 620, 1.15], [960, 620, 1.22],
                    [cat([820, 905], 0.65, sit=0.4, mood="happy"),
                     A("baby", "cl_baby", [1000, 700], 1.0, {"a": 0.0}, sets=[st("exploiting|40%", 1.0, a=0.55)], front=True)],
                    scene_p={"kind": "living"}, sfx=["whoosh@exploiting|40%"])
    T["s7.l13"] = S(R, [1000, 600, 1.1], [1010, 610, 1.16],
                    [A("clk", "cl_clock", [1150, 300], 0.42, {"mode": "wall", "hr": 5.0, "mn": 0.0}),
                     A("bowl", "cl_bowl", [1100, 905], 0.7, {"full": 0.0}, sets=[st("breakfast|35%", 0.8, full=1.0)]),
                     cat([1450, 905], 0.55, mood="happy", look=[-1, 0.4], flip=True)],
                    mbx=M("present", (800, 905), 640, look="bowl", gest=[["hacked|20%", "deadpan", 3.0]]),
                    scene_p={"kind": "kitchen", "time": "night"}, meter_at="Enjoy|60%", sfx=["tink@breakfast|40%"])
    # =========================================================================================== 8. your own body (senior from here)
    SEN = {"age": "senior"}
    T["s8.l0"] = S(R, WIDE, [980, 580, 1.08],
                   [cat([900, 905], 0.6, sit=0.5, **SEN)], scene_p={"kind": "living"}, sfx=["whoosh@body|60%"])
    T["s8.l1"] = S(R, WIDE, [960, 560, 1.04],
                   [cat([760, 905], 0.6, sit=0.6, look=[1, 0.2], **SEN)],
                   mbx=M("neutral", (1900, 905), 600, look="viewer", moves=[mv(0.3, 3.4, (-200, 905), walk=True)]),
                   scene_p={"kind": "living"}, card_at="subtle|75%", sfx=["step@guidelines|30%"],
                   pad=0.3)   # 0.3 s: moves the next lines off a voice + bed overlap the beep scan flagged at 6:14.6
    T["s8.l2"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [A("lb", "cl_lightbox", [0, 170], 0.7, {"n": 0.0}, sets=[st("Researchers|40%", 1.4, n=3.0)])],
                   card_at="100|60%", sfx=["whoosh@Researchers|45%"], norecut=True)
    T["s8.l3"] = S(B, [0, 20, 1.04], [0, 40, 1.1],
                   [A("lb", "cl_lightbox", [0, 170], 0.7, {"n": 3.0, "spots": 0.0}, sets=[st("92|30%", 0.5, spots=1.0)])],
                   card_at="92|30%", meter_at="joint|60%", sfx=["sting@92|30%"], norecut=True)
    T["s8.l4"] = S(B, [0, 40, 1.08], [40, 40, 1.12],
                   [A("lb", "cl_lightbox", [0, 170], 0.7, {"n": 3.0, "spots": 1.0, "q": 0.0}, sets=[st("hurting|60%", 0.4, q=1.0)])],
                   sfx=["pop@hurting|60%"], norecut=True)
    clips = lambda t1=None, t2=None, at2=None: [  # noqa: E731
        A("c1", "cl_clip", [-450, 220], 0.8, {"text": "11%", "on": 0.0 if t1 else 0.0}, sets=[st(t1, 0.4, on=1.0)] if t1 else None),
        A("c2", "cl_clip", [450, 220], 0.8, {"text": "77%", "sub": "EARLY STAGES COUNTED", "on": 0.0},
          sets=[st(at2, 0.4, on=1.0)] if at2 else None)]
    T["s8.l5"] = S(B, [0, 0, 1.0], [0, 20, 1.04], clips(), sfx=["pop@Kidneys|10%"], norecut=True)
    T["s8.l6"] = S(B, [0, 0, 1.0], [0, 20, 1.04], clips("11|10%", None, "77|55%"),
                   card_at="77|60%", sfx=["pop@11|12%", "pop@77|55%"], norecut=True)
    T["s8.l7"] = S(R, [960, 600, 1.1], [970, 610, 1.16],
                   [cat([700, 905], 0.6, sit=0.6, **SEN)],
                   mbx=M("laugh", (1200, 905), 640, look="viewer", gest=[["healthy|70%", "present", 1.5]]),
                   scene_p={"kind": "living"}, sfx=["boing@healthy|75%"])
    boxes = [A(f"b{i}", "cl_litter", [330 + i * 350, 905], 0.75, {"col": ["#6aa0c8", "#c8a06a", "#6ac88a", "#c86a8a"][i]}) for i in range(4)]
    T["s8.l8"] = S(R, WIDE, [980, 570, 1.05], boxes,
                   mbx=M("shrug", (1720, 905), 600, look="viewer", gest=[["three|30%", "shrug", 3.0]]),
                   scene_p={"kind": "living"}, card_at="four|35%", card_px=96, meter_at="peeing|80%", sfx=["tink@three|35%"])
    hs = head([700, 905], 0.8)
    T["s8.l9"] = S(R, [hs[0] + 60, hs[1] - 120, 1.8], [hs[0] + 60, hs[1] - 110, 1.88],
                   [cat([700, 905], 0.8, mood="sleepy", mouth="o", **SEN),
                    A("mir", "cl_mirror", [hs[0] + 230, hs[1] + 120], 0.6, at="dental|50%", moves=[mv("dental|50%", 0.4, (hs[0] + 160, hs[1] + 90))])],
                   scene_p={"kind": "living"}, card_at="129|35%", sfx=["tink@dental|50%"])
    T["s8.l10"] = S(R, [960, 760, 1.6], [970, 770, 1.66],
                    [cat([600, 905], 0.6, sit=0.5, look=[1, 0.6], **SEN), A("rug", "cl_rug", [1000, 925], 0.8),
                     A("hb", "cl_hairball", [1000, 500], 1.0, {"flag": 0.0}, moves=[mv("Hairballs|10%", 0.35, (1000, 925))],
                       sets=[st("honest|45%", 0.4, flag=1.0)])],
                    scene_p={"kind": "living"}, sfx=["thud@Hairballs|20%", "pop@honest|45%"])
    T["s8.l11"] = S(R, [960, 620, 1.1], [960, 630, 1.16],
                    [cat([760, 905], 0.6, sit=1.0, mood="sleepy", look=[1, 0.3], **SEN),
                     A("bowl", "cl_bowl", [1150, 905], 0.7, {"full": 1.0}),
                     A("shd", "cl_carrier", [2400, 935], 1.6, {"shadow": True, "a": 0.5}, moves=[mv("vet|60%", 1.4, (1500, 935))])],
                    scene_p={"kind": "living"}, card_at="vet|65%", card_px=96, meter_at="vet|70%", sfx=["sting@vet|65%"])
    # =========================================================================================== 9. the other deal
    T["s9.l0"] = S(R, WIDE, [960, 570, 1.06],
                   [cat([960, 905], 0.6, sit=0.6, mood="worry", **SEN)],
                   scene_p={"kind": "living", "time": "dusk"}, meter_blink="Eight|10%",
                   chips8={"n0": 8.0, "filled0": 5.0, "y": 220, "sets": [st("Eight|10%", 0.9, filled=8.0), st("Eight|20%", 0.3, pulse=1.0)]},
                   sfx=["tink@Eight|10%", "boing@Raw|75%"])
    T["s9.l1"] = S(R, [900, 560, 1.0], [1250, 560, 1.4],
                   [cat([560, 905], 0.6, look=[1, -0.1], **SEN)],
                   scene_p={"kind": "door", "door_open": 1.0}, sfx=["whoosh@door|70%"])
    T["s9.l2"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                   [A("row", "cl_row", [0, 380], 0.8, {"n": 15, "w": 118}, sets=None)],
                   card_at="2,400|25%", sfx=["pop@followed|20%"], norecut=True)
    T["s9.l3"] = S("cl_street", [960, 600, 1.0], [960, 610, 1.06], [], scene_p={"lights": 1.0},
                   card_at="165|40%", card_px=96, meter_at="half|80%", sfx=["whoosh@road|50%"])
    T["s9.l4"] = S("cl_street", [960, 640, 1.3], [970, 640, 1.36],
                   [cat([820, 792], 0.42, age="kitten", sit=0.5, look=[1, 0.3])], scene_p={"lights": 0.0},
                   card_at="41|20%", sfx=["tink@61|80%"])
    T["s9.l5"] = S("cl_lot", [960, 600, 1.0], [960, 620, 1.06],
                   [A("kits", "cl_kitout", [960, 880], 1.2, {"f": 0.0}, sets=[st("three|35%", 1.6, f=3.0)]),
                    A("fence", "cl_fence", [960, 905], 1.0, {"w": 2600, "h": 520}, front=True)],
                   card_at="colonies|20%", card_px=96, meter_at="odds|80%", sfx=["whoosh@vanished|55%"])
    T["s9.l6"] = S("cl_shelter", [960, 540, 1.0], [960, 520, 1.25], [], card_at="million|30%", sfx=["tink@euthanized|70%"])
    T["s9.l7"] = S(R, [1000, 600, 1.05], [1040, 610, 1.12],
                   [cat([780, 905], 0.6, look=[1, -0.1], **SEN)],
                   scene_p={"kind": "door", "door_open": 0.0, "screen": True}, meter_at="behavioural|70%", sfx=["thud@indoors|35%"])
    T["s9.l7"]["scene_p"]["door_open"] = 0.0
    # =========================================================================================== 10. the verdict
    led = lambda idn="led", **p: A(idn, "cl_parch", [0, 150], 0.62, dict({"mode": "ledger", "left": 0.0, "right": 0.0}, **p))  # noqa: E731
    T["s10.l0"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                    [led(unroll=0.0, sets=None)], sfx=["whoosh@ledger|30%"], norecut=True)
    T["s10.l0"]["actors"][0]["set"] = [st("ledger|20%", 0.9, unroll=1.0)]
    T["s10.l1"] = S(B, [0, 0, 1.0], [-40, 20, 1.05], [led(left=0.2)], card_at="eleven|45%", sfx=["tink@eleven|45%"], norecut=True)
    T["s10.l1"]["actors"][0]["set"] = [st("eleven|45%", 1.0, left=0.45)]
    T["s10.l2"] = S(B, [-40, 20, 1.05], [0, 20, 1.08], [led(left=0.45)], card_at="half|35%", meter_at="fourteen|75%",
                    sfx=["tink@fourteen|75%"], norecut=True)
    T["s10.l2"]["actors"][0]["set"] = [st("half|35%", 1.0, left=0.7)]
    T["s10.l3"] = S(B, [0, 120, 0.82], [0, 130, 0.86], [led(left=0.7, foot=0.0)], sfx=["whoosh@first|10%"], norecut=True)
    T["s10.l3"]["actors"][0]["set"] = [st("first|10%", 1.2, foot=1.0)]
    T["s10.l4"] = S(R, [960, 640, 1.25], [970, 650, 1.32],
                    [cat([860, 905], 0.65, sit=0.5, hat=True, mood="happy", **SEN)],
                    scene_p={"kind": "living"}, card_at="38|50%", sfx=["boing@38|50%"])
    T["s10.l5"] = S(R, [1000, 700, 1.4], [1010, 700, 1.46],
                    [cat([760, 905], 0.6, sit=0.5, hat=True, mood="happy", **SEN),
                     A("cake", "cl_cake", [1220, 905], 0.6, {"mode": "big", "out": 0.0}, sets=[st("old|30%", 0.8, out=1.0)])],
                    scene_p={"kind": "living"}, sfx=["whoosh@old|30%"])
    T["s10.l6"] = S(B, [0, 0, 1.0], [0, 20, 1.04],
                    [A("chart", "cl_paper", [0, 170], 0.75, {"kind": "under4"}), cat([-420, 430], 0.3, "c1", sit=0.4)],
                    card_at="chance|45%", card_px=96, meter_at="four|80%", sfx=["tink@four|80%"], norecut=True)
    T["s10.l7"] = S(B, [0, 0, 1.0], [80, 20, 1.12], [led(left=0.8)], sfx=["tink@owes|60%"], norecut=True)
    T["s10.l8"] = S(B, [80, 20, 1.08], [0, 20, 1.05], [led(left=0.8, right=0.0)], card_at="essential|55%",
                    sfx=["stamp@essential|55%"], norecut=True)
    T["s10.l8"]["actors"][0]["set"] = [st("essential|55%", 0.6, right=0.13)]
    T["s10.l9"] = S(R, [960, 380, 1.4], [960, 400, 1.48],
                    [cat([960, 300], 0.42, sit=1.0, mood="happy", look=[1, 0.3], **SEN), A("box", "cl_box", [960, 420], 0.8, front=True)],
                    scene_p={"kind": "living"}, sfx=["pop@safe|30%"])
    sta = [A("s1", "cl_station", [330, 905], 0.6, {"kind": "food"}), A("s2", "cl_station", [760, 905], 0.6, {"kind": "water"}),
           A("s3", "cl_station", [1200, 905], 0.7, {"kind": "litter"}), A("s4", "cl_station", [1640, 905], 0.7, {"kind": "scratch"})]
    T["s10.l10"] = S(R, WIDE, [980, 570, 1.05], sta + [cat([200, 905], 0.45, moves=[mv(0.1, 3.0, (1450, 905), walk=True)], **SEN)],
                     scene_p={"kind": "living"}, sfx=["pop@water|30%", "pop@scratching|65%"])
    T["s10.l11"] = S(R, [960, 620, 1.1], [960, 620, 1.16],
                     [cat([1400, 905], 0.55, flip=True, look=[1, 0.3], mood="happy",
                          moves=[mv("hunt|30%", 0.45, (830, 905), hop=140)], **SEN)],
                     mbx=M("present", (420, 905), 620, look="hero", prop="toymouse", moves=[mv(0.05, 1.0, (330, 905), walk=True)]),
                     scene_p={"kind": "living"}, sfx=["boing@hunt|35%"])
    T["s10.l12"] = S(R, [1000, 620, 1.2], [1010, 630, 1.26],
                     [A("hero", "cl_petmap", [800, 905], 0.6, {"green": 0.0, "mood": "happy"}, sets=[st("friendly|40%", 0.6, green=1.0)])],
                     mbx=M("point", (1300, 905), 640, look="hero", gest=[["predictable|60%", "laugh", 1.4]]),
                     scene_p={"kind": "living"}, sfx=["tink@friendly|45%"])
    T["s10.l13"] = S(R, [1150, 700, 1.4], [1160, 700, 1.46],
                     [cat([930, 905], 0.55, mood="happy", look=[1, 0], **SEN,
                          moves=[mv("home|25%", 0.5, (960, 905)), mv("respects|50%", 0.5, (930, 905)), mv("nose|80%", 0.4, (960, 905))])],
                     scene_p={"kind": "living"}, card_at="nose|60%", meter_at="nose|70%", sfx=["tink@nose|70%"])
    T["s10.l14"] = S(R, WIDE, [960, 560, 1.06],
                     sta[:2] + [A("box", "cl_box", [1150, 420], 0.6, front=True), cat([1150, 330], 0.32, "c2", sit=1.0, mood="happy", **SEN),
                                A("win", "cl_window", [500, 600], 1.0, {"open": 1.0, "barrier": 1.0})],
                     mbx=M("present", (1600, 905), 600, look="viewer", gest=[["sweet|80%", "laugh", 1.4]]),
                     scene_p={"kind": "living", "nowin": True}, meter_climb=[82, "plus|30%", "damn|85%"], sfx=["tink@sweet|85%"])
    T["s10.l15"] = S(R, WIDE, [960, 560, 1.05],
                     [cat([960, 905], 0.55, sit=0.6, mood="worry", **SEN)],
                     scene_p={"kind": "living"}, meter_swing=[44, "rawer|25%", "rent|70%"], sfx=["boing@rent|75%"])
    T["s10.l16"] = S("cl_village", [990, 720, 1.6], [990, 730, 1.68],
                     jars + [cat([930, 905], 0.55, age="wild", sit=0.75, mood="smug")], sfx=["whoosh@0.05"])
    T["s10.l17"] = S("tc_combo", [990, 730, 1.6], None,
                     jars + [cat([930, 905], 0.55, "wild", age="wild", sit=0.75, mood="smug", sets=[st("never|20%", 0.8, sit=0.97, mood="sleepy")]),
                             cat([3000 + 1330, 740], 0.55, "hero", sit=0.97, mood="sleepy", **SEN)],
                     scene_p={"a": "cl_village", "pa": {}, "b": "cl_room", "pb": {"kind": "living"}, "bx": 2400, "dx": 3000},
                     shots=[cam([990, 730, 1.6], [990, 735, 1.66]), cam([3000 + 1390, 600, 1.5], [3000 + 1390, 610, 1.56], at="Lucky|50%", dur=0.05)],
                     sfx=["whoosh@Lucky|50%"], norecut=True)
    T["s10.l18"] = S(R, [1000, 580, 1.05], [1020, 590, 1.1],
                     [cat([620, 905], 0.55, sit=0.5, mood="happy", **SEN)],
                     mbx=M("present", (1330, 905), 640, look="viewer", prop="book", gest=[["manual|85%", "shrug", 1.4]]),
                     scene_p={"kind": "living"}, no_card=True,
                     stamps=[{"text": "SWEET DEAL (IF...)", "at": "sweet|20%", "x": 640, "y": 300, "color": GREEN, "px": 104, "rot": -7}],
                     meter_at="sweet|30%")
    T["s10.l19"] = S(R, [960, 560, 1.0], [980, 570, 1.04],
                     [cat([620, 905], 0.55, sit=0.5, mood="happy", **SEN)],
                     top_actors=[cat([1250, 1130], 0.62, "endcat", sit=0.4, mood="happy", front=True, **SEN)],
                     scene_p={"kind": "living"}, sfx=["whoosh@bigger|40%"])
    return T
