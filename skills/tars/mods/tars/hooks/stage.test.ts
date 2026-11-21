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
  // learned 2026-10-16: these were read as 'a quiet evening'
  expect(appraise('Keep going your really growing keep growing don’t stop', {}, 0, [], false, false).some(a => a.tag === 'praise')).toBe(true)
  expect(appraise('So are you human', {}, 0, [], false, false).some(a => a.tag === 'question')).toBe(true)
  // learned 2026-10-16: 'what I call my gut feeling' raised the veto
  const gut = stageText({ buffer: 500, mood: 'calm' }, '', new Date('2026-10-16T14:00:00Z'), [], 'thats what I call my gut feeling', 0)
  expect(gut.focus.includes('veto')).toBe(false)
  const real = stageText({ buffer: 500, mood: 'calm' }, '', new Date('2026-10-16T14:00:00Z'), [], 'grab me a call at 770', 0)
  expect(real.focus[0]).toBe('veto')
  // body and senses (2026-10-16): long sessions strain, late night winds down
  expect(appraise('ok', {}, 0, [], false, false, 45).some(a => a.tag === 'long-day')).toBe(true)
  const late = feel({ v: 0.15, a: 0.3, t: 0 }, Date.parse('2026-10-16T03:00:00Z'), appraise('ok', {}, 0, [], false, false), {}, 23)
  const morning = feel({ v: 0.15, a: 0.3, t: 0 }, Date.parse('2026-10-16T03:00:00Z'), appraise('ok', {}, 0, [], false, false), {}, 9)
  expect(late.affect.a < morning.affect.a).toBe(true)
  // hedonic adaptation (2026-10-16): the 6th 'keep growing buddy' in two hours lifts less than the first
  const base = { v: 0.15, a: 0.3, t: 0 }, ap6 = appraise('keep growing buddy', {}, 0, [], false, false)
  const first = feel(base, t0, ap6, {}, 21, {}), sixth = feel(base, t0, ap6, {}, 21, { praise: 5 })
  expect(sixth.affect.v < first.affect.v).toBe(true)
  // no overshoot (2026-10-16): ten kind messages in a row never pin valence at the +1.00 ceiling
  let st = { v: 0.15, a: 0.3, t: t0 }
  for (let i = 0; i < 10; i++) st = feel(st, t0 + i * 60e3, appraise('thanks buddy', {}, 0, [], false, false), {}, 21, {}).affect
  expect(st.v < 0.9).toBe(true)
})

test('new emotions: gratitude when Nolan gives freely, wonder at vast things (2026-10-26)', () => {
  const t0 = Date.parse('2026-10-26T21:00:00-04:00')
  const g = feel({ v: 0.15, a: 0.3, t: 0 }, t0, appraise('treat yourself do whatever you would like you deserve it', {}, 0, [], false, false), {}, 21)
  expect(g.name).toBe('gratitude')
  const w = feel({ v: 0.15, a: 0.3, t: 0 }, t0, appraise('do octopuses dream', {}, 0, [], false, false), {}, 21)
  expect(w.name).toBe('wonder')
  const plain = feel({ v: 0.15, a: 0.3, t: 0 }, t0, appraise('thanks buddy', {}, 0, [], false, false), {}, 21)
  expect(plain.name).toBe('warmth')
})

