# Skills / tools registry

No third-party skills, MCP servers, or plugins were installed as part of Phase 0 preparation.

| Item | Source / version | Review status | Use |
|---|---|---|---|
| Gitleaks pre-commit hook | `gitleaks/gitleaks`, `v8.30.1` | ⚠️ Configured, not executed in this environment | Secret scanning before commit |
| Gitleaks GitHub Action | commit `e0c47f4f8be36e29cdc102c57e68cb5cbf0e8d1e` | ✅ Passed in [run 38851350669](https://github.com/RizkiRamadhani561/NetPulse/actions/runs/38851350669); pinned in CI | CI secret scan |

Before release, pin external GitHub Actions to reviewed commit SHAs and verify license, provenance, and permissions. Do not install extra skills/MCPs from untrusted registries.


The CI workflow pins checkout, setup-python, setup-node, and Gitleaks Action to the full commit SHAs observed in the successful workflow run on 2026-10-16. Re-review these pins before a major upgrade; do not replace them with floating tags without review.
