// "Variety pack" video formats (Nov 19 owner feedback: grab the eye, NOT the same template + sound every time).
// Each video is ONE timeline page with its own look, palette, fonts, motion style and soundtrack.
// Deterministic frame-by-frame render (Playwright) -> JPEG frames -> numpy mix (src/mix-audio.py) -> ffmpeg.
// Usage: node src/build-formats.js [name ...]      (no name = build all)
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { execFileSync } = require('child_process');
const A = require('./art');
const ROOT = path.join(__dirname, '..');
const TT = path.join(ROOT, 'tiktok');
const FPS = 30;
const img = f => 'data:image/png;base64,' + fs.readFileSync(path.join(ROOT, 'listing-images', 'previews', f)).toString('base64');
const esc = s => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');

const FONTS = `<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Caveat:wght@700&family=Inter:wght@400;500;600;800&family=Special+Elite&family=Bangers&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Mountains+of+Christmas:wght@700&family=Nunito:wght@700;900&display=block" rel="stylesheet">`;
const CSS = `*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1920px;overflow:hidden;font-family:Fredoka;position:relative}
.el{position:absolute}.fl{position:relative}.paper{background:#fff;box-shadow:0 26px 60px rgba(0,0,0,.33)}.paper img{width:100%;display:block}
.pill{display:inline-block;border-radius:26px;padding:10px 34px;font-weight:700;white-space:nowrap}
.caret{display:inline-block;margin-left:2px}`;

// ---------- element helper: everything is placed on ONE global timeline ----------
// o: x,y,w,h, t0 (appear), t1 (disappear), fx (entrance), d (entrance secs), out ('fade'|'flipup'|'slideUp'), od,
//    rot, float, kf [[t,dx,dy,scale,rot],...] (absolute times), cls, style, attrs
const E = (html, o = {}) => `<div class="${o.flow ? 'fl' : 'el'} ${o.cls || ''}" data-t0="${o.t0 ?? 0}"${o.t1 != null ? ` data-t1="${o.t1}"` : ''} data-fx="${o.fx || 'none'}" data-d="${o.d || .35}" data-rot="${o.rot || 0}"${o.float ? ' data-float="1"' : ''}${o.out ? ` data-out="${o.out}" data-od="${o.od || .4}"` : ''}${o.kf ? ` data-kf="${esc(JSON.stringify(o.kf))}"` : ''} ${o.attrs || ''} style="${o.x != null ? `left:${o.x}px;` : ''}${o.y != null ? `top:${o.y}px;` : ''}${o.w ? `width:${o.w}px;` : ''}${o.h ? `height:${o.h}px;` : ''}${o.z ? `z-index:${o.z};` : ''}${o.style || ''}">${html}</div>`;
const P = (bg, inner, o = {}) => E(inner, { x: 0, y: 0, w: 1080, h: 1920, fx: 'fade', d: .25, ...o, style: `background:${bg};overflow:hidden;${o.style || ''}` });
const IMG = (f, o = {}) => E(`<img src="${img(f)}">`, { ...o, cls: `paper ${o.cls || ''}`, style: `${o.radius ? `border-radius:${o.radius}px;overflow:hidden;` : ''}${o.style || ''}` });
// Text block. f: font css, s: size, c: color, a: align
const TX = (html, o = {}) => E(html, { x: 60, w: 960, ...o, style: `font-family:${o.f || 'Fredoka'};font-size:${o.s || 60}px;color:${o.c || '#fff'};text-align:${o.a || 'center'};font-weight:${o.wt || 700};line-height:${o.lh || 1.15};${o.style || ''}` });
// Typewriter text (left-aligned so it doesn't jump)
const TYPE = (text, o = {}) => E(`<span class="tx"></span><span class="caret" style="opacity:0">${o.caret || '|'}</span>`, { fx: 'type', d: 99, ...o, attrs: `data-text="${esc(text)}" data-cps="${o.cps || 16}"`, style: `font-family:${o.f || 'Inter'};font-size:${o.s || 56}px;color:${o.c || '#111'};font-weight:${o.wt || 500};line-height:${o.lh || 1.2};white-space:${o.ws || 'normal'};${o.style || ''}` });
const typeDone = (text, t0, cps = 16) => t0 + [...text].length / cps;
const pillE = (t, bg, c, s, o = {}) => E(`<div class="pill" style="background:${bg};color:${c};font-size:${s}px;${o.pstyle || ''}">${t}</div>`, { x: 0, w: 1080, style: 'text-align:center', fx: 'pop', ...o });

// ---------- shared end card: price + orange "Shop on Etsy" + shop name + search phrase + link in bio ----------
const endCard = (t0, o) => P(o.bg, `
  ${TX(o.l1, { y: 250, s: o.l1s || 80, f: o.font || 'Fredoka', c: o.c || '#fff', t0: t0 + .1, fx: 'pop' })}
  ${pillE(o.price, o.pbg || '#FFD93D', o.pc || '#111', 58, { y: 500, t0: t0 + .25 })}
  ${E(`<div style="display:inline-block;background:#F1641E;color:#fff;font-family:Fredoka;font-weight:700;font-size:100px;padding:20px 60px;border-radius:30px;box-shadow:0 12px 0 rgba(0,0,0,.25)">Shop on Etsy</div>`, { x: 0, w: 1080, y: 650, style: 'text-align:center', t0: t0 + .4, fx: 'stamp', float: 1 })}
  ${pillE('DoodleDesignAndCo', '#fff', '#111', 54, { y: 880, t0: t0 + .6, pstyle: 'font-family:Fredoka' })}
  ${TX(o.search, { y: 1010, s: 50, c: o.c || '#fff', t0: t0 + .75, fx: 'up', f: 'Fredoka' })}
  ${TX('🔗 link in bio', { y: 1160, s: 76, c: o.c || '#fff', t0: t0 + .95, fx: 'pop', f: 'Fredoka' })}`, { t0, fx: o.fx || 'fade', d: o.d || .3, z: 30 });
const endCues = t0 => [['whoosh', t0 - .05, .3], ['pop', t0 + .4, .45], ['pop', t0 + .95, .4]];

const V = {};

