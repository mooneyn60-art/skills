// Explainer cast + props (all procedural low-poly): Meatball, a faceless person with knees/elbows, prey, set dressing.
import * as THREE from 'three';
import { mat, mesh, ICO, ICO1, box, cyl, limbGeo, canvasTex, makeCentipede } from './lib.js';

// ---------- Meatball (ball radius 1 unit, face on +x) ----------
export function makeMeatball() {
  const g = new THREE.Group(), body = new THREE.Group(); g.add(body);
  const geo = new THREE.IcosahedronGeometry(1, 2), p = geo.attributes.position, v = new THREE.Vector3();
  for (let i = 0; i < p.count; i++) { v.fromBufferAttribute(p, i); v.multiplyScalar(1 + 0.07 * Math.sin(v.x * 5.1 + v.y * 2.3) * Math.cos(v.z * 4.3 - v.y * 1.7)); p.setXYZ(i, v.x, v.y, v.z); }
  geo.computeVertexNormals();
  body.add(mesh(geo, mat(0x8e4a2b)));
  for (const [x, y, z] of [[0.5, 0.55, 0.55], [-0.6, 0.2, 0.7], [0.7, -0.4, 0.5], [-0.3, -0.6, 0.72], [0.1, 0.85, -0.4], [-0.75, 0.5, -0.3]]) {
    const s = mesh(ICO, mat(0x6a3219), false); s.scale.set(0.16, 0.16, 0.06); s.position.set(x, y, z).normalize().multiplyScalar(0.99); s.lookAt(s.position.clone().multiplyScalar(2)); body.add(s);
  }
  const cap = new THREE.Group(); cap.position.set(0, 0.86, 0); cap.rotation.z = 0.12; body.add(cap);
  const dome = mesh(new THREE.SphereGeometry(0.62, 10, 5, 0, Math.PI * 2, 0, Math.PI / 2), mat(0xc4261e)); dome.scale.y = 0.45; cap.add(dome);
  const brim = mesh(new THREE.CylinderGeometry(0.85, 0.85, 0.05, 12), mat(0xb21f18)); brim.position.set(0.25, 0.02, 0); brim.scale.set(1, 1, 0.75); cap.add(brim);
  const parsley = mesh(ICO, mat(0x3f9a3c)); parsley.scale.set(0.12, 0.08, 0.12); parsley.position.set(0.05, 0.3, 0); cap.add(parsley);
  const face = new THREE.Group(); body.add(face);
  const eyes = [], lids = [], brows = [];
  for (const s of [-1, 1]) {
    const e = new THREE.Group(); e.position.set(0.86, 0.22, s * 0.3); face.add(e);
    const white = mesh(new THREE.SphereGeometry(0.24, 12, 8), mat(0xffffff, { flatShading: false }), false); white.scale.x = 0.6; e.add(white);
    const pupil = mesh(new THREE.SphereGeometry(0.11, 10, 6), mat(0x111111, { flatShading: false }), false); pupil.position.x = 0.13; e.add(pupil);
    const lid = mesh(new THREE.SphereGeometry(0.255, 12, 6, 0, Math.PI * 2, 0, Math.PI / 2), mat(0x8e4a2b), false); lid.scale.x = 0.65; e.add(lid);
    const brow = mesh(new THREE.BoxGeometry(0.05, 0.05, 0.3), mat(0x111111), false); brow.position.set(0.92, 0.55, s * 0.3); face.add(brow);
    eyes.push({ e, pupil, s }); lids.push(lid); brows.push({ brow, s });
  }
  const mouth = mesh(new THREE.SphereGeometry(0.16, 10, 6), mat(0x1a0d08, { flatShading: false }), false); mouth.position.set(0.93, -0.3, 0); mouth.scale.set(0.35, 0.3, 1); face.add(mouth);
  const ink = mat(0x141414), arms = [], legs = [];
  for (const s of [-1, 1]) {
    const sh = new THREE.Group(); sh.position.set(0, -0.1, s * 0.95); g.add(sh);
    sh.add(mesh(limbGeo(0.06, 0.06, 0.7, 5), ink));
    const el = new THREE.Group(); el.position.z = 0.7; sh.add(el);
    el.add(mesh(limbGeo(0.06, 0.055, 0.6, 5), ink));
    const hand = mesh(new THREE.SphereGeometry(0.11, 8, 6), ink); hand.position.z = 0.62; el.add(hand);
    sh.scale.z = s; arms.push({ sh, el, s });
    const hip = new THREE.Group(); hip.position.set(0, -0.85, s * 0.32); g.add(hip);
    const l = mesh(limbGeo(0.065, 0.06, 0.95, 5), ink); l.rotation.x = Math.PI / 2; hip.add(l);
    const foot = mesh(new THREE.SphereGeometry(0.14, 8, 5), ink); foot.scale.set(1.6, 0.6, 1); foot.position.set(0.1, -0.97, 0); hip.add(foot);
    legs.push(hip);
  }
  g.userData = { body, eyes, lids, brows, mouth, arms, legs };
  return g;
}
export const MB_POSES = {
  idle: { sp: 1.25, sy: 0.15, el: 0.25 },
  stop: { sp: -0.45, sy: 1.15, el: -0.9 },
  shrug: { sp: 0.2, sy: 0.25, el: -1.5 },
  hips: { sp: 0.9, sy: -0.6, el: 1.6 },
  point: { sp: 0.1, sy: 1.3, el: 0.0 },
};
// mood: calm | alarm | deadpan | smug | whisper
export function poseMeatball(m, t, pose, talk, mood) {
  const u = m.userData;
  u.arms.forEach((a, k) => {
    const P = mood === 'whisper' && k === 1 ? { sp: -0.2, sy: 1.5, el: -1.9 } : mood === 'sip' && k === 1 ? { sp: 0.38, sy: 2.0, el: -0.3 } : pose;
    a.sh.rotation.order = 'YXZ'; a.sh.rotation.y = P.sy; a.sh.rotation.x = P.sp + 0.05 * Math.sin(t * 2 + a.s);
    a.el.rotation.x = P.el;
  });
  u.mouth.scale.set(0.35, 0.18 + 0.75 * talk, 1);
  u.body.position.y = 0.03 * Math.sin(t * 3.1) + 0.06 * talk;
  u.body.rotation.z = mood === 'smug' ? -0.12 * Math.abs(Math.sin(t * 5)) : 0.04 * Math.sin(t * 1.7) + (mood === 'deadpan' ? -0.05 : 0.04 * talk);
  u.body.rotation.y = mood === 'whisper' ? -0.25 : 0;
  const half = mood === 'deadpan' || mood === 'smug' || mood === 'whisper' || mood === 'sip';
  const lid = half ? 0.75 : (Math.abs(((t + 0.7) % 3.1) - 0.05) < 0.07 ? 1 : 0);
  for (const l of u.lids) { l.visible = lid > 0; l.scale.y = Math.max(0.01, lid); }
  for (const b of u.brows) {
    b.brow.position.y = mood === 'alarm' ? 0.66 : half ? 0.47 : 0.55;
    b.brow.rotation.x = mood === 'alarm' ? -0.25 * b.s : half ? 0.12 * b.s : 0;
  }
  for (const e of u.eyes) { e.pupil.position.y = 0.04 * Math.sin(t * 9 + e.s) * (talk + 0.2); e.pupil.position.z = 0.04 * Math.cos(t * 7 + e.s) * (talk + 0.2); }
}

