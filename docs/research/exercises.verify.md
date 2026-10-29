# Verification log: `exercises` slice (exercise popularity and time per exercise)

Checked 28 Oct 2026 by an adversarial fact-checker. Method: I opened each cited URL with WebFetch. Where the fetcher could not parse a PDF, I downloaded it again, confirmed it was byte-identical (SHA-256) to the researcher's copy, and ran `pdftotext` on it myself. I recomputed all derived arithmetic in `scratchpad/verify_scripts/check.py` and `check_local.py`. The web-search budget ran out partway through, so no new alternative sources could be searched.

## Verdict summary
- **66 datapoints checked: 65 confirmed, 1 corrected.** None were unsupported. One source (the BLS HTML page) was unreachable, but its PDF was found.
- **Highest-impact checks:** the SFIA cardio and strength occasions, the BLS time split, StrengthLog shares, Fitbod sets and swaps, Boostcamp session stats, the rest-interval sources and the Girginer cardio times. The rest are extra checks on items that were suspicious or single-sourced.
- Every quoted number matched the source exactly, to the digit. This covers StrengthLog S1/S2, Fitbod S5/S6/S7/S8 (including per-exercise sets and swap counts), Boostcamp S3/S4, SFIA S11, BLS S22 (PDF), ACSM S12/S13/S13b, Strength Level S9, Ibbott, Silva, Grgic, Singer, Schoenfeld 2015/2016, Garber, Girginer, Strava, PureGym, HFA, JEFIT, da Silveira, Barbosa and Hevy.
- All derived values reproduce:
  - top-25 sum 62.6
  - p_f 0.351
  - Strength Level female shares
  - SFIA cardio shares (sum 8.745 B; treadmill 40.77 %)
  - BLS time split 43.0 % cardio
  - Fitbod shares (bench 2.63 %, squat 1.82 %)
  - consensus bench 5.73 and squat 4.10
  - bout minutes 11.8 / 9.3 / 8.0 / 7.1 / 4.6 / 4.7 / 4.75
  - Strong-log 4.52 sets per bout and 17.0 sets per workout
  - free-exercise-db equipment counts

## Corrections and caveats
| Datapoint | Issue | Fix |
|---|---|---|
| `girginer.treadmill_time` (0.37 h) | Labeled "observed". The source's Table 4 is the **simulation** of the current system ("Mevcut sistem benzetiminde"). The bike service time was an input fixed at 20 min, and the console default is 20 min. | Relabel as a simulated value-added time per customer. Do not treat it as independent evidence for 25-27 min bouts. |
| `bls.time_split`, `bls.gender` | The cited URL https://www.bls.gov/spotlight/2008/sports/ returns an empty page. | Values confirmed in the official PDF https://www.bls.gov/spotlight/2008/sports/pdf/sports_bls_spotlight.pdf (byte-identical to the local copy). Cite the PDF instead. |
| `fb.hip_thrust_bb.sets` note | Fitbod's plain "Hip Thrust" (4,324,303 sets) is **bodyweight-only, lying on the floor**, not "unspecified loading". | Leaving it out of the loaded hip-thrust row is correct; fix the note. |
| `dasilveira.hip_thrust_women` note | "Seated hamstring curl 77 %": in the table the 77 % row is "hamstring leg curl machine"; the seated version is 69 %. | Minor note fix. |
| `silva18.rest_le_60s` | The source contradicts itself: Results say 88.9 % (264/297), the Abstract and Conclusions say 95.0 %. | The researcher already flagged this; 88.9 % matches the counts. |
| `bcg.*` sample | Described as "~1 M workouts"; the page says 901,452 workouts and 168,190 athletes. | Minor. |
| `rec.hip_thrust.weight_women` (estimate) | The tilt of 2.94 comes from the Strength Level OLS fit. StrengthLog's own "830 % more" implies a tilt of about 9.3, so the men's weight of 0.56 % is about 2.6 times the StrengthLog-implied 0.2 %. Fitbod 2022 (3.42x) supports about 3. | This is a defensible blend, but the results are sensitive to it. Document the choice. |

## Representativeness risks (values correct, applicability weak)
- **Cardio inputs come from all-venue national data.** SFIA 2023 participation-days and ATUS 2003-06 both include home and outdoor use. As a result, treadmill (40.8 %) and stationary bike are probably over-weighted compared with the share of time in clubs. SFIA does not split upright from recumbent bikes, so the 50/50 split is an assumption.
- **Cardio bout minutes have no observational anchor.** They rest on ACSM's ≥30 min/day, which is a daily recommendation, and on a simulation whose input was 20 min. ATUS gives 0.7 h per day across all cardio-equipment use.
- **Several free-weight hold-time inputs are assumptions with no time-and-motion source.** These are setup time (2.0 min), warm-up sets (2, from a single user), and the use of 3 working sets. Boostcamp implies about 2.2 completed sets per exercise.
- **The app populations are skewed.** StrengthLog users are strength-focused, while Fitbod users lean toward home and dumbbell training and their exercises are chosen by Fitbod's algorithm. Spearman correlation between the two is 0.06, so the default lambda of 0.5 largely sets the barbell share.
