# PowerShell script to start Docker containers for SynapseSquad application
# Usage: 
#   .\docker-start.ps1           # Production build (default)
#   .\docker-start.ps1 -Dev      # Development with hot-reload

param(
    [switch]$Dev
)

Write-Host "=== SynapseSquad Docker Startup Script ===" -ForegroundColor Cyan
if ($Dev) {
    Write-Host "Mode: Development (hot-reload enabled)" -ForegroundColor Yellow
} else {
    Write-Host "Mode: Production (optimized build)" -ForegroundColor Green
}
Write-Host ""

# Check if Docker is installed and running
Write-Host "Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker command failed"
    }
    Write-Host "Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Docker is not installed or not running." -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Red
    exit 1
}

# Check if Docker daemon is running
Write-Host "Checking Docker daemon..." -ForegroundColor Yellow
try {
    docker info 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker daemon not running"
    }
    Write-Host "Docker daemon is running" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Docker Desktop is not running." -ForegroundColor Red
    Write-Host "Please start Docker Desktop and wait for it to fully initialize." -ForegroundColor Yellow
    Write-Host "Then run this script again." -ForegroundColor Yellow
    exit 1
}

# Check if docker-compose is available
Write-Host "Checking Docker Compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker compose version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker Compose command failed"
    }
    Write-Host "Docker Compose found: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Docker Compose is not available." -ForegroundColor Red
    Write-Host "Please ensure you have Docker Desktop with Compose V2 installed." -ForegroundColor Red
    exit 1
}

# Check if .env file exists
Write-Host ""
Write-Host "Checking environment configuration..." -ForegroundColor Yellow
if (-Not (Test-Path ".env")) {
    Write-Host "WARNING: .env file not found. Using default values." -ForegroundColor Yellow
    Write-Host "For custom configuration, create a .env file based on env.docker.example" -ForegroundColor Yellow
} else {
    Write-Host ".env file found" -ForegroundColor Green
}

# Check if node_modules exists for frontend
Write-Host ""
Write-Host "Checking frontend dependencies..." -ForegroundColor Yellow
if (-Not (Test-Path "frontend\node_modules")) {
    Write-Host "WARNING: frontend/node_modules not found." -ForegroundColor Yellow
    Write-Host "Please run 'cd frontend && npm install --legacy-peer-deps' first." -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Continue anyway? (y/N)"
    if ($response -ne "y" -and $response -ne "Y") {
        Write-Host "Exiting. Please install dependencies first." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "node_modules found - using local packages" -ForegroundColor Green
}

# Determine which compose file to use
if ($Dev) {
    $composeFile = "docker-compose.dev.yml"
    Write-Host "Using development configuration..." -ForegroundColor Yellow
} else {
    $composeFile = "docker-compose.yml"
    Write-Host "Using production configuration..." -ForegroundColor Yellow
}

# Stop any existing containers
Write-Host ""
Write-Host "Stopping any existing containers..." -ForegroundColor Yellow
docker compose -f $composeFile down 2>$null

# Clean up corrupted images if any
Write-Host "Cleaning up old images..." -ForegroundColor Yellow
docker image prune -f 2>$null | Out-Null

# Build and start containers
Write-Host ""
Write-Host "Building and starting containers..." -ForegroundColor Yellow
Write-Host "This may take a few minutes on first run..." -ForegroundColor Cyan
if (-not $Dev) {
    Write-Host "Building production bundle with 'npm run build'..." -ForegroundColor Cyan
}
Write-Host ""

docker compose -f $composeFile up --build -d

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== Containers started successfully! ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Services are available at:" -ForegroundColor Cyan
    Write-Host "  Frontend: http://localhost:3000" -ForegroundColor White
    Write-Host "  Backend:  http://localhost:8000" -ForegroundColor White
    Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor White
    Write-Host ""
    if ($Dev) {
        Write-Host "Development mode: Code changes will hot-reload automatically" -ForegroundColor Cyan
    } else {
        Write-Host "Production mode: Optimized build with nginx serving static files" -ForegroundColor Cyan
    }
    Write-Host ""
    Write-Host "Useful commands:" -ForegroundColor Cyan
    Write-Host "  View logs:        docker compose -f $composeFile logs -f" -ForegroundColor White
    Write-Host "  Stop containers:  docker compose -f $composeFile down" -ForegroundColor White
    Write-Host "  Restart:          docker compose -f $composeFile restart" -ForegroundColor White
    Write-Host "  View status:      docker compose -f $composeFile ps" -ForegroundColor White
    Write-Host ""
    Write-Host "Checking container status..." -ForegroundColor Yellow
    docker compose -f $composeFile ps
} else {
    Write-Host ""
    Write-Host "ERROR: Failed to start containers." -ForegroundColor Red
    Write-Host "Check the logs above for details." -ForegroundColor Red
    Write-Host "You can also run: docker compose logs" -ForegroundColor Yellow
    exit 1
}

