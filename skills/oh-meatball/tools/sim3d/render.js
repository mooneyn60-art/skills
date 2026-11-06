// Deterministic frame renderer: headless Chromium + Three.js -> JPEG frames -> ffmpeg (H.264, 30 fps).
// node render.js --page src/index.html --out a.mp4 [--from 0 --to 51 --fps 30 --scale 1]
// node render.js --page src/index.html --stills 0,5,10 --outdir stills/   (PNG checks)
const http = require('http'), fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.ttf': 'font/ttf', '.json': 'application/json', '.glb': 'model/gltf-binary', '.png': 'image/png', '.jpg': 'image/jpeg' };

(async () => {
  const server = http.createServer((req, res) => {
    const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
    if (!p.startsWith(ROOT) || !fs.existsSync(p)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(res);
  }).listen(0);
  const port = server.address().port;
  const scale = parseFloat(arg('scale', '1'));
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: +arg('w', '1080'), height: +arg('h', '1920') }, deviceScaleFactor: scale });
  page.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') console.error('[page]', m.text()); });
  page.on('pageerror', (e) => console.error('[pageerror]', e.message));
  await page.goto(`http://127.0.0.1:${port}/${arg('page', 'src/index.html')}`);
  await page.waitForFunction(() => window.SIM, null, { timeout: 120000 });
  await page.evaluate(() => window.SIM.ready);
  const t0 = Date.now();
  const stills = arg('stills');
  if (stills) {
    const outdir = arg('outdir', 'work/stills'); fs.mkdirSync(outdir, { recursive: true });
    for (const s of stills.split(',').map(Number)) {
      const url = await page.evaluate((t) => window.SIM.frame(t, 0.95), s);
      fs.writeFileSync(path.join(outdir, `t${String(s).padStart(5, '0')}.jpg`), Buffer.from(url.slice(url.indexOf(',') + 1), 'base64'));
    }
    console.log(`stills ${stills} in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
  } else {
    const fps = +arg('fps', '30'), total = await page.evaluate(() => window.SIM.TOTAL);
    const from = +arg('from', '0'), to = +arg('to', String(total));
    const f0 = Math.round(from * fps), f1 = Math.round(to * fps);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-movflags', '+faststart', arg('out', 'work/out.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let f = f0; f < f1; f++) {
      const url = await page.evaluate((t) => window.SIM.frame(t, 0.93), f / fps);
      const buf = Buffer.from(url.slice(url.indexOf(',') + 1), 'base64');
      if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
      if ((f - f0) % 60 === 0) console.log(`frame ${f}/${f1} ${((Date.now() - t0) / 1000 / (f - f0 + 1)).toFixed(2)} s/frame`);
    }
    ff.stdin.end(); await new Promise((r) => ff.on('close', r));
    console.log(`rendered ${f1 - f0} frames in ${((Date.now() - t0) / 1000).toFixed(0)} s`);
  }
  await browser.close(); server.close();
})().catch((e) => { console.error(e); process.exit(1); });
