// SQLite storage (built into Node 22+, nothing to install).
// Per the FTC Safeguards Rule, this only stores names, contact info, vehicle of interest, stage and notes.
// Never put licence, credit, SSN or income information in here.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { DatabaseSync } = require('node:sqlite');
const config = require('./config');
const { STAGES, GROUPS, DEFAULT_STEPS, APPT_TEMPLATES } = require('./sequences');

fs.mkdirSync(path.dirname(config.dbPath), { recursive: true });
const db = new DatabaseSync(config.dbPath);
db.exec('PRAGMA journal_mode = WAL; PRAGMA foreign_keys = ON;');

db.exec(`
CREATE TABLE IF NOT EXISTS customers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL DEFAULT '',
  last_name TEXT NOT NULL DEFAULT '',
  phone TEXT,
  email TEXT,
  stage TEXT NOT NULL DEFAULT 'new_lead',
  prev_stage TEXT,
  status TEXT NOT NULL DEFAULT 'active',      -- active | paused | replied | completed
  vehicle_interest TEXT DEFAULT '',
  objection TEXT DEFAULT '',                   -- the one thing that held them back
  notes TEXT DEFAULT '',
  source TEXT DEFAULT '',
  consent INTEGER NOT NULL DEFAULT 0,          -- consent to texts/emails
  consent_date TEXT,
  consent_source TEXT DEFAULT '',
  on_dnc_registry INTEGER NOT NULL DEFAULT 0,  -- number is on the national Do Not Call registry
  customer_initiated INTEGER NOT NULL DEFAULT 1, -- they contacted the dealership first
  email_opt_out INTEGER NOT NULL DEFAULT 0,
  step_index INTEGER NOT NULL DEFAULT 0,
  next_touch_at TEXT,
  stage_entered_at TEXT NOT NULL,
  lead_at TEXT,
  first_contact_at TEXT,
  sold_date TEXT,
  last_contact_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_cust_due ON customers(status, next_touch_at);
CREATE INDEX IF NOT EXISTS idx_cust_phone ON customers(phone);
CREATE INDEX IF NOT EXISTS idx_cust_email ON customers(email);

CREATE TABLE IF NOT EXISTS interests (
  customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
  stock_number TEXT NOT NULL,
  added_at TEXT NOT NULL,
  PRIMARY KEY (customer_id, stock_number)
);
CREATE INDEX IF NOT EXISTS idx_interest_stock ON interests(stock_number);

CREATE TABLE IF NOT EXISTS inventory (
  stock_number TEXT PRIMARY KEY,
  year TEXT DEFAULT '', make TEXT DEFAULT '', model TEXT DEFAULT '', trim TEXT DEFAULT '',
  color TEXT DEFAULT '', price TEXT DEFAULT '', miles TEXT DEFAULT '', vin TEXT DEFAULT '',
  status TEXT NOT NULL DEFAULT 'available',
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS steps (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  stage TEXT NOT NULL,
  key TEXT,                      -- set for appointment messages (confirm, reminder_day, reminder_2h, no_show)
  day INTEGER NOT NULL,
  channel TEXT NOT NULL,         -- sms | email | call
  subject TEXT DEFAULT '',
  body TEXT NOT NULL,
  approved INTEGER NOT NULL DEFAULT 0,  -- you approved this template's wording
  auto INTEGER NOT NULL DEFAULT 0       -- send without asking (only allowed for Sold stage)
);

CREATE TABLE IF NOT EXISTS tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
  kind TEXT NOT NULL,            -- call | sms | email
  title TEXT NOT NULL,
  subject TEXT DEFAULT '',
  body TEXT DEFAULT '',
  due_at TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',  -- pending | done | skipped
  source TEXT NOT NULL,          -- sequence | reply | appointment | reminder | no_show | outcome | consent | manual
  step_id INTEGER,
  appointment_id INTEGER,
  auto INTEGER NOT NULL DEFAULT 0,
  blocked_reason TEXT,
  created_at TEXT NOT NULL,
  done_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status, due_at);

CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE,
  direction TEXT NOT NULL,       -- out | in
  channel TEXT NOT NULL,         -- sms | email | call
  subject TEXT,
  body TEXT NOT NULL,
  status TEXT NOT NULL,          -- sent | simulated | failed | received | logged
  error TEXT,
  step_id INTEGER,
  automated INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_msg_customer ON messages(customer_id, created_at);

CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);
`);

