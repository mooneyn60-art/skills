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
.bg-sagedk{background:linear-gradient(160deg,#8a9a82,#5f7059)}`;

// ---------- element helpers (fx = entrance effect, at = start time within scene) ----------
const el = (html, o) => `<div class="el ${o.cls || ''}" data-fx="${o.fx || 'none'}" data-at="${o.at || 0}" data-rot="${o.rot || 0}" data-float="${o.float ? 1 : 0}" style="left:${o.x}px;top:${o.y}px;${o.w ? `width:${o.w}px;` : ''}${o.style || ''}">${html}</div>`;
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

// ---------- in-page animation engine ----------
const ENGINE = `
const E={outBack:p=>1+2.7*Math.pow(p-1,3)+1.7*Math.pow(p-1,2),outCubic:p=>1-Math.pow(1-p,3),
 outBounce:p=>{const n=7.5625,d=2.75;if(p<1/d)return n*p*p;if(p<2/d)return n*(p-=1.5/d)*p+.75;if(p<2.5/d)return n*(p-=2.25/d)*p+.9375;return n*(p-=2.625/d)*p+.984375}};
const cl=(v)=>Math.max(0,Math.min(1,v));
window.render=(t,SCENE,shakes,snow)=>{
  const scenes=[...document.querySelectorAll('.scene')];const i=Math.min(scenes.length-1,Math.floor(t/SCENE));const lt=t-i*SCENE;
  scenes.forEach((s,k)=>s.style.display=k===i?'block':'none');const s=scenes[i];
  // scene entrance: quick zoom-punch; slow push-in; hook shake
  const ent=cl(lt/.22);let sc=1.12-.12*E.outCubic(ent)+.035*lt/SCENE;let sx=0,sy=0;
  if(shakes[i]&&lt>.35&&lt<.75){sx=Math.sin(lt*90)*14*(.75-lt);sy=Math.cos(lt*70)*10*(.75-lt)}
  s.style.transform='translate('+sx+'px,'+sy+'px) scale('+sc+')';s.style.opacity=.4+.6*ent;
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
    let fl='';if(e.dataset.float==='1'){fl=' translateY('+(Math.sin(lt*2.4)*10)+'px) rotate('+(Math.sin(lt*1.7)*1.2)+'deg)'}
    e.style.transform=tf+' rotate('+rot+'deg)'+fl;e.style.opacity=op;e.style.transformOrigin='50% 50%';});
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
      ${ad.scenes.map(s => `<div class="scene ${s.bg}">${s.html}</div>`).join('')}<div class="snow">${flakes}</div><script>${ENGINE}</script></body></html>`;
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const dir = path.join(TT, 'frames', name);
    fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    const shakes = ad.scenes.map(s => s.shake ? 1 : 0);
    const total = ad.scenes.length * SCENE, N = Math.round(total * FPS);
    for (let f = 0; f < N; f++) {
      await page.evaluate(([t, S, sh, sn]) => window.render(t, S, sh, sn), [f / FPS, SCENE, shakes, snow]);
      await page.screenshot({ path: path.join(dir, String(f).padStart(4, '0') + '.jpg'), type: 'jpeg', quality: 88 });
    }
    const out = path.join(TT, `DoodleDesignAndCo-TikTok-${name}.mp4`);
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(dir, '%04d.jpg'),
      '-i', path.join(TT, ad.music), '-filter_complex', `[1:a]atrim=0:${total},afade=t=out:st=${total - 1}:d=1[a]`,
      '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out]);
    console.log('built', name, total + 's');
  }
  await b.close();
})();
