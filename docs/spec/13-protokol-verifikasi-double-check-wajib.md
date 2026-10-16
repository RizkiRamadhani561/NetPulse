# 13. PROTOKOL VERIFIKASI & DOUBLE-CHECK (WAJIB)

Tujuan: setiap klaim "berhasil" punya **bukti**, dan bug dicari secara **aktif**, bukan ditunggu. Bagian ini berlaku untuk setiap fitur, setiap fase, dan rilis.

## 13.1 Prinsip

1. **Bukti mengalahkan klaim.** "Kodenya terlihat benar" bukan verifikasi. Verifikasi = perintah dijalankan + hasilnya (ringkas) dilampirkan.
2. **Verifikasi di lingkungan bersih**, bukan hanya di mesin dev: clone baru atau container baru, `.env` dari `.env.example`.
3. **Jangan menilai pekerjaan sendiri saja.** Tambahkan lapisan independen (13.9): reviewer ber-konteks-baru yang tidak melihat alasan implementasi.
4. **Bug = tes yang gagal dulu** (red → green → regression), lalu dicatat di `docs/ai/BUGS.md` (13.10).
5. **Jangan melemahkan pengaman** agar hijau (Aturan 8). Test *flaky* diperbaiki akar masalahnya, bukan di-retry untuk menyembunyikan.
6. **Jujur tentang batas.** Yang tidak bisa kamu uji (mis. ICMP tanpa izin, router asli, tampilan visual yang tak bisa kamu lihat) diberi label ❓ disertai langkah uji manual untukku.
7. **Selisih = temuan.** Bila hasil nyata berbeda dari spesifikasi, itu temuan yang dilaporkan, bukan disesuaikan diam-diam.

## 13.2 Tangga verifikasi (L0–L6)

| Level | Cakupan | Contoh perintah / alat | Lulus jika |
|---|---|---|---|
| **L0 Statis** | Format, lint, tipe | `ruff check` · `ruff format --check` · `mypy` · `eslint` · `tsc --noEmit` · `prettier --check` | 0 error, 0 warning baru |
| **L1 Unit** | Logika murni, state machine, parser, enkripsi | `pytest -q --cov` · `vitest run` · `hypothesis` | Semua lulus; coverage backend ≥ 70% (inti ≥ 90%) |
| **L2 Integrasi** | API + DB + migrasi + scheduler (SQLite in-memory dan Postgres di CI) | `pytest -m integration` · `alembic upgrade head` lalu `downgrade base` lalu `upgrade head` | Migrasi naik-turun bersih; kontrak API sesuai OpenAPI |
| **L3 Build & Run** | Image dibangun dan jalan dari nol | `docker compose build` · `up -d --wait` · `scripts/smoke.sh` (13.4) | Health/ready hijau; smoke lulus |
| **L4 E2E & UI** | Alur pengguna nyata di browser | `playwright test` (desktop + HP) · screenshot · regresi visual · konsol bersih (13.5) | Semua alur lulus; 0 error konsol; screenshot tersimpan |
| **L5 Non-fungsional** | A11y, performa, beban, keamanan | `@axe-core/playwright` · `lhci autorun` · `k6`/Locust · `gitleaks` · `pip-audit` · `pnpm audit` · `bandit` · `semgrep` · `trivy` | A11y 0 pelanggaran serious/critical; Lighthouse ≥ 90; beban 200 perangkat stabil; 0 secret; 0 CVE high/critical tak teratasi |
| **L6 Independen** | Review ber-konteks-baru + uji adversarial (13.7–13.9) | Subagent/sesi reviewer; bug bash | Semua temuan severity tinggi ditutup atau dijelaskan |

Aturan pemakaian: tiap commit kode → minimal **L0–L2**. Tiap fitur selesai → **L0–L4** + checklist UX 6.15 untuk bagian UI. Tiap akhir fase dan rilis → **L0–L6**.

## 13.3 `scripts/verify.sh` (satu pintu)

