# Backend foundation

The API currently exposes a liveness endpoint and a deliberately unready readiness endpoint. Persistence and the scheduler are not configured yet, so readiness returns HTTP 503 by design.

- `GET /healthz` and `GET /api/v1/health`: process liveness.
- `GET /api/v1/ready`: returns `not_ready` until the database and scheduler have real health checks.

Do not add real monitoring or authentication behavior without a feature mini-spec and tests. The API must not invoke user-provided network targets through shell strings.
