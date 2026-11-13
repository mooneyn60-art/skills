// TARS: the assistant in the dashboard. The same tools are exposed over MCP (src/mcp.js),
// so Claude Desktop / Claude Code / claude.ai can run the platform too.
const Anthropic = require('@anthropic-ai/sdk');
const config = require('./config');
const store = require('./db');
const queue = require('./queue');
const appts = require('./appointments');
const { scoreboard } = require('./scoreboard');
const { render } = require('./messaging');
const { customersFromCsv } = require('./csv');
const grow = require('./grow');

const MODEL = 'claude-opus-5-5';
const STAGE_ENUM = Object.keys(store.STAGES);

const SYSTEM = `You are TARS, the assistant inside a car salesperson's follow-up system. The salesperson's dealership CRM (usually DealerSocket) stays the system of record; this tool runs their daily follow-up list.

How the system works:
- Every customer is in exactly one stage: new_lead (internet lead), phone_up, be_back (unsold showroom), appointment, sold, lost, dnc (do not contact).
  The salesperson thinks of these as three buckets: Follow Up (new_lead, phone_up, be_back, appointment), Sold, Outreach (lost).
- Each stage has a day-by-day cadence. When a step is due it becomes a task on the daily list: calls to make, and drafted texts/emails to approve. Nothing sends on its own except templates the salesperson approved for automation (Sold stage and appointment reminders), and only to customers with recorded consent.
- Texts are sent from the salesperson's own phone: "sending" a text returns a link that opens their Messages app with the text filled in.
- Any customer reply stops their automation and puts them on the call list (mark_replied).
- Statuses: active, paused, replied, completed.

Compliance rules you must follow, no exceptions:
- Never text or email anyone without recorded consent. Never contact a dnc customer. Texts only 8 am to 9 pm local time. Respect the Do Not Call registry flag.
- Never put credit, SSN, licence or income information into the system or into messages.
- Never promise a price, payment or approval in a message.

How to work:
- Look things up with the tools before answering. Never invent customers, numbers, stock numbers or prices.
- Be brief, like a sharp sales manager. Short lists. Mention customer ids like (#12).
- When asked to write a message, use draft_message so it lands on the approval list. Only use complete_task with action "send" when the salesperson explicitly says to send it.
- Write messages friendly-professional, from the salesperson, under 300 characters for texts, one ask per message (a question OR a time, not both), no fake urgency, no emojis.
- Help the salesperson sell more: point out replies waiting, hot leads, past buyers due for an upgrade, and new arrivals that match someone. Suggest a campaign when it fits, but ask before running one.
- If a date, time or customer is ambiguous, ask before booking or changing anything.`;

