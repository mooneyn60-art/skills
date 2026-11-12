# 93 · Titles, tags, hashtags and captions: every angle (2026-11-12)
**Answer:** on both platforms the words that matter are the title (YouTube) and the caption (TikTok), written in the words people type; tags, category and hashtag counts have no shown effect. Changed for the seven funnier cuts: YouTube titles, description openers, hashtags and tags; TikTok captions and hashtags. The TikTok "title" we set in Metricool is not published anywhere.
Asked by Nolan 11/12 about 12:25 ET: "And make sure your tags and everything are also updated to be the best look at All angles". Method: four research agents and two rounds of independent checks (five reviewers), plus my own pulls. Rows: `data/93-autocomplete.csv`, `data/93-ytsearch.csv`, `data/93-metadata-before.json`, `data/93-metadata-after.json`.

## 1. What YouTube says (its own Help pages, fetched 11/12; quotes came through a summarising fetch tool, so near-verbatim)
- Title: 100 characters at most. "Be succinct. Viewers may only see part of your title." "put the most important words near the beginning." "Be accurate ... If not, viewers may stop watching, which can impact discoverability." "Limit ALL CAPS and emoji." https://support.google.com/youtube/answer/12340300
- Tags: "tags play a minimal role in your video's discovery"; "Tags can be useful if the content of your video is commonly misspelled." https://support.google.com/youtube/answer/146402
- Description: "Writing descriptions with keywords can help viewers find your videos more easily through search." "Identify 1-2 main words that describe your video and feature them prominently in both your description and title." https://support.google.com/youtube/answer/12948449
- Hashtags: over 60 and all are ignored; "up to three hashtags that are considered most engaging will appear by your video title"; "The more tags you add, the less relevant they become". Nothing says #shorts is needed or does anything. https://support.google.com/youtube/answer/6390658
- Category: "Select a category so viewers can find your video more easily"; no page says it affects ranking. https://support.google.com/youtube/answer/57404
- Ranking: "What matters is how viewers respond to each video when it's recommended to them"; "it's advised not to change what is already working well". https://support.google.com/youtube/answer/16559651
- Profanity: "hell" and "damn" in a title can still earn ads; "shit" limits them; stronger words remove them. https://support.google.com/youtube/answer/6162278
- AI label: "Disclosing AI content alone won't limit a video's audience". https://support.google.com/youtube/answer/14328491
- Shorts cover: the API can set one ("including YouTube Shorts"), Help says Studio on a computer. Not found: how much of a title shows in the Shorts feed; any link between pinned comments and discovery.

## 2. What TikTok says (developer docs, newsroom, transparency pages, fetched 11/12)
- A video has ONE text field: the API "title" is "The video caption. Hashtags (#) and mentions (@) will be matched", 2,200 UTF-16 units at most. Title plus description exists only for photo posts. https://developers.tiktok.com/doc/content-posting-api-reference-direct-post
- Checked on three of our posted videos (public page JSON against Metricool): the public caption is our Metricool "text", character for character; our Metricool "title" appears nowhere on the page. So the TikTok "title" field does nothing a viewer or search can see.
- Hashtags: "only add hashtags that best represent what your video is about"; "More hashtags won't guarantee a broader reach"; #FYP and #ForYou "work just like all other hashtags". https://newsroom.tiktok.com/5-tips-for-tiktok-creators . The For You signals TikTok names include "The hashtags associated with the video" and the soundtrack, not caption words. https://www.tiktok.com/transparency/en-us/recommendation-system/
- Creator Search Insights (in the app: search "Creator Search Insights") shows what people search and "content gap" topics. Only Nolan can open it. https://newsroom.tiktok.com/en-us/creator-search-insights
- Not readable (script-only pages): what TikTok search indexes, hashtag counts, caption editing, profanity and For You eligibility, any effect of the AI label.

## 3. Our own data
- YouTube titles (62 Shorts with Windsor rows, 10/22-11/9; agent and my own count agree): no title feature moves views once topic, date and style are held fixed. Since 10/27 the median is about 1,100 with or without a digit, at 45-65 or over 65 characters. Raw gaps (series tag 1,143 against 895; question titles 596 against 1,082) are the first week's quiz videos against the house-bug Shorts. Safe shape: "Your" or a number first plus one specific odd fact (best: "Your Bed Mites Die at 130°F" 1.9K, "100 Feet a Night to Your Bed" 1.8K).
- TikTok (research 81, 91): hashtag count shows nothing (3 tags median 224, 4: 222, 5: 258, 6: 214); captions opening with the search phrase 313 against 220 (n=17, tangled with topic and length).

