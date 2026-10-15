#!/usr/bin/env bash
# Rebuild the two sample reports exactly as produced for the demo (2026-10-15).
# Truth is re-fetched live from each business's website; the AI answers are the
# recorded claude-websearch observations + dated press reports in answers/<slug>/.
set -euo pipefail
cd "$(dirname "$0")/../scripts"

python3 truth.py --name "The Viridian Bookshop" --town Willoughby --region OH \
  --website https://viridianbookshop.com --slug viridian-bookshop-willoughby \
  --listing https://bookshop.org/shop/ViridianBookshop \
  --social https://www.facebook.com/p/The-Viridian-Bookshop-61570579876171/ \
  --social https://www.instagram.com/viridian.bookshop/ \
  --press https://spectrumnews1.com/oh/cincinnati/news/2026/07/23/bookshop-ai-battle \
  --press https://clevelandmagazine.com/articles/willoughby-bookstore-confronts-google-ai-error-claiming-it-was-permanently-closed/ \
  --press https://clevelandmagazine.com/articles/downtown-willoughby-welcomes-the-viridian-bookshop-in-october \
  --twin "Viridian Books|||https://marketspread.com/vendor/161775/viridian-books/|A different, similarly named bookseller (Oklahoma) that appears in the same web searches" \
  || echo "site unreachable: keeping the previous truth file"

python3 truth.py --name "Stefanina's Wentzville" --town Wentzville --region MO \
  --website https://www.stefaninas-wentzville.com --slug stefaninas-wentzville \
  --listing "https://www.iexitapp.com/Missouri/I-70/Exit%20208/8463" \
  --listing https://www.toasttab.com/local/wentzville-mo-restaurants/best-pizza \
  --social https://www.instagram.com/stefaninaswentzville/ \
  --press https://www.29news.com/2025/08/20/restaurant-battles-fake-deals-offered-by-google-ai-its-coming-back-us/ \
  --press https://www.wlox.com/2026/01/30/restaurant-asks-customers-verify-information-after-ai-generates-fake-deals/ \
  --twin "Stefanina's Pizzeria (Stef's Pizza, O'Fallon)|8645 Veterans Memorial Pkwy, O'Fallon, MO 63366|(636) 272-3499|https://stefaninas.com/|A separately owned 4-location chain (Stef's Pizza, owned by LaBeaume Roderick Group) with the same name in O'Fallon, St. Peters, Lake St. Louis and St. Charles." \
  --twin "Stef's Pizza Jungermann|652 Jungermann Rd, St. Peters, MO 63376|(636) 447-7800|https://stefaninas.com/jungermann-location/|Part of the O'Fallon chain" \
  --twin "Stef's Pizza Lake St. Louis|111 Pond Fort Trail, Lake St. Louis, MO 63367|(636) 625-3333|https://stefaninas.com/lake-st-louis-location/|Part of the O'Fallon chain" \
  --twin "Stef's Pizza Zumbehl|1938 Zumbehl Rd, St. Charles, MO 63303|(636) 724-7800|https://stefaninas.com/zumbehl-location/|Part of the O'Fallon chain" \
  || echo "site unreachable: keeping the previous truth file"

for s in viridian-bookshop-willoughby stefaninas-wentzville; do
  python3 compare.py --slug "$s" --date 2026-10-15
  python3 report.py --slug "$s" --date 2026-10-15 --sample
done
