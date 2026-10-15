from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_endpoint_reports_liveness() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "netpulse-api"}


def test_ready_endpoint_does_not_claim_readiness_before_dependencies_exist() -> None:
    response = client.get("/api/v1/ready")

    assert response.status_code == 503
    assert response.json() == {
        "status": "not_ready",
        "checks": {
            "database": "not_configured",
            "scheduler": "not_started",
        },
    }
