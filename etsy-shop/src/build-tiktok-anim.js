// Animated TikTok ads: deterministic frame-by-frame render (Playwright) -> JPEG frames -> ffmpeg + music.
// Usage: node src/build-tiktok-anim.js [adName]
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { execFileSync } = require('child_process');
const A = require('./art');
const ROOT = path.join(__dirname, '..');
const TT = path.join(ROOT, 'tiktok');
const FPS = 30, SCENE = 2.0;
const img = f => 'data:image/png;base64,' + fs.readFileSync(path.join(ROOT, 'listing-images', 'previews', f)).toString('base64');

const FONTS = `<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Caveat:wght@700&display=block" rel="stylesheet">`;
const CSS = `*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1920px;overflow:hidden;font-family:Fredoka;background:#000}
.scene{position:absolute;inset:0;display:none;overflow:hidden}.el{position:absolute;will-change:transform}
.paper{background:#fff;box-shadow:0 30px 70px rgba(0,0,0,.35)}.paper img{width:100%;display:block}
.capbox{position:absolute;left:100px;right:100px;text-align:center}
.cap{display:inline;background:#fff;color:#111;font-weight:700;line-height:1.55;padding:8px 20px;border-radius:16px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.w{display:inline-block}
.big{position:absolute;left:60px;right:60px;text-align:center;font-weight:700;color:#fff;text-shadow:0 6px 0 rgba(0,0,0,.3)}
.hand{font-family:Caveat;color:#1d4fa0;white-space:nowrap}
.snow{position:absolute;inset:0;pointer-events:none}
.flake{position:absolute;color:#fff;opacity:.85}
.bg-wood{background:repeating-linear-gradient(90deg,#c9a07a 0 150px,#bf946d 150px 154px,#cfa781 154px 300px)}
.bg-red{background:radial-gradient(circle at 50% 35%,#d7263d,#7a0c16)}
.bg-green{background:radial-gradient(circle at 50% 35%,#2f7d4f,#173d27)}
.bg-sage{background:linear-gradient(160deg,#f5efe6,#dfe7da)}
.bg-sagedk{background:linear-gradient(160deg,#8a9a82,#5f7059)}
.bg-burst{background:repeating-conic-gradient(from 0deg at 50% 42%,#d7263d 0 10deg,#c01d33 10deg 20deg)}
.bg-burstg{background:repeating-conic-gradient(from 0deg at 50% 42%,#2f7d4f 0 10deg,#276b43 10deg 20deg)}
.bg-night{background:radial-gradient(circle at 50% 30%,#2b3a67,#0e1430)}
.kin{position:absolute;left:50px;right:50px;text-align:center;font-weight:700;color:#fff;line-height:1.12;z-index:5;
 text-shadow:5px 0 0 #111,-5px 0 0 #111,0 5px 0 #111,0 -5px 0 #111,4px 4px 0 #111,-4px 4px 0 #111,4px -4px 0 #111,-4px -4px 0 #111,0 10px 0 rgba(0,0,0,.35)}
.kin .k{display:inline-block;margin:0 .1em}
.kin .hl{color:#111;text-shadow:none;padding:0 .2em;border-radius:.22em;box-shadow:0 8px 0 rgba(0,0,0,.3)}
.pill{display:inline-block;font-weight:700;border-radius:24px;padding:10px 34px;box-shadow:0 10px 0 rgba(0,0,0,.28);white-space:nowrap}
#flash{position:absolute;inset:0;background:#fff;opacity:0;pointer-events:none;z-index:50}
#prog{position:absolute;left:60px;right:60px;top:184px;height:12px;border-radius:6px;background:rgba(255,255,255,.35);z-index:40;display:none}
#prog i{display:block;height:100%;width:0;border-radius:6px;background:#F1641E;box-shadow:0 0 10px rgba(241,100,30,.8)}`;

// ---------- element helpers (fx = entrance effect, at = start time within scene) ----------
const el = (html, o) => `<div class="el ${o.cls || ''}" data-fx="${o.fx || 'none'}" data-at="${o.at || 0}" data-rot="${o.rot || 0}" data-float="${o.float ? 1 : 0}"${o.until ? ` data-until="${o.until}"` : ''} style="left:${o.x}px;top:${o.y}px;${o.w ? `width:${o.w}px;` : ''}${o.style || ''}">${html}</div>`;
const paper = (f, o) => el(`<img src="${img(f)}">`, { ...o, cls: 'paper' });
const art = (svg, o) => el(svg, o);
// Caption: white TikTok-style box, words pop in one by one
const cap = (text, y = 210, size = 66, at = 0) => `<div class="capbox" style="top:${y}px;font-size:${size}px"><span class="cap">${text.split(' ').map((w, i) => `<span class="w" data-fx="word" data-at="${at + i * 0.09}">${w}</span>`).join(' ')}</span></div>`;
const big = (html, y, size, o = {}) => el(`<div style="font-size:${size}px;text-align:center;font-weight:700;color:${o.color || '#fff'};text-shadow:0 6px 0 rgba(0,0,0,.28)">${html}</div>`, { x: 60, y, w: 960, fx: o.fx || 'stamp', at: o.at || 0 });
// Handwriting that "writes" itself left->right
const hand = (text, x, y, size, at = .35, rot = 0) => el(`<span class="hand" style="font-size:${size}px">${text}</span>`, { x, y, fx: 'write', at, rot });
const sparkles = (cx, cy, at = .3) => ['✨', '⭐', '✨', '🌟'].map((s, i) => el(`<span style="font-size:${70 - i * 6}px">${s}</span>`, { x: cx + [-380, 330, -300, 360][i], y: cy + [-40, -20, 110, 120][i], fx: 'twinkle', at: at + i * .08 })).join('');
const printer = (f, at = .2) => `
  ${el(`<div style="width:900px;height:330px;background:#eceff3;border-radius:46px;box-shadow:0 20px 50px rgba(0,0,0,.35)"></div>`, { x: 90, y: 1100, fx: 'pop', at: 0 })}
  ${el(`<img src="${img(f)}" style="width:100%;display:block">`, { x: 190, y: 300, w: 700, cls: 'paper', fx: 'print', at, style: 'z-index:1' })}
  ${el(`<div style="width:900px;height:250px;background:linear-gradient(#f6f7f9,#d9dde3);border-radius:0 0 46px 46px;box-shadow:0 20px 50px rgba(0,0,0,.25)"><div style="position:absolute;left:150px;top:40px;width:600px;height:18px;background:#1f2328;border-radius:9px"></div><div style="position:absolute;right:70px;top:120px;width:30px;height:30px;border-radius:50%;background:#2ecc71;box-shadow:0 0 18px #2ecc71"></div></div>`, { x: 90, y: 1270, fx: 'pop', at: 0, style: 'z-index:2' })}`;
