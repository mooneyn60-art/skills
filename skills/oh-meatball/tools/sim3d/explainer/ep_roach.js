// Episode: German cockroach (YouTube Short, 8 lines, ~18 s, loops). Low-poly night kitchen, real-size roach (~1.4 cm).
// Beats: egg case + 40 babies (hook) -> newspaper slam, roach darts into a 1/16-inch crack -> soap / glue / hair ->
// head pops off, the body keeps walking ("WEEKS") -> "Don't look behind you." cranes back to the opening framing.
import * as THREE from 'three';
import { mat, mesh, box, cyl, texMat, tileTex, canvasTex, wallPlane, shade } from './lib.js';
import * as P from './props.js';
import * as Q from './props2.js';

export const SHIRT = 0x7a4f8f;
export const LIGHT = { bg: 0x0e1426, hemi: [0xc9d6ff, 0x6a5a48, 1.05], sun: [0xd2ddff, 1.5], sunPos: [-0.8, 3.2, 2.4], sunTgt: [0, 0.9, -0.3],
  lamps: [[0xffd59a, 1.7, [0.0, 1.38, -0.42]], [0xffe6c4, 0.9, [0.3, 2.3, 0.7]]] };

const TOP = 0.9;            // countertop height
const RS = 0.014;           // German cockroach ~1.3-1.4 cm
const HOME = [0.08, -0.28, 0];             // the roach with its egg case (opening + loop frame)
const CRX = -0.2, CRACK = [CRX, -0.555, Math.PI / 2];   // in front of the gap under the backsplash (wall z = -0.6)
const SPREAD = [-0.32, -0.32];
const HEADLESS = [-0.05, -0.22];

function makeKitchen() {
  const g = new THREE.Group();
  const wood = texMat(canvasTex(256, 256, (c, w) => { for (let i = 0; i < 8; i++) { c.fillStyle = shade('#9c6b42', ((i * 37) % 9) - 4); c.fillRect(0, i * 32, w, 31); c.fillStyle = '#6a4528'; c.fillRect(0, i * 32 + 31, w, 1); } }, [5, 5]));
  const fl = new THREE.Mesh(new THREE.PlaneGeometry(4.4, 3.4), wood); fl.rotation.x = -Math.PI / 2; fl.position.set(0.1, 0, 1.0); fl.receiveShadow = true; g.add(fl);
  const paint = mat(0xd9cdb6, { flatShading: false });
  g.add(wallPlane(4.4, 2.5, paint, 0.1, -0.6, 0));
  g.add(wallPlane(3.4, 2.5, paint, -2.1, 1.0, Math.PI / 2), wallPlane(3.4, 2.5, paint, 2.3, 1.0, -Math.PI / 2), wallPlane(4.4, 2.5, paint, 0.1, 2.7, Math.PI));
  const ceil = new THREE.Mesh(new THREE.PlaneGeometry(4.4, 3.4), paint); ceil.rotation.x = Math.PI / 2; ceil.position.set(0.1, 2.5, 1.0); g.add(ceil);
  const splash = wallPlane(2.5, 0.55, texMat(tileTex('#e8eef0', '#aab7bc', 4, [10, 2.2])), 0, -0.598, 0, TOP); g.add(splash);
  // lower cabinets + countertop
  const cab = 0x5f8a78, cabD = shade('#5f8a78', -18);
  g.add(box(2.5, 0.86, 0.56, cab, 0, 0, -0.32));
  for (let k = 0; k < 5; k++) { g.add(box(0.47, 0.7, 0.01, cabD, -1.0 + k * 0.5, 0.08, -0.035, false)); g.add(box(0.1, 0.018, 0.02, 0xd0d0d0, -1.0 + k * 0.5, 0.68, -0.025, false)); }
  g.add(box(2.56, 0.04, 0.62, mat(0xe2dccf), 0, TOP - 0.04, -0.29));
  g.add(box(0.13, 0.0035, 0.004, mat(0x050403), CRX, TOP, -0.598, false));   // the gap the roach squeezes into
  // sink + faucet
  g.add(box(0.46, 0.004, 0.36, 0x9ea4aa, 0.62, TOP, -0.3, false), box(0.4, 0.005, 0.3, 0x50565c, 0.62, TOP, -0.3, false));
  const fa = cyl(0.012, 0.012, 0.25, 0xc8ccd0, 8); fa.position.set(0.62, TOP + 0.125, -0.52); g.add(fa);
  const sp = cyl(0.01, 0.01, 0.14, 0xc8ccd0, 8); sp.rotation.x = Math.PI / 2; sp.position.set(0.62, TOP + 0.245, -0.46); g.add(sp);
  // stove
  for (const [x, z] of [[-0.88, -0.2], [-0.62, -0.2], [-0.88, -0.42], [-0.62, -0.42]]) { const b = mesh(new THREE.TorusGeometry(0.06, 0.01, 4, 14), mat(0x1a1a1a)); b.rotation.x = Math.PI / 2; b.position.set(x, TOP + 0.006, z); g.add(b); }
  g.add(box(0.55, 0.003, 0.5, 0x2a2a2e, -0.75, TOP, -0.31, false));
  // upper cabinets (under-cabinet light strip) + fridge + table
  g.add(box(2.5, 0.62, 0.33, cab, 0, 1.48, -0.435));
  for (let k = 0; k < 5; k++) g.add(box(0.47, 0.56, 0.01, cabD, -1.0 + k * 0.5, 1.51, -0.268, false));
  g.add(box(2.3, 0.012, 0.03, new THREE.MeshBasicMaterial({ color: 0xffe2b0 }), 0, 1.465, -0.3, false));
  g.add(box(0.74, 1.85, 0.68, 0xeceae4, 1.66, 0, -0.26), box(0.02, 0.5, 0.03, 0xb8b8b8, 1.33, 1.2, 0.09, false), box(0.02, 0.3, 0.03, 0xb8b8b8, 1.33, 0.55, 0.09, false));
  const tbl = new THREE.Group(); tbl.add(box(0.9, 0.04, 0.7, 0x8a5a36, 0, 0.72, 0)); for (const [x, z] of [[-0.4, -0.3], [0.4, -0.3], [-0.4, 0.3], [0.4, 0.3]]) tbl.add(box(0.05, 0.72, 0.05, 0x6e4528, x, 0, z));
  tbl.position.set(-1.1, 0, 1.6); g.add(tbl);
  const win = P.makeWindow(); win.position.set(0.6, 1.0, 2.68); win.rotation.y = Math.PI; g.add(win);
  win.userData.glassM.color.setHex(0x14234a); win.userData.moon.visible = true;
  return g;
}

