// Listing photos for 2027 Planner + Budget Planner (2000x1500).
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const DIR = path.join(__dirname, '..', 'listing-images');
const img = f => 'data:image/png;base64,' + fs.readFileSync(path.join(DIR, 'previews', f)).toString('base64');
const FONTS = `<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&family=Jost:wght@300;400;500&display=block" rel="stylesheet">`;
const css = `*{margin:0;padding:0;box-sizing:border-box}body{width:2000px;height:1500px;overflow:hidden;font-family:Jost;color:#3d3d3a;position:relative}
.abs{position:absolute}.paper{position:absolute;background:#fff;box-shadow:0 24px 50px rgba(60,50,30,.22),0 4px 10px rgba(60,50,30,.12)}.paper img{width:100%;display:block}
h1{font-family:'Cormorant Garamond';font-weight:500;line-height:1}
.bg{position:absolute;inset:0;background:linear-gradient(135deg,#f3ede3,#e4e9df)}
.pill{display:inline-block;background:#8a9a82;color:#fff;border-radius:999px;padding:18px 48px;font-size:42px;letter-spacing:.06em}
.chip{background:#fff;border-radius:24px;padding:22px 30px;font-size:38px;box-shadow:0 8px 20px rgba(0,0,0,.06)}`;

const thumb = (cover, a, b, label) => `<div class="bg"></div>
  <div class="paper" style="left:180px;top:170px;width:620px;transform:rotate(-6deg)"><img src="${img(a)}"></div>
  <div class="paper" style="left:1200px;top:170px;width:620px;transform:rotate(6deg)"><img src="${img(b)}"></div>
  <div class="paper" style="left:640px;top:90px;width:720px"><img src="${img(cover)}"></div>
  <div class="abs" style="left:0;right:0;bottom:70px;text-align:center"><span class="pill" style="font-size:54px;padding:24px 64px">${label}</span></div>`;
const grid = (files, title, sub) => `<div class="bg"></div>
  <div class="abs" style="left:0;right:0;top:60px;text-align:center"><h1 style="font-size:110px">${title}</h1><div style="font-size:40px;letter-spacing:.25em;color:#8a9a82;margin-top:14px">${sub}</div></div>
  <div class="abs" style="left:90px;right:90px;top:300px;display:flex;flex-wrap:wrap;gap:26px;justify-content:center">
  ${files.map(f => `<div style="width:${files.length > 12 ? 250 : 330}px;background:#fff;box-shadow:0 8px 18px rgba(0,0,0,.1)"><img src="${img(f)}" style="width:100%;display:block"></div>`).join('')}</div>`;
const incl = (cover, title, items) => `<div class="bg"></div>
  <div class="paper" style="left:130px;top:150px;width:860px;transform:rotate(-2deg)"><img src="${img(cover)}"></div>
  <div class="abs" style="left:1080px;top:150px;width:840px"><h1 style="font-size:110px">What's Included</h1>
  <div style="display:flex;flex-direction:column;gap:18px;margin-top:40px">${items.map(i => `<div class="chip">${i}</div>`).join('')}</div>
  <div style="margin-top:40px"><span class="pill">⚡ INSTANT DOWNLOAD</span></div></div>`;

