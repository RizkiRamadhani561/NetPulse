# 12. KUALITAS & TESTING

- **Unit test:** pinger (mock), logika state machine & debounce & flapping, parser/hitung counter SNMP (termasuk wrap), notifier & retry, agregator data, validasi input.
- **Integrasi:** API dengan SQLite in-memory; migrasi naik/turun.
- **E2E (Playwright):** setup wizard → login → tambah perangkat → status muncul → pause → hapus; alur mode demo; tampilan HP.
- **Aksesibilitas:** cek otomatis `axe` pada halaman utama.
- **Performa:** uji beban sederhana (mis. 200 perangkat simulasi) dan catat hasilnya di dokumentasi; Lighthouse ≥ 90 untuk landing page.
- Target coverage backend ≥ 70%. **CI harus gagal** bila lint, type check, test, `pip-audit/npm audit` (tingkat tinggi), atau secret scan gagal.
- Rilis otomatis: tag `vX.Y.Z` → build & push image ke GHCR → buat GitHub Release dengan changelog.
- Protokol lengkap verifikasi, definisi selesai, dan review independen: **Bagian 13**. Semua test jaringan memakai lab (5.29), bukan jaringan nyata.

---
