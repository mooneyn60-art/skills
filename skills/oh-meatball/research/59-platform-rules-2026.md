# 59 · Platform rules check, 2026 (night shift e, rotation c, 2026-10-29)

These are the current YouTube and TikTok rules for an AI-narrated, drawn, template-built animal-facts channel. Each rule gives its source, the date it was checked, what it means for us, and the risk and fix. This follows research/40 (10/28 night c, which built `tools/sameness.py`) and the setup in research/57 and 58 and OPERATIONS.md.
vidIQ was skipped (balance 3, under the 300 floor).

## 1. YouTube YPP "inauthentic content" (formerly "repetitious")
- **Source:** YouTube Help 1311392, YPP channel monetization policies. Its newest dated notice (2025-07-15) renames "repetitious" to "inauthentic". Checked 2026-10-29. https://support.google.com/youtube/answer/1311392
- **The 2026-07-16 clarification** splits the rule into three buckets: template/mass-produced videos, distressing bait, and AI personas giving health, finance or legal advice. https://techcrunch.com/2026/07/20/youtube-clarifies-policies-around-ai-slop-and-upsetting-videos/
- **What's not allowed (quoted from the Help page):**
  - "Similar or repetitive content with low educational value, commentary, narratives, or minimal variation across videos"
  - "AI-generated content made with generic or unoriginal templates giving the impression of mass production"
  - "Image slideshows, templated storylines, or scrolling text with minimal or no narrative..."
  - **"Videos where characters are put in the same situation over and over again with the same outcome"**
- **What's allowed:**
  - "Same intro and outro ... but the bulk of your content is different"
  - "each video has a distinct storyline, focus, or concept"
  - "creative tools to assist in delivering a unique, well-researched, or creative narrative"
- **What it means for us:** an AI voice and drawn art are fine in themselves. What triggers demonetisation is sameness across the whole channel, and a reviewer looks at the channel, not a single video. Our protection is real education (sourced facts), a narrative arc and visual variety.
- **Risk A (new tonight): our mascot series.** "Would Meatball Survive?" and "Meatball vs X" are the series research/58 says to grow. Both match the quoted line about characters in the same situation with the same outcome if Meatball always meets an animal and always loses or always survives.
  - **Fix:**
    - Vary the outcome: Meatball survives, loses, ties, or "it depends on X".
    - Vary the setting and the question per episode (escape, outsmart, hide, befriend).
    - Make the animal's facts the body of the video, not the gag.
    - Add a `series_outcome` field to those scripts. A future sameness check should WARN if 3 episodes in a row share an outcome.
- **Risk B (already found 10/28): repeated beat skeletons and stock lines.** `tools/sameness.py` gates this, so keep the gate on.
- **Risk C: list videos built from our own single-animal clips.** The reused-content rule covers others' material, but a YouTube list that only re-strings clips we already posted adds "minimal variation".
  - **Fix:** every list gets new narration with a new angle (ranking, comparison, a new fact per animal), a new hook and at least one new drawn shot per entry.

## 2. YouTube altered or synthetic content disclosure
- **Source:** YouTube Help 14328491. Checked 2026-10-29. https://support.google.com/youtube/answer/14328491
- **The rule:**
  - Disclosure is required for realistic AI content: real people saying or doing things they didn't, altered real events, realistic scenes that never happened.
  - It isn't required for non-realistic content, fully animated video, or production help (scripts, outlines, thumbnails).
  - Cloning your own voice counts as a minor edit. Generic AI voices aren't addressed.
- **Key line:** "Disclosing AI content alone won't limit a video's audience or impact its eligibility to earn money." Creators who keep failing to disclose risk labels added for them, removal or YPP suspension.
- **What it means for us:** our drawn videos probably don't need the label, but `isAiGeneratedContent=true` costs nothing and covers the AI narrator, which the page doesn't address. **Keep it on.**
- **Risk:** low. Just never add realistic AI footage of real animals or people without the flag.

## 3. TikTok: Creator Rewards, originality, AI labels, reuse
- **AI label:**
  - TikTok requires a label on AI-generated or significantly edited content "that shows realistic-looking scenes or people".
  - Unlabelled content can be restricted or removed.
  - Source: TikTok Community Guidelines, Integrity & Authenticity. Checked 2026-10-29. https://www.tiktok.com/community-guidelines/en/integrity-authenticity
  - Drawn content isn't strictly covered, but our isAigc=on is safe. **Keep it on.**
- **Originality and For You feed:** "Content is also ineligible for the FYF if it includes unoriginal or reused material without anything new" (same page).
  - Creator Rewards counts only qualified For You views, so a video kept off the For You feed earns $0.
- **Creator Rewards eligibility:** 10K followers, 100K views in 30 days, 18+, videos over 60 s, at least 1,000 For You views. Original content only: no reposts, watermarked clips, duets or stitches, and no compilations without new ideas.
  - Payout factors: originality, play duration, search value, engagement.
  - TikTok's own Creator Rewards page now redirects to Creator Academy and wouldn't render, so these points come from third-party guides:
    - https://shortsfast.com/blog/tiktok-creator-rewards-2026-requirements/
    - https://www.makeinfluence.com/en/academy/tiktok-creator-rewards-program-how-organic-monetization-works-in-2026
    - https://blog.nuelink.com/tiktok-creator-rewards-program/
