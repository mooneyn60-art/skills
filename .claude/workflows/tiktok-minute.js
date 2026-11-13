export const meta = {
  name: 'tiktok-minute',
  description: 'Build Meatball Myths TikTok cuts that run over one minute (65 to 90 s): facts if needed, script, second-model check, render with voice check, lint. Nothing is scheduled or committed.',
  whenToUse: 'Nolan 11/12: every TikTok runs over 1 minute. Pass args {topics:[{slug, family, topic, searched_phrase, packs:[paths] (or omit to have a pack written), short_spec (the checked 20 to 26 s cut of the same topic, if one exists), template (tt-dog-guilty-look.json for pets, tt-grizzly-wms.json for survival), do_not_say, gag_idea}]}. Two topics at a time at most (careful on credits). The main session then looks at the sheets, sends the previews, commits, schedules and logs.',
  phases: [
    { title: 'Facts', detail: 'only for a topic with no fact pack', model: 'sonnet' },
    { title: 'Script', detail: 'one TikTok spec, 65 to 90 seconds' },
    { title: 'Check', detail: 'a second model against the live sources', model: 'opus' },
    { title: 'Build', detail: 'render, voice check, sheet, lint', model: 'sonnet' },
  ],
}

const OM = '/home/user/skills/skills/oh-meatball'
const topics = (args && args.topics) || []
if (!topics.length) { throw new Error('pass args {topics:[...]} (see meta.whenToUse)') }
if (topics.length > 2) { log(`${topics.length} topics passed; the rule is two at a time (careful on credits). Running them in order, two at a time.`) }

const RULES = `
HARD RULES (every agent):
- Repo /home/user/skills. NEVER run a git command that changes anything (no add, commit, checkout, restore, reset, stash, apply, clean, rm, mv, sparse-checkout, worktree, clone). Read-only git is fine. The main session commits.
- Write only the files named as yours for YOUR topic slug. Scratch files go under /dev/shm/<slug>-min/.
- No Metricool tools, no vidIQ tools, no YouTube watch pages (yt-dlp --flat-playlist only), never disable TLS or unset HTTPS_PROXY.
- Read /home/user/skills/skills/channel-brain/MASTER_ORDERS.md first (one Read). Its rules win over this prompt. Then /home/user/skills/.claude/skills/make-short/SKILL.md and its references/spec.md.
- Plain words, short sentences, no em dashes in anything written into the repo. Every number carries its source.
- Be careful on credits: do the job in as few steps as it takes, no side research.
`

const brief = t => `TOPIC (${t.family}): ${t.topic}
slug: ${t.slug}
searched phrase (word for word from a search suggestion): ${t.searched_phrase}
fact packs: ${(t.packs || []).join(', ') || '(none yet: the Facts stage writes one)'}
the checked short cut of this topic: ${t.short_spec || '(none)'}
template (a checked one-minute sweary cut): ${OM}/scripts/drawn-house/${t.template || 'tt-dog-guilty-look.json'}
do not say: ${t.do_not_say || '(see the pack)'}
gag: ${t.gag_idea || '(keep the short cut\'s gag)'}`

const FACTS = { type: 'object', properties: {
  slug: { type: 'string' }, ok: { type: 'boolean' }, pack_path: { type: 'string' },
  problems: { type: 'array', items: { type: 'string' } },
}, required: ['slug', 'ok', 'pack_path', 'problems'] }

const SCRIPT = { type: 'object', properties: {
  slug: { type: 'string' }, ok: { type: 'boolean' }, spec: { type: 'string' },
  lines: { type: 'array', items: { type: 'string' } }, planned_seconds: { type: 'number' },
  lint: { type: 'string' }, notes: { type: 'array', items: { type: 'string' } },
}, required: ['slug', 'ok', 'spec', 'lines', 'planned_seconds', 'lint', 'notes'] }

const CHECK = { type: 'object', properties: {
  slug: { type: 'string' }, cleared: { type: 'boolean' },
  changes: { type: 'array', items: { type: 'object', properties: {
    where: { type: 'string' }, old: { type: 'string' }, new: { type: 'string' }, why: { type: 'string' } },
    required: ['where', 'old', 'new', 'why'] } },
  blocked_reason: { type: 'string' }, lint: { type: 'string' }, check_path: { type: 'string' },
}, required: ['slug', 'cleared', 'changes', 'blocked_reason', 'lint', 'check_path'] }

const BUILD = { type: 'object', properties: {
  slug: { type: 'string' }, ok: { type: 'boolean' }, mp4: { type: 'string' }, seconds: { type: 'number' },
  voice: { type: 'string' }, lint: { type: 'string' }, sheet: { type: 'string' },
  looked: { type: 'array', items: { type: 'string' } }, problems: { type: 'array', items: { type: 'string' } },
}, required: ['slug', 'ok', 'mp4', 'seconds', 'voice', 'lint', 'sheet', 'looked', 'problems'] }

