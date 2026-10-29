# Research slice: Average gym-goer behavior & time allocation by modality (topic = `usage`)

Prepared for the gym-layout planner (demand model → Erlang loss routing → budget/space selection → floor packing).
Every number below is tagged with a source id `[Sxx]` (full list at the end). Values I derived or estimated are
explicitly labelled **ESTIMATE** / **DERIVED** with the arithmetic shown. Research date: 2026-10-28.

> Research constraint: the session-wide web-search budget (shared with other research agents) ran out several times,
> so some lines of inquiry (Mintel, Mindbody, peer-reviewed SOPARC-style gym observation studies, SFIA 2025/2026
> activity-level tables) could not be exhausted. sfia.org itself did not resolve (DNS failure), so the newest SFIA
> activity-level table I could read directly is the **2024 Topline (2023 data)**, read page-by-page from a PDF copy.

---

## 0. Model-ready summary (recommended values)

All recommended values are **ESTIMATES** built from the evidence in sections 2–7; derivations are in section 3.3–3.6 and 9.

### 0.1 Share of on-floor exercise minutes by modality (excludes group-class studio time)

| Modality (engine bucket) | Average member | Strength-focused gym | Cardio/wellness-focused gym | Functional-focused gym |
|---|---|---|---|---|
| Cardio machines | **35%** | 20% | 47% | 22% |
| Barbell / rack / platform / bench-press stations | **11.5%** | 22% | 4% | 22% |
| Dumbbells (+ adjustable/flat benches) | **17.5%** | 20% | 12% | 8% |
| Machines (selectorized + plate-loaded, incl. lat-pulldown/row stacks) | **17%** | 18% | 22% | 2% |
| Cables (crossover / functional trainer / cable column) | **6%** | 8% | 4% | 1% |
| Functional / turf / rig / kettlebell / sled | **7%** | 6% | 3% | 40% |
| Stretch / mobility / core mats | **6%** | 6% | 8% | 5% |
| **Strength ÷ (strength + cardio)** | **≈60%** | ≈77% | ≈47% | ≈60% (+40% functional) |

### 0.2 Cardio sub-mix (share of cardio minutes)

| Equipment id | Average | Strength-focused | Cardio/wellness | Functional |
|---|---|---|---|---|
| treadmill | 40 | 38 | 40 | 15 |
| curved_treadmill | 1 | 3 | 0 | 15 |
| elliptical | 15 | 8 | 20 | 0 |
| upright_bike | 11 | 8 | 10 | 0 |
| recumbent_bike | 8 | 3 | 12 | 0 |
| indoor_cycle (free use, not classes) | 3 | 3 | 2 | 0 |
| air_bike | 2 | 6 | 1 | 25 |
| rower | 7 | 8 | 4 | 25 |
| stair_climber | 10 | 18 | 6 | 0 |
| ski_erg | 1 | 3 | 0 | 20 |
| recumbent_stepper | 2 | 2 | 5 | 0 |

### 0.3 Other core parameters

| Parameter | Recommended | Range | Basis |
|---|---|---|---|
| Visits per member per week (all members) | **1.5** | 0.95–1.95 | HFA 75 days/yr (2022) → ≤86/yr (2025); IHRSA ~100/yr (2016); Placer/DellaVigna ~1.0/wk at low-cost/flat-fee clubs |
| Visits/week, HVLP / cardio-wellness club members | 1.2 | 0.95–1.6 | Placer PF 4.1–4.4 visits per visitor-month; PF internal 6.1→6.5–6.9 per *active* member-month |
| Visits/week, strength-focused (enthusiast) members | 2.0 | 1.4–3.3 | Life Time 5.7–6.2/mo; app lifters 2.7 (median) – 3.3 (mean) workouts/wk |
| Members who never use membership | **4.6%** | 4.6–10% | HFA 2025 |
| Time in building per visit | **70 min** | 66–74 | PureGym gate data 66–69 min; Placer HVLP 74 min |
| Time actively on gym floor per visit | **55 min** | 50–60 | Boostcamp median logged workout 58 min; Strava strength ~50 min; ATUS 42–54 min/day by activity |
| Strength station holding time per exercise | **9 min** | 4–15 | Boostcamp 58 min ÷ 6 exercises = 9.7 min; sensor: 3×10 machine sets in ~4 min |
| Cardio bout length | **25 min** | 10–45 | ATUS 42 min/day on cardio-equipment days; sensor: elliptical bouts 10–30+ min |
| Strength-share drift (S/C time ratio) | **+2%/yr** | 0–3%/yr | SFIA 2019→2023 occasion ratio ×1.099 (+2.4%/yr); 2025 "cardio comeback" tempers it |
| Strength ÷ (strength+cardio) time, men / women | 70% / 45% | 65–75 / 40–50 | ATUS 2009-15 sex split (67.5% / 39.3%) × SFIA shift; Strava 2025 female lifting growth |
| Strength ÷ (strength+cardio) time, age 18–24 / 25–54 / 55+ | 77% / 58% / 42% | ±5 pts | ATUS 2009-15 age split × SFIA shift |

---

## 1. Source quality notes

* **HFA (formerly IHRSA) U.S. Health & Fitness Consumer Report** – annual survey of ~18,000 Americans aged 6+ run by Sports Marketing Surveys USA for the Physical Activity Council [S4][S6][S12]. Best source for *member* usage shares. Full reports are paywalled; numbers here come from HFA's own press pages/articles.
* **SFIA Topline Participation Report** – same PAC survey (18,000 online interviews, U.S. 6+, weighted to 306.9M people; "CORE" fitness participant = 50+ times/yr) [S1]. Population-wide (includes home exercise), but the only source that splits barbell vs dumbbell vs machines and every cardio machine type, with mean days/yr and total occasions.
* **BLS American Time Use Survey (ATUS)** – time-diary data (the closest thing to an observational national measure of minutes) [S22][S23].
* **Placer.ai / HFA FIT Tracker** – passive mobile-location panel: visit frequency and dwell time [S14][S15][S16][S17].
* **Operator data** – PureGym entry/exit data [S18][S19]; Planet Fitness SEC filings and earnings calls [S28–S31].
* **App logs** – StrengthLog (700k+ users), Boostcamp (1M workout logs), Fitbod (15.8M workouts/yr), Strava (180M users), Garmin Connect [S36–S51]. Self-selected (enthusiasts), but they reveal the *exercise-level* mix inside strength sessions.
* **Sensor/observational studies** – GYMetrix (equipment sensors, ~400 UK gyms), YMCA/Track My Gym, U. Calgary sensor thesis, Penn State survey [S52–S57].

---

## 2. (a) Who uses which modality

### 2.1 HFA/IHRSA – share of U.S. facility members using each modality

