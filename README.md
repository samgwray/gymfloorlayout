# gymfloorlayout

gymfloorlayout takes a floor area and a budget, and creates an equipment list, a cost breakdown, a floor layout and
an estimate of business at peak times. Can be used for free at gymfloorlayout.com. For modifications or consulting, contact me directly
at samgwray@gmail.com .

It uses data from public studies to determine the optimal equipment based on what users want while also making sure all
body parts can be encompassed for any individual to train. This is particularly important for a small gym, like a hotel,
or a large gym with a very large budget. This site is not optimal for individuals building a home gym, as that is based solely
on what you like; for that, I offer consulting services.

This repo contains the Python planning engine, FastAPI API and datasets. The frontend isn't
included. You can use it for free at gymfloorlayout.com.

## Try it

You'll need Python 3.11+ and `uv`. From the repo root:

```bash
cd backend
uv sync
.venv/bin/uvicorn gymplanner.api.app:app --reload --port 8100
```

Open [localhost:8100/docs](http://localhost:8100/docs) to try the API, or send a request from
another terminal:

```bash
curl -sS http://localhost:8100/api/plan \
  -H 'Content-Type: application/json' \
  -d '{"area_sqft": 3750, "budget_usd": 195000}'
```

The response is JSON with equipment quantities, costs, layout coordinates, estimated waits
and suggested upgrades. Layout coordinates are in inches. Flooring and installation are
included by default.

You can also set a gym focus (`profile`), equipment `grade`, room dimensions, ceiling height,
member count or equipment exclusions. `GET /api/meta` lists the available options and sample
scenarios; the interactive docs explain all the fields.

## How it works

1. Estimate peak occupancy and which exercises people will want to do.
2. Choose equipment within the budget and space available, accounting for busy stations and
   alternative ways to do each exercise.
3. Arrange it into zones with equipment clearances and aisles, adjusting the selection until
   it fits.
4. Simulate a busy period to estimate waits, substitutions and bottlenecks.

## Where the data comes from

The planner reads the YAML files in [`data/`](data/), which currently cover 72 equipment types
and 111 exercises. This could be adjusted for your gym by accounting for specific equipment or demographics.

The bibliography is in [`data/sources.yaml`](data/sources.yaml). Records cite source IDs;
estimates and combined values also have `derived` entries explaining the assumptions.
These are planning estimates, and the prices and layout still need checking for a real gym.
See [`data/README.md`](data/README.md) for the file guide and units, and
[`docs/research/`](docs/research/) for the research and verification notes.

## Working on it

From `backend/`, after `uv sync`:

```bash
.venv/bin/python -m gymplanner.catalog # validate data and source references
.venv/bin/python -m pytest # run backend tests
```

The engine lives in [`backend/src/gymplanner/`](backend/src/gymplanner/).
[`backend/README.md`](backend/README.md) has the code map, settings and development checks.
