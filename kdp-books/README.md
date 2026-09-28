# Hollow Pine Puzzles — book sources

Each folder holds the source for one KDP paperback: `words.txt` (puzzle lists),
`book.json` (build spec + cover copy) and `metadata.json` (KDP listing).

Rebuild a book from its folder:

    python ../../skills/kdp-publishing/scripts/word_search_book.py book.json -o interior.pdf
    python ../../skills/kdp-publishing/scripts/puzzle_cover.py book.json --pages 82 -o cover.pdf
    python ../../skills/kdp-publishing/scripts/check_metadata.py metadata.json
