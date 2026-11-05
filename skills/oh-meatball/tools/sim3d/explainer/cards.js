// 2D layer for the explainer: word-by-word captions, white fact cards, the map card and the lease card.
// Coordinates are 1080x1920. Captions stay inside x 160-920 with the last line's baseline at ~1400.
export const SOURCES = { psu: 'Penn State Extension', caes: 'Conn. Ag. Exp. Station', wisc: 'Univ. of Wisconsin', uark: 'Univ. of Arkansas', ucipm: 'UC IPM', frontiers: 'Frontiers in Zoology 2024', wsu: 'Washington State Univ.',
  uky: 'Univ. of Kentucky', sciam: 'Scientific American', epa: 'U.S. EPA', cdc: 'CDC',
  mdc: 'Missouri Dept. of Conservation', usu: 'Utah State Univ.', ala: 'American Lung Association', aafa: 'AAFA', niehs: 'NIEHS' };
const YEL = '#ffd23f';
const clamp01 = (x) => Math.max(0, Math.min(1, x));
const back = (x) => { const c = 1.7; x = clamp01(x); return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };

function rrect(c, x, y, w, h, r) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
function wrap(c, text, maxW) {
  const out = []; let cur = '';
  for (const w of text.split(/\s+/)) { const tryL = cur ? cur + ' ' + w : w; if (c.measureText(tryL).width > maxW && cur) { out.push(cur); cur = w; } else cur = tryL; }
  if (cur) out.push(cur);
  return out;
}

// line = timeline line; rel = seconds since the line started. Chunks of up to 3 words; each word appears when spoken,
// the word being spoken is yellow.
export function drawCaption(c, line, rel) {
  const words = line.words; if (!words.length) return;
  let k = -1; for (let i = 0; i < words.length; i++) if (rel >= words[i][0] - 0.03) k = i;
  if (k < 0) return;
  const c0 = Math.floor(k / 3) * 3, shown = words.slice(c0, k + 1).map((w) => w[2].toUpperCase());
  const full = words.slice(c0, c0 + 3).map((w) => w[2].toUpperCase());
  const pop = 1 + 0.1 * Math.exp(-Math.max(0, rel - words[k][0]) / 0.07);
  let size = 92; const maxW = 740;
  c.font = `900 ${size}px Inter`;
  const longest = Math.max(...full.map((w) => c.measureText(w).width));
  if (longest > maxW) size = Math.floor(size * maxW / longest);
  c.font = `900 ${size}px Inter`;
  // lay out the full chunk (stable positions), draw only the words spoken so far
  const space = c.measureText(' ').width + 24, lines = [[]]; let lw = 0;
  full.forEach((w, j) => { const ww = c.measureText(w).width; if (lines[lines.length - 1].length && lw + space + ww > maxW) { lines.push([]); lw = 0; } lines[lines.length - 1].push([w, ww, c0 + j]); lw += (lw ? space : 0) + ww; });
  const lh = size * 1.08, base = 1400 - (lines.length - 1) * lh;
  c.textBaseline = 'alphabetic'; c.lineJoin = 'round'; c.textAlign = 'left';
  lines.forEach((ln, r) => {
    const tw = ln.reduce((a, [, ww]) => a + ww, 0) + space * (ln.length - 1);
    let x = 540 - tw / 2; const y = base + r * lh;
    for (const [w, ww, gi] of ln) {
      if (gi <= k) {
        const sc = gi === k ? pop : 1;
        c.save(); c.translate(x + ww / 2, y - size * 0.35); c.scale(sc, sc); c.translate(-(x + ww / 2), -(y - size * 0.35));
        c.shadowColor = 'rgba(0,0,0,0.8)'; c.shadowBlur = 0; c.shadowOffsetY = 7;
        c.lineWidth = 14; c.strokeStyle = '#000'; c.strokeText(w, x, y);
        c.shadowColor = 'transparent'; c.fillStyle = gi === k ? YEL : '#fff'; c.fillText(w, x, y);
        c.restore();
      }
      x += ww + space;
    }
  });
}

