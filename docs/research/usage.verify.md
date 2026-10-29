# Verification log: usage slice (average gym-goer behavior & time allocation)

Checked on 2026-10-28 by an adversarial fact-checker. Primary documents were opened directly where possible:
- PDFs downloaded and text-searched: SFIA 2024 Topline, Long 2023 thesis, DellaVigna & Malmendier 2006, ABC Wellness Watch Q1 2025, ATUS Table A-1 2025.
- SEC HTML parsed: PF 10-K FY2025, PF May 2025 investor deck.
- Everything else read with WebFetch.

## Bottom line

- **Cited facts: high reliability.** About 70 datapoints were checked and **none was refuted**. Every quoted number appears in its cited source, and every page number given for SFIA (pp. 27, 28, 32, 33) is correct.
- **Derived arithmetic: reproduces.** I recomputed all of it:
  - SFIA cardio and strength occasion shares
  - the 1.099 shift factor
  - the ATUS strength shares (56.3%; by sex 67.5/39.3; by age 75.1/55.6/39.6)
  - the StrengthLog sub-mixes
  - per-member visit ratios and PF members per club
  - every archetype and cardio-mix vector sums to 100.
- **Weak spot: the recommended time shares.** They are judgment layered on population-wide data that includes home exercise (SFIA, ATUS), dated observations (ATUS 2009-15, GYMetrix 2015-16) and enthusiast app logs. Treat them as roughly ±5 percentage points.

## Issues found

| datapoint | issue | severity |
|---|---|---|
| gym_visit.placer_hvlp_minutes | 72.4→74.0 min is confirmed for Q1 2022→Q1 2025. The extra claim "Life Time longest" is **not in S17**: the article names Life Time only for frequent-visitor share. | low |
| gym_visit.puregym_avg_minutes_2022_2024 | The 66-min low bound is marked unfetched (PDF 404). It is **confirmed** on the web version: puregym.com/blog/uk-fitness-report-gym-statistics-2022-2023/ ("average visit tracking in at 66 minutes"). PureGym's own claim that 69 min held "during all three versions" conflicts slightly with that page. | low |
| shift.sfia_2025_cardio_comeback (S2) | sfia.org still fails DNS. Search snippets match the qualitative wording but give **no numbers**, and the 2026 Topline coverage (SGB, Rec Management) has no activity-level figures. This source was used to raise stair_climber to 10% and keep treadmill at 40%. | medium |
| genz.free_weights_use_share | The 81% appears in S35, framed as "younger members… 81% of those currently exercising use free weights at their facility". S34 does not mention free weights. The **same Les Mills Gen Z report gives 82% using pin-loaded or cable machines** (Les Mills Village Gyms case study), so the 81% does not show a preference for free weights over machines. | medium (interpretation) |
| calgary.machine_set_timing | The quote is verbatim, but it comes from a 24-hour pre-test where "it was not known if people were at the gym": one inferred observation, not a measurement. Deployment had 32 equipment sensors (35 were fabricated). | medium (weight given to it) |
| visits.dellavigna_predicted_vs_actual | 9.50 vs 4.17 is verbatim, but the 9.50 forecast comes from a survey of **48 respondents** (Aug 2002), not the 7,752-member panel. | low |
| S8 label | It is the "2018 IHRSA Health Club **Media** Report" (SGB, 24 Jan 2018), not the Consumer Report. The 2016 data year is right. | trivial |
| S32 survey size | "10,442 surveys, 14 countries" is in S33 (ICAA), not S32. S32 says "over 10,000". | trivial |
| shift.pf_cardio_strength_mix | Verbatim: "It really is [indiscernible] ish about a 50-50 mix of cardio and strength". This is the **equipment** mix, not time used. | note |
| sensor.ymca_strength_over_cardio | The page says Track My Gym "tagged all of the gym equipment… over several weeks" and "nearly 1,000 members" were surveyed. It never says "sensors"; the findings are qualitative only. | note |

## Derivation caveats (estimates, not refuted)

- **usage.avg.time_share.cardio = 35%.**
  - The inputs check out: ATUS 9.1/9.1 participation and 0.9/0.7 h, plus the SFIA 1.099 shift.
  - The ATUS baseline (midpoint about 2012) is shifted only for 2019→2023 and the drift after 2023. **2012→2019 is never bridged.**
  - US evidence suggests little drift then: ATUS 2003-08→2009-15 shows the strength:cardio ratio flat (12.5/12.7 → 9.1/9.1). UK GYMetrix 2011-18 suggests a large drift (cardio -33%, resistance +32%).
  - Applying the slice's own +2%/yr drift to the gap would give strength about 63% of strength+cardio minutes, so cardio about 32% of floor time.
  - Recommendation: keep 35% but run the optimizer at 30-38%.
- **strength_station.holding_minutes = 9.** The 58/6 = 9.7 arithmetic is right. But Boostcamp users are programme-following lifters, and the only machine-specific timing is the single Calgary anecdote. Split by station type (machines 4-9, racks 10-15), as the notes already suggest.
- **StrengthLog-based sub-mixes.** The top 25 exercises cover only 62.6% of logged sets, and the machine mix includes only 5 machine types. That overstates the barbell share and omits chest press, shoulder press, pec deck, hip abductor/adductor, Smith machine, hack squat and calf machines.
- **usage.cardio_mix.***
  - Upright vs recumbent split, and air bike / ski erg / curved treadmill / stepper, are pure estimates.
  - The niche 6 points are taken entirely from bikes.
  - Stair climber goes from 6.1% to 10% using Garmin (wearables users) and a qualitative SFIA 2025 claim.

