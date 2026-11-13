/* Dealer Autopilot dashboard (vanilla JS, no build step). */
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const state = { status: null, view: 'today', group: 'follow_up', stage: '', q: '', tarsHistory: [], calStart: null };

async function api(path, opts = {}) {
  const res = await fetch('/api' + path, {
    method: opts.method || 'GET',
    headers: opts.body ? { 'Content-Type': 'application/json' } : {},
    body: opts.body ? JSON.stringify(opts.body) : undefined,
  });
  if (res.status === 401) { showLogin(); throw new Error('Please sign in'); }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || 'Something went wrong');
  return data;
}
function toast(msg) {
  const t = $('#toast'); t.textContent = msg; t.classList.remove('hidden');
  clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.add('hidden'), 3200);
}
const fail = (e) => toast(e.message);
const fmtDate = (iso) => (iso ? new Date(iso).toLocaleString([], { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' }) : '');
const fmtDay = (iso) => (iso ? new Date(iso).toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' }) : '');
const fullName = (c) => `${c.first_name || ''} ${c.last_name || ''}`.trim() || c.phone || c.email || 'Customer';
const stageLabel = (s) => state.status?.stages[s]?.label || s;
const stagePill = (s) => `<span class="pill ${state.status?.stages[s]?.group || ''}">${esc(stageLabel(s))}</span>`;
const pill = (s, label) => `<span class="pill ${esc(s)}">${esc(label || String(s).replace('_', ' '))}</span>`;
const fmtPhone = (p) => { const d = String(p || '').replace(/\D/g, ''); return d.length === 11 && d[0] === '1' ? `(${d.slice(1, 4)}) ${d.slice(4, 7)}-${d.slice(7)}` : p || ''; };
const isMobile = () => /iPhone|Android|iPad/i.test(navigator.userAgent);

// ---------------- login ----------------
function showLogin() { $('#login').classList.remove('hidden'); $('#app').classList.add('hidden'); }
$('#loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  try {
    await api('/login', { method: 'POST', body: { password: $('#loginPassword').value } });
    $('#login').classList.add('hidden'); boot();
  } catch (err) { $('#loginError').textContent = err.message; }
});

// ---------------- boot / nav ----------------
async function loadStatus() {
  state.status = await api('/status');
  const b = $('#banner');
  const notes = [];
  if (state.status.setup_missing.length) notes.push(`<b>Finish setup:</b> add your ${state.status.setup_missing.map((k) => k.replace('dealer_', 'dealership ').replace('_', ' ')).join(', ')} in <a href="#" data-goto="settings">Settings</a> (your address is required in emails).`);
  if (!state.status.email_live) notes.push('Emails are practice only until you <a href="#" data-goto="settings">connect your email</a>.');
  b.innerHTML = notes.join(' &nbsp; ');
  b.classList.toggle('hidden', !notes.length);
}
async function boot() {
  $('#app').classList.remove('hidden');
  try { await loadStatus(); } catch { return; }
  go(location.hash.slice(1) || 'today');
}
function go(view) {
  state.view = VIEWS[view] ? view : 'today';
  history.replaceState(null, '', '#' + state.view);
  $$('#nav button').forEach((b) => b.classList.toggle('active', b.dataset.view === state.view));
  VIEWS[state.view]().catch(fail);
}
$('#nav').addEventListener('click', (e) => { if (e.target.dataset.view) go(e.target.dataset.view); });
window.addEventListener('hashchange', () => { const v = location.hash.slice(1); if (v && v !== state.view && state.status) go(v); });
document.addEventListener('click', (e) => {
  const g = e.target.closest('[data-goto]'); if (g) { e.preventDefault(); go(g.dataset.goto); }
  const c = e.target.closest('[data-close]'); if (c) $('#' + c.dataset.close).classList.add('hidden');
  const cust = e.target.closest('[data-customer]'); if (cust && !e.target.closest('button,a,input,textarea,select')) openCustomer(Number(cust.dataset.customer));
});
const view = () => $('#view');

// ---------------- TODAY (the daily list) ----------------
async function viewToday() {
  const [d, appts] = await Promise.all([api('/today'), api(`/appointments?from=${startOfDay(0)}&to=${startOfDay(1)}`)]);
  const textNote = d.text_mode === 'phone'
    ? 'Texts send from <b>your phone</b>: tap Send and your Messages app opens with the text ready.'
    : 'Texts send from your registered business number.';
  view().innerHTML = `
    <div class="row" style="justify-content:space-between;margin-bottom:12px">
      <div><h1>Today</h1><div class="muted">${new Date().toLocaleDateString([], { weekday: 'long', month: 'long', day: 'numeric' })}
        ${d.in_text_window ? '' : ' &middot; <span class="flag">Outside texting hours (8 am &ndash; 9 pm). Texts will wait.</span>'}</div></div>
      <div class="row"><button class="btn" id="addCust">+ Add customer</button><button class="btn" id="refresh">Refresh</button></div>
    </div>
    <div class="grid two">
      <section>
        <h2>Call these <span class="count-badge">${d.calls.length}</span></h2>
        <p class="muted" style="margin-top:0">Replies first. Target: ${d.call_target}+ calls a day.</p>
        <div id="callList">${d.calls.map(taskCard).join('') || '<div class="card empty">No calls due. Nice.</div>'}</div>
        <h2 style="margin-top:22px">Appointments today <span class="count-badge">${appts.length}</span></h2>
        ${appts.map((a) => `<div class="task" data-customer="${a.customer_id}"><div class="row"><b>${new Date(a.starts_at).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })}</b>
          <span class="who">${esc(fullName(a))}</span> ${pill(a.status)}</div><div class="src">${esc(state.status.appointment_types[a.type] || a.type)}${a.stock_number ? ' &middot; #' + esc(a.stock_number) : ''}</div></div>`).join('') || '<div class="card empty">None today.</div>'}
      </section>
      <section>
        <h2>Approve these <span class="count-badge">${d.approve.length}</span></h2>
        <p class="muted" style="margin-top:0">${textNote} Edit anything before you send.</p>
        <div id="approveList">${d.approve.map(taskCard).join('') || '<div class="card empty">Nothing waiting for approval.</div>'}</div>
        ${d.automatic.length ? `<h2 style="margin-top:22px">Ready to go automatically <span class="count-badge">${d.automatic.length}</span></h2>
          <p class="muted" style="margin-top:0">${d.text_mode === 'phone' ? 'Approved automations. Texts still need one tap since they come from your phone.' : 'These send on their own inside texting hours.'}</p>
          ${d.automatic.map(taskCard).join('')}` : ''}
      </section>
    </div>`;
  $('#refresh').onclick = async () => { await api('/run-now', { method: 'POST' }); viewToday(); };
  $('#addCust').onclick = () => customerForm();
  bindTasks(view(), viewToday);
}
function startOfDay(offset) { const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() + offset); return d.toISOString(); }

const SOURCE_LABEL = { sequence: 'Follow-up schedule', reply: 'Customer replied', appointment: 'Appointment confirmation', reminder: 'Appointment reminder', no_show: 'No-show', outcome: 'Appointment check', consent: 'Needs consent', manual: 'Drafted',
  new_lead: 'NEW LEAD: respond within 5 min', match: 'Inventory match', campaign: 'Campaign', birthday: 'Birthday', referral: 'Referral thank-you' };
