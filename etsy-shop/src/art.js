// Original vector art for the DoodleDesignAndCo Christmas set (no third-party clip art).
const santa = (s = 1) => `
<svg viewBox="0 0 200 220" width="${200 * s}" height="${220 * s}" xmlns="http://www.w3.org/2000/svg">
  <path d="M40 95 Q100 -10 165 70 L175 60 Q185 55 190 68 Q195 82 180 86 L160 95 Z" fill="#d7263d"/>
  <circle cx="186" cy="74" r="13" fill="#fff" stroke="#e8e8e8" stroke-width="2"/>
  <rect x="34" y="88" width="132" height="24" rx="12" fill="#fff" stroke="#eee" stroke-width="2"/>
  <ellipse cx="100" cy="132" rx="52" ry="42" fill="#ffd9c2"/>
  <circle cx="80" cy="128" r="5" fill="#3a2a2a"/><circle cx="120" cy="128" r="5" fill="#3a2a2a"/>
  <circle cx="82" cy="126" r="1.6" fill="#fff"/><circle cx="122" cy="126" r="1.6" fill="#fff"/>
  <ellipse cx="68" cy="144" rx="9" ry="6" fill="#ff9aa2" opacity=".7"/><ellipse cx="132" cy="144" rx="9" ry="6" fill="#ff9aa2" opacity=".7"/>
  <path d="M50 140 Q40 205 100 214 Q160 205 150 140 Q138 160 100 160 Q62 160 50 140Z" fill="#fff" stroke="#ececec" stroke-width="2"/>
  <path d="M74 150 Q88 140 100 150 Q112 140 126 150 Q112 162 100 154 Q88 162 74 150Z" fill="#fff" stroke="#e2e2e2" stroke-width="2"/>
  <circle cx="100" cy="142" r="8" fill="#ff8f80"/>
  <path d="M90 172 Q100 180 110 172" stroke="#c94b4b" stroke-width="3" fill="none" stroke-linecap="round"/>
</svg>`;

const reindeer = (s = 1) => `
<svg viewBox="0 0 200 200" width="${200 * s}" height="${200 * s}" xmlns="http://www.w3.org/2000/svg">
  <g stroke="#8a5a3b" stroke-width="7" stroke-linecap="round" fill="none">
    <path d="M70 70 L52 30 M60 48 L38 44 M56 38 L64 18"/>
    <path d="M130 70 L148 30 M140 48 L162 44 M144 38 L136 18"/>
  </g>
  <ellipse cx="58" cy="88" rx="16" ry="9" fill="#b07a52" transform="rotate(-25 58 88)"/>
  <ellipse cx="142" cy="88" rx="16" ry="9" fill="#b07a52" transform="rotate(25 142 88)"/>
  <ellipse cx="100" cy="115" rx="45" ry="50" fill="#b07a52"/>
  <ellipse cx="100" cy="142" rx="30" ry="24" fill="#e8c8a8"/>
  <circle cx="84" cy="104" r="6" fill="#3a2a2a"/><circle cx="116" cy="104" r="6" fill="#3a2a2a"/>
  <circle cx="86" cy="102" r="2" fill="#fff"/><circle cx="118" cy="102" r="2" fill="#fff"/>
  <circle cx="100" cy="130" r="11" fill="#e63946"/><circle cx="96" cy="126" r="3" fill="#fff" opacity=".7"/>
  <path d="M90 150 Q100 158 110 150" stroke="#6b4226" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M62 160 Q100 178 138 160" stroke="#2a9d8f" stroke-width="9" fill="none" stroke-linecap="round"/>
  <circle cx="100" cy="176" r="8" fill="#f4c430" stroke="#c99a10" stroke-width="2"/>
</svg>`;

