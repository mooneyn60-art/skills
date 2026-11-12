export const meta = {
  name: 'shorts-batch',
  description: 'Build a batch of Meatball Myths Shorts and TikTok cuts from picked topics: fact pack, script pair, second-model check, render with voice check, lint. Nothing is scheduled or committed.',
  whenToUse: 'After topics are picked from research (oh-meatball/research/data/95-topic-queue.csv or a newer queue). Pass args {topics:[{slug, family, topic, searched_phrase, fact, source_url, second_fact, do_not_say, gag_idea, series_no}]}. The main session then looks at the sheets, commits, schedules and logs (make-short skill, steps 7-9).',
  phases: [
    { title: 'Facts', detail: 'one sourced fact pack per topic', model: 'sonnet' },
    { title: 'Script', detail: 'YouTube spec and TikTok spec per topic' },
    { title: 'Check', detail: 'a different model reads every line against the sources', model: 'opus' },
    { title: 'Build', detail: 'render, voice check, contact sheet, lint', model: 'sonnet' },
  ],
}

// How to run: Workflow({ scriptPath: '/home/user/skills/.claude/workflows/shorts-batch.js', args: { topics: [...] } })
// Why these stages: MASTER_ORDERS "The production line", "Make them funnier" rules 1-5, "Direction change"
// script rules 1-7, "Tags and everything" standard 1-6. Each stage exists because skipping it once put a
// wrong or stale video in the queue.

const OM = '/home/user/skills/skills/oh-meatball'
const topics = (args && args.topics) || []
if (!topics.length) { throw new Error('pass args {topics:[...]} (see meta.whenToUse)') }

const RULES = `
HARD RULES (every agent):
- Repo /home/user/skills. NEVER run a git command that changes anything (no add, commit, checkout, restore, reset, stash, apply, clean, rm, mv, sparse-checkout, worktree, clone). Read-only git is fine. The main session commits.
- Write only the files named as yours for YOUR topic slug. Other agents work on other slugs at the same moment. Scratch files go under /dev/shm/<slug>/.
- No Metricool tools, no vidIQ tools, no YouTube watch pages (yt-dlp --flat-playlist only), never disable TLS or unset HTTPS_PROXY.
- Read /home/user/skills/skills/channel-brain/MASTER_ORDERS.md first (one Read). Its rules win over this prompt. Then /home/user/skills/.claude/skills/make-short/SKILL.md and its references/spec.md.
- Plain words, short sentences, no em dashes in anything written into the repo. Every number carries its source.
`

const FACTS = { type: 'object', properties: {
  slug: { type: 'string' }, ok: { type: 'boolean' }, pack_path: { type: 'string' },
  hook_facts: { type: 'array', items: { type: 'string' } }, do_not_say: { type: 'array', items: { type: 'string' } },
  sources: { type: 'array', items: { type: 'string' } }, problems: { type: 'array', items: { type: 'string' } },
}, required: ['slug', 'ok', 'pack_path', 'hook_facts', 'do_not_say', 'sources', 'problems'] }

const SCRIPT = { type: 'object', properties: {
  slug: { type: 'string' }, ok: { type: 'boolean' }, yt_spec: { type: 'string' }, tt_spec: { type: 'string' },
  yt_title: { type: 'string' }, yt_lines: { type: 'array', items: { type: 'string' } }, tt_lines: { type: 'array', items: { type: 'string' } },
  lint: { type: 'string' }, notes: { type: 'array', items: { type: 'string' } },
}, required: ['slug', 'ok', 'yt_spec', 'tt_spec', 'yt_title', 'yt_lines', 'tt_lines', 'lint', 'notes'] }

