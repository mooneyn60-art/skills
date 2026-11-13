import segno, urllib.parse, io
vcard = "\r\n".join(["BEGIN:VCARD","VERSION:3.0","N:Mooney;Nolan","FN:Nolan Mooney","ORG:Centereach Hyundai","TITLE:Sales Consultant",
 "TEL;TYPE=WORK,VOICE:+16316712321","EMAIL;TYPE=WORK:nmooney@trzmotors.com","ADR;TYPE=WORK:;;1815 Middle Country Rd;Centereach;NY;11720;USA",
 "END:VCARD"])
body = "Hi Nolan, I would like to come in.\nDay and time: \nVehicle: \nMy phone: "
appt = "mailto:nmooney@trzmotors.com?subject=" + urllib.parse.quote("Appointment with Nolan") + "&body=" + urllib.parse.quote(body)
def svg(data, color="#0e2238"):
    b = io.BytesIO(); segno.make(data, error='m').save(b, kind='svg', dark=color, light=None, border=0, xmldecl=False, svgns=True, omitsize=True)
    return b.getvalue().decode()
V, A = svg(vcard), svg(appt)

def desk(kind):
    if kind == "card":
        eyebrow, head, sub, qr, steps = "Save my contact", "Let's stay in touch", "Point your phone camera here to add my number and email to your contacts.", V, ["Open your camera", "Point it at the code", "Tap “Add contact”"]
    else:
        eyebrow, head, sub, qr, steps = "Book a visit", "Schedule your appointment", "Scan to send me a quick note with a day and time. I'll confirm it with you personally.", A, ["Open your camera", "Point it at the code", "Pick a day and tap send"]
    return f"""<section class="desk">
  <div class="band"><span class="dealer">Centereach Hyundai</span><span class="eb">{eyebrow}</span></div>
  <div class="dbody">
    <div class="dtext">
      <h1>{head}</h1>
      <p class="sub">{sub}</p>
      <ol>{''.join(f'<li>{s}</li>' for s in steps)}</ol>
      <div class="sig"><b>Nolan Mooney</b><span>Sales Consultant</span><span>631-671-2321 · nmooney@trzmotors.com</span></div>
    </div>
    <div class="qrwrap"><div class="qr">{qr}</div><div class="cap">Scan me</div></div>
  </div>
  <div class="foot">1815 Middle Country Rd, Centereach, NY 11720 · centereachhyundai.com</div>
</section>"""

def pocket():
    return f"""<div class="pc">
  <div class="pl"><div class="pn">Nolan Mooney</div><div class="pt">Sales Consultant</div>
    <div class="pd">Centereach Hyundai</div><div class="pi">631-671-2321<br>nmooney@trzmotors.com<br>1815 Middle Country Rd<br>Centereach, NY 11720</div></div>
  <div class="pr"><div class="pq"><div class="q">{V}</div><span>Save my contact</span></div><div class="pq"><div class="q">{A}</div><span>Book a visit</span></div></div>
</div>"""

html = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--navy:#0e2238;--steel:#5b6b7c;--ice:#e9eff5;--line:#c9d3dd;--accent:#2f7fc1;--display:'Archivo','Helvetica Neue',Arial,sans-serif;--body:'Inter','Helvetica Neue',Arial,sans-serif}}
@page{{size:letter;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--body);color:var(--navy);-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{width:8.5in;height:11in;padding:.5in .75in;display:flex;flex-direction:column;gap:.5in;page-break-after:always;position:relative}}
.page:last-child{{page-break-after:auto}}
.desk{{width:7in;height:4.75in;border:1.5px solid var(--navy);border-radius:.18in;overflow:hidden;display:flex;flex-direction:column;background:#fff}}
.band{{background:var(--navy);color:#fff;display:flex;justify-content:space-between;align-items:center;padding:.16in .3in}}
.dealer{{font-family:var(--display);font-weight:700;letter-spacing:.06em;text-transform:uppercase;font-size:11pt}}
.eb{{font-size:9pt;letter-spacing:.14em;text-transform:uppercase;color:#bcd3ea;font-weight:600}}
.dbody{{flex:1;display:flex;gap:.35in;padding:.3in .3in .15in;align-items:center}}
.dtext{{flex:1;display:flex;flex-direction:column;gap:.13in}}
h1{{font-family:var(--display);font-weight:800;font-size:24pt;line-height:1.05;letter-spacing:-.01em}}
.sub{{font-size:10.5pt;line-height:1.4;color:var(--steel)}}
ol{{list-style:none;counter-reset:s;display:flex;flex-direction:column;gap:.05in}}
ol li{{counter-increment:s;font-size:10pt;display:flex;align-items:center;gap:.09in}}
ol li::before{{content:counter(s);width:.22in;height:.22in;border-radius:50%;background:var(--ice);color:var(--navy);font-weight:600;font-size:8.5pt;display:flex;align-items:center;justify-content:center}}
.sig{{display:flex;flex-direction:column;gap:2px;border-top:1px solid var(--line);padding-top:.1in;font-size:9pt;color:var(--steel)}}
.sig b{{font-family:var(--display);color:var(--navy);font-size:12pt}}
.qrwrap{{display:flex;flex-direction:column;align-items:center;gap:.08in}}
.qr{{width:2.45in;height:2.45in;padding:.14in;border:2px solid var(--navy);border-radius:.14in;background:#fff}}
.qr svg,.q svg{{width:100%;height:100%;display:block}}
.cap{{font-family:var(--display);font-weight:700;font-size:9pt;letter-spacing:.16em;text-transform:uppercase;color:var(--accent)}}
.foot{{background:var(--ice);font-size:8.5pt;color:var(--steel);text-align:center;padding:.09in}}
.note{{font-size:8pt;color:var(--steel);text-align:center;margin-top:auto}}
.grid{{display:grid;grid-template-columns:3.5in 3.5in;grid-auto-rows:2in;gap:0;margin:0 auto;border-top:1px dashed #aab;border-left:1px dashed #aab}}
.pc{{border-right:1px dashed #aab;border-bottom:1px dashed #aab;display:flex;gap:.1in;padding:.14in .14in .14in .16in;position:relative;background:#fff}}
.pc::before{{content:"";position:absolute;left:0;top:0;bottom:0;width:.07in;background:var(--navy)}}
.pl{{flex:1;display:flex;flex-direction:column;padding-left:.06in}}
.pn{{font-family:var(--display);font-weight:800;font-size:13pt;line-height:1.1}}
.pt{{font-size:7.5pt;color:var(--accent);text-transform:uppercase;letter-spacing:.12em;font-weight:600;margin-top:2px}}
.pd{{font-family:var(--display);font-weight:700;font-size:8pt;margin-top:.1in;text-transform:uppercase;letter-spacing:.05em}}
.pi{{font-size:7.3pt;line-height:1.4;color:var(--steel);margin-top:2px}}
.pr{{display:flex;gap:.07in;align-items:center}}
.pq{{display:flex;flex-direction:column;align-items:center;gap:3px}}
.q{{width:.82in;height:.82in}}
.pq span{{font-size:5.6pt;text-transform:uppercase;letter-spacing:.06em;color:var(--navy);font-weight:600;white-space:nowrap}}
</style></head><body>
<div class="page">{desk('card')}{desk('appt')}<p class="note">Cut along the outside edges. Each card fits a 5×7 frame or plastic sign holder.</p></div>
<div class="page" style="padding:.5in .75in">
<div class="grid">{''.join(pocket() for _ in range(10))}</div>
<p class="note">Cut on the dashed lines. Prints best on card stock (65–110 lb).</p></div>
</body></html>"""
open('nolan-cards.html','w').write(html)
