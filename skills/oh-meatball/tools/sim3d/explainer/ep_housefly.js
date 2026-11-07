// Episode: house fly (YouTube Short, 10 lines, ~19.6 s, loops). Same low-poly night kitchen as the roach episode.
// Beats: a fly lands on the sandwich and tastes it with its feet (hook) -> "barfs" a drop, spit puddle, slurp ->
// bug zapper: a second fly hits the paddle and bursts into bits -> the first fly lays eggs in the trash ->
// "7 DAYS" calendar, a swarm of grandkids lifts off -> "Enjoy your sandwich." cranes back to the opening (a fly arriving).
// The kitchen set is a copy of ep_roach.js makeKitchen (minus the backsplash crack) so ep_roach.js stays untouched.
import * as THREE from 'three';
import { mat, mesh, box, cyl, texMat, tileTex, canvasTex, wallPlane, shade, ICO, ICO1 } from './lib.js';
import * as P from './props.js';
import * as Q from './props2.js';
import * as R from './props3.js';

export const SHIRT = 0x7a4f8f;
export const LIGHT = { bg: 0x0e1426, hemi: [0xc9d6ff, 0x6a5a48, 1.05], sun: [0xd2ddff, 1.5], sunPos: [-0.8, 3.2, 2.4], sunTgt: [0, 0.9, -0.3],
  lamps: [[0xffd59a, 1.7, [0.0, 1.38, -0.42]], [0xffe6c4, 0.9, [0.3, 2.3, 0.7]]] };

const TOP = 0.9;              // countertop height
const FS = 0.014;             // house fly ~7 mm; drawn a touch bigger so it reads
const SW = [0.02, -0.27];     // sandwich on its plate
const BIN = [0.98, 0.3], BINH = 0.42, BINR = 0.13;
const FH = -1.0;              // the fly faces the camera side (+x +z)

