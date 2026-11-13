// Rendering templates and delivering messages.
// Texts: text_mode "phone" (default) = you send from your own phone with one tap (sms: link opens your Messages app).
//        text_mode "twilio" = sent by a registered Twilio number (requires A2P 10DLC registration).
// Emails: sent through your SMTP account (e.g. Gmail app password). Without SMTP settings they are SIMULATED.
const nodemailer = require('nodemailer');
const config = require('./config');
const store = require('./db');

let transporter = null;
function mailer() {
  if (!config.emailLive) return null;
  transporter ||= nodemailer.createTransport({
    host: config.smtp.host, port: config.smtp.port, secure: config.smtp.port === 465,
    auth: { user: config.smtp.user, pass: config.smtp.pass },
  });
  return transporter;
}

/** Fill {placeholders}. [[ ... ]] sections are dropped if any placeholder inside them is empty. */
function render(template, customer, extra = {}, settings = store.getSettings()) {
  const c = customer.interests ? customer : store.getCustomer(customer.id);
  const first = (c.interests || [])[0];
  const stock = first ? first.stock_number : '';
  const vehicle = (first && [first.year, first.make, first.model, first.trim].filter(Boolean).join(' ')) || c.vehicle_interest || '';
  const vars = {
    first_name: c.first_name || 'there',
    last_name: c.last_name || '',
    vehicle: vehicle || (stock ? `vehicle (stock #${stock})` : 'vehicle'),
    vehicle_raw: vehicle,
    stock,
    objection: c.objection || '',
    salesperson: settings.salesperson || '[your name]',
    dealership: settings.dealership || 'the dealership',
    dealer_phone: settings.dealer_phone || '',
    dealer_address: settings.dealer_address || '[dealership address]',
    review_link: settings.review_link || '[review link]',
    ...extra,
  };
  const fill = (s) => s.replace(/\{(\w+)\}/g, (m, k) => (k in vars ? vars[k] : m));
  let out = String(template || '').replace(/\[\[([\s\S]*?)\]\]/g, (m, inner) => {
    const keys = [...inner.matchAll(/\{(\w+)\}/g)].map((x) => x[1]);
    const empty = keys.some((k) => !(k === 'vehicle' ? vars.vehicle_raw : vars[k]));
    return empty ? '' : fill(inner);
  });
  return fill(out).replace(/[ \t]{2,}/g, ' ').replace(/ +([.,!?])/g, '$1').trim();
}

/** A link that opens the phone's Messages app with the text filled in. */
function smsLink(phone, body) {
  return `sms:${phone}?&body=${encodeURIComponent(body)}`;
}

async function sendTwilio(to, body) {
  if (!config.smsLive) return { status: 'simulated' };
  const res = await fetch(`https://api.twilio.com/2010-04-01/Accounts/${config.twilio.sid}/Messages.json`, {
    method: 'POST',
    headers: {
      Authorization: 'Basic ' + Buffer.from(`${config.twilio.sid}:${config.twilio.token}`).toString('base64'),
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({ To: to, From: config.twilio.from, Body: body }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.message || `Twilio error ${res.status}`);
  return { status: 'sent' };
}

const esc = (s) => String(s).replace(/[&<>"']/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));

/** Email with the CAN-SPAM basics: unsubscribe link, dealership address, honest subject. */
async function sendEmail(c, subject, body) {
  const s = store.getSettings();
  const unsub = `${config.publicUrl}/unsubscribe/${store.unsubToken(c.id)}`;
  const footer = [s.dealership, s.dealer_address].filter(Boolean).join(', ');
  const text = `${body}\n\n--\n${footer}\nUnsubscribe: ${unsub}`;
  const html = `<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.5;color:#222">${esc(body).replace(/\n/g, '<br>')}</div>
    <p style="font-family:Arial,sans-serif;font-size:12px;color:#888;margin-top:24px">${esc(footer)}<br><a href="${unsub}">Unsubscribe</a></p>`;
  const t = mailer();
  if (!t) return { status: 'simulated' };
  const fromName = (config.smtp.fromName || [s.salesperson, s.dealership].filter(Boolean).join(' - ') || config.smtp.user).replace(/"/g, '');
  await t.sendMail({ from: `"${fromName}" <${config.smtp.user}>`, to: c.email, subject, text, html, headers: { 'List-Unsubscribe': `<${unsub}>` } });
  return { status: 'sent' };
}

module.exports = { render, smsLink, sendTwilio, sendEmail };
