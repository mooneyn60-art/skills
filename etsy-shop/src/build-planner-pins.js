// Pinterest pins (1000x1500) for planner products + wall calendar.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const ROOT = path.join(__dirname, '..');
const img = f => 'data:image/png;base64,' + fs.readFileSync(path.join(ROOT, 'listing-images', 'previews', f)).toString('base64');
const FONTS = `<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&family=Jost:wght@300;400;500&display=block" rel="stylesheet">`;
const css = `*{margin:0;padding:0;box-sizing:border-box}body{width:1000px;height:1500px;overflow:hidden;font-family:Jost;color:#3d3d3a;position:relative}
.abs{position:absolute}.paper{position:absolute;background:#fff;box-shadow:0 20px 44px rgba(60,50,30,.22)}.paper img{width:100%;display:block}
h1{font-family:'Cormorant Garamond';font-weight:500;line-height:1}
.bg{position:absolute;inset:0;background:linear-gradient(160deg,#f5efe6,#e3e9de)}
.pill{display:inline-block;background:#8a9a82;color:#fff;border-radius:999px;padding:16px 42px;font-size:34px;letter-spacing:.05em}`;
const fan = (a, b, c, top) => `<div class="paper" style="left:30px;top:${top + 80}px;width:490px;transform:rotate(-7deg)"><img src="${img(a)}"></div>
  <div class="paper" style="left:480px;top:${top + 60}px;width:490px;transform:rotate(7deg)"><img src="${img(c)}"></div>
  <div class="paper" style="left:190px;top:${top}px;width:620px"><img src="${img(b)}"></div>`;
const pins = {
  'planner-A': `<div class="bg"></div><div class="abs" style="left:0;right:0;top:70px;text-align:center"><div style="font-size:30px;letter-spacing:.3em;color:#8a9a82">PRINTABLE · MINIMAL</div><h1 style="font-size:130px;margin-top:10px">2027 Planner</h1></div>
    ${fan('pl-02.png', 'pl-01.png', 'pl-04.png', 360)}<div class="abs" style="left:0;right:0;bottom:70px;text-align:center"><span class="pill">19 Pages · Instant Download</span></div>`,
  'planner-B': `<div class="bg"></div><div class="abs" style="left:0;right:0;top:70px;text-align:center"><h1 style="font-size:96px">Get Organized</h1><h1 style="font-size:96px;font-style:italic;color:#8a9a82">for 2027</h1></div>
    ${fan('pl-18.png', 'pl-03.png', 'pl-19.png', 420)}<div class="abs" style="left:0;right:0;bottom:70px;text-align:center"><span class="pill" style="background:#c97b5a">Goals · Weekly · Daily · Habits</span></div>`,
  'budget-A': `<div class="bg"></div><div class="abs" style="left:0;right:0;top:70px;text-align:center"><div style="font-size:30px;letter-spacing:.3em;color:#8a9a82">PRINTABLE</div><h1 style="font-size:124px;margin-top:10px">Budget Planner</h1></div>
    ${fan('bg-3.png', 'bg-1.png', 'bg-6.png', 360)}<div class="abs" style="left:0;right:0;bottom:70px;text-align:center"><span class="pill">9 Pages · Instant Download</span></div>`,
  'budget-B': `<div class="bg"></div><div class="abs" style="left:0;right:0;top:70px;text-align:center"><h1 style="font-size:92px">Take Control of</h1><h1 style="font-size:92px;font-style:italic;color:#8a9a82">Your Money in 2027</h1></div>
    ${fan('bg-4.png', 'bg-7.png', 'bg-9.png', 420)}<div class="abs" style="left:0;right:0;bottom:70px;text-align:center"><span class="pill" style="background:#c97b5a">Budget · Bills · Savings · Debt</span></div>`,
};
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1000, height: 1500 } });
  for (const [n, body] of Object.entries(pins)) {
    await p.setContent(`<!doctype html><html><head><meta charset="utf-8">${FONTS}<style>${css}</style></head><body>${body}</body></html>`, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(ROOT, 'pins', `pin-${n}.jpg`), type: 'jpeg', quality: 85 });
  }
  await b.close();
  console.log('ok');
})();
