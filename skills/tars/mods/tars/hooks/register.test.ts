import { test, expect } from 'claude-code/testing'

const ordersText = JSON.stringify({ data: { orders: [{ id: 'stop-1', symbol: 'BE', trigger: 'stop', side: 'sell' }] } })

test('blocks cancelling a live stop with no replacement, allows it after one', async ($, on) => {
  on('tool.call', async ($, e) => {
    const name = (e as { tool: string }).tool
    if (name.endsWith('get_equity_orders')) return { result: ordersText, text: ordersText } as never
    return { result: 'ok', text: 'ok' } as never
  })
  const call = (input: Record<string, unknown>) => ($.tool.call as unknown as (i: Record<string, unknown>) => Promise<{ deny?: string; isError?: boolean; text?: string }>)(input)
  await call({ tool: 'mcp__Robinhood__get_equity_orders', account_number: 'a' })
  const first = await call({ tool: 'mcp__Robinhood__cancel_equity_order', account_number: 'a', order_id: 'stop-1' })
  expect(first.isError === true || typeof first.deny === 'string').toBe(true)
  await call({ tool: 'mcp__Robinhood__place_equity_order', account_number: 'a', symbol: 'BE', side: 'sell', type: 'stop_market', quantity: '2', stop_price: '217' })
  const second = await call({ tool: 'mcp__Robinhood__cancel_equity_order', account_number: 'a', order_id: 'stop-1' })
  expect(second.isError === true).toBe(false)
})
