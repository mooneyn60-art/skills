// The daily list. The cadences don't send anything by themselves: when a step is due, it becomes a task:
//   - "Call these"   (call steps, customers who replied, appointment outcomes)
//   - "Approve these" (drafted texts and emails, ready to send with one tap)
// Only templates you approved for automation (Sold stage + appointment messages) go out on their own,
// and only to customers with recorded consent, inside 8 am - 9 pm.
const config = require('./config');
const store = require('./db');
const { render, smsLink, sendTwilio, sendEmail } = require('./messaging');

const { db } = store;
const name = (c) => `${c.first_name} ${c.last_name}`.trim() || c.phone || c.email || 'Customer';

function addTask(t) {
  const r = db.prepare(`INSERT INTO tasks (customer_id, kind, title, subject, body, due_at, status, source, step_id, appointment_id, auto, blocked_reason, created_at)
    VALUES (?, ?, ?, ?, ?, ?, 'pending', ?, ?, ?, ?, ?, ?)`).run(t.customer_id, t.kind, t.title, t.subject || '', t.body || '', t.due_at || store.nowIso(),
    t.source, t.step_id ?? null, t.appointment_id ?? null, t.auto ? 1 : 0, t.blocked_reason || null, store.nowIso());
  return getTask(Number(r.lastInsertRowid));
}
function getTask(id) {
  return db.prepare(`SELECT t.*, c.first_name, c.last_name, c.phone, c.email, c.stage, c.status AS customer_status, c.consent, c.objection,
      (SELECT group_concat(stock_number, ', ') FROM interests WHERE customer_id = c.id) AS stocks
    FROM tasks t JOIN customers c ON c.id = t.customer_id WHERE t.id = ?`).get(id);
}
function hasPending(customerId, source) {
  return !!db.prepare("SELECT 1 FROM tasks WHERE customer_id = ? AND source = ? AND status = 'pending'").get(customerId, source);
}

/** Should this template go out without asking? */
function isAuto(step, settings) {
  return !!(step && step.auto && step.approved && settings.automation_enabled === '1' && store.STAGES[step.stage]?.auto_ok && step.channel !== 'call');
}

/** Turn a template into a task for one customer, applying the compliance gate. */
function queueTemplate(c, step, { source, appointment_id, extra, due_at } = {}) {
  const settings = store.getSettings();
  const cust = store.getCustomer(c.id);
  const body = render(step.body, cust, extra, settings);
  if (step.channel === 'call') {
    if (store.blockReason(cust, 'call')) return null;
    return addTask({ customer_id: c.id, kind: 'call', title: body, source, step_id: step.id, appointment_id, due_at });
  }
  const blocked = store.blockReason(cust, step.channel);
  if (blocked) {
    if (blocked.startsWith('No recorded consent') && cust.phone && !hasPending(c.id, 'consent') && !store.blockReason(cust, 'call')) {
      addTask({ customer_id: c.id, kind: 'call', source: 'consent',
        title: `Call ${name(cust)}. Ask if it's OK to text and email them, then tick "Consent" on their record. (A ${step.channel === 'sms' ? 'text' : 'email'} is waiting.)` });
    }
    store.logMessage({ customer_id: c.id, direction: 'out', channel: step.channel, body, status: 'skipped', error: blocked, step_id: step.id });
    return null;
  }
  return addTask({
    customer_id: c.id, kind: step.channel, source, step_id: step.id, appointment_id, due_at,
    title: `${step.channel === 'sms' ? 'Text' : 'Email'} ${name(cust)}`,
    subject: step.channel === 'email' ? render(step.subject || 'A note from {dealership}', cust, extra, settings) : '',
    body, auto: isAuto(step, settings),
  });
}

