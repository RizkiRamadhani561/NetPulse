# NetPulse — Master Prompt v2

**Full-stack · Fitur lengkap · Desain modern berbasis hukum UI/UX · Terverifikasi (double-check) · Riset internet terkontrol · Memori proyek untuk AI**

## Apa yang baru di v2

| Area | Tambahan |
|---|---|
| **Fitur** | 14 modul baru: multi-site + probe agent, syslog/SNMP trap, backup konfigurasi + diff, alat diagnostik, IPAM + inventaris, dashboard kustom + mode NOC, eskalasi/on-call, analitik lokal (anomali + prediksi kapasitas), keamanan akun (2FA/passkey/SSO), PWA + Web Push, webhook/plugin/CLI, multi-klien (workspace), lab simulator, asisten AI opsional (Bagian 5.17–5.30). |
| **Desain & UX** | Arah desain modern, 20+ hukum UX dipetakan ke fitur, 10 heuristik Nielsen, checklist WCAG 2.2 AA, aturan desain dashboard monitoring, wireframe halaman baru, checklist review UX (Bagian 6.7–6.15). |
| **Verifikasi** | Tangga verifikasi L0–L6, bukti wajib sebelum klaim "selesai", uji adversarial, uji chaos, review independen oleh reviewer ber-konteks-baru, siklus penanganan bug (Bagian 13). |
| **Riset & skills** | AI boleh menjelajah internet dengan aturan keselamatan; prosedur menyeleksi skill/MCP/plugin dari internet; pencegahan paket palsu dan injeksi prompt (Bagian 14). |
| **Memori AI** | `AGENTS.md`/`CLAUDE.md` + folder `docs/ai/` (state, keputusan, bug, riset, log sesi), protokol awal/akhir sesi, "boot report" dan "teach-back" (Bagian 15, Lampiran). |
| **Fase** | 9 fase dengan prioritas P0/P1/P2 dan gerbang verifikasi di tiap fase; v1.0.0 dirilis setelah Fase 5, sisanya pasca-v1 (Bagian 16). |

## Cara memakai file ini

1. Buat repo kosong (`git init`), simpan file ini sebagai `PROMPT.md` di root.
2. Buka AI coding assistant (Claude Code, Cursor, dsb.) di folder itu, lalu kirim:
   *"Baca PROMPT.md sepenuhnya. Kerjakan Bagian 16 langkah 0–1: tampilkan rencana, risiko, dan pertanyaan klarifikasi. Jangan menulis kode sebelum aku setuju."*
3. Kerjakan **satu fase per sesi**. Di akhir fase, minta laporan verifikasi (Bagian 13) dan baru setujui lanjut.
4. Izin tool: pencarian/pembacaan web **diizinkan** (Bagian 14). Menjalankan perintah destruktif, memasang skill/MCP/plugin pihak ketiga, dan push ke remote tetap **minta konfirmasi**.
5. Tanpa akses file (chat biasa): tempel Bagian 1–4 dan 13–16 dulu, lalu bagian fitur/UI **satu fase per satu waktu**.
6. File ini cukup panjang. Pada Fase 0, AI akan memecahnya menjadi `docs/spec/NN-*.md` supaya tiap sesi hanya membaca bagian yang relevan (Bagian 15.6).

## Peta dokumen

| Bagian | Isi |
|---|---|
| 1–4 | Peran, ringkasan, aturan wajib, tech stack |
| 5 | Spesifikasi fitur: 5.1–5.16 inti; 5.17–5.30 lanjutan (v2) |
| 6 | Desain: 6.1–6.6 dasar dan wireframe; 6.7–6.15 desain modern, hukum UX, aksesibilitas |
| 7–12 | Landing page + docs, database, API, keamanan, struktur repo, testing |
| 13 | **Protokol verifikasi dan double-check** |
| 14 | **Riset internet dan skills** |
| 15 | **Memori AI** |
| 16 | Cara kerja, fase, prioritas, gerbang |
| 17 | Konteks tentangku |
| Lampiran A–F | Template: `AGENTS.md`, `PROJECT_STATE.md`, entri log, laporan verifikasi, skill proyek, subagent |

**Catatan realistis:** cakupan ini besar untuk satu orang. Karena itu fitur diberi prioritas: **P0 = MVP**, **P1 = v1.0.0 (portfolio)**, **P2 = pasca-v1** (jadi roadmap, dan calon *good first issue* untuk kontributor). Jangan menunda rilis v1.0.0 demi P2.

---
