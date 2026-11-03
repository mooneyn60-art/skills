// Outdoor world from street to stratosphere: suburb, city (instanced), countryside, clouds, dust.
import * as THREE from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { mat, texMat, mesh, box, cyl, ICO, BOX, canvasTex, shade, PBR } from './lib.js';

export function rng(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }

export function makeGround() {
  const g = new THREE.Group();
  const grass = new THREE.Mesh(new THREE.CircleGeometry(4.0e6, 64), mat(0x86a35f, { flatShading: false, roughness: 1 }));
  grass.rotation.x = -Math.PI / 2; grass.position.y = -0.03; grass.receiveShadow = true; g.add(grass);
  const road = mat(0x55585e, { flatShading: false, roughness: 0.95 });
  const strip = (w, d, x, z) => { const r = new THREE.Mesh(new THREE.PlaneGeometry(w, d), road); r.rotation.x = -Math.PI / 2; r.position.set(x, -0.01, z); r.receiveShadow = true; g.add(r); };
  // suburb street grid in front/behind the house, then the city grid
  for (const z of [14, -40, 68, -94, 122]) strip(5000, 8, 2300, z);
  for (let x = 240; x < 4800; x += 60) strip(8, 4600, x + 26, 0);
  const dash = mat(0xf2d35a, { flatShading: false });
  for (let x = -40; x < 300; x += 6) { const d = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 0.18), dash); d.rotation.x = -Math.PI / 2; d.position.set(x, -0.005, 14); g.add(d); }
  return g;
}

// Suburb: individual low-poly houses, trees, lamp posts, parked cars (each can crumble).
export function makeSuburb() {
  const g = new THREE.Group(), items = [], r = rng(7);
  const roofC = [0x8e4a3a, 0x5d6670, 0x7a3e2e, 0x4f5a4a, 0x9a6a3a], wallC = [0xe6d7b8, 0xc9d6dc, 0xf0e6d2, 0xd8b99a, 0xbfcfb3, 0xe8c9c0];
  const roofGeo = new THREE.CylinderGeometry(1, 1, 1, 3, 1); roofGeo.rotateY(Math.PI / 2); roofGeo.rotateZ(Math.PI / 2);
  const add = (o, h, kind = 'b') => { o.userData.h = h; o.userData.kind = kind; g.add(o); items.push(o); };
  for (const zr of [3, -14, 28, 54, -66, 82, -108, 108]) for (let x = -50; x < 95; x += 13 + r() * 4) {
    if (x > -14 && x < 17 && zr === 3) continue; // our lot
    const w = 8 + r() * 3, d = 7 + r() * 2, h = 2.8 + (r() < 0.3 ? 2.7 : 0);
    const hs = new THREE.Group();
    hs.add(box(w, h, d, wallC[(r() * wallC.length) | 0], 0, 0, 0));
    const rf = mesh(roofGeo, mat(roofC[(r() * roofC.length) | 0])); rf.scale.set(w + 0.6, 1.3, d * 0.62); rf.position.y = h + 0.65; hs.add(rf);
    hs.add(box(1, 2, 0.1, 0x6a3d2a, 0, 0, d / 2 + 0.03, false));
    for (const s of [-1, 1]) hs.add(box(1.1, 1, 0.08, mat(0x9fc3d8, { roughness: 0.15 }), s * w * 0.28, 1.0, d / 2 + 0.03, false));
    hs.position.set(x, 0, zr + (zr > 0 ? 6 : -6) * 0 + (r() - 0.5) * 2); hs.rotation.y = (zr > 14 ? Math.PI : 0);
    add(hs, h + 1.3);
    if (r() < 0.8) { const tr = tree(r); tr.position.set(x + 6.5, 0, zr + (r() - 0.5) * 8); add(tr, tr.userData.h, 't'); }
  }
  for (let x = -40; x < 100; x += 22) for (const z of [9.5, 18.5]) {
    const lp = new THREE.Group(); const p = cyl(0.08, 0.1, 5, 0x3c4048, 5); p.position.y = 2.5; lp.add(p);
    lp.add(box(0.9, 0.12, 0.2, 0x3c4048, 0.4, 4.9, 0)); lp.position.set(x, 0, z); add(lp, 5, 'p');
  }
  return { g, items };
}
export function tree(r) {
  const t = new THREE.Group(), h = 4 + r() * 4;
  const tr = cyl(0.15, 0.22, h * 0.45, 0x6b4a2e, 5); tr.position.y = h * 0.22; t.add(tr);
  const c = mesh(ICO, mat([0x4f8a46, 0x5f9a4c, 0x3f7a3e][(r() * 3) | 0])); c.scale.set(h * 0.32, h * 0.38, h * 0.32); c.position.y = h * 0.66; t.add(c);
  t.userData.h = h; return t;
}