const tree = (s = 1) => `
<svg viewBox="0 0 160 220" width="${160 * s}" height="${220 * s}" xmlns="http://www.w3.org/2000/svg">
  <rect x="68" y="185" width="24" height="30" rx="4" fill="#8a5a3b"/>
  <path d="M80 40 L20 120 H55 L15 190 H145 L105 120 H140 Z" fill="#2f7d4f"/>
  <path d="M80 40 L45 95 H70 Z" fill="#3c9a62" opacity=".6"/>
  <path d="M40 150 Q80 170 125 140" stroke="#f4c430" stroke-width="4" fill="none"/>
  <path d="M55 105 Q80 118 108 100" stroke="#f4c430" stroke-width="4" fill="none"/>
  <circle cx="60" cy="160" r="7" fill="#e63946"/><circle cx="100" cy="170" r="7" fill="#4ea8de"/>
  <circle cx="82" cy="128" r="7" fill="#e63946"/><circle cx="112" cy="150" r="6" fill="#f4c430"/>
  <circle cx="70" cy="112" r="6" fill="#4ea8de"/>
  <path d="M80 12 l7 15 16 2 -12 11 3 16 -14 -8 -14 8 3 -16 -12 -11 16 -2z" fill="#f4c430"/>
</svg>`;

const gingerbread = (s = 1) => `
<svg viewBox="0 0 140 160" width="${140 * s}" height="${160 * s}" xmlns="http://www.w3.org/2000/svg">
  <path d="M70 8 a24 24 0 1 1 -0.1 0Z M45 52 H95 L125 70 Q132 82 120 86 L98 78 L104 112 L118 140 Q120 152 108 152 L92 150 L70 122 L48 150 L32 152 Q20 152 22 140 L36 112 L42 78 L20 86 Q8 82 15 70Z" fill="#c8814a"/>
  <circle cx="62" cy="30" r="3.5" fill="#3a2a2a"/><circle cx="78" cy="30" r="3.5" fill="#3a2a2a"/>
  <path d="M60 42 Q70 50 80 42" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/>
  <circle cx="70" cy="70" r="5" fill="#e63946"/><circle cx="70" cy="88" r="5" fill="#2a9d8f"/>
  <path d="M22 76 q6 -6 12 0 M106 76 q6 -6 12 0 M30 140 q6 -6 12 0 M98 140 q6 -6 12 0" stroke="#fff" stroke-width="3" fill="none"/>
  <path d="M58 58 L70 64 L82 58 L82 70 L70 64 L58 70Z" fill="#e63946"/>
</svg>`;

const snowman = (s = 1) => `
<svg viewBox="0 0 160 220" width="${160 * s}" height="${220 * s}" xmlns="http://www.w3.org/2000/svg">
  <circle cx="80" cy="160" r="52" fill="#fff" stroke="#d9e6f2" stroke-width="3"/>
  <circle cx="80" cy="82" r="38" fill="#fff" stroke="#d9e6f2" stroke-width="3"/>
  <rect x="48" y="38" width="64" height="8" rx="3" fill="#2b2d42"/>
  <rect x="58" y="6" width="44" height="36" rx="4" fill="#2b2d42"/>
  <rect x="58" y="30" width="44" height="7" fill="#e63946"/>
  <circle cx="68" cy="76" r="4" fill="#2b2d42"/><circle cx="92" cy="76" r="4" fill="#2b2d42"/>
  <path d="M80 86 L104 92 L80 94Z" fill="#f4845f"/>
  <path d="M42 112 Q80 128 118 112 L118 122 Q80 138 42 122Z" fill="#e63946"/>
  <path d="M100 120 L110 160 L96 160 L90 124Z" fill="#c1121f"/>
  <circle cx="80" cy="150" r="5" fill="#2b2d42"/><circle cx="80" cy="172" r="5" fill="#2b2d42"/>
  <path d="M30 140 L6 118 M14 126 L4 130 M128 140 L152 118 M144 126 L154 130" stroke="#8a5a3b" stroke-width="4" stroke-linecap="round"/>
</svg>`;

