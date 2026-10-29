# Footprints & Clearances — Cardio and Functional Equipment

Research slice: `footprint_cardio_functional` · compiled 2026-10-28

This file covers the cardio and functional items in the equipment taxonomy. For each one it gives real commercial model specs: L x W x H, weight, max user weight, power, and the clearances from manuals or vendors. It then gives a **recommended model value** (footprint L x W and clearance front/back/left/right, in inches) that the layout packer can use.

> **Method notes / honesty flags**
> * Every spec below was read from a fetched page or PDF unless marked `fetched=false`. Quotes are verbatim, or near-verbatim where a PDF table had to be flattened to text.
> * The shared WebSearch budget ran out partway through. After that, sources were reached by direct URL (manufacturer sites, PDF links found on those sites). So a few items have fewer independent sources than planned (see **Gaps**).
> * `is_estimate` means the number is my own derivation. The derivation is always written out.

---

## 0. Conventions used by the recommended values

| Term | Meaning |
|---|---|
| **L (length)** | Dimension along the user's facing/working direction (front-to-back of the machine). For a lane/station it is the lane length. |
| **W (width)** | Side-to-side dimension. |
| **Front** | The end the user faces: console end for treadmill/elliptical/bike/stepper, flywheel end for a rower, fan end for an air bike, anchor/wall end for ropes, suspension straps and wall-ball. |
| **Back** | The opposite end. This is the ejection/fall zone for treadmills and the mount/step-off side for most machines. |
| **Left/Right** | Side clearances. For a recumbent stepper, **right = wheelchair-transfer side**. |
| **Shareable** | Neighbours may share side clearances, so two adjacent bikes need one 24 in gap, not 48 in. Keiser says this outright: *"When bikes are positioned adjacent to each other, the free area may be shared."* ADA 1004.1 also lets the required clear floor spaces overlap. A **treadmill rear zone** can overlap an aisle or another empty clearance zone, but never another unit's footprint, a wall, or furniture (LF: *"clear of any obstructions, including walls, furniture, and other equipment"*). |

Footprint values use roughly the **75th percentile** of the commercial flagship models found, rounded up to the next whole inch. Planning on a typical-to-large unit means a real purchase will not break the floor plan. The raw range is always given as well.

---

## 1. Cross-cutting rules and standards (apply to many items)

### 1.1 Treadmill fall zone (ASTM F2115 / EN ISO 20957-6, as written into manuals)
ASTM's current treadmill standard is **ASTM F2115-25 "Standard Specification for Treadmills"** (store.astm.org listing; paywalled, text not accessed, `fetched=false`). Its clearance numbers appear in manufacturer manuals:

| Source | Sides | Behind | Front | Evidence (quotes or labeled summaries) |
|---|---|---|---|---|
| Assault AirRunner owner's manual (non-motorized curved) | 19.7 in (0.5 m) | 79.0 in (2.0 m) | 19.7 in (0.5 m) | Summary: the manual attributes these access and emergency-dismount clearances to ASTM and EN guidance as of March 1, 2017. |
| Precor (P30 console manual, general rule) | 19.7 in | 78 in (2 m) | – | "Treadmills—a minimum of 0.5 m (19.7 in.) on each side of the treadmill and 2 m (78 in.) behind the machine." |
| Cybex 525T manual | 19.7 in | 78.7 in | – | "Minimum clearance is 19.7 inches (0.5 meters) on the sides of the unit" / "78.7 inches (2.0 meters) behind the unit" |
| Matrix T3xe owner's manual | **24 in (0.6 m)** | 79 in, at least treadmill width | – | "a clear zone behind the treadmill that is at least the width of the treadmill and at least 79" (2 meters) long" / "an accessible space on both sides of the treadmill of at least 24" (0.6 meters)" |

Assault also notes: *"ASTM standards are voluntary … The actual area for access, passage around, and emergency dismount is the responsibility of the facility."*

### 1.2 Non-treadmill cardio: the 0.6 m "free area" convention and Precor's general minimum
* **Precor (general rule):** "Cardio equipment other than treadmills—a minimum of 0.5 m (19.7 in.) on at least one side, and 0.5 m (19.7 in.) behind or in front the machine."
* **Keiser M3i manual** (it calls itself an EN ISO 20957-1 Class S product): "The minimum amount of free area space around the bike is 24 inches (610 mm) on all sides … When bikes are positioned adjacent to each other, the free area may be shared."
* **Matrix Performance cycles manual:** a diagram labels a **FREE AREA of 0.6 m (2 ft)** around the **TRAINING AREA** on all sides, plus "Ensure a minimum clearance width of 0.6 meters (24”) for access to and passage around MATRIX equipment. Please note, 0.91 meters (36”) is the ADA recommended clearance width for individuals in wheelchairs."
* The ISO 20957-1:2024 text itself is paywalled and was not accessed (`fetched=false`). The 0.6 m figure here comes from the manuals that cite the standard.

### 1.3 ADA 2010 Standards (U.S. DOJ; access-board.gov PDF, fetched)
* **206.2.13:** "Exercise machines and equipment required to comply with 236 shall be on an accessible route."
* **236.1:** "At least one of each type of exercise machine and equipment shall comply with 1004." The advisory says each kind of cardio machine (bike, rower, stair climber, treadmill) counts as a different type.
* **1004.1:** "Exercise machines and equipment shall have a clear floor space complying with 305 positioned for transfer or for use by an individual seated in a wheelchair. Clear floor or ground spaces required at exercise machines and equipment shall be permitted to overlap." The advisory says one clear space may be shared between two pieces of equipment.
* **305.3:** "The clear floor or ground space shall be 30 inches (760 mm) minimum by 48 inches (1220 mm) minimum."
* **403.5.1:** "the clear width of walking surfaces shall be 36 inches (915 mm) minimum" (32 in allowed at short points).

### 1.4 Sport England "Fitness and Exercise Spaces" Design Guidance Note (2008, Rev 002), fetched
* "Calculation of the total area and capacity of the fitness gym should be based upon a floor area of **5m2 per piece of equipment**. This includes an allowance for circulation space around the equipment."
* Space table (machine footprint range | circulation):
  * Resistance area: 2 m²/machine | 1.75x machine footprint
  * Cardio vascular area: **1.5–2.0 m²/machine | 1.75x machine footprint**
  * Free weights area: 2.5–3.5 m²/machine | 2x machine footprint
  * **Stretch Area: 2.0–2.5 m²/person** | N/A
  * **Spinning Room: 1.0–1.5 m²/machine | 1.25x machine footprint**
  * Footnote: "Circulation includes the area immediately around the machine and the minimum aisle width to access the machine, but does not include the general circulation of the room."
* Ceiling: "The optimum ceiling height should be between 3.5 - 4m … and should not be lower than 2.7m."
* Stretch area: "vinyl covered padded floor matting and wall mounted mirrors … A wall barre should be provided at a height approximately 1.2m above the floor."

### 1.5 Life Fitness "Recommended Live Area"
For some products Life Fitness publishes a **Recommended Live Area** (footprint plus the usable space around it). Example: SYNRGY Accessory Storage System, footprint 36 x 25 x 67 in, live area **37 x 50 x 84 in**. None of the LF cardio pages checked publish one.

