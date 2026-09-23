# Gut Calls — Nolan vs TARS

A running scorecard of Nolan's gut calls, each logged BEFORE the outcome with
exact resolution criteria, alongside TARS's own probability for the same
event. Purpose: find out how good the gut actually is. Weather forecasters
got calibrated by writing every call down and checking it. Same idea.

Last Updated: 2026-09-23
Status: OPEN — 1 call pending

## How scoring works

- Each call gets a precise, checkable criterion and a deadline, fixed at the
  time it is logged. Nobody reinterprets it afterwards.
- TARS logs its own probability for the same event at the same time.
- When the deadline passes, the call is marked HIT or MISS with the
  evidence. TARS's probability is scored too (Brier score), so the
  comparison runs both ways.

## Call #1 — SOFI goes to $20 after earnings

Logged:     2026-09-23, ~11:10am ET
Nolan said: "It goes to 20 after earnings I think"
Context:    SOFI $16.89 at logging. Q3 earnings expected 2026-10-27 before
            the open (date unverified). Needs +18.4% to reach $20.
            Range since March: $14.88-$20.13.

RESOLUTION (chosen by TARS; Nolan can adjust before earnings):
  HIT if SOFI CLOSES at or above $20.00 on any trading day from 2026-10-27
  through 2026-11-27 (one month after the report). Closing price, not
  intraday, so one spike doesn't count.

Nolan's call:  YES
TARS's estimate: ~40%
  Basis: implied volatility ~59% from the Jan-2028 options, about two months
  to the deadline. Chance of FINISHING above $20 is roughly 25%; the chance
  of CLOSING above it on at least one day in the window is higher, around
  40%. Earnings adds upside variance the smooth-volatility maths
  understates, and the $0.17 estimate vs three flat quarters is a real
  catalyst. That's what keeps TARS from going lower.

Outcome: PENDING — scored on 2026-11-27 after the close.
