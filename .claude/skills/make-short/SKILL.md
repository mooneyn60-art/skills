---
name: make-short
description: Make, rewrite, re-render, reschedule or move a Meatball Myths YouTube Short or TikTok cut, from topic to a logged post. Use for "make one about X", "new short", "do a TikTok on X", "try these today", "post this today", "make them funnier", "make it funnier", "too short", "redo it", "swap it in", "move it to 4pm". It holds the order of the steps and the commands, so nothing is scheduled unchecked.
---

# Make a Short (and its TikTok cut)

Rules live in `skills/channel-brain/MASTER_ORDERS.md`; Nolan's words there win over this page. This page is the order of work and the commands. Run commands from `skills/oh-meatball`. If `python3 tools/postkit.py --help` fails on a fresh machine, run `bash tools/setup_env.sh` first.

Why the order matters: every step exists because skipping it once put a wrong or stale video in the queue (a render that silently kept the old file, a title that claimed more than the study, a caption that lost a safety condition).

## 1. Research before anything is built
Nolan's standing order: research first, every time. For a new topic that means numbers, not a guess:
- What people type: `python3 tools/postkit.py kw "seed phrase" "another seed" --search "main query" --out research/data/NN-kw.csv`. The searched words are defined in the `post-metadata` skill.
- What TikTok calls it: find three to five public TikToks on the topic (web search limited to tiktok.com), then `python3 tools/postkit.py ttpage URL ...` and read "TikTok suggests".
- Facts: a fact pack with a source for every number (pattern: `research/84-pets-and-survive-factpack.md`, with a do-not-say list). A different model checks the pack against the live sources.
- A new direction or format (not just a new topic) goes to Nolan as options with the evidence first.
- New videos are pets or Would Meatball Survive. No new bug episodes, no case files.

## 2. Write the spec
One JSON file per cut in `scripts/drawn-house/`: `<slug>-v6-yt.json` for YouTube and `tts-<slug>.json` for the TikTok cut. Copy the newest pair (`cat-sugar-v6-yt.json` and `tts-cat-sugar.json`). If a spec or mp4 named here is not on disk, the checkout is sparse: `git sparse-checkout add /skills/oh-meatball/scripts/drawn-house/`, or for one old file `git show HEAD:skills/oh-meatball/<path> > /dev/shm/<name>`. Write new files at their normal paths; `git add --sparse` adds them. The renderer's docstring (`tools/drawn.py`) is the source of truth for the keys; `references/spec.md` is a short guide.
The script rules are in MASTER_ORDERS, "Make them funnier", rules 1-5. Read them there; do not copy them here. Two things this page adds: write "his cat" and "his dog" in full and "let out a meow", not "meowed" (the voice swallows the short forms); the searched words go in the first spoken sentence.
Voice is fixed: edge-tts `en-US-AndrewMultilingualNeural`, +10%, +3Hz. Fully drawn, no real photos or footage.

## 3. A different model checks the script
Before any render that will be scheduled, a reviewer on another model reads every changed line against the fact pack, the do-not-say list and the rules (pattern: `research/92-factcheck-funnier-cuts.md`). Apply its fixes. Lines already cleared and unchanged need no second look.

## 4. Render and listen
`python3 tools/postkit.py render scripts/drawn-house/<spec>.json episodes/drawn-house/<out>.mp4 --work /dev/shm/<slug>`
It runs `drawn.py`, fails if the renderer errored or left the old file in place, then transcribes the result and compares it with the script line by line.
- **Pass** = exit 0 and the line `ok every line heard to its end`. Schedule on nothing else.
- **FAIL**: render once more (the voice service drops words at random). If the same line fails again, reword the line the check names, then send the new wording through the second-model check (step 3) before rendering again.
- `postkit.py voicecheck SPEC MP4` re-checks an existing file.

