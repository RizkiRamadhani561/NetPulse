# Traceability — Phase 0

Status meanings: ✅ verified with evidence; ⚠️ partial or waiting on a deferred gate; ❌ failed; ❓ not tested.

| ID | Acceptance criterion (Given/When/Then) | Code / artifact | Test / evidence | Status |
|---|---|---|---|---|
| OPS-01 | Given the API process is running, when /api/v1/health or /healthz is requested, then liveness is returned; when DB/scheduler are absent, /api/v1/ready returns 503 rather than claiming readiness. | backend/app/main.py | backend/tests/test_health.py; [Actions run 38852297612](https://github.com/RizkiRamadhani561/NetPulse/actions/runs/38852297612): 7 tests passed, warning-free with warnings treated as errors, 100% of the current API module's 10 statements covered. Actual server runtime remains deferred. | ⚠️ |
| LAB-01 | Given the lab overlay is selected, when its Compose config is used, then synthetic HTTP/SNMP targets join only an internal lab network and no lab ports are published to the host. | docker-compose.lab.yml, lab/README.md, backend/tests/test_foundation_contracts.py | Contract test passed in the latest backend CI. Docker Compose/lab runtime validation is deferred by ADR-006 and has not passed. | ⚠️ |
| LAB-03 | Given the lab fixtures are loaded, then SNMP records use well-formed system OIDs/synthetic values and the scenario remains declarative. | lab/fixtures/snmp/system.snmprec, lab/fixtures/oui-mini.csv, lab/scenarios/default.yml | Static fixture/scenario contract passed in CI. A live snmpsim parser/runtime test has not run. | ⚠️ |
| UX-04 (foundation) | Given the dashboard shell is displayed, then visible focus and reduced-motion behavior are defined and status is not communicated only by color. | frontend/src/app/globals.css, frontend/src/components/dashboard-shell.tsx, frontend/src/components/dashboard-shell.stories.tsx | Static design/accessibility token checks and Storybook production build passed in [run 38852297612](https://github.com/RizkiRamadhani561/NetPulse/actions/runs/38852297612). Screenshots, axe, keyboard-only, contrast and responsive behavior have not been visually inspected. | ⚠️ |

## Phase 0 automated verification

- bash ./scripts/verify.sh --quick: passed in CI with 0 failures and 0 warnings.
- Ruff lint and format, mypy, pytest + coverage floor 70%, pip-audit: passed.
- Frontend locked install, TypeScript, Next.js production build, Storybook production build, npm audit: passed. npm audit found 0 vulnerabilities.
- Gitleaks CLI 8.30.1: passed; output reported no leaks found.
- Evidence run: https://github.com/RizkiRamadhani561/NetPulse/actions/runs/38852297612 (commit 1b95aaf).

## Deferred gates — intentionally not marked as passed

| Gate | Status | Why / exit criteria |
|---|---|---|
| Docker Compose smoke | ⏳ Deferred per ADR-006 | After the full system is built, manually dispatch the workflow; API/web health, home route and documented readiness assertions must pass. Prior failure remains documented in BUG-004. |
| Isolated lab + SNMP simulator runtime | ⏳ Deferred with Docker | Run the internal-only lab, inspect the effective Compose config/ports and confirm synthetic SNMP responses. |
| Browser/accessibility review | ❓ Not tested | Save desktop/mobile screenshots; inspect focus, empty/error states, responsive layout, contrast and reduced motion; run axe and keyboard-only checks. |
| Local Windows verification | ❓ Not tested | Run ./scripts/verify.ps1 -Mode full on the target Windows + Docker Desktop machine once local toolchains are available. |
| Independent review | ❓ Not performed | Obtain a fresh-context review of this phase's changes and close high-severity findings with evidence. |

The foundation is implemented and regular non-container CI is green. That is not a claim of complete runtime integration, accessibility sign-off, independent review, or production readiness. The requested Docker deferral is a scheduling exception, not a passing test.
