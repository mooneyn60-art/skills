// Replace the misspelled "Santa Clause" signature on the coloring book's last page with "Santa Claus".
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const W = path.join(__dirname, '..', 'work');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 2482, height: 3510 } });
  const bg = 'data:image/png;base64,' + fs.readFileSync(path.join(W, 'note300.png')).toString('base64');
  await p.setContent(`<html><head><link href="https://fonts.googleapis.com/css2?family=Great+Vibes&display=block" rel="stylesheet"></head>
  <body style="margin:0;position:relative;width:2482px;height:3510px">
  <img src="${bg}" style="position:absolute;inset:0;width:2482px;height:3510px">
  <div style="position:absolute;left:780px;top:2215px;width:1500px;height:340px;background:rgb(30,48,37)"></div>
  <div style="position:absolute;left:790px;top:2190px;font-family:'Great Vibes';font-size:330px;color:#e8343a;-webkit-text-stroke:7px #fff;paint-order:stroke fill;white-space:nowrap">Santa Claus</div>
  </body></html>`, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(W, 'note-fixed.png') });
  await b.close();
})();
