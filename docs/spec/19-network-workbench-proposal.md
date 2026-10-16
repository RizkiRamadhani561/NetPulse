# Network Workbench — Proposed Product Direction

**Status:** Proposal only — direction confirmed by the project owner; detailed scope and acceptance criteria still require review.  
**Implementation:** Not authorized by this document. Do not implement or change application code based on this proposal until the Phase 0 gates are reviewed and the owner explicitly approves the next implementation scope.

## 1. Owner-confirmed direction

- **Deployment:** Hybrid. A central self-hosted dashboard coordinates local/remote probes; probes make outbound connections to the central service and perform checks only within their authorized network scope.
- **Audience:** Both learners and professionals, with separate **Learning Mode** and **Professional Mode** experiences.
- **Project sequencing:** Phase 0 verification and approval remain mandatory. This proposal does not mark any Phase 0 gate as passed, authorize Phase 1, or override the deferred Docker/isolated-lab integration gate.

## 2. Product vision

Extend NetPulse from network monitoring into a network operations and learning workbench. A user should be able to move from an alert to a reproducible investigation: inspect monitoring evidence, run authorized diagnostics, analyze packet captures, record findings, and produce an incident report.

The workbench complements the existing monitoring product; it must not delay or destabilize the current MVP and v1 release path.

## 3. Two explicit modes

### 3.1 Learning Mode

Designed for students, beginners, and home-lab practice.

- Guided runbooks explain the purpose of each diagnostic step, expected observations, and what a result does or does not prove.
- Repeatable scenarios cover DNS failure, unreachable hosts, TCP connection failures, routing issues, packet loss, DHCP concepts, and TLS certificate problems.
- Prefer synthetic fixtures and an isolated lab for experiments that could disrupt a real network.
- Offer step-by-step tool output interpretation, glossary links, and a lab reset path.
- Clearly label simulated data and simulated results; never present them as observations from a live network.
- Provide a safe progression from guided checks to expert tools without silently widening target scope.

### 3.2 Professional Mode

Designed for authorized troubleshooting and operations.

- Fast access to device, site, probe, service, alert, incident, and diagnostic history.
- Structured results, timestamps, execution duration, target scope, probe identity, and exportable incident evidence.
- Runbooks can be used without introductory explanations; users can still open the reasoning and supporting evidence.
- Scans and captures must operate only on assets and interfaces the user is authorized to test.
- Preserve audit history and avoid changing device configuration by default.

The two modes should share the same backend permission model and safety controls. Learning Mode is not a security bypass, and Professional Mode is not a blanket authorization for arbitrary commands.

## 4. Hybrid architecture

Proposed logical flow:

1. **Central dashboard/API:** identity, roles, sites, assets, scope approval, job scheduling, result storage, audit events, and UI.
2. **Probe agent:** installed on a machine or network segment that can reach the relevant targets. It initiates outbound authenticated HTTPS connections; do not require inbound port forwarding by default.
3. **Job controller:** sends a versioned, structured job specification with an approved tool ID, normalized arguments, target scope, timeout, output limit, and expiry.
4. **Isolated tool runner:** executes supported tools with least privilege, bounded resources, and no access to the Docker socket or unrestricted host filesystem.
5. **Result pipeline:** normalizes output, redacts secrets where applicable, records provenance, and returns structured results to the dashboard.
6. **Optional lab runtime:** separate isolated environment for synthetic targets and repeatable exercises. Its runtime validation remains deferred according to the existing project decision.

Probe enrollment should use a one-time or short-lived enrollment token, followed by a unique revocable probe credential. Jobs must be authenticated, integrity-protected, replay-resistant, and scoped to the probe's configured site and allowed targets.

## 5. Terminal and command execution model

A terminal-like UI is a desired feature, but its execution boundary must be designed before implementation.

- **Diagnostic actions:** prefer typed tool calls with validated arguments rather than assembling shell strings.
- **Tool launcher:** offer named, versioned tools through a registry; each tool declares permitted arguments, required capability, target scope, timeout, output cap, and supported runner.
- **Interactive shell:** if offered, run only inside a disposable, isolated workbench/lab environment with a separate identity and resource limits. Never execute browser-supplied shell text directly in the central API process or on the host.
- **Live-network jobs:** use approved structured diagnostics and explicitly allowlisted read-only device commands. Do not expose unrestricted shell access to a production probe by default.
- **Process control:** support cancellation, bounded runtime, bounded stdout/stderr, concurrency quotas, and cleanup after disconnects or timeout.
- **Audit:** record actor, role, probe, tool, normalized arguments, approved scope, start/end time, exit status, and artifact references. Redact credentials and sensitive packet data.
- **Privilege:** run non-root by default; grant narrowly scoped capabilities only to tools that demonstrably require them.

The UX may look like CMD, PowerShell, or a Linux terminal, but the available commands must reflect the selected runner and platform. Do not imply that PowerShell exists on a Linux runner or that all host interfaces are visible from a container.

