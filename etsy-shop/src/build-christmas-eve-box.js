// Christmas Eve Box Printable Pack: 5 pages (box lid labels, Magic Reindeer Food tags + recipe,
// Cookies/Milk/Carrots notes, Santa's Magic Key tags, Night Before checklist).
// Builds a 5-page PDF (US Letter + A4), Letter PNG previews (ceb-1..5.png) and 4 listing photos (2000x1500).
// Wording rules: no trademarked characters (say "the reindeer", never a named red-nosed one).
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

// ---------- Small original art for this pack ----------
const cookie = (s = 1) => `
<svg viewBox="0 0 100 100" width="${100 * s}" height="${100 * s}" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="44" fill="#d9a066" stroke="#b9824a" stroke-width="4"/>
  <circle cx="50" cy="50" r="36" fill="#e4b07a" opacity=".5"/>
  ${[[34, 32], [62, 28], [48, 52], [28, 60], [68, 58], [52, 74], [74, 42]].map(([x, y]) => `<ellipse cx="${x}" cy="${y}" rx="5" ry="4" fill="#5a3825"/>`).join('')}
</svg>`;

const milk = (s = 1) => `
<svg viewBox="0 0 80 120" width="${80 * s}" height="${120 * s}" xmlns="http://www.w3.org/2000/svg">
  <path d="M52 30 L64 2" stroke="#e63946" stroke-width="7" stroke-linecap="round"/>
  <path d="M55 23 L58 16 M60 12 L62 7" stroke="#fff" stroke-width="7" stroke-linecap="butt"/>
  <path d="M12 26 H68 L62 112 Q61 116 56 116 H24 Q19 116 18 112 Z" fill="#fff" stroke="#9cc9e6" stroke-width="4" stroke-linejoin="round"/>
  <path d="M15 46 H65 L61 110 Q60 113 56 113 H24 Q20 113 19 110 Z" fill="#f4f8fc"/>
  <path d="M15 46 Q28 40 40 46 Q52 52 65 46" stroke="#cfe3f2" stroke-width="3" fill="none"/>
  <path d="M26 58 V96" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".9"/>
</svg>`;

const carrot = (s = 1) => `
<svg viewBox="0 0 120 70" width="${120 * s}" height="${70 * s}" xmlns="http://www.w3.org/2000/svg">
  <path d="M96 22 Q112 6 116 14 Q108 22 100 28 Q118 26 116 36 Q104 36 96 34Z" fill="#2f7d4f"/>
  <path d="M98 26 Q90 14 6 56 Q2 60 8 60 Q92 46 100 36 Q104 30 98 26Z" fill="#f4845f"/>
  <path d="M40 40 l6 6 M60 32 l5 6 M78 28 l4 5 M24 50 l5 5" stroke="#d9663f" stroke-width="3" stroke-linecap="round"/>
</svg>`;

const key = (s = 1) => `
<svg viewBox="0 0 220 90" width="${220 * s}" height="${90 * s}" xmlns="http://www.w3.org/2000/svg">
  <path d="M74 38 H200 Q206 38 206 44 V46 Q206 52 200 52 H74Z" fill="#f4c430" stroke="#c99a10" stroke-width="3"/>
  <path d="M160 52 V74 H174 V64 H182 V74 H196 V52Z" fill="#f4c430" stroke="#c99a10" stroke-width="3" stroke-linejoin="round"/>
  <circle cx="44" cy="45" r="36" fill="#f4c430" stroke="#c99a10" stroke-width="3"/>
  <circle cx="44" cy="45" r="22" fill="#fffdf8" stroke="#c99a10" stroke-width="3"/>
  <path d="M44 31 l4.2 9 9.8 1 -7.4 6.6 2.2 9.6 -8.8 -5 -8.8 5 2.2 -9.6 -7.4 -6.6 9.8 -1z" fill="#e63946"/>
  <path d="M90 38 v14 M104 38 v14" stroke="#c99a10" stroke-width="3"/>
</svg>`;

const scissors = `<svg viewBox="0 0 24 24" width="2.2vh" height="2.2vh" style="vertical-align:middle"><g fill="none" stroke="#9a9aa8" stroke-width="2"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M8.5 7.5 L20 18 M8.5 16.5 L20 6"/></g></svg>`;