// White fact card at the top: red FACT/STAT tag, headline (+ optional sub line after " / "), SOURCE line.
export function drawFactCard(c, card, src, age, fade) {
  const [head, sub] = card.split(' / ');
  const tag = /\d/.test(head) ? 'STAT' : 'FACT';
  const a = clamp01(age / 0.12) * fade, s = 0.85 + 0.15 * back(age / 0.28);
  const x = 110, w = 860, top = 170;
  c.save(); c.globalAlpha = a;
  c.font = '900 62px Inter'; const hl = wrap(c, head, w - 80);
  c.font = '700 36px Inter'; const sl = sub ? wrap(c, sub, w - 80) : [];
  const h = 92 + hl.length * 68 + sl.length * 44 + 70;
  c.translate(540, top); c.scale(s, s); c.translate(-540, -top);
  c.shadowColor = 'rgba(0,0,0,0.35)'; c.shadowBlur = 24; c.shadowOffsetY = 8;
  c.fillStyle = '#ffffff'; rrect(c, x, top, w, h, 26); c.fill();
  c.shadowColor = 'transparent';
  c.fillStyle = '#d7261e'; rrect(c, x + 36, top + 30, tag === 'STAT' ? 124 : 118, 46, 10); c.fill();
  c.fillStyle = '#fff'; c.font = '900 30px Inter'; c.textAlign = 'left'; c.textBaseline = 'alphabetic'; c.letterSpacing = '3px';
  c.fillText(tag, x + 52, top + 64); c.letterSpacing = '0px';
  let y = top + 92 + 56;
  c.fillStyle = '#141414'; c.font = '900 62px Inter';
  for (const l of hl) { c.fillText(l, x + 40, y); y += 68; }
  c.fillStyle = '#3a3a3a'; c.font = '700 36px Inter';
  for (const l of sl) { c.fillText(l, x + 40, y - 14); y += 44; }
  const names = (src || '').split('+').map((k) => SOURCES[k] || k).join(' + ');
  c.fillStyle = '#7a7a7a'; c.font = '700 25px Inter'; c.letterSpacing = '2px';
  c.fillText(('SOURCE: ' + names).toUpperCase(), x + 40, top + h - 30); c.letterSpacing = '0px';
  c.restore();
}

// Map card: crude low-poly continents, a pin on the Mediterranean; arrow (0..1) grows to Pennsylvania.
const NA = [[60, 70], [250, 40], [330, 90], [300, 160], [255, 175], [230, 230], [190, 300], [150, 260], [95, 200], [40, 140]];
const EU = [[470, 70], [610, 40], [700, 70], [690, 140], [640, 170], [560, 160], [500, 165], [470, 130]];
const AF = [[480, 200], [560, 190], [650, 195], [690, 260], [640, 360], [600, 420], [560, 380], [530, 300], [480, 260]];
export function drawMapCard(c, age, arrow, fade = 1) {
  const x = 150, y = 560, w = 780, h = 520, s = 0.85 + 0.15 * back(age / 0.3);
  c.save(); c.globalAlpha = clamp01(age / 0.12) * fade;
  c.translate(540, y + h / 2); c.scale(s, s); c.translate(-540, -(y + h / 2));
  c.shadowColor = 'rgba(0,0,0,0.35)'; c.shadowBlur = 24; c.shadowOffsetY = 8;
  c.fillStyle = '#ffffff'; rrect(c, x, y, w, h, 26); c.fill(); c.shadowColor = 'transparent';
  const mx = x + 30, my = y + 30;
  c.fillStyle = '#9fd0e8'; rrect(c, mx, my, w - 60, h - 60, 16); c.fill();
  c.fillStyle = '#e8d6a8';
  for (const poly of [NA, EU, AF]) { c.beginPath(); poly.forEach(([px, py], i) => (i ? c.lineTo(mx + px, my + py) : c.moveTo(mx + px, my + py))); c.closePath(); c.fill(); }
  c.fillStyle = '#9fd0e8'; c.beginPath(); c.ellipse(mx + 585, my + 178, 88, 14, 0, 0, Math.PI * 2); c.fill();  // the Mediterranean
  const pin = (px, py, label, lx) => {
    c.fillStyle = '#d7261e'; c.beginPath(); c.arc(px, py - 34, 18, Math.PI, 0); c.lineTo(px, py); c.closePath(); c.fill();
    c.fillStyle = '#fff'; c.beginPath(); c.arc(px, py - 34, 7, 0, 7); c.fill();
    c.fillStyle = '#141414'; c.font = '900 30px Inter'; c.textAlign = 'center'; c.fillText(label, lx, py + 40);
  };
  const A = [mx + 585, my + 178], B = [mx + 250, my + 120];
  if (arrow > 0) {
    const u = clamp01(arrow), cx = (A[0] + B[0]) / 2, cy = Math.min(A[1], B[1]) - 120;
    const pt = (q) => [(1 - q) * (1 - q) * A[0] + 2 * (1 - q) * q * cx + q * q * B[0], (1 - q) * (1 - q) * A[1] + 2 * (1 - q) * q * cy + q * q * B[1]];
    c.strokeStyle = '#d7261e'; c.lineWidth = 8; c.setLineDash([18, 12]); c.beginPath();
    for (let i = 0; i <= 40; i++) { const [px, py] = pt(u * i / 40); i ? c.lineTo(px, py) : c.moveTo(px, py); }
    c.stroke(); c.setLineDash([]);
    const [ex, ey] = pt(u), [qx, qy] = pt(Math.max(0, u - 0.03)), ang = Math.atan2(ey - qy, ex - qx);
    c.fillStyle = '#d7261e'; c.beginPath(); c.moveTo(ex + 22 * Math.cos(ang), ey + 22 * Math.sin(ang)); c.lineTo(ex + 18 * Math.cos(ang + 2.3), ey + 18 * Math.sin(ang + 2.3)); c.lineTo(ex + 18 * Math.cos(ang - 2.3), ey + 18 * Math.sin(ang - 2.3)); c.fill();
    if (u >= 1) pin(B[0], B[1], 'PENNSYLVANIA', B[0] + 10);
  }
  pin(A[0], A[1], 'MEDITERRANEAN', A[0] - 40);
  c.restore();
}