const ending = (bg, l1, search) => ({
  bg, html: `${big(l1, 250, 92, { fx: 'pop' })}
  ${el(`<div style="display:inline-block;background:#F1641E;color:#fff;font-weight:700;font-size:100px;padding:20px 60px;border-radius:30px;box-shadow:0 12px 0 rgba(0,0,0,.25)">Shop on Etsy</div>`, { x: 0, y: 590, w: 1080, style: 'text-align:center', fx: 'stamp', at: .35, float: 1 })}
  ${el(`<div style="display:inline-block;background:#fff;color:#111;font-weight:700;font-size:56px;padding:10px 28px;border-radius:18px">DoodleDesignAndCo</div>`, { x: 0, y: 820, w: 1080, style: 'text-align:center', fx: 'pop', at: .6 })}
  ${big(search, 990, 54, { fx: 'pop', at: .8 })}${big('🔗 link in bio', 1140, 66, { fx: 'pop', at: 1.0 })}`
});

// ---------- the ads ----------
const VALUE = '$16.55';
const ADS = {
  'santa-mail-set': { music: 'jingle.wav', scenes: [
    { bg: 'bg-wood', shake: 1, html: `${paper('reply-from-santa-letter.png', { x: 90, y: 640, w: 900, rot: -2, fx: 'drop', float: 1 })}${cap('POV: your kid gets a letter BACK from Santa 😭', 220, 70)}` },
    { bg: 'bg-wood', html: `${paper('reply-from-santa-letter.png', { x: -210, y: 330, w: 1500, fx: 'zoomin' })}${hand('Emma', 250, 845, 120, .3, -3)}${cap('with THEIR name on it ✍️', 1450, 64, .1)}` },
    { bg: 'bg-red', html: `${paper('nice-list-certificate.png', { x: 50, y: 760, w: 980, rot: -3, fx: 'slideR', float: 1 })}${big('✅ APPROVED', 520, 92, { at: .7 })}${cap('+ an OFFICIAL Nice List certificate', 220, 64)}` },
    { bg: 'bg-green', html: `${paper('christmas-wish-list.png', { x: 30, y: 640, w: 470, rot: -8, fx: 'slideL', at: .1 })}${paper('christmas-elf-arrival-letter.png', { x: 580, y: 640, w: 470, rot: 7, fx: 'slideR', at: .3 })}${paper('dear-santa.png', { x: 300, y: 900, w: 480, rot: -1, fx: 'drop', at: .55 })}${cap('+ elf letter + wish list + Dear Santa 🎄', 220, 62)}` },
    { bg: 'bg-red', html: `${big(`<span style="text-decoration:line-through;opacity:.75;font-size:70px">${VALUE}</span>`, 300, 70, { at: .05 })}${big('ALL 5 = $7.99', 420, 132, { at: .35 })}${sparkles(540, 480, .5)}${paper('dear-santa.png', { x: 60, y: 820, w: 400, rot: -8, fx: 'pop', at: .6 })}${paper('reply-from-santa-letter.png', { x: 340, y: 780, w: 400, fx: 'pop', at: .7 })}${paper('christmas-elf-arrival-letter.png', { x: 620, y: 820, w: 400, rot: 8, fx: 'pop', at: .8 })}${cap('on Etsy · instant download', 640, 54, .5)}` },
    { bg: 'bg-green', html: `${printer('reply-from-santa-letter.png')}${cap('No shipping. Print it TONIGHT ⚡', 210, 64)}` },
    ending('bg-red', 'Christmas is coming<br>FAST 🎅', 'search “Santa Mail Set” 👆'),
  ] },
  'elf-arrival': { music: 'jingle.wav', scenes: [
    { bg: 'bg-green', shake: 1, html: `${art(A.elf(2.6), { x: 280, y: 700, fx: 'drop', float: 1 })}${cap('Your elf comes back soon… is he ready? 👀', 220, 68)}` },
    { bg: 'bg-wood', html: `${paper('christmas-elf-arrival-letter.png', { x: 110, y: 620, w: 860, rot: 3, fx: 'slideL', float: 1 })}${cap('this year he brings a LETTER 🧝✉️', 220, 66)}` },
    { bg: 'bg-wood', html: `${paper('christmas-elf-arrival-letter.png', { x: -190, y: 300, w: 1450, fx: 'zoomin' })}${hand('Liam', 230, 735, 120, .3, -2)}${cap('add their name ✍️', 1450, 66, .1)}` },
    { bg: 'bg-green', html: `${paper('christmas-elf-arrival-letter.png', { x: -190, y: -150, w: 1450, fx: 'zoomin' })}${cap('+ ELF RULES (no touching! 🙅‍♀️)', 1300, 64)}` },
    { bg: 'bg-red', html: `${big('$3.29', 330, 170, { at: .1 })}${sparkles(540, 410, .3)}${paper('christmas-elf-arrival-letter.png', { x: 190, y: 720, w: 700, rot: -3, fx: 'pop', at: .4, float: 1 })}${cap('on Etsy · instant download', 600, 54, .3)}` },
    { bg: 'bg-green', html: `${printer('christmas-elf-arrival-letter.png')}${cap('print it the night before ⚡', 210, 64)}` },
    ending('bg-red', 'Make the arrival<br>feel REAL ✨', 'search “Elf Arrival Letter” 👆'),
  ] },
  'nice-list': { music: 'jingle.wav', scenes: [
    { bg: 'bg-red', shake: 1, html: `${el(`<div style="background:#111;color:#fff;font-weight:700;font-size:64px;padding:14px 40px;border-radius:12px;display:inline-block">🚨 BREAKING NEWS 🚨</div>`, { x: 0, y: 470, w: 1080, style: 'text-align:center', fx: 'slideL' })}${paper('nice-list-certificate.png', { x: 50, y: 760, w: 980, rot: -2, fx: 'drop', at: .3, float: 1 })}${cap('from the North Pole 📜', 220, 72)}` },
    { bg: 'bg-wood', html: `${paper('nice-list-certificate.png', { x: -310, y: 420, w: 1700, fx: 'zoomin' })}${hand('Sophia', 330, 905, 130, .3)}${cap('YOU made the Nice List ✅', 220, 70)}` },
    { bg: 'bg-red', html: `${paper('nice-list-certificate.png', { x: -150, y: 260, w: 1700, fx: 'zoomin' })}${cap('signed by Santa + the Head Elf 🎅', 1420, 60)}` },
    { bg: 'bg-green', html: `${art(A.gift(5), { x: 240, y: 980, fx: 'pop', at: .1, float: 1 })}${paper('nice-list-certificate.png', { x: 140, y: 560, w: 800, rot: 5, fx: 'drop', at: .4 })}${cap('the Christmas Eve box must-have 🎁', 220, 62)}` },
    { bg: 'bg-red', html: `${big('$3.29', 330, 170, { at: .1 })}${sparkles(540, 410, .3)}${paper('nice-list-certificate.png', { x: 90, y: 760, w: 900, rot: -3, fx: 'pop', at: .4, float: 1 })}${cap('on Etsy · instant download', 600, 54, .3)}` },
    { bg: 'bg-green', html: `${printer('nice-list-certificate.png')}${cap('print in 2 minutes ⚡', 210, 66)}` },
    ending('bg-red', 'Their face when<br>they read it 🥹', 'search “Nice List Certificate” 👆'),
  ] },
  'coloring-book': { music: 'jingle.wav', scenes: [
    { bg: 'bg-red', shake: 1, html: `${paper('cb-01.png', { x: 160, y: 600, w: 760, rot: -2, fx: 'drop', float: 1 })}${cap('Need 20 minutes of quiet this Christmas? 🤫', 220, 66)}` },
    { bg: 'bg-wood', html: `${['cb-04.png','cb-06.png','cb-08.png','cb-13.png','cb-16.png'].map((f, i) => paper(f, { x: 40 + i * 120, y: 560 + i * 60, w: 520, rot: -10 + i * 5, fx: 'slideR', at: i * .16 })).join('')}${cap('20 Christmas coloring pages 🎨', 220, 66)}` },
    { bg: 'bg-green', html: `${paper('cb-03.png', { x: -150, y: 420, w: 1380, fx: 'zoomin' })}${cap('Santa’s toy factory, reindeer, gingerbread…', 220, 60)}` },
    { bg: 'bg-red', html: `${paper('cb-22.png', { x: 170, y: 560, w: 740, rot: 3, fx: 'pop', at: .1, float: 1 })}${cap('+ a Note from Santa at the end 💌', 220, 64)}` },
    { bg: 'bg-green', html: `${big('$3.99', 330, 170, { at: .1 })}${sparkles(540, 410, .3)}${paper('cb-01.png', { x: 290, y: 760, w: 500, rot: -3, fx: 'pop', at: .4, float: 1 })}${cap('on Etsy · instant download', 600, 54, .3)}` },
    { bg: 'bg-wood', html: `${printer('cb-05.png')}${cap('print as many as you want 🖨️', 210, 64)}` },
    ending('bg-red', 'Print tonight.<br>Quiet Christmas morning ☕', 'search “Santa’s Little Helpers Coloring” 👆'),
  ] },
  'holly-jolly': { music: 'jingle.wav', scenes: [
    { bg: 'bg-green', shake: 1, html: `${paper('hj.png', { x: 190, y: 600, w: 700, rot: -2, fx: 'drop', float: 1 })}${cap('Christmas decor for under $3? 🎄', 220, 70)}` },
    { bg: 'bg-wood', html: `${el(`<div style="padding:30px;background:#f7f3ec;border:28px solid #3b2a20;box-shadow:0 30px 60px rgba(0,0,0,.4)"><img src="${img('hj.png')}" style="width:100%;display:block"></div>`, { x: 200, y: 560, w: 680, fx: 'pop', at: .1, float: 1 })}${cap('just print it + frame it ✨', 220, 68)}` },
    { bg: 'bg-red', html: `${paper('hj.png', { x: -150, y: 380, w: 1380, fx: 'zoomin' })}${cap('vintage ornaments + candy stripes 🍬', 220, 62)}` },
    { bg: 'bg-green', html: `${printer('hj.png')}${cap('done in 2 minutes ⚡', 210, 68)}` },
    { bg: 'bg-red', html: `${big('$2.99', 330, 170, { at: .1 })}${sparkles(540, 410, .3)}${paper('hj.png', { x: 290, y: 760, w: 500, rot: -3, fx: 'pop', at: .4, float: 1 })}${cap('on Etsy · instant download', 600, 54, .3)}` },
    ending('bg-green', 'Instant holiday<br>cheer 🎁', 'search “Holly Jolly Printable” 👆'),
  ] },
  '2027-planner': { music: 'planner.wav', snow: 0, scenes: [
    { bg: 'bg-sage', shake: 1, html: `${paper('pl-01.png', { x: 160, y: 640, w: 760, rot: -2, fx: 'drop', float: 1 })}${cap('me: “2027 is MY year” 💅 also me: no plan', 220, 64)}` },
    { bg: 'bg-sage', html: `${paper('pl-01.png', { x: 110, y: 600, w: 860, rot: 2, fx: 'stamp', float: 1 })}${cap('ok THIS actually fixed it 👇', 220, 64)}` },
    { bg: 'bg-sage', html: `${['pl-02.png', 'pl-03.png', 'pl-04.png', 'pl-18.png', 'pl-19.png'].map((f, i) => paper(f, { x: 40 + i * 120, y: 560 + i * 60, w: 520, rot: -10 + i * 5, fx: 'slideR', at: i * .18 })).join('')}${cap('19 pages that do the thinking', 220, 64)}` },
    { bg: 'bg-sage', html: `${paper('pl-04.png', { x: -160, y: 470, w: 1400, fx: 'zoomin' })}${cap('all 12 months already dated ✔️', 220, 62)}` },
    { bg: 'bg-sagedk', html: `${big('$5.99', 330, 170, { at: .1 })}${sparkles(540, 410, .3)}${paper('pl-01.png', { x: 290, y: 760, w: 500, rot: -3, fx: 'pop', at: .4, float: 1 })}${cap('on Etsy · instant download', 600, 54, .3)}` },
    { bg: 'bg-sage', html: `${printer('pl-04.png')}${cap('print only the pages you need 🖨️', 210, 60)}` },
    ending('bg-sagedk', 'Start 2027<br>organized 🌿', 'search “2027 Planner Printable” 👆'),
  ] },
};