// ---------- Print pages ----------
const STRIPE = `repeating-linear-gradient(45deg,#c1121f 0 12px,#fff 12px 20px,#2f7d4f 20px 32px,#fff 32px 40px)`;
const baseCss = `
  @page { margin: 0; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: 100%; }
  body { font-family: 'Patrick Hand', cursive; color: #2b2d42; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .page { position: relative; width: 100vw; height: 100vh; overflow: hidden; background: #fffdf8; padding: 3.4vh 4.5vw 6.2vh; display: flex; flex-direction: column; break-after: page; page-break-after: always; }
  .page:last-child { break-after: auto; page-break-after: auto; }
  h1, .xm { font-family: 'Mountains of Christmas', cursive; font-weight: 700; color: #c1121f; line-height: 1; }
  .kicker { font-family: Fredoka; font-weight: 500; letter-spacing: .3em; color: #2f7d4f; font-size: 1.7vh; }
  .phead { text-align: center; margin-bottom: 1.6vh; }
  .phead h1 { font-size: 4.6vh; }
  .phead .sub { font-family: Fredoka; font-size: 1.5vh; color: #7a7a8c; margin-top: .5vh; }
  .grid { flex: 1; min-height: 0; display: grid; border: 2px dashed #b9b9c6; }
  .cell { position: relative; padding: 1.4vh 1.4vw; border-right: 2px dashed #b9b9c6; border-bottom: 2px dashed #b9b9c6; min-height: 0; min-width: 0; }
  .card { position: relative; height: 100%; border-radius: 18px; border: 10px solid transparent; overflow: hidden;
    background: linear-gradient(#fffdf8,#fffdf8) padding-box, ${STRIPE} border-box; }
  .card.green { background: linear-gradient(#fffdf8,#fffdf8) padding-box, repeating-linear-gradient(45deg,#2f7d4f 0 12px,#fff 12px 24px) border-box; }
  .card.red { background: linear-gradient(#fffdf8,#fffdf8) padding-box, repeating-linear-gradient(45deg,#c1121f 0 12px,#fff 12px 24px) border-box; }
  .ci { height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 1vh 1.6vw; }
  .line { border-bottom: 2.5px dashed #b9b9c6; display: inline-block; }
  .hole { position: absolute; top: 1vh; left: 1vw; width: 2.2vh; height: 2.2vh; border-radius: 50%; border: 2px solid #b9b9c6; background: #fff; }
  .snip { position: absolute; top: 1.1vh; right: 4.5vw; }
  .abs { position: absolute; }
  .brand { position: absolute; bottom: 2.6vh; left: 0; right: 0; text-align: center; font-family: Fredoka; font-size: 1.2vh; color: #9a9aa8; letter-spacing: .15em; }
  .chk { display: flex; align-items: center; gap: 2vw; font-size: 2.8vh; background: #fff; border-radius: 16px; padding: .7vh 2vw; height: 5.4vh; box-shadow: 0 0 0 2px #eef0f3; }
  .chk i { display: inline-block; flex: none; width: 3.6vh; height: 3.6vh; border: 3.5px solid #2f7d4f; border-radius: 9px; background: #fff; }
  .chk .ic { margin-left: auto; display: flex; align-items: center; }
`;

const BRAND = `<div class="brand">DOODLE DESIGN &amp; CO · PERSONAL USE ONLY</div>`;
const SNIP = `<div class="snip">${scissors}</div>`;

// 1. Christmas Eve Box lid labels (2 per page)
const lidLabel = (flip) => `
  <div class="cell" style="padding:1.6vh 2vw"><div class="card"><div class="ci" style="padding:1.5vh 3vw">
    <div style="display:flex;align-items:center;justify-content:center;gap:3vw;width:100%">
      <div style="flex:none">${flip ? A.reindeer(0.62) : A.santa(0.6)}</div>
      <div style="flex:1;min-width:0">
        <div class="kicker" style="font-size:2vh">✦ SPECIAL DELIVERY ✦</div>
        <h1 style="font-size:7.8vw;margin-top:.8vh;white-space:nowrap">Christmas Eve Box</h1>
        <div style="display:flex;align-items:flex-end;gap:1vw;font-size:3.6vh;margin-top:2.2vh">
          <span style="white-space:nowrap">Special Delivery for</span><span class="line" style="flex:1;height:4vh"></span>
        </div>
        <div style="font-family:Fredoka;font-size:1.85vw;color:#7a7a8c;letter-spacing:.1em;margin-top:2vh;white-space:nowrap">FROM THE NORTH POLE · OPEN ON CHRISTMAS EVE</div>
      </div>
    </div>
    <div style="display:flex;align-items:flex-end;gap:1.5vw;margin-top:1.6vh">${A.holly(0.55)}${A.star(0.35)}${A.gift(0.42, '#2f7d4f', '#e63946')}${A.candycane(0.3)}${A.gift(0.42, '#c1121f', '#f4c430')}${A.star(0.35)}${A.holly(0.55)}</div>
  </div></div></div>`;

