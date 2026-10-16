import type { Register } from 'claude-code'

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
type Sig = { id: string; who: string; kind: 'threat' | 'chance' | 'info' | 'social'; text: string; v: number }
type Slot = { buffer?: number; halted?: boolean; mood?: string; loss_streak?: number; trades?: number }

function etParts(d: Date): { day: string; hm: string; wd: string } {
  const f = (o: Intl.DateTimeFormatOptions) => new Intl.DateTimeFormat('en-CA', { timeZone: 'America/New_York', ...o }).format(d)
  return { day: f({ year: 'numeric', month: '2-digit', day: '2-digit' }), hm: f({ hour: '2-digit', minute: '2-digit', hour12: false }), wd: new Intl.DateTimeFormat('en-US', { timeZone: 'America/New_York', weekday: 'short' }).format(d) }
}


export function stageText(slot: Slot, lastAsk: string, now: Date, lastFocus: string[]): { text: string; focus: string[] } {
  const t = etParts(now), weekday = !['Sat', 'Sun'].includes(t.wd), open = weekday && t.hm >= '09:30' && t.hm < '16:00'
  const sigs: Sig[] = []
  const mood = slot.mood ?? 'calm', buf = slot.buffer ?? 500
  if (slot.halted) sigs.push({ id: 'pit', who: 'Pip (options slot)', kind: 'threat', text: 'Slot is halted at the hard stop. No trades until Nolan restarts it.', v: 0.95 })
  else if (mood !== 'calm') sigs.push({ id: 'pit', who: 'Pip (options slot)', kind: 'threat', text: `Mood ${mood} (${slot.loss_streak ?? 0} losses in a row, buffer $${buf}): trade small per the Mood table.`, v: mood === 'stressed' ? 0.8 : 0.6 })
  else if (open && t.hm >= '10:30' && t.hm < '14:30') sigs.push({ id: 'pit', who: 'Pip (options slot)', kind: 'chance', text: 'Entry window is open (10:30-14:30). Check S1/S2 if Nolan asks for a TARS check.', v: 0.55 })
  if (open) sigs.push({ id: 'guard', who: 'Sid (stops)', kind: 'threat', text: 'Market is open: before any account talk, confirm every stock still has its stop (live check, not memory).', v: 0.5 })
  if (open && t.hm < '10:30') sigs.push({ id: 'hall', who: 'Rhea (Nolan\'s rules)', kind: 'threat', text: 'Before 10:30: Nolan\'s record is 0 for 5 here. Remind him to wait; nothing new opens.', v: 0.75 })
  const ev = EVENTS[t.day]
  if (ev) sigs.push({ id: 'look', who: 'Lookout (calendar)', kind: 'threat', text: `${ev} today.`, v: open ? 0.6 : 0.35 })
  for (const [d, s] of Object.entries(HELD_EARN)) {
    const days = (Date.parse(d) - Date.parse(t.day)) / 864e5
    if (days >= 0 && days <= 3) sigs.push({ id: 'yard', who: 'Gus (holdings)', kind: 'threat', text: `${s} reports earnings after the close ${days === 0 ? 'today' : `in ${days} day${days === 1 ? '' : 's'}`}: a stop can't stop an overnight gap. Raise it with Nolan.`, v: days === 0 ? 0.85 : 0.5 })
  }
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
  const body = chain.length ? chain.join('\n') : 'Quiet mind: nothing urgent on the stage.'
  return { text: `${head}\nTrain of thought before answering (run the Stage step in skills/tars/SKILL.md; act on it in this order if it bears on the message; repo state only, fetch live data for anything about the account):\n${body}`, focus }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'tars-check', description: 'TARS reads the chart under his options rules and trades only if a setup fires' })
    await $.command.register({ name: 'stops', description: 'TARS checks every stock has a stop and adds any missing one' })
    await $.command.register({ name: 'town', description: 'Links to TARS Town and the SPY Live Desk' })
    $.ui.status('TARS · stop guard on')
    return next(e)
  })

  on('prompt.submit', async ($, e, next) => {
    if (e.command || e.isMeta) return next(e)
    try {
      let slot: Slot = {}
      try { slot = JSON.parse(String(await $.fs.read(`${ROOT}/paper/live_options/state.json`))) as Slot } catch { slot = {} }
      let log = ''; try { log = String(await $.fs.read(`${ROOT}/notes/NOLAN_LOG.md`)) } catch { log = '' }
      const heads = log.split('\n').filter(l => l.startsWith('## ')); const lastAsk = (heads[heads.length - 1] || '').replace(/^## /, '').slice(0, 220)
      const lastFocus = ((await $.store.get('stage.focus')) as string[] | undefined) ?? []
      const st = stageText(slot, lastAsk, new Date(), lastFocus)
      await $.store.set('stage.pending', st.focus)
      return next({ ...e, context: [...(e.context ?? []), st.text] })
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
