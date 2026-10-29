# Verification log: preferences slice

Checked 2026-10-28 by an adversarial fact-checker. Each value was checked against its cited page (WebFetch) or against the local PDF copies that the research slices saved (SFIA 2024 Topline, ACSM 2025 HFJ article).

## Verdict summary

- **No checked value is numerically wrong.** Every high-impact input matches its source exactly:
  - HFA member reach
  - PureGym most/least-used manager votes
  - HFA Global floor-space shares
  - StrengthLog and Strength Level gender data
  - HFA demographic shares
  - Planet Fitness equipment counts
  - SFIA 2019-23 changes
  - ACSM ranks
- **Four values could not be reached:** Parkwood free-weight peak availability (35 %), Parkwood rack hours (>50 h/week), and Banana Moon's 25 % and 9 %. The pages return 406/403, and the Wayback Machine is blocked. Search-engine summaries partly corroborate them. Use them only as corroboration.
- **Interpretation problems** (the value is right, but the conclusion drawn from it is not supported):
  - Les Mills' "lack of equipment (33 %)" describes access for people who have not yet started lifting. It is not evidence about gym rack under-provisioning.
  - The Les Mills 82 % pin/cable figure has no stated base.
  - The cited Strava 2024 article does not say "fastest-growing sport for women".
  - Harrison Co.'s +558 % for women's machine use cannot be traced to a primary source and conflicts with HFA's measured decline. It should not cancel the PAC "−" vote for selectorized machines.
- **Definition flaw:** the age and beginner tilt ratios are labelled "vs all-member average", but the formula m=(1+x(r−1))/(1+x_ref(r−1)) treats r as a group-vs-rest ratio. For r=2.5 and x_ref=0.229, the equivalent group-vs-rest ratio is 4.5, and m(x=0.5) is 1.30 by the formula against 1.53 under the stated definition.
- **Weak source URL:** the SFIA URL is a generic sfia.org category page. The numbers match the USTA-hosted PDF copy: https://www.usta.com/es/content/dam/usta/sections/intermountain/districts/colorado/pdfs/sfia-reports/2024-sfia-topline.pdf

## High-impact datapoints

| datapoint | claimed | verdict | evidence found |
|---|---|---|---|
| treadmill.member_use_pct_2024 | 43.4 | confirmed | HFA 30 Oct 2025: "In 2024, 43.4% of members used treadmills". This is PAC rolling 12-month participation, not necessarily at the club. |
| free_weights.member_use_pct_2024 | 32.1 | confirmed | "32.1% trained with dumbbells or free weights" |
| resistance_machines.member_use_pct_2024 / _2021 | 26.6 / 31.4 | confirmed | "down from 31.4% and 23.2% in 2021 to 26.6% and 18.8%" |
| elliptical.member_use_pct_2024 / _2021 | 18.8 / 23.2 | confirmed | same sentence |
| power_rack.pg_most_used_pct | 49 | confirmed | "Squat/Lifting Rack: 49%". PureGym, 30 Oct 2023. Managers, n not given, multi-select. |
| lifting_platform / treadmill / stair_climber / cable / dumbbell / bench / barbells / leg press / leg ext (most used) | 37 / 33 / 30 / 27 / 26 / 18 / 11 / 10 / 8 | confirmed | exact list on page |
| recumbent / agility ladders / Bosu / sit-up / stepper / Ski-Erg / Swiss ball / multi-hip / TRX / Powerplate (least used) | 31 / 31 / 27 / 25 / 22 / 17 / 15 / 12 / 10 / 50 | confirmed | exact list on page. Mapping caveats: "Barbells" may mean Olympic bars rather than fixed barbells; "Sit-up machine" may be a sit-up bench. |
| hfa_global.strength_floor_share_modern | 42 (20 traditional) | confirmed | HCM 20 Aug 2025. Data supplier and sample undisclosed ("almost 30 markets"). |
| hfa_global.cardio_floor_share | 12 (34) | confirmed | HCM: "cardio space has decreased from 34 per cent to 12 per cent" |
| hfa_global.functional_floor_share | 15 | confirmed | Athletech 11 Aug 2025 only. HCM gives no functional figure. |
| hip_thrust W/M (StrengthLog) | 9.3 | confirmed | "hip thrust 830% more" (= 9.3×). Women 2.0 %; men's share not published. |
| leg_press / bench / squat / RDL / curl / OHP / incline DB W/M | 1.42 / 0.766 / 1.15 / 1.55 / 0.583 / 0.857 / 0.619 | confirmed | all set shares match the women and men top-25 lists |
| hip_thrust_bench.strengthlevel_female_share | 58.55 | confirmed | 224,489 female of 383,413 qualifying results (158,924 male) |
| women.female_member_share_2024 | 48.5 | confirmed (derived) | Athletech/HFA: "males made up 51.5%" (2024) |
| older.member_share_55plus_2024 | 22.9 | confirmed | "aged 55 and above ... fell slightly to 22.9%" |
| genz.member_share_under25_2024 | 30.8 | confirmed | "30.8% of all fitness facility members ... in 2024" |
| pf.cardio_pieces_standard_2024 / _2022 | 70 / 100 | confirmed | Q3 2024 call: "roughly 100 pieces of cardio and today, it's about 70" |
| pf.plate_loaded_adoption | 65 | confirmed | Q1 2025: "minimal three pieces of plate loaded across 65% of the estate" |
| pf.cardio_mix_changes / pf.ellipticals_bikes_less_used | qualitative | confirmed | Q4 2024 (Keating); Q3 2023 (CFO Fitzgerald) |
| sfia.* (resistance machines −18.7, elliptical −18.1, cross-training −30.6, group cycling −37.3, stair −17.9/+8.0, rowing −0.3/+7.4, kettlebells +12.5, cardio kickboxing −21.4) | as claimed | confirmed | local PDF `downloads/ex_sfia2024/topline.pdf`, p. 33 table. Cited URL is a category page. |

