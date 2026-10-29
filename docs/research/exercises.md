# Exercise popularity and time per exercise (research slice: `exercises`)

Prepared 28 Oct 2026 for the gym-layout planner (demand model -> Erlang loss routing -> equipment selection -> floor packing).
Every number below is either quoted from a cited source (URL given, fetched unless stated) or explicitly marked **[derived]** / **[estimate]** with its derivation. Scripts and downloaded data used for derivations are listed in Section 11.

---

## 0. Key results for the model (TL;DR)

| Model input | Recommended value | Basis |
|---|---|---|
| Popularity weights for 92 strength exercises | Table 6.1 (`Cons %`, plus men/women vectors) | 50/50 mixture of StrengthLog share-of-sets (strength-focused users) and Fitbod sets-logged (general users) **[derived]** |
| Top-10 strength exercises (share of strength sets) | bench press 5.7 %, back squat 4.1 %, lat pulldown 3.2 %, deadlift 3.1 %, DB curl 2.6 %, DB lateral raise 2.2 %, leg press 2.2 %, OHP 2.1 %, DB row 2.1 %, leg extension 2.1 % | Table 6.1 **[derived]** |
| Cardio modality weights (share of cardio-machine occasions) | treadmill 40.8 %, upright+recumbent bike 25.5 %, elliptical 19.1 %, rower 6.2 %, stair climber 6.1 %, group cycle 2.4 % | SFIA 2024 Topline, 2023 participation-days |
| Share of member station-time on cardio vs strength | 40 % cardio / 60 % strength (range 35-45 %) | BLS ATUS 2003-06 time split = 43 % cardio **[derived]**, adjusted for HFA 2026 "free weights fastest-growing" **[estimate]** |
| Working sets per exercise | 3 (range 2-4) | ACSM 2026 (>=2 sets; strength plateaus ~2-3), Boostcamp 16.7 M sets / 1 M workouts with median 6 exercises -> ~2.8 planned sets **[derived]** |
| Warm-up sets | 2 for heavy barbell lifts, 1 for machine / DB compounds, 0 for isolation | Single-user Strong log: barbell lifts logged with 6-8 sets/session vs 2.5-3.5 for isolation **[estimate]** |
| Inter-set rest held at the station | heavy barbell 2.5 min (2-4); machine/DB compound 1.75-2 min; isolation 1.25 min (1-2); body-weight 1.5 min | ACSM 2009 (>=2-3 min core / 1-2 min assistance), Grgic 2018, Singer 2024, Ibbott 2019 (self-selected 3.5-4.6 min heavy squat), Silva 2018 survey (89 % of timers rest <=60 s) |
| Set duration | 0.6-0.75 min (36-45 s) | ACSM 2009 1-2 s CON + 1-2 s ECC x 8-12 reps; Schoenfeld 2015 0.5-8 s/rep **[derived]** |
| Station hold time per exercise bout | heavy barbell 11.8 min (9-18); loaded hip thrust / BB lunge 9.3; machine compound 8.0; DB compound 7.1; isolation 4.6; body-weight 4.7; functional 4.8; mean 7.1 | Section 5 **[derived]** |
| Cardio bout length | treadmill 27, bike 25, elliptical 25, stair 18, rower 15, air bike / SkiErg 10-12, spin class 45 min | ACSM 2011 (>=20-30 min/day), Girginer & Sahin 2007 observed ~21-22 min/machine, BLS 0.7 h/day **[estimate]** |
| Exercises per session | 6 (IQR 5-7) | Boostcamp 2025 median 6, p75 7 |
| Session length (strength) | median 58 min (Boostcamp), mean ~51 min (Strava weight training), visit 69 min (PureGym) | Section 4.3 |

---

## 1. Sources used

| id | Source | Publisher / year | What it measures | URL | Fetched |
|---|---|---|---|---|---|
| S1 | The Most Popular Gym Exercises for Men & Women in 2025 | StrengthLog, 26 Nov 2025 | % share of all logged sets, top 25 overall / men / women, >700,000 users | https://www.strengthlog.com/most-popular-exercises/ | yes |
| S2 | Top 10 Strength Training Statistics From Half a Million Users | StrengthLog, 2023 | frequency, muscle-group volume by sex, top-10 by sex | https://www.strengthlog.com/strength-training-statistics/ | yes |
| S3 | State of Lifting 2025 | Boostcamp, Feb 2026 | 1,000,000 sampled workouts, 16.7 M sets | https://www.boostcamp.app/state-of-lifting-2025 | yes |
| S4 | State of Lifting: The Gender Report | Boostcamp, Jun 2026 | ~1 M workouts, 168,190 athletes with verified gender | https://www.boostcamp.app/state-of-lifting/gender | yes |
| S5 | Fitbod exercise library ("Sets Logged", "Swapped N times") | Fitbod, accessed Oct 2026 | cumulative sets logged per exercise; swap counts | https://fitbod.me/exercises (+ /barbells, /dumbbells, /back, /chest, /shoulders, /quads, /glutes, /hamstrings, /triceps, /biceps, /abs, /calves, /lower-back, /abductors, /adductors, /trapezius and per-exercise pages) | yes |
| S6 | Fitbod 2025 State of Strength Report | Fitbod, Dec 2025 | 71 M workouts, 2.8 B sets (1 Dec 2024-1 Dec 2025) | https://fitbod.me/blog/fitbod-2025-state-of-strength-report/ | yes |
| S7 | Fitbod's 2022 Year in Review | Fitbod, 2023 | 15.8 M workouts; gender choice ratios | https://fitbod.me/blog/fitbods-2022-year-in-review/ | yes |
| S8 | How strong is the average gym-goer? | Fitbod, 2025/26 | lifter counts, typical loads | https://fitbod.me/blog/how-strong-is-the-average-gym-goer-we-analyzed-millions-of-real-workouts/ | yes |
| S9 | Strength Level strength standards | Strength Level, data to Mar 2026 | community lifts per exercise; male/female qualifying results | https://strengthlevel.com/strength-standards (+ /strength-standards/<exercise>) | yes |
| S10 | Most often selected exercises / per-muscle / arms / legs | JEFIT blog 2022-2024 | ranks only (no counts) | https://www.jefit.com/workout-tips/here-are-the-most-often-selected-exercises-for-jefit ; https://www.jefit.com/exercise-tips/most-popular-jefit-exercise-for-major-muscle-groups ; https://www.jefit.com/workout-tips/the-most-popular-arm-exercises-according-to-jefit-app ; https://www.jefit.com/wp/exercise-tips/most-popular-leg-exercises-seen-by-jefit-app | yes |
| S11 | SFIA 2024 Topline Participation Report (2023 data) | Sports & Fitness Industry Association, 2024 | participants, mean days, occasions per activity; 18,000 online interviews | https://www.usta.com/es/content/dam/usta/sections/intermountain/districts/colorado/pdfs/sfia-reports/2024-sfia-topline.pdf | yes (PDF downloaded) |
| S12 | ACSM Position Stand: Progression Models in Resistance Training for Healthy Adults (Ratamess et al.) | MSSE 41(3):687-708, 2009 | sets, reps, rest, frequency | https://sfu.ca/~ryand/kin343/ACSMresistance.pdf (PubMed 19204579) | yes (PDF downloaded) |
| S13 | ACSM Position Stand: Resistance Training Prescription ... An Overview of Reviews (Currier ... Phillips) | MSSE 58(4):851-872, 2026 | updated prescription | https://pmc.ncbi.nlm.nih.gov/articles/PMC12965823 ; release https://acsm.org/resistance-training-guidelines-update-2026/ | yes |
| S14 | ACSM Position Stand: Quantity and quality of exercise (Garber et al.) | MSSE 43(7):1334-59, 2011 | cardio minutes/day | https://pubmed.ncbi.nlm.nih.gov/21694556/ | yes |
| S15 | Longer interset rest periods... (Schoenfeld et al.) | JSCR 30(7):1805-12, 2016 | 1 vs 3 min rest; 7 ex x 3 sets protocol | https://pubmed.ncbi.nlm.nih.gov/26605807/ | yes |
| S16 | Effects of rest interval duration... strength: systematic review (Grgic et al.) | Sports Med 2018 | rest recommendations | https://pubmed.ncbi.nlm.nih.gov/28933024/ | yes |
| S17 | Give it a rest... Bayesian meta-analysis (Singer et al.) | Front Sports Act Living 2024 | rest vs hypertrophy; NSCA 30-90 s | https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2024.1429789/full | yes |
| S18 | Self-paced vs prescribed inter-set rest (Ibbott et al., IJSPP 14(7):980-986, 2019) - NSWIS summary | NSWIS, 2019 | self-selected rest in heavy squats | https://www.nswis.com.au/nswis-news/the-effect-of-self-paced-and-prescribed-interset-rest-strategies-on-performance-in-strength-training/ | yes |
| S19 | Profiling Rest Intervals between Sets... (Silva et al.) | Sports (Basel) 2018 | survey of 415 gym users (Brazil) | https://pmc.ncbi.nlm.nih.gov/articles/PMC6316470/ | yes |
| S20 | Effect of repetition duration... (Schoenfeld, Ogborn, Krieger) | Sports Med 45(4):577-85, 2015 | rep duration | https://pubmed.ncbi.nlm.nih.gov/25601394/ | yes |
| S21 | Strava Year in Sport 2025 (via Athletech News) | Athletech News, Dec 2025 | mean weight-training session; gender | https://athletechnews.com/running-walking-strength-training-strava-year-in-sport-report/ | yes |
| S22 | BLS Spotlight on Statistics: Sports and Exercise (ATUS 2003-06) | U.S. Bureau of Labor Statistics, May 2008 | % of exercisers and hours/day for weightlifting vs cardio equipment | https://www.bls.gov/spotlight/2008/sports/ | no - page returned empty to the fetcher; values read from a PDF copy of the Spotlight downloaded earlier in this session (scratchpad `research/downloads/bls_spotlight2008/`) |
| S23 | Spor tesislerinde kuyruk problemine yonelik bir benzetim uygulamasi (Girginer & Sahin) | Hacettepe J Sport Sci 18(1):13-30, 2007 | observed cardio-machine use times at a gym (45 days) | https://dergipark.org.tr/en/download/article-file/151321 | yes (PDF) |
| S24 | PureGym data (via The Manual) | The Manual | average gym visit length | https://themanual.com/fitness/new-data-shows-the-top-reasons-why-people-quit-the-gym | yes |
| S25 | How long should a workout be? | Hevy | duration guidance, example rests | https://www.hevyapp.com/how-long-should-a-workout-be/ | yes |
| S26 | Kaggle "weightlifting" (Strong app export, 1 user) | Kaggle user joep89, 2019 | logged sets/exercises per workout | https://www.kaggle.com/datasets/joep89/weightlifting | yes (CSV downloaded) |
| S27 | free-exercise-db (876 exercises with equipment field) | GitHub yuhonas | exercise -> equipment class | https://github.com/yuhonas/free-exercise-db (raw: https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json) | yes (JSON downloaded) |
| S28 | Quantification of weekly strength-training volume per muscle group in competitive physique athletes (da Silveira et al.) | Front Sports Act Living, 2025 | n = 154; exercise use % by sex; sets by region | https://www.frontiersin.org/articles/10.3389/fspor.2025.1536360/full | yes |
| S29 | Training practices of recreationally resistance trained-women (Barbosa et al.) | J Trainology 12(1), 2023 | 1,019 women; lower-limb set distribution | https://www.jstage.jst.go.jp/article/trainology/12/1/12_1/_article/-char/en | yes (abstract) |
| S30 | HFA gym membership climbs 5.6 % in 2025 (HFA 2026 U.S. Health & Fitness Consumer Report) | SGB Media, 2026 | equipment-usage trend | https://sgbonline.com/hfa-gym-membership-climbs-5-6-percent-in-2025/ | yes |
| S31 | SFIA 2022 numbers (via The Barbell) | The Barbell | treadmill / dumbbell participants 2022 | https://thebarbell.com/?p=13439 | yes |
| S32 | Most performed exercises (StrengthLog via The Barbell) | The Barbell, Nov 2024 | secondary copy of S2 | https://thebarbell.com/most-performed-exercises/ | yes |