// ---------- hook variants: new first scene (+ optional new ending) on top of a base ad ----------
const H = (bg, html) => ({ bg, shake: 1, html });
const VARIANTS = {
  'santa-memories': ['santa-mail-set', H('bg-wood', `${paper('reply-from-santa-letter.png', { x: 110, y: 640, w: 860, rot: 3, fx: 'drop', float: 1 })}${cap('things my kids will remember FOREVER 🎅', 220, 68)}`)],
  'santa-tradition': ['santa-mail-set', H('bg-green', `${paper('dear-santa.png', { x: 60, y: 620, w: 520, rot: -7, fx: 'slideL' })}${paper('reply-from-santa-letter.png', { x: 500, y: 680, w: 520, rot: 6, fx: 'slideR', at: .2 })}${cap('the Christmas tradition we’re starting this year ✨', 220, 64)}`)],
  'santa-value': ['santa-mail-set', H('bg-red', `${['dear-santa.png','reply-from-santa-letter.png','christmas-wish-list.png','christmas-elf-arrival-letter.png'].map((f,i)=>paper(f,{x:30+i*240,y:640+(i%2)*70,w:420,rot:-9+i*6,fx:'drop',at:i*.12})).join('')}${cap('$7.99 for ALL of this?? 😳', 220, 76)}`)],
  'elf-pov': ['elf-arrival', H('bg-wood', `${paper('christmas-elf-arrival-letter.png', { x: 110, y: 640, w: 860, rot: -3, fx: 'drop', float: 1 })}${cap('POV: your kids find THIS from their elf 🧝', 220, 68)}`)],
  'elf-budget': ['elf-arrival', H('bg-green', `${art(A.elf(2.4), { x: 300, y: 720, fx: 'pop', float: 1 })}${cap('Christmas elf ideas for TIRED parents 😮‍💨👇', 220, 64)}`)],
  'nice-ask': ['nice-list', H('bg-red', `${paper('nice-list-certificate.png', { x: 50, y: 760, w: 980, rot: 2, fx: 'drop', float: 1 })}${cap('when they ask “am I on the Nice List?” 🥹', 220, 68)}`)],
  'nice-evebox': ['nice-list', H('bg-green', `${art(A.gift(4.5), { x: 270, y: 1000, fx: 'pop' })}${paper('nice-list-certificate.png', { x: 140, y: 600, w: 800, rot: -4, fx: 'drop', at: .25 })}${cap('Christmas Eve box idea for $3.29 🎁', 220, 70)}`)],
  'coloring-winterbreak': ['coloring-book', H('bg-wood', `${paper('cb-01.png', { x: 160, y: 600, w: 760, rot: 3, fx: 'drop', float: 1 })}${cap('winter break survival kit for moms 😅', 220, 70)}`)],
  'coloring-kidstable': ['coloring-book', H('bg-green', `${paper('cb-06.png', { x: 150, y: 600, w: 780, rot: -3, fx: 'drop', float: 1 })}${cap('kids’ table activity for Christmas dinner 🍽️', 220, 66)}`)],
  'dearsanta-tonight': ['santa-mail-set', H('bg-red', `${paper('dear-santa.png', { x: 110, y: 620, w: 860, rot: -2, fx: 'drop', float: 1 })}${cap('writing our letters to Santa tonight ✉️🎅', 220, 68)}`)],
  'lastminute': ['santa-mail-set', H('bg-red', `${big('⚡ NO SHIPPING ⚡', 480, 110, { fx: 'stamp' })}${['nice-list-certificate.png','christmas-elf-arrival-letter.png','cb-01.png'].map((f,i)=>paper(f,{x:60+i*320,y:760+(i%2)*60,w:440,rot:-6+i*6,fx:'pop',at:.3+i*.12})).join('')}${cap('last-minute Christmas magic you print TONIGHT', 220, 62)}`)],
};
// Wish list gets its own full ad
ADS['wish-list'] = { music: 'jingle.wav', scenes: [
  { bg: 'bg-wood', shake: 1, html: `${paper('christmas-wish-list.png', { x: 110, y: 620, w: 860, rot: -2, fx: 'drop', float: 1 })}${cap('Grandma asked what they want for Christmas 👀', 220, 66)}` },
  { bg: 'bg-wood', html: `${paper('christmas-wish-list.png', { x: -190, y: 300, w: 1450, fx: 'zoomin' })}${hand('Mia, 6', 250, 870, 100, .3, -2)}${cap('so they wrote it ALL down ✍️', 1450, 64, .1)}` },
  { bg: 'bg-red', html: `${paper('christmas-wish-list.png', { x: -190, y: -60, w: 1450, fx: 'zoomin' })}${cap('+ a box to draw their #1 wish 🎨', 1350, 62)}` },
  { bg: 'bg-green', html: `${paper('christmas-wish-list.png', { x: 60, y: 660, w: 480, rot: -6, fx: 'slideL' })}${paper('dear-santa.png', { x: 540, y: 660, w: 480, rot: 6, fx: 'slideR', at: .2 })}${cap('send one to Santa, one to Grandma 💌', 220, 64)}` },
  { bg: 'bg-red', html: `${big('$2.99', 330, 170, { at: .1 })}${sparkles(540, 410, .3)}${paper('christmas-wish-list.png', { x: 190, y: 720, w: 700, rot: -3, fx: 'pop', at: .4, float: 1 })}${cap('on Etsy · instant download', 600, 54, .3)}` },
  { bg: 'bg-green', html: `${printer('christmas-wish-list.png')}${cap('print one for every kid 🖨️', 210, 66)}` },
  ending('bg-red', 'Gift shopping<br>made easy 🎁', 'search “Christmas Wish List Kids” 👆'),
] };
for (const [name, [base, hook]] of Object.entries(VARIANTS)) ADS[name] = { ...ADS[base], scenes: [hook, ...ADS[base].scenes.slice(1)] };

