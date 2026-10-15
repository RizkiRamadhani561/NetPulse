# Project State — NetPulse

Last updated: 2026-10-16 (WIB)

## Current position

- **Phase:** 0 — Foundation
- **Overall status:** ⚠️ Partial. Core scaffold and locked dependencies are committed. Backend and frontend CI checks pass, but the Docker Compose smoke test still fails during web startup due to a Next.js TypeScript configuration write.
- **Repository:** `RizkiRamadhani561/NetPulse`, private, default branch `main`.
- **Latest confirmed failure:** [run 38801005332](https://github.com/RizkiRamadhani561/NetPulse/actions/runs/38801005332) — Docker image builds succeeded; runtime web health failed with `EACCES: permission denied, open '/app/tsconfig.json'`.
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

- Backend lint/format/tests passed in the latest completed verification run.
- Frontend typecheck, production build, dependency audit, and secret scanning passed in run [38801005332](https://github.com/RizkiRamadhani561/NetPulse/actions/runs/38801005332).
- Both Docker images built, and API container health passed. Web health failed because Next.js attempted to write `frontend/tsconfig.json` inside the non-root development container while the source is bind-mounted. The config now predeclares Next.js development and production generated-type paths; the structural verifier checks for them.
- Windows Docker Desktop and the isolated lab overlay remain unverified locally.

## Blockers / not verified

1. ❓ CI must confirm the Next.js `tsconfig.json` permission failure is fixed.
2. ❓ The isolated lab overlay and SNMP simulator have not been built/run.
3. ❓ Storybook, browser screenshots, axe/keyboard accessibility checks, and independent code review have not run.
4. ❓ A clean Windows run of `scripts/verify.ps1 -Mode full` remains pending.

## Next safe step

Review CI after the TypeScript include-path fix. If the Compose smoke passes, repeat the default stack on Windows and test the isolated lab overlay before beginning Phase 1.