## Confirmed verbatim (selection)

- **HFA S4:** 43.4 / 32.1 / 26.6 (31.4) / 18.8 (23.2) / yoga 21.8 / Pilates 8.1 / PT 22.6 / SGT 32.3.
- **HFA S6:** 7 B visits; 81 M members; >100 M users; 4.6% never use; free weights (dumbbells, barbells, kettlebells) fastest-growing since 2021; Gen Z penetration 35.5%; 26.1% overall.
- **HFA S12:** 72→75 days; average age 39→37.
- **SFIA S1:** all 10 cardio and strength rows (participants, CORE, mean days, occasions, changes since 2019).
- **ATUS S22:**
  - 9.1 / 9.1% participation (12.5 / 12.7 in 2003-08)
  - hours 0.9 / 0.7
  - sex split 72.2 / 27.8 and 44.7 / 55.3
  - age split 33.5/47.7/18.8 and 14.3/48.9/36.8
  - median ages 32.5 / 46.7
  - 18.1% of people exercise on an average day.
- **ATUS S23 (2025):** 23.4% engaged; 1.47 h (men 1.66, women 1.25).
- **Boostcamp S48:** 58 / 79 / ~109 / 87 min; 6 exercises; 2.7 days/week; log counts per exercise.
- **StrengthLog S46/S47:** all 25 percentages; women's hip thrust 2.0 and leg press 2.7 vs men 1.9; 3.3 workouts/week; hip thrust +830%.
- **Session length:** PureGym 68 min (2025/26) and 69 min (2024/25); Placer 72.4→74.0; Strava "just over 50 minutes".
- **Visit frequency:**
  - IHRSA 101-103 visits/yr
  - S8: 44/36/31/47.5%; 5.7 B visits; 57.3 M members; 43.6% ≥100 visits
  - S11: 4.5 B visits; 66.5 M active members
  - Placer: PF 4.1-4.4 and Life Time 5.7-6.2 per month; PF Q3 2024 44.3 / 16.8 / 11.9%
  - FIT Tracker 184,000 visits per location
  - DellaVigna 4.3 / month.
- **Planet Fitness:** 10-K 51% male; 20.8 M members / 2,896 clubs; "not needed to impose time limits on our cardio machines". Deck: >60% of franchisees opted in to more strength; 46% of members under 35; 20% over 55. Q2 call: 65% added plate-loaded; stair climbers "high level of utilization". Q4 call: nearly 80% format-optimized.
- **GYMetrix:** EGYM page -33 / +32 / +121%; Fitness Network (14 Sep 2015) over-supply ranking, 8-18 kg dumbbells, 2:1 male at peak; HuffPost UK (30 Aug 2016) 7% of free-weight users female.
- **Wearables and apps:** Garmin +19 (2023), +25 / +25 (2024), +29 (2025); Strava 21%, 2x, >500 M uploads; ClassPass +27 / +51 / +66; Fitbod 2022 figures and Fitbod 2026 ranks (~30th / ~38th); JEFIT bench #1.
- **Les Mills:** >50% of regular exercisers do strength; group strength 30→36%; 50% "out of place" in the weights area.
- **ABC Wellness Watch:** working out on own 69%; 44% work out 12+ times/month; generation priority scores.
- **UK industry reports:** Anytime Fitness 6-8 platforms, ~7,000 sq ft, core customers 18-32; low-cost clubs average ~4,000 members.
- **Health and fitness bodies:** NHIS 31.0 / 46.9 / 24.2 and 28.3 / 20.4; ACSM 2009 frequencies and 3-5 min rest; ACSM 2027 #5 (Newswise, 20 Oct 2026).
- **Older survey data:** IDEA 36 / 24 / 23%; HCM 2014 47%.

## Missing data the optimizer needs (not in slice)

1. Measured per-equipment **utilization** (share of open or peak hours in use) by type. Needed to calibrate offered load in the Erlang model; only qualitative over/under-supply rankings were collected.
2. The **peak-hour modality mix**. Peaks skew young and male (GYMetrix 2:1; YMCA strength queues at peak), but only all-day averages are given.
3. **Per-visit participation probabilities** by modality (share of visits with any cardio, rack, dumbbells, machines, cables). Needed for arrival rates per equipment pool.
4. **Substitution and balking** behavior when a station is busy (substitute, wait or skip, plus wait tolerance). This is core to the M/G/c/c model with substitution, and no source was collected.
5. Directly measured **holding times by station type** (rack, bench, cable, each cardio type) and bout lengths per cardio machine type.
6. Usage shares for gym **members specifically** (not the general population) for cables, functional/turf, kettlebells, stair, rower, bikes and racks. The 82% Gen Z machine figure was also missed.
7. Demand for **long-tail machines** beyond the StrengthLog top 25, plus upright vs recumbent split and niche cardio (air bike, ski erg, curved treadmill, stepper).
8. Activity-level **SFIA 2024/2025 counts**, to replace the qualitative "cardio comeback".
9. National **member gender and age mix** (HFA) to weight the archetypes.
10. Usage differences by **facility size and format** (small 24-hour or boutique vs big-box) for frequency and modality mix.
