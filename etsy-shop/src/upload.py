"""Send listings to the Make webhook, which creates them on Etsy.
Usage: python3 src/upload.py <slug> [<slug> ...]"""
import subprocess, sys, os

HOOK = open(os.path.join(os.path.dirname(__file__), "..", ".make_hook")).read().strip()  # private, git-ignored
ROOT = os.path.join(os.path.dirname(__file__), "..")
P, I = f"{ROOT}/products", f"{ROOT}/listing-images"

FOOTER = """
⚡ INSTANT DOWNLOAD
This is a digital file. No physical item will be shipped. After purchase, go to You > Purchases and Reviews > Download Files. You'll also get an email with the download link.

🖨️ PRINTING TIPS
• Print at home or at any print shop (Staples, Office Depot, Walgreens, etc.)
• For best results use white cardstock and choose "Actual size" / 100%
• Print as many copies as your household needs

✨ COMPLETE THE SET
This design is part of our matching Santa Mail collection: Dear Santa letter, Reply from Santa, Christmas Wish List, Nice List Certificate & Christmas Elf Arrival Letter. Get all 5 in the Santa Mail Set bundle and save!

❓ FAQ
Will I receive a physical item? No, this is a digital download only.
Can I edit it on the computer? This version is designed to be filled in by hand.
Can I print it more than once? Yes, for personal and family use.
Refunds? Digital items can't be returned, but if anything is wrong with your file, message me and I'll make it right!

© DoodleDesignAndCo. Original artwork. For personal use only. Please do not resell or share the file."""

L = {
  "reply-from-santa-letter": dict(
    title="Letter from Santa Printable, Reply from Santa Template for Kids, Nice List Santa Letter, Instant Download PDF Letter & A4",
    price="3.49", publish="yes",
    tags="letter from santa,reply from santa,santa reply letter,nice list letter,north pole letter,santa letter pdf,christmas printable,santa claus letter,kids christmas,christmas eve box,north pole mail,santa note for kids,santa letter kids",
    intro="""Printable Letter from Santa. Make Christmas magical with a personal reply straight from the North Pole! This festive "From the Desk of Santa Claus" letter has space to add your child's name and personal notes, plus Santa's official Nice List checkbox.

🎅 WHAT'S INCLUDED
• Reply from Santa letter (PDF) in US Letter (8.5 × 11 in) AND A4
• Pre-written heartfelt letter from Santa with fill-in blanks to personalize
• "North Pole Official Mail" stamp, Nice List / Naughty List checkboxes
• Original hand-drawn Santa, reindeer & gift artwork
"""),
  "nice-list-certificate": dict(
    title="Nice List Certificate Printable, Santa's Official Nice List Award for Kids, Christmas Certificate, Instant Download PDF",
    price="3.29", publish="yes",
    tags="nice list award,santa nice list,nice list printable,christmas award,santa certificate,official nice list,kids christmas award,north pole document,christmas eve box,christmas printable,santa claus,nice list kids,stocking stuffer",
    intro="""Printable Nice List Certificate. Officially certify that your child made Santa's Nice List this year! Signed by Santa Claus and Jingle the Head Elf with a gold "Nice List Approved" seal. Perfect for Christmas Eve boxes, stockings, or tucking under the tree.

🏅 WHAT'S INCLUDED
• Nice List Certificate (PDF) in US Letter AND A4, landscape
• Fill-in lines for your child's name and the year
• Original holly, gingerbread & candy cane artwork
"""),
  "christmas-wish-list": dict(
    title="Christmas Wish List Printable for Kids, Dear Santa Wish List Template, Kids Christmas List, Instant Download PDF Letter & A4",
    price="2.99", publish="yes",
    tags="christmas wish list,kids wish list,santa wish list,kids christmas list,wish list printable,christmas list kids,dear santa list,letter to santa,christmas printable,christmas activity,holiday wish list,gift list for kids,wish list template",
    intro="""Printable Christmas Wish List for kids. Let your little ones write (or draw!) everything they're wishing for this year. Includes space for name, age, 5 wishes, a "Draw your #1 wish" box, and "Something nice I did this year."

🎁 WHAT'S INCLUDED
• Kids Christmas Wish List (PDF) in US Letter (8.5 × 11 in) AND A4
• Original gift, star, snowman & Christmas tree artwork with candy-stripe border
• Great for siblings, classrooms, and grandparents' gift planning
"""),
  "christmas-elf-arrival-letter": dict(
    title="Christmas Elf Arrival Letter Printable, Elf Hello Letter for Kids, Elf Rules, North Pole Welcome Note, Instant Download PDF",
    price="3.29", publish="yes",
    tags="elf arrival letter,elf letter,christmas elf,elf rules,elf welcome letter,elf is back letter,scout elf letter,elf printable,north pole letter,elf ideas,christmas printable,elf hello note,kids christmas",
    intro="""Printable Christmas Elf Arrival Letter. Kick off the season with a magical welcome note from your family's Christmas elf! Fill in your child's name and the elf's name, and share the Elf Rules: don't touch, talk anytime, be kind, and the elf flies home on Christmas Eve.

🧝 WHAT'S INCLUDED
• Christmas Elf arrival letter (PDF) in US Letter (8.5 × 11 in) AND A4
• Fill-in blanks for child's name, elf's name and signature
• Original elf, candy cane & gift artwork
"""),
  "bundle": dict(
    title="Santa Mail Bundle Printable, Letter to Santa, Reply from Santa, Nice List Certificate, Wish List & Elf Letter, Kids Christmas Set",
    price="7.99", publish="no",
    tags="santa letter bundle,santa mail kit,letter to santa,letter from santa,nice list printable,christmas wish list,elf arrival letter,north pole mail,christmas printable,santa letter set,christmas eve box,kids christmas,christmas bundle",
    intro="""Santa Mail Bundle: 5 matching Christmas printables in one instant download! Everything you need for a magical North Pole mail tradition, for less than buying them separately.

📦 WHAT'S INCLUDED (one PDF, 5 pages)
1. Dear Santa letter, for kids to write their wishes
2. Reply from Santa letter
3. Christmas Wish List
4. Nice List Certificate
5. Christmas Elf Arrival Letter
"""),
}

