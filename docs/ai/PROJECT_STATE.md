# Project State — NetPulse

Last updated: 2026-10-16 (WIB)

## Current position

- **Phase:** 0 — Foundation
- **Overall status:** ⚠️ Partial. Core scaffold and locked dependencies are committed. Backend checks pass; the Docker Compose web-startup permission failure is being addressed by preconfiguring the required Next.js 16.4 TypeScript defaults.
- **Repository:** RizkiRamadhani561/NetPulse, private, default branch main.
- **Current issue:** the previous Docker smoke failed with EACCES on /app/tsconfig.json while Next.js attempted to rewrite its TypeScript config.
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

- API scaffold: liveness endpoint is present; readiness correctly reports not_ready until database and scheduler dependencies exist.
- Frontend: dashboard shell and ID/EN labels; monitoring values remain empty placeholders rather than synthetic uptime/latency.
- Secrets: .env is ignored; .env.example contains blank values for secret variables.
- Dependency resolution: backend/uv.lock and frontend/package-lock.json are committed and used by CI/Docker.
- Original master specification is stored at PROMPT.md; working references are under docs/spec/.
- Lab: opt-in internal Docker network and synthetic fixtures are scaffolded; runtime validation remains pending.
- Next.js 16.4 config now sets jsx=react-jsx and preconfigures both development and production generated type include paths.

## Verification snapshot

- Backend lint, format, tests, and structural checks passed after the first include-path patch's formatter correction.
- Frontend typecheck/build/audit and secret scanning passed on that revision.
- The Docker smoke job for that revision had not completed when checked. Review of the exact Next.js v16.4.0 source showed the config also requires jsx=react-jsx; both that and the development type path are now set explicitly.
- Windows Docker Desktop and the isolated lab overlay remain unverified locally.

## Blockers / not verified

1. ❓ CI must verify that preconfigured Next.js defaults prevent tsconfig writes and allow Docker Compose smoke to pass.
2. ❓ The isolated lab overlay and SNMP simulator have not been built/run.
3. ❓ Storybook, browser screenshots, axe/keyboard accessibility checks, and independent code review have not run.
4. ❓ A clean Windows run of scripts/verify.ps1 -Mode full remains pending.

## Next safe step

Review CI after the complete Next.js TypeScript config fix. If Docker Compose smoke passes, repeat the default stack on Windows and test the isolated lab overlay before beginning Phase 1.
