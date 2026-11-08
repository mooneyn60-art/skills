// Episode: brown marmorated stink bug (YouTube Short ~16.3 s, 9 lines, loops) + micro-loop (KEY=loop, one line, ~7.3 s).
// NEW opening (research 68): frame 1 is already a macro on a stink bug crawling out of a wall crack beside the window.
// Same sunny living room as ep_jumpspider.js (fall). Beats: bug out of the crack (hook) -> "moved in last fall / with friends"
// (cutaway: a cluster inside the wall) -> the person raises a slipper -> green stink cloud -> vacuum wand -> the vacuum puffs
// stink -> "lay eggs?" -> "don't breed indoors" -> "hang out all winter" (cluster) -> pulls back to the crack.
// Source: Penn State Extension, Brown Marmorated Stink Bug.
import * as THREE from 'three';
import { mat, mesh, box, cyl, limbGeo, ICO, ICO1 } from './lib.js';
import * as P from './props.js';
import * as Q from './props2.js';
import { makeLivingRoom, LIGHT as JL } from './ep_jumpspider.js';

export const SHIRT = 0x8a4f3a;
export const LIGHT = JL;

const SILL = 1.0, WALLZ = -0.6;
const BS = 0.017;                     // BMSB ~5/8 inch
const CRACK = [0.24, 0.74];           // on the back wall under the window sill
const CUT = [-0.22, 0.84];            // wall cutaway under the sill (the bugs' winter hideout)
const TAU = Math.PI * 2;

function sixLegs(g, m, y, x0, dx, len, r) {
  const legs = [];
  for (const s of [-1, 1]) for (let k = 0; k < 3; k++) {
    const hip = new THREE.Group(); hip.position.set(x0 - k * dx, y, s * 0.14); hip.rotation.order = 'YXZ'; g.add(hip);
    hip.add(mesh(limbGeo(r, r * 0.8, len * 0.45, 4), m));
    const knee = new THREE.Group(); knee.position.z = len * 0.45; hip.add(knee);
    knee.add(mesh(limbGeo(r * 0.8, r * 0.4, len * 0.6, 4), m));
    const kn = 0.15 + Math.asin(Math.min(0.95, (y + len * 0.45 * Math.sin(0.15)) / (len * 0.6)));
    legs.push({ hip, knee, s, k, kn, yaw0: (k - 1) * -0.7 });
  }
  return legs;
}

// brown marmorated stink bug: mottled brown shield, wide shoulders, banded edges, white-banded antennae
export function makeStinkBug() {
  const g = new THREE.Group(), body = new THREE.Group(); g.add(body);
  const brn = mat(0x6e5440), lt = mat(0xd8c8a0), dk = mat(0x3a2a1e), legM = mat(0x8a6a4c);
  const ab = mesh(ICO1, brn); ab.scale.set(0.42, 0.08, 0.3); ab.position.set(-0.12, 0.13, 0); body.add(ab);
  const pro = mesh(ICO1, mat(0x7a5e46)); pro.scale.set(0.14, 0.08, 0.36); pro.position.set(0.2, 0.14, 0); body.add(pro);
  const scu = mesh(ICO1, mat(0x8a6c52)); scu.scale.set(0.2, 0.05, 0.12); scu.position.set(0.0, 0.19, 0); body.add(scu);
  const mem = mesh(ICO1, dk); mem.scale.set(0.14, 0.05, 0.2); mem.position.set(-0.42, 0.15, 0); body.add(mem);
  for (let k = 0; k < 18; k++) { const m = mesh(ICO, mat(k % 3 ? 0x65503e : 0x7c6450), false); m.scale.set(0.045, 0.003, 0.04); m.position.set(-0.4 + (k % 6) * 0.11, 0.205, -0.16 + Math.floor(k / 6) * 0.15); body.add(m); }
  for (const s of [-1, 1]) for (let k = 0; k < 5; k++) { const b = box(0.06, 0.03, 0.03, k % 2 ? 0xd8c8a0 : 0x2e2218, -0.38 + k * 0.1, 0.11, s * 0.29, false); body.add(b); }
  const head = mesh(ICO1, brn); head.scale.set(0.12, 0.06, 0.1); head.position.set(0.4, 0.13, 0); body.add(head);
  for (const s of [-1, 1]) { const e = mesh(ICO1, mat(0x2a1a14), false); e.scale.setScalar(0.035); e.position.set(0.42, 0.15, s * 0.08); body.add(e); }
  const ants = [];
  for (const s of [-1, 1]) {
    const a = new THREE.Group(); a.position.set(0.48, 0.15, s * 0.05); a.rotation.order = 'YXZ'; a.rotation.y = Math.PI / 2 - s * 0.55; a.userData.s = s; body.add(a);
    for (let k = 0; k < 5; k++) { const seg = mesh(limbGeo(0.016, 0.013, 0.1, 4), k === 3 ? lt : k === 4 ? lt : dk, false); seg.position.z = k * 0.1; seg.rotation.x = -Math.PI / 2; a.add(seg); }
    ants.push(a);
  }
  const legs = sixLegs(body, legM, 0.12, 0.2, 0.17, 0.5, 0.03);
  g.userData = { body, legs, ants };
  return g;
}

