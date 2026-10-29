# Strength-equipment pricing (racks, barbells, plates, dumbbells, benches, machines, cables) — research slice `price_strength`

_Snapshot date: 2026-10-28. All prices USD. Prices were read live from manufacturer and authorized-dealer storefronts (most via the stores' public Shopify `products.json` catalog feeds, Rogue via JSON-LD/product HTML). Unless stated otherwise, a price is the advertised new-unit web price (list or current sale) excluding freight, tax, install and negotiated fleet discounts._

## 1. Key findings

- **Free weight is priced by the pound and is remarkably stable across value brands.** Cast-iron Olympic plates cost ~$1.90/lb (REP Old School, Titan, Rogue Olympic, French Fitness; range $1.68–2.06/lb). Rubber hex dumbbells cost ~$1.85/lb in value sets (REP, Rogue, Titan, French Fitness; $1.58–2.17/lb). Bumpers ~$2.10/lb (Rogue Echo/HG 2.0, REP, Titan; $1.93–2.39/lb).
- **Brand premium on free weights is large.** Hammer Strength (Life Fitness store) list prices: urethane round plates $5.91/lb, 12-sided $6.33/lb; 4-sided urethane dumbbells $6.6–9.6/lb; 12-sided urethane dumbbells $8.2–13.6/lb — 3–7x the value tier.
- **Selectorized single-station machines cluster by tier:** value (Body-Solid ProClub/Series II, French Fitness, Titan) ≈ $2.3–3.0k; commercial (Life Fitness Axiom $4,631–5,429; Hoist Club Line $4,890 / ROC-IT $5,805 / HD Dual $4,400; Nautilus Instinct $3,499–3,819 and Impact $5,479–5,899 at a lower-48 dealer; Prime Hybrid $5,150–6,850) ≈ $4.7–5.6k; premium (Hammer Strength Select $4,929–9,449; LF Insignia $6,957–9,091; Nautilus Inspiration $6,789–7,319; Prime Evolution $5,350–8,500) ≈ $6.5–7.3k typical.
- **Plate-loaded machines are cheaper than selectorized in the same brand** (Hammer Strength Iso-Lateral $4,135 vs Select ~$5,800–6,700; Hoist ROC-IT plate-loaded $3,815 vs ROC-IT selectorized $5,805). Premium vs commercial plate-loaded overlap heavily ($3.8–4.3k).
- **Racks:** value power racks ≈ $870 (REP PR-4000 $799.94, Rogue R-3 $870, Titan T-3 $519.97, Body-Solid SPR1000 $1,500); commercial ≈ $2.95k (Rogue RM-4 Monster $1,830 … Hoist CF power cage $3,090); premium ≈ $4.65k (Hammer Strength HD Athletic NX power rack $4,657; HD Elite iD half rack $6,229).
- **Complete power-rack station (rack + 20 kg bar + 350 lb plates + collars):** value ≈ $1,850, commercial ≈ $4,400, premium ≈ $7,500.
- **Dumbbell sets:** 5–50 lb pairs (550 lb) + rack ≈ $1,750 value / $2,750 commercial / $7,000 premium; 5–100 lb pairs (2,100 lb) + racks ≈ $5,000 / $8,550 / $20,150; 105–150 lb pairs (2,550 lb) + rack ≈ $5,450 / $6,950 / $18,750.
- **Dealer list vs street:** the same Nautilus SKUs are listed 1.38–1.53x higher (median 1.49x, n=54) at an Alaska dealer (AKFIT) than at a lower-48 dealer (Fitness Superstore). AKFIT prices were therefore divided by 1.45 before computing tier medians.
- **Remanufactured premium equipment** sells for ~0.40x (CTX Home Gyms) to ~0.63x (Fitness Superstore) of current new list price (median 0.50x across 15 matched Hammer Strength / Life Fitness models), i.e. refurbished premium ≈ new commercial pricing.

## 2. Method

1. **Catalog capture.** Full public product catalogs were downloaded from: REP Fitness (742 products), Life Fitness consumer shop (331) and facility shop (239), Fitness Superstore (3,750; authorized dealer for Body-Solid, Nautilus, French Fitness plus a large remanufactured inventory), Hoist Fitness (673), Prime Fitness USA (189), Torque Fitness (204), Titan Fitness (2,557), Bells of Steel (476), AKFIT (1,462; Matrix/Nautilus/Watson/Rogers/Torque dealer in Alaska) and CTX Home Gyms (777; remanufactured). Rogue Fitness category and product pages (JSON-LD offers + rendered item tables) and Sorinex product pages (embedded `price`) were parsed individually. All feeds showed `updated_at` = 2026-10-28.
2. **Classification.** Each product was mapped to the canonical taxonomy (regex on title + plate-loaded/selectorized line detection) and to a tier: VALUE (REP, Titan, Body-Solid, French Fitness, Bells of Steel, Rogue entry/Monster Lite, Torque home), COMMERCIAL (Rogue Monster, Hoist, Life Fitness Axiom/Optima and LF free-weight benches/racks, Matrix Aura/Versa/Go/G1, Nautilus Instinct/Impact/Leverage, Prime Hybrid/Plate-Loaded/Prodigy, Torque TR), PREMIUM (Hammer Strength, LF Insignia, Matrix Ultra/Magnum, Nautilus Inspiration/One, Prime Evolution, Sorinex, Watson, Rogers Pendulum). Refurbished/remanufactured listings are kept separate.
3. **Anchors and recommended value.** For each item×tier, 2–9 representative *new* listings were chosen (canonical models; accessories excluded). AKFIT prices were divided by 1.45 (see §8). Recommended model price = median of anchors, rounded to $10 (<$1k) or $50. Low/high = min/max of (adjusted) anchors. Where fewer than two anchors existed, the value is flagged as an estimate with its derivation.
4. **Stations** are built from recommended components: power/half rack = frame + 20 kg bar + 350 lb plates + collars; bench stations = bench + bar + 250 lb plates + collars; platform = platform + 260 lb bumpers + bar + collars; dumbbell sets = set price + rack(s) holding 10 pairs per rack. Plate $/lb used for stations: value $1.90 (cast iron), commercial $3.10 (urethane-coated, e.g. REP Equalizer), premium $5.90 (Hammer Strength urethane). Bars: $260 / $310 / $700. Collars: $40 / $55 / $101 (LF Lock-Jaw OLY 2 $101).
5. **Caveats.** Advertised web prices; commercial buyers negotiating multi-unit orders typically pay less than list (the 1.49x AK-vs-lower-48 spread on identical SKUs shows how wide dealer pricing can be). Freight on machines (often $150–800/unit) and white-glove install (Hoist lists $100–800 per item) are excluded.

## 3. Per-pound prices (plates, dumbbells, kettlebells)

### Cast-iron Olympic plates

| Product | Basis | Price | lb | $/lb | Source |
|---|---|---:|---:|---:|---|
| REP Old School Iron Plates | 45 lb pair | $169.98 | 90 | $1.89 | https://repfitness.com/products/old-school-iron-plate-pairs |
| REP Old School Iron Plate Set | 355 lb set | $681.99 | 355 | $1.92 | https://repfitness.com/products/old-school-iron-plate-sets |
| REP Equalizer USA-Made Iron Plates | 45 lb pair | $259.98 | 90 | $2.89 | https://repfitness.com/products/usa-made-equalizer-iron-plates |
| REP Equalizer USA-Made Iron Plate Set | 355 lb set | $1,085.99 | 355 | $3.06 | https://repfitness.com/products/usa-made-equalizer-iron-plate-sets |
| Rogue Olympic Plates (cast iron) | 45 lb pair | $185 | 90 | $2.06 | https://www.roguefitness.com/rogue-olympic-plates |
| Rogue Olympic Plates (cast iron) | 25 lb pair | $93 | 50 | $1.86 | https://www.roguefitness.com/rogue-olympic-plates |
| Rogue Deep Dish Plates | 45 lb pair | $205 | 90 | $2.28 | https://www.roguefitness.com/rogue-deep-dish-plates |
| Rogue Deep Dish Plate Set (shipping incl.) | 410 lb set | $1,203 | 410 | $2.93 | https://www.roguefitness.com/rogue-deep-dish-plates |
| Rogue Machined Olympic Plates | 45 lb pair | $230 | 90 | $2.56 | https://www.roguefitness.com/rogue-machined-olympic-plates |
| Rogue Machined Olympic Plate Set | 245 lb set | $783 | 245 | $3.20 | https://www.roguefitness.com/rogue-machined-olympic-plates |
| Titan Cast Iron Olympic Plate | 45 lb single | $84.97 | 45 | $1.89 | https://titan.fitness/products/45-lb-single-cast-iron-olympic-plate |
| French Fitness Cast Iron Olympic Plate V1 | 45 lb single | $84.60 | 45 | $1.88 | https://fitnesssuperstore.com/products/french-fitness-cast-iron-olympic-weight-plate-v1-45-lbs-new |
| French Fitness Cast Iron Olympic Plate V1 Set | 350 lb set | $589 | 350 | $1.68 | https://fitnesssuperstore.com/products/french-fitness-cast-iron-olympic-weight-plate-v1-set-350-lbs-new |

### Rubber-coated / grip plates

| Product | Basis | Price | lb | $/lb | Source |
|---|---|---:|---:|---:|---|
| REP Rubber Coated Olympic Plates | 45 lb pair | $219.99 | 90 | $2.44 | https://repfitness.com/products/rubber-coated-olympic-plate-pairs |
| REP Rubber Coated Olympic Plate Set | 355 lb set | $884.99 | 355 | $2.49 | https://repfitness.com/products/rubber-coated-olympic-plate-sets |
| French Fitness Colored Rubber Grip Olympic Plate | 45 lb single | $97 | 45 | $2.16 | https://fitnesssuperstore.com/products/french-fitness-colored-rubber-grip-olympic-plate-45-lbs-new |
| French Fitness Colored Rubber Grip Plate Set | 350 lb set | $649 | 350 | $1.85 | https://fitnesssuperstore.com/products/french-fitness-colored-rubber-grip-olympic-plate-set-350-lbs-new |
| Hammer Strength Round Rubber Olympic Plate (list) | 45 lb single | $174 | 45 | $3.87 | https://shop.lifefitness.com/products/hammer-strength-round-rubber-olympic-plates |

### Urethane plates

| Product | Basis | Price | lb | $/lb | Source |
|---|---|---:|---:|---:|---|
| REP Equalizer Urethane-Coated Plates | 45 lb pair | $279.99 | 90 | $3.11 | https://repfitness.com/products/urethane-coated-equalizer-plate-pairs |
| REP Equalizer Urethane-Coated Plate Set | 355 lb set | $1,107.99 | 355 | $3.12 | https://repfitness.com/products/urethane-coated-equalizer-plate-sets |
| Rogue Urethane Plates | 45 lb pair | $351 | 90 | $3.90 | https://www.roguefitness.com/rogue-urethane-plates |
| Rogue Urethane Plate Set | 340 lb set | $1,470 | 340 | $4.32 | https://www.roguefitness.com/rogue-urethane-plates |
| Titan EZ-Grip Elite Urethane Color Plate | 45 lb single | $174.97 | 45 | $3.89 | https://titan.fitness/products/45-lb-single-ez-grip-elite-urethane-color-plate |
| Titan EZ-Grip Elite Urethane Color Plate Set | 340 lb set | $1,599.97 | 340 | $4.71 | https://titan.fitness/products/340-lb-set-ez-grip-elite-urethane-color-plates |
| Hammer Strength Urethane Round Olympic Plate (list) | 45 lb single | $266 | 45 | $5.91 | https://shop.lifefitness.com/products/hammer-strength-urethane-round-olympic-plates |
| Hammer Strength Urethane 12-Sided Olympic Plate (list) | 45 lb single | $285 | 45 | $6.33 | https://shop.lifefitness.com/products/hammer-strength-urethane-12-side-olympic-plates |

### Bumper plates

| Product | Basis | Price | lb | $/lb | Source |
|---|---|---:|---:|---:|---|
| REP Black Bumper Plates (LB) | 45 lb pair | $199.99 | 90 | $2.22 | https://repfitness.com/products/black-bumper-plate-pairs |
| REP Black Bumper Plate Set (LB) | 340 lb set | $749.99 | 340 | $2.21 | https://repfitness.com/products/black-bumper-plate-sets |
| Rogue Echo Bumper Plates V2 | 45 lb pair | $174 | 90 | $1.93 | https://www.roguefitness.com/rogue-echo-bumper-plates-with-white-text |
| Rogue Echo Bumper Set V2 | 260 lb set | $583 | 260 | $2.24 | https://www.roguefitness.com/rogue-echo-bumper-plates-with-white-text |
| Rogue HG 2.0 Bumper Plates | 45 lb pair | $184 | 90 | $2.04 | https://www.roguefitness.com/rogue-hg-2-0-bumper-plates |
| Rogue HG 2.0 Set | 350 lb set | $835 | 350 | $2.39 | https://www.roguefitness.com/rogue-hg-2-0-bumper-plates |
| Rogue HG 2.0 Set | 1000 lb set | $2,006 | 1000 | $2.01 | https://www.roguefitness.com/rogue-hg-2-0-bumper-plates |
| Titan Economy Bumper Plate | 45 lb single | $94.97 | 45 | $2.11 | https://titan.fitness/products/45-lb-single-economy-bumper-plate |
| Titan Economy Bumper Plate Set | 230 lb set | $464.97 | 230 | $2.02 | https://titan.fitness/products/230-lb-set-economy-bumper-plates |
| REP Competition Bumper Plates (LB) | 45 lb pair | $299.99 | 90 | $3.33 | https://repfitness.com/products/competition-bumper-plate-pairs-lb |
| Hammer Strength Standard Rubber Bumper (list) | 45 lb single | $148 | 45 | $3.29 | https://shop.lifefitness.com/products/hammer-strength-standard-rubber-bumpers |
| Hammer Strength Premium Rubber Black Bumper (list) | 45 lb single | $285 | 45 | $6.33 | https://shop.lifefitness.com/products/hammer-strength-premium-rubber-black-bumpers |
| Hammer Strength Urethane Black Bumper (list) | 45 lb single | $464 | 45 | $10.31 | https://shop.lifefitness.com/products/hammer-strength-urethane-black-bumpers |

### Rubber hex dumbbells

| Product | Basis | Price | lb | $/lb | Source |
|---|---|---:|---:|---:|---|
| REP Hex Dumbbell (LB) Set 5-50 | 5-50 pairs | $1,099.99 | 550 | $2.00 | https://repfitness.com/products/rubber-hex-dumbbell-sets |
| REP Hex Dumbbell (LB) Set 5-100 | 5-100 pairs | $3,699.99 | 2100 | $1.76 | https://repfitness.com/products/rubber-hex-dumbbell-sets |
| REP Hex Dumbbells 105-125 (sum of pair prices) | 105-125 pairs | $2,499.95 | 1150 | $2.17 | https://repfitness.com/products/rubber-hex-dumbbell-pairs |
| Rogue Rubber Hex Dumbbell Set 5-50 | 5-50 pairs | $960 | 550 | $1.75 | https://www.roguefitness.com/rogue-rubber-hex-dumbbell-sets |
| Rogue Rubber Hex Dumbbell Set 55-100 | 55-100 pairs | $2,945 | 1550 | $1.90 | https://www.roguefitness.com/rogue-rubber-hex-dumbbell-sets |
| Rogue Rubber Hex 5-50 + 55-100 sets | 5-100 pairs | $3,905 | 2100 | $1.86 | https://www.roguefitness.com/rogue-rubber-hex-dumbbell-sets |
| Rogue Rubber Hex Dumbbell Set 105-125 | 105-125 pairs | $2,200 | 1150 | $1.91 | https://www.roguefitness.com/rogue-rubber-hex-dumbbell-sets |
| Titan 5-50 LB Pairs Rubber Hex Dumbbells | 5-50 pairs | $1,129.97 | 550 | $2.05 | https://titan.fitness/products/5-lb-50-lb-pairs-rubber-hex-dumbbells |
| Titan 55-100 LB Pairs Rubber Hex Dumbbells | 55-100 pairs | $2,699.97 | 1550 | $1.74 | https://titan.fitness/products/55-lb-100-lb-pairs-rubber-hex-dumbbells |
| French Fitness Rubber Coated Hex Set 5-50 | 5-50 pairs | $899.10 | 550 | $1.64 | https://fitnesssuperstore.com/products/french-fitness-rubber-coated-hex-dumbbell-set-5-50-lbs-new |
| French Fitness Rubber Coated Hex Set 5-100 | 5-100 pairs | $3,329.10 | 2100 | $1.58 | https://fitnesssuperstore.com/products/french-fitness-rubber-coated-hex-dumbbell-set-5-100-lbs-new |
| French Fitness Rubber Coated Hex Set 105-150 | 105-150 pairs | $4,699 | 2550 | $1.84 | https://fitnesssuperstore.com/products/french-fitness-rubber-coated-hex-dumbbell-set-105-150-lbs-new |
| Life Fitness Rubber HEX Dumbbells 5-50 set | 5-50 pairs | $1,694 | 550 | $3.08 | https://shop.lifefitness.com/products/rubber-hex-dumbbells |
| Life Fitness Rubber HEX 5-50+55-75+80-100 sets | 5-100 pairs | $6,115 | 2100 | $2.91 | https://shop.lifefitness.com/products/rubber-hex-dumbbells |
| Hammer Strength 4-Sided Rubber Dumbbells 5-50 set (list) | 5-50 pairs | $3,544 | 550 | $6.44 | https://shop.lifefitness.com/products/hammer-strength-4-sided-rubber-dumbbells |
| Hoist (PERL) 5-100 Pair DB set | 5-100 pairs | $5,350 | 2100 | $2.55 | https://www.hoistfitness.com/products/5-100-pair-db-5lbs-incriments-set |

### Urethane dumbbells

| Product | Basis | Price | lb | $/lb | Source |
|---|---|---:|---:|---:|---|
| REP Urethane Dumbbell (LB) Set 5-50 | 5-50 pairs | $1,599.99 | 550 | $2.91 | https://repfitness.com/products/urethane-coated-round-dumbbell-sets |
| REP Urethane Dumbbell (LB) Set 5-100 | 5-100 pairs | $5,699.99 | 2100 | $2.71 | https://repfitness.com/products/urethane-coated-round-dumbbell-sets |
| REP Urethane Dumbbell (LB) Set 105-125 | 105-125 pairs | $2,999.99 | 1150 | $2.61 | https://repfitness.com/products/urethane-coated-round-dumbbell-sets |
| REP Urethane Dumbbell (LB) Set 130-150 (regular price) | 130-150 pairs | $3,299.99 | 1400 | $2.36 | https://repfitness.com/products/urethane-coated-round-dumbbell-sets |
| Rogue Urethane Dumbbell Set 5-50 | 5-50 pairs | $2,420 | 550 | $4.40 | https://www.roguefitness.com/rogue-urethane-dumbbells-new |
| Rogue Urethane Dumbbell Set 5-100 | 5-100 pairs | $8,995 | 2100 | $4.28 | https://www.roguefitness.com/rogue-urethane-dumbbells-new |
| Rogue Urethane Dumbbell Set 105-150 | 105-150 pairs | $9,950 | 2550 | $3.90 | https://www.roguefitness.com/rogue-urethane-dumbbells-new |
| Titan Round Urethane 5-50 set | 5-50 pairs | $2,024.99 | 550 | $3.68 | https://titan.fitness/products/5-lb-50-lb-set-round-urethane-dumbbells |
| Titan Round Urethane 55-100 set | 55-100 pairs | $5,099.97 | 1550 | $3.29 | https://titan.fitness/products/55-lb-100-lb-set-round-urethane-dumbbells |
| French Fitness Urethane Round Pro Style V2 Set 5-100 | 5-100 pairs | $5,699 | 2100 | $2.71 | https://fitnesssuperstore.com/products/french-fitness-urethane-round-pro-style-dumbbell-v2-set-5-100-lbs-new |
| Hammer Strength 4-Sided Urethane 5-50 set (list) | 5-50 pairs | $5,256 | 550 | $9.56 | https://shop.lifefitness.com/products/hammer-strength-4-sided-urethane-dumbbells |
| Hammer Strength 4-Sided Urethane 5-50+55-75+80-100 (list) | 5-100 pairs | $16,662 | 2100 | $7.93 | https://shop.lifefitness.com/products/hammer-strength-4-sided-urethane-dumbbells |
| Hammer Strength 4-Sided Urethane 105-125+130-150 (list) | 105-150 pairs | $16,998 | 2550 | $6.67 | https://shop.lifefitness.com/products/hammer-strength-4-sided-urethane-dumbbells |
| Hammer Strength 12-Sided Urethane 5-50 set (list) | 5-50 pairs | $7,484 | 550 | $13.61 | https://shop.lifefitness.com/products/hammer-strength-12-sided-urethane-dumbbells |
| Hammer Strength 12-Sided Urethane 5-50+55-75+80-100 (list) | 5-100 pairs | $21,702 | 2100 | $10.33 | https://shop.lifefitness.com/products/hammer-strength-12-sided-urethane-dumbbells |

### Steel / chrome-style dumbbells

| Product | Basis | Price | lb | $/lb | Source |
|---|---|---:|---:|---:|---|
| Titan Straight Stainless Steel Hex Dumbbells | 100 lb pair | $399.97 | 200 | $2.00 | https://titan.fitness/products/100-lb-straight-stainless-steel-hex-dumbbells |
| Titan Straight Stainless Steel Hex Dumbbells | 50 lb pair | $224.97 | 100 | $2.25 | https://titan.fitness/products/50-lb-straight-stainless-steel-hex-dumbbells |
| Titan Straight Stainless Steel Hex Dumbbells | 25 lb pair | $124.97 | 50 | $2.50 | https://titan.fitness/products/25-lb-straight-stainless-steel-hex-dumbbells |

### Kettlebells

| Product | Basis | Price | lb | $/lb | Source |
|---|---|---:|---:|---:|---|
| REP Kettlebells (lb) | 35 lb | $74.99 | 35 | $2.14 | https://repfitness.com/products/kettlebells-lb |
| REP Kettlebells (lb) | 50 lb | $119.99 | 50 | $2.40 | https://repfitness.com/products/kettlebells-lb |
| REP Kettlebell Set 8-24 kg (5 bells, 80 kg) | 80 kg set | $360.99 | 176 | $2.05 | https://repfitness.com/products/8-24kg-v3-kettlebell-set |
| Rogue Kettlebell | 35 lb | $80 | 35 | $2.29 | https://www.roguefitness.com/rogue-kettlebells |
| Rogue Kettlebell | 53 lb | $103 | 53 | $1.94 | https://www.roguefitness.com/rogue-kettlebells |
| Rogue Kettlebell | 70 lb | $133 | 70 | $1.90 | https://www.roguefitness.com/rogue-kettlebells |
| Titan Cast Iron Kettlebell | 16 kg | $84.99 | 35 | $2.41 | https://titan.fitness/products/16-kg-cast-iron-kettlebell |
| French Fitness Cast Iron Kettlebell | 35 lb | $68 | 35 | $1.94 | https://fitnesssuperstore.com/products/french-fitness-cast-iron-kettlebell-35-lbs-new |
| French Fitness Cast Iron Kettlebell Set 5-50 (assumed 10 bells, 275 lb) | set | $439 | 275 | $1.60 | https://fitnesssuperstore.com/products/french-fitness-cast-iron-kettlebell-set-5-50-lbs-new |
| Life Fitness Cast Iron Kettlebell (list) | 16 kg | $105 | 35 | $2.98 | https://shop.lifefitness.com/products/cast-iron-kettlebell |
| Life Fitness Cast Iron Kettlebell (list) | 24 kg | $152 | 53 | $2.87 | https://shop.lifefitness.com/products/cast-iron-kettlebell |
| Hammer Strength Competition Kettlebell (list) | 16 kg | $168 | 35 | $4.76 | https://shop.lifefitness.com/products/hammer-strength-competition-kettlebells |
| Hammer Strength Competition Kettlebell (list) | 24 kg | $222 | 53 | $4.20 | https://shop.lifefitness.com/products/hammer-strength-competition-kettlebells |

### Recommended model $/lb

| Material | VALUE | COMMERCIAL | PREMIUM | Derivation |
|---|---:|---:|---:|---|
| Cast-iron plates | $1.90 | $2.90 | — | value = median of 7 value listings $1.89 (range 1.68–2.06); commercial-grade iron (REP Equalizer USA, Rogue Deep Dish/Machined) median $2.91 |
| Rubber-coated grip plates | $2.30 | $3.10 | $3.90 | value median $2.3 (REP, French Fitness); commercial = REP Equalizer urethane-coated $3.11; premium = Hammer Strength round rubber list $3.87 |
| Urethane plates | $3.10 | $3.90 | $6.10 | REP Equalizer $3.11–3.12; Rogue urethane $3.90–4.32, Titan EZ-Grip Elite $3.89–4.71 (median $3.89); Hammer Strength round/12-sided $5.91–6.33 |
| Bumper plates | $2.10 | $3.30 | $8.30 | value median $2.11 (n=9); commercial = REP competition $3.33 / HS standard rubber $3.29; premium = HS premium rubber $6.33 & urethane $10.31 (median $8.32) |
| Rubber hex dumbbells | $1.85 | $2.90 | $5.50 | value median $1.85 (n=12); commercial median $2.91 (Life Fitness $2.91–3.08, Hoist PERL $2.55); premium = Hammer Strength 4-sided rubber $4.75–6.44 |
| Urethane dumbbells | $2.70 | $4.30 | $8.00 | value median $2.71 (REP, Titan, French Fitness); Rogue urethane $3.90–4.40; HS 4-sided $6.63–9.56 and 12-sided $8.16–13.61 (5–100 set: HS 4-sided $7.93/lb) |
| Steel/chrome pro-style dumbbells | $2.25 | — | — | only Titan straight stainless hex pairs captured ($2.00–2.50/lb); see gaps |
| Kettlebells | $2.05 | $3.00 | $3.60 | value median $2.05 (REP, Rogue, Titan, French Fitness); Life Fitness cast iron list $2.87–2.98; Hammer Strength competition $2.29–4.76 (median $3.59 across LF/HS) |

Note the per-lb rate falls with plate/bell size: e.g. Rogue cast-iron 100 lb pair $238 = $1.19/lb vs 2.5 lb pair $18 = $3.60/lb; REP hex 5 lb pair $39.99 = $4.00/lb vs 100 lb pair $439.99 = $2.20/lb. Use set-level $/lb for whole-gym budgeting.

## 4. Olympic barbells

| Tier | Typical | Range | Anchors |
|---|---:|---|---|
| VALUE | $260 | $167.97–$285 | REP Fitness Delta Basic Bar $199.99; REP Fitness Black Canyon Bar - 20kg $259.99; Titan Fitness Performance Series Olympic Barbell $167.97; Titan Fitness Elite Series Olympic Barbell $264.97; Rogue Echo Bar 2.0 $285; Bells of Steel Multi-Purpose Olympic Barbell – The Utility Bar $261.99 |
| COMMERCIAL | $310 | $299.99–$385 | Rogue The Ohio Bar - Black Zinc $305; Rogue 45LB Ohio Power Bar - Black Zinc $315; Rogue The Ohio Bar - Stainless Steel $385; REP Fitness Colorado Bar - 20kg $299.99; Torque Fitness 7' Force Premium Barbell $305; TITAN Series Cerakote Olympic Barbell $349.97 |
| PREMIUM | $700 | $650–$853 | Hammer Strength Olympic WL Bar men 20 kg hard chrome $684; Hammer Strength Olympic WL Bar men 20 kg Cerakote $718; Hammer Strength Power Bars $853; Rogue Olympic Weightlifting Bar - Stainless Steel $650 |

Other bars seen: Titan Performance Series $167.97; French Fitness 7' Olympic power bar (1,500 lb) $249; Rogue 20 kg Ohio Power Bar $365; Rogue Pyrros Bar $755; Hammer Strength Power Bar $853–854; Hammer Strength Gym Bar $840–952 (LF facility shop); Hammer Strength curl bars $482–527; REP trap bar $299.99; Rogue TB-2 trap bar $415.

## 5. Complete-station prices

| Station | VALUE typical (range) | COMMERCIAL typical (range) | PREMIUM typical (range) | Build |
|---|---|---|---|---|
| power_rack | $1,850 ($1,300–$2,600) | $4,400 ($2,950–$5,900) | $7,500 ($6,650–$9,950) | rack frame + 20 kg bar + 350 lb plates + collars |
| half_rack | $1,700 ($1,350–$2,150) | $3,350 ($2,550–$7,550) | $7,450 ($6,250–$9,600) | half-rack frame + bar + 350 lb plates + collars |
| bench_press_station | $1,700 ($1,250–$1,900) | $2,750 ($1,750–$3,550) | $4,250 ($3,800–$5,350) | Olympic flat bench + bar + 250 lb plates + collars |
| incline_bench_station | $1,800 ($1,300–$2,200) | $2,850 ($1,900–$3,900) | $4,800 ($4,100–$5,400) | Olympic incline bench + bar + 250 lb plates + collars |
| decline_bench_station | $1,650 ($1,250–$2,000) | $2,850 ($2,100–$3,900) | $4,550 ($4,100–$5,250) | Olympic decline bench + bar + 250 lb plates + collars |
| lifting_platform | $1,300 ($1,100–$1,500) | $2,300 ($1,900–$2,950) | $8,850 ($3,500–$10,800) | 8x8 (or 6x8/8x8 commercial) platform + 260 lb bumpers + bar + collars |
| dumbbell_set_light | $1,750 ($1,300–$1,950) | $2,750 ($2,250–$3,250) | $7,000 ($4,050–$9,250) | 5–50 lb pairs (550 lb) + 1 rack |
| dumbbell_set_full | $5,000 ($5,000–$5,900) | $8,550 ($7,000–$10,100) | $20,150 ($12,300–$25,200) | 5–100 lb pairs (2,100 lb) + 2 racks |
| dumbbell_heavy_extension | $5,450 ($5,450–$5,450) | $6,950 ($6,950–$10,950) | $18,750 ($16,900–$18,750) | 105–150 lb pairs (2,550 lb) + 1 rack |
| kettlebell_set | $1,150 ($820–$1,150) | $2,550 ($1,150–$2,550) | $3,200 ($2,550–$3,200) | 9 bells ≈4–32 kg (~330 lb) + rack |
| fixed_barbell_set | $3,700 ($2,150–$3,700) | $8,700 ($8,700–$9,050) | $13,850 ($13,850–$17,950) | 10 straight + 10 EZ fixed bars (20–110 lb) + rack(s) |

Component detail for frame/bench stations:

- `power_rack` value: {"frame": 870, "bar": 260, "plates_350lb": 665, "collars": 40} → $1,850
- `power_rack` commercial: {"frame": 2950, "bar": 310, "plates_350lb": 1085, "collars": 55} → $4,400
- `power_rack` premium: {"frame": 4650, "bar": 700, "plates_350lb": 2065, "collars": 101} → $7,500
- `half_rack` value: {"frame": 730, "bar": 260, "plates_350lb": 665, "collars": 40} → $1,700
- `half_rack` commercial: {"frame": 1900, "bar": 310, "plates_350lb": 1085, "collars": 55} → $3,350
- `half_rack` premium: {"frame": 4600, "bar": 700, "plates_350lb": 2065, "collars": 101} → $7,450
- `bench_press_station` value: {"bench": 900, "bar": 260, "plates_250lb": 475, "collars": 40} → $1,700
- `bench_press_station` commercial: {"bench": 1600, "bar": 310, "plates_250lb": 775, "collars": 55} → $2,750
- `bench_press_station` premium: {"bench": 1950, "bar": 700, "plates_250lb": 1475, "collars": 101} → $4,250
- `incline_bench_station` value: {"bench": 1000, "bar": 260, "plates_250lb": 475, "collars": 40} → $1,800
- `incline_bench_station` commercial: {"bench": 1700, "bar": 310, "plates_250lb": 775, "collars": 55} → $2,850
- `incline_bench_station` premium: {"bench": 2500, "bar": 700, "plates_250lb": 1475, "collars": 101} → $4,800
- `decline_bench_station` value: {"bench": 860, "bar": 260, "plates_250lb": 475, "collars": 40} → $1,650
- `decline_bench_station` commercial: {"bench": 1700, "bar": 310, "plates_250lb": 775, "collars": 55} → $2,850
- `decline_bench_station` premium: {"bench": 2250, "bar": 700, "plates_250lb": 1475, "collars": 101} → $4,550
- `lifting_platform` value: {"platform": 450, "bumpers_260lb": 572, "bar": 260, "collars": 40, "total": 1322} → $1,300
- `lifting_platform` commercial: {"platform": 1300, "bumpers_260lb": 625, "bar": 310, "collars": 55, "total": 2290} → $2,300
- `lifting_platform` premium: {"platform": 6231, "bumpers_260lb": 1804, "bar": 718, "collars": 101, "total": 8854} → $8,850

Dumbbell/kettlebell/fixed-bar station builds (from live listings):

- `dumbbell_set_light|value`: REP hex 5-50 set + REP Commercial 2-tier rack → set $1,099.99 + rack $649.99 = **$1,749.98**
- `dumbbell_set_light|value_alt_rogue`: Rogue rubber hex 5-50 set + Rogue 3-tier rack → set $960 + rack $992.50 = **$1,952.50**
- `dumbbell_set_light|value_alt_ff`: French Fitness hex 5-50 + FF 2-tier saddle rack → set $899.10 + rack $899 = **$1,798.10**
- `dumbbell_set_light|commercial`: Life Fitness rubber HEX 5-50 + LF 3-tier hex rack (5-50) → set $1,694 + rack $1,549 = **$3,243**
- `dumbbell_set_light|commercial_alt_rep_urethane`: REP urethane 5-50 + REP commercial rack → set $1,599.99 + rack $649.99 = **$2,249.98**
- `dumbbell_set_light|premium`: Hammer Strength 4-sided urethane 5-50 + HS 2-tier rack → set $5,256 + rack $1,756 = **$7,012**
- `dumbbell_set_light|premium_alt_12sided`: Hammer Strength 12-sided urethane 5-50 + HS 2-tier rack → set $7,484 + rack $1,756 = **$9,240**
- `dumbbell_set_full|value`: REP hex 5-100 set + 2x REP Commercial 2-tier racks → set $3,699.99 + rack $1,299.98 = **$4,999.97**
- `dumbbell_set_full|value_alt_rogue`: Rogue hex 5-50 + 55-100 sets + 2x Rogue 3-tier racks → set $3,905 + rack $1,985 = **$5,890**
- `dumbbell_set_full|value_alt_ff`: French Fitness hex 5-100 + 2x FF 2-tier saddle racks → set $3,329.10 + rack $1,798 = **$5,127.10**
- `dumbbell_set_full|commercial`: LF rubber HEX 5-50/55-75/80-100 + LF 2-tier + LF 3-tier long saddle (5-75) → set $6,115 + rack $3,993 = **$10,108**
- `dumbbell_set_full|commercial_alt_rep_urethane`: REP urethane 5-100 + 2x REP commercial racks → set $5,699.99 + rack $1,299.98 = **$6,999.97**
- `dumbbell_set_full|premium`: HS 4-sided urethane 5-100 + 2x HS 2-tier racks → set $16,662 + rack $3,512 = **$20,174**
- `dumbbell_set_full|premium_alt_12sided`: HS 12-sided urethane 5-100 + 2x HS 2-tier racks → set $21,702 + rack $3,512 = **$25,214**
- `dumbbell_heavy_extension|value`: French Fitness rubber hex 105-150 set + 2-tier rack (value typical $770) → set $4,699 + rack $770 = **$5,469**
- `dumbbell_heavy_extension|value_alt_rep`: REP hex 105-125 pairs + REP urethane 130-150 set (sale) + REP rack → set $4,809.94 + rack $649.99 = **$5,459.93**
- `dumbbell_heavy_extension|commercial`: REP urethane 105-125 + 130-150 (regular price) + REP commercial rack → set $6,299.98 + rack $649.99 = **$6,949.97**
- `dumbbell_heavy_extension|commercial_alt_rogue`: Rogue urethane 105-150 set + Rogue 3-tier rack → set $9,950 + rack $992.50 = **$10,942.50**
- `dumbbell_heavy_extension|premium`: HS 4-sided urethane 105-125 + 130-150 + HS 2-tier rack → set $16,998 + rack $1,756 = **$18,754**
- `kettlebell_set|value`: Rogue kettlebells 9/13/18/26/35/44/53/62/70 lb + REP Kettlebell Rack 2.0 two-tier → set $721 + rack $449.99 = **$1,170.99**
- `kettlebell_set|value_alt_ff`: French Fitness cast-iron KB set 5-50 lb (10 bells) + FF 3-tier KB rack → set $439 + rack $379 = **$818**
- `kettlebell_set|commercial`: Life Fitness cast iron 4-32 kg (9 bells) + LF 3-Tier Accessory Rack → set $1,016 + rack $1,549 = **$2,565**
- `kettlebell_set|premium`: Hammer Strength competition KBs 8-32 kg (9 bells) + LF 3-Tier Accessory Rack → set $1,651 + rack $1,549 = **$3,200**
- `fixed_barbell_set|value`: Titan fixed urethane straight 20-110 + EZ 20-110 sets + 2x Titan fixed barbell racks → set $2,974.94 + rack $719.94 = **$3,694.88**
- `fixed_barbell_set|value_alt_bodysolid`: Body-Solid SBB fixed barbell set (10 bars) + SBBR100 rack (straight only) → set $1,495 + rack $665 = **$2,160**
- `fixed_barbell_set|commercial`: Hammer Strength 4-sided RUBBER straight + EZ 20-110 + LF Barbell Rack → set $7,044 + rack $1,659 = **$8,703**
- `fixed_barbell_set|commercial_alt_hoist`: Hoist 20-110 straight & curl set + Hoist CF-3465 barbell rack → set $7,590 + rack $1,480 = **$9,070**
- `fixed_barbell_set|premium`: Hammer Strength 4-sided URETHANE straight + EZ 20-110 + LF Barbell Rack → set $12,168 + rack $1,659 = **$13,827**
- `fixed_barbell_set|premium_alt_12sided`: Hammer Strength 12-sided urethane straight + EZ 20-110 + LF Barbell Rack → set $16,278 + rack $1,659 = **$17,937**

Set weights used: 5–50 pairs = 550 lb; 55–100 = 1,550 lb; 5–100 = 2,100 lb; 105–125 = 1,150 lb; 130–150 = 1,400 lb; 105–150 = 2,550 lb (2 × sum of 5-lb increments).

## 6. Recommended model prices per item and tier (new equipment)

Typical = median of the anchor listings in §7 (AK-dealer prices ÷1.45), rounded. `est` = estimate/override with derivation in the note.

| Item (taxonomy id) | VALUE | COMMERCIAL | PREMIUM | REFURB est. (0.5 x premium) | Notes |
|---|---|---|---|---|---|
| power_rack_frame | $870 ($520–$1,500) | $2,950 ($1,850–$3,750) | $4,650 ($3,900–$6,600) | $2,300 |  |
| half_rack_frame | $730 ($560–$1,050) | $1,900 ($1,400–$5,400) | $4,600 ($3,500–$6,250) | $2,300 |  |
| smith_machine | $2,250 ($1,400–$3,200) | $5,450 ($3,050–$7,400) | $7,450 ($5,250–$7,650) | $3,700 |  |
| olympic_barbell | $260 ($170–$280) | $310 ($300–$380) | $700 ($650–$850) | — |  |
| bench_press_station_bench | $900 ($610–$1,000) | $1,600 ($860–$1,900) | $1,950 ($1,650–$2,600) | $1,000 |  |
| incline_bench_station_bench | $1,000 ($660–$1,300) | $1,700 ($980–$2,200) | $2,500 ($1,950–$2,700) | $1,250 |  |
| decline_bench_station_bench | $860 ($620–$1,100) | $1,700 ($1,200–$2,200) | $2,250 ($1,950–$2,500) | $1,100 |  |
| adjustable_bench | $510 ($310–$600) | $1,050 ($680–$1,500) | $1,600 ($1,150–$2,000) | $800 |  |
| flat_bench | $280 ($200–$340) | $820 ($400–$920) | $850 ($770–$1,330) est | $400 | premium: HS Flat Bench $772 / HS Utility 75-deg $849 list; Matrix Magnum Pro flat & Nautilus flat (AK) higher; set at HS level |
| preacher_bench | $440 ($410–$460) | $1,350 ($660–$1,800) | $1,550 ($1,200–$1,700) | $800 |  |
| hyperextension | $310 ($220–$330) | $1,350 ($630–$1,950) | $1,700 ($1,600–$1,800) | $850 |  |
| ghd | $550 ($440–$760) | $1,300 ($680–$1,900) | $2,800 ($2,250–$3,600) | $1,400 |  |
| dip_chin_station | $660 ($360–$1,450) | $2,000 ($1,100–$2,600) | $2,100 ($1,750–$2,400) | $1,050 |  |
| hip_thrust_machine | $1,150 ($1,000–$1,250) | $4,350 ($4,300–$4,400) | $5,300 ($4,900–$8,400) | $2,650 |  |
| hip_thrust_bench | $280 ($270–$300) | $330 ($330–$330) | $350 ($330–$450) est | — | premium: no premium hip-thrust bench listing; Rogue Monster Hip Thruster Bench $330 + allowance (estimate) |
| landmine | $100 ($100–$200) | $160 ($120–$200) | $200 ($165–$200) est | — | premium: premium rack-mount landmine ~ Prime Prodigy landmine attachment $200 / Rogue Monster Landmine 2.0 $165 |
| leg_press | $2,350 ($1,550–$2,800) | $4,500 ($2,700–$7,400) | $6,550 ($4,900–$7,900) | $3,300 |  |
| hack_squat | $2,050 ($970–$2,800) | $5,600 ($4,300–$6,650) | $5,700 ($5,100–$7,900) | $2,850 |  |
| belt_squat | $1,200 ($1,000–$2,400) | $4,300 ($2,400–$4,300) est | $5,550 ($4,850–$6,300) | $2,800 | commercial: single new commercial listing (Nautilus PL belt squat $4,299); Rogue Monster Rhino stand-alone $2,415 is the low bound |
| pendulum_squat | $1,750 ($1,400–$2,500) | $6,250 ($5,600–$6,650) est | $7,200 ($5,600–$8,800) | $3,600 | commercial: single listing Prime PL pendulum squat $6,250 |
| leg_extension | $2,700 ($2,550–$2,800) | $5,150 ($3,100–$5,800) | $6,950 ($5,450–$8,300) | $3,500 |  |
| leg_curl | $2,550 ($2,400–$3,300) | $5,000 ($3,300–$6,850) | $7,250 ($5,850–$8,500) | $3,600 |  |
| leg_ext_curl_combo | $3,150 ($2,600–$3,750) | $4,800 ($3,600–$6,500) | $6,500 ($5,800–$7,000) est | $3,250 | premium: premium lines sell separate leg ext/curl; estimate from Prime Hybrid combo $6,500 and Axiom seated combo $5,776 (low confidence) |
| hip_abductor_adductor | $2,550 ($2,150–$3,800) | $4,400 ($3,250–$6,000) | $6,900 ($6,000–$9,100) | $3,450 |  |
| glute_kickback | $2,500 ($660–$3,300) | $4,800 ($3,800–$5,900) | $7,150 ($6,900–$7,750) | $3,600 |  |
| calf_raise | $1,000 ($750–$1,200) est | $1,600 ($1,520–$1,620) est | $2,350 ($1,000–$2,350) est | $1,200 | value: plate-loaded seated calf: Body-Solid GSCR349 $750, French Fitness FFB $1,199; commercial: plate-loaded seated calf: Hoist ROC-IT RPL-5363 $1,615; Nautilus tilt-seat $1,519; premium: plate-loaded seated calf: Hammer Strength $2,352 (Sorinex seated calf $999 is the low bound) |
| calf_raise_selectorized | — | $5,750 ($5,599–$5,900) est | $6,950 ($6,298–$7,635) est | $3,500 | commercial: Nautilus Impact standing calf $5,599; Prime Hybrid seated calf press $5,900; premium: HS Select Standing Calf $6,298; LF Insignia Calf Extension $7,635 |
| leg_press_selectorized | $2,900 ($2,800–$3,000) | $6,550 ($4,850–$8,300) | $9,450 ($8,500–$11,900) | $4,700 |  |
| chest_press | $2,800 ($2,800–$3,000) | $5,050 ($2,950–$6,250) | $7,050 ($5,950–$8,400) | $3,500 |  |
| pec_fly_rear_delt | $2,800 ($2,200–$2,800) | $5,250 ($2,850–$5,900) | $7,100 ($5,950–$7,850) | $3,550 |  |
| shoulder_press | $2,800 ($2,100–$3,000) | $5,050 ($3,100–$6,150) | $7,100 ($5,800–$7,850) | $3,550 |  |
| lat_pulldown | $2,900 ($2,800–$3,000) | $5,050 ($2,950–$6,850) | $7,200 ($4,950–$8,000) | $3,600 |  |
| seated_row | $2,900 ($2,800–$3,000) | $5,050 ($2,600–$5,950) | $7,050 ($5,950–$7,750) | $3,500 |  |
| lat_pulldown_row_combo | $2,800 ($1,350–$3,250) | $3,650 ($3,400–$5,250) | $5,900 ($5,250–$6,550) est | $2,950 | premium: single listing: Hammer Strength Dual Pulldown/Row $5,889 |
| assisted_pullup_dip | $2,800 ($2,150–$3,800) | $5,050 ($3,650–$6,250) | $7,600 ($6,800–$8,400) | $3,800 |  |
| biceps_curl_machine | $2,300 ($2,100–$2,800) | $4,900 ($2,850–$5,800) | $6,450 ($5,350–$7,750) | $3,200 |  |
| triceps_machine | $2,800 ($2,800–$3,300) | $4,750 ($2,950–$5,800) | $6,950 ($5,500–$7,300) | $3,500 |  |
| ab_crunch_machine | $2,800 ($2,000–$3,000) | $4,900 ($2,500–$5,800) | $6,850 ($6,000–$7,750) | $3,400 |  |
| back_extension_machine | $2,500 ($2,500–$2,500) | $5,600 ($2,850–$5,800) | $7,050 ($5,800–$8,000) | $3,500 |  |
| rotary_torso | $3,000 ($3,000–$3,000) | $5,100 ($3,800–$6,100) | $6,950 ($4,750–$8,150) | $3,500 |  |
| plate_loaded_chest_press | $1,750 ($800–$2,400) | $4,000 ($3,800–$4,300) | $4,150 ($3,500–$5,000) | $2,100 |  |
| plate_loaded_row | $1,850 ($400–$2,400) | $3,800 ($3,700–$4,300) | $3,950 ($3,600–$4,150) | $2,000 |  |
| plate_loaded_shoulder_press | $1,150 ($560–$2,400) | $3,800 ($3,800–$4,300) | $4,150 ($4,150–$4,150) | $2,100 |  |
| plate_loaded_high_row | $2,400 ($1,550–$2,400) | $4,050 ($3,800–$4,300) | $4,150 ($3,400–$4,150) | $2,100 |  |
| t_bar_row | $990 ($400–$1,600) | $1,850 ($1,500–$2,200) | $3,050 ($2,850–$3,950) | $1,500 |  |
| multi_station_gym | $5,700 ($5,000–$7,550) | $10,400 ($7,650–$10,750) | $13,500 ($10,750–$14,900) est | $6,750 | premium: no new premium 3-4 stack listing; estimate = commercial typical x1.3; Matrix Aura 4-stack $14,898 (AK list) and Hoist 6-station pod $14,455 bracket the top |
| cable_crossover | $3,800 ($2,750–$5,600) | $7,000 ($6,700–$8,400) | $8,350 ($7,350–$9,350) | $4,200 |  |
| functional_trainer | $2,500 ($2,200–$3,100) | $6,250 ($4,700–$6,800) | $8,850 ($5,800–$10,050) | $4,400 |  |
| cable_column | $2,800 ($2,300–$3,100) | $2,850 ($2,550–$3,150) | $3,700 ($3,160–$4,500) est | $1,850 | premium: no new premium single-column listing found; estimate = commercial typical x1.3 (low confidence) |
| dumbbell_rack_2tier | $770 ($650–$900) | $1,600 ($1,250–$1,900) | $1,600 ($1,450–$1,750) | — |  |
| dumbbell_rack_3tier | $950 ($840–$1,150) | $1,600 ($1,300–$2,000) | $2,050 ($2,050–$2,050) | — |  |
| plate_tree | $230 ($180–$290) | $940 ($800–$1,100) | $1,000 ($800–$1,210) est | — | premium: no Hammer Strength tree found; bracketed by LF Olympic Weight Tree $800, Hoist 4-sided $1,075, Nautilus 2-sided $1,208 (AK list) |
| kettlebell_rack | $380 ($340–$580) | $1,350 ($1,150–$1,550) | $1,550 ($1,130–$1,550) est | — | premium: LF 3-Tier Accessory Rack $1,549 used as premium storage |
| barbell_rack | $400 ($360–$660) | $1,250 ($1,050–$1,500) | $1,700 ($1,650–$1,700) | — |  |

## 7. Anchor listings (evidence) per item and tier

### power_rack_frame

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | REP Fitness PR-4000 Power Rack (Pre-Selected) | $799.94 | $799.94 | https://repfitness.com/products/pr-4000-power-rack-pre-selected |
| value | REP Fitness PR-5000 Power Rack (Pre-Selected) | $919.99 | $919.99 | https://repfitness.com/products/pr-5000-power-rack-pre-selected |
| value | Titan Fitness T-3 Series Power Rack | $519.97 | $519.97 | https://titan.fitness/products/t-3-series-power-rack-82-24 |
| value | Titan Fitness X-3 Series Bolt Down Power Rack | $634.97 | $634.97 | https://titan.fitness/products/x-3-series-bolt-down-power-rack-80-24 |
| value | Rogue Bolt-Together R-3 | $870 | $870 | https://www.roguefitness.com/rogue-bolt-together-r-3 |
| value | Rogue RML-390 Power Rack 3.0 | $1,015 | $1,015 | https://www.roguefitness.com/rogue-rigs-racks/power-racks |
| value | Body-Solid GPR400 Power Rack | $840 | $840 | https://fitnesssuperstore.com/products/body-solid-gpr400-power-rack-new |
| value | Body-Solid SPR1000 Commercial Power Rack | $1,500 | $1,500 | https://fitnesssuperstore.com/products/body-solid-spr1000-commercial-power-rack-new |
| value | Bells of Steel Hydra Four Post Power Rack - Prebuilt | $1,280.89 | $1,280.89 | https://www.bellsofsteel.us/products/hydra-four-post-power-rack-prebuilt |
| commercial | Rogue RM-4 Monster Rack 2.0 | $1,830 | $1,830 | https://www.roguefitness.com/rogue-rigs-racks/power-racks |
| commercial | Rogue RM-6 Monster Rack 2.0 | $2,855 | $2,855 | https://www.roguefitness.com/rogue-rigs-racks/power-racks |
| commercial | Prime PRODIGY / Power Rack | $2,300 | $2,300 | https://www.primefitnessusa.com/products/prodigy-power-rack |
| commercial | Hoist CF-3364 Power Cage | $3,090 | $3,090 | https://www.hoistfitness.com/products/cf-3364-power-cage-gsa |
| commercial | Torque TR2 Power Rack | $5,443 | $3,753.79 | https://akfit.com/products/torque-tr2-power-rack |
| commercial | Nautilus Power Cage Rack | $5,358 | $3,695.17 | https://akfit.com/products/power-cage-rack |
| premium | Hammer Strength HD Athletic NX Power Rack | $4,657 | $4,657 | https://shop.lifefitness.com/products/hammer-strength-hd-athletic-nx-power-rack |
| premium | Rogers Athletic Pendulum Full Rack | $5,651.10 | $3,897.31 | https://akfit.com/products/full-rack |
| premium | Matrix Magnum MEGA Power Rack 8' | $9,598.83 | $6,619.88 | https://akfit.com/products/matrix-magnum-mega-power-rack-8 |

### half_rack_frame

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | REP Fitness Apollo - Half Rack Builder | $919.96 | $919.96 | https://repfitness.com/products/apollo-rack-builder |
| value | Rogue HR-2 Half Rack | $765 | $765 | https://www.roguefitness.com/rogue-hr-2-half-rack |
| value | Titan Fitness T-3 Series Half Rack | $564.97 | $564.97 | https://titan.fitness/products/t-3-series-half-rack |
| value | Titan Fitness X-3 Series Half Rack | $664.97 | $664.97 | https://titan.fitness/products/x-3-series-half-rack |
| value | Body-Solid SPR500 ProClub Line Commercial Half Rack | $690 | $690 | https://fitnesssuperstore.com/products/body-solid-spr500-proclub-line-commercial-half-rack-new |
| value | Bells of Steel Hydra Half Rack - Prebuilt | $1,052.92 | $1,052.92 | https://www.bellsofsteel.us/products/hydra-half-rack-prebuilt |
| commercial | Rogue Monster Lite Half Rack | $1,425 | $1,425 | https://www.roguefitness.com/monster-lite-half-rack |
| commercial | Rogue Monster Collegiate Half Rack | $1,600 | $1,600 | https://www.roguefitness.com/monster-half-racks |
| commercial | Prime PRODIGY / Half Rack | $1,500 | $1,500 | https://www.primefitnessusa.com/products/prodigy-half-rack |
| commercial | Nautilus Half Rack 9-HDHR2 | $3,869 | $3,869 | https://fitnesssuperstore.com/products/nautilus-half-rack-9-hdhr2-new |
| commercial | Torque TR1 Half Rack 8' | $3,180 | $2,193.10 | https://akfit.com/products/torque-tr1-8-ft-half-rack |
| commercial | Hoist CF-3365 Commercial Half Rack | $5,380 | $5,380 | https://www.hoistfitness.com/products/cf-3365-half-rack |
| premium | Hammer Strength HD Athletic NX Half Rack | $3,706 | $3,706 | https://shop.lifefitness.com/products/hammer-strength-hd-athletic-nx-half-rack |
| premium | Hammer Strength HD Elite iD Half Rack | $6,229 | $6,229 | https://shop.lifefitness.com/products/hammer-strength-hd-elite-id-half-rack |
| premium | Rogers Athletic Pendulum Basic Half Rack | $5,099.10 | $3,516.62 | https://akfit.com/products/basic-half-rack |
| premium | Matrix Magnum PRO Half Rack | $7,959.35 | $5,489.21 | https://akfit.com/products/magnum-pro-half-rack |

### smith_machine

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Titan Fitness Smith Machine | $1,799.97 | $1,799.97 | https://titan.fitness/products/smith-machine |
| value | Bells of Steel Smith Machine - Hydra | $1,423.99 | $1,423.99 | https://www.bellsofsteel.us/products/hydra-squat-stand-smith-machine-prebuilt |
| value | Body-Solid SCB1000B ProClub Line Counter-Balanced Smith Machine | $2,660 | $2,660 | https://fitnesssuperstore.com/products/body-solid-scb1000b-proclub-line-counter-balanced-smith-machine-new |
| value | French Fitness FFB Black Elite Smith Machine | $3,199 | $3,199 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-elite-smith-machine-new |
| commercial | Life Fitness Axiom Series Smith Rack | $4,863 | $4,863 | https://shop.lifefitness.com/products/axiom-series-smith-rack |
| commercial | Hoist CF-3755 Dual Angle Smith | $6,050 | $6,050 | https://www.hoistfitness.com/products/cf-3755-dual-angle-smith |
| commercial | Hoist CF-3754 Dual Action Smith | $7,395 | $7,395 | https://www.hoistfitness.com/products/cf-3754-dual-action-smith |
| commercial | Matrix G1 Smith Machine | $4,440 | $3,062.07 | https://akfit.com/products/varsity-smith-machine |
| premium | Hammer Strength Smith Machine | $7,442 | $7,442 | https://shop.lifefitness.com/products/hammer-strength-smith-machine-1 |
| premium | Life Fitness Smith Machine | $7,641 | $7,641 | https://shop.lifefitness.com/products/life-fitness-smith-machine |
| premium | Watson Counter Balance Smith Machine | $7,634.03 | $5,264.85 | https://akfit.com/products/watson-counter-balance-smith-machine |

### olympic_barbell

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | REP Fitness Delta Basic Bar | $199.99 | $199.99 | https://repfitness.com/products/delta-basic-bar |
| value | REP Fitness Black Canyon Bar - 20kg | $259.99 | $259.99 | https://repfitness.com/products/black-canyon-bar-20kg |
| value | Titan Fitness Performance Series Olympic Barbell | $167.97 | $167.97 | https://titan.fitness/products/performance-series-olympic-barbell |
| value | Titan Fitness Elite Series Olympic Barbell | $264.97 | $264.97 | https://titan.fitness/products/elite-series-olympic-barbell |
| value | Rogue Echo Bar 2.0 | $285 | $285 | https://www.roguefitness.com/rogue-echo-bar |
| value | Bells of Steel Multi-Purpose Olympic Barbell – The Utility Bar | $261.99 | $261.99 | https://www.bellsofsteel.us/products/multi-purpose-barbell |
| commercial | Rogue The Ohio Bar - Black Zinc | $305 | $305 | https://www.roguefitness.com/the-ohio-bar-black-zinc |
| commercial | Rogue 45LB Ohio Power Bar - Black Zinc | $315 | $315 | https://www.roguefitness.com/rogue-45lb-ohio-power-bar-black-zinc |
| commercial | Rogue The Ohio Bar - Stainless Steel | $385 | $385 | https://www.roguefitness.com/the-ohio-bar-stainless-steel |
| commercial | REP Fitness Colorado Bar - 20kg | $299.99 | $299.99 | https://repfitness.com/products/colorado-bar-20kg |
| commercial | Torque Fitness 7' Force Premium Barbell | $305 | $305 | https://www.torquefitness.com/products/7-force-premium-barbell |
| commercial | TITAN Series Cerakote Olympic Barbell | $349.97 | $349.97 | https://titan.fitness/products/titan-series-cerakote-olympic-barbell |
| premium | Hammer Strength Olympic WL Bar men 20 kg hard chrome | $684 | $684 | https://shop.lifefitness.com/products/hammer-strength-olympic-weightlifting-bars |
| premium | Hammer Strength Olympic WL Bar men 20 kg Cerakote | $718 | $718 | https://shop.lifefitness.com/products/hammer-strength-olympic-weightlifting-bars |
| premium | Hammer Strength Power Bars | $853 | $853 | https://shop.lifefitness.com/products/hammer-strength-power-bars |
| premium | Rogue Olympic Weightlifting Bar - Stainless Steel | $650 | $650 | https://www.roguefitness.com/rogue-olympic-weightlifting-bar-stainless-steel |

### bench_press_station_bench

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Body-Solid SOFB250 Pro Clubline Olympic Flat Bench | $610 | $610 | https://fitnesssuperstore.com/products/body-solid-sofb250-pro-clubline-olympic-flat-bench-new |
| value | French Fitness FFB Black Olympic Flat Bench Press | $999 | $999 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-olympic-flat-bench-press-new |
| value | Rogue Westside Bench 2.0 | $895 | $895 | https://www.roguefitness.com/rogue-westside-bench-2-0 |
| commercial | Life Fitness Olympic Flat Bench | $1,789 | $1,789 | https://shop.lifefitness.com/products/signature-series-olympic-flat-bench |
| commercial | Hoist CF-3170 Olympic Flat Bench w/ storage | $1,880 | $1,880 | https://www.hoistfitness.com/products/cf-3170-olympic-flat-bench |
| commercial | Nautilus Instinct Olympic Flat Bench 9NN-B7503-60ARS | $1,249 | $1,249 | https://fitnesssuperstore.com/products/nautilus-instinct-olympic-flat-bench-9nn-b7503-60ars-new |
| commercial | Matrix G1 Olympic Flat Bench | $1,240.55 | $855.55 | https://akfit.com/products/matrix-g1-olympic-flat-bench |
| commercial | Rogue Monster Westside Bench | $1,595 | $1,595 | https://www.roguefitness.com/rogue-monster-west-side-bench |
| premium | Life Fitness Olympic Flat Bench w/ storage | $2,623 | $2,623 | https://shop.lifefitness.com/products/signature-series-olympic-flat-bench |
| premium | Matrix Magnum Olympic Flat Bench | $2,801.06 | $1,931.77 | https://akfit.com/products/matrix-magnum-olympic-flat-bench-with-integrated-s |
| premium | Matrix Magnum Breaker Olympic Flat Bench | $3,261.36 | $2,249.21 | https://akfit.com/products/matrix-magnum-breaker-olympic-flat-bench-w-integra |
| premium | Nautilus Olympic Bench Press | $2,529 | $1,744.14 | https://akfit.com/products/olympic-bench-press |
| premium | Sorinex XL Series Competition Bench | $1,649 | $1,649 | https://www.sorinex.com/products/competition-bench |

### incline_bench_station_bench

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Body-Solid SOIB250 Pro Clubline Olympic Incline Bench | $665 | $665 | https://fitnesssuperstore.com/products/body-solid-soib250-pro-clubline-olympic-incline-bench-new |
| value | French Fitness FFB Black Olympic Incline Bench | $999 | $999 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-olympic-incline-bench-new |
| value | French Fitness Napa Olympic Incline Bench w/Weight Storage | $1,299 | $1,299 | https://fitnesssuperstore.com/products/french-fitness-napa-olympic-incline-bench-w-weight-storage-new |
| commercial | Life Fitness Olympic Incline Bench | $1,817 | $1,817 | https://shop.lifefitness.com/products/life-fitness-olympic-incline-bench |
| commercial | Hoist CF-3172 Olympic Incline Bench w/ storage | $2,220 | $2,220 | https://www.hoistfitness.com/products/cf-3172-olympic-incline-bench |
| commercial | Nautilus Instinct Olympic Incline Bench 9NN-B7201-60ARS | $1,559 | $1,559 | https://fitnesssuperstore.com/products/nautilus-instinct-olympic-incline-bench-9nn-b7201-60ars-new |
| commercial | Matrix G1 Olympic Incline Bench | $1,425.79 | $983.30 | https://akfit.com/products/matrix-g1-incline-bench-press |
| premium | Life Fitness Olympic Incline Bench w/ storage | $2,651 | $2,651 | https://shop.lifefitness.com/products/life-fitness-olympic-incline-bench |
| premium | Matrix Magnum Olympic Incline Bench | $3,457.82 | $2,384.70 | https://akfit.com/products/matrix-magnum-olympic-incline-bench-w-integrated-s |
| premium | Matrix Magnum Breaker Olympic Incline Bench | $3,918.12 | $2,702.15 | https://akfit.com/products/matrix-magnum-breaker-olympic-incline-bench-w-inte |
| premium | Nautilus Incline Bench Press | $2,820 | $1,944.83 | https://akfit.com/products/olympic-incline-bench-press |

### decline_bench_station_bench

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Body-Solid SODB250 Pro Clubline Olympic Decline Bench | $625 | $625 | https://fitnesssuperstore.com/products/body-solid-sodb250-pro-clubline-olympic-decline-bench-new |
| value | French Fitness FFB Black Olympic Decline Bench | $1,099 | $1,099 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-olympic-decline-bench-new |
| commercial | Hoist CF-3177 Olympic Decline Bench w/ storage | $2,220 | $2,220 | https://www.hoistfitness.com/products/cf-3177-olympic-decline-bench |
| commercial | Matrix G1 Olympic Decline Bench | $1,768.21 | $1,219.46 | https://akfit.com/products/matrix-g1-olympic-decline-bench |
| premium | Matrix Magnum Olympic Decline Bench | $3,233.29 | $2,229.86 | https://akfit.com/products/matrix-magnum-olympic-decline-bench-w-integrated-s |
| premium | Matrix Magnum Breaker Olympic Decline Bench | $3,659.90 | $2,524.07 | https://akfit.com/products/matrix-magnum-breaker-olympic-decline-bench-w-inte |
| premium | Nautilus Olympic Decline Bench Press | $2,820 | $1,944.83 | https://akfit.com/products/olympic-decline-bench-press |

### adjustable_bench

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | REP Fitness AB-3000 2.0 FID Adjustable Weight Bench | $349.99 | $349.99 | https://repfitness.com/products/ab-3000-fid-adjustable-bench |
| value | REP Fitness AB-5200 2.0 Adjustable Bench | $549.99 | $549.99 | https://repfitness.com/products/ab-5200-2-0 |
| value | Rogue Adjustable Bench 3.0 | $595 | $595 | https://www.roguefitness.com/rogue-adjustable-bench-3-0 |
| value | Titan Fitness Elite Series Adjustable FID Bench | $309.97 | $309.97 | https://titan.fitness/products/single-post-adjustable-fid-bench |
| value | Body-Solid SFID325B Pro Clubline Adjustable Commercial Bench | $505 | $505 | https://fitnesssuperstore.com/products/body-solid-sfid325b-pro-clubline-adjustable-commercial-bench-new |
| value | Bells of Steel Buzz-Saw Heavy-Duty Adjustable Bench | $516.99 | $516.99 | https://www.bellsofsteel.us/products/buzz-saw-bench |
| commercial | Life Fitness Adjustable Bench | $1,495 | $1,495 | https://shop.lifefitness.com/products/life-fitness-adjustable-bench |
| commercial | Hoist 7-Position F.I.D. Bench (base) | $675 | $675 | https://www.hoistfitness.com/products/hf-5165-7-position-f-i-d-bench |
| commercial | Nautilus Instinct Multi-Adjustable Bench 9NN-B7501-60ARS | $1,179 | $1,179 | https://fitnesssuperstore.com/products/nautilus-instinct-multi-adjustable-bench-9nn-b7501-60ars-new |
| commercial | Prime Adjustable Bench | $725 | $725 | https://www.primefitnessusa.com/products/bench |
| commercial | Sorinex 0-90 NP4 Adjustable Bench | $1,249 | $1,249 | https://www.sorinex.com/products/0-90-np4-adjustable-bench |
| commercial | Rogue AB-3 Adjustable Bench | $950 | $950 | https://www.roguefitness.com/rogue-ab-3-adjustable-bench |
| premium | Life Fitness Multi-Adjustable Bench | $2,001 | $2,001 | https://shop.lifefitness.com/products/life-fitness-multi-adjustable-bench |
| premium | Hammer Strength Multi-Adjustable Bench | $1,854 | $1,854 | https://shop.lifefitness.com/products/hammer-strength-multi-adjustable-bench |
| premium | Matrix Magnum Multi-Adjustable Bench | $1,700 | $1,172.41 | https://akfit.com/products/matrix-magnum-pro-flat-to-incline-bench-w-wheels |
| premium | Nautilus Multi-Adjustable Bench | $2,344.62 | $1,616.98 | https://akfit.com/products/multi-adjustable-bench |
| premium | Watson Adjustable Bench | $2,127.04 | $1,466.92 | https://akfit.com/products/watson-adjustable-bench |

### flat_bench

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | REP Fitness FB-5000 Competition Flat Bench | $244.99 | $244.99 | https://repfitness.com/products/fb-5000-competition-flat-bench |
| value | Rogue Flat Utility Bench 2.0 | $195 | $195 | https://www.roguefitness.com/rogue-flat-utility-bench-2-0 |
| value | Rogue Monster Utility Bench 2.0 | $335 | $335 | https://www.roguefitness.com/monster-utility-bench-2-0-mg-black |
| value | TITAN Series Single Post Flat Bench | $249.97 | $249.97 | https://titan.fitness/products/titan-series-single-post-flat-bench |
| value | Body-Solid Pro Clubline SFB125 Flat Bench | $335 | $335 | https://fitnesssuperstore.com/products/body-solid-pro-clubline-sfb125-flat-bench-new |
| value | Sorinex Flat Bench | $309 | $309 | https://www.sorinex.com/products/flat-bench |
| commercial | Life Fitness Flat Bench | $834 | $834 | https://shop.lifefitness.com/products/life-fitness-flat-bench |
| commercial | Life Fitness Utility Bench | $917 | $917 | https://shop.lifefitness.com/products/signature-series-utility-bench |
| commercial | Hoist CF-3163 Flat Bench | $805 | $805 | https://www.hoistfitness.com/products/cf-3163-flat-bench |
| commercial | Matrix G1 Flat Bench | $583.79 | $402.61 | https://akfit.com/products/g1-flat-bench |
| premium | Hammer Strength Flat Bench | $772 | $772 | https://shop.lifefitness.com/products/hammer-strength-flat-bench |
| premium | Hammer Strength Utility Bench - 75 Degree | $849 | $849 | https://shop.lifefitness.com/products/hammer-strength-utility-bench |
| premium | Matrix Magnum Pro Flat Bench | $707.28 | $487.78 | https://akfit.com/products/matrix-magnum-flat-bench |
| premium | Nautilus Flat Bench | $1,333 | $919.31 | https://akfit.com/products/flat-bench |

### preacher_bench

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Body-Solid GPCB329B Preacher Curl Bench | $460 | $460 | https://fitnesssuperstore.com/products/body-solid-gpcb329b-preacher-curl-bench-new |
| value | Titan Fitness Preacher Curl Bench | $410.97 | $410.97 | https://titan.fitness/products/preacher-curl-bench-v3 |
| commercial | Hoist CF-3550 Preacher Curl | $1,345 | $1,345 | https://www.hoistfitness.com/products/cf-3550-preacher-curl |
| commercial | Life Fitness Arm Curl Bench | $1,789 | $1,789 | https://shop.lifefitness.com/products/life-fitness-arm-curl-bench |
| commercial | Matrix G1 Preacher Curl | $954.27 | $658.12 | https://akfit.com/products/matrix-g1-preacher-curl |
| commercial | Prime DOUBLE-SIDED PREACHER | $1,350 | $1,350 | https://www.primefitnessusa.com/products/double-sided-preacher |
| premium | Hammer Strength Seated Arm Curl | $1,709 | $1,709 | https://shop.lifefitness.com/products/hammer-strength-seated-arm-curl |
| premium | Sorinex Standing Preacher Curl | $1,188 | $1,188 | https://www.sorinex.com/products/standing-preacher-curl |
| premium | Nautilus Seated Preacher Curl | $2,278 | $1,571.03 | https://akfit.com/products/seated-preacher-curl |

### hyperextension

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Body-Solid GHYP345B 45 Degree Back Hyperextension | $295 | $295 | https://fitnesssuperstore.com/products/body-solid-ghyp345b-45-degree-back-hyperextension-new |
| value | French Fitness 45 Degree Back Hyperextension HE450 | $329 | $329 | https://fitnesssuperstore.com/products/french-fitness-45-degree-back-hyperextension-he450-new |
| value | Titan Fitness Roman Chair Back Hyperextension | $224.97 | $224.97 | https://titan.fitness/products/back-hyperextension |
| value | Titan Fitness Dual Hyperextension | $319.97 | $319.97 | https://titan.fitness/products/dual-hyperextension |
| commercial | Hoist CF-3663 Back Hyper | $1,480 | $1,480 | https://www.hoistfitness.com/products/cf-3663-back-hyper |
| commercial | Life Fitness Back Extension | $1,937 | $1,937 | https://shop.lifefitness.com/products/signature-series-back-extension |
| commercial | Nautilus Instinct 45 Degree Back Extension 9NN-B7502-60ARS | $1,249 | $1,249 | https://fitnesssuperstore.com/products/nautilus-instinct-45-degree-back-extension-9nn-b7502-60ars-new |
| commercial | Matrix G1 Back Extension Bench | $914.98 | $631.02 | https://akfit.com/products/g1-back-extension-bench |
| premium | Hammer Strength Back Extension | $1,794 | $1,794 | https://shop.lifefitness.com/products/hammer-strength-back-extension |
| premium | Nautilus Adjustable Back Extension | $2,348 | $1,619.31 | https://akfit.com/products/adjustable-back-extension |

### ghd

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | REP Fitness Glute Ham Developer (GHD) | $479.99 | $479.99 | https://repfitness.com/products/ghd-glute-ham-developer |
| value | Rogue 3x3 Echo GHD | $445 | $445 | https://www.roguefitness.com/rogue-echo-ghd |
| value | Titan Fitness Glute & Hamstring Developer | $619.97 | $619.97 | https://titan.fitness/products/glute-hamstring-developer |
| value | French Fitness GHD Glute Ham Developer Roman Chair | $549 | $549 | https://fitnesssuperstore.com/products/french-fitness-ghd-glute-ham-developer-roman-chair-new |
| value | Body-Solid SGH500 Glute and Ham Machine | $755 | $755 | https://fitnesssuperstore.com/products/body-solid-sgh500-glute-and-ham-machine-new |
| commercial | Rogue GH-1 GHD | $680 | $680 | https://www.roguefitness.com/rogue-gh-1-ghd |
| commercial | Rogue Abram GHD 2.0 | $775 | $775 | https://www.roguefitness.com/rogue-abram-glute-ham-developer-2-0 |
| commercial | Rogue Monster Swing Arm GHD | $1,780 | $1,780 | https://www.roguefitness.com/rogue-monster-swing-arm-ghd |
| commercial | Torque X-Series Glute Ham Developer | $2,736 | $1,886.90 | https://akfit.com/products/torque-commercial-glute-ham-developer |
| premium | Hammer Strength Fixed Pad Glute/Ham | $2,812 | $2,812 | https://shop.lifefitness.com/products/hammer-strength-fixed-pad-glute-ham-bench |
| premium | Matrix Magnum Glute Ham Bench | $3,295.04 | $2,272.44 | https://akfit.com/products/matrix-magnum-glute-ham-bench |
| premium | Sorinex Frankenhyper | $3,599 | $3,599 | https://www.sorinex.com/products/frankenhyper |

### dip_chin_station

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Body-Solid GVKR82B Deluxe VKR Vertical Knee Raise, Dip, Pull Up | $665 | $665 | https://fitnesssuperstore.com/products/body-solid-gvkr82b-deluxe-vkr-vertical-knee-raise-dip-pull-up-new |
| value | Titan Fitness Heavy-Duty Power Tower | $355.97 | $355.97 | https://titan.fitness/products/heavy-duty-power-tower |
| value | Body-Solid SVKR1000 Pro Club-Line VKR Vertical Knee Raise Chin Dip | $1,450 | $1,450 | https://fitnesssuperstore.com/products/body-solid-svkr1000-pro-club-line-vkr-vertical-knee-raise-chin-dip-new |
| commercial | Hoist CF-3252 Vertical Knee Raise/Dip | $1,075 | $1,075 | https://www.hoistfitness.com/products/cf-3252-vertical-knee-raise-dip |
| commercial | Life Fitness Dip/Leg Raise | $1,730 | $1,730 | https://shop.lifefitness.com/products/life-fitness-dip-leg-raise |
| commercial | Life Fitness Chin/Dip/Leg Raise | $2,615 | $2,615 | https://shop.lifefitness.com/products/life-fitness-chin-dip-leg-raise |
| commercial | Nautilus Pull Up/Dip/Leg Raise | $3,279 | $2,261.38 | https://akfit.com/products/pull-up-dip-leg-raise |
| premium | Hammer Strength Chin/Dip/Leg Raise | $2,422 | $2,422 | https://shop.lifefitness.com/products/hammer-strength-chin-dip-leg-raise |
| premium | Matrix Magnum VKR w/Chin | $2,526.01 | $1,742.08 | https://akfit.com/products/matrix-magnum-vkr-w-chin |

### hip_thrust_machine

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Titan Fitness Standing Hip Thrust Machine | $999.99 | $999.99 | https://titan.fitness/products/standing-hip-thrust-machine |
| value | Bells of Steel Hip Thrust Machine | $1,259.99 | $1,259.99 | https://www.bellsofsteel.us/products/hip-thrust-machine |
| commercial | Nautilus Plate Loaded Glute Drive 9NP-L1131-60BZS | $4,319 | $4,319 | https://fitnesssuperstore.com/products/nautilus-plate-loaded-glute-drive-9np-l1131-60bzs-new |
| commercial | Hoist CF-3416 Glute Thrust | $4,400 | $4,400 | https://www.hoistfitness.com/products/cf-3416-glute-thrust |
| premium | Hammer Strength Plate Loaded Glute Drive | $4,907 | $4,907 | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-glute-drive |
| premium | Life Fitness Insignia Series Glute Bridge | $8,424 | $8,424 | https://shop.lifefitness.com/products/insignia-series-glute-bridge |
| premium | Rogers Athletic Pendulum Performance Hip Press | $7,721.10 | $5,324.90 | https://akfit.com/products/pendulum-performance-hip-press |

### hip_thrust_bench

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Rogue Monster Lite Hip Thruster Bench | $270 | $270 | https://www.roguefitness.com/monster-lite-hip-thruster-bench |
| value | French Fitness FF-HTB20 Hip Thrust Bench Platform | $299 | $299 | https://fitnesssuperstore.com/products/french-fitness-ff-htb20-hip-thrust-bench-platform-new |
| commercial | Rogue Monster Hip Thruster Bench | $330 | $330 | https://www.roguefitness.com/monster-hip-thruster-bench |

### landmine

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | REP Fitness Landmine | $99.99 | $99.99 | https://repfitness.com/products/power-rack-landmine-attachment |
| value | REP Fitness Free Standing Landmine | $99.99 | $99.99 | https://repfitness.com/products/free-standing-landmine |
| value | Rogue Landmine (single) | $105 | $105 | https://www.roguefitness.com/landmines |
| value | Body-Solid Body Solid LMA Landmine | $199 | $199 | https://fitnesssuperstore.com/products/body-solid-lma-landmine-new |
| commercial | Rogue Monster Landmine 2.0 | $165 | $165 | https://www.roguefitness.com/rogue-monster-landmine-2-0 |
| commercial | Prime PRODIGY / Landmine Attachment | $200 | $200 | https://www.primefitnessusa.com/products/prodigy-landmine |
| commercial | Prime RO-T8 / Landmine | $115 | $115 | https://www.primefitnessusa.com/products/prime-landmine |

### leg_press

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | French Fitness FFB Black 45 Degree Linear Leg Press | $2,799 | $2,799 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-45-degree-linear-leg-press-new |
| value | French Fitness Napa Angled Squat Press Plate Loaded | $2,599 | $2,599 | https://fitnesssuperstore.com/products/french-fitness-napa-angled-squat-press-plate-loaded-new |
| value | Body-Solid LVLP Leverage Horizontal Leg Press | $2,790 | $2,790 | https://fitnesssuperstore.com/products/body-solid-lvlp-leverage-horizontal-leg-press-new |
| value | Titan Fitness Leg Press Hack Squat Machine | $1,529.97 | $1,529.97 | https://titan.fitness/products/leg-press-hack-squat-machine |
| value | Bells of Steel Leg Press Hack Squat Machine | $2,053.99 | $2,053.99 | https://www.bellsofsteel.us/products/leg-press-hack-squat-set |
| value | Body-Solid GLPH1100B Leg Press & Hack Squat | $1,735 | $1,735 | https://fitnesssuperstore.com/products/body-solid-glph1100b-leg-press-hack-squat-new |
| commercial | Nautilus Plate Loaded 9NP-L1141 Angled Leg Press | $4,469 | $4,469 | https://fitnesssuperstore.com/products/nautilus-plate-loaded-9np-l1141-angled-leg-press-new |
| commercial | Prime PLATE LOADED / Leg Press | $4,500 | $4,500 | https://www.primefitnessusa.com/products/plate-loaded-leg-press |
| commercial | Hoist CF-3355 Angled Linear Leg Press | $7,395 | $7,395 | https://www.hoistfitness.com/products/cf-3355-angled-linear-leg-press |
| commercial | Hoist ROC-IT RPL-5403 Dual Action Leg Press | $5,720 | $5,720 | https://www.hoistfitness.com/products/rpl-5403-dual-action-leg-press |
| commercial | Torque Commercial Plate Loaded Leg Press | $3,900 | $2,689.66 | https://akfit.com/products/torque-commercial-plate-loaded-leg-press |
| premium | Hammer Strength Plate Loaded Linear Leg Press | $7,883 | $7,883 | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-linear-leg-press |
| premium | Rogue Iso Leg Press 35 | $6,550 | $6,550 | https://www.roguefitness.com/rogue-iso-leg-press-35 |
| premium | Sorinex Leg Press | $6,499 | $6,499 | https://www.sorinex.com/products/leg-press |
| premium | Watson 45 Degree Leg Press | $7,138.69 | $4,923.23 | https://akfit.com/products/watson-45-degree-leg-press-twin-pin |
| premium | Matrix Magnum 45 Degree Leg Press | $10,423.99 | $7,188.96 | https://akfit.com/products/matrix-mg-45-degree-leg-press |

### hack_squat

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | French Fitness Black FFB Linear Hack Squat | $2,799 | $2,799 | https://fitnesssuperstore.com/products/french-fitness-black-ffb-linear-hack-squat-new |
| value | French Fitness Monster P/L Hack Squat Leg Press | $2,499 | $2,499 | https://fitnesssuperstore.com/products/french-fitness-monster-p-l-hack-squat-leg-press-new |
| value | Titan Fitness Plate-Loaded Linear Hack Squat Machine | $974.99 | $974.99 | https://titan.fitness/products/plate-loaded-linear-hack-squat-machine |
| value | Bells of Steel Leg Press Hack Squat Machine | $2,053.99 | $2,053.99 | https://www.bellsofsteel.us/products/leg-press-hack-squat-set |
| value | Body-Solid GLPH1100B Leg Press & Hack Squat | $1,735 | $1,735 | https://fitnesssuperstore.com/products/body-solid-glph1100b-leg-press-hack-squat-new |
| commercial | Nautilus Plate Loaded Hack Squat 9NP-L1130-60BZS | $4,319 | $4,319 | https://fitnesssuperstore.com/products/nautilus-plate-loaded-hack-squat-9np-l1130-60bzs-new |
| commercial | Hoist CF-3356 Hack Squat | $6,185 | $6,185 | https://www.hoistfitness.com/products/cf-3356-hack-squat |
| commercial | Prime PLATE LOADED / Hack Squat | $6,650 | $6,650 | https://www.primefitnessusa.com/products/plate-loaded-hack-squat |
| commercial | Hoist ROC-IT RPL-5356 Hack Squat/Deadlift/Shrug | $4,985 | $4,985 | https://www.hoistfitness.com/products/rpl-5356-hack-squat-dead-lift-shrug |
| premium | Hammer Strength Plate Loaded Hack Squat | $7,883 | $7,883 | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-hack-squat |
| premium | Sorinex Hack Squat Machine | $5,999 | $5,999 | https://www.sorinex.com/products/hack-squat-machine |
| premium | Matrix Magnum Hack Squat | $7,398 | $5,102.07 | https://akfit.com/products/matrix-mg-hack-squat |
| premium | Watson 30 Degree Hack Squat | $7,760.29 | $5,351.92 | https://akfit.com/products/watson-30-degree-hack-squat |

### belt_squat

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Titan Fitness Belt Squat Machine | $999.97 | $999.97 | https://titan.fitness/products/belt-squat-machine |
| value | Bells of Steel Belt Squat Machine | $1,199.99 | $1,199.99 | https://www.bellsofsteel.us/products/belt-squat-machine |
| value | French Fitness FF-BSM20 Belt Squat Machine | $1,199 | $1,199 | https://fitnesssuperstore.com/products/french-fitness-ff-bsm20-belt-squat-machine-new |
| value | French Fitness Belt Squat Training Platform Plate Loaded | $2,299 | $2,299 | https://fitnesssuperstore.com/products/french-fitness-belt-squat-training-platform-plate-loaded-new |
| value | Rogue Monster Rhino Belt Squat - Stand Alone | $2,415 | $2,415 | https://www.roguefitness.com/monster-rhino-belt-squat-stand-alone-mg-black |
| commercial | Nautilus Plate Loaded 9NP-L1132 Belt Squat | $4,299 | $4,299 | https://fitnesssuperstore.com/products/nautilus-plate-loaded-9np-l1132-belt-squat-new |
| premium | Hammer Strength Plate Loaded Belt Squat | $6,284 | $6,284 | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-belt-squat |
| premium | Rogers Athletic Pit Shark Belt Squat (Short) | $7,031.10 | $4,849.03 | https://akfit.com/products/short-pit-shark-base-package |

### pendulum_squat

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Bells of Steel Pandemonium Squat – 3-in-1 Pendulum Squat / Calf Press / Viking Press Machine | $1,749.99 | $1,749.99 | https://www.bellsofsteel.us/products/pandemonium-squat |
| value | French Fitness Marin Pendulum Squat Machine | $2,499 | $2,499 | https://fitnesssuperstore.com/products/french-fitness-marin-pendulum-squat-machine-new |
| value | French Fitness FFB Black Pendulum Squat Leg Press Machine | $1,399 | $1,399 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-pendulum-squat-leg-press-machine-new |
| commercial | Prime PLATE LOADED I Pendulum Squat | $6,250 | $6,250 | https://www.primefitnessusa.com/products/plate-loaded-i-pendulum-squat |
| premium | Hammer Strength Plate Loaded Pendulum-X Squat | $8,820 | $8,820 | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-pendulum-x-squat-1 |
| premium | Rogers Athletic Pendulum Pro Power Squat | $8,135.10 | $5,610.41 | https://akfit.com/products/pendulum-pro-power-squat |

### leg_extension

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Body-Solid SLE200G ProClub Line Leg Extension | $2,565 | $2,565 | https://fitnesssuperstore.com/products/body-solid-sle200g-proclub-line-leg-extension-new |
| value | French Fitness Tahoe Seated Leg Extension | $2,799 | $2,799 | https://fitnesssuperstore.com/products/french-fitness-tahoe-seated-leg-extension-new |
| commercial | Life Fitness Axiom Series Leg Extension | $5,429 | $5,429 | https://shop.lifefitness.com/products/axiom-series-leg-extension |
| commercial | Hoist Club Line CL-3401 Leg Extension | $4,890 | $4,890 | https://www.hoistfitness.com/products/cl-3401-leg-extension |
| commercial | Hoist ROC-IT RS-2401 Leg Extension | $5,805 | $5,805 | https://www.hoistfitness.com/products/rs-2401-leg-extension |
| commercial | Nautilus Instinct Leg Extension 9NL-S1010-60ARS | $3,819 | $3,819 | https://fitnesssuperstore.com/products/nautilus-instinct-leg-extension-9nl-s1010-60ars-new |
| commercial | Nautilus Impact Leg Extension 9NA-S1312-60AGS | $5,599 | $5,599 | https://fitnesssuperstore.com/products/nautilus-impact-leg-extension-9na-s1312-60ags-new |
| commercial | Prime HYBRID / Leg Extension | $5,750 | $5,750 | https://www.primefitnessusa.com/products/hybrid-leg-extension |
| commercial | Matrix Versa Leg Extension | $4,498 | $3,102.07 | https://akfit.com/products/matrix-versa-leg-extension-w-160lbs |
| commercial | Matrix Aura Leg Extension | $6,399.22 | $4,413.26 | https://akfit.com/products/matrix-aura-leg-extension |
| premium | Hammer Strength Select Leg Extension | $6,430 | $6,430 | https://shop.lifefitness.com/products/hammer-strength-select-leg-extension |
| premium | Life Fitness Insignia Series Leg Extension | $8,315 | $8,315 | https://shop.lifefitness.com/products/insignia-series-leg-extension |
| premium | Nautilus Inspiration Leg Extension 9-IPLE5-60BZ | $6,949 | $6,949 | https://fitnesssuperstore.com/products/nautilus-inspiration-leg-extension-9-iple5-60bz-new |
| premium | Prime EVOLUTION / Leg Extension | $5,450 | $5,450 | https://www.primefitnessusa.com/products/evolution-leg-extension |
| premium | Matrix Ultra Leg Extension | $10,446.44 | $7,204.44 | https://akfit.com/products/matrix-leg-extension |

### leg_curl

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Body-Solid SLC400G ProClub Prone Leg Curl | $2,565 | $2,565 | https://fitnesssuperstore.com/products/body-solid-slc400g-proclub-prone-leg-curl-new |
| value | Body-Solid S2SLC-1 Series II Seated Leg Curl | $2,395 | $2,395 | https://fitnesssuperstore.com/products/body-solid-s2slc-1-series-ii-seated-leg-curl-new |
| value | French Fitness FFB Black Seated Leg Curl | $3,299 | $3,299 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-seated-leg-curl-new |
| commercial | Life Fitness Axiom Series Leg Curl | $5,097 | $5,097 | https://shop.lifefitness.com/products/axiom-series-leg-curl |
| commercial | Hoist Club Line CL-3402 Leg Curl | $4,890 | $4,890 | https://www.hoistfitness.com/products/cl-3402-leg-curl |
| commercial | Hoist ROC-IT RS-2402 Leg Curl | $5,805 | $5,805 | https://www.hoistfitness.com/products/rs-2402-leg-curl |
| commercial | Nautilus Instinct Leg Curl 9NL-S1011-60ARS | $3,819 | $3,819 | https://fitnesssuperstore.com/products/nautilus-instinct-leg-curl-9nl-s1011-60ars-new |
| commercial | Nautilus Impact Seated Leg Curl 9NA-S1313-60AGS | $6,869 | $6,869 | https://fitnesssuperstore.com/products/nautilus-impact-seated-leg-curl-9na-s1313-60ags-new |
| commercial | Prime HYBRID / Seated Leg Curl | $6,000 | $6,000 | https://www.primefitnessusa.com/products/hybrid-seated-leg-curl |
| commercial | Matrix Versa Seated Leg Curl | $4,798 | $3,308.97 | https://akfit.com/products/matrix-versa-seated-leg-curl-w-160lbs |
| commercial | Matrix Aura Seated Leg Curl | $6,938.10 | $4,784.90 | https://akfit.com/products/matrix-aura-seated-leg-curl |
| premium | Hammer Strength Select Seated Leg Curl | $6,728 | $6,728 | https://shop.lifefitness.com/products/hammer-strength-select-seated-leg-curl |
| premium | Life Fitness Insignia Series Seated Leg Curl | $8,485 | $8,485 | https://shop.lifefitness.com/products/insignia-series-seated-leg-curl |
| premium | Nautilus Inspiration Leg Curl 9-IPLC5-60BZ | $7,249 | $7,249 | https://fitnesssuperstore.com/products/nautilus-inspiration-leg-curl-9-iplc5-60bz-new |
| premium | Prime EVOLUTION / Seated Leg Curl | $5,850 | $5,850 | https://www.primefitnessusa.com/products/evolution-seated-leg-curl |
| premium | Matrix Ultra Seated Leg Curl | $10,985.33 | $7,576.09 | https://akfit.com/products/matrix-seated-leg-curl |

### leg_ext_curl_combo

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Body-Solid S2LEC Series II Leg Extension & Leg Curl | $3,160 | $3,160 | https://fitnesssuperstore.com/products/body-solid-s2lec-series-ii-leg-extension-leg-curl-new |
| value | Titan Fitness Selectorized Leg Extension and Curl Machine | $2,609.97 | $2,609.97 | https://titan.fitness/products/selectorized-leg-extension-and-curl-machine |
| value | Body-Solid DLEC-SF Pro Dual Leg Extension & Curl Machine | $3,740 | $3,740 | https://fitnesssuperstore.com/products/body-solid-dlec-sf-pro-dual-leg-extension-curl-machine-new |
| commercial | Life Fitness Axiom Series Leg Curl / Extension | $5,246 | $5,246 | https://shop.lifefitness.com/products/axiom-series-leg-curl-extension |
| commercial | Life Fitness Axiom Series Seated Leg Curl / Extension | $5,776 | $5,776 | https://shop.lifefitness.com/products/axiom-series-seated-leg-curl-extension |
| commercial | Hoist HD-3400 Leg Extension/Leg Curl | $4,400 | $4,400 | https://www.hoistfitness.com/products/hd-3400-leg-extension-leg-curl |
| commercial | Nautilus Instinct Dual Leg Extension / Leg Curl 9NL-D1014-60ARS | $3,619 | $3,619 | https://fitnesssuperstore.com/products/nautilus-instinct-dual-leg-extension-leg-curl-9nl-d1014-60ars-new |
| commercial | Prime HYBRID / Leg Extension/ Leg Curl Combo | $6,500 | $6,500 | https://www.primefitnessusa.com/products/hybrid-leg-extension-leg-curl-combo |
| commercial | Matrix Versa Leg Extension / Leg Curl | $5,298 | $3,653.79 | https://akfit.com/products/matrix-versa-combo-leg-ext-curl-w-160lbs |

### hip_abductor_adductor

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Body-Solid S2IOT-1 Series II Inner and Outer Thigh | $2,545 | $2,545 | https://fitnesssuperstore.com/products/body-solid-s2iot-1-series-ii-inner-and-outer-thigh-new |
| value | Titan Fitness Selectorized Hip Abductor Adductor Machine | $2,149.97 | $2,149.97 | https://titan.fitness/products/selectorized-abductor-adductor-machine |
| value | Body-Solid DIOT-SF Pro Dual Inner & Outer Thigh Machine | $3,800 | $3,800 | https://fitnesssuperstore.com/products/body-solid-diot-sf-pro-dual-inner-outer-thigh-machine-new |
| commercial | Life Fitness Axiom Series Hip Abductor / Adductor | $5,246 | $5,246 | https://shop.lifefitness.com/products/axiom-series-hip-abductor-adductor |
| commercial | Hoist HD-3800 Inner/Outer Thigh | $4,400 | $4,400 | https://www.hoistfitness.com/products/hd-3800-inner-outer-thigh |
| commercial | Nautilus Instinct Dual Inner / Outer Thigh 9NL-D1015-60ARS | $3,619 | $3,619 | https://fitnesssuperstore.com/products/nautilus-instinct-dual-inner-outer-thigh-9nl-d1015-60ars-new |
| commercial | Prime HYBRID / Inner/Outer Thigh | $6,000 | $6,000 | https://www.primefitnessusa.com/products/hybrid-inner-outer-thigh |
| commercial | Matrix Versa Hip Abductor / Adductor | $4,698 | $3,240 | https://akfit.com/products/matrix-versa-hip-adductor-abductor-w-160lbs |
| premium | Life Fitness Insignia Series Hip Abduction / Adduction | $9,091 | $9,091 | https://shop.lifefitness.com/products/insignia-series-hip-abductor-adductor-outlet |
| premium | Nautilus Inspiration Abduction / Adduction 9-IPAA5-60BZ | $6,899 | $6,899 | https://fitnesssuperstore.com/products/nautilus-inspiration-abduction-adduction-9-ipaa5-60bz-new |
| premium | Hammer Strength Select Hip Abduction | $6,020 | $6,020 | https://shop.lifefitness.com/products/hammer-strength-select-hip-abduction |

### glute_kickback

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | French Fitness Newport Selectorized Glute Machine | $3,299 | $3,299 | https://fitnesssuperstore.com/products/french-fitness-newport-selectorized-glute-machine-new |
| value | French Fitness FFB Black Glute Machine | $2,999 | $2,999 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-glute-machine-new |
| value | French Fitness Marin Rear Kick Back Glute | $1,999 | $1,999 | https://fitnesssuperstore.com/products/french-fitness-marin-rear-kick-back-glute-new |
| value | Titan Fitness Plate-Loaded Kickback Glute Machine | $659.97 | $659.97 | https://titan.fitness/products/plate-loaded-kickback-glute-machine |
| commercial | Nautilus Instinct Glute Press 9NL-S1012-60ARS | $3,799 | $3,799 | https://fitnesssuperstore.com/products/nautilus-instinct-glute-press-9nl-s1012-60ars-new |
| commercial | Hoist ROC-IT Glute Master (selectorized) | $5,805 | $5,805 | https://www.hoistfitness.com/products/glute-master |
| commercial | Prime HYBRID / Multi-Hip | $5,900 | $5,900 | https://www.primefitnessusa.com/products/hybrid-multi-hip |
| commercial | Matrix Versa Glute | $5,568.44 | $3,840.30 | https://akfit.com/products/matrix-versa-glute-w-150lbs |
| premium | Hammer Strength Select Hip and Glute | $7,388 | $7,388 | https://shop.lifefitness.com/products/hammer-strength-select-hip-and-glute |
| premium | Life Fitness Insignia Series Glute | $7,733 | $7,733 | https://shop.lifefitness.com/products/insignia-series-glute |
| premium | Nautilus Inspiration Glute Press 9-IPGM5-60AAS | $6,959 | $6,959 | https://fitnesssuperstore.com/products/nautilus-inspiration-glute-press-9-ipgm5-60aas-new |
| premium | Matrix Ultra Glute | $10,036.67 | $6,921.84 | https://akfit.com/products/matrix-glute |

### calf_raise

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Body-Solid GSCR349B Commercial Seated Calf Raise | $750 | $750 | https://fitnesssuperstore.com/products/body-solid-gscr349b-commercial-seated-calf-raise-new |
| value | French Fitness FFB Black Seated Calf Raise Plate Loaded | $1,199 | $1,199 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-seated-calf-raise-plate-loaded-new |
| value | French Fitness Marin Super Horizontal Calf Plate Loaded | $1,899 | $1,899 | https://fitnesssuperstore.com/products/french-fitness-marin-super-horizontal-calf-plate-loaded-new |
| commercial | Hoist ROC-IT RPL-5363 Seated Calf Raise | $1,615 | $1,615 | https://www.hoistfitness.com/products/rpl-5363-seated-calf-raise |
| commercial | Hoist ROC-IT RPL-5405 Standing Calf Raise | $3,815 | $3,815 | https://www.hoistfitness.com/products/rpl-5405-standing-calf-raise |
| commercial | Nautilus Plate Loaded 9NP-L1110 Tilt Seat Calf | $1,519 | $1,519 | https://fitnesssuperstore.com/products/nautilus-plate-loaded-9np-l1110-tilt-seat-calf-new |
| commercial | Nautilus Impact Standing Calf 9NA-S1309-60AGS | $5,599 | $5,599 | https://fitnesssuperstore.com/products/nautilus-impact-standing-calf-9na-s1309-60ags-new |
| commercial | Prime HYBRID / Seated Calf Press | $5,900 | $5,900 | https://www.primefitnessusa.com/products/hybrid-seated-calf-press |
| premium | Hammer Strength Plate Loaded Seated Calf Raise | $2,352 | $2,352 | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-seated-calf-raise |
| premium | Hammer Strength Select Standing Calf | $6,298 | $6,298 | https://shop.lifefitness.com/products/hammer-strength-select-standing-calf |
| premium | Life Fitness Insignia Series Calf Extension | $7,635 | $7,635 | https://shop.lifefitness.com/products/insignia-series-calf-extension |
| premium | Sorinex Seated Calf Machine | $999 | $999 | https://www.sorinex.com/products/seated-calf-machine |

### leg_press_selectorized

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Body-Solid SLP500G ProClub Line Leg Press | $2,990 | $2,990 | https://fitnesssuperstore.com/products/body-solid-slp500g-proclub-line-leg-press-new |
| value | Body-Solid S2LPC-2 Series II Leg Press and Calf Raise | $2,895 | $2,895 | https://fitnesssuperstore.com/products/body-solid-s2lpc-2-series-ii-leg-press-and-calf-raise-new |
| value | French Fitness FFB Black Seated Leg Press | $2,799 | $2,799 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-seated-leg-press-new |
| commercial | Life Fitness Axiom Series Leg Press | $6,399 | $6,399 | https://shop.lifefitness.com/products/axiom-series-leg-press |
| commercial | Hoist HD-3403 Leg Press/Calf Raise | $5,990 | $5,990 | https://www.hoistfitness.com/products/hd-3403-leg-press-calf-raise |
| commercial | Hoist Club Line CL-3403 Leg Press | $6,720 | $6,720 | https://www.hoistfitness.com/products/cl-3403-cl-3403-hs-leg-press |
| commercial | Hoist ROC-IT RS-2403 Leg Press | $8,310 | $8,310 | https://www.hoistfitness.com/products/rs-2403-leg-press |
| commercial | Nautilus Instinct Dual Leg Press / Calf Raise 9NL-D1013-60ARS | $4,839 | $4,839 | https://fitnesssuperstore.com/products/nautilus-instinct-dual-leg-press-calf-raise-9nl-d1013-60ars-new |
| commercial | Nautilus Impact Seated Leg Press 9NA-S1305-60AGS | $8,149 | $8,149 | https://fitnesssuperstore.com/products/nautilus-impact-seated-leg-press-9na-s1305-60ags-new |
| commercial | Prime HYBRID / Leg Press | $8,000 | $8,000 | https://www.primefitnessusa.com/products/hybrid-leg-press |
| commercial | Matrix Aura Leg Press | $7,698 | $5,308.97 | https://akfit.com/products/matrix-aura-leg-press |
| premium | Hammer Strength Select Seated Leg Press | $9,449 | $9,449 | https://shop.lifefitness.com/products/hammer-strength-select-seated-leg-press |
| premium | Life Fitness Insignia Series Arc Leg Press | $11,892 | $11,892 | https://shop.lifefitness.com/products/insignia-series-leg-press |
| premium | Nautilus Inspiration Leg Press 9-IPLP5-60BZ | $9,279 | $9,279 | https://fitnesssuperstore.com/products/nautilus-inspiration-leg-press-9-iplp5-60bz-new |
| premium | Prime EVOLUTION / Leg Press | $8,500 | $8,500 | https://www.primefitnessusa.com/products/evolution-leg-press |
| premium | Matrix Ultra Leg Press | $15,498.46 | $10,688.59 | https://akfit.com/products/leg-press |

### chest_press

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Body-Solid S2CP-2 Series II Chest Press | $2,780 | $2,780 | https://fitnesssuperstore.com/products/body-solid-s2cp-2-series-ii-chest-press-new |
| value | French Fitness FFB Black Dual Stack Chest Press | $2,999 | $2,999 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-dual-stack-chest-press-new |
| value | French Fitness Tahoe Chest Press | $2,799 | $2,799 | https://fitnesssuperstore.com/products/french-fitness-tahoe-chest-press-new |
| commercial | Life Fitness Axiom Series Chest Press | $5,246 | $5,246 | https://shop.lifefitness.com/products/axiom-series-chest-press |
| commercial | Hoist Club Line CL-3301 Chest Press | $4,890 | $4,890 | https://www.hoistfitness.com/products/cl-3301-chest-press |
| commercial | Hoist ROC-IT RS-2301 Chest Press | $5,805 | $5,805 | https://www.hoistfitness.com/products/rs-2301-chest-press |
| commercial | Nautilus Instinct Chest Press 9NL-S2100-60ARS | $3,799 | $3,799 | https://fitnesssuperstore.com/products/nautilus-instinct-chest-press-9nl-s2100-60ars-new |
| commercial | Nautilus Impact Chest Press 9NA-S4301-60AGS | $5,899 | $5,899 | https://fitnesssuperstore.com/products/nautilus-impact-chest-press-9na-s4301-60ags-new |
| commercial | Prime HYBRID / Chest Press | $6,250 | $6,250 | https://www.primefitnessusa.com/products/hybrid-chest-press |
| commercial | Matrix Versa Converging Chest Press | $4,298 | $2,964.14 | https://akfit.com/products/matrix-versa-converging-chest-press-w-160lbs |
| commercial | Matrix Aura Chest Press | $6,612.53 | $4,560.37 | https://akfit.com/products/matrix-chest-press |
| premium | Hammer Strength Select Chest Press | $5,972 | $5,972 | https://shop.lifefitness.com/products/hammer-strength-select-chest-press |
| premium | Life Fitness Insignia Series Chest Press | $8,424 | $8,424 | https://shop.lifefitness.com/products/insignia-series-chest-press |
| premium | Nautilus Inspiration Chest Press 9-IPVP5-60BZ | $7,049 | $7,049 | https://fitnesssuperstore.com/products/nautilus-inspiration-chest-press-9-ipvp5-60bz-new |
| premium | Prime EVOLUTION / Chest Press | $6,600 | $6,600 | https://www.primefitnessusa.com/products/evolution-chest-press |
| premium | Matrix Ultra Converging Chest Press | $11,282.83 | $7,781.26 | https://akfit.com/products/matrix-converging-chest-press |

### pec_fly_rear_delt

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Body-Solid S2PEC-1 Series II Pec Fly and Rear Delt | $2,780 | $2,780 | https://fitnesssuperstore.com/products/body-solid-s2pec-1-series-ii-pec-fly-and-rear-delt-new |
| value | French Fitness Tahoe Pec Fly / Rear Delt | $2,799 | $2,799 | https://fitnesssuperstore.com/products/french-fitness-tahoe-pec-fly-rear-delt-new |
| value | Titan Fitness Selectorized Pec Fly and Reverse Delt Machine | $2,199.97 | $2,199.97 | https://titan.fitness/products/selectorized-pec-fly-and-reverse-delt-machine |
| commercial | Life Fitness Axiom Series Pectoral Fly / Rear Deltoid | $5,246 | $5,246 | https://shop.lifefitness.com/products/axiom-series-pectoral-fly-rear-deltoid |
| commercial | Hoist HD-3900 Pec Fly/Rear Delt | $4,400 | $4,400 | https://www.hoistfitness.com/products/hd-3900-pec-fly-rear-delt |
| commercial | Hoist Club Line CL-3309 Pec Fly/Rear Delt | $5,380 | $5,380 | https://www.hoistfitness.com/products/cl-3309-pec-fly-rear-delt |
| commercial | Nautilus Instinct Dual Pectoral Fly / Rear Deltoid 9NL-D2110-60ARS | $3,619 | $3,619 | https://fitnesssuperstore.com/products/nautilus-instinct-dual-pectoral-fly-rear-deltoid-9nl-d2110-60ars-new |
| commercial | Prime HYBRID / Pec/Rear Delt | $5,900 | $5,900 | https://www.primefitnessusa.com/products/hybrid-pec-rear-delt |
| commercial | Matrix Versa Pec Fly/ Rear Delt | $4,098 | $2,826.21 | https://akfit.com/products/matrix-versa-pectoral-fly-rear-delt-w-150lb |
| commercial | Matrix Aura Rear Delt / Pec Fly | $7,583.64 | $5,230.10 | https://akfit.com/products/matrix-rear-delt-fly |
| premium | Hammer Strength Select Pectoral Fly / Rear Deltoid | $5,972 | $5,972 | https://shop.lifefitness.com/products/hammer-strength-select-pectoral-fly-rear-deltoid |
| premium | Life Fitness Insignia Series Pectoral Fly/Rear Deltoid | $7,866 | $7,866 | https://shop.lifefitness.com/products/insignia-series-pectoral-fly-rear-deltoid |
| premium | Nautilus Inspiration Pec Fly/Rear Deltoid 9-IPPF5-60BZ | $7,099 | $7,099 | https://fitnesssuperstore.com/products/nautilus-inspiration-pec-fly-rear-deltoid-9-ippf5-60bz-new |
| premium | Matrix Ultra Rear Delt / Pec Fly | $10,305 | $7,106.90 | https://akfit.com/products/matrix-rear-delt-pec-fly |

### shoulder_press

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Body-Solid S2SP-2 Series II Shoulder Press | $2,095 | $2,095 | https://fitnesssuperstore.com/products/body-solid-s2sp-2-series-ii-shoulder-press-new |
| value | French Fitness Tahoe Shoulder Press | $2,799 | $2,799 | https://fitnesssuperstore.com/products/french-fitness-tahoe-shoulder-press-new |
| value | French Fitness FFB Black Dual Stack Shoulder Press | $2,999 | $2,999 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-dual-stack-shoulder-press-new |
| commercial | Life Fitness Axiom Series Shoulder Press | $5,246 | $5,246 | https://shop.lifefitness.com/products/axiom-series-shoulder-press |
| commercial | Hoist Club Line CL-3501 Shoulder Press | $4,890 | $4,890 | https://www.hoistfitness.com/products/cl-3501-shoulder-press |
| commercial | Hoist ROC-IT Shoulder Press | $5,805 | $5,805 | https://www.hoistfitness.com/products/shoulder-press |
| commercial | Nautilus Instinct Shoulder Press 9NL-S4100-60ARS | $3,799 | $3,799 | https://fitnesssuperstore.com/products/nautilus-instinct-shoulder-press-9nl-s4100-60ars-new |
| commercial | Nautilus Impact Shoulder Press 9NA-S4307-60AGS | $5,599 | $5,599 | https://fitnesssuperstore.com/products/nautilus-impact-shoulder-press-9na-s4307-60ags-new |
| commercial | Prime HYBRID / Shoulder Press | $6,150 | $6,150 | https://www.primefitnessusa.com/products/hybrid-shoulder-press |
| commercial | Matrix Versa Converging Shoulder Press | $4,498 | $3,102.07 | https://akfit.com/products/matrix-versa-converging-shoulder-press-w-160lbs |
| commercial | Matrix Aura Shoulder Press | $6,343.09 | $4,374.54 | https://akfit.com/products/matrix-shoulder-press |
| premium | Hammer Strength Select Shoulder Press | $5,818 | $5,818 | https://shop.lifefitness.com/products/hammer-strength-select-shoulder-press |
| premium | Life Fitness Insignia Series Shoulder Press | $7,843 | $7,843 | https://shop.lifefitness.com/products/insignia-series-shoulder-press |
| premium | Nautilus Inspiration Shoulder Press Machine 9-IPSP5-60BZ | $7,099 | $7,099 | https://fitnesssuperstore.com/products/nautilus-inspiration-shoulder-press-machine-9-ipsp5-60bz-new |
| premium | Prime EVOLUTION / Shoulder Press | $6,050 | $6,050 | https://www.primefitnessusa.com/products/evolution-shoulder-press |
| premium | Matrix Ultra Converging Shoulder Press | $11,041.46 | $7,614.80 | https://akfit.com/products/matrix-converging-shoulder-press |

### lat_pulldown

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | French Fitness Tahoe Cable Lat Pulldown | $2,799 | $2,799 | https://fitnesssuperstore.com/products/french-fitness-tahoe-cable-lat-pulldown-new |
| value | French Fitness FFB Black Dual Stack Front Lat Pulldown | $2,999 | $2,999 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-dual-stack-front-lat-pulldown-new |
| commercial | Life Fitness Axiom Series Lat Pulldown | $5,246 | $5,246 | https://shop.lifefitness.com/products/axiom-series-pulldown |
| commercial | Hoist Club Line CL-3201 Lat Pulldown | $4,890 | $4,890 | https://www.hoistfitness.com/products/cl-3201-lat-pulldown |
| commercial | Hoist ROC-IT RS-2201 Lat Pulldown | $5,805 | $5,805 | https://www.hoistfitness.com/products/rs-2201-lat-pulldown |
| commercial | Nautilus Instinct Lat Pull Down 9NL-S3310-60ARS | $3,799 | $3,799 | https://fitnesssuperstore.com/products/nautilus-instinct-lat-pull-down-9nl-s3310-60ars-new |
| commercial | Nautilus Impact Lat Pull Down 9NA-S3305-60AGS | $5,599 | $5,599 | https://fitnesssuperstore.com/products/nautilus-impact-lat-pull-down-9na-s3305-60ags-new |
| commercial | Prime HYBRID / Lat Pulldown | $6,850 | $6,850 | https://www.primefitnessusa.com/products/hybrid-lat-pulldown |
| commercial | Matrix Versa Diverging Lat Pulldown | $4,298 | $2,964.14 | https://akfit.com/products/matrix-versa-diverging-lat-pulldown-w-160lbs |
| commercial | Matrix Aura Lat Pulldown | $5,343.91 | $3,685.46 | https://akfit.com/products/matrix-aura-lat-pulldown |
| premium | Hammer Strength Select Lat Pulldown | $4,929 | $4,929 | https://shop.lifefitness.com/products/hammer-strength-select-lat-pulldown |
| premium | Life Fitness Insignia Series Pulldown | $8,000 | $8,000 | https://shop.lifefitness.com/products/insignia-series-pulldown |
| premium | Nautilus Inspiration Lat Pull Down 9-IPPD5-60BZ | $7,099 | $7,099 | https://fitnesssuperstore.com/products/nautilus-inspiration-lat-pull-down-9-ippd5-60bz-new |
| premium | Prime EVOLUTION / Lat Pulldown | $7,200 | $7,200 | https://www.primefitnessusa.com/products/evolution-lat-pulldown-diverging |
| premium | Matrix Ultra Diverging Lat Pulldown | $11,378.26 | $7,847.08 | https://akfit.com/products/matrix-diverging-lat-pulldown |

### seated_row

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | French Fitness Tahoe Seated Row | $2,799 | $2,799 | https://fitnesssuperstore.com/products/french-fitness-tahoe-seated-row-new |
| value | French Fitness FFB Black Dual Stack Low Row | $2,999 | $2,999 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-dual-stack-low-row-new |
| commercial | Life Fitness Axiom Series Seated Row | $5,246 | $5,246 | https://shop.lifefitness.com/products/axiom-series-seated-row-1 |
| commercial | Hoist Club Line CL-3203 Mid Row | $4,890 | $4,890 | https://www.hoistfitness.com/products/cl-3203-mid-row |
| commercial | Hoist ROC-IT Seated Mid Row | $5,805 | $5,805 | https://www.hoistfitness.com/products/seated-mid-row |
| commercial | Nautilus Instinct Vertical Row 9NL-S3320-60ARS | $3,799 | $3,799 | https://fitnesssuperstore.com/products/nautilus-instinct-vertical-row-9nl-s3320-60ars-new |
| commercial | Nautilus Impact Low Row 9NA-S3306-60AGS | $5,599 | $5,599 | https://fitnesssuperstore.com/products/nautilus-impact-low-row-9na-s3306-60ags-new |
| commercial | Prime HYBRID / Seated Row | $5,950 | $5,950 | https://www.primefitnessusa.com/products/hybrid-seated-row |
| commercial | Matrix Versa Diverging Seated Row | $3,798 | $2,619.31 | https://akfit.com/products/matrix-versa-diverging-seated-row-w-160lbs |
| commercial | Matrix Aura Seated Row | $6,157.84 | $4,246.79 | https://akfit.com/products/matrix-aura-seated-row-station |
| premium | Hammer Strength Select Seated Row | $5,972 | $5,972 | https://shop.lifefitness.com/products/hammer-strength-select-seated-row |
| premium | Life Fitness Insignia Series Row | $7,733 | $7,733 | https://shop.lifefitness.com/products/insignia-series-row |
| premium | Nautilus Inspiration Vertical Row 9-IPVR5-60BZ | $7,049 | $7,049 | https://fitnesssuperstore.com/products/nautilus-inspiration-vertical-row-9-ipvr5-60bz-new |
| premium | Prime EVOLUTION / Seated Row | $6,950 | $6,950 | https://www.primefitnessusa.com/products/evolution-seated-row |
| premium | Matrix Ultra Diverging Seated Row | $11,176.18 | $7,707.71 | https://akfit.com/products/matrix-diverging-seated-row |

### lat_pulldown_row_combo

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | REP Fitness Selectorized Lat Pulldown & Low Row (4000/5000 Series) | $1,349.99 | $1,349.99 | https://repfitness.com/products/4000-5000-series-lat-pulldown |
| value | Titan Fitness Lat Tower Pulldown & Cable Row Machine / 10 - 300 LB Selector | $1,649.97 | $1,649.97 | https://titan.fitness/products/lat-tower-10-300-lb-selector |
| value | Body-Solid SLM300G ProClub Line Lat Mid Row | $2,775 | $2,775 | https://fitnesssuperstore.com/products/body-solid-slm300g-proclub-line-lat-mid-row-new |
| value | French Fitness Tahoe Lat Pulldown / Low Row | $2,799 | $2,799 | https://fitnesssuperstore.com/products/french-fitness-tahoe-lat-pulldown-low-row-new |
| value | Rogue Monster Lat Pulldown/Low Row (Stand Alone) | $3,250 | $3,250 | https://www.roguefitness.com/lat-pulldown-low-row-stand-alone |
| commercial | Life Fitness Axiom Series Pulldown / Row | $5,246 | $5,246 | https://shop.lifefitness.com/products/axiom-series-pulldown-row |
| commercial | Hoist HD-3200 Lat Pulldown/Mid Row | $4,400 | $4,400 | https://www.hoistfitness.com/products/hd-3200-lat-pulldown-mid-row |
| commercial | Nautilus Instinct Dual Lat Pull Down / Vertical Row 9NL-D3340-60ARS | $3,619 | $3,619 | https://fitnesssuperstore.com/products/nautilus-instinct-dual-lat-pull-down-vertical-row-9nl-d3340-60ars-new |
| commercial | Matrix Versa Lat Pulldown / Seated Row | $4,898 | $3,377.93 | https://akfit.com/products/matrix-versa-combo-lat-pulldown-seated-row-w-160lb |
| commercial | Rogue LP-2 Lat Pulldown / Low Row | $3,650 | $3,650 | https://www.roguefitness.com/rogue-lp-2-lat-pulldown-low-row |
| premium | Hammer Strength Dual Pulldown/Row | $5,889 | $5,889 | https://shop.lifefitness.com/products/hammer-strength-hd-elite-dual-pulldown-row-1 |

### assisted_pullup_dip

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Body-Solid Body Solid S2ACD Series II Assisted Chin and Dip Machine | $3,820 | $3,820 | https://fitnesssuperstore.com/products/body-solid-s2acd-series-ii-assisted-chin-and-dip-machine-new |
| value | French Fitness Tahoe Assisted Chin Dip | $2,799 | $2,799 | https://fitnesssuperstore.com/products/french-fitness-tahoe-assisted-chin-dip-new |
| value | Body-Solid FCD-STK Pro-Select Weight Assisted Chin-Dip Machine | $2,130 | $2,130 | https://fitnesssuperstore.com/products/body-solid-fcd-stk-pro-select-weight-assisted-chin-dip-machine-new |
| commercial | Hoist HD-3700 Chin/Dip Assist | $5,990 | $5,990 | https://www.hoistfitness.com/products/hd-3700-chin-dip-assist |
| commercial | Nautilus Impact Chin Dip Assist 9NA-S6334-60AGS | $6,229 | $6,229 | https://fitnesssuperstore.com/products/nautilus-impact-chin-dip-assist-9na-s6334-60ags-new |
| commercial | Prime CHIN / DIP ASSIST | $4,800 | $4,800 | https://www.primefitnessusa.com/products/chin-dip-assist |
| commercial | Matrix Aura Dip/Chin Assist | $5,298 | $3,653.79 | https://akfit.com/products/matrix-aura-dip-chin-assist-w-200lbs |
| commercial | Matrix Versa Chin / Dip Assist | $7,336.65 | $5,059.76 | https://akfit.com/products/matrix-versa-combo-chin-dip-assist-w-205lbs |
| premium | Hammer Strength Select Assist Dip Chin | $6,781 | $6,781 | https://shop.lifefitness.com/products/hammer-strength-select-assist-dip-chin |
| premium | Life Fitness Insignia Series Assist Dip Chin | $8,424 | $8,424 | https://shop.lifefitness.com/products/insignia-series-assist-dip-chin |

### biceps_curl_machine

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Body-Solid S2AC Series II Arm Curl Machine | $2,315 | $2,315 | https://fitnesssuperstore.com/products/body-solid-s2ac-series-ii-arm-curl-machine-new |
| value | French Fitness Tahoe Bicep Arm Curl | $2,799 | $2,799 | https://fitnesssuperstore.com/products/french-fitness-tahoe-bicep-arm-curl-new |
| value | Titan Fitness Selectorized Bicep and Tricep Machine | $2,099.97 | $2,099.97 | https://titan.fitness/products/selectorized-bicep-and-tricep-machine |
| commercial | Life Fitness Axiom Series Biceps Curl | $4,631 | $4,631 | https://shop.lifefitness.com/products/axiom-series-biceps-curl |
| commercial | Hoist Club Line CL-3102 Biceps Curl | $4,890 | $4,890 | https://www.hoistfitness.com/products/cl-3102-biceps-curl |
| commercial | Hoist ROC-IT Biceps Curl | $5,805 | $5,805 | https://www.hoistfitness.com/products/biceps-curl |
| commercial | Nautilus Impact Biceps Curl 9NA-S5301-60AGS | $5,599 | $5,599 | https://fitnesssuperstore.com/products/nautilus-impact-biceps-curl-9na-s5301-60ags-new |
| commercial | Prime HYBRID / Arm Curl | $5,150 | $5,150 | https://www.primefitnessusa.com/products/hybrid-arm-curl |
| commercial | Matrix Versa Bicep Curl | $4,098 | $2,826.21 | https://akfit.com/products/matrix-versa-biceps-curl-w-150lbs |
| commercial | Matrix Aura Arm Curl | $5,877.18 | $4,053.23 | https://akfit.com/products/matrix-aura-arm-curl |
| premium | Hammer Strength Select Biceps Curl | $5,509 | $5,509 | https://shop.lifefitness.com/products/hammer-strength-select-biceps-curl |
| premium | Life Fitness Insignia Series Biceps Curl | $7,733 | $7,733 | https://shop.lifefitness.com/products/insignia-series-biceps-curl |
| premium | Nautilus Inspiration Biceps Curl 9-IPBC5-60BZ | $6,789 | $6,789 | https://fitnesssuperstore.com/products/nautilus-inspiration-biceps-curl-9-ipbc5-60bz-new |
| premium | Prime EVOLUTION / Arm Curl | $5,350 | $5,350 | https://www.primefitnessusa.com/products/evolution-arm-curl |
| premium | Matrix Ultra Independent Biceps Curl | $9,323.77 | $6,430.19 | https://akfit.com/products/independent-biceps-curl |

### triceps_machine

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | French Fitness Tahoe Tricep Arm Extension | $2,799 | $2,799 | https://fitnesssuperstore.com/products/french-fitness-tahoe-tricep-arm-extension-new |
| value | French Fitness FFB Black Triceps Press Seated Dip | $2,799 | $2,799 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-triceps-press-seated-dip-new |
| value | French Fitness Newport Selectorized Triceps Press | $3,299 | $3,299 | https://fitnesssuperstore.com/products/french-fitness-newport-selectorized-triceps-press-new |
| commercial | Life Fitness Axiom Series Triceps Extension | $4,631 | $4,631 | https://shop.lifefitness.com/products/axiom-series-triceps-extension |
| commercial | Hoist Club Line CL-3103 Triceps Extension | $4,890 | $4,890 | https://www.hoistfitness.com/products/cl-3103-triceps-extension |
| commercial | Hoist ROC-IT Triceps Extension | $5,805 | $5,805 | https://www.hoistfitness.com/products/rs-1103-triceps-extension |
| commercial | Nautilus Instinct Triceps Extension 9NL-S5110-60ARS | $3,499 | $3,499 | https://fitnesssuperstore.com/products/nautilus-instinct-triceps-extension-9nl-s5110-60ars-new |
| commercial | Nautilus Impact Triceps Extension 9NA-S5302-60AGS | $5,599 | $5,599 | https://fitnesssuperstore.com/products/nautilus-impact-triceps-extension-9na-s5302-60ags-new |
| commercial | Prime HYBRID / Tricep Extension | $5,600 | $5,600 | https://www.primefitnessusa.com/products/hybrid-tricep-extension |
| commercial | Matrix Versa Triceps Press | $4,298 | $2,964.14 | https://akfit.com/products/matrix-versa-triceps-press-w-160lbs |
| commercial | Matrix Aura Tricep Extension | $5,697.55 | $3,929.34 | https://akfit.com/products/matrix-aura-triceps-extension |
| premium | Hammer Strength Select Triceps Extension | $5,509 | $5,509 | https://shop.lifefitness.com/products/hammer-strength-select-triceps-extension |
| premium | Life Fitness Insignia Series Triceps Extension | $6,957 | $6,957 | https://shop.lifefitness.com/products/insignia-series-triceps-extension |
| premium | Nautilus Inspiration Triceps Extension 9-IPTE5-60BZ | $7,049 | $7,049 | https://fitnesssuperstore.com/products/nautilus-inspiration-triceps-extension-9-ipte5-60bz-new |
| premium | Prime EVOLUTION / Tricep Extension | $5,750 | $5,750 | https://www.primefitnessusa.com/products/evolution-tricep-extension |
| premium | Matrix Ultra Triceps Press | $10,603.62 | $7,312.84 | https://akfit.com/products/matrix-seated-triceps-press |

### ab_crunch_machine

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | French Fitness Tahoe Selectorized Horizontal Ab Crunch | $2,799 | $2,799 | https://fitnesssuperstore.com/products/french-fitness-tahoe-selectorized-horizontal-ab-crunch-new |
| value | French Fitness FFB Black Single Stack Abdominal Crunch | $2,999 | $2,999 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-single-stack-abdominal-crunch-new |
| value | Titan Fitness Selectorized Abdominal & Lower Back Machine | $1,999.97 | $1,999.97 | https://titan.fitness/products/selectorized-abdominal-lower-back-machine |
| commercial | Life Fitness Axiom Series Abdominal | $3,908 | $3,908 | https://shop.lifefitness.com/products/axiom-series-abdominal |
| commercial | Hoist Club Line CL-3601 Abdominals | $4,890 | $4,890 | https://www.hoistfitness.com/products/cl-3601-abdominals |
| commercial | Hoist ROC-IT RS-2601 Abdominals | $5,805 | $5,805 | https://www.hoistfitness.com/products/rs-2601-abdominals |
| commercial | Nautilus Impact Abdominal 9NA-S6301-60AGS | $5,599 | $5,599 | https://fitnesssuperstore.com/products/nautilus-impact-abdominal-9na-s6301-60ags-new |
| commercial | Prime HYBRID / Abdominal Crunch | $5,600 | $5,600 | https://www.primefitnessusa.com/products/hybrid-abdominal-crunch |
| commercial | Matrix Versa Abdominal | $3,598 | $2,481.38 | https://akfit.com/products/matrix-versa-abdominal-w-160lbs |
| commercial | Matrix Aura Abdominal Crunch | $6,348.70 | $4,378.41 | https://akfit.com/products/matrix-abdominal-crunch |
| premium | Hammer Strength Select Abdominal Crunch | $6,020 | $6,020 | https://shop.lifefitness.com/products/hammer-strength-select-abdominal-crunch |
| premium | Life Fitness Insignia Series Abdominal | $7,733 | $7,733 | https://shop.lifefitness.com/products/insignia-series-abdominal |
| premium | Nautilus Inspiration Abdominal Crunch 9-IPAC5-60BZ | $7,099 | $7,099 | https://fitnesssuperstore.com/products/nautilus-inspiration-abdominal-crunch-9-ipac5-60bz-new |
| premium | Prime EVOLUTION / Abdominal Crunch | $6,150 | $6,150 | https://www.primefitnessusa.com/products/evolution-abdominal-crunch |
| premium | Matrix Ultra Abdominal Crunch | $9,952.47 | $6,863.77 | https://akfit.com/products/abdominal-crunch |

### back_extension_machine

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | French Fitness Tahoe Selectorized Back Extension | $2,499 | $2,499 | https://fitnesssuperstore.com/products/french-fitness-tahoe-selectorized-back-extension-new |
| commercial | Hoist ROC-IT Low Back | $5,805 | $5,805 | https://www.hoistfitness.com/products/low-back |
| commercial | Nautilus Impact Low Back 9NA-S3302-60AGS | $5,599 | $5,599 | https://fitnesssuperstore.com/products/nautilus-impact-low-back-9na-s3302-60ags-new |
| commercial | Prime HYBRID / Low Back Extension | $5,600 | $5,600 | https://www.primefitnessusa.com/products/hybrid-low-back-extension |
| commercial | Matrix Versa Back Extension | $4,098 | $2,826.21 | https://akfit.com/products/matrix-versa-back-extension-w-160lbs |
| commercial | Matrix Aura Back Extension | $6,736.02 | $4,645.53 | https://akfit.com/products/matrix-aura-back-extension-g3-s52 |
| premium | Hammer Strength Select Back Extension | $6,020 | $6,020 | https://shop.lifefitness.com/products/hammer-strength-select-back-extension |
| premium | Life Fitness Insignia Series Back Extension | $8,000 | $8,000 | https://shop.lifefitness.com/products/insignia-series-back-extension |
| premium | Nautilus Inspiration Back Extension 9-IPBE5-60BZ | $7,049 | $7,049 | https://fitnesssuperstore.com/products/nautilus-inspiration-back-extension-9-ipbe5-60bz-new |
| premium | Prime EVOLUTION / Low Back Extension | $5,800 | $5,800 | https://www.primefitnessusa.com/products/evolution-low-back-extension |
| premium | Matrix Ultra Back Extension | $10,266.82 | $7,080.57 | https://akfit.com/products/back-extension |

### rotary_torso

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | French Fitness Vail Torso Rotation | $2,999 | $2,999 | https://fitnesssuperstore.com/products/french-fitness-vail-torso-rotation-new |
| value | French Fitness Phoenix Rotary Torso Rotation | $2,999 | $2,999 | https://fitnesssuperstore.com/products/french-fitness-phoenix-rotary-torso-rotation-new |
| commercial | Hoist ROC-IT RS-2602 Rotary Torso | $5,805 | $5,805 | https://www.hoistfitness.com/products/rs-2602-rotary-torso |
| commercial | Nautilus Instinct Rotary Torso 9NL-S6300-60ARS | $3,799 | $3,799 | https://fitnesssuperstore.com/products/nautilus-instinct-rotary-torso-9nl-s6300-60ars-new |
| commercial | Prime HYBRID / Rotary Torso | $6,100 | $6,100 | https://www.primefitnessusa.com/products/hybrid-rotary-torso |
| commercial | Matrix Aura Rotary Torso | $6,359.93 | $4,386.16 | https://akfit.com/products/matrix-aura-rotary-torso |
| premium | Life Fitness Insignia Series Torso Rotation | $8,157 | $8,157 | https://shop.lifefitness.com/products/insignia-series-torso-rotation |
| premium | Nautilus Inspiration Rotary Torso 9-IPRT5-60BZS | $6,959 | $6,959 | https://fitnesssuperstore.com/products/nautilus-inspiration-rotary-torso-9-iprt5-60bzs-new |
| premium | Matrix Ultra Rotary Torso | $6,898 | $4,757.24 | https://akfit.com/products/matrix-ultra-rotary-torso-w-200lbs |

### plate_loaded_chest_press

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | French Fitness Marin Iso-Lateral Flat Chest Bench Press Plate Loaded | $2,399 | $2,399 | https://fitnesssuperstore.com/products/french-fitness-marin-iso-lateral-flat-chest-bench-press-plate-loaded-new |
| value | French Fitness Diablo Decline Chest Press Plate Loaded | $2,399 | $2,399 | https://fitnesssuperstore.com/products/french-fitness-diablo-decline-chest-press-plate-loaded-new |
| value | Body-Solid LVBP Leverage Bench Press | $1,095 | $1,095 | https://fitnesssuperstore.com/products/body-solid-lvbp-leverage-bench-press-new |
| value | Titan Fitness Plate-Loaded Chest Press Machine | $799.97 | $799.97 | https://titan.fitness/products/plate-loaded-chest-press-machine |
| commercial | Hoist ROC-IT RPL-5301 Plate-Loaded Chest Press | $3,815 | $3,815 | https://www.hoistfitness.com/products/rpl-5301-chest-press |
| commercial | Prime PLATE LOADED / Chest Press | $4,000 | $4,000 | https://www.primefitnessusa.com/products/plate-loaded-chest-press |
| commercial | Nautilus Leverage Chest Press 9NP-L2002-60BZSS | $4,299 | $4,299 | https://fitnesssuperstore.com/products/nautilus-leverage-chest-press-9np-l2002-60bzss-new |
| premium | Hammer Strength Plate Loaded Iso-Lateral Bench Press | $4,135 | $4,135 | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-iso-lateral-bench-press |
| premium | Hammer Strength Plate Loaded Iso-Lateral Incline Press | $4,135 | $4,135 | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-iso-lateral-incline-press |
| premium | Sorinex Leverage Seated Chest Press | $4,999 | $4,999 | https://www.sorinex.com/products/leverage-chest-press |
| premium | Watson Chest Press | $5,040.79 | $3,476.41 | https://akfit.com/products/watson-chest-press |

### plate_loaded_row

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | French Fitness Marin Iso-Lateral Rowing Low Row Plate Loaded | $2,399 | $2,399 | https://fitnesssuperstore.com/products/french-fitness-marin-iso-lateral-rowing-low-row-plate-loaded-new |
| value | French Fitness Diablo Seated Low Row Plate Loaded | $2,399 | $2,399 | https://fitnesssuperstore.com/products/french-fitness-diablo-seated-low-row-plate-loaded-new |
| value | Body-Solid LVSR Leverage Seated Row | $1,340 | $1,340 | https://fitnesssuperstore.com/products/body-solid-lvsr-leverage-seated-row-new |
| value | Titan Fitness Plate-Loaded Seated Row Machine | $399.97 | $399.97 | https://titan.fitness/products/plate-loaded-seated-row |
| commercial | Hoist ROC-IT RPL-5203 Plate-Loaded Mid Row | $3,815 | $3,815 | https://www.hoistfitness.com/products/rpl-5203-mid-row |
| commercial | Prime PLATE LOADED / Seated Row | $3,700 | $3,700 | https://www.primefitnessusa.com/products/plate-loaded-seated-row |
| commercial | Nautilus Leverage Low Row 9NP-L3004-60BZS | $4,299 | $4,299 | https://fitnesssuperstore.com/products/nautilus-leverage-low-row-9np-l3004-60bzs-new |
| premium | Hammer Strength Plate Loaded Iso-Lateral Row | $4,135 | $4,135 | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-iso-lateral-row |
| premium | Hammer Strength Plate Loaded Iso-Lateral Low Row | $4,135 | $4,135 | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-iso-lateral-low-row |
| premium | Sorinex Leverage Mid Row | $3,799 | $3,799 | https://www.sorinex.com/products/leverage-mid-row |
| premium | Sorinex Leverage Low Row | $3,625 | $3,625 | https://www.sorinex.com/products/lever-low-row |

### plate_loaded_shoulder_press

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | French Fitness Marin Iso-Lateral Shoulder Press Plate Loaded | $2,399 | $2,399 | https://fitnesssuperstore.com/products/french-fitness-marin-iso-lateral-shoulder-press-plate-loaded-new |
| value | Body-Solid LVSP Leverage Shoulder Press | $1,155 | $1,155 | https://fitnesssuperstore.com/products/body-solid-lvsp-leverage-shoulder-press-new |
| value | Titan Fitness Plate-Loaded Deltoid And Shoulder Press Machine | $559.97 | $559.97 | https://titan.fitness/products/plate-loaded-deltoid-shoulder-press-machine |
| commercial | Hoist ROC-IT RPL-5501 Plate-Loaded Shoulder Press | $3,815 | $3,815 | https://www.hoistfitness.com/products/rpl-5501-shoulder-press |
| commercial | Prime PLATE LOADED / Shoulder Press | $3,800 | $3,800 | https://www.primefitnessusa.com/products/plate-loaded-shoulder-press |
| commercial | Nautilus Leverage Shoulder Press 9NP-L4002-60BZS | $4,299 | $4,299 | https://fitnesssuperstore.com/products/nautilus-leverage-shoulder-press-9np-l4002-60bzs-new |
| premium | Hammer Strength Plate Loaded Iso-Lateral Shoulder Press | $4,135 | $4,135 | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-iso-lateral-shoulder-press |

### plate_loaded_high_row

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | French Fitness Marin Iso-Lateral High Row Plate Loaded | $2,399 | $2,399 | https://fitnesssuperstore.com/products/french-fitness-marin-iso-lateral-high-row-plate-loaded-new |
| value | French Fitness Marin Iso-Lateral Front Lat Pulldown Plate Loaded | $2,399 | $2,399 | https://fitnesssuperstore.com/products/french-fitness-marin-iso-lateral-front-lat-pulldown-plate-loaded-new |
| value | Body-Solid LVLA Leverage Lat Pulldown | $1,550 | $1,550 | https://fitnesssuperstore.com/products/body-solid-lvla-leverage-lat-pulldown-new |
| commercial | Hoist ROC-IT RPL-5201 Plate-Loaded Lat Pulldown | $3,815 | $3,815 | https://www.hoistfitness.com/products/rpl-5201-lat-pulldown |
| commercial | Prime PLATE LOADED / Lat Pulldown | $3,800 | $3,800 | https://www.primefitnessusa.com/products/plate-loaded-lat-pulldown |
| commercial | Nautilus Leverage High Row 9NP-L3005-60BZS | $4,299 | $4,299 | https://fitnesssuperstore.com/products/nautilus-leverage-high-row-9np-l3005-60bzs-new |
| commercial | Nautilus Leverage Lat Pull Down 9NP-L3003-60BZS | $4,299 | $4,299 | https://fitnesssuperstore.com/products/nautilus-leverage-lat-pull-down-9np-l3003-60bzs-new |
| premium | Hammer Strength Iso-Lateral High Row | $4,135 | $4,135 | https://shop.lifefitness.com/products/hammer-strength-iso-lateral-high-row |
| premium | Hammer Strength Plate Loaded Iso-Lateral Front Lat Pulldown | $4,135 | $4,135 | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-iso-lateral-front-lat-pulldown |
| premium | Sorinex Leverage High Row | $3,399 | $3,399 | https://www.sorinex.com/products/leverage-high-row |

### t_bar_row

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | French Fitness Chest Supported T-Bar Row TBAR-C40 | $1,099 | $1,099 | https://fitnesssuperstore.com/products/french-fitness-chest-supported-t-bar-row-tbar-c40-new |
| value | French Fitness Chest Supported T-Bar Row TBAR-C90 Black | $1,599 | $1,599 | https://fitnesssuperstore.com/products/french-fitness-chest-supported-t-bar-row-tbar-c90-black-new |
| value | TITAN Series Chest-Supported Row | $1,471.97 | $1,471.97 | https://titan.fitness/products/titan-series-chest-supported-row |
| value | Titan Fitness Chest-Supported T-Bar Row | $399.97 | $399.97 | https://titan.fitness/products/chest-supported-t-bar-row-machine-adjustable |
| value | Rogue T Bar Row | $875 | $875 | https://www.roguefitness.com/rogue-t-bar-row |
| value | Body-Solid STBR500 Pro Clubline T-Bar Row Machine | $640 | $640 | https://fitnesssuperstore.com/products/body-solid-stbr500-pro-clubline-t-bar-row-machine-new |
| commercial | Nautilus Plate Loaded 9NP-L3140 Incline Lever Row | $1,519 | $1,519 | https://fitnesssuperstore.com/products/nautilus-plate-loaded-9np-l3140-incline-row-new |
| commercial | Hoist CF-3661 Incline Leverage Row | $2,220 | $2,220 | https://www.hoistfitness.com/products/cf-3661-incline-leverage-row |
| premium | Hammer Strength Plate Loaded T-Bar Row | $3,032 | $3,032 | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-t-bar-row |
| premium | Sorinex Chest Supported Row Machine | $2,847 | $2,847 | https://www.sorinex.com/products/chest-supported-row-machine |
| premium | Watson Animal Chest Support T-Bar Row | $5,720.66 | $3,945.28 | https://akfit.com/products/watson-animal-chest-support-t-bar-row |

### multi_station_gym

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | French Fitness FFB Black 4 Stack Multi Jungle Gym | $5,699 | $5,699 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-4-stack-multi-jungle-gym-new |
| value | Body-Solid Pro Clubline S1000 Four-Stack Gym | $7,535 | $7,535 | https://fitnesssuperstore.com/products/body-solid-pro-clubline-s1000-four-stack-gym-new |
| value | French Fitness X90 3 Stack Multi-Gym System | $4,999 | $4,999 | https://fitnesssuperstore.com/products/french-fitness-x90-3-stack-multi-gym-system-new |
| commercial | Hoist 4 Stack Multi Gym | $10,755 | $10,755 | https://www.hoistfitness.com/products/h-4400-4-stack-multi-gym |
| commercial | Hoist CMJ-6000-1 4-Station Single Pod | $10,485 | $10,485 | https://www.hoistfitness.com/products/cmj-6000-1-4-station-single-pod |
| commercial | Matrix Varsity 3-Stack Multi-Gym w/3 x 200 lbs Stk | $11,081.99 | $7,642.75 | https://akfit.com/products/matrix-varsity-3-stack-multi-gym-w-3-x-200-lbs-stk-multi-press-lat-pulldown-low-row-leg-extension-prone-leg-curl |
| commercial | Matrix Aura 4-stack Multi-station | $14,898 | $10,274.48 | https://akfit.com/products/matrix-4-stack-multi-station |

### cable_crossover

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Body-Solid Deluxe Cable Crossover 250 GDCC250 | $2,770 | $2,770 | https://fitnesssuperstore.com/products/body-solid-deluxe-cable-crossover-250-gdcc250-new |
| value | French Fitness FFB Black Adjustable Cable Crossover | $3,299 | $3,299 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-adjustable-cable-crossover-new |
| value | Body-Solid SCC1200G Pro Clubline Cable Crossover | $4,275 | $4,275 | https://fitnesssuperstore.com/products/body-solid-scc1200g-pro-clubline-cable-crossover-new |
| value | Body-Solid S2CCO Series II Cable Crossover | $5,595 | $5,595 | https://fitnesssuperstore.com/products/body-solid-s2cco-series-ii-cable-crossover-new |
| commercial | Hoist CMD-6180 Cable Crossover | $7,195 | $7,195 | https://www.hoistfitness.com/products/cmd-6180-cable-crossover |
| commercial | Rogue CC-1 Cable Crossover | $6,725 | $6,725 | https://www.roguefitness.com/rogue-cc-1-cable-crossover |
| commercial | REP Fitness Hyperion - Series 1: Cable Crossover | $6,783.79 | $6,783.79 | https://repfitness.com/products/hyperion-series-1 |
| commercial | Nautilus Multi-Stations 9NP-M9201 Cable Cross Over | $8,389 | $8,389 | https://fitnesssuperstore.com/products/nautilus-multi-stations-9np-m9201-cable-cross-over-new |
| premium | Life Fitness Adjustable Cable Crossover | $9,370 | $9,370 | https://shop.lifefitness.com/products/life-fitness-adjustable-cable-crossover |
| premium | Matrix Aura Adjustable Cable Crossover | $10,665.37 | $7,355.43 | https://akfit.com/products/matrix-aura-cable-crossover-2-x-200lbs-stacks |

### functional_trainer

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | REP Fitness Arcadia - Functional Trainer | $2,199.99 | $2,199.99 | https://repfitness.com/products/arcadia-functional-trainer |
| value | REP Fitness Arcadia Max Functional Trainer | $2,699.99 | $2,699.99 | https://repfitness.com/products/arcadia-max-functional-trainer |
| value | Titan Fitness Functional Trainer | $2,499.97 | $2,499.97 | https://titan.fitness/products/functional-trainer |
| value | Body-Solid GFT100 Functional Trainer | $2,315 | $2,315 | https://fitnesssuperstore.com/products/body-solid-gft100-functional-trainer-new |
| value | French Fitness FFB Black Dual Adjustable Pulley | $3,099 | $3,099 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-dual-adjustable-pulley-new |
| commercial | Life Fitness Axiom Dual Adjustable Pulley | $6,250 | $6,250 | https://shop.lifefitness.com/products/axiom-dual-adjustable-pulley |
| commercial | Hoist HD-3000 Dual Pulley Functional Trainer | $6,720 | $6,720 | https://www.hoistfitness.com/products/hd-3000-dual-pulley-functional-trainer |
| commercial | Nautilus Instinct Dual Adjustable Pulley 9NL-D2002-60AAS | $5,099 | $5,099 | https://fitnesssuperstore.com/products/nautilus-instinct-dual-adjustable-pulley-9nl-d2002-60aas-new |
| commercial | Body-Solid S2FT Series II Functional Trainer | $5,215 | $5,215 | https://fitnesssuperstore.com/products/body-solid-s2ft-series-ii-functional-trainer-new |
| commercial | Prime Functional Trainer | $6,250 | $6,250 | https://www.primefitnessusa.com/products/functional-trainer |
| commercial | Rogue FT-1 Functional Trainer | $6,825 | $6,825 | https://www.roguefitness.com/rogue-ft-1-functional-trainer |
| commercial | Matrix Versa Functional Trainer w/ 18" Storage | $6,798 | $4,688.28 | https://akfit.com/products/matrix-versa-150-lbs-functional-trainer-light-18-s |
| premium | Life Fitness Dual Adjustable Pulley | $10,053 | $10,053 | https://shop.lifefitness.com/products/life-fitness-dual-adjustable-pulley |
| premium | Nautilus Inspiration Dual Adjustable Pulley NP-D9302 | $7,889 | $7,889 | https://fitnesssuperstore.com/products/nautilus-inspiration-dual-adjustable-pulley-np-d9302-new |
| premium | Watson Dual Adjustable Pulley | $8,393.64 | $5,788.72 | https://akfit.com/products/watson-dual-adjustable-pulley |
| premium | Matrix Aura Functional Trainer | $14,229.84 | $9,813.68 | https://akfit.com/products/matrix-aura-functional-trainer-with-300lb |

### cable_column

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | REP Adonis Cable Tower (plate-loaded + selectorized, no base) | $2,299.99 | $2,299.99 | https://repfitness.com/products/adonis-cable-tower |
| value | Titan Fitness Cable Tower / 10 - 320 LB Selector | $2,699.97 | $2,699.97 | https://titan.fitness/products/cable-tower-10-320-lb-selector |
| value | French Fitness FFB Black Cable Column | $2,799 | $2,799 | https://fitnesssuperstore.com/products/french-fitness-ffb-black-cable-column-new |
| value | Body-Solid S2CC Series II Cable Column | $3,010 | $3,010 | https://fitnesssuperstore.com/products/body-solid-s2cc-series-ii-cable-column-new |
| value | Rogue CT-1 Cable Tower | $3,095 | $3,095 | https://www.roguefitness.com/rogue-ct-1-cable-tower |
| commercial | Hoist CMS-6175 Stand Alone Hi-Lo Pulley | $3,160 | $3,160 | https://www.hoistfitness.com/products/cms-6175-stand-alone-hi-lo-pulley |
| commercial | Matrix Aura Adjustable Pulley | $3,698 | $2,550.34 | https://akfit.com/products/matrix-aura-adjustable-pulley-200lbs-stack |

### dumbbell_rack_2tier

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | REP Fitness Commercial Dumbbell Rack | $649.99 | $649.99 | https://repfitness.com/products/commercial-dumbbell-rack |
| value | French Fitness 2 Tier Saddle Dumbbell Rack, 10 Pairs | $899 | $899 | https://fitnesssuperstore.com/products/french-fitness-2-tier-saddle-dumbbell-rack-10-pairs-new |
| value | Body-Solid SDKR500DB 2-Tier PCL Dumbbell Rack | $840 | $840 | https://fitnesssuperstore.com/products/body-solid-sdkr500db-2-tier-pcl-dumbbell-rack-new |
| value | Victory 2-Tier Dumbbell Rack | $699.99 | $699.99 | https://repfitness.com/products/victory-2-tier-dumbbell-rack |
| commercial | Life Fitness Two Tier Dumbbell Rack | $1,894 | $1,894 | https://shop.lifefitness.com/products/life-fitness-two-tier-dumbbell-rack |
| commercial | Hoist CF-3461-2 2-Tier Dumbbell Rack | $1,615 | $1,615 | https://www.hoistfitness.com/products/cf-3461-2-2-tier-horizontal-dumbbell-rack |
| commercial | Nautilus Instinct Dumbbell Rack 10-Pair 2 Tier 9NN-R8001-60ARS | $1,249 | $1,249 | https://fitnesssuperstore.com/products/nautilus-instinct-dumbbell-rack-10-pair-2-tier-9nn-r8001-60ars-new |
| premium | Hammer Strength Two Tier Dumbbell Rack | $1,756 | $1,756 | https://shop.lifefitness.com/products/hammer-strength-two-tier-dumbbell-rack |
| premium | Matrix Magnum 2-Tier Flat Tray Dumbbell Rack | $2,071.33 | $1,428.50 | https://akfit.com/products/matrix-magnum-2-tier-flat-tray-dumbbell-rack |

### dumbbell_rack_3tier

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | REP Commercial Dumbbell Rack (Three-Tier) | $839.99 | $839.99 | https://repfitness.com/products/commercial-dumbbell-rack |
| value | Rogue 3 Tier Dumbbell Rack | $992.50 | $992.50 | https://www.roguefitness.com/rogue-3-tier-dumbbell-rack |
| value | French Fitness 3 Tier Saddle Dumbbell Rack, 10 Pairs | $899 | $899 | https://fitnesssuperstore.com/products/french-fitness-3-tier-saddle-dumbbell-rack-10-pairs-new |
| value | Body-Solid SDKR1000DB 3-Tier PCL Dumbbell Rack | $1,155 | $1,155 | https://fitnesssuperstore.com/products/body-solid-sdkr1000db-3-tier-pcl-dumbbell-rack-new |
| commercial | Life Fitness 3-Tier Hex Dumbbell Rack (5-50) | $1,549 | $1,549 | https://shop.lifefitness.com/products/life-fitness-3-tier-hex-dumbbell-rack-5-50 |
| commercial | Hoist CF-3461-3 3-Tier Dumbbell Rack | $2,015 | $2,015 | https://www.hoistfitness.com/products/cf-3461-3-3-tier-horizontal-dumbbell-rack |
| commercial | Rogue Monster 3 Tier Dumbbell Rack | $1,650 | $1,650 | https://www.roguefitness.com/rogue-monster-3-tier-dumbbell-rack |
| commercial | Nautilus Instinct Dumbbell Rack 10-Pair 3 Tier 9NN-R8002-60ARS | $1,319 | $1,319 | https://fitnesssuperstore.com/products/nautilus-instinct-dumbbell-rack-10-pair-3-tier-9nn-r8002-60ars-new |
| premium | Hammer Strength Three Tier Dumbbell Rack | $2,040 | $2,040 | https://shop.lifefitness.com/products/hammer-strength-three-tier-dumbbell-rack |
| premium | Matrix Magnum 3-Tier Flat-Tray Dumbbell Rack | $2,986.30 | $2,059.52 | https://akfit.com/products/matrix-magnum-3-tier-flat-tray-dumbbell-rack |

### plate_tree

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | REP Fitness Bar & Weight Plate Tree | $179.99 | $179.99 | https://repfitness.com/products/bar-and-weight-plate-tree |
| value | Rogue Vertical Plate Tree 2.0 | $270 | $270 | https://www.roguefitness.com/rogue-vertical-plate-tree-2-0 |
| value | Body-Solid GWT56 Weight Tree | $230 | $230 | https://fitnesssuperstore.com/products/body-solid-gwt56-weight-tree-new |
| value | French Fitness OWT30 Olympic Weight Tree Storage Rack | $289 | $289 | https://fitnesssuperstore.com/products/french-fitness-owt30-olympic-weight-tree-storage-rack-new |
| value | Titan Fitness Portable Weight Plate and Barbell Storage Tree | $219.97 | $219.97 | https://titan.fitness/products/portable-plate-barbell-storage-tree |
| commercial | Life Fitness Olympic Weight Tree | $800 | $800 | https://shop.lifefitness.com/products/olympic-weight-tree |
| commercial | Hoist CF-3443 Olympic Plate Tree | $940 | $940 | https://www.hoistfitness.com/products/cf-3443-olympic-plate-tree |
| commercial | Hoist CF-3444 4-Sided Olympic Plate Tree | $1,075 | $1,075 | https://www.hoistfitness.com/products/cf-3444-4-sided-olympic-plate-tree |
| premium | Matrix Magnum Weight Tree w/Bar Holders | $886.91 | $611.66 | https://akfit.com/products/matrix-mg-weight-tree |
| premium | Nautilus 2-Sided Olympic Weight Tree | $1,208 | $833.10 | https://akfit.com/products/2-sided-olympic-weight-tree |

### kettlebell_rack

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | REP Fitness Kettlebell Rack 2.0 | $449.99 | $449.99 | https://repfitness.com/products/kettlebell-rack-2-0 |
| value | REP Kettlebell Rack 2.0 (Three-Tier) | $579.99 | $579.99 | https://repfitness.com/products/kettlebell-rack-2-0 |
| value | French Fitness 3 Tier Kettlebell Rack | $379 | $379 | https://fitnesssuperstore.com/products/french-fitness-3-tier-kettlebell-rack-new |
| value | Body-Solid GKR60 Kettlebell Rack | $340 | $340 | https://fitnesssuperstore.com/products/body-solid-gkr60-kettlebell-rack-new |
| value | Bells of Steel Kettlebell Rack | $337.99 | $337.99 | https://www.bellsofsteel.us/products/kettlebell-rack |
| commercial | Body-Solid Body Solid SDKR1000KB 3 Tier PCL Kettlebell Rack | $1,130 | $1,130 | https://fitnesssuperstore.com/products/body-solid-sdkr1000kb-3-tier-pcl-kettlebell-rack-new |
| commercial | Life Fitness 3-Tier Accessory Rack | $1,549 | $1,549 | https://shop.lifefitness.com/products/life-fitness-3-tier-accessory-rack |

### barbell_rack

| Tier | Product | Price | Price used (AK÷1.45) | URL |
|---|---|---:|---:|---|
| value | Titan Fitness Fixed Barbell Rack | $359.97 | $359.97 | https://titan.fitness/products/fixed-barbell-rack |
| value | Body-Solid SBBR100 Fixed Weight Barbell Rack | $665 | $665 | https://fitnesssuperstore.com/products/body-solid-sbbr100-fixed-weight-barbell-rack-new |
| value | Bells of Steel Fixed Barbell Rack | $399.99 | $399.99 | https://www.bellsofsteel.us/products/fixed-barbell-rack |
| commercial | Life Fitness Barbell Rack | $1,040 | $1,040 | https://shop.lifefitness.com/products/life-fitness-barbell-rack |
| commercial | Hoist CF-3465 Barbell Rack | $1,480 | $1,480 | https://www.hoistfitness.com/products/cf-3465-barbell-rack |
| premium | Life Fitness Barbell Rack (10-bar) | $1,659 | $1,659 | https://shop.lifefitness.com/products/life-fitness-barbell-rack |
| premium | Matrix Magnum Barbell Rack | $2,469.87 | $1,703.36 | https://akfit.com/products/matrix-magnum-barbell-rack |

## 7b. Other notable listings captured (not used as anchors)

- Hammer Strength MTS (selectorized iso-lateral) line: $8,318 (Abdominal Crunch) to $8,658 (Chest Press, Row, High Row, Front Pulldown, Shoulder Press, Leg Extension, Kneeling Leg Curl) — LF store.
- Hammer Strength plate-loaded specialty: Super Fly $5,040; V-Squat $6,119; Super Squat Press $7,883; Iso-Lateral Chest/Back $5,458; Iso-Lateral D.Y. Row $4,245; Pullover $4,907; Lateral Raise $3,694; Seated/Standing Shrug $2,702; Ground Base Jammer $3,584; Combo Twist $3,694; Plate Loaded Vertical Smith $7,442; Assisted Nordic Ham $4,907; Glute Ham Reverse Hyper Combo $4,960 — LF store.
- Hammer Strength free-weight/racks: HD Athletic NX Squat Stand $2,214; Rubber Platform 4x8 stand-alone $844 / 6x8 $910 / rack insert $1,816–2,081; Traditional Wood Platform $4,980–7,909; Impact Suppression Platform $5,570–8,024; Multi-Adjustable Bench $1,854; Adjustable Decline Bench $1,709; Back Extension $1,794; Chin/Dip/Leg Raise $2,422; Seated Arm Curl $1,709.
- Life Fitness free weights: Universal Cable $12,284 (consumer shop) / $7,616 (facility shop); Adjustable Cable Crossover $9,370; Dual Adjustable Pulley $10,053–11,024; Smith Machine $7,641; Leg Raise $2,272; Dip/Leg Raise $1,730; Chin/Dip/Leg Raise $2,615; Ab Crunch Bench $2,438; Multi-Adjustable Bench $2,001; PWR Play 3/4/5-station rigs $13,004 / $19,067 / $21,272.
- Rogue machines/cables: Iso Leg Press 35 $6,550; LP-2 Lat Pulldown/Low Row $3,650; Monster Lat Pulldown/Low Row (stand-alone) $3,250; CC-1 Cable Crossover $6,725; FT-1 Functional Trainer $6,825; CT-1 Cable Tower $3,095; CT-1X2 $3,525; FM-6 Functional Trainer $5,395 (Twin $6,195); Monster Rhino Belt Squat stand-alone $2,415 (+rack $3,685); Pit Shark $4,680; Westside Scout Hyper $415; Z Hyper $965; T Bar Row $875; Indy T-Bar Row $445; Monster Westside Bench $1,595; RM-43 rack $5,650; Monster Lite Cave $5,700.
- Hoist: MotionCage packages $21,240–33,490 (studio packages $10,670–20,020); multi-jungle pods 4-station $10,485, 6-station $14,455, 9-station $21,780, 14-station $33,980; HD-4000 Simple Trainer $8,555; white-glove install fees $100–800 per product.
- Prime: Prodigy HLP plate-loaded rack $5,100–5,250, HLP selectorized rack $5,875–6,150; Intek Armor urethane dumbbell bundles 5–50 $5,170 and 55–100 $8,932 (composition not stated).
- Sorinex: Apex Rack $8,450; Leverage Chest Press $4,999; Leg Press $6,499; Hack Squat $5,999; Multi-Squat $4,999; Back Attack $4,999; X-Factor $3,999; Chest Supported Row $2,847; Standing Leg Curl $1,599; Seated Calf $999; Recon Bench $799; Free-standing J-Squat $1,419.
- Booty Builder: all machines return $9,990–9,999 from the store API (placeholder, quote-only).

## 8. Dealer-price dispersion (why AKFIT prices were adjusted)

Identical Nautilus SKUs listed at AKFIT (Anchorage, AK dealer) vs Fitness Superstore (lower-48 dealer), 2026-10-28: ratio 1.38–1.53, median **1.49** (n=54). Examples: Nautilus Impact Chest/Leg Extension/Low Row $7,726.62 vs $5,599 (1.38); Instinct Dual Leg Press/Calf $7,123 vs $4,839 (1.47); Inspiration Leg Press $13,699 vs $9,279 (1.48); Leverage Chest Press $6,438 vs $4,299 (1.50); Nautilus Half Rack $5,753 vs $3,869 (1.49). AKFIT shows a `compare_at` of $8,082 on Impact singles (vs $7,726.62 price), consistent with AKFIT pricing near MSRP and Fitness Superstore pricing ~27–33% below. Matrix (only priced at AKFIT) was therefore scaled by 1/1.45 — e.g. Aura Chest Press $6,612.53 → ~$4,560, consistent with search-indexed US dealer listings of $3,895–4,707.69 for the G3-S10 (not fetched; see conflicts).

## 9. Refurbished / remanufactured market

| Model | New list (LF store) | Fitness Superstore reman. | ratio | CTX Home Gyms reman. | ratio |
|---|---:|---:|---:|---:|---:|
| HS Select Chest Press | $5,972 | $3,899 | 0.65 | $1,995 | 0.33 |
| HS Plate-Loaded Iso-Lateral Bench Press | $4,135 | $3,899 | 0.94 | $2,795 | 0.68 |
| HS Smith Machine | $7,442 | $4,299 | 0.58 | $2,995 | 0.4 |
| LF Insignia Leg Extension | $8,315 | $4,399 | 0.53 | $3,495 | 0.42 |
| LF Insignia Shoulder Press | $7,843 | $4,199 | 0.54 | $2,995 | 0.38 |
| HS PL Linear Leg Press | $7,883 | $4,199 | 0.53 | $3,095 | 0.39 |
| HS PL Seated Calf Raise | $2,352 | $2,699 | 1.15 | $999 | 0.42 |
| HS HD Elite Half Rack vs HD Elite iD new | $6,229 | $3,899 | 0.63 | $1,495 | 0.24 |
| HS Select Leg Extension | $6,430 | $4,199 | 0.65 | $2,795 | 0.43 |
| HS Select Seated Leg Curl | $6,728 | $3,999 | 0.59 | $2,995 | 0.45 |
| HS Select Biceps Curl | $5,509 | $3,899 | 0.71 | $2,495 | 0.45 |
| HS Select Triceps Extension | $5,509 | $4,099 | 0.74 | $1,995 | 0.36 |
| HS Select Pec Fly/Rear Delt | $5,972 | $4,399 | 0.74 | $2,995 | 0.5 |
| HS Select Seated Leg Press | $9,449 | $4,399 | 0.47 | $3,495 | 0.37 |
| LF Insignia Biceps Curl | $7,733 | $3,899 | 0.5 | $2,795 | 0.36 |

Median ratio: Fitness Superstore 0.63, CTX 0.4, pooled 0.5. Fitness Superstore remanufactured selectorized units cluster at $3,399–4,399 regardless of brand (Cybex VR3/Eagle, LF Pro/Insignia, Hammer Strength Select, Technogym Selection, Matrix Aura/G3, Precor Discovery); CTX lists the same classes at $1,295–3,495 (e.g. Cybex VR3 Arm Curl $1,495, Hoist Club Line Chest Press $1,995, HS Select Chest Press $1,995, LF Signature Leg Extension $3,295). Remanufactured jungle gyms: LF Signature MJ4 $5,995 (CTX) / $7,899 (FSS), Cybex MG-500 3-stack $4,999 (FSS). Recommended model: refurbished premium/commercial machine price = **0.50 × new premium list** (range 0.40–0.65), roughly equal to new commercial-tier pricing — attractive for small-budget gyms that want premium biomechanics.

## 10. Conflicts and how they were resolved

- **Matrix Aura G3-S10 chest press:** WebSearch summaries reported $3,895 (relinkonline, medical-market-only) and $4,707.69 (another US dealer); a direct fetch of the relinkonline product JSON on 2026-10-28 returned $10,000.00 (apparent placeholder); AKFIT lists $6,612.53. Resolution: use AKFIT ÷1.45 ≈ $4,560 (inside the $3,895–4,708 band).
- **Matrix Magnum 45° leg press:** search summary of Johnson Fitness listed $5,285 and $6,025 (pages returned HTTP 403 to fetch); AKFIT $10,423.99; Freedom Fitness 'sale' $2,500 (search summary, unverified). Resolution: AK÷1.45 = $7,189 kept as a premium anchor; treat $5.3–7.2k as the plausible new range.
- **Hammer Strength Iso-Lateral Bench Press:** LF store $4,135 (verified); search summaries: Fitness Zone $4,017, a reseller $2,999 (ILBPH), remanufactured $3,499 (Fitness Superstore, older index) vs $3,899 (live FSS feed) vs $1,795 (GymPros) vs $2,795 (CTX). Resolution: new = $4,135; refurb range $1,795–3,899.
- **LF Insignia Leg Extension:** LF store $8,315 in the live feed vs $7,950 'sale' in a search summary (older index); remanufactured $4,399 (FSS live), $3,495 (CTX live); certified-used $4,999 and a $1,400 listing (search summaries, unverified). Resolution: new = $8,315 (live).
- **Booty Builder hip-thrust machines:** the WooCommerce store API returns $9,990–9,999 for every machine (placeholder 'request a quote' values). Not used; hip_thrust_machine relies on Hammer Strength Glute Drive $4,907, Nautilus Glute Drive $4,319, Hoist CF-3416 $4,400, Titan $999.99, Bells of Steel $1,259.99.
- **Life Fitness 'Universal Cable'** shows $12,284 on the consumer shop and $7,616 on the facility shop (different configurations/feeds); not used as an anchor.
- **Tier overlap:** in plate-loaded machines, commercial (Hoist ROC-IT $3,815, Nautilus Leverage $4,299, Prime $3,000–6,650) and premium (Hammer Strength $4,135, Sorinex $3,399–4,999) overlap; the model should not assume premium > commercial for plate-loaded items. Similarly HS flat bench ($772) is cheaper than some commercial flat benches (LF $834–917).
- **Titan/REP product ratings:** much of the value tier is marketed to home gyms; for a commercial facility the safer value choices are Body-Solid ProClub/Series II, French Fitness FFB/Marin/Napa (commercial-rated per listing text), Rogue Monster Lite and REP's commercial items (e.g. Commercial Dumbbell Rack, Hyperion cable crossover).

## 11. Gaps

- No live new-price data for Cybex (Prestige/Eagle NX), Technogym (Selection/Pure), Gym80, Panatta, Atlantis, Arsenal Strength or Freemotion — these manufacturers do not publish US prices and the web-search budget was exhausted before dealer quotes could be located; only remanufactured prices exist for Cybex/Technogym/Freemotion (Fitness Superstore $3,399–4,699 selectorized; Technogym Kinesis/Plurima $4,199–12,299).
- Matrix pricing comes from a single (Alaska) dealer; the 1/1.45 adjustment is derived from Nautilus SKU pairs, not Matrix pairs.
- Hammer Strength HD Elite power rack and HS Olympic flat/incline/decline benches are not sold new on the LF store; only remanufactured prices were found (HD Elite power rack $4,299, Olympic flat $2,349, incline $2,799, decline $2,599 at FSS).
- Chrome/pro-style dumbbells (Ivanko, Troy, York pro-style) were not captured beyond Titan stainless hex ($2.00–2.50/lb) and French Fitness urethane 'pro-style' sets ($2.71–3.64/lb).
- Negotiated fleet discounts, freight and installation are not modeled; Hoist publishes white-glove install fees of $100–800 per product as a reference.
- Booty Builder publishes no real prices (placeholders).
- Some value-tier stations mix residential- and commercial-rated equipment; durability-adjusted cost (cost per year of service) is not available from these sources.

## 12. Sources

- `src_rep` — REP Fitness online catalog (products.json feed and product pages) (REP Fitness, 2026) — https://repfitness.com/products.json — fetched=True
- `src_rogue` — Rogue Fitness product and category pages (JSON-LD offers and item tables) (Rogue Fitness, 2026) — https://www.roguefitness.com/rogue-rigs-racks/power-racks — fetched=True
- `src_rogue_iron` — Rogue Olympic Plates (cast iron) product page (Rogue Fitness, 2026) — https://www.roguefitness.com/rogue-olympic-plates — fetched=True
- `src_rogue_deepdish` — Rogue Deep Dish Plates product page (Rogue Fitness, 2026) — https://www.roguefitness.com/rogue-deep-dish-plates — fetched=True
- `src_rogue_machined` — Rogue Machined Olympic Plates product page (Rogue Fitness, 2026) — https://www.roguefitness.com/rogue-machined-olympic-plates — fetched=True
- `src_rogue_urethane_plates` — Rogue Urethane Plates product page (Rogue Fitness, 2026) — https://www.roguefitness.com/rogue-urethane-plates — fetched=True
- `src_rogue_echo` — Rogue Echo Bumper Plates V2 product page (Rogue Fitness, 2026) — https://www.roguefitness.com/rogue-echo-bumper-plates-with-white-text — fetched=True
- `src_rogue_hg` — Rogue HG 2.0 Bumper Plates product page (Rogue Fitness, 2026) — https://www.roguefitness.com/rogue-hg-2-0-bumper-plates — fetched=True
- `src_rogue_hexsets` — Rogue Dumbbell Sets (rubber hex) and Rogue Dumbbells (pairs) product pages (Rogue Fitness, 2026) — https://www.roguefitness.com/rogue-rubber-hex-dumbbell-sets — fetched=True
- `src_rogue_uredb` — Rogue Urethane Dumbbells product page (pairs and sets) (Rogue Fitness, 2026) — https://www.roguefitness.com/rogue-urethane-dumbbells-new — fetched=True
- `src_rogue_kb` — Rogue Kettlebells product page (Rogue Fitness, 2026) — https://www.roguefitness.com/rogue-kettlebells — fetched=True
- `src_lf_shop` — Life Fitness US online store (Life Fitness, Hammer Strength, Insignia, Axiom) products.json feed (Life Fitness, 2026) — https://shop.lifefitness.com/products.json — fetched=True
- `src_lf_facility` — Life Fitness facility (commercial) shop products.json feed (Life Fitness, 2026) — https://facilityshop.lifefitness.com/products.json — fetched=True
- `src_fss` — Fitness Superstore catalog (new Body-Solid, Nautilus, French Fitness; remanufactured commercial equipment) products.json feed (Fitness Superstore, 2026) — https://fitnesssuperstore.com/products.json — fetched=True
- `src_hoist` — Hoist Fitness online catalog (commercial CF/Club Line/ROC-IT/HD Dual MSRP) products.json feed (Hoist Fitness, 2026) — https://www.hoistfitness.com/products.json — fetched=True
- `src_prime` — Prime Fitness USA online catalog (Evolution, Hybrid, Plate Loaded, Prodigy, Intek) (Prime Fitness USA, 2026) — https://www.primefitnessusa.com/products.json — fetched=True
- `src_torque` — Torque Fitness online catalog (Torque Fitness, 2026) — https://www.torquefitness.com/products.json — fetched=True
- `src_titan` — Titan Fitness online catalog (Titan Fitness, 2026) — https://titan.fitness/products.json — fetched=True
- `src_bos` — Bells of Steel US online catalog (Bells of Steel, 2026) — https://www.bellsofsteel.us/products.json — fetched=True
- `src_akfit` — AKFIT (Alaska dealer) catalog incl. Matrix, Nautilus, Watson, Rogers Athletic, Torque commercial (AKFIT Fitness Superstore (Anchorage, AK), 2026) — https://akfit.com/products.json — fetched=True
- `src_ctx` — CTX Home Gyms remanufactured commercial equipment catalog (CTX Home Gyms, 2026) — https://ctxhomegyms.com/products.json — fetched=True
- `src_sorinex` — Sorinex product pages (embedded price): leverage machines, benches, Apex rack, Frankenhyper (Sorinex, 2026) — https://www.sorinex.com/shop — fetched=True
- `src_bootybuilder` — Booty Builder WooCommerce Store API (placeholder prices) (Booty Builder, 2026) — https://bootybuilder.com/wp-json/wc/store/v1/products?per_page=100 — fetched=True
- `src_ws_matrix_g3s10` — WebSearch summary: Matrix Aura G3-S10 dealer prices ($3,895 relinkonline; $4,707.69 other dealer); relinkonline product JSON re-fetched shows $10,000 placeholder (relinkonline / Matrix dealers, 2026) — https://relinkonline.com/products/matrix-fitness-g3s10-aura-chest-press — fetched=False
- `src_ws_johnson_magnum` — WebSearch summary: Johnson Fitness Matrix Magnum MG-PL70 45° leg press $5,285 / $6,025 (HTTP 403 on fetch) (Johnson Fitness & Wellness, 2026) — https://www.johnsonfitness.com/Matrix-Fitness-C13947.aspx — fetched=False
- `src_ws_hs_isobench` — WebSearch summary: Hammer Strength Iso-Lateral Bench Press listings (Fitness Zone $4,017; GymPros reman $1,795; Gym Experts $2,999) (Fitness Zone / GymPros, 2026) — https://www.fitnesszone.com/product/hammer-strength-plate-load-iso-lateral-bench-press.html — fetched=False
- `src_ws_insignia_le` — WebSearch summary: LF Insignia Leg Extension listings (LF $7,950 sale; Fitness Exchange certified used $4,999; Freedom Fitness $1,400) (Fitness Exchange / Freedom Fitness, 2026) — https://commercial.fitnessexchange.com/products/certified-used-life-fitness-insignia-series-leg-extension — fetched=False
