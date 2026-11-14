# 114: which news draws search views (Nolan 11/13 about 22:39 ET)

His words: "Ok so what other news can we do this with that draws lots of search views cause all the big videos we have are search view traffic". The second half is his reading of TikTok Studio (traffic sources); it cannot be seen from here (Personal account, Studio only), so it is recorded as his observation, not measured.

## What today's seven topical TikToks did (public pages, 22:33 ET; `research/102`)
| video | what kind of news | plays | age |
|---|---|---|---|
| Why the ground stop happened | a disruption ends: the cause | 9,631 | 1.4 h |
| Flights grounded (first) | a disruption starts, hours old | 8,473 | 3.4 h |
| Jensen Huang allegations | a scandal and a resignation, a day old | 3,075 | 11.7 h |
| Microsoft outage | a disruption, a day old | 2,912 | 7.5 h |
| GTA 6: what's confirmed | a planned release, six days ahead | 1,182 | 8.4 h |
| Ground stop update ("still on") | no new event | 220 | 2.4 h |
| Jensen part 2 | a recap | 90 | 6.4 h |
Account median before today: 333.

## Search evidence (Google Trends through `postkit.py trends`, US, last month, relative within each set; YouTube suggestions through `postkit.py kw`)
- Web search, set 1: "ground stop" 33.5, "gta 6" 15.8, "microsoft outage" 14.8, "jensen huang" 11.0 (last four weeks). The order matches our plays except GTA 6, where the search is spread over months and big channels own it.
- Web search, set 2: "outage" 64.5 in the last four weeks (mean 11.6), "what happened" 18.2, "recall" 4.0, "is it down" 3.5, "resigns" 0.2. "Outage" is the word people type when something breaks.
- YouTube suggestions today: "why is outlook down", "why is there a ground stop", "what happened to outlook today", "outage faa", "outages today". The question shapes are "why is X down", "why is there X", "what happened to X today".
- TikTok's own suggested searches on our videos are the story in plain words: "faa grounds all flights", "all flights are grounded", "airport system down", "Microsoft Outlook Outage", "Huang Resigns as Nvidia CEO", "gta 6 release date", "how much will gta 6 cost".
- Google's US trending feed at 22:40 ET is otherwise sport and celebrity names: crowded, and not ours.

## Reading (mine)
What worked is not "news" in general. It is a sudden thing that breaks or changes many people's day, where they type a "why" or "what happened" question within hours and there is a plain answer with a source: (1) outages of things people use daily (email, phones, banks, apps, game networks, airlines, power); (2) the end of the same event with its cause; (3) a sudden exit or scandal of a famous name, first day only. A planned event (a release date) brought a third of that; a follow-up with no new event brought almost nothing.
Not measured: how much of the plays were search and how much For You (Studio only); whether the effect holds on a second day (all seven are under 12 hours old); YouTube (the airline Shorts have 100, 6 and 1 views: the effect is TikTok's so far).

## Watchlist (kinds of event, with the trigger to look for)
1. A big app or service down: "is X down", Downdetector spikes (Instagram, TikTok, ChatGPT, Discord, PlayStation Network, Xbox, Steam, banks, phone carriers, card payments). Two videos: "why is X down" within the hour, then "what caused it" when it is fixed.
2. Travel breaking: ground stops, airline system failures, storms closing airports. Thanksgiving week (Wed 11/25 to Sun 11/29) is the busiest travel week of the year.
3. Launch-day failures: GTA 6 launches Thu 11/19; if servers or downloads fail, "why is GTA 6 not working" is an outage video, the kind that worked, not a release explainer.
4. Shopping days breaking: Black Friday 11/27 and Cyber Monday 11/30 (sites or payments down).
5. Recalls and warnings that touch a home (food, cars, medicine) on the day of the notice, from the agency's page.
6. A sudden exit or scandal of a household name, day one only, sourced, with the same guardrails as the Jensen video.
Stay away from: war, attacks, deaths, elections and court cases (not comedy, and the facts move in ways a joke cannot follow); sport and celebrity gossip (crowded, rights and privacy).

## How it could run (options for Nolan; nothing is built until he picks)
A. News watch: a scheduled check a few times a day (trending feed, "outage" searches, Downdetector's front page) that messages him a one-line alert with the numbers; he says go, and the video is out in about an hour. Cost: small checks; a build only on his go.
B. On call only: he names the story, as today.
C. Auto-post: the watch builds and posts on its own. Not recommended: a wrong fact on a breaking story is the one mistake that costs the account, and credits would run without a ceiling.

## Nolan's TikTok Studio screenshots (11/13, 23:02 and 23:03 ET) and his answer
Two of today's videos (he did not say which two), Traffic sources:
- Video A: Search 95.3%, For You 4.1%, Other 0.5%, Personal profile 0.1%, Direct messages / Following / Sound 0.0%.
- Video B: Search 99.7%, Other 0.3%, For You 0.0%, everything else 0.0%.
- "Search queries" on both: "Each search query has low traffic at the moment" (no list yet).
So his reading is right, and measured for the first time: these videos are found by search, almost not at all on For You. That reverses research 81 for news videos (it said captions and hashtags are not the lever): here the words people type are the whole audience. What follows for every topical video: the caption opens with the exact phrase people type (TikTok's suggested searches and `postkit.py kw`), the same phrase is said in the first sentence and stands on the first card, and speed matters because the searching stops when the event does. It also explains the two flops: nobody searches "ground stop update still on" or "jensen huang part 2".
Still not seen: the queries themselves (Studio shows them once one has enough traffic), watch time, and the same screen for an animal video (is the 333 median mostly For You?).

Asked "Want me to set up a news watch ... so you just say go?", he answered: "Yes". Set up 11/13: a scheduled task four times a day (08:47, 12:47, 16:47, 20:47 ET) in a fresh session each time; it reads this file and `data/news-watch-log.csv`, checks the trending feed and searches, and on a hit messages the main session, which tells him in one line. It builds and posts nothing on its own.
The scheduled task is "News watch for Meatball Myths" (trig_01UTxnfDdv3ygbWrKdMcghcv); first run Sat 11/14 08:47 ET. Each run starts with no repo and no connectors: it reads this file and the log from the public raw links, alerts as its final reply (a phone notification for Nolan) and tries to message the main session. The main session adds every alert, and what was done with it, to `data/news-watch-log.csv`. If the alerts are noise after a few days, cut it to twice a day or stop it.
