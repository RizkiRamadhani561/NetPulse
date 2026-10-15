# Traceability — Phase 0

Status meanings: ✅ verified with evidence; ⚠️ partial; ❌ failed; ❓ not tested.

| ID | Acceptance criterion (Given/When/Then) | Code / artifact | Test / evidence | Status |
|---|---|---|---|---|
| OPS-01 | Given the API process is running, when `/api/v1/health` is requested, then it returns liveness; when DB/scheduler are absent, `/api/v1/ready` must not claim readiness. | `backend/app/main.py` | `backend/tests/test_health.py`; local host-environment run: 2 passed; pinned Python 3.14/dependencies still unverified | ⚠️ |
| LAB-01 | Given the lab profile is selected, when compose is built, then synthetic HTTP/SNMP targets are attached only to an internal lab network and are not published to the host. | `docker-compose.lab.yml`, `lab/` | Compose config/build not run in preparation environment | ⚠️ |
| LAB-03 | Given the fixture files are loaded, when parser tests are added later, then the SNMP walk and mini-table contain synthetic, non-sensitive records. | `lab/fixtures/` | Manual/static inspection only; parser tests not yet implemented | ⚠️ |
| UX-04 (foundation) | Given the base dashboard shell is displayed, when navigating by keyboard or reducing motion, then focus is visible and reduced-motion CSS is honored; status labels are not conveyed by color alone. | `frontend/src/app/globals.css`, `frontend/src/components/dashboard-shell.tsx` | Static check only; axe/browser test not run | ⚠️ |

No ID is marked ✅ because runtime and independent review evidence are not yet available.
