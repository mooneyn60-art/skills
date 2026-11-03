// "What if a house centipede doubled in size every 2 seconds?" Deterministic: SIM.render(t) is a pure function of t.
// Fast defaults (measured on a loaded 4-core box, SwiftShader): 3D at 540x960 (px=0.5) upscaled in a 2D compositor
// that draws the text at 1080x1920, Lambert materials, 1024 PCF shadow map, no log-depth (dynamic near/far),
// size-band culling of every world layer. Query overrides: ?px=0.6667&aa=0&shadow=2048&soft=1&pbr=1&logz=1.
import * as THREE from 'three';
import { mat, makeCentipede, animateCentipede, makeRoach, makeCat, makeHuman, poseWalk, makeBathroom, makeInterior, makeHouseShell } from './lib.js';
import { makeCompositor, richText, shadowOn, shadowOff } from './overlay2d.js';
import { makeGround, makeSuburb, makeCars, makeCity, makeLand, makeClouds, makeDust, makeSupertall, TOWER, makeEarth, makeStars, makeMoon, makeHeroCar, R_EARTH } from './world.js';

export const BEATS = [
  [0.0, '2 cm. Hiding behind your toilet.', 'HERO0'],
  [3.2, 'It eats the roaches.', 'FRONT'],
  [6.6, 'Every 2 seconds, it doubles.', 'TOP'],
  [10.0, "Now it's the size of your cat.", 'A'],
  [13.2, '30 legs. Each one taller than you.', 'HUMAN'],
  [16.6, 'Your house is its shell now.', 'WIDE'],
  [20.0, 'Cars become toys.', 'CAR'],
  [23.2, "It hunts the city's roaches.", 'FRONT'],
  [26.4, 'It climbs the tallest tower.', 'COIL'],
  [30.4, 'Skyscrapers snap like toothpicks.', 'WIDE'],
  [34.4, 'Its legs span the whole city.', 'AERIAL'],
  [38.4, 'It walks above the weather.', 'CLOUDS'],
  [42.4, 'Its antennae scrape the sky.', 'SPACE'],
  [46.4, 'Astronauts can see it.', 'ORBIT1'],
  [50.4, 'It still has 30 legs.', 'ORBIT2'],
  [54.4, null, 'ORBIT2'],
];
export const CARD_T = 54.4;
export const TOTAL = 59.5;
const PRESETS = {
  A: [[-1.5, 0.32, 0.6], [0.35, 0.06, 0]],
  SIDE: [[0.25, 0.3, 1.5], [0.0, 0.03, 0]],
  TOP: [[-0.2, 2.3, 0.45], [0.05, 0, 0]],
  FRONT: [[1.7, 0.22, 0.75], [0.0, 0.07, 0]],
  WIDE: [[-2.2, 1.3, 2.0], [0.3, 0.05, 0]],
  AERIAL: [[-0.5, 2.6, 1.1], [0.15, 0, 0]],
  CLOUDS: [[-1.3, 0.22, 1.1], [0.45, 0.12, 0]],
  SPACE: [[-1.9, 0.9, 1.7], [0.4, 0.15, 0]],
  ORBIT1: [[-2.2, 1.6, 2.4], [0.25, -0.1, 0]],
  ORBIT2: [[-2.0, 2.7, 2.9], [0.1, -0.7, 0]],
};
const SUBS = [[0, 'SMALLER THAN A PAPERCLIP'], [0.035, 'LONGER THAN A PAPERCLIP'], [0.2, 'LONGER THAN YOUR HAND'], [0.5, 'LONGER THAN A HOUSE CAT'],
  [1.8, 'LONGER THAN YOU ARE TALL'], [12.5, 'LONGER THAN A SCHOOL BUS'], [33, 'LONGER THAN A BLUE WHALE'], [330, 'LONGER THAN THE EIFFEL TOWER'],
  [830, 'LONGER THAN THE BURJ KHALIFA'], [8849, 'LONGER THAN EVEREST IS TALL'], [42195, 'LONGER THAN A MARATHON'], [100000, 'LONGER THAN SPACE IS HIGH'],
  [410000, 'HIGHER THAN THE SPACE STATION'], [1250000, 'WIDER THAN TEXAS']];

