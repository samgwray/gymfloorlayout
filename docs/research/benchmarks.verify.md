# Verification log: benchmarks slice

- Checked: 2026-10-28 by an adversarial fact-checker.
- Method: I opened each cited URL with WebFetch. Primary PDFs were downloaded and text-extracted with pdftotext:
  - Crunch Item 19 → `scratchpad/verify_crunch_i19.txt`
  - PureGym AR 2018 → `scratchpad/verify_pg_ar2018.txt`
  - IRS Pub 946 → `scratchpad/verify_p946.txt`
  - Anytime Fitness 2022 brochure → `scratchpad/verify_af_brochure22.txt`
- The shared WebSearch budget ran out after one search. All other checks used direct fetches of the cited URLs.

## Result in one line
- **No cited value was refuted.** I checked 70 datapoints. The tables below group some of them.
  - 68 confirmed. For derived values, the inputs and arithmetic also check out.
  - 1 derived band corrected (currency mix-up).
  - 1 derived band unsupported (no data for that size band).
- The remaining risk comes from the **derivations and source mix**, not from transcription.

## Datapoint checks

### Planet Fitness, 2026 FDD and SEC filings

| Datapoint | Verdict | What the source shows |
|---|---|---|
| pf.fdd2026.fitness_equipment_purchase_usd ($333k–$995k) | confirmed | Supported by one source only: VMF's "Finance vs Purchase" table (cites 2026 FDD Item 5 and Item 7 Note 4). Franchise Chatter and 1851 show only the single line "$33,300 to $995,000". FC's financed total ($1,282,500–$3,769,000) is consistent. I did not find the researcher's verbatim sentence. VMF's cover-page figure of "$333,000 to $1,050,000 if you buy it" has a different scope. |
| pf.fdd2026.fitness_equipment_financed_down_usd | confirmed | VMF table: "$33,300 to $298,500". Footnote: "Down payments are typically 10% to 30%". |
| pf.fdd2026.premises_sqft (15–25k) | confirmed | VMF: "approximately 15,000 to 25,000 square feet". |
| pf.10k2025.typical_sqft / members_per_club | confirmed | 10-K: "typically 20,000 square feet"; "approximately 20.8 million members and 2,896 clubs". That gives 7,182 members per club. |
| pf.fdd2026.item19_corp_avg_sqft | confirmed | FC: 19,760 / 19,619 / 21,472 sq ft for 88 / 87 / 87 clubs. Net revenue per sq ft is $66.95 / $100.99 / $123.82. |
| pf.fdd2025.fitness_equipment_usd | confirmed | Franchise Direct: $36,300–$1,103,000. Total $1,525,000–$5,221,500. |
| pf.reequip_cycle_years (5–9) / remodel (12) | confirmed | 10-K: "every five to nine years"; "refurbish and remodel their clubs in year 12". |
| pf.reequip_cardio_years / pf.reequip_strength_years | confirmed, better source found | The 2025 slide text has no column labels. The 2023 PF investor presentation 8-K labels them explicitly: "Previous … Cardio Re-Equip Year 5, Strength Re-Equip Year 7"; "Future … Cardio Re-Equip Year 5, 6, 7*; Strength Re-Equip Year 7, 8, 9*"; "*Determined based on club usage". |
| pf.strength_optin_2024, pf.new_club_capital_usd | confirmed | 2025 Investor Day text: ">60% of franchisees opted-in…"; "New Club Capital ~$3M"; "Remodel ~$1M"; "Unit build out cost $2.4mm - $4.0mm". |
| pf.balanced_mix_clubs_q1_2025, pf.format_optimized_share_2025 | confirmed | Q1 2025 call: "nearly 1,800 clubs…"; plate-loaded added at 65% of the estate. Q4 2025 call: 95% of openings and remodels; "nearly 80%" of the system. |

### Planet Fitness club openings

| Datapoint | Verdict | What the source shows |
|---|---|---|
| pf.club_worcester_2025 | confirmed | NEREJ, Jul 25, 2025: 13,605 sq ft; 48 cardio; 69 strength. |
| pf.club_lakewood_2025 | confirmed | Patch: 17,726 sq ft; 62 cardio; 90 strength. First posted Mar 31, 2025 and updated Jun 2, 2025. |
| pf.club_eden_prairie_2024 | confirmed | 19,000 sq ft; 62 cardio; 93 strength; opening Dec 14, 2024. |
| pf.club_puyallup_2026 | confirmed | KIRO 7, Oct 20, 2026: 19,740 sq ft; 56 cardio; 83 strength. |
| pf.club_sammamish_2026 | confirmed | What Now, Jun 12, 2026: 21,141 sq ft; 56 cardio; 83 strength. The counts are identical to Puyallup in two independent articles, so piece counts follow a template rather than floor area. |
| pf.club_duluth | confirmed | 22,000 sq ft; 110 cardio; 75 strength; 30-Minute Express Circuit. Undated. |
| pf.pieces_per_1000sqft, pf.cardio_share_pieces | confirmed (arithmetic) | 8.60 / 8.57 / 8.16 / 7.04 / 6.57 pieces per 1,000 sq ft, mean 7.79. Cardio share is 40.0–41.0%. |

