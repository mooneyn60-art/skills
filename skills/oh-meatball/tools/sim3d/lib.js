// Shared low-poly building blocks (all geometry procedural, made here: no third-party models).
import * as THREE from 'three';

const MATS = new Map();
// Lambert by default: SwiftShader (CPU WebGL) pays per pixel for PBR; ?pbr=1 restores MeshStandardMaterial.
export const PBR = new URLSearchParams(location.search).get('pbr') === '1';
export function mat(color, opts = {}) {
  const key = color + JSON.stringify(opts);
  if (!MATS.has(key)) {
    if (PBR) MATS.set(key, new THREE.MeshStandardMaterial({ color, flatShading: true, roughness: 0.85, metalness: 0, ...opts }));
    else { const { roughness, metalness, ...rest } = opts; MATS.set(key, new THREE.MeshLambertMaterial({ color, flatShading: true, ...rest })); }
  }
  return MATS.get(key);
}
export function texMat(map, opts = {}) { return PBR ? new THREE.MeshStandardMaterial({ map, roughness: 0.6, ...opts }) : new THREE.MeshLambertMaterial({ map, ...opts }); }
export const ICO = new THREE.IcosahedronGeometry(1, 0);
export const ICO1 = new THREE.IcosahedronGeometry(1, 1);
export const BOX = new THREE.BoxGeometry(1, 1, 1);
export function mesh(geo, m, shadow = true) {
  const o = new THREE.Mesh(geo, m);
  o.castShadow = shadow; o.receiveShadow = true;
  return o;
}
export function box(w, h, d, color, x = 0, y = 0, z = 0, shadow = true) {
  const o = mesh(BOX, typeof color === 'object' ? color : mat(color), shadow);
  o.scale.set(w, h, d); o.position.set(x, y + h / 2, z);
  return o;
}
export function cyl(rt, rb, h, color, seg = 7) {
  return mesh(new THREE.CylinderGeometry(rt, rb, h, seg), typeof color === 'object' ? color : mat(color));
}
// A limb whose geometry runs from its origin along +z (so rotations pivot at the joint).
export function limbGeo(r0, r1, len, seg = 5) {
  const g = new THREE.CylinderGeometry(r1, r0, len, seg, 1);
  g.rotateX(Math.PI / 2); g.translate(0, 0, len / 2);
  return g;
}

export function canvasTex(w, h, draw, rep = [1, 1]) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(rep[0], rep[1]); t.anisotropy = 8;
  return t;
}
export function tileTex(base, grout, n = 4, rep = [1, 1]) {
  return canvasTex(256, 256, (g, w) => {
    g.fillStyle = grout; g.fillRect(0, 0, w, w);
    const s = w / n;
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
      const v = ((i * 7 + j * 13) % 5) * 3;
      g.fillStyle = shade(base, v - 6); g.fillRect(i * s + 3, j * s + 3, s - 6, s - 6);
    }
  }, rep);
}
export function shade(hex, d) {
  const c = new THREE.Color(hex); const hsl = {}; c.getHSL(hsl);
  c.setHSL(hsl.h, hsl.s, Math.min(1, Math.max(0, hsl.l + d / 255)));
  return '#' + c.getHexString();
}