- **AI and Rewards (sources conflict):**
  - One guide says fully AI-made videos with "minimal original input" are excluded.
  - Another says labelling as AI doesn't disqualify a video.
  - Neither is confirmed by TikTok. https://storrito.com/resources/what-tiktoks-ai-monetization-restrictions-signal-for-creator-income/
- **Risk D, the main TikTok one: list videos (E26) reusing clips from TikToks we already posted.** TikTok's duplicate detection doesn't know they're ours. A 90-120 s list stitched from posted cuts reads as "reused material without anything new", which means no For You feed and no Rewards. It would also undercut the 2.5M/3.3M list-format bet.
  - **Fix (cheap):**
    1. New narration per list (ranking/"which is worst" frame, a fresh fact per animal, a new hook).
    2. No reused segment longer than about 3 s, and re-crop or re-colour reused shots.
    3. At least 30% new drawn frames per list.
    4. The new title bar plus a list counter overlay on every entry.
  - **Check:** if a list's qualified views or Rewards come back at $0 with normal views, suspect originality and stop reusing clips.
- **Risk E: the Rewards claim about fully AI videos.** Our protection is human-directed scripts, our own drawn art, and fact-checking with sources. Keep the sources in captions and descriptions as evidence of "original input".

## 4. YouTube monetisation thresholds
- **Source:** YouTube Help 72851. Checked 2026-10-29. https://support.google.com/youtube/answer/72851
- **Full tier (ad revenue) today:**
  - 1,000 subscribers plus either 4,000 qualified long-form watch hours in 12 months, or 10M qualified Shorts views in 90 days.
  - Watch hours from the Shorts feed don't count toward 4,000. The two routes don't combine.
- **Lower tier (fan funding and Shopping, no ad share):** 500 subscribers, 3 public uploads in 90 days, and either 3,000 watch hours in 12 months or 3M Shorts views in 90 days. Page 72851 didn't show this tier; the figures are from https://vidiq.com/blog/post/monetize-youtube-guide/ and air.io.
- **NEW: the YPP update on 2027-02-01.**
  - Page 72851 confirms the date: "Starting February 1, 2027, we are introducing updates to the YouTube Partner Program". Existing partners must accept the new terms by 2027-01-31.
  - Four outlets report that new applicants after that date need **8,000 watch hours or 20M Shorts views** (1,000 subs unchanged). Existing partners are grandfathered, but Shorts revenue sharing gets a new floor. The doubled thresholds aren't on YouTube's page yet.
  - Sources:
    - https://www.newsshooter.com/2026/08/10/youtube-updates-its-partner-program/
    - https://www.cined.com/youtube-makes-monetization-harder-new-partner-program-rules-explained/
    - https://www.searchenginejournal.com/youtube-updates-partner-program-terms-shorts-payout-rules/585331/
    - https://uppbeat.io/blog/creator-news/youtubes-partner-program-is-getting-new-ways-to-earn-in-2027-but-the-bar-to-join-is-rising
- **What it means for us:** OPERATIONS.md stage 3 ("1,000 subs + 4,000 long-form watch hours / 12 months") goes stale on 2027-02-01.
  - If we haven't applied by about 2027-01-31, the bar doubles.
  - That leaves about 13 weeks. We'd need about 4,000 h in that window, roughly 300 h/week, against about 1,300 episode views/week planned at 3.5 min, which is only about 75 h/week.
  - Shorts: 10M views in 90 days is far above our current pace. The lower tier (500 subs + 3M Shorts views) is more reachable but pays no ad share.
- **Owner decision needed (Nolan):**
  - Either sprint on long-form watch hours before 1/31 (more/longer episodes, Shorts that link to long-form, playlists), or accept the 8,000 h / 20M bar and plan stage 3 around it.
  - Also confirm the thresholds in YouTube Studio → Earn, which shows our live eligibility.

## Summary
| # | Risk | Severity | Fix | Owner |
|---|---|---|---|---|
| A | Meatball series = same situation, same outcome | High (channel-level YPP) | Vary outcomes and settings; outcome field plus a sameness WARN | showrunner / tools (g night) |
| D | TikTok lists re-string posted clips | High (kept off For You feed = $0 Rewards) | New narration, ≤3 s reuse, ≥30% new frames | showrunner / studio |
| — | YPP bar doubles 2027-02-01 | High (timing) | Watch-hour sprint vs replan; check Studio → Earn | **Nolan** |
| B | Beat-skeleton sameness | Medium | `tools/sameness.py` gate (built 10/28) | studio |
| E | TikTok "fully AI" Rewards claim | Low-medium (unverified) | Human scripts, own art, sources in captions | showrunner |
| — | AI labels | Low | Keep isAiGeneratedContent / isAigc on | postmaster |
