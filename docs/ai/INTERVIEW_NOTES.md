# Interview Notes

## Why the API has separate liveness and readiness endpoints

- **Liveness** answers: “Is the process responding?”
- **Readiness** answers: “Can this process safely serve the work it promises to handle?”
- During Phase 0, the API process can be alive while the database and scheduler do not exist. Returning `503 not_ready` is more honest than reporting operational readiness.

## Why default ports bind to loopback

The preview is meant for local development. Binding to `127.0.0.1` reduces the chance of accidentally exposing an unfinished dashboard to another device on a home, office, or school network.

## Why there is no fake monitoring data

Fake uptime or latency can mislead someone evaluating a monitoring tool. The UI uses explicit empty states until real samples or intentionally labeled demo fixtures are implemented.
