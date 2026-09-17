const state = { customers: [], appointments: [] };

async function api(path, opts) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.status === 204 ? null : res.json();
}

// ---------- tabs ----------
document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".tab-panel").forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(`tab-${btn.dataset.tab}`).classList.add("active");
    if (btn.dataset.tab === "agenda") loadAgenda();
    if (btn.dataset.tab === "specs") loadSpecs();
  });
});

// ---------- summary / alert bar ----------
async function loadSummary() {
  const s = await api("/api/summary");
  const bar = document.getElementById("alert-bar");
  const pills = [];
  if (s.overdue_followups) pills.push(`<span class="alert-pill overdue">${s.overdue_followups} overdue follow-up${s.overdue_followups > 1 ? "s" : ""}</span>`);
  if (s.today_followups) pills.push(`<span class="alert-pill today">${s.today_followups} due today</span>`);
  if (s.today_appointments) pills.push(`<span class="alert-pill today">${s.today_appointments} appt${s.today_appointments > 1 ? "s" : ""} today</span>`);
  if (s.unconfirmed_soon) pills.push(`<span class="alert-pill unconfirmed">${s.unconfirmed_soon} unconfirmed soon</span>`);
  if (!pills.length) pills.push(`<span class="alert-pill ok">All caught up</span>`);
  bar.innerHTML = pills.join("");
}

// ---------- customers ----------
function statusBadge(status) {
  if (!status) return "";
  return `<span class="badge ${status}">${status}</span>`;
}

function consentDot(value) {
  const v = (value || "unknown").toLowerCase();
  const cls = v === "yes" ? "yes" : v === "no" ? "no" : "unknown";
  return `<span class="dot ${cls}" title="${v}"></span>`;
}

function renderCustomerRows() {
  const q = document.getElementById("search").value.trim().toLowerCase();
  const statusFilter = document.getElementById("filter-status").value;
  const tbody = document.getElementById("customer-rows");
  const rows = state.customers.filter((c) => {
    if (statusFilter && c.status !== statusFilter) return false;
    if (!q) return true;
    const hay = [c.name, c.phone, c.email, c.vehicle_interest, c.tags].join(" ").toLowerCase();
    return hay.includes(q);
  });
  if (!rows.length) {
    tbody.innerHTML = `<tr><td colspan="7" class="empty-state">No customers match.</td></tr>`;
    return;
  }
  tbody.innerHTML = rows
    .map(
      (c) => `
    <tr data-slug="${c.slug}">
      <td>${c.name || c.slug}</td>
      <td>${c.vehicle_interest || ""}</td>
      <td>${statusBadge(c.status)}</td>
      <td>${c.stage || ""}</td>
      <td class="followup ${c.urgency}">${c.next_followup || ""}</td>
      <td>${c.next_followup_channel || ""}</td>
      <td>${consentDot(c.consent_call)}${consentDot(c.consent_text)}${consentDot(c.consent_email)}</td>
    </tr>`
    )
    .join("");
  tbody.querySelectorAll("tr").forEach((tr) => {
    tr.addEventListener("click", () => openCustomer(tr.dataset.slug));
  });
}

async function loadCustomers() {
  state.customers = await api("/api/customers");
  renderCustomerRows();
  document.getElementById("customer-names").innerHTML = state.customers
    .map((c) => `<option value="${c.name}">`)
    .join("");
}

document.getElementById("search").addEventListener("input", renderCustomerRows);
document.getElementById("filter-status").addEventListener("change", renderCustomerRows);

function openModal(id) { document.getElementById(id).classList.remove("hidden"); }
function closeModal(id) { document.getElementById(id).classList.add("hidden"); }
document.querySelectorAll("[data-close]").forEach((btn) =>
  btn.addEventListener("click", (e) => closeModal(e.target.closest(".modal-overlay").id))
);