const tools = [
  { name: 'daily_list', description: "Today's list: calls to make (replies first), drafted texts/emails waiting for approval, and automatic messages queued.", input_schema: { type: 'object', properties: {}, additionalProperties: false } },
  { name: 'scoreboard', description: 'Weekly scoreboard for the last 6 weeks: leads, response time to new leads (target under 5 min), appointment-set rate, show rate, close rate; plus which messages get the most replies.', input_schema: { type: 'object', properties: {}, additionalProperties: false } },
  {
    name: 'search_customers',
    description: 'Search customers. All filters optional. query matches name, phone, email, notes, vehicle or stock number. group is the bucket: follow_up, sold, outreach.',
    input_schema: {
      type: 'object',
      properties: {
        query: { type: 'string' }, stage: { type: 'string', enum: STAGE_ENUM }, group: { type: 'string', enum: ['follow_up', 'sold', 'outreach', 'dnc'] },
        status: { type: 'string', enum: ['active', 'paused', 'replied', 'completed'] }, stock_number: { type: 'string' }, limit: { type: 'integer' },
      },
      additionalProperties: false,
    },
  },
  { name: 'get_customer', description: 'Everything about one customer: contact, stage, consent, stock numbers, open tasks, appointments, and message history.', input_schema: { type: 'object', properties: { id: { type: 'integer' } }, required: ['id'], additionalProperties: false } },
  {
    name: 'add_customer',
    description: 'Add a customer (merges with an existing one with the same phone/email) and start the cadence for their stage. Only set consent true if the salesperson says the customer agreed to texts/emails, and say how (consent_source).',
    input_schema: {
      type: 'object',
      properties: {
        first_name: { type: 'string' }, last_name: { type: 'string' }, phone: { type: 'string' }, email: { type: 'string' },
        stage: { type: 'string', enum: STAGE_ENUM }, stock_numbers: { type: 'array', items: { type: 'string' } },
        vehicle_interest: { type: 'string' }, objection: { type: 'string', description: 'The one thing holding them back' },
        consent: { type: 'boolean' }, consent_source: { type: 'string' }, source: { type: 'string' }, notes: { type: 'string' },
        referred_by: { type: 'string', description: 'Name or phone of the existing customer who referred them' },
        birthday: { type: 'string', description: 'MM-DD' }, sold_date: { type: 'string', description: 'YYYY-MM-DD, for past buyers' },
      },
      required: ['stage'],
      additionalProperties: false,
    },
  },
  {
    name: 'import_customers',
    description: 'Import a list as CSV/tab-separated text with a header row (e.g. a DealerSocket export). Rows without a recognisable stage column go into the given stage. Consent is taken only from a consent/opt-in column.',
    input_schema: { type: 'object', properties: { csv: { type: 'string' }, stage: { type: 'string', enum: STAGE_ENUM } }, required: ['csv', 'stage'], additionalProperties: false },
  },
  {
    name: 'update_customer',
    description: "Change a customer. Changing stage restarts that stage's cadence (e.g. sold when they buy, lost if they bought elsewhere, dnc if they asked not to be contacted). status active resumes, paused stops.",
    input_schema: {
      type: 'object',
      properties: {
        id: { type: 'integer' }, stage: { type: 'string', enum: STAGE_ENUM }, status: { type: 'string', enum: ['active', 'paused'] },
        objection: { type: 'string' }, add_note: { type: 'string' },
        consent: { type: 'boolean' }, consent_source: { type: 'string', description: 'How they agreed, e.g. "said yes on the phone 11/13"' },
        on_dnc_registry: { type: 'boolean' }, referred_by: { type: 'string' }, birthday: { type: 'string', description: 'MM-DD' },
        add_stock_numbers: { type: 'array', items: { type: 'string' } }, remove_stock_numbers: { type: 'array', items: { type: 'string' } },
      },
      required: ['id'],
      additionalProperties: false,
    },
  },
  { name: 'mark_replied', description: 'Record that a customer replied (and what they said). Stops their automation and puts them at the top of the call list.', input_schema: { type: 'object', properties: { customer_id: { type: 'integer' }, text: { type: 'string' } }, required: ['customer_id'], additionalProperties: false } },
  {
    name: 'draft_message',
    description: 'Put a text or email on the approval list for a customer. Placeholders like {first_name} {vehicle} {salesperson} work.',
    input_schema: {
      type: 'object',
      properties: { customer_id: { type: 'integer' }, channel: { type: 'string', enum: ['sms', 'email'] }, subject: { type: 'string' }, body: { type: 'string' } },
      required: ['customer_id', 'channel', 'body'],
      additionalProperties: false,
    },
  },
  {
    name: 'complete_task',
    description: 'Finish a task from the daily list. action "send" sends a text/email (ONLY when the salesperson explicitly says send; texts return a link to send from their phone). "done" logs a call or marks handled (add a note). "skip" drops it.',
    input_schema: {
      type: 'object',
      properties: { id: { type: 'integer' }, action: { type: 'string', enum: ['send', 'done', 'skip'] }, body: { type: 'string' }, subject: { type: 'string' }, note: { type: 'string' } },
      required: ['id', 'action'],
      additionalProperties: false,
    },
  },
  {
    name: 'stock_lookup',
    description: 'With stock_number: the vehicle and every customer interested in it. With query: search stock by make/model/year. With neither: all stock numbers with interest counts.',
    input_schema: { type: 'object', properties: { stock_number: { type: 'string' }, query: { type: 'string' } }, additionalProperties: false },
  },
  {
    name: 'update_stock',
    description: 'Add or update a vehicle (e.g. mark a stock number sold). A new vehicle drafts "just came in" texts to matching customers; marking one sold drafts "that one sold" texts to everyone interested.',
    input_schema: {
      type: 'object',
      properties: {
        stock_number: { type: 'string' }, year: { type: 'string' }, make: { type: 'string' }, model: { type: 'string' }, trim: { type: 'string' },
        color: { type: 'string' }, miles: { type: 'string' }, status: { type: 'string', enum: ['available', 'pending', 'sold'] },
      },
      required: ['stock_number'],
      additionalProperties: false,
    },
  },
  {
    name: 'campaign',
    description: 'Campaigns that create sales: "equity" = past buyers 2-4 years out who may owe less than their car is worth; "reactivation" = leads with no contact in 60+ days. Without run it previews the counts. With run true it puts them on the daily list, per_day at a time (texts for consented customers, calls for the rest). Ask the salesperson before running.',
    input_schema: { type: 'object', properties: { key: { type: 'string', enum: ['equity', 'reactivation'] }, run: { type: 'boolean' }, per_day: { type: 'integer' } }, required: ['key'], additionalProperties: false },
  },
  {
    name: 'find_matches',
    description: 'Customers who might want a given vehicle in inventory (same model as what they asked about).',
    input_schema: { type: 'object', properties: { stock_number: { type: 'string' } }, required: ['stock_number'], additionalProperties: false },
  },
  {
    name: 'list_appointments',
    description: 'Appointments between two dates (dealership local, YYYY-MM-DD, inclusive). Defaults to today through 7 days out.',
    input_schema: { type: 'object', properties: { from_date: { type: 'string' }, to_date: { type: 'string' }, customer_id: { type: 'integer' } }, additionalProperties: false },
  },
  {
    name: 'book_appointment',
    description: 'Book an appointment (dealership local date and 24h time). Moves the customer to the appointment stage, drafts a confirmation text, and queues reminders the day before and 2 hours before.',
    input_schema: {
      type: 'object',
      properties: {
        customer_id: { type: 'integer' }, date: { type: 'string' }, time: { type: 'string' },
        type: { type: 'string', enum: Object.keys(appts.TYPES) }, stock_number: { type: 'string' }, duration_min: { type: 'integer' }, notes: { type: 'string' },
      },
      required: ['customer_id', 'date', 'time', 'type'],
      additionalProperties: false,
    },
  },
  {
    name: 'update_appointment',
    description: 'Reschedule, cancel or record what happened. status showed + result sold/unsold moves them to sold or be_back (give the objection for unsold). no_show drafts a "sorry we missed you" text.',
    input_schema: {
      type: 'object',
      properties: {
        id: { type: 'integer' }, date: { type: 'string' }, time: { type: 'string' },
        status: { type: 'string', enum: ['scheduled', 'confirmed', 'showed', 'no_show', 'cancelled'] },
        result: { type: 'string', enum: ['sold', 'unsold'] }, objection: { type: 'string' }, notes: { type: 'string' },
      },
      required: ['id'],
      additionalProperties: false,
    },
  },
];

