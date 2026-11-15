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

def send(slug):
    d = L[slug]
    if slug == "bundle":
        imgs = ["bundle-01-thumbnail", "bundle-02-whats-included", "dear-santa-03-how-it-works", "dear-santa-04-matching-set"]
        pdfs = [("BUNDLE-Santa-Mail-Set-Letter.pdf", "Santa-Mail-Set-Bundle-DoodleDesignAndCo.pdf")]
    else:
        imgs = [f"{slug}-01-thumbnail", f"{slug}-02-whats-included", "dear-santa-03-how-it-works", "dear-santa-04-matching-set"]
        pdfs = [(f"{slug}-Letter.pdf", f"{slug}-US-Letter.pdf"), (f"{slug}-A4.pdf", f"{slug}-A4.pdf")]
    name = d["title"].split(",")[0]
    alts = [f"{name} printable mockup", f"What's included: {name} PDF, instant download",
            "How it works: purchase, download, print", "Matching Santa Mail printable set"]
    desc = d["intro"] + FOOTER
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
