# Frontend

Next.js dashboard shell for the NetPulse Phase 0 foundation. Indonesian is the default interface language; use the top-right language toggle to switch to English.

The dashboard intentionally displays empty metric states. Device registration, monitoring, charts backed by samples, incidents and alert settings are not implemented yet.

From the repository root, run `docker compose up --build` after copying `.env.example` to `.env`. For direct development, use Node.js 24 LTS and install the dependencies with npm. A committed package lockfile is still pending, so the dependency graph is not yet reproducible.
