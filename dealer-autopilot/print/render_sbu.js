const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + __dirname + '/nolan-stonybrook-flyer.html'); await p.waitForTimeout(1500);
  await p.pdf({ path: __dirname + '/Nolan-Mooney-StonyBrook-Flyer.pdf', format: 'Letter', printBackground: true, preferCSSPageSize: true });
  await p.setViewportSize({ width: 816, height: 1056 });
  await p.screenshot({ path: '/tmp/claude-0/-home-user-skills/746cb3ae-a1c8-5681-a585-aaab40805249/scratchpad/sbu.png', fullPage: true });
  await b.close();
})();
