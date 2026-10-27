# 05. Production at scale: a consistent drawn world at 1-3 Shorts a day

Meatball Research Lab, 2026-10-27. A web-research subagent gathered the prices; the sources are listed at the bottom.
vidIQ spent: **0**.

## Bottom line
**Keep the Python/ffmpeg renderer, but make it a 2D cut-out puppet compositor.**
- Buy the host once, hand-drawn and layered.
- Lock one style.
- Generate only per-episode backgrounds and animal sprites, in that style.
- Automate mouth flaps, blinks, squash/stretch, layer slides and an SFX on every action.

**Running cost: about $40-100 a month**, plus a one-off $400-1,500 for art.

**AI image-to-video for every Short is a trap:**
- At $0.08-0.30 per second with re-rolls, it costs about $25-90 an episode, or $2,000+ a month at our volume.
- Identity drifts between clips.
- It is the look most likely to read as "AI slop" at review.

## Why this pipeline (evidence from items 02 and 04)
- **Animated beats real footage in both outlier samples, and photo-plus-cartoon is worst** (item 02). The look has to change.
- **No image model keeps a character identical across hundreds of images.**
  - Midjourney `--oref`/`--sref`, Nano Banana Pro, gpt-image-1.5 and Recraft styles all drift in small details.
  - A puppet host is drawn once and never regenerated, so only the *style* has to match. That is a far easier problem.
- **A human-drawn host is ownable IP.** Purely AI-generated images probably can't be copyrighted in the US. A recognisable original host is also the strongest single defence against the inauthentic-content rule.

## The pipeline
1. **Host kit (one-off, human illustrator).** Layered PSD/SVG with a written copyright transfer, containing:
   - turnaround
   - separate head/torso/arms/hands/legs
   - 9 mouth shapes (Rhubarb A-H + X)
   - blink frames
   - about 20 expressions
   - about 10 poses
   - a style guide (palette, line weight)
   - about 10 background plates
2. **Style lock.** Train a style LoRA (Flux/FLUX.2 on fal, about $10-25 per run) on the illustrator's plates. Alternatives: a Recraft custom style (~$0.04/image), or Nano Banana / gpt-image with 3-5 reference images.
3. **Per Short:**
   - The script tags beats: `[host:point][animal:octopus scared][sfx:boing]`, one every 1.5-2.5 s.
   - Generate 1-3 animal sprites plus 1 background variant (about $0.10-0.50).
   - Animals are single sprites with eye/mouth overlays and squash/stretch, no full rigs.
   - Every approved sprite goes into a library for reuse. The library compounds, so cost and time per Short fall.
4. **Voice.**
   - ElevenLabs Creator ($22/month, commercial licence, ~121K credits).
   - Our volume is about 145K characters a month (90 Shorts plus 90 TikTok cuts), roughly 72K credits on Flash, so Creator fits.
   - Run Rhubarb Lip Sync (free CLI) on each WAV to get the mouth timeline.
5. **Compositor (existing Python stack):**
   - puppet transforms
   - random blinks every 2-5 s
   - squash on beat hits
   - layer-slide transitions and punch-ins
   - SFX auto-placed from tags (free Sonniss GDC bundle, royalty-free)
   - captions burned in
   - first and last frame matched so it loops
6. **One asset set, three products:**
   - the YouTube Short
   - the 60-90 s TikTok (longer script, same assets)
   - the weekly compilation (stitched with new host link lines)
7. **AI video only for "hero shots":** Kling O3 at ~$0.08/s, at most one 3-5 s shot a week.

**Time per Short (estimate; no hard evidence exists):**
- 4-8 h each for the first 5, while the rig is built.
- About **45-90 min** after that. Most of it is script and joke timing plus sprite QA.

## What to buy first
| Budget | Buy | Probability it pays back in views/hours within 60 days |
|---|---|---|
| First $100 | ElevenLabs Starter/Creator ($6-22) + ~$20 image API + one LoRA run ($10-25) + free Sonniss SFX. Build the puppet compositor with a placeholder AI host. | 60% |
| First $500 | Host kit from Fiverr/Upwork (~$250-400) + 5 plates; retrain the LoRA on it | 55% |
| First $2,000 | Mid-tier illustrator: full kit + 15-20 plates + 3-5 recurring side characters (~$1,200-1,500); Epidemic Sound for a year (~$120); ~$150 of hero AI shots | 45% |

**Order matters:**
- Spend on the **look** before anything else (TARS's plan agrees).
- **Never** spend on YouTube ads or Promote. Paid views and hours count toward neither YPP path.
- The current TikTok Promote push also contaminates the town's organic tests.

## Blunt notes on the current setup
- The town's 48 tools and ~140 queued Shorts were built for the photo slideshow.
  - **Do not re-render the queue.** Let it drain and point new renders at the puppet compositor.
  - P(re-rendering the queue is worth the 2+ days): **15%**.
- **Volume is not the constraint; look and idea are.** Item 02 shows a 30x spread within one identical format.
  - One illustrated Short a day beats three photo Shorts.
  - P(dropping to ~1-2 illustrated Shorts/day loses more views than it gains over 4 weeks): **30%**.

## Recommendations
1. **This week:**
   - Build the puppet layer into the existing renderer with a placeholder host.
   - Commission the host kit.
   - Use the first $100 as listed above.
   - P(first illustrated Short ships by Nov 3): **65%**.
2. **Measure on the NICHE_PLAYBOOK test:** 6 illustrated vs 6 photo, same pillar, stayed-to-watch at 48 h.
   - P(illustrated wins by ≥5 pts): **60%**. (TARS: 10+ pts at 60%; I'm less confident about the size.)
3. **Cap AI video at ≤5% of screen time.**
   - P(a channel built mostly on AI video clips is flagged at YPP review): **35%**.

## Sources (via the subagent; prices change monthly, so recheck official pages)
- gpt-image-1.5 pricing: developers.openai.com/api/docs/models/gpt-image-1.5
- Recraft API: recraft.ai/pricing
- FLUX.2 trainer: fal.ai/models/fal-ai/flux-2-trainer-v2
- Rhubarb: github.com/DanielSWolf/rhubarb-lip-sync
- ElevenLabs tiers: bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs
- Kling/Seedance per-second prices: atlascloud.ai/blog/guides/cheapest-api-provider-seedance-kling-wan
- Sonniss GDC 2026 bundle: rekkerd.org/sonniss-releases-gdc-2026-game-audio-bundle
- Inauthentic-content rename (2025-07-15): socialmediatoday.com/news/youtube-clarifies-monetization-update-inauthentic-repeated-content/752892
- Illustrator prices: Upwork $15-30/h listings; one studio quotes $1-5K per full sheet. These are thin; the kit estimate is the subagent's own.
