"""Check a book's KDP metadata (JSON) against KDP limits and common rejection reasons.

See templates/book.json for the expected fields.

Usage:
  python check_metadata.py book.json
Exit code 1 when any error is found; warnings do not fail.
"""

import argparse
import json
import re
import sys

import kdp_specs as kdp

BANNED_TERMS = ["free", "bestseller", "best seller", "best-selling", "bestselling", "#1", "kindle unlimited",
                "on sale", "new release", "kdp", "amazon", "kindle"]


def contains_term(text, term):
    return re.search(rf"(?<!\w){re.escape(term)}(?!\w)", text.lower()) is not None


def check(meta):
    errors, warnings = [], []
    title, subtitle = meta.get("title", "").strip(), meta.get("subtitle", "").strip()
    if not title:
        errors.append("title is required")
    if len(title) + len(subtitle) > kdp.TITLE_SUBTITLE_MAX:
        errors.append(f"title + subtitle is {len(title) + len(subtitle)} chars; max {kdp.TITLE_SUBTITLE_MAX}")
    for term in BANNED_TERMS:
        if contains_term(f"{title} {subtitle}", term):
            errors.append(f"title/subtitle contains '{term}', which KDP treats as misleading metadata")

    desc = meta.get("description", "")
    if not desc.strip():
        errors.append("description is required")
    if len(desc) > kdp.DESCRIPTION_MAX:
        errors.append(f"description is {len(desc)} chars; max {kdp.DESCRIPTION_MAX}")
    bad_tags = sorted({t.lower() for t in re.findall(r"</?\s*([a-zA-Z0-9]+)", desc)} - kdp.DESCRIPTION_ALLOWED_TAGS)
    if bad_tags:
        errors.append(f"description uses unsupported HTML tags: {', '.join(bad_tags)}")
    if re.search(r"https?://|www\.", desc):
        warnings.append("description contains a URL; KDP may reject links in descriptions")

    keywords = meta.get("keywords", [])
    if len(keywords) > kdp.KEYWORD_SLOTS:
        errors.append(f"{len(keywords)} keywords; KDP has {kdp.KEYWORD_SLOTS} slots")
    if len(keywords) < kdp.KEYWORD_SLOTS:
        warnings.append(f"only {len(keywords)} of {kdp.KEYWORD_SLOTS} keyword slots used")
    title_words = set(re.findall(r"\w+", f"{title} {subtitle}".lower()))
    seen = set()
    for kw in keywords:
        if len(kw) > kdp.KEYWORD_MAX_CHARS:
            errors.append(f"keyword '{kw}' is {len(kw)} chars; max {kdp.KEYWORD_MAX_CHARS}")
        if '"' in kw or "," in kw:
            warnings.append(f"keyword '{kw}': quotes and commas add nothing; use plain phrases")
        for term in BANNED_TERMS:
            if contains_term(kw, term):
                errors.append(f"keyword '{kw}' contains restricted term '{term}'")
        words = set(re.findall(r"\w+", kw.lower()))
        if words and words <= title_words:
            warnings.append(f"keyword '{kw}' only repeats title words; the title is already indexed")
        if words & seen - {"a", "the", "for", "and", "of", "to", "in"}:
            warnings.append(f"keyword '{kw}' repeats words used in another keyword; each slot should add new terms")
        seen |= words

    if any(re.search(r"\b(fans of|readers of|books like|similar to|in the style of)\b", kw.lower()) for kw in keywords):
        warnings.append("a keyword looks like it names another author or book; KDP prohibits that")

    categories = meta.get("categories", [])
    if not categories:
        warnings.append("no categories chosen")
    if len(categories) > kdp.MAX_CATEGORIES:
        errors.append(f"{len(categories)} categories; KDP allows {kdp.MAX_CATEGORIES}")

    ebook_price = meta.get("ebook_price")
    if ebook_price is not None and not kdp.EBOOK_70_MIN <= ebook_price <= kdp.EBOOK_70_MAX:
        warnings.append(f"eBook price ${ebook_price} is outside ${kdp.EBOOK_70_MIN}-${kdp.EBOOK_70_MAX}; only the 35% royalty applies")

    pb = meta.get("paperback")
    if pb:
        width, height = kdp.trim(pb["trim"])
        cost = kdp.print_cost(pb["pages"], width, height)
        min_price = cost / kdp.PAPERBACK_ROYALTY
        if pb.get("price") is not None and pb["price"] < min_price:
            errors.append(f"paperback price ${pb['price']} is below the ${min_price:.2f} minimum (printing ${cost:.2f})")
    return errors, warnings


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("metadata")
    a = p.parse_args()
    with open(a.metadata, encoding="utf-8") as f:
        errors, warnings = check(json.load(f))
    print(json.dumps({"ok": not errors, "errors": errors, "warnings": warnings}, indent=2))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
