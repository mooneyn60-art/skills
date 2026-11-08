// Episode: webbing clothes moth (YouTube Short ~15.8 s, 8 lines, loops) + micro-loop (KEY=loop, one line, ~7.2 s).
// NEW opening (research 68): frame 1 is already a macro on a golden clothes moth fluttering over a hole in a wool sweater.
// Same night bedroom as ep_bedbugs.js; the person sits up in bed. Beats: moth over the hole (hook) -> "It doesn't even eat"
// (it lands) -> "who made the holes?!" -> macro: white larvae chewing the knit, eggs pop -> the person hugs the sweater ->
// stink lines "It's sweaty" -> a bag + "FEW DAYS" freezer card -> "Or keep blaming the moth." cranes back to the opening.
// Sources: Univ. of Kentucky ENTFACT-609 (adults do not feed; 40-50 eggs; larvae eat the fabric), UC IPM Pest Notes 7435
// (soiled/sweaty fabric damaged more; freezer several days below 18 F; larvae shiny white with dark heads; gold adult).
import * as THREE from 'three';
import { mat, mesh, box, cyl, limbGeo, texMat, canvasTex, ICO, ICO1 } from './lib.js';
import * as P from './props.js';
import * as Q from './props2.js';
import { makeBedroom, LIGHT as BL } from './ep_bedbugs.js';

export const SHIRT = 0x4f6fa0;
export const LIGHT = BL;

const MT = 0.55;
const MS = 0.008;                 // webbing clothes moth ~7-8 mm body
const LS = 0.01;                  // full-grown larva ~1 cm
const SW = [-0.36, 0.34];         // sweater centre on the sheet
const TAU = Math.PI * 2;

function knitTex() {
  return canvasTex(128, 128, (c, w) => {
    c.fillStyle = '#7e2a36'; c.fillRect(0, 0, w, w);
    c.strokeStyle = '#a23a4a'; c.lineWidth = 3;
    for (let y = 4; y < w; y += 10) for (let x = 0; x < w; x += 10) { c.beginPath(); c.moveTo(x, y); c.lineTo(x + 5, y + 6); c.lineTo(x + 10, y); c.stroke(); }
    c.fillStyle = '#5e1e28'; for (let y = 0; y < w; y += 20) c.fillRect(0, y, w, 1);
  }, [3, 3]);
}
function makeSweater(holes = true) {
  const g = new THREE.Group(), m = texMat(knitTex());
  const b = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.012, 0.26), m); b.position.y = 0.006; b.castShadow = true; b.receiveShadow = true; g.add(b);
  for (const s of [-1, 1]) { const sl = new THREE.Mesh(new THREE.BoxGeometry(0.075, 0.01, 0.18), m); sl.position.set(0.05, 0.005, s * 0.2); sl.rotation.y = s * 0.35; sl.castShadow = true; g.add(sl); }
  const rib = box(0.03, 0.013, 0.26, 0x6a2230, -0.12, 0, 0, false); g.add(rib);
  const neck = mesh(new THREE.TorusGeometry(0.04, 0.008, 4, 14), mat(0x6a2230)); neck.rotation.x = Math.PI / 2; neck.position.set(0.11, 0.012, 0); g.add(neck);
  if (holes) for (const [x, z, r] of [[0.03, 0.02, 0.0055], [-0.04, -0.05, 0.005], [0.0, 0.08, 0.004], [-0.07, 0.06, 0.0035]]) { const h = cyl(r, r * 0.9, 0.0008, 0xb8c6d6, 9); h.position.set(x, 0.0122, z); g.add(h);
    for (let k = 0; k < 9; k++) { const a = k * 0.7, f = box(0.0007, 0.0006, 0.0014, 0x9a3446, x + Math.cos(a) * r, 0.0125, z + Math.sin(a) * r, false); f.rotation.y = -a; g.add(f); } }
  return g;
}

