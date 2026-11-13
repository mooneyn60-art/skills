const path = require('node:path');
const crypto = require('node:crypto');
const express = require('express');
const config = require('./config');
const store = require('./db');
const queue = require('./queue');
const appts = require('./appointments');
const scheduler = require('./scheduler');
const tars = require('./tars');
const { scoreboard } = require('./scoreboard');
const { render } = require('./messaging');
const { customersFromCsv, inventoryFromCsv } = require('./csv');
const grow = require('./grow');
const email = require('./email');
const QRCode = require('qrcode');
const { StreamableHTTPServerTransport } = require('@modelcontextprotocol/sdk/server/streamableHttp.js');
const { createMcpServer } = require('./mcp');

const app = express();
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: false, limit: '1mb' }));

const safeEq = (a, b) => typeof a === 'string' && typeof b === 'string' && a.length === b.length && crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b));
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));

// ---------------- public routes ----------------

// Only used with text_mode = twilio. In Twilio: Phone Number > Messaging > "A message comes in" > {PUBLIC_URL}/webhooks/twilio/sms
app.post('/webhooks/twilio/sms', (req, res) => {
  if (!config.twilio.token) return res.status(404).end();
  const url = config.publicUrl + req.originalUrl;
  const data = Object.keys(req.body).sort().reduce((acc, k) => acc + k + req.body[k], url);
  const expected = crypto.createHmac('sha1', config.twilio.token).update(Buffer.from(data, 'utf-8')).digest('base64');
  if (!safeEq(req.get('X-Twilio-Signature') || '', expected)) return res.status(403).send('Invalid signature');
  if (req.body.From) queue.handleInboundSms(req.body.From, req.body.Body || '');
  res.type('text/xml').send('<Response></Response>');
});

app.get('/unsubscribe/:token', (req, res) => {
  const id = store.verifyUnsubToken(req.params.token);
  if (id && store.getCustomerRow(id)) {
    store.db.prepare('UPDATE customers SET email_opt_out = 1 WHERE id = ?').run(id);
    store.db.prepare("UPDATE tasks SET status = 'skipped', done_at = ? WHERE customer_id = ? AND kind = 'email' AND status = 'pending'").run(store.nowIso(), id);
    store.logMessage({ customer_id: id, direction: 'in', channel: 'email', body: 'Unsubscribed from emails', status: 'received' });
  }
  res.send(`<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><body style="font-family:Arial,sans-serif;text-align:center;padding:60px 16px">
    <h2>You're unsubscribed</h2><p>You won't receive any more emails from ${esc(store.getSettings().dealership || 'us')}.</p></body>`);
});

// Calendar feed: Google Calendar > Other calendars > From URL, or iPhone Settings > Calendar > Accounts > Add Subscribed Calendar
app.get('/calendar/:token.ics', (req, res) => {
  if (!safeEq(req.params.token, store.getSettings().calendar_token)) return res.status(404).send('Not found');
  res.type('text/calendar; charset=utf-8').send(appts.icsFeed());
});

// MCP for claude.ai (Settings > Connectors > Add custom connector). The token in the URL is the password: keep it private.
app.all('/mcp/:token', async (req, res) => {
  if (!safeEq(req.params.token, store.getSettings().mcp_token)) return res.status(404).json({ error: 'Not found' });
  if (req.method !== 'POST') return res.status(405).set('Allow', 'POST').json({ error: 'Method not allowed' });
  const server = createMcpServer();
  const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
  res.on('close', () => { transport.close(); server.close(); });
  try {
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
  } catch (e) {
    console.error('[mcp]', e);
    if (!res.headersSent) res.status(500).json({ error: 'MCP error' });
  }
});

