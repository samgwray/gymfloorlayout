# Methodology brief (source of truth for the /methodology page prose)

The engine answers: "Given this floor area and budget, which equipment, how many of each, and where?"
It runs five stages. Every parameter comes from data/ (served by GET /api/methodology, /api/sources),
so the page should render live values from the API rather than hard-coding numbers.

1. Who is on the floor at the busiest hour (demand/occupancy.py)
   - Design-peak users = training floor area / (1000 / peak_users_per_1000_sqft), i.e. ~100 sq ft of
     training floor per person at a busy-day peak (campus weight-room head counts, operator guidance).
   - If the user gives a member count: members x daily_visit_rate x peak_concurrency_share x
     design_day_factor; the smaller of the two estimates is used (demand beyond what the floor holds
     comfortably cannot be served by adding equipment).
   - Never above the building-code occupant load (IBC Table 1004.5: exercise rooms 50 gross sq ft/person).
   - A share of floor time is spent between stations (idle_share), so active users = peak x (1 - idle_share).

2. What they want to do (demand/model.py)
   - The average member's floor time splits across modalities: cardio, barbell, dumbbell, machine, cable,
     bodyweight, functional, mobility (profile modality_share; "General fitness" is the data-based average,
     other profiles adjust it for strength-focused, cardio/wellness, functional and amenity gyms).
   - Within a modality, each exercise's share of time = popularity (workout-logging app data) x block
     minutes (how long one exercise block ties up a station: sets x (work + rest) + setup).
   - Result: offered load in Erlangs per exercise = average number of people who want it at the same time.

3. How equipment serves that demand (selection/evaluator.py)
   - Each exercise can be done several ways ("routes"), each using one or more pieces of equipment at once
     (dumbbell bench press = dumbbells + bench) and rated 0-1 for fit (barbell bench press on a bench station
     = 1.0, in a power rack with an adjustable bench ~0.95, on a Smith machine ~0.6).
   - Members try their best route. If its equipment is busy or not in the gym, they move to the next route
     only as willingly as it fits: the chance of trying a fallback equals its fit relative to the route
     before it (nearly everyone accepts a power rack + bench for a bench press at 0.95; few runners settle
     for a rower). The rest wait or skip the exercise, which counts as unmet demand at the peak. This stops
     cheap, poor substitutes from soaking up demand that members would never really move.
   - A member's fallback is judged knowing why the first choice failed: if the dumbbells were busy for the
     bench-and-dumbbells route, they are still busy for a dumbbells-only fallback.
   - Busy probability per equipment type comes from the Erlang loss formula (M/G/c/c, insensitive to how
     long sets take beyond the mean); the coupled system is solved as a loss network with the reduced-load
     (Erlang fixed-point) approximation.
   - Objective = quality-weighted demand served. Shown as "Demand served".

4. Choosing equipment (selection/optimizer.py)
   - Greedy multi-dimensional knapsack: at each step score every possible next purchase in one vectorized
     evaluation; rank by value gained per unit of scarce resource (cost / remaining budget + area / remaining
     area); bundles let complementary items (bench + dumbbells) be bought together; prerequisites respected.
   - Swap search afterwards: drop the weakest unit, refill, keep if better.
   - Stopping rule: stop buying when the next purchase returns less than 4% of the plan's average value per
     dollar so far (or serves a negligible share of demand). Leftover money is reported, with the reason
     (floor full vs. peak demand met) and the next upgrades a bigger budget would buy.
   - Why small gyms get variety and big gyms get redundancy: each extra unit of a type serves less new
     demand than the last (carried load is concave in station count). With light demand, the first unit of
     a new type beats a second unit of an existing one; with heavy demand, queues form at popular stations
     and extra units win.
   - Area per unit = footprint + half of each clearance (clearance zones can overlap neighbours' clearance
     and aisles), checked against training floor x packing efficiency; the layout then verifies it for real.

5. Laying out the floor (layout/)
   - Zones from the entrance to the back: cardio, machines & cables, free weights (heavy flooring, mirrors,
     dumbbells on the back wall), functional/turf, stretching.
   - Rows with real footprints and safety clearances (ASTM F2115 / ISO 20957 treadmill run-off zone behind,
     side clearances, manufacturer guidance), a main aisle from the entrance, walkways >= 36 in (ADA accessible
     route), every machine approachable from an aisle. If something does not fit, the optimizer re-plans with
     less space so the plan never lists equipment the floor cannot hold.

6. Checking the plan (simulation/)
   - Discrete-event simulation of the busiest hours: members arrive at random, pick exercises in proportion
     to demand, wait up to ~3 minutes for their preferred station, then substitute or skip. Reports average
     and 90th-percentile wait, first-choice / substituted / skipped shares and the busiest equipment.

7. Costs
   - Equipment by grade (value, commercial, premium, refurbished), freight & installation as a share of
     equipment, flooring per sq ft by zone (blended by where members spend their time).

8. Limits
   - Planning estimates. Prices vary by region, dealer and promotions; layouts are schematic and need a
     designer's and code official's review (egress, electrical, structure). The model plans for the
     design-peak hour, not for classes or special events.
