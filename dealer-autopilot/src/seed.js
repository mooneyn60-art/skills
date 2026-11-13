// Demo data so you can click around. Run: npm run seed  (uses a separate demo database unless DB_PATH is set)
const path = require('node:path');
process.env.DB_PATH ||= path.join(__dirname, '..', 'data', 'demo.db');
const store = require('./db');
const appts = require('./appointments');
const queue = require('./queue');

store.saveSettings({ salesperson: 'Nolan', dealership: 'Demo Motors', dealer_address: '100 Demo Blvd, Springfield', dealer_phone: '(555) 010-2000', review_link: 'https://g.page/r/demo' });
for (const v of [
  { stock_number: '24518', year: '2024', make: 'Chevrolet', model: 'Tahoe', trim: 'LT', color: 'Black', miles: '12,400' },
  { stock_number: 'T1122', year: '2025', make: 'Toyota', model: 'RAV4', trim: 'XLE', color: 'Blue', miles: '8' },
  { stock_number: 'P3391', year: '2021', make: 'Ford', model: 'F-150', trim: 'XLT', color: 'White', miles: '41,200' },
]) store.upsertInventory(v);

const ago = (days) => new Date(Date.now() - days * 86400000).toISOString();
const people = [
  { first_name: 'Mike', last_name: 'Jones', phone: '555-201-3344', email: 'mike.demo@example.com', stage: 'new_lead', stock_numbers: '24518', consent: true, consent_source: 'Lead form opt-in', source: 'Cars.com' },
  { first_name: 'Sara', last_name: 'Lee', phone: '555-201-9999', stage: 'be_back', stock_numbers: 'T1122', objection: 'the monthly payment', consent: true, consent_source: 'Said yes in person' },
  { first_name: 'Dev', last_name: 'Patel', phone: '555-201-7777', email: 'dev.demo@example.com', stage: 'phone_up', stock_numbers: 'P3391' },
  { first_name: 'Ana', last_name: 'Ruiz', phone: '555-201-5555', email: 'ana.demo@example.com', stage: 'sold', stock_numbers: 'P3391', consent: true, consent_source: 'Signed at delivery' },
  { first_name: 'Tom', last_name: 'Baker', phone: '555-201-1212', stage: 'lost', on_dnc_registry: true, customer_initiated: false },
  { first_name: 'Rita', last_name: 'Gomez', phone: '555-201-3030', stage: 'sold', sold_date: '2023-09-02', vehicle_interest: 'Honda CR-V', consent: true, consent_source: 'Signed at delivery' },
  { first_name: 'Ben', last_name: 'Cho', phone: '555-201-4040', stage: 'new_lead', vehicle_interest: 'Toyota RAV4', consent: true, consent_source: 'Lead form opt-in', referred_by: 'Ana Ruiz' },
];
const ids = people.map((p) => store.upsertCustomer(p).customer.id);
// Make one lead look like it came in 2 days ago and was answered in 3 minutes, for the scoreboard.
store.db.prepare('UPDATE customers SET lead_at = ?, first_contact_at = ? WHERE id = ?').run(ago(2), new Date(Date.now() - 2 * 86400000 + 3 * 60000).toISOString(), ids[2]);
const tz = store.getSettings().timezone;
const tomorrow = store.localParts(new Date(Date.now() + 86400000), tz).date;
appts.create({ customer_id: ids[1], date: tomorrow, time: '11:00', type: 'test_drive', stock_number: 'T1122' });
queue.generateDue();
queue.markReplied(ids[0], 'Is the Tahoe still available? Can I come Saturday?');
console.log('Demo data ready in', process.env.DB_PATH);