// Lease card: the person signs (sig 0..1 = how much of the signature is drawn).
export function drawLease(c, age, sig, fade = 1) {
  const x = 200, y = 600, w = 680, h = 470, s = 0.85 + 0.15 * back(age / 0.3);
  c.save(); c.globalAlpha = clamp01(age / 0.12) * fade;
  c.translate(540, y + h / 2); c.scale(s, s); c.rotate(-0.04); c.translate(-540, -(y + h / 2));
  c.shadowColor = 'rgba(0,0,0,0.35)'; c.shadowBlur = 24; c.shadowOffsetY = 8;
  c.fillStyle = '#fffdf6'; rrect(c, x, y, w, h, 18); c.fill(); c.shadowColor = 'transparent';
  c.fillStyle = '#141414'; c.textAlign = 'center'; c.font = '900 56px Inter'; c.fillText('LEASE', 540, y + 90);
  c.textAlign = 'left'; c.font = '700 34px Inter'; c.fillStyle = '#333';
  c.fillText('TENANT: HOUSE CENTIPEDE', x + 50, y + 170);
  c.fillText('RENT: ROACHES (MONTHLY)', x + 50, y + 225);
  c.strokeStyle = '#999'; c.lineWidth = 3; c.beginPath(); c.moveTo(x + 50, y + 380); c.lineTo(x + w - 50, y + 380); c.stroke();
  c.fillStyle = '#888'; c.font = '700 24px Inter'; c.fillText('SIGNED', x + 50, y + 415);
  if (sig > 0) {
    c.strokeStyle = '#1b3fa8'; c.lineWidth = 6; c.lineCap = 'round'; c.beginPath();
    const n = Math.floor(60 * clamp01(sig));
    for (let i = 0; i <= n; i++) { const q = i / 60, px = x + 70 + q * 440, py = y + 350 - 28 * Math.sin(q * 19) * (0.6 + 0.4 * Math.sin(q * 5)) - 10 * q; i ? c.lineTo(px, py) : c.moveTo(px, py); }
    c.stroke();
  }
  c.restore();
}

export function drawWatermark(c) {
  c.globalAlpha = 0.8; c.fillStyle = '#c4261e'; c.beginPath(); c.ellipse(54, 1757, 9, 4, 0, Math.PI, 0); c.fill();
  c.fillStyle = '#8f4a2b'; c.beginPath(); c.arc(54, 1764, 10, 0, Math.PI * 2); c.fill();
  c.fillStyle = '#fff'; c.font = '600 22px Lora'; c.letterSpacing = '4px'; c.textAlign = 'left'; c.fillText('MEATBALL MYTHS', 74, 1772); c.letterSpacing = '0px'; c.globalAlpha = 1;
}