const nowIso = () => new Date().toISOString();

// ---------- settings ----------
const DEFAULT_SETTINGS = {
  salesperson: '',
  dealership: '',
  dealer_phone: '',
  dealer_address: '',          // required in marketing emails (CAN-SPAM)
  review_link: '',
  timezone: 'America/New_York',
  work_start_hour: '9',
  work_end_hour: '20',
  text_start_hour: '8',        // never earlier than 8 am
  text_end_hour: '21',         // never later than 9 pm
  text_mode: 'phone',          // phone = texts open on your phone to send from your own number | twilio
  automation_enabled: '0',     // master switch for the safe automations (Sold + appointment reminders)
  daily_call_target: '5',
  crm: 'DealerSocket',
  appt_reminders: '1',
};
const EDITABLE = Object.keys(DEFAULT_SETTINGS);
for (const [k, v] of Object.entries(DEFAULT_SETTINGS)) db.prepare('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)').run(k, v);
for (const k of ['secret', 'mcp_token', 'calendar_token']) {
  db.prepare('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)').run(k, crypto.randomBytes(18).toString('hex'));
}
function getSettings() {
  const out = {};
  for (const r of db.prepare('SELECT key, value FROM settings').all()) out[r.key] = r.value;
  return out;
}
function publicSettings() {
  const { secret, mcp_token, calendar_token, ...s } = getSettings();
  return s;
}
function saveSettings(obj) {
  const stmt = db.prepare('INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value');
  for (const [k, v] of Object.entries(obj || {})) {
    if (!EDITABLE.includes(k)) continue;
    let val = String(v ?? '');
    // The legal texting window can be narrowed but never widened past 8 am - 9 pm.
    if (k === 'text_start_hour') val = String(Math.max(8, Math.min(21, Number(val) || 8)));
    if (k === 'text_end_hour') val = String(Math.min(21, Math.max(8, Number(val) || 21)));
    if (k === 'text_mode' && !['phone', 'twilio'].includes(val)) continue;
    stmt.run(k, val);
  }
  return publicSettings();
}

