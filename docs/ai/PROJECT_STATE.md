# Project State — NetPulse

Last updated: 2026-10-16 (WIB)

## Current position

- **Phase:** 0 — Foundation
- **Overall status:** ⚠️ Partial. The initial overview and source scaffold are committed; full runtime and build verification remain outstanding.
- **Repository:** `RizkiRamadhani561/NetPulse`, default branch `main`.
- **Foundation commit:** [`a01f6ea`](https://github.com/RizkiRamadhani561/NetPulse/commit/a01f6ea572d3560427cfd9d84336e7881102eed8).
- **Release:** no release has been published.

## User-confirmed constraints

- Build from a new repository.
- Windows with Docker Desktop is the first development target.
- Demo content and real device monitoring should coexist in the MVP; do not make demo an exclusive global mode without revisiting the decision.
- Support home labs and authorized office/school networks.
- Indonesian and English UI from the MVP.
- Local Docker Compose is the first deployment target.
- The user asked to postpone the repository privacy step. The initial metadata check reported public; the final metadata checks reported private. No visibility setting was changed by the assistant, so the owner should confirm the status in GitHub.
- Commit and push of the initial foundation were explicitly authorized. No other repository settings were changed.

## Current implementation

- API scaffold: liveness endpoint is present; readiness reports `not_ready` until a database and scheduler are implemented.
- Frontend: dashboard shell and ID/EN labels; monitoring values remain empty placeholders rather than synthetic uptime/latency.
- Secrets: `.env` is ignored; `.env.example` contains variable names with blank values.
- Lab: opt-in internal Docker network and synthetic fixtures are scaffolded; the lab runtime is not yet verified.
- Scope and implementation notes are organized under `docs/spec/` and `docs/ai/`. These are working references; per-feature acceptance criteria still need to be expanded as features are implemented.

## Verification snapshot

- Structural checks on the prepared package: 0 failures, 2 warnings (missing dependency lockfiles).
- Backend tests: 2 passed against the already-installed host environment. The pinned dependency graph was not installed.
- Remote verification: GitHub file reads confirmed the README, API entry point, dashboard shell, scope notes, and environment safeguards are present on `main`.
- Docker Compose build/start, browser checks, full dependency installation, Storybook, Gitleaks, and GitHub Actions remain unverified in the preparation environment.

## Blockers / not verified

1. ⚠️ `backend/uv.lock` and `frontend/package-lock.json` are absent. Package registry requests timed out during preparation, so lockfiles were not fabricated.
2. ❓ Docker Compose build/start and HTTP smoke checks have not run because Docker was unavailable in the preparation environment.
3. ❓ Node dependencies were not installed; TypeScript, Storybook, and production build have not been verified.
4. ❓ Gitleaks, pre-commit, GitHub Actions, browser/accessibility checks, and an independent code review have not run.

## Next safe step

Generate and review dependency lockfiles on a network-enabled machine, then run `scripts/verify.ps1 -Mode quick` on Windows. Confirm the Docker stack and isolated lab, then fix any findings before marking Phase 0 complete.