// ================= v3 formats (Nov 18 research: faster ~1.33s beat-synced cuts, kinetic highlighted text,
// sticker pops, pattern-interrupt hook, price-reveal "ding", progress bar, loop-back flash, SFX) =================
const BEAT3 = 1 / 3, CUT = 4 * BEAT3;                  // 180 BPM jingle-punch.wav: 4 beats per cut
const S3 = (bg, html, o = {}) => ({ bg, html, dur: o.dur || CUT, shake: o.shake ? 1 : 0, sfx: o.sfx || [] });
// Kinetic text: words pop one by one; *word* gets a colored highlight pill; _ joins words inside a pill
const kin = (text, y, size = 84, at = 0, o = {}) => { let k = 0; return `<div class="kin" style="top:${y}px;font-size:${size}px">${text.split(' ').map(w => {
  const m = w.match(/^\*(.+)\*([…!?.,:]*)$/), h = !!m, t = (h ? m[1] : w).replace(/_/g, ' '), tail = h ? m[2] : '';
  return `<span class="k${h ? ' hl' : ''}" data-fx="kin" data-at="${(at + (k++) * (o.step || .07)).toFixed(3)}" data-rot="${h ? -2 : 0}" style="${h ? `background:${o.hl || '#FFD93D'}` : ''}">${t}</span>${tail ? `<span class="k" data-fx="kin" data-at="${(at + (k - 1) * (o.step || .07)).toFixed(3)}" style="margin-left:-.08em">${tail}</span>` : ''}`; }).join(' ')}</div>`; };
