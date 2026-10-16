param(
  [ValidateSet("quick", "full")]
  [string]$Mode = "quick"
)

$ErrorActionPreference = "Stop"
$Runner = Join-Path $PSScriptRoot "verify_runner.py"
python $Runner --mode $Mode
exit $LASTEXITCODE
