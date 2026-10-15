# Skills / tools registry

No third-party skills, MCP servers, or plugins were installed as part of Phase 0 preparation.

| Item | Source / version | Review status | Use |
|---|---|---|---|
| Gitleaks pre-commit hook | `gitleaks/gitleaks`, `v8.30.1` | ⚠️ Configured, not executed in this environment | Secret scanning before commit |
| Gitleaks GitHub Action | `gitleaks/gitleaks-action@v3` | ⚠️ Configured, not executed in CI | CI secret scan |

Before release, pin external GitHub Actions to reviewed commit SHAs and verify license, provenance, and permissions. Do not install extra skills/MCPs from untrusted registries.
