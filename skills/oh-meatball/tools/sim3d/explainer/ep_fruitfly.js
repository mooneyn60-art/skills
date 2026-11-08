// Episode: fruit fly (YouTube Short ~15.8 s, 8 lines, loops) + micro-loop (KEY=loop, one line, ~7.3 s, seamless orbit).
// NEW opening (research 68): frame 1 is already a macro on fruit flies walking on a spotted banana, narration from 0.0 s.
// Same night kitchen as ep_housefly.js. Beats: flies on the banana (hook) -> "rode home on your fruit" -> the person
// holds up the banana -> flies rise out of the sink drain -> eggs pop on the banana + "~500" calendar -> "1 WEEK" calendar,
// a swarm lifts off the bowl -> "See you next week." cranes back to the opening macro.
// Source: Univ. of Kentucky ENTFACT-621 (1/8 inch, red eyes, ~500 eggs, egg to adult in about a week, breed in drains).
import * as THREE from 'three';
import { mat, mesh, box, cyl, limbGeo, ICO, ICO1 } from './lib.js';
import * as P from './props.js';
import * as Q from './props2.js';
import { makeKitchen, LIGHT as KL } from './ep_housefly.js';

export const SHIRT = 0x3f7f6a;
export const LIGHT = KL;

const TOP = 0.9;
const FS = 0.0065;              // fruit fly ~3 mm; drawn ~2x so it reads
const BOWL = [-0.3, -0.3], BR = 0.11, BH = 0.05;
const SINK = [0.62, -0.3];
const TAU = Math.PI * 2;

// six jointed legs (same shape as props2 sixLegs so Q.animateLegs walks them)
function sixLegs(g, m, y, x0, dx, len, r) {
  const legs = [];
  for (const s of [-1, 1]) for (let k = 0; k < 3; k++) {
    const hip = new THREE.Group(); hip.position.set(x0 - k * dx, y, s * 0.08); hip.rotation.order = 'YXZ'; g.add(hip);
    hip.add(mesh(limbGeo(r, r * 0.8, len * 0.45, 4), m));
    const knee = new THREE.Group(); knee.position.z = len * 0.45; hip.add(knee);
    knee.add(mesh(limbGeo(r * 0.8, r * 0.4, len * 0.6, 4), m));
    const kn = 0.15 + Math.asin(Math.min(0.95, (y + len * 0.45 * Math.sin(0.15)) / (len * 0.6)));
    legs.push({ hip, knee, s, k, kn, yaw0: (k - 1) * -0.7 });
  }
  return legs;
}

// fruit fly (Drosophila): tan thorax, banded abdomen, big bright-red eyes, clear wings folded flat over the back
export function makeFruitFly() {
  const g = new THREE.Group(), body = new THREE.Group(); g.add(body);
  const tan = mat(0xc99a58), brn = mat(0x5a3a1c), legM = mat(0xb48a52);
  const th = mesh(ICO1, tan); th.scale.set(0.2, 0.17, 0.17); th.position.set(0.1, 0.3, 0); body.add(th);
  const ab = mesh(ICO1, mat(0xb07a3e)); ab.scale.set(0.28, 0.15, 0.17); ab.position.set(-0.2, 0.27, 0); body.add(ab);
  for (let k = 0; k < 3; k++) { const b = mesh(ICO1, brn, false); b.scale.set(0.03, 0.152, 0.16 - k * 0.025); b.position.set(-0.14 - k * 0.09, 0.275, 0); body.add(b); }
  const hd = mesh(ICO1, tan); hd.scale.set(0.11, 0.13, 0.15); hd.position.set(0.34, 0.31, 0); body.add(hd);
  for (const s of [-1, 1]) { const e = mesh(ICO1, mat(0xe0281c, { emissive: 0x3a0804 }), false); e.scale.set(0.085, 0.12, 0.08); e.position.set(0.36, 0.33, s * 0.1); body.add(e); }
  for (const s of [-1, 1]) { const a = mesh(limbGeo(0.012, 0.006, 0.1, 3), brn, false); a.position.set(0.44, 0.38, s * 0.04); a.rotation.set(0, 0, -0.9); body.add(a); }
  const wm = new THREE.MeshLambertMaterial({ color: 0xe6eef4, transparent: true, opacity: 0.5, side: THREE.DoubleSide });
  const wings = [-1, 1].map((s) => { const w = new THREE.Group(); w.position.set(0.05, 0.42, s * 0.04); const p = mesh(ICO1, wm, false); p.scale.set(0.34, 0.01, 0.11); p.position.set(-0.27, 0, s * 0.06); w.add(p); w.rotation.y = s * 0.12; body.add(w); return w; });
  const legs = sixLegs(body, legM, 0.2, 0.2, 0.1, 0.36, 0.018);
  g.userData = { body, legs, wings, ants: [] };
  return g;
}

