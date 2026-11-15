// TikTok ad scenes (1080x1920). Each ad = 4 scenes rendered as PNG, then stitched by ffmpeg with zoom + crossfades.
// Safe zone (third-party guidance): keep text >=120px from sides, >=160px from top, >=480px from bottom.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const A = require('./art');
const ROOT = path.join(__dirname, '..');
const OUT = path.join(ROOT, 'tiktok', 'scenes');
fs.mkdirSync(OUT, { recursive: true });
const img = f => 'data:image/png;base64,' + fs.readFileSync(path.join(ROOT, 'listing-images', 'previews', f)).toString('base64');
const FONTS = `<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Mountains+of+Christmas:wght@700&family=Cormorant+Garamond:wght@500&display=block" rel="stylesheet">`;
const css = `*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1920px;overflow:hidden;font-family:Fredoka;position:relative}
.abs{position:absolute}.paper{position:absolute;background:#fff;box-shadow:0 30px 70px rgba(0,0,0,.35)}.paper img{width:100%;display:block}
.cap{position:absolute;left:120px;right:120px;text-align:center;font-weight:700;color:#fff;line-height:1.15;text-shadow:0 4px 0 rgba(0,0,0,.35),0 0 24px rgba(0,0,0,.35)}
.tag{display:inline-block;background:#fff;color:#111;padding:10px 26px;border-radius:18px;box-shadow:0 6px 0 rgba(0,0,0,.2)}
.wood{position:absolute;inset:0;background:repeating-linear-gradient(90deg,#c9a07a 0 150px,#bf946d 150px 154px,#cfa781 154px 300px)}
.cozy{position:absolute;inset:0;background:radial-gradient(circle at 50% 35%,#c1121f,#7a0c16)}
.sage{position:absolute;inset:0;background:linear-gradient(160deg,#f5efe6,#dfe7da)}`;
// Native TikTok-style caption: white box, black bold text. All text between y=180 and y=1440.
const cap = (t, y = 200, size = 66) => `<div class="abs" style="left:110px;right:110px;top:${y}px;text-align:center"><span style="display:inline;background:#fff;color:#111;font-weight:700;font-size:${size}px;line-height:1.5;padding:8px 22px;border-radius:16px;box-decoration-break:clone;-webkit-box-decoration-break:clone">${t}</span></div>`;
const paper = (f, w, l, t, r = 0) => `<div class="paper" style="width:${w}px;left:${l}px;top:${t}px;transform:rotate(${r}deg)"><img src="${img(f)}"></div>`;
const big = (t, y, size = 120, color = '#fff') => `<div class="cap" style="top:${y}px;font-size:${size}px;color:${color}">${t}</div>`;
const end = (bg, l1, search) => `<div class="${bg}"></div>${big(l1, 260, 92)}
  <div class="abs" style="left:110px;right:110px;top:600px;text-align:center"><span style="display:inline-block;background:#F1641E;color:#fff;font-weight:700;font-size:96px;padding:18px 54px;border-radius:28px;box-shadow:0 10px 0 rgba(0,0,0,.25)">Shop on Etsy</span></div>
  <div class="abs" style="left:110px;right:110px;top:820px;text-align:center"><span class="tag" style="font-size:54px">DoodleDesignAndCo</span></div>
  ${big(search, 990, 56)}${big('🔗 link in bio', 1150, 64)}`;

