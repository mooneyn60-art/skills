// Explainer props for the cockroach + bed-bug episodes (procedural low-poly, same look as props.js).
// Bugs are 1 unit long, face +x, stand on y = 0. The kitchen + bedroom sets live in kitchen.js / bedroom.js.
import * as THREE from 'three';
import { mat, mesh, ICO, ICO1, box, cyl, limbGeo, canvasTex } from './lib.js';

// six jointed legs [hip group, knee group, side, k]; animateLegs walks them (alternating tripod)
function sixLegs(g, m, y, x0, dx, len, r) {
  const legs = [];
  for (const s of [-1, 1]) for (let k = 0; k < 3; k++) {
    const hip = new THREE.Group(); hip.position.set(x0 - k * dx, y, s * 0.09); hip.rotation.order = 'YXZ'; g.add(hip);
    hip.add(mesh(limbGeo(r, r * 0.8, len * 0.45, 4), m));
    const knee = new THREE.Group(); knee.position.z = len * 0.45; hip.add(knee);
    knee.add(mesh(limbGeo(r * 0.8, r * 0.4, len * 0.6, 4), m));
    const kn = 0.15 + Math.asin(Math.min(0.95, (y + len * 0.45 * Math.sin(0.15)) / (len * 0.6)));   // foot on the ground
    legs.push({ hip, knee, s, k, kn, yaw0: (k - 1) * -0.75 });
  }
  return legs;
}
export function animateLegs(b, ph, amp = 1) {
  for (const L of b.userData.legs) {
    const w = ph * 2 * Math.PI + ((L.k + (L.s > 0 ? 1 : 0)) % 2) * Math.PI;
    L.hip.rotation.y = (L.s > 0 ? 0 : Math.PI) + L.s * (L.yaw0 + 0.35 * amp * Math.sin(w));
    L.hip.rotation.x = -0.15 - 0.3 * amp * Math.max(0, Math.cos(w));   // a swinging leg lifts
    L.knee.rotation.x = L.kn;
  }
  for (const a of b.userData.ants || []) a.rotation.x = -0.25 + 0.08 * Math.sin(ph * 3 + a.userData.s);
}

// German cockroach (Blattella germanica): light brown, two dark stripes on the shield behind the head, egg case at the tip
export function makeGermanRoach(withEgg = true) {
  const g = new THREE.Group(), body = new THREE.Group(); g.add(body);
  const tan = mat(0xb3783a), dark = mat(0x3a2210), wing = mat(0x9c6630), legM = mat(0x8a5a2c);
  const ab = mesh(ICO1, tan); ab.scale.set(0.42, 0.11, 0.2); ab.position.set(-0.1, 0.16, 0); body.add(ab);
  for (const s of [-1, 1]) { const w = mesh(ICO1, wing); w.scale.set(0.4, 0.04, 0.12); w.position.set(-0.1, 0.24, s * 0.07); w.rotation.y = s * 0.06; body.add(w); }
  const pro = mesh(ICO1, mat(0xd2a066)); pro.scale.set(0.15, 0.06, 0.2); pro.position.set(0.3, 0.2, 0); body.add(pro);
  for (const s of [-1, 1]) { const st = mesh(ICO, dark, false); st.scale.set(0.12, 0.02, 0.025); st.position.set(0.3, 0.255, s * 0.06); body.add(st); }
  const head = new THREE.Group(); head.position.set(0.44, 0.15, 0); body.add(head);
  const hm = mesh(ICO1, mat(0x8a5a30)); hm.scale.set(0.08, 0.08, 0.1); head.add(hm);
  for (const s of [-1, 1]) { const e = mesh(ICO, dark, false); e.scale.setScalar(0.03); e.position.set(0.04, 0.03, s * 0.07); head.add(e); }
  const ants = [];
  for (const s of [-1, 1]) { const a = new THREE.Group(); a.position.set(0.06, 0.04, s * 0.03); a.rotation.order = 'YXZ'; a.rotation.y = Math.PI / 2 - s * 0.35; a.userData.s = s; a.add(mesh(limbGeo(0.01, 0.004, 0.9, 3), legM, false)); head.add(a); ants.push(a); }
  const legs = sixLegs(body, legM, 0.13, 0.22, 0.17, 0.42, 0.02);
  let egg = null;
  if (withEgg) {   // ~1/4 inch purse-shaped capsule with two rows of segments, carried at the abdomen tip
    egg = new THREE.Group(); egg.position.set(-0.58, 0.15, 0); body.add(egg);
    const cap = mesh(new THREE.BoxGeometry(1, 1, 1, 1, 1, 1), mat(0xc58e4a)); cap.scale.set(0.24, 0.1, 0.14); egg.add(cap);
    for (let k = 0; k < 6; k++) { const r = box(0.012, 0.106, 0.146, 0x7c5428, -0.1 + k * 0.04, -0.053, 0, false); egg.add(r); }
    const keel = box(0.24, 0.012, 0.02, 0x7c5428, 0, 0.05, 0, false); egg.add(keel);
  }
  g.userData = { body, head, legs, ants, egg };
  return g;
}
export function makeNymph() {   // darker, wingless, a tan stripe down the back
  const g = new THREE.Group(), m = mat(0x2e1d10);
  const b = mesh(ICO1, m); b.scale.set(0.42, 0.12, 0.22); b.position.y = 0.14; g.add(b);
  const st = mesh(ICO, mat(0xd8b070), false); st.scale.set(0.38, 0.03, 0.04); st.position.y = 0.25; g.add(st);
  const h = mesh(ICO, m); h.scale.set(0.1, 0.08, 0.11); h.position.set(0.44, 0.13, 0); g.add(h);
  g.userData.legs = sixLegs(g, m, 0.12, 0.2, 0.17, 0.38, 0.02);
  return g;
}

