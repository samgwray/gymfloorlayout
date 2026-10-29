# Real-world gym benchmarks: FDD equipment costs, club sizes, equipment counts, members/sq ft, useful life

Research slice: **benchmarks** (used to check that optimizer outputs look like real gyms of the same size and budget).
Compiled 2026-10-28. All dollar figures are USD unless marked GBP/CAD. "FDD" = Franchise Disclosure Document; "Item 7" = Estimated Initial Investment table; "Item 19" = Financial Performance Representations.

**Method and source quality.** Full FDD PDFs sit behind state registries (NASAA EFD, MN CARDS, CA DFPI) that WebFetch could not reach. Item 7 lines therefore come from **third-party sites that reproduce the FDD tables line by line** (Franchise Direct, Zee Report, Franchise Chatter, 1851 Franchise, VetMyFranchise, FranchiseVS). Where two independent reproductions exist they agree, except where noted under Conflicts. Primary documents fetched directly:
- Crunch Multistate FDD (9/2025) Item 19 PDF
- Planet Fitness FY2025 10-K and 2025 Investor Day 8-K (SEC)
- Life Time FY2025 10-K (SEC)
- PureGym/Pinnacle Bidco 2018 Annual Report
- The Gym Group FY2025 results RNS
- IRS Publication 946 (2025)
- Franchisor websites (Anytime Fitness brochure, Snap Fitness, Crunch FAQ, Orangetheory, Burn Boot Camp, 9Round)

**Limitations.**
- The session's web-search budget ran out partway through (a limit shared by all agents). The rest of the work used direct fetches of known URLs only.
- HFA/IHRSA benchmark tables (club size, members/sq ft) are members-only and could not be read. See Gaps.

---

## 0. Headline benchmarks (for validating optimizer outputs)

| Benchmark | Small (1,000–3,500 sq ft studios) | Medium (4,000–10,000 sq ft, 24/7 / small box) | Large (15,000–40,000 sq ft big box / HVLP) |
|---|---|---|---|
| Equipment capex per gross sq ft (FDD-derived midpoints) | OTF $44, UFC Class $42, F45 ~$57, Club Pilates ~$71 (reformers), Burn Boot Camp $5 (bootcamp) | Anytime $27 (fitness eq. only; $35 with tech pkg), Snap ~$45 (website 4–6k sq ft), Workout Anytime ~$56 (pkg incl. amenities) | Planet Fitness $33, Crunch $39 (2026 FDD), Gold's Gym $43 |
| **Recommended validation band** | **$25–$75, typical $45** | **$20–$60, typical $35** | **$20–$75, typical $38** |
| Equipment pieces per 1,000 gross sq ft | Orangetheory ~13 stations/1k; vendor guide 12.5–17.5/1k (2,000–5,000 sq ft) | no direct count found (interpolated 10–15) | Planet Fitness (5 clubs opened 2024–26) 6.6–8.6, mean 7.8; PureGym 11–14.7 (220+ pieces in 15–20k sq ft) |
| Cardio share of pieces | OTF: 1/3 of stations are treadmills, 1/3 rowers, 1/3 floor | n/a | PF new format ≈40% (5 clubs, 40.0–41.0%); PF legacy example 59.5%; Gold's Gym cardio = 24–27% of equipment **dollars** |
| Members per gross sq ft | Burn Boot Camp ≈0.06 | Anytime Fitness ≈0.12 (0.09–0.17) | HVLP: PF 0.36, PureGym 0.25–0.33, Crunch 0.25. Mid-tier/MMA: UFC Gym 0.14–0.17. Luxury: Life Time ≈0.09 |
| Typical size by brand | OTF 2,690–3,765; F45 ~1,800–2,500; UFC Class 2,000–3,500; Club Pilates ~1,800–2,400 | Anytime 4,000–7,000; Snap 4,000–10,000+; Workout Anytime 5,000–15,000; PureGym small box 5,000–8,000 | PF ~20,000 (15–25k); Gold's 15–25k; Crunch 20–40k (sweet spot 25–30k); PureGym large box 15–20k; UFC Signature avg 32,874; Life Time ~95k (est.) |
| Equipment replacement cycle | — | — | PF: whole club every 5–9 yrs; cardio yrs 5–7, strength yrs 7–9; remodel yr 12 |

Equipment's share of total initial investment is typically 15–34% across formats (median ≈22%). Bootcamp formats are the exception at ≈7%.

---

## 1. FDD Item 7: equipment and related lines by brand

The $/sq ft figures are my derivation: equipment line ÷ stated sq ft range. Low = low $ ÷ high sq ft, high = high $ ÷ low sq ft, mid = midpoint $ ÷ midpoint sq ft.

### 1.1 Large-format gyms (15,000–40,000 sq ft)

#### Planet Fitness, 2026 FDD (issued May 22, 2026)
Sources: VetMyFranchise cost guide, Franchise Chatter 2026 review, 1851 Franchise deep dive. All three agree.

| Line | Low | High | Notes |
|---|---|---|---|
| Fitness Equipment (Item 7 line) | $33,300 | $995,000 | Low end = down payment if financed |
| — financed (down payment) | $33,300 | $298,500 | |
| — purchased outright | **$333,000** | **$995,000** | Quote: "If you choose to purchase rather than finance the required equipment for your location, the cost to purchase the equipment will generally range between $333,000 and $995,000." |
| Non-Fitness Equipment | $89,200 | $1,315,000 | Purchased outright: $892,000–$1,315,000 |
| Leasehold Improvements | $1,000,000 | $2,167,000 | |
| Total | $1,282,500 | $5,386,000 | Financed equipment: $1,282,500–$3,769,000; purchased: $2,385,000–$5,386,000 |
| Premises | 15,000 | 25,000 sq ft | Item 7 Note 3: "approximately 15,000 to 25,000 square feet" |

- **Re-equip:** Item 6 says "Every 5 to 9 years, as the franchisor specifies", at a current cost of $333,000–$995,000.
- **Remodel:** $250,000–$1,200,000, "as frequently as every 12 years".
- **Equipment $/sq ft (purchased):** low $13.3, mid **$33.2**, high $66.3.

