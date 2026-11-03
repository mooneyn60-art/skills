// Per-line plans for the house-centipede explainer: shots, cast blocking, prop timing, cards.
// planKit = timing helpers, set positions, shot builders and prop effects shared by both cuts;
// buildPlan = TikTok cut (32 lines); shots_yt.js = YouTube Short cut (7 lines, loops).
// Every value is a pure function of t, so any frame can be rendered alone (chunked + restart-safe renders).
// Shot: {tgt, yaw (deg, camera offset dir in x/z), dist, h, ly, dyaw, push} orbit-push, or {c0, c1, l0, l1, mv} explicit.
import * as THREE from 'three';

export const clamp01 = (x) => Math.max(0, Math.min(1, x));
export const ease = (x) => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
const PRE = 0.12;
// The approved opening: doorway wide, push-in so the centipede fills the frame by ~1 s. The YouTube Short ends on c0/l0.
export const OPEN = { c0: [-0.9, 1.55, 0.95], l0: [0.95, 0.9, -0.35], c1: [0.459, 0.077, -0.028], l1: [0.43, 0.004, -0.123], mv: 1.0 };

export function planKit(L, T_END) {
  const start = (i) => (i === 0 ? 0 : L[i].t - PRE);
  const end = (i) => (i + 1 < L.length ? start(i + 1) : T_END);
  const W = (i, k) => L[i].t + Math.max(0, L[i].words[Math.min(k, L[i].words.length - 1)][0]);
  const cut = (i, k) => W(i, k) - 0.1;
  const HOME = [0.42, -0.12, 0.3], MBPOS = [0.6, 0.1, 0.57], PPOS = [1.45, -0.45, Math.PI + 0.31], PSEAT = [-0.4, 0.32, 0];
  const fwd = (h, d) => [Math.cos(h) * d, -Math.sin(h) * d], side = (h, d) => [Math.sin(h) * d, Math.cos(h) * d];
  const at = (p, f = 0, s = 0, h) => { const a = fwd(p[2], f), b = side(p[2], s); return [p[0] + a[0] + b[0], p[1] + a[1] + b[1], h ?? p[2]]; };
  const CENT0 = [0.44, -0.125, 0.3], LUNGE = [0.485, -0.139, 0.3];   // centipede before / after the roach lunge
  const C2 = at(HOME, 0.045);                 // after the leg-drop escape
  const LEG = at(HOME, 0.002, 0.016, 0.3);    // the dropped leg on the tile
  const P31 = [0.95, -0.4, 0.293], P31e = [1.177, -0.469, 0.293];   // rent: the centipede pushes a roach to the shoe
  const mbYaw = -MBPOS[2] * 180 / Math.PI, pYaw = 162;
  const cfg = L.map(() => ({ shots: [{}] }));
  const set = (i, o) => Object.assign(cfg[i], o);

  // shared beats, as the line config for line i of the cut being built
  const beat = {
    // doorway wide push-in (OPEN), then top-down on the legs at word `top`
    opening: (i, cardWord, top) => ({ cardWord, cent: { p0: HOME, p1: CENT0, t0: 0, t1: end(i), lin: 1 }, hideMb: 1, shots: [
      { ...OPEN }, { at: cut(i, top), tgt: 'cent', yaw: 160, dist: 0.06, h: 0.16, dyaw: 25, push: 0.9 }] }),
    squish: () => ({ hideMb: 1, cent: { p0: CENT0, p1: CENT0, t0: 0, t1: 1 }, person: { pose: 'slipper', from: 'stand' },
      shots: [{ c0: [0.62, 0.04, -0.2], l0: [1.45, 1.25, -0.45], c1: [0.7, 0.05, -0.24], l1: [1.45, 1.45, -0.45] }] }),
    // Meatball stops the slipper, then the centipede lunges at the roach on word k
    lunge: (i, k, cardWord) => ({ cardWord, mbPose: 'stop', mood: 'alarm', person: { pose: 'slipper' },
      cent: { p0: CENT0, p1: LUNGE, t0: W(i, k) + 0.05, t1: W(i, k) + 0.27, lin: 1 }, shots: [
        { tgt: 'mb', yaw: mbYaw, dist: 0.36, h: 0.02, dyaw: -6, push: 0.85 },
        { at: cut(i, k), tgt: [0.5, 0.004, -0.142], yaw: 75, dist: 0.16, h: 0.07, dyaw: 10, push: 0.9 }] }),
    // "Its leg just fell off!": the leg drops on word 1, the centipede scoots forward
    legDrop: (i) => ({ cent: { p0: HOME, p1: C2, t0: W(i, 1) + 0.12, t1: W(i, 1) + 0.8 }, shots: [
      { tgt: [LEG[0] + 0.006, 0.004, LEG[1]], yaw: 60, dist: 0.085, h: 0.07, dyaw: 10, push: 0.85 }] }),
    shrug: (i) => ({ mbPose: 'shrug', cent: { p0: C2, p1: C2, t0: 0, t1: 1 }, shots: [
      { tgt: 'mb', yaw: mbYaw + 13, dist: 0.34, h: 0.03 },
      { at: cut(i, 1), tgt: 'mb', yaw: mbYaw - 17, dist: 0.33, h: 0.05, dyaw: -8 }] }),
    lease: (i) => ({ person: { pose: 'sign', from: 'stand' }, shots: [
      { tgt: 'pHead', yaw: 150, dist: 1.1, h: -0.25, ly: -0.3 },
      { at: cut(i, 3), tgt: 'pHead', yaw: 185, dist: 0.95, h: -0.15, ly: -0.25, dyaw: -8 }] }),
    // "It does. In roaches.": follow the centipede pushing a roach, then the roach at the shoe on word 2
    rent: (i, t1) => ({ cent: { p0: P31, p1: P31e, t0: start(i) + 0.05, t1, lin: 1 }, shots: [
      { tgt: 'cent', yaw: 164.5, dist: 0.12, h: 0.12, dyaw: 0, push: 1 },
      { at: cut(i, 2), c0: [0.88, 0.06, -0.38], l0: [1.25, 0.0, -0.47], c1: [0.93, 0.058, -0.39], l1: [1.25, 0.0, -0.47] }] }),
  };
  // the lease card over line i: signature from word 2 to word 5
  const leaseAt = (i) => (t) => (t >= start(i) + 0.1 && t < end(i) ? { age: t - start(i) - 0.1, sig: (t - W(i, 2)) / (W(i, 5) - W(i, 2)), fade: clamp01((end(i) - t) / 0.12) } : null);

  // prop effects shared by both cuts
  const vis = (o, a, b, t) => { o.visible = t >= a && t < b; return o.visible; };
  const fx = {
    victim: (S, t, t1, place) => { if (vis(S.victim, t1.a, t1.b, t)) place(S.victim, [0.515 + 0.002 * Math.sin(t * 13), -0.148, 2.9]); },
    droppedLeg: (S, t, t0, t1) => {
      if (!vis(S.leg, t0, t1, t)) return;
      const tw = Math.exp(-(t - t0) / 0.8);
      S.leg.position.set(LEG[0], 0.003, LEG[1]); S.leg.rotation.set(-0.05, LEG[2] + 0.4 * tw * Math.sin((t - t0) * 30), 0);
      S.leg.userData.knee.rotation.x = 0.5 + 0.5 * tw * Math.sin((t - t0) * 23);
    },
    pipe: (S, t, fixed) => {
      S.pipe.userData.wrap.visible = fixed;
      S.pipe.userData.drops.forEach((d, k) => { const ph = (t * 1.4 + k / 3) % 1; d.visible = !fixed; d.position.set(-0.05, 0.28 - 0.27 * ph * ph, 0); });
    },
    rentRoach: (S, t, t0, cp, place) => { if (vis(S.pushRoach, t0, T_END, t)) { const f = fwd(cp[2], 0.038); place(S.pushRoach, [cp[0] + f[0], cp[1] + f[1], cp[2] + 0.2 * Math.sin(t * 6)]); } },
  };

  function finish(extra) {
    // flatten shots with absolute [s0, s1)
    const shots = [];
    cfg.forEach((c, i) => c.shots.forEach((s, j) => shots.push({ ...s, s0: j === 0 ? start(i) : s.at, i })));
    shots.forEach((s, k) => { s.s1 = k + 1 < shots.length ? shots[k + 1].s0 : T_END; });
    const shotAt = (t) => { let k = 0; while (k + 1 < shots.length && shots[k + 1].s0 <= t) k++; return shots[k]; };
    // fact cards: from the card word until the next card or >= 2.2 s
    const cards = [];
    L.forEach((l, i) => { if (l.card) cards.push({ card: l.card, src: l.src, s0: W(i, cfg[i].cardWord || 0) - 0.08, min: end(i) + 0.2 }); });
    cards.forEach((c, k) => { c.s1 = Math.min(Math.max(c.min, c.s0 + 2.2), k + 1 < cards.length ? cards[k + 1].s0 : T_END); });
    const cardAt = (t) => { const c = cards.find((c) => t >= c.s0 && t < c.s1); return c && { ...c, age: t - c.s0, fade: clamp01((c.s1 - t) / 0.15) }; };
    return { cfg, start, end, W, shotAt, anchor, cardAt, mapAt: () => null, leaseAt: () => null, HOME, MBPOS, PPOS, shots, ...extra };
  }
  return { start, end, W, cut, HOME, MBPOS, PPOS, PSEAT, fwd, side, at, CENT0, LUNGE, C2, LEG, P31, P31e, mbYaw, pYaw, cfg, set, beat, leaseAt, vis, fx, finish };
}