// bed bug (Cimex lectularius): flat oval, reddish brown, banded abdomen; userData.belly swells it like a balloon when fed
export function makeBedBug2() {
  const g = new THREE.Group(), body = new THREE.Group(); g.add(body);
  const rb = mat(0x8c3a1e), dk = mat(0x5a2210), legM = mat(0x7a3a1c);
  const belly = new THREE.Group(); belly.position.set(-0.08, 0.1, 0); body.add(belly);
  const ab = mesh(ICO1, rb); ab.scale.set(0.42, 0.09, 0.36); belly.add(ab);
  for (let k = 0; k < 4; k++) { const b = mesh(ICO1, dk, false); b.scale.set(0.02, 0.092, 0.34 - k * 0.05); b.position.set(0.1 - k * 0.11, 0, 0); belly.add(b); }
  const fed = mesh(ICO1, mat(0xc0281a)); fed.scale.set(0.4, 0.1, 0.32); fed.position.y = 0.01; fed.visible = false; belly.add(fed);
  const pro = mesh(ICO1, rb); pro.scale.set(0.1, 0.06, 0.24); pro.position.set(0.36, 0.1, 0); body.add(pro);
  const head = mesh(ICO, dk); head.scale.set(0.08, 0.05, 0.08); head.position.set(0.5, 0.09, 0); body.add(head);
  const beak = mesh(limbGeo(0.012, 0.006, 0.12, 3), dk, false); beak.position.set(0.55, 0.07, 0); beak.rotation.y = Math.PI / 2; beak.rotation.x = 0.6; body.add(beak);
  const ants = [];
  for (const s of [-1, 1]) { const a = new THREE.Group(); a.position.set(0.55, 0.11, s * 0.04); a.rotation.order = 'YXZ'; a.rotation.y = Math.PI / 2 - s * 0.5; a.userData.s = s; a.add(mesh(limbGeo(0.012, 0.007, 0.32, 3), legM, false)); body.add(a); ants.push(a); }
  const legs = sixLegs(body, legM, 0.08, 0.3, 0.2, 0.36, 0.018);
  g.userData = { body, belly, fed, legs, ants };
  return g;
}
// fed 0..1: belly balloons up, elongates and turns red
export function feedBedBug(b, fed) {
  const u = b.userData, s = 1 + 0.9 * fed;
  u.belly.scale.set(1 + 0.35 * fed, s, 1 + 0.15 * fed); u.belly.position.y = 0.1 + 0.05 * fed; u.belly.position.x = -0.08 - 0.1 * fed;
  u.fed.visible = fed > 0.05; u.fed.scale.set(0.4, 0.1 + 0.02 * fed, 0.32);
}
export function makeBugEgg() { const e = mesh(ICO1, mat(0xf4eedd), false); e.scale.set(0.5, 0.3, 0.3); e.position.y = 0.3; const g = new THREE.Group(); g.add(e); return g; }

