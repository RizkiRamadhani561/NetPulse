param(
  [ValidateSet("quick", "full")]
  [string]$Mode = "quick"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
  python scripts/verify_project.py --mode $Mode
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  if ($Mode -eq "full") {
    docker compose config --quiet
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -m pytest backend/tests -q
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    if (-not (Test-Path "backend/uv.lock") -or -not (Test-Path "frontend/package-lock.json")) {
      throw "Full verification is blocked until backend/uv.lock and frontend/package-lock.json have been generated and reviewed."
    }
    Push-Location "frontend"
    try {
      npm ci
      if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
      npm run typecheck
      if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
      npm run build
      if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
      npm audit --audit-level=high
      if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    } finally { Pop-Location }
  }
} finally { Pop-Location }
