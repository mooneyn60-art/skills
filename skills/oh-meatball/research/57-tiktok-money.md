# 57 · TikTok money: how Creator Rewards pays and what we change (2026-10-28)

Nolan, 10/28: "push TikTok hard … we can make some good money and scale YT from it."

## How Creator Rewards pays
Third-party guides only; TikTok publishes no fixed rate.

- **Who qualifies:** 10K followers, 100K views in 30 days, age 18+, videos over 60 s.
- **What counts as a qualified view:** For You views held about 5 s or more; repeat views from the same account count once.
- **RPM** (pay per 1,000 qualified views): about $0.40-1.00 typical. US viewers are worth about $0.85; Brazil about $0.32.
- **What TikTok says raises pay:** originality, play duration (longer watch time), search value, and engagement.
- **Sources:**
  - https://www.elev8or.io/blog/tiktok-creator-rewards-rpm-2026
  - https://www.makeinfluence.com/en/academy/tiktok-creator-rewards-program-how-organic-monetization-works-in-2026
  - https://fluxnote.io/guides/tiktok-creator-rewards-program-rpm
- **What the algorithm pushes** (vendor blogs, unverified):
  - Completion and rewatch first, then shares and saves.
  - Each post gets a small test audience and only spreads if they finish it.
  - Faceless accounts aren't penalised.
  - A recurring series and "Part 2" follow-ups build followers.
  - Source: https://www.darkroomagency.com/observatory/how-tiktok-algorithm-works-in-2026

## Our numbers (Nolan's screenshots, 10/28)
- **Oct 20-26:** 11.4K views, 38 profile views, 179 likes, 1 comment, 2 shares.
- **Where views come from:** For You 96.8%, profile 1.5%, search 1.0%, following 0.7%.
- **Rewards:** we're enrolled. Balance $0.11; per post $0.00 (the tarantula hawk had 759 views).
- **The maths:** about 11K views/week × ~$0.5/1K ≈ $5/week at best.
  - $100/week needs about 200K qualified views/week.
  - $1,000/week needs about 2M.
  - That means single posts reaching 100K+.
  - Our best ever is 5.8K (the bombardier beetle, 10/26).

## What moves the money (in order)
1. **Completion of 60 s+ videos.**
   - TikTok only spreads a post after its test audience finishes it.
   - Shipped today: animal movement, fact gags and no-beep sounds.
   - Proposed: an on-screen title bar (tools/tt_style.py header) so the topic reads in half a second.
   - The art redraw (3 style drafts in progress) is the bigger lever.
2. **Longer play time per viewer:** list videos of 90-120 s that span several animals (tools/tt_style.py listify).
   - These are the 2.5M / 3.3M outlier format.
   - Test 1 a day at 10:00 ET, our audience's peak TikTok hour, which is currently empty.
3. **Double-down rule:**
   - Any TikTok above 2× our median (~400 views) within 24 h gets a Part 2 on the same animal within 48 h.
   - We never did one for the 5.8K beetle.
   - The morning routine checks for these.
4. **Search value** (part of the pay formula):
   - Line 1 of the caption names the thing people search ("bed bugs", "stink bug", "naked mole rat").
   - The title bar text gets read by TikTok's on-screen text recognition too.
5. **US-relevant topics.** US views pay about 2-3× more.
   - House and backyard creatures are a US-relatable topic.
   - Need Nolan's TikTok Analytics → Viewers → top countries screenshot.
6. **Comments are the weakest signal** (1 per 11K views).
   - End each video on a real question with a two-option choice.
   - Reply to comments with a short video ("Reply to @x"); TikTok pushes those to new viewers.
   - Nolan approved reply drafts on 10/28.

## TikTok → YouTube
- **Bio link:** we have more than 1K followers, so the bio can carry a link. Point it at the YouTube channel (Nolan, 1 min).
- **Long-form tie-in:** every list video's last line names the long-form: "the full version is on my YouTube".
  - Mention it at most once per video. Keep the CTA spoken, not a link sticker.
- **Same series on both platforms:** Things Living In Your House runs on both, so a TikTok fan searching YouTube finds the same parts.

## Asks for Nolan
1. **TikTok Analytics → Viewers:** top countries and age.
2. **Rewards analytics → Overview:** qualified views and RPM, 3 days after the new style goes out.
3. **TikTok bio link:** set it to the YouTube channel.
4. **Pins:** pin 3 posts (beetle, centipede, tarantula hawk).

## Viewers (Nolan's TikTok Analytics screenshots, 10/28)
- **Who:** 61% male, 38% female. Ages 18-24 40%, 25-34 34%, 35-44 14%, 45+ 12%: an adult audience. Write for grown men who like gnarly animal facts (fights, venom, gross, survival); the art must look like nature documentary, not a kids' show.
- **Where:** US 45.4%, Pakistan 19.3%, UK 6.8%, Netherlands 2.6%, Germany 2.5%. About 55% are in high-pay countries. Keep topics US/UK-relatable (house, backyard and North American animals).
- **When (Oct 26, the promoted day, ET):** viewers climb from 8 AM, peak 2-4 PM (~1K), and are still ~500/h at 7 PM. TikTok's own peak: Monday 2-3 PM. TikToks now go out between 12 and 5 PM ET; nothing at 9 PM.
- **Daily active viewers:** about 30 (10/21) → 150 (10/25) → 540 (10/26, promotion). This is from one week of data, so check it again on 11/4.
