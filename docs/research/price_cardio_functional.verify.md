# Verification log: price_cardio_functional

Checked 2026-10-28 by an adversarial fact-checker. Target: `price_cardio_functional.md` and its JSON result.

## How it was checked

- Re-pulled about 150 cited Shopify listings through each store's product JSON (`/products/<handle>.js`), comparing price, compare-at price and availability for each variant.
- Read Rogue pages (rig, Lite rig, GymTurf, sleds, medicine balls, Echo bike, rower and ski, Concept2 SkiErg, TrueForm, refurbished Echo) from their schema.org JSON-LD and page text.
- Read Concept2 RowErg and SkiErg, Assault `/bikes/`, NTAI, Rework and Skelcore pages as HTML text, and the Life Fitness preventive-maintenance PDF with `pdftotext`.
- Fetched the Planet Fitness FY2018 and FY2023 10-Ks with WebFetch.
- Downloaded the complete Hoist, Fitness Exchange and iSellFitness catalogs (`products.json`) to recompute the fee statistics.
- johnsonfitness.com (Matrix) returns HTTP 403 to both curl and WebFetch. Sharpsheets and Athletic Business also return 403.
- The session's web-search budget ran out partway through. Only one Matrix price could be cross-checked by search.

## Result in one line

Transcription is excellent: every fetchable listing price matched exactly, and every tier median recomputes with the stated rounding. The problems are in scope and derivation, and four values need correcting.

## Corrections

| id | claimed | corrected | why |
|---|---|---|---|
| `recumbent_bike.price_value` | $2,950 | **$3,000** | The True Performance $2,879 row is the "FLOOR MODEL 9" TOUCHSCREEN" variant, a display unit. The cheapest new variant is "Emerge" at $2,999 (compare-at $3,199). The median of $2,799 / $2,999 / $2,999 / $3,899 is $2,999. |
| `turf_lane.price_commercial` | $2,150 | **~$2,500** | The report defines a lane as 6.5x50 ft (325 sq ft). The cell instead prices a 250 sq ft Rogue roll ($1,924) and a 350 sq ft half-track ($2,349.50). At the slice's own $7.70/sq ft, 325 sq ft costs $2,503. Price lanes as $/sq ft x footprint lane area. |
| `rig_bay.price_premium` | $4,000/bay | **~$1,700/bay** | Not the same scope as the commercial tier. The XTC Compact 2x4 and 4x4 are freestanding 4 ft storage units ("ideal for hospitality ... organization and storage"). The XTC Standard 4x14 ($11,950) includes about 26 attachments. A same-scope premium frame is the Rogue Monster Rig 2.0 Racked: 10' $3,655, 14' $5,055, 20' $5,875, which is $1,469-$1,828 per bay. |
| `freight.recommended_pct_project_default` | 10% | **12%** (8-20) | NTAI states "Installation and shipping commonly add 12-20%" and "Installation adds 8-15%". The Hoist 10.2% figure covers install only. The cited Aira FDD page shows freight of $1,000-$10,000 against an "Initial Fitness Equipment Package $5,906 to $39,800" (lump sum or deposit). The $9,300-$130,165 base and the "8-11%" share do not appear on that page. |

## Confirmed (spot list)

- **Treadmill.** Value $4,350, commercial $10,300 and premium $14,000. All Fitness Exchange, Fitness Superstore, Life Fitness, The Fitness Outlet, Top Fitness and Total Fitness USA rows are exact.
- **Elliptical, bikes, indoor cycle, climber, curved treadmill, air bike, rower, ski erg and recumbent stepper.** All cells match their fetched rows exactly.
- **Rogue Monster Rig 2.0.** Base $2,365 / $3,195 / $3,720 / $4,820; Standard $2,625 / $3,545 / $4,070 / $4,995. The sizing table reads 4'+6' ... 4'+6'+4'+6'+4' with 6 / 8 / 10 / 12 uprights. The REP rig has 8 / 10 / 12 uprights, is 6 ft deep and 108 in tall.
- **Rogue GymTurf.** Width 5 ft, 5/8 in foam backing, $1,089 for 25 ft and $1,924 for 50 ft. ECORE tiles are 23x46 in and 24x24 in.
- **Concept2.** The RowErg "retails for $990" ($1,155 with tall legs) and is $940 / $1,105 at 5 or more units. Ground shipping to the lower 48 is $55 / $85. The SkiErg is $850 and the floor stand $220.
- **Assault.** The /bikes/ page shows the Classic at "Sale price $749 Regular price $799", the Pro X at $899 and the Elite at $1,499, all marked Sold Out.
- **Fitness Exchange fee ladder.** Fees are $199 / $249 / $299 / $349 / $399 / $599 / $499, including the odd $599 at $5k-$5,999. Delivery is local, within 49 miles.
- **Install fees.** iSellFitness charges $399 / $299 / $349. Life Fitness haul-away is $177.
- **Hoist.** Recomputed exactly: n=17, median 10.2%, range 5.7-20.5%.
- **Planet Fitness 10-Ks.** FY2018: "every five to seven years". FY2023: "approximately every five to nine years" ("instead of every five to seven years", effective 1 Jan 2024, "based on store volume"). The report's quoted sentence is a paraphrase.
- **Maintenance sources.** Skelcore says "$300 and $800 per year". Rework says "$200-$400 per machine", "7-10 year useful life" and "turf 3-5 years". The Life Fitness PDF says "every 3 or 6 months".

## Caveats the optimizer should carry

1. **Refurbished pairs.** 15 of the 21 remanufactured listings are sold out, so their prices may be stale. The 6 in-stock pairs have a median of **54.4%**, against 62.4% for all 21. The recommended 50% still holds. The CTX claim now reads "30-70% less" (the blog redirects to buildagym.com), not "40-60%".
2. **Matrix prices.** Matrix figures from Johnson Fitness search snippets could not be fetched, and they move several medians. Without the two Matrix rows, the treadmill commercial median would be $9,250 rather than $10,300. The Endurance LED price of $10,495 was corroborated, and Relink lists the T-ES-LED at $12,507.
3. **Rower commercial tier.** The $1,900 median is pulled up by club-brand rowers. The common club purchase is the Concept2 with tall legs at $1,155.
4. **Sold-out new listings.** Several new listings are sold out: the Assault bikes, all 3 TrueForm rows, LF IC5 and IC6, French Fitness MIC4, BodyKore AR100, the LF SE3 HD outlet unit and both Woodway 4Front rows.
5. **Sleds.** Plate-loaded sled prices exclude plates.

## Missing data (see the structured output for the full list)

- Plates for sleds
- Electrical circuits for motorized cardio
- Rubber flooring under functional and cardio zones
- Volume discounts on fleet orders
- Arc trainer, AMT, UBE, BikeErg and kettlebell sets
- Non-local LTL freight per unit
- Labor to install rigs and turf
- Lease rates
- Availability flags
