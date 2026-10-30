import cairo, sys
sys.path.insert(0, '.')
from drawn_anatomy import ANATOMY
names = list(ANATOMY)
cols, rows, cw, ch = 4, 3, 760, 760
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, cols*cw, rows*ch)
ctx = cairo.Context(surf)
ctx.set_source_rgb(0.93, 0.91, 0.86); ctx.paint()
for i, n in enumerate(names):
    r, c = divmod(i, cols)
    ctx.save(); ctx.translate(c*cw + cw/2, r*ch + ch - 90)
    s = {"cassowary": 0.75, "house_centipede": 0.75, "camel_cricket": 0.75, "cockroach": 0.8, "camel_spider": 0.9}.get(n, 1.0)
    ctx.scale(s, s)
    ctx.set_source_rgb(0.75,0.72,0.66); ctx.rectangle(-480, 0, 960, 8); ctx.fill()
    ANATOMY[n](ctx, 0.3, {"walk": 0.0})
    ctx.restore()
    ctx.set_source_rgb(0.1,0.1,0.1); ctx.select_font_face("sans", 0, 1); ctx.set_font_size(36)
    ctx.move_to(c*cw + 30, r*ch + 50); ctx.show_text(n.replace("_"," ").upper())
surf.write_to_png(sys.argv[1])
