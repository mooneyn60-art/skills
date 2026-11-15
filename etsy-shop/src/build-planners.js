// 2027 Planner + Budget Tracker printables (minimal sage/neutral style). US Letter + A4.
const { chromium } = require('playwright');
const path = require('path');
const OUT = path.join(__dirname, '..', 'products');

const FONTS = `<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Jost:wght@300;400;500&display=block" rel="stylesheet">`;
const C = { sage: '#8a9a82', sageL: '#e7ece3', beige: '#f7f2ea', terra: '#c97b5a', ink: '#3d3d3a', line: '#cfcabf' };
const css = `@page{margin:0}*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Jost;color:${C.ink};-webkit-print-color-adjust:exact;print-color-adjust:exact;font-weight:300}
.pg{width:100vw;height:100vh;page-break-after:always;padding:6vh 7vw 5vh;position:relative;display:flex;flex-direction:column;overflow:hidden}
h1{font-family:'Cormorant Garamond';font-weight:500;font-size:6vh;line-height:1;letter-spacing:.01em}
h2{font-family:'Cormorant Garamond';font-weight:600;font-size:2.4vh}
.eyebrow{font-size:1.25vh;letter-spacing:.35em;text-transform:uppercase;color:${C.sage};font-weight:500}
.rule{height:2px;background:${C.sage};width:12vw;margin:1.4vh 0 2.2vh}
.lines{flex:1;background:repeating-linear-gradient(transparent 0 calc(3.2vh - 1px),${C.line} calc(3.2vh - 1px) 3.2vh)}
.box{border:1px solid ${C.line};border-radius:10px;padding:1.2vh 1.2vw}
.ft{position:absolute;bottom:2.2vh;left:0;right:0;text-align:center;font-size:1vh;letter-spacing:.3em;color:#aaa}
table{width:100%;border-collapse:collapse}
td,th{border:1px solid ${C.line};font-size:1.35vh;padding:0 .6vw;height:3.1vh;text-align:left}
th{background:${C.sageL};font-weight:500;letter-spacing:.06em}
.cal td{vertical-align:top;font-size:1.3vh;padding:.5vh .5vw}
.cb{display:inline-block;width:1.4vh;height:1.4vh;border:1px solid ${C.sage};border-radius:3px;vertical-align:middle;margin-right:.6vw}`;

const FT = '<div class="ft">DOODLE DESIGN &amp; CO · PERSONAL USE</div>';
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const DOW = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
const DOWL = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const Y = 2027;
const weeks = m => { // array of weeks, each 7 cells (day number or '')
  const first = new Date(Date.UTC(Y, m, 1)).getUTCDay(), days = new Date(Date.UTC(Y, m + 1, 0)).getUTCDate();
  const cells = [...Array(first).fill(''), ...Array.from({ length: days }, (_, i) => i + 1)];
  while (cells.length % 7) cells.push('');
  return Array.from({ length: cells.length / 7 }, (_, i) => cells.slice(i * 7, i * 7 + 7));
};
const head = (eyebrow, title) => `<div class="eyebrow">${eyebrow}</div><h1>${title}</h1><div class="rule"></div>`;
const tbl = (cols, rows, widths = []) => `<table><tr>${cols.map((c, i) => `<th style="${widths[i] ? 'width:' + widths[i] : ''}">${c}</th>`).join('')}</tr>${Array.from({ length: rows }, () => `<tr>${cols.map(() => '<td></td>').join('')}</tr>`).join('')}</table>`;

// ---------- 2027 PLANNER ----------
const planner = [];
planner.push(`<div class="pg" style="background:${C.beige};justify-content:center;align-items:center;text-align:center">
  <div style="border:1px solid ${C.sage};padding:8vh 8vw;border-radius:200px 200px 12px 12px">
  <div class="eyebrow">Plan · Dream · Do</div>
  <div style="font-family:'Cormorant Garamond';font-size:20vh;line-height:1;color:${C.sage};margin-top:2vh">${Y}</div>
  <h1 style="font-size:5vh">Annual Planner</h1>
  <div style="margin-top:4vh;font-size:1.6vh;letter-spacing:.2em">THIS PLANNER BELONGS TO</div>
  <div style="border-bottom:1px solid ${C.ink};width:40vw;height:5vh;margin:0 auto"></div></div>${FT}</div>`);
