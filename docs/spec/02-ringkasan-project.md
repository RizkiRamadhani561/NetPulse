# 2. RINGKASAN PROJECT

**NetPulse** adalah dashboard monitoring jaringan **self-hosted, open source (MIT), ringan, dan mudah dipasang dengan satu perintah** (`docker compose up`). Fungsinya:

- Memantau uptime, latency, packet loss, dan bandwidth perangkat jaringan.
- Memindai perangkat yang terhubung di jaringan.
- Mengirim alert ke Telegram (dan channel lain) saat ada masalah.
- Menampilkan semuanya di dashboard modern, real-time, responsif, dan enak dilihat.
- Dilengkapi landing page + dokumentasi untuk menarik pengguna dan kontributor.

**Tagline:** *"Feel the pulse of your network."*

**Target pengguna (persona):**
1. **Admin warnet/kantor kecil/sekolah**: punya 1 router MikroTik + beberapa switch/AP, ingin tahu kapan ada yang mati tanpa belajar Zabbix yang rumit.
2. **Home-lab enthusiast**: punya server, NAS, Raspberry Pi, ingin dashboard cantik dan notifikasi ke HP.
3. **Mahasiswa/pemula jaringan**: ingin alat belajar yang bisa dicoba tanpa perangkat sungguhan (mode demo).
4. **Freelancer/IT support**: memantau jaringan beberapa klien dengan grup dan halaman status.

**Tujuan pemilik project (aku):** portfolio untuk melamar kerja di bidang jaringan/IT, sekaligus project open source yang benar-benar berguna. Karena itu kualitas kode, dokumentasi, keamanan, dan tampilan harus setara produk sungguhan.

**Pembeda dari Zabbix/LibreNMS/Uptime Kuma:** lebih ringan dan simpel dari Zabbix/LibreNMS, lebih "network-aware" (SNMP, discovery, topologi, MikroTik) dibanding Uptime Kuma, dan punya mode demo + UI modern berbahasa Indonesia.

**Cakupan v2:** selain monitoring inti, NetPulse berkembang menjadi platform operasi jaringan yang ringan: multi-site/probe, log dan trap, backup konfigurasi, diagnostik, IPAM, dashboard NOC, eskalasi on-call, analitik lokal, keamanan akun lanjutan, PWA, plugin/webhook, dan multi-klien (Bagian 5.17–5.30), dikerjakan bertahap sesuai prioritas di Bagian 16.3.

---
