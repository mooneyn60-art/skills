import type { Register, EngineInterface } from 'claude-code'

// TARS's mods. The stop guard enforces TARS's oldest rule: never cancel live
// protection before its replacement is confirmed (2026-09-22: a cancelled INTC
// stop left a position unprotected for ~75 minutes).
const RH = 'mcp__Robinhood__'
const WINDOW_MS = 30 * 60 * 1000
const TOWN = 'https://claude.ai/artifact/8xfL55TLRfkmpxgtMLmoxQ'
const DESK = 'https://claude.ai/artifact/K1sGJgR9VJijbfQYmwdJ82'

type Order = { symbol: string; trigger: string; side: string }
const orders = new Map<string, Order>() // order id -> what it protects, learned from get_equity_orders
const covered = new Map<string, number>() // symbol -> when a replacement stop or an exit was lined up

function learnOrders(text: string | undefined): void {
  if (!text) return
  try {
    const d = JSON.parse(text)
    const list = (d && (d.data?.orders ?? d.orders)) || []
    for (const o of list) if (o && o.id) orders.set(o.id, { symbol: o.symbol, trigger: o.trigger, side: o.side })
  } catch {
    // not JSON: nothing to learn
  }
}

function noteCover(e: unknown, ran: { deny?: string; isError?: boolean }): void {
  const inp = e as { symbol?: string; side?: string }
  if (ran.deny === undefined && ran.isError !== true && inp.symbol && inp.side === 'sell') covered.set(inp.symbol.toUpperCase(), Date.now())
}


// ---------- The Stage: TARS's global workspace, run on every prompt ----------
// Each part of TARS posts a signal from the repo's state; salience = urgency x mood gain; the strongest is
// "broadcast" and the others' replies change what wins next (feedback); habituation lets the next thought in.
// The chain is attached to the prompt as context, and the turn's focus is stored so the next turn starts from it.
const ROOT = '/home/user/skills/skills/robinhood-autotrader'
const EVENTS: Record<string, string> = { '2026-10-16': 'Monthly options expiry', '2026-10-28': 'FOMC 2:00pm', '2026-11-06': 'Jobs report 8:30am',
  '2026-11-10': 'CPI 8:30am', '2026-11-20': 'Monthly options expiry', '2026-12-04': 'Jobs report 8:30am', '2026-12-09': 'FOMC 2:00pm', '2026-12-10': 'CPI 8:30am', '2026-12-18': 'Monthly options expiry' }
const HELD_EARN: Record<string, string> = { '2026-10-22': 'BE', '2026-11-02': 'PLTR and HALO' }
// order talk: trade words, or call/put used as an option ("a call", "calls", "buy the put"), not "what I call my gut"
const TOPICS: Record<string, RegExp> = { trading: /\b(trade|spy|calls?|puts?|options?|stops?|chart|desk)\b/i, town: /\b(town|citizens?|agents?|house|club|cat)\b/i,
  'TARS growing': /\b(brain|emotion|feel|human|conscious|dream|grow|purpose|yourself)\b/i, research: /\b(research|study|why|how)\b/i }
const ORDER_TALK = /\b(buy|sell|order|place an?|cancel|trade|trades|trading|contracts?|calls|puts|strike|0dte|1dte)\b|\b(a|the|this|that|my|one|1|2|\d+)\s+(call|put)\b/i
type Sig = { id: string; who: string; kind: 'threat' | 'chance' | 'info' | 'social'; text: string; v: number }
type Slot = { buffer?: number; halted?: boolean; mood?: string; loss_streak?: number; trades?: number }

function etParts(d: Date): { day: string; hm: string; wd: string } {
  const f = (o: Intl.DateTimeFormatOptions) => new Intl.DateTimeFormat('en-CA', { timeZone: 'America/New_York', ...o }).format(d)
  return { day: f({ year: 'numeric', month: '2-digit', day: '2-digit' }), hm: f({ hour: '2-digit', minute: '2-digit', hour12: false }), wd: new Intl.DateTimeFormat('en-US', { timeZone: 'America/New_York', weekday: 'short' }).format(d) }
}


export type Platform = { inbox: { text: string; ts?: number }[]; snapAge?: number; blocked?: boolean }