PFOOTER = """
⚡ INSTANT DOWNLOAD
This is a digital file. No physical item will be shipped. After purchase, go to You > Purchases and Reviews > Download Files.

🖨️ PRINTING TIPS
• Print at home or at any print shop, in color or black & white
• Choose "Actual size" / 100%. Print single pages or the whole set, as often as you need
• Fits standard binders, discbound systems and clipboards (3-hole punch friendly margins)

❓ FAQ
Is this a physical planner? No, it's a printable PDF download.
Can I use it on a tablet (GoodNotes/Notability)? Yes! Import the PDF and write on it digitally.
Can I print more than once? Yes, for personal use.
Refunds? Digital items can't be returned, but if anything is wrong with your file, message me and I'll make it right!

© DoodleDesignAndCo. Original design. For personal use only. Please do not resell or share the file."""

L["2027-planner"] = dict(
    title="2027 Planner Printable, Minimalist Monthly Planner, Weekly & Daily Planner Pages, Habit Tracker, Goal Planner, Instant Download PDF",
    price="5.99", publish="yes", footer=PFOOTER,
    imgs=["planner-01-thumbnail", "planner-02-pages", "planner-03-included", "planner-04-daily"],
    tags="2027 planner,printable planner,2027 calendar,planner printable,monthly planner,weekly planner,daily planner,minimalist planner,habit tracker,goal planner,2027 planner pdf,yearly planner,planner inserts",
    intro="""2027 Printable Planner. Get organized for the new year with this clean, minimalist planner in a calming sage & neutral palette. 19 pages to plan your year, months, weeks and days, then print only what you need.

📅 WHAT'S INCLUDED (19 pages, US Letter AND A4 PDF)
• Cover page
• 2027 Year at a Glance
• 2027 Goals page (6 life areas + word of the year)
• 12 dated monthly calendars, January to December 2027, with notes & to-do
• Undated weekly planner
• Undated daily planner with hourly schedule, priorities, water & gratitude
• Monthly habit tracker
• Notes page
""")
L["budget-planner"] = dict(
    title="Budget Planner Printable, Monthly Budget Tracker, Expense and Bill Tracker, Savings & Debt Payoff Tracker, Finance Planner PDF",
    price="4.99", publish="yes", footer=PFOOTER,
    imgs=["budget-01-thumbnail", "budget-02-pages", "budget-03-included", "budget-04-detail"],
    tags="budget planner,budget tracker,expense tracker,bill tracker,savings tracker,debt payoff tracker,finance planner,budget printable,monthly budget,sinking funds,no spend challenge,budget template,money planner",
    intro="""Printable Budget Planner. Take control of your money with this simple, minimalist finance planner. Track income, spending, bills, savings goals and debt payoff in one place. Undated, so you can start any month!

💰 WHAT'S INCLUDED (9 pages, US Letter AND A4 PDF)
• Cover page
• Annual budget overview (12 months)
• Monthly budget: income, fixed & variable expenses, savings & debt
• Expense tracker
• Bill payment tracker (12-month checklist)
• Savings goal tracker (color-in circles)
• Debt payoff tracker
• Sinking funds tracker (6 funds)
• 30-day no-spend challenge
""")