**Prior year, 2025 FDD** (Franchise Direct):
- Fitness Equipment $36,300–$1,103,000
- Non-Fitness Equipment $76,200–$1,061,000
- Leasehold Improvements $1,250,000–$2,142,000
- Total $1,525,000–$5,221,500

**Item 19, 2026 FDD** (corporate-owned clubs, FY2025; Franchise Chatter):

| Third | Avg sq ft | Net revenue/sq ft | EBITDA/sq ft |
|---|---|---|---|
| Bottom (88 clubs) | 19,760 | $66.95 | $14.21 |
| Middle (87) | 19,619 | $100.99 | $36.13 |
| Upper (87) | 21,472 | $123.82 | $51.45 |

**SEC FY2025 10-K:**
- "Our bright, clean clubs are typically 20,000 square feet".
- "approximately 20.8 million members and 2,896 clubs (2,604 franchisee-owned and 292 corporate-owned)". That is **≈7,182 members/club** (derived).
- "generally replace the fitness equipment in their clubs every five to nine years"; "refurbish and remodel their clubs in year 12".
- Equipment segment revenue was $310.1M in 2025, 23.4% of total revenue.

**2025 Investor Day 8-K:**
- "New Club Capital ~$3M"; "Remodel ~$1M".
- "Unit build out cost $2.4mm - $4.0mm" (68 U.S. clubs, 2023).
- The New Growth Model targets a 5–10% reduction in new-club investment.

#### Crunch Fitness

**2026 FDD** (issued 2026-04-29). Item 7 per Zee Report; the line items sum to the stated totals.

| Line | Low | High |
|---|---|---|
| Fitness equipment, fixtures, other fixed assets | **$850,000** | **$1,500,000** |
| Office equipment, technology, furniture, graphics, supplies | $100,000 | $200,000 |
| Leasehold Improvements | $950,000 | $3,000,000 |
| Total | $2,147,500 | $5,367,000 |

**2025 FDD** (FranchiseVS):
- Fitness Equipment, Fixtures, Other Fixed Assets $150,000–$1,000,000
- Leasehold Improvements $650,000–$2,100,000
- Total $928,000–$3,743,000

**Crunch franchise FAQ:**
- "Our locations range from 20,000 to 40,000 square feet."
- Sweet spot "from 25,000 to 30,000 square feet", with at least 125 parking spots.
- "the initial investment is between $668,000 and $3,488,000, excluding real estate costs."

**Equipment $/sq ft (2026 FDD):** low $21.3, mid **$39.2** (at 30,000 sq ft), high $75.0.

**Item 19, Multistate FDD 9/2025** (primary PDF, FY2024 data, 143 clubs open 12–60 months, median-performing club per cohort):

| Cohort (months open) | 12–24 | 25–36 | 37–48 | 49–60 |
|---|---|---|---|---|
| Median sq ft | 27,000 | 31,220 | 34,000 | 40,000 |
| Average sq ft | 34,155 | 32,624 | 32,517 | 28,433 |
| Average members | 8,062 | 8,303 | 7,842 | 7,484 |
| Clubs | 55 | 34 | 19 | 35 |
| Members per sq ft (derived from averages) | 0.236 | 0.255 | 0.241 | 0.263 |

- Club-weighted: ≈7,949 members on ≈32,173 sq ft, i.e. **0.247 members/sq ft (≈4.0 sq ft/member)**.
- Pricing (Item 19 notes): "base membership package priced at $9.95/month, with a $29 or $39 annual fee"; Peak $19.95/month.
- Franchised clubs, FY2024 average gross revenue by third: $4.31M / $2.51M / $1.48M.

#### Gold's Gym, 2026 FDD
Sources: Franchise Direct and 1851 Franchise. They agree.

| Line | Low | High |
|---|---|---|
| Selectorized Equipment and Free Weights | **$425,000** | **$850,000** |
| Cardiovascular Equipment | **$160,000** | **$275,000** |
| Leasehold Improvements and Construction Costs (assuming no pool) | $1,500,000 | $3,125,000 |
| Initial Inventory, Other Equipment and Supplies | $7,000 | $40,000 |
| Total (excl. real estate purchase) | $2,356,000 | $5,162,000 |

- **Footprint:** "15,000 to 25,000 square feet" (1851).
- **Combined fitness equipment:** $585,000–$1,125,000. That is $23.4–$75.0/sq ft, mid **$42.8/sq ft**.
- **Strength vs cardio:** strength (selectorized + free weights) is **72.6–75.6% of equipment dollars**, a strength:cardio dollar ratio of 2.66–3.09. This is the only FDD found that splits strength from cardio. It is the clearest benchmark for a strength-heritage brand.

#### Retro Fitness
- 2024 FDD total $1,812,216–$2,911,991, $29,000 fee (Franzy). The equipment line was not obtainable.
- Search snippets cite a 2025 total of $2,037,316–$3,241,991 and a "Cardio + Strength Equipment Package $385,000–$625,000". Both are **unverified** (not fetched).

### 1.2 Medium (4,000–15,000 sq ft)

#### Anytime Fitness, 2026 FDD
Sources: Franchise Direct and VetMyFranchise. They agree.

| Line | Low | High |
|---|---|---|
| Fitness Equipment | **$139,873** | **$157,936** |
| Technology Equipment Package | $37,857 | $45,462 |
| Furniture & Fixtures | $15,200 | $18,330 |
| Leasehold Improvements | $170,280 | $417,300 |
| Total | $539,329 | $905,482 |

- **Item 7 assumption:** "a 4,000 to 7,000 square foot center built into a vanilla shell or as-is space".
- **Equipment $/sq ft:** $20.0–$39.5, mid **$27.1**. Including the technology package: mid $34.6.
- **Item 19 (2026 FDD), average monthly members per center:** 660 across all 1,683 centers. By quartile: 4th 995, 3rd 683, 2nd 550, 1st 411.
- **Members per sq ft (derived):** 0.094–0.165, mid **0.12** (≈8.3 sq ft/member).
- **Official 2022 brochure:** "In only about 7,000 square feet, your Anytime Fitness can fulfill member demand". 2022 FDD Item 7 total: $381,575–$783,897.

