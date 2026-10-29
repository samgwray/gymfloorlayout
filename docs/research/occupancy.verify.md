# Verification log: occupancy slice

Adversarial fact-check of `occupancy.md`, 2026-10-28.

**Method.**
- Re-downloaded the two datasets and 17 PDFs into `scratchpad/verify_occ/`, separate from the researcher's copies.
- Re-analyzed both datasets with independently written code in `scratchpad/verify_occ_scripts/` (`berkeley_check.py`, `berkeley_season.py`, `ballarat_check.py`).
- Fetched every other cited page with WebFetch.
- The session's shared WebSearch budget was exhausted. No new searches were possible, so only known URLs were fetched.

**Result.**
- 69 datapoints checked: 63 confirmed, 3 corrected, 1 unsupported, 2 unreachable.
- No invented URLs or fabricated values were found. Every non-estimate quote matched its source.
- The problems are in the derived recommendations.

---

## 1. Corrections (derived values)

### 1.1 Peak concurrency per member is understated by about 15-20%

| Datapoint | Reported | Corrected |
|---|---|---|
| `rec.peak_pct_members` | 1.9% | **≈2.2%** |
| `rec.design_peak_pct_members` | 2.4% | **≈2.7-2.8%** |
| `rec.gross_sqft_per_user` | 140 sq ft | **≈120 sq ft** |

**Cause: mixed bases.**
- v_d = 0.17 is a 7-day average: annual visits ÷ members ÷ 365.
- s_peak = 11% and F_design = 1.25 are defined on **weekdays**: the BLS weekday column, Berkeley weekday-semester days, and Federation University weekday arrivals.
- Weekdays carry more than 1/7 of weekly visits. The sources the report already cites give the uplift (mean weekday share ÷ 14.29%):

| Source | Uplift |
|---|---|
| Federation University entries (S04) | 1.21 |
| Itensity check-ins (S38) | 1.23 |
| Planet Fitness, Mon-Wed only (S10) | 1.22 (an upper bound for Mon-Fri) |

**Fix.**
- Use `N = M × v_d × U_wd × s_peak × F_design`, with U_wd ≈ 1.15-1.2.
- Result: 2.15-2.30% of members at the average weekday peak, and 2.7-2.9% at the design peak.
- This sits next to the UK planning convention of 2.87-2.92%, which removes most of the conflict that Section 6 resolved by argument.

**Knock-on effects.**
- Worked-example design peaks rise to about 130 people (PureGym-like) and 114 (Gym Group-like).
- Gross area per design-peak user becomes 93-116 sq ft (PureGym-like, 12-15k sq ft) and about 143 sq ft (Gym Group-like). Central value about 120.

### 1.2 Berkeley densities are unsupported as measurements

Affects `berkeley.sqft_per_person_*` (110 / 83 / 73 / 59 sq ft per person).
- Neither the OpenML record nor the Kaggle metadata names the university or the counted space. The Kaggle metadata was pulled through Kaggle's API (author Nick Rose, last updated 2017-03-19).
- Two things fit UC Berkeley without proving it: the timestamps are US Pacific, and the data has semester flags. Many West Coast schools run on quarters.
- The RSF's 8,500 sq ft figure comes from the 2026 page, not 2015-17.
- If the AY2016-17 level is the real one, the same arithmetic gives about 187 sq ft per person on an average day.
- `rec.floor_sqft_per_user = 100` therefore rests on an unverified mapping plus a consultant's quote. The Les Mills 6-7 m² figure is attributed to Gerry Salmon and is not a standard.

---

## 2. Caveats the engine should encode

- **Design-day and season factors overlap.**
  - In AY2015-16, 9 of the 17 top-decile days were start-of-semester days. Mean on those days was 94.5, vs 74.4 on other days.
  - Excluding them leaves p90/mean at 1.267 in AY2015-16 but drops it to 1.186 in AY2016-17.
  - Do not multiply F_design 1.25 by the season factor 1.3. Use the larger of the two, or recompute.
- **PureGym "January +40%"** is relative to November-December, which includes December, the quietest month (S37). It overstates January vs an average month. It is also a secondary source (PerfectGym).
- **KKP comfort factor.** KKP never states a factor; 1.5 is implied by 617/411. Max Associates, Shropshire and Elmbridge use 1.0. Richmond's actual supply is 1,246 stations vs a modeled need of 661 (1.89×). Do not stack the factor on an Erlang model.
- **PureGym manager survey.** The figures are "% of UK gym managers that agreed X equipment was the most [least] used". No sample size, question wording or survey date is given. They are rank signals, not usage shares.
- **Alonso-Aubin's 97.29 s** is the set 1-2 interval only. Later self-selected rests rose and the last exceeded the 120 s fixed condition. It is weak support for a 90 s machine rest.
- **Ibbott and Piñero** studied trained lifters: Ibbott, 16 strength-trained men doing heavy back squat; Piñero, 40 trained adults. The 3.5 min barbell rest leans long for average members.
- **ABC Fitness.** 184M is US check-ins. The Fortune article of 28 May 2024 places it in the Q1 report but does not tie the figure to Q1 explicitly. The base of 40M members and 30,000 businesses is global, covering 100+ countries.
- **Row count.** The OpenML and Kaggle descriptions say "26,000 people counts"; the file has 62,184 rows. The report's figure is the correct one.
- **Federation University** data run October-February, which spans the Australian summer break.
- **Girginer bike time.** The model input is a "fixed 20 minutes", but Table 4's bike value-added time is 0.36 h (21.6 min).
- **BLS consistency check (supports the 11%).** The weekday hourly column sums to 227.6%, which implies a mean session of about 1.28 h (D + 1 ≈ 2.28 clock-hours touched). Then 20.5% × 1.28 / 2.28 = 11.5%, close to the recommended 11%.