// a bug on the back wall: belly to the wall, head pointing along angle a (0 = straight down)
const wallBug = (o, x, y, a) => {
  const lx = new THREE.Vector3(Math.sin(a), -Math.cos(a), 0), ly = new THREE.Vector3(0, 0, 1), lz = new THREE.Vector3().crossVectors(lx, ly);
  o.setRotationFromMatrix(new THREE.Matrix4().makeBasis(lx, ly, lz)); o.position.set(x, y, WALLZ + 0.0015);
};

function makeCrack() {
  const g = new THREE.Group(), m = mat(0x4a3e34);
  const pts = [[0, 0.03], [0.006, 0.012], [-0.004, -0.004], [0.007, -0.02], [0.0, -0.034]];
  for (let k = 0; k + 1 < pts.length; k++) { const [a, b] = [pts[k], pts[k + 1]]; const len = Math.hypot(b[0] - a[0], b[1] - a[1]);
    const s = box(0.0008, len, 0.0008, m, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - len / 2, 0, false); s.rotation.z = Math.atan2(b[0] - a[0], -(b[1] - a[1])) * -1; g.add(s); }
  return g;
}
function makeCutaway() {   // a wall cutaway: dark cavity, two studs, pink insulation, the bug cluster goes on it
  const g = new THREE.Group();
  g.add(box(0.3, 0.26, 0.004, 0x2a2018, 0, -0.13, 0, false));
  g.add(box(0.03, 0.26, 0.01, 0xc89a62, -0.12, -0.13, 0.002), box(0.03, 0.26, 0.01, 0xc89a62, 0.12, -0.13, 0.002));
  for (let k = 0; k < 7; k++) { const p = mesh(ICO1, mat(0xe9a0b4)); p.scale.set(0.05, 0.03, 0.008); p.position.set(-0.07 + (k % 3) * 0.07, -0.21 + Math.floor(k / 3) * 0.06, 0.004); g.add(p); }
  const fr = 0xf4efe4; g.add(box(0.32, 0.015, 0.012, fr, 0, 0.0, 0.004), box(0.32, 0.015, 0.012, fr, 0, -0.27, 0.004), box(0.015, 0.28, 0.012, fr, -0.155, -0.135, 0.004), box(0.015, 0.28, 0.012, fr, 0.155, -0.135, 0.004));
  return g;
}

