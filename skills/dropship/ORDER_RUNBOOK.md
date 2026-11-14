# FurEver Faces: order runbook

How one order gets from "paid" to "shipped" while the products are not linked to Printify. Written 2026-11-14 after one timed test with Mac's photo.

## Fulfilment choice

Recommended now: **(b) manual orders**. The products stay as they are and each order is placed by hand in Printify. It works today, needs no rebuild, and suits the first few orders. Move to (a), rebuilding each product inside the Printify app, once orders are regular.

Manual order, click by click:
1. Shopify admin → Orders → open the order. Note the product, variant, pet name and shipping address.
2. Shopify admin → Apps → Printify → Orders → Create order (manual).
3. Pick the matching blank from the catalog (ornament, 11 oz mug, tee...) and a US print provider.
4. Upload the approved art file, place it on the product, enter the customer's shipping address, pay.
5. When Printify gives a tracking number: back in the Shopify order → Fulfill items → paste the tracking number → Fulfill.

## Per-order art workflow

1. **Get the photo.** Open the order. The line item shows "Pet name" and "Pet photo"; download the photo.
2. **Make the art** in the style ordered:
   - Cut the pet out of the photo (`rembg`, model `isnet-general-use`).
   - Royal / Santa Paws / animated styles: place the cut-out on a plain colour canvas and run the image-to-image script (`gen.py`, model `SimianLuo/LCM_Dreamshaper_v7`) with the style prompt.
   - Mugshot / License / Tarot / Rookie Card / Pop Art: drop the cut-out and the pet's name into the HTML template and render it.
   - Check the result by eye. Regenerate with another seed if the anatomy is wrong.
3. **Email the proof** to the customer from the store inbox. Nothing prints until they reply yes. Edits are free.
4. **Send to Printify** using the manual order steps above.
5. **Mark fulfilled** in Shopify with the tracking number.

## Timed test (Mac, Royal style, 2026-11-14)

| Step | Time |
|---|---|
| Cut-out | 6 s |
| Royal art, 640 x 800 | 208 s |
| Enlarge to 2400 x 3000 | under 1 s |
| **Machine total** | **215 s (3.6 min)** |

Not tested: the proof email, the Printify order and the fulfilment step. Those need a real order and Printify access. Estimate for a person doing steps 1, 3, 4 and 5: about 10 minutes, so plan on roughly 15 minutes per order.

## Known limits

- The art is 640 x 800 enlarged by simple resizing. It is fine for a mug or ornament and soft on a 16 x 20 canvas.
- The image model follows the photo more than the prompt; about one result in four needs a retry.
- The image model lives in a cloud session and must be reinstalled if that session is reclaimed.
