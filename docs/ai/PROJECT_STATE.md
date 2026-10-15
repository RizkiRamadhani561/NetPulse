# Project State — NetPulse

Last updated: 2026-10-16 (WIB)

## Current position

- **Phase:** 0 — Foundation
- **Overall status:** ⚠️ Partial. Core scaffold and locked dependencies are committed. Backend/frontend checks pass on the previous revision, but the current CI is re-running after a TypeScript config fix for Docker startup.
- **Repository:** `RizkiRamadhani561/NetPulse`, private, default branch `main`.
- **Current issue:** prior Docker smoke failed with `EACCES: permission denied, open '/app/tsconfig.json'` when Next.js started as non-root with a bind-mounted source tree.
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
- Next.js configuration now predeclares both `.next/types/**/*.ts` and `.next/dev/types/**/*.ts`; the structural checker validates the paths.

## Verification snapshot

- The previous run passed backend checks, frontend typecheck/build/audit, and secret scanning.
- The current run validated repository structure and Ruff lint, then the format check flagged one layout change in the structural checker; that layout is fixed in the follow-up commit.
- The last completed Docker smoke built both images and found the web startup permission error; the config fix is not considered resolved until a new Docker smoke passes.
- Windows Docker Desktop and the isolated lab overlay remain unverified locally.

## Blockers / not verified

1. ❓ The new run must confirm lint/format/backend tests and the Docker Compose smoke all pass after the configuration fix.
2. ❓ The isolated lab overlay and SNMP simulator have not been built/run.
3. ❓ Storybook, browser screenshots, axe/keyboard accessibility checks, and independent code review have not run.
4. ❓ A clean Windows run of `scripts/verify.ps1 -Mode full` remains pending.

## Next safe step

Check the latest CI run. If default Compose smoke passes, repeat the default stack on Windows and test the isolated lab overlay before beginning Phase 1.
