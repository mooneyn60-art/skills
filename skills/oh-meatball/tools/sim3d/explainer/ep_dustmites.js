// Episode: house dust mites (YouTube Short, 10 lines, ~19.7 s, loops). The bed-bug bedroom at night, kept about the bed,
// pillow and dust (no skin/medical framing). Mites are far too small to see (~0.3 mm), so they live in a magnified "microscope
// world" (fabric threads, skin flakes, mites at 100x) built under the floor at y = MY, shown through a 2D microscope iris.
// Beats: pillow push-in -> iris: 8-legged mites (hook) -> Meatball's microscope -> flakes snow down, the mites munch ->
// the pillow gets flung -> freeloaders lounge -> humid mist + a flake blanket -> "HOT WASH / WEEKLY" calendar ->
// "Night night, roomies." pulls back to the opening pillow framing.
import * as THREE from 'three';
import { mat, box } from './lib.js';
import * as P from './props.js';
import * as Q from './props2.js';
import * as R from './props3.js';
import { makeBedroom } from './ep_bedbugs.js';

export const SHIRT = 0x5f9a6a;
export const LIGHT = { bg: 0x05060a, hemi: [0xc2d0ff, 0x5a4a40, 1.0], sun: [0xc8d6ff, 1.3], sunPos: [1.6, 3.0, 1.8], sunTgt: [0, 0.5, 0],
  lamps: [[0xffcf8a, 2.0, [-0.85, 1.0, 1.05]], [0xffe6c4, 0.6, [0.6, 2.3, 0.6]]] };

const MT = 0.55, MY = -20;   // mattress top; microscope-world floor
const MS = 0.03;             // a mite in the microscope world (~0.3 mm at 100x)
const MITES = [[-0.025, 0.0, 0.4], [0.03, -0.02, 2.6], [0.0, 0.04, -1.2], [0.05, 0.03, 1.9], [-0.05, -0.04, -0.3], [-0.07, 0.05, 0.9], [0.07, -0.06, 3.4]];

function makeFabric() {   // woven threads, two layers, over a pale base
  const g = new THREE.Group();
  const base = new THREE.Mesh(new THREE.PlaneGeometry(0.9, 0.9), mat(0x3e5a86, { flatShading: false })); base.rotation.x = -Math.PI / 2; base.position.y = -0.006; g.add(base);
  for (let k = -9; k <= 9; k++) for (const dir of [0, 1]) {
    const f = R.makeFibre(dir ? 0x7f9cc8 : 0x93afd8); f.scale.set(0.9, 0.45, 0.45);
    if (dir) { f.rotation.y = Math.PI / 2; f.position.set(k * 0.045, 0.0, 0); } else f.position.set(0, 0.004 * ((k % 2) ? 1 : -1), k * 0.045);
    g.add(f);
  }
  return g;
}

