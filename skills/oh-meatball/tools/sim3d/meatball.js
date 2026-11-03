// 3D Meatball test: a two-line dialogue in the low-poly bathroom next to a real-size house centipede.
// Timeline (voice lines, word timings, mouth envelopes) comes from work/mb/timeline.json (built by meatball_audio.py).
import * as THREE from 'three';
import { makeCompositor, richText, shadowOn, shadowOff } from './overlay2d.js';
import { mat, mesh, ICO, limbGeo, makeCentipede, animateCentipede, makeRoach, makeHuman, makeBathroom, makeInterior, makeHouseShell } from './lib.js';

const TL = await (await fetch('../work/mb/timeline.json')).json();
const clamp01 = (x) => Math.max(0, Math.min(1, x));
const ease = (x) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));

// ---------- Meatball (ball radius 1 unit) ----------
function makeMeatball() {
  const g = new THREE.Group(), body = new THREE.Group(); g.add(body);
  const geo = new THREE.IcosahedronGeometry(1, 2), p = geo.attributes.position, v = new THREE.Vector3();
  for (let i = 0; i < p.count; i++) { v.fromBufferAttribute(p, i); const n = 1 + 0.07 * Math.sin(v.x * 5.1 + v.y * 2.3) * Math.cos(v.z * 4.3 - v.y * 1.7); v.multiplyScalar(n); p.setXYZ(i, v.x, v.y, v.z); }
  geo.computeVertexNormals();
  const meat = mesh(geo, mat(0x8e4a2b, { roughness: 0.7 })); body.add(meat);
  const spots = [[0.5, 0.55, 0.55], [-0.6, 0.2, 0.7], [0.7, -0.4, 0.5], [-0.3, -0.6, 0.72], [0.1, 0.85, -0.4], [-0.75, 0.5, -0.3]];
  for (const [x, y, z] of spots) { const s = mesh(ICO, mat(0x6a3219), false); s.scale.set(0.16, 0.16, 0.06); s.position.set(x, y, z).normalize().multiplyScalar(0.99); s.lookAt(s.position.clone().multiplyScalar(2)); body.add(s); }
  const shine = mesh(ICO, mat(0xd08a62), false); shine.scale.set(0.2, 0.13, 0.05); shine.position.set(-0.45, 0.62, 0.62); shine.lookAt(-0.9, 1.24, 1.24); body.add(shine);
  // cap: red sauce dome + brim + parsley
  const cap = new THREE.Group(); cap.position.set(0, 0.86, 0); cap.rotation.z = 0.12; body.add(cap);
  const dome = mesh(new THREE.SphereGeometry(0.62, 10, 5, 0, Math.PI * 2, 0, Math.PI / 2), mat(0xc4261e, { roughness: 0.4 })); dome.scale.y = 0.45; cap.add(dome);
  const brim = mesh(new THREE.CylinderGeometry(0.85, 0.85, 0.05, 12), mat(0xb21f18, { roughness: 0.4 })); brim.position.set(0.25, 0.02, 0); brim.scale.set(1, 1, 0.75); cap.add(brim);
  const parsley = mesh(ICO, mat(0x3f9a3c)); parsley.scale.set(0.12, 0.08, 0.12); parsley.position.set(0.05, 0.3, 0); cap.add(parsley);
  // face on +x: googly eyes, brows, mouth
  const face = new THREE.Group(); body.add(face);
  const eyes = [], lids = [], brows = [];
  for (const s of [-1, 1]) {
    const e = new THREE.Group(); e.position.set(0.86, 0.22, s * 0.3); face.add(e);
    const white = mesh(new THREE.SphereGeometry(0.24, 12, 8), mat(0xffffff, { roughness: 0.3, flatShading: false }), false); white.scale.x = 0.6; e.add(white);
    const pupil = mesh(new THREE.SphereGeometry(0.11, 10, 6), mat(0x111111, { roughness: 0.2, flatShading: false }), false); pupil.position.x = 0.13; e.add(pupil);
    const lid = mesh(new THREE.SphereGeometry(0.255, 12, 6, 0, Math.PI * 2, 0, Math.PI / 2), mat(0x8e4a2b), false); lid.scale.x = 0.65; e.add(lid);
    const brow = mesh(new THREE.BoxGeometry(0.05, 0.05, 0.3), mat(0x111111), false); brow.position.set(0.92, 0.55, s * 0.3); face.add(brow);
    eyes.push({ e, pupil, s }); lids.push(lid); brows.push({ brow, s });
  }
  const mouth = mesh(new THREE.SphereGeometry(0.16, 10, 6), mat(0x1a0d08, { roughness: 0.5, flatShading: false }), false); mouth.position.set(0.93, -0.3, 0); mouth.scale.set(0.35, 0.3, 1); face.add(mouth);
  // stick limbs (black)
  const ink = mat(0x141414, { roughness: 0.6 });
  const arms = [];
  for (const s of [-1, 1]) {
    const sh = new THREE.Group(); sh.position.set(0, -0.1, s * 0.95); g.add(sh);
    const up = mesh(limbGeo(0.06, 0.06, 0.7, 5), ink); sh.add(up);
    const el = new THREE.Group(); el.position.z = 0.7; sh.add(el);
    const fo = mesh(limbGeo(0.06, 0.055, 0.6, 5), ink); el.add(fo);
    const hand = mesh(new THREE.SphereGeometry(0.11, 8, 6), ink); hand.position.z = 0.62; el.add(hand);
    sh.scale.z = s; arms.push({ sh, el, s });
  }
  const legs = [];
  for (const s of [-1, 1]) {
    const hip = new THREE.Group(); hip.position.set(0, -0.85, s * 0.32); g.add(hip);
    const l = mesh(limbGeo(0.065, 0.06, 0.95, 5), ink); l.rotation.x = Math.PI / 2; hip.add(l);
    const foot = mesh(new THREE.SphereGeometry(0.14, 8, 5), ink); foot.scale.set(1.6, 0.6, 1); foot.position.set(0.1, -0.97, 0); hip.add(foot);
    legs.push(hip);
  }
  g.userData = { body, eyes, lids, brows, mouth, arms, legs };
  return g;
}
// pose: shoulder yaw/pitch + elbow per arm (radians); local arm points along +z (out to the side)
const POSES = {
  idle: { sp: 1.25, sy: 0.15, el: 0.25 },
  stop: { sp: -0.45, sy: 1.15, el: -0.9 },
  shrug: { sp: 0.2, sy: 0.25, el: -1.5 },
  hips: { sp: 0.9, sy: -0.6, el: 1.6 },
};
function poseMeatball(m, t, pose, talk, mood) {
  const u = m.userData;
  for (const a of u.arms) {
    a.sh.rotation.order = 'YXZ'; a.sh.rotation.y = pose.sy; a.sh.rotation.x = pose.sp + 0.05 * Math.sin(t * 2 + a.s);
    a.el.rotation.x = pose.el; a.el.rotation.y = 0;
  }
  u.mouth.scale.set(0.35, 0.18 + 0.75 * talk, 1);
  u.body.position.y = 0.03 * Math.sin(t * 3.1) + 0.06 * talk;
  u.body.rotation.z = 0.04 * Math.sin(t * 1.7) + (mood === 'deadpan' ? -0.05 : 0.04 * talk);
  const lid = mood === 'deadpan' ? 0.75 : (Math.abs(((t + 0.7) % 3.1) - 0.05) < 0.07 ? 1 : 0);
  for (const l of u.lids) { l.visible = lid > 0; l.scale.y = Math.max(0.01, lid); }
  for (const b of u.brows) { b.brow.position.y = mood === 'alarm' ? 0.66 : mood === 'deadpan' ? 0.47 : 0.55; b.brow.rotation.x = mood === 'alarm' ? -0.25 * b.s : mood === 'deadpan' ? 0.1 * b.s : 0; }
  for (const e of u.eyes) { e.pupil.position.y = 0.04 * Math.sin(t * 9 + e.s) * (talk + 0.2); e.pupil.position.z = 0.04 * Math.cos(t * 7 + e.s) * (talk + 0.2); }
}