// ---------------- House centipede (Scutigera coleoptrata), body length = 1 unit ----------------
// 15 leg pairs (30 legs), long banded legs growing longer to the rear, very long antennae.
export function makeCentipede() {
  const root = new THREE.Group();
  const H = 0.045, N = 15, segLen = 0.82 / N;
  const cA = mat(0xb38a52), cB = mat(0x9a7444), cDark = mat(0x2e2219), cLeg = mat(0xdcc49a), cBand = mat(0x6e5236);
  const segs = [];
  for (let i = 0; i < N; i++) {
    const s = mesh(ICO, i % 2 ? cA : cB);
    const taper = 1 - Math.abs(i - 5) / 22;
    s.scale.set(segLen * 0.78, 0.022, 0.048 * taper);
    s.position.set(0.38 - i * segLen, H, 0);
    root.add(s); s.userData.rig = { s: 0.38 - i * segLen, off: new THREE.Vector3(0, 0, 0) };
    const stripe = mesh(ICO, cDark, false);
    stripe.scale.set(segLen * 0.55, 0.006, 0.014 * taper);
    stripe.position.set(0, 0.85, 0);
    stripe.scale.divide(s.scale);
    s.add(stripe);
    segs.push(s);
  }
  const head = mesh(ICO, cA); head.scale.set(0.05, 0.03, 0.046); head.position.set(0.45, H + 0.004, 0); root.add(head); head.userData.rig = { s: 0.45, off: new THREE.Vector3(0, 0.004, 0) };
  for (const sd of [-1, 1]) {
    const e = mesh(ICO, mat(0x111111, { roughness: 0.3 }), false);
    e.scale.set(0.014, 0.012, 0.012); e.position.set(0.47, H + 0.016, sd * 0.03); root.add(e); e.userData.rig = { s: 0.47, off: new THREE.Vector3(0, 0.016, sd * 0.03) };
  }
  const legs = [];
  for (let i = 0; i < N; i++) for (const side of [1, -1]) {
    const last = i === N - 1;
    const len = last ? 0.85 : 0.30 + 0.30 * (i / (N - 1));
    const fl = len * 0.4, tl = len * 0.6;
    const hip = new THREE.Group(); hip.position.set(0.38 - i * segLen, H, side * 0.02); hip.scale.z = side; hip.userData.rig = { s: 0.38 - i * segLen, off: new THREE.Vector3(0, 0, side * 0.02) };
    const yaw = new THREE.Group(), pitch = new THREE.Group(), knee = new THREE.Group();
    hip.add(yaw); yaw.add(pitch);
    const femur = mesh(limbGeo(0.0042, 0.0032, fl), cLeg); pitch.add(femur);
    knee.position.z = fl; pitch.add(knee);
    const t1 = mesh(limbGeo(0.0032, 0.0026, tl * 0.5), cBand); knee.add(t1);
    const t2 = mesh(limbGeo(0.0026, 0.001, tl * 0.5), cLeg); t2.position.z = tl * 0.5; knee.add(t2);
    root.add(hip);
    const alpha = last ? 0.18 : 0.72;
    const sb = Math.min(0.98, (H + fl * Math.sin(alpha)) / tl);
    const beta = last ? 0.06 : Math.asin(sb);
    legs.push({ i, side, yaw, pitch, knee, last, alpha, beta, baseYaw: last ? -1.25 : 0.55 - 1.15 * (i / (N - 1)) });
  }
  const ants = [];
  for (const side of [1, -1]) {
    let parent = new THREE.Group(); parent.position.set(0.49, H + 0.012, side * 0.012); parent.scale.z = side; root.add(parent); parent.userData.rig = { s: 0.49, off: new THREE.Vector3(0, 0.012, side * 0.012) };
    const chain = [];
    for (let k = 0; k < 9; k++) {
      const g = new THREE.Group();
      if (k > 0) g.position.z = 0.11;
      const m = mesh(limbGeo(0.003 - k * 0.00025, 0.0028 - k * 0.00025, 0.11, 4), k % 2 ? cBand : cLeg, k < 4);
      g.add(m); parent.add(g); chain.push(g); parent = g;
    }
    ants.push({ side, chain });
  }
  const rig = root.children.filter((o) => o.userData.rig);
  root.userData = { segs, legs, ants, H, segLen, rig };
  return root;
}