const CHECK = { type: 'object', properties: {
  slug: { type: 'string' }, cleared: { type: 'boolean' },
  changes: { type: 'array', items: { type: 'object', properties: {
    where: { type: 'string' }, old: { type: 'string' }, new: { type: 'string' }, why: { type: 'string' } },
    required: ['where', 'old', 'new', 'why'] } },
  blocked_reason: { type: 'string' }, lint: { type: 'string' }, check_path: { type: 'string' },
}, required: ['slug', 'cleared', 'changes', 'blocked_reason', 'lint', 'check_path'] }

const BUILD = { type: 'object', properties: {
  slug: { type: 'string' }, ok: { type: 'boolean' },
  yt_mp4: { type: 'string' }, yt_seconds: { type: 'number' }, yt_voice: { type: 'string' }, yt_lint: { type: 'string' }, yt_sheet: { type: 'string' },
  tt_mp4: { type: 'string' }, tt_seconds: { type: 'number' }, tt_voice: { type: 'string' }, tt_lint: { type: 'string' }, tt_sheet: { type: 'string' },
  looked: { type: 'array', items: { type: 'string' } }, problems: { type: 'array', items: { type: 'string' } },
}, required: ['slug', 'ok', 'yt_mp4', 'yt_seconds', 'yt_voice', 'yt_lint', 'yt_sheet', 'tt_mp4', 'tt_seconds', 'tt_voice', 'tt_lint', 'tt_sheet', 'looked', 'problems'] }

const brief = t => `TOPIC (${t.family}): ${t.topic}
slug: ${t.slug}   series number: ${t.series_no}
searched phrase (word for word from a search suggestion): ${t.searched_phrase}
fact the research confirmed: ${t.fact}
source: ${t.source_url}
second fact: ${t.second_fact}
do not say: ${t.do_not_say}
gag idea for line 2: ${t.gag_idea}`

const factsPrompt = t => `You are writing the fact pack for one Meatball Myths Short. Your label: facts-${t.slug}.
${RULES}
${brief(t)}

YOUR FILE: ${OM}/research/facts/${t.slug}.md (new). Pattern to follow: one topic section of ${OM}/research/84-pets-and-survive-factpack.md (read its section 0 and one section).
DO:
1. Open the primary source yourself (the paper, the agency or park service page, the vet school page). Open at least one more independent primary source. A news write-up is not a source. If a page will not open, say so and find the same fact on another primary page.
2. Write 6 to 10 fact rows: id (${t.slug.toUpperCase().replace(/-/g, '').slice(0, 4)}1, 2, ...), the fact in the shortest wording that is still true, the exact quoted sentence, the URL, and what the number is a share of or the condition it needs. A percentage needs what it is a share of. A survival figure needs the count. A safety line needs the trigger a viewer can act on, and comes from an agency.
3. "Three hook facts": the three strongest, each with its number.
4. "Do not say": the tempting overstatements (cause where the study shows a link, "all" where it is "most", an animal's feeling or motive, a single speed or distance where agencies differ).
5. "Shortened-claim traps": wordings that become false when cut to five words.
6. "Disagreements between sources" and "Could not open".
ok is false if the main fact cannot be confirmed from a primary source today; then say why in problems and write the pack anyway with what you found.`