// ---------- small props ----------
export function makeNewspaper() {   // rolled, along +x
  const tex = canvasTex(256, 128, (c, w, h) => { c.fillStyle = '#e9e6dc'; c.fillRect(0, 0, w, h); c.fillStyle = '#5a5a5a'; for (let y = 8; y < h; y += 9) for (let x = 6; x < w; x += 46) c.fillRect(x, y, 30 + ((x * y) % 9), 3); c.fillStyle = '#222'; c.fillRect(10, 4, 120, 12); });
  const r = new THREE.Mesh(new THREE.CylinderGeometry(0.028, 0.028, 0.36, 12), new THREE.MeshLambertMaterial({ map: tex })); r.rotation.z = Math.PI / 2; r.castShadow = true;
  const g = new THREE.Group(); g.add(r); return g;
}
export function makeSoap() { const g = new THREE.Group(); const b = mesh(new THREE.BoxGeometry(1, 1, 1, 2, 2, 2), mat(0xf0b8c8)); b.scale.set(0.07, 0.025, 0.045); b.position.y = 0.0125; g.add(b); const n = mesh(ICO, mat(0xffd6e0)); n.scale.set(0.02, 0.004, 0.012); n.position.y = 0.026; g.add(n); return g; }
export function makeGlue() {
  const g = new THREE.Group();
  const tex = canvasTex(128, 128, (c, w, h) => { c.fillStyle = '#fafafa'; c.fillRect(0, 0, w, h); c.fillStyle = '#e8862a'; c.fillRect(0, 40, w, 46); c.fillStyle = '#fff'; c.font = '900 30px Inter'; c.textAlign = 'center'; c.fillText('GLUE', w / 2, 74); });
  const b = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.02, 0.07, 14), new THREE.MeshLambertMaterial({ map: tex })); b.position.y = 0.035; b.castShadow = true; g.add(b);
  const cap = cyl(0.009, 0.014, 0.018, 0xe8862a, 10); cap.position.y = 0.079; g.add(cap);
  const tip = mesh(new THREE.ConeGeometry(0.004, 0.014, 6), mat(0xe8862a)); tip.position.y = 0.095; g.add(tip);
  return g;
}
export function makeHair() {   // a loose tangle of a few dark strands on the surface
  const g = new THREE.Group(), m = mat(0x2a1a10, { flatShading: false });
  for (let k = 0; k < 4; k++) {
    const pts = []; for (let i = 0; i <= 12; i++) { const a = i * 0.7 + k * 1.3; pts.push(new THREE.Vector3(0.03 * Math.cos(a) + i * 0.004 - 0.02, 0.0015, 0.025 * Math.sin(a * 1.1 + k))); }
    g.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 40, 0.0007, 4), m));
  }
  return g;
}
export function makeCrumbs() { const g = new THREE.Group(); for (let k = 0; k < 9; k++) { const c = mesh(ICO, mat(0xd9a75c)); c.scale.set(0.004 + (k % 3) * 0.002, 0.003, 0.004); c.position.set(0.03 * Math.sin(k * 2.3), 0.002, 0.03 * Math.cos(k * 1.7)); g.add(c); } return g; }
// stand-up desk calendar (faces +z): red header `head`, big word `big`
export function makeCal(head, big) {
  const tex = canvasTex(256, 300, (c, w, h) => {
    c.fillStyle = '#ffffff'; c.fillRect(0, 0, w, h); c.fillStyle = '#c4261e'; c.fillRect(0, 0, w, 70);
    const fit = (txt, px, y) => { c.font = `900 ${px}px Inter`; const k = Math.min(1, (w - 24) / c.measureText(txt).width); c.font = `900 ${Math.floor(px * k)}px Inter`; c.fillText(txt, w / 2, y); };
    c.textAlign = 'center'; c.fillStyle = '#fff'; fit(head, 40, 50);
    c.fillStyle = '#1a1a1a'; fit(big, 120, 210);
    c.fillStyle = '#555'; for (let i = 0; i < 7; i++) { c.beginPath(); c.arc(24 + i * 35, 14, 6, 0, 7); c.fill(); }
  });
  const g = new THREE.Group();
  const page = new THREE.Mesh(new THREE.PlaneGeometry(0.1, 0.117), new THREE.MeshLambertMaterial({ map: tex })); page.position.y = 0.0585; g.add(page);
  g.add(box(0.104, 0.12, 0.006, 0x333333, 0, 0, -0.004));
  return g;
}
export function makeLamp() {   // bedside lamp, the bulb glows
  const g = new THREE.Group();
  g.add(cyl(0.06, 0.07, 0.03, 0x6b5a48, 10)); g.children[0].position.y = 0.015;
  const p = cyl(0.012, 0.012, 0.25, 0x6b5a48, 6); p.position.y = 0.15; g.add(p);
  const sh = mesh(new THREE.CylinderGeometry(0.08, 0.12, 0.14, 12, 1, true), new THREE.MeshLambertMaterial({ color: 0xf6dfa8, emissive: 0x6a4a18, side: THREE.DoubleSide })); sh.position.y = 0.3; g.add(sh);
  return g;
}

// Meatball's mug (Meatball units; child of his forearm group, the hand sits at z 0.62)
export function makeMug() {
  const g = new THREE.Group();
  const c = cyl(0.17, 0.15, 0.32, 0xf2efe6, 12); c.position.set(0, 0, 0.0); g.add(c);
  const coffee = cyl(0.15, 0.15, 0.01, 0x3a2414, 12); coffee.position.y = 0.155; g.add(coffee);
  const h = mesh(new THREE.TorusGeometry(0.08, 0.025, 4, 10), mat(0xf2efe6)); h.position.set(0, 0, 0.17); h.rotation.y = Math.PI / 2; g.add(h);
  g.position.set(0, 0.1, 0.66); g.rotation.x = 0.35;   // upright in the hand, tipped toward the mouth
  return g;
}
