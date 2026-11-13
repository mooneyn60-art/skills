// Features that bring in customers and sales:
//  - your own lead page (with proper consent wording) and a QR code for cards / social
//  - new-arrival matching: "a car like the one you wanted just came in" / "the one you liked sold"
//  - campaigns: upgrade (equity) list for past buyers, reactivation for old unsold leads
//  - birthdays and referral thank-yous
// Everything lands on your daily list for approval. Nothing here sends on its own.
const store = require('./db');
const queue = require('./queue');
const { notifyOwner } = require('./messaging');

const { db } = store;
const nm = (c) => `${c.first_name || ''} ${c.last_name || ''}`.trim() || 'Customer';
const vehicleName = (v) => [v.year, v.make, v.model, v.trim].filter(Boolean).join(' ');

// ---------------- new-arrival matching ----------------
const OPEN_STAGES = ['new_lead', 'phone_up', 'be_back', 'lost'];

/** Customers who might want this vehicle: same make+model as a stock # they liked, or the model named in what they asked for. */
function findMatches(v) {
  const model = String(v.model || '').trim().toLowerCase();
  const make = String(v.make || '').trim().toLowerCase();
  if (!model) return [];
  const rows = db.prepare(`SELECT DISTINCT c.* FROM customers c
    LEFT JOIN interests i ON i.customer_id = c.id LEFT JOIN inventory iv ON iv.stock_number = i.stock_number
    WHERE c.stage IN (${OPEN_STAGES.map(() => '?').join(',')})
      AND (lower(c.vehicle_interest) LIKE ? OR (lower(iv.model) = ? AND (? = '' OR lower(iv.make) = ?)))
      AND c.id NOT IN (SELECT customer_id FROM interests WHERE stock_number = ?)`)
    .all(...OPEN_STAGES, `%${model}%`, model, make, make, v.stock_number);
  return rows;
}

/** Call when a vehicle is added. Drafts a "just came in" text for each matching customer (max 15). */
function onNewVehicle(v) {
  if (!v || v.status === 'sold') return 0;
  const tpl = store.extraTemplate('new_arrival');
  let n = 0;
  for (const c of findMatches(v).slice(0, 15)) {
    if (store.blockReason(c, 'sms')) continue; // only customers you're allowed to text
    if (db.prepare("SELECT 1 FROM tasks WHERE customer_id = ? AND source = 'match' AND status = 'pending'").get(c.id)) continue;
    if (queue.queueTemplate(c, tpl, { source: 'match', extra: { match_vehicle: vehicleName(v), match_stock: v.stock_number } })) n++;
  }
  return n;
}

/** Call when a vehicle is marked sold. Tells everyone who was interested in it (and offers to find another). */
function onVehicleSold(v) {
  const tpl = store.extraTemplate('stock_sold');
  let n = 0;
  for (const c of store.customersForStock(v.stock_number)) {
    if (!OPEN_STAGES.includes(c.stage) || store.blockReason(c, 'sms')) continue;
    if (queue.queueTemplate(c, tpl, { source: 'match', extra: { match_vehicle: vehicleName(v) || `vehicle #${v.stock_number}`, match_stock: v.stock_number } })) n++;
  }
  return n;
}

/** Wrapper used by every "save vehicle" path. */
function saveVehicle(data) {
  const before = db.prepare('SELECT * FROM inventory WHERE stock_number = ?').get(store.normalizeStock(data.stock_number));
  const v = store.upsertInventory(data);
  if (!v) return { vehicle: null, drafted: 0 };
  let drafted = 0;
  if (!before) drafted = onNewVehicle(v);
  else if (before.status !== 'sold' && v.status === 'sold') drafted = onVehicleSold(v);
  return { vehicle: v, drafted };
}

