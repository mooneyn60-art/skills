// Your email account: sends your follow-up emails and watches your inbox for customer replies.
// Connect it on the Setup screen (address + app password), or with SMTP_* settings in .env.
// The password is kept only in this app's database on your own computer.
const nodemailer = require('nodemailer');
const config = require('./config');
const store = require('./db');

const PROVIDERS = {
  gmail: { label: 'Gmail', smtp: { host: 'smtp.gmail.com', port: 465, secure: true }, imap: { host: 'imap.gmail.com', port: 993 } },
  outlook: { label: 'Outlook / Hotmail / Microsoft 365', smtp: { host: 'smtp.office365.com', port: 587, secure: false }, imap: { host: 'outlook.office365.com', port: 993 } },
  yahoo: { label: 'Yahoo', smtp: { host: 'smtp.mail.yahoo.com', port: 465, secure: true }, imap: { host: 'imap.mail.yahoo.com', port: 993 } },
  icloud: { label: 'iCloud', smtp: { host: 'smtp.mail.me.com', port: 587, secure: false }, imap: { host: 'imap.mail.me.com', port: 993 } },
};

/** The connected account, or null. Setup screen wins over .env. */
function account() {
  const s = store.getSettings();
  if (s.email_address && s.email_app_password) {
    const p = PROVIDERS[s.email_provider] || PROVIDERS.gmail;
    return { user: s.email_address, pass: s.email_app_password, smtp: p.smtp, imap: p.imap, fromName: s.email_from_name || '', source: 'setup' };
  }
  if (config.smtp.host && config.smtp.user && config.smtp.pass) {
    return {
      user: config.smtp.user, pass: config.smtp.pass, fromName: config.smtp.fromName, source: 'env',
      smtp: { host: config.smtp.host, port: config.smtp.port, secure: config.smtp.port === 465 },
      imap: process.env.IMAP_HOST ? { host: process.env.IMAP_HOST, port: Number(process.env.IMAP_PORT || 993) } : null,
    };
  }
  return null;
}
const isLive = () => !!account();