| Modality | 2016 (IHRSA 2018 report) [S8][S9] | 2021 [S4] | 2024 [S4] | Change |
|---|---|---|---|---|
| Treadmill | 44% | – | **43.4%** | ≈ flat |
| Resistance machines | 36% | 31.4% | **26.6%** | −15% (2021→24) |
| Free weights / dumbbells | 31% | – | **32.1%** | up; "fastest-growing equipment category since 2021" [S6] |
| Elliptical | – | 23.2% | **18.8%** | −19% (2021→24) |
| Yoga | 36% | – | 21.8% (from 20.2%) | (definitions differ) |
| Pilates | – | – | 8.1% | |
| Stretching | 24% | – | – | |
| Calisthenics | 23% | – | – | |
| Class-based group exercise & training | 47.5% | – | – | |
| Small-group training | – | – | 32.3% | |
| Personal trainer | – | – | 22.6% | |
| Pickleball | – | 3.3% | 8.1% | |

Verbatim evidence:
* [S4] (HFA, 30 Oct 2025): "In 2024, 43.4% of members used treadmills" … "32.1% trained with dumbbells or free weights" … resistance machines and ellipticals "down from 31.4% and 23.2% in 2021 to 26.6% and 18.8%, respectively." … "Yoga participation increased from 20.2% to 21.8% year-over-year, while Pilates climbed to 8.1%." … "Nearly one in four members (22.6%) worked with a personal trainer in 2024" … "Treadmills and free weights remain the backbone of the gym experience".
* [S8] (IHRSA 2018 report, 2016 data): "Treadmills remain the most-used piece of club equipment (44 percent report using a treadmill)." "Resistance machines (36 percent) and free weights/dumbbells (31 percent) rank second and third." "Nearly half of health club members (47.5 percent) participate in class-based group exercise and training."
* [S9] (IHRSA 2017 report, 2016 data): "yoga topped the list, with 36% of members reporting participation." "Stretching (24%) and calisthenics (23%) ranked second and third."
* [S11][S12][S13]: Top-3 equipment in 2021 and 2022 = treadmills, resistance machines and free weights (2021 data listed "treadmills, resistance machines and free weights"; 2022 data listed "treadmills, free weights (dumbbells/hand weights), and resistance machines" – the releases do not say whether the listing order is a strict rank).
* [S6] (HFA, 9 Apr 2026, 2025 data): free-weight usage "has grown faster than any other equipment category since 2021"; "Yoga remained the most widely practiced activity at 17.7 million members".

### 2.2 SFIA – U.S. participation, frequency and total occasions (population 6+, includes home use) [S1]

From *SFIA Topline Participation Report 2024* (2023 data), pages 27–28 ("Fitness Deep Dive") and 32–33 (detailed tables):

| Activity | Participants 2019 (M) | Participants 2023 (M) | Δ 2019→23 | CORE (50+/yr) 2023 (k) | Mean days/yr 2023 | Total occasions 2023 (B) | Δ occasions 2019→23 |
|---|---|---|---|---|---|---|---|
| Treadmill | 56.8 | **54.8** | −3.5% | 26,837 | 65 | **3.565** | −2.5% |
| Stationary cycling (recumbent/upright) | 37.1 | 32.6 | −12.0% | 16,728 | 68 | 2.228 | −2.5% |
| Elliptical motion / cross-trainer | 33.1 | 27.1 | −18.1% | 13,164 | 62 | 1.672 | −16.7% |
| Rowing machine | 12.8 | 12.8 | −0.3% | 4,302 | 42 | 0.539 | +1.1% |
| Stair-climbing machine | 15.4 | 12.6 | −17.9% | 4,530 | 42 | 0.530 | −21.5% |
| Stationary cycling (group) | 9.9 | 6.2 | −37.3% | 2,444 | 34 | 0.211 | −41.4% |
| Free weights (dumbbells/hand weights) | 51.4 | **53.9** | +4.7% | 30,619 | 80 | **4.309** | +9.6% |
| Free weights (barbells) | 28.4 | 29.3 | +3.4% | 15,159 | 77 | 2.255 | +4.1% |
| Weight/resistance machines | 36.2 | 29.4 | −18.7% | 18,065 | 77 | 2.256 | −18.1% |
| Kettlebells | 12.9 | 14.5 | +12.5% | 5,949 | 64 | 0.928 | +15.9% |
| Bodyweight exercise & accessory-assisted | 23.5 | 22.6 | −3.9% | 12,092 | 86 | 1.937 | −2.4% |
| High-impact/intensity training (HIIT) | 22.0 | 21.8 | −1.1% | 9,242 | 61 | 1.326 | +3.4% |
| Cross-training style workouts | 13.5 | 9.4 | −30.6% | 5,013 | 53 | 0.499 | −29.3% |
| Yoga | 30.5 | 34.2 | +12.5% | 13,595 | 57 | 1.950 | +21.8% |
| Pilates | 9.2 | 11.9 | +28.3% | 3,057 | 38 | 0.450 | +29.7% |

SFIA executive summary [S1, p.8]: "many health club-based activities, such as Treadmill, Stair-Climbing, Rowing Machine, and most class-based fitness activities, such as Barre, Pilates, and Yoga, saw good gains in participation in 2023."
SFIA 2026 single-sport reports (2025 data; page not reachable, content seen only in search snippets) [S2, fetched=false]: participation in "treadmill and stair-climbing machine activities increased significantly in 2025"; free-weight categories "continue to demonstrate healthy participation growth"; kettlebells "one of the fastest-growing segments within strength fitness".
Earlier (2022 data) [S3]: treadmill 53.6M, dumbbells 53.1M; kettlebells +6.5%, barbells +1.1%, stair-climbing −24%, group cycling −36.9% (2019→2022).

**DERIVED shares from SFIA occasions (2023):**
* Cardio-machine occasions (8.745 B): treadmill **40.8%**, stationary upright/recumbent **25.5%**, elliptical **19.1%**, rower **6.2%**, stair climber **6.1%**, group cycling **2.4%** (2019: 38.4 / 24.0 / 21.1 / 5.6 / 7.1 / 3.8).
* Strength occasions (9.748 B): dumbbells **44.2%**, barbells **23.1%**, machines **23.1%**, kettlebells **9.5%** (2019: 40.7 / 22.4 / 28.5 / 8.3).
* Free weights (DB+BB) vs machines: **74.4 : 25.6** (2023) vs 68.9 : 31.1 (2019). Barbell = 34.4% of DB+BB occasions.
* Strength : cardio occasion ratio: 1.014 (2019) → **1.115** (2023) ⇒ shift factor **×1.099 in 4 years (+2.4%/yr)**.
* Caveat: SFIA counts activity-days (one person doing dumbbells and machines on the same day counts twice) and includes home equipment (inflates dumbbells/treadmills relative to gyms).

### 2.3 Other surveys on modality participation