Buat di **Fase 0** dan pakai persis sama di lokal dan CI:
- `--quick` memvalidasi struktur dan kontrak keamanan dasar; `--full` menjalankan verifikasi non-container (dependency locks, lint/format, mypy, unit tests + coverage ≥ 70%, pip-audit, TypeScript, Next.js/Storybook builds, npm audit, Gitleaks). Non-zero exit code berarti minimal satu pemeriksaan gagal.
- Menulis laporan Markdown dan log per langkah ke `docs/ai/verification/local-<timestamp>/`.
- Idempoten dan aman dijalankan berulang; tidak menyentuh jaringan nyata.
- Mencetak ringkasan akhir berformat tabel: langkah · status · durasi · lokasi bukti.

### NetPulse workflow override — Docker final-integration gate (ADR-006)

Atas keputusan pengguna pada 2026-10-16, pemeriksaan runtime Docker Compose ditunda hingga fitur sistem selesai. Karena itu, `--full` tidak menjalankan atau memerlukan Docker; ini bukan penghapusan gerbang L3. Workflow GitHub Actions `Docker Compose smoke test` hanya berjalan saat `workflow_dispatch`, setelah `foundation`, `frontend`, dan `secrets` berhasil. Gerbang fase tetap terbuka sampai job manual tersebut lulus.

## 13.4 Smoke test "dari nol" (`scripts/smoke.sh`)

1. Clone bersih ke direktori sementara → salin `.env.example` → generate rahasia acak (skrip `gen-secrets`).
2. `docker compose --profile lab up -d --wait`; cek `/api/v1/health` dan `/api/v1/ready`.
3. Setup admin via API; login; tambah perangkat lab.
4. Pastikan status `UP`; matikan perangkat lab → status menjadi `DOWN` setelah *retries* → **tepat satu** notifikasi terkirim ke *mock* Telegram (bukan Telegram asli) → insiden terbuka.
5. Hidupkan lagi → `UP`, notifikasi pulih terkirim **tepat satu**, insiden tertutup.
6. Restart backend di tengah siklus → **tidak ada** alert palsu (masa tenggang OPS-04).
7. `docker compose down -v`; pastikan tidak ada rahasia di log (`grep` pola token) dan tidak ada proses yatim.

## 13.5 Verifikasi UI (visual dan UX)

- **Matriks screenshot Playwright:** setiap halaman × lebar {1440, 1024, 768, 390, 360} × tema {gelap, terang, kontras tinggi} × state {loading, kosong, normal, error}. Simpan di artefak; baseline visual disetujui manusia.
- **Konsol dan jaringan:** `console.error`, `pageerror`, dan request gagal **menggagalkan test**.
- **Aksesibilitas:** axe pada tiap halaman dan state utama; skrip navigasi **keyboard-only** untuk 5 alur inti; uji zoom 200% dan 400%; `prefers-reduced-motion`.
- **Buta warna:** emulasi defisiensi penglihatan (protanopia, deuteranopia, tritanopia, achromatopsia) via CDP `Emulation.setEmulatedVisionDeficiency`; status harus tetap terbedakan.
- **Kondisi buruk:** throttle jaringan (3G) dan CPU (4×), mode offline, SSE diputus lalu tersambung ulang.
- **Ukuran target:** skrip mengukur bounding box tombol/link ≥ 24 px (≥ 44 px di viewport HP).
- **Checklist 6.15** untuk setiap halaman baru atau berubah; hasilnya dicantumkan di laporan.
- **Kejujuran visual:** bila tool-mu dapat membuka gambar, **lihat sendiri** screenshot dan tulis temuan konkret (selisih jarak, teks terpotong, kontras buruk). Bila tidak bisa, tandai ❓ "visual belum ditinjau" dan minta aku meninjau folder screenshot yang kamu sebutkan.

## 13.6 Verifikasi fungsional khusus domain

