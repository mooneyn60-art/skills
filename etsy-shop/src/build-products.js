// Builds the printable products as PDFs (US Letter + A4) and PNG previews.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const A = require('./art');

const OUT = path.join(__dirname, '..', 'products');
const PREV = path.join(__dirname, '..', 'listing-images', 'previews');
fs.mkdirSync(PREV, { recursive: true });

const FONTS = `<link href="https://fonts.googleapis.com/css2?family=Mountains+of+Christmas:wght@700&family=Patrick+Hand&family=Fredoka:wght@500;600&display=block" rel="stylesheet">`;

const baseCss = (landscape) => `
  @page { margin: 0; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: 100%; height: 100%; }
  body { font-family: 'Patrick Hand', cursive; color: #2b2d42; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .page { position: relative; width: 100vw; height: 100vh; overflow: hidden; background: #fffdf8; padding: 4.2vh 5vw; }
  .frame { position: absolute; inset: 2.2vh 2.6vw; border-radius: 26px;
    border: 14px solid transparent;
    background: linear-gradient(#fffdf8,#fffdf8) padding-box,
      repeating-linear-gradient(45deg,#e63946 0 16px,#fff 16px 32px) border-box; }
  .frame.green { background: linear-gradient(#fffdf8,#fffdf8) padding-box,
      repeating-linear-gradient(45deg,#2f7d4f 0 16px,#fff 16px 32px) border-box; }
  .inner { position: relative; height: 100%; padding: ${landscape ? '5vh 7vw' : '5vh 7vw'}; display: flex; flex-direction: column; }
  h1 { font-family: 'Mountains of Christmas', cursive; font-weight: 700; color: #c1121f; line-height: 1; }
  .line { border-bottom: 2.5px dashed #b9b9c6; height: 3.9vh; }
  .lbl { font-size: 3.2vh; }
  .abs { position: absolute; }
  .brand { position: absolute; bottom: 3.4vh; left: 0; right: 0; text-align: center; font-family: Fredoka; font-size: 1.2vh; color: #9a9aa8; letter-spacing: .15em; }
`;

