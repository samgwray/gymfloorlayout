# Footprints & clearances - strength equipment (racks, free weights, machines, cables)

_Research slice: `footprint_strength`. Compiled 2026-10-28. All inches unless stated. Every model dimension below is copied from the cited manufacturer/dealer spec; every recommended value is an explicitly derived estimate with its derivation shown._

## 1. Conventions used in this file (read first)

- **L (length)** = front-to-back dimension, measured along the line the user faces / walks out / reaches in (for benches: along the bench; for racks and Smith machines: depth; for storage racks: depth). **W (width)** = side-to-side (for racks, benches with uprights and Smith machines W is the bar axis). Where a publisher lists the axes the other way round, the value was re-oriented and the note says so.
- **Footprint** = the at-rest frame (published 'Dimensions', 'Size' or 'Footprint').
- **Live area** = the manufacturer's *recommended live area / training space* (Life Fitness, Hammer Strength, Axiom and Signature use this term). Cybex instead publishes *machine dimensions in use* (moving parts at full travel), which is reported separately and not mixed into live-area statistics.
- **ISO 20957-1 terms**: *training area* = 'area occupied by the user and the equipment while exercising over the full range of movement'; *free area* = 'area in addition to the training area which is required for the user or third party to access the equipment and/or conduct an emergency dismount' (ISO 20957-1:2013, 3.2 and 3.4).
- **Recommended clearance (front/back/left/right)** = an *exclusive* margin beyond the footprint. Facing margins of two neighbours **add** (sum rule): the frame-to-frame gap between A and B on facing sides = clearance_A + clearance_B. Default side margins (12 in) are calibrated so two default neighbours sit 24 in apart (the NSCA minimum, the ISO 0.6 m free area, Star Trac's 24 in and Cybex's 23.6 in). Barbell-station side margins include the loaded-bar overhang, so two adjacent stations leave about 36 in between bar ends (NSCA). **Back = 0** marks wall-type storage meant to stand against a wall.