// ---------------- campaigns ----------------
const CAMPAIGNS = {
  equity: {
    label: 'Upgrade list (bought 2 to 4 years ago)',
    why: 'Past buyers around the 24 to 48 month mark often owe less than the car is worth. This is where repeat sales come from.',
    template: 'equity',
    call: (c) => `Call ${nm(c)}: bought ${c.sold_date}. Their car may be worth more than they owe. Offer to run the numbers.`,
    audience: () => {
      const d = (months) => { const x = new Date(); x.setMonth(x.getMonth() - months); return x.toISOString().slice(0, 10); };
      return db.prepare("SELECT * FROM customers WHERE stage = 'sold' AND sold_date IS NOT NULL AND sold_date <= ? AND sold_date >= ?").all(d(24), d(48));
    },
  },
  reactivation: {
    label: 'Reactivate old leads (no contact in 60+ days)',
    why: 'Leads that went quiet are often still shopping. One friendly check-in brings some back.',
    template: 'reactivation',
    call: (c) => `Call ${nm(c)}: old lead${c.vehicle_interest || c.stocks ? ` (${c.stocks || c.vehicle_interest})` : ''}. Still in the market?`,
    audience: () => {
      const cutoff = new Date(Date.now() - 60 * 86400000).toISOString();
      return db.prepare(`SELECT c.*, (SELECT group_concat(stock_number, ', ') FROM interests WHERE customer_id = c.id) AS stocks FROM customers c
        WHERE c.stage IN ('new_lead','phone_up','be_back','lost') AND c.status IN ('completed','active','paused')
        AND coalesce(c.last_contact_at, c.created_at) <= ? AND c.created_at <= ?`).all(cutoff, cutoff);
    },
  },
};

function campaignPreview(key) {
  const camp = CAMPAIGNS[key];
  if (!camp) throw new Error('Unknown campaign');
  const people = camp.audience().filter((c) => c.stage !== 'dnc');
  const text = people.filter((c) => !store.blockReason(c, 'sms')).length;
  const call = people.filter((c) => store.blockReason(c, 'sms') && !store.blockReason(c, 'call')).length;
  return { key, label: camp.label, why: camp.why, total: people.length, will_text: text, will_call: call, skipped: people.length - text - call };
}

/** Put a campaign on your list, spread over the coming days (perDay customers per day). */
function runCampaign(key, perDay = 10) {
  const camp = CAMPAIGNS[key];
  if (!camp) throw new Error('Unknown campaign');
  perDay = Math.max(1, Math.min(50, Number(perDay) || 10));
  const tpl = store.extraTemplate(camp.template);
  let i = 0, texts = 0, calls = 0;
  for (const c of camp.audience()) {
    if (c.stage === 'dnc') continue;
    if (db.prepare("SELECT 1 FROM tasks WHERE customer_id = ? AND source = 'campaign' AND status = 'pending'").get(c.id)) continue;
    const due_at = new Date(Date.now() + Math.floor(i / perDay) * 86400000).toISOString();
    if (!store.blockReason(c, 'sms')) {
      if (queue.queueTemplate(c, tpl, { source: 'campaign', due_at })) { texts++; i++; }
    } else if (!store.blockReason(c, 'call')) {
      queue.addTask({ customer_id: c.id, kind: 'call', source: 'campaign', title: camp.call(c), due_at });
      calls++; i++;
    }
  }
  return { queued: i, texts, calls, days: Math.ceil(i / perDay) };
}

// ---------------- birthdays & referrals ----------------
function birthdayTick() {
  const s = store.getSettings();
  const { date } = store.localParts(new Date(), s.timezone);
  const mmdd = date.slice(5);
  const tpl = store.extraTemplate('birthday');
  let n = 0;
  for (const c of db.prepare("SELECT * FROM customers WHERE birthday = ? AND stage != 'dnc'").all(mmdd)) {
    const already = db.prepare("SELECT 1 FROM tasks WHERE customer_id = ? AND source = 'birthday' AND created_at >= ?").get(c.id, new Date(Date.now() - 300 * 86400000).toISOString());
    if (already || store.blockReason(c, 'sms')) continue;
    if (queue.queueTemplate(c, tpl, { source: 'birthday' })) n++;
  }
  return n;
}