const ease = (x) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
const clamp01 = (x) => Math.max(0, Math.min(1, x));
export const sizeAt = (t) => 0.02 * Math.pow(2, Math.min(t, CARD_T) / 2);
const X0 = 0.22, ZC = -0.7;
const xAt = (t) => X0 + 0.866 * (sizeAt(t) - 0.02);
// leg cadence slows as it grows (big things move slowly); integrated so the phase is continuous
function legCycles(t) { const T1 = 37.3; return t < T1 ? 2.6 * t - 0.0275 * t * t : 2.6 * T1 - 0.0275 * T1 * T1 + 0.55 * (t - T1); }
function fmt(m) {
  if (m < 1) { const cm = m * 100; return (cm < 10 ? cm.toFixed(1) : Math.round(cm)) + ' cm'; }
  if (m < 1000) return (m < 10 ? m.toFixed(1) : Math.round(m).toLocaleString('en-US')) + ' m';
  const km = m / 1000; return (km < 10 ? km.toFixed(1) : Math.round(km).toLocaleString('en-US')) + ' km';
}

// ---------- renderer ----------
const QP = new URLSearchParams(location.search), QN = (k, d) => (QP.has(k) ? +QP.get(k) : d);
const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: QN('aa', 1) === 1, logarithmicDepthBuffer: QN('logz', 0) === 1, preserveDrawingBuffer: true });
renderer.setPixelRatio(QN('px', 0.5));
renderer.setSize(1080, 1920, false);
renderer.shadowMap.enabled = QN('shadow', 1024) > 0; renderer.shadowMap.type = QN('soft', 0) ? THREE.PCFSoftShadowMap : THREE.PCFShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(40, 1080 / 1920, 0.0004, 150);
const hemi = new THREE.HemisphereLight(0xd6e6ff, 0x8a7a62, 1.15); scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff0d8, 2.9); sun.castShadow = true; sun.shadow.mapSize.set(QN('shadow', 1024), QN('shadow', 1024));
scene.add(sun, sun.target);
const SUN_DIR = new THREE.Vector3(0.4, 0.78, 0.48).normalize();
const skyCanvas = document.createElement('canvas'); skyCanvas.width = 4; skyCanvas.height = 512;
const skyTex = new THREE.CanvasTexture(skyCanvas); skyTex.colorSpace = THREE.SRGBColorSpace; scene.background = skyTex;
scene.fog = new THREE.Fog(0xcfe2f2, 100, 2000);

// ---------- world ----------
const ground = makeGround(); scene.add(ground);
const land = makeLand(); scene.add(land);
const clouds = makeClouds(); scene.add(clouds);
const suburb = makeSuburb(); scene.add(suburb.g);
const city = makeCity(); scene.add(city.im);
const tower = makeSupertall(); scene.add(tower);
const cars = makeCars(); scene.add(cars.body, cars.cab);
const hero = makeHeroCar(); scene.add(hero);
const dust = makeDust(); scene.add(dust.im);
const bath = makeBathroom(); scene.add(bath);
const interior = makeInterior(); scene.add(interior);
const shell = makeHouseShell(); scene.add(shell);
const slab = new THREE.Mesh(new THREE.BoxGeometry(10.2, 0.3, 8.2), mat(0x9a948a)); slab.position.set(3.8, -0.15, 3.1); slab.receiveShadow = true; scene.add(slab);
const earth = makeEarth(); scene.add(earth);
const stars = makeStars(); scene.add(stars);
const moon = makeMoon(); scene.add(moon);
const cent = makeCentipede(); scene.add(cent);
const roach = makeRoach(); roach.scale.setScalar(0.013); roach.position.set(0.42, 0, ZC + 0.01); roach.rotation.y = Math.PI; scene.add(roach);
const cat = makeCat(); cat.position.set(2.6, 0, -0.4); cat.rotation.y = Math.PI; scene.add(cat);
const human = makeHuman(); human.position.set(6.8, 0, -0.3); human.rotation.y = Math.PI; scene.add(human);
const humanBase = human.position.clone(), catBase = cat.position.clone();
const HERO_Z = 12, EARTH_C = new THREE.Vector3(0, -R_EARTH, 0);
const heroX = (t) => 75 - 14 * (t - 20);