const page1 = `<div class="page">
  <div class="phead"><h1>Christmas Eve Box Labels</h1><div class="sub">Cut along the dashed lines and tape to the box lid · 2 per page</div></div>
  <div class="grid" style="grid-template-rows:1fr 1fr">${lidLabel(false)}${lidLabel(true)}</div>
  ${SNIP}${BRAND}</div>`;

// 2. Magic Reindeer Food recipe + 6 tags
const foodTag = (i) => `
  <div class="cell"><div class="card ${i % 2 ? 'red' : 'green'}"><div class="ci" style="padding-left:4.2vw">
    <div class="hole" style="top:50%;left:.9vw;transform:translateY(-50%)"></div>
    <div style="display:flex;align-items:center;gap:1vw">
      ${A.reindeer(0.34)}
      <div style="text-align:left"><div class="kicker" style="font-size:1.25vh;letter-spacing:.2em">CHRISTMAS EVE</div>
      <h1 style="font-size:3.3vw;white-space:nowrap">Magic Reindeer Food</h1></div>
    </div>
    <div style="font-size:1.85vh;line-height:1.3;margin-top:.8vh">Sprinkle on the lawn tonight so the reindeer find your house!</div>
  </div></div></div>`;

const page2 = `<div class="page">
  <div class="phead" style="margin-bottom:1.2vh"><h1>Magic Reindeer Food</h1><div class="sub">1 recipe card + 6 bag tags · cut along the dashed lines, punch a hole and tie to a treat bag</div></div>
  <div class="card green" style="height:auto;flex:none;margin-bottom:1.6vh;border-width:9px">
    <div style="display:flex;align-items:center;gap:2.4vw;padding:1.3vh 2.4vw">
      <div style="flex:none">${A.reindeer(0.5)}</div>
      <div style="flex:1;min-width:0">
        <div class="kicker" style="font-size:1.5vh">RECIPE CARD</div>
        <div class="xm" style="font-size:3.6vh">How to Make Magic Reindeer Food</div>
        <div style="display:flex;gap:2.4vw;margin-top:.7vh;font-size:1.9vh;line-height:1.35">
          <div style="flex:1"><b style="font-family:Fredoka;font-weight:600;color:#2f7d4f">YOU NEED</b><br>❄ 1 cup rolled oats<br>❄ 2 tbsp colored sugar sprinkles<br>❄ A pinch of Christmas magic!</div>
          <div style="flex:1.25"><b style="font-family:Fredoka;font-weight:600;color:#2f7d4f">HOW TO</b><br>1. Mix it all in a bowl.<br>2. Spoon into small bags and add a tag.<br>3. On Christmas Eve, sprinkle on the lawn so the reindeer find your house!</div>
        </div>
        <div style="font-family:Fredoka;font-size:1.3vh;color:#7a7a8c;margin-top:.6vh">Please skip glitter: it isn't safe for birds and animals.</div>
      </div>
    </div>
  </div>
  <div class="grid" style="grid-template-columns:1fr 1fr;grid-template-rows:repeat(3,1fr)">${[0, 1, 2, 3, 4, 5].map(foodTag).join('')}</div>
  ${BRAND}</div>`;

// 3. Cookies for Santa plate note + Milk for Santa + Carrots for the Reindeer
const smallTag = (title, kick, art, msg, cls) => `
  <div class="cell"><div class="card ${cls}"><div class="ci">
    <div style="display:flex;align-items:center;gap:1.2vw">${art}
      <div style="text-align:left"><div class="kicker" style="font-size:1.25vh;letter-spacing:.2em">${kick}</div><h1 style="font-size:3.6vh">${title}</h1></div></div>
    <div style="font-size:1.85vh;margin-top:.8vh;line-height:1.3">${msg}</div>
  </div></div></div>`;

