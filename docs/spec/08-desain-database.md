# 8. DESAIN DATABASE

Rancang skema (boleh ditambah, jelaskan alasannya) dengan migrasi Alembic:

`users`, `sessions`, `api_tokens`, `device_groups`, `devices`, `device_tags`, `checks` (definisi cek), `check_results_raw`, `check_results_1m`, `check_results_1h`, `check_results_1d`, `status_events` (transisi status), `incidents`, `incident_notes`, `snmp_profiles` (terenkripsi), `snmp_interfaces`, `snmp_metrics_raw/1m/1h`, `discovered_hosts`, `host_history`, `topology_nodes`, `topology_links`, `notification_channels` (config terenkripsi), `notification_log`, `alert_rules`, `maintenance_windows`, `status_page_config`, `audit_log`, `settings`; **tambahan v2:** `sites`, `probes`, `probe_tokens`, `log_events`, `config_snapshots`, `ip_subnets`, `ip_allocations`, `vlans`, `assets`, `dashboards`, `dashboard_widgets`, `oncall_schedules`, `escalation_policies`, `runbooks`, `baselines`, `anomalies`, `totp_secrets` (terenkripsi), `webauthn_credentials`, `oidc_identities`, `push_subscriptions`, `webhooks`, `webhook_deliveries`, `workspaces`, `workspace_members`. Tambahkan kolom `site_id` (nullable) dan `workspace_id` (nullable) sejak awal pada tabel yang relevan agar fitur P2 tidak memaksa migrasi besar.

Aturan: index `(device_id, ts)`; kolom waktu disimpan **UTC** dan dikonversi di UI; kredensial dienkripsi (Fernet, kunci dari env `ENCRYPTION_KEY`); soft-delete untuk perangkat agar riwayat laporan tetap utuh; jelaskan strategi retensi dan agregasi (5.14) dan perkiraan ukuran data.

---
