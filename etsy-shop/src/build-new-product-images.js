// Listing photos (2000x1500) for the coloring book + Holly Jolly wall art.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const A = require('./art');
const DIR = path.join(__dirname, '..', 'listing-images');
const img = f => 'data:image/png;base64,' + fs.readFileSync(path.join(DIR, 'previews', f)).toString('base64');
const cb = n => `cb-${String(n).padStart(2, '0')}.png`;
const FONTS = `<link href="https://fonts.googleapis.com/css2?family=Mountains+of+Christmas:wght@700&family=Fredoka:wght@400;500;600&display=block" rel="stylesheet">`;
const css = `*{margin:0;padding:0;box-sizing:border-box}body{width:2000px;height:1500px;overflow:hidden;font-family:Fredoka;position:relative}
.abs{position:absolute}.paper{position:absolute;background:#fff;box-shadow:0 26px 56px rgba(60,30,10,.35)}.paper img{width:100%;display:block}
h1{font-family:'Mountains of Christmas';color:#c1121f;line-height:1}
.wood{position:absolute;inset:0;background:repeating-linear-gradient(90deg,#c9a07a 0 180px,#bf946d 180px 184px,#cfa781 184px 360px)}
.bg{position:absolute;inset:0;background:radial-gradient(circle at 30% 20%,#fff6ee,#f6e1d3 60%,#efcfbf)}
.pill{display:inline-block;background:#c1121f;color:#fff;border-radius:999px;padding:20px 54px;font-weight:600;font-size:52px;box-shadow:0 10px 30px rgba(0,0,0,.25)}
.chip{background:#fff;border-radius:24px;padding:20px 30px;font-size:40px;box-shadow:0 8px 20px rgba(0,0,0,.08)}
.crayon{position:absolute;width:300px;height:42px;border-radius:8px}`;
const crayons = ['#e63946', '#2a9d8f', '#f4c430', '#4ea8de', '#8a5a3b'].map((c, i) => `<div class="crayon" style="background:${c};left:${1560 + i * 18}px;top:${960 + i * 56}px;transform:rotate(-28deg);box-shadow:0 6px 12px rgba(0,0,0,.25)"><div style="position:absolute;right:-34px;top:6px;border-left:40px solid ${c};border-top:15px solid transparent;border-bottom:15px solid transparent;filter:brightness(.85)"></div></div>`).join('');

