# The planning service (FastAPI). Built from the repository root: it needs data/ as well as backend/.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    GYMPLANNER_DATA_DIR=/srv/data \
    PATH=/srv/backend/.venv/bin:$PATH

COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /usr/local/bin/uv

WORKDIR /srv/backend
COPY backend/pyproject.toml backend/uv.lock backend/README.md ./
COPY backend/src ./src
RUN uv sync --frozen --no-dev --no-editable
COPY data /srv/data

USER nobody
EXPOSE 8100
# A plan keeps a CPU busy for seconds: one worker per vCPU, each taking a few requests at a time.
# Past that a request gets a quick 503 rather than slowing every plan in progress.
CMD ["uvicorn", "gymplanner.api.app:app", "--host", "0.0.0.0", "--port", "8100", "--workers", "2", "--limit-concurrency", "6"]