const pill = (t, bg, color, size) => `<div class="pill" style="background:${bg};color:${color};font-size:${size}px">${t}</div>`;
const stk = (html, x, y, at = .3, rot = 0) => el(html, { x, y, fx: 'sticker', at, rot, style: 'z-index:6' });
const emo = (e, x, y, size = 120, at = .3, rot = 0) => stk(`<span style="font-size:${size}px">${e}</span>`, x, y, at, rot);
const centered = (html, y, o = {}) => el(html, { x: 0, y, w: 1080, style: 'text-align:center;z-index:6', fx: o.fx || 'slam', at: o.at || 0, float: o.float });
// Zoom a preview so that point (fx,fy) (fractions of the page) sits at screen (540, cy)
const zoomTo = (f, ratio, fx, fy, W, cy = 1020) => paper(f, { x: Math.round(540 - fx * W), y: Math.round(cy - fy * W * ratio), w: W, fx: 'zoomin' });
const flip = (files, o) => files.map((f, k) => paper(f, { ...o, fx: 'punchin', at: k * (o.step || BEAT3), until: k < files.length - 1 ? (k + 1) * (o.step || BEAT3) : 0, rot: (k % 2 ? 3 : -3) })).join('');
const price3 = (bg, price, was, sub, extra = '') => S3(bg, `${was ? el(`<div style="position:relative;display:inline-block;font-size:76px;font-weight:700;color:#fff;text-shadow:0 5px 0 rgba(0,0,0,.35)">${was}<div data-fx="strike" data-at=".25" style="position:absolute;left:-10px;right:-10px;top:44%;height:12px;background:#FFD93D;border-radius:6px"></div></div>`, { x: 0, y: 240, w: 1080, style: 'text-align:center', fx: 'pop', at: 0 }) : ''}
  ${centered(`<div style="display:inline-block;background:#FFD93D;color:#111;font-weight:700;font-size:160px;padding:0 54px;border-radius:44px;box-shadow:0 14px 0 rgba(0,0,0,.3);transform:rotate(-3deg)">${price}</div>`, 360, { at: .45 })}
  ${sparkles(540, 440, .6)}${kin(sub, 620, 64, .7)}${extra}`, { dur: 6 * BEAT3, sfx: [['ding', .45]] });
const print3 = (f, text) => S3('bg-green', `${printer(f, .05)}${kin(text, 220, 80)}`);
const end3 = (bg, l1, search) => S3(bg, `${kin(l1, 240, 86)}
  ${centered(`<div style="display:inline-block;background:#F1641E;color:#fff;font-weight:700;font-size:100px;padding:20px 60px;border-radius:30px;box-shadow:0 12px 0 rgba(0,0,0,.25)">Shop on Etsy</div>`, 600, { at: .3, float: 1 })}
  ${centered(pill('DoodleDesignAndCo', '#fff', '#111', 56), 830, { fx: 'pop', at: .55 })}
  ${kin(search, 990, 58, .7, { step: .05 })}${kin('🔗 *link_in_bio*', 1170, 76, 1.0)}`, { dur: 8 * BEAT3, sfx: [['pop', .3], ['pop', 1.0]] });
const V3 = scenes => ({ music: 'jingle-punch.wav', v3: 1, scenes });
const LET = 1056 / 816, CERT = 816 / 1056, WL2 = 1123 / 794;
const fan3 = (files, y = 720, at = .1) => files.map((f, k) => paper(f, { x: 40 + k * 300, y: y + (k % 2) * 60, w: 420, rot: -8 + k * 8, fx: 'drop', at: at + k * .1 })).join('');

