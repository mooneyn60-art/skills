// Explainer props for the jumping-spider + dust-mite episodes (procedural low-poly, same look as props.js / props2.js).
// Critters are 1 unit long, face +x, stand on y = 0.
import * as THREE from 'three';
import { mat, mesh, ICO, ICO1, box, cyl, limbGeo, canvasTex } from './lib.js';

// n jointed legs per side [hip group, knee group, side, k]; walks with props2.animateLegs (same userData.legs shape)
function legs(g, m, n, y, x0, dx, len, r, yawStep) {
  const out = [];
  for (const s of [-1, 1]) for (let k = 0; k < n; k++) {
    const hip = new THREE.Group(); hip.position.set(x0 - k * dx, y, s * 0.1); hip.rotation.order = 'YXZ'; g.add(hip);
    const L = len * (k === 0 ? 1.15 : 1);   // a jumper's front legs are the stoutest
    hip.add(mesh(limbGeo(r * (k === 0 ? 1.5 : 1), r * 0.8, L * 0.45, 4), m));
    const knee = new THREE.Group(); knee.position.z = L * 0.45; hip.add(knee);
    knee.add(mesh(limbGeo(r * 0.8, r * 0.45, L * 0.6, 4), m));
    const kn = 0.15 + Math.asin(Math.min(0.95, (y + L * 0.45 * Math.sin(0.15)) / (L * 0.6)));
    out.push({ hip, knee, s, k, kn, yaw0: ((n - 1) / 2 - k) * yawStep });
  }
  return out;
}

// Jumping spider (bold jumper look): black, fuzzy, white abdomen spots, iridescent green fangs, two huge front eyes
export function makeJumpSpider() {
  const g = new THREE.Group(), body = new THREE.Group(); g.add(body);
  const blk = mat(0x1c1a1c), fur = mat(0x2c2a2e), wht = mat(0xf2efe6);
  const ceph = mesh(ICO1, mat(0x46404a)); ceph.scale.set(0.3, 0.2, 0.26); ceph.position.set(0.16, 0.3, 0); body.add(ceph);
  const ab = mesh(ICO1, fur); ab.scale.set(0.34, 0.22, 0.26); ab.position.set(-0.32, 0.3, 0); body.add(ab);
  const spot = mesh(ICO, wht, false); spot.scale.set(0.07, 0.03, 0.07); spot.position.set(-0.26, 0.51, 0); body.add(spot);
  for (const s of [-1, 1]) { const d = mesh(ICO, wht, false); d.scale.set(0.05, 0.025, 0.04); d.position.set(-0.44, 0.47, s * 0.1); body.add(d); }
  const band = mesh(ICO1, mat(0xd8d2c4), false); band.scale.set(0.05, 0.05, 0.27); band.position.set(-0.03, 0.28, 0); body.add(band);
  // face: AME (huge), ALE (medium) across the front; PME (tiny) + PLE on top
  const lens = mat(0x050505, { flatShading: false }), shine = new THREE.MeshBasicMaterial({ color: 0xffffff });
  const eye = (r, x, y, z, glint) => { const e = mesh(new THREE.SphereGeometry(r, 14, 10), lens, false); e.position.set(x, y, z); body.add(e);
    if (glint) { const s = mesh(new THREE.SphereGeometry(r * 0.28, 8, 6), shine, false); s.position.set(x + r * 0.8, y + r * 0.45, z + r * 0.25); body.add(s); } return e; };
  const fringe = mesh(ICO1, mat(0xc8a46a), false); fringe.scale.set(0.03, 0.15, 0.27); fringe.position.set(0.37, 0.33, 0); body.add(fringe);
  const ame = [-1, 1].map((s) => eye(0.085, 0.41, 0.32, s * 0.075, true));
  for (const s of [-1, 1]) { eye(0.042, 0.38, 0.34, s * 0.17, true); eye(0.012, 0.3, 0.42, s * 0.16, false); eye(0.035, 0.12, 0.46, s * 0.15, true); }
  for (const s of [-1, 1]) { const c = mesh(ICO1, mat(0x2fa37e, { emissive: 0x0b3a2a }), false); c.scale.set(0.035, 0.055, 0.032); c.position.set(0.44, 0.2, s * 0.04); body.add(c); }
  const palps = [-1, 1].map((s) => { const p = new THREE.Group(); p.position.set(0.42, 0.24, s * 0.1); p.rotation.order = 'YXZ'; p.rotation.y = Math.PI / 2 - s * 0.2; p.rotation.x = 0.6;
    p.add(mesh(limbGeo(0.025, 0.035, 0.16, 4), wht, false)); body.add(p); return p; });
  const L = legs(body, fur, 4, 0.26, 0.26, 0.075, 0.5, 0.028, 0.55);
  g.userData = { body, legs: L, palps, ame, ants: [] };
  return g;
}

