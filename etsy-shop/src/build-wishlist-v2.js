// "Christmas Wishlist" v2: her flat palette + layout inspired by the 4-gift wishlist format, made our own (ornament caps, flat icons).
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const ROOT = path.join(__dirname, '..');
const santa = fs.readFileSync(path.join(ROOT, 'work', 'santa', 'flat-santa.svg'), 'utf8');
const C = { pink: '#d85873', green: '#2d693c', teal: '#38807c', mint: '#b0deb5', mintLt: '#eef8f0', pinkLt: '#fbeef1', line: '#b9cfc0' };

const ornament = (color) => `<svg viewBox="0 0 40 52" width="34" height="44"><rect x="14" y="2" width="12" height="9" rx="2" fill="${C.green}"/><circle cx="20" cy="30" r="18" fill="${color}"/><path d="M6 30 q14 -9 28 0" stroke="#fff" stroke-width="3" fill="none"/><circle cx="13" cy="23" r="3" fill="#fff" opacity=".7"/></svg>`;
const bullet = (c) => `<svg viewBox="0 0 20 24" width="15" height="18"><rect x="7" y="0" width="6" height="5" rx="1" fill="${C.green}"/><circle cx="10" cy="14" r="8" fill="${c}"/></svg>`;
const icons = {
  gift: `<svg viewBox="0 0 40 40" width="38"><rect x="4" y="14" width="32" height="24" rx="3" fill="${C.pink}"/><rect x="2" y="10" width="36" height="8" rx="2" fill="#e27a90"/><rect x="17" y="10" width="6" height="28" fill="${C.mint}"/><path d="M20 10 q-12 -12 -12 -2 q0 4 12 2 q12 2 12 -2 q0 -10 -12 2" fill="${C.mint}"/></svg>`,
  sock: `<svg viewBox="0 0 40 40" width="38"><path d="M12 4 h16 v20 l6 6 a6 6 0 0 1 -8 8 l-12 -10 a6 6 0 0 1 -2 -4Z" fill="${C.pink}"/><rect x="11" y="3" width="18" height="8" rx="2" fill="${C.mint}"/><circle cx="20" cy="18" r="2" fill="#fff"/><circle cx="24" cy="25" r="2" fill="#fff"/></svg>`,
  sweater: `<svg viewBox="0 0 40 40" width="38"><path d="M12 6 l-10 8 4 8 4 -3 v18 h20 v-18 l4 3 4 -8 -10 -8 q-4 4 -8 4 q-4 0 -8 -4Z" fill="${C.teal}"/><path d="M10 24 h20" stroke="${C.mint}" stroke-width="3" stroke-dasharray="3 3"/><circle cx="20" cy="17" r="2.5" fill="${C.pink}"/></svg>`,
  book: `<svg viewBox="0 0 40 40" width="38"><path d="M4 8 q8 -3 16 2 v26 q-8 -5 -16 -2Z" fill="${C.green}"/><path d="M36 8 q-8 -3 -16 2 v26 q8 -5 16 -2Z" fill="${C.teal}"/><path d="M24 14 q5 -2 9 0 M24 19 q5 -2 9 0" stroke="${C.mint}" stroke-width="2" fill="none"/></svg>`,
  star: `<svg viewBox="0 0 40 40" width="44"><path d="M20 3 l5 11 12 1 -9 8 3 12 -11 -6 -11 6 3 -12 -9 -8 12 -1Z" fill="#f2c14e"/><circle cx="16" cy="16" r="2" fill="#fff" opacity=".8"/></svg>`,
};
const lines = (n, h = 34) => Array.from({ length: n }, () => `<div style="height:${h}px;border-bottom:2px solid ${C.line}"></div>`).join('');
const blines = (n, c = C.pink) => Array.from({ length: n }, (_, i) => `<div style="display:flex;align-items:flex-end;gap:8px;height:34px"><span style="margin-bottom:-3px">${bullet(i % 2 ? C.teal : c)}</span><div style="flex:1;border-bottom:2px solid ${C.line}"></div></div>`).join('');
const card = ({ x, y, w, h, title, icon, body, bg = C.mintLt, border = C.teal, orn = C.pink }) => `
  <div style="position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;background:${bg};border:2.5px dashed ${border};border-radius:22px;padding:22px 18px 10px">
    <div style="position:absolute;top:-30px;left:50%;transform:translateX(-50%)">${ornament(orn)}</div>
    <div style="display:flex;align-items:center;gap:8px;font-family:Fredoka;font-weight:600;color:${C.green};font-size:20px">${icon ? `<span style="display:inline-flex">${icons[icon]}</span>` : ''}${title}</div>${body}</div>`;
