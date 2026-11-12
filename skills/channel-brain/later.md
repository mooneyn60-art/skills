# Later (the work gate's parking list)

One line each. A task lands here when it changes no post in the next 7 days and no scorecard number. Take one out when that stops being true.

- `postkit.py payload --update --from RECORD.json`: start an update from the live Metricool post so fields we do not set (for example notifySubscribers) are kept. Bites only when a live post is edited. (review 11/12)
- Lint for script shape: at least two sourced facts on specs without `_f` tags, a gag, card or `mb` on line 2, three rooms. (review 11/12)
- Lint: are the searched words in the first 40 characters of the title? Today this is read by eye. (review 11/12)
- Refresh `oh-meatball/data/views.csv` (`tools/stats.py`): its last row is 2026-10-29, so `scan.py`'s view checks are off. The scoreboard skill has the real numbers.
- Where viewers live: one week showed about 29% of YouTube views from the US, then the Philippines, Ireland and the UK (research 94). Repeat on three Shorts from different days before touching posting times.
- YouTube Reporting API for impressions and click-through (needs a Google Cloud project and Nolan's sign-in, 15 to 20 minutes): only if the 11/24 vidIQ read returns nothing for Shorts.
- Old tool files that the current flow no longer uses (`channel-brain/tools/outline_lint.py`, `vidcheck.py`, `footage.py`, `realcut.py`; `oh-meatball/tools/ship.py`, `drawn_quick.py`, `sameness.py`): move to an `old/` folder once nothing imports them.
- `oh-meatball/OPERATIONS.md`, `TOWN.md`, `brain/SKILL.md` and `research/experts/*.md` still describe the October flow under "history" markers. Rewrite or delete when there is a quiet day.
- A 13:00 Short on midweek long-form days (the queue holds two Shorts those days): only with numbers that say a third does not hurt.
