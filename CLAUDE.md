# Start here (every session, and again after any context summary)

This repo runs the "Meatball Myths" channel (YouTube + TikTok) for Nolan.

1. Read `skills/channel-brain/MASTER_ORDERS.md` before doing or proposing anything. It holds the standing orders, the banned title words, the long-form format, the agent routing table and the verified platform facts. The page fits in one Read (it is kept under 52,000 bytes). If a Read says the page was cut off, read the rest before acting. `skills/channel-brain/MASTER_ORDERS_LOG.md` holds the history and the reasons: read it when a rule's reason matters. If the chat gets summarized, read MASTER_ORDERS again: rules have been forgotten that way before.
2. Then read `skills/channel-brain/KNOWLEDGE.md` and the newest files in `skills/oh-meatball/research/` (highest number = newest).
3. `skills/oh-meatball/data/posted.csv` logs everything scheduled or posted. Update it with every scheduling change.

## How Nolan wants to work
- Very short replies (Nolan 11/10: "I can't read that much that quick"): 1-2 short lines, plain words, no lists, tables or headers unless he asks. Say only what changed or the one thing he must do. Details go in the repo, not the chat.
- Decide from the data yourself. For a big format change, show the options and the evidence first.
- Research before acting, every time, and end every research run in a queue or script change. Nolan 11/11, after I built and scheduled two videos on a guess: "No wait do research don't jump to conclusions you need to do this every time." When he raises a new direction, get the numbers and show him the options before building or scheduling anything. If a research run gets stopped, start it again; a stop is not permission to skip it.
- Give the source of every number, and say what could not be measured.
- A different model fact-checks every script before it is scheduled.
- His one-line reactions to videos ("too short", "needs more info") are orders: write them into MASTER_ORDERS the same day.
- Commit and push all work. Never `git add -A`; add paths with `git add --sparse <paths>`.

## Tools and skills (added 11/12, on Nolan's "develop yourself")
- Fresh machine: `bash skills/oh-meatball/tools/setup_env.sh` (packages and the speech model; ends with "ready").
- `skills/oh-meatball/tools/postkit.py` does the checks between a spec and a scheduled post: `render` and `voicecheck` (never schedule a file that has not passed), `lint` (titles, tags, captions), `payload` (the Metricool post body; `--call` and `--update` print the exact tool arguments), `log`, `rawurl`, `rehost`, `kw`, `ttpage` (`--csv data/tiktok-stats.csv` keeps a daily record), `trends` (Google Trends: relative search demand, rising searches, seasons), `teardown` (how a video opens: first words, cuts, a sheet of the first 3 seconds), `selftest`. Run it from `skills/oh-meatball`.
- Skills in `.claude/skills/`: `make-short` (topic to logged post), `post-metadata` (titles, tags, captions), `scoreboard` (which number comes from where). MASTER_ORDERS still wins over them.
- A batch of videos: the saved workflow `shorts-batch` (`.claude/workflows/shorts-batch.js`; fact pack, script pair, second-model check, render, lint for a list of topics from the newest topic queue in `skills/oh-meatball/research/data/`). Agent roles with the rules built in: `researcher`, `fact-checker`, `short-builder` (`.claude/agents/`).
- Hooks (`.claude/settings.json`): `.claude/hooks/git-guard.py` blocks whole-tree checkout, `reset --hard`, stash, clean, `add -A` and any git write by an agent; `.claude/hooks/session-start.sh` installs the render tools on a fresh cloud machine. Nolan 11/12: "you have full control download whatever you neex": install what the work needs; logins, approvals and money stay his.
- If a file named here or in a skill is not on disk, the checkout is sparse: `git sparse-checkout list` must include `/.claude/`, `/CLAUDE.md` and `/skills/oh-meatball/scripts/drawn-house/` (add with `git sparse-checkout add <path>`; one old video: `git show HEAD:<path> > /dev/shm/x.mp4`). Never run `git sparse-checkout reapply` or `git checkout -- .` with uncommitted work.
- Agents never run a git command that changes the repo; the main session commits, and commits before starting agents (MASTER_ORDERS, "Agent routing").