// ---------- templates (sequence steps) ----------
if (db.prepare('SELECT COUNT(*) AS n FROM steps').get().n === 0) {
  const ins = db.prepare('INSERT INTO steps (stage, day, channel, subject, body) VALUES (?, ?, ?, ?, ?)');
  for (const [stage, steps] of Object.entries(DEFAULT_STEPS)) for (const s of steps) ins.run(stage, s.day, s.channel, s.subject || '', s.body);
  const insKey = db.prepare("INSERT INTO steps (stage, key, day, channel, subject, body) VALUES ('appointment', ?, 0, ?, '', ?)");
  for (const [key, t] of Object.entries(APPT_TEMPLATES)) insKey.run(key, t.channel, t.body);
}
/** The day-by-day cadence for a stage. */
function getSteps(stage) { return db.prepare('SELECT * FROM steps WHERE stage = ? AND key IS NULL ORDER BY day, id').all(stage); }
/** Every template (cadence + appointment messages), for the Templates screen. */
function allTemplates() { return db.prepare('SELECT * FROM steps ORDER BY stage, key IS NOT NULL, day, id').all(); }
function apptTemplate(key) { return db.prepare("SELECT * FROM steps WHERE stage = 'appointment' AND key = ?").get(key); }
function getStep(id) { return db.prepare('SELECT * FROM steps WHERE id = ?').get(id); }
function updateStep(id, data) {
  const s = getStep(id);
  if (!s) throw new Error('Template not found');
  const body = data.body ?? s.body;
  const subject = data.subject ?? s.subject;
  const day = data.day !== undefined && !s.key ? Math.max(0, Number(data.day) || 0) : s.day;
  const channel = !s.key && ['sms', 'email', 'call'].includes(data.channel) ? data.channel : s.channel;
  // Editing the wording un-approves it, so you always see the final text before it automates.
  const changed = body !== s.body || subject !== s.subject || channel !== s.channel;
  const approved = data.approved !== undefined ? (data.approved ? 1 : 0) : changed ? 0 : s.approved;
  let auto = data.auto !== undefined ? (data.auto ? 1 : 0) : s.auto;
  if (!STAGES[s.stage].auto_ok || channel === 'call' || !approved) auto = 0;
  db.prepare('UPDATE steps SET day = ?, channel = ?, subject = ?, body = ?, approved = ?, auto = ? WHERE id = ?').run(day, channel, subject, body, approved, auto, id);
  return getStep(id);
}
function addStep(stage, data) {
  if (!STAGES[stage]) throw new Error('Unknown stage');
  const r = db.prepare('INSERT INTO steps (stage, day, channel, subject, body) VALUES (?, ?, ?, ?, ?)')
    .run(stage, Math.max(0, Number(data.day) || 0), ['sms', 'email', 'call'].includes(data.channel) ? data.channel : 'sms', data.subject || '', data.body || '');
  return getStep(Number(r.lastInsertRowid));
}
function deleteStep(id) { db.prepare('DELETE FROM steps WHERE id = ? AND key IS NULL').run(id); }

// ---------- helpers ----------
function normalizePhone(p) {
  if (!p) return '';
  const raw = String(p).trim();
  const d = raw.replace(/\D/g, '');
  if (raw.startsWith('+')) return '+' + d;
  if (d.length === 10) return '+1' + d;
  if (d.length === 11 && d.startsWith('1')) return '+' + d;
  return d ? '+' + d : '';
}
const normalizeEmail = (e) => (e ? String(e).trim().toLowerCase() : '');
const normalizeStock = (s) => String(s || '').trim().toUpperCase();
const splitStocks = (s) => String(s || '').split(/[,;|/\s]+/).map(normalizeStock).filter(Boolean);

function localParts(date, tz) {
  const p = Object.fromEntries(new Intl.DateTimeFormat('en-US', {
    timeZone: tz, hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit',
  }).formatToParts(date).map((x) => [x.type, x.value]));
  return { date: `${p.year}-${p.month}-${p.day}`, hour: Number(p.hour) % 24, minute: Number(p.minute) };
}

/** Compliance gate. Returns null if allowed, or a plain-English reason it is blocked. */
function blockReason(c, channel) {
  if (c.stage === 'dnc') return 'Do not contact';
  if (channel === 'sms' || channel === 'call') {
    if (!c.phone) return 'No phone number';
    if (c.on_dnc_registry && !c.customer_initiated) return 'On the Do Not Call registry and did not contact you first';
  }
  if (channel === 'sms' && !c.consent) return 'No recorded consent to text';
  if (channel === 'email') {
    if (!c.email) return 'No email address';
    if (c.email_opt_out) return 'Unsubscribed from email';
    if (!c.consent) return 'No recorded consent';
  }
  return null;
}
/** Texts and calls only between 8 am and 9 pm (or your narrower window), dealership time zone. */
function inTextWindow(settings = getSettings(), when = new Date()) {
  const { hour } = localParts(when, settings.timezone);
  return hour >= Math.max(8, Number(settings.text_start_hour)) && hour < Math.min(21, Number(settings.text_end_hour));
}