async function openCustomer(slug) {
  const c = await api(`/api/customers/${slug}`);
  const body = document.getElementById("modal-customer-body");
  body.innerHTML = `
    <h2>${c.name || slug}</h2>
    <div class="detail-section field-row">
      <div><label>Status<select id="f-status">
        ${["hot", "warm", "cold", "sold", "lost"].map((s) => `<option value="${s}" ${c.status === s ? "selected" : ""}>${s}</option>`).join("")}
      </select></label></div>
      <div><label>Stage<select id="f-stage">
        ${["new", "contacted", "test-drive", "negotiating", "financing", "closed"].map((s) => `<option value="${s}" ${c.stage === s ? "selected" : ""}>${s}</option>`).join("")}
      </select></label></div>
      <div><label>Next follow-up<input id="f-followup" type="date" value="${c.next_followup || ""}"></label></div>
      <div><label>Channel<select id="f-channel">
        ${["", "call", "email", "text"].map((s) => `<option value="${s}" ${c.next_followup_channel === s ? "selected" : ""}>${s || "(unset)"}</option>`).join("")}
      </select></label></div>
    </div>
    <div class="detail-section field-row">
      <div>Phone: ${c.phone || "—"}</div>
      <div>Email: ${c.email || "—"}</div>
      <div>Vehicle: ${c.vehicle_interest || "—"}</div>
    </div>
    <div class="detail-section">
      <h3>Contact consent</h3>
      <div class="field-row">
        ${["call", "text", "email"]
          .map(
            (ch) => `<div><label>${ch}<select id="f-consent-${ch}">
              ${["unknown", "yes", "no"].map((v) => `<option value="${v}" ${c["consent_" + ch] === v ? "selected" : ""}>${v}</option>`).join("")}
            </select></label></div>`
          )
          .join("")}
      </div>
    </div>
    <div class="detail-section">
      <h3>Log a contact now</h3>
      <div class="field-row">
        <button class="btn-secondary" data-log="call">Called</button>
        <button class="btn-secondary" data-log="text">Texted</button>
        <button class="btn-secondary" data-log="email">Emailed</button>
      </div>
    </div>
    <div class="detail-section">
      <h3>Add a note</h3>
      <textarea id="f-note" rows="3" placeholder="What happened / what's next..."></textarea>
    </div>
    <div class="detail-section">
      <button id="btn-save-customer" class="btn-primary">Save changes</button>
      <button id="btn-delete-customer" class="btn-secondary" style="float:right;color:#e0322c;">Delete customer</button>
    </div>
    <div class="detail-section">
      <h3>History</h3>
      <pre style="white-space:pre-wrap;font-size:13px;">${escapeHtml(c.notes_body || "")}</pre>
    </div>
  `;

  let pendingLogChannel = null;
  body.querySelectorAll("[data-log]").forEach((btn) =>
    btn.addEventListener("click", () => {
      pendingLogChannel = btn.dataset.log;
      body.querySelectorAll("[data-log]").forEach((b) => (b.style.outline = ""));
      btn.style.outline = "2px solid var(--accent)";
    })
  );

  document.getElementById("btn-save-customer").addEventListener("click", async () => {
    const payload = {
      status: document.getElementById("f-status").value,
      stage: document.getElementById("f-stage").value,
      next_followup: document.getElementById("f-followup").value,
      next_followup_channel: document.getElementById("f-channel").value,
      consent_call: document.getElementById("f-consent-call").value,
      consent_text: document.getElementById("f-consent-text").value,
      consent_email: document.getElementById("f-consent-email").value,
      note: document.getElementById("f-note").value,
    };
    if (pendingLogChannel) payload.log_contact_channel = pendingLogChannel;
    await api(`/api/customers/${slug}`, { method: "POST", body: JSON.stringify(payload) });
    closeModal("modal-customer");
    await Promise.all([loadCustomers(), loadSummary()]);
  });

  document.getElementById("btn-delete-customer").addEventListener("click", async () => {
    if (!confirm(`Delete ${c.name || slug}? This can't be undone.`)) return;
    await api(`/api/customers/${slug}`, { method: "DELETE" });
    closeModal("modal-customer");
    await Promise.all([loadCustomers(), loadSummary()]);
  });

  openModal("modal-customer");
}

function escapeHtml(s) {
  return s.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
}

document.getElementById("btn-add-customer").addEventListener("click", () => openModal("modal-add-customer"));
document.getElementById("form-add-customer").addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target).entries());
  await api("/api/customers", { method: "POST", body: JSON.stringify(data) });
  e.target.reset();
  closeModal("modal-add-customer");
  await Promise.all([loadCustomers(), loadSummary()]);
});

