# Architecture Decisions

## ADR-001 — SQLite first, SQLAlchemy abstraction (proposed)

- **Status:** Accepted for the initial architecture; persistence not implemented yet.
- **Context:** NetPulse should be easy to run locally and from Docker Compose before it needs multi-node database operations.
- **Decision:** Use SQLite in WAL mode as the default. Use SQLAlchemy models and Alembic migrations so a PostgreSQL profile can be added later.
- **Alternatives:** PostgreSQL as the only default (heavier first setup); direct SQL (less migration/ORM structure).
- **Consequence:** Retention and history tables must be designed around UTC timestamps and indexes such as `(device_id, timestamp)`; actual WAL/migration tests belong to Phase 1.

## ADR-002 — Docker Desktop uses bridge networking by default

- **Status:** Accepted.
- **Context:** Windows with Docker Desktop runs Linux containers inside a lightweight VM. Host networking on Docker Desktop has Layer 4 TCP/UDP constraints and must not be treated as equivalent to Linux host networking for raw ICMP.
- **Decision:** Default services bind their published ports to `127.0.0.1`. The opt-in lab uses an internal-only Docker network. Monitoring-worker network capabilities will be reviewed separately when ICMP is implemented.
- **Consequence:** Do not grant `NET_RAW` to the web or API containers. Investigate a dedicated checker worker plus TCP fallback before real device monitoring.

## ADR-003 — Demo data must not be an exclusive mode

- **Status:** Product constraint confirmed; exact UX/seed implementation pending.
- **Context:** The user wants demo content and real device monitoring to coexist during the MVP.
- **Decision:** Design the later demo feature so demo devices/data can appear alongside user-added real devices. Avoid a global mode switch that disables real monitoring unless the user explicitly changes this constraint.
- **Consequence:** Revisit the meaning of `DEMO_MODE` before using it as a runtime switch or first-run wizard option.

## ADR-004 — No external network mode or scan on by default

- **Status:** Accepted.
- **Context:** The tool will target both home labs and authorized office/school networks; a public repository should fail safe.
- **Decision:** No scan runs automatically. `ALLOW_PUBLIC_SCAN` remains disabled unless the future security model explicitly allows a target. Network tests use loopback or the isolated lab.
- **Consequence:** Implement strict IP/CIDR/URL validation, rate/concurrency limits, and SSRF protections before scan or HTTP-check features are exposed.

## ADR-005 — Do not fake lockfiles

- **Status:** Accepted for this preparation artifact.
- **Context:** The preparation environment could not reach npm/PyPI; a complete resolver-generated lockfile cannot be honestly produced without dependency metadata.
- **Decision:** Keep manifests, record exact verified direct versions where available, and leave lockfiles absent until they can be generated and reviewed online. Full verification must remain blocked until lockfiles exist.
- **Consequence:** This archive is not yet a reproducible build and Phase 0 is not complete.
