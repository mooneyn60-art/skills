# 94 · What the agent can and cannot see, and what was added (2026-11-12)
**Answer:** the biggest blind spot is retention on both platforms. One free fix was found (YouTube views by source, per video), one needs a single tap from Nolan (TikTok watch time through Windsor), one arrives on 11/24 (vidIQ credits). Today's hand work is now a tool and three skills.
Asked by Nolan 11/12 about 12:58 ET: "And Delvin yourself and skills mcps or repositories you want to help us grow whatever you need" (read as: develop yourself). Method: five research agents (tool map, gaps, traffic data, TikTok routes, YouTube routes) and three reviewers. Rows: `data/94-youtube-traffic-by-video.csv`, `data/94-youtube-traffic-by-day.csv`, `data/94-shorts-source-shares.csv`.

## 1. Gaps that blocked decisions (counted across research 60 to 93)
| Gap | Files that hit it | Cheapest route |
|---|---|---|
| YouTube retention curve, stayed-to-watch per Short | 10 | Windsor engaged share now (proxy); vidIQ from 11/24; a Studio screenshot |
| TikTok watch time, finish rate, For You against Search | 6 | Windsor `tiktok_organic` (one tap by Nolan, untested for a personal account); else Supermetrics; else a weekly Studio download |
| YouTube impressions, click-through, "Shown in feed" | 5 | vidIQ from 11/24; a Studio screenshot. No Google API field exists for "Shown in feed" |
| YouTube views by source per video | 3 | Windsor, free, now (section 2) |
| Other channels' retention and transcripts | 6 | vidIQ transcripts from 11/24; heatmaps not possible |
| Search volumes, TikTok hashtag sizes | 6 | suggestions give rank only; TikTok Creator Search Insights screenshot |
| Data lag of 3 days on new posts | 5 | none; read new posts by public counts |
Also found: about 29% of YouTube views in the last 7 days came from the US, then the Philippines 12.8%, Ireland 12.3%, the UK 11.4% (Windsor `country`; one week, a lead to re-check before touching the posting times).

## 2. New data: where YouTube views come from (Windsor `traffic_source`, 10/22 to 11/09, 63 Shorts and 10 long-forms)
- The grouped pull returns no video ids; one call per video with the filter `[["video","eq",ID]]` works (73 calls).
- Shorts: 93.7% of views from the Shorts feed (54,230 of 57,906), 5.5% from search (3,173), 0.9% from everything else. Engaged share inside the feed 43.8%, inside search 50.0%.
- Shorts that ended under 600 views against those at 1,000 to 2,000: median feed views 290 against 1,093, and a lower engaged share inside the feed, 32% against 46% (n=14 and 36 without the six under 100 views; permutation p 0.0009). So low Shorts were shown less and held viewers less. The field has no impressions, so it cannot say which came first.
- Search share does not separate good from poor Shorts (4.2% against 3.5%, p 0.47). Search is a steady add-on of about 140 views a day, and it reaches Shorts the feed ignored (6 to 49 search views on Shorts with almost no feed views).
- Most search views: "Are Daddy Longlegs the Most Venomous Spiders?" 631 (26.7% of its views), "The Spider on Your Window Is Watching You Back" 201. The top four all name a spider; 12 of the top 15 were posted 10/24 to 10/31, so age is not controlled.
- Long-form: 655 views, none from the Shorts feed. Related videos 313 (99% engaged), subscribers 300 (28% engaged), search 23. The Shorts do not send viewers to long-form through the feed.
- Windsor's last day is 11/09, so the 11/10-11/11 drop is not in this pull. Re-pull about 11/14.

## 3. Routes to the numbers still missing
- TikTok. Windsor's `tiktok_organic` field list (https://windsor.ai/data-field/tiktok_organic/) has `video_average_time_watched`, `video_full_watched_rate`, `video_impression_sources_*` and retention by second. Windsor's guide says "A TikTok Business or Creator account you manage"; whether a personal account is accepted is untested, and connecting is the test. The account must stay personal: TikTok's Creator Rewards page says "Only Personal Accounts are eligible. Business Accounts ... do not qualify." (https://www.tiktok.com/creator-academy/article/creator-rewards-program). Fallbacks: Supermetrics (its docs accept a personal account with 100 or more followers; watch time and completion rate, no traffic split, lifetime totals only); a weekly TikTok Studio download by Nolan. Metricool lists the same metrics but its help says personal accounts get limited data, which is why we see nulls. TikTok's Display API has no analytics fields.
- YouTube. Retention curves are in the YouTube Analytics API (`audienceRetention`, one video per query, owner only); impressions and click-through only in the Reporting API reach reports (`channel_reach_basic_a1`, added 2026-01-15). Both need a Google Cloud project and an OAuth consent by the owner (15 to 20 minutes, six steps). Not confirmed for Shorts. vidIQ reads Studio-only numbers through the owner's browser extension: `vidiq_channel_analytics_extended` (`shorts_stayed_to_watch` with feed impressions for up to 50 Shorts per call, `thumbnail_ctr`), `vidiq_channel_analytics` report `audience_retention`; 5 credits a call, balance 3, reset 2026-11-24 14:30 UTC. Windsor cannot be extended to these (its custom fields are formulas over existing fields). Studio's Advanced mode exports up to 500 rows; retention export is not documented.

## 4. What was built (all in the repo)
- `tools/postkit.py`: `render` (renders to a side file and replaces the video only after a transcript check), `voicecheck`, `sheet`, `lint` (the metadata standard as a gate), `payload` (the exact Metricool post body, refused when lint fails), `log` (posted.csv and the post's uuid), `rawurl`, `rehost`, `kw` (search suggestions and top results), `ttpage` (a public TikTok page: plays, label, TikTok's suggested searches, AI label). Each replaces a step done by hand on 11/12.
- `tools/setup_env.sh`: one command that makes a fresh machine ready (packages and the speech model).
- Skills in `.claude/skills/`: `make-short` (topic to logged post), `post-metadata` (titles, tags, captions), `scoreboard` (which number comes from where).
- The old flow (`ship.py`, `outline_lint.py`, `drawn_quick.py`, `sameness.py`) works on outline YAML only; the last outline is from 11/03 and the pet and survival specs are plain JSON. They are kept, not used.

## 5. Asked of Nolan
One thing: open the Windsor TikTok link (sent in chat, not stored here because it is a signed link) and approve. Later, on 11/24: have Chrome open with the vidIQ extension signed in to the channel, so the stayed-to-watch read can run.

## Could not measure or check
- Whether Windsor accepts the personal TikTok account; whether the YouTube retention API returns curves for Shorts; whether the reach report includes feed exposures.
- Anything after 11/09 in Windsor; which day boundary Windsor uses.
- Search volumes; other channels' retention.
