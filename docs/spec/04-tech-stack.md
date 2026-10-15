# 4. TECH STACK

> Versi: gunakan **versi stabil terbaru yang kompatibel**, verifikasi di dokumentasi resmi pada saat Fase 0 (Bagian 14.9), lalu kunci di lockfile. Jangan menebak nama atau versi paket dari ingatan.

| Lapisan | Pilihan | Catatan |
|---|---|---|
| Backend API | Python 3.12+ · FastAPI · Uvicorn · Pydantic v2 | async di mana masuk akal |
| Worker | Proses terpisah (image yang sama, command berbeda) untuk scheduler, poller, scanner, notifier | API tidak boleh terblokir oleh jaringan lambat |
| Database | SQLite (default, mode WAL) via SQLAlchemy 2.0 + Alembic | Rancang agar bisa pindah ke PostgreSQL (profil compose `postgres`); TimescaleDB opsional untuk skala besar |
| Antrian/event | Event bus internal (in-process) di balik interface; Redis opsional hanya bila terbukti perlu | Mulai sederhana |
| Scheduler | APScheduler atau runner asyncio sendiri | Jitter + batas konkurensi |
| Ping | `icmplib` | Fallback TCP ping bila ICMP tidak diizinkan |
| SNMP | `pysnmp` (pakai distribusi yang aktif dirawat; verifikasi) | v2c + v3 |
| Discovery | `scapy` (ARP) atau `python-nmap` + tabel OUI lokal | Tanpa API vendor eksternal |
| SSH/Config | `paramiko` / `netmiko` | Allowlist perintah read-only |
| MikroTik | `routeros-api` | Read-only dulu |
| Real-time | Server-Sent Events (`sse-starlette` atau manual) | Perhatikan buffering di reverse proxy |
| Auth | `argon2-cffi`, `pyotp` (TOTP), `py_webauthn`, `authlib` (OIDC) | Sesuai fitur SEC |
| Push | `pywebpush` (VAPID) | Gratis |
| Observability | `structlog`, `prometheus-client` | JSON log + redaksi rahasia |
| Frontend | Next.js (App Router) · TypeScript strict · Tailwind CSS · shadcn/ui (Radix) · lucide-react | |
| Data/state | TanStack Query · Zustand (seperlunya) · React Hook Form + Zod | |
| Visual | Recharts (waktu), `@xyflow/react` (topologi), `react-grid-layout` + `@dnd-kit` (dashboard kustom), `cmdk` (command palette), `sonner` (toast) | Semua harus punya alternatif keyboard |
| i18n | `next-intl` (ID + EN) | |
| Komponen | Storybook + addon a11y | Katalog komponen dan uji visual |
| Container | Docker multi-stage · docker compose dengan profil: `default`, `postgres`, `proxy` (Caddy, HTTPS otomatis), `lab` (simulator), `monitoring` (Prometheus + Grafana) | Non-root bila mungkin |
| CI/CD | GitHub Actions | lint, type, test, e2e, a11y, Lighthouse, secret scan, audit, build, publish ke GHCR |
| Test | pytest + pytest-asyncio + `hypothesis` (property) · Vitest + Testing Library · Playwright (+ axe) · `k6` atau Locust (beban) | |
| Keamanan | gitleaks · pip-audit · npm/pnpm audit · bandit · semgrep · trivy (image) | |
| Lint/format | ruff + mypy · ESLint + Prettier | |
| Simulasi | `snmpsim` + kontainer dummy (profil `lab`) | Bagian 5.29 |
| Docs & landing | Next.js route terpisah **atau** Astro; deploy ke Vercel/GitHub Pages | |

**Aturan memilih dependensi:** lebih sedikit lebih baik. Sebelum menambah paket: pastikan **benar-benar ada** di registry resmi, dirawat (rilis/commit terbaru), lisensi kompatibel, tidak punya CVE terbuka yang serius, dan versinya dikunci. Catat di `docs/ai/DECISIONS.md` bila signifikan.

---
