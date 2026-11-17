$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $python)) {
    $python = (Get-Command python -ErrorAction Stop).Source
}

$address = "http://127.0.0.1:5000"
$env:PYTHONPATH = Join-Path $projectRoot "src"

# Reuse a server that is already listening on the site's development port.
$existing = Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue
if ($existing) {
    Start-Process $address
    Write-Host "Opened the site already running at $address"
    exit 0
}

$server = Start-Process -FilePath $python `
    -ArgumentList @("-m", "flask", "--app", "portfolio:create_app", "run", "--debug", "--host", "127.0.0.1", "--port", "5000") `
    -WorkingDirectory $projectRoot `
    -PassThru `
    -NoNewWindow

Write-Host "Starting the site at $address ..."
for ($attempt = 0; $attempt -lt 40; $attempt++) {
    if ($server.HasExited) {
        throw "The Flask server exited. Check that dependencies are installed (see README.md)."
    }

    $ready = Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue
    if ($ready) { break }
    Start-Sleep -Milliseconds 500
}

if (-not $ready) {
    Stop-Process -Id $server.Id -ErrorAction SilentlyContinue
    throw "The site did not start listening on port 5000."
}

Start-Process $address
Write-Host "Site opened in your browser. Press Ctrl+C here to stop the server."
$server.WaitForExit()
