# Verification log: price_strength slice

- Checked: 2026-10-28 by an adversarial fact-checker.
- Method:
  - Exact variant prices came from each Shopify store's public `/products/<handle>.js` endpoint, using `curl` plus a parser. Stores: REP, Life Fitness, Hoist, Fitness Superstore (FSS), Prime, Titan, Bells of Steel, Torque, Relink and two Hoist dealers.
  - Rogue prices came from JSON-LD offers and visible page text.
  - I downloaded full catalogs to recompute aggregate statistics: AKFIT (1,462 products), FSS (3,750), CTX (777), Hoist (673) and Life Fitness (331).
  - Raw files are in `scratchpad/verify_ps/dl/`. Scripts are in `scratchpad/verify_ps/scripts/`.
  - WebFetch returned HTTP 429 twice, so I used direct fetches instead. I ran two WebSearches: Matrix G3-S10 and Hoist CF-3364.

## Result in one line
- **Transcription is excellent.** About 60 anchor listings across 11 storefronts matched the live source to the cent.
  - Every median I recomputed was correct (about 12 tier values).
  - The CTX refurb median and the AKFIT/FSS ratio reproduced from the full catalogs.
- **One category is wrong:** "chrome/pro-style dumbbells" is built on a misclassified product.
- **The main risk is the source mix, not transcription:**
  - Commercial and premium tiers use list/MSRP prices. Many of these are quote-only: Hoist shows "Contact Sales Team", and Prime is "NOT FOR ONLINE SALE / GET A QUOTE".
  - Nautilus (FSS) and Titan anchors are street or sale prices.

## Datapoint checks