ADS['v3-santa-mail-set'] = V3([
  S3('bg-burst', `${paper('reply-from-santa-letter.png', { x: 120, y: 600, w: 840, rot: -3, fx: 'punchin', float: 1 })}${kin('POV: Santa *WROTE_BACK* 😭', 230, 100, -.12)}${emo('💌', 760, 520, 150, .35, 12)}`, { shake: 1 }),
  S3('bg-wood', `${paper('reply-from-santa-letter.png', { x: -210, y: 330, w: 1500, fx: 'zoomin' })}${hand('Emma', 250, 845, 120, .2, -3)}${kin('with *THEIR_NAME* on it ✍️', 230, 84)}`),
  S3('bg-red', `${paper('nice-list-certificate.png', { x: 50, y: 760, w: 980, rot: -3, fx: 'slideR', float: 1 })}${kin('+ an OFFICIAL *Nice_List* 📜', 230, 86)}${stk(pill('✅ APPROVED', '#2ecc71', '#fff', 80), 300, 560, .55, -8)}`, { sfx: [['pop', .55]] }),
  S3('bg-green', `${paper('christmas-elf-arrival-letter.png', { x: 140, y: 620, w: 800, rot: 4, fx: 'slideL', float: 1 })}${kin('+ an *elf* arrival letter 🧝', 230, 86)}`),
  S3('bg-wood', `${paper('christmas-wish-list.png', { x: 40, y: 640, w: 500, rot: -7, fx: 'slideL' })}${paper('dear-santa.png', { x: 540, y: 660, w: 500, rot: 6, fx: 'slideR', at: .15 })}${kin('+ wish list + *Dear_Santa* ✉️', 230, 82)}`),
  S3('bg-night', `${['dear-santa.png', 'reply-from-santa-letter.png', 'nice-list-certificate.png', 'christmas-elf-arrival-letter.png', 'christmas-wish-list.png'].map((f, i) => paper(f, { x: 20 + i * 190, y: 700 + (i % 2) * 90, w: 420, rot: -12 + i * 6, fx: 'pop', at: i * BEAT3 * .6 })).join('')}${kin('*5* printables. *1* set. 🤯', 230, 100)}`),
  price3('bg-burst', '$7.99', '$16.55 value', 'ALL 5 · *instant* download', fan3(['dear-santa.png', 'reply-from-santa-letter.png', 'christmas-elf-arrival-letter.png'], 820, .8)),
  print3('reply-from-santa-letter.png', 'No shipping. Print it *TONIGHT* ⚡'),
  end3('bg-red', 'Their face when they read it 🥹', 'search *Santa_Mail_Set* on Etsy'),
]);
ADS['v3-coloring-book'] = V3([
  S3('bg-burstg', `${paper('cb-01.png', { x: 200, y: 640, w: 680, rot: -3, fx: 'punchin', float: 1 })}${kin('I found the *20-minute* quiet trick 🤫', 230, 92, -.12)}${emo('☕', 800, 1180, 140, .4, 10)}`, { shake: 1 }),
  S3('bg-wood', `${flip(['cb-04.png', 'cb-06.png', 'cb-08.png', 'cb-13.png'], { x: 170, y: 600, w: 740 })}${kin('*20* Christmas coloring pages 🎨', 230, 80)}`),
  S3('bg-red', `${flip(['cb-03.png', 'cb-16.png', 'cb-10.png', 'cb-19.png'], { x: 170, y: 600, w: 740 })}${kin('toys, reindeer, *gingerbread* 🍪', 230, 84)}`),
  S3('bg-green', `${paper('cb-22.png', { x: 190, y: 600, w: 700, rot: 3, fx: 'pop', at: .05, float: 1 })}${kin('+ a *Note_from_Santa* at the end 💌', 230, 82)}`),
  S3('bg-night', `${kin('BEFORE: “I’m BORED!” 😩', 330, 82)}${kin('AFTER: *20_min_of_quiet* ☕😌', 760, 82, .55, { hl: '#9be3b5' })}${emo('👇', 470, 560, 110, .4)}`, { sfx: [['pop', .55]] }),
  price3('bg-burst', '$3.99', '', 'that’s *20¢* a page 🤯', paper('cb-01.png', { x: 320, y: 840, w: 440, rot: -4, fx: 'pop', at: .8, float: 1 })),
  print3('cb-05.png', 'print it *again_&_again* 🖨️'),
  end3('bg-green', 'Quiet Christmas morning *unlocked* ☕', 'search *Santa’s_Little_Helpers* on Etsy'),
]);
ADS['v3-nice-list'] = V3([
  S3('bg-burst', `${centered(pill('🚨 BREAKING NEWS 🚨', '#111', '#fff', 68), 230, { at: -.17 })}${kin('the North Pole just released the *NICE_LIST* 📜', 360, 78, .1)}${paper('nice-list-certificate.png', { x: 50, y: 800, w: 980, rot: -2, fx: 'drop', at: -.25, float: 1 })}`, { shake: 1 }),
  S3('bg-wood', `${paper('nice-list-certificate.png', { x: -310, y: 420, w: 1700, fx: 'zoomin' })}${hand('Sophia', 330, 905, 130, .2)}${kin('guess who made it 👀', 230, 88)}`),
  S3('bg-red', `${paper('nice-list-certificate.png', { x: 50, y: 760, w: 980, rot: 2, fx: 'slideL' })}${centered(pill('✅ APPROVED', '#2ecc71', '#fff', 110), 560, { at: .4 })}${kin('*OFFICIALLY* checked by Santa 🎅', 230, 82)}`, { sfx: [['pop', .4]] }),
  S3('bg-green', `${paper('nice-list-certificate.png', { x: -150, y: 260, w: 1700, fx: 'zoomin' })}${kin('signed by Santa + the *Head_Elf* ✍️', 230, 82)}`),
  S3('bg-night', `${art(A.gift(5), { x: 240, y: 1000, fx: 'pop', at: .05, float: 1 })}${paper('nice-list-certificate.png', { x: 140, y: 560, w: 800, rot: 5, fx: 'drop', at: .2 })}${kin('the *Christmas_Eve_box* must-have 🎁', 230, 82)}`),
  price3('bg-burst', '$3.29', '', 'print it in *2_minutes* ⚡', paper('nice-list-certificate.png', { x: 140, y: 820, w: 800, rot: -3, fx: 'pop', at: .8, float: 1 })),
  print3('nice-list-certificate.png', 'add their name. *Print_tonight.* 🖨️'),
  end3('bg-red', 'Is YOUR kid on the list? 👀', 'search *Nice_List_Certificate* on Etsy'),
]);
ADS['v3-elf-arrival'] = V3([
  S3('bg-night', `${art(A.elf(2.6), { x: 280, y: 700, fx: 'punchin', float: 1 })}${kin('POV: your elf came back with a *LETTER* 🧝✉️', 230, 86, -.12)}${emo('👀', 120, 1150, 140, .35, -10)}`, { shake: 1 }),
  S3('bg-wood', `${paper('christmas-elf-arrival-letter.png', { x: 140, y: 600, w: 800, rot: 3, fx: 'slideL', float: 1 })}${kin('he wrote them a *letter* ✉️', 230, 88)}`),
  S3('bg-wood', `${paper('christmas-elf-arrival-letter.png', { x: -190, y: 300, w: 1450, fx: 'zoomin' })}${hand('Liam', 230, 735, 120, .2, -2)}${kin('with *THEIR_NAME* on it ✍️', 1240, 80)}`),
  S3('bg-green', `${paper('christmas-elf-arrival-letter.png', { x: -190, y: -150, w: 1450, fx: 'zoomin' })}${kin('+ ELF RULES: *no_touching!* 🙅‍♀️', 1240, 78)}`),
  S3('bg-red', `${kin('made for *TIRED* parents 😮‍💨', 230, 88)}${stk(pill('⏱️ 2 min', '#fff', '#111', 84), 110, 620, .25, -6)}${stk(pill('🚫 no shipping', '#FFD93D', '#111', 84), 330, 820, .45, 5)}${stk(pill('🖨️ print at 10pm', '#fff', '#111', 84), 150, 1020, .65, -4)}`, { sfx: [['pop', .25], ['pop', .45], ['pop', .65]] }),
  price3('bg-burstg', '$3.29', '', 'instant *download* on Etsy', paper('christmas-elf-arrival-letter.png', { x: 290, y: 800, w: 500, rot: -3, fx: 'pop', at: .8, float: 1 })),
  print3('christmas-elf-arrival-letter.png', 'print it the *night_before* ⚡'),
  end3('bg-red', 'Make the arrival feel *REAL* ✨', 'search *Elf_Arrival_Letter* on Etsy'),
]);
ADS['v3-wish-list-v2'] = V3([
  S3('bg-burstg', `${paper('wl2.png', { x: 190, y: 600, w: 700, rot: -3, fx: 'punchin', float: 1 })}${kin('the *4-gift_rule*… but KIDS write it 🎁', 230, 88, -.12)}`, { shake: 1 }),
  S3('bg-red', `${zoomTo('wl2.png', WL2, .78, .47, 2000)}${kin('something they *WANT* 🎁', 230, 90, 0, { hl: '#ff9fb2' })}`, { dur: 3 * BEAT3 }),
  S3('bg-green', `${zoomTo('wl2.png', WL2, .78, .59, 2000)}${kin('something they *NEED* 🧦', 230, 90, 0, { hl: '#9be3b5' })}`, { dur: 3 * BEAT3 }),
  S3('bg-red', `${zoomTo('wl2.png', WL2, .58, .71, 2000)}${kin('something to *WEAR* 👕', 230, 90, 0, { hl: '#ff9fb2' })}`, { dur: 3 * BEAT3 }),
  S3('bg-green', `${zoomTo('wl2.png', WL2, .84, .71, 2000)}${kin('something to *READ* 📚', 230, 90, 0, { hl: '#9be3b5' })}`, { dur: 3 * BEAT3 }),
  S3('bg-wood', `${zoomTo('wl2.png', WL2, .70, .86, 1700)}${kin('+ their *BIGGEST* wish ⭐', 230, 90)}`),
  price3('bg-burst', '$2.99', '', 'no more *“what_do_they_want?”* texts 😅', paper('wl2.png', { x: 320, y: 860, w: 440, rot: -4, fx: 'pop', at: .8, float: 1 })),
  print3('wl2.png', 'print one for *every_kid* 🖨️'),
  end3('bg-green', 'Grandma will *thank_you* 😂', 'search *Want_Need_Wear_Read* on Etsy'),
]);
ADS['v3-3-printables'] = V3([
  S3('bg-burst', `${kin('*3* Christmas printables every mom needs 🎄', 230, 90, -.12)}${fan3(['reply-from-santa-letter.png', 'nice-list-certificate.png', 'cb-01.png'], 700, -.3)}${stk(pill('wait for #3 👀', '#111', '#fff', 64), 90, 1230, .5, -5)}`, { shake: 1 }),
  S3('bg-wood', `${paper('reply-from-santa-letter.png', { x: 140, y: 600, w: 800, rot: -3, fx: 'punchin', float: 1 })}${kin('*#1* a letter BACK from Santa 🎅', 230, 86)}`),
  S3('bg-wood', `${paper('reply-from-santa-letter.png', { x: -210, y: 330, w: 1500, fx: 'zoomin' })}${hand('Emma', 250, 845, 120, .15, -3)}${kin('with their name on it 🥹', 230, 86)}${stk(pill('5-piece set $7.99', '#FFD93D', '#111', 70), 80, 1230, .5, -5)}`, { sfx: [['ding', .5]] }),
  S3('bg-red', `${paper('nice-list-certificate.png', { x: 50, y: 760, w: 980, rot: -2, fx: 'drop', float: 1 })}${kin('*#2* an OFFICIAL Nice List ✅', 230, 86)}`),
  S3('bg-red', `${paper('nice-list-certificate.png', { x: -150, y: 420, w: 1380, fx: 'zoomin' })}${kin('Christmas Eve box ✔️', 230, 86)}${stk(pill('$3.29', '#FFD93D', '#111', 90), 80, 1230, .45, -5)}`, { sfx: [['ding', .45]] }),
  S3('bg-green', `${flip(['cb-04.png', 'cb-08.png', 'cb-13.png', 'cb-16.png'], { x: 170, y: 640, w: 740 })}${kin('*#3* 20 coloring pages = 20 min of QUIET 🤫', 230, 80)}`),
  S3('bg-green', `${paper('cb-22.png', { x: 190, y: 600, w: 700, rot: 3, fx: 'pop', float: 1 })}${kin('+ a Note from Santa 💌', 230, 86)}${stk(pill('$3.99', '#FFD93D', '#111', 90), 80, 1230, .45, -5)}`, { sfx: [['ding', .45]] }),
  print3('nice-list-certificate.png', 'all instant downloads. *Print_TONIGHT* ⚡'),
  end3('bg-red', 'Which one are YOU printing? 👇', 'search *DoodleDesignAndCo* on Etsy'),
]);