const factsPrompt = t => `You are writing the fact pack for one Meatball Myths TikTok cut that runs over a minute. Your label: facts-${t.slug}.
${RULES}
${brief(t)}

YOUR FILE: ${OM}/research/facts/${t.slug}.md (new, or add rows to it if it exists). Pattern: one topic section of ${OM}/research/84-pets-and-survive-factpack.md (read its section 0 and one section).
A one-minute cut needs more than a Short: write 10 to 14 fact rows (id, the fact in the shortest true wording, the exact quoted sentence, the URL, what a number is a share of or the condition it needs). Open the primary sources yourself (the paper, the agency or park page, the vet school page); a news write-up is not a source. Start from the sources already named in the short cut's spec ("sources" key) and open them again. Then: three hook facts, "Do not say", "Shortened-claim traps", "Disagreements between sources", "Could not open". A safety line comes from an agency and keeps the trigger a viewer can act on.
ok is false if the main fact cannot be confirmed from a primary source today; say why in problems.`

const scriptPrompt = (t, f) => `You are the script writer for one Meatball Myths TikTok cut that runs OVER ONE MINUTE. Your label: script-${t.slug}. You write only from the fact packs.
${RULES}
${brief(t)}
FACT PACKS TO USE: ${[...(t.packs || []), f && f.pack_path].filter(Boolean).join(', ')} (read the section for this topic in full; a number that is not in a pack is not in the script).

WHY: Nolan 11/12: "make sure Tik toks are over 1 min long" and "I lowkey like the TikTok previews". TikTok Rewards pays only on videos of a minute or more, and the drawn accounts that break out run long (research 97). So this is the funny short cut he liked, grown to 65 to 90 seconds: the same voice, more facts, more jokes.

YOUR FILE: ${OM}/scripts/drawn-house/tt-${t.slug}.json (new; if a file of that name exists, read it and say so in notes before replacing it). Copy the structure of the template spec. Read the docstring at the top of ${OM}/tools/drawn.py for the spec keys and use only scenes, props and keys that exist (tools/drawn_creatures.py, drawn_habitats.py, drawn_gags.py, drawn_macros.py).

RULES FOR THE CUT (MASTER_ORDERS: "TikTok orders", "Make them funnier", "Direction change" rules 1 to 7, "Previews and engagement", "What he picked to build next", "Tags and everything"):
- Length 65 to 90 seconds when rendered (plan it with the drawn.py plan mode; under 62 seconds is a fail). About 180 to 260 spoken words.
- The first spoken sentence is the searched question, word for word, and the search phrase is on screen for the first 2 to 2.5 seconds (spec key search_top, at y 150). Frame 0 is the animal close up, already moving.
- Funny first: line 2 is a Meatball gag acted out on screen with a prop or a card. After that every fact line is the joke or is followed by one. Six to nine sweary jokes (a simile, a roast of Meatball, an order, a looks-like line the fact answers). Jokes are on Meatball, never on the viewer or a group, and never add a number, a danger or health claim, an animal's feeling or motive, or a safety instruction.
- Swearing: about one swear a line as a reaction (fuck, fucking and shit lead; damn, ass, bastard, badass, bullshit for variety). A sourced credit ("the AKC says", "in one study") and a safety instruction are said clean, with the reaction after. Never "you" in an insult. A line that names a group of people stays clean. cap_swap has an entry for every strong spelling used.
- Hedges stay ("probably", "likely", "may", "in one small study"). "Your cat" or "your dog" plus a lab result needs one. A safety card carries its condition on the card.
- Names: Meatball's dog is Noodle, his cat is Sauce. Write "his dog, Noodle" or "his cat, Sauce" the first time (with the comma), then the name. Running gag as an action on screen: Sauce does the opposite of what Meatball wants and walks off; Noodle ends up with Meatball's food.
- A new fact or picture every second or two, a cut every 1.5 to 2.5 seconds, at least four locations, a re-hook near the middle ("and it gets weirder"), no spoken outro (no follow, no part two).
- The last line hands the viewer one open, personal question and runs into the hook (the loop). The same question is the corner pill.
- Text: tiktok_title (clean), tiktok_caption = the searched phrase, the main fact with its condition, the gag in the video's words without the swearing, one share line ("Send this to ..."), a quick-pick question, five topic hashtags (no #fyp, no #learnontiktok, no brand tag; survival adds "General info, not safety training."). Also keep title, description and sources keys as the template has them, filled for this topic.
- Keep the short cut's checked wording where it still fits; every new line cites its fact ids in "_f".

THEN: run from ${OM}: python3 tools/postkit.py lint on your spec (0 fail). Plan or scratch-render it under /dev/shm/${t.slug}-min/ to get the length.
Return the spec path, every spoken line in order, the planned seconds, the lint result line and notes (what you were unsure about, each with the line and a fallback wording). ok is false if you could not reach 65 seconds from the packs without padding or repeating: say which facts are missing.`