// ---------- customers ----------
function getCustomerRow(id) { return db.prepare('SELECT * FROM customers WHERE id = ?').get(id); }
function vehicleLabel(stock) {
  const v = db.prepare('SELECT * FROM inventory WHERE stock_number = ?').get(normalizeStock(stock));
  return v ? [v.year, v.make, v.model, v.trim].filter(Boolean).join(' ') : '';
}
function getCustomer(id) {
  const c = getCustomerRow(id);
  if (!c) return null;
  c.interests = db.prepare(`SELECT i.stock_number, v.year, v.make, v.model, v.trim, v.price, v.status AS stock_status
    FROM interests i LEFT JOIN inventory v ON v.stock_number = i.stock_number WHERE i.customer_id = ? ORDER BY i.added_at`).all(id);
  return c;
}
function addInterests(id, stocks) {
  const ins = db.prepare('INSERT OR IGNORE INTO interests (customer_id, stock_number, added_at) VALUES (?, ?, ?)');
  for (const s of stocks) if (normalizeStock(s)) ins.run(id, normalizeStock(s), nowIso());
}
function removeInterest(id, stock) { db.prepare('DELETE FROM interests WHERE customer_id = ? AND stock_number = ?').run(id, normalizeStock(stock)); }

function computeNextTouch(c) {
  if (c.status !== 'active') return null;
  const step = getSteps(c.stage)[c.step_index];
  if (!step) return null;
  return new Date(new Date(c.stage_entered_at).getTime() + step.day * 86400000).toISOString();
}
function reschedule(id) {
  const c = getCustomerRow(id);
  if (!c) return;
  let status = c.status;
  if (status === 'active' && c.step_index >= getSteps(c.stage).length && c.stage !== 'appointment') status = 'completed';
  db.prepare('UPDATE customers SET status = ?, next_touch_at = ?, updated_at = ? WHERE id = ?').run(status, computeNextTouch({ ...c, status }), nowIso(), id);
}

const bool = (v) => (v === true || v === 1 || /^(1|y|yes|true|x|opt.?in|opted in)$/i.test(String(v ?? '').trim()) ? 1 : 0);

/** Create a customer, or merge into an existing one with the same phone/email. */
function upsertCustomer(data) {
  const phone = normalizePhone(data.phone);
  const email = normalizeEmail(data.email);
  const stage = STAGES[data.stage] ? data.stage : 'new_lead';
  const stocks = Array.isArray(data.stock_numbers) ? data.stock_numbers.flatMap(splitStocks) : splitStocks(data.stock_numbers);
  const now = nowIso();
  const existing = (phone && db.prepare('SELECT * FROM customers WHERE phone = ?').get(phone)) || (email && db.prepare('SELECT * FROM customers WHERE email = ?').get(email));

  if (existing) {
    const pick = (k) => data[k] || existing[k];
    db.prepare(`UPDATE customers SET first_name=?, last_name=?, phone=?, email=?, vehicle_interest=?, objection=?, source=?,
      notes=?, updated_at=? WHERE id=?`).run(pick('first_name'), pick('last_name'), phone || existing.phone, email || existing.email,
      pick('vehicle_interest'), pick('objection'), pick('source'),
      data.notes && !String(existing.notes).includes(data.notes) ? [existing.notes, data.notes].filter(Boolean).join('\n') : existing.notes, now, existing.id);
    if (data.consent !== undefined && bool(data.consent) && !existing.consent && existing.stage !== 'dnc') setConsent(existing.id, true, data.consent_source || 'Import', data.consent_date);
    if (data.on_dnc_registry !== undefined && bool(data.on_dnc_registry)) db.prepare('UPDATE customers SET on_dnc_registry = 1 WHERE id = ?').run(existing.id);
    if (data.do_not_contact && bool(data.do_not_contact)) setStage(existing.id, 'dnc');
    addInterests(existing.id, stocks);
    if (data.stage && data.stage !== existing.stage && existing.stage !== 'dnc') setStage(existing.id, stage, { soldDate: data.sold_date });
    return { customer: getCustomer(existing.id), created: false };
  }

  const dnc = data.do_not_contact && bool(data.do_not_contact);
  const consent = dnc ? 0 : bool(data.consent);
  const r = db.prepare(`INSERT INTO customers (first_name, last_name, phone, email, stage, status, vehicle_interest, objection, notes, source,
      consent, consent_date, consent_source, on_dnc_registry, customer_initiated, email_opt_out, stage_entered_at, lead_at, sold_date, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`).run(
    String(data.first_name || '').trim(), String(data.last_name || '').trim(), phone || null, email || null, dnc ? 'dnc' : stage, dnc ? 'completed' : 'active',
    data.vehicle_interest || '', data.objection || '', data.notes || '', data.source || '',
    consent, consent ? (data.consent_date ? new Date(data.consent_date).toISOString() : now) : null, consent ? (data.consent_source || 'Recorded on entry') : '',
    bool(data.on_dnc_registry), data.customer_initiated === undefined ? (stage === 'lost' ? 0 : 1) : bool(data.customer_initiated), dnc ? 1 : 0,
    now, ['new_lead', 'phone_up', 'be_back'].includes(stage) ? (data.lead_at && !isNaN(new Date(data.lead_at)) ? new Date(data.lead_at).toISOString() : now) : null,
    stage === 'sold' ? (data.sold_date || now.slice(0, 10)) : null, now, now);
  const id = Number(r.lastInsertRowid);
  addInterests(id, stocks);
  reschedule(id);
  return { customer: getCustomer(id), created: true };
}

