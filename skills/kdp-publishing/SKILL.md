---
name: kdp-publishing
description: Prepare books for Amazon KDP (Kindle Direct Publishing). Use when the user wants to format a manuscript into a print-ready paperback interior PDF or Kindle EPUB, calculate full-wrap cover or spine dimensions, make a cover template, generate low-content books (journals, notebooks, planners, gratitude logs), check titles/descriptions/keywords/categories against KDP rules, estimate royalties or pick prices, or analyze KDP royalty and KENP reports. Triggers include KDP, Kindle Direct Publishing, self-publishing on Amazon, paperback interior, trim size, spine width, bleed, KENP, Kindle Unlimited page reads, book keywords.
license: Apache-2.0
---

# KDP Publishing

KDP has no public API. Nothing here uploads to KDP or logs into the dashboard, and
you must not automate the KDP website (it risks the user's account). These tools
produce files and checks. The user does the upload at kdp.amazon.com.

All scripts live in `scripts/`, print JSON, and read shared limits from
`scripts/kdp_specs.py`. Run them from the `scripts/` directory.
Dependencies: `pip install reportlab openpyxl python-docx ebooklib`.

## Workflow for a new book

1. **Metadata.** Copy `templates/book.json`, fill it in, run
   `python check_metadata.py book.json`. Fix every error. Treat warnings as advice.
2. **Paperback interior.**
   `python format_interior.py manuscript.docx --title "..." --author "..." --trim 6x9 -o interior.pdf`
   The output reports the final page count.
3. **Cover.** Use that page count:
   `python cover_calc.py --trim 6x9 --pages <N> --paper cream --template cover_template.pdf`
   The cover artwork must be one PDF at the full-wrap size, 300 DPI, with fonts embedded.
   Front-cover art can come from an image-generation tool. Keep text inside the red safe area.
4. **eBook.** `python make_epub.py manuscript.docx --title "..." --author "..." --cover front.jpg -o book.epub`
   (front cover 1600x2560 px). Tell the user to preview it in Kindle Previewer.
5. **Pricing.** `python royalty_calc.py --ebook 4.99 --paperback 14.99 --pages <N> --trim 6x9`
6. Give the user an upload checklist (below).

## Manuscript conventions

- `.docx`: Heading 1 = chapter, other headings = subheads, bold and italic are kept.
- `.md`: `# Chapter`, `## Subhead`, `***` scene break, `**bold**`, `*italic*`.
- `.txt`: a short paragraph starting with "Chapter" starts a chapter.

The interior formatter embeds a serif TTF (Liberation Serif, DejaVu Serif or Times New Roman,
whichever is found). Pass `--font-dir` for a custom family. Chapters open on right-hand
pages. The gutter is re-computed from the final page count.
Use `--bleed` only when images run to the page edge.

## Low-content books

`python low_content.py --style planner --pages 120 --trim 6x9 --title "Daily Planner" -o planner.pdf`
Styles: lined, dot, grid, blank, planner, gratitude. Low-content books can't use an ISBN
to claim content. Warn the user that KDP limits their reach, and that near-duplicate
low-content books get rejected.

## Word search books (fully automated)

1. Write a spec JSON: title, subtitle, author, seed, and 50-60 themed puzzles
   of 12-15 words each (at most 15 letters after spaces are removed). No word
   may sit inside another word in the same puzzle (ANGLE/TRIANGLE); the builder
   rejects those.
2. `python word_search_book.py book.json -o interior.pdf`: large-print 8.5x11
   interior with how-to page, one puzzle per page, answer keys, series page.
   Every grid is verified: each word appears exactly once, and filler letters
   never spell a blocked word.
3. `python puzzle_cover.py book.json --pages <N> -o cover.pdf`: full-wrap
   cover drawn in code (patterns: quilt, yarn, honeycomb, halloween, christmas), with a sample puzzle
   on the back and the barcode area kept clear. Add a `cover` block to the
   spec; see the script docstring.
4. Marketing pins: `python pin_images.py book.json --puzzles 1 13 48 -o pins/`
   makes 1000x1500 Pinterest images showing the exact puzzles printed in the book.
5. Metadata: subtitle must match the cover text. Run `check_metadata.py`.
   Puzzle books are not "low-content" on KDP (they have content), so they
   get a free KDP ISBN.
6. AI disclosure: word lists and descriptions written by Claude are
   AI-generated text. Code-drawn covers are not AI-generated images.

## Reports

Have the user download reports from KDP (Reports > Prior Month Royalties, or the
Dashboard download), then run
`python royalty_report.py report.xlsx --xlsx summary.xlsx`.
Currencies are kept separate on purpose. The KENP payout rate changes monthly, so
the report gives pages read, not dollars.

## KDP rules to enforce

- Title and subtitle must match the cover. No "free", "bestseller", "Kindle",
  "Amazon" or similar promotional terms.
- Keywords: 7 slots, up to 50 characters each. No other authors' names, book titles,
  or trademarks. Don't repeat title words.
- Up to 3 categories.
- eBook 70% royalty needs a list price of $2.99-$9.99 (US). The delivery fee is
  deducted per MB.
- Paperback royalty is 60% of list price minus printing cost (40% for expanded
  distribution). Printing costs in `kdp_specs.py` can change, so confirm them in KDP's
  pricing calculator or pass `--print-cost`.
- Paperbacks need 24-828 pages. Spine text is allowed only above 79 pages.
- **AI-generated content:** KDP requires publishers to disclose AI-generated text,
  images or translations when they publish. Remind the user whenever you generated
  any of the book's content or cover art.
- KDP caps how many new titles an account can create per day. Don't plan mass uploads.

## Upload checklist for the user

1. KDP Bookshelf > Create > Paperback (or Kindle eBook).
2. Details: paste the checked metadata, pick categories, and answer the AI-content question.
3. Content: pick trim/paper/bleed to match the files. Upload `interior.pdf` and the cover PDF.
   Run the Previewer and fix any flags.
4. Pricing: enter the prices you checked with `royalty_calc.py`.
5. Order a proof copy before publishing the paperback.