const _v = new THREE.Vector3();
function anchor(name, S) {
  if (Array.isArray(name)) return new THREE.Vector3(...name);
  if (name === 'cent') return S.cent.position.clone().add(new THREE.Vector3(0, 0.004, 0));
  if (name === 'mb') return S.mb.position.clone();
  if (name === 'pHead') return S.person.userData.head.getWorldPosition(_v).clone();
  if (name === 'drain') return S.drain.position.clone();
  if (name === 'hip') return S.legHip.getWorldPosition(_v).clone();   // hip of the leg that drops off (and grows back)
  return new THREE.Vector3();
}

export function buildPlan(L, T_END) {
  const K = planKit(L, T_END);
  const { start, end, W, cut, HOME, MBPOS, PSEAT, fwd, side, at, C2, LEG, mbYaw, pYaw, set, beat, vis, fx } = K;
  const BABY = [LEG[0] + 0.012, LEG[1] - 0.018, 1.2];
  const BB = at(HOME, 0.067);                 // bed bug (line 8) the centipede creeps to
  const MBC = [MBPOS[0], 0.113, MBPOS[1]];
  const calP = [MBPOS[0] + 0.054 + 0.017, MBPOS[1] + 0.084 - 0.011];

  // 0: doorway wide, push-in so the centipede fills the frame by ~1 s ("30 legs" at 1.2 s), then top-down on the legs
  set(0, beat.opening(0, 5, 7));
  set(1, beat.squish(1));
  set(2, beat.lunge(2, 2, 2));
  set(3, { shots: [{ tgt: 'pHead', yaw: pYaw, dist: 0.8, h: -0.05, ly: -0.1, dyaw: 5, push: 0.85 }] });
  set(4, { mbPose: 'hips', mood: 'deadpan', shots: [
    { tgt: 'mb', yaw: mbYaw, dist: 0.23, h: 0.01, ly: 0.01, dyaw: 3, push: 0.9 },
    { at: cut(4, 5), c0: [0.05, 0.07, 0.15], l0: [-0.4, 0.0, 0.18], c1: [-0.08, 0.05, 0.18], l1: [-0.42, 0, 0.2] }] });
  set(5, { person: { look: (t) => 0.7 * Math.sin((t - start(5)) * 4.5) }, shots: [
    { c0: [0.5, 0.8, -0.1], l0: [1.45, 1.42, -0.45], c1: [0.56, 0.84, -0.14], l1: [1.45, 1.48, -0.45] }] });
  set(6, { cent: { p0: [-0.18, 0.255, -0.2], p1: [-0.1, 0.24, -0.2], t0: start(6) + 0.6, t1: end(6), y: 0.006 }, shots: [
    { c0: [0.35, 0.05, 0.55], l0: [-0.15, 0, 0.25], c1: [0.02, 0.06, 0.34], l1: [-0.15, 0, 0.25] },
    { at: cut(6, 5), tgt: [-0.12, 0.004, 0.245], yaw: 40, dist: 0.12, h: 0.12, dyaw: 15, push: 0.85 }] });
  set(7, { person: { pose: 'crouch', from: 'stand' }, shots: [
    { c0: [-0.12, 0.8, 0.42], l0: [1.3, 0.62, -0.42], c1: [-0.04, 0.8, 0.37], l1: [1.3, 0.66, -0.42] }] });
  set(8, { shots: [
    { tgt: [0.425, 0.004, -0.155], yaw: 90, dist: 0.17, h: 0.12, dyaw: 8, push: 0.9 },
    { at: cut(8, 2), tgt: [0.49, 0.004, -0.16], yaw: 70, dist: 0.17, h: 0.1, dyaw: -10, push: 0.9 },
    { at: cut(8, 4), tgt: [0.47, 0.004, -0.135], yaw: 20, dist: 0.11, h: 0.06, dyaw: 10, push: 0.85 }] });
  const creep = { p0: HOME, p1: at(HOME, 0.035), t0: start(9), t1: end(10), lin: 1 };
  set(9, { night: 1, cent: creep, shots: [{ c0: [0.25, 0.55, 0.45], l0: [-0.4, 1.4, -0.88], c1: [0.58, 0.1, 0.0], l1: [0.46, 0.0, -0.13], mv: 1.0 }] });
  set(10, { night: 1, cent: creep, person: { pose: 'crouch' }, shots: [
    { c0: [-0.05, 0.78, 0.5], l0: [1.3, 0.64, -0.42], c1: [0.02, 0.78, 0.45], l1: [1.3, 0.66, -0.42] }] });
  set(11, { night: 1, mood: 'smug', person: { pose: 'crouch' }, cent: { p0: at(HOME, 0.035), p1: [0.43, -0.2, 1.9], t0: start(11) + 0.45, t1: end(11) },
    shots: [{ tgt: 'mb', yaw: mbYaw, dist: 0.28, h: 0.02, dyaw: -5 }, { at: start(11) + 0.5, tgt: 'cent', yaw: 40, dist: 0.13, h: 0.09, dyaw: 10 }] });
  set(12, { person: { p0: PSEAT, pose: 'seated' }, shots: [{ c0: [0.9, 0.85, 0.6], l0: [-0.35, 1.0, 0.32], c1: [0.84, 0.87, 0.57], l1: [-0.35, 1.04, 0.32] }] });
  set(13, { cent: { p0: HOME, p1: at(HOME, 0.06), t0: W(13, 0) - 0.02, t1: W(13, 0) + 0.18, lin: 1 }, shots: [
    { tgt: [0.47, 0.004, -0.137], yaw: 72, dist: 0.16, h: 0.07, dyaw: 8 },
    { at: cut(13, 2), tgt: [0.475, 0.004, -0.137], yaw: 200, dist: 0.07, h: 0.12, dyaw: 20, push: 0.85 }] });
  set(14, { person: { p0: K.PPOS, p1: [1.85, -0.5, K.PPOS[2]], t0: L[14].t, t1: end(14) - 0.2, pose: 'back', from: 'stand' }, shots: [
    { c0: [0.65, 0.05, -0.2], l0: [1.45, 1.25, -0.45], c1: [0.6, 0.05, -0.18], l1: [1.55, 1.2, -0.46] },
    { at: cut(14, 1), c0: [0.1, 1.0, 0.35], l0: [1.5, 1.2, -0.45], c1: [0.2, 1.0, 0.3], l1: [1.75, 1.25, -0.48] }] });
  set(15, { mbPose: 'point', shots: [
    { tgt: 'mb', yaw: mbYaw, dist: 0.26, h: 0.02, dyaw: 6 },
    { at: cut(15, 2), tgt: 'mb', yaw: mbYaw - 22, dist: 0.27, h: 0.0, dyaw: -6 }] });
  set(16, { shots: [
    { tgt: [0.43, 0.008, -0.105], yaw: 30, dist: 0.17, h: 0.06, dyaw: 8 },
    { at: cut(16, 3), tgt: [0.43, 0.012, -0.095], yaw: 95, dist: 0.12, h: 0.04, dyaw: 10 }] });
  set(17, beat.legDrop(17));
  set(18, beat.shrug(18));
  set(19, { hideCent: 1, shots: [
    { tgt: [(LEG[0] + BABY[0]) / 2, 0.003, (LEG[1] + BABY[1]) / 2], yaw: 40, dist: 0.06, h: 0.045, dyaw: 10 },
    { at: cut(19, 3), tgt: [BABY[0] + 0.005, 0.003, BABY[1]], yaw: 100, dist: 0.05, h: 0.035, dyaw: 12 }] });
  const sp = [BABY[0] + 0.015, BABY[1] - 0.004];
  set(20, { hideCent: 1, shots: [{ c0: [sp[0] + 0.03, 0.03, sp[1] + 0.085], l0: [sp[0] - 0.004, 0.05, sp[1]], c1: [sp[0] + 0.035, 0.025, sp[1] + 0.08], l1: [sp[0] - 0.005, 0.008, sp[1]], mv: 0.7 }] });
  set(21, { mood: 'whisper', shots: [{ tgt: 'mb', yaw: mbYaw, dist: 0.3, h: 0.0, dyaw: 4, push: 0.85 }] });
  set(22, { person: { p0: PSEAT, pose: 'seated' }, shots: [{ c0: [0.75, 0.95, 0.0], l0: [-0.35, 1.03, 0.32], c1: [0.7, 0.97, 0.04], l1: [-0.35, 1.07, 0.32] }] });
  set(23, { mbPose: 'point', shots: [{ tgt: 'mb', yaw: mbYaw, dist: 0.42, h: 0.05, ly: -0.03, dyaw: 6 }] });
  set(24, { cent: { p0: [0.2, 0.62, 1.2], p1: [0.2, 0.62, 1.2], t0: 0, t1: 1, still: 1 }, shots: [{ tgt: [0.2, 0.004, 0.62], yaw: 50, dist: 0.16, h: 0.15, dyaw: 14, push: 0.8 }] });
  const map25 = L[25].t + 0.35;
  set(25, { mbPose: 'hips', mood: 'deadpan', shots: [{ tgt: 'mb', yaw: mbYaw, dist: 0.23, h: 0.0, dyaw: 3 }, { at: map25, tgt: 'mb', yaw: mbYaw + 10, dist: 0.45, h: 0.04, dyaw: -4 }] });
  set(26, { shots: [{ tgt: 'pHead', yaw: 140, dist: 1.0, h: -0.1, ly: -0.15 }] });
  set(27, { cal: 1, shots: [{ tgt: [(MBC[0] + calP[0]) / 2, 0.1, (MBC[2] + calP[1]) / 2], yaw: mbYaw, dist: 0.46, h: 0.03, dyaw: -5 }] });
  set(28, { person: { pose: 'head', from: 'stand' }, shots: [
    { tgt: 'pHead', yaw: pYaw, dist: 1.2, h: 0.0, ly: -0.05 },
    { at: cut(28, 1), c0: [0.6, 0.08, -0.15], l0: [1.45, 1.3, -0.45], c1: [0.66, 0.1, -0.2], l1: [1.45, 1.4, -0.45] }] });
  set(29, { shots: [
    { tgt: [1.0, 0.2, -0.62], yaw: 157, dist: 0.95, h: 0.12, dyaw: 8 },
    { at: cut(29, 3), tgt: [0.7, 0.17, -0.85], yaw: 80, dist: 0.6, h: 0.02, dyaw: 8 },
    { at: cut(29, 5), tgt: [-0.15, 0.2, 1.0], yaw: -60, dist: 0.9, h: 0.15, dyaw: 8 }] });
  set(30, beat.lease(30));
  set(31, beat.rent(31, L[31].t + 1.6));

  const mapAt = (t) => {
    if (t >= start(23) + 0.05 && t < end(23)) return { age: t - start(23) - 0.05, arrow: 0, fade: clamp01((end(23) - t) / 0.12) };
    if (t >= map25 && t < end(25)) return { age: t - map25 + 0.3, arrow: (t - map25 - 0.05) / 0.4, fade: clamp01((end(25) - t) / 0.12) };
    return null;
  };
  const legDrop = W(17, 1);
  function props(t, i, S, h) {
    const { place, popS } = h, cp = S.cent.userData.pos;
    if (K.cfg[i].cent && K.cfg[i].cent.y) S.cent.position.y = K.cfg[i].cent.y;
    fx.victim(S, t, { a: start(2), b: W(2, 2) + 0.55 }, place);
    const sw = cut(4, 5);
    S.swarm.forEach((o, k) => {
      if (!vis(o.r, sw, end(4), t)) return;
      const ph = t * (0.6 + (k % 4) * 0.15) + o.a;
      o.r.position.set(-0.42 + o.d * 0.8 + 0.03 * Math.sin(ph * 2), 0, -0.1 + ((o.z + ph * 0.06) % 0.6));
      o.r.rotation.y = -Math.PI / 2 + 0.3 * Math.sin(ph * 3);
    });
    const prey = [[S.spider, 0, [0.395, -0.175, 2.0], 0.014], [S.silverfish, 1, [0.45, -0.172, -0.6], 0.016], [S.ant, 2, [0.51, -0.172, 2.6], 0.011]];
    for (const [o, k, p, s] of prey) if (vis(o, W(8, k) - 0.05, end(8), t)) { place(o, p); o.scale.setScalar(popS(t, W(8, k) - 0.05, s)); o.rotation.y += 0.15 * Math.sin(t * 7 + k); }
    if (vis(S.bedbug, W(8, 4) - 0.05, end(11), t)) {
      if (i === 11 && t > start(11) + 0.45) { const f = fwd(cp[2], 0.026); place(S.bedbug, [cp[0] + f[0], cp[1] + f[1], cp[2]], 0.006); }
      else place(S.bedbug, BB);
      S.bedbug.scale.setScalar(popS(t, W(8, 4) - 0.05, 0.011));
    }
    if (vis(S.silver2, start(13), end(13), t)) { place(S.silver2, [BB[0] + 0.013, BB[1] - 0.004, 2.4 + (t < W(13, 5) ? 0.4 * Math.sin(t * 25) : 0)]); }
    if (vis(S.bee, W(16, 1) - 0.1, end(16), t)) {
      const s = side(HOME[2], 0.035); S.bee.position.set(HOME[0] + s[0] + 0.004 * Math.sin(t * 3), 0.016 + 0.003 * Math.sin(t * 5), HOME[1] + s[1]);
      S.bee.rotation.set(0, 2.6, 0); S.bee.scale.setScalar(popS(t, W(16, 1) - 0.1, 0.017));
      for (const w of S.bee.userData.wings) w.w.rotation.x = w.s * (0.3 + 0.6 * Math.abs(Math.sin(t * 47)));
    }
    fx.droppedLeg(S, t, legDrop, end(20));
    if (vis(S.baby, start(19), end(20), t)) {
      const u = clamp01((t - start(19)) / (end(20) - start(19)));
      place(S.baby, [BABY[0] + 0.01 * u, BABY[1] - 0.004 * u, BABY[2]], 0.0022);
      h.animate(S.baby, t * 0.3 + u * 0.4 * 30, 1, 1);
    }
    if (vis(S.spider2, start(20), end(20), t)) {
      const y = 0.003 + 0.09 * (1 - ease((t - start(20)) / 0.55));
      S.spider2.position.set(sp[0], y, sp[1]); S.spider2.rotation.set(0, 2.2 + 0.2 * Math.sin(t * 3), 0);
      S.thread.visible = true; S.thread.position.set(sp[0], y + 0.3, sp[1]); S.thread.scale.y = 0.6;
    } else S.thread.visible = false;
    if (vis(S.cal, start(27), end(27), t)) { S.cal.position.set(calP[0], 0, calP[1]); S.cal.scale.setScalar(popS(t, start(27) + 0.05, 1)); }
    if (vis(S.fan, start(29), end(29), t)) S.fan.userData.rotor.rotation.x = t * 37;
    fx.pipe(S, t, t >= W(29, 4));
    const clear = W(29, 6);
    S.boxes.userData.list.forEach((b, k) => { const u = clamp01((t - clear - k * 0.07) / 0.22); b.visible = u < 1; b.scale.setScalar(b.userData.s0 ?? (b.userData.s0 = b.scale.x)); b.scale.multiplyScalar(1 - ease(u)); b.position.x = b.userData.x0 ?? (b.userData.x0 = b.position.x); b.position.x -= 0.25 * ease(u); });
    fx.rentRoach(S, t, start(31), cp, place);
  }
  return K.finish({ mapAt, leaseAt: K.leaseAt(30), props, mbIn: start(2), legDrop });
}
