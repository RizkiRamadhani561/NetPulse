# 6. DESAIN TAMPILAN (UI/UX) — FONDASI

Dokumen ini menetapkan baseline desain untuk fondasi Fase 0. Dashboard saat ini adalah shell visual: angka monitoring tetap berupa tanda kosong karena scheduler dan pengumpulan data belum tersedia. Jangan isi nilai uptime/latency palsu agar UI terlihat aktif.

## 6.1 Arah visual

- Produk self-hosted yang tenang dan mudah dibaca oleh admin jaringan, home-lab enthusiast, mahasiswa dan IT support.
- Dashboard gelap sebagai baseline awal, dengan aksen teal untuk tindakan/fokus dan amber untuk status perhatian. Status tidak boleh disampaikan lewat warna saja; gunakan label dan ikon.
- Hierarki informasi mendahulukan kondisi jaringan dan insiden, lalu tren, grup/perangkat, dan tindakan berikutnya.
- Hindari glow berlebihan, kartu dekoratif tanpa fungsi, animasi konstan, teks kecil untuk informasi penting, dan angka yang tidak berasal dari data nyata.

## 6.2 Tata letak dashboard

- Sidebar desktop untuk navigasi utama; topbar untuk workspace, status lingkungan dan pergantian bahasa.
- Konten utama dibatasi lebarnya supaya tidak melebar di monitor besar; kartu metrik memiliki ukuran konsisten.
- Grafik memiliki grid dan empty state yang menjelaskan kenapa belum ada data.
- Bagian setup memberikan langkah berikutnya tanpa membuat kontrol untuk fitur yang belum tersedia terlihat aktif.
- Di layar kecil, navigasi berubah menjadi bar ringkas, kartu metrik dua kolom, lalu panel menumpuk satu kolom. Tidak boleh ada horizontal overflow pada lebar 360–390 px.

## 6.3 Komponen dan status

- Komponen bersama diletakkan di `frontend/src/components/`; katalog Storybook dipakai setelah dependency lockfile tersedia.
- Komponen yang kelak memuat data harus memiliki state loading, empty, normal, error, serta offline/reconnect untuk stream bila relevan.
- Kontrol yang belum tersedia harus jelas disabled dan diberi label planned; jangan memberikan respons sukses palsu.
- Tombol/link harus punya fokus terlihat, nama aksesibel dan target sentuh memadai. Ikon dekoratif disembunyikan dari screen reader.

## 6.4 Bahasa dan gerak

- Bahasa Indonesia dan Inggris tersedia sejak MVP. Seluruh teks UI berasal dari `frontend/src/messages/id.json` dan `en.json`; kedua dictionary wajib memiliki key yang sama.
- Toggle bahasa mempertahankan halaman dan memperbarui atribut `lang` dokumen.
- Hormati `prefers-reduced-motion`. Animasi status harus halus dan tidak menjadi satu-satunya cara menyampaikan perubahan.

## 6.5 Aksesibilitas

Target proyek adalah WCAG 2.2 AA, tetapi shell awal belum mendapat audit browser/axe. Verifikasi ketika tooling tersedia:

- Navigasi keyboard dan urutan fokus konsisten, fokus selalu terlihat.
- Struktur heading, label, landmark dan aria-label sesuai fungsi.
- Kontras teks dan kontrol cukup; status dibedakan oleh label/ikon selain warna.
- Pembesaran 200% dan 400% tidak membuat fungsi inti hilang.
- Ukuran target interaksi memenuhi WCAG 2.2 SC 2.5.8, dan drag-and-drop punya alternatif non-drag/keyboard.
- Empty/error state tidak hanya bergantung pada warna; pesan menjelaskan kondisi dan tindakan yang mungkin.

## 6.6 Checklist review

Untuk setiap perubahan UI, tinjau desktop dan mobile, ID/EN, keyboard-only, fokus, reduced motion, loading/empty/error, konsol browser, overflow, kontras dan makna ikon. Simpan screenshot jika browser tersedia. Jika visual tidak dapat diperiksa secara langsung, catat sebagai belum teruji alih-alih mengklaim telah lolos.

Referensi desain modern dan seluruh acceptance criteria lanjutan tetap perlu dilengkapi saat fase UI terkait dikerjakan. Status fondasi UI saat ini: ⚠️ hanya pemeriksaan statis; browser, Storybook dan audit aksesibilitas belum dijalankan.