---

## 2. Summary — recommended model values (inches)

| id | Footprint L x W | Front | Back | Left | Right | Height (typ.) | Power | Basis |
|---|---|---|---|---|---|---|---|---|
| treadmill | 84 x 36 | 12* | **79** | 20 | 20 | 56–68 | **Dedicated 120 V/20 A circuit per unit** | ASTM/EN via LF, Precor, Cybex, Matrix manuals |
| curved_treadmill | 70 x 34 | 20 | **79** | 20 | 20 | 63–72 | none (self-powered / AA batteries) | Assault AirRunner manual (ASTM+EN) |
| elliptical | 84 x 30 | 12 | 24 | 24 | 24 | 63–72 | 120 V/15 A (Precor); LF self-powered or 120 V/20 A dedicated for powered consoles | LF CLSX manual, Matrix, Precor |
| upright_bike | 49 x 26 | 12 | 24 | 24 | 24 | 54–63 | self-powered, or 120 V/15 A; Matrix: ≤4 units per dedicated 15 A circuit | Matrix 0.6 m free area; LF |
| recumbent_bike | 67 x 27 | 12 | 24 | 24 | 24 | 51–60 | same as upright | LF CLSR manual; Matrix |
| indoor_cycle | 53 x 23 | 24 | 24 | 24 | 24 | 46–50 | none | Keiser M3i (shareable) |
| air_bike | 55 x 30 | 24* | 24* | 24* | 24* | 52–58 | none | estimate (0.6 m convention) |
| rower | 96 x 26 | 6 | 6 | 12 | 12 | 20–22 (seat 14) | AA/D batteries | derived from Concept2 "9 ft x 4 ft with clearance for use" |
| stair_climber | 61 x 34 | 12* | 24* | 24* | 24* | 79–82 | 8Gx: 12 V/5 A supply; PowerMill 100–240 V 5 A | estimate; **ceiling ≥ 120 in** (StairMaster) |
| ski_erg | 50 x 24 | 12* | 24* | 12* | 12* | 85 | 2 D batteries | Concept2 floor-stand footprint; clearances estimated |
| recumbent_stepper | 73 x 30 | 12 | 12 | 24 | **30** (transfer side) | 46–52 | 12 V battery / adapter | NuStep manual + ADA 305.3 |
| rig_bay (per 4-ft bay) | 48 x 48 | 60 | 60 (0 if wall-mounted) | 60 at run ends only | 60 at run ends only | 105 | none | Throwdown XTC "recommended floor space" (= footprint + 5 ft per side) |
| turf_lane (per lane) | 600 x 60 (range 300–1080 L) | 36* | 36* | 0 to next lane / 24* | 0 / 24* | – | none | Rogue GymTurf 5 ft rolls; Torque "30-yard optimal, 10 yards workable" |
| sled (parked) | 52 x 33 | 12* | 12* | 12* | 12* | 37–38 | none | Torque TANK M4/M1S, Rogue Echo Dog Sled |
| plyo_box_set | 36 x 30 | 48* | 36* | 24* | 24* | ≤62 stacked | none | Rogue / Throwdown box footprints; use zone estimated |
| wall_ball_station | 26 x 48 | 60* | 0 (wall) | 12* | 12* | target 108–120 | none | Rogue 14 in balls, 16 in target at 9/9.5/10 ft; LF med-ball rack |
| battle_rope_station (30 ft rope) | 204 x 72 | 0 (anchor) | 24* | 12* | 12* | – | none | derived: lane = rope/2 + 24 in stance |
| suspension_trainer_station | 96 x 72 | 12* | 12* | 12* | 12* | anchor 84–108 | none | TRX anchor height 7–9 ft; zone estimated |
| heavy_bag | 24 x 24 | 45 | 15 | 15 | 15 | 48–72 bag | none | Throwdown SSTT 4'x7' zone + 4.5 ft bag spacing |
| stretch_area (per user) | 72 x 24 | 4 | 4 | 12 | 12 | – | none | Sport England 2.0–2.5 m²/person |
| accessory_pack (storage rack) | 25 x 36 | 25 | 0 | 0 | 0 | 67 | none | LF accessory rack footprint + LF live area |
| kettlebell_set (rack) | 24 x 77 | 36* | 0 | 0 | 0 | 29–45 | none | Rogue USS 2.0 footprint; front access estimated |

`*` = estimate (derivation in the item section). Shelf/rack items list depth first (L = depth from the wall).

---

## 3. CARDIO

### 3.1 treadmill (commercial motorized)

| Model | L x W x H (in) | Unit wt (lb) | Max user (lb) | Power | Source |
|---|---|---|---|---|---|
| Life Fitness Integrity (S/D base) | 82 x 36 x 56 (209x92x142 cm) | 425 (S) / 434 (D) | 400 | "Dedicated 120 volts/20 amp circuit (voltage may vary outside U.S.)"; sell sheet: "All treadmills should be installed with a dedicated electrical circuit – line, neutral, ground (a single circuit breaker for each treadmill) 120V, 20A or 230V, 10A" | LF US page; LF AU sell sheet |
| Life Fitness Integrity+ | 82 x 36 x 56 | 434 | 400 | "Dedicated 120 volts/20 amp circuit" | LF US page |
| Life Fitness Atmos | 82 x 32 x 60.8 (SL) / 61.4 (SE4) | 370 | 400 | "All treadmills require a dedicated electrical circuit line, neutral, ground, and a single dedicated circuit breaker per unit." "120V, 20A or 230V, 10A" | LF US page |
| Precor TRM 885 | 83 x 35 x 68 (211x89x173 cm) | 430 | 400 | "US & Canada: 120V/20A individual branch circuit; International: 240V" | precor.com; Precor 2025 brochure PDF |
| Star Trac 8TRx | 81 x 35.5 x 60 (206x90x152 cm) | 465 | **500** | "110V/20 Amp dedicated circuit with NEMA 5-20 outlet; or 220V/15 Amp dedicated circuit with NEMA 6-15 outlet" | corehandf.com product page; Core 2026 catalog |
| Star Trac FreeRunner 10TRx | 81 x 35 x 60 | 515.2 | n/a | n/a | Core 2026 catalog |
| Matrix Performance | 86.7 x 36.5 x 66.3 | 434.3 | 400 | n/a | us.matrixfitness.com (search snippet only, `fetched=false`) |

Running surfaces are 60 x 22 in on all flagship units. Step-up heights run 7.5–11 in.

**Clearances:** see §1.1. All sources agree on **2 m (78–79 in) behind**, across the full treadmill width. Sides are 0.5 m (19.7 in) per ASTM/Precor/Cybex/LF, or 0.6 m (24 in) per Matrix. None of the motorized-treadmill manuals asks for front clearance. Assault (non-motorized) asks for 0.5 m in front.

**Recommended:** footprint **84 x 36** (75th percentile is 83 x 36; L rounded up to 84). **Back 79** (2 m, ASTM/EN). **Left/Right 20** (0.5 m; use 24 for Matrix-style compliance; can be shared between adjacent treadmills). **Front 12** is an estimate: no motorized-treadmill manual needs front clearance, but 12 in leaves room for the front-mounted power cord/outlet and service access.
Zone with no sharing: 175 x 76 in = 92 ft². In a row with shared sides: 175 x 56 in = 68 ft².
Sport England cross-check: an 84 x 36 footprint is 1.95 m², inside the 1.5–2.0 m² CV range. Footprint plus 1.75x circulation is about 5.4 m² (58 ft²).

