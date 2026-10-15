# 5. SPESIFIKASI FITUR — RINGKASAN RUANG LINGKUP

Dokumen ini merangkum modul dan ID fitur untuk membantu perencanaan fase. Ini bukan klaim bahwa fitur-fitur tersebut sudah diimplementasikan. Detail perilaku dan acceptance criteria perlu ditetapkan di `docs/ai/TRACEABILITY.md` sebelum tiap fitur dikerjakan.

## Modul inti (Fase 1–5)

- **AUTH-01–06 — Autentikasi dan setup:** wizard first-run, login dengan rate limit, peran Admin/Operator/Viewer, manajemen sesi, token API sekali tampil dan tersimpan sebagai hash, serta reset akun lewat CLI.
- **DEV-01–09 — Perangkat:** CRUD, validasi host dan duplikasi, uji koneksi, pause/resume, maintenance window, parent-child tanpa siklus, grup/tag, bulk action, CSV, duplikasi perangkat dan promosi hasil discovery.
- **CHK-01–08 — Pengecekan:** ICMP, TCP, HTTP(S), DNS, masa berlaku sertifikat, banyak cek per perangkat, scheduler dengan jitter/batas konkurensi, serta retensi/agregasi hasil.
- **SNMP-01–07 — SNMP:** profil v2c/v3 terenkripsi, metrik interface/counter 32- dan 64-bit, CPU/memori/sensor jika tersedia, pilihan interface, grafik bandwidth, dan deteksi vendor.
- **DISC-01–07 — Discovery:** subnet privat secara default, metode ringan, OUI lokal, deteksi perangkat baru, jadwal/manual progress, promosi hasil ke monitoring dan riwayat host.
- **ALERT-01–13 — Alert dan insiden:** aturan default, debounce/flapping, severity, incident lifecycle, acknowledge, pengingat, quiet hours, suppression parent/maintenance, template pesan, Telegram bot read-only, channel tambahan dan delivery history.
- **VIS-01–06 / TOPO-01–07 / REP-01–04 — Visualisasi:** ringkasan metrik, grafik waktu, heatmap status, SSE, timeline insiden, topologi, laporan uptime/SLA, dan ekspor CSV/JSON/PDF.
- **MT-01–08 — MikroTik:** koneksi RouterOS, info sistem/interface/traffic, Hotspot, DHCP, log dan queue. Integrasi awal harus read-only; aksi tulis opsional dan mati secara default.
- **DEMO-01–04 / STATUS-01–03 / SET-01–09 — Operasional:** data demo yang jelas diberi label, status page yang tidak membocorkan host privat, bahasa/tema/monitoring/notifikasi, retensi, user, backup dan audit log.
- **OPS-01–05 / UX-01–04 — Fondasi:** liveness/readiness, metrik/log terstruktur, graceful shutdown, halaman kesehatan sistem, bahasa Indonesia/Inggris, command palette, shortcut dan WCAG 2.2 AA.

## Fitur lanjutan (v2, pasca-v1 sesuai prioritas)

- **PROBE-01–07:** site dan remote probe dengan koneksi outbound, token, buffer offline, heartbeat dan kuorum.
- **LOG-01–06:** syslog dan SNMP trap, allowlist sumber, parser, live-tail dan alert berbasis log.
- **CFG-01–06:** backup konfigurasi terenkripsi, diff dengan redaksi secret dan pemeriksaan kepatuhan; tanpa restore otomatis.
- **TOOLS-01–06:** diagnostik ping/traceroute/DNS/TCP/HTTP/TLS/Wake-on-LAN/kalkulator subnet dengan validasi target.
- **IPAM-01–06:** subnet/VLAN, alokasi IP, inventaris aset, pengingat garansi, label QR dan CSV aman.
- **DASH-01–06:** dashboard kustom, widget, mode NOC, alternatif keyboard untuk drag, filter tersimpan di URL.
- **ONCALL-01–06 / INSIGHT-01–06:** jadwal eskalasi, runbook, timeline insiden, baseline lokal, anomali yang dijelaskan dan perkiraan kapasitas dengan batas data minimum.
- **SEC-01–07 / PWA-01–04 / EXT-01–07 / ORG-01–05 / AI-01–03:** 2FA/passkey/SSO, PWA/Web Push, webhook/plugin/CLI, workspace multi-klien, dan asisten AI opsional read-only.

Semua cek jaringan dibatasi ke lab/loopback atau target yang memang diizinkan. Perlindungan SSRF, validasi CIDR/URL, batas laju, kontrol akses, pengujian dan bukti verifikasi harus disiapkan sebelum modul jaringan aktif dibuat.
