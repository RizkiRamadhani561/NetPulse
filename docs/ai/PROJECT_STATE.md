# Project State — NetPulse

Last updated: 2026-10-16 (WIB)

## Current position

- **Phase:** 0 — Foundation
- **Implementation status:** ⚠️ Phase 0 foundation code and tooling are in place; the final phase gate is not yet passed.
- **Repository:** `RizkiRamadhani561/NetPulse`, private, default branch `main`.
- **Regular CI:** the latest run [38851053518](https://github.com/RizkiRamadhani561/NetPulse/actions/runs/38851053518) passed structure/security contracts, Ruff, mypy, 7 backend tests with 100% coverage of the current API module (70% floor), pip-audit, TypeScript, Next.js and Storybook builds, npm audit, and Gitleaks. The new warning-as-error health-test adjustment is awaiting another CI run.
- **Docker:** intentionally deferred to final integration per ADR-006. The last executed smoke failed with Next.js `EACCES` opening `/app/next-env.d.ts`; the Compose mount was narrowed to `src/` and `.storybook/`, but the runtime fix remains unverified.
- **Last full non-container verification:** [Actions run 38851053518](https://github.com/RizkiRamadhani561/NetPulse/actions/runs/38851053518). Docker Compose was skipped intentionally, not passed.
- **Release:** no release has been published.

## User-confirmed constraints

- Windows + Docker Desktop is the first development target.
- Demo content and real device monitoring should coexist in the MVP.
- Support home labs and authorized office/school networks.
- Indonesian and English UI from the MVP.
- Local Docker Compose is the first deployment target, but runtime smoke is deferred to final integration.
- Keep the repository private.
- Commit/push of foundation and verification fixes is authorized; do not change visibility or other remote settings without approval.

## Current implementation

- API scaffold: liveness endpoints are present; readiness correctly returns `not_ready` while database and scheduler dependencies do not exist.
- Frontend: dashboard shell with ID/EN labels and empty states; monitoring values are not fabricated.
- Secrets: `.env` is ignored; secret variables in `.env.example` are blank.
- Lockfiles: `backend/uv.lock` and `frontend/package-lock.json` are committed and used by locked CI installs.
- Original master specification stays at `PROMPT.md`; the working split references are in `docs/spec/`.
- Isolated lab overlay, synthetic SNMP fixture, HTTP fixture, scenario definition, static lab-safety tests and Storybook setup/story are present. Runtime lab validation has not run.
- Local skill and agent references exist under `.claude/skills/` and `.claude/agents/`; no third-party AI skill/MCP/plugin was installed.
- `scripts/verify.sh` and `scripts/verify.ps1` call a cross-platform runner that records per-step logs and a Markdown report for quick/full non-container checks.

## Verification snapshot

- Baseline run [38849910373](https://github.com/RizkiRamadhani561/NetPulse/actions/runs/38849910373) passed the then-configured backend/structure tests, frontend typecheck/build/npm audit and secret scan. The Docker Compose job was skipped by design.
- The newer CI additions—mypy, the 70% coverage floor, pip-audit, Storybook build and lab static contracts—passed in run 38851053518. The later change to eliminate a Starlette deprecation warning and enforce warnings-as-errors is awaiting CI.
- No local Windows run, browser screenshot/axe review, independent review, Docker Compose build or SNMP simulator runtime test has been claimed.

## Open items for the Phase 0 gate

1. ⏳ Wait for current CI checks and fix any genuine failures without weakening them.
2. ⏳ Resolve Storybook build or backend audit/type/coverage findings if CI identifies any.
3. ⏳ Visual, keyboard-only and axe review is still outstanding; without a browser artifact it remains unverified.
4. ⏳ Docker Compose and the lab overlay must pass the explicitly deferred integration check before the phase can be declared fully gated.
5. ⏳ Run a clean Windows `scripts/verify.ps1 -Mode full` when local toolchains are available.

## Next step

Review the newest CI run, fix its findings, and repeat until all non-container checks pass. Do not begin Phase 1 or claim the Phase 0 gate has passed while deferred runtime/UI evidence is outstanding.