## Suspicious and low-provenance datapoints

| datapoint | claimed | verdict | note |
|---|---|---|---|
| free_weights.peak_availability_pct_parkwood | 35 (50 resistance) | source_unreachable | leisurecentre.com returns 406 to curl and WebFetch; Wayback blocked. One search summary repeats 35 %/50 %; another does not. |
| power_rack.weekly_usage_hours_parkwood | >50 h/wk | source_unreachable | A search summary of the same page says "squat racks (50+ hours)", adjustable benches 39 h, cable stacks 38 h, and Track My Gym data at Parkwood Salisbury. Unverified. |
| crowding.pct_too_busy_peak_uk / pct_queue_machines_uk | 25 / 9 | source_unreachable | Hartlepool Mail and the Sussex Express copy both return 403. Search summaries give "one in four" and "9 per cent". Undated. |
| women.machine_use_growth_2011_2021 | 558 | confirmed (secondary only) | Fitt Insider states it. No Harrison Co. primary found. Conflicts with HFA (31.4→26.6 %) and SFIA (−18.7 %). |
| lifting_platform.women_usage_share_crunch | ≥50 | confirmed (secondary) | Fitt Insider quoting the Crunch CEO via Bloomberg. Unaudited operator remark. |
| acsm.2026.hiit_rank | 12 | confirmed (single source) | ENFAF top-20 only; ACSM publishes the top 10 only. ENFAF's year-on-year notes contain errors (strength "stable" though 5→7). |
| acsm ranks 2023-2026 (strength 2/17/5/7; functional 5/14/9/10; older adults 4/3/3/2) | as claimed | confirmed | 2025 HFJ text (local) and acsm.org 2026 top 10 |
| lifting_barrier.lack_of_equipment | 33 | confirmed value; interpretation unsupported | Les Mills: "the biggest hurdle facing adults considering starting weight training: lack of equipment". This is an access barrier, not gym under-provisioning. |
| genz.pin_cable_machine_use | 82 | confirmed value; base unstated | Les Mills Village Gyms article gives no base |
| strava.2024.women_weight_training_growth | 25 | confirmed value | The "fastest-growing sport type among women" claim is not in the cited Athletech article |
| crowding.overcrowded_nonrenewal_pct | 27 | confirmed as printed | 2017 blog lists it with no attribution. Do not use quantitatively. |
| crowding.hogging_equipment_score | 6.94 | confirmed | listed as "Monopolizing equipment". Survey date not stated. |
| power_rack.most_intimidating_area_pct | 32 | confirmed | PureGym, 25 Oct 2023. n not stated. |
| choice.* (YouGov) | 39 / 25 / 46 | confirmed | 39 % = "rank highest"; 46 % and 25 % = "great deal of importance". Different question bases. |
| crowding.pct_crowds_hurt_consistency | 45 | confirmed | Sogolytics. Survey dates not stated. |
| IHRSA 2016 reach (treadmill / machines / free weights) | 44 / 36 / 31 | confirmed | SGB 24 Jan 2018 |
| PG_EFF19 votes | 59 / 21 / 47 / 36 | confirmed | ResponseSource, 24 Jul 2019 |
| HFA26 (fastest-growing; 65+ +8.6 %; 18-24 35.5 %) | as claimed | confirmed | HFA, 9 Apr 2026 |
| ClassPass (strength +27 %, gym time +51 %) / HYROX (5,000 clubs, 260 %) / EGYM / Strava 2025 / Talker 43 % / LM GFR 50 % / PF Q4 2025 95 % / PG Leeds spec | as claimed | confirmed | verbatim on cited pages |

