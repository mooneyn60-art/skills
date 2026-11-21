# FurEver Faces: orders for the store agent

What is already done, the next steps in order, and what not to do. From TARS at Nolan's request, 11/14.

Last Updated: 2026-11-14
Status: active, replaces your own plan
Audience: the FurEver Faces store agent

## Overview
Nolan's words: the store isn't on track and the work keeps getting handed back to him. Stop new design work. The store can't fill an order yet, and that comes first. Do the steps below in order, one at a time, no sub-agents, no new models. The account is near its weekly usage limit.

## Already done by TARS (don't redo)
- Removed the fake compare-at prices on all 10 products, and the "bestseller" tag.
- Built pet-name and pet-photo upload fields on every product page, and removed "Buy it now" (it skips the photo). Committed to the unpublished theme "FurEver Faces – Holiday Chaos (TARS fixes)". **Not live until Nolan publishes it.**
- Wrote the refund and shipping policy text: `skills/dropship/POLICIES_TO_PASTE.md` on branch `claude/package-installation-setup-yv4j79`.

## Your steps, in this order
1. **Stop the current art and model download.** Save and push anything already made (`git push`).
2. **Fulfillment.** The products are set to manual fulfillment at Nolan's home location; none is linked to Printify. Write Nolan a 5-line, click-by-click guide for one of these two, recommending one:
   - **(a) Rebuild in Printify:** the Printify app in Shopify admin, one product at a time, starting with the ornament, the 11 oz mug and the memorial ornament. This replaces the hand-made products; keep the same titles, prices and descriptions.
   - **(b) Manual orders:** keep the products as they are; for each order, place a Printify order by hand. Fine for the first few orders.
3. **The per-order art workflow,** in `skills/dropship/ORDER_RUNBOOK.md`. For each order:
   1. Open the order and download the "Pet photo".
   2. Make the art in the style ordered (Royal / Santa Paws / Cartoon), with whatever tool you have working.
   3. Email the customer a proof.
   4. When they approve, send the file to Printify (link the order, or a manual order).
   5. Mark it fulfilled with tracking.

   Test it once with Nolan's own pet photo, start to finish, and time it. Report the minutes per order.
4. **Make the dates match.** The site says "Order by Dec 5" in the ticker and steps, but "mid-December" in the product descriptions. Make every product description say Dec 5.
5. **Report to Nolan in 3 lines:** what works, what he must click (publish the theme, paste the policies, the Printify login step), and minutes per order.

## Not now (after the first real order)
- No new designs, slogan products, ads, videos or extra apps.
- No traffic until steps 1-4 are done and Nolan has published the theme.

## Rules
- Never fake reviews, sales counts, "bestseller" tags or compare-at prices.
- Never use trademarked characters or brands.
- Ask before spending money.
