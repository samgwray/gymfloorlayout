"""Extract research + verification results from the workflow journal into per-topic JSON files,
and build a merged, de-duplicated bibliography with stable slug ids."""
import json, re, sys
from pathlib import Path
from urllib.parse import urlsplit

journal, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)
labels, results = {}, {}
for line in journal.read_text().splitlines():
    d = json.loads(line)
    if d.get("type") == "started":
        labels[d["agentId"]] = d["label"]
    elif d.get("type") == "result":
        results[d["agentId"]] = d["result"]

topics = {}
for agent_id, label in labels.items():
    if agent_id not in results:
        continue
    kind, key = label.split(":", 1)
    topics.setdefault(key, {})[kind] = results[agent_id]

def norm_url(u):
    if not u:
        return ""
    p = urlsplit(u.strip())
    host = p.netloc.lower().removeprefix("www.")
    return f"{host}{p.path.rstrip('/')}".lower() + (f"?{p.query}" if p.query else "")

STOP = {"the", "a", "an", "of", "and", "for", "to", "in", "on", "with", "by", "at", "from", "is", "vs",
        "inc", "llc", "ltd", "co", "com", "www", "https", "http", "page", "pdf"}

def words(text):
    return [w for w in re.findall(r"[a-z0-9]+", (text or "").lower()) if w not in STOP]

def make_slug(src, maxlen=44):
    pub = words(src.get("publisher"))[:3]
    title = [w for w in words(src.get("title")) if w not in pub][:5]
    year = str(src.get("year") or "")
    year = year if re.fullmatch(r"(19|20)\d\d", year) else ""
    parts = pub + title
    out = []
    for w in parts:
        if len("-".join(out + [w])) > maxlen - (5 if year else 0):
            break
        out.append(w)
    if year and year not in out:
        out.append(year)
    return "-".join(out) or "source"

merged, by_url, mapping = [], {}, {}
used = set()
for key in sorted(topics):
    research = topics[key].get("research")
    if not research:
        continue
    for src in research.get("sources", []):
        u = norm_url(src.get("url"))
        old = f"{key}:{src['id']}"
        if u and u in by_url:
            mapping[old] = by_url[u]
            continue
        base = make_slug(src)
        sid, n = base, 2
        while sid in used:
            sid, n = f"{base}-{n}", n + 1
        used.add(sid)
        entry = {
            "id": sid,
            "title": src.get("title"),
            "publisher": src.get("publisher"),
            "year": src.get("year"),
            "url": src.get("url"),
            "kind": src.get("kind"),
            "fetched": src.get("fetched"),
            "topics": [key],
        }
        merged.append(entry)
        mapping[old] = sid
        if u:
            by_url[u] = sid
    for src in research.get("sources", []):
        sid = mapping[f"{key}:{src['id']}"]
        e = next(m for m in merged if m["id"] == sid)
        if key not in e["topics"]:
            e["topics"].append(key)

for key, parts in topics.items():
    r = parts.get("research")
    if r:
        for dp in r.get("datapoints", []):
            dp["source_ids"] = [mapping.get(f"{key}:{s}", f"UNMAPPED:{s}") for s in dp.get("source_ids", [])]
    (out_dir / f"{key}.json").write_text(json.dumps(parts, indent=1))

(out_dir / "bibliography.json").write_text(json.dumps(merged, indent=1))
(out_dir / "source_map.json").write_text(json.dumps(mapping, indent=1))
kinds = {}
for m in merged:
    kinds[m["kind"]] = kinds.get(m["kind"], 0) + 1
print("topics:", {k: sorted(v) for k, v in topics.items()})
print("sources:", len(merged), kinds)
