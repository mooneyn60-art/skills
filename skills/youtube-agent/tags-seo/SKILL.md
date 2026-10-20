---
name: tags-seo
description: Write YouTube tags (480 characters or fewer), 3-5 hashtags and the description for an Oh Meatball Short or compilation from the keyword bank, with the AI disclosure always on. Use when asked for tags, hashtags, description, SEO or metadata.
---

# Tags, hashtags, description

Sources (link, don't copy): keyword bank [seo-packaging.md §1](../../oh-meatball/playbook/seo-packaging.md), ready tag
sets §3 (doorbell raccoon, backyard bear, porch goose, dog chaos, parking lot, compilation), description templates
§5a/§5b, hashtag rules §5d. Generator: [tools/meta.py](../../oh-meatball/tools/meta.py).

## Fast path
```bash
cd skills/oh-meatball/tools
./meta.py --type doorbell --animal raccoon --hook "stole a package" > /tmp/meta.json   # title, description, tags
python3 -c "import json;m=json.load(open('/tmp/meta.json'));print(len(m['tags']), m['tags'])"
```
Then adjust by hand with the rules below (meta.py's title is a fallback; use [titles-thumbnail-text](../titles-thumbnail-text/SKILL.md)).

## Tags (YouTube tag field, comma-separated)
- Total **<= 480 characters** including commas (YouTube's limit is 500; keep headroom).
- Order: 2-3 exact-match scenario tags -> animal tags (§1c) -> camera tags (§1d) -> 2-3 head terms (§1a) ->
  `ai animals`, `realistic ai animal video` -> 1-2 seasonal (§1e) only within 2-3 weeks of the date.
- No brand names (ring, nest, arlo, blink, tesla), no "real", no unrelated trending terms (misleading metadata).
- Count before posting: `python3 -c "print(len('''<tags>'''))"`.

## Hashtags
- 3 in the description (max 5): one camera (`#doorbellcam`), one niche (`#animalscaughtoncamera`), one AI (`#aianimals`),
  optionally one animal (`#raccoon`). `#shorts` optional and last.
- Title: 0-2 niche hashtags (`#doorbellcam`, `#plotwist`).
- Never `#fyp`, `#viral`, `#real`, `#notfake`, brand tags.

## Description (Shorts)
```
A raccoon caught on doorbell camera taking a package at 3 AM… then this happened.

⚠️ AI-generated: this clip is fiction, created with AI video tools. No animals were harmed (or real).

🍝 More chaos every day → https://www.youtube.com/channel/UCw98RQD81t_339LX5EJqcrg?sub_confirmation=1
📼 Full compilation → [this week's compilation link]

#doorbellcam #animalscaughtoncamera #aianimals
```
- First line: keyword-rich restatement, no spoiler. "AI-generated" stays in the first 2 lines, always.
- Long-form: use §5b with chapters (see [compilation](../compilation/SKILL.md)).

## Disclosure stays ON (non-negotiable)
- Metricool: `youtubeData.isAiGeneratedContent: true` on every post ([publish](../publish/SKILL.md)).
- After publish, confirm in Studio that "Altered or synthetic content = Yes" ([algorithm.md §0 rule 5, §6](../../oh-meatball/playbook/algorithm.md)).
- TikTok `isAigc: true`, Instagram `isAiGenerated: true` when cross-posting.

## Output
```json
{"title": "...", "description": "...", "tags": ["raccoon caught on camera", "raccoon doorbell camera", "..."],
 "tags_chars": 455, "hashtags": ["#doorbellcam", "#animalscaughtoncamera", "#aianimals"]}
```
