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
