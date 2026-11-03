// YouTube Short cut of the house-centipede explainer (7 lines, ~18 s). Reuses the TikTok beats from planKit;
// adds the bed bug pop on "Even bed bugs.", the leg growing back on "Then grows them back.", and a loop ending:
// the last shot cranes back out to the opening framing (OPEN.c0/l0), so "In roaches." cuts straight into line 0.
import { planKit, OPEN } from './shots.js';

export function buildPlanYT(L, T_END) {
  const K = planKit(L, T_END);
  const { start, end, W, cut, at, LUNGE, set, beat, vis, fx } = K;
  const BUG = at(LUNGE, 0.05, 0.012, 3.6);    // the bed bug pops in just ahead of the centipede after the lunge

  set(0, beat.opening(0, 3, 5));               // card on "30-legged", top-down on "in"
  set(1, beat.squish(1));
  const l2 = beat.lunge(2, 2, 5);              // lunge on "eats"; card "EATS BED BUGS TOO" on "Even"
  l2.shots.push({ at: cut(2, 5), tgt: [(LUNGE[0] + BUG[0]) / 2 + 0.008, 0.004, (LUNGE[1] + BUG[1]) / 2], yaw: 50, dist: 0.1, h: 0.07, dyaw: 10, push: 0.88 });
  set(2, l2);
  set(3, beat.legDrop(3));
  const l4 = beat.shrug(4);                    // shrug, then a new leg scales back in at the hip on "grows"
  const sd = K.side(K.C2[2], 0.0045);          // top-down from behind, hip left of centre: the new leg grows out across the frame
  l4.shots.push({ at: cut(4, 6), tgt: 'hip', off: [sd[0], 0, sd[1]], yaw: 163, dist: 0.014, h: 0.034, dyaw: 8, push: 0.92 });
  set(4, l4);
  set(5, beat.lease(5));
  // rent: the roach lands at the shoe on "In roaches.", then the camera cranes out to the opening framing
  const land = W(6, 3), out = land + 0.05, home = T_END - 0.1;
  const l6 = beat.rent(6, land);
  const shoe = l6.shots[1];
  l6.shots.push({ at: out, c0: shoe.c1, l0: shoe.l1, c1: OPEN.c0, l1: OPEN.l0, mv: home - out });
  set(6, l6);

  const legDrop = W(3, 1);
  function props(t, i, S, h) {
    const { place, popS } = h, cp = S.cent.userData.pos;
    fx.victim(S, t, { a: start(2), b: W(2, 2) + 0.55 }, place);
    if (vis(S.bedbug, W(2, 5) - 0.05, end(2), t)) { place(S.bedbug, BUG); S.bedbug.scale.setScalar(popS(t, W(2, 5) - 0.05, 0.011)); }
    fx.droppedLeg(S, t, legDrop, end(4));
    fx.pipe(S, t, false);
    fx.rentRoach(S, t, start(6), cp, place);
    for (const o of [S.spider, S.spider2, S.thread, S.silverfish, S.silver2, S.ant, S.bee, S.baby, S.cal, S.fan]) o.visible = false;
    for (const o of S.swarm) o.r.visible = false;
  }
  return K.finish({ leaseAt: K.leaseAt(5), props, mbIn: start(2), legDrop, legRegrow: W(4, 7) - 0.05, mbOut: home - 0.45 });
}