function taskCard(t) {
  const who = `<span class="who" data-customer="${t.customer_id}">${esc(fullName(t))}</span>`;
  const meta = `<div class="src">${esc(SOURCE_LABEL[t.source] || t.source)} &middot; ${stageLabel(t.stage)}${t.stocks ? ' &middot; #' + esc(t.stocks) : ''}${t.phone ? ' &middot; ' + esc(fmtPhone(t.phone)) : ''}</div>`;
  if (t.kind === 'check') {
    return `<div class="task" data-task="${t.id}">${who}<div>${esc(t.title)}</div>${meta}
      <div class="row"><button class="btn small" data-outcome="showed-sold">Showed + sold</button><button class="btn small" data-outcome="showed-unsold">Showed, not yet</button>
      <button class="btn small danger" data-outcome="no_show">No-show</button></div></div>`;
  }
  if (t.kind === 'call') {
    return `<div class="task ${t.source === 'reply' || t.source === 'new_lead' ? 'reply' : ''}" data-task="${t.id}">
      <div class="row" style="justify-content:space-between">${who}${t.phone ? `<a class="btn small" href="tel:${esc(t.phone)}">Call ${esc(fmtPhone(t.phone))}</a>` : ''}</div>
      <div>${esc(t.title)}</div>${meta}
      <input placeholder="Call notes (optional)" data-note>
      <div class="row"><button class="btn small primary" data-act="done">Called</button><button class="btn small" data-act="skip">Skip</button>
      ${t.source === 'consent' ? '<button class="btn small" data-consent>They said yes to texts</button>' : ''}</div></div>`;
  }
  return `<div class="task" data-task="${t.id}" data-kind="${t.kind}" data-phone="${esc(t.phone || '')}">
    <div class="row" style="justify-content:space-between">${who}<span class="pill ${t.kind === 'sms' ? 'follow_up' : 'outreach'}">${t.kind === 'sms' ? 'Text' : 'Email'}</span></div>${meta}
    ${t.kind === 'email' ? `<input data-subject value="${esc(t.subject)}">` : ''}
    <textarea data-body rows="${t.kind === 'email' ? 7 : 4}">${esc(t.body)}</textarea>
    ${/\[[^\]]+\]/.test(t.body) ? '<div class="flag">Fill in the [bracketed] parts first.</div>' : ''}
    ${t.blocked_reason ? `<div class="flag">${esc(t.blocked_reason)}</div>` : ''}
    <div class="row"><button class="btn small primary" data-act="send">${t.kind === 'sms' ? 'Send text' : 'Send email'}</button>
      <button class="btn small" data-act="skip">Skip</button><button class="btn small" data-replied>They replied</button>
      ${t.kind === 'sms' ? '<button class="btn small" data-copy>Copy</button>' : ''}</div></div>`;
}
function bindTasks(root, after) {
  root.querySelectorAll('[data-task]').forEach((card) => {
    const id = Number(card.dataset.task);
    const custId = Number(card.querySelector('[data-customer]')?.dataset.customer);
    card.querySelectorAll('[data-act]').forEach((btn) => btn.onclick = async () => {
      const action = btn.dataset.act;
      const body = card.querySelector('[data-body]')?.value;
      const subject = card.querySelector('[data-subject]')?.value;
      const note = card.querySelector('[data-note]')?.value;
      try {
        const r = await api('/tasks/' + id, { method: 'POST', body: { action, body, subject, note } });
        if (r.sms_link) {
          if (isMobile()) location.href = r.sms_link;
          else { await navigator.clipboard?.writeText(body).catch(() => {}); toast('Copied. Paste it into a text to the customer from your phone.'); }
        } else toast(action === 'skip' ? 'Skipped' : action === 'done' ? 'Logged' : r.status === 'simulated' ? 'Logged, but not sent: connect your email in Settings' : 'Sent');
        after();
      } catch (e) { fail(e); }
    });
    const copy = card.querySelector('[data-copy]');
    if (copy) copy.onclick = () => navigator.clipboard.writeText(card.querySelector('[data-body]').value).then(() => toast('Copied'));
    const rep = card.querySelector('[data-replied]');
    if (rep) rep.onclick = () => repliedPrompt(custId, after);
    const consent = card.querySelector('[data-consent]');
    if (consent) consent.onclick = async () => {
      const how = prompt('How did they agree? (e.g. "said yes on the phone")', 'Said yes on the phone');
      if (how === null) return;
      await api('/customers/' + custId, { method: 'PUT', body: { consent: true, consent_source: how } }).catch(fail);
      await api('/tasks/' + id, { method: 'POST', body: { action: 'done', note: 'Got consent: ' + how } }).catch(fail);
      toast('Consent recorded'); after();
    };
    card.querySelectorAll('[data-outcome]').forEach((btn) => btn.onclick = async () => {
      const [status, result] = btn.dataset.outcome.split('-');
      const t = await api('/today').then((d) => [...d.calls].find((x) => x.id === id));
      const body = { status };
      if (result) body.result = result;
      if (result === 'unsold') { const o = prompt('What held them back? (one thing: payment, trade, colour, spouse...)'); if (o === null) return; body.objection = o; }
      try { await api('/appointments/' + t.appointment_id, { method: 'PUT', body }); toast('Saved'); after(); } catch (e) { fail(e); }
    });
  });
}
function repliedPrompt(custId, after) {
  modal(`<h2>They replied</h2><p class="muted">Their automation stops and they go to the top of your call list.</p>
    <label>What did they say? (optional)</label><textarea id="replyText" rows="3"></textarea>
    <div class="row" style="margin-top:12px;justify-content:flex-end"><button class="btn" data-close="modal">Cancel</button><button class="btn primary" id="saveReply">Save</button></div>`);
  $('#saveReply').onclick = async () => {
    try { await api(`/customers/${custId}/replied`, { method: 'POST', body: { text: $('#replyText').value } }); closeModal(); toast('On your call list'); after(); } catch (e) { fail(e); }
  };
}

// ---------------- CUSTOMERS ----------------
async function viewCustomers() {
  const groups = state.status.groups;
  const counts = state.status.counts;
  const gCount = (g) => groups[g].stages.reduce((a, s) => a + (counts[s] || 0), 0);
  const rows = await api(`/customers?group=${state.group}${state.stage ? '&stage=' + state.stage : ''}${state.q ? '&q=' + encodeURIComponent(state.q) : ''}`);
  view().innerHTML = `
    <div class="row" style="justify-content:space-between;margin-bottom:10px"><h1>Customers</h1>
      <div class="row"><input id="search" placeholder="Search name, phone, stock #..." value="${esc(state.q)}" style="width:240px"><button class="btn primary" id="addCust">+ Add</button></div></div>
    <div class="tabs" id="groupTabs">${Object.entries(groups).map(([g, v]) => `<button data-g="${g}" class="${g === state.group ? 'active' : ''}">${esc(v.label)} <span class="count-badge">${gCount(g)}</span></button>`).join('')}</div>
    ${groups[state.group].stages.length > 1 ? `<div class="tabs" id="stageTabs"><button data-s="" class="${!state.stage ? 'active' : ''}">All</button>${groups[state.group].stages.map((s) => `<button data-s="${s}" class="${s === state.stage ? 'active' : ''}">${esc(stageLabel(s))} (${counts[s] || 0})</button>`).join('')}</div>` : ''}
    <div class="table-wrap card" style="padding:0"><table>
      <thead><tr><th>Name</th><th>Stage</th><th>Status</th><th>Stock #</th><th>Consent</th><th>Last contact</th><th>Next step</th></tr></thead>
      <tbody>${rows.map((c) => `<tr class="click" data-customer="${c.id}">
        <td><b>${esc(fullName(c))}</b><div class="muted">${esc(fmtPhone(c.phone))}${c.email ? ' &middot; ' + esc(c.email) : ''}</div></td>
        <td>${stagePill(c.stage)}</td><td>${pill(c.status)}</td><td>${esc(c.stocks || c.vehicle_interest || '')}</td>
        <td>${c.stage === 'dnc' ? '<span class="flag">DNC</span>' : c.consent ? '<span class="ok">Yes</span>' : '<span class="muted">No</span>'}${c.on_dnc_registry ? ' <span class="flag">Registry</span>' : ''}</td>
        <td>${fmtDate(c.last_contact_at)}</td><td>${c.open_tasks ? `<b>${c.open_tasks} on today's list</b>` : fmtDate(c.next_touch_at)}</td></tr>`).join('')
        || '<tr><td colspan="7" class="empty">No customers here yet. <a href="#" data-goto="import">Import a list</a> or add one.</td></tr>'}</tbody></table></div>`;
  $('#groupTabs').onclick = (e) => { const b = e.target.closest('[data-g]'); if (b) { state.group = b.dataset.g; state.stage = ''; viewCustomers().catch(fail); } };
  $('#stageTabs')?.addEventListener('click', (e) => { const b = e.target.closest('[data-s]'); if (b) { state.stage = b.dataset.s; viewCustomers().catch(fail); } });
  let t; $('#search').oninput = (e) => { clearTimeout(t); t = setTimeout(() => { state.q = e.target.value; viewCustomers().then(() => { const s = $('#search'); s.focus(); s.setSelectionRange(s.value.length, s.value.length); }).catch(fail); }, 300); };
  $('#addCust').onclick = () => customerForm();
}

