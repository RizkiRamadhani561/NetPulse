param(
  [ValidateSet("quick", "full")]
  [string]$Mode = "quick"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
  python scripts/verify_project.py --mode $Mode
  if ($LASTEXITCODE -ne 0) { throw "Structural verification failed." }

  if ($Mode -eq "full") {
    if (-not (Test-Path "backend/uv.lock") -or -not (Test-Path "frontend/package-lock.json")) {
      throw "Full verification is blocked until backend/uv.lock and frontend/package-lock.json have been generated and reviewed."
    }

    docker compose config --quiet
    if ($LASTEXITCODE -ne 0) { throw "Docker Compose configuration validation failed." }

    Push-Location "backend"
    try {
      python -m pytest tests -q
      if ($LASTEXITCODE -ne 0) { throw "Backend tests failed." }
    } finally { Pop-Location }

    Push-Location "frontend"
    try {
      npm ci
      if ($LASTEXITCODE -ne 0) { throw "npm ci failed." }
      npm run typecheck
      if ($LASTEXITCODE -ne 0) { throw "Frontend typecheck failed." }
      npm run build
      if ($LASTEXITCODE -ne 0) { throw "Frontend production build failed." }
      npm audit --audit-level=high
      if ($LASTEXITCODE -ne 0) { throw "npm audit reported a high-severity issue." }
    } finally { Pop-Location }
  }
} finally { Pop-Location }