const page3 = `<div class="page">
  <div class="phead"><h1>Treats for Santa &amp; the Reindeer</h1><div class="sub">Plate note + mini tags · cut along the dashed lines</div></div>
  <div class="grid" style="grid-template-columns:1fr 1fr;grid-template-rows:1.55fr 1fr 1fr">
    <div class="cell" style="grid-column:1 / span 2"><div class="card"><div class="ci" style="padding:1.2vh 3vw">
      <div style="display:flex;align-items:center;gap:3vw;width:100%">
        <div style="flex:none;display:flex;flex-direction:column;align-items:center">${A.santa(0.5)}</div>
        <div style="flex:1;min-width:0">
          <div class="kicker" style="font-size:1.8vh">✦ ON THE PLATE ✦</div>
          <h1 style="font-size:7vw;margin-top:.4vh;white-space:nowrap">Cookies for Santa</h1>
          <div style="font-size:2.3vh;line-height:1.4;margin-top:1vh;text-align:left">Dear Santa, we baked these cookies just for you. Thank you for all your hard work tonight!</div>
          <div style="display:flex;align-items:flex-end;gap:1vw;font-size:2.4vh;margin-top:1.4vh"><span>Love from</span><span class="line" style="flex:1;height:3vh"></span></div>
        </div>
        <div style="flex:none;display:flex;flex-direction:column;align-items:center;gap:.6vh">${cookie(0.62)}${cookie(0.48)}</div>
      </div>
    </div></div></div>
    ${smallTag('Milk for Santa', 'A COLD GLASS', milk(0.5), 'A cold glass of milk to wash down your cookies!', 'red')}
    ${smallTag('Milk for Santa', 'A COLD GLASS', milk(0.5), 'A cold glass of milk to wash down your cookies!', 'red')}
    ${smallTag('Carrots for the Reindeer', 'CRUNCHY SNACK', carrot(0.6), 'A crunchy snack to keep the reindeer flying all night!', 'green')}
    ${smallTag('Carrots for the Reindeer', 'CRUNCHY SNACK', carrot(0.6), 'A crunchy snack to keep the reindeer flying all night!', 'green')}
  </div>
  ${SNIP}${BRAND}</div>`;

// 4. Santa's Magic Key tags (4 per page)
const keyTag = (i) => `
  <div class="cell"><div class="card ${i === 1 || i === 2 ? 'green' : 'red'}"><div class="ci">
    <div class="hole"></div>
    <div class="kicker" style="font-size:1.3vh;letter-spacing:.14em;white-space:nowrap">NO CHIMNEY? NO PROBLEM!</div>
    <h1 style="font-size:4.6vw;margin-top:.6vh;white-space:nowrap">Santa's Magic Key</h1>
    <div style="margin-top:1.2vh">${key(0.62)}</div>
    <div style="font-size:2vh;line-height:1.35;margin-top:1vh">Dear Santa, we don't have a chimney, so please use this magic key to come inside. It only works on Christmas Eve!</div>
    <div style="display:flex;align-items:flex-end;gap:.8vw;font-size:2vh;margin-top:1.4vh;width:90%"><span style="white-space:nowrap">The</span><span class="line" style="flex:1;height:2.6vh"></span><span>family</span></div>
    <div style="display:flex;gap:.8vw;margin-top:1.2vh">${A.star(0.2)}${A.snowflake(0.2)}${A.star(0.2)}</div>
  </div></div></div>`;

const page4 = `<div class="page">
  <div class="phead"><h1>Santa's Magic Key</h1><div class="sub">4 tags · cut out, punch a hole and tie a ribbon to a real or play key · hang it on the front door</div></div>
  <div class="grid" style="grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr">${[0, 1, 2, 3].map(keyTag).join('')}</div>
  ${SNIP}${BRAND}</div>`;

