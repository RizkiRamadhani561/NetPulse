# 9. DESAIN API & REAL-TIME

- Prefix `/api/v1`, dokumentasi OpenAPI otomatis di `/docs`, format error konsisten `{ "error": { "code", "message", "details" } }`, pagination berbasis cursor, filter & sort via query param, kode status HTTP yang benar, versi API tercatat.
- Resource minimal: `auth`, `setup`, `users`, `tokens`, `devices`, `groups`, `checks`, `results`, `metrics`, `snmp`, `scan`, `hosts`, `topology`, `incidents`, `alerts`, `rules`, `channels`, `maintenance`, `reports`, `status-page`, `settings`, `backup`, `audit`, `health`, `ready`; **tambahan v2:** `sites`, `probes`, `logs`, `configs`, `tools`, `ipam`, `assets`, `dashboards`, `oncall`, `insights`, `webhooks`, `workspaces`, `push`.
- **Real-time:** endpoint SSE `/api/v1/stream` dengan event bertipe: `device.status`, `check.result`, `incident.opened`, `incident.updated`, `scan.progress`, `scan.host`, `system.notice`. Dukung `Last-Event-ID` untuk lanjut setelah reconnect, heartbeat tiap 15 detik, dan otorisasi per sesi/token.
- Rate limit global yang wajar dan khusus untuk login/endpoint berat.

---
