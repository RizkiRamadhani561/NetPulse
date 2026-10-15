# 7. LANDING PAGE & DOKUMENTASI

**Tujuan:** meyakinkan pengunjung dalam 10 detik dan mengarahkan ke GitHub star / instalasi.

**Struktur section (urut):**
1. **Navbar** — logo, Fitur, Demo, Docs, GitHub (dengan jumlah star), toggle tema & bahasa.
2. **Hero** — headline besar: *"Feel the pulse of your network."* Subheadline: *"Dashboard monitoring jaringan open source yang ringan, cantik, dan siap dipakai dalam satu perintah."* Dua tombol: **Get Started** dan **⭐ Star on GitHub**. Di bawahnya blok kode salin-satu-klik: `docker compose up -d`. Di sisi kanan/bawah: mockup dashboard (screenshot dari mode demo) dalam bingkai browser dengan animasi masuk halus.
3. **Bukti sosial/lencana** — lisensi MIT, versi rilis, status CI, jumlah star, Docker pulls.
4. **Fitur utama (grid 3×2)** — Uptime & Latency, SNMP Bandwidth, Network Discovery, Alert Telegram, Peta Topologi, Integrasi MikroTik. Tiap kartu: ikon, judul, 1–2 kalimat, mini screenshot.
5. **Demo interaktif** — iframe/embedded mode demo atau GIF 10–15 detik yang menunjukkan perangkat DOWN → alert Telegram → pulih.
6. **Cara kerja (3 langkah)** — 1) Clone & `docker compose up`, 2) Buat admin & tambah perangkat, 3) Terima alert di Telegram. Dengan blok kode.
7. **Perbandingan singkat** — tabel NetPulse vs Zabbix vs Uptime Kuma vs LibreNMS (jujur, hanya klaim yang bisa dipertanggungjawabkan).
8. **Privasi & keamanan** — self-hosted, data tetap milikmu, tanpa telemetry, rahasia lewat `.env`, kredensial terenkripsi.
9. **Roadmap** — daftar fitur selesai / sedang dikerjakan / rencana, tautan ke GitHub Issues.
10. **FAQ** — Apakah gratis? Butuh akses root? Jalan di Windows/Raspberry Pi? Mendukung SNMP v3? Bagaimana keamanan data? Cara berkontribusi?
11. **CTA akhir** — ajakan star + kontribusi + tautan Discussions.
12. **Footer** — tautan, lisensi, dibuat oleh [nama pemilik], sosial.

**Persyaratan teknis landing page:** responsif penuh, dark/light mode, i18n ID/EN, skor Lighthouse ≥ 90 di semua kategori, gambar dioptimasi (WebP/AVIF, lazy loading), SEO dasar (title, meta description, Open Graph, Twitter Card, sitemap, robots, JSON-LD `SoftwareApplication`), analytics opsional yang ramah privasi dan dimatikan secara default di repo (mis. Plausible/Umami self-hosted), tidak ada rahasia di kode.

**Dokumentasi (`/docs`):** Pengenalan · Quick Start · Instalasi (Docker, tanpa Docker, Raspberry Pi) · Konfigurasi `.env` (tabel semua variabel) · Membuat bot Telegram (langkah demi langkah dengan gambar) · Mengaktifkan SNMP di MikroTik/Cisco/Ubiquiti/Linux (`snmpd`) · Menyiapkan user RouterOS read-only · Discovery & etika scan · Alert & template · Halaman status publik · Backup & restore · Upgrade · Troubleshooting (ICMP di Docker, `NET_RAW`, `network_mode: host` di Linux vs Docker Desktop Windows/Mac) · Referensi API (OpenAPI) · Arsitektur · Panduan kontribusi · (v2) Probe agent · Syslog dan SNMP trap · Backup konfigurasi · IPAM · 2FA/Passkey/SSO · PWA dan Web Push · API plugin dan webhook · Panduan bekerja dengan AI di repo ini (`docs/ai/`).

---
