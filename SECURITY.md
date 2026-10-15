# Security Policy

## Project status

NetPulse is in Phase 0. The current preview is not a production monitoring service and must not be exposed to untrusted networks.

## Reporting a vulnerability

Please do not report exploitable details in a public issue. Use GitHub's private vulnerability reporting for this repository if it is enabled, or contact the repository owner privately through GitHub and ask for a secure reporting channel. Include the affected version/commit, impact, reproduction steps, and any mitigations you know. Do not include real secrets or unrelated personal data.

## Supported versions

Only the current development branch is expected to receive fixes before v1.0.0. A formal release support policy will be added before the first stable release.

## Security boundaries

- Keep `.env` local and never commit credentials, device community strings, tokens, or private logs.
- Default services bind to loopback.
- Network tests must target loopback or the isolated Docker lab unless the user explicitly authorizes another target.
- Scanning must only be used on networks the operator owns or is authorized to monitor.
- No production security claim is made for the Phase 0 skeleton.
