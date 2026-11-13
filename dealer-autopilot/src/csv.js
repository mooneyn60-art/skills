// Minimal, forgiving CSV parser + column auto-mapping for customer and inventory lists.

function parseCsv(text) {
  text = String(text || '').replace(/^﻿/, '');
  // Auto-detect delimiter: tab (pasted from Excel/Sheets) or comma.
  const firstLine = text.split(/\r?\n/)[0] || '';
  const delim = (firstLine.match(/\t/g) || []).length > (firstLine.match(/,/g) || []).length ? '\t' : ',';
  const rows = [];
  let row = [], field = '', inQ = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (inQ) {
      if (ch === '"' && text[i + 1] === '"') { field += '"'; i++; }
      else if (ch === '"') inQ = false;
      else field += ch;
    } else if (ch === '"') inQ = true;
    else if (ch === delim) { row.push(field); field = ''; }
    else if (ch === '\n' || ch === '\r') {
      if (ch === '\r' && text[i + 1] === '\n') i++;
      row.push(field); rows.push(row); row = []; field = '';
    } else field += ch;
  }
  if (field !== '' || row.length) { row.push(field); rows.push(row); }
  return rows.filter((r) => r.some((x) => String(x).trim() !== ''));
}

const CUSTOMER_ALIASES = {
  first_name: ['first name', 'first', 'firstname', 'fname', 'given name', 'customer first name', 'buyer first name'],
  last_name: ['last name', 'last', 'lastname', 'lname', 'surname', 'customer last name', 'buyer last name'],
  full_name: ['name', 'full name', 'customer', 'customer name', 'client'],
  phone: ['phone', 'cell', 'mobile', 'cell phone', 'cellphone', 'phone number', 'mobile phone', 'number', 'home phone', 'day phone', 'evening phone', 'work phone', 'tel', 'customer cell phone', 'primary phone'],
  email: ['email', 'e mail', 'email address', 'mail', 'customer email', 'primary email'],
  stock_numbers: ['stock', 'stock #', 'stock number', 'stock no', 'stock#', 'stk', 'stk#', 'stock numbers', 'vehicle stock', 'stocknumber', 'vehicle stock number', 'sought stock number'],
  vehicle_interest: ['vehicle', 'vehicle of interest', 'interest', 'car', 'model', 'year make model', 'ymm', 'vehicle interest', 'sought vehicle', 'vehicle sought'],
  objection: ['objection', 'held back', 'concern', 'reason not sold', 'lost reason'],
  notes: ['notes', 'note', 'comments', 'comment'],
  source: ['source', 'lead source', 'lead provider'],
  stage: ['stage', 'bucket', 'type', 'category', 'list', 'sales step', 'sales status', 'lead type', 'lead status', 'status', 'up type'],
  sold_date: ['sold date', 'date sold', 'delivery date', 'delivered date', 'purchase date'],
  lead_at: ['lead date', 'created', 'date created', 'created date', 'lead created', 'received', 'date received'],
  consent: ['consent', 'opt in', 'optin', 'sms opt in', 'text opt in', 'ok to text', 'okay to text', 'tcpa consent', 'text consent'],
  do_not_contact: ['do not contact', 'dnc', 'do not solicit', 'opted out', 'opt out'],
  do_not_text: ['do not text', 'no text', 'do not sms'],
  on_dnc_registry: ['do not call', 'national dnc', 'dnc registry', 'on dnc'],
};

const INVENTORY_ALIASES = {
  stock_number: ['stock', 'stock #', 'stock number', 'stock no', 'stock#', 'stk', 'stk#', 'stocknumber'],
  year: ['year', 'yr'], make: ['make'], model: ['model'], trim: ['trim', 'series'],
  color: ['color', 'exterior color', 'ext color'], price: ['price', 'internet price', 'sale price', 'asking price', 'msrp'],
  miles: ['miles', 'mileage', 'odometer'], vin: ['vin'], status: ['status'],
};