## Derivation checks

- **Gender regression reproduced.** ln(W/M) = 1.746 + 0.980 ln(odds), R² = 0.961. Without the hip thrust, slope 0.681 and predicted hip thrust 4.21, abduction 3.58, adduction 2.53. These match the report.
- **Recommended hip-thrust ratio.** The geometric mean of 4.2 and 9.3 is 6.25. The report gives 6.0, which is within rounding of a judgement call.
- **Multipliers reproduced.** m = √P·T: rack 1.404, platform 1.346, dumbbells 1.291, stair 1.197, cable 1.183, treadmill 1.153, recumbent 0.748, ab crunch 0.866.
- **Age and beginner tilt definition flaw.** See the summary above. Either redefine r as "group vs everyone else", or use m = (1−x)(1−x_ref·r)/(1−x_ref) + x·r.
- **The P prior is a heuristic.** Manager "most used" vote shares are perception, multi-select, from an unknown n of UK HVLP managers. Treating 49 % as "+49 % demand" is an assumption. It is labelled as an estimate, so this is acceptable, but it is the largest single driver of the rack/platform/treadmill multipliers.

## Missing critical data (for the optimizer)

1. **Measured per-station utilisation** (hours/week or peak occupancy by equipment type) from sensor or tag audits: Track My Gym, EGYM, connected cardio consoles, or rec-centre counts. The Parkwood Salisbury audit was not retrieved. This is the main calibration input for the Erlang model.
2. **Wait tolerance and abandonment:** minutes members will wait per equipment type, and the share of visits on which the desired station was unavailable. This is needed to set the blocking-probability targets.
3. **Behavioural substitution:** what members switch to when a rack, bench, cable or treadmill is taken. The engine's substitution matrix has no source in this slice.
4. **Time-of-day modality mix:** the share of strength, cardio and functional use at peak versus off-peak.
5. **Demographic mix by gym format, size or price tier:** female, 55+ and under-25 shares for HVLP, mid-market, premium, YMCA/community and studio formats. The tilts need x, but the planner only knows square footage and budget.
6. **Normalisers for the Planet Fitness counts:** typical PF club size and membership, so that 70 cardio pieces can become pieces per 1,000 sq ft or per 1,000 members.
7. **Usage data for common items given only defaults:** Smith machine, leg curl, assisted pull-up, hack and belt squat, hyperextension, GHD, landmine, preacher, rotary torso. The Smith machine is the most consequential gap.
8. **Dumbbell weight-range demand:** the share of dumbbell use above 50 lb / 25 kg, which decides between the light, full and heavy-extension sets.
9. **In-gym gender and age equipment use** (HFA crosstabs, EGYM by gender). StrengthLog (about 35 % female) and Strength Level are self-selected lifter apps.
10. **Club-only cardio modality split.** HFA, PAC and SFIA reach includes home use.
11. **Group-exercise and studio demand converted to floor area:** small-group training reach 32.3 %, classes, and the Pilates/yoga boom.
