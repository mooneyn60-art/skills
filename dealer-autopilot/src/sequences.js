// Stages and default message templates, written friendly-professional, from the salesperson, one ask per message.
// Every template starts UNAPPROVED. Nothing goes out automatically until you approve the template once
// (Templates tab), and even then only Sold-stage templates and appointment reminders are allowed to automate.
//
// Placeholders: {first_name} {vehicle} {stock} {objection} {salesperson} {dealership} {dealer_phone}
//               {dealer_address} {review_link}
// Text inside [[ ... ]] is dropped when any placeholder in it is empty, e.g. "[[ I know {objection} was the concern.]]"
// Anything in [square brackets] is for you to fill in before sending (video link, times...).

const STAGES = {
  new_lead: { label: 'New internet lead', group: 'follow_up', auto_ok: false },
  phone_up: { label: 'Phone-up', group: 'follow_up', auto_ok: false },
  be_back: { label: 'Unsold showroom (be-back)', group: 'follow_up', auto_ok: false },
  appointment: { label: 'Appointment set', group: 'follow_up', auto_ok: true },
  sold: { label: 'Sold', group: 'sold', auto_ok: true },
  lost: { label: 'Lost / bought elsewhere', group: 'outreach', auto_ok: false },
  dnc: { label: 'Do not contact', group: 'dnc', auto_ok: false },
};
// Your original three buckets, as groups of stages.
const GROUPS = {
  follow_up: { label: 'Follow Up', stages: ['new_lead', 'phone_up', 'be_back', 'appointment'] },
  sold: { label: 'Sold', stages: ['sold'] },
  outreach: { label: 'Outreach', stages: ['lost'] },
  dnc: { label: 'Do not contact', stages: ['dnc'] },
};

const T = (day, channel, body, subject = '') => ({ day, channel, body, subject });