// ---------- faceless person, 1.75 m, faces +x; knees + elbows ----------
export function makePerson(shirt = 0x3c6e8f) {
  const g = new THREE.Group(), skin = mat(0xe0ac85), pants = mat(0x2a2a33), hair = mat(0x3b2618), sm = mat(shirt);
  const pelvis = new THREE.Group(); pelvis.position.y = 0.92; g.add(pelvis);
  const chest = new THREE.Group(); pelvis.add(chest);
  const torso = mesh(new THREE.BoxGeometry(1, 1, 1), sm); torso.scale.set(0.24, 0.6, 0.42); torso.position.y = 0.3; chest.add(torso);
  const neck = cyl(0.05, 0.05, 0.1, skin); neck.position.y = 0.64; chest.add(neck);
  const head = new THREE.Group(); head.position.y = 0.76; chest.add(head);
  const skull = mesh(ICO1, skin); skull.scale.set(0.11, 0.13, 0.1); head.add(skull);
  const hr = mesh(ICO1, hair); hr.scale.set(0.115, 0.08, 0.105); hr.position.set(-0.015, 0.07, 0); head.add(hr);
  const P = { pelvis, chest, head, hips: [], knees: [], sh: [], el: [], hands: [] };
  for (const s of [-1, 1]) {
    const hip = new THREE.Group(); hip.position.set(0, 0, s * 0.1); pelvis.add(hip);
    const th = mesh(limbGeo(0.08, 0.07, 0.46, 6), pants); th.rotation.x = Math.PI / 2; hip.add(th);
    const knee = new THREE.Group(); knee.position.y = -0.46; hip.add(knee);
    const sn = mesh(limbGeo(0.07, 0.06, 0.42, 6), pants); sn.rotation.x = Math.PI / 2; knee.add(sn);
    knee.add(box(0.27, 0.08, 0.11, 0x1c1c1c, 0.06, -0.46, 0));
    const sh = new THREE.Group(); sh.position.set(0, 0.53, s * 0.25); chest.add(sh);
    const ua = mesh(limbGeo(0.055, 0.05, 0.32, 6), sm); ua.rotation.x = Math.PI / 2; sh.add(ua);
    const el = new THREE.Group(); el.position.y = -0.32; sh.add(el);
    const fa = mesh(limbGeo(0.05, 0.045, 0.28, 6), sm); fa.rotation.x = Math.PI / 2; el.add(fa);
    const hand = new THREE.Group(); hand.position.y = -0.32; el.add(hand);
    const hm = mesh(ICO, skin); hm.scale.setScalar(0.055); hand.add(hm);
    P.hips.push(hip); P.knees.push(knee); P.sh.push(sh); P.el.push(el); P.hands.push(hand);
  }
  g.userData = P;
  return g;
}
// arrays are [left(-z), right(+z)]; z* = forward swing, x* = sideways (already mirrored per side)
export const PERSON_POSES = {
  stand: { py: 0.92, lean: 0, hip: [0, 0], knee: [0, 0], shz: [0.08, 0.08], elz: [0.2, 0.2], shx: [0, 0], elx: [0, 0] },
  slipper: { py: 0.92, lean: 0.08, hip: [0, 0], knee: [0, 0], shz: [0.3, 2.6], elz: [0.4, 0.5], shx: [0, 0], elx: [0, 0] },
  crouch: { py: 0.43, lean: -0.45, hip: [1.65, 1.55], knee: [-2.2, -2.15], shz: [0.9, 0.95], elz: [0.5, 0.5], shx: [0, 0], elx: [0, 0] },
  seated: { py: 0.6, lean: 0.05, hip: [1.5, 1.5], knee: [-1.5, -1.5], shz: [0.45, 0.45], elz: [0.8, 0.8], shx: [0, 0], elx: [0, 0] },
  back: { py: 0.92, lean: 0.22, hip: [0.25, -0.3], knee: [-0.2, 0], shz: [1.3, 1.4], elz: [0.9, 0.9], shx: [0, 0], elx: [0, 0] },
  head: { py: 0.92, lean: 0.05, hip: [0, 0], knee: [0, 0], shz: [0, 0], elz: [0, 0], shx: [2.6, 2.6], elx: [1.48, 1.48] },
  sign: { py: 0.92, lean: -0.1, hip: [0, 0], knee: [0, 0], shz: [0.7, 0.9], elz: [1.0, 1.3], shx: [0, 0], elx: [0, 0] },
};
export function posePerson(h, t, pose, talk = 0, lookYaw = 0) {
  const P = h.userData;
  P.pelvis.position.y = pose.py + 0.008 * talk;
  P.chest.rotation.z = pose.lean + 0.02 * Math.sin(t * 6) * talk;
  P.head.rotation.y = lookYaw; P.head.rotation.z = 0.04 * talk * Math.sin(t * 9);
  for (let k = 0; k < 2; k++) {
    const s = k ? 1 : -1;
    P.hips[k].rotation.z = pose.hip[k]; P.knees[k].rotation.z = pose.knee[k];
    P.sh[k].rotation.set(-pose.shx[k] * s, 0, pose.shz[k] + 0.03 * Math.sin(t * 1.3 + k));
    P.el[k].rotation.set(-pose.elx[k] * s, 0, pose.elz[k]);
  }
}

