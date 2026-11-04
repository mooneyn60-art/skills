// 3D Meatball explainer, generic episode page (pest.html?ep=roach|bedbugs&tl=timeline-TAG.json).
// Same format as the approved house-centipede Short: person asks, Meatball answers, word captions, white fact cards.
// The episode module (ep_roach.js / ep_bedbugs.js) builds its set + cast and returns per-line shots and a props(t) hook.
// Every value is a pure function of t, so any frame renders alone (chunked + restart-safe renders).
// Shot: {tgt, yaw (deg), dist, h, ly, dyaw, push} orbit-push around tgt ([x,y,z] or fn(S) -> [x,y,z]),
//       or {c0, c1, l0, l1, mv} explicit camera + look-at moves. Each shot after the first in a line has `at` (s).
import * as THREE from 'three';
import { makeCompositor } from './overlay2d.js';
import * as P from './props.js';
import { drawCaption, drawFactCard, drawWatermark } from './cards.js';

const QP = new URLSearchParams(location.search);
const TL = await (await fetch('../work/' + (QP.get('tl') || 'timeline.json'))).json();
const EP = await import(QP.get('ep') === 'bedbugs' ? './ep_bedbugs.js' : './ep_roach.js');
const L = TL.lines, T_END = TL.total;
const clamp01 = (x) => Math.max(0, Math.min(1, x));
const ease = (x) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
const back = (x) => { const c = 1.7; x = clamp01(x); return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const V = (a) => new THREE.Vector3(...a);

// ---------- renderer + lights ----------
const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(QP.has('px') ? +QP.get('px') : 0.5); renderer.setSize(1080, 1920, false);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(42, 1080 / 1920, 0.002, 30);
const LT = EP.LIGHT;
scene.background = new THREE.Color(LT.bg);
const hemi = new THREE.HemisphereLight(LT.hemi[0], LT.hemi[1], LT.hemi[2]); scene.add(hemi);
const sun = new THREE.DirectionalLight(LT.sun[0], LT.sun[1]); sun.castShadow = true; sun.shadow.mapSize.set(1024, 1024);
sun.position.set(...LT.sunPos); sun.target.position.set(...LT.sunTgt);
Object.assign(sun.shadow.camera, { left: -1.6, right: 1.6, top: 1.6, bottom: -1.6, near: 0.3, far: 10 }); sun.shadow.bias = -0.0003; sun.shadow.normalBias = 0.002;
scene.add(sun, sun.target);
for (const [c, i, p] of LT.lamps) { const l = new THREE.PointLight(c, i, 4, 1.5); l.position.set(...p); scene.add(l); }

// ---------- timing helpers (shared with the episode) ----------
const PRE = 0.12;
const start = (i) => (i === 0 ? 0 : L[i].t - PRE);
const end = (i) => (i + 1 < L.length ? start(i + 1) : T_END);
const W = (i, k) => L[i].t + Math.max(0, L[i].words[Math.min(k, L[i].words.length - 1)][0]);
const cut = (i, k) => W(i, k) - 0.1;
const popS = (t, t0, s, d = 0.25) => s * back((t - t0) / d) * (t >= t0 ? 1 : 0);
const vis = (o, a, b, t) => { o.visible = t >= a && t < b; return o.visible; };
const place = (o, p, y) => { o.position.set(p[0], y, p[1]); o.rotation.set(0, p[2] || 0, 0); };   // p = [x, z, heading]
const lerpA = (a, b, u) => a.map((v, j) => v + (b[j] - v) * u);
const fwd = (h, d) => [Math.cos(h) * d, -Math.sin(h) * d];   // heading h faces (cos h, -sin h)
const K = { L, T_END, start, end, W, cut, popS, vis, place, lerpA, fwd, ease, clamp01, back, V };

// ---------- cast ----------
const S = { scene };
S.mb = P.makeMeatball(); scene.add(S.mb);
S.person = P.makePerson(EP.SHIRT); scene.add(S.person);
const PLAN = EP.build(scene, S, K);   // {cfg[i]: {shots, cardWord, mbPose, mood, person}, MB, MBPOS, mbY, PPOS, mbIn, mbOut, props(t, i)}
const lineIdx = (t) => { let i = 0; while (i + 1 < L.length && start(i + 1) <= t) i++; return i; };
const speaking = (t) => L.find((l) => t >= l.t - 0.02 && t < l.t + l.dur + 0.02);
const env = (l, t) => { if (!l) return 0; const i = Math.floor((t - l.t) * TL.fps); return l.env[Math.max(0, Math.min(l.env.length - 1, i))] || 0; };
function blendPose(a, b, w) { const o = {}; for (const k in a) o[k] = Array.isArray(a[k]) ? a[k].map((v, j) => v + (b[k][j] - v) * w) : a[k] + (b[k] - a[k]) * w; return o; }

// shots flattened with absolute [s0, s1)
const SHOTS = [];
PLAN.cfg.forEach((c, i) => (c.shots || [{}]).forEach((s, j) => SHOTS.push({ ...s, s0: j === 0 ? start(i) : s.at, i })));
SHOTS.forEach((s, k) => { s.s1 = k + 1 < SHOTS.length ? SHOTS[k + 1].s0 : T_END; });
const shotAt = (t) => { let k = 0; while (k + 1 < SHOTS.length && SHOTS[k + 1].s0 <= t) k++; return SHOTS[k]; };
// fact cards: from the card word until the next card, held >= 2.2 s and past the line end
const CARDS = [];
L.forEach((l, i) => { if (l.card) CARDS.push({ card: l.card, src: l.src, s0: W(i, PLAN.cfg[i].cardWord || 0) - 0.08, min: end(i) + 0.2 }); });
CARDS.forEach((c, k) => { c.s1 = Math.min(Math.max(c.min, c.s0 + 2.2), k + 1 < CARDS.length ? CARDS[k + 1].s0 : T_END - 0.15); });
const cardAt = (t) => { const c = CARDS.find((c) => t >= c.s0 && t < c.s1); return c && { ...c, age: t - c.s0, fade: clamp01((c.s1 - t) / 0.15) }; };

function stateAt(t) {
  const i = lineIdx(t), cfg = PLAN.cfg[i], spk = speaking(t), e = env(spk, t), who = spk ? spk.who : null;
  // Meatball pops in at mbIn, pops out at mbOut
  const k = (t < PLAN.mbIn ? 0 : back((t - PLAN.mbIn) / 0.3)) * (PLAN.mbOut != null ? 1 - ease((t - PLAN.mbOut) / 0.25) : 1);
  const MB = PLAN.MB * Math.max(0.001, k), mp = cfg.mbAt || PLAN.MBPOS;
  S.mb.visible = k > 0.001 && !cfg.hideMb; S.mb.scale.setScalar(MB);
  place(S.mb, mp, PLAN.mbY + 1.88 * MB);
  P.poseMeatball(S.mb, t, P.MB_POSES[cfg.mbPose || 'idle'], who === 'M' ? e : 0, cfg.mood || 'calm');
  // person
  const pc = cfg.person || {}, pp = pc.p0 || PLAN.PPOS;
  place(S.person, pp, PLAN.personY || 0);
  let pose = PLAN.POSES[pc.pose || PLAN.pose0];
  if (pc.from) pose = blendPose(PLAN.POSES[pc.from], pose, ease(clamp01((t - start(i)) / 0.35)));
  P.posePerson(S.person, t, pose, who === 'P' ? e : 0, pc.look ? pc.look(t) : 0);
  PLAN.props(t, i, who === 'P' ? e : 0);
}

// ---------- camera ----------
const tgtOf = (g) => V(typeof g === 'function' ? g(S) : g);
function camAt(t) {
  const sh = shotAt(t), u = ease(clamp01((t - sh.s0) / (sh.mv || (sh.s1 - sh.s0))));
  let c, l;
  if (sh.c0) { c = V(sh.c0).lerp(V(sh.c1 || sh.c0), u); l = V(sh.l0).lerp(V(sh.l1 || sh.l0), u); }
  else {
    const tg = tgtOf(sh.tgt), yaw = (sh.yaw + (sh.dyaw ?? 8) * u) * Math.PI / 180, d = sh.dist * (1 + ((sh.push ?? 0.88) - 1) * u);
    l = tg.clone().add(new THREE.Vector3(0, sh.ly || 0, 0));
    c = tg.clone().add(new THREE.Vector3(Math.cos(yaw) * d, sh.h * (d / sh.dist), Math.sin(yaw) * d));
  }
  if (sh.shake) { const a = sh.shake.a * Math.exp(-Math.max(0, t - sh.shake.t) / 0.12) * (t >= sh.shake.t ? 1 : 0); c.y += a * Math.sin(t * 90); c.x += a * 0.6 * Math.cos(t * 77); }
  camera.position.copy(c); camera.lookAt(l);
  if (PLAN.faceCam) PLAN.faceCam(camera);
}

// ---------- 2D layer ----------
const comp = makeCompositor(canvas);
function overlay(t) {
  const c = comp.ctx; comp.begin();
  const fc = cardAt(t); if (fc) drawFactCard(c, fc.card, fc.src, fc.age, fc.fade);
  const cl = L.find((l) => t >= l.t - 0.05 && t < Math.min(l.t + l.dur + 0.3, (L[l.i + 1] || { t: 1e9 }).t - 0.05));
  if (cl) drawCaption(c, cl, t - cl.t);
  drawWatermark(c);
}

function render(t) { stateAt(t); camAt(t); renderer.render(scene, camera); overlay(t); }
function frame(t, q = 0.92) { render(t); return comp.jpeg(q); }
window.SIM = { render, frame, TOTAL: T_END, ready: Promise.all(['900 92px Inter', '700 36px Inter', '600 22px Lora'].map((f) => document.fonts.load(f))).then(() => true) };