## 5. Look
`render` already wrote `<work>/sheet.jpg` (the path is printed). Open that one. `postkit.py sheet MP4 OUT.jpg` is only for an mp4 that already exists. A still cannot show motion: compare frame 0 and frame 1 for "the animal is already moving". Check: the gag in line 2 is visible; cards are readable and not under the TikTok search phrase; TikTok captions show the softened spellings; the last frame is back in the first room (the loop).

## 6. Titles, tags and captions
Follow the `post-metadata` skill, then gate it. Lint each network's spec on its own (a YouTube spec checks the YouTube fields, a `tts-` spec checks the TikTok fields):
`python3 tools/postkit.py lint scripts/drawn-house/<spec>.json --mp4 episodes/drawn-house/<out>.mp4`
- **FAIL** blocks scheduling. Fix it and lint again.
- **WARN** needs a reason. Write the reason in the spec's `_note`; lint reads exit codes only, so the note is for the next reader.
- Lint does not check facts, whether the tags fit the video, or whether the searched words sit in the first 40 characters of the title. Read those yourself.
- `python3 tools/postkit.py selftest` runs lint on built-in good and bad specs. Run it after any change to postkit.

## 7. Commit, push, link
Add paths with `git add --sparse <paths>` (never `git add -A`), commit, push, then:
`python3 tools/postkit.py rawurl episodes/drawn-house/<out>.mp4`
It fails unless the file on disk is the file in the pushed commit, resolves the commit to a full sha, and checks the raw link answers HTTP 200 before it prints it.

## 8. Schedule
- `python3 tools/postkit.py payload SPEC --net youtube|tiktok --when 2026-11-13T16:00:00 --media <raw link or existing static.metricool.com link>` prints the `info` object. It exits non-zero and prints nothing if the spec does not match `--net`, `--when` is not `YYYY-MM-DDTHH:MM:SS`, or `--media` is not an https link.
- New post: add `--call`. It prints the three arguments of Metricool `createScheduledPost`: `blogId` ("7521392"), `date` (the `--when` time with the New York offset, for example `2026-11-13T16:00:00-05:00`) and `info` (a JSON string).
- Change a post: add `--update ID UUID`. It prints the four arguments of `updateScheduledPost`: `blogId`, `id`, `uuid` and `info`. An update replaces the whole post. The id changes on every update; the uuid does not, so log the uuid.
- Load the Metricool tools with ToolSearch (`select:mcp__Metricool_Social_Media_Management__createScheduledPost,mcp__Metricool_Social_Media_Management__updateScheduledPost,mcp__Metricool_Social_Media_Management__getScheduledPosts`), timezone `America/New_York`. Read the schedule one day per call.
- Slots: YouTube three Shorts a day at least 3 hours apart, weekdays 10:00, 16:00, 19:00; weekends 08:00 or 11:00 after a long-form, 14:00 or 15:00, 19:00 ET. TikTok 12:00, 19:00, 21:30 ET. Never in a long-form's slot. The AI label stays on. See MASTER_ORDERS, "Posting".
- After the call: `python3 tools/postkit.py rehost <static.metricool.com link from the response> <local file>` proves Metricool holds the same file.

## 9. Log and tell
- `python3 tools/postkit.py log --net youtube --when "2026-11-13 16:00" --file episodes/drawn-house/<out>.mp4 --spec SPEC --uuid UUID --id ID --media URL [--episode E]` (the time has a space here, not the `T` that `payload` takes) writes `data/posted.csv` (`date,network,episode,file,title`) and the post's uuid in `data/post-ids.csv`. Run it with every scheduling change. With no `--episode`, a row is matched on network and file name; if two rows match it FAILs and asks for `--episode`.
- If Nolan's words caused the work, they go into MASTER_ORDERS the same day with your reading of them; a finding goes into `skills/channel-brain/KNOWLEDGE.md` with its source.
- Commit and push. Then tell Nolan in one or two short lines: what changed, and the one thing he must do if there is one.