function setConsent(id, yes, source = '', date) {
  db.prepare('UPDATE customers SET consent = ?, consent_date = ?, consent_source = ?, updated_at = ? WHERE id = ?')
    .run(yes ? 1 : 0, yes ? (date ? new Date(date).toISOString() : nowIso()) : null, yes ? source || 'Verbal / in person' : '', nowIso(), id);
}

/** Move to a stage and start that stage's cadence from the beginning. */
function setStage(id, stage, { soldDate } = {}) {
  if (!STAGES[stage]) throw new Error('Unknown stage ' + stage);
  const c = getCustomerRow(id);
  if (!c) throw new Error('Customer not found');
  db.prepare(`UPDATE customers SET prev_stage = ?, stage = ?, step_index = 0, stage_entered_at = ?, status = ?, sold_date = ?, updated_at = ? WHERE id = ?`)
    .run(c.stage, stage, nowIso(), stage === 'dnc' ? 'completed' : 'active', stage === 'sold' ? (soldDate || nowIso().slice(0, 10)) : c.sold_date, nowIso(), id);
  // Drop drafted messages from the old stage.
  db.prepare("UPDATE tasks SET status = 'skipped', done_at = ? WHERE customer_id = ? AND status = 'pending' AND source = 'sequence'").run(nowIso(), id);
  if (stage === 'dnc') {
    db.prepare("UPDATE tasks SET status = 'skipped', done_at = ? WHERE customer_id = ? AND status = 'pending'").run(nowIso(), id);
    db.prepare('UPDATE customers SET consent = 0, email_opt_out = 1 WHERE id = ?').run(id);
  }
  reschedule(id);
}

/** active | paused. ('replied' is set by markReplied in queue.js.) */
function setStatus(id, status) {
  const c = getCustomerRow(id);
  if (!c || c.stage === 'dnc') return;
  if (status === 'active' && c.status !== 'active') {
    // Resuming: skip steps already in the past so nothing old piles up.
    const steps = getSteps(c.stage);
    const elapsedDays = (Date.now() - new Date(c.stage_entered_at).getTime()) / 86400000;
    let idx = c.step_index;
    while (idx < steps.length - 1 && steps[idx + 1].day <= elapsedDays) idx++;
    db.prepare("UPDATE customers SET status = 'active', step_index = ? WHERE id = ?").run(idx, id);
  } else {
    db.prepare('UPDATE customers SET status = ? WHERE id = ?').run(status, id);
  }
  reschedule(id);
}

