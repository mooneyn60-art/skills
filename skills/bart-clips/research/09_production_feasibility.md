# 09 — Production Feasibility: what can be made right now for $0 / near-$0

Checked 2026-10-15. Read-only: no media was generated and no credits were spent. Balances come from live tool calls. Free-tier figures for third-party apps come from web roundups that often disagree, so treat them as approximate and check the vendor page before relying on them.

## 1. What the connected accounts hold (checked live)

| Account | Balance / plan | Notes |
|---|---|---|
| **vidIQ** (`vidiq_balance`) | **5,903 credits** (4,995 of 6,000 renewable + 908 of 1,000 add-on). Renewable credits refill **2026-10-22**. | This is a paid Max-tier allowance, so generating with it costs $0 extra. **This is the main AI-video budget.** |
| **Higgsfield** (`balance`) | **0 credits, free plan.** `unlim.available=false`. No free daily generations on MCP. | The listed "unlimited" models (Seedance 2.0, Kling 3.0, Wan 2.7, Gemini Omni) need a paid plan and work on the web only, not through MCP. A **3-day Plus trial** is on offer: 100 MCP-only credits (about 4 Seedance videos), card required, then **auto-renews at $49/mo** unless cancelled. Plus is $49/mo or $39/mo billed annually, 1,000 credits. Ultra is $129/mo or $99/mo billed annually, 3,000 credits. |
| **OpusClip** (`opusclip_get_usage`) | **278 processing minutes** left. API cap: 871 of 900 per month (resets Nov 1). | Clips long source videos into Shorts. It does not generate AI footage, so it is only useful when there is long footage to repurpose. |

### vidIQ generator costs (from the tool descriptions)
| Tool | What it makes | Cost |
|---|---|---|
| `vidiq_generate_video` | Text-to-video or image-to-video, 9:16 supported. Models: veo-3.1 / -fast / -lite, kling-3 / -pro, seedance-2 / -fast, minimax-h3, gemini-omni-flash (includes audio) | duration (s) × model's per-second rate × 20 credits, quoted exactly at submit and refunded on failure. **The per-model rate is not published.** Estimate, assuming the rate tracks API list price (Veo-3.1-fast is about $0.10/s): an 8s clip costs about 16 credits, and Seedance or Kling-pro costs about 3–5x that. Confirm with one quoted submit. |
| `vidiq_voiceover_generate` | TTS MP3 | 14 credits per 1,000 characters (a 45s Short script is about 14 credits) |
| `vidiq_generate_music` | Royalty-free WAV, 10–180s | 25 credits per track |
| `vidiq_generate_broll` | Free stock clips (up to 4, with photographer credit required) | 1 credit per search |
| `vidiq_compose` | Renders scenes, voiceover, music and text overlays into MP4 (vertical supported) | 1 credit per 4s of output, minimum 2 (a 45s Short is about 12 credits) |
| `vidiq_motion_graphics` | Kinetic text, stat counters, title cards (DSL to MP4, 1080x1920) | Cost not shown in the truncated description. Check before use. |
| `vidiq_instagram_publish_reel` / `vidiq_video_upload` | Publishing | Not used in this research |

## 2. Local container (CPU only)
- **Hardware:** 4 vCPU, 15 GB RAM, **no GPU** (`nvidia-smi` is absent), about 27 GB free disk. Local text-to-video or image-to-video diffusion (Wan, LTX, and similar) is **not feasible** here.
- **Installed:** Python 3.13, ffmpeg 6.1, Pillow 12.3, numpy, onnxruntime 1.29, faster-whisper 1.2.1 (captions on CPU). No torch.
- **Repos in /home/user:**
  | Repo | Can it generate AI video or TTS here? |
  |---|---|
  | VoiceStudio | **TTS: yes, slowly.** Its README says it is fully usable on CPU (needs about 5 GB for CPU PyTorch). It includes light engines (`supertonic3`, `pockettts`, `moss_tts_nano`). It is an Electron app plus a FastAPI backend, AGPL-3.0, and fiddly headless. The quicker route is `pip install kokoro-onnx` (0.6.1, on PyPI, runs on onnxruntime CPU). |
  | diffusionstudio | **No.** It is a toy 2D-point diffusion teaching repo (MLP/UNet on 2D data) and does not generate video. |
  | vinci-clips | **No** generation. It clips long videos with Gemini and FFmpeg and needs MongoDB, GCS and a Gemini key. |
  | clipsai | **No** generation. It clips and reframes podcast-style long video and needs WhisperX (torch). |
  | ai-youtube-shorts-generator_samuraigpt | **No** generation. It clips long YouTube videos with an LLM and Whisper and needs an OpenAI-class key (or MuAPI). |
