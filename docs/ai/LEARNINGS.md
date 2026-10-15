# Learnings

- Docker Desktop for Windows runs Linux containers in a lightweight VM; do not assume Linux host-network or raw-ICMP semantics are identical. See the official Docker networking notes in `RESEARCH.md`.
- The API liveness endpoint is not a readiness signal. `/api/v1/ready` should stay non-ready until its real database and scheduler dependencies are checked.
- A dashboard without collected samples should render an empty state, not fabricated uptime/latency values.
- The project scaffold has been committed to GitHub. Lockfiles and runtime/build checks are still pending.