function makeBanana() {
  const g = new THREE.Group();
  const pts = [[-0.1, 0.012, -0.03], [-0.05, 0.0, 0.004], [0.0, -0.002, 0.016], [0.05, 0.0, 0.01], [0.1, 0.014, -0.022]].map((p) => new THREE.Vector3(...p));
  const curve = new THREE.CatmullRomCurve3(pts);
  const tube = new THREE.Mesh(new THREE.TubeGeometry(curve, 24, 0.017, 6, false), mat(0xe9c63a)); tube.castShadow = true; g.add(tube);
  for (const [u, c] of [[0, 0x4a3218], [1, 0x3a2810]]) { const e = mesh(ICO1, mat(c)); e.scale.set(0.012, 0.012, 0.012); e.position.copy(curve.getPoint(u)); g.add(e); }
  // brown ripe spots on the top surface
  for (let k = 0; k < 26; k++) { const u = 0.08 + 0.84 * ((k * 0.618) % 1), p = curve.getPoint(u), a = (k * 2.4) % 1.6 - 0.8;
    const s = mesh(ICO1, mat(0x6a4416), false); s.scale.set(0.0016 + 0.001 * ((k * 7) % 3) / 2, 0.00025, 0.0016); s.position.set(p.x + Math.sin(a) * 0.004, p.y + 0.0165 * Math.cos(a), p.z + Math.sin(a) * 0.012); g.add(s); }
  g.userData = { curve };
  return g;
}

function makeBowl() {
  const g = new THREE.Group();
  const side = new THREE.Mesh(new THREE.CylinderGeometry(BR, BR * 0.6, BH, 18, 1, true), mat(0x3d6fa8, { side: THREE.DoubleSide })); side.position.y = BH / 2; side.castShadow = true; g.add(side);
  const base = cyl(BR * 0.6, BR * 0.6, 0.006, 0x3d6fa8, 18); base.position.y = 0.003; g.add(base);
  const rim = mesh(new THREE.TorusGeometry(BR, 0.005, 4, 22), mat(0x5a8cc4)); rim.rotation.x = Math.PI / 2; rim.position.y = BH; g.add(rim);
  const ap = mesh(ICO1, mat(0xc0282a)); ap.scale.setScalar(0.04); ap.position.set(-0.04, BH - 0.005, -0.04); g.add(ap);
  const or = mesh(ICO1, mat(0xf08a1c)); or.scale.setScalar(0.042); or.position.set(0.045, BH - 0.006, -0.035); g.add(or);
  const ap2 = mesh(ICO1, mat(0x8ab43a)); ap2.scale.setScalar(0.036); ap2.position.set(0.0, BH - 0.01, 0.05); g.add(ap2);
  return g;
}