* **ABC Fitness Wellness Watch Q1 2025** (consumer survey + platform data; platform covers 40M members, 30,000+ gyms/studios) [S45]. "Users primary activity at gym" (active consumers): working out on own (cardio, weights, functional) **69%**; group exercise classes **39%**; PT/special instructor **28%**; recreational/sport **27%**; small-group (≤8) **22%**; streaming **9%**. 42% "Workout at a traditional gym or health club"; 106M check-ins in January 2025.
* **ABC exercise-regimen priority scores** [S45, pp.16–19]: Gen Z top = free weight training 5.54, cardio equipment 5.52, equipment-based exercise 5.50, flexibility/stretching 5.36; Millennials = cardio equipment 5.6, equipment-based 5.6, free weights 5.58; Gen X = cardio equipment 5.54, free weights 5.44; **Baby Boomers = flexibility/stretching 5.24, cardio equipment 5.14, senior fitness 4.66, free weights 4.64**.
* **Les Mills** [S32][S33]: 2026 Global Fitness Report (10,442 online surveys, 14 countries): "Over half of regular exercisers include some form of strength training in their routines"; group strength participation "grown from 30% in 2018 to 36%". Gen Z report (4,000+ aged 16–26) [S34][S35]: "81% of Gen Z gym-goers are taking part in group workouts"; of those, "50% are doing strength training", "35% are doing stretch / mobility", "33% are doing Yoga"; 81% of Gen Z exercisers use free weights at their facility [S35].
* **PureGym UK Fitness Report 2025/26** (YouGov/Censuswide, all exercisers) [S18]: strength training (weightlifting) 51%, strength (bodyweight/bands) 51%, core 49%, gym classes 41%, cross trainer 34%, circuit 32%; 29% of gym members attended a class in the last year; 61% of exercisers do two strength-focused sessions a week. 2024/25 report [S19]: 32% of members attend group classes; 89% of 18–24-year-olds do some strengthening exercise each week.
* **IHRSA via Precor (2014)** [S58]: "female gym goers favour group exercise, with only 47 per cent making use of weights."

### 2.4 What happens inside strength sessions (exercise-level, workout-app logs)

**StrengthLog** (700k+ users, "millions of workouts"; % of all logged sets) [S46][S47] – top 25 (all users):
Bench press 9.7, squat 7.0, deadlift 5.0, lat pulldown 3.8, overhead press 3.4, barbell row 3.2, DB lateral raise 2.7, leg extension 2.5, leg press 2.2, barbell curl 2.1, triceps pushdown (bar) 2.0, incline DB press 1.9, DB curl 1.7, pull-up 1.7, cable close-grip seated row 1.6, triceps pushdown (rope) 1.5, lying leg curl 1.3, DB row 1.3, DB shoulder press 1.3, Romanian deadlift 1.3, seated leg curl 1.2, hammer curl 1.1, standing cable chest fly 1.1, DB chest press 1.0, face pull 1.0 (total 62.6% of sets).
Women's list adds hip thrust 2.0%, Bulgarian split squat 1.4%, stiff-legged deadlift 1.1%, hip abduction machine 1.0%; leg press 2.7% (vs 1.9% men). "The average workout frequency is 3.3 workouts per week." Women do 42% more leg pressing; hip thrusts "830% more" by women; men 30% more bench press [S47].

**DERIVED equipment split of StrengthLog top-25 sets:** barbell **50.6%**, dumbbell **17.6%**, selectorized/plate machines **11.5%**, cable-stack machines (lat pulldown, seated cable row) **8.6%**, cable stations (pushdowns, fly, face pull) **8.9%**, bodyweight **2.7%**.
Within barbell: bench 30.6%, squat 22.1%, deadlift 15.8%, RDL 4.1%, OHP 10.7%, row 10.1%, curl 6.6% ⇒ rack-dependent (squat+OHP) 32.8%, bench station 30.6%, platform/floor (DL, RDL, row) 30.0%, fixed bar (curl) 6.6%.
Within dumbbell: 50% of DB sets are bench-supported (incline/flat/seated press, supported row).
Within machines: lat pulldown 30.2%, leg extension 19.8%, leg curl (lying+seated) 19.8%, leg press 17.5%, seated row 12.7%.
Within cable stations: pushdowns 62.5%, chest fly 19.6%, face pull 17.9%.

**Boostcamp "State of Lifting 2025"** (1,000,000 workout logs, 16.7M sets) [S48]: median workout **58 min** (P75 79, P90 ≈109, mean 87 – skewed by un-ended sessions); median **6** unique exercises per workout; median **2.7** training days/week (16% ≥4); logs containing: bench press 172K, DB lateral raise 153K, squat 150K, leg extension 147K, lat pulldown 140K, deadlift 99K, cable lateral raise 85K.

**Fitbod** [S49][S50]: 15.8M workouts logged in 2022; by load lifted, leg press > barbell bench > lat pulldown; DB biceps curl the most frequent (1.8M workouts); "Treadmill Walking" second most manually-added exercise (396,000; often a warm-up). 2026 analysis: barbell back squat ranks ~30th and deadlift ~38th by number of lifters; more users log the DB bench press than the barbell bench; dumbbells, cables and machines dominate.
**JEFIT** (10M+ members, 2023) [S51]: most-selected = barbell bench press, barbell biceps curl, wide-grip (cable) lat pulldown.

Interpretation: barbell-centric apps (StrengthLog/Boostcamp) over-represent rack/bench work; general-population apps (Fitbod) show dumbbells/machines/cables dominate. The average-member recommendation in §0 sits between them.

### 2.5 Gender and age

| Evidence | Value | Source |
|---|---|---|
| Share of U.S. people (15+) who exercised on an average day, 2009–15 | 18.1% | [S22] |
| Of exercisers on an average day: weight lifting / cardio equipment | 9.1% / 9.1% (2003–08: 12.5% / 12.7%) | [S22] |
| Hours per day on days participated: cardio equipment / weight lifting / aerobics / yoga | 0.7 / 0.9 / 0.8–0.9 / 0.9–1.0 | [S22] |
| Sex split of participants: cardio equipment | 44.7% men / **55.3% women** | [S22] |
| Sex split: weight lifting | **72.2% men** / 27.8% women | [S22] |
| Sex split: yoga / aerobics | 15.7/84.3; 15.5/84.5 (men/women) | [S22] |
| Age split (15–24 / 25–54 / 55+): weight lifting | 33.5 / 47.7 / 18.8% | [S22] |
| Age split: cardio equipment | 14.3 / 48.9 / 36.8% | [S22] |
| Median age: weight lifters / cardio-equipment users | 32.5 / 46.7 yrs | [S22] |
| GYMetrix sensors (UK): free-weight users who are female at any given time | **7%** ("cardio machines is evenly distributed between the sexes") | [S57] (2016) |
| GYMetrix: gym floor at peak | "2:1 male to female" | [S55] (2015) |
| GYMetrix 2011–18: resistance named favourite equipment, females <35 | +121% | [S54] |
| Strava 2025 | "Women … were 21% more likely than men to record Weight Training"; "Gen Z is 2x more likely than Gen X to say weight training is their primary sport" | [S36] |
| NHIS 2020: adults meeting muscle-strengthening guideline | 31.0% (both aerobic+MS 24.2%; men 28.3% vs women 20.4%; 18–34: men 41.3%/women 28.7% … 65+: 15.3%/10.8%) | [S24] |
| Planet Fitness membership | ≈51% male; "Nearly 50/50"; 46% under 35; 20% over 55 | [S28][S29] |
| UK gym membership (YouGov) | men 21% vs women 17% (2025/26); 18% vs 15% (2024/25) | [S18][S19] |
| HFA 2024 | "studios are increasingly female-driven, while multipurpose, corporate, and nonprofit facilities skew male" | [S4] |
| HFA 2022 | average member age 39 → 37; "higher visit rates among older members" | [S12] |
| HFA 2025 | Gen Z (18–24) penetration 35.5%; members 65+ +8.6% YoY | [S6] |
| Penn State survey (n=319) | women: less weight use, more cardio & group exercise, lower comfort in weights areas | [S53] |
| Les Mills 2026 | barriers to starting strength: feeling out of place in weights area 50%, lack of equipment 33%, fear of injury 23% | [S32] |

