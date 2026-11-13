// Loads .env (no extra dependency) and exposes config.
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..');
const envPath = path.join(ROOT, '.env');
if (fs.existsSync(envPath)) {
  for (const line of fs.readFileSync(envPath, 'utf8').split(/\r?\n/)) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
    if (!m || line.trim().startsWith('#')) continue;
    let val = m[2];
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) val = val.slice(1, -1);
    if (process.env[m[1]] === undefined) process.env[m[1]] = val;
  }
}

const env = process.env;
module.exports = {
  ROOT,
  port: Number(env.PORT || 3000),
  publicUrl: (env.PUBLIC_URL || `http://localhost:${env.PORT || 3000}`).replace(/\/$/, ''),
  appPassword: env.APP_PASSWORD || '',
  dbPath: env.DB_PATH || path.join(ROOT, 'data', 'dealer.db'),
  twilio: {
    sid: env.TWILIO_ACCOUNT_SID || '',
    token: env.TWILIO_AUTH_TOKEN || '',
    from: env.TWILIO_FROM_NUMBER || '',
  },
  smtp: {
    host: env.SMTP_HOST || '',
    port: Number(env.SMTP_PORT || 465),
    user: env.SMTP_USER || '',
    pass: env.SMTP_PASS || '',
    fromName: env.EMAIL_FROM_NAME || '',
  },
  anthropicKey: env.ANTHROPIC_API_KEY || '',
  get smsLive() { return !!(this.twilio.sid && this.twilio.token && this.twilio.from); },
  get emailLive() { return !!(this.smtp.host && this.smtp.user && this.smtp.pass); },
};