// house fly: grey body, red eyes, clear wings
export function makeFly() {
  const g = new THREE.Group(), body = new THREE.Group(); g.add(body);
  const gr = mat(0x3a3a40), dk = mat(0x1a1a1e);
  const th = mesh(ICO1, gr); th.scale.set(0.22, 0.18, 0.18); th.position.set(0.1, 0.3, 0); body.add(th);
  const ab = mesh(ICO1, mat(0x55555c)); ab.scale.set(0.3, 0.15, 0.18); ab.position.set(-0.22, 0.27, 0); body.add(ab);
  const hd = mesh(ICO1, dk); hd.scale.set(0.12, 0.14, 0.17); hd.position.set(0.36, 0.3, 0); body.add(hd);
  for (const s of [-1, 1]) { const e = mesh(ICO1, mat(0x9a1e14), false); e.scale.set(0.08, 0.11, 0.08); e.position.set(0.38, 0.32, s * 0.1); body.add(e); }
  const wm = new THREE.MeshLambertMaterial({ color: 0xdfeaf2, transparent: true, opacity: 0.55, side: THREE.DoubleSide });
  const wings = [-1, 1].map((s) => { const w = new THREE.Group(); w.position.set(0.05, 0.44, s * 0.05); const p = mesh(ICO1, wm, false); p.scale.set(0.32, 0.01, 0.12); p.position.set(-0.25, 0, s * 0.12); w.add(p); w.rotation.y = s * 0.35; body.add(w); return w; });
  const L = legs(body, dk, 3, 0.2, 0.2, 0.1, 0.36, 0.02, 0.7);
  g.userData = { body, legs: L, wings, ants: [] };
  return g;
}

// tiny eye chart on a stand (faces +z), 3 cm wide in world units when scale 1
export function makeEyeChart() {
  const tex = canvasTex(200, 260, (c, w, h) => {
    c.fillStyle = '#fbfbf6'; c.fillRect(0, 0, w, h); c.fillStyle = '#111'; c.textAlign = 'center';
    [['E', 80, 80], ['F P', 46, 132], ['T O Z', 32, 172], ['L P E D', 22, 204], ['P E C F D', 15, 228], ['E D F C Z P', 10, 246]].forEach(([s, px, y]) => { c.font = `900 ${px}px Inter`; c.fillText(s, w / 2, y); });
  });
  const g = new THREE.Group();
  const page = new THREE.Mesh(new THREE.PlaneGeometry(0.03, 0.039), new THREE.MeshLambertMaterial({ map: tex })); page.position.y = 0.0215; g.add(page);
  g.add(box(0.032, 0.041, 0.001, 0x6a4a30, 0, 0.001, -0.0007, false));
  const leg = box(0.002, 0.03, 0.002, 0x6a4a30, 0, 0, -0.008, false); leg.rotation.x = -0.35; g.add(leg);
  return g;
}