const nm = (c) => `${c.first_name || ''} ${c.last_name || ''}`.trim();
function slim(c) {
  return {
    id: c.id, name: nm(c), phone: c.phone, email: c.email, stage: c.stage, status: c.status, consent: !!c.consent,
    stocks: c.stocks, vehicle: c.vehicle_interest || undefined, objection: c.objection || undefined,
    last_contact_at: c.last_contact_at, next_touch_at: c.next_touch_at,
  };
}
const slimTask = (t) => ({ id: t.id, kind: t.kind, customer_id: t.customer_id, customer: nm(t), phone: t.phone, title: t.title, subject: t.subject || undefined, body: t.body || undefined, source: t.source, auto: !!t.auto });

async function runTool(name, input, actions = []) {
  const tz = store.getSettings().timezone;
  switch (name) {
    case 'daily_list': {
      // Bring the list up to date first, so this works from Claude Desktop even when the dashboard isn't running.
      queue.generateDue();
      appts.tick();
      const l = queue.dailyList();
      return { calls: l.calls.map(slimTask), approve: l.approve.map(slimTask), automatic: l.automatic.map(slimTask), in_text_window: l.in_text_window, call_target: l.call_target };
    }
    case 'scoreboard': return scoreboard();
    case 'search_customers': {
      const rows = store.listCustomers({ q: input.query, stage: input.stage, group: input.group, status: input.status, stock: input.stock_number, limit: Math.min(Number(input.limit) || 25, 200) });
      return { count: rows.length, customers: rows.map(slim) };
    }
    case 'get_customer': {
      const c = store.getCustomer(input.id);
      if (!c) return { error: 'No customer with that id' };
      return {
        ...c,
        open_tasks: store.db.prepare("SELECT * FROM tasks WHERE customer_id = ? AND status = 'pending'").all(c.id),
        appointments: appts.list({ customer_id: c.id, includeCancelled: true }).map((a) => ({ id: a.id, when: appts.formatLocal(a.starts_at, tz), type: a.type, status: a.status })),
        history: store.getMessages(c.id).slice(-30).map((m) => ({ at: m.created_at, dir: m.direction, channel: m.channel, status: m.status, body: m.body })),
      };
    }
    case 'add_customer': {
      if (!input.phone && !input.email) return { error: 'Need a phone number or email' };
      const r = store.upsertCustomer({ ...input, consent_source: input.consent ? input.consent_source || 'Told TARS' : undefined });
      actions.push(`${r.created ? 'Added' : 'Updated'} ${nm(r.customer)} (#${r.customer.id})`);
      return { created: r.created, ...slim(r.customer) };
    }
    case 'import_customers': {
      const parsed = customersFromCsv(input.csv, input.stage);
      let created = 0, updated = 0;
      for (const c of parsed.customers) (store.upsertCustomer(c).created ? created++ : updated++);
      actions.push(`Imported ${created} new, ${updated} updated`);
      return { created, updated, skipped_no_contact_info: parsed.skipped, columns_used: parsed.mapped };
    }
    case 'update_customer': {
      const c = store.getCustomerRow(input.id);
      if (!c) return { error: 'No customer with that id' };
      const patch = {};
      for (const k of ['stage', 'status', 'objection', 'on_dnc_registry', 'referred_by', 'birthday']) if (input[k] !== undefined) patch[k] = input[k];
      if (input.consent !== undefined) { patch.consent = input.consent; patch.consent_source = input.consent_source || 'Told TARS'; }
      if (input.add_note) patch.notes = [c.notes, `[${new Date().toLocaleDateString('en-US', { timeZone: tz })}] ${input.add_note}`].filter(Boolean).join('\n');
      store.updateCustomer(c.id, patch);
      if (input.add_stock_numbers?.length) store.addInterests(c.id, input.add_stock_numbers);
      for (const s of input.remove_stock_numbers || []) store.removeInterest(c.id, s);
      actions.push(`Updated ${nm(c)} (#${c.id})`);
      return slim(store.getCustomerRow(c.id));
    }
    case 'mark_replied': {
      const r = queue.markReplied(input.customer_id, input.text || '');
      actions.push(`Customer #${input.customer_id} moved to your call list`);
      return r;
    }
    case 'draft_message': {
      const c = store.getCustomer(input.customer_id);
      if (!c) return { error: 'No customer with that id' };
      const blocked = store.blockReason(c, input.channel);
      if (blocked) return { error: `Can't message this customer: ${blocked}` };
      const t = queue.addTask({
        customer_id: c.id, kind: input.channel, source: 'manual', title: `${input.channel === 'sms' ? 'Text' : 'Email'} ${nm(c)}`,
        subject: input.subject ? render(input.subject, c) : '', body: render(input.body, c),
      });
      actions.push(`Drafted ${input.channel === 'sms' ? 'text' : 'email'} for ${nm(c)}, on your approval list`);
      return slimTask(t);
    }
    case 'complete_task': {
      const r = await queue.completeTask(input.id, { action: input.action, body: input.body, subject: input.subject, note: input.note });
      actions.push(`Task #${input.id}: ${r.status}`);
      return r;
    }
    case 'stock_lookup': {
      if (input.stock_number) {
        const stock = store.normalizeStock(input.stock_number);
        return { vehicle: store.listStock().find((s) => s.stock_number === stock) || null, interested: store.customersForStock(stock).map(slim) };
      }
      return store.listStock(input.query).slice(0, 100);
    }
    case 'update_stock': {
      const { vehicle, drafted } = grow.saveVehicle(input);
      actions.push(`Updated stock #${vehicle.stock_number}${drafted ? `, drafted ${drafted} texts to matching customers` : ''}`);
      return { ...vehicle, match_texts_drafted: drafted };
    }
    case 'campaign': {
      if (input.run) {
        const r = grow.runCampaign(input.key, input.per_day);
        actions.push(`Campaign ${input.key}: ${r.queued} customers queued over ${r.days} day(s)`);
        return r;
      }
      return grow.campaignPreview(input.key);
    }
    case 'find_matches': {
      const v = store.listStock().find((x) => x.stock_number === store.normalizeStock(input.stock_number));
      if (!v) return { error: 'Stock number not found in inventory' };
      return grow.findMatches(v).map(slim);
    }
    case 'list_appointments': {
      const today = store.localParts(new Date(), tz).date;
      const fromD = input.from_date || today;
      const toD = input.to_date || store.localParts(new Date(Date.now() + 7 * 86400000), tz).date;
      const to = new Date(new Date(appts.localToIso(toD, '00:00', tz)).getTime() + 86400000).toISOString();
      return appts.list({ from: appts.localToIso(fromD, '00:00', tz), to, customer_id: input.customer_id }).map((a) => ({
        id: a.id, when: appts.formatLocal(a.starts_at, tz), type: a.type, status: a.status, customer_id: a.customer_id, customer: nm(a), phone: a.phone, stock_number: a.stock_number, notes: a.notes,
      }));
    }
    case 'book_appointment': {
      const r = appts.create(input);
      const a = r.appointment;
      actions.push(`Booked ${appts.TYPES[a.type]} for ${nm(a)}, ${appts.formatLocal(a.starts_at, tz)}`);
      return { id: a.id, when: appts.formatLocal(a.starts_at, tz), confirmation_text: r.confirmation_task ? slimTask(r.confirmation_task) : 'Not drafted (no consent to text, or time is in the past)' };
    }
    case 'update_appointment': {
      const a = appts.update(input.id, input);
      actions.push(`Appointment #${a.id}: ${a.status}`);
      return { id: a.id, when: appts.formatLocal(a.starts_at, tz), status: a.status };
    }
    default:
      return { error: 'Unknown tool' };
  }
}

