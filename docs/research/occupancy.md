# Research slice: peak occupancy, attendance profiles, and equipment dwell times

Topic id: `occupancy`. Compiled 2026-10-28.

**Scope.** This slice gives the model what it needs to (1) estimate how many people are on the floor at the design peak, as a function of membership and/or floor area, and (2) set a mean occupancy time per use (minutes a user holds a station, including rest between sets) for each equipment class in the canonical taxonomy. It also covers hourly and weekly attendance shapes, design-day and seasonal factors, crowding hot spots, and the queueing literature for fitness facilities.

**Method.**
- Two public datasets were downloaded and analyzed with `python3 -I`:
  - The "Crowdedness at the Campus Gym" 10-minute head counts, 62,184 rows, mirrored on OpenML as dataset 43752. The MD5 matches OpenML's checksum.
  - The Federation University (Ballarat, Australia) gym entry log, 9,771 rows.
- About 50 primary and secondary sources were read: BLS time-use data, SEC 10-K filings, UK operator annual reports, UK local-authority facility-planning models, building codes, ACSM position stands, peer-reviewed rest-interval studies, a queueing-simulation paper, a 2026 GERAD optimization paper, operator policies, and foot-traffic analytics.
- The analysis scripts are in `scratchpad/research/scripts/` (`analyze_berkeley*.py`, `analyze_ballarat.py`).

**Search limits.**
- The session's shared WebSearch budget (200 calls across all agents) ran out partway through this slice. After that, only known URLs could be fetched.
- Some leads could not be pursued as a result. Section 7 lists them.

**Labeling.** Every number below is either quoted or pointed to in its source, or marked **[derived]** with its derivation. Recommended model values are always derived estimates.

---

## 0. Recommended model parameters (summary)

| Parameter | Recommended | Range | Basis (see sections) |
|---|---|---|---|
| Daily visits per member (visits ÷ members ÷ day) | **0.17** | 0.12–0.19 | Gym Group 2023 ≥0.188; PureGym 2019 ≈0.171; Planet Fitness visitors 4.1–4.4 visits/month (Placer.ai); UK planning models assume 1.5–1.75 visits/week (0.21–0.25/day) [derived] |
| Peak-hour concurrent occupancy as a share of that day's visits (average weekday) | **11%** | 9–13% | BLS weekday 6 pm: 20.5% of exercisers active in the hour; Berkeley 8.2% of daily person-hours × 1.2 h ≈ 9.8%; Federation Uni peak-hour arrivals 11.3–11.9%; UK planning model 13.4% [derived] |
| Peak concurrency as a share of members (average weekday peak hour) | **1.9%** | 1.3–2.9% | 0.17 × 11% [derived] |
| Design-day factor (90th-percentile day ÷ mean day, peak-hour occupancy) | **1.25** | 1.23–1.33 | Berkeley within one academic year: p90/mean = 1.26 and 1.23; p95/mean = 1.33 [derived] |
| **Design peak concurrency, % of members** | **2.4%** | 1.7–3.2% | 1.9% × 1.25; cross-check against UK planning convention of 2.87–2.92% per peak hour [derived] |
| Season surge (January, or semester start, vs. a typical in-season day) | 1.3 | 1.25–1.45 | Berkeley semester-start weekday peak ×1.28; PureGym January 2023 ≈ +40% vs. the prior two months (secondary source) |
| Within-hour (10-minute) peak ÷ hourly mean | 1.15 | 1.14–1.24 | Berkeley. Do **not** apply on top of an Erlang model, which already captures stochastic peaks |
| Weekend peak ÷ weekday peak | 0.75 | 0.5–0.9 | Berkeley 0.77; check-in day-of-week shares |
| Training-floor area per concurrent user at design peak | **100 sq ft** | 70–150 | Berkeley weight rooms: 110 sq ft/person on the average day's peak hour, 83 on the p95 day; Les Mills minimum 6–7 m² (65–75 sq ft) per person [derived] |
| Gross club area per concurrent user at design peak | 140 sq ft | 110–200 | Derived from UK budget-gym (HVLP) membership, visit and size data |
| Legal maximum occupant load | 50 gross sq ft/occupant | — | IBC Table 1004.5, "Exercise rooms 50 gross" |
| Station comfort factor | 1.5 stations per concurrent user | 1.25–1.5 | Knight Kavanagh & Page (KKP) fitness model ×1.5; Sport England comfort thresholds of 70–80% used capacity |
| Mean visit length, door to door | 72 min | 55–95 | Placer.ai value-tier gyms 72.4–74.0 min |
| Active training time per visit | 55 min | 42–70 | BLS weightlifting 0.9 h/day, cardio equipment 0.7 h/day; Piñero 2026 lab sessions 55.3 min; Girginer simulation 0.87 h |
| Rest between sets, held at the station | Machines and assistance lifts: 90 s. Barbell core lifts: 180–240 s | 60–280 s | ACSM 2009; Alonso-Aubin 2024 (97 s); Ibbott 2019 (208–278 s); Piñero 2026 (2.4–3.7 min) |
| Mean occupancy per use: treadmill / power rack / selectorized machine | 25 / 22 / 7 min | Section 3.5 | Derivations in Section 3 |

**How to compute peak concurrency.**
- From membership: `N_peak_design = M × v_d × s_peak × F_design`, with v_d ≈ 0.17, s_peak ≈ 0.11, F_design ≈ 1.25. This gives about 2.4% of members.
- From area: `N_peak_design ≈ A_training_floor / 100 sq ft`, or `A_gross / 140 sq ft`. Hard cap: `A_gross / 50` (code).
- When both membership and area are known, use the **smaller** of the two estimates, and check it against the code cap.

---

## 1. Peak occupancy and hourly attendance profiles

### 1.1 "Crowdedness at the Campus Gym" (university weight rooms, 10-minute head counts), analyzed here

**Source and provenance.**
- OpenML dataset 43752, mirrored from the Kaggle upload by nsrose7224. OpenML lists the collection date as 19 March 2017.
- The description says: "We measured how many people were in this gym once every 10 minutes over the last year."
- File: `Crowdedness-at-the-Campus-Gym.arff`, MD5 `0419bb319481db6bdb11ce211212cb9f`, which matches OpenML.
- The dataset does not name the gym. It is widely attributed to UC Berkeley's Recreational Sports Facility (RSF) weight rooms.
- The RSF publishes a weight-room crowd meter. Its facility page states: "Our three Recreational Sports Facility (RSF) weight rooms total 8,500 square feet."
- **Treat the 8,500 sq ft mapping as an assumption.** The dataset documents neither the counted space nor the counting method.

**Coverage.**
- 62,184 counts from 2015-08-14 to 2017-03-18, covering 538 calendar days and 516 near-complete days (at least 15 hours observed).
- Across all counts: maximum 145, mean 29.1, median 28, 95th percentile 71, 99th percentile 89.

**Structural break.**
- Weekday semester counts in academic year 2016-17 are about 40% lower than in 2015-16. The peak-hour profile mean fell from 71.3 to 41.4.
- This probably reflects a change in the meter or in the counted space, not real demand.
- The **shape** metrics are nonetheless stable across the two years:
  - Peak-hour occupancy as a share of daily person-hours: 8.15% vs. 8.22%.
  - p90/mean of daily peak-hour occupancy: 1.26 vs. 1.23.
- Pooled day-to-day factors are inflated by the break, so use the per-year values.

**Hourly mean occupancy, weekdays during semester, non-holiday (pooled, 29,921 counts).** The table gives the mean count, the share of the day's person-hours, and the 90th percentile.