- **Conclusion:** Locally we can assemble Shorts (ffmpeg plus Pillow for kinetic text, Ken Burns on stills, burned-in captions), produce TTS (kokoro-onnx or VoiceStudio), and produce captions (faster-whisper), all at $0. We cannot create AI footage locally.

## 3. Feasibility table

| Tool | What it makes | Free amount | Cost to scale | Watermark / commercial terms | Agent can drive it here? |
|---|---|---|---|---|---|
| **vidIQ MCP** (connected) | AI text/image-to-video (Veo 3.1, Kling 3, Seedance 2, MiniMax H3, Gemini Omni), voiceover, music, stock B-roll, compose, motion graphics | **5,903 credits now, about 6,000 renewable per month** (already paid) | Plan upgrade or add-ons (vidIQ pricing per vidiq.com/plans) | vidIQ output has no visible watermark noted in the docs. Stock B-roll **requires attribution**. Model-provider terms apply, and Veo embeds SynthID. | **Yes, fully** via MCP: generate, poll, compose, then hand off an MP4 URL |
| **Higgsfield MCP** (connected) | Seedance 2.x/2.5, Kling 3, Wan, MiniMax, FLUX 3 Video, Shorts Studio, TikTok publish | **0** (free plan, no free MCP generations) | 3-day trial (100 credits, card, then $49/mo). Plus $39–49/mo for 1,000 credits (about 200 Kling clips). Ultra $99–129/mo for 3,000. | Paid plans give commercial output. Unlimited and free-generation offers are web-only and do not work through MCP. | Yes once funded. **Not usable at $0.** |
| **OpusClip MCP** (connected) | Clips and reframes long video into Shorts with captions | 278 minutes left | Paid plan minutes | Paid account, so no watermark | Yes, but it needs long source footage (it does not generate) |
| **Local: ffmpeg + Pillow + kokoro-onnx/VoiceStudio + faster-whisper** | Text and motion-graphic Shorts, slideshows, narration, captions | **Unlimited, $0** | $0 (CPU time only: about 1–3 min render per Short) | None. You own the output. kokoro is Apache-2.0. VoiceStudio is AGPL (copyleft applies to the app's code, not to its outputs). | **Yes, fully** (Bash) |
| **Google Flow / Veo (web)** | Veo 3.1 (Lite/Fast) clips, up to 8s, 720p | About 50 credits/day reported (roughly 5 Lite clips). Sources conflict. | Google AI Pro/Ultra subscriptions | Free output reportedly carries a visible "Veo" mark plus SynthID | **No.** Web UI only, and the Gemini API has no free Veo tier. |
| **YouTube Create / Shorts Veo** | Veo clips inside the YouTube app | Free in-app (Veo Fast). Limits not confirmed. | Free | SynthID plus an AI label, and the output is YouTube-native | **No.** Mobile app only, manual. |
| **Sora app** | Sora 2 clips | About 30/day reported in late 2025, possibly reduced since | $4 per 10 extra generations, or ChatGPT Plus/Pro | Visible Sora watermark on free output | **No.** App only, no API at the free tier. |
| **Kling (web)** | 5s clips | About 66 credits/day reported | Paid plans | Watermarked on free. Commercial use not confirmed. | **No.** Web only (but Kling 3 is available through vidIQ). |
| **Hailuo / MiniMax (web)** | 6s 768p clips | Daily free credits reported but unreliable | Paid plans | Watermarked on free | **No** (but MiniMax H3 is available through vidIQ) |
| **Pika / Luma (web)** | Short clips | Small daily or monthly free credits | Paid plans | Watermarked. Luma free is **non-commercial**. | **No** |
| **Seedance / Dreamina (web)** | 1080p clips | Daily credits reported, small or no watermark (sources conflict) | Paid plans | Check ToS | **No** (but Seedance 2 is available through vidIQ) |

## 4. Cheapest realistic pipeline for 1 AI Short per day

**Use the vidIQ credits already paid for, and do all assembly locally.** Incremental cost is $0.

1. Write the script and hook (Claude, free).
2. Generate **2–3 AI hero shots** with `vidiq_generate_video` (veo-3.1-fast or -lite, 9:16, 6–8s each). Estimated 16–50 credits per day. Confirm the real per-second quote on the first submit.
3. Fill the remaining runtime with **stock B-roll** (`vidiq_generate_broll`, 1 credit per search, credit the photographer) or local Pillow/ffmpeg motion-text scenes ($0).
4. Generate narration with **local kokoro-onnx or VoiceStudio** ($0), or `vidiq_voiceover_generate` (about 14 credits) for a better voice.
5. Generate captions with faster-whisper locally, then do the final mux in ffmpeg ($0). `vidiq_compose` (about 12 credits) is the alternative if ffmpeg is unavailable.
6. **Budget:** about 30–80 credits per Short, so about 1,000–2,400 per month against 6,000 renewable. This leaves headroom for 2–4 Shorts per day.
7. **$0 fallback if vidIQ credits run out:** fully local text, motion-graphic and Ken Burns Shorts plus stock B-roll. These are faceless and have no AI footage.

Policy note: YouTube's July 2026 inauthentic-content clarification demonetizes template or mass-produced AI channels at channel level. Each Short needs a distinct script, angle and edit, not a reused template. AI disclosure labels reportedly do not reduce reach.

## 5. What the owner must sign up for

- **Nothing required** for the pipeline above. vidIQ is already funded and resets 2026-10-22.
- **Optional:**
  - **Higgsfield Plus** ($39/mo billed annually) only if Seedance or Kling quality through Higgsfield and its TikTok publishing are wanted. Avoid the "free" 3-day trial unless the owner deliberately accepts the $49 auto-renew.
  - **Google Flow / YouTube Create** (free, manual, owner taps through the app) for extra Veo clips.
  - **A free Pexels API key** for unlimited stock B-roll without spending vidIQ credits.
- **No owner action needed:** installing `kokoro-onnx` locally (pip, $0) for offline TTS.

## Sources
- Live tool calls: vidiq_balance, Higgsfield balance / models_explore / show_plans_and_credits, opusclip_get_usage (2026-10-15)
- [AI Video API Pricing 2026 (devtk.ai)](https://devtk.ai/en/blog/ai-video-generation-pricing-2026/), [echai.ventures pricing](https://echai.ventures/how-founders-use-ai/video-image-audio/what-does-ai-video-and-image-actually-cost-and-what-s-a-sensible-starter-stack-on-a-founder-budget)
- [vidIQ pricing 2026 (1of10)](https://1of10.com/blog/vidiq-pricing/)
- [Google Veo free-tier workflow](https://mikekwal.com/blog/google-veo-free-tier-video-workflow/), [Atlas Cloud: Veo 3.1 free or paid](https://www.atlascloud.ai/blog/guides/veo-3.1-ai-video-generator-free-or-paid), [Veo in YouTube Shorts (etcentric)](https://www.etcentric.org/google-adding-ai-video-generator-veo-3-to-youtube-shorts/)
- [Best free AI video generators 2026 (vuela)](https://vuela.ai/blog/best-free-ai-video-generators-2026), [morphed.app](https://morphed.app/blog/best-free-ai-video-generators), [felloai](https://felloai.com/best-free-ai-video-generators/)
- [Sora paid credits (storyboard18)](https://storyboard18.com/digital/sora-no-longer-fully-free-as-openai-introduces-paid-credits-83589.htm)
- [YouTube inauthentic-content rules (androidheadlines)](https://www.androidheadlines.com/2026/07/youtube-monetization-rules-ai-slop-inauthentic-content.html), [outlierkit July 2026](https://outlierkit.com/blog/youtube-updates-july-2026)
