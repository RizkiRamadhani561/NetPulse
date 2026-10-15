# Project State — NetPulse

Last updated: 2026-10-16 (WIB)

## Current position

- **Phase:** 0 — Foundation
- **Overall status:** ⚠️ Partial. Repository scaffold, bilingual dashboard shell, API liveness/readiness endpoints, internal lab definitions, original prompt, and locked dependency files are committed. Full Phase 0 verification remains open.
- **Repository:** `RizkiRamadhani561/NetPulse`, private, default branch `main`.
- **Latest tracked checkpoint:** [`5938092`](https://github.com/RizkiRamadhani561/NetPulse/commit/59380926a4b43f60b64da4d2b866df25c6ef6fd8) — verification formatting adjustment.
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

- The prior locked CI run passed backend lint/format/tests, frontend typecheck/build/audit, and secret scanning before the Docker smoke job was added.
- Ruff lint passed on the latest attempt; another Ruff lint line-length issue was fixed in the follow-up. Ruff format still needs a green result for the current head.
- The API image built successfully. One container smoke attempt failed on an npm registry reset; a later attempt started the services but a smoke request received connection reset while the web container had no healthcheck. A web readiness healthcheck and richer failure logs have been added.
- Local Docker is unavailable in the preparation environment; Windows validation remains outstanding.

## Blockers / not verified

1. ❓ The next CI run must confirm Ruff lint/format/tests pass with the latest source.
2. ❓ The next Docker Compose smoke run must verify the web healthcheck and recover from transient startup/network errors.
3. ❓ The Docker lab overlay and SNMP simulator have not been built/run.
4. ❓ Storybook, browser screenshots, axe/keyboard accessibility checks, and independent code review have not run.
5. ❓ A clean Windows run of `scripts/verify.ps1 -Mode full` remains pending.

## Next safe step

Review the complete CI result. If the default Compose smoke passes, run the quick verification on Windows and check the default stack locally; then test the isolated lab overlay before beginning Phase 1.
