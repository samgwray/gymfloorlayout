"""FastAPI application factory."""

from __future__ import annotations

import math

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from gymplanner import __version__
from gymplanner.api.routes import router
from gymplanner.settings import get_settings


def json_safe(value: object) -> object:
    """``value`` with every non-finite float written out as text ('nan', 'inf'): JSON has no
    NaN or Infinity, so echoing such an input back as a number would fail the response."""
    if isinstance(value, float) and not math.isfinite(value):
        return str(value)
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [json_safe(item) for item in value]
    return value


async def _invalid_request(request: Request, exc: Exception) -> JSONResponse:
    """FastAPI's 422 for a request that fails validation, safe for any input it echoes."""
    errors = exc.errors() if isinstance(exc, RequestValidationError) else []
    return JSONResponse(status_code=422, content={"detail": json_safe(jsonable_encoder(errors))})


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="gymfloorlayout API",
        version=__version__,
        description=(
            "Chooses the equipment mix and floor layout for a gym from its square footage and "
            "budget, using peak-hour demand from member behavior data and an Erlang loss model."
        ),
    )
    app.add_middleware(GZipMiddleware, minimum_size=1024)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    app.add_exception_handler(RequestValidationError, _invalid_request)
    app.include_router(router)
    return app


app = create_app()