const checkPrompt = (t, f, s) => `You are the second model. You did not write this script. Your label: check-${t.slug}.
${RULES}
${brief(t)}
SPEC: ${s.spec}. FACT PACKS: ${[...(t.packs || []), f && f.pack_path].filter(Boolean).join(', ')}. Pattern of a good check: ${OM}/research/92-factcheck-funnier-cuts.md.
YOUR FILES: the spec (wording fixes only) and ${OM}/research/facts/${t.slug}-min-check.md (new).
DO:
1. Open the primary sources yourself (the checker opens the paper or the agency page, not the pack). Confirm every number, what it is a share of, and every condition.
2. Read every spoken line, every card and the search_top row, the tiktok_title and the tiktok_caption. For each: is it carried by a source as worded? Does a joke add a number, a danger or health claim, an animal's feeling or motive, or a safety instruction? Is a hedge missing? Does a safety line keep its condition and its credit, said clean? Is an insult aimed at the viewer? Is a swear inside a credit? Does the first spoken sentence hold the searched words? Is the pet named with the comma?
3. Fix each problem with the smallest change that makes it true, keeping it funny where you can. List every change (where, old, new, why). Do not rewrite lines that are fine and do not shorten the cut below 65 seconds.
4. Run from ${OM}: python3 tools/postkit.py lint on the spec; it must pass with 0 fail.
5. Write the check file: verdict first, then the table of changes, then what you could not verify.
cleared is true only if, after your changes, you would stake the channel's name on every claim.`

const buildPrompt = (t, s) => `You are building one TikTok cut from a checked spec. Your label: build-${t.slug}. You do not change wording: if a line must change, stop and report it.
${RULES}
SPEC: ${s.spec}
YOUR FILES: ${OM}/episodes/drawn-house/tt-${t.slug}.mp4 and the sheet ${OM}/episodes/drawn-house/sheets/${t.slug}-min-tt.jpg. Layout keys in the spec (positions, pads, zoom, card times) may change; words may not.
DO, from ${OM}:
1. python3 tools/postkit.py render ${s.spec} episodes/drawn-house/tt-${t.slug}.mp4 --work /dev/shm/${t.slug}-min/tt
   A pass is exit 0 and the line "ok every line heard to its end". On FAIL render once more (the voice service drops words at random). If the same line fails twice, do NOT reword it: report the line.
2. The cut must run over one minute: 62 to 92 seconds. Under 62 is a fail: report it, do not pad with silence.
3. Read the contact sheet the render printed (an image) and copy it to the sheet path: the animal is on screen from frame 0; the search phrase is on screen at the start and not covered; the line-2 gag is visible; cards are readable and inside the frame; captions do not sit on a card and show the softened spellings (SH*T, F**K), never the bare word; no two scenes in a row look the same for more than about 8 seconds; the last frame is back in the first room.
4. python3 tools/postkit.py lint ${s.spec} --mp4 episodes/drawn-house/tt-${t.slug}.mp4 (0 fail).
Return the mp4 path, the seconds, the voice-check result line, the lint result line, what you saw on the sheet and every problem. ok is true only if the voice check and lint passed, the length is 62 to 92 seconds and the sheet shows nothing wrong.`

const results = await pipeline(
  topics,
  t => {
    if (t.packs && t.packs.length) return { slug: t.slug, ok: true, pack_path: '', problems: [] }
    return agent(factsPrompt(t), { label: `facts:${t.slug}`, phase: 'Facts', model: 'sonnet', schema: FACTS })
  },
  (f, t) => {
    if (!f || !f.ok) { log(`${t.slug}: no usable fact pack; stopped`); return null }
    return agent(scriptPrompt(t, f), { label: `script:${t.slug}`, phase: 'Script', schema: SCRIPT }).then(s => (s && s.ok ? { f, s } : null))
  },
  (fs, t) => {
    if (!fs) return null
    return agent(checkPrompt(t, fs.f, fs.s), { label: `check:${t.slug}`, phase: 'Check', model: 'opus', schema: CHECK }).then(c => ({ ...fs, c }))
  },
  (x, t) => {
    if (!x) return null
    if (!x.c || !x.c.cleared) { log(`${t.slug}: the check did not clear it (${x.c ? x.c.blocked_reason : 'no result'}); not built`); return { slug: t.slug, script: x.s, check: x.c, build: null } }
    return agent(buildPrompt(t, x.s), { label: `build:${t.slug}`, phase: 'Build', model: 'sonnet', schema: BUILD })
      .then(b => ({ slug: t.slug, script: x.s, check: x.c, build: b }))
  },
)

const done = results.filter(Boolean)
log(`built ${done.filter(r => r.build && r.build.ok).length} of ${topics.length}; the main session now looks at the sheets, sends the previews, commits, schedules and logs`)
return { results: done, dropped: topics.filter((t, i) => !results[i]).map(t => t.slug) }