/** Every minute: turn due cadence steps into tasks. */
function generateDue() {
  const due = db.prepare(`SELECT * FROM customers WHERE status = 'active' AND next_touch_at IS NOT NULL AND next_touch_at <= ? ORDER BY next_touch_at LIMIT 200`).all(store.nowIso());
  let n = 0;
  for (const first of due) {
    // A customer can have several steps due at once (e.g. the day-0 text, email and call).
    for (let guard = 0; guard < 6; guard++) {
      const c = store.getCustomerRow(first.id);
      if (!c || c.status !== 'active' || !c.next_touch_at || c.next_touch_at > store.nowIso()) break;
      n += runStep(c);
    }
  }
  return n;
}

function runStep(c) {
  let n = 0;
  {
    const step = store.getSteps(c.stage)[c.step_index];
    // Don't stack up: if an earlier drafted message for this customer is still waiting, skip it in favour of the newer one.
    if (step && step.channel !== 'call') {
      db.prepare("UPDATE tasks SET status = 'skipped', done_at = ? WHERE customer_id = ? AND status = 'pending' AND source = 'sequence' AND kind = ?")
        .run(store.nowIso(), c.id, step.channel);
    }
    if (step && queueTemplate(c, step, { source: 'sequence' })) n++;
    db.prepare('UPDATE customers SET step_index = step_index + 1 WHERE id = ?').run(c.id);
    store.reschedule(c.id);
  }
  return n;
}

/**
 * Complete a task.
 *  action "send": deliver the (optionally edited) text/email. In phone mode the text is logged as sent and a link
 *                 to open it in your Messages app is returned.
 *  action "done": a call was made (outcome note optional) or the task was handled.
 *  action "skip": drop it.
 */
async function completeTask(id, { action = 'send', body, subject, note } = {}) {
  const t = getTask(id);
  if (!t) throw new Error('Task not found');
  if (t.status !== 'pending') return { status: t.status };
  const finish = (status = 'done') => db.prepare('UPDATE tasks SET status = ?, done_at = ? WHERE id = ?').run(status, store.nowIso(), id);

  if (action === 'skip') { finish('skipped'); return { status: 'skipped' }; }

  if (t.kind === 'call' || action === 'done') {
    if (t.kind === 'call') store.logMessage({ customer_id: t.customer_id, direction: 'out', channel: 'call', body: note ? `Call: ${note}` : `Call: ${t.title}`, status: 'logged' });
    finish();
    return { status: 'done' };
  }

  const c = store.getCustomer(t.customer_id);
  const settings = store.getSettings();
  const text = body ?? t.body;
  const subj = subject ?? t.subject;
  if (/\[[^\]]+\]/.test(text) || /\[[^\]]+\]/.test(subj || '')) throw new Error('Fill in the [bracketed] parts before sending');
  const blocked = store.blockReason(c, t.kind);
  if (blocked) throw new Error(`Can't send: ${blocked}`);
  if (t.kind === 'sms' && !store.inTextWindow(settings)) throw new Error(`Texts can only go out between ${settings.text_start_hour}:00 and ${settings.text_end_hour}:00`);

  let result;
  try {
    if (t.kind === 'email') result = await sendEmail(c, subj, text);
    else if (settings.text_mode === 'twilio') result = await sendTwilio(c.phone, text);
    else result = { status: 'sent', sms_link: smsLink(c.phone, text) };
  } catch (err) {
    store.logMessage({ customer_id: c.id, direction: 'out', channel: t.kind, subject: subj, body: text, status: 'failed', error: err.message, step_id: t.step_id });
    throw err;
  }
  store.logMessage({ customer_id: c.id, direction: 'out', channel: t.kind, subject: t.kind === 'email' ? subj : null, body: text,
    status: result.status, step_id: t.step_id, automated: action === 'auto' });
  finish();
  return result;
}

