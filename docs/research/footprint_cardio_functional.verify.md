# Verification log: footprint_cardio_functional

Checked 2026-10-28 by an adversarial fact-checker. Each check opened the cited page or PDF. PDFs were downloaded and searched as text with `pdftotext`. The shared WebSearch budget ran out partway through, so the only datapoint that rests on search-result snippets is the Matrix Performance treadmill. Its retailer pages returned 403.

## Verdict summary

* 39 datapoints checked: 38 confirmed, 1 corrected, 0 unsupported, 0 unreachable. The researcher's quotes came out verbatim or near-verbatim every time.
* All the 75th-percentile footprint derivations reproduce when recomputed (numpy linear interpolation): treadmill 82.75, upright 48.9, recumbent 67, spin 52.75, stair 60.5, rower width 25.25, curved 69.8 (still 70 with the HIITMill X added).
* **One correction:** `elliptical.footprint_length_in`. The sample left out the Star Trac Rear Drive Elliptical 8RDE (86 x 36 x 73 in), which appears on the same Core 2026 catalog page (the Climb Elliptical 8CE is also 86 x 36 x 73). With the 8RDE added, the 75th percentile is **86**, not 82.8. LF Integrity has an **87 in active length**. Use **87**.

## Checks (most influential first)

| id | claimed | verdict | evidence found |
|---|---|---|---|
| treadmill.clearance_back_in | 79 | confirmed | Matrix T3xe: "a clear zone behind the treadmill that is at least the width of the treadmill and at least 79" (2 meters) long"; Cybex 525T "78.7 inches (2.0 meters) behind"; Precor P30 "2 m (78 in.) behind"; AirRunner "2.0 m (79.0 in.) behind" |
| treadmill.clearance_left/right_in | 20 | confirmed | Precor P30 "0.5 m (19.7 in.) on each side"; Cybex "19.7 inches (0.5 meters) on the sides"; Matrix "at least 24" (0.6 meters)" |
| treadmill.clearance_src.matrix_t3xe | rear 79 x width; sides 24 | confirmed | verbatim on manualslib p.10 |
| treadmill.clearance_src.cybex_525t | 19.7 / 78.7 | confirmed | verbatim on manualsdir p.13 |
| treadmill.power_circuit | dedicated 120V/20A per unit | confirmed | LF Atmos "single dedicated circuit breaker per unit", "120V, 20A or 230V, 10A"; Precor "120V/20A individual branch circuit"; Star Trac "110V/20 Amp dedicated circuit with NEMA 5-20 outlet; or 220V/15 Amp ... NEMA 6-15" |
| treadmill.lf_integrity_plus.dims_in | 82 x 36 x 56 | confirmed | LF page; 434 lb; 400 lb user; step-up 8 in |
| treadmill.precor_trm885.dims_in | 83 x 35 x 68 | confirmed | precor.com; brochure 211 x 89 x 173 cm, 181 kg |
| treadmill.startrac_8trx.dims_in | 81 x 35.5 x 60 | confirmed | corehandf page; 465 lb; 500 lb user |
| treadmill.matrix_performance.dims_in | 86.7 x 36.5 x 66.3 | confirmed (weak) | Search listings (Johnson Fitness, Progym) give 220.2 x 92.6 x 168.5 cm, 400 lb. The cited Matrix page renders no text, and the retailer pages return 403. |
| treadmill.footprint_length_in | 84 | confirmed (estimate) | 75th percentile 82.75. Note that the Matrix unit (86.7) does not fit in 84. |
| curved_treadmill.clearance_front/back_in | 20 / 79 | confirmed | AirRunner manual: "0.5 m (19.7 in.) to the left, right and front, and 2.0 m (79.0 in.) behind" (ASTM + EN, March 1, 2017) |
| curved_treadmill.trueform_runner.dims_in | 64x31x63 / 64x36x63 | confirmed | Rogue 64 x 31 x 63, 700 lb, $6,595; Iron Co 64 x 36 x 63, "700 lbs. walking / 450 lbs. running" |
| curved_treadmill.woodway_curve_ltg.dims_in | 67 x 34 x 70 | confirmed | Rogue page. The $3,495 price is shown beside $3,995, so it may be a sale price. |
| **elliptical.footprint_length_in** | 84 | **corrected: 87** | Core 2026 catalog: Star Trac 8RDE 86 x 36 x 73 in (left out of the sample); LF Integrity active length 87 |
| elliptical.clearance_front_in | 12 | confirmed | LF CLSX: "Allow 1 foot of clearance in front ... and at least 2 ft. (0.6 m) on the side" |
| elliptical.clearance_src.lf_clsx_rear_warning | 6.5 x 3 ft | confirmed | the WARNING text is verbatim, so treating it as an outlier is a judgement call |
| elliptical.precor_efx885.dims_in | 80 x 28 x 71 | confirmed | precor.com: "80 x 28 x 71 in / 203 x 71 x 180 cm" |
| elliptical.lf_integrity.dims_in | 86 x 29 x 63.5; active 87 | confirmed | LF page |
| cardio.clearance_src.precor_general | 19.7 one side + front or back | confirmed | verbatim |
| upright_bike.clearance_left_in | 24 | confirmed | Matrix Performance cycles: "leave a clear zone on both sides ... at least 24" (600 mm)"; diagram shows 0.6 m FREE AREA. Matrix 7xe manual adds: "Please leave a 24" (610 mm) behind the cycle and on one side", with 1' (305 mm) in its diagram. |
| recumbent_bike.clearance_front_in | 12 | confirmed, with caveat | The CLSR text does say "Allow 1 foot of clearance in front". The same manual's WARNING says "at least 3 ft. (0.9 m) between the front or rear ... to any other objects", and its setup diagram labels 3 ft (1 m) at front and rear. |
| indoor_cycle clearances | 24 all sides, shareable | confirmed | Keiser M3i: "24 inches (610 mm) on all sides ... When bikes are positioned adjacent to each other, the free area may be shared." (EN ISO 20957-1 Class S) |
| indoor_cycle.sport_england_spin_area | 1.0-1.5 m2 + 1.25x | confirmed | Sport England space table |
| rower.concept2.use_space_in | 9 x 4 ft | confirmed | concept2.com "Space With Clearance for use: 9 ft x 4 ft (274 cm x 122 cm)" |
| rower.concept2.max_user_lb | 500 | confirmed, with note | "500 lb (227 kg) as tested by Concept2". The same page also gives "300 lb (135 kg) as tested per ... EN 20957-7", which the researcher left out. |
| bikeerg.concept2.use_space_in | 60 x 48 on 48 x 24 | confirmed | concept2.com |
| ski_erg.footprint_length_in | 50 (floor stand) | confirmed | "23.5 in x 50 in x 85 in"; no max user weight listed |
| recumbent_stepper clearances | 12 front/rear, 24 sides | confirmed | NuStep T5 manual Rev N: "24 inches (61 cm) for the sides, and 12 inches (30 cm) for the front and rear. Additional free space is necessary to accommodate wheelchair access." |
| stair_climber.min_ceiling_in | 120 | confirmed | 8Gx page: "Recommended Ceiling Height: 10' (3.05m)"; PowerMill "9' (2.7m)" |
| stair_climber.stairmaster_8gx.dims_in | 58 x 34 x 79 | confirmed | corehandf page; 509 lb; 400 lb user; 12V/5A |
| air_bike.assault_elite.dims_in | 55.08x26.26x55 (alt 47.9x26.2x56) | confirmed | Both sets appear on assaultfitness.com: the specs block, and the FAQ/compare table |
| rig_bay.throwdown_xtc.rec_floor_space | 14x12 ... 14x44 ft | confirmed | Core 2026 catalog p.96-97. The "+10 ft per dimension" rule holds for all 6 configurations. 4' Core is 46 x 48 x 105 in. |
| rig_bay.hs_hd_perimeter.training_space | 123.75 x (W+48) | confirmed | The LF page calls it "Recommended Live Area (Single Side)", not "training space". The values match. |
| heavy_bag.throwdown.area_per_bag | 30.6-66.5 ft2 | confirmed | 22' x 50' / 36 bags; 19' x 28' / 8 bags; SSTT "4' x 7'"; "BAG SPACING 4.5' (137 cm)" |
| turf_lane.torque.run_length | 30 yd optimal, 10 yd workable | confirmed | Torque FAQ, verbatim |
| turf_lane.rogue_gymturf.spec | 5 ft wide; 25/50 ft | confirmed | Rogue page; $1,089 |
| standards.sport_england_area_per_equipment_m2 | 5 m2/piece; CV 1.5-2.0 + 1.75x | confirmed | Sport England 2008 Rev 002, verbatim. Ceiling: not below 2.7 m, optimum 3.5-4 m. |
| standards.ada_clear_floor_space_in / route_width | 30x48; 36 (32 at short points) | confirmed | ADA 2010 305.3, 403.5.1 (+ exception), 1004.1, 236.1 advisory |
| stretch_area.area_per_person_m2 | 2.0-2.5 | confirmed | Sport England table |
| accessory_pack.clearance_front_in | 25 | confirmed (derived) | SYNRGY "Recommended Live Area 37" x 50" x 84"" vs footprint 36 x 25 x 67 |
| wall_ball / TRX / USS 2.0 / foam plyo / TANK M4 / Monkey Rig | various | confirmed | the figures and prices on each vendor page match |

