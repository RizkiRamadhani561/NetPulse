(() => {
  const root = document.documentElement;
  const languageButton = document.getElementById("language-toggle");
  const themeButton = document.getElementById("theme-toggle");
  const translations = {
    en: {
      skip:"Skip to content",navProject:"Project",navRoadmap:"Roadmap",navDocs:"Documentation",getStarted:"Read the docs",eyebrow:"OPEN SOURCE · EARLY PREVIEW",heroTitle:"A clearer view of your network.",heroLede:"NetPulse is being built as a lightweight, self-hosted monitoring workspace for home labs, small offices, schools, and hands-on IT teams.",heroPrimary:"Explore the project",heroSecondary:"View source",heroFootnote:"The project is not production-ready. Device monitoring, authentication, persistent storage, and alerts are still in development.",statusLabel:"CURRENT PROJECT STATUS",statusTitle:"Foundation preview · Phase 0",statusLink:"Read the project state",
      projectLabel:"01 / PROJECT",projectTitle:"Built to stay understandable.",projectIntro:"The aim is not to recreate a heavyweight NOC on day one. NetPulse starts with clear defaults, local control, and an interface that helps operators understand what the system knows — and what it does not.",feature1Title:"A focused workspace",feature1Body:"A quiet interface for network health, device status, and events. The current dashboard is a UI foundation, not a live monitoring service.",statusFoundation:"Foundation in place",feature2Title:"Self-hosted by design",feature2Body:"The intended architecture keeps monitoring data on infrastructure you control and avoids telemetry by default.",statusDesign:"Design goal",feature3Title:"A safe learning path",feature3Body:"Future checks and labs are intended for loopback, isolated containers, and networks you own or have explicit permission to test.",statusPlanned:"Planned",
      designLabel:"02 / DESIGN SYSTEM",designTitle:"Useful detail, not visual noise.",designBody:"The identity uses ink navy, restrained teal, a few network routes, and a steady grid. Vector artwork stays crisp across the app sidebar, repository, and browser tab.",brandGuide:"Open brand guidelines",authAsset:"Login background artwork",authAssetNote:"Prepared for the future authentication screen",plannedAuth:"Phase 1",
      roadmapLabel:"03 / ROADMAP",roadmapTitle:"Build in stages. Verify each one.",roadmapIntro:"The status below follows the source README and project state. Planned work is not represented as shipped capability.",roadmapCurrent:"CURRENT · FOUNDATION",roadmapNext:"NEXT · PLANNED",roadmapLater:"LATER · PLANNED",roadmap0Title:"Project foundation",roadmap0Body:"API and web shells, CI, safety defaults, isolated lab contracts, and verification scripts. Final runtime integration and visual review are still open.",roadmap1Title:"Monitoring MVP",roadmap1Body:"Authentication, setup, device management, checks, monitoring state, and alerts — subject to implementation and verification.",roadmap2Title:"More network context",roadmap2Body:"SNMP metrics, discovery, topology, reports, status pages, integrations, and broader operational tooling.",closingLabel:"MAKE IT BETTER, ONE VERIFIED STEP AT A TIME",closingTitle:"Follow the work, not the hype.",closingBody:"Read the source, check the current scope, and contribute with the project’s safety and verification rules in mind.",closingGitHub:"Open repository",closingDocs:"Project documentation",footerStatus:"Early preview · not for production monitoring"
    },
    id: {
      skip:"Loncat ke konten",navProject:"Proyek",navRoadmap:"Peta jalan",navDocs:"Dokumentasi",getStarted:"Baca dokumentasi",eyebrow:"OPEN SOURCE · PRATINJAU AWAL",heroTitle:"Memahami jaringan dengan lebih jelas.",heroLede:"NetPulse sedang dibangun sebagai ruang monitoring mandiri yang ringan untuk home lab, kantor kecil, sekolah, dan tim IT support.",heroPrimary:"Jelajahi proyek",heroSecondary:"Lihat source code",heroFootnote:"Proyek ini belum siap untuk produksi. Monitoring perangkat, autentikasi, penyimpanan persisten, dan alert masih dalam pengembangan.",statusLabel:"STATUS PROYEK SAAT INI",statusTitle:"Pratinjau fondasi · Fase 0",statusLink:"Baca status proyek",
      projectLabel:"01 / PROYEK",projectTitle:"Dibuat agar mudah dipahami.",projectIntro:"Tujuannya bukan meniru NOC besar dalam satu hari. NetPulse dimulai dengan konfigurasi jelas, kontrol lokal, dan antarmuka yang membantu operator memahami apa yang diketahui sistem — dan apa yang belum.",feature1Title:"Ruang kerja terarah",feature1Body:"Antarmuka sederhana untuk kesehatan jaringan, status perangkat, dan kejadian. Dashboard saat ini masih fondasi UI, belum menjadi layanan monitoring aktif.",statusFoundation:"Fondasi tersedia",feature2Title:"Dirancang self-hosted",feature2Body:"Arsitektur yang dituju menyimpan data monitoring di infrastruktur yang kamu kendalikan dan tidak mengaktifkan telemetry secara default.",statusDesign:"Tujuan desain",feature3Title:"Jalur belajar yang aman",feature3Body:"Pengecekan dan lab mendatang ditujukan untuk loopback, container terisolasi, serta jaringan milik sendiri atau yang secara eksplisit diizinkan.",statusPlanned:"Direncanakan",
      designLabel:"02 / SISTEM DESAIN",designTitle:"Detail berguna, tanpa gangguan visual.",designBody:"Identitas menggunakan navy gelap, teal secukupnya, jalur jaringan sederhana, dan grid konsisten. Ilustrasi vektor tetap tajam di sidebar aplikasi, repositori, serta tab browser.",brandGuide:"Buka panduan brand",authAsset:"Ilustrasi background login",authAssetNote:"Disiapkan untuk layar autentikasi pada fase mendatang",plannedAuth:"Fase 1",
      roadmapLabel:"03 / PETA JALAN",roadmapTitle:"Bangun bertahap. Verifikasi setiap tahap.",roadmapIntro:"Status di bawah mengikuti README dan state proyek. Fitur yang direncanakan tidak ditampilkan sebagai fitur yang sudah rilis.",roadmapCurrent:"SAAT INI · FONDASI",roadmapNext:"BERIKUTNYA · RENCANA",roadmapLater:"NANTI · RENCANA",roadmap0Title:"Fondasi proyek",roadmap0Body:"Kerangka API dan web, CI, default keamanan, kontrak lab terisolasi, serta skrip verifikasi. Integrasi runtime final dan review visual masih terbuka.",roadmap1Title:"MVP monitoring",roadmap1Body:"Autentikasi, setup, manajemen perangkat, pengecekan, status monitoring, dan alert — menunggu implementasi dan verifikasi.",roadmap2Title:"Konteks jaringan lebih luas",roadmap2Body:"Metrik SNMP, discovery, topologi, laporan, halaman status, integrasi, dan perangkat operasional lainnya.",closingLabel:"TINGKATKAN DENGAN SATU LANGKAH TERVERIFIKASI",closingTitle:"Ikuti progres, bukan sekadar klaim.",closingBody:"Baca source code, cek cakupan yang sedang berjalan, dan berkontribusi dengan mengikuti aturan keamanan serta verifikasi proyek.",closingGitHub:"Buka repositori",closingDocs:"Dokumentasi proyek",footerStatus:"Pratinjau awal · belum untuk monitoring produksi"
    }
  };
  function setLanguage(lang) {
    root.lang = lang;
    document.querySelectorAll("[data-i18n]").forEach((node) => {
      const key = node.getAttribute("data-i18n");
      const value = translations[lang][key];
      if (!value) return;
      const icon = node.querySelector("span[aria-hidden='true']");
      node.textContent = value;
      if (icon) node.appendChild(icon);
    });
    languageButton.textContent = lang === "en" ? "ID" : "EN";
    languageButton.setAttribute("aria-label", lang === "en" ? "Ganti bahasa ke Indonesia" : "Switch language to English");
    try { localStorage.setItem("netpulse-site-language", lang); } catch {}
  }
  languageButton.addEventListener("click", () => setLanguage(root.lang === "en" ? "id" : "en"));
  themeButton.addEventListener("click", () => {
    const next = root.dataset.theme === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    themeButton.setAttribute("aria-label", next === "dark" ? "Switch theme to light" : "Switch theme to dark");
    try { localStorage.setItem("netpulse-site-theme", next); } catch {}
  });
  try {
    const savedLanguage = localStorage.getItem("netpulse-site-language");
    const savedTheme = localStorage.getItem("netpulse-site-theme");
    if (savedLanguage === "id" || savedLanguage === "en") setLanguage(savedLanguage);
    if (savedTheme === "dark" || savedTheme === "light") root.dataset.theme = savedTheme;
  } catch {}
})();