#### Snap Fitness

**2025 FDD** (Franchise Direct):
- Fitness Equipment **$60,000–$300,000**
- Furniture and Fixtures $25,500–$56,300
- Build-Out Labor $120,000–$240,000
- Leasehold Improvements $80,000–$280,000
- Technology $15,000–$25,000
- Total $430,800–$1,118,100

1851 Franchise reports the same FDD's fitness equipment as $60,000–$200,000 (see Conflicts).

**Snap website (2026), "Investment breakdown for a 4,000–6,000 square foot club":**
- Equipment **$200k–$250k**
- Leasehold Improvements $175k–$300k
- Total $555k–$828k
- Site requirement: "Min: 4,000 sq. ft." to "Max: 10,000+ sq. ft."
- Equipment $/sq ft: $33.3–$62.5, mid **$45**.

#### Workout Anytime, 2026 FDD
Sources: 1851 Franchise (three models) and Zee Report (Model 1).

| Model | Initial Equipment Package | Real Estate Improvements | Total |
|---|---|---|---|
| 1 | $393,500–$450,000 | $524,000–$657,000 | $1,091,700–$1,411,900 |
| 2 | $513,000–$566,000 | $676,000–$909,000 | $1,386,200–$1,795,400 |
| 3 | $606,000–$660,000 | $1,110,000–$1,313,000 | $1,931,200–$2,305,400 |

- **Size:** "usually in 5,000 to 10,000 square foot spaces"; "Club layouts can fit 7,000 to 15,000 square feet".
- **Equipment $/sq ft (Model 1 vs 5,000–10,000 sq ft):** ≈$39–$90, mid ≈$56. This is an estimate: the model-to-size mapping is not disclosed, and the package likely includes amenity equipment (HydroMassage, CryoLounge per Franzy), so it overstates fitness-equipment-only cost.

#### UFC GYM

**2026 FDD** (Franchise Direct), range from "Class by UFC GYM" to "UFC GYM (Core)":
- Fitness Equipment, Fixtures, and Other Fixed Assets **$142,000–$595,000**
- Leasehold Improvements $0–$500,000
- Total $250,897–$1,643,549
- Size: Class 2,000–3,000 sq ft; Core 8,000–12,000 sq ft.

**2025 FDD** (Franchise Chatter), Class by UFC Gym:
- "Equipment: $110,000 to $130,000"
- Leasehold Improvements $0–$115,000
- Total $232,526–$524,371
- Model sizes: Class ~2,200–3,500; Core ~6,000–10,000; Signature/UFC Fit 20,000–40,000+.

**Item 19 (2025 FDD), Signature/UFC Fit gyms:**
- 22 franchisee-owned gyms: sq ft 15,367–45,388 (avg **32,874**, median 35,302). Members at Dec 31, 2024: avg **5,548** (median 5,477). FY2024 revenue avg $3.59M.
- 3 affiliate-owned gyms: avg 38,807 sq ft; avg 5,233 members.
- Members/sq ft (derived): **0.169** franchise, 0.135 affiliate.

### 1.3 Small studios (1,000–3,800 sq ft)

#### Orangetheory Fitness, 2026 FDD (Franchise Direct)

| Line | Low | High |
|---|---|---|
| Fitness Equipment (incl. installation) and OTBeat System | **$119,122** | **$163,424** |
| Furniture, Fixtures & Equipment | $10,362 | $18,918 |
| Technology System | $46,760 | $62,108 |
| Leasehold Improvements and Construction Costs | $245,000 | $418,317 |
| Total (excl. real estate purchase) | $764,577 | $1,104,920 |

- **Studio size** (orangetheory.com international page): "250 - 350 m2 / 2,690 - 3,765 ft2".
- **Equipment $/sq ft:** $31.6–$60.8, mid **$43.8**.

#### F45 Training, 2025 FDD (Franchise Direct)
- "Equipment Pack" **$115,000** (fixed), plus Equipment Pack Taxes $0–$15,000
- Furniture/Fixtures/Other Equipment $4,000–$10,000
- Optional Recovery Amenities $40,000–$67,000
- Leasehold Improvements $1,000–$300,000
- Stated total $342,200–$786,100 (the low-column lines sum to $349,200)
- 2026 FDD total: $362,300–$857,700 (VetMyFranchise).
- **Size:** "1,800-2,500 square foot" (VetMyFranchise editorial, **not FDD**).
- Equipment $/sq ft ≈$46–$72, mid ≈$57 (estimate).

#### Club Pilates, 2026 FDD (Franchise Direct)
- Fitness Equipment & Initial FF&E Package **$128,986–$170,034**
- Leasehold Improvements $123,056–$519,381
- Stated total $431,289–$1,029,811 (the low column sums to $413,289)
- Size ~1,800–2,400 sq ft and 12–14 reformers are VetMyFranchise estimates, not FDD. Low confidence.
- Equipment $/sq ft ≈$54–$95. Reformer studio; not comparable to a free-weight gym.

#### 9Round, 2026 FDD (Franchise Direct)
- Opening Equipment and Inventory Package **$39,800–$41,700**
- Optional add-ons: Free Weight Station Package $0–$5,000; Cable Machine Package $0–$3,000; Stretching Station Package $0–$2,500
- Heart Rate Zone System $1,400–$2,400; Daily Workout Screens $12,000–$16,000
- Leasehold Improvements $10,000–$110,200
- Total $160,449–$390,300 (9round.com also shows "$160,449 - $390,300")
- Size: "typically 1,200-1,800 sq ft" (Franzy marketing text, low confidence).

#### Burn Boot Camp
- **2024 FDD** (Franchise Chatter):
  - "Exercise and Safety Equipment, Furniture, and Fixtures: $22,821 to $32,760"
  - Leasehold Improvements $59,867–$198,096
  - Total $249,375–$573,679