planner.push(`<div class="pg">${head('Overview', Y + ' at a Glance')}
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2.2vh 3vw">${MONTHS.map((n, m) => `<div>
    <h2 style="color:${C.terra}">${n}</h2>
    <table class="cal" style="margin-top:.5vh"><tr>${DOW.map(d => `<th style="text-align:center;height:2.2vh;font-size:1.1vh;padding:0">${d}</th>`).join('')}</tr>
    ${weeks(m).map(w => `<tr>${w.map(d => `<td style="border:none;text-align:center;height:2vh;font-size:1.15vh;padding:0">${d}</td>`).join('')}</tr>`).join('')}</table></div>`).join('')}</div>${FT}</div>`);
planner.push(`<div class="pg">${head('Intentions', Y + ' Goals')}
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:2vh 3vw;flex:1">${['Health & Wellness', 'Career & Money', 'Relationships', 'Personal Growth', 'Home & Family', 'Fun & Adventure'].map(t => `<div class="box" style="display:flex;flex-direction:column"><h2 style="color:${C.terra}">${t}</h2><div class="lines" style="margin-top:.6vh"></div></div>`).join('')}</div>
  <div class="box" style="margin-top:2vh"><h2>My word for ${Y}: </h2></div>${FT}</div>`);
MONTHS.forEach((n, m) => {
  const w = weeks(m);
  planner.push(`<div class="pg"><div style="display:flex;justify-content:space-between;align-items:flex-end">
    <div><div class="eyebrow">${Y} · Month ${String(m + 1).padStart(2, '0')}</div><h1>${n}</h1></div>
    <div class="box" style="width:30vw;font-size:1.3vh;height:7vh">Focus this month:</div></div><div class="rule"></div>
    <table class="cal" style="flex:1;height:${w.length * 11}vh"><tr>${DOWL.map(d => `<th style="text-align:center;font-size:1.2vh">${d.slice(0, 3).toUpperCase()}</th>`).join('')}</tr>
    ${w.map(r => `<tr>${r.map(d => `<td style="height:${Math.floor(58 / w.length)}vh;width:14.28%;${d === '' ? `background:${C.beige}` : ''}">${d}</td>`).join('')}</tr>`).join('')}</table>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:2vw;margin-top:2vh;height:14vh">
      <div class="box" style="display:flex;flex-direction:column"><h2>Notes</h2><div class="lines"></div></div>
      <div class="box"><h2>To Do</h2>${Array.from({ length: 4 }, () => `<div style="margin-top:.9vh;font-size:1.3vh"><span class="cb"></span><span style="display:inline-block;border-bottom:1px solid ${C.line};width:80%"></span></div>`).join('')}</div>
    </div>${FT}</div>`);
});
planner.push(`<div class="pg">${head('Weekly', 'Week of ______________')}
  <div style="display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(4,1fr);gap:1.4vh 2vw;flex:1">
  ${DOWL.slice(1).concat('Sunday').map(d => `<div class="box" style="display:flex;flex-direction:column"><h2 style="color:${C.terra}">${d}</h2><div class="lines"></div></div>`).join('')}
  <div class="box" style="background:${C.sageL};border:none"><h2>Top 3 Priorities</h2>${[1, 2, 3].map(i => `<div style="margin-top:1vh;font-size:1.4vh">${i}. <span style="display:inline-block;border-bottom:1px solid ${C.sage};width:85%"></span></div>`).join('')}</div></div>${FT}</div>`);