// Body axis: curve(s) -> { p, x, y } in body units (p = axis point at body height, x = tangent, y = dorsal up).
const _m = new THREE.Matrix4(), _z = new THREE.Vector3(), _v = new THREE.Vector3();
export const straightCurve = (H) => (s) => ({ p: new THREE.Vector3(s, H, 0), x: new THREE.Vector3(1, 0, 0), y: new THREE.Vector3(0, 1, 0) });
export function animateCentipede(c, t, freq, speedAmp = 1, curve = null) {
  const { segs, legs, ants, rig, H } = c.userData;
  const w = 2 * Math.PI * freq * t;
  const cv = curve || straightCurve(H);
  for (const o of rig) {
    const { s, off } = o.userData.rig, f = cv(s);
    const i = segs.indexOf(o), wig = i >= 0 ? 0.006 * speedAmp * Math.sin(w * 0.5 - i * 0.45) : 0;
    _z.crossVectors(f.x, f.y).normalize();
    o.position.copy(f.p).addScaledVector(f.x, off.x).addScaledVector(f.y, off.y).addScaledVector(_z, off.z + wig);
    _m.makeBasis(f.x, f.y, _z); o.quaternion.setFromRotationMatrix(_m);
  }
  for (const L of legs) {
    if (L.last) {
      L.yaw.rotation.y = L.baseYaw + 0.06 * Math.sin(w * 0.3);
      L.pitch.rotation.x = -L.alpha; L.knee.rotation.x = L.alpha + L.beta;
      continue;
    }
    const ph = w - L.i * 0.62 + (L.side < 0 ? Math.PI : 0);
    const lift = Math.max(0, Math.cos(ph)) * 0.38 * speedAmp;
    L.yaw.rotation.y = L.baseYaw + 0.3 * speedAmp * Math.sin(ph);
    L.pitch.rotation.x = -(L.alpha + lift);
    L.knee.rotation.x = L.alpha + L.beta;
  }
  for (const A of ants) A.chain.forEach((g, k) => {
    if (k === 0) { g.rotation.y = 0.42; g.rotation.x = -0.32 + 0.05 * Math.sin(t * 2.1 + A.side); }
    else { g.rotation.x = 0.045 + 0.03 * Math.sin(t * 1.7 + k * 0.6 + A.side); g.rotation.y = -0.03 + 0.04 * Math.sin(t * 1.3 + k); }
  });
}

// ---------------- Supporting cast ----------------
export function makeRoach() { // ~1.3 cm German cockroach, length 1 unit
  const g = new THREE.Group();
  const b = mesh(ICO1, mat(0x6b3a1c, { roughness: 0.4 })); b.scale.set(0.5, 0.16, 0.24); b.position.y = 0.2; g.add(b);
  const h = mesh(ICO, mat(0x8a5a30)); h.scale.set(0.12, 0.1, 0.15); h.position.set(0.48, 0.18, 0); g.add(h);
  for (const s of [-1, 1]) for (let k = 0; k < 3; k++) {
    const l = mesh(limbGeo(0.02, 0.012, 0.42, 4), mat(0x4a2812)); l.position.set(0.2 - k * 0.2, 0.17, s * 0.15);
    l.rotation.order = 'YXZ'; l.rotation.y = s > 0 ? (k - 1) * 0.6 : Math.PI - (k - 1) * 0.6; l.rotation.x = 0.5; g.add(l);
  }
  for (const s of [-1, 1]) { const a = mesh(limbGeo(0.012, 0.006, 0.7, 3), mat(0x4a2812), false); a.position.set(0.55, 0.22, s * 0.05); a.rotation.y = Math.PI / 2 - s * 0.35; a.rotation.x = -0.2; g.add(a); }
  return g;
}

export function makeCat() { // ~0.5 m orange tabby, faces +x
  const g = new THREE.Group(), fur = mat(0xd98a3a), dk = mat(0xa85f22), wh = mat(0xf2e3cf);
  const b = mesh(ICO1, fur); b.scale.set(0.24, 0.11, 0.1); b.position.set(0, 0.22, 0); g.add(b);
  const head = mesh(ICO1, fur); head.scale.set(0.085, 0.08, 0.085); head.position.set(0.25, 0.32, 0); g.add(head);
  const muz = mesh(ICO, wh); muz.scale.set(0.04, 0.03, 0.045); muz.position.set(0.32, 0.29, 0); g.add(muz);
  for (const s of [-1, 1]) {
    const ear = mesh(new THREE.ConeGeometry(0.03, 0.06, 4), dk); ear.position.set(0.24, 0.41, s * 0.045); g.add(ear);
    const eye = mesh(ICO, mat(0x2b3a10, { roughness: 0.2 }), false); eye.scale.set(0.012, 0.016, 0.012); eye.position.set(0.325, 0.34, s * 0.035); g.add(eye);
    for (const fx of [0.15, -0.15]) { const l = mesh(limbGeo(0.025, 0.02, 0.18, 5), fur); l.position.set(fx, 0.18, s * 0.06); l.rotation.x = Math.PI / 2; g.add(l); }
  }
  let p = g; for (let k = 0; k < 5; k++) {
    const seg = new THREE.Group(); seg.position.copy(k === 0 ? new THREE.Vector3(-0.22, 0.25, 0) : new THREE.Vector3(0, 0, 0.06));
    if (k === 0) seg.rotation.y = -Math.PI / 2;
    seg.rotation.x = -0.32;
    seg.add(mesh(limbGeo(0.02, 0.017, 0.065, 5), k % 2 ? dk : fur)); p.add(seg); p = seg;
  }
  return g;
}

