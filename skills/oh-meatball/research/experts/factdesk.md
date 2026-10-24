# The Fact & Photo Desk playbook

Desk id: `factdesk`. Absorbs: Fact-Checker, Photo Editor. Read this before every run and append lessons after.

## Read first
- research/30 red team (licensing)
- tools/cands.py, cands_any.py
- research/38 (picture must match line)

## Rules (proven)
- Verify every claim with two independent sources; label what is contested. Wrong quiz answers draw angry 241-like comments.
- Photos: live, unharmed, right species; CC0 or CC BY only for new picks (no CC BY-NC); credit every photo.
- The picture must show what the line says (a "cats falling" line shows a cat falling, not sitting).
- No photographer watermarks in frame; reject soft or blurry crops for full-bleed shots.
- Look at every candidate photo before using it; iNat taxon searches mix species (brown vs polar bears, Alpheus returning butterflies).

## KPIs this desk owns
- Fact errors caught
- Photo-line match rate
- Watermark/blur rejects

## Lessons log (newest last; date, what happened, what we learned, the number)
- 2026-10-24: desk created by merging the roles above.
- 2026-10-24 (series + Halloween + history-02):
  - iNaturalist has no CC0/CC BY photo of Chironex fleckeri, and every wild research-grade CC piranha photo shows a caught or dead fish. Fixes: box jelly photos are other box jellies (Carybdea, Alatina, Copula), with the Chironex line on a text card; piranha photos are live aquarium fish (`quality_grade=casual`, captive).
  - The renderer pins `photos[0]` of an observation. A good second photo (e.g. a howling wolf) can't be used, so check what photos[0] is before pinning. The wolf-howling myth was dropped for this reason (0 usable photos out of ~450).
  - Watermarks can hide in corners. Both 960 px swimming-moose photos (92166840, 102548882) carry "© Coral Ridge Studio" at the bottom left, so crops stop at y=0.9. The vampire bat 248835378 has a gloved hand at the left edge, so crops start right of it.
  - Numbers drift between sources. Cassowary claw: 10 vs 12-13 cm, so the script uses the conservative "up to four inches". Croc bite: Nat Geo says "3,700 psi", but it's 3,700 lb of *force* (16,414 N). Komodo venom's role in kills is contested, so the script says so on air. Moose dive depth (18-20 ft) traces to one anecdote, so it was dropped. Smith 2016 (horses, left-eye) was challenged, while the heart-rate result stands.
  - A crop contact sheet (every shot's crop at 144x256) catches bad framing that full-photo review misses: 4 of 110 crops cut off the animal's head and were re-centred.