// piecewise path: keys [[t, x, z, h], ...] -> [x, z, h, moving]
function path(t, keys) {
  if (t <= keys[0][0]) return [...keys[0].slice(1), 0];
  for (let k = 0; k + 1 < keys.length; k++) {
    const [a, b] = [keys[k], keys[k + 1]];
    if (t < b[0]) { const u = (t - a[0]) / (b[0] - a[0]); return [a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u, a[3] + (b[3] - a[3]) * u, 1]; }
  }
  return [...keys[keys.length - 1].slice(1), 0];
}

export function build(scene, S, K) {
  const { L, T_END, start, end, W, cut, popS, vis, place, fwd, ease, clamp01 } = K;
  scene.add(makeKitchen());
  S.roach = Q.makeGermanRoach(true); S.roach.scale.setScalar(RS); scene.add(S.roach);
  S.nymphs = []; for (let k = 0; k < 40; k++) { const n = Q.makeNymph(); scene.add(n); S.nymphs.push(n); }
  S.paper = Q.makeNewspaper(); scene.add(S.paper);
  S.soap = Q.makeSoap(); S.glue = Q.makeGlue(); S.hair = Q.makeHair(); S.crumbs = Q.makeCrumbs();
  S.cal = Q.makeCal('ALIVE FOR', 'WEEKS'); scene.add(S.soap, S.glue, S.hair, S.crumbs, S.cal);
  S.slipper = P.makeSlipper(); S.slipper.position.set(0, -0.06, 0); S.slipper.rotation.z = Math.PI / 2; S.person.userData.hands[1].add(S.slipper);
  const head = S.roach.userData.head, head0 = head.position.clone();

  const MBPOS = [0.42, -0.17, -Math.PI / 2 + 0.35], PPOS = [0.36, 1.45, Math.PI / 2];
  const P3 = (p, y = TOP) => [p[0], y, p[1]];
  const roachAt = (S) => [S.roach.position.x, TOP + 0.004, S.roach.position.z];
  const mbAt = (S) => [S.mb.position.x, S.mb.position.y, S.mb.position.z];
  const pHead = (S) => S.person.userData.head.getWorldPosition(new THREE.Vector3()).toArray();
  const H3 = P3(HOME, TOP + 0.004);
  const OPEN = { c0: [H3[0] + 0.12, H3[1] + 0.075, H3[2] + 0.2], l0: [H3[0] - 0.02, H3[1], H3[2] - 0.02],
    c1: [H3[0] + 0.03, H3[1] + 0.022, H3[2] + 0.05], l1: [H3[0] - 0.004, H3[1] + 0.001, H3[2]], mv: 1.0 };
  const EGG = [H3[0] - 0.6 * RS, H3[1], H3[2]];
  const cfg = L.map(() => ({ shots: [{}] }));
  const set = (i, o) => Object.assign(cfg[i], o);
  const tSlam = W(1, 0) + 0.22;

  set(0, { cardWord: 7, shots: [{ ...OPEN }, { at: cut(0, 8), tgt: [EGG[0] - 0.012, EGG[1], EGG[2]], yaw: 125, dist: 0.075, h: 0.035, dyaw: 12, push: 0.85 }] });
  set(1, { shots: [{ tgt: [H3[0] - 0.1, H3[1], H3[2] - 0.12], yaw: 70, dist: 0.62, h: 0.34, dyaw: 6, push: 0.95, shake: { t: tSlam, a: 0.012 } }] });
  set(2, { cardWord: 2, mood: 'smug', shots: [{ tgt: mbAt, yaw: 70, dist: 0.46, h: 0.05, dyaw: -6, push: 0.9 },
    { at: cut(2, 2), tgt: [CRX + 0.004, TOP + 0.004, -0.585], yaw: 72, dist: 0.075, h: 0.016, dyaw: 10, push: 0.85 }] });
  set(3, { person: { look: (t) => 0.25 * Math.sin((t - start(3)) * 4) }, shots: [{ c0: [0.2, 1.36, -0.48], l0: [0.36, 1.38, 1.45], c1: [0.22, 1.37, -0.3], l1: [0.36, 1.4, 1.45] }] });
  set(4, { cardWord: 1, shots: [{ tgt: [SPREAD[0] - 0.02, TOP + 0.01, SPREAD[1] - 0.02], yaw: 78, dist: 0.4, h: 0.16, dyaw: -8, push: 0.85 }] });
  set(5, { person: { pose: 'slipper', from: 'stand' }, shots: [{ c0: [0.08, 1.3, -0.52], l0: [0.36, 1.72, 1.45], c1: [0.11, 1.32, -0.42], l1: [0.36, 1.74, 1.45] }] });
  set(6, { cardWord: 4, shots: [{ tgt: roachAt, yaw: 68, dist: 0.1, h: 0.035, dyaw: 10, push: 0.92 },
    { at: cut(6, 4), tgt: [HEADLESS[0] - 0.01, TOP + 0.012, HEADLESS[1] - 0.01], yaw: 72, dist: 0.2, h: 0.045, dyaw: 6, push: 0.92 }] });
  const home = T_END - 0.08, out = W(7, 2) + 0.05;
  const l7a = { tgt: mbAt, yaw: 78, dist: 0.36, h: 0.015, dyaw: 4, push: 0.9 };
  set(7, { mood: 'deadpan', mbPose: 'hips', shots: [l7a, { at: out, c0: [MBPOS[0] + 0.05, TOP + 0.12, MBPOS[1] + 0.24], l0: [MBPOS[0], TOP + 0.11, MBPOS[1]], c1: OPEN.c0, l1: OPEN.l0, mv: home - out }] });
  for (const i of [0, 1]) cfg[i].hideMb = 1;

  // roach paths
  const dart0 = W(1, 0) + 0.05;
  const keys = [[0, ...HOME], [dart0, ...HOME], [dart0 + 0.25, HOME[0] - 0.12, HOME[1] - 0.06, 0.9], [dart0 + 0.6, CRACK[0], CRACK[1], Math.PI / 2],
    [W(2, 4), CRACK[0], CRACK[1], Math.PI / 2], [W(2, 7) + 0.25, CRACK[0], -0.62, Math.PI / 2]];
  const sp = (dx, dz) => [SPREAD[0] + dx, SPREAD[1] + dz];
  const SOAP = sp(-0.07, 0.0), GLUE = sp(0.03, -0.07), HAIR = sp(0.07, 0.03), TOAST = sp(-0.01, 0.06);
  const k4 = [[start(4), SOAP[0] + 0.05, SOAP[1] + 0.03, 2.6], [W(4, 1), SOAP[0] + 0.035, SOAP[1] + 0.012, 2.8], [W(4, 2) - 0.1, SOAP[0] + 0.035, SOAP[1] + 0.012, 2.8],
    [W(4, 2) + 0.3, GLUE[0] + 0.02, GLUE[1] + 0.03, 1.8], [W(4, 3) - 0.05, GLUE[0] + 0.02, GLUE[1] + 0.03, 1.2], [W(4, 3) + 0.35, HAIR[0] - 0.03, HAIR[1] - 0.005, 0.2], [end(4), HAIR[0] - 0.035, HAIR[1] - 0.005, 0.2]];
  const k6 = [[start(6), HEADLESS[0] - 0.03, HEADLESS[1] + 0.01, 0.3], [end(6), HEADLESS[0] + 0.03, HEADLESS[1] - 0.012, 0.6]];
  const tHead = W(6, 2) - 0.05;

  function props(t, i) {
    const r = S.roach, egg = r.userData.egg;
    let p = HOME, mv = 0, still = true, flat = 1;
    if (i === 1 || i === 2) { const q = path(t, keys); p = q; mv = q[3]; still = false; if (t > W(2, 4)) flat = 1 - 0.55 * ease((t - W(2, 4)) / 0.4); }
    else if (i === 4) { const q = path(t, k4); p = q; mv = q[3]; still = false; }
    else if (i === 6 || i === 5) { const q = path(t, k6); p = q; mv = 1; still = false; }
    r.visible = !(i === 2 && t > W(2, 7) + 0.25) && i !== 3;
    place(r, p, TOP); r.scale.set(RS, RS * flat, RS);
    Q.animateLegs(r, still ? 0 : t * (mv ? 7 : 1.2), still ? 0 : mv ? 1 : 0.15);
    egg.visible = i !== 6 && i !== 5;
    // the head pops off on "live" (line 6), hops, lands beside the walking body
    if (i === 6 && t >= tHead) {
      if (head.parent !== scene) { scene.add(head); head.scale.setScalar(RS); }
      const u = clamp01((t - tHead) / 0.45), hp = [HEADLESS[0] - 0.005, HEADLESS[1] + 0.03];
      const b0 = path(tHead, k6), f = fwd(b0[2], 0.44 * RS);
      head.position.set(b0[0] + f[0] + (hp[0] - b0[0] - f[0]) * u, TOP + 0.002 + 0.03 * Math.sin(Math.PI * u), b0[1] + f[1] + (hp[1] - b0[1] - f[1]) * u);
      head.rotation.set(0, 1.2 + 6 * u, 0);
    } else if (head.parent === scene) { r.userData.body.add(head); head.position.copy(head0); head.scale.setScalar(1); head.rotation.set(0, 0, 0); }
    // 40 babies fan out behind the egg case on "babies"
    const tb = W(0, 8) - 0.12;
    S.nymphs.forEach((n, k) => {
      if (!vis(n, tb + k * 0.012, end(0), t)) return;
      const row = Math.floor(k / 10), col = k % 10, a = Math.PI * (0.62 + 0.76 * col / 9), d = 0.013 + row * 0.0065;
      n.position.set(EGG[0] + Math.cos(a) * d, TOP, EGG[2] + Math.sin(a) * d * 1.3); n.rotation.set(0, -a + Math.PI + 0.3 * Math.sin(k), 0);
      n.scale.setScalar(popS(t, tb + k * 0.012, 0.0045, 0.18)); Q.animateLegs(n, t * 6 + k, 0.6);
    });
    // newspaper slam on "Get it!"
    if (vis(S.paper, W(1, 0) - 0.05, end(1), t)) {
      const u = clamp01((t - W(1, 0) + 0.05) / (tSlam - W(1, 0) + 0.05)), y = t < tSlam ? TOP + 0.24 * (1 - u * u) + 0.028 : TOP + 0.028 + 0.02 * ease((t - tSlam - 0.25) / 0.3);
      S.paper.position.set(HOME[0] + 0.03, y, HOME[1] + 0.02); S.paper.rotation.set(0, -0.2, t < tSlam ? 0.25 * (1 - u) : 0);
    }
    // soap / glue / hair pop on their words; crumbs + toast on "Everything"
    if (vis(S.crumbs, W(4, 0) - 0.05, end(4), t)) { place(S.crumbs, TOAST, TOP); S.crumbs.scale.setScalar(popS(t, W(4, 0) - 0.05, 1)); }
    if (vis(S.soap, W(4, 1) - 0.06, end(4), t)) { place(S.soap, [...SOAP, 0.4], TOP); S.soap.scale.setScalar(popS(t, W(4, 1) - 0.06, 1)); }
    if (vis(S.glue, W(4, 2) - 0.06, end(4), t)) { place(S.glue, [...GLUE, 0.6], TOP); S.glue.scale.setScalar(popS(t, W(4, 2) - 0.06, 1)); }
    if (vis(S.hair, W(4, 3) - 0.06, end(4), t)) { place(S.hair, [...HAIR, 0], TOP); S.hair.scale.setScalar(popS(t, W(4, 3) - 0.06, 1)); }
    if (vis(S.cal, W(6, 4) - 0.06, end(6), t)) { S.cal.position.set(HEADLESS[0] - 0.035, TOP, HEADLESS[1] - 0.05); S.cal.scale.setScalar(popS(t, W(6, 4) - 0.06, 0.22)); }
    S.slipper.visible = i === 5;
  }
  function faceCam(cam) { if (S.cal.visible) S.cal.lookAt(cam.position.x, S.cal.position.y, cam.position.z); }
  const POSES = { ...P.PERSON_POSES };
  return { cfg, props, faceCam, POSES, pose0: 'stand', MB: 0.06, MBPOS, mbY: TOP, PPOS, mbIn: start(2), mbOut: home - 0.5 };
}
