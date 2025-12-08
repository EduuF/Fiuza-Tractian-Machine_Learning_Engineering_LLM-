Write-Host "=== 1. Running ISORT (Import Sorting) ===" -ForegroundColor Cyan
isort .
if ($LASTEXITCODE -ne 0) { Write-Host "ISORT Failed!" -ForegroundColor Red; exit 1 }

Write-Host "=== 2. Running BLACK (Code Formatting) ===" -ForegroundColor Cyan
black .
if ($LASTEXITCODE -ne 0) { Write-Host "BLACK Failed!" -ForegroundColor Red; exit 1 }

Write-Host "=== 3. Running FLAKE8 (Style Enforcement) ===" -ForegroundColor Cyan
flake8 .
if ($LASTEXITCODE -ne 0) { Write-Host "FLAKE8 Failed!" -ForegroundColor Red; exit 1 }

Write-Host "=== 4. Running MYPY (Static Type Checking) ===" -ForegroundColor Cyan
mypy .
if ($LASTEXITCODE -ne 0) { Write-Host "MYPY Failed!" -ForegroundColor Red; exit 1 }

Write-Host "✅ ALL CHECKS PASSED! Code is clean." -ForegroundColor Green