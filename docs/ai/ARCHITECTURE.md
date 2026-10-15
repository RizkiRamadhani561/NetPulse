# Architecture — Phase 0

## Current shape

```text
Browser (127.0.0.1:3000)
  └── Next.js dashboard shell (ID/EN label toggle, empty state only)

API (127.0.0.1:8000)
  ├── GET /healthz and /api/v1/health → liveness
  └── GET /api/v1/ready → not_ready until DB + scheduler exist

Optional isolated Docker lab (not started by default)
  ├── lab-http (synthetic HTTP response)
  └── snmp-simulator (synthetic SNMP records)
```

## Planned data path for Phase 1

A scheduler will enqueue due checks for a device. A worker executes one checker (ICMP with a safe platform-aware implementation, or a TCP fallback), validates the result, and writes a timestamped sample. A state machine debounces consecutive failures before changing status. State transitions become incident events. A notifier consumes those events and sends alerts through the configured channel while respecting rate limits and retries. The API exposes stored summaries and SSE events to the UI.

This path is architectural intent, not implemented behavior yet.

## Boundaries

- API and web containers do not receive raw-packet capabilities.
- The default web/API ports bind to loopback.
- The lab overlay isolates synthetic targets from the host/LAN and is not active by default.
- No telemetry is planned. Secrets stay server-side and are never put into `NEXT_PUBLIC_*` variables.
- Database engine, migrations, scheduler, checkers, auth, and SSE are deferred to their feature phases.
