---
name: post-metadata
description: Write or fix the TEXT around a Meatball Myths video (YouTube title, description, tags, hashtags, first comment; TikTok caption) so it matches what people search and stays true to the checked facts. Use for "fix the tags", "update titles", "tags and everything", "hashtags", "captions", "better title", "change the caption", "SEO", "what do people search", and before any post is scheduled or any text changes, even one word. Not for the video itself (make-short).
---

# Titles, tags and captions

The evidence is in `skills/oh-meatball/research/93-metadata-all-angles.md`; the standing rule is in `skills/channel-brain/MASTER_ORDERS.md` under "Tags and everything, from every angle" (that page wins if it differs from this one). Run commands from `skills/oh-meatball`.

What the evidence says, in one breath: on YouTube the title and the first sentence of the description carry search, tags "play a minimal role" (YouTube's own words), and nothing official says the category or #shorts changes ranking. On TikTok a video has one text field, the caption; the "title" Metricool asks for is published nowhere. Metadata does not rescue a video viewers swipe away, so spend minutes here, not hours.

## 1. Find the words
`python3 tools/postkit.py kw "seed" "seed" --search "main query" --out research/data/NN-kw.csv`
Use suggestions that extend your seed (a seed that only echoes itself shows nothing). If no suggestion extends it, try two other seeds; if still none, build the title from the words of the top results and say "search volume not measurable" in the report. For TikTok, read TikTok's own suggested searches on a few top videos: `python3 tools/postkit.py ttpage URL ...`.

**Searched words** = the top YouTube or Google suggestion for the topic from `postkit.py kw`, word for word: the seed question itself when it is rank 1 in both the YouTube and the web list, otherwise the shortest suggestion that extends it. The first spoken sentence, the description's first sentence and the TikTok on-screen phrase use these words.

## 2. Write to the standard
YouTube Short:
- Title: the searched words in the first 40 characters, the hedge kept, one specific odd fact, one emoji, the series tag last, 100 units at most, a statement. A statement title drops the question words: "why do cats knead" becomes "Why Cats Knead ..." (no "do", no "?"). Question titles did worse here and quiz words are banned.
- Description: first sentence is the question people type; then the checked facts unchanged; then four hashtags (two topic, `#meatballmyths`, `#shorts` last); then the Sources line. Big-animal safety videos keep "General information, not safety training."
- Tags: 8 to 12 phrases in total, the series tag and "Meatball Myths" included. Take the rest from the YouTube suggestions, then the web ones, longest first. Each is 30 characters or fewer (skip a longer suggestion) and answered by the video (skip "dough", "asmr" and the like). No tag that promises advice the video does not give. Write the tags after the script exists.
- First comment: an open question that pulls a story.
TikTok:
- Caption: the search phrase that is on screen, the checked fact with its condition, the Meatball gag in the video's own words without the swearing, a question, five topic hashtags. No #fyp, no #learnontiktok, no brand tag. Safety videos keep "General info, not safety training."
Put the text in the spec (`title`, `description`, `tags`, `pinned_comment`, `tiktok_caption`).

## 3. A different model checks the wording
Metadata is public text about facts, so it goes through the same check as a script. Give the reviewer the cleared text, the new text, the spoken lines, the fact pack with its do-not-say list, and ask for three things: does any new wording claim more than its source; does every limit and house rule hold; is a stronger searched phrase missing. Slips this caught on 11/12: "knows its name" (the study shows cats tell their name from other words), "lean right" without saying it is the dog's right, a "how many attacks" question answered with only the unprovoked count, a caption that dropped the condition from a safety line.
The safest edits reuse cleared sentences word for word. Shortening a sentence is where conditions get lost.

## 4. Gate it
Lint the YouTube spec and the `tts-` spec separately; each checks only its own network's fields: `python3 tools/postkit.py lint scripts/drawn-house/<spec>.json`. It checks lengths, banned title words, swear stems in text fields, tag limits, hashtags, placeholder text (UNCHECKED, TODO and so on), the safety line and that the TikTok caption opens with the on-screen phrase. Fix every FAIL. A WARN needs its reason in the spec's `_note`. Lint does not check facts, whether the tags fit the video, or that the searched words sit in the first 40 characters of the title: read those yourself.

## 5. Apply and log
`python3 tools/postkit.py payload SPEC --net youtube|tiktok --when YYYY-MM-DDTHH:MM:SS --media <the post's current https media link> --update ID UUID` prints the four arguments of Metricool `updateScheduledPost` (an update replaces everything, so the first comment and the media link must be the current ones). Take ID and UUID from `getScheduledPosts`, one day per call. Update `data/posted.csv` when a title changes. Changing the text of a video that is already live is a different thing: YouTube advises not to change what is working.

## What cannot be measured from here
Search volumes (suggestions give rank only), TikTok hashtag sizes, and whether tags or hashtags ever changed our views. Say so when reporting.
