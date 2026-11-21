# Car Sales Follow-Up System: build brief

The spec for the agent building Nolan's automated follow-up system as a car salesperson. Written by TARS for Nolan (11/13).

Last Updated: 2026-11-13
Status: brief for the builder agent
Audience: Nolan's follow-up builder agent, Nolan

## Overview
Nolan sells cars. The goal: no lead or customer ever falls through the cracks, and every follow-up goes out on time with Nolan only stepping in for real conversations.

**The system's job:** know who each person is (stage), what they need next (cadence), send or queue it, stop the moment a human reply or a sale happens, and hand Nolan a short "who to call today" list.

**Measure everything against 4 numbers** (weekly):

| Number | Formula |
|---|---|
| Response time to new internet leads | target under 5 minutes |
| Appointment-set rate | appointments ÷ leads |
| Show rate | shows ÷ appointments |
| Sold rate | sold ÷ shows |

Plus repeat/referral sales from past customers, monthly.

## Rule 0: compliance first (build this before any message goes out)
Getting this wrong costs real money and can cost Nolan his job. Confirm the details with the dealership's management or compliance person.
- **Use the dealership's CRM if it has automation** (VinSolutions, DealerSocket, Elead, DriveCentric and others all do). It already handles consent, opt-outs and records, and the dealership owns the customer data. Ask the sales manager before running texts from a personal phone or a separate tool: many dealerships forbid it.
- **Texts and calls (US federal TCPA):**
  - Automated or marketing texts need the customer's consent first. Record when and how they gave it.
  - Honour STOP / "don't text me" immediately and permanently.
  - Send only 8 am-9 pm in the customer's local time.
  - Check numbers against the Do Not Call registry for anyone who didn't contact the dealership first.
  - Several states have stricter rules (for example Florida and Oklahoma): ask.
- **Business texting through a service like Twilio** requires A2P 10DLC registration, or messages get blocked.
- **Email (CAN-SPAM):**
  - an unsubscribe link in every marketing email
  - the dealership's physical address
  - honest subject lines
- **Customer data:** dealerships fall under the FTC Safeguards Rule. No customer info (licence, credit, SSN, income) in spreadsheets, personal email or chat tools. Names, phone, email, vehicle of interest and stage only.
- **Pricing:** never text a price, payment or "approved" claim the dealership can't honour in writing.

## The stages (every person is in exactly one)
1. **New internet lead:** filled out a form or a third-party lead.
2. **Phone-up:** called in.
3. **Unsold showroom (be-back):** visited, didn't buy.
4. **Appointment set:** has a date and time.
5. **Sold:** took delivery.
6. **Lost:** bought elsewhere, or not in the market. Long, slow nurture only.
7. **Do not contact:** opted out. Nothing, ever.

**Stop rules:**
- Any reply from the customer stops the automated sequence and puts them on Nolan's call list.
- Booking an appointment moves them to stage 4.
- A sale moves them to stage 5.

## Cadences
D0 = the day they came in. Call steps are "put on Nolan's list", never auto-dialled.

### New internet lead
| When | What |
|---|---|
| Within 5 min | Text plus email: thank them, answer their exact question (the vehicle they asked about), one question back ("Are you trading anything in?") |
| D0 | Call (Nolan) |
| D1 | Text: short walkaround video of the vehicle they asked about |
| D2 | Call |
| D3 | Email: a second option (similar vehicle or trim) and appointment times |
| D5 | Text: "Still looking, or should I close your file?" |
| D7, D10, D14 | Alternate text / email / call, each with one new thing (new arrival, incentive, trade value) |
| D21, D30 | Then monthly nurture until they buy or opt out |

### Unsold showroom (be-back)
| When | What |
|---|---|
| D0 (same evening) | Thank-you text with Nolan's name and photo, recapping the vehicle and the one thing that held them back |
| D1 | Call about that one thing (payment, trade, colour, spouse) |
| D3 | Something new (another unit, a programme, an updated trade number) |
| D7 | Call |
| D14 | Text |
| D30 | Email |
| After | Monthly |

### Appointment set
- **Confirmation:** text when booked.
- **Reminder:** the day before, plus 2 hours before, with the address and "ask for Nolan".
- **No-show:** a "sorry we missed you" text 30 min after, plus a rebook link or times.

### Sold (where repeat business and referrals come from)
| When | What |
|---|---|
| D0 | Thank-you text plus a delivery photo |
| D3 | "How's the new car? Any questions about Bluetooth, keys or features?" |
| D7 | Review request (one link) |
| D30 | Check-in plus a referral ask |
| ~6 months / first service | Service reminder |
| Ongoing | Birthday (if given) and purchase anniversary |
| Months 24-30 (lease end or equity) | "Your car may be worth more than you owe" |

### Lost / bought elsewhere
- Congratulate them and ask if they want occasional updates.
- Then quarterly at most, and only if they said yes.

## Message rules (every message)
- Short (under 300 characters for texts), from Nolan, in Nolan's voice. Never "Dear valued customer".
- Personal fields:
  - first name
  - vehicle of interest
  - the one objection or detail from the visit
  - Nolan's name
- One ask per message: a question or an appointment time, never both.
- Never pushy. Never fake urgency ("only 1 left today" unless it's true).
- No price, payment or approval claims unless the manager signed off.

## Build plan (in order; don't skip ahead)
1. **Week 1: the list, not the robot.**
   - A simple customer table: name, phone, email, consent (yes/no plus date), stage, vehicle, last contact, next step, next date.
   - Every morning, the system makes Nolan a list: "Call these 5. These 8 texts are drafted, approve with one tap."
   - **Nothing sends on its own yet.**
2. **Week 2: templates.** All the messages above, written in Nolan's voice, with the personal fields. Nolan approves each template once.
3. **Week 3: automate only the safe ones.** Appointment reminders, sold-customer thank-yous and review requests, to customers with recorded consent. New-lead first-touch only through the dealership CRM or a registered sender.
4. **Week 4: the scoreboard.** The 4 numbers, weekly, plus which message gets the most replies.
5. **After that:** one change a week, measured.

## Rules for the builder agent
- **Draft-and-approve before auto-send.** Nolan sees every new message type before it goes out automatically.
- **Stop on reply, every time.** A customer who answers gets a human.
- **Never message anyone without recorded consent,** never after STOP, never outside 8 am-9 pm.
- **Don't build a giant system.** A table, a daily list, templates and reminders beat any fancy dashboard.
- **Ask Nolan, don't guess:** dealership CRM name, whether texting from his own number is allowed, his hours, his voice (send him 3 sample texts to pick from).