// ---------- in-page animation engine ----------
const ENGINE = `
const E={outBack:p=>1+2.7*Math.pow(p-1,3)+1.7*Math.pow(p-1,2),outCubic:p=>1-Math.pow(1-p,3),
 outBounce:p=>{const n=7.5625,d=2.75;if(p<1/d)return n*p*p;if(p<2/d)return n*(p-=1.5/d)*p+.75;if(p<2.5/d)return n*(p-=2.25/d)*p+.9375;return n*(p-=2.625/d)*p+.984375}};
const cl=(v)=>Math.max(0,Math.min(1,v));
window.render=(t,durs,shakes,snow,v3)=>{
  const scenes=[...document.querySelectorAll('.scene')];let i=0,t0=0;while(i<durs.length-1&&t>=t0+durs[i]){t0+=durs[i];i++}
  const lt=t-t0,SCENE=durs[i],TOTAL=durs.reduce((a,b)=>a+b,0);
  scenes.forEach((s,k)=>s.style.display=k===i?'block':'none');const s=scenes[i];
  // scene entrance: quick zoom-punch; slow push-in; hook shake
  const ent=cl(lt/.22);let sc=1.12-.12*E.outCubic(ent)+.035*lt/SCENE;let sx=0,sy=0,extra='';
  if(shakes[i]&&lt>.35&&lt<.75){sx=Math.sin(lt*90)*14*(.75-lt);sy=Math.cos(lt*70)*10*(.75-lt)}
  if(v3){const B=v3.beat,ph=t%B,bn=Math.round((t-ph)/B);const e2=cl(lt/.16);
    // entrance alternates: zoom punch / whip pan left / whip pan right; plus beat-synced zoom punches
    const kind=i===0?0:i%3;sc=1+(kind===0?(i===0?.06:.2)*(1-E.outCubic(e2)):0)+(bn%2===0?.045:.018)*Math.exp(-ph*14)+.03*lt/SCENE;
    if(kind)sx=(kind===1?-1:1)*320*(1-E.outCubic(e2));
    if(shakes[i]&&lt<.45){sx+=Math.sin(lt*95)*22*(.45-lt)/.45;sy=Math.cos(lt*75)*16*(.45-lt)/.45;extra=' rotate('+(Math.sin(lt*60)*1.5*(.45-lt)/.45)+'deg)'}
    let fo=i===0?.3*cl(1-lt/.12):.35*cl(1-lt/.09);const left=TOTAL-t;if(left<.2)fo=Math.max(fo,.3*(1-left/.2));
    document.getElementById('flash').style.opacity=fo;
    const pg=document.getElementById('prog');pg.style.display='block';pg.firstChild.style.width=(100*Math.min(1,t/TOTAL))+'%';}
  s.style.transform='translate('+sx+'px,'+sy+'px) scale('+sc+')'+extra;s.style.opacity=v3?1:.4+.6*ent;
  const lt0=lt;{const lt=v3&&i===0?lt0+.3:lt0;
  s.querySelectorAll('[data-fx]').forEach(e=>{const at=+e.dataset.at,fx=e.dataset.fx,rot=+(e.dataset.rot||0);
    let p=cl((lt-at)/.45),tf='',op=1;
    if(fx==='drop'){tf='translateY('+(-1700*(1-E.outBounce(cl((lt-at)/.7))))+'px)'}
    else if(fx==='pop'){const q=cl((lt-at)/.38);tf='scale('+Math.max(0,E.outBack(q))+')';op=q>0?1:0}
    else if(fx==='stamp'){const q=cl((lt-at)/.3);tf='scale('+(2.6-1.6*E.outCubic(q))+')';op=q}
    else if(fx==='slideL'){tf='translateX('+(-1300*(1-E.outCubic(p)))+'px)'}
    else if(fx==='slideR'){tf='translateX('+(1300*(1-E.outCubic(p)))+'px)'}
    else if(fx==='zoomin'){tf='scale('+(1+.08*lt/2)+')'}
    else if(fx==='word'){const q=cl((lt-at)/.18);tf='scale('+(q?E.outBack(q):0)+') translateY('+(20*(1-q))+'px)';op=q?1:0}
    else if(fx==='write'){const q=cl((lt-at)/.7);e.style.clipPath='inset(-40% '+(100-100*q)+'% -40% -5%)'}
    else if(fx==='twinkle'){const q=cl((lt-at)/.3);tf='scale('+(q*(1+.25*Math.sin(lt*12+at*9)))+') rotate('+(lt*90)+'deg)';op=q}
    else if(fx==='print'){const q=cl((lt-at)/1.3);tf='translateY('+(900-760*E.outCubic(q))+'px)';e.style.clipPath='inset(0 0 '+Math.max(0,(1-q)*100-10)+'% 0)'}
    else if(fx==='kin'){const q=cl((lt-at)/.16);tf='scale('+(q?E.outBack(q):0)+') translateY('+(30*(1-q))+'px) rotate('+(rot*(1-q)*3)+'deg)';op=q?1:0}
    else if(fx==='sticker'){const q=cl((lt-at)/.3),d=Math.max(0,lt-at);tf='scale('+(q?E.outBack(q)*(1+.05*Math.sin(d*11)):0)+') rotate('+(10*Math.sin(d*7)*Math.exp(-d*2.5))+'deg)';op=q?1:0}
    else if(fx==='slam'){const q=cl((lt-at)/.2);tf='scale('+(3.4-2.4*E.outCubic(q))+')';op=q>0?1:0}
    else if(fx==='strike'){const q=cl((lt-at)/.25);e.style.clipPath='inset(-20% '+(100-100*q)+'% -20% 0)'}
    else if(fx==='punchin'){const q=cl((lt-at)/.25);tf='scale('+(1.18-.18*E.outCubic(q)+.04*lt)+')';op=q>0?1:0}
    if(e.dataset.until&&lt>=+e.dataset.until)op=0;
    let fl='';if(e.dataset.float==='1'){fl=' translateY('+(Math.sin(lt*2.4)*10)+'px) rotate('+(Math.sin(lt*1.7)*1.2)+'deg)'}
    e.style.transform=tf+' rotate('+rot+'deg)'+fl;e.style.opacity=op;e.style.transformOrigin='50% 50%';});}
  // snow
  if(snow){document.querySelectorAll('.flake').forEach((f,k)=>{const sp=60+(k*37)%120,x0=(k*173)%1080,y0=(k*311)%1920;
    f.style.transform='translate('+((x0+Math.sin(t*1.3+k)*40)%1080)+'px,'+((y0+sp*t)%2000-60)+'px)'})}
};`;