**DERIVED demographic propensities (ATUS 2009–15, strength share of strength+cardio minutes = participation share × hours):**
* All: (9.1×0.9)/(9.1×0.9+9.1×0.7) = **56.3%**.
* Men: (0.722×9.1×0.9)/(…+0.447×9.1×0.7) = **67.5%**; women: **39.3%**.
* Age 15–24: **75.1%**; 25–54: **55.6%**; 55+: **39.6%**.
* Applying the SFIA 2019→2023 shift factor (×1.099 on the S/C odds): all 58.6%, men 69.5%, women 41.5%, 15–24 76.8%, 25–54 58.0%, 55+ 41.9%. Recommended (2025–26) values in §0.3 add ~+2 pts for continued drift and ~+3–4 pts extra for women (Strava/GYMetrix evidence of faster female growth).

---

## 3. (b) Time allocation within a visit and session length

### 3.1 Session length evidence

| Measure | Value | Source |
|---|---|---|
| PureGym member data (UK), average visit | **68 min** (2025/26) | [S18] "Based on our own member data, the average visit time nationwide sits at 68 minutes." |
| PureGym, average visit (2022–2024 reports) | **69 min** ("1 hour and 9 minutes"; consistent across 2022, 2023, 2024) | [S19] |
| PureGym 2022 report | 66 min (search snippet only; PDF 404) | [S20] fetched=false |
| Placer.ai, value/HVLP gyms (U.S.) | 72.4 min (Q1 2022) → **74.0 min** (Q1 2025); visit length rose in all tiers; Life Time longest | [S17] |
| Boostcamp logged workouts | median **58 min**, P75 79, P90 ≈109, mean 87 | [S48] |
| Strava 2025 strength sessions | "just over 50 minutes" | [S37] |
| ATUS (2009–15) on days participated | cardio equipment 0.7 h (42 min); weight lifting 0.9 h (54 min) | [S22] |
| ATUS 2025, all sports/exercise/recreation | 1.47 h/day for those who engaged (men 1.66, women 1.25); 23.4% engage per day | [S23] |
| UK exercisers' self-reported workout length | 15–29 min 20%; 30–59 min 41%; 1–1.5 h 19%; ≥1 h 32% | [S18] |
| Orangetheory class | "a 1 hour, full body workout" (treadmill/rower/floor blocks) | [S61] |

**Recommendation:** in-building 70 min (gate data, includes changing); active floor time 55 min (app logs: 50–58 min). For the queueing model use 55 min of equipment demand per visit.

### 3.2 Evidence on minutes by modality

* ATUS 2009–15: equal shares of exercisers did weight lifting and cardio-equipment on an average day (9.1% each), but lifting days are longer (0.9 vs 0.7 h) ⇒ strength ≈56% of strength+cardio minutes [S22] (DERIVED).
* GYMetrix equipment-utilisation studies, "hundreds of facilities between 2011 and 2018": member time on cardio **−33%**, on resistance **+32%** [S54].
* YMCA of Pierce & Kitsap Counties (Track My Gym sensors on all equipment, hour-by-hour, plus ~1,000-member survey): "More members are using strength equipment versus cardio equipment"; "platforms with racks and cable stacks have very high usage"; strength equipment "is too busy and creates wait times, especially during peak hours" [S56].
* GYMetrix (≈400 UK gyms tracked, 2015): biggest over-supply = "1 Crosstrainers 2 Treadmills 3 Upright cycles"; "there's usually a lack of 8-18kg dumbbells. These are the most popular pieces of kit in the gyms" [S55].
* Parkwood Health & Fitness (UK) case (secondary, page not readable): peak availability free weights 35%, resistance 50%; cardio need "around 30% of the gym floor (down from over 50% just 10 years ago)" [S63, fetched=false].
* Planet Fitness moved to "about a 50-50 mix of cardio and strength" (equipment mix, Q2 2025 call; the transcript marks the words just before "about" as indiscernible) with more stair climbers and fewer arc trainers/ellipticals [S30].
* No 2019–2026 source directly measures minutes-per-modality inside a typical visit (see Gaps).

### 3.3 DERIVATION – average-member time shares (§0.1)

1. Strength:cardio two-way split. ATUS 2009–15 baseline 56.3% strength. SFIA activity-day ratio moved ×1.099 between 2019 and 2023 ⇒ 58.6%. Garmin (+25% 2024, +29% 2025 strength) and HFA (free weights fastest-growing since 2021) push further, while SFIA 2025 reports a treadmill/stair "cardio comeback" ⇒ adopt **≈60% strength / 40% cardio** of strength+cardio minutes.
2. Non-S/C carve-outs. Functional/turf/kettlebell ≈7% (SFIA kettlebell + cross-training + ~⅓ of bodyweight occasions ≈ 2.07 B vs 17.6 B cardio+strength ≈ 10.5% of population activity; reduced because much bodyweight/HIIT is home- or class-based). Stretch/mobility ≈6% (IHRSA: 24% of members stretch; a 5-min warm-up/cool-down in a 55-min session ≈ 9%, but many do it in-place).
3. Remaining 87% split 60/40 ⇒ strength 52%, cardio 35%.
4. Within strength (52%): free weights 56% (HFA participation 32.1 vs 26.6 ⇒ 55% FW; SFIA occasions 74% FW incl. home use; GYMetrix: dumbbells most popular), machines 33%, cables 11% (StrengthLog cable stations 8.9% of top-25 sets; Fitbod "cables … dominate") ⇒ FW 29, machines 17, cables 6. Free weights split barbell 40% / dumbbell 60% (SFIA barbell = 34% of DB+BB occasions; StrengthLog barbell-heavy; Fitbod DB-heavy) ⇒ barbell 11.5, dumbbell 17.5.

### 3.4 DERIVATION – archetype vectors

