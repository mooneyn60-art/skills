// Episode: silverfish (YouTube Short, 10 lines, ~19.7 s, loops). Meatball's guest bedroom at night (makeBedroom from
// ep_bedbugs.js); the person reads in bed with an open book on the blanket. Real-size silverfish (body ~1.2 cm).
// Beats: a silverfish grazing a nibbled page (hook) -> "Lights on!": overhead light snaps on, it darts into the book's
// gutter -> Meatball smug + the silverfish peeking out of the binding -> glue / paper / cereal -> "MONTHS" calendar ->
// a toy dinosaur pops behind it, Meatball sips -> "Read it a bedtime story." cranes back to the opening framing.
import * as THREE from 'three';
import { mat, mesh, box, cyl, limbGeo, canvasTex, ICO, ICO1 } from './lib.js';
import * as P from './props.js';
import * as Q from './props2.js';
import { makeBedroom } from './ep_bedbugs.js';

export const SHIRT = 0x4f7fb0;
export const LIGHT = { bg: 0x0e1426, hemi: [0xc2d0ff, 0x5a4a40, 1.0], sun: [0xc8d6ff, 1.3], sunPos: [1.6, 3.0, 1.8], sunTgt: [0, 0.5, 0],
  lamps: [[0xffcf8a, 2.0, [-0.85, 1.0, 1.05]], [0xffe6c4, 0.6, [0.6, 2.3, 0.6]]] };

const MT = 0.55;                  // mattress top (makeBedroom)
const YB = 0.75;                  // blanket top
const YP = YB + 0.016;            // page top
const SF = 0.014;                 // silverfish: body ~1.2 cm (UC IPM: up to 1/2 inch)
const BK = [0.12, 0.1];           // open book centre (x, z); spine along x, the page top faces +x (away from the reader)
const PW = 0.15, PH = 0.23;       // one page: 15 cm wide (z), 23 cm tall (x)
const pg = (u, v) => [BK[0] + PH / 2 - PH * v, BK[1] - PW + 2 * PW * u];   // spread texture (u, v) -> world (x, z)
const BITE = pg(0.86, 0.74);
const HOME = [BITE[0] - 0.002, BITE[1] - 0.012, -Math.PI / 2];              // head on the bite, facing +z
const GUT = BK[1];
const TOPX = BK[0] + PH / 2;
const SPREAD = [0.04, 0.43];
const GLUE = [SPREAD[0] + 0.03, SPREAD[1] - 0.05], PAPER = [SPREAD[0] - 0.02, SPREAD[1] + 0.01], CEREAL = [SPREAD[0] + 0.035, SPREAD[1] + 0.06];
const CALP = [0.03, 0.33];
const DINO = [BITE[0] + 0.04, BITE[1] + 0.03];

