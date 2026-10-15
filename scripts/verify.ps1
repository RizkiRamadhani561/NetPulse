param(
  [ValidateSet("quick", "full")]
  [string]$Mode = "quick"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$StackStarted = $false
$ReadinessFile = Join-Path $env:TEMP ("netpulse-readiness-" + [guid]::NewGuid().ToString("N") + ".json")

function Wait-NetPulseHttp([string]$Url) {
  for ($attempt = 1; $attempt -le 30; $attempt++) {
    & curl.exe --fail --silent --show-error --max-time 5 $Url --output NUL 2>$null
    if ($LASTEXITCODE -eq 0) { return }
    Start-Sleep -Seconds 2
  }
  throw "HTTP smoke test did not succeed after 30 attempts: $Url"
}
Push-Location $Root
try {
  python scripts/verify_project.py --mode $Mode
  if ($LASTEXITCODE -ne 0) { throw "Structural verification failed." }

  if ($Mode -eq "full") {
    foreach ($tool in @("docker", "npm", "uv", "gitleaks", "curl.exe")) {
      if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) {
        throw "Required tool '$tool' is missing. Install it before running full verification."
      }
    }
    foreach ($lockfile in @("backend/uv.lock", "frontend/package-lock.json")) {
      if (-not (Test-Path $lockfile)) { throw "Required lockfile is missing: $lockfile" }
    }

    Push-Location "backend"
    try {
      & uv sync --locked --extra dev
      if ($LASTEXITCODE -ne 0) { throw "Locked backend dependency sync failed." }
      & uv run --locked --extra dev ruff check app tests ../scripts
      if ($LASTEXITCODE -ne 0) { throw "Ruff lint failed." }
      & uv run --locked --extra dev ruff format --check app tests ../scripts
      if ($LASTEXITCODE -ne 0) { throw "Ruff format check failed." }
      & uv run --locked --extra dev pytest tests -q
      if ($LASTEXITCODE -ne 0) { throw "Backend tests failed." }
    } finally { Pop-Location }

    Push-Location "frontend"
    try {
      npm ci --no-audit --no-fund
      if ($LASTEXITCODE -ne 0) { throw "npm ci failed." }
      npm run typecheck
      if ($LASTEXITCODE -ne 0) { throw "Frontend typecheck failed." }
      npm run build
      if ($LASTEXITCODE -ne 0) { throw "Frontend production build failed." }
      npm audit --audit-level=high
      if ($LASTEXITCODE -ne 0) { throw "npm audit reported a high-severity issue." }
    } finally { Pop-Location }

    docker compose config --quiet
    if ($LASTEXITCODE -ne 0) { throw "Docker Compose configuration validation failed." }

    try {
      $StackStarted = $true
      docker compose up -d --build --wait --wait-timeout 180
      if ($LASTEXITCODE -ne 0) {
        docker compose ps
        docker compose logs --no-color --tail 150
        throw "Docker Compose build/start/healthcheck failed; see container logs above."
      }

      Wait-NetPulseHttp "http://127.0.0.1:8000/api/v1/health"
      Wait-NetPulseHttp "http://127.0.0.1:3000/api/health"
      Wait-NetPulseHttp "http://127.0.0.1:3000/"

      $ReadyCode = $null
      for ($attempt = 1; $attempt -le 30; $attempt++) {
        $ReadyCode = & curl.exe --silent --show-error --output $ReadinessFile --write-out "%{http_code}" --max-time 5 "http://127.0.0.1:8000/api/v1/ready" 2>$null
        if ($LASTEXITCODE -eq 0 -and $ReadyCode -eq "503") { break }
        Start-Sleep -Seconds 2
      }
      if ($LASTEXITCODE -ne 0 -or $ReadyCode -ne "503") { throw "Readiness endpoint must return the documented 503 until DB/scheduler checks exist." }
      python -c "import json; assert json.load(open(r'$ReadinessFile', encoding='utf-8'))['status'] == 'not_ready'"
      if ($LASTEXITCODE -ne 0) { throw "Readiness response body did not match the expected not_ready status." }
    } finally {
      if ($StackStarted) {
        docker compose down --remove-orphans
        if ($LASTEXITCODE -ne 0) { Write-Warning "Docker Compose cleanup returned a non-zero exit code." }
      }
      Remove-Item $ReadinessFile -ErrorAction SilentlyContinue
    }

    Push-Location "backend"
    try {
      & gitleaks dir --redact ..
      if ($LASTEXITCODE -ne 0) { throw "Gitleaks scan failed." }
    } finally { Pop-Location }
  }
} finally {
  Pop-Location
}
