// 3D Meatball explainer: person asks, Meatball explains, in the low-poly bathroom with a real-size house centipede.
// Driven by work/timeline.json (explainer_audio.py: line starts, word timings, mouth envelopes, card + source keys).
// Shots/props per line live in shots.js; this file owns the scene, the per-frame state and the 2D layer.
import * as THREE from 'three';
import { makeCompositor } from './overlay2d.js';
import { makeCentipede, animateCentipede, makeRoach, makeBathroom, makeInterior, makeHouseShell } from './lib.js';
import * as P from './props.js';
import { drawCaption, drawFactCard, drawMapCard, drawLease, drawWatermark } from './cards.js';
import { buildPlan } from './shots.js';

const TL = await (await fetch('../work/timeline.json')).json();
const L = TL.lines, T_END = TL.total;
const clamp01 = (x) => Math.max(0, Math.min(1, x));
const ease = (x) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
const back = (x) => { const c = 1.7; x = clamp01(x); return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const V = (a) => new THREE.Vector3(...a);

// ---------- renderer + lights ----------
const canvas = document.getElementById('c');
const QP = new URLSearchParams(location.search);
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(QP.has('px') ? +QP.get('px') : 0.5); renderer.setSize(1080, 1920, false);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(42, 1080 / 1920, 0.004, 30);
const hemi = new THREE.HemisphereLight(0xe6eeff, 0x9a8a72, 1.2); scene.add(hemi);
const sun = new THREE.DirectionalLight(0xfff0d8, 2.6); sun.castShadow = true; sun.shadow.mapSize.set(1024, 1024);
sun.position.set(2.2, 4, 2.2); sun.target.position.set(0.4, 0, 0);
Object.assign(sun.shadow.camera, { left: -2, right: 2, top: 2, bottom: -2, near: 0.5, far: 10 }); sun.shadow.bias = -0.0003; sun.shadow.normalBias = 0.002;
scene.add(sun, sun.target);
const lamp = new THREE.PointLight(0xffe2b8, 1.4, 4, 1.5); lamp.position.set(0.3, 2.3, 0.2); scene.add(lamp);
const DAY = { bg: 0xdfe9ef, hemi: [0xe6eeff, 1.2], sun: [0xfff0d8, 2.6], lamp: 1.4 }, NIGHT = { bg: 0x1a2850, hemi: [0x8fa2dd, 1.0], sun: [0xb0c4ff, 1.9], lamp: 0.35 };
function setLight(n) { scene.background = new THREE.Color(n.bg); hemi.color.setHex(n.hemi[0]); hemi.intensity = n.hemi[1]; sun.color.setHex(n.sun[0]); sun.intensity = n.sun[1]; lamp.intensity = n.lamp; }

// ---------- set + cast ----------
scene.add(makeBathroom(), makeInterior(), makeHouseShell());
const S = {};   // everything shots.js may position
S.cent = makeCentipede(); S.cent.scale.setScalar(0.04); scene.add(S.cent);
S.baby = P.makeBabyCentipede(); S.baby.scale.setScalar(0.01); scene.add(S.baby);
S.mb = P.makeMeatball(); S.MB = 0.06; S.mb.scale.setScalar(S.MB); scene.add(S.mb);
S.person = P.makePerson(); scene.add(S.person);
S.slipper = P.makeSlipper(); S.slipper.position.set(0, -0.06, 0); S.slipper.rotation.z = Math.PI / 2; S.person.userData.hands[1].add(S.slipper);
for (const k of ['victim', 'pushRoach']) { S[k] = makeRoach(); S[k].scale.setScalar(0.016); scene.add(S[k]); }
S.swarm = []; for (let i = 0; i < 30; i++) { const r = makeRoach(); r.scale.setScalar(0.016); scene.add(r); S.swarm.push({ r, a: i * 2.39, d: 0.05 + (i % 7) * 0.035, z: (i % 5) * 0.12 }); }
S.spider = P.makeSpider(); S.spider.scale.setScalar(0.014); scene.add(S.spider);
S.spider2 = P.makeSpider(); S.spider2.scale.setScalar(0.012); scene.add(S.spider2);
S.thread = new THREE.Mesh(new THREE.CylinderGeometry(0.0004, 0.0004, 1, 3), new THREE.MeshBasicMaterial({ color: 0xffffff })); scene.add(S.thread);
S.silverfish = P.makeSilverfish(); S.silverfish.scale.setScalar(0.016); scene.add(S.silverfish);
S.silver2 = P.makeSilverfish(); S.silver2.scale.setScalar(0.016); scene.add(S.silver2);
S.ant = P.makeAnt(); S.ant.scale.setScalar(0.011); scene.add(S.ant);
S.bedbug = P.makeBedBug(); S.bedbug.scale.setScalar(0.011); scene.add(S.bedbug);
S.bee = P.makeBee(); S.bee.scale.setScalar(0.017); scene.add(S.bee);
S.leg = P.makeLooseLeg(); S.leg.scale.setScalar(0.05); scene.add(S.leg);
S.drain = P.makeDrain(); S.drain.position.set(-0.15, 0, 0.25); scene.add(S.drain);
S.win = P.makeWindow(); S.win.position.set(-0.4, 1.0, -0.88); scene.add(S.win);
S.fan = P.makeFan(); S.fan.position.set(1.0, 0, -0.62); S.fan.rotation.y = Math.PI + 0.4; scene.add(S.fan);
S.pipe = P.makePipe(); S.pipe.position.set(0.75, 0, -0.85); scene.add(S.pipe);
S.boxes = P.makeBoxes(); S.boxes.position.set(-0.25, 0, 1.0); scene.add(S.boxes);
S.cal = P.makeCalendar(); scene.add(S.cal);
S.towel = P.makeTowel(); S.towel.position.set(0.2, 0, 0.62); S.towel.rotation.y = 0.5; scene.add(S.towel);
const looseLegOf = S.cent.userData.legs.find((l) => l.i === 6 && l.side === 1);   // the leg that drops off

const PLAN = buildPlan(L, T_END);
const lineIdx = (t) => { let i = 0; while (i + 1 < L.length && PLAN.start(i + 1) <= t) i++; return i; };
const speaking = (t) => L.find((l) => t >= l.t - 0.02 && t < l.t + l.dur + 0.02);
const env = (l, t) => { if (!l) return 0; const i = Math.floor((t - l.t) * TL.fps); return l.env[Math.max(0, Math.min(l.env.length - 1, i))] || 0; };

// pos on the floor: [x, z, heading]; heading h faces (cos h, -sin h)
function place(o, p, y = 0) { o.position.set(p[0], y, p[1]); o.rotation.set(0, p[2] || 0, 0); }
function lerpP(a, b, u) { return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u]; }
function blendPose(a, b, w) { const o = {}; for (const k in a) o[k] = Array.isArray(a[k]) ? a[k].map((v, j) => v + (b[k][j] - v) * w) : a[k] + (b[k] - a[k]) * w; return o; }
const popS = (t, t0, s) => s * back((t - t0) / 0.25) * (t >= t0 ? 1 : 0);

