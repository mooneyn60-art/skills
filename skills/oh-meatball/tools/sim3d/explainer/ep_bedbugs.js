// Episode: bed bugs (YouTube Short, 8 lines, ~19 s, loops). Low-poly bedroom at night; the person sits up in Meatball's
// guest bed with 3 bites on the forearm. Real-size bugs (adult ~6 mm, eggs ~1 mm).
// Beats: 3 bites (hook) -> a bug on the sheet + apple seed -> bugs + eggs in the mattress seam -> a bug feeds on the
// forearm and balloons up red -> Meatball on the nightstand -> "MONTHS" calendar -> "Sweet dreams." cranes back to the opening.
import * as THREE from 'three';
import { mat, mesh, box, cyl, texMat, canvasTex, wallPlane, shade, ICO1 } from './lib.js';
import * as P from './props.js';
import * as Q from './props2.js';

export const SHIRT = 0x4f7fb0;
export const LIGHT = { bg: 0x0e1426, hemi: [0xc2d0ff, 0x5a4a40, 1.0], sun: [0xc8d6ff, 1.3], sunPos: [1.6, 3.0, 1.8], sunTgt: [0, 0.5, 0],
  lamps: [[0xffcf8a, 2.0, [-0.85, 1.0, 1.05]], [0xffe6c4, 0.6, [0.6, 2.3, 0.6]]] };

const MT = 0.55;            // mattress top
const BS = 0.006;           // adult bed bug ~6 mm (EPA: 5-7 mm)
const SEAM_Z = 0.752, SEAM_X = 0.35;
const BUGP = [0.12, 0.3, 2.4];   // the bug on the sheet (line 1)

function makeBedroom() {
  const g = new THREE.Group();
  const wood = texMat(canvasTex(256, 256, (c, w) => { for (let i = 0; i < 8; i++) { c.fillStyle = shade('#8a6040', ((i * 37) % 9) - 4); c.fillRect(0, i * 32, w, 31); c.fillStyle = '#5a3d26'; c.fillRect(0, i * 32 + 31, w, 1); } }, [5, 5]));
  const fl = new THREE.Mesh(new THREE.PlaneGeometry(3.8, 3.6), wood); fl.rotation.x = -Math.PI / 2; fl.position.set(0.8, 0, 0.8); fl.receiveShadow = true; g.add(fl);
  const paint = mat(0x8796b5, { flatShading: false });
  g.add(wallPlane(3.8, 2.5, paint, 0.8, -1.0, 0), wallPlane(3.6, 2.5, paint, -1.1, 0.8, Math.PI / 2), wallPlane(3.6, 2.5, paint, 2.7, 0.8, -Math.PI / 2), wallPlane(3.8, 2.5, paint, 0.8, 2.6, Math.PI));
  const ceil = new THREE.Mesh(new THREE.PlaneGeometry(3.8, 3.6), paint); ceil.rotation.x = Math.PI / 2; ceil.position.set(0.8, 2.5, 0.8); g.add(ceil);
  // bed: frame, headboard, mattress with piping seams, fitted sheet, pillow, blanket over the legs
  g.add(box(2.1, 0.3, 1.6, 0x6b4a32, 0, 0, 0), box(0.08, 1.05, 1.6, 0x5a3c28, -1.04, 0, 0));
  g.add(box(2.0, 0.25, 1.5, mat(0xe9e2d2), 0, 0.3, 0));
  const pipe = mat(0xb9ad94);
  for (const y of [0.3, MT]) for (const z of [-0.752, SEAM_Z]) { const p = cyl(0.007, 0.007, 2.0, pipe, 6); p.rotation.z = Math.PI / 2; p.position.set(0, y, z); g.add(p); }
  const sheet = texMat(canvasTex(128, 128, (c, w) => { c.fillStyle = '#eef3f8'; c.fillRect(0, 0, w, w); c.fillStyle = '#dbe6f0'; for (let i = 0; i < 8; i++) c.fillRect(0, i * 16, w, 3); }, [6, 4]));
  const sh = new THREE.Mesh(new THREE.PlaneGeometry(1.98, 1.4), sheet); sh.rotation.x = -Math.PI / 2; sh.position.set(0, MT + 0.002, 0); sh.receiveShadow = true; g.add(sh);
  const pil = mesh(ICO1, mat(0xf6f6f2)); pil.name = 'bedPillow'; pil.scale.set(0.22, 0.08, 0.38); pil.position.set(-0.82, MT + 0.07, 0.1); g.add(pil);
  g.add(box(1.15, 0.2, 1.42, mat(0xc0484a), 0.42, MT, 0.0));
  g.add(box(0.06, 0.004, 1.42, mat(0xe8d0a0), -0.12, MT + 0.2, 0.0, false));
  // nightstand (Meatball's spot) + lamp, rug, window with moon
  g.add(box(0.42, 0.55, 0.4, 0x7a5636, -0.82, 0, 1.05));
  const lamp = Q.makeLamp(); lamp.position.set(-0.92, 0.55, 1.15); g.add(lamp);
  g.add(box(1.2, 0.01, 0.8, 0x6a7f5a, 1.5, 0, 0.6, false));
  const win = P.makeWindow(); win.position.set(0.5, 1.0, -0.98); g.add(win);
  win.userData.glassM.color.setHex(0x14234a); win.userData.moon.visible = true; win.userData.stars.forEach((s) => (s.visible = true));
  return g;
}

