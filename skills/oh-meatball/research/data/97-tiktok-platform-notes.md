# 97 · What TikTok itself says (platform notes, fetched 2026-11-12)
**Answer:** nothing TikTok publishes says drawn, AI-labelled, narrated or scheduled-by-API videos get less reach, and nothing describes a 200-view batch. What TikTok does say: a low view count "doesn't necessarily mean it broke a rule"; the one place a restriction shows is the analytics Performance tab (a warning bar) and Account Check. Reach rules that could touch us are the unoriginal rule (reused material), the spam rule, and the new viewer slider for AI-generated content. Logged-out TikTok search and Creative Center hashtags could not be read.
Method: headless Chromium (Playwright) on TikTok's own pages, about 25 page loads, 1.5 s or more apart, no logins. Pages are quoted as the browser rendered them on 11/12. Read-only; no signed link or token saved.

## 1. For You feed (FYF) eligibility
- Page "For You feed Eligibility Standards", released 2026-08-25, effective 2026-09-24. https://www.tiktok.com/safety/en/policies-and-engagement/fyf-standards
  - "We make ineligible for the FYF certain content that may not be suitable for a broad audience."
  - "Even if a video doesn't make it to the FYF, people may still find it through search or by going to a creator's account. If a video isn't getting many views, it also doesn't necessarily mean it broke a rule. Creators can check TikTok's analytics to see how their videos are performing, including if there were any made ineligible for recommendation."
  - Repetition rule: "We aim to prevent our systems from repeatedly recommending content that could lead to a negative experience, such as extreme fitness or dieting, sexual suggestiveness, sadness, or overgeneralized mental health advice." (None is our topic.)
- Integrity and Authenticity, same dates. https://www.tiktok.com/safety/en/policies-and-engagement/integrity-authenticity
  - "Content is also ineligible for the FYF if it includes unoriginal or reused material without anything new."
  - "Content that tries to manipulate people into giving gifts or inflating likes or follows isn't eligible for the FYF."
  - "We strictly prohibit automation tools, scripts, or other tricks designed to bypass our systems." (This is about bypassing, not scheduling.)
  - Misinformation: "Content is ineligible for the FYF if it contains misinformation that may cause moderate harm to individuals or society." Note for fact claims on dangerous animals (what to do if a moose charges): safety advice that is wrong is the one place a fact error could cost eligibility. We cannot tell if it would.
- Creator Academy "Understanding TikTok's Originality Policy", last updated 2026-09-26. https://www.tiktok.com/creator-academy/article/tiktok-originality-policy
  - Unoriginal is: "Content copied completely from others." "Content that is largely repurposed from another source without adding any creative edits." "Content combined from multiple sources with little or no additional information and/or content value." "Content with someone else's visible watermark or superimposed logo."
  - "Unoriginal content may be removed from the For You feed, making it harder to discover."
  - "Think your content is original, but still not getting many views? It may be due to a lack of community engagement rather than being ineligible for the FYF."
- Creator Academy "Why is your video not getting recommended on the For You feed?", last updated 2026-04-30. https://www.tiktok.com/creator-academy/article/video-not-recommended
  - Lists unoriginal ("recycled, spammy"), shocking or graphic, mature, dangerous activity or challenges. "If your content is made ineligible for the FYF or otherwise restricted, this information will appear in the TikTok analytics tool."
  - "if one of your videos isn't getting many views, it doesn't necessarily mean it wasn't recommended for the For You feed."
- Mass-produced or templated videos: NOT FOUND on any TikTok page read. The unoriginal definition above is the nearest text, and it is about reused or copied material, not a repeated format. Our 81 posts share a template but not footage.
- Newsroom "How TikTok recommends videos #ForYou", 2020-06-18 (old, still live). https://newsroom.tiktok.com/how-tiktok-recommends-videos-for-you?lang=en
  - "We also don't recommend duplicated content, content you've already seen before, or any content that's considered spam."
  - "your For You feed generally won't show two videos in a row made with the same sound or by the same creator."
  - "neither follower count nor whether the account has had previous high-performing videos are direct factors in the recommendation system."
  - "videos that have just been uploaded or are under review, and spam content such as videos seeking to artificially increase traffic, also may be ineligible for recommendation into anyone's For You feed."