export function build(scene, S, K) {
  const { L, T_END, start, end, W, cut, popS, vis, place, ease, clamp01 } = K;
  const LOOP = L.length === 1;
  scene.add(makeKitchen());
  S.bowl = makeBowl(); S.bowl.position.set(BOWL[0], TOP, BOWL[1]); scene.add(S.bowl);
  S.ban = makeBanana(); S.ban.position.set(BOWL[0], TOP + BH + 0.03, BOWL[1] + 0.005); S.ban.rotation.y = 0.35; scene.add(S.ban);
  S.ban.updateMatrixWorld(true);
  const curve = S.ban.userData.curve;
  const onBan = (u, side = 0) => { const p = curve.getPoint(u).applyMatrix4(S.ban.matrixWorld); const tg = curve.getTangent(u).transformDirection(S.ban.matrixWorld);
    return { p: [p.x + side * 0.004 * -tg.z, p.y + 0.0165, p.z + side * 0.004 * tg.x], h: Math.atan2(-tg.z, tg.x) }; };
  // the drain: a dark disc in the sink basin
  S.drain = cyl(0.022, 0.022, 0.002, 0x15171a, 16); S.drain.position.set(SINK[0], TOP + 0.006, SINK[1]); scene.add(S.drain);
  const grate = mesh(new THREE.TorusGeometry(0.014, 0.0025, 4, 16), mat(0x9aa0a6)); grate.rotation.x = Math.PI / 2; grate.position.set(SINK[0], TOP + 0.0075, SINK[1]); scene.add(grate);

  // cast of flies: 5 on the banana (index 0 = the hero), 6 drain flies, 14 swarm flies
  const SPOTS = [[0.48, 0], [0.3, -1], [0.66, 1], [0.2, 1], [0.8, -1]];
  S.flies = SPOTS.map(() => { const f = makeFruitFly(); f.scale.setScalar(FS); scene.add(f); return f; });
  S.dflies = []; for (let k = 0; k < 6; k++) { const f = makeFruitFly(); f.scale.setScalar(FS); scene.add(f); S.dflies.push(f); }
  S.swarm = []; for (let k = 0; k < 14; k++) { const f = makeFruitFly(); f.scale.setScalar(FS); scene.add(f); S.swarm.push(f); }
  S.eggs = []; for (let k = 0; k < 40; k++) { const e = Q.makeBugEgg(); e.scale.setScalar(0.0001); scene.add(e); S.eggs.push(e); }
  S.cal500 = Q.makeCal('ONE FEMALE', '~500 EGGS'); scene.add(S.cal500);
  S.calWk = Q.makeCal('EGG TO FLY', '1 WEEK'); scene.add(S.calWk);
  S.handBan = makeBanana(); S.handBan.scale.setScalar(1.0); S.handBan.position.set(0, -0.07, 0); S.handBan.rotation.set(0, 0, Math.PI / 2); S.person.userData.hands[1].add(S.handBan);

  const hero = onBan(SPOTS[0][0], SPOTS[0][1]), F0 = hero.p;
  const OPEN = { c0: [F0[0] + 0.024, F0[1] + 0.013, F0[2] + 0.024], l0: [F0[0], F0[1] + 0.001, F0[2]],
    c1: [F0[0] + 0.022, F0[1] + 0.012, F0[2] + 0.026], l1: [F0[0], F0[1] + 0.001, F0[2]], mv: 2.2 };
  const MBPOS = [-0.08, -0.17, -Math.PI / 2 - 0.5], PPOS = [0.0, 1.45, Math.PI / 2];
  const mbAt = (S) => [S.mb.position.x, S.mb.position.y, S.mb.position.z];
  const PSHOT = { c0: [-0.14, 1.42, -0.22], l0: [0.0, 1.76, 1.45], c1: [-0.12, 1.43, -0.12], l1: [0.0, 1.78, 1.45] };
  const BOWLT = [BOWL[0], TOP + BH + 0.03, BOWL[1]];
  const DR = [SINK[0], TOP + 0.006, SINK[1]];
  const cfg = L.map(() => ({ shots: [{}] }));
  const set = (i, o) => Object.assign(cfg[i], o);
  let home = T_END, out = T_END;
  if (!LOOP) {
    set(0, { shots: [{ ...OPEN }, { at: cut(0, 5) + 0.05, tgt: BOWLT, yaw: 62, dist: 0.32, h: 0.16, dyaw: 10, push: 0.85 }] });
    set(1, { cardWord: 3, mood: 'deadpan', shots: [{ tgt: (S) => [S.mb.position.x - 0.03, S.mb.position.y, S.mb.position.z], yaw: 70, dist: 0.42, h: 0.04, dyaw: 6, push: 0.9 },
      { at: cut(1, 3), tgt: onBan(SPOTS[2][0], SPOTS[2][1]).p, yaw: 118, dist: 0.05, h: 0.016, dyaw: 14, push: 0.85 }] });
    set(2, { person: { pose: 'slipper', from: 'stand' }, shots: [{ ...PSHOT }] });
    set(3, { cardWord: 3, mood: 'smug', shots: [{ tgt: [DR[0], DR[1] + 0.02, DR[2]], yaw: 75, dist: 0.2, h: 0.14, dyaw: 12, push: 0.82 }] });
    set(4, { person: { pose: 'back', from: 'stand', look: (t) => 0.5 * Math.sin((t - start(4)) * 7) }, shots: [{ ...PSHOT }] });
    set(5, { cardWord: 2, mood: 'smug', shots: [{ tgt: onBan(0.4, 0).p, yaw: 95, dist: 0.07, h: 0.03, dyaw: -12, push: 0.85 },
      { at: cut(5, 3), tgt: [BOWL[0] - 0.12, TOP + 0.07, BOWL[1] + 0.12], yaw: 60, dist: 0.32, h: 0.06, dyaw: 6, push: 0.9 }] });
    set(6, { cardWord: 0, mood: 'smug', shots: [{ tgt: [BOWL[0], TOP + 0.12, BOWL[1]], yaw: 80, dist: 0.5, h: 0.08, dyaw: 6, push: 1.12 }] });
    home = T_END - 0.08; out = W(7, 3) + 0.08;
    set(7, { mood: 'smug', mbPose: 'hips', shots: [{ tgt: (S) => [S.mb.position.x - 0.03, S.mb.position.y, S.mb.position.z], yaw: 75, dist: 0.42, h: 0.04, dyaw: 4, push: 0.9 },
      { at: out, c0: [MBPOS[0] + 0.12, TOP + 0.14, MBPOS[1] + 0.32], l0: [MBPOS[0], TOP + 0.1, MBPOS[1]], c1: OPEN.c0, l1: OPEN.l0, mv: home - out }] });
    cfg[0].hideMb = 1;
  } else set(0, { hideMb: 1, shots: [{ c0: OPEN.c0, l0: OPEN.l0 }] });   // the loop camera is set in faceCam

  const RNG = (k) => { const x = Math.sin(k * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
  const flap = (f, t, on, sp = 90) => f.userData.wings.forEach((w, k) => { const s = k ? 1 : -1; w.rotation.x = on ? s * (0.3 + 0.8 * Math.sin(t * sp + k * 0.3)) : 0; w.rotation.y = s * (on ? 0.15 : 0.12); });
  // periodic helpers: every motion repeats exactly over T_END so frame T_END == frame 0 (micro-loop)
  const PER = LOOP ? Math.round(T_END * 30) / 30 : T_END;   // micro-loop period = the exact rendered frame count
  const cyc = (n) => (n * TAU) / PER;
  let tNow = 0;

  function props(t, i) {
    tNow = t;
    // flies on the banana: shuffle along it, legs stepping, a little grooming turn
    S.flies.forEach((f, k) => {
      const [u0, sd] = SPOTS[k], wob = 0.03 * Math.sin(cyc(1 + (k % 2)) * t + k), st = onBan(Math.min(0.93, Math.max(0.07, u0 + wob)), sd);
      f.visible = !(i === 6 && t > W(6, 2) && k > 0);
      place(f, [st.p[0], st.p[2], st.h + (k % 2 ? Math.PI : 0) + 0.4 * Math.sin(cyc(1) * t + k)], st.p[1]);
      Q.animateLegs(f, (Math.round(3 * PER) / PER) * t + k * 0.3, k === 0 ? 0.5 : 0.35); flap(f, t, false);
    });
    // drain flies spiral up out of the sink on "drain" (line 3)
    S.dflies.forEach((f, k) => {
      const t0 = LOOP ? 1e9 : W(3, 5) - 0.1 + k * 0.08;
      if (!vis(f, t0, LOOP ? 0 : end(4), t)) return;
      const d = t - t0, a = k * 1.05 + d * 5, r = 0.01 + 0.025 * d;
      f.position.set(DR[0] + Math.cos(a) * r, DR[1] + 0.004 + 0.06 * d + 0.004 * Math.sin(t * 17 + k), DR[2] + Math.sin(a) * r);
      f.rotation.set(0, -a - Math.PI / 2, 0.15); flap(f, t + k * 0.07, true);
      Q.animateLegs(f, 0, 0); f.scale.setScalar(popS(t, t0, FS, 0.12));
    });
    // eggs pop on the banana on "eggs" (line 5)
    const te = LOOP ? 1e9 : W(5, 4) - 0.12;
    S.eggs.forEach((e, k) => {
      if (!vis(e, te + k * 0.012, LOOP ? 0 : end(6), t)) return;
      const st = onBan(0.3 + 0.24 * ((k * 0.618) % 1), ((k * 0.37) % 1) * 2 - 1);
      e.position.set(st.p[0], st.p[1] - 0.0005, st.p[2]); e.rotation.set(0, k, 0); e.scale.setScalar(Math.max(0.0001, popS(t, te + k * 0.012, 0.0011, 0.18)));
    });
    if (!LOOP && vis(S.cal500, W(5, 3) - 0.08, end(5), t)) { S.cal500.position.set(BOWL[0] - 0.17, TOP, BOWL[1] + 0.1); S.cal500.scale.setScalar(popS(t, W(5, 3) - 0.08, 1.4)); }
    else S.cal500.visible = false;
    if (!LOOP && vis(S.calWk, W(6, 4) - 0.08, end(6), t)) { S.calWk.position.set(BOWL[0] + 0.2, TOP, BOWL[1] + 0.12); S.calWk.scale.setScalar(popS(t, W(6, 4) - 0.08, 1.4)); }
    else S.calWk.visible = false;
    // the swarm lifts off the bowl on "fly" (line 6)
    const tS = LOOP ? 1e9 : W(6, 2) - 0.1;
    S.swarm.forEach((g, k) => {
      if (!vis(g, tS + k * 0.03, LOOP ? 0 : end(6), t)) return;
      const d = t - tS - k * 0.03, a = k * 2.4 + d * (2.5 + RNG(k) * 2), r = 0.03 + 0.07 * RNG(k + 3) + 0.04 * d;
      g.position.set(BOWL[0] + Math.cos(a) * r, TOP + BH + 0.03 + d * (0.09 + 0.06 * RNG(k + 11)) + 0.006 * Math.sin(t * 13 + k), BOWL[1] + Math.sin(a) * r);
      g.rotation.set(0.2 * Math.sin(t * 9 + k), -a - Math.PI / 2, 0.15); flap(g, t + k * 0.11, true);
      g.scale.setScalar(popS(t, tS + k * 0.03, FS, 0.15)); Q.animateLegs(g, 0, 0);
    });
    S.handBan.visible = !LOOP && i === 2;
  }
  // micro-loop camera: a closed orbit around the hero fly (yaw sways, distance breathes), identical at t = 0 and t = T_END
  function faceCam(cam) {
    if (S.cal500.visible) S.cal500.lookAt(cam.position.x, S.cal500.position.y, cam.position.z);
    if (S.calWk.visible) S.calWk.lookAt(cam.position.x, S.calWk.position.y, cam.position.z);
    if (!LOOP) return;
    const ph = cyc(1) * tNow, yaw = 0.78 + 0.5 * Math.sin(ph), d = 0.04 * (1 + 0.12 * Math.sin(2 * ph)), F = onBan(SPOTS[0][0], SPOTS[0][1]).p;
    cam.position.set(F[0] + Math.cos(yaw) * d, F[1] + 0.014 + 0.004 * Math.cos(ph), F[2] + Math.sin(yaw) * d);
    cam.lookAt(F[0], F[1] + 0.002, F[2]);
  }
  const POSES = { ...P.PERSON_POSES };
  return { cfg, props, faceCam, POSES, pose0: 'stand', MB: 0.06, MBPOS, mbY: TOP, PPOS, mbIn: LOOP ? 1e9 : start(1), mbOut: LOOP ? null : home - 0.5 };
}