const scriptPrompt = (t, f) => `You are the script writer for one Meatball Myths Short and its TikTok cut. Your label: script-${t.slug}. You write only from the fact pack.
${RULES}
${brief(t)}
FACT PACK: ${f.pack_path} (read it in full). Hook facts: ${JSON.stringify(f.hook_facts)}. Do not say: ${JSON.stringify(f.do_not_say)}.

YOUR FILES: ${OM}/scripts/drawn-house/${t.slug}-v6-yt.json and ${OM}/scripts/drawn-house/tts-${t.slug}.json (new).
TEMPLATES: copy the structure of the newest pair of the same family. Pets: cat-sugar-v6-yt.json and tts-cat-sugar.json, or dog-guilty-look-v6-yt.json and tts-dog-guilty-look.json. Survival: grizzly-wms-v6-yt.json and tts-grizzly-wms.json, or moose-wms-v6-yt.json and tts-moose-wms.json. Read both files of the pair, and the docstring at the top of ${OM}/tools/drawn.py for the spec keys (creatures, scenes, macros, gags, cards). Use only scenes, props and spec keys that exist in the tools (check tools/drawn_creatures.py, drawn_habitats.py, drawn_gags.py, drawn_macros.py). A new animal is defined in stage.creature_cfg with a plan (mammal, bird, reptile, fish ...) and only the keys that plan's code reads: the header of tools/drawn_creatures.py lists them (mammal extras include hump, horns, beard, antlers, mane_line, spots), and grizzly-wms-v6-yt.json shows a big mammal (stage s about 0.85 with open_zoom 1.55 so it does not look dog-sized). Never invent a key; if the animal cannot be drawn with the existing keys, say so in notes.
RULES OF THE SCRIPT (all in MASTER_ORDERS; these are the ones writers break):
- "Make them funnier", rules 1-5: the hook is the fact with the searched words in the first spoken sentence; line 2 is a Meatball gag DRAWN on screen with a prop or a card; every later fact line is the joke or is followed by one; at least two sourced facts; jokes are on Meatball, never on the viewer or a group, and never add a number, a danger or health claim, an animal's feeling or motive, or a safety instruction; hedges stay ("probably", "likely", "may", "in one small study").
- "Direction change", the seven rules for pet and survival scripts (hedge on "your cat/dog" plus a lab result; no feeling or motive in a reaction; a safety card carries its condition; no single bear speed or spray distance; counts say "confirmed" and the year; no ending says a tactic saved Meatball).
- Voice traps: write "his cat" and "his dog" in full, "let out a meow" not "meowed".
- YouTube cut: 16 to 20 seconds when rendered (about 42 to 52 spoken words; the cat-sugar cut is the yardstick), one or two mild words only (damn, hell, ass, dumbass, badass, bastards), no strong word anywhere. At least three rooms; the first and last line share a room so it loops; no outro.
- TikTok cut: 20 to 26 seconds, the same facts, about one swear a line as a reaction (fuck, fucking, shit lead), attributions and safety instructions said clean with the reaction after, never "you" in an insult, cap_swap has an entry for every strong spelling used, search_top shows the searched phrase for the first 2 to 2.5 seconds at y 150.
- Each beat that states a fact carries "_f" with the fact ids from the pack. "sources" lists the URLs. "_note" says what was left out and why.
- Pets have names (MASTER_ORDERS "What he picked to build next"): Meatball's dog is Noodle, his cat is Sauce. Say "his dog Noodle" or "his cat Sauce" the first time, then the name. Running gag, always an action on screen: Sauce does the opposite of what Meatball wants and walks off; Noodle ends up with Meatball's food.
- Built to be answered (MASTER_ORDERS "Previews and engagement", rules 1-4): the last spoken line hands the viewer one open, personal question and runs into the hook ("What's the worst thing your dog got out of the trash? And"); the same question is the corner pill and the pinned comment; the TikTok caption ends on a quick pick and may carry one share line ("Send this to whoever feeds the dog under the table."). Survival endings keep "Meatball lived. Nothing's guaranteed." before the question.
${t.use_pack ? `- PACK LIMITS set by the main session: ${t.use_pack.note}` : ''}
TEXT (follow /home/user/skills/.claude/skills/post-metadata/SKILL.md): run python3 tools/postkit.py kw with two seeds from ${OM} for the searched words. YouTube title: searched words in the first 40 characters, hedge kept, one odd fact, one emoji, series tag last: "(Things Living In Your House #${t.series_no})" for pets or "(Would Meatball Survive? #${t.series_no})" for survival, 100 UTF-16 units at most, statement form, no banned word (TRUE or FALSE, Myth, Believe, Cartoons, Lied, Did you know). Description: first sentence is the searched question, then the checked facts, four hashtags (two topic, #meatballmyths, #shorts last), a Sources line (survival adds "General information, not safety training."). Tags: 8 to 12 suggestion phrases, each 30 characters or fewer, each answered by the video. pinned_comment: one open question. TikTok caption: the on-screen phrase, the fact with its condition, the gag in the video's words without swearing, a question, five topic hashtags (no #fyp, no #learnontiktok, no brand tag; survival adds "General info, not safety training.").
THEN run from ${OM}: python3 tools/postkit.py lint scripts/drawn-house/${t.slug}-v6-yt.json and the same for tts-${t.slug}.json. Fix until both print "=> pass" with 0 fail; give a reason for any WARN in the spec's _note. Return the spoken lines of both cuts, the title, the last lint lines, and notes (anything you were unsure of).`

