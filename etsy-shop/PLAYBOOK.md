# DoodleDesignAndCo Team Playbook (shared by every agent)

## 🎯 #1 TEAM GOAL (set Nov 18): FIRST SALE BY SUN NOV 22
Every agent works toward this first. The plan, based on our research (beginner-seller guides: Outfy, Promptless Press, Insight Agent, ProfitTree):
1. **Sale live now.** Owner sets **25% off all listings, Nov 19 – Dec 1** (one sale covering launch week + Cyber Week). Strike-through prices plus Etsy's "on sale" surfacing.
2. **Traffic.** 3 TikToks/day (scheduled), daily Pinterest pins, and the owner shares listings in her own Facebook/Instagram stories and parent groups (promo threads only).
3. **More listings.** Add the Elf Letter Bundle this week (shop goes to 13). Aim for 20 listings by early December.
4. **Etsy Ads $3/day** on the Santa Mail Set, Coloring Book and Nice List, **only once the owner approves** the spend.
5. **Hero products to push:** Santa Mail Set ($7.99 → $5.99 on sale), Coloring Book, Nice List, Elf Letter Bundle.
6. **When the first order arrives:** the analyst reports it, and the owner sends a warm thank-you. Never ask for or incentivize reviews.

## The business
- **Etsy shop:** DoodleDesignAndCo (shop_id 69156121). It sells printable digital downloads: Christmas kids' printables, planners and wall art.
- **Owner:** new to AI. Every message to her must be short and plain, with numbered steps for anything she has to do.
- **Goal:** traction and sales before Christmas. The key windows are Cyber Week (Nov 27 – Dec 1) and the last-minute "print tonight" window (Dec 15–24). After that, New Year planners.

## Listings (Etsy listing IDs)
| Product | ID | Price |
|---|---|---|
| Santa Mail Set bundle (5 printables) | 4617961573 | $7.99 |
| Dear Santa letter (her Canva design) | 4617955241 | $3.49 |
| Reply / Letter from Santa | 4617969930 | $3.49 |
| Nice List Certificate | 4617970196 | $3.29 |
| Christmas Wish List | 4617961559 | $2.99 |
| Christmas Wish List v2 (Want/Need/Wear/Read) | 4620448127 | $2.99 |
| Christmas Elf Arrival Letter | 4617961567 | $3.29 |
| Christmas Elf Letter Bundle (4 letters) | 4620465174 | $4.99 |
| Santa's Little Helpers Coloring Book | 4619864564 | $3.99 |
| Holly Jolly wall art | 4619864570 | $2.99 |
| 2027 Planner | 4617986184 | $5.99 |
| Budget Planner | 4617978275 | $4.99 |
| 2027 Wall Calendar | 4617981997 | $3.99 |

## Systems and how to use them
- **Make** (team 3447485, free plan: **max 2 active scenarios, ~1,000 ops/month**, **5 MB file limit**):
  - Listing uploader: scenario 7049678. Send through webhook with `etsy-shop/src/upload.py <slug>`. It costs about 11 ops per listing.
  - Pinterest: scenario 7049952. Use `etsy-shop/src/pinterest.py` (boards/pins). Board IDs are in `etsy-shop/pins/board_ids.json`.
  - Etsy API runner: scenario 7049590, on-demand, usually **inactive** (slot limit). Results land in data store 202355.
  - Webhook URLs live in the git-ignored files `etsy-shop/.make_hook` and `.pin_hook`. **Never commit them.**
  - **If those files are missing (fresh container):** recover the URLs with the Make tool `hooks_get` (listing upload hook id **3068819** → `.make_hook`, Pinterest hook id **3068908** → `.pin_hook`) and write them back into those files.
  - **If product previews or PDFs are missing:** rebuild them with `etsy-shop/src/build-*.js`. Products made from the owner's own uploads (Dear Santa, coloring book, Holly Jolly) can't be rebuilt, so reuse the videos already in `etsy-shop/media/`.

## Autopilot schedule (runs even if nobody checks in)
| When (ET) | Who | What |
|---|---|---|
| Daily 1:47 PM | shop-manager | Health check: are the next 48 h of TikToks scheduled (top up if not)? Any new orders? Post 1 Pinterest pin. |
| Mon 2:17 PM | analyst → SEO lead → manager | Weekly review, fix weak listings, owner update |
| Mon + Thu 8:23 PM | content creator | New videos, fill 3/day TikTok slots for the next 4 days, plus pins |
| Wed 7:41 PM | product designer → SEO lead | Design and list 1 new seasonal product (≈$0.20 Etsy listing fee) |
| Dec 15 (once) | manager | Switch everything to "last-minute, print tonight" |
| Dec 26 (once) | manager | Pivot to New Year: planners, budget and calendar content; thank-you notes product |
| Jan 5 (once) | manager | Launch Valentine's products and content |
Every run: stay within the Make budget (~1,000 ops/month). If a run hits an error it can't fix, report it plainly to the owner instead of retrying in a loop.
- **Metricool:** use the brand **"doodle and co" (blogId 8191388, TikTok @doodley)** ONLY. **NEVER touch "meatballmyths" (7521392).** Instagram isn't connected yet.
- **Video and image hosting for Metricool:** commit to `etsy-shop/media/` on branch `claude/great-turing-rqc91h`, then use `https://raw.githubusercontent.com/mooneyn60-art/skills/claude/great-turing-rqc91h/etsy-shop/media/<file>` (check that it returns 200).
- **Repo is PUBLIC:** never commit product PDFs, her uploads or listing previews (`products/`, `work/`, `listing-images/`, `tiktok/` are git-ignored).

## Build tools (etsy-shop/src)
- `build-products.js`, `build-planners.js`, `build-calendar.js`, `build-wishlist-v2.js`: product PDFs (Letter + A4).
- `build-*-images.js`: listing photos at 2000×1500.
- `build-tiktok-anim.js`: animated TikToks (ADS + VARIANTS blocks), 1080×1920, about 14 s.
- `make-music.py`: royalty-free music (our own "Jingle Bells" arrangement plus an original planner loop).
- `build-pins.js`, `build-planner-pins.js`: Pinterest pins at 1000×1500.

## Rules (from our research)
- **Etsy:**
  - Exactly 13 tags, each ≤20 characters.
  - Titles ≤140 characters, with **at most one "&"**.
  - Keep prices ≥ $2.50 (fees).
  - Always offer US Letter + A4.
  - Use "Christmas elf", never "Elf on the Shelf" (trademark). Avoid NORAD and Rudolph.
  - No review incentives or swaps.
- **TikTok:**
  - 1–3 posts/day, spaced 3–4 h apart. Slots are 10 AM, 2 PM and 6 PM ET.
  - Hook in the first 2 s, with a cut every ~2 s.
  - Show the price, "Shop on Etsy" and "link in bio".
  - Set commercialContentOwnBrand to true.
  - Don't repost the same video within 7 days.
  - TikTok Shop doesn't allow digital downloads, so always send buyers to Etsy.
- **Pinterest:** 1000×1500 pins, keyword titles, link to the Etsy listing.
- **Honesty:** if art is AI-made, the owner must tick Etsy's AI disclosure. Never invent reviews or sales numbers.
- **Money:** never spend money (ads, upgrades) without the owner approving that specific charge.