export function makeHuman(shirt = 0x2f3d6b) { // 1.75 m, faces +x
  const g = new THREE.Group(), skin = mat(0xe0ac85), pants = mat(0x2a2a33), hair = mat(0x3b2618);
  const parts = {};
  for (const s of [-1, 1]) {
    const hip = new THREE.Group(); hip.position.set(0, 0.92, s * 0.1); g.add(hip);
    const leg = mesh(limbGeo(0.075, 0.06, 0.88, 6), pants); leg.rotation.x = Math.PI / 2; hip.add(leg);
    const shoe = box(0.26, 0.08, 0.11, 0x1c1c1c, 0.05, -0.92, 0); hip.add(shoe);
    const sh = new THREE.Group(); sh.position.set(0, 1.45, s * 0.24); g.add(sh);
    const arm = mesh(limbGeo(0.055, 0.045, 0.62, 6), mat(shirt)); arm.rotation.x = Math.PI / 2; sh.add(arm);
    const hand = mesh(ICO, skin); hand.scale.setScalar(0.055); hand.position.y = -0.66; sh.add(hand);
    parts[s > 0 ? 'hipR' : 'hipL'] = hip; parts[s > 0 ? 'shR' : 'shL'] = sh;
  }
  const torso = mesh(BOX, mat(shirt)); torso.scale.set(0.24, 0.6, 0.42); torso.position.y = 1.22; g.add(torso);
  const neck = cyl(0.05, 0.05, 0.1, skin); neck.position.y = 1.56; g.add(neck);
  const head = mesh(ICO1, skin); head.scale.set(0.11, 0.13, 0.1); head.position.y = 1.68; g.add(head);
  const hr = mesh(ICO1, hair); hr.scale.set(0.115, 0.08, 0.105); hr.position.set(-0.015, 1.75, 0); g.add(hr);
  g.userData = parts;
  return g;
}
export function poseWalk(h, t, amp) {
  const { hipL, hipR, shL, shR } = h.userData, s = Math.sin(t);
  hipL.rotation.z = s * amp; hipR.rotation.z = -s * amp; shL.rotation.z = -s * amp * 0.8; shR.rotation.z = s * amp * 0.8;
}