---

## 3. Reproduced from the raw data (independent code, exact match)

**Berkeley** (OpenML 43752; MD5 0419bb31… matches OpenML).
- 62,184 rows, 2015-08-14 to 2017-03-18, 538 days. Max 145, mean 29.07, median 28, p95 71, p99 89.
- Pooled weekday-semester peak at 17:00, mean 58.9, which is 7.33% of the day's person-hours. Normalized profile identical.

| Metric | AY2015-16 | AY2016-17 |
|---|---|---|
| Per-day peak-hour mean | 76.9 | 45.5 |
| p90 | 97.2 | 56.2 |
| p95 | 101.9 | 58.8 |
| p90/mean | 1.265 | 1.235 |
| Daily 10-minute maximum (mean) | 88.0 | 56.2 |
| Peak-hour share of person-hours | 8.15% | 8.22% |

- Semester start: 73.2 vs 57.0, ratio 1.28.
- Weekend 45.3 (0.77×). Outside semester 39.7 (0.67×).
- Peak-hour distribution 77 / 69 / 40 / 21 / 16 / 14 / 10 / 15. Evening window share 19.8%.

**Federation University** (MD5 e1eeb1cc…, identical to the researcher's copy).
- 9,771 entries (9,708 Mem, 63 VP) on 146 days, 66.9 per day, maximum 151.
- Weekday and weekend hourly shares and day-of-week shares match exactly. One small omission: the weekend share at 07:00 is 0.5%.

---

## 4. Sources confirmed verbatim

| Datapoint(s) | Source | Result |
|---|---|---|
| bls.hourly_weekday / weekend / peak_hour_share; 0.7 h and 0.9 h for 2009-15 | S06 BLS 2017 | Full table matches; "5:00 p.m. to 7:00 p.m. was the most popular time" |
| bls.cardio_hours, weightlifting_hours, all_exercise_hours, duration distribution, gender splits | S05 BLS 2008 (PDF via WebFetch; MD5 matches the researcher's copy) | 0.7 / 0.9 / 1.5 h; 10/29/25/11/19/6%; 64/36 and 44/56 |
| tgg.visits_2023, avg_members, share_4plus, example_size | S13 RNS, S14 AR 2023 | "more than 60 million visits"; "872,000"; "almost six times per month"; 50.8%; Coventry 16,285 sq ft, opened Nov 2023 |
| puregym.visits_2019, members_per_gym, box_sizes | S15 AR 2019 | "70 million visits to a PureGym site in 2019"; 4,710 (FY2019 12-month column; Q4 column is 4,602); 1,124k average members; Fitness World acquired 14 Jan 2020, so it is excluded |
| puregym.stations_example; ukplan visits, 65%, /34, 1 h | S20 Elmbridge | PURE GYM LOCAL (WALTON-ON-THAMES), Stations 220; FIA 2012 parameters |
| ukplan (Richmond), sportengland.comfort | S18 | 1.5/week; 65%; 34 hours; 80% halls; 70% pools |
| ukplan.comfort_factor, KKP 1.75 and 39 | S17 | 24,664 × 65% / 39 = 411; 617 "with comfort factor applied"; "usage over 70% of capacity is busy" |
| ibc.*, ffpc.* | S24 WAC, S25 BOAF | "Exercise rooms 50 gross"; locker 50; pool 50; deck 15; FFPC 50 with equipment / 15 without |
| pf.* | S16 10-K | 19.7M members, 2,722 clubs; "typically 20,000 square feet"; no cardio time limits |
| placer.* | S07, S09, S10 | 72.4 to 74.0 min; dayparts 19.7/16.5, 11.8/22.2, 11.6/21.9; PF 4.1-4.4 and LT 5.7-6.2 visits/month (all of 2025); PF Mon/Tue/Wed 17.4/17.7/17.2% |
| placer.lifetime_long_visits | S11 (URL is real: "Gyms See Foot Traffic Surge in Q1…", 13 May 2024) | 43.3% of visits over 90 min |
| hotspot.*, leastused.*, puregym.busiest_times | S37 | All 20 percentages match |
| lesmills.*, cmaa.* | S22, S23 | 6-7 / 5 / 4 / 10 m²; 2 members/m²; 7.5 sq ft/member; 9,573 sq ft; 83% fitness |
| rsf.* | S02, S03 | 8,500 sq ft; over 100 cardio machines; 30-minute limit; virtual line at 95%, Mon-Fri 5-7 pm |
| girginer.* | S34 | 20-minute default; bike "fixed 20 minutes"; Table 4: 0.37 / 0.35 / 0.36 h; 91/39/20%; 75/20/5 and 20/5/45/30 splits; 0.87 h and 1.93 h; exponential arrivals and triangular service times |
| gerad.* | S35 | 60 customers, 3-hour window, 3-6 pieces each; cluster total 90; idle time 39 to 12 min; 17.5% / 19% |
| ibbott.*, alonso.*, pinero.*, acsm.* | S28-S33 | All quotes match. Ibbott protocol is heavy back squat (NSWIS, PubMed) |
| itensity.*, harvard.*, ucla.*, concept2.*, abc.*, season.*, vendor.*, ihrsa.*, idea.* | S38, S39, S52, S40, S49, S51, S50, S21 | All match as quoted |
| policy.uga / ohio / northeastern / britannia / memphis / ymca; ubc.birdcoop | S41-S46, S48 | All match |

---

## 5. Unreachable

- `chicago.open_floor` (S27): 403 from both the dev and production amlegal URLs. No search budget was left to find a mirror.
- `policy.rutgers` (S47): 403.
- Shropshire (S19): 503. Not needed, because Elmbridge and Richmond carry the same parameters.
