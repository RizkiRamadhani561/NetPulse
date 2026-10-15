# Contributing to NetPulse

Thanks for considering a contribution. NetPulse is under active development; check `docs/ai/PROJECT_STATE.md` and the relevant specification before changing code.

## Before opening a PR

1. Open or reference an issue for non-trivial work.
2. Keep changes focused on one feature ID and follow `AGENTS.md`.
3. Add or update tests before fixing behavior.
4. Run `bash ./scripts/verify.sh --quick`; run `--full` for phase-end work when the required tools are available.
5. Never include real credentials, internal network inventories, database dumps, or private logs.
6. Use Conventional Commit messages, for example `feat(CHK-01): add basic ping checker` or `docs(ai): record phase checkpoint`.

## Network safety

Tests must use loopback or the isolated Docker lab. Do not run scans against public, school, office, or third-party networks unless the operator has explicitly authorized the exact targets.

## Pull requests

Explain the intent, feature IDs, verification commands and outputs, known limitations, and any manual test steps. UI changes should include desktop and mobile screenshots plus accessibility findings.