// ---------------- Bathroom + house interior (house footprint x[-1.2,8.8] z[-0.9,7.1]) ----------------
// Walls are inward-facing planes (dollhouse trick): seen from inside, culled from outside.
export function wallPlane(len, h, m, x, z, rotY, y0 = 0) {
  const p = new THREE.Mesh(new THREE.PlaneGeometry(len, h), m);
  p.position.set(x, y0 + h / 2, z); p.rotation.y = rotY; p.receiveShadow = true;
  return p;
}
export function makeBathroom() {
  const g = new THREE.Group();
  const tile = texMat(tileTex('#eef1f2', '#b9c2c6', 4, [12, 12]));
  const fl = new THREE.Mesh(new THREE.PlaneGeometry(2.6, 2.3), tile); fl.rotation.x = -Math.PI / 2; fl.position.set(0.1, 0.002, 0.25); fl.receiveShadow = true; g.add(fl);
  const white = mat(0xf4f4f2, { roughness: 0.25 }), chrome = mat(0xc8ccd0, { roughness: 0.2, metalness: 0.6 });
  const toilet = new THREE.Group();
  const base = cyl(0.11, 0.14, 0.3, white, 16); base.position.y = 0.15; toilet.add(base);
  const bowl = cyl(0.2, 0.14, 0.14, white, 16); bowl.scale.set(1, 1, 1.3); bowl.position.set(0, 0.36, 0.06); toilet.add(bowl);
  const seat = cyl(0.21, 0.21, 0.03, mat(0xfafafa, { roughness: 0.3 }), 16); seat.scale.set(1, 1, 1.3); seat.position.set(0, 0.445, 0.06); toilet.add(seat);
  toilet.add(box(0.44, 0.38, 0.2, white, 0, 0.42, -0.2));
  toilet.add(box(0.47, 0.04, 0.22, white, 0, 0.8, -0.2));
  toilet.add(box(0.06, 0.02, 0.03, chrome, 0.17, 0.75, -0.08));
  toilet.position.set(0.12, 0, -0.5); toilet.userData.h = 0.85; g.add(toilet);
  const tub = new THREE.Group();
  tub.add(box(0.75, 0.55, 1.6, white, 0, 0, 0));
  const water = box(0.62, 0.02, 1.46, mat(0xbfe3ef, { roughness: 0.1 }), 0, 0.52, 0, false); tub.add(water);
  tub.add(box(0.05, 0.05, 0.18, chrome, 0, 0.8, -0.72));
  tub.position.set(-0.82, 0, -0.08); tub.userData.h = 0.6; g.add(tub);
  const sink = new THREE.Group();
  sink.add(box(0.6, 0.82, 0.45, mat(0x6f8fa3), 0, 0, 0));
  sink.add(box(0.64, 0.06, 0.5, white, 0, 0.82, 0));
  sink.add(box(0.03, 0.18, 0.03, chrome, 0, 0.88, -0.17));
  sink.position.set(0.85, 0, 1.12); sink.userData.h = 0.9; g.add(sink);
  const mirror = box(0.55, 0.7, 0.02, mat(0xd6e6ee, { roughness: 0.05, metalness: 0.4 }), 0.85, 1.25, 1.38, false); mirror.userData.h = 2; g.add(mirror);
  const rug = box(0.7, 0.012, 0.5, mat(0x5c8f8a), 0.3, 0, 0.35, false); rug.userData.h = 0.4; g.add(rug);
  const towel = box(0.05, 0.6, 0.45, mat(0xe5b45a), 1.36, 0.8, 0.45); towel.userData.h = 1.5; g.add(towel);
  const plant = new THREE.Group(); plant.add(cyl(0.08, 0.06, 0.16, mat(0xb86a45), 7));
  const lv = mesh(ICO, mat(0x4f8a46)); lv.scale.set(0.14, 0.2, 0.14); lv.position.y = 0.26; plant.add(lv); plant.children[0].position.y = 0.08;
  plant.position.set(-1.0, 0.55, 0.85); plant.userData.h = 0.5; g.add(plant);
  g.userData.props = [toilet, tub, sink, mirror, rug, towel, plant];
  return g;
}

