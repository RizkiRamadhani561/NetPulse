# NetPulse

**Feel the pulse of your network.**

NetPulse dirancang sebagai dashboard monitoring jaringan yang ringan dan self-hosted untuk home lab, kantor kecil, sekolah, dan tim IT support. Targetnya mencakup pengecekan uptime/latensi, metrik SNMP, discovery, riwayat insiden, dan notifikasi Telegram dengan pemasangan yang mudah dipahami pemula.

> **Status proyek: fondasi Fase 0.** Repository ini baru berisi kerangka proyek dan tampilan dashboard awal. Monitoring perangkat, autentikasi, penyimpanan, notifikasi, dan discovery belum diimplementasikan. Jangan buka preview ini ke jaringan yang tidak tepercaya dan jangan gunakan sebagai sistem monitoring produksi.

## Stack yang direncanakan

- **API:** Python 3.14, FastAPI, Uvicorn
- **Database:** SQLite mode WAL, SQLAlchemy, Alembic; PostgreSQL sebagai opsi tahap berikutnya
- **Web:** Next.js App Router, TypeScript strict, React, Tailwind CSS, Storybook
- **Runtime:** Docker Compose, dengan profil lab terisolasi
- **Quality:** pytest, Ruff, pengecekan TypeScript, Playwright, Gitleaks, audit dependensi

Hasil riset versi ada di [`docs/ai/RESEARCH.md`](docs/ai/RESEARCH.md). Lockfile `backend/uv.lock` dan `frontend/package-lock.json` sudah di-commit dan dipakai CI melalui `uv sync --locked` serta `npm ci`. Build terbaru tetap harus dibuktikan oleh hasil CI, bukan hanya karena lockfile tersedia.

## Persyaratan

- Docker Desktop dengan backend WSL 2 di Windows, atau Docker Engine + Compose di Linux
- Git
- Internet saat pertama kali membangun image/mengunduh dependensi

## Pratinjau Docker (ditunda ke integrasi akhir)

Konfigurasi Compose tersedia, tetapi pengujian runtime sengaja ditunda sampai fitur sistem selesai dan pemeriksaan kode stabil. Jangan anggap preview container sudah tervalidasi. Pada tahap integrasi akhir, salin `.env.example` menjadi `.env`, jalankan `docker compose up --build`, cek dashboard/API, lalu hentikan dengan `docker compose down`. Port layanan dirancang hanya terikat ke `127.0.0.1` agar tidak terbuka ke LAN secara default.

## Verifikasi lokal

Di Windows PowerShell:

```powershell
./scripts/verify.ps1 -Mode quick
./scripts/verify.ps1 -Mode full
```

Dari Git Bash atau WSL, gunakan `bash ./scripts/verify.sh --quick` atau `bash ./scripts/verify.sh --full`. Pemeriksaan cepat memvalidasi file inti, parsing JSON/TOML, kesamaan key terjemahan, dan beberapa konvensi keamanan/desain. Verifikasi penuh membutuhkan lockfile yang sudah diselesaikan, Docker/Node, dependensi tes Python, serta Gitleaks; pemeriksaan yang tidak tersedia tidak dianggap lulus.

## Lab jaringan

Overlay compose lab dirancang agar layanan dummy hanya berada di jaringan Docker internal. Lab tidak aktif lewat perintah `docker compose up` biasa. Baca [`lab/README.md`](lab/README.md) sebelum menjalankannya.

## Keamanan dan privasi

Tidak ada telemetry yang direncanakan. Jangan commit `.env`, file database, backup, kredensial SNMP/router, atau token. Baca [`SECURITY.md`](SECURITY.md) sebelum melaporkan celah keamanan. Fitur pemindaian akan dibatasi ke jaringan privat secara default dan harus digunakan hanya pada jaringan yang diizinkan.

## Kontribusi dan lisensi

Baca [`CONTRIBUTING.md`](CONTRIBUTING.md). Lisensi proyek adalah MIT; lihat [`LICENSE`](LICENSE).
