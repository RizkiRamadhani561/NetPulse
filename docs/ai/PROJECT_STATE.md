# Project State — NetPulse

Last updated: 2026-10-16 (WIB)

## Current position

- **Phase:** 0 — Foundation
- **Overall status:** ⚠️ Partial. The repository scaffold, bilingual dashboard shell, API liveness/readiness endpoints, internal lab definitions, original prompt, and dependency lockfiles are committed.
- **Repository:** `RizkiRamadhani561/NetPulse`, private, default branch `main`.
- **Release:** no release has been published.

## User-confirmed constraints

- Windows with Docker Desktop is the first development target.
- Demo content and real device monitoring should coexist in the MVP.
- Support home labs and authorized office/school networks.
- Indonesian and English UI from the MVP.
- Local Docker Compose is the first deployment target.
- The user changed repository visibility to private. Keep the repository private; the assistant did not change visibility.
- Commit/push of foundation and verification fixes is authorized. Other repository settings have not been changed.

## Current implementation

- API scaffold: liveness endpoint is present; readiness correctly reports `not_ready` until database and scheduler dependencies exist.
- Frontend: dashboard shell and ID/EN labels; monitoring values remain empty placeholders rather than synthetic uptime/latency.
- Secrets: `.env` is ignored; `.env.example` contains blank values for secret variables.
- Dependency resolution: `backend/uv.lock` and `frontend/package-lock.json` are committed and used by CI/Docker.
- Original master specification is stored at `PROMPT.md`; working references are under `docs/spec/`.
- Lab: opt-in internal Docker network and synthetic fixtures are scaffolded; runtime validation remains pending.

## Verification snapshot

- The pre-container-smoke revision passed backend lint/format/tests, frontend typecheck/build/audit, and secret scanning.
- On the latest locked CI run, Ruff lint passed; Ruff format requested one final compact formatting change in the structural checker. That change is now applied without weakening the check.
- API container image built successfully on earlier Docker smoke. A later smoke attempt started the services but a request reset the connection; the web service healthcheck and diagnostic logs are now configured, and the newest smoke result remains to be checked.
- Local Docker is unavailable in the preparation environment; Windows validation remains outstanding.

## Blockers / not verified

1. ❓ The next CI run must confirm Ruff lint/format/backend tests all pass together.
2. ❓ Default Compose smoke must complete successfully after the web healthcheck and retry changes.
3. ❓ The isolated lab overlay and SNMP simulator have not been built/run.
4. ❓ Storybook, browser screenshots, axe/keyboard accessibility checks, and independent code review have not run.
5. ❓ A clean Windows run of `scripts/verify.ps1 -Mode full` remains pending.

## Next safe step

Review the complete CI result after the final formatting adjustment. If the default Compose smoke passes, run quick verification on Windows and validate the default stack and isolated lab before beginning Phase 1.