// webbing clothes moth: golden, narrow wings folded flat/roof-like at rest, reddish-gold head tuft, long antennae
export function makeMoth() {
  const g = new THREE.Group(), body = new THREE.Group(); g.add(body);
  const gold = mat(0xc9a35a), dk = mat(0x8a6a3a);
  const bd = mesh(ICO1, gold); bd.scale.set(0.34, 0.08, 0.08); bd.position.set(-0.05, 0.12, 0); body.add(bd);
  const hd = mesh(ICO1, gold); hd.scale.set(0.07, 0.07, 0.07); hd.position.set(0.3, 0.13, 0); body.add(hd);
  const tuft = mesh(ICO1, mat(0xd2763a)); tuft.scale.set(0.06, 0.05, 0.06); tuft.position.set(0.3, 0.19, 0); body.add(tuft);
  for (const s of [-1, 1]) { const e = mesh(ICO1, mat(0x2a1a10), false); e.scale.setScalar(0.03); e.position.set(0.34, 0.14, s * 0.05); body.add(e); }
  const ants = [-1, 1].map((s) => { const a = new THREE.Group(); a.position.set(0.34, 0.17, s * 0.03); a.rotation.order = 'YXZ'; a.rotation.y = -Math.PI / 2 + s * 0.35; a.rotation.x = -0.35; a.add(mesh(limbGeo(0.008, 0.004, 0.55, 3), dk, false)); a.userData.s = s; body.add(a); return a; });
  const wm = mat(0xd6b46a, { side: THREE.DoubleSide });
  const wings = [-1, 1].map((s) => { const w = new THREE.Group(); w.position.set(0.18, 0.17, s * 0.02); const p = mesh(ICO1, wm, false); p.scale.set(0.42, 0.006, 0.09); p.position.set(-0.36, 0, s * 0.08); w.add(p);
    const fr = mesh(ICO1, mat(0xe8cc8a, { side: THREE.DoubleSide }), false); fr.scale.set(0.12, 0.004, 0.06); fr.position.set(-0.74, 0, s * 0.1); w.add(fr); body.add(w); return w; });
  for (const s of [-1, 1]) for (let k = 0; k < 3; k++) { const l = mesh(limbGeo(0.012, 0.008, 0.2, 3), dk, false); l.position.set(0.15 - k * 0.08, 0.08, s * 0.05); l.rotation.set(s * 0.9, 0, 0); body.add(l); }
  g.userData = { body, wings, ants };
  return g;
}
// rest: wings folded back roof-like; fly: spread + flapping (ph in radians)
function poseMoth(m, ph, flying) {
  m.userData.wings.forEach((w, k) => { const s = k ? 1 : -1;
    if (flying) { w.rotation.set(s * (0.2 + 0.9 * Math.sin(ph)), s * -0.9, 0); }
    else { w.rotation.set(s * 0.32, s * 0.08, 0); } });
  m.userData.ants.forEach((a) => { a.rotation.x = -0.35 + 0.1 * Math.sin(ph * 0.25 + a.userData.s); });
}
// larva: shiny white segments, dark head capsule; wiggle along the body
function makeLarva() {
  const g = new THREE.Group(), segs = [];
  for (let k = 0; k < 9; k++) { const s = mesh(ICO1, mat(0xf3efe4, { flatShading: false }), false); const r = 0.075 - Math.abs(k - 3) * 0.006; s.scale.set(0.07, r, r); s.position.set(0.4 - k * 0.1, r, 0); g.add(s); segs.push(s); }
  const hd = mesh(ICO1, mat(0x4a2e1a), false); hd.scale.set(0.06, 0.055, 0.06); hd.position.set(0.48, 0.06, 0); g.add(hd);
  g.userData = { segs, hd };
  return g;
}
function wiggleLarva(l, ph, amp = 1) { l.userData.segs.forEach((s, k) => { s.position.z = amp * 0.03 * Math.sin(ph - k * 0.8); }); l.userData.hd.position.y = 0.06 + amp * 0.02 * Math.max(0, Math.sin(ph * 2)); }