### Other large-format brands

| Datapoint | Verdict | What the source shows |
|---|---|---|
| crunch.fdd2026.fitness_equipment_fixtures_usd | confirmed | Zee Report (2026): $850,000–$1,500,000; total $2,147,500–$5,367,000. Only one reproduction carries this line. |
| crunch.item19.median_sqft / avg_members | confirmed (primary PDF) | Median sq ft 27,000 / 31,220 / 34,000 / 40,000. Average sq ft 34,155 / 32,624 / 32,517 / 28,433. Average members 8,062 / 8,303 / 7,842 / 7,484. Club counts 55 / 34 / 19 / 35. "CF FDD 9/2025", FY2024. |
| crunch.members_per_sqft | confirmed (arithmetic) | Club-weighted 7,949 members ÷ 32,173 sq ft = 0.247. |
| crunch.faq.sqft, crunch.membership_price | confirmed | FAQ: "20,000 to 40,000"; sweet spot 25–30k. Price $9.95/mo with a $29/$39 annual fee; Peak $19.95. Some locations charge up to $49.95. |
| golds.fdd2026 strength / cardio, golds.sqft | confirmed | Franchise Direct and 1851 agree: strength $425k–$850k; cardio $160k–$275k; footprint "15,000 to 25,000 square feet". |
| ufc.item19 signature sqft / members; ufc.fdd2026; ufc.fdd2025 class | confirmed | Avg 32,874 sq ft, median 35,302, 22 gyms. Avg members 5,548, median 5,477. FD 2026: $142k–$595k. FC 2025: Class equipment $110k–$130k. |

### Medium-format brands

| Datapoint | Verdict | What the source shows |
|---|---|---|
| af.fdd2026.fitness_equipment_usd, premises_sqft, item19 members | confirmed | FD and VMF: $139,873–$157,936. VMF: "4,000 to 7,000 square foot center". Average 660 members (1,683 centers; quartiles 995 / 683 / 550 / 411). The Item 19 figures come from one reproduction only. |
| af.2022.typical_sqft | confirmed (brochure PDF) | "In only about 7,000 square feet"; $381,575–$783,897 (2022 Item 7). |
| snap.web2026.equipment_usd_4k_6k, snap.site_sqft | confirmed | Equipment $200k–$250k; Min 4,000 / Max 10,000+ sq ft. The floor plans give no piece counts. |
| snap.fdd2025.fitness_equipment_usd | confirmed (FD) | FD 2025: $60,000–$300,000. I did not re-check the 1851 figure of $200k. |
| wa.fdd2026.equipment_package_usd, wa.sqft | confirmed | 1851 values match. The claim that the package includes HydroMassage or CryoLounge is **not** in 1851. |

### Small studios

| Datapoint | Verdict | What the source shows |
|---|---|---|
| otf.fdd2026.fitness_equipment_usd, otf.studio_sqft | confirmed | $119,122–$163,424. The line includes installation and the OTBeat heart-rate system. Studio size "250 - 350 m2 / 2,690 - 3,765 ft2". |
| treadmill.otf_count_per_studio | confirmed | Riverstone 14 (wording ambiguous). Bay Shore 16. Tribeca 16 per station, but it is "the biggest studio in Manhattan", so 16 is the upper end. |
| f45.fdd2025.equipment_pack_usd | confirmed | $115,000 / $115,000; taxes $0–$15,000. |
| burn (equipment line, sq ft, Item 19 brackets) | confirmed | Equipment $22,821–$32,760; 3,600–7,000 sq ft. Brackets 569 / 442 / 343 / 250 / 169 across 307 outlets, which gives an outlet-weighted average of 334 members. |

### UK chains, Life Time, tax and vendor guides

