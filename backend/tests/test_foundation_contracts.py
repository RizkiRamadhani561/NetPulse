"""Static safety contracts for the Phase 0 network lab and local preview."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_default_services_only_publish_ports_on_loopback() -> None:
    compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")

    assert '"127.0.0.1:8000:8000"' in compose
    assert '"127.0.0.1:3000:3000"' in compose
    assert "./frontend/src:/app/src:ro" in compose
    assert "./frontend/.storybook:/app/.storybook:ro" in compose
    assert not any(
        line.strip() == "- ./frontend:/app" for line in compose.splitlines()
    )


def test_lab_overlay_is_internal_and_has_no_published_ports() -> None:
    overlay = (ROOT / "docker-compose.lab.yml").read_text(encoding="utf-8")

    assert "internal: true" in overlay
    assert "lab_internal" in overlay
    assert "lab-http:" in overlay
    assert "snmp-simulator:" in overlay
    assert overlay.count("profiles: [lab]") == 2
    assert "ports:" not in overlay


def test_snmp_fixture_contains_well_formed_synthetic_records() -> None:
    fixture = ROOT / "lab/fixtures/snmp/system.snmprec"
    records = [
        line.split("|")
        for line in fixture.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert records
    assert all(len(record) == 3 for record in records)
    assert all(record[0].startswith("1.3.6.1.2.1.1.") for record in records)
    assert all(record[1].isdigit() for record in records)
    values = " ".join(record[2] for record in records).lower()
    assert "netpulse" in values
    assert not any(
        word in values for word in ("password", "community string", "real router")
    )


def test_default_lab_scenario_is_declarative_and_uses_lab_hosts() -> None:
    scenario = (ROOT / "lab/scenarios/default.yml").read_text(encoding="utf-8")

    assert scenario.count("executable: false") == 2
    assert "http://lab-http:8080/health" in scenario
    assert "snmp-simulator:1161/udp" in scenario
    assert "execution is not implemented in Phase 0" in scenario