// ---------- scene ----------
const canvas = document.getElementById('c');
const QP = new URLSearchParams(location.search), QN = (k, d) => (QP.has(k) ? +QP.get(k) : d);
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(QN('px', 0.5)); renderer.setSize(1080, 1920, false);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
const scene = new THREE.Scene(); scene.background = new THREE.Color(0xdfe9ef);
const camera = new THREE.PerspectiveCamera(42, 1080 / 1920, 0.005, 200);
scene.add(new THREE.HemisphereLight(0xe6eeff, 0x9a8a72, 1.2));
const sun = new THREE.DirectionalLight(0xfff0d8, 2.6); sun.castShadow = true; sun.shadow.mapSize.set(1024, 1024);
sun.position.set(2.2, 4, 2.2); sun.target.position.set(0.4, 0, 0);
Object.assign(sun.shadow.camera, { left: -2, right: 2, top: 2, bottom: -2, near: 0.5, far: 10 }); sun.shadow.bias = -0.0003; sun.shadow.normalBias = 0.002;
scene.add(sun, sun.target);
const lamp = new THREE.PointLight(0xffe2b8, 1.4, 4, 1.5); lamp.position.set(0.3, 2.3, 0.2); scene.add(lamp);
scene.add(makeBathroom(), makeInterior(), makeHouseShell());
const MB = 0.06, mb = makeMeatball(); mb.scale.setScalar(MB); mb.position.set(0.56, 0.95 * MB * 1.0 + 0.9 * MB * 0.1, 0.05); scene.add(mb);
mb.position.y = (0.85 + 0.95 + 0.08) * MB;
const cent = makeCentipede(); cent.scale.setScalar(0.04); cent.position.set(0.47, 0, -0.16); cent.rotation.y = 0.5; scene.add(cent);
const human = makeHuman(0x3c6e8f); human.position.set(1.16, 0, 0.35); human.rotation.y = Math.PI + 0.25; scene.add(human);
const roaches = [];
for (let i = 0; i < 30; i++) { const r = makeRoach(); r.scale.setScalar(0.016); scene.add(r); roaches.push({ r, a: i * 2.39, d: 0.05 + (i % 7) * 0.035, z: (i % 5) * 0.12 }); }
const victim = makeRoach(); victim.scale.setScalar(0.014); victim.position.set(0.5, 0, -0.21); victim.rotation.y = 2.4; scene.add(victim);

