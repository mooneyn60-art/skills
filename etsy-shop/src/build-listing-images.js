// Listing photos for the "Dear Santa" letter listing (2000x1500 JPEG, 4:3 as Etsy recommends).
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const A = require('./art');

const DIR = path.join(__dirname, '..', 'listing-images');
const img = f => 'data:image/png;base64,' + fs.readFileSync(path.join(DIR, 'previews', f)).toString('base64');
const FONTS = `<link href="https://fonts.googleapis.com/css2?family=Mountains+of+Christmas:wght@700&family=Fredoka:wght@400;500;600&display=block" rel="stylesheet">`;
const css = `*{margin:0;padding:0;box-sizing:border-box}body{width:2000px;height:1500px;overflow:hidden;font-family:Fredoka}
.bg{position:absolute;inset:0;background:radial-gradient(circle at 30% 20%,#fff6ee,#f6e1d3 60%,#efcfbf)}
.wood{position:absolute;inset:0;background:repeating-linear-gradient(90deg,#c9a07a 0 180px,#bf946d 180px 184px,#cfa781 184px 360px);}
.paper{position:absolute;background:#fff;box-shadow:0 30px 60px rgba(60,30,10,.35),0 6px 14px rgba(60,30,10,.25)}
.paper img{width:100%;display:block}
h1{font-family:'Mountains of Christmas';color:#c1121f;line-height:1}
.pill{display:inline-block;background:#c1121f;color:#fff;border-radius:999px;padding:18px 44px;font-weight:600;font-size:46px}
.abs{position:absolute}`;

const pages = {
  '01-thumbnail': `
    <div class="wood"></div>
    <div class="paper" style="left:560px;top:90px;width:900px;transform:rotate(-3deg)"><img src="${img('dear-santa.png')}"></div>
    <div class="abs" style="left:60px;top:880px;transform:rotate(-8deg)">${A.gingerbread(2.4)}</div>
    <div class="abs" style="left:110px;top:120px">${A.gift(2.6)}</div>
    <div class="abs" style="right:70px;top:700px">${A.candycane(3)}</div>
    <div class="abs" style="right:80px;top:120px">${A.holly(2.6)}</div>
    <div class="abs" style="left:0;right:0;bottom:60px;text-align:center"><span class="pill" style="font-size:58px;padding:22px 60px;box-shadow:0 10px 30px rgba(0,0,0,.25)">Letter to Santa · Printable PDF</span></div>`,
  '02-whats-included': `
    <div class="bg"></div>
    <div class="paper" style="left:120px;top:150px;width:860px;transform:rotate(-2deg)"><img src="${img('dear-santa.png')}"></div>
    <div class="abs" style="left:1060px;top:170px;width:860px">
      <h1 style="font-size:130px">What's Included</h1>
      <div style="font-size:52px;color:#2b2d42;line-height:1.7;margin-top:40px">
        🎄 1 Dear Santa letter (PDF)<br>📄 US Letter size, 8.5 × 11 in<br>✏️ Fill-in name, age &amp; wish list<br>✅ Nice / Naughty checkboxes<br>🖨️ Print as many as your family needs
      </div>
      <div style="margin-top:60px"><span class="pill">⚡ INSTANT DOWNLOAD</span></div>
      <div style="font-size:36px;color:#7a7a8c;margin-top:30px">Digital file only. No physical item will be shipped.</div>
    </div>`,
  '03-how-it-works': `
    <div class="bg"></div>
    <h1 class="abs" style="left:0;right:0;top:110px;text-align:center;font-size:150px">How It Works</h1>
    <div class="abs" style="left:110px;right:110px;top:420px;display:flex;gap:60px">
      ${[['1', 'Purchase', 'Check out on Etsy', A.gift(1.4)], ['2', 'Download', 'Instantly from Purchases &amp; Reviews', A.star(1.4)], ['3', 'Print', 'At home or at any print shop', A.snowflake(1.4, '#4ea8de')], ['4', 'Write to Santa!', 'Fill in, decorate &amp; mail it to the North Pole', A.santa(0.8)]]
        .map(([n, t, d, art]) => `<div style="flex:1;background:#fff;border-radius:40px;padding:50px 30px;text-align:center;box-shadow:0 14px 30px rgba(0,0,0,.12)">
          <div style="width:110px;height:110px;margin:0 auto;border-radius:50%;background:#c1121f;color:#fff;font-size:64px;font-weight:600;display:flex;align-items:center;justify-content:center">${n}</div>
          <div style="height:190px;display:flex;align-items:center;justify-content:center;margin-top:30px">${art}</div>
          <div style="font-size:56px;font-weight:600;color:#2b2d42;margin-top:20px">${t}</div>
          <div style="font-size:36px;color:#6a6a7c;margin-top:16px;line-height:1.35">${d}</div></div>`).join('')}
    </div>
    <div class="abs" style="left:0;right:0;bottom:90px;text-align:center;font-size:40px;color:#6a6a7c">Tip: print on white cardstock at "Actual size" / 100% for the best result</div>`,
  '04-matching-set': `
    <div class="bg" style="background:radial-gradient(circle at 50% 30%,#f2fbf5,#d8efe1)"></div>
    <h1 class="abs" style="left:0;right:0;top:70px;text-align:center;font-size:130px;color:#2f7d4f">Complete the Santa Mail Set</h1>
    <div class="abs" style="left:0;right:0;top:250px;text-align:center;font-size:46px;color:#2b2d42">Matching Reply from Santa, Wish List, Nice List Certificate &amp; Elf Letter</div>
    <div class="paper" style="left:90px;top:440px;width:440px;transform:rotate(-5deg)"><img src="${img('dear-santa.png')}"></div>
    <div class="paper" style="left:470px;top:420px;width:440px;transform:rotate(2deg)"><img src="${img('reply-from-santa-letter.png')}"></div>
    <div class="paper" style="left:850px;top:430px;width:440px;transform:rotate(-2deg)"><img src="${img('christmas-wish-list.png')}"></div>
    <div class="paper" style="left:1230px;top:420px;width:440px;transform:rotate(4deg)"><img src="${img('christmas-elf-arrival-letter.png')}"></div>
    <div class="paper" style="left:1390px;top:1000px;width:540px;transform:rotate(-4deg)"><img src="${img('nice-list-certificate.png')}"></div>
    <div class="abs" style="left:120px;bottom:80px"><span class="pill" style="background:#2f7d4f">Find the bundle in our shop ★</span></div>`,
};

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 2000, height: 1500 } });
  for (const [name, body] of Object.entries(pages)) {
    await page.setContent(`<!doctype html><html><head><meta charset="utf-8">${FONTS}<style>${css}</style></head><body>${body}</body></html>`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(DIR, `dear-santa-${name}.jpg`), type: 'jpeg', quality: 86 });
    console.log('img', name);
  }
  await browser.close();
})();
