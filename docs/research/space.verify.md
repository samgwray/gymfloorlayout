# Verification log: space slice (clearances, aisles, zoning, ceilings, flooring)

- Checked 2026-10-28 by an adversarial fact-checker.
- **Method.** I re-downloaded every cited PDF from its URL into `scratchpad/verify_space/dl/` and extracted the text with pdftotext (text is in `scratchpad/verify_space/txt/`). The sources covered:
  - Precor TRM 800 and TRM 885 v2
  - LF T-series
  - Star Trac 10TRx
  - Matrix 17208
  - Matrix cycles and R7xe
  - Keiser M3i
  - NuStep T5
  - AirRunner
  - Technogym Run Personal
  - StairMaster 8Gx
  - Core 2026 catalog
  - ADA 2010
  - NSCA checklist and TSAC
  - CCTS ISO report
  - ISO preview
- HTML pages were fetched with curl and converted to text (`verify_space/html/`). Shopify product JSON was used for prices (`verify_space/shop/`).
- **Rendered images.** I viewed the UFC worksheet images (pp. 083–087) and rendered the figures on the Star Trac and Technogym clearance pages (`verify_space/img/`).
- **Fetched with WebFetch** (curl was blocked): ManualsLib T3xe, HFA, Sadler, Sekendiz, Corada DOJ guidance, Rush Walter. Athletic Business returned 403 everywhere.

## Bottom line
- **Transcription is accurate.** Every quoted value I opened matched its source.
- **No number was invented.** The NSCA Standards 2017 citation URL (`http://www.nsca-scj.com`) is not a document URL. The real PDF is https://www.nsca.com/globalassets/education/nsca_strength_and_conditioning_professional_standards_and_guidelines.pdf, and its Table D1 confirms 90, 40, 130 and 144 ft².
- **Corrections (derived values):**
  1. **Stair-climber clearance is too small** (rear 24 in).
     - LF PowerMill Integrity manual: "Keep a distance of at least 3 ft. (1 m) behind and 1 ft. (0.3 m) on each side".
     - StairMaster 10G manual (mirror text seen only via search): 20 in sides and 48 in (1.25 m) front and behind.
     - The 8Gx envelope of 33 sq ft should therefore be about 39 sq ft (LF rule) to about 58–79 sq ft (StairMaster 10G rule).
  2. **Treadmill front clearance of 0 in is contradicted by two manufacturer figures.**
     - The Technogym Run Personal figure shows 60 cm in front of the console. So does the Star Trac 10TRx "Required Clearance" figure (0.6 m).
     - The 0 rests only on Precor and ASTM being silent about the front. Use 24 in where a console faces a wall or another row.
- **Unsupported:** `ihrsa2017.sqft_per_member` (9–15 sq ft).
  - Its only source is an anonymous Brainscape flashcard, which says "per person", not per member.
  - The IHRSA report itself is paywalled, and a search found no IHRSA sq-ft-per-member figure.
  - ACSM 4th ed. (via IDEA) gives 10–14 sq ft per member, which is verified. Use that instead.
- **Caveats on confirmed items:**
  - The Star Trac sheet's text says 39.4 in (1.0 m) per side, but its own figure labels the sides 23.6 in (0.6 m). "Strict mode 39.4 in" rests on text that conflicts with the figure.
  - ACSM 3rd ed. "25–50 sq ft per piece":
    - Fit Supply states the value without an edition.
    - The Athletic Business page (403) is attributed to the 3rd ed. (2006) only through search summaries.
    - Athletic Business "Custom Fit" reportedly quotes ACSM as 20–40 sq ft per cardio piece.
  - NSCA rack: 130 ft² assumes no sharing. NSCA's own 3-ft bar-end spacing implies about 100 ft² per rack in a row. This is inconsistent with the bench handling (90 in rows).
  - Rework's "18 in acceptable for code" is not a code value. ASTM/EN require 0.5 m (19.7 in).
  - Sekendiz reports "60% (n = 6)". 6 of 11 is 55%; the source has the inconsistency, not the researcher.

## Datapoint checks (selected for optimizer influence and suspicion)