function makeKitchen() {
  const g = new THREE.Group();
  const wood = texMat(canvasTex(256, 256, (c, w) => { for (let i = 0; i < 8; i++) { c.fillStyle = shade('#9c6b42', ((i * 37) % 9) - 4); c.fillRect(0, i * 32, w, 31); c.fillStyle = '#6a4528'; c.fillRect(0, i * 32 + 31, w, 1); } }, [5, 5]));
  const fl = new THREE.Mesh(new THREE.PlaneGeometry(4.4, 3.4), wood); fl.rotation.x = -Math.PI / 2; fl.position.set(0.1, 0, 1.0); fl.receiveShadow = true; g.add(fl);
  const paint = mat(0xd9cdb6, { flatShading: false });
  g.add(wallPlane(4.4, 2.5, paint, 0.1, -0.6, 0));
  g.add(wallPlane(3.4, 2.5, paint, -2.1, 1.0, Math.PI / 2), wallPlane(3.4, 2.5, paint, 2.3, 1.0, -Math.PI / 2), wallPlane(4.4, 2.5, paint, 0.1, 2.7, Math.PI));
  const ceil = new THREE.Mesh(new THREE.PlaneGeometry(4.4, 3.4), paint); ceil.rotation.x = Math.PI / 2; ceil.position.set(0.1, 2.5, 1.0); g.add(ceil);
  g.add(wallPlane(2.5, 0.55, texMat(tileTex('#e8eef0', '#aab7bc', 4, [10, 2.2])), 0, -0.598, 0, TOP));
  const cab = 0x5f8a78, cabD = shade('#5f8a78', -18);
  g.add(box(2.5, 0.86, 0.56, cab, 0, 0, -0.32));
  for (let k = 0; k < 5; k++) { g.add(box(0.47, 0.7, 0.01, cabD, -1.0 + k * 0.5, 0.08, -0.035, false)); g.add(box(0.1, 0.018, 0.02, 0xd0d0d0, -1.0 + k * 0.5, 0.68, -0.025, false)); }
  g.add(box(2.56, 0.04, 0.62, mat(0xe2dccf), 0, TOP - 0.04, -0.29));
  g.add(box(0.46, 0.004, 0.36, 0x9ea4aa, 0.62, TOP, -0.3, false), box(0.4, 0.005, 0.3, 0x50565c, 0.62, TOP, -0.3, false));
  const fa = cyl(0.012, 0.012, 0.25, 0xc8ccd0, 8); fa.position.set(0.62, TOP + 0.125, -0.52); g.add(fa);
  const sp = cyl(0.01, 0.01, 0.14, 0xc8ccd0, 8); sp.rotation.x = Math.PI / 2; sp.position.set(0.62, TOP + 0.245, -0.46); g.add(sp);
  for (const [x, z] of [[-0.88, -0.2], [-0.62, -0.2], [-0.88, -0.42], [-0.62, -0.42]]) { const b = mesh(new THREE.TorusGeometry(0.06, 0.01, 4, 14), mat(0x1a1a1a)); b.rotation.x = Math.PI / 2; b.position.set(x, TOP + 0.006, z); g.add(b); }
  g.add(box(0.55, 0.003, 0.5, 0x2a2a2e, -0.75, TOP, -0.31, false));
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

// sandwich on a plate; returns [group, top-of-bread height above the counter]
function makeSandwich() {
  const g = new THREE.Group();
  const plate = cyl(0.085, 0.07, 0.008, 0xf4f2ec, 18); plate.position.y = 0.004; g.add(plate);
  let y = 0.008;
  const layer = (w, h, d, c, dx = 0, dz = 0, ry = 0) => { const b = mesh(new THREE.BoxGeometry(w, h, d, 2, 1, 2), mat(c)); b.position.set(dx, y + h / 2, dz); b.rotation.y = ry; g.add(b); y += h; return b; };
  layer(0.095, 0.014, 0.095, 0xd9a866);           // bottom slice (crust colour)
  layer(0.1, 0.004, 0.1, 0x5fae3c, 0.002, -0.002, 0.25);   // lettuce
  layer(0.092, 0.006, 0.09, 0xe39a9a, -0.002, 0.001, -0.12); // ham
  layer(0.088, 0.004, 0.088, 0xf2c94c, 0.003, 0.002, 0.45);  // cheese, turned
  const top = layer(0.095, 0.016, 0.095, 0xd9a866, 0, 0, 0.05);
  const crumb = box(0.085, 0.0012, 0.085, 0xf1dfb8, 0, y, 0, false); crumb.rotation.y = 0.05; g.add(crumb);   // pale crumb face
  y += 0.0012;
  return [g, y, top];
}

// electric bug-zapper paddle in the hand: handle + head along the hand's -y, face in the y-z plane
function makeZapper() {
  const g = new THREE.Group();
  const h = cyl(0.014, 0.012, 0.15, 0x2d4f8a, 8); h.position.y = -0.09; g.add(h);
  g.add(box(0.012, 0.012, 0.03, 0xd7261e, 0.012, -0.06, 0, false));      // the button
  const head = new THREE.Group(); head.position.y = -0.31; g.add(head);
  const Y = 0xf2c230, w = 0.2, hh = 0.26, t = 0.014;
  head.add(box(t, t, w, Y, 0, hh / 2 - t / 2, 0), box(t, t, w, Y, 0, -hh / 2 - t / 2, 0));
  const side = (s) => { const b = box(t, hh, t, Y, 0, -hh / 2, s * (w / 2 - t / 2)); head.add(b); };
  side(-1); side(1);
  const wire = 0x9aa0a6;
  for (let k = 1; k < 9; k++) head.add(box(0.002, hh - t, 0.0015, wire, 0, -hh / 2, -w / 2 + k * w / 9, false));
  for (let k = 1; k < 11; k++) head.add(box(0.002, 0.0015, w - t, wire, 0, -hh / 2 + k * hh / 11 - t / 2, 0, false));
  const glowM = new THREE.MeshBasicMaterial({ color: 0x8fd8ff, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide });
  const glow = new THREE.Mesh(new THREE.PlaneGeometry(w, hh), glowM); glow.rotation.y = Math.PI / 2; glow.position.y = -t / 2; head.add(glow);
  g.userData = { head, glowM };
  return g;
}

function makeBin() {
  const g = new THREE.Group();
  const side = new THREE.Mesh(new THREE.CylinderGeometry(BINR, BINR * 0.85, BINH, 16, 1, true), mat(0x4a6b8a, { side: THREE.DoubleSide }));
  side.position.y = BINH / 2; side.castShadow = true; side.receiveShadow = true; g.add(side);
  const rim = mesh(new THREE.TorusGeometry(BINR, 0.007, 4, 18), mat(0x3a5672)); rim.rotation.x = Math.PI / 2; rim.position.y = BINH; g.add(rim);
  const bag = cyl(BINR - 0.004, BINR - 0.004, 0.01, 0x1d1f22, 16); bag.position.y = BINH - 0.05; g.add(bag);
  const junk = [[0xf1efe8, 0.04, -0.04, 0.03, 0.035], [0xe8e2d0, 0.03, 0.05, -0.02, 0.03], [0xc94a3a, 0.025, -0.06, -0.05, 0.022], [0x8a6a4a, 0.035, 0.0, 0.07, 0.02]];
  for (const [c, r, x, z, hgt] of junk) { const m = mesh(ICO, mat(c)); m.scale.set(r, hgt, r); m.position.set(x, BINH - 0.045 + hgt * 0.5, z); m.rotation.y = x * 20; g.add(m); }
  // banana peel the fly lays on (the eggs sit on it)
  const peel = new THREE.Group(); peel.position.set(0.01, BINH - 0.028, 0.0);
  for (let k = 0; k < 4; k++) { const p = mesh(ICO1, mat(k ? 0xe8c33a : 0xd9b02c)); p.scale.set(0.05, 0.008, 0.016); p.rotation.y = k * Math.PI / 2 + 0.3; p.position.set(Math.cos(k * Math.PI / 2 + 0.3) * 0.035, 0, -Math.sin(k * Math.PI / 2 + 0.3) * 0.035); peel.add(p); }
  const stem = mesh(ICO1, mat(0x5a4426)); stem.scale.set(0.012, 0.01, 0.012); peel.add(stem); g.add(peel);
  g.userData = { peelY: BINH - 0.02 };
  return g;
}

// fly extras: a proboscis under the head and a drop of saliva on its tip
function dressFly(f) {
  const b = f.userData.body;
  const pr = new THREE.Group(); pr.position.set(0.4, 0.22, 0); b.add(pr);
  const tube = cyl(0.03, 0.02, 1, 0x4a2a22, 6); tube.position.y = -0.5; pr.add(tube);
  const pad = mesh(ICO1, mat(0x6a3a2c)); pad.scale.set(0.06, 0.03, 0.08); pad.position.y = -1; pr.add(pad);
  const drop = mesh(ICO1, new THREE.MeshLambertMaterial({ color: 0xeedc8a, transparent: true, opacity: 0.8, emissive: 0x3a3010 }), false);
  drop.position.set(0.44, 0.0, 0); b.add(drop);
  f.userData.prob = pr; f.userData.drop = drop;
  pr.scale.set(1, 0.001, 1);
}

// piecewise path: keys [[t, x, y, z], ...] -> [x, y, z], eased per segment
function path3(t, keys, ease) {
  if (t <= keys[0][0]) return keys[0].slice(1);
  for (let k = 0; k + 1 < keys.length; k++) {
    const [a, b] = [keys[k], keys[k + 1]];
    if (t < b[0]) { const u = ease((t - a[0]) / (b[0] - a[0])); return [1, 2, 3].map((j) => a[j] + (b[j] - a[j]) * u); }
  }
  return keys[keys.length - 1].slice(1);
}

export function build(scene, S, K) {
  const { L, T_END, start, end, W, cut, popS, vis, place, fwd, ease, clamp01 } = K;
  scene.add(makeKitchen());
  const [sand, sandH] = makeSandwich(); sand.position.set(SW[0], TOP, SW[1]); scene.add(sand);
  const SY = TOP + sandH;
  S.bin = makeBin(); S.bin.position.set(BIN[0], 0, BIN[1]); scene.add(S.bin);
  const PEEL = [BIN[0] + 0.01, S.bin.userData.peelY, BIN[1]];

  S.fly = R.makeFly(); dressFly(S.fly); S.fly.scale.setScalar(FS); scene.add(S.fly);
  S.fly2 = R.makeFly(); S.fly2.scale.setScalar(0.016); scene.add(S.fly2);
  S.kids = []; for (let k = 0; k < 14; k++) { const f = R.makeFly(); scene.add(f); S.kids.push(f); }
  S.eggs = []; for (let k = 0; k < 36; k++) { const e = Q.makeBugEgg(); scene.add(e); S.eggs.push(e); }
  S.cal = Q.makeCal('EGG TO FLY', '7 DAYS'); scene.add(S.cal);
  S.zap = makeZapper(); S.person.userData.hands[1].add(S.zap);
  // spit puddle on the bread, taste sparkles at the feet, zap flash + bits
  S.puddle = mesh(ICO1, new THREE.MeshLambertMaterial({ color: 0xe9d27c, transparent: true, opacity: 0.78, emissive: 0x2a2208 }), false); scene.add(S.puddle);
  const sparkM = new THREE.MeshBasicMaterial({ color: 0xffe35a, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending, depthWrite: false });
  S.sparks = []; for (let k = 0; k < 6; k++) { const s = new THREE.Mesh(new THREE.RingGeometry(0.6, 1, 14), sparkM); s.rotation.x = -Math.PI / 2; scene.add(s); S.sparks.push(s); }
  const flashM = new THREE.MeshBasicMaterial({ color: 0xbfeaff, transparent: true, opacity: 1, blending: THREE.AdditiveBlending, depthWrite: false });
  S.flash = new THREE.Mesh(ICO1, flashM); scene.add(S.flash);
  S.bits = []; for (let k = 0; k < 16; k++) {
    const m = k % 4 === 3 ? new THREE.MeshLambertMaterial({ color: 0xdfeaf2, transparent: true, opacity: 0.6, side: THREE.DoubleSide }) : mat(k % 4 === 2 ? 0x9a1e14 : 0x2a2a30);
    const b = mesh(ICO, m, false); scene.add(b); S.bits.push(b);
  }

  const MBPOS = [0.2, -0.2, -Math.PI / 2 - 0.35], PPOS = [0.36, 1.45, Math.PI / 2];
  const mbAt = (S) => [S.mb.position.x, S.mb.position.y, S.mb.position.z];
  const F3 = [SW[0] + 0.02, SY, SW[1] + 0.026];                        // where the fly stands on the bread
  const FLYIN = [F3[0] - 0.01, F3[1] + 0.024, F3[2] + 0.006];               // it arrives from here (t = 0 and the loop end)
  const OPEN = { c0: [F3[0] + 0.06, F3[1] + 0.012, F3[2] + 0.11], l0: [F3[0] - 0.01, F3[1] - 0.008, F3[2] - 0.01],
    c1: [F3[0] + 0.032, F3[1] + 0.009, F3[2] + 0.056], l1: [F3[0], F3[1] + 0.002, F3[2]], mv: 1.9 };
  const zapAt = (S) => S.zap.userData.head.getWorldPosition(new THREE.Vector3()).toArray();
  const cfg = L.map(() => ({ shots: [{}] }));
  const set = (i, o) => Object.assign(cfg[i], o);
  const PSHOT = { c0: [0.12, 1.46, -0.24], l0: [0.36, 1.62, 1.45], c1: [0.15, 1.47, -0.12], l1: [0.36, 1.64, 1.45] };

  const tLand = 0.6, tBarf = W(1, 3) - 0.05, tZap = W(5, 5) - 0.05;
  set(0, { cardWord: 7, shots: [{ ...OPEN }, { at: cut(0, 5), tgt: [F3[0], F3[1] + 0.002, F3[2]], yaw: 48, dist: 0.042, h: 0.007, dyaw: 14, push: 0.85 }] });
  set(1, { mood: 'deadpan', shots: [{ tgt: [0.11, TOP + 0.06, -0.23], yaw: 84, dist: 0.55, h: 0.08, dyaw: 4, push: 0.92 },
    { at: cut(1, 3), tgt: [F3[0], F3[1] + 0.004, F3[2]], yaw: 58, dist: 0.05, h: 0.01, dyaw: 10, push: 0.85 }] });
  set(2, { person: { pose: 'back', from: 'stand', look: (t) => 0.5 * Math.sin((t - start(2)) * 7) }, shots: [{ ...PSHOT }] });
  set(3, { cardWord: 0, mood: 'smug', shots: [{ tgt: [F3[0] + 0.004, F3[1] + 0.002, F3[2] + 0.004], yaw: 38, dist: 0.06, h: 0.022, dyaw: 18, push: 0.88 }] });
  set(4, { person: { pose: 'slipper', from: 'stand' }, shots: [{ c0: [0.12, 1.46, -0.24], l0: [0.36, 1.72, 1.45], c1: [0.14, 1.47, -0.16], l1: [0.36, 1.74, 1.45] }] });
  set(5, { cardWord: 4, mood: 'alarm', mbPose: 'stop', person: { pose: 'slipper' },
    shots: [{ tgt: (S) => [S.mb.position.x - 0.08, S.mb.position.y, S.mb.position.z], yaw: 80, dist: 0.5, h: 0.04, dyaw: 4, push: 0.9 },
      { at: cut(5, 4), tgt: zapAt, yaw: -78, dist: 0.75, h: 0.02, dyaw: 6, push: 0.9, shake: { t: tZap, a: 0.01 } }] });
  set(6, { mbPose: 'shrug', person: { pose: 'stand', from: 'slipper', look: (t) => 0.3 * Math.sin((t - start(6)) * 3) }, shots: [{ ...PSHOT }] });
  const BT = [BIN[0], BINH, BIN[1]];
  set(7, { cardWord: 3, mood: 'smug', shots: [{ tgt: [BT[0], BT[1] - 0.01, BT[2]], yaw: 72, dist: 0.24, h: 0.2, dyaw: 8, push: 0.82 }] });
  const CAL = [BIN[0] + 0.24, BIN[1] + 0.06];
  set(8, { cardWord: 1, mood: 'smug', shots: [{ c0: [BIN[0] + 0.14, 0.4, BIN[1] + 1.45], l0: [BIN[0] + 0.12, 0.13, BIN[1]], c1: [BIN[0] + 0.14, 0.38, BIN[1] + 1.25], l1: [BIN[0] + 0.12, 0.13, BIN[1]] },
    { at: cut(8, 3), tgt: [BIN[0], BINH + 0.1, BIN[1]], yaw: 82, dist: 0.42, h: 0.06, dyaw: 6, push: 1.15 }] });
  const home = T_END - 0.08, out = W(9, 2) + 0.05;
  set(9, { mood: 'smug', mbPose: 'hips', shots: [{ tgt: (S) => [S.mb.position.x - 0.06, S.mb.position.y, S.mb.position.z], yaw: 78, dist: 0.5, h: 0.03, dyaw: 4, push: 0.9 },
    { at: out, c0: [MBPOS[0] + 0.12, TOP + 0.14, MBPOS[1] + 0.34], l0: [MBPOS[0], TOP + 0.1, MBPOS[1]], c1: OPEN.c0, l1: OPEN.l0, mv: home - out }] });
  cfg[0].hideMb = 1;

  // main fly: lands at t = 0..tLand, sits until line 7, flies into the bin, lays eggs; flies back in for the loop
  const binIn = [[start(7), PEEL[0] - 0.16, PEEL[1] + 0.2, PEEL[2] + 0.08], [W(7, 2) - 0.08, PEEL[0] - 0.02, PEEL[1] + 0.004, PEEL[2] + 0.02]];
  const EGGC = [PEEL[0] + 0.018, PEEL[1], PEEL[2] + 0.004];
  const loopIn = [[out, FLYIN[0] + 0.22, FLYIN[1] + 0.12, FLYIN[2] + 0.25], [home, ...FLYIN], [T_END, ...FLYIN]];
  function flyState(t, i) {
    if (t < tLand) { const u = ease(t / tLand); return { p: [FLYIN[0] + (F3[0] - FLYIN[0]) * u, FLYIN[1] + (F3[1] - FLYIN[1]) * u, FLYIN[2] + (F3[2] - FLYIN[2]) * u], h: FH, fly: 1 - clamp01((t - tLand + 0.08) / 0.08), vis: 1 }; }
    if (i <= 6) return { p: F3, h: FH, fly: 0, vis: 1 };
    if (i === 7 || i === 8) { const p = path3(t, binIn, ease); return { p, h: -0.4, fly: t < binIn[1][0] ? 1 : 0, vis: 1 }; }
    if (t >= out) return { p: path3(t, loopIn, ease), h: FH, fly: 1, vis: 1 };
    return { p: F3, h: FH, fly: 0, vis: 0 };
  }
  const flap = (f, t, on, sp = 70) => f.userData.wings.forEach((w, k) => { const s = k ? 1 : -1; w.rotation.x = on ? s * (0.25 + 0.75 * Math.sin(t * sp + k * 0.3)) : 0; w.rotation.y = s * (on ? 0.1 : 0.35); });

  // the zap victim flies at the paddle face from the camera side; bits burst along random rays
  const RNG = (k) => { const x = Math.sin(k * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
  const bitV = S.bits.map((_, k) => { const a = RNG(k) * Math.PI * 2, e = -0.3 + RNG(k + 50) * 1.3, v = 0.55 + 0.6 * RNG(k + 90); return [Math.cos(a) * Math.cos(e) * v, Math.sin(e) * v + 0.25, Math.sin(a) * Math.cos(e) * v, 0.0025 + 0.004 * RNG(k + 7)]; });

  function props(t, i, pe) {
    // main fly
    const f = S.fly, st = flyState(t, i);
    f.visible = !!st.vis;
    const bob = st.fly ? 0.0015 * Math.sin(t * 23) : 0;
    f.position.set(st.p[0], st.p[1] + bob, st.p[2]); f.rotation.set(0, st.h, st.fly ? 0.12 : 0);
    flap(f, t, st.fly > 0.5);
    const tasting = (i === 0 && t > tLand) || i === 3;
    Q.animateLegs(f, st.fly ? 0 : t * (tasting ? 4.5 : 1.5), st.fly ? 0 : tasting ? 0.45 : 0.12);
    // proboscis: down on "feet", on "barfs" with a drop, through the spit/slurp line
    let pr = 0;
    if (i === 0) pr = ease((t - W(0, 7) + 0.05) / 0.25);
    else if (i === 1) pr = ease((t - tBarf) / 0.2);
    else if (i === 2) pr = 1;
    else if (i === 3) pr = t < W(3, 5) ? 1 : 1 - 0.6 * ease((t - W(3, 5) - 0.4) / 0.3);
    f.userData.prob.scale.set(1, Math.max(0.001, pr * 0.22), 1);
    const drop = f.userData.drop; drop.visible = (i === 1 && t > tBarf) || i === 2;
    const dk = i === 1 ? popS(t, tBarf + 0.05, 1, 0.3) : 1; drop.scale.set(0.11 * dk, 0.08 * dk, 0.11 * dk);
    // spit puddle grows "till it's soup", vanishes on "slurps"
    if (vis(S.puddle, start(3), end(3), t)) {
      const g = ease((t - W(3, 0)) / (W(3, 3) + 0.25 - W(3, 0))), s = t < W(3, 5) ? g : 1 - ease((t - W(3, 5) - 0.05) / 0.45);
      const fp = fwd(FH, 0.46 * FS);
      S.puddle.position.set(F3[0] + fp[0], F3[1] + 0.0005, F3[2] + fp[1]);
      S.puddle.scale.set(0.0001 + 0.0055 * s, 0.0001 + 0.0012 * s, 0.0001 + 0.0055 * s);
      S.puddle.visible = s > 0.01;
    }
    // taste sparkles under the feet on "tasting ... feet"
    const sp0 = W(0, 2) - 0.05;
    S.sparks.forEach((s, k) => {
      if (!vis(s, sp0 + k * 0.05, end(0), t)) return;
      const side = k % 2 ? 1 : -1, row = Math.floor(k / 2), lx = (0.28 - row * 0.2) * FS, lz = side * (0.32 + 0.04 * row) * FS;
      const c = Math.cos(FH), sn = Math.sin(FH);
      s.position.set(F3[0] + lx * c + lz * sn, F3[1] + 0.0003, F3[2] - lx * sn + lz * c);
      const ph = (t - sp0 - k * 0.05) * 2.2; s.scale.setScalar(FS * (0.08 + 0.12 * (ph % 1))); s.material.opacity = 0.9;
    });
    sparkM.opacity = 0.9 * (1 - ((t * 2.2) % 1) * 0.7);

    // zapper in hand on lines 4-6, glows on impact
    S.zap.visible = i >= 4 && i <= 6;
    S.zap.userData.glowM.opacity = t >= tZap && t < tZap + 0.5 ? 0.9 * Math.exp(-(t - tZap) / 0.15) + 0.25 * (Math.sin(t * 90) > 0 ? 1 : 0) * Math.exp(-(t - tZap) / 0.2) : 0;
    const Z = i === 5 ? zapAt(S) : null;
    if (Z && vis(S.fly2, cut(5, 4) - 0.05, tZap, t)) {
      const u = clamp01((t - cut(5, 4) + 0.05) / (tZap - cut(5, 4) + 0.05)), a = [Z[0] + 0.12, Z[1] + 0.08, Z[2] - 0.32];
      S.fly2.position.set(a[0] + (Z[0] - a[0]) * u, a[1] + (Z[1] - a[1]) * u + 0.01 * Math.sin(t * 19), a[2] + (Z[2] - a[2]) * u);
      S.fly2.rotation.set(0, Math.PI / 2 + 0.4, 0.15); flap(S.fly2, t, true, 75); Q.animateLegs(S.fly2, 0, 0);
    } else S.fly2.visible = false;
    if (Z && vis(S.flash, tZap, tZap + 0.3, t)) { const u = (t - tZap) / 0.3; S.flash.position.set(Z[0] - 0.01, Z[1], Z[2]); S.flash.scale.setScalar(0.01 + 0.035 * ease(u)); flashM.opacity = 1 - u; }
    else S.flash.visible = false;
    S.bits.forEach((b, k) => {
      if (!Z || !vis(b, tZap, end(5), t)) return;
      const d = t - tZap, v = bitV[k];
      b.position.set(Z[0] - 0.015 + v[0] * d, Z[1] + v[1] * d - 1.6 * d * d, Z[2] - 0.02 + v[2] * d);
      b.scale.set(v[3], v[3] * (k % 4 === 3 ? 0.15 : 0.8), v[3] * 0.8); b.rotation.set(t * 9 + k, t * 7, k);
    });

    // eggs pop in a heap on "eggs" (line 7), hatch away on "Grandkids"
    const te = W(7, 3) - 0.12, tKids = W(8, 3) - 0.1;
    S.eggs.forEach((e, k) => {
      if (!vis(e, te + k * 0.018, i === 8 ? tKids + 0.2 : end(8), t) || (i !== 7 && i !== 8)) { e.visible = false; return; }
      const a = k * 2.399, r = 0.003 + 0.0028 * Math.sqrt(k);
      e.position.set(EGGC[0] + Math.cos(a) * r, EGGC[1] + 0.0012 * (k % 3), EGGC[2] + Math.sin(a) * r);
      e.rotation.set(0, a * 1.7, 0);
      const s = popS(t, te + k * 0.018, 0.0055, 0.2) * (t > tKids ? 1 - ease((t - tKids) / 0.2) : 1); e.scale.setScalar(Math.max(0.0001, s));
    });
    // the "7 DAYS" calendar on the floor by the bin
    if (vis(S.cal, W(8, 1) - 0.08, end(8), t)) { S.cal.position.set(CAL[0], 0, CAL[1]); S.cal.scale.setScalar(popS(t, W(8, 1) - 0.08, 2.0)); }
    // grandkids lift off the bin in a buzzing column
    S.kids.forEach((g, k) => {
      if (!vis(g, tKids + k * 0.03, end(8), t)) return;
      const d = t - tKids - k * 0.03, a = k * 2.4 + d * (2.5 + RNG(k) * 2), r = 0.03 + 0.09 * RNG(k + 3) + 0.05 * d;
      g.position.set(BIN[0] + Math.cos(a) * r, PEEL[1] + 0.02 + d * (0.17 + 0.12 * RNG(k + 11)) + 0.01 * Math.sin(t * 13 + k), BIN[1] + Math.sin(a) * r);
      g.rotation.set(0.2 * Math.sin(t * 9 + k), -a - Math.PI / 2, 0.15);
      g.scale.setScalar(popS(t, tKids + k * 0.03, 0.03, 0.15)); flap(g, t + k * 0.11, true, 72); Q.animateLegs(g, 0, 0);
    });
  }
  function faceCam(cam) { if (S.cal.visible) S.cal.lookAt(cam.position.x, S.cal.position.y, cam.position.z); }
  const POSES = { ...P.PERSON_POSES };
  return { cfg, props, faceCam, POSES, pose0: 'stand', MB: 0.06, MBPOS, mbY: TOP, PPOS, mbIn: start(1), mbOut: home - 0.5 };
}