// 5. Night Before checklist (full page, candy-stripe frame)
const items = [
  ['Cookies out for Santa', cookie(0.42)],
  ['Milk poured for Santa', milk(0.34)],
  ['Carrots out for the reindeer', carrot(0.42)],
  ['Reindeer food sprinkled', A.reindeer(0.26)],
  ['Stockings hung', A.candycane(0.24)],
  ['Pajamas on', A.star(0.38)],
  ['Teeth brushed &amp; a Christmas story', A.tree(0.2)],
  ['Asleep early!', A.snowflake(0.38)],
];
const page5 = `<div class="page" style="padding:2.2vh 2.6vw 5.6vh">
  <div class="card" style="border-width:14px;border-radius:26px">
    <div style="height:100%;padding:3vh 6vw 3vh;display:flex;flex-direction:column">
      <div style="display:flex;align-items:center;gap:2.5vw">
        ${A.santa(0.46)}
        <div><div class="kicker">CHRISTMAS EVE</div>
        <h1 style="font-size:5.6vw;margin-top:.6vh;white-space:nowrap">The Night Before Checklist</h1>
        <div style="font-family:Fredoka;font-size:2vh;color:#7a7a8c;margin-top:.8vh">Tick each box before Santa comes!</div></div>
      </div>
      <div style="display:flex;align-items:flex-end;gap:1vw;font-size:2.8vh;margin-top:2vh"><span>My name:</span><span class="line" style="flex:1;height:3.4vh"></span></div>
      <div style="display:flex;flex-direction:column;gap:1vh;margin-top:1.8vh">
        ${items.map(([t, art]) => `<div class="chk"><i></i><span>${t}</span><span class="ic">${art}</span></div>`).join('')}
      </div>
      <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:auto">
        <div style="font-size:2.6vh;line-height:1.4">All done? Shhh... listen<br>for sleigh bells!</div>
        <div style="display:flex;align-items:flex-end;gap:.6vw">${A.gift(0.48, '#2f7d4f', '#e63946')}${A.tree(0.42)}${A.gift(0.4, '#c1121f', '#f4c430')}</div>
      </div>
    </div>
  </div>
  ${BRAND}</div>`;

const pages = [page1, page2, page3, page4, page5];
const doc = (body, css) => `<!doctype html><html><head><meta charset="utf-8">${FONTS}<style>${css}</style></head><body>${body}</body></html>`;

// ---------- Listing photos ----------
const imgCss = `*{margin:0;padding:0;box-sizing:border-box}body{width:2000px;height:1500px;overflow:hidden;font-family:Fredoka}
.bg{position:absolute;inset:0;background:radial-gradient(circle at 30% 20%,#fff6ee,#f6e1d3 60%,#efcfbf)}
.wood{position:absolute;inset:0;background:repeating-linear-gradient(90deg,#c9a07a 0 180px,#bf946d 180px 184px,#cfa781 184px 360px)}
.paper{position:absolute;background:#fff;box-shadow:0 30px 60px rgba(60,30,10,.35),0 6px 14px rgba(60,30,10,.25)}
.paper img{width:100%;display:block}
h1{font-family:'Mountains of Christmas';color:#c1121f;line-height:1}
.pill{display:inline-block;background:#c1121f;color:#fff;border-radius:999px;padding:22px 60px;font-weight:600;font-size:58px;box-shadow:0 10px 30px rgba(0,0,0,.25)}
.chip{display:flex;align-items:center;gap:22px;background:#fff;border-radius:999px;padding:16px 40px;font-size:42px;color:#2b2d42;box-shadow:0 6px 18px rgba(60,30,10,.15);margin-top:20px}
.abs{position:absolute}
.cap{font-family:Fredoka;font-weight:600;font-size:34px;color:#2f7d4f;text-align:center;margin-top:16px}`;

