---
name: publish
description: Schedule an Oh Meatball Short or compilation to YouTube through the Metricool MCP tools (createScheduledPost with youtubeData tags, isAiGeneratedContent true, type short, 10 AM / 4 PM ET), hosting the media at a public raw GitHub URL. Use when asked to post, schedule, upload or publish a video.
---

# Publish via Metricool

The human approves the final title + slot before scheduling. Metricool has the YouTube channel connected and a real
tag field ([research/14](../../oh-meatball/research/14-pivot-satisfying-ai.md)).

## 1. Host the media at a public URL
Metricool `media` needs a public URL. Commit the finished file (not raw generations) and use the raw GitHub URL:
```
https://raw.githubusercontent.com/mooneyn60-art/skills/<branch>/skills/oh-meatball/<folder>/<file>.mp4
e.g. https://raw.githubusercontent.com/mooneyn60-art/skills/claude/youtube-monetization-strategy-m9vz6i/skills/oh-meatball/caught-on-camera/goose_sneakers.mp4
```
The commit must be pushed (and the repo public) first. Verify before scheduling:
```bash
curl -sIL "<url>" | grep -iE "^HTTP|content-length"    # expect 200 and the file size
```
Keep files under ~50 MB (`CRF=26` on the tools if needed). Thumbnails (`.jpg`) use the same pattern.

## 2. Get the brand
`getBrandSettings` -> take `blogId` and the timezone (use `America/New_York` for our slots).
Check what's already queued: `getScheduledPosts` for the week, so you don't double-book a slot.

## 3. Schedule
Slots: weekdays 10:00 and 16:00 ET; Saturday compilation 10:00 ([weekly-plan](../weekly-plan/SKILL.md)).
`createScheduledPost` with `date` in ISO 8601 with offset (EDT -04:00 until 2026-11-01, EST -05:00 after) and `info`:
```json
{
  "autoPublish": true,
  "draft": false,
  "text": "A raccoon caught on doorbell camera taking a package at 3 AM… then this happened.\n\n⚠️ AI-generated: this clip is fiction, created with AI video tools. No animals were harmed (or real).\n\n#doorbellcam #animalscaughtoncamera #aianimals",
  "media": ["https://raw.githubusercontent.com/mooneyn60-art/skills/<branch>/skills/oh-meatball/new-format/raccoon_return/raccoon_return.mp4"],
  "providers": [{"network": "youtube"}],
  "publicationDate": {"dateTime": "2026-10-27T16:00:00", "timezone": "America/New_York"},
  "firstCommentText": "",
  "shortener": false,
  "smartLinkData": {"ids": []},
  "descendants": [],
  "youtubeData": {
    "title": "Raccoon Took the Package… Then Came Back 😳 #plotwist",
    "type": "short",
    "privacy": "public",
    "tags": ["raccoon caught on camera", "raccoon doorbell camera", "doorbell camera", "caught on camera", "ai animals"],
    "category": "PETS_ANIMALS",
    "madeForKids": false,
    "isAiGeneratedContent": true
  }
}
```
Rules: `type` = `"short"` for vertical <= 3 min, `"video"` for the long-form compilation (add `videoThumbnailUrl`
with the raw .jpg URL only for `video`, and only if the channel is verified; otherwise omit it or the request is
rejected). `isAiGeneratedContent` is **always true**. `madeForKids` always false. `tags` comes from
[tags-seo](../tags-seo/SKILL.md) (list form, total <= 480 chars). Leave `notifySubscribers` out.

## 4. After scheduling
- Report the returned `plannerUrl` to the human.
- After it goes live: in Studio confirm "Altered or synthetic content = Yes", set the Related video to this week's
  compilation, pin a comment ([seo-packaging.md §5c](../../oh-meatball/playbook/seo-packaging.md)).
- Add a row to [data/metrics.csv](../../oh-meatball/data/metrics.csv) when the video id is known ([analytics-review](../analytics-review/SKILL.md)).
- Cross-post the clean master to TikTok/Reels only when those are linked (`tiktokData.isAigc: true`,
  `instagramData.type: "REEL", isAiGenerated: true`).

Fix a mistake with `updateScheduledPost` (same `info` shape) instead of creating a duplicate.