// ---------- shots ----------
const L = TL.lines, T_END = TL.total;
const V = (a) => new THREE.Vector3(...a);
const SHOTS = [
  { t: 0, cam: [[0.05, 0.09, -0.2], [0.1, 0.1, -0.17]], look: [[1.16, 1.1, 0.35], [1.16, 1.15, 0.35]] },                       // past Meatball, up at the human
  { t: L[0].t + L[0].dur * 0.55, cam: [[0.98, 1.42, 0.3], [0.95, 1.36, 0.28]], look: [[0.5, 0.0, -0.06], [0.51, 0.02, -0.06]] }, // human POV down at the floor
  { t: L[1].t - 0.15, cam: [[1.02, 0.17, 0.0], [0.96, 0.16, -0.01]], look: [[0.5, 0.075, -0.07], [0.5, 0.075, -0.07]] },     // Meatball + centipede
  { t: L[2].t - 0.1, cam: [[0.2, 0.05, 0.75], [0.23, 0.06, 0.73]], look: [[1.16, 1.2, 0.35], [1.16, 1.25, 0.35]] },        // up at the human
  { t: L[3].t - 0.1, cam: [[0.84, 0.115, 0.08], [0.8, 0.112, 0.07]], look: [[0.56, 0.1, 0.05], [0.56, 0.1, 0.05]] },        // deadpan close
  { t: L[3].t + L[3].dur + 0.25, cam: [[-0.05, 0.07, 0.12], [-0.17, 0.05, 0.16]], look: [[-0.4, 0.0, 0.18], [-0.42, 0.0, 0.2]] }, // the reveal
];
function shotAt(t) { let i = 0; while (i + 1 < SHOTS.length && SHOTS[i + 1].t <= t) i++; return SHOTS[i]; }
function lineAt(t) { return L.find((l) => t >= l.t && t < l.t + l.dur + 0.05); }
function env(l, t) { if (!l) return 0; const i = Math.floor((t - l.t) * TL.fps); return l.env[Math.max(0, Math.min(l.env.length - 1, i))] || 0; }