// ---------- body path: straight walk, the tower coil, and the Earth's curvature ----------
const C0 = 26.4, C1 = 30.0;   // coil window
const coilW = (t) => ease((t - C0) / 0.9) * (1 - ease((t - (C1 - 0.6)) / 0.8));
function rootPose(t) {   // root on the sphere: angle phi along the walking direction (x)
  const phi = xAt(t) / R_EARTH;
  return { pos: new THREE.Vector3(R_EARTH * Math.sin(phi), R_EARTH * Math.cos(phi) - R_EARTH, ZC), phi };
}
function curveAt(t) {
  const S = sizeAt(t), H = cent.userData.H, rho = R_EARTH / S, w = coilW(t), root = rootPose(t).pos;
  const Rw = 34 + 0.05 * S, u = clamp01((t - C0) / (C1 - C0));
  const helix = (s) => {   // world-space helix around the tower, head up, sliding upward over time
    const th = 2.2 + 0.55 * (t - C0) + (s * S) / Rw;
    const y = 60 + 150 * u + (s + 0.45) * S * 0.32;
    return new THREE.Vector3(TOWER.x + Rw * Math.cos(th), y, TOWER.z + Rw * Math.sin(th));
  };
  const base = (s) => new THREE.Vector3((rho + H) * Math.sin(s / rho), (rho + H) * Math.cos(s / rho) - rho, 0);
  const P = (s) => (w <= 0 ? base(s) : base(s).lerp(helix(s).sub(root).divideScalar(S), w));
  return (s) => {
    const p = P(s), x = P(s + 0.01).sub(P(s - 0.01)).normalize();
    const upB = new THREE.Vector3(Math.sin(s / rho), Math.cos(s / rho), 0);
    let y = upB;
    if (w > 0) { const hp = helix(s); const radial = new THREE.Vector3(hp.x - TOWER.x, 0, hp.z - TOWER.z).normalize(); y = upB.clone().lerp(radial, w).normalize(); }
    y = y.sub(x.clone().multiplyScalar(y.dot(x))).normalize();
    return { p, x, y };
  };
}

// ---------- crumble pre-pass (every frame independent of render order) ----------
const breakables = [];
for (const o of bath.userData.props) breakables.push({ o, h: o.userData.h, k: o.userData.h === 0.85 ? 0.62 : 1.4, indoor: true });
for (const o of interior.userData.parts) breakables.push({ o, h: o.userData.h, k: 0.58, indoor: true });
for (const o of suburb.items) breakables.push({ o, h: o.userData.h, k: 2.2 });
for (const b of breakables) { b.base = { s: b.o.scale.clone(), p: b.o.position.clone(), r: b.o.rotation.clone() }; b.tb = Infinity; b.wp = new THREE.Vector3(); b.o.getWorldPosition(b.wp); }
const towerTb = new Float32Array(city.towers.length).fill(Infinity);
const carTb = new Float32Array(cars.cars.length).fill(Infinity);
const carX = (c, t) => { const span = 4700; return -100 + ((((c.x0 + c.v * t + 100) % span) + span) % span); };
const events = [];
let roachTb = Infinity;
const SUPER_TB = 30.0;
events.push({ p: new THREE.Vector3(TOWER.x, 200, TOWER.z), s: 260, t0: SUPER_TB, seed: 4242 });
function inFoot(x, z, t, pad = 0) {
  const S = sizeAt(t), xc = xAt(t);
  if (coilW(t) > 0.5) return Math.hypot(x - TOWER.x, z - TOWER.z) < 0.45 * S + pad;
  return x > xc - 0.75 * S - pad && x < xc + 0.62 * S + pad && Math.abs(z - ZC) < 0.5 * S + pad;
}
for (let t = 0; t <= CARD_T; t += 1 / 30) {
  const S = sizeAt(t), xc = xAt(t);
  if (roachTb === Infinity && xc + 0.45 * S >= roach.position.x - 0.004) { roachTb = t; events.push({ p: roach.position.clone(), s: 0.015, t0: t, seed: 99 }); }
  for (const b of breakables) {
    if (b.tb !== Infinity) continue;
    if (S > b.k * b.h && (inFoot(b.wp.x, b.wp.z, t, b.h * 0.5) || (b.indoor && S > 3.2 * b.h))) {
      b.tb = t; events.push({ p: b.wp.clone(), s: Math.max(0.3, b.h * 0.8), t0: t, seed: events.length + 1 });
    }
  }
  if (S > 40 && S < 40000) city.towers.forEach((tw, i) => {
    if (towerTb[i] === Infinity && S > 1.6 * tw.h && inFoot(tw.x, tw.z, t)) { towerTb[i] = t; if (events.length < 1200) events.push({ p: new THREE.Vector3(tw.x, 0, tw.z), s: tw.h * 0.7, t0: t, seed: i + 7 }); }
  });
  if (S > 25 && S < 3000) cars.cars.forEach((c, i) => {
    if (carTb[i] !== Infinity) return;
    const x = carX(c, t);
    if (Math.hypot(x - (xc + 0.47 * S), c.z - ZC) < 0.14 * S) { carTb[i] = t; events.push({ p: new THREE.Vector3(x, 0, c.z), s: 4, t0: t, seed: 5000 + i }); }
  });
}