export function build(scene, S, K) {
  const { L, T_END, start, end, W, cut, popS, vis, place, ease, clamp01 } = K;
  scene.add(makeBedroom());
  const pd = S.person.userData, arm = pd.el[1];
  // 3 bites on the right forearm (its geometry runs down -y from the elbow)
  S.bites = [0.1, 0.15, 0.21].map((y, k) => { const b = mesh(ICO1, mat(0xd2484a), false); b.scale.set(0.0045, 0.008, 0.007); b.position.set(0.045, -y, (k - 1) * 0.01); arm.add(b); return b; });
  S.armBug = Q.makeBedBug2(); S.armBug.scale.setScalar(BS); S.armBug.position.set(0.051, -0.125, 0.0); S.armBug.rotation.set(0, 0, -Math.PI / 2); arm.add(S.armBug);
  S.bug = Q.makeBedBug2(); S.bug.scale.setScalar(BS); scene.add(S.bug);
  S.seed = mesh(ICO1, mat(0x5a3218)); S.seed.scale.set(0.0035, 0.0018, 0.0022); scene.add(S.seed);
  S.seam = [];   // bugs + eggs + dark spots tucked along the front piping
  for (let k = 0; k < 7; k++) { const b = Q.makeBedBug2(); b.scale.setScalar(BS * (k % 3 ? 1 : 0.6)); b.position.set(SEAM_X - 0.05 + k * 0.016, MT - 0.012 + (k % 2) * 0.004, SEAM_Z + 0.004); b.rotation.set(Math.PI / 2 - 0.2, 0.3 * k, Math.PI / 2); scene.add(b); S.seam.push(b); }
  for (let k = 0; k < 12; k++) { const e = Q.makeBugEgg(); e.scale.setScalar(0.0012); e.position.set(SEAM_X - 0.06 + k * 0.009, MT - 0.008, SEAM_Z + 0.0065); e.rotation.set(Math.PI / 2, 0, 0.4 * k); scene.add(e); S.seam.push(e); }
  for (let k = 0; k < 14; k++) { const d = mesh(ICO1, mat(0x1a0d08), false); d.scale.setScalar(0.0008 + (k % 3) * 0.0004); d.position.set(SEAM_X - 0.07 + k * 0.011, MT - 0.004 - (k % 4) * 0.004, SEAM_Z + 0.006); scene.add(d); }
  S.cal = Q.makeCal('NO MEAL FOR', 'MONTHS'); scene.add(S.cal);
  S.napkin = box(0.36, 0.02, 0.62, 0xffffff, 0, 0, 0, false); S.napkin.position.set(0, 0, 0); const nk = new THREE.Group(); nk.add(S.napkin); S.armBug.userData.body.add(nk); S.napkin = nk; nk.position.set(0.5, 0.18, 0);
  S.hugPillow = mesh(ICO1, mat(0xf6f6f2)); S.hugPillow.scale.set(0.09, 0.2, 0.3); S.hugPillow.position.set(0.17, 0.32, 0); pd.chest.add(S.hugPillow);
  S.bedPillow = scene.getObjectByName('bedPillow');

  const POSES = { ...P.PERSON_POSES,
    bed: { py: 0.1, lean: 0.22, hip: [1.5, 1.5], knee: [0, 0], shz: [0.25, 0.55], elz: [0.3, 1.05], shx: [0, 0.15], elx: [0, 0] },
    shrug: { py: 0.1, lean: 0.05, hip: [1.5, 1.5], knee: [0, 0], shz: [0.6, 0.55], elz: [1.4, 1.05], shx: [0.5, 0.15], elx: [0, 0] },
    hug: { py: 0.1, lean: -0.12, hip: [1.5, 1.5], knee: [0, 0], shz: [1.15, 1.15], elz: [1.1, 1.1], shx: [-0.55, -0.55], elx: [0, 0] },
    fist: { py: 0.1, lean: 0.0, hip: [1.5, 1.5], knee: [0, 0], shz: [0.25, 2.6], elz: [0.3, 0.9], shx: [0, 0], elx: [0, 0] },
  };
  const PPOS = [-0.55, 0.12, 0], MBPOS = [-0.8, 1.02, -0.6];
  const armAt = (S) => S.bites[1].getWorldPosition(new THREE.Vector3()).toArray();
  const armBugAt = (S) => S.armBug.getWorldPosition(new THREE.Vector3()).toArray();
  const pHead = (S) => S.person.userData.head.getWorldPosition(new THREE.Vector3()).toArray();
  const mbAt = (S) => [S.mb.position.x, S.mb.position.y, S.mb.position.z];
  const OPEN = { c0: [0.75, 1.3, 1.35], l0: [-0.45, 1.0, 0.25], c1: [-0.17, 1.13, 0.53], l1: [-0.31, 1.01, 0.4], mv: 1.0 };
  const SEAMT = [SEAM_X, MT - 0.006, SEAM_Z];
  const cfg = L.map(() => ({ shots: [{}] }));
  const set = (i, o) => Object.assign(cfg[i], o);

  set(0, { shots: [{ ...OPEN }, { at: cut(0, 5), tgt: armAt, yaw: 50, dist: 0.1, h: 0.07, dyaw: 12, push: 0.85 }] });
  set(1, { cardWord: 2, shots: [{ tgt: [BUGP[0], MT, BUGP[1]], yaw: 60, dist: 0.05, h: 0.022, dyaw: 12, push: 0.85 },
    { at: cut(1, 4), tgt: SEAMT, yaw: 82, dist: 0.075, h: 0.012, dyaw: -14, push: 0.85 }] });
  set(2, { person: { pose: 'shrug', from: 'bed' }, shots: [{ tgt: pHead, yaw: 8, dist: 1.9, h: -0.15, ly: -0.3, dyaw: 6, push: 0.92 }] });
  set(3, { cardWord: 1, shots: [{ tgt: armBugAt, yaw: 90, dist: 0.07, h: 0.035, dyaw: -12, push: 0.85 }, { at: cut(3, 8), tgt: armBugAt, yaw: 70, dist: 0.04, h: 0.022, dyaw: 8, push: 0.88 }] });
  set(4, { person: { pose: 'hug', from: 'bed', look: (t) => 0.35 * Math.sin((t - start(4)) * 6) }, shots: [{ tgt: pHead, yaw: 14, dist: 1.6, h: -0.1, ly: -0.25, dyaw: -6, push: 0.9 }] });
  set(5, { cardWord: 2, mbPose: 'hips', mood: 'smug', shots: [{ tgt: mbAt, yaw: -20, dist: 0.5, h: 0.05, dyaw: 8, push: 0.9 }] });
  set(6, { person: { pose: 'fist', from: 'bed' }, shots: [{ tgt: pHead, yaw: 4, dist: 2.1, h: -0.1, ly: -0.12, dyaw: 6, push: 0.92 }] });
  const sweet = W(7, 7) - 0.1, home = T_END - 0.08, out = W(7, 8) + 0.15;
  set(7, { cardWord: 3, mood: 'deadpan', shots: [{ tgt: [SEAM_X - 0.02, MT + 0.215, SEAM_Z - 0.1], yaw: 70, dist: 0.3, h: 0.09, dyaw: -8, push: 0.85 },
    { at: sweet, tgt: mbAt, yaw: -15, dist: 0.4, h: 0.04, dyaw: 4, push: 0.95 },
    { at: out, c0: [MBPOS[0] + 0.35, 0.95, MBPOS[1] - 0.05], l0: [MBPOS[0], 0.75, MBPOS[1]], c1: OPEN.c0, l1: OPEN.l0, mv: home - out }] });
  cfg[0].hideMb = 1;

  function props(t, i) {
    // the bug on the sheet walks toward the person's hip; the apple seed pops on "Apple-seed"
    if (vis(S.bug, start(1), cut(1, 4) + 0.05, t)) { const u = (t - start(1)) / 1.6; place(S.bug, [BUGP[0] - 0.012 * u, BUGP[1] - 0.006 * u, BUGP[2]], MT + 0.003); Q.animateLegs(S.bug, t * 4, 1); }
    if (vis(S.seed, W(1, 2) - 0.06, cut(1, 4) + 0.05, t)) { S.seed.position.set(BUGP[0] - 0.004, MT + 0.0035, BUGP[1] - 0.012); S.seed.rotation.y = 0.5; S.seed.scale.set(0.0035, 0.0018, 0.0022).multiplyScalar(popS(t, W(1, 2) - 0.06, 1) || 0.001); }
    for (const [k, b] of S.seam.entries()) if (b.userData.legs) Q.animateLegs(b, t * 0.8 + k, 0.2);
    // the bug on the forearm drinks: belly balloons up red from "Then" to the end of the line
    const feed = i === 3, f = feed ? ease(clamp01((t - W(3, 3) + 0.05) / 0.9)) : 0;
    S.armBug.visible = feed; Q.feedBedBug(S.armBug, f); if (feed) Q.animateLegs(S.armBug, t < W(3, 3) ? t * 3 : 0, t < W(3, 3) ? 0.6 : 0);
    // ...with manners: a tiny napkin bib pops on "with" and dabs
    if (vis(S.napkin, W(3, 9) - 0.08, end(3), t)) { S.napkin.scale.setScalar(popS(t, W(3, 9) - 0.08, 1)); S.napkin.rotation.z = -0.5 + 0.12 * Math.sin(t * 14); }
    // dramatic pillow hug on "Will I get sick?!"
    S.hugPillow.visible = i === 4; S.bedPillow.visible = i !== 4;
    if (vis(S.cal, W(7, 3) - 0.06, sweet, t)) { S.cal.position.set(SEAM_X - 0.02, MT + 0.2, SEAM_Z - 0.1); S.cal.scale.setScalar(popS(t, W(7, 3) - 0.06, 0.6)); }
  }
  function faceCam(cam) { if (S.cal.visible) S.cal.lookAt(cam.position.x, S.cal.position.y, cam.position.z); }
  return { cfg, props, faceCam, POSES, pose0: 'bed', personY: MT - 0.02, MB: 0.07, MBPOS, mbY: 0.55, PPOS, mbIn: start(1), mbOut: home - 0.5 };
}
