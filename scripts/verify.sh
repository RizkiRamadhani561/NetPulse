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
  for tool in docker npm; do
    if ! command -v "$tool" >/dev/null 2>&1; then
      echo "❌ Missing required tool for full verification: $tool"
      missing=1
    fi
  done
  if ! python -c "import pytest" >/dev/null 2>&1; then
    echo "❌ Missing Python test dependencies. Install backend dev extras first."
    missing=1
  fi
  if [[ ! -f frontend/package-lock.json ]]; then
    echo "❌ frontend/package-lock.json is missing; generate and review it before full verification."
    missing=1
  fi
  if [[ ! -f backend/uv.lock ]]; then
    echo "❌ backend/uv.lock is missing; generate and review it before full verification."
    missing=1
  fi
  if [[ "$missing" -ne 0 ]]; then
    echo "⚠️ Full verification is blocked; quick structural checks are not a substitute for L0–L5 evidence."
    exit 2
  fi
  docker compose config --quiet
  python -m pytest backend/tests -q
  (cd frontend && npm ci && npm run typecheck && npm run build && npm audit --audit-level=high)
  if command -v gitleaks >/dev/null 2>&1; then
    gitleaks dir --redact .
  else
    echo "❌ Gitleaks CLI is required for full verification." >&2
    exit 2
  fi
fi
