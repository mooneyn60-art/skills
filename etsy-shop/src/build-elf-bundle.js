// Christmas Elf Letter Bundle: 4 matching elf letters (arrival, I'm back, goodbye, gentle reminder).
// Builds a 4-page PDF (US Letter + A4), Letter PNG previews (elfb-1..4.png) and 4 listing photos (2000x1500).
// Wording rule: "Christmas Elf" only (never the trademarked shelf-elf name).
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const A = require('./art');

const OUT = path.join(__dirname, '..', 'products');
const DIR = path.join(__dirname, '..', 'listing-images');
const PREV = path.join(DIR, 'previews');
fs.mkdirSync(OUT, { recursive: true });
fs.mkdirSync(PREV, { recursive: true });

const FONTS = `<link href="https://fonts.googleapis.com/css2?family=Mountains+of+Christmas:wght@700&family=Patrick+Hand&family=Fredoka:wght@400;500;600&display=block" rel="stylesheet">`;

// Same look as the Christmas Elf Arrival Letter in build-products.js (green candy-stripe frame).
const baseCss = `
  @page { margin: 0; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: 100%; }
  body { font-family: 'Patrick Hand', cursive; color: #2b2d42; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .page { position: relative; width: 100vw; height: 100vh; overflow: hidden; background: #fffdf8; padding: 4.2vh 5vw; break-after: page; page-break-after: always; }
  .page:last-child { break-after: auto; page-break-after: auto; }
  .frame { position: absolute; inset: 2.2vh 2.6vw; border-radius: 26px; border: 14px solid transparent;
    background: linear-gradient(#fffdf8,#fffdf8) padding-box,
      repeating-linear-gradient(45deg,#2f7d4f 0 16px,#fff 16px 32px) border-box; }
  .inner { position: relative; height: 100%; padding: 5vh 7vw; display: flex; flex-direction: column; }
  h1 { font-family: 'Mountains of Christmas', cursive; font-weight: 700; color: #c1121f; line-height: 1; }
  .kicker { font-family: Fredoka; letter-spacing: .3em; color: #2f7d4f; font-size: 2vh; }
  .line { border-bottom: 2.5px dashed #b9b9c6; height: 3.9vh; }
  .abs { position: absolute; }
  .box { background: #eef7f1; border-radius: 20px; padding: 1.5vh 2.5vw; font-size: 2.4vh; }
  .boxh { font-family: Fredoka; font-weight: 600; color: #2f7d4f; font-size: 2.6vh; letter-spacing: .1em; margin-bottom: .8vh; }
  .chk { display: flex; align-items: center; gap: 1.4vw; font-size: 2.6vh; margin-top: .6vh; }
  .chk i { display: inline-block; flex: none; width: 3.2vh; height: 3.2vh; border: 3px solid #2f7d4f; border-radius: 7px; background: #fff; }
  .brand { position: absolute; bottom: 3.4vh; left: 0; right: 0; text-align: center; font-family: Fredoka; font-size: 1.2vh; color: #9a9aa8; letter-spacing: .15em; }
`;

const BRAND = `<div class="brand">DOODLE DESIGN &amp; CO · PERSONAL USE ONLY</div>`;
const dear = `<div style="display:flex;gap:1vw;align-items:flex-end"><span>Dear</span><span class="line" style="flex:1"></span><span>,</span></div>`;
const sign = (text) => `<div style="font-size:2.6vh">${text}<br><span class="line" style="display:inline-block;width:30vw"></span><div style="font-size:1.7vh;color:#9a9aa8;font-family:Fredoka;letter-spacing:.1em">ELF'S NAME</div></div>`;