| Hour | Mean | % of day | p90 | Hour | Mean | % of day | p90 |
|---|---|---|---|---|---|---|---|
| 05 | 1.4 | 0.2 | 4 | 15 | 43.9 | 5.5 | 65 |
| 06 | 13.9 | 1.7 | 24 | 16 | 52.0 | 6.5 | 79 |
| 07 | 24.3 | 3.0 | 37 | **17** | **58.9** | **7.3** | **90** |
| 08 | 32.4 | 4.0 | 47 | 18 | 57.7 | 7.2 | 87 |
| 09 | 37.3 | 4.6 | 53 | 19 | 54.2 | 6.7 | 82 |
| 10 | 40.9 | 5.1 | 59 | 20 | 50.7 | 6.3 | 79 |
| 11 | 42.6 | 5.3 | 63 | 21 | 53.3 | 6.6 | 84 |
| 12 | 41.7 | 5.2 | 61 | 22 | 50.7 | 6.3 | 81 |
| 13 | 40.5 | 5.0 | 58.7 | 23 | 36.9 | 4.6 | 70 |
| 14 | 39.6 | 4.9 | 57 | 00 | 25.5 | 3.2 | 46.7 |

- **Normalized weekday profile (peak = 1.00):** 06 0.24, 07 0.41, 08 0.55, 09 0.63, 10 0.69, 11 0.72, 12 0.71, 13 0.69, 14 0.67, 15 0.74, 16 0.88, **17 1.00**, 18 0.98, 19 0.92, 20 0.86, 21 0.90, 22 0.86, 23 0.63, 00 0.43.
- **Weekend during semester** (peak 17–18 h, mean 45.3): 08 0.39, 09 0.68, 10 0.83, 11 0.87, 12 0.82, 13 0.78, 14 0.79, 15 0.83, 16 0.89, 17 1.00, 18 1.00, 19 0.97, 20 0.92, 21 0.95, 22 0.94, 23 0.46.
- **Weekday outside semester:** peak at 18 h, mean 39.7, which is 0.67× the in-semester weekday peak.

**Which hour is each day's peak?** Over 262 weekday semester days: 17 h on 77 days, 18 h on 69, 21 h on 40, 19 h on 21, 16 h on 16, 22 h on 14, 20 h on 10, other hours on 15.

**Concentration of use.**
- On weekday semester days, the peak hour holds a mean of **8.2%** of the day's person-hours (per-day mean; pooled-profile value 7.3%).
- The figure is 8.9% on weekend semester days and 10.5% on weekdays outside semester.
- The 18:00–20:59 window holds 19.8% of daily person-hours.
- The peak-hour mean is 1.54× the mean over open hours on weekdays, 1.29× on weekends and 1.77× outside semester.

**Day-to-day variability, per academic year (weekday semester days only):**

| Metric | AY2015-16 (165 days) | AY2016-17 (97 days) |
|---|---|---|
| Per-day peak-hour mean occupancy: mean / median / p90 / p95 | 76.9 / 78.2 / 97.2 / 101.9 | 45.5 / 45.2 / 56.2 / 58.8 |
| Design-day factor p90/mean (p95/mean) | **1.26 (1.33)** | **1.23 (1.29)** |
| Daily maximum 10-minute count: mean / p90 / p95 / max | 88.0 / 112 / 116.8 / 138 | 56.2 / 74.4 / 81.0 / 108 |
| 10-minute peak ÷ peak-hour mean | 1.14 | 1.24 |
| Daily person-hours (mean) | 959 | 572 |

**Seasonality.**
- Weekday peak-hour occupancy at the start of semester was 73.2, vs. 57.0 for the rest of semester: a factor of **1.28**.
- Weekday mean occupancy by month: February 43.5 and September 41.3 vs. December 21.0 and June–July 22–23.

**Density, assuming the counts cover the 8,500 sq ft of weight rooms (AY2015-16) [derived]:**

| Scenario | Sq ft per person |
|---|---|
| Average day's peak hour (76.9 people) | 110 |
| p95 day's peak hour (101.9) | 83 |
| p95 day's 10-minute maximum (116.8) | 73 |
| Absolute maximum (145) | 59 |

The facility also shows queueing at the top end. The RSF runs a weight-room "virtual line", which "will be activated anytime the RSF Weight Room reaches 95% capacity or higher". It operated Monday–Friday, 5–7 pm, "through the fall 2024 semester". Separately, cardio "has a 30-minute limit, and sign-up is required for some machines". Sources: recwell.berkeley.edu RSF and crowd-meter pages.

### 1.2 Federation University (Mt Helen, Ballarat) gym entry log, analyzed here

**Source.** Ballarat Open Data, "Gym access times 1 Oct 2019 – 27 Feb 2020", CC BY-SA 4.0. The file is `gym_entry_point_data_cleaned_20191001-0227csv.csv`. The log records entries only, with no exit times.

**Coverage.** 9,771 entries (9,708 "Mem", 63 "VP"), all through "UniSports Reception". Entries fall on 146 days, a mean of 66.9 per day and a maximum of 151.

**Share of entries by hour of arrival:**

| Day type | Shares by hour |
|---|---|
| Weekday (n = 8,474) | 05 3.8%, **06 11.9%**, 07 6.0%, 08 5.6%, 09 4.9%, 10 4.8%, 11 5.0%, 12 6.5%, 13 6.5%, 14 4.7%, 15 6.1%, **16 11.3%**, **17 10.2%**, 18 6.2%, 19 4.5%, 20 2.0%. Top three hours: 33.4% |
| Weekend (n = 1,297) | 08 12.0%, 09 13.3%, 10 12.1%, 11 13.2%, 12 11.6%, 13 11.3%, 14 9.6%, 15 11.5%, 16 5.0% |

**Day of week:** Mon 20.3%, Tue 18.6%, Wed 17.9%, Thu 15.4%, Fri 14.5%, Sat 7.0%, Sun 6.2%.

**Takeaway.** The peak arrival hour holds about 11–12% of a weekday's arrivals. With visits of about 1 hour, the peak-hour concurrent occupancy is about 11–12% of daily visits [derived].

### 1.3 US time-use data (BLS American Time Use Survey)

**Hourly profile.** BLS Spotlight on Statistics, "Sports and Exercise" (2017), chart "Percentage of people who engaged in sports and exercise on a given day, by hour of day when exercising, 2009–15". The table gives total, weekend-day and weekday columns.

| Hour | Total | Weekend | Weekday | Hour | Total | Weekend | Weekday |
|---|---|---|---|---|---|---|---|
| 4 AM | 1.5 | 0.5 | 1.8 | 4 PM | 17.3 | 19.8 | 16.4 |
| 5 AM | 5.3 | 1.8 | 6.6 | **5 PM** | **19.1** | 17.5 | 19.7 |
| 6 AM | 9.3 | 6.1 | 10.4 | **6 PM** | 18.9 | 14.1 | **20.5** |
| 7 AM | 11.2 | 11.6 | 11.0 | 7 PM | 16.0 | 11.6 | 17.5 |
| 8 AM | 13.4 | 15.4 | 12.7 | 8 PM | 11.0 | 8.5 | 11.9 |
| 9 AM | 14.4 | 17.8 | 13.2 | 9 PM | 6.4 | 5.5 | 6.7 |
| 10 AM | 14.4 | 19.8 | 12.6 | 10 PM | 2.9 | 3.3 | 2.8 |
| 11 AM | 13.1 | 20.2 | 10.7 | 11 PM | 1.2 | 2.2 | 0.9 |
| Noon | 14.4 | 20.5 | 12.2 | Midnight | 0.7 | 1.6 | 0.4 |
| 1 PM | 14.2 | 21.5 | 11.6 | 1 AM | 0.6 | 1.2 | 0.3 |
| 2 PM | 14.9 | 20.8 | 12.8 | 2 AM | 0.3 | 0.8 | 0.1 |
| 3 PM | 16.0 | 20.4 | 14.5 | 3 AM | 0.3 | 0.3 | 0.3 |

