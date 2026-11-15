// Thumbnail + "What's included" photos for each product listing (2000x1500 JPEG).
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const A = require('./art');

const DIR = path.join(__dirname, '..', 'listing-images');
const img = f => 'data:image/png;base64,' + fs.readFileSync(path.join(DIR, 'previews', f)).toString('base64');
const FONTS = `<link href="https://fonts.googleapis.com/css2?family=Mountains+of+Christmas:wght@700&family=Fredoka:wght@400;500;600&display=block" rel="stylesheet">`;
const css = `*{margin:0;padding:0;box-sizing:border-box}body{width:2000px;height:1500px;overflow:hidden;font-family:Fredoka}
.bg{position:absolute;inset:0;background:radial-gradient(circle at 30% 20%,#fff6ee,#f6e1d3 60%,#efcfbf)}
.wood{position:absolute;inset:0;background:repeating-linear-gradient(90deg,#c9a07a 0 180px,#bf946d 180px 184px,#cfa781 184px 360px)}
.paper{position:absolute;background:#fff;box-shadow:0 30px 60px rgba(60,30,10,.35),0 6px 14px rgba(60,30,10,.25)}
.paper img{width:100%;display:block}
h1{font-family:'Mountains of Christmas';color:#c1121f;line-height:1}
.pill{display:inline-block;background:#c1121f;color:#fff;border-radius:999px;padding:22px 60px;font-weight:600;font-size:58px;box-shadow:0 10px 30px rgba(0,0,0,.25)}
.abs{position:absolute}`;

const products = [
  { slug: 'reply-from-santa-letter', label: 'Letter from Santa · Printable', landscape: false,
    items: ['🎅 Reply from Santa letter (PDF)', '📄 US Letter + A4 sizes', '✍️ Space for name & personal notes', '✅ Nice List checkbox', '🖨️ Print at home in minutes'] },
  { slug: 'nice-list-certificate', label: 'Nice List Certificate · Printable', landscape: true,
    items: ['🏅 Official Nice List Certificate (PDF)', '📄 US Letter + A4 (landscape)', '✍️ Fill in name & year', '⭐ Gold "Approved" seal design', '🖨️ Print at home in minutes'] },
  { slug: 'christmas-wish-list', label: 'Christmas Wish List · Printable', landscape: false,
    items: ['🎁 Kids Christmas Wish List (PDF)', '📄 US Letter + A4 sizes', '✍️ Name, age & 5 wishes', '🎨 "Draw your #1 wish" box', '🖨️ Print for every sibling'] },
  { slug: 'christmas-elf-arrival-letter', label: 'Elf Arrival Letter · Printable', landscape: false,
    items: ['🧝 Christmas Elf arrival letter (PDF)', '📄 US Letter + A4 sizes', '✍️ Fill in child & elf names', '📜 Fun Elf Rules included', '🖨️ Print at home in minutes'] },
];

const pages = {};
for (const p of products) {
  const w = p.landscape ? 1300 : 860;
  pages[`${p.slug}-01-thumbnail`] = `
    <div class="wood"></div>
    <div class="paper" style="left:${1000 - w / 2}px;top:${p.landscape ? 200 : 90}px;width:${w}px;transform:rotate(-3deg)"><img src="${img(p.slug + '.png')}"></div>
    <div class="abs" style="left:50px;top:900px;transform:rotate(-8deg)">${A.gingerbread(2.2)}</div>
    <div class="abs" style="left:90px;top:110px">${A.gift(2.4)}</div>
    <div class="abs" style="right:60px;top:720px">${A.candycane(2.8)}</div>
    <div class="abs" style="right:70px;top:110px">${A.holly(2.4)}</div>
    <div class="abs" style="left:0;right:0;bottom:60px;text-align:center"><span class="pill">${p.label}</span></div>`;
  pages[`${p.slug}-02-whats-included`] = `
    <div class="bg"></div>
    <div class="paper" style="left:${p.landscape ? 70 : 120}px;top:${p.landscape ? 330 : 150}px;width:${p.landscape ? 1000 : 840}px;transform:rotate(-2deg)"><img src="${img(p.slug + '.png')}"></div>
    <div class="abs" style="left:${p.landscape ? 1130 : 1060}px;top:170px;width:${p.landscape ? 820 : 880}px">
      <h1 style="font-size:120px">What's Included</h1>
      <div style="font-size:48px;color:#2b2d42;line-height:1.75;margin-top:40px">${p.items.join('<br>')}</div>
      <div style="margin-top:60px"><span class="pill" style="font-size:46px;padding:18px 44px">⚡ INSTANT DOWNLOAD</span></div>
      <div style="font-size:34px;color:#7a7a8c;margin-top:30px">Digital file only. No physical item will be shipped.</div>
    </div>`;
}
pages['bundle-01-thumbnail'] = `
  <div class="wood"></div>
  <div class="paper" style="left:120px;top:140px;width:560px;transform:rotate(-8deg)"><img src="${img('dear-santa.png')}"></div>
  <div class="paper" style="left:520px;top:100px;width:560px;transform:rotate(-2deg)"><img src="${img('reply-from-santa-letter.png')}"></div>
  <div class="paper" style="left:920px;top:110px;width:560px;transform:rotate(3deg)"><img src="${img('christmas-wish-list.png')}"></div>
  <div class="paper" style="left:1320px;top:150px;width:560px;transform:rotate(8deg)"><img src="${img('christmas-elf-arrival-letter.png')}"></div>
  <div class="paper" style="left:560px;top:760px;width:880px;transform:rotate(-1deg)"><img src="${img('nice-list-certificate.png')}"></div>
  <div class="abs" style="left:0;right:0;bottom:50px;text-align:center"><span class="pill" style="background:#2f7d4f">5-Piece Santa Mail Set · Printable</span></div>`;
pages['bundle-02-whats-included'] = `
  <div class="bg" style="background:radial-gradient(circle at 50% 30%,#f2fbf5,#d8efe1)"></div>
  <h1 class="abs" style="left:0;right:0;top:80px;text-align:center;font-size:140px;color:#2f7d4f">5 Printables in 1 Bundle</h1>
  <div class="abs" style="left:0;right:0;top:330px;text-align:center;font-size:58px;color:#2b2d42;line-height:1.75">
    ✉️ Dear Santa letter<br>🎅 Reply from Santa letter<br>🎁 Christmas Wish List<br>🏅 Nice List Certificate<br>🧝 Christmas Elf Arrival Letter</div>
  <div class="abs" style="left:0;right:0;bottom:120px;text-align:center"><span class="pill">⚡ INSTANT DOWNLOAD · SAVE vs. buying separately</span></div>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 2000, height: 1500 } });
  for (const [name, body] of Object.entries(pages)) {
    await page.setContent(`<!doctype html><html><head><meta charset="utf-8">${FONTS}<style>${css}</style></head><body>${body}</body></html>`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(DIR, `${name}.jpg`), type: 'jpeg', quality: 86 });
  }
  await browser.close();
  console.log('done', Object.keys(pages).length);
})();