const letters = [
  // 1. Arrival (same design as the existing single listing)
  `<div class="page"><div class="frame"></div><div class="inner">
  <div style="display:flex;align-items:center;gap:2vw">
    ${A.elf(0.6)}
    <div><div class="kicker">SPECIAL DELIVERY</div>
    <h1 style="font-size:6.5vh">I'm Here from the North Pole!</h1></div>
  </div>
  <div style="font-size:2.5vh;line-height:1.45;margin-top:1.5vh">
    ${dear}
    <p style="margin-top:1.5vh">Hooray, I made it! Santa sent me all the way from the North Pole to be your Christmas Elf this season. My name is</p>
    <div class="line" style="width:60%"></div>
    <p style="margin-top:1.5vh">Every night I fly back to tell Santa all about your day, and every morning I'll be hiding somewhere new. Can you find me?</p>
  </div>
  <div class="box" style="margin-top:2.5vh">
    <div class="boxh">✨ ELF RULES ✨</div>
    <div>❄ Please don't touch me, or my Christmas magic might fade.</div>
    <div>❄ Talk to me anytime, I'll tell Santa everything!</div>
    <div>❄ Be kind, be helpful, and spread lots of Christmas cheer.</div>
    <div>❄ I'll fly home with Santa on Christmas Eve.</div>
  </div>
  <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:auto;margin-bottom:5vh">
    <div style="font-size:2.6vh">Your new best elf friend,<br><span class="line" style="display:inline-block;width:30vw"></span></div>
    <div style="display:flex;align-items:flex-end">${A.candycane(0.4)}${A.gift(0.5, '#e63946', '#f4c430')}</div>
  </div>
</div>${BRAND}</div>`,

  // 2. I'm Back
  `<div class="page"><div class="frame"></div><div class="inner">
  <div style="display:flex;align-items:center;gap:2vw">
    ${A.elf(0.6)}
    <div><div class="kicker">GUESS WHO MISSED YOU?</div>
    <h1 style="font-size:7.5vh;margin-top:1vh">I'm Back!</h1>
    <div style="font-family:Fredoka;font-size:2.2vh;color:#7a7a8c;margin-top:.6vh">Back for another magical year!</div></div>
  </div>
  <div style="font-size:2.5vh;line-height:1.45;margin-top:1.5vh">
    ${dear}
    <p style="margin-top:1.5vh">Surprise, it's me again! Your very own Christmas Elf is back for another magical season. Did you remember my name? It's</p>
    <div class="line" style="width:60%"></div>
    <p style="margin-top:1.5vh">I missed you SO much since last Christmas. Wow, look how much you've grown!</p>
  </div>
  <div class="box" style="margin-top:2vh">
    <div class="boxh">❄ MY YEAR AT THE NORTH POLE ❄</div>
    <div>★ I helped paint toys in Santa's workshop.</div>
    <div>★ I fed the reindeer carrots every morning.</div>
    <div>★ I practiced my best hiding spots, just for you!</div>
  </div>
  <div style="font-size:2.5vh;line-height:1.45;margin-top:2vh">
    <p>This year, I can't wait to see you</p>
    <div class="line"></div>
  </div>
  <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:auto;margin-bottom:5vh">
    ${sign('Hugs from your elf friend,')}
    <div style="display:flex;align-items:flex-end">${A.star(0.45)}${A.gift(0.5, '#2f7d4f', '#f4c430')}</div>
  </div>
</div>${BRAND}</div>`,

  // 3. Goodbye (Christmas Eve)
  `<div class="page"><div class="frame"></div><div class="inner">
  <div style="display:flex;align-items:center;gap:2vw">
    ${A.elf(0.6)}
    <div><div class="kicker">CHRISTMAS EVE</div>
    <h1 style="font-size:6.5vh">Time to Fly Home with Santa!</h1></div>
  </div>
  <div style="font-size:2.5vh;line-height:1.45;margin-top:1.5vh">
    ${dear}
    <p style="margin-top:1.5vh">Tonight is Christmas Eve, and it's time for me to fly home with Santa on his sleigh. Thank you for sharing your home and your heart with me this season. I had the BEST time with you!</p>
    <p style="margin-top:1.5vh">My favorite memory with you this year was</p>
    <div class="line"></div>
    <div class="line"></div>
  </div>
  <div class="box" style="margin-top:2.2vh">
    <div class="boxh">✨ UNTIL NEXT CHRISTMAS ✨</div>
    <div>❄ Keep being kind, brave and helpful.</div>
    <div>❄ Listen for sleigh bells tonight, that's me waving goodbye!</div>
    <div>❄ I'll be back next Christmas. I'll miss you lots!</div>
  </div>
  <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:auto;margin-bottom:5vh">
    ${sign('Love and hugs, your elf,')}
    <div style="display:flex;align-items:flex-end">${A.tree(0.42)}${A.gift(0.45)}</div>
  </div>
</div>${BRAND}</div>`,

  // 4. Gentle Reminder
  `<div class="page"><div class="frame"></div><div class="inner">
  <div style="display:flex;align-items:center;gap:2vw">
    ${A.elf(0.6)}
    <div><div class="kicker">A NOTE FROM YOUR ELF</div>
    <h1 style="font-size:5.6vh;white-space:nowrap">A Gentle Reminder</h1>
    <div style="font-family:Fredoka;font-size:2.2vh;color:#7a7a8c;margin-top:.6vh">Kind deeds make Christmas magic!</div></div>
  </div>
  <div style="font-size:2.5vh;line-height:1.45;margin-top:1.5vh">
    ${dear}
    <p style="margin-top:1.5vh">I have loved watching you this season! Christmas is getting close, and Santa's sleigh runs on kindness. Let's practice these together:</p>
  </div>
  <div class="box" style="margin-top:1.5vh;padding:1.2vh 2.5vw 1.6vh">
    <div class="chk"><i></i>Be kind to my brothers, sisters and friends</div>
    <div class="chk"><i></i>Help with chores around the house</div>
    <div class="chk"><i></i>Say please &amp; thank you</div>
    <div class="chk"><i></i>Listen the first time</div>
    <div class="chk"><i></i>Share and take turns</div>
    <div class="chk"><i></i>Use gentle hands and kind words</div>
  </div>
  <div style="font-size:2.5vh;line-height:1.45;margin-top:2vh">
    <p>Every time you tick a box, my Christmas magic sparkles a little brighter. I believe in you!</p>
  </div>
  <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:auto;margin-bottom:5vh">
    ${sign('Your cheering elf friend,')}
    <div style="display:flex;align-items:flex-end">${A.candycane(0.4)}${A.star(0.5)}</div>
  </div>
</div>${BRAND}</div>`,
];