function stageOptions(sel) { return Object.entries(state.status.stages).map(([k, v]) => `<option value="${k}" ${k === sel ? 'selected' : ''}>${esc(v.label)}</option>`).join(''); }
function customerForm(c = null) {
  const v = c || { stage: state.view === 'customers' && state.stage ? state.stage : 'new_lead' };
  modal(`<h2>${c ? 'Edit customer' : 'Add customer'}</h2>
    <div class="grid two"><div><label>First name</label><input id="f_first" value="${esc(v.first_name)}"></div><div><label>Last name</label><input id="f_last" value="${esc(v.last_name)}"></div></div>
    <div class="grid two"><div><label>Mobile</label><input id="f_phone" value="${esc(v.phone)}" inputmode="tel"></div><div><label>Email</label><input id="f_email" value="${esc(v.email)}" type="email"></div></div>
    <div class="grid two"><div><label>Stage</label><select id="f_stage">${stageOptions(v.stage)}</select></div>
      <div><label>Stock #(s)</label><input id="f_stock" value="${esc((v.interests || []).map((i) => i.stock_number).join(', '))}" placeholder="24518, T1122"></div></div>
    <label>Vehicle of interest (if no stock #)</label><input id="f_vehicle" value="${esc(v.vehicle_interest)}">
    <label>The one thing holding them back</label><input id="f_objection" value="${esc(v.objection)}" placeholder="payment, trade value, colour, spouse...">
    <div class="grid two"><div><label>Referred by (name or phone)</label><input id="f_ref" value="${esc(v.referred_by_name)}"></div>
      <div><label>Birthday (MM-DD)</label><input id="f_bday" value="${esc(v.birthday)}" placeholder="03-15"></div></div>
    <label>Notes</label><textarea id="f_notes" rows="2">${esc(v.notes)}</textarea>
    <div class="card" style="margin-top:12px;padding:10px">
      <label class="switch"><input type="checkbox" id="f_consent" ${v.consent ? 'checked' : ''}> They agreed to get texts / emails from me</label>
      <label>How they agreed</label><input id="f_consent_src" value="${esc(v.consent_source)}" placeholder="Lead form opt-in, said yes in person, texted me first...">
      <label class="switch" style="margin-top:8px"><input type="checkbox" id="f_dnc" ${v.on_dnc_registry ? 'checked' : ''}> Number is on the Do Not Call registry</label>
      <label class="switch"><input type="checkbox" id="f_init" ${v.customer_initiated === 0 ? '' : 'checked'}> They contacted the dealership first</label>
    </div>
    <p class="muted" style="font-size:12px">Never store credit, SSN, licence or income info here.</p>
    <div class="row" style="justify-content:flex-end;margin-top:8px"><button class="btn" data-close="modal">Cancel</button><button class="btn primary" id="f_save">Save</button></div>`);
  $('#f_save').onclick = async () => {
    const body = {
      first_name: $('#f_first').value, last_name: $('#f_last').value, phone: $('#f_phone').value, email: $('#f_email').value,
      stage: $('#f_stage').value, stock_numbers: $('#f_stock').value, vehicle_interest: $('#f_vehicle').value, objection: $('#f_objection').value,
      notes: $('#f_notes').value, consent: $('#f_consent').checked, consent_source: $('#f_consent_src').value,
      on_dnc_registry: $('#f_dnc').checked, customer_initiated: $('#f_init').checked,
      referred_by: $('#f_ref').value, birthday: $('#f_bday').value,
    };
    if (!body.phone && !body.email) return toast('Add a phone or email');
    if (body.consent && !body.consent_source) return toast('Note how they agreed to be contacted');
    try {
      const r = c ? await api('/customers/' + c.id, { method: 'PUT', body }) : (await api('/customers', { method: 'POST', body })).customer;
      closeModal(); await api('/run-now', { method: 'POST' }); await loadStatus(); toast('Saved'); openCustomer(r.id); VIEWS[state.view]();
    } catch (e) { fail(e); }
  };
}