const DEFAULT_STEPS = {
  new_lead: [
    T(0, 'sms', "Hi {first_name}, it's {salesperson} at {dealership}. Thanks for your interest in the {vehicle}[[ (stock #{stock})]]. It's here and available to see. Are you planning on trading anything in? Reply STOP to opt out."),
    T(0, 'email', "Hi {first_name},\n\nThanks for reaching out about the {vehicle}[[ (stock #{stock})]]. It's here on the lot and available, and I'm happy to answer any questions about it.\n\nAre you planning on trading anything in?\n\n{salesperson}\n{dealership}\n{dealer_phone}", 'The {vehicle} you asked about'),
    T(0, 'call', 'Call {first_name} about the {vehicle}. Confirm it fits, ask about trade and timeframe, offer two appointment times.'),
    T(1, 'sms', "Hi {first_name}, it's {salesperson}. I put together a quick walkaround video of the {vehicle} for you: [paste video link]. Would you like to see it in person?"),
    T(2, 'call', 'Call {first_name}. Follow up on the walkaround video and offer an appointment.'),
    T(3, 'email', "Hi {first_name},\n\nI wanted to give you a second option alongside the {vehicle}: [similar vehicle or trim, stock #]. Both are worth a look.\n\nWould [day/time 1] or [day/time 2] work for you to come see them?\n\n{salesperson}\n{dealership}\n{dealer_phone}", 'Another option for you, {first_name}'),
    T(5, 'sms', "Hi {first_name}, it's {salesperson} at {dealership}. Are you still looking, or should I close your file for now? Either answer is completely fine."),
    T(7, 'sms', "Hi {first_name}, it's {salesperson}. [One new thing: new arrival / incentive / trade value]. Would you like me to send you the details?"),
    T(10, 'email', "Hi {first_name},\n\nI wanted to share something new that might help with your search: [new arrival / incentive / trade value].\n\nWould you like me to put a few options together for you?\n\n{salesperson}\n{dealership}\n{dealer_phone}", 'Something new for you, {first_name}'),
    T(14, 'call', 'Call {first_name}. One new reason to talk (new arrival, incentive or trade value).'),
    T(21, 'email', "Hi {first_name},\n\nJust checking in. If you're still shopping, let me know what matters most to you (budget, size, features) and I'll send over the best matches.\n\n{salesperson}\n{dealership}\n{dealer_phone}", 'Still shopping, {first_name}?'),
    T(30, 'sms', "Hi {first_name}, it's {salesperson} at {dealership}. Checking in to see if you're still in the market. Is there anything I can help with?"),
    T(60, 'email', "Hi {first_name},\n\nWe've had some new vehicles come in since we last talked. If you're still looking, I'd be glad to help whenever the timing is right.\n\n{salesperson}\n{dealership}\n{dealer_phone}", 'New arrivals at {dealership}'),
    T(90, 'sms', "Hi {first_name}, it's {salesperson}. Just checking in. Are you still looking for a vehicle, or have you found one?"),
  ],
  phone_up: [
    T(0, 'sms', "Hi {first_name}, it's {salesperson} at {dealership}. Thanks for calling about the {vehicle}. This is my cell, so feel free to text me any questions. When would be a good time for you to come see it? Reply STOP to opt out."),
    T(1, 'call', 'Call {first_name} about the {vehicle}. Offer two appointment times.'),
    T(3, 'sms', "Hi {first_name}, it's {salesperson}. [One new thing: second option / incentive / trade value]. Would you like me to send you the details?"),
    T(7, 'call', 'Call {first_name}. Check in and offer an appointment.'),
    T(14, 'email', "Hi {first_name},\n\nI wanted to follow up on the {vehicle}. If anything has changed in what you're looking for, let me know and I'll find the right options for you.\n\n{salesperson}\n{dealership}\n{dealer_phone}", 'Following up on the {vehicle}'),
    T(30, 'sms', "Hi {first_name}, it's {salesperson} at {dealership}. Are you still looking, or should I close your file for now? Either answer is completely fine."),
    T(60, 'sms', "Hi {first_name}, it's {salesperson}. Just checking in. Is there anything I can help you with?"),
  ],
  be_back: [
    T(0, 'sms', "Hi {first_name}, it's {salesperson}. Thanks for taking the time to look at the {vehicle} today.[[ I know {objection} was the main concern, so I'm going to work on some options for you.]] Would tomorrow afternoon be a good time to talk?"),
    T(1, 'call', 'Call {first_name} about the one thing that held them back[[: {objection}]].'),
    T(3, 'sms', "Hi {first_name}, it's {salesperson}. I have an update for you: [another unit / program / updated trade number]. Would you like me to send over the details?"),
    T(7, 'call', 'Call {first_name}. Check in on the {vehicle} decision.'),
    T(14, 'sms', "Hi {first_name}, it's {salesperson} at {dealership}. Are you still thinking about the {vehicle}, or would you like me to look at other options for you?"),
    T(30, 'email', "Hi {first_name},\n\nI wanted to check in since your visit. If you're still looking, I'd be glad to help, whether that's the {vehicle} or something else that fits better.\n\n{salesperson}\n{dealership}\n{dealer_phone}", 'Checking in, {first_name}'),
    T(60, 'sms', "Hi {first_name}, it's {salesperson}. Just checking in. Are you still in the market for a vehicle?"),
    T(90, 'email', "Hi {first_name},\n\nWe've had new inventory come in. If you're still shopping, let me know what you're looking for and I'll send the best matches.\n\n{salesperson}\n{dealership}\n{dealer_phone}", 'New arrivals at {dealership}'),
  ],
  appointment: [],
  sold: [
    T(0, 'sms', "Congratulations on your new {vehicle}, {first_name}! Thank you for choosing {dealership}. It was a pleasure working with you. - {salesperson}"), // tip: attach your delivery photo in Messages before you hit send
    T(3, 'sms', "Hi {first_name}, it's {salesperson}. How are you enjoying the {vehicle}? Do you have any questions about the Bluetooth, keys or features?"),
    T(7, 'sms', "Hi {first_name}, I hope you're enjoying the {vehicle}! If you had a good experience, would you mind leaving a quick review? {review_link}"),
    T(30, 'sms', "Hi {first_name}, it's {salesperson}. I hope the {vehicle} is treating you well! If you know anyone who's looking for a vehicle, I'd really appreciate it if you sent them my way."),
    T(180, 'email', "Hi {first_name},\n\nIt's been about six months with your {vehicle}, so it may be getting close to time for service. Our service team will take great care of you, and I'm happy to help you get scheduled.\n\n{salesperson}\n{dealership}\n{dealer_phone}", 'Time for service on your {vehicle}?'),
    T(365, 'sms', "Happy one year with your {vehicle}, {first_name}! Thank you again for being a customer. If there's ever anything I can do for you, just let me know. - {salesperson}"),
    T(730, 'sms', "Hi {first_name}, it's {salesperson} at {dealership}. Vehicles like your {vehicle} are holding their value well, and yours may be worth more than you owe. Would you like me to run the numbers for you?"),
  ],
  lost: [
    T(0, 'sms', "Hi {first_name}, it's {salesperson}. Congratulations on your new vehicle! Would you like me to send you occasional updates, like trade values or new arrivals? No problem at all if not."),
    T(90, 'email', "Hi {first_name},\n\nI hope you're enjoying your vehicle. Here's a quick update from {dealership}: [trade values / new arrivals].\n\n{salesperson}\n{dealership}\n{dealer_phone}", 'A quick update from {dealership}'),
    T(180, 'email', "Hi {first_name},\n\nJust a quick check-in from {dealership}. If you or someone you know is shopping, I'm always happy to help.\n\n{salesperson}\n{dealership}\n{dealer_phone}", 'Checking in from {dealership}'),
  ],
  dnc: [],
};

// Appointment messages (not a day-by-day cadence; sent around the appointment time).
const APPT_TEMPLATES = {
  confirm: { channel: 'sms', body: "Hi {first_name}, you're all set for your {appt_type} on {appt_time}. Our address is {dealer_address}. Just ask for {salesperson} when you arrive. See you then!" },
  reminder_day: { channel: 'sms', body: "Hi {first_name}, it's {salesperson} at {dealership}. Just a reminder about your {appt_type} tomorrow, {appt_time}. We're at {dealer_address}, and you can ask for me when you arrive. Does that time still work for you?" },
  reminder_2h: { channel: 'sms', body: "Hi {first_name}, looking forward to seeing you at {appt_clock} today[[ for the {vehicle}]]. We're at {dealer_address}. Just ask for {salesperson}." },
  no_show: { channel: 'sms', body: "Hi {first_name}, it's {salesperson}. Sorry we missed you today! Would [day/time 1] or [day/time 2] work better to come by?" },
};

module.exports = { STAGES, GROUPS, DEFAULT_STEPS, APPT_TEMPLATES };
