"""Merge data-synthesis fragments + bibliography into data/*.yaml.

Only bibliography entries actually referenced by some dataset are kept in sources.yaml.
"""
import json, sys
from pathlib import Path
import yaml

frag_dir, research_dir, data_dir = map(Path, sys.argv[1:4])
import re
KIND_RULES = [
    (r"derived", "derived"),
    (r"fdd|sec[ _]filing|filing|annual[ _]report|annual[ _]results|10-k|rns", "filing"),
    (r"standard|regulat|building[ _]code|code[ _]interpretation|design criteria|policy", "standard"),
    (r"peer|study|thesis|journal|position stand|meta-analysis|systematic|rct|conference|working[ _]paper|academic|student", "study"),
    (r"workout-app|app[ _]data|app data|community lift|lift database|app community", "app_data"),
    (r"dataset|statistics", "dataset"),
    (r"manual|spec|manufacturer|mfr|catalog", "manufacturer"),
    (r"retail|dealer|store|listing|refurb|product", "retailer"),
    (r"news|press|blog|trade|article|search|web[ _]page|summary|commentary|newsletter", "article"),
    (r"industry|survey|report|analytics|association|planning|operator|insurer|guide|franchisor|company|participation|poll", "industry_report"),
]
def load(name):
    p = frag_dir / name
    return yaml.safe_load(p.read_text()) if p.exists() else None

def kind_of(k):
    k = (k or "").lower()
    for pattern, val in KIND_RULES:
        if re.search(pattern, k):
            return val
    return "article"

def dump(path, obj):
    path.write_text(yaml.safe_dump(obj, sort_keys=False, allow_unicode=True, width=100))

extra_sources = []
equipment = []
for name in ["equipment_cardio_functional.yaml", "equipment_free_weights.yaml", "equipment_machines.yaml"]:
    f = load(name)
    if f:
        equipment += f.get("equipment", [])
        extra_sources += f.get("extra_sources", []) or []
ex = load("exercises.yaml") or {}
extra_sources += ex.get("extra_sources", []) or []
beh = load("behavior.yaml") or {}
extra_sources += beh.pop("extra_sources", []) or []
space = load("space.yaml") or {}
extra_sources += space.pop("extra_sources", []) or []
costs = load("costs.yaml") or {}
extra_sources += costs.pop("extra_sources", []) or []
bench = load("benchmarks.yaml") or {}
extra_sources += bench.pop("extra_sources", []) or []
scen = load("scenarios.yaml") or {}
extra_sources += scen.pop("extra_sources", []) or []

refs = set() # Collect referenced source ids.
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("sources", "installation_sources") and isinstance(v, list):
                refs.update(v)
            else:
                walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)
for obj in (equipment, ex.get("exercises", []), beh, space, costs, bench):
    walk(obj)

bib = json.loads((research_dir / "bibliography.json").read_text())
sources, seen = [], set()
for s in bib:
    if s["id"] in refs and s["id"] not in seen:
        seen.add(s["id"])
        entry = {"id": s["id"], "title": s["title"] or s["id"], "publisher": s.get("publisher"),
                 "year": str(s["year"]) if s.get("year") else None, "url": s.get("url"),
                 "kind": kind_of(s.get("kind")), "accessed": "2026-10"}
        sources.append({k: v for k, v in entry.items() if v is not None})
for s in extra_sources:
    if s["id"] not in seen:
        seen.add(s["id"])
        s = dict(s)
        s["kind"] = kind_of(s.get("kind"))
        sources.append(s)
missing = sorted(refs - seen)

data_dir.mkdir(parents=True, exist_ok=True)
dump(data_dir / "equipment.yaml", {"version": 1, "equipment": equipment})
dump(data_dir / "exercises.yaml", {"version": 1, "exercises": ex.get("exercises", [])})
dump(data_dir / "behavior.yaml", {"version": 1, **{k: v for k, v in beh.items() if k != "version"}})
dump(data_dir / "space.yaml", {"version": 1, **{k: v for k, v in space.items() if k != "version"}})
dump(data_dir / "costs.yaml", {"version": 1, **{k: v for k, v in costs.items() if k != "version"}})
dump(data_dir / "benchmarks.yaml", {"version": 1, **{k: v for k, v in bench.items() if k != "version"}})
dump(data_dir / "scenarios.yaml", {"version": 1, **{k: v for k, v in scen.items() if k != "version"}})
dump(data_dir / "sources.yaml", {"version": 1, "sources": sources})
print(f"equipment={len(equipment)} exercises={len(ex.get('exercises', []))} sources={len(sources)} missing_refs={missing}")
