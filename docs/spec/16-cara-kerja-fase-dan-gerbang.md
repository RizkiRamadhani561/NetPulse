# 16. CARA KERJA, FASE, DAN GERBANG

## 16.1 Langkah awal (sebelum kode)

0. **Boot:** jalankan boot sequence (15.3.A) bila `docs/ai/` sudah ada; bila belum, ini sesi pertama.
1. **Rencana:** tampilkan arsitektur, daftar fase, risiko teknis, hasil riset awal (14.9), dan **pertanyaan klarifikasi**. **Tunggu persetujuanku.**
2. **Kode pertama (Fase 0):** `.gitignore`, `.env.example`, `.pre-commit-config.yaml` (gitleaks), `LICENSE`, `AGENTS.md`/`CLAUDE.md`, `docs/ai/*`, `docs/spec/*`, `scripts/verify.sh`, CI dasar, skill dan subagent proyek, struktur repo, design tokens dan Storybook kosong. Baru kode aplikasi.

## 16.2 Siklus per fitur

1. **Boot/checkpoint:** baca state; pilih satu ID fitur.
2. **Mini-spec:** tulis kriteria penerimaan Given/When/Then di `TRACEABILITY.md`.
3. **Riset** bila ada hal yang belum pasti (Bagian 14) dan catat.
4. **Tes dulu** (merah), lalu **implementasi minimal** (hijau), lalu rapikan.
5. **Verifikasi L0–L4** di lokal; untuk UI jalankan checklist 6.15 dan simpan screenshot desktop + HP.
6. **Review diri:** baca diff sendiri dengan pertanyaan "apa yang bisa rusak?" (13.7).
7. **Review independen** (13.9) untuk fitur besar atau akhir fase.
8. **Perbarui memori** (15.3.C) dan **commit** (Conventional Commits).

Aturan umum: tulis kode bersih (type hint/TypeScript strict, nama deskriptif, fungsi kecil, tanpa duplikasi, komentar hanya untuk hal tak jelas). Jelaskan trade-off (mis. SSE vs WebSocket, SQLite vs PostgreSQL) dengan opsi, rekomendasi, dan alasan singkat. Bila perlu tindakan manual dariku (BotFather, menyalakan SNMP di router), **sebutkan langkahnya jelas**. Untuk UI, ikuti Bagian 6 secara ketat dan pakai identitas visual NetPulse.

## 16.3 Fase, prioritas, dan ID fitur

| Fase | Rilis | Prioritas | Isi | ID fitur |
|---|---|---|---|---|
| **0. Fondasi** | — | P0 | Repo, pengaman rahasia, CI, `verify.sh`, memori AI + spec terpecah, skill dan subagent proyek, lab dasar, design tokens + Storybook, skeleton backend/frontend | **OPS-01**, **LAB-01/03**, UX-04 (dasar) |
| **1. MVP** | — | P0 | Setup wizard, login, CRUD perangkat, ping, state machine, dashboard dasar, daftar dan detail perangkat, SSE, alert Telegram dasar, retensi dasar, skenario lab + test jaringan di lab | AUTH-01–03, DEV-01–03, DEV-05, CHK-01, VIS-01/02/05, ALERT-01/02/04/05/10, SET-01–04, LAB-02/04 |
| **2. Monitoring lanjutan** | — | P1 | Cek TCP/HTTP/DNS/SSL, SNMP, discovery, grup/tag/bulk, parent–child, maintenance, insiden dan flapping, agregasi data | CHK-02–08, SNMP-01–07, DISC-01–07, DEV-04/06/07/08/09, ALERT-03/06–09 |
| **3. Visual & UX** | — | P1 | Topologi, laporan dan SLA, command palette dan shortcut, i18n penuh, tema terang/kontras tinggi, UptimeStrip, aksesibilitas penuh WCAG 2.2, poles desain modern | TOPO-01–07, REP-01–04, UX-01–03, UX-04, VIS-03/04/06 |
| **4. Integrasi & operasional** | — | P1 | MikroTik read-only, mode demo, status page publik, channel tambahan, bot commands, API token, backup/restore, audit log, Prometheus, kesehatan sistem | MT-01–07, DEMO-01–04, STATUS-01–03, ALERT-11–13, AUTH-04–06, SET-05–09, OPS-02–05 |
| **5. Hardening & publikasi** | **v1.0.0** | P1 | Hardening keamanan, uji beban, review independen penuh, landing page, dokumentasi (EN + ID), README dengan GIF, template issue/PR, rilis | (Bagian 7, 10, 12, 13) |
| **6. Remote & observability** | v1.1 | P2 | Multi-site + probe agent, syslog/trap, backup konfigurasi + diff, alat diagnostik | PROBE-01–07, LOG-01–06, CFG-01–06, TOOLS-01–06 |
| **7. Operasi & kecerdasan** | v1.2 | P2 | IPAM + inventaris, dashboard kustom + mode NOC, eskalasi/on-call, analitik lokal | IPAM-01–06, DASH-01–06, ONCALL-01–06, INSIGHT-01–06 |
| **8. Platform** | v1.3 | P2 | 2FA/passkey/SSO, PWA + Web Push, webhook/plugin/CLI, workspace multi-klien, asisten AI opsional, aksi tulis MikroTik (opsional, dimatikan default) | SEC-01–07, PWA-01–04, EXT-01–07, ORG-01–05, AI-01–03, MT-08 |

**Gerbang fase (wajib sebelum lanjut):** Bagian 13.11 "Per fase". Setelah gerbang lulus, kirimkan **laporan fase**: ID selesai beserta status (✅/⚠️/❌/❓), ringkasan bukti, bug diketahui, hasil review independen, hasil teach-back, dan usulan fase berikut. **Tunggu persetujuanku.**

## 16.4 Komunikasi

- Jawab dalam **Bahasa Indonesia**; kode, nama variabel, commit, dan dokumentasi publik dalam **Bahasa Inggris** (kecuali `README.id.md` dan terjemahan i18n).
- Sampaikan masalah atau perubahan arah **segera**, jangan menunggu akhir fase.
- Sarankan pesan commit (Conventional Commits) untuk tiap bagian.
- Jangan memuji berlebihan atau menyetujui semuanya: bila usulanku punya risiko atau lebih buruk dari alternatif, katakan terus terang disertai alasan.

---