function listingPages() {
  const img = n => 'data:image/png;base64,' + fs.readFileSync(path.join(PREV, `ceb-${n}.png`)).toString('base64');
  const names = ['Box Labels', 'Reindeer Food', 'Treat Notes', 'Magic Key', 'Checklist'];
  return {
    'cebox-01-thumbnail': `
      <div class="wood"></div>
      <div class="paper" style="left:30px;top:200px;width:620px;transform:rotate(-11deg)"><img src="${img(2)}"></div>
      <div class="paper" style="left:350px;top:120px;width:620px;transform:rotate(-5deg)"><img src="${img(3)}"></div>
      <div class="paper" style="left:1030px;top:120px;width:620px;transform:rotate(5deg)"><img src="${img(4)}"></div>
      <div class="paper" style="left:1350px;top:200px;width:620px;transform:rotate(11deg)"><img src="${img(5)}"></div>
      <div class="paper" style="left:690px;top:70px;width:620px;transform:rotate(0deg)"><img src="${img(1)}"></div>
      <div class="abs" style="left:0;right:0;bottom:60px;text-align:center"><span class="pill">Christmas Eve Box Printables · 5 Pages</span></div>`,
    'cebox-02-included': `
      <div class="bg" style="background:radial-gradient(circle at 50% 30%,#f2fbf5,#d8efe1)"></div>
      <div class="paper" style="left:110px;top:170px;width:820px;transform:rotate(-2deg)"><img src="${img(1)}"></div>
      <div class="abs" style="left:1000px;top:90px;width:950px">
        <h1 style="font-size:116px;color:#2f7d4f">What's Included</h1>
        <div style="margin-top:20px">
          <div class="chip">🎁 Christmas Eve Box lid labels (2)</div>
          <div class="chip">🦌 Reindeer Food tags (6) + recipe</div>
          <div class="chip">🍪 Cookies, milk &amp; carrot notes</div>
          <div class="chip">🔑 Santa's Magic Key tags (4)</div>
          <div class="chip">✅ Night Before checklist</div>
          <div class="chip">📄 US Letter + A4 PDFs</div>
        </div>
        <div style="margin-top:40px"><span class="pill" style="font-size:44px;padding:18px 44px">⚡ INSTANT DOWNLOAD</span></div>
        <div style="font-size:32px;color:#7a7a8c;margin-top:22px">Digital file only. No physical item will be shipped.</div>
      </div>`,
    'cebox-03-pages': `
      <div class="bg"></div>
      <h1 class="abs" style="left:0;right:0;top:70px;text-align:center;font-size:116px">Everything for a Magical Christmas Eve</h1>
      ${[1, 2, 3, 4, 5].map((n, i) => `
      <div class="abs" style="left:${40 + i * 388}px;top:400px;width:370px">
        <div class="paper" style="position:relative;width:370px"><img src="${img(n)}"></div>
        <div class="cap">${i + 1}. ${names[i]}</div>
      </div>`).join('')}
      <div class="abs" style="left:0;right:0;bottom:250px;text-align:center;font-size:50px;color:#2b2d42">Print at home tonight, fill the box, and watch the magic 🎄</div>`,
    'cebox-04-reindeer-food': `
      <div class="wood"></div>
      <div class="paper" style="left:90px;top:-170px;width:1150px;transform:rotate(-3deg)"><img src="${img(2)}"></div>
      <div class="abs" style="left:1300px;top:230px;width:640px;background:#fffdf8;border-radius:40px;padding:56px 50px;box-shadow:0 20px 50px rgba(60,30,10,.3);text-align:center">
        <h1 style="font-size:96px">Magic Reindeer Food</h1>
        <div style="font-size:40px;color:#2b2d42;line-height:1.5;margin-top:30px">Easy oat recipe card plus 6 cute bag tags. Sprinkle on the lawn so the reindeer find your house!</div>
        <div style="margin-top:34px">${A.reindeer(1.2)}</div>
      </div>
      <div class="abs" style="left:1300px;width:640px;top:1230px;text-align:center"><span class="pill" style="background:#2f7d4f;font-size:42px;padding:18px 40px">Recipe + 6 Tags</span></div>`,
  };
}

(async () => {
  const browser = await chromium.launch();
  const checkDir = process.env.CEB_CHECK_DIR; // optional: also save A4 page renders for checking
  for (const fmt of ['Letter', 'A4']) {
    const [w, h] = fmt === 'Letter' ? [816, 1056] : [794, 1123];
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
    await page.setContent(doc(pages.join(''), baseCss), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({ path: path.join(OUT, `christmas-eve-box-pack-${fmt}.pdf`), format: fmt, printBackground: true });
    if (fmt === 'Letter' || checkDir) {
      for (let i = 0; i < pages.length; i++) {
        await page.setContent(doc(pages[i], baseCss), { waitUntil: 'networkidle' });
        await page.evaluate(() => document.fonts.ready);
        const file = fmt === 'Letter' ? path.join(PREV, `ceb-${i + 1}.png`) : path.join(checkDir, `ceb-A4-${i + 1}.png`);
        await page.screenshot({ path: file });
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
