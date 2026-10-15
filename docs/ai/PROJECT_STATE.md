# Project State — NetPulse

Last updated: 2026-10-16 (WIB)

## Current position

- **Phase:** 0 — Foundation
- **Overall status:** ⚠️ Partial. Repository scaffold, bilingual dashboard shell, API liveness/readiness endpoints, lab definitions, and locked dependency files are committed. Full Phase 0 verification is still open.
- **Repository:** `RizkiRamadhani561/NetPulse`, private, default branch `main`.
- **Current task checkpoint:** [`c555bea`](https://github.com/RizkiRamadhani561/NetPulse/commit/c555bea81748bbb4d015c055765398f5c5e0fae8) — added the original master specification at `PROMPT.md`.
- **Release:** no release has been published.

## User-confirmed constraints

- Windows with Docker Desktop is the first development target.
- Demo content and real device monitoring should coexist in the MVP; do not make demo an exclusive global mode without revisiting the decision.
- Support home labs and authorized office/school networks.
- Indonesian and English UI from the MVP.
- Local Docker Compose is the first deployment target.
- The user changed repository visibility to private during the initial push process. Keep its current private status; the assistant did not change visibility.
- Commit and push of the foundation and verification fixes are authorized. Other repository settings have not been changed.

## Current implementation

- API scaffold: liveness endpoint is present; readiness correctly reports `not_ready` until database and scheduler dependencies exist.
- Frontend: dashboard shell and ID/EN labels; monitoring values remain empty placeholders rather than synthetic uptime/latency.
- Secrets: `.env` is ignored; `.env.example` contains variable names with blank values.
- Dependency resolution: committed `backend/uv.lock` and `frontend/package-lock.json`; CI and Docker images now consume the lockfiles.
- Original project specification is stored at `PROMPT.md`; split working references are under `docs/spec/`.
- Lab: opt-in internal Docker network and synthetic fixtures are scaffolded; lab runtime validation is still pending.

## Verification snapshot

- GitHub Actions passed backend lint/format/tests, frontend typecheck/build/audit, and secret scanning on the pre-container-smoke revision.
- On the latest smoke attempt, the API Docker image built successfully with the locked runtime graph. The web image failed while downloading npm packages due to registry `ECONNRESET`; retry settings have now been added to the frontend Dockerfile.
- A formatting check identified one 101-character line in `scripts/verify_project.py`; it is shortened in the follow-up fix.
- Local Docker is unavailable in the preparation environment; Windows validation remains outstanding.

## Blockers / not verified

1. ❓ The next Docker Compose smoke run has not yet confirmed that the npm registry reset is recoverable.
2. ❓ The Docker lab overlay and its SNMP simulator have not been built/run.
3. ❓ Storybook, browser screenshots, axe/keyboard accessibility checks, and independent code review have not run.
4. ❓ A clean Windows run of `scripts/verify.ps1 -Mode full` remains pending.

## Next safe step

Review CI after retry and Ruff fixes. If the default Compose smoke passes, run quick verification on Windows and confirm the stack locally; then test the isolated lab overlay before beginning Phase 1.