// ---------- prey + cast (body length ~1 unit, faces +x) ----------
const legRing = (g, n, len, r, y, m, spread = 0.9, droop = 0.6) => {
  for (const s of [-1, 1]) for (let k = 0; k < n; k++) {
    const l = mesh(limbGeo(r, r * 0.6, len, 4), m); l.position.set(0.15 - k * (0.3 / Math.max(1, n - 1)), y, s * 0.08);
    l.rotation.order = 'YXZ'; l.rotation.y = s > 0 ? (k - (n - 1) / 2) * spread * 0.5 : Math.PI - (k - (n - 1) / 2) * spread * 0.5; l.rotation.x = droop; g.add(l);
  }
};
export function makeSpider() {
  const g = new THREE.Group(), m = mat(0x2b2420);
  const ab = mesh(ICO1, m); ab.scale.set(0.42, 0.32, 0.34); ab.position.set(-0.3, 0.35, 0); g.add(ab);
  const ce = mesh(ICO1, mat(0x3a302a)); ce.scale.set(0.24, 0.18, 0.2); ce.position.set(0.12, 0.3, 0); g.add(ce);
  for (const s of [-1, 1]) for (let k = 0; k < 4; k++) {
    const hip = new THREE.Group(); hip.position.set(0.15 - k * 0.07, 0.32, s * 0.12); g.add(hip);
    hip.rotation.order = 'YXZ'; hip.rotation.y = (s > 0 ? 0 : Math.PI) + s * (k - 1.5) * 0.45; hip.rotation.x = -0.7 * s;
    const a = mesh(limbGeo(0.03, 0.025, 0.42, 4), m); hip.add(a);
    const kn = new THREE.Group(); kn.position.z = 0.42; kn.rotation.x = 1.5 * s; hip.add(kn);
    kn.add(mesh(limbGeo(0.025, 0.012, 0.48, 4), m));
  }
  return g;
}
export function makeSilverfish() {
  const g = new THREE.Group(), m = mat(0x8a96a0), d = mat(0x5e6872);
  for (let i = 0; i < 6; i++) { const s = mesh(ICO1, i % 2 ? m : d); const w = 0.17 * (1 - i / 8); s.scale.set(0.11, 0.05, w); s.position.set(0.3 - i * 0.12, 0.06, 0); g.add(s); }
  for (const a of [-0.35, 0, 0.35]) { const tl = mesh(limbGeo(0.012, 0.004, 0.45, 3), d); tl.position.set(-0.35, 0.06, 0); tl.rotation.y = -Math.PI / 2 + a; g.add(tl); }
  for (const s of [-1, 1]) { const an = mesh(limbGeo(0.012, 0.004, 0.5, 3), d); an.position.set(0.38, 0.07, s * 0.03); an.rotation.y = Math.PI / 2 - s * 0.4; g.add(an); }
  legRing(g, 3, 0.18, 0.012, 0.05, d);
  return g;
}
export function makeAnt() {
  const g = new THREE.Group(), m = mat(0x1d1512);
  for (const [x, sx, sy] of [[0.35, 0.14, 0.12], [0.08, 0.16, 0.08], [-0.25, 0.22, 0.15]]) { const s = mesh(ICO1, m); s.scale.set(sx, sy, sy); s.position.set(x, 0.18, 0); g.add(s); }
  legRing(g, 3, 0.3, 0.015, 0.16, m, 1.0, 0.7);
  for (const s of [-1, 1]) { const an = mesh(limbGeo(0.012, 0.008, 0.3, 3), m); an.position.set(0.45, 0.24, s * 0.04); an.rotation.y = Math.PI / 2 - s * 0.5; an.rotation.x = -0.5; g.add(an); }
  return g;
}
export function makeBedBug() {
  const g = new THREE.Group(), m = mat(0x7a2e1a);
  const b = mesh(ICO1, m); b.scale.set(0.42, 0.12, 0.36); b.position.y = 0.13; g.add(b);
  const h = mesh(ICO, mat(0x5e2414)); h.scale.set(0.12, 0.08, 0.16); h.position.set(0.42, 0.13, 0); g.add(h);
  legRing(g, 3, 0.26, 0.018, 0.1, mat(0x5e2414));
  return g;
}
export function makeBee() {
  const g = new THREE.Group(), y = mat(0xf2c12e), k = mat(0x1a1410);
  for (let i = 0; i < 5; i++) { const s = mesh(new THREE.CylinderGeometry(0.2 - Math.abs(i - 2) * 0.04, 0.2 - Math.abs(i - 1.6) * 0.04, 0.12, 10), i % 2 ? k : y); s.rotation.z = Math.PI / 2; s.position.set(0.2 - i * 0.11, 0.4, 0); g.add(s); }
  const h = mesh(ICO1, k); h.scale.setScalar(0.14); h.position.set(0.36, 0.42, 0); g.add(h);
  const st = mesh(new THREE.ConeGeometry(0.03, 0.12, 5), k); st.rotation.z = Math.PI / 2; st.position.set(-0.4, 0.4, 0); g.add(st);
  const wm = new THREE.MeshLambertMaterial({ color: 0xe8f4ff, transparent: true, opacity: 0.6, side: THREE.DoubleSide });
  const wings = [];
  for (const s of [-1, 1]) { const w = new THREE.Group(); w.position.set(0.08, 0.58, s * 0.05); const p = mesh(ICO1, wm, false); p.scale.set(0.2, 0.02, 0.32); p.position.z = s * 0.3; w.add(p); g.add(w); wings.push({ w, s }); }
  g.userData.wings = wings;
  return g;
}
export function makeBabyCentipede() {
  const c = makeCentipede();
  for (const L of c.userData.legs) if (L.i >= 4) L.yaw.parent.visible = false;   // hatchlings: 4 leg pairs
  return c;
}
export function makeLooseLeg() {   // a dropped centipede leg (centipede units)
  const g = new THREE.Group(), a = mat(0xdcc49a), b = mat(0x6e5236);
  const f = mesh(limbGeo(0.0042, 0.0032, 0.2), a); g.add(f);
  const k = new THREE.Group(); k.position.z = 0.2; g.add(k);
  k.add(mesh(limbGeo(0.0032, 0.0026, 0.15), b)); const t2 = mesh(limbGeo(0.0026, 0.001, 0.15), a); t2.position.z = 0.15; k.add(t2);
  g.userData.knee = k;
  return g;
}