export function build(scene, S, K) {
  const { L, T_END, start, end, W, cut, popS, vis, place, ease, clamp01 } = K;
  const LOOP = L.length === 1;
  scene.add(makeBedroom());
  S.sw = makeSweater(); S.sw.position.set(SW[0], MT + 0.003, SW[1]); S.sw.rotation.y = 0.25; scene.add(S.sw); S.sw.updateMatrixWorld(true);
  const onSw = (x, z, dy = 0) => { const v = new THREE.Vector3(x, 0.0125 + dy, z).applyMatrix4(S.sw.matrixWorld); return [v.x, v.y, v.z]; };
  const HOLE = onSw(0.03, 0.02);
  S.moth = makeMoth(); S.moth.scale.setScalar(MS); scene.add(S.moth);
  S.larvae = [[0.042, 0.02, 2.6], [0.03, 0.034, 1.4], [0.016, 0.012, -0.5], [-0.032, -0.05, 0.9]].map(([x, z, h]) => { const l = makeLarva(); l.scale.setScalar(LS); const p = onSw(x, z, -0.001); l.position.set(p[0], p[1], p[2]); l.rotation.y = h; scene.add(l); return l; });
  S.eggs = []; for (let k = 0; k < 40; k++) { const e = Q.makeBugEgg(); scene.add(e); S.eggs.push(e); }
  S.cal = Q.makeCal('IN THE FREEZER', 'FEW DAYS'); scene.add(S.cal);
  const bagM = new THREE.MeshLambertMaterial({ color: 0xdfeef8, transparent: true, opacity: 0.35, depthWrite: false });
  S.bag = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.05, 0.5), bagM); S.bag.position.set(SW[0], MT + 0.026, SW[1]); S.bag.rotation.y = 0.25; scene.add(S.bag);
  const zip = box(0.345, 0.004, 0.012, 0x3a7ac8, 0, 0.025, 0.245, false); S.bag.add(zip);
  const stinkM = new THREE.MeshBasicMaterial({ color: 0xb6d24a, transparent: true, opacity: 0.85 });
  S.stink = [-0.06, 0.0, 0.06].map((dz, k) => { const pts = []; for (let j = 0; j < 12; j++) pts.push(new THREE.Vector3(0.012 * Math.sin(j * 1.1 + k), j * 0.012, 0)); const m = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 24, 0.0025, 5), stinkM); const p = onSw(0.0, dz, 0.004); m.position.set(p[0], p[1], p[2]); scene.add(m); return m; });
  // hugged sweater (line 4)
  S.hugSw = makeSweater(false); S.hugSw.scale.setScalar(0.8); S.hugSw.rotation.set(0, 0, Math.PI / 2); S.hugSw.position.set(0.2, 0.32, 0); S.person.userData.chest.add(S.hugSw);

  const POSES = { ...P.PERSON_POSES,
    bed: { py: 0.1, lean: 0.22, hip: [1.5, 1.5], knee: [0, 0], shz: [0.25, 0.55], elz: [0.3, 1.05], shx: [0, 0.15], elx: [0, 0] },
    shrug: { py: 0.1, lean: 0.05, hip: [1.5, 1.5], knee: [0, 0], shz: [0.6, 0.55], elz: [1.4, 1.05], shx: [0.5, 0.15], elx: [0, 0] },
    hug: { py: 0.1, lean: -0.12, hip: [1.5, 1.5], knee: [0, 0], shz: [1.15, 1.15], elz: [1.1, 1.1], shx: [-0.55, -0.55], elx: [0, 0] },
  };
  const PPOS = [-0.62, 0.0, 0], MBPOS = [-0.3, -0.36, -Math.PI / 2];
  const pHead = (S) => S.person.userData.head.getWorldPosition(new THREE.Vector3()).toArray();
  const mbAt = (S) => [S.mb.position.x, S.mb.position.y, S.mb.position.z];
  const HOV = [HOLE[0], HOLE[1] + 0.013, HOLE[2]];
  const OPEN = { c0: [HOV[0] + 0.018, HOV[1] + 0.006, HOV[2] + 0.017], l0: [HOV[0], HOV[1] - 0.003, HOV[2]],
    c1: [HOV[0] + 0.015, HOV[1] + 0.005, HOV[2] + 0.014], l1: [HOV[0], HOV[1] - 0.003, HOV[2]], mv: 1.9 };
  const SWT = [SW[0], MT + 0.02, SW[1]];
  const cfg = L.map(() => ({ shots: [{}] }));
  const set = (i, o) => Object.assign(cfg[i], o);
  let home = T_END, out = T_END, tLand = 1e9;
  if (!LOOP) {
    tLand = W(1, 3);
    set(0, { shots: [{ ...OPEN }, { at: cut(0, 5) + 0.02, tgt: SWT, yaw: 60, dist: 0.5, h: 0.32, dyaw: 10, push: 0.88 }] });
    set(1, { cardWord: 3, mood: 'deadpan', shots: [{ tgt: mbAt, yaw: 96, dist: 0.5, h: 0.06, dyaw: 6, push: 0.9 },
      { at: cut(1, 3), tgt: () => [LAND[0], LAND[1] + 0.002, LAND[2]], yaw: 55, dist: 0.035, h: 0.014, dyaw: 12, push: 0.85 }] });
    set(2, { person: { pose: 'shrug', from: 'bed' }, shots: [{ tgt: pHead, yaw: 8, dist: 1.9, h: -0.15, ly: -0.3, dyaw: 6, push: 0.92 }] });
    set(3, { cardWord: 0, mood: 'smug', shots: [{ tgt: [HOLE[0] + 0.005, HOLE[1], HOLE[2]], yaw: 30, dist: 0.065, h: 0.04, dyaw: 22, push: 0.82 }] });
    set(4, { person: { pose: 'hug', from: 'bed', look: (t) => 0.35 * Math.sin((t - start(4)) * 6) }, shots: [{ tgt: pHead, yaw: 14, dist: 1.6, h: -0.1, ly: -0.25, dyaw: -6, push: 0.9 }] });
    set(5, { cardWord: 1, mood: 'smug', mbPose: 'hips', shots: [{ tgt: SWT, yaw: 70, dist: 0.34, h: 0.12, dyaw: 8, push: 0.9 }] });
    set(6, { cardWord: 0, mood: 'deadpan', mbPose: 'point', shots: [{ tgt: [SW[0] - 0.03, MT + 0.05, SW[1] + 0.05], yaw: 112, dist: 0.6, h: 0.22, dyaw: 8, push: 0.92 }] });
    home = T_END - 0.25; out = W(7, 4) - 0.05;
    set(7, { mood: 'smug', mbPose: 'hips', shots: [{ tgt: mbAt, yaw: 96, dist: 0.45, h: 0.05, dyaw: 4, push: 0.9 },
      { at: out, c0: [MBPOS[0] - 0.03, MT + 0.2, MBPOS[1] + 0.42], l0: [MBPOS[0], MT + 0.1, MBPOS[1]], c1: OPEN.c0, l1: OPEN.l0, mv: home - out }] });
    cfg[0].hideMb = 1;
  } else set(0, { hideMb: 1, shots: [{ c0: OPEN.c0, l0: OPEN.l0 }] });   // the loop camera is set in faceCam

  const cyc = (n) => (n * TAU) / T_END;
  const LAND = onSw(0.045, 0.0, 0.0);
  let tNow = 0;
  function props(t, i) {
    tNow = t;
    // moth: hovers over the hole (t < tLand), lands beside it, takes off again for the loop
    const fl = (Math.round(14 * T_END) / T_END) * TAU * t;
    let p, flying = true, h = 2.2 + 0.3 * Math.sin(cyc(1) * t);
    const hover = (tt) => [HOV[0] + 0.004 * Math.cos(cyc(1) * tt), HOV[1] + 0.002 * Math.sin(cyc(2) * tt), HOV[2] + 0.004 * Math.sin(cyc(1) * tt)];
    if (t < tLand) p = hover(t);
    else if (t < tLand + 0.4) { const u = ease((t - tLand) / 0.4), a = hover(tLand); p = [a[0] + (LAND[0] - a[0]) * u, a[1] + (LAND[1] - a[1]) * u, a[2] + (LAND[2] - a[2]) * u]; }
    else if (t < out) { p = LAND; flying = false; h = 2.0; }
    else { const u = ease(clamp01((t - out) / (home - out))), a = hover(T_END); p = [LAND[0] + (a[0] - LAND[0]) * u, LAND[1] + (a[1] - LAND[1]) * u, LAND[2] + (a[2] - LAND[2]) * u]; }
    S.moth.position.set(p[0], p[1], p[2]); S.moth.rotation.set(0, h, flying ? 0.15 : 0); poseMoth(S.moth, fl, flying);
    // larvae chew at the hole edges: shown in the loop and from line 3 on (hidden on the opening so the hook is the moth)
    const showL = LOOP || i >= 3;
    S.larvae.forEach((l, k) => { l.visible = showL; wiggleLarva(l, (Math.round(3 * T_END) / T_END) * TAU * t + k * 1.3, 1); });
    // eggs pop on "40" (line 3)
    const te = LOOP ? 1e9 : W(3, 5) - 0.1;
    S.eggs.forEach((e, k) => {
      if (!vis(e, te + k * 0.01, LOOP ? 0 : end(6), t)) return;
      const a = k * 2.399, r = 0.004 + 0.0022 * Math.sqrt(k), q = onSw(0.012 + Math.cos(a) * r, -0.004 + Math.sin(a) * r, -0.0005);
      e.position.set(q[0], q[1], q[2]); e.scale.setScalar(Math.max(0.0001, popS(t, te + k * 0.01, 0.0018, 0.18)));
    });
    // stink lines (line 5), bag (line 6), freezer card (line 6)
    S.stink.forEach((m, k) => { m.visible = !LOOP && i === 5 && t > W(5, 1) - 0.1; if (m.visible) { m.scale.set(1, 0.6 + 0.4 * Math.sin(t * 5 + k), 1); m.rotation.y = 0.4 * Math.sin(t * 3 + k); } });
    if (vis(S.bag, LOOP ? 1e9 : W(6, 0) - 0.06, LOOP ? 0 : end(6), t)) S.bag.scale.setScalar(popS(t, W(6, 0) - 0.06, 1));
    if (!LOOP && vis(S.cal, W(6, 2) - 0.06, end(6), t)) { S.cal.position.set(SW[0] + 0.1, MT + 0.012, SW[1] - 0.17); S.cal.scale.setScalar(popS(t, W(6, 2) - 0.06, 1.25)); }
    else S.cal.visible = false;
    S.hugSw.visible = !LOOP && i === 4;
  }
  function faceCam(cam) {
    if (S.cal.visible) S.cal.lookAt(cam.position.x, S.cal.position.y, cam.position.z);
    if (!LOOP) return;
    const ph = cyc(1) * tNow, yaw = 0.75 + 0.5 * Math.sin(ph), d = 0.03 * (1 + 0.1 * Math.sin(2 * ph));
    cam.position.set(HOLE[0] + Math.cos(yaw) * d, HOLE[1] + 0.02 + 0.004 * Math.cos(ph), HOLE[2] + Math.sin(yaw) * d);
    cam.lookAt(HOLE[0], HOLE[1] + 0.008, HOLE[2]);
  }
  return { cfg, props, faceCam, POSES, pose0: 'bed', personY: MT - 0.02, MB: 0.07, MBPOS, mbY: MT, PPOS, mbIn: LOOP ? 1e9 : start(1), mbOut: LOOP ? null : home - 0.5 };
}