const flake = (x, y, s, c) => `<svg style="position:absolute;left:${x}px;top:${y}px" width="${s}" height="${s}" viewBox="0 0 20 20"><g stroke="${c}" stroke-width="2" stroke-linecap="round">${[0, 60, 120].map(r => `<path transform="rotate(${r} 10 10)" d="M10 2 V18 M10 5 l-2.5 -2.5 M10 5 l2.5 -2.5 M10 15 l-2.5 2.5 M10 15 l2.5 2.5"/>`).join('')}</g></svg>`;
const dot = (x, y, r, c) => `<div style="position:absolute;left:${x}px;top:${y}px;width:${r}px;height:${r}px;border-radius:50%;background:${c}"></div>`;
const tree = (x, y, w, fill, deco, garland) => {
  const h = w * 2.15;
  return `<svg style="position:absolute;left:${x}px;top:${y}px" width="${w}" height="${h}" viewBox="0 0 100 215">
  <path d="M50 0 L64 46 h-6 L76 98 h-8 L88 150 h-8 L100 215 H0 L20 150 h-8 L32 98 h-8 L42 46 h-6Z" fill="${fill}"/>
  ${[60, 120, 180].map(yy => `<path d="M${30 - yy / 10} ${yy} q${(40 + yy / 5) / 2} 10 ${40 + yy / 5} -6" stroke="#fff" stroke-width="2.5" fill="none"/>`).join('')}
  ${[[44, 64], [56, 66], [32, 124], [52, 128], [70, 122], [22, 186], [48, 190], [76, 184]].map(([cx, cy]) => `<circle cx="${cx}" cy="${cy}" r="4.2" fill="${garland}"/>`).join('')}
  ${[[50, 26], [40, 92], [60, 154]].map(([cx, cy]) => `<path d="M${cx - 9} ${cy} q4 -7 8 0 q4 7 8 0 q4 -7 8 0" stroke="${deco}" stroke-width="3" fill="none" stroke-linecap="round"/>`).join('')}
  <path d="M50 -14 l4 9 10 1 -8 6 3 10 -9 -5 -9 5 3 -10 -8 -6 10 -1Z" fill="#f2c14e" transform="translate(0,4) scale(1)"/></svg>`;
};

