# Traceability — Phase 0

Status meanings: ✅ verified with evidence; ⚠️ partial or waiting on an explicitly deferred gate; ❌ failed; ❓ not tested.

| ID | Acceptance criterion (Given/When/Then) | Code / artifact | Test / evidence | Status |
|---|---|---|---|---|
| OPS-01 | Given the API process is running, when /api/v1/health or /healthz is requested, then it returns liveness; when DB/scheduler are absent, /api/v1/ready returns 503 and does not claim readiness. | backend/app/main.py | backend/tests/test_health.py; previous passing baseline: [Actions run 38849910373](https://github.com/RizkiRamadhani561/NetPulse/actions/runs/38849910373). Latest coverage/mypy additions await CI. | ⚠️ |
| LAB-01 | Given the lab overlay is selected, when its Compose config is used, then synthetic HTTP/SNMP targets join only an internal lab network and no lab ports are published to the host. | docker-compose.lab.yml, lab/README.md, backend/tests/test_foundation_contracts.py | Static test checks internal-only lab network, no published ports, and loopback-only default ports. Actual Compose build/run is deferred to final integration by ADR-006. | ⚠️ |
| LAB-03 | Given the lab fixtures are loaded, then the SNMP record file uses well-formed system OIDs and synthetic values, and the default scenario remains declarative (not executable). | lab/fixtures/snmp/system.snmprec, lab/fixtures/oui-mini.csv, lab/scenarios/default.yml | backend/tests/test_foundation_contracts.py validates record shape, synthetic labels, and the non-executable scenario. Runtime snmpsim parsing has not run because container integration is deferred. | ⚠️ |
| UX-04 (foundation) | Given the dashboard shell is displayed, then keyboard focus is visible, reduced motion is respected, and visual status is not communicated by color alone. | frontend/src/app/globals.css, frontend/src/components/dashboard-shell.tsx, frontend/src/components/dashboard-shell.stories.tsx | Static token checks and a Storybook story are present. Browser screenshots, keyboard-only, axe, zoom and contrast reviews have not run. | ⚠️ |

## Phase 0 tooling

- scripts/verify.sh and scripts/verify.ps1 call the cross-platform scripts/verify_runner.py.
- --quick runs dependency-free structural/safety checks.
- --full runs locked backend/frontend installs, Ruff, mypy, backend tests with a 70% coverage floor, pip-audit, TypeScript, Next.js build, Storybook build, npm audit and Gitleaks. It writes logs and a Markdown report under docs/ai/verification/local-*.
- Docker Compose runtime checks are intentionally excluded from --full and remain a final integration gate, as recorded in ADR-006.

No row is marked ✅ until its latest relevant CI/local output is available. The phase gate remains open while deferred Docker and UI/runtime review evidence is unverified.