// ---------- set dressing ----------
export function makeDrain() {
  const g = new THREE.Group();
  const ring = mesh(new THREE.CylinderGeometry(0.06, 0.065, 0.006, 20), mat(0xc8ccd0)); ring.position.y = 0.003; g.add(ring);
  const hole = mesh(new THREE.CylinderGeometry(0.048, 0.048, 0.007, 20), mat(0x15171a)); hole.position.y = 0.004; g.add(hole);
  for (let i = -2; i <= 2; i++) { const bar = box(0.008, 0.004, 0.09 - Math.abs(i) * 0.012, 0xb4b9be, i * 0.018, 0.005, 0, false); g.add(bar); }
  const wet = new THREE.MeshLambertMaterial({ color: 0xa9d4e6, transparent: true, opacity: 0.55, emissive: 0x16303a });
  for (const [x, z, sx, sz] of [[0.12, 0.05, 0.11, 0.07], [-0.1, -0.08, 0.08, 0.06], [0.3, 0.14, 0.12, 0.06], [0.48, 0.02, 0.07, 0.05], [0.05, -0.15, 0.05, 0.04]]) {
    const p = new THREE.Mesh(new THREE.CircleGeometry(1, 14), wet); p.rotation.x = -Math.PI / 2; p.scale.set(sx, sz, 1); p.position.set(x, 0.0035, z); g.add(p);
  }
  return g;
}
export function makeWindow() {   // on the back wall (normal +z); glass + moon swap for night
  const g = new THREE.Group();
  const frameM = mat(0xffffff);
  g.add(box(0.78, 0.05, 0.05, frameM, 0, -0.025, 0), box(0.78, 0.05, 0.05, frameM, 0, 0.8, 0), box(0.05, 0.85, 0.05, frameM, -0.39, -0.025, 0), box(0.05, 0.85, 0.05, frameM, 0.39, -0.025, 0), box(0.03, 0.8, 0.03, frameM, 0, 0, 0.01));
  const glassM = new THREE.MeshBasicMaterial({ color: 0xbfe0f2 });
  const glass = new THREE.Mesh(new THREE.PlaneGeometry(0.74, 0.78), glassM); glass.position.set(0, 0.4, -0.005); g.add(glass);
  const moon = new THREE.Mesh(new THREE.CircleGeometry(0.11, 24), new THREE.MeshBasicMaterial({ color: 0xfff6d8 })); moon.position.set(0.16, 0.56, 0); g.add(moon);
  const stars = [];
  for (const [x, y] of [[-0.25, 0.65], [-0.12, 0.3], [-0.28, 0.2], [0.27, 0.25], [0.05, 0.7]]) { const s = new THREE.Mesh(new THREE.CircleGeometry(0.008, 6), moon.material); s.position.set(x, y, 0); g.add(s); stars.push(s); }
  g.userData = { glassM, moon, stars };
  return g;
}
export function makeFan() {
  const g = new THREE.Group(), w = mat(0xf0f0f0), gr = mat(0x8a9399);
  g.add(cyl(0.08, 0.1, 0.03, w, 12)); g.children[0].position.y = 0.015;
  const pole = cyl(0.015, 0.015, 0.25, gr, 6); pole.position.y = 0.15; g.add(pole);
  const head = new THREE.Group(); head.position.set(0.02, 0.32, 0); g.add(head);
  const cage = mesh(new THREE.TorusGeometry(0.13, 0.008, 4, 20), gr); cage.rotation.y = Math.PI / 2; head.add(cage);
  const hub = cyl(0.03, 0.03, 0.05, w, 8); hub.rotation.z = Math.PI / 2; head.add(hub);
  const rotor = new THREE.Group(); rotor.position.x = 0.03; head.add(rotor);
  for (let k = 0; k < 3; k++) { const b = mesh(ICO, mat(0x7fb8d6)); b.scale.set(0.01, 0.11, 0.045); b.position.y = 0.06; const a = new THREE.Group(); a.rotation.x = k * 2.094; a.add(b); rotor.add(a); }
  g.userData.rotor = rotor;
  return g;
}
export function makePipe() {   // wall pipe with a leaky joint along +x
  const g = new THREE.Group(), m = mat(0x6f7a84);
  const run = cyl(0.025, 0.025, 0.6, m, 10); run.rotation.z = Math.PI / 2; run.position.set(0, 0.3, 0); g.add(run);
  const down = cyl(0.025, 0.025, 0.3, m, 10); down.position.set(0.3, 0.15, 0); g.add(down);
  const joint = cyl(0.035, 0.035, 0.06, mat(0x9aa0a6), 10); joint.rotation.z = Math.PI / 2; joint.position.set(-0.05, 0.3, 0); g.add(joint);
  const wrap = cyl(0.04, 0.04, 0.07, mat(0xd7d7d7), 10); wrap.rotation.z = Math.PI / 2; wrap.position.copy(joint.position); wrap.visible = false; g.add(wrap);
  const dm = new THREE.MeshLambertMaterial({ color: 0x8fd0f0, emissive: 0x204050 });
  const drops = [0, 1, 2].map(() => { const d = mesh(ICO1, dm, false); d.scale.set(0.014, 0.02, 0.014); g.add(d); return d; });
  const pud = new THREE.Mesh(new THREE.CircleGeometry(1, 14), new THREE.MeshLambertMaterial({ color: 0xa9d4e6, transparent: true, opacity: 0.6, emissive: 0x16303a }));
  pud.rotation.x = -Math.PI / 2; pud.scale.set(0.08, 0.05, 1); pud.position.set(-0.05, 0.004, 0.03); g.add(pud);
  g.userData = { joint, wrap, drops };
  return g;
}
export function makeBoxes() {
  const g = new THREE.Group(), list = [];
  for (const [x, y, z, s, c] of [[0, 0, 0, 0.26, 0xb8895a], [0.02, 0.26, 0.01, 0.2, 0xc69a68], [0.3, 0, 0.05, 0.22, 0xa97c50], [-0.02, 0.46, 0, 0.14, 0xd0a674]]) {
    const b = box(s, s, s, c, 0, 0, 0); b.position.set(x, y + s / 2, z); const tape = box(s * 1.01, 0.02, s * 0.2, 0xe0d4b0, 0, 0, 0, false); b.add(tape); tape.scale.divideScalar(s); tape.position.set(0, 0.5, 0);
    g.add(b); list.push(b);
  }
  g.userData.list = list;
  return g;
}
export function makeCalendar() {
  const tex = canvasTex(256, 300, (c, w, h) => {
    c.fillStyle = '#ffffff'; c.fillRect(0, 0, w, h);
    c.fillStyle = '#c4261e'; c.fillRect(0, 0, w, 70);
    c.fillStyle = '#fff'; c.font = '900 40px Inter'; c.textAlign = 'center'; c.fillText('YEARS', w / 2, 50);
    c.fillStyle = '#1a1a1a'; c.font = '900 190px Inter'; c.fillText('7', w / 2, 260);
    c.fillStyle = '#555'; for (let i = 0; i < 7; i++) { c.beginPath(); c.arc(24 + i * 35, 14, 6, 0, 7); c.fill(); }
  });
  const g = new THREE.Group();
  const page = new THREE.Mesh(new THREE.PlaneGeometry(0.1, 0.117), new THREE.MeshLambertMaterial({ map: tex })); page.position.y = 0.0585; g.add(page);
  const back = box(0.104, 0.12, 0.006, 0x333333, 0, 0, -0.004); g.add(back);
  return g;
}
export function makeTowel() {
  const tex = canvasTex(128, 128, (c, w) => { for (let i = 0; i < 8; i++) { c.fillStyle = i % 2 ? '#f4f0e6' : '#7cc4e4'; c.fillRect(0, i * 16, w, 16); } });
  const t = new THREE.Mesh(new THREE.PlaneGeometry(0.13, 0.2), new THREE.MeshLambertMaterial({ map: tex })); t.rotation.x = -Math.PI / 2; t.position.y = 0.004; t.receiveShadow = true;
  const g = new THREE.Group(); g.add(t); return g;
}
export function makeSlipper() {
  const g = new THREE.Group();
  const sole = box(0.27, 0.025, 0.1, 0x6d4bb0, 0, 0, 0); g.add(sole);
  const strap = box(0.08, 0.04, 0.1, 0x8e6bd0, 0.06, 0.025, 0); g.add(strap);
  return g;
}
