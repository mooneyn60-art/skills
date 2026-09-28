"""Estimate KDP royalties per sale for eBook and paperback at one or more prices.

Usage:
  python royalty_calc.py --ebook 4.99 --file-mb 1.2
  python royalty_calc.py --paperback 12.99 14.99 --trim 6x9 --pages 240
  python royalty_calc.py --paperback 12.99 --trim 6x9 --pages 240 --print-cost 3.88
"""

import argparse
import json

import kdp_specs as kdp


def ebook_royalty(price, file_mb):
    delivery = round(kdp.EBOOK_DELIVERY_PER_MB * file_mb, 2)
    options = {"35%": round(price * 0.35, 2)}
    if kdp.EBOOK_70_MIN <= price <= kdp.EBOOK_70_MAX:
        options["70%"] = round((price - delivery) * 0.70, 2)
    best = max(options, key=options.get)
    return {"price": price, "delivery_cost": delivery, "royalty_options": options, "best_plan": best}


def paperback_royalty(price, pages, trim_name, print_cost=None):
    kdp.check_page_count(pages)
    width, height = kdp.trim(trim_name)
    cost = print_cost if print_cost is not None else round(kdp.print_cost(pages, width, height), 2)
    return {
        "price": price,
        "printing_cost": cost,
        "royalty_amazon": round(price * kdp.PAPERBACK_ROYALTY - cost, 2),
        "royalty_expanded_distribution": round(price * kdp.PAPERBACK_EXPANDED_ROYALTY - cost, 2),
        "minimum_list_price": round(cost / kdp.PAPERBACK_ROYALTY, 2),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ebook", type=float, nargs="*", default=[])
    p.add_argument("--file-mb", type=float, default=1.0, help="eBook file size in MB (delivery cost)")
    p.add_argument("--paperback", type=float, nargs="*", default=[])
    p.add_argument("--pages", type=int)
    p.add_argument("--trim", default="6x9")
    p.add_argument("--print-cost", type=float, help="override printing cost from the KDP calculator")
    a = p.parse_args()
    if a.paperback and not a.pages:
        p.error("--paperback needs --pages")

    result = {
        "ebook": [ebook_royalty(x, a.file_mb) for x in a.ebook],
        "paperback": [paperback_royalty(x, a.pages, a.trim, a.print_cost) for x in a.paperback],
        "note": "US marketplace estimates. Confirm printing cost in KDP's pricing calculator.",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