BLS: "5:00 p.m. to 7:00 p.m. was the most popular time to participate in sports and exercise, overall."

**Normalized profiles [derived], recommended as the default shape for commercial (non-campus) gyms:**
- **Weekday:** 04 0.09, 05 0.32, 06 0.51, 07 0.54, 08 0.62, 09 0.64, 10 0.61, 11 0.52, 12 0.60, 13 0.57, 14 0.62, 15 0.71, 16 0.80, 17 0.96, **18 1.00**, 19 0.85, 20 0.58, 21 0.33, 22 0.14, 23 0.04.
- **Weekend:** 06 0.28, 07 0.54, 08 0.72, 09 0.83, 10 0.92, 11 0.94, 12 0.95, **13 1.00**, 14 0.97, 15 0.95, 16 0.92, 17 0.81, 18 0.66, 19 0.54, 20 0.40, 21 0.26, 22 0.15, 23 0.10.

**Concentration [derived].**
- The weekday peak hour holds 9.0% of the day's person-hour slots. The total column gives 8.07%, which closely matches Berkeley's 8.2%.
- 18:00–20:59 holds 21.9% of weekday slots. This is identical to Placer.ai's 21.9% of value-gym visits between 6 and 9 pm (Section 1.4).

**Converting to concurrency [derived].**
- If 20.5% of the day's exercisers are active at some point during the 6 pm hour, and visits last D hours, the expected occupancy at an instant within that hour is about 20.5% × D/(D+1).
- That gives about 11% of daily visitors for D = 1.2 h, and 12% for D = 1.5 h.

**Time per activity.** BLS reports average hours on days the activity was done:
- 2003–06 (BLS Spotlight, May 2008, p. 12): all sports and exercise 1.5 h; using cardiovascular equipment **0.7 h**; aerobics 0.8 h; running 0.9 h; **weightlifting 0.9 h**; walking 0.9 h; yoga 0.9 h.
- 2009–15 (2017 Spotlight): weight lifting 0.9 h on both weekdays and weekend days; cardiovascular equipment 0.7 h on both.

**Duration distribution, 2003–06:** under 30 min 10%; 30–59 min 29%; 1 h–1 h 29 min 25%; 1 h 30 min–1 h 59 min 11%; 2 h–3 h 59 min 19%; 4 h or more 6%.

**Participant gender split, 2003–06:** weightlifting 64% men / 36% women; cardiovascular equipment 44% / 56%.

### 1.4 Foot-traffic analytics (Placer.ai, US chains)

"The Current Pace of the Fitness Space" (Placer Research, 5 May 2025):
- **Average visit length at value-priced gyms rose from 72.4 minutes (Q1 2022) to 74.0 minutes (Q1 2025).** Mid-range and high-end tiers also rose, "relatively modest[ly]", but the report gives no figures for them.
- Share of visits by daypart, Q1 2025:

| Tier | 6–9 a.m. | 6–9 p.m. |
|---|---|---|
| High-end | 19.7% | 16.5% |
| Mid-range | 11.8% | 22.2% |
| Value-priced | 11.6% | **21.9%** |

Other Placer.ai figures:
- **Planet Fitness and Life Time, Q2 2025 recap:** "visitors to Planet Fitness visited an average of 4.1 to 4.4 times a month, while visitors to Life Time visit an average of 5.7 to 6.2 times a month."
- **Planet Fitness, H1 2024:** Monday 17.4%, Tuesday 17.7% and Wednesday 17.2% of weekly visits. Attendance "quiets down as the weekend approaches."
- **Life Time:** 43.3% of visits lasted more than 90 minutes (January–April 2024 data, reported by Athletech News on 13 May 2024).

**Caution.** Placer visit lengths come from mobile location data and include locker room and lobby time. Treat them as door-to-door durations, not time on the floor.

### 1.5 Check-in and swipe analytics (other operators and campuses)

- **Itensity gym software, South Africa, June 2026, 2,408,152 member check-ins.**
  - Day-of-week shares: Mon 21.8%, Tue 20.2%, Wed 17.2%, Thu 15.8%, Fri 12.7%, Sat 7.7%, Sun 4.5%.
  - Time blocks: 04:00–07:59 18.2%; 09:00–15:59 41.5%; 16:00–18:59 27.9%.
  - "On an average weekday, 17:00 runs at roughly 2.4 times the volume of the midday plateau." Friday 17:00 is "58% quieter" than Monday 17:00.
  - Saturday peaks at 08:00; Sunday at 11:00.
- **PureGym (UK) app data**, blog post of 30 October 2023:
  - Busiest day Tuesday; quietest day Sunday.
  - Busiest month February; quietest month December.
  - Busiest day of the year: the second Tuesday in March.
- **Harvard MAC swipes, September 2021 – August 2022 (Harvard Open Data Project):**
  - 94,628 swipes from 14,733 unique IDs. Swipes per ID: median 3, mean about 6.38, maximum 147.
  - Busiest days: Tuesday > Wednesday > Monday. Hourly peaks around 10 am and 5 pm.
- **UCLA Recreation (Daily Bruin, 2016):** about 1.5 million entrance records, June 2015 – June 2016. Weekday traffic peaks around 5:30 pm and "rapidly climbs from 2 PM onward."
- **ABC Fitness "Wellness Watch", Q1 2024** (reported by Fortune, 28 May 2024): 184 million US gym check-ins in the quarter, "nearly double pre-pandemic levels". The sample covers 40 million members and 30,000 businesses.

### 1.6 Seasonal and design-day factors

| Factor | Value | Source |
|---|---|---|
| Design day (p90 ÷ mean daily peak-hour occupancy) | 1.23–1.26 (p95: 1.29–1.33) | Berkeley, computed per year |
| Semester start vs. rest of semester | 1.28 | Berkeley |
| January surge | ≈1.4 vs. the prior two months | PureGym data as cited by PerfectGym (17 Sep 2024): "a nearly 40% surge in gym visits in January 2023 compared to the previous two months". **Secondary source** |
| January vs. December check-ins | 1.4–1.6 | Rework vendor guide. **Unsourced; low confidence** |
| Seasonal peak months | Jan–Mar; Sep–Oct | IDEA (2011): "Seasonally, the most crowded times are from January through March"; also September–October |
| Busiest weekday share of weekly visits | 17.7% (Tue, Planet Fitness) to 21.8% (Mon, South Africa) | vs. 14.3% average: ×1.24–1.53 |

---

## 2. Visits per member, members per square foot, and occupant load

### 2.1 Operator data

| Operator, year | Members | Sites | Visits | Derived [derived] |
|---|---|---|---|---|
| The Gym Group (UK, 24/7 HVLP), 2023 | 872,000 average; 850,000 at year end | 233 at year end (229 in 2022) | "more than 60 million visits"; "the average member visited almost six times per month"; "50.8% of our members visiting our gyms at least four times per month" | ≥5.73 visits/member/month; **≥0.188 visits/member/day**; about 3,775 members per gym; about 711 visits per gym per day |
| PureGym (UK, 24/7 HVLP), 2019 | 1,124k average | 263 at year end (222 in 2018) | "70 million visits to a PureGym site in 2019"; average members per gym **4,710** (2018: 4,994) | about 5.2 visits/member/month; **≈0.171 visits/member/day**; about 790 visits per gym per day. Assumes the 70 million excludes Fitness World |
| Planet Fitness (US HVLP), FY2024 | "approximately 19.7 million members" | 2,722 clubs, "typically 20,000 square feet" | No visit data in the 10-K. Placer.ai: visitors average 4.1–4.4 visits/month | **7,237 members/club; 0.36 members/sq ft (2.8 sq ft/member)** |
| Life Time (US premium) | — | — | Placer.ai: visitors 5.7–6.2 visits/month; 43.3% of visits >90 min | Member and size data not retrieved (Section 7) |