**Suggested engine rules (derived from the sources in section 2):**
1. Footprint + clearance rectangles must not overlap each other, walls (except 0-margin sides) or columns.
2. Use a minimum 24 in between any two frames (NSCA minimum; ISO 0.6 m free area; Cybex 23.6 in; Matrix 24 in; Star Trac 24 in). For large gyms use the **36 in preferred** spacing (NSCA 'optimal'): add +6 in to every side margin that faces another unit.
3. Keep the main circulation aisles at 36 in or wider (NSCA passageways 36 in; ADA 403.5.1 accessible route 36 in; Star Trac 36 in walkway on the entry side) and corridors at 60 in (NSCA TSAC hallways). Clearance rectangles may adjoin aisles but should not be counted as aisle width.
4. Leave 36 in between the ends of loaded Olympic bars (NSCA checklist). This is built into the barbell-station side margins below.
5. ADA: at least one of each type of machine needs a 30 x 48 in clear floor space beside it, adjoining an accessible route (36 x 48 in if enclosed on three sides, per the Cybex manual's ADA note). Clear floor spaces may overlap each other and may lie inside a unit's clearance margins (ADA 1004.1 advisory). Practical encoding: for one unit of each type, enlarge one side margin to 30 in or wider along a 48 in length.
6. Overhead: 12 ft clear ceiling for overhead lifting areas (NSCA checklist); rack, tower and pull-up items need about 96-110 in of clear height (section 4).
7. Structured-output ids: `<item>.footprint_in` holds 'L x W' and `<item>.clearance_in` holds 'front/back/left/right' (in); global rules use the `nsca.*`, `iso20957.*`, `ada.*`, `layout_rule.*` and `liveArea.*` ids.

## 2. Standards and published spacing guidance (verbatim evidence)

| ID | Source | Guidance (verbatim or precise pointer) |
|---|---|---|
| `iso20957_1_2013` | [ISO 20957-1:2013 §3.2 / §3.4](https://cdn.standards.iteh.ai/samples/56102/b0f72c8378484be29dc5ec9548ce4943/ISO-20957-1-2013.pdf) | 3.2 training area: 'area occupied by the user and the equipment while exercising over the full range of movement'. 3.4 free area: 'area in addition to the training area which is required for the user or third party to access the equipment and/or conduct an emergency dismount over and above the full range of movement'. (Edition 2013 withdrawn and replaced by ISO 20957-1:2024; numeric free-area clause not in the free preview.) |
| `kingsbox_manual` | [Manufacturer manual quoting EN ISO 20957-1:2013](https://www.manualslib.com/manual/2565908/Kingsbox-Foldable-Flat-Bench.html) | 'The free area shall not be less than 0,6 m greater than the training area' 'in the directions from which the equipment is accessed.' 'The free area must also include the area for emergency dismount.' (p.4). Italian text p.19: free area 'di almeno 0,6m tutt'attorno' and 'Nel caso di più attrezzi posizionati uno accanto all'altro, questi possono condividere l'area libera' (side-by-side units may share the free area). |
| `cybex_20040` | [Cybex Eagle NX owner's manuals (all models)](https://kb.cybexintl.com/Owners_Manuals/Strength/20040-999-4.pdf) | 'Free area for access to unit and emergency dismount. Minimum clearance is 23.6 inches (0.6 meters).' 'Adjacent units may share the free area.' 'All other machines must have a clear floor space of 23" for all access point on the machine, unless shown in the Owner's Manual.' ADA note: 'clear floor space of at least 30 by 48 inches ... If the clear space is enclosed on three sides ... 36 by 48 inches.' |
| `matrix_mabr1` | [Matrix MABR1 bench manual (Rev 1.1, 2023)](https://cdn.shopify.com/s/files/1/0554/8795/5111/files/Bench_Manual.pdf) | 'Ensure a minimum clearance width of 0.6 meters (24") for access to and passage around Matrix strength equipment. Please note, 0.91 meters (36") is the ADA recommended clearance width for individuals in wheelchairs.' Diagram: TRAINING AREA 1.42 m (56") x 0.78 m (30.5") = bench footprint; 'FREE AREA 0.6 M (2 FT) WIDE PATH'. |
| `startrac_ipl5002` | [Star Trac IP-L5002 manual p.19](https://videogame.manualsonline.com/manuals/mfg/star_trac/ipl5002.html?p=19) | 'a clearance of 24 inches (60.96cm) be maintained between and behind machines including moving arms and levers.' 'a walkway of at least 36 inches (91.44cm) ... is recommended front of, or on the entry side of each machine.' |
| `nsca_checklist` | [NSCA Safety Checklist](https://www.nsca.com/contentassets/2a0a87ccabbe4a149dd915168b20d603/nsca-safety-checklist.pdf) | Machine area: 'Easy access to each station (a minimum of 2 feet [61 cm] between machines; 3 feet [91 cm] is optimal)'. Free-weight area: 'Olympic bars properly spaced (3 feet [91 cm]) between ends'. 'Ceiling height sufficient for overhead exercises (12 feet [3.7 m] minimum)'. 'Mirrors placed a minimum of 20 inches [51 cm] off the floor'. |
| `nsca_standards_2017` | [NSCA Standards & Guidelines 2017, Appendix 4 Table D1](https://www.nsca.com/globalassets/education/nsca_strength_and_conditioning_professional_standards_and_guidelines.pdf) | Prone/supine: '(6 ft + 3 ft) x (7 ft + 3 ft) = 90 ft2'. Standing: '(4 ft + 6 ft) x (4 ft) = 40 ft2'. Standing in a rack: '(7 ft + 6 ft) x (10 ft) = 130 ft2' (rack width term 8-10 ft). Olympic lifting: '(8 ft + 4 ft) x (8 ft + 4 ft) = 144 ft2'. Note: combined platform/rack stations 'should be combined'. Guideline 3.1: 'minimum average floor space allowance per participant (100 ft2)'; 'number of participants per barbell or training station (up to 3)'. |
| `nsca_tsac` | [NSCA TSAC Module 5.0 (2018)](https://www.nsca.com/contentassets/4bc4e495944c470d81c429294a2b4c05/tsac-module-5.0--5.1.pdf) | 'Ceiling height 12-14 ft of clearance'; 'Mirrors 20 in. from floor, 6 in. from equipment'; 'Passageways 36 in.'; 'Hallways 60 in.'; 'Tallest equipment and dumbbell racks - Placed along walls'; bench example '(6 + 3 + 3) x (7 + 3 + 3) = 156 ft2' (3 ft safety space each side). |
| `ada_2010` | [2010 ADA Standards](https://www.access-board.gov/ada/) | 236.1: 'At least one of each type of exercise machine and equipment shall comply with 1004.' 206.2.13: such equipment 'shall be on an accessible route'. 1004.1: 'clear floor space complying with 305 positioned for transfer or for use by an individual seated in a wheelchair. Clear floor or ground spaces required at exercise machines and equipment shall be permitted to overlap.' 305.3: '30 inches (760 mm) minimum by 48 inches (1220 mm) minimum'. 403.5.1: accessible route clear width '36 inches (915 mm) minimum'. |

**Interpretation and conflicts.** ISO and the Cybex manuals require a 0.6 m (23.6 in) free area on access sides that neighbours may share; NSCA gives 24 in minimum and 36 in optimal between machines. Under the sum rule a 12 in exclusive margin per side meets the 24 in minimum. NSCA's area formulas are more generous than manufacturer live areas for barbell work: 130 ft2 per rack station (13 ft wide) against 100 ft2 (10 x 10 ft) in the LF and HS live areas. The 156 ft2 TSAC bench example also differs from the 90 ft2 in the 2017 Standards table, because TSAC adds 3 ft on *each* side. The model uses the manufacturer live areas plus NSCA's 36 in between bar ends, and keeps the NSCA formulas as the high bound.

## 3. Barbell and plate-loading geometry

- Olympic men's bar: **86.75 in** overall ('Exact length is 86.75"'), loadable sleeve **16.40 in**, 28.5 mm shaft, 20 kg ([Rogue Ohio Bar](https://www.roguefitness.com/the-ohio-bar-black-zinc)). This is the 7.2 ft (2.2 m) bar the task refers to. Rack frames are about 48-73 in wide, so a loaded bar overhangs each upright by roughly 7-19 in.
- The LF and HS live areas for every barbell station (Olympic flat, incline and decline benches, Olympic squat rack, Smith, NX/iD power racks) are **120 in wide**. That leaves (120 - 86.75)/2 = 16.6 in beyond each bar end, so two adjoining live areas give about 33 in between bar ends, close to NSCA's 36 in.
- Plate-loaded machines: HS live areas add **+48 in of width** (24 in per side) on the Iso-Lateral Bench Press, Iso-Lateral Chest/Back, Iso-Lateral Front Lat Pulldown and Belt Squat, so plates can be loaded at the horns. The exceptions are the Linear Leg Press (+24 in) and the Glute Drive (+0 in).
- Dumbbell racks: the LF and HS 2- and 3-tier live areas add **+36 in in front** and 0 at the ends and back (LF 3-tier saddle: +24 in).

## 4. Derived statistics: how much bigger than the frame is the space actually needed?

Across **103 manufacturer live-area/footprint pairs** (LF Insignia, Axiom and Signature FZ; HS Select, MTS, plate-loaded, benches and racks; NSCA formula rows), the live area is a median **2.10x** the footprint area (IQR 1.76-2.80). The median addition is **+24 in of length** and **+24 in of width**. (Derived estimate: computed over the section 5 rows that list both a footprint and a manufacturer live area. Cybex in-use rows are excluded.)

| Family | n | median live/footprint area | median +L (range) | median +W (range) |
|---|---|---|---|---|
| Selectorized single-station | 63 | 1.88x | 24 (0-54) | 18 (0-51) |
| Barbell stations (racks, Olympic benches, Smith) | 13 | 3.40x | 42 (24-71) | 55 (33-69) |
| Benches & bodyweight (FID, flat, preacher, hyper, GHD, VKR) | 10 | 3.80x | 36 (24-56) | 40 (0-48) |
| Storage (dumbbell & barbell racks) | 6 | 2.39x | 36 (24-46) | 0 (0-26) |
| Plate-loaded (incl. MTS twins) | 10 | 1.86x | 24 (12-36) | 18 (0-48) |

Cybex *in-use* extensions (moving parts at full travel beyond the at-rest frame): seated leg press +32 in L, Eagle hip ab/adduction +18 L/+30 W, glute +12 to +22 L, leg extension +12 L, chest press +8 L, torso +5-6 W; most other Eagle NX units 0. These moving-part extensions fit inside the recommended front margins.

Heights and overhead envelopes: LF Insignia live areas are 82.7 in (210 cm) high, except the Assist Dip Chin at 105 in (frame 87 in); HS Chin/Dip/Leg Raise live height is 110 in; HS HD Elite iD racks are 96 in; Rogue racks are 90.4 in (92.25 in HR-2); HS Select Lat Pulldown is 89 in; Cybex VR3 Lat Pull is 90 in; Smith machines are 88-93 in.

## 5. Per-item data: representative commercial models and recommended model values

### `power_rack` - Power rack (full rack)

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Rogue | RML-490 Power Rack | 53 | 53 | 90.4 | - | [rogue_rml490](https://www.roguefitness.com/rogue-rml-490-power-rack) | Gear Specs: L 49 x W 49; 'Foot Print 53" x 53"' (used) |
| Rogue | R-3 Power Rack (30in depth) | 40 | 53 | 90.4 | - | [rogue_r3](https://www.roguefitness.com/rogue-r-3-power-rack) | 'Foot Print 34" or 40" x 53"'; width 43" |
| Hammer Strength | HD Athletic NX Power Rack | 62 | 65 | 91 | 120 x 120 | [lfshop_hs_nx_power](https://shop.lifefitness.com/products/hammer-strength-hd-athletic-nx-power-rack) | Depth 62/Width 65/Height 91; 'Live Area: 10' x 10'' |
| Hammer Strength | HD Elite iD Power Rack | 64 | 73 | 96 | 120 x 120 | [lfcom_hd_elite_power](https://www.lifefitness.com/en-us/catalog/strength-training/racks-rigs-platforms/hd-elite-id-power-rack) | '64" x 73" x 96"'; 'Live area: 10' x 10'' |

**Recommended model value:** footprint **58 x 59 in** (L x W); clearance **front 48 / back 12 / left 32 / right 32 in**. Exclusive envelope = 118 x 123 in = 100.8 ft2 (frame 23.8 ft2). Confidence: medium.  
_Derivation:_ Frame = median of Rogue RML-490 (53x53), R-3 (40x53), HS HD Athletic NX (62x65), HS HD Elite iD (64x73). Depth margins from LF/HS 'Live Area 10x10 ft' (120 in) -> 62 in split 48 front (walk-out, plate loading, spotter) / 12 back. Sides = bar overhang (86.75-59)/2 = 14 + 18 beyond each bar end -> 36 in between neighbouring bar ends (NSCA checklist). Total ~123 x 118 in vs LF/HS 120 x 120. NSCA rack formula (7+6 ft) x 10 ft = 156 x 120 in is a conservative upper bound.

### `half_rack` - Half rack / squat rack

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Rogue | HR-2 Half Rack | 49 | 48 | 92.25 | - | [rogue_hr2](https://www.roguefitness.com/rogue-hr-2-half-rack) | 'Foot Print 48" x 49"' |
| Hammer Strength | HD Athletic NX Half Rack | 50 | 48 | 86 | - | [lfshop_hs_nx_half](https://shop.lifefitness.com/products/hammer-strength-hd-athletic-nx-half-rack) | 'Dimensions (D x W x H): 50" x 48" x 86"' |
| Hammer Strength | HD Elite iD Half Rack | 56 | 73 | 96 | 84 x 120 | [lfshop_hs_id_half](https://shop.lifefitness.com/products/hammer-strength-hd-elite-id-half-rack) | '56" x 73" x 96"'; 'Live Area: 7' x 10''; storage depth 21" included |
| Hammer Strength | Olympic Squat Rack OSR | 59 | 69 | 73 | - | [hs_catalog_2024](https://cdn.shopify.com/s/files/1/0573/6877/2685/files/ISBU_Hammer-Strength-Catalog-2024-ENGLISH.pdf) | catalog L x W x H |
| Life Fitness | Signature Olympic Squat Rack | 77.5 | 66 | 75.5 | 120 x 120 | [lfcom_lf_squat_rack](https://www.lifefitness.com/en-us/catalog/strength-training/benches/life-fitness-olympic-squat-rack) | Footprint 77.5 x 66 x 75.5; live 120 x 120 |
| BodyKore | G701 Half Rack | 64 | 51 | 94 | - | [bk_g701](https://www.recoveryforathletes.com/products/g701-half-rack) | dealer listing 64x51x94 (axis order not labeled) |

**Recommended model value:** footprint **53 x 50 in** (L x W); clearance **front 36 / back 6 / left 36 / right 36 in**. Exclusive envelope = 95 x 122 in = 80.5 ft2 (frame 18.4 ft2). Confidence: medium.  
_Derivation:_ Frame = median of Rogue HR-2 (49x48), HS NX half (50x48), HS iD half (56x73), BodyKore G701 (64x51). Front 36: lifter walks bar out in front of uprights (HS iD live area 7x10 ft -> +28 in depth; LF Signature squat rack +42.5). Sides = (86.75-50)/2 = 18 overhang + 18 beyond bar end = 36.

### `lifting_platform` - Lifting platform (8x8)

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Hammer Strength | Traditional Wood Platform TWP-6X8 | 94.5 | 75.5 | 3.25 | - | [hs_catalog_2024](https://cdn.shopify.com/s/files/1/0573/6877/2685/files/ISBU_Hammer-Strength-Catalog-2024-ENGLISH.pdf) | 6x8 ft platform; 2 inserts flank a rack |
| Hammer Strength | Rubber Platform RPI-6X8 | 92 | 72 | 0.75 | - | [hs_catalog_2024](https://cdn.shopify.com/s/files/1/0573/6877/2685/files/ISBU_Hammer-Strength-Catalog-2024-ENGLISH.pdf) | rubber 6x8 |
| NSCA | Typical lifting platform (guideline) | 96 | 96 | - | 144 x 144 | [nsca_standards_2017](https://www.nsca.com/globalassets/education/nsca_strength_and_conditioning_professional_standards_and_guidelines.pdf) | 'Lifting platform length (typically 8 ft) ... width (typically 8 ft)'; (8+4)x(8+4)=144 ft2 |

**Recommended model value:** footprint **96 x 96 in** (L x W); clearance **front 24 / back 24 / left 24 / right 24 in**. Exclusive envelope = 144 x 144 in = 144.0 ft2 (frame 64.0 ft2). Confidence: medium.  
_Derivation:_ NSCA: platform typically 8 x 8 ft + 4 ft perimeter walkway cushion per dimension -> (8+4)x(8+4)=144 ft2, i.e. 24 in each side if centred. Matches ISO 20957-1 free area 0.6 m. Bar (86.75 in) fits inside the 96 in platform.

### `bench_press_station` - Olympic flat bench (bench press station)

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Signature Olympic Flat Bench | 49 | 51 | 51 | 91 x 120 | [lfshop_lf_oly_flat](https://shop.lifefitness.com/products/signature-series-olympic-flat-bench) | live 91 x 120 x 51 |
| Hammer Strength | Olympic Flat Bench | 51 | 52 | 51 | 75 x 120 | [lfcom_hs_oly_flat](https://www.lifefitness.com/en-us/catalog/strength-training/benches/olympic-flat-bench) | D x W x H 51x52x51; live 75 x 120 |
| Cybex | Free Weight Olympic Bench Press 16010 | 60 | 53 | 51 | - | [cybex_16010](https://kb.cybexintl.com/Owners_Manuals/Strength/16010-999-4.pdf) | 60 L x 53 W x 51 H |
| Rogue | Westside Bench 2.0 | 52.5 | 34 | 54.6 | - | [rogue_westside](https://www.roguefitness.com/rogue-westside-bench-2-0) | 'Foot Print 52.5" x 34"' (rack uprights narrower than commercial) |
| NSCA | Bench press formula (6 ft bench) | - | - | - | 108 x 120 | [nsca_standards_2017](https://www.nsca.com/globalassets/education/nsca_strength_and_conditioning_professional_standards_and_guidelines.pdf) | (6+3) ft x (7+3) ft = 90 ft2 |

**Recommended model value:** footprint **52 x 52 in** (L x W); clearance **front 18 / back 24 / left 36 / right 36 in**. Exclusive envelope = 94 x 124 in = 80.9 ft2 (frame 18.8 ft2). Confidence: medium.  
_Derivation:_ Frame = median of LF Signature (49x51), HS (51x52), Cybex 16010 (60x53), Rogue Westside (52.5x34). Depth margin = median(LF +42, HS +24, NSCA formula +56) = 42 -> 18 foot end + 24 head/spotter end. Width: LF & HS live area and NSCA formula all = 120 in; sides = (86.75-52)/2 + 18 = 35.5 -> 36.

### `incline_bench_station` - Olympic incline bench

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Signature Olympic Incline Bench | 58 | 51 | 57 | 101 x 120 | [lfcom_lf_oly_incline](https://www.lifefitness.com/en-us/catalog/strength-training/benches/life-fitness-olympic-incline-bench) | lifefitness.com 58x51x57; live 101 x 120 (shop page lists 86x68x57 - treated as error) |
| Hammer Strength | Olympic Incline Bench | 59 | 52 | 59 | 95 x 120 | [lfcom_hs_oly_incline](https://www.lifefitness.com/en-us/catalog/strength-training/benches/olympic-incline-bench) | D x W x H; live 95 x 120 (catalog OIB 51x52x58) |

**Recommended model value:** footprint **59 x 52 in** (L x W); clearance **front 18 / back 24 / left 36 / right 36 in**. Exclusive envelope = 101 x 124 in = 87.0 ft2 (frame 21.3 ft2). Confidence: medium.  
_Derivation:_ Frame = LF Signature (58x51), HS (59x52). Depth margin LF +43 / HS +36 -> 18 front + 24 back (spotter). Width 120 in live area (LF, HS) -> sides 36 incl. bar overhang.

### `decline_bench_station` - Olympic decline bench

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Signature Olympic Decline Bench | 68 | 51 | 51 | 110 x 120 | [lfcom_lf_oly_decline](https://www.lifefitness.com/en-us/catalog/strength-training/benches/life-fitness-olympic-decline-bench) | live 110 x 120 |
| Hammer Strength | Olympic Decline Bench | 70 | 52 | 51 | 94 x 120 | [lfcom_hs_oly_decline](https://www.lifefitness.com/en-us/catalog/strength-training/benches/olympic-decline-bench) | D x W x H; live 94 x 120 (catalog O-DB 60x53x50) |
| Cybex | Free Weight Olympic Decline Press 16060 | 73 | 53 | 47 | - | [cybex_16060](https://kb.cybexintl.com/Owners_Manuals/Strength/16060-999-4.pdf) | 53 W x 73 L x 47 H |

**Recommended model value:** footprint **70 x 52 in** (L x W); clearance **front 18 / back 18 / left 36 / right 36 in**. Exclusive envelope = 106 x 124 in = 91.3 ft2 (frame 25.3 ft2). Confidence: medium.  
_Derivation:_ Frame = median LF (68x51), HS (70x52), Cybex 16060 (73x53). Depth margin LF +42 / HS +24 -> 18/18. Width 120 in live area -> sides 36.

### `smith_machine` - Smith machine

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Signature Smith Machine | 49 | 87 | 93 | 120 x 120 | [lfshop_lf_smith](https://shop.lifefitness.com/products/life-fitness-smith-machine) | published 87 x 49 x 93 (L x W) - re-oriented: bar axis = W; live 120 x 120 |
| Hammer Strength | Smith Machine | 49 | 86.5 | 92.8 | 120 x 120 | [lfshop_hs_smith](https://shop.lifefitness.com/products/hammer-strength-smith-machine-1) | 49 x 86.5 x 92.8; live 120 x 120 |
| Hammer Strength | Plate-Loaded Vertical Smith | 49.63 | 90.15 | 92 | - | [lfshop_hs_vsmith](https://shop.lifefitness.com/products/hammer-strength-plate-loaded-vertical-smith-machine) | 49.63 x 90.15 x 92 |
| Life Fitness | Axiom Smith Rack | 56 | 73 | 88 | 120 x 120 | [lfshop_axiom_smith](https://shop.lifefitness.com/products/axiom-series-smith-rack) | 56 x 73 x 88; live 120 x 120 (L x W) |
| BodyKore | G271 Smith Machine | 52 | 94 | 93 | - | [bk_g271](https://www.recoveryforathletes.com/products/g271-smith-machine) | listing 94x52x93 - re-oriented (bar axis = W) |

**Recommended model value:** footprint **50 x 87 in** (L x W); clearance **front 48 / back 24 / left 18 / right 18 in**. Exclusive envelope = 122 x 123 in = 104.2 ft2 (frame 30.2 ft2). Confidence: medium.  
_Derivation:_ Frame = median LF (49x87), HS (49x86.5), HS vertical (49.6x90.2), Axiom smith rack (56x73), BodyKore G271 (52x94); W is the bar axis. LF, HS and Axiom all publish a 120 x 120 in live area -> depth +70 split 48 front (bench/walk-in) / 24 back; sides (120-87)/2 = 16.5 -> 18.

### `dumbbell_rack_2tier_10pair` - Dumbbell rack, 2-tier 10-pair

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Two-Tier Dumbbell Rack (10 pairs) | 25 | 90 | 33 | 61 x 90 | [lfshop_lf_2tier](https://shop.lifefitness.com/products/life-fitness-two-tier-dumbbell-rack) | published 90 x 25 x 33; live 90 x 61; 'Accommodates 10 pairs' |
| Hammer Strength | Two-Tier Dumbbell Rack FW-DR2 (10 pairs) | 21 | 90 | 33 | 57 x 90 | [lfshop_hs_2tier](https://shop.lifefitness.com/products/hammer-strength-two-tier-dumbbell-rack) | published 21 x 90 x 33; live 57 x 90; catalog 90x24x32 |
| REP Fitness | Victory 2-Tier Dumbbell Rack (10 pairs) | 24 | 84 | 29.5 | - | [rep_victory_2tier](https://repfitness.com/products/victory-2-tier-dumbbell-rack) | Length 84, Depth 24, Height 29.5 |
| REP Fitness | Commercial Dumbbell Rack 2-tier saddle (5-50) | 23.33 | 84.24 | 31.76 | - | [rep_commercial_dbr](https://repfitness.com/products/commercial-dumbbell-rack) | 5-50 lb set on single 2-tier |

**Recommended model value:** footprint **24 x 87 in** (L x W); clearance **front 36 / back 0 / left 0 / right 0 in**. Exclusive envelope = 60 x 87 in = 36.2 ft2 (frame 14.5 ft2). Confidence: high.  
_Derivation:_ Rack = median LF two-tier (25x90, 10 pairs), HS FW-DR2 (21x90, 10 pairs), REP Victory (24x84, 10 pairs), REP commercial saddle (23.3x84.2). LF & HS live areas both add exactly 36 in in front and 0 at ends; racks belong against walls (NSCA TSAC).

### `dumbbell_rack_3tier` - Dumbbell rack, 3-tier (15-pair)

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Hammer Strength | Three-Tier Dumbbell Rack (15 pairs) | 27 | 90 | 39 | 63 x 90 | [lfshop_hs_3tier](https://shop.lifefitness.com/products/hammer-strength-three-tier-dumbbell-rack) | 27 x 90 x 39; live 63 x 90; 'Stores 15 pairs' |
| Life Fitness | 3-Tier Long Saddle Rack 5-75 (15 pairs) | 29 | 96 | 38 | 53 x 97 | [lfshop_lf_3tier_long](https://shop.lifefitness.com/products/life-fitness-3-tier-long-saddle-dumbbell-rack-5-75) | 96 x 29 x 38; live 97 x 53 |
| Rogue | 3-Tier Dumbbell Rack (15 pairs) | 30 | 93 | 33 | - | [rogue_3tier_dbr](https://www.roguefitness.com/rogue-3-tier-dumbbell-rack) | 93 L x 30 W x 33 H; 15 pairs |
| REP Fitness | Commercial Dumbbell Rack 3-tier (5-95) | 26.15 | 84.24 | 34.28 | - | [rep_commercial_dbr](https://repfitness.com/products/commercial-dumbbell-rack) | 5-95 lb set on single 3-tier (19 pairs) |

**Recommended model value:** footprint **28 x 92 in** (L x W); clearance **front 30 / back 0 / left 0 / right 0 in**. Exclusive envelope = 58 x 92 in = 37.1 ft2 (frame 17.9 ft2). Confidence: medium.  
_Derivation:_ Rack = median HS three-tier (27x90, 15 pairs), LF 3-tier long saddle (29x96, 15 pairs 5-75), Rogue 3-tier (30x93, 15 pairs), REP commercial 3-tier (26.2x84.2). Front = median of HS +36 / LF +24 = 30.

### `dumbbell_rack_horizontal_15pair` - Dumbbell rack, horizontal 15-pair

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| REP Fitness | Commercial Dumbbell Rack 2-tier shelf (5-70, 14 pairs) | 23.33 | 84.24 | 31.52 | - | [rep_commercial_dbr](https://repfitness.com/products/commercial-dumbbell-rack) | 5-70 lb set on single 2-tier |
| Life Fitness | 3-Tier Short Saddle 5-50 (10 pairs) | 29 | 61 | 38 | 53 x 61 | [lfshop_lf_3tier_short](https://shop.lifefitness.com/products/life-fitness-3-tier-short-saddle-dumbbell-rack-5-50) | 61 x 29 x 38; live 61 x 53 (reference) |

**Recommended model value:** footprint **24 x 90 in** (L x W); clearance **front 36 / back 0 / left 0 / right 0 in**. Exclusive envelope = 60 x 90 in = 37.5 ft2 (frame 15.0 ft2). Confidence: low.  
_Derivation:_ ESTIMATE. No published 15-pair 2-tier commercial rack found. REP commercial 2-tier shelf rack holds a 5-70 lb set (14 pairs) in 84.24 x 23.33 in; adding one pair -> ~90 in. Front 36 per LF/HS 2-tier live areas.

### `adjustable_bench` - Adjustable (FID) bench

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Adjustable Bench | 55 | 25 | 45 | 97 x 73 | [lfshop_lf_adj_bench](https://shop.lifefitness.com/products/life-fitness-adjustable-bench) | Footprint (D x W x H) 55 x 25 x 45; live 97 x 73 |
| Life Fitness | Multi-Adjustable Bench | 58 | 29 | 17 | - | [lfshop_lf_mab](https://shop.lifefitness.com/products/life-fitness-multi-adjustable-bench) | 58 x 29 x 17 |
| Hammer Strength | Multi-Adjustable Bench | 54 | 27 | 18 | - | [lfshop_hs_mab](https://shop.lifefitness.com/products/hammer-strength-multi-adjustable-bench) | 54 x 27 x 18 |
| Rogue | Adjustable Bench 3.0 | 56.5 | 24.75 | 17.5 | - | [rogue_ab3](https://www.roguefitness.com/rogue-adjustable-bench-3-0) | '24.75" Rear Foot Width x 56.5" Length at Base' |
| REP Fitness | AB-5200 2.0 | 57.6 | 25.8 | 17.5 | - | [rep_ab5200](https://repfitness.com/products/ab-5200-2-0) | Assembled length 57.6, width 25.8 |
| Cybex | Free Adjustable Bench 16000 | 56 | 25 | 46 | - | [cybex_16000](https://kb.cybexintl.com/Owners_Manuals/Strength/16000-999-4.pdf) | manual lists 25 L x 56 W x 46 H (axes swapped) |

**Recommended model value:** footprint **56 x 25 in** (L x W); clearance **front 24 / back 18 / left 24 / right 24 in**. Exclusive envelope = 98 x 73 in = 49.7 ft2 (frame 9.7 ft2). Confidence: medium.  
_Derivation:_ Bench = median LF adjustable (55x25), LF MAB (58x29), HS MAB (54x27), Rogue AB-3.0 (56.5x24.75), REP AB-5200 2.0 (57.6x25.8), Cybex 16000 (56x25). LF live area 97 x 73 -> +42 L (24 front/18 back) and +48 W (24 per side for dumbbell arcs).

### `flat_bench` - Flat bench

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Hammer Strength | Flat Bench | 50 | 19 | 16 | 98 x 67 | [lfshop_hs_flat](https://shop.lifefitness.com/products/hammer-strength-flat-bench) | Footprint (D x W x H) 50x19x16; live 98 x 67 (catalog FW-FB 50x22x16) |
| Life Fitness | Flat Bench | 46 | 31 | 16.5 | 88 x 74 | [lfshop_lf_flat](https://shop.lifefitness.com/products/life-fitness-flat-bench) | 46 x 31 x 16.5; live 88 x 74 |
| Rogue | Flat Utility Bench 2.0 | 47 | 14 | 18 | - | [rogue_flat2](https://www.roguefitness.com/rogue-flat-utility-bench-2-0) | 'Footprint: 47" x 14"' |
| REP Fitness | FB-5000 Competition Flat Bench | 50.5 | 21 | 16.9 | - | [rep_fb5000](https://repfitness.com/products/fb-5000-competition-flat-bench) | length 50.5, width 21 |
| Cybex | Free Weight Flat Bench 16040 | 43 | 24 | 17 | - | [cybex_16040](https://kb.cybexintl.com/Owners_Manuals/Strength/16040-999-4.pdf) | 43 L x 24 W x 17 H (metric line says 122 cm) |

**Recommended model value:** footprint **47 x 21 in** (L x W); clearance **front 24 / back 24 / left 24 / right 24 in**. Exclusive envelope = 95 x 69 in = 45.5 ft2 (frame 6.9 ft2). Confidence: medium.  
_Derivation:_ Bench = median HS (50x19), LF (46x31), Rogue (47x14), REP FB-5000 (50.5x21), Cybex (43x24). Live areas HS 98x67 (+48/+48), LF 88x74 (+42/+43) -> 24 all round.

### `preacher_bench` - Preacher / arm-curl bench

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Hammer Strength | Seated Arm Curl | 38 | 34 | 42 | 74 x 70 | [lfshop_hs_arm_curl](https://shop.lifefitness.com/products/hammer-strength-seated-arm-curl) | Footprint 38x34x42; live 74 x 70 (catalog FW-AC 39x36x43) |
| Life Fitness | Arm Curl Bench | 47 | 33 | 46 | - | [lfshop_lf_arm_curl](https://shop.lifefitness.com/products/life-fitness-arm-curl-bench) | 47 x 33 x 46 |
| Cybex | Free Weight Scott Curl 16130 | 39 | 29 | 37 | - | [cybex_16130](https://kb.cybexintl.com/Owners_Manuals/Strength/16130-999-4.pdf) | 29 W x 39 L x 37 H |
| BodyKore | G257 Preacher Curl | 34 | 41 | 52 | - | [bk_g257](https://www.recoveryforathletes.com/products/g257-preacher-curl) | listing 34x41x52 |

**Recommended model value:** footprint **39 x 34 in** (L x W); clearance **front 24 / back 12 / left 18 / right 18 in**. Exclusive envelope = 75 x 70 in = 36.5 ft2 (frame 9.2 ft2). Confidence: medium.  
_Derivation:_ Bench = median HS seated arm curl (38x34), LF arm curl bench (47x33), Cybex Scott curl (39x29), BodyKore G257 (34x41). HS live area 74x70 -> +36/+36: 24 front (user side) /12 back, 18 per side.

### `hyperextension` - 45-degree hyperextension

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Hammer Strength | Back Extension (45-deg) BW-BE | 59 | 28 | 45 | 83 x 64 | [lfshop_hs_backext](https://shop.lifefitness.com/products/hammer-strength-back-extension) | Footprint 59x28x45; live 83 x 64 |
| Life Fitness | Back Extension (45-deg) | 50 | 37 | 38 | 106 x 74 | [lfcom_lf_backext](https://www.lifefitness.com/en-us/catalog/strength-training/benches/life-fitness-back-extension) | live 106 x 74 |
| Cybex | Free Weight 45-deg Back Extension 16020 | 58 | 30 | 32 | - | [cybex_16020](https://kb.cybexintl.com/Owners_Manuals/Strength/16020-999-4.pdf) | 30 W x 58 L x 32 H |

**Recommended model value:** footprint **58 x 30 in** (L x W); clearance **front 30 / back 12 / left 18 / right 18 in**. Exclusive envelope = 100 x 66 in = 45.8 ft2 (frame 12.1 ft2). Confidence: medium.  
_Derivation:_ 45-degree unit = median HS BW-BE (59x28), LF (50x37), Cybex 16020 (58x30). Live areas HS +24/+36, LF +56/+37 -> length margin median 40 -> 30 front (head/torso descent) / 12 back; width 36.5 -> 18 per side.

### `ghd` - Glute-ham developer (GHD)

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Rogue | Abram GHD | 73 | 44.5 | - | - | [rogue_abram_ghd](https://www.roguefitness.com/rogue-abram-ghd) | 'Overall Footprint: 73" x 44-1/2"' |
| REP Fitness | Glute Ham Developer | 70 | 36 | 42 | - | [rep_ghd](https://repfitness.com/products/ghd-glute-ham-developer) | Length 70, Width 36, Height 42 (top of pads) |
| Hammer Strength | Fixed Pad Glute/Ham | 74 | 34 | 51 | 110 x 82 | [lfshop_hs_fp_gh](https://shop.lifefitness.com/products/hammer-strength-fixed-pad-glute-ham-bench) | live 110 x 82 |
| Hammer Strength | Glute/Ham BW-GH | 72 | 33 | 50 | - | [hs_catalog_2024](https://cdn.shopify.com/s/files/1/0573/6877/2685/files/ISBU_Hammer-Strength-Catalog-2024-ENGLISH.pdf) | catalog |
| Hammer Strength | Glute Ham / Reverse Hyper Combo | 88 | 40 | 53 | 112 x 88 | [lfshop_hs_gh_rh](https://shop.lifefitness.com/products/hammer-strength-glute-ham-reverse-hyper-combo) | live 112 x 88 |

**Recommended model value:** footprint **73 x 36 in** (L x W); clearance **front 24 / back 12 / left 24 / right 24 in**. Exclusive envelope = 109 x 84 in = 63.6 ft2 (frame 18.2 ft2). Confidence: medium.  
_Derivation:_ GHD = median Rogue Abram (73x44.5), REP (70x36), HS fixed-pad (74x34), HS BW-GH (72x33), HS GH/reverse-hyper (88x40). HS live areas +36/+48 and +24/+48 -> 24 front / 12 back, 24 per side.

### `dip_chin_station` - Dip / chin / VKR tower

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Hammer Strength | Chin/Dip/Leg Raise | 49 | 44 | 92 | 85 x 44 | [lfshop_hs_cdl](https://shop.lifefitness.com/products/hammer-strength-chin-dip-leg-raise) | live 85 x 44 x 110 (overhead) |
| Life Fitness | Chin/Dip/Leg Raise | 45 | 50 | 91.5 | - | [lfshop_lf_cdl](https://shop.lifefitness.com/products/life-fitness-chin-dip-leg-raise) | 45 x 50 x 91.5 |
| BodyKore | CF2110 Chin Dip Tower | 50 | 49 | 89 | - | [bk_cf2110](https://www.recoveryforathletes.com/products/cf2110-chin-dip-tower) | listing |
| Life Fitness | Dip/Leg Raise (no chin) | 41.5 | 29 | 61 | 77.5 x 47 | [lfshop_lf_dlr](https://shop.lifefitness.com/products/life-fitness-dip-leg-raise) | live 77.5 x 47 |

**Recommended model value:** footprint **47 x 47 in** (L x W); clearance **front 36 / back 12 / left 12 / right 12 in**. Exclusive envelope = 95 x 71 in = 46.8 ft2 (frame 15.3 ft2). Confidence: medium.  
_Derivation:_ Tower = median HS chin/dip/leg raise (49x44), LF chin/dip/leg raise (45x50), BodyKore CF2110 (50x49), LF dip/leg raise (41.5x29). HS live 85x44x110 and LF 77.5x47 -> +36 front. Overhead envelope 110 in (HS).

### `hip_thrust_machine` - Hip thrust machine (plate-loaded)

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Hammer Strength | Plate-Loaded Glute Drive | 68 | 58.5 | 40 | 98 x 58.5 | [lfshop_hs_glute_drive](https://shop.lifefitness.com/products/hammer-strength-plate-loaded-glute-drive) | live 98 x 58.5 (D x W) |
| BodyKore | FL1844 Hip Thrust/Glute Builder | 54 | 57 | 52 | - | [bk_fl1844](https://www.recoveryforathletes.com/products/stacked-series-hip-thrust-glute-builder-plate-loaded-fl1844) | listing |
| Life Fitness | Insignia Glute Bridge (selectorized) | 75.8 | 31.8 | 58.1 | 99.6 x 67.8 | [lfshop_insignia_glute_bridge](https://shop.lifefitness.com/products/insignia-series-glute-bridge) | live 99.6 x 67.8 |
| BodyKore | GR624 Selectorized Hip Thrust | 50 | 63 | 65 | - | [bk_gr624](https://www.recoveryforathletes.com/products/gr624-selectorized-hip-thrust) | listing |

**Recommended model value:** footprint **61 x 58 in** (L x W); clearance **front 30 / back 12 / left 12 / right 12 in**. Exclusive envelope = 103 x 82 in = 58.7 ft2 (frame 24.6 ft2). Confidence: medium.  
_Derivation:_ Plate-loaded = median HS Glute Drive (68x58.5) and BodyKore FL1844 (54x57). HS live area 98 x 58.5 -> +30 front, +0 width (sides set to 12 in minimum half-gap). Insignia Glute Bridge (selectorized) live +24/+36 shown for reference.

### `hip_thrust_bench` - Hip thrust bench (barbell)

_No published commercial model with dimensions was found for this item (see gaps). Bench geometry from the flat-bench rows and bar length from section 3 were used._

**Recommended model value:** footprint **24 x 48 in** (L x W); clearance **front 48 / back 12 / left 36 / right 36 in**. Exclusive envelope = 84 x 120 in = 70.0 ft2 (frame 8.0 ft2). Confidence: low.  
_Derivation:_ ESTIMATE (no commercial hip-thrust-bench spec found). Bench ~48 x 24 in used side-on; user lies perpendicular to bench (front 48 for torso/feet); loaded 86.75 in bar spans width -> sides (86.75-48)/2 + 18 = 37 -> 36.

### `landmine` - Landmine station

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| REP Fitness | Free Standing Landmine (base) | 18.4 | 13.8 | - | - | [rep_landmine](https://repfitness.com/products/free-standing-landmine) | base plate 18.4 x 13.8; total length w/ sleeve 26.3 |
| Rogue | Ohio Bar (bar length governing landmine reach) | 86.75 | - | - | - | [rogue_ohio_bar](https://www.roguefitness.com/the-ohio-bar-black-zinc) | 'Exact length is 86.75"' |

**Recommended model value:** footprint **18 x 14 in** (L x W); clearance **front 120 / back 6 / left 36 / right 36 in**. Exclusive envelope = 144 x 86 in = 86.0 ft2 (frame 1.8 ft2). Confidence: low.  
_Derivation:_ ESTIMATE. Base = REP free-standing landmine plate 18.4 x 13.8 in (sleeve to 26.3 in). Bar 86.75 in projects forward + ~33 in standing user -> 120 in front. Sides 36 for presses/rows; rotational work (bar sweeps ~+/-45 deg -> ~120 in chord) needs ~60 per side.

### `fixed_barbell_rack` - Fixed barbell rack

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Barbell Rack (10 bars) | 38 | 34.5 | 61.5 | 84 x 60 | [lfshop_lf_barbell_rack](https://shop.lifefitness.com/products/life-fitness-barbell-rack) | 38 x 34.5 x 61.5; live 84 x 60 |
| Hammer Strength | Barbell Rack FW-BAR | 31 | 28 | 60 | - | [hs_catalog_2024](https://cdn.shopify.com/s/files/1/0573/6877/2685/files/ISBU_Hammer-Strength-Catalog-2024-ENGLISH.pdf) | catalog |

**Recommended model value:** footprint **35 x 31 in** (L x W); clearance **front 42 / back 6 / left 12 / right 12 in**. Exclusive envelope = 83 x 55 in = 31.7 ft2 (frame 7.5 ft2). Confidence: medium.  
_Derivation:_ Rack = median LF barbell rack (38x34.5, 10 bars) and HS FW-BAR (31x28). LF live area 84 x 60 -> +46 L / +25.5 W.

### `plate_tree` - Plate tree (auxiliary storage)

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Hammer Strength | Deluxe Weight Tree FW-DWT | 20 | 27 | 39 | - | [hs_catalog_2024](https://cdn.shopify.com/s/files/1/0573/6877/2685/files/ISBU_Hammer-Strength-Catalog-2024-ENGLISH.pdf) | catalog |
| Cybex | Free Weight Weight Tree 16140 | 35 | 25 | 54 | - | [cybex_16140](https://kb.cybexintl.com/Owners_Manuals/Strength/16140-999-4.pdf) | 35 L x 25 W x 54 H |

**Recommended model value:** footprint **27 x 26 in** (L x W); clearance **front 18 / back 18 / left 18 / right 18 in**. Exclusive envelope = 63 x 62 in = 27.1 ft2 (frame 4.9 ft2). Confidence: low.  
_Derivation:_ ESTIMATE. Tree = HS deluxe weight tree (20x27) and Cybex weight tree (35x25); loaded from all sides; no live area published.

### `leg_press` - 45-degree leg press (plate-loaded)

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Hammer Strength | Plate-Loaded Linear Leg Press HSLLP | 95 | 65 | 57 | 113 x 89 | [lfshop_hs_llp](https://shop.lifefitness.com/products/hammer-strength-plate-loaded-linear-leg-press) | live 113 x 89 |
| Life Fitness | Plate Loaded Linear Leg Press | 98 | 61 | 61 | - | [lfcom_lf_llp](https://www.lifefitness.com/en-us/catalog/strength-training/plate-loaded/life-fitness-linear-leg-press) |  |
| Cybex | Plate Loaded Leg Press 16110 | 83 | 64 | 54 | - | [cybex_16110](https://kb.cybexintl.com/Owners_Manuals/Strength/16110-999-4.pdf) | 64 W x 83 L x 54 H |
| BodyKore | G277 45-Degree Leg Press | 83 | 64 | 47 | - | [bk_g277](https://www.recoveryforathletes.com/products/g277-45-degree-leg-press) | listing 64x83x47 re-oriented |

**Recommended model value:** footprint **89 x 64 in** (L x W); clearance **front 24 / back 12 / left 24 / right 24 in**. Exclusive envelope = 125 x 112 in = 97.2 ft2 (frame 39.6 ft2). Confidence: medium.  
_Derivation:_ 45-deg plate-loaded = median HS Linear (95x65), LF Linear (98x61), Cybex 16110 (83x64), BodyKore G277 (83x64). HS live area 113x89 -> +18 L / +24 W; front raised to ISO 0.6 m access minimum; sides 24 (plate-loading at carriage horns; HS plate-loaded live areas typically +48 in width) - conflict noted.

### `hack_squat` - Hack squat (plate-loaded)

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Hammer Strength | Plate-Loaded Hack Squat PL-HSQ | 85 | 61 | 59 | - | [lfshop_hs_hack](https://shop.lifefitness.com/products/hammer-strength-plate-loaded-hack-squat) |  |
| Cybex | Plate Loaded Hack Squat 16200 | 80.15 | 60.57 | 53.65 | - | [cybex_16200](https://kb.cybexintl.com/Owners_Manuals/Strength/16200-999-4.pdf) | 60.57 W x 80.15 L |
| BodyKore | CF2175 Hack Squat | 80 | 64 | 55 | - | [bk_cf2175](https://www.recoveryforathletes.com/products/cf2175-hack-squat) | listing 64x80x55 re-oriented |

**Recommended model value:** footprint **80 x 61 in** (L x W); clearance **front 24 / back 12 / left 24 / right 24 in**. Exclusive envelope = 116 x 109 in = 87.8 ft2 (frame 33.9 ft2). Confidence: medium.  
_Derivation:_ Plate-loaded = median HS PL-HSQ (85x61), Cybex 16200 (80.2x60.6), BodyKore CF2175 (80x64). No live area published; plate-loaded rule: 24 front (access), 24 per side (plate loading), 12 back.

### `belt_squat_pendulum` - Belt squat / pendulum squat

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Hammer Strength | Plate-Loaded Belt Squat PL-BSQ | 78 | 63 | 64 | 102 x 111 | [lfshop_hs_belt](https://shop.lifefitness.com/products/hammer-strength-plate-loaded-belt-squat) | live 102 x 111 |
| Hammer Strength | Plate-Loaded Pendulum-X Squat | 97 | 45 | 81 | - | [lfshop_hs_pendulum](https://shop.lifefitness.com/products/hammer-strength-plate-loaded-pendulum-x-squat-1) |  |
| Hammer Strength | Plate-Loaded V-Squat PL-VSQ | 97 | 42 | 81 | - | [lfshop_hs_vsquat](https://shop.lifefitness.com/products/hammer-strength-plate-loaded-v-squat) |  |
| BodyKore | CF8137 Pendulum Squat | 83 | 43 | 67 | - | [bk_cf8137](https://www.recoveryforathletes.com/products/cf8137-pendulum-squat) | listing |
| BodyKore | FL1834 Belt Squat | 66 | 68 | 87 | - | [bk_fl1834](https://www.recoveryforathletes.com/products/fl1834-belt-squat) | listing |

**Recommended model value:** footprint **84 x 54 in** (L x W); clearance **front 24 / back 12 / left 24 / right 24 in**. Exclusive envelope = 120 x 102 in = 85.0 ft2 (frame 31.5 ft2). Confidence: medium.  
_Derivation:_ Average of archetype medians: belt squat (HS PL-BSQ 78x63, BodyKore FL1834 66x68 -> 72x65.5) and pendulum/V-squat (HS Pendulum-X 97x45, HS V-Squat 97x42, BodyKore CF8137 83x43 -> 97x43). HS belt-squat live area 102x111 -> +24 L / +48 W.

### `leg_extension` - Leg extension

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Insignia Leg Extension | 65.4 | 41.5 | 58.1 | 83.4 x 65.5 | [lfcom_insignia_le](https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-leg-extension) |  |
| Hammer Strength | Select Leg Extension | 47 | 41 | 64 | 89 x 65 | [lfshop_hs_select_le](https://shop.lifefitness.com/products/hammer-strength-select-leg-extension) | catalog HS-LE same |
| Cybex | Eagle NX Leg Extension 20050 | 50 | 43 | 56 | in-use 62 x 43 | [cybex_20050](https://kb.cybexintl.com/Owners_Manuals/Strength/20050-999-4.pdf) | in use 62 x 43 |
| Life Fitness | Axiom Leg Extension | 73 | 40 | 53 | 91 x 64 | [lfshop_axiom_le](https://shop.lifefitness.com/products/axiom-series-leg-extension) |  |
| Life Fitness | Signature (FZLE) Leg Extension | 57 | 42 | 64 | 99 x 66 | [lf_fz_manual_p32](https://personalcare.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=32) |  |

**Recommended model value:** footprint **57 x 42 in** (L x W); clearance **front 30 / back 12 / left 12 / right 12 in**. Exclusive envelope = 99 x 66 in = 45.4 ft2 (frame 16.6 ft2). Confidence: high.  
_Derivation:_ Median of LF Insignia (65.4x41.5), HS Select (47x41), Cybex Eagle NX (50x43), LF Axiom (73x40), LF Signature FZ (57x42). Live-area length margins 18/42/18/42 -> 30 front; width margins all +24 -> 12 per side. Cybex in-use +12 L.

### `leg_curl` - Leg curl (seated or prone)

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Insignia Seated Leg Curl | 61 | 39.7 | 58.1 | 79 x 63.7 | [lfcom_insignia_slc](https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-seated-leg-curl) |  |
| Hammer Strength | Select Seated Leg Curl | 55 | 34 | 55 | 89 x 58 | [lfshop_hs_select_slc](https://shop.lifefitness.com/products/hammer-strength-select-seated-leg-curl) |  |
| Cybex | Eagle NX Seated Leg Curl 20060 | 62 | 43 | 56 | in-use 62 x 43 | [cybex_20060](https://kb.cybexintl.com/Owners_Manuals/Strength/20060-999-4.pdf) | in use same |
| Life Fitness | Insignia (Prone) Leg Curl | 62.6 | 41.7 | 58.1 | 98.6 x 65.7 | [lfshop_insignia_lc](https://shop.lifefitness.com/products/insignia-series-leg-curl) | prone |
| Hammer Strength | Select (Prone) Leg Curl | 65 | 39 | 55 | 107 x 63 | [lfshop_hs_select_lc](https://shop.lifefitness.com/products/hammer-strength-select-leg-curl) | prone |
| Life Fitness | Signature (FZSLC) Seated Leg Curl | 62 | 42 | 64 | 104 x 66 | [lf_fz_manual_p33](https://personalcare.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=33) |  |

**Recommended model value:** footprint **62 x 41 in** (L x W); clearance **front 36 / back 12 / left 12 / right 12 in**. Exclusive envelope = 110 x 65 in = 49.7 ft2 (frame 17.7 ft2). Confidence: high.  
_Derivation:_ Median of seated and prone units: Insignia seated (61x39.7), HS Select seated (55x34), Cybex NX (62x43), Insignia prone (62.6x41.7), HS Select prone (65x39), LF FZ seated (62x42). Length margins 18/34/36/42/42 -> 36; width +24 -> 12 per side.

### `leg_ext_curl_combo` - Leg extension / curl combo

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Axiom Leg Curl/Extension | 63 | 40 | 53 | 105 x 64 | [lfshop_axiom_lcle](https://shop.lifefitness.com/products/axiom-series-leg-curl-extension) |  |
| Life Fitness | Axiom Seated Leg Curl/Extension | 70 | 46 | 53 | 100 x 70 | [lfshop_axiom_slcle](https://shop.lifefitness.com/products/axiom-series-seated-leg-curl-extension) |  |

**Recommended model value:** footprint **67 x 43 in** (L x W); clearance **front 36 / back 12 / left 12 / right 12 in**. Exclusive envelope = 115 x 67 in = 53.5 ft2 (frame 20.0 ft2). Confidence: medium.  
_Derivation:_ LF Axiom leg curl/extension (63x40, live +42/+24) and Axiom seated leg curl/extension (70x46, live +30/+24).

### `hip_abductor_adductor` - Hip abductor / adductor (combo)

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Insignia Hip Abduction/Adduction | 67 | 63.4 | 58.2 | 67 x 89 | [lfcom_insignia_haa](https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-hip-abductor-adductor) |  |
| Life Fitness | Axiom Hip Abductor/Adductor | 68 | 67 | 73 | 68 x 103 | [lfshop_axiom_haa](https://shop.lifefitness.com/products/axiom-series-hip-abductor-adductor) |  |
| Cybex | Eagle NX Hip Abduction/Adduction 20180 | 64 | 33 | 56 | in-use 82 x 63 | [cybex_20180](https://kb.cybexintl.com/Owners_Manuals/Strength/20180-999-4.pdf) | in use 82 x 63 |
| BodyKore | GR632 Hip Adductor/Abductor | 70 | 40 | 65 | - | [bk_gr632](https://www.recoveryforathletes.com/products/gr632-hip-adductor-abductor) | listing |
| Hammer Strength | Select Hip Abduction (single fn) | 61 | 26 | 55 | 61 x 77 | [lfshop_hs_select_hab](https://shop.lifefitness.com/products/hammer-strength-select-hip-abduction) | single-function reference |

**Recommended model value:** footprint **67 x 52 in** (L x W); clearance **front 24 / back 12 / left 18 / right 18 in**. Exclusive envelope = 103 x 88 in = 62.9 ft2 (frame 24.2 ft2). Confidence: medium.  
_Derivation:_ Combo = median Insignia (67x63.4), Axiom (68x67), Cybex NX (64x33 at rest; 82x63 in use), BodyKore GR632 (70x40). Live areas add 0 length, +25.6/+36 width (combo) -> 18 per side; front set to ISO 24 access minimum.

### `glute_kickback` - Glute kickback / multi-hip

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Insignia Glute | 73 | 38.4 | 58.1 | 73 x 62.4 | [lfcom_insignia_glute](https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-glute) |  |
| Hammer Strength | Select Hip & Glute | 65 | 39 | 72 | 94 x 39 | [lfshop_hs_select_hg](https://shop.lifefitness.com/products/hammer-strength-select-hip-and-glute) |  |
| Cybex | Eagle Glute 11170 | 69.65 | 41.14 | 61 | in-use 81.35 x 41.14 | [cybex_11170](https://kb.cybexintl.com/Owners_Manuals/Strength/11170-999-4.pdf) | in use 81.35 L |
| Cybex | VR3 Glute 12170 | 63 | 42 | 64 | in-use 85 x 42 | [cybex_12170](https://kb.cybexintl.com/Owners_Manuals/Strength/12170-999-4.pdf) | in use 85 x 42 |
| Life Fitness | Signature (FZGL) Glute | 72 | 36 | 64 | 72 x 60 | [lf_fz_manual_p35](https://caraudio.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=35) |  |

**Recommended model value:** footprint **70 x 39 in** (L x W); clearance **front 30 / back 12 / left 12 / right 12 in**. Exclusive envelope = 112 x 63 in = 49.0 ft2 (frame 19.0 ft2). Confidence: medium.  
_Derivation:_ Median Insignia glute (73x38.4), HS hip & glute (65x39), Cybex Eagle glute (69.7x41.1), Cybex VR3 glute (63x42), LF FZ glute (72x36). Live margins L 0/29/0, W 24/0/24; Cybex in-use +12-22 L (lever travel) -> front 30.

### `calf_raise` - Calf raise (seated / standing)

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Hammer Strength | Plate-Loaded Seated Calf Raise | 49 | 33 | 44 | - | [lfshop_hs_pl_calf](https://shop.lifefitness.com/products/hammer-strength-plate-loaded-seated-calf-raise) | catalog PL-CALF 49x33x54 |
| Hammer Strength | Select Standing Calf | 58 | 45 | 72 | 76 x 63 | [lfshop_hs_select_sc](https://shop.lifefitness.com/products/hammer-strength-select-standing-calf) |  |
| Hammer Strength | Select Horizontal Calf | 61 | 32 | 55 | 77 x 56 | [lfshop_hs_select_hc](https://shop.lifefitness.com/products/hammer-strength-select-horizontal-calf) |  |
| Life Fitness | Insignia Calf Extension | 40.2 | 68.5 | 58.1 | 58.2 x 92.5 | [lfcom_insignia_calf](https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-calf-extension) |  |
| Cybex | Plate Loaded 60-deg Calf 16290 | 60.63 | 29.87 | 50.95 | - | [cybex_16290](https://kb.cybexintl.com/Owners_Manuals/Strength/16290-999-4.pdf) |  |
| BodyKore | CF2172 Calf Raise | 51 | 33 | 36 | - | [bk_cf2172](https://www.recoveryforathletes.com/products/cf2172-calf-raise) | listing |

**Recommended model value:** footprint **54 x 33 in** (L x W); clearance **front 24 / back 12 / left 18 / right 18 in**. Exclusive envelope = 90 x 69 in = 43.1 ft2 (frame 12.4 ft2). Confidence: medium.  
_Derivation:_ Median HS PL seated calf (49x33), HS Select standing (58x45), HS horizontal (61x32), Insignia calf ext (40.2x68.5), Cybex 60-deg PL (60.6x29.9), BodyKore CF2172 (51x33). Live margins +18 L / +18-24 W; sides 18 to allow plate loading on seated plate-loaded units.

### `chest_press` - Chest press

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Insignia Chest Press | 43.2 | 55.3 | 58.1 | 67.2 x 55.3 | [lfcom_insignia_cp](https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-chest-press) |  |
| Hammer Strength | Select Chest Press | 41 | 57 | 64 | 83 x 57 | [lfshop_hs_select_cp](https://shop.lifefitness.com/products/hammer-strength-select-chest-press) |  |
| Cybex | Eagle NX Chest Press 20000 | 45 | 57 | 71 | in-use 53 x 57 | [cybex_20000](https://kb.cybexintl.com/Owners_Manuals/Strength/20000-999-4.pdf) | in use 53 x 57 |
| Life Fitness | Axiom Chest Press | 44 | 51 | 53 | 59 x 63 | [lfshop_axiom_cp](https://shop.lifefitness.com/products/axiom-series-chest-press) |  |
| Life Fitness | Signature (FZCP) Chest Press | 57 | 52 | 71 | 96 x 52 | [lf_fz_manual_p30](https://personalcare.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=30) |  |

**Recommended model value:** footprint **44 x 55 in** (L x W); clearance **front 30 / back 12 / left 12 / right 12 in**. Exclusive envelope = 86 x 79 in = 47.2 ft2 (frame 16.8 ft2). Confidence: high.  
_Derivation:_ Median Insignia (43.2x55.3), HS Select (41x57), Cybex NX (45x57), Axiom (44x51), LF FZ (57x52). Length margins 24/42/15/39 -> 30; width margins ~0 -> 12 minimum.

### `pec_fly_rear_delt` - Pec fly / rear delt

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Insignia Pectoral Fly/Rear Deltoid | 79.9 | 77.6 | 80.1 | 91.9 x 101.6 | [lfcom_insignia_pfrd](https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-pectoral-fly-rear-deltoid) |  |
| Hammer Strength | Select Pectoral Fly/Rear Deltoid | 49 | 56 | 71 | 103 x 68 | [lfshop_hs_select_pfrd](https://shop.lifefitness.com/products/hammer-strength-select-pectoral-fly-rear-deltoid) |  |
| Life Fitness | Axiom Pectoral Fly/Rear Deltoid | 61 | 75 | 81 | 97 x 99 | [lfshop_axiom_pfrd](https://shop.lifefitness.com/products/axiom-series-pectoral-fly-rear-deltoid) |  |
| Life Fitness | Signature (FZPEC) Fly | 50 | 38 | 64 | 94 x 46 | [lf_fz_manual_p34](https://personalcare.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=34) |  |

**Recommended model value:** footprint **56 x 66 in** (L x W); clearance **front 42 / back 12 / left 12 / right 12 in**. Exclusive envelope = 110 x 90 in = 68.8 ft2 (frame 25.7 ft2). Confidence: medium.  
_Derivation:_ Median Insignia (79.9x77.6), HS Select (49x56), Axiom (61x75), LF FZ fly (50x38). Length margins 12/54/36/44 -> 40 -> 42; width margins 24/12/24/8 -> 18 -> 12 per side minimum.

### `shoulder_press` - Shoulder press

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Insignia Shoulder Press | 64.4 | 56.8 | 72.8 | 88.4 x 68.8 | [lfcom_insignia_sp](https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-shoulder-press) |  |
| Hammer Strength | Select Shoulder Press | 60 | 56 | 64 | 102 x 56 | [lfshop_hs_select_sp](https://shop.lifefitness.com/products/hammer-strength-select-shoulder-press) |  |
| Cybex | Eagle NX Overhead Press 20010 | 68 | 61 | 56 | in-use 68 x 61 | [cybex_20010](https://kb.cybexintl.com/Owners_Manuals/Strength/20010-999-4.pdf) |  |
| Life Fitness | Axiom Shoulder Press | 61 | 55 | 53 | 85 x 67 | [lfshop_axiom_sp](https://shop.lifefitness.com/products/axiom-series-shoulder-press) |  |
| Life Fitness | Signature (FZSP) Shoulder Press | 60 | 52 | 64 | 102 x 52 | [lf_fz_manual_p30](https://personalcare.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=30) |  |

**Recommended model value:** footprint **61 x 56 in** (L x W); clearance **front 36 / back 12 / left 12 / right 12 in**. Exclusive envelope = 109 x 80 in = 60.6 ft2 (frame 23.7 ft2). Confidence: high.  
_Derivation:_ Median Insignia (64.4x56.8), HS Select (60x56), Cybex NX (68x61), Axiom (61x55), LF FZ (60x52). Length margins 24/42/24/42 -> 33 -> 36.

### `lat_pulldown` - Lat pulldown

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Insignia Pulldown | 55.6 | 56.9 | 76.2 | 79.6 x 68.9 | [lfcom_insignia_pd](https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-pulldown) |  |
| Hammer Strength | Select Lat Pulldown | 54 | 33 | 89 | 78 x 48 | [lfshop_hs_select_pd](https://shop.lifefitness.com/products/hammer-strength-select-lat-pulldown) |  |
| Cybex | Eagle NX Pulldown 20130 | 57 | 65 | 74 | in-use 57 x 65 | [cybex_20130](https://kb.cybexintl.com/Owners_Manuals/Strength/20130-999-4.pdf) |  |
| Life Fitness | Axiom Pulldown | 60 | 55 | 73 | 84 x 67 | [lfshop_axiom_pd](https://shop.lifefitness.com/products/axiom-series-pulldown) |  |
| Life Fitness | Signature (FZPD) Pulldown | 54 | 52 | 78 | 96 x 64 | [lf_fz_manual_p31](https://personalcare.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=31) |  |

**Recommended model value:** footprint **56 x 55 in** (L x W); clearance **front 24 / back 12 / left 12 / right 12 in**. Exclusive envelope = 92 x 79 in = 50.5 ft2 (frame 21.4 ft2). Confidence: high.  
_Derivation:_ Median Insignia (55.6x56.9), HS Select (54x33), Cybex NX (57x65), Axiom (60x55), LF FZ (54x52). Length margins 24/24/24/42 -> 24; width 12-15 -> 12 per side min. Heights to 89-90 in.

### `seated_row` - Seated row

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Insignia Row | 48.8 | 55.4 | 58.1 | 72.8 x 67.4 | [lfcom_insignia_row](https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-row) |  |
| Hammer Strength | Select Seated Row | 52 | 34 | 71 | 76 x 52 | [lfshop_hs_select_row](https://shop.lifefitness.com/products/hammer-strength-select-seated-row) |  |
| Cybex | Eagle NX Row 20030 | 68 | 43 | 73 | in-use 68 x 43 | [cybex_20030](https://kb.cybexintl.com/Owners_Manuals/Strength/20030-999-4.pdf) |  |
| Life Fitness | Axiom Seated Row | 65 | 40 | 53 | 89 x 58 | [lfshop_axiom_row](https://shop.lifefitness.com/products/axiom-series-seated-row-1) |  |
| Life Fitness | Signature (FZRW) Row/Rear Delt | 58 | 43 | 64 | 82 x 52 | [lf_fz_manual_p32](https://personalcare.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=32) |  |

**Recommended model value:** footprint **58 x 43 in** (L x W); clearance **front 24 / back 12 / left 12 / right 12 in**. Exclusive envelope = 94 x 67 in = 43.7 ft2 (frame 17.3 ft2). Confidence: high.  
_Derivation:_ Median Insignia row (48.8x55.4), HS Select (52x34), Cybex NX (68x43), Axiom (65x40), LF FZ (58x43). All four live areas add +24 in length; width +9 to +18.

### `lat_pulldown_row_combo` - Lat pulldown / row combo

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Axiom Pulldown/Row | 81 | 50 | 85 | 105 x 86 | [lfshop_axiom_pdrow](https://shop.lifefitness.com/products/axiom-series-pulldown-row) |  |
| Hammer Strength | HD Elite Dual Pulldown/Row HDU-DPR | 63 | 36 | 96 | - | [lfcom_hs_pdrow](https://www.lifefitness.com/en-us/catalog/strength-training/cable-machines-functional-trainers/hammer-strength-pulldown-row) |  |
| BodyKore | GR638 Lat Pulldown/Low Row | 69 | 49 | 94 | - | [bk_gr638](https://www.recoveryforathletes.com/products/gr638-lat-pulldown-low-row) | listing |

**Recommended model value:** footprint **69 x 49 in** (L x W); clearance **front 24 / back 12 / left 18 / right 18 in**. Exclusive envelope = 105 x 85 in = 62.0 ft2 (frame 23.5 ft2). Confidence: medium.  
_Derivation:_ Median LF Axiom pulldown/row (81x50, live +24/+36), HS HD Elite dual pulldown/row (63x36), BodyKore GR638 (69x49).

### `assisted_pullup_dip` - Assisted pull-up / dip

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Insignia Assist Dip Chin | 63.8 | 58 | 87 | 63.8 x 58 | [lfcom_insignia_adc](https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-assist-dip-chin) | live height 105 |
| Hammer Strength | Select Assist Dip Chin | 46 | 45 | 87 | 70 x 45 | [lfshop_hs_select_adc](https://shop.lifefitness.com/products/hammer-strength-select-assist-dip-chin) |  |
| BodyKore | GR636 Chin Dip Assist | 55 | 49 | 90 | - | [bk_gr636](https://www.recoveryforathletes.com/products/gr636-chin-dip-assist) | listing |

**Recommended model value:** footprint **55 x 49 in** (L x W); clearance **front 24 / back 12 / left 12 / right 12 in**. Exclusive envelope = 91 x 73 in = 46.1 ft2 (frame 18.7 ft2). Confidence: medium.  
_Derivation:_ Median Insignia ADC (63.8x58), HS Select ADC (46x45), BodyKore GR636 (55x49). Live margins 0/+24 L, 0 W; Insignia live height 105 in (overhead).

### `biceps_curl_machine` - Biceps curl machine

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Insignia Biceps Curl | 47.9 | 62.7 | 58.1 | 71.9 x 62.7 | [lfcom_insignia_bc](https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-biceps-curl) |  |
| Hammer Strength | Select Biceps Curl | 45 | 41 | 55 | 53 x 65 | [lfshop_hs_select_bc](https://shop.lifefitness.com/products/hammer-strength-select-biceps-curl) |  |
| Cybex | Eagle NX Arm Curl 20070 | 45 | 60 | 60 | in-use 45 x 60 | [cybex_20070](https://kb.cybexintl.com/Owners_Manuals/Strength/20070-999-4.pdf) |  |
| Life Fitness | Axiom Biceps Curl | 55 | 41 | 53 | 79 x 53 | [lfshop_axiom_bc](https://shop.lifefitness.com/products/axiom-series-biceps-curl) |  |
| Life Fitness | Signature (FZBC) Biceps Curl | 36 | 60 | 64 | 78 x 69 | [lf_fz_manual_p31](https://personalcare.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=31) |  |

**Recommended model value:** footprint **45 x 60 in** (L x W); clearance **front 24 / back 12 / left 12 / right 12 in**. Exclusive envelope = 81 x 84 in = 47.2 ft2 (frame 18.8 ft2). Confidence: high.  
_Derivation:_ Median Insignia (47.9x62.7), HS Select (45x41), Cybex NX (45x60), Axiom (55x41), LF FZ (36x60). Length margins 24/8/24/42 -> 24.

### `triceps_machine` - Triceps machine

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Insignia Triceps Extension | 53.9 | 39.6 | 58.1 | 84.4 x 57.6 | [lfcom_insignia_te](https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-triceps-extension) |  |
| Hammer Strength | Select Triceps Extension | 45 | 44 | 55 | 53 x 68 | [lfshop_hs_select_te](https://shop.lifefitness.com/products/hammer-strength-select-triceps-extension) |  |
| Cybex | Eagle NX Arm Extension 20080 | 45 | 60 | 60 | in-use 45 x 60 | [cybex_20080](https://kb.cybexintl.com/Owners_Manuals/Strength/20080-999-4.pdf) |  |
| Life Fitness | Axiom Triceps Extension | 57 | 41 | 53 | 81 x 53 | [lfshop_axiom_te](https://shop.lifefitness.com/products/axiom-series-triceps-extension) |  |
| Life Fitness | Signature (FZTP) Triceps Press | 64 | 43 | 64 | 106 x 43 | [lf_fz_manual_p31](https://personalcare.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=31) |  |

**Recommended model value:** footprint **54 x 43 in** (L x W); clearance **front 30 / back 12 / left 12 / right 12 in**. Exclusive envelope = 96 x 67 in = 44.7 ft2 (frame 16.1 ft2). Confidence: high.  
_Derivation:_ Median Insignia triceps ext (53.9x39.6), HS Select (45x44), Cybex NX (45x60), Axiom (57x41), LF FZ triceps press (64x43). Length margins 30.5/8/24/42 -> 27 -> 30.

### `ab_crunch_machine` - Ab crunch machine

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Insignia Abdominal | 52.4 | 46.3 | 58.1 | 76.5 x 57.9 | [lfcom_insignia_ab](https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-abdominal) |  |
| Hammer Strength | Select Abdominal Crunch | 62 | 35 | 55 | 70 x 58 | [lfshop_hs_select_ab](https://shop.lifefitness.com/products/hammer-strength-select-abdominal-crunch) |  |
| Cybex | Eagle NX Abdominal 20090 | 57 | 40 | 56 | in-use 57 x 40 | [cybex_20090](https://kb.cybexintl.com/Owners_Manuals/Strength/20090-999-4.pdf) |  |
| Life Fitness | Axiom Abdominal | 50 | 41 | 53 | 62 x 65 | [lfshop_axiom_ab](https://shop.lifefitness.com/products/axiom-series-abdominal) |  |
| Life Fitness | Signature (FZAB) Abdominal | 52 | 47 | 64 | 74 x 47 | [lf_fz_manual_p33](https://personalcare.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=33) |  |

**Recommended model value:** footprint **52 x 41 in** (L x W); clearance **front 24 / back 12 / left 12 / right 12 in**. Exclusive envelope = 88 x 65 in = 39.7 ft2 (frame 14.8 ft2). Confidence: high.  
_Derivation:_ Median Insignia (52.4x46.3), HS Select (62x35), Cybex NX (57x40), Axiom (50x41), LF FZ (52x47). Length margins 24/8/12/22 -> 17 -> raised to ISO 24 access minimum.

### `back_extension_machine` - Back extension machine

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Insignia Back Extension | 54.8 | 41.8 | 58.1 | 66.8 x 65.8 | [lfcom_insignia_be](https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-back-extension) |  |
| Hammer Strength | Select Back Extension | 46 | 40 | 55 | 64 x 64 | [lfshop_hs_select_be](https://shop.lifefitness.com/products/hammer-strength-select-back-extension) |  |
| Cybex | Eagle NX Back Extension 20100 | 59 | 40 | 56 | in-use 59 x 40 | [cybex_20100](https://kb.cybexintl.com/Owners_Manuals/Strength/20100-999-4.pdf) |  |
| Life Fitness | Signature (FZBE) Back Extension | 53 | 44 | 64 | 71 x 68 | [lf_fz_manual_p35](https://caraudio.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=35) |  |

**Recommended model value:** footprint **54 x 41 in** (L x W); clearance **front 24 / back 12 / left 12 / right 12 in**. Exclusive envelope = 90 x 65 in = 40.6 ft2 (frame 15.4 ft2). Confidence: high.  
_Derivation:_ Median Insignia (54.8x41.8), HS Select (46x40), Cybex NX (59x40), LF FZ (53x44). Length margins 12/18/18 -> 18 -> 24 minimum; width +24 -> 12 per side.

### `rotary_torso` - Rotary torso

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Insignia Torso Rotation | 45.5 | 44 | 61.9 | 69.5 x 56 | [lfcom_insignia_tr](https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-torso-rotation) |  |
| Cybex | Eagle NX Torso Rotation 20190 | 46 | 47 | 79 | in-use 46 x 53 | [cybex_20190](https://kb.cybexintl.com/Owners_Manuals/Strength/20190-999-4.pdf) | in use 46 x 53 |
| Cybex | VR3 Torso 12190 | 47 | 46 | 64 | in-use 47 x 51 | [cybex_12190](https://kb.cybexintl.com/Owners_Manuals/Strength/12190-999-4.pdf) | in use 47 x 51 |
| Life Fitness | Signature (FZTR) Torso Rotation | 48 | 36 | 64 | 90 x 48 | [lf_fz_manual_p35](https://caraudio.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=35) |  |

**Recommended model value:** footprint **47 x 45 in** (L x W); clearance **front 36 / back 12 / left 12 / right 12 in**. Exclusive envelope = 95 x 69 in = 45.5 ft2 (frame 14.7 ft2). Confidence: medium.  
_Derivation:_ Median Insignia (45.5x44), Cybex NX (46x47), Cybex VR3 (47x46), LF FZ (48x36). Length margins 24/42 -> 33 -> 36; Cybex in-use +5-6 W.

### `plate_loaded_chest_press` - Plate-loaded (iso-lateral) chest press

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Hammer Strength | Iso-Lateral Bench Press | 48 | 67 | 72 | 84 x 115 | [lfshop_hs_ilbp](https://shop.lifefitness.com/products/hammer-strength-plate-loaded-iso-lateral-bench-press) | live 84 x 115 x 96 (catalog IL-BP 49x52x69) |
| Hammer Strength | Iso-Lateral Horizontal Bench Press | 60 | 69 | 57 | - | [lfshop_hs_ilhbp](https://shop.lifefitness.com/products/hammer-strength-plate-loaded-iso-lateral-horizontal-bench-press) | catalog 66x61x42 |
| Hammer Strength | MTS Iso-Lateral Chest Press (selectorized) | 40 | 67 | 77 | 64 x 79 | [lfshop_hs_mts_cp](https://shop.lifefitness.com/products/hammer-strength-mts-iso-lateral-chest-press) | reference |
| Cybex | Plate Loaded Chest Press 16080 | 59 | 50 | 52 | - | [cybex_16080](https://kb.cybexintl.com/Owners_Manuals/Strength/16080-999-4.pdf) |  |

**Recommended model value:** footprint **59 x 67 in** (L x W); clearance **front 36 / back 12 / left 24 / right 24 in**. Exclusive envelope = 107 x 115 in = 85.5 ft2 (frame 27.5 ft2). Confidence: medium.  
_Derivation:_ Median HS Iso-Lateral Bench Press (48x67), HS Iso-Lateral Horizontal Bench Press (60x69), Cybex 16080 (59x50). HS IL bench press live area 84x115 -> +36 L / +48 W (24 per side for plate loading).

### `plate_loaded_row` - Plate-loaded (iso-lateral) row

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Hammer Strength | Iso-Lateral Row | 61 | 50 | 52 | - | [lfshop_hs_ilrow](https://shop.lifefitness.com/products/hammer-strength-plate-loaded-iso-lateral-row) | catalog IL-ROW 59x50x51 |
| Hammer Strength | Iso-Lateral Low Row | 50 | 48 | 66 | - | [lfshop_hs_illr](https://shop.lifefitness.com/products/hammer-strength-plate-loaded-iso-lateral-low-row) | catalog IL-LR 48x47x67 |
| Hammer Strength | MTS Iso-Lateral Row (selectorized) | 51 | 62 | 82 | 75 x 74 | [lfshop_hs_mts_row](https://shop.lifefitness.com/products/hammer-strength-mts-iso-lateral-row-1) | reference |
| Cybex | Plate Loaded Row 16090 | 82 | 34 | 48 | - | [cybex_16090](https://kb.cybexintl.com/Owners_Manuals/Strength/16090-999-4.pdf) | manual 34 L x 82 W (re-oriented, uncertain) |

**Recommended model value:** footprint **61 x 48 in** (L x W); clearance **front 24 / back 12 / left 24 / right 24 in**. Exclusive envelope = 97 x 96 in = 64.7 ft2 (frame 20.3 ft2). Confidence: medium.  
_Derivation:_ Median HS Iso-Lateral Row (61x50), HS Iso-Lateral Low Row (50x48), Cybex 16090 (82x34, orientation uncertain). No PL live area; MTS row (selectorized twin) +24 L; plate-loaded side rule 24.

### `plate_loaded_shoulder_press` - Plate-loaded shoulder press

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Hammer Strength | Iso-Lateral Shoulder Press | 52 | 60 | 73 | - | [lfshop_hs_ilsp](https://shop.lifefitness.com/products/hammer-strength-plate-loaded-iso-lateral-shoulder-press) | catalog IL-SP 51x58x74 |
| Hammer Strength | MTS Iso-Lateral Shoulder Press (selectorized) | 45 | 62 | 54 | 69 x 74 | [lfshop_hs_mts_sp](https://shop.lifefitness.com/products/hammer-strength-mts-iso-lateral-shoulder-press) | reference |

**Recommended model value:** footprint **52 x 60 in** (L x W); clearance **front 24 / back 12 / left 24 / right 24 in**. Exclusive envelope = 88 x 108 in = 66.0 ft2 (frame 21.7 ft2). Confidence: medium.  
_Derivation:_ HS Iso-Lateral Shoulder Press 52x60 (catalog 51x58). MTS shoulder press live +24 L; plate-loaded side rule 24.

### `plate_loaded_high_row` - Plate-loaded high row / pulldown

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Hammer Strength | Iso-Lateral High Row | 64 | 57 | 79 | - | [lfshop_hs_ilhr](https://shop.lifefitness.com/products/hammer-strength-iso-lateral-high-row) | catalog IL-HR 61x41x79 |
| Hammer Strength | Iso-Lateral Front Lat Pulldown | 65 | 49 | 79 | 77 x 97 | [lfshop_hs_ilfp](https://shop.lifefitness.com/products/hammer-strength-plate-loaded-iso-lateral-front-lat-pulldown) | live 77 x 97 x 96 (catalog IL-PD 65x41x80) |
| Hammer Strength | MTS Iso-Lateral High Row (selectorized) | 51 | 62 | 82 | 75 x 74 | [lfshop_hs_mts_hr](https://shop.lifefitness.com/products/hammer-strength-mts-iso-lateral-high-row) | reference |
| Cybex | Plate Loaded Pulldown 16070 | 49 | 87 | 72 | - | [cybex_16070](https://kb.cybexintl.com/Owners_Manuals/Strength/16070-999-4.pdf) |  |

**Recommended model value:** footprint **64 x 57 in** (L x W); clearance **front 24 / back 12 / left 24 / right 24 in**. Exclusive envelope = 100 x 105 in = 72.9 ft2 (frame 25.3 ft2). Confidence: medium.  
_Derivation:_ Median HS Iso-Lateral High Row (64x57), HS Iso-Lateral Front Lat Pulldown (65x49), Cybex 16070 PL pulldown (49x87). HS front lat pulldown live area 77x97 -> +12 L / +48 W.

### `t_bar_row` - T-bar row (chest-supported)

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Hammer Strength | Iso-Lateral T-Bar Row (chest-supported) | 70 | 60 | 39 | - | [lfcom_hs_iltbar](https://www.lifefitness.com/en-us/catalog/strength-training/plate-loaded/iso-lateral-t-bar-row) | 'plate-loaded, chest-supported row machine' |
| BodyKore | CF2173 Standing T-Bar Row | 70 | 37 | 48 | - | [bk_cf2173](https://www.recoveryforathletes.com/products/cf2173-standing-t-bar-row) | listing 37x70x48 re-oriented |
| Cybex | Plate Loaded T-Bar Row 16280 | 78.64 | 32.87 | 47.48 | - | [cybex_16280](https://kb.cybexintl.com/Owners_Manuals/Strength/16280-999-4.pdf) | in-use height 47.48 |
| Hammer Strength | Plate-Loaded T-Bar Row PL-TBR (lever) | 82.8 | 32.4 | 20.7 | - | [lfshop_hs_tbar](https://shop.lifefitness.com/products/hammer-strength-plate-loaded-t-bar-row) |  |

**Recommended model value:** footprint **70 x 37 in** (L x W); clearance **front 24 / back 12 / left 24 / right 24 in**. Exclusive envelope = 106 x 85 in = 62.6 ft2 (frame 18.0 ft2). Confidence: medium.  
_Derivation:_ Chest-supported = median HS Iso-Lateral T-Bar Row (70x60), BodyKore CF2173 (70x37), Cybex 16280 (78.6x32.9). Plate-loaded rule: 24 per side for loading.

### `multi_station_gym` - Multi-station (3-4 stack jungle gym)

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| BodyKore | GM5003 Four-Station Jungle Gym | 80 | 144 | 87 | - | [bk_gm5003](https://www.recoveryforathletes.com/products/gm5003-four-station-position-jungle-gym) | listing 144x80x87 re-oriented |
| BodyKore | MTI4005 3-Station Multi-Gym | 84 | 105 | 86 | - | [bk_mti4005](https://www.recoveryforathletes.com/products/mti4005-3-station-multi-gym-chest-back-leg-extension-leg-press) | listing 105x84x86 re-oriented |
| Life Fitness | Universal Cable (max config) | 69.8 | 103.8 | 89.7 | - | [lfshop_lf_universal](https://shop.lifefitness.com/products/life-fitness-universal-cable) | min 41.5 x 68.8; max 69.8 x 103.8 |

**Recommended model value:** footprint **82 x 125 in** (L x W); clearance **front 36 / back 36 / left 24 / right 24 in**. Exclusive envelope = 154 x 173 in = 185.0 ft2 (frame 71.2 ft2). Confidence: low.  
_Derivation:_ ESTIMATE between BodyKore MTI4005 3-station (84x105) and GM5003 4-station (80x144); LF Universal Cable max 69.8x103.8. Stations face several sides, so 36 in user zones front and back; no live area published.

### `cable_crossover` - Cable crossover (two adjustable stacks + bridge)

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Adjustable Cable Crossover | 28.5 | 150 | 94 | - | [lfcom_lf_acc](https://www.lifefitness.com/en-us/catalog/strength-training/cable-machines-functional-trainers/adjustable-cable-crossover) | published 150 x 28.5 x 94 (re-oriented: span = W) |
| BodyKore | G502 Cable Crossover | 28 | 151 | 91 | - | [bk_g502](https://www.recoveryforathletes.com/products/g502-cable-crossover) | listing 151x28x91 re-oriented |

**Recommended model value:** footprint **28 x 150 in** (L x W); clearance **front 48 / back 12 / left 12 / right 12 in**. Exclusive envelope = 88 x 174 in = 106.3 ft2 (frame 29.2 ft2). Confidence: low.  
_Derivation:_ Frame = LF Adjustable Cable Crossover (28.5 x 150) and BodyKore G502 (28 x 151); the user works inside the 150 in span. No live area published; front 48 is an ESTIMATE for split-stance/lunge positions forward of the tower plane.

### `functional_trainer` - Functional trainer (dual adjustable pulley)

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Signature Dual Adjustable Pulley | 45 | 62 | 94 | - | [lfshop_lf_dap](https://shop.lifefitness.com/products/life-fitness-dual-adjustable-pulley) | shop 45x62x94 (lifefitness.com 44x62x95); live area published as 217x410x112 - unit error suspected |
| Hammer Strength | HD Elite Dual Adjustable Pulley | 61 | 51 | 96 | - | [lfcom_hs_dap](https://www.lifefitness.com/en-us/catalog/strength-training/cable-machines-functional-trainers/hammer-strength-dual-adjustable-pulley) | D x W x H; width 42 or 72 option |
| SportsArt | DS972 Dual Stack Functional Trainer | 39.4 | 60.2 | 89.2 | - | [rfa_sportsart](https://www.recoveryforathletes.com/products/sportsart-ds972-status-dual-stack-functional-trainer) | listing 60.2 x 39.4 x 89.2 (L x W) re-oriented |
| BodyKore | MX1161 Functional Trainer | 48 | 70 | 89 | - | [bk_mx1161](https://www.recoveryforathletes.com/products/mx1161-functional-trainer-dual-adjustable-pulley) | listing 70x48x89 re-oriented |

**Recommended model value:** footprint **47 x 61 in** (L x W); clearance **front 60 / back 12 / left 24 / right 24 in**. Exclusive envelope = 119 x 109 in = 90.1 ft2 (frame 19.9 ft2). Confidence: low.  
_Derivation:_ Frame = median LF Signature DAP (45x62), HS HD Elite DAP (61x51), SportsArt DS972 (39.4x60.2), BodyKore MX1161 (48x70). Users step 3-5 ft out from the pulleys; front 60 is an ESTIMATE (LF's published live area '217x410x112 in' is evidently a unit error).

### `cable_column` - Cable column (single adjustable)

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Cybex | VR3 Cable Column 12220 | 50 | 43 | 92 | in-use 57 x 52 | [cybex_12220](https://kb.cybexintl.com/Owners_Manuals/Strength/12220-999-4.pdf) | in use 57 x 52 |
| BodyKore | MX1174 Universal1 Single Adjustable Pulley | 50 | 48 | 85 | - | [bk_mx1174](https://www.recoveryforathletes.com/products/mx1174-universal1-single-station-adjustable-pulley-system) | listing |

**Recommended model value:** footprint **50 x 46 in** (L x W); clearance **front 48 / back 12 / left 18 / right 18 in**. Exclusive envelope = 110 x 82 in = 62.6 ft2 (frame 16.0 ft2). Confidence: low.  
_Derivation:_ Frame = Cybex VR3 cable column (50x43; in use 57x52) and BodyKore MX1174 (50x48). Front 48 / sides 18 are ESTIMATES for pull, press and chop patterns (Cybex in-use +7 L / +9 W).

### `leg_press_selectorized` - Seated leg press (selectorized, reference only)

| Brand | Model | L | W | H | Live/in-use L x W | Source | Note |
|---|---|---|---|---|---|---|---|
| Life Fitness | Insignia Arc Leg Press | 79.5 | 44.8 | 64.7 | 97.5 x 68.8 | [lfshop_insignia_lp](https://shop.lifefitness.com/products/insignia-series-leg-press) |  |
| Hammer Strength | Select Seated Leg Press | 79 | 40 | 71 | 79 x 64 | [lfshop_hs_select_slp](https://shop.lifefitness.com/products/hammer-strength-select-seated-leg-press) |  |
| Cybex | Eagle NX Leg Press 20040 | 68 | 42 | 73 | in-use 100 x 42 | [cybex_20040](https://kb.cybexintl.com/Owners_Manuals/Strength/20040-999-4.pdf) | in use 100 L |
| Life Fitness | Axiom Leg Press | 86 | 40 | 53 | 98 x 64 | [lfshop_axiom_lp](https://shop.lifefitness.com/products/axiom-series-leg-press) |  |

_Reference only (not a taxonomy item)._

## 6. Summary table of recommended values (for the layout engine)

| id | L | W | front | back | left | right | envelope L x W | envelope ft2 | confidence |
|---|---|---|---|---|---|---|---|---|---|
| power_rack | 58 | 59 | 48 | 12 | 32 | 32 | 118 x 123 | 100.8 | medium |
| half_rack | 53 | 50 | 36 | 6 | 36 | 36 | 95 x 122 | 80.5 | medium |
| lifting_platform | 96 | 96 | 24 | 24 | 24 | 24 | 144 x 144 | 144.0 | medium |
| bench_press_station | 52 | 52 | 18 | 24 | 36 | 36 | 94 x 124 | 80.9 | medium |
| incline_bench_station | 59 | 52 | 18 | 24 | 36 | 36 | 101 x 124 | 87.0 | medium |
| decline_bench_station | 70 | 52 | 18 | 18 | 36 | 36 | 106 x 124 | 91.3 | medium |
| smith_machine | 50 | 87 | 48 | 24 | 18 | 18 | 122 x 123 | 104.2 | medium |
| dumbbell_rack_2tier_10pair | 24 | 87 | 36 | 0 | 0 | 0 | 60 x 87 | 36.2 | high |
| dumbbell_rack_3tier | 28 | 92 | 30 | 0 | 0 | 0 | 58 x 92 | 37.1 | medium |
| dumbbell_rack_horizontal_15pair | 24 | 90 | 36 | 0 | 0 | 0 | 60 x 90 | 37.5 | low |
| adjustable_bench | 56 | 25 | 24 | 18 | 24 | 24 | 98 x 73 | 49.7 | medium |
| flat_bench | 47 | 21 | 24 | 24 | 24 | 24 | 95 x 69 | 45.5 | medium |
| preacher_bench | 39 | 34 | 24 | 12 | 18 | 18 | 75 x 70 | 36.5 | medium |
| hyperextension | 58 | 30 | 30 | 12 | 18 | 18 | 100 x 66 | 45.8 | medium |
| ghd | 73 | 36 | 24 | 12 | 24 | 24 | 109 x 84 | 63.6 | medium |
| dip_chin_station | 47 | 47 | 36 | 12 | 12 | 12 | 95 x 71 | 46.8 | medium |
| hip_thrust_machine | 61 | 58 | 30 | 12 | 12 | 12 | 103 x 82 | 58.7 | medium |
| hip_thrust_bench | 24 | 48 | 48 | 12 | 36 | 36 | 84 x 120 | 70.0 | low |
| landmine | 18 | 14 | 120 | 6 | 36 | 36 | 144 x 86 | 86.0 | low |
| fixed_barbell_rack | 35 | 31 | 42 | 6 | 12 | 12 | 83 x 55 | 31.7 | medium |
| plate_tree | 27 | 26 | 18 | 18 | 18 | 18 | 63 x 62 | 27.1 | low |
| leg_press | 89 | 64 | 24 | 12 | 24 | 24 | 125 x 112 | 97.2 | medium |
| hack_squat | 80 | 61 | 24 | 12 | 24 | 24 | 116 x 109 | 87.8 | medium |
| belt_squat_pendulum | 84 | 54 | 24 | 12 | 24 | 24 | 120 x 102 | 85.0 | medium |
| leg_extension | 57 | 42 | 30 | 12 | 12 | 12 | 99 x 66 | 45.4 | high |
| leg_curl | 62 | 41 | 36 | 12 | 12 | 12 | 110 x 65 | 49.7 | high |
| leg_ext_curl_combo | 67 | 43 | 36 | 12 | 12 | 12 | 115 x 67 | 53.5 | medium |
| hip_abductor_adductor | 67 | 52 | 24 | 12 | 18 | 18 | 103 x 88 | 62.9 | medium |
| glute_kickback | 70 | 39 | 30 | 12 | 12 | 12 | 112 x 63 | 49.0 | medium |
| calf_raise | 54 | 33 | 24 | 12 | 18 | 18 | 90 x 69 | 43.1 | medium |
| chest_press | 44 | 55 | 30 | 12 | 12 | 12 | 86 x 79 | 47.2 | high |
| pec_fly_rear_delt | 56 | 66 | 42 | 12 | 12 | 12 | 110 x 90 | 68.8 | medium |
| shoulder_press | 61 | 56 | 36 | 12 | 12 | 12 | 109 x 80 | 60.6 | high |
| lat_pulldown | 56 | 55 | 24 | 12 | 12 | 12 | 92 x 79 | 50.5 | high |
| seated_row | 58 | 43 | 24 | 12 | 12 | 12 | 94 x 67 | 43.7 | high |
| lat_pulldown_row_combo | 69 | 49 | 24 | 12 | 18 | 18 | 105 x 85 | 62.0 | medium |
| assisted_pullup_dip | 55 | 49 | 24 | 12 | 12 | 12 | 91 x 73 | 46.1 | medium |
| biceps_curl_machine | 45 | 60 | 24 | 12 | 12 | 12 | 81 x 84 | 47.2 | high |
| triceps_machine | 54 | 43 | 30 | 12 | 12 | 12 | 96 x 67 | 44.7 | high |
| ab_crunch_machine | 52 | 41 | 24 | 12 | 12 | 12 | 88 x 65 | 39.7 | high |
| back_extension_machine | 54 | 41 | 24 | 12 | 12 | 12 | 90 x 65 | 40.6 | high |
| rotary_torso | 47 | 45 | 36 | 12 | 12 | 12 | 95 x 69 | 45.5 | medium |
| plate_loaded_chest_press | 59 | 67 | 36 | 12 | 24 | 24 | 107 x 115 | 85.5 | medium |
| plate_loaded_row | 61 | 48 | 24 | 12 | 24 | 24 | 97 x 96 | 64.7 | medium |
| plate_loaded_shoulder_press | 52 | 60 | 24 | 12 | 24 | 24 | 88 x 108 | 66.0 | medium |
| plate_loaded_high_row | 64 | 57 | 24 | 12 | 24 | 24 | 100 x 105 | 72.9 | medium |
| t_bar_row | 70 | 37 | 24 | 12 | 24 | 24 | 106 x 85 | 62.6 | medium |
| multi_station_gym | 82 | 125 | 36 | 36 | 24 | 24 | 154 x 173 | 185.0 | low |
| cable_crossover | 28 | 150 | 48 | 12 | 12 | 12 | 88 x 174 | 106.3 | low |
| functional_trainer | 47 | 61 | 60 | 12 | 24 | 24 | 119 x 109 | 90.1 | low |
| cable_column | 50 | 46 | 48 | 12 | 18 | 18 | 110 x 82 | 62.6 | low |

**Mapping to dumbbell taxonomy:** `dumbbell_set_light` (5-50 lb, 10 pairs) = one 2-tier 10-pair rack (LF and HS racks are rated for 10 pairs). `dumbbell_set_full` (5-100 lb, 20 pairs) = two 2-tier 10-pair racks, or one 3-tier 15-pair rack plus a 2-tier rack. `dumbbell_heavy_extension` (105-150 lb, 10 pairs in 5 lb steps) = one 2-tier 10-pair rack rated to 150 lb (the HS 2- and 3-tier racks list 'Max Dumbbell Size: 150 LB'). Pair counts per rack come from the LF and HS shop pages and from REP's 'Set Range'. Treat this mapping as a derived estimate.

## 7. Conflicts, errors found in sources, and how they were resolved

- Hammer Strength plate-loaded dimensions differ between the 2024 catalog and the current LF web/shop pages. Iso-Lateral Bench Press: catalog IL-BP 49x52x69 against web 48x67x72. Iso-Lateral High Row: IL-HR 61x41x79 against 64x57x79. Iso-Lateral Wide Chest: 45x59x69 against 77x45x75 (likely re-ordered axes). Olympic Decline: O-DB 60x53x50 against 70x52x51. The model uses the newer web/shop values; catalog values are kept in the notes.
- The LF shop page for the Signature Olympic Incline Bench lists 86 x 68 x 57 in. lifefitness.com lists 58 x 51 x 57 in for the same product, and the shop value is inconsistent with its own live area (101 x 120). The model uses 58 x 51.
- The LF Signature Dual Adjustable Pulley 'Recommended Live Area: 217" x 410" x 112"' is implausible (18 x 34 ft). It is probably a unit error (cm) and is not used. The LF DAP footprint is 45x62x94 (shop) against 44x62x95 (lifefitness.com).
- The Axiom Leg Curl live area of '101.2" x 170" x 77.2"' has an implausible 170 in width (the footprint is 43 in wide); its width margin was not used.
- The Cybex Eagle NX Glute manual (20170) repeats the Pulldown's dimensions (57x65x74). This looks like a copy error, so Eagle (11170) and VR3 (12170) glute dimensions are used instead.
- The HS Glute Drive live area is given as '98 in x 58.5 in x 40 in (249 cm x 240 cm)'. The metric width (240 cm = 94.5 in) conflicts with the imperial 58.5 in. The imperial value is used.
- The Rogue RML-490 page lists L 49 x W 49 but 'Foot Print 53" x 53"' (base feet). The 53 x 53 footprint is used, since the floor is occupied to the outside of the feet.
- The Cybex 16040 flat bench manual lists 43 in L but 122 cm (48 in) in metric. 43 in is used, with a range of 43-48.
- BodyKore dealer listings do not label axis order. Values were re-oriented so that W is the bar or stack-span axis where that is evident, and flagged in the notes.
- NSCA rack formula (156 in wide) vs manufacturer live areas (120 in): resolved toward the manufacturer value plus NSCA's 36 in between bar ends (section 2).
- The leg press side margin conflicts: the HS Linear Leg Press live area adds only 24 in of total width, while other HS plate-loaded live areas add 48 in. The model uses 24 in per side for loading.

## 8. Gaps and limitations

- The numeric free-area clause of ISO 20957-1 (current edition 2024) is paywalled. The 0.6 m value comes from manufacturer manuals that quote EN ISO 20957-1:2013 (KingsBox) or apply it (Cybex 23.6 in, Matrix 24 in).
- No Matrix Ultra/Versa/Magnum spec sheets were retrieved: the Matrix site is a JavaScript single-page app and the web-search budget for this session ran out. Matrix appears only through its MABR1 manual (ISO training/free-area convention and 24 in / 36 in clearance text). Precor, Nautilus, Hoist and Prime were not covered.
- No dedicated commercial hip-thrust bench spec was found. `hip_thrust_bench`, `landmine`, `dumbbell_rack_horizontal_15pair`, `plate_tree`, `multi_station_gym`, `cable_crossover`, `functional_trainer` and `cable_column` clearances are derived estimates (low confidence).
- The Nautilus/Core Health & Fitness Glute Drive manual reportedly gives 24 in clearance on each side, 48 in behind and 19.7 in between adjacent machines. It was seen only in a search summary and not fetched, so it is not used.
- ACSM Health/Fitness Facility Standards spacing values were not retrieved in this slice.
- Live-area semantics vary by manufacturer. LF Insignia live areas look like footprint + 24 in on the access axis + 12-24 in on the other axis, i.e. ISO training area + 0.6 m free area. Life Fitness does not define the term on the pages fetched.
- The distribution of a published live-area margin between front and back, or left and right, is not specified by manufacturers. The split used here (front-heavy for machines; symmetric sides) is an assumption.

## Appendix A. Incidental list prices seen while collecting specs (outside this slice; for cross-checking only)

Prices are the first-variant price in the Life Fitness US online store catalog (`shop.lifefitness.com/products.json`), fetched 2026-10-28, in USD. Plates and bars are not included. The first variant is not always the base configuration.

| Product | USD |
|---|---|
| HS HD Athletic NX Power Rack | 4,657 |
| HS HD Athletic NX Half Rack | 3,706 |
| HS HD Elite iD Half Rack | 6,229 |
| LF Olympic Flat Bench (Signature) | 1,789 |
| LF Olympic Incline Bench | 1,817 |
| LF Smith Machine | 7,641 |
| HS Smith Machine | 7,442 |
| LF Two-Tier Dumbbell Rack | 1,894 |
| HS Two-Tier Dumbbell Rack | 1,756 |
| HS Three-Tier Dumbbell Rack | 2,040 |
| LF Adjustable Bench | 1,495 |
| HS Multi-Adjustable Bench | 1,854 |
| HS Flat Bench | 772 |
| HS Seated Arm Curl | 1,709 |
| HS Back Extension | 1,794 |
| HS Fixed Pad Glute/Ham | 2,812 |
| HS Chin/Dip/Leg Raise | 2,422 |
| HS Plate Loaded Glute Drive | 4,907 |
| LF Barbell Rack | 1,659 |
| HS PL Linear Leg Press | 7,883 |
| HS PL Hack Squat | 7,883 |
| HS PL Belt Squat | 6,284 |
| HS PL Pendulum-X Squat | 8,820 |
| HS PL Iso-Lateral Bench Press | 4,135 |
| HS PL Iso-Lateral Row | 4,135 |
| HS PL Iso-Lateral Shoulder Press | 4,135 |
| HS Iso-Lateral High Row | 4,135 |
| HS PL T-Bar Row | 3,032 |
| HS PL Seated Calf Raise | 2,352 |
| Insignia Leg Extension | 8,315 |
| Insignia Seated Leg Curl | 8,485 |
| Insignia Chest Press | 8,424 |
| Insignia Pulldown | 8,000 |
| Insignia Row | 7,733 |
| Insignia Shoulder Press | 7,843 |
| Insignia Arc Leg Press | 11,892 |
| Axiom Pulldown/Row | 5,246 |
| Axiom Leg Curl/Extension | 5,246 |
| HS Select Leg Extension | 6,430 |
| HS Select Chest Press | 5,972 |
| LF Adjustable Cable Crossover | 9,370 |
| LF Dual Adjustable Pulley | 10,053 |
| Axiom Dual Adjustable Pulley | 6,250 |
| LF Universal Cable | 12,284 |
| HS Rubber Platform (4x8 insert) | 844 |
| HS Traditional Wood Platform | 4,980 |

## 9. Source index

| ID | Title | Publisher | Year | URL |
|---|---|---|---|---|
| `ada_2010` | 2010 ADA Standards for Accessible Design (206.2.13, 236, 305.3, 403.5.1, 1004.1) | U.S. Access Board / DOJ | 2010 | https://www.access-board.gov/ada/ |
| `bk_cf2110` | BodyKore cf2110-chin-dip-tower (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/cf2110-chin-dip-tower |
| `bk_cf2172` | BodyKore cf2172-calf-raise (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/cf2172-calf-raise |
| `bk_cf2173` | BodyKore cf2173-standing-t-bar-row (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/cf2173-standing-t-bar-row |
| `bk_cf2175` | BodyKore cf2175-hack-squat (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/cf2175-hack-squat |
| `bk_cf8137` | BodyKore cf8137-pendulum-squat (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/cf8137-pendulum-squat |
| `bk_fl1834` | BodyKore fl1834-belt-squat (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/fl1834-belt-squat |
| `bk_fl1844` | BodyKore stacked-series-hip-thrust-glute-builder-plate-loaded-fl1844 (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/stacked-series-hip-thrust-glute-builder-plate-loaded-fl1844 |
| `bk_g257` | BodyKore g257-preacher-curl (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/g257-preacher-curl |
| `bk_g271` | BodyKore g271-smith-machine (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/g271-smith-machine |
| `bk_g277` | BodyKore g277-45-degree-leg-press (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/g277-45-degree-leg-press |
| `bk_g502` | BodyKore g502-cable-crossover (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/g502-cable-crossover |
| `bk_g701` | BodyKore g701-half-rack (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/g701-half-rack |
| `bk_gm5003` | BodyKore gm5003-four-station-position-jungle-gym (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/gm5003-four-station-position-jungle-gym |
| `bk_gr624` | BodyKore gr624-selectorized-hip-thrust (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/gr624-selectorized-hip-thrust |
| `bk_gr632` | BodyKore gr632-hip-adductor-abductor (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/gr632-hip-adductor-abductor |
| `bk_gr636` | BodyKore gr636-chin-dip-assist (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/gr636-chin-dip-assist |
| `bk_gr638` | BodyKore gr638-lat-pulldown-low-row (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/gr638-lat-pulldown-low-row |
| `bk_mti4005` | BodyKore mti4005-3-station-multi-gym-chest-back-leg-extension-leg-press (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/mti4005-3-station-multi-gym-chest-back-leg-extension-leg-press |
| `bk_mx1161` | BodyKore mx1161-functional-trainer-dual-adjustable-pulley (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/mx1161-functional-trainer-dual-adjustable-pulley |
| `bk_mx1174` | BodyKore mx1174-universal1-single-station-adjustable-pulley-system (dealer listing with manufacturer specs) | Recovery For Athletes (BodyKore) |  | https://www.recoveryforathletes.com/products/mx1174-universal1-single-station-adjustable-pulley-system |
| `cybex_11170` | Cybex Eagle Glute Owner's Manual (part 11170-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/11170-999-4.pdf |
| `cybex_12170` | Cybex VR3 Glute Owner's Manual (part 12170-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/12170-999-4.pdf |
| `cybex_12190` | Cybex VR3 Torso Owner's Manual (part 12190-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/12190-999-4.pdf |
| `cybex_12220` | Cybex VR3 Cable Column Owner's Manual (part 12220-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/12220-999-4.pdf |
| `cybex_16000` | Cybex Free Adjustable Bench Owner's Manual (part 16000-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/16000-999-4.pdf |
| `cybex_16010` | Cybex Free Weight Olympic Bench Press Owner's Manual (part 16010-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/16010-999-4.pdf |
| `cybex_16020` | Cybex Free Weight 45 deg Back Extension Owner's Manual (part 16020-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/16020-999-4.pdf |
| `cybex_16040` | Cybex Free Weight Flat Bench Owner's Manual (part 16040-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/16040-999-4.pdf |
| `cybex_16060` | Cybex Free Weight Olympic Decline Press Owner's Manual (part 16060-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/16060-999-4.pdf |
| `cybex_16070` | Cybex Plate Loaded Pulldown Owner's Manual (part 16070-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/16070-999-4.pdf |
| `cybex_16080` | Cybex Plate Loaded Chest Press Owner's Manual (part 16080-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/16080-999-4.pdf |
| `cybex_16090` | Cybex Plate Loaded Row Owner's Manual (part 16090-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/16090-999-4.pdf |
| `cybex_16110` | Cybex Plate Loaded Leg Press Owner's Manual (part 16110-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/16110-999-4.pdf |
| `cybex_16130` | Cybex Free Weight Scott Curl Owner's Manual (part 16130-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/16130-999-4.pdf |
| `cybex_16140` | Cybex Free Weight Weight Tree Owner's Manual (part 16140-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/16140-999-4.pdf |
| `cybex_16200` | Cybex Plate Loaded Hack Squat Owner's Manual (part 16200-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/16200-999-4.pdf |
| `cybex_16280` | Cybex Plate Loaded T-Bar Row Owner's Manual (part 16280-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/16280-999-4.pdf |
| `cybex_16290` | Cybex Plate Loaded 60 Degree Calf Owner's Manual (part 16290-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/16290-999-4.pdf |
| `cybex_20000` | Cybex Eagle NX Chest Press Owner's Manual (part 20000-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/20000-999-4.pdf |
| `cybex_20010` | Cybex Eagle NX Overhead Press Owner's Manual (part 20010-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/20010-999-4.pdf |
| `cybex_20030` | Cybex Eagle NX Row Owner's Manual (part 20030-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/20030-999-4.pdf |
| `cybex_20040` | Cybex Eagle NX Leg Press Owner's Manual (part 20040-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/20040-999-4.pdf |
| `cybex_20050` | Cybex Eagle NX Leg Extension Owner's Manual (part 20050-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/20050-999-4.pdf |
| `cybex_20060` | Cybex Eagle NX Seated Leg Curl Owner's Manual (part 20060-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/20060-999-4.pdf |
| `cybex_20070` | Cybex Eagle NX Arm Curl Owner's Manual (part 20070-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/20070-999-4.pdf |
| `cybex_20080` | Cybex Eagle NX Arm Extension Owner's Manual (part 20080-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/20080-999-4.pdf |
| `cybex_20090` | Cybex Eagle NX Abdominal Owner's Manual (part 20090-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/20090-999-4.pdf |
| `cybex_20100` | Cybex Eagle NX Back Extension Owner's Manual (part 20100-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/20100-999-4.pdf |
| `cybex_20130` | Cybex Eagle NX Pulldown Owner's Manual (part 20130-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/20130-999-4.pdf |
| `cybex_20180` | Cybex Eagle NX Hip Abduction/Adduction Owner's Manual (part 20180-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/20180-999-4.pdf |
| `cybex_20190` | Cybex Eagle NX Torso Rotation Owner's Manual (part 20190-999-4) | Cybex International (Life Fitness) |  | https://kb.cybexintl.com/Owners_Manuals/Strength/20190-999-4.pdf |
| `hs_catalog_2024` | Hammer Strength Catalog 2024 (English) - Specifications pp. 59-64 | Hammer Strength / Life Fitness | 2024 | https://cdn.shopify.com/s/files/1/0573/6877/2685/files/ISBU_Hammer-Strength-Catalog-2024-ENGLISH.pdf |
| `iso20957_1_2013` | ISO 20957-1:2013 Stationary training equipment - Part 1: General safety requirements (preview: clause 3 terms & definitions) | ISO (preview hosted by iTeh) | 2013 | https://cdn.standards.iteh.ai/samples/56102/b0f72c8378484be29dc5ec9548ce4943/ISO-20957-1-2013.pdf |
| `kingsbox_manual` | KingsBox Foldable Flat Bench manual - EN ISO 20957-1:2013 Class S, free-area statement (pp. 4, 19) | KingsBox (via ManualsLib) |  | https://www.manualslib.com/manual/2565908/Kingsbox-Foldable-Flat-Bench.html |
| `lf_fz_manual_p30` | Life Fitness Signature Series (FZ selectorized) Owner's Manual, 4. Machine Specifications (chest/shoulder press) | Life Fitness (via ManualsOnline) |  | https://personalcare.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=30 |
| `lf_fz_manual_p31` | Life Fitness Signature Series Owner's Manual, Machine Specifications p.4-2 (pulldown/biceps/triceps) | Life Fitness (via ManualsOnline) |  | https://personalcare.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=31 |
| `lf_fz_manual_p32` | Life Fitness Signature Series Owner's Manual, Machine Specifications (row/rear delt, seated leg press, leg extension) | Life Fitness (via ManualsOnline) |  | https://personalcare.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=32 |
| `lf_fz_manual_p33` | Life Fitness Signature Series Owner's Manual, Machine Specifications (seated leg curl, abdominal, calf) | Life Fitness (via ManualsOnline) |  | https://personalcare.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=33 |
| `lf_fz_manual_p34` | Life Fitness Signature Series Owner's Manual, Machine Specifications (fly, hip ad/abduction, lateral raise) | Life Fitness (via ManualsOnline) |  | https://personalcare.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=34 |
| `lf_fz_manual_p35` | Life Fitness Signature Series Owner's Manual, Machine Specifications p.4-6 (back extension, glute, torso rotation) | Life Fitness (via ManualsOnline) |  | https://caraudio.manualsonline.com/manuals/mfg/life_fitness/8006348637.html?p=35 |
| `lfcom_hd_elite_power` | Life Fitness US product page: hd elite id power rack | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/racks-rigs-platforms/hd-elite-id-power-rack |
| `lfcom_hs_dap` | Life Fitness US product page: hammer strength dual adjustable pulley | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/cable-machines-functional-trainers/hammer-strength-dual-adjustable-pulley |
| `lfcom_hs_iltbar` | Life Fitness US product page: iso lateral t bar row | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/plate-loaded/iso-lateral-t-bar-row |
| `lfcom_hs_oly_decline` | Life Fitness US product page: olympic decline bench | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/benches/olympic-decline-bench |
| `lfcom_hs_oly_flat` | Life Fitness US product page: olympic flat bench | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/benches/olympic-flat-bench |
| `lfcom_hs_oly_incline` | Life Fitness US product page: olympic incline bench | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/benches/olympic-incline-bench |
| `lfcom_hs_pdrow` | Life Fitness US product page: hammer strength pulldown row | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/cable-machines-functional-trainers/hammer-strength-pulldown-row |
| `lfcom_insignia_ab` | Life Fitness US product page: insignia series abdominal | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-abdominal |
| `lfcom_insignia_adc` | Life Fitness US product page: insignia series assist dip chin | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-assist-dip-chin |
| `lfcom_insignia_bc` | Life Fitness US product page: insignia series biceps curl | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-biceps-curl |
| `lfcom_insignia_be` | Life Fitness US product page: insignia series back extension | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-back-extension |
| `lfcom_insignia_calf` | Life Fitness US product page: insignia series calf extension | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-calf-extension |
| `lfcom_insignia_cp` | Life Fitness US product page: insignia series chest press | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-chest-press |
| `lfcom_insignia_glute` | Life Fitness US product page: insignia series glute | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-glute |
| `lfcom_insignia_haa` | Life Fitness US product page: insignia series hip abductor adductor | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-hip-abductor-adductor |
| `lfcom_insignia_le` | Life Fitness US product page: insignia series leg extension | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-leg-extension |
| `lfcom_insignia_pd` | Life Fitness US product page: insignia series pulldown | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-pulldown |
| `lfcom_insignia_pfrd` | Life Fitness US product page: insignia series pectoral fly rear deltoid | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-pectoral-fly-rear-deltoid |
| `lfcom_insignia_row` | Life Fitness US product page: insignia series row | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-row |
| `lfcom_insignia_slc` | Life Fitness US product page: insignia series seated leg curl | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-seated-leg-curl |
| `lfcom_insignia_sp` | Life Fitness US product page: insignia series shoulder press | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-shoulder-press |
| `lfcom_insignia_te` | Life Fitness US product page: insignia series triceps extension | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-triceps-extension |
| `lfcom_insignia_tr` | Life Fitness US product page: insignia series torso rotation | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/selectorized/insignia-series-torso-rotation |
| `lfcom_lf_acc` | Life Fitness US product page: adjustable cable crossover | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/cable-machines-functional-trainers/adjustable-cable-crossover |
| `lfcom_lf_backext` | Life Fitness US product page: life fitness back extension | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/benches/life-fitness-back-extension |
| `lfcom_lf_llp` | Life Fitness US product page: life fitness linear leg press | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/plate-loaded/life-fitness-linear-leg-press |
| `lfcom_lf_oly_decline` | Life Fitness US product page: life fitness olympic decline bench | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/benches/life-fitness-olympic-decline-bench |
| `lfcom_lf_oly_incline` | Life Fitness US product page: life fitness olympic incline bench | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/benches/life-fitness-olympic-incline-bench |
| `lfcom_lf_squat_rack` | Life Fitness US product page: life fitness olympic squat rack | Life Fitness / Hammer Strength |  | https://www.lifefitness.com/en-us/catalog/strength-training/benches/life-fitness-olympic-squat-rack |
| `lfshop_axiom_ab` | Life Fitness shop spec table: axiom-series-abdominal | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/axiom-series-abdominal |
| `lfshop_axiom_bc` | Life Fitness shop spec table: axiom-series-biceps-curl | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/axiom-series-biceps-curl |
| `lfshop_axiom_cp` | Life Fitness shop spec table: axiom-series-chest-press | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/axiom-series-chest-press |
| `lfshop_axiom_haa` | Life Fitness shop spec table: axiom-series-hip-abductor-adductor | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/axiom-series-hip-abductor-adductor |
| `lfshop_axiom_lcle` | Life Fitness shop spec table: axiom-series-leg-curl-extension | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/axiom-series-leg-curl-extension |
| `lfshop_axiom_le` | Life Fitness shop spec table: axiom-series-leg-extension | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/axiom-series-leg-extension |
| `lfshop_axiom_lp` | Life Fitness shop spec table: axiom-series-leg-press | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/axiom-series-leg-press |
| `lfshop_axiom_pd` | Life Fitness shop spec table: axiom-series-pulldown | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/axiom-series-pulldown |
| `lfshop_axiom_pdrow` | Life Fitness shop spec table: axiom-series-pulldown-row | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/axiom-series-pulldown-row |
| `lfshop_axiom_pfrd` | Life Fitness shop spec table: axiom-series-pectoral-fly-rear-deltoid | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/axiom-series-pectoral-fly-rear-deltoid |
| `lfshop_axiom_row` | Life Fitness shop spec table: axiom-series-seated-row-1 | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/axiom-series-seated-row-1 |
| `lfshop_axiom_slcle` | Life Fitness shop spec table: axiom-series-seated-leg-curl-extension | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/axiom-series-seated-leg-curl-extension |
| `lfshop_axiom_smith` | Life Fitness shop spec table: axiom-series-smith-rack | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/axiom-series-smith-rack |
| `lfshop_axiom_sp` | Life Fitness shop spec table: axiom-series-shoulder-press | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/axiom-series-shoulder-press |
| `lfshop_axiom_te` | Life Fitness shop spec table: axiom-series-triceps-extension | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/axiom-series-triceps-extension |
| `lfshop_hs_2tier` | Life Fitness shop spec table: hammer-strength-two-tier-dumbbell-rack | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-two-tier-dumbbell-rack |
| `lfshop_hs_3tier` | Life Fitness shop spec table: hammer-strength-three-tier-dumbbell-rack | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-three-tier-dumbbell-rack |
| `lfshop_hs_arm_curl` | Life Fitness shop spec table: hammer-strength-seated-arm-curl | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-seated-arm-curl |
| `lfshop_hs_backext` | Life Fitness shop spec table: hammer-strength-back-extension | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-back-extension |
| `lfshop_hs_belt` | Life Fitness shop spec table: hammer-strength-plate-loaded-belt-squat | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-belt-squat |
| `lfshop_hs_cdl` | Life Fitness shop spec table: hammer-strength-chin-dip-leg-raise | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-chin-dip-leg-raise |
| `lfshop_hs_flat` | Life Fitness shop spec table: hammer-strength-flat-bench | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-flat-bench |
| `lfshop_hs_fp_gh` | Life Fitness shop spec table: hammer-strength-fixed-pad-glute-ham-bench | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-fixed-pad-glute-ham-bench |
| `lfshop_hs_gh_rh` | Life Fitness shop spec table: hammer-strength-glute-ham-reverse-hyper-combo | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-glute-ham-reverse-hyper-combo |
| `lfshop_hs_glute_drive` | Life Fitness shop spec table: hammer-strength-plate-loaded-glute-drive | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-glute-drive |
| `lfshop_hs_hack` | Life Fitness shop spec table: hammer-strength-plate-loaded-hack-squat | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-hack-squat |
| `lfshop_hs_id_half` | Life Fitness shop spec table: hammer-strength-hd-elite-id-half-rack | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-hd-elite-id-half-rack |
| `lfshop_hs_ilbp` | Life Fitness shop spec table: hammer-strength-plate-loaded-iso-lateral-bench-press | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-iso-lateral-bench-press |
| `lfshop_hs_ilfp` | Life Fitness shop spec table: hammer-strength-plate-loaded-iso-lateral-front-lat-pulldown | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-iso-lateral-front-lat-pulldown |
| `lfshop_hs_ilhbp` | Life Fitness shop spec table: hammer-strength-plate-loaded-iso-lateral-horizontal-bench-press | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-iso-lateral-horizontal-bench-press |
| `lfshop_hs_ilhr` | Life Fitness shop spec table: hammer-strength-iso-lateral-high-row | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-iso-lateral-high-row |
| `lfshop_hs_illr` | Life Fitness shop spec table: hammer-strength-plate-loaded-iso-lateral-low-row | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-iso-lateral-low-row |
| `lfshop_hs_ilrow` | Life Fitness shop spec table: hammer-strength-plate-loaded-iso-lateral-row | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-iso-lateral-row |
| `lfshop_hs_ilsp` | Life Fitness shop spec table: hammer-strength-plate-loaded-iso-lateral-shoulder-press | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-iso-lateral-shoulder-press |
| `lfshop_hs_llp` | Life Fitness shop spec table: hammer-strength-plate-loaded-linear-leg-press | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-linear-leg-press |
| `lfshop_hs_mab` | Life Fitness shop spec table: hammer-strength-multi-adjustable-bench | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-multi-adjustable-bench |
| `lfshop_hs_mts_cp` | Life Fitness shop spec table: hammer-strength-mts-iso-lateral-chest-press | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-mts-iso-lateral-chest-press |
| `lfshop_hs_mts_hr` | Life Fitness shop spec table: hammer-strength-mts-iso-lateral-high-row | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-mts-iso-lateral-high-row |
| `lfshop_hs_mts_row` | Life Fitness shop spec table: hammer-strength-mts-iso-lateral-row-1 | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-mts-iso-lateral-row-1 |
| `lfshop_hs_mts_sp` | Life Fitness shop spec table: hammer-strength-mts-iso-lateral-shoulder-press | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-mts-iso-lateral-shoulder-press |
| `lfshop_hs_nx_half` | Life Fitness shop spec table: hammer-strength-hd-athletic-nx-half-rack | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-hd-athletic-nx-half-rack |
| `lfshop_hs_nx_power` | Life Fitness shop spec table: hammer-strength-hd-athletic-nx-power-rack | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-hd-athletic-nx-power-rack |
| `lfshop_hs_pendulum` | Life Fitness shop spec table: hammer-strength-plate-loaded-pendulum-x-squat-1 | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-pendulum-x-squat-1 |
| `lfshop_hs_pl_calf` | Life Fitness shop spec table: hammer-strength-plate-loaded-seated-calf-raise | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-seated-calf-raise |
| `lfshop_hs_select_ab` | Life Fitness shop spec table: hammer-strength-select-abdominal-crunch | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-select-abdominal-crunch |
| `lfshop_hs_select_adc` | Life Fitness shop spec table: hammer-strength-select-assist-dip-chin | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-select-assist-dip-chin |
| `lfshop_hs_select_bc` | Life Fitness shop spec table: hammer-strength-select-biceps-curl | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-select-biceps-curl |
| `lfshop_hs_select_be` | Life Fitness shop spec table: hammer-strength-select-back-extension | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-select-back-extension |
| `lfshop_hs_select_cp` | Life Fitness shop spec table: hammer-strength-select-chest-press | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-select-chest-press |
| `lfshop_hs_select_hab` | Life Fitness shop spec table: hammer-strength-select-hip-abduction | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-select-hip-abduction |
| `lfshop_hs_select_hc` | Life Fitness shop spec table: hammer-strength-select-horizontal-calf | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-select-horizontal-calf |
| `lfshop_hs_select_hg` | Life Fitness shop spec table: hammer-strength-select-hip-and-glute | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-select-hip-and-glute |
| `lfshop_hs_select_lc` | Life Fitness shop spec table: hammer-strength-select-leg-curl | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-select-leg-curl |
| `lfshop_hs_select_le` | Life Fitness shop spec table: hammer-strength-select-leg-extension | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-select-leg-extension |
| `lfshop_hs_select_pd` | Life Fitness shop spec table: hammer-strength-select-lat-pulldown | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-select-lat-pulldown |
| `lfshop_hs_select_pfrd` | Life Fitness shop spec table: hammer-strength-select-pectoral-fly-rear-deltoid | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-select-pectoral-fly-rear-deltoid |
| `lfshop_hs_select_row` | Life Fitness shop spec table: hammer-strength-select-seated-row | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-select-seated-row |
| `lfshop_hs_select_sc` | Life Fitness shop spec table: hammer-strength-select-standing-calf | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-select-standing-calf |
| `lfshop_hs_select_slc` | Life Fitness shop spec table: hammer-strength-select-seated-leg-curl | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-select-seated-leg-curl |
| `lfshop_hs_select_slp` | Life Fitness shop spec table: hammer-strength-select-seated-leg-press | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-select-seated-leg-press |
| `lfshop_hs_select_sp` | Life Fitness shop spec table: hammer-strength-select-shoulder-press | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-select-shoulder-press |
| `lfshop_hs_select_te` | Life Fitness shop spec table: hammer-strength-select-triceps-extension | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-select-triceps-extension |
| `lfshop_hs_smith` | Life Fitness shop spec table: hammer-strength-smith-machine-1 | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-smith-machine-1 |
| `lfshop_hs_tbar` | Life Fitness shop spec table: hammer-strength-plate-loaded-t-bar-row | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-t-bar-row |
| `lfshop_hs_vsmith` | Life Fitness shop spec table: hammer-strength-plate-loaded-vertical-smith-machine | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-vertical-smith-machine |
| `lfshop_hs_vsquat` | Life Fitness shop spec table: hammer-strength-plate-loaded-v-squat | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/hammer-strength-plate-loaded-v-squat |
| `lfshop_insignia_glute_bridge` | Life Fitness shop spec table: insignia-series-glute-bridge | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/insignia-series-glute-bridge |
| `lfshop_insignia_lc` | Life Fitness shop spec table: insignia-series-leg-curl | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/insignia-series-leg-curl |
| `lfshop_insignia_lp` | Life Fitness shop spec table: insignia-series-leg-press | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/insignia-series-leg-press |
| `lfshop_lf_2tier` | Life Fitness shop spec table: life-fitness-two-tier-dumbbell-rack | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/life-fitness-two-tier-dumbbell-rack |
| `lfshop_lf_3tier_long` | Life Fitness shop spec table: life-fitness-3-tier-long-saddle-dumbbell-rack-5-75 | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/life-fitness-3-tier-long-saddle-dumbbell-rack-5-75 |
| `lfshop_lf_3tier_short` | Life Fitness shop spec table: life-fitness-3-tier-short-saddle-dumbbell-rack-5-50 | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/life-fitness-3-tier-short-saddle-dumbbell-rack-5-50 |
| `lfshop_lf_adj_bench` | Life Fitness shop spec table: life-fitness-adjustable-bench | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/life-fitness-adjustable-bench |
| `lfshop_lf_arm_curl` | Life Fitness shop spec table: life-fitness-arm-curl-bench | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/life-fitness-arm-curl-bench |
| `lfshop_lf_barbell_rack` | Life Fitness shop spec table: life-fitness-barbell-rack | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/life-fitness-barbell-rack |
| `lfshop_lf_cdl` | Life Fitness shop spec table: life-fitness-chin-dip-leg-raise | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/life-fitness-chin-dip-leg-raise |
| `lfshop_lf_dap` | Life Fitness shop spec table: life-fitness-dual-adjustable-pulley | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/life-fitness-dual-adjustable-pulley |
| `lfshop_lf_dlr` | Life Fitness shop spec table: life-fitness-dip-leg-raise | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/life-fitness-dip-leg-raise |
| `lfshop_lf_flat` | Life Fitness shop spec table: life-fitness-flat-bench | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/life-fitness-flat-bench |
| `lfshop_lf_mab` | Life Fitness shop spec table: life-fitness-multi-adjustable-bench | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/life-fitness-multi-adjustable-bench |
| `lfshop_lf_oly_flat` | Life Fitness shop spec table: signature-series-olympic-flat-bench | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/signature-series-olympic-flat-bench |
| `lfshop_lf_smith` | Life Fitness shop spec table: life-fitness-smith-machine | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/life-fitness-smith-machine |
| `lfshop_lf_universal` | Life Fitness shop spec table: life-fitness-universal-cable | Life Fitness / Hammer Strength |  | https://shop.lifefitness.com/products/life-fitness-universal-cable |
| `matrix_mabr1` | Matrix MABR1 bench owner's manual (Rev 1.1) - training area / free area diagram, clearance note | Matrix Fitness / Johnson Health Tech | 2023 | https://cdn.shopify.com/s/files/1/0554/8795/5111/files/Bench_Manual.pdf |
| `nsca_checklist` | NSCA's Safety Checklist for Exercise Facility and Equipment Maintenance | National Strength and Conditioning Association |  | https://www.nsca.com/contentassets/2a0a87ccabbe4a149dd915168b20d603/nsca-safety-checklist.pdf |
| `nsca_standards_2017` | NSCA Strength and Conditioning Professional Standards and Guidelines (Strength Cond J 39(6)), Appendix 4 Table D1 'Calculations for space needs' | National Strength and Conditioning Association | 2017 | https://www.nsca.com/globalassets/education/nsca_strength_and_conditioning_professional_standards_and_guidelines.pdf |
| `nsca_tsac` | NSCA TSAC Module 5.0-5.1 Facility guidelines (slides) | National Strength and Conditioning Association | 2018 | https://www.nsca.com/contentassets/4bc4e495944c470d81c429294a2b4c05/tsac-module-5.0--5.1.pdf |
| `rep_ab5200` | REP Fitness AB-5200 2.0 Adjustable Bench | REP Fitness |  | https://repfitness.com/products/ab-5200-2-0 |
| `rep_commercial_dbr` | REP Fitness Commercial Dumbbell Rack (2- and 3-tier variants) | REP Fitness |  | https://repfitness.com/products/commercial-dumbbell-rack |
| `rep_fb5000` | REP Fitness FB-5000 Competition Flat Bench | REP Fitness |  | https://repfitness.com/products/fb-5000-competition-flat-bench |
| `rep_ghd` | REP Fitness Glute Ham Developer (GHD) | REP Fitness |  | https://repfitness.com/products/ghd-glute-ham-developer |
| `rep_landmine` | REP Fitness Free Standing Landmine | REP Fitness |  | https://repfitness.com/products/free-standing-landmine |
| `rep_victory_2tier` | REP Fitness Victory 2-Tier Dumbbell Rack | REP Fitness |  | https://repfitness.com/products/victory-2-tier-dumbbell-rack |
| `rfa_sportsart` | SportsArt DS972 Dual Stack Functional Trainer (dealer listing) | Recovery For Athletes |  | https://www.recoveryforathletes.com/products/sportsart-ds972-status-dual-stack-functional-trainer |
| `rogue_3tier_dbr` | Rogue 3-Tier Dumbbell Rack product page | Rogue Fitness |  | https://www.roguefitness.com/rogue-3-tier-dumbbell-rack |
| `rogue_ab3` | Rogue Adjustable Bench 3.0 product page | Rogue Fitness |  | https://www.roguefitness.com/rogue-adjustable-bench-3-0 |
| `rogue_abram_ghd` | Rogue Abram GHD product page | Rogue Fitness |  | https://www.roguefitness.com/rogue-abram-ghd |
| `rogue_flat2` | Rogue Flat Utility Bench 2.0 product page | Rogue Fitness |  | https://www.roguefitness.com/rogue-flat-utility-bench-2-0 |
| `rogue_hr2` | Rogue HR-2 Half Rack product page | Rogue Fitness |  | https://www.roguefitness.com/rogue-hr-2-half-rack |
| `rogue_ohio_bar` | Rogue Ohio Bar product page (bar length / sleeve) | Rogue Fitness |  | https://www.roguefitness.com/the-ohio-bar-black-zinc |
| `rogue_r3` | Rogue R-3 Power Rack product page | Rogue Fitness |  | https://www.roguefitness.com/rogue-r-3-power-rack |
| `rogue_rml490` | Rogue RML-490 Power Rack product page | Rogue Fitness |  | https://www.roguefitness.com/rogue-rml-490-power-rack |
| `rogue_westside` | Rogue Westside Bench 2.0 product page | Rogue Fitness |  | https://www.roguefitness.com/rogue-westside-bench-2-0 |
| `startrac_ipl5002` | Star Trac IP-L5002 owner's manual, p.19 (clearance & walkway) | Star Trac (via ManualsOnline) |  | https://videogame.manualsonline.com/manuals/mfg/star_trac/ipl5002.html?p=19 |
