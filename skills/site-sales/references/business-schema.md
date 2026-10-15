# Business JSON schema

`scripts/build_site.py` reads one `sites/<slug>/business.json` per business
(adapted from the local-booking-sites schema). Fill fields **only** from public
sources you can link to. Anything you would otherwise guess goes in as a
placeholder object, which the page shows with a dashed "Placeholder:" outline
and `--check` lists:

```json
"phone": { "placeholder": "Phone number (owner to add)" }
```

Any value below may be a placeholder except `name` and `sources`.

| Field | Type | Notes |
| --- | --- | --- |
| `name` | string | **Required.** Exactly as the business writes it. |
| `category` | string | Short label shown above the name ("Urban flower micro-farm"). |
| `location.city`, `location.state` | string | Shown with the category. Leave `city` out if the business location is not public. |
| `location.label` | string | Shown as "Where" under Contact (for example a market stall). |
| `location.map_query` | string | Text for the Google Maps link. Defaults to address + city + state. |
| `tagline` | string | One line under the name. Must be a fair summary of the sources. |
| `about` | string | Short paragraph from the sources, lightly edited. |
| `highlights[]` | strings | Tick list under About. Facts only. |
| `services_title` | string | Heading for the services list. Default "What we offer". |
| `services[]` | array | **Required, at least one.** `{ "name", "description"?, "price"? }`. A numeric price is formatted with `currency` (default `$`); omit unknown prices or use a placeholder. |
| `hours_title` | string | Default "Hours". |
| `hours` | list or object | Either `[{ "label", "value" }]` rows, or `mon`…`sun` → `["HH:MM","HH:MM"]` / `null` (closed). |
| `email`, `phone`, `instagram`, `facebook` | string | At least one **real** route is required. |
| `cta` | object | Main button: `kind` (`email`, `phone`, `instagram`, `facebook`, `url`), `label`, optional `subject`/`body` (email) or `url`. |
| `theme` | object | `primary`, `accent`, `background`, `surface`, `text`, `muted`, `font_display`, `font_body` (Google Fonts). Style, not fact. |
| `sources[]` | array | **Required.** `{ "url", "note" }` for every page a fact came from. Listed in the preview footer. |
| `_preview_by` | string | Optional sender name for the preview banner. Keys starting with `_` are notes and are never rendered. |

Do not add photos or reviews unless the owner has supplied them or given
permission; their Instagram/Facebook images are their content.

Build modes:

- default: **preview** — black "Free preview … not the official site" banner,
  `noindex`, and a "Where these details came from" source list.
- `--final`: no banner, no source list. Use only after the owner has paid and
  confirmed every fact and placeholder.