// Interior partitions + furniture of the rest of the house (crumble when outgrown).
export function makeInterior() {
  const g = new THREE.Group();
  const wood = texMat(canvasTex(256, 256, (c, w) => {
    for (let i = 0; i < 8; i++) { c.fillStyle = shade('#b07a4a', ((i * 37) % 9) - 4); c.fillRect(0, i * 32, w, 31); c.fillStyle = '#7c5232'; c.fillRect(0, i * 32 + 31, w, 1); }
  }, [6, 6]));
  const fl = new THREE.Mesh(new THREE.PlaneGeometry(10, 8), wood); fl.rotation.x = -Math.PI / 2; fl.position.set(3.8, 0.001, 3.1); fl.receiveShadow = true; g.add(fl);
  const paint = mat(0xe9e1d3, { flatShading: false }), btile = texMat(tileTex('#cfe3e3', '#9fb5b5', 3, [6, 3]));
  const parts = [];
  const add = (o, h) => { o.userData.h = h; g.add(o); parts.push(o); };
  // bathroom walls (x=1.4 with a door gap z[-0.85,-0.05]; z=1.4)
  add(wallPlane(1.45, 2.6, btile, 1.4, 0.675, -Math.PI / 2), 2.6);
  add(wallPlane(0.8, 0.5, btile, 1.4, -0.45, -Math.PI / 2, 2.1), 2.6);
  add(wallPlane(2.6, 2.6, btile, 0.1, 1.4, Math.PI), 2.6);
  // hallway wall z=0.8 x[1.4,8.8] with two doors
  add(wallPlane(1.6, 2.6, paint, 2.2, 0.8, Math.PI), 2.6);
  add(wallPlane(3.0, 2.6, paint, 5.0, 0.8, Math.PI), 2.6);
  add(wallPlane(1.0, 2.6, paint, 8.3, 0.8, Math.PI), 2.6);
  // living room furniture
  const sofa = new THREE.Group(); sofa.add(box(2.2, 0.45, 0.9, 0x55708a, 0, 0, 0)); sofa.add(box(2.2, 0.5, 0.25, 0x4a627a, 0, 0.45, -0.33));
  sofa.position.set(4.5, 0, 5.8); add(sofa, 1);
  add(box(1.2, 0.4, 0.6, 0x8a5a36, 4.5, 0, 4.4), 0.5);
  add(box(2.6, 0.01, 1.8, 0xc9b28a, 4.5, 0, 4.6, false), 0.4);
  const lamp = new THREE.Group(); lamp.add(cyl(0.02, 0.02, 1.5, 0x333333, 5)); lamp.children[0].position.y = 0.75;
  const shadeM = cyl(0.14, 0.22, 0.25, 0xf3e3b5, 8); shadeM.position.y = 1.55; lamp.add(shadeM); lamp.position.set(6.2, 0, 6.3); add(lamp, 1.7);
  const tv = box(1.4, 0.8, 0.06, 0x111418, 4.5, 0.9, 1.0); add(tv, 1.8);
  add(box(1.6, 0.6, 0.4, 0x6e4a2e, 4.5, 0, 1.05), 0.8);
  add(box(0.9, 1.9, 0.5, 0x8c6b4a, 8.3, 0, 2.2), 2);
  g.userData.parts = parts;
  return g;
}

// Outer shell of the house: inner faces (always) + outer skin (enabled when it leaves the ground).
export function makeHouseShell() {
  const g = new THREE.Group();
  const inner = mat(0xf1ead9, { flatShading: false }), outer = mat(0xd9c7a3), roofM = mat(0x8e4a3a), trim = mat(0xffffff);
  const W = 10, D = 8, Hh = 2.7, cx = 3.8, cz = 3.1;
  const innerG = new THREE.Group(), outerG = new THREE.Group();
  innerG.add(wallPlane(W, Hh, inner, cx, cz - D / 2, 0));
  innerG.add(wallPlane(W, Hh, inner, cx, cz + D / 2, Math.PI));
  innerG.add(wallPlane(D, Hh, inner, cx - W / 2, cz, Math.PI / 2));
  innerG.add(wallPlane(D, Hh, inner, cx + W / 2, cz, -Math.PI / 2));
  const ceil = new THREE.Mesh(new THREE.PlaneGeometry(W, D), inner); ceil.rotation.x = Math.PI / 2; ceil.position.set(cx, Hh, cz); innerG.add(ceil);
  const body = box(W + 0.1, Hh, D + 0.1, outer, cx, 0, cz); outerG.add(body);
  const roofGeo = new THREE.CylinderGeometry(1, 1, 1, 3, 1); roofGeo.rotateY(Math.PI / 2); roofGeo.rotateZ(Math.PI / 2);
  const roof = mesh(roofGeo, roofM); roof.scale.set(W + 0.6, 1.4, 4.94);
  roof.position.set(cx, Hh + 0.7, cz); outerG.add(roof);
  for (let i = 0; i < 4; i++) outerG.add(box(1.0, 1.1, 0.06, mat(0x9fc3d8, { roughness: 0.1 }), cx - 3.6 + i * 2.4, 0.9, cz + D / 2 + 0.06, false));
  outerG.add(box(1.0, 2.0, 0.08, mat(0x6a3d2a), cx + 1.2, 0, cz + D / 2 + 0.07, false));
  outerG.add(box(0.5, 1.3, 0.5, 0x7a6a62, cx + 3, Hh + 0.9, cz - 1));
  outerG.visible = false;
  g.add(innerG, outerG);
  g.userData = { innerG, outerG, center: new THREE.Vector3(cx, 0, cz) };
  return g;
}