planner.push(`<div class="pg">${head('Daily', 'Date ______________')}
  <div style="display:grid;grid-template-columns:1.3fr 1fr;gap:2vw;flex:1">
    <div class="box" style="padding:0"><table>${Array.from({ length: 16 }, (_, i) => `<tr><td style="width:18%;font-size:1.25vh;color:${C.sage};height:4.4vh;border-left:none">${((i + 5) % 12) + 1}:00 ${i + 6 < 12 ? 'AM' : 'PM'}</td><td style="border-right:none"></td></tr>`).join('')}</table></div>
    <div style="display:flex;flex-direction:column;gap:2vh">
      <div class="box"><h2>Top Priorities</h2>${[1, 2, 3].map(() => `<div style="margin-top:1.1vh;font-size:1.3vh"><span class="cb"></span><span style="display:inline-block;border-bottom:1px solid ${C.line};width:80%"></span></div>`).join('')}</div>
      <div class="box" style="flex:1;display:flex;flex-direction:column"><h2>To Do</h2><div class="lines"></div></div>
      <div class="box"><h2>Water</h2><div style="font-size:2.4vh;color:${C.sage};letter-spacing:.5vw;margin-top:.5vh">○○○○○○○○</div></div>
      <div class="box" style="height:12vh"><h2>Grateful for</h2></div></div></div>${FT}</div>`);
planner.push(`<div class="pg">${head('Habits', 'Habit Tracker · Month ________')}
  <table><tr><th style="width:24%">Habit</th>${Array.from({ length: 31 }, (_, i) => `<th style="padding:0;text-align:center;font-size:1vh">${i + 1}</th>`).join('')}</tr>
  ${Array.from({ length: 20 }, () => `<tr><td style="height:3.4vh"></td>${Array.from({ length: 31 }, () => '<td style="padding:0"></td>').join('')}</tr>`).join('')}</table>${FT}</div>`);
planner.push(`<div class="pg">${head('Notes', 'Notes')}<div class="lines"></div>${FT}</div>`);

// ---------- BUDGET TRACKER ----------
const budget = [];
budget.push(`<div class="pg" style="background:${C.beige};justify-content:center;align-items:center;text-align:center">
  <div style="border:1px solid ${C.sage};padding:9vh 9vw;border-radius:12px">
  <div class="eyebrow">Save · Spend Wisely · Grow</div>
  <h1 style="font-size:9vh;margin-top:2vh">Budget</h1><h1 style="font-size:9vh;font-style:italic;color:${C.sage}">Planner</h1>
  <div style="margin-top:3vh;font-size:1.6vh;letter-spacing:.25em">MONTHLY FINANCE TRACKER</div></div>${FT}</div>`);
budget.push(`<div class="pg">${head('Overview', 'Annual Budget Overview · Year ______')}
  ${tbl(['Month', 'Income', 'Expenses', 'Savings', 'Debt Paid', 'Notes'], 0, ['16%'])}
  <table style="margin-top:-1px">${MONTHS.map(n => `<tr><td style="width:16%;height:4.3vh;color:${C.terra}">${n}</td><td></td><td></td><td></td><td></td><td></td></tr>`).join('')}
  <tr><td style="font-weight:500;height:4.3vh">TOTAL</td><td></td><td></td><td></td><td></td><td></td></tr></table>${FT}</div>`);
budget.push(`<div class="pg">${head('Monthly', 'Monthly Budget · ____________')}
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:2vh 2vw;flex:1">
    <div>${tbl(['Income Source', 'Expected', 'Actual'], 5, ['50%'])}
    <div style="margin-top:2vh">${tbl(['Savings & Debt', 'Budget', 'Actual'], 6, ['50%'])}</div>
    <div class="box" style="margin-top:2vh;background:${C.sageL};border:none;font-size:1.5vh;line-height:2.4">Total Income: ________<br>Total Expenses: ________<br>Left Over: ________</div></div>
    <div>${tbl(['Fixed Expenses', 'Budget', 'Actual'], 9, ['50%'])}
    <div style="margin-top:2vh">${tbl(['Variable Expenses', 'Budget', 'Actual'], 9, ['50%'])}</div></div>
  </div>${FT}</div>`);
