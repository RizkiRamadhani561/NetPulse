# Changelog

All notable changes will be documented here. No version has been released.

## Unreleased — Phase 0 foundation

- Added the FastAPI liveness/readiness shell and bilingual Next.js dashboard with honest empty states.
- Added Docker Compose development definitions and an opt-in internal lab overlay with synthetic HTTP/SNMP fixtures.
- Added repository instructions, split specifications, architecture decisions, research records, phase memory, contributor/security guidance, and local verification skills/agents.
- Committed resolver-generated backend/frontend lockfiles; CI enforces locked installs.
- Added backend contract/safety tests; Ruff, mypy, coverage, pip-audit, TypeScript, Next.js and Storybook builds, npm audit, and Gitleaks.
- Added a cross-platform verification runner that writes per-step logs and a Markdown report. CI uses the same quick-verification entry point as local use.
- Pinned GitHub Actions to full commit SHAs and Gitleaks CLI to 8.30.1.
- Regular non-container checks passed in [GitHub Actions run 38851788088](https://github.com/RizkiRamadhani561/NetPulse/actions/runs/38851788088).
- Remaining: user-deferred Docker Compose/lab runtime integration, browser screenshots and axe/keyboard review, clean Windows full-runner validation, and independent review. This foundation is not production-ready and no release has been published.
