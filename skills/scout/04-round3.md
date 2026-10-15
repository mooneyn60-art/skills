# Scout 04: Round 3, out-of-the-box (2026-10-15)

**Brief.** Find something unusual and really good that rounds 1 and 2 did not cover. Excluded: AI Fact Watch, Bound, agent-ready businesses, "what AI says about you", Etsy printables, websites for local businesses, AI agent content.

**Method.**
- Brainstormed 30 ideas through six lenses: (a) new data, laws or features, (b) money people are owed, (c) AI-versus-human price arbitrage, (d) gifts and memories, (e) chores for tiny businesses, (f) ideas that are illegal or too risky.
- Searched the web, news, app stores and vendor pages, plus Hacker News comments since 2025 through the Algolia API. Reddit blocks the crawler.
- Killed any idea that is crowded, needs cold outreach, needs a human per order, or is deceptive.

**Scoring** (1-5, 5 is best): **D** demand, **G** gap (how weak existing offers are), **S** self-spread, **A** agent-deliverable with no human, **Sp** speed to first dollar, **R** legal/platform risk (5 = low).

## 1. The 30-idea list

| # | Lens | Idea | D | G | S | A | Sp | R | Tot | One-line verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | c,d,a | **House history book.** "The story of your house and the land under it," built from free public archives | 4 | 5 | 4 | 4 | 4 | 4 | **25** | Humans charge $350-1,250 for this and we found no AI version. **Winner.** |
| 2 | d | AI-curated printed yearbook of a group chat ("The Chat Annual") | 3 | 3 | 5 | 4 | 3 | 3 | 21 | One book gets bought by every member. Strong second SKU on the same print pipeline. |
| 3 | b,e | US "tell everyone once": certified death-notification letters by mail API | 4 | 4 | 2 | 3 | 2 | 2 | 17 | A real gap, but it opens a fraud path (closing accounts of a living person) and every error lands on a grieving family. Parked. |
| 4 | d | Map plus story of "what was on your street in 1900" as a wall print | 3 | 3 | 4 | 4 | 4 | 4 | 22 | Becomes the cheap entry tier of #1, not a separate product. |
| 5 | d | "The house you grew up in" Christmas gift for parents | 4 | 4 | 3 | 4 | 4 | 4 | 23 | The best gift angle for #1. Merged into it. |
| 6 | b | Credit-card benefit claims (trip delay, purchase and phone protection) | 3 | 3 | 2 | 2 | 2 | 3 | 15 | The cardholder must file through the issuer's portal, so we could only make a claim packet. Guides already exist. |
| 7 | b | Agent scans your inbox and claims refunds, price drops and settlements | 4 | 1 | 3 | 2 | 2 | 2 | 14 | [Serve AI (YC)](https://www.ycombinator.com/companies/serve-ai) already does it. Also needs inbox scopes and phone calls. |
| 8 | b | Class-action settlement claims filed on users' behalf | 4 | 2 | 4 | 3 | 3 | 1 | 17 | Claims are sworn by the claimant. Bulk third-party filing is the fraud pattern administrators fight. **Ruled out.** |
| 9 | b | Unclaimed-property finder for other people, paid by finder's fee | 3 | 2 | 1 | 3 | 2 | 1 | 12 | Needs cold outreach, and finder fees are regulated state by state. **Ruled out.** |
| 10 | b | EU261 or UK Delay Repay claims | 4 | 1 | 2 | 4 | 3 | 3 | 17 | AirHelp, Flightright and Delay Repay apps own it. |
| 11 | b | Paid homestead-exemption filing | 3 | 2 | 1 | 4 | 3 | 1 | 14 | Filing is free, and state AGs warn about paid "filing service" mailers. Deceptive. **Ruled out.** |
| 12 | c | Flat-fee DIY property-tax appeal packet | 4 | 1 | 2 | 4 | 3 | 4 | 18 | [AppealDesk already does $49 flat](https://www.appealdesk.com/compare/appealdesk-vs-ownwell). Ownwell takes 25-35%. |
| 13 | c | Medical-bill error and dispute letters | 5 | 1 | 2 | 4 | 3 | 3 | 18 | Crowded: [Bill Decoder, IQBill, Curai](https://www.ibtimes.co.uk/patients-use-ai-challenge-medical-bills-1825193), Counterforce. |
| 14 | c | Translating old handwritten genealogy records (Kurrent, Latin, Polish) | 3 | 1 | 2 | 5 | 3 | 4 | 18 | Free chat models already do it: *"amazing at one shot decoding hand written vital records"* ([HN 2026-09-24](https://news.ycombinator.com/item?id=49838090)). |
| 15 | e | Membership cancellation by certified mail | 3 | 1 | 2 | 5 | 4 | 4 | 19 | Pain is real ([HN 2025-10-09](https://news.ycombinator.com/item?id=45523493)), but [Mailform](https://mailform.io/lp/cancel-gym) and [Letter Pilot](https://theletterpilot.com/templates/cancel-gym-membership) exist. Thin margin on postage. |
| 16 | a | Local council and school-board meeting digests for news deserts | 3 | 1 | 4 | 4 | 2 | 2 | 16 | [Hamlet, Civic Sunlight, Locunity](https://www.cjr.org/analysis/ai-local-news-civic-sunlight-maine.php) are already there. Errors about real officials create defamation risk. |
| 17 | a | Retrieving medical records under the HIPAA right of access, by fax API | 3 | 3 | 1 | 2 | 2 | 3 | 14 | Records come back by mail to the patient, so the loop can't close without a human. |
| 18 | d | "Wrapped" stats for a group chat | 3 | 1 | 5 | 5 | 1 | 3 | 18 | Free apps such as [WhatStats, ZapZipped and The Cringe](https://apps.apple.com/app/id1481007233) already do it. No money in it. Only the print version (#2) is viable. |
| 19 | d | Life-story book of a pet | 3 | 2 | 3 | 4 | 3 | 4 | 19 | A Bound variant, not new. |
| 20 | d | Voice-cloned bedtime stories from grandparents | 3 | 2 | 3 | 4 | 3 | 1 | 16 | Consent and fraud risk with voice cloning. **Ruled out.** |
| 21 | d | 3D-printed miniature of your house | 3 | 2 | 4 | 2 | 2 | 3 | 16 | Print QC needs a human. Etsy is full of house portraits. |
| 22 | a | Satellite timelapse of your house over 40 years | 2 | 2 | 3 | 4 | 3 | 4 | 18 | Google Earth Timelapse is free. Only works as a page inside #1. |
| 23 | e | ADA/accessibility fixes for tiny web shops | 3 | 1 | 1 | 2 | 2 | 2 | 11 | Overlay vendors dominate (and accessiBe drew an FTC fine). Real fixes need theme access. |
| 24 | e | EU GPSR "responsible person" for Etsy sellers | 3 | 2 | 1 | 1 | 2 | 2 | 11 | Needs an EU legal entity. |
| 25 | e | Reminders and filing for LLC annual reports | 3 | 1 | 1 | 4 | 2 | 3 | 14 | Registered agents bundle it. Looks like the scam mailers. |
| 26 | e | Preliminary lien notices for small contractors | 3 | 1 | 1 | 4 | 2 | 3 | 14 | Levelset (Procore) owns it. |
| 27 | a | "Who died in my house" report | 3 | 1 | 3 | 4 | 4 | 2 | 17 | [DiedInHouse](https://www.cnbc.com/2013/10/23/did-someone-die-in-this-house-new-site-lets-you-search.html) exists and the angle is morbid. It does prove people pay for address history (see §2). |
| 28 | f | "Refund-as-a-service" (social-engineering retailers into refunds) | - | - | - | - | - | 0 | - | This is fraud. **Ruled out.** |
| 29 | f | Credit repair, court filings for others, tax prep for pay | - | - | - | - | - | 0 | - | Barred by CROA advance fees, unauthorized practice of law (DoNotPay was fined by the FTC in 2024), and the PTIN requirement. **Ruled out.** |
| 30 | f | Ticket bots, fake reviews, scraping people-search sites | - | - | - | - | - | 0 | - | Barred by the BOTS Act and the FTC fake-review rule (2024). **Ruled out.** |

**What the lenses showed.**
- **Money owed (lens b) does not work for us.** Every viable claim either already has a funded owner (Serve AI, AirHelp, Ownwell) or needs the claimant's own login or sworn statement.
- **The arbitrage lens (c) produced the winner,** once it was combined with gifting (d). The best fit is a job where:
  - humans still charge hundreds of dollars,
  - free public archives hold the raw material,
  - an AI Overview cannot answer the question, because the answer is unique to one address.

---

## 2. Deep dive #1: House history book (working name "Housestory"; check the trademark)

**The need.** Owners of older homes, new buyers, and adult children of the family home all want to know two things: who lived here, and what was here before. Today the job is done by hand by historical societies and researchers, and it takes weeks.

**Proof that people pay.**
- **Human researchers:**
  - [Brownstone Detectives](https://www.brownstonedetectives.com/reports/) charges $975 per NYC report and takes 6-8 weeks.
  - [Ancestry Solutions](https://ancestrysolutions.com/services/propertysearch/propertyhistories.html) charges $1,249 for a bound book.
  - [Wells-Ogunquit Historical Society](https://www.wellsogunquithistory.org/house-history-service) charges $900 for about 25 staff hours.
  - [Wauwatosa Historical Society](https://wauwatosahistoricalsociety.org/?p=4224) charges $35 and takes 2-4 weeks.
- **Gift market:** The UK gift shop [aFewHomeTruths on Not On The High Street](https://www.notonthehighstreet.com/afewhometruths/product/personalised-new-home-house-history) sells a researched house-history print for £45.
- **Mass-market curiosity about a specific address:** DiedInHouse sold $11.99 address reports at up to about a thousand a day, and roughly 30-40k in total by 2015 ([CNBC 2013](https://www.cnbc.com/2013/10/23/did-someone-die-in-this-house-new-site-lets-you-search.html), [GeekWire 2015](https://www.geekwire.com/2015/find-out-if-someone-died-in-your-house-with-this-new-website/)).
- **Libraries publish "Who lived in my house?" guides** ([Multnomah County](https://multcolib.org/es/node/10749)) because patrons keep asking.

**Market size.** About 4.06M existing homes sold in 2025 ([AP/NAR](https://www.clickondetroit.com/business/2026/01/14/2025-us-home-sales-stuck-at-30-year-low-as-mortgage-rates-prices-weighed-on-market/)); about 1 in 6 US homes predates 1950 (ACS B25034, verify Day 1); realtors spend $50-300 per closing gift ([industry blogs](https://climbtheladder.com/how-much-do-realtors-spend-on-closing-gifts/)).

**Competitors and their gaps.**
- **Humans** are slow and cost $350-1,250, and are hard to find outside big cities.
- **Hint**, the Martha Stewart startup with a $10M seed ([Fortune 2026-05-13](https://dc.fortune.com/2026/05/13/exclusive-martha-stewart-ai-startup-hint-seed-funding-slow-ventures/)), and HomeZada build a *maintenance* record (permits, warranties), not a narrative history. Hint could add this later. Our window is now.
- **No AI house-history product** turned up in our searches. That means no evidence found, not proven absence.

**Every source is free, public and reachable by program.**

| Source | What it gives | Access |
|---|---|---|
| Census Geocoder | Coordinates and census tract | Free, no key |
| BLM Township Geocoder plus GLO land-patent records | The *first private owner of the land* and the president who signed the patent | Free. Covers the 30 public-land states ([guide](https://townshipamerica.com/blog/blm-glo-records-2026-whats-new-how-to-use)) |
| LOC Sanborn fire-insurance maps | Footprint, materials and neighbors, roughly 1880s-1960s | Free, about 47 states plus DC ([LOC](https://www.infodocket.com/2017/05/25/library-of-congress-releases-digital-collection-with-nearly-25000-sanborn-fire-insurance-maps-with-more-to-come/)) |
| Chronicling America (loc.gov API) | Full-text search of the street address in old newspapers: ads, weddings, sales | No key, 20 requests/min ([LOC API](https://www.loc.gov/apis/additional-apis/chronicling-america-api/)) |
| 1950 Census | The household at the address (names, jobs, ages) | Address to enumeration district via the Morse finder, then a vision model reads the page ([NARA FAQ](https://1950census.archives.gov/howto/faq.html)) |
| USGS aerial single frames | Photos from 1937 on; "your lot in 1940" | Free, about 6.4M frames ([data.gov](https://catalog.data.gov/dataset/aerial-photo-single-frames)). Needs an EROS login |
| DPLA and LOC photos and postcards | Pictures of the neighborhood | Free API key |

**The product.**
1. **Free "Land Card," shareable.** The visitor enters an address. Within minutes they get one image with:
   - the first land patent ("Deeded 1859, signed by President Buchanan"),
   - a crop of the Sanborn map or 1940s aerial photo,
   - a count of house-specific finds, such as "3 newspaper mentions, 1950 household found."

   **This doubles as a preview before purchase,** so nobody pays for a thin book.
2. **Digital House Biography, $29.** A PDF of 20-30 pages:
   - a timeline of land, house, street and town,
   - maps and aerial photos then and now,
   - "who lived here" from the 1950 census and older newspapers,
   - the era's context: prices and events.

   Every fact carries a footnote with the source and link, and gaps are stated honestly.
3. **Hardcover, $79 plus shipping,** printed on demand by Lulu. Uses the same pipeline as Bound.
4. **Gift edition, $129.** A custom dedication page ("From your agent, Jane Doe" or "For Mom and Dad, the house we grew up in"), plus a framed-print PDF.

**How it spreads, with no outreach.**
1. **Neighborhood loop.** A Land Card posted in a Nextdoor or neighborhood Facebook group reaches people who share the same patent, Sanborn sheet and aerials. Each extra order from that street costs us less to make and is more fun for the buyer.
2. **Gifts.** Adult children give "the house you grew up in" to their parents at Christmas, and realtors give closing gifts. Every delivered book has a colophon with our URL, so it reaches more agents and more neighbors.
3. **Visual short videos.** "Your street in 1925": a real Sanborn map dissolving into today's satellite view, animated with Higgsfield and scheduled through OpusClip. Primary-source maps are novel content, not slop.
4. **Etsy listing** for "house history / new home gift". The delivered file links to our order form.
5. **Why AI search can't take the traffic.** An AI Overview cannot produce one house's 1950 household or its land patent.

**Zero-human delivery.**
- **Hourly agent.** It reads paid orders from the Higgsfield site database and runs the source pipeline above. It then writes cited prose and renders the PDF with code. Finally it emails the PDF from Gmail and saves it to Drive.
- **Hardcover orders.** The agent sends a proof link. When the customer approves, it submits the job to the Lulu API.
- **Unit economics (estimate).** API and image cost is about $1-3 per book. A hardcover costs about $15-20 to print, so margin is roughly $55 on the $79 edition and about $26 on the $29 PDF.

**Risks.**
- **Results vary by address.** Rural homes, new builds, and the 13 original states lack GLO patents. Mitigations:
  - The free preview shows what was found before the customer pays.
  - The "Land & Neighborhood" edition is honest about what it covers.
  - A refund is offered if there is no house-specific find.
- **Hallucination.** A hard rule: no claim without a source. The renderer refuses any sentence without a source ID.
- **Privacy.** Use people only from the 1950 census, which is public under the 72-year rule, and from newspapers before 1964. No post-1964 people data, no people-search sites, no "deaths" angle. Offer an opt-out.
- **Copyright.**
  - LOC Sanborn maps are listed as "no known restrictions."
  - Newspapers from before 1929 are public domain.
  - For 1929-63 newspapers, use short quotes plus a link, not full page images.
- **Copycats.** Hint, Ancestry or MyHeritage could add this. Our edge is speed, gift positioning and the neighborhood loop.

## 3. Deep dive #2: "The Chat Annual," a printed yearbook of a group chat

- **What it is.** The customer uploads a WhatsApp or Telegram export. The book contains:
  - AI-picked best moments, inside jokes and a timeline,
  - superlatives ("most likely to send a 4-minute voice note"),
  - the chat's photos.
- **Price.** $39 hardcover, and each member can order their own copy.
- **Competitors.**
  - [Zapptales](https://www.zapptales.com/en/?p=36186) prints the *raw* chat for about €25-30. It has no curation.
  - The free "Wrapped" apps only produce stats.
- **Loop.** The best of any idea: one upload leads to N buyers.
- **Weaknesses.**
  - Every member's messages are printed, so the uploader must confirm consent.
  - Explicit content needs filtering.
  - iMessage export is hard.
  - The seasonal peak is New Year's ("2026 in the chat").
- **Verdict.** A third SKU for late December on the same Lulu pipeline. Not the lead.

## 4. Deep dive #3: US "tell everyone once" death-notification letters

- **Gap.**
  - The UK has the free [Death Notification Service](https://www.which.co.uk/news/article/new-service-notifies-banks-of-a-loved-ones-death-with-a-single-click-abrpG1B3FUrn) and Tell Us Once. The US has nothing like them.
  - [Empathy](https://www.elayne.com/resources/empathy-reviews-pricing-alternatives) sells mainly through insurers and employers.
  - Executors report more than 500 hours of admin and about 20 months to settle affairs ([Empathy Cost of Dying](https://empathy.com/blog/cost-of-dying)).
- **How it would work.** The executor lists the accounts. We generate and send certified letters with a death-certificate copy through the [Lob API](https://help.lob.com/print-and-mail/building-a-mail-strategy/certified-mail-or-registered-mail), which supports certified mail and return receipts.
- **Why we pass.**
  - Anyone could use it to "close" a *living* person's accounts, and we have no reliable way to verify a death. That makes it an identity-fraud tool.
  - Many firms demand their own forms or phone calls, so a human loop creeps in.
  - The audience is grieving, so errors are unforgivable.

---

## 5. Recommendation: build Housestory, judged head-to-head

| | **Housestory** | **Bound** (round 2) | **AI Fact Watch** (round 1) |
|---|---|---|---|
| Proof people pay | **Strong.** Humans charge $35-1,250, and DiedInHouse sold tens of thousands of $12 address reports | Inferred (DIY anecdotes, parent surveys) | Good. Comparable tools sell at $29-149/mo |
| Gatekeeper | None | OpenAI app review | None |
| Self-spread | Neighborhood posts, gift colophons, map videos, Etsy | App directories (traffic unproven) plus the object itself | Weak. Relies on content and a free check |
| Safe from AI Overviews | **Yes** (unique per address) | Mostly | Partly (its SEO pages compete with AI) |
| Recurring revenue | No (one-off, gifts) | No | **Yes ($29/mo)** |
| Zero-human delivery | Yes, with variable research depth | Yes, but image consistency is a risk | Yes |
| Legal risk | Low (public records, pre-1964 only) | Medium (character IP, kids' products) | Low-medium (naming businesses) |
| Fit for Q4 2026 | **Excellent** (Christmas, "the house you grew up in") | Excellent | Neutral |

**Verdict.**
- **Housestory beats Bound.** It has harder evidence of payment, no review gate, an uncrowded and unusual angle, and the same Lulu pipeline. Bound can become a second SKU on that pipeline later.
- **It does not clearly beat AI Fact Watch on lifetime value.** AI Fact Watch is the better recurring business, but its sales cycle is slower, and its distribution leans on content we have to make.
- **Plan:** launch Housestory now to catch the gift season and get to first dollar fastest. Keep AI Fact Watch as the B2B track for Q1 2027.

### 7-day plan
- **Day 1.** Owner completes the setup below. The agent tests the source pipeline on 15 varied addresses: urban pre-1900, a 1920s suburb, a 1960s tract house, and a rural home in an original-13 state.
  It records the hit rate for each source and checks the ACS share of pre-1950 homes.
- **Day 2.**
  - Write the pipeline code: geocode, then PLSS and GLO, then Sanborn, Chronicling America, the 1950 census enumeration district and page read, aerials, and DPLA.
  - Build a store of facts with sources, so that every sentence cites a source ID.
- **Day 3.**
  - Build the PDF renderer (digital plus Lulu interior and cover specs), the Land Card image and the "no source, no sentence" check.
  - Order 2 test hardcovers.
- **Day 4.**
  - Build the Higgsfield site: address form, free Land Card, Stripe Payment Links for $29, $79 and $129, the database and the hourly order agent.
  - Write the privacy policy and the sourcing disclaimer.
- **Day 5.**
  - Make 5 "your street in 1925" videos from public-domain Sanborn maps and schedule them in OpusClip for the owner to approve.
  - Create the Etsy listing.
  - Post the owner's own Land Card in their neighborhood group.
- **Day 6.** Run 10 friends-and-family addresses end to end, collect testimonials, fix thin-result handling.
- **Day 7.** Open sales with a "Christmas delivery: order by Dec X" banner (Lulu's holiday cutoff). Target: first paid digital order.

**Kill criteria by Day 21.** Fewer than 10 paid orders, or more than 30% of previews with no house-specific find in the target markets. Either way, narrow to pre-1950 neighborhoods only, or fall back to AI Fact Watch.

### Owner's one-time setup (about 1.5 hours)
1. **Stripe:** three Payment Links, with shipping-address collection on the hardcover.
2. **Lulu Print API:** sandbox and production keys, plus a card on file. Shared with Bound if that is built later.
3. **Free accounts:** USGS EROS (EarthExplorer) login and a DPLA API key. Census Geocoder and loc.gov need no key.
4. **Higgsfield website** with the API keys stored in website secrets, plus an optional domain (~$12).
5. **Etsy seller account**, and a TikTok and YouTube channel connected to OpusClip.
6. **Gmail and Drive:** a Gmail label "HOUSE" and a Drive folder for books.
7. **Sign off** on four things:
   - the privacy rule (pre-1964 people data only, opt-out honored),
   - the "sourced facts only" promise,
   - the refund policy (refund if no house-specific find),
   - the colophon wording.