const doc = (body, css) => `<!doctype html><html><head><meta charset="utf-8">${FONTS}<style>${css}</style></head><body>${body}</body></html>`;

// ---------- Listing photos ----------
const imgCss = `*{margin:0;padding:0;box-sizing:border-box}body{width:2000px;height:1500px;overflow:hidden;font-family:Fredoka}
.bg{position:absolute;inset:0;background:radial-gradient(circle at 30% 20%,#fff6ee,#f6e1d3 60%,#efcfbf)}
.wood{position:absolute;inset:0;background:repeating-linear-gradient(90deg,#c9a07a 0 180px,#bf946d 180px 184px,#cfa781 184px 360px)}
.paper{position:absolute;background:#fff;box-shadow:0 30px 60px rgba(60,30,10,.35),0 6px 14px rgba(60,30,10,.25)}
.paper img{width:100%;display:block}
h1{font-family:'Mountains of Christmas';color:#c1121f;line-height:1}
.pill{display:inline-block;background:#c1121f;color:#fff;border-radius:999px;padding:22px 60px;font-weight:600;font-size:58px;box-shadow:0 10px 30px rgba(0,0,0,.25)}
.chip{display:flex;align-items:center;gap:22px;background:#fff;border-radius:999px;padding:18px 40px;font-size:44px;color:#2b2d42;box-shadow:0 6px 18px rgba(60,30,10,.15);margin-top:22px}
.abs{position:absolute}
.cap{font-family:Fredoka;font-weight:600;font-size:40px;color:#2f7d4f;text-align:center;margin-top:18px}`;