**Gym sizes.**
- PureGym defines "Large Box Format" gyms as "typically over 12,000 square feet" and "Small Box Format" gyms as "typically 6,000–9,000 square feet".
- Example Gym Group site: Coventry, 16,285 sq ft, opened November 2023.
- Example PureGym station count: PureGym Local Walton-on-Thames has **220 stations**, per the Active Places listing in Elmbridge Council's demand appendix.

**Planet Fitness and time limits.** The FY2024 10-K says that its use of space is, at least in part, why "we have not needed to impose time limits on our cardio machines."

**Members per square foot by format:**

| Format | Members per sq ft | Sq ft per member | Basis |
|---|---|---|---|
| US HVLP (Planet Fitness) | 0.36 | 2.8 | Derived from the 10-K |
| UK HVLP (PureGym, Large Box ≥12,000 sq ft) | 0.31–0.39 | 2.5–3.2 | Derived; 4,710 members over 12,000–15,000 sq ft |
| UK HVLP (Gym Group) | ≈0.23 | ≈4.3 | Derived; about 3,775 members over a 16,285 sq ft example site |
| Les Mills industry benchmark | 0.19 | 5.4 | "industry benchmarks suggest a target of 2 members per square meter (10.7ft²)" |
| Private-club fitness and spa (CMAA / CSFA) | 0.13 | 7.5 | "Respondents allocated 7.5 square feet per individual member in their fitness and spa facilities". The average fitness/wellness center was 9,573 sq ft in 2018 (10,120 in 2016); about 83% of that area is fitness |
| Boutique, strength gym, hotel, apartment | — | — | Not found (Section 7) |

### 2.2 UK facility-planning models (local-authority needs assessments)

These models convert membership into concurrent users at the peak hour. They assume each user occupies one station for a one-hour session.

| Model (author, year) | Visits per member per week | % of visits in peak | Peak hours per week | Session | Stations |
|---|---|---|---|---|---|
| Max Associates, Richmond (Nov 2023) | 1.5 | 65% | 34 | — | Stations = peak-hour visits ("divided by the number of peak time hours per week (34) to give the number of fitness stations required"). Penetration 14.6% |
| Shropshire Council appendix (2020; FIA 2019 parameters) | "1.5 times per week or six times per month" | "65% of use is during peak times" | "/34" | "The average health and fitness session is one hour" | Demand defined as "the demand during a peak hour session" |
| Elmbridge appendix (2017; FIA 2012 parameters) | 1.5 | 65% | 34 | 1 hour | Same method |
| Knight Kavanagh & Page (KKP), South Staffordshire (Jan 2020) | **1.75** | 65% | **39** (written "39 weeks"; the arithmetic shows peak hours per week) | — | 411 peak-hour visits → **617 stations "with comfort factor applied"**, i.e. a factor of 1.50 |

**Derived [derived].**
- Peak-hour visits per member = 1.5 × 0.65 / 34 = **2.87%**, or 1.75 × 0.65 / 39 = **2.92%**.
- As a share of an average day's visits: 0.65/34 × 7 = **13.4%** (11.7% using 39 hours).
- KKP's comfort factor implies about 4.4 stations per 100 members, or a target peak utilization of about 67% (1/1.5).

**Sport England Facilities Planning Model comfort thresholds:**
- Sports halls: "Sport England sets the comfort level at 80% of capacity used at peak times."
- Pools: "The model assumes usage over 70% of capacity is busy."
- These are useful analogues for a target peak utilization, or blocking tolerance, per equipment class.

**Industry rule of thumb (IHRSA, 2011, via IDEA Fit, Applebaum, 22 Nov 2011):** "you can expect 10%–12% of your members to use the facility during peak hours".
- This conflicts with the planning models' ~3% per peak hour, but the two are reconcilable. The IHRSA figure most plausibly counts users across a multi-hour peak period.
- For example, 11% across a 4-hour peak with 1.2-hour visits gives about 3.3% concurrent [derived].

### 2.3 Space per user while training

**Les Mills, "What's the most profitable area of your club?" (Jo Bryce, 2025):**
- "A gym floor requires 6 or 7m² per person" (65–75 sq ft).
- "cardio is 5m²" (54 sq ft).
- Group training studio "roughly 4m2 per person" (43 sq ft).
- CrossFit-style training "roughly ten square meters per person" (108 sq ft).

**Berkeley weight rooms** (Section 1.1): 110 sq ft/person on the average day's peak hour; 73–83 sq ft/person on the busiest days.

**Recommendation [derived].**
- Design to **100 sq ft of training floor per concurrent user** at the design peak.
- At 70–75 sq ft per user the floor is at Les Mills's minimum, i.e. crowded.
- The legal floor is 50 sq ft gross per occupant (Section 2.4).

### 2.4 Building code occupant load (life-safety maximum, not a comfort level)

