// Episode: window jumping spider (YouTube Short, 9 lines, ~19 s, loops). Sunny living-room window by day (UC IPM: day-active
// hunters); real-size spider (~1.2 cm). Beats: 8 eyes staring into the camera (hook) -> it hops closer, the person backs off ->
// eye chart -> no web: stalks + pounces on a fly -> leaps a 40-body-length ruler at the camera -> the person, winded ->
// hides behind the armchair -> Meatball's sip -> "It's still watching." pulls back from the stare to the opening framing.
import * as THREE from 'three';
import { mat, mesh, box, texMat, canvasTex, wallPlane, shade } from './lib.js';
import * as P from './props.js';
import * as Q from './props2.js';
import * as R from './props3.js';

export const SHIRT = 0xd9822b;
export const LIGHT = { bg: 0x9fd4f2, hemi: [0xeaf4ff, 0x8a7458, 1.2], sun: [0xfff1d6, 1.7], sunPos: [-1.0, 3.2, 2.2], sunTgt: [0, 0.9, -0.4],
  lamps: [[0xfff0d0, 1.4, [0.0, 1.5, -0.2]], [0xffe6c4, 0.8, [0.6, 2.3, 1.0]]] };

const SILL = 1.0;           // window-sill top
const SS = 0.012;           // jumping spider ~1.2 cm
const HOME = [0.0, -0.49, -Math.PI / 2];   // facing the room (+z): opening + loop frame
const HOP = [0.0, -0.462, -Math.PI / 2];
const CHART = [-0.165, -0.5], SEE = [-0.2, -0.5, 0];
const FLY = [0.125, -0.5], CREEP0 = [0.035, -0.5, 0], CREEP1 = [0.088, -0.5, 0];
const RUL0 = -0.3, RULZ = -0.49, RN = 40;  // ruler: 40 body lengths along +x from x = RUL0

function makeLivingRoom() {
  const g = new THREE.Group();
  const wood = texMat(canvasTex(256, 256, (c, w) => { for (let i = 0; i < 8; i++) { c.fillStyle = shade('#b07a4a', ((i * 37) % 9) - 4); c.fillRect(0, i * 32, w, 31); c.fillStyle = '#7a5030'; c.fillRect(0, i * 32 + 31, w, 1); } }, [5, 5]));
  const fl = new THREE.Mesh(new THREE.PlaneGeometry(4.4, 3.6), wood); fl.rotation.x = -Math.PI / 2; fl.position.set(0.1, 0, 1.1); fl.receiveShadow = true; g.add(fl);
  const paint = mat(0xefe2c4, { flatShading: false });
  // back wall with the window hole (x -0.5..0.5, y SILL..1.95)
  g.add(wallPlane(1.7, 2.5, paint, -1.35, -0.6, 0), wallPlane(1.7, 2.5, paint, 1.35, -0.6, 0), wallPlane(1.0, SILL, paint, 0, -0.6, 0), wallPlane(1.0, 0.55, paint, 0, -0.6, 0, 1.95));
  g.add(wallPlane(3.6, 2.5, paint, -2.1, 1.2, Math.PI / 2), wallPlane(3.6, 2.5, paint, 2.3, 1.2, -Math.PI / 2), wallPlane(4.4, 2.5, paint, 0.1, 2.9, Math.PI));
  const ceil = new THREE.Mesh(new THREE.PlaneGeometry(4.4, 3.6), paint); ceil.rotation.x = Math.PI / 2; ceil.position.set(0.1, 2.5, 1.1); g.add(ceil);
  const out = R.makeOutside(1.6, 1.4); out.position.set(0, SILL + 0.45, -0.75); g.add(out);
  // window frame + panes, sill (deep, painted wood) + apron
  const fr = mat(0xffffff);
  g.add(box(1.08, 0.05, 0.08, fr, 0, 1.95, -0.6), box(0.05, 0.98, 0.08, fr, -0.52, SILL - 0.01, -0.6), box(0.05, 0.98, 0.08, fr, 0.52, SILL - 0.01, -0.6), box(0.03, 0.95, 0.03, fr, 0, SILL, -0.62, false), box(1.0, 0.03, 0.03, fr, 0, 1.47, -0.62, false));
  const glass = new THREE.Mesh(new THREE.PlaneGeometry(1.0, 0.95), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.12 })); glass.position.set(0, SILL + 0.475, -0.625); g.add(glass);
  g.add(box(1.16, 0.04, 0.22, mat(0xf4efe4), 0, SILL - 0.04, -0.51), box(1.0, 0.07, 0.03, mat(0xe8e2d4), 0, SILL - 0.12, -0.585, false));
  const curL = R.makeCurtain(0.42, 1.25), curR = R.makeCurtain(0.42, 1.25); curL.position.set(-0.78, 2.12, -0.5); curR.position.set(0.78, 2.12, -0.5); g.add(curL, curR);
  // a plant + a picture frame for scale and colour
  const pot = box(0.22, 0.24, 0.22, 0xc0643a, -1.2, 0, -0.3); g.add(pot);
  for (let k = 0; k < 6; k++) { const l = mesh(new THREE.ConeGeometry(0.05, 0.45, 5), mat(0x4e9a46)); l.position.set(-1.2 + 0.06 * Math.cos(k), 0.45, -0.3 + 0.06 * Math.sin(k)); l.rotation.set(0.3 * Math.sin(k * 2), 0, 0.3 * Math.cos(k * 2)); g.add(l); }
  const pic = box(0.5, 0.36, 0.03, 0x3a2a1c, 1.25, 1.35, -0.585, false); g.add(pic);
  g.add(box(0.44, 0.3, 0.01, 0x8fbfd8, 1.25, 1.38, -0.567, false));
  return g;
}