### 3.2 curved_treadmill (non-motorized)

| Model | L x W x H (in) | Unit wt (lb) | Max user (lb) | Power | Source |
|---|---|---|---|---|---|
| Woodway Curve | 70 x 33 x 72 (178x84x183 cm) | 355 | n/a on page | "Electrical: Not Required for Standard Display Curve" | woodway.com |
| Woodway Curve LTG | 67 x 34 x 70 | 297 | 350 running | – | roguefitness.com ($3,495) |
| TrueForm Runner | 64 x 31 x 63 (Rogue) / 64 x **36** x 63 (Iron Co) | 350 | 700 (Rogue) / "700 lbs. walking / 450 lbs. running" (Iron Co) | – | Rogue ($6,595); Iron Company |
| Assault AirRunner | 69.7 x 33.1 x 64.0 (1770x841x1626 mm) | 280 | 350 (158.8 kg) | 4 AA batteries | AirRunner owner's manual PDF |
| Throwdown HIITMill X | 78 x **55** x 66 | 441 | 350 | – | Core 2026 catalog (55 in width looks like it includes the handrails; flagged) |
| Technogym Skillmill | ~75 x 35 x 61 (1910x890x1540 mm) | ~397 (180 kg) | not confirmed | – | dealer/catalog excerpt via search (`fetched=false`) |

**Clearances:** Assault AirRunner manual, quoted in §1.1: **0.5 m left/right/front, 2.0 m behind**.
**Recommended:** **70 x 34**, front 20 / back 79 / left 20 / right 20. No electrical circuit needed.
Conflict: the TrueForm width is 31 in per Rogue and 36 in per Iron Company. The 34 in planning width sits between them. A 36-in TrueForm still fits inside the 20-in side clearances.

### 3.3 elliptical

| Model | L x W x H (in) | Unit wt (lb) | Max user (lb) | Power | Source |
|---|---|---|---|---|---|
| Precor EFX 885 | 80 x 28 x 71 (203x71x180 cm) | 340 | 350 | "120V/15A (US & Canada) / 240V (International)" | precor.com (fetched) |
| Life Fitness Integrity cross-trainer | 86 x 29 x 63.5 (218x73x161 cm); **active length 87 in** | 298 | 400 | NA: "120V, 20A outlet with dedicated line, neutral, ground wires and dedicated circuit breaker" (for powered console versions) | LF US page |
| Life Fitness Integrity CLSX (older gen) | 81.75 x 28 x 65 | 239 base / 243 w/ console | 350 | self-powered (6 V battery console); "If a properly grounded, 15amp outlet is not available, one must be installed" | LF CLSX operation manual |
| Star Trac 8CT Cross Trainer | 76 x 30 x 72 (193x76x182 cm) | 365 | n/a | n/a | Core 2026 catalog |
| (reference, home) LF E1 | 81.7 x 30 x 58.9 | 211 | 400 | 120 V | LF E1 assembly manual |

**Clearance evidence**
* LF CLSX manual: "Allow 1 foot of clearance in front of the Life Fitness Cross-Trainer to allow for movement of the pedal levers and at least 2 ft. (0.6 m) on the side." The same manual's safety list also says: "Keep the area 6.5 ft. (2 m) by 3 ft. (1 m) behind the Life Fitness cross-trainer clear of any obstructions" (looks like treadmill boilerplate; outlier).
* LF E1 assembly manual: "Allow a minimum clearance of 2 feet (0.6 meter) around the product."
* Matrix ascent trainer/elliptical manual (via search snippet; manualmachine page returned 403, `fetched=false`): "leave a 24" (610 mm) clearance on one side of the elliptical and 24" (610 mm) either in front or behind."
* Precor general rule: 0.5 m on at least one side and 0.5 m behind or in front.

**Recommended:** **84 x 30** (75th percentile is 82.8 x 29.2; LF needs 87 in active length, so add 3 in at the back for that model). Front 12 (LF), back 24 (0.6 m convention, LF E1, Matrix), sides 24 (LF/Matrix; shareable, so the gap between two ellipticals is 24 in).
Conflict: LF CLSX's 2 m x 1 m rear warning was **not** adopted, because no other elliptical source supports it. A strict-LF "conservative mode" could set back = 79.
Conflict: the Precor EFX 885 length was fetched as **80 in** from precor.com. One search snippet gave 86 x 28 x 71 in, and a retailer gave 80 x 30 x 67 in.

### 3.4 upright_bike

| Model | L x W x H (in) | Unit wt (lb) | Max user (lb) | Power | Source |
|---|---|---|---|---|---|
| Precor UBK 885 | 48 x 21 x 61 (122x53x155 cm) | 169 | 350 | 120V/15A (US&CA) | precor.com |
| Life Fitness Integrity Lifecycle upright | 41.5 x 24.5 x 54.5 (105x62x138 cm) | 169 | 400 | self-powered (C & X consoles); 120V 20A dedicated only for Attachable TV / Discover consoles | LF AU sell sheet |
| Star Trac 8UB | 46 x 25 x 63 (117x64x160 cm) | 150.8 | n/a | n/a | Core 2026 catalog |
| Matrix Performance upright | 51.5 x 25.7 x 60.5 (130.7x65.4x153.7 cm) | n/a | 400 | n/a | Matrix Performance cycles manual |
| Matrix U7xe (Premium, 2009) | 44 x 29 x 60 | 160 | 400 | "7xe: These products must be AC powered … daisy-chained together, up to 4 units per dedicated 15 amp circuit" | Matrix Premium cycles manual |

**Clearance evidence:** Matrix free area of 0.6 m (2 ft) around the training area. LF (Integrity bike manual, below) asks for 24 in each side, at least 1 ft in front, and a 3 ft front-or-rear warning. Precor general rule.
**Recommended:** **49 x 26** (75th percentile 48.9 x 25.2). Front 12, back 24, left 24, right 24 (shareable).

### 3.5 recumbent_bike