Not usable / not found: Hevy, Strong, Alpha Progression, Gymshark and Strava publish no per-exercise frequency tables (searched; Hevy's own blog only states bench press "is by far our most popular exercise", https://www.hevyapp.com/stronger-with-hevy/). SFIA single-sport reports (upright vs recumbent split, gender) are paywalled. NSCA *Essentials* tables are not online (cited via S17).

---

## 2. Strength-exercise popularity by source

### 2.1 StrengthLog 2025 - share of all logged sets (S1)
Sample: "millions of workouts" from "over 700,000 users"; metric = % of all logged sets. Top 25 overall = 62.6 % of all sets **[derived: sum of the 25 shares]**.

| Rank | Overall | % | Men | % | Women | % |
|---|---|---|---|---|---|---|
| 1 | Bench Press | 9.7 | Bench Press | 10.7 | Bench Press | 8.2 |
| 2 | Squat | 7.0 | Squat | 6.7 | Squat | 7.7 |
| 3 | Deadlift | 5.0 | Deadlift | 4.8 | Deadlift | 5.4 |
| 4 | Lat Pulldown | 3.8 | Lat Pulldown | 3.6 | Lat Pulldown | 4.1 |
| 5 | Overhead Press | 3.4 | Overhead Press | 3.5 | Overhead Press | 3.0 |
| 6 | Barbell Row | 3.2 | Barbell Row | 3.2 | Barbell Row | 2.9 |
| 7 | Dumbbell Lateral Raise | 2.7 | Dumbbell Lateral Raise | 2.8 | Leg Press | 2.7 |
| 8 | Leg Extension | 2.5 | Leg Extension | 2.4 | Leg Extension | 2.7 |
| 9 | Leg Press | 2.2 | Barbell Curl | 2.4 | Dumbbell Lateral Raise | 2.6 |
| 10 | Barbell Curl | 2.1 | Tricep Pushdown With Bar | 2.1 | Hip Thrust | 2.0 |
| 11 | Tricep Pushdown With Bar | 2.0 | Incline Dumbbell Press | 2.1 | Romanian Deadlift | 1.7 |
| 12 | Incline Dumbbell Press | 1.9 | Pull-Up | 2.0 | Cable Close Grip Seated Row | 1.6 |
| 13 | Dumbbell Curl | 1.7 | Leg Press | 1.9 | Dumbbell Shoulder Press | 1.6 |
| 14 | Pull-Up | 1.7 | Dumbbell Curl | 1.8 | Dumbbell Curl | 1.6 |
| 15 | Cable Close Grip Seated Row | 1.6 | Cable Close Grip Seated Row | 1.5 | Dumbbell Row | 1.5 |
| 16 | Tricep Pushdown With Rope | 1.5 | Tricep Pushdown With Rope | 1.5 | Tricep Pushdown With Bar | 1.5 |
| 17 | Lying Leg Curl | 1.3 | Lying Leg Curl | 1.3 | Barbell Curl | 1.4 |
| 18 | Dumbbell Row | 1.3 | Dumbbell Row | 1.2 | Bulgarian Split Squat | 1.4 |
| 19 | Dumbbell Shoulder Press | 1.3 | Standing Cable Chest Fly | 1.2 | Tricep Pushdown With Rope | 1.3 |
| 20 | Romanian Deadlift | 1.3 | Seated Leg Curl | 1.2 | Seated Leg Curl | 1.3 |
| 21 | Seated Leg Curl | 1.2 | Hammer Curl | 1.2 | Incline Dumbbell Press | 1.3 |
| 22 | Hammer Curl | 1.1 | Dumbbell Shoulder Press | 1.2 | Lying Leg Curl | 1.2 |
| 23 | Standing Cable Chest Fly | 1.1 | Close-Grip Bench Press | 1.1 | Stiff-Legged Deadlift | 1.1 |
| 24 | Dumbbell Chest Press | 1.0 | Dumbbell Chest Press | 1.1 | Hip Abduction Machine | 1.0 |
| 25 | Face Pull | 1.0 | Romanian Deadlift | 1.1 | Face Pull | 1.0 |

Verbatim gender statements (S1/S2): men train the bench press "30% more", the barbell curl "71% more"; women train the leg press "42% more" and the hip thrust "830% more" than men. S2: men do "64% more training for biceps, 50% more for chest, and 46% more for triceps"; women do "43% more training for glutes and 28% more for thigh muscles"; oblique work ~2x in women; "The average workout frequency is 3.3 workouts per week."

**[derived]** Female share of StrengthLog sets implied by overall = p_f x women + (1-p_f) x men, least squares over 20 exercises present in all three lists: **p_f = 0.35**. Men's hip-thrust share implied by "+830 %": 2.0 / 9.3 = **0.22 %**.

### 2.2 Fitbod - cumulative "Sets Logged" (S5)
Fitbod ranks exercises "based on how many sets have been logged by Fitbod users". Selected values (all exact page values):

| Exercise | Sets logged | Exercise | Sets logged |
|---|---|---|---|
| Dumbbell Bicep Curl | 11,988,008 | Machine Fly | 3,744,823 |
| Hammer Curls | 10,391,123 | Dumbbell Squat | 3,743,936 |
| Dumbbell Row | 10,105,842 | Calf Raise | 1,515,400 |
| Dumbbell Bench Press | 10,009,222 | Cable Tricep Pushdown | 3,797,656 |
| Lat Pulldown | 9,684,781 | Cable Crossover Fly | 3,148,104 |
| Barbell Bench Press | 8,702,771 | Dip | 3,169,684 |
| Dumbbell Shoulder Press | 7,993,508 | Ab Crunch Machine | 2,812,905 |
| Dumbbell Fly | 7,705,017 | Lying Hamstrings Curl | 2,755,579 |
| Cable Row | 7,243,267 | Cable Face Pull | 2,496,755 |
| Dumbbell Skullcrusher | 6,955,739 | Cable Lateral Raise | 2,405,679 |
| Push Up | 6,723,750 | Seated Back Extension | 2,359,595 |
| Dumbbell Front Raise | 6,658,201 | Barbell Hip Thrust | 2,313,022 |
| Cable Rope Tricep Extension | 6,634,413 | Machine Leg Press | 2,169,424 |
| Leg Extension | 6,456,032 | Chin Up | 2,164,015 |
| Crunches | 6,413,700 | Machine Row | 2,150,001 |
| Barbell Curl | 6,392,670 | Machine Bench Press | 2,083,700 |
| Back Squat | 6,036,005 | Front Squat | 2,014,709 |
| Leg Press | 5,489,749 | Preacher Curl | 1,877,663 |
| Seated Tricep Press | 5,268,021 | Hammerstrength Chest Press | 1,798,337 |
| Deadlift | 5,108,578 | Machine Hip Abductor | 1,747,865 |
| Dumbbell Incline Bench Press | 5,092,125 | Glute Kickback Machine | 1,727,762 |
| Dumbbell Lunge | 5,051,344 | Cable Crunch | 1,707,669 |
| Dumbbell Rear Delt Raise | 5,008,862 | Hammerstrength Iso Row | 1,627,758 |
| Plank | 4,951,454 | Hammerstrength High Row | 1,580,411 |
| EZ-Bar Curl | 4,849,955 | Machine Bicep Curl | 1,532,249 |
| Dumbbell Romanian Deadlift | 4,633,512 | Machine Tricep Dip | 1,522,390 |
| Dumbbell Shoulder Raise (a lateral raise) | 4,548,625 | Seated Machine Calf Press | 1,468,648 |
| Pull Up | 4,343,343 | Kettlebell Swing | 1,472,336 |
| Hip Thrust (unspecified loading) | 4,324,303 | Machine Shoulder Press | 1,446,091 |
| Seated Leg Curl | 4,254,937 | Machine Hip Adductor | 1,417,813 |
| Bench Dip | 4,217,199 | Calf Press (on leg press) | 1,338,090 |
| Close-Grip Bench Press | 4,046,080 | Machine Tricep Extension | 1,300,142 |
| Back Extensions (GHR/45-degree bench) | 3,999,754 | Machine Preacher Curl | 1,241,092 |
| Barbell Incline Bench Press | 3,953,814 | Hanging Leg Raise | 1,228,387 |
| Barbell Shoulder Press | 3,789,263 | Hack Squat | 1,085,651 |
| Bent Over Barbell Row | 3,420,702 | Smith Machine Squat | 973,303 |
| Romanian Deadlift | 3,386,245 | T-Bar Row | 879,374 |
| Dumbbell Shrug | 3,012,522 | Hammerstrength Shoulder Press | 785,601 |
| Skullcrusher (bar) | 3,008,701 | Standing Machine Calf Press | 613,332 |
| Dumbbell Hip Thrust | 1,057,468 | Trap Bar Deadlift | 392,684 |
| Ab Rollout | 1,237,222 | Glute Ham Raise | 255,369 |
| Battle Ropes | 197,286 | Sled Push / Drag / Pull | 120,469 / 93,467 / 39,462 |
| Box Jump | 407,558 | Wall Ball | 86,546 |

Other Fitbod findings: 2025 report - "analyzed 71 million workouts, 2.8 billion lifting sets"; most-logged exercises 2025: Dumbbell Bicep Curl, Lat Pulldown, Dumbbell Bench Press, Hammer Curl, Dumbbell Row (S6); "Barbell back squat ranks around 30th by number of lifters", deadlift "around 38th", more users log DB bench than barbell bench (S8). 2022 (S7): Leg Press was #1 by total volume lifted (8.3 B lb), then bench (5.9 B) and lat pulldown (5.4 B) = 12 % of all volume; "Treadmill Walking" was the 2nd most manually-added exercise (396,000 adds, after bench 410,000).

### 2.3 Strength Level - community lifts and female share (S9)
Totals: "195,513,376 community lifts" from "27,893,268" users. Counts are 1RM/strength-check entries, so they over-represent the big barbell lifts (bench 48.7 M vs lat pulldown 2.0 M) and are used here mainly for **sex mix per exercise**.

| Exercise | Community lifts | Qualifying M | Qualifying F | Female share |
|---|---|---|---|---|
| Bench Press | 48,718,584 | 9,906,475 | 1,017,062 | 9.3 % |
| Squat | 24,988,444 | 6,014,970 | 1,024,968 | 14.6 % |
| Deadlift | 22,978,599 | 5,398,185 | 995,561 | 15.6 % |
| Shoulder Press | 5,644,500 | 1,622,185 | 205,287 | 11.2 % |
| Pull Ups | 4,852,758 | 1,220,115 | 127,994 | 9.5 % |
| Dumbbell Bench Press | 4,734,253 | 1,144,906 | 110,778 | 8.8 % |
| Dumbbell Curl | 3,634,702 | 844,943 | 113,053 | 11.8 % |
| Push Ups | 2,928,475 | 776,543 | 99,110 | 11.3 % |
| Sled Leg Press | 2,661,088 | 569,448 | 158,689 | 21.8 % |
| Barbell Curl | 2,565,545 | 686,253 | 66,256 | 8.8 % |
| Incline Dumbbell Bench Press | 2,367,587 | 611,670 | 35,630 | 5.5 % |
| Incline Bench Press | 2,165,292 | 568,407 | 25,560 | 4.3 % |
| Bent Over Row | 2,162,181 | 650,326 | 86,969 | 11.8 % |
| Dips | 2,162,628 | 489,613 | 27,862 | 5.4 % |
| Dumbbell Shoulder Press | 2,106,645 | 540,746 | 80,451 | 13.0 % |
| Lat Pulldown | 2,011,718 | 598,899 | 129,195 | 17.7 % |
| Front Squat | 1,597,959 | 403,428 | 110,429 | 21.5 % |
| Hex Bar Deadlift | 1,437,859 | 288,570 | 46,602 | 13.9 % |
| Chin Ups | 1,225,888 | 229,507 | 27,929 | 10.8 % |
| Hip Thrust | 1,221,785 | 158,924 | 224,489 | **58.6 %** |
| Dumbbell Lateral Raise | 1,211,431 | 281,425 | 33,087 | 10.5 % |
| Leg Extension | 1,152,891 | 298,464 | 74,196 | 19.9 % |
| Romanian Deadlift | 1,151,417 | 264,363 | 95,377 | 26.5 % |
| Horizontal Leg Press | 945,397 | 180,003 | 90,488 | 33.5 % |
| Dumbbell Row | 927,185 | 209,928 | 42,757 | 16.9 % |
| Chest Press (machine) | 822,882 | 180,929 | 25,479 | 12.3 % |
| Tricep Pushdown | 805,104 | 214,143 | 23,852 | 10.0 % |
| Hammer Curl | 752,185 | 182,235 | 16,192 | 8.2 % |
| Seated Cable Row | 711,455 | 177,068 | 33,327 | 15.8 % |
| Hack Squat | 564,866 | 135,021 | 18,860 | 12.3 % |
| Machine Shoulder Press | 488,940 | 105,396 | 12,143 | 10.3 % |
| Machine Chest Fly | 487,945 | 134,143 | 11,191 | 7.7 % |
| Dumbbell Bulgarian Split Squat | 482,453 | 75,522 | 28,457 | 27.4 % |
| Seated Leg Curl | 457,839 | 98,023 | 27,521 | 21.9 % |
| EZ Bar Curl | 457,832 | 96,954 | 5,482 | 5.4 % |
| Goblet Squat | 385,610 | 47,926 | 23,544 | 32.9 % |
| Barbell Shrug | 372,602 | 72,216 | 3,194 | 4.2 % |
| T Bar Row | 368,631 | 79,547 | 6,351 | 7.4 % |
| Lying Leg Curl | 358,631 | 62,636 | 14,216 | 18.5 % |
| Machine Calf Raise | 350,435 | 66,968 | 10,235 | 13.3 % |
| Dumbbell Fly | 345,131 | 67,623 | 7,334 | 9.8 % |
| Hip Adduction | 344,261 | 21,353 | 14,321 | **40.1 %** |
| Smith Machine Bench Press | 341,390 | 58,928 | 3,483 | 5.6 % |
| Smith Machine Squat | 276,386 | 39,296 | 8,857 | 18.4 % |
| Seated Calf Raise | 253,479 | 36,941 | 5,188 | 12.3 % |
| Cable Fly | 236,590 | 30,763 | 2,390 | 7.2 % |
| Hip Abduction | 203,182 | 22,679 | 25,248 | **52.7 %** |
| Face Pull | 181,223 | 28,796 | 7,505 | 20.7 % |

### 2.4 Boostcamp State of Lifting 2025 and Gender Report (S3, S4)
* Workouts containing the exercise (of 1 M sampled): bench press 172 K ("15% more than squat (150K) and 74% more than deadlift (99K)"), DB lateral raise 153 K, squat 150 K, leg extension 147 K, lat pulldown 140 K, deadlift 99 K, cable lateral raise 85 K; lateral raises combined 238 K. **[derived]** => P(exercise appears in a session): bench 17.2 %, DB lateral raise 15.3 %, squat 15.0 %, leg extension 14.7 %, lat pulldown 14.0 %, deadlift 9.9 %, cable lateral raise 8.5 %.
* Most common same-session pairs: leg curl + leg extension 59 K; bench press + incline DB bench 35 K; lat pulldown + seated cable row 30 K (co-location hint for layout).
* Skip rates (share of programmed sets skipped): seated calf raise 38 %, cable crunch 36 %, standing calf raise 36 %, hanging leg raise 34 %, leg curl 28 %, leg press 26 %, leg extension 24 %, barbell squat 17 %, bench press 10 %. Totals: 13.1 M sets completed, 3.5 M skipped; leg-exercise skip 24 % vs upper-body 18 %; "Nearly half of all users who train legs never log a single calf exercise."
* Training splits tagged: upper/lower 139 K, PPL 74 K, bro split 26 K, full body 15 K.
* Gender report: skipped sets women 16.2 % vs men 21.6 %; top-10 overlap men vs women 8/10 (advanced), 7/10 (intermediate), 6/10 (beginner); advanced shared: bench, squat, lat pulldown, leg extension, deadlift, lateral raise, RDL, seated row. "Women-coded" lifts: Hip Abductor (Machine) #9 for beginner women (9.5 % of workouts); Hip Thrust (Barbell) #10 for beginner (8.4 %) and intermediate (8.2 %) women; neither in any men's top 10. Equipment mix of logged exercises: bodyweight 14.7 % (beginner women) vs 6.4 % (beginner men); barbell 18.0 % (beginner women) to 23.3 % (advanced women) vs ~24-28 % for men.

### 2.5 JEFIT (S10) - ranks only
"Barbell Bench Press", "Barbell Bicep Curl" and "Wide Grip Lat Pull-Down" are the three most-selected exercises (10 M+ members, 1,350+ exercises; Mar 2023). Machine-column ranking (downloads over the past decade, May 2024) - legs: Prone Leg Curl, Leg Extension, Leg Press, Seated Leg Curl, Smith Machine Squat, Hack Squat, Thigh (Hip) Abduction, Thigh (Hip) Adduction ...; chest: Machine Fly, Cable Crossover, Machine Bench Press, Incline Chest Press, Smith Bench ...; back: Wide Grip Lat Pulldown, Cable Seated Row, Back Hyperextension ...; shoulders: Machine Shoulder Press, Machine Shrug ...; triceps (machine): Machine Dip, Cable Rope Triceps Extension, Cable Pushdown. Arms list (May 2022): "Dip" leads triceps, "Barbell Curl" leads biceps; community "more than 92,000,000 workouts".

### 2.6 Other sex-difference evidence
* **Fitbod 2022 (S7)** choice ratios - men over women: chin-ups 5.04x, preacher curls 4.93x, dips 2.83x, back squat 1.40x, deadlift 1.40x; women over men: DB hip thrust 5.58x, DB sumo squat 5.30x, DB glute bridge 3.77x, barbell hip thrust 3.42x, DB Bulgarian split squat 2.55x, single-leg RDL 2.22x, jump squats 1.71x; women prefer "59 of 67 squat and deadlift variations".
* **Fitbod 2025 (S6)**: "Women trained glutes 56% more than men"; "Men logged 73% more bro-split workouts"; "Women logged 23% more mobility exercises".
* **Strava 2025 (S21)**: "Women logged weight training activities at rates 21% higher than men."
* **BLS ATUS 2003-06 (S22)**: weightlifting participants 64 % male / 36 % female; "using cardiovascular equipment" 44 % male / 56 % female.
* **da Silveira et al. 2025 (S28)**, 154 physique athletes: "Men generally performed a higher volume of upper body sets (47.2 +/- 14.6) compared to women (18.2 +/- 7.4)"; lower body women 23.8 +/- 11.2 vs men 11.5 +/- 7.0. Most-used exercises - men off-season: seated hamstring-curl machine 83 %, seated calf raise 82 %, lateral raise 81 %, lat pulldown 78 %, 45-degree leg press 77 %; women pre-contest: hip thrust 80 %, seated hamstring curl 77 %, stiff-leg deadlift 77 %, squat 74 %, leg extension 71 %.
* **Barbosa et al. 2023 (S29)**, 1,019 recreational women: lower-limb weekly sets = quadriceps 34.29 %, gluteus maximus 28.57 %, knee flexors 11.43 %, hip adductors 8.57 %, gluteus medius 8.57 %, triceps surae 8.57 %.

### 2.7 Source agreement and biases **[derived]**
Spearman rank correlation (script `compute_weights.py`): StrengthLog vs Fitbod on StrengthLog's top 25 = **0.06** (essentially uncorrelated within the top 25); StrengthLog vs Strength Level = **0.66** (n = 24); Fitbod vs Strength Level = **0.56** (n = 47). Interpretation: StrengthLog and Strength Level users are strength-focused barbell lifters (StrengthLog: "our users are probably in the top 10% (or higher) of the population in terms of strength"), while Fitbod's algorithm and user base (60 % new to strength training in 2025; many home users) pushes dumbbell and machine isolation work (DB curl is #1). The median ratio StrengthLog% / Fitbod% on the overlap is 1.27 (range 0.33 for hammer curl to 3.84 for bench press). Neither population alone is "the average commercial-gym member", hence the 50/50 mixture in Section 5.1.

---

## 3. Cardio-modality popularity

### 3.1 SFIA 2024 Topline (2023 data; U.S. ages 6+; 18,000 online interviews) (S11)

| Activity | Participants 2023 | Mean days/participant | Occasions (participant-days) | Casual (1-49x) | Core (50+x) | 1-yr change |
|---|---|---|---|---|---|---|
| Treadmill | 54,829 K | 65 | 3.565 B | 27,992 K | 26,837 K | +2.3 % |
| Stationary Cycling (Recumbent/Upright) | 32,628 K | 68 | 2.228 B | 15,901 K | 16,728 K | +1.6 % |
| Elliptical Motion/Cross-Trainer | 27,062 K | 62 | 1.672 B | 13,898 K | 13,164 K | 0.0 % |
| Rowing Machine | 12,775 K | 42 | 0.539 B | 8,473 K | 4,302 K | +7.4 % |
| Stair-Climbing Machine | 12,605 K | 42 | 0.530 B | 8,075 K | 4,530 K | +8.0 % |
| Stationary Cycling (Group) | 6,227 K | 34 | 0.211 B | 3,783 K | 2,444 K | -0.7 % |
| Free Weights (Dumbbells/Hand Weights) | 53,858 K | 80 | 4.309 B | 23,238 K | 30,619 K | +1.4 % |
| Free Weights (Barbells) | 29,333 K | 77 | 2.255 B | 14,174 K | 15,159 K | +2.3 % |
| Weight/Resistance Machines | 29,426 K | 77 | 2.256 B | 11,361 K | 18,065 K | -1.9 % |
| Kettlebells | 14,466 K | 64 | 0.928 B | 8,517 K | 5,949 K | +5.6 % |
| Bodyweight Exercise & Accessory-Assisted | 22,578 K | 86 | 1.937 B | 10,486 K | 12,092 K | +2.5 % |
| High Impact/Intensity Training | 21.8 M | 61 | 1.326 B | 12,559 K | 9,242 K | -0.1 % |
| Cross-Training Style Workouts | 9,404 K | 53 | 0.499 B | 4,391 K | 5,013 K | +1.7 % |
| Yoga | 34,249 K | 57 | 1.950 B | - | - | +1.8 % |

SFIA text: "Health club-based activities (Treadmill, Stair-Climbing Machine, Stationary Cycling [Recumbent/Upright], and Rowing Machine) all had good participation increases from 2022." Older figure (S31): treadmill 53.6 M and dumbbells 53.1 M participants in 2022.

**[derived]** Shares of cardio-machine occasions (sum 8.745 B): treadmill 40.8 %, upright+recumbent bike 25.5 %, elliptical 19.1 %, rower 6.2 %, stair climber 6.1 %, group cycle 2.4 %. Shares of (overlapping) strength-category occasions (sum 11.685 B): dumbbells 36.9 %, machines 19.3 %, barbells 19.3 %, body-weight 16.6 %, kettlebells 7.9 %.
Caveat: SFIA counts any venue (home + club); treadmill and dumbbells include home use, so club shares of elliptical/stair/rower are likely somewhat higher than these national shares.

### 3.2 Facility-level observation (S23)
Girginer & Sahin (2007) observed a Turkish fitness centre for 45 days: bottleneck cardio area = 5 treadmills, 5 recumbent bikes, 4 air-walker/glider machines ("uzay yuruyusu"); console default "20 dakika" (20 min); bike use modelled as a fixed 20 min; first (warm-up) machine chosen: 75 % bike, 20 % glider, 5 % treadmill; last machine: 45 % treadmill, 20 % bike, 5 % glider, 30 % leave directly. Simulated value-added time per customer: bike 0.36 h, glider 0.35 h, treadmill 0.37 h (i.e. ~21-22 min per machine), other equipment 0.68 h, total 0.87 h; bikes had a 1.36 h mean queue (5.66 people) - a real-world case of under-provisioned bikes.

### 3.3 Time split cardio vs strength
BLS ATUS 2003-06 (S22): on an average day, among people who exercised, 13.1 % did weightlifting and 12.7 % used cardiovascular equipment; participants spent 0.9 h (weightlifting) and 0.7 h (cardio equipment). **[derived]** time-weighted split = 13.1x0.9 : 12.7x0.7 = 57 % strength : 43 % cardio. HFA 2026 (S30): "Free weight usage - dumbbells, barbells and kettlebells - has grown faster than any other equipment category since 2021", with a shift "away from some traditional high-intensity and stand-alone cardio options". **Recommended default: 40 % cardio / 60 % strength station-time [estimate]**, range 35-45 %; gyms targeting older adults should move toward 45-50 % cardio, strength-focused gyms toward 25-30 %.

### 3.4 Modalities not covered by SFIA **[estimate]**
No usage statistic was found for air bikes, SkiErgs, curved non-motorised treadmills or seated recumbent steppers. Recommended nominal model weights (as a fraction of cardio occasions, taken *out of* the SFIA modality they substitute for): air bike 1.5 % (from rower + stationary-bike share; HIIT/cross-training population = SFIA HIIT 21.8 M and cross-training 9.4 M participants), SkiErg 0.75 % (from rower), curved treadmill 2 % (from treadmill; same user need), recumbent stepper 1 % (from recumbent bike; older-adult facilities only). Confidence: low - these are diversity items for the selector, not demand-driven items.

---

## 4. Training prescriptions and logged session structure

### 4.1 Guidelines

| Source | Statement (verbatim or table pointer) |
|---|---|
| ACSM 2009 (S12), Table 2 | "It is recommended that 1-3 sets per exercise be used by novice individuals." / "Multiple-set programs ... are recommended for progression to intermediate and advanced training." |
| ACSM 2009, Table 2 | "rest periods of at least 2-3 min be used for core exercises using heavier loads ... For assistance exercises, a shorter rest period length of 1-2 min may suffice." |
| ACSM 2009, Table 2 (hypertrophy) | "moderate loading be used (70-85% of 1 RM) for 8-12 repetitions per set for 1-3 sets per exercise" (novice/intermediate); advanced "3-6 sets per exercise"; "1- to 2-min rest periods be used in novice and intermediate training" |
| ACSM 2009, abstract | loads "8-12 repetition maximum" for novices; heavy loading "using 3- to 5-min rest periods between sets performed at a moderate contraction velocity (1-2 s CON; 1-2 s ECC)"; endurance "short rest periods (<90 s)"; frequency "2-3 d/wk for novice ... 3-4 ... intermediate ... 4-5 ... advanced"; the 2002/1998 minimum standard "one set of 8-12 repetitions for 8-10 exercises" |
| ACSM 2009, Table 2 (endurance/circuit) | "For circuit weight training, it is recommended that rest periods correspond to the time needed to get from one exercise station to another." |
| ACSM 2026 (S13) | "healthy adults are advised to complete at least two sets per exercise"; strength gains plateau at ~2-3 sets/exercise; hypertrophy enhanced by "higher volume (>=10 sets/muscle group/wk)"; strength favoured by ">=80% one-repetition maximum"; train "at least twice weekly, with all major muscle groups being engaged"; "short (<1 min) versus long (>1 min) between-set rest intervals" did not affect strength; machines vs free weights did not affect strength. Press release: "80% of 1RM for 2-3 sets per exercise", "about 10 sets per muscle group per week". |
| ACSM 2011 (S14) | cardio ">=30 min.d on >=5 d.wk for a total of >=150 min.wk" (moderate) or ">=20 min.d on >=3 d.wk (>=75 min.wk)" (vigorous); resistance exercise "On 2-3 d.wk ... for each of the major muscle groups" |
| NSCA (via S17) | Singer et al. 2024 cite "the NSCA's 30-90 s recommendation" for hypertrophy rest and argue it "warrant[s] reconsideration". |
| Schoenfeld et al. 2016 (S15) | protocol "3 sets of 8-12 repetition maximum (RM) of 7 different exercises per session", 3 sessions/wk; 3-min rest beat 1-min rest for strength and thigh hypertrophy. |
| Grgic et al. 2018 (S16) | "robust gains in muscular strength can be achieved even with short RIs (< 60 s)"; "longer duration RIs (> 2 min) are required to maximize strength gains in resistance-trained individuals"; untrained: "short to moderate RIs (60-120 s) are sufficient". |
| Singer et al. 2024 (S17) | "a small hypertrophic benefit to employing inter-set rest interval durations >60 s"; "did not detect appreciable differences in hypertrophy when resting >90 s between sets". |
| Schoenfeld et al. 2015 (S20) | "hypertrophic outcomes are similar when training with repetition durations ranging from 0.5 to 8 s"; >10 s per rep inferior. |
| Hevy (S25) | guidance: beginner "25 to 40 minutes", intermediate "roughly 50 to 60 minutes", advanced "at least 70 minutes"; example programs: compound 2-3 min rest, isolation 1-1.5 min, 2-4 sets. |

### 4.2 What lifters actually do (rest)
* **Silva et al. 2018 (S19)**, 415 Brazilian gym members (198 women, 217 men), training 3.9 +/- 1.3 sessions/wk: 71.6 % control their rest; of those, rest used = 15 s 24.3 %, 30 s 26.7 %, 45 s 13.3 %, 60 s 24.6 %, 90 s 2.7 %, >90 s 1 %; "88.9% of the participants that reported controlling RIs adopt an RI of up to 60 s" (abstract says 95.0 %; internal inconsistency noted).
* **Ibbott et al. 2019 (S18)**, 16 strength-trained men, 5 x 5 heavy back squat: self-selected rest rose "from 207.52 to 277.71 s" from set 1 to set 4 (3.5-4.6 min).
* Interpretation: general members doing machine/isolation work rest about 30-60 s (they rarely time rest >60 s), while heavy barbell lifters rest 2-5 min. Hence class-specific rests in Section 5.

### 4.3 Logged session structure
| Metric | Value | Source |
|---|---|---|
| Session duration, median / p75 / p90 / mean | 58 / 79 / ~109 / 87 min | Boostcamp 2025 (S3) - mean inflated by sessions left running |
| Unique exercises per session | median 6, p75 7; 44 % of workouts have 5-6; 7 % of lifters "regularly program 9 or more"; <9 % of sessions have only 2 | S3 |
| Sets per workout | 16.7 M sets tracked / 1 M workouts = 16.7 planned; 13.1 M completed = 13.1 **[derived]** | S3 |
| Sets per exercise | 16.7 / 6 = 2.8 planned, 13.1 / 6 = 2.2 completed **[derived]** (median exercises used as proxy for mean) | S3 |
| Minutes per exercise, all-in | 58 / 6 = 9.7 min **[derived]** | S3 |
| Training frequency | median 2.7 days/wk (Boostcamp); 3.3 workouts/wk (StrengthLog); 3.9 sessions/wk (Silva 2018) | S3, S2, S19 |
| Weight-training activity length | "The average strength session lasted just over 50 minutes." (Strava 2025, Sep 2024-Aug 2025) | S21 |
| Whole gym visit | "the average gym visit lasts 1 hour and 9 minutes" (PureGym UK) | S24 |
| Time per day by activity (participants) | weightlifting 0.9 h, cardio equipment 0.7 h; all sports 1.5 h (ATUS 2003-06) | S22 |
| Single-user Strong log (583 workouts, Oct 2015-Sep 2018) | 3.75 exercises/workout (median 3), 17.0 sets/workout (median 16), 4.53 sets per exercise bout (median 4); barbell squat 8.3, incline bench 6.6, chin-up 6.3 sets/bout vs DB lateral raise 2.6, lat pulldown 2.7, BB curl 2.8 **[derived from S26]** - illustrates warm-up-set overhead on barbell lifts; n = 1 lifter, not representative | S26 |

---

## 5. Derivations

### 5.1 Recommended popularity weights (Table 6.1 `Cons %`) **[derived]**
1. Row universe: 92 strength exercises/families covering all canonical strength stations (variants that share a station were summed, e.g. leg press = Fitbod "Leg Press" + "Machine Leg Press"; lateral raise = "Dumbbell Lateral Raise" + "Dumbbell Shoulder Raise").
2. Fitbod share f(e) = Fitbod sets(e) / 330,937,675 (sum over the 92 rows).
3. StrengthLog share s(e) = published overall share for the 25 listed exercises; for the other 67 rows, s(e) = min(0.99 %, 1.27 x f(e)), where 1.27 is the median s/f ratio on the 25 overlapping rows and 0.99 % respects the fact that anything outside the top 25 is < 1.0 %. s is then renormalised to 100 % over the rows.
4. Consensus share = 0.5 x s(e) + 0.5 x f(e), renormalised (lambda = 0.5 = equal weight to a strength-focused and a general population; set lambda higher for a barbell/performance gym, lower for a beginner/budget gym).
5. Men/women vectors: tilt t(e) = SL_women/SL_men where both are published (19 exercises); otherwise t(e) = exp(0.905 + 0.504 ln(F/M odds in Strength Level)) - an OLS fit on those 19 exercises (R^2 = 0.72); t = 1 where no sex data exist. With p_f = 0.35 (Section 2.1): men = c / ((1-p_f) + p_f t), women = t x men, each renormalised to 100 %.
Sensitivity: bench press ranges from 2.6 % (Fitbod population) to 8.8 % (StrengthLog population, renormalised); DB curl 1.6 % to 3.6 %; leg press 2.0-2.3 %; lat pulldown 2.9-3.5 % (the stable "universal" machines).

### 5.2 Station hold time per exercise bout **[derived]**
Bout = setup/teardown + warm-up sets x warm-up cycle + working sets x set duration + (working sets - 1) x rest. Parameters:

| Class | Examples | Setup min | Warm-up sets x cycle | Working sets | Set min | Rest min | Bout min |
|---|---|---|---|---|---|---|---|
| A heavy barbell | squat, bench, deadlift, OHP, BB row, RDL, incline/decline/close-grip bench, front squat, Olympic lifts | 2.0 | 2 x 1.5 | 3 | 0.6 | 2.5 | **11.8** |
| A2 loaded barbell accessory | barbell/DB hip thrust, barbell lunge | 2.0 | 1 x 1.5 | 3 | 0.6 | 2.0 | **9.3** |
| B machine/plate-loaded compound | leg press, hack squat, chest/shoulder press, pulldown, rows, Smith | 0.7 | 1 x 1.2 | 3 | 0.7 | 2.0 | **8.0** |
| D dumbbell/KB compound | DB bench/incline/shoulder press, DB row, lunges, BSS, goblet squat, swings | 0.5 | 1 x 1.0 | 3 | 0.7 | 1.75 | **7.1** |
| C isolation (machine, cable, DB) | curls, extensions, raises, flyes, leg ext/curl, abduction, calf | 0.3 | 0 | 3 | 0.6 | 1.25 | **4.6** |
| BW body-weight | pull-up, chin-up, dip, hanging raise, push-up | 0.2 | 0 | 3 | 0.5 | 1.5 | **4.7** |
| F functional | sled, ropes, wall ball, box jump, TRX | 0.5 | 0 | 3 | 0.75 | 1.0 | **4.8** |

Sources for each parameter: working sets 3 (ACSM 2026 >=2 with plateau 2-3; Boostcamp ~2.8 planned); rest A 2.5 min (ACSM 2009 ">=2-3 min" core; Grgic ">2 min" trained; Ibbott self-selected 3.5-4.6 min), B 2.0 min, D 1.75 min, C 1.25 min (ACSM 2009 "1-2 min" assistance; NSCA 30-90 s; Singer plateau ~90 s; Silva: most timed rests <=60 s); set duration 0.6 min = 8-12 reps x 3-4 s (ACSM 1-2 s CON + 1-2 s ECC) + unrack/re-rack; warm-up sets and setup (plate loading/unloading) are **[estimates]** informed by the single-user Strong log (barbell lifts logged with 6-8 sets vs ~3 for isolation). Ranges for sensitivity: A 9-18 min (rest 2-4 min, 1-3 warm-ups), B 6-10, D 5-9, C 3.5-6.5.
**Calibration check:** consensus-weighted mean bout = **7.1 min**; 6 exercises x 7.1 = 42.5 min of station holding inside a 58-min median Boostcamp session, leaving ~15 min for warm-up, walking between stations, waiting and breaks (all-in 9.7 min per exercise). Consistent with Strava's ~51-min average weight-training activity.

### 5.3 Station-time weights (Table 6.1 `ST %`) **[derived]**
ST share(e) proportional to consensus share of sets / 3 working sets x bout minutes(e). Heavy barbell exercises carry ~2.6x the station-time per set of isolation work, which is why racks/platforms/bench stations take 35 % of strength station-time but only 21 % of sets (Table 7.1).

### 5.4 Combining strength and cardio **[derived]**
Floor station-time share = 0.60 x strength ST% + 0.40 x cardio share, where cardio share(m) is proportional to SFIA occasions(m) x bout minutes(m) (treadmill 27, bike 25, elliptical 25, stair 18, rower 15, spin 45 - bout minutes are **[estimates]** anchored on ACSM's >=20-30 min/day, Girginer & Sahin's ~21-22 min/machine and the 20-min console default). Result: Table 6.3.

### 5.5 Cardio bout minutes **[estimate]**
| Modality | Typical | Low-High | Rationale |
|---|---|---|---|
| treadmill | 27 | 20-45 | ACSM >=30 min moderate; Girginer 0.37 h (22 min) per customer; walking sessions are longer |
| upright/recumbent bike | 25 | 20-40 | Girginer bike fixed 20 min; ACSM 20-30 min |
| elliptical | 25 | 20-40 | Girginer glider 0.35 h (21 min) |
| stair climber | 18 | 10-30 | vigorous modality -> ACSM >=20 min vigorous; usually shorter |
| rower | 15 | 8-25 | vigorous; often used as warm-up/intervals |
| indoor cycle (group class) | 45 | 30-60 | class format |
| air bike / SkiErg | 10-12 | 5-20 | interval use |
| recumbent stepper | 25 | 15-40 | rehab/older adults |
| curved treadmill | 15 | 8-25 | sprint/interval use |


---

## 6. Ranked exercise list with per-source values and recommended weights

Strength rows are ranked by the recommended consensus share of strength sets (Section 5.1). Cardio modalities are ranked separately by SFIA occasions (Table 6.2) and merged with strength by station-time in Table 6.3.

### Table 6.1 - Ranked strength-exercise list (92 rows)

Columns: SL = StrengthLog share of logged sets 2025 (all / men / women; '-' = outside that top-25, i.e. below 1.0 % all, 1.1 % men, 1.0 % women); FB = Fitbod 'sets logged'; LV = Strength Level community lifts and female share of qualifying results; BC = Boostcamp workout logs containing the exercise (thousands); Cons/Men/Women = recommended share of strength sets (%), derived (Section 5); Bout = modelled minutes the station is held per exercise bout; ST% = share of strength station-time.

| # | Exercise (id) | Primary equipment | Alternates | SL all/M/W % | FB sets | LV lifts (F share) | BC k | Cons % | Men % | Women % | W/M | Class | Bout min | ST % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Barbell bench press (flat) (`bench_press_bb`) | `bench_press_station` | power_rack+flat_bench, smith_machine | 9.7/10.7/8.2 | 8,702,771 | 48,718,584 (9.3% F) | 172 | 5.74 | 6.17 | 4.90 | 0.77 | A | 11.8 | 9.56 |
| 2 | Barbell back squat (`back_squat_bb`) | `power_rack` | half_rack, smith_machine | 7.0/6.7/7.7 | 6,036,005 | 24,988,444 (14.6% F) | 150 | 4.10 | 3.85 | 4.58 | 1.15 | A | 11.8 | 6.84 |
| 3 | Lat pulldown (`lat_pulldown`) | `lat_pulldown` | lat_pulldown_row_combo, cable_column, functional_trainer, plate_loaded_high_row | 3.8/3.6/4.1 | 9,684,781 | 2,011,718 (17.7% F) | 140 | 3.19 | 3.01 | 3.55 | 1.14 | B | 8.0 | 3.61 |
| 4 | Barbell deadlift (conventional) (`deadlift_bb`) | `lifting_platform` | power_rack (floor) | 5.0/4.8/5.4 | 5,108,578 | 22,978,599 (15.6% F) | 99 | 3.05 | 2.89 | 3.36 | 1.12 | A | 11.8 | 5.09 |
| 5 | Dumbbell biceps curl (`curl_db`) | `dumbbell_set_light` | cable_column, biceps_curl_machine | 1.7/1.8/1.6 | 11,988,008 | 3,634,702 (11.8% F) | - | 2.59 | 2.66 | 2.45 | 0.89 | C | 4.6 | 1.68 |
| 6 | Dumbbell lateral raise (`lateral_raise_db`) | `dumbbell_set_light` | cable_column, functional_trainer | 2.7/2.8/2.6 | 6,597,969 | 1,211,431 (10.5% F) | 153 | 2.23 | 2.26 | 2.17 | 0.93 | C | 4.6 | 1.45 |
| 7 | Leg press (45-degree / sled) (`leg_press`) | `leg_press` | hack_squat, leg_press (selectorized) | 2.2/1.9/2.7 | 7,659,173 | 2,661,088 (21.8% F) | - | 2.16 | 1.86 | 2.74 | 1.42 | B | 8.0 | 2.44 |
| 8 | Barbell overhead press (`ohp_bb`) | `power_rack` | half_rack, smith_machine | 3.4/3.5/3.0 | 3,789,263 | 5,644,500 (11.2% F) | - | 2.12 | 2.21 | 1.96 | 0.86 | A | 11.8 | 3.54 |
| 9 | One-arm dumbbell row (`row_db`) | `dumbbell_set_full+flat_bench` | seated_row, plate_loaded_row | 1.3/1.2/1.5 | 10,105,842 | 927,185 (16.9% F) | - | 2.12 | 1.93 | 2.49 | 1.25 | D | 7.1 | 2.13 |
| 10 | Leg extension (machine) (`leg_extension`) | `leg_extension` | leg_ext_curl_combo | 2.5/2.4/2.7 | 6,456,032 | 1,152,891 (19.9% F) | 147 | 2.12 | 2.00 | 2.33 | 1.12 | C | 4.6 | 1.38 |
| 11 | Hammer curl (`hammer_curl`) | `dumbbell_set_light` | cable_column | 1.1/1.2/- | 10,391,123 | 752,185 (8.2% F) | - | 2.07 | 2.26 | 1.71 | 0.73 | C | 4.6 | 1.35 |
| 12 | Barbell bent-over row (`row_bb`) | `lifting_platform` | power_rack (floor), smith_machine, t_bar_row | 3.2/3.2/2.9 | 3,420,702 | 2,162,181 (11.8% F) | - | 1.98 | 2.02 | 1.89 | 0.91 | A | 11.8 | 3.29 |
| 13 | Flat dumbbell bench press (`bench_press_db`) | `dumbbell_set_full+flat_bench` | bench_press_station, chest_press | 1.0/1.1/- | 10,009,222 | 4,734,253 (8.8% F) | - | 1.97 | 2.12 | 1.67 | 0.76 | D | 7.1 | 1.98 |
| 14 | Barbell curl (`curl_bb`) | `fixed_barbell_set` | cable_column, biceps_curl_machine | 2.1/2.4/1.4 | 6,392,670 | 2,565,545 (8.8% F) | - | 1.92 | 2.23 | 1.34 | 0.58 | C | 4.6 | 1.25 |
| 15 | Seated cable row (close grip) (`seated_cable_row`) | `seated_row` | lat_pulldown_row_combo, cable_column, plate_loaded_row | 1.6/1.5/1.6 | 7,243,267 | 711,455 (15.8% F) | - | 1.82 | 1.76 | 1.95 | 1.07 | B | 8.0 | 2.06 |
| 16 | Dumbbell shoulder press (`shoulder_press_db`) | `dumbbell_set_full+adjustable_bench` | shoulder_press, plate_loaded_shoulder_press | 1.3/1.2/1.6 | 7,993,508 | 2,106,645 (13.0% F) | - | 1.80 | 1.59 | 2.20 | 1.33 | D | 7.1 | 1.81 |
| 17 | Overhead/seated dumbbell triceps extension (`oh_triceps_db`) | `dumbbell_set_light+adjustable_bench` | cable_column | -/-/- | 8,386,126 | - | - | 1.72 | 1.70 | 1.76 | 1.00 | C | 4.6 | 1.12 |
| 18 | Triceps pushdown (rope) (`pushdown_rope`) | `cable_column` | cable_crossover, functional_trainer | 1.5/1.5/1.3 | 6,634,413 | - | - | 1.69 | 1.75 | 1.57 | 0.87 | C | 4.6 | 1.10 |
| 19 | Incline dumbbell press (`incline_press_db`) | `dumbbell_set_full+adjustable_bench` | incline_bench_station, smith_machine | 1.9/2.1/1.3 | 5,092,125 | 2,367,587 (5.5% F) | - | 1.64 | 1.86 | 1.20 | 0.62 | D | 7.1 | 1.64 |
| 20 | Dumbbell fly (`fly_db`) | `dumbbell_set_full+flat_bench` | pec_fly_rear_delt, cable_crossover | -/-/- | 7,705,017 | 345,131 (9.8% F) | - | 1.61 | 1.71 | 1.43 | 0.81 | C | 4.6 | 1.05 |
| 21 | Dumbbell skullcrusher (`skullcrusher_db`) | `dumbbell_set_light+flat_bench` | fixed_barbell_set | -/-/- | 6,955,739 | - | - | 1.50 | 1.48 | 1.54 | 1.00 | C | 4.6 | 0.98 |
| 22 | Triceps pushdown (bar) (`pushdown_bar`) | `cable_column` | cable_crossover, functional_trainer, triceps_machine | 2.0/2.1/1.5 | 3,797,656 | 805,104 (10.0% F) | - | 1.49 | 1.63 | 1.21 | 0.71 | C | 4.6 | 0.97 |
| 23 | Push-up (`push_up`) | `stretch_area` | accessory_pack | -/-/- | 6,723,750 | 2,928,475 (11.3% F) | - | 1.47 | 1.52 | 1.37 | 0.88 | BW | 4.7 | 0.97 |
| 24 | Dumbbell front raise (`front_raise_db`) | `dumbbell_set_light` | cable_column | -/-/- | 6,658,201 | - | - | 1.46 | 1.44 | 1.49 | 1.00 | C | 4.6 | 0.95 |
| 25 | Pull-up (`pull_up`) | `dip_chin_station` | rig_bay, power_rack, assisted_pullup_dip | 1.7/2.0/- | 4,343,343 | 4,852,758 (9.5% F) | - | 1.43 | 1.52 | 1.25 | 0.79 | BW | 4.7 | 0.95 |
| 26 | Dumbbell rear-delt raise (`rear_delt_raise_db`) | `dumbbell_set_light` | pec_fly_rear_delt, cable_crossover | -/-/- | 5,836,111 | - | - | 1.33 | 1.32 | 1.36 | 1.00 | C | 4.6 | 0.87 |
| 27 | Dumbbell lunge (static/walking) (`lunge_db`) | `dumbbell_set_full` | turf_lane, smith_machine | -/-/- | 5,206,073 | - | - | 1.24 | 1.22 | 1.27 | 1.00 | D | 7.1 | 1.24 |
| 28 | Seated leg curl (`seated_leg_curl`) | `leg_curl` | leg_ext_curl_combo | 1.2/1.2/1.3 | 4,254,937 | 457,839 (21.9% F) | - | 1.19 | 1.14 | 1.28 | 1.08 | C | 4.6 | 0.77 |
| 29 | Shrug (DB/BB/Smith/machine) (`shrug`) | `dumbbell_set_full` | fixed_barbell_set, smith_machine, power_rack | -/-/- | 4,887,006 | 372,602 (4.2% F) | - | 1.19 | 1.42 | 0.75 | 0.51 | C | 4.6 | 0.77 |
| 30 | EZ-bar curl (`ez_curl`) | `fixed_barbell_set` | cable_column | -/-/- | 4,849,955 | 457,832 (5.3% F) | - | 1.18 | 1.37 | 0.82 | 0.58 | C | 4.6 | 0.77 |
| 31 | Lat pulldown variants (wide/V-bar/reverse/single-arm) (`lat_pulldown_variants`) | `lat_pulldown` | lat_pulldown_row_combo, cable_column | -/-/- | 4,771,605 | - | - | 1.17 | 1.16 | 1.20 | 1.00 | B | 8.0 | 1.32 |
| 32 | Upright row (BB/DB/cable) (`upright_row`) | `fixed_barbell_set` | dumbbell_set_light, cable_column | -/-/- | 4,595,946 | - | - | 1.15 | 1.13 | 1.17 | 1.00 | C | 4.6 | 0.74 |
| 33 | Hanging / captain's-chair knee & leg raise (`hanging_raise`) | `dip_chin_station` | rig_bay | -/-/- | 4,518,757 | - | - | 1.13 | 1.12 | 1.16 | 1.00 | BW | 4.7 | 0.75 |
| 34 | Romanian deadlift (barbell) (`rdl_bb`) | `lifting_platform` | power_rack, dumbbell_set_full | 1.3/1.1/1.7 | 3,386,245 | 1,151,417 (26.5% F) | - | 1.10 | 0.92 | 1.47 | 1.54 | A | 11.8 | 1.84 |
| 35 | Close-grip bench press (`close_grip_bench`) | `bench_press_station` | power_rack+flat_bench, smith_machine | -/1.1/- | 4,046,080 | - | - | 1.06 | 1.05 | 1.09 | 1.00 | A | 11.8 | 1.77 |
| 36 | Plate-loaded chest press (flat/incline/decline) (`pl_chest_press`) | `plate_loaded_chest_press` | chest_press | -/-/- | 4,029,485 | - | - | 1.06 | 1.05 | 1.08 | 1.00 | B | 8.0 | 1.20 |
| 37 | Back extension (45-degree / GHD bench) (`back_extension`) | `hyperextension` | back_extension_machine, ghd | -/-/- | 3,999,754 | - | - | 1.05 | 1.04 | 1.08 | 1.00 | C | 4.6 | 0.69 |
| 38 | Incline barbell bench press (`incline_bench_bb`) | `incline_bench_station` | power_rack+adjustable_bench, smith_machine | -/-/- | 3,953,814 | 2,165,292 (4.3% F) | - | 1.05 | 1.25 | 0.67 | 0.52 | A | 11.8 | 1.75 |
| 39 | Machine fly (pec deck) (`pec_deck`) | `pec_fly_rear_delt` | cable_crossover | -/-/- | 3,744,823 | 487,945 (7.7% F) | - | 1.02 | 1.12 | 0.82 | 0.71 | C | 4.6 | 0.66 |
| 40 | Lying leg curl (`lying_leg_curl`) | `leg_curl` | leg_ext_curl_combo | 1.3/1.3/1.2 | 2,755,579 | 358,631 (18.5% F) | - | 1.01 | 1.02 | 0.98 | 0.92 | C | 4.6 | 0.66 |
| 41 | Step-up (BW/DB/BB) (`step_up`) | `plyo_box_set` | flat_bench, dumbbell_set_full | -/-/- | 3,596,191 | - | - | 0.99 | 0.98 | 1.02 | 1.00 | D | 7.1 | 1.00 |
| 42 | Standing cable chest fly (`cable_fly`) | `cable_crossover` | functional_trainer, pec_fly_rear_delt | 1.1/1.2/- | 3,148,104 | 236,590 (7.2% F) | - | 0.98 | 1.09 | 0.77 | 0.68 | C | 4.6 | 0.64 |
| 43 | Hip thrust (barbell/dumbbell, loaded) (`hip_thrust`) | `hip_thrust_bench` | hip_thrust_machine, smith_machine, glute_kickback | -/-/2.0 | 3,370,490 | 1,221,785 (58.6% F) | - | 0.96 | 0.56 | 1.72 | 2.94 | A2 | 9.3 | 1.26 |
| 44 | Parallel-bar dip (`dips`) | `dip_chin_station` | assisted_pullup_dip, triceps_machine | -/-/- | 3,169,684 | 2,162,628 (5.4% F) | - | 0.93 | 1.08 | 0.65 | 0.58 | BW | 4.7 | 0.62 |
| 45 | Skullcrusher (barbell/EZ) (`skullcrusher_bb`) | `fixed_barbell_set+flat_bench` | dumbbell_set_light | -/-/- | 3,008,701 | - | - | 0.91 | 0.90 | 0.93 | 1.00 | C | 4.6 | 0.59 |
| 46 | Machine triceps extension / machine dip (`triceps_machine`) | `triceps_machine` | assisted_pullup_dip, cable_column | -/-/- | 2,822,532 | - | - | 0.88 | 0.87 | 0.90 | 1.00 | C | 4.6 | 0.57 |
| 47 | Ab crunch machine (`ab_crunch_machine`) | `ab_crunch_machine` | cable_column | -/-/- | 2,812,905 | - | - | 0.88 | 0.87 | 0.90 | 1.00 | C | 4.6 | 0.57 |
| 48 | Machine biceps curl (incl. machine preacher) (`biceps_machine`) | `biceps_curl_machine` | preacher_bench, cable_column | -/-/- | 2,773,341 | - | - | 0.87 | 0.86 | 0.89 | 1.00 | C | 4.6 | 0.57 |
| 49 | Olympic lifts & derivatives (cleans, snatches, jerks, push press) (`olympic_lifts`) | `lifting_platform` | power_rack | -/-/- | 2,739,969 | - | - | 0.86 | 0.85 | 0.89 | 1.00 | A | 11.8 | 1.44 |
| 50 | Cable lateral raise (`cable_lateral_raise`) | `cable_column` | functional_trainer, cable_crossover | -/-/- | 2,624,028 | - | 85 | 0.85 | 0.84 | 0.87 | 1.00 | C | 4.6 | 0.55 |
| 51 | Cable face pull (`face_pull`) | `cable_column` | cable_crossover, functional_trainer | 1.0/-/1.0 | 2,496,755 | 181,223 (20.7% F) | - | 0.83 | 0.76 | 0.98 | 1.25 | C | 4.6 | 0.54 |
| 52 | Seated back extension (machine) (`back_ext_machine`) | `back_extension_machine` | hyperextension | -/-/- | 2,359,595 | - | - | 0.77 | 0.76 | 0.79 | 1.00 | C | 4.6 | 0.50 |
| 53 | Cable biceps curl (`cable_curl`) | `cable_column` | functional_trainer | -/-/- | 2,297,208 | - | - | 0.75 | 0.74 | 0.77 | 1.00 | C | 4.6 | 0.49 |
| 54 | Shoulder press (machine, incl. plate-loaded) (`machine_shoulder_press`) | `shoulder_press` | plate_loaded_shoulder_press | -/-/- | 2,231,692 | 488,940 (10.3% F) | - | 0.73 | 0.76 | 0.66 | 0.83 | B | 8.0 | 0.82 |
| 55 | Chin-up (`chin_up`) | `dip_chin_station` | rig_bay, power_rack, assisted_pullup_dip | -/-/- | 2,164,015 | 1,225,888 (10.8% F) | - | 0.71 | 0.73 | 0.65 | 0.85 | BW | 4.7 | 0.47 |
| 56 | Seated row machine (selectorized) (`machine_row`) | `seated_row` | plate_loaded_row | -/-/- | 2,150,001 | - | - | 0.70 | 0.69 | 0.72 | 1.00 | B | 8.0 | 0.79 |
| 57 | Chest press (selectorized) (`machine_chest_press`) | `chest_press` | plate_loaded_chest_press | -/-/- | 2,083,700 | 822,882 (12.3% F) | - | 0.68 | 0.69 | 0.66 | 0.92 | B | 8.0 | 0.77 |
| 58 | Front squat (`front_squat`) | `power_rack` | half_rack | -/-/- | 2,014,709 | 1,597,959 (21.5% F) | - | 0.66 | 0.59 | 0.79 | 1.29 | A | 11.8 | 1.10 |
| 59 | Bulgarian split squat (`bss`) | `dumbbell_set_full+flat_bench` | smith_machine, power_rack | -/-/1.4 | 1,969,153 | 482,453 (27.4% F) | - | 0.64 | 0.54 | 0.84 | 1.51 | D | 7.1 | 0.64 |
| 60 | Smith machine bench (flat+incline) (`smith_bench`) | `smith_machine` | bench_press_station | -/-/- | 1,963,489 | 341,390 (5.6% F) | - | 0.64 | 0.74 | 0.45 | 0.59 | B | 8.0 | 0.72 |
| 61 | Kettlebell swing (`kb_swing`) | `kettlebell_set` | dumbbell_set_full | -/-/- | 1,887,482 | - | - | 0.61 | 0.61 | 0.63 | 1.00 | D | 7.1 | 0.62 |
| 62 | Preacher curl (bench) (`preacher_curl`) | `preacher_bench` | biceps_curl_machine | -/-/- | 1,877,663 | - | - | 0.61 | 0.60 | 0.63 | 1.00 | C | 4.6 | 0.40 |
| 63 | Assisted pull-up/chin-up/dip (machine) (`assisted_pullup_dip`) | `assisted_pullup_dip` | lat_pulldown | -/-/- | 1,876,529 | - | - | 0.61 | 0.60 | 0.63 | 1.00 | B | 8.0 | 0.69 |
| 64 | Hip abduction (machine) (`hip_abduction`) | `hip_abductor_adductor` | cable_column | -/-/1.0 | 1,747,865 | 203,182 (52.7% F) | - | 0.57 | 0.36 | 0.97 | 2.61 | C | 4.6 | 0.37 |
| 65 | Glute kickback machine (`glute_kickback_machine`) | `glute_kickback` | cable_column, hip_thrust_machine | -/-/- | 1,727,762 | - | - | 0.56 | 0.56 | 0.58 | 1.00 | C | 4.6 | 0.37 |
| 66 | Cable crunch (`cable_crunch`) | `cable_column` | ab_crunch_machine | -/-/- | 1,707,669 | - | - | 0.56 | 0.55 | 0.57 | 1.00 | C | 4.6 | 0.36 |
| 67 | Plate-loaded iso-lateral row (`pl_iso_row`) | `plate_loaded_row` | seated_row | -/-/- | 1,627,758 | - | - | 0.53 | 0.52 | 0.54 | 1.00 | B | 8.0 | 0.60 |
| 68 | Plate-loaded high row (`pl_high_row`) | `plate_loaded_high_row` | lat_pulldown | -/-/- | 1,580,411 | - | - | 0.52 | 0.51 | 0.53 | 1.00 | B | 8.0 | 0.58 |
| 69 | Cable glute kickback / hip extension (`cable_kickback`) | `cable_column` | glute_kickback | -/-/- | 1,569,567 | - | - | 0.51 | 0.51 | 0.52 | 1.00 | C | 4.6 | 0.33 |
| 70 | Seated calf raise (machine) (`seated_calf`) | `calf_raise` | leg_press | -/-/- | 1,468,648 | 253,479 (12.3% F) | - | 0.48 | 0.49 | 0.46 | 0.92 | C | 4.6 | 0.31 |
| 71 | Hip adduction (machine) (`hip_adduction`) | `hip_abductor_adductor` | cable_column | -/-/- | 1,417,813 | 344,261 (40.1% F) | - | 0.46 | 0.34 | 0.70 | 2.02 | C | 4.6 | 0.30 |
| 72 | Goblet squat (DB/KB) (`goblet_squat`) | `dumbbell_set_full` | kettlebell_set | -/-/- | 1,372,496 | 385,610 (32.9% F) | - | 0.45 | 0.35 | 0.63 | 1.73 | D | 7.1 | 0.45 |
| 73 | Calf press on leg press (`leg_press_calf`) | `leg_press` | calf_raise | -/-/- | 1,338,090 | - | - | 0.44 | 0.43 | 0.45 | 1.00 | C | 4.6 | 0.28 |
| 74 | Stiff-legged deadlift (BB/DB) (`sldl`) | `dumbbell_set_full` | lifting_platform | -/-/1.1 | 1,321,873 | - | - | 0.43 | 0.43 | 0.44 | 1.00 | D | 7.1 | 0.43 |
| 75 | Straight-arm pulldown (`straight_arm_pulldown`) | `cable_column` | lat_pulldown, cable_crossover | -/-/- | 1,318,920 | - | - | 0.43 | 0.42 | 0.44 | 1.00 | C | 4.6 | 0.28 |
| 76 | Suspension trainer (TRX) exercises (`suspension`) | `suspension_trainer_station` | rig_bay | -/-/- | 1,249,093 | - | - | 0.41 | 0.40 | 0.42 | 1.00 | F | 4.8 | 0.27 |
| 77 | Decline barbell bench press (`decline_bench_bb`) | `decline_bench_station` | smith_machine | -/-/- | 1,208,914 | - | - | 0.39 | 0.39 | 0.40 | 1.00 | A | 11.8 | 0.66 |
| 78 | Cable pull-through (`cable_pull_through`) | `cable_column` | hip_thrust_bench | -/-/- | 1,132,962 | - | - | 0.37 | 0.36 | 0.38 | 1.00 | C | 4.6 | 0.24 |
| 79 | Hack squat (machine) (`hack_squat`) | `hack_squat` | leg_press, belt_squat | -/-/- | 1,085,651 | 564,866 (12.3% F) | - | 0.35 | 0.36 | 0.34 | 0.92 | B | 8.0 | 0.40 |
| 80 | Barbell lunge (`lunge_bb`) | `power_rack` | smith_machine | -/-/- | 982,507 | - | - | 0.32 | 0.32 | 0.33 | 1.00 | A2 | 9.3 | 0.42 |
| 81 | Smith machine squat (`smith_squat`) | `smith_machine` | power_rack, hack_squat | -/-/- | 973,303 | 276,386 (18.4% F) | - | 0.32 | 0.30 | 0.36 | 1.17 | B | 8.0 | 0.36 |
| 82 | Overhead cable triceps extension (rope) (`oh_triceps_cable`) | `cable_column` | functional_trainer | -/-/- | 934,398 | - | - | 0.30 | 0.30 | 0.31 | 1.00 | C | 4.6 | 0.20 |
| 83 | Standing calf raise (machine) (`standing_calf`) | `calf_raise` | smith_machine, leg_press | -/-/- | 903,432 | 350,435 (13.3% F) | - | 0.29 | 0.29 | 0.29 | 0.96 | C | 4.6 | 0.19 |
| 84 | T-bar row (`t_bar_row`) | `t_bar_row` | landmine, plate_loaded_row | -/-/- | 879,374 | 368,631 (7.4% F) | - | 0.29 | 0.32 | 0.23 | 0.69 | B | 8.0 | 0.32 |
| 85 | Landmine press/row (`landmine`) | `landmine` | t_bar_row | -/-/- | 872,676 | - | - | 0.28 | 0.28 | 0.29 | 1.00 | D | 7.1 | 0.29 |
| 86 | Machine reverse fly (`rear_delt_machine`) | `pec_fly_rear_delt` | cable_crossover | -/-/- | 416,595 | - | - | 0.14 | 0.13 | 0.14 | 1.00 | C | 4.6 | 0.09 |
| 87 | Wall ball / med-ball slam (`wall_ball_slam`) | `wall_ball_station` | turf_lane | -/-/- | 408,382 | - | - | 0.13 | 0.13 | 0.14 | 1.00 | F | 4.8 | 0.09 |
| 88 | Box jump (`box_jump`) | `plyo_box_set` | turf_lane | -/-/- | 407,558 | - | - | 0.13 | 0.13 | 0.14 | 1.00 | F | 4.8 | 0.09 |
| 89 | Trap/hex-bar deadlift (`trap_bar_deadlift`) | `lifting_platform` | power_rack (floor) | -/-/- | 392,684 | 1,437,859 (13.9% F) | - | 0.13 | 0.13 | 0.13 | 0.98 | A | 11.8 | 0.21 |
| 90 | Glute-ham raise (`ghr`) | `ghd` | leg_curl | -/-/- | 255,369 | - | - | 0.08 | 0.08 | 0.09 | 1.00 | C | 4.6 | 0.05 |
| 91 | Sled push/drag/pull (`sled`) | `turf_lane+sled` | air_bike | -/-/- | 253,398 | - | - | 0.08 | 0.08 | 0.09 | 1.00 | F | 4.8 | 0.06 |
| 92 | Battle ropes (`battle_ropes`) | `battle_rope_station` | turf_lane | -/-/- | 233,117 | - | - | 0.08 | 0.07 | 0.08 | 1.00 | F | 4.8 | 0.05 |

### Table 6.2 - Cardio modalities (SFIA 2024 Topline, 2023 data, U.S. ages 6+)

Unified ST% assumes the recommended default 40 % of member station-time on cardio machines (Section 5.4).

| # | Modality | Equipment id | Participants (M) | Mean days/yr | Occasions (B) | Share of cardio occasions | Bout min (est.) | Share of cardio station-time | Unified ST % of all floor time |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Treadmill (walk/run) | `treadmill` | 54.8 | 65 | 3.565 | 40.8% | 27 | 43.6% | 17.4% |
| 2 | Stationary bike (upright + recumbent) | `upright_bike / recumbent_bike` | 32.6 | 68 | 2.228 | 25.5% | 25 | 25.2% | 10.1% |
| 3 | Elliptical / cross-trainer | `elliptical` | 27.1 | 62 | 1.672 | 19.1% | 25 | 18.9% | 7.6% |
| 4 | Rowing machine | `rower` | 12.8 | 42 | 0.539 | 6.2% | 15 | 3.7% | 1.5% |
| 5 | Stair-climbing machine | `stair_climber` | 12.6 | 42 | 0.530 | 6.1% | 18 | 4.3% | 1.7% |
| 6 | Group stationary cycling (spin) | `indoor_cycle` | 6.2 | 34 | 0.211 | 2.4% | 45 | 4.3% | 1.7% |
| - | Air bike, SkiErg, curved treadmill, recumbent stepper | `air_bike`, `ski_erg`, `curved_treadmill`, `recumbent_stepper` | not tracked by SFIA | - | - | no data (see Section 3.4 for nominal model weights) | 10-20 | - | - |

### Table 6.3 - Unified ranking by share of all floor station-time (strength 60 % / cardio 40 %)

| # | Exercise / modality | Equipment | % of all station-time |
|---|---|---|---|
| 1 | Treadmill (walk/run) | `treadmill` | 17.43 |
| 2 | Stationary bike (upright + recumbent) | `upright_bike / recumbent_bike` | 10.09 |
| 3 | Elliptical / cross-trainer | `elliptical` | 7.57 |
| 4 | Barbell bench press (flat) | `bench_press_station` | 5.74 |
| 5 | Barbell back squat | `power_rack` | 4.10 |
| 6 | Barbell deadlift (conventional) | `lifting_platform` | 3.05 |
| 7 | Lat pulldown | `lat_pulldown` | 2.17 |
| 8 | Barbell overhead press | `power_rack` | 2.12 |
| 9 | Barbell bent-over row | `lifting_platform` | 1.98 |
| 10 | Stair-climbing machine | `stair_climber` | 1.73 |
| 11 | Group stationary cycling (spin) | `indoor_cycle` | 1.72 |
| 12 | Leg press (45-degree / sled) | `leg_press` | 1.47 |
| 13 | Rowing machine | `rower` | 1.46 |
| 14 | One-arm dumbbell row | `dumbbell_set_full+flat_bench` | 1.28 |
| 15 | Seated cable row (close grip) | `seated_row` | 1.24 |
| 16 | Flat dumbbell bench press | `dumbbell_set_full+flat_bench` | 1.19 |
| 17 | Romanian deadlift (barbell) | `lifting_platform` | 1.10 |
| 18 | Dumbbell shoulder press | `dumbbell_set_full+adjustable_bench` | 1.08 |
| 19 | Close-grip bench press | `bench_press_station` | 1.06 |
| 20 | Incline barbell bench press | `incline_bench_station` | 1.05 |
| 21 | Dumbbell biceps curl | `dumbbell_set_light` | 1.01 |
| 22 | Incline dumbbell press | `dumbbell_set_full+adjustable_bench` | 0.98 |
| 23 | Dumbbell lateral raise | `dumbbell_set_light` | 0.87 |
| 24 | Olympic lifts & derivatives (cleans, snatches, jerks, push press) | `lifting_platform` | 0.87 |
| 25 | Leg extension (machine) | `leg_extension` | 0.82 |
| 26 | Hammer curl | `dumbbell_set_light` | 0.81 |
| 27 | Lat pulldown variants (wide/V-bar/reverse/single-arm) | `lat_pulldown` | 0.79 |
| 28 | Hip thrust (barbell/dumbbell, loaded) | `hip_thrust_bench` | 0.76 |
| 29 | Barbell curl | `fixed_barbell_set` | 0.75 |
| 30 | Dumbbell lunge (static/walking) | `dumbbell_set_full` | 0.75 |
| 31 | Plate-loaded chest press (flat/incline/decline) | `plate_loaded_chest_press` | 0.72 |
| 32 | Overhead/seated dumbbell triceps extension | `dumbbell_set_light+adjustable_bench` | 0.67 |
| 33 | Triceps pushdown (rope) | `cable_column` | 0.66 |
| 34 | Front squat | `power_rack` | 0.66 |
| 35 | Dumbbell fly | `dumbbell_set_full+flat_bench` | 0.63 |
| 36 | Step-up (BW/DB/BB) | `plyo_box_set` | 0.60 |
| 37 | Dumbbell skullcrusher | `dumbbell_set_light+flat_bench` | 0.59 |
| 38 | Push-up | `stretch_area` | 0.58 |
| 39 | Triceps pushdown (bar) | `cable_column` | 0.58 |
| 40 | Pull-up | `dip_chin_station` | 0.57 |


---

## 7. Equipment roll-up and substitution

### Table 7.2 - Observed substitutions (Fitbod 'Alternatives & Variations' swap counts)

| Exercise (id) | Most frequent swaps (count of times users swapped this exercise for the alternative) |
|---|---|
| Barbell bench press (flat) (`bench_press_bb`) | DB bench 68,375; DB incline 20,189; BB incline 17,620; Smith bench 16,772; Hammer Strength chest press 13,311; machine bench 13,132 |
| Barbell back squat (`back_squat_bb`) | leg press 34,788; leg extension 18,226; DB squat 13,630; hack squat 13,440; Smith squat 12,137; machine leg press 8,250 |
| Barbell deadlift (conventional) (`deadlift_bb`) | DB RDL 32,899; seated leg curl 26,190; RDL 19,710; lying leg curl 16,219; Smith SLDL 9,979; trap-bar DL 5,915 |
| Lat pulldown (`lat_pulldown`) | DB row 14,173; cable row 13,432; pull-up 10,462; V-bar pulldown 9,220; HS high row 8,920; machine row 6,714 |
| Leg extension (machine) (`leg_extension`) | single-leg extension 12,090; leg press 7,761; machine leg press 5,402; DB lunge 5,290; DB squat 4,772 |
| Seated cable row (close grip) (`seated_cable_row`) | machine row 26,660; lat pulldown 25,333; DB row 20,250; HS iso row 9,989; BB row 9,250 |
| Leg press (45-degree / sled) (`leg_press`) | machine leg press 47,411; leg extension 21,086; back squat 14,977; hack squat 12,052; DB squat 7,112 |
| Flat dumbbell bench press (`bench_press_db`) | BB bench 58,005; DB incline 27,162; machine bench 17,723; HS chest press 13,606; machine fly 10,844 |
| Seated leg curl (`seated_leg_curl`) | lying leg curl 25,876; DB RDL 10,001; leg extension 5,121; standing leg curl 4,178 |
| Lying leg curl (`lying_leg_curl`) | seated leg curl 60,378; DB RDL 14,636; standing leg curl 5,888 |
| Hip abduction (machine) (`hip_abduction`) | machine hip adductor 2,935; cable hip abduction 1,949; side leg raise 1,198 |
| Hack squat (machine) (`hack_squat`) | leg press 16,573; leg extension 12,076; back squat 8,103; machine leg press 6,674 |
| Dumbbell shoulder press (`shoulder_press_db`) | machine shoulder press 16,538; BB shoulder press 9,803; HS shoulder press 9,061 |
| Hip thrust (barbell/dumbbell, loaded) (`hip_thrust`) | glute kickback machine 21,501; cable hip extension 16,131; DB hip thrust 16,046; cable pull-through 12,904 (swaps away from barbell hip thrust) |
| Smith machine squat (`smith_squat`) | back squat 3,972; leg press 3,247; leg extension 2,852; hack squat 2,041 |
| Triceps pushdown (bar) (`pushdown_bar`) | rope extension 14,705; seated triceps press 3,170; DB skullcrusher 3,005; machine dip 2,797 |
| Cable lateral raise (`cable_lateral_raise`) | DB lateral raise 12,032; DB shoulder raise 10,512; machine lateral raise 4,688 |
| Pull-up (`pull_up`) | lat pulldown 53,295; assisted pull-up 26,373; DB row 24,393; cable row 22,046 |
| Romanian deadlift (barbell) (`rdl_bb`) | DB RDL 29,495; seated leg curl 14,601; lying leg curl 9,807; deadlift 9,351 |
| Barbell overhead press (`ohp_bb`) | DB shoulder press 35,434; seated BB press 8,700; machine shoulder press 7,602; HS shoulder press 5,942 |
| Machine fly (pec deck) (`pec_deck`) | cable crossover fly 10,820; DB fly 9,378; machine bench 5,348 |
| Calf press on leg press (`leg_press_calf`) | seated machine calf 6,890; standing machine calf 3,753; standing DB calf 2,321 |
| Dumbbell biceps curl (`curl_db`) | hammer curl 16,105; cable curl 12,098; BB curl 11,463; EZ curl 10,969; machine curl 10,025 |
| Shoulder press (machine, incl. plate-loaded) (`machine_shoulder_press`) | DB shoulder press 5,538; HS shoulder press 4,003; machine lateral raise 1,581 |
| Seated row machine (selectorized) (`machine_row`) | cable row 28,277; HS iso row 9,767; lat pulldown 8,501; DB row 7,471 |
| Parallel-bar dip (`dips`) | bench dip 35,797; rope extension 31,732; assisted dip 30,420; machine dip 28,609 |
| Ab crunch machine (`ab_crunch_machine`) | crunch 3,986; cable crunch 3,588; vertical knee raise 2,205; plank 2,083 |
| Back extension (45-degree / GHD bench) (`back_extension`) | seated back extension (machine) 40,578; superman 17,102; incline back extension 12,625 |
| Glute kickback machine (`glute_kickback_machine`) | cable hip extension 20,296; BB hip thrust 14,659; hip thrust 9,732; cable pull-through 9,406 |
| T-bar row (`t_bar_row`) | cable row 6,191; DB row 4,419; machine row 4,137; lat pulldown 4,130; HS iso row 3,656 |
| Bulgarian split squat (`bss`) | DB Bulgarian split squat 9,931; leg extension 5,254; DB lunge 3,762; leg press 3,695 |
| Standing cable chest fly (`cable_fly`) | machine fly 30,758; DB fly 15,448; DB bench 7,221; HS chest press 6,336 |
| Plate-loaded chest press (flat/incline/decline) (`pl_chest_press`) | HS incline press 9,273; machine bench 7,690; DB bench 5,322; machine fly 5,109 (from HS chest press page) |
| Cable face pull (`face_pull`) | cable lateral raise 3,740; DB front raise 3,433; DB rear-delt raise 3,342 |
| Smith machine bench (flat+incline) (`smith_bench`) | BB bench 11,620; DB bench 8,945; DB fly 4,362; machine bench 4,196 |
| Dumbbell lateral raise (`lateral_raise_db`) | cable lateral raise 4,020 + 6,373; machine lateral raise 1,667 + 2,457 (DB lateral raise + DB shoulder raise pages) |

### Table 7.1 - Strength demand rolled up to the primary station

| Primary station (composite = dumbbells used at a bench) | Share of strength sets % | Share of strength station-time % |
|---|---|---|
| `power_rack` | 7.20 | 11.90 |
| `lifting_platform` | 7.12 | 11.88 |
| `bench_press_station` | 6.80 | 11.34 |
| `dumbbell_set_light` | 9.67 | 6.29 |
| `dumbbell_set_full+flat_bench` | 6.34 | 5.80 |
| `cable_column` | 7.77 | 5.05 |
| `lat_pulldown` | 4.37 | 4.94 |
| `dumbbell_set_full+adjustable_bench` | 3.44 | 3.45 |
| `dumbbell_set_full` | 3.31 | 2.90 |
| `seated_row` | 2.52 | 2.85 |
| `dip_chin_station` | 4.20 | 2.79 |
| `fixed_barbell_set` | 4.25 | 2.76 |
| `leg_press` | 2.60 | 2.73 |
| `incline_bench_station` | 1.05 | 1.75 |
| `leg_curl` | 2.20 | 1.43 |
| `leg_extension` | 2.11 | 1.37 |
| `hip_thrust_bench` | 0.96 | 1.26 |
| `plate_loaded_chest_press` | 1.06 | 1.20 |
| `dumbbell_set_light+adjustable_bench` | 1.72 | 1.12 |
| `plyo_box_set` | 1.13 | 1.09 |
| `smith_machine` | 0.96 | 1.08 |
| `dumbbell_set_light+flat_bench` | 1.50 | 0.98 |
| `stretch_area` | 1.47 | 0.97 |
| `shoulder_press` | 0.73 | 0.82 |
| `chest_press` | 0.68 | 0.77 |
| `pec_fly_rear_delt` | 1.15 | 0.75 |
| `assisted_pullup_dip` | 0.61 | 0.69 |
| `hyperextension` | 1.06 | 0.69 |
| `hip_abductor_adductor` | 1.03 | 0.67 |
| `decline_bench_station` | 0.39 | 0.66 |
| `cable_crossover` | 0.98 | 0.64 |
| `kettlebell_set` | 0.62 | 0.62 |
| `plate_loaded_row` | 0.53 | 0.60 |
| `fixed_barbell_set+flat_bench` | 0.91 | 0.59 |
| `plate_loaded_high_row` | 0.52 | 0.58 |
| `triceps_machine` | 0.88 | 0.57 |
| `ab_crunch_machine` | 0.88 | 0.57 |
| `biceps_curl_machine` | 0.87 | 0.57 |
| `calf_raise` | 0.77 | 0.50 |
| `back_extension_machine` | 0.77 | 0.50 |
| `hack_squat` | 0.35 | 0.40 |
| `preacher_bench` | 0.61 | 0.40 |
| `glute_kickback` | 0.56 | 0.37 |
| `t_bar_row` | 0.29 | 0.32 |
| `landmine` | 0.28 | 0.29 |
| `suspension_trainer_station` | 0.41 | 0.27 |
| `wall_ball_station` | 0.13 | 0.09 |
| `turf_lane+sled` | 0.08 | 0.06 |
| `ghd` | 0.08 | 0.05 |
| `battle_rope_station` | 0.08 | 0.05 |

Notes on the equipment mapping: the primary-equipment column uses the canonical taxonomy ids; composite keys (`dumbbell_set_full+flat_bench`, `dumbbell_set_light+adjustable_bench`, ...) mean the exercise holds a bench (the constrained station) while drawing a dumbbell pair from the rack. Exercise -> equipment class was cross-checked against free-exercise-db (S27; 876 exercises, equipment field: barbell 170, dumbbell 123, other 122, body only 111, cable 81, none 77, machine 67, kettlebells 56, bands 20, medicine ball 17, exercise ball 12, foam roll 11, e-z curl bar 9). Examples: "Barbell Bench Press - Medium Grip" = barbell; "Wide-Grip Lat Pulldown" = cable; "Leg Press", "Leg Extensions", "Seated Leg Curl", "Thigh Abductor", "Hack Squat", "Smith Machine Squat", "Butterfly", "Leverage Iso Row" = machine; "Barbell Hip Thrust" = barbell; "Hyperextensions (Back Extensions)" = other; "Face Pull", "Triceps Pushdown", "Cable Crossover", "Pull Through" = cable; "Goblet Squat" = kettlebells; "Pullups", "Dips - Triceps Version" = body only; cardio entries "Jogging, Treadmill", "Bicycling, Stationary", "Elliptical Trainer", "Rowing, Stationary", "Stairmaster", "Step Mill", "Recumbent Bike" = machine. (Note: free-exercise-db's "Air Bike" is a floor crunch, not a fan bike.) Fitbod lists its own equipment per exercise, e.g. Back Squat "Barbells, Squat Rack"; Bench "Barbells, Flat Bench"; Back Extensions "Glute Ham Raise Bench"; Calf Press "Leg Press"; Cable Lateral Raise / Face Pull "Hi-Lo Pulley Cable"; Cable Crossover Fly "Crossover Cable"; Lat Pulldown "Lat Pulldown Cable".

Substitution guidance for the Erlang-loss routing **[derived from Table 7.2]**: when a station is busy, the empirical swap targets are (i) the same movement on a different implement (bench -> DB bench 68 K swaps; leg press <-> machine leg press 47 K; lying <-> seated leg curl 60 K/26 K; pull-up -> lat pulldown 53 K; OHP -> DB shoulder press 35 K; deadlift/RDL -> DB RDL 33 K/29 K), then (ii) a different station training the same muscle (squat -> leg press 35 K / leg extension 18 K; deadlift -> seated leg curl 26 K; cable row -> machine row 27 K / lat pulldown 25 K). Suggested substitution acceptance probabilities for the model: same-movement alternative 0.6-0.8, same-muscle alternative 0.3-0.5, otherwise 0.1 **[estimate]**; normalise each row of swap counts in Table 7.2 to get the relative split among alternatives.

---

## 8. Sex differences - recommended adjustments

| Exercise / station | Women vs men (recommended W/M tilt in Table 6.1) | Evidence |
|---|---|---|
| Hip thrust (`hip_thrust_bench` / `hip_thrust_machine`) | 2.9x | SL: women 2.0 % of sets vs men ~0.22 % ("830% more"); Strength Level 58.6 % female; Fitbod 2022 3.42x (BB) / 5.58x (DB); Boostcamp #10 for beginner & intermediate women; physique women 80 % use |
| Hip abduction machine | 2.6x | Strength Level 52.7 % female; SL women 1.0 % (#24); Boostcamp #9 for beginner women (9.5 % of workouts) |
| Hip adduction machine | 2.0x | Strength Level 40.1 % female |
| Goblet squat, Bulgarian split squat, RDL | 1.5-1.7x | Strength Level 32.9 %, 27.4 %, 26.5 % female; SL women BSS 1.4 %, RDL 1.7 % vs men RDL 1.1 %; Fitbod 2022 BSS 2.55x, SL-RDL 2.22x |
| Leg press | 1.4x | SL 2.7 % vs 1.9 % ("42% more"); Strength Level horizontal leg press 33.5 % female |
| Squat, deadlift, lat pulldown, leg extension, leg curls | 1.1-1.15x | SL shares (e.g. squat 7.7 vs 6.7) |
| Bench press, DB bench | 0.77x | SL 8.2 vs 10.7 ("30% more" for men) |
| Barbell/EZ curl, incline bench (BB), dips, shrugs | 0.5-0.6x | SL BB curl 1.4 vs 2.4 ("71% more" for men); Strength Level incline 4.3 %, dips 5.4 %, shrug 4.2 %, EZ curl 5.4 % female; Fitbod 2022 dips 2.83x men, chin-ups 5.04x men, preacher 4.93x men |
| Region totals | women: +43 % glute and +28 % thigh sets; men: +64 % biceps, +50 % chest, +46 % triceps (S2); women glutes +56 % (S6); women lower-body 23.8 vs men 11.5 weekly sets, men upper 47.2 vs women 18.2 (S28) | |
| Cardio equipment users | 56 % female (ATUS 2003-06) vs weightlifting 36 % female | S22 |

Model use: compute the gym's demand vector as w = (1 - share_female) x men_vector + share_female x women_vector (both in Table 6.1). Default share_female 0.35-0.45 for a mixed commercial gym **[estimate]**; StrengthLog's implied set share is 0.35 (Section 2.1).

---

## 9. Conflicts and how they were resolved

| Topic | Conflict | Recommended model value |
|---|---|---|
| Rank of barbell lifts | StrengthLog/Strength Level put bench, squat, deadlift at #1-3 (bench 9.7 % of sets); Fitbod puts back squat ~30th and deadlift ~38th by number of lifters, with DB curl #1 | 50/50 mixture (bench 5.7 %, squat 4.1 %, deadlift 3.1 %); raise lambda (weight on StrengthLog) to 0.7-0.8 for performance gyms, lower to 0.2-0.3 for budget/beginner gyms |
| Most-logged exercise | Boostcamp: bench press 172 K workouts > DB lateral raise 153 K > squat 150 K > leg extension 147 K > lat pulldown 140 K; StrengthLog by sets: lateral raise only #7 | Use sets (StrengthLog, Fitbod) for demand; Boostcamp's workout-presence probabilities are used for co-location/validation only |
| Rest between sets | ACSM 2009 >=2-3 min (core) / 1-2 min (assistance); NSCA 30-90 s (hypertrophy); ACSM 2026: <1 vs >1 min no strength difference; survey: 89 % of timers rest <=60 s; trained lifters self-select 3.5-4.6 min on heavy squats | class-specific: 2.5 / 2.0 / 1.75 / 1.25 min (A / B / D / C) |
| Sets per exercise | ACSM 2009 1-3 (novice) / 3-6 (advanced hypertrophy); ACSM 2026 >=2, plateau 2-3; Boostcamp 2.2 completed-2.8 planned; single-user Strong log 4.5 incl. warm-ups | 3 working sets + class warm-ups |
| Session length | Boostcamp median 58 min (mean 87 inflated by un-closed sessions); Strava mean ~51 min; ATUS 0.9 h weightlifting/day; PureGym visit 69 min | 55-60 min strength sessions; visit 60-70 min including cardio/changing |
| Cardio vs strength time | ATUS 2003-06 -> 43 % cardio; HFA 2026 free weights fastest-growing; SFIA treadmill still the largest single activity by occasions (3.57 B) besides dumbbells (4.31 B) | 40 % cardio default |
| Cardio modality shares | SFIA includes home use (treadmill/bike over-weighted vs clubs); Girginer's gym: bike was the bottleneck (75 % first choice) | SFIA occasion shares, with 4 nominal small-modality weights (Section 3.4) |

---

## 10. Gaps
* No workout-tracking app publishes per-exercise shares for cardio machines in gyms; cardio modality weights rely on SFIA national participation (all venues).
* SFIA does not split upright vs recumbent bikes, and does not track air bikes, SkiErgs, curved treadmills or seated steppers (single-sport reports paywalled; sfia.org unreachable from the fetcher during this session).
* No public multi-user, set-level workout dataset with timestamps was found; set and rest durations rest on guidelines, two rest-interval studies and a single-user Strong log. Hevy/Strong exports are single users. Belt squat / pendulum squat, rotary torso, multi-hip and back-extension-machine demand have little or no direct data (Fitbod "Machine Squat" 233,699 sets is the closest proxy for belt/pendulum squats).
* Strength Level counts are strength-check entries (1RM calculators), not training frequency; used for sex mix only.
* StrengthLog lists only its top 25 (62.6 % of sets); the tail is imputed from Fitbod (Section 5.1).
* Turkish observation (S23) and ATUS (S22) are older (2006, 2003-06) and single-facility / national-general respectively.
* The BLS Spotlight page could not be fetched directly (empty response); its values were read from a PDF copy obtained in this session.
* Warm-up sets, setup/plate-loading time and transition time are estimates; no time-and-motion study of free-weight station setup was found.

## 11. Reproducibility
* Downloads (each in its own new directory under `research/downloads/`): `kaggle_weightlifting_joep89/` (Strong export, 9,932 set rows, 583 workouts), `free_exercise_db/exercises.json` (876 exercises), `ex_sfia2024/topline.pdf` (SFIA 2024 Topline), `ex_girginer2007/article.pdf`, `acsm2009/acsm2009.pdf`.
* Scripts (`research/ex_scripts/`): `analyze_strong_log.py`, `analyze_fedb.py`, `compute_weights.py` (weights, sex vectors, bout minutes, roll-up; output `research/ex_text/weights_out.json`), `cardio_weights.py`, `make_tables.py`. All run with `python3 -I` from outside the download directories.