const arc = (a, b, u, hgt) => [a[0] + (b[0] - a[0]) * u, hgt * Math.sin(Math.PI * u), a[1] + (b[1] - a[1]) * u];

export function build(scene, S, K) {
  const { L, T_END, start, end, W, cut, popS, vis, place, ease, clamp01 } = K;
  scene.add(makeLivingRoom());
  S.sp = R.makeJumpSpider(); S.sp.scale.setScalar(SS); scene.add(S.sp);
  S.fly = R.makeFly(); S.fly.scale.setScalar(0.008); scene.add(S.fly);
  S.chart = R.makeEyeChart(); scene.add(S.chart);
  S.ruler = R.makeRuler(RN, SS); scene.add(S.ruler);
  S.chair = R.makeArmchair(); S.chair.position.set(0.78, 0, 0.62); scene.add(S.chair);
  S.mug = Q.makeMug(); S.mb.userData.arms[1].el.add(S.mug);

  const POSES = { ...P.PERSON_POSES,
    winded: { py: 0.84, lean: -0.5, hip: [0.35, 0.35], knee: [-0.45, -0.45], shz: [0.75, 0.75], elz: [0.15, 0.15], shx: [0, 0], elx: [0, 0] },
    hide: { py: 0.38, lean: -0.1, hip: [1.75, 1.7], knee: [-2.3, -2.25], shz: [1.15, 1.1], elz: [0.9, 0.9], shx: [0, 0], elx: [0, 0] },
    ask: { py: 0.92, lean: 0.12, hip: [0, 0], knee: [0, 0], shz: [0.5, 0.5], elz: [1.2, 1.2], shx: [0.4, 0.4], elx: [0, 0] },
  };
  const MBPOS = [0.36, -0.52, -Math.PI / 2 + 0.45], PPOS = [0.08, 1.15, Math.PI / 2];
  const P3 = (p, y = SILL) => [p[0], y, p[1]];
  const mbAt = (S) => [S.mb.position.x, S.mb.position.y, S.mb.position.z];
  const pHead = (S) => S.person.userData.head.getWorldPosition(new THREE.Vector3()).toArray();
  const H3 = P3(HOME, SILL + 0.004);
  const OPEN = { c0: [H3[0] + 0.015, H3[1] + 0.017, H3[2] + 0.068], l0: [H3[0], H3[1] + 0.004, H3[2]],
    c1: [H3[0] + 0.008, H3[1] + 0.01, H3[2] + 0.045], l1: [H3[0], H3[1] + 0.003, H3[2]], mv: 1.0 };
  const cfg = L.map(() => ({ shots: [{}] }));
  const set = (i, o) => Object.assign(cfg[i], o);
  const tHop = W(1, 0) + 0.05, tPounce = W(4, 5) - 0.05, tLeap = W(6, 1) - 0.02, tLand = W(6, 4) + 0.15;
  const tSip = start(8), tDead = W(8, 4) - 0.1;

  set(0, { cardWord: 5, shots: [{ ...OPEN }, { at: cut(0, 6), tgt: [H3[0], H3[1], H3[2] + 0.004], yaw: 84, dist: 0.03, h: 0.004, dyaw: 8, push: 0.85 }] });
  set(1, { person: { pose: 'back', from: 'stand' }, shots: [{ c0: [-0.006, SILL + 0.009, -0.545], l0: [0.05, 1.45, 1.15], c1: [-0.006, SILL + 0.009, -0.545], l1: [0.05, 1.45, 1.15] }] });
  set(2, { cardWord: 0, mood: 'smug', mbPose: 'hips', shots: [{ tgt: mbAt, yaw: 76, dist: 0.42, h: 0.05, dyaw: -6, push: 0.9 },
    { at: cut(2, 1), tgt: [SEE[0] + 0.012, SILL + 0.008, -0.5], yaw: 118, dist: 0.13, h: 0.022, dyaw: -8, push: 0.85 }] });
  set(3, { person: { look: (t) => 0.5 * Math.sin((t - start(3)) * 6) }, shots: [{ c0: [-0.05, 1.42, -0.3], l0: [0.08, 1.62, 1.15], c1: [-0.04, 1.43, -0.12], l1: [0.08, 1.64, 1.15] }] });
  set(4, { cardWord: 0, shots: [{ tgt: [0.1, SILL + 0.004, -0.5], yaw: 158, dist: 0.08, h: 0.018, dyaw: 8, push: 0.8 }] });
  set(5, { person: { pose: 'ask', from: 'stand' }, shots: [{ c0: [0.2, 1.4, -0.3], l0: [0.08, 1.6, 1.15], c1: [0.18, 1.42, -0.1], l1: [0.08, 1.62, 1.15] }] });
  set(6, { cardWord: 2, shots: [{ tgt: (S) => [S.sp.position.x, SILL + 0.004 + 0.5 * (S.sp.position.y - SILL), RULZ], yaw: 18, dist: 0.13, h: 0.035, dyaw: 0, push: 1 },
    { at: cut(6, 5), c0: [2.2, 1.3, 1.5], l0: [0.08, 1.12, 1.15], c1: [2.1, 1.3, 1.48], l1: [0.08, 1.1, 1.15] }], person: { p0: [0.08, 1.15, 0.25], pose: 'winded', from: 'stand' } });
  set(7, { person: { p0: [0.74, 1.12, Math.PI / 2 + 0.25], pose: 'hide', from: 'stand', look: (t) => 0.4 * Math.sin((t - start(7)) * 8) }, shots: [{ c0: [0.5, 0.98, -0.45], l0: [0.76, 0.95, 1.0], c1: [0.52, 0.97, -0.3], l1: [0.76, 0.95, 1.0] }] });
  const home = T_END - 0.08, out = cut(8, 4);   // "It's still watching." pulls back from the stare to the opening framing
  set(8, { cardWord: 0, mbPose: 'hips', moodAt: (t) => (t < tDead ? 'sip' : 'deadpan'), shots: [{ tgt: mbAt, yaw: 80, dist: 0.36, h: 0.02, dyaw: 4, push: 0.9 },
    { at: out, c0: OPEN.c1, l0: OPEN.l1, c1: OPEN.c0, l1: OPEN.l0, mv: home - out }] });
  for (const i of [0, 1, 4]) cfg[i].hideMb = 1;

  function props(t, i) {
    const sp = S.sp, u = sp.userData;
    let p = HOME, y = SILL, pitch = 0, walk = 0, amp = 0;
    if (i === 1) { const k = clamp01((t - tHop) / 0.28); p = [HOME[0], HOME[1] + (HOP[1] - HOME[1]) * ease(k), HOME[2]]; y = SILL + 0.008 * Math.sin(Math.PI * k); }
    else if (i === 2) p = SEE;
    else if (i === 4) {   // creep low and slow, then pounce onto the fly
      if (t < tPounce) { const k = clamp01((t - start(4)) / (tPounce - start(4))); p = [CREEP0[0] + (CREEP1[0] - CREEP0[0]) * k, CREEP0[1], 0]; walk = t * 1.6; amp = 0.5; y = SILL - 0.001; }
      else { const k = clamp01((t - tPounce) / 0.22), q = arc(CREEP1, FLY, k, 0.012); p = [q[0] - 0.006 * k, q[2], 0]; y = SILL + q[1]; pitch = -0.4 * Math.sin(Math.PI * k); }
    } else if (i === 6) {   // leap the ruler, toward the camera
      const a = [RUL0, RULZ], b = [RUL0 + RN * SS, RULZ], k = clamp01((t - tLeap) / (tLand - tLeap)), q = arc(a, b, ease(k), 0.035);
      p = [q[0], q[2], 0]; y = SILL + 0.0021 + q[1]; pitch = k > 0 && k < 1 ? 0.35 * Math.cos(Math.PI * k) : 0;
    }
    place(sp, p, y); sp.rotation.z = pitch;
    sp.visible = i !== 3 && i !== 5 && !(i === 6 && t > cut(6, 5)) && i !== 7;
    Q.animateLegs(sp, walk, amp);
    u.body.position.y = 0.02 * Math.sin(t * 2.3);
    // the eyes track the camera-side: a slight body sway while staring
    if (i === 0 || i === 8) sp.rotation.y = HOME[2] + 0.06 * Math.sin(t * 1.4) * (i === 0 ? clamp01((cut(0, 6) - t) / 0.3) : 0);
    u.palps.forEach((q, k) => { q.rotation.x = 0.6 + 0.25 * Math.sin(t * 9 + k * 2); });
    // eye chart pops on "eyes"; the spider leans in to read it
    if (vis(S.chart, cut(2, 1), end(2), t)) { place(S.chart, [...CHART, -Math.PI / 2 + 0.65], SILL); S.chart.scale.setScalar(popS(t, cut(2, 1), 1)); u.body.rotation.z = 0.12 * Math.sin((t - cut(2, 1)) * 3); }
    else u.body.rotation.z = 0;
    // the fly lands, rubs its hands, then gets pounced (carried under the spider's fangs)
    if (vis(S.fly, start(4), end(4), t)) {
      const land = clamp01((t - start(4)) / 0.4);
      if (t < tPounce + 0.18) { place(S.fly, [FLY[0] + 0.04 * (1 - land), FLY[1] - 0.02 * (1 - land), Math.PI], SILL + 0.05 * (1 - land) * (1 - land)); Q.animateLegs(S.fly, t * 2, 0.3); S.fly.userData.wings.forEach((w, k) => (w.rotation.x = land < 1 ? 0.6 * Math.sin(t * 90 + k) : 0)); }
      else { const f = new THREE.Vector3(0.5 * SS, 0, 0).applyAxisAngle(new THREE.Vector3(0, 1, 0), sp.rotation.y); S.fly.position.set(sp.position.x + f.x, SILL + 0.003, sp.position.z + f.z); S.fly.rotation.set(0.6, 0.4, 1.2); }
    }
    if (vis(S.ruler, start(6) - 0.05, cut(6, 5), t)) { S.ruler.position.set(RUL0, SILL, RULZ); S.ruler.scale.set(1, 1, popS(t, start(6) - 0.05, 1) || 0.001); }
    S.mug.visible = i === 8 && t < tDead + 0.2;
  }
  return { cfg, props, POSES, pose0: 'stand', MB: 0.055, MBPOS, mbY: SILL, PPOS, mbIn: start(2), mbOut: home - 0.5 };
}
