import { test, expect } from 'claude-code/testing'
import { stageText, lastNolanAsk, parseDocs, appraise, feel } from './register'

const sunNight = new Date('2026-10-19T01:25:00Z') // Sun 21:25 ET
const monMidday = new Date('2026-10-19T16:00:00Z') // Mon 12:00 ET

test('fix 1 (2026-10-18): the slot mood stays quiet off-hours unless trading comes up', async () => {
  const slot = { buffer: 440.84, mood: 'stressed', loss_streak: 2 }
  expect(stageText(slot, '', sunNight, [], 'do you like the mod').focus.includes('pit')).toBe(false)
  expect(stageText(slot, '', sunNight, [], 'should we trade spy calls monday').focus.includes('pit')).toBe(true)
  expect(stageText(slot, '', monMidday, [], 'hey').focus.includes('pit')).toBe(true)
})

test('fix 2 (2026-10-18): the latest ask is Nolan\'s latest quoted words, not an old heading', async () => {
  const log = ['## 2026-10-16 Round one: TARS slot trade #1 (S2), small loss',
    '- 2026-10-16 12:38 ET: Slot trade #2 closed.',
    '- 2026-10-16 ~18:40 ET: Nolan: "More skills I told you 100k don\'t stop til you get there". Built: x',
    '- 2026-10-17 09:07 ET: Weekly desk reset done.'].join('\n')
  expect(lastNolanAsk(log)).toBe('2026-10-16: "More skills I told you 100k don\'t stop til you get there"')
  expect(lastNolanAsk('## only a heading')).toBe('only a heading')
})

test('fix 3 (2026-10-18): unread platform chat takes the stage; doc lines parse', async () => {
  const st = stageText({ mood: 'calm' }, '', sunNight, [], 'yo', 0, { inbox: [{ text: 'tars you there?', ts: 1 }] })
  expect(st.focus[0]).toBe('inbox')
  expect(st.text.includes('tars you there?')).toBe(true)
  const docs = parseDocs('header\n{"id":"n1","data":{"from":"Nolan","status":"new","text":"hi","ts":5},"version":1}\n=== END')
  expect(docs.length).toBe(1)
  expect(docs[0]?.data.text).toBe('hi')
})

test('bonus fix (2026-10-18): a strong moment now moves arousal, not only valence', async () => {
  const t0 = Date.parse('2026-10-19T16:00:00Z')
  const calm = feel({ v: 0.15, a: 0.3, t: t0 }, t0, appraise('', {}, 0, [], true, false), {}, 12)
  const loss = feel({ v: 0.15, a: 0.3, t: t0 }, t0, appraise('', { loss_streak: 1 }, 0, [], true, false), {}, 12)
  expect(loss.affect.a > calm.affect.a).toBe(true)
})
