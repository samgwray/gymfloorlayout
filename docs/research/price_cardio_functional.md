# Equipment prices: cardio & functional (topic: price_cardio_functional)

Prepared 2026-10-28 for the gym-layout planner. Every listing price below was observed on 2026-10-28 (the "date seen") unless the row says otherwise.

## 1. Method

- **Data collection.** About 25 manufacturer and dealer storefronts expose machine-readable catalogs (Shopify `products.json`). I downloaded those catalogs on 2026-10-28, about 30,000 product rows in all. Sources include Life Fitness's own store, Fitness Exchange, Fitness Superstore, Top Fitness (a Precor dealer), Push Pedal Pull, The Fitness Outlet, LiveFit, Total Fitness USA, REP, Titan, Torque, Power Systems, TRX, TITLE Boxing, Everlast, Hoist, CTX Home Gyms (remanufactured), Blue Sky Fit Supply, Competitors Outlet, iSellFitness, Recovery for Athletes, American Barbell, Bells of Steel, Fringe Sport and elitefts. I matched products by exact title and console variant, and took the price and the "compare-at" (list or MSRP) price from the feed. Rogue pages were parsed from their schema.org JSON-LD. Concept2 and Assault Fitness pages were read directly. Johnson Fitness (Matrix) sits behind Cloudflare, so its prices come from search-index snippets of its product and category pages; those rows are marked `fetched=false`.

- **Tiers.** VALUE = light-commercial or budget-commercial lines: Spirit CT/CE/CU/CR 800-900, Star Trac 4-series, Body-Solid Endurance, Matrix Lifestyle, StairMaster 4G, REP/Titan functional. COMMERCIAL = mainstream club grade: Star Trac 6-series, Life Fitness Club Series+/Aspire/Integrity, Matrix Endurance/Performance LED, Precor 600 line, StairMaster 8Gx, Concept2 with stand or tall legs, Rogue. PREMIUM = top club lines and touchscreen consoles: Precor 700/800 line with P82/P84, Star Trac 8/10-series, Matrix Performance Touch, Woodway, NOHrD, Hammer Strength HD, Torque TANK, Legend, Life Fitness/Escape accessories.

- **Recommended value.** The recommended value is the **median of the listed current selling prices** in each item×tier cell. It is rounded to $50 above $1,000, to $10 between $100 and $1,000, and to $1 below $100. Low and high are the min and max of the cell. Each recommended value is a derived estimate (`is_estimate=true`). Prices are street/selling prices; where a dealer shows a higher compare-at (MSRP) price, it appears in the "List" column.

- **Exclusions.** Prices exclude sales tax, freight and installation (see §4). For plate-loaded sleds, prices exclude plates.

## 2. Recommended model prices (USD, new, per unit or station)

| Item id | Unit | VALUE typical (low-high, n) | COMMERCIAL typical (low-high, n) | PREMIUM typical (low-high, n) |
|---|---|---|---|---|
| `treadmill` | unit | **$4,350** ($3,799-$5,465, n=6) | **$10,300** ($6,199-$12,065, n=9) | **$14,000** ($12,800-$19,600, n=9) |
| `curved_treadmill` | unit | **$3,500** ($3,299-$4,495, n=5) | **$6,400** ($4,499-$6,895, n=5) | **$9,100** ($8,199-$9,467, n=4) |
| `elliptical` | unit | **$3,300** ($2,860-$4,640, n=5) | **$6,500** ($5,455-$8,625, n=7) | **$12,450** ($10,400-$15,430, n=6) |
| `upright_bike` | unit | **$2,950** ($2,399-$3,700, n=4) | **$4,200** ($3,829-$5,505, n=7) | **$8,650** ($5,150-$9,499, n=5) |
| `recumbent_bike` | unit | **$2,950** ($2,799-$3,899, n=4) | **$4,950** ($3,885-$6,555, n=8) | **$8,350** ($5,540-$9,899, n=6) |
| `indoor_cycle` | unit | **$1,850** ($1,100-$2,199, n=6) | **$2,600** ($2,401-$2,985, n=6) | **$3,850** ($3,120-$4,395, n=6) |
| `air_bike` | unit | **$900** ($749-$945, n=4) | **$1,500** ($1,199-$2,049, n=5) | **$2,700** ($2,575-$2,784, n=2) |
| `rower` | unit | **$930** ($925-$990, n=3) | **$1,900** ($1,155-$2,720, n=6) | **$3,650** ($3,099-$6,795, n=4) |
| `stair_climber` | unit | **$5,750** ($3,995-$5,999, n=4) | **$10,250** ($8,399-$12,420, n=4) | **$14,250** ($13,107-$17,649, n=6) |
| `ski_erg` | unit (with floor stand from commercial tier up) | **$850** ($825-$899, n=3) | **$1,150** ($1,070-$1,199, n=2) | **$1,700** ($1,654-$2,499, n=3) |
| `recumbent_stepper` | unit | **$4,800** ($4,799-$5,095, n=3) | **$7,400** ($5,400-$7,695, n=5) | **$7,750** ($7,595-$7,948, n=4) |
| `rig_bay` | per bay | **$780** ($714-$860, n=4) | **$1,000** ($875-$1,182, n=6) | **$4,000** ($2,810-$4,006, n=3) |
| `turf_lane` | per lane (see sq-ft basis) | **$1,000** ($669-$1,906, n=4) | **$2,150** ($1,924-$2,350, n=2) | **$4,350** ($3,426-$5,237, n=2) |
| `sled` | unit (plates not included for plate-loaded sleds) | **$290** ($215-$349, n=5) | **$440** ($335-$909, n=7) | **$2,150** ($1,799-$2,699, n=4) |
| `plyo_box_set` | set | **$490** ($272-$764, n=5) | **$1,200** ($825-$1,516, n=4) | **$2,050** ($1,900-$3,135, n=4) |
| `wall_ball_station` | station | **$320** ($314-$333, n=2) | **$460** ($446-$475, n=2) | **$660** ($540-$771, n=2) |
| `battle_rope_station` | station | **$150** ($145-$174, n=3) | **$260** ($244-$329, n=3) | **$380** ($340-$412, n=2) |
| `suspension_trainer_station` | station | **$180** ($130-$230, n=2) | **$310** ($290-$335, n=2) | **$430** ($423-$445, n=2) |
| `heavy_bag` | station | **$310** ($263-$378, n=3) | **$690** ($548-$750, n=3) | **$1,050** ($1,000-$1,396, n=3) |
| `stretch_area` | per mat / user | **$43** ($41.50-$43.61, n=2) | **$110** ($98.38-$112, n=2) | **$170** ($129-$210, n=3) |
| `accessory_pack` | pack | **$480** ($482-$482, n=1) | **$1,100** ($1,112-$1,112, n=1) | **$3,850** ($3,866-$3,866, n=1) |

Derived unit-cost companions:

- **Turf per sq ft** (material only). VALUE **$2.06/sq ft**: French Fitness 6.5x82 ft rolls, V1 $669 = $1.26, V2 $899 = $1.69, V3 $1,099 = $2.06; Bells of Steel 538 sq ft roll $1,905.99 = $3.54; Titan 4x15 ft $239.97 = $4.00 (list $4.58). Median of the five is $2.06. COMMERCIAL **$7.70/sq ft**: French Fitness 14x50 ft marked 2-lane track $4,699 = $6.71; Rogue/Dollamur GymTurf (5 ft wide, 5/8 in foam backing) 5x50 ft $1,924 = $7.70 and 5x25 ft $1,089 = $8.71. PREMIUM **$13.30/sq ft**: ECORE RageTurf Rally 12 mm turf-on-rubber tile $10.54 sale ($13.81 list); UltraTile 1 in $16.11 sale ($21.13 list). The premium figure is the midpoint of the two sale prices.

- **Turf lane definition.** The per-lane prices in the table assume a 6.5x50 ft lane, about 325 sq ft. The value cell uses whole 6.5x82 ft rolls because those rolls are sold uncut. The commercial cell uses a Rogue 5x50 ft roll or half of the French Fitness 2-lane track. The premium cell uses 325 sq ft of ECORE tile. For other lane sizes, use the per-sq-ft figures above.

- **Rig per linear foot** (frame only, standard attachments). REP 4000 rig: 14 ft $2,434.99 = $174/ft; 20 ft $2,979.99 = $149/ft; 24 ft $3,570.99 = $149/ft. Rogue Monster Rig 2.0 Base: M-14 $3,195 = $228/ft; M-20 $3,720 = $186/ft; M-24 $4,820 = $201/ft. Throwdown XTC Standard 4x14 with about 17 storage and station attachments: $11,950 = $854/ft. Bay geometry from the Rogue spec table: M-10 = 4 ft + 6 ft bays (6 uprights); M-14 = 3 bays (8 uprights); M-20 = 4 bays (10 uprights); M-24 = 5 bays (12 uprights). REP: 14 ft = 8 uprights, 20 ft = 10, 24 ft = 12, all 6 ft deep and 108 in tall.

## 3. Listing evidence by item (all prices USD, new)

