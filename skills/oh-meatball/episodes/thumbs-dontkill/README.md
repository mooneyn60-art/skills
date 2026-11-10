# "Don't Kill It" thumbnails (white-background recipe)

This is the look that small channels in our niche are breaking out with (research/70-niche-outliers-1110.md section 4):
- one huge illustrated creature on plain white, with a soft shadow on the floor
- a sneaker sole coming in from a top corner, about to squish it
- 2 to 4 hand-lettered words in black, one in red or blue
- a hand-drawn arrow at the creature
- nothing else

These are made for YouTube "Test & compare" against the current dark Anton thumbnails.

## Run

    # all 7 deliverables + contact sheets (about 10 s on one core)
    python3 tools/thumb_dontkill.py --json episodes/thumbs-dontkill/specs.json \
        --contact episodes/thumbs-dontkill \
        --compare episodes/longform-kill-or-keep-2/thumb_a.jpg episodes/longform-kill-or-keep-2/thumb_b.jpg \
                  episodes/longform-kill-or-keep-2/thumb_c.jpg

    # one spec
    python3 tools/thumb_dontkill.py --json episodes/thumbs-dontkill/specs.json --only kk2_b

    # quick one-off without JSON
    python3 tools/thumb_dontkill.py --creature house_centipede --headline "NEVER|*STEP* ON IT" --accent blue \
        --shoe tl --meatball -o /tmp/x.jpg

How to write a headline: use `|` to split lines and `*stars*` around the accent word, for example `"DON'T|*KILL*|IT!"`.

Creatures: `wolf_spider`, `cellar_spider` and `house_centipede`. Each is drawn top-down with the real body plan:
- spiders: 8 legs, carapace and abdomen
- centipede: 15 leg pairs, long antennae and trailing last legs

Other spec keys (shoe corner/size/rot, arrow from/to/bend, `meatball`, `web`, `line_scale`, `look`, `zoom`) are listed in the tool's docstring.

Every output writes `NAME_168.jpg` next to it. Look at that file before you ship. `contact_168.jpg` shows all 7 at 168x94 (1:1 pixels) on mid-grey, next to the three current Kill-or-Keep-2 thumbs.

The lettering font is Permanent Marker (Apache 2.0), in brand/fonts/ (see LICENSES.txt).

## Ranking (best first), with what is weak

1. **kk2_a** (wolf spider + shoe + "DON'T KILL IT!"): the purest copy of the proven recipe. It has the biggest words at 168 px and the spider reads instantly. Weak: the apostrophe in DON'T almost merges ("DONT"), and the shoe is a corner crop that reads as "blue sneaker sole" only at 320 px and up.
2. **centipede_a** ("DON'T SQUISH IT!"): the centipede is unmistakable, even at 168. Weak: SQUISH is long, so the words are smaller than in kk2_a, and the 30 legs make a busy texture next to the text.
3. **cellarspider_a** ("DON'T KILL IT!"): the long legs span the frame and the pale body sits right under the shoe. Weak: the body and legs are pale on white, so it has the least contrast of the set. The body is drawn about 2x real proportion so that it reads at all.
4. **kk2_c** ("NOT THIS ONE!", mirrored layout): the best curiosity angle for a "kill 5 / keep 3" title. Weak: "THIS ONE!" is small at 168 px, so only "NOT" carries the line.
5. **centipede_b** ("IT EATS ROACHES"): gives the "(Here's Why)" payoff and pairs well with the title. Weak: two long lines of text, so the words are smaller than in centipede_a.
6. **cellarspider_b** ("IT EATS SPIDERS", web corner, no shoe): the strongest surprise hook ("a spider that eats spiders?"). Weak: there is no shoe, which drops the threat element. The web is faint at 168 and the arrow crosses legs.
7. **kk2_b** (kk2_a plus Meatball, arms out): this is the brand twist. Weak: Meatball is only 320 px tall, with a brown head next to a brown spider, so at 168 he is a small brown dot on a stick. He also shrinks the spider and the words, which hurts the two things that drive the click.

Ship first: kk2_a for Kill-or-Keep 2, centipede_a for the centipede episode, and cellarspider_a for the cellar spider episode. Use the B/C variants as the "Test & compare" challengers.
