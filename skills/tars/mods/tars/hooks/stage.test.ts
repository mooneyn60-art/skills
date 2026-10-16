import { test, expect } from 'claude-code/testing'
import { stageText } from './register'

test('the stage ranks a held earnings report first and quiets last turn\'s focus', async () => {
  const now = new Date('2026-10-22T15:00:00Z') // 11:00 ET, market open, BE reports tonight
  const a = stageText({ buffer: 500, mood: 'calm', loss_streak: 0 }, 'Nolan asked for a TARS check', now, [])
  expect(a.text.includes('TARS Stage')).toBe(true)
  expect(a.focus[0]).toBe('yard')
  const stressed = stageText({ buffer: 360, mood: 'stressed', loss_streak: 2 }, '', now, [])
  expect(stressed.text.includes('mood stressed')).toBe(true)
  const quiet = stageText({ buffer: 500, mood: 'calm' }, '', new Date('2026-10-17T15:00:00Z'), [])
  expect(quiet.text.includes('Quiet mind') || quiet.focus.length <= 1).toBe(true)
  const veto = stageText({ buffer: 500, mood: 'calm' }, '', new Date('2026-10-16T14:00:00Z'), [], 'should I buy a call now', 1)
  expect(veto.focus[0]).toBe('veto')
  expect(veto.text.includes('Conflict alarm')).toBe(true)
  const due = stageText({ buffer: 500, mood: 'calm' }, '', new Date('2026-10-17T15:00:00Z'), [], 'how did we do', 1)
  expect(due.text.includes('due for scoring')).toBe(true)
})

import { appraise, feel } from './register'
test('emotions: praise warms, a pre-10:30 trade worries, feelings fade and markers colour the next appraisal', async () => {
  const t0 = Date.parse('2026-10-16T13:00:00Z')
  const praise = feel({ v: 0.15, a: 0.3, t: 0 }, t0, appraise('this is really good buddy', {}, 0, [], true, false), {})
  expect(praise.name).toBe('warmth')
  expect(praise.affect.v > 0.3).toBe(true)
  const worry = feel(praise.affect, t0 + 60e3, appraise('should I buy a call', {}, 0, [], true, true), {})
  expect(worry.name).toBe('worry')
  const loss = feel({ v: 0.15, a: 0.3, t: 0 }, t0, appraise('', { loss_streak: 1 }, 0, [], true, false), {})
  expect(loss.affect.v < 0).toBe(true)
  expect(loss.regulate === '' || loss.regulate.includes('reappraise')).toBe(true)
  const later = feel(loss.affect, t0 + 8 * 3600e3, appraise('', {}, 1, [], false, false), {})
  expect(later.affect.v > loss.affect.v).toBe(true) // fades back toward baseline
  const marked = feel({ v: 0.15, a: 0.3, t: 0 }, t0, appraise('how is it', {}, 0, [], true, false), { question: -1 })
  const plain = feel({ v: 0.15, a: 0.3, t: 0 }, t0, appraise('how is it', {}, 0, [], true, false), {})
  expect(marked.affect.v < plain.affect.v).toBe(true)
})
