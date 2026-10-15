"""Minimal API entry point for the NetPulse Phase 0 foundation."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="NetPulse API",
    description="Self-hosted network monitoring API — Phase 0 foundation.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json",
)


@app.get("/healthz", tags=["operations"], include_in_schema=False)
@app.get("/api/v1/health", tags=["operations"])
def health() -> dict[str, str]:
    """Return liveness only; this endpoint intentionally does not claim readiness."""
    return {"status": "ok", "service": "netpulse-api"}


@app.get("/api/v1/ready", tags=["operations"])
def readiness() -> JSONResponse:
    """Signal that application dependencies are not ready during Phase 0."""
    return JSONResponse(
        status_code=503,
        content={
            "status": "not_ready",
            "checks": {
                "database": "not_configured",
                "scheduler": "not_started",
            },
        },
    )