// Cars: one InstancedMesh (body) + cabin; driving along the x-streets.
export function makeCars(n = 260) {
  const r = rng(11), body = new THREE.InstancedMesh(BOX, mat(0xffffff, { roughness: 0.4 }), n), cab = new THREE.InstancedMesh(BOX, mat(0x2a3440, { roughness: 0.2 }), n);
  body.castShadow = cab.castShadow = true; body.receiveShadow = true;
  const cols = [0xd23b2f, 0x2f6fd2, 0xf2f2f2, 0x222222, 0xe8b63a, 0x3f9a5a, 0x9aa3ad];
  const cars = [];
  for (let i = 0; i < n; i++) {
    const lane = [14, -40, 68, -94, 122][i % 5] + (r() < 0.5 ? -2 : 2);
    cars.push({ x0: -80 + r() * 4500, z: lane, v: (lane % 2 ? 1 : -1) * (6 + r() * 6), dir: 0 });
    body.setColorAt(i, new THREE.Color(cols[(r() * cols.length) | 0]));
  }
  return { body, cab, cars };
}

const WIN = canvasTex(64, 128, (c, w, h) => {
  c.fillStyle = '#f4f1ea'; c.fillRect(0, 0, w, h);
  for (let y = 4; y < h - 4; y += 8) for (let x = 4; x < w - 4; x += 8) { c.fillStyle = ((x * 3 + y * 7) % 23) < 3 ? '#e9d79a' : '#4b6378'; c.fillRect(x, y, 5, 5); }
});
// City: instanced towers; per-instance base matrix kept so towers can be crushed.
export const TOWER = { x: 430, z: 45, h: 640 };
export function makeCity() {
  const r = rng(23), towers = [];
  for (let x = 110; x < 3600; x += 85) for (let z = -1700; z < 1700; z += 85) {
    if (Math.abs(z - 14) < 30) continue;
    for (let k = 0; k < 2; k++) {
      if (r() < 0.35) continue;
      const cx = x + 10 + k * 36 + r() * 6, cz = z + 10 + r() * 40;
      if (Math.hypot(cx - TOWER.x, cz - TOWER.z) < 70) continue;
      const center = Math.exp(-(((x - 700) / 900) ** 2) - ((z / 900) ** 2));
      const h = 14 + Math.pow(r(), 2.2) * 45 + center * Math.pow(r(), 1.3) * 300;
      towers.push({ x: cx, z: cz, w: 18 + r() * 12, d: 18 + r() * 12, h, c: new THREE.Color().setHSL(0.08 + r() * 0.5, 0.12 + r() * 0.15, 0.55 + r() * 0.25) });
    }
  }
  const im = new THREE.InstancedMesh(BOX, texMat(WIN, { flatShading: true }), towers.length);
  im.castShadow = true; im.receiveShadow = true;
  const m = new THREE.Matrix4();
  towers.forEach((t, i) => { m.compose(new THREE.Vector3(t.x, t.h / 2, t.z), new THREE.Quaternion(), new THREE.Vector3(t.w, t.h, t.d)); im.setMatrixAt(i, m); im.setColorAt(i, t.c); });
  return { im, towers };
}

// Countryside at km scale: field patches, lakes, mountains.
export function makeLand() {
  const r = rng(5), g = new THREE.Group(), n = 2600;
  const im = new THREE.InstancedMesh(BOX, mat(0xffffff, { flatShading: true, roughness: 1 }), n); im.receiveShadow = true;
  const m = new THREE.Matrix4(), q = new THREE.Quaternion(), cols = [0x7fa356, 0x9bb862, 0x6f9448, 0xc8b56a, 0x8aa85a, 0xa7a35a];
  for (let i = 0; i < n; i++) {
    const a = r() * Math.PI * 2, d = 5000 + Math.pow(r(), 0.7) * 260000, s = 600 + r() * 3500 * (d / 60000 + 0.3);
    q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), r() * 3);
    m.compose(new THREE.Vector3(2000 + Math.cos(a) * d, -0.02 + r() * 0.01, Math.sin(a) * d), q, new THREE.Vector3(s, 0.02, s * (0.5 + r())));
    im.setMatrixAt(i, m); im.setColorAt(i, new THREE.Color(cols[(r() * cols.length) | 0]));
  }
  g.add(im);
  const lake = mat(0x4f86b8, { roughness: 0.2, flatShading: false });
  for (let i = 0; i < 40; i++) { const a = r() * 6.28, d = 8000 + r() * 200000, l = new THREE.Mesh(new THREE.CircleGeometry(1, 7), lake); l.scale.set(800 + r() * 5000, 800 + r() * 4000, 1); l.rotation.x = -Math.PI / 2; l.position.set(Math.cos(a) * d, 0.0, Math.sin(a) * d); g.add(l); }
  const mtn = new THREE.ConeGeometry(1, 1, 6, 1);
  for (let i = 0; i < 70; i++) {
    const a = r() * 6.28, d = 30000 + r() * 250000, h = 1500 + r() * 4000;
    const mm = mesh(mtn, mat(r() < 0.5 ? 0x6f7d5a : 0x7d7a66), false); mm.scale.set(h * (1.5 + r()), h, h * (1.5 + r())); mm.position.set(Math.cos(a) * d, h / 2, Math.sin(a) * d); mm.rotation.y = r() * 3; g.add(mm);
    if (h > 3500) { const cap = mesh(mtn, mat(0xf4f6f8), false); cap.scale.set(mm.scale.x * 0.28, h * 0.28, mm.scale.z * 0.28); cap.position.set(mm.position.x, h * 0.86, mm.position.z); cap.rotation.y = mm.rotation.y; g.add(cap); }
  }
  return g;
}