* **Strength-focused** (young, male-skewed; e.g., hardcore/performance gyms, college-age): ATUS-adjusted strength share for age 15–24 = 76.8% and men = 69.5% ⇒ target ≈77%. Rack/platform share raised toward app-lifter evidence (StrengthLog barbell 50.6% of top-25 sets ⇒ barbell ≈32% of strength minutes); stair climbers over-weighted in cardio (PF: stair climbers "getting a high level of utilization" [S30]; Garmin stair climbing +25% 2024 [S41]).
* **Cardio/wellness-focused** (HVLP legacy, community/YMCA/medical, older or female-skewed): ATUS-adjusted strength share for 55+ = 41.9%, women = 41.5% ⇒ target ≈45–47%; Boomers rank flexibility and cardio above free weights [S45]; novices prefer machines; Planet Fitness was cardio-heavy until it rebalanced toward ~50/50 equipment in 2024–25 [S29][S30][S31].
* **Functional-focused** (CrossFit/Hyrox/F45/OTF-style): HYROX = 8 × 1 km runs + SkiErg 1000 m, sled push 50 m, sled pull 50 m, burpee broad jump 80 m, row 1000 m, farmers carry 200 m, sandbag lunges 100 m, 100 wall balls [S60]; Orangetheory = 1-hour treadmill/rower/floor format [S61]. Hence functional/turf/rig ≈40%, barbell 22%, ergs/curved treadmills ≈22%, minimal machines/cables. **Low confidence – no direct usage measurement.**

### 3.5 Bout / holding-time evidence

* Boostcamp: 58 min ÷ 6 exercises ⇒ **≈9.7 min per strength exercise** (incl. transitions) [S48] (DERIVED).
* U. Calgary sensor study (Anytime Fitness, Calgary, 31 May–12 Jun 2022; 32 equipment sensors; 30,000+ data points): pec-fly sensors "reported 3 motion events over a period of 4 minutes, consistent with a typical machine workout of three sets of 10 repetitions which take about 30 seconds followed by 30 seconds of rest"; StairMaster sessions "typically long in duration (perhaps 10 minutes)"; "On cardio equipment like the Elliptical, the events are 10, 20, even 30 minutes or higher"; busy periods "between 10AM and 1PM, and again between 5PM and 9PM" [S52].
* ACSM progression models (2009): novice 8–12 RM, "2-3 d x wk(-1) for novice training", "3-4 d … intermediate", "4-5 d … advanced"; 3–5-min rest periods for intermediate/advanced heavy work [S25] – supports longer rack holding times (10–15 min) than machine stations (4–9 min).
* ATUS: 42 min/day of cardio equipment on days used [S22] ⇒ upper anchor for a cardio bout (many such days are cardio-only).
* Planet Fitness 10-K: floor-space allocation is "why we have not needed to impose time limits on our cardio machines" [S28].

---

## 4. (c) Visit frequency and low/non-use

| Measure | Value | Per week | Source |
|---|---|---|---|
| IHRSA (mid-2010s) visits per member | "hovered consistently between 101 and 103 visits annually"; "roughly two visits a week" | ≈1.95 | [S10] |
| IHRSA 2016 data: 5.7 B visits / 57.3 M members | 99.5/yr (DERIVED) | 1.91 | [S8] |
| Members using club ≥100 times in 2016 | 43.6% (≈25 M) | – | [S8] |
| 2021: 4.5 B visits / 66.5 M members | 67.7/yr (DERIVED, pandemic) | 1.30 | [S11][S13] |
| HFA 2022 average attendance | 75 days (from 72 in 2021) | 1.44 | [S12] |
| HFA 2025: ~7 B visits / 81 M members (>100 M users) | ≤86.4/yr per member (DERIVED upper bound; 70/yr per user) | ≤1.66 | [S6][S7] |
| HFA FIT Tracker 2025 | >184,000 visits per location (+4.2%); avg monthly visits per visitor +1.1% | ≈504 visits/location/day (DERIVED) | [S14] |
| Placer.ai 2025: Planet Fitness / Life Time visits per visitor per month | 4.1–4.4 / 5.7–6.2 | 0.94–1.01 / 1.31–1.43 | [S15] |
| Planet Fitness internal, *active* members (used club in month) | ~6.1/month → "mid- to high 6s" (2025) | 1.40 → 1.5–1.6 | [S30] |
| Planet Fitness visitor frequency, Q3 2024 | 44.3% <2/month; 16.8% ≥8/month (12.9% 2019); 11.9% ≥10/month (8.6% 2019) | – | [S16] |
| DellaVigna & Malmendier (3 U.S. clubs, 7,752 members, 3 yrs) | 4.3/month (actual 4.17 vs predicted 9.50) | ≈0.97 | [S21] |
| ABC Fitness 2025 (active consumers, any setting) | 44% work out 12+ times/month; Boomers 58% vs Gen Z 37% | – | [S45] |
| UK exercisers (YouGov) | 2–3×/wk 40%; 4–6× 24%; once 17%; daily 8% | – | [S18] |
| App lifters | StrengthLog mean 3.3/wk; Boostcamp median 2.7/wk | 2.7–3.3 | [S47][S48] |
| Never use membership | 4.6% (from ~10%) | – | [S6] |

DellaVigna & Malmendier also: "Eighty percent of the monthly members would have been better off had they paid per visit"; average 2.31 months between last attendance and cancellation [S21].

**Recommendation:** 1.5 visits/member/week overall; distribution heavily skewed (≈45% of visitors <0.5/wk at HVLP clubs vs 12–17% at ≥2/wk).

---

## 5. (d) Cardio equipment-level shares

| Equipment | SFIA participants 2023 (M) | SFIA occasions share 2023 | HFA member share 2024 | Trend evidence | Recommended share of cardio minutes (avg) |
|---|---|---|---|---|---|
| treadmill | 54.8 | 40.8% | 43.4% | flat; SFIA 2025 "increased significantly" | **40%** |
| upright + recumbent bike | 32.6 | 25.5% | n/a | −12% participants 2019→23 | 11% + 8% |
| elliptical | 27.1 | 19.1% | 18.8% | −18% (SFIA), −19% (HFA 2021→24); PF removing ellipticals/arc trainers | **15%** |
| rower | 12.8 | 6.2% | n/a | stable (+1%) | 7% |
| stair_climber | 12.6 | 6.1% | n/a | Garmin +25% (2024); SFIA 2025 "increased significantly"; PF "significantly increased the complement of stair climbers" | **10%** |
| indoor_cycle (group) | 6.2 | 2.4% | n/a | −41% occasions 2019→23 | 3% (free use) |
| air_bike / ski_erg / curved_treadmill / recumbent_stepper | no survey category | – | – | functional-fitness formats (HYROX, CrossFit) | 2% / 1% / 1% / 2% (ESTIMATE) |

Treadmill is the most-used machine by every measure: ≈2.1× elliptical occasions (SFIA), 2.3× elliptical member share (HFA), ≈1.6× all upright/recumbent bikes, ≈6.7× stair climbers (2023, before the stair surge).

---

## 6. (e) The strength shift, 2019–2026

