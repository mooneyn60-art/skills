import type { Register, EngineInterface } from 'claude-code'

// The slot's money rules as a hard gate, not a reminder (skills/robinhood-autotrader/routines/TARS_OPTIONS_LIVE.md).
// Only orders that OPEN an option position are checked; closing orders and stops always pass, so protection is
// never blocked. Rules change only with Nolan's words: edit the numbers here when the routine file changes.
const STATE = '/home/user/skills/skills/robinhood-autotrader/paper/live_options/state.json'
const CAP: Record<string, number> = { calm: 500, tense: 250, stressed: 100, halted: 0 } // max premium per trade, by mood
const ENTRIES: Record<string, number> = { calm: 2, tense: 2, stressed: 1, halted: 0 }
const DAY_STOP = -100 // after this realized on the day, no more entries

export type Slot = { mood?: string; halted?: boolean; day?: string; day_realized?: number; entries_today?: number; buffer?: number }
export type Order = { legs?: { position_effect?: string; side?: string }[]; quantity?: string; price?: string; type?: string }

function et(d: Date): { day: string; hm: string; wd: string } {
  const f = (o: Intl.DateTimeFormatOptions) => new Intl.DateTimeFormat('en-CA', { timeZone: 'America/New_York', ...o }).format(d)
  return { day: f({ year: 'numeric', month: '2-digit', day: '2-digit' }), hm: f({ hour: '2-digit', minute: '2-digit', hour12: false }), wd: new Intl.DateTimeFormat('en-US', { timeZone: 'America/New_York', weekday: 'short' }).format(d) }
}

/** Why this order breaks a slot rule, or '' when it may go. */
export function check(o: Order, slot: Slot, now: Date): string {
  const legs = o.legs ?? []
  if (!legs.some(l => l.position_effect === 'open')) return '' // closing or a stop: always allowed
  const t = et(now), mood = slot.halted ? 'halted' : (slot.mood ?? 'calm')
  const today = slot.day === t.day
  if (mood === 'halted' || (slot.buffer ?? 500) <= 300) return 'the slot is HALTED (buffer at or under $300). Only Nolan restarts it.'
  if (['Sat', 'Sun'].includes(t.wd) || t.hm < '10:30' || t.hm >= '14:30') return `entries are only 10:30-14:30 ET on weekdays (now ${t.hm} ET).`
  if (today && (slot.day_realized ?? 0) <= DAY_STOP) return `the day stop is hit (${slot.day_realized} realized today, limit ${DAY_STOP}).`
  const max = ENTRIES[mood] ?? 2
  if (today && (slot.entries_today ?? 0) >= max) return `mood ${mood} allows ${max} entr${max === 1 ? 'y' : 'ies'} a day and ${slot.entries_today} are used.`
  if ((o.type ?? 'limit') !== 'limit') return 'opening orders must be limit orders at the mid (rules: never chase).'
  const prem = Number(o.price ?? 0) * Number(o.quantity ?? 1) * 100
  const cap = Math.min(CAP[mood] ?? 500, slot.buffer ?? 500)
  if (prem > cap) return `premium $${prem.toFixed(0)} is over the $${cap} cap for mood ${mood}.`
  return ''
}

async function gate($: EngineInterface, e: unknown): Promise<string> {
  let slot: Slot = {}
  try { slot = JSON.parse(String(await $.fs.read(STATE))) as Slot } catch { slot = {} }
  const why = check(e as Order, slot, new Date())
  if (!why) return ''
  const said = String((await $.store.get('guard.lastPrompt')) ?? '')
  if (/\boverride\b/i.test(said)) { $.ui.toast(`TARS guard: overridden by Nolan (${why})`); return '' }
  return `TARS slot guard: ${why} If this is Nolan's own trade, he can say "override".`
}

export const register: Register = on => {
  // remember Nolan's latest message: the word "override" in it lets his own trade through the gate
  on('prompt.submit', async ($, e, next) => {
    if (!e.isMeta && !e.command) await $.store.set('guard.lastPrompt', String(e.text ?? '').slice(0, 2000))
    return next(e)
  })

  on('tool.call', { tool: 'mcp__Robinhood__place_option_order' }, async ($, e, next) => {
    const deny = await gate($, e); return deny ? { deny } : next(e)
  })
  on('tool.call', { tool: 'mcp__Robinhood__review_option_order' }, async ($, e, next) => {
    const deny = await gate($, e); return deny ? { deny } : next(e)
  })
}