let cached = { key: '', t: null };
function mailer() {
  const a = account();
  if (!a) return null;
  const key = [a.user, a.pass, a.smtp.host].join('|');
  if (cached.key !== key) {
    cached = { key, t: nodemailer.createTransport({ host: a.smtp.host, port: a.smtp.port, secure: a.smtp.secure, auth: { user: a.user, pass: a.pass } }) };
  }
  return cached.t;
}
function fromHeader() {
  const a = account();
  const s = store.getSettings();
  const name = (a.fromName || [s.salesperson, s.dealership].filter(Boolean).join(' - ') || a.user).replace(/"/g, '');
  return `"${name}" <${a.user}>`;
}

/** Send one email. Returns {status: 'sent'} or {status: 'simulated'} when no account is connected. */
async function send({ to, subject, text, html, headers }) {
  const t = mailer();
  if (!t) return { status: 'simulated' };
  await t.sendMail({ from: fromHeader(), to, subject, text, html, headers });
  return { status: 'sent' };
}

/** Send yourself a test email, and check the inbox login works. */
async function test() {
  const a = account();
  if (!a) throw new Error('Connect your email first.');
  try {
    await mailer().verify();
  } catch (e) {
    store.setInternal({ email_verified: '' });
    throw new Error(friendly(e));
  }
  store.setInternal({ email_verified: '1' });
  await send({ to: a.user, subject: 'Dealer Autopilot is connected', text: 'Your email is connected. Follow-up emails will go out from this address, and customer replies will show up on your call list.' });
  let inbox = 'not checked';
  if (a.imap) {
    try { await withInbox(async () => {}); inbox = 'ok'; } catch (e) { inbox = friendly(e); }
  }
  return { sent_to: a.user, inbox };
}

function friendly(e) {
  const m = String(e && (e.response || e.responseText || e.message) || e);
  if (/535|auth|invalid credentials|username and password|AUTHENTICATIONFAILED/i.test(m)) {
    return 'Your email or app password was not accepted. For Gmail, use a 16-letter App Password (not your normal password), with 2-Step Verification turned on.';
  }
  if (/ENOTFOUND|ECONNREFUSED|ETIMEDOUT|network/i.test(m)) return 'Could not reach the email server. Check your internet connection.';
  return m.slice(0, 200);
}

// ---------------- reply watching ----------------
async function withInbox(fn) {
  const a = account();
  if (!a || !a.imap) return null;
  const { ImapFlow } = require('imapflow');
  const client = new ImapFlow({ host: a.imap.host, port: a.imap.port, secure: true, auth: { user: a.user, pass: a.pass }, logger: false });
  await client.connect();
  const lock = await client.getMailboxLock('INBOX');
  try { return await fn(client); } finally { lock.release(); await client.logout().catch(() => {}); }
}

const UNSUB = /^\s*(unsubscribe|stop|remove me|take me off|no more emails?)\b/i;
let checking = false;

/**
 * Look for new emails from customers. A reply stops their follow-ups and puts them on the call list;
 * "unsubscribe" stops emails to them. Returns { checked, replies, unsubscribes }.
 */
async function checkReplies() {
  if (checking || !account()?.imap) return { checked: 0 };
  checking = true;
  const queue = require('./queue');
  const { simpleParser } = require('mailparser');
  const s = store.getSettings();
  let checked = 0, replies = 0, unsubscribes = 0;
  try {
    await withInbox(async (client) => {
      const validity = String(client.mailbox.uidValidity);
      let lastUid = s.email_uid_validity === validity ? Number(s.email_last_uid || 0) : 0;
      if (!lastUid) {
        // First run: start from now, so old mail isn't treated as new replies.
        lastUid = Math.max(0, Number(client.mailbox.uidNext || 1) - 1);
        store.setInternal({ email_uid_validity: validity, email_last_uid: String(lastUid) });
        return;
      }
      const uids = (await client.search({ uid: `${lastUid + 1}:*` }, { uid: true })) || [];
      const fresh = uids.filter((u) => u > lastUid).slice(0, 200);
      let maxUid = lastUid;
      for (const uid of fresh) {
        maxUid = Math.max(maxUid, uid);
        const msg = await client.fetchOne(String(uid), { envelope: true, source: true }, { uid: true });
        checked++;
        const from = msg?.envelope?.from?.[0]?.address?.toLowerCase();
        if (!from || from === account().user.toLowerCase()) continue;
        const c = store.db.prepare('SELECT * FROM customers WHERE lower(email) = ?').get(from);
        if (!c) continue;
        let text = '';
        try { text = (await simpleParser(msg.source)).text || ''; } catch { /* keep subject only */ }
        // Keep just what they wrote, not the quoted thread below it.
        const mine = text.split(/\n\s*(On .+wrote:|-{2,}\s*Original Message|From: )/i)[0].trim();
        const subject = msg.envelope.subject || '';
        if (UNSUB.test(mine) || /unsubscribe/i.test(subject)) {
          store.db.prepare('UPDATE customers SET email_opt_out = 1 WHERE id = ?').run(c.id);
          store.db.prepare("UPDATE tasks SET status = 'skipped', done_at = ? WHERE customer_id = ? AND kind = 'email' AND status = 'pending'").run(store.nowIso(), c.id);
          store.logMessage({ customer_id: c.id, direction: 'in', channel: 'email', subject, body: mine.slice(0, 1000) || 'Asked to unsubscribe', status: 'received' });
          unsubscribes++;
        } else {
          queue.markReplied(c.id, (mine || subject).slice(0, 1000), 'email');
          replies++;
        }
      }
      store.setInternal({ email_last_uid: String(maxUid) });
    });
    store.setInternal({ email_last_check: store.nowIso(), email_last_error: '' });
  } catch (e) {
    store.setInternal({ email_last_check: store.nowIso(), email_last_error: friendly(e) });
  } finally {
    checking = false;
  }
  return { checked, replies, unsubscribes };
}

module.exports = { PROVIDERS, account, isLive, send, test, checkReplies, friendly };