- Newsroom/Transparency "recommendation system" page (undated, copyright 2025). https://www.tiktok.com/safety/en/policies-and-engagement/recommendation-system
  - The appendix lists what the system predicts: "Like, share, comment on, or mark a video as 'Not Interested.'"; "Follow the video's author or interact with their profile."; "Finish, skip, or favorite a video."; "Spend a certain amount of time viewing a video."; "Tap the video's soundtrack."
  - Video signals it uses: "The time the video was posted." "The video's soundtrack." "The length of the video." "The hashtags associated with the video." "The language setting of the video's author."
  - Step called "Similarity check": top-ranked videos that are "too similar to each other - for example, they use the same sound - we replace them". Our drawn template with one AI voice is a similar-look series; this text names sound, not look. Not measurable.
  - "Rules ... ensure that videos in your For You feed include content from creators in your region".
  - No page says new videos get a small first batch. Nothing says how many people see a new video.

## 2. AI-generated content (AIGC): labels, viewer control, distribution
- Newsroom "More ways to spot, shape and understand AI-generated content", dated 2025-11-24 on the page (press coverage ran 2025-11-18, so the date is not certain). https://newsroom.tiktok.com/more-ways-to-spot-shape-and-understand-ai-generated-content?lang=en-GB
  - "In the coming weeks, we'll start testing a new AI-generated content control in our 'Manage topics' feature to empower people to choose how much AIGC they want to see in their For You feeds."
  - "the AIGC setting is intended to help people tailor the diverse range of content in their feed, rather than removing or replacing content in feeds entirely. This means that people who love AI-generated history content can see more of this content, while those who'd rather see less can choose to dial things down."
  - "We require people to label realistic AI-generated content on TikTok ... This includes labeling tools we offer creators as well as our own detection models. We also use ... C2PA Content Credentials ... These efforts helped label over 1.3 billion videos to date."
  - Invisible watermarks: "we'll start adding invisible watermarks to AI-generated content made with TikTok tools like AI Editor Pro, and content uploaded with C2PA Content Credentials."
  - Not stated: whether the test reached everyone, or how much the slider cuts reach. I could not read the in-app control.
- Creator Academy "AI-generated content label". https://www.tiktok.com/creator-academy/en/article/ai-generated-content-label
  - "Applying the label will not have an impact on organic engagement with your content, provided that your content isn't violative and meets our For You feed eligibility standards."
  - "Turning on the AI-generated content setting won't affect the distribution of your video as long as it doesn't violate our Community Guidelines."
  - "No, you cannot edit or remove the label after posting your video at this time."
  - Disclosure "isn't needed when": "Using artistic styles, like anime"; "Using generic text-to-speech (TTS) narration, when the TTS isn't a recognizable voice of a known individual". (The label stays on by standing order; this only records what TikTok requires.)
- Help Center "AI-generated content". https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content (redirected to a tiktok.com/support FAQ)
  - AIGC "includes images, video and/or audio that is generated or modified by artificial intelligence, such as ... depictions created in a particular artistic style (e.g. painting, cartoons, and anime)."
  - "Creator label ... will read 'creator labeled as AI-generated'." The two TikTok pages differ: this one counts cartoon style as AIGC, the Creator Academy one says anime style needs no disclosure.
- Net reading: TikTok says the label itself costs nothing. The only measurable cost TikTok admits to is the viewer slider, and it says that setting reduces and increases, it does not remove. No TikTok figure on how many viewers use it.

