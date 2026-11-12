---
name: make-short
description: Make, check and schedule a Meatball Myths YouTube Short and its TikTok cut, from topic to a logged post. Use this whenever a new Short or TikTok is to be written, rewritten, made funnier, re-rendered, swapped into a scheduled post or moved, even if Nolan only says "make one about X", "fix that one" or "try these today". It holds the order of the steps and the commands that replace hand work, so nothing is scheduled unchecked.
---

# Make a Short (and its TikTok cut)

Rules live in `skills/channel-brain/MASTER_ORDERS.md` and Nolan's words there win over this page. This page is the order of work and the commands. Run commands from `skills/oh-meatball`. If `python3 tools/postkit.py --help` fails on a fresh machine, run `bash tools/setup_env.sh` first.

Why the order matters: every step below exists because skipping it once put a wrong or stale video in the queue (a render that silently kept the old file, a title that claimed more than the study, a caption that lost a safety condition).

## 1. Research before anything is built
Nolan's standing order is research first, every time. For a new topic that means numbers, not a guess:
- What people type: `python3 tools/postkit.py kw "seed phrase" "another seed" --search "main query" --out research/data/NN-kw.csv`. Take the strongest suggestion as the search phrase.
- What TikTok itself calls it: find three to five public TikToks on the topic (web search limited to tiktok.com), then `python3 tools/postkit.py ttpage URL ...` and read "TikTok suggests". It is often not the question you assumed ("guilty dogs", not "why does my dog look guilty").
- Facts: a fact pack with a source for every number (pattern: `research/84-pets-and-survive-factpack.md`, with a do-not-say list). A different model checks the pack against the live sources.
- A new direction or format (not just a new topic) goes to Nolan as options with the evidence before anything is built.

## 2. Write the spec
One JSON file per cut in `scripts/drawn-house/`: `<slug>-v6-yt.json` for YouTube and `tts-<slug>.json` for the TikTok cut. Copy the newest pair as a template and read `references/spec.md` for the keys.
The script rules that hold today (check MASTER_ORDERS "Make them funnier" and "The v6 template" for changes):
- Funny first. Line 1 is the fact, with the searched phrase in the first spoken sentence. Line 2 is a Meatball gag that is drawn, not only said (a prop, a card, him acting it out). After that every fact line is the joke or is followed by one; a line that is only a study detail is cut. Keep at least two sourced facts.
- Jokes are on Meatball. A joke never adds a number, a danger or health claim, an animal's feeling or motive, or a safety instruction. Hedges stay ("probably", "may", "in one small study"). Attributions and safety instructions are said clean, with the reaction after.
- YouTube: 15 to 20 s, one or two mild words, statement title. TikTok: about one swear a line, `cap_swap` softens every spelling used, `search_top` shows the search phrase for the first 2 to 2.5 s, 20 to 26 s for a short cut or 61 s and more for a Rewards cut.
- Write "his cat" and "his dog" in full and "let out a meow", not "meowed": the voice swallows the short forms.

## 3. A different model checks the script
Before any render that will be scheduled, a reviewer on another model reads every changed line against the fact pack, the do-not-say list and the rules above (pattern: `research/92-factcheck-funnier-cuts.md`). Apply its fixes. Unchanged, already-cleared lines need no second look.

## 4. Render and listen
`python3 tools/postkit.py render scripts/drawn-house/<spec>.json episodes/drawn-house/<out>.mp4 --work /dev/shm/<slug>`
This runs `drawn.py`, fails loudly if the renderer exited with an error or left the old file in place, then transcribes the result and compares it with the script line by line. Do not schedule on anything but a pass. `postkit.py voicecheck SPEC MP4` re-checks an existing file.

## 5. Look
`python3 tools/postkit.py sheet episodes/drawn-house/<out>.mp4 /tmp/<slug>.jpg` and read the image. Check: frame 0 is the animal already moving; the gag in line 2 is visible; cards are readable and not under the TikTok search phrase; captions show softened spellings on TikTok; the last line returns to the first room for the loop.

## 6. Titles, tags and captions
Follow the `post-metadata` skill, then gate it:
`python3 tools/postkit.py lint scripts/drawn-house/<spec>.json --mp4 episodes/drawn-house/<out>.mp4`
A FAIL blocks scheduling. A WARN is a deviation from the standard that needs a reason.

## 7. Commit, push, link
Add paths with `git add --sparse <paths>` (never `git add -A`), commit, push, then:
`python3 tools/postkit.py rawurl episodes/drawn-house/<out>.mp4`
It prints the raw link at the pushed commit and refuses if the file on disk is not the one in that commit.

## 8. Schedule
- Build the exact post body: `python3 tools/postkit.py payload SPEC --net youtube|tiktok --when 2026-11-13T16:00:00 --media <raw link or existing static.metricool.com link>`.
- Load the Metricool tools with ToolSearch (`select:mcp__Metricool_Social_Media_Management__createScheduledPost,...updateScheduledPost,...getScheduledPosts`), brand `7521392`, timezone `America/New_York`. An update needs the whole body again; the post's id changes on every update and its uuid stays. Read the schedule one or two days per call.
- Slots and limits are in MASTER_ORDERS ("Posting", "Views are stuck on both platforms"): three Shorts a day at least three hours apart, never in the long-form's slot; the AI label stays on.
- After the call: `python3 tools/postkit.py rehost <static.metricool.com link from the response> <local file>` proves Metricool holds the same file.

## 9. Log and tell
- `data/posted.csv`: one row per post (`date,network,episode,file,title`), changed with every scheduling change.
- If Nolan's words caused the work, they go into MASTER_ORDERS the same day with your reading of them; a finding goes into `skills/channel-brain/KNOWLEDGE.md` with its source.
- Commit and push. Then tell Nolan in one or two short lines: what changed, and the one thing he must do if there is one.