- **2026 FDD** (burnbootcamp.com): total "$291,145 to $678,003"; locations "approximately 3,600 to 7,000 square feet".
- **Equipment $/sq ft:** $3.3–$9.1, mid ≈$5.2. Bootcamp formats are equipment-light.
- **Item 19 (2024 FDD, 307 outlets, CY2023)**, average members by bracket:

| Bracket | >500 | 400–500 | 300–399 | 200–299 | <200 |
|---|---|---|---|---|---|
| Avg members | 569 | 442 | 343 | 250 | 169 |
| Outlets | 25 | 60 | 95 | 97 | 30 |

- Outlet-weighted average ≈**334 members** (derived), ≈0.063 members/sq ft.

#### Brands with no usable FDD data this session
- **EoS Fitness:** Franzy's "eos" page is EOS Worldwide, a coaching franchise. One third-party site (pulserevops) claims a 2026 EoS Fitness FDD total of "~$2,000,000 to ~$5,000,000". Not fetched, unverified.
- **Chuze Fitness:** no FDD located. It may be company-operated only (unverified).

---

## 2. Equipment counts per location and density

### 2.1 Planet Fitness opening announcements (piece counts + sq ft)

| Club (date) | Sq ft | Cardio | Strength | Total | Pieces / 1,000 sq ft | Cardio share | Gross sq ft / piece | Source |
|---|---|---|---|---|---|---|---|---|
| Worcester MA, Mercantile Center (Jul 25, 2025) | 13,605 | 48 | 69 | 117 | 8.60 | 41.0% | 116 | NEREJ |
| Lakewood WA (Jun 2, 2025) | 17,726 | 62 | 90 | 152 | 8.57 | 40.8% | 117 | Patch |
| Eden Prairie MN (opening Dec 14, 2024) | 19,000 | 62 | 93 | 155 | 8.16 | 40.0% | 123 | EP Local News |
| Puyallup South Hill WA (Oct 20, 2026) | 19,740 | 56 | 83 | 139 | 7.04 | 40.3% | 142 | KIRO 7 |
| Sammamish WA (Jun 12, 2026) | 21,141 | 56 | 83 | 139 | 6.57 | 40.3% | 152 | What Now |
| Duluth MN (undated; likely pre-rebalance layout) | 22,000 | 110 | 75 | 185 | 8.41 | 59.5% | 119 | WDIO |
| Shelby Twp & Bloomfield Twp MI (Jun 15, 2015) | 30,000 each | "over 120 pieces of high-quality cardio equipment" | n/a | — | — | — | — | REBusiness |

- **2024–2026 openings:** 6.6–8.6 pieces per 1,000 gross sq ft (mean 7.8, median 8.2). Cardio is a consistent **40–41% of pieces**: 2.65–3.53 cardio and 3.9–5.1 strength pieces per 1,000 sq ft.
- Gross area per piece is 116–152 sq ft. That area includes locker rooms, Black Card Spa (hydromassage, tanning) and the functional room.
- With ≈7,182 members/club, that is ≈46–61 members per piece (derived).
- The amenity lists show what the strength floor now includes: "plate-loaded bench presses, squat machines, and a seated calf raise", a turf functional room, a HIIT zone "with air bikes and rowers", stretching/mobility, and free weights (Worcester).

### 2.2 UK budget chains
- **PureGym:** "We're a 24 hour gym with over 220+ pieces of gym kit" (Leeds City Centre South page). A 2019 Leamington opening had "more than 220 pieces of equipment". The equipment page lists Matrix and Precor kit, "dumbbells ... up to 50kg in most gyms", and plate-loaded "in most gyms". The Leeds page adds a "6-bay lifting rig", "sled track", "BootyBuilder" and "perfect squat machine".
- Combined with large-box size of 15,000–20,000 sq ft (2018 AR), that gives **≈11–14.7 pieces per 1,000 sq ft** and ≈23 members per piece (derived).
- **The Gym Group:** "a typical fit out for one of The Gym Group's sites encompasses around 200 pieces of modern equipment" (Health Club Management, 2 Sep 2014; RFP to Life Fitness, Technogym, Precor, Cybex, Matrix).

### 2.3 Boutique studios
- **Orangetheory:**
  - Riverstone, 3,200 sq ft (2018): "will feature 14 treadmills, rowers and strength floor stations".
  - Bay Shore NY, 3,550 sq ft (2019): "equipped with 16 treadmills".
  - Tribeca (2023): "room for 16 people at each of three stations" (treadmill, rower, bench/free weights), so up to 48 per class.
  - Highland Village Houston, 3,229 sq ft (2019): 28 per class.
  - **Typical: 14–16 treadmills plus 14–16 water rowers plus 14–16 floor stations**, ≈13 stations per 1,000 sq ft.
- **Club Pilates:** 12–14 reformers (estimate, VetMyFranchise).
- **PushPress group-training example** (vendor guide, 2,500–3,500 sq ft):
  - "1 rig (6–8 stations) or 6 standalone racks"
  - "4× Concept2 Model D" rowers; "2× Echo or AssaultBike"
  - "6–8 sets" of bumpers
  - Equipment $28,000–$48,000
  - Pilates studio: "6–10 reformers at $3,500–$6,000 each"
  - Cycle studio: "20–25 bikes at $1,200–$2,500 each"

### 2.4 Vendor density rule of thumb
Atlantis Strength (Canadian manufacturer, Dec 2025):
- Mid-sized gym (2,000–5,000 sq ft): "about 25 to 35 pieces of exercise equipment per 2,000 sq ft". That is 12.5–17.5 per 1,000 sq ft.
- Strength area split: "60% machines and 40% free weights".

---

## 3. Cardio vs strength, and the shift toward strength

