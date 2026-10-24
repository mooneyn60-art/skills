# The Showrunner (head writer) playbook

Desk id: `showrunner`. Absorbs: Showrunner, Hitmaker, Writer, Historian, Newsroom. Read this before every run and append lessons after.

## Read first
- research/39 Meatball show bible
- research/28 Shorts virality
- research/19 topic backlog
- research/27 case studies
- research/41 stickman reference

## Rules (proven)
- Persona: "The Narrator Who Is Food". Meatball is a calm nature-doc narrator who quietly worries whenever eating or predators come up.
- Joke density: about 4.5-7 jokes a minute; pause before the punch word; one soft "tink" sting max; the Fork gag on eating lines.
- Hook = the claim stated as a fact or a correction ("Tigers aren't just striped on the fur..."). Never open on "True or false?".
- Danger-to-you and gross biology beat cute trivia (vidIQ outliers 10/24: "Never Play Dead with Bears" 682K on a 1.7K-sub channel).
- Search-first: every episode answers a question people type (research/34: "do animals know they're pets" +732%).
- Vary structure between episodes; templated sameness is the main YPP review risk.
- Trend-jacking: a fact-checked Short within 24 h when an animal story goes viral; skip if nothing is truly viral.

## KPIs this desk owns
- Jokes/minute
- Retention at joke beats
- Shorts views per topic class

## Lessons log (newest last; date, what happened, what we learned, the number)
- 2026-10-24: desk created by merging the roles above.
- 2026-10-24 (Would Meatball Survive? pack, Halloween pack, history-02):
  - A 20-26 s Short is 60-68 words at +4%, loop line included. My first draft ran 72-93 words (27-35 s est.), so trim before cutting. Each shot covers 8 words at most, which keeps every picture under 3 s. A word-count + `at` checker script caught 28 over-long shots in the first draft.
  - `at` cut words must be unique from the previous cut onward. "a", "it", "they" and "its/it's" match too early, so cut on content words.
  - The verdict card ("Survival odds / Delicious odds") is the series' signature. Rotate the third tag every Short ("Fruit odds: relevant", "Leftovers: none") so the series doesn't read as templated (YPP risk, research/38 P8).
  - Not every verdict has to be zero. The cone snail ("It's a snail. Just never pick one up."), piranha and blue-ringed octopus land better as reversals.
  - Long-form at +4% with -3Hz pitch runs about 160 wpm. 1,150 words comes to about 7.3 min, and 1,000 words came up short, so budget 1,150-1,350 words for 7-9 min.
  - vidIQ (10 credits): "do animals know they're pets" now reads under 750/mo (research/34 had 44K). The neighbours carry the volume: "do cats understand humans" +90.6%, "how dogs see humans" comp 29. Put the question in the title and the neighbours in the tags.
- 2026-10-24 (newsroom, marketing desk): nothing truly viral to trend-jack. The best candidate, a California "shark photobomb" (ClickOrlando 10/22), has no view counts, no confirmed species and an article that says it "looks fake". I skipped it (accuracy first). Evergreen spin-off for the backlog: great whites breach fully out of the water when ambushing seals from below (False Bay). It fits the danger class; use CC photos, never the clip.
- 2026-10-24 (Meatball Explains #2, "The Most Dangerous Animal in the World Isn't What You Think", Tue 11/3 2 PM):
  - Topic pick, 15 credits on keywords: "the most dangerous animal in the world" 12.6K/mo comp 59, "deadliest animals" 49K/mo +76%, "most dangerous animals in the world" 22K/mo +127%. "Animals that look harmless but are dangerous" reads under 750/mo; its neighbours (slow loris, blue-ringed octopus) are mostly spent by the survive pack. A ranked countdown ("smallest number first") is one story with a built-in payoff, and it reused zero myths from 04/07.
  - Titles: the plain search phrase plus "Isn't What You Think" scored 100; "(It's Not a Shark)" 99; a colon claim title 96. For long-form, the search phrase plus a curiosity tail beats a claim title.
  - Words: 1,086 words rendered to 6:53 (Ep #1: 1,104 words → 7:04), so 155-160 wpm holds. Budget about 1,150 for 7:15.
  - Shorts: I capped every hook group at 46-60 words, loop line included, with no text cards or holds over 0.3 s. Ep #1's groups ran 68-102 words and rendered 30-44 s. Count the group words before rendering: under 60 words lands near 25 s.
  - Shorts questions: put the question as its own 4-6-word beat just before the loop line ("Still going in the water? Comment."). hook_loop then appends loop_say after it, so the question is the last spoken line before the loop.
  - Comment read-outs: the episode after a new one always renders before its predecessor airs (render days ahead). Ep #2's beat 2 had to guess Ep #1's answers. Fix: render the read-out beat last, or keep it a single beat that can be re-rendered with --skip-existing after the comments arrive.
  - Thumbnail: dog face-forward with eyes + smug Meatball + "DEADLIER THAN SHARKS", no rays, scored 60, our best yet (the previous best was 57, also a front-facing dog). A snarling lion with "NOT EVEN CLOSE" scored 38 ("too busy", "face and text compete"). vidIQ asked for a question mark: next test is "DEADLIER THAN SHARKS?".
  - tools/episode.py has no separate Shorts voice ("short_voice" is ignored): Shorts use the spec "voice". It needs a code change before a premium Shorts voice can be tested.