### `treadmill`: Commercial motorized treadmill

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | Spirit CT800 Treadmill | $3,999 | $4,999 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-ct800-treadmill-2020) | yes |  |
| value | Star Trac 4TR (10" LCD) | $3,799 | $4,299 | [Fitness Exchange](https://fitnessexchange.com/products/star-trac-4tr-treadmill) | yes |  variant: 10" LCD |
| value | Body-Solid Endurance T150 Commercial Treadmill (New) | $4,195 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/body-solid-endurance-t150-commercial-treadmill-new) | yes |  |
| value | True Launch (Unite LED) | $4,499 |  | [Fitness Exchange](https://fitnessexchange.com/products/true-launch-treadmill-1) | yes |  variant: Unite LED |
| value | Spirit CT850 Treadmill | $4,999 | $5,999 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-ct850-treadmill) | yes |  |
| value | Matrix Lifestyle LED Treadmill | $5,465 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Matrix-Lifestyle-LED-Treadmill-P36993.aspx) | no (search snippet) | price from search-index snippet; site behind Cloudflare |
| commercial | Star Trac 6TR (LED) | $6,199 | $6,899 | [Fitness Exchange](https://fitnessexchange.com/products/star-trac-6tr-treadmill-1) | yes |  variant: Apex LED |
| commercial | Spirit CT900 Treadmill | $6,999 | $7,999 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-ct900-treadmill) | yes |  |
| commercial | Life Fitness Club Series+ Treadmill (SL) | $7,599 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/club-series-plus-treadmill) | yes |  variant: SL / Black Onyx |
| commercial | Life Fitness Aspire Treadmill (SL) | $9,269 |  | [The Fitness Outlet](https://thefitnessoutlet.com/products/life-fitness-aspire-treadmill) | yes |  variant: Artic Silver / SL Console |
| commercial | Life Fitness Integrity+ Treadmill (base console) | $10,299 |  | [The Fitness Outlet](https://thefitnessoutlet.com/products/life-fitness-integrity-treadmill) | yes |  |
| commercial | Matrix Endurance LED Treadmill | $10,495 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Matrix-Endurance-LED-Treadmill-P36836.aspx) | no (search snippet) | search-index snippet |
| commercial | Matrix Performance LED Treadmill | $11,420 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Matrix-Performance-LED-Treadmill-P36860.aspx) | no (search snippet) | search-index snippet |
| commercial | Precor TRM 681 Treadmill (P84) | $11,800 |  | [Top Fitness (Precor dealer)](https://topfitness.com/products/precor-trm-681-treadmill-p84) | yes |  |
| commercial | Precor TRM 761 Treadmill | $12,065 |  | [Top Fitness (Precor dealer)](https://topfitness.com/products/precor-trm-761-treadmill) | yes |  |
| premium | Precor TRM 781 Treadmill (P82) | $12,800 |  | [Top Fitness (Precor dealer)](https://topfitness.com/products/precor-trm-781-treadmill-p82) | yes |  |
| premium | Precor TRM 791 Treadmill | $14,290 |  | [Top Fitness (Precor dealer)](https://topfitness.com/products/precor-trm-791-treadmill) | yes |  |
| premium | Star Trac 8TR (24" touch) | $13,999 | $15,399 | [Fitness Exchange](https://fitnessexchange.com/products/star-trac-8tr-treadmill) | yes |  variant: 24" Touchscreen |
| premium | Star Trac 10TRx FreeRunner (LED) | $13,949 | $15,399 | [Fitness Exchange](https://fitnessexchange.com/products/star-trac-10trx-treadmill) | yes |  |
| premium | True Apex (Unite 16") | $13,299 |  | [Fitness Exchange](https://fitnessexchange.com/products/true-fitness-apex-treadmill) | yes |  variant: Unite 16" - TV Capable (No Tuner) |
| premium | Woodway 4Front Treadmill with 19" TV | $17,999 |  | [Total Fitness USA](https://tfusa.net/products/woodway-4front-treadmill-with-19-tv) | yes |  |
| premium | Woodway 4Front Treadmill with Prosmart Touch Screen | $19,600 |  | [Total Fitness USA](https://tfusa.net/products/woodway-4ftont-treadmill-with-prosmart-touch-screen) | yes |  |
| premium | Matrix Performance Touch Treadmill | $18,570 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Matrix-Performance-Touch-Treadmill-P36857.aspx) | no (search snippet) | search-index snippet |
| premium | Life Fitness Integrity Treadmill SE3 HD (compare-at/regular) | $13,059 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/integrity-treadmill) | yes | Shopify JSON compare_at_price of outlet listing; outlet sale $7,183 |

### `curved_treadmill`: Non-motorized curved treadmill

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | REP Strive Curved Treadmill | $3,800 |  | [REP Fitness](https://www.repfitness.com/products/rep-strive-series-curved-treadmill) | yes |  |
| value | PRO 6 Arcadia Air Runner Non Motorized Curve Treadmill (New) | $4,495 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/pro-6-arcadia-air-runner-non-motorized-curve-treadmill-new) | yes |  |
| value | Assault Runner Pro Treadmill | $3,499 |  | [Push Pedal Pull](https://pushpedalpull.com/products/retail-assault-runner-pro-treadmill) | yes |  |
| value | BodyKore Air Runner- AR100 | $3,400 | $4,495 | [Competitors Outlet](https://competitorsoutlet.com/products/bodykore-air-runner-ar100) | yes |  |
| value | Tru Grit Runner Curved Manual Treadmill | $3,299 |  | [Total Fitness USA](https://tfusa.net/products/tru-grit-runner-curved-manual-treadmill) | yes |  |
| commercial | Assault Runner Elite Treadmill | $4,499 |  | [Push Pedal Pull](https://pushpedalpull.com/products/retail-assault-runner-elite-treadmill) | yes |  |
| commercial | Woodway Curve LTG Treadmill | $5,981 |  | [BLK BOX Fitness (US storefront)](https://www.blkboxfitness.com/en-us/products/woodway-curve-ltg-treadmill) | yes | Shopify product JSON |
| commercial | Trueform Performance Non-Motorized Treadmill (New) | $6,395 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/trueform-performance-non-motorized-treadmill-new) | yes |  |
| commercial | TrueForm Runner (Rogue) | $6,595 | $7,195 | [Rogue Fitness](https://www.roguefitness.com/trueform-runner) | yes | JSON-LD offers $6,595-$7,195 by tread option |
| commercial | TrueForm Runner Manual Treadmill | $6,895 | $7,855 | [Competitors Outlet](https://competitorsoutlet.com/products/trueform-runner-1) | yes |  |
| premium | NOHrD Sprintbok V2 (base) | $8,199 |  | [Top Fitness (Precor dealer)](https://topfitness.com/products/nohrd-sprintbok-treadmill) | yes |  |
| premium | Hammer Strength HD Tread | $9,467 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/hammer-strength-hd-tread) | yes |  |
| premium | Hammer Strength HD Tread | $9,196 |  | [Push Pedal Pull](https://pushpedalpull.com/products/retail-hammer-strength-hd-tread) | yes |  |
| premium | NOHrD Sprintbok V2 (LiveFit, base) | $8,999 |  | [LiveFit](https://livefit.com/products/nohrd-sprintbok-v2) | yes |  |

### `elliptical`: Elliptical / cross-trainer

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | Spirit CE800 Elliptical | $3,199 | $4,199 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-ce800-elliptical-2020) | yes |  |
| value | Spirit CE850 Elliptical | $3,499 | $4,999 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-ce850-elliptical-2020) | yes |  |
| value | Star Trac 4CT (10" LCD) | $3,299 | $3,699 | [Fitness Exchange](https://fitnessexchange.com/products/star-trac-ct-cross-trainer) | yes |  variant: 10" LCD |
| value | Body-Solid Endurance E5000 Premium Elliptical Trainer (New) | $2,860 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/body-solid-endurance-e5000-premium-elliptical-trainer-new) | yes |  |
| value | Matrix Lifestyle LED Elliptical | $4,640 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Matrix-Lifestyle-LED-Elliptical-P36997.aspx) | no (search snippet) | search-index snippet |
| commercial | Star Trac 6CT (LED) | $6,249 | $6,949 | [Fitness Exchange](https://fitnessexchange.com/products/star-trac-6ct-cross-trainer) | yes |  variant: Apex LED |
| commercial | Spirit CE900 Elliptical | $5,999 | $6,999 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-ce900-elliptical) | yes |  |
| commercial | LF Club Series+ Elliptical (SL) | $6,499 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/club-series-elliptical-cross-trainer) | yes |  variant: SL / Black Onyx |
| commercial | Matrix Endurance LED Elliptical | $6,795 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Commercial-Ellipticals-C161.aspx) | no (search snippet) | search-index snippet |
| commercial | Life Fitness Aspire Elliptical (SL) | $7,209 |  | [The Fitness Outlet](https://thefitnessoutlet.com/products/life-fitness-aspire-elliptical) | yes |  variant: Choose One / Artic Silver |
| commercial | Precor EFX 500 Line (base console) | $5,455 |  | [Push Pedal Pull](https://pushpedalpull.com/products/retail-precor-efx-500-line) | yes |  |
| commercial | Matrix Performance LED Elliptical | $8,625 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Commercial-Ellipticals-C161.aspx) | no (search snippet) | search-index snippet |
| premium | Star Trac 8CT (16" touch) | $12,499 | $13,799 | [Fitness Exchange](https://fitnessexchange.com/products/star-trac-8ct-cross-trainer) | yes |  variant: 16" Touchscreen |
| premium | Precor EFX 885 Elliptical (P84) | $14,130 |  | [Top Fitness (Precor dealer)](https://topfitness.com/products/precor-efx-885-elliptical-p84) | yes |  |
| premium | Precor EFX 685 Elliptical (P84) | $12,020 |  | [Top Fitness (Precor dealer)](https://topfitness.com/products/precor-efx-685-elliptical-p84) | yes |  |
| premium | Life Fitness Integrity Elliptical w/ 16in SE4 Console | $12,371 |  | [LiveFit](https://livefit.com/products/life-fitness-integrity-elliptical-w-16in-se4-console) | yes |  |
| premium | Spirit CE1000ENT Elliptical | $10,400 | $12,000 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-ce1000ent) | yes |  |
| premium | Matrix Performance Touch Elliptical | $15,430 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Matrix-Performance-Touch-Elliptical-P36892.aspx) | no (search snippet) | search-index snippet |

### `upright_bike`: Upright bike

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | Spirit CU800 Upright Bike | $2,399 | $3,399 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-cu800-upright-bike) | yes |  |
| value | Star Trac 4UB (10" LCD) | $2,699 | $2,999 | [Fitness Exchange](https://fitnessexchange.com/products/star-trac-4ub-upright-bike) | yes |  variant: 10" LCD |
| value | Spirit CU900 Upright Bike | $3,199 | $4,199 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-cu900-upright-bike) | yes |  |
| value | Matrix Lifestyle LED Upright Cycle | $3,700 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Commercial-Exercise-Bikes-C578.aspx) | no (search snippet) | search-index snippet |
| commercial | Star Trac 6UB (LED) | $3,829 | $3,999 | [Fitness Exchange](https://fitnessexchange.com/products/star-trac-6ub-upright-bike) | yes |  variant: Apex LED |
| commercial | Precor UBK 635 (P31) | $3,885 |  | [Push Pedal Pull](https://pushpedalpull.com/products/retail-precor-600-line-upright-bike) | yes |  variant: P31 Console - UBK 635 |
| commercial | LF Club Series+ Upright (SL) | $4,099 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/club-series-plus-upright-lifecycle-bike) | yes |  variant: SL / Black Onyx |
| commercial | LF Integrity S Upright (SL) | $4,207 |  | [LiveFit](https://livefit.com/products/life-fitness-integrity-s-upright-bike-w-sl) | yes |  |
| commercial | Matrix Endurance LED Upright Cycle | $4,890 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Commercial-Exercise-Bikes-C578.aspx) | no (search snippet) | search-index snippet |
| commercial | Life Fitness Integrity Upright SL (compare-at/regular) | $5,406 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/integrity-lifecycle-upright-exercise-bike) | yes | outlet sale $4,324.80 |
| commercial | Matrix Performance LED Upright Cycle | $5,505 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Matrix-Performance-LED-Upright-Cycle-P36886.aspx) | no (search snippet) | search-index snippet; product page also showed $4,830 |
| premium | Precor UBK 835 (P31) | $5,150 |  | [Push Pedal Pull](https://pushpedalpull.com/products/retail-precor-800-line-upright-bike) | yes |  variant: P31 Console - UBK 835 |
| premium | Star Trac 8UB (16" touch) | $9,499 | $10,499 | [Fitness Exchange](https://fitnessexchange.com/products/star-trac-8ub-upright-bike) | yes |  variant: 16" TOUCH |
| premium | Spirit CU1000ENT Upright Bike | $6,300 | $7,300 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-cu000ent-upright-bike) | yes |  |
| premium | Precor UBK 885 Upright Bike (P84) | $9,100 |  | [Top Fitness (Precor dealer)](https://topfitness.com/products/precor-ubk-885-upright-bike-p84) | yes |  |
| premium | Life Fitness Integrity Upright SE4 (compare-at/regular) | $8,651 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/integrity-lifecycle-upright-exercise-bike) | yes | outlet sale $6,920.96 |

### `recumbent_bike`: Recumbent bike

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | Spirit CR800 Recumbent Bike | $2,799 | $3,799 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-cr800-recumbent-bike-1) | yes |  |
| value | Star Trac 4RB (10" LCD) | $2,999 | $3,399 | [Fitness Exchange](https://fitnessexchange.com/products/star-trac-4rb-recumbent-bike) | yes |  variant: 10" LCD |
| value | True Performance Series Recumbent (base) | $2,879 | $3,599 | [Fitness Exchange](https://fitnessexchange.com/products/true-performance-series-recumbent-bike) | yes |  |
| value | Spirit CR900 Recumbent Bike | $3,899 | $4,899 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-cr900-recumbent-bike) | yes |  |
| commercial | Star Trac 6RB (LED) | $4,249 | $4,699 | [Fitness Exchange](https://fitnessexchange.com/products/star-trac-6rb-recumbent-bike) | yes |  variant: Apex LED |
| commercial | Precor RBK 635 (P31) | $3,885 |  | [Push Pedal Pull](https://pushpedalpull.com/products/retail-precor-600-line-recumbent-bike) | yes |  variant: P31 Console - RBK 635 |
| commercial | LF Integrity S Recumbent (SL) | $4,525 |  | [LiveFit](https://livefit.com/products/life-fitness-integrity-s-recumbent-bike-with-sl-final-stock) | yes |  |
| commercial | LF Aspire Recumbent (SL) | $4,737 |  | [The Fitness Outlet](https://thefitnessoutlet.com/products/life-fitness-aspire-lifecycle-recumbent-exercise-bike) | yes |  |
| commercial | Matrix Endurance LED Recumbent | $5,685 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Commercial-Recumbent-Bikes-C163.aspx) | no (search snippet) | search-index snippet; product page showed $4,985 |
| commercial | LF Club Series+ Recumbent (SL) | $5,149 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/club-series-recumbent) | yes |  variant: SL / Black Onyx |
| commercial | Life Fitness Integrity Recumbent SL (compare-at/regular) | $6,055 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/integrity-lifecycle-recumbent-exercise-bike-open-box) | yes | outlet sale $4,844 |
| commercial | Matrix Performance LED Recumbent | $6,555 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Matrix-Performance-LED-Recumbent-P36882.aspx) | no (search snippet) | search-index snippet |
| premium | Precor RBK 835 (P31) | $5,540 |  | [Push Pedal Pull](https://pushpedalpull.com/products/retail-precor-800-line-recumbent-bike) | yes |  variant: P31 Console - RBK 835 |
| premium | Star Trac 8RB (16" touch) | $9,899 | $10,999 | [Fitness Exchange](https://fitnessexchange.com/products/star-trac-8rb-recumbent-bike) | yes |  variant: 16" TOUCH |
| premium | Spirit CR1000ENT Recumbent Bike | $7,100 | $8,100 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-cr1000ent-recumbent-bike) | yes |  |
| premium | Precor RBK 685 Recumbent Bike (P84) | $7,930 |  | [Top Fitness (Precor dealer)](https://topfitness.com/products/precor-rbk-685-recumbent-bike-p84) | yes |  |
| premium | Precor RBK 885 Recumbent Bike (P84) | $9,480 |  | [Top Fitness (Precor dealer)](https://topfitness.com/products/precor-rbk-885-recumbent-bike-p84) | yes |  |
| premium | LF Club Series+ Recumbent (SE4) | $8,750 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/club-series-recumbent) | yes |  variant: SE4 / Black Onyx |

### `indoor_cycle`: Indoor cycle (spin bike)

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | Body-Solid ESB250 Endurance Indoor Cycle Bike (New) | $1,100 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/body-solid-esb250-endurance-indoor-cycle-bike-new) | yes |  |
| value | French Fitness MIC4 Magnetic Indoor Commercial Cycle (New) | $1,499 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/french-fitness-mic4-magnetic-indoor-commercial-cycle-new) | yes |  |
| value | Schwinn IC Classic (base) | $1,569 | $1,729 | [Fitness Exchange](https://fitnessexchange.com/products/schwinn-ic-classic-indoor-cycle) | yes |  |
| value | Spirit CIC850 Indoor Cycle | $2,099 | $2,699 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-cic850-indoor-cycle) | yes |  |
| value | Schwinn SC5 Indoor Cycle | $2,099 | $2,299 | [Fitness Exchange](https://fitnessexchange.com/products/schwinn-sc5-indoor-cycle) | yes |  |
| value | Octane Fitness Surge Indoor Cycle | $2,199 | $2,799 | [Fitness Exchange](https://fitnessexchange.com/products/octane-fitness-surge-indoor-cycle) | yes |  |
| commercial | Life Fitness IC3 | $2,401 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/ic3-indoor-cycle) | yes |  |
| commercial | Schwinn AC Sport | $2,439 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/schwinn-ac-sport-9-7340-wintp0-bike-new) | yes |  |
| commercial | Matrix CXC Indoor Training Cycle | $2,530 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Matrix-CXC-Indoor-Training-Cycle-P33587.aspx) | no (search snippet) | search-index snippet |
| commercial | Keiser Fitness M3 Indoor Bike | $2,660 |  | [The Fitness Outlet](https://thefitnessoutlet.com/products/keiser-m3-indoor-bike) | yes |  |
| commercial | Life Fitness IC5 | $2,947 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/ic5-indoor-cycle) | yes |  |
| commercial | Keiser M3i | $2,985 |  | [The Fitness Outlet](https://thefitnessoutlet.com/products/keiser-m3i-indoor-bike-with-bluetooth) | yes |  |
| premium | Keiser M3i Studio Indoor Bike | $3,120 | $3,320 | [Recovery for Athletes](https://recoveryforathletes.com/products/keiser-m3i-studio-indoor-bike) | yes |  |
| premium | Keiser Fitness M3i Studio Plus Indoor Bike | $3,490 |  | [The Fitness Outlet](https://thefitnessoutlet.com/products/keiser-fitness-m3i-studio-plus-indoor-bike) | yes |  |
| premium | Life Fitness IC6 | $3,493 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/ic6-indoor-cycle) | yes |  |
| premium | Matrix CXP Indoor Training Cycle | $4,180 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Matrix-CXP-Indoor-Training-Cycle--P34810.aspx) | no (search snippet) | search-index snippet |
| premium | Life Fitness IC7 | $4,367 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/ic7-indoor-cycle) | yes |  |
| premium | SportsArt G516 Status Eco-Powr Indoor Cycling Bike (New) | $4,395 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/sportsart-g516-status-eco-powr-indoor-cycling-bike-new) | yes |  |

### `air_bike`: Air (fan) bike

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | AssaultBike Classic | $749 | $799 | [Assault Fitness](https://www.assaultfitness.com/bikes/) | yes | sale $749, regular $799; shown sold out |
| value | AssaultBike Pro X | $899 |  | [Assault Fitness](https://www.assaultfitness.com/bikes/) | yes | shown sold out |
| value | BUILT Strength Air Bike (New) | $899 |  | [CTX Home Gyms](https://ctxhomegyms.com/products/build-air-bike-new) | yes |  |
| value | Rogue Echo Bike V3.0 | $945 |  | [Rogue Fitness](https://www.roguefitness.com/rogue-echo-bike) | yes |  |
| commercial | Hyrox Perform Series Air Bike | $1,199 |  | [Fitness Exchange](https://fitnessexchange.com/products/hyrox-perform-series-air-bike) | yes |  |
| commercial | AssaultBike Elite | $1,499 |  | [Assault Fitness](https://www.assaultfitness.com/bikes/) | yes | also $1,499 at Rogue; 10-yr frame/3-yr parts/1-yr labor |
| commercial | True Vapor ADX Air Bike | $1,499 | $1,799 | [Top Fitness (Precor dealer)](https://topfitness.com/products/true-vapor-adx-air-bike) | yes |  |
| commercial | True Fitness ADX Airdyne Bike | $1,699 | $1,799 | [Fitness Exchange](https://fitnessexchange.com/products/true-fitness-adx-airdyne-bike) | yes |  |
| commercial | Spirit AB950 Air Bike | $2,049 | $2,649 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-ab950-air-bike) | yes |  |
| premium | Renegade Air Bike Unlimited Mag | $2,575 | $2,745 | [Fitness Exchange](https://fitnessexchange.com/products/renegade-air-bike-unlimited-mag) | yes |  |
| premium | Hammer Strength HD Air Bike | $2,784 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/hammer-strength-hd-air-bike) | yes |  |

### `rower`: Rower

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | Rogue Echo Rower | $925 |  | [Rogue Fitness](https://www.roguefitness.com/rogue-echo-rower) | yes |  |
| value | Body-Solid R300 Endurance Rower (New) | $925 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/body-solid-r300-endurance-rower-new) | yes |  |
| value | Concept2 RowErg (standard legs) | $990 |  | [Concept2](https://www.concept2.com/ergs/rowerg) | yes | 5+ units: $940 each; ground shipping $55 (lower 48) |
| commercial | Concept2 RowErg (tall legs) | $1,155 |  | [Concept2](https://www.concept2.com/ergs/rowerg) | yes | 5+ units: $1,105 each; ground shipping $85 (lower 48) |
| commercial | Concept2 RowErg Indoor Rower w/PM5 Console (New) | $1,200 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/concept2-rowerg-indoor-rower-w-pm5-console-new) | yes |  |
| commercial | Life Fitness Row HX | $1,899 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/row-hx-trainer) | yes |  |
| commercial | Octane Fitness Ro Rower | $1,899 | $2,199 | [Fitness Exchange](https://fitnessexchange.com/products/octane-fitness-ro-rower) | yes |  |
| commercial | WaterRower M1 HiRise Rowing Machine | $1,999 |  | [Push Pedal Pull](https://pushpedalpull.com/products/retail-waterrower-m1-hirise-rowing-machine) | yes |  |
| commercial | Matrix Rower (commercial) | $2,720 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Commercial-Rowers-C166.aspx) | no (search snippet) | search-index snippet |
| premium | WaterRower Metallic S1 | $3,099 |  | [LiveFit](https://livefit.com/products/waterrower-metallic-s1) | yes |  |
| premium | Life Fitness Heat Row (Standard) | $3,275 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/heat-row) | yes |  variant: Standard |
| premium | Matrix RXP Rower | $4,030 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Matrix-RXP-Rower-P38331.aspx) | no (search snippet) | search-index snippet; category page showed $4,595 |
| premium | SportsArt G260 Status Eco-Powr Rower (New) | $6,795 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/sportsart-g260-status-eco-powr-rower-new) | yes |  |

### `stair_climber`: Revolving-stair climber (StepMill type)

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | Pro 6 Aspen StairMill Stair Climber (New) | $3,995 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/pro-6-aspen-stairmill-stair-climber-new) | yes |  |
| value | Spirit CSC880 Stairclimber | $5,499 | $6,500 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-csc880-stairclimber) | yes |  |
| value | StairMaster 4G (10" LCD) | $5,999 | $7,099 | [Fitness Exchange](https://fitnessexchange.com/products/stairmaster-4g-stairclimber) | yes |  variant: 10" LCD |
| value | STEPR Pro (base) | $5,999 | $6,999 | [Fitness Exchange](https://fitnessexchange.com/products/stepr-pro-stair-climber) | yes |  |
| commercial | Spirit CSC900 StairClimber | $8,399 | $9,399 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-csc900-stairclimber) | yes |  |
| commercial | StairMaster 8Gx (LED) | $10,099 | $11,199 | [Fitness Exchange](https://fitnessexchange.com/products/stairmaster-8gx-stairclimber) | yes |  variant: LED |
| commercial | Precor StairClimber 835 | $10,440 |  | [Push Pedal Pull](https://pushpedalpull.com/products/retail-precor-stairclimber-836) | yes |  |
| commercial | Matrix Endurance LED ClimbMill | $12,420 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Commercial-Steppers-Climbers-C13887.aspx) | no (search snippet) | search-index snippet |
| premium | Life Fitness Integrity Plus Powermill with SL Console | $13,107 |  | [LiveFit](https://livefit.com/products/life-fitness-integrity-plus-powermill-with-sl-console) | yes |  |
| premium | Stairmaster 10 Series 10G Gauntlet w/ LED Display (New) | $13,349 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/stairmaster-10-series-10g-gauntlet-w-led-display-new) | yes |  |
| premium | Matrix Performance LED ClimbMill | $13,790 |  | [Johnson Fitness & Wellness (Matrix dealer)](https://www.johnsonfitness.com/Matrix-Performance-LED-ClimbMill-P36878.aspx) | no (search snippet) | search-index snippet |
| premium | Precor SCL 885 Stair Climber | $14,670 |  | [Top Fitness (Precor dealer)](https://topfitness.com/products/precor-scl-885-stair-climber) | yes |  |
| premium | Precor SCL 895 Stair Climber | $15,280 |  | [Top Fitness (Precor dealer)](https://topfitness.com/products/precor-scl-895-stair-climber) | yes |  |
| premium | Stairmaster 10 Series 10G Gauntlet w/16" Touch Display (New) | $17,649 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/stairmaster-10-series-10g-gauntlet-w-16-touch-display-new) | yes |  |

### `ski_erg`: Ski erg

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | Rogue Echo Ski (no stand) | $825 |  | [Rogue Fitness](https://www.roguefitness.com/rogue-echo-ski) | yes | JSON-LD offers $825-$995 |
| value | Concept2 SkiErg (wall-mount, no stand) | $850 |  | [Concept2](https://www.concept2.com/ergs/skierg) | yes | 5+ units $810 each |
| value | BUILT Strength Ski Machine (New) | $899 |  | [CTX Home Gyms](https://ctxhomegyms.com/products/built-strength-ski-machine-new) | yes |  |
| commercial | Concept2 SkiErg + standard floor stand | $1,070 |  | [Rogue Fitness](https://www.roguefitness.com/concept-2-skierg-2) | yes | = $850 + $220 stand (Concept2 list); also Power Systems $1,070 |
| commercial | Concept2 Skierg w/ PM5 Console (New) | $1,199 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/concept2-skierg-w-pm5-console-new) | yes |  |
| premium | Throwdown HIIT Ski 9-4890-KINTP0 (New) | $1,654 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/throwdown-hiit-ski-9-4890-kintp0-new) | yes |  |
| premium | TKO AirRaid Ski Trainer | $1,700 | $1,870 | [LiveFit](https://livefit.com/products/tko-airraid-ski-trainer) | yes |  |
| premium | Stepr Ski XL | $2,499 |  | [Fitness Exchange](https://fitnessexchange.com/products/stepr-ski-xl) | yes |  |

### `recumbent_stepper`: Seated total-body recumbent stepper

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | Spirit CRS800S Recumbent Stepper | $4,799 | $5,799 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-crs800s-recumbent-stepper-2020) | yes |  |
| value | Spirit 7.0S Recumbent Stepper | $4,800 | $5,800 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-7-0s-recumbent-stepper-1) | yes |  |
| value | NuStep T4r | $5,095 |  | [Fitness Exchange](https://fitnessexchange.com/products/nustep-t4r-recumbent-crosstrainer) | yes |  |
| commercial | Spirit 7.5S Recumbent Stepper | $5,400 | $6,400 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-7-5s-recumbent-stepper) | yes |  |
| commercial | NuStep T5 | $7,295 |  | [Fitness Exchange](https://fitnessexchange.com/products/nustep-t5-recumbent-crosstrainer) | yes |  |
| commercial | SciFit StepOne (base) | $7,400 |  | [Fitness Exchange](https://fitnessexchange.com/products/scifit-stepone-recumbent-stepper) | yes |  |
| commercial | SciFit StepOne (LF shop) | $7,655 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/stepone-recumbent-stepper-prem-seat-cool-gray) | yes |  |
| commercial | NuStep T5XR | $7,695 |  | [Fitness Exchange](https://fitnessexchange.com/products/nustep-t5xr-recumbent-crosstrainer) | yes |  |
| premium | NuStep T6 Pro | $7,595 |  | [Push Pedal Pull](https://pushpedalpull.com/products/retail-nustep-t6-pro) | yes |  |
| premium | NuStep T6 (base) | $7,595 |  | [Fitness Exchange](https://fitnessexchange.com/products/nustep-t6-recumbent-crosstrainer) | yes |  |
| premium | NuStep T5XRW | $7,895 |  | [Fitness Exchange](https://fitnessexchange.com/products/nustep-t5xrw-recumbent-crosstrainer-1) | yes |  |
| premium | Spirit Fitness 8.5S Recumbent Stepper | $7,948 | $8,950 | [Fitness Exchange](https://fitnessexchange.com/products/spirit-fitness-8-5s-recumbent-stepper) | yes |  |

### `rig_bay`: Rig bay (one bay of a pull-up/functional rig)

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | REP Rig 4000 14ft (3 bays) per bay | $812 |  | [REP Fitness](https://www.repfitness.com/products/rig-pre-selected) | yes | $2,434.99 / 3 bays; 8 uprights, 6ft deep, 108in tall |
| value | REP Rig 4000 20ft (4 bays) per bay | $745 |  | [REP Fitness](https://www.repfitness.com/products/rig-pre-selected) | yes | $2,979.99 / 4 bays; 10 uprights |
| value | REP Rig 4000 24ft (5 bays) per bay | $714 |  | [REP Fitness](https://www.repfitness.com/products/rig-pre-selected) | yes | $3,570.99 / 5 bays; 12 uprights |
| value | REP Rig 5000 14ft (3 bays) per bay | $860 |  | [REP Fitness](https://www.repfitness.com/products/rig-pre-selected) | yes | $2,579.99 / 3 bays |
| commercial | Rogue Monster Lite Rig 2.0 Base ML-14 (3 bays) per bay | $1,017 |  | [Rogue Fitness](https://www.roguefitness.com/monster-lite-rig-2-0) | yes | $3,050 / 3 bays (4+6+4 ft) |
| commercial | Rogue Monster Lite Rig 2.0 Base ML-20 (4 bays) per bay | $875 |  | [Rogue Fitness](https://www.roguefitness.com/monster-lite-rig-2-0) | yes | $3,500 / 4 bays |
| commercial | Rogue Monster Rig 2.0 Base M-14 (3 bays) per bay | $1,065 |  | [Rogue Fitness](https://www.roguefitness.com/monster-rig-2-0) | yes | $3,195 / 3 bays |
| commercial | Rogue Monster Rig 2.0 Base M-20 (4 bays) per bay | $930 |  | [Rogue Fitness](https://www.roguefitness.com/monster-rig-2-0) | yes | $3,720 / 4 bays |
| commercial | Rogue Monster Rig 2.0 Standard M-14 (3 bays) per bay | $1,182 |  | [Rogue Fitness](https://www.roguefitness.com/monster-rig-2-0) | yes | $3,545 / 3 bays |
| commercial | Rogue Monster Rig 2.0 Standard M-24 (5 bays) per bay | $999 |  | [Rogue Fitness](https://www.roguefitness.com/monster-rig-2-0) | yes | $4,995 / 5 bays |
| premium | Throwdown XTC Compact 2x4 (1 bay + attachments) | $2,810 | $3,049 | [Fitness Exchange](https://fitnessexchange.com/products/throwdown-2-x-4-compact-xtc-rig) | yes |  |
| premium | Throwdown XTC Compact 4x4 (1 bay + attachments) | $4,006 | $4,299 | [Fitness Exchange](https://fitnessexchange.com/products/throwdown-4-x-4-compact-xtc-rig) | yes |  |
| premium | Throwdown XTC Standard 4x14 per bay (approx. 3 bays incl. attachments) | $3,983 |  | [Fitness Exchange](https://fitnessexchange.com/products/throwdown-4-x-14-standard-xtc-rig) | yes | $11,950 rig with ~17 attachments / ~3 bays (bay count inferred from 14 ft length and 4 ft crossmembers) |

### `turf_lane`: Turf sled/sprint lane

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | French Fitness V1 turf roll 6.5x82 ft (533 sq ft) | $669 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/french-fitness-artificial-grass-synthetic-lawn-turf-flooring-roll-82-x-6-5-v1-base) | yes |  |
| value | French Fitness V2 turf roll 6.5x82 ft (533 sq ft) | $899 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/french-fitness-artificial-grass-synthetic-lawn-turf-flooring-roll-82-x-6-5-v2-plus) | yes |  |
| value | French Fitness V3 turf roll 6.5x82 ft (533 sq ft) | $1,099 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/french-fitness-artificial-grass-synthetic-lawn-turf-flooring-roll-82-x-6-5-v3-premium) | yes |  |
| value | Bells of Steel turf roll 6.56x82 ft (538 sq ft) | $1,906 |  | [Bells of Steel](https://www.bellsofsteel.us/products/turf-roll) | yes |  |
| commercial | Rogue GymTurf (Dollamur) 5x50 ft (250 sq ft) | $1,924 |  | [Rogue Fitness](https://www.roguefitness.com/gymturf) | yes | 5 ft wide, 5/8in foam backing; 5x25 ft = $1,089 |
| commercial | French Fitness 14x50 ft turf track (2 lanes) per lane | $2,350 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/french-fitness-artificial-performance-gym-turf-track-w-start-marker-14-ft-x-50-ft-new) | yes | $4,699 for 700 sq ft, two marked lanes |
| premium | ECORE RageTurf Rally tile, 6.5x50 ft lane (325 sq ft) | $3,426 | $4,490 | [Blue Sky Fit Supply](https://blueskyfitsupply.com/products/ecore-rageturf-rally-interlocking-tile-12mm-athletic-turf) | yes | tile 23x46in (7.35 sq ft) $77.45 sale / $101.50 list -> $10.54-$13.81/sq ft |
| premium | ECORE RageTurf UltraTile 1in, 6.5x50 ft lane (325 sq ft) | $5,237 | $6,866 | [Blue Sky Fit Supply](https://blueskyfitsupply.com/products/ecore-rageturf-ultratile-1-athletic-turf-tile) | yes | tile 24x24in $64.45 sale / $84.50 list -> $16.11-$21.13/sq ft |

### `sled`: Push/pull sled

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | Titan High-Low Push-Pull Sled | $215 | $255 | [Titan Fitness](https://titan.fitness/products/high-low-push-pull-sled) | yes |  |
| value | Rogue Slice Sled | $220 |  | [Rogue Fitness](https://www.roguefitness.com/rogue-slice-sled) | yes | JSON-LD $220-$270 |
| value | Rogue Echo Dog Sled | $290 |  | [Rogue Fitness](https://www.roguefitness.com/rogue-echo-dog-sled) | yes | JSON-LD $290-$345 |
| value | French Fitness Push / Pull Weight Sled V2 (New) | $349 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/french-fitness-push-pull-weight-sled-v2-new) | yes |  |
| value | Body-Solid GWS100 Weight Sled (New) | $340 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/body-solid-gws100-weight-sled-new) | yes |  |
| commercial | Rogue Dog Sled | $335 |  | [Rogue Fitness](https://www.roguefitness.com/rogue-dog-sled) | yes | JSON-LD $335-$355 |
| commercial | Granite Series Training Sled | $380 |  | [Power Systems](https://powersystems.com/products/granite-series-sled) | yes |  |
| commercial | Centr x HYROX Official Competition Power Sled | $435 |  | [LiveFit](https://livefit.com/products/centr-x-hyrox-official-competition-power-sled) | yes |  |
| commercial | Rogue Alpaca Sled | $440 |  | [Rogue Fitness](https://www.roguefitness.com/rogue-alpaca-sled) | yes | JSON-LD $440-$500 |
| commercial | Life Fitness Push-Pull Sled (base+handles) | $825 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/push-pull-weight-sled) | yes |  variant: Base + Handles |
| commercial | Torque TANK M1 | $849 |  | [Torque Fitness](https://www.torquefitness.com/products/tank-m1-push-sled) | yes |  |
| commercial | Legend Fitness 3262 Pro Series Push/Pull Power Sled | $909 | $1,059 | [Blue Sky Fit Supply](https://blueskyfitsupply.com/products/legend-fitness-3262-pro-series-push-pull-power-sled) | yes |  |
| premium | Torque TANK M4 | $1,799 |  | [Torque Fitness](https://www.torquefitness.com/products/tanktm-m4) | yes |  |
| premium | Torque TANK M3 | $1,799 |  | [Torque Fitness](https://www.torquefitness.com/products/tank-m3) | yes |  |
| premium | Torque TANK MX | $2,499 |  | [Torque Fitness](https://www.torquefitness.com/products/tank-mx) | yes |  |
| premium | Torque TANK SX | $2,699 |  | [Torque Fitness](https://www.torquefitness.com/products/tank-sx-push-sled) | yes |  |

### `plyo_box_set`: Plyo box set (covering ~12-30 in)

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | REP 3-in-1 Soft Plyo Box Medium + Large | $355 |  | [REP Fitness](https://www.repfitness.com/products/3-in-1-soft-plyo-boxes) | yes | Medium $129.99 + Large $224.99 |
| value | Titan 3-in-1 Soft Foam Plyo Box x2 | $272 |  | [Titan Fitness](https://titan.fitness/products/3-in-1-soft-foam-plyometric-box-20-in-24-in-30-in) | yes | 2 x $135.97 (sale; list $209.99) |
| value | Torque X-Impact TriplePlyo 20-24-30 | $490 |  | [Torque Fitness](https://www.torquefitness.com/products/tripleplyo®) | yes |  |
| value | American Barbell steel stackable set 12/18/24/30 | $515 |  | [American Barbell](https://www.americanbarbell.com/products/steel-plyometric-box-set-of-12-18-24-30) | yes |  |
| value | Body-Solid Plyometric Box Set 12", 18", 24" & 30" | $764 |  | [Fitness Exchange](https://fitnessexchange.com/products/body-solid-plyometric-box-set-12-18-24-30) | yes |  |
| commercial | REP Stackable Soft Foam Plyo full set | $1,060 |  | [REP Fitness](https://www.repfitness.com/products/stackable-soft-foam-plyo-box) | yes |  variant: Full Set |
| commercial | Rogue Foam Games Box x3 | $825 |  | [Rogue Fitness](https://www.roguefitness.com/rogue-foam-games-box) | yes | 3 x $275 |
| commercial | Torque X-Impact Plyostack set 6-24in | $1,292 |  | [Torque Fitness](https://www.torquefitness.com/products/x-impact-plyostack-set) | yes |  |
| commercial | Troy Foam Stackable Plyo Box Set #TPLYOPAC | $1,516 |  | [Fitness Exchange](https://fitnessexchange.com/products/troy-foam-stackable-plyo-box-set-tplyopac) | yes |  |
| premium | Legend Fitness 3134 Plyo Box Set | $1,939 | $2,279 | [Blue Sky Fit Supply](https://blueskyfitsupply.com/products/legend-fitness-3134-plyo-box-set) | yes |  |
| premium | Powermax Soft Plyoboxes Set of 5 | $2,193 |  | [elitefts](https://www.elitefts.com/products/powermax-soft-plyoboxes-set-of-5) | yes |  |
| premium | Power Systems Plyo-Safe G2 (base) | $1,900 |  | [Power Systems](https://powersystems.com/products/plyo-safe-g2-plyo-blocks) | yes |  |
| premium | Hammer Strength Stackable Plyo set 3-24in | $3,135 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/hammer-strength-stackable-plyo-box) | yes |  variant: Set: 3-24" |

### `wall_ball_station`: Wall-ball station (1 target + 3 balls 10/14/20 lb)

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | REP target + REP Medicine Balls 2.0 (10/14/20) | $333 |  | [REP Fitness](https://www.repfitness.com/products/medicine-ball-2-0) | yes | target $99.99 (repfitness.com/products/wall-ball-targets) + $69.99 + $77.99 + $84.99 |
| value | Fringe target plate + Torque Light wall ball package (8/14/20) | $314 |  | [Torque Fitness / Fringe Sport](https://www.torquefitness.com/products/4-ft-wall-ball-package) | yes | Fringe single target plate $74 + Torque 3-ball package $240 |
| commercial | Fringe target w/ post + Fringe Immortal (10/14/20) | $446 |  | [Fringe Sport](https://www.fringesport.com/products/immortal-medicine-ball) | yes | $119 target + $89 + $109 + $129 |
| commercial | Rogue Double Wall Ball Target + Rogue Medicine Balls (10/14/20) | $475 |  | [Rogue Fitness](https://www.roguefitness.com/rogue-medicine-balls) | yes | $120 target + $105 + $115 + $135 |
| premium | Rogue target + Escape Endura wall balls (10/14/20, Life Fitness) | $771 |  | [Life Fitness / Rogue](https://shop.lifefitness.com/products/escape-endura-wall-balls) | yes | $120 + $205 + $216 + $230 |
| premium | Rogue target + Torque complete 5-ball package (12-20 lb) | $540 |  | [Torque Fitness / Rogue](https://www.torquefitness.com/products/6-ft-wall-ball-package) | yes | $120 + $420 |

### `battle_rope_station`: Battle-rope station (rope + anchor)

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | REP Sleeve Battle Rope 1.5in x 50ft + REP wall anchor | $145 |  | [REP Fitness](https://www.repfitness.com/products/sleeve-battle-rope) | yes |  |
| value | Bells of Steel Battle Rope 1.5in x 40ft + REP strap anchor | $148 |  | [Bells of Steel / REP](https://www.bellsofsteel.us/products/battle-rope) | yes |  |
| value | French Fitness 2in x 40ft rope + REP wall anchor | $174 |  | [Fitness Superstore / REP](https://fitnesssuperstore.com/products/french-fitness-training-battle-rope-2-in-x-40-ft-new) | yes |  |
| commercial | REP Sleeve Battle Rope 2in x 50ft + Fringe wall anchor | $244 |  | [REP Fitness / Fringe Sport](https://www.repfitness.com/products/sleeve-battle-rope) | yes |  |
| commercial | Torque Battle Rope 30ft x 2in + Fringe wall anchor | $262 |  | [Torque Fitness / Fringe Sport](https://www.torquefitness.com/products/battle-rope-30-ft-2-in) | yes |  |
| commercial | Power Systems Covered Battle Rope (top variant) + Fringe anchor | $329 |  | [Power Systems / Fringe Sport](https://powersystems.com/products/covered-battle-rope) | yes | Covered Battle Rope listed $195-$275 |
| premium | elitefts FUEL Pureformance Battle Rope 50ft + American Barbell rope anchor | $412 |  | [elitefts / American Barbell](https://www.elitefts.com/products/fuel-pureformance-battle-rope) | yes |  |
| premium | Centr x HYROX Official Competition Power Rope + American Barbell anchor | $340 |  | [LiveFit / American Barbell](https://livefit.com/products/centr-x-hyrox-official-competition-power-rope) | yes |  |

### `suspension_trainer_station`: Suspension-trainer station (strap + mount)

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | Bells of Steel Human Trainer (low variant) + ceiling mount | $130 |  | [Bells of Steel](https://www.bellsofsteel.us/products/human-trainer-bodyweight-suspension-system) | yes | Human Trainer $99.99-$199.99; ceiling mount $29.99 |
| value | Bells of Steel Human Trainer (high variant) + ceiling mount | $230 |  | [Bells of Steel](https://www.bellsofsteel.us/products/human-trainer-bodyweight-suspension-system) | yes |  |
| commercial | TRX Commercial Suspension Trainer + TRX X-Mount | $290 |  | [Fitness Exchange](https://fitnessexchange.com/products/trx-commercial-suspension-trainer) | yes |  |
| commercial | TRX PRO4 System + TRX X-Mount | $335 |  | [TRX Training](https://www.trxtraining.com/products/pro) | yes | PRO4 regular $289.95 (sale $217.46) |
| premium | TRX Commercial ST + 1/8 share of Legend 3905 Suspension Trainer Rig | $445 |  | [Blue Sky Fit Supply / Fitness Exchange](https://blueskyfitsupply.com/products/legend-fitness-3905-suspension-trainer-rig) | yes | Legend rig $1,559 (8 eyelet connection points) |
| premium | TRX PRO4 + 1/6 share of TRX MultiMount | $423 |  | [Fitness Exchange / TRX](https://fitnessexchange.com/products/trx-multimount) | yes | MultiMount $799 supports up to 9 trainers; 6 assumed |

### `heavy_bag`: Heavy bag station (bag + mount)

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | TITLE Made in USA 100lb Punching Bag + hanger/spring bundle | $310 |  | [TITLE Boxing](https://www.titleboxing.com/products/title-boxing-made-in-the-usa-100lb-punching-bag) | yes | bag $269.99 (list $349.99) |
| value | French Fitness 100 lb heavy bag + FF hanger attachment | $378 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/french-fitness-heavy-punching-bag-100-lb-new) | yes |  |
| value | Everlast 100lb Elite Pro Heavy Bag (high variant) + universal hanger | $263 |  | [Everlast](https://www.everlast.com/products/100lb-elite-pro-heavy-bag) | yes |  |
| commercial | WBC by TITLE Made in USA 100lb + Club chain system 4.0 + USA wall-mount hanger | $750 |  | [TITLE Boxing](https://www.titleboxing.com/products/wbc-by-title-boxing-made-in-usa-100lb-heavy-bag) | yes |  |
| commercial | PowerForce Heavy Bag and Stand Combo | $688 |  | [Power Systems](https://powersystems.com/products/powerforce-hanging-bag-with-stand) | yes |  |
| commercial | Throwdown 6 ft Heavy Bag + TITLE wall-mount hanger | $548 |  | [Fitness Superstore / TITLE](https://fitnesssuperstore.com/products/throwdown-6-ft-heavy-bags-td-hb-6-new) | yes |  |
| premium | Life Fitness Heavy Bag + TITLE wall-mount hanger | $1,039 |  | [Life Fitness / TITLE](https://shop.lifefitness.com/products/life-fitness-heavy-bag) | yes |  |
| premium | Everlast 1910 Pro 100lb Leather + TITLE wall-mount hanger | $1,000 |  | [Everlast / TITLE](https://www.everlast.com/products/1910-pro-100lb-leather-heavy-punching-bag) | yes |  |
| premium | Throwdown FreeStanding Punching Bag | $1,396 | $1,499 | [The Fitness Outlet](https://thefitnessoutlet.com/products/throwdown-freestanding-punching-bag) | yes |  |

### `stretch_area`: Stretch area

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | Body-Solid BSTFM20 hanging mat + 1/6 Body-Solid mat hanger | $43.61 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/body-solid-bstfm20-hanging-exercise-mat-new) | yes |  |
| value | French Fitness 15mm hanging yoga mat + 1/6 FF mat hanger | $41.50 |  | [Fitness Superstore](https://fitnesssuperstore.com/products/french-fitness-15mm-extra-thick-hanging-yoga-mat-new) | yes |  |
| commercial | Life Fitness Core Mat 0.59in + 1/8 LF wall mat rack | $98.38 |  | [Life Fitness](https://shop.lifefitness.com/products/core-mats) | yes |  |
| commercial | AIREX Fitness Mat (top variant) + 1/8 LF wall mat rack | $112 |  | [Power Systems / Life Fitness](https://powersystems.com/products/airex-mat) | yes | AIREX listed $71.25-$102.50 |
| premium | Element 4x6 ft exercise mat (floor zone) | $129 |  | [LiveFit](https://livefit.com/products/element-fitness-4x6-exercise-mat) | yes |  |
| premium | Power Systems Premium Gym Mat (top variant) | $210 |  | [Power Systems](https://powersystems.com/products/premium-gym-mat) | yes | listed $149.50-$209.50 |
| premium | Fitness Exchange 4x6 heavy-duty large gym mat | $170 |  | [Fitness Exchange](https://fitnessexchange.com/products/4-x-6-heavy-duty-large-home-gym-mat-24gs) | yes |  |

### `accessory_pack`: Accessory pack (5 mini bands, 4 loop bands, 4 rollers, 4 mats, 2 stability balls, storage)

| Tier | Model / bundle | Price | List (compare-at) | Source (publisher) | Fetched | Note |
|---|---|---|---|---|---|---|
| value | Body-Solid/GoFit/French Fitness bundle | $482 |  | [Fitness Superstore / Fitness Exchange](https://fitnesssuperstore.com/) | yes | mini-band 5-pk $13; BS bands $14.95/$19.95/$32.95/$42.95; 2x BS 36in roller $44.95 + 2x GoFit 18in $21.99; 4x BS hanging mat $39.95; FF balls $20+$18; FF mat hanger $27 |
| commercial | Life Fitness accessory bundle | $1,112 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/) | yes | LF mini power bands set $120; power bands 0.5-1.75in $146; 2x roller $59 + 2x hard roller $69; 4x core mat $89; 2x stability ball avg $79.50; wall mat rack $75 |
| premium | Life Fitness bundle + LF Accessory Rack (additional storage) | $3,866 |  | [Life Fitness (shop.lifefitness.com)](https://shop.lifefitness.com/products/life-fitness-accessory-rack) | yes | as commercial but Hammer Strength stability balls $161 and LF Accessory Rack $2,666 instead of $75 mat rack |

## 4. Freight, delivery and installation

| Evidence | Value | Source |
|---|---|---|
| Concept2 RowErg ground shipping, lower 48 (parcel, self-assembly) | $55 standard legs / $85 tall legs = 5.6% / 7.4% of $990 / $1,155; Canada $100/$140 | [Concept2](https://www.concept2.com/ergs/rowerg) |
| Concept2 volume pricing | 5+ pieces: RowErg $990 -> $940, SkiErg $850 -> $810 (about 5% off); 10+ pieces may get shipping discounts by quote | [Concept2](https://www.concept2.com/ergs/rowerg) |
| Hoist "Assembly & White Glove Installation" add-ons (17 products) | $100-$800 per product; 5.7-20.5% of list price, median 10.2%. Cycling bikes: $250-$300 (10.2-20.5%) | [Hoist Fitness store](https://www.hoistfitness.com/) |
| iSellFitness installation service products | Treadmill / elliptical / recumbent $399; indoor cycle $299; rower $349; Smith machine $499; leg press $600 | [iSellFitness](https://isellfitness.com/products/treadmill-assembly-set-up-installation-service) |
| Fitness Exchange delivery & assembly fee ladder (local, within 49 mi) | $199 (items $0-999), $249 ($1,000-1,999), $299 ($2,000-2,999), $349 ($3,000-3,999), $399 ($4,000-4,999), $599 ($5,000-5,999), $499 ($6,000-9,999). That is 5-12% for $3k-$10k cardio | [Fitness Exchange](https://fitnessexchange.com/products/delivery-installation-6000-9999) |
| Life Fitness haul-away of old unit | $177 per unit (treadmill / elliptical / bike / strength); must be bought with installed equipment | [Life Fitness](https://shop.lifefitness.com/products/white-glove-installation-add-on-haul-away) |
| The Fitness Outlet delivery options | Liftgate only $65; threshold delivery $109 | [The Fitness Outlet](https://thefitnessoutlet.com/products/delivery-services) |
| Johnson Fitness (Matrix) delivery | Policy page: "Delivery & Installation - $249.00 - $549.00"; Matrix CXC page: delivery & assembly $229 (9.1% of $2,530); older commercial page $199 installed / $149 threshold | [Johnson Fitness policies](https://www.johnsonfitness.com/Policies) (search snippet, fetched=false) |
| NTAI Fitness gym equipment cost estimator (vendor blog) | "Installation and shipping commonly add 12-20% on top of the equipment number"; "Installation adds 8-15%"; "Shipping to a major metro costs $500-$1,500 per pallet"; rural $2,000-$4,000 | [ntaifitness.com](https://www.ntaifitness.com/tools/gym-equipment-cost-estimator/) |
| Aira Fitness 2025 FDD Item 7 (via fdd.ninja) | Freight & delivery of initial equipment package $1,000-$10,000 against a package of $9,300-$130,165 (about 8-11% at matched ends) | [fdd.ninja](https://www.fdd.ninja/brands/aira_fitness/2025/pay_freight_delivery_costs_initial_equipment_package_franchise) (fetched=false) |
| The Exercise Coach FDD (via sharpsheets) | Shipping, installation and setup $7,000-$9,000 vs equipment package $10,000-$81,000 | [sharpsheets.io](https://sharpsheets.io/?p=26165) (fetched=false) |
| Rogue rig anchoring hardware | Rogue Rig Concrete Anchor Kit $35 (18 anchors for 10 ft rig ... 36 for 24 ft rig); rigs must be bolted to floor or skid plates | [Rogue](https://www.roguefitness.com/monster-rig-2-0) |

**Recommended model values (derived estimates):**
- Cardio, delivered and installed by a commercial dealer: **8% of equipment cost** (range 5-15%), with a floor of about **$250 per installed unit**. Basis: Hoist median 10.2%; Fitness Exchange ladder 5-8% for $6k-$10k units; iSellFitness $399 on a $10.3k treadmill is 3.9%; FDD freight about 8-11%.
- Non-motorized, parcel-shipped cardio (rower, ski erg, air bike): **7%** (range 5-10%). Basis: Concept2 shipping 5.6-7.4%; self-assembly assumed.
- Functional rigs and turf (multi-pallet LTL freight plus anchoring or adhesive): **12%** (range 8-20%). Basis: NTAI 12-20% landed-cost guidance and $500-$1,500 per pallet.
- Small functional goods (ropes, balls, mats, boxes, straps): **6%** (range 0-10%). Many retailers ship these free; parcel otherwise.
- Whole-project planning default: **10%** of the equipment subtotal.

## 5. Refurbished / remanufactured discount vs new

| Model pair | Reman price | New price | Discount | Reman source | New source |
|---|---|---|---|---|---|
| Life Fitness Integrity Treadmill SE3 HD | $5,299 | $13,059 | 59.4% | [link](https://fitnesssuperstore.com/products/life-fitness-integrity-treadmill-w-se3-hd-treadmill-remanufactured) | [LF shop regular (compare-at) price](https://shop.lifefitness.com/products/integrity-treadmill) |
| Life Fitness Integrity CLST treadmill vs current Integrity SL | $2,395 | $7,425 | 67.7% | [link](https://ctxhomegyms.com/products/life-fitness-clst-integrity-series-treadmill-remanufactured-1) | [LF shop regular (compare-at) Integrity SL](https://shop.lifefitness.com/products/integrity-treadmill-outlet) |
| StairMaster 10G (reman) vs 10G LED new | $4,995 | $13,349 | 62.6% | [link](https://ctxhomegyms.com/products/stairmaster-10-series-10g-gauntlet-stepmill-remanufactured) | [Fitness Superstore new](https://fitnesssuperstore.com/products/stairmaster-10-series-10g-gauntlet-w-led-display-new) |
| StairMaster 8G 10in touch (reman) vs 8Gx LED new | $4,995 | $10,099 | 50.5% | [link](https://ctxhomegyms.com/products/stairmaster-8g-gauntlet-stepmill-w-10-touchscreen-console-remanufactured) | [Fitness Exchange new](https://fitnessexchange.com/products/stairmaster-8gx-stairclimber) |
| Star Trac 10 FreeRunner 19in (reman) vs 20in new | $7,299 | $16,999 | 57.1% | [link](https://fitnesssuperstore.com/products/star-trac-10-series-freerunner-treadmill-w-19-embedded-display-remanufactured) | [Fitness Superstore new](https://fitnesssuperstore.com/products/star-trac-10-series-freerunner-treadmill-w-20-embedded-display-new) |
| Matrix Performance Treadmill TouchXL | $5,495 | $20,020 | 72.6% | [link](https://ctxhomegyms.com/products/matrix-performance-treadmill-w-touch-xl-console-remanufactured) | [Johnson Fitness list (search snippet)](https://www.johnsonfitness.com/Matrix-Performance-TouchXL-Treadmill-P36852.aspx) |
| Matrix Performance ClimbMill TouchXL | $7,495 | $23,120 | 67.6% | [link](https://ctxhomegyms.com/products/matrix-performance-climbmill-w-touch-xl-console-remanufactured) | [Johnson Fitness list (search snippet)](https://www.johnsonfitness.com/Commercial-Steppers-Climbers-C13887.aspx) |
| NuStep T5XR | $4,895 | $7,695 | 36.4% | [link](https://ctxhomegyms.com/products/nustep-t5xr-cross-trainer-remanufactured) | [Fitness Exchange new](https://fitnessexchange.com/products/nustep-t5xr-recumbent-crosstrainer) |
| NuStep T4r | $2,995 | $5,095 | 41.2% | [link](https://ctxhomegyms.com/products/nustep-t4r-recumbent-cross-trainer-remanufactured) | [Fitness Exchange new](https://fitnessexchange.com/products/nustep-t4r-recumbent-crosstrainer) |
| Keiser M3 indoor cycle | $999 | $2,660 | 62.4% | [link](https://ctxhomegyms.com/products/keiser-m3-indoor-cycle-remanufactured-1) | [The Fitness Outlet new](https://thefitnessoutlet.com/products/keiser-m3-indoor-bike) |
| AssaultBike Elite | $549 | $1,499 | 63.4% | [link](https://ctxhomegyms.com/products/assault-air-bike-elite-remanufactured) | [Assault Fitness new](https://www.assaultfitness.com/bikes/) |
| Rogue Echo Bike (Rogue refurbished) | $595 | $945 | 37.0% | [link](https://www.roguefitness.com/rogue-echo-bike-refurbished) | [Rogue new](https://www.roguefitness.com/rogue-echo-bike) |
| Precor EFX 885 (P82 reman) vs EFX 885 P84 new | $2,995 | $14,130 | 78.8% | [link](https://ctxhomegyms.com/products/precor-efx-885-commercial-cross-trainer-w-p82-console-remanufactured) | [Top Fitness new](https://topfitness.com/products/precor-efx-885-elliptical-p84) |
| Precor RBK 835 (P30 reman) vs RBK 835 P31 new | $1,995 | $5,540 | 64.0% | [link](https://ctxhomegyms.com/products/precor-rbk-835-recumbent-bike-w-p30-console-remanufactured) | [Push Pedal Pull new](https://pushpedalpull.com/products/retail-precor-800-line-recumbent-bike) |
| Precor UBK 885 (P82 reman, Fitness Superstore) vs UBK 885 P84 new | $3,799 | $9,100 | 58.3% | [link](https://fitnesssuperstore.com/products/precor-ubk-885-upright-bike-w-p82-console-remanufactured) | [Top Fitness new](https://topfitness.com/products/precor-ubk-885-upright-bike-p84) |
| Woodway 4Front (reman, CTX) vs new w/19in TV | $5,995 | $17,999 | 66.7% | [link](https://ctxhomegyms.com/products/woodway-4front-treadmill-remanufactured) | [Total Fitness USA new](https://tfusa.net/products/woodway-4front-treadmill-with-19-tv) |
| Woodway 4Front ProSmart (reman, FSS) vs new ProSmart | $10,499 | $19,600 | 46.4% | [link](https://fitnesssuperstore.com/products/woodway-4front-treadmill-w-21-prosmart-console-remanufactured) | [Total Fitness USA new](https://tfusa.net/products/woodway-4ftont-treadmill-with-prosmart-touch-screen) |
| Life Fitness Integrity CLSU upright vs Integrity SL upright | $999 | $5,406 | 81.5% | [link](https://ctxhomegyms.com/products/life-fitness-integrity-series-clsu-upright-bike-remanufactured) | [LF shop regular (compare-at)](https://shop.lifefitness.com/products/integrity-lifecycle-upright-exercise-bike) |
| Concept2 Model E (reman) vs RowErg tall legs new | $749 | $1,155 | 35.2% | [link](https://ctxhomegyms.com/products/concept2-model-e-indoor-rower-remanufactured) | [Concept2 new](https://www.concept2.com/ergs/rowerg) |
| Matrix Performance Upright Touch | $2,495 | $13,280 | 81.2% | [link](https://ctxhomegyms.com/products/matrix-performance-upright-cycle-w-touch-console-remanufactured) | [Johnson Fitness list (search snippet)](https://www.johnsonfitness.com/Commercial-Exercise-Bikes-C578.aspx) |
| Precor StretchTrainer C240i (reman) vs StretchTrainer new | $1,249 | $1,270 | 1.7% | [link](https://fitnesssuperstore.com/products/precor-c240i-stretch-trainer-remanufactured) | [Push Pedal Pull new](https://pushpedalpull.com/products/retail-precor-stretchtrainer) |

Pair statistics: n=21, median **62.4%**, mean 56.7%, IQR 43.8-67.7%, range 1.7-81.5%.

Published claims (not independently verified): Fitness Superstore says remanufactured equipment is "30-70% below MSRP" (Octane category page); its About page says 30-60% and its buyer guides 40-70%. CTX Home Gyms says "typically 40-60% off new commercial pricing". Athletic Business reports savings "of about 70 percent compared to the cost of new equipment". Club Solutions quotes a dealer at "between 30 and 50 percent". These all come from search snippets (fetched=false).

Life Fitness outlet (new/open-box) pricing seen 2026-10-28 is a separate "near-new" channel: Integrity Treadmill SE3 HD $7,183 vs $13,059 regular (45% off); ST console $5,627 vs $9,379 (40% off); SL $5,940 vs $7,425 (20% off); Integrity upright and recumbent bikes 20% off.

Interpretation: the pairs compare remanufactured *previous-generation* units with *current* MSRP or dealer prices. Dealers often discount new commercial cardio 10-20% below compare-at: Fitness Exchange shows Star Trac at about 10% and Spirit at about 20-30% under compare-at. Large club orders can be negotiated lower again. Measured against realistic new street prices, the remanufactured discount is therefore lower than the pair median.

**Recommended model values:** branded commercial cardio refurbished = **50% of new typical price** (range 35-70%). Simple self-powered machines (air bike, rower, ski erg, recumbent stepper) = **40%** (range 35-63%; Echo Bike 37%, Concept2 35%, NuStep 36-41%, Assault Elite 63%). Functional steel and soft goods: **do not model a refurbished channel**. The market is thin, and the only matched simple product, the Precor StretchTrainer, was just 1.7% cheaper remanufactured.

## 6. Useful life and annual maintenance

Evidence:
- Planet Fitness 10-K FY2018: "all franchisees are required to replace their existing equipment with new equipment every five to seven years." The FY2023 10-K says "Franchisee-owned stores are generally required to replace their equipment every five to nine years" (changed effective 1 Jan 2024). [SEC FY2018](https://www.sec.gov/Archives/edgar/data/1637207/000163720719000009/plnt10-k12312018document.htm), [SEC FY2023](https://www.sec.gov/Archives/edgar/data/1637207/000163720724000020/plnt-20231231.htm)
- Rework "Equipment Lifecycle & Maintenance Planning for Gyms" (2025 vendor guide) says cardio has a "7-10 year useful life under commercial use" and "High-traffic machines in large gyms may hit end of useful life at 5-7 years". The same guide gives strength 15-20 yr, free weights 20-30 yr, "turf 3-5 years" and rubber flooring 5-8 yr. It also says "Annual cost for a full-service contract on a commercial cardio unit runs $200-$400 per machine", that third-party service is "often 15-25% less expensive than OEM", and that "The standard depreciation schedule is 7 years straight-line". [rework.com](https://resources.rework.com/libraries/gym-fitness-growth/equipment-lifecycle-maintenance)
- Skelcore guide: annual contracts for a single commercial treadmill "between $300 and $800 per year"; a ten-treadmill floor "$4,000 to $6,000 per year"; "one to four technician visits a year"; lifespan "seven to ten years or more". [skelcore.com](https://www.skelcore.com/guides/what-cost-commercial-treadmills-annual-maintenance-contract)
- Life Fitness "The Importance of Preventive Maintenance" (PDF): "Life Fitness will schedule your preventive maintenance visits every 3 or 6 months". It also says "IHRSA recommends that once every five years club operators spend 10% of revenue on investments like new equipment." [Life Fitness PDF](https://www.lifefitness.com/Kentico13CoreBase/media/LFMedia/LF-PDFs/service-agreements-preventative-maintenance-download-data.pdf)
- Warranty floors: StairMaster commercial "Limited 10 year warranty on structural frame ..., all other components warranted for 2 years parts and 1 year labor" (Fitness Superstore 8Gx page). AssaultBike Elite: 10-yr frame, 3-yr non-wear parts, 1-yr labor (fetched=false). Legend Fitness plyo sets, sleds and suspension rig: 15-year warranty. TKO suspension bay: frame 10 yr, pull-up bars 5 yr, shelving 1 yr. TKO push sled: frame 5 yr, parts 1 yr. ECORE RageTurf: 5-year commercial warranty. Life Fitness battle rope and core mats: 90 days.
- Extended-plan pricing as a repair-cost proxy (Fitness Exchange Safeware, certified pre-owned, 12 months): $599 for $10k-$15k items (4.0-6.0%/yr); $319 for $5k-$5,999 (5.3-6.4%); $279 for $3k-$3,999 (7.0-9.3%). These plans cover used equipment and include insurer margin, so treat them as an upper bound.

| Item id | Useful life typical (low-high), yrs | Annual maintenance % of price, typical (low-high) | Basis |
|---|---|---|---|
| `treadmill` | 7 (5-10) | 5.0% (3.0-8.0%) | life: PLNT 10-K re-equip 5-7 yr (2018) / 5-9 yr (2024+); vendor guides 7-10 yr, 5-7 yr high-traffic; maint: $300-$800/yr service contract per commercial treadmill (Skelcore) / $10.3k typical commercial price |
| `curved_treadmill` | 10 (8-12) | 2.0% (1.0-3.0%) | life: estimate: no motor/electronics; treat like other self-powered cardio upper range; maint: estimate: no motor; slats/bearings only |
| `elliptical` | 8 (7-10) | 4.0% (2.5-6.0%) | life: vendor guide 7-10 yr commercial cardio; PLNT 5-9 yr re-equip; maint: $200-$400/yr full-service per cardio unit (Rework guide) / $6.5k |
| `upright_bike` | 8 (7-10) | 4.0% (2.5-7.0%) | life: as elliptical; maint: $200-$400/yr / $4.2k |
| `recumbent_bike` | 8 (7-10) | 4.0% (2.5-6.0%) | life: as elliptical; maint: $200-$400/yr / $4.95k |
| `indoor_cycle` | 7 (5-8) | 5.0% (3.0-8.0%) | life: estimate: heavy class use; lower end of 7-10 yr cardio range; maint: estimate: pads/belts/pedals wear quickly in classes; $100-$200/yr on $2.6k |
| `air_bike` | 8 (6-10) | 3.0% (2.0-5.0%) | life: AssaultBike Elite 10-yr frame warranty; cardio range; maint: estimate: belts/bearings; simple mechanics |
| `rower` | 10 (7-12) | 2.0% (1.0-3.0%) | life: estimate: simple air-flywheel design; Concept2 lists a "Limited 2 Year & 5 Year Warranty"; maint: estimate: chain/seat rollers |
| `stair_climber` | 7 (5-9) | 4.0% (3.0-6.0%) | life: PLNT re-equip range; StairMaster commercial 10-yr frame/2-yr parts/1-yr labor warranty; maint: $200-$400+/yr / $10.25k, plus higher wear on step chains (estimate) |
| `ski_erg` | 10 (7-12) | 2.0% (1.0-3.0%) | life: estimate: same construction class as rower; maint: estimate |
| `recumbent_stepper` | 10 (7-12) | 2.5% (1.5-4.0%) | life: estimate: low-speed, rehab-duty units; maint: $200/yr on $7.4k (estimate) |
| `rig_bay` | 20 (15-25) | 1.0% (0.5-2.0%) | life: steel frame; Legend 15-yr warranty, TKO 10-yr structural frame warranty; maint: estimate: hardware re-torque, J-cup/strap replacement |
| `turf_lane` | 4 (3-5) | 2.0% (1.0-3.0%) | life: vendor guide: turf 3-5 yr; ECORE RageTurf 5-yr commercial warranty; maint: estimate: cleaning, seam repair; replacement via useful life |
| `sled` | 12 (8-15) | 2.0% (1.0-4.0%) | life: Legend sleds 15-yr warranty; TKO sled frame 5-yr/parts 1-yr; maint: estimate: skid/wheel replacement (Torque sells replacement airless tires $45-$110) |
| `plyo_box_set` | 6 (4-8) | 2.0% (1.0-4.0%) | life: estimate: foam/vinyl covers wear; steel Legend sets 15-yr warranty; maint: estimate: cover replacement (REP covers $34.99-$59.99) |
| `wall_ball_station` | 3 (2-4) | 0.0% (0.0-2.0%) | life: estimate: consumable soft goods; maint: consumable: handled by short useful life |
| `battle_rope_station` | 3 (2-4) | 0.0% (0.0-2.0%) | life: estimate; Life Fitness battle rope 90-day warranty; maint: consumable |
| `suspension_trainer_station` | 4 (3-5) | 0.0% (0.0-2.0%) | life: estimate: nylon straps; mounts last much longer; maint: consumable |
| `heavy_bag` | 5 (3-7) | 1.0% (0.0-3.0%) | life: estimate; maint: estimate: chain/swivel replacement |
| `stretch_area` | 2 (1-3) | 0.0% (0.0-2.0%) | life: estimate; Life Fitness core mats 90-day warranty; maint: consumable |
| `accessory_pack` | 2 (1-3) | 0.0% (0.0-2.0%) | life: estimate: consumables; maint: consumable |

## 7. Conflicts and caveats

- **Matrix (Johnson Fitness)** pages show different prices for the same model. Performance LED Upright: $5,505 on category pages vs $4,830 on the product page. RXP rower: $4,030 vs $4,595. Endurance LED Recumbent: $5,685 vs $4,985. The higher (category/list) value is used and the conflict is noted in the row.
- **Precor TRM 885** was quoted at $14,010 (Top Fitness, earlier search snippet). Top Fitness now lists the current TRM 681/691/761/781/791 line at $11,800-$14,290, so the TRM 885 figure is excluded.
- **Assault Fitness** shows all three AssaultBikes as "Sold Out" at the listed prices (Classic $749 sale / $799 regular, Pro X $899, Elite $1,499). Rogue lists the same prices.
- **AssaultRunner Pro** is $3,499 at Push Pedal Pull vs $4,899 at Total Fitness USA. Both are kept; the curved-treadmill value median uses the PPP price.
- **TrueForm Runner**: elitefts shows $4,000-$4,300 and Sorinex was reported at $3,995 (search). These look like non-standard or old prices. The model uses Fitness Superstore $6,395, Rogue $6,595 and Competitors Outlet $6,895.
- **Life Fitness "TRX Suspension Trainer" ($446)** is a TRX Rip Trainer kit according to its own description, so it is excluded from suspension-trainer pricing.
- **Rower commercial tier**: Concept2 RowErg with tall legs ($1,155) is the de-facto club standard and is cheaper than club-brand rowers (LF Row HX $1,899, Matrix $2,720). The tier median is $1,900. A planner that favours value may want the Concept2 price for the commercial tier.
- **Ski erg premium**: no "top club line" ski erg is clearly better than Concept2. The premium tier uses the club-brand alternatives (Throwdown HIIT Ski, TKO AirRaid, Stepr Ski XL). In practice premium gyms usually buy Concept2 SkiErg + floor stand ($1,070).
- **Rig premium tier** prices include many storage and station attachments (Throwdown XTC). Frame-only premium per-bay cost was not found; Rogue Monster Standard ($999-$1,313 per bay) is the best frame-only upper reference.
- **Plate-loaded sleds** need plates. Torque TANK sleds (premium) have built-in adjustable resistance and need no plates, which partly offsets their price.
- **Shopify `updated_at`** shows the feed date, not the date of the last price change. All prices are as served on 2026-10-28.

## 8. Gaps

- No current new USD price was found for Technogym (Skillrun, Skillmill, Excite) or Cybex/Life Fitness Platinum Club Series. Technogym Skillmill: CAD $20,350 new (Northern Fitness) and US remanufactured $7,999; the regular Woodway Curve (non-LTG) new US price was also not found.
- No list prices were found for Stages SC3, Keiser M3i (commercial direct), Schwinn AC Performance Plus or Peloton Commercial; dealers show "call for price".
- No primary industry statistic was found for freight as % of equipment. The recommended 8-12% is triangulated from dealer fee schedules, Hoist install fees, Concept2 shipping, FDD Item 7 summaries and vendor guidance.
- No independent study of maintenance cost as % of price was found. The percentages above are derived from per-unit service-contract dollars divided by typical price.
- Web search quota was exhausted part-way through. Later evidence came from direct fetches of retailer catalogs and pages already identified.

## 9. Source index (publishers)

- American Barbell: https://www.americanbarbell.com
- Assault Fitness: https://www.assaultfitness.com/bikes/
- BLK BOX Fitness (US storefront): https://www.blkboxfitness.com/en-us
- Bells of Steel: https://www.bellsofsteel.us
- Bells of Steel / REP: https://www.bellsofsteel.us
- Blue Sky Fit Supply: https://blueskyfitsupply.com
- Blue Sky Fit Supply / Fitness Exchange: https://blueskyfitsupply.com
- CTX Home Gyms: https://ctxhomegyms.com
- Competitors Outlet: https://competitorsoutlet.com
- Concept2: https://www.concept2.com/ergs/rowerg, https://www.concept2.com/ergs/skierg
- Everlast: https://www.everlast.com
- Everlast / TITLE: https://www.everlast.com
- Fitness Exchange: https://fitnessexchange.com
- Fitness Exchange / TRX: https://fitnessexchange.com
- Fitness Superstore: https://fitnesssuperstore.com
- Fitness Superstore / Fitness Exchange: https://fitnesssuperstore.com/
- Fitness Superstore / REP: https://fitnesssuperstore.com
- Fitness Superstore / TITLE: https://fitnesssuperstore.com
- Fringe Sport: https://www.fringesport.com
- Johnson Fitness & Wellness (Matrix dealer): https://www.johnsonfitness.com/Commercial-Ellipticals-C161.aspx, https://www.johnsonfitness.com/Commercial-Exercise-Bikes-C578.aspx, https://www.johnsonfitness.com/Commercial-Recumbent-Bikes-C163.aspx, https://www.johnsonfitness.com/Commercial-Rowers-C166.aspx
- Life Fitness: https://shop.lifefitness.com
- Life Fitness (shop.lifefitness.com): https://shop.lifefitness.com, https://shop.lifefitness.com/
- Life Fitness / Rogue: https://shop.lifefitness.com
- Life Fitness / TITLE: https://shop.lifefitness.com
- LiveFit: https://livefit.com
- LiveFit / American Barbell: https://livefit.com
- Power Systems: https://powersystems.com
- Power Systems / Fringe Sport: https://powersystems.com
- Power Systems / Life Fitness: https://powersystems.com
- Push Pedal Pull: https://pushpedalpull.com
- REP Fitness: https://www.repfitness.com
- REP Fitness / Fringe Sport: https://www.repfitness.com
- Recovery for Athletes: https://recoveryforathletes.com
- Rogue Fitness: https://www.roguefitness.com/concept-2-skierg-2, https://www.roguefitness.com/gymturf, https://www.roguefitness.com/monster-lite-rig-2-0, https://www.roguefitness.com/monster-rig-2-0
- TITLE Boxing: https://www.titleboxing.com
- TRX Training: https://www.trxtraining.com
- The Fitness Outlet: https://thefitnessoutlet.com
- Titan Fitness: https://titan.fitness
- Top Fitness (Precor dealer): https://topfitness.com
- Torque Fitness: https://www.torquefitness.com
- Torque Fitness / Fringe Sport: https://www.torquefitness.com
- Torque Fitness / Rogue: https://www.torquefitness.com
- Total Fitness USA: https://tfusa.net
- elitefts: https://www.elitefts.com
- elitefts / American Barbell: https://www.elitefts.com