export function makeClouds(n = 420) {
  const r = rng(3), parts = [];
  for (let k = 0; k < 7; k++) { const p = new THREE.IcosahedronGeometry(1, 0); const s = 0.5 + r() * 0.6; p.scale(s * 1.3, s * 0.8, s); p.translate((r() - 0.5) * 2.2, (r() - 0.3) * 0.6, (r() - 0.5) * 1.2); parts.push(p); }
  const geo = mergeGeometries(parts);
  const im = new THREE.InstancedMesh(geo, mat(0xffffff, { emissive: 0x6d7f95, emissiveIntensity: 0.35, transparent: true }), n);
  im.castShadow = false;
  const m = new THREE.Matrix4(), q = new THREE.Quaternion();
  for (let i = 0; i < n; i++) {
    const a = r() * 6.28, d = 6500 + Math.pow(r(), 0.8) * 70000, s = 300 + r() * 1000 + d * 0.012;
    q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), r() * 6);
    m.compose(new THREE.Vector3(2000 + Math.cos(a) * d, 900 + r() * 900, Math.sin(a) * d), q, new THREE.Vector3(s, s * 0.6, s)); im.setMatrixAt(i, m);
  }
  return im;
}

// Dust puffs for crumbling things; events {p, s, t0}.
export function makeDust(max = 900) {
  const im = new THREE.InstancedMesh(ICO, mat(0xcdb894, { roughness: 1 }), max); im.frustumCulled = false;
  const m = new THREE.Matrix4(), q = new THREE.Quaternion(), zero = new THREE.Matrix4().makeScale(0, 0, 0);
  function update(events, t) {
    let k = 0;
    for (const e of events) {
      const age = t - e.t0; if (age < 0 || age > 2.2) continue;
      const rr = rng(e.seed);
      for (let j = 0; j < 7 && k < max; j++, k++) {
        const a = rr() * 6.28, up = rr();
        const sp = e.s * (0.35 + 0.5 * rr()) * (1 - Math.exp(-age * 2.2));
        const sc = e.s * (0.18 + 0.2 * rr()) * Math.min(1, age * 4) * Math.max(0, 1 - age / 2.2);
        q.setFromAxisAngle(new THREE.Vector3(rr(), rr(), rr()).normalize(), age + j);
        m.compose(new THREE.Vector3(e.p.x + Math.cos(a) * sp, e.p.y + e.s * 0.15 + up * sp * 0.5, e.p.z + Math.sin(a) * sp), q, new THREE.Vector3(sc, sc * 0.8, sc));
        im.setMatrixAt(k, m);
      }
    }
    for (; k < max; k++) im.setMatrixAt(k, zero);
    im.instanceMatrix.needsUpdate = true;
  }
  return { im, update };
}

// The supertall the centipede climbs: stacked, tapering low-poly blocks + spire.
export function makeSupertall() {
  const g = new THREE.Group(), glass = texMat(WIN, { color: 0xbfd3e6 }), steel = mat(0x8c99a6);
  let y = 0, w = 64;
  for (const [hh, ww] of [[200, 64], [160, 52], [120, 40], [80, 30], [40, 20]]) {
    const b = new THREE.Mesh(BOX, glass); b.scale.set(ww, hh, ww); b.position.y = y + hh / 2; b.castShadow = b.receiveShadow = true; g.add(b);
    const ring = new THREE.Mesh(BOX, steel); ring.scale.set(ww + 4, 4, ww + 4); ring.position.y = y + hh; g.add(ring);
    y += hh;
  }
  const spire = new THREE.Mesh(new THREE.ConeGeometry(5, 60, 6), steel); spire.position.y = y + 30; spire.castShadow = true; g.add(spire);
  g.position.set(TOWER.x, 0, TOWER.z); g.userData.h = y + 60;
  return g;
}

