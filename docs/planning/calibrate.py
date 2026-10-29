"""Run scenarios and a size x budget grid; compare with validation bands restated for the
training floor. Usage:
python calibrate.py [--grid] [--detail ID]"""
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "backend" / "src"))
from gymplanner.api.schemas import PlanRequest # noqa: E402
from gymplanner.catalog import load_catalog # noqa: E402
from gymplanner.planning import create_plan # noqa: E402

cat = load_catalog(REPO_ROOT / "data")
NON_PIECES = {"mobility"}


def band_for(sqft):
    """The band, restated for the training floor, whose sizes (widened a little) take in this floor."""
    for b in cat.validation_bands:
        on_floor = b.on_training_floor()
        if on_floor.total_sqft.low * 0.8 <= sqft <= on_floor.total_sqft.high * 1.25:
            return on_floor
    return None


def training_share(sqft):
    """Training share of the band whose typical gym's training floor is nearest this size."""
    return min(cat.validation_bands, key=lambda b: abs(b.total_sqft.typical * b.training_share - sqft)).training_share


def flag(value, rng):
    if rng is None:
        return ""
    if value < rng.low:
        return "LOW"
    if value > rng.high:
        return "HIGH"
    return "ok"


def run(label, area, budget, profile="general", grade="commercial", show=False, **kw):
    t = time.perf_counter()
    r = create_plan(PlanRequest(area_sqft=area, budget_usd=budget, profile=profile, grade=grade, **kw), cat, seed=7)
    ms = (time.perf_counter() - t) * 1000
    pieces = sum(i.units for i in r.items if i.category not in NON_PIECES)
    cardio = sum(i.units for i in r.items if i.category == "cardio")
    per_k = pieces / r.space.training_sqft * 1000
    usd_sqft = (r.costs.equipment_usd + r.costs.installation_usd) / r.space.training_sqft
    cardio_share = cardio / pieces if pieces else 0
    b = band_for(r.space.training_sqft)
    dropped = [w for w in r.warnings if w.startswith("Left out")]
    print(
        f"{label:28s} {area:>7,.0f}sqft ${budget:>9,.0f} {profile[:8]:8s} | pieces {pieces:3d} ({per_k:5.1f}/1k {flag(per_k, b and b.pieces_per_1000_sqft):4s}) "
        f"types {r.metrics.type_count:2d} | eq$/sqft {usd_sqft:5.1f} {flag(usd_sqft, b and b.equipment_usd_per_sqft):4s} | cardio {cardio_share:4.0%} {flag(cardio_share, b and b.cardio_share_of_pieces):4s} "
        f"| served {r.metrics.quality_served_share:4.0%}/{r.metrics.served_share:4.0%} cov {r.metrics.coverage_share:4.0%} | wait {r.simulation.mean_wait_min:4.1f}m skip {r.simulation.skipped_share:4.0%} "
        f"| left ${r.costs.remaining_usd:>8,.0f} | peak {r.demand.peak_users:5.1f} | {ms:6.0f}ms{' DROPPED' if dropped else ''}"
    )
    if show:
        for i in r.items:
            print(f"     {i.zone:12s} {i.name:42s} x{i.units:<3d} ${i.subtotal_usd:>10,.0f}  util {i.utilization:4.0%}  block {i.blocking:4.0%}")
        print("     warnings:", r.warnings)
        print("     upgrades:", [(" + ".join(f'{x.name} x{x.units}' for x in u.items), round(u.cost_usd), f"{u.gain_share:.2%}") for u in r.next_upgrades])
        print("     note:", r.upgrade_note)
        print("     coverage:", ", ".join(f"{c.label} {c.coverage:.0%}" for c in r.coverage))
    return r


if __name__ == "__main__":
    detail = sys.argv[sys.argv.index("--detail") + 1] if "--detail" in sys.argv else None
    for s in cat.scenarios:
        run(s.id, s.area_sqft, s.budget_usd, s.profile, s.grade, show=(detail == s.id or detail == "all"))
    if "--grid" in sys.argv:
        print()
        for area, per_sqft in [(600, 40), (1200, 35), (2500, 40), (4000, 35), (6000, 35), (10000, 35), (20000, 38), (35000, 38)]: # Training floors and equipment $ per sq ft of building; the building is the floor over its training share, as for the sample scenarios' budgets. Flooring adds about $6 per sq ft.
            building = area / training_share(area)
            for mult in (0.5, 1.0, 2.0):
                run(f"grid {mult}x", area, building * per_sqft * mult + area * 6)
