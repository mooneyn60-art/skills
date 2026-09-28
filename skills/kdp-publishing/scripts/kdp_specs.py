"""Amazon KDP print and metadata specifications shared by every script in this skill.

Values follow KDP Help pages (Paperback manuscript/cover guidelines, Royalties,
Metadata guidelines). Amazon changes printing costs periodically; confirm the
figures in PRINT_COST against the KDP pricing calculator before relying on them.
"""

BLEED = 0.125  # inches, added to top, bottom and outside edge (interior) / all sides (cover)
MIN_PAGES = 24
MAX_PAGES = 828  # black ink on white/cream; some trims and color inks allow fewer
SPINE_TEXT_MIN_PAGES = 80  # KDP allows spine text only on books with more than 79 pages
SPINE_TEXT_MARGIN = 0.0625  # keep spine text this far from each fold
COVER_SAFE_MARGIN = 0.125  # keep cover text/art this far inside the trim line
MIN_DPI = 300

# Page thickness in inches per page, by paper/ink type.
PAPER_THICKNESS = {
    "white": 0.002252,  # black ink, white paper
    "cream": 0.0025,  # black ink, cream paper
    "standard-color": 0.002252,
    "premium-color": 0.002347,
}

# Common KDP paperback trim sizes (width, height) in inches.
TRIM_SIZES = {
    "5x8": (5.0, 8.0),
    "5.06x7.81": (5.06, 7.81),
    "5.25x8": (5.25, 8.0),
    "5.5x8.5": (5.5, 8.5),
    "6x9": (6.0, 9.0),
    "6.14x9.21": (6.14, 9.21),
    "6.69x9.61": (6.69, 9.61),
    "7x10": (7.0, 10.0),
    "7.44x9.69": (7.44, 9.69),
    "7.5x9.25": (7.5, 9.25),
    "8x10": (8.0, 10.0),
    "8.25x6": (8.25, 6.0),
    "8.25x8.25": (8.25, 8.25),
    "8.5x8.5": (8.5, 8.5),
    "8.5x11": (8.5, 11.0),
    "8.27x11.69": (8.27, 11.69),
}

# Inside (gutter) margin by page count: (max_pages, gutter_inches).
GUTTER_BY_PAGES = [(150, 0.375), (300, 0.5), (500, 0.625), (700, 0.75), (828, 0.875)]
OUTSIDE_MARGIN_NO_BLEED = 0.25
OUTSIDE_MARGIN_BLEED = 0.375

# Metadata limits.
TITLE_SUBTITLE_MAX = 200
DESCRIPTION_MAX = 4000
KEYWORD_SLOTS = 7
KEYWORD_MAX_CHARS = 50
MAX_CATEGORIES = 3
DESCRIPTION_ALLOWED_TAGS = {"b", "i", "u", "em", "strong", "br", "p", "h4", "h5", "h6", "ul", "ol", "li"}

# Royalty rules.
EBOOK_70_MIN, EBOOK_70_MAX = 2.99, 9.99  # USD list price range eligible for 70%
EBOOK_DELIVERY_PER_MB = 0.15  # USD, deducted under the 70% plan (Amazon.com)
PAPERBACK_ROYALTY = 0.60  # of list price, Amazon marketplaces
PAPERBACK_EXPANDED_ROYALTY = 0.40  # expanded distribution

# US black-ink paperback printing cost: (fixed, per_page) by page band and trim class.
# Verify against the KDP calculator; pass --print-cost to override.
PRINT_COST = {
    "regular": [(108, 2.30, 0.0), (828, 1.00, 0.012)],
    "large": [(108, 2.84, 0.0), (828, 1.00, 0.017)],
}


def trim(name):
    if name not in TRIM_SIZES:
        raise SystemExit(f"Unknown trim '{name}'. Options: {', '.join(TRIM_SIZES)}")
    return TRIM_SIZES[name]


def check_page_count(pages):
    if not MIN_PAGES <= pages <= MAX_PAGES:
        raise SystemExit(f"Page count {pages} is outside KDP's {MIN_PAGES}-{MAX_PAGES} range.")


def gutter_margin(pages):
    for max_pages, gutter in GUTTER_BY_PAGES:
        if pages <= max_pages:
            return gutter
    raise SystemExit(f"Page count {pages} exceeds KDP's {MAX_PAGES}-page maximum.")


def spine_width(pages, paper):
    if paper not in PAPER_THICKNESS:
        raise SystemExit(f"Unknown paper '{paper}'. Options: {', '.join(PAPER_THICKNESS)}")
    return pages * PAPER_THICKNESS[paper]


def is_large_trim(width, height):
    return width > 6.12 or height > 9.0


def print_cost(pages, width, height):
    bands = PRINT_COST["large" if is_large_trim(width, height) else "regular"]
    for max_pages, fixed, per_page in bands:
        if pages <= max_pages:
            return fixed + per_page * pages
    raise SystemExit(f"Page count {pages} exceeds KDP's {MAX_PAGES}-page maximum.")