## 3. Content Posting API (the route Metricool uses)
- "Content Sharing Guidelines", last updated 2026-08-04. https://developers.tiktok.com/docs/en/content-sharing-guidelines
  - "all content uploaded via this endpoint will be restricted to private viewing mode. To lift this restriction, your API client must undergo an audit". "Unaudited API Clients can only post contents in SELF_ONLY viewership." Our posts are public, so the client posting for us is an audited one (my inference; the page does not name Metricool).
  - "Posting cap: There is a limit on the number of posts that can be made to a creator account in a 24-hour window via Direct Post API. The upper limit may vary among creators (typically around 15 posts per day/ creator account) and is shared across all API Clients using Direct Post." We post 3 to 4 a day.
  - "Intended Use: API Clients should facilitate authentic creators to post original content to TikTok. Not acceptable: An app that copies arbitrary contents from other platforms to TikTok."
  - Required in the client: the user picks title, privacy, comment/duet/stitch, and commercial-content disclosure; "no default value" for privacy.
- Direct Post reference. https://developers.tiktok.com/docs/en/content-posting-api-reference-direct-post
  - Video post fields found: title, privacy_level, disable_duet, disable_comment, disable_stitch, video_cover_timestamp_ms, brand_content_toggle, brand_organic_toggle, is_aigc ("Set to true if the video is AI generated content ... labelled with Creator labeled as AI-generated tag"). No field for a sound or music on video posts. The photo example has "auto_add_music" (photos only). So: an API video carries the sound baked into the mp4; the API cannot pick a library sound. TikTok does not call this a reach limit.
  - Rate limits: "Each user access_token is limited to 6 requests per minute."
  - Error text "reached_active_user_cap", "unaudited_client_can_only_post_to_private_accounts".
- Nothing on developers.tiktok.com (5 pages read: get started, guidelines, direct post, upload, media transfer) says anything about reach, For You treatment, "posted via" labels or trending-sound limits for API posts. The FAQ page returned 404. NOT FOUND is a result here: TikTok publishes no reach difference.
- Lore (vendor blogs, no TikTok source): "API posts reach less" and "schedulers cannot use trending sounds". The sound half matches the missing field above. The reach half has no source.

## 4. Account status and what to do about low views
- Newsroom "More updates to help the TikTok community create and share safely", 2024-04-17. https://newsroom.tiktok.com/more-updates-to-help-the-tiktok-community-create-and-share-safely?lang=en
  - "Account Check ... will enable creators to quickly audit their account and their last 30 posts, and see at a glance whether they are in good standing on TikTok ... whether access to certain features, like comments or direct messaging, has been restricted ... whether their content has been removed for breaking our rules or has been restricted from reaching the For You feed."
  - Policy: "make an entire account temporarily ineligible for recommendation in the For You feed if a creator repeatedly posts content that goes against our For You feed standards. Their account and content will be harder to find in search. We will notify creators when their account has been restricted in this way, and they will be able to appeal."
- Help Center "Why is my account not being recommended?". https://www.tiktok.com/support/faq_detail?id=7543604783110969862&category=web_account
  - "If you repeatedly post content that is unsuitable for the For You feed, your account and posts won't appear in the For You feed and will be harder to find in search." "We may automatically restore your account to good standing at any time". "we'll notify you in your inbox notifications and profile": a notice reading "Ineligible for recommendation" under the username; the appeal button is at the top of that list.
- Creator Academy "Moderation and Appeals", last updated 2026-09-26. https://www.tiktok.com/creator-academy/en/article/guidelines-moderation-status-and-appeals
  - Where states show: Inbox (Account Updates; full record in Account Status), Profile (taken-down videos carry a tag), "Analytics: if a video isn't eligible for the For You feed, a warning bar appears at the top of the Performance tab."
  - "strikes expire from your account record after 90 days."
- States that limit FYF: (1) one video ineligible (warning bar on its Performance tab); (2) whole account ineligible for recommendation (inbox and profile notice, search harder too); (3) bans for repeated or severe violations. TikTok's own advice for low views: check analytics for an ineligibility notice first; otherwise treat it as "a lack of community engagement" and adjust content (originality page and not-recommended page above). TikTok gives no other low-view advice on the pages I could read.
- Owner check list (screens only Nolan can open, none shown to the public): Inbox > Account Updates; profile page "Ineligible for recommendation" line; TikTok Studio > More tools > Account check; Performance tab of the last 5 posts for the warning bar. The public-page flags we read earlier (isReviewing False, penalty 102) are not documented by TikTok.
- Not readable: Creator Academy "Understanding the Recommendation System" and "Keeping your account in good standing with content check lite" (script only; 477 characters returned). Their menu titles are all I have.