const elf = (s = 1) => `
<svg viewBox="0 0 200 230" width="${200 * s}" height="${230 * s}" xmlns="http://www.w3.org/2000/svg">
  <path d="M55 90 Q110 -20 175 40 Q150 40 145 90Z" fill="#2a9d8f"/>
  <circle cx="178" cy="40" r="11" fill="#f4c430"/>
  <rect x="48" y="82" width="104" height="18" rx="9" fill="#e63946"/>
  <path d="M52 120 L28 100 L50 136Z M148 120 L172 100 L150 136Z" fill="#ffd9c2"/>
  <ellipse cx="100" cy="132" rx="50" ry="44" fill="#ffd9c2"/>
  <circle cx="82" cy="128" r="6" fill="#3a2a2a"/><circle cx="118" cy="128" r="6" fill="#3a2a2a"/>
  <circle cx="84" cy="126" r="2" fill="#fff"/><circle cx="120" cy="126" r="2" fill="#fff"/>
  <ellipse cx="68" cy="146" rx="9" ry="6" fill="#ff9aa2" opacity=".7"/><ellipse cx="132" cy="146" rx="9" ry="6" fill="#ff9aa2" opacity=".7"/>
  <path d="M86 152 Q100 166 114 152" stroke="#c94b4b" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <path d="M60 172 L100 186 L140 172 L150 225 H50Z" fill="#2a9d8f"/>
  <path d="M60 172 L72 188 L84 176 L100 192 L116 176 L128 188 L140 172 L100 186Z" fill="#e63946"/>
  <circle cx="100" cy="205" r="5" fill="#f4c430"/>
</svg>`;

const gift = (s = 1, c1 = '#2f7d4f', c2 = '#e63946') => `
<svg viewBox="0 0 120 120" width="${120 * s}" height="${120 * s}" xmlns="http://www.w3.org/2000/svg">
  <rect x="12" y="44" width="96" height="70" rx="6" fill="${c1}"/>
  <rect x="6" y="32" width="108" height="20" rx="5" fill="${c1}" stroke="#00000022" stroke-width="2"/>
  <rect x="52" y="32" width="16" height="82" fill="${c2}"/>
  <path d="M60 32 Q30 2 26 22 Q24 34 60 32 Q90 2 94 22 Q96 34 60 32Z" fill="${c2}"/>
</svg>`;

const snowflake = (s = 1, color = '#9cc9e6') => `
<svg viewBox="0 0 100 100" width="${100 * s}" height="${100 * s}" xmlns="http://www.w3.org/2000/svg">
  <g stroke="${color}" stroke-width="5" stroke-linecap="round" fill="none">
    ${[0, 60, 120].map(r => `<g transform="rotate(${r} 50 50)"><path d="M50 6 V94"/><path d="M50 22 L40 12 M50 22 L60 12 M50 78 L40 88 M50 78 L60 88"/></g>`).join('')}
  </g>
</svg>`;

const candycane = (s = 1) => `
<svg viewBox="0 0 80 160" width="${80 * s}" height="${160 * s}" xmlns="http://www.w3.org/2000/svg">
  <defs><pattern id="cc" width="20" height="20" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="20" height="20" fill="#fff"/><rect width="9" height="20" fill="#e63946"/></pattern></defs>
  <path d="M58 150 V50 Q58 14 36 14 Q14 14 14 40" stroke="#c9c9c9" stroke-width="22" fill="none" stroke-linecap="round"/>
  <path d="M58 150 V50 Q58 14 36 14 Q14 14 14 40" stroke="url(#cc)" stroke-width="18" fill="none" stroke-linecap="round"/>
</svg>`;

const star = (s = 1, color = '#f4c430') => `
<svg viewBox="0 0 100 100" width="${100 * s}" height="${100 * s}" xmlns="http://www.w3.org/2000/svg">
  <path d="M50 4 l13 29 32 3 -24 21 7 31 -28 -16 -28 16 7 -31 -24 -21 32 -3z" fill="${color}" stroke="#d4a017" stroke-width="3" stroke-linejoin="round"/>
</svg>`;

const holly = (s = 1) => `
<svg viewBox="0 0 120 70" width="${120 * s}" height="${70 * s}" xmlns="http://www.w3.org/2000/svg">
  <path d="M60 38 Q40 10 8 18 Q22 26 14 34 Q28 34 26 46 Q40 38 60 38Z" fill="#2f7d4f"/>
  <path d="M60 38 Q80 10 112 18 Q98 26 106 34 Q92 34 94 46 Q80 38 60 38Z" fill="#3c9a62"/>
  <circle cx="54" cy="44" r="8" fill="#e63946"/><circle cx="66" cy="44" r="8" fill="#c1121f"/><circle cx="60" cy="34" r="8" fill="#e63946"/>
</svg>`;

module.exports = { santa, reindeer, tree, gingerbread, snowman, elf, gift, snowflake, candycane, star, holly };
