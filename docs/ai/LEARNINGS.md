# Learnings

- Docker Desktop for Windows runs Linux containers in a lightweight VM; do not assume Linux host-network or raw-ICMP semantics are identical. See the official Docker networking notes in `RESEARCH.md`.
- The API liveness endpoint is not a readiness signal. `/api/v1/ready` should stay non-ready until its real database and scheduler dependencies are checked.
- A dashboard without collected samples should render an empty state, not fabricated uptime/latency values.
- The dependency lockfiles are committed and enforced by CI: Python uses `uv sync --locked`; frontend uses `npm ci`.
- Keep local verification cross-platform by routing PowerShell and Bash entry points through one Python runner. Save logs/report for each run, and never count deferred Docker checks as passing.