async function openCustomer(id) {
  const c = await api('/customers/' + id).catch(fail);
  if (!c) return;
  $('#drawerTitle').textContent = fullName(c);
  const stockChips = c.interests.map((i) => `<span class="chip">#${esc(i.stock_number)}${i.make ? ' ' + esc([i.year, i.make, i.model].filter(Boolean).join(' ')) : ''}</span>`).join('') || '<span class="muted">None</span>';
  const thread = c.messages.map((m) => m.direction === 'in'
    ? `<div class="bubble in">${esc(m.body)}<div class="meta">${m.channel} &middot; ${fmtDate(m.created_at)}</div></div>`
    : `<div class="bubble out ${['skipped', 'failed'].includes(m.status) ? 'bad' : ''}">${m.subject ? '<b>' + esc(m.subject) + '</b>\n' : ''}${esc(m.body)}<div class="meta">${m.channel === 'call' ? 'call' : m.channel} &middot; ${esc(m.status)}${m.error ? ': ' + esc(m.error) : ''}${m.automated ? ' &middot; auto' : ''} &middot; ${fmtDate(m.created_at)}</div></div>`).join('');
  $('#drawerBody').innerHTML = `
    <div class="section row">${stagePill(c.stage)} ${pill(c.status)} ${c.stage === 'dnc' ? '<span class="flag">Do not contact</span>' : ''}</div>
    <div class="section kv">
      <div>Mobile</div><div>${c.phone ? `<a href="tel:${esc(c.phone)}">${esc(fmtPhone(c.phone))}</a>` : '-'}</div>
      <div>Email</div><div>${esc(c.email || '-')}${c.email_opt_out ? ' <span class="flag">unsubscribed</span>' : ''}</div>
      <div>Consent</div><div>${c.consent ? `<span class="ok">Yes</span> &middot; ${esc(c.consent_source)} &middot; ${fmtDay(c.consent_date)}` : '<span class="flag">Not recorded</span>'}</div>
      <div>DNC registry</div><div>${c.on_dnc_registry ? `<span class="flag">On registry</span>${c.customer_initiated ? ' (they contacted us first)' : ''}` : 'No'}</div>
      <div>Holding back</div><div>${esc(c.objection || '-')}</div>
      <div>Source</div><div>${esc(c.source || '-')}</div>
      ${c.referred_by_name ? `<div>Referred by</div><div>${c.referred_by_id ? `<a href="#" data-open="${c.referred_by_id}">${esc(c.referred_by_name)}</a>` : esc(c.referred_by_name) + ' <span class="muted">(not matched to a customer)</span>'}</div>` : ''}
      ${c.birthday ? `<div>Birthday</div><div>${esc(c.birthday)}</div>` : ''}
      ${c.sold_date ? `<div>Sold</div><div>${esc(c.sold_date)}</div>` : ''}
      <div>Stock #s</div><div class="chips">${stockChips}</div>
      ${c.notes ? `<div>Notes</div><div style="white-space:pre-wrap">${esc(c.notes)}</div>` : ''}
    </div>
    <div class="section row">
      <button class="btn small" id="d_edit">Edit</button>
      <button class="btn small" id="d_replied">They replied</button>
      <button class="btn small" id="d_appt">Book appointment</button>
      <button class="btn small" id="d_draft">Write a text/email</button>
      ${c.stage !== 'sold' && c.stage !== 'dnc' ? '<button class="btn small" id="d_sold">Mark sold</button>' : ''}
      ${c.status === 'active' ? '<button class="btn small" id="d_pause">Pause</button>' : c.stage !== 'dnc' ? '<button class="btn small" id="d_resume">Resume follow-up</button>' : ''}
      ${c.stage !== 'dnc' ? '<button class="btn small danger" id="d_dnc">Do not contact</button>' : ''}
    </div>
    <div class="section"><h3>Move to stage</h3><select id="d_stage">${stageOptions(c.stage)}</select></div>
    ${c.blocks.sms || c.blocks.email ? `<div class="section card" style="padding:10px"><b>Why some messages won't go out:</b><br>${c.blocks.sms ? 'Texts: ' + esc(c.blocks.sms) + '<br>' : ''}${c.blocks.email ? 'Email: ' + esc(c.blocks.email) : ''}</div>` : ''}
    ${c.next_step ? `<div class="section"><h3>Next scheduled (step ${c.step_index + 1} of ${c.total_steps}, ${fmtDate(c.next_touch_at)})</h3><div class="preview">${c.next_step.channel.toUpperCase()}: ${esc(c.next_step.preview)}</div></div>` : ''}
    ${c.appointments.length ? `<div class="section"><h3>Appointments</h3>${c.appointments.map((a) => `<div class="row" style="margin-bottom:6px">${fmtDate(a.starts_at)} &middot; ${esc(state.status.appointment_types[a.type] || a.type)} ${pill(a.status)}</div>`).join('')}</div>` : ''}
    <div class="section"><h3>History</h3><div class="thread">${thread || '<span class="muted">Nothing yet.</span>'}</div></div>
    <div class="section"><button class="btn small danger" id="d_delete">Delete customer</button></div>`;
  $('#drawer').classList.remove('hidden');
  const refresh = async () => { await loadStatus(); openCustomer(id); VIEWS[state.view]().catch(() => {}); };
  const put = (body) => api('/customers/' + id, { method: 'PUT', body }).then(refresh).catch(fail);
  $('#d_edit').onclick = () => customerForm(c);
  $$('#drawerBody [data-open]').forEach((a) => a.onclick = (e) => { e.preventDefault(); openCustomer(Number(a.dataset.open)); });
  $('#d_replied').onclick = () => repliedPrompt(id, refresh);
  $('#d_appt').onclick = () => apptForm({ customer: c });
  $('#d_draft').onclick = () => draftForm(c, refresh);
  $('#d_sold') && ($('#d_sold').onclick = () => put({ stage: 'sold' }));
  $('#d_pause') && ($('#d_pause').onclick = () => put({ status: 'paused' }));
  $('#d_resume') && ($('#d_resume').onclick = () => put({ status: 'active' }));
  $('#d_dnc') && ($('#d_dnc').onclick = () => confirm('Mark as Do Not Contact? Nothing will ever go to them again.') && put({ stage: 'dnc' }));
  $('#d_stage').onchange = (e) => put({ stage: e.target.value });
  $('#d_delete').onclick = async () => { if (confirm('Delete this customer and their history?')) { await api('/customers/' + id, { method: 'DELETE' }); $('#drawer').classList.add('hidden'); refresh(); } };
}
function draftForm(c, after) {
  modal(`<h2>Write to ${esc(fullName(c))}</h2>
    <label>Type</label><select id="dr_ch"><option value="sms">Text</option><option value="email">Email</option></select>
    <div id="dr_subj_wrap" class="hidden"><label>Subject</label><input id="dr_subj"></div>
    <label>Message</label><textarea id="dr_body" rows="5" placeholder="Hi {first_name}, it's {salesperson}..."></textarea>
    <p class="muted" style="font-size:12px">Goes onto Today's approval list. One ask per message, no price promises.</p>
    <div class="row" style="justify-content:flex-end"><button class="btn" data-close="modal">Cancel</button><button class="btn primary" id="dr_save">Add to approval list</button></div>`);
  $('#dr_ch').onchange = (e) => $('#dr_subj_wrap').classList.toggle('hidden', e.target.value !== 'email');
  $('#dr_save').onclick = async () => {
    try { await api(`/customers/${c.id}/draft`, { method: 'POST', body: { channel: $('#dr_ch').value, subject: $('#dr_subj').value, body: $('#dr_body').value } }); closeModal(); toast("Added to today's list"); after(); } catch (e) { fail(e); }
  };
}

// ---------------- CALENDAR ----------------
function apptForm({ customer, appt, date } = {}) {
  const a = appt || {};
  const d = a.starts_at ? new Date(a.starts_at) : date ? new Date(date + 'T10:00') : new Date(Date.now() + 86400000);
  const local = new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
  modal(`<h2>${appt ? 'Appointment' : 'Book appointment'}</h2>
    ${customer || appt ? `<p><b>${esc(fullName(customer || appt))}</b></p>` : `<label>Customer</label><input id="a_search" placeholder="Search name or phone"><div id="a_results"></div>`}
    <div class="grid two"><div><label>When</label><input id="a_when" type="datetime-local" value="${local}"></div>
      <div><label>Type</label><select id="a_type">${Object.entries(state.status.appointment_types).map(([k, v]) => `<option value="${k}" ${k === (a.type || 'test_drive') ? 'selected' : ''}>${v}</option>`).join('')}</select></div></div>
    <div class="grid two"><div><label>Stock #</label><input id="a_stock" value="${esc(a.stock_number || customer?.interests?.[0]?.stock_number || '')}"></div>
      <div><label>Length (min)</label><input id="a_dur" type="number" value="${a.duration_min || 60}"></div></div>
    <label>Notes</label><input id="a_notes" value="${esc(a.notes)}">
    ${appt ? `<label>Status</label><select id="a_status">${['scheduled', 'confirmed', 'showed', 'no_show', 'cancelled'].map((s) => `<option ${s === a.status ? 'selected' : ''} value="${s}">${s.replace('_', '-')}</option>`).join('')}</select>` : '<p class="muted" style="font-size:12px">A confirmation text is drafted for you, and reminders are queued for the day before and 2 hours before.</p>'}
    <div class="row" style="justify-content:space-between;margin-top:12px">${appt ? '<button class="btn danger" id="a_del">Delete</button>' : '<span></span>'}
      <div class="row"><button class="btn" data-close="modal">Cancel</button><button class="btn primary" id="a_save">Save</button></div></div>`);
  let pickedId = customer?.id || a.customer_id;
  const s = $('#a_search');
  if (s) s.oninput = async () => {
    const rows = s.value.length > 1 ? await api('/customers?q=' + encodeURIComponent(s.value) + '&limit=6') : [];
    $('#a_results').innerHTML = rows.map((c) => `<button class="btn small" style="margin:4px 4px 0 0" data-pick="${c.id}">${esc(fullName(c))} ${esc(fmtPhone(c.phone))}</button>`).join('');
    $$('#a_results [data-pick]').forEach((b) => b.onclick = () => { pickedId = Number(b.dataset.pick); s.value = b.textContent; $('#a_results').innerHTML = ''; });
  };
  $('#a_save').onclick = async () => {
    if (!pickedId) return toast('Pick a customer');
    const body = { customer_id: pickedId, starts_at: new Date($('#a_when').value).toISOString(), type: $('#a_type').value, stock_number: $('#a_stock').value, duration_min: $('#a_dur').value, notes: $('#a_notes').value };
    try {
      if (appt) {
        body.status = $('#a_status').value;
        if (body.status === 'showed') { const sold = confirm('Did they buy? OK = Sold, Cancel = not yet'); body.result = sold ? 'sold' : 'unsold'; if (!sold) body.objection = prompt('What held them back?') || ''; }
        await api('/appointments/' + appt.id, { method: 'PUT', body });
      } else await api('/appointments', { method: 'POST', body });
      closeModal(); toast('Saved'); await loadStatus(); VIEWS[state.view]().catch(() => {});
      if (!$('#drawer').classList.contains('hidden')) openCustomer(pickedId);
    } catch (e) { fail(e); }
  };
  $('#a_del') && ($('#a_del').onclick = async () => { if (confirm('Delete this appointment?')) { await api('/appointments/' + appt.id, { method: 'DELETE' }); closeModal(); VIEWS[state.view](); } });
}
async function viewCalendar() {
  if (!state.calStart) { const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() - ((d.getDay() + 6) % 7)); state.calStart = d; }
  const start = new Date(state.calStart);
  const end = new Date(start); end.setDate(end.getDate() + 14);
  const list = await api(`/appointments?from=${start.toISOString()}&to=${end.toISOString()}`);
  const days = [...Array(14)].map((_, i) => { const d = new Date(start); d.setDate(d.getDate() + i); return d; });
  const todayKey = new Date().toDateString();
  view().innerHTML = `
    <div class="row" style="justify-content:space-between;margin-bottom:12px"><h1>Calendar</h1>
      <div class="row"><button class="btn" id="c_prev">&larr;</button><button class="btn" id="c_today">This week</button><button class="btn" id="c_next">&rarr;</button><button class="btn primary" id="c_new">+ Appointment</button></div></div>
    <p class="muted">Want these on your phone's calendar? Copy your calendar link from <a href="#" data-goto="settings">Settings</a>.</p>
    <div class="cal-grid">${days.map((d) => {
      const ev = list.filter((a) => new Date(a.starts_at).toDateString() === d.toDateString());
      return `<div class="cal-day ${d.toDateString() === todayKey ? 'today' : ''} ${ev.length ? '' : 'empty-day'}" data-date="${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}">
        <div class="d">${d.toLocaleDateString([], { weekday: 'short', month: 'short', day: 'numeric' })}</div>
        ${ev.map((a) => `<div class="cal-ev ${a.status}" data-appt="${a.id}" title="${esc(fullName(a))}">${new Date(a.starts_at).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })} ${esc(fullName(a))}</div>`).join('')}</div>`;
    }).join('')}</div>`;
  const shift = (n) => { state.calStart.setDate(state.calStart.getDate() + n); viewCalendar().catch(fail); };
  $('#c_prev').onclick = () => shift(-7); $('#c_next').onclick = () => shift(7);
  $('#c_today').onclick = () => { state.calStart = null; viewCalendar().catch(fail); };
  $('#c_new').onclick = () => apptForm();
  $$('.cal-ev').forEach((el) => el.onclick = (e) => { e.stopPropagation(); apptForm({ appt: list.find((a) => a.id === Number(el.dataset.appt)) }); });
  $$('.cal-day').forEach((el) => el.ondblclick = () => apptForm({ date: el.dataset.date }));
}

// ---------------- STOCK ----------------
async function viewStock(q = '') {
  const rows = await api('/stock' + (q ? '?q=' + encodeURIComponent(q) : ''));
  view().innerHTML = `
    <div class="row" style="justify-content:space-between;margin-bottom:12px"><h1>Stock numbers</h1>
      <div class="row"><input id="s_q" placeholder="Search stock #, make, model..." value="${esc(q)}" style="width:240px"><button class="btn primary" id="s_add">+ Vehicle</button></div></div>
    <p class="muted">Every stock number in inventory or that a customer is interested in. Click one to see who wants it.</p>
    <div class="table-wrap card" style="padding:0"><table><thead><tr><th>Stock #</th><th>Vehicle</th><th>Miles</th><th>Status</th><th>Interested</th></tr></thead>
    <tbody>${rows.map((r) => `<tr class="click" data-stock="${esc(r.stock_number)}"><td><b>#${esc(r.stock_number)}</b></td><td>${esc([r.year, r.make, r.model, r.trim].filter(Boolean).join(' ') || '-')}${r.color ? ' &middot; ' + esc(r.color) : ''}</td>
      <td>${esc(r.miles || '')}</td><td>${pill(r.status === 'available' ? 'active' : r.status === 'sold' ? 'opted_out' : 'paused', r.status)}</td><td><b>${r.interested}</b></td></tr>`).join('') || '<tr><td colspan="5" class="empty">No stock yet. Import your inventory on the Import page or add stock #s to customers.</td></tr>'}</tbody></table></div>`;
  let t; $('#s_q').oninput = (e) => { clearTimeout(t); t = setTimeout(() => viewStock(e.target.value).then(() => { const s = $('#s_q'); s.focus(); s.setSelectionRange(s.value.length, s.value.length); }), 300); };
  $('#s_add').onclick = () => stockForm({});
  $$('[data-stock]').forEach((tr) => tr.onclick = () => openStock(tr.dataset.stock));
}
function stockForm(v) {
  modal(`<h2>${v.stock_number ? 'Vehicle #' + esc(v.stock_number) : 'Add vehicle'}</h2>
    <div class="grid two"><div><label>Stock #</label><input id="v_stock" value="${esc(v.stock_number)}" ${v.stock_number ? 'disabled' : ''}></div><div><label>Year</label><input id="v_year" value="${esc(v.year)}"></div></div>
    <div class="grid two"><div><label>Make</label><input id="v_make" value="${esc(v.make)}"></div><div><label>Model</label><input id="v_model" value="${esc(v.model)}"></div></div>
    <div class="grid two"><div><label>Trim</label><input id="v_trim" value="${esc(v.trim)}"></div><div><label>Color</label><input id="v_color" value="${esc(v.color)}"></div></div>
    <div class="grid two"><div><label>Miles</label><input id="v_miles" value="${esc(v.miles)}"></div><div><label>Status</label><select id="v_status">${['available', 'pending', 'sold'].map((s) => `<option ${s === v.status ? 'selected' : ''}>${s}</option>`).join('')}</select></div></div>
    <div class="row" style="justify-content:flex-end;margin-top:12px"><button class="btn" data-close="modal">Cancel</button><button class="btn primary" id="v_save">Save</button></div>`);
  $('#v_save').onclick = async () => {
    const stock = $('#v_stock').value.trim(); if (!stock) return toast('Stock # required');
    const body = Object.fromEntries(['year', 'make', 'model', 'trim', 'color', 'miles', 'status'].map((k) => [k, $('#v_' + k).value]));
    try { const r = await api('/stock/' + encodeURIComponent(stock), { method: 'PUT', body }); closeModal(); toast(r.drafted ? `Saved. ${r.drafted} text(s) drafted for interested customers (see Today).` : 'Saved'); viewStock(); } catch (e) { fail(e); }
  };
}
async function openStock(stock) {
  const d = await api('/stock/' + encodeURIComponent(stock));
  const v = d.vehicle;
  modal(`<h2>#${esc(stock)} ${esc([v.year, v.make, v.model, v.trim].filter(Boolean).join(' '))}</h2>
    <p class="muted">${d.customers.length} interested customer${d.customers.length === 1 ? '' : 's'}</p>
    ${d.customers.map((c) => `<div class="task" data-customer="${c.id}"><div class="row"><span class="who">${esc(fullName(c))}</span>${stagePill(c.stage)}${pill(c.status)}</div><div class="src">${esc(fmtPhone(c.phone))}</div></div>`).join('')}
    <div class="row" style="justify-content:flex-end;margin-top:12px"><button class="btn" id="v_edit">Edit vehicle</button><button class="btn primary" data-close="modal">Done</button></div>`);
  $('#v_edit').onclick = () => stockForm(v);
  $$('#modalCard [data-customer]').forEach((el) => el.addEventListener('click', closeModal));
}

// ---------------- TEMPLATES ----------------
async function viewTemplates() {
  const all = await api('/templates');
  const s = await api('/settings');
  const KEYS = { confirm: 'When booked', reminder_day: 'Day before', reminder_2h: '2 hours before', no_show: 'After a no-show',
    new_arrival: 'New arrival matches what they wanted', stock_sold: 'The car they liked sold', equity: 'Upgrade campaign (past buyers)', reactivation: 'Reactivate old leads',
    birthday: 'Birthday', referral_thanks: 'Thank a referrer' };
  const stages = [...Object.keys(state.status.stages).filter((k) => k !== 'dnc'), 'extras'];
  const card = (t) => {
    const autoOk = state.status.stages[t.stage]?.auto_ok && t.channel !== 'call';
    return `<div class="step" data-tpl="${t.id}">
      <div class="row">${t.key ? `<b>${KEYS[t.key]}</b>` : `<label style="margin:0">Day</label><input type="number" min="0" data-f="day" value="${t.day}" style="width:80px">
        <select data-f="channel" style="width:110px">${['sms', 'email', 'call'].map((c) => `<option value="${c}" ${c === t.channel ? 'selected' : ''}>${c === 'sms' ? 'Text' : c === 'email' ? 'Email' : 'Call'}</option>`).join('')}</select>`}
        <span class="grow"></span>${t.approved ? '<span class="ok">Approved</span>' : '<span class="muted">Not approved yet</span>'}</div>
      ${t.channel === 'email' ? `<label>Subject</label><input data-f="subject" value="${esc(t.subject)}">` : ''}
      <label>${t.channel === 'call' ? 'Call reminder' : 'Message'}</label><textarea data-f="body" rows="${t.channel === 'email' ? 6 : 3}">${esc(t.body)}</textarea>
      ${t.channel === 'sms' ? `<div class="muted" style="font-size:12px" data-len></div>` : ''}
      <div class="row" style="margin-top:8px">
        <button class="btn small" data-save>Save</button>
        ${t.channel !== 'call' ? `<button class="btn small ${t.approved ? '' : 'primary'}" data-approve>${t.approved ? 'Un-approve' : 'Approve wording'}</button>` : ''}
        ${autoOk ? `<label class="switch"><input type="checkbox" data-auto ${t.auto ? 'checked' : ''} ${t.approved ? '' : 'disabled'}> Send automatically (consented customers only)</label>` : ''}
        ${t.key ? '' : '<button class="btn small danger" data-del>Delete</button>'}
      </div></div>`;
  };
  view().innerHTML = `<h1>Templates</h1>
    <p class="muted">Written in your voice: friendly-professional, one ask per message. Placeholders: {first_name} {vehicle} {stock} {objection} {salesperson} {dealership} {dealer_phone} {review_link} (Grow messages also use {match_vehicle} {match_stock} {referral_name}).
      Text in <code>[[ ]]</code> is left out when its placeholder is empty. Anything in <code>[brackets]</code> is for you to fill in before sending.<br>
      <b>Approve each template once.</b> Only Sold-stage messages and appointment messages can ever send automatically, and only after you approve them and turn on automation:
      <label class="switch"><input type="checkbox" id="autoMaster" ${s.automation_enabled === '1' ? 'checked' : ''}> Automation on</label></p>
    <div class="tabs" id="tplTabs">${stages.map((st, i) => `<button data-st="${st}" class="${i === 0 ? 'active' : ''}">${esc(st === 'extras' ? 'Grow messages' : stageLabel(st))}</button>`).join('')}</div>
    <div class="steps" id="tplList"></div>
    <button class="btn" id="tplAdd">+ Add step</button>`;
  let cur = stages[0];
  const draw = () => {
    const list = all.filter((t) => t.stage === cur);
    $('#tplList').innerHTML = list.map(card).join('') || '<p class="muted">No templates for this stage.</p>';
    $('#tplAdd').classList.toggle('hidden', cur === 'appointment' || cur === 'extras');
    $$('#tplList [data-tpl]').forEach((el) => {
      const id = Number(el.dataset.tpl);
      const val = (f) => el.querySelector(`[data-f="${f}"]`)?.value;
      const len = el.querySelector('[data-len]');
      const updLen = () => { if (len) { const n = val('body').length; len.innerHTML = `${n} characters ${n > 300 ? '<span class="flag">(keep texts under 300)</span>' : ''}`; } };
      updLen(); el.querySelector('[data-f="body"]').oninput = updLen;
      const save = async (extra = {}) => {
        const body = { body: val('body'), subject: val('subject'), day: val('day'), channel: val('channel'), ...extra };
        const r = await api('/templates/' + id, { method: 'PUT', body }).catch(fail);
        if (r) { Object.assign(all.find((t) => t.id === id), r); draw(); toast('Saved'); }
      };
      el.querySelector('[data-save]').onclick = () => save();
      el.querySelector('[data-approve]') && (el.querySelector('[data-approve]').onclick = () => save({ approved: !all.find((t) => t.id === id).approved }));
      el.querySelector('[data-auto]') && (el.querySelector('[data-auto]').onchange = (e) => save({ auto: e.target.checked }));
      el.querySelector('[data-del]') && (el.querySelector('[data-del]').onclick = async () => { if (confirm('Delete this step?')) { await api('/templates/' + id, { method: 'DELETE' }); all.splice(all.findIndex((t) => t.id === id), 1); draw(); } });
    });
  };
  $('#tplTabs').onclick = (e) => { const b = e.target.closest('[data-st]'); if (!b) return; cur = b.dataset.st; $$('#tplTabs button').forEach((x) => x.classList.toggle('active', x === b)); draw(); };
  $('#tplAdd').onclick = async () => { const t = await api('/templates', { method: 'POST', body: { stage: cur, day: 1, channel: 'sms', body: "Hi {first_name}, it's {salesperson}. " } }); all.push(t); draw(); };
  $('#autoMaster').onchange = async (e) => { await api('/settings', { method: 'PUT', body: { automation_enabled: e.target.checked ? '1' : '0' } }); toast(e.target.checked ? 'Automation on for approved Sold + appointment messages' : 'Automation off. Everything waits for you.'); };
  draw();
}

// ---------------- GROW ----------------
async function viewGrow() {
  const g = await api('/grow');
  view().innerHTML = `<h1>Grow</h1><p class="muted">More customers, more sales. Everything here lands on your Today list for approval. Nothing sends on its own.</p>
    <div class="grid two">
      <div class="card"><h2>Your lead page</h2>
        <p class="muted">Share this link on Facebook, Instagram, Marketplace, and in your email and text signatures. Print the QR code on your business cards.
          Shoppers send you their info, tick a proper consent box, and can save your contact. The lead lands at the top of Today with a 5-minute clock (plus an email alert once email is set up).</p>
        <div class="row" style="align-items:flex-start;gap:16px"><img src="${g.qr}" alt="QR code for your lead page" width="140" height="140" style="border-radius:8px;background:#fff;padding:6px">
          <div class="grow"><code class="url">${esc(g.lead_page_url)}</code>
          <div class="row" style="margin-top:8px"><button class="btn small" id="g_copy">Copy link</button><a class="btn small" href="/me" target="_blank" rel="noopener">Open page</a><a class="btn small" href="${g.qr}" download="my-lead-page-qr.png">Download QR</a></div>
          <p class="muted" style="font-size:12px">Leads from this page in the last 30 days: <b>${g.leads_from_page_30d}</b>. Shoppers can only reach it once the app is online at a public address (see the README).</p></div></div>
      </div>
      <div class="card"><h2>Inventory matches</h2>
        <p class="muted">When you add a vehicle (on the Stock #s page, by importing inventory, or by telling TARS "we just got a 2022 RAV4 in"), everyone who asked about that model gets a "just came in" text drafted for you.
          When a car someone liked is marked sold, they get a "that one sold, want me to find something similar?" text drafted. This only applies to customers who agreed to texts.</p>
        <h2 style="margin-top:14px">Referrals &amp; birthdays</h2>
        <p class="muted">Fill in "Referred by" on a customer. When they buy, you get a task to thank whoever sent them. Add birthdays (MM-DD) and a birthday text is drafted on the day.
          Referral sales so far: <b>${g.referral_sales}</b> &middot; Birthdays on file: <b>${g.birthdays_on_file}</b>.</p></div>
    </div>
    <h2 style="margin-top:18px">Campaigns</h2>
    <div class="grid two">${g.campaigns.map((c) => `<div class="card"><h2>${esc(c.label)}</h2><p class="muted">${esc(c.why)}</p>
      <p><b>${c.total}</b> customers &middot; ${c.will_text} get a drafted text &middot; ${c.will_call} go on your call list (no consent to text)${c.skipped ? ` &middot; ${c.skipped} can't be contacted` : ''}</p>
      <div class="row"><label style="margin:0">Per day</label><input type="number" min="1" max="50" value="10" style="width:80px" data-per="${c.key}">
      <button class="btn primary" data-camp="${c.key}" ${c.total ? '' : 'disabled'}>Add to my list</button></div></div>`).join('')}</div>`;
  $('#g_copy').onclick = () => navigator.clipboard.writeText(g.lead_page_url).then(() => toast('Link copied'));
  $$('[data-camp]').forEach((b) => b.onclick = async () => {
    const per = $(`[data-per="${b.dataset.camp}"]`).value;
    if (!confirm(`Put this campaign on your list, ${per} per day?`)) return;
    try { const r = await api('/grow/campaign/' + b.dataset.camp, { method: 'POST', body: { per_day: per } }); toast(`${r.queued} customers queued over ${r.days} day(s)`); viewGrow(); } catch (e) { fail(e); }
  });
}

// ---------------- SCOREBOARD ----------------
async function viewScoreboard() {
  const s = await api('/scoreboard');
  const w = s.weeks;
  const cell = (v, suffix = '', good) => (v === null || v === undefined ? '<td class="num muted">-</td>' : `<td class="num ${good === undefined ? '' : good ? 'good' : 'bad'}">${v}${suffix}</td>`);
  const label = (wk) => new Date(wk.from).toLocaleDateString([], { month: 'short', day: 'numeric' });
  view().innerHTML = `<h1>Scoreboard</h1><p class="muted">Weekly, Monday to Sunday. The four numbers that matter.</p>
    <div class="grid cols-4" style="margin-bottom:16px">
      <div class="card stat"><div class="num">${w[0].median_response_min ?? '-'}${w[0].median_response_min !== null ? '<small> min</small>' : ''}</div><div class="lbl">Response time to new leads (target under 5)</div></div>
      <div class="card stat"><div class="num">${w[0].appointment_rate_pct ?? '-'}${w[0].appointment_rate_pct !== null ? '%' : ''}</div><div class="lbl">Appointment rate (${w[0].appointments_set} of ${w[0].leads} leads)</div></div>
      <div class="card stat"><div class="num">${w[0].show_rate_pct ?? '-'}${w[0].show_rate_pct !== null ? '%' : ''}</div><div class="lbl">Show rate (${w[0].shows} showed, ${w[0].no_shows} no-show)</div></div>
      <div class="card stat"><div class="num">${w[0].close_rate_pct ?? '-'}${w[0].close_rate_pct !== null ? '%' : ''}</div><div class="lbl">Close rate (${w[0].sold} sold)</div></div>
    </div>
    <div class="table-wrap card score" style="padding:0"><table>
      <thead><tr><th>Week of</th><th class="num">Leads</th><th class="num">Median response</th><th class="num">Under 5 min</th><th class="num">Not contacted</th><th class="num">Appts</th><th class="num">Appt rate</th><th class="num">Show rate</th><th class="num">Sold</th><th class="num">Close rate</th></tr></thead>
      <tbody>${w.map((x) => `<tr><td>${label(x)}</td>${cell(x.leads)}${cell(x.median_response_min, ' min', x.median_response_min === null ? undefined : x.median_response_min <= 5)}${cell(x.under_5_min_pct, '%')}${cell(x.not_contacted, '', x.not_contacted === 0)}${cell(x.appointments_set)}${cell(x.appointment_rate_pct, '%')}${cell(x.show_rate_pct, '%')}${cell(x.sold)}${cell(x.close_rate_pct, '%')}</tr>`).join('')}</tbody></table></div>
    <h2 style="margin-top:20px">Which messages get replies (last 8 weeks)</h2>
    <div class="table-wrap card" style="padding:0"><table><thead><tr><th>Stage</th><th>Message</th><th class="num">Sent</th><th class="num">Replies</th><th class="num">Reply rate</th></tr></thead>
      <tbody>${s.top_messages.map((m) => `<tr><td>${esc(stageLabel(m.stage))}${m.key ? '' : ' D' + m.day}</td><td>${esc(m.preview)}...</td><td class="num">${m.sent}</td><td class="num">${m.replies}</td><td class="num">${m.reply_rate_pct ?? '-'}%</td></tr>`).join('') || '<tr><td colspan="5" class="empty">Send a few messages and this fills in.</td></tr>'}</tbody></table></div>
    <p class="muted">Repeat / referral sales in the last 30 days: <b>${s.repeat_sales_30d}</b> (customers whose source mentions referral or repeat).</p>`;
}

// ---------------- IMPORT ----------------
async function viewImport() {
  view().innerHTML = `<h1>Import</h1>
    <div class="grid two">
      <div class="card"><h2>Customers</h2>
        <p class="muted">From DealerSocket: run a report or export of your customers/leads to Excel or CSV, then upload it here or paste the rows (including the header row).
          Columns are matched automatically: name, cell phone, email, stock #, sales step, lead source, sold date, opt-in / do-not-call flags.</p>
        <p class="muted"><b>Consent only comes from an opt-in column</b> (e.g. "OK to Text"). Without one, you'll get a "call and ask" task before anything is texted.</p>
        <label>Stage for rows without one</label><select id="i_stage">${stageOptions('new_lead')}</select>
        <label>File</label><input type="file" id="i_file" accept=".csv,.txt,.tsv">
        <label>...or paste</label><textarea id="i_csv" rows="8" placeholder="First Name,Last Name,Cell Phone,Email,Stock Number,OK to Text"></textarea>
        <div class="row" style="margin-top:10px"><button class="btn" id="i_preview">Preview</button><button class="btn primary" id="i_go">Import</button></div>
        <div id="i_out" style="margin-top:12px"></div></div>
      <div class="card"><h2>Inventory</h2>
        <p class="muted">Upload or paste your inventory list (stock #, year, make, model, trim, color, miles, VIN, status) so messages can name the vehicle.</p>
        <label>File</label><input type="file" id="v_file" accept=".csv,.txt,.tsv">
        <label>...or paste</label><textarea id="v_csv" rows="8" placeholder="Stock,Year,Make,Model,Trim,Miles"></textarea>
        <div class="row" style="margin-top:10px"><button class="btn primary" id="v_go">Import inventory</button></div><div id="v_out" style="margin-top:12px"></div></div>
    </div>`;
  const readFile = (inp, ta) => inp.onchange = () => { const f = inp.files[0]; if (f) f.text().then((t) => (ta.value = t)); };
  readFile($('#i_file'), $('#i_csv')); readFile($('#v_file'), $('#v_csv'));
  $('#i_preview').onclick = async () => {
    try {
      const r = await api('/import/customers', { method: 'POST', body: { csv: $('#i_csv').value, stage: $('#i_stage').value, preview: true } });
      $('#i_out').innerHTML = `<p><b>${r.total}</b> customers found${r.skipped ? `, ${r.skipped} rows skipped (no phone or email)` : ''}.</p>
        <p class="muted">Columns used: ${Object.entries(r.mapped).map(([k, v]) => `${esc(v)} &rarr; ${k.replace('_', ' ')}`).join(', ') || 'none recognised'}</p>
        <div class="table-wrap"><table><tr><th>Name</th><th>Phone</th><th>Email</th><th>Stock</th><th>Stage</th><th>Consent</th></tr>
        ${r.customers.map((c) => `<tr><td>${esc(c.first_name + ' ' + c.last_name)}</td><td>${esc(c.phone)}</td><td>${esc(c.email)}</td><td>${esc(c.stock_numbers)}</td><td>${esc(stageLabel(c.stage))}</td><td>${c.consent ? esc(c.consent) : '-'}</td></tr>`).join('')}</table></div>`;
    } catch (e) { fail(e); }
  };
  $('#i_go').onclick = async () => {
    try {
      const r = await api('/import/customers', { method: 'POST', body: { csv: $('#i_csv').value, stage: $('#i_stage').value } });
      await api('/run-now', { method: 'POST' }); await loadStatus();
      $('#i_out').innerHTML = `<p class="ok"><b>${r.created}</b> added, <b>${r.updated}</b> updated${r.skipped ? `, ${r.skipped} skipped (no phone/email)` : ''}. <a href="#" data-goto="today">See today's list</a></p>`;
    } catch (e) { fail(e); }
  };
  $('#v_go').onclick = async () => {
    try { const r = await api('/import/inventory', { method: 'POST', body: { csv: $('#v_csv').value } }); $('#v_out').innerHTML = `<p class="ok">${r.imported} vehicles imported.${r.match_texts_drafted ? ` ${r.match_texts_drafted} "just came in" texts drafted for matching customers.` : ''}</p>`; } catch (e) { fail(e); }
  };
}

// ---------------- SETTINGS ----------------
async function viewSettings() {
  const s = await api('/settings');
  const st = state.status;
  const field = (k, label, ph = '', type = 'text') => `<label>${label}</label><input data-k="${k}" type="${type}" value="${esc(s[k])}" placeholder="${esc(ph)}">`;
  const hours = (k, min = 0, max = 24) => `<select data-k="${k}">${[...Array(max - min + 1)].map((_, i) => { const h = i + min; return `<option value="${h}" ${String(h) === s[k] ? 'selected' : ''}>${h === 0 || h === 24 ? '12 am' : h < 12 ? h + ' am' : h === 12 ? '12 pm' : h - 12 + ' pm'}</option>`; }).join('')}</select>`;
  const desktopCfg = JSON.stringify({ mcpServers: { 'dealer-autopilot': { command: 'node', args: ['--disable-warning=ExperimentalWarning', '/FULL/PATH/TO/dealer-autopilot/src/mcp-stdio.js'] } } }, null, 2);
  view().innerHTML = `<h1>Settings</h1>
    <div class="grid two">
      <div class="card"><h2>You</h2>
        ${field('salesperson', 'Your name (signs every message)', 'Nolan')}
        ${field('dealership', 'Dealership name')}
        ${field('dealer_address', 'Dealership address (required in emails, used in appointment texts)', '123 Main St, City, ST')}
        ${field('dealer_phone', 'Your phone number for messages')}
        ${field('review_link', 'Review link (Google / DealerRater)', 'https://g.page/r/...')}
        <label>Dealership CRM</label><input data-k="crm" value="${esc(s.crm)}">
      </div>
      <div class="card"><h2>Hours &amp; texting</h2>
        <label>Time zone</label><input data-k="timezone" value="${esc(s.timezone)}" placeholder="America/New_York">
        <div class="grid two"><div><label>Your hours start</label>${hours('work_start_hour')}</div><div><label>Your hours end</label>${hours('work_end_hour')}</div></div>
        <div class="grid two"><div><label>Texts no earlier than</label>${hours('text_start_hour', 8, 21)}</div><div><label>Texts no later than</label>${hours('text_end_hour', 8, 21)}</div></div>
        <p class="muted" style="font-size:12px">The law allows 8 am to 9 pm. You can narrow it, not widen it.</p>
        <label>Send texts from</label><select data-k="text_mode"><option value="phone" ${s.text_mode === 'phone' ? 'selected' : ''}>My own phone (one tap per text)</option><option value="twilio" ${s.text_mode === 'twilio' ? 'selected' : ''}>Registered business number (Twilio + A2P 10DLC)</option></select>
        <label>Calls to aim for each day</label><input data-k="daily_call_target" type="number" value="${esc(s.daily_call_target)}">
        <label class="switch" style="margin-top:10px"><input type="checkbox" data-k="appt_reminders" ${s.appt_reminders === '1' ? 'checked' : ''}> Appointment reminders (day before + 2 hours before)</label>
        <label class="switch"><input type="checkbox" data-k="automation_enabled" ${s.automation_enabled === '1' ? 'checked' : ''}> Automation on (only approved Sold + appointment templates)</label>
      </div>
    </div>
    <div class="row" style="margin:14px 0"><button class="btn primary" id="saveSettings">Save settings</button></div>
    <div class="card" style="margin-bottom:14px"><h2>Your email</h2>
      <p class="muted">Follow-up emails go out from your own email address, and replies land in your inbox. Every few minutes the app checks your inbox:
        a customer's reply stops their follow-ups and puts them on your call list, and "unsubscribe" stops emails to them.</p>
      <p>${st.email_live && st.email_verified ? `<span class="ok">Connected: <b>${esc(st.email_account)}</b></span>` : st.email_live ? `<span class="flag">Saved for ${esc(st.email_account)} but not confirmed yet. Click <b>Connect &amp; send test</b>.</span>` : '<span class="flag">Not connected yet. Emails are only practice until you connect.</span>'}
        ${st.email_last_check ? `<br><span class="muted" style="font-size:13px">Inbox last checked ${fmtDate(st.email_last_check)}${st.email_last_error ? ` &middot; <span class="flag">${esc(st.email_last_error)}</span>` : ''}</span>` : ''}</p>
      <div class="grid two">
        <div><label>Email provider</label><select id="em_provider">${Object.entries(st.email_providers).map(([k, v]) => `<option value="${k}" ${k === (s.email_provider || 'gmail') ? 'selected' : ''}>${esc(v)}</option>`).join('')}</select></div>
        <div><label>Your email address</label><input id="em_address" type="email" value="${esc(s.email_address)}" placeholder="you@gmail.com"></div>
        <div><label>App password ${s.email_password_set ? '(saved; leave blank to keep it)' : ''}</label><input id="em_pass" type="password" autocomplete="new-password" placeholder="${s.email_password_set ? '••••••••••••••••' : '16 letters from Google'}"></div>
        <div><label>Name people see (optional)</label><input id="em_name" value="${esc(s.email_from_name)}" placeholder="${esc([s.salesperson, s.dealership].filter(Boolean).join(' - ') || 'Your name - Dealership')}"></div>
      </div>
      <details style="margin-top:10px"><summary>How to get a Gmail app password (2 minutes)</summary>
        <ol class="muted" style="margin:8px 0 0;padding-left:20px;line-height:1.7">
          <li>Go to <b>myaccount.google.com</b> and open <b>Security</b>.</li>
          <li>Turn on <b>2-Step Verification</b> if it isn't on already.</li>
          <li>Search the account settings for <b>App passwords</b>, create one named "Dealer Autopilot", and copy the 16 letters.</li>
          <li>Paste them above and click <b>Connect &amp; send test</b>. Your normal Gmail password won't work here.</li>
        </ol>
        <p class="muted" style="font-size:13px">The app password is stored only in this app on your computer. Remove it anytime with Disconnect, or delete it in your Google account.</p></details>
      <div class="row" style="margin-top:12px"><button class="btn primary" id="em_save">Connect &amp; send test</button>
        ${st.email_live ? '<button class="btn" id="em_check">Check inbox now</button><button class="btn danger" id="em_disc">Disconnect</button>' : ''}</div>
      <p id="em_out" style="margin-bottom:0"></p>
    </div>
    <div class="grid two">
      <div class="card"><h2>Use with Claude (MCP)</h2>
        <p class="muted">Run everything by talking to Claude: "what's on my list", "book Mike for Saturday at 11", "import this list".</p>
        <h3>claude.ai / Claude app</h3><p class="muted">Settings &rarr; Connectors &rarr; Add custom connector &rarr; paste this URL (the app must be online at your public address). Keep it private: it works like a password.</p>
        <code class="url">${esc(st.mcp_url)}</code>
        <h3 style="margin-top:12px">Claude Desktop / Claude Code (same computer)</h3><p class="muted">Add to Claude Desktop's config (Settings &rarr; Developer &rarr; Edit config), or run <code>claude mcp add dealer-autopilot -- node /FULL/PATH/src/mcp-stdio.js</code>:</p>
        <code class="url" style="white-space:pre">${esc(desktopCfg)}</code></div>
      <div class="card"><h2>Calendar on your phone</h2>
        <p class="muted">Subscribe to this link and your appointments show up in your phone's calendar (updates every ~15 minutes). Google Calendar: Other calendars &rarr; + &rarr; From URL. iPhone: Settings &rarr; Calendar &rarr; Accounts &rarr; Add Account &rarr; Other &rarr; Add Subscribed Calendar.</p>
        <code class="url">${esc(st.calendar_url)}</code>
        <h2 style="margin-top:16px">Status</h2>
        <p>Email: ${st.email_live ? '<span class="ok">connected</span>' : '<span class="flag">simulation (add SMTP to .env)</span>'}<br>
        Texts: ${s.text_mode === 'phone' ? '<span class="ok">your phone</span>' : st.twilio_live ? '<span class="ok">Twilio connected</span>' : '<span class="flag">Twilio not set up</span>'}<br>
        TARS: ${st.tars_ready ? '<span class="ok">ready</span>' : '<span class="flag">add ANTHROPIC_API_KEY to .env</span>'}</p></div>
    </div>`;
  $('#em_save').onclick = async () => {
    const out = $('#em_out'); out.innerHTML = 'Connecting...';
    try {
      await api('/settings', { method: 'PUT', body: { email_provider: $('#em_provider').value, email_address: $('#em_address').value, email_app_password: $('#em_pass').value, email_from_name: $('#em_name').value } });
      const r = await api('/email/test', { method: 'POST' });
      out.innerHTML = `<span class="ok">Connected. A test email went to ${esc(r.sent_to)}.${r.inbox === 'ok' ? ' Inbox checking is on.' : r.inbox !== 'not checked' ? ' Inbox check failed: ' + esc(r.inbox) : ''}</span>`;
      await loadStatus(); setTimeout(() => viewSettings(), 2500);
    } catch (e) { out.innerHTML = `<span class="flag">${esc(e.message)}</span>`; }
  };
  $('#em_check') && ($('#em_check').onclick = async () => {
    try { const r = await api('/email/check', { method: 'POST' }); await loadStatus(); toast(r.replies || r.unsubscribes ? `${r.replies} repl${r.replies === 1 ? 'y' : 'ies'}, ${r.unsubscribes} unsubscribe(s) found` : 'No new customer replies'); viewSettings(); } catch (e) { fail(e); }
  });
  $('#em_disc') && ($('#em_disc').onclick = async () => { await api('/email/disconnect', { method: 'POST' }); await loadStatus(); toast('Email disconnected'); viewSettings(); });
  $('#saveSettings').onclick = async () => {
    const body = {};
    $$('[data-k]').forEach((el) => { body[el.dataset.k] = el.type === 'checkbox' ? (el.checked ? '1' : '0') : el.value; });
    try { await api('/settings', { method: 'PUT', body }); await loadStatus(); toast('Saved'); viewSettings(); } catch (e) { fail(e); }
  };
}

// ---------------- modal ----------------
function modal(html) { $('#modalCard').innerHTML = html; $('#modal').classList.remove('hidden'); }
function closeModal() { $('#modal').classList.add('hidden'); }
$('#modal').addEventListener('click', (e) => { if (e.target.id === 'modal') closeModal(); });

// ---------------- TARS ----------------
$('#tarsToggle').onclick = () => { $('#tars').classList.toggle('hidden'); $('#tarsInput').focus(); };
$('#tarsInput').addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); $('#tarsForm').requestSubmit(); } });
$('#tarsForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const msg = $('#tarsInput').value.trim(); if (!msg) return;
  $('#tarsInput').value = '';
  const log = $('#tarsLog');
  log.insertAdjacentHTML('beforeend', `<div class="msg user">${esc(msg)}</div>`);
  const thinking = document.createElement('div'); thinking.className = 'msg bot muted'; thinking.textContent = 'Thinking...'; log.append(thinking);
  log.scrollTop = log.scrollHeight;
  try {
    const r = await api('/tars', { method: 'POST', body: { message: msg, history: state.tarsHistory } });
    thinking.className = 'msg bot';
    thinking.innerHTML = esc(r.reply).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>') + (r.actions.length ? `<div class="actions">${r.actions.map(esc).join('<br>')}</div>` : '');
    state.tarsHistory.push({ role: 'user', content: msg }, { role: 'assistant', content: r.reply });
    if (r.actions.length) { await loadStatus(); VIEWS[state.view]().catch(() => {}); }
  } catch (err) { thinking.textContent = err.message; }
  log.scrollTop = log.scrollHeight;
});

const VIEWS = { today: viewToday, customers: viewCustomers, calendar: viewCalendar, stock: () => viewStock(), templates: viewTemplates, grow: viewGrow, scoreboard: viewScoreboard, import: viewImport, settings: viewSettings };
boot();