- **Planet Fitness (largest U.S. HVLP chain) rebalanced its floors in 2024–2025:**
  - 2025 Investor Day 8-K: "Moving clubs to a more balanced footprint of cardio and strength equipment".
  - Same 8-K: "More than 60% of franchisees opted-in to adding additional strength equipment in 2024"; "Option to remove 30-minute workout area to create space for more functional training".
  - Investor Day summary (search snippet): format-optimized clubs have "reduced cardio, more step mills, distributed free weights".
  - Q1 2025 call: "nearly 1,800 clubs have the more balanced mix of equipment". Also: "added the minimal three pieces of plate loaded across 65% of the estate last year". Every franchisee opening in 2025 chose the rebalanced mix.
  - Q4 2025 call: "In 2025, 95% of those who opened or remodeled clubs chose an optimized format"; "nearly 80% of our entire system featuring some version of a format-optimized layout or equipment offering".
  - Result in counts: recent PF openings are **≈40% cardio / 60% strength by piece count** (section 2.1). The undated Duluth example (likely the older layout) is 59.5% cardio.
- **Gold's Gym (strength heritage):** cardio is only **24–27% of equipment dollars** (2026 FDD). Cardio units cost more per piece than most strength stations, so cardio's share by **count** is likely ≤25%. That is an estimate, not a disclosed figure.
- **PureGym (UK HVLP):** recent sites advertise lifting rigs, sled tracks and plate-loaded glute machines alongside cardio (Leeds page).
- **Recommended model inputs (estimates):**
  - Budget/general gyms: target cardio ≈35–45% of pieces (typical 40%).
  - Strength-focused gyms: ≈20–30% (typical 25%).

---

## 4. Startup equipment budgets by size band

### 4.1 FDD-derived (most credible)

| Size band | Brand (FDD yr) | Sq ft | Equipment line | $/sq ft (low–mid–high) |
|---|---|---|---|---|
| Small 1k–3.8k | Orangetheory (2026) | 2,690–3,765 | $119,122–$163,424 | 31.6–43.8–60.8 |
| Small | UFC GYM Class (2025) | 2,200–3,500 | $110,000–$130,000 | 31.4–42.1–59.1 |
| Small | F45 (2025) | ~1,800–2,500 (not FDD) | $115,000 (+$0–15,000 tax) | 46–57–72 |
| Small | Club Pilates (2026) | ~1,800–2,400 (not FDD) | $128,986–$170,034 | 54–71–95 |
| Small | 9Round (2026) | ~1,200–1,800 (not FDD) | $39,800–$52,200 incl. optional pkgs | ~22–29–44 (est.) |
| Medium 3.6k–7k (bootcamp) | Burn Boot Camp (2024) | 3,600–7,000 | $22,821–$32,760 | 3.3–5.2–9.1 |
| Medium 4k–7k | Anytime Fitness (2026) | 4,000–7,000 | $139,873–$157,936 | 20.0–27.1–39.5 |
| Medium 4k–6k | Snap Fitness (website 2026) | 4,000–6,000 | $200,000–$250,000 | 33.3–45.0–62.5 |
| Medium 5k–15k | Workout Anytime M1–M3 (2026) | 5,000–15,000 | $393,500–$660,000 | ≈39–56–90 (est.; includes amenities) |
| Large 15k–25k | Planet Fitness (2026) | 15,000–25,000 | $333,000–$995,000 (purchase) | 13.3–33.2–66.3 |
| Large 15k–25k | Gold's Gym (2026) | 15,000–25,000 | $585,000–$1,125,000 | 23.4–42.8–75.0 |
| Large 20k–40k | Crunch (2026) | 20,000–40,000 | $850,000–$1,500,000 (incl. fixtures) | 21.3–39.2–75.0 |

- Medium-band totals cluster around **$140k–$250k for 4,000–7,000 sq ft**.
- Large-band totals cluster around **$330k–$1.5M for 15,000–40,000 sq ft**.

### 4.2 Vendor/consultant guides (lower credibility, for context)

**Atlantis Strength (CAD, Dec 2025):**

| Gym size | Total equipment (CAD) |
|---|---|
| Small (≤1,000 sq ft) | $10k–$40k ("$25 to $50 per sq ft") |
| Boutique (1,000–2,000) | $25k–$100k |
| Mid (2,000–5,000) | $50k–$200k+ |
| Large (5,000–10,000) | $200k–$500k+ |
| Luxury (10,000+) | ≥$500k |

**PushPress (2019, updated Oct 2026):**
- Group training (2,500–3,500 sq ft): $28k–$48k equipment, plus rubber flooring "$4,000–$9,000" for "3,000 sq ft". That is ≈$1.33–$3.00/sq ft (derived).
- PT studio (800–1,200 sq ft): $8k–$15k.
- Buying new adds "30–50%" over a mixed new/used purchase.

### 4.3 Equipment as a share of total initial investment (derived from FDD totals)

| Brand | Equipment share (midpoint) |
|---|---|
| Orangetheory | 15% |
| 9Round | 17% |
| PF (purchased) | 17% |
| Club Pilates | 20.5% |
| Anytime | 21% |
| F45 | 22% |
| Gold's | 23% |
| Snap (2025 FDD) | 23% |
| Crunch (2026) | 31% |
| Snap (website) | 32.5% |
| Workout Anytime | 34% |
| UFC (2026) | 39% |
| Burn Boot Camp | 7% |

Typical ≈22% (median of the 12 non-bootcamp brands; interquartile ≈19–32%). UFC GYM Class alone (2025 FDD: $110k–$130k of $232.5k–$524.4k) is ≈32%.

### 4.4 UK capex per site
- PureGym 2018 AR: "Average initial capital investment for mature gyms (£'000) 1,190" (2017: 1,142). This covers "site fit out, fixtures, fittings and equipment".
- That is ≈£60–£79 per sq ft for a 15–20k sq ft large-box site (derived).

---

## 5. Club size and members per square foot