const page = `
<div style="position:relative;width:794px;height:1123px;background:#fff;overflow:hidden">
  ${flake(20, 300, 18, C.mint)}${flake(740, 285, 20, C.pink)}${flake(320, 440, 14, C.mint)}${flake(760, 870, 18, C.mint)}${dot(305, 30, 9, C.pink)}${dot(770, 380, 8, C.mint)}${dot(30, 440, 8, C.pink)}
  <div style="position:absolute;left:8px;top:14px;width:300px">${santa.replace('<svg ', '<svg width="300" height="265" ')}</div>
  <div style="position:absolute;left:318px;top:-6px;font-family:'Dancing Script';font-weight:700;font-size:118px;color:${C.pink};line-height:1">Christmas</div>
  <div style="position:absolute;left:400px;top:118px;font-family:'Gochi Hand';font-size:84px;color:${C.green};letter-spacing:6px;transform:rotate(-2deg)">WISHLIST</div>
  <svg style="position:absolute;left:316px;top:216px" width="470" height="60" viewBox="0 0 470 60"><path d="M6 40 q30 -30 50 -4 q-20 18 -12 -2 q100 -26 160 0 M290 34 q60 -24 170 -6 q10 4 0 10" stroke="${C.pink}" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M247 50 c-26 -18 -16 -36 0 -24 c16 -12 26 6 0 24Z" fill="none" stroke="${C.pink}" stroke-width="3"/></svg>
  <div style="position:absolute;left:46px;top:290px;right:40px;display:flex;align-items:flex-end;gap:10px;font-family:Fredoka;font-weight:600;font-size:30px;color:${C.green}">My Name:<div style="flex:1;border-bottom:2.5px solid ${C.green};height:34px"></div>Age:<div style="width:80px;border-bottom:2.5px solid ${C.green};height:34px"></div></div>
  <div style="position:absolute;left:52px;top:342px;font-family:'Dancing Script';font-weight:700;font-size:64px;color:${C.pink}">Dear Santa,</div>
  <div style="position:absolute;left:56px;top:418px;font-family:'Patrick Hand';font-size:24px;color:#333">I've been extra good this year! Here are a few things I'm wishing for…</div>
  ${card({ x: 40, y: 486, w: 425, h: 222, title: 'My Christmas Wishes', icon: 'gift', body: blines(4), orn: C.pink })}
  ${card({ x: 485, y: 486, w: 272, h: 100, title: 'Something I Want', icon: 'gift', body: lines(1, 30), bg: C.pinkLt, border: C.pink, orn: C.teal })}
  ${card({ x: 485, y: 622, w: 272, h: 98, title: 'Something I Need', icon: 'sock', body: lines(1, 30), bg: C.mintLt, border: C.teal, orn: C.pink })}
  ${card({ x: 360, y: 746, w: 192, h: 142, title: 'Something to Wear', icon: 'sweater', body: lines(2, 30), bg: C.pinkLt, border: C.pink, orn: C.teal })}
  ${card({ x: 568, y: 746, w: 189, h: 142, title: 'Something to Read', icon: 'book', body: lines(2, 30), bg: C.mintLt, border: C.teal, orn: C.pink })}
  ${card({ x: 360, y: 922, w: 397, h: 150, title: 'My BIGGEST Christmas Wish', icon: 'star', body: lines(2, 38), bg: '#fff8e8', border: '#e3b23c', orn: C.pink })}
  ${tree(110, 744, 210, C.mint, C.teal, C.pink)}${tree(-34, 868, 156, C.teal, C.mint, C.pink)}
  <div style="position:absolute;left:262px;top:1046px">${icons.gift.replace('width="38"', 'width="70"')}</div>
  <div style="position:absolute;left:420px;bottom:10px;font-family:Fredoka;font-size:11px;letter-spacing:.3em;color:#a9b8ad">DOODLE DESIGN &amp; CO · PERSONAL USE</div>
</div>`;

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 3 });
  await p.setContent(`<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Gochi+Hand&family=Fredoka:wght@400;600&family=Patrick+Hand&display=block" rel="stylesheet"><style>@page{margin:0;size:794px 1123px}*{box-sizing:border-box;margin:0;padding:0}body{-webkit-print-color-adjust:exact;print-color-adjust:exact}</style></head><body>${page}</body></html>`, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const out = path.join(ROOT, 'products');
  await p.screenshot({ path: path.join(ROOT, 'work', 'wishlist-v2.png') });
  await p.pdf({ path: path.join(out, 'christmas-wishlist-v2-A4.pdf'), width: '794px', height: '1123px', printBackground: true });
  // US Letter: same design scaled to fit 8.5x11
  await p.setContent(`<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Gochi+Hand&family=Fredoka:wght@400;600&family=Patrick+Hand&display=block" rel="stylesheet"><style>@page{margin:0;size:816px 1056px}*{box-sizing:border-box;margin:0;padding:0}body{width:816px;height:1056px;overflow:hidden;display:flex;justify-content:center;-webkit-print-color-adjust:exact;print-color-adjust:exact}.s{transform:scale(${1056 / 1123});transform-origin:top center;height:1056px}</style></head><body><div class="s">${page}</div></body></html>`, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: path.join(out, 'christmas-wishlist-v2-Letter.pdf'), width: '816px', height: '1056px', printBackground: true });
  await b.close(); console.log('ok');
})();