// silverfish: carrot-shaped, silvery scales, long antennae, three tail filaments. 1 unit long, faces +x, stands on y = 0.
function makeSilverfish() {
  const g = new THREE.Group();
  const silver = new THREE.MeshPhongMaterial({ color: 0xaeb9c2, specular: 0xffffff, shininess: 70, flatShading: true });
  const dark = new THREE.MeshPhongMaterial({ color: 0x6d7983, specular: 0xbfcad3, shininess: 40, flatShading: true });
  const app = mat(0x5a646c);
  const segs = [];
  const N = 11;
  for (let k = 0; k < N; k++) {
    const u = k / (N - 1), w = 0.2 * (k < 3 ? 1 - 0.04 * (2 - k) : Math.pow(1 - (u - 0.2) / 0.8, 0.9) * 0.78 + 0.22 * (1 - u) + 0.03);
    const s = mesh(ICO1, k % 2 ? silver : dark); s.scale.set(0.078, 0.045 * (1 - 0.5 * u), w / 2);
    s.position.set(0.38 - k * 0.08, 0.05, 0); g.add(s); segs.push(s);
  }
  const head = mesh(ICO1, dark); head.scale.set(0.06, 0.04, 0.075); head.position.set(0.46, 0.05, 0); g.add(head);
  for (const s of [-1, 1]) { const e = mesh(ICO, mat(0x15181b), false); e.scale.setScalar(0.018); e.position.set(0.48, 0.07, s * 0.05); g.add(e); }
  const ants = [];
  for (const s of [-1, 1]) {
    const a = new THREE.Group(); a.position.set(0.5, 0.06, s * 0.025); a.rotation.y = Math.PI / 2 - s * 0.38;
    const m = mesh(limbGeo(0.01, 0.003, 0.8, 3), app, false); m.rotation.x = -0.18; a.add(m); g.add(a); ants.push({ a, s });
  }
  const tail = new THREE.Group(); tail.position.set(0.38 - (N - 1) * 0.08 - 0.02, 0.045, 0); g.add(tail);
  for (const a of [-0.42, 0, 0.42]) { const c = mesh(limbGeo(0.01, 0.003, 0.5, 3), app, false); c.rotation.set(-0.08, -Math.PI / 2 + a, 0, 'YXZ'); tail.add(c); }
  const legs = [];
  for (const s of [-1, 1]) for (let k = 0; k < 3; k++) {
    const h = new THREE.Group(); h.position.set(0.33 - k * 0.09, 0.035, s * 0.07); g.add(h);
    const m = mesh(limbGeo(0.012, 0.006, 0.17, 3), app, false); m.rotation.x = 0.55; h.add(m);
    legs.push({ h, s, k });
  }
  g.userData = { segs, ants, tail, legs, head };
  return g;
}
// run (amp 1): fish-like body wave + scurrying legs; idle (amp ~0.1): breathing + antenna sway
function wiggle(sf, t, amp, nib = 0) {
  const { segs, ants, tail, legs, head } = sf.userData, ph = t * (amp > 0.5 ? 26 : 3);
  segs.forEach((s, k) => { s.position.z = amp * 0.035 * Math.sin(ph - k * 0.75) * (0.25 + k / 10); });
  tail.position.z = segs[segs.length - 1].position.z; tail.rotation.y = amp * 0.4 * Math.sin(ph - 8.5);
  head.position.x = 0.46 + nib * 0.02 * Math.max(0, Math.sin(t * 16));
  ants.forEach(({ a, s }) => { a.rotation.y = Math.PI / 2 - s * (0.38 + 0.12 * Math.sin(t * 5 + s)) + amp * 0.2 * Math.sin(ph); });
  legs.forEach(({ h, s, k }) => { h.rotation.y = (s > 0 ? 0 : Math.PI) + s * ((k - 1) * -0.6 + amp * 0.5 * Math.sin(ph * 1.3 + (k + (s > 0)) % 2 * Math.PI)); });
}

