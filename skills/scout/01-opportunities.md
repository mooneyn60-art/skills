# Scout 01: Opportunity scan (2026-10-15)

Method: I searched Hacker News comments from 2025-2026 through the Algolia API, plus news, vendor and FTC pages.
Reddit blocks this crawler, so it was not used. No vidIQ credits were spent.
Scores run 1-5, and 5 is best. For **Risk**, 5 means low legal or platform risk. **Auto** means how fully our agents can deliver the product with no human.

## Ranked candidates

| # | Need (who) | Evidence | Demand | Gap | Auto | Speed to $ | Risk | Total |
|---|---|---|---|---|---|---|---|---|
| 1 | **AI answers spread false facts about my business** (local small businesses) | Business owners in the news, 2025-26 (see the winner section) | 4 | 4 | 4 | 4 | 4 | **20** |
| 2 | AI-shopping readiness for tiny Shopify/Etsy shops | [dataslayer](https://www.dataslayer.ai/blog/how-to-sell-on-chatgpt-complete-setup-guide-for-2026), [ROI Rev](https://roirevolution.com/blog/shopify-chatgpt-integration/) | 3 | 3 | 4 | 3 | 4 | 17 |
| 3 | A "second opinion" scam inbox for elderly parents (adult children pay) | [HN 2026-08-05](https://news.ycombinator.com/item?id=49183068), [HN 2025-11-23](https://news.ycombinator.com/item?id=46027312), [HN 2025-09-15](https://news.ycombinator.com/item?id=45248343) | 4 | 2 | 4 | 3 | 3 | 16 |
| 4 | Check a rental listing before paying a deposit (renters aged 18-29) | [FTC: $65M reported losses](https://ftc.gov/news-events/data-visualizations/data-spotlight/2025/12/rental-scams-hit-home-65-million-reported-losses), [HN 2025-05-14](https://news.ycombinator.com/item?id=43981380), [HN 2025-07-03](https://news.ycombinator.com/item?id=44459670) | 4 | 4 | 2 | 3 | 2 | 15 |
| 5 | Ghost-job and fake-recruiter filter (job seekers) | [HN 2026-04-17](https://news.ycombinator.com/item?id=47807108), [HN 2026-08-31](https://news.ycombinator.com/item?id=49504825) | 4 | 2 | 3 | 3 | 3 | 15 |
| 6 | Sorting floods of AI-written job applications (small employers) | [HN 2025-01-24](https://news.ycombinator.com/item?id=42817227), [HN 2026-10-15](https://news.ycombinator.com/item?id=50105289) | 4 | 1 | 3 | 2 | 3 | 13 |
| 7 | Monitoring deepfake impersonation of small creators and coaches | [HN 2025-08-29](https://news.ycombinator.com/item?id=45070147), [Loti AI free tier](https://www.barchart.com/story/news/31612706/dolphin-partner-loti-ai-expands-digital-identity-protection-to-everyone) | 3 | 2 | 2 | 2 | 2 | 11 |

Why the others lost:
- **#2:** Shopify now enrolls eligible merchants in agentic storefronts automatically, so this gap is closing.
- **#3:** Free tools already do this: [Norton Genie](https://us.norton.com/products/genie-scam-detector) and [Bitdefender Scamio](https://betanews.com/2023/12/14/bitdefender-launches-free-ai-powered-scam-detector).
- **#4:** A real check needs phone calls and reverse image search, so it is hard to automate. A wrong "it's safe" verdict is also a liability.
- **#6:** The applicant-tracking market is crowded.
- **#7:** Funded companies such as Loti, Ceartas and Rulta already cover it, and it needs face recognition.

---

## Winner: "AI Fact Watch". Find and fix what AI says wrong about a local business

### The need, with evidence
Google AI Overviews, ChatGPT and Gemini now answer "is X open / what are X's deals / is X legit" before people visit a business's own site. When they get it wrong, the business loses customers or staff get yelled at, and owners have no clear way to get it fixed.

- **Stefanina's, Wentzville, MO.** AI Overviews invented deals such as a second pizza for $4. Customers were "yelling at employees." Owner: *"As a small business, we can't honor a Google AI special."* The problem was reported in Aug 2025 ([29news](https://www.29news.com/2025/08/20/restaurant-battles-fake-deals-offered-by-google-ai-its-coming-back-us/), [CO/AI 2025-08-25](https://getcoai.com/news/montana-restaurant-begs-customers-to-stop-using-google-ai-for-specials/)) and was still in the news in Jan 2026 ([WLOX 2026-01-30](https://www.wlox.com/2026/01/30/restaurant-asks-customers-verify-information-after-ai-generates-fake-deals/)).
- **Viridian Bookshop, Willoughby, OH (2026-07-23).** The AI summary said "permanently closed" and gave the wrong address, and sales dropped. The owner reported it repeatedly, filled out Google's complaint form and chatted with Google's bot, and the result was still wrong. *"They don't make it easy to get help."* ([Spectrum News](https://spectrumnews1.com/oh/cincinnati/news/2026/07/23/bookshop-ai-battle), [Cleveland Mag](https://clevelandmagazine.com/articles/willoughby-bookstore-confronts-google-ai-error-claiming-it-was-permanently-closed/))
- **Anna Mae's Bakery, Millbank, ON (2026).** The AI mixed it up with a same-named Illinois bakery and announced a fake "closing July 31." Customers kept asking about it ([PPC Land](https://ppc.land/google-ai-overview-forces-anna-maes-bakery-to-deny-fake-july-31-closing/), [CTV](https://www.ctvnews.ca/kitchener/article/anna-maes-bakery-and-restaurant-not-closing-despite-ai-rumours/)).
- **Wolf River Electric, MN (2025).** An AI Overview falsely said the company was being sued by the state attorney general. A $150k contract was cancelled, and the company sued Google for $110M+ ([GovTech](https://www.govtech.com/public-safety/minnesota-solar-company-sues-google-over-ai-summary), [Futurism](https://futurism.com/company-sues-google-ai-overviews.md)).
- **Wrong phone numbers in AI Overviews.** Callers who can't get through go to a competitor ([MarTech](https://martech.org/time-to-check-your-phone-numbers-in-ai-overviews)).
- **HN:** *"Is that relevant when we already have official truth sources: our websites? That information is ours"* ([2025-07-24](https://news.ycombinator.com/item?id=44669777)). *"How many people are currently trying to figure out how to intentionally get AI chat bots to send people to their site... There will be billions in it"* ([2025-07-07](https://news.ycombinator.com/item?id=44494196)).

**How many people have it.** The US has about 33M small businesses, and several million of them rely on local search: restaurants, retail, trades and clinics. Every one with a same-name twin, a recent change to hours or prices, or stale directory listings is exposed. Only the dramatic cases make the news; most owners don't know what AI says about them. That is the opening for a free check.

### Who pays and how much
- **Owner-operators.** Restaurants, bakeries, shops, salons, trades and clinics pay **$29/mo** for Watch. Comparable dashboards cost $31-149/mo: [BrightLocal from $31](https://www.brightlocal.com/local-seo-tools/local-ai-visibility), [LocalSeen $49-149](https://alternativeto.net/software/localseen/about/), [Otterly $29](https://trustmary.com/blog/best-ai-search-visibility-tools/).
- **Businesses hit right now** (closed, fake deal, false lawsuit) pay **$99 once** for an Emergency Fix. Their pain is acute and the purchase is immediate.
- **Later:** a $149/mo white-label report for small local-marketing freelancers.

### Why nobody does this well yet
1. **Existing tools measure the wrong thing.** They are visibility and share-of-voice dashboards for marketers ("are you mentioned?"), not "is what AI says about you *true*?" Only [Insites](https://insites.com/features/ai-visibility-monitoring/) scores accuracy, and it sells to agencies.
2. **Nobody does the fix.** Owners get a chart, not a corrected set of sources.
3. **Owners don't know the problem exists.** Each owner in the news learned about it from customers. Nobody offers a free, instant "what does AI say about you?" check aimed at Main Street.
4. **The official path is a thumbs-down button.** Owners need a structured, dated evidence log and an escalation pack. No product provides one.

### The product
1. **Free AI Fact Check** (lead magnet). The owner enters business name, city and website on our site. Within an hour, an agent emails a 1-page PDF showing what Google AI Overview, Gemini and a web-grounded Claude check say about these points:
   - Open or closed status
   - Hours, address and phone
   - Prices and deals
   - "Lawsuit / scam / reviews" queries
   - "Best [category] in [city]"

   Each item is marked with a red, yellow or green flag.
2. **Watch, $29/mo.** We rerun the same prompts every week on 3-4 AI engines, and email an alert the same day if a fact flips (for example "closed," a new fake deal, or a wrong phone number). The monthly report includes dated screenshots.
3. **Fix Kit** (included in Watch). Generated per business:
   - A canonical "Official facts" page: HTML with LocalBusiness and FAQ schema plus llms.txt, for the owner to paste or for us to host.
   - Ready-to-post Google Business Profile updates.
   - A list of conflicting directory listings (Yelp, Facebook, Apple Maps, Bing), with deep links and exact corrected text.
   - Pre-written Google feedback submissions.
   - A disambiguation statement when the error comes from a same-name business.
4. **Emergency Fix, $99 one-time.** Delivered within 48h: the full Fix Kit, plus a daily recheck for 30 days, plus an evidence log of timestamped captures and sources cited. The owner can use the log for a Google escalation or give it to a lawyer.
5. **What we promise.** We do not promise that Google will change its answer. We promise detection, corrected sources and documentation. This wording appears on the site.

### How the agents deliver it end to end
- **Site.** Built with Higgsfield `create_website` and `website_db`, with API keys stored in `website_secrets`. It has a form, a leads table, a customers table and a checks table, plus Stripe Payment Links that need no code.
- **Hourly "checker" agent** (a scheduled Claude Code agent):
  - Reads new leads and due checks from the database.
  - Queries Google AI Overview through the [SerpApi free tier, 250 searches/mo](https://scrapegraphai.com/blog/serpapi-pricing), the Gemini API with search grounding (free tier), and its own web search.
  - Diffs the answers against the facts on the business's own site and Google Business Profile, and scores each fact.
  - Renders the PDF and sends it from the owner's Gmail.
  - Logs the results to Drive.
- **Daily "fixer" agent.** For paid customers, it generates the Fix Kit files (HTML, schema, posts, feedback text), then emails them and saves them in the customer's Drive folder.
- **Weekly "watch" agent.** It reruns the prompts, diffs them against last week, and sends alerts. Monthly, it compiles the report.
- **Inbox agent.** It answers customer replies with a template plus Claude, and flags refunds or angry emails to the owner. Gmail labels are the queue.
- **Cost.** About $0 per customer until volume passes the free tiers. After that, the SerpApi $25 tier is paid from the first subscription. Add ChatGPT (paid API) once MRR is above $200.

### How customers find it (organic, automatable)
- **TikTok and YouTube Shorts series "AI said they were closed."** These are 30-45s retellings of *public news cases* (the cases above, plus new ones the agent finds weekly). Videos and voiceover are made with vidIQ or Higgsfield and scheduled through OpusClip, and the owner taps approve. Every video ends with a CTA: "Free check: what does AI say about YOUR business? Link in bio."
- **Data posts that name no one,** for example "We checked 25 bakeries' AI answers: 4 had wrong hours." These posts are anonymized and aggregate only.
- **Search-intent pages** written by the agent: "Google AI Overview says my business is closed: how to fix," "AI made up a deal at my restaurant," and similar. These match exactly what the owners in the news were searching for.
- **The free check is shareable.** Owners post their own red flags, and the Viridian case shows that this kind of post goes viral locally.
- **No cold email and no paid outreach.**

### What the owner sets up once (about 1-2 hours)
1. A Stripe account and two Payment Links ($29/mo, $99 one-time). Gumroad is the fallback.
2. A [SerpApi](https://serpapi.com) free account and a Google AI Studio (Gemini) API key. Paste both into Higgsfield website secrets.
3. A new TikTok and a YouTube channel, both connected to OpusClip. A Gmail label "AIFW" and a Drive folder.
4. Approve the site copy, especially the "no guarantee" wording, and the first 5 videos. After that, tap approve on each scheduled post.
5. Optional: a domain (~$12/yr) after the first sale.

### First-week plan
- **Day 1:**
  - Owner completes the setup above.
  - The agent builds and publishes the site and database, and wires the Stripe links.
- **Day 2:**
  - The agent runs the checker on 20 public example businesses to calibrate prompts and scoring. These results are used internally only and never published by name.
  - It builds the PDF template.
- **Day 3:**
  - The agent writes 3 SEO help pages.
  - It scripts and renders 5 videos, then schedules them in OpusClip for the owner to approve.
- **Day 4:**
  - The hourly checker goes live.
  - Run the owner's friends and family businesses through it as beta users and collect testimonials.
- **Day 5:**
  - Post an anonymized data post ("X of 20 had a wrong fact").
  - The agent starts a daily news scan for new "AI got my business wrong" stories, which feed new videos.
- **Days 6-7:**
  - Follow up on free checks that came back red by sending one email to people who opted in, offering the $99 Emergency Fix.
  - Target: first paid customer.

### Risks and mitigations
- **Answers vary by location and session.** Run checks with a location set to the business's city, record the date and time, and phrase findings as "observed on [date]."
- **Search scraping terms of service.** Use SerpApi and the official Gemini API rather than scraping directly. Keep volume low.
- **Defamation or naming risk in content.** Only retell published news cases with sources. Data posts stay anonymized.
- **Over-promising.** No guarantees, and offer a refund within 14 days.
- **Competition.** BrightLocal and others are adding "AI visibility." Our edge is accuracy and fixes for owner-operators, plus the free instant check and the emergency offer. Move fast on content.
- **Gmail volume and deliverability.** Send only to people who opted in. Cap volume. Move to a transactional sender after about 50 customers.
- **API costs if the free check goes viral.** Rate-limit free checks per day and queue the overflow.