| Model | L x W x H (in) | Unit wt (lb) | Max user (lb) | Power | Source |
|---|---|---|---|---|---|
| Precor RBK 885 | 67 x 23 x 54 (170x58x137 cm) | 219 | 350 | 120V/15A | precor.com |
| Life Fitness Integrity recumbent | 67 x 26 x 51.5 | 211 (S) / 215 (D) | 400 | as upright | LF AU sell sheet (the sheet prints "67" (179 cm)"; 67 in = 170 cm, so the cm figure is a typo) |
| Star Trac 8RB | 65 x 28 x 60 (164x71x151 cm) | 208 | n/a | n/a | Core 2026 catalog |
| Matrix Performance recumbent | 59.2 x 25.7 x 55.1 | n/a | 400 | n/a | Matrix Performance cycles manual |
| Matrix R7xe | 62 x 29 x 54 | 174 | 400 | AC; ≤4 per dedicated 15 A circuit | Matrix Premium cycles manual |

**Clearance evidence (LF Integrity CLSR recumbent operation manual):** "WARNING: Allow a distance of 24 in. (0.6 m) between the widest part of the bike and other objects on either side. Provide at least 3 ft. (0.9 m) between the front or rear of the LIFE FITNESS bike to any other objects." Setup section: "Allow 1 foot of clearance in front … and at least 2 ft. (0.6 m) on the side." Power: "None (Optional External Power Supply 100-240 VAC, 1 Amp)". This manual's own dimension table (52.75 in long) disagrees with the 67-in sell sheet and was not used.
**Recommended:** **67 x 27**. Front 12, back 24, sides 24 (shareable). LF's 36-in front-or-rear warning is a conservative alternative.

### 3.6 indoor_cycle (spin bike)

| Model | L x W x H (in) | Unit wt (lb) | Max user (lb) | Source |
|---|---|---|---|---|
| Keiser M3i | 51 (depth) x 26 x 49 | 92 | 350 | Keiser M3i manual |
| Life Fitness IC7 | ~52 x 20.5 ("REQUIRED FOOT PRINT: APPROX. 132 X 52 CM"); max saddle/handlebar height ~47 in (120 cm) | 119 (54 kg) | 330 (150 kg) | LF IC7 manual |
| Schwinn AC Sport | 50 x 20 x 50 | 134 | n/a | Core 2026 catalog |
| Schwinn SC5 | 55 x 21 x 46 | 134 | n/a | Core 2026 catalog |

**Clearance:** Keiser M3i: "The minimum amount of free area space around the bike is 24 inches (610 mm) on all sides … When bikes are positioned adjacent to each other, the free area may be shared." Sport England spinning room: 1.0–1.5 m²/machine plus 1.25x footprint circulation.
**Recommended:** **53 x 23**, 24 in on all sides, shareable. In a shared grid each bike takes (53+24) x (23+24) = 77 x 47 in = 25 ft² (2.3 m²). That matches Sport England's 2.25–3.4 m² per spin bike including circulation.

### 3.7 air_bike (fan bike)

| Model | L x W x H (in) | Unit wt (lb) | Max user (lb) | Power | Source |
|---|---|---|---|---|---|
| AssaultBike Elite | 55.08 x 26.26 x 55 (FAQ/compare) ; spec table 47.9 x 26.2 x 56 | 138.89 (FAQ) / 125 (table) | 350 | "No electricity required" | assaultfitness.com |
| Rogue Echo Bike V3.0 | 55 (seat furthest back) x 29.5 (at handles) x 52.25 ; **floor footprint 44.5 x 23.75** | 123 | 330 | – | roguefitness.com ($945) |
| Throwdown HIIT Bike | 51 x 29 x 58 | 146 | 350 | – | Core 2026 catalog |

**Clearance:** no manufacturer air-bike clearance was found (gap).
**Recommended:** **55 x 30** (covers moving-arm width). 24 on all sides as an estimate: the 0.6 m free-area convention from the Keiser/Matrix bike manuals, since air-bike arms swing like an elliptical's. The front 24 also keeps the fan's airflow off whoever is next.
Conflict: Assault's own page gives two different sets of dimensions and weights. The larger (FAQ) set was used.

### 3.8 rower

| Model | L x W x H (in) | Unit wt (lb) | Max user (lb) | Power | Source |
|---|---|---|---|---|---|
| Concept2 RowErg | 96 x 24; seat 14 in (std) / 20 in (tall legs) | 57 / 68 | **500 ("as tested by Concept2")** | 2 D cells | concept2.com |
| Life Fitness Row HX Trainer | 83.85 x 20.47 x 22.04 | 71 dry / 108 with water | 330 | 4 AA | LF US page |
| Throwdown HIIT Rower | 96 x 26.5; seat 14 in | 82 | 350 | – | Core 2026 catalog |

**Clearance:** Concept2: "Assembled: 8 ft x 2 ft (244 cm x 61 cm)" and "**With Clearance for use: 9 ft x 4 ft (274 cm x 122 cm)**". Storage (standing upright): 25 x 33 x 54 in.
**Recommended:** **96 x 26** (75th percentile width 25.2). Clearances come from Concept2's use envelope (+12 in length, +24 in width, split evenly): **front 6, back 6, left 12, right 12**.
Concept2's BikeErg (for reference) also publishes "Clearance for use: 60 in x 48 in" on a 48 x 24 footprint, the same +12 / +24 pattern.

### 3.9 stair_climber (revolving stairs)

| Model | L x W x H (in) | Unit wt (lb) | Max user (lb) | Power | Ceiling | Source |
|---|---|---|---|---|---|---|
| StairMaster 8Gx | 58 x 34 x 79 (147x86x200 cm); step 8 in high, 10 in deep x 22 in wide; step-up 9 in | 509 | 400 | "12V/5Amp power supply" | **10 ft (3.05 m)** | corehandf.com 8Gx page; Core 2026 catalog |
| StairMaster 10G | 63 x 34 x 81 | 615 | n/a | n/a | 10 ft | Core 2026 catalog |
| Life Fitness PowerMill Climber | 55.92 x 32.81 x 82.3 (143x84x210 cm); step 7.5 in; step-up 10.5 in | 473 | 400 | "100-240 volts, 50/60 Hz, 5 Amps" | **9 ft (2.7 m)** | LF US page |
| StairMaster 4G (light commercial) | 54 x 29 x 64 | 348 | n/a | n/a | 8 ft | Core 2026 catalog |

**Clearance:** no manufacturer floor clearance was found for stair climbers (gap). Precor's general non-treadmill rule (0.5 m one side, 0.5 m front or back) is the only sourced minimum.
**Recommended:** **61 x 34** (75th percentile 60.5 x 34). Front 12, back 24 (mount/step-off at the rear), sides 24. All are estimates from the 0.6 m convention, which is more conservative than Precor's 0.5 m. **Ceiling ≥ 120 in** for StairMaster Gauntlet units; ≥ 108 in is enough for the PowerMill.

### 3.10 ski_erg

| Model | Footprint / H (in) | Weight (lb) | Max user | Power | Source |
|---|---|---|---|---|---|
| Concept2 SkiErg on floor stand | "23.5 in x 50 in x 85 in (60 cm x 127 cm x 216 cm)" (W x D x H) | 41 + 35 stand | not listed | 2 D cells | concept2.com |
| Concept2 SkiErg on wide floor stand | 32 x 52 x 85 | 41 + 42 | not listed | 2 D cells | concept2.com |
| Concept2 SkiErg wall-mounted | W 19 (bottom) – 20.5 (top) x D 16 x H 85 | 41 | – | – | concept2.com |
| Throwdown HIIT Ski | 20 W x 16 D x 85 (optional platform) | 52 | 350 | – | Core 2026 catalog |

**Clearance:** none published (gap).
**Recommended:** **50 x 24** (floor stand). Front 12, back 24 (step off the stand / hip hinge), sides 12 (the pull is in the sagittal plane; same lateral allowance as Concept2's RowErg). All are estimates. The unit is 85 in tall, so the ceiling must be at least 96 in (estimate).

### 3.11 recumbent_stepper (seated total-body)

| Model | L x W x H (in) | Unit wt (lb) | Max user (lb) | Power | Source |
|---|---|---|---|---|---|
| NuStep T5 | 73 x 30 x 46 (top-view drawing 72.3 x 29.1) | 285 (page) / 298 (manual) | 500 | 12 V battery | nustep.com; T5 manual Rev N |
| NuStep T5XR | 73 x 30 x 46 | 295 | 600 | 12 V battery | nustep.com |
| NuStep T6MAX | 73 x 30 x 52 (drawing 72.3 x 28.4) | 298 | 600 | AC adapter | nustep.com; T6 manual Rev E |
| SciFit StepOne | 68 x 30 x 48 | 312 | 450 (premium seat) / 500 (standard) | "Self generating; low voltage AC adapter included" | lifefitness.com |

**Clearance:** NuStep T5 and T6 manuals: "The minimum amount of required free space around the equipment is 24 inches (61 cm) for the sides, and 12 inches (30 cm) for the front and rear. **Additional free space is necessary to accommodate wheelchair access.**" ADA 305.3/1004.1: 30 x 48 in clear floor space positioned for transfer (may overlap with neighbours).
**Recommended:** **73 x 30**. Front 12, back 12, left 24, **right 30** (ADA parallel-approach transfer space: 48 in along the seat, 30 in out from the machine; use 48 if a forward approach is wanted).

---

## 4. FUNCTIONAL

### 4.1 rig_bay (one bay of a pull-up/functional rig)

| Product | Dimensions | Notes | Source |
|---|---|---|---|
| Throwdown Alpha XTC 4' Core | 46 x 48 x 105 in | 11-ga 3x6 in steel | Core 2026 catalog |
| Throwdown Alpha XTC 4' Add-On | 46 x 45 x 105 in | adds one bay (shares a post) | Core 2026 catalog |
| Throwdown XTC rigs, recommended floor space | 2x4 Compact → 14'x12'; 4x4 Compact → 14'x14'; 2x8 Compact → 18'x12'; 4x14 Std → 14'x24'; 4x24 Std → 14'x34'; 4x34 Std → 14'x44' | Each equals rig footprint + 10 ft in both dimensions, i.e. **5 ft (60 in) on every side** | Core 2026 catalog |
| Throwdown Functional Strength Station | 60 x 54 x 105 in → recommended 14' x 14' | | Core 2026 catalog |
| Rogue Monster Lite Monkey Rig 2.0 | "Total Rig Footprint: 24'-3" x 6'-8"", height 9' (12' center) | | roguefitness.com |
| Rogue W-4 wall-mount rig | "Foot Print 4' x 6'", height 9', 162 lb, $595 | | roguefitness.com |
| Rogue V2 Castro Rig | footprint 80 x 53 in, height 180 in, 474 lb | | roguefitness.com |
| Hammer Strength HD Perimeter (wall rig) | single side 39.75 x 7 x 97.2 in; "Recommended training space (single side): 123.75" x (Perimeter Width+48")"; max training weight 495 lb | barbell-oriented; about 117 in of working depth in front of the wall unit | lifefitness.com |

**Recommended:** **48 x 48** per 4-ft bay (Throwdown core 46 x 48; Rogue W-4 4 ft). Front 60, back 60 (0 if wall-mounted), left/right 60 **at the ends of a continuous rig run only** (0 between bays). All from Throwdown's +5 ft rule. For barbell-heavy bays use Hammer Strength's ~117 in front. Rig height is about 9 ft (97–108 in), so the ceiling must clear the rig plus pull-up/muscle-up head room. Rogue notes the wall-ball target "Will need a 9' or taller upright to reach competition height."

### 4.2 turf_lane (per lane)

| Source | Value |
|---|---|
| Rogue GymTurf | "Width: 5’", lengths 25' and 50', 5/8" high-density foam backing, pile ≈ 3/4", 90 lb (25') / 180 lb (50'), $1,089; usable to "create sled lanes, sprint tracks" |
| Torque TANK FAQ | "While a 30-yard run is optimal for pushing TANK™, you can get a high-intensity, full-body workout in on this push pull sled with only 10 yards of space available." |
| Torque TANK M4 (sled width) | 31.9 in wide; "bi-directional, eliminating the need to turn the unit around, which also reduces path width reserved for TANK™ runs" |

**Recommended:** lane width **60 in** (one GymTurf roll; leaves about 14 in either side of a 32-in sled). Length **600 in (50 ft)** as the default. The workable range is **360 in (10 yd, Torque minimum)** to **1080 in (30 yd, Torque optimum)**, and 300 in (one 25' roll) is the micro-gym option. End run-outs of **36 in** each are an estimate (room to stop, step around, or reverse a 50–70 in sled). Adjacent lanes share edges (0). Keep 24 in from other equipment (estimate).

### 4.3 sled

| Model | L x W x H (in) | Weight (lb) | Price | Source |
|---|---|---|---|---|
| Torque TANK M4 | 52.4 x 31.9 x 37.1 | 198 | $1,799 | roguefitness.com |
| Torque TANK M1S | 50.5 x 32.4 x 37.5 (wheelbarrow 69.8 x 32.4 x 17.7) | 113 | $1,299 | roguefitness.com |
| Rogue Echo Dog Sled | 36.5 x 25 x 37.5 | 87 (450+ lb capacity) | $290 | roguefitness.com |

**Recommended (parking footprint):** **52 x 33**, 12 in all round (estimate). It is normally parked at the end of a turf lane, inside the lane's run-out.

### 4.4 plyo_box_set

| Product | Footprint | Notes | Source |
|---|---|---|---|
| Rogue Foam Plyo Box (6/12/20/24 in) | "Foot Print: 28" x 28"" (all heights) | 7–27 lb each; full set $1,115; 3-set $790 | roguefitness.com |
| Rogue Games Box (3-in-1) | 30 x 20 x 24 in (heights 20/24/30) | 56 lb, $135 | roguefitness.com |
| Throwdown Power Plyo set | "wide 30"x36" base"; 6/12/24 boxes stack to 6–42 in | | Core 2026 catalog |

**Recommended:** storage/working footprint **36 x 30**. Use zone: front 48 (approach/take-off), back 36 (landing/step-down), sides 24. All estimates; no vendor use-zone guidance was found (gap).

### 4.5 wall_ball_station

| Item | Value | Source |
|---|---|---|
| Rogue medicine (wall) balls | "Diameter 14"", 4–30 lb | roguefitness.com |
| Rogue bolt-together wall-ball target | 16 in steel plate; "standard CrossFit wall ball height options of 9', 9.5’, and 10’"; "Will need a 9' or taller upright to reach competition height"; $105 | roguefitness.com |
| Life Fitness Vertical Medicine Ball Storage | footprint 25.5 x 25 x 56 in | lifefitness.com |
| Throwdown rig "Target + DPU adapter" | rig-mounted target accessory | Core 2026 catalog |

**Recommended:** station footprint **26 deep x 48 wide** against a wall or rig: one med-ball storage plus the throwing spot under the target. Front 60 (athlete squat/throw zone, using Throwdown's 5-ft working space around rigs), back 0 (wall), sides 12 (estimate). The wall or upright must reach a **10 ft** target center.

### 4.6 battle_rope_station

| Product | Lengths / dia / weight | Price | Source |
|---|---|---|---|
| Rogue Battle Rope | 50' x 1.5", 25 lb; "must be anchored to a smooth, round surface" | $139.99 | roguefitness.com |
| TRX Battle Rope | 1.5"; 30' (19 lb) / 50' (26 lb); "Must be anchored to sturdy, round surface like a pole or a tree" | $149.95 / $199.95 | commercial.trxtraining.com |
| Throwdown Battle Ropes | 1.5" x 20', 1.5" x 30', 2" x 30'; floor-mount and standing rope anchors | – | Core 2026 catalog |

**Derivation:** the rope loops around the anchor and the athlete holds both ends, so the anchor-to-hands distance is about rope length / 2. Add ~24 in of stance behind the hands.
**Recommended (30-ft rope default):** lane **204 x 72** (180 + 24 in long; 72 in wide for the wave envelope plus the athlete; width estimated). Front 0 (anchor at wall/rig/floor anchor), back 24, sides 12. For a 50-ft rope the lane is **324 x 72**. All are estimates.

### 4.7 suspension_trainer_station

| Item | Value | Source |
|---|---|---|
| TRX Suspension Anchor | "Accommodating anchor heights of 7-9ft"; strap 38 x 2 x 0.5 in | trxtraining.com |
| TRX Xtender | "Suggested to use when the anchor point is 9 ft or more off the ground" | trxtraining.com |
| TRX XMount | 6"L x 4.75"W x 2.5"D, 1.64 lb, "mounts to any load-bearing walls or ceiling studs" | trxtraining.com |

**Recommended:** anchor at **84–108 in** (TRX). The floor training zone (footprint) is **96 deep x 72 wide**, with 12 in all round. This is an estimate: the user's body extends 6–7 ft from the anchor in supine and plank exercises, and it matches Throwdown's 5-ft working ring around rig posts plus body length. On a rig, plan one user per 48-in bay.

### 4.8 heavy_bag

| Item | Value | Source |
|---|---|---|
| Throwdown 4' heavy bag | 16" x 48", 100 lb | Core 2026 catalog |
| Throwdown 6' heavy bag | 14" x 72", 120 lb filled | Core 2026 catalog |
| Throwdown freestanding punching bag | 24 x 24 x 67 in, listed "117 lbS (18.9 kg)" (unit mismatch in source) | Core 2026 catalog |
| Throwdown SSTT single-station training tree | 46.2 x 12 x 96.2 in; **"RECOMMENDED FLOOR SPACE 4’ x 7’"** | Core 2026 catalog |
| Throwdown FBR/ABR bag racks | **"BAG SPACING 4.5’ (137 cm)"**; recommended floor space per bag works out to 30.6 ft² (36-bag ABR) up to 66.5 ft² (8-bag ABR) | Core 2026 catalog |

**Recommended:** footprint **24 x 24** (bag swing envelope or freestanding base). Front 45 (striking stance), back 15, sides 15. This gives 54 in centre-to-centre spacing (Throwdown's 4.5 ft) and an 84-in zone length (SSTT's 7 ft). Total zone 54 x 84 in = 31.5 ft², which matches Throwdown's dense-rack figure of about 30.6 ft² per bag. The exact split of the zone into front/back/sides is my estimate; the totals are sourced.

### 4.9 stretch_area (per mat/user)

| Item | Value | Source |
|---|---|---|
| Sport England | "Stretch Area 2.0m²/person 2.5 m²/person" (= 21.5–26.9 ft²) | Sport England 2008 |
| Throwdown exercise mats | 21" x 48" and 21" x 66" | Core 2026 catalog |

**Recommended:** mat zone **72 x 24**, ends 4, sides 12. Total 80 x 48 in = 26.7 ft² = 2.48 m², the top of the Sport England range. Sides are shareable between mats, so a dense mat field uses about 2.0 m². Put it near the gym entrance, with padded flooring, mirrors and a barre at about 1.2 m (Sport England).

### 4.10 accessory_pack (bands, rollers, mats, stability balls + storage)

| Product | Footprint | Source |
|---|---|---|
| Life Fitness Accessory Storage Rack (SAR) | "36” x 25” x 67”" (94x66x171 cm) | lifefitness.com |
| Life Fitness SYNRGY Accessory Storage System | 36 x 25 x 67 in; **"Recommended Live Area (L x W x H): 37” x 50” x 84”"** | lifefitness.com |
| Rogue Universal Storage System 2.0 | "76.5" overall (70" shelf) x 23.75" (depth)"; H 29.25 (2-tier) / 45.25 (3-tier) | roguefitness.com |
| Rogue Mass Storage | 47" or 74" wide x 14" deep x 45.5/72.5" H | roguefitness.com |

**Recommended:** **25 deep x 36 wide**, front 25 (from LF's 50-in live-area depth), back/sides 0 (the 1-in length difference in the live area is ignored).

### 4.11 kettlebell_set (rack)

| Product | Footprint | Capacity | Price | Source |
|---|---|---|---|---|
| Rogue USS 2.0 (flat KB trays) | 76.5 x 23.75 in; H 29.25 / 45.25 | "enough to stack sixteen 70LB kettlebells stacked two deep" per 70" shelf | $395 / $467.50 | roguefitness.com |
| Rogue Mass Storage + KB shelf | 47 or 74 x 14 in | 600+ lb in plates per base unit | $415 configured | roguefitness.com |
| Throwdown Kettlebell Shelf, 4' | rig-mounted (dual post) | – | – | Core 2026 catalog |

**Recommended:** **24 deep x 77 wide**, front 36 (estimate: users hinge/squat to pick bells; matches the ADA 36-in route), back/sides 0.

---

## 5. Electrical summary (for the packer's "power drop" logic)

| Item | Requirement | Source |
|---|---|---|
| treadmill | **One dedicated 120 V/20 A circuit per treadmill** (NEMA 5-20) or 220–240 V 10–15 A dedicated (NEMA 6-15) | LF Integrity/Integrity+/Atmos; Precor TRM 885; Star Trac 8TRx |
| elliptical | Precor EFX 885 120 V/15 A; LF Integrity: dedicated 120 V/20 A for powered consoles, otherwise self-powered | Precor; LF |
| upright/recumbent bike | Precor 120 V/15 A; LF self-powered (C/X consoles); Matrix 7xe: AC, **up to 4 units daisy-chained per dedicated 15 A circuit** | Precor; LF; Matrix |
| stair_climber | 8Gx: 12 V/5 A power supply (adapter); PowerMill: 100–240 V, 5 A | Core; LF |
| recumbent_stepper | NuStep T5/T5XR 12 V battery; T6MAX AC adapter; StepOne self-generating + adapter | NuStep; LF |
| curved_treadmill, air_bike, rower, ski_erg, indoor_cycle | No mains power (self-powered / batteries) | Woodway, Assault, Concept2, LF |

## 6. Ceiling heights

StairMaster 8Gx/10G: 10 ft · LF PowerMill: 9 ft · StairMaster 4G: 8 ft · Jacobs Ladder: 7.5 ft · SkiErg unit: 85 in · rigs: 97–105 in tall (Rogue 9 ft uprights) · Sport England gyms: not below 2.7 m (8.9 ft), optimum 3.5–4 m.

---

## 7. Conflicts (and how they were resolved)

1. **Treadmill side clearance:** 19.7 in (ASTM/Precor/Cybex) vs 24 in (Matrix). Use **20 in**, shareable; 24 is the conservative option.
2. **Elliptical rear:** LF CLSX warns of a 2 m x 1 m rear zone; LF E1, Matrix and Precor say 0.5–0.6 m. Use **24 in**, with 79 as the strict-LF option.
3. **Bike front/rear:** LF warns 3 ft front-or-rear but its setup text says 1 ft front; Matrix 0.6 m. Use **front 12 / back 24**.
4. **Precor EFX 885 length:** 80 in (precor.com, fetched) vs 86 in (search snippet). The fetched value is used.
5. **AssaultBike Elite:** 55.08 x 26.26 x 55 / 138.9 lb (FAQ) vs 47.9 x 26.2 x 56 / 125 lb (spec table), both on assaultfitness.com. The larger set is used.
6. **TrueForm Runner:** width 31 in (Rogue) vs 36 in (Iron Co); capacity 700 lb (Rogue) vs 700 lb walking / 450 lb running (Iron Co).
7. **NuStep T5 weight:** 285 lb (product page) vs 298 lb (manual).
8. **LF Integrity recumbent:** 67 in printed with "179 cm" (the cm value is a typo). The CLSR manual's 52.75 in length is inconsistent and was not used.
9. **Throwdown freestanding bag weight** "117 lbS (18.9 kg)": the units disagree. Use as indicative only.
10. **Throwdown HIITMill X width** of 55 in is much wider than other curved treadmills (31–36 in), probably including the rails. The planning width stays 34 in.

## 8. Gaps

* **The shared WebSearch budget ran out partway through.** Remaining sources were reached by direct URL, so some items rest on one vendor family.
* No manufacturer **floor clearance** was found for **air bikes, stair climbers (StepMill/PowerMill), ski ergs, plyo boxes, battle ropes, suspension trainers, or wall-ball stations**. The values given are labelled estimates.
* Max user weight is missing for Woodway Curve (standard), Concept2 SkiErg, and Star Trac 10TRx/8CT/8UB/8RB.
* ASTM F2115-25 and ISO 20957-1/-6 are paywalled. Their clearance figures are taken from manuals that cite them, not from the standards' own text.
* Matrix's current product pages render with JavaScript and could not be read. Matrix data comes from Matrix owner's manuals (PDF) and one search snippet (`fetched=false`).
* The ACSM Health/Fitness Facility Standards and Guidelines (5th ed.) could not be accessed. Sport England's 2008 guidance note stands in as the design-guide source for per-user stretch area and per-machine circulation.
* Turf-lane run-out lengths and battle-rope/TRX zone widths are geometric derivations, not vendor numbers.

## 9. Machine-readable recommended values (inches)

```yaml
# footprint: [L, W]; clearance: [front, back, left, right]; shareable_sides: bool
treadmill:            {footprint: [84, 36], clearance: [12, 79, 20, 20], shareable_sides: true, power: dedicated_120v_20a}
curved_treadmill:     {footprint: [70, 34], clearance: [20, 79, 20, 20], shareable_sides: true, power: none}
elliptical:           {footprint: [84, 30], clearance: [12, 24, 24, 24], shareable_sides: true, power: 120v_15a_or_self}
upright_bike:         {footprint: [49, 26], clearance: [12, 24, 24, 24], shareable_sides: true, power: self_or_120v_15a_shared}
recumbent_bike:       {footprint: [67, 27], clearance: [12, 24, 24, 24], shareable_sides: true, power: self_or_120v_15a_shared}
indoor_cycle:         {footprint: [53, 23], clearance: [24, 24, 24, 24], shareable_sides: true, power: none}
air_bike:             {footprint: [55, 30], clearance: [24, 24, 24, 24], shareable_sides: true, power: none}
rower:                {footprint: [96, 26], clearance: [6, 6, 12, 12],   shareable_sides: true, power: none}
stair_climber:        {footprint: [61, 34], clearance: [12, 24, 24, 24], shareable_sides: true, power: low_voltage_adapter, min_ceiling_in: 120}
ski_erg:              {footprint: [50, 24], clearance: [12, 24, 12, 12], shareable_sides: true, power: none, min_ceiling_in: 96}
recumbent_stepper:    {footprint: [73, 30], clearance: [12, 12, 24, 30], shareable_sides: true, power: battery_or_adapter, ada_transfer_side: right}
rig_bay:              {footprint: [48, 48], clearance: [60, 60, 60, 60], end_clearance_only_lr: true, wall_mounted_back: 0, height_in: 105}
turf_lane:            {footprint: [600, 60], length_range: [300, 1080], clearance: [36, 36, 0, 0], other_equipment_side_gap: 24}
sled:                 {footprint: [52, 33], clearance: [12, 12, 12, 12]}
plyo_box_set:         {footprint: [36, 30], clearance: [48, 36, 24, 24]}
wall_ball_station:    {footprint: [26, 48], clearance: [60, 0, 12, 12], requires_wall_height_in: 120}
battle_rope_station:  {footprint: [204, 72], clearance: [0, 24, 12, 12], rope_ft: 30, footprint_50ft_rope: [324, 72]}
suspension_trainer_station: {footprint: [96, 72], clearance: [12, 12, 12, 12], anchor_height_in: [84, 108]}
heavy_bag:            {footprint: [24, 24], clearance: [45, 15, 15, 15], center_spacing_in: 54}
stretch_area:         {footprint: [72, 24], clearance: [4, 4, 12, 12], per_user_m2: [2.0, 2.5]}
accessory_pack:       {footprint: [25, 36], clearance: [25, 0, 0, 0]}
kettlebell_set:       {footprint: [24, 77], clearance: [36, 0, 0, 0]}
```

## 10. Sources (all fetched unless noted)

* Precor TRM 885 — https://www.precor.com/en-US/products/TRM885 ; brochure https://static.precor.com/sell-sheet/all/TRM/TRM885-Product-Brochure-ENG.pdf
* Precor EFX 885 — https://www.precor.com/en-US/products/EFX885 · UBK 885 — https://www.precor.com/en-US/products/UBK885 · RBK 885 — https://www.precor.com/en-US/products/RBK885
* Precor P30 console manual (spacing rules) — https://www.manualslib.com/manual/886465/Precor-P30.html?page=7
* Life Fitness Integrity treadmill — https://lifefitness.com/en-us/catalog/cardio/treadmills/integrity-series-treadmill ; Integrity+ — https://www.lifefitness.com/en-us/catalog/cardio/treadmills/integrity-plus ; Atmos — https://www.lifefitness.com/en-us/catalog/cardio/treadmills/atmos-treadmill
* LF AU sell sheets — Treadmill https://www.lifefitness.com.au/wp-content/uploads/2019/04/Integrity-Treadmill-Sellsheet-Update-vf.pdf ; Upright https://www.lifefitness.com.au/wp-content/uploads/2019/04/Integrity-Upright-Sellsheet-Update-vf.pdf ; Recumbent https://www.lifefitness.com.au/wp-content/uploads/2019/04/Integrity-Recumbent-Sellsheet-Update-vf.pdf
* LF Integrity elliptical — https://lifefitness.com/en-us/catalog/cardio/ellipticals/integrity-series-elliptical-cross-trainer
* LF Integrity CLSX cross-trainer manual — https://cdn.shopify.com/s/files/1/2063/2201/files/Life_Fitness_Integrity_Series_Cross-Trainer_CLSX_Operation_Manual.pdf
* LF E1 cross-trainer assembly manual — https://kb.cybexintl.com/Assembly_Manuals/Cross_Trainer/AI_CT_E1_Cross_Trainer_Assembly_Manual_M051-00K102-0007.pdf
* LF Integrity CLSR recumbent manual — https://keystonefitness.ca/wp-content/uploads/2023/05/Life-Fitness-Integrity-Series-Recumbent-Lifecycle-Exercise-Bike-CLSR-Operation-Manual.pdf
* LF IC7 manual — https://cdn.shopify.com/s/files/1/0134/3275/0138/files/IC-LFIC7B2_EN-WEB.pdf
* LF PowerMill — https://www.lifefitness.com/en-us/catalog/cardio/stair-climbers-stepper-machines/powermill-climber ; SciFit StepOne — https://www.lifefitness.com/en-us/catalog/cardio/stair-climbers-stepper-machines/stepone-recumbent-stepper ; Row HX — https://www.lifefitness.com/en-us/catalog/cardio/rowers/row-hx-trainer
* LF storage — https://www.lifefitness.com/en-us/catalog/strength-training/storage-racks/life-fitness-accessory-storage-rack ; https://www.lifefitness.com/en-us/catalog/strength-training/storage-racks/synrgy-accessory-storage-system ; https://www.lifefitness.com/en-us/catalog/strength-training/storage-racks/life-fitness-vertical-medicine-ball-storage
* Hammer Strength HD Perimeter — https://www.lifefitness.com/en-us/catalog/strength-training/racks-rigs-platforms/hd-athletic-pro-perimeter
* Core Health & Fitness 2026 Catalog (Star Trac, StairMaster, Schwinn, Throwdown) — https://embed.pickit.com/files/xi8xbjjtay0uabg/67d365cc39f321090cac7d59/Core%202026%20Catalog.pdf (linked from https://corehandf.com/product-brand/stairmaster/)
* StairMaster 8Gx — https://corehandf.com/products/stairmaster-8gx-1 ; Star Trac 8TRx — https://corehandf.com/products/8trx-treadmill-copy
* Matrix T3xe owner's manual — https://www.manualslib.com/manual/1061544/Matrix-T3xe.html?page=10
* Matrix Performance cycles manual — https://cdn.shopify.com/s/files/1/2063/2201/files/matrix_performance_upright_cycle_manual.pdf
* Matrix Premium cycles manual (R7xe/U7xe/H7xe) — https://fleetfitness.com.au/assets/product/Matrix-R7xe-EP92-Owners-Manual.pdf
* Matrix elliptical manual (24-in rule) — https://manualmachine.com/matrix/e5xc/20856185-instructions-manual (`fetched=false`, 403; quote via search snippet)
* Matrix Performance treadmill — https://us.matrixfitness.com/eng/cardio/performance/treadmill (`fetched=false`, JS page; figures via search snippet)
* Cybex 525T manual — https://www.manualsdir.com/manuals/762629/cybex-525t-treadmill.html?page=13
* Assault AirRunner manual — https://hefitness.se/produktfiler/airrunner.pdf ; AssaultBike Elite — https://www.assaultfitness.com/bikes/assault-bike-elite/
* Woodway Curve — https://www.woodway.com/products/curve/ ; Curve LTG — https://www.roguefitness.com/the-rogue-woodway-curve-ltg-treadmill
* TrueForm Runner — https://www.roguefitness.com/trueform-runner ; https://www.ironcompany.com/trueform-runner-non-motorized-curved-treadmill
* Keiser M3i manual — https://cdn.shopify.com/s/files/1/0092/7373/7295/files/keiser-m3i-user-manual.pdf
* Concept2 RowErg — https://www.concept2.com/ergs/rowerg ; SkiErg — https://www.concept2.com/ergs/skierg ; BikeErg — https://www.concept2.com/bikeerg
* Rogue Echo Bike — https://www.roguefitness.com/rogue-echo-bike
* NuStep T5 / T5XR / T6MAX — https://www.nustep.com/product/t5/ , https://www.nustep.com/product/t5xr/ , https://www.nustep.com/product/t6max/ ; manuals https://www.nustep.com/wp-content/uploads/2023/08/50274-T5-User-Manual-English-Rev-N.pdf , https://www.nustep.com/wp-content/uploads/2023/08/52390-T6-User-Manual-English-Rev-E.pdf
* ADA 2010 Standards — https://www.access-board.gov/files/ada/ADA-Standards.pdf
* Sport England, Fitness and Exercise Spaces (2008) — https://sportengland-production-files.s3.eu-west-2.amazonaws.com/s3fs-public/fitness-and-exercise-spaces.pdf?VersionId=BitV0h3FgG.ImxmuPWLc3iSKiCsosrDc
* Rogue GymTurf — https://www.roguefitness.com/gymturf ; TANK M4 — https://www.roguefitness.com/torque-fitness-tank-m4-sled ; TANK M1S — https://www.roguefitness.com/torque-fitness-tank-m1s-push-sled ; Echo Dog Sled — https://www.roguefitness.com/rogue-echo-dog-sled
* Torque TANK FAQ — https://torquefitness.com/pages/tank-faq
* Rogue Foam Plyo Boxes — https://www.roguefitness.com/rogue-foam-plyoboxes ; Games Box — https://www.roguefitness.com/rogue-games-box
* Rogue Medicine Balls — https://www.roguefitness.com/rogue-medicine-balls ; Wall Ball Target — https://www.roguefitness.com/bolt-together-wall-ball-target-for-infinity-monster-lite
* Rogue Battle Rope — https://www.roguefitness.com/rogue-battle-rope ; TRX Battle Rope — https://commercial.trxtraining.com/products/trx-battle-rope-commercial-partners
* TRX Suspension Anchor — https://www.trxtraining.com/products/suspension-anchor ; Xtender — https://www.trxtraining.com/products/xtender ; XMount — https://www.trxtraining.com/products/xmount
* Rogue Monkey Rig 2.0 — https://www.roguefitness.com/rogue-monster-lite-monkey-rig-2-0 ; V2 Castro Rig — https://www.roguefitness.com/rogue-v2-castro-rig-10755 ; W-4 — https://www.roguefitness.com/rogue-w-4-4-wall-mount-rig
* Rogue USS 2.0 — https://www.roguefitness.com/rogue-universal-storage-system-2-0 ; Mass Storage — https://www.roguefitness.com/custom-mass-storage
* ASTM F2115-25 listing — https://store.astm.org/f2115-25.html (`fetched=false`) ; ISO 20957-1:2024 — https://www.iso.org/standard/81908.html (`fetched=false`)