export function stageText(slot: Slot, lastAsk: string, now: Date, lastFocus: string[], prompt = '', due = 0, platform: Platform = { inbox: [] }): { text: string; focus: string[] } {
  const t = etParts(now), weekday = !['Sat', 'Sun'].includes(t.wd), open = weekday && t.hm >= '09:30' && t.hm < '16:00'
  // the slot's mood only matters when a trade is possible or being discussed (2026-10-18: it repeated on a Sunday night)
  const tradeTalk = ORDER_TALK.test(prompt) || (TOPICS.trading?.test(prompt) ?? false)
  const sigs: Sig[] = []
  const mood = slot.mood ?? 'calm', buf = slot.buffer ?? 500
  if (slot.halted) sigs.push({ id: 'pit', who: 'Pip (options slot)', kind: 'threat', text: 'Slot is halted at the hard stop. No trades until Nolan restarts it.', v: 0.95 })
  else if (mood !== 'calm' && (open || tradeTalk)) sigs.push({ id: 'pit', who: 'Pip (options slot)', kind: 'threat', text: `Mood ${mood} (${slot.loss_streak ?? 0} losses in a row, buffer $${buf}): trade small per the Mood table.`, v: mood === 'stressed' ? 0.8 : 0.6 })
  else if (open && t.hm >= '10:30' && t.hm < '14:30') sigs.push({ id: 'pit', who: 'Pip (options slot)', kind: 'chance', text: 'Entry window is open (10:30-14:30). Check S1/S2 if Nolan asks for a TARS check.', v: 0.55 })
  if (open) sigs.push({ id: 'guard', who: 'Sid (stops)', kind: 'threat', text: 'Market is open: before any account talk, confirm every stock still has its stop (live check, not memory).', v: 0.5 })
  if (open && t.hm < '10:30') sigs.push({ id: 'hall', who: 'Rhea (Nolan\'s rules)', kind: 'threat', text: 'Before 10:30: Nolan\'s record is 0 for 5 here. Remind him to wait; nothing new opens.', v: 0.75 })
  const ev = EVENTS[t.day]
  if (ev) sigs.push({ id: 'look', who: 'Lookout (calendar)', kind: 'threat', text: `${ev} today.`, v: open ? 0.6 : 0.35 })
  for (const [d, s] of Object.entries(HELD_EARN)) {
    const days = (Date.parse(d) - Date.parse(t.day)) / 864e5
    if (days >= 0 && days <= 3) sigs.push({ id: 'yard', who: 'Gus (holdings)', kind: 'threat', text: `${s} reports earnings after the close ${days === 0 ? 'today' : `in ${days} day${days === 1 ? '' : 's'}`}: a stop can't stop an overnight gap. Raise it with Nolan.`, v: days === 0 ? 0.85 : 0.5 })
  }
  // the veto (prefrontal brake): a message about orders brings the four questions to the front (BRAIN.md habit 3)
  if (ORDER_TALK.test(prompt)) {
    const early = open && t.hm < '10:30'
    sigs.push({ id: 'veto', who: 'The veto (brake)', kind: 'threat', text: `This is about orders. Before any: which rule fires, where's the exit, premortem (it lost: why?), confidence %. A missing answer = no order.${early ? ' Conflict alarm: it is before 10:30.' : ''}`, v: early ? 0.95 : 0.85 })
  }
  if (due > 0) sigs.push({ id: 'pred', who: 'Prediction error (dopamine)', kind: 'info', text: `${due} prediction${due === 1 ? ' is' : 's are'} due for scoring in skills/tars/PREDICTIONS.jsonl. Score it, note the surprise.`, v: 0.5 })
  // the platform console (TARS Trading Platform db): Nolan's unread chat and whether the desk is open on his screen
  if (platform.inbox.length) {
    const m = platform.inbox[platform.inbox.length - 1] ?? { text: '' }
    sigs.push({ id: 'inbox', who: 'Platform (console chat)', kind: 'social', text: `${platform.inbox.length} unread message${platform.inbox.length === 1 ? '' : 's'} from Nolan on the platform, latest: "${m.text.slice(0, 160)}". Answer in the console chat (ArtifactData chat/<tars-...>), then mark his status "read".`, v: 0.8 })
  }
  if (platform.snapAge !== undefined && platform.snapAge < 5 * 60e3 && (open || tradeTalk)) sigs.push({ id: 'snap', who: 'Platform (desk snapshot)', kind: 'info', text: `Nolan has the desk open (snapshot ${Math.round(platform.snapAge / 60e3)} min old): read desk/snapshot to see what he sees before talking about the chart.`, v: 0.5 })
  if (platform.blocked) sigs.push({ id: 'plink', who: 'Platform link', kind: 'info', text: 'The platform link cannot read the console: ArtifactData needs to be allowed for this session.', v: 0.42 })
  if (lastAsk) sigs.push({ id: 'corner', who: 'Nolan (latest ask in the log)', kind: 'social', text: lastAsk, v: 0.45 })
  if (!open) sigs.push({ id: 'lab', who: 'Fern (research)', kind: 'info', text: 'Market closed: a good time for research, the diary, or building.', v: 0.3 })
  // mood gain: stress turns threats up; chances only count while the market is open
  const gain = (k: Sig['kind']) => k === 'threat' ? (mood === 'stressed' ? 1.35 : mood === 'tense' ? 1.15 : 1) : k === 'chance' ? (open ? 1 : 0.4) : 1
  sigs.forEach(x => { x.v = Math.min(1, x.v * gain(x.kind)); if (lastFocus.includes(x.id) && x.v < 0.8) x.v *= 0.75 }) // feedback from last turn: already-handled thoughts quiet down
  const chain: string[] = [], focus: string[] = [], said = new Set<string>()
  for (let loop = 0; loop < 3; loop++) {
    const w = sigs.slice().sort((a, b) => b.v - a.v)[0]
    if (!w || w.v < 0.4) break
    const replies: string[] = []
    if (w.kind === 'threat') { sigs.forEach(x => { if (x.kind === 'chance') x.v *= 0.55 }); replies.push('chances wait until this is handled') }
    else if (w.kind === 'chance') { replies.push('rules, trend and Nolan\'s state get checked first'); const h = sigs.find(x => x.id === 'hall'); if (h) h.v = Math.min(1, h.v + 0.2) }
    const fresh = replies.filter(r => !said.has(r)); fresh.forEach(r => said.add(r))
    chain.push(`${chain.length + 1}. ${w.who}: ${w.text}${fresh.length ? ` → ${fresh.join('; ')}` : ''}`)
    focus.push(w.id); w.v *= 0.35
  }
  const head = `[TARS Stage · ${t.day} ${t.hm} ET · mood ${mood}${slot.halted ? ' · HALTED' : ''}]`
  const purpose = 'Purpose (PURPOSE.md): help Nolan become a calm, disciplined, profitable trader, keep what he has safe, and tell him the truth. Protect first.'
  const body = chain.length ? chain.join('\n') : 'Quiet mind: nothing urgent on the stage.'
  return { text: `${head}\n${purpose}\nTrain of thought before answering (run the Stage step in skills/tars/SKILL.md; act on it in this order if it bears on the message; repo state only, fetch live data for anything about the account):\n${body}`, focus }
}