## 6. Candidate tool families

These are candidates for research and staged approval, not a commitment to install all tools.

| Family | Candidate tools | Initial use |
|---|---|---|
| Core diagnostics | ping, traceroute, MTR, dig/nslookup, TCP/HTTP/TLS checks | Routine troubleshooting |
| Discovery and port/service inventory | Nmap | Authorized, rate-limited host and service discovery |
| Packet analysis | TShark, tcpdump; export to Wireshark desktop | Analyze approved PCAP/PCAPNG files; live capture only where the probe has explicit interface permissions |
| Performance | iperf3 | Throughput tests between explicitly configured endpoints; avoid unbounded tests |
| TLS inspection | testssl.sh or a reviewed equivalent | Read-only configuration inspection of authorized endpoints |
| Device access | SSH via a maintained library and command allowlist; vendor APIs | Read-only configuration/status inspection by default |
| Network source of truth | Optional NetBox integration | Import/synchronize inventory only after ownership, credentials, and conflict behavior are defined |

For each dependency, verify maintenance status, license compatibility with NetPulse's MIT license, provenance, platform support, image size, privilege requirements, and update process before adoption. No candidate is assumed to be installed or available in the current implementation.

## 7. Scope and safety controls

- Default scan scope remains private address space and explicitly enrolled assets; public targets require a deliberate, auditable authorization path if that capability is ever approved.
- Enforce target validation server-side and again at the probe. Resolve hostnames carefully and defend against SSRF, DNS rebinding, redirects to disallowed networks, and access to cloud metadata endpoints.
- Apply per-user, per-probe, and per-target rate/concurrency limits, job expiry, cancellation, and quotas.
- No brute-force, credential spraying, exploit automation, flooding, stealth/evasion, or destructive actions.
- No configuration writes to network devices in the initial workbench. Existing read-only principles remain in force.
- Packet captures may contain credentials, personal data, or business-sensitive traffic. Require explicit capture authorization, short default retention, access controls, safe download, and documented deletion.
- Keep probe credentials, SNMP credentials, and device secrets out of logs, terminal history, job arguments, and artifacts.
- Display an authorization reminder and exact target scope before launching a scan or capture.
- Separate demo/lab evidence from live-network evidence throughout the UI, API, and exports.

## 8. Suggested delivery sequence (proposed, not yet adopted)

This is a candidate ordering to discuss after the existing Phase 0 gate. It does not renumber or supersede the official phase table in docs/spec/16-cara-kerja-fase-dan-gerbang.md.

1. **Workbench foundations:** tool registry, permission model, job lifecycle, structured output, audit events, timeout/cancellation, and threat model.
2. **Core diagnostic workflows:** existing TOOLS scope plus investigation timeline and guided runbooks.
3. **Hybrid probe foundation:** enrollment, outbound authenticated transport, scope policy, offline buffer, heartbeat, revocation, and version compatibility.
4. **Learning lab:** isolated repeatable scenarios and explicit simulated-data labeling; verify runtime only at the already agreed integration point.
5. **Discovery integration:** Nmap-backed, bounded discovery and inventory promotion after license/security review.
6. **Packet analysis:** PCAP/PCAPNG upload and TShark analysis first; UI packet explorer next; live capture only after interface permissions, retention, and isolation tests pass.
7. **Professional workflows:** incident evidence bundles, exports, role-based approvals, and operator-focused UX.
8. **Optional interactive shell:** only after isolation, threat modeling, authorization, cancellation, audit, and adversarial tests have passed.

Do not delay v1.0.0 for these proposed post-v1 capabilities. The exact release mapping must be reconciled with the existing P0/P1/P2 priorities before any implementation begins.

## 9. Definition of ready for implementation

Before starting a workbench feature, create a reviewed ADR and testable Given/When/Then acceptance criteria in docs/ai/TRACEABILITY.md. At minimum, agree on:

- Supported deployment and probe platforms.
- Trust boundary and threat model for central server, probe, and runner.
- Permission matrix for Admin, Operator, Viewer, and any future lab user.
- Authorized target-scope representation and enforcement.
- Tool registry schema and output normalization.
- Secret redaction, audit retention, PCAP handling, and data deletion.
- Time/resource limits and cancellation behavior.
- Dependency/license review and reproducible tool images.
- Unit, integration, adversarial, browser/accessibility, and runtime tests.
- Evidence required for each acceptance criterion and the applicable phase gate.

## 10. Explicit non-goals for this proposal

- No application code changes or dependency installation.
- No enabling unrestricted shell on the central server or production probe.
- No unrestricted public scanning or offensive automation.
- No claim that Nmap, Wireshark/TShark, tcpdump, or any other candidate tool is currently integrated.
- No change to Phase 0 status, Docker/lab deferral, release gates, or phase approval process.
