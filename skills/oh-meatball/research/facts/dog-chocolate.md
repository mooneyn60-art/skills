# Fact pack: dog-chocolate (series 72), chocolate and dogs

Prepared for: Meatball Myths pet Short and TikTok cut. Research date: 2026-11-16. Topic prefix: DOGC.
Searched phrase (word for word, from the brief): can dogs eat chocolate.

How each source was opened:
- [raw] = I fetched the page myself with curl and copied the quote from the page text today.
- [api] = the journal record from the Europe PMC API (abstract only; the paper itself was not opened).
- Quotes keep the source's own spelling and units.

## 0. Read this first

- SOLID: the main fact. The FDA page opened today (page says "Content current as of: 04/29/2024"). Both the dose line (9 and 18 mg per pound) and the table (227 vs 57 mg per ounce) are on it, word for word.
- SOLID: a second independent source agrees. The Merck Veterinary Manual chapter (written by an ASPCA Animal Poison Control Center vet, peer reviewed by a University of Minnesota vet school toxicologist, last updated Feb 2026) gives 20 mg/kg for mild signs and 40-50 mg/kg for heart effects, which is the same as FDA's 9 and 18 mg per pound.
- SOLID: the ASPCA page says darker chocolate means more risk.
- ABOUT THE "4x": it is the FDA table, 227 / 57 = 3.98, for dark chocolate (70-85% cacao) against milk chocolate, per ounce. That is theobromine only. Merck counts theobromine plus caffeine together and its dark and milk rows do not give the same ratio (see section 4). Say "about 4 times" and credit the FDA table, never "4 times as deadly".
- NOT FOUND / NOT OPENED: a vet school page. Cornell returned 404 and UC Davis returned 403 (see "Could not open"). The USDA FoodData Central lookup (FDA's own source for the table) was rate limited.
- ok = true: the main fact is confirmed from the agency's own page today.

## 1. Fact rows

| ID | Fact (shortest true wording) | Exact quoted sentence | URL | Share of what / condition it needs |
|---|---|---|---|---|
| DOGC1 | Theobromine can cause mild signs in dogs at doses as low as 9 mg per pound of body weight. | "Theobromine can cause mild signs in dogs with doses as low as 9 mg per pound of body weight, and severe signs starting around 18 mg per pound of body weight." [raw] | https://www.fda.gov/animal-veterinary/animal-health-literacy/leave-chocolate-out-rovers-celebrations | A dose per pound of the dog's own weight, so the same bite is a bigger dose for a small dog. "As low as" and "around" are the agency's hedges. Not one dose for all dogs. |
| DOGC2 | Severe signs start around 18 mg per pound, double the mild dose. | Same sentence as DOGC1. [raw] | same | Per pound of body weight. "Starting around": an approximate line, and FDA also lists how sensitive the dog is as a factor. |
| DOGC3 | Dark chocolate (70-85% cacao) has about 227 mg of theobromine in one ounce. Milk chocolate has about 57 mg. That is about 4 times as much (227 / 57 = 3.98, my arithmetic). | The table, "Approximate amount of theobromine in 1 ounce (mg)": "Milk chocolate 57", "Dark chocolate with 70-85% cacao 227". Same page: "the darker the chocolate, the higher the cocoa content, and therefore, the more theobromine the chocolate contains." [raw] | same | Per 1 ounce of chocolate, theobromine only, "approximate". Brands vary (Merck: "The exact amount of methylxanthines in chocolate varies"). The 4x is a ratio of two table values, not a measured result on any one bar. |
| DOGC4 | The same page lists more: semisweet chips 136 mg per ounce, unsweetened baking chocolate 364 mg per ounce. | Table rows "Semisweet chocolate chips 136" and "Unsweetened baking chocolate 364". [raw] | same | Per 1 ounce, theobromine, approximate. Baking chocolate is about 6.4 times milk (364 / 57, my arithmetic). |
| DOGC5 | Size matters. Half a 12-ounce bag (6 oz) of semisweet chips may give a 60-lb Lab only mild signs, but a 6-lb Chihuahua severe signs. | "That means a large dog like a Labrador retriever may develop only mild signs after eating half a 12-ounce bag (6 ounces) of semisweet chocolate chips, while a small dog like a Chihuahua may develop severe signs after eating the same amount." [raw] | same | FDA's worked example: 6 oz x 136 mg = 816 mg. Lab (60 lb): 13.6 mg per pound, "would likely have only mild to moderate signs". Chihuahua (6 lb): 136 mg per pound, "would have severe signs of chocolate toxicity and possibly die without veterinary care". Two example dogs, not a rule for every dog. |
| DOGC6 | Why chocolate hurts dogs: theobromine and caffeine are stimulants, and dogs break them down more slowly than people, so the effects last longer. | "Dogs, on the other hand, can't break down these compounds as quickly, so the side effects last longer." [raw] | same | Cause stated by FDA as the reason side effects last. Merck gives the half-life of theobromine in dogs as 17.5 hours. |
| DOGC7 | Signs can show up within a few hours: vomiting, diarrhea, fast heart rate, restlessness, muscle spasms, seizures. Severe cases can lead to death in some cases. | "Signs of chocolate toxicity can appear within a few hours of a dog eating the chocolate and can range from mild to severe" and "Severe chocolate toxicity can lead to death in some cases." [raw] | same | "Some cases" and "can": not every dog, not every bite. Merck says signs "usually occur within 6-12 hours after ingestion", so "a few hours" and "6 to 12 hours" are both agency wording (section 4). |
| DOGC8 | An independent vet reference gives the same two lines: mild signs at 20 mg/kg, heart effects at 40-50 mg/kg, seizures at 60 mg/kg or more. | "In general, mild clinical signs (vomiting, diarrhea, polydipsia) may occur in dogs ingesting 20 mg/kg; cardiotoxic effects occur after ingesting 40-50 mg/kg, and seizures occur after ingesting doses ≥ 60 mg/kg." [raw] | https://www.merckvetmanual.com/toxicology/food-hazards/chocolate-toxicosis-in-animals | Per kilogram of the dog, methylxanthines (theobromine plus caffeine). 20 mg/kg is 9.1 mg per pound and 40 mg/kg is 18.2 mg per pound (my arithmetic), so it matches FDA. Same chapter: "individual susceptibility to methylxanthines varies" and severe signs "may occur at much lower doses". |
| DOGC9 | The ASPCA also says the darker the chocolate, the greater the risk, and white chocolate has the least. | "The darker (higher cacao percentage) the chocolate, or the higher the caffeine content, the greater the risk for toxicity. White chocolate has the lowest methylxanthine content while baking chocolate and cocoa powder have the highest concentrations." [raw] | https://www.aspca.org/pet-care/animal-poison-control/people-foods-avoid-feeding-your-pets | A direction (darker = more), not a number. Agency-level statement of the same idea as DOGC3. |
| DOGC10 | In one vet clinic's records of 156 dogs that ate chocolate, 112 had no signs, 44 had signs, and 43 of those 44 survived. | "One hundred and twelve dogs had no clinical signs. Forty-four dogs had clinical signs of chocolate intoxication." and "43 of the 44 dogs survived." [api] | https://pubmed.ncbi.nlm.nih.gov/33788297/ (Weingart, Hartmann, Kohn, J Small Anim Pract 2021, DOI 10.1111/jsap.13329) | 156 dogs seen at one clinic, 2015-2019, which is a count of dogs brought in, not all dogs that ever eat chocolate. 28 of the 44 sick dogs "ingested dark and bitter chocolate". The 43 of 44 survived "after decontamination (apomorphine, activated carbon) and symptomatic treatment", meaning with vet care. Abstract only; paper not opened. This paper is on FDA's own reference list. |
| DOGC11 | Safety line (from an agency): if your pet is sick or has an emergency, call your veterinarian; if they are not available, call an emergency animal hospital or an animal poison control center. | "FDA cannot give veterinary medical advice. If your pet is sick or has a veterinary emergency, call your veterinarian. If your veterinarian is unavailable, call your local emergency animal hospital or an animal poison control center." [raw] | https://www.fda.gov/animal-veterinary/animal-health-literacy/leave-chocolate-out-rovers-celebrations | The trigger a viewer can act on: "if your pet is sick" or you know your dog ate chocolate. Merck: "Early GI decontamination can decrease severity of clinical effects", which is why calling early matters. |
| DOGC12 | FDA's storage advice: keep chocolate stored safely out of dogs' reach. | "keep chocolate stored safely out of their reach." [raw] | same | Agency advice. Fits the gag (cake on the top shelf), but see section 3 on the ladder card. |

(12 usable rows. All were read on the live page or API record today.)

## 2. Three hook facts

1. DOGC3: dark chocolate (70-85% cacao) has about 227 mg of theobromine per ounce, milk chocolate about 57. About 4 times as much (FDA table, per ounce, approximate).
2. DOGC1 + DOGC5: FDA's dose is per pound of the dog: mild signs from 9 mg per pound, severe from about 18. The same 6 ounces of semisweet chips may give a 60-lb Lab mild signs and a 6-lb Chihuahua severe signs.
3. DOGC10: in a 156-dog clinic record, 112 had no signs and 43 of the 44 that did survived with vet care. Only as the "call the vet early" payoff, not as "it's fine".

## 3. Do not say

| Tempting line | Why it fails | Safe version |
|---|---|---|
| "A little is fine" / "this much is safe" / any safe amount | FDA gives where mild signs start ("as low as 9 mg per pound"), not a safe amount, and it depends on the dog (DOGC1, DOGC5). | "FDA says mild signs can start at 9 mg per pound of the dog." |
| One dose for all dogs ("10 grams kills a dog") | The dose is per pound of body weight and varies by sensitivity (DOGC1, DOGC5, DOGC8). | Always say "per pound" or show the Lab and the Chihuahua. |
| "One bite always kills" / "chocolate kills dogs" | FDA says "can lead to death in some cases". 112 of 156 dogs in the clinic record had no signs and 43 of 44 sick dogs survived with care (DOGC7, DOGC10). | "Severe cases can be fatal." |
| "Dark chocolate is 4 times as deadly" | The 4x is theobromine per ounce in a table, not deaths or danger (DOGC3). | "About 4 times the theobromine, per ounce, in FDA's table." |
| "Milk chocolate is safe / only dark is dangerous" | Milk chocolate still has 57 mg per ounce and a small dog can reach the mild dose with little (DOGC3, DOGC5). | Say "less theobromine", not "safe". |
| "White chocolate is safe" | Merck: "negligible source of methylxanthines", but it is high in fat and the pancreatitis line applies (FDA: chocolate "can contain a lot of fat and sugar"). Keep out of the script. | Leave white chocolate out. |
| "Dogs can't taste/know it's bad" or any dog feeling or motive ("Noodle knows he shouldn't") | No source. A reaction is an action on screen, never a feeling or motive said as fact. | "Noodle stares up." (action only). |
| "Make the dog vomit at home" or any home treatment | FDA gives no such advice; it says call the vet. Merck says treatment is by a vet (decontamination, supportive care). | The only instruction is "call your vet". |
| "Wait and see if he's ok" | Signs may take hours (DOGC7: a few hours; Merck: 6-12 hours). | "If your dog ate chocolate or seems sick, call your vet." |
| "Dogs can't process theobromine" | FDA: dogs "can't break down these compounds as quickly", slower, not unable. | "Dogs break it down slower than people." |
| A joke that adds a number, a danger or a safety instruction (rule 3 of "Make them funnier") | Jokes are on Meatball only. | The ladder card, the cake and Noodle's stare are all actions. |

## 4. Shortened-claim traps

| Long, true wording | Cut to five words and it becomes false |
|---|---|
| "About 4 times the theobromine per ounce (FDA table)" | "Dark chocolate is 4x deadlier." (danger, not theobromine; not per bar, per ounce) |
| "Mild signs can start at 9 mg per pound of the dog" | "9 mg is toxic." (drops "per pound", reads as one dose for any dog) |
| "May develop only mild signs" (the Lab) | "Labs are fine." (not what FDA says; "mild to moderate" and "likely") |
| "Severe cases can lead to death in some cases" | "Chocolate kills dogs." |
| "Severe signs starting around 18 mg per pound" | "18 mg kills." (a dose of severe signs, per pound, not death) |
| "Dark chocolate (70-85% cacao)" | "Dark chocolate" alone: FDA's 227 is for 70-85%; unsweetened baking chocolate is 364 and semisweet chips 136, so "dark" has no single number. |
| "43 of 44 sick dogs survived with vet treatment" | "Dogs survive chocolate." (drops "with treatment", "at one clinic" and that 44 is only the sick ones) |
| "Keep chocolate out of reach" | "Put it on a high shelf and you're done." (FDA says stored safely out of reach; a dog that stares at a top shelf and a ladder is the joke, and a counter is not out of reach for every dog; keep the ladder card as a visual gag only) |
| "If your pet is sick, call your vet" | "Call your vet" alone drops the trigger. Keep "if your dog ate chocolate or seems sick". |

## 5. Disagreements between sources

- Theobromine alone vs methylxanthines: FDA's table counts theobromine only (milk 57, dark 70-85% 227, chips 136, baking 364 mg per ounce). Merck's table counts theobromine plus caffeine (milk 64, semisweet and sweet dark 150-160, baker's 440, cocoa powder 807 mg per ounce). Merck's own dark-to-milk ratio from its semisweet row is about 2.3 to 2.5, and for a 65% bar (its worked example, 286 mg per ounce) about 4.5. So "4x" holds for FDA's 70-85% row; with other bars it is anywhere from about 2.4x to 6x or more. Use only the FDA table and name it.
- When signs show: FDA "within a few hours"; Merck "usually ... within 6-12 hours". Say "hours", not one number.
- Dose lines agree: FDA 9 and 18 mg per pound = 19.8 and 39.7 mg/kg; Merck 20 mg/kg mild and 40-50 mg/kg heart effects. (my conversions, 1 kg = 2.2 lb). Merck adds seizures at 60 mg/kg or more (about 27 mg per pound); FDA does not give a seizure dose, so do not mix the two on one card.
- FDA says "as low as 9" and Merck says "may occur" and "severe clinical signs and death may occur at much lower doses". So 9 is not a floor of safety.
- Merck says about 1 ounce of milk chocolate per pound of body weight "is potentially lethal"; FDA gives no lethal dose. Not used: a lethal number would invite a "safe below it" reading.
- The FDA page is dated 04/29/2024 ("Content current as of"). It is the page the brief named; Merck (updated Feb 2026) confirms the numbers are still current.

## 6. Could not open

- Cornell Richard P. Riney Canine Health Center chocolate page (on FDA's reference list): the URL I tried (vet.cornell.edu .../riney-canine-health-center/.../chocolate-toxicity and the animal-health-and-diagnostic-center health-topics address) returned HTTP 404. Not used.
- UC Davis School of Veterinary Medicine "Chocolate Poisoning in Dogs" (vetmed.ucdavis.edu/hospital/animal-health-topics/chocolate-poisoning-dogs): HTTP 403 to curl. Not used.
- USDA FoodData Central (the source FDA cites for the theobromine table): the API returned HTTP 429 (rate limit on the demo key) and the numbers were not checked there. The FDA page is the agency source for the table; Merck gives its own table (section 5).
- The Weingart 2021 paper itself (journal page) was not opened; only the abstract from the Europe PMC API (DOGC10). The source page of Pet Poison Helpline was not opened (not needed).
- The Merck chapter is a veterinary reference book, not an agency or a paper; I rely on it as the second source because it is written by an ASPCA Animal Poison Control Center vet and peer reviewed by a vet school toxicologist. If the checker wants a vet school page, use the ASPCA page (DOGC9) and the Weingart abstract (DOGC10) in addition.

## 7. Notes for the script (not facts)

- Gag (line 2): Meatball bakes a chocolate cake and puts it on the top shelf; his dog, Noodle, stares up. Card: "Meatball asks for a ladder." All action, no motive or feeling said. Write "his dog, Noodle," with the comma.
- Do not let the ladder card or the top shelf stand as a safety instruction. If a safety line is said, it is the DOGC11 one, said clean, and it carries its trigger ("if your dog ate chocolate or seems sick").
- The searched phrase "can dogs eat chocolate" goes in the first spoken sentence. The honest answer line is "No. Chocolate is toxic to dogs" (FDA: "Chocolate is toxic to dogs." [raw]), then the hedged numbers.
- Per-pound math as a visual (my arithmetic from FDA's table, to be re-checked by the second model): a 10-lb dog at 9 mg per pound is 90 mg, about 0.4 oz of dark (90 / 227) or about 1.6 oz of milk (90 / 57). Only use it if shown as "FDA's mild-sign line for a 10-pound dog", never as a safe or toxic amount for a real dog, and never as the only dose.