| Year | Signal | Source |
|---|---|---|
| 2011–18 | GYMetrix sensors: member time on cardio −33%, resistance +32% | [S54] |
| 1998→2018 | share of Americans regularly strength training +10 pts but "remains below 30%" (PF investor deck) | [S29] |
| 2019→23 | SFIA: dumbbells +4.7%, barbells +3.4%, kettlebells +12.5%; machines −18.7%, elliptical −18.1%, stair −17.9%, group cycling −37.3% | [S1] |
| 2021→24 | HFA members: machines 31.4→26.6%, elliptical 23.2→18.8%; free weights fastest-growing category since 2021 | [S4][S6] |
| 2022→25 | Garmin: strength training up >20% four years running (2023: fitness-equipment activities +19%, HIIT +112%; 2024: strength +25%, stair +25%; 2025: strength +29%) | [S39][S41][S42] |
| 2023 | ACSM: strength training with free weights #2 worldwide trend (cited by Planet Fitness) | [S29] |
| 2024 | Planet Fitness: >60% of franchisees opted to add strength equipment; option to remove 30-minute circuit for functional space | [S29] |
| 2025 | PF: 65% of estate added plate-loaded; "about a 50-50 mix of cardio and strength"; >70% (mid-year) and "nearly 80%" (year-end) of system format-optimized | [S30][S31] |
| 2025 | Strava: weight training ≥500 M uploads; women 21% more likely than men to log it; Gen Z 2× Gen X as primary sport | [S36][S38] |
| 2025 | ClassPass: Strength Training #3 (+27% YoY), Gym Time +51%, Pilates #1 (+66%) | [S43] |
| 2025 | SFIA: "cardio comeback" – treadmill and stair-climbing up significantly | [S2] (fetched=false) |
| 2026 | ACSM: Traditional Strength Training #7; 2027 list (published 20 Oct 2026): #5 | [S26][S27] |
| 2026 | Les Mills: >50% of regular exercisers strength train; group strength 30% (2018) → 36% | [S32] |
| 2026 | Anytime Fitness (UK): "reducing the size of our cardio areas, removing some of our selectorised kit"; 6–8 lifting platforms per club | [S59] |

Model implication: strength share keeps drifting up (~+2%/yr in the S/C ratio), with free weights (especially dumbbells, racks/platforms, plate-loaded) gaining at the expense of selectorized machines and ellipticals; stair climbers and treadmills are the cardio winners.

---

## 7. Observational / sensor studies found

1. **GYMetrix** (UK consultancy; wireless sensors on equipment; ~400 UK gyms by 2015; "hundreds of facilities" 2011–18): cardio over-supply (cross-trainers, treadmills, upright cycles); 8–18 kg dumbbells most popular; 2:1 male:female at peak; 7% of free-weight users female; cardio time −33%, resistance +32% (2011–18) [S54][S55][S57].
2. **YMCA of Pierce & Kitsap Counties / Track My Gym** (all equipment tagged, hour-by-hour, several weeks, ~1,000-member survey): strength use > cardio use; racks/platforms and cable stacks very high usage; strength wait times at peak [S56].
3. **Long (2023), U. Calgary MSc thesis** (sensor network, Anytime Fitness Calgary, 2 weeks, 32 sensors): machine set timing, cardio bout lengths, daily peaks [S52].
4. **BLS ATUS** time diaries (national, 2003–2015 detail) [S22].
5. **Placer.ai / HFA FIT Tracker** passive location panel (≈11,000 facilities) [S14]–[S17].
6. **GymCam** (Khurana et al., Proc. ACM IMWUT 2(4), 2018; single camera in a varsity gym over five days) – a recognition method paper; no modality-share statistics usable here (not fetched).

---

## 8. Conflicts and reconciliation

