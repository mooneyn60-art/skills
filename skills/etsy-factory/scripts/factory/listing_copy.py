"""Listing copy: build the description and enforce Etsy's title/tag rules plus our originality rules."""

import json
import re

TITLE_MAX = 140
TAG_MAX = 20
TAG_COUNT = 13
TAG_RE = re.compile(r"^[A-Za-z0-9 '\-]+$")
TITLE_RE = re.compile(r"^[A-Za-z0-9 ,.'&:|+%\-()/]+$")
# Etsy allows %, :, & and + at most once each in a title.
TITLE_ONCE = "%:&+"

# Brands, characters and trademarked game names we must never use. Extend as needed.
BANNED = [
    "disney", "pixar", "marvel", "grinch", "rudolph", "frosty", "elf on the shelf", "charlie brown", "peanuts",
    "snoopy", "hallmark", "family feud", "scattergories", "pictionary", "scrabble", "monopoly", "jeopardy",
    "wheel of fortune", "taboo", "boggle", "yahtzee", "uno", "pokemon", "barbie", "lego", "harry potter",
    "star wars", "minecraft", "bluey", "cocomelon", "taylor swift", "nfl", "nba", "coca", "starbucks",
    "home alone", "polar express", "the office", "cricut", "canva", "dollar tree", "costco", "trader joe",
    "dave ramsey", "baby shark", "paw patrol", "hello kitty", "squishmallow", "wordle", "sudoku daily",
]
# House rule for this shop: none of our listings or files mention motor vehicles.
OFF_TOPIC = re.compile(r"\b(cars?|trucks?|automobiles?|vehicles?)\b", re.I)


def banned_hits(text):
    low = text.lower()
    hits = [b for b in BANNED if re.search(rf"\b{re.escape(b)}\b", low)]
    if OFF_TOPIC.search(text):
        hits.append(OFF_TOPIC.search(text).group(0))
    return hits


def validate(listing, all_text):
    errs = []
    title = listing["title"]
    if len(title) > TITLE_MAX:
        errs.append(f"title is {len(title)} chars (max {TITLE_MAX})")
    if not TITLE_RE.match(title):
        errs.append("title has characters Etsy rejects")
    for ch in TITLE_ONCE:
        if title.count(ch) > 1:
            errs.append(f"title uses '{ch}' more than once")
    tags = listing["tags"]
    if len(tags) != TAG_COUNT:
        errs.append(f"{len(tags)} tags (need exactly {TAG_COUNT})")
    if len({t.lower() for t in tags}) != len(tags):
        errs.append("duplicate tags")
    for tg in tags:
        if len(tg) > TAG_MAX:
            errs.append(f"tag '{tg}' is {len(tg)} chars (max {TAG_MAX})")
        if not TAG_RE.match(tg):
            errs.append(f"tag '{tg}' has invalid characters")
    price = listing["price"]
    if not 0.20 <= price <= 50000:
        errs.append("price out of Etsy range")
    hits = banned_hits(all_text)
    if hits:
        errs.append(f"banned or off-topic terms: {sorted(set(hits))}")
    if errs:
        raise SystemExit("Listing copy failed checks:\n  - " + "\n  - ".join(errs))


def description(spec):
    L = spec["listing"]
    bullets = "\n".join(f"• {i}" for i in spec["included"])
    details = "\n".join(f"• {d}" for d in L.get("details", []))
    return f"""{L['intro']}

WHAT'S INCLUDED
{bullets}

DETAILS
• Instant digital download: PDF files in US Letter (8.5 x 11 in) and A4 (210 x 297 mm)
{details}
• Print at home or at any print shop, as many copies as you need for your own use

HOW TO DOWNLOAD
1. Complete your purchase.
2. On Etsy, go to You > Purchases and reviews and click Download Files. Etsy also emails you a link.
3. Open the PDF and print. "Fit to page" or "Actual size" both work.

PLEASE NOTE
• This is a digital product. No physical item will be shipped.
• Colors can look slightly different on screens and printers.
• For personal, family and classroom use. Please do not resell, share or redistribute the files.
• Because this is an instant download, returns are not accepted. If anything is wrong with your file, send me a message and I will fix it right away.

All puzzles, questions, artwork and layouts are original designs.
"""


def build(spec, out_dir, files):
    L = spec["listing"]
    desc = description(spec)
    corpus = json.dumps(spec) + desc
    validate(L, corpus)
    listing = {
        "slug": spec["slug"],
        "title": L["title"],
        "description": desc,
        "price": L["price"],
        "tags": L["tags"],
        "materials": L.get("materials", ["digital download", "pdf"]),
        "taxonomy_path": L["taxonomy_path"],
        "taxonomy_id": L.get("taxonomy_id"),
        "who_made": "i_did",
        "when_made": "made_to_order",
        "is_supply": False,
        "type": "download",
        "quantity": 999,
        "should_auto_renew": True,
        "files": files["pdf"],
        "images": files["images"],
    }
    with open(f"{out_dir}/listing.json", "w", encoding="utf-8") as f:
        json.dump(listing, f, indent=2)
    with open(f"{out_dir}/listing.md", "w", encoding="utf-8") as f:
        f.write(f"# {L['title']}\n\n**Price:** ${L['price']:.2f}  \n**Tags:** {', '.join(L['tags'])}\n\n```\n{desc}```\n")
    return listing