function stateAt(t) {
  const i = lineIdx(t), cfg = PLAN.cfg[i], spk = speaking(t), e = env(spk, t), who = spk ? spk.who : null;
  const night = !!cfg.night;
  setLight(night ? NIGHT : DAY);
  S.win.userData.glassM.color.setHex(night ? 0x14234a : 0xbfe0f2); S.win.userData.moon.visible = night; S.win.userData.stars.forEach((s) => (s.visible = night));
  // centipede
  const cm = cfg.cent || { p0: PLAN.HOME, p1: PLAN.HOME, t0: 0, t1: 1 };
  const u = clamp01((t - cm.t0) / Math.max(1e-3, cm.t1 - cm.t0)), cp = lerpP(cm.p0, cm.p1, cm.lin ? u : ease(u));
  place(S.cent, cp); S.cent.visible = !cfg.hideCent;
  const travel = Math.hypot(cm.p1[0] - cm.p0[0], cm.p1[1] - cm.p0[1]) * u;
  animateCentipede(S.cent, cm.still ? 0.3 : t * 0.25 + travel * 30, 1, cm.still ? 0 : u > 0 && u < 1 ? 1 : 0.25);
  if (looseLegOf) looseLegOf.yaw.parent.visible = t < PLAN.legDrop;
  S.cent.userData.pos = cp;
  // Meatball
  const mbIn = PLAN.mbIn, k = t < mbIn ? 0 : back((t - mbIn) / 0.3);
  S.mb.visible = k > 0.001 && !cfg.hideMb; S.mb.scale.setScalar(S.MB * Math.max(0.001, k));
  const mp = cfg.mbAt || PLAN.MBPOS; place(S.mb, mp, (0.85 + 0.95 + 0.08) * S.MB * Math.max(0.001, k));
  P.poseMeatball(S.mb, t, P.MB_POSES[cfg.mbPose || 'idle'], who === 'M' ? e : 0, cfg.mood || 'calm');
  if (cfg.mood === 'whisper') S.mb.rotation.z = -0.18;
  // person
  const pc = cfg.person || {};
  const pp = pc.p1 ? lerpP(pc.p0, pc.p1, ease(clamp01((t - pc.t0) / (pc.t1 - pc.t0)))) : (pc.p0 || PLAN.PPOS);
  place(S.person, pp);
  let pose = P.PERSON_POSES[pc.pose || 'stand'];
  if (pc.from) { const a = P.PERSON_POSES[pc.from], w = ease(clamp01((t - PLAN.start(i)) / 0.35)); pose = blendPose(a, pose, w); }
  P.posePerson(S.person, t, pose, who === 'P' ? e : 0, pc.look ? pc.look(t) : 0);
  S.slipper.visible = pc.pose === 'slipper';
  // prey + props (each visible only where its line config shows it)
  PLAN.props(t, i, S, { place, popS, animate: animateCentipede });
}