budget.push(`<div class="pg">${head('Spending', 'Expense Tracker · ____________')}${tbl(['Date', 'Description', 'Category', 'Amount', '✓'], 24, ['13%', '40%', '22%', '17%'])}${FT}</div>`);
budget.push(`<div class="pg">${head('Bills', 'Bill Payment Tracker')}
  <table><tr><th style="width:22%">Bill</th><th style="width:9%">Due</th><th style="width:11%">Amount</th>${MONTHS.map(m => `<th style="padding:0;text-align:center;font-size:1.05vh">${m.slice(0, 3)}</th>`).join('')}</tr>
  ${Array.from({ length: 20 }, () => `<tr><td style="height:3.5vh"></td><td></td><td></td>${MONTHS.map(() => '<td></td>').join('')}</tr>`).join('')}</table>${FT}</div>`);
budget.push(`<div class="pg">${head('Goals', 'Savings Goal Tracker')}
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:2.5vh 3vw;flex:1">${[1, 2].map(() => `<div class="box"><div style="font-size:1.5vh;line-height:2.6">Saving for: ________________<br>Goal amount: ________<br>Target date: ________</div>
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:.8vh;margin-top:1.5vh">${Array.from({ length: 50 }, () => `<div style="aspect-ratio:1;border:1px solid ${C.sage};border-radius:50%"></div>`).join('')}</div>
    <div style="font-size:1.2vh;color:#888;margin-top:1vh">Color in a circle each time you save toward your goal</div></div>`).join('')}</div>${FT}</div>`);
budget.push(`<div class="pg">${head('Debt', 'Debt Payoff Tracker')}
  <div class="box" style="font-size:1.5vh;line-height:2.6;margin-bottom:2vh">Debt: ______________ &nbsp;&nbsp; Starting balance: ________ &nbsp;&nbsp; Interest rate: ______ &nbsp;&nbsp; Min. payment: ______</div>
  ${tbl(['Date', 'Payment', 'Interest', 'Remaining Balance', 'Notes'], 22, ['15%', '17%', '15%', '23%'])}${FT}</div>`);
budget.push(`<div class="pg">${head('Planning', 'Sinking Funds')}
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2vh 2vw;flex:1">${Array.from({ length: 6 }, () => `<div class="box"><div style="font-size:1.4vh;line-height:2.4">Fund: __________<br>Goal: ______</div>
  <table style="margin-top:1vh">${Array.from({ length: 9 }, () => '<tr><td style="height:2.8vh"></td><td></td></tr>').join('')}</table></div>`).join('')}</div>${FT}</div>`);
budget.push(`<div class="pg">${head('Challenge', 'No-Spend Challenge · ____________')}
  <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:1.5vh 1.5vw;margin-top:2vh">${Array.from({ length: 30 }, (_, i) => `<div style="aspect-ratio:1;border:1px solid ${C.sage};border-radius:12px;display:flex;align-items:flex-start;justify-content:flex-start;padding:.8vh .8vw;font-size:1.6vh;color:${C.terra}">${i + 1}</div>`).join('')}</div>
  <div class="box" style="margin-top:3vh;flex:1;display:flex;flex-direction:column"><h2>What I saved / what I learned</h2><div class="lines"></div></div>${FT}</div>`);

(async () => {
  const b = await chromium.launch();
  for (const [slug, pages] of [['2027-planner', planner], ['budget-planner', budget]]) {
    for (const fmt of ['Letter', 'A4']) {
      const p = await b.newPage();
      await p.setViewportSize(fmt === 'Letter' ? { width: 816, height: 1056 } : { width: 794, height: 1123 });
      await p.setContent(`<!doctype html><html><head><meta charset="utf-8">${FONTS}<style>${css}</style></head><body>${pages.join('')}</body></html>`, { waitUntil: 'networkidle' });
      await p.evaluate(() => document.fonts.ready);
      await p.pdf({ path: path.join(OUT, `${slug}-${fmt}.pdf`), format: fmt, printBackground: true });
      await p.close();
    }
    console.log(slug, pages.length, 'pages');
  }
  await b.close();
})();
