---
name: verify
description: Run NetPulse verification checks and report evidence without hiding failures.
allowed-tools: Bash(./scripts/verify.sh *)
---

1. Run `bash ./scripts/verify.sh --quick` during normal work.
2. Run `bash ./scripts/verify.sh --full` at phase end after the lockfiles and required tools are available.
3. Read the generated evidence and list missing or skipped checks explicitly.
4. For failures, reproduce first, add a meaningful failing test, fix the root cause, and re-run.
5. Never lower coverage thresholds, disable hooks, use `--no-verify`, or manufacture passing output.
6. Update `docs/ai/TRACEABILITY.md`, `PROJECT_STATE.md`, and `SESSION_LOG.md` with honest statuses.
