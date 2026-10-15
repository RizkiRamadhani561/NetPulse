# Project State — NetPulse

Last updated: 2026-10-16 (WIB)

## Current position

- **Phase:** 0 — Foundation
- **Overall status:** ⚠️ Partial. Repository scaffold, bilingual dashboard shell, API liveness/readiness endpoints, internal lab definitions, original prompt, and dependency lockfiles are committed.
- **Repository:** `RizkiRamadhani561/NetPulse`, private, default branch `main`.
- **Release:** no release has been published.

## User-confirmed constraints

- Windows with Docker Desktop is the first development target.
- Demo content and real device monitoring should coexist in the MVP.
- Support home labs and authorized office/school networks.
- Indonesian and English UI from the MVP.
- Local Docker Compose is the first deployment target.
- The user changed repository visibility to private. Keep the repository private; the assistant did not change visibility.
- Commit/push of the foundation and verification fixes is authorized. Other repository settings have not been changed.

## Current implementation

- API scaffold: liveness endpoint is present; readiness correctly reports `not_ready` until database and scheduler dependencies exist.
- Frontend: dashboard shell and ID/EN labels; monitoring values remain empty placeholders rather than synthetic uptime/latency.
- Secrets: `.env` is ignored; `.env.example` contains blank values for secret variables.
- Dependency resolution: `backend/uv.lock` and `frontend/package-lock.json` are committed and used by CI/Docker.
- Original master specification is stored at `PROMPT.md`; working references are under `docs/spec/`.
- Lab: opt-in internal Docker network and synthetic fixtures are scaffolded; runtime validation remains pending.

## Verification snapshot

- GitHub Actions backend checks passed after the final structural-check formatting adjustment.
- On the latest observed run, frontend typecheck/build/audit and secret scanning passed; the default Compose smoke was still running when checked.
- Docker smoke now uses a web healthcheck, retries transient connection errors, prints service logs on failure, and has a 180-second startup-health timeout to avoid an unbounded wait.
- Local Docker is unavailable in the preparation environment; Windows validation remains outstanding.

## Blockers / not verified

1. ❓ The current run's Docker Compose smoke result must be checked after it completes.
2. ❓ The isolated lab overlay and SNMP simulator have not been built/run.
3. ❓ Storybook, browser screenshots, axe/keyboard accessibility checks, and independent code review have not run.
4. ❓ A clean Windows run of `scripts/verify.ps1 -Mode full` remains pending.

## Next safe step

Review the full CI result. If default Compose smoke passes, run quick verification on Windows and validate the default stack locally; then test the isolated lab overlay before beginning Phase 1.
