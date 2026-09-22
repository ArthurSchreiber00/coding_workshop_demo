<#
.SYNOPSIS
  Toolshed Quick Start: Python finden, .venv anlegen, Abhängigkeiten installieren,
  Tests ausführen, App starten und prüfen, ob die Website antwortet.

.EXAMPLE
  .\quickstart.ps1                 # alles
  .\quickstart.ps1 -SkipTests      # ohne Tests
  .\quickstart.ps1 -Port 8080      # anderer Port
  .\quickstart.ps1 -CheckOnly      # nur prüfen, ob die Website läuft
  .\quickstart.ps1 -NoBrowser      # Browser nicht öffnen
  .\quickstart.ps1 -StopAfterCheck # App nach erfolgreicher Prüfung wieder beenden (z. B. CI)
#>
param(
    [int]$Port = 8000,
    [switch]$SkipTests,
    [switch]$CheckOnly,
    [switch]$NoBrowser,
    [switch]$StopAfterCheck
)

$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

function Write-Step($msg) { Write-Host "" ; Write-Host "==> $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "    OK      $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "    HINWEIS $msg" -ForegroundColor Yellow }
function Fail($msg)       { Write-Host "    FEHLER  $msg" -ForegroundColor Red; exit 1 }

$isWin = ($env:OS -eq "Windows_NT")
if ($isWin) { $venvPython = Join-Path $root ".venv\Scripts\python.exe" }
else        { $venvPython = Join-Path $root ".venv/bin/python" }

function Get-Website {
    param([int]$TimeoutSec = 30)
    $url = "http://127.0.0.1:$Port/api/items"
    $deadline = (Get-Date).AddSeconds($TimeoutSec)
    while ((Get-Date) -lt $deadline) {
        try {
            $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 3
            if ($resp.StatusCode -eq 200) { return $resp }
        } catch { Start-Sleep -Milliseconds 500 }
    }
    return $null
}

function Show-Result($resp) {
    $count = @($resp.Content | ConvertFrom-Json).Count
    Write-Ok "Website läuft: http://127.0.0.1:$Port  ($count Geräte in der API)"
    Write-Host "            Oberfläche: http://127.0.0.1:$Port"
    Write-Host "            API-Doku:   http://127.0.0.1:$Port/docs"
}

# ---------------------------------------------------------------- CheckOnly
if ($CheckOnly) {
    Write-Step "Prüfe Website auf Port $Port"
    $resp = Get-Website -TimeoutSec 5
    if ($resp) { Show-Result $resp; exit 0 }
    Fail "Keine Antwort von http://127.0.0.1:$Port - läuft die App? Start: .\quickstart.ps1"
}

# ---------------------------------------------------------------- Python
Write-Step "Python suchen (mindestens 3.10)"
$py = $null
$candidates = @(
    @{ Exe = "py";      Args = @("-3") },
    @{ Exe = "python";  Args = @() },
    @{ Exe = "python3"; Args = @() }
)
foreach ($c in $candidates) {
    if (-not (Get-Command $c.Exe -ErrorAction SilentlyContinue)) { continue }
    $cargs = @($c.Args)
    $out = (& $c.Exe @cargs --version 2>&1 | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) { continue }
    if ($out -match "Python 3\.(\d+)") {
        if ([int]$Matches[1] -ge 10) { $py = $c; Write-Ok "$out  (Befehl: $($c.Exe) $($cargs -join ' '))"; break }
        else { Write-Warn "$out ist zu alt (mindestens 3.10)" }
    }
}
if (-not $py) {
    Fail "Kein passendes Python gefunden. Python 3.11+ von https://www.python.org/downloads/ installieren ('Add python.exe to PATH' anhaken)."
}

# ---------------------------------------------------------------- venv
Write-Step "Virtuelles Environment .venv"
if (Test-Path $venvPython) {
    Write-Ok "vorhanden"
} else {
    $cargs = @($py.Args) + @("-m", "venv", ".venv")
    & $py.Exe @cargs
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $venvPython)) { Fail ".venv konnte nicht angelegt werden." }
    Write-Ok "angelegt"
}

# ---------------------------------------------------------------- Abhängigkeiten
Write-Step "Abhängigkeiten installieren (requirements.txt)"
& $venvPython -m pip install --disable-pip-version-check -q -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Fail 'pip install fehlgeschlagen. Firmenproxy? Dann vorher setzen:  $env:HTTPS_PROXY = "http://proxy:port"'
}
Write-Ok "installiert"

# ---------------------------------------------------------------- Tests
if (-not $SkipTests) {
    Write-Step "Tests ausführen"
    & $venvPython -m pytest -q -p no:warnings
    if ($LASTEXITCODE -ne 0) { Fail "Tests fehlgeschlagen (Ausgabe oben)." }
    Write-Ok "alle Tests grün"
}

# ---------------------------------------------------------------- App starten
Write-Step "App starten auf Port $Port"
$proc = $null
$already = Get-Website -TimeoutSec 2
if ($already) {
    Write-Warn "Auf Port $Port antwortet bereits eine App - nichts gestartet."
    $resp = $already
} else {
    $serverArgs = @("-m", "uvicorn", "app.main:app", "--port", "$Port")
    if ($isWin) {
        $proc = Start-Process -FilePath $venvPython -ArgumentList $serverArgs -WorkingDirectory $root -PassThru
        Write-Ok "gestartet in eigenem Fenster (PID $($proc.Id)). Beenden: Fenster schließen oder  Stop-Process -Id $($proc.Id)"
    } else {
        $proc = Start-Process -FilePath $venvPython -ArgumentList $serverArgs -WorkingDirectory $root -PassThru -RedirectStandardError (Join-Path $root ".quickstart-server.log")
        Write-Ok "gestartet im Hintergrund (PID $($proc.Id), Log: .quickstart-server.log). Beenden: kill $($proc.Id)"
    }
    Write-Step "Warte auf die Website"
    $resp = Get-Website -TimeoutSec 30
}

if (-not $resp) {
    Fail "Die App antwortet nicht auf http://127.0.0.1:$Port. Fehlermeldung im Server-Fenster prüfen."
}
Show-Result $resp

$page = Invoke-WebRequest -Uri "http://127.0.0.1:$Port/" -UseBasicParsing -TimeoutSec 5
if ($page.Content -match "Toolshed" -and $page.Content -match "bersicht") { Write-Ok "Startseite rendert (Toolshed / Übersicht)" }
else { Write-Warn "Startseite antwortet, enthält aber nicht den erwarteten Inhalt." }

if ($StopAfterCheck) {
    if ($proc) { Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue; Write-Ok "App wieder beendet (-StopAfterCheck)" }
} elseif (-not $NoBrowser) {
    Start-Process "http://127.0.0.1:$Port"
}

Write-Host ""
Write-Host "Fertig. Nächster Schritt: exercises\00-setup.md" -ForegroundColor Cyan
exit 0
