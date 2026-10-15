# Known Bugs and Blockers

## Open blockers

| ID | Severity | Status | Summary | Evidence / next action |
|---|---|---|---|---|
| BUG-001 | High | Open | Dependency lockfiles are missing because package registries were unreachable during preparation. | Generate/review `backend/uv.lock` and `frontend/package-lock.json` on a network-enabled machine, then run full verification. |
| BUG-002 | High | Open | Docker build and startup have not been tested in the current environment. | Run the default Compose stack and the lab overlay on Docker Desktop for Windows. |
| BUG-003 | Medium | Open | Storybook configuration and package compatibility have not been verified by installation/build. | Install from the locked frontend graph, run `npm run storybook` and `npm run build-storybook`. |

No other issue is considered verified closed by this archive.