// When a referred customer buys, thank whoever sent them.
store.stageHooks.push((id, stage, oldStage) => {
  if (stage !== 'sold' || oldStage === 'sold') return;
  const c = store.getCustomerRow(id);
  if (!c || !c.referred_by_id) return;
  const ref = store.getCustomerRow(c.referred_by_id);
  if (!ref || ref.stage === 'dnc') return;
  const tpl = store.extraTemplate('referral_thanks');
  const done = queue.queueTemplate(ref, tpl, { source: 'referral', extra: { referral_name: nm(c) } });
  if (!done && !store.blockReason(ref, 'call')) {
    queue.addTask({ customer_id: ref.id, kind: 'call', source: 'referral', title: `Call ${nm(ref)} to thank them: ${nm(c)} bought, and they referred them.` });
  }
});

// ---------------- your lead page ----------------
const hits = new Map();
function rateLimited(ip) {
  const now = Date.now();
  const list = (hits.get(ip) || []).filter((t) => now - t < 3600000);
  list.push(now);
  hits.set(ip, list);
  return list.length > 5;
}

/** A shopper filled in your lead page. */
async function leadFromPage(form, ip) {
  if (form.website) return { ok: true }; // spam trap
  if (rateLimited(ip || 'x')) throw new Error('Too many submissions. Please call or text instead.');
  const phone = store.normalizePhone(form.phone);
  const email = store.normalizeEmail(form.email);
  if (!form.first_name || (!phone && !email)) throw new Error('Please add your name and a phone number or email.');
  const s = store.getSettings();
  const consent = form.consent === 'yes' || form.consent === 'on' || form.consent === true;
  const { customer, created } = store.upsertCustomer({
    first_name: String(form.first_name).slice(0, 60), last_name: String(form.last_name || '').slice(0, 60), phone, email,
    vehicle_interest: String(form.vehicle || '').slice(0, 120), notes: form.message ? `From my page: ${String(form.message).slice(0, 500)}` : '',
    stage: 'new_lead', source: 'My lead page', referred_by: form.referred_by ? String(form.referred_by).slice(0, 80) : undefined,
    ...(consent ? { consent: true, consent_source: `Checked the consent box on my lead page (${new Date().toLocaleString('en-US', { timeZone: s.timezone })}, IP ${ip || 'unknown'})` } : {}),
  });
  if (!created && consent) store.setConsent(customer.id, true, `Checked the consent box on my lead page (${new Date().toISOString()})`);
  queue.addTask({ customer_id: customer.id, kind: 'call', source: 'new_lead',
    title: `NEW LEAD from your page: ${nm(customer)}${customer.vehicle_interest ? `, looking for: ${customer.vehicle_interest}` : ''}. Respond within 5 minutes.${form.message ? ` They wrote: "${String(form.message).slice(0, 140)}"` : ''}` });
  queue.generateDue();
  notifyOwner(`New lead: ${nm(customer)}`, `${nm(customer)} just filled in your lead page.\nPhone: ${phone || '-'}\nEmail: ${email || '-'}\nLooking for: ${customer.vehicle_interest || '-'}\nMessage: ${form.message || '-'}\nConsent to texts: ${consent ? 'yes' : 'no'}\n\nRespond within 5 minutes.`).catch(() => {});
  return { ok: true, id: customer.id };
}

function vcard() {
  const s = store.getSettings();
  const [first, ...rest] = String(s.salesperson || 'Sales').split(' ');
  return ['BEGIN:VCARD', 'VERSION:3.0', `N:${rest.join(' ')};${first};;;`, `FN:${s.salesperson || 'Sales'}`, `ORG:${s.dealership || ''}`,
    s.dealer_phone ? `TEL;TYPE=CELL:${s.dealer_phone}` : '', s.dealer_address ? `ADR;TYPE=WORK:;;${s.dealer_address};;;;` : '', 'END:VCARD']
    .filter(Boolean).join('\r\n') + '\r\n';
}

module.exports = { saveVehicle, findMatches, onNewVehicle, onVehicleSold, CAMPAIGNS, campaignPreview, runCampaign, birthdayTick, leadFromPage, vcard };