// =====================================================================================
// 1. TEXTING SANTA — iMessage-style chat, cozy lo-fi beat, send/receive blips + typing clicks -> Santa Mail Set
// =====================================================================================
const mkChat = (NAME, c = {}) => {
  const msgs = c.msgs || [  // [side, html, time, dotsFrom]
    ['R', 'Santa… are you even real?? 🤨', .5],
    ['L', 'Ho ho ho! 🎅 Very real. And I have a surprise for you…', 2.3, 1.3],
    ['R', 'WHAT surprise 😳😳', 3.6],
    ['L', 'A letter. From me. With <b>YOUR</b> name on it ✉️', 5.1, 4.3],
    ['L', `<img src="${img('reply-from-santa-letter.png')}" style="width:420px;display:block;border-radius:24px"><div style="font-size:30px;color:#555;margin-top:10px">📎 Letter_from_Santa.pdf</div>`, 6.2, null, 1],
    ['R', 'MOM!!! 😭😭😭', 7.4],
    ['L', 'Tell her it prints in 2 minutes 😉🖨️', 8.7, 8.0],
  ];
  const bubble = (side, html, t, att) => E(html, { flow: 1, t0: t, fx: 'pop', d: .3, style: `max-width:760px;padding:${att ? '16px' : '22px 34px'};border-radius:44px;font-family:Inter;font-weight:500;font-size:54px;line-height:1.25;${side === 'R' ? `background:${c.blue || '#2f7cf6'};color:#fff;`+'transform-origin:100% 100%' : 'background:#e5e5ea;color:#111;transform-origin:0 100%'}` });
  const dots = (a, b) => E(`<span class="dot">●</span><span class="dot">●</span><span class="dot">●</span>`, { x: 0, y: 0, t0: a, t1: b, fx: 'pop', d: .2, style: 'background:#e5e5ea;color:#8e8e93;font-size:30px;padding:22px 30px;border-radius:40px;letter-spacing:6px' });
  const chat = msgs.map(([s, h, t, d, att]) => `<div class="slot" data-ta="${d ?? t}" style="position:relative;display:flex;justify-content:${s === 'R' ? 'flex-end' : 'flex-start'};margin-bottom:22px">${bubble(s, h, t, att)}${d != null ? dots(d, t) : ''}</div>`).join('');
  const T0 = 9.9, T1 = 12.4, TE = 14.0;
  V[NAME] = {
    music: c.music || 'xmas-lofi.wav', musicVol: .75, dur: 18.0,
    html: `${P('#f2f2f7', '', { fx: 'none' })}
    ${E(`<div style="width:110px;height:110px;border-radius:50%;background:${c.avBg || 'linear-gradient(#ff8a8a,#d7263d)'};margin:0 auto;font-size:70px;line-height:110px;text-align:center">${c.av || '🎅'}</div><div style="text-align:center;font-family:Inter;font-weight:600;font-size:40px;color:#111;margin-top:8px">${c.who || 'Santa Claus'}</div><div style="text-align:center;font-family:Inter;font-size:28px;color:#8e8e93">North Pole · online</div>`, { x: 0, y: 160, w: 1080, h: 260, style: 'background:#f9f9fb;border-bottom:2px solid #ddd;padding-top:20px' })}
    ${E(`<div id="chat" style="padding:30px 44px">${chat}</div>`, { x: 0, y: 420, w: 1080, h: 820, style: 'overflow:hidden' })}
    ${E(`<div style="display:flex;align-items:center;gap:20px"><div style="flex:1;border:3px solid #d1d1d6;border-radius:40px;padding:16px 30px;font-family:Inter;font-size:38px;color:#b0b0b5;background:#fff">Message</div><div style="width:72px;height:72px;border-radius:50%;background:${c.blue || '#2f7cf6'};color:#fff;font-size:44px;text-align:center;line-height:72px">↑</div></div>`, { x: 44, y: 1270, w: 992 })}
    ${E(`<div style="display:inline-block;max-width:940px;background:#FFD93D;color:#111;font-family:Fredoka;font-weight:700;font-size:78px;line-height:1.1;padding:20px 40px;border-radius:30px;box-shadow:0 10px 0 rgba(0,0,0,.18)">${c.hook || 'I texted Santa…<br>he ANSWERED 😳'}</div>`, { x: 0, w: 1080, y: 190, style: 'text-align:center', t0: -.3, t1: 3.3, fx: 'pop', rot: -2, z: 10 })}
    ${P(c.zbg || 'radial-gradient(circle at 50% 35%,#24386e,#0b1022)', `
      ${c.zoom || `${IMG('reply-from-santa-letter.png', { x: -210, y: 330, w: 1500, fx: 'none' })}
      ${E(`<span style="font-family:Caveat;font-size:120px;color:#1d4fa0">Emma</span>`, { x: 250, y: 845, t0: T0 + .3, fx: 'write', d: .7, rot: -3 })}`}
      ${pillE(c.zt || 'Santa wrote back ✉️', '#fff', '#111', 64, { y: 200, t0: T0 + .05, fx: 'slam', d: .2 })}
      ${pillE(c.zp || '$7.99 · 5-piece Santa Mail Set', '#FFD93D', '#111', 58, { y: 1260, t0: T0 + .6 })}`, { t0: T0, t1: T1, fx: 'slideR', d: .3, z: 20 })}
    ${P(c.blue || '#2f7cf6', `
      ${TX(c.p2t || '+ Nice List, elf letter, wish list & Dear Santa 🎄', { y: 210, s: 62, t0: T1 + .05, fx: 'up' })}
      ${(c.p2f || ['nice-list-certificate.png', 'christmas-elf-arrival-letter.png', 'christmas-wish-list.png', 'dear-santa.png']).map((f, k) => IMG(f, { x: [70, 560, 90, 560][k], y: [520, 470, 900, 880][k], w: f.startsWith('nice') ? 470 : 420, rot: [-6, 5, 4, -5][k], t0: T1 + .15 + k * .25, fx: 'pop' })).join('')}`, { t0: T1, t1: TE + .3, fx: 'slideL', d: .25, z: 21 })}
    ${endCard(TE, c.end || { bg: 'linear-gradient(170deg,#2f7cf6,#1b4fb8)', l1: 'Their face when Santa writes back 🥹', price: '$7.99 · instant download', search: 'search “Santa Mail Set” on Etsy', fx: 'up' })}`,
    custom: `
      if(!window.SL){const H=820-60;window.SL=[...document.querySelectorAll('.slot')].map(s=>({ta:+s.dataset.ta,tg:Math.max(0,s.offsetTop+s.offsetHeight-H)}));}
      let cur=0;for(const s of SL){if(T<s.ta)break;cur=cur+(s.tg-cur)*E.outCubic(cl((T-s.ta)/.3));}
      document.getElementById('chat').style.transform='translateY('+(-cur)+'px)';
      document.querySelectorAll('.dot').forEach((d,k)=>d.style.opacity=.35+.65*Math.max(0,Math.sin(T*9-k*1.1)));`,
    cues: [...msgs.flatMap(([sd, , t, d]) => [[sd === 'R' ? 'send' : 'recv', t, sd === 'R' ? .55 : .6], ...(d != null ? [['typing', d, .18]] : [])]), ['whoosh', T0 - .05, .4], ['ding', T0 + .6, .5], ['paper', T1, .4], ...endCues(TE)],
  };
};
mkChat('text-santa');

// =====================================================================================
// 2. NOTES-APP CHECKLIST — "Christmas Eve box checklist", upbeat pop drums, typing + check ticks -> Christmas Eve Box Pack
// =====================================================================================
const mkNotes = (NAME, c = {}) => {
  const items = c.items || ['🧦 new pajamas', '🍫 hot cocoa + a mug', '🎬 a Christmas movie', '📖 a new book', '🦌 magic reindeer food', '🍪 note for Santa’s cookies', '🗝️ Santa’s magic key'];
  const tA = k => .5 + k * .5, tick = [4.2, 4.6, 5.0, 5.4], TW = 6.0, TP = 7.6, TPR = 10.9, TE = 12.6;
  const rows = items.map((it, k) => {
    const y = 520 + k * 100;
    return `${E('', { x: 70, y: y + 6, w: 54, h: 54, t0: tA(k), fx: 'pop', style: 'border:4px solid #c9c2ad;border-radius:50%' })}
      ${TYPE(it, { x: 150, y, w: 820, s: 52, t0: tA(k), cps: 40, ws: 'nowrap', c: '#2b2b2b' })}
      ${k < 4 ? `${E('✓', { x: 70, y: y + 6, w: 54, h: 54, t0: tick[k], fx: 'tick', d: .25, style: 'background:#f2a900;border-radius:50%;color:#fff;font-family:Inter;font-weight:800;font-size:38px;text-align:center;line-height:54px' })}
        ${E('', { x: 150, y: y + 32, w: 560, h: 5, t0: tick[k] + .05, fx: 'wipe', d: .25, style: 'background:#8d8774;border-radius:3px' })}`
      : E('?', { x: 70, y: y + 6, w: 54, h: 54, t0: TW, fx: 'tick', d: .25, style: 'background:#ff4d4d;border-radius:50%;color:#fff;font-family:Inter;font-weight:800;font-size:38px;text-align:center;line-height:54px' })}`;
  }).join('');
  const pages = c.pages || ['ceb-1.png', 'ceb-2.png', 'ceb-3.png', 'ceb-4.png', 'ceb-5.png'], labels = c.labels || ['box labels ✔', 'reindeer food tags ✔', 'cookies for Santa ✔', 'Santa’s magic key ✔', 'night-before checklist ✔'];
  const tp = k => TP + .3 + k * .55;
  V[NAME] = {
    music: c.music || 'xmas-popdrums.wav', musicVol: .7, dur: 16.6,
    html: `${P('repeating-linear-gradient(#fdfbf3 0 98px,#ece6d2 98px 100px)', '', { fx: 'none' })}
    ${E(`<span style="color:#d99a00">‹ Notes</span><span style="float:right;color:#d99a00">Done</span>`, { x: 60, y: 175, w: 960, style: 'font-family:Inter;font-weight:500;font-size:42px' })}
    ${TX(c.title || 'Christmas Eve box checklist 🎁', { x: 70, y: 250, w: 940, a: 'left', s: 76, c: '#1d1d1d', f: 'Inter', wt: 800, t0: -.3, fx: 'pop' })}
    ${TX(c.sub || '(the thing EVERYONE forgets 👀)', { x: 70, y: 430, w: 940, a: 'left', s: 42, c: '#8a8370', f: 'Inter', wt: 500, t0: .15, fx: 'fade' })}
    ${rows}
    ${E(`<div class="pill" style="background:#ff4d4d;color:#fff;font-family:Inter;font-weight:800;font-size:58px;padding:20px 36px;box-shadow:0 10px 0 rgba(0,0,0,.2)">${c.wait || 'WAIT… I forgot the PRINTABLES 😱'}</div>`, { x: 0, w: 1080, y: 1262, style: 'text-align:center', t0: TW + .1, fx: 'slam', d: .2, rot: -3 })}
    ${P(c.pbg || 'radial-gradient(circle at 50% 30%,#fff0f3,#ffc9d6)', `
      ${TX(c.ptitle || 'Christmas Eve Box Pack 🎁', { y: 200, s: 64, c: c.accent || '#b3123a', f: 'Inter', wt: 800, t0: TP + .05, fx: 'down' })}
      ${labels.map((l, k) => pillE(l, '#fff', c.accent || '#b3123a', 50, { y: 320, t0: tp(k), t1: k < 4 ? tp(k + 1) : TE, pstyle: 'font-family:Inter;font-weight:800' })).join('')}
      ${pages.map((f, k) => IMG(f, { x: [60, 330, 600, 190, 470][k], y: [430, 450, 430, 800, 820][k], w: 420, rot: [-6, 3, 7, -3, 5][k], t0: tp(k), fx: ['slideL', 'drop', 'slideR', 'slideL', 'slideR'][k], d: .3 })).join('')}
      ${E(`<div style="width:330px;height:330px;border-radius:50%;background:#FFD93D;box-shadow:0 14px 0 rgba(0,0,0,.2);text-align:center;font-family:Inter;color:#111;padding-top:70px"><div style="font-size:110px;font-weight:800;line-height:1">${c.price || '$3.99'}</div><div style="font-size:34px;font-weight:600">${c.priceSub || 'all 5 pages'}</div></div>`, { x: 680, y: 1000, t0: TPR, fx: 'stamp', rot: 8 })}
      ${pillE('instant download · print tonight ⚡', c.accent || '#b3123a', '#fff', 46, { y: 1350, t0: TPR + .3, pstyle: 'font-family:Inter;font-weight:800' })}`, { t0: TP, t1: TE + .3, fx: 'slideL', d: .3 })}
    ${endCard(TE, c.end || { bg: '#ffd84d', c: '#222', l1: 'Christmas Eve box: DONE ✅', price: '$3.99 · 5 printable pages', pbg: '#fff', search: 'search “Christmas Eve Box printable” on Etsy', fx: 'up' })}`,
    cues: [['pop', 0, .4], ['typing', .5, .3], ['typing', 2.1, .3], ...tick.map(t => ['check', t, .6]), ['scratch', TW, .7], ['boom', TW + .1, .4], ['whoosh', TP, .4], ...pages.map((_, k) => ['paper', tp(k), .45]), ['ding', TPR, .55], ...endCues(TE)],
  };
};
mkNotes('notes-evebox');

// =====================================================================================
// 3. RATING METER — "Rating our printables 1–10", purple neon, comedic pizzicato, rising meter SFX -> range of products
// =====================================================================================
const mkRating = (NAME, c = {}) => {
  const S = [2.2, 4.8, 7.4, 10.0], TE = 13.4;
  const items = c.items || [
    { n: 'Holly Jolly wall art', p: '$2.99', s: 7, why: 'cute… but the kids don’t care 😅', imgs: [['hj.png', 290, 380, 500, 0]] },
    { n: 'Coloring book (20 pages)', p: '$3.99', s: 9, why: '20 minutes of QUIET ☕', imgs: [['cb-01.png', 140, 400, 400, -5], ['cb-06.png', 540, 380, 400, 5]] },
    { n: 'Nice List certificate', p: '$3.29', s: 10, why: 'their face when they read it 🥹', imgs: [['nice-list-certificate.png', 130, 430, 820, -2]] },
    { n: 'Santa Mail Set (5 pages)', p: '$7.99', s: 11, why: 'it broke the meter 🤯', imgs: [['dear-santa.png', 60, 420, 400, -8], ['reply-from-santa-letter.png', 340, 380, 400, 0], ['christmas-elf-arrival-letter.png', 620, 420, 400, 8]] },
  ];
  const seg = (it, k) => {
    const s = S[k], e = k < 3 ? S[k + 1] : TE, fx = ['slideR', 'slideL', 'drop', 'stamp'][k];
    return `${TX(`#${k + 1} · ${it.n}`, { y: 210, s: 66, f: 'Bangers', wt: 400, t0: s, t1: e, fx: 'down', style: 'letter-spacing:2px;text-shadow:0 6px 0 #ff3ea5' })}
      ${it.imgs.map(([f, x, y, w, r], j) => f.endsWith('.png') ? IMG(f, { x, y, w, rot: r, t0: s + j * .1, t1: e, fx, d: .3 }) : E(`<span style="font-size:${w}px">${f}</span>`, { x, y, rot: r, t0: s + j * .1, t1: e, fx, d: .3 })).join('')}
      ${it.p ? E(`<div class="pill" style="background:#FFD93D;color:#111;font-family:Bangers;font-weight:400;font-size:76px;padding:6px 30px">${it.p}</div>`, { x: 700, y: 330, t0: s + .3, t1: e, fx: 'stamp', rot: 10, z: 5 }) : ''}
      ${E('', { x: 110, y: 1150, w: 860, h: 70, t0: s, t1: e, style: 'background:rgba(255,255,255,.18);border-radius:35px;border:4px solid rgba(255,255,255,.5)' })}
      ${E('', { x: 110, y: 1150, w: 0, h: 70, t0: s + .5, t1: e, fx: 'fill', d: 1.0, attrs: `data-to="${it.s >= 10 ? 100 : it.s * 10}" data-W="860"`, style: 'border-radius:35px;background:linear-gradient(90deg,#3dff9e,#ffe14d,#ff3ea5);box-shadow:0 0 30px rgba(255,62,165,.7)' })}
      ${E('', { x: 110, y: 1250, t0: s + .5, t1: e, fx: 'count', d: 1.0, attrs: `data-from="0" data-to="${it.s}" data-suf="/10"`, style: 'font-family:Bangers;font-size:120px;color:#fff;line-height:1;text-shadow:0 6px 0 #ff3ea5' })}
      ${TX(it.why, { x: 430, y: 1262, w: 520, a: 'left', s: 46, f: 'Nunito', wt: 900, t0: s + 1.5, t1: e, fx: 'pop', lh: 1.1 })}
      ${k === 3 ? E('<span style="font-size:190px">💥</span>', { x: 830, y: 1080, t0: s + 1.5, t1: e, fx: 'pop', z: 6 }) : ''}`;
  };
  V[NAME] = {
    music: c.music || 'xmas-pizzicato.wav', musicVol: .75, dur: 17.6,
    html: `${P(c.bg || 'linear-gradient(160deg,#2a1458,#6b2fa0)', '', { fx: 'none' })}
    ${E('', { x: 0, y: 0, w: 1080, h: 1920, style: 'background:radial-gradient(circle at 20% 15%,rgba(255,62,165,.25),transparent 40%),radial-gradient(circle at 85% 70%,rgba(61,255,158,.18),transparent 45%)' })}
    ${TX(c.title || 'Rating our Christmas printables 1–10 😬', { y: 210, s: 100, f: 'Bangers', wt: 400, t0: -.3, t1: S[0], fx: 'slam', d: .2, style: 'letter-spacing:2px;text-shadow:0 7px 0 #ff3ea5' })}
    ${TX('(brutally honest)', { y: 470, s: 50, f: 'Nunito', wt: 900, c: '#ffe14d', t0: .3, t1: S[0], fx: 'pop' })}
    ${(c.hookImgs || ['hj.png', 'cb-01.png', 'nice-list-certificate.png', 'reply-from-santa-letter.png']).map((f, k) => IMG(f, { x: [70, 560, 80, 540][k], y: [620, 600, 1040, 990][k], w: f.startsWith('nice') ? 460 : 380, rot: [-7, 6, 5, -4][k], t0: .1 * k - .2, t1: S[0], fx: 'pop' })).join('')}
    ${items.map(seg).join('')}
    ${endCard(TE, c.end || { bg: 'linear-gradient(160deg,#2a1458,#6b2fa0)', font: 'Bangers', l1s: 96, l1: 'Which one gets YOUR 10? 👇', price: 'from $2.99 · instant downloads', search: 'search “DoodleDesignAndCo” on Etsy', fx: 'stamp' })}`,
    cues: [['boom', 0, .6], ['pop', .3, .4], ...S.flatMap((s, k) => [['whoosh', s - .05, .35], ['rise', s + .5, .35], ['pop', s + 1.5, .4]]), ['boom', S[3] + 1.5, .7], ['tada', S[3] + 1.55, .45], ...endCues(TE)],
  };
};
mkRating('rating-meter');

// =====================================================================================
// 4. COMMENT REPLY — "Replying to: where do I get this??", pastel pink, "We Wish You a Merry Christmas" -> shop/bio/search how-to
// =====================================================================================
{
  const S1 = 2.4, S2 = 5.0, S3 = 7.6, TG = 9.3, TA = 10.8, TE = 12.6;
  const thumbs = [['reply-from-santa-letter.png', 'Santa Mail Set', '$7.99'], ['nice-list-certificate.png', 'Nice List', '$3.29'], ['cb-01.png', 'Coloring Book', '$3.99'], ['elfb-2.png', 'Elf Letters', '$4.99']];
  const phone = inner => E(`<div style="position:absolute;inset:18px;border-radius:52px;background:#fff;overflow:hidden">${inner}</div>`, { x: 230, y: 640, w: 620, h: 790, style: 'background:#1d1d1f;border-radius:70px;box-shadow:0 30px 60px rgba(120,20,60,.35)' });
  const profile = `
    <div style="text-align:center;padding-top:50px;font-family:Inter">
      <div style="width:150px;height:150px;border-radius:50%;margin:0 auto;background:#8a9a82;color:#fff;font-family:Fredoka;font-weight:700;font-size:48px;line-height:150px">D&amp;Co</div>
      <div style="font-weight:800;font-size:40px;margin-top:18px;color:#111">DoodleDesignAndCo</div>
      <div style="font-size:28px;color:#666;margin-top:6px">printable Christmas magic ✨</div>
      <div id="biolink" style="display:inline-block;margin-top:22px;font-weight:800;font-size:34px;color:#fff;background:#F1641E;border-radius:30px;padding:10px 30px">🔗 link in bio</div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:30px">${['reply-from-santa-letter.png', 'nice-list-certificate.png', 'cb-01.png', 'elfb-1.png', 'ceb-1.png', 'wl2.png'].map(f => `<div style="height:200px;background:url(${img(f)}) center/cover"></div>`).join('')}</div>
    </div>`;
  const search = `
    <div style="padding:60px 30px;font-family:Inter">
      <div style="position:relative;height:80px;border:3px solid #222;border-radius:40px;padding:16px 26px;font-size:34px;color:#111">🔍${TYPE('DoodleDesignAndCo', { x: 84, y: 16, s: 36, t0: S3 + .4, cps: 14, ws: 'nowrap', wt: 600 })}</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:34px">${thumbs.map(([f, n, p], k) => E(`<div style="height:230px;border-radius:20px;background:url(${img(f)}) center/cover #f4f4f4;border:2px solid #eee"></div><div style="font-size:26px;font-weight:600;color:#222;margin-top:6px">${n}</div><div style="font-size:30px;font-weight:800;color:#111">${p}</div>`, { flow: 1, t0: TG + k * .2, fx: 'pop' })).join('')}</div>
    </div>`;
  V['reply-comment'] = {
    music: 'xmas-wewish.wav', musicVol: .7, dur: 16.6,
    html: `${P('radial-gradient(#ffc2d1 12%,transparent 13%) 0 0/80px 80px,#ffe4ec', '', { fx: 'none' })}
    ${E(`<div style="display:flex;gap:22px;align-items:center"><div style="width:84px;height:84px;border-radius:50%;background:#d9d9de;flex:none;font-size:48px;text-align:center;line-height:84px">👤</div><div><div style="font-family:Inter;font-size:30px;color:#888;font-weight:500">Reply to a comment we get every day</div><div style="font-family:Inter;font-weight:800;font-size:56px;color:#111">where do I get this?? 😍🙏</div></div></div>`, { x: 90, y: 200, w: 900, t0: -.3, t1: TE, fx: 'pop', z: 6, style: 'background:#fff;border-radius:34px;padding:26px 34px;box-shadow:0 14px 30px rgba(180,40,90,.2)', rot: -1 })}
    ${TX('OK here’s EXACTLY where 👇', { y: 470, s: 72, c: '#c2185b', t0: .5, t1: S1, fx: 'pop', z: 6 })}
    ${['reply-from-santa-letter.png', 'nice-list-certificate.png', 'cb-06.png'].map((f, k) => IMG(f, { x: [110, 600, 360][k], y: [700, 690, 930][k], w: f.startsWith('nice') ? 400 : 360, rot: [-8, 7, -2][k], t0: .7 + k * .15, t1: S1, fx: 'drop', d: .6 })).join('')}
    ${TX('1️⃣ tap our name / profile 👆', { y: 470, s: 64, c: '#c2185b', t0: S1, t1: S2, fx: 'slideR' })}
    ${TX('2️⃣ tap the 🔗 link in our bio', { y: 470, s: 64, c: '#c2185b', t0: S2, t1: S3, fx: 'slideR' })}
    ${TX('3️⃣ or search on Etsy 🔍', { y: 470, s: 64, c: '#c2185b', t0: S3, t1: TA, fx: 'slideR' })}
    ${E(phone(profile), { x: 0, y: 0, t0: S1, t1: S3, fx: 'up', d: .35 })}
    ${E(phone(search), { x: 0, y: 0, t0: S3, t1: TA, fx: 'flipin', d: .35 })}
    ${E('<span style="font-size:130px">👆</span>', { x: 470, y: 900, t0: S1 + .4, t1: S3, kf: [[S1 + .4, 0, 0, 1, 0], [S1 + .7, 0, -20, .85, 0], [S1 + .9, 0, 0, 1, 0], [S2 + .2, 30, 210, 1, 0], [S2 + .5, 30, 190, .85, 0], [S2 + .7, 30, 210, 1, 0]], z: 8 })}
    ${P('radial-gradient(#ffc2d1 12%,transparent 13%) 0 0/80px 80px,#ffe4ec', `
      ${TX('everything is an instant download 📥', { y: 450, s: 70, c: '#c2185b', t0: TA, fx: 'pop' })}
      ${TX('print it TONIGHT ⚡ no shipping', { y: 640, s: 64, c: '#111', t0: TA + .3, fx: 'pop' })}
      ${pillE('from $2.99', '#FFD93D', '#111', 90, { y: 830, t0: TA + .55, fx: 'stamp' })}
      ${thumbs.map(([f], k) => IMG(f, { x: 90 + k * 225, y: 1060, w: f.startsWith('nice') ? 260 : 200, rot: [-6, 4, -3, 6][k], t0: TA + .7 + k * .1, fx: 'pop' })).join('')}`, { t0: TA, t1: TE + .3, fx: 'fade', d: .2, z: 5 })}
    ${endCard(TE, { bg: 'linear-gradient(170deg,#ff6f91,#e0457b)', l1: 'Now you know 😉 see you in the shop!', price: 'Santa Mail Set $7.99 · Nice List $3.29', search: 'search “DoodleDesignAndCo” on Etsy', fx: 'up' })}`,
    custom: `const b=document.getElementById('biolink');if(b){const on=T>${S2}&&T<${S3};b.style.transform='scale('+(on?1.08+.08*Math.sin(T*10):1)+')';b.style.boxShadow=on?'0 0 0 '+(8+6*Math.sin(T*10))+'px rgba(241,100,30,.35)':'none';}`,
    cues: [['pop', 0, .45], ['pop', .5, .35], ['whoosh', S1, .35], ['pop', S1 + .7, .45], ['whoosh', S2, .35], ['pop', S2 + .5, .45], ['whoosh', S3, .35], ['typing', S3 + .4, .3], ...[0, 1, 2, 3].map(k => ['pop', TG + k * .2, .3]), ['ding', TA + .55, .5], ...endCues(TE)],
  };
}

// =====================================================================================
// 5. COZY FIREPLACE — slow typewriter, "Silent Night" music box + fire crackle -> Letter from Santa
// =====================================================================================
{
  const cream = '#ffe9c7', glow = 'text-shadow:0 0 18px rgba(255,170,80,.55)';
  const L = [  // text, y, t0, groupEnd
    ['it’s 9pm.', 240, -.6, 6.6], ['the kids are finally asleep.', 370, 1.0, 6.6], ['and you forgot the letter from Santa. 😬', 600, 3.2, 6.6],
    ['breathe. ☕', 240, 7.0, 11.8], ['it’s a printable.', 370, 8.0, 11.8], ['add their name. print. done. ✨', 500, 9.2, 11.8],
  ];
  const TL = 12.2, TPR = 14.2, TE = 16.0, CPS = 15;
  const stocking = (x, c) => E(`<svg width="120" height="200" viewBox="0 0 120 200"><path d="M20 30 h60 v95 q0 20 20 30 q20 12 10 32 q-10 16 -40 6 l-40 -20 q-16 -10 -10 -30 z" fill="${c}"/><rect x="12" y="10" width="76" height="34" rx="10" fill="#fff6e8"/></svg>`, { x, y: 1100, z: 3 });
  const typeCues = L.flatMap(([t, , t0]) => [...t].map((_, i) => ['typewriter', t0 + i / CPS, .22]).filter(c => c[1] >= 0 && /\S/.test([...t][Math.round((c[1] - t0) * CPS)] || ' ')));
  V['cozy-fireplace'] = {
    music: 'xmas-musicbox.wav', musicVol: .8, dur: 20.0,
    html: `${P('#2e1a13', '', { fx: 'none' })}
    ${E('', { x: 0, y: 0, w: 1080, h: 1920, style: 'background:repeating-linear-gradient(0deg,transparent 0 76px,rgba(0,0,0,.35) 76px 80px),repeating-linear-gradient(90deg,transparent 0 156px,rgba(0,0,0,.3) 156px 160px);opacity:.6' })}
    ${E('', { x: 0, y: 0, w: 1080, h: 1920, attrs: 'id="glow"', style: 'background:radial-gradient(ellipse at 50% 82%,rgba(255,140,40,.55),rgba(255,100,20,.12) 45%,transparent 70%)' })}
    ${E('', { x: 160, y: 1130, w: 760, h: 790, style: 'background:#5a4034;border-radius:40px 40px 0 0;box-shadow:inset 0 0 0 14px #4a332a' })}
    ${E('<div id="fire" style="position:absolute;inset:0"></div>', { x: 280, y: 1250, w: 520, h: 670, style: 'background:#140806;border-radius:260px 260px 0 0;overflow:hidden' })}
    ${E('', { x: 70, y: 1060, w: 940, h: 74, style: 'background:linear-gradient(#7a4f31,#5b3a24);border-radius:12px;box-shadow:0 14px 30px rgba(0,0,0,.5)' })}
    ${Array.from({ length: 14 }, (_, k) => E('', { x: 95 + k * 65, y: 1040 + (k % 2) * 8, w: 22, h: 22, cls: 'bulb', style: `border-radius:50%;background:${['#ffcf5a', '#ff6b6b', '#7ee081', '#6bb8ff'][k % 4]}` })).join('')}
    ${stocking(200, '#c1121f')}${stocking(470, '#2f7d4f')}${stocking(740, '#c1121f')}
    ${L.map(([t, y, t0, g]) => TYPE(t, { x: 90, y, w: 900, s: 72, f: "'Special Elite'", c: cream, t0, t1: g, out: 'fade', od: .5, cps: CPS, wt: 400, style: glow })).join('')}
    ${TYPE('a letter back from Santa 🎅', { x: 90, y: 200, w: 900, s: 52, f: "'Special Elite'", c: cream, t0: TL + .2, t1: TE, cps: CPS, wt: 400, style: glow })}
    ${IMG('reply-from-santa-letter.png', { x: 250, y: 300, w: 580, t0: TL, t1: TE, fx: 'rise', d: 1.2, float: 1, style: 'box-shadow:0 0 60px rgba(255,170,80,.45)' })}
    ${E(`<span style="font-family:Caveat;font-size:52px;color:#1d4fa0">Emma</span>`, { x: 430, y: 500, t0: TL + 1.0, t1: TE, fx: 'write', d: .8 })}
    ${E(`<div style="background:#fff6e8;border-radius:16px;padding:16px 30px;font-family:'Special Elite';color:#5b2a12;text-align:center;box-shadow:0 12px 26px rgba(0,0,0,.4)"><div style="font-size:84px">$3.49</div><div style="font-size:34px">instant download</div></div>`, { x: 650, y: 820, t0: TPR, t1: TE, fx: 'pop', rot: 6, z: 6 })}
    ${endCard(TE, { bg: 'radial-gradient(circle at 50% 30%,#7a1f12,#2a0d08)', font: "'Special Elite'", c: cream, l1s: 70, l1: 'you’ve got this. ❤️ merry Christmas.', price: '$3.49 · print it tonight', pbg: cream, search: 'search “Letter from Santa printable” on Etsy', fx: 'fade', d: .8 })}`,
    custom: `
      const f=document.getElementById('fire');if(!f.children.length){for(let k=0;k<7;k++){const d=document.createElement('div');d.style.cssText='position:absolute;border-radius:50% 50% 40% 40%;filter:blur(6px);mix-blend-mode:screen';f.appendChild(d);}
        for(let k=0;k<14;k++){const d=document.createElement('div');d.className='ember';d.style.cssText='position:absolute;width:8px;height:8px;border-radius:50%;background:#ffb347';f.appendChild(d);}}
      [...f.children].forEach((d,k)=>{if(d.className==='ember'){const p=((T*.35+k*.13)%1);d.style.left=(120+((k*97)%280)+Math.sin(T*3+k)*20)+'px';d.style.top=(560-p*520)+'px';d.style.opacity=(1-p)*.9;return;}
        const w=[260,200,220,170,150,120,90][k],h=w*1.6*(1+.14*Math.sin(T*7.3+k*1.7)+.07*Math.sin(T*13+k)),x=260-w/2+[-120,110,0,-60,70,-10,30][k]+Math.sin(T*3+k)*8;
        d.style.width=w+'px';d.style.height=h+'px';d.style.left=x+'px';d.style.top=(560-h*.8)+'px';
        d.style.background='radial-gradient(ellipse at 50% 70%,'+['#ffd76a','#ffb347','#ff8c2b','#ff6a1a','#ffe08a','#fff1b8','#ffd76a'][k]+',rgba(255,80,0,.0) 70%)';});
      document.getElementById('glow').style.opacity=.75+.2*Math.sin(T*6.1)+.08*Math.sin(T*15.7);
      document.querySelectorAll('.bulb').forEach((b,k)=>{const o=.45+.55*Math.max(0,Math.sin(T*1.8+k*1.3));b.style.opacity=o;b.style.boxShadow='0 0 '+(10+16*o)+'px '+getComputedStyle(b).backgroundColor;});`,
    cues: [['crackle', 0, .5], ...typeCues, ['chime', TL, .35], ['chime', TPR, .4], ['chime', TE + .4, .3]],
  };
}

// =====================================================================================
// 6. ELF DAY-IN-THE-LIFE — vlog timestamps, mint + candy stripes, "Deck the Halls" -> Christmas Elf Letter Bundle
// =====================================================================================
{
  const S = [2.4, 4.6, 6.8, 9.0, 11.2], TPR = 13.4, TE = 15.4;
  const segs = [
    ['6:00 AM', 'cocoa + a cookie for breakfast ☕🍪', null],
    ['8:00 AM', 'writes the kids: “I’m HERE!” ✉️', 'elfb-1.png'],
    ['12:00 PM', 'a big “I’m BACK!” for returning elves 🎉', 'elfb-2.png'],
    ['3:00 PM', 'a gentle reminder to be kind 💚', 'elfb-4.png'],
    ['Christmas Eve', 'time to fly home with Santa 🛷', 'elfb-3.png'],
  ];
  const stripe = 'repeating-linear-gradient(45deg,#e63946 0 40px,#fff 40px 80px)';
  const stamp = (t, t0, t1) => E(`<div class="pill" style="background:#1f5f43;color:#fff;font-family:Inter;font-weight:800;font-size:46px;border-radius:18px;padding:8px 26px">⏰ ${t}</div>`, { x: 70, y: 190, t0, t1, fx: 'stamp', d: .2, z: 5 });
  V['elf-dayinlife'] = {
    music: 'xmas-deckhalls.wav', musicVol: .75, dur: 19.4,
    html: `${P('#dff7ec', '', { fx: 'none' })}
    ${E('', { x: 0, y: 0, w: 1080, h: 150, style: `background:${stripe}` })}${E('', { x: 0, y: 1480, w: 1080, h: 440, style: `background:${stripe}` })}
    ${TX('A day in the life of a North Pole elf 🧝', { y: 220, s: 96, f: "'Mountains of Christmas'", c: '#c1121f', t0: -.3, t1: S[0], fx: 'pop', lh: 1.05 })}
    ${TX('(busier than you think)', { y: 470, s: 46, c: '#1f5f43', f: 'Inter', wt: 800, t0: .4, t1: S[0], fx: 'fade' })}
    ${E(A.elf(2.6), { x: 290, y: 640, t0: -.2, t1: S[1], fx: 'pop', float: 1 })}
    ${segs.map(([ts, cap, f], k) => {
      const s = S[k], e = k < 4 ? S[k + 1] : TPR;
      return `${stamp(ts, s, e)}${TX(cap, { y: 310, s: 60, c: '#123d2b', f: 'Fredoka', t0: s + .1, t1: e, fx: 'up' })}
        ${f ? IMG(f, { x: 230, y: 480, w: 620, rot: [0, -3, 3, -2, 2][k], t0: s, t1: e, fx: ['', 'slideR', 'drop', 'slideL', 'flipin'][k], d: .35 }) : `${E('<span style="font-size:150px">☕</span>', { x: 130, y: 1080, t0: s + .3, t1: e, fx: 'pop', rot: -10 })}${E('<span style="font-size:150px">🍪</span>', { x: 760, y: 1060, t0: s + .5, t1: e, fx: 'pop', rot: 12 })}`}`;
    }).join('')}
    ${stamp('5:00 PM · mom prints them', TPR, TE)}
    ${TX('all 4 elf letters', { y: 310, s: 70, c: '#123d2b', t0: TPR + .05, t1: TE, fx: 'up' })}
    ${['elfb-1.png', 'elfb-2.png', 'elfb-3.png', 'elfb-4.png'].map((f, k) => IMG(f, { x: 40 + k * 245, y: 520 + (k % 2) * 60, w: 330, rot: -8 + k * 5, t0: TPR + .1 + k * .1, t1: TE, fx: 'pop' })).join('')}
    ${pillE('$4.99 · add their names ✍️', '#c1121f', '#fff', 64, { y: 1130, t0: TPR + .5, t1: TE, fx: 'stamp' })}
    ${endCard(TE, { bg: `linear-gradient(rgba(193,18,31,.9),rgba(193,18,31,.9)),${stripe}`, font: 'Fredoka', l1: 'Your elf’s whole season = DONE ✅', price: '$4.99 · 4 printable elf letters', search: 'search “Christmas Elf Letter Bundle” on Etsy', fx: 'slideL' })}`,
    cues: [['pop', 0, .4], ...S.map(s => ['shutter', s, .6]), ...S.slice(1).map(s => ['paper', s + .05, .4]), ['shutter', TPR, .6], ['ding', TPR + .5, .5], ...endCues(TE)],
  };
}

// =====================================================================================
// 7. NAUGHTY OR NICE QUIZ — split red/green game show, Santa-o-meter, game-show loop + buzzer/ding -> Nice List
// =====================================================================================
{
  const S = [2.0, 4.6, 7.2], TV = 9.8, TC = 11.2, TPR = 12.6, TE = 14.0;
  const Q = [['ate the cookie meant for Santa 🍪', -1], ['cleaned up WITHOUT being asked 🧹', 1], ['peeked at the presents 👀🎁', -1]];
  const q = ([text, side], k) => {
    const s = S[k], e = k < 2 ? S[k + 1] : TV, tx = side < 0 ? -330 : 330;
    return `${TX(text, { x: 90, y: 440, w: 900, s: 60, c: '#111', f: 'Fredoka', t0: s, t1: e, fx: 'pop', style: 'background:#fff;border-radius:30px;padding:30px 20px;box-shadow:0 12px 0 rgba(0,0,0,.25)' })}
      ${E('', { x: 90, y: 860, w: 900, h: 90, t0: s, t1: e, fx: 'fade', style: 'border-radius:45px;background:linear-gradient(90deg,#ff2d55,#ffd60a 50%,#30d158);border:6px solid #fff;box-shadow:0 10px 0 rgba(0,0,0,.3)' })}
      ${E('<div style="width:150px;height:150px;border-radius:50%;background:#fff;border:6px solid #111;font-size:96px;text-align:center;line-height:138px">🎅</div>', { x: 465, y: 830, t0: s, t1: e, kf: [[s + .3, 0, 0, 1, 0], [s + .55, -220, 0, 1, -20], [s + .85, 200, 0, 1, 20], [s + 1.1, -90, 0, 1, -8], [s + 1.5, tx, 0, 1.1, 0]] })}
      ${TX(side < 0 ? 'NAUGHTY 😈' : 'NICE 😇', { y: 1080, s: 130, f: 'Bangers', wt: 400, t0: s + 1.55, t1: e, fx: 'slam', d: .2, style: `text-shadow:0 8px 0 #111;color:${side < 0 ? '#ffd1d9' : '#d6ffe4'}` })}`;
  };
  V['naughty-nice'] = {
    music: 'xmas-gameshow.wav', musicVol: .65, dur: 18.0,
    html: `${P('linear-gradient(90deg,#e0233c 50%,#12a150 50%)', '', { fx: 'none' })}
    ${E('', { x: 0, y: 0, w: 1080, h: 1920, style: 'background:repeating-conic-gradient(from 0deg at 50% 45%,rgba(255,255,255,.07) 0 8deg,transparent 8deg 16deg)' })}
    ${TX('NAUGHTY', { x: 20, w: 520, y: 190, s: 104, f: 'Bangers', wt: 400, t0: -.3, fx: 'slam', d: .2, style: 'text-shadow:0 7px 0 #111;letter-spacing:3px' })}
    ${TX('NICE', { x: 540, w: 520, y: 190, s: 104, f: 'Bangers', wt: 400, t0: -.2, fx: 'slam', d: .2, style: 'text-shadow:0 7px 0 #111;letter-spacing:3px' })}
    ${E('<div style="width:110px;height:110px;border-radius:50%;background:#111;color:#ffd60a;font-family:Bangers;font-size:60px;text-align:center;line-height:110px">VS</div>', { x: 485, y: 190, t0: -.1, fx: 'pop' })}
    ${TX('Naughty or Nice? 🤔<br>YOU decide 👇', { x: 90, y: 430, w: 900, s: 84, f: 'Bangers', wt: 400, t0: -.3, t1: S[0], fx: 'pop', style: 'background:#111;border-radius:34px;padding:30px 10px;letter-spacing:2px' })}
    ${E('<span style="font-size:220px">😈</span>', { x: 120, y: 900, t0: .1, t1: S[0], fx: 'pop', rot: -10 })}${E('<span style="font-size:220px">😇</span>', { x: 700, y: 900, t0: .3, t1: S[0], fx: 'pop', rot: 10 })}
    ${Q.map(q).join('')}
    ${TX('Santa’s final verdict…', { x: 90, y: 440, w: 900, s: 92, f: 'Bangers', wt: 400, t0: TV, t1: TPR, fx: 'pop', style: 'background:#111;border-radius:34px;padding:24px 10px;letter-spacing:2px' })}
    ${IMG('nice-list-certificate.png', { x: 90, y: 680, w: 900, t0: TC, t1: TE, fx: 'slam', d: .22, rot: -2 })}
    ${E('<div class="pill" style="background:#30d158;color:#fff;font-family:Bangers;font-weight:400;font-size:120px;border:8px solid #fff;padding:0 40px">NICE ✅</div>', { x: 560, y: 1190, t0: TC + .35, t1: TE, fx: 'stamp', rot: -12, z: 5 })}
    ${pillE('Official Nice List · $3.29', '#FFD93D', '#111', 70, { y: 450, t0: TPR, t1: TE, fx: 'slam', d: .2, pstyle: 'font-family:Bangers;font-weight:400;letter-spacing:2px' })}
    ${endCard(TE, { bg: 'linear-gradient(90deg,#b5162b 50%,#0e7f3f 50%)', font: 'Bangers', l1s: 92, l1: 'Comment: NAUGHTY or NICE? 👇', price: '$3.29 · print it in 2 minutes', search: 'search “Nice List Certificate” on Etsy', fx: 'stamp' })}`,
    cues: [['boom', 0, .6], ...S.flatMap((s, k) => [['whoosh', s, .3], ['rise', s + .4, .25], [Q[k][1] < 0 ? 'buzz' : 'ding', s + 1.55, Q[k][1] < 0 ? .35 : .5]]), ['drumroll', TV, .55], ['boom', TC, .6], ['tada', TC + .35, .5], ['ding', TPR, .45], ...endCues(TE)],
  };
}

// =====================================================================================
// 8. PAPER STOP-MOTION — 8 fps held frames + jitter on a cutting mat, toy marimba + printer whirr + shutter -> Coloring Book
// =====================================================================================
{
  const pages = ['cb-01.png', 'cb-04.png', 'cb-06.png', 'cb-08.png', 'cb-13.png', 'cb-16.png'];
  const fast = ['cb-02.png', 'cb-03.png', 'cb-05.png', 'cb-07.png', 'cb-09.png', 'cb-10.png', 'cb-11.png', 'cb-12.png', 'cb-14.png', 'cb-15.png', 'cb-17.png', 'cb-18.png', 'cb-19.png', 'cb-20.png'];
  const tp = k => 1.6 + k * 1.0, TF = 7.6, TN = 9.6, TPR = 11.4, TE = 13.2;
  const rots = [-4, 3, -2, 5, -5, 2];
  const crayon = (x, y, c, r) => E(`<div style="width:240px;height:46px;border-radius:10px 4px 4px 10px;background:${c};box-shadow:0 6px 0 rgba(0,0,0,.25);position:relative"><div style="position:absolute;right:-34px;top:8px;border-left:36px solid ${c};border-top:15px solid transparent;border-bottom:15px solid transparent"></div><div style="position:absolute;left:40px;top:0;width:60px;height:46px;background:rgba(255,255,255,.35)"></div></div>`, { x, y, rot: r, cls: 'jit' });
  const counter = (n, t0, t1) => E(`<div style="width:250px;height:230px;background:#ffe66d;box-shadow:0 10px 18px rgba(0,0,0,.3);font-family:Caveat;text-align:center;color:#333;padding-top:20px"><div style="font-size:46px">pages:</div><div style="font-size:110px;line-height:1">${n}/20</div></div>`, { x: 770, y: 190, t0, t1, rot: 5, cls: 'jit', z: 12 });
  V['paper-stopmotion'] = {
    music: 'xmas-toymarimba.wav', musicVol: .7, dur: 17.2, step: 1 / 8,
    html: `${P('#1e6b66', '', { fx: 'none' })}
    ${E('', { x: 0, y: 0, w: 1080, h: 1920, style: 'background:repeating-linear-gradient(0deg,transparent 0 59px,rgba(255,255,255,.12) 59px 60px),repeating-linear-gradient(90deg,transparent 0 59px,rgba(255,255,255,.12) 59px 60px),repeating-linear-gradient(0deg,transparent 0 298px,rgba(255,255,255,.22) 298px 300px),repeating-linear-gradient(90deg,transparent 0 298px,rgba(255,255,255,.22) 298px 300px)' })}
    ${crayon(40, 1500, '#e63946', -20)}${crayon(780, 1560, '#2a9df4', 15)}${crayon(330, 1660, '#f4c430', -5)}${crayon(-60, 1000, '#7ac74f', 70)}
    ${E(`<div style="background:#fffdf7;padding:24px 34px;font-family:Caveat;font-size:76px;color:#222;line-height:1.05;box-shadow:0 10px 20px rgba(0,0,0,.3)">I printed a whole coloring book… for $3.99 🖍️</div>`, { x: 70, y: 200, w: 940, t0: -.3, t1: 2.4, rot: -2, cls: 'jit', z: 12 })}
    ${E(`<div style="background:#fffdf7;padding:14px 26px;font-family:Caveat;font-size:62px;color:#222;box-shadow:0 8px 16px rgba(0,0,0,.3)">20 Christmas coloring pages ✏️</div>`, { x: 60, y: 230, w: 680, t0: 2.4, t1: TE, rot: -3, cls: 'jit', z: 12 })}
    ${pages.map((f, k) => IMG(f, { x: 290 + (k % 3 - 1) * 20, y: 470, w: 500, t0: tp(k), rot: rots[k], cls: 'jit', z: 3 + k, kf: [[tp(k), 0, 760, 1, 0], [tp(k) + .55, 0, 260, 1, 0], [tp(k) + .8, 0, 0, 1, 0]] })).join('')}
    ${fast.map((f, k) => IMG(f, { x: 290, y: 470, w: 500, t0: TF + k * .125, t1: TN, rot: (k % 2 ? 4 : -4), cls: 'jit', z: 10 })).join('')}
    ${pages.map((_, k) => counter(k + 1, tp(k) + .8, k < 5 ? tp(k + 1) + .8 : TF)).join('')}
    ${fast.map((_, k) => counter(7 + k, TF + k * .125, k < fast.length - 1 ? TF + (k + 1) * .125 : 99)).join('')}
    ${IMG('cb-22.png', { x: 250, y: 440, w: 580, t0: TN, rot: 2, cls: 'jit', z: 11, kf: [[TN, 0, 760, 1, 0], [TN + .5, 0, 0, 1, 0]] })}
    ${E(`<div style="background:#ff6fa8;color:#fff;padding:12px 28px;font-family:Caveat;font-size:66px;box-shadow:0 8px 16px rgba(0,0,0,.3)">+ a Note from Santa at the end 💌</div>`, { x: 90, y: 1060, t0: TN + .6, rot: -3, cls: 'jit', z: 13 })}
    ${E(`<div style="width:360px;background:#fffdf7;border-radius:20px;padding:30px 20px;text-align:center;font-family:Caveat;color:#222;box-shadow:0 12px 20px rgba(0,0,0,.35);position:relative"><div style="position:absolute;left:24px;top:24px;width:30px;height:30px;border-radius:50%;background:#1e6b66"></div><div style="font-size:150px;line-height:.9">$3.99</div><div style="font-size:56px">= 20¢ a page</div></div>`, { x: 640, y: 690, t0: TPR, rot: 9, cls: 'jit', z: 14 })}
    ${E('', { x: 140, y: 1200, w: 800, h: 720, z: 20, style: 'background:linear-gradient(#f4f5f7,#cfd4da);border-radius:40px 40px 0 0;box-shadow:0 -10px 40px rgba(0,0,0,.35)' })}
    ${E('', { x: 240, y: 1236, w: 600, h: 20, z: 21, style: 'background:#1f2328;border-radius:10px' })}
    ${E('', { x: 860, y: 1300, w: 34, h: 34, z: 21, cls: 'led', style: 'background:#2ecc71;border-radius:50%;box-shadow:0 0 18px #2ecc71' })}
    ${endCard(TE, { bg: 'linear-gradient(rgba(201,167,124,.92),rgba(201,167,124,.92)),repeating-linear-gradient(90deg,#b8925f 0 6px,#c9a77c 6px 18px)', font: 'Caveat', l1s: 96, c: '#2b1d0e', l1: 'snow day? sick day? PRINT DAY 🖨️', price: '$3.99 · 20 pages + Note from Santa', search: 'search “Santa’s Little Helpers coloring” on Etsy', fx: 'none' })}`,
    custom: `document.querySelectorAll('.led').forEach(l=>l.style.opacity=(Math.floor(T*4)%2)?1:.3);`,
    cues: [['shutter', 0, .5], ...pages.flatMap((_, k) => [['printer', tp(k) - .1, .35], ['shutter', tp(k) + .8, .6]]), ['printer', TF, .35], ...fast.map((_, k) => ['shutter', TF + k * .125, .3]), ['paper', TN, .5], ['shutter', TN + .5, .6], ['pop', TN + .6, .4], ['ding', TPR, .5], ...endCues(TE)],
  };
}

// =====================================================================================
// NON-CHRISTMAS "new year reset" set: sage/neutral, calm, slow fades, original acoustic / lo-fi / piano
// =====================================================================================
// 9. 2027 WALL CALENDAR — slow wall-calendar flip-through (pages flip UP), calm acoustic
{
  const T0 = 2.0, PER = .9, TPR = T0 + 12 * PER + .2, TE = TPR + 2.0;
  const files = ['cal-01.png', 'cal-02.png', 'cal-03.png', 'cal-04.png', 'cal-05.png', 'cal-06.png', 'cal-07.png', 'cal-08.png', 'cal-09.png', 'cal-10.png', 'cal-11.png', 'cal-12.png', 'cal-13.png'];
  const caps = [[T0, '12 botanical months 🌿'], [T0 + 3 * PER, 'Sunday start · room for notes'], [T0 + 6 * PER, 'print at home · US Letter + A4'], [T0 + 9 * PER, 'calm on the wall all year']];
  const serif = "'Cormorant Garamond'";
  V['calm-calendar'] = {
    music: 'calm-acoustic.wav', musicVol: .85, dur: TE + 4.0,
    html: `${P('linear-gradient(#f1ece3,#e4dccf)', '', { fx: 'none' })}
    ${E('', { x: 0, y: 1440, w: 1080, h: 480, style: 'background:linear-gradient(#d9cfbf,#cfc4b2)' })}
    ${E('<svg width="200" height="330" viewBox="0 0 200 330"><path d="M100 330 C100 250 100 180 100 90" stroke="#7d8f73" stroke-width="6" fill="none"/>' + [0, 1, 2, 3, 4, 5].map(k => `<ellipse cx="${k % 2 ? 130 : 70}" cy="${110 + k * 36}" rx="34" ry="14" fill="${['#8a9a82', '#a3b18a', '#7d8f73'][k % 3]}" transform="rotate(${k % 2 ? -30 : 30} ${k % 2 ? 130 : 70} ${110 + k * 36})"/>`).join('') + '<rect x="55" y="250" width="90" height="80" rx="10" fill="#c9a98c"/></svg>', { x: 850, y: 1200, z: 2 })}
    ${TX('2027, but make it calm 🌿', { y: 200, s: 88, f: serif, wt: 600, c: '#3f4f3a', t0: -.4, fx: 'fade', d: .5, style: 'font-style:italic' })}
    ${E('', { x: 530, y: 360, w: 20, h: 20, style: 'background:#6b5a4a;border-radius:50%;box-shadow:0 3px 6px rgba(0,0,0,.3)', z: 40 })}
    ${files.map((f, k) => IMG(f, { x: 90, y: 400, w: 900, t0: -1, t1: k < 12 ? T0 + k * PER : 99, out: k < 12 ? 'flipup' : null, od: .55, z: 30 - k, style: 'transform-origin:50% 0;box-shadow:0 18px 40px rgba(60,40,20,.22)' })).join('')}
    ${caps.map(([t, c], k) => TX(c, { y: 1160, s: 50, f: 'Inter', wt: 500, c: '#5c6b55', t0: t, t1: k < 3 ? caps[k + 1][0] : TPR, fx: 'rise', d: .6, out: 'fade', od: .3, style: 'letter-spacing:1px' })).join('')}
    ${TX('a slow flip-through', { y: 1160, s: 46, f: 'Inter', wt: 500, c: '#7d8f73', t0: .2, t1: T0, fx: 'fade', d: .6, style: 'letter-spacing:4px' })}
    ${pillE('2027 Wall Calendar · $3.99', '#8a9a82', '#fff', 60, { y: 1160, t0: TPR, t1: TE, fx: 'rise', d: .6, pstyle: `font-family:${serif};font-weight:600` })}
    ${TX('instant download · 13 pages', { y: 1270, s: 44, f: 'Inter', wt: 500, c: '#5c6b55', t0: TPR + .3, t1: TE, fx: 'fade' })}
    ${endCard(TE, { bg: '#dfe7da', font: serif, c: '#2f3b2b', l1s: 90, l1: 'a calm year starts on the wall 🌿', price: '$3.99 · 2027 Wall Calendar', pbg: '#fff', search: 'search “2027 Wall Calendar printable” on Etsy', fx: 'fade', d: .7 })}`,
    cues: [...files.slice(0, 12).map((_, k) => ['paper', T0 + k * PER - .5, .28]), ['chime', TPR, .35], ['chime', TE + .3, .25]],
  };
}
// 10. BUDGET RESET — before (receipt chaos) -> after (organized pages) -> No-Spend Challenge tick-off, lo-fi + rain
{
  const TA = 2.6, PER = .75, pg = ['bg-1.png', 'bg-2.png', 'bg-3.png', 'bg-4.png', 'bg-5.png', 'bg-6.png', 'bg-7.png', 'bg-8.png'];
  const caps = ['', 'annual overview', 'monthly budget', 'expense tracker', 'bill tracker', 'savings goals', 'debt payoff', 'sinking funds'];
  const TN = TA + .4 + pg.length * PER, NS = 14, TPR = TN + 1.2 + NS * .2 + .4, TE = TPR + 1.8;
  const serif = "'Cormorant Garamond'";
  const receipt = (k) => { const x = [60, 330, 640, 160, 520, 780, 90, 400, 700, 250][k], y = [520, 470, 540, 820, 760, 860, 1100, 1050, 1120, 1300][k], r = [-18, 10, -6, 14, -12, 20, 8, -15, 6, -4][k];
    return E(`<div style="width:200px;height:300px;background:#fff;box-shadow:0 10px 20px rgba(0,0,0,.18);padding:22px 18px;font-family:Inter;font-size:20px;color:#999;clip-path:polygon(0 0,100% 0,100% 94%,90% 100%,80% 94%,70% 100%,60% 94%,50% 100%,40% 94%,30% 100%,20% 94%,10% 100%,0 94%)">RECEIPT<br>————<br>coffee ... 6.40<br>snacks ... 12.99<br>??? ... 48.00<br>————<br><b style="color:#c0392b;font-size:26px">$$$ ??</b></div>`, { x, y, rot: r, t0: -.5 + k * .05, t1: TA + .6, fx: 'drop', d: .5, kf: [[TA, 0, 0, 1, 0], [TA + .5, (x < 450 ? -1 : 1) * 900, -200, .9, r * 3]] }); };
  // box centres on the No-Spend page (bg-9, 765x990): 6 columns x 5 rows
  const W = 700, X0 = 190, Y0 = 470, H = W * 990 / 765;
  const box = k => ({ x: X0 + W * (.067 + .074 + (k % 6) * .1495), y: Y0 + H * (.272 + .056 + Math.floor(k / 6) * .1135) });
  V['budget-reset'] = {
    music: 'calm-lofirain.wav', musicVol: .9, dur: TE + 4.0,
    html: `${P('#f4efe7', '', { fx: 'none' })}
    ${TX('budget reset for 2027 🧾', { y: 200, s: 86, f: serif, wt: 600, c: '#3d3a33', t0: -.4, fx: 'fade', d: .5, z: 40 })}
    ${pillE('BEFORE 😵‍💫', '#c97b5a', '#fff', 52, { y: 340, t0: -.2, t1: TA + .4, z: 40, pstyle: 'font-family:Inter;font-weight:800;letter-spacing:2px' })}
    ${Array.from({ length: 10 }, (_, k) => receipt(k)).join('')}
    ${pillE('AFTER 🌿', '#8a9a82', '#fff', 52, { y: 340, t0: TA + .4, t1: TN, fx: 'rise', pstyle: 'font-family:Inter;font-weight:800;letter-spacing:2px' })}
    ${pg.map((f, k) => IMG(f, { x: 250, y: 460, w: 580, t0: TA + .4 + k * PER, t1: k < pg.length - 1 ? TA + .4 + (k + 1) * PER + .3 : TN + .3, fx: k ? 'slideR' : 'rise', d: .4, rot: k % 2 ? 1.5 : -1.5, z: 5 + k })).join('')}
    ${caps.map((c, k) => c ? TX(c, { y: 1260, s: 50, f: 'Inter', wt: 500, c: '#5c6b55', t0: TA + .4 + k * PER, t1: k < pg.length - 1 ? TA + .4 + (k + 1) * PER : TN, fx: 'fade', d: .2, style: 'letter-spacing:2px' }) : '').join('')}
    ${TX('No-Spend Challenge ✔', { y: 330, s: 72, f: serif, wt: 600, c: '#3d3a33', t0: TN, t1: TPR, fx: 'rise' })}
    ${IMG('bg-9.png', { x: X0, y: Y0, w: W, t0: TN, fx: 'rise', d: .5, z: 20 })}
    ${Array.from({ length: NS }, (_, k) => { const b = box(k); return E('✓', { x: b.x - 36, y: b.y - 46, w: 72, t0: TN + 1.2 + k * .2, fx: 'tick', d: .25, z: 21, style: 'font-family:Caveat;font-size:84px;color:#5f7f4f;text-align:center' }); }).join('')}
    ${E(`<div style="width:330px;height:330px;border-radius:50%;background:#8a9a82;color:#fff;text-align:center;padding-top:72px;font-family:${serif};box-shadow:0 12px 30px rgba(60,70,50,.3)"><div style="font-size:112px;font-weight:600;line-height:1">$4.99</div><div style="font-family:Inter;font-size:30px;margin-top:6px">9 printable pages</div></div>`, { x: 680, y: 1060, t0: TPR, fx: 'rise', d: .5, z: 25, rot: 6 })}
    ${TX('Budget Planner · instant download', { x: 60, y: 1388, w: 900, a: 'left', s: 36, style: 'white-space:nowrap', f: 'Inter', wt: 600, c: '#3d3a33', t0: TPR + .3, fx: 'fade', z: 25 })}
    ${endCard(TE, { bg: '#e9e4da', font: serif, c: '#2f3b2b', l1s: 92, l1: 'new year, calm money 🌿', price: '$4.99 · Budget Planner', pbg: '#8a9a82', pc: '#fff', search: 'search “Budget Planner printable” on Etsy', fx: 'fade', d: .7 })}`,
    cues: [['paper', TA, .35], ['whoosh', TA + .05, .2], ...pg.map((_, k) => ['paper', TA + .4 + k * PER, .25]), ['chime', TN, .3], ...Array.from({ length: NS }, (_, k) => ['check', TN + 1.2 + k * .2, .35]), ['chime', TPR, .35], ['chime', TE + .3, .25]],
  };
}
// 11. "THINGS I'M DOING DIFFERENTLY IN 2027" — handwritten list + planner pages, cream/terracotta, soft felt piano -> 2027 Planner
{
  const items = [['one calm planner, not 5 apps', 'pl-01.png'], ['see my whole year at a glance', 'pl-02.png'], ['goals I actually look at', 'pl-03.png'], ['plan monthly, not panic daily', 'pl-04.png'], ['track tiny habits ✓', 'pl-18.png']];
  const S = items.map((_, k) => 1.6 + k * 2.1), TPR = S[4] + 2.2, TE = TPR + 1.8;
  const serif = "'Cormorant Garamond'";
  V['calm-planner'] = {
    music: 'calm-piano.wav', musicVol: .9, dur: TE + 4.0,
    html: `${P('linear-gradient(#f8f1e9,#efe3d6)', '', { fx: 'none' })}
    ${TX('things I’m doing differently in 2027 ✍️', { y: 190, s: 76, f: serif, wt: 600, c: '#7a3e2b', t0: -.4, fx: 'fade', d: .5, style: 'font-style:italic', lh: 1.05 })}
    ${items.map(([t], k) => E(`<span style="font-family:Caveat;font-size:68px;color:#4a3a30">${k + 1}. ${t}</span>`, { x: 80, y: 370 + k * 84, t0: S[k], fx: 'write', d: .8 })).join('')}
    ${items.map(([, f], k) => IMG(f, { x: 300, y: 805, w: 480, t0: k ? S[k] : .2, t1: k < 4 ? S[k + 1] + .4 : TE, fx: k ? 'slideR' : 'rise', d: .5, rot: k % 2 ? 2 : -2, z: 5 + k, style: 'box-shadow:0 18px 40px rgba(122,62,43,.2)' })).join('')}
    ${E(`<div style="background:#b5654a;color:#fff;border-radius:24px;padding:18px 34px;text-align:center;font-family:${serif}"><div style="font-size:84px;font-weight:600;line-height:1">$5.99</div><div style="font-family:Inter;font-size:30px">2027 Planner · instant download</div></div>`, { x: 640, y: 1180, t0: TPR, fx: 'rise', d: .5, rot: 5, z: 20 })}
    ${endCard(TE, { bg: '#f3e6da', font: serif, c: '#5a2e20', l1s: 92, l1: '2027: calm, on paper 🤍', price: '$5.99 · 2027 Planner', pbg: '#b5654a', pc: '#fff', search: 'search “2027 Planner printable” on Etsy', fx: 'fade', d: .7 })}`,
    cues: [...S.map(s => ['paper', s - .05, .22]), ['chime', TPR, .35], ['chime', TE + .3, .25]],
  };
}

// ---------- in-page engine ----------
const ENGINE = `
const E={outBack:p=>1+2.7*Math.pow(p-1,3)+1.7*Math.pow(p-1,2),outCubic:p=>1-Math.pow(1-p,3),inOut:p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2,
 outBounce:p=>{const n=7.5625,d=2.75;if(p<1/d)return n*p*p;if(p<2/d)return n*(p-=1.5/d)*p+.75;if(p<2.5/d)return n*(p-=2.25/d)*p+.9375;return n*(p-=2.625/d)*p+.984375}};
const cl=v=>Math.max(0,Math.min(1,v));let ELS=null;
const hash=(a,b)=>{const x=Math.sin(a*127.1+b*311.7)*43758.5453;return x-Math.floor(x)};
window.render=(t)=>{
 const T=window.STEP?Math.floor(t/STEP+1e-6)*STEP:t;
 if(!ELS)ELS=[...document.querySelectorAll('[data-t0]')];
 for(let i=0;i<ELS.length;i++){const e=ELS[i];
  const t0=+e.dataset.t0,t1=e.dataset.t1!=null?+e.dataset.t1:1e9;
  if(T<t0||T>=t1){e.style.visibility='hidden';e.style.opacity=0;continue;}
  e.style.visibility='inherit';
  const fx=e.dataset.fx,d=+e.dataset.d,lt=T-t0,p=cl(lt/d),rot=+e.dataset.rot;let tf='',op=1;
  if(fx==='fade')op=E.outCubic(p);
  else if(fx==='pop'){tf='scale('+Math.max(0,E.outBack(p))+')';op=p>0?1:0}
  else if(fx==='tick'){tf='scale('+Math.max(0,E.outBack(p))+')';op=p>0?1:0}
  else if(fx==='up'){tf='translateY('+(120*(1-E.outCubic(p)))+'px)';op=p}
  else if(fx==='down'){tf='translateY('+(-120*(1-E.outCubic(p)))+'px)';op=p}
  else if(fx==='rise'){tf='translateY('+(50*(1-E.outCubic(p)))+'px)';op=E.outCubic(p)}
  else if(fx==='slideL'){tf='translateX('+(-1300*(1-E.outCubic(p)))+'px)'}
  else if(fx==='slideR'){tf='translateX('+(1300*(1-E.outCubic(p)))+'px)'}
  else if(fx==='drop'){tf='translateY('+(-1900*(1-E.outBounce(p)))+'px)'}
  else if(fx==='stamp'){tf='scale('+(2.4-1.4*E.outCubic(p))+')';op=p}
  else if(fx==='slam'){tf='scale('+(3-2*E.outCubic(p))+')';op=p>0?1:0}
  else if(fx==='flipin'){tf='perspective(1600px) rotateY('+(90*(1-E.outCubic(p)))+'deg)'}
  else if(fx==='wipe'){e.style.clipPath='inset(-20% '+(100-100*p)+'% -20% 0)'}
  else if(fx==='write'){e.style.clipPath='inset(-40% '+(100-100*p)+'% -40% -5%)'}
  else if(fx==='fill'){e.style.width=(+e.dataset.w*(+e.dataset.to/100)*E.outCubic(p))+'px'}
  else if(fx==='count'){const v=Math.round(+e.dataset.from+(+e.dataset.to-+e.dataset.from)*E.outCubic(p));e.textContent=(e.dataset.pre||'')+v+(e.dataset.suf||'')}
  else if(fx==='type'){const s=e._s||(e._s=[...e.dataset.text]),n=Math.min(s.length,Math.floor(lt*(+e.dataset.cps)));e.firstChild.textContent=s.slice(0,n).join('');
    const done=n>=s.length,since=lt-s.length/(+e.dataset.cps);e.lastChild.style.opacity=(!done||(since<1.2&&Math.floor(since*3)%2===0))?1:0}
  if(e.dataset.out&&t1<1e9){const q=cl((t1-T)/(+e.dataset.od));
    if(e.dataset.out==='fade')op*=q;
    else if(e.dataset.out==='flipup'){const r=E.inOut(1-q);tf+=' perspective(2200px) rotateX('+(-105*r)+'deg)';op*=r>.85?(1-r)/.15:1}
    else if(e.dataset.out==='slideUp')tf+=' translateY('+(-1500*E.inOut(1-q))+'px)'}
  if(e.dataset.kf){const K=e._k||(e._k=JSON.parse(e.dataset.kf));let v=K[0].slice(1);
    for(let k=0;k<K.length;k++){if(T>=K[k][0]){v=K[k].slice(1);if(k+1<K.length&&T<K[k+1][0]){const q=E.outCubic((T-K[k][0])/(K[k+1][0]-K[k][0]));v=v.map((a,j)=>a+(K[k+1][j+1]-a)*q)}}}
    tf='translate('+v[0]+'px,'+v[1]+'px) scale('+v[2]+') rotate('+v[3]+'deg) '+tf}
  if(e.dataset.float)tf+=' translateY('+(Math.sin(T*2.2+t0)*9)+'px) rotate('+(Math.sin(T*1.6+t0)*1)+'deg)';
  if(window.STEP&&e.classList.contains('jit')){const s=Math.floor(T/STEP);tf+=' translate('+((hash(s,i)-.5)*7)+'px,'+((hash(i,s)-.5)*7)+'px) rotate('+((hash(s+.5,i)-.5)*1.4)+'deg)'}
  e.style.transform=tf+' rotate('+rot+'deg)';e.style.opacity=op;}
 if(window.custom)window.custom(T,t);
};`;

(async () => {
  const only = process.argv.slice(2);
  const b = await chromium.launch();
  for (const [name, v] of Object.entries(V)) {
    if (only.length && !only.includes(name)) continue;
    const page = await b.newPage({ viewport: { width: 1080, height: 1920 } });   // fresh page: no leftover globals
    const html = `<!doctype html><html><head><meta charset="utf-8">${FONTS}<style>${CSS}</style></head><body>${v.html}
      <script>${ENGINE}window.STEP=${v.step || 0};${v.custom ? `window.custom=(T,t)=>{${v.custom}};` : ''}</script></body></html>`;
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const dir = path.join(TT, 'frames', name);
    fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    const N = Math.round(v.dur * FPS);
    for (let f = 0; f < N; f++) {
      await page.evaluate(t => window.render(t), f / FPS);
      await page.screenshot({ path: path.join(dir, String(f).padStart(4, '0') + '.jpg'), type: 'jpeg', quality: 88 });
    }
    const spec = path.join(dir, 'audio.json'), wav = path.join(dir, 'audio.wav');
    fs.writeFileSync(spec, JSON.stringify({ music: v.music, musicVol: v.musicVol, dur: v.dur, cues: v.cues, out: wav }));
    execFileSync('python3', [path.join(__dirname, 'mix-audio.py'), spec]);
    const out = path.join(TT, `DoodleDesignAndCo-TikTok-${name}.mp4`);
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(dir, '%04d.jpg'), '-i', wav,
      '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out]);
    console.log('built', name, v.dur + 's', v.music);
    await page.close();
  }
  await b.close();
})();