export function build(scene, S, K) {
  const { L, T_END, start, end, W, cut, popS, vis, place, ease, clamp01 } = K;
  const LOOP = L.length === 1;
  scene.add(makeLivingRoom());
  const cr = makeCrack(); cr.position.set(CRACK[0], CRACK[1], WALLZ + 0.001); scene.add(cr);
  S.cutaway = makeCutaway(); S.cutaway.position.set(CUT[0], CUT[1], WALLZ + 0.002); scene.add(S.cutaway);
  S.bug = makeStinkBug(); S.bug.scale.setScalar(BS); scene.add(S.bug);
  S.pack = []; for (let k = 0; k < 11; k++) { const b = makeStinkBug(); b.scale.setScalar(BS); scene.add(b); S.pack.push(b); }
  S.slip = P.makeSlipper(); S.slip.position.set(0, -0.06, 0); S.slip.rotation.z = Math.PI / 2; S.person.userData.hands[1].add(S.slip);
  S.wand = new THREE.Group(); { const tube = cyl(0.016, 0.016, 0.7, 0x9aa0a8, 10); tube.position.y = -0.35; S.wand.add(tube); const nz = box(0.12, 0.03, 0.05, 0x3a3e46, 0, -0.71, 0); S.wand.add(nz); }
  S.wand.position.set(0, -0.04, 0); S.wand.rotation.z = 0.3; S.person.userData.hands[1].add(S.wand);
  const cloudM = new THREE.MeshBasicMaterial({ color: 0x9ccc3a, transparent: true, opacity: 0.5, depthWrite: false });
  S.cloud = []; for (let k = 0; k < 9; k++) { const c = new THREE.Mesh(ICO1, cloudM); scene.add(c); S.cloud.push(c); }

  // the bug crawls out of the crack and down during line 0; returns to the crack for the loop
  const P0 = [CRACK[0] + 0.002, CRACK[1] - 0.012], P1 = [CRACK[0] + 0.006, CRACK[1] - 0.05];
  const tCrawl = LOOP ? T_END : cut(0, 5);
  const bugPos = (t) => { if (LOOP) return P0; if (t >= (L[8] ? start(8) : 1e9)) return P0; const u = ease(clamp01(t / tCrawl)); return [P0[0] + (P1[0] - P0[0]) * u, P0[1] + (P1[1] - P0[1]) * u]; };
  const bugAt = (t) => { const p = bugPos(t); return [p[0], p[1], WALLZ + 0.008]; };
  const B0 = bugAt(0), B1 = bugAt(tCrawl);
  const OPEN = { c0: [B0[0] + 0.03, B0[1] - 0.012, B0[2] + 0.066], l0: B0, c1: [B1[0] + 0.024, B1[1] - 0.008, B1[2] + 0.056], l1: B1, mv: tCrawl };
  const MBPOS = [0.36, -0.52, -Math.PI / 2 + 0.45], PPOS = [0.08, 1.15, Math.PI / 2];
  const mbAt = (S) => [S.mb.position.x, S.mb.position.y, S.mb.position.z];
  const PSHOT = { c0: [0.24, 1.36, -0.36], l0: [0.08, 1.72, 1.15], c1: [0.24, 1.37, -0.26], l1: [0.08, 1.74, 1.15] };
  const CUTT = [CUT[0], CUT[1] - 0.13, WALLZ];
  const cfg = L.map(() => ({ shots: [{}] }));
  const set = (i, o) => Object.assign(cfg[i], o);
  let home = T_END, out = T_END;
  if (!LOOP) {
    set(0, { shots: [{ ...OPEN }, { at: cut(0, 5) + 0.05, tgt: [0.22, 0.84, WALLZ], yaw: 80, dist: 0.7, h: 0.12, dyaw: 6, push: 0.88 }] });
    set(1, { cardWord: 4, mood: 'deadpan', shots: [{ tgt: (S) => [S.mb.position.x, S.mb.position.y, S.mb.position.z], yaw: 78, dist: 0.45, h: 0.05, dyaw: 6, push: 0.9 },
      { at: cut(1, 5), tgt: CUTT, yaw: 84, dist: 0.36, h: 0.02, dyaw: 8, push: 0.85 }] });
    set(2, { person: { pose: 'slipper', from: 'stand' }, shots: [{ ...PSHOT }] });
    set(3, { cardWord: 0, mood: 'alarm', shots: [{ tgt: [B1[0], B1[1], WALLZ], yaw: 70, dist: 0.2, h: 0.0, dyaw: 12, push: 0.85 }] });
    const VSHOT = { c0: [0.26, 1.3, -0.36], l0: [0.08, 1.32, 1.15], c1: [0.25, 1.31, -0.26], l1: [0.08, 1.36, 1.15] };
    set(4, { person: { pose: 'sign', from: 'stand' }, shots: [{ ...VSHOT }] });
    set(5, { cardWord: 0, mood: 'smug', person: { pose: 'sign', look: (t) => 0.5 * Math.sin((t - start(5)) * 6) }, shots: [{ ...VSHOT }] });
    set(6, { person: { pose: 'back', from: 'sign', look: (t) => 0.3 * Math.sin((t - start(6)) * 4) }, shots: [{ ...PSHOT }] });
    set(7, { cardWord: 0, mood: 'deadpan', mbPose: 'stop', shots: [{ tgt: (S) => [S.mb.position.x, S.mb.position.y, S.mb.position.z], yaw: 72, dist: 0.42, h: 0.04, dyaw: 6, push: 0.9 }] });
    home = T_END - 0.25; out = W(8, 4) - 0.05;
    set(8, { mood: 'smug', mbPose: 'hips', shots: [{ tgt: CUTT, yaw: 96, dist: 0.32, h: 0.03, dyaw: -8, push: 0.85 },
      { at: out, c0: [CUTT[0] + 0.02, CUTT[1] + 0.02, CUTT[2] + 0.3], l0: CUTT, c1: OPEN.c0, l1: OPEN.l0, mv: home - out }] });
    cfg[0].hideMb = 1;
  } else set(0, { hideMb: 1, shots: [{ c0: OPEN.c0, l0: OPEN.l0 }] });   // the loop camera is set in faceCam

  const PER = LOOP ? Math.round(T_END * 30) / 30 : T_END;   // micro-loop period = the exact rendered frame count
  const cyc = (n) => (n * TAU) / PER;
  let tNow = 0;
  function props(t, i) {
    tNow = t;
    const p = bugPos(t), moving = !LOOP && t < tCrawl;
    wallBug(S.bug, p[0], p[1], LOOP ? 0.22 * Math.sin(cyc(1) * t) : 0.12 + 0.08 * Math.sin(t * 2));
    Q.animateLegs(S.bug, LOOP ? (Math.round(2 * PER) / PER) * t : moving ? t * 2.6 : t * 0.4, LOOP ? 0.25 : moving ? 0.7 : 0.12);
    for (const a of S.bug.userData.ants) a.rotation.x = -0.1 + 0.15 * Math.sin(cyc(3) * t + a.userData.s);
    // the winter pack in the wall cutaway (line 1 "With friends" and line 8)
    const showPack = !LOOP && ((i === 1 && t >= cut(1, 5)) || i === 8);
    S.cutaway.visible = showPack;
    S.pack.forEach((b, k) => {
      b.visible = showPack; if (!showPack) return;
      const a = k * 2.399, r = 0.012 + 0.011 * Math.sqrt(k);
      wallBug(b, CUT[0] + Math.cos(a) * r * 1.3, CUT[1] - 0.13 + Math.sin(a) * r, a * 1.7);
      b.position.z = WALLZ + 0.008 + (k % 3) * 0.002; Q.animateLegs(b, t * 0.5 + k, 0.1);
    });
    // stink cloud: off the wall bug on "stinks" (line 3), off the vacuum nozzle on "stinks" (line 5)
    let src = null, t0 = 0;
    if (!LOOP && i === 3) { src = [B1[0], B1[1], WALLZ + 0.02]; t0 = W(3, 4) - 0.1; }
    if (!LOOP && i === 5) { const h = S.person.userData.hands[1].getWorldPosition(new THREE.Vector3()); src = [h.x + 0.05, h.y - 0.05, h.z - 0.25]; t0 = W(5, 3) - 0.1; }
    S.cloud.forEach((c, k) => {
      if (!src || t < t0) { c.visible = false; return; }
      c.visible = true; const d = t - t0, a = k * 0.7, sc = (i === 5 ? 0.09 : 0.03) * (0.4 + 0.6 * ease(d / 0.5)) * (0.7 + 0.3 * Math.sin(k * 3));
      c.position.set(src[0] + Math.cos(a) * sc * 0.9, src[1] + (k % 3) * sc * 0.5 + d * sc * 0.6, src[2] + Math.sin(a) * sc * 0.6 + sc * 0.4);
      c.scale.setScalar(sc); c.material.opacity = 0.45 * (1 - 0.4 * ease((d - 0.8) / 0.6));
    });
    S.slip.visible = !LOOP && i === 2 || (!LOOP && i === 3);
    S.wand.visible = !LOOP && (i === 4 || i === 5);
  }
  function faceCam(cam) {
    if (!LOOP) return;
    const ph = cyc(1) * tNow, B = bugAt(0), yaw = 1.25 + 0.32 * Math.sin(ph), d = 0.068 * (1 + 0.1 * Math.sin(2 * ph));
    cam.position.set(B[0] + Math.cos(yaw) * d, B[1] - 0.01 + 0.008 * Math.cos(ph), B[2] + Math.sin(yaw) * d);
    cam.lookAt(B[0], B[1], B[2] - 0.006);
  }
  const POSES = { ...P.PERSON_POSES };
  return { cfg, props, faceCam, POSES, pose0: 'stand', MB: 0.055, MBPOS, mbY: SILL, PPOS, mbIn: LOOP ? 1e9 : start(1), mbOut: LOOP ? null : home - 0.5 };
}
