// Weekly scoreboard: the 4 numbers from the brief, plus which message gets the most replies.
const store = require('./db');

const { db } = store;

function weekStart(d, tz) {
  // Monday 00:00 in the dealership time zone
  const { date } = store.localParts(d, tz);
  const local = new Date(date + 'T00:00:00Z');
  const dow = (local.getUTCDay() + 6) % 7;
  local.setUTCDate(local.getUTCDate() - dow);
  return require('./appointments').localToIso(local.toISOString().slice(0, 10), '00:00', tz);
}

const pct = (a, b) => (b ? Math.round((a / b) * 100) : null);
function median(arr) {
  if (!arr.length) return null;
  const s = [...arr].sort((x, y) => x - y);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}

function weekStats(from, to) {
  const leads = db.prepare("SELECT * FROM customers WHERE lead_at >= ? AND lead_at < ?").all(from, to);
  const internet = leads.filter((c) => c.source !== 'Inbound text');
  const responseMins = internet.filter((c) => c.first_contact_at).map((c) => (new Date(c.first_contact_at) - new Date(c.lead_at)) / 60000).filter((m) => m >= 0);
  const appts = db.prepare("SELECT * FROM appointments WHERE created_at >= ? AND created_at < ?").all(from, to);
  const held = db.prepare("SELECT status FROM appointments WHERE starts_at >= ? AND starts_at < ? AND status IN ('showed','no_show')").all(from, to);
  const shows = held.filter((a) => a.status === 'showed').length;
  const sold = db.prepare("SELECT COUNT(*) AS n FROM customers WHERE sold_date >= ? AND sold_date < ?").get(from.slice(0, 10), to.slice(0, 10)).n;
  return {
    from, to,
    leads: leads.length,
    median_response_min: median(responseMins) === null ? null : Math.round(median(responseMins) * 10) / 10,
    under_5_min_pct: pct(responseMins.filter((m) => m <= 5).length, internet.length),
    not_contacted: internet.filter((c) => !c.first_contact_at).length,
    appointments_set: appts.length,
    appointment_rate_pct: pct(appts.length, leads.length),
    shows, no_shows: held.length - shows,
    show_rate_pct: pct(shows, held.length),
    sold,
    close_rate_pct: pct(sold, shows),
  };
}

/** Which templates get replies: a reply within 3 days of a message counts for that message. */
function templateReplies(from) {
  const rows = db.prepare(`SELECT m.step_id, s.stage, s.day, s.channel, s.key, substr(s.body, 1, 90) AS preview, COUNT(*) AS sent,
      SUM(CASE WHEN EXISTS (SELECT 1 FROM messages r WHERE r.customer_id = m.customer_id AND r.direction = 'in' AND r.created_at > m.created_at
        AND r.created_at <= datetime(m.created_at, '+3 days')) THEN 1 ELSE 0 END) AS replies
    FROM messages m JOIN steps s ON s.id = m.step_id
    WHERE m.direction = 'out' AND m.status IN ('sent','simulated') AND m.created_at >= ?
    GROUP BY m.step_id ORDER BY (1.0 * replies / COUNT(*)) DESC, sent DESC LIMIT 15`).all(from);
  return rows.map((r) => ({ ...r, reply_rate_pct: pct(r.replies, r.sent) }));
}

function scoreboard(weeks = 6) {
  const tz = store.getSettings().timezone;
  const start = new Date(weekStart(new Date(), tz));
  const out = [];
  for (let i = 0; i < weeks; i++) {
    const from = new Date(start.getTime() - i * 7 * 86400000);
    const to = new Date(from.getTime() + 7 * 86400000);
    out.push(weekStats(from.toISOString(), to.toISOString()));
  }
  const repeatSince = new Date(Date.now() - 30 * 86400000).toISOString().slice(0, 10);
  return {
    weeks: out,
    top_messages: templateReplies(new Date(Date.now() - 56 * 86400000).toISOString()),
    repeat_sales_30d: db.prepare(`SELECT COUNT(*) AS n FROM customers WHERE sold_date >= ? AND (source LIKE '%referral%' OR source LIKE '%repeat%' OR prev_stage = 'lost')`).get(repeatSince).n,
  };
}

module.exports = { scoreboard };