function makeBook() {
  const g = new THREE.Group();
  const tex = canvasTex(1024, 784, (c, w, h) => {
    c.fillStyle = '#f3ead2'; c.fillRect(0, 0, w, h);
    c.fillStyle = '#4a4238';
    for (const x0 of [60, w / 2 + 50]) {
      c.font = '700 30px Lora'; c.fillText(x0 < w / 2 ? 'Chapter Seven' : '', x0, 80);
      for (let y = 120; y < h - 50; y += 17) { const len = 390 - (y > h - 100 && x0 > w / 2 ? 160 : (y * 7 + x0) % 23); let x = x0; while (x < x0 + len) { const wl = 12 + ((x * 13 + y * 7) % 41); c.fillRect(x, y, Math.min(wl, x0 + len - x), 5); x += wl + 6; } }
    }
    const gr = c.createLinearGradient(w / 2 - 50, 0, w / 2 + 50, 0);
    gr.addColorStop(0, 'rgba(60,45,25,0)'); gr.addColorStop(0.5, 'rgba(60,45,25,0.55)'); gr.addColorStop(1, 'rgba(60,45,25,0)');
    c.fillStyle = gr; c.fillRect(w / 2 - 50, 0, 100, h);
    // the grazing damage: an irregular scraped patch with a ragged hole at the right page's lower outer corner
    const bx = 0.86 * w, by = 0.74 * h;
    c.fillStyle = '#e2d4b0'; c.beginPath(); for (let k = 0; k <= 40; k++) { const a = k / 40 * 2 * Math.PI, r = 62 + 8 * Math.sin(k * 2.7) + 5 * Math.cos(k * 5.1); c.lineTo(bx + r * Math.cos(a) * 1.3, by + r * Math.sin(a)); } c.fill();
    c.fillStyle = '#5c4a30'; c.beginPath(); for (let k = 0; k <= 30; k++) { const a = k / 30 * 2 * Math.PI, r = 26 + 5 * Math.sin(k * 3.3) + 3 * Math.cos(k * 7.1); c.lineTo(bx + 10 + r * Math.cos(a) * 1.4, by + 6 + r * Math.sin(a)); } c.fill();
    c.fillStyle = 'rgba(40,30,20,0.35)'; for (let k = 0; k < 14; k++) c.fillRect(bx - 90 + (k * 37) % 170, by - 50 + (k * 23) % 100, 4, 4);
  });
  const page = new THREE.Mesh(new THREE.PlaneGeometry(2 * PW, PH), new THREE.MeshLambertMaterial({ map: tex })); page.receiveShadow = true;
  page.rotation.set(-Math.PI / 2, 0, -Math.PI / 2); page.position.set(BK[0], YP + 0.0004, BK[1]); g.add(page);
  const pm = mat(0xf6efdc);
  g.add(box(PH, 0.012, PW - 0.003, pm, BK[0], YB + 0.004, BK[1] - PW / 2 - 0.0015), box(PH, 0.012, PW - 0.003, pm, BK[0], YB + 0.004, BK[1] + PW / 2 + 0.0015));
  g.add(box(PH + 0.016, 0.004, 2 * PW + 0.02, mat(0x2e4a6a), BK[0], YB, BK[1]));
  return g;
}
function makeCereal() {
  const g = new THREE.Group(), m = mat(0xe0a548), geo = new THREE.TorusGeometry(0.0065, 0.003, 5, 9);
  for (let k = 0; k < 8; k++) { const r = mesh(geo, m); r.rotation.set(Math.PI / 2 + 0.3 * Math.sin(k), 0, k); r.position.set(0.022 * Math.sin(k * 2.4), 0.003, 0.02 * Math.cos(k * 1.9)); g.add(r); }
  return g;
}
function makePaperScrap() {
  const tex = canvasTex(256, 180, (c, w, h) => { c.fillStyle = '#ece8dc'; c.fillRect(0, 0, w, h); c.fillStyle = '#333'; c.fillRect(12, 10, 150, 18); c.fillStyle = '#6a6a6a'; for (let y = 40; y < h - 6; y += 12) for (let x = 12; x < w; x += 82) c.fillRect(x, y, 66 - ((x + y) % 11), 5); });
  const m = new THREE.Mesh(new THREE.PlaneGeometry(0.08, 0.056), new THREE.MeshLambertMaterial({ map: tex })); m.rotation.x = -Math.PI / 2; m.position.y = 0.0012; m.receiveShadow = true;
  const g = new THREE.Group(); g.add(m); return g;
}
function makeDino() {   // a little green toy dinosaur, faces +x
  const g = new THREE.Group(), m = mat(0x5aa14e), d = mat(0x3f7a38);
  const b = mesh(ICO1, m); b.scale.set(0.024, 0.017, 0.013); b.position.set(0, 0.036, 0); g.add(b);
  const n = mesh(ICO1, m); n.scale.set(0.009, 0.014, 0.008); n.position.set(0.02, 0.054, 0); n.rotation.z = -0.5; g.add(n);
  const h = mesh(ICO1, m); h.scale.set(0.015, 0.009, 0.009); h.position.set(0.032, 0.066, 0); g.add(h);
  for (const s of [-1, 1]) { const e = mesh(ICO, mat(0x111111), false); e.scale.setScalar(0.0022); e.position.set(0.038, 0.071, s * 0.006); g.add(e); }
  const t = mesh(new THREE.ConeGeometry(0.011, 0.05, 6), m); t.rotation.z = Math.PI / 2 + 0.25; t.position.set(-0.042, 0.03, 0); g.add(t);
  for (const s of [-1, 1]) { g.add(box(0.008, 0.024, 0.007, d, 0.002, 0, s * 0.008)); const a = box(0.003, 0.009, 0.003, d, 0.02, 0.03, s * 0.009); a.rotation.z = 0.8; g.add(a); }
  for (let k = 0; k < 4; k++) { const sp = mesh(new THREE.ConeGeometry(0.003, 0.007, 4), mat(0xe8c040)); sp.position.set(0.012 - k * 0.012, 0.054 - k * 0.002, 0); g.add(sp); }
  return g;
}