## 5. Evidence on the "200 view jail" (measured, not lore)
- TikTok: no statement of a 200 limit or a first batch (section 1).
- Buffer, 11.4 million TikTok posts, 150,000+ accounts, published 2025-10-08, fixed-effects model (observational). https://buffer.com/resources/how-often-should-you-post-on-tiktok/ . Median views per post by weekly posts: 1 = 489; 2 to 5 = 506; 6 to 10 = 487; 11+ = 459. 90th percentile: 3,722; 6,983; 10,092; 14,401. "the relative gains hold true across all account sizes." Reading: a median near 500 at any frequency, and more posts mostly add top-end chances. Our median is 229, about half the Buffer median. Buffer gives no median by follower band, so we cannot say how far below small accounts we are. Fetched via WebFetch 11/12.
- No study of an early-batch cap, its causes, or what lifts it was found. The only search hits were vendor blogs (see lore). Nothing measured says what changes it.
- Lore, at most five lines (all vendor or creator blogs, no data): (1) first test group "about 150 to 300 people"; (2) failing the batch is low watch-through; (3) fix = hook, new visual every few seconds, one niche; (4) one blog says 200 is "a coincidence" of small test audiences; (5) a stuck video "rarely recovers". Our 66 old posts that gained a median 1 view in 2 days (research 91) fit (5) but prove nothing about the cause.

## 6. Logged-out search and Creative Center (headless browser, 11/12)
- Search. https://www.tiktok.com/search?q=... for "why does my dog look guilty", "can cats taste sweet", "what to do if a moose charges": the page loaded (tabs Top, Users, Videos, LIVE, Photo; "Log in" button) but the result grid stayed as grey placeholder boxes after 8 s, and again after 20 s on the Videos tab for "can cats taste sweet". No result video links in the page. The search results call never came back; the suggestion call did (autocomplete for "cat" gave "Popular Cat TikToks", "why do cats like catnip", "cuddly cat"). So: who ranks and whether our videos appear: NOT MEASURED. I stopped after one retry, as ordered. Search results need a login or a real device. Our 18% Search share (TikTok Studio) is the only search number we have.
- Creative Center. https://ads.tiktok.com/business/creativecenter/... hashtag trends redirected to https://ads.tiktok.com/creative/creativeCenter/trends/hashtag?countryCode=US&period=7&region=US . Logged out it shows only the top 3 overall for the US in 7 days: #veteransday (News & Entertainment, 63K posts, 68.8M views), #mymoonmyman (News & Entertainment, 19.8K posts, 43.9M views), #piratetoken (Games, 59.1K posts, 428.3M views). "View more" asks to "Log in or sign up". The user-info call answered "invalid user" and then "too many requests" (code 40100). No Pets and Animals filter and no 30-day view without a login: NOT MEASURED. I stopped there.

## What this changes for the queue
- Nothing found says to change the look, the label, the account type or the Metricool route. All four are cleared as far as TikTok's pages go (no stated reach cost; the only stated cost is the viewer slider).
- Cheap and free: Nolan opens Account check and the Performance tab of a few recent posts (section 4 list). If a warning bar or "Ineligible for recommendation" shows, that settles the view jail; if none, the rule-based cause is ruled out and engagement is what TikTok itself points to.
- Possible, small: the API video has no library sound, and TikTok says the system uses the soundtrack as a signal. Whether a library sound would help a drawn narrated video is not shown anywhere. Test only if a native-app post of one video is allowed (it has not been; do not propose it as a rule).

## Not measured
- In-app screens (Account check, analytics warning bar, the AIGC slider): owner only.
- Logged-out search ranking and Creative Center Pets and Animals hashtags: need login.
- Whether Metricool's client is audited (inferred from public posts).
- Creator Academy recommendation page and content-check-lite page (script only).
- Any size, timing or rule for a first test batch.