const checkPrompt = (t, f, s) => `You are the second model. You check one script pair before it is rendered, against the live sources. You did not write it. Your label: check-${t.slug}. Default to changing a line when the source does not carry it.
${RULES}
${brief(t)}
FACT PACK: ${f.pack_path}. SPECS: ${s.yt_spec} and ${s.tt_spec}. Pattern of a good check: ${OM}/research/92-factcheck-funnier-cuts.md.
YOUR FILES: the two specs (wording fixes only) and ${OM}/research/facts/${t.slug}-check.md (new; on a second pass add a section "Second pass" at the end and keep what is there).${t.recheck ? `
SECOND PASS: these specs were checked once already (read the check file). The main session then changed this: ${t.recheck.changed} Judge the changed wording hardest (does a name, a question or a cut line add or lose a claim, a condition or a credit?), then read the rest once more as in step 2. If the cut gets too long for its limit (YouTube 20.05 s, TikTok 26 s) that is the builder's report, not yours.` : ''}
DO:
1. Open the primary sources yourself. The checker opens the paper, not the pack. Confirm every number, what it is a share of, and every condition.
2. Read every spoken line of both cuts, every card and search_top row, the title, the description, every tag, the pinned comment and the TikTok caption. For each: is it carried by a source as worded? Does a joke add a number, a danger or health claim, an animal's feeling or motive, or a safety instruction? Is a hedge missing? Does a tag or title promise something the video does not give? Does a safety line keep its condition? Is an insult aimed at the viewer? Are attributions and safety instructions clean on TikTok? Does the first spoken sentence hold the searched words?
3. Fix each problem in the spec with the smallest change that makes it true, keeping it funny where you can. List every change (where, old, new, why). Do not rewrite lines that are fine.
4. Run from ${OM}: python3 tools/postkit.py lint on both specs; they must pass with 0 fail after your changes.
5. Write the check file: verdict first, then the table of changes, then what you could not verify.
cleared is true only if, after your changes, you would stake the channel's name on every claim. If the main fact itself does not hold, set cleared false and say why in blocked_reason; change nothing else.`

