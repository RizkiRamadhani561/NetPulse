# Project State — NetPulse

Last updated: 2026-10-17 (WIB)

## Current position

- **Phase:** 0 — Foundation
- **Implementation status:** ✅ Foundation implementation is in place and regular non-container CI is green. Formal integration/release gates remain explicitly open.
- **Repository:** RizkiRamadhani561/NetPulse, private, default branch main.
- **Latest regular CI:** [Run 38852297612](https://github.com/RizkiRamadhani561/NetPulse/actions/runs/38852297612), commit 8fe85e8. All three required jobs passed: foundation/backend, frontend build/audit, secret scanning.
- **Coverage:** 7 backend tests passed with warnings-as-errors; current backend app module has 100% coverage of 10 statements, above the enforced 70% floor.
- **Dependency/security checks:** pip-audit reported no known vulnerabilities; npm audit found 0 vulnerabilities; Gitleaks CLI 8.30.1 reported no leaks.
- **Docker:** deliberately deferred to project-wide final integration per ADR-006 and the user's explicit direction. Previous smoke [run 38803517944](https://github.com/RizkiRamadhani561/NetPulse/actions/runs/38803517944) failed because Next.js couldn't open /app/next-env.d.ts; Compose now mounts only source directories, but runtime behavior remains unverified.
- **Release:** none. Do not call the scaffold production-ready.

## User-confirmed constraints

- Windows + Docker Desktop is the first development target.
- Demo content and real device monitoring should coexist in the MVP.
- Support home labs and authorized office/school networks.
- Indonesian and English UI from the MVP.
- Compose runtime smoke is held until the full system is built; this is a deferral, not a passing test.
- Keep the repository private.
- Commit/push of foundation and verification fixes is authorized; do not change visibility or other remote settings without approval.

## UI refresh — 2026-10-17

- The dashboard UI refresh is being prepared on branch `feat/netpulse-ui-ux-refresh`; it keeps Phase 0 preview semantics and does not implement monitoring features.
- Visual baseline: Space Grotesk for headings, Inter for body copy, IBM Plex Mono for technical labels; teal `#54D8B6` remains the primary accent and `#D93A2F` is reserved for critical/destructive states.
- Focus navigation, reduced-motion behavior, subdued surfaces, and preview-only empty states are retained; the browser contract now checks typography tokens, critical tokens, planned controls, and keyboard skip navigation.
- **Verification status:** the branch build, browser/axe audit, screenshot review, and CI results are pending. Do not close UX-04 until the new artifacts and checks have been inspected.
- **Remote visibility discrepancy:** current GitHub repository metadata reports `public`, while earlier project state said private. No visibility or other repository setting was changed as part of this UI task.

## Current implementation

- API scaffold exposes liveness endpoints; readiness honestly returns not_ready until database and scheduler dependencies exist.
- Frontend dashboard shell has ID/EN labels, visual tokens, reduced-motion/focus rules, and empty states; monitoring values are not fabricated.
- .env is ignored, and secret variables in .env.example remain blank.
- backend/uv.lock and frontend/package-lock.json are committed and used by locked CI installs.
- Original master specification remains in PROMPT.md; working split references are in docs/spec/.
- Internal lab overlay, synthetic HTTP/SNMP fixtures, scenario, static lab-contract tests, Storybook setup/story, and local verification agent/skill notes exist. Runtime lab validation has not run.
- Bash and PowerShell entry points call the cross-platform Python verification runner. CI now calls bash ./scripts/verify.sh --quick; --full covers the non-container toolchain and writes per-step logs/report.
- GitHub Actions references are SHA-pinned; Gitleaks CLI is pinned to 8.30.1.

## Latest verification snapshot

- [Actions run 38852297612](https://github.com/RizkiRamadhani561/NetPulse/actions/runs/38852297612): complete, success.
- Quick verification through the shared entry point: 0 failures, 0 warnings.
- Ruff lint/format, mypy, tests + 70% coverage floor, pip-audit: pass.
- npm ci, TypeScript, Next.js production build, Storybook production build, npm audit: pass; npm audit found 0 vulnerabilities.
- Secret scan: pass; Gitleaks 8.30.1 output says no leaks found.
- Docker Compose job: skipped as configured. Do not count as passed.
- The local PowerShell full runner, browser screenshots/axe/keyboard review, SNMP simulator runtime, and independent reviewer have not been run.

## Remaining gates and known blockers

1. **BUG-004 / Docker integration:** manually dispatch the Compose smoke workflow after the full system is implemented. Confirm API/web health, home route, and readiness behavior. Keep unresolved until it passes.
2. **LAB-01 / LAB-03:** static safety contracts pass; actual lab compose and SNMP simulator runtime remain unverified until final integration.
3. **UX-04:** Storybook builds, but no real browser screenshots, axe report, keyboard-only, contrast, or responsive-overflow review is available yet.
4. **Independent review:** repository review instructions exist, but no independent reviewer result has been produced.
5. **Windows:** a clean scripts/verify.ps1 -Mode full run is pending. CI ran on hosted Ubuntu.

## Phase 0 decision

The foundation implementation and automated non-container checks are complete. At the user's direction, Docker runtime is a project-wide final-integration gate rather than a task that must run after every feature commit or block ongoing implementation. The phase report records this exception explicitly; it does not turn deferred checks into passes. Visual/a11y and independent review also remain unverified, so there is no production/release sign-off.

## Next step

Present the Phase 0 report for review and wait for approval before beginning Phase 1. Keep all deferred runtime/UI/review gates visible in the project state.
