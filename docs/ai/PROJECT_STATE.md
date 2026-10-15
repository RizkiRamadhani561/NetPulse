# Project State — NetPulse

Last updated: 2026-10-16 (WIB)

## Current position

- **Phase:** 0 — Foundation
- **Overall status:** ⚠️ Partial. Repository scaffold, bilingual dashboard shell, API liveness/readiness endpoints, lab definitions, locked dependency files, and CI improvements are committed. Full Phase 0 verification remains open.
- **Repository:** `RizkiRamadhani561/NetPulse`, private, default branch `main`.
- **Latest tracked checkpoint:** [`685d1c9`](https://github.com/RizkiRamadhani561/NetPulse/commit/685d1c9bd313cec95e755ea4979d06a32f797571) — retry configuration for transient npm download failures.
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
- Dependency resolution: committed `backend/uv.lock` and `frontend/package-lock.json`; CI and Docker images consume the lockfiles.
- Original master specification is stored at `PROMPT.md`; working references are under `docs/spec/`.
- Lab: opt-in internal Docker network and synthetic fixtures are scaffolded; lab runtime validation is still pending.

## Verification snapshot

- GitHub Actions passed backend lint/format/tests, frontend typecheck/build/audit, and secret scanning on the pre-container-smoke revision.
- The latest locked CI run passed Ruff lint after the string-length fix; its format check then reported remaining formatting differences in `scripts/verify_project.py`. The formatter-only change is the current follow-up.
- Default Docker smoke built the API image from the locked runtime graph. The first frontend image build failed while downloading npm packages due to registry `ECONNRESET`; retries were added to the Dockerfile and the next smoke run has not yet been reviewed.
- Local Docker is unavailable in the preparation environment; Windows validation remains outstanding.

## Blockers / not verified

1. ❓ Ruff format check must pass on the latest source after the final formatting adjustment.
2. ❓ The Docker Compose smoke after npm retry settings must complete successfully.
3. ❓ The Docker lab overlay and SNMP simulator have not been built/run.
4. ❓ Storybook, browser screenshots, axe/keyboard accessibility checks, and independent code review have not run.
5. ❓ A clean Windows run of `scripts/verify.ps1 -Mode full` remains pending.

## Next safe step

Review CI after the script formatting adjustment and npm retry changes. If the default Compose smoke passes, run quick verification on Windows and confirm the stack locally; then test the isolated lab overlay before beginning Phase 1.
