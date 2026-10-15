# Project State — NetPulse

Last updated: 2026-10-16 (WIB)

## Current position

- **Phase:** 0 — Foundation
- **Overall status:** ⚠️ Partial. The initial repository overview is committed; the Phase 0 source scaffold is being added in a separate commit.
- **Repository:** `RizkiRamadhani561/NetPulse` (public at the time of this push; default branch `main`).
- **Current task:** publish the foundation and verify the remote tree.
- **Release:** no release has been published.

## User-confirmed constraints

- Build from a new repository.
- Windows with Docker Desktop is the first development target.
- Demo content and real device monitoring should coexist in the MVP; do not make demo an exclusive global mode without revisiting the decision.
- Support home labs and authorized office/school networks.
- Indonesian and English UI from the MVP.
- Local Docker Compose is the first deployment target.
- Repository visibility remains public for now; the owner may change it later.
- Commit and push were explicitly authorized for the initial foundation. Repository security settings have not been changed.

## Current implementation

- API scaffold: liveness endpoint is present; readiness reports `not_ready` until a database and scheduler are implemented.
- Frontend: dashboard shell and ID/EN labels; monitoring values remain empty placeholders rather than synthetic uptime/latency.
- Secrets: `.env` is ignored; `.env.example` contains variable names with blank values.
- Lab: opt-in internal Docker network and synthetic fixtures are scaffolded; the lab runtime is not yet verified.
- Scope and implementation notes are organized under `docs/spec/` and `docs/ai/`. Per-feature acceptance criteria still need to be expanded as features are implemented.

## Verification snapshot

- Structural checks on the prepared package: 0 failures, 2 warnings (missing dependency lockfiles).
- Backend tests: 2 passed against the already-installed host environment. The pinned dependency graph was not installed.
- Docker Compose build/start, browser checks, full dependency installation, Storybook, Gitleaks, and GitHub Actions remain unverified in the preparation environment.

## Blockers / not verified

1. ⚠️ `backend/uv.lock` and `frontend/package-lock.json` are absent. Package registry requests timed out during preparation, so lockfiles were not fabricated.
2. ❓ Docker Compose build/start and HTTP smoke checks have not run because Docker was unavailable in the preparation environment.
3. ❓ Node dependencies were not installed; TypeScript, Storybook, and production build have not been verified.
4. ❓ Gitleaks, pre-commit, GitHub Actions, browser/accessibility checks, and an independent code review have not run.

## Next safe step

Generate and review dependency lockfiles on a network-enabled machine, then run `scripts/verify.ps1 -Mode quick` on Windows. Confirm the Docker stack and isolated lab, then fix any findings before marking Phase 0 complete.
