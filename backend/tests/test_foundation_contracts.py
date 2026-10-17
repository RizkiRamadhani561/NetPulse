"""Static safety contracts for the Phase 0 network lab and local preview."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_default_services_only_publish_ports_on_loopback() -> None:
    compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")

    assert '"127.0.0.1:8000:8000"' in compose
    assert '"127.0.0.1:3000:3000"' in compose
    assert "./frontend/src:/app/src:ro" in compose
    assert "./frontend/.storybook:/app/.storybook:ro" in compose
    assert not any(line.strip() == "- ./frontend:/app" for line in compose.splitlines())


def test_read_only_api_persists_sqlite_only_in_the_named_data_volume() -> None:
    compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")

    api_service = compose.split("  api:\n", maxsplit=1)[1].split("\n  web:", maxsplit=1)[0]
    assert "read_only: true" in api_service
    assert "DATABASE_URL: ${DATABASE_URL:-sqlite:///./data/netpulse.db}" in api_service
    assert "- netpulse_data:/app/data" in api_service


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
        line.split("|") for line in fixture.read_text(encoding="utf-8").splitlines() if line.strip()
    ]

    assert records
    assert all(len(record) == 3 for record in records)
    assert all(record[0].startswith("1.3.6.1.2.1.1.") for record in records)
    assert all(record[1].isdigit() for record in records)
    values = " ".join(record[2] for record in records).lower()
    assert "netpulse" in values
    assert not any(word in values for word in ("password", "community string", "real router"))


def test_default_lab_scenario_is_declarative_and_uses_lab_hosts() -> None:
    scenario = (ROOT / "lab/scenarios/default.yml").read_text(encoding="utf-8")

    assert scenario.count("executable: false") == 2
    assert "http://lab-http:8080/health" in scenario
    assert "snmp-simulator:1161/udp" in scenario
    assert "execution is not implemented in Phase 0" in scenario


def test_gitleaks_job_can_read_pull_request_metadata() -> None:
    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    secrets_job = workflow.split("\n  secrets:\n", maxsplit=1)[1]
    permissions = secrets_job.split("\n    steps:\n", maxsplit=1)[0]

    assert "contents: read" in permissions
    assert "pull-requests: read" in permissions
    assert "security-events: write" in permissions


def test_browser_audit_uses_pinned_tools_and_upload_action() -> None:
    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert '"@axe-core/playwright": "4.14.0"' in workflow
    assert '"playwright": "1.64.1"' in workflow
    assert "node scripts/verify_ui.cjs" in workflow
    assert re.search(r"uses: actions/upload-artifact@[0-9a-f]{40}", workflow)


def test_api_runtime_smoke_is_part_of_ci_and_full_verification() -> None:
    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    runner = (ROOT / "scripts/verify_runner.py").read_text(encoding="utf-8")

    assert "API runtime smoke without Docker" in workflow
    assert "uv run --locked --extra dev python ../scripts/smoke_api.py" in workflow
    assert "scripts/smoke_api.py" in runner


def test_windows_quick_verification_runs_in_ci() -> None:
    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "runs-on: windows-latest" in workflow
    assert "shell: pwsh" in workflow
    assert "run: ./scripts/verify.ps1 -Mode quick" in workflow


def test_environment_template_covers_all_documented_runtime_variables() -> None:
    template = (ROOT / ".env.example").read_text(encoding="utf-8")
    documented = {
        "APP_ENV",
        "SECRET_KEY",
        "ENCRYPTION_KEY",
        "DATABASE_URL",
        "ALLOWED_ORIGINS",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "DEMO_MODE",
        "ALLOW_PUBLIC_SCAN",
        "DEFAULT_TIMEZONE",
        "LOG_LEVEL",
        "RETENTION_RAW_DAYS",
        "CHECK_CONCURRENCY",
        "ENABLE_UPDATE_CHECK",
        "ENABLE_MIKROTIK_WRITE",
        "TRUSTED_PROXIES",
        "SYSLOG_PORT",
        "TRAP_PORT",
        "VAPID_PUBLIC_KEY",
        "VAPID_PRIVATE_KEY",
        "OIDC_ISSUER",
        "OIDC_CLIENT_ID",
        "OIDC_CLIENT_SECRET",
        "SMTP_HOST",
        "SMTP_USER",
        "SMTP_PASSWORD",
        "ENABLE_AI",
        "AI_PROVIDER",
        "AI_API_KEY",
    }
    present = {
        line.split("=", maxsplit=1)[0].strip()
        for line in template.splitlines()
        if line.strip() and not line.lstrip().startswith("#") and "=" in line
    }

    assert documented <= present


def test_spec_index_local_markdown_links_resolve() -> None:
    index = ROOT / "docs/spec/INDEX.md"
    assert (ROOT / "PROMPT.md").is_file()

    links = re.findall(r"\]\(([^)]+\.md)\)", index.read_text(encoding="utf-8"))
    assert links
    missing = [link for link in links if not (index.parent / link).is_file()]
    assert not missing, f"broken local spec links: {missing}"


def test_github_actions_are_pinned_to_full_commit_shas() -> None:
    workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    uses_lines = [
        line.strip().split("uses:", maxsplit=1)[1].strip()
        for line in workflow.splitlines()
        if line.strip().startswith("uses:")
    ]

    assert uses_lines
    assert all(re.fullmatch(r"[^@\s]+@[0-9a-f]{40}", action) for action in uses_lines)
