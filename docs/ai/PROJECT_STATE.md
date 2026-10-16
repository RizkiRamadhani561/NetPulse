# Project State — NetPulse

Last updated: 2026-10-16 (WIB)

## Current position

- **Phase:** 0 — Foundation
- **Overall status:** ⚠️ Partial. Backend checks, frontend typecheck/build/audit, and secret scanning are the regular CI checks. Docker Compose runtime validation is intentionally deferred to the final integration stage; it has not passed yet.
- **Repository:** RizkiRamadhani561/NetPulse, private, default branch main.
- **Known Docker issue:** Next.js 16.4 previously threw `EACCES` for `/app/next-env.d.ts` because the full frontend directory was bind-mounted over the image's writable work directory. Compose now mounts only `src/` and `.storybook/` read-only. Runtime behavior remains unverified.
- **Last failed Docker smoke:** https://github.com/RizkiRamadhani561/NetPulse/actions/runs/38803517944
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
- Compose keeps generated runtime/config files in the image-owned work directory and selectively mounts `frontend/src` and `frontend/.storybook` read-only for source changes.

## Verification snapshot

- Regular CI checks: structural checks, Ruff lint/format, backend tests, frontend typecheck, production build, dependency audit, and secret scanning.
- Docker Compose smoke no longer runs on every push or pull request. It is manual-only so container integration can be completed after the system's features are ready.
- The latest failed container run showed API health succeeded but Next.js web health timed out on a generated-file permission error. The selective mount configuration addresses the likely cause but still needs an actual Compose run.
- Windows Docker Desktop and the isolated lab overlay remain unverified locally.

## Blockers / not verified

1. ⏳ Final Docker Compose smoke, including API health, frontend health/home page, and documented readiness response.
2. ❓ The isolated lab overlay and SNMP simulator have not been built/run.
3. ❓ Storybook, browser screenshots, axe/keyboard accessibility checks, and independent code review have not run.
4. ❓ A clean Windows run of `scripts/verify.ps1 -Mode full` remains pending.

## Next safe step

Continue building and validating features using the regular backend/frontend CI checks. When feature work is complete and checks are stable, run the CI workflow manually to perform the final Docker Compose integration smoke test.