* **Session length:** PureGym 66 vs 68 vs 69 min (gate data); Placer 74 min (location pings, HVLP); Boostcamp median 58/mean 87 (app timer); Strava ~50 min (strength only). → Building time 70 min; floor time 55 min.
* **Visit frequency:** ~100/yr (IHRSA 2015–16) vs 75 days (HFA 2022) vs ≤86 (HFA 2025). Placer (4.1–4.4/visitor-month at PF) vs PF internal active-member (6.1→6.5–6.9/month): different denominators (all device visitors vs. members who checked in that month) and method. → 1.5/wk average; segment-specific values in §0.3.
* **Free weights vs machines:** HFA participation 55:45; SFIA occasions 74:26 (home dumbbells inflate); StrengthLog barbell-dominated; Fitbod dumbbell/machine/cable-dominated. → 56% free weights / 33% machines / 11% cables of strength minutes for the average member.
* **Gender:** ATUS 2009–15 (72% of lifters male) and GYMetrix 2016 (7% of free-weight users female) vs Strava 2025 (women 21% more likely to log weight training) and StrengthLog (women's top exercises are barbell squat/bench/deadlift). The older observational data predate the 2019–26 female lifting boom → women's strength share raised to ~45% of S+C minutes (from 39% in 2009–15).
* **2025 cardio:** SFIA "return of cardio" (treadmill, stair) vs Garmin/HFA/ClassPass strength growth → both can be true (stair climbers/treadmills grow while ellipticals, bikes and selectorized machines shrink); keep treadmill share flat, raise stair climber, cut elliptical.

---

## 9. Recommended values for the engine (ids)

| id | value | notes |
|---|---|---|
| `usage.avg.time_share.cardio` | 0.35 | §3.3 |
| `usage.avg.time_share.barbell` | 0.115 | rack/platform/bench stations |
| `usage.avg.time_share.dumbbell` | 0.175 | 50% of DB time needs a bench |
| `usage.avg.time_share.machines` | 0.17 | selectorized + plate-loaded |
| `usage.avg.time_share.cables` | 0.06 | |
| `usage.avg.time_share.functional` | 0.07 | turf/rig/KB/sled |
| `usage.avg.time_share.stretch` | 0.06 | |
| `usage.strength_focused.*` | 0.20/0.22/0.20/0.18/0.08/0.06/0.06 | same order as above |
| `usage.cardio_wellness.*` | 0.47/0.04/0.12/0.22/0.04/0.03/0.08 | |
| `usage.functional_focused.*` | 0.22/0.22/0.08/0.02/0.01/0.40/0.05 | low confidence |
| `usage.cardio_mix.avg` | TM .40, curved .01, ell .15, upright .11, recumbent .08, spin .03, air .02, row .07, stair .10, ski .01, stepper .02 | §5 |
| `usage.barbell_mix` | rack (squat+OHP) .33, bench station .31, platform/floor (DL/RDL/row) .30, fixed bar .06 | StrengthLog-derived |
| `usage.machine_mix` | lat pulldown .30, leg ext .20, leg curl .20, leg press .175, seated row .125 (top-5 only) | StrengthLog-derived; add hip abd/add, glute, chest/shoulder press from equipment slice |
| `usage.cable_mix` | pushdowns .625, fly .196, face pull .179 | StrengthLog-derived |
| `usage.visits_per_week.avg` | 1.5 | |
| `usage.session.floor_minutes` | 55 | |
| `usage.session.building_minutes` | 70 | |
| `usage.holding.strength_station_min` | 9 | 4–15 |
| `usage.holding.cardio_bout_min` | 25 | 10–45 |
| `usage.never_use_share` | 0.046 | |
| `usage.strength_drift_per_year` | 0.02 | on S/C odds |

---

## 10. Gaps

1. No 2019–2026 source directly measures **minutes per modality within a typical visit** for average members; the split is derived (ATUS 2009–15 × SFIA shift × app/sensor evidence).
2. Member-level usage shares for **cables, functional/turf, stair climbers, rowers, bikes, barbells** are not in HFA's public releases (only treadmill, free weights, machines, elliptical, yoga, Pilates).
3. **SFIA 2025/2026 activity-level counts** inaccessible (sfia.org DNS failure; paywalled single-sport reports) – newest table used is 2023 data.
4. No usage data distinguish **upright vs recumbent bikes**, or cover **curved treadmills, air bikes, ski ergs, recumbent steppers** (allocations are estimates).
5. Gender/age modality splits for **gym members specifically** are dated (ATUS 2009–15; GYMetrix 2015–16) or app-based.
6. **ACSM rankings 2019–2025** not verified (journal paywall); only 2023 (#2, via PF deck), 2026 (#7), 2027 (#5).
7. Functional-focused archetype vector is the weakest (format-based reasoning, no measured shares).
8. Peak-hour distributions and occupancy belong to another slice; only incidental evidence recorded here.
9. Gym Group (UK) CEO statement on strength-over-cardio (Express & Star) and PureGym 2022 PDF (66 min) could not be fetched.

---

## 11. Sources

| id | Title / publisher (year) | URL | fetched |
|---|---|---|---|
| S1 | SFIA Topline Participation Report 2024 (2023 data), Sports & Fitness Industry Association (copy hosted by USTA) | https://www.usta.com/es/content/dam/usta/sections/intermountain/districts/colorado/pdfs/sfia-reports/2024-sfia-topline.pdf | yes (pp.4,7–8,27–35) |
| S2 | SFIA: 2026 fitness participation trends – strength, yoga, Pilates and the return of cardio | https://sfia.org/resources/2026-fitness-participation-trends-what-sfias-latest-research-reveals-about-strength-training-yoga-pilates-and-the-return-of-cardio/ | no (DNS failure; search snippet only) |
| S3 | The Barbell: Survey reveals fitness trends (SFIA 2023 Topline) | https://thebarbell.com/survey-reveals-fitness-trends/ | yes |
| S4 | HFA: How 77 Million Fitness Members Work Out (30 Oct 2025) | https://www.healthandfitness.org/how-77-million-fitness-members-work-out-new-hfa-data-reveals-shifting-equipment-training-and-membership-trends/ | yes |
| S5 | HFA press release: New HFA Data Shows How 77 Million US Fitness Facility Members Work Out | https://www.healthandfitness.org/new-hfa-data-shows-how-77-million-us-fitness-facility-members-work-out | yes |
| S6 | HFA: 81 Million Americans Were Members of a Fitness Facility in 2025 (9 Apr 2026) | https://www.healthandfitness.org/81-million-americans-were-members-of-a-fitness-facility-in-2025-new-hfa-report-finds/ | yes |
| S7 | Recreation Management: More Than 100 Million Visit Fitness Facilities in 2025 | https://recmanagement.com/articles/155773/more-100-million-visit-fitness-facilities-2025 | yes |
| S8 | SGB: IHRSA report shows healthy fitness market (2018 report, 2016 data) | https://sgbonline.com/ihrsa-report-shows-healthy-fitness-market/ | yes |
| S9 | IDEA Fit: Most popular club activities (IHRSA 2017 report) | https://www.ideafit.com/most-popular-club-activities | yes |
| S10 | Health Club Management: key findings from 2016 IHRSA Health Club Consumer Report | https://www.healthclubmanagement.co.uk/health-club-management-features/IHRSA-update-A-look-at-the-key-findings-from-2016-IHRSA-Health-Club-Consumer-Report/31225 | yes |
| S11 | HFA: IHRSA Releases 2022 Health Club Consumer Report (17 Nov 2022) | https://www.healthandfitness.org/ihrsa-releases-2022-health-club-consumer-report/ | yes |
| S12 | HFA: IHRSA Releases 2023 U.S. Health & Fitness Consumer Report (20 Dec 2023) | https://www.healthandfitness.org/?p=1195 | yes |
| S13 | SGB: IHRSA 2022 Health Club Consumer Report coverage | https://sgbonline.com/?p=265275 | yes |
| S14 | HFA: US Fitness Industry Extends Record Visitation Streak Through 2025 (FIT Tracker) | https://www.healthandfitness.org/es/us-fitness-industry-extends-record-visitation-streak-through-2025/ | yes |
| S15 | Placer.ai: Life Time & Planet Fitness Q2 2025 recap | https://www.placer.ai/anchor/articles/life-time-planet-fitness-q2-2025-recap | yes |
| S16 | Placer.ai: Planet Fitness – Raising the Bar(bell) | https://www.placer.ai/anchor/articles/planet-fitness-raising-the-bar-bell | yes |
| S17 | Athletech News: 7 foot traffic insights (Placer.ai data) | https://athletechnews.com/7-foot-traffic-insights-that-belong-on-every-gym-operators-radar/ | yes |
| S18 | PureGym: UK Fitness Report 2025/26 | https://www.puregym.com/blog/uk-fitness-report-gym-statistics/ | yes |
| S19 | PureGym: UK Fitness Report 2024/25 | https://www.puregym.com/blog/uk-fitness-report-gym-statistics-2024-2025/ | yes |
| S20 | PureGym UK Gym Report 2022 (PDF) | https://edit.puregym.com/media/817923/puregym-uk-gym-report-2022.pdf | no (404) |
| S21 | DellaVigna & Malmendier, "Paying Not to Go to the Gym", AER 96(3) 2006 | https://eml.berkeley.edu/~ulrike/Papers/gym.pdf | yes |
| S22 | BLS Spotlight on Statistics: Sports and Exercise (2017; ATUS 2003–15) | https://www.bls.gov/spotlight/2017/sports-and-exercise/home.htm | yes |
| S23 | BLS ATUS Table A-1, 2025 annual averages | https://www.bls.gov/tus/tables/a1-2025.pdf | yes |
| S24 | NCHS Data Brief 443: Physical Activity Among Adults, US 2020 | https://www.cdc.gov/nchs/products/databriefs/db443.htm | yes |
| S25 | ACSM Position Stand: Progression models in resistance training (MSSE 2009) | https://pubmed.ncbi.nlm.nih.gov/19204579/ | yes |
| S26 | ACSM Fitness Trends page (2027 list) | https://www.acsm.org/education-resources/trending-topics-resources/acsm-fitness-trends | yes |
| S27 | Newswise: ACSM Announces Top Fitness Trends for 2027 | https://www.newswise.com/articles/acsm-announces-top-fitness-trends-for-2027 | yes |
| S28 | Planet Fitness Form 10-K FY2025 | https://www.sec.gov/Archives/edgar/data/1637207/000163720726000011/plnt-20251231.htm | yes |
| S29 | Planet Fitness Investor Presentation May 2025 (8-K Ex. 99.1) | https://www.sec.gov/Archives/edgar/data/1637207/000163720725000059/planetfitnessincinvestor.htm | yes |
| S30 | Planet Fitness Q2 2025 earnings call transcript | https://allmind.ai/earnings/event/bt_PLNT_2025_Q2 | yes |
| S31 | Planet Fitness Q4 2025 earnings call transcript | https://allmind.ai/earnings/event/bt_PLNT_2025_Q4 | yes |
| S32 | Les Mills: 2026 Global Fitness Report article | https://www.lesmills.com/ae/articles/2026-global-fitness-report-strength-and-wellness-to-drive-next-wave-of-member-growth | yes |
| S33 | ICAA: Strength & wellness drive fitness club growth (Les Mills GFR 2026) | https://www.icaa.cc/industrynews/2026-02/GET-STRONGER-Strength-wellness-drive-fitness-club-growth.htm | yes |
| S34 | Les Mills: Landmark report lifts the lid on Gen Z fitness | https://www.lesmills.com/us/clubs-and-facilities/research-insights/fitness-trends/landmark-report-lifts-the-lid-on-gen-z-fitness/ | yes |
| S35 | Les Mills APAC: Fitness in focus – 6 things we learned in 2023 | https://www.lesmills.com.au/news/clubs/2023/12/fitness-in-focus-6-things-we-learned-in-2023 | yes |
| S36 | Strava: 12th Annual Year in Sport Trend Report (2 Dec 2025) | https://press.strava.com/articles/strava-releases-12th-annual-year-in-sport-trend-report-2025 | yes |
| S37 | Athletech News: Strava Year in Sport 2025 | https://athletechnews.com/running-walking-strength-training-strava-year-in-sport-report/ | yes |
| S38 | Strava: Overhauls Strength Experience (21 May 2026) | https://press.strava.com/articles/strava-overhauls-strength-experience-with-expanded-partner-ecosystem-new-workout-log-and-muscle-maps | yes |
| S39 | Garmin: A look back at 2023 (fitness report) | https://www.garmin.com/en-AU/blog/?p=2893 | yes |
| S40 | Garmin: 2024 Garmin Connect Data Report | https://www.garmin.com/en-AU/blog/?p=3202 | yes |
| S41 | Athletech News: Garmin 2024 data report | https://athletechnews.com/track-running-hiit-pilates-garmin-data-report/ | yes |
| S42 | Garmin: 2025 Garmin Connect data report | https://www.garmin.com/en-PH/blog/?p=631 | yes |
| S43 | SGB: Pilates dominates ClassPass bookings in 2025 | https://sgbonline.com/pilates-dominates-fitness-bookings-for-classpass-in-2025/ | yes |
| S44 | Fortune: ClassPass 2024 Pilates | https://fortune.com/well/2024/12/27/pilates-health-benefits-classpass-fitness-trend/ | yes |
| S45 | ABC Fitness Wellness Watch Q1 2025 (PDF) | https://abcfitness.com/wp-content/uploads/Wellness-Watch-Q1-2025.pdf | yes (all 23 pages) |
| S46 | StrengthLog: Most popular gym exercises 2025 | https://www.strengthlog.com/most-popular-exercises/ | yes |
| S47 | StrengthLog: Top 10 strength training statistics (half a million users) | https://www.strengthlog.com/?p=19094 | yes |
| S48 | Boostcamp: State of Lifting 2025 | https://www.boostcamp.app/state-of-lifting-2025 | yes |
| S49 | Fitbod: 2022 Year in Review | https://fitbod.me/blog/fitbods-2022-year-in-review/ | yes |
| S50 | Fitbod: How strong is the average gym-goer (2026) | https://fitbod.me/blog/how-strong-is-the-average-gym-goer-we-analyzed-millions-of-real-workouts/ | yes |
| S51 | JEFIT: Most often selected exercises (2023) | https://www.jefit.com/blog/here-are-the-most-often-selected-exercises-for-jefit | yes |
| S52 | Long, J. (2023) MSc thesis, University of Calgary (equipment-sensor network in a fitness centre) | https://hdl.handle.net/1880/116677 | yes (PDF text) |
| S53 | Wilson et al. (2022) Gender differences in college student PA and campus recreational facility use, J Am Coll Health 70(5) | https://pure.psu.edu/en/publications/gender-differences-in-college-student-physical-activity-and-campu/ | yes |
| S54 | EGYM: Machine utilization (citing GYMetrix studies 2011–2018) | https://us.egym.com/en-us/machine-utilization | yes |
| S55 | The Fitness Network: 13 costly mistakes (GYMetrix founder interview, 2015) | https://thefitnessnetwork.org/blog/the-13-costly-mistakes-your-gym-is-making-due-to-a-lack-of-data | yes |
| S56 | YMCA of Pierce & Kitsap Counties: The Study – a better, stronger, faster gym experience | https://www.ymcapkc.org/node/1000750 | yes |
| S57 | HuffPost UK (2016): Are certain exercises better for men than women? (GYMetrix data) | https://huffingtonpost.co.uk/amp/entry/are-certain-exercises-better-for-men-than-women_n_11776510 | yes |
| S58 | Health Club Management (2014): Women's weight training could be key to growing gym market | https://www.healthclubmanagement.co.uk/health-club-management-news/Women&rsquo;s-weight-training-could-be-key-to-growing-gym-market-study/308388 | yes |
| S59 | 2026 State of the UK Fitness Industry Report, p.73 (Anytime Fitness) | https://online.flippingbook.com/view/55959561/73/ | yes |
| S60 | HYROX: The fitness race (format) | https://hyrox.com/the-fitness-race/ | yes |
| S61 | Orangetheory FAQ | https://www.orangetheory.com/en-us/faq | yes |
| S62 | Les Mills: Understanding the strength continuum | https://www.lesmills.com/articles/understanding-the-strength-continuum-2 | yes |
| S63 | Leisure Centre: Purposeful Gym Design (Parkwood case) | https://leisurecentre.com/Purposeful-Gym-Design | no (empty page; search snippet only) |
| S64 | 2025 State of the UK Fitness Industry Report, pp.94–95 (low-cost operators) | https://online.flippingbook.com/view/408285620/94-95 | yes |
| S65 | Club Solutions: 2025 fitness equipment trends | https://clubsolutionsmagazine.com/2025/11/2025-fitness-equipment-trends-what-drove-member-demand-in-health-clubs/ | yes |