// flat ruler along +x, `n` body lengths of `unit` m, a label every 10 lengths ("10X" ... "40X")
export function makeRuler(n, unit) {
  const len = n * unit;
  const tex = canvasTex(2048, 64, (c, w, h) => {
    c.fillStyle = '#f2c94c'; c.fillRect(0, 0, w, h); c.fillStyle = '#1a1a1a';
    for (let i = 0; i <= n; i++) { const x = Math.min(w - 3, (i / n) * w); c.fillRect(x - 2, 0, 4, i % 10 ? 18 : 36); }
    c.font = '900 26px Inter'; c.textAlign = 'center';
    for (let i = 10; i <= n; i += 10) c.fillText(`${i}X`, Math.min(w - 32, (i / n) * w), 60);
  });
  tex.wrapS = tex.wrapT = THREE.ClampToEdgeWrapping;
  const g = new THREE.Group();
  const top = new THREE.Mesh(new THREE.PlaneGeometry(len, 0.018), new THREE.MeshLambertMaterial({ map: tex })); top.rotation.x = -Math.PI / 2; top.position.set(len / 2, 0.0021, 0); top.receiveShadow = true; g.add(top);
  g.add(box(len, 0.002, 0.018, 0xc9a43c, len / 2, 0, 0, false));
  return g;
}

// armchair, seat faces +z (back on the -z side)
export function makeArmchair(color = 0x7a9a6a) {
  const g = new THREE.Group(), m = mat(color), d = mat(0x5a3d26);
  g.add(box(0.72, 0.42, 0.7, m, 0, 0.08, 0), box(0.72, 0.5, 0.16, m, 0, 0.5, -0.27), box(0.12, 0.26, 0.7, m, -0.3, 0.5, 0), box(0.12, 0.26, 0.7, m, 0.3, 0.5, 0));
  g.add(box(0.5, 0.08, 0.5, mat(0x8fb07e), 0, 0.5, 0.06));
  for (const [x, z] of [[-0.3, -0.28], [0.3, -0.28], [-0.3, 0.28], [0.3, 0.28]]) g.add(box(0.05, 0.08, 0.05, d, x, 0, z));
  return g;
}

// a pleated curtain panel hanging from y = top, `w` wide, facing +z
export function makeCurtain(w, h, color = 0xe9d9a8) {
  const g = new THREE.Group(), m = mat(color), m2 = mat(new THREE.Color(color).multiplyScalar(0.86).getHex());
  const n = 7; for (let k = 0; k < n; k++) { const p = mesh(ICO1, k % 2 ? m : m2); p.scale.set(w / n * 0.62, h / 2, 0.04); p.position.set(-w / 2 + (k + 0.5) * w / n, -h / 2, 0.02 * (k % 2)); g.add(p); }
  const rod = cyl(0.012, 0.012, w + 0.2, 0x8a6a3a, 8); rod.rotation.z = Math.PI / 2; rod.position.y = 0.02; g.add(rod);
  return g;
}

// the view outside a sunny window: sky, sun, hills, a tree (MeshBasic plane, w x h)
export function makeOutside(w, h) {
  const tex = canvasTex(256, 256, (c, W, H) => {
    const sk = c.createLinearGradient(0, 0, 0, H); sk.addColorStop(0, '#5fb2ec'); sk.addColorStop(0.7, '#bfe4fa'); c.fillStyle = sk; c.fillRect(0, 0, W, H);
    c.fillStyle = '#fff7c8'; c.beginPath(); c.arc(190, 52, 22, 0, 7); c.fill();
    c.fillStyle = '#ffffff'; for (const [x, y, r] of [[60, 60, 16], [80, 54, 20], [102, 62, 14], [150, 110, 10], [166, 106, 13]]) { c.beginPath(); c.arc(x, y, r, 0, 7); c.fill(); }
    c.fillStyle = '#7cc46a'; c.beginPath(); c.moveTo(0, 190); c.quadraticCurveTo(90, 150, 170, 185); c.quadraticCurveTo(220, 168, 256, 178); c.lineTo(256, 256); c.lineTo(0, 256); c.fill();
    c.fillStyle = '#5aa34e'; c.fillRect(0, 215, W, 41);
    c.fillStyle = '#6b4a2e'; c.fillRect(48, 150, 10, 70); c.fillStyle = '#3f8f3c'; c.beginPath(); c.arc(53, 140, 30, 0, 7); c.fill(); c.beginPath(); c.arc(36, 156, 20, 0, 7); c.fill(); c.beginPath(); c.arc(72, 154, 22, 0, 7); c.fill();
  });
  tex.wrapS = tex.wrapT = THREE.ClampToEdgeWrapping;
  return new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tex }));
}

