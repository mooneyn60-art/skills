# Quarterly Rule Audit, Q4 2026 (first one)

One-line: R1-R17 read end to end against the live book (NOLAN_LOG,
trades.jsonl) and the hourly routine. 16 documentation drifts FIXED in
TARS_RULES.md (18 edits, no rule's substance changed). 9 findings where
what the account DOES no longer matches what the rules SAY. Those need
Nolan, because fixing them means either changing a rule or changing behaviour.

Last Updated: 2026-10-01
Status: DONE. No trades. No substantive rule changes.
Audience: Nolan, TARS sessions

## The worst one

**The account now runs on unwritten exceptions.** On 2026-09-30 TARS bought a
SPY "core" position as a FRACTIONAL share (R12 forbids fractional shares
because they can't carry a stop), with NO STOP (R4: "a position without a
live stop is a bug"), by MARKET order (R5: limit orders only), after Nolan
overrode the 15% cash floor (R3). Each step had Nolan's go-ahead, and each
is reasonable on its own. But none of it is written into the rules, so the
rulebook now describes a book that doesn't exist. This is the carve-out
creep the audit routine warns about: "how a mechanical system becomes a
discretionary one without anyone noticing."

## A. Documentation drift, FIXED in TARS_RULES.md

    where                     said                                     now says
    top banner                "NOT changed: R4's 8% trail ... stays"   trail widened 8% -> 20% on 9/22
    R2 (repair note)          "the 8% trail stays in force"            + note: widened to 20% same day
    R2                        old rule 3 (5% of 20-day high) as live   labelled HISTORY, deleted 9/22
    R2                        "Rule 5, the sector cap"                 it is rule 3 now
    R3 (twice)                "account is never refilled"              annotated: weekly deposits since 9/17
    R3 ABBV note              exits "below both moving averages"       below the 200-day
    R3 granularity            "all five R2 conditions"                 three since 9/22
    R3                        $340 "KNOWN FUTURE PROBLEM"              marked RESOLVED 9/22
    R4 exits note             "R2's five conditions", 8% trail         labelled history; principle stands
    R4                        "TENB ... is the live test"              TENB closed 9/17, +0.77R
    R1                        "no options until R9 opens them"         + "or R17's slot"
    R9 target structure (2x)  "$50 per option" cap                     superseded: 3%, R17 slot 6%
    TARS-2 status block       8% trail "still in force"                widened to 20% on 9/22
    R15                       evidence quoted as t=8.46 only           + status: t=2.21 clustered;
                                                                         integration test worse; repeal pending
    R16                       "As of 9/23 the streak is 0"             marked snapshot; 10/1: R16 ON
    R17 slot trade #1         open position description                outcome added: -0.21R, 9/28
    header                    Last Updated 9/24                        10/1

## B. Rules the account is NOT following (need Nolan: change the rule or the behaviour)

1. **SPY core position** breaks R12 (fractional), R4 (no stop) and R5
   (market order). Either write an "index core" carve-out into the rules
   (no stop, fractional allowed, limit or market), or bring it into line.
   TARS's suggestion: a written carve-out is honest. An index fund doesn't
   need a single-stock stop, but it must be WRITTEN, with a size limit.

2. **The 15% cash floor (R3)** was below the floor on 9/28-9/29 through
   Nolan's buys and was overridden on 9/30. The override is recorded in
   NOLAN_LOG as "one-time", but the floor has no written override
   procedure and no restore deadline. Cash was ~4% on 10/1.

3. **Nolan's own trades sit outside every rule.** Puts, sub-60-day options,
   a 0DTE NVDA call, five WBD $31 calls at $0.03, several options open at
   once, SOFI shares added on the way down (R3: "no averaging down, ever"),
   positions with no stop. None of the rules says which of R2-R17 apply to
   trades Nolan places himself. R7 ("only one agent places orders") also
   doesn't address the owner trading in the app while TARS manages stops,
   which is how stops got cancelled under TARS twice in a week.
   Needed: one short section, "Owner trades", saying what TARS does when
   Nolan trades (log, protect with a stop, or leave alone).

4. **R17 says "exactly one option"; the account held up to three calls plus
   puts at once (9/28)**, mostly outside R17's contract rules. Either the
   extra options are "owner trades" (see 3) or R17's count is not being
   followed.

5. **R4's trail is mechanical, but INTC's trail raise (101.70 -> 101.91)
   waited from 9/24 to 9/30 "on Nolan's go-ahead"**. R4 says stops are
   raised on the close without asking. Either the desk lacked permission
   (a tooling issue to fix) or R4 is being treated as discretionary.

6. **R8 / R17 scoring not done.** No closed slot trade records
   `spy_same_window_pct`, and Nolan's 9/30 sales of two SOFI calls have no
   closing rows (R8's reconciliation rule exists because of exactly this
   gap). Behaviour to fix, at the desk.

7. **R13 (no dollar balances in pushed files) is being broken in
   notes/NOLAN_LOG.md**: post-9/23 entries carry buying power, cash and
   position dollar totals. R13's text covers the ledger and commit
   messages; the log is pushed to the same remote. Proposed: the log
   follows R13 too, going forward; history is not rewritten.

8. **R15's evidence is contested** (see A). The repeal recommendation from
   2026-09-26 is still waiting for Nolan. It is the only rule whose own
   integration test says it makes the system worse.

9. **R16 retirement and R6 breaker**: the October monthly audit measured the
   live R6 breaker at ~2.5pp/yr of CAGR for ~4pp less drawdown (one run,
   not hurdle-tested). Nothing to change now; flagged so the weekend block
   tests it properly.

## Contradictions checked and NOT found

- No two rules use the same threshold in opposite directions (R15's
  inversion carries its own trend-exit exemption).
- Numbers repeated across rules agree: 20% cap (R3, R15, R17 by reference),
  8% stop and +8% breakeven (R4, R15, hourly routine), 3-day earnings gap
  (R2, R15), 15% floor (R3, R17), 20/25 VIX zones (R15, hourly routine).
- A trigger that can't fire: R9's own gate still leaves TARS-opened options
  practically unaffordable at $2,000 (documented in R9, not new).

## Stale evidence

No rule's evidence is older than six months; all of it is from September
2026. But two pieces were re-tested this week and came back worse:
R15 (above), and R2's 200-day return edge, which reversed over the last 12
months (t=-2.11, n=11; research/2026-10-01_MONTHLY_AUDIT.md). R2's risk
role is unaffected.

## Carve-outs, reconciled

    written:    SOFI exempt from the trend exit and sector cap (9/22)
                [moot since 9/30: SOFI was stopped out, 0 shares]
    UNWRITTEN:  SPY core (B1), cash-floor override (B2), owner trades (B3),
                multi-option holdings (B4)
