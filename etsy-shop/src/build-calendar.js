// 2027 printable wall calendar — 13 landscape pages, minimal botanical style. US Letter + A4.
const { chromium } = require('playwright');
const path = require('path');
const OUT = path.join(__dirname, '..', 'products');
const FONTS = `<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&family=Jost:wght@300;400;500&display=block" rel="stylesheet">`;
const Y = 2027;
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const PAL = ['#8a9a82', '#b9a7c9', '#9cb59a', '#e0a98f', '#c9b27a', '#7fa7b5', '#d38f7b', '#a3b18a', '#c4925e', '#b5734f', '#8c7d6b', '#7b9a8a'];
const sprig = c => `<svg viewBox="0 0 120 220" width="100%" height="100%"><path d="M60 215 C58 150 62 90 60 10" stroke="${c}" stroke-width="3" fill="none"/>
  ${[30, 60, 90, 120, 150, 180].map((y, i) => `<ellipse cx="${i % 2 ? 82 : 38}" cy="${y}" rx="22" ry="10" fill="${c}" opacity="${0.55 + (i % 3) * 0.15}" transform="rotate(${i % 2 ? -30 : 30} ${i % 2 ? 82 : 38} ${y})"/>`).join('')}
  <ellipse cx="60" cy="10" rx="9" ry="14" fill="${c}"/></svg>`;
const css = `@page{margin:0}*{box-sizing:border-box;margin:0;padding:0}body{font-family:Jost;color:#3d3d3a;font-weight:300;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:100vw;height:100vh;page-break-after:always;display:flex;padding:6vh 4.5vw;gap:4vw;background:#fdfbf7;position:relative;overflow:hidden}
h1{font-family:'Cormorant Garamond';font-weight:500;line-height:1}
table{border-collapse:collapse;width:100%;height:100%;table-layout:fixed}
th{font-size:1.7vh;letter-spacing:.2em;font-weight:500;padding-bottom:1vh}
td{border-top:1px solid #d9d4c9;vertical-align:top;padding:.8vh .6vw;font-size:2.2vh}
.ft{position:absolute;bottom:2vh;right:4.5vw;font-size:1.1vh;letter-spacing:.3em;color:#b0aa9e}`;
const weeks = m => {
  const first = new Date(Date.UTC(Y, m, 1)).getUTCDay(), days = new Date(Date.UTC(Y, m + 1, 0)).getUTCDate();
  const c = [...Array(first).fill(''), ...Array.from({ length: days }, (_, i) => i + 1)];
  while (c.length % 7) c.push('');
  return Array.from({ length: c.length / 7 }, (_, i) => c.slice(i * 7, i * 7 + 7));
};
const pages = [`<div class="pg" style="align-items:center;justify-content:center;flex-direction:column;text-align:center">
  <div style="display:flex;gap:2vw;height:28vh">${PAL.slice(0, 5).map(c => `<div style="width:7vw">${sprig(c)}</div>`).join('')}</div>
  <h1 style="font-size:26vh;color:#8a9a82;margin-top:3vh">${Y}</h1><div style="font-size:2.4vh;letter-spacing:.6em;margin-top:1vh">WALL CALENDAR</div>
  <div class="ft">DOODLE DESIGN &amp; CO</div></div>`];
MONTHS.forEach((n, m) => {
  const c = PAL[m];
  pages.push(`<div class="pg">
    <div style="width:24vw;display:flex;flex-direction:column">
      <div style="font-size:1.6vh;letter-spacing:.4em;color:${c};font-weight:500">${Y}</div>
      <h1 style="font-size:7.2vh;margin-top:1vh">${n}</h1>
      <div style="font-size:1.5vh;letter-spacing:.3em;margin-top:1vh;color:#999">${String(m + 1).padStart(2, '0')} / 12</div>
      <div style="flex:1;margin:4vh 2vw 0">${sprig(c)}</div>
      <div style="border-top:1px solid #d9d4c9;padding-top:1vh;font-size:1.4vh;letter-spacing:.2em;height:12vh">NOTES</div>
    </div>
    <div style="flex:1"><table><tr>${['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'].map(d => `<th style="color:${c}">${d}</th>`).join('')}</tr>
      ${weeks(m).map(w => `<tr>${w.map(d => `<td>${d}</td>`).join('')}</tr>`).join('')}</table></div>
    <div class="ft">DOODLE DESIGN &amp; CO · PERSONAL USE</div></div>`);
});
(async () => {
  const b = await chromium.launch();
  for (const fmt of ['Letter', 'A4']) {
    const p = await b.newPage();
    await p.setViewportSize(fmt === 'Letter' ? { width: 1056, height: 816 } : { width: 1123, height: 794 });
    await p.setContent(`<!doctype html><html><head><meta charset="utf-8">${FONTS}<style>${css}</style></head><body>${pages.join('')}</body></html>`, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: path.join(OUT, `2027-wall-calendar-${fmt}.pdf`), format: fmt, landscape: true, printBackground: true });
  }
  await b.close();
  console.log('calendar', pages.length);
})();