function updateCustomer(id, data) {
  const c = getCustomerRow(id);
  if (!c) return null;
  for (const k of ['first_name', 'last_name', 'vehicle_interest', 'objection', 'notes', 'source']) {
    if (k in data) db.prepare(`UPDATE customers SET ${k} = ? WHERE id = ?`).run(String(data[k] ?? ''), id);
  }
  if ('phone' in data) db.prepare('UPDATE customers SET phone = ? WHERE id = ?').run(normalizePhone(data.phone) || null, id);
  if ('email' in data) db.prepare('UPDATE customers SET email = ? WHERE id = ?').run(normalizeEmail(data.email) || null, id);
  if ('on_dnc_registry' in data) db.prepare('UPDATE customers SET on_dnc_registry = ? WHERE id = ?').run(bool(data.on_dnc_registry), id);
  if ('customer_initiated' in data) db.prepare('UPDATE customers SET customer_initiated = ? WHERE id = ?').run(bool(data.customer_initiated), id);
  if ('consent' in data && c.stage !== 'dnc') setConsent(id, bool(data.consent), data.consent_source, data.consent_date);
  if ('stock_numbers' in data) {
    db.prepare('DELETE FROM interests WHERE customer_id = ?').run(id);
    addInterests(id, Array.isArray(data.stock_numbers) ? data.stock_numbers.flatMap(splitStocks) : splitStocks(data.stock_numbers));
  }
  if (data.stage && data.stage !== c.stage) setStage(id, data.stage, { soldDate: data.sold_date });
  if (data.status && ['active', 'paused'].includes(data.status) && data.status !== getCustomerRow(id).status) setStatus(id, data.status);
  db.prepare('UPDATE customers SET updated_at = ? WHERE id = ?').run(nowIso(), id);
  return getCustomer(id);
}
function deleteCustomer(id) { db.prepare('DELETE FROM customers WHERE id = ?').run(id); }

function listCustomers({ stage, group, status, q, stock, limit = 500 } = {}) {
  const where = [];
  const params = [];
  if (stage) { where.push('c.stage = ?'); params.push(stage); }
  if (group && GROUPS[group]) { where.push(`c.stage IN (${GROUPS[group].stages.map(() => '?').join(',')})`); params.push(...GROUPS[group].stages); }
  if (status) { where.push('c.status = ?'); params.push(status); }
  if (stock) { where.push('c.id IN (SELECT customer_id FROM interests WHERE stock_number LIKE ?)'); params.push('%' + normalizeStock(stock) + '%'); }
  if (q) {
    const like = '%' + String(q).trim().toLowerCase() + '%';
    const digits = String(q).replace(/\D/g, '');
    where.push(`(lower(c.first_name || ' ' || c.last_name) LIKE ? OR lower(coalesce(c.email,'')) LIKE ? OR coalesce(c.phone,'') LIKE ?
      OR lower(c.vehicle_interest) LIKE ? OR lower(c.notes) LIKE ? OR c.id IN (SELECT customer_id FROM interests WHERE lower(stock_number) LIKE ?))`);
    params.push(like, like, digits.length >= 3 ? '%' + digits + '%' : like, like, like, like);
  }
  return db.prepare(`SELECT c.*, (SELECT group_concat(stock_number, ', ') FROM interests WHERE customer_id = c.id) AS stocks,
      (SELECT COUNT(*) FROM tasks t WHERE t.customer_id = c.id AND t.status = 'pending') AS open_tasks
    FROM customers c ${where.length ? 'WHERE ' + where.join(' AND ') : ''}
    ORDER BY (c.status = 'replied') DESC, c.updated_at DESC LIMIT ?`).all(...params, Number(limit));
}

// ---------- messages ----------
function logMessage(m) {
  const now = nowIso();
  const r = db.prepare(`INSERT INTO messages (customer_id, direction, channel, subject, body, status, error, step_id, automated, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`).run(m.customer_id ?? null, m.direction, m.channel, m.subject || null, m.body, m.status, m.error || null, m.step_id ?? null, m.automated ? 1 : 0, now);
  if (m.customer_id && m.direction === 'out' && ['sent', 'simulated', 'logged'].includes(m.status)) {
    db.prepare('UPDATE customers SET last_contact_at = ?, first_contact_at = coalesce(first_contact_at, ?) WHERE id = ?').run(now, now, m.customer_id);
  }
  return Number(r.lastInsertRowid);
}
function getMessages(customerId) { return db.prepare('SELECT * FROM messages WHERE customer_id = ? ORDER BY created_at, id').all(customerId); }
function recentMessages(limit = 150) {
  return db.prepare(`SELECT m.*, c.first_name, c.last_name FROM messages m LEFT JOIN customers c ON c.id = m.customer_id
    ORDER BY m.created_at DESC, m.id DESC LIMIT ?`).all(limit);
}