// piecewise path: keys [[t, x, z, h], ...] -> [x, z, h, moving]
function path(t, keys) {
  if (t <= keys[0][0]) return [...keys[0].slice(1), 0];
  for (let k = 0; k + 1 < keys.length; k++) {
    const [a, b] = [keys[k], keys[k + 1]];
    if (t < b[0]) { const u = (t - a[0]) / (b[0] - a[0]); const mv = Math.hypot(b[1] - a[1], b[2] - a[2]) > 1e-4 ? 1 : 0; return [a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u, a[3] + (b[3] - a[3]) * u, mv]; }
  }
  return [...keys[keys.length - 1].slice(1), 0];
}
const hd = (a, b) => Math.atan2(-(b[1] - a[1]), b[0] - a[0]);

export function build(scene, S, K) {
  const { L, T_END, start, end, W, cut, popS, vis, place, ease, clamp01 } = K;
  scene.add(makeBedroom());
  scene.add(makeBook());
  S.sf = makeSilverfish(); S.sf.scale.setScalar(SF); scene.add(S.sf);
  S.glue = Q.makeGlue(); S.paper = makePaperScrap(); S.cereal = makeCereal(); S.dino = makeDino();
  S.cal = Q.makeCal('NO FOOD FOR', 'MONTHS'); scene.add(S.glue, S.paper, S.cereal, S.dino, S.cal);
  S.mug = Q.makeMug(); S.mb.userData.arms[1].el.add(S.mug);
  S.ceil = new THREE.PointLight(0xfff1d8, 0, 6, 1.2); S.ceil.position.set(0.3, 2.3, 0.3); scene.add(S.ceil);
  const bulb = mesh(new THREE.CylinderGeometry(0.14, 0.18, 0.05, 14), new THREE.MeshLambertMaterial({ color: 0xf4efe4, emissive: 0x000000 }), false);
  bulb.position.set(0.3, 2.475, 0.3); scene.add(bulb); S.bulb = bulb;

  const POSES = { ...P.PERSON_POSES,
    bed: { py: 0.1, lean: 0.22, hip: [1.5, 1.5], knee: [0, 0], shz: [0.25, 0.55], elz: [0.3, 1.05], shx: [0, 0.15], elx: [0, 0] },
    shrug: { py: 0.1, lean: 0.05, hip: [1.5, 1.5], knee: [0, 0], shz: [0.6, 0.55], elz: [1.4, 1.05], shx: [0.5, 0.15], elx: [0, 0] },
    fist: { py: 0.1, lean: 0.0, hip: [1.5, 1.5], knee: [0, 0], shz: [0.25, 2.6], elz: [0.3, 0.9], shx: [0, 0], elx: [0, 0] },
    gasp: { py: 0.1, lean: -0.12, hip: [1.5, 1.5], knee: [0, 0], shz: [0.9, 0.9], elz: [1.9, 1.9], shx: [0.2, 0.2], elx: [0, 0] },
  };
  const PPOS = [-0.55, 0.12, 0], MBPOS = [-0.8, 1.02, -0.6];
  const pHead = (S) => S.person.userData.head.getWorldPosition(new THREE.Vector3()).toArray();
  const mbAt = (S) => [S.mb.position.x, S.mb.position.y, S.mb.position.z];
  const sfAt = (S) => [S.sf.position.x, S.sf.position.y + 0.002, S.sf.position.z];
  const H3 = [HOME[0], YP + 0.002, HOME[1]];
  const OPEN = { c0: [H3[0] - 0.045, H3[1] + 0.05, H3[2] + 0.075], l0: [H3[0] + 0.005, H3[1] - 0.035, H3[2] - 0.01],
    c1: [H3[0] - 0.035, H3[1] + 0.035, H3[2] + 0.045], l1: [H3[0], H3[1] - 0.018, H3[2] + 0.002], mv: 1.4 };
  const cfg = L.map(() => ({ shots: [{}] }));
  const set = (i, o) => Object.assign(cfg[i], o);
  const tOn = W(1, 0) + 0.05, tDark = start(4);

  set(0, { cardWord: 4, shots: [{ ...OPEN }, { at: cut(0, 4), tgt: [H3[0], H3[1], H3[2] + 0.004], yaw: 150, dist: 0.055, h: 0.03, ly: -0.014, dyaw: 14, push: 0.85 }] });
  set(1, { person: { pose: 'gasp', from: 'bed' }, shots: [{ tgt: [BK[0] - 0.01, YP, BK[1] + 0.06], yaw: 158, dist: 0.36, h: 0.3, dyaw: 6, push: 0.93, shake: { t: tOn, a: 0.01 } },
    { at: cut(1, 2), tgt: [BITE[0] - 0.005, YP, (BITE[1] + GUT) / 2], yaw: 165, dist: 0.13, h: 0.075, dyaw: 10, push: 0.85 }] });
  set(2, { cardWord: 2, mood: 'smug', mbPose: 'hips', shots: [{ tgt: mbAt, yaw: -20, dist: 0.5, h: 0.05, dyaw: 8, push: 0.9 },
    { at: cut(2, 3), tgt: [TOPX + 0.004, YB + 0.008, GUT], yaw: 25, dist: 0.065, h: 0.022, dyaw: -12, push: 0.88 }] });
  set(3, { person: { pose: 'shrug', from: 'bed', look: (t) => 0.3 * Math.sin((t - start(3)) * 5) }, shots: [{ tgt: pHead, yaw: 8, dist: 1.9, h: -0.15, ly: -0.3, dyaw: 6, push: 0.92 }] });
  set(4, { cardWord: 0, shots: [{ tgt: [SPREAD[0] + 0.02, YB + 0.035, SPREAD[1] - 0.015], yaw: 202, dist: 0.42, h: 0.2, dyaw: -10, push: 0.8 }] });
  set(5, { person: { pose: 'fist', from: 'bed' }, shots: [{ tgt: pHead, yaw: 4, dist: 2.1, h: -0.1, ly: -0.12, dyaw: 6, push: 0.92 }] });
  set(6, { cardWord: 2, shots: [{ tgt: [CALP[0] - 0.03, YB + 0.012, CALP[1] - 0.005], yaw: 192, dist: 0.15, h: 0.04, dyaw: 10, push: 0.85 }] });
  set(7, { person: { pose: 'shrug', from: 'bed', look: (t) => 0.2 * Math.sin((t - start(7)) * 3) }, shots: [{ tgt: pHead, yaw: 14, dist: 1.6, h: -0.1, ly: -0.25, dyaw: -6, push: 0.9 }] });
  const tSip = cut(8, 3);
  set(8, { cardWord: 2, shots: [{ tgt: [HOME[0] + 0.03, YP, HOME[1] + 0.022], yaw: 190, dist: 0.2, h: 0.09, ly: -0.012, dyaw: -10, push: 0.9 },
    { at: tSip, tgt: mbAt, yaw: -15, dist: 0.42, h: 0.03, dyaw: 4, push: 0.92 }], moodAt: (t) => (t >= tSip ? 'sip' : 'calm') });
  const home = T_END - 0.08, out = W(9, 2) + 0.05;
  set(9, { mood: 'deadpan', mbPose: 'hips', shots: [{ tgt: mbAt, yaw: -20, dist: 0.4, h: 0.04, dyaw: 4, push: 0.92 },
    { at: out, c0: [MBPOS[0] + 0.35, 0.95, MBPOS[1] - 0.05], l0: [MBPOS[0], 0.75, MBPOS[1]], c1: OPEN.c0, l1: OPEN.l0, mv: home - out }] });
  for (const i of [0, 1]) cfg[i].hideMb = 1;

  // line 1: dart from the bite to the gutter, run up it and sink into the binding
  const d0 = tOn + 0.12, g0 = [HOME[0] + 0.01, GUT + 0.003], g1 = [BK[0] + 0.03, GUT];
  const k1 = [[0, ...HOME], [d0, ...HOME], [d0 + 0.32, ...g0, hd(HOME, g0)], [d0 + 0.5, ...g1, hd(g0, g1)]];
  const tSink = d0 + 0.5;
  // line 4: glue -> paper -> cereal on their words
  const s0 = [SPREAD[0] - 0.05, SPREAD[1] - 0.06], a = [GLUE[0] - 0.022, GLUE[1] + 0.004], b = [PAPER[0], PAPER[1] - 0.005], c = [CEREAL[0] - 0.03, CEREAL[1] - 0.005];
  const k4 = [[start(4), ...s0, hd(s0, a)], [W(4, 0) - 0.15, ...a, hd(s0, a)], [W(4, 1) - 0.25, ...a, hd(s0, a) + 0.4], [W(4, 1) + 0.05, ...b, hd(a, b)],
    [W(4, 2) - 0.25, ...b, hd(a, b)], [W(4, 2) + 0.05, ...c, hd(b, c)], [end(4), ...c, hd(b, c)]];

  function props(t, i) {
    const sf = S.sf;
    // the overhead light: on from "Lights on!" until line 4 (night shift resumes)
    const on = t >= tOn && t < tDark ? ease((t - tOn) / 0.08) : 0;
    S.ceil.intensity = 3.2 * on; S.bulb.material.emissive.setRGB(0.9 * on, 0.85 * on, 0.7 * on);
    let p = HOME, y = YP, amp = 0.12, nib = 0;
    if (i === 0 || i === 9) nib = 1;
    else if (i === 1) { const q = path(t, k1); p = q; amp = q[3] ? 1 : 0.12; if (t > tSink) y = YP - 0.012 * ease((t - tSink) / 0.12); }
    else if (i === 2) { p = [TOPX - 0.001, GUT, 0]; y = YB + 0.004; }
    else if (i === 4) { const q = path(t, k4); p = q; y = YB; amp = q[3] ? 1 : 0.12; nib = q[3] ? 0 : 1; }
    else if (i === 6) { p = [CALP[0] - 0.035, CALP[1] - 0.004, -Math.PI / 2 + 0.25]; y = YB; }
    else if (i === 8) nib = t < W(8, 2) - 0.1 ? 1 : 0;
    sf.visible = i !== 3 && i !== 5 && i !== 7 && !(i === 1 && t > tSink + 0.12);
    place(sf, p, y); wiggle(sf, t, amp, nib);
    if (vis(S.glue, start(4), end(4), t)) { place(S.glue, [...GLUE, 0.5], YB); S.glue.scale.setScalar(popS(t, W(4, 0) - 0.06, 1) || 0.001); }
    if (vis(S.paper, start(4), end(4), t)) { place(S.paper, [...PAPER, 0.3], YB); S.paper.scale.setScalar(popS(t, W(4, 1) - 0.06, 1) || 0.001); }
    if (vis(S.cereal, start(4), end(4), t)) { place(S.cereal, CEREAL, YB); S.cereal.scale.setScalar(popS(t, W(4, 2) - 0.06, 1) || 0.001); }
    if (vis(S.cal, W(6, 2) - 0.06, end(6), t)) { S.cal.position.set(CALP[0], YB, CALP[1] + 0.025); S.cal.scale.setScalar(popS(t, W(6, 2) - 0.06, 0.32)); }
    if (vis(S.dino, W(8, 2) - 0.06, tSip, t)) { place(S.dino, [...DINO, Math.PI + 0.5], YP); S.dino.scale.setScalar(popS(t, W(8, 2) - 0.06, 0.75)); }
    S.mug.visible = i === 8 && t >= tSip;
  }
  function faceCam(cam) { if (S.cal.visible) S.cal.lookAt(cam.position.x, S.cal.position.y, cam.position.z); }
  return { cfg, props, faceCam, POSES, pose0: 'bed', personY: MT - 0.02, MB: 0.07, MBPOS, mbY: 0.55, PPOS, mbIn: start(2), mbOut: home - 0.5 };
}