// ---------- per-frame helpers ----------
const M = new THREE.Matrix4(), Q = new THREE.Quaternion(), V = new THREE.Vector3(), SC = new THREE.Vector3(), ZERO = new THREE.Matrix4().makeScale(0, 0, 0);
const Y_AXIS = new THREE.Vector3(0, 1, 0), Z_AXIS = new THREE.Vector3(0, 0, 1);
function crumble(b, t) {
  const e = ease(clamp01((t - b.tb) / 0.7));
  b.o.scale.set(b.base.s.x * (1 + 0.15 * e), b.base.s.y * (1 - 0.88 * e), b.base.s.z * (1 + 0.15 * e));
  b.o.position.copy(b.base.p); b.o.rotation.copy(b.base.r); b.o.rotation.z += 0.25 * e * Math.sin(b.wp.x * 13.1);
}
function setSky(alt) {
  const k1 = clamp01((alt - 400) / 15000), k2 = clamp01((alt - 15000) / 120000), k3 = clamp01((alt - 150000) / 1500000);
  const mix = (a, b, c, d) => new THREE.Color(a).lerp(new THREE.Color(b), k1).lerp(new THREE.Color(c), k2).lerp(new THREE.Color(d), k3);
  const top = mix(0x3f84dc, 0x1b4bb0, 0x040a22, 0x02030a), hor = mix(0xd2e4f2, 0x9cc2ea, 0x3b70c4, 0x070b1c);
  const g = skyCanvas.getContext('2d'), gr = g.createLinearGradient(0, 0, 0, 512);
  gr.addColorStop(0, '#' + top.getHexString()); gr.addColorStop(0.62, '#' + hor.getHexString()); gr.addColorStop(1, '#' + hor.clone().multiplyScalar(0.9).getHexString());
  g.fillStyle = gr; g.fillRect(0, 0, 4, 512); skyTex.needsUpdate = true;
  scene.fog.color.copy(hor);
  stars.material.opacity = clamp01((alt - 60000) / 200000);
}
function beatAt(t) { let i = 0; while (i + 1 < BEATS.length && BEATS[i + 1][0] <= t) i++; return i; }
function targetAt(t) {   // what the camera frames: mid-body (rides the curvature, follows the coil)
  const S = sizeAt(t), { pos, phi } = rootPose(t);
  const T = pos.clone().add(new THREE.Vector3(0.15 * S, 0.05 * S, 0).applyAxisAngle(Z_AXIS, -phi));
  const w = coilW(t);
  if (w > 0) T.lerp(new THREE.Vector3(TOWER.x, 60 + 150 * clamp01((t - C0) / (C1 - C0)) + 0.15 * S, TOWER.z), w);
  return { T, phi };
}
function poseWorld(name, t, u) {
  const S = sizeAt(t), { T, phi } = targetAt(t);
  if (name === 'HERO0') { // low by the toilet base, slow push-in
    const k = ease(clamp01(t / 3.3));
    return { pos: new THREE.Vector3(1.35, 0.42, -0.05).lerp(new THREE.Vector3(0.39, 0.018, -0.655), k), look: new THREE.Vector3(0.12, 0.36, -0.55).lerp(new THREE.Vector3(0.2, 0.012, -0.7), k) };
  }
  if (name === 'HUMAN') return { pos: new THREE.Vector3(11.6, 1.05, 0.05), look: new THREE.Vector3(3.8 + 0.4 * u, 1.5, -0.65) };
  if (name === 'CAR') { // chase the red car as it drives under the legs
    const hx = heroX(t);
    return { pos: new THREE.Vector3(hx + 16, 2.2 + 1.5 * u, HERO_Z + 6.5), look: new THREE.Vector3(hx - 20, 3 + 0.1 * S, HERO_Z - 9) };
  }
  if (name === 'COIL') { // orbit the supertall while it climbs
    const a = 0.9 + 0.35 * (t - C0), D = 1.35 * S + 200, h = 0.45 * S + 170 + 60 * u;
    return { pos: new THREE.Vector3(TOWER.x + D * Math.cos(a), h, TOWER.z + D * Math.sin(a)), look: T.clone() };
  }
  const P = PRESETS[name], off = new THREE.Vector3(...P[0]);
  const spin = name.startsWith('ORBIT') ? 0.55 * u : 0.16 * (u - 0.5);   // the last act moves faster
  off.applyAxisAngle(Y_AXIS, spin + 0.05 * Math.sin(t * 0.37));
  off.multiplyScalar(1 - 0.06 * u);
  const toW = (v) => v.clone().applyAxisAngle(Z_AXIS, -phi).multiplyScalar(S).add(T);
  return { pos: toW(off), look: toW(new THREE.Vector3(...P[1])) };
}
const CUTS = new Set(['CAR', 'COIL', 'HUMAN']);   // hard cuts: a blended move would fly through buildings
function camPose(t) {
  const i = beatAt(t), b = BEATS[i];
  const end = i + 1 < BEATS.length ? BEATS[i + 1][0] : TOTAL;
  const u = (t - b[0]) / (end - b[0]);
  const cur = poseWorld(b[2], t, u);
  const k = i === 0 || CUTS.has(b[2]) ? 1 : ease((t - b[0]) / 1.3);
  if (k >= 1) return cur;
  const prev = poseWorld(BEATS[i - 1][2], t, 1);
  return { pos: prev.pos.lerp(cur.pos, k), look: prev.look.lerp(cur.look, k) };
}