## 4. What people type and what wins (pulled 11/12)
- YouTube suggestions (`data/93-autocomplete.csv`, rank only, no volumes): "can cats taste sweet" (not "sugar"); "why do dogs look guilty", "dog guilty look", "guilty dog"; "do cats know their name"; "dog tail wag meaning", "dog tail wagging left and right"; "what to do if a moose charges", "moose vs bear"; "can you outrun a grizzly bear", "what to do if you see a grizzly bear"; "shark attacks 2025", "what to do if you see a shark".
- YouTube top results (`data/93-ytsearch.csv`): cat-sugar Shorts are tiny (best 216 views); guilty-dog is owned by funny compilations (57.7M, 10.0M); "Think You Can Outrun A Bear? Think Again!" 328K as a Short; "Dog Tail-Wag Direction" 50.6K at 17 s.
- TikTok (32 public videos read, one page each): every real pet or animal video is labelled Pets / Animals / Nature (ours: Comics & Cartoon). The top captions are short and are the question itself: "Do cats know their own name? #catfacts" 1.0M plays from a 29,600-follower account; "Can cats taste sweet things? #mythorfact" 49.8K. TikTok's own suggested searches: "guilty dogs", "Guilty Dog Face", "dog body language" (not "tail wag"), "moose charging", "moose encounter", "Grizzly Bear Videos", "swimming with sharks". Hashtags do not explain reach: the 4.3M and 2.0M dog videos have none. Most shared: #guiltydog (650K and 641K), #catfacts, #grizzlybear (4 of 5), #moose.

## 5. What changed (before and after in `data/93-metadata-*.json`)
- YouTube titles: search words first, hedge kept, one odd fact. Cat "Your Cat Likely Can't Taste Sweet or Sugar: 1 Broken Gene"; dog "14 Dogs Tested: Your Dog's Guilty Look May Not Be a Confession"; grizzly "You Can't Outrun a Grizzly Bear: It Can Run as Fast as a Racehorse"; shark "Shark Attacks 2025: 65 Confirmed Unprovoked Bites Worldwide"; tail wag "Your Dog's Tail Wag May Lean to Its Right When It Sees You". Moose and cat-name keep their titles (the reviewers rejected "knows its name": the study shows cats tell their name from other words).
- YouTube descriptions: only the first sentence (now the searched question) and the hashtag line (two topic tags, #meatballmyths, #shorts last). Shark adds the sourced "29 provoked bites" so the opener's question is answered truthfully.
- YouTube tags: phrases from the suggestions, each 30 characters or fewer, 8 to 12 per video.
- TikTok captions: the on-screen search phrase, the cleared fact, the Meatball gag from the cleared script, a question, five topic hashtags (no #learnontiktok, no brand tag, no #fyp).
- Not changed, with the reason: category (no stated effect), the AI label (stays on), first comments, the TikTok title field (not published), the bug Shorts in the queue (their descriptions already open with the search phrase and their titles already have the safe shape).

## 6. Checks
Round 1, three reviewers on the YouTube draft: 7 fixes (sweets to sugar wording, "knows its name" rejected, whose right, the shark question, a grizzly tag that promised charge advice, tags over 30 characters, two wanted search phrases). Round 2, two reviewers on the merged YouTube set and the TikTok captions: 6 fixes, every one a return to cleared wording (the dog caption got its "owners told the dog not to eat a treat and left the room" back; the moose caption its "because a moose won't chase you very far"; the grizzly caption now quotes the TikTok cut's own joke, "Meatball is now the tennis ball"; "anyway" came out of the cat caption; the tag "cats know their name" became "do cats respond to their name"; the shark opener became one sentence). All mechanical counts pass: titles 77 to 99 of 100 units, tags 30 characters or fewer and 175 to 287 in total, captions 243 to 493 of 2,200, five hashtags each on TikTok and four on YouTube.
Applied in Metricool 11/12 12:55 to 12:56 ET to all 14 posts (the cat Short for 16:00 first). One extra test: the Fri 11/13 dog Short carries `videoCoverMilliseconds` 1900, the frame with the card GUILTY LOOK / MAY NOT BE A CONFESSION; Metricool accepted it, and whether YouTube shows it is read from the public thumbnail on Sat 11/14.

## For the next scripts (found here, cannot be fixed without re-rendering)
- Say the searched phrase in the first spoken sentence. YouTube matches searches against "the title, tags, description, and video content" (https://support.google.com/youtube/answer/16090438). The cat cut says "sugar" where people type "sweet"; the moose cut never says "charges" or "attack".
- TikTok's own search wording is often not the question we assumed: "guilty dogs", "dog body language", "moose charging", "bear encounter". Read `suggestedWords` on a few top videos of the topic (one curl per public page) before fixing the on-screen phrase.
- The shark title says 2025; searches already lean to 2026. Replace the count when the 2026 summary is out, never before.

## Could not measure
- Search volumes (suggestions give rank only); TikTok hashtag sizes (not on public pages) and TikTok search results (need a login); what TikTok search indexes.
- Any effect of tags, hashtags, category or description on our own views: we have never varied them.
- How much of a title shows in the Shorts feed; whether #shorts does anything.
- Whether the new metadata helps: these seven also changed topic and jokes at the same time.