- **State machine:** *stateful property test* (hypothesis): urutan acak hasil cek tidak pernah menghasilkan transisi ilegal; `retries` dan debounce benar; flapping terdeteksi tepat pada ambangnya; parent-child tidak pernah melingkar.
- **Waktu:** semua logika waktu memakai **jam yang dapat disuntik** (fake clock): uji lompatan jam, zona waktu lain, pergantian hari/DST pada agregasi.
- **SNMP:** perhitungan bps dengan **counter wrap** 32/64-bit dan reset; interface naik-turun; nilai negatif/NaN ditolak.
- **Agregasi dan retensi:** hasil agregat = hasil hitung ulang dari data mentah (uji kesetaraan); job retensi tidak menghapus data yang belum diagregasi.
- **Scheduler:** tidak *double-run*, tidak *drift*, menghormati batas konkurensi; tetap berjalan bila satu cek *hang* (timeout keras).
- **SSE:** `Last-Event-ID` melanjutkan tanpa kehilangan/duplikasi; heartbeat; klien lambat tidak memblokir server.
- **Kriptografi:** *round-trip* enkripsi, rotasi kunci, data lama tetap terbaca; kunci salah → error jelas, bukan crash.
- **Probe (bila ada):** idempotensi pengiriman ulang; urutan terbalik; kuorum.
- **Multi-tenant (bila ada):** *tenant leakage test* otomatis di **setiap** endpoint.

## 13.7 Daftar uji adversarial (bug bash, minimal ini)

1. Host berisi metakarakter shell (`1.1.1.1; rm -rf /`, `$(id)`, `` `id` ``) → ditolak, tidak pernah mencapai shell.
2. CIDR tidak valid, terlalu besar (`10.0.0.0/8` untuk scan), IPv6 dengan *scope id*, hostname Unicode/IDN, panjang berlebih.
3. **XSS:** nama perangkat/grup/catatan berisi `<script>`, `"><img onerror=...>` → ter-escape di dashboard, PDF, CSV, dan pesan Telegram (escape HTML/MarkdownV2 yang benar).
4. **CSV injection** pada ekspor (`=cmd|...`, `+`, `-`, `@`).
5. **SSRF** pada HTTP check: `http://169.254.169.254`, `localhost`, redirect ke alamat internal, DNS rebinding sederhana.
6. Respons HTTP check sangat besar atau lambat → dibatasi ukuran dan waktu.
7. 10.000 perangkat / 1 juta baris hasil → halaman tetap responsif (pagination, virtualisasi).
8. Counter SNMP wrap, nilai mundur, OID tidak ada, SNMP timeout, community salah.
9. Dua pengguna mengedit perangkat yang sama (konflik); klik ganda "Simpan"; kirim ulang form.
10. Jam sistem melompat maju/mundur; zona waktu ≠ Asia/Jakarta; pergantian bulan/tahun.
11. SSE putus dan tersambung ulang berulang; tab di latar belakang lama.
12. Telegram membalas 429 (`retry_after`), 400 (chat tidak valid), timeout → retry dengan backoff, tidak spam, tidak hilang diam-diam.
13. Database terkunci/penuh; disk penuh; migrasi gagal di tengah.
14. Restart saat insiden terbuka → insiden tidak ganda; status pulih benar.
15. Parent-child melingkar; menghapus parent; menghapus perangkat yang punya insiden terbuka.
16. Upload CSV impor berisi baris rusak, encoding aneh, 50 MB → pratinjau + error per baris, tanpa crash.
17. Login: *brute force*, enumerasi username (pesan sama untuk salah user/password), sesi kedaluwarsa, CSRF.
18. Token API: dipakai setelah dicabut, scope tidak cukup, token di log (tidak boleh).
19. Respons dengan data sensitif (hash password, kunci enkripsi, community) **tidak pernah** muncul di API, log, atau UI.
20. Fitur mati (`DEMO_MODE`, AI, aksi tulis MikroTik) benar-benar tidak dapat diakses lewat API langsung.
21. Locale ID/EN: string panjang, pluralisasi, format tanggal/angka.
22. ICMP tidak diizinkan di kontainer → fallback TCP ping dengan pesan yang jelas.

## 13.8 Uji ketahanan (chaos ringan, dengan lab)

