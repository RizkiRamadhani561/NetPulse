#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="${1:---quick}"
case "$MODE" in
  --quick) CHECK_MODE="quick" ;;
  --full) CHECK_MODE="full" ;;
  *) echo "Usage: $0 [--quick|--full]" >&2; exit 2 ;;
esac

exec python "$ROOT_DIR/scripts/verify_runner.py" --mode "$CHECK_MODE"