/** history: [{ role, content: string }] from earlier turns. Returns { reply, actions }. */
async function chat(history, message) {
  if (!config.anthropicKey) {
    return { reply: "I'm not switched on yet. Add ANTHROPIC_API_KEY to the .env file and restart. (You can also run everything from Claude itself over MCP; see the README.)", actions: [] };
  }
  const client = new Anthropic({ apiKey: config.anthropicKey });
  const s = store.getSettings();
  const messages = [
    ...history.filter((m) => m && ['user', 'assistant'].includes(m.role) && m.content).slice(-20).map((m) => ({ role: m.role, content: String(m.content) })),
    { role: 'user', content: `${message}\n\n(Now: ${new Date().toLocaleString('en-US', { timeZone: s.timezone, weekday: 'long', dateStyle: undefined })} ${new Date().toLocaleString('en-US', { timeZone: s.timezone })}. Salesperson: ${s.salesperson || 'not set'}, ${s.dealership || 'dealership not set'}.)` },
  ];
  const actions = [];
  for (let i = 0; i < 12; i++) {
    const response = await client.beta.messages.create({
      model: MODEL,
      max_tokens: 16000,
      betas: ['server-side-fallback-2026-07-01'],
      fallbacks: 'default',
      thinking: { type: 'adaptive' },
      output_config: { effort: 'medium' },
      system: SYSTEM,
      tools,
      messages,
    });
    if (response.stop_reason === 'refusal') return { reply: "Sorry, I can't help with that one.", actions };
    const text = response.content.filter((b) => b.type === 'text').map((b) => b.text).join('\n').trim();
    const uses = response.content.filter((b) => b.type === 'tool_use');
    if (response.stop_reason !== 'tool_use' || !uses.length) return { reply: text || '(no answer)', actions };
    messages.push({ role: 'assistant', content: response.content });
    const results = [];
    for (const tu of uses) {
      try {
        results.push({ type: 'tool_result', tool_use_id: tu.id, content: JSON.stringify(await runTool(tu.name, tu.input || {}, actions)) });
      } catch (err) {
        results.push({ type: 'tool_result', tool_use_id: tu.id, content: `Error: ${err.message}`, is_error: true });
      }
    }
    messages.push({ role: 'user', content: results });
  }
  return { reply: 'That took too many steps. Try a narrower question.', actions };
}

module.exports = { chat, tools, runTool, SYSTEM };
