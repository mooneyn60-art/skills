// Pinterest pins (1000x1500) for listings added after the first pin batch:
// Elf Letter Bundle (4620465174), Christmas Eve Box Pack (4620620821), Wish List v2 (4620448127).
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const A = require('./art');
const ROOT = path.join(__dirname, '..');
const OUT = path.join(ROOT, 'pins');
const img = f => 'data:image/png;base64,' + fs.readFileSync(path.join(ROOT, 'listing-images', 'previews', f)).toString('base64');
const FONTS = `<link href="https://fonts.googleapis.com/css2?family=Mountains+of+Christmas:wght@700&family=Fredoka:wght@400;500;600;700&display=block" rel="stylesheet">`;
const css = `*{margin:0;padding:0;box-sizing:border-box}body{width:1000px;height:1500px;overflow:hidden;font-family:Fredoka;position:relative}
.abs{position:absolute}.paper{position:absolute;background:#fff;box-shadow:0 24px 50px rgba(60,30,10,.3)}.paper img{width:100%;display:block}
h1{font-family:'Mountains of Christmas';line-height:.95}.cta{display:inline-block;border-radius:999px;padding:16px 44px;font-weight:600;font-size:38px}`;
const stripe = 'repeating-linear-gradient(45deg,#e63946 0 34px,#fff 34px 68px)';
const pins = {
  'elf-bundle-A': `
    <div class="abs" style="inset:0;background:#dff7ec"></div>
    <div class="abs" style="left:0;right:0;top:0;height:40px;background:${stripe}"></div><div class="abs" style="left:0;right:0;bottom:0;height:40px;background:${stripe}"></div>
    <div class="abs" style="left:0;right:0;top:80px;text-align:center"><div style="font-size:40px;color:#1f5f43;font-weight:600;letter-spacing:.08em">4 LETTERS FROM YOUR CHRISTMAS ELF</div>
      <h1 style="font-size:118px;color:#c1121f;margin-top:16px">Elf Letter Bundle</h1></div>
    ${['elfb-1.png', 'elfb-2.png', 'elfb-3.png', 'elfb-4.png'].map((f, i) => `<div class="paper" style="left:${[40, 520, 60, 500][i]}px;top:${[390, 370, 800, 780][i]}px;width:420px;transform:rotate(${[-5, 4, 3, -4][i]}deg)"><img src="${img(f)}"></div>`).join('')}
    <div class="abs" style="left:0;right:0;bottom:80px;text-align:center"><span class="cta" style="background:#c1121f;color:#fff">Arrival · I'm Back · Reminder · Goodbye</span></div>`,
  'evebox-A': `
    <div class="abs" style="inset:0;background:radial-gradient(circle at 50% 25%,#fff0f3,#ffc9d6)"></div>
    <div class="abs" style="left:0;right:0;top:70px;text-align:center"><div style="font-size:40px;color:#b3123a;font-weight:600;letter-spacing:.08em">PRINTABLE CHRISTMAS EVE BOX PACK</div>
      <h1 style="font-size:122px;color:#b3123a;margin-top:14px">Christmas Eve Box</h1>
      <div style="font-size:38px;color:#5a2030;margin-top:12px">labels · reindeer food · cookies for Santa · magic key · checklist</div></div>
    ${['ceb-1.png', 'ceb-2.png', 'ceb-3.png', 'ceb-4.png', 'ceb-5.png'].map((f, i) => `<div class="paper" style="left:${[40, 350, 660, 180, 500][i]}px;top:${[470, 450, 470, 860, 850][i]}px;width:${i < 3 ? 310 : 330}px;transform:rotate(${[-6, 2, 6, -3, 4][i]}deg)"><img src="${img(f)}"></div>`).join('')}
    <div class="abs" style="left:0;right:0;bottom:60px;text-align:center"><span class="cta" style="background:#b3123a;color:#fff">⚡ Instant Download · Print Tonight</span></div>`,
  'wishlist-v2-A': `
    <div class="abs" style="inset:0;background:repeating-linear-gradient(90deg,#c9a07a 0 140px,#bf946d 140px 143px,#cfa781 143px 280px)"></div>
    <div class="abs" style="left:0;right:0;top:50px;text-align:center"><div style="display:inline-block;background:#fffdf8;border-radius:40px;padding:28px 50px;box-shadow:0 12px 30px rgba(0,0,0,.2)">
      <div style="font-size:38px;color:#2f7d4f;font-weight:600">THE 4-GIFT RULE FOR KIDS</div><h1 style="font-size:96px;color:#c1121f;margin-top:10px">Want · Need · Wear · Read</h1></div></div>
    <div class="paper" style="left:180px;top:390px;width:660px;transform:rotate(-2deg)"><img src="${img('wl2.png')}"></div>
    <div class="abs" style="left:40px;bottom:180px;transform:rotate(-10deg)">${A.gift(1.6)}</div>
    <div class="abs" style="left:0;right:0;bottom:50px;text-align:center"><span class="cta" style="background:#c1121f;color:#fff">Christmas Wish List Printable</span></div>`,
};
(async () => {
  const b = await chromium.launch();
  for (const [n, body] of Object.entries(pins)) {
    const page = await b.newPage({ viewport: { width: 1000, height: 1500 } });
    await page.setContent(`<!doctype html><html><head><meta charset="utf-8">${FONTS}<style>${css}</style></head><body>${body}</body></html>`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(OUT, `pin-${n}.jpg`), type: 'jpeg', quality: 85 });
    await page.close();
  }
  await b.close();
  console.log('pins', Object.keys(pins).length);
})();