Matikan backend di tengah polling · matikan DB · blokir DNS · putuskan jaringan kontainer · Telegram *mock* mengembalikan error · kirim 1.000 event serentak · mulai ulang 5× berturut-turut. Hasil yang diharapkan: **tidak ada alert palsu massal, tidak ada kehilangan data yang sudah dikonfirmasi, pemulihan otomatis**, dan log menjelaskan apa yang terjadi.

## 13.9 Review independen (double-check oleh pihak lain)

- **Kapan:** akhir fitur besar, akhir setiap fase, dan sebelum rilis.
- **Siapa:** subagent *reviewer* atau sesi baru dengan konteks bersih (prompt di Lampiran F). Reviewer menerima **ID fitur, spesifikasi, diff, dan laporan verifikasi**; **tidak** menerima alasan/penjelasan implementasi.
- **Dua lintasan:** (a) kebenaran dan kesesuaian spesifikasi, (b) adversarial: keamanan, UX, ketahanan.
- **Keluaran:** daftar temuan (severity, lokasi, bukti, saran) di `docs/ai/reviews/<tanggal>-<label>.md`.
- **Tanggapan wajib:** builder menutup tiap temuan (perbaikan + test) atau membantah dengan alasan tertulis. Temuan *critical/high* menahan gerbang fase.
- Bila tool tidak punya subagent: buka sesi baru, tempel prompt reviewer, dan berikan hanya diff + spesifikasi.

## 13.10 Penanganan bug

1. **Reproduksi** dan tulis langkahnya. 2. **Tulis test yang gagal.** 3. Cari **akar masalah** (bukan gejala). 4. Perbaiki seminimal mungkin. 5. Test lulus + jalankan L0–L2. 6. Cari **bug serupa** di tempat lain (grep pola yang sama). 7. Catat di `docs/ai/BUGS.md` (gejala, akar, perbaikan, test regresi, commit). 8. Bila bug menunjukkan celah proses, tambahkan ke `LEARNINGS.md` dan, bila berulang, ke checklist/skill.

## 13.11 Definition of Done

**Per fitur** (semua harus benar, dengan bukti):
- [ ] Kriteria penerimaan (Given/When/Then) tertulis di `TRACEABILITY.md` dan **semuanya** lulus.
- [ ] Test ditulis (unit + integrasi; E2E untuk alur pengguna) dan lulus di lingkungan bersih.
- [ ] State loading/kosong/error ada; UI lulus checklist 6.15; screenshot desktop + HP tersimpan.
- [ ] A11y: axe bersih; keyboard-only bisa; target dan kontras memenuhi 6.10.
- [ ] Tidak ada rahasia di kode/log/memori; input divalidasi; keluaran di-encode.
- [ ] i18n ID + EN lengkap; dokumentasi/README diperbarui; `.env.example` diperbarui bila perlu.
- [ ] Memori diperbarui (`PROJECT_STATE`, `SESSION_LOG`, `DECISIONS`, `TRACEABILITY`).
- [ ] Commit mengikuti Conventional Commits.

**Per fase (gerbang):** `scripts/verify.sh --full` hijau · laporan verifikasi tersimpan · reviewer independen selesai dan temuan tinggi tertutup · bug terbuka dengan severity tinggi = 0 · matriks keterlacakan untuk semua ID fase berstatus ✅ (atau ⚠️/❓ yang dijelaskan dan kusetujui) · audit memori (15.5) selesai · **aku menyetujui** sebelum fase berikut.

**v1.0.0:** semua gerbang Fase 0–5 lulus; orang yang belum pernah melihat proyek ini bisa memasang dan menjalankannya dari README dalam ≤ 10 menit (uji nyata, dicatat); demo meyakinkan; landing page live; `SECURITY.md` dan pemindaian rahasia pada seluruh riwayat Git bersih.

## 13.12 Matriks keterlacakan

`docs/ai/TRACEABILITY.md` memetakan **ID fitur → file kode → test → bukti → status** (✅/⚠️/❌/❓). Ini sumber kebenaran untuk "apa yang sudah jadi dan terbukti". Tidak ada ID yang boleh berstatus ✅ tanpa tautan ke bukti.

---