// ---------- agenda ----------
async function loadAgenda() {
  const days = parseInt(document.getElementById("agenda-days").value, 10);
  const [customers, appts] = await Promise.all([api("/api/customers"), api("/api/appointments")]);
  state.appointments = appts;
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const items = [];
  customers.forEach((c) => {
    if (!c.next_followup) return;
    if (["sold", "lost"].includes(c.status) && !c.next_followup) return;
    items.push({ kind: "followup", date: c.next_followup, who: c.name || c.slug, detail: c.next_followup_channel || "(channel unset)", slug: c.slug });
  });
  appts.forEach((a) => {
    if (!a.date) return;
    items.push({ kind: "appointment", date: a.date, who: a.customer, detail: `${a.type || "appointment"}${a.time ? " @ " + a.time : ""}`, confirmed: (a.confirmed || "").toLowerCase() === "true", slug: a.slug });
  });

  const overdue = items.filter((i) => new Date(i.date) < today);
  const overdueEl = document.getElementById("agenda-overdue");
  overdueEl.innerHTML = overdue.length
    ? `<div class="day-block"><h4 style="color:var(--overdue)">Overdue</h4>${overdue.map(renderAgendaItem).join("")}</div>`
    : "";

  const listEl = document.getElementById("agenda-days-list");
  let html = "";
  for (let i = 0; i < days; i++) {
    const d = new Date(today);
    d.setDate(d.getDate() + i);
    const iso = d.toISOString().slice(0, 10);
    const dayItems = items.filter((it) => it.date === iso);
    if (!dayItems.length) continue;
    const label = i === 0 ? "Today" : d.toLocaleDateString(undefined, { weekday: "long", month: "short", day: "numeric" });
    html += `<div class="day-block"><h4>${label}</h4>${dayItems.map(renderAgendaItem).join("")}</div>`;
  }
  listEl.innerHTML = html || `<div class="empty-state">Nothing scheduled in this range.</div>`;

  attachAgendaHandlers();
}

function renderAgendaItem(it) {
  if (it.kind === "appointment") {
    return `<div class="agenda-item">
      <span><span class="tag-appt">APPT</span>${it.who} — ${it.detail}${it.confirmed ? "" : '<span class="unconfirmed-flag">UNCONFIRMED</span>'}</span>
      ${it.confirmed ? "" : `<button class="btn-secondary" data-confirm="${it.slug}">Confirm</button>`}
    </div>`;
  }
  return `<div class="agenda-item" data-open-customer="${it.slug}">
    <span><span class="tag-followup">FOLLOW-UP</span>${it.who} — ${it.detail}</span>
  </div>`;
}

function attachAgendaHandlers() {
  document.querySelectorAll("[data-confirm]").forEach((btn) =>
    btn.addEventListener("click", async (e) => {
      e.stopPropagation();
      await api(`/api/appointments/${btn.dataset.confirm}`, { method: "POST", body: JSON.stringify({ confirmed: true }) });
      loadAgenda();
    })
  );
  document.querySelectorAll("[data-open-customer]").forEach((el) =>
    el.addEventListener("click", () => openCustomer(el.dataset.openCustomer))
  );
}

document.getElementById("agenda-days").addEventListener("change", loadAgenda);
document.getElementById("btn-add-appt").addEventListener("click", () => openModal("modal-add-appt"));
document.getElementById("form-add-appt").addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target).entries());
  await api("/api/appointments", { method: "POST", body: JSON.stringify(data) });
  e.target.reset();
  closeModal("modal-add-appt");
  loadAgenda();
});

// ---------- vehicle specs ----------
async function loadSpecs() {
  const specs = await api("/api/vehicle-specs");
  const el = document.getElementById("specs-list");
  if (!specs.length) {
    el.innerHTML = `<div class="empty-state">No vehicle specs filed yet. Send Claude a photo of a manual/spec sheet to add one.</div>`;
    return;
  }
  el.innerHTML = specs
    .map(
      (s) => `<div class="spec-card"><h4>${[s.year, s.make, s.model, s.trim].filter(Boolean).join(" ")}</h4><pre>${escapeHtml(s.body || "")}</pre></div>`
    )
    .join("");
}

// ---------- init ----------
async function refreshAll() {
  await Promise.all([loadCustomers(), loadSummary()]);
}
refreshAll();
setInterval(refreshAll, 60000);
