# Phase 0 Research Notes

Research checked on **2026-10-16 (WIB)**. Links are maintained for re-checking; package versions can change before dependencies are locked. “Latest” means the latest stable version visible from the cited source at the time of research, not a promise that it remains latest later.

## 1. Runtime and UI dependency candidates

| Component | Candidate | Finding / rationale | Source |
|---|---|---|---|
| Python | 3.14 | Python 3.15.0 became stable on 2026-10-09, but it is very new. Use 3.14 for a more conservative initial compatibility target, then re-evaluate once the full package graph is resolved. | [Python 3.15 release](https://blog.python.org/2026/10/python-3150-final-is-here/) |
| FastAPI | 0.143.2 | PyPI showed 0.143.2 uploaded 2026-10-15. The exact API behavior must still be validated with the pinned Python version and resolved dependencies. | [PyPI FastAPI](https://pypi.org/project/fastapi/) |
| SQLAlchemy | 2.1.4 | Current 2.1 release, uploaded 2026-10-07; requires Python >=3.11. | [PyPI SQLAlchemy 2.1.4](https://pypi.org/project/SQLAlchemy/2.1.4/) |
| Node.js | 24.22.0 LTS | Use the LTS line instead of the Current line for less runtime churn. Node 26 is listed as Current at this research date. | [Node.js downloads](https://nodejs.org/en/download), [release schedule](https://github.com/nodejs/Release/blob/main/README.md) |
| Next.js | 16.4.0 | The Next.js team announced 16.4 on 2026-10-06, including React 19.3 features. | [Next.js blog](https://nextjs.org/blog) |
| React / React DOM | 19.3.0 | React 19.3 was announced on 2026-09-09 and is listed as the latest version. | [React 19.3](https://react.dev/blog/2026/09/09/react-19-3), [React versions](https://react.dev/versions) |
| Tailwind CSS | 4.3.3 | npm showed Tailwind 4.3.3 as latest at check time. | [npm Tailwind CSS](https://www.npmjs.com/package/tailwindcss) |
| shadcn/ui | Add only when needed | Official docs support Tailwind v4 and React 19. Do not import a component registry before checking the exact component source/license and verifying installation output. | [shadcn Tailwind v4](https://ui.shadcn.com/docs/tailwind-v4) |
| Playwright | 1.64.1 | npm showed 1.64.1 as the latest stable tag; 1.65 prereleases were not selected. | [npm Playwright Test](https://www.npmjs.com/package/%40playwright/test) |
| Storybook | 10.6.2 | npm showed 10.6.2. Official docs recommend the Vite-based Next.js framework for most projects. Compatibility still needs actual install/build verification. | [npm Storybook](https://www.npmjs.com/package/storybook), [Next.js + Vite framework](https://storybook.js.org/docs/get-started/frameworks/nextjs-vite) |
| Ruff | 0.17.1 | PyPI showed 0.17.1 uploaded 2026-10-15. | [PyPI Ruff](https://pypi.org/project/ruff/) |

**Locking limitation:** package-registry access timed out in the preparation environment. `frontend/package.json` and `backend/pyproject.toml` record the selected direct dependencies, but `frontend/package-lock.json` and `backend/uv.lock` have intentionally not been fabricated. Do not call the build reproducible until both are generated and reviewed.

## 2. PySNMP and lab simulator

- PySNMP 7.1.30 was listed on PyPI with a 2026-09-28 release. That indicates ongoing releases; its API is still to be exercised before adding a production SNMP poller.
- `snmpsim` 1.2.2 was listed on PyPI with a 2026-04-26 release and a production/stable classifier. The lab image pins that simulator version, but its container build and CLI arguments have not been executed here.
- SNMP v2c and v3 implementation must be verified against the official docs/package API during the SNMP phase. Never store community strings in logs or fixtures.

Sources: [PySNMP on PyPI](https://pypi.org/project/pysnmp/), [snmpsim 1.2.2 on PyPI](https://pypi.org/project/snmpsim/).

## 3. ICMP and Docker Desktop networking

- Docker Desktop runs the Docker Engine in a lightweight Linux VM; outbound container traffic is routed through the platform backend.
- Docker host-networking support on Docker Desktop is an opt-in feature (version 4.34+) and the documented path is Layer 4 TCP/UDP. It must not be relied on for raw ICMP.
- Therefore `network_mode: host` is not a Windows default. The main API/web containers are not granted `NET_RAW`. When ping is implemented, use a dedicated checker worker and verify permissions (`NET_RAW`, `net.ipv4.ping_group_range`) in Linux; provide a TCP fallback for environments where ICMP is blocked.
- Do not test against office/school networks in CI. All automated network tests must use loopback or the internal Docker lab.

Sources: [Docker Desktop networking](https://docs.docker.com/desktop/features/networking/), [Docker host networking limitations](https://docs.docker.com/engine/network/drivers/host/).

## 4. Server-Sent Events (SSE)

- FastAPI's current documentation covers `EventSourceResponse` and `ServerSentEvent`; the built-in feature was added in FastAPI 0.135.0.
- Its documented defaults include a ping comment every 15 seconds, `Cache-Control: no-cache`, and `X-Accel-Buffering: no` to avoid Nginx buffering.
- When `/api/v1/stream` is implemented, preserve `Last-Event-ID`, authorize stream sessions/tokens, use heartbeat messages, and test reconnects. Reverse proxy/read timeout and per-browser connection limits still need design validation.

Sources: [FastAPI SSE documentation](https://fastapi.tiangolo.com/tutorial/server-sent-events/), [Nginx proxy buffering](https://nginx.org/en/docs/http/ngx_http_proxy_module.html).

## 5. Telegram Bot API limits

Official Telegram bot FAQ currently advises no more than about one message/second in a single chat, up to 20 messages/minute in a group, and about 30 broadcasts/second for free bulk broadcasts. A notifier must handle HTTP 429 and `retry_after`, queue/batch messages where safe, and avoid sending repeat alerts on every failed poll.

Source: [Telegram Bots FAQ](https://core.telegram.org/bots/faq).

## 6. Accessibility baseline

- Use WCAG 2.2 AA as the UI target. WCAG 2.2 became a W3C Recommendation on 2023-10-05; the W3C publication history records a further Recommendation on 2024-12-12.
- Initial CSS includes visible keyboard focus, reduced-motion handling, and labels/text beyond color alone. This is only a starting point; run axe plus keyboard/manual reviews at UI feature time.

Sources: [W3C WCAG 2.2 Recommendation](https://www.w3.org/WAI/news/2023-10-05/wcag22rec/), [WCAG 2.2 publication history](https://www.w3.org/standards/history/WCAG22/).

## 7. Authentication/security verification

Use OWASP ASVS 5.0.0 (latest stable noted by the project) as a checklist for authentication, session management, authorization, cryptography, input validation, and error handling. Do not treat this as a claim of ASVS conformance until requirements are mapped to tests/evidence.

Source: [OWASP ASVS releases](https://github.com/OWASP/ASVS/releases), [OWASP ASVS project](https://github.com/OWASP/ASVS).

## 8. Secrets and GitHub Actions

- Gitleaks CLI v8.30.1 was visible on the project release listing; the official GitHub Action has a v3 line using Node 24. The previous v2 runtime no longer works on GitHub-hosted runners after the documented September 2026 removal of Node 20.
- Configured Gitleaks in `.pre-commit-config.yaml` and `.github/workflows/ci.yml`. Neither has been run yet in this preparation environment.
- Before v1.0.0, review and pin third-party GitHub Actions to exact commit SHAs, verify their permissions, and enable GitHub secret scanning + push protection manually if available. These repository settings have not been changed.

Sources: [Gitleaks releases](https://github.com/gitleaks/gitleaks/releases), [Gitleaks Action v3 migration](https://github.com/gitleaks/gitleaks-action/releases).

## 9. Competitor scan (public docs only; no code or copy reused)

| Project | Publicly documented emphasis | Initial lesson for NetPulse |
|---|---|---|
| Uptime Kuma | Self-hosted uptime/service monitoring with a web UI and notification integrations. | Minimize time-to-first-check and make setup easy for a beginner. |
| LibreNMS | Network monitoring and customizable dashboards/widgets. | Network-specific metrics and dashboards are differentiators, but configuration complexity should be controlled. |
| Gatus | Configuration-driven service health checks and status. | Keep checks declarative and testable; document every check type clearly. |
| Beszel | Lightweight server monitoring. | Keep resource use and installation friction low. |

This is a product-direction scan, not a benchmark or proof of comparative superiority. Revisit with hands-on installation and feature tests before writing comparison claims on a public landing page.

Sources: [Uptime Kuma](https://github.com/louislam/uptime-kuma), [LibreNMS dashboard docs](https://docs.librenms.org/Extensions/Dashboards/), [Gatus](https://github.com/TwiN/gatus), [Beszel](https://github.com/henrygd/beszel).

## 10. Decisions carried forward

1. Use Node 24 LTS and Python 3.14 as conservative starting points; revisit all pins during dependency lock generation.
2. Use SQLAlchemy 2.1 series based on current official release metadata; add Alembic migration tooling when persistence enters Phase 1.
3. Keep raw-packet/network capabilities out of the API/web containers.
4. Use an internal-only lab network and synthetic SNMP fixture data.
5. No telemetry, no real secrets in example files, and no public-network scan defaults.