const pages = {
  'coloring-01-thumbnail': `<div class="wood"></div>
    ${[[cb(4), 130, 220, -9], [cb(8), 1240, 200, 8]].map(([f, l, t, r]) => `<div class="paper" style="left:${l}px;top:${t}px;width:620px;transform:rotate(${r}deg)"><img src="${img(f)}"></div>`).join('')}
    <div class="paper" style="left:640px;top:80px;width:720px"><img src="${img(cb(1))}"></div>${crayons}
    <div class="abs" style="left:0;right:0;bottom:56px;text-align:center"><span class="pill">20 Christmas Coloring Pages · Printable</span></div>`,
  'coloring-02-pages': `<div class="bg"></div>
    <div class="abs" style="left:0;right:0;top:40px;text-align:center"><h1 style="font-size:104px">20 Pages to Color</h1><div style="font-size:38px;color:#2f7d4f;letter-spacing:.2em;margin-top:6px">SANTA · ELVES · REINDEER · GINGERBREAD · SNOWMEN</div></div>
    <div class="abs" style="left:70px;right:70px;top:250px;display:flex;flex-wrap:wrap;gap:20px;justify-content:center">
    ${Array.from({ length: 20 }, (_, i) => `<div style="width:170px;background:#fff;box-shadow:0 6px 14px rgba(0,0,0,.12)"><img src="${img(cb(i + 2))}" style="width:100%;display:block"></div>`).join('')}</div>`,
  'coloring-03-included': `<div class="bg"></div>
    <div class="paper" style="left:120px;top:150px;width:860px;transform:rotate(-2deg)"><img src="${img(cb(13))}"></div>
    <div class="abs" style="left:1060px;top:140px;width:880px"><h1 style="font-size:110px">What's Included</h1>
    <div style="display:flex;flex-direction:column;gap:16px;margin-top:36px">${['🎨 Cover + 20 coloring pages', '🎅 Santa, elves, reindeer & cozy scenes', '💌 Bonus "Note from Santa" page', '📄 US Letter + A4 PDF', '🖨️ Print as many times as you like'].map(i => `<div class="chip">${i}</div>`).join('')}</div>
    <div style="margin-top:36px"><span class="pill" style="font-size:44px">⚡ INSTANT DOWNLOAD</span></div></div>`,
  'coloring-04-note': `<div class="wood"></div>
    <div class="paper" style="left:180px;top:120px;width:760px;transform:rotate(-3deg)"><img src="${img(cb(22))}"></div>
    <div class="abs" style="left:1040px;top:260px;width:860px"><h1 style="font-size:96px">A Note from Santa</h1>
    <div style="font-size:48px;color:#fff;margin-top:30px;line-height:1.5;text-shadow:0 3px 8px rgba(0,0,0,.4)">The last page says they're officially on the Nice List, signed by Santa himself 🎅</div>
    <div style="margin-top:40px"><span class="pill" style="background:#2f7d4f;font-size:44px">Perfect for Christmas Eve boxes 🎁</span></div></div>`,
  'wishlist2-01-thumbnail': `<div class="wood"></div>
    <div class="paper" style="left:560px;top:70px;width:900px;transform:rotate(-2deg)"><img src="${img('wl2.png')}"></div>
    <div class="abs" style="left:90px;top:120px">${A.gift(2.4)}</div><div class="abs" style="left:1600px;top:820px">${A.candycane(2.6)}</div>
    <div class="abs" style="left:0;right:0;bottom:50px;text-align:center"><span class="pill">Christmas Wish List · Want Need Wear Read</span></div>`,
  'wishlist2-02-closeup': `<div class="bg"></div><div class="paper" style="left:-260px;top:-380px;width:2520px"><img src="${img('wl2.png')}"></div>`,
  'wishlist2-03-included': `<div class="bg"></div>
    <div class="paper" style="left:120px;top:110px;width:880px;transform:rotate(-2deg)"><img src="${img('wl2.png')}"></div>
    <div class="abs" style="left:1060px;top:150px;width:880px"><h1 style="font-size:110px">What's Included</h1>
    <div style="display:flex;flex-direction:column;gap:16px;margin-top:36px">${['🎁 My Christmas Wishes list', '🧦 Want · Need · Wear · Read boxes', '⭐ "My BIGGEST Christmas Wish"', '📄 US Letter + A4 PDF', '🖨️ Print one for every kid'].map(i => `<div class="chip">${i}</div>`).join('')}</div>
    <div style="margin-top:36px"><span class="pill" style="font-size:44px">⚡ INSTANT DOWNLOAD</span></div></div>`,
  'hollyjolly-01-thumbnail': `<div class="abs" style="inset:0;background:linear-gradient(#efe9e1,#e6ddd2)"></div>
    <div class="abs" style="left:0;right:0;bottom:0;height:300px;background:#cdb9a3"></div>
    <div class="abs" style="left:640px;top:110px;width:720px;padding:34px;background:#f7f3ec;border:26px solid #3b2a20;box-shadow:0 30px 60px rgba(0,0,0,.35)"><img src="${img('hj.png')}" style="width:100%;display:block"></div>
    <div class="abs" style="left:150px;top:820px">${A.tree(2.2)}</div><div class="abs" style="left:1550px;top:960px">${A.gift(2.4)}</div>
    <div class="abs" style="left:0;right:0;bottom:50px;text-align:center"><span class="pill">Holly Jolly Christmas Printable Wall Art</span></div>`,
  'hollyjolly-02-closeup': `<div class="bg"></div><div class="paper" style="left:560px;top:60px;width:880px"><img src="${img('hj.png')}"></div>`,
  'hollyjolly-03-included': `<div class="bg"></div>
    <div class="paper" style="left:140px;top:150px;width:800px;transform:rotate(-2deg)"><img src="${img('hj.png')}"></div>
    <div class="abs" style="left:1040px;top:180px;width:880px"><h1 style="font-size:110px">What's Included</h1>
    <div style="display:flex;flex-direction:column;gap:16px;margin-top:36px">${['🎄 Holly Jolly Christmas print', '📄 US Letter (8.5×11) + A4 PDF', '🖼️ Fits standard frames', '✉️ Also works as a card or gift tag', '🖨️ Print at home or a print shop'].map(i => `<div class="chip">${i}</div>`).join('')}</div>
    <div style="margin-top:36px"><span class="pill" style="font-size:44px">⚡ INSTANT DOWNLOAD</span></div></div>`,
  'hollyjolly-04-mantel': `<div class="abs" style="inset:0;background:linear-gradient(#3d4a40,#2c362f)"></div>
    <div class="abs" style="left:0;right:0;top:1060px;height:70px;background:#6b4a33;box-shadow:0 20px 40px rgba(0,0,0,.4)"></div>
    <div class="abs" style="left:760px;top:330px;width:480px;padding:22px;background:#fff;border:18px solid #c9a46a;box-shadow:0 20px 40px rgba(0,0,0,.5)"><img src="${img('hj.png')}" style="width:100%;display:block"></div>
    <div class="abs" style="left:240px;top:700px">${A.tree(1.7)}</div><div class="abs" style="left:1440px;top:760px">${A.snowman(1.4)}</div>
    <div class="abs" style="left:0;right:0;top:1200px;text-align:center;font-size:52px;color:#fff;font-weight:600">Cozy Christmas decor in minutes ✨</div>`,
};
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 2000, height: 1500 } });
  for (const [n, body] of Object.entries(pages).filter(([n]) => !process.argv[2] || n.startsWith(process.argv[2]))) {
    await p.setContent(`<!doctype html><html><head><meta charset="utf-8">${FONTS}<style>${css}</style></head><body>${body}</body></html>`, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(DIR, `${n}.jpg`), type: 'jpeg', quality: 86 });
  }
  await b.close(); console.log('ok');
})();
