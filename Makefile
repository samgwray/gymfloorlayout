API_PORT ?= 8100
WEB_PORT ?= 3100

.PHONY: setup api web dev test test-api test-web lint format openapi data-check

setup:
	cd backend && uv sync
	cd frontend && npm install

api:
	cd backend && .venv/bin/uvicorn gymplanner.api.app:app --reload --port $(API_PORT)

web:
	cd frontend && API_URL=http://127.0.0.1:$(API_PORT) npx next dev -p $(WEB_PORT)

dev:
	$(MAKE) -j2 api web

test: test-api test-web

test-api:
	cd backend && .venv/bin/python -m pytest

test-web:
	cd frontend && npm run typecheck && npm run lint

lint:
	cd backend && .venv/bin/ruff check src tests && .venv/bin/mypy src tests
	cd frontend && npm run lint

format:
	cd backend && .venv/bin/ruff check --fix src tests

openapi: # Regenerate the OpenAPI spec and frontend API types.
	cd backend && .venv/bin/python -m gymplanner.api.export_openapi openapi.json
	cd frontend && npm run gen:api

data-check: # Validate the datasets and print a summary.
	cd backend && .venv/bin/python -m gymplanner.catalog