**IBC 2021 Table 1004.5, "Maximum Floor Area Allowances Per Occupant"** (verbatim from Washington's adoption, WAC 51-50-1004, certified 3/27/2024):
- "Exercise rooms 50 gross"
- "Locker rooms 50 gross"
- "Skating rinks, swimming pools — Rink and pool 50 gross; Decks 15 gross"
- Footnote a: "Floor area in square feet per occupant."

**BOAF Informal Interpretation 8582** (Florida, 2021 edition): "Table 1004.5 establishes an occupant load factor of 50 gross for exercise rooms." It adds: "the FFPC establishes an occupant load factor of 50 for exercise rooms with equipment and 15 for exercise rooms without equipment." The FFPC is the Florida Fire Prevention Code, which is based on NFPA 101.

**Chicago amendment** (from a search snippet; the page returned 403): "Exercise rooms / With equipment / 50 gross / Open floor / 20 net".

**Implication.** A 10,000 sq ft gross gym has a code maximum of 200 occupants. The design peak is about 70–100 people, which is 35–50% of the code load [derived].

### 2.5 Worked examples [derived]

| Gym | Inputs | Design-peak concurrency |
|---|---|---|
| UK HVLP, PureGym-like | 4,710 members × 0.171 × 0.11 = 89 average-day peak; ×1.25 = **111** | On 12,000–15,000 sq ft gross: 108–135 sq ft per person |
| Gym Group-like | 3,775 × 0.188 × 0.11 = 78 average-day peak; ×1.25 = **98** | On about 16,000 sq ft: about 165 sq ft per person |
| 5,000 sq ft training floor, membership unknown | 5,000 / 100 = **50** design-peak users | Code cap ≈ 100 if the floor is the whole gross area |

---

## 3. Dwell times: visit level and station level

### 3.1 Visit duration

| Measure | Value | Source |
|---|---|---|
| Door-to-door, US value gyms | 72.4 min (Q1 2022) → 74.0 min (Q1 2025) | Placer.ai |
| Door-to-door, premium | 43.3% of Life Time visits >90 min | Placer.ai via Athletech |
| Time in activity on days performed | Weightlifting 0.9 h; cardio equipment 0.7 h; all exercise 1.5 h | BLS ATUS 2003–06 and 2009–15 |
| Lab session: 4 lower-body exercises × 4 sets at 10RM | 55.3 ± 12.6 min with 2–3 min prescribed rest; 70.5 ± 19.1 min self-selected | Piñero et al. 2026 |
| Simulated active (value-added) time per customer | 0.87 h; 0.76 h in the proposed scenario | Girginer & Şahin 2007 |
| Planned workout content (model assumption) | 3–6 pieces of equipment; each use at least one 5–10 min period; example facility limit 1 h; customer limit 45 min | GERAD G-2026-10 |

### 3.2 Cardio: minutes per use

**Girginer & Şahin (2007)**, Hacettepe J. Sport Sciences 18(1):13–30. Private fitness center in Turkey: 51 pieces of equipment; 45 days of logged arrival and usage times (from 19 June 2006); open weekdays 10:00–23:30.
- The cardio queue covered 14 machines: 5 treadmills, 5 "yatay bisiklet" (horizontal/recumbent bikes) and 4 "uzay yürüyüşü" (air-walker/elliptical type).
- Device programs default to **20 minutes**, adjustable by the user. Bikes were "used for a fixed 20 minutes".
- Simulated value-added time per customer: treadmill **0.37 h (22 min)**, air-walker **0.35 h (21 min)**, bike 0.36 h.
- Utilization: bike 91%, air-walker 39%, treadmill 20%.
- Warm-up choice: 75% bike, 20% air-walker, 5% treadmill. Cool-down choice: 20% bike, 5% air-walker, 45% treadmill; 30% left directly.

**ACSM (Garber et al. 2011):** "moderate-intensity cardiorespiratory exercise training for ≥30 min·d on ≥5 d·wk … or vigorous-intensity … for ≥20 min·d on ≥3 d·wk".

**BLS:** 0.7 h (42 min) of cardio-equipment use on days it is performed. This total may span several machines, and includes home equipment.

**Concept2 2025 Year in Review:**
- "Most Popular Workout Length: 30 minutes."
- "over 79.7 billion meters", more than 12.9 million workouts logged. That is about 6.2 km per logged workout [derived], mixing RowErg, SkiErg and BikeErg; BikeErg meters inflate the figure.
- These are dedicated logbook users, which biases the figure upward relative to gym warm-up use.

**Posted time limits.** Most limits are 30 minutes when others wait (Section 3.4). IDEA (2011): "typically 45–60 minutes max per person" during peak times.

### 3.3 Strength: set and rest structure

**ACSM Position Stand (Ratamess et al. 2009), MSSE 41(3):687–708:**
- "it is recommended that rest periods of at least 2–3 min be used for core exercises using heavier loads (... such as the squat and bench press)".
- "For assistance exercises ... a shorter rest period length of 1–2 min may suffice".
- Heavy loading (1–6 RM): "3- to 5-min rest periods".
- Hypertrophy: "1- to 2-min rest periods be used in novice and intermediate training programs".
- "one to three sets per exercise be used by novice individuals initially"; "three to four sets per exercise produced the most substantial effect sizes".
- Repetition velocity: "moderate contraction velocity (1–2 s CON; 1–2 s ECC)". That makes 10 reps last about 20–40 s [derived].

**Observed self-selected rest, all of which is spent at the station:**

| Study | Participants and protocol | Self-selected rest |
|---|---|---|
| Ibbott et al. 2019, IJSPP 14(7):980–986 | 16 strength-trained men; heavy back squat, 5×5 | Rose "from 207.52 to 277.71 s" between sets 1 and 4 (3.5–4.6 min). No performance difference vs. 3- or 5-minute prescribed rest |
| Ibbott et al. 2019, Perceptual and Motor Skills | Same population; 5 sets of 5RM squats | "interset rest period increased ... between Sets 3, 4, and 5" |
| Alonso-Aubin et al. 2024, JFMK | 13 trained men; back squat 5×4 at 80% of 1RM | "SR 97.29 ± 23.70 seg vs. FR 120 ± 0.00 seg" between sets 1 and 2 |
| Piñero et al. 2026, IJES Conference Proceedings 15(8):23 | 40 trained adults; Smith squat, leg extension, two calf raises, 4 sets at 10RM | **3.7 ± 1.2 min** self-selected vs. 2.4 ± 0.3 min prescribed |

The Piñero sessions work out to about 13.8 min per exercise with prescribed rest and 17.6 min per exercise with self-selected rest [derived].

### 3.4 Posted time limits (operator caps on dwell at peak)

| Facility | Cardio | Racks, benches, platforms | Other |
|---|---|---|---|
| UC Berkeley RSF | 30 min; sign-up required for some machines | Weight-room virtual line at ≥95% capacity, Mon–Fri 5–7 pm | — |
| University of Georgia (2022) | "Time is limited to 30 minutes on all equipment" in the weight rooms | 30 min at "a single station or activity ... when others are waiting" | — |
| Ohio University (WellWorks) | "20 minute time limit if someone is waiting" | Same limit | Peak defined as "4:30-7:30pm Monday-Friday" |
| Northeastern (Mills) | "20-minute time limit on all equipment if others are waiting" | Same limit | — |
| Britannia Centre (2026) | 30 min | "Squat racks: 20 min" | — |
| University of Memphis | 30 min if others waiting | — | — |
| YMCA of South Hampton Roads | "30-minute maximum on cardio machines during peak hours" | — | — |
| Rutgers (search snippet; page returned 403) | 45 min | 30 min on squat racks, benches and platforms | — |
| Planet Fitness 10-K | No cardio time limits needed | — | — |

These caps are binding only at the peak. They suggest that unconstrained dwell on racks and cardio often exceeds 20–30 minutes.

### 3.5 Recommended mean occupancy per use, by canonical equipment id [derived]

**Derivation used for resistance stations:**

`T = setup + n_sets × t_set + (n_sets − 1) × t_rest + loading/unloading + exit`

- t_set ≈ 0.6 min for 8–12 reps (ACSM velocity), or 0.5 min for heavy 3–5 reps.
- t_rest: 1.0–1.5 min for small and assistance exercises (ACSM; Alonso-Aubin's 97 s); 2–2.5 min for plate-loaded compound lifts; 3.5 min for barbell core lifts (Ibbott's 208–278 s; Piñero's self-selected 3.7 min).
- Sets: 3 working sets typical (ACSM); barbell lifts add 2–3 warm-up sets with about 1–1.25 min rests.
- Plate loading and unloading: about 2–3 min.

Worked derivations:
- Selectorized machine: 0.75 + 3×0.6 + 2×1.5 + 0.5 = **6.05 → 7 min**, rounded up for phone and adjustment time.
- Power rack (squat): 0.5 + 3 warm-ups × (0.5 + 1.25) + 4 working sets × 0.5 + 3 × 3.5 + 2.5 + 0.5 = **21.25 → 22 min**.
- Bench press station: 0.5 + 2 × (0.5 + 1.0) + 2.0 + 3 × 0.5 + 2 × 2.5 + 2.0 = **14 min**.

Cardio values anchor on Girginer (20–22 min), ACSM (at least 20–30 min) and the 30-minute caps. Low-data items are flagged low confidence.

| Id | Typical (min) | Range | Confidence | Basis |
|---|---|---|---|---|
| treadmill | **25** | 10–45 | medium-low | Girginer 22; 30-min caps; ACSM ≥20–30; BLS 42/day |
| curved_treadmill | 10 | 3–20 | low | Interval and sprint use; no data |
| elliptical | 22 | 10–40 | low-medium | Girginer air-walker 21 |
| upright_bike | 20 | 10–40 | low-medium | Girginer 20-min fixed |
| recumbent_bike | 22 | 10–40 | low | Girginer horizontal bike 20; older users |
| indoor_cycle | 20 | 10–45 | low | Open-floor use; classes excluded |
| air_bike | 8 | 3–15 | low | Interval use |
| rower | 12 | 5–30 | low | Concept2's 30-min mode is for dedicated users; gym warm-up use is shorter |
| stair_climber | 15 | 8–30 | low | High intensity; 30-min caps |
| ski_erg | 8 | 3–15 | low | PureGym managers: 17% name it "least used" |
| recumbent_stepper | 20 | 10–30 | low | Rehab and older-adult use |
| power_rack | **22** | 12–40 | medium-low | Derivation above; caps 20–30 |
| half_rack | 20 | 12–35 | low-medium | As for the rack, slightly shorter |
| lifting_platform | 25 | 15–40 | low-medium | Deadlift/Olympic: rack derivation + heavier loading |
| bench_press_station | 14 | 8–25 | medium-low | Derivation above |
| incline_bench_station | 12 | 8–20 | low | Bench derivation, fewer warm-ups |
| decline_bench_station | 10 | 6–15 | low | — |
| smith_machine | 13 | 8–25 | low | 0.5 + 2 warm-ups (3) + 3×0.5 + 2×2.5 + 1.5 |
| dumbbell sets (light, full, heavy extension) | 6 per pair-use | 3–10 | low | 0.5 + 3×0.6 + 2×1.5 + 0.5; a user typically does 2–3 dumbbell exercises |
| adjustable_bench | 12 | 6–20 | low | 2 dumbbell exercises × 4.8 + 1.5 |
| flat_bench | 10 | 5–18 | low | — |
| preacher_bench | 6 | 4–10 | low | Single-joint |
| hyperextension | 5 | 3–8 | low | — |
| ghd | 6 | 3–10 | low | — |
| dip_chin_station | 6 | 3–10 | low | — |
| hip_thrust_machine | 10 | 6–15 | low | Plate-loaded |
| hip_thrust_bench | 12 | 8–18 | low | Barbell loading |
| landmine | 8 | 5–12 | low | — |
| fixed_barbell_set | 6 per bar-use | 4–10 | low | — |
| kettlebell_set | 10 per user | 5–20 | low | — |
| leg_press | 10 | 6–15 | low-medium | Plate-loaded: 1 + 3×0.6 + 2×2 + 2.5 ≈ 9.3 |
| hack_squat, belt/pendulum squat | 12 | 8–18 | low | 4 sets, heavier |
| leg_extension, leg_curl, chest_press, shoulder_press, lat_pulldown, seated_row, assisted_pullup_dip, glute_kickback | **7** | 4–12 | medium-low | Selectorized derivation |
| leg_ext_curl_combo, pec_fly_rear_delt, hip_abductor_adductor, lat_pulldown_row_combo | 10–12 | 6–18 | low | Two exercises per visit |
| biceps_curl_machine, triceps_machine, ab_crunch_machine, back_extension_machine, calf_raise | 5 | 3–8 | low | Shorter rests (about 1 min) |
| rotary_torso | 4 | 2–6 | low | — |
| plate_loaded_chest_press, plate_loaded_row, plate_loaded_shoulder_press, plate_loaded_high_row, t_bar_row | 9 | 6–14 | low | Selectorized + plate loading |
| multi_station_gym | 7 per station-use | 4–12 | low | — |
| cable_crossover | 12 | 6–20 | low | Two exercises; occupies both stacks |
| functional_trainer | 12 | 6–20 | low | — |
| cable_column | 8 | 4–12 | low | — |
| rig_bay | 15 | 8–25 | low | Pull-ups + accessory circuits |
| turf_lane / sled | 8 | 4–15 | low | 4–6 lengths × (0.5 work + 1 rest) |
| plyo_box_set, wall_ball_station | 6 | 3–10 | low | — |
| battle_rope_station | 5 | 2–8 | low | — |
| suspension_trainer_station | 10 | 5–15 | low | — |
| heavy_bag | 12 | 6–20 | low | 3–4 rounds × (3 work + 1 rest) |
| stretch_area (per mat or user), accessory_pack mats | 10 | 5–15 | low | — |

**Model note.** Under the Erlang loss model (M/G/c/c), the blocking probability depends on the service-time distribution only through its mean (the insensitivity property). These means are therefore sufficient inputs.

**Offered load per class at the design peak:**

`a_k = λ_peak × u_k × n_k × S_k`, with `λ_peak = N_peak / D_floor`

- u_k: share of visitors using class k.
- n_k: uses per visit.
- S_k: mean occupancy from the table above.
- D_floor: active floor time, about 55 min.

---

## 4. Crowding hot spots: which equipment members wait for

**PureGym survey of UK gym managers (blog, 30 October 2023).** Percentages are the share of managers naming the item; the survey's sample size is not stated.
- **Most used:** Squat/lifting rack **49%**, Olympic lifting platform 37%, treadmill 33%, Climbmill/StairMaster 30%, cable machine 27%, dumbbells 26%, bench press 18%, barbells 11%, leg press machine 10%, leg extension machine 8%.
- **Least used:** Powerplate 50%, recumbent bike 31%, agility ladders 31%, Bosu ball 27%, sit-up machine 25%, stepper 22%, SkiErg 17%, Swiss ball 15%, multi-hip machine 12%, TRX system 10%.

**Other evidence:**
- **UC Berkeley RSF.** The weight-room virtual line runs Mon–Fri 5–7 pm when the room is at ≥95% capacity; cardio needs sign-up for some machines. The weight room is the binding constraint at the evening peak.
- **UBC Birdcoop** (student proposal, 2022): "four bench racks, five squat racks, and six lifting platforms". Demand causes "a shortage of popular gym equipment such as squat racks, bench racks, and lifting platforms". Waiting users stand by the equipment, so the station effectively stays occupied.
- **Girginer & Şahin (2007).** Bikes were the bottleneck: 91% utilization, a mean wait of 1.36 h and 5.66 people in queue. Bikes were the main warm-up choice (75%). Adding a sixth bike cut the mean bike wait to 1.00 h.
- **Planet Fitness** has not needed cardio time limits, attributed to its use of space.
- **GERAD paper:** "During peak hours ... the number of customers present in a facility often exceeds the available equipment capacity."
- **Vendor claims, low confidence (Rework guide):** "41% of cancellations cite 'overcrowding at peak times'", attributed to the IHRSA Consumer Report 2024 but not verified. "Off-peak (9am-4pm weekdays) utilization averages 28% of peak-hour capacity" is unsourced.

**Implication for the model.** The highest-blocking classes at peak are power racks, half racks and platforms, then treadmills, stair climbers, cables, dumbbells and the bench press. Give these the largest redundancy in large gyms. Recumbent bikes, ski ergs, multi-hip machines and specialty items have low demand.

---

## 5. Queueing models applied to fitness facilities

1. **Girginer, N. & Şahin, B. (2007).** "A case study of simulation for queueing problem in the fitness centers." Hacettepe J. of Sport Sciences 18(1):13–30.
   - Inter-arrival times fitted an exponential distribution (χ² test), i.e. Poisson arrivals. Service times fitted triangular distributions. FIFO single queue per equipment group.
   - Arena discrete-event simulation over an 11-hour day; 45 days of data from a private center.
   - The authors chose simulation over analytic models because the system "does not fit theoretical queue models".
   - Scenarios: adding one bike reduced the mean total time in system from 1.93 h to 1.60 h. An aerobics-class scenario reduced it to 0.89 h, with bike utilization falling to 58%.
2. **Těšínská, A. (2012).** "Obsluha zákazníků fitcentra" (Customer service in a gym), bachelor's thesis, University of Economics, Prague. Applies the "simple exponential model and the exponential model with a parallel service" (M/M/1, M/M/c) using the STORM and STOCHASTICA software to Hit Fitness Flóra in Prague. Only the record was accessible; no figures.
3. **Djeumou Fomeni, F. & Yermeche, E. W. (2026).** "A decision support optimization model to reduce congestion in fitness centres with an account for users' preferences." Les Cahiers du GERAD G-2026-10.
   - A capacity-constrained network-flow model with equipment clusters, using 5–15 minute periods.
   - Test case: 60 customers in a 3-hour peak, each planning 3–6 pieces of equipment.
   - The test facility replicates a real Montreal gym. Cluster capacities: leg machines 5, treadmills 8, stair mills 2, abs and lower back 3, free weights and benches zone 16, upper-body machines 7, recumbent and stationary bikes 10, rowing 3, ellipticals 8, bars 4, others 8, spin bikes 8, stretching 8. **Total 90** [derived].
   - Average idle (waiting) time under first-come-first-served (FIFO) was about 39 min per customer, falling to 12 min with optimization. Total delay fell by up to 17.5%; idle time by up to 19%.
4. **UK planning practice** (Sections 2.2 and 2.3) is a deterministic peak-hour method plus a comfort factor (KKP ×1.5), with Sport England comfort thresholds of 70–80% used capacity. It is an implicit target-utilization rule that the Erlang model can replace or calibrate against.

**Gap.** No peer-reviewed application of the Erlang loss model (M/G/c/c) to gym equipment sizing was found within the available search budget. The approach used here is analogous to telephone-trunk and hospital-bed sizing. With equipment substitution it becomes a loss network with overflow.

---

## 6. Conflicts and how they were resolved

| Issue | Sources | Resolution |
|---|---|---|
| Visits per member | UK planning 1.5–1.75/week (6.5–7.6/month) vs. operators: Gym Group ≈5.7/month, PureGym ≈5.2/month, Planet Fitness visitors 4.1–4.4/month (and inactive members not counted), Life Time 5.7–6.2/month | Use 0.17/day (≈5.2/month) as default; 0.12–0.15 for US HVLP with many inactive members; 0.19–0.20 for premium |
| Peak share | IHRSA "10–12% of members during peak hours" vs. planning ≈2.9% per peak hour vs. derived ≈1.9–2.4% | IHRSA counts the whole multi-hour peak period. Use 2.4% of members concurrent at the design peak |
| Day-to-day factor | Pooled Berkeley p90/mean 1.44 vs. per-year 1.23–1.26 | Pooled value is inflated by the 2016 structural break. Use 1.25 |
| Cardio dwell | Girginer ~20–22 min; BLS 42 min/day; IDEA caps 45–60 min; most caps 30 min; Concept2 30-min mode | Default treadmill 25, elliptical 22, bikes 20–22, stair climber 15; shorter for interval machines |
| Rest at racks | ACSM ≥2–3 min (3–5 heavy); observed self-selected 3.5–4.6 min (Ibbott) and 3.7 min (Piñero) vs. 97 s (Alonso-Aubin, first rest only) | Barbell core lifts 3–3.5 min; machines and assistance 1.5 min |
| Density at peak | Les Mills minimum 65–75 sq ft/person; Berkeley 73–110; IBC legal 50 gross | Design 100 sq ft of training floor per concurrent user; flag "crowded" below 75 |

---

## 7. Gaps and caveats

- **Search budget.** The session-wide WebSearch limit (200 calls, shared across agents) was exhausted. These leads could not be pursued:
  - Google Popular Times studies.
  - Planet Fitness crowd-meter methodology.
  - Live occupancy feeds from PureGym and The Gym Group.
  - IoT and sensor studies of per-machine dwell, such as GymCam-type camera studies and BLE beacons.
  - Published statistics from workout apps (Hevy, Strong, JEFIT, Fitbod, Boostcamp): workout duration, sets, rest timers.
  - HFA/IHRSA consumer-report visit frequencies.
  - Life Time 10-K center sizes and memberships.
  - Anytime Fitness and Orangetheory FDD membership counts.
  - Hotel and apartment fitness-center usage rates.
  - COVID-era density rules, such as ukactive's guidance.
- **No directly measured per-machine strength dwell times were found.** Strength values in Section 3.5 are derived from set and rest structure (ACSM, the rest-interval studies, the Piñero session times) and from posted caps. Confidence is low to medium.
- **Berkeley dataset caveats:**
  - The counted space is undocumented; the 8,500 sq ft mapping is assumed.
  - The ~40% level shift in academic year 2016-17 is unexplained.
  - The campus profile has more late-night use (21–23 h) than commercial gyms. Prefer the BLS-derived profile for commercial settings.
- **Federation University data** are entries only, at a small campus gym (about 67 entries/day).
- **Placer.ai visit lengths** are door-to-door from mobile panels. Daypart shares are of visits (arrivals), not occupancy.
- **Pages fetched only partly or blocked:**
  - ICC codes site (403): table quoted from WA WAC 51-50-1004 and the Florida BOAF interpretation instead.
  - Chicago amendment and Rutgers policy (403): values from search snippets only.
  - Medium article on the Kaggle dataset (403).
  - Harvard MAC raw CSV is on Google Drive and was not downloaded.
- **Boutique, strength-gym, hotel and apartment** members per square foot: not found.

---

## 8. Sources

| Id | Source | URL | Fetched |
|---|---|---|---|
| S01 | OpenML 43752 "Crowdedness-at-the-Campus-Gym" (Kaggle, nsrose7224; collected 2017) | https://www.openml.org/api/v1/json/data/43752 ; data: https://openml.org/data/v1/download/22102577/Crowdedness-at-the-Campus-Gym.arff | yes (downloaded, analyzed) |
| S02 | UC Berkeley RecWell, RSF facility page | https://recwell.berkeley.edu/facilities/rsf/ | yes |
| S03 | UC Berkeley RecWell, RSF Weight Room Crowd Meter | https://recwell.berkeley.edu/facilities/recreational-sports-facility-rsf/rsf-weight-room-crowd-meter/ | yes |
| S04 | Federation University, Gym access times 1 Oct 2019–27 Feb 2020 (Ballarat Open Data) | https://ballaratopendata.org.au/dataset/25da8aba-94e6-4593-b1b3-473744206304/resource/9f29bf6d-141b-499d-94dd-2e9d969826c4/download/gym_entry_point_data_cleaned_20191001-0227csv.csv | yes (downloaded, analyzed) |
| S05 | BLS Spotlight on Statistics: Sports and Exercise (May 2008) | https://www.bls.gov/spotlight/2008/sports/pdf/sports_bls_spotlight.pdf | yes |
| S06 | BLS Spotlight on Statistics: Sports and Exercise (2017) | https://www.bls.gov/spotlight/2017/sports-and-exercise/ | yes |
| S07 | Placer.ai, "The Current Pace of the Fitness Space" (5 May 2025) | https://www.placer.ai/anchor/reports/the-current-pace-of-the-fitness-space?gated=false | yes |
| S08 | Athletech News, "7 foot traffic insights..." (10 Jun 2025) | https://athletechnews.com/7-foot-traffic-insights-that-belong-on-every-gym-operators-radar/ | yes |
| S09 | Placer.ai, Life Time & Planet Fitness Q2 2025 recap | https://www.placer.ai/anchor/articles/life-time-planet-fitness-q2-2025-recap | yes |
| S10 | Placer.ai, Planet Fitness at the 2024 halfway point | https://www.placer.ai/anchor/articles/planet-fitness-at-the-2024-halfway-point | yes |
| S11 | Athletech News (13 May 2024), Placer.ai Life Time 43.3% >90 min | https://athletechnews.com/?p=105562 | yes |
| S13 | The Gym Group plc 2023 Full Year Results (RNS, 13 Mar 2024) | https://www.investegate.co.uk/announcement/rns/the-gym-group--gym/the-gym-group-plc-2023-full-year-results-/8084694 | yes |
| S14 | The Gym Group plc Annual Report 2023 | https://prelive.tggplc.com/media/tu2menvr/tgg_ar23.pdf | yes |
| S15 | PureGym Annual Report 2019 | https://s25.q4cdn.com/171963401/files/doc_financials/2019/ar/PureGym-Annual-Report-2019-Final.pdf | yes |
| S16 | Planet Fitness Form 10-K FY2024 | https://www.sec.gov/Archives/edgar/data/1637207/000163720725000016/plnt-20241231.htm | yes (first 100k characters) |
| S17 | KKP, South Staffordshire Indoor Sports Facilities Needs Assessment (Jan 2020) | https://www.sstaffs.gov.uk/sites/default/files/2023-03/indoor_sports_facilities_needs_assessment_january_2020.pdf | yes |
| S18 | Max Associates, Richmond-upon-Thames Indoor Built Sports Facility Assessment (Nov 2023) | https://www.richmond.gov.uk/media/hsdbmlfk/indoor_sports_facility_needs_assessment_2023.pdf | yes |
| S19 | Shropshire Council, Appendix 9 Demand for Health and Fitness 2038 | https://www.shropshire.gov.uk/committee-services/documents/s26045/Appendix 9 - Demand for Health and Fitness 2038.pdf | yes |
| S20 | Elmbridge, Appendix 8 Demand for Health and Fitness | https://www.elmbridge.gov.uk/sites/default/files/2023-03/Appendix%208%20-%20Elmbridge%20-%20Demand%20for%20Health%20and%20Fitness.pdf | yes |
| S21 | IDEA Fit, "Managing Peak Times at Your Facility" (Applebaum, 22 Nov 2011) | https://www.ideafit.com/managing-peak-times-at-your-facility | yes |
| S22 | Les Mills, "What's the most profitable area of your club?" (2025) | https://www.lesmills.com/articles/whats-the-most-profitable-area-of-your-club | yes |
| S23 | CMAA Board Brief, July 2020 (2019 CSFA Trends Report) | https://www.cmaa.org/media/1ndprduq/2020-07-boardbrief.pdf | yes |
| S24 | WAC 51-50-1004 (IBC 2021 Table 1004.5 as adopted by Washington) | https://lawfilesext.leg.wa.gov/Law/WACArchive/2024/pdf/WAC%20%2051%20-%2050%20%20CHAPTER/WAC%20%2051%20-%2050%20-1004.pdf | yes |
| S25 | BOAF Informal Interpretation 8582 (2021) | https://interpretations.boaf.net/view/8582/pdf | yes |
| S26 | ICC, IBC 2021 Chapter 10 | https://codes.iccsafe.org/content/IBC2021P2/chapter-10-means-of-egress | no (403) |
| S27 | Chicago Building Code ch. 14B-10 (amendment to Table 1004.5) | https://dev-codelibrary.amlegal.com/codes/chicago/latest/chicago_il/0-0-0-2547381 | no (403; snippet only) |
| S28 | ACSM Position Stand, Ratamess et al. 2009 | https://sfu.ca/~ryand/kin343/ACSMresistance.pdf | yes |
| S29 | ACSM Position Stand, Garber et al. 2011 (PubMed) | https://pubmed.ncbi.nlm.nih.gov/21694556/ | yes |
| S30 | Ibbott et al. 2019, IJSPP 14(7):980–986 | https://lida.sport-iat.de/ta/Record/4056101 ; https://www.nswis.com.au/nswis-news/the-effect-of-self-paced-and-prescribed-interset-rest-strategies-on-performance-in-strength-training/ | yes |
| S31 | Ibbott et al. 2019, Perceptual and Motor Skills (PMID 30866743) | https://pubmed.ncbi.nlm.nih.gov/30866743/ | yes |
| S32 | Alonso-Aubin et al. 2024, JFMK | https://pmc.ncbi.nlm.nih.gov/articles/PMC11503322/ | yes |
| S33 | Piñero et al. 2026, IJES Conference Proceedings 15(8):23 | https://digitalcommons.wku.edu/ijesab/vol15/iss8/23 | yes |
| S34 | Girginer & Şahin 2007, Hacettepe J. Sport Sciences 18(1):13–30 | https://dergipark.org.tr/en/download/article-file/151321 | yes |
| S35 | Djeumou Fomeni & Yermeche 2026, GERAD G-2026-10 | https://www.gerad.ca/papers/G-2026-10.pdf | yes |
| S36 | Těšínská 2012, VŠE Prague bachelor's thesis (record) | https://invenio.nusl.cz/record/115402?ln=en | yes (record only) |
| S37 | PureGym blog, "When is the gym quiet" (30 Oct 2023) | https://www.puregym.com/blog/when-is-the-gym-quiet | yes |
| S38 | Itensity, "When South Africa Goes to Gym: 2.4 Million Check-Ins Analysed" (2026) | https://itensityonline.com/?p=948336 | yes |
| S39 | Harvard Open Data Project, "How busy is the MAC?" | https://www.hodp.org/project/how-busy-is-the-mac | yes |
| S40 | Concept2, 2025 Year in Review | https://www.concept2.com/blog/2025-concept2-year-in-review-moving-together | yes |
| S41 | UGA Recreational Sports facility policies (Aug 2022) | https://recsports.uga.edu/wp-content/uploads/sites/17/2022/08/FAC_1_FACILITY-POLICIES-08.2022.pdf | yes |
| S42 | Ohio University WellWorks Fitness Center | https://www.ohio.edu/wellworks/fitness-center | yes |
| S43 | Northeastern Mills fitness center policies | https://millsatnucampussportsandrec.sites.northeastern.edu/files/2023/05/Policies-Fitness-Center-JPL.pdf | yes |
| S44 | Britannia Centre, Fitness Centre Etiquette (2026) | https://britanniacentre.org/wp-content/uploads/2026/04/Fitness-Centre-Etiquette-24x36-2.pdf | yes |
| S45 | University of Memphis Campus Rec, fitness area rules | https://preview.memphis.edu/campusrec/pdfs/finess-area-rules.pdf | yes |
| S46 | YMCA of South Hampton Roads | https://www.ymcashr.org/node/631 | yes |
| S47 | Rutgers Recreation, Fitness Center Policy | https://recreation.rutgers.edu/about-us/recreation-policies/fitness-center-policy | no (403; snippet only) |
| S48 | UBC ENGL301 student proposal (Birdcoop, 2022) | https://blogs.ubc.ca/engl30198a2022s12/files/2022/06/Chris-Jung-ENGL301-Formal-Research-Proposal.pdf | yes |
| S49 | Fortune (28 May 2024), ABC Fitness Q1 Wellness Watch | https://fortune.com/well/article/gym-use-increase-pandemic-gen-z/ | yes |
| S50 | Rework, Peak Hour Management & Capacity Planning for Gyms (vendor) | https://resources.rework.com/libraries/gym-fitness-growth/peak-hour-management | yes |
| S51 | PerfectGym blog (17 Sep 2024) | https://perfectgym.com/en/blog/club-owners/when-gym-least-busy | yes |
| S52 | Daily Bruin Stack, UCLA gym traffic (2016) | https://stack.dailybruin.com/2016/11/22/gym-traffic | yes |