(async () => {
  const only = process.argv[2];
  const b = await chromium.launch();
  const page = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const [name, ad] of Object.entries(ADS)) {
    if (only && name !== only) continue;
    const snow = ad.snow !== 0;
    const flakes = snow ? Array.from({ length: 45 }, (_, k) => `<div class="flake" style="font-size:${18 + (k * 7) % 26}px">❄</div>`).join('') : '';
    const html = `<!doctype html><html><head><meta charset="utf-8">${FONTS}<style>${CSS}</style></head><body>
      ${ad.scenes.map(s => `<div class="scene ${s.bg}">${s.html}</div>`).join('')}<div class="snow">${flakes}</div>${ad.v3 ? '<div id="prog"><i></i></div><div id="flash"></div>' : ''}<script>${ENGINE}</script></body></html>`;
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const dir = path.join(TT, 'frames', name);
    fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    const shakes = ad.scenes.map(s => s.shake ? 1 : 0);
    const durs = ad.scenes.map(s => s.dur || SCENE);
    const total = +durs.reduce((a, b) => a + b, 0).toFixed(3), N = Math.round(total * FPS);
    const v3 = ad.v3 ? { beat: BEAT3 } : null;
    for (let f = 0; f < N; f++) {
      await page.evaluate(([t, D, sh, sn, v]) => window.render(t, D, sh, sn, v), [f / FPS, durs, shakes, snow, v3]);
      await page.screenshot({ path: path.join(dir, String(f).padStart(4, '0') + '.jpg'), type: 'jpeg', quality: 88 });
    }
    const out = path.join(TT, `DoodleDesignAndCo-TikTok-${name}.mp4`);
    // v3: sound effects on cuts (whoosh), hook (boom) and any per-scene cues (ding on price, pop on stickers)
    const cues = [];
    if (ad.v3) { let t0 = 0; ad.scenes.forEach((s, k) => { cues.push([k ? 'whoosh' : 'boom', Math.max(0, t0 - (k ? .08 : 0))]); (s.sfx || []).forEach(([n, at]) => cues.push([n, t0 + at])); t0 += durs[k]; }); }
    const sfxIn = cues.flatMap(([n]) => ['-i', path.join(TT, `sfx-${n}.wav`)]);
    const vol = { whoosh: .35, boom: .7, ding: .55, pop: .4 };
    const mix = cues.length ? cues.map(([n, at], k) => `[${k + 2}:a]adelay=${Math.round(at * 1000)}|${Math.round(at * 1000)},volume=${vol[n]}[s${k}];`).join('') +
      `[1:a]volume=0.8[m];[m]${cues.map((_, k) => `[s${k}]`).join('')}amix=inputs=${cues.length + 1}:normalize=0:duration=first,atrim=0:${total},afade=t=out:st=${(total - .6).toFixed(3)}:d=0.6[a]`
      : `[1:a]atrim=0:${total},afade=t=out:st=${total - 1}:d=1[a]`;
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(dir, '%04d.jpg'),
      '-i', path.join(TT, ad.music), ...sfxIn, '-filter_complex', mix,
      '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out]);
    console.log('built', name, total + 's');
  }
  await b.close();
})();