| Operator / format | Size | Members | Members / sq ft (derived) | Source |
|---|---|---|---|---|
| Planet Fitness (HVLP) | "typically 20,000 sq ft"; corporate Item 19 avg 19,619–21,472 | 20.8M / 2,896 clubs = 7,182 | **0.36** (2.8 sq ft/member) | PF FY2025 10-K; 2026 FDD Item 19 |
| Crunch (HVLP) | avg 28,433–34,155; median 27,000–40,000 | avg 7,484–8,303 | **0.236–0.263** (club-weighted 0.247) | Crunch FDD 9/2025 Item 19 |
| PureGym large box (UK HVLP) | 15,000–20,000 | 4,994 avg per gym (2018) | **0.25–0.33** | Pinnacle Bidco AR 2018 |
| The Gym Group (UK HVLP) | not disclosed (one 20,000 sq ft "destination" test) | 945k avg / 260 sites ≈3,635 | n/a | FY2025 RNS |
| UFC GYM Signature/UFC Fit | avg 32,874 (franchise), 38,807 (affiliate) | 5,548 / 5,233 | **0.169 / 0.135** | 2025 FDD Item 19 |
| Anytime Fitness (24/7 small box) | 4,000–7,000 | 660 avg monthly members | **0.094–0.165** (mid 0.12) | 2026 FDD Items 7/19 |
| Life Time (luxury athletic club) | >18M indoor sq ft / 189 centers ≈95,000 | 1.6M individuals / 189 ≈8,466 (873k memberships ≈4,619) | **≈0.089** | Life Time FY2025 10-K |
| Burn Boot Camp (bootcamp studio) | 3,600–7,000 | ≈334 avg (bracket-weighted) | **≈0.063** | 2024 FDD Item 19 |

- **HFA context:** "Commercial Fitness Facilities: 55K+" in the U.S. (HFA homepage). The 2026 HFA Fitness Industry Benchmarking Report (244 operators, ~27,000 facilities) is members-only.
- **Visit frequency** (useful for the occupancy slice): Life Time reports "Average visits per membership ... 149 for 2025". At 1.83 individuals per membership, that is ≈81 visits per individual per year (derived).
- **Revenue per member** (only for sizing context): Crunch base $9.95/mo plus a $29–$39 annual fee; PureGym £18.38/member/month (2018); Life Time $3,531 per center membership per year (2025).

**Recommended members/sq ft for the model (estimates):**

| Format | Typical | Range |
|---|---|---|
| HVLP big box | 0.30 | 0.24–0.36 |
| Mid-tier big box | 0.15 | 0.13–0.17 |
| 24/7 small box | 0.12 | 0.09–0.17 |
| Luxury | 0.09 | — |
| Boutique/bootcamp | 0.06 | 0.05–0.10 (low confidence) |

---

## 6. Equipment useful life and replacement cycles

| Source | Statement | Value |
|---|---|---|
| Planet Fitness FY2025 10-K | "Franchisee-owned clubs are generally required to replace their equipment every five to nine years"; remodel "in year 12" | 5–9 yrs; remodel 12 yrs |
| PF 2026 FDD Item 6 | Re-equip "Every 5 to 9 years, as the franchisor specifies"; remodel "as frequently as every 12 years" | 5–9 yrs |
| PF 2025 Investor Day (slide 17) | New model: cardio re-equip years 5–7, strength years 7–9. Previous model: cardio yr 5, strength yr 7. "Determined based on club usage". Slide text was scrambled, so the column assignment is inferred. | cardio 5–7; strength 7–9 |
| PF equipment revenue mix | Replacement ≈60% of Q4-2025 equipment revenue; 2026 guide ≈70% re-equip; 96 new-club placements in Q4 2025 | — |
| PureGym 2018 AR (depreciation) | "Fixtures and fittings Straight line over 6 years"; "Leasehold improvements Straight line over 3-15 years"; "IT equipment ... 3 years" | 6 yrs |
| The Gym Group FY2025 | "Maintenance Capital Expenditure - costs of replacement gym equipment" = £17.3m for 260 sites; useful economic life of "certain gym and other equipment" revised from 1 Jan 2025 (detail in AR 2024 p.132, not retrieved) | ≈£66.5k per site per year (derived) |
| IRS Pub 946 (2025), Table B-1 | Class 79.0 Recreation ("entertainment services on payment of a fee or admission charge"): class life 10, GDS 7, ADS 10. Class 57.0 Distributive Trades and Services (personal services): 9 / 5 / 9 | Tax: 7-yr GDS typical |

**Recommended model values (estimates):**
- Cardio: 6 yrs (5–7)
- Strength (selectorized/plate-loaded): 8 yrs (7–9)
- Racks, benches, plates and dumbbells: at least the strength life, ≥8 yrs. No source quantified this; PushPress says only that steel "doesn't wear out".
- Annual replacement reserve ≈ equipment capex ÷ blended life (6–8 yrs) ≈ 12.5–17% of initial equipment cost per year; ≈14% at a 7-yr blend (derived).

---

## 7. Conflicts and how they were reconciled

1. **Snap Fitness 2025 FDD fitness equipment:**
   - Franchise Direct: $60k–$300k.
   - 1851 Franchise: $60k–$200k.
   - Snap's own 2026 website: $200k–$250k for 4,000–6,000 sq ft.
   - **Use:** the website figure (≈$45/sq ft typical).
2. **Crunch equipment line:**
   - 2025 FDD: $150k–$1.0M.
   - 2026 FDD: $850k–$1.5M.
   - The 2025 low end is implausible for a 20–40k sq ft club and may reflect financed or used packages or conversions. **Use:** 2026.
3. **Crunch totals:**
   - FAQ: $668k–$3.488M excluding real estate.
   - 2025 FDD: $928k–$3.743M.
   - 2026 FDD: $2.1475M–$5.367M (includes real estate lines).
   - These are different years and scopes. **Use:** 2026 for current.
4. **Planet Fitness equipment:**
   - 2025 FDD: $36.3k–$1.103M.
   - 2026 FDD: $33.3k–$995k.
   - The drop matches the New Growth Model's targeted 5–10% investment reduction. **Use:** 2026 purchase range $333k–$995k.
5. **PF club size:**
   - 10-K "typically 20,000"; FDD 15k–25k; Item 19 corporate average 19.6k–21.5k.
   - Openings range 13.6k–42.3k (the 42,315 sq ft Hope Mills club is from a search snippet only).
   - **Use:** 20,000 typical.
