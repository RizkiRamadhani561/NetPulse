# Project State — NetPulse

Last updated: 2026-10-16 (WIB)

## Current position

- **Phase:** 0 — Foundation
- **Overall status:** ⚠️ Partial. Repository scaffold, bilingual dashboard shell, API liveness/readiness endpoints, lab definitions, and initial CI are committed. Docker Compose runtime smoke is now part of CI but still needs a result and Windows validation.
- **Repository:** `RizkiRamadhani561/NetPulse`, private, default branch `main`.
- **Current head at the last preparation checkpoint:** [`285a8b6`](https://github.com/RizkiRamadhani561/NetPulse/commit/285a8b6d3154284c3308e82b80b52f60ae24cbb1) — dependency lockfiles added.
- **Release:** no release has been published.

## User-confirmed constraints

- Build from a new repository.
- Windows with Docker Desktop is the first development target.
- Demo content and real device monitoring should coexist in the MVP; do not make demo an exclusive global mode without revisiting the decision.
- Support home labs and authorized office/school networks.
- Indonesian and English UI from the MVP.
- Local Docker Compose is the first deployment target.
- The repository was changed to private by the user during the initial push process. Keep its current private status; the assistant did not change visibility.
- Commit and push of the foundation and verification fixes are authorized. Other repository settings have not been changed.

## Current implementation

- API scaffold: liveness endpoint is present; readiness correctly reports `not_ready` until the database and scheduler are implemented.
- Frontend: dashboard shell and ID/EN labels; monitoring values remain empty placeholders rather than synthetic uptime/latency.
- Secrets: `.env` is ignored; `.env.example` contains variable names with blank values.
- Dependency resolution: committed `backend/uv.lock` and `frontend/package-lock.json`; CI and Docker images now use locked dependencies.
- Lab: opt-in internal Docker network and synthetic fixtures are scaffolded; runtime validation of the lab overlay is still pending.
- Scope and implementation notes are organized under `docs/spec/` and `docs/ai/`. These are working references; acceptance criteria must be expanded in traceability as features are implemented.

## Verification snapshot

- Structural check at the prepared package: 0 failures; two lockfile warnings were resolved once the locks were generated.
- Backend tests: 2 passed against the earlier host-installed environment. The current lockfile-based CI test result is tracked in GitHub Actions.
- A prior GitHub CI run completed successfully for backend lint/format/tests, frontend typecheck/build/audit, and Gitleaks.
- A newer Docker Compose smoke job is now configured to build and run the app, check both liveness endpoints and the home page, and confirm readiness stays accurately `not_ready` until dependencies exist.
- Runtime verification on Windows and the opt-in isolated lab remains pending.

## Blockers / not verified

1. ❓ The new Docker Compose smoke result has not yet been reviewed for the current head.
2. ❓ The Docker lab overlay and its SNMP simulator have not been built/run in this environment.
3. ❓ Storybook, browser screenshots, axe/keyboard accessibility checks, and independent code review have not run.
4. ❓ A clean Windows run of `scripts/verify.ps1 -Mode full` remains pending.

## Next safe step

Review the latest GitHub Actions run after lockfile-based CI changes. If the default Compose smoke passes, run the quick checks on Windows and confirm the stack locally; then test the isolated lab overlay before beginning Phase 1.
