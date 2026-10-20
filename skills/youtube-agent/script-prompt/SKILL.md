---
name: script-prompt
description: Turn an Oh Meatball idea (animal x camera x location x twist) into a realistic text-to-video generation prompt with real animal behavior, a twist at 70-85% and a loopable ending, plus a safety check. Use when asked to write a video prompt, script a clip, or turn a plan row into a generation.
---

# Script -> video-gen prompt

Winning format: one realistic shot, 8-12 s, looks like real doorbell/security/dashcam/phone footage
([research/14](../../oh-meatball/research/14-pivot-satisfying-ai.md)). Obvious AI (cartoon look, costumes, tools) died at 2 views.

## Prompt skeleton (fill every line; 60-120 words total)
```
[CAMERA] Realistic [camera type] footage, [angle/height], [lens look], [lighting], [time of day].
[SCENE] [Location], [2-3 concrete set details].
[0-1 s] [Animal, real species, natural size] is already [moving action] in frame.
[1-6 s] [Setup beat: believable behavior for the species].
[~7 s, 70-85%] [Twist: one surprising but physically plausible action].
[last 1-2 s] [Reaction beat], ends [loop cue: exits the way it entered / returns to the opening pose].
[STYLE] Single continuous shot, static camera, no cuts, natural motion, photorealistic fur, real animal anatomy,
no text, no people's faces, no clothing or accessories on the animal, ambient sound only.
```
Camera look cues (the grain, timestamp and labels are added later by `camify.sh`, so do NOT ask the model for text):
- doorbell_night: "wide fisheye from a doorbell at chest height, black-and-white infrared night vision"
- security_day: "high corner security camera looking down, slightly washed-out daylight"
- dashcam: "dashboard camera behind a windshield, wide angle, road ahead"
- phone: "handheld phone video through a window, slight shake"

## Real behavior only
- Use what the species actually does: raccoons grab with hands and drag; geese honk, flap, carry small objects;
  bears sit, swim, sniff; dogs dig, zoom, look guilty; deer lick and stare; possums freeze.
- No costumes, hats, tools, talking, human posture, impossible strength. Absurd comes from *context* and *timing*.

## Safety gate (reject or rewrite if any is true)
- Animal in distress, pain, trapped, injured, chased, attacked, fighting, near a moving car, or being rescued
  (YPP named example; [algorithm.md §0 rule 2](../../oh-meatball/playbook/algorithm.md)).
- Human injury, real people's likeness, real place names, brand logos, news framing.
- Same animal + same twist as the last 10 uploads.

## Example
Idea: raccoon x doorbell_night x front porch x "returns the package"
```
Realistic doorbell camera footage, wide fisheye at chest height, black-and-white infrared night vision, 3 AM.
Front porch with a welcome mat, a cardboard delivery box and a potted plant.
A raccoon is already on the porch, tugging the box toward the steps with both front paws.
It drags the box to the edge, pauses and looks straight up into the camera.
It slowly pushes the box back onto the welcome mat and pats it twice.
It backs away down the steps and exits left, the porch empty again like the start.
Single continuous shot, static camera, no cuts, natural motion, photorealistic fur, real raccoon anatomy,
no text, no people, no clothing on the animal, ambient night crickets only.
```
Safety: no distress, no danger -> OK. Hook pairing: formula #18 "The politest thief ever" ([hooks](../hooks/SKILL.md)).
Next: [produce](../produce/SKILL.md).
