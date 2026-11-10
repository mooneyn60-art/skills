// 3D long-form (16:9): "The 30-legged bug in your house you should never kill" — one bathroom story, ~85 lines.
// explainer.html?plan=long&tl=timeline-centlong.json&wide=1&vfov=30. Same set + cast as the approved centipede Short
// (explainer.js owns the scene); this file maps each script row's `beat` to shots, blocking and prop timing.
// Beats reuse the planKit beats (opening/squish/lunge/legDrop/shrug/lease/rent) and the TikTok-cut line plans,
// re-indexed by beat name, plus new long-form beats (multi-prey, stop-go run, lights-on, baby lineup, calendars, ...).
// Words are found by text (wi), so the script can change without breaking the timing.
// Every value is a pure function of t (chunked, restart-safe renders).
import * as THREE from 'three';
import { planKit, OPEN, clamp01, ease } from './shots.js';
import { makeCentipede, animateCentipede } from './lib.js';
import * as P from './props.js';
import { makeCal } from './props2.js';

const DK = 1.3;   // 16:9 at vfov 30 is tighter vertically than the 9:16 cut: close orbit shots pull back by this much

export function buildPlanLong(L, T_END, S, scene, rows) {
  const K = planKit(L, T_END);
  const { start, end, W, HOME, MBPOS, PPOS, PSEAT, fwd, side, at, CENT0, LUNGE, C2, LEG, mbYaw, pYaw, cfg, set, beat, vis, fx } = K;
  const norm = (s) => s.toLowerCase().replace(/[^a-z0-9']/g, '');
  const wi = (i, w) => { const k = L[i].words.findIndex((x) => norm(x[2]).startsWith(norm(w))); return k < 0 ? 0 : k; };
  const Wt = (i, w) => W(i, wi(i, w));
  const cutw = (i, w) => Wt(i, w) - 0.1;
  const B = (name) => rows.map((r, i) => (r.beat === name ? i : -1)).filter((i) => i >= 0);
  const B1 = (name) => B(name)[0];

  // ---------- extra props ----------
  const bath = scene.children.find((g) => g.userData.props), tubWater = bath && bath.userData.props[1].children[1];
  const lineup = [4, 5, 7, 9, 11, 13, 15].map((pairs, k) => {
    const c = makeCentipede(); for (const l of c.userData.legs) if (l.i >= pairs) l.yaw.parent.visible = false;
    c.userData.s0 = 0.017 + k * 0.006; scene.add(c); return c;
  });
  const babies = [0, 1, 2, 3, 4].map(() => { const b = P.makeBabyCentipede(); scene.add(b); return b; });
  const cal150 = makeCal('UP TO', '150'); scene.add(cal150);
  const cal3 = makeCal('TO GROW UP', '3 YRS'); scene.add(cal3);
  const held = [P.makeSpider(), P.makeSilverfish(), P.makeAnt()]; held.forEach((o) => scene.add(o));
  const heldS = [0.011, 0.014, 0.01];

  const BB = at(HOME, 0.067), BABY = [LEG[0] + 0.012, LEG[1] - 0.018, 1.2];
  const MBC = [MBPOS[0], 0.113, MBPOS[1]], calP = [MBPOS[0] + 0.071, MBPOS[1] + 0.073];
  const calShot = { tgt: [(MBC[0] + calP[0]) / 2, 0.1, (MBC[2] + calP[1]) / 2], yaw: mbYaw, dist: 0.46, h: 0.03, dyaw: -5 };

  // ---------- beats (line config for line i of this cut) ----------
  const pDist = [0.8, 1.0, 0.9, 1.1], pYawV = [0, -22, 18, 35];
  const mbV = [[0, 0.28, 0.02, 6], [13, 0.32, 0.03, -6], [-17, 0.24, 0.0, 4], [22, 0.36, 0.05, -5]];
  const centV = [{ yaw: 60, dist: 0.14, h: 0.07, dyaw: 20 }, { yaw: 200, dist: 0.12, h: 0.1, dyaw: -15 }, { yaw: 120, dist: 0.2, h: 0.15, dyaw: 12 }];
  const wideV = [
    { c0: [1.3, 1.25, 1.25], l0: [0.2, 0.15, -0.2], c1: [1.22, 1.2, 1.12], l1: [0.25, 0.1, -0.2] },
    { c0: [-0.3, 1.3, 1.3], l0: [0.6, 0.1, -0.3], c1: [-0.25, 1.22, 1.2], l1: [0.55, 0.08, -0.3] },
    { c0: [0.45, 0.28, 1.3], l0: [0.35, 0.1, -0.5], c1: [0.45, 0.24, 1.15], l1: [0.4, 0.08, -0.5] },
    { c0: [1.3, 0.65, 0.25], l0: [-0.5, 0.3, 0.15], c1: [1.25, 0.6, 0.15], l1: [-0.5, 0.25, 0.1] },
  ];
  const still = (p) => ({ p0: p, p1: p, t0: 0, t1: 1, still: 1 });
  const creep = (i) => ({ p0: HOME, p1: at(HOME, 0.035), t0: start(i), t1: end(i), lin: 1 });
  const chead = (S) => { const c = S.cent.position, h = S.cent.rotation.y, f = fwd(h, 0.018); return [c.x + f[0], 0.003, c.z + f[1]]; };
  const PR = (i, r) => (r.pose ? { pose: r.pose, from: 'stand' } : {});
  let legDrop = null, legRegrow = null, nightBase = null;
  const lights = {};   // line -> time the light comes on

  const BEATS = {
    opening: (i) => beat.opening(i, wi(i, '30'), wi(i, 'in')),
    squish: (i) => beat.squish(i),
    lunge: (i) => beat.lunge(i, wi(i, 'eating'), wi(i, 'eating')),
    pTalk: (i, r) => {
      const v = r.v || 0, far = r.pose === 'head' || r.pose === 'sign' || r.pose === 'slipper';
      return { person: PR(i, r), shots: [{ tgt: 'pHead', yaw: pYaw + pYawV[v], dist: far ? 1.3 : pDist[v], h: 0.0, ly: far ? -0.14 : -0.12, dyaw: v % 2 ? -5 : 5, push: 0.88 }] };
    },
    pLook: (i) => ({ person: { look: (t) => 0.7 * Math.sin((t - start(i)) * 4.5) }, shots: [
      { c0: [0.25, 0.9, 0.0], l0: [1.45, 1.5, -0.45], c1: [0.3, 0.93, -0.03], l1: [1.45, 1.55, -0.45] }] }),
    mb: (i, r) => {
      const [dy, d, h, dyaw] = mbV[r.v || 0];
      return { mbPose: r.pose || 'idle', mood: r.mood || 'calm', shots: [{ tgt: 'mb', yaw: mbYaw + dy, dist: d, h, dyaw, push: 0.88 }] };
    },
    swarm: (i) => ({ mbPose: 'hips', mood: 'deadpan', swarmAt: cutw(i, 'know'), shots: [
      { tgt: 'mb', yaw: mbYaw, dist: 0.23, h: 0.01, ly: 0.01, dyaw: 3, push: 0.9 },
      { at: cutw(i, 'know'), c0: [0.05, 0.07, 0.15], l0: [-0.4, 0.0, 0.18], c1: [-0.08, 0.05, 0.18], l1: [-0.42, 0, 0.2] }] }),
    swarm2: (i) => ({ mood: 'alarm', swarmAt: cutw(i, 'bigger'), shots: [
      { tgt: 'mb', yaw: mbYaw - 10, dist: 0.3, h: 0.02, dyaw: 4 },
      { at: cutw(i, 'bigger'), c0: [0.05, 0.07, 0.15], l0: [-0.4, 0.0, 0.18], c1: [-0.1, 0.05, 0.2], l1: [-0.42, 0, 0.2] }] }),
    crouch: () => ({ person: { pose: 'crouch', from: 'stand' }, shots: [
      { c0: [-0.3, 0.85, 0.55], l0: [1.3, 0.72, -0.42], c1: [-0.22, 0.85, 0.5], l1: [1.3, 0.76, -0.42] }] }),
    menu: (i) => ({ shots: [
      { tgt: [0.425, 0.004, -0.155], yaw: 90, dist: 0.17, h: 0.12, dyaw: 8, push: 0.9 },
      { at: cutw(i, 'silverfish'), tgt: [0.49, 0.004, -0.16], yaw: 70, dist: 0.17, h: 0.1, dyaw: -10, push: 0.9 },
      { at: cutw(i, 'bed'), tgt: [0.47, 0.004, -0.135], yaw: 20, dist: 0.11, h: 0.06, dyaw: 10, push: 0.85 }] }),
    cent: (i, r) => ({ cent: creep(i), shots: [{ tgt: 'cent', push: 0.85, ...centV[r.v || 0] }] }),
    multi: (i) => ({ cent: { p0: CENT0, p1: LUNGE, t0: Wt(i, 'catch') + 0.05, t1: Wt(i, 'catch') + 0.27, lin: 1 }, shots: [
      { tgt: 'cent', yaw: 75, dist: 0.16, h: 0.07, dyaw: 8 },
      { at: cutw(i, 'several'), tgt: [LUNGE[0] + 0.03, 0.004, LUNGE[1] - 0.01], yaw: 30, dist: 0.1, h: 0.06, dyaw: 12, push: 0.88 }] }),
    multi2: () => ({ cent: still(LUNGE), shots: [{ tgt: [LUNGE[0] + 0.03, 0.004, LUNGE[1] - 0.01], yaw: 110, dist: 0.09, h: 0.05, dyaw: 15, push: 0.88 }] }),
    drain: (i) => ({ cent: { p0: [-0.18, 0.255, -0.2], p1: [-0.1, 0.24, -0.2], t0: start(i) + 0.6, t1: end(i), y: 0.006 }, shots: [
      { c0: [0.35, 0.05, 0.55], l0: [-0.15, 0, 0.25], c1: [0.02, 0.06, 0.34], l1: [-0.15, 0, 0.25] },
      { at: cutw(i, 'like'), tgt: [-0.12, 0.004, 0.245], yaw: 40, dist: 0.12, h: 0.12, dyaw: 15, push: 0.85 }] }),
    drainClose: (i) => ({ cent: { p0: [-0.13, 0.25, 2.6], p1: [-0.06, 0.21, 2.6], t0: start(i), t1: end(i), y: 0.006, lin: 1 }, shots: [
      { tgt: [-0.13, 0.004, 0.25], yaw: -30, dist: 0.1, h: 0.16, dyaw: 25, push: 0.85 }] }),
    boxes: (i) => ({ cent: { p0: [0.05, 0.8, -2.61], p1: [-0.11, 0.895, -2.61], t0: start(i), t1: end(i), lin: 1 }, shots: [
      { tgt: [-0.2, 0.1, 0.95], yaw: -50, dist: 0.55, h: 0.1, dyaw: 8 },
      { at: cutw(i, 'cardboard'), tgt: 'cent', yaw: -40, dist: 0.15, h: 0.06, dyaw: 10 }] }),
    window: () => ({ night: 1, hideMb: 1, shots: [{ c0: [0.3, 0.9, 0.5], l0: [-0.4, 1.15, -0.88], c1: [0.15, 0.95, 0.25], l1: [-0.4, 1.15, -0.88] }] }),
    wide: (i, r) => ({ shots: [{ ...wideV[r.v || 0] }] }),
    night: (i) => ({ night: 1, cent: creep(i), shots: [{ c0: [0.25, 0.55, 0.45], l0: [-0.4, 1.4, -0.88], c1: [0.58, 0.1, 0.0], l1: [0.46, 0.0, -0.13], mv: 1.0 }] }),
    nightCrouch: (i) => ({ night: 1, cent: creep(i), person: { pose: 'crouch', from: 'stand' }, shots: [
      { c0: [-0.25, 0.85, 0.6], l0: [1.3, 0.72, -0.42], c1: [-0.18, 0.85, 0.55], l1: [1.3, 0.75, -0.42] }] }),
    welcome: (i) => ({ night: 1, mood: 'smug', person: { pose: 'crouch' }, cent: { p0: at(HOME, 0.035), p1: [0.43, -0.2, 1.9], t0: start(i) + 0.45, t1: end(i) },
      shots: [{ tgt: 'mb', yaw: mbYaw, dist: 0.28, h: 0.02, dyaw: -5 }, { at: start(i) + 0.5, tgt: 'cent', yaw: 40, dist: 0.13, h: 0.09, dyaw: 10 }] }),
    lightsOn: (i) => {
      const tl = Wt(i, 'light') + 0.05; lights[i] = tl;
      return { night: 1, nightUntil: tl, cent: { p0: [0.43, -0.2, 2.36], p1: [0.2, -0.43, 2.36], t0: tl + 0.25, t1: tl + 0.75, lin: 1 }, shots: [
        { tgt: [0.38, 0.004, -0.25], yaw: 65, dist: 0.2, h: 0.1, dyaw: 4, push: 0.95 },
        { at: cutw(i, 'flees'), tgt: [0.28, 0.02, -0.36], yaw: 45, dist: 0.32, h: 0.12, dyaw: 6 }] };
    },
    headHold: (i) => ({ person: { pose: 'back', from: 'stand', look: (t) => 0.4 * Math.sin((t - start(i)) * 6) }, shots: [
      { tgt: 'pHead', yaw: pYaw - 10, dist: 1.2, h: 0.0, ly: -0.12 },
      { at: W(i, 1) - 0.1, c0: [0.6, 0.08, -0.15], l0: [1.45, 1.3, -0.45], c1: [0.66, 0.1, -0.2], l1: [1.45, 1.4, -0.45] }] }),
    seated: (i, r) => ({ person: { p0: PSEAT, pose: 'seated' }, shots: [[
      { c0: [1.0, 0.95, 0.65], l0: [-0.35, 1.08, 0.32], c1: [0.94, 0.97, 0.62], l1: [-0.35, 1.12, 0.32] },
      { c0: [0.85, 1.02, -0.05], l0: [-0.35, 1.1, 0.32], c1: [0.8, 1.04, -0.01], l1: [-0.35, 1.14, 0.32] },
      { c0: [0.75, 1.0, -0.35], l0: [-0.4, 1.1, 0.32], c1: [0.7, 1.02, -0.3], l1: [-0.4, 1.13, 0.32] }][r.v || 0]] }),
    run: (i) => ({ cent: { p0: [1.05, -0.25, Math.PI], p1: [0.3, -0.25, Math.PI], t0: start(i) + 0.1, t1: end(i), lin: 1 }, shots: [
      { tgt: 'cent', yaw: 95, dist: 0.22, h: 0.07, dyaw: 0, push: 1 }] }),
    stopGo: (i) => {
      const a = start(i) + 0.05, b = Wt(i, 'stops') + 0.1, c = Wt(i, 'races') - 0.05, d = end(i);
      return { cent: { keys: [[a, 1.15, -0.28, Math.PI], [b, 0.85, -0.28, Math.PI], [c, 0.85, -0.28, Math.PI], [d, 0.4, -0.28, Math.PI]] }, shots: [
        { tgt: 'cent', yaw: 80, dist: 0.2, h: 0.06, dyaw: 0, push: 1 }] };
    },
    hunt: (i) => ({ cent: { p0: HOME, p1: at(HOME, 0.06), t0: Wt(i, 'pounce') - 0.02, t1: Wt(i, 'pounce') + 0.18, lin: 1 }, shots: [
      { tgt: [0.47, 0.004, -0.137], yaw: 72, dist: 0.16, h: 0.07, dyaw: 8 },
      { at: cutw(i, 'lasso'), tgt: [0.475, 0.004, -0.137], yaw: 200, dist: 0.07, h: 0.12, dyaw: 20, push: 0.85 }] }),
    head: (i, r) => ({ cent: still(HOME), shots: [[
      { tgt: chead, yaw: -17, dist: 0.055, h: 0.015, dyaw: 10, push: 0.85 },
      { tgt: chead, yaw: 35, dist: 0.05, h: 0.02, dyaw: -12, push: 0.85 },
      { tgt: chead, yaw: -60, dist: 0.06, h: 0.03, dyaw: 14, push: 0.85 }][r.v || 0]] }),
    backAway: (i) => ({ person: { p0: PPOS, p1: [1.85, -0.5, PPOS[2]], t0: L[i].t, t1: end(i) - 0.2, pose: 'back', from: 'stand' }, shots: [
      { c0: [0.65, 0.05, -0.2], l0: [1.45, 1.25, -0.45], c1: [0.6, 0.05, -0.18], l1: [1.55, 1.2, -0.46] },
      { at: cutw(i, 'will'), c0: [-0.1, 1.15, 0.45], l0: [1.5, 1.42, -0.45], c1: [0.0, 1.15, 0.4], l1: [1.75, 1.45, -0.48] }] }),
    bee: (i) => ({ shots: [
      { tgt: [0.43, 0.008, -0.105], yaw: 30, dist: 0.17, h: 0.06, dyaw: 8 },
      { at: cutw(i, 'like'), tgt: [0.43, 0.012, -0.095], yaw: 95, dist: 0.12, h: 0.04, dyaw: 10 }] }),
    legDrop: (i) => { legDrop = W(i, 1); return beat.legDrop(i); },
    shrug: (i) => beat.shrug(i),
    legClose: () => ({ cent: still(C2), shots: [{ tgt: [LEG[0], 0.003, LEG[1]], yaw: 120, dist: 0.05, h: 0.03, dyaw: 15, push: 0.85 }] }),
    regrow: (i) => {
      legRegrow = Wt(i, 'back') - 0.05; const sd = side(C2[2], 0.0045);
      return { cent: still(C2), shots: [
        { tgt: 'cent', yaw: 120, dist: 0.12, h: 0.08, dyaw: 10 },
        { at: cutw(i, 'grows'), tgt: 'hip', off: [sd[0], 0, sd[1]], yaw: 163, dist: 0.014, h: 0.034, dyaw: 8, push: 0.92 }] };
    },
    antennae: (i) => ({ cent: still(HOME), shots: [
      { tgt: chead, yaw: -17, dist: 0.09, h: 0.012, dyaw: 6, push: 0.9 },
      { at: cutw(i, 'antennae'), tgt: (S) => { const p = chead(S), f = fwd(HOME[2], 0.02); return [p[0] + f[0], 0.003, p[1 + 1] + f[1]]; }, yaw: 70, dist: 0.07, h: 0.03, dyaw: 12 }] }),
    tub: (i, r) => ({ cent: { p0: [-0.86, 0.02, 1.2], p1: [-0.8, 0.05, 1.2], t0: start(i), t1: end(i), y: 0.552, lin: 1 }, tubDry: 1, shots: [[
      { tgt: [-0.8, 0.556, 0.05], yaw: 60, dist: 0.14, h: 0.12, dyaw: 10, push: 0.85 },
      { tgt: [-0.8, 0.552, 0.05], yaw: 5, dist: 0.1, h: 0.07, dyaw: -10, push: 0.88 }][r.v || 0]] }),
    rear: () => ({ cent: still(HOME), shots: [{ tgt: 'cent', yaw: 163, dist: 0.1, h: 0.045, dyaw: 25, push: 0.9 }] }),
    spin: () => ({ cent: still(HOME), shots: [{ tgt: 'cent', yaw: -17, dist: 0.13, h: 0.06, dyaw: 200, push: 1 }] }),
    cal150: (i) => ({ mbPose: 'point', calObj: cal150, shots: [{ ...calShot }] }),
    cal3: (i) => ({ mbPose: 'point', mood: 'deadpan', calObj: cal3, shots: [{ ...calShot, dyaw: 5 }] }),
    cal7: (i) => ({ calObj: S.cal, shots: [{ ...calShot }] }),
    baby: (i) => ({ hideCent: 1, shots: [
      { tgt: [BABY[0], 0.003, BABY[1]], yaw: 40, dist: 0.06, h: 0.045, dyaw: 10 },
      { at: W(i, 3) - 0.1, tgt: [BABY[0] + 0.005, 0.003, BABY[1]], yaw: 100, dist: 0.05, h: 0.035, dyaw: 12 }] }),
    spiderDrop: () => {
      const sp = [BABY[0] + 0.015, BABY[1] - 0.004];
      return { hideCent: 1, shots: [{ c0: [sp[0] + 0.03, 0.03, sp[1] + 0.085], l0: [sp[0] - 0.004, 0.05, sp[1]], c1: [sp[0] + 0.035, 0.025, sp[1] + 0.08], l1: [sp[0] - 0.005, 0.008, sp[1]], mv: 0.7 }] };
    },
    whisper: () => ({ mood: 'whisper', shots: [{ tgt: 'mb', yaw: mbYaw, dist: 0.3, h: 0.0, dyaw: 4, push: 0.85 }] }),
    babies: () => ({ hideCent: 1, hideMb: 1, shots: [{ tgt: [0.37, 0.02, 0.3], yaw: 90, dist: 0.36, h: 0.14, dyaw: 0, push: 0.94 }] }),
    map: () => ({ mbPose: 'point', shots: [{ tgt: 'mb', yaw: mbYaw, dist: 0.42, h: 0.05, ly: -0.03, dyaw: 6 }] }),
    centStill: () => ({ cent: still([0.2, 0.62, 1.2]), shots: [{ tgt: [0.2, 0.004, 0.62], yaw: 50, dist: 0.16, h: 0.15, dyaw: 14, push: 0.8 }] }),
    mapArrow: (i) => ({ mbPose: 'hips', mood: 'deadpan', shots: [{ tgt: 'mb', yaw: mbYaw, dist: 0.23, h: 0.0, dyaw: 3 }, { at: L[i].t + 0.35, tgt: 'mb', yaw: mbYaw + 10, dist: 0.45, h: 0.04, dyaw: -4 }] }),
    mapHold: () => ({ mbPose: 'point', shots: [{ tgt: 'mb', yaw: mbYaw + 18, dist: 0.5, h: 0.05, dyaw: -6 }] }),
    fixes: (i) => ({ shots: [
      { tgt: [1.0, 0.2, -0.62], yaw: 157, dist: 0.95, h: 0.12, dyaw: 8 },
      { at: cutw(i, 'fix'), tgt: [0.7, 0.17, -0.85], yaw: 80, dist: 0.6, h: 0.02, dyaw: 8 },
      { at: cutw(i, 'clear'), tgt: [-0.15, 0.2, 1.0], yaw: -60, dist: 0.9, h: 0.15, dyaw: 8 }] }),
    lease: (i) => beat.lease(i),
    rent: (i) => beat.rent(i, L[i].t + 1.6),
    outro: (i) => {
      const o = L[i].t + L[i].dur + 0.25;
      return { mood: 'smug', mbPose: 'hips', shots: [{ tgt: 'mb', yaw: mbYaw, dist: 0.26, h: 0.02, dyaw: 4 },
        { at: o, c0: [MBPOS[0] + 0.25, 0.16, MBPOS[1] + 0.2], l0: [MBPOS[0], 0.11, MBPOS[1]], c1: [1.3, 1.25, 1.25], l1: [0.3, 0.12, -0.15], mv: T_END - o - 0.4 }] };
    },
  };

  rows.forEach((r, i) => {
    const f = BEATS[r.beat]; if (!f) throw new Error(`no beat ${r.beat} (line ${i})`);
    const o = f(i, r);
    if (r.mood && !o.mood) o.mood = r.mood;
    if (r.pose && !o.mbPose && (r.beat === 'mb')) o.mbPose = r.pose;
    set(i, o);
  });
  // night lighting carries the bedbug from the menu to "You're welcome."
  const iMenu = B1('menu'), iNight = B1('night'), iWelcome = B1('welcome'), iLights = B1('lightsOn');
  const iMulti = B1('multi'), iMulti2 = B1('multi2'), iHunt = B1('hunt'), iBee = B1('bee'), iLegClose = B1('legClose');
  const iBaby = B1('baby'), iSpider = B1('spiderDrop'), iBabies = B1('babies'), iFix = B1('fixes'), iRent = B1('rent'), iLunge = B1('lunge');
  const iCent = B('cent'), iMap = B1('map'), iMapA = B1('mapArrow'), iMapH = B1('mapHold'), iLease = B1('lease'), iDrain = B('drain').concat(B('drainClose'));

  // close orbit shots pull back for the 16:9 frame
  cfg.forEach((c) => c.shots.forEach((s) => {
    if (s.dist == null) return;
    if (s.tgt === 'mb') { s.dist *= 1.55; s.ly = (s.ly || 0) + 0.012; }           // keep Meatball's hat in frame
    else if (s.tgt === 'pHead') { s.dist = Math.max(1.2, s.dist * 1.3); s.ly = Math.max(-0.16, Math.min(s.ly || 0, -0.1)); }
    else if (s.dist < 0.7) s.dist *= DK;
  }));

  // chapters (start of the line that opens each one)
  const chapters = []; rows.forEach((r, i) => { if (r.ch) chapters.push({ i, t: i === 0 ? 0 : start(i), name: r.ch }); });

  function props(t, i, S, h) {
    const { place, popS } = h, c = cfg[i], cp = S.cent.userData.pos;
    if (c.cent && c.cent.y) S.cent.position.y = c.cent.y;
    if (tubWater) tubWater.visible = !c.tubDry;   // an empty tub: the centipede is stuck on the dry white floor
    fx.victim(S, t, { a: start(iLunge), b: W(iLunge, wi(iLunge, 'eating')) + 0.55 }, place);
    // roach swarm behind Meatball ("You don't want to know", "a bigger bug problem")
    const sw = c.swarmAt;
    S.swarm.forEach((o, k) => {
      if (!sw || !vis(o.r, sw, end(i), t)) { o.r.visible = false; return; }
      const ph = t * (0.6 + (k % 4) * 0.15) + o.a;
      o.r.position.set(-0.42 + o.d * 0.8 + 0.03 * Math.sin(ph * 2), 0, -0.1 + ((o.z + ph * 0.06) % 0.6));
      o.r.rotation.y = -Math.PI / 2 + 0.3 * Math.sin(ph * 3);
    });
    // the menu: spider, silverfish, ant pop on their words; the bed bug stays until the centipede carries it off
    const prey = [[S.spider, 'spiders', [0.395, -0.175, 2.0], 0.014], [S.silverfish, 'silverfish', [0.45, -0.172, -0.6], 0.016], [S.ant, 'ants', [0.51, -0.172, 2.6], 0.011]];
    for (const [o, w, p, s] of prey) {
      if (i === iMenu && vis(o, Wt(iMenu, w) - 0.05, end(iMenu), t)) { place(o, p); o.scale.setScalar(popS(t, Wt(iMenu, w) - 0.05, s)); o.rotation.y += 0.15 * Math.sin(t * 7); }
      else o.visible = false;
    }
    S.bedbug.visible = false;
    if (i === iMenu && t >= Wt(iMenu, 'bed') - 0.05) { S.bedbug.visible = true; place(S.bedbug, BB); S.bedbug.scale.setScalar(popS(t, Wt(iMenu, 'bed') - 0.05, 0.011)); }
    if (i >= iNight && i <= iWelcome) {
      S.bedbug.visible = true; S.bedbug.scale.setScalar(0.011);
      if (i === iWelcome && t > start(iWelcome) + 0.45) { const f = fwd(cp[2], 0.026); place(S.bedbug, [cp[0] + f[0], cp[1] + f[1], cp[2]], 0.006); }
      else place(S.bedbug, BB);
    }
    // several prey at once: spider, silverfish, ant pop around the centipede's head and quiver while it eats
    const hc = [LUNGE[0], LUNGE[1]], hh = LUNGE[2];
    held.forEach((o, k) => {
      const t0 = Wt(iMulti, 'several') + k * 0.12;
      if (!((i === iMulti || i === iMulti2) && t >= t0)) { o.visible = false; return; }
      o.visible = true;
      const f = fwd(hh, 0.03 + (k === 1 ? 0.008 : 0)), s2 = side(hh, (k - 1) * 0.014);
      place(o, [hc[0] + f[0] + s2[0] + 0.0015 * Math.sin(t * 31 + k), hc[1] + f[1] + s2[1], hh + Math.PI + 0.3 * (k - 1) + 0.15 * Math.sin(t * 17 + k)]);
      const eat = i === iMulti2 && k === 1 ? 1 - ease((t - Wt(iMulti2, 'eats')) / 1.2) : 1;
      o.scale.setScalar(Math.max(0.0001, popS(t, t0, heldS[k]) * eat));
    });
    // the silverfish the centipede pounces on
    if (vis(S.silver2, start(iHunt), end(iHunt), t) && i === iHunt) place(S.silver2, [BB[0] + 0.013, BB[1] - 0.004, 2.4 + (t < Wt(iHunt, 'sting') ? 0.4 * Math.sin(t * 25) : 0)]);
    else S.silver2.visible = false;
    if (i === iBee && vis(S.bee, Wt(iBee, 'bee') - 0.1, end(iBee), t)) {
      const s = side(HOME[2], 0.035); S.bee.position.set(HOME[0] + s[0] + 0.004 * Math.sin(t * 3), 0.016 + 0.003 * Math.sin(t * 5), HOME[1] + s[1]);
      S.bee.rotation.set(0, 2.6, 0); S.bee.scale.setScalar(popS(t, Wt(iBee, 'bee') - 0.1, 0.017));
      for (const w of S.bee.userData.wings) w.w.rotation.x = w.s * (0.3 + 0.6 * Math.abs(Math.sin(t * 47)));
    } else S.bee.visible = false;
    // the dropped leg: twitches after the drop, twitches again in its close-up
    if (vis(S.leg, legDrop, end(iLegClose), t)) {
      const tw = Math.exp(-(t - legDrop) / 0.8) + (i === iLegClose ? 0.7 * Math.exp(-(t - start(iLegClose)) / 1.2) : 0);
      S.leg.position.set(LEG[0], 0.003, LEG[1]); S.leg.rotation.set(-0.05, LEG[2] + 0.4 * tw * Math.sin((t - legDrop) * 30), 0);
      S.leg.userData.knee.rotation.x = 0.5 + 0.5 * tw * Math.sin((t - legDrop) * 23);
    }
    // hatchling + the spider that drops in on it
    if (vis(S.baby, start(iBaby), end(iSpider), t)) {
      const u = clamp01((t - start(iBaby)) / (end(iSpider) - start(iBaby)));
      S.baby.scale.setScalar(0.01); place(S.baby, [BABY[0] + 0.01 * u, BABY[1] - 0.004 * u, BABY[2]], 0.0022);
      h.animate(S.baby, t * 0.3 + u * 12, 1, 1);
    }
    const sp = [BABY[0] + 0.015, BABY[1] - 0.004];
    if (vis(S.spider2, start(iSpider), end(iSpider), t)) {
      const y = 0.003 + 0.09 * (1 - ease((t - start(iSpider)) / 0.55));
      S.spider2.position.set(sp[0], y, sp[1]); S.spider2.rotation.set(0, 2.2 + 0.2 * Math.sin(t * 3), 0);
      S.thread.visible = true; S.thread.position.set(sp[0], y + 0.3, sp[1]); S.thread.scale.y = 0.6;
    } else S.thread.visible = false;
    // growth lineup: 4 -> 15 leg pairs, each pops on its word
    const pops = [start(iBabies) + 0.1, Wt(iBabies, 'ten'), Wt(iBabies, 'fourteen'), Wt(iBabies, 'eighteen'), Wt(iBabies, 'all'), Wt(iBabies, 'way'), Wt(iBabies, 'thirty')];
    lineup.forEach((c2, k) => {
      if (i !== iBabies || t < pops[k] - 0.05) { c2.visible = false; return; }
      c2.visible = true; place(c2, [0.1 + k * 0.068, 0.3, 0], 0.013);   // on the rug, side-on, smallest on the left
      c2.scale.setScalar(Math.max(0.0001, popS(t, pops[k] - 0.05, c2.userData.s0)));
      animateCentipede(c2, t * 0.4 + k, 1, 0.15);
    });
    // a few hatchlings scatter around the "150" calendar
    babies.forEach((b, k) => {
      const ic = B1('cal150'), t0 = Wt(ic, '150') + k * 0.08;
      if (i !== ic || t < t0) { b.visible = false; return; }
      b.visible = true; const a = k * 1.3 + 0.4, r = 0.05 + 0.012 * k, u = t - t0;
      place(b, [calP[0] + Math.cos(a) * r + 0.01 * u * Math.cos(a), calP[1] + Math.sin(a) * r * 0.6 + 0.01 * u * Math.sin(a), -a + Math.PI], 0.0022);
      b.scale.setScalar(popS(t, t0, 0.0085)); animateCentipede(b, t * 0.3 + k, 1, 1);
    });
    // calendars by Meatball (150 / 3 YRS / 7 YEARS)
    for (const o of [cal150, cal3, S.cal]) o.visible = false;
    if (c.calObj && t >= start(i) + 0.05) { const o = c.calObj; o.visible = true; o.position.set(calP[0], 0, calP[1]); o.scale.setScalar(popS(t, start(i) + 0.05, 1)); }
    // fan + leaky pipe + clutter: the fan appears and spins from the fixes line on; the pipe is fixed on "leaks"; boxes go on "clutter"
    if (vis(S.fan, start(iFix), T_END, t)) S.fan.userData.rotor.rotation.x = t * 37;
    fx.pipe(S, t, t >= Wt(iFix, 'leaks'));
    const clear = Wt(iFix, 'cardboard');
    S.boxes.userData.list.forEach((b, k) => { const u = clamp01((t - clear - k * 0.07) / 0.22); b.visible = u < 1; b.scale.setScalar(b.userData.s0 ?? (b.userData.s0 = b.scale.x)); b.scale.multiplyScalar(1 - ease(u)); b.position.x = b.userData.x0 ?? (b.userData.x0 = b.position.x); b.position.x -= 0.25 * ease(u); });
    fx.rentRoach(S, t, start(iRent), cp, place);
    if (t >= end(iRent)) S.pushRoach.visible = false;
  }
  function faceCam(cam) { for (const o of [cal150, cal3]) if (o.visible) o.lookAt(cam.position.x, o.position.y, cam.position.z); }

  const mapAt = (t) => {
    if (t >= start(iMap) + 0.05 && t < end(iMap)) return { age: t - start(iMap) - 0.05, arrow: 0, fade: clamp01((end(iMap) - t) / 0.12) };
    const m = L[iMapA].t + 0.35;
    if (t >= m && t < end(iMapA)) return { age: t - m + 0.3, arrow: (t - m - 0.05) / 0.4, fade: 1 };
    if (t >= end(iMapA) && t < end(iMapH)) return { age: 1, arrow: 1, fade: clamp01((end(iMapH) - t) / 0.12) };
    return null;
  };
  // 2D extras: a white flash when the light comes on; the chapter tag (full-frame coords, top-left)
  function overlay(c, t, full) {
    for (const k in lights) { const d = t - lights[k]; if (d >= 0 && d < 0.25) full((g, w, hh) => { g.fillStyle = `rgba(255,252,235,${0.75 * (1 - d / 0.25)})`; g.fillRect(0, 0, w, hh); }); }
    const ch = chapters.filter((x) => x.i > 0 && t >= x.t && t < x.t + 2.8).pop();
    if (ch) full((g) => {
      const a = clamp01((t - ch.t) / 0.15) * clamp01((ch.t + 2.8 - t) / 0.25), n = chapters.indexOf(ch) + 1;
      g.save(); g.globalAlpha = a; g.translate(-30 * (1 - ease((t - ch.t) / 0.3)), 0);
      g.font = '900 30px Inter'; const label = `CHAPTER ${n}`; g.font = '900 46px Inter'; const name = ch.name.toUpperCase();
      const wN = g.measureText(name).width; const bw = Math.max(260, wN + 64);
      g.fillStyle = 'rgba(15,15,20,0.78)'; g.beginPath(); g.roundRect(48, 44, bw, 124, 18); g.fill();
      g.fillStyle = '#ffd23f'; g.font = '900 28px Inter'; g.letterSpacing = '4px'; g.fillText(label, 80, 88); g.letterSpacing = '0px';
      g.fillStyle = '#fff'; g.font = '900 46px Inter'; g.fillText(name, 80, 144);
      g.restore();
    });
  }
  return K.finish({ props, faceCam, mapAt, overlay, chapters, leaseAt: K.leaseAt(iLease), mbIn: start(iLunge), legDrop: legDrop ?? 1e9, legRegrow, anchor: anchorL });
}

const _v = new THREE.Vector3();
function anchorL(name, S) {
  if (typeof name === 'function') return new THREE.Vector3(...((p) => [p[0], p[1], p[2]])(name(S)));
  if (Array.isArray(name)) return new THREE.Vector3(...name);
  if (name === 'cent') return S.cent.position.clone().add(new THREE.Vector3(0, 0.004, 0));
  if (name === 'mb') return S.mb.position.clone();
  if (name === 'pHead') return S.person.userData.head.getWorldPosition(_v).clone();
  if (name === 'hip') return S.legHip.getWorldPosition(_v).clone();
  return new THREE.Vector3();
}
