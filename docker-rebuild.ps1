# Quick rebuild script for Docker containers
# Usage: .\docker-rebuild.ps1

param(
    [switch]$Dev
)

Write-Host "=== Docker Rebuild Script ===" -ForegroundColor Cyan
Write-Host ""

# Determine which compose file
if ($Dev) {
    $composeFile = "docker-compose.dev.yml"
    Write-Host "Rebuilding DEVELOPMENT containers..." -ForegroundColor Yellow
} else {
    $composeFile = "docker-compose.yml"
    Write-Host "Rebuilding PRODUCTION containers..." -ForegroundColor Yellow
}

# Stop containers
Write-Host "Stopping containers..." -ForegroundColor Yellow
docker compose -f $composeFile down

# Rebuild without cache
Write-Host "Rebuilding images (no cache)..." -ForegroundColor Yellow
docker compose -f $composeFile build --no-cache

# Start containers
Write-Host "Starting containers..." -ForegroundColor Yellow
docker compose -f $composeFile up -d

# Show status
Write-Host ""
Write-Host "=== Rebuild Complete ===" -ForegroundColor Green
Write-Host ""
docker compose -f $composeFile ps

Write-Host ""
Write-Host "Access the application at:" -ForegroundColor Cyan
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor White