// ---------- text overlay (2D compositor at output resolution) ----------
const comp = makeCompositor(canvas, Math.round(1080 * QN('out', 1)), Math.round(1920 * QN('out', 1))), YEL = '#ffd23f', WHT = '#ffffff';
function overlay(t, S) {
  const c = comp.ctx;
  comp.begin();
  shadowOn(c, 12, 2, 0.6);
  richText(c, [['What if a ', WHT], ['house centipede', YEL], [' doubled in size every 2 seconds?', WHT]], 540, 150, 960, '500 62px Lora', 72);
  c.textAlign = 'left'; c.fillStyle = WHT;
  c.font = '600 19px Lora'; c.letterSpacing = '6px'; c.globalAlpha = 0.92; c.fillText('SIZE', 76, 542);
  const pulse = 1 + 0.06 * Math.exp(-((t % 2) / 0.12)) * (t > 0.5 ? 1 : 0);   // a small kick on every doubling
  c.globalAlpha = 1; c.letterSpacing = '0px'; c.font = `500 ${Math.round(96 * pulse)}px Lora`; c.fillText(fmt(S), 72, 640);
  let sub = SUBS[0][1]; for (const [v, sx] of SUBS) if (S >= v) sub = sx;
  c.font = '600 17px Lora'; c.letterSpacing = '3.4px'; c.globalAlpha = 0.88;
  const sw = c.measureText(sub).width; c.fillText(sub, 76, 690);
  shadowOff(c); c.fillStyle = 'rgba(255,255,255,0.6)'; c.fillRect(76, 662, sw, 1.5); c.fillStyle = WHT; shadowOn(c, 12, 2, 0.6);
  c.letterSpacing = '0px'; c.globalAlpha = 1;
  const i = beatAt(t), b = BEATS[i], end = i + 1 < BEATS.length ? BEATS[i + 1][0] : TOTAL;
  if (b[1]) { c.globalAlpha = Math.min(clamp01((t - b[0]) / 0.3), clamp01((end - t) / 0.25)); richText(c, [[b[1], WHT]], 540, 1205, 840, '400 46px Lora', 58); c.globalAlpha = 1; }
  c.globalAlpha = 0.8; c.fillStyle = '#c4261e'; c.beginPath(); c.ellipse(54, 1757, 9, 4, 0, Math.PI, 0); c.fill();
  c.fillStyle = '#8f4a2b'; c.beginPath(); c.arc(54, 1764, 10, 0, Math.PI * 2); c.fill();
  c.fillStyle = WHT; c.font = '600 22px Lora'; c.letterSpacing = '4px'; c.fillText('MEATBALL MYTHS', 74, 1772); c.letterSpacing = '0px'; c.globalAlpha = 1;
  const k = clamp01((t - CARD_T) / 0.6);
  if (k > 0) {
    shadowOff(c); c.globalAlpha = k; c.fillStyle = '#07080c'; c.fillRect(0, 0, 1080, 1920);
    c.globalAlpha = clamp01((t - CARD_T - 0.4) / 0.6);
    richText(c, [['Which ', WHT], ['bug', YEL], [' in your house should double next?', WHT]], 540, 800, 840, '500 66px Lora', 80);
    c.globalAlpha = 0.7 * clamp01((t - CARD_T - 1.4) / 0.6); c.textAlign = 'center'; c.font = '600 26px Lora'; c.letterSpacing = '7px'; c.fillStyle = WHT;
    c.fillText('COMMENT BELOW', 540, 1110); c.letterSpacing = '0px'; c.textAlign = 'left'; c.globalAlpha = 1;
  }
}