// ---------------- your public lead page ----------------
function leadPage(msg = '', ok = false) {
  const st = store.getSettings();
  const name = esc(st.salesperson || 'your salesperson');
  const dealer = esc(st.dealership || 'the dealership');
  const field = (n, label, type = 'text', req = false) => `<label>${label}${req ? ' *' : ''}<input name="${n}" type="${type}" ${req ? 'required' : ''} maxlength="120"></label>`;
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${name} | ${dealer}</title><style>
:root{--bg:#f4f5f7;--card:#fff;--text:#1c2230;--muted:#6b7385;--brand:#1f4fd8;--line:#e3e6ec}
@media (prefers-color-scheme:dark){:root{--bg:#11141a;--card:#1a1e27;--text:#e8ebf2;--muted:#9aa3b5;--brand:#5b8cff;--line:#2b3140}}
*{box-sizing:border-box}body{margin:0;font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--text)}
main{max-width:480px;margin:0 auto;padding:24px 16px}.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;margin-bottom:14px}
h1{margin:0;font-size:24px}p{color:var(--muted)}label{display:block;font-size:14px;color:var(--muted);margin-top:12px}
input,textarea{display:block;width:100%;margin-top:4px;font:inherit;padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--text)}
.btn{display:block;width:100%;text-align:center;background:var(--brand);color:#fff;border:0;border-radius:10px;padding:13px;font:inherit;font-weight:600;margin-top:16px;text-decoration:none;cursor:pointer}
.btn.alt{background:transparent;color:var(--brand);border:1px solid var(--brand)}.row{display:flex;gap:10px}.row .btn{margin-top:8px}
.consent{display:flex;gap:10px;align-items:flex-start;font-size:13px;line-height:1.4}.consent input{width:auto;margin-top:3px}
.msg{padding:12px;border-radius:10px;background:${ok ? '#e5f6ee' : '#fdecea'};color:${ok ? '#12825a' : '#c0362c'}}.hp{position:absolute;left:-5000px}
</style></head><body><main>
<div class="card"><h1>${name}</h1><p style="margin:4px 0 0">${dealer}${st.dealer_address ? '<br>' + esc(st.dealer_address) : ''}</p>
<div class="row">${st.dealer_phone ? `<a class="btn" href="tel:${esc(st.dealer_phone)}">Call</a><a class="btn alt" href="sms:${esc(st.dealer_phone)}">Text</a>` : ''}</div>
<a class="btn alt" href="/me/contact.vcf">Save my contact</a></div>
${msg ? `<div class="card msg">${esc(msg)}</div>` : ''}
${ok ? '' : `<form class="card" method="post" action="/me"><h2 style="margin:0 0 4px;font-size:19px">Looking for a vehicle?</h2><p style="margin:0">Tell me what you need and I'll get right back to you.</p>
${field('first_name', 'First name', 'text', true)}${field('last_name', 'Last name')}${field('phone', 'Mobile number', 'tel')}${field('email', 'Email', 'email')}
${field('vehicle', 'What are you looking for?')}<label>Anything else? (trade-in, timing, questions)<textarea name="message" rows="3" maxlength="500"></textarea></label>
${field('referred_by', 'Who referred you? (optional)')}<input class="hp" name="website" tabindex="-1" autocomplete="off">
<label class="consent"><input type="checkbox" name="consent" value="yes"><span>I agree to receive calls and text messages, including automated ones, from ${name} at ${dealer} at the number I provided, and emails about vehicles and my inquiry. Consent is not a condition of purchase. Message and data rates may apply. Reply STOP to opt out at any time.</span></label>
<button class="btn" type="submit">Send</button></form>`}
</main></body></html>`;
}
app.get('/me', (req, res) => res.send(leadPage()));
app.post('/me', async (req, res) => {
  try {
    await grow.leadFromPage(req.body || {}, req.ip);
    res.send(leadPage(`Thanks! ${store.getSettings().salesperson || 'I'} will be in touch shortly.`, true));
  } catch (e) { res.status(400).send(leadPage(e.message)); }
});
app.get('/me/contact.vcf', (req, res) => res.type('text/vcard').set('Content-Disposition', 'attachment; filename="contact.vcf"').send(grow.vcard()));

// ---------------- login ----------------
const sessionToken = () => crypto.createHmac('sha256', store.getSettings().secret).update('session:' + config.appPassword).digest('hex');
const readCookie = (req, n) => {
  const m = (req.headers.cookie || '').split(/;\s*/).find((c) => c.startsWith(n + '='));
  return m ? decodeURIComponent(m.slice(n.length + 1)) : '';
};
app.post('/api/login', (req, res) => {
  if (!config.appPassword) return res.json({ ok: true });
  if (!safeEq(String(req.body?.password || ''), config.appPassword)) return res.status(401).json({ error: 'Wrong password' });
  const secure = config.publicUrl.startsWith('https') ? '; Secure' : '';
  res.setHeader('Set-Cookie', `da_session=${sessionToken()}; HttpOnly; SameSite=Lax; Path=/; Max-Age=${60 * 60 * 24 * 30}${secure}`);
  res.json({ ok: true });
});
app.use('/api', (req, res, next) => {
  if (!config.appPassword || safeEq(readCookie(req, 'da_session'), sessionToken())) return next();
  res.status(401).json({ error: 'login required' });
});

// ---------------- API ----------------
const wrap = (fn) => (req, res) => Promise.resolve(fn(req, res)).catch((e) => res.status(400).json({ error: e.message }));

app.get('/api/status', (req, res) => {
  const s = store.getSettings();
  const counts = {};
  for (const r of store.db.prepare('SELECT stage, COUNT(*) AS n FROM customers GROUP BY stage').all()) counts[r.stage] = r.n;
  res.json({
    stages: store.STAGES, groups: store.GROUPS, counts, appointment_types: appts.TYPES,
    email_live: email.isLive(), email_account: email.account()?.user || '', email_verified: store.getSettings().email_verified === '1' || email.account()?.source === 'env', email_providers: Object.fromEntries(Object.entries(email.PROVIDERS).map(([k, v]) => [k, v.label])),
    email_last_check: store.getSettings().email_last_check || '', email_last_error: store.getSettings().email_last_error || '', twilio_live: config.smsLive, tars_ready: !!config.anthropicKey,
    in_text_window: store.inTextWindow(s),
    setup_missing: ['salesperson', 'dealership', 'dealer_address'].filter((k) => !s[k]),
    mcp_url: `${config.publicUrl}/mcp/${s.mcp_token}`,
    calendar_url: `${config.publicUrl}/calendar/${s.calendar_token}.ics`,
    public_url: config.publicUrl,
  });
});
app.get('/api/settings', (req, res) => res.json(store.publicSettings()));
app.put('/api/settings', (req, res) => res.json(store.saveSettings(req.body)));

// daily list
app.get('/api/today', (req, res) => res.json(queue.dailyList()));
app.post('/api/tasks/:id', wrap(async (req, res) => res.json(await queue.completeTask(Number(req.params.id), req.body || {}))));
app.post('/api/run-now', wrap(async (req, res) => res.json(await scheduler.tick())));

// customers
app.get('/api/customers', (req, res) => res.json(store.listCustomers(req.query)));
app.post('/api/customers', wrap((req, res) => {
  const b = req.body || {};
  if (!b.phone && !b.email) throw new Error('A phone number or email is required');
  if (b.consent) b.consent_source ||= 'Recorded on entry';
  res.json(store.upsertCustomer(b));
}));
app.get('/api/customers/:id', (req, res) => {
  const c = store.getCustomer(Number(req.params.id));
  if (!c) return res.status(404).json({ error: 'not found' });
  const steps = store.getSteps(c.stage);
  const step = steps[c.step_index];
  c.next_step = step && c.status === 'active' ? { ...step, preview: render(step.body, c) } : null;
  c.total_steps = steps.length;
  c.messages = store.getMessages(c.id);
  c.tasks = store.db.prepare("SELECT * FROM tasks WHERE customer_id = ? AND status = 'pending' ORDER BY due_at").all(c.id);
  c.appointments = appts.list({ customer_id: c.id, includeCancelled: true });
  c.blocks = { sms: store.blockReason(c, 'sms'), email: store.blockReason(c, 'email'), call: store.blockReason(c, 'call') };
  res.json(c);
});
app.put('/api/customers/:id', wrap((req, res) => res.json(store.updateCustomer(Number(req.params.id), req.body || {}))));
app.delete('/api/customers/:id', (req, res) => { store.deleteCustomer(Number(req.params.id)); res.json({ ok: true }); });
app.post('/api/customers/:id/replied', wrap((req, res) => res.json(queue.markReplied(Number(req.params.id), req.body?.text || ''))));
app.post('/api/customers/:id/draft', wrap((req, res) => {
  const out = tars.runTool('draft_message', { customer_id: Number(req.params.id), ...req.body });
  Promise.resolve(out).then((r) => (r.error ? res.status(400).json(r) : res.json(r)));
}));
app.post('/api/customers/bulk', wrap((req, res) => {
  const { ids = [], action, stage } = req.body || {};
  for (const id of ids.map(Number)) {
    if (action === 'stage' && stage) store.setStage(id, stage);
    else if (['active', 'paused'].includes(action)) store.setStatus(id, action);
    else if (action === 'delete') store.deleteCustomer(id);
  }
  res.json({ ok: true, count: ids.length });
}));

// import
app.post('/api/import/customers', wrap((req, res) => {
  const { csv, stage = 'new_lead', preview } = req.body || {};
  if (!store.STAGES[stage]) throw new Error('Pick a stage');
  const parsed = customersFromCsv(csv, stage);
  if (preview) return res.json({ ...parsed, customers: parsed.customers.slice(0, 8), total: parsed.customers.length });
  let created = 0, updated = 0;
  for (const c of parsed.customers) (store.upsertCustomer(c).created ? created++ : updated++);
  res.json({ created, updated, skipped: parsed.skipped, mapped: parsed.mapped });
}));
app.post('/api/import/inventory', wrap((req, res) => {
  const rows = inventoryFromCsv(req.body?.csv);
  // The first inventory import just loads the lot. After that, new arrivals are matched to your leads (capped so your list doesn't flood).
  const firstLoad = store.db.prepare('SELECT COUNT(*) AS n FROM inventory').get().n === 0;
  let drafted = 0;
  for (const v of rows) {
    if (firstLoad || drafted >= 40) store.upsertInventory(v);
    else drafted += grow.saveVehicle(v).drafted;
  }
  res.json({ imported: rows.length, match_texts_drafted: drafted, first_load: firstLoad });
}));

// stock
app.get('/api/stock', (req, res) => res.json(store.listStock(req.query.q)));
app.get('/api/stock/:stock', (req, res) => {
  const stock = store.normalizeStock(req.params.stock);
  res.json({ vehicle: store.listStock().find((s) => s.stock_number === stock) || { stock_number: stock }, customers: store.customersForStock(stock) });
});
app.put('/api/stock/:stock', wrap((req, res) => res.json(grow.saveVehicle({ ...req.body, stock_number: req.params.stock }))));
app.delete('/api/stock/:stock', (req, res) => { store.deleteStock(req.params.stock); res.json({ ok: true }); });

// templates
app.get('/api/templates', (req, res) => res.json(store.allTemplates()));
app.put('/api/templates/:id', wrap((req, res) => res.json(store.updateStep(Number(req.params.id), req.body || {}))));
app.post('/api/templates', wrap((req, res) => res.json(store.addStep(req.body?.stage, req.body || {}))));
app.delete('/api/templates/:id', (req, res) => { store.deleteStep(Number(req.params.id)); res.json({ ok: true }); });

// appointments
app.get('/api/appointments', (req, res) => res.json(appts.list({ from: req.query.from, to: req.query.to })));
app.post('/api/appointments', wrap((req, res) => res.json(appts.create(req.body || {}))));
app.put('/api/appointments/:id', wrap((req, res) => res.json(appts.update(Number(req.params.id), req.body || {}))));
app.delete('/api/appointments/:id', (req, res) => { appts.remove(Number(req.params.id)); res.json({ ok: true }); });

// grow
app.get('/api/grow', wrap(async (req, res) => {
  const st = store.getSettings();
  const url = `${config.publicUrl}/me`;
  res.json({
    lead_page_url: url,
    qr: await QRCode.toDataURL(url, { margin: 1, width: 320 }),
    campaigns: Object.keys(grow.CAMPAIGNS).map((k) => grow.campaignPreview(k)),
    leads_from_page_30d: store.db.prepare("SELECT COUNT(*) AS n FROM customers WHERE source = 'My lead page' AND created_at >= ?").get(new Date(Date.now() - 30 * 86400000).toISOString()).n,
    referral_sales: store.db.prepare("SELECT COUNT(*) AS n FROM customers WHERE stage = 'sold' AND (referred_by_id IS NOT NULL OR coalesce(referred_by_name,'') != '')").get().n,
    birthdays_on_file: store.db.prepare('SELECT COUNT(*) AS n FROM customers WHERE birthday IS NOT NULL').get().n,
    salesperson: st.salesperson,
  });
}));
app.post('/api/grow/campaign/:key', wrap((req, res) => res.json(grow.runCampaign(req.params.key, req.body?.per_day))));

// email
app.post('/api/email/test', wrap(async (req, res) => res.json(await email.test())));
app.post('/api/email/check', wrap(async (req, res) => res.json(await email.checkReplies())));
app.post('/api/email/disconnect', wrap((req, res) => { store.setInternal({ email_app_password: '', email_address: '', email_last_uid: '', email_uid_validity: '', email_last_error: '', email_verified: '' }); res.json({ ok: true }); }));

app.get('/api/scoreboard', (req, res) => res.json(scoreboard()));
app.get('/api/messages', (req, res) => res.json(store.recentMessages(Number(req.query.limit) || 150)));

app.post('/api/tars', wrap(async (req, res) => {
  const { message, history = [] } = req.body || {};
  if (!message) throw new Error('Ask TARS something');
  res.json(await tars.chat(history, message));
}));

app.use(express.static(path.join(config.ROOT, 'public')));

if (require.main === module) {
  app.listen(config.port, () => {
    const s = store.getSettings();
    console.log(`\n  Dealer Autopilot: http://localhost:${config.port}`);
    console.log(`  Texts:  ${s.text_mode === 'twilio' ? (config.smsLive ? 'Twilio (live)' : 'Twilio (SIMULATED: add keys to .env)') : 'from your own phone (one tap per text)'}`);
    console.log(`  Email:  ${email.isLive() ? 'connected: ' + email.account().user : 'not connected yet (Setup screen)'}`);
    console.log(`  TARS:   ${config.anthropicKey ? 'ready' : 'off: add ANTHROPIC_API_KEY to .env'}`);
    console.log(`  MCP:    ${config.publicUrl}/mcp/${s.mcp_token}\n`);
    scheduler.start();
    // Check your inbox for customer replies every 3 minutes.
    const watch = () => email.checkReplies().then((r) => r.replies && console.log(`[email] ${r.replies} customer repl${r.replies === 1 ? 'y' : 'ies'}`)).catch(() => {});
    setTimeout(watch, 5000); setInterval(watch, 3 * 60 * 1000);
  });
}

module.exports = app;
