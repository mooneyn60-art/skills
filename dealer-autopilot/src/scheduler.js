// Runs every minute: turns due cadence steps into tasks on your list, queues appointment reminders,
// and sends only the automations you approved (inside 8 am - 9 pm, to consented customers).
const queue = require('./queue');
const appointments = require('./appointments');

let running = false;
async function tick() {
  if (running) return { skipped: 'already running' };
  running = true;
  try {
    const queued = queue.generateDue();
    const appt = appointments.tick();
    const auto_sent = await queue.autoSend();
    return { queued, appointment_tasks: appt, auto_sent };
  } finally {
    running = false;
  }
}

function start() {
  const run = () => tick().catch((e) => console.error('[scheduler]', e));
  setTimeout(run, 2000);
  return setInterval(run, 60 * 1000);
}

module.exports = { start, tick };