// ---------- camera ----------
function camAt(t) {
  const sh = PLAN.shotAt(t), u = ease(clamp01((t - sh.s0) / (sh.mv || (sh.s1 - sh.s0))));
  let c, l;
  if (sh.c0) { c = V(sh.c0).lerp(V(sh.c1 || sh.c0), u); l = V(sh.l0).lerp(V(sh.l1 || sh.l0), u); }
  else {
    const tg = PLAN.anchor(sh.tgt, S), yaw = (sh.yaw + (sh.dyaw ?? 8) * u) * Math.PI / 180, d = sh.dist * (1 + ((sh.push ?? 0.88) - 1) * u);
    l = tg.clone().add(new THREE.Vector3(0, sh.ly || 0, 0));
    c = tg.clone().add(new THREE.Vector3(Math.cos(yaw) * d, sh.h * (d / sh.dist), Math.sin(yaw) * d));
  }
  camera.position.copy(c); camera.lookAt(l);
  if (S.cal.visible) { S.cal.lookAt(camera.position.x, S.cal.position.y, camera.position.z); }
}

// ---------- 2D layer ----------
const comp = makeCompositor(canvas);
function overlay(t) {
  const c = comp.ctx; comp.begin();
  const i = lineIdx(t), cfg = PLAN.cfg[i];
  if (cfg.night) { c.save(); c.globalCompositeOperation = 'multiply'; c.fillStyle = '#9db0ea'; c.fillRect(0, 0, 1080, 1920); c.restore(); }
  const mc = PLAN.mapAt(t); if (mc) drawMapCard(c, mc.age, mc.arrow, mc.fade);
  const lc = PLAN.leaseAt(t); if (lc) drawLease(c, lc.age, lc.sig, lc.fade);
  const fc = PLAN.cardAt(t); if (fc) drawFactCard(c, fc.card, fc.src, fc.age, fc.fade);
  const cl = L.find((l) => t >= l.t - 0.05 && t < Math.min(l.t + l.dur + 0.3, (L[l.i + 1] || { t: 1e9 }).t - 0.05));
  if (cl) drawCaption(c, cl, t - cl.t);
  drawWatermark(c);
}

function render(t) { stateAt(t); camAt(t); renderer.render(scene, camera); overlay(t); }
function frame(t, q = 0.92) { render(t); return comp.jpeg(q); }
window.SIM = { render, frame, TOTAL: T_END, ready: Promise.all(['900 92px Inter', '700 36px Inter', '600 22px Lora'].map((f) => document.fonts.load(f))).then(() => true) };
