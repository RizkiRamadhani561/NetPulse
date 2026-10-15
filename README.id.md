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

Hasil riset versi ada di [`docs/ai/RESEARCH.md`](docs/ai/RESEARCH.md). Lockfile dependensi belum dibuat karena registry paket tidak bisa dijangkau dari lingkungan penyusunan paket ini. Karena itu, build yang reproducible belum boleh diklaim.

## Persyaratan

- Docker Desktop dengan backend WSL 2 di Windows, atau Docker Engine + Compose di Linux
- Git
- Internet saat pertama kali membangun image/mengunduh dependensi

## Menjalankan preview lokal

1. Clone repository, lalu ekstrak/salin isi arsip Fase 0 ke root clone jika memakai arsip yang disiapkan.
2. Salin `.env.example` menjadi `.env` lewat PowerShell. File contoh tidak berisi kredensial; biarkan bagian rahasia kosong sampai fiturnya dibuat.

   ```powershell
   Copy-Item .env.example .env
   ```

3. Jalankan:

   ```powershell
   docker compose up --build
   ```

4. Buka [http://localhost:3000](http://localhost:3000). Endpoint liveness API ada di [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health).
5. Hentikan layanan dengan `docker compose down`.

Port dipasang ke `127.0.0.1` secara default, jadi belum terbuka ke perangkat lain di LAN.

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
