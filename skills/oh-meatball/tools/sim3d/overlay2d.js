// 2D compositor: copies the WebGL frame into a 2D canvas, draws the text overlay there, returns a JPEG.
// Much faster than a page screenshot (no DOM raster + PNG round trip). Coordinates are in 1080x1920 space.
// The 3D canvas may be smaller (fast SwiftShader pass); it is upscaled here and the text is drawn at full output res.
export function makeCompositor(glCanvas, outW = 1080, outH = 1920) {
  const out = document.createElement('canvas');
  out.width = outW; out.height = outH;
  const ctx = out.getContext('2d');
  ctx.imageSmoothingQuality = 'high';
  // portrait: k = width / 1080. Landscape (16:9 long-form): the same 1080x1920 text space, scaled to the frame
  // height and centred (captions and cards sit in the middle column; WIDE_K enlarges them a little).
  const wide = outW > outH;
  const k = wide ? (outH / 1920) * (globalThis.WIDE_K || 1.25) : out.width / 1080;
  // the fact card (text y >= 170) sits ~12 px under the frame top; captions land at ~82% of the height
  const ox = wide ? (outW - 1080 * k) / 2 : 0, oy = wide ? Math.max((outH - 1920 * k) / 2, 12 - 160 * k) : 0;
  return {
    ctx, wide,
    begin() { ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.drawImage(glCanvas, 0, 0, outW, outH); ctx.setTransform(k, 0, 0, k, ox, oy); },
    jpeg(q = 0.92) { return out.toDataURL('image/jpeg', q); },
  };
}

export function shadowOn(ctx, blur = 10, oy = 2, a = 0.55) { ctx.shadowColor = `rgba(0,0,0,${a})`; ctx.shadowBlur = blur; ctx.shadowOffsetY = oy; ctx.shadowOffsetX = 0; }
export function shadowOff(ctx) { ctx.shadowColor = 'transparent'; ctx.shadowBlur = 0; ctx.shadowOffsetY = 0; }

// Rich text: runs = [[text, color], ...]; wraps on spaces within maxW; centered on cx; returns bottom y.
export function richText(ctx, runs, cx, top, maxW, font, lineH, opts = {}) {
  ctx.font = font; ctx.textBaseline = 'alphabetic'; ctx.letterSpacing = opts.spacing || '0px';
  const words = [];
  for (const [txt, col] of runs) for (const w of txt.split(/(\s+)/)) if (w) words.push([w, col]);
  const lines = []; let cur = [], wsum = 0;
  for (const [w, col] of words) {
    const ww = ctx.measureText(w).width;
    if (/^\s+$/.test(w)) { if (cur.length) { cur.push([w, col, ww]); wsum += ww; } continue; }
    if (wsum + ww > maxW && cur.length) { while (cur.length && /^\s+$/.test(cur[cur.length - 1][0])) wsum -= cur.pop()[2]; lines.push([cur, wsum]); cur = []; wsum = 0; }
    cur.push([w, col, ww]); wsum += ww;
  }
  if (cur.length) lines.push([cur, wsum]);
  let y = top + lineH * 0.8;
  for (const [ln, w] of lines) {
    let x = cx - w / 2;
    for (const [t, col, ww] of ln) {
      if (opts.stroke) { ctx.lineJoin = 'round'; ctx.lineWidth = opts.stroke; ctx.strokeStyle = '#000'; ctx.strokeText(t, x, y); }
      ctx.fillStyle = col; ctx.fillText(t, x, y); x += ww;
    }
    y += lineH;
  }
  return y;
}