| Datapoint | Verdict | What the source shows |
|---|---|---|
| puregym.lbf_sqft, sbf_sqft, avg_members, capex, depreciation | confirmed (primary PDF) | LBF 15,000–20,000; SBF 5,000–8,000; 4,994 average members (2017: 5,070); £1,190k initial capex; fixtures and fittings depreciated over 6 years. The 4,994 average covers all PureGyms, including SBF sites and Soho conversions. |
| puregym.pieces_per_gym, dumbbell.puregym_max_kg | confirmed | "over 220+ pieces of gym kit" (Leeds; site area not stated). "dumbbells up to 50kg (in most gyms)". |
| gymgroup.pieces_per_gym_2014 | confirmed | "around 200 pieces of modern equipment" (Sep 2, 2014). |
| lifetime.visits_per_membership / indoor sqft | confirmed | "149 for 2025". "over 18 million of indoor square feet" and 189 destinations; the filing also says "more than 185 centers". |
| tax.macrs_class79_recreation | confirmed (primary PDF) | Class 79.0 Recreation: 10 / 7 / 10. Class 57.0: 9 / 5 / 9. |
| atlantis.pieces_per_2000sqft, cost tiers | confirmed | "For every 2,000 square feet … about 25 to 35 pieces" (mid-sized section). The tiers are CAD. The page shows mid-sized "CAD $50,000 to $200,000" and large "CAD $200,000 to $500,000", without the "+" the researcher added. |
| pushpress.sqft_per_concurrent_member, group-training budget, prices | confirmed | 60–80 / 25–40 / 80–100 / 150–250 sq ft. $28k–$48k ($25k–$45k if mixing new and used). Bikes $1,200–$2,500; reformers $3,500–$6,000. |

### Derived bands

| Datapoint | Verdict | What the source shows |
|---|---|---|
| bench.recommended_equipment_usd_per_sqft_small (45, 25–75) | **corrected** | Atlantis's "$25 to $50 per square foot" is on a Canadian page whose figures are labeled CAD. That is about USD $18–36. The low end of the band should be about $18–20 USD. In addition, OTF's line bundles OTBeat and installation, and the F45 and Club Pilates sizes are not from FDDs. |
| bench.recommended_pieces_per_1000sqft_medium (12, 10–15) | **unsupported** | No 4,000–10,000 sq ft piece counts exist in the slice. The band interpolates a CAD vendor rule written for 2,000–5,000 sq ft and a UK large-box marketing claim. Snap's floor plans give no counts. |

## Derivation and representativeness caveats
- **Planet Fitness counts.**
  - Two of the five 2024–26 openings have identical counts, and three are in Washington State. Treat the large-gym density band as resting on about 3–4 independent points.
  - "Strength pieces" include free weights, and the unit of a piece is not defined.
- **Studio formats.** Small-gym benchmarks come from class studios (OTF, F45, Burn, UFC Class). Their demand is synchronized class demand, unlike an open floor.
- **Members per sq ft.** These are membership-stock ratios. They need visit frequency and the peak-hour share before they can be used for queueing.
- **Equipment share of investment.** The 22% median counts Snap twice (FDD and website).

## Missing critical data
1. **Gross-to-net ratio.**
   - Missing: the share of gross sq ft that is training floor, as opposed to locker rooms, lobby and desk, offices, amenity rooms (such as the PF Black Card spa) and circulation.
   - Why it matters: it is needed to convert the user's sq ft into packable area. It is also needed to compare optimizer density with the gross-area benchmarks (PF 116–152 gross sq ft per piece).
2. **Category-level counts in real gyms.**
   - Missing: racks and platforms, Smith machines, benches, dumbbell pairs and maximum weight, cable stations, selectorized vs plate-loaded machines, and the treadmill / elliptical / bike / stair split.
   - Why it matters: the slice splits only cardio vs strength, so the optimizer's diversity and redundancy logic cannot be validated.
3. **Medium-format piece counts** (4,000–10,000 sq ft; Anytime, Snap, independents). None were found.
4. **Small open-floor gym benchmarks** (1,000–3,500 sq ft, 24/7 or independent).
   - Missing: members per sq ft and piece counts.
   - The current small-gym figures come from class-based studios.
5. **Peak concurrency benchmarks.**
   - Missing: check-ins per hour or people per 1,000 sq ft at peak for HVLP and 24/7 clubs, and visits per member for budget chains. Only Life Time's luxury-club figure (149 visits per membership) is present.
   - Also missing: the code occupant-load factor for exercise rooms, which caps capacity.
6. **Cardio share by count for strength-focused and mid-tier gyms.** The only figure is inferred from the Gold's Gym dollar split.
7. **Currency normalization.** CAD (Atlantis) and GBP (PureGym) values are mixed into USD bands without conversion.
8. **Unit-cost decomposition.**
   - Missing: price per treadmill, per selectorized machine, per rack, and $/lb for dumbbells.
   - Without these, the $/sq ft benchmarks cannot be decomposed for budget validation.
9. **Flooring, freight and installation** as a share of the equipment budget.
   - FDDs bury these costs in other lines.
   - The only figure, PushPress's $1.33–$3.00/sq ft for rubber, looks low for commercial installed flooring.
10. **Discount for used or refurbished equipment** in small-budget plans. The only figure is PushPress's remark that buying new costs 30–50% more.
11. **HFA/IHRSA medians** for club size, members per sq ft and capex per sq ft. These are members-only and were not obtained.