6. **Anytime Fitness size:**
   - 2022 brochure "about 7,000"; 2026 Item 7 4,000–7,000.
   - Other unverified sites give 3,500–8,000.
   - **Use:** 4,000–7,000, typical 5,500.
7. **Orangetheory size:**
   - Official 2,690–3,765.
   - Unverified sites give 1,800–3,200 or "prototype B 2,800–3,400".
   - **Use:** official.
8. **UFC GYM model sizes:**
   - 2026 page: Class 2,000–3,000, Core 8,000–12,000.
   - 2025 page: Class 2,200–3,500, Core 6,000–10,000.
   - Reported as a range.
9. **Table arithmetic:**
   - F45 low total stated $342,200 vs lines summing to $349,200.
   - Club Pilates low $431,289 vs $413,289.
   - Snap totals are $500 off the line sums.
   - Equipment lines are unaffected.
10. **PF cardio share:**
    - Recent openings ≈40%; Duluth 59.5%.
    - The difference reflects the 2024–25 rebalance. **Use:** 40% for new budget-gym builds.

---

## 8. Recommended validation bands for optimizer outputs

These are my estimates synthesized from the data above.

| Check | Small (≤3,500 sq ft) | Medium (4,000–10,000) | Large (15,000–40,000) |
|---|---|---|---|
| Equipment $ / gross sq ft | 25–75 (typ. 45) | 20–60 (typ. 35) | 20–75 (typ. 38; HVLP ≈33, strength-focused ≈43) |
| Pieces / 1,000 gross sq ft | 12–17 (typ. 13) | 10–15 (typ. 12) | 6–10 (typ. 8) |
| Gross sq ft per piece | ≈60–85 | ≈65–100 | ≈100–150 (PF 116–152) |
| Cardio share of pieces | studio-dependent | 35–45% | budget 35–45% (typ. 40%); strength-focused 20–30% (typ. 25%) |
| Members / sq ft (for demand sizing) | 0.06–0.10 (boutique) | 0.09–0.17 (typ. 0.12) | 0.13–0.36 (HVLP typ. 0.30; mid-tier 0.15) |
| Equipment share of all-in opening budget | 15–32% | 20–34% (bootcamp ≈7%) | 17–31% |

Interpretation:
- If an optimizer plan for a 20,000 sq ft, ~$660k budget gym yields ~160 pieces (8 per 1,000 sq ft) with ~40% cardio, it matches a 2025-era Planet Fitness.
- A 5,500 sq ft, $150k plan should look like an Anytime Fitness. No piece count was found for that format; a vendor heuristic suggests ~55–80 pieces (est.).

---

## 9. Gaps

- HFA/IHRSA benchmark tables (median club size, members/sq ft, revenue/sq ft, equipment capex) are members-only. The 2026 HFA Benchmarking Report and older IHRSA Profiles of Success were not readable.
- No FDD equipment line obtained for EoS Fitness (franchise status unverified) or Chuze Fitness (likely not franchised). Only totals were obtained for Retro Fitness.
- No FDD gives a separate flooring line; flooring is buried in leasehold improvements or FF&E. The only flooring figure is a vendor blog's ≈$1.3–$3.0/sq ft for rubber.
- No published piece counts for Anytime Fitness / Snap Fitness equipment packages, Crunch clubs, or Gold's Gym clubs.
- The Gym Group average gym size and revised equipment useful-life policy (AR 2024 p.132) were not retrieved.
- Depreciation lives for fitness equipment in the PF and Life Time 10-K notes were not retrieved: the WebFetch text was truncated and direct SEC download was blocked.
- Several studio sizes (F45, Club Pilates, 9Round) come from editorial or marketing text, not FDD notes.
- The web search budget ran out mid-task, so some leads (Retro Fitness Item 7 detail, PF Q2-2025 call ">70% of clubs" statement, Hope Mills 42,315 sq ft) are reported only as unverified search snippets or omitted.

---

## 10. Sources

