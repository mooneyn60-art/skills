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

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'tars-check', description: 'TARS reads the chart under his options rules and trades only if a setup fires' })
    await $.command.register({ name: 'stops', description: 'TARS checks every stock has a stop and adds any missing one' })
    await $.command.register({ name: 'town', description: 'Links to TARS Town and the SPY Live Desk' })
    $.ui.status('TARS · stop guard on')
    return next(e)
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
