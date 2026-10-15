# 01 — Niche research: "my AI agent ecosystem" (TikTok / Shorts / Reels)

Researched 2026-10-15. Sources: TikTok page JSON (curl), vidIQ outlier search (IG + TikTok, last 30-150 days), vidIQ YouTube search, web. vidIQ spend: ~25 credits.
"Self-reported" means a creator's own marketing claim that nobody has independently verified.

## 1. @trevsagents (model account)

| Metric | Value | Source |
|---|---|---|
| Display name / bio | "t's agents" / "GUIDE TO MAKE YOUR OWN ECOSYSTEM👇" | TikTok profile JSON |
| Followers / following | **8,292** / 22 | same |
| Likes / videos | **48.3K** / **81** (~600 likes per video on average) | same |
| Account created | 2024-07-29 (createTime 1722236221). The account was probably renamed when it pivoted. | same |
| Link in bio | trevsagents.com | same |
| Example video 7696963130223643934 | Posted 2026-10-15, 167 s long, 476 plays, 21 likes, 12 saves at time of check. Caption: "Replying to @neuromancer42 these are my best performing ai agents. COMMENT OR DM ME IF U WANT TO KNOW HOW #openclaw #claudecode #hermesagent #aiassistant #aiecosystem" | video JSON |

**Offer** ([trevsagents.com](https://trevsagents.com/)):
- **Free tier:** a Discord server ("open to all"), with teardowns and agent setups.
- **Paid tier:** "Inner Circle" at **$49/mo**, cancel anytime, checked out through **Gumroad** (trevsagents.gumroad.com). It includes:
  - an "Agent Builder" installer;
  - a **14-agent library**, with new agents weekly;
  - a mission-control dashboard;
  - a "zero to first dollar" path;
  - 1-on-1 access to Trev.
- **Social proof (self-reported):** "2,000+ builders". The testimonials are small and believable ("45 videos, 4K views, 25 subs"). One says "Best $30 I've ever spent", which suggests an earlier $29-30 price.
- **Income claims:** none, and there is no disclaimer either.

**Recurring patterns:**
- Comment-reply videos ("Replying to @…").
- A POV phone filming a monitor, never a face.
- Long tours (~2-3 min) that click through each building to its agent's dashboard.
- Hashtags: #openclaw #claudecode #hermesagent #aiecosystem.
- The CTA is engagement-bait: "COMMENT OR DM ME".

**Gaps:**
- Top videos and per-video views could not be listed. TikTok's item list needs a signed API call; SocialBlade and Urlebird returned 403; vidIQ has not indexed the account.
- Cadence (inferred): 81 posts, and the current pivot is recent, so likely about 1 post a day.
- Next step: open the profile on a phone and sort by Popular.

## 2. Comparable creators (short-form, AI agents / Claude Code / OpenClaw + money)

| Handle (platform) | Followers | Best recent video (views, outlier×) | Hook / format | Offer + price | Faceless? |
|---|---|---|---|---|---|
| @lorens.ghiraldo (IG) | 23.3K | "AI Agent Ecosystem Tour 2 — Part 1": **2.3M** (329×) | POV pointer stick on a neon sci-fi dashboard. Each segment: agent role → live simulation → revenue | Affiliate link to Whop "AI Agent Academy" (@androoagi, 3,561 joined, price hidden) | Yes |
| Steven Shoaf (YT Shorts) | 9.7K subs | "I added Jarvis to my Mission Control dashboard": **102.6K** (10.8×), 376 comments | Dashboard demo, #openclaw #agents | Free Discord (discord.gg/agentsinstall). Paid Whop community **$97/mo** "founder pricing" ([shoaf.dev](https://www.shoaf.dev/)) | Mostly screen |
| jakebeau (YT Shorts) | 5.35K | "Best AI agent setup? Obsidian+Claude, OpenClaw, Hermes…": **92.8K** (55.5×) | Comparison / opinion | n/a | Screen |
| @haejuicyy (TikTok) | 5.8K | "POV: Jarvis is building you a $30k MRR app": **622K** (120×) | Jarvis fantasy + glowing setup | Comment-for-guide | Face + screen |
| @lasthumannode (IG) | 15.3K | "I told Claude to make $1,000 in a week": **435K** (110×) | Challenge timelapse of dashboards + "Gmail Connected" | Guide | **Yes** |
| @mplentg (TikTok) | 1.8K | "I Let AI Run My Side Hustle (It Made $3,000)": **634K** (2,959×) | Tweet screenshot + kinetic captions | n/a | **Yes** |
| @josh.castell7 (TikTok) | 4.9K | "Yesterday Claude took a trade": **79.7K** (31×) | Trading-bot daily update (green screen) | n/a | Face |
| @techwithcole3 (TikTok) | 409 | Claude + Higgsfield → KDP coloring books: **638K** (990×) | Split-screen tutorial | Higgsfield partner (paid) | Partial |
| @lauv.scale (TikTok) | 1.3K | "Day 2 of trying random high-value skills" (AI builds a local-business site): **136K** (138×) | "Day N" series | Manus sponsor + comment-for-guide | Face |
| @waymaker_rono (TikTok) | 3.4K | "Claude + Shopify = 10k/month (explained in caveman)": **584K** (1,829×) | "Caveman" explainer | Shopify partner | Face |
| Nate Herk (YT, long + Shorts) | 1.07M subs | "How to Build Claude Agent Teams…": 378K | Tutorials | Free Skool (300K+ members). AIS+ **$99/mo or $839/yr** (~3,500 paid) ([review](https://aifunnelinsider.com/ai-automation-society-plus-skool-review/)). Hostinger VPS code | No |
| Simon Scrapes (Skool) | n/a | n/a | Claude Code + n8n | Agentic Academy **$37/mo**, rising to $87 ([review](https://aifunnelinsider.com/agentic-academy-review-2026/)) | No |

**Takeaways:**
- Outliers come from **tiny accounts**: 409-23K followers reaching 100K-2.3M views. The niche is open to new accounts.
- The direct format matches (lorens, Shoaf, jakebeau, trevsagents) are all **dashboard tours**. The "Mission Control" and "Jarvis" framing is the current visual trend.
- The pixel-art office layer is also trending: the open-source "Pixel Agents" VS Code extension ([github](https://github.com/pixel-agents-hq/pixel-agents)), and OpenClaw "workspace monitor" builds at 55× outlier.

## 3. Formats that pull views (evidence)

| Rank | Format | Evidence | Fit for us |
|---|---|---|---|
| 1 | **Ecosystem / Mission Control tour** (POV, one agent per beat) | lorens 2.3M (329×); Shoaf 102K; trevsagents' core format | We have 6 real agents. Our pixel town is the visual hook. |
| 2 | **"I told AI to do X" challenge / timelapse** | @lasthumannode 435K; @mplentg 634K | TARS week-long run; booking-site agent "find 10 shops with no website" |
| 3 | **Single-niche money workflow** ("Claude + KDP", "Claude + Shopify") | techwithcole3 638K (KDP!); waymaker 584K; jeremysuseskrea 56K | Hollow Pine Puzzles is a KDP proof point. Never invent sales. |
| 4 | **"Day N" series** | lauv.scale 136K, "Day 2" + local-business site | "Day N of my AI agents running 6 side projects" |
| 5 | **Comment-reply deep dive** | trevsagents uses it constantly. Replies inherit the original video's context. | Answer "how does the trading agent decide?" |
| 6 | **Trading-bot daily update** | josh.castell7 79.7K | TARS journal readout. High compliance risk (see §4). |
| 7 | Comparison / opinion ("best agent setup?") | jakebeau 92.8K (55×) | "Claude Code scheduled tasks vs OpenClaw" |

**Hook formulas seen repeatedly:**
- "POV: [AI] just [result]"
- "I told Claude to [goal] in [time]"
- "[Tool] + [platform] = [outcome]"
- "9 months of using Claude and NOW I find this"
- "Posting this before he deletes it" / "DELETING IN 24 HOURS"
- "explained like cavemen"
- "Comment 'CLAUDE' for the free guide"

**Avoid:**
- The "men's lust = printing" (Eromify) and "Male version of OF" hooks: an adult-adjacent trend, high outlier counts, but a brand-safety risk.
- The fake-urgency "deleting in 24h" hook.

## 4. Compliance (what not to say)

**FTC**
- **"Results not typical" is not a safe harbor.** It was removed in the 2009 Endorsement Guides revision. If we show an atypical result, we must state what people **generally achieve** ([FTC FAQ](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking)).
- **Earnings claims need substantiation**, and implied claims ("printing", "quit your job", a lifestyle b-roll) count as claims too.
  - The FTC's 2021 **Notice of Penalty Offenses on Money-Making Opportunities** exposes sellers of courses, communities and templates to civil penalties of roughly $50K+ per violation.
  - A 2025 proposal would extend the Business Opportunity Rule to "business coaching". Its status is stalled under the current FTC ([Kelley Drye](https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/ftc-puts-pedal-to-the-metal-to-release-proposed-rule-on-mlm-earnings-claims-changes-to-business-opportunity-rule-but-republican-commissioners-pump-the-brakes-in-potential-foreshadowing.md)).
- **Enforcement precedent in this exact niche:** Operation AI Comply (Sept 2024) targeted **Ascend Ecom** (≥$25M, "AI-powered passive income stores"), Ecommerce Empire Builders and FBA Machine ([American Banker](https://americanbanker.com/news/ftc-takes-action-against-five-companies-using-ai-in-fraudulent-ways)).
- **Affiliate and sponsor disclosure:**
  - It must appear **in the video**: on screen, and spoken when the endorsement is spoken. The TikTok caption alone is "very unlikely to be clear and conspicuous".
  - Use "Paid link" / "I earn a commission". "Affiliate link" alone is insufficient.
  - Put the disclosure at the **start** ([FTC FAQ](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking)).

**TikTok**
- Frauds & Scams policy: no Ponzi/MLM/pyramid content, and no "investment schemes with promise of high returns" ([BuzzFeed on the policy](https://www.buzzfeednews.com/article/tanyachen/tiktok-is-banning-mlms-and-other-money-scams)).
- Get-rich-quick framing risks takedowns or For You ineligibility. Always use the **commercial content disclosure toggle** when promoting our own paid tier or an affiliate.
- **Bio link:** personal accounts need **1,000 followers**; business accounts can add one at any follower count but lose the full music library ([Stan guide](https://stan.store/blog/tiktok-link-bio-requirements-2026-guide/)). Before 1K, use plain text plus "comment for link" auto-DMs.
- **TARS (trading):**
  - Never give buy/sell calls, promise returns, or show P&L as a hook.
  - Frame it as "how my agent journals and follows rules", with "not financial advice" on screen.
  - Personalized advice may trigger SEC/FINRA investment-adviser issues.

**Never say:**
- "passive income", "printing", "$X/month", "quit your job", "guaranteed", "while I sleep it makes money", "easy money"
- any number we can't document with screenshots and dates

**Do say:** "here's what it actually produced this week, including the zeros".
Real numbers with context (cost, time, failures) are compliant and differentiate us. Add "Your results will vary; most people earn nothing at first."

## 5. Monetization stack (no capital)

| Layer | Option | Cost / fee | Notes |
|---|---|---|---|
| Free community | **Discord** | $0 | trevsagents and Shoaf use it. Best for faceless and dev audiences. |
| | Skool free group | $9/mo Hobby | 10% transaction fee on paid tiers. Pro is $99/mo with 2.9% ([pricing](https://aifunnelinsider.com/skool-pricing-2026/)). |
| Paid tier | **Whop** | $0/mo, ~2.7% + $0.30 | 30% fee on Whop Discover sales. Native Discord role gating ([compare](https://www.builtbyfoundry.io/blog/whop-vs-skool-2026-7-costs-compared)). |
| | Gumroad (trevsagents uses it) | 10% + $0.50, 30% via Discover | Easiest. Costs more at scale ([fees](https://roo.beehiiv.com/p/gumroad-fees-2026)). |
| Templates storefront | Lemon Squeezy (5% + $0.50, merchant of record) / Gumroad / Whop | — | Sells one-time agent template packs |
| | Stan Store | $29/mo | Only worth it once there are sales |
| Affiliates | **Hostinger VPS** | **40%** commission, 30-day cookie, $100 min payout ([Hostinger](https://www.hostinger.com/tutorials/affiliate-marketing-programs/)) | Nate Herk pushes Hostinger "claude-code-hosting" VPS. Fits the "Claude Code on a VPS" story. |
| | **ElevenLabs** | **22% for 12 months**, 90-day cookie, $5 min, paid via PartnerStack ([ElevenLabs](https://elevenlabs.io/affiliate)) | Natural fit: voiceovers for Dark Facts / Oh Meatball |
| | Higgsfield / Manus / Polsia partner programs | Paid per post (seen as #higgsfieldpartner, #manuspartner) | Inbound sponsor deals once views exist |

**Price anchors in the niche:** $37 (Simon), **$49** (Trev), $59 (Goldie), $97 (Shoaf), $99 (Nate). Founder pricing that steps up at member milestones is the standard play.

## Launch plan

**Positioning:** "Agent Town" — 6 real Claude Code scheduled-task agents, shown with real outputs including failures. Faceless POV of the pixel town, with each building opening that agent's dashboard. The point of difference vs Trev: radical honesty (receipts, costs, misses) and specific, verifiable agents.

**First 10 videos (ranked by expected pull):**

| # | Hook (first 2 s, on-screen text + VO) | What's on screen |
|---|---|---|
| 1 | "I have 6 AI agents working for me. Here's what each one did this week." | POV phone → pixel town. Tap each building → dashboard → one real output per agent. 60-75 s. |
| 2 | "My AI found 12 barbers with no website and built one for each." | Booking-site agent: map/search list → generated site scroll → drafted DM (blur names). Show it was not sent until reviewed. |
| 3 | "My AI publishes a puzzle book every week. Here's the whole pipeline." | Hollow Pine Puzzles building → puzzle generation → interior PDF flip → KDP draft screen. Real royalties only, even if $0. |
| 4 | "I gave Claude a trading desk with rules it can't break." | TARS building → hourly check log → journal entry → rules file. "Not financial advice" on screen. No P&L brag. |
| 5 | "Replying to @…: how do the agents run without me?" | Claude Code scheduled-task list / cron → a run log ticking. Comment-reply format. |
| 6 | "My AI runs a cat soap opera. Episode 14 just dropped." | Oh Meatball studio building → script → generated scene → posted clip. Funny, shareable. |
| 7 | "Day 1 of letting 6 AI agents run my side projects for 30 days." | Town at dawn → task queue → end-of-day tally card (real numbers). The series engine. |
| 8 | "I asked my AI how visible dentists are in ChatGPT. Most are invisible." | Dentist audit building → audit report → score card. B2B credibility. |
| 9 | "This agent makes faceless TikToks while I sleep. Here's its actual view count." | Dark Facts building → script → render → analytics, real numbers including flops. |
| 10 | "What my AI agents cost me per month (and what broke)." | Cost dashboard: API, VPS, tools. A failure reel. Trust builder that sets up the offer. |

**Cadence:**
- **Weeks 1-4:** 2 posts/day on TikTok (cross-post to Shorts and Reels), 1 tour + 1 single-agent deep dive. Reply to the top comments with video (comment-reply format) daily.
- **Weeks 5+:** 1-2/day.
- Recycle any video with 3× median views into Part 2 within 48 h.
- Every post gets a CTA: "Comment TOWN and I'll send the free Discord".

**Offer ladder:**
1. **Free:** Discord "Agent Town". Weekly teardown, #show-your-agents channel, free starter skill (1 agent template).
2. **$9-19 one-time:** single agent template packs: booking-site builder, KDP puzzle pipeline, faceless-video generator. Sold on Lemon Squeezy or Whop.
3. **$29/mo founder → $49/mo:** "Town Hall" paid tier on Whop with Discord role gating. All templates, VPS + Claude Code setup guide, monthly build call. Price steps up at 100 and 300 members.
4. **Affiliates throughout:** Hostinger VPS (40%), ElevenLabs (22%/12 mo). Disclosed on screen and spoken.
5. **Later:** a $149-299 done-with-you setup, and a B2B line from the dentist audit / booking-site agents. These are services, not "income".

**Guardrails:** no income claims, real dated receipts only, "results vary" on any money talk, commercial-content toggle on, no trading advice.
