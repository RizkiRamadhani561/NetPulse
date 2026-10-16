# Project State — NetPulse

Last updated: 2026-10-16 (WIB)

## Current position

- **Phase:** 0 — Foundation
- **Overall status:** ⚠️ Partial. Core scaffold and locked dependencies are committed. Backend checks, frontend typecheck/build/audit, and secret scanning pass on the latest completed run; Docker Compose smoke remains blocked by a generated-file permission issue.
- **Repository:** RizkiRamadhani561/NetPulse, private, default branch main.
- **Current issue:** Next.js 16.4 fails with `EACCES` opening `/app/next-env.d.ts`. The source directory is bind-mounted, while the dev process runs as non-root `node`. Compose now gives this generated file a separate named volume; CI must confirm the fix.
- **Latest failed Docker run:** https://github.com/RizkiRamadhani561/NetPulse/actions/runs/38803517944
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
- Next.js TypeScript settings preconfigure both generated type paths and the automatic JSX runtime.
- Docker Compose isolates the generated `next-env.d.ts` in a named volume so the non-root dev process can update it without requiring write access to the host source tree.

## Verification snapshot

- Latest completed CI run passed structural checks, Ruff lint/format, backend tests, frontend typecheck, production build, dependency audit, and secret scanning.
- Docker image builds completed and API health passed. The web container failed health checks after Next.js logged `EACCES` on `/app/next-env.d.ts`.
- The named-volume change and structural regression check are committed in the current follow-up; their effect is not confirmed until a new Docker smoke run passes.
- Windows Docker Desktop and the isolated lab overlay remain unverified locally.

## Blockers / not verified

1. ❓ CI must confirm the frontend healthcheck and all Docker Compose smoke assertions pass with the generated-file volume.
2. ❓ The isolated lab overlay and SNMP simulator have not been built/run.
3. ❓ Storybook, browser screenshots, axe/keyboard accessibility checks, and independent code review have not run.
4. ❓ A clean Windows run of `scripts/verify.ps1 -Mode full` remains pending.

## Next safe step

Review the new CI run. If Docker Compose smoke passes, repeat the default stack on Windows and test the isolated lab overlay before beginning Phase 1.
