// Pinterest pins (1000x1500) — 2 designs per listing.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const A = require('./art');

const ROOT = path.join(__dirname, '..');
const OUT = path.join(ROOT, 'pins');
fs.mkdirSync(OUT, { recursive: true });
const img = f => 'data:image/png;base64,' + fs.readFileSync(path.join(ROOT, 'listing-images', 'previews', f)).toString('base64');
const FONTS = `<link href="https://fonts.googleapis.com/css2?family=Mountains+of+Christmas:wght@700&family=Fredoka:wght@400;500;600&display=block" rel="stylesheet">`;
const css = `*{margin:0;padding:0;box-sizing:border-box}body{width:1000px;height:1500px;overflow:hidden;font-family:Fredoka;position:relative}
.abs{position:absolute}.paper{position:absolute;background:#fff;box-shadow:0 24px 50px rgba(60,30,10,.35)}.paper img{width:100%;display:block}
h1{font-family:'Mountains of Christmas';line-height:.95}
.band{position:absolute;left:0;right:0;text-align:center;color:#fff}
.cta{display:inline-block;background:#fff;color:#c1121f;border-radius:999px;padding:16px 44px;font-weight:600;font-size:38px}`;

const P = [
  { slug: 'dear-santa', file: 'dear-santa.png', h: 'Letter to Santa', sub: 'Printable for Kids', hook: 'A Christmas tradition they\'ll love' },
  { slug: 'reply-from-santa', file: 'reply-from-santa-letter.png', h: 'Letter from Santa', sub: 'Printable Reply', hook: 'Make Christmas morning magical' },
  { slug: 'nice-list', file: 'nice-list-certificate.png', h: 'Nice List Certificate', sub: 'Printable', hook: 'Perfect for Christmas Eve boxes', land: true },
  { slug: 'wish-list', file: 'christmas-wish-list.png', h: 'Christmas Wish List', sub: 'Printable for Kids', hook: 'Easy holiday gift planning' },
  { slug: 'elf-arrival', file: 'christmas-elf-arrival-letter.png', h: 'Elf Arrival Letter', sub: 'Printable', hook: 'Welcome your Christmas elf' },
];

const pins = {};
for (const p of P) {
  const pw = p.land ? 900 : 700;
  // Design A: wood mockup + red title band
  pins[`${p.slug}-A`] = `
    <div class="abs" style="inset:0;background:repeating-linear-gradient(90deg,#c9a07a 0 140px,#bf946d 140px 143px,#cfa781 143px 280px)"></div>
    <div class="band" style="top:0;height:330px;background:#c1121f;padding-top:50px">
      <h1 style="font-size:104px">${p.h}</h1><div style="font-size:44px;margin-top:14px;letter-spacing:.06em">${p.sub.toUpperCase()}</div></div>
    <div class="paper" style="left:${500 - pw / 2}px;top:${p.land ? 520 : 390}px;width:${pw}px;transform:rotate(-3deg)"><img src="${img(p.file)}"></div>
    <div class="abs" style="left:20px;bottom:200px;transform:rotate(-10deg)">${A.gingerbread(1.3)}</div>
    <div class="abs" style="right:20px;bottom:220px">${A.candycane(1.6)}</div>
    <div class="band" style="bottom:0;height:170px;background:#2f7d4f;padding-top:38px"><span class="cta" style="color:#2f7d4f">⚡ Instant Download · Print Today</span></div>`;
  // Design B: light background, hook text, tilted paper
  pins[`${p.slug}-B`] = `
    <div class="abs" style="inset:0;background:radial-gradient(circle at 50% 25%,#fff8f0,#f6dccb)"></div>
    <div class="abs" style="left:40px;top:40px">${A.snowflake(.9)}</div><div class="abs" style="right:40px;top:60px">${A.snowflake(.7)}</div>
    <div class="abs" style="left:0;right:0;top:80px;text-align:center">
      <div style="font-size:40px;color:#2f7d4f;font-weight:600;letter-spacing:.08em">${p.hook.toUpperCase()}</div>
      <h1 style="font-size:120px;color:#c1121f;margin-top:16px">${p.h}</h1></div>
    <div class="paper" style="left:${500 - pw / 2 + 20}px;top:${p.land ? 560 : 420}px;width:${pw}px;transform:rotate(3deg)"><img src="${img(p.file)}"></div>
    <div class="abs" style="left:0;right:0;bottom:60px;text-align:center"><span class="cta" style="background:#c1121f;color:#fff">Shop on Etsy · DoodleDesignAndCo</span></div>`;
}
// Bundle pins
const fan = (top) => ['dear-santa.png', 'reply-from-santa-letter.png', 'christmas-wish-list.png', 'christmas-elf-arrival-letter.png']
  .map((f, i) => `<div class="paper" style="left:${40 + i * 215}px;top:${top + (i % 2) * 30}px;width:330px;transform:rotate(${[-8, -3, 3, 8][i]}deg)"><img src="${img(f)}"></div>`).join('')
  + `<div class="paper" style="left:190px;top:${top + 420}px;width:620px;transform:rotate(-2deg)"><img src="${img('nice-list-certificate.png')}"></div>`;
pins['bundle-A'] = `
  <div class="abs" style="inset:0;background:radial-gradient(circle at 50% 30%,#f2fbf5,#cfe9d9)"></div>
  <div class="band" style="top:0;height:300px;background:#2f7d4f;padding-top:45px"><h1 style="font-size:100px">Santa Mail Set</h1><div style="font-size:42px;margin-top:12px">5 MATCHING CHRISTMAS PRINTABLES</div></div>
  ${fan(380)}
  <div class="band" style="bottom:0;height:160px;background:#c1121f;padding-top:34px"><span class="cta">Letters · Wish List · Nice List · Elf</span></div>`;
pins['bundle-B'] = `
  <div class="abs" style="inset:0;background:repeating-linear-gradient(90deg,#c9a07a 0 140px,#bf946d 140px 143px,#cfa781 143px 280px)"></div>
  <div class="abs" style="left:0;right:0;top:50px;text-align:center"><div style="display:inline-block;background:#fffdf8;border-radius:40px;padding:30px 50px;box-shadow:0 12px 30px rgba(0,0,0,.2)">
    <div style="font-size:38px;color:#2f7d4f;font-weight:600">EASY CHRISTMAS TRADITION</div><h1 style="font-size:96px;color:#c1121f;margin-top:10px">North Pole Mail Kit</h1></div></div>
  ${fan(400)}
  <div class="abs" style="left:0;right:0;bottom:50px;text-align:center"><span class="cta" style="background:#c1121f;color:#fff">⚡ Instant Download</span></div>`;

(async () => {
  const b = await chromium.launch();
  const page = await b.newPage({ viewport: { width: 1000, height: 1500 } });
  for (const [n, body] of Object.entries(pins)) {
    await page.setContent(`<!doctype html><html><head><meta charset="utf-8">${FONTS}<style>${css}</style></head><body>${body}</body></html>`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(OUT, `pin-${n}.jpg`), type: 'jpeg', quality: 85 });
  }
  await b.close();
  console.log('pins', Object.keys(pins).length);
})();
