# Scout 03: Round 2, self-spreading products (2026-10-15)

**Brief.** Find a product that is new, that distributes itself, and that runs with zero human steps after setup. Round 1's winner (AI Fact Watch) and its candidates are not repeated here.

**Method.** Web and news search, Hacker News comments through the Algolia API, and vendor and policy pages. Reddit blocks the crawler. I could not browse the logged-in ChatGPT app directory, so "nobody offers X there" means **no evidence found**, not proven absence.

**Scoring.** Each column is scored 1-5, and 5 is best.
- **D:** demand.
- **G:** gap, meaning how weak the existing offers are.
- **S:** self-spread, meaning a built-in loop or marketplace.
- **A:** how much our agents can run it end to end.
- **Sp:** speed to first dollar.
- **R:** legal and platform risk, where 5 means low risk.

## 1. Candidates (18)

| # | Idea | D | G | S | A | Sp | R | Tot | One-line verdict |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Print-from-chat book.** An app inside ChatGPT and Claude that turns a story, recipes or memories you made in chat into a real hardcover | 4 | 4 | 4 | 4 | 3 | 3 | **22** | Distribution comes from new app directories with few apps. Print by API, no humans. **Winner.** |
| 2 | AI-animated photo invitations (save-the-dates, kids' parties) on Etsy plus own site | 3 | 3 | 4 | 3 | 4 | 3 | 20 | Each video reaches 50-200 guests. But Etsy prices are ~$10 and its API has no messaging. |
| 3 | Disclosure kit for California AB 723 (AI-altered listing photos) | 3 | 3 | 3 | 4 | 3 | 3 | 19 | A real new law with poor compliance. B2B, and MLS vendors are moving in. |
| 4 | Kids' drawing turned into an animated or "realistic" keepsake | 3 | 2 | 4 | 4 | 3 | 3 | 19 | Very shareable, but ChatGPT does it free and apps exist (Yumero, KidsAI, Doodle Dreams). Fold it into #1. |
| 5 | Group AI video card (friends add messages) | 3 | 1 | 5 | 4 | 3 | 3 | 19 | Perfect loop, but Tribute and VidDay own it. |
| 6 | Custom AI songs on Etsy | 4 | 1 | 3 | 4 | 4 | 2 | 18 | Proven demand, but a Suno-fueled race to the bottom. |
| 7 | "Is your Etsy shop visible in ChatGPT?" checker | 2 | 3 | 2 | 4 | 3 | 4 | 18 | The Etsy app in ChatGPT is still beta (2026-05-05), and Instant Checkout died in March. Too early. |
| 8 | Share card from Anthropic Economic Index data: "how AI is used on your job's tasks" | 3 | 2 | 4 | 5 | 2 | 2 | 18 | The data explicitly supports no inference about job risk, so the viral framing would mislead. Rejected. |
| 9 | "AI Wrapped" from ChatGPT or Claude exports | 3 | 1 | 5 | 4 | 2 | 3 | 18 | Viral but unmonetizable. ChatGPT shipped its own year-in-review. |
| 10 | Family scam "safe word" kit | 3 | 2 | 3 | 5 | 1 | 4 | 18 | Good deed, no revenue. Norton and Bitdefender are free (round 1). |
| 11 | Paid packs of Claude Skills or agent skills | 2 | 2 | 3 | 5 | 2 | 4 | 18 | Directories are free and copying is trivial. |
| 12 | "What does AI say about me?" self-check for people | 2 | 2 | 4 | 4 | 3 | 2 | 17 | Ordinary people get "no info" (a boring card). Nuicho, Stork and LLM Pulse exist. Abuse risk with other people's names. |
| 13 | EU AI Act Art. 50 chatbot-disclosure generator plus badge | 2 | 2 | 3 | 5 | 2 | 3 | 17 | The duty mostly sits with chatbot vendors, so small and medium businesses won't pay. |
| 14 | Photo to 3D-printed figurine (you or your pet) | 3 | 2 | 5 | 2 | 2 | 2 | 16 | Huge share loop, but print quality needs a human QC step. Didiga and digxipop exist. |
| 15 | Making small businesses "agent-ready" (booking, llms.txt, MCP) | 2 | 1 | 2 | 4 | 2 | 4 | 15 | Google AI Mode books through Booksy, OpenTable, Resy and Vagaro, so the platforms solve it, not us. |
| 16 | Programmatic free-tool pages for mass questions | 3 | 1 | 1 | 5 | 1 | 4 | 15 | AI Overviews eat the clicks, and Google penalizes scaled content. Dead channel in 2026. |
| 17 | AI-animated memorial tribute videos | 3 | 2 | 2 | 3 | 3 | 1 | 14 | Grief plus "deadbot" backlash, and errors are unforgivable. |
| 18 | "Human-made" certification badge for artists | 3 | 1 | 4 | 2 | 2 | 2 | 14 | Verification needs humans. "Not By AI" and the Authors Guild already do it. |

**Two hypotheses tested and rejected.**
- **Agent-ready small businesses.** Agentic booking already runs through booking platforms: [Booksy + Google AI Mode](https://biz.booksy.com/blog/booksy-google-ai-mode-integration) and [Tom's Guide](https://www.tomsguide.com/ai/googles-ai-mode-now-books-your-event-tickets-and-beauty-appointments-for-you). Agentic shopping also stalled: OpenAI ended Instant Checkout in March 2026 after only "about a dozen" Shopify merchants integrated ([Forrester](https://www.forrester.com/blogs/what-it-means-that-the-leader-in-agentic-commerce-just-pulled-back), [Shopifreaks](https://www.shopifreaks.com/openai-pivots-from-instant-checkout-to-an-app-based-shopping-model-inside-chatgpt/)).
- **"What AI says about you."** Real cases exist ([Holmen/noyb](https://www.silicon.co.uk/e-regulation/surveillance/norway-chatgpt-complaint-605071)). However, I found no evidence that recruiters look people up in AI, and tools already exist ([Nuicho](https://www.producthunt.com/posts/nuicho-ai-reputation-checker), [LLM Pulse](https://llmpulse.ai/blog/best-ai-reputation-tools/)).

---

## 2. Deep dive #1: Print-from-chat book (working name "Bound"; check the trademark, and avoid "Chatbooks", which is taken)

**Need.** People now create keepsake content inside chatbots and have no way to make it physical:
- Personalized bedtime stories.
- Easy readers starring the child.
- Grandma's recipes.
- Memoir interviews and trip journals.

**Evidence.**
- **HN, 2026-04-21** ([item](https://news.ycombinator.com/item?id=47855520)). A parent had an LLM write a level-matched reader for a 4-year-old and turned it into coloring pages. *"We printed it off… and we stapled it into her own book."* That is the exact job, done by hand.
- **HN, 2026-02-04** ([item](https://news.ycombinator.com/item?id=46893648)). A builder says the family notebook compiled into a printed book is *"the most valuable thing in our house."*
- **Lurie Children's study** ([Boston Globe, 2026-06-12](https://bostonglobe.com/2026/06/12/lifestyle/ai-in-parenting)). More than 80% of US parents have used AI for parenting tasks, and 43% do so weekly.
- **Kaspersky survey, Nov 2025** ([says.com](https://says.com/my/tech/ai-bedtime-stories)). Nearly half of respondents expect AI bedtime stories to become normal.
- **Viral "doodle to real" trend.** Parents already run their kids' art through ChatGPT ([Tom's Guide](https://www.tomsguide.com/ai/i-turned-my-kids-art-into-lifelike-images-using-chatgpt-heres-how-you-can-too)).

**Who sells it and why they fall short.**
- **Standalone AI storybook sites** ([StoryBee](https://storybee.app/book-creation-printing), LuluStories, Wonderbly). They make you start over in their own editor, and they don't use what you already wrote in chat.
- **Printify's ChatGPT app** ([tracker](https://www.getdrio.com/app-tracker/printify)). It proves physical commerce works inside ChatGPT, but it sells mugs and shirts, not books.
- **No book apps found.** I found no ChatGPT or Claude app from Lulu, Blurb, Mixbook, Shutterfly or Chatbooks. The one storybook GPT I found ("Sparkle") is listed as removed or inactive ([whatplugin](https://whatplugin.ai/gpts/sparkle-the-storybook-maker)).
- **Opening.** The app directories are about 10 months old (opened 2025-12-18; [CMOtech](https://cmotech.news/story/openai-turns-chatgpt-into-platform-with-app-directory)). Discovery runs largely on name search and categories ([sista.ai](https://blog.sista.ai/2026/03/gpt-app-store-guide-how-to-win.html)), and the shelf is thin.

**How it spreads (three loops, none needing outreach).**
1. **Marketplace.** Listings in the ChatGPT app directory (800M weekly users) and in Claude's connector directory. One MCP App serves both ([HN 2026-09-04](https://news.ycombinator.com/item?id=49564115)). An app name built on search intent, e.g. "Print as Book", catches people searching "print", "book" or "storybook" in-chat.
2. **The object.** A hardcover gets shown to grandparents, teachers and playdate parents. A tasteful colophon on the last page reads "Made with Bound, turn any chat into a book: [url]". Gifts multiply: one story, plus copies for both sets of grandparents.
3. **Shareable preview.** Before buying, the user gets a free flip-through web preview link (cover plus pages) that they can send to family. The link page has a "make your own" button.

**Business rules (OpenAI policy, [submission guidelines](https://developers.openai.com/apps-sdk/app-submission-guidelines)).**
- Apps may sell **physical goods only**.
- Checkout must be **external**, on our own domain. A Stripe Checkout link fits that rule.
- Apps may not "explicitly target children under 13." We therefore market to **adults**: parents, grandparents, family historians. Kids are the readers, not the users.

**How the product works with zero humans.**
1. **In chat**, the user says "make this into a book." The app tool receives the title, the text split into pages, a style choice and the dedication page. The app returns a cover mock and a price, then a Stripe link to pay $39 for a hardcover or $24 for a softcover, plus shipping.
2. **Hourly scheduled Claude agent:**
   - Reads paid orders from the database.
   - Generates 8-16 illustrations in one consistent style (Higgsfield `generate_image_batch`, then `upscale_image` to 300 dpi).
   - Lays out the interior and cover PDFs to Lulu specs with a code renderer.
   - Emails a proof link.
3. **Customer approval.** The customer clicks Approve, or gets one free redo with a note. The agent then submits the job to the [Lulu Print API](https://www.lulu.com/sell/sell-on-your-site/print-api). That API has no fees beyond print, shipping and fulfillment, no minimum run, and webhooks for shipping status.
4. **Tracking.** The agent forwards tracking emails. An inbox agent handles "where's my book" messages from Lulu's webhooks and flags refunds to the owner.

**Unit economics (estimate; verify with Lulu's calculator on Day 1).**
- Color hardcover print costs roughly $12-20 per unit. Images cost about $1-2.
- At $39 plus shipping, gross margin is about $15-25 per book.
- Q4 matters: it is the gift season, and Lulu's holiday print cutoffs fall in early December.

**Blunt weaknesses.**
- **App review is a gate.** OpenAI can reject the app or take weeks. Mitigation: the website and the Claude custom-connector URL work from Day 4 regardless.
- **Directory traffic is unproven.** I found no per-app install data. Loop 1 may be small, which would leave loops 2 and 3 to carry it.
- **Character IP.** Users *will* ask for PAW Patrol, Disney or Pokémon (see the HN parent above). We must auto-refuse trademarked characters and named real celebrities before anything is printed. That needs a hard filter plus a terms-of-service clause.
- **Children's-product rules.** CPSIA tracking labels and lead rules: ordinary paper books are reportedly exempt from lead testing, but confirm before launch. COPPA applies only if a child is the user, so the account holder must be an adult. Keep data minimal and delete each order's files 90 days after delivery.
- **Print defects** (misprints, damage) depend on Lulu's reprint policy. The agent can file reprints, but some cases will hit the owner's inbox.
- **Image consistency** across 12 pages is the main quality risk. Use a single fixed style per book with character reference images, and give the customer one redo.
- **Copycat risk.** Lulu or Mixbook could ship their own app. Our edge is speed plus the name and listing; it is not a moat.

## 3. Deep dive #2: AI-animated photo invitations (Etsy plus own site)

- **Demand.** The Etsy keywords "video wedding invite" and "wedding video invitation" have Jan-2026 data showing listings at a **$10-11 median**, and the terms are rated easy to rank for ([rankhero](https://www.rankhero.com/keywords/video-wedding-invite)). Today's sellers offer templates ([AnimatedInvitesStore](https://www.etsy.com/shop/AnimatedInvitesStore)). Animating the couple's real photo is new, and Higgsfield can do it.
- **Loop.** The strongest of all 18 ideas: every order is texted to 50-200 guests, and an optional end card reads "Made by X". Etsy search supplies demand with no outreach.
- **Weaknesses:**
  - The price anchor is ~$10. Our cost is ~$1-3 per video plus re-rolls.
  - Faces warp, and couples are unforgiving, so expect revision demands.
  - The Etsy API v3 has no messaging, so the photo hand-off must go through a link in the delivered PDF to our upload page (the standard Canva-template pattern).
  - Etsy requires AI disclosure ([TechCrunch](https://techcrunch.com/2024/07/09/etsy-new-seller-policy-2024-generative-ai)).
  - The wedding peak is Jan-Mar, though kids' party invites are year-round.
- **Verdict.** A good **second product** to run on the same pipeline later. Not the lead: the margin is thin, and the human-like revision loop is real.

## 4. Deep dive #3: AB 723 altered-listing-photo disclosure pages

- **The law.** California AB 723, in force since 2026-01-01, requires licensees to disclose digitally altered listing images *and* link to the unaltered original via link, URL or QR code ([Inman 2026-01-23](https://www.inman.com/2026/01/23/what-you-should-know-about-californias-new-listing-photo-law/), [SDAR best practice](https://www.sdar.com/news/ab-723-best-practice.html)).
- **Compliance is poor.** A study of about 40,000 photos found 10.8% altered and **over 90% of those undisclosed** ([HousingWire 2026-06-24](https://www.housingwire.com/articles/most-ai-altered-listings-go-undisclosed-california-law-bans-it/)). The blocker is workflow: originals never reach the agent.
- **Product.** The agent uploads before/after pairs. We stamp a compliant label on the edited image and host a permanent proof page with a QR code. Free with our branding; $9 per listing or $19/mo unbranded.
- **Loop.** Proof pages are seen by buyers and other agents. A modest loop.
- **Weaknesses:**
  - Only one state found so far.
  - Coraly already does this at the MLS level with San Diego MLS, and staging vendors (Styldod, PropMedia) bundle it.
  - Buyers are B2B and price-sensitive.
  - We must avoid giving anything that reads as legal advice.
- **Verdict.** Real but narrow, and an incumbent is wiring it in upstream. Pass unless more states copy the law.

---

## 5. Recommendation: build "Bound", a print-from-chat book app (ChatGPT + Claude + web)

**Why this one.**
- **New distribution.** It is the only idea that combines a brand-new marketplace with a thin shelf (the 2025-12 directories) with a physical object that advertises itself, in the Q4 gift window.
- **Zero-human fulfillment by API.** Stripe, our hourly agent and Lulu, with the customer approving their own proof.
- **No dependence on content or outreach.**

**Biggest bet.** App review and directory traffic. The web plus Claude-connector path hedges it from Day 4.

### 7-day build and launch plan
- **Day 1 (owner setup + agent).**
  - Owner completes the setup list below.
  - The agent prices 3 formats in Lulu's calculator and fixes prices.
  - The agent checks the ChatGPT directory for "book" or "print" apps (owner logged in) and picks the final name.
- **Day 2.**
  - Build the MCP App server: the `make_book` and `get_quote` tools, an inline cover-preview widget, and Stripe Checkout redirect.
  - Write the IP/celebrity filter.
  - Deploy to the owner's Cloudflare or Vercel account from GitHub.
- **Day 3.**
  - Write the PDF layout engine (interior + cover to Lulu specs) and the illustration pipeline (Higgsfield batch + upscale).
  - Order **2 physical test books** at our own cost (~$40) to check print quality.
  - Submit the ChatGPT app for review and the Claude directory listing.
- **Day 4.**
  - Launch the website with a paste-or-upload-your-chat form, a free flip-through preview page and a share button.
  - Turn on the hourly order agent and proof-approval emails.
  - Publish the Claude custom-connector URL with instructions.
- **Day 5.**
  - Write 3 intent pages: "print ChatGPT story as a book", "turn bedtime stories into a hardcover", "make a family recipe book from chat".
  - Make 3 short demo videos with Higgsfield (chat, then book flip-through) and schedule them via OpusClip for owner approval.
- **Day 6.**
  - Test books arrive (or ETA). Fix layout issues.
  - Run end-to-end tests: refund, reprint, redo.
- **Day 7.**
  - Open sales with "order by Dec X for Christmas" on every page.
  - Target the first paid order from the web/Claude path. ChatGPT directory sales come after approval.

### Owner's one-time setup (about 2 hours)
1. **Stripe account.** Turn on Checkout and shipping-address collection, and enable Stripe Tax.
2. **Lulu account.** Create Print API sandbox and production keys, and add a payment card for print charges.
3. **OpenAI Platform.** Developer verification for app submission, plus a support email.
4. **Claude.** Submit to the connectors directory, using the form or account that Anthropic requires.
5. **Hosting.** A Cloudflare (Workers + R2) or Vercel account linked to GitHub. Higgsfield hosting is fine for the website, but it is unproven as an MCP endpoint.
6. **Domain** (~$12) plus a Gmail label "BOUND" and a Drive folder for proofs.
7. **Sign off** on the terms of service (no trademarked characters or real celebrities; adult purchasers; 90-day data deletion), the refund and reprint policy, and the colophon wording.
8. **Optional.** A TikTok account connected to OpusClip, approving each post with one tap.

**Kill criteria by Day 21.**
- Fewer than 5 paid books, or ChatGPT rejection with no Claude/web traction: pivot the same pipeline to #2 (animated invitations) for the Jan-Mar wedding season.
- A defect rate above 10%: stop and change printer.
