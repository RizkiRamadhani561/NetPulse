# 15. MEMORI AI (PAHAM, INGAT, DAN KONSISTEN)

## 15.1 Prinsip

AI **tidak otomatis mengingat** antar sesi; konteks hilang saat sesi baru atau ketika percakapan dipadatkan. Karena itu **repositori adalah memorinya**: semua yang penting ditulis ke file, diversikan di Git, dan dibaca ulang di awal sesi. Tiga lapis:

| Lapisan | File | Isi | Sifat |
|---|---|---|---|
| **Aturan tetap** | `AGENTS.md` (+ `CLAUDE.md` yang meng-impor `@AGENTS.md`) | Aturan kerja, perintah, peta dokumen, *boot sequence* | Singkat (< 120–200 baris), dimuat tiap sesi |
| **Keadaan dan sejarah** | `docs/ai/*` | Posisi proyek, keputusan, bug, riset, log sesi, keterlacakan | Hidup, diperbarui tiap tugas |
| **Prosedur** | `.claude/skills/*` (atau setara) | Cara melakukan tugas berulang | Dimuat saat relevan |

Fitur memori otomatis milik tool (bila ada) boleh dipakai sebagai pelengkap, tetapi **`docs/ai/` adalah sumber kebenaran** karena bisa ditinjau, di-diff, dan dibawa antar tool/mesin.

## 15.2 Struktur file

```
AGENTS.md                      # aturan tetap + boot sequence (lihat Lampiran A)
CLAUDE.md                      # berisi "@AGENTS.md" + catatan khusus Claude Code
docs/
  spec/                        # PROMPT.md dipecah per bagian (15.6)
  ai/
    PROJECT_STATE.md           # posisi saat ini: fase, status ID fitur, blokir, langkah berikut
    SESSION_LOG.md             # append-only: ringkasan tiap sesi
    DECISIONS.md               # ADR: keputusan + alternatif + alasan
    ARCHITECTURE.md            # peta modul, alur data, cara menjalankan
    BUGS.md                    # log bug (13.10)
    LEARNINGS.md               # jebakan dan pelajaran ("ICMP di Docker butuh NET_RAW")
    RESEARCH.md                # riset dan sumber (14.3)
    SKILLS_REGISTRY.md         # skill/MCP/plugin pihak ketiga yang dipakai (14.5)
    TRACEABILITY.md            # ID fitur → kode → test → bukti → status
    INTERVIEW_NOTES.md         # keputusan teknis + trade-off + cerita STAR untuk wawancara
    verification/              # laporan verifikasi per fase/rilis (13.3)
    reviews/                   # hasil review independen (13.9)
    archive/                   # entri lama yang dipadatkan
.claude/skills/                # skill proyek (Lampiran E)
.claude/agents/                # subagent: reviewer, ux-auditor, security-auditor (Lampiran F)
```

## 15.3 Protokol sesi

**A. Awal sesi (boot sequence, wajib):**
1. Baca `AGENTS.md` → `docs/ai/PROJECT_STATE.md` → 3 entri terakhir `SESSION_LOG.md` → bug terbuka di `BUGS.md` → `DECISIONS.md` yang relevan.
2. `git status` dan `git log --oneline -15`; bandingkan dengan memori. **Bila berbeda, kode yang benar**; perbaiki memori dan catat.
3. Kirim **Boot Report** (5–8 baris): fase saat ini, yang selesai (ID), yang sedang berjalan, blokir, risiko, rencana sesi ini.
4. Bila rencana mengubah arah, tunggu persetujuanku.

**B. Selama sesi (checkpoint rule):** setelah **setiap sub-tugas selesai** (bukan di akhir saja) perbarui `PROJECT_STATE.md` dan, bila ada keputusan/bug/pelajaran, file terkait. Tujuannya: bila sesi terputus atau konteks dipadatkan, tidak ada yang hilang.

**C. Akhir sesi/tugas:**
1. Tambah entri di `SESSION_LOG.md` (tanggal WIB, tujuan, yang dikerjakan, bukti verifikasi, langkah berikut).
2. Perbarui `TRACEABILITY.md`, `ARCHITECTURE.md` (bila struktur berubah), dan `INTERVIEW_NOTES.md` (bila ada keputusan teknis bernilai cerita).
3. **Commit memori bersama kode** yang bersangkutan (pesan: `docs(ai): ...` atau sertakan di commit fitur).

**D. Teach-back (pemahaman):** di akhir fase, jelaskan ulang kepadaku dengan bahasa sederhana: arsitektur saat ini, alur data satu cek dari awal sampai alert, 3 keputusan terpenting dan alasannya, 3 risiko terbesar. Aku akan mengoreksi bila ada yang keliru; koreksiku dicatat sebagai pelajaran.

## 15.4 Aturan penulisan memori

- **Fakta, bukan opini;** setiap klaim "selesai" menautkan bukti. Hal yang belum pasti ditandai `(belum terverifikasi)`.
- **Tanggal** setiap entri (WIB, format `2026-10-16 01:24`). Jangan menghapus sejarah; tandai yang usang sebagai `SUPERSEDED oleh <ID>`.
- **Ringkas:** `PROJECT_STATE.md` ≤ 150 baris; `AGENTS.md` ≤ 120 baris. Tumpukan detail dipindah ke file lain dan ditautkan.
- **Tanpa rahasia** (Aturan 2): tidak ada token, password, IP internal nyata, atau data pengguna.
- **Satu fakta, satu tempat:** hindari duplikasi antar file; tautkan.
- **ID konsisten:** selalu pakai ID fitur (AUTH-01, dst.), ID keputusan (`ADR-007`), ID bug (`BUG-012`).

## 15.5 Pemeliharaan

- **Audit memori di akhir tiap fase:** cocokkan `PROJECT_STATE`, `TRACEABILITY`, dan `ARCHITECTURE` dengan kode nyata; hapus/arsipkan yang usang; pastikan `AGENTS.md` masih akurat dan singkat.
- **Rotasi:** `SESSION_LOG.md` > 400 baris → pindahkan entri lama ke `archive/` dengan ringkasan satu paragraf per bulan.
- **Bila instruksi yang sering terlewat** (ditemukan dari kesalahan berulang), naikkan menjadi aturan di `AGENTS.md` atau jadikan skill/hook, bukan sekadar catatan.

## 15.6 Memecah spesifikasi (hemat konteks)

`PROMPT.md` panjang. Pada **Fase 0**, pecah menjadi `docs/spec/NN-<slug>.md` (satu file per Bagian, mis. `05-fitur.md`, `06-desain.md`, `13-verifikasi.md`) dan buat `docs/spec/INDEX.md` berisi ringkasan satu baris tiap file. Sesi berikutnya membaca `INDEX.md` lalu **hanya** bagian yang relevan dengan fase/fitur yang dikerjakan. `PROMPT.md` asli tetap disimpan tanpa diubah sebagai referensi; bila spesifikasi berubah, perbarui bagian di `docs/spec/` **dan** catat di `DECISIONS.md`.

---
