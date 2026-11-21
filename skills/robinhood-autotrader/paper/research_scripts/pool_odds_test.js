const fs = require("fs");
const html = fs.readFileSync(process.argv[2], "utf8"), hist = JSON.parse(fs.readFileSync(process.argv[3]));
const a = html.indexOf("// ---------- indicators ----------"), b = html.indexOf("function canvasCtx");
const etHM = t => new Intl.DateTimeFormat("en-GB", {timeZone: "America/New_York", hour: "2-digit", minute: "2-digit", hour12: false}).format(t);
const etDay = t => new Intl.DateTimeFormat("en-CA", {timeZone: "America/New_York"}).format(t);
eval(html.slice(a, b).replace(/^function (\w+)/gm, "global.$1 = function $1"));
const days = {};
for (const [k, v] of Object.entries(hist)) { const t = new Date(k + ":00Z"), hm = etHM(t); if (hm < "09:30" || hm >= "16:00") continue;
  (days[etDay(t)] = days[etDay(t)] || []).push({t, hm, o: v[0], h: v[1], l: v[2], c: v[3], v: v[4] || 0}); }
const ds = Object.keys(days).sort(); const rows = [];
for (let di = 1; di < ds.length; di++) {
  const day = days[ds[di]].sort((x, y) => x.t - y.t), prev = days[ds[di - 1]];
  for (let i = 30; i < day.length - 30; i += 5) {
    const bars = day.slice(0, i + 1).map(x => ({...x})); indicators(bars); const st = structure(bars, prev), c = bars[i].c;
    const up = st.pools.filter(p => p.p > c && !p.taken).sort((x, y) => x.p - y.p)[0], dn = st.pools.filter(p => p.p < c && !p.taken).sort((x, y) => y.p - x.p)[0];
    if (!up || !dn) continue;
    let res = null; for (let k = i + 1; k < day.length; k++) { const hU = day[k].h >= up.p, hD = day[k].l <= dn.p; if (hU && hD) break; if (hU) { res = 1; break; } if (hD) { res = 0; break; } }
    if (res === null) continue;
    const dA = up.p - c, dB = c - dn.p, last = bars[i];
    rows.push({d: ds[di], pu: dB / (dA + dB), res, trend: last.trend, sig: (c - last.vwap) / (last.sd || 1), macd: last.macd > last.msig ? 1 : -1, rsi: last.rsi});
  }
}
const brier = f => rows.reduce((s, r) => s + (f(r) - r.res) ** 2, 0) / rows.length;
console.log("n", rows.length, "days", new Set(rows.map(r => r.d)).size, "up-first rate", (rows.filter(r => r.res).length / rows.length).toFixed(3));
console.log("brier 0.5:", brier(() => 0.5).toFixed(4), " distance:", brier(r => r.pu).toFixed(4));
for (const [lo, hi] of [[0, .2], [.2, .4], [.4, .6], [.6, .8], [.8, 1.01]]) { const g = rows.filter(r => r.pu >= lo && r.pu < hi); if (g.length) console.log(`pred ${lo}-${hi}: n ${g.length} actual up ${(g.filter(r => r.res).length / g.length).toFixed(2)} mean pred ${(g.reduce((s, r) => s + r.pu, 0) / g.length).toFixed(2)}`); }
for (const [name, f] of [["trend", r => r.trend], ["macd", r => r.macd], ["vwap side", r => Math.sign(r.sig)], ["rsi>50", r => r.rsi > 50 ? 1 : -1]]) {
  // residual: does the factor shift outcome beyond distance?
  const g1 = rows.filter(r => f(r) > 0), g0 = rows.filter(r => f(r) < 0);
  const res = g => g.reduce((s, r) => s + r.res - r.pu, 0) / (g.length || 1);
  console.log(name, "+: n", g1.length, "excess up", res(g1).toFixed(3), " -: n", g0.length, "excess up", res(g0).toFixed(3));
}