const products = [
  {
    slug: 'reply-from-santa-letter',
    title: 'Reply from Santa',
    html: `
<div class="page"><div class="frame"></div><div class="inner">
  <div style="display:flex;align-items:center;gap:2vw;margin-top:1vh">
    <div>${A.santa(0.7)}</div>
    <div style="flex:1">
      <div style="font-family:Fredoka;font-size:1.8vh;letter-spacing:.3em;color:#2f7d4f">FROM THE DESK OF</div>
      <h1 style="font-size:7vh">Santa Claus</h1>
      <div style="font-family:Fredoka;font-size:2vh;color:#7a7a8c">123 Candy Cane Lane · North Pole · Est. Long Ago</div>
    </div>
    <div class="abs" style="right:1vw;top:-2vh;transform:rotate(12deg);border:4px solid #c1121f;color:#c1121f;border-radius:50%;width:11vh;height:11vh;display:flex;align-items:center;justify-content:center;text-align:center;font-family:Fredoka;font-weight:600;font-size:1.35vh;line-height:1.2">NORTH POLE<br>★ ★ ★<br>OFFICIAL<br>MAIL</div>
  </div>
  <div style="font-size:2.5vh;line-height:1.45;margin-top:1.5vh">
    <div style="display:flex;gap:1vw;align-items:flex-end"><span>Dear</span><span class="line" style="flex:1"></span><span>,</span></div>
    <p style="margin-top:2vh">Ho, ho, ho! Thank you so much for your wonderful letter. The elves and I read it by the fireplace with a big mug of cocoa. I am so proud of you this year, especially for</p>
    <div class="line"></div>
    <p style="margin-top:1.5vh">Mrs. Claus says you have been extra kind, and the reindeer are practicing their flying so we can visit your home on Christmas Eve. Please remember to</p>
    <div class="line"></div>
    <p style="margin-top:1.5vh">Keep being the amazing kid you are. See you soon!</p>
  </div>
  <div style="display:flex;align-items:flex-end;justify-content:space-between;margin-top:auto;margin-bottom:5vh">
    <div style="font-size:2.6vh">
      With love and twinkles,<br>
      <span style="font-family:'Mountains of Christmas';font-size:5.5vh;color:#c1121f">Santa Claus</span>
      <div style="display:flex;gap:2vw;margin-top:1vh;font-size:2.8vh">
        <span><span style="display:inline-block;width:3vh;height:3vh;border:3px solid #2f7d4f;border-radius:6px;vertical-align:middle;position:relative"><span style="position:absolute;left:.4vh;top:-1.6vh;color:#2f7d4f;font-size:4vh">✓</span></span> Nice List</span>
        <span><span style="display:inline-block;width:3vh;height:3vh;border:3px solid #c1121f;border-radius:6px;vertical-align:middle"></span> Naughty List</span>
      </div>
    </div>
    <div style="display:flex;align-items:flex-end">${A.reindeer(0.55)}${A.gift(0.45)}</div>
  </div>
  <div class="abs" style="left:3vw;top:30vh;opacity:.5">${A.snowflake(0.35)}</div>
  <div class="abs" style="right:3vw;top:44vh;opacity:.5">${A.snowflake(0.28)}</div>
</div><div class="brand">DOODLE DESIGN &amp; CO · PERSONAL USE ONLY</div></div>`,
  },
  {
    slug: 'nice-list-certificate',
    title: 'Nice List Certificate',
    landscape: true,
    html: `
<div class="page"><div class="frame green"></div><div class="inner" style="align-items:center;text-align:center;justify-content:center">
  <div class="abs" style="left:2vw;top:2vh">${A.holly(0.9)}</div>
  <div class="abs" style="right:2vw;top:2vh;transform:scaleX(-1)">${A.holly(0.9)}</div>
  <div style="font-family:Fredoka;letter-spacing:.4em;color:#2f7d4f;font-size:2.4vh">★ OFFICIAL NORTH POLE DOCUMENT ★</div>
  <h1 style="font-size:12vh;margin-top:1vh">Nice List Certificate</h1>
  <div style="font-size:3.6vh;margin-top:2vh">This certifies that</div>
  <div class="line" style="width:55vw;height:9vh;margin:0 auto"></div>
  <div style="font-size:3.6vh;margin-top:2.5vh;max-width:62vw">has been officially added to <b style="color:#c1121f">Santa's Nice List</b> for being kind, helpful, and full of Christmas cheer in the year</div>
  <div class="line" style="width:14vw;height:6vh;margin:0 auto"></div>
  <div style="display:flex;justify-content:space-between;align-items:flex-end;width:78vw;margin-top:3vh">
    <div style="text-align:center"><div style="font-family:'Mountains of Christmas';font-size:6vh;color:#c1121f">Santa Claus</div><div style="border-top:2.5px solid #2b2d42;width:22vw;font-size:2.4vh;padding-top:.5vh">Santa Claus</div></div>
    <div style="position:relative;width:20vh;height:20vh">
      <svg viewBox="0 0 100 100" width="100%" height="100%"><g fill="#f4c430" stroke="#c99a10" stroke-width="1.5">${Array.from({length:24},(_,i)=>`<circle cx="${50+44*Math.cos(i*Math.PI/12)}" cy="${50+44*Math.sin(i*Math.PI/12)}" r="7"/>`).join('')}<circle cx="50" cy="50" r="42"/></g><circle cx="50" cy="50" r="33" fill="none" stroke="#c99a10" stroke-width="1.5" stroke-dasharray="3 3"/></svg>
      <div class="abs" style="inset:0;display:flex;align-items:center;justify-content:center;font-family:Fredoka;font-weight:600;color:#7a5200;font-size:2vh;line-height:1.1">NICE<br>LIST<br>★ APPROVED ★</div>
    </div>
    <div style="text-align:center"><div style="font-family:'Mountains of Christmas';font-size:6vh;color:#2f7d4f">Jingle</div><div style="border-top:2.5px solid #2b2d42;width:22vw;font-size:2.4vh;padding-top:.5vh">Head Elf</div></div>
  </div>
  <div class="abs" style="left:3vw;bottom:5vh">${A.gingerbread(0.6)}</div>
  <div class="abs" style="right:3vw;bottom:4vh">${A.candycane(0.6)}</div>
</div><div class="brand">DOODLE DESIGN &amp; CO · PERSONAL USE ONLY</div></div>`,
  },
  {
    slug: 'christmas-wish-list',
    title: 'Christmas Wish List',
    html: `
<div class="page"><div class="frame"></div><div class="inner">
  <div style="text-align:center;margin-top:1vh">
    <div style="font-family:Fredoka;letter-spacing:.35em;color:#2f7d4f;font-size:2vh">MY VERY OWN</div>
    <h1 style="font-size:8vh">Christmas Wish List</h1>
  </div>
  <div class="abs" style="left:2vw;top:1vh">${A.star(0.6)}</div>
  <div class="abs" style="right:2vw;top:1vh">${A.star(0.6)}</div>
  <div class="abs" style="right:1vw;bottom:4vh;display:flex;align-items:flex-end">${A.snowman(0.4)}${A.tree(0.45)}</div>
  <div style="display:flex;gap:3vw;margin-top:2vh;font-size:3vh">
    <div style="flex:2;display:flex;gap:1vw;align-items:flex-end">Name: <span class="line" style="flex:1"></span></div>
    <div style="flex:1;display:flex;gap:1vw;align-items:flex-end">Age: <span class="line" style="flex:1"></span></div>
  </div>
  <div style="margin-top:2.5vh;font-size:3vh;color:#c1121f">Dear Santa, here are the things I am wishing for:</div>
  ${Array.from({ length: 5 }, (_, i) => `
  <div style="display:flex;align-items:flex-end;gap:1.5vw;margin-top:1vh">
    <span style="width:4.6vh;height:4.6vh;flex:none">${i % 2 ? A.gift(0.36, '#e63946', '#2f7d4f') : A.gift(0.36)}</span>
    <span class="line" style="flex:1"></span>
  </div>`).join('')}
  <div style="display:flex;gap:3vw;margin-top:2vh;height:19vh">
    <div style="flex:1;border:3px dashed #2f7d4f;border-radius:18px;padding:1.5vh 1.5vw;font-size:2.6vh;color:#2f7d4f">Draw your #1 wish here!</div>
    <div style="flex:1;font-size:2.8vh;display:flex;flex-direction:column;gap:1.2vh">
      <div>Something nice I did this year:</div><div class="line"></div><div class="line"></div>
      
    </div>
  </div>
</div><div class="brand">DOODLE DESIGN &amp; CO · PERSONAL USE ONLY</div></div>`,
  },
  {
    slug: 'christmas-elf-arrival-letter',
    title: 'Christmas Elf Arrival Letter',
    html: `
<div class="page"><div class="frame green"></div><div class="inner">
  <div style="display:flex;align-items:center;gap:2vw">
    ${A.elf(0.6)}
    <div><div style="font-family:Fredoka;letter-spacing:.3em;color:#2f7d4f;font-size:2vh">SPECIAL DELIVERY</div>
    <h1 style="font-size:6.5vh">I'm Here from the North Pole!</h1></div>
  </div>
  <div style="font-size:2.5vh;line-height:1.45;margin-top:1.5vh">
    <div style="display:flex;gap:1vw;align-items:flex-end"><span>Dear</span><span class="line" style="flex:1"></span><span>,</span></div>
    <p style="margin-top:1.5vh">Hooray, I made it! Santa sent me all the way from the North Pole to be your Christmas Elf this season. My name is</p>
    <div class="line" style="width:60%"></div>
    <p style="margin-top:1.5vh">Every night I fly back to tell Santa all about your day, and every morning I'll be hiding somewhere new. Can you find me?</p>
  </div>
  <div style="margin-top:2.5vh;background:#eef7f1;border-radius:20px;padding:1.5vh 2.5vw;font-size:2.4vh">
    <div style="font-family:Fredoka;font-weight:600;color:#2f7d4f;font-size:2.6vh;letter-spacing:.1em;margin-bottom:.8vh">✨ ELF RULES ✨</div>
    <div>❄ Please don't touch me, or my Christmas magic might fade.</div>
    <div>❄ Talk to me anytime, I'll tell Santa everything!</div>
    <div>❄ Be kind, be helpful, and spread lots of Christmas cheer.</div>
    <div>❄ I'll fly home with Santa on Christmas Eve.</div>
  </div>
  <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:auto;margin-bottom:5vh">
    <div style="font-size:2.6vh">Your new best elf friend,<br><span class="line" style="display:inline-block;width:30vw"></span></div>
    <div style="display:flex;align-items:flex-end">${A.candycane(0.4)}${A.gift(0.5, '#e63946', '#f4c430')}</div>
  </div>
</div><div class="brand">DOODLE DESIGN &amp; CO · PERSONAL USE ONLY</div></div>`,
  },
];

(async () => {
  const browser = await chromium.launch();
  for (const p of products) {
    for (const fmt of ['Letter', 'A4']) {
      const page = await browser.newPage();
      const dims = fmt === 'Letter' ? [816, 1056] : [794, 1123];
      const [w, h] = p.landscape ? [dims[1], dims[0]] : dims;
      await page.setViewportSize({ width: w, height: h });
      await page.setContent(`<!doctype html><html><head><meta charset="utf-8">${FONTS}<style>${baseCss(p.landscape)}</style></head><body>${p.html}</body></html>`, { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready);
      await page.pdf({ path: path.join(OUT, `${p.slug}-${fmt}.pdf`), format: fmt, landscape: !!p.landscape, printBackground: true });
      if (fmt === 'Letter') {
        await page.screenshot({ path: path.join(PREV, `${p.slug}.png`), scale: 'device' });
      }
      await page.close();
    }
    console.log('built', p.slug);
  }
  await browser.close();
})();
