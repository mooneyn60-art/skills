import { test, expect } from 'claude-code/testing'
import { check } from './register'

const open = (price: string, qty = '1', type = 'limit') => ({ legs: [{ position_effect: 'open', side: 'buy' }], price, quantity: qty, type })
const noon = new Date('2026-10-19T16:00:00Z') // Mon 12:00 ET

test('slot rules: window, mood cap, entries, halt, limit-only; closing orders always pass', async () => {
  const calm = { mood: 'calm', buffer: 500, day: '2026-10-19', entries_today: 0, day_realized: 0 }
  expect(check(open('2.40'), calm, noon)).toBe('')
  expect(check(open('2.40'), calm, new Date('2026-10-19T14:00:00Z'))).toContain('10:30-14:30') // 10:00 ET
  expect(check(open('2.40'), { ...calm, mood: 'stressed' }, noon)).toContain('$100 cap')
  expect(check(open('0.95'), { ...calm, mood: 'stressed' }, noon)).toBe('')
  expect(check(open('0.95'), { ...calm, mood: 'stressed', entries_today: 1 }, noon)).toContain('1 entry')
  expect(check(open('2.40'), { ...calm, buffer: 290 }, noon)).toContain('HALTED')
  expect(check(open('2.40', '1', 'market'), calm, noon)).toContain('limit')
  expect(check(open('2.40'), { ...calm, day_realized: -101 }, noon)).toContain('day stop')
  expect(check({ legs: [{ position_effect: 'close', side: 'sell' }], price: '9', type: 'stop_market' }, { mood: 'stressed', buffer: 100 }, new Date('2026-10-19T19:50:00Z'))).toBe('')
})

test('a closing order goes straight through the gate (protection is never blocked)', async ($, on) => {
  on('tool.call', async () => ({ result: 'placed', text: 'placed' }) as never)
  const call = (i: Record<string, unknown>) => ($.tool.call as unknown as (x: Record<string, unknown>) => Promise<{ deny?: string; isError?: boolean; text?: string }>)(i)
  const order = { tool: 'mcp__Robinhood__place_option_order', account_number: 'a', legs: [{ option_id: 'x', side: 'buy', position_effect: 'close' }], quantity: '1', price: '3.00' }
  const closing = await call(order)
  expect(closing.isError === true).toBe(false)
})