// ---------- frame ----------
function render(tReq) {
  const t = Math.min(tReq, CARD_T + 0.7);
  const S = sizeAt(t), xc = xAt(t), rp = rootPose(t);
  cent.scale.setScalar(S); cent.position.copy(rp.pos); cent.rotation.set(0, 0, -rp.phi);
  animateCentipede(cent, legCycles(t), 1, 1 - 0.6 * coilW(t), curveAt(t));
  cent.updateMatrixWorld();
  // roach, cat, human, hero car
  roach.visible = t < roachTb + 0.15; roach.position.x = 0.42 + 0.004 * Math.sin(t * 9); roach.rotation.y = Math.PI + 0.25 * Math.sin(t * 3.1);
  const cf = clamp01((t - 12.3) / 2.5);
  cat.rotation.y = cf > 0 ? -Math.PI / 2 : Math.PI; cat.position.set(catBase.x + 0.6 * cf, 0, catBase.z + 9 * cf * cf); cat.visible = t < 16;
  const hf = Math.max(0, t - 15.4);
  human.rotation.y = hf > 0 ? -Math.PI / 2 : Math.PI;
  human.position.set(humanBase.x, 0, humanBase.z + 2.2 * hf * hf + 3 * hf);
  poseWalk(human, hf > 0 ? hf * 11 : 0, hf > 0 ? 0.6 : 0);
  human.visible = t < 19;
  hero.visible = t > 19 && t < 24; hero.position.set(heroX(t), 0, HERO_Z); hero.rotation.y = Math.PI;
  // crumbles
  for (const b of breakables) { if (t >= b.tb) crumble(b, t); else { b.o.scale.copy(b.base.s); b.o.position.copy(b.base.p); b.o.rotation.copy(b.base.r); } }
  const cam = camPose(t), cpos = cam.pos, ray = [];
  const tgtT = targetAt(t).T;
  for (let k = 0; k <= 10; k++) ray.push(cpos.clone().lerp(cam.look, k / 10 * 0.85), cpos.clone().lerp(tgtT, k / 10 * 0.85));
  city.towers.forEach((tw, i) => {
    const p = t >= towerTb[i] ? ease(clamp01((t - towerTb[i]) / 1.0)) : 0;
    let h = tw.h * (1 - 0.9 * p);
    // never let a tower swallow the camera: drop any tower the camera is inside of (or brushing against)
    for (const q of ray) if (q.y < h + 8 && Math.abs(q.x - tw.x) < tw.w / 2 + 12 && Math.abs(q.z - tw.z) < tw.d / 2 + 12) { h = 0.01; break; }
    M.compose(V.set(tw.x, h / 2, tw.z), Q.identity(), SC.set(tw.w * (1 + 0.2 * p), h, tw.d * (1 + 0.2 * p))); city.im.setMatrixAt(i, M);
  });
  city.im.instanceMatrix.needsUpdate = true;
  const sp = ease(clamp01((t - SUPER_TB) / 1.2)); tower.scale.set(1 + 0.3 * sp, 1 - 0.9 * sp, 1 + 0.3 * sp); tower.rotation.z = 0.25 * sp;
  cars.cars.forEach((c, i) => {
    if (t >= carTb[i]) { cars.body.setMatrixAt(i, ZERO); cars.cab.setMatrixAt(i, ZERO); return; }
    const x = carX(c, t), d = Math.sign(c.v);
    M.compose(V.set(x, 0.55, c.z), Q.identity(), SC.set(4.4, 0.9, 1.9)); cars.body.setMatrixAt(i, M);
    M.compose(V.set(x - d * 0.3, 1.25, c.z), Q.identity(), SC.set(2.3, 0.6, 1.7)); cars.cab.setMatrixAt(i, M);
  });
  cars.body.instanceMatrix.needsUpdate = cars.cab.instanceMatrix.needsUpdate = true;
  dust.update(events, t);
  // the house rides on its back
  const L0 = 17.6, lp = ease(clamp01((t - L0) / 1.5));
  shell.userData.outerG.visible = t >= L0;
  const back = cent.localToWorld(new THREE.Vector3(-0.05, 0.075, 0)), tgt = back.sub(new THREE.Vector3(3.8, 0, 3.1));
  shell.position.set(0, 0, 0).lerp(tgt, lp); shell.position.y += 4 * lp * (1 - lp) * 0.4 * S + (lp >= 1 ? 0.004 * S * Math.sin(legCycles(t) * 6.28) : 0);
  shell.rotation.z = 0.12 * Math.sin(lp * Math.PI) - (lp >= 1 ? rp.phi : 0);
  shell.visible = S < 20000;
  // size-band culling: each layer only exists where it can be seen
  interior.visible = bath.visible = t < 26; slab.visible = t < 40;
  suburb.g.visible = cars.body.visible = cars.cab.visible = S < 3000;
  city.im.visible = S > 2 && S < 60000; tower.visible = S > 10 && t < SUPER_TB + 1.4;
  land.visible = S > 150 && S < 30000; clouds.material.opacity = clamp01((S - 6000) / 6000); ground.visible = S < 30000; clouds.visible = S > 6000 && S < 400000;
  earth.visible = S >= 30000; moon.visible = S > 300000; stars.visible = S > 20000;
  // camera
  const cp = camPose(t);
  camera.position.copy(cp.pos);
  if (S < 30000 && camera.position.y < 0.002) camera.position.y = 0.002;
  camera.lookAt(cp.look);
  const dist = camera.position.distanceTo(cp.look);
  camera.near = Math.max(0.0004, Math.min(S * 0.02, dist * 0.05)); camera.far = Math.max(150, S * 6000, 1.2e8 * (S > 300000 ? 1 : 0));
  camera.updateProjectionMatrix();
  stars.position.copy(camera.position); stars.scale.setScalar(camera.far * 0.9);
  // light + sky
  const { T } = targetAt(t), E = Math.max(0.6, S * 2.6);
  sun.position.copy(T).addScaledVector(SUN_DIR, E * 4); sun.target.position.copy(T);
  Object.assign(sun.shadow.camera, { left: -E, right: E, top: E, bottom: -E, near: E * 0.5, far: E * 9 });
  sun.shadow.camera.updateProjectionMatrix(); sun.shadow.bias = -0.0003; sun.shadow.normalBias = E / sun.shadow.mapSize.x * 1.2;
  setSky(camera.position.distanceTo(EARTH_C) - R_EARTH);
  scene.fog.near = Math.max(120, S * 10); scene.fog.far = Math.max(2500, S * 60);
  if (tReq < CARD_T + 0.7) renderer.render(scene, camera);
  overlay(tReq, S);
}
function frame(t, q = 0.92) { render(t); return comp.jpeg(q); }
scene.userData.cam = camera;
window.SIM = { render, frame, renderer, scene, TOTAL, BEATS: BEATS.map((b) => [b[0], b[1]]), ready: Promise.all(['400 46px Lora', '500 62px Lora', '600 20px Lora'].map((f) => document.fonts.load(f))).then(() => true) };
