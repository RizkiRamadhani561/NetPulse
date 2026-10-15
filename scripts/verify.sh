#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="${1:---quick}"
case "$MODE" in
  --quick) CHECK_MODE="quick" ;;
  --full) CHECK_MODE="full" ;;
  *) echo "Usage: $0 [--quick|--full]" >&2; exit 2 ;;
esac

cd "$ROOT_DIR"
python scripts/verify_project.py --mode "$CHECK_MODE"

if [[ "$CHECK_MODE" == "full" ]]; then
  missing=0
  for tool in docker npm uv gitleaks curl; do
    if ! command -v "$tool" >/dev/null 2>&1; then
      echo "❌ Missing required tool for full verification: $tool"
      missing=1
    fi
  done
  for lockfile in backend/uv.lock frontend/package-lock.json; do
    if [[ ! -f "$lockfile" ]]; then
      echo "❌ Required lockfile is missing: $lockfile"
      missing=1
    fi
  done
  if [[ "$missing" -ne 0 ]]; then
    echo "⚠️ Full verification cannot proceed until the missing tools/files are available."
    exit 2
  fi

  (
    cd backend
    uv sync --locked --extra dev
    uv run --locked --extra dev ruff check app tests ../scripts
    uv run --locked --extra dev ruff format --check app tests ../scripts
    uv run --locked --extra dev pytest tests -q
  )

  (
    cd frontend
    npm ci --no-audit --no-fund
    npm run typecheck
    npm run build
    npm audit --audit-level=high
  )

  docker compose config --quiet
  readiness_file="$(mktemp)"
  cleanup() {
    local status=$?
    if [[ "$status" -ne 0 ]]; then
      docker compose ps || true
      docker compose logs --no-color --tail 150 || true
    fi
    docker compose down --remove-orphans
    rm -f "$readiness_file"
    return "$status"
  }
  trap cleanup EXIT
  docker compose up -d --build --wait

  curl --fail --silent --show-error --retry 30 --retry-connrefused --retry-all-errors --retry-delay 2 --max-time 5 \
    http://127.0.0.1:8000/api/v1/health >/dev/null
  curl --fail --silent --show-error --retry 30 --retry-connrefused --retry-all-errors --retry-delay 2 --max-time 5 \
    http://127.0.0.1:3000/api/health >/dev/null
  curl --fail --silent --show-error --retry 30 --retry-connrefused --retry-all-errors --retry-delay 2 --max-time 5 \
    http://127.0.0.1:3000/ >/dev/null

  ready_code="$(curl --silent --show-error --output "$readiness_file" --write-out '%{http_code}' --max-time 5 \
    http://127.0.0.1:8000/api/v1/ready)"
  test "$ready_code" = "503"
  python -c 'import json,sys; assert json.load(open(sys.argv[1], encoding="utf-8"))["status"] == "not_ready"' "$readiness_file"

  gitleaks dir --redact .
  echo "✅ Full local verification passed, including the Docker Compose smoke test."
fi
