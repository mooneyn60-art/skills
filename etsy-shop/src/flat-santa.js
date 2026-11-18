// Flat peeking Santa in the "Christmas Wishlist" palette: pink #d85873, dark green #2d693c, teal #38807c, mint #b0deb5.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const W = path.join(__dirname, '..', 'work', 'santa');
const P = { pink: '#d85873', pinkDk: '#c4475f', green: '#2d693c', teal: '#38807c', mint: '#b0deb5', mintLt: '#dff2e2', skin: '#f7cdb0', cheek: '#f0a0ad', nose: '#e8808f' };
const whites = (fill) => `
  <circle cx="284" cy="116" r="22" fill="${fill}"/>
  <rect x="56" y="104" width="206" height="40" rx="20" fill="${fill}"/>
  <path d="M86 176 C80 236 120 276 160 278 C200 276 240 236 234 176 C222 196 200 204 160 204 C120 204 98 196 86 176Z" fill="${fill}"/>
  <path d="M160 196 C146 182 114 184 106 200 C124 206 146 206 160 198 C174 206 196 206 214 200 C206 184 174 182 160 196Z" fill="${fill}"/>`;
const mitten = (x) => `
  <rect x="${x}" y="222" width="54" height="52" rx="22" fill="${P.green}"/>
  <rect x="${x + 40}" y="238" width="20" height="26" rx="10" fill="${P.green}"/>
  <rect x="${x - 4}" y="216" width="62" height="16" rx="8" fill="${P.mint}"/>`;
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 300">
  <path d="M70 118 C70 50 130 14 190 22 C240 28 275 60 290 96 C296 112 284 122 272 112 C258 92 240 80 226 78 C238 96 244 110 246 124 Z" fill="${P.pink}"/>
  <path d="M190 22 C240 28 275 60 290 96 C296 112 284 122 272 112 C262 98 250 88 236 82 C226 56 210 34 190 22Z" fill="${P.pinkDk}" opacity=".35"/>
  <path d="M118 66 q10 -14 22 -4 q8 8 -2 14 q-8 3 -8 -5" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/>
  <circle cx="165" cy="48" r="5" fill="#fff"/><circle cx="205" cy="62" r="5" fill="#fff"/><circle cx="150" cy="92" r="4.5" fill="#fff"/>
  <ellipse cx="160" cy="160" rx="72" ry="58" fill="${P.skin}"/>
  <g transform="translate(3,6)">${whites(P.mint)}</g>
  ${whites('#ffffff')}
  <path d="M100 224 C120 258 200 258 220 224 C206 250 184 262 160 262 C136 262 114 250 100 224Z" fill="${P.mintLt}"/>
  <path d="M118 150 q14 -12 28 0 M174 150 q14 -12 28 0" stroke="#fff" stroke-width="9" stroke-linecap="round" fill="none"/>
  <path d="M118 152 q14 -12 28 0 M174 152 q14 -12 28 0" stroke="${P.mint}" stroke-width="3" stroke-linecap="round" fill="none" opacity=".9"/>
  <circle cx="132" cy="166" r="7" fill="${P.green}"/><circle cx="188" cy="166" r="7" fill="${P.green}"/>
  <circle cx="134.5" cy="163.5" r="2.2" fill="#fff"/><circle cx="190.5" cy="163.5" r="2.2" fill="#fff"/>
  <ellipse cx="112" cy="186" rx="13" ry="8" fill="${P.cheek}" opacity=".8"/><ellipse cx="208" cy="186" rx="13" ry="8" fill="${P.cheek}" opacity=".8"/>
  <ellipse cx="160" cy="184" rx="14" ry="11" fill="${P.nose}"/><ellipse cx="155" cy="180" rx="4" ry="3" fill="#fff" opacity=".6"/>
  <path d="M148 218 q12 10 24 0" stroke="${P.pink}" stroke-width="5" fill="none" stroke-linecap="round"/>
  <rect x="0" y="262" width="340" height="30" rx="15" fill="${P.teal}"/>
  <path d="M18 277 h304" stroke="${P.mint}" stroke-width="5" stroke-linecap="round" stroke-dasharray="2 26"/>
  ${mitten(30)}${mitten(256)}
</svg>`;
fs.writeFileSync(path.join(W, 'flat-santa.svg'), svg);
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 2040, height: 1800 } });
  await p.setContent(`<html><body style="margin:0;background:transparent">${svg.replace('<svg ', '<svg width="2040" height="1800" ')}</body></html>`);
  await p.screenshot({ path: path.join(W, 'flat-santa-transparent.png'), omitBackground: true });
  await b.close(); console.log('ok');
})();