const ADS = {
  'santa-mail-set': [
    `<div class="wood"></div>${paper('reply-from-santa-letter.png', 900, 90, 640, -2)}${cap('POV: your kid gets a letter<br><b>BACK</b> from Santa 😭', 230, 72)}`,
    `<div class="wood"></div>${paper('reply-from-santa-letter.png', 1500, -210, 520, 0)}${cap('and it has THEIR name on it ✍️', 230)}`,
    `<div class="cozy"></div>${paper('nice-list-certificate.png', 980, 50, 760, -3)}${cap('+ an OFFICIAL Nice List<br>certificate ✅', 230)}`,
    `<div class="cozy"></div>${paper('christmas-wish-list.png', 470, 60, 640, -7)}${paper('christmas-elf-arrival-letter.png', 470, 550, 640, 6)}${cap('+ wish list + elf letter<br>+ Dear Santa letter 🎄', 230)}`,
    `<div class="wood"></div>${paper('dear-santa.png', 430, 50, 700, -8)}${paper('reply-from-santa-letter.png', 430, 330, 640, 0)}${paper('christmas-elf-arrival-letter.png', 430, 600, 700, 8)}${big('ALL 5 = $7.99', 230, 130)}${cap('on Etsy · print at home in 2 min ⚡', 470, 56)}`,
    end('cozy', 'Christmas is coming<br>FAST 🎅', 'search “Santa Mail Set” 👆'),
  ],
  'elf-arrival': [
    `<div class="wood"></div>${paper('christmas-elf-arrival-letter.png', 860, 110, 660, 3)}${cap('Elf arriving Dec 1?<br>Don’t forget THIS 👇', 230, 74)}`,
    `<div class="wood"></div>${paper('christmas-elf-arrival-letter.png', 1450, -190, 470, 0)}${cap('“Hooray, I made it!” 🧝', 230, 70)}`,
    `<div class="sage" style="background:linear-gradient(160deg,#eaf6ef,#cfe9d9)"></div>${paper('christmas-elf-arrival-letter.png', 1450, -190, -60, 0)}${cap('elf rules included<br>(no touching! 🙅‍♀️)', 1180, 66)}`,
    `<div class="cozy"></div>${paper('christmas-elf-arrival-letter.png', 860, 110, 640, -3)}${cap('fill in their name + your elf’s name ✍️', 230, 60)}`,
    `<div class="wood"></div>${paper('christmas-elf-arrival-letter.png', 800, 140, 700, 2)}${big('$3.29', 220, 150)}${cap('on Etsy · instant download ⚡', 460, 56)}`,
    end('cozy', 'Make the arrival<br>feel REAL ✨', 'search “Elf Arrival Letter” 👆'),
  ],
  'nice-list': [
    `<div class="cozy"></div>${paper('nice-list-certificate.png', 980, 50, 720, -2)}${cap('Breaking news from<br>the North Pole 📜', 230, 76)}`,
    `<div class="wood"></div>${paper('nice-list-certificate.png', 1700, -310, 520, 0)}${cap('YOU MADE THE NICE LIST ✅', 230, 70)}`,
    `<div class="cozy"></div>${paper('nice-list-certificate.png', 1700, -150, 300, 0)}${cap('signed by Santa + the Head Elf 🎅', 1180, 60)}`,
    `<div class="wood"></div>${paper('nice-list-certificate.png', 900, 90, 720, 4)}${cap('slip it in the<br>Christmas Eve box 🎁', 230, 72)}`,
    `<div class="cozy"></div>${paper('nice-list-certificate.png', 900, 90, 760, -3)}${big('$3.29', 220, 150)}${cap('on Etsy · print it in 2 minutes ⚡', 460, 56)}`,
    end('cozy', 'Their face when<br>they read it 🥹', 'search “Nice List Certificate” 👆'),
  ],
  '2027-planner': [
    `<div class="sage"></div>${paper('pl-01.png', 760, 160, 640, -2)}${cap('me saying “2027 is MY year”<br>with zero plan 😅', 230, 64)}`,
    `<div class="sage"></div>${paper('pl-01.png', 860, 110, 600, 2)}${cap('ok THIS actually makes it easy 👇', 230, 62)}`,
    `<div class="sage"></div>${paper('pl-04.png', 1400, -160, 470, 0)}${cap('all 12 months already dated ✔️', 230, 62)}`,
    `<div class="sage"></div>${paper('pl-18.png', 520, 40, 620, -4)}${paper('pl-19.png', 520, 520, 660, 4)}${cap('weekly + daily + habit tracker', 230, 62)}`,
    `<div class="sage"></div>${paper('pl-02.png', 560, 60, 700, -5)}${paper('pl-03.png', 560, 460, 660, 5)}${big('<span style="color:#3d3d3a;text-shadow:none">$5.99</span>', 220, 150)}${cap('on Etsy · 19 printable pages', 460, 54)}`,
    end('sage" style="background:linear-gradient(160deg,#8a9a82,#5f7059)', 'Start 2027<br>organized 🌿', 'search “2027 Planner Printable” 👆'),
  ],
};

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [ad, scenes] of Object.entries(ADS)) {
    for (let i = 0; i < scenes.length; i++) {
      await p.setContent(`<!doctype html><html><head><meta charset="utf-8">${FONTS}<style>${css}</style></head><body>${scenes[i]}</body></html>`, { waitUntil: 'networkidle' });
      await p.evaluate(() => document.fonts.ready);
      await p.screenshot({ path: path.join(OUT, `${ad}-${i + 1}.png`) });
    }
  }
  await b.close();
  console.log(Object.keys(ADS).join(' '));
})();