## Issues the optimizer should know about

1. **Elliptical length is understated.** Raise it to 87 in. Width 30 stands if only the 8RDE is added. If the incline 8CE (also 86 x 36) is counted as well, the 75th-percentile width is 34.5, so 35.
2. **Recumbent and upright bike front/rear.** The LF source quoted for "front 12" also tells you to leave 3 ft front or rear. The Matrix manuals (24 in behind, 1 ft front) support 12/24, so keep 12/24 but offer 36 as a strict-LF mode.
3. **"Treadmill rear zone may overlap an aisle"** appears in the notes of `treadmill.clearance_back_in`, but no cited source says it. LF and Matrix only say the zone must be "clear of any obstruction". The aisle overlap is the researcher's interpretation, and it saves about 79 x 36 in per treadmill, so it needs to be labelled as an assumption.
4. **Matrix Performance treadmill (86.7 in long)** is now corroborated, but only by search snippets. It is 2.7 in longer than the 84 in planning footprint.
5. **Concept2 RowErg max user.** 500 lb is Concept2's own test. The EN 20957-7 rating is 300 lb.

## Missing critical data (for the optimizer)

* Manufacturer floor clearances for revolving-stair climbers (StairMaster 8Gx/10G/StepMill owner's manuals). A moving-step machine may need a treadmill-like 2 m rear zone, not the estimated 24 in.
* No manufacturer clearances for air bikes (Assault/Echo manuals) or the Concept2 SkiErg manual. The values given are 0.6 m estimates.
* A sourced rule for whether a treadmill's 2 m rear zone may overlap a circulation aisle, or another treadmill's rear zone in back-to-back rows. This needs the ASTM F2115 / ISO 20957-6 text or a vendor facility-planning guide.
* No sourced main-aisle or general-circulation widths beyond the ADA 36 in minimum. Sport England's per-machine circulation explicitly excludes "general circulation of the room". The ACSM facility standards were not accessed.
* Minimum ceiling heights for treadmills (step-up 7.5-11 in plus up to 15% incline) and ellipticals (peak pedal height), plus overhead clearance above rigs (Monkey Rig centre uprights are 12 ft) and above wall-ball targets (10 ft). Only stair climbers and Jacobs Ladder have ceiling values.
* Vendor "live area" or per-user training-zone specs for functional stations (for example LF SYNRGY360, Matrix Connexus, Precor Queenax). These would replace the low-confidence estimates for the plyo, battle-rope, TRX, wall-ball and sled zones.
* Commercial purchase prices for the core cardio items (treadmill, elliptical, upright/recumbent bike, stair climber, recumbent stepper, spin bike). This slice gives prices only for Rogue-sold functional items and a few non-motorized units, so the budget optimizer still needs these from another slice.
* Equipment weights are captured, but floor loading (lb/ft2) for upper-floor sites is not.