const comp = makeCompositor(canvas);
function captions(t) {   // s5 style: bold uppercase chunks of 3 words, the spoken word in yellow
  const c = comp.ctx; comp.begin();
  const l = lineAt(t);
  if (l) {
    const words = l.words, rel = t - l.t;
    let k = 0; for (let i = 0; i < words.length; i++) if (rel >= words[i][0] - 0.02) k = i;
    const c0 = Math.floor(k / 3) * 3, chunk = words.slice(c0, c0 + 3);
    const pop = 1 + 0.08 * Math.exp(-Math.max(0, rel - words[k][0]) / 0.08);
    shadowOn(c, 0, 7, 0.85);
    richText(c, chunk.map((w, j) => [w[2].toUpperCase() + (j < chunk.length - 1 ? ' ' : ''), c0 + j === k ? '#ffd23f' : '#ffffff']), 540, 1150, 960, `900 ${Math.round(86 * pop)}px Inter`, 96, { stroke: 12 });
    shadowOff(c);
  }
  c.globalAlpha = 0.8; c.fillStyle = '#c4261e'; c.beginPath(); c.ellipse(54, 1757, 9, 4, 0, Math.PI, 0); c.fill();
  c.fillStyle = '#8f4a2b'; c.beginPath(); c.arc(54, 1764, 10, 0, Math.PI * 2); c.fill();
  c.fillStyle = '#fff'; c.font = '600 22px Lora'; c.letterSpacing = '4px'; c.textAlign = 'left'; c.fillText('MEATBALL MYTHS', 74, 1772); c.letterSpacing = '0px'; c.globalAlpha = 1;
}

function render(t) {
  const sh = shotAt(t), next = SHOTS[SHOTS.indexOf(sh) + 1], t1 = next ? next.t : T_END, u = ease(clamp01((t - sh.t) / (t1 - sh.t)));
  camera.position.copy(V(sh.cam[0]).lerp(V(sh.cam[1]), u)); camera.lookAt(V(sh.look[0]).lerp(V(sh.look[1]), u));
  const l = lineAt(t), e = env(l, t), who = l ? l.who : null;
  const mood = t >= L[3].t - 0.1 ? 'deadpan' : t >= L[1].t - 0.2 && t < L[1].t + L[1].dur ? 'alarm' : 'calm';
  const pose = t >= L[1].t - 0.15 && t < L[1].t + L[1].dur + 0.2 ? POSES.stop : t >= L[3].t - 0.1 ? POSES.hips : POSES.idle;
  poseMeatball(mb, t, pose, who === 'meatball' ? e : 0, mood);
  mb.rotation.y = t < L[3].t - 0.1 ? 0.35 : 0.0; // faces the human, then the camera for the deadpan
  human.position.y = who === 'human' ? 0.01 * e : 0; human.rotation.z = who === 'human' ? 0.02 * Math.sin(t * 6) * e : 0;
  // the centipede creeps to the roach and eats it
  const ct = Math.min(t, 6.0); cent.position.set(0.47 - 0.012 * ct, 0, -0.16 - 0.004 * ct);
  animateCentipede(cent, t * 1.4, 1, 0.6);
  victim.visible = t < 5.2; victim.position.x = 0.5 + 0.003 * Math.sin(t * 13);
  // the reveal: roaches swarming along the tub's base
  const rv = clamp01((t - SHOTS[5].t + 0.2) / 0.4);
  roaches.forEach((o, i) => {
    o.r.visible = rv > 0;
    const ph = t * (0.6 + (i % 4) * 0.15) + o.a;
    o.r.position.set(-0.42 + o.d * 0.8 + 0.03 * Math.sin(ph * 2), 0, -0.1 + ((o.z + ph * 0.06) % 0.6));
    o.r.rotation.y = -Math.PI / 2 + 0.3 * Math.sin(ph * 3);
  });
  renderer.render(scene, camera);
  captions(t);
}
function frame(t, q = 0.92) { render(t); return comp.jpeg(q); }
window.SIM = { render, frame, TOTAL: T_END, ready: Promise.all(['900 86px Inter', '600 22px Lora'].map((f) => document.fonts.load(f))).then(() => true) };