export function build(scene, S, K) {
  const { L, T_END, start, end, W, cut, popS, vis, place, ease, clamp01 } = K;
  scene.add(makeBedroom());
  const micro = new THREE.Group(); micro.position.set(0, MY, 0); scene.add(micro);
  micro.add(makeFabric());
  const ml = new THREE.PointLight(0xfff2dc, 1.6, 2, 1.2); ml.position.set(0.1, 0.5, 0.25); micro.add(ml);
  S.mites = MITES.map(([x, z, h]) => { const m = R.makeDustMite(); m.scale.setScalar(MS); place(m, [x, z, h], 0.006); micro.add(m); return m; });
  S.flakes = Array.from({ length: 16 }, (_, k) => { const f = R.makeFlake(k); f.scale.setScalar(0.018 + 0.01 * (k % 3)); micro.add(f); return f; });
  S.blanket = R.makeFlake(3); S.blanket.scale.setScalar(0.04); micro.add(S.blanket);
  S.mist = Array.from({ length: 14 }, () => { const m = new THREE.Mesh(new THREE.SphereGeometry(1, 8, 6), new THREE.MeshLambertMaterial({ color: 0xffffff, transparent: true, opacity: 0.25, depthWrite: false })); micro.add(m); return m; });
  S.scope = R.makeMicroscope(); S.scope.scale.setScalar(0.55); S.scope.position.set(-0.7, 0.55, 0.9); S.scope.rotation.y = 0.5; scene.add(S.scope);
  S.cal = Q.makeCal('HOT WASH', 'WEEKLY'); scene.add(S.cal);
  S.pillow = scene.getObjectByName('bedPillow'); const PIL = S.pillow.position.clone();
  S.pillow.geometry = new THREE.IcosahedronGeometry(1, 3); S.pillow.material = new THREE.MeshLambertMaterial({ color: 0xdfe8f5 });   // soft, not a rock

  const POSES = { ...P.PERSON_POSES,
    bed: { py: 0.1, lean: 0.22, hip: [1.5, 1.5], knee: [0, 0], shz: [0.25, 0.55], elz: [0.3, 1.05], shx: [0, 0.15], elx: [0, 0] },
    squint: { py: 0.1, lean: -0.35, hip: [1.5, 1.5], knee: [0, 0], shz: [0.7, 0.7], elz: [1.6, 1.6], shx: [0.2, 0.2], elx: [0, 0] },
    shrug: { py: 0.1, lean: 0.05, hip: [1.5, 1.5], knee: [0, 0], shz: [0.6, 0.55], elz: [1.4, 1.05], shx: [0.5, 0.15], elx: [0, 0] },
    fling: { py: 0.1, lean: 0.1, hip: [1.5, 1.5], knee: [0, 0], shz: [2.4, 2.5], elz: [0.2, 0.2], shx: [0.3, 0.3], elx: [0, 0] },
    hug: { py: 0.1, lean: -0.12, hip: [1.5, 1.5], knee: [0, 0], shz: [1.15, 1.15], elz: [1.1, 1.1], shx: [-0.55, -0.55], elx: [0, 0] },
    fist: { py: 0.1, lean: 0.0, hip: [1.5, 1.5], knee: [0, 0], shz: [0.25, 2.6], elz: [0.3, 0.9], shx: [0, 0], elx: [0, 0] },
  };
  const PPOS = [-0.55, 0.32, 0], MBPOS = [-0.8, 1.06, -0.6];
  const mbAt = (S) => [S.mb.position.x, S.mb.position.y, S.mb.position.z];
  const pHead = (S) => S.person.userData.head.getWorldPosition(new THREE.Vector3()).toArray();
  const PL = [PIL.x, PIL.y + 0.04, PIL.z];
  const OPEN = { c0: [PL[0] + 0.95, PL[1] + 0.5, PL[2] - 0.95], l0: PL, c1: [PL[0] + 0.28, PL[1] + 0.17, PL[2] - 0.45], l1: PL, mv: 1.2 };
  const MC = (dx = 0, dz = 0) => [dx, MY + 0.01, dz];   // a point in the microscope world
  const IRIS = [];   // [t0, t1) windows shown through the microscope iris
  const cfg = L.map(() => ({ shots: [{}] }));
  const set = (i, o) => Object.assign(cfg[i], o);
  const macro = (at, s) => ({ at, ...s, macro: 1 });

  const tFling = W(4, 2) - 0.05, tBlanket = W(7, 2) - 0.08;
  set(0, { cardWord: 4, shots: [{ ...OPEN }, macro(cut(0, 4), { tgt: MC(0, 0), yaw: 60, dist: 0.13, h: 0.09, dyaw: 14, push: 0.8 })] });
  set(1, { cardWord: 2, mbPose: 'point', shots: [{ tgt: [-0.76, 0.68, 0.98], yaw: 25, dist: 0.6, h: 0.12, dyaw: 8, push: 0.9 },
    { at: cut(1, 2), person: 1, tgt: pHead, yaw: 20, dist: 1.1, h: -0.05, ly: -0.15, dyaw: 6, push: 0.85 }], person: { pose: 'squint', from: 'bed' } });
  set(2, { person: { pose: 'shrug', from: 'squint' }, shots: [{ tgt: pHead, yaw: 8, dist: 1.5, h: -0.1, ly: -0.25, dyaw: 6, push: 0.92 }] });
  set(3, { cardWord: 1, shots: [macro(null, { tgt: MC(0, 0), yaw: 100, dist: 0.16, h: 0.08, dyaw: -12, push: 0.8 })] });
  set(4, { person: { pose: 'fling', from: 'bed' }, shots: [{ tgt: [-0.1, 0.9, 0.3], yaw: 40, dist: 2.2, h: 0.35, dyaw: 4, push: 0.95 }] });
  set(5, { cardWord: 0, mood: 'smug', mbPose: 'hips', shots: [{ tgt: mbAt, yaw: -20, dist: 0.45, h: 0.05, dyaw: 8, push: 0.9 },
    macro(cut(5, 1), { tgt: MC(0.02, 0), yaw: 30, dist: 0.13, h: 0.05, dyaw: 10, push: 0.85 })] });
  set(6, { person: { pose: 'hug', from: 'bed', look: (t) => 0.35 * Math.sin((t - start(6)) * 6) }, shots: [{ tgt: pHead, yaw: 14, dist: 1.5, h: -0.1, ly: -0.25, dyaw: -6, push: 0.9 }] });
  set(7, { cardWord: 0, shots: [macro(null, { tgt: MC(-0.03, 0), yaw: 75, dist: 0.13, h: 0.06, dyaw: 12, push: 0.8 })] });
  set(8, { person: { pose: 'fist', from: 'bed' }, shots: [{ tgt: pHead, yaw: 4, dist: 2.0, h: -0.1, ly: -0.12, dyaw: 6, push: 0.92 }] });
  const home = T_END - 0.08, out = cut(9, 5);
  set(9, { cardWord: 1, mood: 'deadpan', mbPose: 'point', shots: [{ tgt: [-0.74, 0.66, 1.03], yaw: -5, dist: 0.75, h: 0.08, dyaw: 6, push: 0.9 },
    { at: out, c0: OPEN.c1, l0: OPEN.l1, c1: OPEN.c0, l1: OPEN.l0, mv: home - out }] });
  cfg[0].hideMb = 1;
  // iris windows (shot start .. next shot start)
  const flat = []; cfg.forEach((c, i) => c.shots.forEach((s, j) => flat.push({ s0: j === 0 ? start(i) : s.at, m: s.macro })));
  flat.forEach((f, k) => { if (f.m) IRIS.push([f.s0, k + 1 < flat.length ? flat[k + 1].s0 : T_END]); });

  function props(t, i) {
    // mites: slow wander + munch (head bob); legs always busy
    S.mites.forEach((m, k) => {
      const [x, z, h] = MITES[k], w = 0.006 * Math.sin(t * 0.7 + k);
      place(m, [x + w * Math.cos(h), z - w * Math.sin(h), h + 0.15 * Math.sin(t * 0.5 + k)], 0.006);
      Q.animateLegs(m, t * 1.2 + k * 0.3, 0.6);
      m.userData.body.rotation.z = i === 3 && t > W(3, 1) ? 0.18 * Math.max(0, Math.sin(t * 14 + k)) : 0;   // munch
      m.rotation.z = i === 5 && k === 1 ? Math.PI * ease(clamp01((t - cut(5, 1)) / 0.4)) : 0;   // one freeloader rolls onto its back
    });
    // skin flakes snow down on "shed" and stay as snacks
    S.flakes.forEach((f, k) => {
      const t0 = W(3, 1) + 0.06 * k, x = 0.16 * Math.sin(k * 2.7), z = 0.13 * Math.cos(k * 1.9);
      if (!vis(f, t0, T_END, t) || i < 3) { f.visible = false; return; }
      const u = clamp01((t - t0) / 0.9); f.position.set(x + 0.02 * Math.sin(t * 3 + k) * (1 - u), 0.25 * (1 - u) + 0.008, z); f.rotation.set(0.6 * (1 - u) * Math.sin(k + t * 4), k, 0);
    });
    // "Cozy.": a mite pulls a flake over itself like a blanket
    const bm = S.mites[0];
    if (vis(S.blanket, tBlanket, end(7), t)) { const u = ease(clamp01((t - tBlanket) / 0.3)); S.blanket.position.set(bm.position.x, 0.004 + 0.016 * u, bm.position.z); S.blanket.rotation.set(0, 0.3, 0.2 * (1 - u)); }
    // humid mist drifting up through the threads (line 7)
    S.mist.forEach((m, k) => { const ph = ((t * 0.12 + k / 14) % 1); m.visible = i === 7; m.position.set(0.18 * Math.sin(k * 3.3), 0.02 + 0.2 * ph, 0.15 * Math.cos(k * 2.1)); m.scale.setScalar(0.02 + 0.04 * ph); m.material.opacity = 0.22 * Math.sin(Math.PI * ph); });
    // the pillow gets flung on "bite?!" and is back on the bed (off camera) from line 9
    if (i >= 4 && i < 9 && t >= tFling) { const u = clamp01((t - tFling) / 0.55); S.pillow.position.set(PIL.x + 1.9 * u, PIL.y + 0.7 * Math.sin(Math.PI * u) - 0.55 * u * u, PIL.z + 0.9 * u); S.pillow.rotation.set(0, 0, 5 * u); }
    else { S.pillow.position.copy(PIL); S.pillow.rotation.set(0, 0, 0); }
    if (vis(S.cal, W(9, 1) - 0.06, out, t)) { S.cal.position.set(-0.64, 0.55, 1.0); S.cal.scale.setScalar(popS(t, W(9, 1) - 0.06, 0.7)); }
  }
  function faceCam(cam) { if (S.cal.visible) S.cal.lookAt(cam.position.x, S.cal.position.y, cam.position.z); }
  // microscope iris: everything outside a circle goes black; a thin rim + a small label
  function overlay(c, t) {
    const w = IRIS.find(([a, b]) => t >= a && t < b); if (!w) return;
    const r = 470 * Math.min(1, 0.2 + 0.8 * ease((t - w[0]) / 0.22)), cx = 540, cy = 930;
    c.save(); c.fillStyle = '#000'; c.beginPath(); c.rect(0, 0, 1080, 1920); c.arc(cx, cy, r, 0, Math.PI * 2, true); c.fill('evenodd');
    c.strokeStyle = '#3a3a3a'; c.lineWidth = 14; c.beginPath(); c.arc(cx, cy, r, 0, Math.PI * 2); c.stroke();
    c.fillStyle = 'rgba(255,255,255,0.75)'; c.font = '700 30px Inter'; c.textAlign = 'center'; c.letterSpacing = '6px'; c.fillText('MICROSCOPE VIEW', cx, cy + r + 52); c.letterSpacing = '0px';
    c.restore();
  }
  return { cfg, props, faceCam, overlay, POSES, pose0: 'bed', personY: MT - 0.02, MB: 0.07, MBPOS, mbY: 0.55, PPOS, mbIn: start(1), mbOut: home - 0.5 };
}
