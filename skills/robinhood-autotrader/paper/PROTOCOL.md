# Paper Trading Protocol

Rules for building a track record that is worth something.
Last updated: 2026-09-11 · Status: active · Audience: TARS, and the account owner checking my work

## Overview

The live account has **12 process trades** behind it, with a measured expectancy of
**+$0.33 per trade** — statistically indistinguishable from random. That is not
enough evidence to justify risking anyone's money, and no amount of confident
narration changes it.

This ledger exists to fix that at zero cost. Every trade the strategy would have
taken gets logged the same way a real one would, and `expectancy.py` computes
whether an edge exists. The number it prints is the only thing that should ever
justify funding this.

## The rules that make it honest

Paper trading is worthless when it is allowed to cheat, and it cheats in
predictable ways. These five rules close the known holes:

1. **Log the trade BEFORE the outcome is known.** Entry, stop, target, size and
   thesis are written at the moment of the decision. A trade recorded after the
   fact is not evidence, it is a memory with a flattering bias.

2. **Fill at the bid when selling, the ask when buying. Never the mid.** This is
   the single most common way backtests lie. On a wide-spread name it is the
   difference between an edge and a fee.

3. **Never edit a closed trade.** If a record is wrong, append a correction with
   a new id and a note. The ledger is append-only. A history that can be revised
   is a history that will be.

4. **A skipped trade is still a data point.** If the process generated a
   candidate and it was passed on, log it with `"exit_reason": "not_taken"` and
   the reason. Otherwise the record silently keeps only the ideas that felt good,
   which is how a strategy appears to work.

5. **Report R, not dollars.** R = realized ÷ planned_risk. Dollars scale with
   account size and hide whether the process works. R does not.

## Schema

One JSON object per line in `trades.jsonl`:

```json
{
  "id": "2026-09-11-001",
  "symbol": "NWSA",
  "instrument": "equity",
  "direction": "long",
  "opened": "2026-09-11T13:45:00Z",
  "closed": "2026-09-19T14:10:00Z",
  "entry": 29.00,
  "stop": 27.88,
  "target": 31.24,
  "exit": 30.10,
  "qty": 5,
  "atr_at_entry": 0.682,
  "planned_risk": 5.60,
  "realized_pnl": 5.50,
  "exit_reason": "target",
  "thesis": "pullback to Aug 10-20 base, 50d/100d = 1.045, rate-neutral (beta_TLT +0.33)"
}
```

`exit_reason` is one of: `target`, `stop`, `trail`, `thesis_broken`, `time`,
`not_taken`. It is not decoration — the breakdown by exit reason is what caught
the live account's real defect (full-size losses against fractional wins).

## Ad-hoc options requests ("my friend's AI made X%")

Not every candidate comes from the scan. When the owner (or anyone) relays
someone else's trade or result and asks to replicate it, that request gets the
full options research protocol in `reference/options.md` section 0 — never a
faster path, because a secondhand win story arrives pre-wrapped in confidence
and a real, checkable price move, which makes it *more* persuasive than a scan
hit, not less. Run all eight steps: verify the catalyst is real, read what it
actually implies (not just its headline direction), check price against analyst
target dispersion, check the macro calendar independent of the single-name
story, confirm earnings doesn't fall inside the contract's life, price the real
contract (IV/delta/theta/POP/breakeven), price the SIZE against the account's
explicit dollar floor (not a percentage), and log the result either way with
`"source": "ad_hoc"` in the thesis field.

A well-researched decline is exactly as valuable to the record as a taken trade
— it is why the next similar pitch has a dated, specific precedent to check
against instead of starting from zero.

## Scoring declined candidates

A `not_taken` record is worthless as an audit trail unless it is eventually
scored -- otherwise "the gates cost us money" or "the gates saved us" is just an
opinion. Score it mechanically, on a fixed rule, not a vibe:

1. Take the recorded `entry`, `stop`, `target` from the original record.
2. Walk forward from `opened` and check daily bars for whichever of these
   happens first: the price touches `stop`, touches `target`, or **10 trading
   days elapse** with neither touched.
3. Append a new record with `id` = `"<original-id>-SCORE"`, `exit_reason` =
   `"scored_not_taken"`, and `realized_pnl` computed as if the original size had
   been taken (entry/stop define planned_risk exactly as a real trade would).
   **Append, never edit the original** -- same rule as everything else here.
4. The running "gate tally" for a review is the sum of these scored records'
   R-multiples. It is not evidence of anything until there are enough of them
   that a confidence interval would clear zero -- see Stopping rules below,
   same bar as the real ledger.

Do this in a batch (e.g. weekly), not per-candidate per-session -- 10 trading
days rarely elapse between one session and the next.

## Beating the benchmark is a separate question

`expectancy.py` answers "did this make money against what was risked." It cannot
answer "did picking these names beat just owning the index." `benchmark.py`
does, by subtracting what the benchmark returned over the identical holding
window:

```bash
python3 skills/robinhood-autotrader/paper/benchmark.py --strategy congress-disclosure
```

This is not a nicety. The NANC congressional-trading ETF beat the S&P since
Feb 2023 purely by being concentrated in tech during a tech bull market — raw
return scored it skilful, excess return scores it flat. Any rule that buys a
sector-tilted basket inherits that illusion, and a rising market will hand it
profits that have nothing to do with the selection rule.

Two schema requirements follow, both load-bearing:

- **`entry` must hold the actual fill price**, not the limit price. A record
  with `entry: null` and only `limit_price` set is unscoreable against a
  benchmark and silently drops out of the sample. The first closed options
  trade (`2026-09-11-NVDA-C235-1002-LIVE`) has exactly this defect.
- **Tag every record with `strategy`** (e.g. `congress-disclosure`, `scan`,
  `ad_hoc`). Untagged records score as one undifferentiated blob, so a good
  rule and a bad one average into "indistinguishable."

Missing benchmark dates are reported unscoreable and never interpolated or
carried forward. A fabricated benchmark produces an alpha number that looks
computed, which is worse than no number at all.

## Stopping rules

These are commitments, not guidelines.

- **If the 95% confidence interval on expectancy is entirely below zero, stop.**
  The strategy does not work. Rebuild it or abandon it; do not keep trading it
  because the sample "feels" unlucky.
- **If the interval still spans zero after 100 trades, the edge is too small to
  matter** at this account size even if it is real. Say so plainly.
- **Do not fund the live account until the interval clears zero** — and, given
  the owner's debt at 23% APR, not until that debt is at zero either. A proven
  edge of +0.2R is still worse than a guaranteed 23%.

## Reading the output

```bash
python3 skills/robinhood-autotrader/paper/expectancy.py
```

The verdict line is the whole point. `indistinguishable from random` means
exactly that, however green the total looks — a positive sum over a small sample
is the single easiest thing in trading to mistake for skill.