// ---------- dust mites ----------
// house dust mite (Dermatophagoides): pale cream, round, eight stubby legs, tiny mouthparts up front
export function makeDustMite() {
  const g = new THREE.Group(), body = new THREE.Group(); g.add(body);
  const cr = mat(0xeee2c4), lg = mat(0xd8c8a0);
  const b = mesh(ICO1, cr); b.scale.set(0.42, 0.26, 0.32); b.position.set(-0.05, 0.3, 0); body.add(b);
  for (const s of [-1, 1]) for (let k = 0; k < 3; k++) { const h = mesh(limbGeo(0.006, 0.003, 0.22, 3), lg, false); h.position.set(-0.3, 0.42, s * 0.12); h.rotation.set(-0.7, s > 0 ? -2.6 + k * 0.25 : 2.6 - k * 0.25 + Math.PI, 0); body.add(h); }
  const gn = mesh(ICO1, mat(0xc8a878)); gn.scale.set(0.1, 0.08, 0.1); gn.position.set(0.4, 0.26, 0); body.add(gn);
  const L = legs(body, lg, 4, 0.22, 0.24, 0.16, 0.4, 0.035, 0.75);
  g.userData = { body, legs: L, ants: [] };
  return g;
}
// a translucent skin flake (a thin irregular chip)
export function makeFlake(seed = 1) {
  const sh = new THREE.Shape(), n = 7;
  for (let k = 0; k < n; k++) { const a = k / n * Math.PI * 2, r = 0.5 + 0.3 * Math.sin(seed * 3.1 + k * 2.3); k ? sh.lineTo(r * Math.cos(a), r * Math.sin(a)) : sh.moveTo(r, 0); }
  const m = mesh(new THREE.ShapeGeometry(sh), new THREE.MeshLambertMaterial({ color: 0xf6ead8, transparent: true, opacity: 0.85, side: THREE.DoubleSide }), false);
  m.rotation.x = -Math.PI / 2;
  const g = new THREE.Group(); g.add(m); return g;
}
// fabric fibre (a woven-looking tube) along +x, length 1
export function makeFibre(color = 0xf1f3f6) {
  const pts = []; for (let i = 0; i <= 10; i++) pts.push(new THREE.Vector3(i / 10 - 0.5, 0.012 * Math.sin(i * 1.7), 0.01 * Math.cos(i * 1.3)));
  return mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 24, 0.012, 6), mat(color, { flatShading: false }));
}
// lab microscope (meters, ~0.35 tall), eyepiece toward -x
export function makeMicroscope() {
  const g = new THREE.Group(), w = mat(0xf2f2f2), k = mat(0x2a2a2e);
  g.add(box(0.16, 0.025, 0.12, w, 0, 0, 0));
  const arm = box(0.03, 0.26, 0.04, w, -0.05, 0.02, 0); arm.rotation.z = 0.15; g.add(arm);
  g.add(box(0.11, 0.008, 0.09, k, 0.02, 0.09, 0));
  const tube = cyl(0.02, 0.022, 0.16, w, 10); tube.position.set(0.0, 0.25, 0); tube.rotation.z = 0.5; g.add(tube);
  const ep = cyl(0.014, 0.014, 0.05, k, 10); ep.position.set(-0.05, 0.33, 0); ep.rotation.z = 0.5; g.add(ep);
  const obj = cyl(0.01, 0.008, 0.04, k, 8); obj.position.set(0.035, 0.155, 0); g.add(obj);
  return g;
}
