# Business JSON schema

`scripts/build_site.py` reads one JSON file per business. Only `name`, at least
one service, and one contact route are required; every other section is left
out of the page when it is missing. Fill each field only from what the
screenshots show.

| Field | Type | Notes |
| --- | --- | --- |
| `name` | string | **Required.** Exactly as on their profile. |
| `tagline` | string | Short line under the name in the hero. |
| `bio` | string | Their bio, lightly cleaned up. Shown as "About". |
| `location.address`, `location.city` | string | Shown under Contact. |
| `phone`, `email`, `instagram` | string | At least one of these, or `booking.endpoint`, is **required**. |
| `currency` | string | Prefix for numeric prices. Default `$`. |
| `services[]` | array | **Required, at least one.** |
| `services[].name` | string | **Required.** |
| `services[].price` | number or string | A number is formatted with `currency`; a string such as `"from $45"` is shown as written. Leave it out if unknown. |
| `services[].duration_min` | integer | Used to size time slots. Default 30. |
| `services[].description` | string | Optional one-liner. |
| `reviews[]` | array | `{ "quote", "author", "source" }`. Real reviews only, quoted exactly. |
| `photos[]` | array | URL strings, or `{ "src", "alt" }`. The first photo becomes the hero background. Use photos the owner has given you permission to use. |
| `theme` | object | `primary`, `accent`, `background`, `surface`, `text`, `muted` (CSS colours), `font_display`, `font_body` (Google Fonts names). Match their Instagram look. |
| `booking.hours` | object | Keys `mon`…`sun`, each `["HH:MM", "HH:MM"]` or `null` for closed. Default Mon–Sat 09:00–17:00. |
| `booking.slot_minutes` | integer | Gap between start times. Default 30. |
| `booking.days_ahead` | integer | How far ahead clients can book. Default 21. |
| `booking.endpoint` | string or null | Optional URL that accepts a JSON POST (for example a Formspree form). When it is set, the page adds a "Send booking request" button. |

## How booking works

The page is a single static HTML file with no server, so it takes booking
*requests*, not confirmed bookings. The visitor picks a service, day and time,
enters a name and contact, and then sends a pre-filled message by text, email or
Instagram DM, or through `booking.endpoint`. The business confirms by replying.

When a client pays for the site, move them to a real scheduler (Square
Appointments, Calendly, Acuity, Booksy, Fresha and so on) and swap the booking
section for that scheduler's embed or link, so double-bookings can't happen.