function listingPages() {
  const img = n => 'data:image/png;base64,' + fs.readFileSync(path.join(PREV, `elfb-${n}.png`)).toString('base64');
  const names = ['Arrival', "I'm Back!", 'Goodbye', 'Gentle Reminder'];
  return {
    'elfbundle-01-thumbnail': `
      <div class="wood"></div>
      <div class="paper" style="left:60px;top:170px;width:680px;transform:rotate(-9deg)"><img src="${img(1)}"></div>
      <div class="paper" style="left:470px;top:100px;width:680px;transform:rotate(-3deg)"><img src="${img(2)}"></div>
      <div class="paper" style="left:860px;top:110px;width:680px;transform:rotate(3deg)"><img src="${img(4)}"></div>
      <div class="paper" style="left:1260px;top:170px;width:680px;transform:rotate(9deg)"><img src="${img(3)}"></div>
      <div class="abs" style="left:20px;top:1150px;transform:rotate(-8deg)">${A.gingerbread(1.2)}</div>
      <div class="abs" style="right:40px;top:1140px">${A.candycane(1.2)}</div>
      <div class="abs" style="left:0;right:0;bottom:60px;text-align:center"><span class="pill" style="background:#2f7d4f">4 Christmas Elf Letters · Printable</span></div>`,
    'elfbundle-02-included': `
      <div class="bg" style="background:radial-gradient(circle at 50% 30%,#f2fbf5,#d8efe1)"></div>
      <div class="paper" style="left:110px;top:170px;width:820px;transform:rotate(-2deg)"><img src="${img(1)}"></div>
      <div class="abs" style="left:1010px;top:110px;width:930px">
        <h1 style="font-size:116px;color:#2f7d4f">What's Included</h1>
        <div style="margin-top:26px">
          <div class="chip">🧝 Elf Arrival letter</div>
          <div class="chip">👋 "I'm Back!" letter</div>
          <div class="chip">🎄 Christmas Eve Goodbye letter</div>
          <div class="chip">✅ Gentle Reminder checklist</div>
          <div class="chip">📄 US Letter + A4 PDFs</div>
          <div class="chip">✍️ Fill in child &amp; elf names</div>
        </div>
        <div style="margin-top:44px"><span class="pill" style="font-size:44px;padding:18px 44px">⚡ INSTANT DOWNLOAD</span></div>
        <div style="font-size:32px;color:#7a7a8c;margin-top:24px">Digital file only. No physical item will be shipped.</div>
      </div>`,
    'elfbundle-03-pages': `
      <div class="bg"></div>
      <h1 class="abs" style="left:0;right:0;top:70px;text-align:center;font-size:120px">One Matching Set, All Season Long</h1>
      ${[1, 2, 3, 4].map((n, i) => `
      <div class="abs" style="left:${50 + i * 480}px;top:290px;width:460px">
        <div class="paper" style="position:relative;width:460px"><img src="${img(n)}"></div>
        <div class="cap">${i + 1}. ${names[i]}</div>
      </div>`).join('')}
      <div class="abs" style="left:0;right:0;bottom:70px;text-align:center;font-size:46px;color:#2b2d42">From the first morning to Christmas Eve 🎄</div>`,
    'elfbundle-04-goodbye': `
      <div class="wood"></div>
      <div class="paper" style="left:90px;top:-60px;width:1150px;transform:rotate(-3deg)"><img src="${img(3)}"></div>
      <div class="abs" style="left:1300px;top:260px;width:640px;background:#fffdf8;border-radius:40px;padding:56px 50px;box-shadow:0 20px 50px rgba(60,30,10,.3);text-align:center">
        <h1 style="font-size:96px">A Sweet Goodbye</h1>
        <div style="font-size:42px;color:#2b2d42;line-height:1.5;margin-top:30px">Your elf flies home with Santa on Christmas Eve, and leaves space for a favorite memory from this year.</div>
        <div style="margin-top:40px">${A.elf(1.1)}</div>
      </div>
      <div class="abs" style="left:0;right:0;bottom:50px;text-align:center"><span class="pill" style="background:#2f7d4f">Christmas Eve Goodbye Letter</span></div>`,
  };
}

(async () => {
  const browser = await chromium.launch();
  for (const fmt of ['Letter', 'A4']) {
    const [w, h] = fmt === 'Letter' ? [816, 1056] : [794, 1123];
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    await page.setContent(doc(letters.join(''), baseCss), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({ path: path.join(OUT, `elf-letter-bundle-${fmt}.pdf`), format: fmt, printBackground: true });
    if (fmt === 'Letter') {
      for (let i = 0; i < letters.length; i++) {
        await page.setContent(doc(letters[i], baseCss), { waitUntil: 'networkidle' });
        await page.evaluate(() => document.fonts.ready);
        await page.screenshot({ path: path.join(PREV, `elfb-${i + 1}.png`) });
      }
    }
    await page.close();
    console.log('built', fmt);
  }
  const page = await browser.newPage({ viewport: { width: 2000, height: 1500 } });
  for (const [name, body] of Object.entries(listingPages())) {
    await page.setContent(doc(body, imgCss), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(DIR, `${name}.jpg`), type: 'jpeg', quality: 86 });
  }
  await browser.close();
  console.log('done');
})();
