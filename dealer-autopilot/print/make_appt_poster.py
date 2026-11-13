import segno, io
exec(open('make_cards.py').read().split('def svg')[0])  # reuse vcard
def svg(data, color):
    b = io.BytesIO(); segno.make(data, error='q').save(b, kind='svg', dark=color, light=None, border=0, xmldecl=False, svgns=True, omitsize=True)
    return b.getvalue().decode()
Q = svg(appt, "#0b1d31")
html = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--navy:#0b1d31;--navy2:#13304f;--steel:#5d6e80;--ice:#eaf1f8;--line:#d3dde7;--accent:#3a8fd6;--display:'Archivo','Helvetica Neue',Arial,sans-serif;--body:'Inter','Helvetica Neue',Arial,sans-serif}}
@page{{size:letter;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--body);color:var(--navy);-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{width:8.5in;height:11in;position:relative;overflow:hidden;background:#fff;display:flex;flex-direction:column}}
.top{{position:relative;background:linear-gradient(160deg,var(--navy2) 0%,var(--navy) 70%);color:#fff;padding:.6in .8in 1.75in;overflow:hidden}}
.top svg.lines{{position:absolute;inset:0;width:100%;height:100%;opacity:.16}}
.brand{{position:relative;display:flex;justify-content:space-between;align-items:center;font-size:10pt;letter-spacing:.2em;text-transform:uppercase;font-weight:600;color:#bcd4ec}}
.brand b{{font-family:var(--display);color:#fff;letter-spacing:.14em;font-weight:800}}
.eyebrow{{position:relative;margin-top:.4in;display:inline-flex;align-items:center;gap:.12in;font-size:10.5pt;letter-spacing:.24em;text-transform:uppercase;color:var(--accent);font-weight:700}}
.eyebrow::before{{content:"";width:.45in;height:2px;background:var(--accent)}}
h1{{position:relative;font-family:var(--display);font-weight:900;font-size:56pt;line-height:.95;letter-spacing:-.02em;margin-top:.12in}}
.lede{{position:relative;font-size:13pt;line-height:1.45;color:#c9d9ea;margin-top:.2in;max-width:5.4in}}
.card{{position:relative;margin:-1.3in auto 0;width:4.3in;background:#fff;border-radius:.3in;padding:.32in;box-shadow:0 .12in .4in rgba(11,29,49,.22),0 0 0 1px var(--line);display:flex;flex-direction:column;align-items:center;gap:.16in;z-index:2}}
.qr{{width:3.6in;height:3.6in;position:relative}}
.qr svg{{width:100%;height:100%;display:block}}
.corner{{position:absolute;width:.42in;height:.42in;border:4px solid var(--accent)}}
.c1{{top:-.16in;left:-.16in;border-right:0;border-bottom:0;border-top-left-radius:.12in}}
.c2{{top:-.16in;right:-.16in;border-left:0;border-bottom:0;border-top-right-radius:.12in}}
.c3{{bottom:-.16in;left:-.16in;border-right:0;border-top:0;border-bottom-left-radius:.12in}}
.c4{{bottom:-.16in;right:-.16in;border-left:0;border-top:0;border-bottom-right-radius:.12in}}
.scan{{font-family:var(--display);font-weight:800;font-size:12pt;letter-spacing:.3em;text-transform:uppercase;color:var(--navy);margin-top:.08in}}
.steps{{display:flex;justify-content:center;gap:.45in;margin-top:.38in}}
.step{{display:flex;align-items:center;gap:.1in;font-size:11pt;font-weight:500}}
.step i{{font-style:normal;width:.32in;height:.32in;border-radius:50%;background:var(--navy);color:#fff;font-family:var(--display);font-weight:800;font-size:10pt;display:flex;align-items:center;justify-content:center}}
.who{{margin:auto .8in .0in;display:flex;justify-content:space-between;align-items:flex-end;border-top:1.5px solid var(--line);padding:.26in 0 .3in}}
.name{{font-family:var(--display);font-weight:900;font-size:26pt;letter-spacing:-.01em;line-height:1}}
.role{{font-size:9.5pt;letter-spacing:.2em;text-transform:uppercase;color:var(--accent);font-weight:700;margin-top:.07in}}
.contact{{text-align:right;font-size:11pt;line-height:1.55;color:var(--steel)}}
.contact b{{color:var(--navy);font-weight:600}}
.bar{{height:.22in;background:linear-gradient(90deg,var(--navy) 0 70%,var(--accent) 70% 100%)}}
</style></head><body><div class="page">
<div class="top">
<svg class="lines" viewBox="0 0 850 500" preserveAspectRatio="none" fill="none" stroke="#9cc6ee" stroke-width="2">
{''.join(f'<path d="M{-200+i*70} 520 C {150+i*60} 330, {380+i*45} 260, {900+i*20} {-40+i*18}"/>' for i in range(12))}
</svg>
<div class="brand"><b>Centereach Hyundai</b><span>Sales</span></div>
<div class="eyebrow">Book a visit</div>
<h1>Schedule your<br>appointment.</h1>
<p class="lede">Scan to send me a quick note with a day and time. I'll confirm it with you personally.</p>
</div>
<div class="card"><div class="qr">{Q}<span class="corner c1"></span><span class="corner c2"></span><span class="corner c3"></span><span class="corner c4"></span></div><div class="scan">Scan me</div></div>
<div class="steps"><div class="step"><i>1</i>Open your camera</div><div class="step"><i>2</i>Point at the code</div><div class="step"><i>3</i>Pick a time, tap send</div></div>
<div class="who"><div><div class="name">Nolan Mooney</div><div class="role">Sales Consultant</div></div>
<div class="contact"><b>631-671-2321</b><br>nmooney@trzmotors.com<br>1815 Middle Country Rd, Centereach, NY 11720</div></div>
<div class="bar"></div>
</div></body></html>"""
open('nolan-appointment-sign.html','w').write(html)