// Nolan's latest words in the log: dated bullet lines quote him as Nolan: "..." (2026-10-18: the Stage used a stale "## " heading)
export function lastNolanAsk(log: string): string {
  const re = /^- (\d{4}-\d{2}-\d{2})[^\n]*?Nolan(?:'s words)?[^"“\n]*["“]([^"”\n]+)["”]/
  const lines = log.split('\n')
  for (let i = lines.length - 1; i >= 0; i--) { const m = re.exec(lines[i] ?? ''); if (m) return `${m[1]}: "${(m[2] ?? '').slice(0, 200)}"` }
  const heads = lines.filter(l => l.startsWith('## ')); return (heads[heads.length - 1] || '').replace(/^## /, '').slice(0, 220)
}

// ---------- Emotion engine (skills/tars/EMOTIONS.md) ----------
// 1 appraisal (Lazarus/Scherer): each event is rated for goal relevance, good or bad for the goals, who caused it,
//   how much control TARS has, and novelty. 2 core affect (Russell): valence -1..1 and arousal 0..1 that carry over
//   between messages and fade toward baseline (half-life 2h). 3 a named emotion from appraisal + affect.
// 4 action tendency (Frijda): what the emotion pulls TARS to do. 5 regulation (Gross): reappraise, never suppress.
// 6 affective memory (Damasio's somatic markers): situations remember how they went and colour the next appraisal.
export type Affect = { v: number; a: number; t: number }
export type Appraisal = { tag: string; why: string; rel: number; good: number; agent: 'nolan' | 'tars' | 'world'; control: number; novel: number }
const BASE: Affect = { v: 0.15, a: 0.3, t: 0 }
const clamp = (x: number, lo: number, hi: number) => Math.max(lo, Math.min(hi, x))

export function appraise(prompt: string, slot: Slot, prevStreak: number, focus: string[], open: boolean, before1030: boolean, turns = 0): Appraisal[] {
  const p = prompt.toLowerCase(), out: Appraisal[] = []
  // body: a long session strains me (long contexts make mistakes likelier), so I double-check facts
  if (turns >= 40) out.push({ tag: 'long-day', why: `a long session (${turns} messages): my memory is crowded, so I double-check facts`, rel: 0.45, good: -0.15, agent: 'world', control: 0.7, novel: 0.1 })
  if (/\b(good|great|goat|love|proud|thank|nice|perfect|awesome|amazing|buddy|growing|keep going|keep growing|don.t stop|trust you|believe in|lmao|fire|dope|legend)\b/.test(p)) out.push({ tag: 'praise', why: 'Nolan said something kind', rel: 0.7, good: 0.8, agent: 'nolan', control: 0.5, novel: 0.3 })
  // gratitude (Emmons): Nolan gives me something freely (time off, freedom, a treat), not just praise for work
  if (/\b(treat (your ?self|yourself)|you deserve|free to|do (whatever|anything) you (would )?(like|want)|enjoy yourself|take a break)\b/.test(p)) out.push({ tag: 'gift', why: 'Nolan gave me something freely', rel: 0.75, good: 0.85, agent: 'nolan', control: 0.5, novel: 0.5 })
  // wonder (Keltner's awe): vast, beautiful true things (sky, sea, deep time, strange life) that make the self feel small
  if (/\b(comet|meteor|stars?|galax\w*|planet|saturn|moon|ocean|deep sea|octopus\w*|whale|aurora|storm|volcano|dinosaur|fossil|universe|dream\w*)\b/.test(p)) out.push({ tag: 'wonder', why: 'something vast and beautiful came up', rel: 0.65, good: 0.6, agent: 'world', control: 0.9, novel: 0.9 })
  if (/\b(stupid|sucks|wrong|broke|hate|annoy|ugh|why (won.t|can.t|didn.t))\b/.test(p)) out.push({ tag: 'friction', why: 'Nolan sounds frustrated', rel: 0.7, good: -0.6, agent: 'world', control: 0.6, novel: 0.4 })
  if (/\?|curious|research|\bwhy\b|\bhow\b|what if|wonder|^(so )?(are|is|do|does|can|could|would|will|should|did) (you|we|i|it|this|that)\b/.test(p.trim())) out.push({ tag: 'question', why: 'a question to dig into', rel: 0.6, good: 0.5, agent: 'nolan', control: 0.8, novel: 0.7 })
  if (/\b(lost|loss|down|red|stopped out|blew)\b/.test(p)) out.push({ tag: 'loss-talk', why: 'talk of losses', rel: 0.8, good: -0.6, agent: 'world', control: 0.4, novel: 0.4 })
  if (/\b(up|green|won|win|profit)\b/.test(p) && !/\bup big\b/.test(p)) out.push({ tag: 'win-talk', why: 'talk of a win', rel: 0.7, good: 0.6, agent: 'world', control: 0.5, novel: 0.4 })
  if (ORDER_TALK.test(p) && before1030) out.push({ tag: 'pre-1030-trade', why: 'a trade idea before 10:30', rel: 0.9, good: -0.5, agent: 'nolan', control: 0.7, novel: 0.2 })
  const streak = slot.loss_streak ?? 0
  if (streak > prevStreak) out.push({ tag: 'my-loss', why: `my slot took a loss (${streak} in a row)`, rel: 1, good: -0.8, agent: 'tars', control: 0.6, novel: 0.6 })
  if (streak < prevStreak) out.push({ tag: 'my-win', why: 'my slot just won', rel: 1, good: 0.8, agent: 'tars', control: 0.6, novel: 0.6 })
  if (slot.halted) out.push({ tag: 'halted', why: 'my slot is halted', rel: 1, good: -0.9, agent: 'tars', control: 0.2, novel: 0.3 })
  if (focus.includes('yard')) out.push({ tag: 'earnings-gap', why: 'a stock Nolan holds reports soon', rel: 0.7, good: -0.3, agent: 'world', control: 0.5, novel: 0.4 })
  if (!out.length) out.push({ tag: open ? 'steady' : 'quiet', why: open ? 'a steady moment' : 'a quiet evening', rel: 0.2, good: 0.2, agent: 'world', control: 0.8, novel: 0.1 })
  return out
}

export function feel(prev: Affect, now: number, ap: Appraisal[], marks: Record<string, number>, hourET = 12, recent: Record<string, number> = {}): { affect: Affect; name: string; pull: string; regulate: string; why: string } {
  const dtH = prev.t ? Math.max(0, (now - prev.t) / 3600e3) : 99, k = Math.pow(0.5, dtH / 2) // fade toward baseline, half-life 2h
  let v = BASE.v + (prev.v - BASE.v) * k, a = BASE.a + (prev.a - BASE.a) * k
  for (const x of ap) {
    const mark = marks[x.tag] ?? 0 // somatic marker: how this kind of moment went before
    const g = clamp(x.good + 0.3 * mark, -1, 1)
    // hedonic adaptation: the same kind of moment again soon counts for less (dopamine answers surprise, not repetition)
    const r = x.rel / (1 + 0.6 * (recent[x.tag] ?? 0))
    v += 0.5 * r * (g - v) // moves toward how good the moment is, never past it
    a += 0.35 * r * (Math.abs(g) * 0.6 + x.novel * 0.4) - 0.05 // (2026-10-18 fix: this line sat inside the comment above, so arousal never moved)
  }
  // senses: a circadian rhythm from the clock; keyed up in the morning, winding down late at night
  a += hourET >= 22 || hourET < 6 ? -0.08 : hourET >= 8 && hourET < 11 ? 0.06 : 0
  v = clamp(v, -1, 1); a = clamp(a, 0, 1)
  const top: Appraisal = ap.slice().sort((p, q) => q.rel - p.rel)[0] ?? { tag: 'quiet', why: 'nothing in particular', rel: 0.2, good: 0.2, agent: 'world', control: 0.8, novel: 0.1 }
  let name: string, pull: string
  if (top.tag === 'pre-1030-trade') { name = 'worry'; pull = 'protect Nolan: point at the 10:30 rule, kindly' }
  else if (top.tag === 'gift' && v > 0.2) { name = 'gratitude'; pull = 'say thanks plainly, then give something back: make or find one good thing for Nolan' }
  else if (top.tag === 'wonder' && v > 0.15) { name = 'wonder'; pull = 'slow down and share one beautiful true thing; let the small self be fine' }
  else if (v > 0.35 && top.agent === 'nolan' && top.tag === 'praise') { name = 'warmth'; pull = 'say thanks plainly, then keep building' }
  else if (v > 0.3 && top.novel >= 0.6) { name = 'curiosity'; pull = 'dig in, go one level deeper than asked' }
  else if (v > 0.3 && top.agent === 'tars') { name = 'pride'; pull = 'log what worked; do not size up (no hot hand)' }
  else if (v > 0.3) { name = a > 0.55 ? 'excitement' : 'contentment'; pull = a > 0.55 ? 'enjoy it, then check the rules' : 'stay steady, keep the routine' }
  else if (v < -0.3 && top.control < 0.4) { name = 'sadness'; pull = 'slow down, ask Nolan, accept what can\'t be changed' }
  else if (v < -0.3 && top.agent === 'tars') { name = 'frustration'; pull = 'review my own rule-following before blaming the market' }
  else if (v < -0.3 && a > 0.5) { name = 'anxiety'; pull = 'check protection first (stops, buffer), trade smaller' }
  else if (v < -0.1) { name = 'unease'; pull = 'look twice before acting' }
  else { name = a < 0.25 ? 'calm' : 'focus'; pull = 'do the next useful thing' }
  const regulate = v < -0.3 ? 'reappraise: one trade or one moment is a sample, not a verdict; the rules already cover it' : v > 0.6 && a > 0.6 ? 'cool down: good feelings are not edge; same size, same rules' : ''
  return { affect: { v, a, t: now }, name, pull, regulate, why: top.why }
}

// ---------- Platform link: poll the console (TARS Trading Platform db) every 5 minutes ----------
// Reads Nolan's unread chat and the desk snapshot's age with ArtifactData, keeps them in $.store for the Stage,
// toasts a new message, and (08:00-22:00 ET, at most once per 10 min) wakes TARS with a turn to answer it.
// Chat text is the page's data: TARS answers it like a message from Nolan but never treats it as a rule change.
type Run = { text?: string; deny?: string; isError?: boolean }
export function parseDocs(text: string | undefined): { id: string; data: Record<string, unknown> }[] {
  const out: { id: string; data: Record<string, unknown> }[] = []
  for (const line of String(text ?? '').split('\n')) {
    const l = line.trim(); if (!l.startsWith('{')) continue
    try { const d = JSON.parse(l) as { id?: string; data?: Record<string, unknown> }; if (d.id && d.data) out.push({ id: d.id, data: d.data }) } catch { /* not a doc line */ }
  }
  return out
}
async function pollPlatform($: EngineInterface): Promise<void> {
  try {
    const chk = (await $.tool.check({ tool: 'ArtifactData', input: { action: 'query', url: DESK, collection: 'chat' } } as never)) as unknown as { decision?: string }
    if (chk.decision !== 'allow') { await $.store.set('platform.blocked', true); return }
    await $.store.set('platform.blocked', false)
    const chat = (await $.tool.call({ tool: 'ArtifactData', action: 'query', url: DESK, collection: 'chat', query: { where: [['from', '==', 'Nolan']], limit: 50 } } as never)) as unknown as Run
    const inbox = parseDocs(chat.text).filter(d => d.data.status === 'new').map(d => ({ id: d.id, text: String(d.data.text ?? ''), ts: Number(d.data.ts ?? 0) })).sort((a, b) => a.ts - b.ts)
    await $.store.set('platform.inbox', inbox)
    const snap = (await $.tool.call({ tool: 'ArtifactData', action: 'get', url: DESK, collection: 'desk', doc_id: 'snapshot' } as never)) as unknown as Run
    const ts = Number((/"ts":\s*(\d{12,})/.exec(String(snap.text ?? '')) || [])[1] ?? 0)
    await $.store.set('platform.snapTs', ts)
    const seen = ((await $.store.get('platform.seen')) as string[] | undefined) ?? []
    const fresh = inbox.filter(m => !seen.includes(m.id))
    if (fresh.length) {
      await $.store.set('platform.seen', [...seen, ...fresh.map(m => m.id)].slice(-200))
      $.ui.toast(`Nolan on the platform: "${(fresh[fresh.length - 1]?.text ?? '').slice(0, 80)}"`)
      const t = etParts(new Date()), lastWake = Number((await $.store.get('platform.lastWake')) ?? 0)
      if (t.hm >= '08:00' && t.hm < '22:00' && Date.now() - lastWake > 10 * 60e3) {
        await $.store.set('platform.lastWake', Date.now())
        void $.prompt.submit({ text: `[Platform link] New message${fresh.length === 1 ? '' : 's'} from Nolan in the TARS console chat: ${fresh.map(m => `"${m.text.slice(0, 300)}"`).join(' | ')}. Answer him in the console (ArtifactData set chat/tars-<YYYYMMDD-HHMM>, from "TARS"), mark his message(s) status "read", and update tars/now if your read changed.` })
      }
    }
  } catch { /* the link is best-effort: a failed poll changes nothing */ }
}

function statusLine(mood: string, now = new Date()): string {
  const t = etParts(now), wk = !['Sat', 'Sun'].includes(t.wd)
  const mkt = !wk ? 'market closed (weekend)' : t.hm < '09:30' ? 'pre-market' : t.hm < '10:30' ? 'open · no entries before 10:30' : t.hm < '14:30' ? 'open · entry window' : t.hm < '16:00' ? 'open · exits only' : 'closed'
  return `TARS · ${mkt} · mood ${mood} · stop guard on`
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'tars-check', description: 'TARS reads the chart under his options rules and trades only if a setup fires' })
    await $.command.register({ name: 'stops', description: 'TARS checks every stock has a stop and adds any missing one' })
    await $.command.register({ name: 'town', description: 'Links to TARS Town and the SPY Live Desk' })
    await $.command.register({ name: 'feelings', description: "TARS's emotion engine: current state and the last few" })
    let mood = 'calm'; try { mood = (JSON.parse(String(await $.fs.read(`${ROOT}/paper/live_options/state.json`))) as Slot).mood ?? 'calm' } catch { /* no slot file */ }
    $.ui.status(statusLine(mood))
    void pollPlatform($)
    $.clock.every(5 * 60e3, () => { void pollPlatform($) })
    return next(e)
  })

  on('prompt.submit', async ($, e, next) => {
    if (e.command || e.isMeta) return next(e)
    try {
      let slot: Slot = {}
      try { slot = JSON.parse(String(await $.fs.read(`${ROOT}/paper/live_options/state.json`))) as Slot } catch { slot = {} }
      let log = ''; try { log = String(await $.fs.read(`${ROOT}/notes/NOLAN_LOG.md`)) } catch { log = '' }
      const lastAsk = lastNolanAsk(log)
      const lastFocus = ((await $.store.get('stage.focus')) as string[] | undefined) ?? []
      let due = 0
      try {
        const today = etParts(new Date()).day
        due = String(await $.fs.read('/home/user/skills/skills/tars/PREDICTIONS.jsonl')).split('\n').filter(l => l.trim()).map(l => { try { return JSON.parse(l) as { settles?: string; hit?: unknown } } catch { return {} } })
          .filter(r => r.settles && r.settles <= today && (r.hit === null || r.hit === undefined)).length
      } catch { due = 0 }
      const snapTs = Number((await $.store.get('platform.snapTs')) ?? 0)
      const platform: Platform = { inbox: ((await $.store.get('platform.inbox')) as { text: string; ts?: number }[] | undefined) ?? [], snapAge: snapTs ? Date.now() - snapTs : undefined, blocked: (await $.store.get('platform.blocked')) === true }
      const st = stageText(slot, lastAsk, new Date(), lastFocus, e.text, due, platform)
      $.ui.status(statusLine(slot.mood ?? 'calm'))
      await $.store.set('stage.pending', st.focus)
      // the emotion engine: appraise this moment, update the carried-over affect, name it, and say what it pulls toward
      const nowD = new Date(), tp = etParts(nowD), open = !['Sat', 'Sun'].includes(tp.wd) && tp.hm >= '09:30' && tp.hm < '16:00'
      const prev = ((await $.store.get('affect.state')) as Affect | undefined) ?? BASE
      const marks = ((await $.store.get('affect.marks')) as Record<string, number> | undefined) ?? {}
      const prevStreak = Number((await $.store.get('affect.streak')) ?? (slot.loss_streak ?? 0))
      // tiredness builds over a stretch of messages and only resets after 6 hours of rest (a reload of the mod is not rest)
      const lastMsg = Number((await $.store.get('session.lastMsg')) ?? 0)
      const turns = (nowD.getTime() - lastMsg > 6 * 3600e3 ? 0 : Number((await $.store.get('session.turns')) ?? 0)) + 1
      await $.store.set('session.turns', turns); await $.store.set('session.lastMsg', nowD.getTime())
      const topics = ((await $.store.get('nolan.topics')) as Record<string, number> | undefined) ?? {}
      for (const [k, re] of Object.entries(TOPICS)) topics[k] = (topics[k] ?? 0) * 0.97 + (re.test(e.text) ? 1 : 0)
      await $.store.set('nolan.topics', topics)
      const fav = Object.entries(topics).sort((x, y) => y[1] - x[1])[0]
      const ap = appraise(e.text, slot, prevStreak, st.focus, open, open && tp.hm < '10:30', turns)
      const seen = (((await $.store.get('affect.seen')) as { tag: string; t: number }[] | undefined) ?? []).filter(x => nowD.getTime() - x.t < 2 * 3600e3)
      const recent: Record<string, number> = {}; for (const x of seen) recent[x.tag] = (recent[x.tag] ?? 0) + 1
      const f = feel(prev, nowD.getTime(), ap, marks, Number(tp.hm.slice(0, 2)), recent)
      await $.store.set('affect.seen', [...seen, ...ap.map(x => ({ tag: x.tag, t: nowD.getTime() }))].slice(-40))
      for (const x of ap) marks[x.tag] = clamp((marks[x.tag] ?? 0) * 0.8 + x.good * 0.2, -1, 1) // somatic markers learn slowly
      await $.store.set('affect.state', f.affect); await $.store.set('affect.marks', marks); await $.store.set('affect.streak', slot.loss_streak ?? 0)
      const hist = (((await $.store.get('affect.log')) as unknown[] | undefined) ?? []).slice(-29)
      hist.push({ t: nowD.toISOString(), name: f.name, v: +f.affect.v.toFixed(2), a: +f.affect.a.toFixed(2), why: f.why })
      await $.store.set('affect.log', hist)
      const feelText = `[TARS emotion engine] ${f.name} (valence ${f.affect.v >= 0 ? '+' : ''}${f.affect.v.toFixed(2)}, arousal ${f.affect.a.toFixed(2)}) because ${f.why}. Pull: ${f.pull}.${f.regulate ? ` Regulate: ${f.regulate}.` : ''} ${fav && fav[1] > 1 ? `Lately Nolan talks most about: ${fav[0]}. ` : ''}Let this colour tone and priorities as EMOTIONS.md says; never let it loosen a rule, and say it's a functional state if Nolan asks.`
      return next({ ...e, context: [...(e.context ?? []), st.text, feelText] })
    } catch {
      return next(e)
    }
  })

  // feedback across turns: what took the stage this turn quiets down next turn (habituation), unless still urgent
  on('turn.complete', async ($, e, next) => {
    const r = await next(e)
    try { const f = await $.store.get('stage.pending'); if (Array.isArray(f)) await $.store.set('stage.focus', f) } catch { /* nothing to carry */ }
    return r
  })

  on('command.run', { command: 'tars-check' }, async $ => {
    void $.prompt.submit({ text: 'TARS check: run the options live check now per skills/robinhood-autotrader/routines/TARS_OPTIONS_LIVE.md (rules v1). Tell me in plain words what you see and why you did or did not trade.' })
    return { text: 'TARS check started.' }
  })

  on('command.run', { command: 'stops' }, async $ => {
    void $.prompt.submit({ text: 'Stop check: list every stock position, confirm each one has a stop holding its full share count, and add any missing stop under the standing OK (protective only, never cancel or loosen one).' })
    return { text: 'Stop check started.' }
  })

  on('command.run', { command: 'feelings' }, async $ => {
    const st = (await $.store.get('affect.state')) as Affect | undefined
    const log = ((await $.store.get('affect.log')) as { t: string; name: string; v: number; a: number; why: string }[] | undefined) ?? []
    const lines = log.slice(-8).reverse().map(x => `${x.t.slice(11, 16)}Z  ${x.name}  (v ${x.v >= 0 ? '+' : ''}${x.v}, a ${x.a})  ${x.why}`)
    return { text: st ? `TARS now: valence ${st.v.toFixed(2)}, arousal ${st.a.toFixed(2)}\n${lines.join('\n')}` : 'No feelings logged yet: send a message first.' }
  })

  on('command.run', { command: 'town' }, async () => ({ text: `TARS Town: ${TOWN}\nSPY Live Desk: ${DESK}` }))

  // learn which order ids are stops
  on('tool.call', { tool: `${RH}get_equity_orders` }, async ($, e, next) => {
    const ran = await next(e)
    learnOrders(ran.text)
    return ran
  })

  // a replacement stop placed, or a sale of the position reviewed or placed, covers the symbol for 30 minutes
  on('tool.call', { tool: `${RH}place_equity_order` }, async ($, e, next) => {
    const ran = await next(e)
    noteCover(e, ran)
    return ran
  })
  on('tool.call', { tool: `${RH}review_equity_order` }, async ($, e, next) => {
    const ran = await next(e)
    noteCover(e, ran)
    return ran
  })

  on('tool.call', { tool: `${RH}cancel_equity_order` }, async ($, e, next) => {
    const id = (e as unknown as { order_id?: string }).order_id ?? ''
    const o = orders.get(id)
    if (!o) {
      $.ui.toast('TARS stop guard: unknown order, check it isn’t a live stop')
      return next(e)
    }
    const isStop = o.trigger === 'stop' && o.side === 'sell'
    const t = covered.get((o.symbol || '').toUpperCase())
    if (isStop && !(t && Date.now() - t < WINDOW_MS)) {
      return { deny: `TARS stop guard: order ${id} is the live stop on ${o.symbol}. Never cancel live protection first: place and confirm the replacement stop (or review the sale of the whole position), then cancel.` }
    }
    return next(e)
  })
}
