// Appointments: confirmation when booked, reminders the day before and 2 hours before, a "did they show?"
// check 30 minutes after, and a "sorry we missed you" text for no-shows.
// Also publishes a calendar feed (.ics) for Google Calendar / iPhone / Outlook.
const store = require('./db');
const queue = require('./queue');

const { db } = store;
db.exec(`
CREATE TABLE IF NOT EXISTS appointments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
  starts_at TEXT NOT NULL,
  duration_min INTEGER NOT NULL DEFAULT 60,
  type TEXT NOT NULL DEFAULT 'visit',
  stock_number TEXT DEFAULT '',
  notes TEXT DEFAULT '',
  status TEXT NOT NULL DEFAULT 'scheduled',  -- scheduled | confirmed | showed | no_show | cancelled
  reminder_day_done INTEGER NOT NULL DEFAULT 0,
  reminder_2h_done INTEGER NOT NULL DEFAULT 0,
  outcome_task_done INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_appt_time ON appointments(starts_at);
`);

const TYPES = { test_drive: 'Test drive', appraisal: 'Trade appraisal', visit: 'Visit', delivery: 'Delivery', phone_call: 'Phone call' };

function tzOffsetMs(date, tz) {
  const p = Object.fromEntries(new Intl.DateTimeFormat('en-US', { timeZone: tz, hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' })
    .formatToParts(date).map((x) => [x.type, x.value]));
  return Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour % 24, +p.minute, +p.second) - date.getTime();
}
/** "2026-11-20" + "14:30" in the dealership's time zone -> ISO (UTC) */
function localToIso(dateStr, timeStr, tz) {
  const [y, mo, d] = String(dateStr).split('-').map(Number);
  const [h, mi] = String(timeStr || '00:00').split(':').map(Number);
  if (!y || !mo || !d) throw new Error('Date must look like 2026-11-20');
  const guess = Date.UTC(y, mo - 1, d, h || 0, mi || 0);
  let ts = guess - tzOffsetMs(new Date(guess), tz);
  ts = guess - tzOffsetMs(new Date(ts), tz);
  return new Date(ts).toISOString();
}
const fmt = (iso, tz, opts) => new Date(iso).toLocaleString('en-US', { timeZone: tz, ...opts });
const formatLocal = (iso, tz) => fmt(iso, tz, { weekday: 'long', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
const formatClock = (iso, tz) => fmt(iso, tz, { hour: 'numeric', minute: '2-digit' });

function get(id) {
  return db.prepare(`SELECT a.*, c.first_name, c.last_name, c.phone, c.email, c.stage FROM appointments a JOIN customers c ON c.id = a.customer_id WHERE a.id = ?`).get(id);
}
function list({ from, to, customer_id, includeCancelled = false } = {}) {
  const where = [];
  const params = [];
  if (from) { where.push('a.starts_at >= ?'); params.push(from); }
  if (to) { where.push('a.starts_at < ?'); params.push(to); }
  if (customer_id) { where.push('a.customer_id = ?'); params.push(customer_id); }
  if (!includeCancelled) where.push("a.status != 'cancelled'");
  return db.prepare(`SELECT a.*, c.first_name, c.last_name, c.phone, c.email, c.stage FROM appointments a JOIN customers c ON c.id = a.customer_id
    ${where.length ? 'WHERE ' + where.join(' AND ') : ''} ORDER BY a.starts_at`).all(...params);
}

function extraFor(a, tz) {
  return { appt_type: (TYPES[a.type] || 'your visit').toLowerCase(), appt_time: formatLocal(a.starts_at, tz), appt_clock: formatClock(a.starts_at, tz) };
}
function queueAppt(a, key, source) {
  const s = store.getSettings();
  const tpl = store.apptTemplate(key);
  if (!tpl) return null;
  return queue.queueTemplate({ id: a.customer_id }, tpl, { source, appointment_id: a.id, extra: extraFor(a, s.timezone) });
}

/** Book. Provide starts_at (ISO) or date + time (dealership local). Moves the customer to the Appointment stage. */
function create(data) {
  const s = store.getSettings();
  const c = store.getCustomerRow(Number(data.customer_id));
  if (!c) throw new Error('Customer not found');
  if (c.stage === 'dnc') throw new Error('This customer is Do Not Contact');
  const starts_at = data.starts_at ? new Date(data.starts_at).toISOString() : localToIso(data.date, data.time, s.timezone);
  if (Number.isNaN(new Date(starts_at).getTime())) throw new Error('Invalid date/time');
  const now = store.nowIso();
  const stock = store.normalizeStock(data.stock_number || '');
  const r = db.prepare(`INSERT INTO appointments (customer_id, starts_at, duration_min, type, stock_number, notes, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`)
    .run(c.id, starts_at, Number(data.duration_min) || 60, TYPES[data.type] ? data.type : 'visit', stock, data.notes || '', now, now);
  const a = get(Number(r.lastInsertRowid));
  if (stock) store.addInterests(c.id, [stock]);
  if (c.stage !== 'appointment' && c.stage !== 'sold') store.setStage(c.id, 'appointment');
  // Booking is a two-way conversation: clear "replied" so they aren't double-listed.
  db.prepare("UPDATE tasks SET status = 'done', done_at = ? WHERE customer_id = ? AND status = 'pending' AND source = 'reply'").run(now, c.id);
  const task = new Date(starts_at) > new Date() ? queueAppt(a, 'confirm', 'appointment') : null;
  return { appointment: get(a.id), confirmation_task: task };
}

/** Reschedule, cancel, or record the outcome: showed | no_show. */
function update(id, data) {
  const a = get(id);
  if (!a) throw new Error('Appointment not found');
  const s = store.getSettings();
  let starts_at = a.starts_at;
  if (data.starts_at) starts_at = new Date(data.starts_at).toISOString();
  else if (data.date || data.time) {
    const cur = store.localParts(new Date(a.starts_at), s.timezone);
    starts_at = localToIso(data.date || cur.date, data.time || `${String(cur.hour).padStart(2, '0')}:${String(cur.minute).padStart(2, '0')}`, s.timezone);
  }
  const moved = starts_at !== a.starts_at;
  const status = data.status || (moved && ['no_show', 'cancelled'].includes(a.status) ? 'scheduled' : a.status);
  db.prepare(`UPDATE appointments SET starts_at = ?, duration_min = ?, type = ?, notes = ?, status = ?, reminder_day_done = ?, reminder_2h_done = ?, outcome_task_done = ?, updated_at = ? WHERE id = ?`)
    .run(starts_at, Number(data.duration_min ?? a.duration_min), TYPES[data.type] ? data.type : a.type, data.notes ?? a.notes, status,
      moved ? 0 : a.reminder_day_done, moved ? 0 : a.reminder_2h_done, moved ? 0 : a.outcome_task_done, store.nowIso(), id);
  const out = get(id);
  // Clear the outcome check once answered.
  if (['showed', 'no_show', 'cancelled'].includes(status) || moved) {
    db.prepare("UPDATE tasks SET status = 'done', done_at = ? WHERE appointment_id = ? AND status = 'pending' AND source IN ('outcome','reminder')").run(store.nowIso(), id);
  }
  if (moved && new Date(starts_at) > new Date() && status !== 'cancelled') queueAppt(out, 'confirm', 'appointment');
  if (data.status === 'no_show' && a.status !== 'no_show') {
    queueAppt(out, 'no_show', 'no_show');
    const c = store.getCustomerRow(out.customer_id);
    if (c.stage === 'appointment') store.setStage(c.id, c.prev_stage && c.prev_stage !== 'appointment' ? c.prev_stage : 'be_back');
  }
  if (data.status === 'showed' && data.result) {
    // result: sold | unsold (unsold -> be-back with the one objection)
    if (data.result === 'sold') store.setStage(out.customer_id, 'sold');
    else {
      if (data.objection) store.updateCustomer(out.customer_id, { objection: data.objection });
      store.setStage(out.customer_id, 'be_back');
    }
  }
  if (data.status === 'cancelled') {
    const c = store.getCustomerRow(out.customer_id);
    if (c.stage === 'appointment') store.setStage(c.id, c.prev_stage && c.prev_stage !== 'appointment' ? c.prev_stage : 'be_back');
  }
  return get(id);
}
function remove(id) { db.prepare('DELETE FROM appointments WHERE id = ?').run(id); }

/** Every minute: queue reminders and "did they show?" checks. */
function tick() {
  const s = store.getSettings();
  const now = Date.now();
  let n = 0;
  const open = db.prepare("SELECT * FROM appointments WHERE status IN ('scheduled','confirmed') AND starts_at > ? AND starts_at <= ?")
    .all(new Date(now - 12 * 3600000).toISOString(), new Date(now + 36 * 3600000).toISOString());
  const today = store.localParts(new Date(now), s.timezone).date;
  const tomorrow = store.localParts(new Date(now + 86400000), s.timezone).date;
  for (const a of open) {
    const t = new Date(a.starts_at).getTime();
    const apptDay = store.localParts(new Date(t), s.timezone).date;
    const created = new Date(a.created_at).getTime();
    if (s.appt_reminders === '1' && !a.reminder_day_done && apptDay === tomorrow && store.localParts(new Date(now), s.timezone).hour >= 10) {
      if (now - created > 3 * 3600000) { queueAppt(a, 'reminder_day', 'reminder'); n++; }
      db.prepare('UPDATE appointments SET reminder_day_done = 1 WHERE id = ?').run(a.id);
    }
    if (s.appt_reminders === '1' && !a.reminder_2h_done && t - now <= 2 * 3600000 && t > now) {
      if (now - created > 3 * 3600000 && apptDay === today) { queueAppt(a, 'reminder_2h', 'reminder'); n++; }
      db.prepare('UPDATE appointments SET reminder_2h_done = 1, reminder_day_done = 1 WHERE id = ?').run(a.id);
    }
    if (!a.outcome_task_done && now >= t + 30 * 60000) {
      queue.addTask({ customer_id: a.customer_id, kind: 'check', source: 'outcome', appointment_id: a.id,
        title: `Did ${a.first_name} ${a.last_name} show for the ${(TYPES[a.type] || 'appointment').toLowerCase()} at ${formatClock(a.starts_at, s.timezone)}?` });
      db.prepare('UPDATE appointments SET outcome_task_done = 1 WHERE id = ?').run(a.id);
      n++;
    }
  }
  return n;
}

/** A reply of "C" / "yes" to a reminder confirms the next appointment instead of going to the call list. */
function handleConfirmReply(customerId, body) {
  if (!/^\s*(c|confirm|confirmed|yes|yep|y|yes it does|see you then)\s*[.!]*\s*$/i.test(body || '')) return false;
  const a = db.prepare("SELECT * FROM appointments WHERE customer_id = ? AND status = 'scheduled' AND starts_at > ? ORDER BY starts_at LIMIT 1").get(customerId, store.nowIso());
  if (!a) return false;
  db.prepare("UPDATE appointments SET status = 'confirmed', updated_at = ? WHERE id = ?").run(store.nowIso(), a.id);
  return true;
}

// ---- calendar feed (.ics) ----
const icsEsc = (s) => String(s || '').replace(/\\/g, '\\\\').replace(/\n/g, '\\n').replace(/[,;]/g, (m) => '\\' + m);
const icsDate = (iso) => new Date(iso).toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
function icsFeed() {
  const s = store.getSettings();
  const lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Dealer Autopilot//EN', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH',
    `X-WR-CALNAME:${icsEsc((s.dealership || 'Sales') + ' appointments')}`, 'REFRESH-INTERVAL;VALUE=DURATION:PT15M'];
  for (const a of list({ from: new Date(Date.now() - 60 * 86400000).toISOString(), includeCancelled: true })) {
    const end = new Date(new Date(a.starts_at).getTime() + a.duration_min * 60000).toISOString();
    const who = `${a.first_name} ${a.last_name}`.trim() || 'Customer';
    const veh = a.stock_number ? store.vehicleLabel(a.stock_number) || `#${a.stock_number}` : '';
    lines.push('BEGIN:VEVENT', `UID:appt-${a.id}@dealer-autopilot`, `DTSTAMP:${icsDate(a.updated_at)}`, `DTSTART:${icsDate(a.starts_at)}`, `DTEND:${icsDate(end)}`,
      `SUMMARY:${icsEsc(`${TYPES[a.type] || 'Appt'}: ${who}${veh ? ' - ' + veh : ''}`)}`,
      `DESCRIPTION:${icsEsc([a.phone && 'Phone: ' + a.phone, a.stock_number && 'Stock #' + a.stock_number, a.notes, 'Status: ' + a.status].filter(Boolean).join('\n'))}`,
      `STATUS:${a.status === 'cancelled' ? 'CANCELLED' : a.status === 'confirmed' ? 'CONFIRMED' : 'TENTATIVE'}`,
      'BEGIN:VALARM', 'TRIGGER:-PT30M', 'ACTION:DISPLAY', `DESCRIPTION:${icsEsc(who)}`, 'END:VALARM', 'END:VEVENT');
  }
  lines.push('END:VCALENDAR');
  return lines.map((l) => (l.length > 74 ? l.match(/.{1,73}/g).join('\r\n ') : l)).join('\r\n') + '\r\n';
}

module.exports = { TYPES, create, update, remove, get, list, tick, handleConfirmReply, icsFeed, localToIso, formatLocal };
