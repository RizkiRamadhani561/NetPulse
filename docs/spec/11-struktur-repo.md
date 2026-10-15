# 11. STRUKTUR REPO

```
netpulse/
  backend/
    app/
      api/ (router per resource)
      core/ (config, security, logging, crypto)
      db/ (models, session, migrations)
      services/ (pinger, service_checker, snmp_poller, scanner, notifier, scheduler, aggregator, demo_generator, mikrotik; v2: log_receiver, config_backup, diagnostics, ipam, insights, probe_gateway) + worker.py (entrypoint proses worker)
      schemas/
      cli.py
    tests/
    Dockerfile
    pyproject.toml
  frontend/
    src/ (app, components, features, lib, hooks, messages/{id,en}.json)
    tests/
    Dockerfile
    package.json
  docs/
    site/ (dokumentasi publik + landing page)
    spec/ (PROMPT.md dipecah per bagian, Bagian 15.6)
    ai/ (memori AI: PROJECT_STATE, SESSION_LOG, DECISIONS, BUGS, ... Bagian 15)
  agent/ (probe agent, Fase 6)
  lab/ (profil compose lab: simulator, scenarios/, fixtures/)
  scripts/ (update-oui, gen-secrets, seed-demo, verify.sh, smoke.sh)
  .claude/ (skills/, agents/)
  AGENTS.md  CLAUDE.md
  .github/
    workflows/ (ci.yml, release.yml, codeql.yml)
    ISSUE_TEMPLATE/ (bug_report.yml, feature_request.yml)
    PULL_REQUEST_TEMPLATE.md
    dependabot.yml
  docker-compose.yml
  docker-compose.dev.yml
  .env.example
  .gitignore
  .pre-commit-config.yaml   (ruff, mypy, prettier, gitleaks)
  LICENSE                   (MIT)
  README.md  README.id.md
  CONTRIBUTING.md  CODE_OF_CONDUCT.md  SECURITY.md  CHANGELOG.md
```

Isi `.env.example` minimal (nama saja, tanpa nilai asli): `APP_ENV`, `SECRET_KEY`, `ENCRYPTION_KEY`, `DATABASE_URL`, `ALLOWED_ORIGINS`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `DEMO_MODE`, `ALLOW_PUBLIC_SCAN`, `DEFAULT_TIMEZONE`, `LOG_LEVEL`, `RETENTION_RAW_DAYS`, `CHECK_CONCURRENCY`, `ENABLE_UPDATE_CHECK`, `ENABLE_MIKROTIK_WRITE`. **Tambahan v2 (hanya nama):** `TRUSTED_PROXIES`, `SYSLOG_PORT`, `TRAP_PORT`, `VAPID_PUBLIC_KEY`, `VAPID_PRIVATE_KEY`, `OIDC_ISSUER`, `OIDC_CLIENT_ID`, `OIDC_CLIENT_SECRET`, `SMTP_HOST`, `SMTP_USER`, `SMTP_PASSWORD`, `ENABLE_AI`, `AI_PROVIDER`, `AI_API_KEY`. Semua yang bersifat rahasia dibaca hanya di backend.

---