// Earth for the orbit act: faceted icosphere with noise continents, a cloud deck, glow, stars and a Moon.
export const R_EARTH = 6371000;
function vnoise(x, y, z) { // cheap smooth-ish 3D noise from sines
  return Math.sin(x * 1.7 + Math.sin(y * 2.3)) * Math.cos(y * 1.9 + z * 0.7) + 0.5 * Math.sin(z * 3.1 + x * 2.2) * Math.cos(x * 2.9 - y * 1.3) + 0.25 * Math.sin(x * 6.3 + y * 5.1 + z * 4.7);
}
export function makeEarth() {
  const g = new THREE.Group();
  const geo = new THREE.IcosahedronGeometry(R_EARTH, 5), pos = geo.attributes.position, col = new Float32Array(pos.count * 3);
  const c = new THREE.Color(), v = new THREE.Vector3();
  for (let i = 0; i < pos.count; i += 3) {
    v.set(0, 0, 0); for (let k = 0; k < 3; k++) v.add(new THREE.Vector3().fromBufferAttribute(pos, i + k)); v.normalize();
    const lat = Math.abs(v.z), n = vnoise(v.x * 2.2, v.y * 2.2, v.z * 2.2) + (v.y > 0.97 ? 2 : 0); // poles on ±z: we stand at +y
    if (v.y > 0.97) c.set([0x6f9a4c, 0x7fa356, 0x8aa85a][(i / 3) % 3]);
    else if (Math.abs(v.z) > 0.93) c.set(0xf2f5f8);
    else if (n > 0.15) c.set(lat < 0.3 && n > 0.6 ? 0xc8b06a : n > 0.9 ? 0x7c8a5a : 0x6f9a4c);
    else c.set(n > -0.05 ? 0x3f86c4 : 0x2c6aa8);
    for (let k = 0; k < 3; k++) col.set([c.r, c.g, c.b], (i + k) * 3);
  }
  geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
  const earth = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ vertexColors: true, flatShading: true }));
  earth.receiveShadow = true; g.add(earth);
  const r = rng(77), n = 700, cl = new THREE.InstancedMesh(ICO, mat(0xffffff, { emissive: 0x8090a0, emissiveIntensity: 0.3 }), n);
  const m = new THREE.Matrix4(), q = new THREE.Quaternion(), up = new THREE.Vector3(0, 1, 0);
  for (let i = 0; i < n; i++) {
    v.set(r() * 2 - 1, r() * 2 - 1, r() * 2 - 1).normalize();
    if (v.y > 0.995) v.set(0.3, 0.9, 0.3).normalize();
    q.setFromUnitVectors(up, v); const s = 60000 + r() * 180000;
    m.compose(v.clone().multiplyScalar(R_EARTH + 9000), q, new THREE.Vector3(s, 6000, s * (0.4 + r() * 0.6))); cl.setMatrixAt(i, m);
  }
  g.add(cl);
  const glow = new THREE.Mesh(new THREE.IcosahedronGeometry(R_EARTH * 1.03, 3), new THREE.MeshBasicMaterial({ color: 0x6fb3ff, transparent: true, opacity: 0.28, side: THREE.BackSide, depthWrite: false }));
  g.add(glow);
  g.position.set(0, -R_EARTH, 0);
  return g;
}
export function makeStars(n = 1400) {
  const r = rng(9), p = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) { const v = new THREE.Vector3(r() * 2 - 1, r() * 2 - 1, r() * 2 - 1).normalize(); p.set([v.x, v.y, v.z], i * 3); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(p, 3));
  return new THREE.Points(g, new THREE.PointsMaterial({ color: 0xffffff, size: 2.2, sizeAttenuation: false, transparent: true, opacity: 0, depthWrite: false, fog: false }));
}
export function makeMoon() {
  const m = new THREE.Mesh(new THREE.IcosahedronGeometry(1737000, 2), mat(0xc9c9c4));
  m.position.set(-26e6, 14e6, -40e6); return m;
}
export function makeHeroCar() {
  const g = new THREE.Group();
  g.add(box(4.4, 0.9, 1.9, 0xd23b2f, 0, 0.35, 0)); g.add(box(2.3, 0.65, 1.7, 0x2a3440, -0.2, 1.25, 0));
  for (const x of [-1.4, 1.4]) for (const z of [-0.95, 0.95]) { const w = cyl(0.36, 0.36, 0.25, 0x1a1a1a, 8); w.rotation.x = Math.PI / 2; w.position.set(x, 0.36, z); g.add(w); }
  return g;
}