| Datapoint | Claimed | Verdict | Evidence (live, 2026-10-28) |
|---|---|---|---|
| power_rack.listed_value | $799.94 | confirmed | REP PR-4000 (Pre-Selected) `.js`: 79994 cents, both colours. |
| power_rack.listed_commercial | $1,830 | confirmed | Rogue power-racks page: "Rogue RM-4 Monster Rack 2.0 $1,830.00". The other anchors on the same page also match: RM-6 $2,855, R-3 $870, RML-390 $1,015, Monster Lite Half $1,425, Collegiate Half $1,600. |
| power_rack.listed_premium | $4,657 | confirmed | LF `.js`: HS HD Athletic NX Power Rack $4,657. |
| power_rack.frame_price_commercial | $2,950 | confirmed (caveat) | All 6 anchors verified; the median of $2,972.5 rounds to $2,950. Caveats:<br>• Hoist CF-3364 is the `-gsa` listing, tagged GSA and NoPricing.<br>• Two dealers (banditfitness.com, thefitnessoutlet.com) sell it at **$2,782** with a compare-at of $3,090. $3,090 is therefore list, and street is 10% lower; the median at street is about $2,800.<br>• The AKFIT anchors (Torque TR2 $5,443, Nautilus cage $5,358) match. |
| power_rack.station_price_commercial | $4,400 | confirmed (assumption flagged) | Frame $2,950 + bar $310 + 350 lb × $3.10 + collars $55. The REP Equalizer urethane 355 lb set is $1,107.99 ($3.12/lb), and the Ohio Bar is $305; both verified. The **350 lb of plates per rack is an unsourced modeling assumption.** |
| chest_press.listed_commercial | $5,246 | confirmed | LF Axiom Series Chest Press, both frame colours. |
| chest_press.listed_premium | $5,972 | confirmed | LF HS Select Chest Press. |
| chest_press.price_commercial | $5,050 | confirmed (caveat) | Anchors: LF $5,246; Hoist CL-3301 $4,890 and RS-2301 $5,805; FSS Nautilus Instinct $3,799 and Impact $5,899; Prime Hybrid $6,250; AKFIT Matrix Aura $6,612.53 (÷1.45 = $4,560). The median of 8 is $5,068.<br>Caveats:<br>• The Prime page prints "$6,250.00 … GET A QUOTE" and is tagged NOT FOR ONLINE SALE.<br>• The Hoist product page CTA is "Contact Sales Team"; the price appears only in the site's product cards.<br>• The tier mixes list prices (LF, Hoist, Prime) with FSS street prices. Nautilus is about 31% below AKFIT's $8,082 compare-at. |
| chest_press.price_premium | $7,050 | confirmed | HS Select $5,972, Insignia $8,424, Nautilus Inspiration $7,049 (FSS), Prime Evolution $6,600. The median is $7,049. |
| smith_machine.price_commercial | $5,450 | confirmed | LF Axiom Smith Rack $4,863; Hoist CF-3755 $6,050 and CF-3754 $7,395 (both NoPricing/GSA); AKFIT Matrix G1 Smith $4,440. The G1 is a genuine G1FW161 despite its "varsity" URL slug. The median is $5,456.5. |
| cable_crossover.price_commercial | $7,000 | confirmed | Hoist CMD-6180 $7,195 (NoPricing); Rogue CC-1 $6,725 (JSON-LD); REP Hyperion S1 $6,783.79 (base colours); Nautilus 9NP-M9201 $8,389. The median is $6,989. |
| functional_trainer.listed_commercial | $6,250 | confirmed | LF Axiom Dual Adjustable Pulley. Hoist HD-3000 $6,720 is also verified. |
| leg_press.listed_premium | $7,883 | confirmed | LF HS Plate Loaded Linear Leg Press. Hoist CF-3355 $7,395 is also verified. |
| iron_plates.rep_old_school_355_set | $1.92/lb | confirmed | "355lb Set" $681.99 (SKU WPS-1100-355-Group) = $1.921/lb. The page does not show set contents, so the price assumes a plate-only weight. |
| iron_plates.per_lb_value | $1.90/lb | confirmed (note) | Verified: Rogue 45 lb pair $185, FF 350 lb set $589 and REP set. Titan's $84.97 is a sale price (compare-at $104.99 = $2.33/lb). Using the regular price leaves the median at $1.89. |
| rubber_hex_dumbbells.rep_5_100_set | $1.76/lb | confirmed | "5-100lb Set" $3,699.99 ÷ 2,100 lb. |
| dumbbell_set_full.station_price_value | $5,000 | confirmed | $3,699.99 plus 2 × REP Commercial Dumbbell Rack Two-Tier at $649.99. |
| dumbbell_set_full.station_price_premium | $20,150 | confirmed | HS 4-Sided Urethane sets: 5-50 $5,256, 55-75 $5,144, 80-100 $6,262 (sum $16,662). Sets are pairs: the 5–50 singles total ×2 = $5,556. Plus the HS Two Tier rack at $1,756 × 2. |
| urethane_dumbbells.rogue_5_100_set | $4.28/lb | confirmed | Rogue Urethane Dumbbell Set 5LB-100LB $8,995. The 105-150 set at $9,950 also matches. |
| bumper_plates.rogue_echo_260_set | $2.24/lb | confirmed | "$583.00 … (2) Each of 10-15-25-35-45LB" = 260 lb. |
| olympic_barbell.price_commercial | $310 | confirmed | Rogue Ohio Bar Black Zinc $305 and Torque Force $305 verified. The median of 6 is $310. |
| smith_machine.price_value | $2,250 | confirmed (note) | Anchors match: Titan $1,799.97, BoS $1,423.99, Body-Solid $2,660, FF $3,199.<br>• Titan's price is a sale (compare-at $2,249.99).<br>• The BoS unit is out of stock.<br>• At Titan's regular price the median is about $2,450. |
| adjustable_bench.price_value | $510 | confirmed | REP AB-3000 2.0 $349.99, AB-5200 2.0 $549.99, Rogue Adjustable Bench $595. The median of 6 is $511. |
| lifting_platform.station_price_premium | $8,850 | confirmed (note) | HS Traditional Wood 6x8 stand-alone $6,231; HS premium bumpers, 260 lb built as 4×25 + 2×35 + 2×45 = $1,804; HS WL bar $718. The HS 6x8 rubber platform is $910 (a $3,533 build) and the Impact Suppression platform is $6,346. The median of the three HS 6x8 platforms is $6,231, which is consistent with the report's method. |
| dealer.ak_to_lower48_ratio | 1.49 | confirmed (caveat) | Recomputed on 59 model-number matches: **median 1.495**.<br>• 53 of 59 matches fall within 1.38–1.54. The outliers are platforms (1.72–2.50) and the Instinct Triceps (1.62).<br>• The ÷1.45 factor is applied to **Matrix/Watson/Rogers** without any same-SKU check. The only cross-check is a search-summary price for the Matrix Aura chest press ($3,895–4,708), which brackets AK÷1.45 = $4,560.<br>• Relink's JSON shows a $10,000 placeholder, and Cenmed returned 403. |
| refurb.ctx_selectorized_band | $2,495 | confirmed | Live CTX prices: HS Select Chest Press $1,995, Hoist Club Line Chest Press $1,995, Cybex VR3 Arm Curl $1,495, HS Select Seated Leg Press $3,495. Full-catalog median of remanufactured single-station selectorized units: **$2,495** (n=144, IQR $1,995–2,995). |
| refurb.fss_selectorized_band | $3,899 | confirmed (note) | Live FSS prices: HS Select Chest Press reman $3,899, HS Smith $4,299, HS Select Seated Leg Press $4,399. Full-catalog median: **$3,999** (n=155, IQR $3,899–4,099). The band holds, but the central value is about $100 low. |
| refurb.reman_to_new_ratio | 0.50 | confirmed | The table arithmetic reproduces: FSS 0.63, CTX 0.40, pooled 0.50. I spot-checked 7 of the listings. |
| chrome_pro_style_dumbbells.titan_stainless_100_pair | $2.00/lb | **unsupported** | Titan describes the product as "Rubber Coated Hex Dumbbells with stainless steel straight handles", "ideal for home and garage gyms", tagged "Rubber Hex Dumbbells". It is not a chrome or pro-style dumbbell. Its $399.97 price is a weekly-deal sale (compare-at $484.99 = $2.42/lb). |
| chrome_pro_style_dumbbells.per_lb_value | $2.25/lb | **corrected → $2.71/lb** | Every anchor is a misclassified Titan rubber-hex sale price. The only real "pro-style" product found is the French Fitness Urethane Round Pro Style V2 set, 5–100 lb pairs, at $5,699 = $2.71/lb (FSS). No chrome dumbbell price was found. |

## Derivation issues to carry into the model
1. **List vs street.** Value-tier anchors include sale and street prices, such as Titan (20–25% below compare-at) and FSS Nautilus (about 31% below the MSRP AKFIT shows). Commercial and premium tiers are largely list/MSRP from LF, Hoist and Prime, and Hoist and Prime commercial lines are quote-only. Real purchase prices for commercial and premium are probably 10–30% below the modeled typical values. Example: the Hoist CF-3364 sells for $2,782 at dealers against a $3,090 list.
2. **Station builds rest on unsourced allocations:** 350 lb of plates per rack, 250 lb per bench, and 10 dumbbell pairs per rack (including the 105–150 lb pairs).
3. **The Hoist feed contains placeholders**, such as "PS- HALF RACK" at $1,000,000, and 89 items tagged NoPricing. Its prices should be treated as list, not transactable.

## Missing critical data
See `missing_critical_data` in the structured output. In short:
- discount from list to street price;
- freight and installation;
- the plate inventory that plate-loaded machines require;
- the basis for the per-station plate and rack allocations;
- new prices for Cybex, Technogym, Precor and Freemotion, and US lower-48 prices for Matrix;
- squat stands, specialty bars and rigs;
- durability rating and service life;
- stack and attachment upcharges.