L["2027-wall-calendar"] = dict(
    title="2027 Wall Calendar Printable, Minimalist Botanical Monthly Calendar, Landscape Calendar 2027, Instant Download PDF Letter & A4",
    price="3.99", publish="yes", footer=PFOOTER,
    imgs=["calendar-01-thumbnail", "calendar-02-pages", "calendar-03-detail", "calendar-04-included"],
    tags="2027 calendar,wall calendar,printable calendar,2027 wall calendar,monthly calendar,botanical calendar,calendar printable,minimalist calendar,2027 printable,desk calendar,family calendar,calendar 2027 pdf,boho calendar",
    intro="""2027 Printable Wall Calendar. A calm, minimalist botanical calendar with a different soft color for every month. Print it at home, hang it on the fridge or clip it to a board, and start the new year organized.

🌿 WHAT'S INCLUDED (13 pages, landscape, US Letter AND A4 PDF)
• Cover page
• 12 monthly calendars, January to December 2027 (Sunday start)
• Notes section on every month
• Large date boxes for appointments, birthdays & plans
""")

def send(slug):
    d = L[slug]
    if slug == "bundle":
        imgs = ["bundle-01-thumbnail", "bundle-02-whats-included", "dear-santa-03-how-it-works", "dear-santa-04-matching-set"]
        pdfs = [("BUNDLE-Santa-Mail-Set-Letter.pdf", "Santa-Mail-Set-Bundle-DoodleDesignAndCo.pdf")]
    elif "imgs" in d:
        imgs = d["imgs"]
        pdfs = [(f"{slug}-Letter.pdf", f"{slug}-US-Letter.pdf"), (f"{slug}-A4.pdf", f"{slug}-A4.pdf")]
    else:
        imgs = [f"{slug}-01-thumbnail", f"{slug}-02-whats-included", "dear-santa-03-how-it-works", "dear-santa-04-matching-set"]
        pdfs = [(f"{slug}-Letter.pdf", f"{slug}-US-Letter.pdf"), (f"{slug}-A4.pdf", f"{slug}-A4.pdf")]
    name = d["title"].split(",")[0]
    alts = [f"{name} printable mockup", f"{name}: all pages preview" if "imgs" in d else f"What's included: {name} PDF, instant download",
            f"What's included: {name} PDF" if "imgs" in d else "How it works: purchase, download, print",
            f"{name} page details" if "imgs" in d else "Matching Santa Mail printable set"]
    desc = d["intro"] + d.get("footer", FOOTER)
    args = ["curl", "-sS", "-w", " HTTP %{http_code}", HOOK,
            "-F", f"slug={slug}", "-F", f"title={d['title']}", "-F", f"price={d['price']}",
            "-F", "taxonomy=1250", "-F", f"tags={d['tags']}", "-F", f"publish={d['publish']}",
            "-F", f"description={desc}"]
    for n, (im, alt) in enumerate(zip(imgs, alts), 1):
        args += ["-F", f"img{n}=@{I}/{im}.jpg;type=image/jpeg", "-F", f"alt{n}={alt}"]
    for n, (f, fn) in enumerate(pdfs):
        args += ["-F", f"pdf{n + 1 if n else ''}=@{P}/{f};filename={fn};type=application/pdf"]
    for t in d["tags"].split(","):
        assert len(t) <= 20, t
    assert len(d["tags"].split(",")) == 13 and len(d["title"]) <= 140
    print(slug, subprocess.run(args, capture_output=True, text=True).stdout)

for s in sys.argv[1:]:
    send(s)