/** Send the tasks that are allowed to go automatically. Texts in phone mode can't send themselves; they stay on the list. */
async function autoSend() {
  const settings = store.getSettings();
  if (settings.automation_enabled !== '1') return 0;
  const rows = db.prepare("SELECT id, kind FROM tasks WHERE status = 'pending' AND auto = 1 AND due_at <= ? ORDER BY due_at LIMIT 30").all(store.nowIso());
  let n = 0;
  for (const r of rows) {
    if (r.kind === 'sms' && settings.text_mode !== 'twilio') continue;
    if (!store.inTextWindow(settings)) break;
    try { await completeTask(r.id, { action: 'auto' }); n++; } catch (e) {
      db.prepare('UPDATE tasks SET auto = 0, blocked_reason = ? WHERE id = ?').run(e.message, r.id);
    }
  }
  return n;
}

/**
 * The customer replied. Stop all automation for them and put them on the call list.
 * (With your own phone, replies come to you: tap "They replied". With Twilio, this runs on its own.)
 */
function markReplied(customerId, text = '', channel = 'sms') {
  const c = store.getCustomerRow(customerId);
  if (!c) throw new Error('Customer not found');
  store.logMessage({ customer_id: c.id, direction: 'in', channel, body: text || '(replied - logged by you)', status: 'received' });
  if (c.stage === 'dnc') return { action: 'dnc' };
  db.prepare("UPDATE customers SET status = 'replied', next_touch_at = NULL, updated_at = ? WHERE id = ?").run(store.nowIso(), c.id);
  db.prepare("UPDATE tasks SET status = 'skipped', done_at = ? WHERE customer_id = ? AND status = 'pending' AND source = 'sequence'").run(store.nowIso(), c.id);
  if (!hasPending(c.id, 'reply')) {
    addTask({ customer_id: c.id, kind: 'call', source: 'reply', title: `${name(c)} replied${text ? `: "${text.slice(0, 140)}"` : ''}. Get back to them now.` });
  }
  return { action: 'call_list' };
}

const STOP = /^\s*(stop|stopall|unsubscribe|cancel|end|quit|opt ?out|remove me|don'?t text me|do not text)\b/i;
/** Inbound text via Twilio: STOP words = do not contact, forever. Anything else = replied. */
function handleInboundSms(from, body) {
  const phone = store.normalizePhone(from);
  let c = db.prepare('SELECT * FROM customers WHERE phone = ?').get(phone);
  if (!c) c = store.upsertCustomer({ phone, stage: 'new_lead', source: 'Inbound text' }).customer;
  if (STOP.test(body || '')) {
    store.logMessage({ customer_id: c.id, direction: 'in', channel: 'sms', body, status: 'received' });
    store.setStage(c.id, 'dnc');
    return { action: 'opted_out' };
  }
  if (require('./appointments').handleConfirmReply(c.id, body)) {
    store.logMessage({ customer_id: c.id, direction: 'in', channel: 'sms', body, status: 'received' });
    return { action: 'appointment_confirmed' };
  }
  return markReplied(c.id, body);
}

/** The morning list. */
function dailyList() {
  const settings = store.getSettings();
  const rows = db.prepare(`SELECT t.id FROM tasks t WHERE t.status = 'pending' AND t.due_at <= ? ORDER BY
      CASE t.source WHEN 'new_lead' THEN 0 WHEN 'reply' THEN 1 WHEN 'outcome' THEN 2 WHEN 'appointment' THEN 3 WHEN 'reminder' THEN 3
        WHEN 'no_show' THEN 4 WHEN 'referral' THEN 5 WHEN 'match' THEN 6 ELSE 8 END, t.due_at`)
    .all(new Date(Date.now() + 2 * 3600000).toISOString()).map((r) => getTask(r.id));
  const calls = rows.filter((t) => t.kind === 'call' || t.kind === 'check');
  const messages = rows.filter((t) => t.kind === 'sms' || t.kind === 'email');
  return {
    calls,
    approve: messages.filter((t) => !t.auto),
    automatic: messages.filter((t) => t.auto),
    text_mode: settings.text_mode,
    in_text_window: store.inTextWindow(settings),
    call_target: Number(settings.daily_call_target) || 5,
  };
}

module.exports = { addTask, getTask, queueTemplate, generateDue, completeTask, autoSend, markReplied, handleInboundSms, dailyList, isAuto };