// ---------- inventory ----------
function upsertInventory(v) {
  const stock = normalizeStock(v.stock_number);
  if (!stock) return null;
  const cur = db.prepare('SELECT * FROM inventory WHERE stock_number = ?').get(stock) || {};
  const f = (k) => (v[k] !== undefined && v[k] !== '' ? String(v[k]) : cur[k] || '');
  const st = String(v.status || '').toLowerCase();
  const status = ['available', 'pending', 'sold'].includes(st) ? st : cur.status || 'available';
  db.prepare(`INSERT INTO inventory (stock_number, year, make, model, trim, color, price, miles, vin, status, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(stock_number) DO UPDATE SET year=excluded.year, make=excluded.make, model=excluded.model,
    trim=excluded.trim, color=excluded.color, price=excluded.price, miles=excluded.miles, vin=excluded.vin, status=excluded.status, updated_at=excluded.updated_at`)
    .run(stock, f('year'), f('make'), f('model'), f('trim'), f('color'), f('price'), f('miles'), f('vin'), status, nowIso());
  return db.prepare('SELECT * FROM inventory WHERE stock_number = ?').get(stock);
}
function listStock(q) {
  const rows = db.prepare(`SELECT s.stock_number, v.year, v.make, v.model, v.trim, v.color, v.price, v.miles, v.vin, coalesce(v.status, 'not in inventory') AS status,
      (SELECT COUNT(*) FROM interests i WHERE i.stock_number = s.stock_number) AS interested
    FROM (SELECT stock_number FROM inventory UNION SELECT stock_number FROM interests) s LEFT JOIN inventory v ON v.stock_number = s.stock_number
    ORDER BY interested DESC, s.stock_number`).all();
  if (!q) return rows;
  const needle = String(q).toLowerCase();
  return rows.filter((r) => Object.values(r).some((x) => String(x ?? '').toLowerCase().includes(needle)));
}
function customersForStock(stock) {
  return db.prepare('SELECT c.* FROM customers c JOIN interests i ON i.customer_id = c.id WHERE i.stock_number = ? ORDER BY c.updated_at DESC').all(normalizeStock(stock));
}
function deleteStock(stock) { db.prepare('DELETE FROM inventory WHERE stock_number = ?').run(normalizeStock(stock)); }

// ---------- unsubscribe tokens ----------
function unsubToken(id) { return id + '.' + crypto.createHmac('sha256', getSettings().secret).update(String(id)).digest('hex').slice(0, 20); }
function verifyUnsubToken(token) {
  const t = String(token);
  const expected = unsubToken(Number(t.split('.')[0]));
  return expected.length === t.length && crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(t)) ? Number(t.split('.')[0]) : null;
}

module.exports = {
  db, nowIso, STAGES, GROUPS,
  getSettings, publicSettings, saveSettings,
  getSteps, getStep, updateStep, addStep, deleteStep, allTemplates, apptTemplate,
  normalizePhone, normalizeEmail, normalizeStock, splitStocks, localParts, blockReason, inTextWindow, bool,
  upsertCustomer, updateCustomer, getCustomer, getCustomerRow, listCustomers, deleteCustomer,
  setStage, setStatus, setConsent, reschedule, addInterests, removeInterest, vehicleLabel,
  logMessage, getMessages, recentMessages,
  upsertInventory, listStock, customersForStock, deleteStock,
  unsubToken, verifyUnsubToken,
};
