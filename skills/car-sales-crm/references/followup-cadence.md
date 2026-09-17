# Follow-up cadence and stage flow

## Default cadence by status

| status | meaning | next follow-up |
|---|---|---|
| hot | actively deciding — just visited, just discussed numbers, said they'll decide "this week" | next business day |
| warm | engaged but not urgent — test drove, asked good questions, no timeline pressure | 3-4 days |
| cold | early browsing, went quiet after first contact, "just looking" | 7-14 days |
| sold | deal closed | none — move to a check-in cadence instead, see below |
| lost | went with another dealer / vehicle / decided not to buy | none, unless they said "check back in [timeframe]" — respect what they told you over any default |

Always let something the customer explicitly said override the table (e.g. "call me back after the 15th" beats the default).

## Stage progression

`new -> contacted -> test-drive -> negotiating -> financing -> closed`

Update `stage` whenever it changes so the digest and message drafts reflect where they actually are — talking points for someone at `negotiating` are different from someone at `new`.

## After the sale: staying on the hook for referrals/repeat business

Once `status: sold`, don't stop tracking them — switch to a light-touch cadence instead of the sales cadence:
- ~1 week after delivery: check-in text (how's the vehicle, any questions).
- ~1 month: quick check-in, ask for a review/referral if the interaction was positive.
- Around service intervals or lease-end/loan-payoff timing if known: reach back out — this is often the best source of repeat business.

Set `next_followup` for these same as any other reminder; just note in the customer's file that it's a post-sale touch, not a sales push.
