# Member preferences, most-wanted equipment, crowding complaints and trends

Research slice: **preferences** (feeds the planner's per-equipment *desirability multipliers* and demographic tilts).
Compiled 2026-10-28. Equipment ids follow the canonical taxonomy (e.g. `power_rack`, `hip_thrust_machine`).

**Method.** I fetched primary or near-primary pages directly wherever possible: ACSM pages and the full 2025 ACSM HFJ article (PDF), HFA press releases, Planet Fitness earnings-call transcripts and SEC filings, PureGym survey pages, The Gym Group report PDFs, Les Mills research pages, StrengthLog, Strength Level, Strava and ClassPass coverage. Every number below carries its source. Values I derived are marked **(derived)** or **(estimate)** with the derivation shown.

**Limitations.**
- The session's shared web-search budget ran out several times, so some leads were followed only by fetching known URLs.
- Several pages returned 403/406. Where a number comes only from a search-engine summary of such a page, its source is marked `fetched=false` in the source list, and it is used only as corroboration.
- Members-only reports (HFA full reports, the Les Mills Global Fitness Report PDF, the EGYM whitepaper, Which? member tables, Mintel) could not be read in full.

---

## 0. Key takeaways for the model

1. **The four things most members use are treadmills, free weights, resistance machines and ellipticals.** HFA 2024 member-usage shares are: treadmill **43.4 %**, free weights/dumbbells **32.1 %**, resistance machines **26.6 %** (down from 31.4 % in 2021) and ellipticals **18.8 %** (down from 23.2 % in 2021) [HFA25X].
2. **Squat racks and platforms are the most-used and most-contested stations in general-population gyms.** UK gym managers named the squat/lifting rack most used (49 %), ahead of the Olympic lifting platform (37 %), treadmill (33 %), Climbmill/StairMaster (30 %), cable machine (27 %), dumbbells (26 %) and bench press (18 %) [PG_MU23]. Garage Gym Reviews calls the squat rack "the most coveted piece of equipment of them all", and "hogging equipment" is the No. 1 gym annoyance at 6.94/10 (n=2,000) [GGR24]. A UK club audit (not fetched; search summary only) found free weights only **35 %** available at peak and squat racks used **>50 h/week** [PARKWOOD].
3. **Least-used items (candidates to cut first):** Powerplate (50 % of managers), recumbent bike (31 %), agility ladders (31 %), Bosu (27 %), **sit-up/ab machine (25 %)**, stepper (22 %), **SkiErg (17 %)**, Swiss ball (15 %), **multi-hip machine (12 %)**, TRX (10 %) [PG_MU23]. Planet Fitness "pulled back on ellipticals and arc trainers" and says "elliptical and bikes are getting far less used" [PF_Q4_24, PF_Q3_23].
4. **The shift to strength is measurable:**
   - ACSM ranked strength training **#2 (2023), #17 (2024), #5 (2025) and #7 (2026)** [ACSM23, ACSM25, ACSM26].
   - HFA says free weights grew "faster than any other equipment category since 2021" [HFA26].
   - Planet Fitness cut its standard cardio count from **~100 to ~70 pieces (-30 %)** and added **≥3 plate-loaded pieces in ~65 % of clubs** [PF_Q3_24, PF_Q1_25].
   - "Modern" clubs give **42 %** of floor space to strength (traditional layouts 20 %); cardio falls from **34 % to 12 %**; functional zones take **15 %** [HFAGLOBAL].
5. **Treadmills are the exception within cardio.** They are still the most-used modality (43.4 %), Planet Fitness "maintained a strong complement of treadmills", and stair climbers were *increased* [HFA25X, PF_Q4_24]. The cardio cuts fall on ellipticals, arc trainers and bikes.
6. **Women drive glute-equipment demand, and the effect is very large.**
   - StrengthLog (>700k users): women perform the **hip thrust 830 % more** than men (≈9.3×) and the leg press 42 % more. Men bench 30 % more and barbell-curl 71 % more [STRENGTHLOG25].
   - Strength Level: **58.6 %** of hip-thrust and **52.7 %** of hip-abduction results are female, against **9.3 %** for bench press [SL_*].
   - Crunch reports women at "50%+ of lifting platform usage" [FITT_WOMEN].
7. **Intimidation is concentrated in the free-weight area.**
   - The squat rack is the single most intimidating area (32 %), followed by the pull-up/chin-up station and the bench press [PG_FEAR23].
   - Among aspiring lifters, 50 % "feel out of place in the weights area" and 33 % cite lack of equipment as the primary reason they have not started lifting [LM_GFR26].
   - 43 % of US women have never lifted weights at a gym [TALKER25].
   - Machines and cables are the beginner-friendly on-ramp; the Les Mills Gen Z report found 82 % of Gen Z using pin-loaded or cable machines [LM_VILLAGE].
8. **Demographics are moving toward young, male-skewed lifters, with older adults growing fastest.**
   - Members under 25 make up **30.8 %** of US members (22.9 % in 2015); men are **51.5 %** (49.6 % in 2019); members 55+ are **22.9 %** [HFA25_DEMO].
   - Members 65+ grew **8.6 %** YoY in 2025, the fastest cohort, and "visit gyms and studios more often than any other age group" [HFA26, ACSM26].
   - Boomers and the Silent generation prefer "stationary cycling, stretching, Tai Chi and weight/resistance machines" [IHRSA18].
9. **Functional training is growing.** HYROX reached 5,000 training clubs with 260 %/yr affiliation growth [HYROX_PR24], and new UK HVLP sites add sled tracks, 6-bay rigs, a BootyBuilder and a "perfect squat" machine [PG_LEEDS]. But US participation in "cross-training style workouts" fell 30.6 % from 2019 to 2023 [SFIA24]. Favour turf/sled lanes over CrossFit-style boxes.
10. **Derived desirability multipliers (Section 7).** Highest: `power_rack`/`half_rack` 1.40, `lifting_platform` 1.35, dumbbells 1.29, `bench_press_station` 1.25, `stair_climber` 1.20, cables 1.18, `treadmill` 1.15. Lowest: `recumbent_bike` 0.75 (unless the facility skews older), `ab_crunch_machine` 0.87, `elliptical`/`upright_bike`/`heavy_bag` 0.90, `glute_kickback` 0.94.

---

## 1. What members actually use (reach / most-used)

### 1.1 Share of US fitness-facility members using each modality

| Modality | 2016 (IHRSA 2018 Media Report) | 2021 (HFA) | 2024 (HFA 2025 Expanded Insights) | Change | Source |
|---|---|---|---|---|---|
| Treadmill | 44 % | n/a | **43.4 %** | ≈ flat (-0.6 pt vs 2016) | IHRSA18, HFA25X |
| Free weights / dumbbells | 31 % | n/a | **32.1 %** | +1.1 pt vs 2016 | IHRSA18, HFA25X |
| Resistance machines | 36 % | 31.4 % | **26.6 %** | -4.8 pt since 2021; -9.4 pt vs 2016 | IHRSA18, HFA25X |
| Elliptical | n/a | 23.2 % | **18.8 %** | -4.4 pt since 2021 | HFA25X |
| Yoga (members) | 36 %* | 20.2 % (2023) | 21.8 % | | HFA25X |
| Pilates | | | 8.1 % | | HFA25X |
| Small-group training / personal training | | | 32.3 % / 22.6 % | | HFA25X |

\*The 2016 yoga figure (IDEA summary of the IHRSA 2017 report) uses a different base, so it is not comparable.

Quotes:
- HFA, Oct 30 2025: "In 2024, 43.4% of members used treadmills." Free weights and dumbbells were 32.1 %. "Resistance machines fell from 31.4% in 2021 to 26.6% in 2024. Ellipticals fell from 23.2% to 18.8%." Base: a nationally representative survey of 18,000 US residents, rolling 12-month participation [HFA25X].
- IHRSA 2018 Media Report: "44 percent report using a treadmill"; resistance machines "36 percent"; free weights/dumbbells "31 percent" (2016 data) [IHRSA18].
- HFA 2023 report (2022 data): "treadmills, free weights (dumbbells/hand weights), and resistance machines remained the three most popular types" [HFA23].
- HFA, April 2026: "Free weight usage — dumbbells, barbells, and kettlebells — has grown faster than any other equipment category since 2021" [HFA26].

**Modeling note.** These are per-member *reach* figures (share of members who use the modality at all in a year). They are not time shares. Use them as a check on the exercise/time-allocation slice: treadmills reach the most members, and free weights are second and rising.

### 1.2 Gym-manager perception of most- and least-used kit (PureGym UK, published 30 Oct 2023)

Each figure is the "% of UK gym managers who agreed that item was the most / least used". The number of managers was not published [PG_MU23].

| Most used | % | Mapped id | | Least used | % | Mapped id |
|---|---|---|---|---|---|---|
| Squat/Lifting Rack | **49** | `power_rack`, `half_rack` | | Powerplate | **50** | (not in taxonomy) |
| Olympic Lifting Platform | **37** | `lifting_platform` | | Recumbent Bike | **31** | `recumbent_bike` |
| Treadmill | **33** | `treadmill` | | Agility Ladders | **31** | `accessory_pack` component |
| Climbmill/Stair-Master | **30** | `stair_climber` | | Bosu-Ball | **27** | `accessory_pack` component |
| Cable Machine | **27** | cables | | Sit-up Machine | **25** | `ab_crunch_machine` |
| Dumbbells | **26** | dumbbell sets | | Stepper (pedal) | **22** | (not in taxonomy; avoid) |
| Bench Press | **18** | `bench_press_station` | | Ski-Erg | **17** | `ski_erg` |
| Barbells | **11** | `fixed_barbell_set` | | Swiss Ball | **15** | `accessory_pack` component |
| Leg Press Machine | **10** | `leg_press` | | Multi-Hip Machine | **12** | `glute_kickback` |
| Leg Extension Machine | **8** | `leg_extension` | | TRX System | **10** | `suspension_trainer_station` |

Supporting quotes from the same page: treadmills and squat racks are popular "across the country", and the recumbent bike is where you "should always be able to get on and get riding". The page suggests trying a bosu ball when the treadmill is too busy ("Treadmill too busy?").

**PureGym 2019 manager vote on "most effective" kit** (press release, 24 Jul 2019; % of managers) [PG_EFF19]:

| Goal | Top answers |
|---|---|
| Overall top performer | Lifting Platform 21 %, Squat Rack 13 %, Cable Machine 11 %, Dumbbells 7 %, Climbmill/StairMaster 5 %, TRX 3 % |
| Building muscle | Squat/Lifting Rack 59 %, Lifting Platform 57 %, Dumbbells 54 %, Barbells 37 %, Cable Machine 23 %, Leg Press 13 %, Bench Press 12 %, Pull-up/Chin-up Bar 7 %, Lat Pull-Down 5 %, Kettlebells 5 % |
| Overall fitness | Rowing Machine 47 %, Treadmill 39 %, Climbmill/StairMaster 24 %, Kettlebells 23 %, TRX 19 %, Indoor Cycle 18 %, Dumbbells 16 %, Elliptical 15 %, Cable Machine 14 %, Lifting Platform 11 % |
| Weight loss | Climbmill/StairMaster 36 %, Squat/Lifting Rack 33 %, Rowing Machine 26 %, Lifting Platform 25 %, Treadmill 25 %, Dumbbells 23 %, Barbells 20 %, Kettlebells 16 %, Assault Bike 12 %, Indoor Cycle 12 % |

### 1.3 Measured utilisation (single-club audit; corroboration only)
- Parkwood Health & Fitness (UK), as summarised by a search engine from leisurecentre.com, "Purposeful Gym Design" (page returned HTTP 406, **not fetched**): "At peak time the average availability of free weights and resistance equipment is only **35%** and **50%** respectively. Squat racks were the most-used equipment, with the highest average usage across the week at **over 50 hours**." [PARKWOOD]

### 1.4 Gen Z / connected-equipment usage signals
- The Les Mills *Gen Z Fitness: Cracking the Code* report (2023; >4,000 people aged 16–26 in North America, Europe and Asia) found "50% of Gen Z exercisers taking part in strength-based group training" and that "82% are using pin-loaded or cable resistance machines in their facilities" [LM_VILLAGE]. Strength training is the No. 1 preferred group workout, "up from 10th place in 2021" [LM_GENZ, LM_ATTRACT].
- EGYM smart-machine data (Nov 2025): "Gen Z leans into machine leg extension and machine hip abduction, with step machines rounding out their top three." Millennials put "walking and treadmill in the top spots, but strength machines such as machine hip abduction and machine leg press sit right behind." Over 2010–2022, consumers "spent far more time using free weights and resistance equipment and far less time on cardio machines" [EGYM25]. (This is EGYM's own platform, so it is machine-biased.)
- The Gym Group *Gen Z Fitness Pulse 2025* (UK, n=2,071, aged 16–28, 1–7 July 2025) [TGG_GENZ25]:
  - Strength training is part of the routine for **54.8 %**; running outdoors 52.1 %; team sports 31.9 %; spin/HIIT/cardio 29.5 %; yoga/Pilates 28.2 %; dance 18.3 %; functional training (e.g. HYROX) **12.8 %**.
  - Strength training was ranked as the activity done most often by **24.9 %**.
  - "While dumbbells, barbells, and machines make up the heart of gyms, this insight shows they should now be complemented by offerings like Pilates, spin classes, and similar group fitness sessions."

---

## 2. What members want: reasons for joining and leaving

| Finding | Value | Population / date | Source |
|---|---|---|---|
| Equipment as a gym-choice factor (3rd after cost 58 % and location 46 %) | **39 %** | 1,120 GB adults, 9 Feb 2022 | YOUGOV22 |
| "Enough machines at peak times" as a choice factor | **25 %** general; **35 %** millennials | same | YOUGOV22 |
| "Has the right equipment" as a choice factor | **46 %** general; **53 %** millennials | same | YOUGOV22 |
| Women vs men: variety of classes | 23 % vs 8 % | same | YOUGOV22 |
| Women vs men: cleanliness | 41 % vs 33 % | same | YOUGOV22 |
| Left gym because too expensive | 35 % | >1,000 US adults (updated 18 May 2026) | SOGO26 |
| "Crowds made their gym environment uncomfortable" | 27 % | same | SOGO26 |
| "Crowds make it harder to stay consistent" | **45 %** | same | SOGO26 |
| Gym choice: cost / location | 39 % / 35 % | same | SOGO26 |
| Aspiring lifters: "feeling out of place in the weights area" | **50 %** | Les Mills 2026 Global Fitness Report (>10,000 consumers) | LM_GFR26 |
| Aspiring lifters: "lack of equipment" as primary reason not lifting | **33 %** | same | LM_GFR26, LM_CONF |
| Aspiring lifters: fear of injury | 23 % | same | LM_GFR26 |
| Lifters: conflicting advice / unsure how to progress | 58 % / 37 % | same | LM_GFR26 |
| Reasons for not renewing: overcrowded facility | 27 % (cost 30 %, time 26 %, location 18 %) | **Unsourced** list in a 2017 newspaper fitness blog; low confidence | COLUMBIAN17 |
| Which? 2025 gym survey | "gyms being too busy and regularly feeling crowded was a common issue"; also "faulty machines that were not being repaired quickly enough" | 6,498 UK adults, Sept 2025 (scores members-only) | WHICH25 |
| Campus/club request surveys | Princeton Lakeside (2026): dumbbell/weights rack 96.1 % support, cable machine 89.1 % | search summary only, **not fetched** (image-only PDF) | PRINCETON26 |

**Interpretation.** Equipment ranks third as a reason to choose a gym. Crowding at peak is a top-two in-gym complaint, and close to half of members say it hurts their consistency. Squat racks, free weights and benches are the bottleneck. For members who want to lift but don't yet, not enough equipment is the main stated barrier (33 %), behind feeling out of place (50 %), which is a reason not to under-provision racks.

---

## 3. Crowding and waiting complaints

- **Garage Gym Reviews survey** of 2,000 US public-gym users (updated 25 Jul 2024), top-10 "Annoying Gym Behavior Score" (1–10) [GGR24]:
  1. Hogging equipment **6.94**
  2. Not sanitizing equipment 6.81
  3. Strangers staring/approaching 6.72
  4. Strangers moving to the machine next to you 6.66
  5. Music out loud 6.62

  Also: **22 %** admitted taking over multiple pieces of equipment at once. The squat rack is called "the most coveted piece of equipment of them all", with advice not to do biceps curls in the rack at peak.
- **Banana Moon UK survey** of 1,000 gym members, via Hartlepool Mail (HTTP 403, **not fetched**): 25 % are annoyed it is "too busy at peak times", and a further **9 %** are frustrated at having to queue for machines [BANANAMOON].
- **Les Mills (Phillip Mills, 18 Dec 2024)**: "inevitable bottlenecks on the gym floor (particularly as we enter high season)" mean "many younger members joining gyms to lift weights aren't staying very long" [LM_PM25].
- **PureGym (2023)**: the least-used list is offered as "a good way to guarantee a quieter workout with less queuing" [PG_MU23].
- **Planet Fitness**: "the functional areas just have more open space so people can work out" [PF_Q3_23]. "Removing some of the less utilized cardio equipment frees up floor space ... for members to grab a mat and weights" [PF_Q3_24].

**What members wait for most (synthesis).** In priority order: squat/power racks, then the Olympic platform, flat bench press, cable stations and dumbbell bays. The evidence is the manager vote, the coveted-rack commentary and the single-club audit (racks >50 h/week; free weights 35 % available at peak). Treadmills are the cardio item most likely to be fully occupied. I found no large published study that measures queue length by equipment type (see Gaps).

---

## 4. The strength-training boom: trend reports

### 4.1 ACSM Worldwide Fitness Trends (rank among top 20)

| Trend | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|
| Strength training with free weights (2023) / Traditional strength training (2024–26) | **2** | **17** | **5** | **7** |
| Functional fitness training | 5 | 14 | 9 | 10 (sources dispute the 2025 base: #9 per 2025 table vs "#12" per 2026 coverage) |
| Body weight training | 3 | not in top 20 | 18 | not in top 20 (per ES list) |
| Fitness programs for older adults | 4 | 3 | 3 | **2** |
| HIIT | 7 | (reported #20, unverified) | 6 | 12 (ES list only) |
| Balance, flow and core strength | – | – | – | 5 |
| Group fitness classes | – | – | – | 13 (ES list only) |
| Commercial/big-box gyms | – | – | – | 19 (ES list only) |
| Wearable technology | 1 | 1 | 1 | 1 |

Sources and quotes:
- 2023 (newswise ACSM release; >4,500 pros): No. 2 "Strength Training with Free Weights", which incorporates "barbells, dumbbells and/or kettlebells" [ACSM23].
- 2025 HFJ article, Table 3 and text (N=2,083 final sample; 45 possible trends; 10-point Likert scale): "After falling to no. 17 in the 2024 survey, traditional strength training moves back up the trends list to no. 5 ... incorporates equipment such as barbells, dumbbells, and kettlebells". Functional fitness "most recently fell to no. 14 in 2024". The article also says "there is a clear and pressing need for low-cost and budget gyms that offer traditional strength training facilities" [ACSM25].
- 2026 (acsm.org; ~2,000 respondents): No. 7 Traditional Strength Training, No. 10 Functional Fitness Training, No. 2 Fitness Programs for Older Adults. The release says "Resistance exercises use free weights such as barbells, dumbbells and kettlebells", "fewer than 30% of U.S. adults meet the recommended guidelines for muscle-strengthening activity" and "adults 65 and older now visit gyms and studios more often than any other age group" [ACSM26]. Ranks 11–20 come from one Spanish-language summary (1,540 valid responses), so they are lower confidence [ACSM26_ES].
- Planet Fitness's 2025 Investor Day slide cites the same signal: "Strength training with free weights catapulted to the #2 fitness trend globally in 2023" [PF_ID25].

### 4.2 Other boom indicators

| Indicator | Value | Source |
|---|---|---|
| Free-weight usage growth | "grown faster than any other equipment category since 2021" | HFA26 |
| US members in 2025 | 81 M (all-time high, +5.2 % vs 2024) | HFA26 |
| ClassPass 2025 most-booked workouts (1 Jan–10 Oct 2025) | Pilates #1 (+66 %), Yoga #2 (+28 %), **Strength Training #3 (+27 % YoY)**, Cycling #4 (+6 %), Barre (+30 %), **Gym Time #6 (+51 %)**, Boxing (-7 %), Low-impact (+112 %) | CLASSPASS25 |
| Strava 2024 | weight-training uploads among women **+25 %**, the fastest-growing sport for women (135 M+ users) | STRAVA24 |
| Strava 2025 (survey >30,000) | Gen Z **2×** as likely as Gen X to say weight training is their primary sport; 61 % more Gen Z than Gen X lift for aesthetics; women **21 % more likely** than men to record Weight Training | STRAVA25 |
| Life Time member survey (~3,000) | "building muscle was the No. 1 goal for 2024" | CNBC24 |
| Les Mills 2026 Global Fitness Report (>10,000) | "Over half of regular exercisers include some form of strength training"; group strength participation 30 % (2018) → 36 % | LM_GFR26 |
| The Gym Group Annual Report 2023 | "'Fit not Thin' is driving a shift from cardio to strength and functional fitness" | TGG_AR23 |
| Planet Fitness Q3 2023 | "our members are consistently seeking more strength and less cardio"; "Gen Z clearly seems to prefer strength and functional workouts versus cardio"; "Gen Zs are 25% of our member base" | PF_Q3_23 |

### 4.3 US participation trends 2019 → 2023, all settings (SFIA 2024 Topline; US ages 6+; same PAC/SMS survey family as HFA)

| Activity | 2019 | 2023 | 2019→23 | 2022→23 |
|---|---|---|---|---|
| Treadmill | 56.8 M | 54.8 M | -3.5 % | +2.3 % |
| Free weights (dumbbells/hand weights) | 51.4 M | 53.9 M | +4.7 % | +1.4 % |
| Stationary cycling (recumbent/upright) | 37.1 M | 32.6 M | -12.0 % | +1.6 % |
| Weight/resistance machines | 36.2 M | 29.4 M | **-18.7 %** | -1.9 % |
| Free weights (barbells) | 28.4 M | 29.3 M | +3.4 % | +2.3 % |
| Elliptical | 33.1 M | 27.1 M | **-18.1 %** | 0.0 % |
| Kettlebells | 12.9 M | 14.5 M | **+12.5 %** | +5.6 % |
| Stair-climbing machine | 15.4 M | 12.6 M | -17.9 % | **+8.0 %** |
| Rowing machine | 12.8 M | 12.8 M | -0.3 % | **+7.4 %** |
| Cross-training style workouts | 13.5 M | 9.4 M | **-30.6 %** | +1.7 % |
| Stationary cycling (group) | 9.9 M | 6.2 M | **-37.3 %** | -0.7 % |
| Pilates | 9.2 M | 11.9 M | +28.3 % | +15.0 % |
| Yoga | 30.5 M | 34.2 M | +12.5 % | +1.8 % |

Caveat: 2019→2020 includes COVID gym closures. That favoured home-friendly free weights over gym-only machines, so read the 1-year column for current momentum. (I read these numbers from the PDF copy obtained by the sibling exercise slice; sfia.org could not be reached from this session.) [SFIA24]

---

## 5. Equipment trends in new buildouts and refits

### 5.1 Planet Fitness (largest US operator; ~51 % male, Gen Z fastest-growing)
- Q3 2023: "Treadmills still get about the same use, but things like elliptical and bikes are getting far less used." "strength equipment costs less than cardio". "we are also adding additional open spaces for stretching and working out" [PF_Q3_23].
- Q3 2024: "Two years ago, the standard was roughly 100 pieces of cardio and today, it's about 70" ("the reduction of about 30% of the cardio equipment"). "More than 60% of our clubs or more than 1,700 will have the additional pieces of strength equipment". "Removing some of the less utilized cardio equipment frees up floor space". 30-minute-circuit equipment can be moved to "provide additional floor space for members to grab a mat and weights" [PF_Q3_24].
- Q4 2024: "we've pulled back on ellipticals and arc trainers but increased the complement of stair climbers ... and maintained a strong complement of treadmills". "nearly 65% of the estate opting in to put the plate-loaded equipment in their clubs". "there is a greater utilization of strength equipment in our members, or prospective members' workout routines" [PF_Q4_24].
- Q1 2025: "we added the minimal three pieces of plate loaded across 65% of the estate last year"; "nearly 1,800 clubs have the more balanced mix of equipment" [PF_Q1_25].
- Q4 2025: "In 2025, 95% of those who opened or remodeled clubs chose an optimized format"; "nearly 80% of our entire system featuring some version of a format-optimized layout" [PF_Q4_25].
- 2025 Investor Day 8-K: "Moving clubs to a more balanced footprint of cardio and strength equipment"; "Option to remove 30-minute workout area to create space for more functional training" [PF_ID25].
- FY2025 10-K: member base "approximately 51% male"; "Generation Z represents our fastest growing demographic" [PF_10K25].
- **Conflict:** Fitt Insider (Apr 2025) says Planet Fitness was removing "more than 40% of cardio machines across 1.7K locations" [FITT_WOMEN]. The company's own figure is ~30 % (100 → 70). **Recommended: use 30 %** (primary source).

### 5.2 Floor-space allocation (HFA 2025 Global Report, via HCM 20 Aug 2025 and Athletech 11 Aug 2025)
- "modern clubs allocating 42 per cent of floor space to strength training compared with 20 per cent in traditional layouts"; "cardio space has decreased from 34 per cent to 12 per cent" [HFAGLOBAL_HCM].
- "strength zones now occupying 42% of modern gym floor space, the highest share on record ... cardio areas have shrunk to 12% while functional training zones account for 15% of total space" [HFAGLOBAL_ATN].
- The original data supplier is not named in either article. These are shares of *total* club floor, so they do not sum to 100 % (studios, changing rooms and circulation make up the rest).

### 5.3 New UK HVLP build spec and glute machines
- PureGym Leeds City Centre South (2025–26 refit): "over 220+ pieces of gym kit", "An impressive 6-bay lifting rig", "a brand new functional area featuring a fresh sled track, a Hyrox runner", "the game changing perfect squat machine and the BootyBuilder V8" [PG_LEEDS].
- PureGym estate-wide equipment page: "plate-loaded equipment (in most gyms)", dumbbells "up to 50kg (in most gyms)", fixed-resistance "ab machines ... and hip abductors". Battle ropes/TRX only "in some gyms" [PG_EQUIP].
- Booty Builder (vendor claim): hip-thrust machines "quickly became standard equipment across Europe, North America, and Asia"; glute zones are "a must-have feature for many facilities"; machines "installed in gyms across more than 180 countries" [BOOTYBUILDER]. This is self-reported, so low weight.

### 5.4 Functional / HYROX
- HYROX (11 Dec 2024): "recently celebrated its 5,000th global Training Club"; "over 2,300 new clubs affiliated this year"; affiliations "growing at 260% per annum"; "600,000 active racers" [HYROX_PR24].
- HYROX race stations: SkiErg 1000 m, sled push 50 m, sled pull 50 m, burpee broad jumps 80 m, rowing 1000 m, farmers carry 200 m, sandbag lunges 100 m, wall balls 100 reps, plus 8 × 1 km runs [HYROX_RACE]. This maps directly to demand for `turf_lane`, `sled`, `ski_erg`, `rower`, `wall_ball_station` and `kettlebell_set` (farmers carry).
- Counter-signal: US "cross-training style workouts" participation fell 30.6 % (2019–23) [SFIA24]. Rig/box-style functional training is flat; sled/turf and ergs (HYROX-style) are rising.

### 5.5 Machines being cut for low use
Evidence, strongest first:
- ellipticals and arc trainers [PF_Q4_24, PF_Q3_23, HFA25X: 23.2 % → 18.8 %]
- upright/recumbent bikes [PF_Q3_23; PG_MU23: recumbent 31 % least used]
- Powerplate (50 %), sit-up/ab crunch machine (25 %), pedal stepper (22 %), multi-hip/kickback (12 %) [PG_MU23]
- 30-minute circuit machines relocated or removed [PF_Q3_24, PF_ID25]
- No source specifically covers `rotary_torso` (see Gaps).

---

## 6. Demographic differences

### 6.1 Women

**Measured exercise tilt (StrengthLog 2025; share of logged sets, >700,000 users; published 26 Nov 2025)** [STRENGTHLOG25]

| Exercise → equipment | Women % | Men % | W/M |
|---|---|---|---|
| Hip thrust → `hip_thrust_machine` / `hip_thrust_bench` | 2.0 | ~0.215 (from "830% more") | **9.3** |
| Romanian deadlift → bar/dumbbells | 1.7 | 1.1 | **1.55** |
| Leg press → `leg_press` | 2.7 | 1.9 | **1.42** |
| DB shoulder press → dumbbells / `adjustable_bench` | 1.6 | 1.2 | 1.33 |
| DB row → dumbbells / `flat_bench` | 1.5 | 1.2 | 1.25 |
| Squat → `power_rack` | 7.7 | 6.7 | 1.15 |
| Lat pulldown → `lat_pulldown` | 4.1 | 3.6 | 1.14 |
| Deadlift → `lifting_platform` | 5.4 | 4.8 | 1.13 |
| Leg extension → `leg_extension` | 2.7 | 2.4 | 1.13 |
| Seated leg curl / lying leg curl → `leg_curl` | 1.3 / 1.2 | 1.2 / 1.3 | 1.08 / 0.92 |
| Cable close-grip row → `seated_row` / cables | 1.6 | 1.5 | 1.07 |
| Lateral raise → dumbbells | 2.6 | 2.8 | 0.93 |
| Overhead press → `power_rack` / `shoulder_press` | 3.0 | 3.5 | 0.86 |
| Tricep pushdown (bar / rope) → cables | 1.5 / 1.3 | 2.1 / 1.5 | 0.71 / 0.87 |
| Bench press → `bench_press_station` | 8.2 | 10.7 | **0.77** |
| Incline DB press → `adjustable_bench` | 1.3 | 2.1 | 0.62 |
| Barbell curl → `fixed_barbell_set` / `preacher_bench` | 1.4 | 2.4 | **0.58** |
| Pull-up → `dip_chin_station` | <1.0 (not in top 25) | 2.0 | **< 0.5** |
| Hip abduction machine → `hip_abductor_adductor` | 1.0 | <1.1 (not in top 25) | n/a (see fit) |
| Bulgarian split squat → `flat_bench` + dumbbells | 1.4 | <1.1 | > 1.27 |

Quote: "Women train the leg press 42% more and hip thrust 830% more than men." "Men train the bench press 30% more, and the barbell curl 71% more than women."

**Strength Level community data (female share of qualifying results; fetched 28 Oct 2026)** [SL_*]

| Lift | Qualifying results | Female results | Female share |
|---|---|---|---|
| Hip thrust | 383,413 | 224,489 | **58.55 %** |
| Hip abduction | 47,927 | 25,248 | **52.68 %** |
| Hip adduction | 35,674 | 14,321 | 40.14 % |
| Leg press | 728,137 | 158,689 | 21.79 % |
| Leg extension | 372,660 | 74,196 | 19.91 % |
| Lat pulldown | 728,094 | 129,195 | 17.74 % |
| Deadlift | 6,393,746 | 995,561 | 15.57 % |
| Squat | 7,039,938 | 1,024,968 | 14.56 % |
| Bench press | 10,923,537 | 1,017,062 | 9.31 % |
| Barbell curl | 752,509 | 66,256 | 8.80 % |

**Derived W/M for glute machines (derived).** I regressed ln(StrengthLog W/M) on ln(Strength Level F/M odds) over the 8 lifts that appear in both sources: ln(W/M) = 1.746 + 0.980·ln(odds), R² = 0.961. It predicts hip abduction W/M **6.4** and hip adduction **3.9**. Dropping the hip-thrust point gives slope 0.68 and predicts hip abduction **3.6**, adduction **2.5** and hip thrust 4.2 (the measured value is 9.3).

**Recommended women/men ratios (estimates):**
- `hip_thrust_machine` / `hip_thrust_bench`: r = **6.0** (range 4.2–9.3)
- `hip_abductor_adductor` (combo): r = **4.0** (range 3.0–5.3; Fitbod set counts give ≈55 % abduction / 45 % adduction use)
- `glute_kickback`: r = **3.5** (range 2–6). There is no direct gender data, so I used the glute-isolation analogues.
- Other ratios as in the table above.

StrengthLog's own user base is about **35 % female** (derived: least-squares fit of overall = f·W + (1-f)·M over 20 lifts gives f = 0.351). The US member base is **48.5 % female** (derived from HFA's 51.5 % male) [HFA25_DEMO].

**Applying the tilt.** Use demand_e(f) ∝ 1 + f·(r_e − 1), normalised to the reference female share f_ref = 0.485:
m_women(e, f) = (1 + f(r_e − 1)) / (1 + 0.485(r_e − 1)).

| Equipment | r | f=0.20 | f=0.30 | f=0.485 | f=0.60 | f=0.70 | f=0.90 |
|---|---|---|---|---|---|---|---|
| hip thrust (measured r) | 9.30 | 0.53 | 0.69 | 1.00 | 1.19 | 1.36 | 1.69 |
| `hip_thrust_machine`/bench (recommended r) | 6.00 | 0.58 | 0.73 | 1.00 | 1.17 | 1.31 | 1.61 |
| `hip_abductor_adductor` | 4.00 | 0.65 | 0.77 | 1.00 | 1.14 | 1.26 | 1.51 |
| `glute_kickback` | 3.50 | 0.68 | 0.79 | 1.00 | 1.13 | 1.24 | 1.47 |
| `leg_press` | 1.42 | 0.90 | 0.94 | 1.00 | 1.04 | 1.08 | 1.14 |
| RDL-driven dumbbell/bar demand | 1.55 | 0.88 | 0.92 | 1.00 | 1.05 | 1.09 | 1.18 |
| `power_rack` (squat) | 1.15 | 0.96 | 0.97 | 1.00 | 1.02 | 1.03 | 1.06 |
| `bench_press_station` | 0.77 | 1.08 | 1.05 | 1.00 | 0.97 | 0.94 | 0.89 |
| `fixed_barbell_set`/`preacher_bench` | 0.58 | 1.15 | 1.10 | 1.00 | 0.94 | 0.89 | 0.78 |
| `dip_chin_station` | ≤0.50 | 1.19 | 1.12 | 1.00 | 0.92 | 0.86 | 0.73 |

**Other women-specific evidence**
- Crunch (CEO in Bloomberg, cited by Fitt Insider, Apr 2025): women account for "50%+ of lifting platform usage" [FITT_WOMEN].
- Same Fitt piece: Harrison Co. found women's free-weight use **+150 %** and resistance-machine use **+558 %** from 2011 to 2021. CDC: 73 % of US women and 83 % of women 65+ don't meet strength guidelines [FITT_WOMEN].
- Strava: women's weight-training uploads +25 % in 2024 [STRAVA24]; in 2025 women were 21 % more likely than men to record Weight Training [STRAVA25].
- Talker Research for Burn Boot Camp (2,000 US women, 19–24 Feb 2025): "43% of women have never lifted weights at the gym"; among those who have, "55% feel intimidated and worried about how they look"; "42% lack the confidence to lift in front of others" [TALKER25].
- PureGym (25 Oct 2023): 45 % of women vs 29 % of men would be nervous if other gym-goers were fitter [PG_FEAR23].
- University of Winchester / BSA conference (Apr 2019; 25 women interviewed): "most of the women gym users ... avoided the weights section or only used it when there were few men around" [BSA19].
- Older benchmark (HCM 2015, citing IHRSA and Precor): 72 % of female members do group exercise but "only 47 per cent make use of weights and resistance equipment". Women 35–54 allocate 29 % of workout time to strength [HCM15, PRECOR14].
- China (Houlang Research Institute 2025, young people): 53 % of women vs ~70 % of men enjoy free weights, a W/M of about 0.76 for free weights in general [CHINADAILY25].

### 6.2 Older adults (55+ / 65+)
- **Share of members:** 55+ = **22.9 %** of US members in 2024 [HFA25_DEMO]. 65+ members grew **8.6 %** YoY in 2025, the fastest of any cohort [HFA26]. "adults 65 and older now visit gyms and studios more often than any other age group" [ACSM26].
- **Trend priority:** ACSM "Fitness programs for older adults" ranked #4 (2023), #3 (2024), #3 (2025) and **#2 (2026)**. "Balance, flow and core strength" ranked #5 in 2026 [ACSM23–26].
- **Equipment preference (ordinal only):** IHRSA 2018 Media Report: "The Boomer and Silent generations preferred aquatic exercise, stationary cycling, stretching, Tai Chi and weight/resistance machines." "Generation Xers focus on equipment, with ellipticals, cardio cross-trainers, free weights, resistance machines and treadmills topping the list." [IHRSA18]. IHRSA 2019: "Gen Xers and younger Boomers prefer to utilize cardio and strength training equipment" [IHRSA19].
- **Tenure:** members 55+ average "over seven years of membership" vs 2.9 years for ages 18–24 [IHRSA16_HCM].
- **Low recumbent use in young chains:** recumbent bike least used (31 % of PureGym managers) [PG_MU23]. UK low-cost gyms have few older members (The Gym Group AR 2023: 16–24s 29 % are current members, 45–64 10 %, 65+ 4 %; Kantar/Mintel Aug 2023, n=2,000) [TGG_AR23]. Recumbent demand is demographic, not universal.
- Machines for older adults: a search-engine summary of an Athletic Business article (403, **not fetched**) says many older adults use machines because they "require little professional instruction and provide greater stability" [AB_OLDER]. A 2025 network meta-analysis found machine and free-weight outcomes broadly similar, so type selection "might depend on individual preference" (search summary of PubMed 40452461; not fetched).

### 6.3 Gen Z
- Under-25s are **30.8 %** of US members (22.9 % in 2015) [HFA25_DEMO]. Gen Z aged 18–24 have the highest penetration of any age group at **35.5 %** [HFA26].
- Planet Fitness: Gen Z are 25 % of its base (2023) and "clearly seems to prefer strength and functional workouts versus cardio" [PF_Q3_23]; they are the fastest-growing segment and lead joins [PF_Q4_24, PF_10K25]. ABC Fitness: "Twenty-nine percent of new gym joiners are Gen Zers" (Q1 2024) [FORTUNE24].
- Strava 2025: Gen Z 2× Gen X on weight training as primary sport [STRAVA25].
- Les Mills: Gen Z strength exercisers use pin-loaded/cable machines at 82 %; strength is the top group workout; "91% choose a multipurpose (read: big-box) facility equipped with free weights, cardio equipment, and group classes"; 30 % of Gen Z regularly work out in facilities vs 15–25 % of all adults [LM_VILLAGE, LM_GENZ, FITT_GENZ].
- EGYM: Gen Z's top machines are leg extension, hip abduction and step machines [EGYM25].
- TGG Gen Z 2025: 54.8 % include strength training; 12.8 % functional (e.g. HYROX) [TGG_GENZ25].

### 6.4 Beginners and "gymtimidation"
- PureGym (25 Oct 2023) [PG_FEAR23]:
  - "50% of non-gym members say they find the idea of going to the gym scary".
  - "A third of us (32%) said the most intimidating area of the gym was the squat rack", followed by the pull-up/chin-up machine and the bench press.
  - 64 % didn't know how heavy their weights should be; 44 % didn't know how to set up a treadmill; 48 % would be too embarrassed to ask for help.
- Isopure/OnePoll (2,000 US adults, 2019): lifting weights is the most intimidating activity (39 %); "In the free weights section" 10 %; "intimidation by all the machines at the gym (11 percent)" as a reason for a subpar routine [ISOPURE19].
- Les Mills 2026: 50 % of aspiring lifters feel out of place in the weights area; 45 % are unsure of technique; 25 % are unclear how to lift safely [LM_GFR26, LM_CONF].
- Les Mills Gen Z: the barriers "center on a lack of confidence, including feeling intimidated, uneducated, or being on their own" [FITT_GENZ].
- **Implication:** beginner-heavy (HVLP) gyms need visible machine and cable capacity as an on-ramp, but the rack count must still meet experienced-lifter demand. Separate the rack zone, or use half racks around the perimeter, so the weights area feels less exposed.

---

## 7. Derived desirability multipliers

### 7.1 Method (derived; all values `is_estimate=true`)
- **Popularity prior** P_e = 1 + (MU_e − LU_e)/100, from the PureGym manager most-used (MU) and least-used (LU) vote shares (Section 1.2). Unlisted items get 1.0. P_e is clipped to [0.5, 1.5].
- **Trend factor** T_e. Item-specific directional votes override the category default. Votes are counted once per independent *source family*: PF, PAC (SFIA+HFA share one survey), Strava, ClassPass, HYROX, PureGym-new-build, vendor, EGYM, Harrison, ACSM.
  - With item votes: T_e = 1 + 0.05 × clip(net votes, −3, +3).
  - Without: T_e = category default (cardio 0.95, strength 1.05, functional 1.05). The defaults rest on the HFA Global floor-space shift, TGG's "shift from cardio to strength and functional fitness", PF's cardio cut and ACSM's strength ranking. They are deliberately modest, because treadmill reach is still 43.4 %.
- **Recommended multiplier** m_e = √P_e × T_e. The square root avoids double counting when the engine's usage model already reflects popularity. Use P_e × T_e if an item has no separate usage model; use T_e alone if the usage model is fully calibrated. `low`/`high` in the table cover these three variants.

**Vote matrix (source family: sign)**
- treadmill: PF 0 (maintained, "same use"), PAC 0 (-3.5 %/4 y; +2.3 %/1 y) → **T 1.00**
- elliptical: PF −, PAC − (HFA 23.2→18.8 %; SFIA -18.1 %) → **0.90**
- upright_bike, recumbent_bike: PF − ("bikes far less used"), PAC − (-12.0 %) → **0.90**
- indoor_cycle: PAC − (group cycling -37.3 %), ClassPass 0 (+6 %) → **0.95**
- rower: PAC + (+7.4 % 1 y), HYROX + → **1.10**
- stair_climber: PF + ("increased the complement"), PAC 0 (-17.9 % 4 y but +8.0 % 1 y) → **1.05**
- ski_erg: HYROX + → **1.05**
- free-weight stations (racks, platforms, benches, dumbbells, fixed barbells, kettlebells): PAC + (HFA "fastest-growing"), Strava +, ClassPass + (strength +27 %, gym time +51 %) → **1.15**
- plate-loaded (leg press, hack squat, iso-lateral chest/row/shoulder/high-row, T-bar): PF + (≥3 pieces in 65 % of estate) → **1.05**
- belt/pendulum squat: PureGym new-build + ("perfect squat machine") → **1.05**
- hip_thrust_machine: PureGym new-build + (BootyBuilder), vendor + → **1.10**
- selectorized (generic): PAC − (resistance machines 31.4→26.6 %; SFIA -18.7 %), Harrison + (women +558 %) → **1.00**
- leg_extension, hip_abductor_adductor: selectorized + EGYM + (Gen Z top picks) → **1.05**
- turf_lane, sled: HYROX +, PureGym new-build + (sled track), PF + (functional space) → **1.15**
- rig_bay: PAC − (cross-training -30.6 %), PureGym new-build + (6-bay rig) → **1.00**
- wall_ball_station: HYROX +, PAC − → **1.00**
- plyo_box_set: PAC − → **0.95**
- heavy_bag: PAC − (cardio kickboxing -21.4 %), ClassPass − (boxing -7 %) → **0.90**
- stretch_area: ACSM + (balance/flow/core #5), PF + (stretching space), PAC + (yoga +12.5 %, Pilates +28.3 %) → **1.15**

### 7.2 Result table

| equipment_id | P_e | T_e | **m_e** | low | high |
|---|---|---|---|---|---|
| `power_rack` | 1.49 | 1.15 | **1.40** | 1.15 | 1.71 |
| `half_rack` | 1.49 | 1.15 | **1.40** | 1.15 | 1.71 |
| `lifting_platform` | 1.37 | 1.15 | **1.35** | 1.15 | 1.58 |
| `dumbbell_set_light` | 1.26 | 1.15 | **1.29** | 1.15 | 1.45 |
| `dumbbell_set_full` | 1.26 | 1.15 | **1.29** | 1.15 | 1.45 |
| `dumbbell_heavy_extension` | 1.00* | 1.15 | **1.15** | 1.15 | 1.15 |
| `bench_press_station` | 1.18 | 1.15 | **1.25** | 1.15 | 1.36 |
| `fixed_barbell_set` | 1.11 | 1.15 | **1.21** | 1.15 | 1.28 |
| `stair_climber` | 1.30 | 1.05 | **1.20** | 1.05 | 1.37 |
| `cable_crossover` / `functional_trainer` / `cable_column` | 1.27 | 1.05 | **1.18** | 1.05 | 1.33 |
| `treadmill` | 1.33 | 1.00 | **1.15** | 1.00 | 1.33 |
| `incline_bench_station` / `decline_bench_station` / `adjustable_bench` / `flat_bench` | 1.00 | 1.15 | **1.15** | 1.15 | 1.15 |
| `kettlebell_set` | 1.00 | 1.15 | **1.15** | 1.15 | 1.15 |
| `turf_lane` / `sled` | 1.00 | 1.15 | **1.15** | 1.15 | 1.15 |
| `stretch_area` | 1.00 | 1.15 | **1.15** | 1.15 | 1.15 |
| `rower` | 1.00 | 1.10 | **1.10** | 1.10 | 1.10 |
| `leg_press` | 1.10 | 1.05 | **1.10** | 1.05 | 1.16 |
| `hip_thrust_machine` | 1.00 | 1.10 | **1.10** | 1.10 | 1.10 |
| `leg_extension` | 1.08 | 1.05 | **1.09** | 1.05 | 1.13 |
| `smith_machine`, `preacher_bench`, `hyperextension`, `ghd`, `dip_chin_station`, `hip_thrust_bench`, `landmine` | 1.00 | 1.05 | **1.05** | 1.05 | 1.05 |
| `hack_squat`, `belt_squat`, `plate_loaded_chest_press`, `plate_loaded_row`, `plate_loaded_shoulder_press`, `plate_loaded_high_row`, `t_bar_row` | 1.00 | 1.05 | **1.05** | 1.05 | 1.05 |
| `hip_abductor_adductor` | 1.00 | 1.05 | **1.05** | 1.05 | 1.05 |
| `battle_rope_station`, `accessory_pack` | 1.00 | 1.05 | **1.05** | 1.05 | 1.05 |
| `leg_ext_curl_combo` | 1.08 | 1.00 | **1.04** | 1.00 | 1.08 |
| `leg_curl`, `calf_raise`, `chest_press`, `pec_fly_rear_delt`, `shoulder_press`, `lat_pulldown`, `seated_row`, `lat_pulldown_row_combo`, `assisted_pullup_dip`, `biceps_curl_machine`, `triceps_machine`, `back_extension_machine`, `rotary_torso`, `multi_station_gym` | 1.00 | 1.00 | **1.00** | 1.00 | 1.00 |
| `rig_bay`, `wall_ball_station` | 1.00 | 1.00 | **1.00** | 1.00 | 1.00 |
| `suspension_trainer_station` | 0.90 | 1.05 | **1.00** | 0.95 | 1.05 |
| `ski_erg` | 0.83 | 1.05 | **0.96** | 0.87 | 1.05 |
| `curved_treadmill`, `indoor_cycle`, `air_bike`, `recumbent_stepper`, `plyo_box_set` | 1.00 | 0.95 | **0.95** | 0.95 | 0.95 |
| `glute_kickback` | 0.88 | 1.00 | **0.94** | 0.88 | 1.00 |
| `elliptical`, `upright_bike`, `heavy_bag` | 1.00 | 0.90 | **0.90** | 0.90 | 0.90 |
| `ab_crunch_machine` | 0.75 | 1.00 | **0.87** | 0.75 | 1.00 |
| `recumbent_bike` | 0.69 | 0.90 | **0.75** | 0.62 | 0.90 |

\*PureGym's "Dumbbells 26 %" refers to standard dumbbells (PureGym stocks "up to 50kg in most gyms"). The 105–150 lb extension serves a niche of advanced (mostly male) lifters, so I set its P to 1.0.

**Small vs. large gyms.** For a *small* gym, pick distinct items in roughly m_e order for diversity:
1. rack (+ bar/plates)
2. dumbbells
3. adjustable bench
4. cable/functional trainer
5. treadmill
6. stair climber or rower
7. leg press / leg extension combo
8. lat-pulldown/row combo
9. hip thrust (bench or machine, scaled by the women share)
10. stretch/turf space

For a *large* gym, duplicate the items with the highest m_e and the highest contention: racks, benches, dumbbell bays, cables, treadmills and stair climbers. Then add breadth: plate-loaded, glute machines and turf/sled. Avoid duplicating ellipticals, recumbents (unless the gym skews older), ab crunch and multi-hip machines.

### 7.3 Demographic tilt ratios beyond gender (estimates, low confidence)
No published equipment-by-age usage ratios were found. These are ordinal-to-ratio mappings of the evidence in Sections 6.2–6.4, on the ladder {0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5, 2.0, 2.5, 3.0}. Apply them as m = (1 + x(r−1)) / (1 + x_ref(r−1)), where x is the facility's share of the group. Reference shares: x_ref = 0.229 for 55+ and 0.308 for under-25s [HFA25_DEMO]. Calibrate against real check-in or equipment telemetry when available.

| equipment | r 55+ | r Gen Z (<25) | r beginner | Evidence |
|---|---|---|---|---|
| `recumbent_bike` | 2.5 | 0.4 | 1.3 | IHRSA: boomers prefer stationary cycling; PG least used in young chain |
| `recumbent_stepper` | 3.0 | 0.3 | 1.2 | Designed for older/rehab users; older-adult ACSM #2 |
| `upright_bike` | 1.5 | 0.6 | 1.2 | IHRSA (boomers); PF "bikes far less used" with Gen Z-led joins |
| `elliptical` | 1.2 | 0.6 | 1.2 | IHRSA (Gen X uses ellipticals); PF/HFA declines |
| `treadmill` | 1.2 | 0.9 | 1.2 | HFA most used; PureGym: 44 % don't know set-up (still beginner default) |
| `stair_climber` | 0.7 | 1.2 | 0.9 | EGYM Gen Z top-3 step machines; PF adding |
| selectorized machines | 1.3 | 1.1 | 1.3 | IHRSA boomers resistance machines; Les Mills 82 % Gen Z pin/cable; beginners avoid free-weight area |
| `leg_extension`, `hip_abductor_adductor` | 1.2 | 1.3 | 1.3 | EGYM Gen Z top picks |
| cables | 1.0 | 1.1 | 1.1 | Les Mills 82 % pin/cable |
| `power_rack`/`half_rack` | 0.4 | 1.3 | 0.6 | PureGym squat rack most intimidating (32 %); Strava Gen Z 2× weight training |
| `lifting_platform` | 0.3 | 1.2 | 0.5 | as above |
| bench stations | 0.6 | 1.2 | 0.8 | bench press 3rd most intimidating |
| dumbbells (light/full) | 0.9 | 1.2 | 1.0 | HFA free weights fastest-growing |
| `dumbbell_heavy_extension` | 0.3 | 1.3 | 0.4 | advanced-lifter niche |
| plate-loaded machines | 0.7 | 1.2 | 0.9 | PF plate-loaded add for Gen Z-led base |
| `hip_thrust_machine` | 0.6 | 1.3 | 1.0 | gender effect dominates; young-female skew |
| `turf_lane`/`sled` | 0.4 | 1.2 | 0.7 | HYROX / TGG functional 12.8 % |
| `stretch_area` | 1.3 | 1.0 | 1.1 | ACSM balance/core #5; IHRSA boomers stretching |
| `assisted_pullup_dip` | 1.2 | 1.0 | 1.2 | beginner/older on-ramp for pull-ups |
| `dip_chin_station` | 0.5 | 1.2 | 0.7 | pull-up station 2nd most intimidating |

---

## 8. Conflicts and resolutions

| Topic | Source A | Source B | Recommendation |
|---|---|---|---|
| ACSM 2025 rank of functional fitness | #9 (2025 HFJ Table 3) | "up from #12 in 2025" (2026 coverage: karmactive, ES summary) | Use **#9**, the primary table |
| ACSM 2026 sample | "survey of 2,000" (ACSM) | 1,540 valid of 2,038 (ES summary) | Report ~2,000 invited/received; 1,540 valid if the ES summary is right |
| PF cardio reduction | ~30 % (100 → 70 pieces; CEO, Q3 2024) | ">40% of cardio machines" (Fitt Insider) | **30 %** (primary) |
| Resistance machines: declining or growing? | HFA: member use 31.4 % → 26.6 % (2021–24); SFIA -18.7 % (2019–23) | PF adds plate-loaded; EGYM Gen Z top machines; Harrison women +558 % | Selectorized **flat (T=1.00)**; plate-loaded **slightly up (1.05)**. Machines remain the beginner on-ramp |
| Treadmill vs shrinking cardio floor | HFA Global: cardio space 34 % → 12 % | HFA usage 43.4 % (most used); PF "maintained a strong complement of treadmills" | Keep treadmills (T=1.00); take the cardio cuts from ellipticals, bikes and arc trainers |
| SkiErg | PureGym 17 % least used | HYROX growth (SkiErg is station 1) | m=0.96; include in functional/HYROX-oriented or larger gyms only |
| TRX | 10 % least used (2023) | 19 % of managers rate it most effective for overall fitness (2019) | m=1.00; cheap, wall-mounted, low priority |
| Recumbent bike | 31 % least used (young UK chain) | IHRSA boomers prefer stationary cycling; 65+ the fastest-growing cohort | Base m=0.75 × older-adult tilt (r=2.5) |
| Hip-thrust W/M | StrengthLog 9.3 | Strength Level fit without hip thrust 4.2 | r = 6.0 (range 4.2–9.3) |
| Free weights, Gen Z gateway | Les Mills: free weights ranked 5th as a *gateway* workout (search summary) | Gen Z 2× weight training as primary sport (Strava); strength top group workout | Gateway ≠ steady state; beginners start on cardio/machines, then migrate to free weights |

---

## 9. Gaps
- **No large-sample, equipment-specific queue/wait-time study** (minutes waited per rack/bench/cable) was found. The evidence is manager perception, annoyance surveys and one club audit (not fetched). Suggest instrumenting with operator data or using the occupancy slice's Erlang outputs.
- **No published usage ratios by age group for specific machines** (recumbent, NuStep, selectorized). The older-adult, Gen Z and beginner ratios in 7.3 are estimates.
- **Rotary torso, ab crunch, back-extension machine utilisation:** the only direct data is PureGym's "sit-up machine" (25 % least used). Nothing was found on rotary torso.
- **Glute kickback gender split:** no direct data; r = 3.5 is inferred from analogues.
- **Belt squat / pendulum squat adoption counts:** only qualitative (PureGym "perfect squat machine").
- **HFA Global Report:** the original data supplier and method behind the 42 % / 12 % / 15 % floor shares are not disclosed in the coverage.
- **Members-only sources not read:** the full HFA 2025/2026 consumer reports (gender/age × equipment tables), the Les Mills 2026 GFR PDF, the EGYM *Strength Shift* whitepaper, Mintel UK Health & Fitness Clubs, and the Which? 2025 chain scores.
- **Mindbody consumer-survey percentages** (beyond ClassPass bookings) and Garmin Connect strength-activity growth were not retrieved.
- **The "gymtok" / TikTok trend** has no quantitative datapoint.

---

## 10. Sources

| id | Title | Publisher | Year | URL | Fetched |
|---|---|---|---|---|---|
| ACSM26 | 2026 fitness trends (Top 10) | ACSM | 2025 | https://acsm.org/top-fitness-trends-2026 | yes |
| ACSM26_ES | ACSM 2026 tendencias mundiales del fitness (top 20) | ENFAF | 2025 | https://enfaf.com/acsm-2026-tendencias-mundiales-del-fitness/ | yes |
| ACSM26_KARM | ACSM Top Fitness Trends 2026 coverage | Karmactive | 2025 | https://www.karmactive.com/acsm-top-fitness-trends-2026-wearables-hold-1-mental-health-surges-to-top-6-strength-training-gaps-persist/ | yes |
| ACSM25 | 2025 ACSM Worldwide Fitness Trends: Future Directions (HFJ 28(6)) | ACSM / LWW (hosted by CSParks) | 2024 | https://www.csparks.org/wp-content/uploads/2025/01/2025_acsm_worldwide_fitness_trends__future.6.pdf | yes (curl + pdftotext) |
| ACSM25_WEB | Top fitness trends 2025 | ACSM | 2024 | https://acsm.org/top-fitness-trends-2025/ | yes |
| ACSM24 | Wearable Technology Named Top Fitness Trend for 2024 | ACSM | 2023 | https://acsm.org/top-fitness-trends-2024/ | yes |
| ACSM23 | Wearable Technology Named Top Fitness Trend for 2023 | ACSM via Newswise | 2022 | https://www.newswise.com/articles/wearable-technology-named-top-fitness-trend-for-2023 | yes |
| HFA25X | How 77 Million Fitness Members Work Out | Health & Fitness Association | 2025 | https://www.healthandfitness.org/how-77-million-fitness-members-work-out-new-hfa-data-reveals-shifting-equipment-training-and-membership-trends/ | yes |
| HFA25X_PR | New HFA Data Shows How 77 Million US Fitness Facility Members Work Out | HFA | 2025 | https://www.healthandfitness.org/new-hfa-data-shows-how-77-million-us-fitness-facility-members-work-out | yes |
| HFA26 | 81 Million Americans Were Members of a Fitness Facility in 2025 | HFA | 2026 | https://www.healthandfitness.org/?p=5212 | yes |
| SGB26 | HFA: gym membership climbs in 2025 | SGB Online | 2026 | https://sgbonline.com/hfa-gym-membership-climbs-5-6-percent-in-2025/ | yes |
| HFA25_DEMO | US gyms younger, more male: HFA report | Athletech News | 2025 | https://athletechnews.com/us-gyms-younger-more-male-hfa-report/ | yes |
| HFAGLOBAL_HCM | The HFA's annual report shows the global fitness industry is resilient | Health Club Management | 2025 | https://www.healthclubmanagement.co.uk/health-club-management-news/The-HFAs-annual-report-shows-the-global-fitness-industry-is-resilient-and-poised-for-growth/356856 | yes |
| HFAGLOBAL_ATN | HFA Global Report fitness industry | Athletech News | 2025 | https://athletechnews.com/hfa-global-report-fitness-industry/ | yes |
| HFA23 | IHRSA Releases 2023 U.S. Health & Fitness Consumer Report | HFA | 2023 | https://www.healthandfitness.org/?p=1195 | yes |
| IHRSA19 | Report: Health Club, Gym & Studio Usage Reach All-Time High (2019 Consumer Report) | IHRSA/HFA | 2019 | https://www.healthandfitness.org/?p=2273 | yes |
| IHRSA18 | IHRSA Report Shows Healthy Fitness Market (2018 Media Report, 2016 data) | SGB Online | 2018 | https://sgbonline.com/?p=115573 | yes |
| IHRSA16_HCM | IHRSA update: key findings from the 2016 Health Club Consumer Report | Health Club Management | 2016 | https://www.healthclubmanagement.co.uk/health-club-management-features/IHRSA-update-A-look-at-the-key-findings-from-2016-IHRSA-Health-Club-Consumer-Report/31225 | yes |
| PF_Q3_23 | Planet Fitness Q3 2023 earnings call | AllMind (transcript) | 2023 | https://allmind.ai/earnings/event/bt_PLNT_2023_Q3 | yes |
| PF_Q3_24 | Planet Fitness Q3 2024 earnings call | AllMind | 2024 | https://allmind.ai/earnings/event/bt_PLNT_2024_Q3 | yes |
| PF_Q4_24 | Planet Fitness Q4 2024 earnings call | AllMind | 2025 | https://allmind.ai/earnings/event/bt_PLNT_2024_Q4 | yes |
| PF_Q1_25 | Planet Fitness Q1 2025 earnings call | AllMind | 2025 | https://allmind.ai/earnings/event/bt_PLNT_2025_Q1 | yes |
| PF_Q4_25 | Planet Fitness Q4 2025 earnings call | AllMind | 2026 | https://allmind.ai/earnings/event/bt_PLNT_2025_Q4 | yes |
| PF_ID25 | Planet Fitness 2025 Investor Day presentation (8-K exhibit) | SEC EDGAR | 2025 | https://www.sec.gov/Archives/edgar/data/1637207/000163720725000059/planetfitnessincinvestor.htm | yes |
| PF_10K25 | Planet Fitness FY2025 Form 10-K | SEC EDGAR | 2026 | https://www.sec.gov/Archives/edgar/data/1637207/000163720726000011/plnt-20251231.htm | yes (partial) |
| CNBC24 | As strength training gets more popular, Peloton and Planet Fitness shift focus | CNBC (via NBC Connecticut) | 2024 | https://www.nbcconnecticut.com/news/business/money-report/as-strength-training-gets-more-popular-peloton-and-planet-fitness-shift-focus/3367888/ | yes |
| YPULSE26 | Planet Fitness says Gen Z is leading the golden age of fitness | YPulse | 2026 | https://www.ypulse.com/newsfeed/2026/01/12/planet-fitness-says-gen-z-is-leading-the-golden-age-of-fitness-right-now/ | yes |
| FITT_WOMEN | Women usher in strength training's new era | Fitt Insider | 2025 | https://insider.fitt.co/women-usher-in-strength-trainings-new-era/ | yes |
| TGG_AR23 | The Gym Group Annual Report and Accounts 2023 | The Gym Group plc | 2024 | https://prelive.tggplc.com/media/tu2menvr/tgg_ar23.pdf | yes (copy from sibling slice) |
| TGG_GENZ25 | Gen Z Fitness Pulse Report 2025 | The Gym Group plc | 2025 | https://www.tggplc.com/media/4luo4kpk/tgg-pr-gen-z-survey-report-2025.pdf | yes (pdftotext) |
| LM_GENZ | Landmark report lifts the lid on Gen Z fitness | Les Mills | 2024 | https://www.lesmills.com/us/clubs-and-facilities/research-insights/fitness-trends/landmark-report-lifts-the-lid-on-gen-z-fitness/ | yes |
| LM_VILLAGE | Village Gyms taps into strength training trend | Les Mills | 2023 | https://www.lesmills.com/nordic/articles/village-gyms-taps-into-strength-training-trend-to-turbocharge-member-attendance-and-engagement | yes |
| LM_ATTRACT | Attract the next generation into your classes | Les Mills | 2023 | https://www.lesmills.com/uk/articles/attract-the-next-generation-into-your-classes | yes |
| LM_GFR26 | 2026 Global Fitness Report: strength and wellness to drive next wave of member growth | Les Mills | 2026 | https://www.lesmills.com/clubs-and-facilities/research-insights/fitness-trends/2026-global-fitness-report-strength-and-wellness-to-drive-next-wave-of-member-growth/ | yes |
| LM_CONF | Strength has a confidence crisis | Les Mills | 2026 | https://www.lesmills.com/nordic/articles/strength-has-a-confidence-crisis-heres-how-your-club-can-solve-it | yes |
| LM_PM25 | Phillip Mills: 5 group training picks for 2025 | Les Mills | 2024 | https://www.lesmills.com/articles/phillip-mills-5-group-training-picks-for-2025 | yes |
| FITT_GENZ | Issue No. 240: Gen Z x Fitness | Fitt Insider | 2023 | https://insider.fitt.co/issue-no-240-gen-z-x-fitness/ | yes |
| FORTUNE24 | Gym use increase, Gen Z (ABC Fitness Wellness Watch) | Fortune | 2024 | https://fortune.com/well/article/gym-use-increase-pandemic-gen-z/ | yes |
| STRAVA24 | Strava 2024 fitness report highlights trends | Athletech News | 2024 | https://athletechnews.com/strava-2024-fitness-report-highlights-trends | yes |
| STRAVA25 | Strava Releases 12th Annual Year in Sport Trend Report | Strava (via Webull/press wire) | 2025 | https://www.webull.com/news/13961203642123264 | yes |
| STRAVA23 | Strava Year in Sport Trend Report (motivation across generations) | Strava (PR Newswire) | 2024 | https://prnewswire.com/news-releases/strava-releases-year-in-sport-trend-report-showing-what-makes-and-breaks-motivation-across-generations-302019644.html | yes |
| CLASSPASS25 | Pilates dominates fitness bookings for ClassPass in 2025 | SGB Online | 2025 | https://sgbonline.com/pilates-dominates-fitness-bookings-for-classpass-in-2025/ | yes |
| PG_MU23 | When is the gym quiet? (most/least used equipment) | PureGym | 2023 | https://www.puregym.com/blog/when-is-the-gym-quiet/ | yes |
| PG_EFF19 | The Six Most Effective Gym Machines, According to Gym Managers | PureGym (ResponseSource) | 2019 | https://pressreleases.responsesource.com/newsroom/Puregym/release/98110/?print=true | yes |
| PG_FEAR23 | Feeling scared of the gym? You're not alone | PureGym | 2023 | https://www.puregym.com/blog/gym-fear-intimidation-report/ | yes |
| PG_LEEDS | PureGym Leeds City Centre South | PureGym | 2025 | https://one.puregym.com/gyms/leeds-city-centre-south | yes |
| PG_EQUIP | PureGym equipment | PureGym | 2026 | https://puregym.com/equipment | yes |
| ISOPURE19 | Gymtimidation prevents Americans from exercising more often | Fox News (OnePoll/Isopure) | 2019 | https://www.foxnews.com/lifestyle/gymtimidation-prevents-a-percentage-of-americans-from-exercising-more-often-study-claims | yes |
| TALKER25 | What are women's top health goals for 2025 | Talker Research (Burn Boot Camp) | 2025 | https://talkerresearch.com/what-are-womens-top-health-goals-for-2025/ | yes |
| BSA19 | Women put off using the weights sections of gyms by intimidatory atmosphere among men | British Sociological Association | 2019 | https://es.britsoc.co.uk/women-put-off-using-the-weights-sections-of-gyms-by-intimidatory-atmosphere-among-men-says-research/ | yes |
| HCM15 | Strength training: Empowering women | Health Club Management | 2015 | https://www.healthclubmanagement.co.uk/health-club-management-features/Strength-training-Empowering-women/29698 | yes |
| PRECOR14 | Women's weight training could be key to growing gym market (Precor study) | Leisure Opportunities | 2014 | http://www.leisureopportunities.co.uk/news/Women%E2%80%99s-weight-training-could-be-key-to-growing-gym-market-study/308388 | yes |
| STRENGTHLOG25 | Most Popular Gym Exercises for Men & Women in 2025 | StrengthLog | 2025 | https://www.strengthlog.com/most-popular-exercises/ | yes |
| SL_HIPTHRUST | Hip Thrust Strength Standards | Strength Level | 2026 | https://strengthlevel.com/strength-standards/hip-thrust | yes |
| SL_HIPABD | Hip Abduction Strength Standards | Strength Level | 2026 | https://strengthlevel.com/strength-standards/hip-abduction | yes |
| SL_HIPADD | Hip Adduction Strength Standards | Strength Level | 2026 | https://strengthlevel.com/strength-standards/hip-adduction | yes |
| SL_SQUAT | Squat Strength Standards | Strength Level | 2026 | https://strengthlevel.com/strength-standards/squat | yes |
| SL_BENCH | Bench Press Strength Standards | Strength Level | 2026 | https://strengthlevel.com/strength-standards/bench-press | yes |
| SL_DEADLIFT | Deadlift Strength Standards | Strength Level | 2026 | https://strengthlevel.com/strength-standards/deadlift | yes |
| SL_LEGPRESS | Leg Press Strength Standards | Strength Level | 2026 | https://strengthlevel.com/strength-standards/leg-press | yes |
| SL_LEGEXT | Leg Extension Strength Standards | Strength Level | 2026 | https://strengthlevel.com/strength-standards/leg-extension | yes |
| SL_LATPD | Lat Pulldown Strength Standards | Strength Level | 2026 | https://strengthlevel.com/strength-standards/lat-pulldown | yes |
| SL_BBCURL | Barbell Curl Strength Standards | Strength Level | 2026 | https://strengthlevel.com/strength-standards/barbell-curl | yes |
| CHINADAILY25 | Gym life working out for more women | China Daily | 2025 | https://www.chinadaily.com.cn/a/202506/10/WS684783c5a310a04af22c411e_3.html | yes |
| EGYM25 | Gen Z, Millennials, strength training, wearables: EGYM report | Athletech News | 2025 | https://athletechnews.com/gen-z-millennials-strength-training-wearables-egym-report/ | yes |
| EGYM25_PR | EGYM data shows how Gen Z & Millennials are shaping fitness | EGYM (Fitt Insider press release) | 2025 | https://insider.fitt.co/press-release/egym-data-shows-how-gen-z-millennials-are-shaping-fitness | yes |
| YOUGOV22 | What are people looking for in a gym membership? | YouGov | 2022 | https://yougov.com/articles/41119-uk-what-are-people-looking-gym-membership | yes |
| WHICH25 | Best and worst gyms rated | Which? | 2025 | https://www.which.co.uk/reviews/gyms/article/best-and-worst-gyms-rated-azhqg5g2z1B6 | yes (member tables locked) |
| SOGO26 | Why gym members quit (study) | Sogolytics | 2026 | https://www.sogolytics.com/blog/why-gym-members-quit-study/ | yes |
| GGR24 | Bad gym habits (survey of 2,000) | Garage Gym Reviews | 2024 | https://www.garagegymreviews.com/bad-gym-habits | yes |
| BANANAMOON | 6 reasons why people put off going to the gym | Hartlepool Mail | n.d. | https://hartlepoolmail.co.uk/news/6-reasons-why-people-put-off-going-to-the-gym-360267 | **no** (403) |
| PARKWOOD | Purposeful Gym Design (Parkwood Health & Fitness utilisation) | leisurecentre.com | n.d. | https://leisurecentre.com/Purposeful-Gym-Design | **no** (406/empty) |
| PRINCETON26 | Tigerwell Supplement Lakeside Survey Results | Princeton University Lakeside Committee | 2026 | https://lakesidecommittee.princeton.edu/wp-content/uploads/sites/315/2026/01/Tigerwell-Supplement-Lakeside-Survey-Results.pptx.pdf | **no** (image-only) |
| COLUMBIAN17 | Don't Be A Quitter (reasons for not renewing) | The Columbian blog | 2017 | https://blogs.columbian.com/sherri-mcmillan/?p=2007 | yes |
| HYROX_PR24 | HYROX celebrates 5,000 Training Clubs | HYROX (Fitt Insider press release) | 2024 | https://insider.fitt.co/press-release/hyrox-celebrates-5000-training-clubs-and-launch-of-its-performance-centers/ | yes |
| HYROX_RACE | The Fitness Race | HYROX | 2026 | https://hyrox.com/the-fitness-race/ | yes |
| BOOTYBUILDER | The History of the Hip Thrust Machine | Booty Builder | 2026 | https://bootybuilder.com/?p=11934 | yes |
| SFIA24 | 2024 Topline Participation Report (2023 data) | Sports & Fitness Industry Association | 2024 | https://sfia.org/resource_categories/research-insights/ | **no** (sfia.org DNS failure; numbers read from the PDF copy obtained by the sibling exercise slice) |
| AB_OLDER | Resistance training facilitates daily activity for elders | Athletic Business | n.d. | https://www.athleticbusiness.com/operations/programming/news/15150087/resistance-training-facilitates-daily-activity-for-elders | **no** (403) |

Supporting computation scripts were kept in a local research workspace (not included in this repository):
- `gender_tilt.py`: Strength Level × StrengthLog fit
- `desirability.py` and `desirability_final.json`: P/T/m table
