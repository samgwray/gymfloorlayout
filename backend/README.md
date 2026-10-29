# gymfloorlayout backend

This backend is a FastAPI app that takes a training floor area and a budget to make an equipment plan, a floor layout and a simulated peak hour.
For personalization please reach out to me at samgwray@gmail.com .

## Run

```bash
uv sync
.venv/bin/uvicorn gymplanner.api.app:app --port 8100 # http://127.0.0.1:8100/docs
.venv/bin/python -m gymplanner.catalog # validate ../data and print a summary
```

`GYMPLANNER_DATA_DIR`, `GYMPLANNER_CORS_ORIGINS` and `GYMPLANNER_SIM_SEED` override the data
folder (default `../data`), the allowed origins (default port 3100) and the simulation seed.

## Packages (`src/gymplanner/`)

| Package | What it does |
| --- | --- |
| `catalog/` | Load and validate the YAML datasets, check cross-references, fingerprint the data |
| `demand/` | Design-peak occupancy and offered load (Erlangs) per exercise |
| `queueing/` | Erlang B, scalar and vectorized |
| `selection/` | Route table, loss-network evaluator, greedy and swap-search optimizer, explanations |
| `layout/` | Row and wall layouts of the floor, the placement search, the hard-rule validator |
| `simulation/` | Discrete-event replay of the design hour |
| `planning/` | Request to response: room, fitting the plan to the floor, reasons, wording |
| `api/` | App, routes and response schemas |

`planning/fitting.py` is where the optimizer meets the layout: the optimizer budgets space with
an estimate, so the plan is laid out, re-planned on less area while units are left out, grown
while the budget buys more that fits, and its upgrade list is checked the same way.
`planning/reasons.py` words why a plan stops where it does (the floor, the budget, demand met,
too few members, exclusions) from what it can still buy.

## Checks

```bash
.venv/bin/python -m pytest -q # unit, property and end-to-end tests
.venv/bin/ruff check src tests
.venv/bin/mypy src tests # strict
```

`make format` applies lint fixes while keeping comments inline with one preceding space.

Most tests use the small catalog in `tests/fixtures/mini_data`. `tests/test_calibration.py`
and `tests/test_small_floors.py` run the real datasets: the sample scenarios against the
validation bands in `data/benchmarks.yaml`, and small or narrow floors end to end.

After changing a response model, regenerate `openapi.json` from `backend/`:

```bash
.venv/bin/python -m gymplanner.api.export_openapi openapi.json
```