function key(s) { return String(s || '').trim().toLowerCase().replace(/[_\-.]+/g, ' ').replace(/\s+/g, ' '); }

function mapHeaders(headers, aliases) {
  const map = {};
  headers.forEach((h, i) => {
    const k = key(h);
    for (const [field, names] of Object.entries(aliases)) {
      if (map[field] !== undefined) continue;
      if (k === field.replace(/_/g, ' ') || names.includes(k)) { map[field] = i; break; }
    }
  });
  return map;
}

/** Map a stage/status word (including DealerSocket-style sales steps) to one of our 7 stages. */
function stageFrom(v) {
  const k = key(v);
  if (!k) return '';
  if (/(sold|deliver|purchas|won)/.test(k)) return 'sold';
  if (/(do not|dnc|opt.?out|unsubscrib)/.test(k)) return 'dnc';
  if (/(lost|dead|bought elsewhere|inactive|outreach|orphan|cold)/.test(k)) return 'lost';
  if (/(appointment|appt|scheduled)/.test(k)) return 'appointment';
  if (/(be.?back|showroom|walk.?in|visit|demo|write.?up|unsold|follow)/.test(k)) return 'be_back';
  if (/(phone|call.?in)/.test(k)) return 'phone_up';
  if (/(internet|web|online|lead|new|prospect|email)/.test(k)) return 'new_lead';
  return '';
}

/** Turn CSV text into customer objects. defaultStage applies when a row has no recognisable stage. */
function customersFromCsv(text, defaultStage) {
  const rows = parseCsv(text);
  if (rows.length < 2) return { customers: [], headers: rows[0] || [], mapped: {} };
  const headers = rows[0];
  const m = mapHeaders(headers, CUSTOMER_ALIASES);
  const get = (r, f) => (m[f] !== undefined ? String(r[m[f]] ?? '').trim() : '');
  const customers = rows.slice(1).map((r) => {
    let first = get(r, 'first_name'), last = get(r, 'last_name');
    if (!first && !last && get(r, 'full_name')) {
      const full = get(r, 'full_name');
      if (full.includes(',')) { [last, first] = full.split(',').map((s) => s.trim()); }
      else { const parts = full.split(/\s+/); first = parts.shift(); last = parts.join(' '); }
    }
    return {
      first_name: first, last_name: last,
      phone: get(r, 'phone'), email: get(r, 'email'),
      stock_numbers: get(r, 'stock_numbers'), vehicle_interest: get(r, 'vehicle_interest'),
      objection: get(r, 'objection'),
      notes: get(r, 'notes'), source: get(r, 'source') || 'Import',
      stage: stageFrom(get(r, 'stage')) || defaultStage,
      sold_date: get(r, 'sold_date'),
      lead_at: get(r, 'lead_at') || undefined,
      consent: m.consent !== undefined ? (get(r, 'do_not_text') && /^(1|y|yes|true|x)$/i.test(get(r, 'do_not_text')) ? '0' : get(r, 'consent')) : undefined,
      do_not_contact: get(r, 'do_not_contact'),
      on_dnc_registry: get(r, 'on_dnc_registry'),
    };
  }).filter((c) => c.phone || c.email);
  const mapped = Object.fromEntries(Object.entries(m).map(([f, i]) => [f, headers[i]]));
  return { customers, headers, mapped, skipped: rows.length - 1 - customers.length };
}

function inventoryFromCsv(text) {
  const rows = parseCsv(text);
  if (rows.length < 2) return [];
  const m = mapHeaders(rows[0], INVENTORY_ALIASES);
  return rows.slice(1).map((r) => {
    const o = {};
    for (const f of Object.keys(INVENTORY_ALIASES)) o[f] = m[f] !== undefined ? String(r[m[f]] ?? '').trim() : '';
    o.status = (o.status || '').toLowerCase();
    return o;
  }).filter((v) => v.stock_number);
}

module.exports = { parseCsv, customersFromCsv, inventoryFromCsv, stageFrom };
