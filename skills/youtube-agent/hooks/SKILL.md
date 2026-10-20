---
name: hooks
description: Write the first-second hook (opening visual + on-screen text of 6 words or fewer) for an Oh Meatball "caught on camera" animal Short. Use when planning or editing a clip and asked for a hook, an opener, on-screen text, or "why are people swiping away".
---

# Hooks: 21 formulas for caught-on-camera Shorts

The feed decides on "Viewed vs. Swiped away" in the first second ([algorithm.md §0 rule 1, §4 Hook](../../oh-meatball/playbook/algorithm.md)).
A hook = **frame-1 visual** (animal already moving, cam UI visible) + **text hook of 6 words or fewer** that sets an
expectation the twist (at 70-85% of runtime) breaks. You draft; the human picks.

## Rules
- Frame 1 has motion and a clear subject. Never open on an empty porch; trim the first 1-2 s of every generation.
- Cam overlay (timestamp, REC, camera label) is on from frame 1: it is the genre signal.
- Text: 6 words max, top third (avoid bottom 20% and right edge), on screen 0-2 s.
- The hook never reveals the twist and never claims the clip is real ("REAL", "not fake").
- No hook may imply danger, injury or a rescue ([algorithm.md §0 rule 2](../../oh-meatball/playbook/algorithm.md)).

## The 21 formulas
| # | Formula | Frame-1 visual | Text hook example |
|---|---------|----------------|-------------------|
| 1 | Time stamp dread | IR doorbell, eyes glowing at the edge | `3:12 AM. Something's on the porch` |
| 2 | Wait for it | Raccoon already lifting a package | `Wait for the second one…` |
| 3 | Mistaken identity | Shape at the door, backlit | `I thought it was the delivery guy` |
| 4 | Why is my X | Pool water sloshing, fur floating | `Why is my pool moving??` |
| 5 | Finally caught | Goose mid-grab of a sneaker | `Finally caught the shoe thief` |
| 6 | Nobody expected | Deer approaching the lens | `Nobody expected what he did next` |
| 7 | Thought no one was watching | Bear looks both ways | `He thought no one was watching` |
| 8 | Left for N minutes | Dog standing in a fresh hole | `I left for 10 minutes` |
| 9 | Neighbor sent this | Shaky phone frame, animal in shot | `My neighbor sent me this` |
| 10 | One job | Dog "guarding" an open gate | `He had one job` |
| 11 | Day N series | Same goose, same porch | `Day 7 of the goose` |
| 12 | Rate it | Raccoon mid-escape over a fence | `Rate this escape 1-10` |
| 13 | Spot it | Busy backyard, one odd detail | `Did you spot it?` |
| 14 | Wrong address | Moose at the front door | `Pretty sure he's lost` |
| 15 | Before the light | Porch dark, motion at the edge | `Wait for the porch light` |
| 16 | Countdown | Animal frozen, staring at lens | `3… 2… 1…` |
| 17 | It came back | Empty spot where the animal left | `It came back. With friends` |
| 18 | Polite criminal | Raccoon knocking on the door | `The politest thief ever` |
| 19 | Owner POV | Dashcam, animal in the road | `Dad told me to honk` |
| 20 | Question | Animal staring directly into the lens | `What is he looking for?` |
| 21 | Real or AI | Hyper-realistic close-up | `Real or AI? Watch his paws` |

Formula 21 is allowed because the AI disclosure label answers it honestly; never answer "real" in replies ([reply-drafts](../reply-drafts/SKILL.md)).

## Output format
Given an idea, return 3 hooks from different formulas:
```
Idea: raccoon steals a package, a second raccoon helps, porch light snaps on
1. #2 Wait for it   | visual: raccoon already dragging the box at 0.0 s | text: "Wait for the second one…"
2. #15 Before light | visual: dark porch, box moving                     | text: "Wait for the porch light"
3. #1 Time stamp    | visual: IR, two pairs of glowing eyes               | text: "3:12 AM. Two of them?"
Pick: 1 (strongest expectation-break; twist = the light catches both mid-step)
```
Log the chosen formula number in `hook` when the clip goes into [data/metrics.csv](../../oh-meatball/data/metrics.csv) notes so
[analytics-review](../analytics-review/SKILL.md) can rank formulas by Viewed %.