const pages = {
  'planner-01-thumbnail': thumb('pl-01.png', 'pl-02.png', 'pl-04.png', '2027 Printable Planner'),
  'planner-02-pages': grid(Array.from({ length: 19 }, (_, i) => `plsm-${String(i + 1).padStart(2, '0')}.png`), '19 Printable Pages', 'MINIMAL · UNDATED WEEKLY & DAILY · DATED 2027 MONTHS'),
  'planner-03-included': incl('pl-04.png', '', ['📅 2027 year at a glance', '🗓️ 12 dated monthly calendars', '✍️ Weekly + daily planner pages', '🎯 Goals page & habit tracker', '📄 US Letter + A4 PDF · print unlimited']),
  'planner-04-daily': thumb('pl-18.png', 'pl-03.png', 'pl-19.png', 'Weekly · Daily · Habit Tracker'),
  'budget-01-thumbnail': thumb('bg-1.png', 'bg-3.png', 'bg-6.png', 'Printable Budget Planner'),
  'budget-02-pages': grid(Array.from({ length: 9 }, (_, i) => `bg-${i + 1}.png`), '9 Budget Pages', 'TRACK · SAVE · PAY OFF DEBT'),
  'budget-03-included': incl('bg-3.png', '', ['💰 Monthly budget & annual overview', '🧾 Expense & bill payment trackers', '🎯 Savings goal & sinking funds', '📉 Debt payoff tracker', '🚫 30-day no-spend challenge']),
  'budget-04-detail': thumb('bg-7.png', 'bg-4.png', 'bg-9.png', 'Savings · Debt · No-Spend'),
};

const cthumb = `<div class="bg"></div>
  <div class="paper" style="left:120px;top:560px;width:820px;transform:rotate(-5deg)"><img src="${img('cal-04.png')}"></div>
  <div class="paper" style="left:1060px;top:560px;width:820px;transform:rotate(5deg)"><img src="${img('cal-11.png')}"></div>
  <div class="paper" style="left:440px;top:90px;width:1120px"><img src="${img('cal-01.png')}"></div>
  <div class="abs" style="left:0;right:0;bottom:60px;text-align:center"><span class="pill" style="font-size:54px;padding:24px 64px">2027 Printable Wall Calendar</span></div>`;
pages['calendar-01-thumbnail'] = cthumb;
pages['calendar-02-pages'] = `<div class="bg"></div>
  <div class="abs" style="left:0;right:0;top:60px;text-align:center"><h1 style="font-size:110px">13 Printable Pages</h1><div style="font-size:40px;letter-spacing:.25em;color:#8a9a82;margin-top:14px">COVER + 12 MONTHS · LANDSCAPE</div></div>
  <div class="abs" style="left:80px;right:80px;top:310px;display:flex;flex-wrap:wrap;gap:24px;justify-content:center">
  ${Array.from({ length: 13 }, (_, i) => `<div style="width:340px;background:#fff;box-shadow:0 8px 18px rgba(0,0,0,.1)"><img src="${img('calsm-' + String(i + 1).padStart(2, '0') + '.png')}" style="width:100%;display:block"></div>`).join('')}</div>`;
pages['calendar-03-detail'] = `<div class="bg"></div><div class="paper" style="left:150px;top:150px;width:1700px"><img src="${img('cal-07.png')}"></div>`;
pages['calendar-04-included'] = `<div class="bg"></div>
  <div class="paper" style="left:90px;top:380px;width:980px;transform:rotate(-2deg)"><img src="${img('cal-02.png')}"></div>
  <div class="abs" style="left:1130px;top:150px;width:800px"><h1 style="font-size:110px">What's Included</h1>
  <div style="display:flex;flex-direction:column;gap:18px;margin-top:40px">${['🌿 Cover + 12 monthly pages', '📅 Accurate 2027 dates, Sunday start', '✍️ Notes section every month', '🎨 A different botanical color each month', '📄 US Letter + A4 landscape PDF'].map(i => `<div class="chip">${i}</div>`).join('')}</div>
  <div style="margin-top:40px"><span class="pill">⚡ INSTANT DOWNLOAD</span></div></div>`;

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 2000, height: 1500 } });
  for (const [n, body] of Object.entries(pages).filter(([n]) => !process.argv[2] || n.startsWith(process.argv[2]))) {
    await p.setContent(`<!doctype html><html><head><meta charset="utf-8">${FONTS}<style>${css}</style></head><body>${body}</body></html>`, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(DIR, `${n}.jpg`), type: 'jpeg', quality: 86 });
  }
  await b.close();
  console.log('ok');
})();
