# Verification log: footprint_strength (adversarial fact-check)

Checked 2026-10-28. Primary documents were re-downloaded independently (not the researcher's copies) into
a temporary research directory and searched as text (pdftotext). Web pages were read with WebFetch or as raw HTML from the Life Fitness shop and catalog.

**Result:** 0 refuted, 0 unreachable. All 26 non-estimate datapoints are confirmed verbatim. 16 estimate items had their cited manufacturer evidence spot-checked, and every number matched. Some caveats about scope and derivation are listed below.

## Non-estimate datapoints (all confirmed)

| id | value | where verified (verbatim) |
|---|---|---|
| nsca.floor_space_per_participant_sqft | 100 ft2 | NSCA 2017 Standards, Guideline 3.1: "minimum average floor space allowance per participant (100 ft2)". **Scope:** supervised school/college S&C rooms at peak usage, set alongside staff ratios. It is not a commercial-gym or fire-code density. |
| nsca.participants_per_station | up to 3 | Same doc: narrative says "(up to 3)"; Guideline 3.1 says "(3)". Same scope caveat: team rotation. |
| nsca.space_bench/standing/rack/platform | 90/40/130/144 ft2 | Table D1 "Calculations for space needs" (App. 4), verbatim formulas. 40 ft2 is the 4-ft curl-bar example; a 7-ft Olympic bar gives (7+6)x4 = 52 ft2. The full rack-station range is 88-130 ft2. |
| nsca.tsac_bench_sqft | 156 ft2 | TSAC Module 5.0: "(6 + 3 + 3) x (7 + 3 + 3) = 156 ft2" (3 ft safety space each side). |
| nsca.machine_spacing_in | 24 / 36 | NSCA checklist: "a minimum of 2 feet [61 cm] between machines; 3 feet [91 cm] is optimal". Applies to the machine, free-weight (benches) and aerobic areas. |
| nsca.bar_end_spacing_in | 36 | NSCA checklist: "Olympic bars properly spaced (3 feet [91 cm]) between ends" (free-weight and weightlifting areas). |
| nsca.ceiling_min_ft | 12 | NSCA checklist "(12 feet [3.7 m] minimum)"; TSAC "12-14 ft of clearance". |
| nsca.passageway_in / hallway_in | 36 / 60 | TSAC table "Passageways 36 in." / "Hallways 60 in."; also "Spacing/passageways - 36 in. or 3 ft". |
| nsca.mirror_offsets_in | 20 / 6 | Checklist "minimum of 20 inches [51 cm] off the floor"; TSAC "20 in. from floor, 6 in. from equipment". |
| iso20957.free_area_min_in | 23.6 in | Cybex 20040 p.7 "Minimum clearance is 23.6 inches (0.6 meters)" (also in Cybex 16140 and 16200); KingsBox p.4 "not less than 0,6 m greater than the training area". HomCom and Sportstech manuals say the same. The margin is measured beyond the **training area** (user + full ROM), not beyond the frame. The 2013 edition has been replaced by ISO 20957-1:2024; the current clause text was not verified (paywalled). |
| iso20957.free_area_shareable | yes | Cybex: "Adjacent units may share the free area."; KingsBox IT p.19 / SL p.64 / HR p.79. |
| iso20957.definitions | 3.2 / 3.4 | iTeh ISO 20957-1:2013 preview, verbatim. |
| cybex.clear_floor_other_access_in | 23 in | Cybex 20040 pp.3, 7, verbatim. |
| matrix.min_access_clearance_in | 24 in | Matrix MABR1 Rev 1.1, verbatim (0.91 m / 36 in ADA note too). |
| startrac.between_behind_in / entry_walkway_in | 24 / 36 | ManualsOnline Star Trac IP-L5002 p.19, verbatim. The 24 in is measured from the "moving arms and levers", not from the frame. |
| ada.clear_floor_space_in | 30 x 48 | 305.3, 1004.1 (overlap allowed; advisory: one space may serve two machines), 236.1, 206.2.13. **Caveat:** Cybex's "36 x 48 if enclosed on three sides" covers forward approach only. ADA 305.7.2 requires a **60 in** wide alcove for parallel approach when the alcove is more than 15 in deep. |
| ada.accessible_route_width_in | 36 | 403.5.1 verbatim. Exceptions: 32 in for at most 24 in of length; 42-48 in at 180-degree turns (403.5.2). |
| olympic_bar.length_in / sleeve_in | 86.75 / 16.40 | Rogue Ohio Bar FAQ "Exact length is 86.75""; Gear Specs '16.40" loadable sleeve length'. |
| barbell_station.live_width_in | 120 | LF Olympic Flat 91x120x51; HS Olympic Flat 75x120; HS Smith 120x120x92.8; LF Smith 120x120x93; HS NX and HS iD power racks 10'x10'; HS iD half rack 7'x10'. |
| dumbbell_rack.front_live_add_in | 36 | LF 2-tier 90x25x33 -> live 90x61x33; HS 2-tier 21x90x33 -> 57x90; HS 3-tier 27x90x39 -> 63x90. |

## Estimate items: evidence spot-checked (all numbers match the sources)

HS NX power rack D62/W65/H91 with 10'x10' live area. HS iD power rack 64x73x96 with 10'x10'. Rogue RML-490 53x53 and HR-2 48x49. HS iD half rack 56x73x96 with 7'x10'. HS and LF Smith machines. HS linear leg press 95x65x57 with live 113x89. Insignia chest press, pulldown and leg extension, with live areas. HS Select chest press 41x57x64 with live 83x57. HS IL bench press 48x67x72 with live 84x115x96. LF adjustable bench 55x25 with live 97x73. LF cable crossover 150x28.5x94 (no live area published). LF DAP 45x62x94, whose live area really is published as 217x410x112. Cybex 12220 50x43x92 (in use 57x52), Cybex 16140 35x25x54, Cybex 16200 60.57 W x 80.15 L.

## Caveats and flags for the optimizer

1. **Scope of the NSCA density figures.** The 100 ft2/participant and 3/station values are supervision guidelines for athletic S&C rooms. Label them as such and do not treat them as a commercial-gym standard.
2. **Commercial versus garage racks.** `power_rack.footprint_in` (58x59) is a median that includes garage racks (Rogue R-3 with a 30 in depth; RML-490). It is smaller than both commercial HS frames (62x65, 64x73). The envelope stays near 10x10 ft because clearances absorb the difference, so the area impact is small.
3. **Rack ceiling height.** The HS NX power rack product page states "Requires minimum ceiling height of 102"". This is not in the structured data.
4. **Bench storage variant.** The LF Olympic Flat Bench is 49x51x51 without storage but **70x68x51 with storage**. The report used only the no-storage frame.
5. **Heavy-dumbbell rack rating.** The HS 2- and 3-tier spec tables say "Max Dumbbell Size 150 LB", but the same pages say "optimized for dumbbells under 125 lbs" (5 pairs per tier, 1,400 lb per tier). The report's mapping of the 105-150 lb heavy set onto one 2-tier 10-pair rack is therefore doubtful.
6. **Where the margin is measured from.** ISO and Star Trac measure their margins from the training or moving-part envelope, not the frame. The 12 in default side margin (sum rule) is valid only where nothing moves past the frame on that side.
7. **ADA alcoves.** Use a 60 in alcove width for parallel or transfer approach (305.7.2), not 36 in.