| Datapoint | Verdict | Source evidence |
|---|---|---|
| astm_f2115_12.rear_in / side_in | confirmed | CPH: 2012 standard "0.5 m (19.7 inches) on each side … 2 m (78 inches) behind". Precor TRM800 p.~10: "as of October 1, 2012 … 0.5 m (19.7 in.) on each side … 2 m (78 in.) behind". AirRunner: 2.0 m (79.0 in.) behind. |
| treadmill.recommended_rear_in (79 × width) | confirmed (note) | Matrix T3xe: "at least the width of the treadmill and at least 79″ (2 meters) long". LF, Matrix commercial and Technogym specify 1 m wide, so use max(unit width, 39.4 in). |
| treadmill.recommended_side_in (24) | confirmed | Matrix T3xe: "at least 24″ (0.6 meters)" on both sides. Precor and ASTM: 19.7 in. |
| treadmill.recommended_front_in (0) | **corrected → 24 in** | Technogym figure: 60 cm in front. Star Trac figure: 0.6 m arrow at the front corner. Precor and ASTM are silent. |
| startrac.treadmill_clear_in | confirmed (conflict) | Text: 39.4 in each side, 78.8 in behind. The figure on the same page labels the sides 23.6 in (0.6 m). |
| lf.treadmill_rear_zone; matrix.treadmill_landing_zone; technogym.treadmill_free_space | confirmed | LF: "six feet (2 meters) by three feet (1 meter) behind". Matrix 17208: "78.75″ (2000 mm) x 39.50″ (1000 mm) landing zone". Technogym: "free space of 2x1 m"; the figure shows 200 × 100 cm behind and 60 cm on the sides and front. |
| precor.other_cardio_clear | confirmed | "0.5 m (19.7 in.) on at least one side, and 0.5 m (19.7 in.) behind or in front". |
| iso20957_1.free_area_m / area_definitions | confirmed | CCTS210727002SX p.8, clause 5.17 d), verbatim. ISO preview 3.2 and 3.4, verbatim. |
| keiser / matrix_cycles / matrix_r7xe / nustep / airrunner clearances | confirmed | All quotes verbatim in the downloaded manuals. Keiser footprint 51 × 26 in. |
| c2.rower_use_area; c2.bikeerg_use_area; c2.skierg_dims | confirmed | concept2.com: 9 × 4 ft; 60 × 48 in; 23.5 × 50 × 85 in. |
| stair_climber.recommended_clear_in | **corrected** | LF PowerMill manual: 1 m (39 in) behind, 0.3 m on each side, 9 ft ceiling. StairMaster 10G (mirror): 0.5 m sides, 1.25 m front and rear. |
| stair_climber.envelope_example_sqft (33) | **corrected → ≈39–79** | 8Gx 58 × 34 in: (58+39)×(34+24)/144 = 39.1 sq ft. With the StairMaster 10G rule: (58+96)×(34+40)/144 = 79.1 sq ft standalone, 57.8 sq ft in a row. |
| treadmill / indoor_cycle envelope examples | confirmed | Inputs (Precor brochure 211 × 89 cm; Keiser 51 × 26 in) and arithmetic check out. |
| nsca.machine_gap_in / aerobic / freeweight / bar_end | confirmed | NSCA checklist (ESTC 4th ed., 2016) verbatim: 2 ft minimum, 3 ft optimal; Olympic bars 3 ft between ends. |
| nsca_std.bench / standing / rack / platform | confirmed, better URL | NSCA SCJ 39(6), Table D1: 90, 40, 130 and 144 ft². |
| nsca_tsac.bench_station_sqft (156) | confirmed | "(6 + 3 + 3) x (7 + 3 + 3) = 156 ft2". |
| power_rack.recommended_area_sqft (130) | confirmed (caveat) | Correct as isolated. In rows, the 3-ft end cushions can be shared, giving about 100 sq ft. |
| rig.* (floor space, height) | confirmed | Core 2026 catalog: FSS 60 × 54 in → 14 × 14 ft; PTC 24 × 26 ft; XTC 14×12 / 14×14 / 18×12 / 14×24 / 14×34 / 14×44 ft; height 105 in. |
| acsm4.* (40–60 per piece, 10–14 per member, 3-ft buffer, 40–60 per group-ex user) | confirmed | IDEA (May 23, 2013; updated Aug 11, 2023) citing ACSM 2012 4th ed., verbatim. |
| acsm3.equip_area_sqft | confirmed (weak) | Fit Supply: "ACSM allows 25 to 50 sq ft per station" (no edition). Athletic Business returned 403. |
| ihrsa2017.sqft_per_member | **unsupported** | Flashcard only; says "per person". |
| ufc.cardio / selectorized / freeweight / stretch / group_ex | confirmed | UFC 4-740-02 Fig. B-1: 50, 50 and 65 sf per station; stretching 50 sf per person (minimum 2 people); group exercise 50 sf per person, minimum 1,250 ft². |
| ufc.ceiling_ft; ufc.floor_*; ufc.mirrors; ufc.wall_protection_in | confirmed | Table 4-25, verbatim. |
| ufc_ws.* (zone %, net/gross shares) | confirmed | Worksheet images: 5 × 50 = 250; 80 × 50 = 4,000; 46 × 50 = 2,300; 80 × 65 = 5,200. Lobby 2,485; support 2,628; admin 1,372 + 125 + 375. Lockers 3,456 / 2,524. 77,903 net → 93,484 gross at 0.2. |
| ufc.office_sqft | confirmed (note) | The 120 / 100 / 64 ft² offices are listed under "Core HAWC Spaces" and "Administrative Spaces". |
| ada.* (305.3, 403.5.1, 403.5.3, 236.1, 206.2.13, 1004.1, 225.2.1, 903.3, 604.3.1, 608.2.1) | confirmed | ADA 2010 PDF, verbatim. DOJ guidance (Corada): CFS "in the aisle behind the device". |
| nsca_tsac.passageway / hallway / ceiling / mirror / floor_by_zone | confirmed | TSAC Module 5.0 table, verbatim. |
| stairmaster / 4G / Jacobs / PowerMill ceilings; treadmill.step_up_in | confirmed | Core catalog: 10 ft; 8 ft; 7.5 / 8.5 ft; step-up 7–11 in. LF: "Ceiling Height Required 9' (2.7m)". |
| ceiling.treadmill_min_ft (EST 9) | confirmed derivation | 76 + 11 + 6 + 4 + 6 = 103 in. Consistent with PowerMill's 9 ft. |
| zone.normalized_mean; zone.recommended_mainstream | confirmed (arithmetic) | Rework, Dynamo, Glofox and UFC inputs verified. The means of 36.6 / 52.0 / 9.0 / 2.5 recompute. These are weak priors (1 military program + 3 blogs). |
| support.training_share_micro (EST 0.80) | confirmed derivation | 2 × 64 + 120 + 80 = 328 sq ft. That is 22% of 1,500 sq ft and 13% of 2,500 sq ft. No plumbing-code basis. |
| sekendiz / jimenez / sadler / redwoods / truefitness / skelcore / rework / rushwalter | confirmed | All verbatim. Caveats noted above. |
| greatmats (thickness, starting prices, Geneva $2.21 / $2.76), dgfloors (all ranges, install $1.50–3, turnkey), bos 6 mm limit | confirmed | All verbatim. |
| hs / hoist / titan / bos platforms; Guardian $28 (22.5 × 22.5 in); Gorilla $99; BoS roll $999.99; THOR $2.58 / $2.77 | confirmed | Shopify product JSON. |

## Missing for the optimizer (details in the structured output)
- NSCA Standards: 100 ft² per participant at peak and up to 3 participants per station.
- ADA 305.7 alcove widths: 36 in (forward approach) and 60 in (parallel approach).
- Stepmill and elliptical clearances from citable manuals.
- IBC egress: exits, travel distance, egress width.
- IPC plumbing-fixture counts.
- Floor live load.
- Treadmill dedicated circuits.
- Per-machine training areas for strength and cable equipment.
- Current-edition ISO 20957-1:2024, 20957-6 and ACSM 5th ed. text.
- Sled-lane length.
