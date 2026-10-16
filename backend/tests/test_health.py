import asyncio

import httpx
from app.main import app


async def get_response(path: str) -> httpx.Response:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        return await client.get(path)


def test_health_endpoint_reports_liveness() -> None:
    response = asyncio.run(get_response("/api/v1/health"))

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "netpulse-api"}


def test_ready_endpoint_does_not_claim_readiness_before_dependencies_exist() -> None:
    response = asyncio.run(get_response("/api/v1/ready"))

    assert response.status_code == 503
    assert response.json() == {
        "status": "not_ready",
        "checks": {
            "database": "not_configured",
            "scheduler": "not_started",
        },
    }


def test_healthz_alias_stays_available_for_container_healthcheck() -> None:
    response = asyncio.run(get_response("/healthz"))

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "netpulse-api"}