const buildPrompt = (t, s) => `You are building one Short and its TikTok cut from checked specs. Your label: build-${t.slug}. You do not change wording: if a line must change, stop and report it.${t.recheck ? ' This is a re-render after a wording change: the old mp4s and sheets are replaced. If a cut runs over its limit (YouTube 20.05 s, TikTok 26 s), try shorter pads first (spec key pad, layout only), then report the seconds; never cut a word.' : ''}
${RULES}
SPECS: ${s.yt_spec} and ${s.tt_spec}.
YOUR FILES: ${OM}/episodes/drawn-house/yt-${t.slug}-v6.mp4 and ${OM}/episodes/drawn-house/tts-${t.slug}.mp4 (new), and layout-only keys in the two specs (pad, _note, card position, scene or stage numbers) when a cut runs long or a card is covered.
DO, from ${OM}, one cut after the other:
1. python3 tools/postkit.py render scripts/drawn-house/${t.slug}-v6-yt.json episodes/drawn-house/yt-${t.slug}-v6.mp4 --work /dev/shm/${t.slug}-yt
   A pass is exit 0 and the line "ok every line heard to its end". On FAIL render once more (the voice service drops words at random). If the same line fails twice, do NOT reword it: report the line in problems.
2. Read the contact sheet the render printed (an image): the animal is on screen from frame 0; the line-2 gag is visible; cards are readable and inside the frame; captions do not sit on a card; the last frame is back in the first room. On the TikTok cut also: the search phrase is on screen at the start and not covered; captions show the softened spellings (SH*T, F**K), never the bare word.
3. python3 tools/postkit.py lint scripts/drawn-house/${t.slug}-v6-yt.json --mp4 episodes/drawn-house/yt-${t.slug}-v6.mp4 : YouTube must be 16.0 to 20.05 s. If it is long, trim pads (0.2 to 0.35 s) before cutting anything, render again and re-check. Never cut a fact or a hedge to make length; report it.
4. The same three steps for tts-${t.slug}.json into episodes/drawn-house/tts-${t.slug}.mp4 with --work /dev/shm/${t.slug}-tt (20 to 26 s).
5. Copy both sheets to ${OM}/episodes/drawn-house/sheets/${t.slug}-yt.jpg and ${t.slug}-tt.jpg (make the folder if missing).
Return the paths, the seconds, the voice-check result line and the lint result line of each cut, what you saw on each sheet, and every problem. ok is true only if both cuts passed the voice check and lint with 0 fail and the sheets show nothing wrong.`

const results = await pipeline(
  topics,
  t => {
    // recheck: the main session edited checked specs (names, a new last line); go straight to Check and Build.
    if (t.recheck) return { slug: t.slug, ok: true, pack_path: t.recheck.pack_path, hook_facts: [], do_not_say: [], sources: [], problems: [] }
    // use_pack: the main session read a partly confirmed pack and accepts it within the limits it names.
    if (t.use_pack) return { slug: t.slug, ok: true, pack_path: t.use_pack.pack_path, hook_facts: t.use_pack.hook_facts || [], do_not_say: t.use_pack.do_not_say || [], sources: [], problems: [t.use_pack.note || ''] }
    return agent(factsPrompt(t), { label: `facts:${t.slug}`, phase: 'Facts', model: 'sonnet', schema: FACTS })
  },
  (f, t) => {
    if (!f || !f.ok) { log(`${t.slug}: fact pack did not confirm the main fact; stopped`); return null }
    if (t.recheck) return { f, s: { slug: t.slug, ok: true, yt_spec: t.recheck.yt_spec, tt_spec: t.recheck.tt_spec } }
    return agent(scriptPrompt(t, f), { label: `script:${t.slug}`, phase: 'Script', schema: SCRIPT }).then(s => (s && s.ok ? { f, s } : null))
  },
  (fs, t) => {
    if (!fs) return null
    return agent(checkPrompt(t, fs.f, fs.s), { label: `check:${t.slug}`, phase: 'Check', model: 'opus', schema: CHECK }).then(c => ({ ...fs, c }))
  },
  (x, t) => {
    if (!x) return null
    if (!x.c || !x.c.cleared) { log(`${t.slug}: the check did not clear it (${x.c ? x.c.blocked_reason : 'no result'}); not built`); return { slug: t.slug, facts: x.f, script: x.s, check: x.c, build: null } }
    return agent(buildPrompt(t, x.s), { label: `build:${t.slug}`, phase: 'Build', model: 'sonnet', schema: BUILD })
      .then(b => ({ slug: t.slug, facts: x.f, script: x.s, check: x.c, build: b }))
  },
)

const done = results.filter(Boolean)
log(`built ${done.filter(r => r.build && r.build.ok).length} of ${topics.length}; the main session now looks at the sheets, commits, schedules and logs`)
return { results: done, dropped: topics.filter((t, i) => !results[i]).map(t => t.slug) }
