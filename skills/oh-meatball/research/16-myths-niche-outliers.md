# 16 — Animal-myths niche: what is breaking out now (snapshot 2026-10-22)

**Sources.** The free `youtube-agent/virality/scripts/outliers.py` (yt-dlp, no API key). It ran 6 query sets: 8 long-form and 8 Shorts relevance queries, plus 7 long-form and 6 Shorts queries filtered to **upload date = this year** (YouTube `sp` filter, via a scratch wrapper that reuses the script's scoring). That came to about 230 scored videos. One web search found nothing useful. No vidIQ, no paid tools.

**Score** = a video's views ÷ the median views of its channel's ~15 latest uploads (videos and Shorts).

**Legend.** **[M]** = measured in these runs. **[I]** = my inference.

**Caveats.**
- YouTube bot-walled per-video metadata, so exact upload dates exist only for a few videos. "Age" is YouTube's relative `publishedTimeText` from the date-filtered search, and it was checked against 8 known dates.
- Shorts ages are not shown by search. Every Shorts row in table B comes from the "this year" filter, so each one is ≤ ~10 months old **[M]**.
- Channels with a tiny median (under 100 views) give inflated scores. Weigh those by raw views.

## 1. Top outliers

### A. Long-form, ≤ 12 months old (on-niche only)

| # | Title | Channel | Views | Score | Length | Age | URL |
|---|---|---|---|---|---|---|---|
| 1 | 28 Mythical Sea Creatures that Really EXISTED! \| Full series | Mysterious-Fact | 1.01M | 62.9x | 37:35 | 10 mo | youtu.be/iwYkO8Erf2Y |
| 2 | 42 Animal Myths You've Believed Your Whole Life | Oddly Factual | 118k | 53.8x | 1:50:47 | 4 mo | youtu.be/yKjgTtMawTQ |
| 3 | 40 Animal Myths You've Believed Your Whole Life | Lying Pie | 335k | 45.9x | 32:11 | 10 mo | youtu.be/fRFrWTEDH0s |
| 4 | TRUE or FALSE ANIMAL QUIZ | GUESS IT | 2.9k | 42.0x (median 68) | 13:44 | 8 mo | youtu.be/_b9-R9FnNM0 |
| 5 | 7 Extinct Animals That Might Still Be Alive in the Amazon | Myths-creature | 1.64M | 32.8x | 9:53 | 7 mo (2026-03-14) | youtu.be/dUJ8yLMT09c |
| 6 | Weird Animals Iceberg | Psychopoly | 2.09M | 12.8x | 54:30 | 10 mo | youtu.be/0mvkvPc-IS0 |
| 7 | 36 Animal Facts So Weird I Had to Animate Them | Slug hug | 33k | 10.1x | 2:31 | 11 mo | youtu.be/d9T3Q-o3HZo |
| 8 | Weird Animal Facts You Never Knew - Part 6 | What Gives? | 508k | 9.7x | 10:09 | 9 mo | youtu.be/t6VGXyfDT_Y |
| 9 | Animal Lies And Myths That You Actually Believe - Part 2 | What Gives? | 419k | 8.2x | 9:53 | 6 mo | youtu.be/yiucYrgAulY |
| 10 | Fake Animal Facts You STILL Believe! - Part 1 | WildNature Lab | 976 | 7.6x | 4:57 | 5 mo | youtu.be/Ra_YzDjHlGw |
| 11 | Weird Animal Facts You Never Knew - Part 7 | What Gives? | 383k | 7.5x | 12:08 | 8 mo | youtu.be/w4vGRZUEVwA |
| 12 | The Craziest Discoveries That Proved Historians Wrong (Kelevin-style, adjacent) | The Paint Explainer | 2.33M | 6.8x | 19:43 | 7 mo | youtu.be/yVN20FcBbwM |
| 13 | Absurd Animal Myths That Turned Out To Be Completely Wrong | Mindfeed | 849 | 5.5x | 8:01 | 9 days | youtu.be/hEBoCBJ89pE |
| 14 | Sharks Can't Smell Blood a Mile Away + 6 More Animal Myths Busted | Wilder TCG | 276 | 5.2x | 4:57 | 2 days | youtu.be/evU0cQBKfEY |
| 15 | Epic Animal Facts | Wild Kratts | 675k | 5.1x | 40:49 | 5 mo | youtu.be/vqxbWSC_E4I |
| 16 | True or False? The Ultimate Animal Quiz Challenge! | Blue Peter | 10.3k | 3.2x | 7:33 | 3 wk | youtu.be/_DrIGEOcgWc |
| 17 | Mythical Creatures That Turned Out To Be Real | Trust Me Bro | 1.86M | 2.4x | 28:05 | 6 mo | youtu.be/TvhuqC8oxlY |

### B. Shorts, uploaded this year (2026)

| # | Title | Channel | Views | Score | URL |
|---|---|---|---|---|---|
| S1 | The Biggest Lies In The Animal Kingdom! 😱 | Infinite Fact | 3.42M | 53.4x | youtu.be/dNUKmtATygA |
| S2 | TRUE OR FAKE IN ANIMAL HOSPITAL! (Part 2) (Roblox) | SKYROBLOX | 2.93M | 112.7x | youtu.be/ATxlaWDwf7M |
| S3 | You've Been Lied To About Rats 🐀 | TailsAndPawsDaily | 750k | 28.9x | youtu.be/4AIerBvcOmY |
| S4 | Animal Myths You Still Believe (But Are Wrong) | CritterTalks | 337k | 4.8x | youtu.be/AqBVBu0eAF4 |
| S5 | Animal Survival Myths That Could Get You in Trouble | Cryptic Facts | 104k | 11.4x | youtu.be/Fb_2xhmKDbo |
| S6 | Disney Lied To Us About Lion King 🦁 | rxy08zpdyy | 70.9k | 653x (tiny median) | youtu.be/WmWtZHnzuxg |
| S7 | JAWS WAS LYING | PrimateShorts | 51k | 3.2x | youtu.be/l3BvsN88Gto |
| S8 | 3 Animal Myths You STILL Believe 💀🐘🐋 | WildByte | 27.8k | 14.3x | youtu.be/9y9wPQ8sTDo |
| S9 | Animal Myths — Busted 🚫 | FactPaw Daily | 27.4k | 27.4x | youtu.be/adgmun4OIrY |
| S10 | This Famous Animal Fact Is Actually Wrong 🐭 | General Enlightenment | 10.9k | 10.1x | youtu.be/--1zeo-dNAs |
| S11 | 4 Animal Myths You Learned as a Kid — All Wrong! | Fact Fangs | 9.9k | 7.6x | youtu.be/TJmTUUrEGpc |
| S12 | 9 More Animal Myths That Are Completely Wrong 🤩 | Fact Chat | 7.1k | 228x (median 31) | youtu.be/F2GBeN-PIHw |

### C. Evergreen Shorts monsters (relevance search, age unknown, likely older)

These show which topics can scale. Lengths are measured from the Shorts pages **[M]**.

- *Animals With the Saddest Love Lives*, FactPaw: 36.6M views, 795x, 70 s.
- *5 Animals That Made the Dumbest Mistakes*, CritterTalks: 15.7M views, 224x, 87 s.
- *Fascinating Animal Facts You Didn't Know!*, FactPaw: 12.1M views, 264x, 58 s, uploaded 2025-01.
- *Top 4 Animals That Look FAKE But Are 100% Real*, CocoMode: 10.2M views, 58x, 53 s.
- *The Unluckiest Animals In The World 😭*, Infinite Fact: 8.8M views, 137x, 35 s.
- *Mind-Blowing Animal Facts (TRUE or FALSE⁉️)*, GVO Kids: 1.14M views, 57x, 94 s.

## 2. Patterns

### Title formulas (exact templates, counted from the tables) [M]

1. **`[N] Animal Myths You've Believed Your Whole Life`**. Two separate channels hit 46x and 54x with this near-identical title. The N is big (40 or 42).
2. **`Animal Lies (And Myths) That You Actually Believe - Part [N]`** and **`Weird Animal Facts You Never Knew - Part [N]`**. What Gives? alone has 7 entries, all 2.4x–9.7x, and the series is now at Part 10.
3. **`[Monsters / Mythical Creatures / Extinct Animals] That Really Existed / Might Still Be Alive`**. These have the biggest raw views in the niche: 1.0M, 1.6M, 1.9M, 2.5M.
4. **`You've Been Lied To About [Animal]`** and **`[Movie/Brand] Lied To Us About [Animal]`**. Examples are rats (750k), Lion King, JAWS and Animal Planet. "Lied" appears in 6 of the top-scoring Shorts.
5. **`[N] Animal Myths You STILL Believe [emoji]`** and **`... You Learned as a Kid — All Wrong!`**. The capitalised STILL recurs.
6. **`[Superlative] Animals In The World`**: Unluckiest, Saddest Love Lives, Dumbest Mistakes, Biggest Lies. These are the 8–37M-view Shorts.
7. **`TRUE or FALSE [Animal] Quiz`** / **`TRUE OR FAKE ...`**.
   - In long-form, this title works mainly for tiny or kids channels (high score, low raw views).
   - In Shorts, "TRUE OR FAKE" carried a 2.9M Roblox Short.
   - **[I]** Use "True or False" as the *hook format*. Put the *myth/lie promise* in the title, e.g. "... You STILL Believe (True or False?)".

### Thumbnails [I]

These are inferred from the titles and channel styles. The thumbnails themselves were not fetched.

- One shocked mascot or face, plus one animal photo, plus a red ✗ or "FALSE" stamp, plus 1–3 words ("LIES", "WRONG", "STILL?").
- "Really existed" videos show a monster silhouette next to a real photo.
- What Gives? and Slug hug use a cartoon or drawn style that is consistent across the whole series, so viewers recognise a series thumbnail instantly. This matches Kelevin's mascot + 2–3 big words (see `15`).

### Length [M]

- Recent long-form winners fall into two clusters:
  - **9:50–12:10**: What Gives? ×5, Myths-creature.
  - **30–110 min mega-compilations**: Oddly Factual, Lying Pie, Mysterious-Fact, Psychopoly.
- Our ~10–11 min sits in the proven cluster.
- Viral animal-fact Shorts ran 35–94 s. Our 45–90 s fits.
- **[I]** After about 6 episodes, stitch them into a "Full Series"/compilation upload. The 37-min Mysterious-Fact compilation scored 62.9x.

### Topic clusters that over-perform [M]

1. **"Real monsters"**: cryptids, mythical creatures that existed, extinct animals still alive. These get the highest raw views.
2. **General "myths you believed"** lists with a big N.
3. **Media lied to you**: Disney, Jaws, Animal Planet.
4. **Specific-animal myths**: rats, sharks, elephants, cats.
5. **Danger/survival myths**.
6. **Emotional superlatives**: unluckiest, saddest, dumbest.
7. **"Looks fake but is real"**.

### Series packaging [M]

- What Gives? numbers parts and keeps going (Part 1 → 10). Part 1 and Part 2 of "Animal Lies" are their best (11.3x and 8.2x), and later parts decay to about 2–4x.
- Mysterious-Fact and hollnes recut with "| Full Series" and "| Part-4".
- **[I]** "Part 2" works when Part 1 already won. Start a numbered series only after one episode outperforms.

### Competition [M]

- Most "true or false animal quiz" long-form results are kids/quiz channels with low views. Nobody in the scored set combines a mascot, jokes and a TRUE/FALSE countdown for adults.
- The adult myth channels (What Gives?, Lying Pie, Oddly Factual) are narration lists with no interactive game.
- **[I]** That combination is our open lane.

## 3. Next 15 episodes (ranked)

Each episode has ~10–12 myths. T/F answers are given in brackets. Verify each myth during scripting.

1. **"Animal 'Facts' From School That Are Completely WRONG"** (clusters 2 and 5; the 46x and 54x formula).
   - Myths: bats are blind [F]; chameleons change colour to hide [F, mostly mood/temperature]; ostriches bury their heads [F]; goldfish have 3-second memory [F]; bulls hate red [F]; lemmings jump off cliffs [F, the footage was staged]; camels store water in humps [F]; porcupines shoot quills [F]; touch a baby bird and mum rejects it [F]; daddy longlegs are the most venomous [F]; elephants never forget [mostly T]; owls spin heads 360° [F].
2. **"Disney & Jaws Lied To You About These Animals"** (Lion King 653x, JAWS WAS LYING, Animal Planet).
   - Myths: hyenas only scavenge [F]; male lions do the hunting [F]; Nemo's dad would turn female [T]; great whites hunt humans/hold grudges [F]; elephants love peanuts [F]; elephants fear mice [F]; rats are filthy [F, they groom constantly]; Bambi's deer mums stay with fawns [F, they leave them hidden]; foxes and hounds stay friends... reframe it as an "animals can form cross-species friendships" myth [T]; pandas are vegetarians by design [F, carnivore gut].
3. **"Monsters That Turned Out To Be REAL — True or False?"** (cluster 1, 1–2.5M views).
   - Myths: the giant squid is real [T]; the kraken was a real animal [T, giant/colossal squid]; megalodon still lives [F]; the "sea serpent" was the oarfish [T]; dragons existed [T-ish, the Komodo dragon]; unicorns walked the earth [T, Elasmotherium]; Bigfoot was a real ape [T, Gigantopithecus, extinct]; mermaids = manatees [T, sailor sightings]; the Loch Ness monster is a plesiosaur [F]; the chupacabra = mangy coyotes [T].
4. **"Extinct Animals That Are Secretly Still Alive"** (32.8x, 1.64M).
   - Myths: the coelacanth came back [T]; the takahe was rediscovered [T]; the Lord Howe stick insect was found again [T]; a Fernandina giant tortoise was found in 2019 [T]; the Chacoan peccary was known from fossils first [T]; the Tasmanian tiger is confirmed alive [F]; the dodo survived somewhere [F]; the Bermuda petrel was rediscovered [T]; the ivory-billed woodpecker is confirmed [F, disputed]; the woolly mammoth is still alive [F, but lived until about 4,000 years ago, T].
5. **"Shark Myths That Could Get You Killed"** (Wilder TCG, JAWS, sharks cluster).
   - Myths: sharks smell a drop of blood a mile away [F]; sharks must swim or die [some T]; sharks never get cancer [F]; punch a shark's nose [partly T]; cows kill more people than sharks [T]; dolphins protect swimmers [F]; sharks are older than trees [T]; sharks have bones [F]; sharks are mindless eating machines [F]; there are freshwater sharks [T, bull shark].
6. **"Animal Survival Myths That Could Get You Killed"** (S5, 11.4x).
   - Myths: pee on a jellyfish sting [F]; play dead for every bear [F]; suck out snake venom [F]; zig-zag to escape a crocodile [F]; make yourself big vs a cougar [T]; quicksand will drown you [F]; jump in water to escape bees [F]; moose injure more people than bears in Alaska [T]; hippos are the deadliest big land animal [T]; a rattlesnake always rattles first [F].
7. **"You've Been Lied To About Rats & Mice"** (S3, 750k).
   - Myths: rats alone spread the Black Death [F, fleas/humans]; mice love cheese [F]; rats can't vomit [T]; rats laugh when tickled [T]; NYC has more rats than people [F]; rats can tread water for days [T]; rats free trapped friends [T]; mice sing to each other [T]; pigeons are "rats with wings" disease bombs [mostly F]; rats are colour-blind loners [F].
8. **"Cat & Dog Myths You STILL Believe"** (cat/dog cluster, S11).
   - Myths: dogs see in black and white [F]; cats always land on their feet [F]; 1 dog year = 7 human years [F]; cats should drink milk [F]; a dog's mouth is cleaner than yours [F]; purring = happy [F]; tail wag = friendly [F]; dogs sweat by panting [F, paw pads]; all cats hate water [F]; a warm dry nose = a sick dog [F].
9. **"Animals That Look FAKE But Are 100% Real — True or False?"** (10.2M Short, Slug hug "so weird I had to animate them").
   - Myths: the mantis shrimp punch boils water [T]; axolotls regrow parts of their brain [T]; tardigrades survive space [T]; wombats poop cubes [T]; the platypus glows under UV [T]; one jellyfish is immortal [T]; the pistol shrimp is louder than a gunshot [T]; a lizard squirts blood from its eyes [T]; snails can sleep 3 years [F, exaggerated]; the "hairy frog" breaks its own bones for claws [T].
10. **"The Unluckiest Animals On Earth — True or False?"** (8.8–36.6M Shorts).
    - Myths: turkeys drown looking up at rain [F]; an ostrich's eye is bigger than its brain [T]; male anglerfish fuse to females [T]; male honeybees die after mating [T]; mayflies live one day [T for adults]; the kiwi egg is about 20% of mum's body [T]; pandas are "too dumb to breed" [F]; koalas don't recognise leaves off the branch [viral, debated, an F-ish twist]; the dodo was stupid [F]; sloths mistake their arm for a branch [anecdotal].
11. **"Animal Myths Your Grandparents Believed"** (S12 "Old Wives' Tales", S11).
    - Myths: cows lie down before rain [F]; toads give you warts [F]; cats steal babies' breath [F]; the groundhog predicts spring [F]; bats tangle in your hair [F]; snakes hypnotise prey [F]; bread is good for ducks [F]; rice makes birds explode [F]; earwigs crawl into ears [F]; a dog eats grass when sick [F].
12. **"Which Animal Is ACTUALLY Deadliest?"** (danger cluster).
    - Myths: the mosquito is the deadliest [T]; piranhas strip a cow in seconds [F]; a black widow bite usually kills [F]; orcas attack humans in the wild [F]; the cassowary is dangerous [T]; coconuts kill 150 a year [F]; tarantulas are deadly [F]; the box jellyfish can kill in minutes [T]; the hippo kills more than lions [T]; snakes chase people [F].
13. **"Ocean Myths Everyone Gets Wrong"**.
    - Myths: the octopus has 3 hearts [T]; starfish are fish [F]; whales spout water [F]; seahorse dads give birth [T]; dolphins sleep with half a brain [T]; a blue whale's heart is the size of a car [F, golf-cart size]; sea otters hold hands [T]; goldfish grow to the size of their bowl [F]; jellyfish have no brain [T]; sharks are fish but dolphins aren't [T].
14. **"Bird Myths Busted"**.
    - Myths: swans can break your arm [F]; penguins mate for life [mostly F]; hummingbirds ride on geese [F]; flamingos are pink from food [T]; crows remember faces [T]; vultures circle the dying [F]; a duck's quack doesn't echo [F]; owls are wise [F, average]; parrots understand words [partly T]; birds sleep in nests [F, mostly not].
15. **"Bug & Spider Myths You Swallowed (Literally)"**.
    - Myths: you swallow 8 spiders a year [F]; honeybees die after stinging you [T]; a worm cut in half = 2 worms [F]; cockroaches survive nukes [partly T]; flies live 24 hours [F]; ants lift 50x their weight [T]; moths eat clothes [F, larvae do]; spiders are insects [F]; daddy longlegs are spiders [F, harvestmen]; fireflies glow to attract mates [T].

**Why this order [I].**
- 1–4 copy the formulas with the most repeated wins (the same title won on 2 channels; "real monsters" has the biggest raw views).
- 5–8 are single-animal "lied to" angles proven in 2026 Shorts.
- 9–10 repackage the biggest-ever Shorts superlatives as a quiz.
- 11–15 are solid but less directly measured.
- After 6 episodes, publish "60 Animal Myths You've Believed Your Whole Life | Full Series".

## 4. Ten Short title templates (TRUE-or-FALSE hook)

1. `True or False: [Myth]? 🤔` (e.g. "True or False: Bats Are Blind?")
2. `You've Been Lied To About [Animal] 🐀 (True or False?)`
3. `[Movie] Lied To You About [Animal] 🦁`
4. `[Myth] — TRUE or FALSE? (Most People Get This Wrong)`
5. `This Famous [Animal] Fact Is Actually FALSE ❌`
6. `You STILL Believe This [Animal] Myth 💀`
7. `Can [Animal] Really [Claim]? TRUE or FALSE`
8. `The Unluckiest Animal Myth: TRUE or FALSE? 😭`
9. `This Animal Looks FAKE — Real or Fake? 🤯`
10. `[Myth] Could Get You Killed — TRUE or FALSE?`

Templates 2, 3, 5, 6, 8, 9 and 10 mirror measured 2026 winners (S1–S11, C). Templates 1, 4 and 7 adapt the "TRUE OR FAKE" Short (S2) and GVO Kids (57x) **[I]**.

Raw data: the scratchpad files `rlong.json`, `rshort.json` and `merged.json` from this session (not kept in the repo).