### FDD reproductions and franchisor material
- Franchise Chatter – Planet Fitness 2026 review: https://www.franchisechatter.com/2026/09/21/planet-fitness-franchise-review-2026-costs-fees-news-average-revenues-and-or-profits/
- VetMyFranchise – Planet Fitness cost guide (2026 FDD): https://vetmyfranchise.com/blog/planet-fitness-franchise-cost-guide
- 1851 Franchise – Planet Fitness deep dive: https://1851franchise.com/franchise-deep-dive-planet-fitness-franchise-costs-fees-profit-and-data-2723399
- Franchise Direct – Planet Fitness (2025 FDD): https://www.franchisedirect.com/fitnessfranchises/planet-fitness-franchise-12988/ufoc
- Franchise Direct – Anytime Fitness (2026 FDD): https://www.franchisedirect.com/directory/anytimefitnessinc/ufoc/5872
- VetMyFranchise – Anytime Fitness (2026 FDD): https://vetmyfranchise.com/blog/anytime-fitness-franchise-cost
- Anytime Fitness franchise brochure (2022 FDD figures): https://www.anytimefitness.com/wp-content/uploads/2022/06/The-Anytime-Fitness-Franchise-Opportunity.pdf
- Snap Fitness investment page: https://www.snapfitness.com/us/why-franchise-with-snap-fitness/investment
- Franchise Direct – Snap Fitness (2025 FDD): https://www.franchisedirect.com/fitnessfranchises/snap-fitness-franchise-06321/ufoc
- 1851 Franchise – Snap Fitness: https://1851franchise.com/snap-fitness-franchise-costs-fees-profit-2730959
- Crunch Multistate FDD 9/2025 Item 19 (PDF): https://pub-22da695f2b6542a48e234bc59bc67d23.r2.dev/item19/57a44b3b-aaec-4a16-9f70-77e2b090f1d5.pdf
- Crunch franchise FAQ: https://www.crunch.com/franchise/faq
- Zee Report – Crunch (2026 FDD Item 7): https://zeereport.com/reports/crunch-fitness-franchise-cost
- FranchiseVS – Crunch (2025 FDD Item 7): https://franchisevs.com/franchise/crunch
- VetMyFranchise – Crunch: https://vetmyfranchise.com/blog/crunch-fitness-franchise-cost
- FranchiseDepth – Crunch (2026 FDD issue date): https://franchisedepth.com/franchise/crunch/
- Franchise Direct – Gold's Gym (2026 FDD): https://www.franchisedirect.com/fitnessfranchises/golds-gym-franchise-07663/ufoc
- 1851 Franchise – Gold's Gym: https://1851franchise.com/golds-gym-franchise-costs-fees-profit-data-2733313
- 1851 Franchise – Workout Anytime: https://1851franchise.com/workout-anytime-franchise-deep-dive-costs-fees-profit-2731602
- Zee Report – Workout Anytime: https://zeereport.com/reports/workout-anytime-franchise-cost
- Franzy – Retrofitness: https://franzy.com/franchises/retrofitness
- Franchise Direct – UFC GYM (2026 FDD): https://www.franchisedirect.com/fitnessfranchises/ufc-gym-franchise-company-franchise-09772/ufoc
- Franchise Chatter – UFC GYM review (2025 FDD): https://www.franchisechatter.com/2026/03/17/ufc-gym-franchise-review-2026-costs-fees-news-average-revenues-and-or-profits/
- Franchise Direct – Orangetheory (2026 FDD): https://www.franchisedirect.com/fitnessfranchises/orangetheory-fitness-franchise-09691/ufoc
- Orangetheory international opportunities: https://www.orangetheory.com/en-us/international-opportunities
- Franchise Direct – F45 (2025 FDD): https://www.franchisedirect.com/f45-training-franchise-cost-fees/ufoc
- VetMyFranchise – F45: https://vetmyfranchise.com/blog/f45-training-franchise-cost
- Franchise Direct – 9Round (2026 FDD): https://www.franchisedirect.com/fitnessfranchises/9round-franchise-07263/ufoc
- 9Round – What it takes: https://9round.com/fitness-franchises/what-it-takes
- Franchise Direct – Club Pilates (2026 FDD): https://www.franchisedirect.com/fitnessfranchises/club-pilates-franchise-13309/ufoc
- VetMyFranchise – Club Pilates: https://vetmyfranchise.com/blog/club-pilates-franchise-cost
- Franchise Chatter – Burn Boot Camp (2024 FDD): https://www.franchisechatter.com/?p=109804
- Burn Boot Camp – cost page (2026 FDD): https://burnbootcamp.com/franchise/how-much-does-it-cost-to-own-a-burn-boot-camp-franchise

### SEC / annual reports / company releases
- Planet Fitness FY2025 10-K: https://www.sec.gov/Archives/edgar/data/1637207/000163720726000011/plnt-20251231.htm
- Planet Fitness 2025 Investor Day (8-K exhibit): https://www.sec.gov/Archives/edgar/data/1637207/000163720725000059/planetfitnessincinvestor.htm
- PF Q1 2025 earnings call transcript: https://allmind.ai/earnings/event/bt_PLNT_2025_Q1
- PF Q4 2025 earnings call transcript: https://allmind.ai/earnings/event/bt_PLNT_2025_Q4
- Life Time FY2025 10-K: https://www.sec.gov/Archives/edgar/data/1869198/000186919826000010/lth-20251231.htm
- Pinnacle Bidco plc (PureGym) Annual Report 2018: https://s25.q4cdn.com/171963401/files/doc_financials/2018/ar/pinnacle-bidco-plc-2018-annual-report.pdf
- The Gym Group FY2025 results (RNS): https://www.ticker.app/lse/GYM/rns/2026-03-11/The-Gym-Group-PLC-2025-Full-Year-Results/1143W

### Club openings and press
- NEREJ – PF Worcester: https://nerej.com/planet-fitness-opens-13-605-s-f-location-in-mercantile-center
- Patch – PF Lakewood: https://patch.com/washington/lakewood-jblm/planet-fitness-opens-lakewood
- EP Local News – PF Eden Prairie: https://eplocalnews.org/?p=91154
- KIRO 7 – PF Puyallup: https://www.kiro7.com/news/local/planet-fitness-expands-adding-second-location-puyallup/LCMNPOZZMNERZFPVPEMGUST3RE/
- What Now – PF Sammamish: https://whatnow.com/?p=407268
- WDIO – PF Duluth: https://www.wdio.com/?p=218028
- REBusiness – PF Detroit (2015): https://rebusinessonline.com/planet-fitness-opens-two-new-detroit-area-locations/
- Community Impact – OTF Riverstone: https://communityimpact.com/sugar-land-missouri-city/business/orangetheory-fitness-to-open-riverstone-location-dec-14/
- Greater Long Island – OTF Bay Shore: https://greaterlongisland.com/?p=20261
- Tribeca Citizen – OTF Tribeca: https://tribecacitizen.com/2023/09/12/sneak-peek-orangetheory-fitness/
- Community Impact – OTF Highland Village: https://communityimpact.com/houston/heights-river-oaks-montrose/impacts/2019/11/13/orangetheory-opens-highland-village-location
- PureGym Leeds City Centre South: https://one.puregym.com/gyms/leeds-city-centre-south
- PureGym equipment page: https://puregym.com/equipment
- Leamington Observer – PureGym (2019): https://leamingtonobserver.co.uk/news/look-around-leamingtons-newest-gym/
- Health Club Management – The Gym Group RFP (2014): https://www.healthclubmanagement.co.uk/health-club-management-news/The-Gym-Group-targets-equipment-giants-for-new-supply-proposals/311111

### Government / association / vendor
- IRS Publication 946 (2025): https://www.irs.gov/pub/irs-pdf/p946.pdf
- Health & Fitness Association homepage: https://www.healthandfitness.org/
- HFA 2026 Fitness Industry Benchmarking Report (members-only): https://www.healthandfitness.org/2026-fitness-industry-benchmarking-report/
- Atlantis Strength – commercial gym equipment cost: https://atlantisstrength.com/build-yourself/commercial-gym-equipment-cost
- PushPress – gym equipment & floorplan guide: https://www.pushpress.com/blog/gym-equipment-and-floorplan-guide
