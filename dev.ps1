<#
.SYNOPSIS
  Unified development launcher for FastAPI backend and React frontend (PowerShell).
.DESCRIPTION
  Creates/activates Python venv (backend/.venv), installs dependencies if needed,
  loads backend .env file, starts backend (uvicorn) and then starts frontend (npm start).
  Cleans up backend process when script exits (Ctrl+C supported).
.PARAMETER BackendPort
  Port to run the backend on (default 8000). Overrides BACKEND_PORT env variable.
.PARAMETER ReinstallPython
  Force reinstall of Python dependencies from requirements.txt.
.PARAMETER Quiet
  Suppress non-essential log messages.
.EXAMPLE
  ./dev.ps1
.EXAMPLE
  ./dev.ps1 -BackendPort 8081
.EXAMPLE
  ./dev.ps1 -ReinstallPython
.NOTES
  Run from repository root. Requires Python, Node.js, npm.
#>
param(
    [int]$BackendPort = 8000,
    [switch]$ReinstallPython,
    [switch]$Quiet
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Log {
    param([string]$Message, [string]$Level = 'INFO')
    if ($Quiet -and $Level -eq 'INFO') { return }
    $color = switch ($Level) { 'INFO' { 'Cyan' } 'WARN' { 'Yellow' } 'ERROR' { 'Red' } 'OK' { 'Green' } default { 'White' } }
    Write-Host "[dev][$Level] $Message" -ForegroundColor $color
}

function Test-CommandExists {
    param([string]$Name, [string]$InstallHint)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        Write-Log "Command '$Name' not found. $InstallHint" 'ERROR'
        throw "Missing dependency: $Name"
    }
}

# --- Pre-flight checks -----------------------------------------------------
Write-Log "Checking required commands..."
Test-CommandExists -Name python -InstallHint 'Install Python 3.10+ from https://www.python.org/downloads/'
Test-CommandExists -Name node -InstallHint 'Install Node.js LTS from https://nodejs.org/'
Test-CommandExists -Name npm -InstallHint 'Node.js installer provides npm.'

Write-Log "Python: $(python --version)" 'OK'
Write-Log "Node: $(node --version)" 'OK'
Write-Log "npm: $(npm --version)" 'OK'

# --- Backend setup ---------------------------------------------------------
$repoRoot = Split-Path -Parent $PSCommandPath
$backendDir = Join-Path $repoRoot 'backend'
$requirements = Join-Path $repoRoot 'requirements.txt'
if (-not (Test-Path $backendDir)) { throw "Backend directory not found at $backendDir" }

Set-Location $backendDir
if (-not (Test-Path '.venv')) {
    Write-Log 'Creating Python virtual environment (.venv)'
    python -m venv .venv
}

$activate = Join-Path $backendDir '.venv/Scripts/Activate.ps1'
. $activate
Write-Log "Virtual environment activated." 'OK'

if ($ReinstallPython) {
    Write-Log 'Reinstalling Python dependencies (forced).'
    if (Test-Path $requirements) { pip install --upgrade -r $requirements } else { Write-Log 'requirements.txt not found; skipping.' 'WARN' }
}
elseif (-not (Get-Command uvicorn -ErrorAction SilentlyContinue)) {
    Write-Log 'Installing Python dependencies (uvicorn missing).'
    if (Test-Path $requirements) { pip install -r $requirements } else { Write-Log 'requirements.txt not found; skipping.' 'WARN' }
}
else {
    Write-Log 'Python dependencies appear installed.' 'OK'
}

# Load env variables from backend/.env if present
$envFile = Join-Path $backendDir '.env'
if (Test-Path $envFile) {
    Write-Log 'Loading backend .env variables'
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^\s*#') { return }
        if ($_ -match '^\s*$') { return }
        if ($_ -match '^(?<key>[^=]+)=(?<val>.*)$') {
            $key = $Matches['key'].Trim()
            $val = $Matches['val']
            # Use Set-Item for dynamic environment variable assignment under StrictMode
            Set-Item -Path "Env:$key" -Value $val
        }
    }
}
else {
    Write-Log 'No backend .env found (optional).' 'WARN'
}

if ($env:BACKEND_PORT) { $BackendPort = [int]$env:BACKEND_PORT }
if (-not $env:FRONT_END_URL) { $env:FRONT_END_URL = 'http://localhost:3000' }

Write-Log "Backend will run on port $BackendPort" 'INFO'

# Start backend process
Write-Log 'Starting backend (python -m uvicorn main:app --reload)' 'INFO'
$backendProc = Start-Process -FilePath python -ArgumentList '-m','uvicorn','main:app','--reload','--port',"$BackendPort" -PassThru -WorkingDirectory $backendDir -WindowStyle Hidden
Start-Sleep -Milliseconds 800
if ($backendProc.HasExited) { throw "Backend failed to start. Exit code: $($backendProc.ExitCode)" }
Write-Log "Backend started (PID=$($backendProc.Id))" 'OK'

# --- Frontend setup --------------------------------------------------------
$frontendDir = Join-Path $repoRoot 'frontend'
if (-not (Test-Path $frontendDir)) { throw "Frontend directory not found at $frontendDir" }
Set-Location $frontendDir

if (-not (Test-Path (Join-Path $frontendDir 'node_modules'))) {
    Write-Log 'Installing frontend dependencies (npm install)'
    npm install
} else {
    Write-Log 'Frontend dependencies present.' 'OK'
}

# CRA env file optional
$feEnv = Join-Path $frontendDir '.env'
if (Test-Path $feEnv) { Write-Log 'Frontend .env detected.' 'INFO' }
if (-not $env:REACT_APP_API_BASE_URL) { $env:REACT_APP_API_BASE_URL = "http://localhost:$BackendPort" }

Write-Log 'Starting frontend (npm start)' 'INFO'
# Run npm start in current console so developer sees live output

$cancelled = $false
$handler = Register-EngineEvent -SourceIdentifier ConsoleCancelEvent -Action { 
    Write-Log 'Ctrl+C detected. Shutting down...' 'WARN'
    $script:cancelled = $true
}

try {
    npm start
}
finally {
    Write-Log 'Stopping backend process...' 'INFO'
    if ($backendProc -and -not $backendProc.HasExited) {
        try { $backendProc.CloseMainWindow() | Out-Null } catch {}
        Start-Sleep -Milliseconds 300
        if (-not $backendProc.HasExited) {
            try { $backendProc.Kill() } catch {}
        }
    }
    Write-Log 'Backend stopped.' 'OK'
    if ($handler) { Unregister-Event -SourceIdentifier ConsoleCancelEvent -ErrorAction SilentlyContinue }
    Set-Location $repoRoot
    if ($cancelled) { Write-Log 'Session terminated by user.' 'WARN' } else { Write-Log 'Session ended.' 'OK' }
}

Write-Log "Frontend: http://localhost:3000" 'INFO'
Write-Log "Backend: http://localhost:$BackendPort/status" 'INFO'
