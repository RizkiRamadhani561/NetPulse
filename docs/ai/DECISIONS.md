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

- **Status:** SUPERSEDED by commit [285a8b6](https://github.com/RizkiRamadhani561/NetPulse/commit/285a8b6d3154284c3308e82b80b52f60ae24cbb1).
- **Context:** The preparation environment initially could not reach npm/PyPI, so resolver-generated lockfiles could not honestly be created there.
- **Decision:** Do not hand-write or fabricate lockfile metadata. Later, GitHub Actions successfully resolved and committed `backend/uv.lock` and `frontend/package-lock.json`; locked installs are now mandatory.
- **Consequence:** The original limitation is historical. Continue verifying the committed graph with `uv sync --locked`, `npm ci`, and dependency audits.

## ADR-006 — Defer Docker runtime integration to the final system stage

- **Status:** Accepted on 2026-10-16 at the user's direction.
- **Context:** The initial Compose smoke exposed a Next.js generated-file permission failure and repeated integration retries were interrupting regular feature work.
- **Options:** A) Keep Compose smoke on every push; B) disable Docker validation entirely; C) retain the smoke but run it manually after backend, frontend, and secret checks pass.
- **Decision:** C. Regular CI validates code, tests, type checks, builds, audits, and secrets. The Docker Compose smoke job runs only via manual `workflow_dispatch` and depends on those checks.
- **Consequence:** Docker testing is deferred, not waived. The Phase 0 integration gate remains open until the manual container smoke passes at the agreed final-integration point.

## ADR-007 — Dashboard visual system and motion (accepted 2026-10-17)

- **Context:** The Phase 0 dashboard needs a coherent visual foundation before monitoring modules are implemented; the UI must not imply live telemetry or make planned controls appear functional.
- **Decision:** Use Space Grotesk for headings, Inter for interface copy, and IBM Plex Mono for technical labels. Keep slate surfaces and `#54D8B6` as the primary accent. Reserve `#D93A2F` for true critical/destructive states, pairing it with `#FF8B80` text when the surface requires it.
- **Motion:** Short 140/180/260 ms transitions and a restrained entry cue; no persistent decorative animation. Respect `prefers-reduced-motion`.
- **Interaction:** Only implemented controls look interactive. Planned modules remain disabled; preview metrics remain empty until data is real. This ADR does not mark UX-04, runtime integration, or production readiness as complete.
